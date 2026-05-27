# Error Handling and Audit Logging

Infrastructure for structured validation errors and audit trail tracking in the domainization system.

## Modules

| File | Purpose |
|------|---------|
| `validation_error_classes.py` | Structured error types with codes E001–E010 |
| `audit_logger.py` | Audit trail for all governance-relevant events |
| `test_validation_error_classes.py` | 38 unit tests for error classes |
| `test_audit_logger.py` | 35 unit tests for audit logging |

---

## Validation Error Classes

### Error Codes

| Code | Description | Default Severity |
|------|-------------|-----------------|
| E001 | Artifact not registered | HIGH |
| E002 | Invalid domain assignment | HIGH |
| E003 | Invalid lifecycle transition | MEDIUM |
| E004 | Domain boundary violation | HIGH |
| E005 | SSOT conflict detected | CRITICAL |
| E006 | Missing required metadata | MEDIUM |
| E007 | Deprecated artifact modification | HIGH |
| E008 | Authority chain violation | CRITICAL |
| E009 | Forbidden cloud provider reference | CRITICAL |
| E010 | Feature without report value | LOW |

### Enforcement Modes

- **WARNING** (default during FAST LANE phase): Errors are reported but do not block commits.
- **BLOCKING** (post-MVP enforcement): Critical/high errors block commits.

### Usage

```python
from validation_error_classes import (
    ValidationError,
    ErrorCode,
    EnforcementMode,
    create_registration_error,
    create_invalid_domain_error,
    create_authority_chain_error,
)

# Using a convenience factory function
error = create_registration_error(
    artifact_id="my_file_md",
    file_path="docs/my_file.md",
)
print(error.format_error())
# 🟠 [E001] Gate 1: Artifact Registration (WARNING)
#
#   Artifact: my_file_md
#   Error:    Artifact 'docs/my_file.md' is not registered in the domainization system
#
#   Suggestion: Add YAML frontmatter to markdown files or register in artifact_registry.yaml...

# Using the generic factory with overrides
error = ValidationError.from_error_code(
    gate_name="Gate 4: Boundary Enforcement",
    artifact_id="engine_py",
    error_code=ErrorCode.E008_AUTHORITY_CHAIN_VIOLATION,
    enforcement_mode=EnforcementMode.BLOCKING,
)
assert error.is_blocking() is True
```

### Available Factory Functions

| Function | Error Code | Gate |
|----------|-----------|------|
| `create_registration_error()` | E001 | Gate 1 |
| `create_invalid_domain_error()` | E002 | Gate 2 |
| `create_invalid_lifecycle_error()` | E003 | Gate 3 |
| `create_boundary_violation_error()` | E004 | Gate 4 |
| `create_ssot_conflict_error()` | E005 | Gate 5 |
| `create_missing_metadata_error()` | E006 | Gate 1 |
| `create_deprecated_modification_error()` | E007 | Gate 3 |
| `create_authority_chain_error()` | E008 | Gate 4 |
| `create_forbidden_provider_error()` | E009 | Gate 2 |
| `create_no_report_value_error()` | E010 | Gate 5 |

---

## Audit Logger

### Event Types

| Event Type | Tracked Action |
|-----------|----------------|
| `artifact_registered` | New artifact added to registry |
| `metadata_changed` | Artifact metadata field updated |
| `lifecycle_transition` | Lifecycle state change |
| `validation_failure` | Commit gate validation error/warning |
| `bypass_used` | `--no-verify` or similar bypass |
| `registry_modified` | Registry file write operation |

### Log File Format

- Location: `.domainization/logs/audit_YYYY-MM-DD.log`
- Format: One JSON object per line (JSONL)
- Rotation: Daily (new file per day)
- Retention: Configurable, default 30 days

### Log Entry Structure

```json
{
  "timestamp": "2025-05-25T14:30:00",
  "event_type": "lifecycle_transition",
  "artifact_id": "allocation_engine_py",
  "domain": "SIGNALS",
  "details": {
    "from_state": "development",
    "to_state": "active"
  }
}
```

### Usage

```python
from audit_logger import AuditLogger

logger = AuditLogger()

# Log artifact registration
logger.log_registration(
    artifact_id="my_doc_md",
    domain="ARCH",
    artifact_type="SSOT",
    file_path="docs/my_doc.md",
)

# Log lifecycle transition
logger.log_lifecycle_transition(
    artifact_id="engine_py",
    from_state="development",
    to_state="active",
    domain="SIGNALS",
)

# Log validation failure
logger.log_validation_failure(
    error_code="E001",
    artifact_id="unregistered_file",
    gate_name="Gate 1: Artifact Registration",
    error_message="Artifact not registered",
)

# Log bypass usage
logger.log_bypass(
    reason="Emergency hotfix",
    context="pre-commit hook",
)

# Rotate old logs (call periodically or via CLI)
removed = logger.rotate_logs()

# Read today's entries
entries = logger.read_log_entries()

# Filter by event type
from audit_logger import AuditEventType
failures = logger.read_log_entries(event_type=AuditEventType.VALIDATION_FAILURE)
```

### Configuration

```python
# Custom logs directory and retention
logger = AuditLogger(
    logs_dir="/path/to/custom/logs",
    retention_days=7,
)

# Disable logging (e.g., in tests)
logger = AuditLogger(enabled=False)

# Toggle at runtime
logger.enabled = False
```

---

## Running Tests

```bash
cd .domainization/src
pytest test_validation_error_classes.py -v
pytest test_audit_logger.py -v
```

---

## Design Decisions

1. **Warning-first**: All errors default to `enforcement_mode="warning"` during FAST LANE phase. No commits are blocked until post-MVP enforcement is enabled.
2. **Structured JSON logs**: Machine-parseable JSONL format enables downstream analysis and health reporting.
3. **Thread-safe writes**: `threading.Lock` ensures concurrent validation runs do not corrupt log files.
4. **Factory pattern**: Convenience functions reduce boilerplate and ensure consistent error formatting across all 5 commit gates.
5. **Configurable retention**: Log rotation prevents unbounded disk usage while preserving audit history.
