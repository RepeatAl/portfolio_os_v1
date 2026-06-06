# Single Asset Intelligence Framework — Peer / Benchmark Artifact

**Artifact**: peer_benchmark.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 11.1 Create peer/benchmark artifact
**Requirements**: SAI-REQ-10 (Peer/Benchmark Reality Boundary)
**Verification Gate**: VG-SAI-1 (Requirements Completeness Gate)
**Status**: Draft

---

## 1. Purpose and Scope

This artifact defines the comprehensive interpretation scope for relative market behavior assessment within the Single Asset Intelligence Framework. It covers all dimensions of relative strength, benchmark comparison, sector comparison, peer comparison, correlation structure, beta decomposition, volatility, and drawdown analysis — the full peer/benchmark reality boundary mandated by SAI-REQ-10.

This artifact governs three SAI analysis blocks:

- **SAI-BLK-19**: Relative Strength (daily temporal class)
- **SAI-BLK-20**: Benchmark/Sector/Peer Correlation (daily temporal class)
- **SAI-BLK-21**: Peer Comparison (daily temporal class)

**This is a definition-layer artifact.** It contains no implementation code, no peer selection algorithms, no correlation formulas, no factor model methodology, no beta calculation procedures, no statistical significance methodology, no scoring systems, no ranking algorithms, no recommendation logic, no allocation decisions, no trading signals, no registry mutations, no fact/signal creation, and no asset/narrative mappings.

**Core statement**: Peer groups are non-canonical until the Peer Group Registry exists. SAI consumes peer definitions; it does not create them.

(See: design.md, Section: Components and Interfaces — Market Position Blocks)
(See: requirements.md, Section: SAI-REQ-10 — Peer/Benchmark Reality Boundary)

---

## 2. Core Peer/Benchmark Interpretation Principles

### Principle 1 — Own-Strength vs. Beta-Driven Movement

The fundamental diagnostic question for any market position observation is: does this asset move because of its own fundamental characteristics, or because it is carried by index/sector/factor exposure? SAI must distinguish between asset-specific strength and beta-driven movement in every relative market observation. An asset that rises only because its sector rises has not demonstrated own-strength.

### Principle 2 — Peer Groups Are Non-Canonical Until Peer Group Registry Exists

Peer comparison requires a defined, canonical peer group. Until the Peer Group Registry exists and provides canonical peer definitions, peer comparison interpretation within SAI-BLK-21 is blocked or severely limited. SAI does NOT create ad-hoc peer groups, does NOT select peers, and does NOT invent peer sets. This is a hard constraint.

### Principle 3 — Correlation Is Context, Not Signal

Correlation coefficients, beta decomposition, and co-movement patterns are diagnostic context for understanding relative behavior. They are NOT trading signals, NOT factor model outputs, and NOT inputs to portfolio optimization. SAI observes correlation structure; it does not act on it.

### Principle 4 — Relative Observation Requires Reference Frame

Every relative market observation requires an explicit reference frame (benchmark, sector, or peer group). An observation without a defined reference frame is not valid. SAI must always state what the asset is being compared against.

### Principle 5 — Drawdown Context Matters

A drawdown must be contextualized: was it market-wide, sector-wide, or asset-specific? The same percentage decline has different diagnostic meaning depending on whether the broader market experienced a comparable decline. SAI distinguishes between shared stress and idiosyncratic decline.

---

## 3. Covered Blocks

### SAI-BLK-19: Relative Strength

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-19 |
| **block_name** | Relative Strength |
| **category** | Market Position |
| **temporal_class** | daily |
| **purpose** | Diagnose price strength relative to benchmark, sector, and peers |
| **primary_fact_families** | Price performance vs benchmark, sector performance, drawdown history |
| **primary_signal_families** | Relative strength signals, momentum signals, drawdown signals |
| **deferred_dependencies** | None |
| **boundary_statement** | Produces relative strength diagnostic only — never momentum scores, trading signals, or buy/sell implications |

### SAI-BLK-20: Benchmark/Sector/Peer Correlation

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-20 |
| **block_name** | Benchmark/Sector/Peer Correlation |
| **category** | Market Position |
| **temporal_class** | daily |
| **purpose** | Diagnose correlation structure and beta decomposition |
| **primary_fact_families** | Correlation coefficients, rolling beta, R-squared, factor exposures |
| **primary_signal_families** | Correlation regime signals, beta decomposition signals |
| **deferred_dependencies** | Correlation/Dependency Framework |
| **boundary_statement** | Produces correlation diagnostic only — never factor model outputs, statistical arbitrage signals, or pairs trading recommendations |

### SAI-BLK-21: Peer Comparison

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-21 |
| **block_name** | Peer Comparison |
| **category** | Market Position |
| **temporal_class** | daily |
| **purpose** | Diagnose competitive positioning relative to peer group |
| **primary_fact_families** | Peer financial metrics, market share, growth differentials, margin differentials |
| **primary_signal_families** | Peer-relative comparison signals, competitive position signals |
| **deferred_dependencies** | Peer Group Registry |
| **boundary_statement** | Produces peer-relative diagnostic only — never peer ranking, factor model analysis, or competitive strategy recommendations |

(See: block_taxonomy.md, Section: Market Position Blocks)
(See: temporal_resolution_matrix.md, Section: Daily Temporal Class)

---

## 4. Relative Strength Interpretation Scope (SAI-BLK-19)

SAI-BLK-19 covers the diagnostic assessment of price strength relative to defined reference frames. The following interpretation dimensions are within scope per SAI-REQ-10.

### 4.1 Relative Strength vs. Benchmark

**Diagnostic question**: Is the asset generating returns above or below its primary benchmark, and is this divergence persistent or transient?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Relative strength vs. benchmark |
| **Reference frame** | Primary benchmark (e.g., S&P 500, MSCI World, STOXX 600 — as assigned by asset classification) |
| **Evidence consumed** | Asset total return, benchmark total return, relative return spread, lookback windows (1-month, 3-month, 6-month, 12-month) |
| **Diagnostic purpose** | Establishes whether the asset is participating in or diverging from broad market behavior. Persistent relative weakness or strength is diagnostic context for fundamental investigation. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-19-01 — direct coverage: persistent underperformance despite sector tailwind) |

### 4.2 Relative Strength vs. Sector

**Diagnostic question**: Is the asset performing in line with its sector, or is there asset-specific divergence from sector behavior?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Relative strength vs. sector |
| **Reference frame** | Sector index (as determined by asset's GICS/ICB sector classification) |
| **Evidence consumed** | Asset total return, sector index total return, relative return spread, sector-relative performance over multiple lookback windows |
| **Diagnostic purpose** | Distinguishes between sector-driven movement and asset-specific behavior. An asset that underperforms its sector while the sector rises suggests asset-specific weakness masked by sector tailwinds. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-19-01 — direct coverage: persistent underperformance despite sector tailwind) |

### 4.3 Relative Strength vs. Peers

**Diagnostic question**: How does the asset perform relative to its defined peer group?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Relative strength vs. peers |
| **Reference frame** | Canonical peer group (as provided by Peer Group Registry — non-canonical until registry exists) |
| **Evidence consumed** | Asset total return, peer group median/mean total return, rank within peer group return distribution |
| **Diagnostic purpose** | Provides the most granular comparison by measuring performance against companies with similar business characteristics. Persistent divergence from peer performance indicates asset-specific factors. |
| **Peer Group Registry dependency** | This dimension requires canonical peer definitions from the Peer Group Registry. Without the registry, peer-relative strength observation is limited to benchmark and sector comparisons only. No ad-hoc peer groups permitted. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-19-02 — related coverage: maximum drawdown exceeding 2x sector drawdown) |

### 4.4 Volatility

**Diagnostic question**: What is the realized volatility of the asset, and how does it compare to its reference frames?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Volatility |
| **Reference frame** | Benchmark, sector, peer group (where available) |
| **Evidence consumed** | Realized volatility (annualized standard deviation of returns), relative volatility vs. benchmark, relative volatility vs. sector, volatility regime changes |
| **Diagnostic purpose** | Volatility is diagnostic context for understanding the risk characteristics of the asset. Elevated volatility relative to sector or benchmark indicates higher uncertainty or information asymmetry. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-19-02 — related coverage: disproportionate drawdown exposure) |

### 4.5 Drawdown

**Diagnostic question**: What is the magnitude of decline from peak, and is the drawdown shared or idiosyncratic?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Drawdown |
| **Reference frame** | Benchmark, sector (to contextualize whether drawdown is market-wide, sector-wide, or asset-specific) |
| **Evidence consumed** | Maximum drawdown from peak, current drawdown depth, drawdown duration, recovery trajectory, benchmark drawdown over same period, sector drawdown over same period |
| **Diagnostic purpose** | Drawdown context determines whether an asset's decline reflects broad market stress (systemic), sector stress (shared), or asset-specific deterioration (idiosyncratic). The diagnostic meaning of a -30% drawdown is fundamentally different if the market also declined -25% vs. if the market was flat. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-19-02 — direct coverage: maximum drawdown exceeding 2x sector drawdown) |

(See: fact_consumption_matrix.md, Section: SAI-BLK-19 Fact Mappings)
(See: signal_consumption_matrix.md, Section: SAI-BLK-19 Signal Mappings)

---

## 5. Benchmark/Sector/Peer Correlation Interpretation Scope (SAI-BLK-20)

SAI-BLK-20 covers the diagnostic assessment of correlation structure, co-movement patterns, and beta decomposition. This block has a deferred dependency on the Correlation/Dependency Framework.

### 5.1 Correlation to Benchmark

**Diagnostic question**: How strongly does the asset co-move with the primary benchmark, and is the correlation regime stable?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Correlation to benchmark |
| **Reference frame** | Primary benchmark |
| **Evidence consumed** | Rolling correlation coefficient (benchmark), correlation stability over time, correlation regime shift observations |
| **Diagnostic purpose** | Benchmark correlation establishes the baseline co-movement regime. High correlation means the asset largely moves with the market. Low correlation suggests idiosyncratic drivers dominate. Sudden correlation shifts are diagnostic of structural changes. |
| **Deferred dependency** | Correlation calculation methodology deferred to Correlation/Dependency Framework. Without it, only raw observed correlation values are reported. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-20-01 — direct coverage: correlation regime shift exceeding 0.3 over 60 days) |

### 5.2 Correlation to Peers

**Diagnostic question**: How strongly does the asset co-move with its peer group, and what does divergence imply?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Correlation to peers |
| **Reference frame** | Canonical peer group (as provided by Peer Group Registry — non-canonical until registry exists) |
| **Evidence consumed** | Pairwise correlation coefficients with individual peers, average correlation with peer group, correlation dispersion within peer group |
| **Diagnostic purpose** | Peer correlation context establishes whether the asset shares its peers' market behavior or diverges. Low peer correlation may indicate misclassification, unique business characteristics, or structural change. |
| **Peer Group Registry dependency** | This dimension requires canonical peer definitions. Without the registry, peer correlation observation is blocked. No ad-hoc peer correlations permitted. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-20-01 — related coverage: correlation regime shifts) |

### 5.3 Beta Decomposition

**Diagnostic question**: How much of the asset's movement is explained by market beta, sector beta, and idiosyncratic factors?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Beta decomposition |
| **Reference frame** | Primary benchmark (market beta), sector index (sector beta) |
| **Evidence consumed** | Market beta coefficient, sector beta coefficient, R-squared values, idiosyncratic return component, beta stability over time |
| **Diagnostic purpose** | Beta decomposition is the formal mechanism for answering whether the asset moves by own-strength or by beta-driven movement. An asset with high market beta and low idiosyncratic return is primarily a market proxy. An asset with high idiosyncratic return moves independently of market/sector forces. |
| **Deferred dependency** | Beta decomposition methodology deferred to Correlation/Dependency Framework. Without it, only raw observed beta values are reported without regime detection or statistical context. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-20-02 — direct coverage: asymmetric beta with upside participation below 0.7) |

### 5.4 Own-Strength vs. Beta-Driven Movement

**Diagnostic question**: Is the asset generating returns through its own fundamental characteristics, or merely being carried by index/sector exposure?

| Field | Value |
|-------|-------|
| **Interpretation dimension** | Own-strength vs. beta-driven movement |
| **Reference frame** | Derived from beta decomposition analysis |
| **Evidence consumed** | Idiosyncratic return component, alpha observation (excess return after beta adjustment), consistency of own-strength contribution |
| **Diagnostic purpose** | This is the synthesis dimension. By combining beta decomposition, relative strength, and correlation context, SAI produces a diagnostic observation of whether the asset demonstrates fundamental agency or passive co-movement. This distinction informs downstream blocks that depend on asset-specific quality assessment. |
| **Deferred dependency** | Formal own-strength isolation requires Correlation/Dependency Framework methodology. Without it, only directional observations are possible (asset rose while sector fell → suggests own-strength). |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-20-02 — related coverage: asymmetric beta indicating poor own-strength characteristics) |

(See: fact_consumption_matrix.md, Section: SAI-BLK-20 Fact Mappings)
(See: signal_consumption_matrix.md, Section: SAI-BLK-20 Signal Mappings)
(See: deferred_interfaces.md, Section: 2.5 Correlation/Dependency Framework)

---

## 6. Peer Comparison Interpretation Scope (SAI-BLK-21)

SAI-BLK-21 covers the diagnostic assessment of competitive positioning relative to a defined peer group. This block has a primary deferred dependency on the Peer Group Registry.

### 6.1 Peer Group Dependency Statement

**SAI consumes peer definitions; it does not create them.**

SAI-BLK-21 requires canonical peer group definitions from the Peer Group Registry. The following rules govern peer comparison interpretation:

1. Peer comparison requires a defined, canonical peer group provided by the Peer Group Registry
2. Ad-hoc peer comparisons using invented or assumed peer sets are prohibited
3. Until the Peer Group Registry provides canonical definitions, SAI-BLK-21 operates with severely limited interpretation capability
4. The `deferred_dependency_notes` field must state: "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."
5. When the Peer Group Registry becomes available, SAI-BLK-21 consumes its definitions without modification

### 6.2 Unavailable Peer Group Registry Handling

When the Peer Group Registry is unavailable:

| Behavior | Description |
|----------|-------------|
| **Peer comparison interpretation** | Blocked or severely limited |
| **Ad-hoc peer groups** | Prohibited — SAI does NOT invent peer sets |
| **Assumed peer sets** | Prohibited — common industry knowledge does NOT substitute for canonical definitions |
| **Fallback behavior** | SAI-BLK-21 output reports the limitation explicitly; no peer metrics are fabricated |
| **evidence_completeness** | Set to "insufficient" when Peer Group Registry is unavailable |
| **deferred_dependency_notes** | Must contain explicit limitation statement |
| **Other blocks unaffected** | SAI-BLK-19 and SAI-BLK-20 operate independently with benchmark/sector reference frames |

### 6.3 Peer Comparison Dimensions (When Peer Group Registry Available)

When the Peer Group Registry provides canonical peer definitions, SAI-BLK-21 observes:

| Dimension | What SAI Observes | What SAI Does NOT Do |
|-----------|------------------|---------------------|
| Growth differentials | Revenue/earnings growth relative to peer median | Does not rank peers by growth |
| Margin differentials | Operating/gross margin relative to peer median | Does not score margin quality vs. peers |
| Valuation differentials | Multiple premium/discount relative to peer median | Does not label premium as justified/unjustified |
| Return differentials | ROIC/ROE relative to peer median | Does not rank peers by return quality |
| Market share observations | Share position relative to peer group total | Does not predict share trajectory |
| Financial metric divergence | Standard deviation distance from peer median | Does not label outlier as positive/negative |

### 6.4 Peer Comparison Evidence Requirements

| Field | Value |
|-------|-------|
| **Required input** | Canonical peer group definition from Peer Group Registry |
| **Minimum peer count** | As defined by Peer Group Registry (SAI does not set minimums) |
| **Metric comparability** | Peers must share comparable financial reporting standards and fiscal periods |
| **Temporal alignment** | Peer metrics must be aligned to same reporting period where possible |
| **Staleness rule** | Daily temporal class applies — peer metric freshness follows market data cadence for pricing, quarterly for fundamentals |

(See: fact_consumption_matrix.md, Section: SAI-BLK-21 Fact Mappings)
(See: signal_consumption_matrix.md, Section: SAI-BLK-21 Signal Mappings)
(See: deferred_interfaces.md, Section: 2.3 Peer Group Registry)

---

## 7. Benchmark Comparison Boundary

### 7.1 What SAI May Observe (Benchmark Context)

- Asset total return vs. benchmark total return over defined lookback windows
- Magnitude and direction of relative performance spread
- Persistence of relative performance (transient vs. sustained divergence)
- Whether outperformance/underperformance coincides with sector behavior
- Drawdown relative to benchmark during market stress

### 7.2 What SAI Must NOT Do (Benchmark Context)

- Must NOT label an asset as a benchmark "winner" or "loser"
- Must NOT imply that benchmark outperformance indicates a buy opportunity
- Must NOT imply that benchmark underperformance indicates a sell opportunity
- Must NOT create momentum-based trading signals from relative strength
- Must NOT extrapolate relative strength trends into future performance expectations
- Must NOT use relative strength as an input to portfolio optimization

---

## 8. Sector Comparison Boundary

### 8.1 What SAI May Observe (Sector Context)

- Asset performance relative to its assigned sector index
- Whether asset-specific strength or weakness diverges from sector behavior
- Sector rotation context (is the sector itself strong or weak relative to the market?)
- Degree to which asset movement is explained by sector-level forces

### 8.2 What SAI Must NOT Do (Sector Context)

- Must NOT recommend sector rotation
- Must NOT label sectors as "favorable" or "unfavorable" for investment
- Must NOT create sector-timing signals
- Must NOT produce sector scores or sector rankings
- Must NOT imply sector membership determines asset quality
- Must NOT conflate sector performance with asset-specific fundamentals

---

## 9. Peer Comparison Boundary

### 9.1 What SAI May Observe (Peer Context)

- Financial metric position relative to peer group median (growth, margins, returns, leverage)
- Valuation multiple relative to peer group median
- Performance relative to peer group returns
- Divergence magnitude (standard deviations from peer median)
- Whether divergence is persistent or transient

### 9.2 What SAI Must NOT Do (Peer Context)

- Must NOT rank peers (no ordinal ranking within peer group)
- Must NOT assign "best-in-class" or "worst-in-class" labels
- Must NOT imply that peer-relative discount/premium is a buy/sell signal
- Must NOT create competitive strategy recommendations
- Must NOT score competitive positioning
- Must NOT select, modify, or challenge peer group composition
- Must NOT use peer comparison to generate factor model exposures
- Must NOT imply that peer-relative divergence indicates mispricing

---

## 10. Peer Group Registry Dependency

### 10.1 Interface Contract Summary

SAI-BLK-21 depends on the Peer Group Registry for canonical peer definitions. The interface contract is declared in the deferred interfaces artifact. This section summarizes the dependency relationship.

| Aspect | Detail |
|--------|--------|
| **What SAI expects** | Canonical peer group definitions, selection methodology, rotation rules, versioning, validity metadata |
| **What SAI provides** | Peer-relative observations, competitive position context, completeness assessment |
| **What SAI must NOT define** | Peer selection criteria, peer group composition, peer rotation triggers, peer ranking |
| **Current status** | Peer Group Registry unavailable — SAI-BLK-21 interpretation blocked for peer-relative dimensions |
| **Affected interpretation** | All Section 6 dimensions require canonical peer definitions; Section 4.3 (relative strength vs. peers) and Section 5.2 (correlation to peers) also affected |

### 10.2 Graceful Degradation When Peer Group Registry Unavailable

When the Peer Group Registry is unavailable, SAI Market Position blocks degrade as follows:

| Block | Impact | Remaining Capability |
|-------|--------|---------------------|
| SAI-BLK-19 | Partial — peer-relative strength unavailable | Benchmark-relative and sector-relative strength fully operational |
| SAI-BLK-20 | Partial — peer correlation unavailable | Benchmark correlation and sector correlation fully operational; beta decomposition available for market and sector |
| SAI-BLK-21 | Severe — primary function blocked | Only general competitive context from public sources without formal peer-relative metrics |

---

## 11. Correlation/Dependency Framework Dependency

### 11.1 Interface Contract Summary

SAI-BLK-20 depends on the Correlation/Dependency Framework for calculation methodology. The interface contract is declared in the deferred interfaces artifact.

| Aspect | Detail |
|--------|--------|
| **What SAI expects** | Correlation calculation methodology, rolling window parameters, regime detection rules, beta decomposition approach, significance thresholds |
| **What SAI provides** | Correlation regime context, beta interpretation, correlation anomaly observations |
| **What SAI must NOT define** | Correlation formulas, window parameter selection, factor model definitions, statistical significance testing, regime detection algorithms |
| **Current status** | Correlation/Dependency Framework unavailable — SAI-BLK-20 operates with raw observation only |

### 11.2 Graceful Degradation When Correlation/Dependency Framework Unavailable

When the Correlation/Dependency Framework is unavailable:

- SAI-BLK-20 reports raw observed correlation values without regime context
- Beta decomposition is limited to raw observed coefficients without methodology validation
- Correlation regime shift detection is limited to simple magnitude observation without statistical confirmation
- The `deferred_dependency_notes` field states: "Correlation/Dependency Framework not yet available — interpretation limited to raw correlation observation without canonical calculation methodology or regime detection rules."
- SAI-BLK-19 and SAI-BLK-21 are NOT affected by this specific dependency

(See: deferred_interfaces.md, Section: 2.5 Correlation/Dependency Framework)
(See: deferred_interfaces.md, Section: 2.3 Peer Group Registry)

---

## 12. Red Flag Cross-Reference to Canonical Taxonomy

This artifact does NOT create, define, or add new red flags. The canonical red flag definitions for Market Position blocks reside exclusively in the red flag taxonomy artifact. This section cross-references each interpretation dimension against the canonical red flag taxonomy.

| # | Interpretation Dimension | Primary Block | Related Canonical red_flag_id(s) | Canonical Red Flag Title / Summary | Coverage Status |
|---|--------------------------|---------------|----------------------------------|-----------------------------------|----------------|
| 1 | Relative strength vs. benchmark | SAI-BLK-19 | RF-19-01 | Persistent Underperformance Despite Sector Tailwind | direct canonical coverage |
| 2 | Relative strength vs. sector | SAI-BLK-19 | RF-19-01 | Persistent Underperformance Despite Sector Tailwind | direct canonical coverage |
| 3 | Relative strength vs. peers | SAI-BLK-19 | RF-19-01 | Persistent Underperformance Despite Sector Tailwind (peer context) | related canonical coverage |
| 4 | Volatility | SAI-BLK-19 | RF-19-02 | Maximum Drawdown Exceeding 2x Sector Drawdown (volatility context) | related canonical coverage |
| 5 | Drawdown | SAI-BLK-19 | RF-19-02 | Maximum Drawdown Exceeding 2x Sector Drawdown | direct canonical coverage |
| 6 | Correlation to benchmark | SAI-BLK-20 | RF-20-01 | Correlation Regime Shift Exceeding 0.3 Over 60 Days | direct canonical coverage |
| 7 | Correlation to peers | SAI-BLK-20 | RF-20-01 | Correlation Regime Shift Exceeding 0.3 Over 60 Days (peer context) | related canonical coverage |
| 8 | Beta decomposition | SAI-BLK-20 | RF-20-02 | Asymmetric Beta — Upside Participation Ratio Below 0.7 | direct canonical coverage |
| 9 | Own-strength vs. beta-driven | SAI-BLK-20 | RF-20-02 | Asymmetric Beta — Upside Participation Ratio Below 0.7 | related canonical coverage |
| 10 | Peer financial divergence | SAI-BLK-21 | RF-21-01 | Fundamental Divergence Exceeding 2 Standard Deviations from Peer Median | direct canonical coverage |
| 11 | Peer valuation divergence | SAI-BLK-21 | RF-21-02 | Valuation Premium Exceeding 50% Above Peers Without Fundamental Justification | direct canonical coverage |

This artifact does NOT define red flags, assign RF IDs, or establish new red flag conditions. All canonical red flag definitions, evidence thresholds, temporal persistence rules, and severity assignments reside in the red flag taxonomy artifact.

(See: red_flag_taxonomy.md, Section: 5.19 SAI-BLK-19 Red Flags)
(See: red_flag_taxonomy.md, Section: 5.20 SAI-BLK-20 Red Flags)
(See: red_flag_taxonomy.md, Section: 5.21 SAI-BLK-21 Red Flags)

---

## 13. Explicit Prohibition Section

### 13.1 Prohibited Outputs

| # | Prohibited Item | Category | Reason |
|---|----------------|----------|--------|
| 1 | Peer ranking | Ranking | SAI observes relative position; it does not rank |
| 2 | Momentum score | Scoring | Relative strength is diagnostic context, not a numeric score |
| 3 | Factor model outputs | Methodology | Factor model construction is not SAI's domain |
| 4 | Statistical arbitrage signals | Trading | SAI does not produce trading signals |
| 5 | Pairs trading recommendations | Trading | Correlation observation does not imply tradeable relationships |
| 6 | Beta-based trading signals | Trading | Beta decomposition is context, not a signal |
| 7 | Peer group composition | Definition | SAI consumes peer groups; it does not define them |
| 8 | Peer selection methodology | Definition | Peer selection rules belong to the Peer Group Registry |
| 9 | Correlation calculation formulas | Methodology | Correlation computation belongs to the Correlation/Dependency Framework |
| 10 | Sector rotation recommendations | Recommendation | Sector-relative observation does not imply rotation advice |
| 11 | Buy/sell/hold based on relative strength | Decision | Relative strength informs context; it never instructs action |
| 12 | Expected return from beta exposure | Prediction | Beta observation does not imply return prediction |

### 13.2 Prohibited Language

**Ranking/scoring language** (forbidden):
- "best", "worst", "top-ranked", "bottom-ranked"
- "outperform candidate", "underperform candidate"
- "score", "rank", "alpha", "expected return"
- "conviction", "attractive", "unattractive"

**Trading/action language** (forbidden):
- "buy", "sell", "hold"
- "reduce exposure", "increase position"
- "avoid", "trading signal"
- "momentum play", "mean reversion trade"

**Methodology language** (forbidden):
- "our correlation model", "our beta estimate"
- "statistically significant" (SAI does not perform significance testing)
- "our peer selection", "we define peers as"
- "fair beta", "correct correlation"

### 13.3 Allowed Language

**Diagnostic context language** (allowed):
- "diagnostic relative strength context"
- "benchmark-relative behavior"
- "sector-relative behavior"
- "peer-relative observation"
- "correlation context"
- "beta-driven movement"
- "asset-specific movement"
- "requires review"
- "evidence limitation"
- "peer comparison unavailable without Peer Group Registry"
- "correlation regime context limited without Correlation/Dependency Framework"
- "drawdown context: market-wide / sector-wide / asset-specific"

(See: output_object_spec.md, Section: Prohibited Fields)
(See: requirements.md, Section: SAI-REQ-5 — Non-Scoring / Non-Recommendation Constraint)

---

## 14. Interpretation Dimension Coverage Summary

The following table summarizes all required interpretation dimensions per SAI-REQ-10 and their coverage within this artifact.

| # | Required Dimension | Covered In | Block |
|---|-------------------|-----------|-------|
| 1 | Relative strength vs. benchmark | Section 4.1 | SAI-BLK-19 |
| 2 | Relative strength vs. sector | Section 4.2 | SAI-BLK-19 |
| 3 | Relative strength vs. peers | Section 4.3 | SAI-BLK-19 |
| 4 | Correlation to benchmark | Section 5.1 | SAI-BLK-20 |
| 5 | Correlation to peers | Section 5.2 | SAI-BLK-20 |
| 6 | Beta decomposition | Section 5.3 | SAI-BLK-20 |
| 7 | Volatility | Section 4.4 | SAI-BLK-19 |
| 8 | Drawdown | Section 4.5 | SAI-BLK-19 |
| 9 | Own-strength vs. beta-driven movement | Section 5.4 | SAI-BLK-20 |

**Coverage confirmation**: All 9 interpretation dimensions required by SAI-REQ-10 are covered with diagnostic scope definitions, evidence consumption requirements, and deferred dependency documentation.

---

## 15. Relationship to Fact Consumption Matrix

The Market Position blocks consume the following fact category groups from the Market Evidence Framework:

| Block | Fact Category Groups Consumed |
|-------|------------------------------|
| SAI-BLK-19 | Price performance vs benchmark, sector performance, drawdown history |
| SAI-BLK-20 | Correlation coefficients, rolling beta, R-squared, factor exposures |
| SAI-BLK-21 | Peer financial metrics, market share, growth differentials, margin differentials |

SAI does not create these facts. It consumes them from the Market Evidence Framework via declarative consumption contracts.

(See: fact_consumption_matrix.md, Section: Market Position Block Mappings)

---

## 16. Relationship to Signal Consumption Matrix

The Market Position blocks consume the following signal categories:

| Block | Signal Categories Consumed |
|-------|---------------------------|
| SAI-BLK-19 | Relative strength signals, momentum signals, drawdown signals |
| SAI-BLK-20 | Correlation regime signals, beta decomposition signals |
| SAI-BLK-21 | Peer-relative comparison signals, competitive position signals |

SAI does not calculate these signals. It consumes them from the Market Evidence Framework via declarative consumption contracts.

(See: signal_consumption_matrix.md, Section: Market Position Signal Mappings)

---

## 17. Relationship to Output Object Specification

SAI-BLK-19, SAI-BLK-20, and SAI-BLK-21 produce output objects conforming to the canonical SAI output object specification. The peer/benchmark artifact adds the following constraints beyond standard output object rules:

1. The `interpretation_summary` field must identify the reference frame (benchmark, sector, or peer group) for every relative observation
2. The `evidence_completeness` field must be "insufficient" for SAI-BLK-21 when Peer Group Registry is unavailable
3. The `evidence_completeness` field should be "low" for SAI-BLK-20 when Correlation/Dependency Framework is unavailable
4. The `deferred_dependency_notes` field must document Peer Group Registry unavailability for SAI-BLK-21
5. The `deferred_dependency_notes` field must document Correlation/Dependency Framework unavailability for SAI-BLK-20
6. The `interpretation_summary` field must never contain any language from the prohibited list (Section 13.2)
7. Own-strength vs. beta-driven interpretation must be explicitly stated in SAI-BLK-20 output

(See: output_object_spec.md, Section: Allowed Fields)
(See: output_object_spec.md, Section: Prohibited Fields)

---

## 18. Relationship to Provenance Contract

All Market Position interpretations must satisfy the provenance contract:

- Every relative strength observation must trace to specific price/performance fact IDs
- Every correlation observation must trace to specific correlation coefficient fact IDs
- Every peer comparison must trace to specific peer financial metric fact IDs
- Timestamp inheritance applies — interpretations inherit temporal context from market data observation dates
- No orphan market position interpretations are valid
- Staleness thresholds for daily temporal class apply: stale after 2 days, expired after 5 days

Market Position blocks are particularly sensitive to evidence freshness because:
- Relative strength changes daily as market prices update
- Correlation regimes can shift rapidly during market stress
- Peer comparisons depend on both daily price data and quarterly fundamental data (hybrid freshness)

(See: provenance_contract.md, Section: Provenance Chain Specification)
(See: provenance_contract.md, Section: Timestamp Inheritance Rules)
(See: temporal_resolution_matrix.md, Section: Daily Temporal Class)

---

## 19. Relationship to Temporal Resolution Matrix

All three Market Position blocks have daily temporal class:

| Block | Temporal Class | Stale Threshold | Expired Threshold | Rationale |
|-------|---------------|-----------------|-------------------|-----------|
| SAI-BLK-19 | daily | 2 days | 5 days | Relative strength depends on daily price data |
| SAI-BLK-20 | daily | 2 days | 5 days | Correlation coefficients require daily return observations |
| SAI-BLK-21 | daily | 2 days | 5 days | Peer comparison includes daily market pricing context |

**Hybrid freshness note for SAI-BLK-21**: Peer comparison consumes both daily market data (price, returns) and quarterly fundamental data (margins, growth, leverage). The block follows daily temporal class for price-based comparisons, but fundamental peer metric comparisons inherit quarterly freshness from underlying filings.

(See: temporal_resolution_matrix.md, Section: Daily Temporal Class)

---

## 20. Acceptance Criteria Traceability

This section documents how each SAI-REQ-10 acceptance criterion is satisfied by this artifact.

| # | Acceptance Criterion | Artifact Section | Status |
|---|---------------------|-----------------|--------|
| 1 | Beta decomposition methodology documented (market, sector, idiosyncratic) | Section 5.3 — Beta Decomposition | Satisfied — market beta, sector beta, idiosyncratic component documented as interpretation dimensions |
| 2 | Relative strength interpretation defined for all three comparison levels (benchmark, sector, peers) | Sections 4.1, 4.2, 4.3 | Satisfied — all three reference frames covered |
| 3 | Correlation coefficient interpretation context defined per block | Sections 5.1, 5.2 | Satisfied — benchmark correlation and peer correlation context defined |
| 4 | Peer comparison explicitly requires a defined peer group — ad-hoc comparisons prohibited | Section 6.1, 6.2 | Satisfied — explicit prohibition with degradation rules |
| 5 | Peer groups declared as non-canonical until Peer Group Registry exists | Section 2 (Principle 2), Section 6.1, Section 10 | Satisfied — stated multiple times with handling rules |
| 6 | "Moves by own strength" vs. "moves by beta" distinction formally articulated | Section 2 (Principle 1), Section 5.4 | Satisfied — own-strength vs. beta-driven distinction is central |
| 7 | Drawdown analysis includes context (market-wide vs. sector-wide vs. asset-specific) | Section 4.5, Section 2 (Principle 5) | Satisfied — drawdown contextualization with three levels |

---

## 21. Verification Gate Evidence

### VG-SAI-1 (Requirements Completeness Gate) Evidence

This artifact provides evidence for VG-SAI-1 by demonstrating that all 3 Market Position blocks (SAI-BLK-19, SAI-BLK-20, SAI-BLK-21) are defined with stable identifiers, categories, purposes, fact families, signal families, temporal resolution, deferred dependencies, and boundary statements (Section 3).

### VG-SAI-4 (Interface Contract Gate) Evidence

This artifact provides supporting evidence for VG-SAI-4 by demonstrating that:
- The Peer Group Registry interface dependency is documented with graceful degradation rules (Section 10)
- The Correlation/Dependency Framework interface dependency is documented with graceful degradation rules (Section 11)
- Both dependencies reference the canonical interface contracts in deferred_interfaces.md

### VG-SAI-10 (Cross-Framework Consistency Gate) Evidence

This artifact provides supporting evidence for VG-SAI-10 by using consistent terminology with:
- Market Evidence Framework (fact/signal category names)
- Deferred Interfaces artifact (Peer Group Registry, Correlation/Dependency Framework)
- Block Taxonomy (block IDs, categories, names)
- Red Flag Taxonomy (canonical RF IDs)

**Explicit no-auto-completion statement**: This artifact provides EVIDENCE ONLY toward VG-SAI-1, VG-SAI-4, and VG-SAI-10. It does NOT execute or pass any verification gate. Gate execution requires separate, explicit Task 15 verification artifacts with PASS/FAIL evidence.

(See: tasks.md, Section: 15.1 Execute VG-SAI-1)
(See: tasks.md, Section: 15.4 Execute VG-SAI-4)
(See: tasks.md, Section: 15.10 Execute VG-SAI-10)

---

## 22. No-Drift Statement

This artifact is a definition-layer document. It has been verified to contain:

- ✓ Zero implementation code
- ✓ Zero peer selection algorithms or peer group creation
- ✓ Zero correlation calculation formulas or factor model methodology
- ✓ Zero beta calculation procedures or statistical significance methodology
- ✓ Zero scoring, ranking, or recommendation logic
- ✓ Zero allocation decisions or position sizing
- ✓ Zero trading signals or buy/sell/hold instructions
- ✓ Zero registry or SSOT mutations
- ✓ Zero fact/signal/evidence primitive creation
- ✓ Zero asset-to-narrative mappings
- ✓ Zero red flag creation — all references point to canonical red_flag_taxonomy.md
- ✓ All cross-references in canonical (See: [Deliverable], Section: [Title]) format
- ✓ Peer groups documented as non-canonical until Peer Group Registry exists
- ✓ SAI consumes peer definitions; it does not create them

If scope pressure toward peer group creation, correlation formula definition, factor model construction, or trading signal generation is detected during future task execution, this artifact must be consulted as the authoritative boundary reference for relative market position interpretation within SAI.

---

*End of artifact.*
