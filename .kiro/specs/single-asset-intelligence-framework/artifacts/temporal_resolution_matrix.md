# Single Asset Intelligence Framework — Temporal Resolution Matrix

**Artifact**: temporal_resolution_matrix.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 7.1 Create temporal resolution matrix
**Requirements**: SAI-REQ-6 (Temporal Resolution Requirements)
**Verification Gate**: VG-SAI-9 (Temporal Resolution Gate)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the canonical temporal resolution assignment for every SAI analysis block. It specifies:

- Which temporal class each block belongs to (quarterly, monthly, daily, real-time)
- Why each block requires its assigned frequency (rationale tied to source data cadence)
- When evidence becomes stale or expired per temporal class
- What source cadence dependencies drive the refresh frequency
- Whether real-time operation is prohibited, allowed, or reserved for future consideration

Temporal resolution governs evidence freshness assessment. It does NOT define scheduling, data pipelines, refresh automation, or implementation logic. It is a declaration of minimum data frequency requirements and staleness thresholds.

This is a definition-layer artifact. It contains no implementation code, no schedulers, no refresh logic, no runtime validators, no database schemas, and no API schemas.

(See: design.md, Section: Temporal Resolution Design)
(See: requirements.md, Section: SAI-REQ-6 — Temporal Resolution Requirements)
(See: provenance_contract.md, Section: 4. Evidence Freshness Determination)

---

## 2. Temporal Class Definitions

| Temporal Class | Refresh Requirement | Stale Threshold | Expired Threshold | Block Types | Source Cadence Driver |
|----------------|--------------------|-----------------|--------------------|-------------|----------------------|
| quarterly | Updated after each earnings/filing cycle | > 100 days | > 120 days | Foundation, Operational, Financial Stability, Risk, Earnings, Outlook | Corporate filings (10-Q, 10-K, earnings releases) |
| monthly | Updated monthly for trend detection | > 35 days | > 45 days | Working Capital (optional upgrade) | Intra-quarter operational data, management updates |
| daily | Updated daily from market data feeds | > 2 days | > 5 days | Valuation, Market Position, Portfolio Context | Market prices, trading volumes, index calculations |
| real-time | Exceptional; not default for any block | > 1 hour | > 4 hours | None by default — reserved for future | Streaming market data (future, if implemented) |

### Temporal Class Behavior

- **quarterly**: Evidence tied to corporate disclosure cycles. New filings replace stale evidence. Between filings, existing evidence remains "current" until the stale threshold.
- **monthly**: Evidence benefits from more frequent updates but remains valid between monthly refreshes. Applicable where intra-quarter shifts carry diagnostic value.
- **daily**: Evidence changes with each trading day. Market prices, relative strength, and portfolio weights require daily observation to remain diagnostically meaningful.
- **real-time**: Reserved for future streaming capabilities. Currently no SAI block requires real-time evidence. Real-time creates false precision and imposes disproportionate infrastructure burden relative to diagnostic value.

---

## 3. Full Temporal Resolution Matrix (All 24 Blocks)

### 3.1 Foundation Blocks

#### SAI-BLK-01 — Asset Identity

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-01 |
| block_name | Asset Identity |
| temporal_class | quarterly |
| rationale | Asset identity data (sector classification, listing status, corporate structure) changes only with corporate actions or annual reclassifications. Source data is published in quarterly/annual filings. Daily refresh adds no diagnostic value. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Corporate filings (10-Q, 10-K), sector classification databases, listing exchange data |
| real_time_status | prohibited |

#### SAI-BLK-02 — Business Model Quality

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-02 |
| block_name | Business Model Quality |
| temporal_class | quarterly |
| rationale | Business model characteristics (revenue composition, competitive position, moat indicators) are disclosed in quarterly earnings reports and filings. Business models do not change intra-quarter. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Corporate filings (10-Q, 10-K), earnings call transcripts, segment disclosures |
| real_time_status | prohibited |

---

### 3.2 Operational Blocks

#### SAI-BLK-03 — Revenue Quality

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-03 |
| block_name | Revenue Quality |
| temporal_class | quarterly |
| rationale | Revenue breakdown, geographic mix, customer concentration, and organic growth metrics are reported quarterly. Revenue recognition follows the quarterly disclosure cycle. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly earnings releases, 10-Q segment data, revenue composition disclosures |
| real_time_status | prohibited |

#### SAI-BLK-04 — Demand/Pipeline

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-04 |
| block_name | Demand/Pipeline |
| temporal_class | quarterly |
| rationale | Backlog, bookings, order intake, and pipeline data are disclosed in quarterly filings and earnings calls. Pipeline shifts between filings are not publicly observable. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly earnings releases, management commentary, backlog disclosures, order intake reports |
| real_time_status | prohibited |

#### SAI-BLK-05 — Margin Quality

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-05 |
| block_name | Margin Quality |
| temporal_class | quarterly |
| rationale | Gross margin, operating margin, SGA ratios, and margin trajectories are calculated from quarterly income statements. Margin data is inherently tied to the quarterly reporting cycle. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly income statements, segment profitability, cost structure disclosures |
| real_time_status | prohibited |

#### SAI-BLK-06 — Cashflow Quality

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-06 |
| block_name | Cashflow Quality |
| temporal_class | quarterly |
| rationale | Operating cashflow, FCF, capex, and cash conversion metrics are derived from quarterly cashflow statements. Cash generation quality is assessed on a quarterly disclosure basis. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly cashflow statements, capex disclosures, working capital changes |
| real_time_status | prohibited |

#### SAI-BLK-11 — Working Capital

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-11 |
| block_name | Working Capital |
| temporal_class | quarterly |
| rationale | Receivables, payables, inventory, and cash conversion cycle data are disclosed quarterly. Working capital efficiency is measured from balance sheet snapshots at quarter-end. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly balance sheets, working capital line items, DSO/DPO/inventory days calculations |
| real_time_status | prohibited |

**Note on SAI-BLK-11**: Working Capital has quarterly as its primary temporal class. A monthly optional upgrade is recognized for cases where intra-quarter working capital shifts carry diagnostic value (e.g., seasonal inventory buildup, payment cycle changes). If monthly data becomes available from supplementary sources, this block MAY operate at monthly cadence (stale > 35 days, expired > 45 days) without requiring redesign. The quarterly assignment remains the canonical minimum.

#### SAI-BLK-14 — Pricing Power

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-14 |
| block_name | Pricing Power |
| temporal_class | quarterly |
| rationale | Pricing history, contract escalation clauses, volume-vs-price mix, and competitive pricing context are disclosed in quarterly earnings calls and filings. Pricing power is assessed over quarterly intervals. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly earnings transcripts, pricing disclosures, volume/price mix analysis, contract terms |
| real_time_status | prohibited |

---

### 3.3 Financial Stability Blocks

#### SAI-BLK-07 — Balance Sheet Quality

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-07 |
| block_name | Balance Sheet Quality |
| temporal_class | quarterly |
| rationale | Total assets, equity, debt structure, asset composition, and goodwill/intangibles are reported on quarterly balance sheets. Balance sheet structure changes only with quarterly filings or material corporate actions. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly balance sheets (10-Q, 10-K), asset composition disclosures, goodwill/intangible schedules |
| real_time_status | prohibited |

#### SAI-BLK-08 — Credit/Solvency Risk

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-08 |
| block_name | Credit/Solvency Risk |
| temporal_class | quarterly |
| rationale | Gross debt, net debt, maturity schedules, interest coverage, credit ratings, and covenant data are disclosed in quarterly filings. Debt issuance and refinancing events occur sporadically but are captured in quarterly updates. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly balance sheets, debt maturity schedules, credit rating agency updates, covenant compliance disclosures |
| real_time_status | prohibited |

#### SAI-BLK-09 — Hidden Liabilities

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-09 |
| block_name | Hidden Liabilities |
| temporal_class | quarterly |
| rationale | Off-balance-sheet obligations, contingent liabilities, operating leases, purchase obligations, and litigation exposure are disclosed in quarterly footnotes and MD&A sections. These obligations change with filing updates. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly filing footnotes, contingent liability disclosures, lease schedules, litigation updates |
| real_time_status | prohibited |

#### SAI-BLK-10 — Pension Obligations

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-10 |
| block_name | Pension Obligations |
| temporal_class | quarterly |
| rationale | Defined benefit obligations, plan assets, funding gap, and actuarial assumptions are disclosed in quarterly/annual filings. Pension status changes with actuarial revaluations tied to the reporting cycle. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly/annual pension disclosures, actuarial assumption updates, plan asset reports |
| real_time_status | prohibited |

---

### 3.4 Risk Blocks

#### SAI-BLK-12 — Customer Concentration

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-12 |
| block_name | Customer Concentration |
| temporal_class | quarterly |
| rationale | Top customer revenue share, customer count, contract duration, and switching cost data are disclosed in quarterly filings. Customer relationships shift over quarters, not days. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly revenue disclosures, customer concentration filings (10-K top customer tables), contract announcements |
| real_time_status | prohibited |

#### SAI-BLK-13 — Supply Chain Stability

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-13 |
| block_name | Supply Chain Stability |
| temporal_class | quarterly |
| rationale | Supplier concentration, geographic sourcing, inventory buffers, and lead time data are disclosed in quarterly filings and earnings calls. Supply chain structural data changes with corporate reporting cadence. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly filings, supply chain disclosures, inventory reports, earnings call commentary |
| real_time_status | prohibited |

---

### 3.5 Earnings Blocks

#### SAI-BLK-15 — Earnings Quality

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-15 |
| block_name | Earnings Quality |
| temporal_class | quarterly |
| rationale | EPS composition, non-recurring items, accrual ratios, and audit opinions are tied to quarterly earnings releases. Earnings quality is inherently a quarterly-disclosure metric. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly earnings releases, income statement details, accrual analysis, audit reports |
| real_time_status | prohibited |

#### SAI-BLK-16 — Guidance/Estimate Revisions

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-16 |
| block_name | Guidance/Estimate Revisions |
| temporal_class | quarterly |
| rationale | Management guidance and analyst estimate revisions are published around quarterly earnings cycles. Guidance is updated quarterly; estimate revisions cluster around reporting dates. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly earnings calls, management guidance updates, consensus estimate databases, revision history |
| real_time_status | prohibited |

---

### 3.6 Valuation Blocks

#### SAI-BLK-17 — Valuation Context

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-17 |
| block_name | Valuation Context |
| temporal_class | daily |
| rationale | Valuation multiples (P/E, EV/EBITDA, P/FCF, P/B, dividend yield) are derived from market prices that change every trading day. Historical multiple trajectories require daily price observation for meaningful trend detection. |
| stale_threshold | > 2 days |
| expired_threshold | > 5 days |
| source_cadence_dependency | Daily market prices, trading volumes, market capitalization, enterprise value calculations |
| real_time_status | allowed |

#### SAI-BLK-18 — Value Trap Guard

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-18 |
| block_name | Value Trap Guard |
| temporal_class | daily |
| rationale | Value trap detection requires daily price observation to identify declining multiples coinciding with fundamental deterioration. The "cheap but impaired" condition requires current pricing context combined with fundamental evidence. |
| stale_threshold | > 2 days |
| expired_threshold | > 5 days |
| source_cadence_dependency | Daily market prices, valuation multiple calculations, fundamental deterioration signals |
| real_time_status | allowed |

---

### 3.7 Market Position Blocks

#### SAI-BLK-19 — Relative Strength

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-19 |
| block_name | Relative Strength |
| temporal_class | daily |
| rationale | Relative strength vs. benchmark, sector, and peers requires daily price comparison. Intraday or weekly aggregation misses short-term divergence patterns that signal asset-specific strength vs. beta-driven movement. |
| stale_threshold | > 2 days |
| expired_threshold | > 5 days |
| source_cadence_dependency | Daily asset prices, benchmark index values, sector index values, peer group prices |
| real_time_status | allowed |

#### SAI-BLK-20 — Benchmark/Sector/Peer Correlation

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-20 |
| block_name | Benchmark/Sector/Peer Correlation |
| temporal_class | daily |
| rationale | Correlation coefficients, rolling beta, and R-squared calculations require daily return observations. Correlation regime changes are detectable only with daily granularity. |
| stale_threshold | > 2 days |
| expired_threshold | > 5 days |
| source_cadence_dependency | Daily return series, benchmark returns, sector returns, rolling window calculations |
| real_time_status | allowed |

#### SAI-BLK-21 — Peer Comparison

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-21 |
| block_name | Peer Comparison |
| temporal_class | daily |
| rationale | Competitive positioning relative to peers requires daily market data for relative performance assessment. Peer financial metrics update quarterly, but relative market positioning (price performance, market cap ranking) changes daily. |
| stale_threshold | > 2 days |
| expired_threshold | > 5 days |
| source_cadence_dependency | Daily peer group prices, market capitalizations, relative performance metrics, peer financial data (quarterly overlay) |
| real_time_status | allowed |

---

### 3.8 Outlook Blocks

#### SAI-BLK-22 — Company Outlook

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-22 |
| block_name | Company Outlook |
| temporal_class | quarterly |
| rationale | Forward-looking company diagnostics depend on management commentary, capital allocation plans, strategic initiatives, and M&A activity — all disclosed in quarterly filings and earnings calls. Company outlook does not change meaningfully between filings. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Quarterly earnings calls, strategic initiative disclosures, capital allocation plans, M&A announcements |
| real_time_status | prohibited |

#### SAI-BLK-23 — Asset-Class Outlook

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-23 |
| block_name | Asset-Class Outlook |
| temporal_class | quarterly |
| rationale | Asset-class level conditions (sector fundamentals, regulatory environment, macro sensitivity, industry cycle position) evolve over quarters, not days. Regulatory changes and industry cycle shifts manifest over multi-quarter periods. |
| stale_threshold | > 100 days |
| expired_threshold | > 120 days |
| source_cadence_dependency | Sector reports, regulatory filings, macro indicators, industry cycle data |
| real_time_status | prohibited |

---

### 3.9 Portfolio Context Block

#### SAI-BLK-24 — Portfolio Fit

| Field | Value |
|-------|-------|
| block_id | SAI-BLK-24 |
| block_name | Portfolio Fit |
| temporal_class | daily |
| rationale | Portfolio fit diagnostics (concentration contribution, dependency overlap, diversification context) depend on current portfolio weights and market prices that change daily. A position's portfolio contribution shifts with daily price movements. |
| stale_threshold | > 2 days |
| expired_threshold | > 5 days |
| source_cadence_dependency | Daily portfolio weights, position market values, correlation matrices, concentration calculations |
| real_time_status | allowed |

---

## 4. Rationale: Filing-Based Blocks = Quarterly

**Principle**: Blocks whose primary evidence originates from corporate filings and earnings disclosures are assigned the quarterly temporal class.

**Why quarterly is the correct minimum frequency**:

1. **Source data cadence**: Public companies report financial results quarterly (10-Q) and annually (10-K). The vast majority of fundamental data (revenue, margins, cashflow, balance sheet, debt, working capital, earnings) is only observable when filings are published. No higher-frequency source exists for these metrics.

2. **No intra-quarter observability**: Between filing dates, revenue composition, margin structure, cashflow quality, debt maturity schedules, and hidden liabilities are not publicly observable. Attempting daily or monthly refresh on quarterly data produces no new information — it would recycle stale data without acknowledgment.

3. **Diagnostic validity**: Filing-based blocks produce diagnostics about structural conditions (business model quality, credit risk, pension obligations) that genuinely change on a quarterly cadence. A company's balance sheet quality does not shift meaningfully between filings absent extraordinary events.

4. **False freshness avoidance**: Assigning daily or monthly cadence to filing-dependent blocks would create a false sense of freshness. The underlying evidence would remain unchanged between quarters, but the temporal_status would incorrectly report "current."

**Filing-based blocks (18 total)**:
- SAI-BLK-01 through SAI-BLK-06 (Foundation + Operational core)
- SAI-BLK-07 through SAI-BLK-10 (Financial Stability)
- SAI-BLK-11 (Working Capital — primary assignment)
- SAI-BLK-12 through SAI-BLK-14 (Risk + Operational remaining)
- SAI-BLK-15 through SAI-BLK-16 (Earnings)
- SAI-BLK-22 through SAI-BLK-23 (Outlook)

(See: requirements.md, SAI-REQ-6, Acceptance Criterion 5)

---

## 5. Rationale: Market-Relative Blocks = Daily

**Principle**: Blocks whose primary evidence depends on market prices, trading data, or portfolio weights are assigned the daily temporal class.

**Why daily is the correct minimum frequency**:

1. **Source data cadence**: Market prices, index values, and portfolio weights change every trading day. The source data genuinely refreshes daily, making daily the natural minimum frequency.

2. **Diagnostic relevance**: Relative strength, correlation structure, beta decomposition, and valuation multiples are only meaningful when computed from current market data. A 3-day-old relative strength reading may miss a significant divergence event.

3. **Short-term divergence detection**: The diagnostic purpose of market position blocks is to detect whether an asset moves by its own fundamental strength or merely by index/sector beta. This distinction requires daily granularity — weekly aggregation would mask the signal.

4. **Portfolio weight sensitivity**: Portfolio fit diagnostics depend on current position values. A significant daily price move changes concentration contribution, diversification value, and fragility exposure immediately.

5. **Valuation context accuracy**: Valuation multiples (P/E, EV/EBITDA) use market price as the numerator. Stale prices produce stale multiples that may mislead about current market pricing context.

**Market-relative blocks (6 total)**:
- SAI-BLK-17 (Valuation Context)
- SAI-BLK-18 (Value Trap Guard)
- SAI-BLK-19 (Relative Strength)
- SAI-BLK-20 (Benchmark/Sector/Peer Correlation)
- SAI-BLK-21 (Peer Comparison)
- SAI-BLK-24 (Portfolio Fit)

(See: requirements.md, SAI-REQ-6, Acceptance Criterion 6)

---

## 6. Rationale: Real-Time is Exceptional

**Principle**: No SAI block is assigned real-time as its primary temporal class. Real-time is reserved for future consideration and carries significant constraints.

**Why real-time is exceptional and not default**:

1. **False precision**: Real-time evidence refresh (sub-hourly) creates a false sense of precision for diagnostic interpretation. SAI blocks produce qualitative interpretive outputs, not trading signals. A diagnostic interpretation that changes every minute provides no additional insight over one that changes daily.

2. **Infrastructure burden**: Real-time data streaming imposes disproportionate infrastructure cost (streaming connections, tick-by-tick processing, sub-second staleness detection) relative to the diagnostic value gained. SAI is not a trading system.

3. **Interpretation stability**: Diagnostic interpretations should be stable enough for human consumption. Real-time oscillation in block outputs (e.g., "valuation context changes every 30 seconds") undermines the purpose of structured diagnostic interpretation.

4. **Noise amplification**: Real-time market data contains significant noise (bid-ask bounce, microstructure effects, algorithmic trading artifacts). Daily closing prices filter this noise; real-time data amplifies it into the diagnostic layer.

5. **Scope boundary**: SAI is diagnostic and interpretive — not a real-time monitoring or alerting system. Real-time requirements belong to execution systems, not to evidence interpretation layers.

**Real-time status assignments**:
- **prohibited**: Filing-based blocks where real-time makes no conceptual sense (source data is quarterly)
- **allowed**: Market-relative blocks that could technically operate in real-time but do not require it for diagnostic validity
- **future**: Reserved for streaming signal capabilities that may be added without redesigning existing blocks

**Current real-time block count**: 0 (zero blocks assigned real-time as primary temporal class)

(See: design.md, Section: Temporal Resolution Design — "Creates false precision and infrastructure burden without proportional diagnostic value")

---

## 7. SAI-BLK-11 Working Capital: Monthly Optional Upgrade

SAI-BLK-11 (Working Capital) is assigned quarterly as its primary temporal class, consistent with all other filing-based blocks. However, this block is uniquely positioned for a monthly optional upgrade:

**Why monthly is optional but recognized**:

1. **Intra-quarter sensitivity**: Working capital metrics (DSO, DPO, inventory days) can shift meaningfully within a quarter due to seasonal patterns, payment cycle changes, or inventory buildups. Monthly observation catches these shifts earlier.

2. **Supplementary data availability**: Some companies provide monthly operational updates, and working capital proxies (e.g., factoring facility usage, supplier payment timing) may be observable monthly from supplementary sources.

3. **Early warning value**: A deterioration in working capital efficiency between quarters (rising DSO, inventory buildup) can signal liquidity pressure before it appears in quarterly filings.

**Monthly upgrade conditions**:
- Monthly data must be available from a legitimate source (not interpolated or estimated)
- The monthly temporal class applies only when monthly evidence is genuinely observable
- If monthly data is unavailable, the block operates at quarterly cadence with no diagnostic penalty
- Monthly thresholds: stale > 35 days, expired > 45 days

**The quarterly assignment remains the canonical minimum**. Monthly is an enhancement, not a requirement.

---

## 8. Coverage Summary

### Blocks per Temporal Class

| Temporal Class | Block Count | Block IDs |
|----------------|-------------|-----------|
| quarterly | 18 | SAI-BLK-01, SAI-BLK-02, SAI-BLK-03, SAI-BLK-04, SAI-BLK-05, SAI-BLK-06, SAI-BLK-07, SAI-BLK-08, SAI-BLK-09, SAI-BLK-10, SAI-BLK-11, SAI-BLK-12, SAI-BLK-13, SAI-BLK-14, SAI-BLK-15, SAI-BLK-16, SAI-BLK-22, SAI-BLK-23 |
| monthly | 0 (SAI-BLK-11 optional upgrade) | — |
| daily | 6 | SAI-BLK-17, SAI-BLK-18, SAI-BLK-19, SAI-BLK-20, SAI-BLK-21, SAI-BLK-24 |
| real-time | 0 | — |
| **Total** | **24** | — |

### Coverage Completeness Check

- All 24 blocks have explicit temporal class assignments: **YES**
- All 24 blocks have rationale for their assignment: **YES**
- All 24 blocks have stale thresholds defined: **YES**
- All 24 blocks have expired thresholds defined: **YES**
- All 24 blocks have source cadence dependencies documented: **YES**
- All 24 blocks have real-time status assigned: **YES**
- No block lacks temporal resolution: **CONFIRMED**

### Real-Time Status Distribution

| Status | Block Count | Blocks |
|--------|-------------|--------|
| prohibited | 18 | All quarterly blocks (filing-based) |
| allowed | 6 | All daily blocks (market-relative) |
| future | 0 | No block currently assigned |

---

## 9. Verification Gate Evidence — VG-SAI-9

**Gate**: VG-SAI-9 (Temporal Resolution Gate)
**Requirement**: All 24 blocks have temporal assignment with rationale

### Evidence Statement

This artifact provides complete temporal resolution evidence for VG-SAI-9:

1. **All 24 blocks defined**: Sections 3.1 through 3.9 define temporal resolution for SAI-BLK-01 through SAI-BLK-24. No block is missing.

2. **Temporal class assigned per block**: Every block has an explicit temporal_class field with value from {quarterly, monthly, daily, real-time}.

3. **Rationale per block**: Every block has a rationale field explaining WHY that temporal class is assigned, tied to source data cadence.

4. **Stale and expired thresholds per block**: Every block has stale_threshold and expired_threshold fields with values consistent with the temporal class definitions in Section 2.

5. **Source cadence dependency per block**: Every block has a source_cadence_dependency field documenting what drives the data update frequency.

6. **Real-time status per block**: Every block has a real_time_status field with value from {prohibited, allowed, future}.

7. **Rationale sections provided**:
   - Section 4: Filing-based blocks = quarterly (with enumeration)
   - Section 5: Market-relative blocks = daily (with enumeration)
   - Section 6: Real-time is exceptional (with justification)

8. **SAI-BLK-11 monthly upgrade documented**: Section 7 explicitly addresses the monthly optional upgrade pathway.

9. **Coverage complete**: Section 8 confirms all 24 blocks covered, totals verified.

**Gate readiness**: This artifact is READY for explicit VG-SAI-9 gate execution. The gate artifact (`gate_vg_sai_09.md`) will record the formal PASS/FAIL determination with evidence references.

---

## 10. No-Drift Statement

This artifact is a definition-layer document only. It:

- Does NOT create implementation code
- Does NOT define schedulers or cron jobs
- Does NOT implement refresh logic or data pipelines
- Does NOT create runtime validators
- Does NOT define database schemas or API schemas
- Does NOT produce scoring, ranking, recommendation, allocation, or trading logic
- Does NOT create facts, signals, or evidence primitives
- Does NOT mutate any registry or SSOT
- Does NOT create asset-to-narrative mappings
- Does NOT define how temporal thresholds are enforced at runtime

Temporal resolution is declared here. Implementation is a downstream concern outside SAI's definition-layer scope.

---

## 11. Cross-References

- (See: design.md, Section: Temporal Resolution Design)
- (See: design.md, Section: Error Handling — Stale Evidence)
- (See: requirements.md, Section: SAI-REQ-6 — Temporal Resolution Requirements)
- (See: provenance_contract.md, Section: 4. Evidence Freshness Determination)
- (See: block_taxonomy.md, Section: 4. Block Definitions — temporal_resolution field)
- (See: output_object_spec.md, Section: temporal_status field)

---

*End of temporal_resolution_matrix.md*
