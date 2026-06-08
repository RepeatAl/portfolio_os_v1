# Implementation Plan: Peer Group Registry Methodology Framework

## Overview

This implementation plan covers the documentation and verification tasks required to complete the Peer Group Registry Methodology Framework spec. All tasks produce documentation artifacts only — no registry data, no runtime code, no SAI modifications, no market data integration, no trading logic.

## Tasks

- [ ] 1. Produce Q1–Q10 Decision Intake Document
  - Create artifacts/decision_intake_review_2026-06-08.md
  - Cover Q1–Q10 each with: decision statement, evidence citations, key rationale, deferred items
  - Include summary table: question / decision / primary source / deferred items
  - Mark Q6 as EVIDENCE_PARTIAL (numeric thresholds deferred) and Q7 as EVIDENCE_INSUFFICIENT (private comparables deferred)
  - Include market data readiness decisions summary and trading governance boundary confirmation
  - _Requirements: PGMF-DEC-01 through PGMF-DEC-10_

- [ ] 2. Verify Source Authority Traceability
  - Create artifacts/source_authority_verification_2026-06-08.md
  - Build traceability table: decision / cited source / authority tier / status
  - Flag any decision citing only Tier 2 or Tier 3 sources
  - Confirm Q6 soft threshold approach is correctly marked EVIDENCE_PARTIAL
  - Confirm Q7 deferral is correctly marked EVIDENCE_INSUFFICIENT
  - _Requirements: Source Authority Hierarchy (Section 3)_

- [ ] 3. Create Field Taxonomy Reference
  - Create artifacts/field_taxonomy_reference_2026-06-08.md
  - Section 1: Current methodology fields — all required in any v1 registry record
  - Section 2: Data-model readiness fields — reserved, null in v1
  - Section 3: Future market data integration fields — placeholder only
  - Section 4: Future trading governance fields — FUTURE_COMPLIANCE_REFERENCE
  - For each field: name, type, allowed values, description, scope, source_authority
  - Confirm no trading governance field appears in current methodology section
  - _Requirements: PGMF-DEC-04, PGMF-DEC-08, Market Data Fields (Section 8), Trading Governance (Section 9)_

- [ ] 4. Create ETF / Fund Peer Rule Specification
  - Create artifacts/etf_fund_peer_rule_specification_2026-06-08.md
  - Document all ETF comparison fields with types and sources
  - Define benchmark_context vs. etf_peer role distinction with examples
  - Explain tracking difference vs. tracking error distinction (SRC-F-01)
  - Define same-index ETF peer group boundary
  - Document UCITS vs. 1940-Act domicile handling
  - List prohibited comparisons: ETF vs. company examples
  - Provide benchmark context instrument examples per confirmed family
  - Confirm no ETF/company mixing in any example
  - _Requirements: PGMF-DEC-05_

- [ ] 5. Create Cross-Region Comparability Specification
  - Create artifacts/cross_region_comparability_specification_2026-06-08.md
  - Document accounting standard comparability gaps (KPMG SRC-H-02, PwC SRC-H-03): R&D, leases, inventory, financial instruments
  - Document GICS vs. ICB taxonomy reconciliation requirement
  - Explain trading_currency vs. reporting_currency distinction
  - Document fiscal_year_end alignment requirement
  - Define comparability_adjustment_required flag usage rules
  - Provide cross-region peer examples requiring adjustment
  - List all European-listed peers in confirmed families with exchange_mic and accounting_standard
  - _Requirements: PGMF-DEC-08_

- [ ] 6. Create Governance and Versioning Specification
  - Create artifacts/governance_versioning_specification_2026-06-08.md
  - Document annual review process: who reviews, what criteria trigger a change
  - Define event-triggered review triggers: M&A, revenue mix shift >30%, business model restructuring, listing change, accounting standard change
  - Document challenge/appeal process: initiation, resolution, allowed changes
  - Define change management workflow: trigger to effective_date creation
  - Document versioning mechanics: new record creation, old record deprecation
  - Provide governance field reference for all required fields
  - Define methodology_version increment rules
  - _Requirements: PGMF-DEC-09, PGMF-DEC-10_

- [ ] 7. Create Market Data Readiness Specification
  - Create artifacts/market_data_readiness_specification_2026-06-08.md
  - Document current-scope data model fields: exchange_mic, market_data_source, data_vendor, data_latency_class, exchange_timezone, trading_calendar_id, derived_data_policy, index_license_required
  - Document future vendor integration fields: realtime_entitlement_required, display_usage_allowed, non_display_usage_allowed, redistribution_allowed
  - Add exchange-specific notes: XETR/CET, XNAS/ET near-24hr, XNYS/ET, XAMS/XPAR/XMIL/CET
  - Explain non-display derived data policy (SRC-I-07)
  - Include explicit boundary statement: these fields do NOT integrate market data
  - _Requirements: Market Data Readiness Fields (Section 8)_

- [ ] 8. Create Trading Governance Boundary Specification
  - Create artifacts/trading_governance_boundary_2026-06-08.md
  - State: MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue
  - Document all trading governance fields with regulatory source, scope (FUTURE_COMPLIANCE_REFERENCE), and activation condition
  - Document pre-trade controls vocabulary from SEC 15c3-5 (SRC-I-10)
  - Document EU algo trading vocabulary from MiFID II RTS 6 (SRC-I-11)
  - Include explicit prohibition: no trading enablement may be derived from these fields
  - _Requirements: Trading Governance Boundary (Section 9)_

- [ ] 9. Create Unsupported Asset Class Handling Specification
  - Create artifacts/unsupported_asset_class_handling_2026-06-08.md
  - Define UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION and PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON status values
  - Document all 8 asset classes: commodities, crypto, bonds/credit, derivatives, FX/cash, private companies, ETFs/funds, indices
  - For each class: why company-peer logic does not apply, alternative methodology needed, v1 status
  - Document private_comparable_context role and valuation_peer_allowed = false rule
  - Include additive-only extension rule
  - _Requirements: Unsupported Asset Class Handling (Section 7)_

- [ ] 10. Create SAI Compatibility Verification Document
  - Create artifacts/sai_compatibility_verification_2026-06-08.md
  - Build table: SAI-BLK-21 expects (deferred_interfaces.md Section 2.3) vs. this framework provides
  - Confirm deferred_interfaces.md Section 2.3 is not modified
  - Confirm peer_benchmark.md Section 6 is not modified
  - Confirm no SAI artifact, gate, or requirement is modified
  - Document graceful degradation behavior (unchanged from current SAI behavior)
  - _Requirements: SAI Compatibility (Section 10)_

- [ ] 11. Execute Verification Gate VG-PGMF-1
  - Create artifacts/gate_vg_pgmf_1.md
  - Run full checklist: requirements.md complete, design.md complete, all 10 artifact tasks complete
  - Verify: no registry YAML created, no peer group IDs assigned, no implementation code, no SAI artifacts modified, no market data integrated, no trading logic created
  - Record gate result: PEER_GROUP_REGISTRY_METHODOLOGY_FRAMEWORK_SPEC_READY_FOR_HUMAN_REVIEW or BLOCKED
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
      "description": "Tasks that depend on wave 1 outputs (Task 2 depends on Task 1; Tasks 4, 7, 8 depend on Task 3)"
    },
    {
      "wave": 3,
      "tasks": [11],
      "description": "Verification gate — depends on all tasks 1–10 complete"
    }
  ]
}
```

Tasks 1–10 are independent of each other and may be executed in parallel. Task 11 depends on all preceding tasks being complete.

## Notes

- All tasks produce Markdown documentation artifacts in `.kiro/specs/peer-group-registry-methodology-framework/artifacts/`
- No task produces runtime code, registry YAML, database schema, or SAI artifact modifications
- Q6 numeric threshold calibration is explicitly deferred — EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED
- Q7 private comparable full methodology is explicitly deferred — EVIDENCE_INSUFFICIENT
- Market data fields in Task 7 are schema reservations only — no data integration occurs
- Trading governance fields in Task 8 are FUTURE_COMPLIANCE_REFERENCE only — no current obligations
- MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue
