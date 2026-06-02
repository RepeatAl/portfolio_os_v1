# Cloud Provider Pattern Detection

## Overview

The Cloud Provider Detector module scans source files for forbidden cloud provider references (AWS, Supabase, Azure) while allowing Google Cloud Platform references. This enforces the Google-only deployment constraint for Portfolio OS.

All detection operates in **observability/warning mode only** — no blocking occurs during the FAST LANE phase.

## Features

- **Pattern-based detection** for AWS, Supabase, and Azure references
- **Allowlist for Google Cloud Platform** (GCP, googleapis, Firestore, BigQuery, etc.)
- **File scanning** with extension filtering and directory exclusion
- **Directory scanning** with recursive support
- **Line-level reporting** with provider identification and line numbers
- **Mixed-provider handling** — correctly identifies forbidden references even when allowed references are present on the same line

## Usage

### Basic Pattern Checking

```python
from cloud_provider_detector import CloudProviderDetector

detector = CloudProviderDetector()

# Check if a reference is forbidden
detector.is_forbidden_provider("import boto3")  # True (AWS)
detector.is_forbidden_provider("supabase.auth.signIn()")  # True (Supabase)
detector.is_forbidden_provider("azure.storage.blob")  # True (Azure)
detector.is_forbidden_provider("from google.cloud import storage")  # False (allowed)

# Check if a reference is allowed
detector.is_allowed_provider("googleapis.com")  # True
detector.is_allowed_provider("firestore")  # True
```

### Scanning Content

```python
content = '''
import boto3
from google.cloud import storage
client = boto3.client('s3')
'''

result = detector.scan_content(content, file_path="app.py")
print(result.has_forbidden_references)  # True
print(result.forbidden_providers)  # {'aws'}
print(result.summary())  # "Found 2 forbidden cloud provider reference(s) [aws] in app.py"
```

### Scanning Files

```python
from pathlib import Path

result = detector.scan_file(Path("src/storage_client.py"))
if result.has_forbidden_references:
    for match in result.forbidden_matches:
        print(f"  Line {match.line_number}: [{match.provider}] {match.line_content.strip()}")
```

### Scanning Directories

```python
results = detector.scan_directory(Path("src/"), recursive=True)
for result in results:
    if result.has_forbidden_references:
        print(result.summary())
```

### Retrieving Pattern Lists

```python
# Get all forbidden patterns grouped by provider
forbidden = detector.get_forbidden_patterns()
# {'aws': [...], 'supabase': [...], 'azure': [...]}

# Get all allowed patterns grouped by provider
allowed = detector.get_allowed_patterns()
# {'google': [...]}
```

## Forbidden Providers

| Provider | Example Patterns |
|----------|-----------------|
| AWS | `boto3`, `s3://`, `.amazonaws.com`, `aws-sdk`, `dynamodb`, `cloudformation`, `sagemaker` |
| Supabase | `supabase.co`, `SUPABASE_URL`, `@supabase/`, `supabase-js` |
| Azure | `azure.storage`, `.azurewebsites.net`, `.blob.core.windows.net`, `@azure/`, `cosmosdb` |

## Allowed Providers

| Provider | Example Patterns |
|----------|-----------------|
| Google | `google.cloud`, `googleapis.com`, `gcp.`, `firestore`, `bigquery`, `gs://`, `gcloud`, `google.sheets` |

## Testing

```bash
# Run unit tests for pattern detection
.venv/bin/python -m pytest .domainization/src/test_cloud_provider_detector.py -v

# Run integration tests for observer integration
.venv/bin/python -m pytest .domainization/src/test_cloud_provider_observer_integration.py -v
```

## Observer Integration

The `CloudProviderDetector` is integrated into Observer 4 (Boundary Awareness Validator) via the `scan_files_for_cloud_providers()` method. This enables cloud provider scanning as part of the commit gate validation pipeline.

### How It Works

1. Observer 4 receives a list of changed file paths
2. `scan_files_for_cloud_providers()` scans each file using `CloudProviderDetector.scan_file()`
3. For each forbidden match, a `ValidationWarning` is generated with:
   - Provider-specific warning code (W501 for AWS, W502 for Supabase, W503 for Azure)
   - Provider name in the warning message
   - File path and line number where the reference was found
   - The offending line content in the suggestion field
4. Warnings are severity "medium" — they never block commits

### Usage in Observer 4

```python
from observer_boundary_awareness import BoundaryAwarenessValidator
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from pathlib import Path

# Initialize validator
validator = BoundaryAwarenessValidator(artifact_registry, domain_registry)

# Scan specific files for cloud provider references
changed_files = [Path("src/deploy.py"), Path("src/storage.py")]
warnings = validator.scan_files_for_cloud_providers(changed_files)

for warning in warnings:
    print(warning)
    # 🟡 [BoundaryAwarenessValidator] src/deploy.py: Forbidden cloud provider
    #    reference detected: [AWS] at line 3 in src/deploy.py
    #    Suggestion: Remove or replace AWS reference. Portfolio OS uses Google
    #    Cloud Platform only. Line 3: import boto3
```

### Warning Codes

| Code | Provider | Description |
|------|----------|-------------|
| W500 | Generic | Forbidden cloud provider reference (fallback) |
| W501 | AWS | AWS service reference detected |
| W502 | Supabase | Supabase API reference detected |
| W503 | Azure | Azure infrastructure reference detected |

## Requirements Satisfied

- **11.1**: Commit gates scan for forbidden cloud provider references
- **11.2**: AWS service references are detected (warning mode)
- **11.3**: Supabase API calls are detected (warning mode)
- **11.4**: Azure infrastructure references are detected (warning mode)
- **11.5**: Google Cloud Platform references are allowed
- **11.6**: Google Sheets API references are allowed
- **11.7**: Error message specifies which provider and where it was found

## Related Files

- `cloud_provider_detector.py` — Main detection module
- `test_cloud_provider_detector.py` — Unit tests (36 tests)
- `observer_boundary_awareness.py` — Observer 4 with cloud provider integration
- `test_cloud_provider_observer_integration.py` — Integration tests (19 tests)
- `validation_result.py` — Warning codes (W500-W503)
