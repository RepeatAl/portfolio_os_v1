# Requirements Document

## Introduction

**Spec**: single-asset-intelligence-framework
**Phase**: Requirements
**Status**: Draft / Requirements Foundation
**Authority**: ARCH
**Source Reference**: `.domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md`

The Single Asset Intelligence (SAI) Framework is the canonical asset-level diagnostic layer between the Market Evidence Framework (facts/signals) and downstream portfolio/reporting layers. It organizes and interprets evidence about individual companies and assets into 24 structured analysis blocks — answering whether an asset is fundamentally stable, financially resilient, fairly valued, operationally sound, and portfolio-appropriate.

SAI is diagnostic and interpretive ONLY. It does not score, rank, recommend, allocate, or execute.

## Scope

SAI defines:
- 24 canonical analysis blocks for single-asset diagnostics
- Fact consumption contracts per block
- Signal consumption contracts per block
- Provenance chain requirements
- Valuation trap guard boundary
- Financial stability boundary
- Earnings/operational reality boundary
- Peer/benchmark reality boundary
- Portfolio fit output interface
- Red flag taxonomy
- Temporal resolution requirements
- Extension mechanism

## Hard Exclusions

The following are explicitly prohibited:
- No implementation code
- No scoring algorithms or numeric scores
- No ranking systems
- No probability models
- No buy/sell/hold recommendations
- No allocation decisions or position sizing
- No price targets or fair value estimates
- No "undervalued" or "overvalued" labels
- No asset-to-narrative mapping creation
- No registry mutation (Narrative Registry, artifact registry)
- No new fact/signal/evidence primitive creation
- No Market Evidence Framework mutation
- No Narrative Framework v2 mutation
- No Market Organism Layer 0 mutation
- No central glossary mutation

## Glossary

Use canonical glossary reference. Local candidates:
- Analysis_Block: A discrete diagnostic dimension organizing evidence about a specific aspect of an asset.
- Fact_Consumption_Contract: Declaration of which fact categories an analysis block requires as input.
- Signal_Consumption_Contract: Declaration of which signal categories an analysis block requires as input.
- Red_Flag: An evidence-based condition within an analysis block that indicates elevated risk requiring attention.

## Requirements

### SAI-REQ-1: Canonical Analysis Block Taxonomy

**Purpose**: Establish the complete, stable set of diagnostic dimensions that organize all asset-level evidence interpretation.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define exactly 24 analysis blocks with stable identifiers, organized into logical categories, each representing a discrete diagnostic dimension for asset-level evidence interpretation.

**In Scope**:
- Definition of all 24 analysis blocks with unique, immutable identifiers
- Category assignment (Foundation, Operational, Financial Stability, Risk, Earnings, Valuation, Market Position, Outlook, Portfolio Context)
- Block naming conventions and identifier format
- Block independence principle (each block functions without requiring other blocks' outputs)
- Block composability (higher layers may consume any combination)

**Out of Scope**:
- Implementation logic for any block
- Scoring or weighting of blocks
- Block prioritization or ordering by importance
- Block-to-block dependency chains

#### Acceptance Criteria

1. Exactly 24 analysis blocks are defined with stable identifiers following the format `SAI-BLK-NN`
2. All blocks are categorized into one of: Foundation, Operational, Financial Stability, Risk, Earnings, Valuation, Market Position, Outlook, Portfolio Context
3. Each block has a unique name, identifier, category, and purpose statement
4. Block independence is explicitly stated — no block requires another block's output to function
5. The complete block taxonomy matches the preflight definition:
   - Asset Identity, Business Model Quality, Revenue Quality, Demand/Pipeline, Margin Quality, Cashflow Quality, Balance Sheet Quality, Credit/Solvency Risk, Hidden Liabilities, Pension Obligations, Working Capital, Customer Concentration, Supply Chain Stability, Pricing Power, Earnings Quality, Guidance/Estimate Revisions, Valuation Context, Value Trap Guard, Relative Strength, Benchmark/Sector/Peer Correlation, Peer Comparison, Company Outlook, Asset-Class Outlook, Portfolio Fit
6. No block produces a numeric score, ranking, or recommendation

**Related Preflight Section**: Section 6
**Verification Gate**: VG-SAI-1

---

### SAI-REQ-2: Fact Consumption Contracts

**Purpose**: Define exactly which fact categories from the Market Evidence Framework each analysis block requires as input, ensuring complete evidence coverage and no orphan blocks.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define explicit fact consumption contracts for each of the 24 analysis blocks, referencing the 68 canonical fact categories defined in the Market Evidence Framework preflight inventory.

**In Scope**:
- Mapping of fact categories to analysis blocks (many-to-many relationship)
- Minimum fact coverage per block (≥1 fact category per block)
- Coverage completeness matrix (all 68 fact categories assigned to at least one block)
- KPI-to-block mapping validation (resolves SAI-GAP-7)
- Fact category domain groupings (Revenue, Demand/Pipeline, Margin, Cashflow, Balance Sheet, Obligations, Working Capital, Concentration, Valuation, Market/Relative)

**Out of Scope**:
- Fact creation or modification (Market Evidence Framework responsibility)
- Data ingestion pipeline definition
- Signal calculation methodology
- Implementation of fact retrieval logic

#### Acceptance Criteria

1. Every analysis block has ≥1 fact category mapped in its consumption contract
2. All 68 fact categories from the preflight inventory are assigned to at least one block
3. Coverage matrix is complete and reviewable (block × fact category)
4. KPI-Micro Asset Analysis Sheet mapping is validated against the fact consumption contracts
5. No fact consumption contract references a fact category not defined in the Market Evidence Framework
6. Fact consumption contracts are declarative only — no retrieval logic or implementation

**Related Preflight Section**: Section 7, Section 8
**Verification Gate**: VG-SAI-2

---

### SAI-REQ-3: Signal Consumption Contracts

**Purpose**: Define exactly which signal categories each analysis block requires, ensuring that calculated signals are consumed within proper analytical context.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define explicit signal consumption contracts for each of the 24 analysis blocks, referencing the 23 canonical signal categories defined in the Market Evidence Framework preflight inventory.

**In Scope**:
- Mapping of signal categories to analysis blocks (many-to-many relationship)
- Minimum signal coverage per block (≥1 signal category per block)
- Signal-to-block assignment rationale
- Coverage completeness matrix (all 23 signal categories assigned)
- Signal interpretation context per block

**Out of Scope**:
- Signal calculation formulas (Signal Calculation Framework responsibility)
- Signal creation or modification
- Signal threshold definitions
- Implementation of signal retrieval or computation

#### Acceptance Criteria

1. Every analysis block has ≥1 signal category mapped in its consumption contract
2. All 23 signal categories from the preflight inventory are assigned to at least one block
3. Signal consumption contracts specify the interpretive context (what the signal means within the block)
4. No signal consumption contract references a signal category not defined in the Market Evidence Framework
5. Signal consumption contracts are declarative only — no calculation logic or implementation

**Related Preflight Section**: Section 9
**Verification Gate**: VG-SAI-3

---

### SAI-REQ-4: Provenance Chain Requirement

**Purpose**: Ensure every SAI interpretation is traceable back to specific evidence, preventing orphan claims and maintaining institutional accountability.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL require every interpretation produced within any analysis block to trace back to specific facts and/or signals with full provenance chain, including source identification, temporal context, and evidence linkage.

**In Scope**:
- Provenance chain specification per analysis block
- Required provenance metadata (source fact/signal ID, timestamp, source type)
- No-orphan-interpretation rule (every interpretation must have evidence backing)
- Timestamp inheritance model (interpretations inherit temporal context from source evidence)
- Provenance validation rules

**Out of Scope**:
- Provenance storage implementation
- Data lineage tooling
- Audit trail implementation
- Fact/signal creation provenance (Market Evidence Framework responsibility)

#### Acceptance Criteria

1. Provenance chain specification documented for all 24 analysis blocks
2. No-orphan-interpretation rule is explicitly stated and enforceable
3. Required provenance metadata schema defined (fact/signal reference, timestamp, source type)
4. Timestamp inheritance model documented (SAI interpretations inherit source evidence temporal context)
5. An interpretation without evidence provenance is explicitly declared invalid
6. Provenance requirements do not create circular dependencies between blocks

**Related Preflight Section**: Section 4
**Verification Gate**: VG-SAI-4

---

### SAI-REQ-5: Non-Scoring / Non-Recommendation Constraint

**Purpose**: Establish the absolute boundary that SAI is diagnostic and interpretive only, preventing scope creep into scoring, ranking, or recommendation territory.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL prohibit the production of numeric scores, rankings, probabilities, buy/sell/hold recommendations, allocation decisions, position sizing, price targets, or fair value estimates within any analysis block or framework output.

**In Scope**:
- Explicit prohibition of: numeric scores, rankings, probabilities, recommendations
- Explicit prohibition of: buy/sell/hold signals, allocation decisions, position sizing
- Explicit prohibition of: price targets, fair value estimates, "undervalued"/"overvalued" labels
- Diagnostic language boundary (what SAI MAY say vs. what it MUST NOT say)
- Valuation context principle: "Low valuation is not automatically undervaluation. A stock is not cheap because it fell. A stock is cheap only if market expectation is below realistic value creation."

**Out of Scope**:
- Defining what a scoring layer would look like (future framework)
- Recommendation engine design
- Decision engine architecture

#### Acceptance Criteria

1. Zero scoring or recommendation language exists in any SAI deliverable
2. Explicit prohibition list is documented and covers all listed categories
3. The valuation context principle is stated verbatim in the Valuation Context block definition
4. Diagnostic language boundary is defined (SAI interprets evidence, it does not prescribe action)
5. The distinction between "interpreting valuation context" and "recommending based on valuation" is clearly articulated
6. Boundary enforcement principle stated: "A company can be operationally excellent and still overvalued. A company can be statistically cheap but structurally impaired."

**Related Preflight Section**: Section 3
**Verification Gate**: VG-SAI-5

---

### SAI-REQ-6: Temporal Resolution Requirements

**Purpose**: Define the minimum data frequency expectations for each analysis block, ensuring temporal appropriateness of evidence consumption.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define minimum data frequency requirements for each of the 24 analysis blocks, specifying whether the block requires quarterly, monthly, daily, or real-time evidence refresh to maintain diagnostic validity.

**In Scope**:
- Temporal resolution assignment per block (quarterly, monthly, daily, real-time)
- Staleness threshold per block (when evidence becomes too old to be valid)
- Temporal resolution rationale (why each block needs its assigned frequency)
- Resolution of SAI-GAP-10 (temporal resolution gap from preflight)

**Out of Scope**:
- Data pipeline scheduling implementation
- Real-time streaming architecture
- Data refresh automation
- Alert/notification systems for stale data

#### Acceptance Criteria

1. All 24 analysis blocks have explicit temporal resolution requirements assigned
2. Each assignment includes rationale (why this frequency is the minimum)
3. Staleness thresholds are defined per block (evidence older than X is flagged)
4. Temporal resolution categories are limited to: quarterly, monthly, daily, real-time
5. Financial filing-dependent blocks (Balance Sheet, Credit/Solvency, etc.) are assigned quarterly minimum
6. Market data-dependent blocks (Relative Strength, Correlation, etc.) are assigned daily minimum
7. SAI-GAP-10 is explicitly resolved by this requirement

**Related Preflight Section**: Section 6, Gap Analysis
**Verification Gate**: VG-SAI-6

---

### SAI-REQ-7: Valuation Context and Value Trap Guard

**Purpose**: Define the multi-dimensional evidence requirements for valuation interpretation, preventing single-metric valuation conclusions and establishing the value trap detection boundary.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL require the Valuation Context block to consume evidence from at least 6 dimensions (cashflow quality, credit/solvency risk, hidden liabilities, earnings quality, company outlook, and peer context) before producing any valuation interpretation, and SHALL prohibit valuation conclusions without solvency evidence.

**In Scope**:
- Multi-dimensional valuation evidence requirements (minimum 6 dimensions)
- Value trap detection criteria (cheap-but-impaired patterns)
- Solvency evidence requirement for valuation interpretation
- Structural vs. cyclical discount distinction
- Valuation context principles:
  - "A company can be operationally excellent and still overvalued."
  - "A company can be statistically cheap but structurally impaired."
  - "Low valuation is not automatically undervaluation."

**Out of Scope**:
- Fair value calculation methodology
- Valuation model selection (DCF, multiples, etc.)
- Price target derivation
- Buy/sell signals based on valuation

#### Acceptance Criteria

1. Valuation Context block requires evidence from ≥6 dimensions before producing interpretation
2. Required dimensions explicitly listed: cashflow, credit/solvency, hidden liabilities, earnings quality, outlook, peer context
3. Value Trap Guard block defined with structural vs. cyclical discount criteria
4. Valuation conclusions without solvency evidence are explicitly prohibited
5. All three valuation context principles are stated in the block definition
6. No "undervalued" or "overvalued" labels are produced — only contextual interpretation

**Related Preflight Section**: Section 6, Section 10
**Verification Gate**: VG-SAI-7

---

### SAI-REQ-8: Financial Stability / Credit-Solvency Boundary

**Purpose**: Define the comprehensive evidence scope for financial stability assessment, covering all dimensions of balance sheet health, credit risk, and hidden obligations.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL cover the following financial stability dimensions within the Credit/Solvency Risk, Balance Sheet Quality, Hidden Liabilities, and Pension Obligations blocks: gross debt, net debt, maturity schedule, short-term debt, available liquidity, interest coverage, net debt/EBITDA, FCF/debt, lease liabilities, purchase obligations, off-balance commitments, pension obligations, pension funding gap, goodwill/intangibles/impairment, LBO history, sponsor overhang, covenant pressure, and bond/CDS/rating evidence.

**In Scope**:
- Gross debt and net debt assessment
- Debt maturity schedule and refinancing risk
- Short-term debt exposure and liquidity coverage
- Interest coverage ratio interpretation
- Leverage ratios (net debt/EBITDA, FCF/debt)
- Lease liabilities (IFRS 16 / ASC 842)
- Non-cancellable purchase obligations
- Off-balance-sheet commitments and guarantees
- Pension obligations and funding gap
- Goodwill, intangibles, and impairment risk
- LBO history and sponsor overhang assessment
- Covenant pressure indicators
- Bond market evidence, CDS spreads, credit ratings
- Credit ratings consumed as inputs, NOT as truth

**Out of Scope**:
- Credit scoring models
- Default probability calculations
- Credit rating assignment
- Bankruptcy prediction models

#### Acceptance Criteria

1. All listed financial stability categories have explicit fact category mappings
2. Credit ratings are documented as "input evidence, not truth" — SAI does not assign or endorse ratings
3. Hidden liabilities block covers: off-balance-sheet, litigation, guarantees, contingencies, goodwill risk
4. Pension obligations block covers: defined benefit obligations, funding gap, plan asset adequacy
5. LBO history and sponsor overhang are addressed within Credit/Solvency Risk
6. Covenant pressure indicators are defined with evidence requirements
7. Each category has at least one red flag example documented

**Related Preflight Section**: Section 6, Section 8
**Verification Gate**: VG-SAI-8

---

### SAI-REQ-9: Earnings and Operational Reality Boundary

**Purpose**: Define the evidence scope for earnings quality and operational assessment, distinguishing real demand from artificial or story-driven metrics.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL cover the following earnings and operational dimensions: earnings quality, revenue quality, guidance, estimate revisions, backlog, book-to-bill, order intake, margin durability, FCF conversion, working capital efficiency, customer concentration, and supply chain capacity, and SHALL distinguish between real demand, pulled-forward demand, and story-only demand.

**In Scope**:
- Earnings quality assessment (accrual quality, one-offs, adjustments, GAAP vs. adjusted gap)
- Revenue quality interpretation (organic growth, recurring vs. transactional, ARR trends)
- Management guidance assessment and revision tracking
- Consensus estimate revision analysis (3-month, 6-month trends)
- Backlog and RPO interpretation
- Book-to-bill ratio diagnostic
- Order intake trajectory analysis
- Margin durability assessment (gross, operating, EBITDA trends)
- FCF conversion quality (OCF to FCF pathway)
- Working capital efficiency (DSO, DPO, inventory days)
- Customer concentration risk assessment
- Supply chain capacity and stability evaluation
- Demand reality distinction: real vs. pulled-forward vs. story-only

**Out of Scope**:
- Earnings forecasting models
- Revenue prediction
- Margin forecasting
- Supply chain optimization

#### Acceptance Criteria

1. All listed earnings/operational categories have explicit fact and signal mappings
2. Demand reality distinction is formally defined with evidence criteria for each category
3. "Story-only demand" is defined (demand narrative without order/backlog evidence)
4. "Pulled-forward demand" is defined (current orders borrowed from future periods)
5. Red flag examples documented for each operational category
6. Earnings quality assessment explicitly addresses GAAP vs. adjusted earnings gap
7. Working capital efficiency criteria include DSO/DPO/inventory days thresholds

**Related Preflight Section**: Section 6, Section 7
**Verification Gate**: VG-SAI-9

---

### SAI-REQ-10: Peer/Benchmark Reality Boundary

**Purpose**: Define the evidence scope for relative market position assessment, determining whether an asset moves by its own fundamental strength or merely by index/sector beta.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL cover the following peer/benchmark dimensions: relative strength vs. benchmark/sector/peers, correlation coefficients, beta decomposition, volatility assessment, and drawdown analysis, and SHALL determine whether price movement reflects asset-specific strength or index/sector beta exposure.

**In Scope**:
- Relative strength vs. primary benchmark (e.g., S&P 500, MSCI World)
- Relative strength vs. sector index
- Relative strength vs. defined peer group
- Correlation coefficient analysis (benchmark, sector, peers)
- Beta decomposition (market beta, sector beta, idiosyncratic component)
- Realized volatility assessment
- Maximum drawdown analysis
- Co-movement pattern detection
- Asset-specific strength vs. beta-driven movement distinction
- Peer group definition requirements (non-canonical until Peer Group Registry exists)

**Out of Scope**:
- Peer group creation or canonicalization (future Peer Group Registry)
- Statistical arbitrage models
- Pairs trading signals
- Momentum scoring or factor models

#### Acceptance Criteria

1. Beta decomposition methodology documented (market, sector, idiosyncratic)
2. Relative strength interpretation defined for all three comparison levels (benchmark, sector, peers)
3. Correlation coefficient interpretation context defined per block
4. Peer comparison explicitly requires a defined peer group — ad-hoc comparisons prohibited
5. Peer groups declared as non-canonical until Peer Group Registry exists
6. "Moves by own strength" vs. "moves by beta" distinction formally articulated
7. Drawdown analysis includes context (market-wide vs. sector-wide vs. asset-specific)

**Related Preflight Section**: Section 6
**Verification Gate**: VG-SAI-10

---

### SAI-REQ-11: Portfolio Fit Output Interface

**Purpose**: Define the structured output that SAI provides to portfolio-level consumers, covering concentration, dependency, and diversification context without crossing into allocation territory.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define a Portfolio Fit output interface covering: concentration contribution, dependency overlap, narrative overlap (future interface), macro sensitivity, liquidity sensitivity, diversification contribution, and fragility contribution, and SHALL NOT include capital weight, target weight, position size, buy/sell signals, or portfolio optimization outputs.

**In Scope**:
- Concentration contribution assessment (how this asset affects portfolio concentration)
- Dependency overlap detection (shared dependencies with other portfolio assets)
- Narrative overlap interface (future — how narrative exposure overlaps with portfolio)
- Macro sensitivity profile (interest rate, inflation, growth, currency exposure)
- Liquidity sensitivity (ADV, bid-ask, market impact potential)
- Diversification contribution context (correlation-based diversification value)
- Fragility contribution assessment (tail risk, drawdown contribution potential)
- Output schema definition (what fields Portfolio Fit produces)

**Out of Scope**:
- Capital weight assignment or recommendation
- Target weight calculation
- Position size determination
- Buy/sell/hold signals
- Portfolio optimization algorithms
- Rebalancing triggers or schedules
- Risk budgeting

#### Acceptance Criteria

1. Portfolio Fit output schema is fully defined with all required fields
2. Zero allocation language exists in the output interface (no weight, size, buy/sell)
3. Concentration contribution is defined in terms of exposure dimensions, not capital percentage
4. Dependency overlap is defined with evidence requirements
5. Narrative overlap is declared as future interface (not implemented in current phase)
6. Macro sensitivity categories are enumerated (rates, inflation, growth, FX)
7. Liquidity sensitivity includes ADV-based liquidity assessment criteria

**Related Preflight Section**: Section 6
**Verification Gate**: VG-SAI-11

---

### SAI-REQ-12: Future Narrative Exposure Interface Contract

**Purpose**: Declare the interface contract for future linkage between SAI and the Narrative Registry, without creating any asset-to-narrative mappings in the current phase.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL declare an explicit interface contract for future narrative exposure linkage to the Narrative Registry, specifying how narrative exposure evidence would be consumed and validated, and SHALL NOT create any Asset-to-Narrative mappings or add entries to the Narrative Registry.

**In Scope**:
- Interface contract declaration (what SAI will need from Narrative Registry)
- Narrative exposure evidence requirements (what evidence is needed to claim exposure)
- Narrative lifecycle state respect (falsified narratives have no forward exposure)
- Canonical narrative_id reference format
- Distinction between sector membership and narrative exposure
- Contract boundary: SAI consumes narrative context, does not create it

**Out of Scope**:
- Asset-to-Narrative mapping creation (Narrative Population Framework responsibility)
- Narrative creation or modification
- Narrative lifecycle management
- Narrative scoring or strength assessment

#### Acceptance Criteria

1. Interface contract is documented with required fields and expected behavior
2. No Asset-to-Narrative mappings are created in any SAI deliverable
3. Narrative exposure requires explicit evidence linking per Market Evidence Framework
4. Narrative lifecycle state is respected (falsified = no forward exposure)
5. Sector membership is explicitly distinguished from narrative exposure
6. The contract references canonical `narrative_id` format from Narrative Registry

**Related Preflight Section**: Section 5
**Verification Gate**: VG-SAI-12

---

### SAI-REQ-13: Red Flag Taxonomy per Analysis Block

**Purpose**: Define evidence-based warning conditions within each analysis block that indicate elevated risk, requiring attention from downstream consumers.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define a minimum of 2 red flags per analysis block, each with explicit evidence thresholds and provenance requirements, covering all 24 canonical analysis blocks.

**In Scope**:
- Red flag definition per block (minimum 2 per block = minimum 48 total)
- Evidence threshold specification for each red flag
- Red flag severity indication (categorical, not scored)
- Red flag evidence provenance requirement (what facts/signals trigger the flag)
- Red flag temporal context (when the condition must persist to be flagged)
- Red flag combination patterns (when multiple flags in different blocks compound risk)

**Out of Scope**:
- Red flag scoring or numeric severity ratings
- Automated alert/notification systems
- Red flag resolution actions or recommendations
- Red flag aggregation into a single risk score

#### Acceptance Criteria

1. Red flag taxonomy covers all 24 analysis blocks with ≥2 red flags each
2. Each red flag has an explicit evidence threshold (what fact/signal condition triggers it)
3. Red flags are categorical (elevated/critical) — no numeric severity scores
4. Red flag provenance is required (which specific evidence triggered the flag)
5. Temporal persistence requirements are defined (transient vs. sustained conditions)
6. Example red flags from preflight Section 7 are incorporated (e.g., book-to-bill < 1.0, leverage > 4x)

**Related Preflight Section**: Section 7
**Verification Gate**: VG-SAI-9

---

### SAI-REQ-14: Additive-Only Extension Mechanism

**Purpose**: Define how the analysis block taxonomy can grow over time without breaking existing blocks, consumers, or provenance chains.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define an additive-only extension mechanism for the analysis block taxonomy, ensuring that new blocks can be added without modifying, removing, or redefining existing blocks, and that existing block identifiers are immutable once defined.

**In Scope**:
- Extension rules for adding new analysis blocks
- Block identifier immutability guarantee (once assigned, never reassigned)
- Category extension rules (new categories may be added)
- Backward compatibility requirements (existing consumers unaffected by new blocks)
- Versioning approach for the block taxonomy
- Extension proposal process (what information is required to add a block)

**Out of Scope**:
- Block removal or deprecation (not permitted in current architecture)
- Block merger or consolidation
- Block identifier reassignment
- Breaking changes to existing block definitions

#### Acceptance Criteria

1. Extension rules are documented with explicit steps for adding a new block
2. Block identifier immutability is explicitly stated (SAI-BLK-NN identifiers never reused)
3. Existing block definitions cannot be modified by extensions (additive-only)
4. New blocks must satisfy the same requirements as existing blocks (fact/signal contracts, red flags, temporal resolution)
5. Backward compatibility guarantee is stated (adding block 25 cannot break blocks 1-24)
6. Extension proposal template defined (required fields for new block proposal)

**Related Preflight Section**: Section 6 (Block Architecture Principles)
**Verification Gate**: VG-SAI-11

---

### SAI-REQ-15: Evidence Sufficiency / Completeness Indicator

**Purpose**: Define a qualitative mechanism for indicating how complete the evidence base is for each analysis block, without introducing numeric scoring.

**Requirement Statement**: THE Single Asset Intelligence Framework SHALL define a qualitative evidence completeness indicator per analysis block using categorical values only (high/medium/low/insufficient), indicating the degree to which available evidence covers the block's fact and signal consumption contracts.

**In Scope**:
- Completeness indicator taxonomy: high, medium, low, insufficient
- Definition of each completeness level per block
- Evidence coverage thresholds for each level (percentage of required facts/signals available)
- Completeness indicator as metadata (not a score, not a recommendation)
- Temporal staleness impact on completeness (stale evidence degrades completeness)

**Out of Scope**:
- Numeric completeness scores (0-100, percentages as outputs)
- Confidence intervals or probability distributions
- Completeness-based recommendations ("insufficient = do not invest")
- Automated completeness-to-action mapping

#### Acceptance Criteria

1. Completeness taxonomy defined with exactly 4 levels: high, medium, low, insufficient
2. Each level has explicit criteria (e.g., high = all required facts/signals available and current)
3. Completeness is categorical only — no numeric conversion permitted
4. Staleness impact documented (stale evidence can downgrade completeness from high to medium/low)
5. Completeness indicator is explicitly NOT a score and NOT a recommendation
6. No action mapping exists (insufficient completeness does not trigger any recommendation)

**Related Preflight Section**: Section 6
**Verification Gate**: VG-SAI-12

---

## Canonical Analysis Blocks

The following table defines the complete taxonomy of 24 analysis blocks with their categories and primary evidence domains.

| # | Block ID | Block Name | Category | Primary Evidence Domain |
|---|----------|-----------|----------|------------------------|
| 1 | SAI-BLK-01 | Asset Identity | Foundation | Corporate filings, sector classification |
| 2 | SAI-BLK-02 | Business Model Quality | Foundation | Revenue mix, customer type, recurring vs. transactional |
| 3 | SAI-BLK-03 | Revenue Quality | Operational | Revenue growth, organic growth, ARR, RPO, backlog |
| 4 | SAI-BLK-04 | Demand / Pipeline | Operational | Order intake, book-to-bill, backlog, pipeline indicators |
| 5 | SAI-BLK-05 | Margin Quality | Operational | Gross margin, operating margin, EBITDA margin, trends |
| 6 | SAI-BLK-06 | Cashflow Quality | Operational | Operating CF, FCF, FCF conversion, capex intensity |
| 7 | SAI-BLK-07 | Balance Sheet Quality | Financial Stability | Cash, debt structure, maturity schedule, leverage ratios |
| 8 | SAI-BLK-08 | Credit / Solvency Risk | Financial Stability | Interest coverage, net debt/EBITDA, FCF/debt, ratings |
| 9 | SAI-BLK-09 | Hidden Liabilities | Financial Stability | Off-balance-sheet, litigation, guarantees, contingencies |
| 10 | SAI-BLK-10 | Pension Obligations | Financial Stability | Pension funding gap, plan status, obligation trajectory |
| 11 | SAI-BLK-11 | Working Capital | Operational | Inventory, DSO, DPO, working capital cycle |
| 12 | SAI-BLK-12 | Customer Concentration | Risk | Revenue concentration, top-customer dependency |
| 13 | SAI-BLK-13 | Supply Chain Stability | Risk | Supplier concentration, geographic risk, capacity constraints |
| 14 | SAI-BLK-14 | Pricing Power | Operational | Cost pass-through ability, competitive moat indicators |
| 15 | SAI-BLK-15 | Earnings Quality | Earnings | Accrual quality, one-offs, adjustments, GAAP vs. adjusted gap |
| 16 | SAI-BLK-16 | Guidance / Estimate Revisions | Earnings | Management guidance, consensus revisions, beat/miss history |
| 17 | SAI-BLK-17 | Valuation Context | Valuation | Multiples, FCF yield, PEG, relative valuation |
| 18 | SAI-BLK-18 | Value Trap Guard | Valuation | Cheap-but-impaired detection, structural vs. cyclical discount |
| 19 | SAI-BLK-19 | Relative Strength | Market Position | Price momentum vs. benchmark, sector, peers |
| 20 | SAI-BLK-20 | Benchmark / Sector / Peer Correlation | Market Position | Beta, correlation coefficients, co-movement patterns |
| 21 | SAI-BLK-21 | Peer Comparison | Market Position | Operational/financial comparison to defined peer group |
| 22 | SAI-BLK-22 | Company Outlook | Outlook | Forward guidance, strategic direction, management credibility |
| 23 | SAI-BLK-23 | Asset-Class Outlook | Outlook | Sector/industry outlook, structural trends, regulatory trajectory |
| 24 | SAI-BLK-24 | Portfolio Fit | Portfolio Context | Concentration, dependency overlap, narrative overlap, diversification |

---

## Deferred Interface Contracts

The following frameworks are not yet canonicalized. SAI declares what it needs from each without depending on their existence for current-phase work.

| # | Deferred Framework | Expected Artifact | What SAI Needs | Impacted Blocks | Priority |
|---|-------------------|-------------------|----------------|-----------------|----------|
| 1 | Valuation Framework | `valuation_framework_md` | Canonical valuation methodology definitions, fair value boundary rules | SAI-BLK-17, SAI-BLK-18 | HIGH |
| 2 | Earnings Intelligence Framework | `earnings_intelligence_framework_md` | Earnings quality calculation rules, estimate revision taxonomy | SAI-BLK-15, SAI-BLK-16 | HIGH |
| 3 | Peer Group Registry | `peer_group_registry_yaml` | Canonical peer group definitions per asset | SAI-BLK-21 | MEDIUM |
| 4 | Portfolio Health Framework | `portfolio_health_framework_md` | Portfolio-level construct definitions for fit assessment | SAI-BLK-24 | HIGH |
| 5 | Correlation/Dependency Framework | `correlation_dependency_framework_md` | Correlation calculation methodology, dependency detection rules | SAI-BLK-20 | MEDIUM |
| 6 | Signal Calculation Framework | `signal_calculation_framework_md` | Signal derivation formulas and calculation rules | All blocks (signal consumption) | MEDIUM |
| 7 | Data Ingestion/Normalization Framework | `data_ingestion_normalization_framework_md` | Normalized fact delivery contracts | All blocks (fact consumption) | MEDIUM |

---

## Non-Deferred Gap Resolutions

The following gaps identified in the preflight are resolved within this requirements document:

| Gap ID | Gap Description | Resolution | Resolved By |
|--------|----------------|------------|-------------|
| SAI-GAP-7 | KPI-Micro Asset Analysis Sheet mapping not formalized | KPI mapping acceptance criterion added — fact consumption contracts must validate against KPI-Micro sheet | SAI-REQ-2, Acceptance Criterion 4 |
| SAI-GAP-10 | Temporal resolution undefined for analysis blocks | Temporal resolution requirements defined for all 24 blocks with quarterly/monthly/daily/real-time categories | SAI-REQ-6 |

---

## Verification Gates

Gates must be explicitly executed and must not be auto-completed.

| Gate ID | Gate Description | Requirements Covered | Pass Criteria |
|---------|-----------------|---------------------|---------------|
| VG-SAI-1 | Block Taxonomy Completeness | SAI-REQ-1 | All 24 blocks defined with stable IDs, categories, and purpose statements |
| VG-SAI-2 | Fact Consumption Coverage | SAI-REQ-2 | Coverage matrix complete; all 68 fact categories assigned; all blocks have ≥1 fact |
| VG-SAI-3 | Signal Consumption Coverage | SAI-REQ-3 | Coverage matrix complete; all 23 signal categories assigned; all blocks have ≥1 signal |
| VG-SAI-4 | Provenance Chain Integrity | SAI-REQ-4 | Provenance specification exists for all 24 blocks; no orphan interpretation paths |
| VG-SAI-5 | Non-Scoring Constraint | SAI-REQ-5 | Zero scoring/recommendation/allocation language in any deliverable |
| VG-SAI-6 | Temporal Resolution Assignment | SAI-REQ-6 | All 24 blocks have assigned temporal resolution with rationale |
| VG-SAI-7 | Valuation Guard Completeness | SAI-REQ-7 | Valuation block requires ≥6 evidence dimensions; solvency requirement documented |
| VG-SAI-8 | Financial Stability Coverage | SAI-REQ-8 | All listed financial categories have fact mappings; credit ratings as input documented |
| VG-SAI-9 | Earnings/Operational Coverage | SAI-REQ-9, SAI-REQ-13 | All categories covered; demand reality distinction defined; red flags documented |
| VG-SAI-10 | Peer/Benchmark Coverage | SAI-REQ-10 | Beta decomposition documented; peer comparison requires defined group |
| VG-SAI-11 | Portfolio Fit Interface + Extension | SAI-REQ-11, SAI-REQ-14 | Output schema defined; no allocation language; extension rules documented |
| VG-SAI-12 | Narrative Interface + Completeness | SAI-REQ-12, SAI-REQ-15 | Interface contract documented; completeness taxonomy defined; no mappings created |

---

## Cross-References

(See: README_market_evidence_framework, Section: 1. Scope Statement)
(See: README_market_evidence_framework, Section: 2. Glossary Reference)
(See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)
(See: README_market_evidence_framework, Section: Layer 1: Observed Facts — Properties)
(See: README_market_evidence_framework, Section: Layer 1: What is NOT an Observed Fact)
(See: README_market_evidence_framework, Section: Layer 2: Calculated_Signal)
(See: README_market_organism_principles, Section: Principle 2 — Layers of Abstraction)
(See: README_market_organism_principles, Section: Principle 3 — Additive Architecture)
(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)
(See: README_narrative_framework_v2, Section: Narrative Lifecycle States)
(See: narrative_registry, Section: REGISTRY ENTRIES — Wave 1 Population)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 2. Source Inventory)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 3. Boundary Definition)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 4. Relationship to Market Evidence Framework)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 5. Relationship to Narrative Registry)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 6. Core Analysis Blocks)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 7. Micro KPI Mapping)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 8. Required Fact Categories)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 9. Required Signal Categories)
(See: shared_glossary_reference, Section: Canonical Terms)
