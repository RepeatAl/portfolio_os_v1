# Single Asset Intelligence Framework — Signal-to-Block Consumption Matrix

**Artifact**: signal_consumption_matrix.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 3.1 Create signal-to-block consumption matrix
**Requirements**: SAI-REQ-3 (Signal Consumption Contracts)
**Verification Gate**: VG-SAI-7 (Signal Coverage Gate)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the complete mapping between the 23 canonical signal categories (from the Market Evidence Framework preflight inventory) and the 24 SAI analysis blocks. It establishes which blocks consume which signals, ensuring full coverage and no orphan signals or signal-starved blocks.

This is a definition-layer artifact. It contains no implementation code, no calculation formulas, no scoring logic, no allocation decisions, and no executable architecture.

(See: design.md, Section: Evidence Consumption Design)
(See: requirements.md, Section: SAI-REQ-3 — Signal Consumption Contracts)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 9. Canonical Signal Categories)

---

## 2. Consumption Matrix Principles

1. **Many-to-many**: A signal category may be consumed by multiple blocks; a block may consume multiple signal categories.
2. **Primary vs. Secondary**: Each signal has one primary consuming block (where it is the core diagnostic input) and zero or more secondary consumers (where it provides supporting context).
3. **Declarative only**: This matrix declares consumption relationships. It does NOT define signal calculation formulas, retrieval logic, or threshold values.
4. **Signal Calculation Framework responsibility**: How signals are computed from facts is defined by the Signal Calculation Framework (deferred). SAI only declares what it consumes.
5. **No new signal creation**: Only the 23 enumerated signal categories from the preflight inventory are used. No new signal IDs are invented.
6. **Deferred interface notes**: Blocks whose taxonomy describes signal families NOT in the 23 enumerated categories are marked with deferred interface notes.

---

## 3. Signal-Centric Consumption Matrix

This table maps each of the 23 signal categories to their consuming blocks.

| # | Signal Category ID | Primary Consumer(s) | Secondary Consumer(s) |
|---|---|---|---|
| 1 | `revenue_quality_signal` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-15 (Earnings Quality) |
| 2 | `demand_visibility_signal` | SAI-BLK-04 (Demand/Pipeline) | SAI-BLK-03 (Revenue Quality) |
| 3 | `margin_durability_signal` | SAI-BLK-05 (Margin Quality) | SAI-BLK-06 (Cashflow Quality), SAI-BLK-15 (Earnings Quality) |
| 4 | `cashflow_conversion_signal` | SAI-BLK-06 (Cashflow Quality) | SAI-BLK-15 (Earnings Quality), SAI-BLK-18 (Value Trap Guard) |
| 5 | `liquidity_stress_signal` | SAI-BLK-07 (Balance Sheet Quality) | SAI-BLK-08 (Credit/Solvency Risk) |
| 6 | `refinancing_risk_signal` | SAI-BLK-07 (Balance Sheet Quality) | SAI-BLK-08 (Credit/Solvency Risk) |
| 7 | `interest_coverage_deterioration_signal` | SAI-BLK-08 (Credit/Solvency Risk) | SAI-BLK-07 (Balance Sheet Quality) |
| 8 | `pension_underfunding_signal` | SAI-BLK-10 (Pension Obligations) | — |
| 9 | `off_balance_sheet_leverage_signal` | SAI-BLK-09 (Hidden Liabilities) | SAI-BLK-08 (Credit/Solvency Risk) |
| 10 | `working_capital_stress_signal` | SAI-BLK-11 (Working Capital) | SAI-BLK-06 (Cashflow Quality) |
| 11 | `customer_concentration_risk_signal` | SAI-BLK-12 (Customer Concentration) | SAI-BLK-03 (Revenue Quality) |
| 12 | `supply_chain_fragility_signal` | SAI-BLK-13 (Supply Chain Stability) | — |
| 13 | `earnings_quality_signal` | SAI-BLK-15 (Earnings Quality) | SAI-BLK-18 (Value Trap Guard) |
| 14 | `estimate_revision_signal` | SAI-BLK-16 (Guidance/Estimate Revisions) | SAI-BLK-22 (Company Outlook) |
| 15 | `guidance_quality_signal` | SAI-BLK-16 (Guidance/Estimate Revisions) | SAI-BLK-22 (Company Outlook) |
| 16 | `valuation_stretch_signal` | SAI-BLK-17 (Valuation Context) | SAI-BLK-18 (Value Trap Guard) |
| 17 | `valuation_trap_risk_signal` | SAI-BLK-18 (Value Trap Guard) | SAI-BLK-17 (Valuation Context) |
| 18 | `relative_strength_signal` | SAI-BLK-19 (Relative Strength) | SAI-BLK-21 (Peer Comparison) |
| 19 | `peer_divergence_signal` | SAI-BLK-21 (Peer Comparison) | SAI-BLK-19 (Relative Strength) |
| 20 | `benchmark_beta_signal` | SAI-BLK-20 (Benchmark/Sector/Peer Correlation) | SAI-BLK-19 (Relative Strength) |
| 21 | `correlation_dependency_signal` | SAI-BLK-20 (Benchmark/Sector/Peer Correlation) | — |
| 22 | `outlook_revision_signal` | SAI-BLK-22 (Company Outlook) | SAI-BLK-23 (Asset-Class Outlook) |
| 23 | `portfolio_fit_signal` | SAI-BLK-24 (Portfolio Fit) | — |

---

## 4. Block-Centric Signal Consumption View

This section lists each of the 24 blocks and the signal categories it consumes, with interpretive context.

---

### SAI-BLK-01: Asset Identity (Foundation)

| Role | Signal Categories |
|------|------------------|
| Primary | — |
| Secondary | — |

**Deferred Interface Note**: The block taxonomy defines signal families "Classification signals, sector rotation signals" for this block. These signal families are described in the block taxonomy but are NOT enumerated in the preflight's 23 canonical signal categories. Signal coverage for this block is deferred pending future signal inventory expansion or Signal Calculation Framework resolution.

**Interpretive Context**: Asset Identity establishes canonical classification. When classification or sector rotation signals become enumerated, they would inform reclassification detection and sector rotation exposure.

---

### SAI-BLK-02: Business Model Quality (Foundation)

| Role | Signal Categories |
|------|------------------|
| Primary | — |
| Secondary | — |

**Deferred Interface Note**: The block taxonomy defines signal families "Business model durability signals, competitive advantage signals" for this block. These signal families are described in the block taxonomy but are NOT enumerated in the preflight's 23 canonical signal categories. Signal coverage for this block is deferred pending future signal inventory expansion or Signal Calculation Framework resolution.

**Interpretive Context**: Business Model Quality diagnoses structural business model sustainability. When business model durability and competitive advantage signals become enumerated, they would inform moat erosion detection and business model fragility assessment.

---

### SAI-BLK-03: Revenue Quality (Operational)

| Role | Signal Categories |
|------|------------------|
| Primary | `revenue_quality_signal` |
| Secondary | `demand_visibility_signal`, `customer_concentration_risk_signal` |

**Interpretive Context**: Revenue Quality consumes the revenue quality signal as its core diagnostic input — assessing revenue health, growth quality, durability, and mix. Demand visibility provides forward context for revenue sustainability. Customer concentration risk provides dependency context for revenue fragility assessment.

---

### SAI-BLK-04: Demand/Pipeline (Operational)

| Role | Signal Categories |
|------|------------------|
| Primary | `demand_visibility_signal` |
| Secondary | — |

**Interpretive Context**: Demand/Pipeline consumes the demand visibility signal as its core input — assessing forward demand confidence based on pipeline, backlog, and order indicators. This signal directly informs the block's purpose of diagnosing demand trajectory and pipeline health.

---

### SAI-BLK-05: Margin Quality (Operational)

| Role | Signal Categories |
|------|------------------|
| Primary | `margin_durability_signal` |
| Secondary | — |

**Interpretive Context**: Margin Quality consumes the margin durability signal as its core diagnostic — assessing margin sustainability, compression risk, and structural trend. The signal informs whether margins are structurally sound or under pressure.

---

### SAI-BLK-06: Cashflow Quality (Operational)

| Role | Signal Categories |
|------|------------------|
| Primary | `cashflow_conversion_signal` |
| Secondary | `margin_durability_signal`, `working_capital_stress_signal` |

**Interpretive Context**: Cashflow Quality consumes the cashflow conversion signal as its primary diagnostic — assessing earnings-to-cash conversion quality. Margin durability provides context for whether margin trends affect cash generation. Working capital stress signals whether cash is being consumed by operational inefficiency.

---

### SAI-BLK-07: Balance Sheet Quality (Financial Stability)

| Role | Signal Categories |
|------|------------------|
| Primary | `liquidity_stress_signal`, `refinancing_risk_signal` |
| Secondary | `interest_coverage_deterioration_signal` |

**Interpretive Context**: Balance Sheet Quality consumes liquidity stress and refinancing risk as its core signals — assessing near-term liquidity adequacy and debt maturity wall exposure. Interest coverage deterioration provides supporting evidence of balance sheet strain from a debt-servicing perspective.

---

### SAI-BLK-08: Credit/Solvency Risk (Financial Stability)

| Role | Signal Categories |
|------|------------------|
| Primary | `interest_coverage_deterioration_signal` |
| Secondary | `liquidity_stress_signal`, `refinancing_risk_signal`, `off_balance_sheet_leverage_signal` |

**Interpretive Context**: Credit/Solvency Risk consumes interest coverage deterioration as its primary signal — assessing the trend in ability to service debt obligations. Liquidity stress, refinancing risk, and off-balance-sheet leverage provide supporting context for comprehensive solvency assessment.

---

### SAI-BLK-09: Hidden Liabilities (Financial Stability)

| Role | Signal Categories |
|------|------------------|
| Primary | `off_balance_sheet_leverage_signal` |
| Secondary | — |

**Interpretive Context**: Hidden Liabilities consumes the off-balance-sheet leverage signal as its core diagnostic — detecting hidden leverage from operating leases, guarantees, and other off-balance-sheet items that distort the true liability profile.

---

### SAI-BLK-10: Pension Obligations (Financial Stability)

| Role | Signal Categories |
|------|------------------|
| Primary | `pension_underfunding_signal` |
| Secondary | — |

**Interpretive Context**: Pension Obligations consumes the pension underfunding signal as its sole signal input — assessing pension obligation risk relative to company resources, funding gap trajectory, and actuarial assumption sensitivity.

---

### SAI-BLK-11: Working Capital (Operational)

| Role | Signal Categories |
|------|------------------|
| Primary | `working_capital_stress_signal` |
| Secondary | — |

**Interpretive Context**: Working Capital consumes the working capital stress signal as its core input — detecting working capital efficiency deterioration through cash conversion cycle health, inventory buildup, and collection quality trends.

---

### SAI-BLK-12: Customer Concentration (Risk)

| Role | Signal Categories |
|------|------------------|
| Primary | `customer_concentration_risk_signal` |
| Secondary | — |

**Interpretive Context**: Customer Concentration consumes the customer concentration risk signal as its core diagnostic — assessing revenue dependency risk from top-customer concentration, contract fragility, and switching cost adequacy.

---

### SAI-BLK-13: Supply Chain Stability (Risk)

| Role | Signal Categories |
|------|------------------|
| Primary | `supply_chain_fragility_signal` |
| Secondary | — |

**Interpretive Context**: Supply Chain Stability consumes the supply chain fragility signal as its core diagnostic — assessing supply chain risk from supplier concentration, geographic sourcing dependency, and single-source vulnerability.

---

### SAI-BLK-14: Pricing Power (Operational)

| Role | Signal Categories |
|------|------------------|
| Primary | — |
| Secondary | — |

**Deferred Interface Note**: The block taxonomy defines signal families "Pricing power signals, pass-through ability signals, elasticity indicators" for this block. These signal families are described in the block taxonomy but are NOT enumerated in the preflight's 23 canonical signal categories. Signal coverage for this block is deferred pending future signal inventory expansion or Signal Calculation Framework resolution.

**Interpretive Context**: Pricing Power diagnoses ability to maintain or increase prices without demand destruction. When pricing power, pass-through ability, and elasticity signals become enumerated, they would inform price/volume decomposition analysis and competitive pricing constraint detection.

---

### SAI-BLK-15: Earnings Quality (Earnings)

| Role | Signal Categories |
|------|------------------|
| Primary | `earnings_quality_signal` |
| Secondary | `revenue_quality_signal`, `margin_durability_signal`, `cashflow_conversion_signal` |

**Interpretive Context**: Earnings Quality consumes the earnings quality signal as its core diagnostic — assessing reported earnings reliability and sustainability. Revenue quality provides input quality context. Margin durability and cashflow conversion provide cross-validation evidence for accrual-vs-cash divergence detection.

---

### SAI-BLK-16: Guidance/Estimate Revisions (Earnings)

| Role | Signal Categories |
|------|------------------|
| Primary | `estimate_revision_signal`, `guidance_quality_signal` |
| Secondary | — |

**Interpretive Context**: Guidance/Estimate Revisions consumes both estimate revision and guidance quality signals as its dual primary inputs — assessing consensus estimate trajectory (direction and magnitude) alongside management guidance credibility and revision patterns.

---

### SAI-BLK-17: Valuation Context (Valuation)

| Role | Signal Categories |
|------|------------------|
| Primary | `valuation_stretch_signal` |
| Secondary | `valuation_trap_risk_signal` |

**Interpretive Context**: Valuation Context consumes the valuation stretch signal as its primary diagnostic — assessing current valuation relative to historical and peer context. Valuation trap risk provides supporting context for detecting conditions where apparent cheapness may mask impairment. Note: Valuation interpretation requires cross-reference evidence from multiple evidence dimensions — this is handled via shared underlying facts/signals, not block-to-block dependency.

---

### SAI-BLK-18: Value Trap Guard (Valuation)

| Role | Signal Categories |
|------|------------------|
| Primary | `valuation_trap_risk_signal` |
| Secondary | `valuation_stretch_signal`, `cashflow_conversion_signal`, `earnings_quality_signal` |

**Interpretive Context**: Value Trap Guard consumes the valuation trap risk signal as its primary diagnostic — detecting probability that low valuation reflects structural impairment rather than opportunity. Valuation stretch provides the "cheapness" context. Cashflow conversion and earnings quality provide the fundamental deterioration evidence needed to distinguish structural impairment from cyclical discount.

---

### SAI-BLK-19: Relative Strength (Market Position)

| Role | Signal Categories |
|------|------------------|
| Primary | `relative_strength_signal` |
| Secondary | `benchmark_beta_signal`, `peer_divergence_signal` |

**Interpretive Context**: Relative Strength consumes the relative strength signal as its primary diagnostic — assessing momentum relative to benchmark, sector, and peers. Benchmark beta provides context for whether strength is own-driven or beta-driven. Peer divergence signals whether relative performance reflects company-specific factors.

---

### SAI-BLK-20: Benchmark/Sector/Peer Correlation (Market Position)

| Role | Signal Categories |
|------|------------------|
| Primary | `benchmark_beta_signal`, `correlation_dependency_signal` |
| Secondary | — |

**Interpretive Context**: Benchmark/Sector/Peer Correlation consumes benchmark beta and correlation dependency signals as its dual primary inputs — diagnosing whether the asset moves by own strength or is dragged by index/sector correlation, and the degree of co-movement dependence on external factors.

---

### SAI-BLK-21: Peer Comparison (Market Position)

| Role | Signal Categories |
|------|------------------|
| Primary | `peer_divergence_signal` |
| Secondary | `relative_strength_signal` |

**Interpretive Context**: Peer Comparison consumes the peer divergence signal as its primary diagnostic — assessing the degree of divergence from peer group behavior. Relative strength provides supporting context for competitive positioning interpretation. Note: peer groups are non-canonical until Peer Group Registry exists.

---

### SAI-BLK-22: Company Outlook (Outlook)

| Role | Signal Categories |
|------|------------------|
| Primary | `outlook_revision_signal` |
| Secondary | `estimate_revision_signal`, `guidance_quality_signal` |

**Interpretive Context**: Company Outlook consumes the outlook revision signal as its primary diagnostic — detecting changes in forward outlook assessment. Estimate revision and guidance quality provide supporting evidence for outlook trajectory validation from the earnings/guidance perspective.

---

### SAI-BLK-23: Asset-Class Outlook (Outlook)

| Role | Signal Categories |
|------|------------------|
| Primary | — |
| Secondary | `outlook_revision_signal` |

**Deferred Interface Note**: The block taxonomy defines signal families "Sector rotation signals, regulatory risk signals, cycle position signals" for this block. The only preflight-enumerated signal that partially overlaps is `outlook_revision_signal` (consumed as secondary context). The full signal family coverage described in the taxonomy is NOT enumerated in the preflight's 23 canonical signal categories. Primary signal coverage for this block is deferred pending future signal inventory expansion or Signal Calculation Framework resolution.

**Interpretive Context**: Asset-Class Outlook diagnoses asset-class-level conditions. The outlook revision signal provides company-level outlook context that may inform broader asset-class assessment. Full sector rotation, regulatory risk, and cycle position signals await enumeration.

---

### SAI-BLK-24: Portfolio Fit (Portfolio Context)

| Role | Signal Categories |
|------|------------------|
| Primary | `portfolio_fit_signal` |
| Secondary | — |

**Interpretive Context**: Portfolio Fit consumes the portfolio fit signal as its sole primary input — assessing asset contribution to portfolio diversification, concentration, and fit within portfolio-level constructs.

---

## 5. Coverage Summary

### 5.1 Signal Category Coverage

| Metric | Value |
|--------|-------|
| Total signal categories in preflight inventory | 23 |
| Signal categories mapped to ≥1 block | 23 |
| Signal categories unmapped | 0 |

**Result**: All 23 canonical signal categories are assigned to at least one block. Zero orphan signals exist.

### 5.2 Block Signal Coverage

| Metric | Value |
|--------|-------|
| Total blocks in SAI taxonomy | 24 |
| Blocks with ≥1 signal category assigned (primary or secondary) | 20 |
| Blocks with deferred-only signal coverage | 4 |

**Blocks with ≥1 enumerated signal category**:

| Block ID | Block Name | Signal Count (Primary + Secondary) |
|----------|-----------|-------------------------------------|
| SAI-BLK-03 | Revenue Quality | 3 (1P + 2S) |
| SAI-BLK-04 | Demand/Pipeline | 1 (1P) |
| SAI-BLK-05 | Margin Quality | 1 (1P) |
| SAI-BLK-06 | Cashflow Quality | 3 (1P + 2S) |
| SAI-BLK-07 | Balance Sheet Quality | 3 (2P + 1S) |
| SAI-BLK-08 | Credit/Solvency Risk | 4 (1P + 3S) |
| SAI-BLK-09 | Hidden Liabilities | 1 (1P) |
| SAI-BLK-10 | Pension Obligations | 1 (1P) |
| SAI-BLK-11 | Working Capital | 1 (1P) |
| SAI-BLK-12 | Customer Concentration | 1 (1P) |
| SAI-BLK-13 | Supply Chain Stability | 1 (1P) |
| SAI-BLK-15 | Earnings Quality | 4 (1P + 3S) |
| SAI-BLK-16 | Guidance/Estimate Revisions | 2 (2P) |
| SAI-BLK-17 | Valuation Context | 2 (1P + 1S) |
| SAI-BLK-18 | Value Trap Guard | 4 (1P + 3S) |
| SAI-BLK-19 | Relative Strength | 3 (1P + 2S) |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | 2 (2P) |
| SAI-BLK-21 | Peer Comparison | 2 (1P + 1S) |
| SAI-BLK-22 | Company Outlook | 3 (1P + 2S) |
| SAI-BLK-24 | Portfolio Fit | 1 (1P) |

**Blocks with deferred-only signal coverage (no enumerated signal category assigned as primary)**:

| Block ID | Block Name | Reason | Deferred Interface Note |
|----------|-----------|--------|-------------------------|
| SAI-BLK-01 | Asset Identity | Signal families "Classification signals, sector rotation signals" described in block taxonomy but NOT enumerated in preflight signal inventory | Deferred: signal categories described in block taxonomy but not enumerated in preflight signal inventory. Coverage depends on future Signal Calculation Framework or signal inventory expansion. |
| SAI-BLK-02 | Business Model Quality | Signal families "Business model durability signals, competitive advantage signals" described in block taxonomy but NOT enumerated in preflight signal inventory | Deferred: signal categories described in block taxonomy but not enumerated in preflight signal inventory. Coverage depends on future Signal Calculation Framework or signal inventory expansion. |
| SAI-BLK-14 | Pricing Power | Signal families "Pricing power signals, pass-through ability signals, elasticity indicators" described in block taxonomy but NOT enumerated in preflight signal inventory | Deferred: signal categories described in block taxonomy but not enumerated in preflight signal inventory. Coverage depends on future Signal Calculation Framework or signal inventory expansion. |
| SAI-BLK-23 | Asset-Class Outlook | Signal families "Sector rotation signals, regulatory risk signals, cycle position signals" described in block taxonomy but NOT enumerated in preflight signal inventory. `outlook_revision_signal` consumed as secondary only. | Deferred: primary signal categories described in block taxonomy but not enumerated in preflight signal inventory. Secondary consumption of `outlook_revision_signal` provides partial coverage. |

### 5.3 Coverage Assessment

- **All 23 signal categories**: Fully mapped — zero orphans.
- **20 of 24 blocks**: Have at least 1 enumerated signal category assigned (primary or secondary).
- **4 of 24 blocks**: Have signal families described in taxonomy but those signal families do not correspond to any of the 23 preflight-enumerated signal categories. These are marked as deferred interface notes. The block taxonomy accurately describes what signals these blocks WILL consume — the gap is that those signals are not yet part of the canonical 23-signal inventory.

This is NOT a design error. The block taxonomy correctly identifies signal needs. The preflight signal inventory covers the core 23 categories. Future signal inventory expansion (via Signal Calculation Framework or additive extension) will close the gap for the 4 deferred blocks.

---

## 6. Deferred Signal Dependencies

The following blocks have signal dependencies that cannot be fully satisfied from the current 23-signal inventory:

### 6.1 SAI-BLK-01 (Asset Identity) — Deferred

**Taxonomy-described signals**: Classification signals, sector rotation signals
**Preflight inventory match**: None of the 23 enumerated signal categories
**Impact**: Block operates on fact families only until classification/sector rotation signals are enumerated
**Resolution path**: Signal Calculation Framework defines and enumerates classification and sector rotation signal categories → added to canonical signal inventory → this matrix updated

### 6.2 SAI-BLK-02 (Business Model Quality) — Deferred

**Taxonomy-described signals**: Business model durability signals, competitive advantage signals
**Preflight inventory match**: None of the 23 enumerated signal categories
**Impact**: Block operates on fact families only until business model signals are enumerated
**Resolution path**: Signal Calculation Framework defines and enumerates business model durability and competitive advantage signal categories → added to canonical signal inventory → this matrix updated

### 6.3 SAI-BLK-14 (Pricing Power) — Deferred

**Taxonomy-described signals**: Pricing power signals, pass-through ability signals, elasticity indicators
**Preflight inventory match**: None of the 23 enumerated signal categories
**Impact**: Block operates on fact families only until pricing power signals are enumerated
**Resolution path**: Signal Calculation Framework defines and enumerates pricing power signal categories → added to canonical signal inventory → this matrix updated

### 6.4 SAI-BLK-23 (Asset-Class Outlook) — Partial Coverage / Deferred

**Taxonomy-described signals**: Sector rotation signals, regulatory risk signals, cycle position signals
**Preflight inventory match**: `outlook_revision_signal` (secondary consumer only — partial overlap)
**Impact**: Block has secondary signal consumption via outlook_revision_signal but lacks primary signal categories for its full diagnostic scope
**Resolution path**: Signal Calculation Framework defines and enumerates sector rotation, regulatory risk, and cycle position signal categories → added to canonical signal inventory → this matrix updated with primary assignments

---

## 7. No-Drift Statement

This artifact:
- **Does NOT** define signal calculation formulas or methodology
- **Does NOT** create new signal category IDs beyond the 23 enumerated in the preflight
- **Does NOT** mutate the Signal Calculation Framework
- **Does NOT** mutate the Market Evidence Framework
- **Does NOT** create implementation code, database schemas, or API designs
- **Does NOT** produce scoring, ranking, recommendation, allocation, or trading logic
- **Does NOT** create facts, signals, or evidence primitive objects
- **Does NOT** create asset-to-narrative mappings
- **Does NOT** mutate any registry or SSOT document

This artifact is a definition-layer consumption matrix ONLY. It declares which blocks consume which signals — nothing more.

---

## 8. VG-SAI-7 Evidence Statement

**Verification Gate**: VG-SAI-7 (Signal Coverage Gate)
**Gate Status**: EVIDENCE PROVIDED — awaiting explicit gate execution

This artifact provides the following evidence toward VG-SAI-7:

| Check | Status | Evidence |
|-------|--------|----------|
| All 23 signal categories assigned to ≥1 block | ✓ COMPLETE | Section 3 maps all 23 signals; Section 5.1 confirms 23/23 mapped |
| All blocks have ≥1 signal assigned | PARTIAL (20/24 enumerated + 4 deferred) | Section 5.2 documents 20 blocks with enumerated signals; 4 blocks have deferred signal families not in the 23-signal inventory |
| Signal consumption matrix complete | ✓ COMPLETE | Section 3 (signal-centric) and Section 4 (block-centric) provide full bidirectional mapping |
| No signal categories referenced outside preflight inventory | ✓ COMPLETE | Only the 23 preflight-enumerated signal category IDs are used |
| Deferred dependencies documented | ✓ COMPLETE | Section 6 documents all 4 deferred blocks with rationale and resolution path |

**Gate Interpretation Note**: The 4 blocks with deferred-only signal coverage (SAI-BLK-01, SAI-BLK-02, SAI-BLK-14, SAI-BLK-23) have signal families described in the block taxonomy but those families are not part of the 23 enumerated signal categories. This is an interface gap between the block taxonomy (which correctly anticipates future signals) and the current signal inventory (which defines exactly 23 categories). The gap is acknowledged, documented, and does not represent a mapping error. These blocks still consume fact families and operate validly at reduced signal richness.

**VG-SAI-7 is NOT passed by this artifact**. This artifact provides evidence only. The gate must be explicitly executed in a separate verification gate artifact (`gate_vg_sai_07.md`) with PASS/FAIL determination.

(See: tasks.md, Section: 15.7 Execute VG-SAI-7 Signal Coverage Gate)

---

## 9. Cross-References

- (See: block_taxonomy.md, Section: All block definitions — signal_families fields)
- (See: fact_consumption_matrix.md, Section: Complementary fact-to-block mapping)
- (See: design.md, Section: Evidence Consumption Design)
- (See: design.md, Section: Deferred Interface Design — Signal Calculation Framework)
- (See: requirements.md, Section: SAI-REQ-3 — Signal Consumption Contracts)
- (See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 9. Canonical Signal Categories)

---

*End of artifact.*
