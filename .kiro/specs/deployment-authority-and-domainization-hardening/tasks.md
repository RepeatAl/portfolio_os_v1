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

- [x] 2. Phase 1 Verification Gate
  - Ensure all tests pass (`pytest tests/ -v`), verify all 4 modules import cleanly, verify both YAML data files parse without error, confirm no existing governance-runtime-enforcement tests are broken (non-interference). Ask the user if questions arise.

- [x] 3. Property-Based Tests (Hypothesis, min 200 iterations)
  - [x] 3.1 Create tests/test_influence_graph_properties.py — Properties 1, 2, 3
    - **Property 1: Dependency Declaration Round-Trip** — Generate arbitrary ModuleDependencyDeclaration objects, serialize to dict, deserialize back, assert equality
    - **Property 2: Cycle Detection Completeness** — Generate random DAGs (must report no cycle) and graphs with injected back-edges (must report cycle with valid path). Verify violations emit critical audit records when applicable.
    - **Property 3: Directionality Enforcement** — Generate module sets with random direction assignments; downstream modules with upstream write_deps must produce violations, otherwise no violations. Verify malformed module declarations fail validation.
    - **Validates: Requirements 1.4, 1.5, 2.1, 2.2, 2.3, 2.5, 3.1, 3.2, 3.4**
    - **Execution notes:**
      - Use Hypothesis (already installed in project)
      - Inspect existing property test patterns in `tests/test_property_*.py` before writing
      - Reuse existing test helpers where available (DRY)
      - Do NOT use static fixtures only — generate diverse inputs
      - Do NOT hardcode old 342-test baseline — use actual discovered baseline from current run

  - [x] 3.2 Create tests/test_deployment_authority_properties.py — Properties 4, 5, 6
    - **Property 4: Authority Model Round-Trip** — Generate valid authority configurations (3 roles, frozensets of Authority), serialize/deserialize, assert equivalence
    - **Property 5: Topology Constraint Enforcement** — Generate configurations with/without forbidden pairs; configurations with forbidden pairs must be rejected, clean configurations must be accepted
      - **IMPORTANT: Forbidden pair deviation** — Implementation uses `(change_enforcement_mode, execute_override)` instead of design spec's `(deploy, change_enforcement_mode)`. Test the IMPLEMENTED pair explicitly. Document whether implementation should remain or be corrected. Do NOT silently normalize the deviation.
      - Verify `mutate_governance` and `deploy` cannot be held by one role (pair 1)
      - Verify `change_enforcement_mode` and `execute_override` cannot be held by one role (pair 2, as implemented)
    - **Property 6: Deploy Provenance Round-Trip** — Generate arbitrary DeployProvenance records, serialize/deserialize, assert equality. Verify invalid deploy provenance (is_validated=False) emits WARNING. Verify validated provenance is accepted consistently.
    - **Validates: Requirements 4.3, 4.5, 5.1, 5.2, 5.3, 6.1, 6.5**
    - **Execution notes:**
      - Verify check_authority only succeeds for assigned authorities
      - Test all 6 authority values against all 3 roles

  - [x] 3.3 Create tests/test_transition_cooldown_properties.py — Property 7
    - **Property 7: Cooldown Enforcement** — Generate sequences of (timestamp, is_emergency) pairs; no two successful non-emergency transitions within cooldown_duration; emergency overrides always succeed with cooldown_bypassed=True
    - **Additional invariants to test:**
      - Generate cooldown_hours below (0.5), inside (4.0), and above (30.0) allowed range — verify clamping to [1.0, 24.0]
      - Verify repeated transitions inside cooldown window are rejected
      - Verify transitions after cooldown window expires are accepted
      - Verify emergency override requires non-empty bypass_reason (ValueError if empty)
      - Verify emergency override records an audit event to ledger
      - Verify transition history records both accepted and rejected attempts
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.5**

  - [x] 3.4 Create tests/test_domain_lifecycle_properties.py — Property 8
    - **Property 8: Domain Lifecycle Transition Validation** — Generate all (from_state, to_state) combinations; valid transitions {(active,deprecated), (deprecated,archived), (deprecated,active)} accepted, all others rejected
    - **Additional invariants to test:**
      - Verify deprecated domains cannot own active responsibilities (cannot_own check)
      - Verify reassignment plans preserve required ownership handoff semantics
      - Verify reassignment execution records ledger entries
      - Verify unknown domains default to ACTIVE only where implementation explicitly defines that behavior
    - **Validates: Requirements 9.2, 9.3, 9.4**

- [x] 4. Phase 2 Verification Gate and Forbidden-Pair Resolution
  - [x] 4.1 Resolve forbidden-authority-pair deviation (CTO Decision: additive stricter set)
    - **CTO Decision (2026-05-31):** The final FORBIDDEN_AUTHORITY_PAIRS set SHALL be additive and stricter, not weaker. The implementation keeps the existing pair AND adds the design-spec pair.
    - **Final forbidden-pair set (3 pairs):**
      1. `(mutate_governance, deploy)` — original pair 1 (design + implementation agree)
      2. `(deploy, change_enforcement_mode)` — design-spec pair 2 (ADD THIS)
      3. `(change_enforcement_mode, execute_override)` — implementation pair 2 (KEEP THIS)
    - Update `governance/deployment_authority.py` FORBIDDEN_AUTHORITY_PAIRS to contain all 3 pairs
    - Update `tests/test_deployment_authority_properties.py` to test all 3 forbidden pairs explicitly
    - Update property test docstring to reflect resolution (no longer a "deviation" — it is an additive decision)
    - Verify existing property tests still pass after the change
    - If the current spec or design doc conflicts with adding the third pair, STOP and report the conflict to the user
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 4.2 Run full property test suite under default Hypothesis profile
    - **Exact command:** `.venv/bin/python -m pytest tests/test_influence_graph_properties.py tests/test_deployment_authority_properties.py tests/test_transition_cooldown_properties.py tests/test_domain_lifecycle_properties.py -v --hypothesis-profile=default --hypothesis-show-statistics`
    - Verify the tests run under the `default` profile (max_examples=200), NOT the `fast` CI profile (max_examples=5)
    - Verify all 8 properties pass
    - Verify each property test that declares `@settings(max_examples=200)` actually reports the full intended example volume, or explain any lower count caused by exhausted finite search space
    - Do NOT accept a report that only says "33 passed" without Hypothesis statistics
    - Document: exact profile used, exact command, exact test count, exact property count, exact runtime
    - Explicitly confirm whether the forbidden-pair deviation has been resolved
    - Produce the Phase 2 verification report at `.domainization/reports/property_tests_verification_gate_task4.md`
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 5. Integration and Wiring
  - [ ] 5.2 Write unit tests for all 4 modules
    - `tests/test_influence_graph.py` — Valid/invalid YAML loading, missing fields, missing file, module exclusion on missing declaration
    - `tests/test_deployment_authority.py` — Valid/invalid YAML, role count validation, unvalidated deployment WARNING, final 3-pair forbidden set enforcement
    - `tests/test_transition_cooldown.py` — Config clamping (below min, above max, missing section), cooldown rejection message
    - `tests/test_domain_lifecycle.py` — Default state=active, deprecation cannot_own check, reassignment plan generation, invalid transition rejection
    - Do NOT duplicate property tests — unit tests cover deterministic edge cases, malformed files, missing fields, missing files, and exact error semantics
    - Include the final forbidden-pair decision (3 pairs) in deployment_authority unit tests
    - _Requirements: 1.2, 1.3, 4.4, 5.3, 6.4, 7.4, 9.4, 10.3_

  - [ ] 5.1 Create tests/test_delta_non_interference.py
    - Verify existing enforcement modes (observability/soft/hard) behavior unchanged
    - Verify no new fail modes introduced beyond fail_open/fail_soft/fail_closed
    - Verify Mutation_Audit_Ledger schema unchanged (only additive event types)
    - Verify Domain_Registry schema unchanged (only additive lifecycle_state field)
    - Verify Actor_Identity and Policy_Versioner consumed read-only
    - Verify no existing governance-runtime-enforcement behavior regresses
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ] 5.3 Wire initialization sequence
    - Ensure governance init loads delta components in order: InfluenceGraph → DeploymentAuthority → TransitionCooldown → DomainLifecycleManager
    - Verify CRITICAL events halt init (influence graph cycles, topology violations)
    - Verify fail_soft components (cooldown, lifecycle) degrade gracefully
    - No framework escalation. No plugin system. No event bus. No runtime kernel.
    - _Requirements: 2.4, 4.4, 5.4, 11.5_

- [ ] 6. Final Verification Gate
  - **Exact command:** `.venv/bin/python -m pytest tests/ -v --hypothesis-profile=default --hypothesis-show-statistics`
  - Report: total, passed, failed, skipped
  - Report: property-test statistics (Hypothesis example counts per test)
  - Report: unit-test count
  - Report: integration-test count
  - Report: non-interference-test count
  - Confirm additive-only delta behavior
  - Confirm no regression against the current discovered baseline (do NOT hardcode old 342 number — use actual discovered baseline)
  - If baseline count differs from earlier reports, document why
  - Produce verification report at `.domainization/reports/final_verification_gate_task6.md`
  - Ask the user if questions arise.

- [ ] 7. Documentation
  - [ ] 7.1 Create `governance/README_deployment_authority_and_domain_lifecycle.md`
    - Create ONLY after Task 6 passes
    - Document all 4 new modules: influence_graph, deployment_authority, transition_cooldown, domain_lifecycle
    - Document both YAML data files: governance_influence_declarations.yaml, deployment_authority_model.yaml
    - Document the final forbidden-pair set (3 pairs) with CTO decision rationale
    - Document the initialization sequence and integration with existing ledger/enforcer infrastructure
    - Document the transition_hysteresis config section
    - Document requirements traceability
    - Document that this is a lean delta layer, not a framework expansion
    - Include key interfaces and usage examples
    - Follow existing README style from `governance/README_enforcement_runtime_and_integration.md`

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Verification gates are explicit execution points (per steering rule) — they MUST be dispatched and run, never auto-completed
- Property tests use Hypothesis with `@settings(max_examples=200)`
- All modules reuse existing infrastructure: Mutation_Audit_Ledger, Actor_Identity, Policy_Versioner
- Python 3.13.7 via `.venv/bin/python`, tests via `.venv/bin/python -m pytest`
- After this spec completes, governance cycle closes — focus shifts to REASONING domain
- **CTO Decision (2026-05-31):** Forbidden-pair deviation resolved as ADDITIVE. Final set = 3 pairs. No silent deviations permitted before integration.
- **Task 5 execution order is MANDATORY:** 5.2 (unit tests) → 5.1 (non-interference) → 5.3 (wiring). Rationale: lock module behavior before verifying non-interference, then wire only after both are green.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.7"] },
    { "id": 1, "tasks": ["1.3", "1.4", "1.5", "1.6"] },
    { "id": 2, "tasks": ["3.1", "3.2", "3.3", "3.4"] },
    { "id": 3, "tasks": ["4.1"] },
    { "id": 4, "tasks": ["4.2"] },
    { "id": 5, "tasks": ["5.2"] },
    { "id": 6, "tasks": ["5.1"] },
    { "id": 7, "tasks": ["5.3"] },
    { "id": 8, "tasks": ["7.1"] }
  ]
}
```
