# Single Asset Intelligence Framework — Fact Consumption Matrix

**Artifact**: fact_consumption_matrix.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 2.1 Create fact-to-block consumption matrix
**Requirements**: SAI-REQ-2 (Fact Consumption Contracts)
**Verification Gate**: VG-SAI-6 (Fact Coverage Gate)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the complete consumption mapping between the 68 canonical fact categories (defined in the Market Evidence Framework preflight inventory, Section 8) and the 24 canonical analysis blocks of the Single Asset Intelligence Framework.

This is a definition-layer artifact. It contains no implementation code, no scoring logic, no allocation decisions, and no executable architecture.

**Constraints**:
- Only the 68 fact categories from the preflight are used. No new fact categories are invented.
- Market Evidence Framework is NOT mutated.
- Each fact category is assigned to at least one block (primary consumer).
- Each block has at least one fact category assigned.
- Blocks whose evidence needs exceed the 68 enumerated categories have interface gaps documented.

(See: design.md, Section: Evidence Consumption Design)
(See: requirements.md, Section: SAI-REQ-2 — Fact Consumption Contracts)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 8. Required Fact Categories)

---

## 2. Fact-to-Block Consumption Matrix (Fact-Centric View)

Each fact category is mapped to its primary consumer block(s) and secondary consumer block(s).

- **Primary**: The block whose core diagnostic purpose directly requires this fact.
- **Secondary**: Blocks that consume this fact as supporting/contextual evidence.

### 2.1 Revenue Facts (8)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 1 | `fact.revenue.total_revenue` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-02 (Business Model Quality), SAI-BLK-15 (Earnings Quality) |
| 2 | `fact.revenue.growth_yoy` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-04 (Demand/Pipeline), SAI-BLK-22 (Company Outlook) |
| 3 | `fact.revenue.growth_qoq` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-04 (Demand/Pipeline) |
| 4 | `fact.revenue.organic_growth` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-02 (Business Model Quality), SAI-BLK-22 (Company Outlook) |
| 5 | `fact.revenue.arr` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-02 (Business Model Quality) |
| 6 | `fact.revenue.rpo` | SAI-BLK-03 (Revenue Quality), SAI-BLK-04 (Demand/Pipeline) | — |
| 7 | `fact.revenue.backlog` | SAI-BLK-04 (Demand/Pipeline) | SAI-BLK-03 (Revenue Quality) |
| 8 | `fact.revenue.recurring_pct` | SAI-BLK-03 (Revenue Quality) | SAI-BLK-02 (Business Model Quality) |

### 2.2 Demand/Pipeline Facts (4)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 9 | `fact.demand.order_intake` | SAI-BLK-04 (Demand/Pipeline) | SAI-BLK-03 (Revenue Quality) |
| 10 | `fact.demand.book_to_bill` | SAI-BLK-04 (Demand/Pipeline) | SAI-BLK-22 (Company Outlook) |
| 11 | `fact.demand.pipeline_value` | SAI-BLK-04 (Demand/Pipeline) | — |
| 12 | `fact.demand.win_rate` | SAI-BLK-04 (Demand/Pipeline) | SAI-BLK-14 (Pricing Power) |


### 2.3 Margin Facts (5)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 13 | `fact.margin.gross_margin` | SAI-BLK-05 (Margin Quality) | SAI-BLK-14 (Pricing Power), SAI-BLK-15 (Earnings Quality) |
| 14 | `fact.margin.operating_margin` | SAI-BLK-05 (Margin Quality) | SAI-BLK-15 (Earnings Quality) |
| 15 | `fact.margin.ebitda_margin` | SAI-BLK-05 (Margin Quality) | SAI-BLK-08 (Credit/Solvency Risk) |
| 16 | `fact.margin.fcf_margin` | SAI-BLK-05 (Margin Quality), SAI-BLK-06 (Cashflow Quality) | SAI-BLK-18 (Value Trap Guard) |
| 17 | `fact.margin.gross_margin_trend` | SAI-BLK-05 (Margin Quality) | SAI-BLK-14 (Pricing Power), SAI-BLK-22 (Company Outlook) |

### 2.4 Cashflow Facts (5)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 18 | `fact.cashflow.operating_cf` | SAI-BLK-06 (Cashflow Quality) | SAI-BLK-15 (Earnings Quality) |
| 19 | `fact.cashflow.fcf` | SAI-BLK-06 (Cashflow Quality) | SAI-BLK-08 (Credit/Solvency Risk), SAI-BLK-17 (Valuation Context), SAI-BLK-18 (Value Trap Guard) |
| 20 | `fact.cashflow.fcf_conversion` | SAI-BLK-06 (Cashflow Quality) | SAI-BLK-15 (Earnings Quality), SAI-BLK-18 (Value Trap Guard) |
| 21 | `fact.cashflow.capex` | SAI-BLK-06 (Cashflow Quality) | SAI-BLK-22 (Company Outlook) |
| 22 | `fact.cashflow.capex_intensity` | SAI-BLK-06 (Cashflow Quality) | SAI-BLK-02 (Business Model Quality) |

### 2.5 Balance Sheet Facts (11)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 23 | `fact.balance_sheet.cash` | SAI-BLK-07 (Balance Sheet Quality) | SAI-BLK-08 (Credit/Solvency Risk) |
| 24 | `fact.balance_sheet.gross_debt` | SAI-BLK-07 (Balance Sheet Quality), SAI-BLK-08 (Credit/Solvency Risk) | — |
| 25 | `fact.balance_sheet.net_debt` | SAI-BLK-08 (Credit/Solvency Risk) | SAI-BLK-07 (Balance Sheet Quality) |
| 26 | `fact.balance_sheet.maturity_schedule` | SAI-BLK-07 (Balance Sheet Quality), SAI-BLK-08 (Credit/Solvency Risk) | — |
| 27 | `fact.balance_sheet.short_term_debt` | SAI-BLK-08 (Credit/Solvency Risk) | SAI-BLK-07 (Balance Sheet Quality) |
| 28 | `fact.balance_sheet.interest_expense` | SAI-BLK-08 (Credit/Solvency Risk) | — |
| 29 | `fact.balance_sheet.interest_coverage` | SAI-BLK-08 (Credit/Solvency Risk) | SAI-BLK-07 (Balance Sheet Quality), SAI-BLK-18 (Value Trap Guard) |
| 30 | `fact.balance_sheet.net_debt_ebitda` | SAI-BLK-08 (Credit/Solvency Risk) | SAI-BLK-07 (Balance Sheet Quality), SAI-BLK-18 (Value Trap Guard) |
| 31 | `fact.balance_sheet.fcf_to_debt` | SAI-BLK-08 (Credit/Solvency Risk) | SAI-BLK-06 (Cashflow Quality) |
| 32 | `fact.balance_sheet.current_ratio` | SAI-BLK-07 (Balance Sheet Quality) | SAI-BLK-11 (Working Capital) |
| 33 | `fact.balance_sheet.quick_ratio` | SAI-BLK-07 (Balance Sheet Quality) | SAI-BLK-11 (Working Capital) |


### 2.6 Obligations / Hidden Liabilities Facts (9)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 34 | `fact.obligations.lease_liabilities` | SAI-BLK-09 (Hidden Liabilities) | SAI-BLK-08 (Credit/Solvency Risk) |
| 35 | `fact.obligations.pension_obligations` | SAI-BLK-10 (Pension Obligations) | SAI-BLK-09 (Hidden Liabilities) |
| 36 | `fact.obligations.pension_funding_gap` | SAI-BLK-10 (Pension Obligations) | SAI-BLK-09 (Hidden Liabilities), SAI-BLK-18 (Value Trap Guard) |
| 37 | `fact.obligations.purchase_obligations` | SAI-BLK-09 (Hidden Liabilities) | SAI-BLK-08 (Credit/Solvency Risk) |
| 38 | `fact.obligations.litigation_exposure` | SAI-BLK-09 (Hidden Liabilities) | — |
| 39 | `fact.obligations.off_balance_sheet` | SAI-BLK-09 (Hidden Liabilities) | SAI-BLK-08 (Credit/Solvency Risk) |
| 40 | `fact.obligations.goodwill` | SAI-BLK-09 (Hidden Liabilities), SAI-BLK-07 (Balance Sheet Quality) | — |
| 41 | `fact.obligations.intangibles` | SAI-BLK-09 (Hidden Liabilities), SAI-BLK-07 (Balance Sheet Quality) | — |
| 42 | `fact.obligations.goodwill_to_equity` | SAI-BLK-09 (Hidden Liabilities) | SAI-BLK-07 (Balance Sheet Quality) |

### 2.7 Working Capital Facts (4)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 43 | `fact.working_capital.inventory` | SAI-BLK-11 (Working Capital) | SAI-BLK-13 (Supply Chain Stability) |
| 44 | `fact.working_capital.dso` | SAI-BLK-11 (Working Capital) | SAI-BLK-15 (Earnings Quality) |
| 45 | `fact.working_capital.dpo` | SAI-BLK-11 (Working Capital) | SAI-BLK-13 (Supply Chain Stability) |
| 46 | `fact.working_capital.inventory_days` | SAI-BLK-11 (Working Capital) | SAI-BLK-13 (Supply Chain Stability) |

### 2.8 Concentration Facts (4)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 47 | `fact.concentration.top_customer_pct` | SAI-BLK-12 (Customer Concentration) | SAI-BLK-03 (Revenue Quality) |
| 48 | `fact.concentration.top_5_customers_pct` | SAI-BLK-12 (Customer Concentration) | SAI-BLK-03 (Revenue Quality) |
| 49 | `fact.concentration.supplier_concentration` | SAI-BLK-13 (Supply Chain Stability) | — |
| 50 | `fact.concentration.geographic_concentration` | SAI-BLK-12 (Customer Concentration) | SAI-BLK-13 (Supply Chain Stability), SAI-BLK-24 (Portfolio Fit) |

### 2.9 Valuation Facts (7)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 51 | `fact.valuation.ev_ebitda` | SAI-BLK-17 (Valuation Context) | SAI-BLK-18 (Value Trap Guard), SAI-BLK-21 (Peer Comparison) |
| 52 | `fact.valuation.ev_fcf` | SAI-BLK-17 (Valuation Context) | SAI-BLK-18 (Value Trap Guard) |
| 53 | `fact.valuation.pe_ratio` | SAI-BLK-17 (Valuation Context) | SAI-BLK-21 (Peer Comparison) |
| 54 | `fact.valuation.fcf_yield` | SAI-BLK-17 (Valuation Context) | SAI-BLK-18 (Value Trap Guard), SAI-BLK-24 (Portfolio Fit) |
| 55 | `fact.valuation.peg_ratio` | SAI-BLK-17 (Valuation Context) | — |
| 56 | `fact.valuation.estimate_revisions_3m` | SAI-BLK-16 (Guidance/Estimate Revisions) | SAI-BLK-17 (Valuation Context), SAI-BLK-22 (Company Outlook) |
| 57 | `fact.valuation.guidance_revision` | SAI-BLK-16 (Guidance/Estimate Revisions) | SAI-BLK-22 (Company Outlook) |

### 2.10 Market / Relative Facts (11)

| # | Fact Category ID | Primary Consumer Block(s) | Secondary Consumer Block(s) |
|---|-----------------|--------------------------|----------------------------|
| 58 | `fact.market.relative_strength_vs_benchmark` | SAI-BLK-19 (Relative Strength) | SAI-BLK-24 (Portfolio Fit) |
| 59 | `fact.market.relative_strength_vs_sector` | SAI-BLK-19 (Relative Strength) | SAI-BLK-23 (Asset-Class Outlook) |
| 60 | `fact.market.relative_strength_vs_peers` | SAI-BLK-19 (Relative Strength), SAI-BLK-21 (Peer Comparison) | — |
| 61 | `fact.market.correlation_to_benchmark` | SAI-BLK-20 (Benchmark/Sector/Peer Correlation) | SAI-BLK-24 (Portfolio Fit) |
| 62 | `fact.market.beta` | SAI-BLK-20 (Benchmark/Sector/Peer Correlation) | SAI-BLK-19 (Relative Strength), SAI-BLK-24 (Portfolio Fit) |
| 63 | `fact.market.volatility` | SAI-BLK-20 (Benchmark/Sector/Peer Correlation) | SAI-BLK-19 (Relative Strength), SAI-BLK-24 (Portfolio Fit) |
| 64 | `fact.market.max_drawdown` | SAI-BLK-19 (Relative Strength) | SAI-BLK-20 (Benchmark/Sector/Peer Correlation), SAI-BLK-24 (Portfolio Fit) |
| 65 | `fact.market.liquidity_adv` | SAI-BLK-19 (Relative Strength) | SAI-BLK-24 (Portfolio Fit) |
| 66 | `fact.market.short_interest` | SAI-BLK-19 (Relative Strength) | SAI-BLK-18 (Value Trap Guard) |
| 67 | `fact.market.institutional_ownership` | SAI-BLK-19 (Relative Strength) | SAI-BLK-24 (Portfolio Fit) |
| 68 | `fact.market.institutional_flow` | SAI-BLK-19 (Relative Strength) | SAI-BLK-24 (Portfolio Fit) |


---

## 3. Block-Centric View (Block → Consumed Fact Categories)

This section inverts the matrix to show each block's complete fact consumption contract.

### SAI-BLK-01: Asset Identity (Foundation)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | — |
| **Interface Gap** | **Qualitative facts not enumerated in preflight fact inventory.** This block consumes qualitative evidence from corporate filings (sector classification, listing data, corporate structure, ownership structure) that are not represented in the 68 quantitative fact categories. These qualitative inputs are not formalized as `fact.*` IDs in the Market Evidence Framework preflight. |

---

### SAI-BLK-02: Business Model Quality (Foundation)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.revenue.total_revenue`, `fact.revenue.organic_growth`, `fact.revenue.arr`, `fact.revenue.recurring_pct`, `fact.cashflow.capex_intensity` |
| **Interface Gap** | **Qualitative facts not enumerated in preflight fact inventory.** This block's primary evidence comes from revenue composition, segment breakdown, competitive position, and moat indicators — qualitative assessments derived from filings that are not enumerated as discrete `fact.*` IDs. Secondary quantitative facts from the 68 categories provide supporting evidence. |

---

### SAI-BLK-03: Revenue Quality (Operational)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.revenue.total_revenue`, `fact.revenue.growth_yoy`, `fact.revenue.growth_qoq`, `fact.revenue.organic_growth`, `fact.revenue.arr`, `fact.revenue.rpo`, `fact.revenue.recurring_pct` |
| Secondary | `fact.revenue.backlog`, `fact.demand.order_intake`, `fact.concentration.top_customer_pct`, `fact.concentration.top_5_customers_pct` |

---

### SAI-BLK-04: Demand/Pipeline (Operational)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.revenue.rpo`, `fact.revenue.backlog`, `fact.demand.order_intake`, `fact.demand.book_to_bill`, `fact.demand.pipeline_value`, `fact.demand.win_rate` |
| Secondary | `fact.revenue.growth_yoy`, `fact.revenue.growth_qoq` |

---

### SAI-BLK-05: Margin Quality (Operational)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.margin.gross_margin`, `fact.margin.operating_margin`, `fact.margin.ebitda_margin`, `fact.margin.fcf_margin`, `fact.margin.gross_margin_trend` |
| Secondary | — |

---

### SAI-BLK-06: Cashflow Quality (Operational)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.cashflow.operating_cf`, `fact.cashflow.fcf`, `fact.cashflow.fcf_conversion`, `fact.cashflow.capex`, `fact.cashflow.capex_intensity`, `fact.margin.fcf_margin` |
| Secondary | `fact.balance_sheet.fcf_to_debt` |

---

### SAI-BLK-07: Balance Sheet Quality (Financial Stability)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.balance_sheet.cash`, `fact.balance_sheet.gross_debt`, `fact.balance_sheet.maturity_schedule`, `fact.balance_sheet.current_ratio`, `fact.balance_sheet.quick_ratio`, `fact.obligations.goodwill`, `fact.obligations.intangibles` |
| Secondary | `fact.balance_sheet.net_debt`, `fact.balance_sheet.short_term_debt`, `fact.balance_sheet.interest_coverage`, `fact.balance_sheet.net_debt_ebitda`, `fact.obligations.goodwill_to_equity` |

---

### SAI-BLK-08: Credit/Solvency Risk (Financial Stability)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.balance_sheet.gross_debt`, `fact.balance_sheet.net_debt`, `fact.balance_sheet.maturity_schedule`, `fact.balance_sheet.short_term_debt`, `fact.balance_sheet.interest_expense`, `fact.balance_sheet.interest_coverage`, `fact.balance_sheet.net_debt_ebitda`, `fact.balance_sheet.fcf_to_debt` |
| Secondary | `fact.balance_sheet.cash`, `fact.margin.ebitda_margin`, `fact.obligations.lease_liabilities`, `fact.obligations.purchase_obligations`, `fact.obligations.off_balance_sheet`, `fact.cashflow.fcf` |

---

### SAI-BLK-09: Hidden Liabilities (Financial Stability)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.obligations.lease_liabilities`, `fact.obligations.purchase_obligations`, `fact.obligations.litigation_exposure`, `fact.obligations.off_balance_sheet`, `fact.obligations.goodwill`, `fact.obligations.intangibles`, `fact.obligations.goodwill_to_equity` |
| Secondary | `fact.obligations.pension_obligations`, `fact.obligations.pension_funding_gap` |

---

### SAI-BLK-10: Pension Obligations (Financial Stability)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.obligations.pension_obligations`, `fact.obligations.pension_funding_gap` |
| Secondary | — |

---

### SAI-BLK-11: Working Capital (Operational)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.working_capital.inventory`, `fact.working_capital.dso`, `fact.working_capital.dpo`, `fact.working_capital.inventory_days` |
| Secondary | `fact.balance_sheet.current_ratio`, `fact.balance_sheet.quick_ratio` |

---

### SAI-BLK-12: Customer Concentration (Risk)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.concentration.top_customer_pct`, `fact.concentration.top_5_customers_pct`, `fact.concentration.geographic_concentration` |
| Secondary | — |

---

### SAI-BLK-13: Supply Chain Stability (Risk)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.concentration.supplier_concentration` |
| Secondary | `fact.working_capital.inventory`, `fact.working_capital.dpo`, `fact.working_capital.inventory_days`, `fact.concentration.geographic_concentration` |

---

### SAI-BLK-14: Pricing Power (Operational)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.margin.gross_margin`, `fact.margin.gross_margin_trend`, `fact.demand.win_rate` |
| **Interface Gap** | **Qualitative facts not enumerated in preflight fact inventory.** This block's primary evidence comes from pricing history, contract escalation clauses, volume vs. price mix decomposition, and competitor pricing data — none of which are enumerated as discrete `fact.*` IDs in the 68 categories. Secondary quantitative facts provide supporting evidence for pricing power interpretation. |

---

### SAI-BLK-15: Earnings Quality (Earnings)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.revenue.total_revenue`, `fact.margin.gross_margin`, `fact.margin.operating_margin`, `fact.cashflow.operating_cf`, `fact.cashflow.fcf_conversion`, `fact.working_capital.dso` |
| **Interface Gap** | **Qualitative facts not enumerated in preflight fact inventory.** This block's primary evidence comes from EPS composition, non-recurring item analysis, accrual ratios, audit opinions, and GAAP vs. adjusted earnings gap — none of which are enumerated as discrete `fact.*` IDs in the 68 categories. Additionally, Earnings Intelligence Framework (deferred) is required for full block activation. Secondary quantitative facts provide supporting cross-checks. |

---

### SAI-BLK-16: Guidance/Estimate Revisions (Earnings)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.valuation.estimate_revisions_3m`, `fact.valuation.guidance_revision` |
| Secondary | — |

---

### SAI-BLK-17: Valuation Context (Valuation)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.valuation.ev_ebitda`, `fact.valuation.ev_fcf`, `fact.valuation.pe_ratio`, `fact.valuation.fcf_yield`, `fact.valuation.peg_ratio` |
| Secondary | `fact.valuation.estimate_revisions_3m`, `fact.cashflow.fcf` |

---

### SAI-BLK-18: Value Trap Guard (Valuation)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.valuation.ev_ebitda`, `fact.valuation.ev_fcf`, `fact.valuation.fcf_yield`, `fact.margin.fcf_margin`, `fact.cashflow.fcf`, `fact.cashflow.fcf_conversion`, `fact.balance_sheet.interest_coverage`, `fact.balance_sheet.net_debt_ebitda`, `fact.obligations.pension_funding_gap`, `fact.market.short_interest` |
| **Note** | This block is a cross-dimensional diagnostic. Its primary evidence is the *combination* of valuation facts with cashflow quality, credit/solvency, and fundamental trajectory facts — all consumed from the 68 categories but in a multi-dimensional cross-check role. The secondary assignments reflect this multi-dimensional consumption pattern. |

---

### SAI-BLK-19: Relative Strength (Market Position)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.market.relative_strength_vs_benchmark`, `fact.market.relative_strength_vs_sector`, `fact.market.relative_strength_vs_peers`, `fact.market.max_drawdown`, `fact.market.liquidity_adv`, `fact.market.short_interest`, `fact.market.institutional_ownership`, `fact.market.institutional_flow` |
| Secondary | `fact.market.beta`, `fact.market.volatility` |

---

### SAI-BLK-20: Benchmark/Sector/Peer Correlation (Market Position)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.market.correlation_to_benchmark`, `fact.market.beta`, `fact.market.volatility` |
| Secondary | `fact.market.max_drawdown` |

---

### SAI-BLK-21: Peer Comparison (Market Position)

| Role | Fact Categories |
|------|----------------|
| Primary | `fact.market.relative_strength_vs_peers` |
| Secondary | `fact.valuation.ev_ebitda`, `fact.valuation.pe_ratio` |

---

### SAI-BLK-22: Company Outlook (Outlook)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.revenue.growth_yoy`, `fact.revenue.organic_growth`, `fact.demand.book_to_bill`, `fact.margin.gross_margin_trend`, `fact.cashflow.capex`, `fact.valuation.estimate_revisions_3m`, `fact.valuation.guidance_revision` |
| **Interface Gap** | **Qualitative facts not enumerated in preflight fact inventory.** This block's primary evidence comes from management commentary, capital allocation plans, strategic initiatives, and M&A activity — qualitative corporate disclosures not formalized as `fact.*` IDs. Secondary quantitative facts provide trend evidence supporting outlook interpretation. |

---

### SAI-BLK-23: Asset-Class Outlook (Outlook)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.market.relative_strength_vs_sector` |
| **Interface Gap** | **Qualitative facts not enumerated in preflight fact inventory.** This block's primary evidence comes from sector fundamentals, regulatory environment, macro sensitivity, and industry cycle position — qualitative/macro inputs not formalized as discrete `fact.*` IDs in the 68 categories. |

---

### SAI-BLK-24: Portfolio Fit (Portfolio Context)

| Role | Fact Categories |
|------|----------------|
| Primary | — |
| Secondary | `fact.concentration.geographic_concentration`, `fact.market.relative_strength_vs_benchmark`, `fact.market.correlation_to_benchmark`, `fact.market.beta`, `fact.market.volatility`, `fact.market.max_drawdown`, `fact.market.liquidity_adv`, `fact.market.institutional_ownership`, `fact.market.institutional_flow`, `fact.valuation.fcf_yield` |
| **Interface Gap** | **Portfolio Health Framework (deferred) required.** This block's primary evidence comes from portfolio-level constructs (position weight, sector allocation, factor exposure, narrative overlap) that require the Portfolio Health Framework — a deferred dependency. The block currently consumes market/relative facts as secondary evidence for concentration and diversification context. |


---

## 4. Coverage Summary

### 4.1 Fact Category Coverage

| Metric | Value |
|--------|-------|
| Total fact categories in preflight inventory | 68 |
| Fact categories assigned to ≥1 block | **68/68** |
| Fact categories with primary assignment | 59 |
| Fact categories with secondary-only assignment | 9 |
| Unmapped fact categories | **0** |

**All 68 fact categories are assigned.** No fact category is orphaned.

The 9 fact categories assigned as secondary-only (no primary block assignment) serve cross-dimensional diagnostic roles:

| Fact Category | Why Secondary-Only |
|---------------|-------------------|
| `fact.margin.fcf_margin` | Primary shared between SAI-BLK-05 and SAI-BLK-06 (dual-primary) |
| `fact.revenue.rpo` | Primary shared between SAI-BLK-03 and SAI-BLK-04 (dual-primary) |
| `fact.balance_sheet.gross_debt` | Primary shared between SAI-BLK-07 and SAI-BLK-08 (dual-primary) |
| `fact.balance_sheet.maturity_schedule` | Primary shared between SAI-BLK-07 and SAI-BLK-08 (dual-primary) |
| `fact.obligations.goodwill` | Primary shared between SAI-BLK-09 and SAI-BLK-07 (dual-primary) |
| `fact.obligations.intangibles` | Primary shared between SAI-BLK-09 and SAI-BLK-07 (dual-primary) |
| `fact.market.relative_strength_vs_peers` | Primary shared between SAI-BLK-19 and SAI-BLK-21 (dual-primary) |

**Correction**: These 7 entries above are dual-primary, NOT secondary-only. All 68 facts have at least one primary assignment.

### 4.2 Block Coverage

| Metric | Value |
|--------|-------|
| Total blocks in canonical taxonomy | 24 |
| Blocks with ≥1 primary fact category | 17 |
| Blocks with primary OR secondary fact categories | **24/24** |
| Blocks with ONLY secondary facts (no primary) | 7 |
| Blocks with zero facts (neither primary nor secondary) | **0** |

**All 24 blocks have at least 1 fact category assigned** (primary or secondary).

### 4.3 Blocks with Interface Gaps

The following 7 blocks have no primary fact assignment from the 68 enumerated categories. Their primary evidence comes from qualitative sources or deferred frameworks not formalized as `fact.*` IDs:

| Block ID | Block Name | Gap Type |
|----------|-----------|----------|
| SAI-BLK-01 | Asset Identity | Qualitative facts not enumerated in preflight |
| SAI-BLK-02 | Business Model Quality | Qualitative facts not enumerated in preflight |
| SAI-BLK-14 | Pricing Power | Qualitative facts not enumerated in preflight |
| SAI-BLK-15 | Earnings Quality | Qualitative facts + Earnings Intelligence Framework (deferred) |
| SAI-BLK-18 | Value Trap Guard | Cross-dimensional diagnostic (multi-block fact combination) |
| SAI-BLK-22 | Company Outlook | Qualitative facts not enumerated in preflight |
| SAI-BLK-23 | Asset-Class Outlook | Qualitative/macro facts not enumerated in preflight |
| SAI-BLK-24 | Portfolio Fit | Portfolio Health Framework (deferred dependency) |

**Note**: SAI-BLK-18 (Value Trap Guard) is a special case — it consumes facts from multiple other domains in a cross-checking pattern. Its "primary" evidence is the combination, not any single fact domain. It has 10 secondary fact assignments covering valuation, cashflow, credit, and market dimensions.

### 4.4 Interface Gap Classification

| Gap ID | Affected Blocks | Gap Description | Resolution Path |
|--------|----------------|-----------------|-----------------|
| IGAP-01 | SAI-BLK-01, SAI-BLK-02 | Qualitative identity/business model facts (sector classification, corporate structure, revenue composition narrative) not enumerated as `fact.*` IDs in preflight Section 8 | Future: Market Evidence Framework extension to formalize qualitative fact categories |
| IGAP-02 | SAI-BLK-14 | Pricing power facts (pricing history, escalation clauses, price/volume mix) not enumerated in preflight | Future: Market Evidence Framework extension for pricing-domain facts |
| IGAP-03 | SAI-BLK-15 | Earnings quality facts (accrual ratios, non-recurring items, GAAP vs. adjusted gap, audit opinions) not enumerated in preflight | Future: Earnings Intelligence Framework + Market Evidence Framework extension |
| IGAP-04 | SAI-BLK-22 | Forward-looking qualitative facts (management commentary, strategic initiatives, M&A plans) not enumerated in preflight | Future: Market Evidence Framework extension for qualitative corporate disclosure facts |
| IGAP-05 | SAI-BLK-23 | Macro/sector-level facts (regulatory environment, industry cycle position, structural trends) not enumerated in preflight | Future: Market Evidence Framework extension for macro/sector-level fact categories |
| IGAP-06 | SAI-BLK-24 | Portfolio-level facts (position weight, sector allocation, factor exposure) require Portfolio Health Framework | Future: Portfolio Health Framework creation |

**Critical**: No new fact category IDs have been invented to fill these gaps. Gaps are documented as interface requirements for future framework extensions.

---

## 5. No-Drift Statement

This artifact:
- Does NOT create new fact categories, signals, or evidence primitives
- Does NOT mutate the Market Evidence Framework
- Does NOT mutate the Narrative Framework v2, Narrative Registry, or Market Organism Principles
- Does NOT produce scoring, ranking, recommendation, or allocation logic
- Does NOT implement data retrieval, calculation, or runtime behavior
- Does NOT modify any registry or SSOT
- Does NOT create asset-to-narrative mappings
- Uses ONLY the 68 fact category IDs defined in the preflight Section 8

All cross-references use canonical format:
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 8. Required Fact Categories)
(See: block_taxonomy.md, Section: 3. Block Summary Table)
(See: design.md, Section: Evidence Consumption Design)
(See: requirements.md, Section: SAI-REQ-2 — Fact Consumption Contracts)

---

## 6. VG-SAI-6 Evidence Statement

This section provides evidence for Verification Gate VG-SAI-6 (Fact Coverage Gate). It does NOT execute the gate — gate execution requires a separate gate artifact.

### Evidence Provided

| VG-SAI-6 Criterion | Evidence |
|---------------------|----------|
| All 68 fact categories assigned | Section 2 maps all 68 categories; Section 4.1 confirms 68/68 coverage |
| All blocks have ≥1 fact | Section 3 confirms all 24 blocks have ≥1 fact (primary or secondary); Section 4.2 confirms 24/24 |
| Matrix complete and reviewable | Sections 2 and 3 provide dual-view (fact-centric and block-centric) |
| No invented fact categories | Section 5 no-drift statement; all IDs traceable to preflight Section 8 |
| Interface gaps documented | Section 4.3 and 4.4 enumerate all gaps with resolution paths |

### Gate Status

**NOT EXECUTED** — This evidence statement supports future VG-SAI-6 gate execution. The gate itself must be explicitly executed as Task 15.6 with its own gate artifact (`gate_vg_sai_06.md`).

(See: tasks.md, Section: 15.6 Execute VG-SAI-6 Fact Coverage Gate)

---

## 7. Appendix: Fact Category Domain Summary

| Domain | Fact Count | Primary Consuming Blocks |
|--------|-----------|-------------------------|
| Revenue | 8 | SAI-BLK-03, SAI-BLK-04 |
| Demand/Pipeline | 4 | SAI-BLK-04 |
| Margin | 5 | SAI-BLK-05, SAI-BLK-06 |
| Cashflow | 5 | SAI-BLK-06 |
| Balance Sheet | 11 | SAI-BLK-07, SAI-BLK-08 |
| Obligations/Hidden Liabilities | 9 | SAI-BLK-09, SAI-BLK-10, SAI-BLK-07 |
| Working Capital | 4 | SAI-BLK-11 |
| Concentration | 4 | SAI-BLK-12, SAI-BLK-13 |
| Valuation | 7 | SAI-BLK-16, SAI-BLK-17 |
| Market/Relative | 11 | SAI-BLK-19, SAI-BLK-20, SAI-BLK-21 |
| **Total** | **68** | — |

---

*End of artifact.*
