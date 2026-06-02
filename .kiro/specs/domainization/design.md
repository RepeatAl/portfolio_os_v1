# Design Document

## Overview

The domainization system provides artifact governance for Portfolio OS through a layered architecture consisting of:

1. **Registry Layer** - Central indexing of all artifacts with metadata
2. **Domain Model Layer** - Definition of 12 canonical domains with authority boundaries
3. **Lifecycle Management Layer** - State machines for artifact evolution
4. **Validation Layer** - Commit gates enforcing governance rules
5. **Reporting Layer** - Health monitoring and violation detection

The design prioritizes the core reasoning chain (SIGNALS → SEMANTICS → REASONING → REPORT) over surface domains, implements soft validation during the FAST LANE REPORT MVP phase, and ensures that governance supports rather than blocks report development.

### Design Principles

1. **Report-First**: Every component must justify its value to report quality
2. **Gradual Enforcement**: Start with soft validation, harden as system matures
3. **Authority Chains**: Runtime flows represent who can create meaning, not just data movement
4. **Core Domain Priority**: Reasoning domains take precedence over surface domains
5. **Explainability**: All validation failures provide actionable guidance
6. **Determinism**: Same input always produces same validation result
7. **Non-Breaking**: Existing functionality continues working during migration

## Architecture

### System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PORTFOLIO OS REPOSITORY                      │
│                                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │   docs/    │  │  engines/  │  │  reports/  │  │   data/   │ │
│  │   (SSOT)   │  │  (ENGINE)  │  │ (REPORT)   │  │  (DATA)   │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘ │
│                                                                   │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAINIZATION SYSTEM                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    REGISTRY LAYER                         │  │
│  │  ┌────────────────┐         ┌──────────────────┐         │  │
│  │  │    Artifact    │◄────────┤     Domain       │         │  │
│  │  │    Registry    │         │     Registry     │         │  │
│  │  └────────────────┘         └──────────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 LIFECYCLE LAYER                           │  │
│  │  ┌────────────────┐         ┌──────────────────┐         │  │
│  │  │     State      │◄────────┤   Transition     │         │  │
│  │  │    Machine     │         │    Validator     │         │  │
│  │  └────────────────┘         └──────────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 VALIDATION LAYER                          │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐       │  │
│  │  │Gate 1│─▶│Gate 2│─▶│Gate 3│─▶│Gate 4│─▶│Gate 5│       │  │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 REPORTING LAYER                           │  │
│  │  ┌────────────────┐         ┌──────────────────┐         │  │
│  │  │     Health     │         │    Violation     │         │  │
│  │  │    Reporter    │         │    Detector      │         │  │
│  │  └────────────────┘         └──────────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Git Commit   │
                    │  Hook System  │
                    └───────────────┘
```



## Components and Interfaces

### 1. Registry Layer

#### Artifact Registry

**Purpose**: Central index of all artifacts with metadata

**Data Structure**:
```yaml
artifacts:
  - artifact_id: string (unique identifier)
    file_path: string (relative path from repo root)
    primary_domain: string (domain ID)
    secondary_domains: list[string] (optional)
    artifact_type: string (type ID)
    lifecycle_status: string (current state)
    created_date: string (YYYY-MM-DD)
    last_modified: string (YYYY-MM-DD)
    owner_role: string (responsibility description)
    ssot_relationship: string (canonical|derived|implementation)
    allowed_writers: list[string] (domain IDs)
    allowed_readers: list[string] (domain IDs, "ALL" for public)
    dependencies: list[string] (artifact IDs)
```

**Operations**:
- `register_artifact(metadata)` - Add new artifact to registry
- `update_artifact(artifact_id, metadata)` - Update existing artifact
- `get_artifact(artifact_id)` - Retrieve artifact metadata
- `list_artifacts_by_domain(domain_id)` - Get all artifacts for a domain
- `list_artifacts_by_type(artifact_type)` - Get all artifacts of a type
- `list_artifacts_by_lifecycle(lifecycle_status)` - Get artifacts in a state
- `validate_artifact_metadata(metadata)` - Check metadata completeness

**Storage**: `.domainization/artifact_registry.yaml`

**Frontmatter Support**: Markdown files can embed metadata in YAML frontmatter instead of registry entries

#### Domain Registry

**Purpose**: Define canonical domains with authority boundaries

**Data Structure**:
```yaml
domains:
  - domain_id: string (unique identifier)
    name: string (human-readable name)
    responsibility_scope: string (what this domain owns)
    allowed_artifact_types: list[string] (type IDs)
    cannot_own: list[string] (explicit exclusions)
    priority: string (core|surface)
    authority_level: int (1=highest for SIGNALS, 4=lowest for REPORT in reasoning chain)
```

**Operations**:
- `get_domain(domain_id)` - Retrieve domain definition
- `list_domains()` - Get all domains
- `list_core_domains()` - Get core reasoning domains
- `list_surface_domains()` - Get surface domains
- `validate_domain_assignment(artifact_type, domain_id)` - Check if domain can own type
- `get_domain_priority(domain_id)` - Get priority level

**Storage**: `.domainization/domain_registry.yaml`

**Core Reasoning Chain**: SIGNALS (1) → SEMANTICS (2) → REASONING (3) → REPORT (4)

**Surface Domains**: STATE, DATA, USER, DEPLOY, MEMORY, SIM, GOV, ARCH



### 2. Lifecycle Management Layer

#### State Machine Engine

**Purpose**: Define and enforce lifecycle state transitions

**Data Structure**:
```yaml
artifact_types:
  SSOT:
    states: [draft, review, canonical, deprecated]
    transitions:
      - from: draft
        to: review
        condition: "Author completes initial version"
      - from: review
        to: canonical
        condition: "Domain owner approves"
      - from: canonical
        to: draft
        condition: "Revision required"
      - from: canonical
        to: deprecated
        condition: "Superseded by new version"
    
  ENGINE:
    states: [planned, development, active, deprecated]
    transitions:
      - from: planned
        to: development
        condition: "Implementation begins"
      - from: development
        to: active
        condition: "Production ready"
      - from: development
        to: development
        condition: "Iteration allowed"
      - from: active
        to: deprecated
        condition: "Replaced by new engine"
    
  REPORT_OUT:
    states: [generated, current, archived]
    transitions:
      - from: generated
        to: current
        condition: "Becomes latest version"
      - from: current
        to: archived
        condition: "Superseded by newer report"
```

**Operations**:
- `get_state_machine(artifact_type)` - Get state machine for type
- `validate_transition(artifact_type, from_state, to_state)` - Check if transition is valid
- `get_allowed_transitions(artifact_type, current_state)` - Get valid next states
- `is_modifiable(artifact_type, lifecycle_status)` - Check if artifact can be modified

**Storage**: `.domainization/lifecycle_state_machine.yaml`

**Special Rules**:
- Deprecated artifacts cannot be modified (except metadata)
- Only one canonical SSOT per topic
- Current reports automatically archive previous current

#### Transition Validator

**Purpose**: Enforce state machine rules during artifact updates

**Operations**:
- `validate_lifecycle_change(artifact_id, new_status)` - Validate state transition
- `check_deprecated_modification(artifact_id)` - Block modifications to deprecated artifacts
- `enforce_canonical_uniqueness(topic, artifact_id)` - Ensure single canonical SSOT



### 3. Validation Layer (Commit Gates)

#### Gate 1: Artifact Registration Validator

**Purpose**: Ensure all artifacts have metadata

**Validation Logic**:
```python
def validate_registration(changed_files):
    for file in changed_files:
        if file.is_new() or file.is_modified():
            metadata = get_metadata(file)
            if metadata is None:
                return ValidationError(
                    f"Artifact {file.path} missing domain metadata",
                    suggestion="Add YAML frontmatter or register in artifact_registry.yaml"
                )
            if not validate_metadata_schema(metadata):
                return ValidationError(
                    f"Invalid metadata for {file.path}",
                    suggestion="Required fields: artifact_id, primary_domain, artifact_type, lifecycle_status"
                )
    return ValidationSuccess()
```

**Enforcement Mode**: 
- FAST LANE phase: Warning only (soft validation)
- Post-MVP phase: Blocking (hard validation)

#### Gate 2: Domain Assignment Validator

**Purpose**: Validate domain assignments against domain registry

**Validation Logic**:
```python
def validate_domain_assignment(artifact):
    domain = get_domain(artifact.primary_domain)
    if domain is None:
        return ValidationError(
            f"Invalid domain '{artifact.primary_domain}' for {artifact.file_path}",
            suggestion=f"Valid domains: {list_domains()}"
        )
    
    if artifact.artifact_type not in domain.allowed_artifact_types:
        return ValidationError(
            f"Domain '{artifact.primary_domain}' cannot own artifact type '{artifact.artifact_type}'",
            suggestion=f"Valid domains for {artifact.artifact_type}: {get_valid_domains(artifact.artifact_type)}"
        )
    
    return ValidationSuccess()
```

**Enforcement Mode**: 
- FAST LANE phase: Warning only
- Post-MVP phase: Blocking

#### Gate 3: Lifecycle Validator

**Purpose**: Enforce valid lifecycle state transitions

**Validation Logic**:
```python
def validate_lifecycle_transition(artifact_id, new_status):
    artifact = get_artifact(artifact_id)
    old_status = artifact.lifecycle_status
    
    if not is_valid_transition(artifact.artifact_type, old_status, new_status):
        return ValidationError(
            f"Invalid lifecycle transition: {old_status} → {new_status}",
            suggestion=f"Valid transitions from {old_status}: {get_allowed_transitions(artifact.artifact_type, old_status)}"
        )
    
    if old_status == "deprecated" and artifact.is_modified():
        return ValidationError(
            f"Cannot modify deprecated artifact {artifact_id}",
            suggestion="Only metadata updates allowed for deprecated artifacts"
        )
    
    return ValidationSuccess()
```

**Enforcement Mode**: 
- FAST LANE phase: Warning only
- Post-MVP phase: Blocking



#### Gate 4: Boundary Enforcement Validator

**Purpose**: Enforce domain ownership and writer rules

**Validation Logic**:
```python
def validate_boundary_enforcement(artifact, modifier_domain):
    if modifier_domain not in artifact.allowed_writers:
        return ValidationError(
            f"Domain '{modifier_domain}' cannot modify {artifact.file_path}",
            suggestion=f"Request approval from {artifact.primary_domain} owner"
        )
    
    # Check authority chain violations
    if is_authority_chain_violation(artifact, modifier_domain):
        return ValidationError(
            f"Authority chain violation: {modifier_domain} cannot create meaning in {artifact.primary_domain} domain",
            suggestion="Follow authority chain: SIGNALS → SEMANTICS → REASONING → REPORT"
        )
    
    return ValidationSuccess()

def is_authority_chain_violation(artifact, modifier_domain):
    # SIGNALS can only write raw signals
    if modifier_domain == "SIGNALS" and artifact.artifact_type in ["SEMANTIC_STATE", "REASONING_OBJECT"]:
        return True
    
    # SEMANTICS can only write semantic states
    if modifier_domain == "SEMANTICS" and artifact.artifact_type in ["SIGNAL", "REASONING_OBJECT"]:
        return True
    
    # REASONING can only write reasoning objects
    if modifier_domain == "REASONING" and artifact.artifact_type in ["SIGNAL", "SEMANTIC_STATE"]:
        return True
    
    # REPORT can only write human-readable text
    if modifier_domain == "REPORT" and artifact.artifact_type in ["SIGNAL", "SEMANTIC_STATE", "REASONING_OBJECT"]:
        return True
    
    return False
```

**Enforcement Mode**: 
- FAST LANE phase: Warning only
- Post-MVP phase: Blocking

#### Gate 5: SSOT Consistency Validator

**Purpose**: Prevent SSOT conflicts and maintain authority

**Validation Logic**:
```python
def validate_ssot_consistency(artifact):
    if artifact.ssot_relationship == "canonical":
        # Check for existing canonical SSOT on same topic
        existing_canonical = find_canonical_ssot(artifact.topic)
        if existing_canonical and existing_canonical.artifact_id != artifact.artifact_id:
            return ValidationError(
                f"SSOT conflict: Multiple canonical documents for topic '{artifact.topic}'",
                suggestion=f"Mark one as canonical, others as derived. Existing: {existing_canonical.artifact_id}"
            )
    
    if artifact.ssot_relationship == "derived":
        # Check that canonical SSOT is referenced
        if not artifact.dependencies or not has_canonical_reference(artifact.dependencies):
            return ValidationError(
                f"Derived document {artifact.artifact_id} must reference canonical SSOT",
                suggestion="Add canonical SSOT artifact_id to dependencies"
            )
    
    if artifact.ssot_relationship == "implementation":
        # Check that SSOT specification is referenced
        if not artifact.dependencies or not has_ssot_reference(artifact.dependencies):
            return ValidationError(
                f"Implementation {artifact.artifact_id} must reference SSOT specification",
                suggestion="Add SSOT specification artifact_id to dependencies"
            )
    
    return ValidationSuccess()
```

**Enforcement Mode**: 
- FAST LANE phase: Warning only
- Post-MVP phase: Blocking



### 4. Reporting Layer

#### Health Reporter

**Purpose**: Generate domainization health reports

**Report Structure**:
```yaml
report_date: "YYYY-MM-DD"
report_version: "1.0"
enforcement_mode: "soft" | "hard"

summary:
  total_artifacts: int
  registered_artifacts: int
  unregistered_artifacts: int
  registration_percentage: float

domain_coverage:
  - domain_id: string
    domain_name: string
    artifact_count: int
    artifact_types:
      - type: string
        count: int

lifecycle_distribution:
  - artifact_type: string
    states:
      - state: string
        count: int

violations:
  - artifact_id: string
    file_path: string
    violation_type: string
    severity: "critical" | "high" | "medium" | "low"
    description: string
    recommendation: string

recommendations:
  - priority: "high" | "medium" | "low"
    action: string
    rationale: string
```

**Operations**:
- `generate_health_report()` - Create comprehensive health report
- `get_domain_coverage()` - Calculate artifact distribution by domain
- `get_lifecycle_distribution()` - Calculate artifact distribution by lifecycle state
- `detect_violations()` - Identify governance violations
- `generate_recommendations()` - Suggest improvements

**Performance Target**: < 10 seconds for 1000 artifacts

#### Violation Detector

**Purpose**: Identify governance violations

**Detection Rules**:
```python
def detect_violations():
    violations = []
    
    # Unregistered artifacts
    for file in list_all_files():
        if not is_registered(file):
            violations.append(Violation(
                artifact_id=None,
                file_path=file,
                violation_type="unregistered",
                severity="high",
                description="Artifact not registered in domainization system",
                recommendation="Add metadata or register in artifact_registry.yaml"
            ))
    
    # Missing lifecycle status
    for artifact in list_artifacts():
        if not artifact.lifecycle_status:
            violations.append(Violation(
                artifact_id=artifact.artifact_id,
                file_path=artifact.file_path,
                violation_type="missing_lifecycle",
                severity="medium",
                description="Artifact missing lifecycle status",
                recommendation=f"Add lifecycle_status field with valid state for {artifact.artifact_type}"
            ))
    
    # SSOT conflicts
    ssot_topics = {}
    for artifact in list_artifacts_by_relationship("canonical"):
        if artifact.topic in ssot_topics:
            violations.append(Violation(
                artifact_id=artifact.artifact_id,
                file_path=artifact.file_path,
                violation_type="ssot_conflict",
                severity="critical",
                description=f"Multiple canonical SSOTs for topic '{artifact.topic}'",
                recommendation=f"Mark one as canonical, others as derived. Conflicts with: {ssot_topics[artifact.topic]}"
            ))
        ssot_topics[artifact.topic] = artifact.artifact_id
    
    # Deprecated artifacts being modified
    for artifact in list_artifacts_by_lifecycle("deprecated"):
        if artifact.recently_modified():
            violations.append(Violation(
                artifact_id=artifact.artifact_id,
                file_path=artifact.file_path,
                violation_type="deprecated_modification",
                severity="high",
                description="Deprecated artifact was modified",
                recommendation="Only metadata updates allowed for deprecated artifacts"
            ))
    
    return violations
```



## Data Models

### Artifact Metadata Schema

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class ArtifactMetadata:
    artifact_id: str  # Unique identifier (e.g., "system_architecture_md")
    file_path: str  # Relative path from repo root
    primary_domain: str  # Domain ID (e.g., "ARCH")
    artifact_type: str  # Type ID (e.g., "SSOT")
    lifecycle_status: str  # Current state (e.g., "canonical")
    created_date: date  # Creation date
    last_modified: date  # Last modification date
    owner_role: str  # Responsibility description
    ssot_relationship: str  # "canonical" | "derived" | "implementation"
    allowed_writers: List[str]  # Domain IDs with write permission
    allowed_readers: List[str]  # Domain IDs with read permission ("ALL" for public)
    
    # Optional fields
    secondary_domains: Optional[List[str]] = None  # Additional domain associations
    dependencies: Optional[List[str]] = None  # Artifact IDs this depends on
    topic: Optional[str] = None  # Topic for SSOT conflict detection
    
    def validate(self) -> bool:
        """Validate metadata completeness and correctness"""
        required_fields = [
            self.artifact_id, self.file_path, self.primary_domain,
            self.artifact_type, self.lifecycle_status, self.created_date,
            self.last_modified, self.owner_role, self.ssot_relationship,
            self.allowed_writers, self.allowed_readers
        ]
        return all(field is not None for field in required_fields)
    
    def is_modifiable(self) -> bool:
        """Check if artifact can be modified"""
        return self.lifecycle_status != "deprecated"
    
    def can_write(self, domain_id: str) -> bool:
        """Check if domain has write permission"""
        return domain_id in self.allowed_writers
    
    def can_read(self, domain_id: str) -> bool:
        """Check if domain has read permission"""
        return "ALL" in self.allowed_readers or domain_id in self.allowed_readers
```

### Domain Definition Schema

```python
from dataclasses import dataclass
from typing import List

@dataclass
class DomainDefinition:
    domain_id: str  # Unique identifier (e.g., "SIGNALS")
    name: str  # Human-readable name (e.g., "Signal Generation")
    responsibility_scope: str  # What this domain owns
    allowed_artifact_types: List[str]  # Type IDs this domain can own
    cannot_own: List[str]  # Explicit exclusions
    priority: str  # "core" | "surface"
    authority_level: Optional[int] = None  # 1-4 for core reasoning chain
    
    def can_own_type(self, artifact_type: str) -> bool:
        """Check if domain can own artifact type"""
        return artifact_type in self.allowed_artifact_types
    
    def is_core_domain(self) -> bool:
        """Check if this is a core reasoning domain"""
        return self.priority == "core"
    
    def get_authority_level(self) -> int:
        """Get authority level in reasoning chain (lower = higher authority)"""
        return self.authority_level if self.authority_level else 999
```



### Lifecycle State Machine Schema

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class StateTransition:
    from_state: str
    to_state: str
    condition: str  # Human-readable description
    
@dataclass
class StateMachine:
    artifact_type: str
    states: List[str]
    transitions: List[StateTransition]
    
    def is_valid_transition(self, from_state: str, to_state: str) -> bool:
        """Check if transition is allowed"""
        for transition in self.transitions:
            if transition.from_state == from_state and transition.to_state == to_state:
                return True
        return False
    
    def get_allowed_transitions(self, current_state: str) -> List[str]:
        """Get valid next states from current state"""
        return [t.to_state for t in self.transitions if t.from_state == current_state]
    
    def get_initial_state(self) -> str:
        """Get initial state for new artifacts"""
        return self.states[0]

# Predefined state machines
STATE_MACHINES = {
    "SSOT": StateMachine(
        artifact_type="SSOT",
        states=["draft", "review", "canonical", "deprecated"],
        transitions=[
            StateTransition("draft", "review", "Author completes initial version"),
            StateTransition("review", "canonical", "Domain owner approves"),
            StateTransition("canonical", "draft", "Revision required"),
            StateTransition("canonical", "deprecated", "Superseded by new version"),
        ]
    ),
    "ENGINE": StateMachine(
        artifact_type="ENGINE",
        states=["planned", "development", "active", "deprecated"],
        transitions=[
            StateTransition("planned", "development", "Implementation begins"),
            StateTransition("development", "active", "Production ready"),
            StateTransition("development", "development", "Iteration allowed"),
            StateTransition("active", "deprecated", "Replaced by new engine"),
        ]
    ),
    "REPORT_OUT": StateMachine(
        artifact_type="REPORT_OUT",
        states=["generated", "current", "archived"],
        transitions=[
            StateTransition("generated", "current", "Becomes latest version"),
            StateTransition("current", "archived", "Superseded by newer report"),
        ]
    ),
    "DATA_OUT": StateMachine(
        artifact_type="DATA_OUT",
        states=["generated", "current", "archived"],
        transitions=[
            StateTransition("generated", "current", "Becomes latest version"),
            StateTransition("current", "archived", "Superseded by newer data"),
        ]
    ),
    "DATA_IN": StateMachine(
        artifact_type="DATA_IN",
        states=["active", "stale", "archived"],
        transitions=[
            StateTransition("active", "stale", "Data becomes outdated"),
            StateTransition("stale", "archived", "Moved to historical storage"),
        ]
    ),
}
```

### Validation Result Schema

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidationResult:
    success: bool
    gate_name: str
    artifact_id: Optional[str] = None
    error_message: Optional[str] = None
    suggestion: Optional[str] = None
    severity: str = "error"  # "error" | "warning"
    
    @staticmethod
    def success_result(gate_name: str) -> 'ValidationResult':
        return ValidationResult(success=True, gate_name=gate_name)
    
    @staticmethod
    def error_result(gate_name: str, artifact_id: str, error_message: str, suggestion: str) -> 'ValidationResult':
        return ValidationResult(
            success=False,
            gate_name=gate_name,
            artifact_id=artifact_id,
            error_message=error_message,
            suggestion=suggestion,
            severity="error"
        )
    
    @staticmethod
    def warning_result(gate_name: str, artifact_id: str, error_message: str, suggestion: str) -> 'ValidationResult':
        return ValidationResult(
            success=True,  # Warnings don't block
            gate_name=gate_name,
            artifact_id=artifact_id,
            error_message=error_message,
            suggestion=suggestion,
            severity="warning"
        )
```



## Error Handling

### Validation Error Handling

**Principle**: All validation failures must be explainable and actionable

**Error Response Structure**:
```python
@dataclass
class ValidationError:
    gate_name: str  # Which gate failed
    artifact_id: str  # Affected artifact
    error_code: str  # Machine-readable error code
    error_message: str  # Human-readable description
    suggestion: str  # Actionable resolution guidance
    severity: str  # "critical" | "high" | "medium" | "low"
    enforcement_mode: str  # "blocking" | "warning"
```

**Error Codes**:
- `E001`: Artifact not registered
- `E002`: Invalid domain assignment
- `E003`: Invalid lifecycle transition
- `E004`: Domain boundary violation
- `E005`: SSOT conflict detected
- `E006`: Missing required metadata
- `E007`: Deprecated artifact modification
- `E008`: Authority chain violation
- `E009`: Forbidden cloud provider reference
- `E010`: Feature without report value

**Error Handling Strategy**:

1. **FAST LANE Phase** (soft validation):
   - All errors become warnings
   - Commit proceeds with warning log
   - Violations tracked for future enforcement
   - Developer notified but not blocked

2. **Post-MVP Phase** (hard validation):
   - Critical/high severity errors block commit
   - Medium/low severity errors become warnings
   - Clear error messages with resolution steps
   - Link to documentation for complex issues

**Example Error Messages**:

```
❌ Gate 2: Domain Assignment Failed

Artifact: engines/new_feature.py
Error: Domain 'REPORT' cannot own artifact type 'ENGINE'

Suggestion: Valid domains for ENGINE artifacts:
  - SIGNALS (signal generation engines)
  - SEMANTICS (semantic interpretation engines)
  - REASONING (reasoning logic engines)
  - DATA (data processing engines)

Change primary_domain to one of the above domains.

Documentation: .domainization/docs/domain_boundaries.md
```

### Registry Corruption Handling

**Detection**:
- Schema validation on every registry read
- Checksum verification
- Duplicate artifact_id detection
- Orphaned reference detection

**Recovery**:
- Automatic backup before every write
- Rollback to last valid state
- Manual recovery mode with validation
- Health report generation after recovery

**Backup Strategy**:
```
.domainization/backups/
  artifact_registry_YYYY-MM-DD_HH-MM-SS.yaml
  domain_registry_YYYY-MM-DD_HH-MM-SS.yaml
```

### Performance Degradation Handling

**Monitoring**:
- Track commit gate execution time
- Alert if > 5 seconds
- Profile slow operations
- Optimize registry queries

**Mitigation**:
- Cache registry in memory
- Index artifacts by domain and type
- Lazy load artifact metadata
- Parallel gate execution where possible



## Testing Strategy

### Unit Testing

**Registry Layer Tests**:
- Test artifact registration with valid metadata
- Test artifact registration with invalid metadata
- Test artifact retrieval by ID, domain, type, lifecycle
- Test metadata validation
- Test frontmatter parsing
- Test registry YAML serialization/deserialization

**Domain Model Tests**:
- Test domain definition loading
- Test domain validation
- Test artifact type ownership rules
- Test core vs surface domain classification
- Test authority level ordering

**Lifecycle Tests**:
- Test state machine loading
- Test valid transitions
- Test invalid transitions
- Test deprecated artifact modification blocking
- Test initial state assignment

**Validation Gate Tests**:
- Test Gate 1: Registration validation
- Test Gate 2: Domain assignment validation
- Test Gate 3: Lifecycle transition validation
- Test Gate 4: Boundary enforcement validation
- Test Gate 5: SSOT consistency validation
- Test soft vs hard enforcement modes
- Test error message generation

**Test Coverage Target**: > 90% for all components

### Integration Testing

**End-to-End Commit Flow**:
```python
def test_commit_flow_valid_artifact():
    # Setup: Create test artifact with valid metadata
    artifact = create_test_artifact(
        artifact_id="test_engine",
        primary_domain="SIGNALS",
        artifact_type="ENGINE",
        lifecycle_status="development"
    )
    
    # Execute: Run commit gates
    result = run_commit_gates([artifact])
    
    # Assert: All gates pass
    assert result.success == True
    assert len(result.errors) == 0

def test_commit_flow_invalid_domain():
    # Setup: Create artifact with invalid domain assignment
    artifact = create_test_artifact(
        artifact_id="test_report",
        primary_domain="REPORT",  # Invalid for ENGINE type
        artifact_type="ENGINE",
        lifecycle_status="development"
    )
    
    # Execute: Run commit gates
    result = run_commit_gates([artifact])
    
    # Assert: Gate 2 fails
    assert result.success == False
    assert result.failed_gate == "Gate 2: Domain Assignment"
    assert "cannot own artifact type" in result.error_message
```

**Registry Persistence Tests**:
- Test registry save and load
- Test concurrent registry access
- Test registry corruption recovery
- Test backup and restore

**Performance Tests**:
- Test commit gate execution time with 100 artifacts
- Test commit gate execution time with 1000 artifacts
- Test health report generation time
- Test registry query performance

### Acceptance Testing

**Scenario 1: New Developer Adds Feature**
```gherkin
Given a new developer wants to add a signal generation engine
When they create engines/new_signal_engine.py
And they add metadata with primary_domain="SIGNALS"
And they commit the changes
Then all commit gates should pass
And the artifact should be registered
And the health report should show the new artifact
```

**Scenario 2: Invalid Domain Assignment**
```gherkin
Given a developer modifies a report output file
When they change primary_domain from "REPORT" to "SIGNALS"
And they commit the changes
Then Gate 2 should fail
And the commit should be blocked (in hard mode)
And an error message should explain the violation
And the error message should suggest valid domains
```

**Scenario 3: SSOT Conflict**
```gherkin
Given a canonical SSOT document exists for "portfolio_state"
When a developer creates a new document
And marks it as canonical SSOT for "portfolio_state"
And they commit the changes
Then Gate 5 should fail
And the commit should be blocked (in hard mode)
And the error should identify the conflicting documents
```

**Scenario 4: Gradual Migration**
```gherkin
Given the system is in FAST LANE phase
When a developer commits an unregistered artifact
Then commit gates should generate warnings
But the commit should proceed
And the violation should be logged
And the health report should show the unregistered artifact
```



## Implementation Phases

### Phase 1: Foundation (Week 1-2)

**Goal**: Create basic infrastructure without enforcement

**Deliverables**:
1. Create `.domainization/` directory structure
2. Create `domain_registry.yaml` with 12 canonical domains
3. Create `artifact_registry.yaml` template
4. Create `lifecycle_state_machine.yaml` with state machines for all artifact types
5. Create basic Python modules for registry operations

**Success Criteria**:
- Directory structure exists
- Registry files are valid YAML
- Domain definitions are complete
- State machines are defined
- No existing functionality is broken

**Testing**:
- Unit tests for registry loading
- Schema validation tests
- No integration with git yet

### Phase 2: Registration (Week 3-4)

**Goal**: Register existing artifacts without enforcement

**Deliverables**:
1. Add YAML frontmatter to all markdown files in `docs/`
2. Register all Python engines in artifact registry
3. Register all report outputs
4. Register all data files
5. Create registration helper scripts

**Success Criteria**:
- All SSOT documents have frontmatter
- All engines are registered
- All outputs are registered
- Health report shows 100% registration
- No existing functionality is broken

**Testing**:
- Validate all frontmatter
- Validate all registry entries
- Generate first health report

### Phase 3: Soft Validation (Week 5-6)

**Goal**: Implement commit gates in warning mode

**Deliverables**:
1. Implement all 5 commit gates
2. Create pre-commit hook script
3. Configure gates for soft validation (warnings only)
4. Create validation result logging
5. Create developer documentation

**Success Criteria**:
- All gates execute on commit
- Violations generate warnings
- Commits proceed regardless of violations
- Warnings are logged
- Developers receive actionable feedback

**Testing**:
- Test each gate independently
- Test gate execution order
- Test warning message clarity
- Test performance (< 5 seconds)



### Phase 4: Report MVP Stabilization (Week 7-10)

**Goal**: Focus on report quality while monitoring violations

**Deliverables**:
1. Continue soft validation
2. Generate weekly health reports
3. Track violation trends
4. Fix high-priority violations
5. Improve report quality (primary focus)

**Success Criteria**:
- Report quality improvements delivered
- Violation count decreasing
- No new critical violations
- Health reports show progress
- Domainization does not block report work

**Testing**:
- Monitor gate execution time
- Track violation resolution rate
- Validate report improvements

### Phase 5: Hard Enforcement (Week 11-12)

**Goal**: Enable blocking validation for critical violations

**Deliverables**:
1. Switch critical violations to blocking mode
2. Keep medium/low violations as warnings
3. Update developer documentation
4. Create violation resolution guides
5. Implement emergency bypass mechanism

**Success Criteria**:
- Critical violations block commits
- Clear error messages guide resolution
- Emergency bypass available for urgent fixes
- No false positives blocking valid work
- Developer satisfaction maintained

**Testing**:
- Test blocking behavior
- Test error message clarity
- Test bypass mechanism
- Test developer workflow impact

### Phase 6: Monitoring and Optimization (Week 13+)

**Goal**: Continuous improvement and monitoring

**Deliverables**:
1. Automated health report generation
2. Violation trend analysis
3. Performance optimization
4. Documentation updates
5. Developer training materials

**Success Criteria**:
- Health reports generated automatically
- Performance < 5 seconds for all operations
- Zero critical violations
- Developer adoption > 90%
- System maintainability high

**Testing**:
- Performance benchmarks
- User satisfaction surveys
- Violation resolution time tracking

## Migration Strategy

### Backward Compatibility

**Principle**: Existing functionality must continue working

**Guarantees**:
1. No file moves during initial phases
2. No forced metadata addition
3. No breaking changes to existing scripts
4. Gradual enforcement rollout
5. Clear migration path for each artifact

### Rollback Plan

**Triggers**:
- Critical functionality broken
- Developer productivity significantly impacted
- Performance degradation > 10 seconds
- False positive rate > 10%

**Rollback Steps**:
1. Disable commit gates
2. Restore previous registry state from backup
3. Document issues encountered
4. Fix issues in development environment
5. Re-enable with fixes

**Prevention**:
- Comprehensive testing before each phase
- Gradual rollout with monitoring
- Developer feedback loops
- Emergency bypass mechanism



## Security Considerations

### Access Control

**Registry Modification**:
- Only domain owners can modify domain definitions
- Only artifact owners can modify artifact metadata
- Registry changes require code review
- Backup before every modification

**Commit Gate Bypass**:
- Emergency bypass requires explicit flag
- Bypass usage is logged
- Bypass requires justification
- Bypass is audited in health reports

### Data Integrity

**Registry Integrity**:
- Schema validation on every read/write
- Checksum verification
- Duplicate detection
- Orphaned reference detection
- Automatic backup before changes

**Metadata Integrity**:
- Required field validation
- Type checking
- Reference validation (domain IDs, artifact IDs)
- Lifecycle state validation

### Audit Trail

**Tracked Events**:
- Artifact registration
- Metadata changes
- Lifecycle transitions
- Validation failures
- Bypass usage
- Registry modifications

**Audit Log Format**:
```yaml
timestamp: "YYYY-MM-DD HH:MM:SS"
event_type: "artifact_registered" | "metadata_changed" | "validation_failed" | "bypass_used"
artifact_id: string
user: string
details: object
```

## Performance Optimization

### Registry Caching

**Strategy**:
- Load registry into memory on first access
- Cache for duration of commit gate execution
- Invalidate cache on registry modification
- Index by artifact_id, domain_id, artifact_type

**Implementation**:
```python
class RegistryCache:
    def __init__(self):
        self._cache = None
        self._last_modified = None
    
    def get_registry(self):
        current_modified = get_file_modified_time("artifact_registry.yaml")
        if self._cache is None or current_modified > self._last_modified:
            self._cache = load_registry()
            self._last_modified = current_modified
        return self._cache
    
    def invalidate(self):
        self._cache = None
```

### Parallel Gate Execution

**Strategy**:
- Gates 1-3 can run in parallel (independent)
- Gates 4-5 depend on registry state
- Use thread pool for parallel execution
- Aggregate results

**Performance Target**:
- Single artifact validation: < 100ms
- 10 artifacts: < 500ms
- 100 artifacts: < 2 seconds
- 1000 artifacts: < 5 seconds

### Query Optimization

**Indexes**:
- artifact_id → artifact (primary key)
- domain_id → list[artifact]
- artifact_type → list[artifact]
- lifecycle_status → list[artifact]
- topic → list[artifact] (for SSOT conflict detection)

**Query Patterns**:
```python
# Optimized queries
def get_artifacts_by_domain(domain_id: str) -> List[Artifact]:
    return domain_index[domain_id]

def get_canonical_ssot_by_topic(topic: str) -> Optional[Artifact]:
    candidates = topic_index[topic]
    return next((a for a in candidates if a.ssot_relationship == "canonical"), None)
```

## Monitoring and Observability

### Metrics

**System Metrics**:
- Total artifacts registered
- Artifacts by domain
- Artifacts by type
- Artifacts by lifecycle state
- Violation count by type
- Violation count by severity

**Performance Metrics**:
- Commit gate execution time (p50, p95, p99)
- Health report generation time
- Registry query time
- Cache hit rate

**Quality Metrics**:
- Registration coverage percentage
- Violation resolution rate
- Time to resolve violations
- False positive rate

### Dashboards

**Health Dashboard**:
- Registration coverage over time
- Violation trends
- Domain coverage
- Lifecycle distribution

**Performance Dashboard**:
- Gate execution time trends
- Query performance
- Cache effectiveness

**Developer Dashboard**:
- My artifacts
- My violations
- My domain's health
- Recent changes



## Technology Stack

### Core Technologies

**Language**: Python 3.9+
- Chosen for consistency with existing Portfolio OS codebase
- Rich ecosystem for YAML parsing and validation
- Good performance for file system operations

**Data Format**: YAML
- Human-readable and editable
- Good support for comments and documentation
- Native Python support via PyYAML

**Git Integration**: Pre-commit hooks
- Standard git hook mechanism
- Runs automatically on commit
- Can be bypassed in emergencies

### Dependencies

**Required**:
- `PyYAML` - YAML parsing and serialization
- `pydantic` - Data validation and schema enforcement
- `pathlib` - File system operations
- `dataclasses` - Data structure definitions

**Optional**:
- `pytest` - Testing framework
- `pytest-cov` - Code coverage
- `black` - Code formatting
- `mypy` - Type checking

### File Structure

```
.domainization/
├── artifact_registry.yaml          # Central artifact index
├── domain_registry.yaml            # Domain definitions
├── lifecycle_state_machine.yaml    # State machine definitions
├── config.yaml                     # System configuration
├── backups/                        # Registry backups
│   ├── artifact_registry_*.yaml
│   └── domain_registry_*.yaml
├── logs/                           # Audit logs
│   ├── validation_*.log
│   └── audit_*.log
├── reports/                        # Health reports
│   └── health_report_*.yaml
├── hooks/                          # Git hooks
│   └── pre-commit
└── src/                            # Python implementation
    ├── __init__.py
    ├── registry.py                 # Registry operations
    ├── domain.py                   # Domain model
    ├── lifecycle.py                # Lifecycle management
    ├── validators.py               # Commit gate validators
    ├── reporter.py                 # Health reporting
    ├── cache.py                    # Performance caching
    └── cli.py                      # Command-line interface
```

## Command-Line Interface

### Registry Management

```bash
# Register a new artifact
domainization register <file_path> --domain SIGNALS --type ENGINE --lifecycle development

# Update artifact metadata
domainization update <artifact_id> --lifecycle active

# List artifacts
domainization list --domain SIGNALS
domainization list --type ENGINE
domainization list --lifecycle canonical

# Show artifact details
domainization show <artifact_id>
```

### Validation

```bash
# Validate current repository state
domainization validate

# Validate specific files
domainization validate <file_path>...

# Run specific gate
domainization validate --gate 2

# Dry run (show what would happen)
domainization validate --dry-run
```

### Health Reporting

```bash
# Generate health report
domainization health

# Generate health report for specific domain
domainization health --domain SIGNALS

# Export health report
domainization health --output health_report.yaml

# Show violations only
domainization health --violations-only
```

### Configuration

```bash
# Show current configuration
domainization config show

# Set enforcement mode
domainization config set enforcement_mode soft
domainization config set enforcement_mode hard

# Enable/disable specific gate
domainization config set gate_1_enabled false
```

## Documentation Requirements

### Developer Documentation

**Getting Started Guide**:
- What is domainization?
- Why do we need it?
- How does it affect my workflow?
- Quick start tutorial

**Domain Guide**:
- List of all domains
- Responsibilities of each domain
- What each domain can and cannot own
- Authority chain explanation

**Artifact Type Guide**:
- List of all artifact types
- Lifecycle states for each type
- When to use each type
- Examples

**Metadata Guide**:
- Required fields
- Optional fields
- How to add frontmatter
- How to register in artifact_registry.yaml

**Troubleshooting Guide**:
- Common validation errors
- How to resolve each error
- When to use bypass
- Who to contact for help

### Architecture Documentation

**System Architecture**:
- Component diagram
- Data flow diagram
- Authority chain diagram
- Integration points

**Design Decisions**:
- Why YAML for registry?
- Why pre-commit hooks?
- Why soft validation first?
- Why 12 domains?

**Extension Guide**:
- How to add a new domain
- How to add a new artifact type
- How to add a new validation gate
- How to modify state machines



## Design Decisions and Rationale

### Why 12 Domains?

**Decision**: Use 12 canonical domains instead of fewer or more

**Rationale**:
- Splits LOGIC into SIGNALS, SEMANTICS, REASONING for clear authority chain
- Separates concerns at the right granularity
- Not too few (would mix responsibilities)
- Not too many (would create confusion)
- Aligns with Portfolio OS architecture philosophy

**Alternatives Considered**:
- 5 domains (too coarse, mixes concerns)
- 20+ domains (too fine, creates overhead)

### Why Soft Validation First?

**Decision**: Start with warnings, move to blocking later

**Rationale**:
- Avoids blocking report development (primary goal)
- Allows gradual adoption
- Builds developer trust
- Identifies false positives before enforcement
- Aligns with FAST LANE REPORT MVP priority

**Alternatives Considered**:
- Hard enforcement from day 1 (would block report work)
- No enforcement (would not prevent violations)

### Why YAML for Registry?

**Decision**: Use YAML files instead of database

**Rationale**:
- Human-readable and editable
- Version controlled with code
- No external dependencies
- Easy to backup and restore
- Supports comments for documentation
- Sufficient performance for expected scale

**Alternatives Considered**:
- SQLite database (overkill for scale, not version controlled)
- JSON (less readable, no comments)
- Custom format (reinventing the wheel)

### Why Pre-commit Hooks?

**Decision**: Use git pre-commit hooks for validation

**Rationale**:
- Runs automatically on every commit
- Standard git mechanism
- Can be bypassed in emergencies
- Provides immediate feedback
- No CI/CD dependency

**Alternatives Considered**:
- CI/CD validation (too late, commit already made)
- Manual validation (not enforced)
- IDE integration (not universal)

### Why Authority Chains?

**Decision**: Model runtime flows as authority chains, not just data flows

**Rationale**:
- Clarifies who can create meaning
- Prevents semantic confusion
- Enforces architectural principles
- Aligns with Portfolio OS philosophy
- Makes violations more obvious

**Alternatives Considered**:
- Pure data flow model (misses authority concept)
- No flow validation (allows violations)

### Why Gradual Migration?

**Decision**: Implement in 6 phases over 13+ weeks

**Rationale**:
- Minimizes risk of breaking existing functionality
- Allows learning and adjustment
- Builds developer confidence
- Prioritizes report value over governance
- Provides rollback points

**Alternatives Considered**:
- Big bang migration (too risky)
- No migration plan (chaotic)

## Future Enhancements

### Phase 7+: Advanced Features

**Automated Artifact Discovery**:
- Scan repository for unregistered files
- Suggest domain assignments based on file path and content
- Auto-generate metadata templates

**Dependency Graph Visualization**:
- Visualize artifact dependencies
- Show authority chain flows
- Identify circular dependencies
- Generate architecture diagrams

**Advanced Analytics**:
- Artifact churn rate by domain
- Lifecycle transition patterns
- Violation hotspots
- Domain health scores

**Integration with CI/CD**:
- Automated health reports on PR
- Violation trends in PR comments
- Block PR merge on critical violations
- Automated artifact registration

**Machine Learning Enhancements**:
- Predict domain assignment from file content
- Suggest lifecycle transitions
- Detect anomalous patterns
- Recommend artifact refactoring

### Long-term Vision

**Domain-Organized Repository**:
- Migrate to `domains/` folder structure
- Physical organization matches logical organization
- Easier navigation and discovery
- Clear ownership boundaries

**Runtime Flow Enforcement**:
- Validate flows at runtime, not just commit time
- Block forbidden authority chain violations
- Trace signal-to-report chains
- Generate flow diagrams

**Multi-Repository Support**:
- Extend domainization to multiple repositories
- Shared domain registry
- Cross-repository dependencies
- Federated governance

## Conclusion

The domainization system provides Portfolio OS with a robust artifact governance framework that:

1. **Prioritizes Report Value**: Soft validation during FAST LANE phase ensures governance supports rather than blocks report development

2. **Enforces Authority Chains**: Runtime flows represent who can create meaning, preventing semantic confusion

3. **Enables Gradual Adoption**: 6-phase implementation minimizes risk and builds developer confidence

4. **Maintains Explainability**: All validation failures provide actionable guidance

5. **Scales Appropriately**: Designed for 1000+ artifacts with < 5 second validation time

6. **Preserves Flexibility**: Emergency bypass and rollback mechanisms prevent governance from becoming a blocker

The design balances governance rigor with development velocity, ensuring that domainization enhances rather than hinders Portfolio OS evolution.
