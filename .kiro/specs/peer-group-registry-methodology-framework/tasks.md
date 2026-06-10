# Implementation Plan: Peer Group Registry Methodology Framework

## Overview

This plan covers all documentation and verification tasks required to complete the Peer Group Registry Methodology Framework. All tasks produce Markdown artifacts only.

Hard boundaries — no task may produce:
- Registry YAML or registry data files
- Runtime code, services, APIs, or database schemas
- Market data integrations or vendor connections
- Broker or exchange connections
- Order routing or execution logic
- Scoring, ranking, recommendation, or allocation logic
- SAI artifact modifications
- Canonical peer group IDs or peer assignments

## Tasks

- [x] 1. Produce Q1–Q10 Decision Intake Document
  - Create `artifacts/decision_intake_review_2026-06-08.md`
  - Cover Q1–Q10 each with: decision statement, evidence citations by source authority domain, key rationale, deferred items
  - Include summary table: question / decision / authority domain / deferred items
  - Mark Q6 as EVIDENCE_PARTIAL with threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED
  - Mark Q7 as EVIDENCE_INSUFFICIENT with private_comparable_context role only
  - Include market data readiness summary (CURRENT_MODEL_NULLABLE vs. FUTURE_VENDOR_INTEGRATION)
  - Include trading governance boundary confirmation (FUTURE_COMPLIANCE_REFERENCE, no current obligations)
  - _Requirements: PGMF-DEC-01 through PGMF-DEC-10_

- [x] 2. Verify Source Authority Traceability
  - Create `artifacts/source_authority_verification_2026-06-08.md`
  - Build traceability table: decision / cited source / authority domain / traceability status
  - Verify each decision is cited against sources in its correct authority domain
  - Flag any decision citing only Tier 2 or Tier 3 sources as sole authority
  - Confirm Q6 is marked NUMERIC_THRESHOLDS_DEFERRED with categorical bands only
  - Confirm Q7 is marked EVIDENCE_INSUFFICIENT with private_comparable_context role only
  - Confirm no trading governance source is used as a current-obligation rule
  - _Requirements: Source Authority Hierarchy (Section 3)_

- [x] 3. Create Field Taxonomy Reference
  - Create `artifacts/field_taxonomy_reference_2026-06-08.md`
  - Section 1: Current methodology fields required in any v1 record (entity, security, peer assignment, comparability gate, ETF/fund, cross-region, governance)
  - Section 2: Data-model readiness fields CURRENT_MODEL_NULLABLE — list all 8 fields with activation rationale
  - Section 3: Future vendor integration fields FUTURE_VENDOR_INTEGRATION — list all 9 fields excluded until vendor agreement exists
  - Section 4: Future trading governance fields FUTURE_COMPLIANCE_REFERENCE — list all 14 fields with regulatory source
  - For each field: name, type, allowed values, description, scope label, source_authority domain
  - Confirm no FUTURE_COMPLIANCE_REFERENCE field appears in current methodology section
  - Confirm CURRENT_MODEL_NULLABLE fields match Listing Record in design.md
  - _Requirements: PGMF-DEC-04, PGMF-DEC-08, Sections 8 and 9_

- [x] 4. Create ETF / Fund Peer Rule Specification
  - Create `artifacts/etf_fund_peer_rule_specification_2026-06-08.md`
  - Document all ETF/fund comparison fields with types, requirements, and source authority (ETF_methodology_authority)
  - Define peer_role = etf_peer vs. peer_role = benchmark_context distinction with examples
  - Explain tracking_difference vs. tracking_error distinction (SRC-F-01 Morningstar)
  - Define same-index ETF peer group boundary
  - Document UCITS vs. 1940-Act domicile handling
  - List prohibited comparisons: asset_type = etf with peer_role = core_peer or adjacent_peer against company assets
  - Provide benchmark_context instrument examples per confirmed family
  - Confirm no ETF receives core_peer or adjacent_peer in any example
  - _Requirements: PGMF-DEC-05_

- [x] 5. Create Cross-Region Comparability Specification
  - Create `artifacts/cross_region_comparability_specification_2026-06-08.md`
  - Document accounting standard comparability gaps: R&D capitalization, lease accounting, inventory LIFO prohibition, financial instruments classification
  - Document GICS vs. ICB taxonomy reconciliation requirement
  - Explain trading_currency vs. reporting_currency distinction
  - Document fiscal_year_end alignment requirement
  - Define comparability_adjustment_required = true trigger conditions
  - Provide cross-region peer examples: Rheinmetall XETR/IFRS/EUR vs. LMT XNYS/GAAP/USD
  - List European-listed peers from confirmed families with exchange_mic, accounting_standard, comparability_adjustment_required
  - _Requirements: PGMF-DEC-08_

- [x] 6. Create Governance and Versioning Specification
  - Create `artifacts/governance_versioning_specification_2026-06-08.md`
  - Document annual review process and review_cycle field
  - Define event-triggered review triggers: material M&A, revenue mix shift >30%, business model restructuring, primary listing change, accounting standard change
  - Document challenge/appeal process consistent with ICB model (SRC-C-01)
  - Define change management workflow: trigger event to new versioned record
  - Document versioning non-overlap property: no two active records for same canonical_object_id + family_id at same date; gaps allowed when documented
  - Provide governance field reference for all required fields
  - Define methodology_version increment rules
  - _Requirements: PGMF-DEC-09, PGMF-DEC-10_

- [x] 7. Create Market Data Readiness Specification
  - Create `artifacts/market_data_readiness_specification_2026-06-08.md`
  - Section 1 — CURRENT_MODEL_NULLABLE: document all 8 fields that must exist in v1 schema with null values; explain why each must exist now
  - Section 2 — FUTURE_VENDOR_INTEGRATION: document all 9 fields excluded from v1 schema; explain activation condition for each
  - Add exchange-specific notes: XETR/CET, XNAS/ET near-24hr, XNYS/ET multi-MIC, XAMS/XPAR/XMIL/CET
  - Explain non-display derived data policy (SRC-I-07)
  - Include explicit boundary statement: these fields do NOT integrate market data; they reserve schema space only
  - _Requirements: Market Data Readiness Fields (Section 8)_

- [x] 8. Create Trading Governance Boundary Specification
  - Create `artifacts/trading_governance_boundary_2026-06-08.md`
  - State: MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue
  - State: all 14 trading governance fields are FUTURE_COMPLIANCE_REFERENCE — reserved in methodology vocabulary only, not part of v1 schema, not populated, not operational
  - Document each field with regulatory source, authority domain (future_trading_reference), and activation condition
  - Reproduce three-gate activation model from design.md (Regulatory Status Gate, Jurisdiction Gate, Implementation Gate)
  - Include what-may/must-not-be-done-now rules
  - Include explicit prohibition: no trading enablement may be derived from the presence of these fields
  - _Requirements: Trading Governance Boundary (Section 9)_

- [x] 9. Create Unsupported Asset Class Handling Specification
  - Create `artifacts/unsupported_asset_class_handling_2026-06-08.md`
  - Define UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION and PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON and their effect on peer_comparison_allowed and peer_group_available
  - Document all 8 asset classes: commodities, crypto, bonds/credit, derivatives, FX/cash, private companies, ETFs/funds (PGF-09), indices
  - For each class: why company-peer logic does not apply, alternative methodology needed, v1 status, peer_role in v1
  - Document private_comparable_context: role definition, valuation_peer_allowed = false, comparison_mode_allowed = ecosystem_context_only
  - Include additive-only extension rule
  - _Requirements: Unsupported Asset Class Handling (Section 7)_

- [x] 10. Create SAI Compatibility Verification Document
  - Create `artifacts/sai_compatibility_verification_2026-06-08.md`
  - Build table: SAI-BLK-21 expects (deferred_interfaces.md Section 2.3) vs. this framework provides
  - Map all 17 SAI output contract fields to the interface contract elements
  - Confirm deferred_interfaces.md Section 2.3 is not modified
  - Confirm peer_benchmark.md Section 6 is not modified
  - Confirm no SAI artifact, gate, or requirement is modified
  - Document graceful degradation: peer_group_available = false, peer_comparison_allowed = false, ad-hoc peers prohibited
  - Verify all 13 correctness properties from design.md are satisfiable
  - _Requirements: SAI Compatibility (Section 10)_

- [x] 11. Execute Verification Gate VG-PGMF-1
  - Create `artifacts/gate_vg_pgmf_1.md`
  - Run full checklist: requirements.md v2 complete, design.md v2 complete (READY_FOR_TASKS)
  - Verify Tasks 1–10 artifacts are all complete
  - Verify: no registry YAML created, no peer group IDs assigned, no implementation code, no SAI artifacts modified, no market data integrated, no trading logic created
  - Verify all 13 correctness properties are satisfiable given data model and methodology rules
  - Record gate result: PEER_GROUP_REGISTRY_METHODOLOGY_FRAMEWORK_SPEC_COMPLETE or BLOCKED
  - _Requirements: All sections_

- [x] 12. Update Framework README
  - Update `README_peer_group_registry_methodology_framework.md`
  - Reflect final design.md v2 state: canonical_object_id, six-role peer_role taxonomy, CURRENT_MODEL_NULLABLE / FUTURE_VENDOR_INTEGRATION / FUTURE_COMPLIANCE_REFERENCE scope labels, 13 correctness properties, design status READY_FOR_TASKS
  - Update canonical artifact map to include all Task 1–10 artifact files
  - Confirm final spec status: PEER_GROUP_REGISTRY_METHODOLOGY_TASKS_READY_FOR_HUMAN_REVIEW
  - _Requirements: All sections_

## Task Dependency Graph

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": [1, 3, 5, 6, 9, 10],
      "description": "Independent documentation tasks — may execute in parallel"
    },
    {
      "wave": 2,
      "tasks": [2, 4, 7, 8],
      "description": "Task 2 depends on Task 1; Tasks 4, 7, 8 each depend on Task 3 field taxonomy being complete"
    },
    {
      "wave": 3,
      "tasks": [11, 12],
      "description": "Gate (Task 11) and README update (Task 12) depend on Tasks 1–10 all complete"
    }
  ]
}
```

## Notes

- All tasks produce Markdown documentation artifacts under `.kiro/specs/peer-group-registry-methodology-framework/artifacts/` except Task 12 which updates the README at the spec root
- Q6 numeric threshold calibration is deferred — EVIDENCE_PARTIAL; all records carry threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED
- Q7 private comparable full methodology is deferred — EVIDENCE_INSUFFICIENT; v1 allows private_comparable_context role with ecosystem_context_only only
- CURRENT_MODEL_NULLABLE fields must be in v1 schema even when null — prevents architectural rewrite when market data is added
- FUTURE_VENDOR_INTEGRATION fields are not in v1 schema — require active vendor agreements before population
- All 14 trading governance fields are FUTURE_COMPLIANCE_REFERENCE — reserved vocabulary only, not operational, not current obligations
- MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue
