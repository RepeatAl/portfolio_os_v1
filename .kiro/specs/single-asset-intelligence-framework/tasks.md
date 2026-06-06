# Implementation Plan: Single Asset Intelligence Framework

## Overview

**Spec**: single-asset-intelligence-framework
**Phase**: Tasks
**Status**: Draft / Task Plan
**Authority**: ARCH
**Source References**:
- `.domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md`
- `.kiro/specs/single-asset-intelligence-framework/requirements.md`
- `.kiro/specs/single-asset-intelligence-framework/design.md`

This plan defines definition-layer artifact creation tasks for the Single Asset Intelligence Framework. All tasks produce documentation and specification artifacts. No implementation code, scoring, recommendation, allocation, or registry mutation is authorized.

## Task Execution Rules

1. Tasks are definition-layer artifact tasks only.
2. Tasks must not create implementation code, database schemas, API designs, or runtime architecture.
3. Tasks must not mutate SSOT documents or registries.
4. Tasks must not create scoring, ranking, recommendation, allocation, or trading logic.
5. Verification gates require explicit gate execution artifacts — they are not auto-completed.
6. If a task discovers scope pressure toward implementation or scoring, it must stop and report drift.
7. No facts, signals, or evidence objects may be created.
8. No asset-to-narrative mappings or narrative mappings may be created.
9. All cross-references must use canonical (See: [Deliverable], Section: [Title]) format.

## Tasks

- [x] 1. Canonical Block Taxonomy Artifact
  - [x] 1.1 Create block taxonomy document
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/block_taxonomy.md`
    - Define all 24 blocks (SAI-BLK-01 through SAI-BLK-24) with: block_id, block_name, category, purpose, fact families, signal families, temporal resolution, output type, provenance requirement, red flag requirement, deferred dependencies, non-scoring boundary statement
    - Organize blocks by category: Foundation, Operational, Financial Stability, Risk, Earnings, Valuation, Market Position, Outlook, Portfolio Context
    - _Requirements: SAI-REQ-1, SAI-REQ-14_
    - _Verification Gate: VG-SAI-1, VG-SAI-5_

- [x] 2. Fact Consumption Matrix
  - [x] 2.1 Create fact-to-block consumption matrix
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/fact_consumption_matrix.md`
    - Map all 68 fact categories from the preflight to their consuming blocks
    - Verify every block has at least 1 fact category assigned
    - Verify every fact category is assigned to at least 1 block
    - Mark any missing fact categories as interface gaps (do NOT invent new facts)
    - Do NOT mutate Market Evidence Framework
    - _Requirements: SAI-REQ-2_
    - _Verification Gate: VG-SAI-6_

- [x] 3. Signal Consumption Matrix
  - [x] 3.1 Create signal-to-block consumption matrix
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/signal_consumption_matrix.md`
    - Map all 23 signal categories from the preflight to their consuming blocks
    - Verify every block has at least 1 signal category assigned
    - Verify every signal category is assigned to at least 1 block
    - Do NOT define calculation formulas
    - Do NOT create signals or mutate Signal Calculation Framework
    - Mark deferred signal dependencies where calculation rules are unavailable
    - _Requirements: SAI-REQ-3_
    - _Verification Gate: VG-SAI-7_

- [x] 4. Output Object Specification
  - [x] 4.1 Create output object specification
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/output_object_spec.md`
    - Define allowed fields: block_id, asset_id, consumed_facts, consumed_signals, interpretation_summary, red_flags, evidence_completeness, temporal_status, provenance_chain, deferred_dependency_notes
    - Define prohibited fields explicitly: score, rank, recommendation, target_weight, position_size, price_target, fair_value, buy/sell/hold, probability_of_success, expected_return, alpha_estimate, confidence_score, conviction_level, risk_score, overvalued, undervalued, fairly_valued, buy_signal, sell_signal, hold_signal
    - Include YAML schema example (conceptual, not implementation)
    - _Requirements: SAI-REQ-5_
    - _Verification Gate: VG-SAI-2_

- [x] 5. Provenance Contract Artifact
  - [x] 5.1 Create provenance contract
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/provenance_contract.md`
    - Define: source_fact_ids, source_signal_ids, timestamps, source_type, evidence_freshness, completeness metadata
    - Define invalid orphan interpretation rule
    - Define timestamp inheritance rules
    - Define stale/expired status handling with thresholds per temporal class
    - _Requirements: SAI-REQ-4_
    - _Verification Gate: VG-SAI-3_

- [x] 6. Red Flag Taxonomy Artifact
  - [x] 6.1 Create red flag taxonomy
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/red_flag_taxonomy.md`
    - Define at least 2 red flags per block (minimum 48 total)
    - Each red flag includes: red_flag_id, block_id, condition, required evidence, temporal persistence, severity (informational/elevated/critical), provenance requirement, non-action statement
    - Red flags must NOT create numeric risk scores, trigger actions, map to buy/sell/hold, or aggregate into ratings
    - _Requirements: SAI-REQ-13_
    - _Verification Gate: VG-SAI-8_

- [x] 7. Temporal Resolution Matrix
  - [x] 7.1 Create temporal resolution matrix
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/temporal_resolution_matrix.md`
    - Define for each block: block_id, temporal class (quarterly/monthly/daily/real-time), rationale, stale threshold, expired threshold, source cadence dependency, real-time status (prohibited/allowed/future)
    - Explain: filing-based blocks = quarterly, market-relative blocks = daily, real-time = exceptional
    - _Requirements: SAI-REQ-6_
    - _Verification Gate: VG-SAI-9_

- [x] 8. Deferred Interface Contract Artifacts
  - [x] 8.1 Create deferred interface contracts
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md`
    - Define contracts for: Valuation Framework, Earnings Intelligence Framework, Peer Group Registry, Portfolio Health Framework, Correlation/Dependency Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework
    - Each contract: what SAI expects to consume, what SAI may emit, what SAI must not define, current limitation, affected SAI blocks
    - Do NOT define those frameworks — only declare interface expectations
    - _Requirements: SAI-REQ-11, SAI-REQ-12, SAI-REQ-14_
    - _Verification Gate: VG-SAI-4_

- [x] 9. Valuation / Value Trap Guard Artifact
  - [x] 9.1 Create valuation boundary artifact
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/valuation_boundary.md`
    - Preserve principle: "Low valuation is not automatically undervaluation. A stock is not cheap because it fell. A stock is cheap only if market expectation is below realistic value creation."
    - Require valuation interpretation to consume: cashflow, credit/solvency, hidden liabilities, earnings quality, outlook, peer context
    - Prohibit: fair value estimate, target price, undervalued/overvalued/fairly valued labels, expected return, probability of revaluation, buy/sell/hold implication
    - _Requirements: SAI-REQ-7_
    - _Verification Gate: VG-SAI-2_

- [x] 10. Credit / Solvency Artifact
  - [x] 10.1 Create credit/solvency artifact
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/credit_solvency.md`
    - Include full scope: gross debt, net debt, maturity schedule, short-term debt, available liquidity, interest coverage, net debt/EBITDA, FCF/debt, lease liabilities, purchase obligations, off-balance commitments, pension obligations, pension funding gap, goodwill/intangibles/impairment, LBO history, sponsor overhang, covenant pressure, bond/CDS/rating evidence
    - State: Credit ratings are inputs, not truth
    - _Requirements: SAI-REQ-8_
    - _Verification Gate: VG-SAI-1_

- [x] 11. Peer / Benchmark Artifact
  - [x] 11.1 Create peer/benchmark artifact
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/peer_benchmark.md`
    - Include: relative strength vs benchmark/sector/peers, correlation, beta decomposition, volatility, drawdown, own-strength vs beta-driven movement
    - State: peer groups non-canonical until Peer Group Registry exists; SAI consumes peer definitions, does not create them; no ranking, scoring, factor model, or trading signal
    - _Requirements: SAI-REQ-10_
    - _Verification Gate: VG-SAI-1_

- [x] 12. Portfolio Fit Interface Artifact
  - [x] 12.1 Create portfolio fit interface artifact
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/portfolio_fit_interface.md`
    - Allowed: concentration contribution, dependency overlap, future narrative overlap interface, macro sensitivity, liquidity sensitivity, diversification contribution, fragility contribution
    - Forbidden: target weight, position size, capital allocation, buy/sell, optimization, rebalance instruction, overweight/underweight/neutral labels, portfolio score
    - _Requirements: SAI-REQ-11_
    - _Verification Gate: VG-SAI-12_

- [ ] 13. KPI Mapping Validation Artifact
  - [ ] 13.1 Create KPI mapping artifact
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/kpi_mapping.md`
    - Map at least 80% of KPI-Micro Asset Analysis Sheet items to canonical SAI blocks
    - If KPI sheet is not available in repo, create a placeholder mapping contract and mark external input required
    - Do NOT invent unavailable KPI sheet contents
    - _Requirements: SAI-REQ-2_
    - _Verification Gate: VG-SAI-11_

- [ ] 14. Cross-Framework Terminology Audit
  - [ ] 14.1 Create terminology audit artifact
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/terminology_audit.md`
    - Compare SAI terms against: Market Evidence Framework, Narrative Framework v2, Market Organism Principles, Shared Glossary Reference
    - Document any term conflicts as findings (do NOT mutate glossary)
    - _Requirements: SAI-REQ-4_
    - _Verification Gate: VG-SAI-10_

- [ ] 15. Verification Gate Artifacts
  - [ ] 15.1 Execute VG-SAI-1 Requirements Completeness Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_01.md`
    - Check: all 24 blocks defined with stable IDs, categories, purposes
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-1_

  - [ ] 15.2 Execute VG-SAI-2 Boundary Enforcement Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_02.md`
    - Check: zero scoring/recommendation/allocation language in all artifacts
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-2_

  - [ ] 15.3 Execute VG-SAI-3 Provenance Chain Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_03.md`
    - Check: provenance specification per block; no orphan interpretation paths
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-3_

  - [ ] 15.4 Execute VG-SAI-4 Interface Contract Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_04.md`
    - Check: all 7 deferred framework interfaces have explicit contracts
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-4_

  - [ ] 15.5 Execute VG-SAI-5 Taxonomy Stability Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_05.md`
    - Check: block IDs frozen; extension mechanism documented; no block removal
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-5_

  - [ ] 15.6 Execute VG-SAI-6 Fact Coverage Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_06.md`
    - Check: all 68 fact categories assigned; all blocks have ≥1 fact; matrix complete
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-6_

  - [ ] 15.7 Execute VG-SAI-7 Signal Coverage Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_07.md`
    - Check: all 23 signal categories assigned; all blocks have ≥1 signal; matrix complete
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-7_

  - [ ] 15.8 Execute VG-SAI-8 Red Flag Taxonomy Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_08.md`
    - Check: ≥2 red flags per block; minimum 48 total; evidence-based; categorical severity only
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-8_

  - [ ] 15.9 Execute VG-SAI-9 Temporal Resolution Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_09.md`
    - Check: all 24 blocks have temporal assignment with rationale
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-9_

  - [ ] 15.10 Execute VG-SAI-10 Cross-Framework Consistency Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_10.md`
    - Check: SAI terminology consistent with Market Evidence, Narrative Framework, Market Organism, Glossary
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-10_

  - [ ] 15.11 Execute VG-SAI-11 KPI Mapping Validation Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_11.md`
    - Check: ≥80% of KPI-Micro items mapped to canonical blocks
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-11_

  - [ ] 15.12 Execute VG-SAI-12 Portfolio Fit Interface Gate
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/gate_vg_sai_12.md`
    - Check: output schema defined; no allocation language; completeness taxonomy defined
    - Record: PASS / FAIL / BLOCKED with evidence
    - _Verification Gate: VG-SAI-12_

- [ ] 16. README Artifact
  - [ ] 16.1 Create SAI framework README
    - Create `.kiro/specs/single-asset-intelligence-framework/artifacts/README_single_asset_intelligence.md`
    - Explain: what SAI is, what SAI is not, how to read artifacts, canonical block list, relationship to Market Evidence, relationship to downstream frameworks, verification gate process, strict exclusions
    - _Requirements: All_

- [ ] 17. Artifact Registry Readiness Check
  - [ ] 17.1 Create registry readiness report
    - Create `.domainization/reports/single_asset_intelligence_framework_registry_readiness.md`
    - Document whether artifact registry update is required by repo governance policy
    - If update is required, document the needed mutation and STOP for human approval
    - Do NOT mutate artifact registry without explicit human approval
    - _Requirements: Governance_

- [ ] 18. Final Task Execution Report
  - [ ] 18.1 Create final tasks report
    - Create `.domainization/reports/single_asset_intelligence_framework_task_execution_report_2026-06-06.md`
    - Include: files created, requirements coverage, design coverage, verification gate artifact summary, deferred interface summary, unresolved gaps, confirmations (no implementation, no scoring, no registry mutation, no asset mapping)
    - _Requirements: Governance_

## Notes

- This is a definition-layer artifact plan. No implementation code is authorized.
- All artifacts are documentation/specification files. No executable logic.
- Verification gates are NOT passed until their gate artifact exists with explicit PASS/FAIL evidence.
- Design readiness is NOT gate completion. A task may prepare evidence for a gate, but the gate result must be recorded in a verification artifact.
- Failed or blocked gates halt progression.
- If a task discovers scope pressure toward scoring/recommendation/implementation, it must stop and create a drift report.
- All artifacts go under `.kiro/specs/single-asset-intelligence-framework/artifacts/` or `.domainization/reports/`.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1", "3.1", "4.1", "5.1", "7.1"] },
    { "id": 2, "tasks": ["6.1", "8.1", "9.1", "10.1", "11.1", "12.1"] },
    { "id": 3, "tasks": ["13.1", "14.1"] },
    { "id": 4, "tasks": ["15.1", "15.2", "15.3", "15.4", "15.5", "15.6", "15.7", "15.8", "15.9", "15.10", "15.11", "15.12"] },
    { "id": 5, "tasks": ["16.1", "17.1"] },
    { "id": 6, "tasks": ["18.1"] }
  ]
}
```
