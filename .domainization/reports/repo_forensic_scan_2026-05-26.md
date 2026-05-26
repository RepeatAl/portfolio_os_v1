# Repository Forensic Scan Report

**Date**: 2026-05-26
**Purpose**: Pre-implementation governance alignment for report-runtime-integrity spec
**Scope**: Full repository artifact classification

---

## 1. Summary

| Category | Count | Status |
|----------|-------|--------|
| Canonical artifacts (SSOT docs, engines, governance) | 56 | Active, authoritative |
| Compatibility artifacts (legacy briefing files) | 14 | Functional, will be deprecated |
| Transient artifacts (generated outputs) | 37 | Not authoritative, regenerable |
| Historical artifacts (archived snapshots) | 7 | Preserved, read-only |
| Infrastructure artifacts (domainization system) | ~105 | Active governance tooling |
| Spec artifacts (Kiro specs, steering) | 15 | Active governance docs |
| Unregistered artifacts | 6 | Need classification |

---

## 2. Canonical Artifacts (SSOT Documents)

| File Path | Domain | Lifecycle | Registry Status | Action |
|-----------|--------|-----------|-----------------|--------|
| `docs/system_architecture.md` | ARCH | canonical | Registered | None |
| `docs/engine_design_principles.md` | ARCH | canonical | Registered | None |
| `docs/signal_calculation_framework.md` | SIGNALS | canonical | Registered | None |
| `docs/portfolio_health_framework.md` | SIGNALS | canonical | Registered | None |
| `docs/market_regime_framework.md` | SIGNALS | canonical | Registered | None |
| `docs/correlation_dependency_framework.md` | SIGNALS | canonical | Registered | None |
| `docs/scoring_methodology_framework.md` | SIGNALS | canonical | Registered | None |
| `docs/semantic_signal_registry.md` | SEMANTICS | canonical | Registered | None |
| `docs/semantic_reasoning_rules.md` | SEMANTICS | canonical | Registered | None |
| `docs/decision_governance.md` | GOV | canonical | Registered | None |
| `docs/report_reasoning_system.md` | REPORT | canonical | Registered | None |
| `docs/report_section_specification.md` | REPORT | canonical | Registered | None |
| `docs/simulation_architecture.md` | SIM | canonical | Registered | None |
| `docs/dashboard_philosophy.md` | USER | canonical | Registered | None |
| `docs/portfolio_memory_architecture.md` | MEMORY | canonical | Registered | None |
| `docs/portfolio_state_model.md` | STATE | canonical | Registered | None |
| `docs/watchlist_asset_registry_framework.md` | STATE | canonical | Registered | None |
| `docs/data_ingestion_normalization_framework.md` | DATA | canonical | Registered | None |

### Canonical Engines (15 total)

| File Path | Domain | Lifecycle | Registry Status | Action |
|-----------|--------|-----------|-----------------|--------|
| `engines/allocation_engine.py` | SIGNALS | active | Registered | None |
| `engines/regime_engine.py` | SIGNALS | active | Registered | None |
| `engines/attribution_engine.py` | SIGNALS | active | Registered | None |
| `engines/scoring_engine.py` | SIGNALS | active | Registered | None |
| `engines/semantic_engine.py` | SEMANTICS | active | Registered | None |
| `engines/decision_engine.py` | REASONING | active | Registered | None |
| `engines/quality_engine.py` | REASONING | active | Registered | None |
| `engines/priority_engine.py` | REASONING | active | Registered | None |
| `engines/report_engine.py` | REPORT | active | Registered | None |
| `engines/morning_briefing_engine.py` | REPORT | active | Registered | None |
| `engines/delta_engine.py` | REPORT | active | Registered | None |
| `engines/scenario_engine.py` | SIM | active | Registered | None |
| `engines/visual_engine.py` | ARCH | active | Registered | None |
| `engines/engine_registry.py` | ARCH | active | Registered | None |
| `engines/engine_runner.py` | ARCH | active | Registered | None |

---

## 3. Compatibility Artifacts (Legacy Briefing Files)

These 14 briefing files are produced by Signal Engines directly, bypassing the canonical chain.
They remain functional but will be deprecated once chain-compliant outputs are implemented.

| File Path | Domain | Lifecycle | Registry Status | Recommended Action |
|-----------|--------|-----------|-----------------|-------------------|
| `allocation_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `attribution_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `correlation_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `cross_asset_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `divergence_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `early_warning_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `flow_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `liquidity_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `market_breadth_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `narrative_dependency_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `portfolio_memory_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `regime_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `relative_strength_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |
| `scenario_briefing.txt` | REPORT | compatibility | Registered | Deprecate after chain migration |

**Note**: The registry classifies these as `REPORT_OUT` with lifecycle `current`. After implementation of report-runtime-integrity, their lifecycle should transition to `deprecated` with a sunset date.

---

## 4. Transient Artifacts (Generated Signal Outputs)

These `.xlsx` files are regenerable signal outputs. Not authoritative — produced fresh each pipeline run.

| File Path | Domain | Type | Registry Status | Action |
|-----------|--------|------|-----------------|--------|
| `allocation_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `attribution_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `regime_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `scenario_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `risk_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `correlation_matrix.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `high_correlation_pairs.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `divergence_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `early_warning_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `flow_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `liquidity_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `market_breadth_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `narrative_risk_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `relative_strength_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `cross_asset_engine.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `divergence_market_data.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `liquidity_signals.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `macro_output.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `narrative_summary.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `trigger_dependency.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `breadth_category_strength.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `category_attribution.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `category_relative_strength.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `cross_asset_data.xlsx` | SIGNALS | DATA_OUT | Registered | None |
| `allocation_governance.xlsx` | STATE | DATA_OUT | Registered | None |
| `category_exposure.xlsx` | STATE | DATA_OUT | Registered | None |
| `category_flow.xlsx` | STATE | DATA_OUT | Registered | None |
| `portfolio_output.xlsx` | STATE | DATA_OUT | Registered | None |
| `watchlist.xlsx` | STATE | DATA_IN | Registered | None |
| `portfolio_report.txt` | REPORT | REPORT_OUT | Registered | None |
| `morning_briefing.txt` | REPORT | REPORT_OUT | Registered | None |

---

## 5. Historical Artifacts (Preserved)

| File Path | Domain | Lifecycle | Registry Status | Action |
|-----------|--------|-----------|-----------------|--------|
| `history/briefing_2026-05-23.txt` | MEMORY | archived | Registered | Preserve |
| `history/macro_2026-05-23.xlsx` | MEMORY | archived | Registered | Preserve |
| `history/narrative_2026-05-23.xlsx` | MEMORY | archived | Registered | Preserve |
| `history/portfolio_2026-05-23.xlsx` | MEMORY | archived | Registered | Preserve |
| `history/portfolio_memory.xlsx` | MEMORY | captured | Registered | Preserve |
| `history/regime_history.xlsx` | MEMORY | captured | Registered | Preserve |
| `history/report_2026-05-24.txt` | MEMORY | archived | Registered | Preserve |

---

## 6. Unregistered Artifacts (Gap Analysis)

These files exist on disk but are NOT in the artifact registry:

| File Path | Probable Domain | Probable Type | Recommended Action |
|-----------|----------------|---------------|-------------------|
| `docs/confidence_model.md` | GOV | SSOT | Register (future sprint) |
| `docs/action_space_framework.md` | GOV | SSOT | Register (future sprint) |
| `docs/deployment_intelligence_framework.md` | REASONING | SSOT | Register (future sprint) |
| `docs/multilingual_rendering_framework.md` | REPORT | SSOT | Register (future sprint) |
| `docs/opportunity_engine_design.md` | ARCH | SSOT | Register (future sprint) |
| `docs/report_pipeline_architecture.md` | ARCH | SSOT | Register (future sprint) |
| `docs/future_framework_backlog.md` | ARCH | SSOT | Register (future sprint) |
| `docs/trusted_signal_sources.md` | DATA | SSOT | Register (future sprint) |
| `docs/portfolio_os_domainization_steering.md` | GOV | STEERING | Register (future sprint) |
| `reports/governance_stabilization_audit_2026-05-25.md` | GOV | REPORT_OUT | Register (future sprint) |
| `reports/governance_stabilization_preflight_2026-05-25.md` | GOV | REPORT_OUT | Register (future sprint) |
| `reports/governance_stabilization_verification_2026-05-25.md` | GOV | REPORT_OUT | Register (future sprint) |
| `reports/task_1_execution_report.md` | ARCH | REPORT_OUT | Register (future sprint) |
| `reports/pm_report_engine.py` | REPORT | ENGINE | Registered (development) |

**Note**: These are the 13 unregistered artifacts identified in the baseline health report. Registration is deferred to the implementation phase per the spec (Requirement 3).

---

## 7. Infrastructure Artifacts (Domainization System)

The `.domainization/` directory contains ~105 files (Python modules, tests, docs, configs).
These are governance infrastructure — not subject to the same lifecycle as product artifacts.

**Status**: Consistent, well-organized, fully operational in observability mode.

---

## 8. Spec and Steering Artifacts

| File Path | Type | Status |
|-----------|------|--------|
| `.kiro/specs/report-runtime-integrity/requirements.md` | Spec | NEW — ready for commit |
| `.kiro/specs/report-runtime-integrity/design.md` | Spec | NEW — ready for commit |
| `.kiro/specs/report-runtime-integrity/tasks.md` | Spec | NEW — ready for commit |
| `.kiro/specs/report-runtime-integrity/.config.kiro` | Config | NEW — ready for commit |
| `.kiro/specs/domainization/` (6 files) | Spec | Existing, untracked |
| `.kiro/steering/` (5 files) | Steering | Existing, untracked |

---

## 9. Misplaced Artifacts

| File Path | Issue | Recommendation |
|-----------|-------|----------------|
| `docs/documants-to-take-selected/` | Empty directory with typo in name | Remove (empty, no content) |
| `data.json` | Root-level config file | Acceptable (registered as STATE/CONFIG) |

---

## 10. Files That Should NOT Be Committed

| File/Pattern | Reason |
|--------------|--------|
| `.DS_Store` (all locations) | macOS metadata |
| `__pycache__/` (all locations) | Python bytecode cache |
| `*.pyc` | Compiled Python |
| `.coverage` | Test coverage data |
| `.pytest_cache/` | Pytest cache |

**Status**: `.gitignore` updated to cover `.pytest_cache/` and `.coverage`.

---

*Generated: 2026-05-26*
*Phase: Pre-implementation governance alignment*
