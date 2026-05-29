# Requirements Document

## Introduction

This specification extends governance-runtime-enforcement WITHOUT redefining existing enforcement semantics.

This is a **Narrow Delta Spec** — a lean Infrastructure Hardening Delta Layer that addresses genuine structural gaps at the META-GOVERNANCE level. It does NOT:
- Define new enforcement modes (observability/soft/hard already exist in governance-runtime-enforcement)
- Define new fail modes (fail_open/fail_soft/fail_closed already exist in governance-runtime-enforcement)
- Define new provenance systems (governance state provenance already exists in governance-runtime-enforcement Req 41)
- Override existing runtime contracts defined in governance-runtime-enforcement Requirements 1–49
- Duplicate any requirement from governance-runtime-enforcement

**Scope Calibration:** MoneyHorst is a Financial Intelligence Compiler. The governance layer protects correctness, determinism, auditability, and deployment safety — but it is NOT the product. This spec is intentionally minimal. Advanced governance machinery (authority inheritance, domain merge/split, complex transition quorums) is deferred to a future backlog and will only be revisited when team scale or regulatory requirements demand it.

The four areas addressed (in lean form) are:
1. **Governance Circular Influence Protection** — Dependency declaration, cycle detection, and directionality enforcement
2. **Minimal Deployment Authority** — OWNER/CI/RUNTIME authority model with topology constraint and deploy provenance
3. **Simple Enforcement Stability** — Anti-flapping cooldown and rollback logging
4. **Minimal Domain Lifecycle** — Three states (active, deprecated, archived) with deprecation reassignment rules

## Glossary

- **Governance_Influence_Graph**: A directed graph where nodes are governance modules and edges represent read/write dependencies or governance influence direction between modules
- **Circular_Influence**: A condition where governance module A influences module B which influences module A (directly or transitively), creating a feedback loop that can amplify or oscillate governance decisions
- **Influence_Direction**: The declared direction of governance effect between two modules; one of `upstream` (affects modules that consume this module's output) or `downstream` (affects modules whose output this module consumes)
- **Deployment_Authority_Model**: A minimal authority model defining three actor roles (OWNER, CI, RUNTIME) with explicit authority partitioning
- **Authority_Role**: One of three deployment actor classifications: `OWNER` (human operator with full governance mutation rights), `CI` (automated pipeline with deploy and validation rights), `RUNTIME` (execution process with hash acceptance and fail-mode rights)
- **Deploy_Provenance**: A structured record linking a deployment event to the CI run, actor, and policy version that authorized it
- **Transition_Cooldown**: A minimum elapsed time after an enforcement mode transition during which no further transitions are permitted, preventing mode oscillation
- **Domain_Lifecycle_State**: A lifecycle classification for domains themselves (not artifacts); one of `active`, `deprecated`, `archived`
- **Domain_Deprecation**: The process of marking a domain as deprecated, triggering artifact reassignment planning for artifacts owned by that domain

## Requirements

### Requirement 1: Governance Module Dependency Declaration

**User Story:** As a system architect, I want governance modules to declare their read dependencies, write dependencies, and governance influence direction, so that circular influence paths can be detected statically.

#### Acceptance Criteria

1. THE Governance_Influence_Graph SHALL require each governance module to declare: read dependencies (modules whose output it consumes), write dependencies (modules whose state it modifies), and Influence_Direction (upstream or downstream)
2. WHEN a governance module is loaded, THE Governance_Influence_Graph SHALL validate that the module's dependency declaration exists and contains all required fields
3. IF a governance module lacks a dependency declaration, THEN THE Governance_Influence_Graph SHALL emit a CRITICAL severity event and exclude the module from influence analysis
4. THE dependency declarations SHALL be persisted in a structured YAML file (`.domainization/governance_influence_declarations.yaml`) separate from source code
5. FOR ALL governance modules with dependency declarations, serializing then deserializing the declaration SHALL produce an equivalent object (round-trip property)

### Requirement 2: Circular Governance Influence Detection

**User Story:** As a system architect, I want circular governance influence paths to be detected and rejected, so that governance feedback loops cannot amplify or oscillate decisions.

#### Acceptance Criteria

1. WHEN the Governance_Influence_Graph is constructed from module declarations, THE Governance_Influence_Graph SHALL perform cycle detection on the directed dependency graph
2. IF a cycle is detected in the Governance_Influence_Graph, THEN THE Governance_Influence_Graph SHALL reject the cyclic path and emit a CRITICAL severity event containing the full cycle path (module A → module B → ... → module A)
3. THE cycle detection SHALL operate on the transitive closure of influence edges, detecting indirect cycles (A→B→C→A) as well as direct cycles (A→B→A)
4. THE Governance_Influence_Graph SHALL perform cycle detection at governance initialization (before any enforcement decisions are made)
5. FOR ALL acyclic governance influence graphs, adding any single edge that creates a cycle SHALL be detected and rejected (cycle detection completeness property)

### Requirement 3: Governance Influence Directionality Enforcement

**User Story:** As a system architect, I want governance influence direction to be enforced, so that downstream modules cannot influence upstream modules and create hidden feedback paths.

#### Acceptance Criteria

1. THE Governance_Influence_Graph SHALL enforce that influence edges respect declared Influence_Direction: a module declared as `downstream` SHALL NOT write to or modify the state of modules declared as `upstream` relative to it
2. WHEN a governance module attempts to write to a module that is upstream in the influence graph, THE Governance_Influence_Graph SHALL detect the directionality violation and emit a CRITICAL severity event
3. THE Governance_Influence_Graph SHALL produce a directionality violation report listing all detected reverse-direction influence paths
4. FOR ALL valid governance influence graphs, reversing any single edge direction SHALL either maintain acyclicity or be detected as a directionality violation (directionality consistency property)

### Requirement 4: Minimal Deployment Authority Model

**User Story:** As a deployment engineer, I want a minimal authority model defining OWNER, CI, and RUNTIME roles with explicit authority partitioning, so that deployment boundaries are clear without enterprise overhead.

#### Acceptance Criteria

1. THE Deployment_Authority_Model SHALL define exactly three Authority_Roles: `OWNER` (human operator), `CI` (automated pipeline), `RUNTIME` (execution process)
2. THE Deployment_Authority_Model SHALL assign authorities as follows: OWNER holds `mutate_governance` and `change_enforcement_mode`; CI holds `deploy` and `accept_runtime_hash`; RUNTIME holds `execute_override` (emergency only, per governance-runtime-enforcement Req 35) and `change_fail_mode` (within pipeline execution bounds)
3. THE Deployment_Authority_Model SHALL be persisted in a structured YAML file (`.domainization/deployment_authority_model.yaml`)
4. WHEN the Deployment_Authority_Model is loaded, THE Governance_Runtime SHALL validate that the authority assignments match the declared model
5. FOR ALL valid Deployment_Authority_Model configurations, serializing then deserializing the model SHALL produce an equivalent object (round-trip property)

### Requirement 5: Deployment Authority Topology Constraint

**User Story:** As a system architect, I want no single actor to both deploy and mutate governance, so that CI cannot unilaterally change the rules it enforces.

#### Acceptance Criteria

1. THE Deployment_Authority_Model SHALL enforce that no Authority_Role holds both `deploy` and `mutate_governance` authorities simultaneously
2. THE Deployment_Authority_Model SHALL enforce that no Authority_Role holds both `change_enforcement_mode` and `deploy` authorities simultaneously
3. WHEN an authority configuration violates the topology constraints, THE Governance_Runtime SHALL reject the configuration at initialization and emit a CRITICAL severity event identifying the violated constraint
4. THE topology constraints SHALL be validated at governance initialization and whenever the authority model file is modified

### Requirement 6: Deploy Provenance Recording

**User Story:** As a deployment engineer, I want every deployment event linked to the CI run, actor, and policy version that authorized it, so that deployment decisions are fully traceable.

#### Acceptance Criteria

1. WHEN a deployment occurs, THE Governance_Runtime SHALL record a Deploy_Provenance entry containing: CI workflow run identifier, triggering actor identity, governance_policy_version active at deployment time, git commit SHA, and deployment timestamp
2. THE Deploy_Provenance SHALL include the runtime_integrity_hash (from governance-runtime-enforcement Req 36) that was validated at deployment time
3. THE Deploy_Provenance SHALL be persisted in the Mutation_Audit_Ledger with event type `deployment_authorized`
4. IF a deployment occurs without a matching CI validation run (manual deployment), THE Deploy_Provenance SHALL flag the deployment as `unvalidated` and emit a WARNING severity event
5. FOR ALL Deploy_Provenance records, serializing then deserializing the record SHALL produce an equivalent object (round-trip property)

### Requirement 7: Enforcement Mode Transition Cooldown

**User Story:** As a governance maintainer, I want enforcement mode transitions subject to a cooldown period, so that the system cannot oscillate between modes within a short timeframe (anti-flapping).

#### Acceptance Criteria

1. WHEN an enforcement mode transition occurs, THE Transition_Cooldown SHALL record the transition timestamp and enforce a minimum elapsed time before any subsequent transition is permitted, preventing mode oscillation
2. IF a mode transition is requested during an active Transition_Cooldown, THEN THE Governance_Runtime SHALL reject the transition and emit a WARNING severity event containing the remaining cooldown duration
3. THE Transition_Cooldown SHALL apply to all transitions: observability→soft, soft→hard, hard→soft, soft→observability (both escalation and de-escalation)
4. THE Transition_Cooldown duration SHALL be configurable in `.domainization/config.yaml` under a `transition_hysteresis` section, with a minimum of 1 hour, a default of 4 hours, and a maximum of 24 hours
5. WHEN an emergency override is invoked by a USER actor (governance-runtime-enforcement Req 35), THE Transition_Cooldown SHALL be bypassed with mandatory audit logging of the bypass reason

### Requirement 8: Enforcement Mode Rollback Logging

**User Story:** As a governance auditor, I want all enforcement mode transitions (including rollbacks and rejected attempts) persisted with context, so that mode transition history is complete.

#### Acceptance Criteria

1. WHEN a mode transition is attempted (whether successful or rejected), THE Governance_Runtime SHALL persist a structured record in the Mutation_Audit_Ledger containing: requested transition direction, success/rejection status, cooldown state, actor, and timestamp
2. WHEN a rollback (de-escalation) occurs, THE record SHALL additionally include: justification text and the governance_policy_version active at rollback time
3. THE transition audit persistence extends governance-runtime-enforcement Requirement 7.3 (which records successful transitions only) by also recording rejected attempts with rejection reasons
4. THE Governance_Runtime SHALL support querying transition history to produce a timeline of all transition attempts with their outcomes

### Requirement 9: Domain Lifecycle State Model

**User Story:** As a governance maintainer, I want domains themselves to have lifecycle states, so that domain deprecation and archival are formally governed rather than ad-hoc.

#### Acceptance Criteria

1. THE Domain_Registry SHALL support Domain_Lifecycle_State for each domain with the following valid states: `active`, `deprecated`, `archived`
2. THE Domain_Registry SHALL define valid transitions between Domain_Lifecycle_States: active→deprecated, deprecated→archived, deprecated→active (reactivation)
3. WHEN a domain lifecycle transition is requested, THE Governance_Runtime SHALL validate the transition against the defined valid transitions before persisting the change
4. IF an invalid domain lifecycle transition is attempted, THEN THE Governance_Runtime SHALL reject the transition and emit a CRITICAL severity event with the domain identifier, attempted from-state, attempted to-state, and valid transitions from the current state
5. THE Domain_Lifecycle_State SHALL be persisted in `.domainization/domain_registry.yaml` as a new field on each domain entry, defaulting to `active` for all existing domains
6. FOR ALL domain lifecycle state transitions, serializing then deserializing the transition record SHALL produce an equivalent object (round-trip property)

### Requirement 10: Domain Deprecation Artifact Reassignment

**User Story:** As a governance maintainer, I want domain deprecation to trigger artifact reassignment planning, so that artifacts owned by a deprecated domain are not orphaned.

#### Acceptance Criteria

1. WHEN a domain transitions to `deprecated` state, THE Governance_Runtime SHALL identify all artifacts with that domain as their `primary_domain` in the Artifact_Registry
2. WHEN a domain is deprecated, THE Governance_Runtime SHALL require a `reassignment_target` domain to be specified as part of the deprecation request
3. IF the `reassignment_target` domain cannot own all artifact types currently owned by the deprecated domain (per `cannot_own` constraints in the Domain_Registry), THEN THE Governance_Runtime SHALL reject the deprecation and report which artifact types cannot be reassigned
4. THE Governance_Runtime SHALL produce a reassignment plan listing each affected artifact and its proposed new domain, requiring explicit OWNER approval before execution
5. WHEN artifact reassignment is executed, THE Mutation_Audit_Ledger SHALL record each reassignment with: artifact identifier, previous domain, new domain, deprecation reason, and actor

### Requirement 11: Delta-Layer Non-Interference Guarantee

**User Story:** As a system architect, I want this delta spec to guarantee non-interference with existing governance-runtime-enforcement contracts, so that hardening does not break foundational guarantees.

#### Acceptance Criteria

1. THE delta layer SHALL NOT modify the behavior of any existing enforcement mode (observability, soft, hard) as defined in governance-runtime-enforcement Requirements 5–7
2. THE delta layer SHALL NOT introduce new fail modes beyond fail_open, fail_soft, and fail_closed as defined in governance-runtime-enforcement Requirement 29
3. THE delta layer SHALL NOT modify the existing Mutation_Audit_Ledger schema; it SHALL only append new event types (`deployment_authorized`, `enforcement_mode_rollback`, `domain_lifecycle_transition`) to the existing event type enumeration
4. THE delta layer SHALL NOT modify the existing Domain_Registry schema beyond adding the `lifecycle_state` field to each domain entry
5. THE delta layer SHALL reuse existing infrastructure (Mutation_Audit_Ledger, Actor_Identity, Governance_Policy_Version) from governance-runtime-enforcement rather than creating parallel systems

### Requirement 12: Property-Based Test Coverage for Delta Spec Contracts

**User Story:** As a governance maintainer, I want property-based tests (Hypothesis) for all new contracts introduced by this delta spec, so that the new governance logic is verified across generated input spaces.

#### Acceptance Criteria

1. THE test suite SHALL include Property_Test coverage for Governance_Influence_Graph cycle detection (all generated acyclic graphs remain acyclic after validation; all generated cyclic graphs are detected and rejected)
2. THE test suite SHALL include Property_Test coverage for Deployment_Authority_Model topology constraints (no valid configuration allows a single role to hold both deploy and mutate_governance)
3. THE test suite SHALL include Property_Test coverage for Transition_Cooldown enforcement (no transition permitted within cooldown period for all generated transition sequences)
4. THE test suite SHALL include Property_Test coverage for Domain_Lifecycle_State transition validation (valid transitions accepted, invalid transitions rejected for all domain states)
5. THE test suite SHALL include Property_Test coverage for Deploy_Provenance serialization and deserialization (round-trip property)

---

## CTO Strategic Directive: Post-Governance Focus Shift

**Status:** BINDING | **Decision Date:** 2026-05-29 | **Owner:** CTO

After this spec (deployment-authority-and-domainization-hardening) AND governance-runtime-enforcement are both implemented, verified, and merged:

### The Governance Cycle Closes.

No further governance specs. The governance layer is complete.

### Strategic Focus Shifts to: Financial Intelligence Expansion

**Priority order for next specs:**

| Priority | Domain | Current Artifacts | Target | Rationale |
|----------|--------|:-:|:-:|-----------|
| 1 | **REASONING** | 8 | 25+ | Biggest imbalance. Conviction Engine, Opportunity Engine, Decision Intelligence, Portfolio Intelligence |
| 2 | **SIMULATION** | 2 | 15+ | What-if, Stress Tests, Regime Simulation |
| 3 | **OPTIONS** | 0 | 10+ | Requires SIGNALS + REASONING + SIM foundation first |

### MoneyHorst's Burggraben in 12 Monaten:

```
Signal → Bedeutung → Wahrscheinlichkeit → Simulation → Entscheidung
```

Nicht: mehr Governance.

### Guiding Principle:

> MoneyHorst gewinnt durch bessere Modelle, nicht durch mehr Governance.
> Die Governance ist jetzt groß genug, um das System zu schützen,
> und klein genug, um nicht selbst zum Produkt zu werden.
