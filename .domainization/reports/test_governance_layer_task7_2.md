# Test Governance Layer — MoneyHorst Inventory Report

**Task:** 7.2 MoneyHorst Test Governance Layer  
**Date:** 2026-06-01  
**Purpose:** Regression-safe extension governance for future Engines, Signals, and Reports  
**Scope:** Follow-up governance documentation (NOT an execution gate)

---

## 1. Fresh Baseline Discovery

**Command:** `.venv/bin/python -m pytest tests/ --collect-only -q`  
**Result:** 494 tests collected in 6.99s  
**Discovery method:** Dynamic (independent of Task 6)

---

## 2. Test File Inventory and Classification

### 2.1 Property Tests (Hypothesis-based correctness properties)

| File | Test Count | Domain Coverage |
|------|:---:|---|
| `tests/test_influence_graph_properties.py` | 8 | Governance (influence graph) |
| `tests/test_deployment_authority_properties.py` | 10 | Governance (deployment authority) |
| `tests/test_transition_cooldown_properties.py` | 10 | Governance (transition cooldown) |
| `tests/test_domain_lifecycle_properties.py` | 6 | Governance (domain lifecycle) |
| `tests/test_property_actor_identity_roundtrip.py` | 2 | Governance (actor identity) |
| `tests/test_property_canonical_boundary_enforcement.py` | 6 | Governance (canonical boundary) |
| `tests/test_property_chain_provenance_integrity.py` | 5 | Runtime (chain provenance) |
| `tests/test_property_confidence_degradation.py` | 6 | Runtime (confidence policy) |
| `tests/test_property_data_availability_summary.py` | 3 | Report (data availability) |
| `tests/test_property_deployment_matrix_partition.py` | 7 | Runtime (deployment matrix) |
| `tests/test_property_enforcement_mode_roundtrip.py` | 4 | Governance (enforcement modes) |
| `tests/test_property_forbidden_flow_detection.py` | 5 | Architecture (pipeline flows) |
| `tests/test_property_gate_result_roundtrip.py` | 2 | Governance (gate framework) |
| `tests/test_property_governance_event_completeness.py` | 5 | Governance (events) |
| `tests/test_property_graceful_degradation.py` | 5 | Runtime (degradation) |
| `tests/test_property_non_determinism_injection.py` | 6 | Runtime (determinism) |
| `tests/test_property_pipeline_determinism.py` | 4 | Runtime (pipeline) |
| `tests/test_property_pipeline_state_aggregation.py` | 4 | Runtime (state aggregation) |
| `tests/test_property_portfolio_watchlist_separation.py` | 7 | Report (portfolio/watchlist) |
| `tests/test_property_position_transition_rendering.py` | 6 | Report (position transitions) |
| `tests/test_property_provenance_parseability.py` | 8 | Governance (provenance) |
| `tests/test_property_reasoning_object_schema.py` | 6 | Runtime (reasoning objects) |
| `tests/test_property_reasoning_object_section_mapping.py` | 3 | Report (section mapping) |
| `tests/test_property_report_structure_invariant.py` | 3 | Report (structure) |
| `tests/test_property_report_value_validation.py` | 8 | Report (value validation) |
| `tests/test_property_run_context_temporal_consistency.py` | 4 | Runtime (temporal consistency) |
| `tests/test_property_schema_version_compatibility.py` | 5 | Governance (schema versions) |
| `tests/test_property_section_completeness.py` | 5 | Report (section completeness) |
| `tests/test_property_self_disable_guard.py` | 3 | Governance (self-disable) |
| `tests/test_property_semantic_coverage_invariant.py` | 5 | Semantics (coverage) |
| `tests/test_property_semantic_delta_correctness.py` | 5 | Semantics (delta) |
| `tests/test_property_semantic_state_round_trip.py` | 4 | Runtime (semantic state) |
| `tests/test_property_sunset_governance_behavior.py` | 6 | Governance (sunset) |

**Total property test files:** 33  
**Total property tests:** 176


### 2.2 Non-Interference Tests (delta-layer guarantees)

| File | Test Count | Purpose |
|------|:---:|---|
| `tests/test_delta_non_interference.py` | 32 | Verifies delta layer does not regress existing enforcement modes, fail modes, ledger schema, domain registry schema, or read-only consumption of Actor_Identity/Policy_Versioner |

**Total non-interference test files:** 1

---

### 2.3 Integration Tests (cross-module interaction)

| File | Test Count | Purpose |
|------|:---:|---|
| `tests/test_delta_init.py` | 12 | Verifies initialization sequence: InfluenceGraph → DeploymentAuthority → TransitionCooldown → DomainLifecycleManager; CRITICAL events halt init; fail_soft components degrade gracefully |

**Total integration test files:** 1

---

### 2.4 Unit Tests (isolated module behavior)

| File | Test Count | Module Under Test |
|------|:---:|---|
| `tests/test_influence_graph.py` | 14 | `governance/influence_graph.py` |
| `tests/test_deployment_authority.py` | 22 | `governance/deployment_authority.py` |
| `tests/test_transition_cooldown.py` | 20 | `governance/transition_cooldown.py` |
| `tests/test_domain_lifecycle.py` | 22 | `governance/domain_lifecycle.py` |
| `tests/test_audit_ledger_verification.py` | 20 | `governance/mutation_audit_ledger.py` |
| `tests/test_boundary_shadow_ledger_wiring.py` | 9 | Boundary/shadow/ledger wiring |
| `tests/test_cold_start_handler.py` | 22 | `governance/cold_start_handler.py` |
| `tests/test_deterministic_ordering_enforcement.py` | 14 | Deterministic ordering |
| `tests/test_enforcement_config_loader.py` | 23 | `governance/enforcement_config_loader.py` |
| `tests/test_enforcement_runtime_verification.py` | 14 | Enforcement runtime integration |
| `tests/test_lifecycle_audit_wiring.py` | 14 | Lifecycle/audit wiring |
| `tests/test_ontology_growth_observer.py` | 21 | `governance/ontology_growth_observer.py` |
| `tests/test_pipeline_initializer.py` | 16 | `governance/pipeline_initializer.py` |
| `tests/test_policy_versioner.py` | 16 | `governance/policy_versioner.py` |
| `tests/test_sunset_governance.py` | 27 | `governance/sunset_governance.py` |

**Total unit test files (in `tests/`):** 15

---

### 2.5 Unclassified / Verification Scripts

| File | Classification | Explanation |
|------|---|---|
| `tests/verify_ledger_integration.py` | `unclassified` — verification script | Not a standard test module; appears to be a manual verification script for ledger integration. Collected by pytest but serves a different purpose than automated regression tests. |
| `tests/conftest.py` | N/A — fixture file | Pytest configuration/fixtures, not a test file |

---

## 3. Engine Test Status Inventory

### 3.1 Engines in `engines/` Directory (14 engines)

| Engine File | Domain | Has Dedicated Test? | Test Location |
|---|---|:---:|---|
| `engines/allocation_engine.py` | SIGNALS | NO | — |
| `engines/attribution_engine.py` | SIGNALS | NO | — |
| `engines/regime_engine.py` | SIGNALS | NO | — |
| `engines/scoring_engine.py` | SIGNALS | NO | — |
| `engines/semantic_engine.py` | SEMANTICS | NO | — |
| `engines/decision_engine.py` | REASONING | NO | — |
| `engines/quality_engine.py` | REASONING | NO | — |
| `engines/priority_engine.py` | REASONING | NO | — |
| `engines/report_engine.py` | REPORT | YES | `engines/test_report_engine.py` |
| `engines/morning_briefing_engine.py` | REPORT | NO | — |
| `engines/delta_engine.py` | REPORT | NO | — |
| `engines/scenario_engine.py` | SIM | NO | — |
| `engines/visual_engine.py` | ARCH | NO | — |
| `engines/engine_registry.py` | ARCH | NO | — |
| `engines/engine_runner.py` | ARCH | NO | — |
| `engines/pipeline_orchestrator.py` | ARCH | YES | `engines/test_pipeline_orchestrator.py` |

### 3.2 Engine Test Files (co-located in `engines/`)

| Test File | Tests For | Category |
|---|---|---|
| `engines/test_report_engine.py` | `report_engine.py` | Unit + integration |
| `engines/test_pipeline_orchestrator.py` | `pipeline_orchestrator.py` | Unit + integration |
| `engines/test_degradation_propagation.py` | Cross-engine degradation propagation | Integration |
| `engines/test_report_engine_portfolio_watchlist.py` | Report engine portfolio/watchlist blocks | Unit |
| `engines/test_hardening_5_daily_report.py` | Full pipeline end-to-end (Hardening 5) | Integration |

**Note:** Engine test files in `engines/` are NOT collected by `pytest tests/` — they require explicit path inclusion (e.g., `pytest engines/`).


---

## 4. Signal Test Status Inventory

### 4.1 Signal Domain Structure

**No dedicated `signals/` directory exists** in the repository. Signal generation is handled by engines in the `engines/` directory that belong to the SIGNALS domain:

| Signal Engine | File | Has Dedicated Test? |
|---|---|:---:|
| Allocation Engine | `engines/allocation_engine.py` | NO |
| Attribution Engine | `engines/attribution_engine.py` | NO |
| Regime Engine | `engines/regime_engine.py` | NO |
| Scoring Engine | `engines/scoring_engine.py` | NO |

### 4.2 Signal-Related Property Tests

The following property tests cover signal-related behavior indirectly:

| Test File | Signal Relevance |
|---|---|
| `tests/test_property_semantic_delta_correctness.py` | Tests signal ID delta computation |
| `tests/test_property_chain_provenance_integrity.py` | Tests signal engine provenance in chain |
| `tests/test_property_semantic_coverage_invariant.py` | Tests semantic state coverage (consumes signals) |

### 4.3 Signal Domain Test Coverage Assessment

**Direct signal engine unit tests: NONE**  
Signal engines (allocation, attribution, regime, scoring) have zero dedicated test files. Their correctness is only indirectly validated through downstream property tests that consume their output format.

---

## 5. Runtime Module Test Status

### 5.1 Runtime Test Files (co-located in `runtime/`)

| Test File | Module Under Test | Category |
|---|---|---|
| `runtime/test_chain_validator.py` | `runtime/chain_validator.py` | Unit |
| `runtime/test_confidence_policy.py` | `runtime/confidence_policy.py` | Unit |
| `runtime/test_deployment_matrix.py` | `runtime/deployment_matrix.py` | Unit |
| `runtime/test_pipeline_result.py` | `runtime/pipeline_result.py` | Unit |
| `runtime/test_reasoning_object.py` | `runtime/reasoning_object.py` | Unit |
| `runtime/test_run_context.py` | `runtime/run_context.py` | Unit |
| `runtime/test_runtime_state_model.py` | `runtime/runtime_state_model.py` | Unit |
| `runtime/test_semantic_state_store.py` | `runtime/semantic_state_store.py` | Unit |
| `runtime/test_severity_taxonomy.py` | `runtime/severity_taxonomy.py` | Unit |

**Note:** Runtime test files are co-located and NOT collected by `pytest tests/` — they require explicit path inclusion (e.g., `pytest runtime/`).

---

## 6. Governance Module Test Status

### 6.1 Governance Test Files (co-located in `governance/`)

| Test File | Module Under Test | Category |
|---|---|---|
| `governance/test_canonical_boundary.py` | `governance/canonical_boundary.py` | Unit |
| `governance/test_provenance_schema.py` | `governance/provenance_schema.py` | Unit |
| `governance/test_schema_version_registry.py` | `governance/schema_version_registry.py` | Unit |

**Note:** Governance co-located tests are NOT collected by `pytest tests/` — they require explicit path inclusion.

---

## 7. Coverage Gaps

### 7.1 Critical Gaps — Engines Without Tests

| Engine | Domain | Gap Severity | Notes |
|---|---|:---:|---|
| `allocation_engine.py` | SIGNALS | HIGH | Core signal generation, no unit tests |
| `attribution_engine.py` | SIGNALS | HIGH | Core signal generation, no unit tests |
| `regime_engine.py` | SIGNALS | HIGH | Core signal generation, no unit tests |
| `scoring_engine.py` | SIGNALS | HIGH | Core signal generation, no unit tests |
| `semantic_engine.py` | SEMANTICS | HIGH | Core semantic interpretation, no unit tests |
| `decision_engine.py` | REASONING | HIGH | Core reasoning, no unit tests |
| `quality_engine.py` | REASONING | MEDIUM | Reasoning quality, no unit tests |
| `priority_engine.py` | REASONING | MEDIUM | Reasoning priority, no unit tests |
| `morning_briefing_engine.py` | REPORT | LOW | Deprecated (replaced by chain-compliant report) |
| `delta_engine.py` | REPORT | MEDIUM | Report delta detection, no unit tests |
| `scenario_engine.py` | SIM | MEDIUM | Simulation, no unit tests |
| `visual_engine.py` | ARCH | LOW | Visualization, no unit tests |
| `engine_registry.py` | ARCH | LOW | Registry metadata, no unit tests |
| `engine_runner.py` | ARCH | LOW | Orchestration, no unit tests |

### 7.2 Signal Domain — Complete Gap

The SIGNALS domain (authority_level: 1, first in the reasoning chain) has **zero dedicated test files**. This is the most critical coverage gap for regression-safe extension:

- **Impact:** New signal engines cannot be validated against existing signal contracts
- **Risk:** Signal format changes could silently break downstream SEMANTICS and REASONING
- **Recommendation:** Priority 1 for test governance expansion

### 7.3 Governance Modules Without Dedicated Tests (in `tests/`)

| Module | Has Property Test? | Has Unit Test? | Gap |
|---|:---:|:---:|---|
| `governance/actor_identity.py` | YES | NO | Unit test gap |
| `governance/boundary_enforcer.py` | Partial | YES (wiring) | Covered via integration |
| `governance/gate_framework.py` | YES | NO | Unit test gap |
| `governance/hash_canonicalizer.py` | NO | NO | Full gap |
| `governance/invariant_validator.py` | NO | NO | Full gap |
| `governance/runtime_integrity_hash.py` | NO | NO | Full gap |
| `governance/shadow_authority_detector.py` | NO | NO | Full gap |
| `governance/state_provenance_tagger.py` | NO | NO | Full gap |


---

## 8. Test Category Summary

### 8.1 By Category (within `tests/` directory — 494 tests)

| Category | File Count | Test Count | Description |
|---|:---:|:---:|---|
| Property tests | 33 | 176 | Hypothesis-based correctness properties |
| Unit tests | 15 | 274 | Isolated module behavior |
| Integration tests | 1 | 12 | Cross-module interaction (delta_init) |
| Non-interference tests | 1 | 32 | Delta-layer guarantees |
| Regression/baseline tests | 0 | 0 | No dedicated baseline preservation tests (baseline is the full suite) |
| Unclassified | 1 | 0 | `verify_ledger_integration.py` — verification script (0 tests collected) |

### 8.2 By Category (outside `tests/` — not in baseline count)

| Location | File Count | Category |
|---|:---:|---|
| `engines/test_*.py` | 5 | Unit + integration (engine-specific) |
| `runtime/test_*.py` | 9 | Unit (runtime modules) |
| `governance/test_*.py` | 3 | Unit (governance modules) |

---

## 9. Extension Governance Recommendations

### 9.1 Adding a New Engine

To extend MoneyHorst with a new engine regression-safe:

1. **Create engine file** in `engines/<engine_name>.py`
2. **Register in artifact registry** with correct domain assignment
3. **Create unit test** in `engines/test_<engine_name>.py` (co-located)
4. **Create property test** in `tests/test_property_<engine_name>_<property>.py` if the engine has invariants
5. **Verify non-interference** by running `pytest tests/test_delta_non_interference.py`
6. **Run full baseline** to confirm no regression: `pytest tests/ --collect-only -q` should show baseline + new tests

### 9.2 Adding a New Signal

Since no `signals/` directory exists, signals are engines in the SIGNALS domain:

1. Follow the "Adding a New Engine" process above
2. Assign `primary_domain: SIGNALS` in artifact registry
3. **Critical:** Create at least one property test validating signal output format
4. Verify downstream consumers (SEMANTICS engine) can parse the new signal format

### 9.3 Adding a New Report

1. **Create report engine** in `engines/<report_name>_engine.py` or `reports/`
2. **Register in artifact registry** with `primary_domain: REPORT`
3. **Create property test** for report structure invariants
4. **Verify** report does not introduce new enforcement modes or fail modes (non-interference)

---

## 10. Baseline Preservation Contract

### Current Baseline

- **Test count:** 494 (from `tests/` directory)
- **Discovery date:** 2026-06-01
- **Discovery method:** `.venv/bin/python -m pytest tests/ --collect-only -q`

### Regression Rule

Any change that reduces the test count below 494 without explicit CTO approval is a regression. New features MUST add tests (additive-only).

### Baseline Verification Command

```bash
.venv/bin/python -m pytest tests/ --collect-only -q | tail -1
# Expected: "494 tests collected" or higher
```

---

## 11. File-to-Category Complete Mapping

### Property Tests (`test_*_properties.py` or `test_property_*.py`)

```
tests/test_influence_graph_properties.py          → property
tests/test_deployment_authority_properties.py     → property
tests/test_transition_cooldown_properties.py      → property
tests/test_domain_lifecycle_properties.py         → property
tests/test_property_actor_identity_roundtrip.py   → property
tests/test_property_canonical_boundary_enforcement.py → property
tests/test_property_chain_provenance_integrity.py → property
tests/test_property_confidence_degradation.py     → property
tests/test_property_data_availability_summary.py  → property
tests/test_property_deployment_matrix_partition.py → property
tests/test_property_enforcement_mode_roundtrip.py → property
tests/test_property_forbidden_flow_detection.py   → property
tests/test_property_gate_result_roundtrip.py      → property
tests/test_property_governance_event_completeness.py → property
tests/test_property_graceful_degradation.py       → property
tests/test_property_non_determinism_injection.py  → property
tests/test_property_pipeline_determinism.py       → property
tests/test_property_pipeline_state_aggregation.py → property
tests/test_property_portfolio_watchlist_separation.py → property
tests/test_property_position_transition_rendering.py → property
tests/test_property_provenance_parseability.py    → property
tests/test_property_reasoning_object_schema.py    → property
tests/test_property_reasoning_object_section_mapping.py → property
tests/test_property_report_structure_invariant.py → property
tests/test_property_report_value_validation.py    → property
tests/test_property_run_context_temporal_consistency.py → property
tests/test_property_schema_version_compatibility.py → property
tests/test_property_section_completeness.py       → property
tests/test_property_self_disable_guard.py         → property
tests/test_property_semantic_coverage_invariant.py → property
tests/test_property_semantic_delta_correctness.py → property
tests/test_property_semantic_state_round_trip.py  → property
tests/test_property_sunset_governance_behavior.py → property
```

### Non-Interference Tests

```
tests/test_delta_non_interference.py              → non-interference
```

### Integration Tests

```
tests/test_delta_init.py                          → integration
```

### Unit Tests

```
tests/test_influence_graph.py                     → unit
tests/test_deployment_authority.py                → unit
tests/test_transition_cooldown.py                 → unit
tests/test_domain_lifecycle.py                    → unit
tests/test_audit_ledger_verification.py           → unit
tests/test_boundary_shadow_ledger_wiring.py       → unit
tests/test_cold_start_handler.py                  → unit
tests/test_deterministic_ordering_enforcement.py  → unit
tests/test_enforcement_config_loader.py           → unit
tests/test_enforcement_runtime_verification.py    → unit
tests/test_lifecycle_audit_wiring.py              → unit
tests/test_ontology_growth_observer.py            → unit
tests/test_pipeline_initializer.py                → unit
tests/test_policy_versioner.py                    → unit
tests/test_sunset_governance.py                   → unit
```

### Unclassified

```
tests/verify_ledger_integration.py               → unclassified (verification script, not standard test pattern)
```

---

**Report generated:** 2026-06-01  
**No existing runtime files modified.**  
**No new tests written.**  
**No code refactored.**
