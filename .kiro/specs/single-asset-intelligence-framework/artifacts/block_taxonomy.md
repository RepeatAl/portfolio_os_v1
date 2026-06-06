# Single Asset Intelligence Framework — Canonical Block Taxonomy

**Artifact**: block_taxonomy.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 1.1 Create block taxonomy document
**Requirements**: SAI-REQ-1 (Canonical Analysis Block Taxonomy), SAI-REQ-14 (Additive-Only Extension Mechanism)
**Verification Gates**: VG-SAI-1 (Requirements Completeness), VG-SAI-5 (Taxonomy Stability)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the complete, stable set of 24 canonical analysis blocks that organize all asset-level evidence interpretation within the Single Asset Intelligence Framework. Each block is a discrete diagnostic dimension — it organizes evidence, produces interpretive output, and never scores, ranks, or recommends.

This is a definition-layer artifact. It contains no implementation code, no scoring logic, no allocation decisions, and no executable architecture.

(See: design.md, Section: Components and Interfaces — Analysis Block Architecture)
(See: requirements.md, Section: SAI-REQ-1 — Canonical Analysis Block Taxonomy)

---

## 2. Block Architecture Principles

1. **Independence**: Each block functions without requiring another block's output. No block-to-block dependencies exist within SAI.
2. **Evidence-backed**: Every block consumes at least one fact family and at least one signal family from the Market Evidence Framework.
3. **Non-scoring**: Blocks organize and interpret evidence. They do not produce numeric scores, rankings, or recommendations.
4. **Composable**: Higher layers (scoring, allocation, reporting) may consume any combination of blocks. SAI does not control downstream consumption.
5. **Extensible**: New blocks can be added without modifying existing blocks (additive-only architecture).
6. **Provenance-linked**: Every interpretation traces to specific facts/signals with full provenance chain.

(See: design.md, Section: Block Independence Design)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 6. Core Analysis Blocks — Block Architecture Principles)

---

## 3. Block Summary Table

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

---

## 4. Foundation Blocks

### SAI-BLK-01: Asset Identity

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-01 |
| **block_name** | Asset Identity |
| **category** | Foundation |
| **purpose** | Establish canonical identity and classification of the asset |
| **fact_families** | Company filings, sector classification, listing data, corporate structure |
| **signal_families** | Classification signals, sector rotation signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | All identity claims must reference corporate filings or official regulatory data sources with filing date and document reference |
| **red_flag_requirement** | Minimum 2 red flags: (1) Corporate structure opacity — material subsidiaries undisclosed or jurisdictional complexity obscuring economic reality (elevated); (2) Sector classification conflict — company self-classification contradicts revenue composition evidence (informational) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of asset identity evidence only. |

---

### SAI-BLK-02: Business Model Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-02 |
| **block_name** | Business Model Quality |
| **category** | Foundation |
| **purpose** | Diagnose the structural quality and sustainability of the business model |
| **fact_families** | Revenue composition, segment breakdown, competitive position, moat indicators |
| **signal_families** | Business model durability signals, competitive advantage signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Business model claims must reference revenue segment data, customer type disclosures, and competitive position evidence from filings or management commentary with source attribution |
| **red_flag_requirement** | Minimum 2 red flags: (1) Revenue model fragility — >60% of revenue from non-recurring/transactional sources with no contractual visibility (elevated); (2) Competitive moat erosion — declining market share or pricing power deterioration over 3+ consecutive quarters with evidence (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of business model evidence only. |

---

## 5. Operational Blocks

### SAI-BLK-03: Revenue Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-03 |
| **block_name** | Revenue Quality |
| **category** | Operational |
| **purpose** | Diagnose revenue sustainability, concentration, and organic vs inorganic growth |
| **fact_families** | Revenue breakdown, geographic mix, customer concentration, recurring vs one-time, ARR, RPO, backlog |
| **signal_families** | Revenue growth signals, organic growth signals, concentration signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Revenue claims must reference filed revenue data with period, segment breakdown, and organic/inorganic decomposition sourced from corporate filings or management disclosures |
| **red_flag_requirement** | Minimum 2 red flags: (1) Organic growth negative while total growth positive — growth solely from M&A for 3+ quarters (elevated); (2) ARR growth decelerating while total revenue grows — mix shift toward non-recurring revenue masking quality deterioration (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of revenue quality evidence only. |

---

### SAI-BLK-04: Demand/Pipeline

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-04 |
| **block_name** | Demand/Pipeline |
| **category** | Operational |
| **purpose** | Diagnose demand visibility, backlog health, and pipeline trajectory |
| **fact_families** | Backlog, bookings, order intake, pipeline disclosures, guidance commentary, book-to-bill ratio |
| **signal_families** | Demand momentum signals, pipeline signals, booking trend signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Demand claims must reference order intake data, backlog disclosures, or pipeline metrics from corporate filings or management commentary with observation period specified |
| **red_flag_requirement** | Minimum 2 red flags: (1) Book-to-bill sustained below 1.0 for 3+ quarters — demand erosion pattern with evidence of declining order intake relative to revenue recognition (elevated); (2) Backlog declining while revenue maintained — demand pull-forward exhaustion risk indicating future revenue shortfall (critical) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of demand/pipeline evidence only. |

---

### SAI-BLK-05: Margin Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-05 |
| **block_name** | Margin Quality |
| **category** | Operational |
| **purpose** | Diagnose margin structure, compression risk, and operating leverage |
| **fact_families** | Gross margin, operating margin, SGA ratio, R&D ratio, margin trajectory, EBITDA margin |
| **signal_families** | Margin expansion/compression signals, operating leverage signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Margin claims must reference filed financial data with explicit period, margin type identification, and trend calculation methodology citing source line items |
| **red_flag_requirement** | Minimum 2 red flags: (1) Gross margin compression >200bps without revenue offset — structural cost pressure eroding profitability (elevated); (2) Operating leverage negative — costs growing faster than revenue for 3+ quarters indicating loss of operational discipline (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of margin quality evidence only. |

---

### SAI-BLK-06: Cashflow Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-06 |
| **block_name** | Cashflow Quality |
| **category** | Operational |
| **purpose** | Diagnose cash generation quality, FCF conversion, and cash vs accrual divergence |
| **fact_families** | Operating cashflow, FCF, capex, working capital changes, cash conversion, capex intensity |
| **signal_families** | Cash conversion signals, FCF yield signals, capex intensity signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Cashflow claims must reference cash flow statement data from corporate filings with period specification and explicit derivation of FCF from operating CF minus capex |
| **red_flag_requirement** | Minimum 2 red flags: (1) FCF conversion below 50% for 3 consecutive quarters — persistent gap between reported earnings and actual cash generation (elevated); (2) Negative FCF despite positive EBITDA — accrual-based profit not converting to cash, indicating potential earnings quality issue (critical) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of cashflow quality evidence only. |

---

### SAI-BLK-11: Working Capital

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-11 |
| **block_name** | Working Capital |
| **category** | Operational |
| **purpose** | Diagnose working capital efficiency, cash cycle health, and liquidity pressure |
| **fact_families** | Receivables, payables, inventory, cash conversion cycle, days outstanding (DSO, DPO, inventory days) |
| **signal_families** | Working capital efficiency signals, inventory buildup signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Working capital claims must reference balance sheet line items from corporate filings with period specification and explicit calculation methodology for days-outstanding metrics |
| **red_flag_requirement** | Minimum 2 red flags: (1) Inventory build exceeding revenue growth for 2+ quarters — cash consumed by unsold inventory indicating demand weakness or supply chain misjudgment (elevated); (2) DSO increasing by >10 days over trailing 4 quarters — deteriorating collection quality suggesting customer financial stress or aggressive revenue recognition (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of working capital evidence only. |

---

### SAI-BLK-14: Pricing Power

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-14 |
| **block_name** | Pricing Power |
| **category** | Operational |
| **purpose** | Diagnose ability to maintain or increase prices without demand destruction |
| **fact_families** | Pricing history, contract escalation clauses, volume vs price mix, competitor pricing |
| **signal_families** | Pricing power signals, pass-through ability signals, elasticity indicators |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Pricing power claims must reference price/volume decomposition from filings, contract structure disclosures, or management commentary on pricing actions with quantified impact |
| **red_flag_requirement** | Minimum 2 red flags: (1) Volume decline following price increase — demand elasticity evidence indicating inability to maintain pricing without customer loss (elevated); (2) Cost pass-through failure — input cost increases not reflected in selling prices for 2+ quarters indicating competitive constraint on pricing (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of pricing power evidence only. |

---

## 6. Financial Stability Blocks

### SAI-BLK-07: Balance Sheet Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-07 |
| **block_name** | Balance Sheet Quality |
| **category** | Financial Stability |
| **purpose** | Diagnose overall balance sheet health, asset quality, and capital structure |
| **fact_families** | Total assets, equity, debt structure, asset composition, goodwill/intangibles, maturity schedule, current ratio, quick ratio |
| **signal_families** | Leverage signals, asset quality signals, capital structure signals, liquidity stress signals, refinancing risk signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Balance sheet claims must reference filed balance sheet data with reporting period, auditor attestation status, and explicit line items from corporate filings |
| **red_flag_requirement** | Minimum 2 red flags: (1) Material maturity wall within 18 months — >30% of total debt maturing in tight credit market environment with evidence of refinancing constraint (critical); (2) Goodwill exceeding 100% of tangible equity — intangible asset concentration creating impairment vulnerability with acquisition history reference (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of balance sheet evidence only. |

---

### SAI-BLK-08: Credit/Solvency Risk

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-08 |
| **block_name** | Credit/Solvency Risk |
| **category** | Financial Stability |
| **purpose** | Diagnose credit risk, refinancing exposure, and solvency trajectory |
| **fact_families** | Gross debt, net debt, maturity schedule, interest coverage, credit ratings, covenants, LBO history, sponsor overhang, bond/CDS spreads, short-term debt, available liquidity, FCF/debt ratio |
| **signal_families** | Credit deterioration signals, refinancing risk signals, covenant pressure signals, interest coverage deterioration signals, liquidity stress signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Credit/solvency claims must reference debt structure data from filings, credit rating agency publications (treated as input not truth), bond market data with observation date, and covenant disclosure from loan agreements |
| **red_flag_requirement** | Minimum 2 red flags: (1) Net debt/EBITDA exceeds 4x with declining EBITDA — leverage unsustainable at current earnings trajectory with evidence of deterioration over trailing periods (critical); (2) Interest coverage below 2x and declining — ability to service debt materially impaired with trend evidence over 3+ quarters (critical) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of credit/solvency evidence only. Credit ratings are consumed as inputs, NOT endorsed as truth. |

---

### SAI-BLK-09: Hidden Liabilities

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-09 |
| **block_name** | Hidden Liabilities |
| **category** | Financial Stability |
| **purpose** | Diagnose off-balance-sheet obligations, contingent liabilities, and undisclosed risks |
| **fact_families** | Operating leases, purchase obligations, guarantees, litigation, off-balance items, goodwill/intangibles |
| **signal_families** | Hidden obligation signals, contingent liability signals, off-balance-sheet leverage signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Hidden liability claims must reference footnote disclosures from corporate filings, contingent liability notes, operating lease schedules, and off-balance-sheet arrangement disclosures with specific filing reference |
| **red_flag_requirement** | Minimum 2 red flags: (1) Off-balance-sheet obligations exceeding 30% of reported debt — material hidden leverage distorting headline debt metrics with evidence from filing footnotes (critical); (2) Aggregate contingent liabilities (litigation + guarantees) exceeding 15% of equity — undisclosed risk concentration threatening capital adequacy with quantified exposure (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of hidden liability evidence only. |

---

### SAI-BLK-10: Pension Obligations

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-10 |
| **block_name** | Pension Obligations |
| **category** | Financial Stability |
| **purpose** | Diagnose pension funding status, obligation trajectory, and actuarial risk |
| **fact_families** | Defined benefit obligations, plan assets, funding gap, actuarial assumptions, obligation growth trajectory |
| **signal_families** | Pension underfunding signals, obligation growth signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Pension claims must reference pension footnote disclosures from corporate filings including DBO amount, plan asset fair value, discount rate assumption, and expected return on assets with reporting period |
| **red_flag_requirement** | Minimum 2 red flags: (1) Pension underfunding exceeding 20% of market capitalization — pension liability scale poses material risk to equity value with evidence of funding gap relative to company size (critical); (2) Discount rate assumption >100bps above peer median — aggressive actuarial assumption understating true obligation with peer comparison evidence (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of pension obligation evidence only. |

---

## 7. Risk Blocks

### SAI-BLK-12: Customer Concentration

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-12 |
| **block_name** | Customer Concentration |
| **category** | Risk |
| **purpose** | Diagnose revenue dependency on key customers and concentration risk |
| **fact_families** | Top customer revenue share, customer count, contract duration, switching costs, top-5 customer percentage, geographic concentration |
| **signal_families** | Concentration trend signals, customer loss signals, customer concentration risk signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Concentration claims must reference customer disclosure data from corporate filings (segment notes, risk factor disclosures) with reporting period and explicit identification of concentration methodology |
| **red_flag_requirement** | Minimum 2 red flags: (1) Single customer exceeding 30% of revenue — extreme dependency on one relationship creating binary risk with evidence from segment/customer disclosures (critical); (2) Top-5 customers exceeding 70% of revenue with short contract duration — concentration without contractual protection creating revenue fragility (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of customer concentration evidence only. |

---

### SAI-BLK-13: Supply Chain Stability

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-13 |
| **block_name** | Supply Chain Stability |
| **category** | Risk |
| **purpose** | Diagnose supply chain fragility, single-source risk, and disruption exposure |
| **fact_families** | Supplier concentration, geographic sourcing, inventory buffer, lead times, capacity constraints |
| **signal_families** | Supply disruption signals, lead time signals, inventory adequacy signals, supply chain fragility signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Supply chain claims must reference risk factor disclosures, supplier dependency notes from filings, and inventory adequacy data with source attribution and observation period |
| **red_flag_requirement** | Minimum 2 red flags: (1) Single-source dependency for critical input — no disclosed alternative supplier for material component/service creating binary supply risk (critical); (2) Geographic concentration in high-risk jurisdiction — >50% of sourcing from single country with elevated geopolitical or regulatory disruption risk (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of supply chain stability evidence only. |

---

## 8. Earnings Blocks

### SAI-BLK-15: Earnings Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-15 |
| **block_name** | Earnings Quality |
| **category** | Earnings |
| **purpose** | Diagnose earnings sustainability, accrual quality, and manipulation risk |
| **fact_families** | EPS composition, non-recurring items, accrual ratios, audit opinions, GAAP vs adjusted earnings gap |
| **signal_families** | Earnings quality signals, accrual anomaly signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Earnings quality claims must reference income statement data, reconciliation of GAAP to non-GAAP, audit opinion status, and accrual analysis derived from cash flow statement vs income statement comparison with filing period |
| **red_flag_requirement** | Minimum 2 red flags: (1) Persistent GAAP-to-adjusted gap exceeding 30% for 4+ quarters — recurring "one-off" adjustments indicating structural earnings quality concern (critical); (2) Accrual ratio rising while cash conversion declining — widening gap between reported profit and cash generation suggesting potential earnings manipulation (elevated) |
| **deferred_dependencies** | Earnings Intelligence Framework (future — provides accrual ratio thresholds, non-recurring item classification, earnings manipulation detection heuristics) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of earnings quality evidence only. |

---

### SAI-BLK-16: Guidance/Estimate Revisions

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-16 |
| **block_name** | Guidance/Estimate Revisions |
| **category** | Earnings |
| **purpose** | Diagnose management guidance credibility and analyst estimate trajectory |
| **fact_families** | Management guidance history, analyst estimates, revision history, beat/miss pattern, estimate revision magnitude (3-month, 6-month) |
| **signal_families** | Guidance credibility signals, estimate revision momentum signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Guidance claims must reference specific guidance ranges from earnings calls/filings, consensus estimate data with source and date, and historical accuracy record with minimum 8-quarter history |
| **red_flag_requirement** | Minimum 2 red flags: (1) Guidance consistently missed or revised down for 3+ consecutive quarters — management credibility erosion with evidence of systematic over-promise (elevated); (2) Negative estimate revision trend accelerating — consensus downgrades accelerating in magnitude over trailing 3-month and 6-month windows (elevated) |
| **deferred_dependencies** | Earnings Intelligence Framework (future — provides earnings quality calculation rules and guidance credibility methodology) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, or any form of numeric assessment. It produces diagnostic interpretation of guidance and estimate revision evidence only. |

---

## 9. Valuation Blocks

### SAI-BLK-17: Valuation Context

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-17 |
| **block_name** | Valuation Context |
| **category** | Valuation |
| **purpose** | Provide diagnostic context on current market pricing relative to fundamentals |
| **fact_families** | P/E, EV/EBITDA, P/FCF, P/B, dividend yield, historical multiples, PEG ratio, FCF yield |
| **signal_families** | Valuation compression/expansion signals, multiple trajectory signals, valuation stretch signals |
| **temporal_resolution** | daily |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Valuation context claims must reference market price data with observation date, fundamental data from filings with period, and historical multiple ranges with lookback window. Valuation interpretation requires cross-reference evidence from cashflow quality, credit/solvency, hidden liabilities, earnings quality, company outlook, and peer context — all via shared underlying facts/signals (not block outputs) |
| **red_flag_requirement** | Minimum 2 red flags: (1) Valuation multiple >2 standard deviations above historical median without fundamental improvement — pricing disconnected from evidence-based value creation trajectory (elevated); (2) FCF yield below risk-free rate — market pricing implies growth expectations requiring extraordinary execution with no margin of safety (elevated) |
| **deferred_dependencies** | Valuation Framework (future — provides canonical valuation methodology definitions, sector-appropriate valuation approaches, and negative-earnings handling rules) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, fair value estimates, price targets, "undervalued"/"overvalued" labels, or any form of numeric assessment. It provides valuation context for diagnostic interpretation only. "Low valuation is not automatically undervaluation. A stock is not cheap because it fell. A stock is cheap only if market expectation is below realistic value creation." |

---

### SAI-BLK-18: Value Trap Guard

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-18 |
| **block_name** | Value Trap Guard |
| **category** | Valuation |
| **purpose** | Detect conditions where apparent cheapness masks structural impairment |
| **fact_families** | Same as Valuation Context plus cashflow quality facts, credit risk facts, fundamental trajectory facts, dividend sustainability facts |
| **signal_families** | Value trap indicator signals, fundamental deterioration signals, valuation trap risk signals |
| **temporal_resolution** | daily |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Value trap claims must reference multiple evidence dimensions simultaneously: valuation multiples, cashflow generation, credit/solvency status, and fundamental trajectory — all with source attribution. No value trap diagnosis is valid from a single evidence dimension |
| **red_flag_requirement** | Minimum 2 red flags: (1) Low multiple coincides with declining FCF and rising leverage — statistical cheapness reflecting structural impairment rather than opportunity, with evidence from valuation, cashflow, and debt metrics (critical); (2) High dividend yield from price decline with deteriorating payout coverage — dividend yield trap where yield is unsustainable, with evidence of dividend exceeding FCF generation (critical) |
| **deferred_dependencies** | Valuation Framework (future — provides canonical methodology for distinguishing structural discount from cyclical discount) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, fair value estimates, "undervalued"/"overvalued" labels, probability assessments of being a value trap, or any form of numeric assessment. It produces diagnostic narrative explaining which trap conditions are present or absent, with evidence citations only. |

---

## 10. Market Position Blocks

### SAI-BLK-19: Relative Strength

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-19 |
| **block_name** | Relative Strength |
| **category** | Market Position |
| **purpose** | Diagnose price strength relative to benchmark, sector, and peers |
| **fact_families** | Price performance vs benchmark, sector performance, drawdown history, momentum trajectory |
| **signal_families** | Relative strength signals, momentum signals, drawdown signals |
| **temporal_resolution** | daily |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Relative strength claims must reference market price data with observation date, benchmark/sector index identification, lookback period specification, and calculation methodology (total return vs price return) |
| **red_flag_requirement** | Minimum 2 red flags: (1) Persistent underperformance despite sector tailwind — asset underperforming its sector index for 6+ months while sector outperforms benchmark, indicating asset-specific weakness (elevated); (2) Maximum drawdown exceeding 2x sector drawdown — amplified downside participation suggesting structural fragility or idiosyncratic risk concentration (elevated) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, momentum scores, or any form of numeric assessment. It produces diagnostic interpretation of relative strength evidence only. |

---

### SAI-BLK-20: Benchmark/Sector/Peer Correlation

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-20 |
| **block_name** | Benchmark/Sector/Peer Correlation |
| **category** | Market Position |
| **purpose** | Diagnose correlation structure and beta decomposition |
| **fact_families** | Correlation coefficients, rolling beta, R-squared, factor exposures, volatility |
| **signal_families** | Correlation regime signals, beta decomposition signals, benchmark beta signals, correlation dependency signals |
| **temporal_resolution** | daily |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Correlation claims must reference calculation parameters (rolling window length, data frequency), benchmark/index identification, and observation period with explicit methodology for beta decomposition |
| **red_flag_requirement** | Minimum 2 red flags: (1) Correlation regime shift — rolling correlation to benchmark changes by >0.3 over 60-day window without fundamental justification, indicating structural relationship change (informational); (2) Asymmetric beta — upside beta significantly below downside beta (participation ratio <0.7), indicating asset captures downside but misses upside movements (elevated) |
| **deferred_dependencies** | Correlation/Dependency Framework (future — provides rolling window parameters, regime detection rules, beta decomposition methodology) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, alpha estimates, or any form of numeric assessment. It produces diagnostic interpretation of correlation structure evidence only. |

---

### SAI-BLK-21: Peer Comparison

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-21 |
| **block_name** | Peer Comparison |
| **category** | Market Position |
| **purpose** | Diagnose competitive positioning relative to peer group |
| **fact_families** | Peer financial metrics, market share, growth differentials, margin differentials, valuation differentials |
| **signal_families** | Peer-relative comparison signals, competitive position signals, peer divergence signals |
| **temporal_resolution** | daily |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Peer comparison claims must reference canonical peer group definition (or note non-canonical status), time-aligned financial data from filings, and consistent metric methodology applied across all compared peers |
| **red_flag_requirement** | Minimum 2 red flags: (1) Fundamental divergence from peer group — asset's margins, growth, or returns diverging negatively from peer median by >2 standard deviations for 2+ quarters indicating competitive deterioration (elevated); (2) Valuation premium without fundamental justification — asset priced >50% above peer median multiples without corresponding superior growth/margins/returns evidence (informational) |
| **deferred_dependencies** | Peer Group Registry (future — provides canonical peer group definitions, peer selection methodology, peer rotation rules) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, competitive rankings, or any form of numeric assessment. It produces diagnostic interpretation of peer comparison evidence only. Peer groups are non-canonical until the Peer Group Registry exists. |

---

## 11. Outlook Blocks

### SAI-BLK-22: Company Outlook

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-22 |
| **block_name** | Company Outlook |
| **category** | Outlook |
| **purpose** | Synthesize forward-looking company-specific diagnostic from all available evidence |
| **fact_families** | Management commentary, capital allocation plans, strategic initiatives, M&A activity, guidance revisions |
| **signal_families** | Forward momentum signals, strategic execution signals, outlook revision signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Outlook claims must reference specific management commentary from earnings calls or filings, capital allocation disclosures, strategic initiative announcements, and M&A activity with dates and source documents |
| **red_flag_requirement** | Minimum 2 red flags: (1) Management guidance credibility collapse — 3+ consecutive quarters of missed guidance or material downward revisions indicating systematic forward-looking unreliability (elevated); (2) Strategic pivot without evidence of execution capability — announced strategic change into new market/technology without demonstrated competence or resource allocation evidence (informational) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, probability assessments, conviction levels, or any form of numeric assessment. It produces diagnostic interpretation of company outlook evidence only. |

---

### SAI-BLK-23: Asset-Class Outlook

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-23 |
| **block_name** | Asset-Class Outlook |
| **category** | Outlook |
| **purpose** | Diagnose asset-class level conditions affecting this asset |
| **fact_families** | Sector fundamentals, regulatory environment, macro sensitivity, industry cycle position |
| **signal_families** | Sector rotation signals, regulatory risk signals, cycle position signals |
| **temporal_resolution** | quarterly |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Asset-class outlook claims must reference sector-level data from industry sources, regulatory developments with specific citation, and macro factor sensitivity evidence with observation period and methodology |
| **red_flag_requirement** | Minimum 2 red flags: (1) Adverse regulatory development — material regulatory change announced or proposed that directly impacts the asset's sector with evidence of revenue/margin exposure quantification (elevated); (2) Industry cycle late-stage indicators — multiple sector-level signals indicating peak cycle conditions (capex overinvestment, margin peak, capacity additions) without asset-specific resilience evidence (informational) |
| **deferred_dependencies** | None |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, sector allocation recommendations, or any form of numeric assessment. It produces diagnostic interpretation of asset-class level conditions only. |

---

## 12. Portfolio Context Block

### SAI-BLK-24: Portfolio Fit

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-24 |
| **block_name** | Portfolio Fit |
| **category** | Portfolio Context |
| **purpose** | Diagnose how this asset relates to portfolio-level constructs (concentration, overlap, sensitivity) |
| **fact_families** | Position weight, sector allocation, geographic allocation, factor exposure, ADV/liquidity metrics |
| **signal_families** | Concentration contribution signals, diversification signals, liquidity signals, portfolio fit signals |
| **temporal_resolution** | daily |
| **output_type** | Diagnostic interpretation |
| **provenance_requirement** | Portfolio fit claims must reference current portfolio composition data with observation date, concentration metrics with calculation methodology, and correlation/overlap evidence with time window specification |
| **red_flag_requirement** | Minimum 2 red flags: (1) Concentration contribution breach — single asset contributing >15% to portfolio sector concentration or >10% to single-factor exposure without explicit risk acknowledgment (elevated); (2) Liquidity mismatch — position size exceeding 5 days of average daily volume (ADV), creating material exit friction with evidence of ADV and position size (elevated) |
| **deferred_dependencies** | Portfolio Health Framework (future — provides portfolio-level construct definitions, concentration measurement methodology, overlap detection rules) |
| **non_scoring_boundary** | This block does NOT produce scores, rankings, ratings, recommendations, buy/sell/hold signals, target weights, position sizes, allocation instructions, rebalance triggers, "overweight"/"underweight"/"neutral" labels, or any form of numeric assessment. It produces diagnostic interpretation of portfolio fit evidence only. |

---

## 13. Additive-Only Extension Mechanism

(See: requirements.md, Section: SAI-REQ-14 — Additive-Only Extension Mechanism)
(See: design.md, Section: Extension Mechanism)

### 13.1 Extension Rules

The block taxonomy is extendable under strict additive-only constraints:

| Rule | Description |
|------|-------------|
| New block identifiers | New blocks receive SAI-BLK-25, SAI-BLK-26, etc. — identifiers are never reused |
| Identifier immutability | Once a block_id is assigned to a block_name, that assignment is permanent and irrevocable |
| No block removal | No existing block (SAI-BLK-01 through SAI-BLK-24) may be removed or deprecated |
| No block renaming | No existing block_name may be changed once canonicalized |
| No category reassignment | No existing block may change its assigned category |
| No fact family removal | Existing fact family mappings may not be removed (new families may be added) |
| No signal family removal | Existing signal family mappings may not be removed (new families may be added) |
| No temporal downgrade | No block may reduce its temporal resolution (e.g., daily → quarterly is forbidden) |
| Backward compatibility | Adding block SAI-BLK-25+ cannot break existing blocks SAI-BLK-01 through SAI-BLK-24 |

### 13.2 What MAY Be Added

- New blocks (SAI-BLK-25+) with full field specification
- New fact families to existing blocks (additive only)
- New signal families to existing blocks (additive only)
- New red flags to existing blocks (minimum 2 per block is a floor, not a ceiling)
- New categories if a new block does not fit existing categories
- New temporal resolution classes (e.g., weekly) with documented rationale

### 13.3 Block Identifier Immutability Guarantee

Once assigned, a block identifier is permanently bound to its block definition:

- SAI-BLK-01 is permanently "Asset Identity"
- SAI-BLK-02 is permanently "Business Model Quality"
- ... (all 24 identifiers are frozen)
- SAI-BLK-24 is permanently "Portfolio Fit"

If a block concept becomes obsolete, the identifier remains reserved. It is NEVER reassigned to a different concept. The block may be annotated as "historically defined, no longer actively consumed" but its identifier persists in the registry.

### 13.4 Backward Compatibility Guarantee

Any extension to the taxonomy MUST satisfy:

1. Existing consumers of blocks SAI-BLK-01 through SAI-BLK-24 are unaffected
2. Existing provenance chains remain valid
3. Existing red flag definitions remain unchanged
4. Existing fact/signal consumption contracts remain unchanged
5. Existing temporal resolution assignments remain unchanged
6. No existing output object fields are removed or renamed

### 13.5 Extension Proposal Template

Any proposal to add a new block (SAI-BLK-25+) must provide:

| Required Field | Description |
|----------------|-------------|
| **proposed_block_id** | Next available SAI-BLK-NN identifier |
| **block_name** | Human-readable block name |
| **category** | Existing category or proposed new category |
| **purpose** | One-sentence diagnostic purpose |
| **fact_families** | Which fact domains this block will consume (minimum 1) |
| **signal_families** | Which signal types this block will consume (minimum 1) |
| **temporal_resolution** | Required refresh frequency with rationale |
| **output_type** | Must be "Diagnostic interpretation" |
| **provenance_requirement** | What source evidence must be cited |
| **red_flag_requirement** | Minimum 2 red flags with evidence thresholds |
| **deferred_dependencies** | External frameworks needed (if any) with interface contract |
| **non_scoring_boundary** | Explicit statement that block does NOT produce scores/recommendations |
| **rationale** | Why this block is needed and what diagnostic gap it fills |
| **independence_proof** | Demonstration that new block does not require other blocks' outputs |
| **backward_compat_proof** | Demonstration that existing blocks are unaffected |

### 13.6 Extension Governance

- Extensions require ARCH authority approval
- Extensions must pass VG-SAI-5 (Taxonomy Stability Gate) verification
- Extensions must satisfy the same requirements as existing blocks (SAI-REQ-1 through SAI-REQ-15 where applicable)
- Extensions are documented in this artifact as amendments (never modifying existing block definitions)

---

## 14. Deferred Dependency Summary

The following external frameworks are required by specific blocks but do not yet exist. SAI declares interface contracts for these dependencies without defining the frameworks themselves.

| Deferred Framework | Affected Blocks | What SAI Expects |
|-------------------|-----------------|-----------------|
| Earnings Intelligence Framework | SAI-BLK-15, SAI-BLK-16 | Accrual ratio thresholds, non-recurring item classification, earnings manipulation detection heuristics, guidance credibility methodology |
| Valuation Framework | SAI-BLK-17, SAI-BLK-18 | Canonical valuation methodology definitions, sector-appropriate valuation approaches, negative-earnings handling, structural vs cyclical discount methodology |
| Peer Group Registry | SAI-BLK-21 | Canonical peer group definitions per asset, peer selection methodology, peer rotation rules |
| Correlation/Dependency Framework | SAI-BLK-20 | Rolling window parameters, regime detection rules, beta decomposition methodology |
| Portfolio Health Framework | SAI-BLK-24 | Portfolio-level construct definitions, concentration measurement methodology, overlap detection rules |

Until these frameworks exist, affected blocks operate with available evidence only and document the limitation in `deferred_dependency_notes`.

(See: design.md, Section: Deferred Interface Design)

---

## 15. Verification Readiness

This artifact provides evidence for the following verification gates:

### VG-SAI-1 (Requirements Completeness Gate)

- All 24 blocks defined: YES (SAI-BLK-01 through SAI-BLK-24)
- Stable identifiers: YES (SAI-BLK-NN format, immutable)
- Categories assigned: YES (9 categories)
- Purpose statements: YES (one per block)
- Fact families mapped: YES (≥1 per block)
- Signal families mapped: YES (≥1 per block)

NOTE: This artifact provides evidence toward VG-SAI-1 but does NOT constitute gate execution. VG-SAI-1 requires a separate gate execution artifact with explicit PASS/FAIL determination.

### VG-SAI-5 (Taxonomy Stability Gate)

- Block IDs frozen: YES (SAI-BLK-01 through SAI-BLK-24 permanently assigned)
- Extension mechanism documented: YES (Section 13)
- No block removal permitted: YES (Section 13.1)
- Identifier immutability stated: YES (Section 13.3)
- Backward compatibility guaranteed: YES (Section 13.4)

NOTE: This artifact provides evidence toward VG-SAI-5 but does NOT constitute gate execution. VG-SAI-5 requires a separate gate execution artifact with explicit PASS/FAIL determination.

---

## 16. Cross-References

(See: design.md, Section: Components and Interfaces — Analysis Block Architecture)
(See: design.md, Section: Block Independence Design)
(See: design.md, Section: Extension Mechanism)
(See: design.md, Section: Valuation / Value Trap Design)
(See: design.md, Section: Credit / Solvency Design)
(See: design.md, Section: Peer / Benchmark Design)
(See: design.md, Section: Portfolio Fit Design)
(See: requirements.md, Section: SAI-REQ-1 — Canonical Analysis Block Taxonomy)
(See: requirements.md, Section: SAI-REQ-14 — Additive-Only Extension Mechanism)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 6. Core Analysis Blocks)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 8. Required Fact Categories)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 9. Required Signal Categories)
(See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)
(See: README_market_organism_principles, Section: Principle 3 — Additive Architecture)

---

*Artifact generated: 2026-06-06*
*Authority: ARCH*
*Layer: Definition — No implementation code*
*Task: 1.1 Create block taxonomy document*
*Requirements: SAI-REQ-1, SAI-REQ-14*
*Verification Gates: VG-SAI-1, VG-SAI-5 (evidence provided, gate execution pending)*
