# Observability Mode Configuration

## Overview

The domainization system operates in **observability mode** during the FAST LANE REPORT MVP phase. This means all validation observers generate warnings only — commits are never blocked, report development is never interrupted, and governance provides visibility without friction.

The configuration file at `.domainization/config.yaml` controls the enforcement mode, observer settings, performance targets, and phase-specific rules.

## Features

### Enforcement Modes

The system supports three enforcement modes:

| Mode | Behavior | Phase |
|------|----------|-------|
| `observability` | Warnings only, no blocking | FAST LANE (current) |
| `soft` | Warnings with strict audit trail | Post-MVP transition |
| `hard` | Blocking, violations prevent commits | Full enforcement |

### Observer Control

Each of the 5 validation observers can be individually enabled or disabled:

- **RegistrationValidator** — Detects unregistered artifacts and missing metadata
- **DomainAssignmentValidator** — Detects invalid domain assignments
- **LifecycleValidator** — Detects invalid lifecycle transitions
- **BoundaryAwarenessValidator** — Detects authority chain violations, cloud provider issues, runtime flow violations
- **SSOTConsistencyValidator** — Detects SSOT conflicts and missing references

### FAST LANE Phase Rules

During the FAST LANE phase, the configuration enforces:

- Commit gates are deferred (no blocking behavior)
- Governance does not block report development
- Registry enforcement remains soft-validation only
- All violation types generate warnings, not errors

### Performance Targets

- Validation timeout: 5000ms (< 5 seconds per Requirement 15.1)
- Health report timeout: 10000ms (< 10 seconds per Requirement 15.3)

## Usage

### View Current Configuration

```bash
.venv/bin/python .domainization/src/cli_main.py config show
```

Output:
```
================================================================================
DOMAINIZATION CONFIGURATION
================================================================================

Configuration File: .domainization/config.yaml

Enforcement Mode:
  observability

Observer Status:
  RegistrationValidator: ✓ Enabled
  DomainAssignmentValidator: ✓ Enabled
  LifecycleValidator: ✓ Enabled
  BoundaryAwarenessValidator: ✓ Enabled
  SSOTConsistencyValidator: ✓ Enabled

Performance Settings:
  Validation Timeout: 5000ms
  Health Report Timeout: 10000ms

Logging Settings:
  Level: INFO
  Audit Enabled: True

================================================================================
```

### Change Enforcement Mode

```bash
# Set to soft mode (post-MVP transition)
.venv/bin/python .domainization/src/cli_main.py config set --enforcement-mode soft

# Set to hard mode (full enforcement - only after MVP stabilizes)
.venv/bin/python .domainization/src/cli_main.py config set --enforcement-mode hard

# Return to observability mode
.venv/bin/python .domainization/src/cli_main.py config set --enforcement-mode observability
```

### Enable/Disable Observers

```bash
# Disable a specific observer
.venv/bin/python .domainization/src/cli_main.py config set --disable-observer LifecycleValidator

# Enable a specific observer
.venv/bin/python .domainization/src/cli_main.py config set --enable-observer LifecycleValidator

# Disable multiple observers
.venv/bin/python .domainization/src/cli_main.py config set --disable-observer LifecycleValidator BoundaryAwarenessValidator
```

### Adjust Performance Settings

```bash
# Set validation timeout to 3 seconds
.venv/bin/python .domainization/src/cli_main.py config set --validation-timeout 3000

# Set health report timeout to 15 seconds
.venv/bin/python .domainization/src/cli_main.py config set --health-report-timeout 15000
```

### Configure Logging

```bash
# Set log level to DEBUG for troubleshooting
.venv/bin/python .domainization/src/cli_main.py config set --log-level DEBUG

# Disable audit logging
.venv/bin/python .domainization/src/cli_main.py config set --audit-enabled false
```

### Programmatic Access

```python
from pathlib import Path
import yaml

# Load configuration
config_path = Path('.domainization/config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Check enforcement mode
if config['enforcement_mode'] == 'observability':
    print("System is in observability mode - warnings only")

# Check if an observer is enabled
if config['observers']['RegistrationValidator']['enabled']:
    print("Registration observer is active")

# Check FAST LANE rules
if config['fast_lane_rules']['commit_gates_deferred']:
    print("Commit gates are deferred during FAST LANE")
```

## Testing

### Run Configuration CLI Tests

```bash
.venv/bin/python -m pytest .domainization/src/test_cli_config_commands.py -v
```

### Verify Config File Loads Correctly

```bash
.venv/bin/python -c "
import yaml
from pathlib import Path

config_path = Path('.domainization/config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

assert config['enforcement_mode'] == 'observability'
assert config['current_phase'] == 'fast_lane_report_mvp'
assert config['fast_lane_rules']['commit_gates_deferred'] is True
assert config['fast_lane_rules']['report_development_unblocked'] is True
assert config['fast_lane_rules']['registry_soft_validation_only'] is True
print('✓ Configuration file is valid and correctly configured for FAST LANE phase')
"
```

### Verify CLI Integration

```bash
# Show config (should display observability mode)
.venv/bin/python .domainization/src/cli_main.py config show

# Set and verify enforcement mode
.venv/bin/python .domainization/src/cli_main.py config set --enforcement-mode soft
.venv/bin/python .domainization/src/cli_main.py config show
.venv/bin/python .domainization/src/cli_main.py config set --enforcement-mode observability
```

## Requirements Satisfied

| Requirement | Description | How Satisfied |
|-------------|-------------|---------------|
| 5.9 | Commit gates deferred until MVP stabilizes | `enforcement_mode: observability` ensures no blocking; `fast_lane_rules.commit_gates_deferred: true` documents the deferral |
| 5.10 | Governance shall not block report development | `fast_lane_rules.report_development_unblocked: true`; observability mode never blocks |
| 9.8 | Registry enforcement remains soft-validation only | `fast_lane_rules.registry_soft_validation_only: true`; all observers generate warnings only |

## Related Files

- `.domainization/config.yaml` — Main configuration file
- `.domainization/src/cli_config_commands.py` — CLI commands for config management
- `.domainization/src/test_cli_config_commands.py` — Tests for config CLI commands
- `.domainization/src/validation_orchestrator.py` — Orchestrator that respects enforcement mode
- `.domainization/src/README_validation_observers.md` — Documentation for validation observers
