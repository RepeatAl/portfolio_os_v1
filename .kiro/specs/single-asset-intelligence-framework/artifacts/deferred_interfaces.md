# Single Asset Intelligence Framework — Deferred Interface Contracts

**Artifact**: deferred_interfaces.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 8.1 Create deferred interface contracts
**Requirements**: SAI-REQ-11 (Portfolio Fit Output Interface), SAI-REQ-12 (Future Narrative Exposure Interface Contract), SAI-REQ-14 (Additive-Only Extension Mechanism)
**Verification Gate**: VG-SAI-4 (Interface Contract Gate)
**Status**: Draft

---

## 1. Purpose and Scope

This artifact declares explicit interface contracts for all external frameworks that SAI depends on but does NOT define, implement, or own. Each contract specifies:

- What SAI expects to consume from the external framework
- What SAI may emit that the external framework could consume
- What SAI must NOT define (explicit boundary)
- What happens when the external framework is unavailable (current limitation)
- Which SAI blocks are affected by the dependency

**This artifact is a declaration, not an implementation.** SAI declares its interface expectations. SAI does NOT build, design, implement, or architect any of the seven deferred frameworks listed below.

**Scope boundary**: This document contains zero implementation code, zero calculation formulas, zero scoring logic, zero methodology definitions, zero database schemas, zero API designs, zero ETL pipelines, zero runtime validators, zero parsers, zero services, zero registry mutations, zero fact/signal creation, and zero asset/narrative mappings.

(See: design.md, Section: Deferred Interface Design)
(See: requirements.md, Section: SAI-REQ-14 — Additive-Only Extension Mechanism)

---

## 2. Interface Contract Definitions

### 2.1 Valuation Framework

#### What SAI Expects to Consume

SAI expects the Valuation Framework to provide:

- Canonical valuation methodology definitions (which multiples are primary per sector/asset type)
- Negative earnings handling rules (how to value companies with negative EPS, negative EBITDA)
- Sector-appropriate valuation approach selection (growth vs. value, asset-heavy vs. asset-light)
- Fair value methodology parameters (DCF discount rates, terminal growth assumptions — as methodology context, NOT as calculated fair values)
- Valuation regime classification (expansion, compression, mean-reversion phases)
- Historical multiple context windows (5-year, 10-year, sector median parameters)

SAI consumes these definitions to contextualize valuation facts observed in the Market Evidence Framework. SAI interprets multiples within methodology context — it does not calculate fair value.

#### What SAI May Emit

SAI may emit outputs that the Valuation Framework could consume:

- Current observed valuation multiples (P/E, EV/EBITDA, P/FCF, P/B, dividend yield) with provenance
- Valuation trajectory observations (compression/expansion direction, magnitude)
- Evidence completeness assessment for valuation interpretation
- Red flag conditions related to valuation anomalies (e.g., value trap indicators)
- Temporal staleness metadata for valuation facts

#### What SAI Must NOT Define

- Fair value calculation methodology or formulas
- Target price derivation
- Discount rate selection rules
- Terminal value assumptions
- Valuation model selection (DCF vs. multiples vs. asset-based)
- "Undervalued" / "overvalued" / "fairly valued" labels
- Expected return estimates
- Probability of revaluation
- Buy/sell/hold implications based on valuation

#### Current Limitation

When the Valuation Framework is unavailable, SAI-BLK-17 (Valuation Context) and SAI-BLK-18 (Value Trap Guard) operate with raw multiple observation only. Interpretation is limited to factual multiple reporting without canonical methodology context. The deferred_dependency_notes field states: "Valuation Framework not yet available — interpretation limited to raw multiple observation without canonical methodology context."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-17 | Valuation Context | Primary dependency — methodology context unavailable |
| SAI-BLK-18 | Value Trap Guard | Primary dependency — structural vs. cyclical discount rules unavailable |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Valuation Framework. SAI does NOT build, design, implement, or architect the Valuation Framework. The Valuation Framework is a separate, independent framework with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Valuation Framework may evolve independently. SAI will consume whatever interface the Valuation Framework eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Valuation Framework's internal design decisions.


---

### 2.2 Earnings Intelligence Framework

#### What SAI Expects to Consume

SAI expects the Earnings Intelligence Framework to provide:

- Earnings quality calculation rules (accrual ratio computation methodology)
- Accrual ratio thresholds (what constitutes high/normal/low accrual quality)
- Non-recurring item classification rules (which items qualify as non-recurring, one-off, or extraordinary)
- Earnings manipulation detection heuristics (Beneish M-Score components, Sloan ratio methodology)
- GAAP vs. adjusted earnings gap interpretation rules (what magnitude of adjustment gap is concerning)
- Earnings persistence model parameters (how to assess sustainability of current earnings run-rate)
- Beat/miss pattern significance thresholds (when a beat/miss pattern becomes diagnostic)

SAI consumes these rules to interpret earnings facts within the Earnings Quality and Guidance/Estimate Revisions blocks. SAI does NOT score earnings quality.

#### What SAI May Emit

SAI may emit outputs that the Earnings Intelligence Framework could consume:

- Observed earnings composition facts (EPS breakdown, recurring vs. one-time, GAAP vs. adjusted)
- Accrual ratio observations from financial statements with provenance
- Guidance revision trajectory observations (direction, magnitude, frequency)
- Evidence completeness assessment for earnings interpretation
- Red flag conditions related to earnings anomalies (e.g., persistent accrual divergence)
- Temporal freshness metadata for earnings data

#### What SAI Must NOT Define

- Accrual ratio calculation formulas
- Earnings quality scoring methodology
- Manipulation detection algorithms
- Earnings forecast models
- Earnings surprise prediction
- Consensus estimate generation
- Earnings momentum scoring
- Any numeric "quality score" for earnings

#### Current Limitation

When the Earnings Intelligence Framework is unavailable, SAI-BLK-15 (Earnings Quality) and SAI-BLK-16 (Guidance/Estimate Revisions) operate with raw earnings fact observation only. Interpretation is limited to factual earnings composition reporting without canonical quality assessment rules. The deferred_dependency_notes field states: "Earnings Intelligence Framework not yet available — interpretation limited to raw earnings observation without canonical quality calculation rules."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-15 | Earnings Quality | Primary dependency — quality calculation rules unavailable |
| SAI-BLK-16 | Guidance/Estimate Revisions | Secondary dependency — revision significance thresholds unavailable |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Earnings Intelligence Framework. SAI does NOT build, design, implement, or architect the Earnings Intelligence Framework. The Earnings Intelligence Framework is a separate, independent framework with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Earnings Intelligence Framework may evolve independently. SAI will consume whatever interface the Earnings Intelligence Framework eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Earnings Intelligence Framework's internal design decisions.

---

### 2.3 Peer Group Registry

#### What SAI Expects to Consume

SAI expects the Peer Group Registry to provide:

- Canonical peer group definitions per asset (which companies constitute valid peers for a given asset)
- Peer selection methodology (criteria used to determine peer group membership)
- Peer rotation rules (when and why peers are added/removed from a group)
- Peer group versioning (temporal tracking of peer group composition changes)
- Peer group validity metadata (confidence in peer group appropriateness, staleness indicators)
- Multi-level peer classification (primary peers, secondary peers, aspirational peers)

SAI consumes these definitions for peer comparison context within the Peer Comparison block. SAI does NOT define peer groups or peer selection criteria.

#### What SAI May Emit

SAI may emit outputs that the Peer Group Registry could consume:

- Peer-relative financial metric observations (margin differentials, growth differentials, valuation differentials)
- Competitive position interpretation based on consumed peer definitions
- Evidence completeness assessment for peer comparison interpretation
- Red flag conditions related to peer positioning (e.g., persistent underperformance vs. all peers)
- Temporal freshness metadata for peer comparison data

#### What SAI Must NOT Define

- Peer selection criteria or algorithms
- Peer group composition decisions
- Peer rotation triggers or rules
- Peer group creation methodology
- Peer ranking or scoring
- "Best-in-class" or "worst-in-class" labels
- Peer group consensus definitions
- Statistical peer clustering algorithms

#### Current Limitation

When the Peer Group Registry is unavailable, SAI-BLK-21 (Peer Comparison) operates without canonical peer definitions. Peer comparison interpretation is blocked until a canonical peer group is provided. The deferred_dependency_notes field states: "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-21 | Peer Comparison | Primary dependency — canonical peer definitions unavailable; block output severely limited |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Peer Group Registry. SAI does NOT build, design, implement, or architect the Peer Group Registry. The Peer Group Registry is a separate, independent registry with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Peer Group Registry may evolve independently. SAI will consume whatever interface the Peer Group Registry eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Peer Group Registry's internal design decisions.


---

### 2.4 Portfolio Health Framework

#### What SAI Expects to Consume

SAI expects the Portfolio Health Framework to provide:

- Concentration measurement definitions (how portfolio concentration is calculated — HHI, top-N weight, sector concentration)
- Overlap classification rules (what constitutes dependency overlap, narrative overlap, factor overlap)
- Sensitivity metric definitions (macro sensitivity, liquidity sensitivity, fragility contribution methodology)
- Diversification contribution methodology (how an individual asset's diversification value is assessed within portfolio context)
- Portfolio-level threshold definitions (at what point concentration becomes "elevated," overlap becomes "material")
- Correlation-based portfolio risk parameters (how pairwise/group correlations inform portfolio-level constructs)

SAI consumes these definitions for portfolio fit interpretation within the Portfolio Fit block. SAI does NOT allocate, rebalance, or size positions.

#### What SAI May Emit

SAI may emit outputs that the Portfolio Health Framework could consume:

- Individual asset concentration contribution observations (exposure dimensions, not capital percentages)
- Dependency overlap indicators (shared supply chains, shared customers, shared factor exposures)
- Macro sensitivity profile per asset (interest rate, inflation, growth, currency exposure observations)
- Liquidity sensitivity observations (ADV, bid-ask spread, market impact potential)
- Correlation context per asset (benchmark, sector, peer correlation observations)
- Evidence completeness assessment for portfolio fit interpretation

#### What SAI Must NOT Define

- Capital allocation methodology
- Target weight calculation
- Position sizing rules
- Rebalancing triggers or schedules
- Portfolio optimization algorithms
- Risk budgeting methodology
- Overweight/underweight/neutral labels
- Portfolio score or portfolio health score
- Buy/sell signals based on portfolio context
- Trade execution rules

#### Current Limitation

When the Portfolio Health Framework is unavailable, SAI-BLK-24 (Portfolio Fit) operates with raw exposure observation only. Interpretation is limited to factual exposure reporting without canonical concentration/overlap/sensitivity methodology. The deferred_dependency_notes field states: "Portfolio Health Framework not yet available — interpretation limited to raw exposure observation without canonical portfolio construct definitions."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-24 | Portfolio Fit | Primary dependency — portfolio construct definitions unavailable |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Portfolio Health Framework. SAI does NOT build, design, implement, or architect the Portfolio Health Framework. The Portfolio Health Framework is a separate, independent framework with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Portfolio Health Framework may evolve independently. SAI will consume whatever interface the Portfolio Health Framework eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Portfolio Health Framework's internal design decisions.

---

### 2.5 Correlation/Dependency Framework

#### What SAI Expects to Consume

SAI expects the Correlation/Dependency Framework to provide:

- Correlation calculation methodology (Pearson, Spearman, rolling window specifications)
- Rolling window parameters (lookback period, minimum observation count, weighting scheme)
- Regime detection rules (how to identify correlation regime shifts — trending, mean-reverting, breakdown)
- Beta decomposition approach (market beta, sector beta, idiosyncratic component isolation methodology)
- Correlation significance thresholds (when correlation is statistically meaningful vs. noise)
- Correlation stability assessment methodology (how to distinguish stable correlations from spurious ones)

SAI consumes these definitions for correlation interpretation within the Benchmark/Sector/Peer Correlation block. SAI does NOT calculate correlations.

#### What SAI May Emit

SAI may emit outputs that the Correlation/Dependency Framework could consume:

- Observed correlation regime context (whether asset is in a high-correlation or low-correlation regime)
- Beta decomposition interpretation (how much movement is market-driven vs. asset-specific)
- Evidence completeness assessment for correlation interpretation
- Red flag conditions related to correlation anomalies (e.g., sudden correlation breakdown)
- Temporal freshness metadata for correlation data
- Correlation context per block (how correlation affects other SAI block interpretations)

#### What SAI Must NOT Define

- Correlation calculation formulas
- Rolling window parameter selection rules
- Beta estimation methodology
- Factor model definitions
- Statistical significance testing methodology
- Regime detection algorithms
- Correlation forecasting or prediction
- Pairs trading signals based on correlation
- Statistical arbitrage models

#### Current Limitation

When the Correlation/Dependency Framework is unavailable, SAI-BLK-20 (Benchmark/Sector/Peer Correlation) operates with raw correlation coefficient observation only. Interpretation is limited to factual correlation reporting without canonical methodology context for regime detection or beta decomposition. The deferred_dependency_notes field states: "Correlation/Dependency Framework not yet available — interpretation limited to raw correlation observation without canonical calculation methodology or regime detection rules."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Primary dependency — calculation methodology and regime detection unavailable |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Correlation/Dependency Framework. SAI does NOT build, design, implement, or architect the Correlation/Dependency Framework. The Correlation/Dependency Framework is a separate, independent framework with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Correlation/Dependency Framework may evolve independently. SAI will consume whatever interface the Correlation/Dependency Framework eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Correlation/Dependency Framework's internal design decisions.


---

### 2.6 Signal Calculation Framework

#### What SAI Expects to Consume

SAI expects the Signal Calculation Framework to provide:

- Signal derivation formulas (how each of the 23 canonical signal categories is calculated from underlying facts)
- Signal threshold definitions (what values constitute high/medium/low signal strength)
- Signal normalization rules (how signals are normalized for cross-asset comparability)
- Signal temporal alignment rules (how signals from different time periods are aligned)
- Signal confidence metadata (data quality indicators for each calculated signal)
- Signal update cadence (how frequently each signal is recalculated)
- Signal dependency chains (which facts are required as inputs for each signal)

SAI consumes calculated signals as finished products. SAI does NOT implement signal calculation logic.

#### What SAI May Emit

SAI may emit outputs that the Signal Calculation Framework could consume:

- Signal consumption validation feedback (which signals were consumed, which were missing/stale)
- Evidence completeness observations per signal category (whether required signals were available)
- Temporal staleness observations for consumed signals
- Signal interpretation context (how SAI used each signal within its diagnostic framework)
- Red flag conditions triggered by signal anomalies

#### What SAI Must NOT Define

- Signal calculation formulas or algorithms
- Signal threshold derivation methodology
- Signal normalization procedures
- Signal backtesting methodology
- Signal optimization or tuning
- Signal creation (new signal categories)
- Signal mutation (modification of existing signals)
- Signal scoring or signal strength ratings
- Signal-based trading rules
- Signal aggregation into composite indicators

#### Current Limitation

When the Signal Calculation Framework is unavailable, ALL SAI blocks operate with reduced signal context. Blocks that have fact-only evidence can still produce interpretations (with reduced completeness), but signal-dependent interpretations are limited. The deferred_dependency_notes field states: "Signal Calculation Framework not yet available — signal-dependent interpretations limited; fact-based interpretation preserved where possible."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-01 | Asset Identity | Signal consumption reduced — classification signals unavailable |
| SAI-BLK-02 | Business Model Quality | Signal consumption reduced — durability signals unavailable |
| SAI-BLK-03 | Revenue Quality | Signal consumption reduced — growth/concentration signals unavailable |
| SAI-BLK-04 | Demand/Pipeline | Signal consumption reduced — momentum signals unavailable |
| SAI-BLK-05 | Margin Quality | Signal consumption reduced — leverage signals unavailable |
| SAI-BLK-06 | Cashflow Quality | Signal consumption reduced — conversion signals unavailable |
| SAI-BLK-07 | Balance Sheet Quality | Signal consumption reduced — leverage signals unavailable |
| SAI-BLK-08 | Credit/Solvency Risk | Signal consumption reduced — deterioration signals unavailable |
| SAI-BLK-09 | Hidden Liabilities | Signal consumption reduced — obligation signals unavailable |
| SAI-BLK-10 | Pension Obligations | Signal consumption reduced — underfunding signals unavailable |
| SAI-BLK-11 | Working Capital | Signal consumption reduced — efficiency signals unavailable |
| SAI-BLK-12 | Customer Concentration | Signal consumption reduced — concentration signals unavailable |
| SAI-BLK-13 | Supply Chain Stability | Signal consumption reduced — disruption signals unavailable |
| SAI-BLK-14 | Pricing Power | Signal consumption reduced — pricing signals unavailable |
| SAI-BLK-15 | Earnings Quality | Signal consumption reduced — quality signals unavailable |
| SAI-BLK-16 | Guidance/Estimate Revisions | Signal consumption reduced — revision signals unavailable |
| SAI-BLK-17 | Valuation Context | Signal consumption reduced — multiple trajectory signals unavailable |
| SAI-BLK-18 | Value Trap Guard | Signal consumption reduced — deterioration signals unavailable |
| SAI-BLK-19 | Relative Strength | Signal consumption reduced — momentum signals unavailable |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Signal consumption reduced — regime signals unavailable |
| SAI-BLK-21 | Peer Comparison | Signal consumption reduced — comparison signals unavailable |
| SAI-BLK-22 | Company Outlook | Signal consumption reduced — forward signals unavailable |
| SAI-BLK-23 | Asset-Class Outlook | Signal consumption reduced — sector signals unavailable |
| SAI-BLK-24 | Portfolio Fit | Signal consumption reduced — concentration/diversification signals unavailable |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Signal Calculation Framework. SAI does NOT build, design, implement, or architect the Signal Calculation Framework. The Signal Calculation Framework is a separate, independent framework with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Signal Calculation Framework may evolve independently. SAI will consume whatever interface the Signal Calculation Framework eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Signal Calculation Framework's internal design decisions.

---

### 2.7 Data Ingestion/Normalization Framework

#### What SAI Expects to Consume

SAI expects the Data Ingestion/Normalization Framework to provide:

- Normalized fact objects (standardized structure regardless of original data source)
- Provenance metadata per fact (source identification, retrieval timestamp, source authority level)
- Temporal alignment (all facts aligned to a canonical temporal reference — fiscal quarter, calendar date, observation timestamp)
- Currency normalization (all monetary values expressed in a canonical currency or with explicit conversion metadata)
- Unit standardization (consistent units across all fact categories — percentages, ratios, absolute values)
- Data quality indicators (completeness, reliability, recency per fact)
- Source lineage (full chain from raw data source through normalization to delivered fact)

SAI consumes normalized facts as finished products. SAI does NOT implement data retrieval, parsing, normalization, or enrichment logic.

#### What SAI May Emit

SAI may emit outputs that the Data Ingestion/Normalization Framework could consume:

- Fact consumption confirmation (which facts were successfully consumed by SAI)
- Missing fact reports (which expected facts were not delivered for a given asset/period)
- Fact quality feedback (facts that appeared malformed, inconsistent, or implausible)
- Temporal staleness observations (facts that exceeded staleness thresholds)
- Evidence completeness gaps (systematic missing data patterns across assets)

#### What SAI Must NOT Define

- Data source selection or prioritization
- Data retrieval implementation (APIs, scrapers, feeds)
- Data parsing logic (HTML, PDF, XBRL, JSON parsing)
- Data normalization algorithms
- Currency conversion methodology
- Temporal alignment algorithms
- Data deduplication logic
- Data enrichment pipelines
- ETL pipeline architecture
- Database schema design
- Data warehouse structure
- Data quality scoring methodology

#### Current Limitation

When the Data Ingestion/Normalization Framework is unavailable, ALL SAI blocks operate without guaranteed fact delivery. SAI cannot interpret evidence that has not been delivered. The deferred_dependency_notes field states: "Data Ingestion/Normalization Framework not yet available — fact delivery not guaranteed; SAI interpretation depends on external fact provisioning."

#### Affected SAI Blocks

| Block ID | Block Name | Impact |
|----------|-----------|--------|
| SAI-BLK-01 | Asset Identity | Fact consumption dependent — identity facts require normalization |
| SAI-BLK-02 | Business Model Quality | Fact consumption dependent — business model facts require normalization |
| SAI-BLK-03 | Revenue Quality | Fact consumption dependent — revenue facts require normalization |
| SAI-BLK-04 | Demand/Pipeline | Fact consumption dependent — demand facts require normalization |
| SAI-BLK-05 | Margin Quality | Fact consumption dependent — margin facts require normalization |
| SAI-BLK-06 | Cashflow Quality | Fact consumption dependent — cashflow facts require normalization |
| SAI-BLK-07 | Balance Sheet Quality | Fact consumption dependent — balance sheet facts require normalization |
| SAI-BLK-08 | Credit/Solvency Risk | Fact consumption dependent — credit facts require normalization |
| SAI-BLK-09 | Hidden Liabilities | Fact consumption dependent — liability facts require normalization |
| SAI-BLK-10 | Pension Obligations | Fact consumption dependent — pension facts require normalization |
| SAI-BLK-11 | Working Capital | Fact consumption dependent — working capital facts require normalization |
| SAI-BLK-12 | Customer Concentration | Fact consumption dependent — concentration facts require normalization |
| SAI-BLK-13 | Supply Chain Stability | Fact consumption dependent — supply chain facts require normalization |
| SAI-BLK-14 | Pricing Power | Fact consumption dependent — pricing facts require normalization |
| SAI-BLK-15 | Earnings Quality | Fact consumption dependent — earnings facts require normalization |
| SAI-BLK-16 | Guidance/Estimate Revisions | Fact consumption dependent — guidance facts require normalization |
| SAI-BLK-17 | Valuation Context | Fact consumption dependent — valuation facts require normalization |
| SAI-BLK-18 | Value Trap Guard | Fact consumption dependent — multi-dimensional facts require normalization |
| SAI-BLK-19 | Relative Strength | Fact consumption dependent — price/performance facts require normalization |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Fact consumption dependent — correlation facts require normalization |
| SAI-BLK-21 | Peer Comparison | Fact consumption dependent — peer financial facts require normalization |
| SAI-BLK-22 | Company Outlook | Fact consumption dependent — outlook facts require normalization |
| SAI-BLK-23 | Asset-Class Outlook | Fact consumption dependent — sector/macro facts require normalization |
| SAI-BLK-24 | Portfolio Fit | Fact consumption dependent — portfolio facts require normalization |

#### No-Framework-Invention Statement

SAI declares the interface expectation for the Data Ingestion/Normalization Framework. SAI does NOT build, design, implement, or architect the Data Ingestion/Normalization Framework. The Data Ingestion/Normalization Framework is a separate, independent framework with its own authority, lifecycle, and ownership.

#### Governance Boundary Statement

This contract is a declaration of interface expectations, not an implementation commitment. The Data Ingestion/Normalization Framework may evolve independently. SAI will consume whatever interface the Data Ingestion/Normalization Framework eventually provides, provided it satisfies the expectations declared above. SAI has no authority over the Data Ingestion/Normalization Framework's internal design decisions.


---

## 3. Deferred Dependency Summary Table

| # | Framework | SAI Consumes | SAI Emits | SAI Must NOT Define | Blocks Affected |
|---|-----------|-------------|-----------|--------------------:|-----------------|
| 1 | Valuation Framework | Methodology definitions, sector approaches, regime classification | Observed multiples, trajectory, red flags | Fair value, target price, undervalued/overvalued labels | SAI-BLK-17, SAI-BLK-18 |
| 2 | Earnings Intelligence Framework | Quality calculation rules, thresholds, manipulation heuristics | Earnings composition observations, accrual observations | Quality scores, manipulation algorithms, forecast models | SAI-BLK-15, SAI-BLK-16 |
| 3 | Peer Group Registry | Canonical peer definitions, selection methodology, rotation rules | Peer-relative observations, competitive position context | Peer selection criteria, peer group composition, peer ranking | SAI-BLK-21 |
| 4 | Portfolio Health Framework | Concentration measurement, overlap rules, sensitivity definitions | Exposure observations, dependency overlap, macro sensitivity | Allocation, position sizing, rebalancing, target weights | SAI-BLK-24 |
| 5 | Correlation/Dependency Framework | Calculation methodology, window parameters, regime detection | Regime context, beta interpretation, correlation anomalies | Correlation formulas, factor models, statistical testing | SAI-BLK-20 |
| 6 | Signal Calculation Framework | Signal derivation formulas, thresholds, normalization rules | Consumption validation, completeness observations | Signal formulas, signal creation, signal optimization | All 24 blocks |
| 7 | Data Ingestion/Normalization Framework | Normalized facts, provenance metadata, temporal alignment | Consumption confirmation, missing fact reports, quality feedback | ETL pipelines, parsers, data sources, database schemas | All 24 blocks |

---

## 4. Affected Block Mapping Table

| Block ID | Block Name | Deferred Dependencies |
|----------|-----------|----------------------|
| SAI-BLK-01 | Asset Identity | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-02 | Business Model Quality | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-03 | Revenue Quality | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-04 | Demand/Pipeline | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-05 | Margin Quality | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-06 | Cashflow Quality | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-07 | Balance Sheet Quality | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-08 | Credit/Solvency Risk | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-09 | Hidden Liabilities | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-10 | Pension Obligations | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-11 | Working Capital | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-12 | Customer Concentration | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-13 | Supply Chain Stability | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-14 | Pricing Power | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-15 | Earnings Quality | Earnings Intelligence Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-16 | Guidance/Estimate Revisions | Earnings Intelligence Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-17 | Valuation Context | Valuation Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-18 | Value Trap Guard | Valuation Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-19 | Relative Strength | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Correlation/Dependency Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-21 | Peer Comparison | Peer Group Registry, Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-22 | Company Outlook | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-23 | Asset-Class Outlook | Signal Calculation Framework, Data Ingestion/Normalization Framework |
| SAI-BLK-24 | Portfolio Fit | Portfolio Health Framework, Signal Calculation Framework, Data Ingestion/Normalization Framework |

---

## 5. Unavailable-Framework Behavior

When a deferred framework is unavailable, SAI blocks behave as follows:

### 5.1 Graceful Degradation Principle

SAI blocks do NOT fail silently when a deferred dependency is unavailable. Instead, they:

1. **Continue operating** with whatever evidence IS available (facts from other sources, raw observations)
2. **Explicitly document** the limitation in the `deferred_dependency_notes` field of the output object
3. **Reduce evidence completeness** assessment to reflect the gap (typically "low" or "insufficient")
4. **Do NOT invent** methodology to fill the gap — no approximation, no substitution, no assumption
5. **Do NOT suppress** the block output — the limitation itself is diagnostic information

### 5.2 Per-Framework Unavailability Behavior

| Framework | Unavailable Behavior | Evidence Completeness Impact |
|-----------|---------------------|------------------------------|
| Valuation Framework | Raw multiple observation without methodology context | Medium → Low |
| Earnings Intelligence Framework | Raw earnings composition without quality rules | Medium → Low |
| Peer Group Registry | Peer comparison blocked (ad-hoc comparisons prohibited) | Low → Insufficient |
| Portfolio Health Framework | Raw exposure observation without construct definitions | Medium → Low |
| Correlation/Dependency Framework | Raw correlation observation without regime context | Medium → Low |
| Signal Calculation Framework | Fact-only interpretation (signal-dependent interpretation reduced) | Varies by block |
| Data Ingestion/Normalization Framework | No guaranteed fact delivery (interpretation may be impossible) | Low → Insufficient |

### 5.3 Cascading Unavailability

If both the Data Ingestion/Normalization Framework AND the Signal Calculation Framework are unavailable, SAI blocks have no guaranteed evidence supply. In this state:

- Blocks that receive manually provisioned facts may still produce limited interpretation
- Blocks without any evidence source produce output with `evidence_completeness: insufficient`
- No block is removed from the output structure — all 24 blocks always appear
- The system-level limitation is documented at the output level, not hidden

### 5.4 No Silent Degradation Rule

SAI MUST NOT:

- Silently omit a block because its deferred dependency is unavailable
- Pretend a block has full evidence when a deferred framework is missing
- Substitute its own methodology for a missing framework's methodology
- Use "reasonable defaults" or "industry standards" in place of canonical definitions
- Infer what a deferred framework would provide based on common practice

---

## 6. Boundary Statement

### Absolute Boundaries

This artifact declares interface expectations ONLY. The following are explicitly prohibited:

1. **No framework definition**: This artifact does NOT define any of the seven deferred frameworks. It declares what SAI expects from them — nothing more.

2. **No methodology creation**: This artifact does NOT create valuation methodologies, earnings calculation formulas, peer selection algorithms, portfolio optimization logic, correlation calculation procedures, signal derivation formulas, or data ingestion pipelines.

3. **No scoring**: This artifact does NOT introduce any numeric scores, rankings, or ratings — not for SAI, not for the deferred frameworks, not for the interface between them.

4. **No implementation**: This artifact does NOT contain code, schemas, APIs, services, validators, parsers, or runtime architecture of any kind.

5. **No registry mutation**: This artifact does NOT modify the artifact registry, domain registry, narrative registry, or any other canonical registry in the system.

6. **No fact/signal creation**: This artifact does NOT create new facts, signals, evidence objects, or any Market Evidence Framework primitives.

7. **No asset mapping**: This artifact does NOT create asset-to-narrative mappings, asset-to-peer mappings, or any other asset-level entity relationships.

### Interface vs. Implementation Distinction

| This artifact IS | This artifact IS NOT |
|-----------------|---------------------|
| A declaration of expectations | An implementation specification |
| A contract statement | A design document for deferred frameworks |
| A boundary marker | An architecture blueprint |
| A dependency acknowledgment | A dependency resolution |
| A limitation disclosure | A workaround proposal |

---

## 7. Relationship to Existing SAI Artifacts

This artifact relates to the following SAI deliverables:

| Artifact | Relationship |
|----------|-------------|
| block_taxonomy.md | Defines the 24 blocks that consume deferred framework interfaces |
| fact_consumption_matrix.md | Maps facts consumed by blocks — facts originate from Data Ingestion/Normalization Framework |
| signal_consumption_matrix.md | Maps signals consumed by blocks — signals originate from Signal Calculation Framework |
| output_object_spec.md | Defines the output object with `deferred_dependency_notes` field |
| provenance_contract.md | Defines provenance requirements that deferred frameworks must satisfy |
| red_flag_taxonomy.md | Defines red flags that may be triggered by deferred framework availability |
| temporal_resolution_matrix.md | Defines temporal freshness that deferred frameworks must respect |

(See: block_taxonomy.md, Section: Block Architecture Principles)
(See: output_object_spec.md, Section: Output Object Fields — deferred_dependency_notes)
(See: provenance_contract.md, Section: Provenance Chain Requirements)

---

## 8. VG-SAI-4 Evidence Statement

This artifact provides evidence for **VG-SAI-4 (Interface Contract Gate)** by demonstrating:

| Gate Criterion | Evidence |
|---------------|----------|
| All 7 deferred framework interfaces have explicit contracts | Sections 2.1–2.7 define contracts for all 7 frameworks |
| Each contract declares what SAI expects to consume | "What SAI Expects to Consume" section per framework |
| Each contract declares what SAI may emit | "What SAI May Emit" section per framework |
| Each contract declares what SAI must NOT define | "What SAI Must NOT Define" section per framework |
| Each contract declares current limitation | "Current Limitation" section per framework |
| Each contract identifies affected SAI blocks | "Affected SAI Blocks" table per framework |
| No framework is invented or implemented | No-Framework-Invention Statement per framework |
| Governance boundary is stated | Governance Boundary Statement per framework |

**Gate readiness**: This artifact is READY FOR EXPLICIT GATE EXECUTION. VG-SAI-4 is NOT passed by this artifact alone — it requires a separate gate execution artifact with explicit PASS/FAIL evidence.

(See: tasks.md, Section: 15.4 Execute VG-SAI-4 Interface Contract Gate)

---

## 9. No-Drift Statement

This artifact has been created within the definition-layer scope of the Single Asset Intelligence Framework. During creation, no scope pressure toward implementation, scoring, recommendation, allocation, or framework invention was observed or accommodated.

**Confirmed**:
- Zero implementation code produced
- Zero scoring or recommendation logic introduced
- Zero registry or SSOT mutations performed
- Zero facts, signals, or evidence primitives created
- Zero asset-to-narrative or asset-to-peer mappings created
- Zero deferred frameworks were defined, designed, or architected
- All cross-references use canonical format
- All content is in English

---

*End of artifact*
