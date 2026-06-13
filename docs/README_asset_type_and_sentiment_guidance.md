# Asset Type and Analyst Sentiment Guidance

---

## Purpose

This README is architecture guidance for future specs and future extensions to the MoneyHorst / Portfolio OS system. It records decisions and constraints for:

- Supporting ETF/fund assets as analyzable asset types beyond operating-company equities
- Consuming analyst sentiment as an upstream evidence/signal input

This document is NOT an implementation. It is NOT a requirement mutation. It is NOT part of the active SAI gate execution pipeline. It does not create executable logic, does not modify existing spec artifacts, and does not trigger any verification gate.

Future specs that address asset-type expansion or sentiment integration should consume this guidance as an architectural starting point.

---

## Authority and Scope

| Field | Value |
|-------|-------|
| **Authority** | ARCH guidance |
| **Status** | Guidance / future-spec input |
| **Applies to** | Future MoneyHorst asset-type support and future sentiment-signal contracts |
| **Does NOT mutate** | Current SAI requirements, design, tasks, artifacts, gates, registries, or SSOT files |

---

## Cross-References

This guidance must be read together with the MoneyHorst Investment Style, Method, and Allocation Taxonomy SSOT:

- `docs/moneyhorst/investment_style_method_taxonomy_ssot.md`

That SSOT defines the distinction between asset class, instrument, investment style, factor, method, asset allocation, strategy, and system layer. This document uses "asset type" in the SAI block-applicability sense and must not override the taxonomy SSOT.

---

## Core Principles

1. **Asset type must be explicit.** Every asset analyzed by SAI or any future extension must carry an explicit asset_type classification. Implicit assumptions about asset nature are prohibited.

2. **ETF/fund assets are valid analyzable assets, but not operating-company equities.** They may be represented, analyzed, and included in portfolio context — but they have fundamentally different evidence structures and require adapted interpretation.

3. **Operating-company blocks must not be mechanically applied to ETFs/funds.** Blocks designed for corporate fundamentals (revenue, margins, earnings, solvency) cannot be applied to fund products without explicit reinterpretation or disabling.

4. **Analyst sentiment is evidence or signal input, not a recommendation.** Sentiment data (ratings, revisions, target prices, consensus) is consumed as evidence. It never becomes a SAI output, never overrides hard evidence, and never generates action instructions.

5. **Sentiment must never override hard evidence, provenance, or boundary rules.** No amount of positive analyst consensus can substitute for missing financial data, broken provenance chains, or violated boundary constraints.

6. **SAI consumes analyst sentiment only if delivered by approved upstream evidence/signal frameworks.** SAI does not scrape, calculate, or derive sentiment independently. It consumes pre-calculated sentiment signals from upstream frameworks that satisfy provenance requirements.

7. **SAI must not create buy/sell/hold, conviction, target price, or expected return outputs from sentiment.** This prohibition is absolute regardless of the strength, unanimity, or recency of analyst sentiment inputs.

---

## Asset Type Handling

### Taxonomy Clarification

In the MoneyHorst Investment Taxonomy, ETFs and funds are classified as **instruments**: legal/security wrappers used to express exposure.

Within SAI guidance, ETFs and funds may also be treated as distinct **asset types** for block-applicability purposes. This means certain SAI blocks may be enabled, disabled, or reinterpreted depending on whether the subject is an operating company equity, ETF, fund, index, derivative, commodity, or other wrapper.

These two classifications are compatible because they operate at different architectural layers:

- **Taxonomy layer**: ETF/fund = instrument
- **SAI block-applicability layer**: ETF/fund = asset type category

This document must not be interpreted as redefining ETFs or funds as investment styles, factors, strategies, or asset classes.

The following asset-type categories are defined at guidance level for future specification work.

### operating_company_equity

| Field | Value |
|-------|-------|
| **Description** | A publicly traded equity security representing ownership in an operating corporation with revenue, costs, assets, liabilities, and earnings |
| **What SAI may consume** | All 68 fact categories, all 23 signal categories as currently defined |
| **Block applicability** | All 24 SAI blocks apply directly |
| **Special provenance needs** | Standard corporate filing provenance (10-K, 10-Q, 20-F, annual reports) |
| **Boundary notes** | Current SAI architecture fully covers this type |

### etf

| Field | Value |
|-------|-------|
| **Description** | An exchange-traded fund that tracks an index, sector, commodity, or strategy — a pooled investment vehicle, not an operating company |
| **What SAI may consume** | Holdings composition, issuer identity, index/methodology, TER/fees, liquidity (ADV, spread), tracking error, AUM, domicile, distribution policy, replication method, concentration (top holdings), look-through exposures, benchmark methodology |
| **Blocks requiring reinterpretation or disabling** | Revenue Quality, Margin Quality, Cashflow Quality, Credit/Solvency Risk, Pension Obligations, Customer Concentration, Supply Chain Stability, Pricing Power, Earnings Quality, Guidance/Estimate Revisions, Valuation Context, Value Trap Guard |
| **Blocks that may remain relevant** | Portfolio Fit, Relative Strength, Liquidity Sensitivity (via ADV), Correlation (vs. benchmark/peers), Drawdown, Macro Sensitivity, Narrative/Exposure overlap |
| **Special provenance needs** | Holdings date, issuer/source, index methodology source, AUM/date, TER/fee date, tracking error period, replication method source, domicile/legal structure source |
| **Boundary notes** | ETF analysis must not infer fund quality from issuer brand alone; must not treat an ETF as a company with revenue, margins, or solvency |

### fund

| Field | Value |
|-------|-------|
| **Description** | A mutual fund, UCITS, or other pooled investment vehicle that is not exchange-traded — similar to ETF but with different liquidity, pricing, and trading characteristics |
| **What SAI may consume** | Same as ETF plus: NAV calculation frequency, redemption terms, gate provisions, side pocket exposure, fund-of-fund structure |
| **Blocks requiring reinterpretation or disabling** | Same as ETF |
| **Blocks that may remain relevant** | Same as ETF, with additional liquidity constraints (redemption terms vs. ADV) |
| **Special provenance needs** | Same as ETF plus: NAV publication source, redemption schedule, prospectus date |
| **Boundary notes** | Fund analysis must respect the same boundaries as ETF; additional liquidity constraints from redemption terms |

### index

| Field | Value |
|-------|-------|
| **Description** | A market index (e.g., S&P 500, MSCI World) used as a benchmark reference — not a tradeable instrument per se, but a reference frame |
| **What SAI may consume** | Composition, methodology, rebalance schedule, sector/geographic weights, constituent count, concentration metrics |
| **Blocks requiring reinterpretation or disabling** | All operating-company blocks disabled; index serves as reference frame for SAI-BLK-19, SAI-BLK-20 |
| **Blocks that may remain relevant** | Used as benchmark in Relative Strength, Correlation blocks — not as a standalone analyzed asset |
| **Special provenance needs** | Index provider, methodology document date, constituent list date |
| **Boundary notes** | An index is a reference frame, not an investment to be scored or recommended |

### commodity

| Field | Value |
|-------|-------|
| **Description** | A physical or financially-settled commodity (oil, gold, copper, agricultural) analyzed as an asset class exposure |
| **What SAI may consume** | Spot/futures prices, supply/demand fundamentals, storage costs, contango/backwardation, seasonal patterns, geopolitical supply risk |
| **Blocks requiring reinterpretation or disabling** | All corporate blocks disabled; commodity has no revenue, margins, or solvency |
| **Blocks that may remain relevant** | Relative Strength (vs. commodity index), Correlation, Macro Sensitivity, Portfolio Fit |
| **Special provenance needs** | Exchange/source, contract specification, settlement type, observation timestamp |
| **Boundary notes** | Commodity analysis must not infer "fair value" or "target price" — SAI boundary rules apply |

### derivative_or_structured_product

| Field | Value |
|-------|-------|
| **Description** | Options, futures, swaps, structured notes, or other derivative instruments |
| **What SAI may consume** | Underlying reference, payoff structure, maturity, Greeks (as evidence), implied volatility context |
| **Blocks requiring reinterpretation or disabling** | All operating-company blocks disabled for the derivative itself (underlying may be separately analyzed) |
| **Blocks that may remain relevant** | Liquidity Sensitivity, Correlation to underlying, Portfolio Fit (exposure contribution) |
| **Special provenance needs** | Contract specification, exchange/OTC source, pricing model reference, valuation timestamp |
| **Boundary notes** | SAI must not price derivatives, recommend strategies, or calculate Greeks independently |

### cash_or_cash_equivalent

| Field | Value |
|-------|-------|
| **Description** | Cash, money market instruments, T-bills, or other near-zero-duration instruments |
| **What SAI may consume** | Yield, currency, maturity, counterparty, liquidity |
| **Blocks requiring reinterpretation or disabling** | All blocks effectively disabled — cash has no equity-style diagnostics |
| **Blocks that may remain relevant** | Portfolio Fit (concentration contribution from cash allocation) |
| **Special provenance needs** | Currency, counterparty identification, yield observation date |
| **Boundary notes** | Minimal SAI relevance; primarily a portfolio context component |

### other

| Field | Value |
|-------|-------|
| **Description** | Any asset type not covered above — real estate, private equity, crypto, collectibles, etc. |
| **What SAI may consume** | To be determined per asset type when a dedicated spec is created |
| **Blocks requiring reinterpretation or disabling** | To be determined — likely most operating-company blocks disabled |
| **Blocks that may remain relevant** | Portfolio Fit, Macro Sensitivity, Liquidity Sensitivity (if applicable) |
| **Special provenance needs** | To be determined per asset type |
| **Boundary notes** | Must not apply equity-centric analysis without explicit adaptation |

---

## ETF / Fund Analysis Boundary

SAI or any future ETF/Fund Intelligence module must NOT:

- Infer ETF quality from issuer brand alone
- Recommend ETF purchase or sale
- Assign fund scores or rankings
- Create target allocation or position size
- Create portfolio optimization logic
- Invent holdings or look-through exposures
- Assume benchmark methodology if not provided
- Treat an ETF as a company with revenue, margins, earnings, or solvency (unless analyzing the issuer entity, not the fund product)

ETF/fund analysis produces diagnostic observations about fund structure, methodology, cost, liquidity, and exposure characteristics. It never prescribes action.

---

## Analyst Sentiment Handling

Analyst sentiment is defined as a future upstream evidence/signal input. SAI or any future sentiment-consuming module receives sentiment data from approved upstream frameworks — it does not generate, scrape, or independently calculate sentiment.

### Allowed Future Inputs

The following sentiment-derived evidence may be consumed by SAI blocks when delivered by approved upstream frameworks:

| # | Input | Description |
|---|-------|-------------|
| 1 | Consensus rating distribution | Distribution of buy/hold/sell ratings across covering analysts |
| 2 | Rating changes / upgrades / downgrades | Directional shifts in analyst ratings over time |
| 3 | Estimate revisions | Changes to EPS, revenue, EBITDA consensus estimates |
| 4 | Price target dispersion (as evidence only) | Spread between highest and lowest analyst price targets — consumed as disagreement evidence, NOT as SAI output |
| 5 | Recommendation breadth (as evidence only) | Number of analysts with active coverage — consumed as coverage evidence, NOT as recommendation |
| 6 | Analyst count | Total number of analysts covering the asset |
| 7 | Revision momentum | Direction and acceleration of estimate revision trends |
| 8 | EPS / revenue / EBITDA consensus revision trajectory | Time-series pattern of consensus estimate changes |
| 9 | Sentiment disagreement / dispersion | Degree of analyst disagreement as a diagnostic signal |
| 10 | Stale analyst coverage indicator | Flag when analyst coverage is outdated or abandoned |

---

## Analyst Sentiment Boundary

SAI must NOT:

- Produce buy/sell/hold from analyst sentiment
- Endorse analyst ratings as authoritative conclusions
- Treat analyst consensus as truth
- Convert analyst sentiment into recommendation output
- Create a conviction score from sentiment inputs
- Create a confidence score from analyst count
- Create expected return from target price inputs
- Use price targets as fair value
- Use analyst sentiment as standalone evidence (must be corroborated by fundamental/market evidence)
- Override fundamental, credit, valuation, or provenance gaps with sentiment

Analyst sentiment is one evidence dimension among many. It informs diagnostic context. It never instructs action.

---

## Provenance Requirements

### For ETF/Fund Inputs

| # | Required Provenance Field | Purpose |
|---|--------------------------|---------|
| 1 | Holdings date | Temporal freshness of holdings composition |
| 2 | Issuer/source | Identity of the fund issuer |
| 3 | Index methodology source | Authority for benchmark/tracking methodology |
| 4 | AUM/date | Fund size observation timestamp |
| 5 | TER/fee date | Fee schedule observation timestamp |
| 6 | Liquidity observation timestamp | When ADV/spread was last observed |
| 7 | Tracking error period | Time window over which tracking error is measured |
| 8 | Replication method source | How the fund replicates its benchmark |
| 9 | Domicile/legal structure source | Jurisdictional and regulatory context |

### For Analyst Sentiment Inputs

| # | Required Provenance Field | Purpose |
|---|--------------------------|---------|
| 1 | Analyst/source provider | Who published the rating/estimate |
| 2 | Publication timestamp | When the opinion was published |
| 3 | Rating scale normalization | How the source's scale maps to standard categories |
| 4 | Revision timestamp | When the estimate was last revised |
| 5 | Consensus provider | Which aggregator compiled the consensus |
| 6 | Target price currency and date (if used as evidence) | Currency and observation date for dispersion evidence |
| 7 | Stale threshold | How long before sentiment data is considered stale |
| 8 | Coverage count | Number of analysts in the consensus sample |

---

## Relationship to Existing SAI Boundaries

This guidance is conceptually consistent with the following existing SAI architectural constraints (referenced here without modifying those files):

| SAI Artifact | Relevant Boundary | Guidance Alignment |
|--------------|-------------------|-------------------|
| output_object_spec.md | Prohibited fields (score, rank, recommendation, etc.) | ETF/sentiment outputs must respect the same prohibited fields |
| provenance_contract.md | No-orphan interpretation rule | ETF and sentiment inputs require full provenance chains |
| deferred_interfaces.md | Upstream framework dependency model | Sentiment is an upstream framework dependency, not SAI-internal |
| peer_benchmark.md | Relative behavior boundary | ETFs may use relative strength/correlation blocks with same boundaries |
| portfolio_fit_interface.md | No allocation authority | ETF/fund portfolio fit follows same diagnostic-only boundary |
| valuation_boundary.md | No fair value / target price | Analyst target prices cannot become SAI fair value outputs |
| credit_solvency.md | Ratings are input evidence, not truth | Analyst ratings follow same principle: input evidence, not truth |

---

## Future Spec Candidates

The following are candidate future specifications that would consume this guidance:

| # | Candidate Spec | Purpose |
|---|---------------|---------|
| 1 | ETF / Fund Intelligence Framework | Define ETF/fund-specific analysis blocks, evidence contracts, and interpretation rules |
| 2 | Asset Type Registry | Canonical registry of supported asset types with block applicability rules |
| 3 | Analyst Sentiment Evidence Contract | Formal interface contract for consuming sentiment from upstream providers |
| 4 | Look-Through Exposure Framework | Define how ETF/fund holdings are decomposed into underlying exposures |
| 5 | Fund Holdings Ingestion Contract | Formal contract for receiving normalized fund holdings data |
| 6 | Consensus Estimate Signal Contract | Formal signal contract for consuming consensus estimate revisions |
| 7 | Asset-Type-Aware SAI Adaptation Layer | Rules for enabling/disabling/reinterpreting SAI blocks per asset type |

---

## Non-Goals

This document explicitly does NOT:

- Contain implementation code
- Define database schemas or APIs
- Create runtime validators, parsers, services, or ETL pipelines
- Mutate any registry or SSOT file
- Mutate SAI requirements, design, tasks, artifacts, or gates
- Execute any verification gate
- Create scoring, ranking, or recommendation logic
- Create allocation, position sizing, or trading logic
- Create asset-to-narrative mappings
- Create facts, signals, or evidence primitives

---

## Guidance Summary

1. **ETFs/funds are valid future assets**, but require asset-type-aware interpretation. Operating-company blocks cannot be mechanically applied. Fund-specific evidence dimensions (holdings, TER, tracking error, replication method) are required.

2. **Analyst sentiment is a useful evidence/signal input**, but never a recommendation source. It informs diagnostic context alongside fundamental and market evidence. It never overrides hard evidence or generates action instructions.

3. **Future specs must preserve SAI boundaries.** All existing prohibitions (no scoring, no recommendation, no allocation, no trading) apply equally to ETF/fund analysis and sentiment consumption.

---

*End of guidance document.*
