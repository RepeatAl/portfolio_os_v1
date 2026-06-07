# Single Asset Intelligence Framework

## 1. Purpose and Scope

SAI is the canonical asset-level diagnostic layer between the Market Evidence Framework (facts/signals) and downstream portfolio/reporting layers. It organizes evidence about individual assets into 24 structured analysis blocks for diagnostic interpretation.

SAI is **diagnostic and interpretive ONLY** — definition-layer in the current phase. It does not produce scores, recommendations, or actionable trading signals. It interprets evidence with full provenance tracing.

---

## 2. What SAI Is

- Canonical asset-level diagnostic framework
- 24 analysis blocks organizing evidence interpretation
- Consumes facts from Market Evidence Framework
- Consumes calculated signals from Signal Calculation Framework
- Produces diagnostic interpretations with provenance
- Definition-layer architecture (no implementation code)

SAI exists to provide structured, auditable, block-level diagnostic output for each asset under analysis. Each block has defined inputs (facts/signals), defined outputs (interpretation objects), and defined boundaries (what it does NOT produce).

---

## 3. What SAI Is NOT

SAI does **NOT**:

- Create implementation code
- Create database schemas
- Create API contracts
- Create runtime architecture
- Create facts, signals, or evidence primitives
- Mutate Market Evidence Framework
- Mutate Signal Calculation Framework
- Mutate registries or SSOT files
- Create scoring, ranking, or recommendations
- Create allocation, trading, or position sizing
- Create target weights, price targets, or fair value
- Create expected return, conviction, or buy/sell/hold signals
- Create portfolio optimization
- Create asset-to-narrative mappings
- Create peer groups
- Create Portfolio Health methodology
- Create Valuation methodology
- Create Earnings methodology
- Replace human PM decision-making

---

## 4. Definition-Layer Status

All artifacts in this specification are **documentation and specification only**. No executable logic exists. No runtime code is produced. No database schemas are created. No API endpoints are defined.

This is a pure definition-layer framework that specifies:
- What blocks exist
- What each block consumes
- What each block produces
- What boundaries each block respects
- What red flags each block can raise

---

## 5. Canonical Artifact Map

| Artifact | Description |
|----------|-------------|
| `requirements.md` | 15 SAI requirements (SAI-REQ-1 through SAI-REQ-15) |
| `design.md` | Architecture, components, data models, correctness properties |
| `tasks.md` | Implementation plan with 18 tasks |
| `artifacts/block_taxonomy.md` | 24 canonical blocks |
| `artifacts/fact_consumption_matrix.md` | 68 fact categories mapped to blocks |
| `artifacts/signal_consumption_matrix.md` | 23 signal categories mapped to blocks |
| `artifacts/output_object_spec.md` | Output object schema and prohibited fields |
| `artifacts/provenance_contract.md` | Provenance chain requirements |
| `artifacts/red_flag_taxonomy.md` | 48 red flags across 24 blocks |
| `artifacts/temporal_resolution_matrix.md` | Temporal class per block |
| `artifacts/deferred_interfaces.md` | 7 deferred framework contracts |
| `artifacts/valuation_boundary.md` | Valuation/value-trap interpretation boundary |
| `artifacts/credit_solvency.md` | Financial stability boundary (4 blocks) |
| `artifacts/peer_benchmark.md` | Market position boundary (3 blocks) |
| `artifacts/portfolio_fit_interface.md` | Portfolio fit output interface |
| `artifacts/kpi_mapping_validation.md` | KPI mapping (20/20 available items) |
| `artifacts/terminology_audit.md` | Cross-framework terminology consistency |
| `gates/` | 12 verification gate execution artifacts (VG-SAI-1 through VG-SAI-12) |

---

## 6. How to Read the Artifacts

**Recommended reading order:**

1. **`block_taxonomy.md`** — Start here. Understand the 24-block structure, block categories, and what each block is responsible for.
2. **`fact_consumption_matrix.md`** and **`signal_consumption_matrix.md`** — Understand what evidence each block consumes. These define the input contracts.
3. **`output_object_spec.md`** — Understand what each block produces. This defines the output contract and prohibited fields.
4. **`red_flag_taxonomy.md`** — Understand what diagnostic warnings each block can raise.
5. **Domain artifacts** (`valuation_boundary.md`, `credit_solvency.md`, `peer_benchmark.md`, `portfolio_fit_interface.md`) — For specific block boundary details.
6. **`provenance_contract.md`** — For provenance chain and no-orphan rule details.
7. **`deferred_interfaces.md`** — For understanding what SAI expects from frameworks not yet defined.

---

## 7. Canonical Block List

| Block ID | Block Name | Category |
|----------|-----------|----------|
| SAI-BLK-01 | Asset Identity | Foundation |
| SAI-BLK-02 | Business Model Quality | Foundation |
| SAI-BLK-03 | Revenue Quality | Operational |
| SAI-BLK-04 | Demand/Pipeline | Operational |
| SAI-BLK-05 | Margin Quality | Operational |
| SAI-BLK-06 | Cashflow Quality | Operational |
| SAI-BLK-07 | Balance Sheet Quality | Financial Stability |
| SAI-BLK-08 | Credit/Solvency Risk | Financial Stability |
| SAI-BLK-09 | Hidden Liabilities | Financial Stability |
| SAI-BLK-10 | Pension Obligations | Financial Stability |
| SAI-BLK-11 | Working Capital | Operational |
| SAI-BLK-12 | Customer Concentration | Risk |
| SAI-BLK-13 | Supply Chain Stability | Risk |
| SAI-BLK-14 | Pricing Power | Operational |
| SAI-BLK-15 | Earnings Quality | Earnings |
| SAI-BLK-16 | Guidance/Estimate Revisions | Earnings |
| SAI-BLK-17 | Valuation Context | Valuation |
| SAI-BLK-18 | Value Trap Guard | Valuation |
| SAI-BLK-19 | Relative Strength | Market Position |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Market Position |
| SAI-BLK-21 | Peer Comparison | Market Position |
| SAI-BLK-22 | Company Outlook | Outlook |
| SAI-BLK-23 | Asset-Class Outlook | Outlook |
| SAI-BLK-24 | Portfolio Fit | Portfolio Context |

**Category summary:** Foundation (2), Operational (6), Financial Stability (4), Risk (2), Earnings (2), Valuation (2), Market Position (3), Outlook (2), Portfolio Context (1).

---

## 8. Relationship to Market Evidence Framework

SAI **consumes** from the Market Evidence Framework (MEF):

- **Observed_Facts**: Raw factual evidence (earnings reports, filings, price data, credit ratings, etc.)
- **Calculated_Signals**: Derived signals computed from observed facts (momentum, volatility, trend metrics, etc.)

SAI does **NOT** create facts or signals. It only interprets them.

**Evidence mapping:**
- 68 fact categories mapped to blocks (see `fact_consumption_matrix.md`)
- 23 signal categories mapped to blocks (see `signal_consumption_matrix.md`)

The relationship is strictly one-directional: MEF → SAI. SAI never writes back to MEF.

---

## 9. Relationship to Deferred Downstream Frameworks

SAI declares interface expectations for 7 frameworks that do not yet exist:

| # | Deferred Framework | SAI Dependency |
|---|-------------------|----------------|
| 1 | Valuation Framework | SAI-BLK-17, SAI-BLK-18 expect valuation model outputs |
| 2 | Earnings Intelligence Framework | SAI-BLK-15, SAI-BLK-16 expect earnings model outputs |
| 3 | Peer Group Registry | SAI-BLK-21 expects peer group definitions |
| 4 | Portfolio Health Framework | SAI-BLK-24 expects portfolio context |
| 5 | Correlation/Dependency Framework | SAI-BLK-20 expects correlation data |
| 6 | Signal Calculation Framework | Multiple blocks expect signal family taxonomy |
| 7 | Data Ingestion/Normalization Framework | All blocks expect normalized fact inputs |

SAI declares what it expects from these frameworks. SAI does **NOT** define these frameworks. See `deferred_interfaces.md` for full contract specifications.

---

## 10. Output Object Summary

Each block produces a structured output object containing:

| Field | Description |
|-------|-------------|
| `block_id` | Canonical block identifier (e.g., SAI-BLK-01) |
| `asset_id` | Asset under analysis |
| `consumed_facts` | List of fact IDs consumed with timestamps |
| `consumed_signals` | List of signal IDs consumed with timestamps |
| `interpretation_summary` | Diagnostic text interpretation |
| `red_flags` | Array of triggered red flags (if any) |
| `evidence_completeness` | Completeness metric for consumed evidence |
| `temporal_status` | Current/stale/expired status |
| `provenance_chain` | Full trace from interpretation back to source facts |
| `deferred_dependency_notes` | Notes on unavailable deferred framework inputs |

### Prohibited Output Fields

The following fields are **strictly prohibited** in any SAI output object:

- `score`, `rank`, `recommendation`
- `target_weight`, `position_size`, `price_target`
- `fair_value`, `buy`, `sell`, `hold`
- `probability`, `expected_return`, `alpha`
- `confidence_score`, `conviction`, `risk_score`
- `overvalued`, `undervalued`, `fairly_valued`
- `buy_signal`, `sell_signal`, `hold_signal`

These fields belong to downstream decision-making frameworks and are outside SAI's diagnostic mandate.

---

## 11. Provenance and No-Orphan Rule

### Provenance Contract

Every interpretation produced by SAI MUST trace to specific fact/signal IDs with timestamps. The provenance chain establishes:

- **What** evidence was consumed
- **When** it was consumed (temporal anchor)
- **Which** block produced the interpretation
- **How** the interpretation relates to the consumed evidence

### No-Orphan Rule

An output without provenance is **invalid**. There are no orphan interpretations in SAI.

- Every `interpretation_summary` must reference at least one consumed fact or signal
- Every `red_flag` must reference the evidence that triggered it
- If evidence is unavailable, the block produces a `deferred_dependency_note` rather than an unsupported interpretation

---

## 12. Red Flag Taxonomy Summary

SAI defines **48 red flags** distributed across all 24 blocks (minimum 2 per block).

### Severity Levels (categorical only)

| Severity | Meaning |
|----------|---------|
| `informational` | Observation worth noting; no immediate concern |
| `elevated` | Pattern requires monitoring; potential diagnostic concern |
| `critical` | Significant diagnostic warning; evidence strongly suggests issue |

### Non-Action Principle

Red flags are diagnostic observations. They do **NOT**:
- Trigger actions
- Map to buy/sell/hold decisions
- Aggregate into composite scores
- Generate recommendations
- Override human PM judgment

See `red_flag_taxonomy.md` for the complete 48-flag specification.

---

## 13. Temporal Resolution Summary

| Temporal Class | Block Count | Basis |
|---------------|-------------|-------|
| Quarterly | 18 | Filing-based (earnings, 10-Q, 10-K) |
| Daily | 6 | Market-relative (price, volume, momentum) |

### Stale/Expired Thresholds

- **Quarterly blocks**: Stale after >100 days from last filing; expired after >120 days
- **Daily blocks**: Stale after 2 trading days; expired after 5 trading days

### Real-Time Exception

Real-time resolution is exceptional and NOT the default. No block operates on real-time by default. Real-time is reserved for future implementation phases if required.

See `temporal_resolution_matrix.md` for per-block temporal classification.

---

## 14. Domain Boundary Summaries

### Valuation Boundary (SAI-BLK-17, SAI-BLK-18)

SAI interprets valuation-related evidence (multiples, comps, historical ranges) but does NOT produce:
- Fair value estimates
- Target prices
- Overvalued/undervalued determinations
- Valuation models or DCF outputs

See `valuation_boundary.md` for full specification.

### Credit/Solvency Boundary (SAI-BLK-07, SAI-BLK-08, SAI-BLK-09, SAI-BLK-10)

SAI treats credit ratings and solvency metrics as **input evidence**, not as truth. SAI does NOT:
- Assign credit ratings
- Produce solvency scores
- Override external rating agency assessments

See `credit_solvency.md` for full specification.

### Peer/Benchmark Boundary (SAI-BLK-19, SAI-BLK-20, SAI-BLK-21)

SAI consumes peer group data but does NOT:
- Create peer groups
- Rank assets against peers
- Produce relative performance scores

See `peer_benchmark.md` for full specification.

### Portfolio Fit Boundary (SAI-BLK-24)

SAI produces portfolio context interpretation but has NO allocation authority. SAI does NOT:
- Recommend position sizes
- Suggest target weights
- Optimize portfolio composition

See `portfolio_fit_interface.md` for full specification.

---

## 15. KPI Mapping Status

**VG-SAI-11 is PASS** (amended 2026-06-07).

CTO/operator completeness declaration received. The 20 analysis blocks (Geschäftsmodell through Portfolio Fit) are declared the full and complete canonical KPI-Micro denominator. All 20 items map to valid SAI blocks (100% coverage). ≥80% criterion satisfied.

The Macro KPI List (market/regime monitor categories) is explicitly excluded from the VG-SAI-11 denominator.

---

## 16. Verification Gate Summary

| Gate | Description | Status |
|------|-------------|--------|
| VG-SAI-1 | Requirements Completeness Gate | **PASS** |
| VG-SAI-2 | Boundary Enforcement Gate | **PASS** |
| VG-SAI-3 | Provenance Chain Gate | **PASS** |
| VG-SAI-4 | Interface Contract Gate | **PASS** |
| VG-SAI-5 | Taxonomy Stability Gate | **PASS** |
| VG-SAI-6 | Fact Coverage Gate | **PASS** |
| VG-SAI-7 | Signal Coverage Gate | **PASS** |
| VG-SAI-8 | Red Flag Taxonomy Gate | **PASS** |
| VG-SAI-9 | Temporal Resolution Gate | **PASS** |
| VG-SAI-10 | Cross-Framework Consistency Gate | **PASS** |
| VG-SAI-11 | KPI Mapping Validation Gate | **PASS** (amended 2026-06-07) |
| VG-SAI-12 | Portfolio Fit Interface Gate | **PASS** |

**Summary:** 12/12 PASSED.

---

## 17. Strict Exclusions

SAI does **NOT** — under any circumstance:

- Create implementation code
- Create database schemas
- Create API contracts
- Create runtime architecture
- Create facts, signals, or evidence primitives
- Mutate Market Evidence Framework
- Mutate Signal Calculation Framework
- Mutate registries or SSOT files
- Create scoring, ranking, or recommendations
- Create allocation, trading, or position sizing
- Create target weights, price targets, or fair value
- Create expected return, conviction, or buy/sell/hold signals
- Create portfolio optimization
- Create asset-to-narrative mappings
- Create peer groups
- Create Portfolio Health methodology
- Create Valuation methodology
- Create Earnings methodology
- Replace human PM decision-making

Any artifact, output, or interpretation that violates these exclusions is non-compliant and must be corrected.

---

## 18. Known Unresolved Items

| # | Item | Impact |
|---|------|--------|
| 1 | 4 blocks with deferred signal-family taxonomy-vs-inventory gaps (SAI-BLK-01, SAI-BLK-02, SAI-BLK-14, SAI-BLK-23) | Signal consumption partially unresolvable until Signal Calculation Framework defines taxonomy |
| 2 | Peer Group Registry unavailable: SAI-BLK-21 peer comparison blocked | Block cannot fully operate without peer group definitions |
| 4 | Domainization registry not updated (Task 17 pending) | SAI artifacts not yet registered in `.domainization/artifact_registry.yaml` |

These items require external input or governance coordination to resolve.

---

## 19. Future Handoff Notes

Two tasks remain for SAI completion:

- **Task 17.1 — Registry Readiness Check**: Verify SAI artifacts are ready for registration in the domainization registry. Requires human review of artifact metadata and governance alignment.
- **Task 18.1 — Final Execution Report**: Produce the final SAI execution summary documenting all completed work, verification gate results, and remaining blockers. Requires human review and CTO sign-off.

Both tasks are governance-level activities requiring human coordination. They do not involve creating implementation code or modifying the SAI specification itself.

---

*End of README.*
