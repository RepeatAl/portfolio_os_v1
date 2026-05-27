# Runtime and Configuration Artifact Registration

## Overview

This document describes the runtime and configuration artifact registration process implemented in Task 12. Runtime entry points (`main.py`, `app.py`) have been registered in the artifact registry with complete metadata, enabling proper artifact tracking and governance within the domainization system.

## Purpose

The registration of runtime artifacts serves multiple purposes:

1. **Domain Ownership** - Establishes clear ownership boundaries for runtime entry points
2. **Artifact Tracking** - Enables the domainization system to track and validate runtime artifacts
3. **Dependency Management** - Documents dependencies between runtime entry points and engines
4. **Lifecycle Management** - Tracks the lifecycle status of each runtime artifact
5. **Access Control** - Defines which domains can write to and read from each runtime artifact
6. **Implementation Traceability** - Links runtime artifacts to their architectural specifications

## Registry Schema

Each registered runtime artifact contains metadata in the artifact registry with the following fields:

```yaml
- artifact_id: <unique_identifier>
  file_path: <relative_path>
  primary_domain: <DOMAIN_ID>
  artifact_type: <RUNTIME|DASHBOARD>
  lifecycle_status: <STATUS>
  created_date: <YYYY-MM-DD>
  last_modified: <YYYY-MM-DD>
  owner_role: <description>
  ssot_relationship: implementation
  allowed_writers: [<DOMAIN_ID>, ...]
  allowed_readers: [ALL]
  dependencies: [<artifact_id>, ...]
  description: <human_readable_description>
  tags: [<tag1>, <tag2>, ...]
```

### Field Descriptions

- **artifact_id**: Unique identifier derived from filename (e.g., `main_py`)
- **file_path**: Relative path from repo root (e.g., `main.py`)
- **primary_domain**: Primary owning domain (DEPLOY for runtime, USER for dashboard)
- **artifact_type**: `RUNTIME` for execution entry points, `DASHBOARD` for user-facing applications
- **lifecycle_status**: Current lifecycle state (active for production-ready artifacts)
- **created_date**: Original creation date
- **last_modified**: Last modification date
- **owner_role**: Description of the artifact's responsibility
- **ssot_relationship**: `implementation` (runtime artifacts implement architectural specifications)
- **allowed_writers**: List of domains permitted to modify the artifact
- **allowed_readers**: List of domains permitted to read the artifact (typically `[ALL]`)
- **dependencies**: List of artifact IDs this runtime artifact depends on
- **description**: Human-readable description of artifact functionality
- **tags**: Categorization tags for filtering and organization

## Registered Runtime Artifacts

### Deploy Domain (DEPLOY)

Runtime entry points for system execution:

- **main.py** - Main runtime entry point for Portfolio OS engine execution pipeline
  - Artifact ID: `main_py`
  - Artifact Type: RUNTIME
  - Lifecycle Status: active
  - Dependencies: `engine_runner_py`, `engine_registry_py`
  - Allowed Writers: DEPLOY, ARCH
  - Tags: runtime, deploy, entry_point

### User Domain (USER)

Dashboard and user-facing applications:

- **app.py** - Streamlit dashboard application for portfolio visualization and interaction
  - Artifact ID: `app_py`
  - Artifact Type: DASHBOARD
  - Lifecycle Status: active
  - Dependencies: `dashboard_philosophy_md`
  - Allowed Writers: USER, ARCH
  - Tags: dashboard, user, streamlit

## Registration Details

### Task 12.1 - Register Runtime Entry Points

Registered runtime entry points with appropriate domain ownership:

| Artifact | Domain | Type | Status | Dependencies |
|----------|--------|------|--------|--------------|
| main.py | DEPLOY | RUNTIME | active | engine_runner_py, engine_registry_py |
| app.py | USER | DASHBOARD | active | dashboard_philosophy_md |

### Validation

After registration, all runtime artifacts were validated to ensure:

1. **Schema Compliance** - All required metadata fields are present
2. **Domain Validity** - DEPLOY and USER are valid domain IDs
3. **Artifact Type** - RUNTIME and DASHBOARD are valid artifact types
4. **Lifecycle Validity** - "active" is valid for both RUNTIME and DASHBOARD types
5. **Dependency Validity** - Referenced dependencies exist in the registry
6. **Implementation Relationship** - ssot_relationship is set to "implementation"

## Lifecycle States

### RUNTIME Artifacts

Valid lifecycle states for RUNTIME artifacts:

- **planned**: Runtime entry point is planned but not yet implemented
- **development**: Runtime entry point is under active development
- **active**: Runtime entry point is production-ready and actively used
- **deprecated**: Runtime entry point is no longer recommended

### DASHBOARD Artifacts

Valid lifecycle states for DASHBOARD artifacts:

- **planned**: Dashboard is planned but not yet implemented
- **development**: Dashboard is under active development
- **active**: Dashboard is production-ready and actively used
- **deprecated**: Dashboard is no longer recommended

### Lifecycle Transitions

```
planned → development → active → deprecated
         ↓            ↑
         └────────────┘
         (iteration allowed)
```

## Domain Boundaries and Access Control

### DEPLOY Domain

- **Responsibility**: Manages deployment infrastructure and runtime execution
- **Owns**: RUNTIME artifacts (execution entry points, deployment scripts)
- **Cannot Own**: SSOT, ENGINE, REPORT_OUT, SEMANTIC_STATE, REASONING_OBJECT

### USER Domain

- **Responsibility**: Manages user-facing interfaces and dashboards
- **Owns**: DASHBOARD artifacts (Streamlit apps, visualization interfaces)
- **Cannot Own**: SSOT, ENGINE, SIGNAL, SEMANTIC_STATE, REASONING_OBJECT

### Access Control

Both runtime artifacts allow writes from their primary domain plus ARCH (for architectural changes):

```yaml
# main.py
allowed_writers: [DEPLOY, ARCH]
allowed_readers: [ALL]

# app.py
allowed_writers: [USER, ARCH]
allowed_readers: [ALL]
```

## Usage

### Querying Runtime Artifacts

```bash
# List all runtime artifacts
domainization list --type RUNTIME

# List all dashboard artifacts
domainization list --type DASHBOARD

# List by domain
domainization list --domain DEPLOY
domainization list --domain USER

# Show details
domainization show main_py
domainization show app_py
```

### Updating Runtime Artifacts

```bash
# Update lifecycle status
domainization update main_py --lifecycle active

# Update last modified date
domainization update app_py --last-modified 2026-05-26

# Add dependencies
domainization update main_py --dependencies engine_runner_py engine_registry_py
```

### Validating Runtime Artifacts

```bash
# Validate all runtime artifacts
domainization validate --type RUNTIME

# Validate specific artifact
domainization validate --files main.py

# Validate dashboard artifacts
domainization validate --type DASHBOARD
```

## Dependencies

### main.py Dependencies

```
main.py (DEPLOY/RUNTIME)
├── engine_runner.py (ARCH/ENGINE) - Orchestrates engine execution
└── engine_registry.py (ARCH/ENGINE) - Defines engine dependencies and order
```

### app.py Dependencies

```
app.py (USER/DASHBOARD)
└── dashboard_philosophy.md (USER/SSOT) - Dashboard design principles
```

## Integration with Domainization System

### Registry Integration

All registered runtime artifacts are tracked in the artifact registry:

- **Location**: `.domainization/artifact_registry.yaml`
- **Format**: YAML with full metadata
- **Validation**: Automatic validation on registration and updates

### Validation Observers

Multiple observers validate registered runtime artifacts:

1. **RegistrationValidator**: Ensures runtime artifacts are registered
2. **DomainAssignmentValidator**: Validates DEPLOY/USER domain ownership
3. **LifecycleValidator**: Validates lifecycle transitions
4. **BoundaryAwarenessValidator**: Checks domain boundaries
5. **SSOTConsistencyValidator**: Validates dependency references

## Requirements Satisfied

This implementation satisfies the following requirements:

- **1.2** - Register artifacts with metadata (runtime entry points)
- **1.5** - Artifact metadata includes domain, type, lifecycle, dependencies
- **2.3** - Domain assignment validation (DEPLOY, USER domains)
- **9.1** - Artifact registration with proper domain ownership
- **9.2** - Semantic relationship tracking (implementation)
- **9.3** - Dependency documentation

## File Structure

```
./
├── main.py                        # DEPLOY domain (RUNTIME)
├── app.py                         # USER domain (DASHBOARD)
│
.domainization/
├── artifact_registry.yaml         # Registry with all metadata
└── src/
    └── README_runtime_artifact_registration.md  # This file
```

## See Also

- [Engine Registration](README_engine_registration.md) - Engine registration guide
- [SSOT Document Registration](README_ssot_document_registration.md) - SSOT registration guide
- [Data Artifact Registration](README_data_artifact_registration.md) - Data artifact registration
- [Report Output Registration](README_report_output_registration.md) - Report output registration
- [Registry Layer Python API](README_registry_layer_python_api.md) - Registry API
- [Command-Line Interface](README_command_line_interface.md) - CLI documentation

## Summary

Task 12 successfully registered all runtime entry points with complete metadata in the artifact registry. This enables:

- **Clear Domain Ownership** - main.py owned by DEPLOY, app.py owned by USER
- **Artifact Tracking** - Both runtime artifacts are tracked in the registry
- **Dependency Management** - Dependencies on engines and SSOT specifications are explicit
- **Lifecycle Management** - Runtime artifact lifecycle is tracked and validated
- **Access Control** - Read/write permissions are defined (primary domain + ARCH)
- **Implementation Traceability** - Runtime artifacts linked to architectural specifications
- **Validation** - Automated validation ensures compliance

Total runtime artifacts registered: 2 (across 2 domains)

## Author

Implemented as part of Task 12 of the domainization system for Portfolio OS.

## License

Internal use only.
