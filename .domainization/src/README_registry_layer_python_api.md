# Domainization Registry Layer

This directory contains the Python implementation of the domainization registry layer - the core data models and operations for managing artifacts, domains, and lifecycle state machines.

## Overview

The registry layer provides three main registries:
- **Artifact Registry**: Tracks all artifacts in the system with metadata
- **Domain Registry**: Defines the 12 canonical domains and their boundaries
- **Lifecycle State Machines**: Defines valid states and transitions for each artifact type

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Registry Layer                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐│
│  │ Artifact Registry│  │ Domain Registry  │  │ Lifecycle  ││
│  │                  │  │                  │  │ Manager    ││
│  │ - Load/Save      │  │ - Load domains   │  │ - Validate ││
│  │ - Register       │  │ - Query domains  │  │   transitions││
│  │ - Update         │  │ - Validate       │  │ - Check    ││
│  │ - Query          │  │   assignments    │  │   modifiable││
│  └──────────────────┘  └──────────────────┘  └────────────┘│
│         │                      │                     │       │
│         ▼                      ▼                     ▼       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐│
│  │ ArtifactMetadata │  │ DomainDefinition │  │ StateMachine││
│  │ Data Model       │  │ Data Model       │  │ Data Model ││
│  └──────────────────┘  └──────────────────┘  └────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │     YAML Configuration      │
              │                             │
              │ - artifact_registry.yaml    │
              │ - domain_registry.yaml      │
              │ - lifecycle_state_machine.yaml│
              └─────────────────────────────┘
```

## Core Components

### 1. Artifact Registry (`artifact_registry.py`)

Manages the artifact registry with full CRUD operations.

**Key Classes:**
- `ArtifactRegistry`: Main registry operations class

**Key Methods:**
```python
registry = ArtifactRegistry()
registry.load()  # Load from YAML

# Register new artifact
registry.register_artifact(metadata)

# Update existing artifact
registry.update_artifact(artifact_id, metadata)

# Query operations
artifact = registry.get_artifact(artifact_id)
artifacts = registry.list_artifacts_by_domain('SIGNALS')
artifacts = registry.list_artifacts_by_type('ENGINE')
artifacts = registry.list_artifacts_by_lifecycle('active')

# Save changes
registry.save()  # Creates backup before saving
```

**Features:**
- Automatic backup before saving
- Validation on register/update
- Frontmatter parsing for markdown files
- Multiple query methods

### 2. Artifact Metadata (`artifact_schema.py`)

Data model for artifact metadata with validation.

**Key Classes:**
- `ArtifactMetadata`: Artifact metadata dataclass

**Required Fields:**
- `artifact_id`, `file_path`, `primary_domain`, `artifact_type`
- `lifecycle_status`, `created_date`, `last_modified`, `owner_role`
- `ssot_relationship`, `allowed_writers`, `allowed_readers`

**Optional Fields:**
- `secondary_domains`, `dependencies`, `topic`, `description`, `tags`

**Key Methods:**
```python
metadata = ArtifactMetadata(...)

# Validation
is_valid, errors = metadata.validate()

# Permission checks
can_modify = metadata.is_modifiable()  # Based on lifecycle
can_write = metadata.can_write('SIGNALS')
can_read = metadata.can_read('REPORT')
```

### 3. Domain Registry (`domain_registry.py`)

Manages the 12 canonical domains and their boundaries.

**Key Classes:**
- `DomainRegistry`: Domain registry operations class

**Key Methods:**
```python
registry = DomainRegistry()
registry.load()

# Query domains
domain = registry.get_domain('SIGNALS')
all_domains = registry.list_domains()
core_domains = registry.list_core_domains()  # 4 core reasoning domains
surface_domains = registry.list_surface_domains()  # 8 surface domains

# Validate domain assignments
is_valid, error = registry.validate_domain_assignment('ENGINE', 'SIGNALS')
valid_domains = registry.get_valid_domains_for_type('ENGINE')

# Get core reasoning chain in authority order
chain = registry.get_core_reasoning_chain()  # [SIGNALS, SEMANTICS, REASONING, REPORT]
```

### 4. Domain Definition (`domain_schema.py`)

Data model for domain definitions.

**Key Classes:**
- `DomainDefinition`: Domain definition dataclass

**Fields:**
- `domain_id`, `name`, `responsibility_scope`
- `allowed_artifact_types`, `cannot_own`
- `priority` (core/surface), `authority_level` (1-4 for core, None for surface)

**Key Methods:**
```python
domain = DomainDefinition(...)

# Check artifact type ownership
can_own = domain.can_own_type('ENGINE')

# Check domain type
is_core = domain.is_core_domain()

# Get authority level (1=highest, 999=surface)
level = domain.get_authority_level()
```

### 5. Lifecycle Manager (`lifecycle_manager.py`)

Manages lifecycle state machines for all artifact types.

**Key Classes:**
- `LifecycleManager`: Lifecycle operations class

**Key Methods:**
```python
manager = LifecycleManager()
manager.load()

# Get state machine for artifact type
sm = manager.get_state_machine('SSOT')

# Validate transitions
is_valid, error = manager.validate_transition('SSOT', 'draft', 'review')
allowed = manager.get_allowed_transitions('SSOT', 'draft')

# Check modifiability
can_modify = manager.is_modifiable('SSOT', 'deprecated')  # False

# Get initial state for new artifacts
initial = manager.get_initial_state('ENGINE')  # 'planned'
```

### 6. Lifecycle State Machine (`lifecycle_schema.py`)

Data models for state machines and transitions.

**Key Classes:**
- `StateTransition`: Represents a valid state transition
- `StateMachine`: Complete state machine for an artifact type

**Key Methods:**
```python
sm = StateMachine(...)

# Check transition validity
is_valid = sm.is_valid_transition('draft', 'review')

# Get allowed transitions
next_states = sm.get_allowed_transitions('draft')

# Check modifiability
can_modify = sm.is_modifiable('deprecated')  # False

# Get initial state
initial = sm.get_initial_state()
```

## The 12 Canonical Domains

### Core Reasoning Chain (Authority Levels 1-4)
1. **SIGNALS** (Level 1): Raw signal calculation, market data processing
2. **SEMANTICS** (Level 2): Semantic state creation, signal interpretation
3. **REASONING** (Level 3): Decision logic, portfolio conclusions
4. **REPORT** (Level 4): Human-readable report generation

### Surface Domains
- **GOV**: Governance, decision frameworks, confidence models
- **ARCH**: System design, architecture, integration patterns
- **STATE**: Portfolio holdings, watchlist management
- **DATA**: Data ingestion, normalization, ETL processes
- **USER**: Dashboard, visualization, user interaction
- **DEPLOY**: Runtime orchestration, deployment scripts
- **MEMORY**: Historical snapshots, portfolio memory
- **SIM**: Scenario modeling, what-if analysis

## Artifact Types

11 artifact types with distinct lifecycle state machines:

1. **SSOT**: Single Source of Truth documents (draft → review → canonical → deprecated)
2. **ENGINE**: Implementation code (planned → development → active → deprecated)
3. **REPORT_OUT**: Generated reports (generated → current → archived) [read-only]
4. **DATA_IN**: Input data files (active → stale → archived)
5. **DATA_OUT**: Output data files (generated → current → archived) [read-only]
6. **RUNTIME**: Execution scripts (development → active → deprecated)
7. **DASHBOARD**: UI components (development → active → deprecated)
8. **SNAPSHOT**: Historical captures (captured → archived) [read-only]
9. **CONFIG**: Configuration files (draft → active → deprecated)
10. **CALIBRATION**: Calibration documents (draft → active → superseded)
11. **STEERING**: Kiro steering rules (draft → active → deprecated)

## Usage Examples

### Example 1: Register a New Artifact

```python
from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata

# Create metadata
metadata = ArtifactMetadata(
    artifact_id='signals_momentum_engine',
    file_path='signals/momentum_calculator.py',
    primary_domain='SIGNALS',
    artifact_type='ENGINE',
    lifecycle_status='development',
    created_date='2026-05-25',
    last_modified='2026-05-25',
    owner_role='Signals Engineer',
    ssot_relationship='implementation',
    allowed_writers=['SIGNALS'],
    allowed_readers=['ALL'],
    description='Momentum signal calculation engine'
)

# Register
registry = ArtifactRegistry()
registry.load()
registry.register_artifact(metadata)
registry.save()
```

### Example 2: Validate Domain Assignment

```python
from domain_registry import DomainRegistry

registry = DomainRegistry()
registry.load()

# Check if SIGNALS can own ENGINE
is_valid, error = registry.validate_domain_assignment('ENGINE', 'SIGNALS')
if is_valid:
    print("✓ SIGNALS can own ENGINE artifacts")
else:
    print(f"✗ {error}")

# Get all valid domains for ENGINE
valid_domains = registry.get_valid_domains_for_type('ENGINE')
print(f"Valid domains for ENGINE: {', '.join(valid_domains)}")
```

### Example 3: Validate Lifecycle Transition

```python
from lifecycle_manager import LifecycleManager

manager = LifecycleManager()
manager.load()

# Check if transition is valid
is_valid, error = manager.validate_transition('SSOT', 'draft', 'review')
if is_valid:
    print("✓ Can transition from draft to review")
else:
    print(f"✗ {error}")

# Get allowed transitions
allowed = manager.get_allowed_transitions('SSOT', 'draft')
print(f"From draft, can transition to: {', '.join(allowed)}")
```

### Example 4: Query Artifacts by Domain

```python
from artifact_registry import ArtifactRegistry

registry = ArtifactRegistry()
registry.load()

# Get all SIGNALS artifacts
signals_artifacts = registry.list_artifacts_by_domain('SIGNALS')
print(f"Found {len(signals_artifacts)} SIGNALS artifacts:")
for artifact in signals_artifacts:
    print(f"  - {artifact.artifact_id} ({artifact.artifact_type})")
```

## Testing

Comprehensive test suite with 184 tests covering all functionality:

```bash
# Run all tests
python -m pytest .domainization/src/test_*.py -v

# Run specific test file
python -m pytest .domainization/src/test_artifact_registry_ops.py -v

# Run with coverage
python -m pytest .domainization/src/test_*.py --cov=.domainization/src
```

**Test Files:**
- `test_artifact_registry.py`: Artifact metadata and schema validation (26 tests)
- `test_artifact_registry_ops.py`: Artifact registry operations (18 tests)
- `test_domain_registry.py`: Domain registry schema validation (18 tests)
- `test_domain_registry_ops.py`: Domain registry operations (21 tests)
- `test_domain_schema.py`: Domain definition data model (19 tests)
- `test_lifecycle_schema.py`: Lifecycle state machine data model (23 tests)
- `test_lifecycle_manager.py`: Lifecycle manager operations (26 tests)
- `test_lifecycle_state_machine.py`: State machine YAML validation (33 tests)

## File Structure

```
.domainization/src/
├── README.md                          # This file
├── artifact_schema.py                 # Artifact metadata data model
├── artifact_registry.py               # Artifact registry operations
├── domain_schema.py                   # Domain definition data model
├── domain_registry.py                 # Domain registry operations
├── lifecycle_schema.py                # Lifecycle state machine data model
├── lifecycle_manager.py               # Lifecycle manager operations
├── test_artifact_registry.py          # Artifact schema tests
├── test_artifact_registry_ops.py      # Artifact registry tests
├── test_domain_registry.py            # Domain schema tests
├── test_domain_registry_ops.py        # Domain registry tests
├── test_domain_schema.py              # Domain definition tests
├── test_lifecycle_schema.py           # Lifecycle schema tests
├── test_lifecycle_manager.py          # Lifecycle manager tests
└── test_lifecycle_state_machine.py    # State machine YAML tests
```

## Design Principles

1. **Separation of Concerns**: Data models, operations, and validation are cleanly separated
2. **Validation First**: All operations validate data before making changes
3. **Immutability Where Appropriate**: Read-only states prevent accidental modifications
4. **Clear Authority Chain**: Core reasoning domains have explicit authority levels
5. **Type Safety**: Dataclasses provide type hints and validation
6. **Comprehensive Testing**: 184 tests ensure reliability

## Next Steps

This registry layer provides the foundation for:
- CLI tools for artifact management (Task 3)
- Validation rules enforcement (Task 4)
- Git hooks for automated validation (Task 5)
- Kiro agent integration (Task 6)

## Requirements Satisfied

This implementation satisfies requirements:
- **1.1-1.6**: Artifact metadata and registry operations
- **2.1-2.8**: Domain definitions and validation
- **4.1-4.7**: Lifecycle state machines and transitions
- **8.1-8.6**: Permission checking and modifiability rules
