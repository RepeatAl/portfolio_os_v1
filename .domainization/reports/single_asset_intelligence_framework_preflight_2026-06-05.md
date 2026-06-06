# Single Asset Intelligence Framework — Preflight Report

**Spec**: `single-asset-intelligence-framework`
**Date**: 2026-06-05
**Branch**: `spec/single-asset-intelligence-framework`
**Type**: Preflight reconnaissance / architecture definition
**Status**: PREFLIGHT ONLY

---

## 1. Executive Summary

### Readiness Assessment

The system is architecturally ready to proceed with the Single Asset Intelligence Framework specification. The foundational evidence layer — Market Evidence Framework — is canonicalized on `main` as of 2026-06-04 and provides the complete ontological hierarchy (Observed_Facts → Calculated_Signals → Evidence_Containers) required for asset-level evidence consumption. The Narrative Registry is populated with 3 canonical narratives (AI Infrastructure, Defense Rearmament, GLP-1/Obesity Medicine) and provides narrative-context linkage capability.

### Available Foundations

| Foundation | Status | Location |
|-----------|--------|----------|
| Market Evidence Framework | Canonical SSOT on main | `docs/README_market_evidence_framework.md` |
| Narrative Registry | Populated (3 entries) | `docs/registries/narrative_registry.yaml` |
| Narrative Framework v2 | Canonical on main | `docs/README_narrative_framework_v2.md` |
| Market Organism Principles | Canonical on main | `docs/README_market_organism_principles.md` |
| State_Change Taxonomy | Canonical on main | Referenced in Narrative Framework |
| Expansion Taxonomy | Canonical on main | Referenced in Market Evidence Framework |

### Missing Foundations (Backlog)

| Missing Framework | Impact on SAI | Resolution |
|------------------|---------------|------------|
| Valuation Framework | Valuation Context block partially unbacked | Deferred — SAI declares interface contract |
| Earnings Intelligence Framework | Earnings Quality block partially unbacked | Deferred — SAI declares interface contract |
| Peer Group Registry | Peer Comparison block partially unbacked | Deferred — SAI declares interface contract |
| Signal Calculation Framework | Signal derivation rules underdefined | Deferred — SAI consumes signals, does not define calculation |
| Data Ingestion/Normalization Framework | Raw data pipeline underdefined | Deferred — SAI consumes normalized facts |

### Primary Risk

Scope creep into scoring/recommendation territory. The Single Asset Intelligence Framework MUST remain diagnostic and interpretive only. It organizes evidence about a single asset into structured analysis blocks. It does NOT score, rank, recommend, allocate, or produce buy/sell signals.

### Recommendation

**PROCEED** to requirements phase. All architectural foundations required for definition-layer work are in place. Missing frameworks are documented as gaps with clear interface contracts.

(See: README_market_evidence_framework, Section: 1. Scope Statement)
(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)

---

## 2. Source Inventory

### Canonical Sources Available on Main


| # | Source Document | Artifact ID | Status | Relevance to SAI |
|---|----------------|-------------|--------|-----------------|
| 1 | Market Evidence Framework | `market_evidence_framework_md` | Canonical SSOT | PRIMARY — defines Facts, Signals, Evidence Objects consumed by SAI |
| 2 | Narrative Registry | `narrative_registry_yaml` | Populated (3 narratives) | Provides narrative-context for asset exposure mapping (future) |
| 3 | Narrative Framework v2 | `narrative_framework_md` | Canonical SSOT | Defines narrative lifecycle, falsification, connected systems |
| 4 | Market Organism Principles | `market_organism_principles_md` | Canonical SSOT | Foundational reasoning principles (causation, feedback loops) |
| 5 | State_Change Taxonomy | `state_change_taxonomy_md` | Canonical | Event classification for fact provenance |
| 6 | Expansion Taxonomy | `expansion_taxonomy_md` | Canonical | Growth-mode classification for revenue/demand signals |
| 7 | Shared Glossary Reference | `shared_glossary_reference_md` | Canonical | Term definitions and semantic consistency |
| 8 | Domainization Governance | `deployment_authority_model_yaml` | Canonical | Authority model for artifact lifecycle |

### Missing Sources (Future / Backlog)

| # | Missing Source | Expected Artifact ID | Impact on SAI | Priority |
|---|--------------|---------------------|---------------|----------|
| 1 | Portfolio Health Framework | `portfolio_health_framework_md` | Portfolio Fit block cannot reference canonical portfolio-level constructs | HIGH — next layer above SAI |
| 2 | Correlation/Dependency Framework | `correlation_dependency_framework_md` | Benchmark/Peer Correlation block partially unbacked | MEDIUM |
| 3 | Signal Calculation Framework | `signal_calculation_framework_md` | Signal derivation formulas not canonicalized | MEDIUM |
| 4 | Data Ingestion/Normalization Framework | `data_ingestion_normalization_framework_md` | Raw data pipeline contracts undefined | MEDIUM |
| 5 | Scoring Methodology Framework | `scoring_methodology_framework_md` | SAI does NOT score — but scoring layer consumes SAI output | LOW (SAI is upstream) |
| 6 | Valuation Framework | `valuation_framework_md` | Valuation Context and Value Trap Guard blocks partially unbacked | HIGH |
| 7 | Earnings Intelligence Framework | `earnings_intelligence_framework_md` | Earnings Quality and Guidance blocks partially unbacked | HIGH |
| 8 | Peer Group Registry | `peer_group_registry_yaml` | Peer Comparison block has no canonical peer definitions | MEDIUM |

### Upstream Inputs Requiring Canonicalization

| Input | Current Form | Required Canonicalization |
|-------|-------------|--------------------------|
| KPI-Micro Asset Analysis Sheet | Spreadsheet / manual analysis | Must be mapped to canonical fact categories and analysis blocks |
| Market KPI Monitor List | External reference list | Must be formalized as canonical signal/fact source registry |
| Analyst Coverage Notes | Unstructured research notes | Must be decomposed into Observed_Facts per Market Evidence Framework |

(See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)
(See: narrative_registry, Section: REGISTRY ENTRIES — Wave 1 Population)

---

## 3. Boundary Definition

### Single Asset Intelligence IS

| Capability | Description |
|-----------|-------------|
| Company/Asset Diagnostic Architecture | Structured framework for organizing all evidence about a single company or asset |
| Financial Stability Interpretation | Assessment of balance sheet health, credit risk, solvency, liquidity — diagnostic only |
| Operational Reality Assessment | Evaluation of revenue quality, demand visibility, margin durability, cashflow conversion |
| Valuation-Context Guard | Provides valuation context (cheap vs. impaired, expensive vs. justified) — no buy/sell |
| Peer/Benchmark Reality Check | Relative strength, correlation, beta analysis against relevant comparators |
| Outlook Interpretation Input | Structured input for company and sector outlook assessment |
| Portfolio-Fit Input | Provides concentration, dependency, and diversification context for portfolio-level consumers |

### Single Asset Intelligence is NOT

| Excluded Capability | Why Excluded | Where It Belongs |
|--------------------|--------------|-----------------|
| Buy/Sell Engine | SAI is diagnostic, not prescriptive | Future: Decision Engine (not yet designed) |
| Allocation Engine | SAI assesses one asset; allocation is portfolio-level | Future: Portfolio Allocation Framework |
| Scoring Engine | SAI interprets evidence; scoring reduces to numbers | Future: Scoring Methodology Framework |
| Asset-to-Narrative Mapping | Mapping assets to narratives is a separate concern | Narrative Population Framework |
| Market Regime Framework | Regime detection is market-level, not asset-level | Future: Market Regime Framework |
| Dashboard | SAI is a data/logic layer, not a presentation layer | Future: Reporting/UI layer |
| Trading System | SAI has zero execution capability | Out of scope permanently |
| Implementation Code | This preflight is definition-only | Future: Implementation phase |

### Boundary Enforcement Principle

The SAI Framework defines WHAT analysis blocks exist, WHAT evidence they consume, and WHAT their interpretive boundaries are. It does NOT define HOW to calculate, HOW to score, or WHAT to do with the output.

(See: README_market_evidence_framework, Section: 1. Scope Statement — "definition-layer document")
(See: README_market_organism_principles, Section: Principle 2 — Layers of Abstraction)

---

## 4. Relationship to Market Evidence Framework

### Dependency Model

```
┌─────────────────────────────────────────────────┐
│        Single Asset Intelligence Framework       │
│   (Organizes & interprets asset-level evidence)  │
└──────────────────────┬──────────────────────────┘
                       │ CONSUMES
                       ▼
┌─────────────────────────────────────────────────┐
│          Market Evidence Framework                │
│   (Defines Facts, Signals, Evidence Objects)     │
└─────────────────────────────────────────────────┘
```

### Consumption Rules

1. **SAI consumes Observed_Facts** — Every analysis block in SAI is fed by one or more fact categories defined in the Market Evidence Framework
2. **SAI consumes Calculated_Signals** — SAI interprets signal values within analysis block context
3. **SAI may reference Evidence_Containers** — When grouped evidence is relevant to an analysis block
4. **SAI MUST maintain provenance** — Every interpretation in SAI must trace back to specific facts/signals with full provenance chain
5. **SAI MUST NOT create hidden facts/signals/evidence objects** — During this preflight or any future phase, SAI cannot mint new evidence primitives without going through the Market Evidence Framework's creation rules

### Provenance Contract

| Rule | Description |
|------|-------------|
| Provenance-linked | Every SAI analysis block output must reference the facts/signals it consumed |
| No orphan interpretations | An interpretation without evidence provenance is invalid |
| No fact creation | SAI does not create facts — it consumes them |
| No signal creation | SAI does not define signal calculations — it consumes calculated signals |
| Timestamp inheritance | SAI interpretations inherit the temporal context of their source evidence |

(See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)
(See: README_market_evidence_framework, Section: Layer 1: Observed Facts — Properties)

---

## 5. Relationship to Narrative Registry

### Current State

The Narrative Registry contains 3 canonical narratives as of 2026-06-05:
- `narrative.ai_infrastructure` — AI infrastructure buildout supercycle
- `narrative.defense_rearmament` — Structural defense spending increase
- `narrative.glp1_obesity_medicine` — GLP-1 obesity medicine market expansion

### Future Relationship (Post-SAI)

In future phases, SAI MAY identify which narratives a given asset has exposure to. For example: an asset in the semiconductor space may have exposure to `narrative.ai_infrastructure`. This linkage would enable portfolio-level narrative concentration analysis.

### Strict Boundaries During Preflight

| Constraint | Rationale |
|-----------|-----------|
| MUST NOT create Asset-to-Narrative mappings | This is the Narrative Population Framework's responsibility |
| MUST NOT add narratives to the registry | Narrative creation follows its own lifecycle and falsification process |
| MUST NOT treat asset baskets as narratives | A basket of assets is not a narrative — narratives are belief structures |
| MUST NOT infer narrative exposure without evidence | Exposure requires explicit evidence linking per Market Evidence Framework |

### Interface Contract (Future)

When SAI eventually surfaces narrative exposure, it will:
1. Reference the canonical `narrative_id` from the Narrative Registry
2. Provide evidence provenance for the exposure claim
3. Respect the narrative's `lifecycle_state` (a falsified narrative has no forward exposure)
4. Not conflate sector membership with narrative exposure

(See: narrative_registry, Section: narratives — Entry 1: AI Infrastructure)
(See: README_narrative_framework_v2, Section: Narrative Lifecycle States)

---

## 6. Core Analysis Blocks


The Single Asset Intelligence Framework organizes asset-level evidence into 24 canonical analysis blocks. Each block represents a discrete analytical dimension. Blocks are not scored — they are diagnostic containers that organize evidence for interpretation.

| # | Block Name | Category | Primary Evidence Source | Dependency |
|---|-----------|----------|------------------------|------------|
| 1 | Asset Identity | Foundation | Corporate filings, sector classification | None |
| 2 | Business Model Quality | Foundation | Revenue mix, customer type, recurring vs. transactional | None |
| 3 | Revenue Quality | Operational | Revenue growth, organic growth, ARR, RPO, backlog | None |
| 4 | Demand / Pipeline | Operational | Order intake, book-to-bill, backlog, pipeline indicators | None |
| 5 | Margin Quality | Operational | Gross margin, operating margin, EBITDA margin, trends | None |
| 6 | Cashflow Quality | Operational | Operating CF, FCF, FCF conversion, capex intensity | None |
| 7 | Balance Sheet Quality | Financial Stability | Cash, debt structure, maturity schedule, leverage ratios | None |
| 8 | Credit / Solvency Risk | Financial Stability | Interest coverage, net debt/EBITDA, FCF/debt, ratings | None |
| 9 | Hidden Liabilities | Financial Stability | Off-balance-sheet, litigation, guarantees, contingencies | None |
| 10 | Pension Obligations | Financial Stability | Pension funding gap, plan status, obligation trajectory | None |
| 11 | Working Capital | Operational | Inventory, DSO, DPO, working capital cycle | None |
| 12 | Customer Concentration | Risk | Revenue concentration, top-customer dependency | None |
| 13 | Supply Chain Stability | Risk | Supplier concentration, geographic risk, capacity constraints | None |
| 14 | Pricing Power | Operational | Ability to pass through costs, competitive moat indicators | None |
| 15 | Earnings Quality | Earnings | Accrual quality, one-offs, adjustments, GAAP vs. adjusted gap | Earnings Intelligence Framework (future) |
| 16 | Guidance / Estimate Revisions | Earnings | Management guidance, consensus estimate revisions, beat/miss history | Earnings Intelligence Framework (future) |
| 17 | Valuation Context | Valuation | Multiples, FCF yield, PEG, relative valuation | Valuation Framework (future) |
| 18 | Value Trap Guard | Valuation | Cheap-but-impaired detection, structural vs. cyclical discount | Valuation Framework (future) |
| 19 | Relative Strength | Market Position | Price momentum vs. benchmark, sector, peers | None |
| 20 | Benchmark / Sector / Peer Correlation | Market Position | Beta, correlation coefficients, co-movement patterns | Correlation/Dependency Framework (future) |
| 21 | Peer Comparison | Market Position | Operational/financial comparison to defined peer group | Peer Group Registry (future) |
| 22 | Company Outlook | Outlook | Forward guidance, strategic direction, management credibility | None |
| 23 | Asset-Class Outlook | Outlook | Sector/industry outlook, structural trends, regulatory trajectory | None |
| 24 | Portfolio Fit | Portfolio Context | Concentration, dependency overlap, narrative overlap, diversification | Portfolio Health Framework (future) |

### Block Architecture Principles

1. **Independence**: Each block can be assessed independently — no block requires another block's output to function
2. **Evidence-backed**: Every block must consume at least one fact category from Market Evidence Framework
3. **Non-scoring**: Blocks organize and interpret evidence — they do not produce numeric scores
4. **Composable**: Higher layers (scoring, allocation, reporting) may consume any combination of blocks
5. **Extensible**: New blocks can be added without breaking existing blocks (additive-only architecture)

(See: README_market_evidence_framework, Section: 2. Glossary Reference — Evidence_Container)
(See: README_market_organism_principles, Section: Principle 3 — Additive Architecture)

---

## 7. Micro KPI Mapping

### Purpose

This section maps representative KPIs from a typical micro asset analysis sheet (e.g., KPI-Micro Asset Analysis Sheet) into the canonical analysis block structure. This mapping validates that the 24 analysis blocks can absorb real-world analytical practice.

### Representative KPI-to-Block Mapping

| # | Source KPI (from Micro Sheet) | Canonical Block | Required Fact Category | Required Signal Category | Red Flag Example | Missing Dependency |
|---|------------------------------|-----------------|----------------------|------------------------|-----------------|-------------------|
| 1 | Revenue Growth YoY | Revenue Quality | `fact.revenue.growth_yoy` | `revenue_quality_signal` | Negative organic growth masked by acquisitions | None |
| 2 | Organic Revenue Growth | Revenue Quality | `fact.revenue.organic_growth` | `revenue_quality_signal` | Organic growth negative for 3+ quarters | None |
| 3 | ARR / Recurring Revenue % | Revenue Quality | `fact.revenue.arr`, `fact.revenue.recurring_pct` | `revenue_quality_signal` | ARR growth decelerating while total revenue grows (mix shift) | None |
| 4 | Order Intake | Demand / Pipeline | `fact.demand.order_intake` | `demand_visibility_signal` | Order intake below revenue (book-to-bill < 1.0) | None |
| 5 | Book-to-Bill Ratio | Demand / Pipeline | `fact.demand.book_to_bill` | `demand_visibility_signal` | Sustained below 1.0 — demand erosion | None |
| 6 | Backlog / RPO | Demand / Pipeline | `fact.demand.backlog`, `fact.revenue.rpo` | `demand_visibility_signal` | Backlog declining while revenue maintained (pull-forward risk) | None |
| 7 | Gross Margin | Margin Quality | `fact.margin.gross_margin` | `margin_durability_signal` | Gross margin compression >200bps without revenue offset | None |
| 8 | Operating Margin | Margin Quality | `fact.margin.operating_margin` | `margin_durability_signal` | Operating leverage negative (costs growing faster than revenue) | None |
| 9 | EBITDA Margin | Margin Quality | `fact.margin.ebitda_margin` | `margin_durability_signal` | EBITDA margin decline masked by addbacks | None |
| 10 | Free Cash Flow | Cashflow Quality | `fact.cashflow.fcf` | `cashflow_conversion_signal` | Negative FCF despite positive EBITDA | None |
| 11 | FCF Conversion | Cashflow Quality | `fact.cashflow.fcf_conversion` | `cashflow_conversion_signal` | Conversion consistently below 70% — working capital or capex issue | None |
| 12 | Net Debt / EBITDA | Credit / Solvency Risk | `fact.balance_sheet.net_debt_ebitda` | `liquidity_stress_signal` | Leverage above 4x with declining EBITDA | None |
| 13 | Interest Coverage | Credit / Solvency Risk | `fact.balance_sheet.interest_coverage` | `interest_coverage_deterioration_signal` | Coverage below 3x and declining | None |
| 14 | Debt Maturity Schedule | Balance Sheet Quality | `fact.balance_sheet.maturity_schedule` | `refinancing_risk_signal` | Material maturity wall within 18 months + tight credit markets | None |
| 15 | Pension Funding Status | Pension Obligations | `fact.obligations.pension_funding_gap` | `pension_underfunding_signal` | Underfunding >20% of market cap | None |
| 16 | Customer Concentration | Customer Concentration | `fact.concentration.top_customer_pct` | `customer_concentration_risk_signal` | Single customer >30% of revenue | None |
| 17 | EV/EBITDA Multiple | Valuation Context | `fact.valuation.ev_ebitda` | `valuation_stretch_signal` | >2 standard deviations above historical median | Valuation Framework |
| 18 | FCF Yield | Valuation Context | `fact.valuation.fcf_yield` | `valuation_stretch_signal` | FCF yield below risk-free rate | Valuation Framework |
| 19 | Relative Strength vs. Index | Relative Strength | `fact.market.relative_strength_vs_benchmark` | `relative_strength_signal` | Persistent underperformance despite sector tailwind | None |
| 20 | Estimate Revisions (3M) | Guidance / Estimate Revisions | `fact.earnings.estimate_revision_3m` | `estimate_revision_signal` | Negative revision trend accelerating | Earnings Intelligence Framework |

### Mapping Completeness Assessment

- **20 of 24 blocks** have at least one representative KPI mapping
- **4 blocks** (Asset Identity, Business Model Quality, Supply Chain Stability, Asset-Class Outlook) require qualitative fact inputs not typically captured in numeric KPI sheets
- **3 blocks** have explicit missing framework dependencies (Valuation Context, Guidance/Estimate Revisions, Peer Comparison)

(See: README_market_evidence_framework, Section: Layer 1: Observed Facts — Examples)
(See: README_market_evidence_framework, Section: Layer 2: Calculated_Signal)

---

## 8. Required Fact Categories


The following fact categories represent the minimum set of Observed_Facts required to populate the 24 analysis blocks. These are organized by analytical domain.

### Revenue Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 1 | `fact.revenue.total_revenue` | Total reported revenue | Corporate filing |
| 2 | `fact.revenue.growth_yoy` | Year-over-year revenue growth rate | Corporate filing (derived) |
| 3 | `fact.revenue.growth_qoq` | Quarter-over-quarter revenue growth rate | Corporate filing (derived) |
| 4 | `fact.revenue.organic_growth` | Organic revenue growth (ex-M&A, ex-FX) | Corporate filing / management disclosure |
| 5 | `fact.revenue.arr` | Annual Recurring Revenue | Corporate filing (SaaS/subscription models) |
| 6 | `fact.revenue.rpo` | Remaining Performance Obligations | Corporate filing (ASC 606) |
| 7 | `fact.revenue.backlog` | Order backlog / contracted revenue not yet recognized | Corporate filing |
| 8 | `fact.revenue.recurring_pct` | Percentage of recurring vs. transactional revenue | Corporate filing / management disclosure |

### Demand / Pipeline Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 9 | `fact.demand.order_intake` | New orders received in period | Corporate filing |
| 10 | `fact.demand.book_to_bill` | Ratio of orders received to revenue recognized | Corporate filing (derived) |
| 11 | `fact.demand.pipeline_value` | Total pipeline value (if disclosed) | Management disclosure |
| 12 | `fact.demand.win_rate` | Contract win rate (if disclosed) | Management disclosure |

### Margin Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 13 | `fact.margin.gross_margin` | Gross margin percentage | Corporate filing |
| 14 | `fact.margin.operating_margin` | Operating margin percentage | Corporate filing |
| 15 | `fact.margin.ebitda_margin` | EBITDA margin percentage | Corporate filing |
| 16 | `fact.margin.fcf_margin` | Free cash flow as percentage of revenue | Corporate filing (derived) |
| 17 | `fact.margin.gross_margin_trend` | Gross margin directional trend (expanding/stable/compressing) | Corporate filing (multi-period) |

### Cashflow Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 18 | `fact.cashflow.operating_cf` | Cash flow from operations | Corporate filing |
| 19 | `fact.cashflow.fcf` | Free cash flow (operating CF minus capex) | Corporate filing (derived) |
| 20 | `fact.cashflow.fcf_conversion` | FCF as percentage of net income or EBITDA | Corporate filing (derived) |
| 21 | `fact.cashflow.capex` | Capital expenditure | Corporate filing |
| 22 | `fact.cashflow.capex_intensity` | Capex as percentage of revenue | Corporate filing (derived) |

### Balance Sheet Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 23 | `fact.balance_sheet.cash` | Cash and cash equivalents | Corporate filing |
| 24 | `fact.balance_sheet.gross_debt` | Total gross debt (short-term + long-term) | Corporate filing |
| 25 | `fact.balance_sheet.net_debt` | Net debt (gross debt minus cash) | Corporate filing (derived) |
| 26 | `fact.balance_sheet.maturity_schedule` | Debt maturity profile by year | Corporate filing (notes) |
| 27 | `fact.balance_sheet.short_term_debt` | Debt maturing within 12 months | Corporate filing |
| 28 | `fact.balance_sheet.interest_expense` | Annual interest expense | Corporate filing |
| 29 | `fact.balance_sheet.interest_coverage` | EBIT / interest expense ratio | Corporate filing (derived) |
| 30 | `fact.balance_sheet.net_debt_ebitda` | Net debt / EBITDA leverage ratio | Corporate filing (derived) |
| 31 | `fact.balance_sheet.fcf_to_debt` | FCF / gross debt ratio | Corporate filing (derived) |
| 32 | `fact.balance_sheet.current_ratio` | Current assets / current liabilities | Corporate filing |
| 33 | `fact.balance_sheet.quick_ratio` | (Current assets - inventory) / current liabilities | Corporate filing (derived) |

### Obligations / Hidden Liabilities Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 34 | `fact.obligations.lease_liabilities` | Total operating + finance lease obligations | Corporate filing (IFRS 16 / ASC 842) |
| 35 | `fact.obligations.pension_obligations` | Defined benefit pension obligations | Corporate filing |
| 36 | `fact.obligations.pension_funding_gap` | Underfunding amount (obligation minus plan assets) | Corporate filing |
| 37 | `fact.obligations.purchase_obligations` | Non-cancellable purchase commitments | Corporate filing (notes) |
| 38 | `fact.obligations.litigation_exposure` | Material litigation / legal contingencies | Corporate filing (notes) |
| 39 | `fact.obligations.off_balance_sheet` | Off-balance-sheet arrangements and guarantees | Corporate filing (notes) |
| 40 | `fact.obligations.goodwill` | Total goodwill on balance sheet | Corporate filing |
| 41 | `fact.obligations.intangibles` | Total intangible assets | Corporate filing |
| 42 | `fact.obligations.goodwill_to_equity` | Goodwill as percentage of total equity | Corporate filing (derived) |

### Working Capital Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 43 | `fact.working_capital.inventory` | Total inventory | Corporate filing |
| 44 | `fact.working_capital.dso` | Days Sales Outstanding | Corporate filing (derived) |
| 45 | `fact.working_capital.dpo` | Days Payable Outstanding | Corporate filing (derived) |
| 46 | `fact.working_capital.inventory_days` | Days Inventory Outstanding | Corporate filing (derived) |

### Concentration Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 47 | `fact.concentration.top_customer_pct` | Revenue from largest customer (%) | Corporate filing (segment/notes) |
| 48 | `fact.concentration.top_5_customers_pct` | Revenue from top 5 customers (%) | Corporate filing / management disclosure |
| 49 | `fact.concentration.supplier_concentration` | Dependence on key suppliers | Corporate filing (risk factors) |
| 50 | `fact.concentration.geographic_concentration` | Revenue by geography | Corporate filing (segment) |

### Valuation Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 51 | `fact.valuation.ev_ebitda` | EV/EBITDA multiple | Market data + corporate filing |
| 52 | `fact.valuation.ev_fcf` | EV/FCF multiple | Market data + corporate filing |
| 53 | `fact.valuation.pe_ratio` | Price/Earnings ratio | Market data + corporate filing |
| 54 | `fact.valuation.fcf_yield` | FCF yield (FCF / market cap) | Market data + corporate filing |
| 55 | `fact.valuation.peg_ratio` | PEG ratio (P/E / growth rate) | Market data + estimates |
| 56 | `fact.valuation.estimate_revisions_3m` | Consensus estimate revisions (3-month) | Analyst consensus data |
| 57 | `fact.valuation.guidance_revision` | Management guidance change vs. prior | Corporate filing / earnings call |

### Market / Relative Facts

| # | Fact Category ID | Description | Source Type |
|---|-----------------|-------------|-------------|
| 58 | `fact.market.relative_strength_vs_benchmark` | Price performance relative to primary benchmark | Market data |
| 59 | `fact.market.relative_strength_vs_sector` | Price performance relative to sector index | Market data |
| 60 | `fact.market.relative_strength_vs_peers` | Price performance relative to defined peer group | Market data |
| 61 | `fact.market.correlation_to_benchmark` | Correlation coefficient to benchmark | Market data (calculated) |
| 62 | `fact.market.beta` | Beta to benchmark | Market data (calculated) |
| 63 | `fact.market.volatility` | Realized volatility (annualized) | Market data (calculated) |
| 64 | `fact.market.max_drawdown` | Maximum drawdown from peak | Market data (calculated) |
| 65 | `fact.market.liquidity_adv` | Average daily volume / liquidity | Market data |
| 66 | `fact.market.short_interest` | Short interest as % of float | Market data |
| 67 | `fact.market.institutional_ownership` | Institutional ownership percentage | Regulatory filings (13F) |
| 68 | `fact.market.institutional_flow` | Net institutional buying/selling | Regulatory filings (13F, derived) |

### Total: 68 Fact Categories across 9 domains

(See: README_market_evidence_framework, Section: Layer 1: Observed Facts — Properties)
(See: README_market_evidence_framework, Section: Layer 1: What is NOT an Observed Fact)

---

## 9. Required Signal Categories


Calculated_Signals are derived values produced by applying defined calculations to one or more Observed_Facts. They are reproducible, timestamped, and non-causal (they detect, they do not cause). The following signal categories are required for the SAI Framework.

| # | Signal Category ID | Description | Input Facts | Analysis Block(s) Served |
|---|-------------------|-------------|-------------|--------------------------|
| 1 | `revenue_quality_signal` | Composite assessment of revenue health (growth, quality, durability, mix) | Revenue facts 1-8 | Revenue Quality |
| 2 | `demand_visibility_signal` | Forward demand confidence based on pipeline/backlog/order indicators | Demand facts 9-12, Revenue facts 6-7 | Demand / Pipeline |
| 3 | `margin_durability_signal` | Assessment of margin sustainability and trend | Margin facts 13-17 | Margin Quality |
| 4 | `cashflow_conversion_signal` | Quality of earnings-to-cash conversion | Cashflow facts 18-22, Margin facts | Cashflow Quality |
| 5 | `liquidity_stress_signal` | Near-term liquidity adequacy assessment | Balance sheet facts 23, 27, 32-33, Cashflow fact 19 | Balance Sheet Quality, Credit/Solvency |
| 6 | `refinancing_risk_signal` | Debt maturity wall risk relative to cash generation | Balance sheet facts 26-27, Cashflow fact 19 | Balance Sheet Quality, Credit/Solvency |
| 7 | `interest_coverage_deterioration_signal` | Trend in ability to service debt | Balance sheet facts 28-29, Margin facts | Credit / Solvency Risk |
| 8 | `pension_underfunding_signal` | Pension obligation risk relative to company resources | Obligations facts 35-36 | Pension Obligations |
| 9 | `off_balance_sheet_leverage_signal` | Hidden leverage from leases, guarantees, off-BS items | Obligations facts 34, 38-39 | Hidden Liabilities |
| 10 | `working_capital_stress_signal` | Working capital efficiency deterioration | Working capital facts 43-46 | Working Capital |
| 11 | `customer_concentration_risk_signal` | Revenue dependency risk from customer concentration | Concentration facts 47-48 | Customer Concentration |
| 12 | `supply_chain_fragility_signal` | Supply chain risk from supplier/geographic concentration | Concentration facts 49-50 | Supply Chain Stability |
| 13 | `earnings_quality_signal` | Assessment of reported earnings reliability and sustainability | Revenue facts, Margin facts, Cashflow facts | Earnings Quality |
| 14 | `estimate_revision_signal` | Direction and magnitude of consensus estimate changes | Valuation facts 56-57 | Guidance / Estimate Revisions |
| 15 | `guidance_quality_signal` | Management guidance credibility and revision pattern | Valuation fact 57, historical guidance accuracy | Guidance / Estimate Revisions |
| 16 | `valuation_stretch_signal` | Current valuation relative to historical and peer context | Valuation facts 51-55 | Valuation Context |
| 17 | `valuation_trap_risk_signal` | Probability that low valuation reflects structural impairment rather than opportunity | Valuation facts + Credit/Solvency facts + Cashflow facts | Value Trap Guard |
| 18 | `relative_strength_signal` | Momentum relative to benchmark, sector, and peers | Market facts 58-60 | Relative Strength |
| 19 | `peer_divergence_signal` | Degree of divergence from peer group behavior | Market facts 60, Peer operational comparison | Peer Comparison |
| 20 | `benchmark_beta_signal` | Whether stock moves by own strength or index/sector drag | Market facts 61-62 | Benchmark/Sector/Peer Correlation |
| 21 | `correlation_dependency_signal` | Degree of co-movement dependence on external factors | Market facts 61-62, 63 | Benchmark/Sector/Peer Correlation |
| 22 | `outlook_revision_signal` | Change in forward outlook assessment | Company Outlook inputs, Guidance facts | Company Outlook |
| 23 | `portfolio_fit_signal` | Asset contribution to portfolio diversification/concentration | Portfolio-level context, Concentration facts | Portfolio Fit |

### Signal Architecture Principles

1. **Derived, not observed**: Signals are always calculated from facts — never directly observed
2. **Reproducible**: Given the same input facts and formula, the signal value is deterministic
3. **Non-causal**: A signal detects a condition — it does not cause the condition
4. **Timestamped**: Every signal carries the timestamp of calculation and the temporal window of input facts
5. **Formula-defined**: Signal calculation formulas will be defined in the Signal Calculation Framework (future)
6. **SAI consumes, does not define**: SAI declares which signals it needs; the Signal Calculation Framework defines how they are computed

(See: README_market_evidence_framework, Section: Layer 2: Calculated_Signal)
(See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)

---

## 10. Valuation Trap Boundary

### Core Principle

**Low valuation ≠ undervaluation.** A stock is not cheap because it fell. A stock is not cheap because its multiple is low relative to history. "Cheap" means the market's embedded expectation is below a realistic assessment of future value creation — and that realistic assessment must itself be evidence-backed.

### Valuation Trap Taxonomy

| Condition | Interpretation | SAI Response |
|-----------|---------------|-------------|
| Low multiple + strong fundamentals | Potential opportunity — market may underweight evidence | Flag for deeper analysis (no recommendation) |
| Low multiple + deteriorating fundamentals | Potential value trap — cheapness reflects impairment | Flag value trap risk signal |
| Low multiple + high leverage + refinancing risk | Structural impairment — cheapness reflects solvency risk | Flag credit-solvency override |
| High multiple + strong growth + proven execution | Potentially justified — market pays for quality | Provide context (no "expensive" judgment without evidence) |
| High multiple + decelerating growth + narrative dependence | Potential overvaluation — market may overweight narrative | Flag valuation stretch signal |

### Evidence Requirements for Valuation Assessment

A valid valuation context assessment MUST consume:
1. **Cashflow evidence** — What is the company actually generating?
2. **Credit/solvency evidence** — Can the company survive to realize its value?
3. **Hidden liability evidence** — Are there claims not reflected in headline numbers?
4. **Outlook evidence** — What is the realistic forward trajectory?
5. **Peer context** — How does valuation compare to comparable companies?
6. **Earnings quality evidence** — Are reported earnings trustworthy?

### Explicit Constraints

- **No buy/sell recommendation authorized** — SAI provides valuation context, never prescriptive action
- **No price target** — SAI does not produce fair value estimates
- **No "undervalued" / "overvalued" label** — SAI provides evidence for interpretation, not conclusion
- **Valuation without context is meaningless** — A P/E of 8x means nothing without understanding WHY it's 8x

(See: README_market_evidence_framework, Section: 31. Valuation Trap Boundary)
(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)

---

## 11. Financial Stability / Credit-Solvency Boundary

### Scope

The Financial Stability dimension covers all evidence related to a company's ability to meet its financial obligations, maintain operational continuity, and avoid structural impairment from leverage, liquidity, or hidden claims.

### Evidence Domains

| Domain | Key Facts | Key Signals | Red Flags |
|--------|-----------|-------------|-----------|
| Debt Burden | Gross debt, net debt, net debt/EBITDA | `liquidity_stress_signal` | Leverage >4x with declining EBITDA |
| Refinancing Wall | Maturity schedule, short-term debt | `refinancing_risk_signal` | >30% of debt maturing within 18 months |
| Cashflow Coverage | FCF/debt, interest coverage | `interest_coverage_deterioration_signal` | Interest coverage <2x and declining |
| Liquidity Runway | Cash, current ratio, revolver availability | `liquidity_stress_signal` | Cash runway <12 months at current burn |
| Lease Obligations | Operating + finance leases (IFRS 16) | `off_balance_sheet_leverage_signal` | Leases >50% of reported debt equivalent |
| Pension Obligations | Funding gap, plan status, obligation growth | `pension_underfunding_signal` | Underfunding >20% of market cap |
| Off-Balance Commitments | Guarantees, purchase obligations, contingencies | `off_balance_sheet_leverage_signal` | Aggregate off-BS >2x reported debt |
| LBO / Sponsor History | Acquisition leverage, dividend recaps, sponsor overhang | `refinancing_risk_signal` | PE-loaded capital structure with near-term maturities |
| Goodwill Impairment Risk | Goodwill/equity ratio, acquisition history | N/A (qualitative flag) | Goodwill >100% of tangible equity |
| Covenant Pressure | Maintenance vs. incurrence covenants | `liquidity_stress_signal` | Within 10% of covenant trigger levels |
| Bond / CDS / Rating Evidence | Spread levels, CDS movement, rating actions | External market signals | Credit spread widening >200bps in 3 months |

### Credit Rating Policy

Credit ratings (S&P, Moody's, Fitch) are treated as **inputs, not truth**. Ratings are lagging indicators that reflect agency methodology, not real-time credit quality. SAI consumes ratings as one evidence point among many — never as the sole determinant of credit assessment.

### Structural Impairment Detection

A company is considered at risk of structural financial impairment when multiple signals converge:
- High leverage AND declining cashflow
- Near-term maturities AND tight credit markets
- Hidden liabilities AND weak equity cushion
- Pension underfunding AND negative demographic trend

SAI surfaces these convergences diagnostically. It does NOT predict default, assign credit scores, or recommend action.

(See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)
(See: README_market_evidence_framework, Section: Layer 1: Observed Facts — Source-attributed)

---

## 12. Earnings / Operational Reality Boundary


### Scope

The Earnings / Operational Reality dimension covers all evidence related to whether a company's reported performance reflects genuine economic reality, whether forward guidance is credible, and whether operational demand is sustainable.

### Core Questions This Dimension Answers

1. **Earnings Quality**: Are reported earnings trustworthy? What is the gap between GAAP and adjusted? Are there recurring "one-offs"?
2. **Revenue Quality**: Is revenue organic? Is it recurring? Is it growing from real demand or accounting timing?
3. **Guidance Credibility**: Does management consistently guide accurately? What is the beat/miss pattern?
4. **Estimate Momentum**: Is consensus moving up or down? Is the revision rate accelerating?
5. **Demand Reality**: Is the backlog real (will it convert)? Is book-to-bill sustainable? Is order intake representing genuine new demand or pull-forward?
6. **Margin Durability**: Are margins expanding due to operating leverage or one-time benefits? Can current margins be maintained?
7. **FCF Conversion**: Is the company converting reported earnings to actual cash? If not, why?
8. **Working Capital**: Is working capital consuming cash (inventory build, receivables stretch)?
9. **Customer Concentration**: Is growth dependent on a single customer or a broad base?
10. **Supply Chain Capacity**: Can the company fulfill demand? Are there constraints?

### Evidence Matrix

| Question | Primary Facts | Primary Signals | Confidence Requirement |
|----------|--------------|-----------------|----------------------|
| Earnings Quality | GAAP vs. adjusted gap, accrual ratios, one-off frequency | `earnings_quality_signal` | Minimum 4 quarters history |
| Revenue Quality | Organic growth, recurring %, ARR trajectory | `revenue_quality_signal` | Minimum 4 quarters history |
| Guidance Credibility | Historical guidance vs. actual, revision frequency | `guidance_quality_signal` | Minimum 8 quarters history |
| Estimate Momentum | 3M/6M/12M revision direction and magnitude | `estimate_revision_signal` | Current consensus + history |
| Demand Reality | Book-to-bill, backlog conversion rate, pipeline quality | `demand_visibility_signal` | Minimum 4 quarters history |
| Margin Durability | Margin trend, cost structure, operating leverage | `margin_durability_signal` | Minimum 4 quarters + peer context |
| FCF Conversion | FCF/net income, FCF/EBITDA, working capital impact | `cashflow_conversion_signal` | Minimum 4 quarters history |
| Working Capital | DSO trend, inventory days, DPO trend | `working_capital_stress_signal` | Minimum 4 quarters history |
| Customer Concentration | Top customer %, top 5 %, trend | `customer_concentration_risk_signal` | Current disclosure |
| Supply Chain | Supplier concentration, geographic risk, capacity utilization | `supply_chain_fragility_signal` | Current disclosure + qualitative |

### Operational Reality Red Flags

| Red Flag | Evidence Required | Severity |
|----------|------------------|----------|
| Persistent GAAP-to-adjusted gap >30% | 4+ quarters of large adjustments | HIGH |
| Book-to-bill consistently <1.0 | 3+ quarters below 1.0 | HIGH |
| FCF conversion <50% with growing revenue | Cash not following reported earnings | HIGH |
| Inventory build exceeding revenue growth | Working capital consuming cash | MEDIUM |
| Customer concentration >40% single name | Revenue dependency risk | HIGH |
| Guidance consistently missed or revised down | 3+ quarters of negative revision | MEDIUM |
| Organic growth negative while total growth positive | Growth from M&A only | MEDIUM |
| Backlog declining while revenue maintained | Demand pull-forward exhaustion | HIGH |

(See: README_market_evidence_framework, Section: Layer 2: Calculated_Signal — "reproducible given the same inputs and formula")
(See: README_market_organism_principles, Section: Principle 5 — Reality over Narrative)

---

## 13. Peer / Benchmark Reality Boundary

### Scope

The Peer / Benchmark Reality dimension covers all evidence related to whether an asset's price behavior reflects its own fundamental strength or is merely a function of index membership, sector rotation, or peer-group correlation.

### Core Analytical Questions

1. **Does this stock move by its own strength?** Or is it dragged by benchmark/sector momentum?
2. **What is the correlation structure?** High correlation to benchmark = less idiosyncratic alpha potential
3. **How does beta behave asymmetrically?** Does the stock participate in upside but amplify downside (or vice versa)?
4. **How does it compare operationally to peers?** Not just price — fundamentals vs. peer fundamentals
5. **Is relative strength genuine?** Outperformance with weaker fundamentals = fragile. Underperformance with strong fundamentals = potential opportunity.

### Evidence Domains

| Domain | Key Facts | Key Signals | Interpretation |
|--------|-----------|-------------|---------------|
| Relative Strength | `fact.market.relative_strength_vs_benchmark/sector/peers` | `relative_strength_signal` | Positive RS = outperforming; but must check WHY |
| Correlation | `fact.market.correlation_to_benchmark` | `correlation_dependency_signal` | High correlation = index proxy; low correlation = idiosyncratic |
| Beta | `fact.market.beta` | `benchmark_beta_signal` | Beta >1.5 = amplified market risk; Beta <0.5 = defensive |
| Volatility | `fact.market.volatility` | N/A (input to other signals) | Context for risk-adjusted assessment |
| Drawdown | `fact.market.max_drawdown` | N/A (input to risk assessment) | Historical downside behavior |
| Peer Divergence | Peer operational metrics comparison | `peer_divergence_signal` | Fundamental divergence from peers may explain price divergence |

### Beta Decomposition Principle

Stock return = alpha + (beta × market return) + residual

SAI must decompose price behavior to distinguish:
- **Genuine alpha**: Asset outperforms because of its own fundamentals
- **Beta participation**: Asset moves because the market/sector moves
- **Correlation drag**: Asset underperforms because of benchmark/sector weakness despite own strength

### Peer Comparison Requirements

A valid peer comparison requires:
1. **Defined peer group** — Not arbitrary; peers must share business model, end-market, or size characteristics
2. **Consistent metrics** — Same metrics compared across all peers (apples-to-apples)
3. **Time-aligned** — Same reporting periods compared
4. **Contextual** — Differences explained, not just flagged

Note: The Peer Group Registry (future framework) will provide canonical peer group definitions. Until then, peer comparisons are ad-hoc and flagged as lower confidence.

(See: README_market_evidence_framework, Section: Market-level facts — relative positioning)
(See: README_market_organism_principles, Section: Principle 4 — Context over Isolated Data Points)

---

## 14. Portfolio Fit Boundary

### Scope

The Portfolio Fit dimension provides evidence about how a single asset would contribute to (or detract from) portfolio-level characteristics. It is an INPUT to portfolio-level decisions — never the decision itself.

### What Portfolio Fit Assesses

| Dimension | Description | Evidence Required |
|-----------|-------------|------------------|
| Concentration Contribution | Would adding/holding this asset increase concentration risk? | Position size, sector weight, geographic weight |
| Dependency Overlap | Does this asset share dependencies with existing holdings? | Supply chain, customer base, regulatory exposure |
| Narrative Overlap | Does this asset have exposure to narratives already represented? | Narrative Registry linkage (future) |
| Macro Sensitivity | How does this asset respond to macro factors (rates, inflation, FX)? | Beta to macro factors, historical sensitivity |
| Liquidity Sensitivity | Can this position be exited without material market impact? | ADV, position size vs. ADV, bid-ask spread |
| Diversification Contribution | Does this asset reduce portfolio risk through low correlation? | Correlation to existing holdings |
| Portfolio Fragility | Does this asset add to or reduce overall portfolio fragility? | Tail risk contribution, drawdown behavior |

### Explicit Constraints

| Constraint | Rationale |
|-----------|-----------|
| NO allocation decision | SAI provides fit context; allocation is a portfolio-level decision |
| NO position sizing | SAI does not determine how much to hold |
| NO buy/sell based on fit | Fit is one input among many; never sufficient for action |
| NO portfolio optimization | Mathematical optimization is out of SAI scope |
| Portfolio Health Framework required | Full portfolio fit requires the future Portfolio Health Framework |

### Interface to Portfolio Layer

SAI's Portfolio Fit block produces structured evidence that the future Portfolio Health Framework consumes:
- Per-asset concentration metrics
- Per-asset dependency declarations
- Per-asset correlation contribution
- Per-asset narrative exposure (future, via Narrative Registry)

This is a one-way flow: SAI → Portfolio Health. The Portfolio Health Framework does NOT feed back into SAI.

(See: README_market_organism_principles, Section: Principle 2 — Layers of Abstraction)
(See: README_market_evidence_framework, Section: Evidence_Consumer — "reads evidence to make decisions")

---

## 15. Gap Matrix


The following gaps have been identified during preflight reconnaissance. Each gap represents a missing dependency, undefined interface, or unresolved architectural question that must be addressed during the requirements or design phase.

| Gap ID | Description | Severity | Affected Blocks | Resolution Phase | Deferred? |
|--------|-------------|----------|----------------|-----------------|-----------|
| SAI-GAP-1 | Valuation Framework not yet canonicalized — Valuation Context and Value Trap Guard blocks lack formal valuation methodology backing | HIGH | Valuation Context, Value Trap Guard | Requirements — declare interface contract | YES — SAI defines consumption interface; Valuation Framework defines methodology |
| SAI-GAP-2 | Earnings Intelligence Framework not yet defined — Earnings Quality and Guidance blocks lack formal earnings methodology backing | HIGH | Earnings Quality, Guidance/Estimate Revisions | Requirements — declare interface contract | YES — SAI defines consumption interface; Earnings Intelligence defines methodology |
| SAI-GAP-3 | Peer Group Registry not yet created — Peer Comparison block has no canonical peer group definitions | MEDIUM | Peer Comparison | Requirements — declare interface contract | YES — SAI defines what peer comparison needs; Peer Group Registry provides definitions |
| SAI-GAP-4 | Signal Calculation Framework not yet defined — all signal categories lack formal calculation formulas | MEDIUM | All blocks (signal consumption) | Design — declare signal interface contracts | YES — SAI declares which signals it needs; Signal Calc Framework defines formulas |
| SAI-GAP-5 | Data Ingestion/Normalization Framework not yet defined — raw data pipeline contracts undefined | MEDIUM | All blocks (fact consumption) | Design — declare fact format contracts | YES — SAI declares fact format requirements; Data Ingestion delivers normalized facts |
| SAI-GAP-6 | Portfolio Health Framework not yet defined — Portfolio Fit block cannot reference portfolio-level canonical constructs | HIGH | Portfolio Fit | Requirements — declare output interface | YES — SAI provides portfolio fit input; Portfolio Health Framework consumes it |
| SAI-GAP-7 | KPI-Micro Asset Analysis Sheet not canonicalized — existing analytical practice not formally mapped to SAI blocks | LOW | All blocks (validation) | Requirements — include mapping as acceptance criterion | NO — resolve during requirements phase |
| SAI-GAP-8 | Correlation/Dependency Framework not yet defined — formal correlation methodology undefined | MEDIUM | Benchmark/Sector/Peer Correlation | Requirements — declare interface contract | YES — SAI consumes correlation evidence; dedicated framework defines methodology |
| SAI-GAP-9 | No canonical fact format schema — Market Evidence Framework defines semantics but not wire format | LOW | All blocks (implementation) | Design — declare schema requirements | YES — implementation concern, not definition concern |
| SAI-GAP-10 | Temporal resolution undefined — minimum data frequency for each analysis block not yet specified | MEDIUM | All blocks | Requirements — define temporal requirements per block | NO — resolve during requirements phase |

### Gap Resolution Strategy

- **Deferred gaps** (SAI-GAP-1 through SAI-GAP-6, SAI-GAP-8, SAI-GAP-9): SAI declares interface contracts during its own requirements/design phase. The missing frameworks are responsible for fulfilling those contracts when they are built.
- **Non-deferred gaps** (SAI-GAP-7, SAI-GAP-10): Must be resolved during SAI's own requirements phase. They do not depend on external frameworks.

(See: README_market_evidence_framework, Section: Dependencies — signal_calculation_framework_md, data_ingestion_normalization_framework_md)

---

## 16. Candidate Requirements (Draft IDs Only)

The following candidate requirements are identified during preflight for formal elaboration during the requirements phase. These are preliminary — final requirements will be refined, potentially merged, split, or reordered.

| Req ID | One-Line Description | Priority | Related Blocks |
|--------|---------------------|----------|----------------|
| SAI-REQ-1 | Define the canonical analysis block taxonomy (24 blocks) with stable identifiers | MUST | All |
| SAI-REQ-2 | Define fact consumption contracts per analysis block (which facts each block requires) | MUST | All |
| SAI-REQ-3 | Define signal consumption contracts per analysis block (which signals each block requires) | MUST | All |
| SAI-REQ-4 | Define the provenance chain requirement (every interpretation traces to facts/signals) | MUST | All |
| SAI-REQ-5 | Define the non-scoring constraint (SAI interprets but never scores, ranks, or recommends) | MUST | All |
| SAI-REQ-6 | Define the temporal resolution requirements per analysis block | SHOULD | All |
| SAI-REQ-7 | Define the valuation trap detection boundary and evidence requirements | MUST | Valuation Context, Value Trap Guard |
| SAI-REQ-8 | Define the financial stability assessment boundary and convergence criteria | MUST | Balance Sheet, Credit/Solvency, Hidden Liabilities, Pension |
| SAI-REQ-9 | Define the earnings/operational reality assessment boundary | MUST | Revenue Quality, Demand, Margins, Cashflow, Earnings Quality |
| SAI-REQ-10 | Define the peer/benchmark reality boundary and decomposition requirements | SHOULD | Relative Strength, Correlation, Peer Comparison |
| SAI-REQ-11 | Define the portfolio fit output interface for downstream consumption | SHOULD | Portfolio Fit |
| SAI-REQ-12 | Define the narrative exposure interface contract (future linkage to Narrative Registry) | COULD | Portfolio Fit, all blocks |
| SAI-REQ-13 | Define red flag taxonomy per analysis block with evidence thresholds | SHOULD | All |
| SAI-REQ-14 | Define the additive-only extension mechanism for new analysis blocks | MUST | Architecture |
| SAI-REQ-15 | Define the confidence/completeness indicator per block (evidence sufficiency) | SHOULD | All |

### Requirement Prioritization Notes

- **MUST** requirements define the core architecture — SAI cannot ship without them
- **SHOULD** requirements enhance the framework significantly but can be phased
- **COULD** requirements represent future extensibility — documented now, implemented later
- All requirements must respect the boundary definition (Section 3) and the non-scoring constraint

(See: README_market_evidence_framework, Section: 1. Scope Statement)
(See: README_market_organism_principles, Section: Principle 3 — Additive Architecture)

---

## 17. Verification Gate Proposal

The following verification gates are proposed for the SAI Framework specification lifecycle. Each gate must be explicitly executed (not auto-inferred) per Verification Gate Governance policy.

| Gate ID | Gate Name | Description | Phase | Pass Criteria |
|---------|-----------|-------------|-------|---------------|
| VG-SAI-1 | Requirements Completeness Gate | All 24 analysis blocks have defined fact/signal consumption contracts | Requirements | Every block has ≥1 fact category and ≥1 signal category mapped |
| VG-SAI-2 | Boundary Enforcement Gate | Non-scoring, non-prescriptive constraints verified in all requirement language | Requirements | Zero instances of scoring/recommendation language in requirements |
| VG-SAI-3 | Provenance Chain Gate | Every analysis block output traces to Market Evidence Framework primitives | Design | Provenance chain documented for all 24 blocks |
| VG-SAI-4 | Interface Contract Gate | All deferred framework interfaces have explicit consumption contracts | Design | SAI-GAP-1 through SAI-GAP-6 have formal interface declarations |
| VG-SAI-5 | Taxonomy Stability Gate | Analysis block taxonomy is stable and additive-only extension is proven | Design | Block IDs are frozen; extension mechanism documented |
| VG-SAI-6 | Fact Coverage Gate | All 68+ fact categories are mappable to at least one analysis block | Design | Coverage matrix complete with no orphan facts |
| VG-SAI-7 | Signal Coverage Gate | All 23 signal categories have defined input facts and output blocks | Design | Signal-to-block mapping complete |
| VG-SAI-8 | Red Flag Taxonomy Gate | Red flags per block are evidence-based with defined thresholds | Design | Each block has ≥2 defined red flags with evidence criteria |
| VG-SAI-9 | Temporal Resolution Gate | Minimum data frequency defined per block (SAI-GAP-10 resolved) | Design | All blocks have temporal requirements |
| VG-SAI-10 | Cross-Framework Consistency Gate | SAI terminology consistent with Market Evidence Framework, Narrative Framework v2, Market Organism Principles | Design | Zero terminology conflicts identified |
| VG-SAI-11 | KPI Mapping Validation Gate | Existing KPI-Micro Asset Analysis Sheet maps cleanly to SAI blocks | Requirements | ≥80% of existing KPIs mapped to canonical blocks |
| VG-SAI-12 | Portfolio Fit Interface Gate | Portfolio Fit block output format defined and compatible with future Portfolio Health Framework | Design | Output schema declared with clear consumption contract |

### Gate Execution Rules

Per Verification Gate Governance (mandatory steering):
1. Each gate MUST be explicitly executed — never auto-completed
2. Each gate MUST produce an artifact document with pass/fail evidence
3. Each gate MUST be dispatched as a real task to a subagent
4. Failed gates MUST halt progress and report to user

(See: verification_gate_governance, Section: Core Rule)
(See: verification_gate_governance, Section: Verification Gate Checklist)

---

## 18. Final Recommendation

### Decision: PROCEED to requirements.md

### Justification

1. **Architectural foundations are in place.** The Market Evidence Framework provides the canonical evidence hierarchy (Facts → Signals → Evidence Objects) that SAI will consume. The Narrative Registry provides narrative context. Market Organism Principles provide reasoning guardrails.

2. **Missing frameworks are documented as gaps.** Valuation Framework, Earnings Intelligence Framework, Peer Group Registry, Signal Calculation Framework, Data Ingestion Framework, Correlation/Dependency Framework, and Portfolio Health Framework are all identified with severity, resolution strategy, and deferral status. SAI will declare interface contracts for all deferred dependencies.

3. **Scope is clearly bounded.** SAI is diagnostic/interpretive only. It organizes and interprets asset-level evidence. It does not score, rank, recommend, allocate, or execute. This boundary is enforced at the requirements level (SAI-REQ-5) and verified at VG-SAI-2.

4. **The framework fills a critical architectural layer.** SAI sits between Market Evidence (raw facts/signals) and Portfolio Health (portfolio-level assessment). Without SAI, there is no structured way to organize asset-level evidence into coherent analytical dimensions. The Market Evidence Framework provides the bricks; SAI provides the rooms.

5. **24 analysis blocks are identified and categorized.** The block taxonomy covers Foundation, Operational, Financial Stability, Risk, Earnings, Valuation, Market Position, Outlook, and Portfolio Context dimensions. This provides comprehensive coverage of single-asset analytical practice.

### Risks Acknowledged

| Risk | Mitigation |
|------|-----------|
| Scope creep into scoring | VG-SAI-2 boundary enforcement gate; SAI-REQ-5 non-scoring constraint |
| Over-dependence on missing frameworks | Interface contracts isolate SAI from missing dependencies |
| Taxonomy instability | VG-SAI-5 taxonomy stability gate; additive-only principle |
| Fact/signal proliferation | Minimum viable fact set (68 categories) identified; extension governed |
| Preflight-to-requirements drift | This report serves as canonical reference for requirements phase |

### Next Steps

1. Create `spec/single-asset-intelligence-framework` branch
2. Create `.kiro/specs/single-asset-intelligence-framework/requirements.md`
3. Elaborate SAI-REQ-1 through SAI-REQ-15 into formal acceptance criteria
4. Execute VG-SAI-1 (Requirements Completeness Gate) upon requirements completion
5. Proceed to design.md upon requirements approval

### Cross-References

- (See: README_market_evidence_framework, Section: 1. Scope Statement)
- (See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)
- (See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)
- (See: README_market_evidence_framework, Section: 31. Valuation Trap Boundary)
- (See: README_narrative_framework_v2, Section: Narrative Lifecycle States)
- (See: narrative_registry, Section: REGISTRY ENTRIES — Wave 1 Population)
- (See: README_market_organism_principles, Section: Principle 2 — Layers of Abstraction)
- (See: README_market_organism_principles, Section: Principle 3 — Additive Architecture)
- (See: README_market_organism_principles, Section: Principle 4 — Context over Isolated Data Points)
- (See: README_market_organism_principles, Section: Principle 5 — Reality over Narrative)
- (See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)
- (See: verification_gate_governance, Section: Core Rule)

---

*Report generated: 2026-06-05*
*Authority: ARCH*
