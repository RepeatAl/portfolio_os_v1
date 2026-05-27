# Domainization System - Foundation Infrastructure

This directory contains the foundation infrastructure for the Portfolio OS domainization system, which provides artifact governance through domain boundaries, lifecycle tracking, and validation.

## Directory Structure

```
.domainization/
├── backups/              # Automatic registry backups (created on write)
├── hooks/                # Optional pre-commit hooks for validation
├── logs/                 # Audit logs and validation history
├── reports/              # Health reports and violation summaries
├── src/                  # Python modules and tests
│   ├── artifact_schema.py
│   ├── test_artifact_registry.py
│   ├── test_domain_registry.py
│   └── test_lifecycle_state_machine.py
├── artifact_registry.yaml       # Central artifact index
├── domain_registry.yaml         # 12 canonical domain definitions
├── lifecycle_state_machine.yaml # State machines for 11 artifact types
└── README.md                    # This file
```

## Core Components

### 1. Domain Registry (`domain_registry.yaml`)

Defines 12 canonical domains with authority boundaries:

**Core Reasoning Chain** (priority: core):
- SIGNALS (authority_level: 1) - Raw signal calculation
- SEMANTICS (authority_level: 2) - Semantic interpretation
- REASONING (authority_level: 3) - Decision logic
- REPORT (authority_level: 4) - Human-readable text

**Surface Domains** (priority: surface):
- GOV - Governance frameworks
- ARCH - System architecture
- STATE - Portfolio state
- DATA - Data management
- USER - User interface
- DEPLOY - Deployment
- MEMORY - Historical snapshots
- SIM - Simulation

Each domain specifies:
- `allowed_artifact_types` - What it can own
- `cannot_own` - Explicit exclusions
- `responsibility_scope` - What it's responsible for

### 2. Lifecycle State Machines (`lifecycle_state_machine.yaml`)

Defines valid states and transitions for 11 artifact types:

- **SSOT**: draft → review → canonical → deprecated
- **ENGINE**: planned → development → active → deprecated
- **REPORT_OUT**: generated → current → archived
- **DATA_IN**: active → stale → archived
- **DATA_OUT**: generated → current → archived
- **RUNTIME**: development → active → deprecated
- **DASHBOARD**: development → active → deprecated
- **SNAPSHOT**: captured → archived
- **CONFIG**: draft → active → deprecated
- **CALIBRATION**: draft → active → superseded
- **STEERING**: draft → active → deprecated

Each state machine defines:
- Valid states
- Initial state for new artifacts
- Allowed transitions with conditions
- Modifiable vs read-only states

### 3. Artifact Registry (`artifact_registry.yaml`)

Central index of all artifacts with metadata. Contains:

**Required Fields**:
- `artifact_id` - Unique identifier
- `file_path` - Relative path from repo root
- `primary_domain` - Domain ID
- `artifact_type` - Type ID
- `lifecycle_status` - Current state
- `created_date` - YYYY-MM-DD format
- `last_modified` - YYYY-MM-DD format
- `owner_role` - Responsibility description
- `ssot_relationship` - canonical|derived|implementation|none
- `allowed_writers` - Domain IDs with write permission
- `allowed_readers` - Domain IDs with read permission (or "ALL")

**Optional Fields**:
- `secondary_domains` - Additional domain associations
- `dependencies` - Artifact IDs this depends on
- `topic` - For SSOT conflict detection
- `description` - Human-readable description
- `tags` - Categorization tags

**Note**: Markdown files should use YAML frontmatter instead of registry entries.

### 4. Schema Validation (`src/artifact_schema.py`)

Python module providing:
- `ArtifactMetadata` dataclass with validation
- `validate_artifact_dict()` function for schema checking
- Methods for permission checking (`can_write`, `can_read`)
- Lifecycle state checking (`is_modifiable`)

## Testing

All components have comprehensive unit tests:

```bash
# Run all tests
python -m pytest .domainization/src/ -v

# Run specific test file
python -m pytest .domainization/src/test_domain_registry.py -v
python -m pytest .domainization/src/test_lifecycle_state_machine.py -v
python -m pytest .domainization/src/test_artifact_registry.py -v
```

**Test Coverage**:
- 77 total tests
- Domain registry: 17 tests
- Lifecycle state machines: 34 tests
- Artifact registry & schema: 26 tests

## Governance Mode

**Current Phase**: FOUNDATION + OBSERVABILITY

The system is configured for the FAST LANE REPORT MVP phase:

- ✅ Artifact indexing and registry
- ✅ Lifecycle tracking and visibility
- ✅ Dependency mapping
- ✅ SSOT visibility
- ✅ Health reporting
- ⏸️ Hard commit blocking (deferred)
- ⏸️ Mandatory metadata enforcement (deferred)

All validation operates in **OBSERVABILITY MODE**:
- Generate warnings, not errors
- Report violations, don't block commits
- Build visibility, not enforcement
- Help reasoning, not punish contributors

## Next Steps

The foundation infrastructure is complete. Next tasks:

1. **Task 2**: Implement registry layer Python modules
2. **Task 3**: Implement validation observers (warnings only)
3. **Task 4**: Implement reporting layer
4. **Task 8-12**: Register existing artifacts
5. **Task 20**: Configure observability mode

## Requirements Satisfied

This implementation satisfies the following requirements:

- **Req 1.1**: Central artifact registry created
- **Req 1.2**: Metadata schema defined
- **Req 2.1-2.10**: 12 canonical domains with authority boundaries
- **Req 3.1-3.7**: 11 artifact types with lifecycle states
- **Req 4.1-4.7**: Lifecycle state management
- **Req 8.1-8.7**: Metadata schema validation

## Documentation

For detailed information, see:
- Requirements: `.kiro/specs/domainization/requirements.md`
- Design: `.kiro/specs/domainization/design.md`
- Tasks: `.kiro/specs/domainization/tasks.md`
