# Implementation Plan: Governance Runtime Enforcement (Scope-Frozen)

## Overview

This plan implements the governance runtime enforcement system after CTO-approved scope freeze (2026-05-29). Active scope: 28 of 49 requirements. Deferred: Warning System (Req 20–24), Advanced Hardenings (Req 30, 35, 37, 38, 42), Meta-Governance (Req 43–47). All new modules go in `governance/`. Property-based tests use Hypothesis with `@settings(max_examples=100)`. Execution: `.venv/bin/python`.

**Principle**: Governance protects MoneyHorst. Governance does not become MoneyHorst.

## Tasks

- [x] 1. Foundation: Data Contracts and Actor Model
  - [x] 1.1 Create `governance/actor_identity.py` with ActorType StrEnum and ActorIdentity dataclass
    - Implement `ActorType` StrEnum with 7 values: SYSTEM, CI, USER, ENGINE, MIGRATION, RUNTIME, HOT_RELOAD
    - Implement `ActorIdentity` dataclass with actor_type, actor_id, context dict, is_fallback boolean
    - Implement `from_environment()`, `ci_actor()`, `engine_actor()` class methods
    - Implement serialization to/from dict for YAML persistence
    - _Requirements: 33.1, 33.2, 33.3, 33.4, 33.5, 33.6_

  - [x] 1.2 Create `governance/gate_framework.py` with GateResult and GateSummary dataclasses
    - Implement `GateResult` dataclass with gate_name, status, enforcement_action, duration_ms, details, timestamp, governance_policy_version, governance_state_provenance
    - Implement `GateSummary` dataclass with total_gates, passed, failed, blocked, timed_out, total_duration_ms, aggregate_state, git_sha, branch, runtime_integrity_hash
    - Implement serialization to/from dict for JSON/YAML round-trip
    - Implement `compute_aggregate_state()` logic: healthy/partial/degraded/collapsed
    - _Requirements: 5.5, 5.6, 26.1, 26.2, 26.3, 26.4, 32.1, 32.2, 32.6_

  - [x] 1.3 Create `governance/fail_mode_registry.py` with FailMode StrEnum and FailModeRegistry class
    - Implement `FailMode` StrEnum with fail_open, fail_soft, fail_closed
    - Implement `FailModeRegistry` class loading from `.domainization/fail_mode_config.yaml`
    - Implement `get_fail_mode(component_name)` and `get_all_classifications()`
    - Implement `freeze()` and `is_frozen()` for self-disable protection (Req 49)
    - Implement `attempt_modification()` returning (allowed, reason) tuple
    - _Requirements: 29.1, 29.7, 49.1, 49.2, 49.4_

  - [x] 1.4 Create `governance/state_provenance_tagger.py` with GovernanceProvenance StrEnum and StateProvenanceTagger
    - Implement `GovernanceProvenance` StrEnum with 6 values: authoritative, cached, fallback_derived, bootstrap_derived, partially_degraded, indeterminate
    - Implement `StateProvenanceTagger` with `tag()` and `get_current_provenance()` methods
    - _Requirements: 41.1, 41.2, 41.3, 41.4, 41.5, 41.6_

  - [x] 1.5 Create `.domainization/fail_mode_config.yaml` configuration file
    - Define schema_version, component fail-mode classifications per the design
    - Include enforcement-mode-dependent fail modes for yaml_config_parser and lifecycle_enforcer
    - _Requirements: 29.7_

  - [x]* 1.6 Write property test for ActorIdentity round-trip serialization
    - **Property 3: ActorIdentity Round-Trip Serialization**
    - **Validates: Requirements 33.6**
    - File: `tests/test_property_actor_identity_roundtrip.py`

  - [x]* 1.7 Write property test for GateResult round-trip serialization
    - **Property 1: GateResult Round-Trip Serialization**
    - **Validates: Requirements 5.6, 26.4**
    - File: `tests/test_property_gate_result_roundtrip.py`

  - [x]* 1.8 Write property test for Enforcement Mode round-trip
    - **Property 4: Enforcement Mode Round-Trip**
    - **Validates: Requirements 7.6**
    - File: `tests/test_property_enforcement_mode_roundtrip.py`

  - [x]* 1.9 Write property test for Self-Disable Guard immutability
    - **Property 32: Self-Disable Guard Immutability**
    - **Validates: Requirements 49.1, 49.2, 49.4**
    - File: `tests/test_property_self_disable_guard.py`

- [x] 2. Foundation Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/test_property_actor_identity_roundtrip.py tests/test_property_gate_result_roundtrip.py tests/test_property_enforcement_mode_roundtrip.py tests/test_property_self_disable_guard.py -v`
  - Verify all foundation modules import cleanly
  - Produce verification artifact

- [x] 3. CI Pipeline Hardening
  - [x] 3.1 Extend `.github/workflows/python-app.yml` with full test suite step
    - Add step: `.venv/bin/python -m pytest tests/ -v --tb=short` with 60s time budget
    - Ensure step blocks merge on failure
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [x] 3.2 Add all-directory syntax validation step to CI workflow
    - Add step: `.venv/bin/python -m compileall -q` for engines/, runtime/, governance/, .domainization/src/, tests/
    - Use quiet mode, block merge on failure
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.3 Add YAML validation step to CI workflow
    - Add inline Python step to load and validate required keys in config.yaml, domain_registry.yaml, artifact_registry.yaml, lifecycle_state_machine.yaml
    - Block merge on parse failure, report file name and error
    - _Requirements: 3.1, 3.2, 3.3_

  - [x] 3.4 Add ENGINE_REGISTRY-based import validation step to CI workflow
    - Add step that reads `engines/engine_registry.py` ENGINE_REGISTRY dict
    - Import only engines listed in the registry (not hardcoded)
    - Block merge on import failure for any registered engine
    - Future engines with optional dependencies are only validated if registered
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 3.5 Create `governance/runtime_integrity_hash.py` with RuntimeIntegrityHash class
    - Implement `compute()` method: SHA-256 over deterministically sorted, canonicalized file contents
    - Implement `verify_against(expected_hash)` returning (match, details) tuple
    - Define TARGET_PATHS covering behavior-defining files:
      - `.domainization/config.yaml`
      - `.domainization/lifecycle_state_machine.yaml`
      - `.domainization/domain_registry.yaml`
      - `.domainization/artifact_registry.yaml`
      - `.domainization/fail_mode_config.yaml`
      - `governance/confidence_policy.yaml`
      - `governance/*.py`
      - `runtime/*.py`
      - `engines/engine_registry.py`
    - Do NOT hash individual engine implementations (*_engine.py)
    - _Requirements: 36.1, 36.2, 36.5, 36.6_

  - [x] 3.6 Create `governance/hash_canonicalizer.py` with HashCanonicalizer class
    - Implement `normalize_line_endings()`: CRLF/CR → LF
    - Implement `normalize_encoding()`: → UTF-8
    - Implement `strip_trailing_whitespace()`: per-line strip
    - Implement `ensure_final_newline()`: exactly one trailing newline
    - Implement `canonicalize_yaml()`: parse → re-serialize with sorted keys
    - Implement `canonicalize_python()`: LF + UTF-8 + strip trailing whitespace
    - Implement `canonicalize_file()`: auto-detect by extension
    - Implement `compute_hash()`: SHA-256 over sorted canonicalized content
    - _Requirements: 48.1, 48.2, 48.3, 48.4_

  - [x] 3.7 Add runtime integrity hash step to CI workflow
    - Add informational step computing and persisting the hash as CI artifact
    - Wire RuntimeIntegrityHash with HashCanonicalizer
    - 5s time budget
    - _Requirements: 36.1, 36.2_

  - [ ]* 3.8 Write property test for Runtime Integrity Hash determinism
    - **Property 19: Runtime Integrity Hash Determinism**
    - **Validates: Requirements 36.1, 36.5, 36.6**
    - File: `tests/test_property_runtime_integrity_hash.py`

  - [ ]* 3.9 Write property test for Hash Canonicalization platform independence
    - **Property 31: Hash Canonicalization Platform Independence**
    - **Validates: Requirements 48.1, 48.2, 48.4**
    - File: `tests/test_property_hash_canonicalization.py`

- [x] 4. CI Hardening Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify CI workflow YAML is valid and all new steps are present
  - Verify `governance/runtime_integrity_hash.py` and `governance/hash_canonicalizer.py` import cleanly
  - Produce verification artifact

- [-] 5. Enforcement Runtime: Gate Executor, Lifecycle, Boundary, Cold-Start
  - [x] 5.1 Implement GateFramework executor logic in `governance/gate_framework.py`
    - Implement `__init__(config, enforcement_mode)` loading gate configurations
    - Implement `execute_gate(gate_name, check_fn, time_budget_ms)` with timeout handling
    - Implement `execute_all_gates()` producing GateSummary
    - Implement enforcement mode logic: observability→warn, soft→block if blocking_in_soft, hard→block if blocking_in_soft or blocking_in_hard
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4_

  - [x] 5.2 Create `governance/lifecycle_enforcer.py` with LifecycleEnforcer class
    - Implement `__init__(state_machine_path, enforcement_mode)` loading lifecycle YAML
    - Implement `validate_transition(artifact_id, artifact_type, from_state, to_state)` against state machine
    - Implement `is_read_only(artifact_type, current_state)` checking read_only_states
    - Implement `is_regenerable(artifact_type, current_state)` checking regenerable_states
    - Implement `enforce_transition()`, `enforce_read_only()`, `enforce_regenerable()` producing GateResult
    - Respect enforcement mode: observability→warn, soft→reject with warning, hard→reject with error
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.1, 9.2, 9.3, 9.4, 10.1, 10.2, 10.3, 10.4_

  - [x] 5.3 Create `governance/boundary_enforcer.py` with BoundaryEnforcer class
    - Implement `__init__(artifact_registry_path, domain_registry_path, enforcement_mode)`
    - Implement `check_write_permission(writing_domain, artifact_id)` checking allowed_writers
    - Implement `check_cannot_own(domain_id, artifact_type)` checking cannot_own constraints
    - Implement `enforce_write()` and `enforce_domain_assignment()` producing GateResult
    - Implement `detect_cross_domain_interaction()` for cross-domain logging
    - Implement `classify_artifact()` for canonical boundary runtime discovery
    - Handle `ALL` in allowed_writers as universal permission
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 17.1, 17.2, 17.3, 17.4, 18.1, 18.2, 18.3, 18.4, 19.1, 19.2, 19.3, 19.4_

  - [x] 5.4 Create `governance/cold_start_handler.py` with simplified ColdStartHandler
    - Implement `is_cold_start()`: returns True if governance state is missing (no ledger file)
    - Implement `initialize(actor)`: create minimal defaults, return bootstrap LedgerEntry
    - Cold-start forces observability mode regardless of configured mode
    - Tag provenance as `bootstrap_derived`
    - No stuck-cold-start detection, no 3-run threshold, no complex bootstrap
    - _Requirements: 31.1, 31.2_

  - [ ]* 5.5 Write property test for Gate Blocking Correctness
    - **Property 6: Gate Blocking Correctness**
    - **Validates: Requirements 5.1, 5.3, 5.4**
    - File: `tests/test_property_gate_blocking_correctness.py`

  - [ ]* 5.6 Write property test for Lifecycle Transition Validation
    - **Property 7: Lifecycle Transition Validation Correctness**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
    - File: `tests/test_property_lifecycle_transition_validation.py`

  - [ ]* 5.7 Write property test for Read-Only State Protection
    - **Property 8: Read-Only State Protection**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**
    - File: `tests/test_property_read_only_protection.py`

  - [ ]* 5.8 Write property test for Regenerable State Gate
    - **Property 9: Regenerable State Gate**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**
    - File: `tests/test_property_regenerable_state_gate.py`

  - [ ]* 5.9 Write property test for Boundary Enforcement Correctness
    - **Property 10: Boundary Enforcement Correctness**
    - **Validates: Requirements 16.1, 16.2, 16.3, 16.4, 16.5**
    - File: `tests/test_property_boundary_enforcement.py`

  - [ ]* 5.10 Write property test for Cannot-Own Constraint Consistency
    - **Property 11: Cannot-Own Constraint Consistency**
    - **Validates: Requirements 17.1, 17.2, 17.3, 17.4**
    - File: `tests/test_property_cannot_own_consistency.py`

- [x] 6. Enforcement Runtime Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify gate framework, lifecycle enforcer, boundary enforcer, cold-start handler all import and integrate
  - Verify enforcement mode logic across observability/soft/hard
  - Produce verification artifact

- [x] 7. Audit Ledger, Policy Versioning, and Shadow Authority
  - [x] 7.1 Create `governance/mutation_audit_ledger.py` with LedgerEntry dataclass and MutationAuditLedger class
    - Implement `LedgerEntry` dataclass with entry_id, event_type, timestamp, actor, governance_policy_version, severity, details
    - Implement `MutationAuditLedger.__init__(ledger_path)` with file creation on missing
    - Implement `append(entry)` with append-only YAML persistence
    - Implement `query_by_time_range(start, end)` and `query_by_event_type(event_type)`
    - Implement `recover_from_corruption()` creating new ledger on failure
    - Implement `is_cold_start()` checking ledger existence
    - Support event types: REGISTRY_ADD, REGISTRY_MODIFY, REGISTRY_REMOVE, GOVERNANCE_EVENT, POLICY_CHANGE, SUNSET_TRANSITION
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 13.1, 13.2, 13.3, 13.4, 13.5, 14.1, 14.2, 14.3, 15.1, 15.2, 15.3_

  - [x] 7.2 Create `governance/policy_versioner.py` with PolicyVersioner class
    - Implement `compute_version()` as SHA-256 of combined sorted governance file contents
    - Implement `detect_change(previous_version)` returning boolean
    - Implement `get_current_version()` for embedding in GateResult and LedgerEntry
    - Define GOVERNANCE_FILES list: config.yaml, lifecycle_state_machine.yaml, domain_registry.yaml, confidence_policy.yaml
    - _Requirements: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6_

  - [x] 7.3 Create `governance/shadow_authority_detector.py` with ShadowAuthorityDetector class (OBSERVATION ONLY)
    - Implement `check_write_authority(writing_module, target_artifact_id)` returning boolean
    - Implement `record_shadow_event(writing_module, target_artifact_id, declared_writers)` returning event dict
    - Implement `get_observation_report()` returning `{"unique_paths": int, "undeclared_writers": [...], "severity_recommendation": str}`
    - Distinguish registered engine shadow authority from unregistered module shadow authority
    - The detector MUST observe, measure, and report ONLY
    - The detector MUST NOT decide severity, classify as critical, or block
    - Severity assignment and blocking decisions belong to GateFramework/EnforcementMode, not here
    - CTO DIRECTIVE: No hard threshold, no CRITICAL classification, no blocking logic in detector
    - _Requirements: 40.1, 40.2, 40.3, 40.4, 40.5_

  - [ ]* 7.4 Write property test for Policy Version Determinism
    - **Property 18: Policy Version Determinism**
    - **Validates: Requirements 34.1, 34.5, 34.6**
    - File: `tests/test_property_policy_version_determinism.py`

  - [ ]* 7.5 Write property test for Shadow Authority Detection Threshold
    - **Property 24: Shadow Authority Detection Threshold**
    - **Validates: Requirements 40.1, 40.3, 40.5**
    - File: `tests/test_property_shadow_authority_threshold.py`

- [x] 8. Audit Ledger Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify mutation audit ledger, policy versioner, shadow authority detector all import and integrate
  - Verify ledger append-only behavior and corruption recovery
  - Produce verification artifact

- [x] 9. Integration Wiring
  - [x] 9.1 Add enforcement mode configuration to `.domainization/config.yaml`
    - Add `governance_enforcement.mode` field (default: `observability`)
    - Add transition criteria documentation as YAML comments
    - Wire enforcement mode into GateFramework, LifecycleEnforcer, BoundaryEnforcer initialization
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 9.2 Wire lifecycle transition audit logging
    - Connect LifecycleEnforcer to MutationAuditLedger
    - Emit GOVERNANCE_EVENT on every enforce_transition() call
    - Include actor identity, policy version, and provenance in ledger entries
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [x] 9.3 Wire boundary enforcer to audit ledger
    - Connect BoundaryEnforcer to MutationAuditLedger for cross-domain interaction logging
    - Connect ShadowAuthorityDetector to MutationAuditLedger for shadow event recording
    - _Requirements: 19.1, 40.1, 40.3_

  - [x] 9.4 Implement runtime invariant preservation validation
    - Create `governance/invariant_validator.py` with RuntimeInvariantValidator class
    - Validate runtime-owned invariants only:
      - INV-3: Chain_Model is SIGNALS(L1)->SEMANTICS(L2)->REASONING(L3)->REPORT(L4)
      - INV-4: Severity levels strictly ordered (INFO < WARNING < DEGRADED < CRITICAL < CANONICAL_BREAK < DETERMINISTIC_FAILURE)
      - INV-5: Runtime states belong to orthogonal integrity dimensions
      - INV-7: Pipeline execution completes (degraded output preferred over no output)
      - INV-8: Observability mode never blocks commits or pipeline execution
    - Wire into gate framework as a validation gate
    - Note: INV-1, INV-2, INV-6, INV-9, INV-10 are Domainization-owned invariants — not validated here
    - _Requirements: 25.3, 25.4, 25.5, 25.7, 25.8_

  - [x] 9.5 Implement ontology growth observability report
    - Create `governance/ontology_growth_observer.py` with OntologyGrowthObserver class
    - The module MUST: measure, report, trend
    - The module MUST NOT: block, reject, enforce
    - Output: current counts (artifact types, governance dimensions, severity levels, total concepts), growth rate, recommendation
    - No pre-registration blocking — observation only
    - CTO DIRECTIVE: This is an observation engine, not a constraint enforcer
    - _Requirements: 39.1, 39.2, 39.3, 39.4_

  - [x] 9.6 Wire cold-start handler into pipeline initialization
    - Check `is_cold_start()` at pipeline start
    - If cold-start: call `initialize(actor)`, force observability mode, tag provenance
    - If not cold-start: proceed with configured enforcement mode
    - _Requirements: 31.1, 31.2_

- [x] 10. Final Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify full integration: gate framework → lifecycle → boundary → ledger → policy versioner
  - Verify enforcement mode transitions work end-to-end
  - Verify cold-start → normal mode transition
  - Verify invariant preservation across all modules
  - Produce final verification artifact

## Notes

- Tasks marked with `*` are optional property tests and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Verification gates (tasks 2, 4, 6, 8, 10) are independent gates requiring explicit execution — they are NOT auto-completed
- Property tests validate universal correctness properties from the design document
- Foundation (tasks 1–2) is DONE — all property tests passing
- Deferred requirements (Warning System, Advanced Hardenings, Meta-Governance) are tracked in `docs/future_framework_backlog.md`
- Req 31 (Cold-Start) is simplified per CTO directive: just "IF missing THEN init defaults AND observability mode"
- Total active tasks: 38 (down from 87 pre-freeze)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["3.1", "3.2", "3.3", "3.4", "3.6"] },
    { "id": 1, "tasks": ["3.5", "3.7"] },
    { "id": 2, "tasks": ["3.8", "3.9"] },
    { "id": 3, "tasks": ["5.1", "5.2", "5.3", "5.4"] },
    { "id": 4, "tasks": ["5.5", "5.6", "5.7", "5.8", "5.9", "5.10"] },
    { "id": 5, "tasks": ["7.1", "7.2", "7.3"] },
    { "id": 6, "tasks": ["7.4", "7.5"] },
    { "id": 7, "tasks": ["9.1", "9.4", "9.5"] },
    { "id": 8, "tasks": ["9.2", "9.3", "9.6"] }
  ]
}
```
