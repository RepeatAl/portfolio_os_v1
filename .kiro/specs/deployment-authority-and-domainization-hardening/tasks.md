# Implementation Plan: Deployment Authority and Domainization Hardening

## Overview

Lean delta layer implementation: 4 Python modules + 2 YAML data files extending governance-runtime-enforcement. Three phases — Foundation (data + modules), Property Tests, Integration + Verification. Each phase ends with an explicit verification gate.

## Tasks

- [x] 1. Foundation: Data Files and Core Modules
  - [x] 1.1 Create governance influence declarations YAML
    - Create `.domainization/governance_influence_declarations.yaml` with schema_version, all 13 module declarations (influence_graph, deployment_authority, transition_cooldown, domain_lifecycle, gate_framework, lifecycle_enforcer, boundary_enforcer, warning_governor, mutation_audit_ledger, policy_versioner, fail_mode_registry, state_provenance_tagger, shadow_authority_detector)
    - Each module declares: module_id, read_dependencies, write_dependencies, influence_direction (upstream/downstream)
    - _Requirements: 1.1, 1.4_

  - [x] 1.2 Create deployment authority model YAML
    - Create `.domainization/deployment_authority_model.yaml` with schema_version and exactly 3 roles: OWNER (mutate_governance, change_enforcement_mode), CI (deploy, accept_runtime_hash), RUNTIME (execute_override, change_fail_mode)
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 1.3 Implement governance/influence_graph.py
    - Implement `InfluenceDirection` enum, `ModuleDependencyDeclaration` frozen dataclass, `CycleDetectionResult`, `DirectionalityViolation` dataclasses
    - Implement `GovernanceInfluenceGraph` class: `load_declarations()` from YAML, `validate_declaration()`, `build_graph()` adjacency list from write_dependencies, `detect_cycles()` via DFS, `enforce_directionality()` checking downstream-writes-upstream violations, `validate_at_init()` orchestrator
    - Emit CRITICAL events to Mutation_Audit_Ledger on cycle detection, missing declarations, directionality violations
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3_

  - [x] 1.4 Implement governance/deployment_authority.py
    - Implement `AuthorityRole` enum (OWNER/CI/RUNTIME), `Authority` enum (6 authorities), `AuthorityAssignment` frozen dataclass, `DeployProvenance` dataclass
    - Implement `FORBIDDEN_AUTHORITY_PAIRS` constant, `DeploymentAuthorityModel` class: `load_model()` from YAML, `validate_topology()` checking forbidden pairs, `validate_at_init()`, `record_deploy_provenance()` appending to Mutation_Audit_Ledger with event_type `deployment_authorized`, `check_authority()`
    - Flag unvalidated deployments (is_validated=False) with WARNING severity
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4_

  - [x] 1.5 Implement governance/transition_cooldown.py
    - Implement `CooldownConfig` dataclass (duration_hours: float, default 4.0, clamped [1.0, 24.0]), `CooldownState` dataclass with `remaining` property, `TransitionAttempt` dataclass
    - Implement `TransitionCooldown` class: `load_config()` from config.yaml `transition_hysteresis` section, `get_cooldown_state()` querying ledger for last successful transition, `attempt_transition()` enforcing cooldown with emergency bypass, `query_transition_history()`
    - Record both successful and rejected attempts to Mutation_Audit_Ledger with event_type `enforcement_mode_rollback`
    - Emergency overrides (is_emergency=True) bypass cooldown with mandatory bypass_reason audit
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4_

  - [x] 1.6 Implement governance/domain_lifecycle.py
    - Implement `DomainLifecycleState` enum (active/deprecated/archived), `VALID_DOMAIN_TRANSITIONS` dict, `DeprecationRequest`, `ReassignmentPlanEntry`, `ReassignmentPlan` dataclasses
    - Implement `DomainLifecycleManager` class: `get_domain_state()` defaulting to ACTIVE, `validate_transition()` against VALID_DOMAIN_TRANSITIONS, `request_deprecation()` with cannot_own check and reassignment plan generation, `execute_reassignment()` recording to ledger, `transition_domain()` for non-deprecation transitions
    - Record all lifecycle transitions to Mutation_Audit_Ledger with event_type `domain_lifecycle_transition`
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5_

  - [x] 1.7 Add transition_hysteresis config section
    - Add `transition_hysteresis: { cooldown_hours: 4 }` section to `.domainization/config.yaml`
    - _Requirements: 7.4_

- [ ] 2. Phase 1 Verification Gate
  - Ensure all tests pass (`pytest tests/ -v`), verify all 4 modules import cleanly, verify both YAML data files parse without error, confirm no existing governance-runtime-enforcement tests are broken (non-interference). Ask the user if questions arise.

- [ ] 3. Property-Based Tests (Hypothesis, min 200 iterations)
  - [ ] 3.1 Create tests/test_influence_graph_properties.py — Properties 1, 2, 3
    - **Property 1: Dependency Declaration Round-Trip** — Generate arbitrary ModuleDependencyDeclaration objects, serialize to dict, deserialize back, assert equality
    - **Property 2: Cycle Detection Completeness** — Generate random DAGs (must report no cycle) and graphs with injected back-edges (must report cycle with valid path)
    - **Property 3: Directionality Enforcement** — Generate module sets with random direction assignments; downstream modules with upstream write_deps must produce violations, otherwise no violations
    - **Validates: Requirements 1.4, 1.5, 2.1, 2.2, 2.3, 2.5, 3.1, 3.2, 3.4**

  - [ ] 3.2 Create tests/test_deployment_authority_properties.py — Properties 4, 5, 6
    - **Property 4: Authority Model Round-Trip** — Generate valid authority configurations (3 roles, frozensets of Authority), serialize/deserialize, assert equivalence
    - **Property 5: Topology Constraint Enforcement** — Generate configurations with/without forbidden pairs; configurations with forbidden pairs must be rejected, clean configurations must be accepted
    - **Property 6: Deploy Provenance Round-Trip** — Generate arbitrary DeployProvenance records, serialize/deserialize, assert equality
    - **Validates: Requirements 4.3, 4.5, 5.1, 5.2, 5.3, 6.1, 6.5**

  - [ ] 3.3 Create tests/test_transition_cooldown_properties.py — Property 7
    - **Property 7: Cooldown Enforcement** — Generate sequences of (timestamp, is_emergency) pairs; no two successful non-emergency transitions within cooldown_duration; emergency overrides always succeed with cooldown_bypassed=True
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.5**

  - [ ] 3.4 Create tests/test_domain_lifecycle_properties.py — Property 8
    - **Property 8: Domain Lifecycle Transition Validation** — Generate all (from_state, to_state) combinations; valid transitions {(active,deprecated), (deprecated,archived), (deprecated,active)} accepted, all others rejected
    - **Validates: Requirements 9.2, 9.3, 9.4**

- [ ] 4. Phase 2 Verification Gate
  - Run full property test suite (`pytest tests/test_influence_graph_properties.py tests/test_deployment_authority_properties.py tests/test_transition_cooldown_properties.py tests/test_domain_lifecycle_properties.py -v`), verify all 8 properties pass with ≥200 iterations each. Ask the user if questions arise.

- [ ] 5. Integration and Wiring
  - [ ] 5.1 Create tests/test_delta_non_interference.py
    - Verify existing enforcement modes (observability/soft/hard) behavior unchanged
    - Verify no new fail modes introduced beyond fail_open/fail_soft/fail_closed
    - Verify Mutation_Audit_Ledger schema unchanged (only additive event types)
    - Verify Domain_Registry schema unchanged (only additive lifecycle_state field)
    - Verify Actor_Identity and Policy_Versioner consumed read-only
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ]* 5.2 Write unit tests for all 4 modules
    - `tests/test_influence_graph.py` — Valid/invalid YAML loading, missing fields, missing file, module exclusion on missing declaration
    - `tests/test_deployment_authority.py` — Valid/invalid YAML, role count validation, unvalidated deployment WARNING
    - `tests/test_transition_cooldown.py` — Config clamping (below min, above max, missing section), cooldown rejection message
    - `tests/test_domain_lifecycle.py` — Default state=active, deprecation cannot_own check, reassignment plan generation, invalid transition rejection
    - _Requirements: 1.2, 1.3, 4.4, 5.3, 6.4, 7.4, 9.4, 10.3_

  - [ ] 5.3 Wire initialization sequence
    - Ensure governance init loads delta components in order: InfluenceGraph → DeploymentAuthority → TransitionCooldown → DomainLifecycleManager
    - Verify CRITICAL events halt init (influence graph cycles, topology violations)
    - Verify fail_soft components (cooldown, lifecycle) degrade gracefully
    - _Requirements: 2.4, 4.4, 5.4, 11.5_

- [ ] 6. Final Verification Gate
  - Run full test suite (`pytest tests/ -v`), verify ALL property tests (8 properties × 200 iterations), unit tests, integration tests, and non-interference tests pass. Produce verification metrics (total, passed, failed, skipped). Confirm delta layer is additive-only with no breaking changes to governance-runtime-enforcement. Ask the user if questions arise.

- [ ] 7. Documentation
  - [ ] 7.1 Create `governance/README_deployment_authority_and_domain_lifecycle.md`
    - Document all 4 new modules: influence_graph, deployment_authority, transition_cooldown, domain_lifecycle
    - Document both YAML data files: governance_influence_declarations.yaml, deployment_authority_model.yaml
    - Include key interfaces, usage examples, CTO directives, and requirements traceability
    - Document the initialization sequence and integration with existing ledger/enforcer infrastructure
    - Document the transition_hysteresis config section
    - Follow existing README style from `governance/README_enforcement_runtime_and_integration.md`

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Verification gates are explicit execution points (per steering rule) — they MUST be dispatched and run, never auto-completed
- Property tests use Hypothesis with `@settings(max_examples=200)`
- All modules reuse existing infrastructure: Mutation_Audit_Ledger, Actor_Identity, Policy_Versioner
- Python 3.13.7 via `.venv/bin/python`, tests via `.venv/bin/python -m pytest`
- After this spec completes, governance cycle closes — focus shifts to REASONING domain

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.7"] },
    { "id": 1, "tasks": ["1.3", "1.4", "1.5", "1.6"] },
    { "id": 2, "tasks": ["3.1", "3.2", "3.3", "3.4"] },
    { "id": 3, "tasks": ["5.1", "5.2", "5.3"] }
  ]
}
```
