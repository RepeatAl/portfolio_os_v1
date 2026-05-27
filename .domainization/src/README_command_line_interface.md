# Command-Line Interface Implementation

## Overview

This implementation provides a comprehensive command-line interface (CLI) for the domainization system. The CLI enables artifact management, validation, health reporting, and system configuration through a unified command-line tool.

## Architecture

### Core Components

1. **CLI Main** (`cli_main.py`)
   - Unified entry point for all commands
   - Argument parsing and routing
   - Error handling and exit codes

2. **Registry Commands** (`cli_registry_commands.py`)
   - `register` - Register new artifacts
   - `update` - Update artifact metadata
   - `list` - List artifacts with filters
   - `show` - Display artifact details

3. **Validation Commands** (`cli_validation_commands.py`)
   - `validate` - Run validation observers
   - Support for specific files and observers
   - Dry-run mode
   - Color-coded output

4. **Health Commands** (`cli_health_commands.py`)
   - `health` - Generate health reports
   - Domain filtering
   - File output support
   - Violations-only mode

5. **Configuration Commands** (`cli_config_commands.py`)
   - `config show` - Display configuration
   - `config set` - Modify configuration
   - Enforcement mode control
   - Observer management

## Installation

The CLI is located at `.domainization/domainization` and can be run directly:

```bash
./.domainization/domainization --help
```

For convenience, create an alias:

```bash
alias domainization='./.domainization/domainization'
```

## Command Reference

### Registry Management

#### Register Artifact

Register a new artifact in the domainization system:

```bash
domainization register <artifact_id> <file_path> <domain> <type> [options]
```

**Example:**

```bash
domainization register \
  signal_engine_allocation \
  engines/allocation_engine.py \
  SIGNALS \
  ENGINE \
  --description "Allocation signal generation engine" \
  --tags allocation signals
```

**Options:**
- `--lifecycle <status>` - Lifecycle status
- `--owner-role <role>` - Owner role description
- `--ssot-relationship <rel>` - SSOT relationship (canonical|derived|implementation|none)
- `--allowed-writers <domains>` - Write permission domains
- `--allowed-readers <domains>` - Read permission domains
- `--secondary-domains <domains>` - Secondary domains
- `--dependencies <artifact_ids>` - Dependencies
- `--topic <topic>` - Topic for SSOT conflict detection
- `--description <desc>` - Description
- `--tags <tags>` - Tags

#### Update Artifact

Update metadata for an existing artifact:

```bash
domainization update <artifact_id> [options]
```

**Example:**

```bash
domainization update signal_engine_allocation --lifecycle active
```

**Options:** Same as register command (all optional)

#### List Artifacts

List artifacts with optional filters:

```bash
domainization list [options]
```

**Examples:**

```bash
# List all artifacts
domainization list

# Filter by domain
domainization list --domain SIGNALS

# Filter by type
domainization list --type ENGINE

# Filter by lifecycle with details
domainization list --lifecycle active --verbose
```

**Options:**
- `--domain <domain>` - Filter by domain ID
- `--type <type>` - Filter by artifact type
- `--lifecycle <status>` - Filter by lifecycle status
- `--verbose, -v` - Show detailed information

#### Show Artifact

Display detailed information about a specific artifact:

```bash
domainization show <artifact_id>
```

**Example:**

```bash
domainization show signal_engine_allocation
```

### Validation

#### Run Validation

Run validation observers on the current repository state:

```bash
domainization validate [options]
```

**Examples:**

```bash
# Run all observers
domainization validate

# Validate specific files
domainization validate --files engines/new_engine.py docs/new_doc.md

# Run specific observer
domainization validate --observer RegistrationValidator

# Dry-run mode (always exits with 0)
domainization validate --dry-run

# Disable colors
domainization validate --no-color
```

**Options:**
- `--files <paths>` - Validate specific files only
- `--observer <name>` - Run specific observer only
  - `RegistrationValidator`
  - `DomainAssignmentValidator`
  - `LifecycleValidator`
  - `BoundaryAwarenessValidator`
  - `SSOTConsistencyValidator`
- `--dry-run` - Perform validation without affecting exit code
- `--no-color` - Disable colored output

### Health Reporting

#### Generate Health Report

Generate a comprehensive health report:

```bash
domainization health [options]
```

**Examples:**

```bash
# Generate full health report
domainization health

# Filter by domain
domainization health --domain SIGNALS

# Save to file
domainization health --output reports/health_report.yaml

# Show only violations
domainization health --violations-only

# Save without stdout
domainization health --output reports/health.yaml --quiet
```

**Options:**
- `--domain <domain>` - Filter by domain ID
- `--output, -o <path>` - Save report to file (YAML format)
- `--violations-only` - Show only violations section
- `--no-violations` - Exclude violations from report
- `--quiet, -q` - Suppress stdout output when saving to file

### Configuration

#### Show Configuration

Display current domainization configuration:

```bash
domainization config show
```

**Output:**

```
================================================================================
DOMAINIZATION CONFIGURATION
================================================================================

Configuration File: /path/to/.domainization/config.yaml

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

#### Set Configuration

Modify domainization configuration:

```bash
domainization config set [options]
```

**Examples:**

```bash
# Set enforcement mode
domainization config set --enforcement-mode soft

# Enable/disable observers
domainization config set --enable-observer RegistrationValidator
domainization config set --disable-observer LifecycleValidator

# Set performance timeouts
domainization config set --validation-timeout 3000

# Set logging
domainization config set --log-level DEBUG --audit-enabled true

# Set multiple options
domainization config set \
  --enforcement-mode observability \
  --enable-observer RegistrationValidator \
  --validation-timeout 5000 \
  --log-level INFO
```

**Options:**
- `--enforcement-mode <mode>` - Set enforcement mode (observability|soft|hard)
- `--enable-observer <observers>` - Enable specific observers
- `--disable-observer <observers>` - Disable specific observers
- `--validation-timeout <ms>` - Validation timeout in milliseconds
- `--health-report-timeout <ms>` - Health report timeout in milliseconds
- `--log-level <level>` - Set logging level (DEBUG|INFO|WARNING|ERROR)
- `--audit-enabled <bool>` - Enable/disable audit logging (true/false)

## Exit Codes

- `0` - Success
- `1` - Error or validation warnings found
- `130` - Interrupted by user (Ctrl+C)

## Enforcement Modes

### Observability Mode (Default)

- All validation observers generate warnings only
- Commits are never blocked
- Violations are logged for visibility
- Ideal for FAST LANE development phase

### Soft Mode

- Critical and high severity violations generate warnings
- Medium and low severity violations are informational
- Commits proceed with warnings

### Hard Mode

- Critical and high severity violations block commits
- Medium and low severity violations generate warnings
- Strict enforcement of governance rules

## Common Workflows

### Registering a New Engine

```bash
# 1. Register the engine
domainization register \
  my_new_engine \
  engines/my_engine.py \
  SIGNALS \
  ENGINE \
  --description "My new signal engine"

# 2. Verify registration
domainization show my_new_engine

# 3. Run validation
domainization validate --files engines/my_engine.py
```

### Updating Artifact Lifecycle

```bash
# Move from development to active
domainization update my_engine --lifecycle active

# Verify update
domainization show my_engine
```

### Checking System Health

```bash
# Generate full health report
domainization health

# Check specific domain
domainization health --domain SIGNALS

# Check for violations only
domainization health --violations-only
```

### Configuring for Different Phases

```bash
# FAST LANE phase (observability only)
domainization config set --enforcement-mode observability

# Post-MVP phase (soft enforcement)
domainization config set --enforcement-mode soft

# Production phase (hard enforcement)
domainization config set --enforcement-mode hard
```

## Color-Coded Output

The CLI uses color-coded output for better readability:

- 🔴 **Critical** - Red (critical severity)
- 🟠 **High** - Orange (high severity)
- 🟡 **Medium** - Yellow (medium severity)
- 🟢 **Low** - Green (low severity)
- ✓ **Success** - Green checkmark
- ✗ **Error** - Red cross

Colors can be disabled with `--no-color` flag or automatically when output is not a TTY.

## Testing

Comprehensive test suite with 49 tests covering all functionality:

```bash
# Run all CLI tests
python -m pytest .domainization/src/test_cli_*.py -v

# Run specific test file
python -m pytest .domainization/src/test_cli_registry_commands.py -v

# Run integration tests
python -m pytest .domainization/src/test_cli_integration.py -v
```

**Test Files:**
- `test_cli_registry_commands.py` - Registry command tests (15 tests)
- `test_cli_validation_commands.py` - Validation command tests (9 tests)
- `test_cli_health_commands.py` - Health command tests (7 tests)
- `test_cli_config_commands.py` - Configuration command tests (12 tests)
- `test_cli_integration.py` - End-to-end integration tests (6 tests)

## File Structure

```
.domainization/
├── domainization                      # Bash wrapper script
└── src/
    ├── cli_main.py                    # Main CLI entry point
    ├── cli_registry_commands.py       # Registry management commands
    ├── cli_validation_commands.py     # Validation commands
    ├── cli_health_commands.py         # Health reporting commands
    ├── cli_config_commands.py         # Configuration commands
    ├── test_cli_registry_commands.py  # Registry command tests
    ├── test_cli_validation_commands.py # Validation command tests
    ├── test_cli_health_commands.py    # Health command tests
    ├── test_cli_config_commands.py    # Configuration command tests
    ├── test_cli_integration.py        # Integration tests
    └── README_command_line_interface.md # This file
```

## Implementation Details

### RegistryCommands Class

Provides registry management functionality:

```python
class RegistryCommands:
    def register(self, args: argparse.Namespace) -> int
    def update(self, args: argparse.Namespace) -> int
    def list_artifacts(self, args: argparse.Namespace) -> int
    def show(self, args: argparse.Namespace) -> int
```

**Features:**
- Validates domain and artifact type combinations
- Checks lifecycle transitions
- Creates backups before saving
- Provides detailed error messages

### ValidationCommands Class

Provides validation functionality:

```python
class ValidationCommands:
    def validate(self, args: argparse.Namespace) -> int
    def _display_observer_result(self, result)
    def _display_observability_report(self, report)
    def _display_warning(self, warning)
```

**Features:**
- Runs all or specific observers
- Color-coded severity indicators
- Dry-run mode for safe testing
- Performance tracking

### HealthCommands Class

Provides health reporting functionality:

```python
class HealthCommands:
    def health(self, args: argparse.Namespace) -> int
    def _filter_by_domain(self, report: dict, domain_id: str) -> dict
```

**Features:**
- Comprehensive health reports
- Domain filtering
- YAML file output
- Violations-only mode
- Quiet mode for automation

### ConfigCommands Class

Provides configuration management:

```python
class ConfigCommands:
    def show(self, args: argparse.Namespace) -> int
    def set_config(self, args: argparse.Namespace) -> int
    def _load_config(self) -> dict
    def _save_config(self, config: dict) -> None
```

**Features:**
- Display current configuration
- Modify enforcement mode
- Enable/disable observers
- Set performance timeouts
- Configure logging

## Performance

### Targets

- Registry operations: < 1 second
- Validation: < 5 seconds for 1000 artifacts
- Health report: < 10 seconds for 1000 artifacts
- Configuration: < 100ms

### Optimization

The CLI is optimized for performance:

1. **Lazy Loading** - Registries loaded only when needed
2. **Efficient Queries** - Uses optimized registry methods
3. **Minimal I/O** - Reduces file system operations
4. **Caching** - Reuses loaded registries

## Error Handling

The CLI provides clear error messages:

```bash
# Invalid domain
$ domainization register test test.py INVALID ENGINE
Error: Invalid domain 'INVALID'
Valid domains: SIGNALS, SEMANTICS, REASONING, REPORT, GOV, ARCH, STATE, DATA, USER, DEPLOY, MEMORY, SIM

# Invalid lifecycle transition
$ domainization update test --lifecycle planned
Error: Invalid transition from 'active' to 'planned'. Valid transitions: deprecated

# Artifact not found
$ domainization show nonexistent
Error: Artifact 'nonexistent' not found
```

## Tips

1. **Use `--help` for any command** to see detailed usage:
   ```bash
   domainization register --help
   ```

2. **Use `--verbose` with list** to see full artifact details:
   ```bash
   domainization list --verbose
   ```

3. **Use `--dry-run` for validation** to check without affecting exit codes:
   ```bash
   domainization validate --dry-run
   ```

4. **Save health reports** for tracking over time:
   ```bash
   domainization health --output reports/health_$(date +%Y%m%d).yaml
   ```

5. **Filter validation** to specific observers for faster checks:
   ```bash
   domainization validate --observer RegistrationValidator
   ```

## Troubleshooting

### Command Not Found

If you get "command not found", ensure the script is executable:

```bash
chmod +x .domainization/domainization
```

### Module Import Errors

Ensure you're running from the repository root and have the correct Python environment activated.

### Validation Failures

Use `--dry-run` to see warnings without blocking:

```bash
domainization validate --dry-run
```

Then address warnings one at a time.

### Configuration Issues

Reset to defaults by deleting the config file:

```bash
rm .domainization/config.yaml
domainization config show  # Will show defaults
```

## Integration with Other Tools

### Git Hooks

The CLI can be integrated with git hooks:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run validation on staged files
STAGED_FILES=$(git diff --cached --name-only)
if [ -n "$STAGED_FILES" ]; then
    ./.domainization/domainization validate --files $STAGED_FILES
fi
```

### CI/CD Pipelines

Use in CI/CD for automated validation:

```yaml
# .github/workflows/validate.yml
- name: Run Domainization Validation
  run: |
    ./.domainization/domainization validate
    ./.domainization/domainization health --output reports/health.yaml
```

### Automation Scripts

Integrate with automation scripts:

```bash
#!/bin/bash
# Daily health check

REPORT_FILE="reports/health_$(date +%Y%m%d).yaml"
./.domainization/domainization health --output "$REPORT_FILE" --quiet

# Check for critical violations
if grep -q "critical:" "$REPORT_FILE"; then
    echo "Critical violations detected!"
    exit 1
fi
```

## Requirements Satisfied

This implementation satisfies the following requirements:

- **1.1** - CLI for artifact registration
- **1.2** - Register artifacts with metadata
- **1.3** - Update artifact metadata
- **1.6** - Query artifacts by domain, type, lifecycle
- **5.1** - Run validation observers
- **5.7** - Display validation results
- **5.8** - Support dry-run mode
- **10.1** - Generate health reports
- **10.2** - Domain coverage reporting
- **10.3** - Lifecycle distribution reporting
- **10.4** - Violations reporting
- **10.5** - Actionable recommendations
- **10.6** - Report metadata (timestamp, version)
- **10.7** - Healthy system indicators

## See Also

- [CLI Usage Guide](README_cli_usage.md) - Detailed usage examples
- [Registry Layer Documentation](README_registry_layer_python_api.md)
- [Validation Observers Documentation](README_validation_observers.md)
- [Reporting Layer Documentation](README_reporting_layer.md)
- [Design Document](../../.kiro/specs/domainization/design.md)
- [Requirements Document](../../.kiro/specs/domainization/requirements.md)

## Author

Implemented as part of the domainization system for Portfolio OS.

## License

Internal use only.
