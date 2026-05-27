# Architecture Documentation

## Overview

The domainization system provides artifact governance for Portfolio OS through a **5-layer architecture** that indexes, classifies, validates, and reports on all repository artifacts. The system operates in **observability mode** during the FAST LANE phase — generating warnings and visibility without blocking commits.

The architecture enforces the core reasoning chain (SIGNALS → SEMANTICS → REASONING → REPORT) as an authority hierarchy, ensuring meaning flows through proper channels from raw data to human-readable output.

## System Architecture

### Layer Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PORTFOLIO OS REPOSITORY                         │
│                                                                       │
│   docs/        engines/       reports/       data/       *.xlsx      │
│   (SSOT)       (ENGINE)       (REPORT)       (DATA)      (DATA_OUT)  │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DOMAINIZATION SYSTEM                            │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  LAYER 1: REGISTRY LAYER (Central Indexing)                 │    │
│  │                                                              │    │
│  │  artifact_registry.py ◄──── domain_registry.py              │    │
│  │  (artifact CRUD ops)        (12 canonical domains)          │    │
│  │                                                              │    │
│  │  registry_cache.py                                           │    │
│  │  (in-memory indexes, O(1) lookups)                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  LAYER 2: DOMAIN MODEL LAYER (Classification)               │    │
│  │                                                              │    │
│  │  domain_schema.py                                            │    │
│  │  (DomainDefinition dataclass, authority levels)              │    │
│  │                                                              │    │
│  │  12 Domains: GOV, ARCH, SIGNALS, SEMANTICS, REASONING,      │    │
│  │              REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  LAYER 3: LIFECYCLE MANAGEMENT LAYER (State Machines)       │    │
│  │                                                              │    │
│  │  lifecycle_schema.py          lifecycle_manager.py           │    │
│  │  (StateTransition,            (LifecycleManager class,      │    │
│  │   StateMachine dataclasses)    transition validation)        │    │
│  │                                                              │    │
│  │  11 Artifact Types: SSOT, ENGINE, REPORT_OUT, DATA_IN,      │    │
│  │  DATA_OUT, RUNTIME, DASHBOARD, SNAPSHOT, CONFIG,             │    │
│  │  CALIBRATION, STEERING                                       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  LAYER 4: VALIDATION LAYER (Observers + Orchestrator)       │    │
│  │                                                              │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │    │
│  │  │Observer 1│ │Observer 2│ │Observer 3│ │Observer 4│       │    │
│  │  │Registr.  │ │Domain    │ │Lifecycle │ │Boundary  │       │    │
│  │  │Validator │ │Assign.   │ │Validator │ │Awareness │       │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │    │
│  │                                                              │    │
│  │  ┌──────────┐     ┌────────────────────────────────┐        │    │
│  │  │Observer 5│     │  validation_orchestrator.py     │        │    │
│  │  │SSOT      │────▶│  (runs all observers,           │        │    │
│  │  │Consist.  │     │   collects warnings)            │        │    │
│  │  └──────────┘     └────────────────────────────────┘        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  LAYER 5: REPORTING LAYER (Health & Violations)             │    │
│  │                                                              │    │
│  │  health_reporter.py           violation_detector.py          │    │
│  │  (domain coverage,            (unregistered artifacts,       │    │
│  │   lifecycle distribution,      SSOT conflicts,               │    │
│  │   recommendations)             deprecated modifications)     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  CROSS-CUTTING: CLI + Hooks + Caching + Logging             │    │
│  │                                                              │    │
│  │  cli_main.py (register, validate, health, config)           │    │
│  │  hooks/pre-commit (optional, warnings only)                  │    │
│  │  registry_cache.py (indexed in-memory cache)                 │    │
│  │  audit_logger.py (structured audit trail)                    │    │
│  │  registry_backup_manager.py (automatic backups)              │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```


### Component Interaction Flow

```
User Action (commit, CLI command)
        │
        ▼
┌───────────────────┐
│   CLI / Hook      │  Entry points: cli_main.py, pre-commit hook
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Registry Cache   │  Loads artifacts, domains, lifecycles into memory
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Validation       │  Orchestrator runs 5 observers sequentially
│  Orchestrator     │  Each observer returns warnings (never blocks)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Health Reporter  │  Aggregates results into actionable report
│  + Violation Det. │  Outputs YAML or human-readable format
└───────────────────┘
```

## Design Decisions and Rationale

### Decision 1: Observability Over Enforcement

**Choice**: All validation gates operate in warning-only mode during FAST LANE phase.

**Rationale**: A visible unhealthy system is preferable to an invisible blocked system. During rapid development, blocking commits creates friction that slows report value delivery. Observability builds awareness without creating bottlenecks.

**Implication**: The `enforcement_mode` field in config controls whether violations block or warn. The system is designed to transition to hard enforcement once the report MVP stabilizes.

### Decision 2: Observer Pattern for Validation

**Choice**: Five independent validation observers coordinated by an orchestrator, rather than a monolithic validator.

**Rationale**:
- Each observer has a single responsibility (registration, domain, lifecycle, boundary, SSOT)
- Observers can be enabled/disabled independently via configuration
- New validation rules can be added as new observers without modifying existing code
- Observers can run in parallel for performance (future optimization)
- Testing is simplified — each observer is independently testable

### Decision 3: Authority Chain as First-Class Concept

**Choice**: The SIGNALS → SEMANTICS → REASONING → REPORT chain is modeled as an authority hierarchy, not just a data flow.

**Rationale**: In Portfolio OS, meaning is created progressively:
1. **SIGNALS** produces raw numerical signals (no interpretation)
2. **SEMANTICS** interprets signals into semantic states (what they mean)
3. **REASONING** draws conclusions from semantic states (what to do)
4. **REPORT** renders reasoning into human language (how to communicate)

Each layer can only create meaning within its authority. A signal engine cannot produce semantic interpretations. A report engine cannot contain business logic. This prevents architectural drift where layers bypass the chain.

### Decision 4: YAML-Based Configuration

**Choice**: All registry data stored in YAML files rather than a database.

**Rationale**:
- YAML is human-readable and git-friendly (diffs are meaningful)
- No external database dependency
- Configuration can be reviewed in pull requests
- Developers can manually edit registries when needed
- Backup and recovery is simple file operations

**Trade-off**: Performance is limited for very large registries (>10,000 artifacts). The in-memory cache mitigates this for the expected scale (100-1000 artifacts).

### Decision 5: Dual Metadata Storage

**Choice**: Markdown files use YAML frontmatter; non-markdown files use `artifact_registry.yaml`.

**Rationale**:
- Markdown frontmatter keeps metadata co-located with content (single source of truth)
- Non-markdown files (Python, Excel, JSON) cannot embed YAML frontmatter
- The registry serves as the central index regardless of storage location
- Frontmatter is parsed automatically during validation

### Decision 6: Gradual Migration Strategy

**Choice**: Artifacts can exist unregistered during the migration phase without triggering blocking errors.

**Rationale**:
- Portfolio OS has 50+ existing files that need registration
- Requiring all files to be registered before any governance works would block progress
- Health reports expose registration gaps, creating natural pressure to register
- The system becomes more valuable as more artifacts are registered

### Decision 7: Report-First Priority

**Choice**: Every system component must justify its value to report quality.

**Rationale**: Portfolio OS exists to produce investment reports. Infrastructure, governance, and architecture are means to that end. This principle prevents over-engineering governance at the expense of report delivery.

**Application**: Features that improve governance but not report quality are deferred until the report MVP is stable.


## Component Details

### Layer 1: Registry Layer

| Component | File | Purpose |
|-----------|------|---------|
| Artifact Registry | `artifact_registry.py` | CRUD operations for artifact metadata |
| Domain Registry | `domain_registry.py` | Domain definition loading and queries |
| Registry Cache | `registry_cache.py` | In-memory indexed cache for performance |
| Artifact Schema | `artifact_schema.py` | `ArtifactMetadata` dataclass and validation |

**Key interfaces**:
- `ArtifactRegistry.register_artifact(metadata)` — Add artifact to registry
- `ArtifactRegistry.get_artifact(artifact_id)` — Retrieve by ID
- `DomainRegistry.validate_domain_assignment(type, domain)` — Check ownership rules
- `RegistryCache.list_artifacts_by_domain(domain_id)` — O(1) indexed query

### Layer 2: Domain Model Layer

| Component | File | Purpose |
|-----------|------|---------|
| Domain Schema | `domain_schema.py` | `DomainDefinition` dataclass with authority |

**12 Canonical Domains**:

| Domain | Priority | Authority Level | Responsibility |
|--------|----------|-----------------|----------------|
| SIGNALS | Core | 1 (highest) | Raw signal generation |
| SEMANTICS | Core | 2 | Semantic interpretation |
| REASONING | Core | 3 | Reasoning and conclusions |
| REPORT | Core | 4 | Human-readable output |
| GOV | Surface | — | Governance and rules |
| ARCH | Surface | — | Architecture decisions |
| STATE | Surface | — | Portfolio state management |
| DATA | Surface | — | Data ingestion and normalization |
| USER | Surface | — | User interface and dashboards |
| DEPLOY | Surface | — | Deployment and infrastructure |
| MEMORY | Surface | — | Historical data and snapshots |
| SIM | Surface | — | Simulation and scenarios |

### Layer 3: Lifecycle Management Layer

| Component | File | Purpose |
|-----------|------|---------|
| Lifecycle Schema | `lifecycle_schema.py` | `StateMachine`, `StateTransition` dataclasses |
| Lifecycle Manager | `lifecycle_manager.py` | State machine loading and transition validation |

**State machines per artifact type**:
- **SSOT**: draft → review → canonical → deprecated
- **ENGINE**: planned → development → active → deprecated
- **REPORT_OUT**: generated → current → archived
- **DATA_IN**: active → stale → archived
- **DATA_OUT**: generated → current → archived
- **RUNTIME**: planned → active → deprecated
- **DASHBOARD**: planned → active → deprecated
- **SNAPSHOT**: current → archived
- **CONFIG**: draft → active → deprecated
- **CALIBRATION**: draft → active → deprecated
- **STEERING**: draft → active → deprecated

### Layer 4: Validation Layer

| Component | File | Purpose |
|-----------|------|---------|
| Observer 1 | `observer_registration.py` | Detects unregistered artifacts |
| Observer 2 | `observer_domain_assignment.py` | Validates domain-type ownership |
| Observer 3 | `observer_lifecycle.py` | Validates state transitions |
| Observer 4 | `observer_boundary_awareness.py` | Enforces authority chains |
| Observer 5 | `observer_ssot_consistency.py` | Prevents SSOT conflicts |
| Orchestrator | `validation_orchestrator.py` | Coordinates all observers |
| Error Classes | `validation_error_classes.py` | Structured error codes (E001-E010) |
| Result Model | `validation_result.py` | `ValidationResult` dataclass |

### Layer 5: Reporting Layer

| Component | File | Purpose |
|-----------|------|---------|
| Health Reporter | `health_reporter.py` | Generates comprehensive health reports |
| Violation Detector | `violation_detector.py` | Identifies governance violations |

### Cross-Cutting Concerns

| Component | File | Purpose |
|-----------|------|---------|
| CLI Main | `cli_main.py` | Entry point with subcommands |
| CLI Registry | `cli_registry_commands.py` | register, update, list, show |
| CLI Validation | `cli_validation_commands.py` | validate command |
| CLI Health | `cli_health_commands.py` | health command |
| CLI Config | `cli_config_commands.py` | config show/set |
| CLI Recovery | `cli_recovery_commands.py` | backup restore |
| Audit Logger | `audit_logger.py` | Structured audit trail |
| Backup Manager | `registry_backup_manager.py` | Automatic registry backups |
| Recovery Manager | `registry_recovery_manager.py` | Restore from backups |


## Extension Points

The architecture is designed for extensibility at three primary points:

### Adding New Domains

**Where**: `.domainization/domain_registry.yaml`

**Steps**:
1. Add a new domain entry to `domain_registry.yaml`:
   ```yaml
   - domain_id: "NEW_DOMAIN"
     name: "New Domain Name"
     responsibility_scope: "What this domain owns"
     allowed_artifact_types: ["ENGINE", "SSOT", "CONFIG"]
     cannot_own: ["REPORT_OUT"]
     priority: "surface"
     authority_level: null
   ```
2. The `DomainRegistry` class automatically loads new domains on next cache refresh
3. Validation observers will recognize the new domain immediately
4. No code changes required — purely configuration-driven

**Constraints**:
- Domain IDs must be unique uppercase strings
- `allowed_artifact_types` must reference valid artifact types
- Core domains (with `authority_level`) should only be added with governance approval

### Adding New Artifact Types

**Where**: `.domainization/lifecycle_state_machine.yaml`

**Steps**:
1. Define the new artifact type's state machine in `lifecycle_state_machine.yaml`:
   ```yaml
   NEW_TYPE:
     states: [draft, active, deprecated]
     transitions:
       - from: draft
         to: active
         condition: "Ready for use"
       - from: active
         to: deprecated
         condition: "Superseded"
   ```
2. Add the new type to relevant domains' `allowed_artifact_types` in `domain_registry.yaml`
3. The `LifecycleManager` automatically loads new state machines
4. Validation observers will validate transitions for the new type

**Constraints**:
- Each artifact type must have at least one state
- Transitions must reference valid states within the same type
- The first state in the `states` list is the initial state for new artifacts

### Adding New Validation Observers (Gates)

**Where**: `.domainization/src/` (new Python file)

**Steps**:
1. Create a new observer file following the naming pattern `observer_<name>.py`:
   ```python
   from validation_result import ValidationResult

   class NewObserver:
       """Observer N: Description of what it validates."""

       def __init__(self, registry_cache=None):
           self.cache = registry_cache

       def validate(self, changed_files=None, artifacts=None):
           """Run validation and return list of ValidationResult."""
           results = []
           # ... validation logic ...
           results.append(ValidationResult(
               success=True,
               gate_name="new_observer",
               artifact_id=artifact_id,
               error_message="Description of issue",
               suggestion="How to fix it",
               severity="warning"
           ))
           return results
   ```
2. Register the observer in `validation_orchestrator.py`:
   ```python
   from observer_new_name import NewObserver

   class ValidationOrchestrator:
       def __init__(self):
           self.observers = [
               RegistrationValidator(),
               DomainAssignmentValidator(),
               LifecycleValidator(),
               BoundaryAwarenessValidator(),
               SSOTConsistencyValidator(),
               NewObserver(),  # Add here
           ]
   ```
3. Add configuration toggle in `.domainization/config.yaml` if needed

**Constraints**:
- Observers must return `ValidationResult` objects
- In observability mode, observers must never raise exceptions that block commits
- Observers should target < 1 second execution time individually
- Each observer should have a corresponding test file `test_observer_<name>.py`

### Adding New CLI Commands

**Where**: `.domainization/src/cli_<category>_commands.py`

**Steps**:
1. Create or extend a CLI command module:
   ```python
   import argparse

   def register_commands(subparsers):
       """Register subcommands for this category."""
       parser = subparsers.add_parser('new-command', help='Description')
       parser.add_argument('--flag', help='Flag description')
       parser.set_defaults(func=handle_new_command)

   def handle_new_command(args):
       """Handle the new-command subcommand."""
       # Implementation
       pass
   ```
2. Register in `cli_main.py`:
   ```python
   from cli_new_commands import register_commands as register_new
   register_new(subparsers)
   ```

## Data Flow

### Registration Flow

```
Developer creates/modifies file
        │
        ▼
CLI: domainization register <file>
        │
        ▼
ArtifactRegistry.register_artifact()
        │
        ├──▶ Validate metadata schema
        ├──▶ Check domain assignment validity
        ├──▶ Verify lifecycle state is valid initial state
        ├──▶ Create backup of registry
        │
        ▼
Write to artifact_registry.yaml
        │
        ▼
RegistryCache.invalidate()  (next query triggers reload)
```

### Validation Flow

```
Pre-commit hook OR CLI: domainization validate
        │
        ▼
ValidationOrchestrator.run_all()
        │
        ├──▶ Observer 1: Check registration completeness
        ├──▶ Observer 2: Validate domain assignments
        ├──▶ Observer 3: Validate lifecycle transitions
        ├──▶ Observer 4: Check boundary/authority violations
        ├──▶ Observer 5: Check SSOT consistency
        │
        ▼
Collect all ValidationResult objects
        │
        ▼
Format and display warnings (never block in observability mode)
```

### Health Report Flow

```
CLI: domainization health
        │
        ▼
HealthReporter.generate_health_report()
        │
        ├──▶ Load all artifacts via RegistryCache
        ├──▶ Calculate domain coverage
        ├──▶ Calculate lifecycle distribution
        ├──▶ Run ViolationDetector.detect_violations()
        ├──▶ Generate recommendations
        │
        ▼
Output YAML report to stdout or file
```

## Performance Architecture

### Caching Strategy

The `RegistryCache` provides the performance backbone:

- **Lazy loading**: Cache loads on first access, not at import time
- **File modification tracking**: Compares mtimes to avoid unnecessary reloads
- **Multi-index structure**: Separate indexes for domain, type, lifecycle, topic
- **O(1) lookups**: All indexed queries are constant-time dictionary lookups

### Performance Targets

| Operation | Target | Mechanism |
|-----------|--------|-----------|
| Full validation (1000 artifacts) | < 5 seconds | Cached indexes |
| Health report generation | < 10 seconds | Cached aggregation |
| Single artifact lookup | < 1 ms | Direct dictionary access |
| Domain query | < 1 ms | Pre-built domain index |
| Cache refresh | < 4 seconds | YAML parsing + index rebuild |

### Scalability Limits

- **Domains**: Supports 20+ domains (currently 12)
- **Artifact types**: Supports 10+ lifecycle states per type
- **Artifacts**: Optimized for 1000 artifacts, functional up to ~10,000
- **Observers**: Linear scaling with observer count (currently 5)

## Security and Safety

### Non-Destructive by Design

- Validation never modifies artifacts or registry
- Pre-commit hook never blocks commits (observability mode)
- Backup created before every registry write
- Recovery available from any backup

### Audit Trail

All significant operations are logged:
- Artifact registration and updates
- Lifecycle transitions
- Validation results
- Configuration changes
- Backup and recovery operations

Logs stored in `.domainization/logs/audit_*.log` with rotation.

## Testing

### Test Coverage

```bash
# Run all domainization tests
cd .domainization/src
python -m pytest -v

# Run specific layer tests
python -m pytest test_artifact_registry*.py -v          # Registry layer
python -m pytest test_domain_*.py -v                    # Domain model layer
python -m pytest test_lifecycle_*.py -v                 # Lifecycle layer
python -m pytest test_observer_*.py -v                  # Validation layer
python -m pytest test_health_reporter*.py test_violation_detector.py -v  # Reporting layer
python -m pytest test_registry_cache*.py -v             # Caching
python -m pytest test_cli_*.py -v                       # CLI
```

### Test Organization

| Test File | Tests |
|-----------|-------|
| `test_artifact_registry.py` | Registry CRUD operations |
| `test_artifact_registry_ops.py` | Advanced registry queries |
| `test_domain_registry.py` | Domain loading and queries |
| `test_domain_schema.py` | Domain dataclass validation |
| `test_lifecycle_schema.py` | State machine dataclass logic |
| `test_lifecycle_manager.py` | Transition validation |
| `test_lifecycle_state_machine.py` | State machine definitions |
| `test_observer_registration.py` | Observer 1 tests |
| `test_observer_domain_assignment.py` | Observer 2 tests |
| `test_observer_lifecycle.py` | Observer 3 tests |
| `test_observer_boundary_awareness.py` | Observer 4 tests |
| `test_observer_ssot_consistency.py` | Observer 5 tests |
| `test_validation_orchestrator.py` | Orchestrator integration |
| `test_health_reporter.py` | Health report generation |
| `test_health_reporter_with_violations.py` | Violation scenarios |
| `test_violation_detector.py` | Violation detection logic |
| `test_registry_cache.py` | Cache operations |
| `test_registry_cache_performance.py` | Performance benchmarks |
| `test_cli_*.py` | CLI command tests |
| `test_audit_logger.py` | Audit logging |
| `test_registry_backup_manager.py` | Backup operations |
| `test_registry_recovery_manager.py` | Recovery operations |

## Requirements Satisfied

This documentation satisfies the following requirements:

- ✅ **Requirement 15.10**: Validation rules are clearly documented
- ✅ System architecture documented with component diagrams
- ✅ Design decisions explained with rationale
- ✅ Extension points documented for adding domains, artifact types, and gates
- ✅ Layer responsibilities and interfaces described
- ✅ Data flow documented for registration, validation, and health reporting
- ✅ Performance architecture and targets documented

## Related Files

### Configuration Files
- `.domainization/domain_registry.yaml` — Domain definitions
- `.domainization/lifecycle_state_machine.yaml` — State machine definitions
- `.domainization/artifact_registry.yaml` — Artifact metadata store

### Source Files (by layer)
- **Registry**: `artifact_registry.py`, `domain_registry.py`, `registry_cache.py`, `artifact_schema.py`
- **Domain Model**: `domain_schema.py`
- **Lifecycle**: `lifecycle_schema.py`, `lifecycle_manager.py`
- **Validation**: `observer_*.py`, `validation_orchestrator.py`, `validation_error_classes.py`, `validation_result.py`
- **Reporting**: `health_reporter.py`, `violation_detector.py`
- **CLI**: `cli_main.py`, `cli_*_commands.py`
- **Infrastructure**: `audit_logger.py`, `registry_backup_manager.py`, `registry_recovery_manager.py`

### Other Documentation
- `README_registry_layer_python_api.md` — Registry API details
- `README_validation_observers.md` — Observer implementation details
- `README_reporting_layer.md` — Reporting layer details
- `README_registry_cache.md` — Cache implementation details
- `README_cli_usage.md` — CLI usage guide
- `README_backup_and_recovery.md` — Backup system details
- `README_error_handling_and_audit_logging.md` — Error handling details
