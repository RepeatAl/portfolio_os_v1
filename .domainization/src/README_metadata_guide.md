# Metadata Guide

## Overview

Every artifact in Portfolio OS must have metadata that identifies its domain ownership, lifecycle status, and access permissions. This guide explains how to add metadata to artifacts using either YAML frontmatter (for markdown files) or the central artifact registry (for non-markdown files).

The metadata schema is defined in `artifact_schema.py` and validated automatically by the domainization system's validation observers.

## Features

- Consistent metadata schema across all artifact types
- YAML frontmatter support for markdown files
- Central registry for non-markdown files (Python, Excel, JSON, etc.)
- Automatic schema validation with actionable error messages
- Permission-based access control (writers and readers)
- SSOT relationship tracking for document authority chains

## Required Metadata Fields

Every artifact must include these fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `artifact_id` | string | Unique identifier for the artifact | `system_architecture_md` |
| `file_path` | string | Relative path from repo root | `docs/system_architecture.md` |
| `primary_domain` | string | Domain ID from domain_registry.yaml | `ARCH` |
| `artifact_type` | string | Type ID from lifecycle_state_machine.yaml | `SSOT` |
| `lifecycle_status` | string | Current state from the type's state machine | `canonical` |
| `created_date` | string | Creation date in YYYY-MM-DD format | `2026-01-15` |
| `last_modified` | string | Last modification date in YYYY-MM-DD format | `2026-05-25` |
| `owner_role` | string | Responsibility description | `System architect` |
| `ssot_relationship` | string | One of: `canonical`, `derived`, `implementation`, `none` | `canonical` |
| `allowed_writers` | list[string] | Domain IDs with write permission | `[ARCH]` |
| `allowed_readers` | list[string] | Domain IDs with read permission (`ALL` for public) | `[ALL]` |


## Optional Metadata Fields

These fields provide additional context and are recommended but not required:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `secondary_domains` | list[string] | Additional domain associations | `[USER, DEPLOY]` |
| `dependencies` | list[string] | Artifact IDs this artifact depends on | `[report_reasoning_system_md]` |
| `topic` | string | Topic for SSOT conflict detection | `system_architecture` |
| `description` | string | Human-readable description | `"Defines system architecture"` |
| `tags` | list[string] | Categorization tags | `[architecture, design]` |

## Valid Values Reference

### Domain IDs (primary_domain)

Core reasoning domains: `SIGNALS`, `SEMANTICS`, `REASONING`, `REPORT`

Surface domains: `GOV`, `ARCH`, `STATE`, `DATA`, `USER`, `DEPLOY`, `MEMORY`, `SIM`

### Artifact Types (artifact_type)

`SSOT`, `ENGINE`, `REPORT_OUT`, `DATA_IN`, `DATA_OUT`, `RUNTIME`, `DASHBOARD`, `SNAPSHOT`, `CONFIG`, `CALIBRATION`, `STEERING`

### SSOT Relationships (ssot_relationship)

- `canonical` — This is the authoritative source for its topic
- `derived` — This document derives from a canonical SSOT (must reference it in dependencies)
- `implementation` — This artifact implements a specification (must reference SSOT in dependencies)
- `none` — No SSOT relationship (used for data outputs, runtime artifacts, etc.)

### Lifecycle States by Artifact Type

| Artifact Type | Valid States |
|---------------|-------------|
| SSOT | `draft`, `review`, `canonical`, `deprecated` |
| ENGINE | `planned`, `development`, `active`, `deprecated` |
| REPORT_OUT | `generated`, `current`, `archived` |
| DATA_IN | `active`, `stale`, `archived` |
| DATA_OUT | `generated`, `current`, `archived` |
| RUNTIME | `planned`, `development`, `active`, `deprecated` |
| DASHBOARD | `planned`, `development`, `active`, `deprecated` |
| SNAPSHOT | `current`, `archived` |
| CONFIG | `active`, `deprecated` |
| CALIBRATION | `draft`, `active`, `deprecated` |
| STEERING | `draft`, `active`, `deprecated` |


## How to Add YAML Frontmatter (Markdown Files)

Markdown files embed metadata directly in the file using YAML frontmatter. The frontmatter block is placed at the very beginning of the file, enclosed by `---` delimiters.

### Frontmatter Format

```markdown
---
artifact_id: my_document_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-01-15
last_modified: 2026-05-25
owner_role: System architect
ssot_relationship: canonical
topic: my_topic
allowed_writers: [ARCH]
allowed_readers: [ALL]
---

# Document Title

Your document content starts here...
```

### Rules for Frontmatter

1. The `---` delimiter must be the very first line of the file (no blank lines before it)
2. The closing `---` must appear on its own line
3. All required fields must be present
4. Date values use `YYYY-MM-DD` format (no quotes needed in frontmatter)
5. Lists can use inline format `[ARCH, GOV]` or block format:
   ```yaml
   allowed_writers:
     - ARCH
     - GOV
   ```

### Complete SSOT Document Example

```markdown
---
artifact_id: report_reasoning_system_md
primary_domain: REPORT
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-02-01
last_modified: 2026-05-25
owner_role: Report generation architect
ssot_relationship: canonical
topic: report_reasoning
allowed_writers: [REPORT]
allowed_readers: [ALL]
---

# Report Reasoning System

This document defines how reasoning outputs are transformed into report language...
```

### Complete ENGINE Document Example (Markdown)

```markdown
---
artifact_id: custom_engine_design_md
primary_domain: SIGNALS
artifact_type: SSOT
lifecycle_status: draft
created_date: 2026-05-25
last_modified: 2026-05-25
owner_role: Signal generation engineer
ssot_relationship: canonical
topic: custom_engine_design
allowed_writers: [SIGNALS]
allowed_readers: [ALL]
dependencies:
  - signal_calculation_framework_md
---

# Custom Engine Design

Design specification for a new signal generation engine...
```


## How to Register in artifact_registry.yaml (Non-Markdown Files)

Non-markdown files (Python, Excel, JSON, YAML, etc.) cannot embed frontmatter. These artifacts are registered in the central registry file at `.domainization/artifact_registry.yaml`.

### Registry Entry Format

Each entry is a YAML dictionary under the `artifacts:` key:

```yaml
artifacts:
  - artifact_id: my_engine_py
    file_path: engines/my_engine.py
    primary_domain: SIGNALS
    artifact_type: ENGINE
    lifecycle_status: active
    created_date: "2026-05-25"
    last_modified: "2026-05-25"
    owner_role: Signal generation engineer
    ssot_relationship: implementation
    allowed_writers:
      - SIGNALS
    allowed_readers:
      - ALL
    dependencies:
      - signal_calculation_framework_md
    description: "Generates custom signals for portfolio analysis"
    tags:
      - signals
      - custom
```

### Rules for Registry Entries

1. Add entries under the `artifacts:` key in `.domainization/artifact_registry.yaml`
2. The `artifact_id` must be unique across the entire registry
3. Date values must be quoted strings in YYYY-MM-DD format: `"2026-05-25"`
4. Lists use YAML block format (indented with `-`)
5. The `file_path` is relative to the repository root
6. Optional fields can be omitted entirely (do not include empty values)

### Naming Convention for artifact_id

Use the file name with underscores replacing dots and path separators:

| File Path | artifact_id |
|-----------|-------------|
| `engines/allocation_engine.py` | `allocation_engine_py` |
| `data/market_snapshot.xlsx` | `market_snapshot_xlsx` |
| `portfolio_output.xlsx` | `portfolio_output_xlsx` |
| `main.py` | `main_py` |
| `reports/pm_report_engine.py` | `pm_report_engine_py` |

### Using the CLI to Register

You can also register artifacts using the CLI:

```bash
# Register a new artifact
python -m domainization register \
  --artifact-id my_engine_py \
  --file-path engines/my_engine.py \
  --primary-domain SIGNALS \
  --artifact-type ENGINE \
  --lifecycle-status active \
  --owner-role "Signal generation engineer" \
  --ssot-relationship implementation \
  --allowed-writers SIGNALS \
  --allowed-readers ALL
```

### Using the Python API to Register

```python
import sys
sys.path.insert(0, '.domainization/src')

from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata

# Initialize registry
registry = ArtifactRegistry()
registry.load()

# Create metadata
metadata = ArtifactMetadata(
    artifact_id="my_engine_py",
    file_path="engines/my_engine.py",
    primary_domain="SIGNALS",
    artifact_type="ENGINE",
    lifecycle_status="active",
    created_date="2026-05-25",
    last_modified="2026-05-25",
    owner_role="Signal generation engineer",
    ssot_relationship="implementation",
    allowed_writers=["SIGNALS"],
    allowed_readers=["ALL"],
    dependencies=["signal_calculation_framework_md"],
    description="Generates custom signals for portfolio analysis",
    tags=["signals", "custom"]
)

# Validate and register
is_valid, errors = metadata.validate()
if is_valid:
    registry.register_artifact(metadata)
    registry.save()
else:
    print(f"Validation errors: {errors}")
```


## Templates by Artifact Type

### Template: SSOT Document (Markdown with Frontmatter)

```yaml
---
artifact_id: <filename_without_extension>_md
primary_domain: <DOMAIN_ID>
artifact_type: SSOT
lifecycle_status: draft
created_date: <YYYY-MM-DD>
last_modified: <YYYY-MM-DD>
owner_role: <role description>
ssot_relationship: canonical
topic: <topic_name>
allowed_writers: [<PRIMARY_DOMAIN>]
allowed_readers: [ALL]
---
```

### Template: ENGINE (Python file in registry)

```yaml
- artifact_id: <filename>_py
  file_path: engines/<filename>.py
  primary_domain: <DOMAIN_ID>
  artifact_type: ENGINE
  lifecycle_status: development
  created_date: "<YYYY-MM-DD>"
  last_modified: "<YYYY-MM-DD>"
  owner_role: <role description>
  ssot_relationship: implementation
  allowed_writers:
    - <PRIMARY_DOMAIN>
  allowed_readers:
    - ALL
  dependencies:
    - <ssot_artifact_id>
  description: "<what this engine does>"
  tags:
    - <domain_tag>
    - <function_tag>
```

### Template: REPORT_OUT (Generated report file)

```yaml
- artifact_id: <filename>_txt
  file_path: <filename>.txt
  primary_domain: REPORT
  artifact_type: REPORT_OUT
  lifecycle_status: current
  created_date: "<YYYY-MM-DD>"
  last_modified: "<YYYY-MM-DD>"
  owner_role: Report generation system
  ssot_relationship: none
  allowed_writers:
    - REPORT
  allowed_readers:
    - ALL
  dependencies:
    - <generating_engine_artifact_id>
  description: "<what this report contains>"
  tags:
    - report
    - <report_type>
```

### Template: DATA_OUT (Generated data file)

```yaml
- artifact_id: <filename>_xlsx
  file_path: <filename>.xlsx
  primary_domain: <DOMAIN_ID>
  artifact_type: DATA_OUT
  lifecycle_status: current
  created_date: "<YYYY-MM-DD>"
  last_modified: "<YYYY-MM-DD>"
  owner_role: <generating system>
  ssot_relationship: none
  allowed_writers:
    - <PRIMARY_DOMAIN>
  allowed_readers:
    - ALL
  dependencies:
    - <generating_engine_artifact_id>
  description: "<what this data contains>"
  tags:
    - data
    - <data_type>
```

### Template: DATA_IN (External input data)

```yaml
- artifact_id: <filename>_xlsx
  file_path: data/<filename>.xlsx
  primary_domain: DATA
  artifact_type: DATA_IN
  lifecycle_status: active
  created_date: "<YYYY-MM-DD>"
  last_modified: "<YYYY-MM-DD>"
  owner_role: Data ingestion system
  ssot_relationship: none
  allowed_writers:
    - DATA
  allowed_readers:
    - ALL
  description: "<what this data source provides>"
  tags:
    - data
    - input
```

### Template: RUNTIME (Entry point)

```yaml
- artifact_id: <filename>_py
  file_path: <filename>.py
  primary_domain: DEPLOY
  artifact_type: RUNTIME
  lifecycle_status: active
  created_date: "<YYYY-MM-DD>"
  last_modified: "<YYYY-MM-DD>"
  owner_role: Deployment engineer
  ssot_relationship: implementation
  allowed_writers:
    - DEPLOY
    - ARCH
  allowed_readers:
    - ALL
  dependencies:
    - <architecture_ssot_artifact_id>
  description: "<what this runtime does>"
  tags:
    - runtime
    - <purpose>
```

### Template: DASHBOARD (UI application)

```yaml
- artifact_id: <filename>_py
  file_path: <filename>.py
  primary_domain: USER
  artifact_type: DASHBOARD
  lifecycle_status: active
  created_date: "<YYYY-MM-DD>"
  last_modified: "<YYYY-MM-DD>"
  owner_role: UI/UX engineer
  ssot_relationship: implementation
  allowed_writers:
    - USER
  allowed_readers:
    - ALL
  dependencies:
    - dashboard_philosophy_md
  description: "<what this dashboard provides>"
  tags:
    - dashboard
    - <feature>
```


## Validation and Error Messages

The domainization system validates metadata automatically. Here are common validation errors and how to fix them:

### Missing Required Field

```
Error: Missing required field: primary_domain
Fix: Add the primary_domain field with a valid domain ID from domain_registry.yaml
```

### Invalid Date Format

```
Error: created_date must be in YYYY-MM-DD format: 25-05-2026
Fix: Use ISO format dates: "2026-05-25"
```

### Invalid SSOT Relationship

```
Error: ssot_relationship must be one of ['canonical', 'derived', 'implementation', 'none']
Fix: Choose one of the valid relationship types
```

### Duplicate artifact_id

```
Error: Artifact with ID 'my_engine_py' already exists
Fix: Use a unique artifact_id. Check existing entries with:
     python -m domainization list
```

### Validating Metadata Programmatically

```python
from artifact_schema import ArtifactMetadata, validate_artifact_dict

# Validate a dictionary
artifact_dict = {
    'artifact_id': 'my_artifact',
    'file_path': 'path/to/file.py',
    'primary_domain': 'SIGNALS',
    # ... other fields
}

is_valid, errors = validate_artifact_dict(artifact_dict)
if not is_valid:
    for error in errors:
        print(f"  - {error}")
```

### Parsing Frontmatter from Existing Files

```python
from pathlib import Path
from artifact_registry import ArtifactRegistry

# Parse frontmatter from a markdown file
frontmatter = ArtifactRegistry.parse_frontmatter(Path('docs/my_document.md'))
if frontmatter:
    print(f"Domain: {frontmatter['primary_domain']}")
    print(f"Type: {frontmatter['artifact_type']}")
else:
    print("No frontmatter found")
```

## Decision Guide: Frontmatter vs Registry

| Scenario | Use Frontmatter | Use Registry |
|----------|----------------|--------------|
| Markdown documentation file | ✓ | |
| Python source file | | ✓ |
| Excel data file | | ✓ |
| JSON configuration | | ✓ |
| YAML configuration | | ✓ |
| Shell scripts | | ✓ |
| Generated text reports | | ✓ |

**Rule of thumb**: If the file supports YAML frontmatter (markdown), embed metadata there. For everything else, use `artifact_registry.yaml`.

## Testing

### Validate Schema

```bash
# Run schema validation tests
cd .domainization/src
python -m pytest test_artifact_schema.py -v

# Run registry operation tests
python -m pytest test_artifact_registry.py -v
```

### Validate Frontmatter Parsing

```bash
# Run frontmatter parsing tests
cd .domainization/src
python -m pytest test_artifact_registry.py -v -k "frontmatter"
```

### Run Full Validation

```bash
# Validate all registered artifacts
python -m domainization validate

# Validate a specific file
python -m domainization validate --file engines/my_engine.py
```

## Requirements Satisfied

This guide documents the following requirements:

- ✅ **8.1**: Metadata includes artifact_id, primary_domain, artifact_type, lifecycle_status, created_date, and last_modified
- ✅ **8.2**: Metadata optionally includes secondary_domains, owner_role, ssot_relationship, allowed_writers, allowed_readers, and dependencies
- ✅ **8.3**: YAML frontmatter is validated against the schema
- ✅ **8.4**: Artifact registry entries are validated against the schema
- ✅ **8.5**: Invalid metadata produces specific validation errors
- ✅ **8.6**: Metadata queries return all fields for the artifact

## Related Files

- `artifact_schema.py` — Metadata schema definition and validation logic
- `artifact_registry.py` — Registry operations (register, update, query, frontmatter parsing)
- `../artifact_registry.yaml` — Central artifact registry for non-markdown files
- `../domain_registry.yaml` — Valid domain definitions
- `../lifecycle_state_machine.yaml` — Valid lifecycle states per artifact type
- `test_artifact_schema.py` — Schema validation tests
- `test_artifact_registry.py` — Registry operation tests
