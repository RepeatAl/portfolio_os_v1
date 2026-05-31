# Deployment Authority and Domain Lifecycle — Delta Layer Documentation

## Overview

This is a lean delta layer extending governance-runtime-enforcement, not a framework expansion.

The delta layer addresses four structural gaps at the meta-governance level without redefining existing enforcement semantics, fail modes, or provenance systems:

1. **Governance Influence Graph** — Static dependency declarations + cycle detection to prevent governance feedback loops
2. **Deployment Authority Model** — OWNER/CI/RUNTIME role partitioning with topology constraint enforcement
3. **Transition Cooldown** — 4h default anti-flapping guard for enforcement mode transitions
4. **Domain Lifecycle** — Three-state model (active/deprecated/archived) with deprecation-triggered artifact reassignment

**Principle**: No framework escalation. No plugin system. No event bus. No runtime kernel. Simple linear initialization, not an architecture.

---

## Modules

### 1. Influence Graph (`governance/influence_graph.py`)

**Purpose**: Manages governance module dependency declarations, cycle detection, and directionality enforcement. Prevents circular governance influence paths that could amplify or oscillate decisions.

**Key Classes**:

| Class | Type | Description |
|-------|------|-------------|
| `InfluenceDirection` | StrEnum | `upstream` or `downstream` |
| `ModuleDependencyDeclaration` | frozen dataclass | Immutable declaration: module_id, read_dependencies, write_dependencies, influence_direction |
| `CycleDetectionResult` | dataclass | has_cycle (bool), cycle_path (list of module IDs) |
| `DirectionalityViolation` | dataclass | violating_module, target_module, violator_direction, target_direction, reason |
| `GovernanceInfluenceGraph` | class | Main orchestrator: load, validate, detect cycles, enforce directionality |

**Public Interfaces**:

```python
from governance.influence_graph import GovernanceInfluenceGraph

graph = GovernanceInfluenceGraph(
    declarations_path=".domainization/governance_influence_declarations.yaml",
    ledger=ledger,  # Optional MutationAuditLedger
)

# Full validation at init (load → build graph → detect cycles → enforce directionality)
is_valid, errors = graph.validate_at_init()

# Individual operations
declarations = graph.load_declarations()
is_valid = graph.validate_declaration(decl)
adjacency = graph.build_graph()
cycle_result = graph.detect_cycles()
violations = graph.enforce_directionality()
```

**Serialization**:

```python
from governance.influence_graph import ModuleDependencyDeclaration, InfluenceDirection

decl = ModuleDependencyDeclaration(
    module_id="deployment_authority",
    read_dependencies=("policy_versioner",),
    write_dependencies=("mutation_audit_ledger",),
    influence_direction=InfluenceDirection.DOWNSTREAM,
)
d = decl.to_dict()
restored = ModuleDependencyDeclaration.from_dict(d)
assert decl == restored
```

**Fail Mode**: `fail_closed` — Cannot proceed with circular governance. Halts init on cycles or missing declarations.

---

### 2. Deployment Authority (`governance/deployment_authority.py`)

**Purpose**: Defines the minimal OWNER/CI/RUNTIME authority model, enforces topology constraints (forbidden authority pairs), and records deploy provenance to the audit ledger.

**Key Classes**:

| Class | Type | Description |
|-------|------|-------------|
| `AuthorityRole` | StrEnum | `OWNER`, `CI`, `RUNTIME` |
| `Authority` | StrEnum | 6 authorities: mutate_governance, change_enforcement_mode, deploy, accept_runtime_hash, execute_override, change_fail_mode |
| `AuthorityAssignment` | frozen dataclass | role + frozenset of authorities |
| `DeployProvenance` | dataclass | Structured deployment event record |
| `DeploymentAuthorityModel` | class | Load model, validate topology, check authority, record provenance |

**Public Interfaces**:

```python
from governance.deployment_authority import (
    DeploymentAuthorityModel,
    DeployProvenance,
    AuthorityRole,
    Authority,
    FORBIDDEN_AUTHORITY_PAIRS,
)

model = DeploymentAuthorityModel(
    model_path=".domainization/deployment_authority_model.yaml",
    ledger=ledger,  # Optional MutationAuditLedger
)

# Full validation at init
is_valid, errors = model.validate_at_init()

# Check if a role holds a specific authority
can_deploy = model.check_authority(AuthorityRole.CI, Authority.DEPLOY)  # True

# Record deploy provenance
provenance = DeployProvenance(
    deploy_id="uuid-here",
    timestamp="2026-06-01T14:00:00Z",
    actor_role=AuthorityRole.CI,
    authority_used=Authority.DEPLOY,
    is_validated=True,
    runtime_hash="sha256:abc123...",
    details={"ci_workflow_run_id": "12345"},
)
model.record_deploy_provenance(provenance)
```

**Fail Mode**: `fail_closed` — Cannot proceed with topology violation. Halts init on forbidden pair detection.

---

### 3. Transition Cooldown (`governance/transition_cooldown.py`)

**Purpose**: Anti-flapping guard for enforcement mode transitions. Enforces a configurable cooldown period between transitions. Emergency overrides bypass cooldown with mandatory audit logging.

**Key Classes**:

| Class | Type | Description |
|-------|------|-------------|
| `CooldownConfig` | dataclass | duration_hours (float, clamped [1.0, 24.0], default 4.0) |
| `CooldownState` | dataclass | is_active, last_transition_time, cooldown_expires_at, remaining_seconds |
| `TransitionAttempt` | dataclass | Full record of a transition attempt with result |
| `TransitionCooldown` | class | Load config, check state, attempt transitions, query history |

**Public Interfaces**:

```python
from governance.transition_cooldown import TransitionCooldown

cooldown = TransitionCooldown(
    config_path=".domainization/config.yaml",
    ledger=ledger,  # Optional MutationAuditLedger
)

# Check current cooldown state
state = cooldown.get_cooldown_state()
if state.is_active:
    print(f"Cooldown active, {state.remaining:.0f}s remaining")

# Attempt a transition
attempt = cooldown.attempt_transition(
    from_mode="observability",
    to_mode="soft",
    actor=actor_identity,
)
if attempt.result == "accepted":
    # Transition allowed
    ...
elif attempt.result == "rejected_cooldown":
    # Cooldown active, transition blocked
    ...

# Emergency override (bypasses cooldown)
attempt = cooldown.attempt_transition(
    from_mode="hard",
    to_mode="soft",
    actor=actor_identity,
    is_emergency=True,
    bypass_reason="Critical false positive blocking production pipeline",
)
# attempt.result == "accepted_emergency"

# Query full transition history
history = cooldown.query_transition_history()
```

**Fail Mode**: `fail_soft` — If cooldown state is unreadable, degrades gracefully.

---

### 4. Domain Lifecycle (`governance/domain_lifecycle.py`)

**Purpose**: Manages domain lifecycle states (active/deprecated/archived) and handles deprecation-triggered artifact reassignment planning and execution.

**Key Classes**:

| Class | Type | Description |
|-------|------|-------------|
| `DomainLifecycleState` | StrEnum | `active`, `deprecated`, `archived` |
| `DeprecationRequest` | dataclass | domain_id, reassignment_target, reason, requested_by, timestamp |
| `ReassignmentPlanEntry` | dataclass | artifact_id, artifact_type, previous_domain, new_domain |
| `ReassignmentPlan` | dataclass | Full plan with entries, blocked_types, is_valid |
| `DomainLifecycleManager` | class | State queries, transition validation, deprecation, reassignment |

**Valid Transitions** (defined in `VALID_DOMAIN_TRANSITIONS`):

| From | To | Description |
|------|----|-------------|
| active | deprecated | Deprecation request (requires reassignment_target) |
| deprecated | archived | All artifacts reassigned (terminal) |
| deprecated | active | Reactivation |
| archived | — | Terminal state, no transitions out |

**Public Interfaces**:

```python
from governance.domain_lifecycle import (
    DomainLifecycleManager,
    DomainLifecycleState,
    DeprecationRequest,
)

manager = DomainLifecycleManager(
    domain_registry_path=".domainization/domain_registry.yaml",
    artifact_registry_path=".domainization/artifact_registry.yaml",
    ledger=ledger,  # Optional MutationAuditLedger
)

# Get domain state (defaults to ACTIVE for unknown domains)
state = manager.get_domain_state("GOV")  # DomainLifecycleState.ACTIVE

# Validate a transition
is_valid, reason = manager.validate_transition("GOV", DomainLifecycleState.DEPRECATED)

# Request deprecation (produces reassignment plan)
request = DeprecationRequest(
    domain_id="MEMORY",
    reassignment_target="STATE",
    reason="Memory domain consolidated into State domain",
    requested_by="rabieb",
    timestamp="2026-06-01T18:00:00Z",
)
success, result = manager.request_deprecation(request)
if success:
    plan = result  # ReassignmentPlan for OWNER approval
    manager.execute_reassignment(plan, actor_identity)

# Non-deprecation transition
success, message = manager.transition_domain(
    domain_id="MEMORY",
    to_state=DomainLifecycleState.ARCHIVED,
    actor=actor_identity,
)
```

**Fail Mode**: `fail_soft` — If domain registry is unreadable, skip lifecycle checks with WARNING.

---

## Data Files

### Governance Influence Declarations (`.domainization/governance_influence_declarations.yaml`)

**Purpose**: Static dependency declarations for all governance modules. Consumed by the InfluenceGraph at initialization to build the directed dependency graph and perform cycle/directionality validation.

**Schema**:

```yaml
schema_version: "1.0.0"
modules:
  - module_id: "<string>"           # Unique module identifier
    read_dependencies: [<string>]   # Modules whose output this module consumes
    write_dependencies: [<string>]  # Modules whose state this module modifies
    influence_direction: "<upstream|downstream>"
```

**Current declarations**: 13 modules (influence_graph, deployment_authority, transition_cooldown, domain_lifecycle, gate_framework, lifecycle_enforcer, boundary_enforcer, warning_governor, mutation_audit_ledger, policy_versioner, fail_mode_registry, state_provenance_tagger, shadow_authority_detector).

---

### Deployment Authority Model (`.domainization/deployment_authority_model.yaml`)

**Purpose**: Defines the three-role authority model with explicit authority assignments and forbidden pairs. Consumed by DeploymentAuthorityModel at initialization for topology constraint validation.

**Schema**:

```yaml
schema_version: "1.0.0"
roles:
  - role_id: "<OWNER|CI|RUNTIME>"
    description: "<string>"
    authorities:
      - "<authority_name>"

forbidden_pairs:
  - pair: ["<authority_a>", "<authority_b>"]
    rationale: "<string>"
```

**Current role assignments**:

| Role | Authorities |
|------|-------------|
| OWNER | mutate_governance, change_enforcement_mode |
| CI | deploy, accept_runtime_hash |
| RUNTIME | execute_override, change_fail_mode |

---

## CTO Decision: Forbidden Authority Pairs (2026-05-31)

The final `FORBIDDEN_AUTHORITY_PAIRS` set is **additive and stricter**. No silent deviations are permitted.

**Final forbidden-pair set (3 pairs)**:

| # | Pair | Rationale |
|---|------|-----------|
| 1 | `(mutate_governance, deploy)` | OWNER cannot deploy — prevents single actor from both mutating governance and deploying |
| 2 | `(deploy, change_enforcement_mode)` | CI cannot change enforcement mode — prevents deployer from altering the rules it enforces |
| 3 | `(change_enforcement_mode, execute_override)` | Mode change and override must be separate actors — prevents enforcement bypass |

**Resolution**: The implementation keeps the original pair AND adds the design-spec pair. This is an additive decision — no pair was removed, no deviation was silently normalized.

---

## Initialization Sequence

The delta layer initializes in strict linear order via `governance/delta_init.py`:

```
1. InfluenceGraph       (CRITICAL — halts on cycles or missing declarations)
2. DeploymentAuthority  (CRITICAL — halts on topology violations)
3. TransitionCooldown   (fail_soft — degrades gracefully on config errors)
4. DomainLifecycleManager (fail_soft — degrades gracefully on registry errors)
```

If a CRITICAL component fails, initialization halts immediately and subsequent components are NOT loaded. fail_soft components that encounter errors log warnings and return None, but do not halt init.


**Usage**:

```python
from governance.delta_init import initialize_delta_layer

result = initialize_delta_layer(
    declarations_path=".domainization/governance_influence_declarations.yaml",
    authority_model_path=".domainization/deployment_authority_model.yaml",
    config_path=".domainization/config.yaml",
    domain_registry_path=".domainization/domain_registry.yaml",
    artifact_registry_path=".domainization/artifact_registry.yaml",
    ledger=ledger,  # Optional MutationAuditLedger
)

if result.success:
    # All CRITICAL components passed
    graph = result.influence_graph
    authority = result.deployment_authority
    cooldown = result.transition_cooldown  # May be None if degraded
    lifecycle = result.domain_lifecycle    # May be None if degraded
else:
    # CRITICAL failure — check result.errors
    for error in result.errors:
        print(f"CRITICAL: {error}")
```

---

## Integration with Existing Infrastructure

The delta layer consumes existing governance-runtime-enforcement infrastructure in **read-only** mode. No existing modules are modified.

| Existing Component | Delta Layer Interaction | Modification |
|---|---|---|
| `Mutation_Audit_Ledger` | Append new event types | Schema unchanged, additive event types only |
| `Actor_Identity` | Consumed (read-only) | No modification |
| `Policy_Versioner` | Consumed (read-only) | No modification |
| `Fail_Mode_Registry` | Not touched | No modification |
| `Domain_Registry` | Add `lifecycle_state` field | Additive field only, no schema break |
| `config.yaml` | Add `transition_hysteresis` section | Additive section only |

### New Ledger Event Types (additive only)

| Event Type | Source Module | Description |
|-----------|--------------|-------------|
| `deployment_authorized` | Deployment Authority | Deploy provenance record |
| `enforcement_mode_rollback` | Transition Cooldown | Mode transition attempt (success or rejected) |
| `domain_lifecycle_transition` | Domain Lifecycle | Domain state change or artifact reassignment |

---

## Transition Hysteresis Configuration

Located in `.domainization/config.yaml` under the `transition_hysteresis` section:

```yaml
transition_hysteresis:
  cooldown_hours: 4  # Default: 4.0 | Min: 1.0 | Max: 24.0
```

**Clamping behavior**:
- Values below 1.0 are clamped to 1.0 with a WARNING log
- Values above 24.0 are clamped to 24.0 with a WARNING log
- Missing section defaults to 4.0 hours
- Invalid values (non-numeric) default to 4.0 hours

---

## Requirements Traceability

| Module | Requirement IDs |
|--------|----------------|
| `governance/influence_graph.py` | 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3 |
| `governance/deployment_authority.py` | 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4 |
| `governance/transition_cooldown.py` | 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4 |
| `governance/domain_lifecycle.py` | 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5 |
| `governance/delta_init.py` | 2.4, 4.4, 5.4, 11.5 |
| `.domainization/governance_influence_declarations.yaml` | 1.1, 1.4 |
| `.domainization/deployment_authority_model.yaml` | 4.1, 4.2, 4.3 |
| Non-interference guarantee | 11.1, 11.2, 11.3, 11.4, 11.5 |
| Property-based test coverage | 12.1, 12.2, 12.3, 12.4, 12.5 |

---

## Test Coverage

### Property-Based Tests (Hypothesis, max_examples=200)

| File | Properties | Validates |
|------|:----------:|-----------|
| `tests/test_influence_graph_properties.py` | 8 | Req 1.4, 1.5, 2.1, 2.2, 2.3, 2.5, 3.1, 3.2, 3.4 |
| `tests/test_deployment_authority_properties.py` | 10 | Req 4.3, 4.5, 5.1, 5.2, 5.3, 6.1, 6.5 |
| `tests/test_transition_cooldown_properties.py` | 10 | Req 7.1, 7.2, 7.3, 7.5 |
| `tests/test_domain_lifecycle_properties.py` | 6 | Req 9.2, 9.3, 9.4 |

### Unit Tests

| File | Tests | Coverage |
|------|:-----:|----------|
| `tests/test_influence_graph.py` | 14 | YAML loading, missing fields, validation |
| `tests/test_deployment_authority.py` | 22 | YAML loading, topology, provenance, 3-pair enforcement |
| `tests/test_transition_cooldown.py` | 20 | Config clamping, cooldown rejection, history |
| `tests/test_domain_lifecycle.py` | 22 | Default state, deprecation, reassignment, transitions |

### Integration and Non-Interference

| File | Tests | Coverage |
|------|:-----:|----------|
| `tests/test_delta_init.py` | 12 | Initialization sequence, CRITICAL halts, fail_soft degradation |
| `tests/test_delta_non_interference.py` | 32 | Enforcement modes unchanged, no new fail modes, schema additive-only |

---

## Verification

Final verification gate passed with 494 tests (0 failures, 0 regressions).

**Artifact**: `.domainization/reports/final_verification_gate_task6.md`
