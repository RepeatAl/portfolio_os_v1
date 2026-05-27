# Integration End-to-End Tests

## Overview

Comprehensive integration tests that validate end-to-end flows across multiple domainization system components. These tests verify that the system works correctly as a whole, not just individual units.

## Features

- **Commit Gate Execution Flow**: Tests all 5 validation observers running in sequence
- **Registry Persistence and Loading**: Tests YAML save/load cycles for artifact, domain, and lifecycle registries
- **CLI Commands**: Tests all CLI subcommands (register, list, validate, health, config, recover)
- **Pre-Commit Hook Execution**: Tests hook script validity, observability mode, and graceful error handling
- **Backup and Recovery**: Tests automatic backup creation, retention policy, and full recovery flow
- **Health Report Integration**: Tests health report generation with real registry data

## Usage

### Running All Integration Tests

```bash
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py -v
```

### Running Specific Test Classes

```bash
# Commit gate flow tests
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py::TestCommitGateExecutionFlow -v

# Registry persistence tests
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py::TestRegistryPersistenceAndLoading -v

# CLI command tests
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py::TestCLICommands -v

# Pre-commit hook tests
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py::TestPreCommitHookExecution -v

# Backup and recovery tests
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py::TestBackupAndRecovery -v

# Health report integration tests
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py::TestHealthReportIntegration -v
```

## Testing

```bash
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end_flows.py -v
```

Expected output: 38 tests passing.

## Requirements Satisfied

- **15.1**: Commit gates execute in less than 5 seconds (performance target verified)
- **15.2**: Artifact registry supports at least 1000 artifacts (tested with 1000-artifact registry)
- **15.3**: Health reports generate in less than 10 seconds (timing verified)
- **15.5**: Same input always produces same validation result (determinism test)

## Related Files

- `.domainization/src/validation_orchestrator.py` - Orchestrates all 5 observers
- `.domainization/src/artifact_registry.py` - Artifact registry with YAML persistence
- `.domainization/src/cli_main.py` - CLI entry point
- `.domainization/hooks/pre-commit` - Optional pre-commit hook script
- `.domainization/src/registry_backup_manager.py` - Backup creation and retention
- `.domainization/src/registry_recovery_manager.py` - Recovery from backups
- `.domainization/src/health_reporter.py` - Health report generation
