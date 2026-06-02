# Backup and Recovery

## Overview

The backup and recovery system provides automatic registry protection and disaster recovery for the domainization system. It creates timestamped backups before every registry write operation and provides CLI commands to list, restore, and validate backups.

## Features

### Automatic Backup (registry_backup_manager.py)
- Creates a timestamped backup before every registry write operation
- Saves backups to `.domainization/backups/` with format `{stem}_YYYY-MM-DD_HH-MM-SS.yaml`
- Enforces retention policy keeping only the last 10 backups per registry file
- Auto-creates backup directory if missing

### Recovery Operations (registry_recovery_manager.py)
- Lists all available backups with metadata (name, size, timestamp)
- Restores registry from a specific backup file
- Restores from the most recent backup (quick recovery)
- Validates restored registry integrity (schema, duplicates, structure)
- Generates health report after successful recovery
- Creates safety backup of current registry before overwriting

### CLI Commands (cli_recovery_commands.py)
- `domainization recover list` — Show available backups in a formatted table
- `domainization recover restore <backup_file>` — Restore from a specific backup
- `domainization recover latest` — Restore from the most recent backup

## Usage

### Automatic Backup (No Action Required)

Backups are created automatically whenever the artifact registry is saved:

```python
from artifact_registry import ArtifactRegistry

registry = ArtifactRegistry()
registry.load()
registry.register_artifact(metadata)
registry.save()  # Backup created automatically before write
```

### Manual Backup Operations

```python
from pathlib import Path
from registry_backup_manager import (
    create_backup,
    list_backups,
    cleanup_old_backups,
    create_backup_and_cleanup,
)

registry_path = Path('.domainization/artifact_registry.yaml')

# Create a single backup
backup_path = create_backup(registry_path)

# List all backups (oldest first)
backups = list_backups(registry_path)

# Enforce retention policy (keep last 10)
removed = cleanup_old_backups(registry_path, keep=10)

# Combined: backup + cleanup (used before every write)
backup_path = create_backup_and_cleanup(registry_path)
```

### Recovery via CLI

```bash
# List available backups
python -m cli_main recover list

# Restore from a specific backup
python -m cli_main recover restore artifact_registry_2025-05-25_14-30-00.yaml

# Restore from the most recent backup
python -m cli_main recover latest
```

### Recovery via Python API

```python
from registry_recovery_manager import RegistryRecoveryManager

manager = RegistryRecoveryManager()

# List available backups
backups = manager.list_available_backups()
for backup in backups:
    print(f"{backup['file_name']} - {backup['modified_time_str']} ({backup['file_size']} bytes)")

# Restore from specific backup
result = manager.restore_from_backup('/path/to/backup.yaml')
print(f"Success: {result['success']}")
print(f"Artifacts: {result['validation_result']['artifact_count']}")

# Restore from latest backup
result = manager.restore_latest_backup()
```

## Backup Strategy

### File Naming Convention

```
.domainization/backups/
    artifact_registry_2025-05-25_14-30-00.yaml
    artifact_registry_2025-05-25_15-00-00.yaml
    domain_registry_2025-05-25_14-30-00.yaml
    pre_recovery_20250525_143000.yaml  (safety backup before restore)
```

### Retention Policy
- Default: keep last 10 backups per registry file
- Oldest backups are removed first
- Configurable via `keep` parameter
- Safety backups (pre_recovery_*) are not subject to automatic cleanup

### Recovery Safety
- Before restoring, a safety backup of the current registry is created
- Backup files are validated before restoration (YAML parsing, schema check)
- If validation fails, the restore is aborted and current registry is preserved
- Post-restore validation confirms integrity
- Health report generated after successful recovery

## Validation After Recovery

The recovery process validates:
1. **YAML Structure** — File is valid YAML
2. **Registry Schema** — Contains `artifacts` key with a list
3. **Artifact Schema** — Each artifact has required fields
4. **Duplicate Detection** — No duplicate `artifact_id` values
5. **Health Report** — Summary of registry state after recovery

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Source file missing | `create_backup()` returns `None` |
| Backup dir missing | Auto-created on first backup |
| Backup file not found | `FileNotFoundError` raised |
| Invalid YAML in backup | `ValueError` raised, current registry preserved |
| Invalid schema in backup | `ValueError` raised, current registry preserved |
| No backups available | `FileNotFoundError` raised by `restore_latest_backup()` |

## Testing

### Unit Tests (test_registry_backup_manager.py)
- Backup creation with correct timestamp naming
- Backup content matches original file
- Retention policy enforcement (keeps only last N)
- Chronological listing of backups
- Auto-creation of backup directory
- Multiple backups have unique names
- File extension preservation

### Integration Tests (test_registry_recovery_manager.py)
- Listing backups (empty, nonexistent dir, multiple files, .backup extension)
- Restoring from specific backup (valid, safety backup creation)
- Restoring latest backup (success, most recent selection, custom path)
- Validation after recovery (valid/invalid registry, duplicates, empty files)
- Health report generation after recovery
- Error handling (missing files, corrupt YAML, non-registry YAML)
- Current registry preservation on failure

### Running Tests

```bash
# Run backup manager unit tests
python -m pytest test_registry_backup_manager.py -v

# Run recovery integration tests
python -m pytest test_registry_recovery_manager.py -v

# Run all backup/recovery tests
python -m pytest test_registry_backup_manager.py test_registry_recovery_manager.py -v
```

## Requirements Satisfied

This implementation satisfies the following requirements:

- ✅ Create backup before every registry write operation (Req 9.6)
- ✅ Save backups to `.domainization/backups/` with timestamp
- ✅ Implement backup retention policy (keep last 10 backups)
- ✅ Create recovery command to restore from backup
- ✅ Implement registry validation after recovery
- ✅ Generate health report after recovery
- ✅ Automatic backup before every write (Req 15.11)

## Related Files

- `registry_backup_manager.py` — Backup creation and retention logic
- `registry_recovery_manager.py` — Recovery operations and validation
- `cli_recovery_commands.py` — CLI commands for recovery
- `cli_main.py` — Main CLI entry point (includes `recover` command)
- `artifact_registry.py` — Artifact registry (calls backup on save)
- `health_reporter.py` — Health report generation after recovery
- `test_registry_backup_manager.py` — Unit tests for backup
- `test_registry_recovery_manager.py` — Integration tests for recovery
