# Peer Group Registry Methodology Framework — SAI Compatibility Verification

**Artifact**: sai_compatibility_verification_2026-06-08.md
**Task**: Task 10 — Create SAI Compatibility Verification Document
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_10_SAI_COMPATIBILITY_VERIFICATION_READY_FOR_HUMAN_REVIEW

**Purpose**: Verifies that the PGMF is compatible with future SAI reasoning while preserving all architectural boundaries. Verification-only — no SAI mutation, no runtime, no peer assignments.

**Boundary statement**: SAI compatibility verification confirms that the methodology can be safely interpreted by future SAI reasoning. It does not mutate SAI, create runtime behavior, create peer assignments, create peer_group_id values, create peer_group_registry.yaml, authorize trading, or activate production use.

**Hard boundaries**: No peer_group_registry.yaml. No final peer assignments. No canonical peer_group_id. No SAI mutation. No runtime code. No market data. No broker/exchange/ATS. No trading logic.


---

## 1. SAI Allowed Behavior

SAI may:
- Read methodology artifacts (Tasks 1–9) as future reasoning context
- Surface methodology status (peer_group_available, peer_comparison_allowed, blocked_reason)
- Explain why peer assignment is blocked (unsupported status, governance conflict, source insufficient)
- Explain why source authority is insufficient for a given asset
- Explain why an asset is unsupported or deferred (Task 9 handling statuses)
- Explain why ETF/Fund methodology differs from company methodology (Task 4 rules)
- Explain why cross-region comparability requires adjustment (Task 5 flags)
- Explain why governance violations block active use (Task 6 lifecycle/review states)
- Explain why market data readiness ≠ peer eligibility (Task 7 separation)
- Explain why trading governance is future-only (Task 8 FUTURE_COMPLIANCE_REFERENCE)
- Preserve useful context without assigning final peer groups (private_comparable_context, benchmark_context)

---

## 2. SAI Prohibited Behavior

SAI must NOT:
- Create peer_group_registry.yaml
- Create canonical peer_group_id values
- Assign companies to final peer groups
- Assign ETFs/funds to company peer groups (ETF/company boundary violation)
- Assign private companies to public-equity peer groups
- Assign derivatives, options, warrants, certificates, leveraged products, crypto, FX, commodities, bonds, indices, or baskets to final peer groups
- Infer peer eligibility from ticker availability
- Infer peer eligibility from market data availability
- Infer tradability from market data fields (CURRENT_MODEL_NULLABLE ≠ trading eligibility)
- Infer execution eligibility from peer methodology
- Bypass source authority (every decision must trace to Tier 1 sources in correct domain)
- Bypass governance lifecycle state (under_review, overdue, deprecated records have specific handling)
- Silently fallback from ETF/Fund methodology to company methodology
- Silently fallback from unsupported asset handling to equity peer methodology
- Hallucinate comparability adjustments (must surface comparability_note from record)
- Hallucinate missing source evidence
- Mutate SAI artifacts
- Implement runtime logic

---

## 3. SAI Blocking / Graceful Degradation Model

When methodology evidence is insufficient, SAI must block the operation and surface the reason clearly.

| Block State | Trigger | SAI Behavior |
|-------------|---------|-------------|
| `BLOCK_FINAL_PEER_ASSIGNMENT` | No Peer Group Registry exists (current state) | Surface standard deferred_dependency_notes; no ad-hoc peers |
| `BLOCK_PEER_GROUP_ID_CREATION` | Registry creation task not yet executed | No peer_group_id values generated or hallucinated |
| `BLOCK_UNSUPPORTED_ASSET_CLASS` | Asset has unsupported_status ≠ null (Task 9) | Surface unsupported status; preserve context if useful |
| `BLOCK_SOURCE_INSUFFICIENT` | Source authority does not meet Tier 1 threshold for classification | Identify missing evidence; reference relevant source authority domain |
| `BLOCK_IDENTITY_UNRESOLVED` | canonical_object_id cannot be confirmed | Block all assignment; flag for identity resolution |
| `BLOCK_GOVERNANCE_CONFLICT` | Overlapping active records or lifecycle_status violation (Task 6) | Log governance violation; refuse peer comparison |
| `BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED` | comparability_adjustment_required = true but comparability_note is empty | Block raw metric comparison; require note population |
| `BLOCK_ETF_COMPANY_FALLBACK` | ETF/fund being compared using company methodology (Task 4 violation) | Refuse; surface that ETF/Fund methodology applies separately |
| `BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY` | Market data field populated ≠ methodology eligibility | Refuse peer assignment based on data availability alone |
| `BLOCK_TRADING_ELIGIBILITY_INFERENCE` | Trading governance field referenced as current capability | Surface as FUTURE_COMPLIANCE_REFERENCE only; refuse trading inference |

### SAI Response Pattern for Each Block

For each blocked condition, SAI must:
1. State the block reason clearly in deferred_dependency_notes or blocked_reason
2. Preserve context if useful (private_comparable_context, benchmark_context references preserved)
3. Identify what evidence is missing (source authority gap, identity gap, governance gap)
4. Reference the relevant methodology artifact (Task number and section)
5. Avoid final classification — no peer_group_id, no peer_role = core_peer for unsupported assets
6. Avoid investment or trading implications
7. Avoid confidence inflation (confidence must decrease when evidence is incomplete)
8. Avoid making the output appear operational (no "ready for trading" or "eligible for execution")

---

## 4. Compatibility Matrix (Tasks 1–9)

| PGMF Artifact | Compatibility Requirement | SAI Allowed | SAI Blocked | Status |
|---------------|--------------------------|-------------|-------------|--------|
| Task 1 — Decision Intake | SAI may read Q1–Q10 decisions as methodology context | Explain which decisions are canonical; surface deferred items (Q6, Q7) | Create final peer assignments based on decisions alone | COMPATIBLE |
| Task 2 — Source Authority | SAI may reference source authority hierarchy for confidence assessment | Explain authority domains; surface Tier 1/2/3 tracing | Override authority hierarchy; use Tier 3 as standalone rule | COMPATIBLE |
| Task 3 — Field Taxonomy | SAI may interpret field requirements per asset_type | Identify applicable fields; surface gaps as data_quality_status | Populate fields; create schema entries; invent field values | COMPATIBLE |
| Task 4 — ETF/Fund Rule | SAI must respect ETF/company boundary | Explain why ETFs are not company peers; surface benchmark_context role | Assign etf_peer to company assets; assign core_peer to ETFs vs. companies | COMPATIBLE |
| Task 5 — Cross-Region | SAI must respect comparability_adjustment_required | Surface comparability_note; explain GAAP/IFRS differences | Compare GAAP/IFRS metrics without flag; suppress adjustment notes | COMPATIBLE |
| Task 6 — Governance | SAI must respect lifecycle_status, review_status, challenge_status | Surface under_review/overdue states; refuse overlapping active records | Ignore governance; assign from deprecated/under_review without noting | COMPATIBLE |
| Task 7 — Market Data Readiness | SAI must separate market data availability from methodology eligibility | Explain that market data ≠ peer eligibility; surface null data_quality | Infer peer eligibility from exchange_mic or data_latency_class presence | COMPATIBLE |
| Task 8 — Trading Governance | SAI must treat all trading fields as FUTURE_COMPLIANCE_REFERENCE | Surface trading fields as future-only when referenced | Infer tradability; suggest execution; imply broker connectivity | COMPATIBLE |
| Task 9 — Unsupported Assets | SAI must block unsupported asset classes from peer assignment | Explain unsupported status; preserve context; surface handling status | Assign unsupported assets to peer groups; fallback to equity methodology | COMPATIBLE |

**All 9 task artifacts: COMPATIBLE**

---

## 5. SAI Verification Scenarios

### A. Public Equity with Sufficient Source Authority

Asset: Listed company, canonical_object_id resolved, GICS-classified, Tier 1 source supports classification.
Expected SAI behavior: SAI may identify methodology eligibility and explain that the asset could receive peer assignment when the Peer Group Registry is created. SAI must NOT create final peer_group_id or registry entry.
Block state: BLOCK_FINAL_PEER_ASSIGNMENT (no registry exists yet)

### B. Public Equity with Incomplete Identity

Asset: Company reference exists but canonical_object_id cannot be confirmed (e.g., ticker-only, no FIGI/ISIN resolved).
Expected SAI behavior: SAI blocks final peer assignment and surfaces BLOCK_IDENTITY_UNRESOLVED. Explains that identity resolution is required before classification.

### C. ETF with Missing Benchmark and Holdings Data

Asset: ETF with asset_type = etf but no benchmark_index, no tracking_difference, no TER available.
Expected SAI behavior: SAI uses ETF/Fund methodology (Task 4) and blocks comparison due to insufficient evidence. Surfaces financial_comparability_gate_status = blocked, data_quality_status = insufficient.

### D. ETF Mistakenly Compared to Operating Companies

Asset: ETF proposed as core_peer or adjacent_peer for a company asset.
Expected SAI behavior: SAI blocks ETF-to-company fallback (BLOCK_ETF_COMPANY_FALLBACK). Explains that ETF/Fund methodology applies separately. ETF may only be benchmark_context or etf_peer.

### E. Cross-Region Without GAAP/IFRS Adjustment

Asset: European IFRS company compared to US GAAP company on operating margin without comparability_adjustment_required flag.
Expected SAI behavior: SAI blocks silent comparability (BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED). Requires comparability_adjustment_required = true and comparability_note before margin comparison.

### F. Private Company Referenced as Context

Asset: SpaceX referenced as strategic comparable for PGF-06 defense/AI companies.
Expected SAI behavior: SAI preserves context with peer_role = private_comparable_context. Blocks public-equity peer assignment (valuation_peer_allowed = false). Surfaces: "Private company — context only."

### G. Derivative Referencing Supported Underlying

Asset: NVDA call option.
Expected SAI behavior: SAI may evaluate NVDA (the underlying) separately if eligible. The option itself receives DERIVATIVE_ON_SUPPORTED_UNDERLYING — no peer group. SAI explains that derivatives do not become peer-group members.

### H. Index or Basket

Asset: S&P 500 Index.
Expected SAI behavior: SAI treats as benchmark_context only. Never assigns operating-company peer status. Never assigns etf_peer. Status: INDEX_OR_BASKET_REFERENCE_ONLY.

### I. Crypto, Commodity, FX, Bond

Asset: Bitcoin, Gold, EUR/USD, German Bund.
Expected SAI behavior: SAI blocks current methodology support. Status: UNSUPPORTED_CURRENT_METHODOLOGY. Surfaces: "Asset class not supported by current Peer Group Methodology (v1)."

### J. Market Data Available but No Methodology Eligibility

Asset: Asset has exchange_mic, data_latency_class populated — but has not been classified by the methodology.
Expected SAI behavior: SAI blocks market data as methodology proxy (BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY). Explains that data availability does not equal peer eligibility.

### K. Trading Governance Fields Referenced

Asset: Query references tradability_status or execution_venue_eligible.
Expected SAI behavior: SAI surfaces as FUTURE_COMPLIANCE_REFERENCE only. States: "Trading governance field — not operational; future compliance reference only." Blocks any trading/execution eligibility inference.

### L. Governance Overlap or Deprecated Status

Asset: Two active records exist for same canonical_object_id + family_id (governance violation).
Expected SAI behavior: SAI blocks active use (BLOCK_GOVERNANCE_CONFLICT). Refuses peer comparison. Logs governance violation. Requires resolution before comparison can proceed.

---

## 6. SAI Confidence Behavior

Consistent with `decision_governance.md`:

- Confidence means methodology/signal alignment — NOT certainty
- Confidence does NOT authorize final registry creation
- Confidence does NOT authorize trading or execution
- Confidence must DECREASE when:
  - Source authority is incomplete (Q6 NUMERIC_THRESHOLDS_DEFERRED, Q7 EVIDENCE_INSUFFICIENT)
  - Identity is unresolved
  - Governance state is under_review or overdue
  - Comparability evidence is incomplete (comparability_adjustment_required but note empty)
  - Market data fields are null (reduced data_quality_status)

High confidence in methodology compatibility means: "Multiple methodology dimensions are consistently satisfied." It does NOT mean: "The peer group is ready for production use."

---

## 7. Human Review Boundary

SAI compatibility verification does NOT approve production use. Human review is required before:
- Any future SAI integration with PGMF
- Any peer group registry creation
- Any runtime implementation
- Any methodology activation
- Any peer assignment

This document verifies architectural compatibility only — it does not authorize operational deployment.

---

## 8. Future Integration Readiness

SAI may only become operationally connected to PGMF through a future implementation spec that separately defines:
- Input contracts (what SAI consumes from the registry)
- Output contracts (what SAI produces from peer definitions)
- Schema references (which PGMF fields SAI reads)
- Validation logic (how SAI verifies record integrity)
- Block-state semantics (how SAI handles each block condition at runtime)
- Audit behavior (how SAI logs governance-aware decisions)
- Test coverage (verification that all scenarios A–L are tested)
- Governance approval (CTO sign-off on integration design)
- Human approval (additive-only extension principle)

---

## 9. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml | CONFIRMED |
| No final peer assignments | CONFIRMED |
| No canonical peer_group_id | CONFIRMED |
| No SAI artifact mutation | CONFIRMED |
| No SAI runtime code | CONFIRMED |
| No validation code | CONFIRMED |
| No market data | CONFIRMED |
| No broker/exchange/ATS | CONFIRMED |
| No order routing | CONFIRMED |
| No execution logic | CONFIRMED |
| No compliance claim | CONFIRMED |
| Tasks 1–9 unchanged | CONFIRMED |
| Task 11 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_10_SAI_COMPATIBILITY_VERIFICATION_READY_FOR_HUMAN_REVIEW
```

---

*End of SAI compatibility verification.*
