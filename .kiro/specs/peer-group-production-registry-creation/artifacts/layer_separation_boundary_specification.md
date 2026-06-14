# Layer Separation and Boundary Specification

> **Spec**: peer-group-production-registry-creation | **Task**: 3
> **Date**: 2026-06-14 | **Authority**: CTO / Architecture
> **Status**: DOCUMENTATION_ONLY

---

## Purpose

This artifact defines the explicit architectural layer boundaries showing what the Peer Group Production Registry owns versus what belongs to other Portfolio OS layers. It establishes prohibited cross-layer behaviors, schema boundaries, correlation calculation prohibitions, dependency boundaries, and No-Authority-Simulation rules.

This artifact is documentation only. It does not create registry content, execute calculations, or activate any system.

---

## 1. Layer Separation Table

The following table defines all 10 architectural layers within the Portfolio OS architecture, their ownership, responsibilities, and interaction mode with the Peer Group Production Registry.

| # | Layer | Owner | Responsibility | Registry Interaction |
|---|-------|-------|---------------|---------------------|
| 1 | Asset Registry / Watchlist | Asset identity layer | Canonical asset identity (ISIN, FIGI, legal entity) | Registry references identity; does not own it |
| 2 | Peer Group Registry | THIS DESIGN | Peer comparability, structural context, family/subcluster | Owns peer assignments and structural relationships |
| 3 | Portfolio State | Portfolio State layer | Holdings, weights, exposures, NAV | Consumes registry as read-only context |
| 4 | Signal Engines | Signal layer | Signal activation and calculation | Does not consume registry directly |
| 5 | Semantic Interpretation | Semantic layer | Meaning derivation from signals/context | May consume registry structure; does not modify it |
| 6 | PM Reasoning | Reasoning layer | Investment interpretation | May consume registry context for explanations |
| 7 | Report Rendering | Rendering layer | Human-readable output | May present registry context; owns language |
| 8 | Action Space | Action layer | Possible action framing | May reference peer context; does not get actions from registry |
| 9 | SAI | Intelligence framework | Deferred peer interface consumption | Read-only consumer through contract boundary |
| 10 | Trading/Execution | OUT OF SCOPE | Prohibited | No interaction whatsoever |

---

## 2. Layer Boundary Detail — What Each Layer Owns and Does NOT Own

### 2.1 Asset Registry / Watchlist

| Aspect | Detail |
|--------|--------|
| **Owns** | Canonical asset identity (ISIN, FIGI, exchange listing, legal entity), asset type classification, instrument metadata |
| **Does NOT own** | Peer comparability, peer role assignments, family membership, subcluster assignments |
| **Interaction with Registry** | Registry references canonical asset identity via `canonical_object_id`; registry does not duplicate or override identity fields |
| **Prohibited behaviors** | Registry must not become the asset registry; must not override identity fields; must not compete with asset identity ownership |

### 2.2 Peer Group Registry (THIS DESIGN)

| Aspect | Detail |
|--------|--------|
| **Owns** | Peer group family definitions (PGF-01 through PGF-09, future PGF-10), peer role assignments, subcluster assignments, structural relationships, dependency relationships (structural context only), regional comparability caveats, structural break caveats, source authority traceability, canonical peer_group_id values (when minted after approval), production authority and lifecycle state |
| **Does NOT own** | Asset identity, portfolio holdings, market data, trading signals, scores/rankings, semantic conclusions, report text, statistical calculations, portfolio health metrics |
| **Interaction with Registry** | IS the registry — defines and governs all peer comparability content |
| **Prohibited behaviors** | Must not calculate correlations, beta, covariance, factor exposure; must not produce scores, rankings, or recommendations; must not generate semantic conclusions or PM reasoning |

### 2.3 Portfolio State

| Aspect | Detail |
|--------|--------|
| **Owns** | Holdings, weights, exposures, NAV, position state, return attributions |
| **Does NOT own** | Peer group assignments, comparability context, family/subcluster definitions |
| **Interaction with Registry** | Consumes registry as read-only context for position interpretation and exposure analysis |
| **Prohibited behaviors** | Registry must not calculate or store portfolio state values; no circular dependency where registry depends on portfolio state |

### 2.4 Signal Engines

| Aspect | Detail |
|--------|--------|
| **Owns** | Signal activation, signal calculation, rolling correlations, momentum signals, regime detection |
| **Does NOT own** | Peer comparability, structural context, family membership |
| **Interaction with Registry** | Does not consume registry directly; operates on market data and portfolio state |
| **Prohibited behaviors** | Registry must not produce signal activation; must not calculate rolling correlations or momentum outputs |

### 2.5 Semantic Interpretation

| Aspect | Detail |
|--------|--------|
| **Owns** | Meaning derivation from signals and context, semantic state activation, narrative conclusions |
| **Does NOT own** | Structural peer assignments, family definitions, registry content |
| **Interaction with Registry** | May consume registry structure (peer roles, dependencies) as input; does not modify registry |
| **Prohibited behaviors** | Registry must not produce semantic conclusions; must not activate semantic states (e.g., dependency_elevated, concentration_risk_elevated) |

### 2.6 PM Reasoning

| Aspect | Detail |
|--------|--------|
| **Owns** | Investment interpretation, thesis evaluation, narrative generation for PM consumption |
| **Does NOT own** | Peer group definitions, structural context ownership, comparability rules |
| **Interaction with Registry** | May consume registry context for explanations and peer-comparison framing |
| **Prohibited behaviors** | Registry must not generate PM reasoning; must not produce investment thesis validation; must not imply buy/sell/hold conclusions |

### 2.7 Report Rendering

| Aspect | Detail |
|--------|--------|
| **Owns** | Human-readable output, language rendering, multilingual presentation, dashboard visualization |
| **Does NOT own** | Structural state values, peer assignments, comparability logic |
| **Interaction with Registry** | May present registry context in reports; owns language/localization |
| **Prohibited behaviors** | Registry must not embed natural-language narrative as structural values; must not render reports or dashboards |

### 2.8 Action Space

| Aspect | Detail |
|--------|--------|
| **Owns** | Possible action framing, action generation, buy/sell/size/rebalance options |
| **Does NOT own** | Peer comparability, structural context, family assignments |
| **Interaction with Registry** | May reference peer context for action boundaries; does not receive actions from registry |
| **Prohibited behaviors** | Registry must not generate actions; must not produce buy/sell instructions or position sizing |

### 2.9 SAI (Signal Architecture Interface)

| Aspect | Detail |
|--------|--------|
| **Owns** | Signal intelligence, deferred interface consumption, system-layer coordination |
| **Does NOT own** | Peer group content, registry governance, peer assignments |
| **Interaction with Registry** | Read-only consumer through contract boundary (deferred peer interfaces) |
| **Prohibited behaviors** | Registry must not mutate SAI; SAI must not write back to registry; no SAI artifact modification during registry creation |

### 2.10 Trading/Execution

| Aspect | Detail |
|--------|--------|
| **Owns** | OUT OF SCOPE — trading, brokerage, exchange connectivity, order routing, allocation, execution |
| **Does NOT own** | N/A — entirely out of scope for this architecture |
| **Interaction with Registry** | **No interaction whatsoever** — absolute prohibition |
| **Prohibited behaviors** | Any connection, reference, or data flow between registry and trading/execution is absolutely prohibited |

---

## 3. Prohibited Cross-Layer Behaviors Table

The following table explicitly lists behaviors that are prohibited across architectural layer boundaries. Any violation constitutes a boundary breach.

| # | Prohibited Behavior | Source Layer | Target Layer | Violation Type |
|---|---------------------|-------------|--------------|----------------|
| 1 | Registry calculating statistical correlation | Peer Group Registry | Signal Engines / Correlation Engine | Calculation leakage |
| 2 | Registry calculating rolling correlation | Peer Group Registry | Signal Engines | Calculation leakage |
| 3 | Registry calculating beta or covariance | Peer Group Registry | Risk/Factor models | Calculation leakage |
| 4 | Registry calculating factor exposure | Peer Group Registry | Factor/Signal models | Calculation leakage |
| 5 | Registry calculating portfolio concentration | Peer Group Registry | Portfolio Health | Calculation leakage |
| 6 | Registry activating semantic states | Peer Group Registry | Semantic Interpretation | Reasoning leakage |
| 7 | Registry producing scores or rankings | Peer Group Registry | Scoring Methodology | Output leakage |
| 8 | Registry generating recommendations | Peer Group Registry | Action Space / PM Reasoning | Authority simulation |
| 9 | Registry inferring trading signals | Peer Group Registry | Signal Engines / Trading | Authority simulation |
| 10 | Registry calculating portfolio health | Peer Group Registry | Portfolio Health | Calculation leakage |
| 11 | Registry rendering report text | Peer Group Registry | Report Rendering | Rendering leakage |
| 12 | Registry generating PM interpretation | Peer Group Registry | PM Reasoning | Reasoning leakage |
| 13 | Registry producing action instructions | Peer Group Registry | Action Space | Authority simulation |
| 14 | Registry mutating SAI artifacts | Peer Group Registry | SAI | Mutation violation |
| 15 | Registry duplicating asset identity | Peer Group Registry | Asset Registry / Watchlist | Identity ownership violation |
| 16 | Registry storing portfolio holdings | Peer Group Registry | Portfolio State | Ownership violation |
| 17 | Registry embedding market data | Peer Group Registry | Signal Engines / Market Data | Scope violation |
| 18 | Registry connecting to trading systems | Peer Group Registry | Trading/Execution | Absolute prohibition |
| 19 | Registry producing expected returns | Peer Group Registry | All downstream | Authority simulation |
| 20 | Registry generating conviction scores | Peer Group Registry | Scoring / PM Reasoning | Authority simulation |
| 21 | Registry producing market regime conclusions | Peer Group Registry | Market Regime Framework | Calculation leakage |
| 22 | Registry producing dashboard rendering | Peer Group Registry | Report Rendering / Dashboard | Rendering leakage |
| 23 | Downstream systems modifying registry content | Any downstream | Peer Group Registry | Write-back violation |
| 24 | SAI writing back to registry | SAI | Peer Group Registry | Contract violation |

---

## 4. Registry Schema Boundaries

### 4.1 What the Registry Contains

The production registry schema contains the following and only the following:

| Category | Contents |
|----------|----------|
| Family definitions | Peer group family definitions (PGF-01 through PGF-09, future PGF-10) |
| Peer role assignments | core_peer, adjacent_peer, benchmark_context, etf_peer, excluded_non_peer, private_comparable_context |
| Subcluster assignments | Primary/secondary/dependency context per record |
| Regional comparability | Regional comparability caveats (LatAm, SE Asia, etc.) |
| Structural break caveats | Post-merger, spin-off, integration-period documentation |
| Source authority | Source authority traceability to PGMF and P1–P4 decision records |
| Dependency relationships | Structural context relationships only (10 governed types) |
| Canonical IDs | Canonical peer_group_id values (when minted after approval) |
| Production authority | Production authority and lifecycle state fields |

### 4.2 What the Registry Excludes

The production registry schema explicitly excludes the following:

| Category | Excluded Content | Owning Layer |
|----------|-----------------|--------------|
| Asset identity | ISIN, FIGI, exchange listing, legal entity | Asset Registry / Watchlist |
| Portfolio holdings | Holdings, weights, exposures, NAV | Portfolio State |
| Market data | Price information, volume, market feeds | Signal Engines / Market Data |
| Trading state | Trading signals, execution state, order routing | Trading/Execution (OUT OF SCOPE) |
| Scores/rankings | Asset scores, opportunity rankings, prioritization | Scoring Methodology |
| Semantic conclusions | PM interpretations, meaning derivation, narrative | Semantic Interpretation |
| Report text | Rendered narrative, human-readable output | Report Rendering |
| Statistical calculations | Correlation, beta, covariance, factor exposure | Correlation/Dependency Engine, Risk models |
| Portfolio health | Health metrics, concentration calculations | Portfolio Health Framework |
| Conviction/prediction | Confidence-as-prediction, expected returns, target prices | Prohibited everywhere |

---

## 5. No-Authority-Simulation Rules

### 5.1 Core Principle

The Peer Group Production Registry provides structured comparability context. It does NOT simulate, imply, or generate investment authority.

### 5.2 No-Authority-Simulation Declarations

| # | Declaration |
|---|-------------|
| 1 | The registry does NOT imply that a peer assignment is an investment recommendation |
| 2 | The registry does NOT imply that a comparable peer is a buy/sell/hold conclusion |
| 3 | The registry does NOT imply that peer group membership validates an investment thesis |
| 4 | The registry ONLY provides structured comparability context |
| 5 | Any downstream system consuming registry data is responsible for its own governance boundaries |
| 6 | No downstream system may attribute investment conclusions to the registry |

### 5.3 Downstream Responsibility Model

| Downstream Consumer | Responsibility |
|--------------------|---------------|
| Portfolio State | Owns its own position interpretation; registry provides context only |
| Semantic Reasoning | Owns its own conclusions; registry provides structure only |
| PM Reasoning | Owns its own thesis evaluation; registry provides comparability context only |
| Report Rendering | Owns its own language and presentation; registry provides structural tokens only |
| Action Space | Owns its own action generation; registry provides boundary context only |
| Opportunity Engine | Owns its own screening/ranking; registry provides family/peer context only |
| SAI | Owns its own signal intelligence; registry provides peer fields through contract only |
| Portfolio Health | Owns its own health calculations; registry provides dependency structure only |

### 5.4 Prohibited Authority Claims

The registry must never produce output that could be interpreted as:

- Investment recommendation (buy/sell/hold)
- Thesis validation or invalidation
- Conviction scoring
- Expected return generation
- Target price derivation
- Position sizing guidance
- Allocation recommendation
- Trading signal
- Opportunity ranking
- Portfolio action instruction

---

## 6. Correlation Calculation Prohibition Table

The following calculations are **absolutely prohibited** within the production registry and all tasks governed by this spec. Each calculation belongs to a specific downstream system that owns its execution.

| # | Prohibited Calculation | Owning System | Reason |
|---|----------------------|---------------|--------|
| 1 | Statistical correlation | Correlation/Dependency Engine | Requires market data and time-series analysis; belongs to engine layer |
| 2 | Rolling correlation | Signal Engines | Requires windowed time-series computation; belongs to signal layer |
| 3 | Beta | Risk/Factor models | Requires regression analysis against market factor; belongs to risk layer |
| 4 | Covariance | Risk/Factor models | Requires paired return series computation; belongs to risk layer |
| 5 | Factor exposure | Factor/Signal models | Requires multi-factor regression; belongs to factor analysis layer |
| 6 | Concentration calculation | Portfolio Health | Requires portfolio state + position sizing; belongs to health framework |
| 7 | Semantic dependency state activation | Semantic Reasoning | Requires interpretation engine; belongs to semantic layer |
| 8 | Scoring/ranking output | Scoring Methodology | Requires scoring rules and criteria; belongs to scoring framework |
| 9 | Recommendation output | Prohibited everywhere in registry | No system may produce recommendations through the registry |
| 10 | Portfolio health metrics | Portfolio Health Framework | Requires portfolio state integration; belongs to health framework |
| 11 | Market regime conclusions | Market Regime Framework | Requires market data analysis and regime detection; belongs to regime framework |
| 12 | Expected return generation | Prohibited everywhere in registry | No system may produce expected returns through the registry |

### 6.1 Why These Calculations Are Prohibited

The registry is a **structural intelligence layer**. It provides the context needed for downstream systems to perform their own calculations. The distinction is:

- **Registry provides**: "Asset A has a `supply_chain_dependency` relationship with Asset B" (structural fact)
- **Downstream calculates**: "The rolling correlation between A and B is 0.72" (statistical calculation)

The registry documents **what relationships exist**. Downstream systems determine **what those relationships mean quantitatively**.

### 6.2 Enforcement

- Verification Gate check M (No Correlation Output) validates zero statistical calculation outputs
- Verification Gate check N (No Semantic Activation) validates zero semantic state activations
- Verification Gate check O (No Scoring/Ranking) validates zero scoring or recommendation leakage
- Verification Gate check P (Boundary Compliance) validates all prohibited outputs are absent

---

## 7. Dependency Boundary Table

The following table defines what dependency-related behaviors are allowed versus prohibited within the registry.

### 7.1 Allowed Dependency Behaviors

| # | Allowed Behavior | Description |
|---|-----------------|-------------|
| 1 | Document structural relationships | Record that Asset A has a relationship of type X with Target B |
| 2 | Record source authority for relationships | Trace each relationship to PGMF or P1–P4 decision record |
| 3 | Preserve evidence_status per relationship | Track VERIFIED, INFERRED, or CONTEXT_ONLY status |
| 4 | Graph traversal by downstream systems | Downstream systems may traverse the dependency graph structure |
| 5 | Dependency visualization context | Provide structural data for dependency visualization tools |

### 7.2 Prohibited Dependency Behaviors

| # | Prohibited Behavior | Owning System | Why Prohibited |
|---|---------------------|---------------|----------------|
| 1 | Calculate statistical correlation | Correlation/Dependency Engine | Requires market data time-series; not structural context |
| 2 | Calculate rolling correlation | Signal Engines | Requires windowed computation; not structural context |
| 3 | Calculate beta or covariance | Risk/Factor models | Requires return-series regression; not structural context |
| 4 | Calculate factor exposure | Factor/Signal models | Requires multi-factor analysis; not structural context |
| 5 | Calculate concentration from dependencies | Portfolio Health | Requires portfolio state + weight data; not structural context |
| 6 | Activate semantic dependency states | Semantic Reasoning | Requires interpretation; not structural context |
| 7 | Produce scoring/ranking from graph | Scoring Methodology | Requires scoring criteria; not structural context |
| 8 | Generate recommendation from dependencies | Prohibited | No recommendations from registry under any circumstance |
| 9 | Infer trading signals from structure | Signal Engines / Trading | Structural context is not a signal; no trading signals permitted |
| 10 | Calculate portfolio health from dependencies | Portfolio Health Framework | Requires health calculation engine; not structural context |

### 7.3 The Boundary Principle

The registry provides **graph-readable structural context**. It documents edges (relationships) and nodes (assets, families, themes, etc.) with metadata (type, direction, evidence, confidence). It does NOT execute graph algorithms, produce centrality scores, calculate shortest paths, determine clustering coefficients, or derive any quantitative output from the graph structure.

Downstream systems that consume the dependency graph are responsible for:
- Their own graph algorithms
- Their own quantitative calculations
- Their own interpretive conclusions
- Their own governance boundaries

---

## 8. Requirements Traceability

| Requirement | Coverage in This Artifact |
|-------------|--------------------------|
| R13 (Output Restrictions) | Sections 3, 4.2, 6, 7.2 — all prohibited outputs explicitly listed |
| R17 (Trading and Market Data Boundary) | Sections 2.10, 3 (#18), 4.2 — absolute prohibition documented |
| R27 (Portfolio OS Scope Preservation) | Sections 2.1–2.10, 5 — each layer's scope bounded |
| R28 (Registry Layer Separation) | Sections 1, 2 — all 10 layers documented with ownership |
| R29 (No Authority Simulation) | Section 5 — full No-Authority-Simulation rules |

---

## 9. Boundary Confirmations

- ✓ All 10 layers from design.md documented with explicit boundaries
- ✓ Prohibited cross-layer behaviors explicitly listed (24 items)
- ✓ Registry schema boundaries defined (contains vs excludes)
- ✓ No-Authority-Simulation rules confirmed (6 declarations)
- ✓ Correlation Calculation Prohibition Table present (12 prohibited calculations)
- ✓ Dependency Boundary Table present (5 allowed, 10 prohibited behaviors)
- ✓ No calculations implemented
- ✓ No registry content created
- ✓ No runtime code produced
- ✓ Documentation only

---

## Controlling Sources

- design.md Section 5 (Layer Separation Diagram)
- design.md Section 6 (Registry Schema Boundaries)
- design.md Section 15 (Dependency Boundary Table)
- design.md Section 16 (Correlation Calculation Prohibition Table)
- design.md Section 25 (No-Authority-Simulation)
- requirements.md R13, R17, R27, R28, R29

---

```
LAYER_SEPARATION_BOUNDARY_SPECIFICATION_COMPLETE
```

---

*End of layer separation and boundary specification.*
