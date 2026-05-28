# Implementation Plan: Governance Runtime Enforcement

## Overview

This plan implements the governance runtime enforcement system in 6 phases following CTO-mandated phasing: Foundation (data contracts + actor model), CI Hardening, Enforcement Runtime (gates, lifecycle, boundary, warnings), Mutation Audit Ledger, Meta-Hardenings, and Final Integration. Each phase ends with a verification gate. All new modules go in `governance/`. Property-based tests use Hypothesis with `@settings(max_examples=100)`.

## Tasks

- [ ] 1. Foundation: Data Contracts and Actor Model
  - [ ] 1.1 Create `governance/actor_identity.py` with ActorType StrEnum and ActorIdentity dataclass
    - Implement `ActorType` StrEnum with 7 values: SYSTEM, CI, USER, ENGINE, MIGRATION, RUNTIME, HOT_RELOAD
    - Implement `ActorIdentity` dataclass with actor_type, actor_id, context dict, is_fallback boolean
    - Implement `from_environment()`, `ci_actor()`, `engine_actor()` class methods
    - Implement serialization to/from dict for YAML persistence
    - _Requirements: 33.1, 33.2, 33.3, 33.4, 33.5, 33.6_

  - [ ] 1.2 Create `governance/gate_framework.py` with GateResult and GateSummary dataclasses
    - Implement `GateResult` dataclass with gate_name, status, enforcement_action, duration_ms, details, timestamp, governance_policy_version, governance_state_provenance
    - Implement `GateSummary` dataclass with total_gates, passed, failed, blocked, timed_out, total_duration_ms, aggregate_state, git_sha, branch, runtime_integrity_hash, governance_overhead_percent
    - Implement serialization to/from dict for JSON/YAML round-trip
    - Implement `compute_aggregate_state()` logic: healthy/partial/degraded/collapsed
    - _Requirements: 5.5, 5.6, 26.1, 26.2, 26.3, 26.4, 32.1, 32.2, 32.6_

  - [ ] 1.3 Create `governance/fail_mode_registry.py` with FailMode StrEnum and FailModeRegistry class
    - Implement `FailMode` StrEnum with fail_open, fail_soft, fail_closed
    - Implement `FailModeRegistry` class loading from `.domainization/fail_mode_config.yaml`
    - Implement `get_fail_mode(component_name)` and `get_all_classifications()`
    - Implement `freeze()` and `is_frozen()` for self-disable protection (Req 49)
    - Implement `attempt_modification()` returning (allowed, reason) tuple
    - _Requirements: 29.1, 29.7, 49.1, 49.2, 49.4_

  - [ ] 1.4 Create `governance/state_provenance_tagger.py` with GovernanceProvenance StrEnum and StateProvenanceTagger
    - Implement `GovernanceProvenance` StrEnum with 6 values: authoritative, cached, fallback_derived, bootstrap_derived, partially_degraded, indeterminate
    - Implement `StateProvenanceTagger` with `tag()` and `get_current_provenance()` methods
    - _Requirements: 41.1, 41.2, 41.3, 41.4, 41.5, 41.6_

  - [ ] 1.5 Create `.domainization/fail_mode_config.yaml` configuration file
    - Define schema_version, component fail-mode classifications per the design
    - Include enforcement-mode-dependent fail modes for yaml_config_parser and lifecycle_enforcer
    - _Requirements: 29.7_


  - [ ]* 1.6 Write property test for ActorIdentity round-trip serialization
    - **Property 3: ActorIdentity Round-Trip Serialization**
    - **Validates: Requirements 33.6**
    - File: `tests/test_property_actor_identity_roundtrip.py`

  - [ ]* 1.7 Write property test for GateResult round-trip serialization
    - **Property 1: GateResult Round-Trip Serialization**
    - **Validates: Requirements 5.6, 26.4**
    - File: `tests/test_property_gate_result_roundtrip.py`

  - [ ]* 1.8 Write property test for Enforcement Mode round-trip
    - **Property 4: Enforcement Mode Round-Trip**
    - **Validates: Requirements 7.6**
    - File: `tests/test_property_enforcement_mode_roundtrip.py`

  - [ ]* 1.9 Write property test for Self-Disable Guard immutability
    - **Property 32: Self-Disable Guard Immutability**
    - **Validates: Requirements 49.1, 49.2, 49.4**
    - File: `tests/test_property_self_disable_guard.py`

- [ ] 2. Foundation Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/test_property_actor_identity_roundtrip.py tests/test_property_gate_result_roundtrip.py tests/test_property_enforcement_mode_roundtrip.py tests/test_property_self_disable_guard.py -v`
  - Verify all foundation modules import cleanly
  - Produce verification artifact

- [ ] 3. CI Pipeline Hardening
  - [ ] 3.1 Extend `.github/workflows/python-app.yml` with full test suite step
    - Add step: `python -m pytest tests/ -v --tb=short` with 60s time budget
    - Ensure step blocks merge on failure
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 3.2 Add all-directory syntax validation step to CI workflow
    - Add step: `python -m compileall` for engines/, runtime/, governance/, .domainization/src/, tests/
    - Use quiet mode, block merge on failure
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 3.3 Add YAML validation step to CI workflow
    - Add inline Python step to load and validate required keys in config.yaml, domain_registry.yaml, artifact_registry.yaml, lifecycle_state_machine.yaml
    - Block merge on parse failure, report file name and error
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ] 3.4 Add all-engine import validation step to CI workflow
    - Add step to import all 12 engines: allocation, report, regime, scoring, priority, scenario, decision, quality, delta, morning_briefing, visual, semantic
    - Block merge on import failure
    - _Requirements: 4.1, 4.2, 4.3_

  - [ ] 3.5 Create `governance/runtime_integrity_hash.py` with RuntimeIntegrityHash class
    - Implement `compute()` method: SHA-256 over deterministically sorted file contents
    - Implement `verify_against(expected_hash)` returning (match, details) tuple
    - Define TARGET_PATHS covering governance YAML, runtime/*.py, governance/*.py
    - _Requirements: 36.1, 36.2, 36.5, 36.6_

  - [ ] 3.6 Create `governance/hash_canonicalizer.py` with HashCanonicalizer class
    - Implement `normalize_line_endings()`: CRLF/CR → LF
    - Implement `normalize_encoding()`: → UTF-8
    - Implement `strip_trailing_whitespace()`: per-line strip
    - Implement `ensure_final_newline()`: exactly one trailing newline
    - Implement `canonicalize_yaml()`: parse → re-serialize with sorted keys
    - Implement `canonicalize_python()`: LF + UTF-8 + strip trailing whitespace
    - Implement `canonicalize_file()`: auto-detect by extension
    - Implement `compute_hash()`: SHA-256 over sorted canonicalized content
    - _Requirements: 48.1, 48.2, 48.3, 48.4_

  - [ ] 3.7 Add runtime integrity hash step to CI workflow
    - Add informational step computing and persisting the hash as CI artifact
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

- [ ] 4. CI Hardening Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify CI workflow YAML is valid and all new steps are present
  - Produce verification artifact


- [ ] 5. Enforcement Runtime: Gate Framework, Lifecycle, and Boundary
  - [ ] 5.1 Implement GateFramework class in `governance/gate_framework.py`
    - Implement `__init__(config, enforcement_mode)` loading gate configurations
    - Implement `execute_gate(gate_name, check_fn, time_budget_ms)` with timeout handling
    - Implement `execute_all_gates()` producing GateSummary
    - Implement enforcement mode logic: observability→warn, soft→block if blocking_in_soft, hard→block if blocking_in_soft or blocking_in_hard
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4_

  - [ ] 5.2 Create `governance/lifecycle_enforcer.py` with LifecycleEnforcer class
    - Implement `__init__(state_machine_path, enforcement_mode)` loading lifecycle YAML
    - Implement `validate_transition(artifact_id, artifact_type, from_state, to_state)` against state machine
    - Implement `is_read_only(artifact_type, current_state)` checking read_only_states
    - Implement `is_regenerable(artifact_type, current_state)` checking regenerable_states
    - Implement `enforce_transition()`, `enforce_read_only()`, `enforce_regenerable()` producing GateResult
    - Respect enforcement mode: observability→warn, soft→reject with warning, hard→reject with error
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.1, 9.2, 9.3, 9.4, 10.1, 10.2, 10.3, 10.4_

  - [ ] 5.3 Create `governance/boundary_enforcer.py` with BoundaryEnforcer class
    - Implement `__init__(artifact_registry_path, domain_registry_path, enforcement_mode)`
    - Implement `check_write_permission(writing_domain, artifact_id)` checking allowed_writers
    - Implement `check_cannot_own(domain_id, artifact_type)` checking cannot_own constraints
    - Implement `enforce_write()` and `enforce_domain_assignment()` producing GateResult
    - Implement `detect_cross_domain_interaction()` for cross-domain logging
    - Handle `ALL` in allowed_writers as universal permission
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 17.1, 17.2, 17.3, 17.4, 18.1, 18.2, 18.3, 18.4, 19.1, 19.2, 19.3, 19.4_

  - [ ] 5.4 Create `governance/recursion_protector.py` with RecursionProtector class
    - Define GOVERNANCE_META_ARTIFACTS frozenset (ledger, baselines, gate results)
    - Implement `is_governance_meta(artifact_id)` classification
    - Implement `should_apply_governance(artifact_id, operation)` with MAX_RECURSION_DEPTH=1
    - Implement `check_recursion_depth(current_depth)` guard
    - _Requirements: 30.1, 30.2, 30.3, 30.4, 30.5, 30.6_

  - [ ] 5.5 Create `governance/cold_start_handler.py` with ColdStartHandler class
    - Implement `is_cold_start()` checking ledger, baseline, gate history existence
    - Implement `initialize(actor)` creating bootstrap entries
    - Implement `check_stuck_cold_start(consecutive_runs)` with 3-run threshold
    - Implement `get_cold_start_event()` producing LedgerEntry
    - Cold-start forces observability regardless of configured mode
    - _Requirements: 31.1, 31.2, 31.3, 31.4, 31.5, 31.6, 31.7, 31.8, 31.9_

  - [ ] 5.6 Create `governance/deadlock_preventer.py` with DeadlockPreventer class
    - Implement `detect_deadlock(rejected_artifact_id, violation_source_artifact_id)` using same-artifact matching
    - Implement `emergency_override(artifact_id, violation, justification, actor)` with USER/MIGRATION restriction
    - Implement `check_override_frequency(window_days=7)` with 3-override threshold
    - _Requirements: 35.1, 35.2, 35.3, 35.4, 35.5, 35.6_

  - [ ]* 5.7 Write property test for Observability Mode Never Blocks
    - **Property 5: Observability Mode Never Blocks**
    - **Validates: Requirements 5.2, 7.5, 24.4, 25.8**
    - File: `tests/test_property_observability_never_blocks.py`

  - [ ]* 5.8 Write property test for Enforcement Mode Gate Blocking Correctness
    - **Property 6: Enforcement Mode Gate Blocking Correctness**
    - **Validates: Requirements 5.1, 5.3, 5.4**
    - File: `tests/test_property_gate_blocking_correctness.py`

  - [ ]* 5.9 Write property test for Lifecycle Transition Validation
    - **Property 7: Lifecycle Transition Validation Correctness**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
    - File: `tests/test_property_lifecycle_transition_validation.py`

  - [ ]* 5.10 Write property test for Read-Only State Protection
    - **Property 8: Read-Only State Protection**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**
    - File: `tests/test_property_read_only_protection.py`

  - [ ]* 5.11 Write property test for Regenerable State Gate
    - **Property 9: Regenerable State Gate**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**
    - File: `tests/test_property_regenerable_state_gate.py`

  - [ ]* 5.12 Write property test for Boundary Enforcement Correctness
    - **Property 10: Boundary Enforcement Correctness**
    - **Validates: Requirements 16.1, 16.2, 16.3, 16.4, 16.5**
    - File: `tests/test_property_boundary_enforcement.py`

  - [ ]* 5.13 Write property test for Cannot-Own Constraint Consistency
    - **Property 11: Cannot-Own Constraint Consistency**
    - **Validates: Requirements 17.1, 17.2, 17.3, 17.4**
    - File: `tests/test_property_cannot_own_consistency.py`

  - [ ]* 5.14 Write property test for Aggregate Governance State Determinism
    - **Property 17: Aggregate Governance State Determinism**
    - **Validates: Requirements 32.1, 32.2, 32.4, 32.6**
    - File: `tests/test_property_aggregate_state_determinism.py`

  - [ ]* 5.15 Write property test for Governance Recursion Depth Bound
    - **Property 16: Governance Recursion Depth Bound**
    - **Validates: Requirements 30.1, 30.2, 30.3, 30.4, 30.5, 30.6**
    - File: `tests/test_property_recursion_depth_bound.py`

  - [ ]* 5.16 Write property test for Cold-Start Forces Observability
    - **Property 22: Cold-Start Forces Observability**
    - **Validates: Requirements 31.7**
    - File: `tests/test_property_cold_start_observability.py`

  - [ ]* 5.17 Write property test for Deadlock Detection Correctness
    - **Property 20: Deadlock Detection Correctness**
    - **Validates: Requirements 35.1, 35.4**
    - File: `tests/test_property_deadlock_detection.py`

- [ ] 6. Enforcement Runtime (Gates + Lifecycle + Boundary) Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify gate framework, lifecycle enforcer, boundary enforcer, recursion protector, cold-start handler, deadlock preventer all import and integrate
  - Produce verification artifact


- [ ] 7. Mutation Audit Ledger and Warning Governance
  - [ ] 7.1 Create `governance/mutation_audit_ledger.py` with LedgerEntry dataclass and MutationAuditLedger class
    - Implement `LedgerEntry` dataclass with entry_id, event_type, timestamp, actor, governance_policy_version, severity, details
    - Implement `MutationAuditLedger.__init__(ledger_path)` with file creation on missing
    - Implement `append(entry)` with append-only YAML persistence
    - Implement `query_by_time_range(start, end)` and `query_by_event_type(event_type)`
    - Implement `recover_from_corruption()` creating new ledger on failure
    - Implement `is_cold_start()` checking ledger existence
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 13.1, 13.2, 13.3, 13.4, 13.5, 14.1, 14.2, 14.3, 15.1, 15.2, 15.3_

  - [ ] 7.2 Create `governance/policy_versioner.py` with PolicyVersioner class
    - Implement `compute_version()` as SHA-256 of combined sorted governance file contents
    - Implement `detect_change(previous_version)` returning boolean
    - Implement `get_current_version()` caching the computed hash
    - Define GOVERNANCE_FILES list per design
    - _Requirements: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6_

  - [ ] 7.3 Create `governance/warning_governor.py` with GovernanceWarning dataclass and WarningGovernor class
    - Implement `GovernanceWarning` dataclass with code, artifact_id, message, severity, source, timestamp
    - Implement `WarningGovernor.__init__(baseline_path, enforcement_mode)`
    - Implement `process_warnings(warnings)` producing WarningReport
    - Implement `deduplicate(warnings)` with (code, artifact_id) key, 50-unique cap
    - Implement `classify_against_baseline(warning)` returning known/new/stale
    - Implement `detect_stale_baseline_entries(emitted_warnings)` for cleanup
    - Implement `compute_trend(current_count, previous_count)` with 20% threshold alert
    - _Requirements: 20.1, 20.2, 20.3, 20.4, 21.1, 21.2, 21.3, 21.4, 22.1, 22.2, 22.3, 22.4, 23.1, 23.2, 23.3, 23.4, 24.1, 24.2, 24.3, 24.4, 24.5_

  - [ ] 7.4 Create `.domainization/warning_baseline.yaml` initial baseline file
    - Define schema_version, last_updated, empty entries list
    - Include added_date and expires_after_days fields per design
    - _Requirements: 20.1, 45.1_

  - [ ] 7.5 Create `governance/shadow_authority_detector.py` with ShadowAuthorityDetector class
    - Implement `__init__(artifact_registry_path)` loading registry
    - Implement `check_write_authority(writing_module, target_artifact_id)` returning boolean
    - Implement `record_shadow_event()` producing structured event dict
    - Implement `check_threshold(events_this_run)` with 5-unique-path threshold
    - _Requirements: 40.1, 40.2, 40.3, 40.4, 40.5_

  - [ ]* 7.6 Write property test for LedgerEntry round-trip serialization
    - **Property 2: LedgerEntry Round-Trip Serialization**
    - **Validates: Requirements 11.4, 12.5, 13.3**
    - File: `tests/test_property_ledger_entry_roundtrip.py`

  - [ ]* 7.7 Write property test for Ledger Append-Only Chronological Ordering
    - **Property 21: Ledger Append-Only Chronological Ordering**
    - **Validates: Requirements 13.2**
    - File: `tests/test_property_ledger_chronological_order.py`

  - [ ]* 7.8 Write property test for Warning Deduplication Correctness
    - **Property 12: Warning Deduplication Correctness**
    - **Validates: Requirements 22.1, 22.2, 22.3, 22.4**
    - File: `tests/test_property_warning_deduplication.py`

  - [ ]* 7.9 Write property test for Warning Baseline Suppression Idempotence
    - **Property 13: Warning Baseline Suppression Idempotence**
    - **Validates: Requirements 20.2, 20.3, 28.8**
    - File: `tests/test_property_baseline_suppression_idempotence.py`

  - [ ]* 7.10 Write property test for Warning Trend Alert Threshold
    - **Property 14: Warning Trend Alert Threshold**
    - **Validates: Requirements 23.3, 23.4**
    - File: `tests/test_property_trend_alert_threshold.py`

  - [ ]* 7.11 Write property test for Severity Ordering Preservation
    - **Property 15: Severity Ordering Preservation**
    - **Validates: Requirements 24.1, 24.2, 24.3, 24.5, 25.4**
    - File: `tests/test_property_severity_ordering.py`

  - [ ]* 7.12 Write property test for Policy Version Determinism
    - **Property 18: Policy Version Determinism**
    - **Validates: Requirements 34.1, 34.5, 34.6**
    - File: `tests/test_property_policy_version_determinism.py`

  - [ ]* 7.13 Write property test for Shadow Authority Detection Threshold
    - **Property 24: Shadow Authority Detection Threshold**
    - **Validates: Requirements 40.1, 40.3, 40.5**
    - File: `tests/test_property_shadow_authority_threshold.py`

- [ ] 8. Mutation Audit Ledger and Warning Governance Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify ledger persistence, warning governance, shadow authority detection all function correctly
  - Produce verification artifact


- [ ] 9. Meta-Hardenings: Complexity, Rotation, Decay, Scoped Versioning, Temporary Authority
  - [ ] 9.1 Create `governance/complexity_monitor.py` with GovernanceComplexityMonitor class
    - Implement `ComplexityMetrics` dataclass with total_governance_modules, total_config_files, total_state_categories, total_enforcement_paths, budget_exceeded, exceeded_dimensions
    - Implement `compute_metrics()` scanning governance/ directory and .domainization/ configs
    - Implement `is_over_budget()` checking against thresholds from config.yaml
    - Implement `check_addition(category)` validating whether a new concept can be added
    - Budget thresholds: max_governance_modules=25, max_config_files=10, max_state_categories=60, max_enforcement_paths=15
    - _Requirements: 43.1, 43.2, 43.3, 43.4, 43.5_

  - [ ] 9.2 Create `governance/ledger_rotation.py` with LedgerRotationManager class
    - Implement `__init__(ledger_dir)` with MAX_ENTRIES=1000, MAX_FILE_SIZE_KB=500
    - Implement `needs_rotation()` checking entry count and file size
    - Implement `rotate()` archiving current ledger with timestamp suffix, creating new active ledger with previous archive hash as first entry
    - Implement `list_archived_ledgers()` returning chronological list
    - Implement `query_across_all(event_type, start, end)` transparent cross-archive queries
    - Implement `compute_chain_hash()` for hash continuity verification
    - _Requirements: 44.1, 44.2, 44.3, 44.4, 44.5, 44.6_

  - [ ] 9.3 Create `governance/baseline_decay.py` with BaselineDecayManager class
    - Implement `BaselineEntry` dataclass with code, artifact_id, reason, added_date, expires_after_days, revalidation_reason
    - Implement `__init__(baseline_path, reference_date)` with DEFAULT_EXPIRY_DAYS=90
    - Implement `get_expired_entries()` comparing added_date + expires_after_days against reference_date
    - Implement `get_expiring_soon(within_days=14)` for early warning
    - Implement `revalidate(code, artifact_id, reason)` resetting added_date
    - Implement `compute_health()` returning total, expired, expiring_soon, avg_age
    - Implement `is_maintenance_overdue()` with 30% expired threshold
    - _Requirements: 45.1, 45.2, 45.3, 45.4, 45.5_

  - [ ] 9.4 Create `governance/scoped_policy_versioner.py` with ScopedPolicyVersioner class
    - Define POLICY_DOMAINS mapping: lifecycle, boundary, severity, warning, gate
    - Implement `compute_scoped_version(domain)` as SHA-256 of domain-specific files
    - Implement `compute_global_version()` as SHA-256 of all scoped versions combined
    - Implement `detect_scoped_changes(previous_versions)` returning list of changed domains
    - Implement `get_all_versions()` returning domain to hash mapping
    - _Requirements: 46.1, 46.2, 46.3, 46.4, 46.5_

  - [ ] 9.5 Create `governance/temporary_authority.py` with TemporaryAuthorityManager class
    - Implement `TemporaryAuthority` dataclass with target_pattern, granted_domain, expires_at, reason, declaring_actor, created_at
    - Implement `declare()` with MAX_DURATION_DAYS=7 validation, USER/MIGRATION actor restriction
    - Implement `is_authorized(artifact_id, writing_domain)` checking active declarations with glob matching
    - Implement `get_active_declarations()` filtering expired entries
    - Implement `expire_stale()` returning and removing expired declarations
    - Implement `revoke(target_pattern, actor)` with audit logging
    - _Requirements: 47.1, 47.2, 47.3, 47.4, 47.5, 47.6_

  - [ ] 9.6 Create `governance/self_disable_guard.py` with SelfDisableGuard class
    - Implement `lock_enforcement_state(fail_mode_config, enforcement_mode)` freezing state at pipeline start
    - Implement `attempt_modification(component_name, target_field, new_value)` returning (allowed, reason)
    - Implement `detect_circular_weakening(modification_chain)` detecting self-referential weakening
    - Implement `is_locked()` returning current lock state
    - _Requirements: 49.1, 49.2, 49.3, 49.4_

  - [ ] 9.7 Create `governance/performance_budget_monitor.py` with PerformanceBudgetMonitor class
    - Implement `__init__()` with BUDGET_PERCENT=15.0
    - Implement `start_pipeline_timer()` and `start_governance_timer()`/`stop_governance_timer()`
    - Implement `is_over_budget()` comparing governance time to pipeline time
    - Implement `get_overhead_percent()` computing (governance_time / pipeline_time) * 100
    - Implement `get_priority_order()` returning fail_closed > fail_soft > fail_open > informational
    - _Requirements: 38.1, 38.2, 38.3, 38.4, 38.5, 38.6_

  - [ ] 9.8 Create `governance/transient_artifact_promoter.py` with TransientArtifactPromoter class
    - Implement `detect_boundary_crossing(artifact_name, is_persisted, is_passed_downstream)` returning boolean
    - Implement `promote_to_canonical(artifact_name, reason, actor)` with ledger recording
    - Implement `validate_canonical_requirements(artifact_name)` checking schema and provenance
    - Respect enforcement mode for blocking vs warning behavior
    - _Requirements: 37.1, 37.2, 37.3, 37.4, 37.5_

  - [ ]* 9.9 Write property test for Governance Overhead Budget Enforcement
    - **Property 25: Governance Overhead Budget Enforcement**
    - **Validates: Requirements 38.1, 38.3, 38.4**
    - File: `tests/test_property_overhead_budget_enforcement.py`

  - [ ]* 9.10 Write property test for Governance Complexity Budget Enforcement
    - **Property 26: Governance Complexity Budget Enforcement**
    - **Validates: Requirements 43.1, 43.2, 43.4**
    - File: `tests/test_property_complexity_budget_enforcement.py`

  - [ ]* 9.11 Write property test for Ledger Rotation Hash Continuity
    - **Property 27: Ledger Rotation Hash Continuity**
    - **Validates: Requirements 44.3, 44.4, 44.5**
    - File: `tests/test_property_ledger_rotation_hash_continuity.py`

  - [ ]* 9.12 Write property test for Baseline Entry Expiration Determinism
    - **Property 28: Baseline Entry Expiration Determinism**
    - **Validates: Requirements 45.1, 45.2, 45.3**
    - File: `tests/test_property_baseline_expiration_determinism.py`

  - [ ]* 9.13 Write property test for Scoped Policy Version Independence
    - **Property 29: Scoped Policy Version Independence**
    - **Validates: Requirements 46.1, 46.4, 46.5**
    - File: `tests/test_property_scoped_policy_version_independence.py`

  - [ ]* 9.14 Write property test for Temporary Authority Bounded Duration
    - **Property 30: Temporary Authority Bounded Duration**
    - **Validates: Requirements 47.3, 47.4**
    - File: `tests/test_property_temporary_authority_bounded_duration.py`

  - [ ]* 9.15 Write property test for Bounded Fail-Soft Degradation Escalation
    - **Property 23: Bounded Fail-Soft Degradation Escalation**
    - **Validates: Requirements 42.2, 42.3**
    - File: `tests/test_property_bounded_degradation_escalation.py`

- [ ] 10. Meta-Hardenings Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify all meta-hardening modules import and integrate with foundation components
  - Produce verification artifact

- [ ] 11. Integration Wiring and Enforcement Mode Configuration
  - [ ] 11.1 Wire enforcement mode reading from `.domainization/config.yaml` into all enforcement components
    - Add `governance_enforcement` section to config.yaml with mode, transition criteria, gate configurations
    - Wire GateFramework, LifecycleEnforcer, BoundaryEnforcer, WarningGovernor to read enforcement_mode from config
    - Implement enforcement mode change detection and ledger recording
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ] 11.2 Wire MutationAuditLedger into all enforcement components
    - Connect GateFramework to log gate results to ledger
    - Connect LifecycleEnforcer to log transitions to ledger
    - Connect BoundaryEnforcer to log violations to ledger
    - Connect WarningGovernor to log trend data to ledger
    - Connect DeadlockPreventer to log overrides to ledger
    - _Requirements: 11.1, 11.2, 11.3, 27.1, 27.2, 27.3_

  - [ ] 11.3 Wire ColdStartHandler, RecursionProtector, and SelfDisableGuard into pipeline initialization
    - Cold-start check runs first, forces observability if detected
    - SelfDisableGuard locks enforcement state after config load
    - RecursionProtector wraps all governance operations
    - _Requirements: 31.7, 30.1, 49.1_

  - [ ] 11.4 Wire PerformanceBudgetMonitor into pipeline execution
    - Start pipeline timer at orchestrator entry
    - Wrap each governance operation with governance timer
    - Skip non-critical checks when budget exceeded
    - _Requirements: 38.1, 38.2, 38.3, 38.4_

  - [ ] 11.5 Wire TemporaryAuthorityManager into BoundaryEnforcer and ShadowAuthorityDetector
    - BoundaryEnforcer checks temporary authorities before rejecting writes
    - ShadowAuthorityDetector classifies temporary-authorized writes as `authorized_temporary`
    - _Requirements: 47.1, 47.2, 47.3_

  - [ ] 11.6 Wire BaselineDecayManager into WarningGovernor
    - Check expired entries during warning processing
    - Escalate expired baseline entries to visible warnings
    - _Requirements: 45.2, 45.4, 45.5_

  - [ ] 11.7 Wire LedgerRotationManager into MutationAuditLedger
    - Check rotation needed before each append
    - Rotate transparently when threshold exceeded
    - _Requirements: 44.1, 44.2, 44.5_

  - [ ] 11.8 Wire ScopedPolicyVersioner into GateResult and LedgerEntry production
    - Include both global and relevant scoped versions in gate results
    - Emit SCOPED_POLICY_CHANGE events when individual domains change
    - _Requirements: 46.3, 46.4_

  - [ ] 11.9 Wire GovernanceComplexityMonitor into health reporting
    - Compute complexity metrics during pipeline execution
    - Emit CRITICAL event when budget exceeded
    - _Requirements: 43.2, 43.3_

  - [ ] 11.10 Implement bounded fail-soft degradation tracking
    - Track consecutive degraded runs per component
    - Escalate to CRITICAL after 5 consecutive degraded runs
    - Emit GOVERNANCE_DEGRADATION_PERSISTENT after 10 consecutive runs
    - _Requirements: 42.1, 42.2, 42.3, 42.4, 42.5_

  - [ ] 11.11 Implement invariant preservation checks
    - Verify INV-1 through INV-10 are not violated by new enforcement logic
    - Ensure observability mode never blocks (INV-8)
    - Ensure pipeline always completes (INV-7)
    - _Requirements: 25.1, 25.2, 25.3, 25.4, 25.5, 25.6, 25.7, 25.8, 25.9, 25.10_

  - [ ] 11.12 Update artifact registry with all new governance modules
    - Register all new governance/*.py files in .domainization/artifact_registry.yaml
    - Register new config files (fail_mode_config.yaml, warning_baseline.yaml, mutation_audit_ledger.yaml)
    - Set appropriate primary_domain, allowed_writers, lifecycle_state for each
    - _Requirements: 39.1, 39.2, 39.3, 39.4, 39.5_

- [ ] 12. Final Integration Verification — Output Contract
  - Ensure all tests pass, ask the user if questions arise.
  - Run: `.venv/bin/python -m pytest tests/ -v --tb=short`
  - Verify all 24 governance modules import and integrate end-to-end
  - Verify enforcement mode transitions work across all components
  - Verify ledger persistence survives restart (write, stop, read back)
  - Produce final verification artifact with full metrics

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Verification gates (tasks 2, 4, 6, 8, 10, 12) are independent gates requiring explicit execution per steering rule
- Property tests validate universal correctness properties from the design document (32 total)
- Unit tests validate specific examples and edge cases
- All new modules go in `governance/` directory per HARDENING 10 (no plugin architecture)
- Python 3.13.7 via `.venv/bin/python`; tests via `.venv/bin/python -m pytest`
- Property-based tests use Hypothesis with `@settings(max_examples=100)`
- Registry updates required for every new file (task 11.12)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.4", "1.5"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["1.6", "1.7", "1.8", "1.9"] },
    { "id": 3, "tasks": ["3.1", "3.2", "3.3", "3.4", "3.6"] },
    { "id": 4, "tasks": ["3.5", "3.7"] },
    { "id": 5, "tasks": ["3.8", "3.9"] },
    { "id": 6, "tasks": ["5.1", "5.2", "5.4", "5.5"] },
    { "id": 7, "tasks": ["5.3", "5.6"] },
    { "id": 8, "tasks": ["5.7", "5.8", "5.9", "5.10", "5.11", "5.12", "5.13", "5.14", "5.15", "5.16", "5.17"] },
    { "id": 9, "tasks": ["7.1", "7.2", "7.3", "7.4"] },
    { "id": 10, "tasks": ["7.5"] },
    { "id": 11, "tasks": ["7.6", "7.7", "7.8", "7.9", "7.10", "7.11", "7.12", "7.13"] },
    { "id": 12, "tasks": ["9.1", "9.3", "9.4", "9.7"] },
    { "id": 13, "tasks": ["9.2", "9.5", "9.6", "9.8"] },
    { "id": 14, "tasks": ["9.9", "9.10", "9.11", "9.12", "9.13", "9.14", "9.15"] },
    { "id": 15, "tasks": ["11.1", "11.3"] },
    { "id": 16, "tasks": ["11.2", "11.4", "11.5", "11.6", "11.7", "11.8", "11.9"] },
    { "id": 17, "tasks": ["11.10", "11.11", "11.12"] }
  ]
}
```
