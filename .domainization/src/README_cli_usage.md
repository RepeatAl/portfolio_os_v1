# Domainization CLI Usage Guide

## Overview

The domainization CLI provides a unified command-line interface for managing artifacts, running validation, generating health reports, and configuring the domainization system.

## Installation

The CLI is located at `.domainization/domainization` and can be run directly:

```bash
./.domainization/domainization --help
```

For convenience, you can add it to your PATH or create an alias:

```bash
alias domainization='./.domainization/domainization'
```

## Commands

### Registry Management

#### Register a New Artifact

Register a new artifact in the domainization system:

```bash
domainization register <artifact_id> <file_path> <domain> <type> [options]
```

**Required Arguments:**
- `artifact_id`: Unique identifier for the artifact
- `file_path`: Path to the artifact file (relative to repo root)
- `domain`: Primary domain ID (e.g., SIGNALS, REPORT, ARCH)
- `type`: Artifact type (e.g., ENGINE, SSOT, DATA_OUT)

**Optional Arguments:**
- `--lifecycle <status>`: Lifecycle status (uses initial state if not provided)
- `--owner-role <role>`: Owner role description
- `--ssot-relationship <rel>`: SSOT relationship (canonical|derived|implementation|none)
- `--allowed-writers <domains>`: List of domain IDs with write permission
- `--allowed-readers <domains>`: List of domain IDs with read permission
- `--secondary-domains <domains>`: Secondary domain IDs
- `--dependencies <artifact_ids>`: Artifact IDs this depends on
- `--topic <topic>`: Topic for SSOT conflict detection
- `--description <desc>`: Artifact description
- `--tags <tags>`: Tags for categorization

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

#### Update Artifact Metadata

Update metadata for an existing artifact:

```bash
domainization update <artifact_id> [options]
```

**Optional Arguments:**
- `--domain <domain>`: New primary domain ID
- `--lifecycle <status>`: New lifecycle status
- `--file-path <path>`: New file path
- `--owner-role <role>`: New owner role
- `--ssot-relationship <rel>`: New SSOT relationship
- `--allowed-writers <domains>`: New allowed writers
- `--allowed-readers <domains>`: New allowed readers
- `--secondary-domains <domains>`: New secondary domains
- `--dependencies <artifact_ids>`: New dependencies
- `--topic <topic>`: New topic
- `--description <desc>`: New description
- `--tags <tags>`: New tags

**Example:**

```bash
domainization update signal_engine_allocation --lifecycle active
```

#### List Artifacts

List artifacts with optional filters:

```bash
domainization list [options]
```

**Optional Arguments:**
- `--domain <domain>`: Filter by domain ID
- `--type <type>`: Filter by artifact type
- `--lifecycle <status>`: Filter by lifecycle status
- `--verbose, -v`: Show detailed information

**Examples:**

```bash
# List all artifacts
domainization list

# List artifacts in SIGNALS domain
domainization list --domain SIGNALS

# List all ENGINE artifacts
domainization list --type ENGINE

# List active artifacts with details
domainization list --lifecycle active --verbose
```

#### Show Artifact Details

Display detailed information about a specific artifact:

```bash
domainization show <artifact_id>
```

**Example:**

```bash
domainization show signal_engine_allocation
```

### Validation

#### Run Validation Observers

Run validation observers on the current repository state:

```bash
domainization validate [options]
```

**Optional Arguments:**
- `--files <paths>`: Validate specific files only
- `--observer <name>`: Run specific observer only
  - `RegistrationValidator`
  - `DomainAssignmentValidator`
  - `LifecycleValidator`
  - `BoundaryAwarenessValidator`
  - `SSOTConsistencyValidator`
- `--dry-run`: Perform validation without affecting exit code
- `--no-color`: Disable colored output

**Examples:**

```bash
# Run all validation observers
domainization validate

# Validate specific files
domainization validate --files engines/new_engine.py docs/new_doc.md

# Run specific observer
domainization validate --observer RegistrationValidator

# Dry-run mode (always exits with 0)
domainization validate --dry-run
```

### Health Reporting

#### Generate Health Report

Generate a comprehensive health report:

```bash
domainization health [options]
```

**Optional Arguments:**
- `--domain <domain>`: Filter by domain ID
- `--output, -o <path>`: Save report to file (YAML format)
- `--violations-only`: Show only violations section
- `--no-violations`: Exclude violations from report
- `--quiet, -q`: Suppress stdout output when saving to file

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

# Save to file without stdout
domainization health --output reports/health.yaml --quiet
```

### Configuration

#### Show Configuration

Display current domainization configuration:

```bash
domainization config show
```

#### Set Configuration

Modify domainization configuration:

```bash
domainization config set [options]
```

**Optional Arguments:**
- `--enforcement-mode <mode>`: Set enforcement mode (observability|soft|hard)
- `--enable-observer <observers>`: Enable specific observers
- `--disable-observer <observers>`: Disable specific observers
- `--validation-timeout <ms>`: Validation timeout in milliseconds
- `--health-report-timeout <ms>`: Health report timeout in milliseconds
- `--log-level <level>`: Set logging level (DEBUG|INFO|WARNING|ERROR)
- `--audit-enabled <bool>`: Enable/disable audit logging (true/false)

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

## Exit Codes

- `0`: Success
- `1`: Error or validation warnings found
- `130`: Interrupted by user (Ctrl+C)

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

## See Also

- [Registry Layer Python API](README_registry_layer_python_api.md)
- [Validation Observers](README_validation_observers.md)
- [Reporting Layer](README_reporting_layer.md)
- [Registry Cache](README_registry_cache.md)
