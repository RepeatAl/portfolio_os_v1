# Dependency Types v2

---
artifact_id: dependency_types_v2_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines the 10 canonical dependency types that classify causal connections in the Organism_Graph
ssot_relationship: canonical
topic: dependency_type_classification
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_principles_md, state_change_taxonomy_md, temporal_taxonomy_md]
---

## Scope Statement

This document defines the formal classification of all Dependency_Types in the Market Organism Framework. It establishes exactly ten canonical types that classify the causal connections (edges) in the Organism_Graph — the mechanisms through which State_Changes propagate from source to target. Each type is defined by its causal channel, propagation mechanism, directionality, and temporal profile. This document does NOT contain engines, code, scores, weights, probabilities, asset lists, correlation matrices, dashboards, or any executable logic.

---

## Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary

This document does not define terms. It consumes them.

---

## Type Enumeration

The Dependency_Type taxonomy contains exactly ten types. Each represents a fundamentally distinct causal mechanism through which a State_Change at one node produces an effect at another node in the Organism_Graph.

| # | Dependency_Type | Canonical ID | Causal Channel | Directionality |
|---|----------------|-------------|----------------|----------------|
| 1 | Price | `dep.price` | Economic | Unidirectional |
| 2 | Fundamental | `dep.fundamental` | Economic | Unidirectional |
| 3 | Narrative | `dep.narrative` | Informational | Bidirectional |
| 4 | Flow | `dep.flow` | Economic | Unidirectional |
| 5 | Ownership | `dep.ownership` | Structural | Bidirectional |
| 6 | Supply_Chain | `dep.supply_chain` | Structural | Unidirectional |
| 7 | Macro | `dep.macro` | Economic | Unidirectional |
| 8 | Behavioral | `dep.behavioral` | Informational | Conditional |
| 9 | Regulatory | `dep.regulatory` | Structural | Conditional |
| 10 | Butterfly | `dep.butterfly` | Informational | Conditional |

---

## Differentiation Matrix

No two types share identical causal channel + directionality + propagation characteristics. The following matrix confirms uniqueness:

| Canonical ID | Channel | Directionality | Distinguishing Propagation |
|-------------|---------|----------------|---------------------------|
| `dep.price` | Economic | Unidirectional | Market price transmission between traded instruments |
| `dep.fundamental` | Economic | Unidirectional | Business metric causation through operational linkage |
| `dep.narrative` | Informational | Bidirectional | Belief and theme propagation through shared interpretation |
| `dep.flow` | Economic | Unidirectional | Capital movement between pools and instruments |
| `dep.ownership` | Structural | Bidirectional | Legal or equity relationship creating mutual exposure |
| `dep.supply_chain` | Structural | Unidirectional | Physical or service delivery dependency |
| `dep.macro` | Economic | Unidirectional | Policy or regime transmission across economic system |
| `dep.behavioral` | Informational | Conditional | Sentiment or herding behavior contingent on market state |
| `dep.regulatory` | Structural | Conditional | Rule or compliance imposition contingent on threshold breach |
| `dep.butterfly` | Informational | Conditional | Non-obvious cross-domain propagation through indirect channels |

**Uniqueness Verification**: Each row has a unique combination of {Channel, Directionality, Distinguishing Propagation}. Within the same Channel+Directionality group, the propagation mechanism is distinct:
- Economic + Unidirectional: Price (market price), Fundamental (business metrics), Flow (capital movement), Macro (policy regime) — four distinct mechanisms
- Informational + Bidirectional: Narrative (belief systems) — unique
- Structural + Bidirectional: Ownership (legal/equity) — unique
- Structural + Unidirectional: Supply_Chain (physical delivery) — unique
- Informational + Conditional: Behavioral (sentiment/herding), Butterfly (cross-domain indirect) — distinct triggers
- Structural + Conditional: Regulatory (rule imposition) — unique

---

## Type Definitions


### Price

`dep.price`

**Causal Channel**: Economic

**Propagation Mechanism**: A State_Change at the source entity alters its market price, which directly transmits to the target entity's market price through arbitrage relationships, benchmark pricing, or derivative linkage. The causal channel is the price discovery mechanism itself — the target's price adjusts BECAUSE the source's price changed, through an identifiable market microstructure connection.

**Directionality**: Unidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Price dependencies typically exhibit the shortest Latency (Day) among all types due to continuous market pricing, with Duration varying by the persistence of the source State_Change.

**Example**:
- Source: Brent Crude Oil futures
- Target: Jet fuel spot price
- Mechanism: Jet fuel is refined from crude oil; its production cost floor is set by crude input price. When Brent rises due to an Oil Shock (State_Change), jet fuel spot price adjusts upward through the refining cost transmission channel.

**Differentiation**: Distinguished from `dep.fundamental` by operating through market price transmission rather than business metric causation. Price dependency requires both source and target to be priced instruments connected through a pricing mechanism. Fundamental dependency operates through operational metrics (revenue, margin, volume) that may or may not immediately reflect in price.

---

### Fundamental

`dep.fundamental`

**Causal Channel**: Economic

**Propagation Mechanism**: A State_Change at the source entity alters a business metric (revenue, margin, volume, cost structure) at the target entity through an operational linkage. The causal channel is the business relationship itself — the target's fundamentals change BECAUSE the source's operational reality changed, through an identifiable commercial or operational connection.

**Directionality**: Unidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Fundamental dependencies typically exhibit Latency of Week to Quarter, as business metric changes require operational cycles (reporting periods, contract renewals, production cycles) to manifest at the target.

**Example**:
- Source: Apple iPhone unit sales
- Target: TSMC advanced node utilization rate
- Mechanism: Apple is TSMC's largest customer for advanced process nodes. When Apple's iPhone sales guidance rises (Corporate State_Change: `sc.corporate.guidance`), TSMC's fab utilization increases because Apple orders more chips through their manufacturing agreement.

**Differentiation**: Distinguished from `dep.price` by operating through business metric causation rather than market price transmission. The source need not be a priced instrument — it can be any operational metric. The effect manifests in the target's fundamentals (revenue, utilization, margin) before necessarily appearing in market price.

---

### Narrative

`dep.narrative`

**Causal Channel**: Informational

**Propagation Mechanism**: A State_Change at the source entity alters the prevailing market belief system or investment theme, which propagates to the target entity through shared narrative membership. The causal channel is collective interpretation — the target is affected BECAUSE market participants update their beliefs about a theme that encompasses both source and target, through the informational network of analysis, media, and consensus formation.

**Directionality**: Bidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Narrative dependencies exhibit variable Latency (Day to Month) depending on the speed of consensus formation, with potentially long Duration as narratives persist across market cycles.

**Example**:
- Source: Nvidia data center revenue acceleration
- Target: Broadcom custom AI chip program perception
- Mechanism: Nvidia's results strengthen the "AI Infrastructure" narrative (`sc.narrative.ai`). Market participants update their beliefs about AI infrastructure spending broadly, which elevates perception of Broadcom's custom AI chip business through shared narrative membership. The effect is bidirectional: Broadcom's AI wins also reinforce the narrative that benefits Nvidia.

**Differentiation**: Distinguished from `dep.behavioral` by operating through belief and theme propagation rather than sentiment-driven herding. Narrative dependency requires shared membership in an identifiable investment theme. Behavioral dependency operates through crowd psychology and imitation regardless of thematic connection.


---

### Flow

`dep.flow`

**Causal Channel**: Economic

**Propagation Mechanism**: A State_Change at the source entity triggers capital movement (inflows or outflows) that directly affects the target entity's liquidity, valuation, or funding conditions. The causal channel is the movement of money itself — the target is affected BECAUSE capital physically relocates from one pool to another, through identifiable fund flows, rebalancing mechanics, or allocation shifts.

**Directionality**: Unidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Flow dependencies typically exhibit Latency of Day to Week for liquid markets (ETF rebalancing, margin calls) and Week to Month for institutional allocation shifts (mandate changes, fund redemptions).

**Example**:
- Source: Emerging market sovereign risk event
- Target: US Treasury demand
- Mechanism: A sovereign stress event in emerging markets triggers capital flight. Institutional investors redeem EM allocations and redirect capital to US Treasuries as a safe haven. The target (US Treasury demand) increases BECAUSE capital physically moves from EM pools to US fixed income pools through fund flow mechanics.

**Differentiation**: Distinguished from `dep.price` by operating through capital movement rather than price transmission. Price dependency connects two instruments through a pricing mechanism (arbitrage, benchmark). Flow dependency connects two pools through capital reallocation — the target's conditions change because money arrived or departed, not because a related price changed.

---

### Ownership

`dep.ownership`

**Causal Channel**: Structural

**Propagation Mechanism**: A State_Change at the source entity propagates to the target entity through a legal or equity relationship that creates mutual exposure. The causal channel is the ownership structure itself — the target is affected BECAUSE it shares a parent entity, subsidiary relationship, joint venture, or significant equity stake with the source, creating structural coupling that transmits operational and financial effects.

**Directionality**: Bidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Ownership dependencies exhibit Latency of Day to Week for publicly disclosed relationships (consolidated reporting, dividend flows) and Week to Quarter for structural effects (capital allocation decisions, strategic pivots propagating through corporate hierarchy).

**Example**:
- Source: Alphabet corporate restructuring decision
- Target: Waymo autonomous vehicle program
- Mechanism: Alphabet's decision to restructure its "Other Bets" segment directly affects Waymo's funding, strategic direction, and operational independence through the parent-subsidiary ownership relationship. Conversely, Waymo's progress (or lack thereof) affects Alphabet's consolidated results and capital allocation decisions. The bidirectional structural coupling means State_Changes propagate in both directions through the ownership link.

**Differentiation**: Distinguished from `dep.supply_chain` by operating through legal/equity relationships rather than physical or service delivery. Ownership dependency requires a formal structural relationship (parent, subsidiary, significant stake). Supply_Chain dependency operates through commercial delivery relationships that exist independently of ownership structure.

---

### Supply_Chain

`dep.supply_chain`

**Causal Channel**: Structural

**Propagation Mechanism**: A State_Change at the source entity propagates to the target entity through a physical goods delivery or service provision relationship. The causal channel is the delivery dependency itself — the target is affected BECAUSE it relies on the source for inputs (components, materials, services) that are necessary for its operations, creating a structural dependency on the source's ability to deliver.

**Directionality**: Unidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Supply_Chain dependencies typically exhibit Latency of Week to Quarter, reflecting physical delivery lead times, inventory buffer depletion, and the time required for supply disruptions to propagate through production schedules.

**Example**:
- Source: ASML EUV lithography machine production
- Target: TSMC advanced node capacity expansion
- Mechanism: TSMC's ability to expand its most advanced manufacturing nodes depends on receiving EUV lithography machines from ASML. A State_Change affecting ASML's production capacity (e.g., component shortage, factory disruption) directly constrains TSMC's capacity expansion timeline through the physical delivery dependency. TSMC cannot substitute this input from another supplier.

**Differentiation**: Distinguished from `dep.ownership` by operating through commercial delivery relationships rather than legal/equity structure. Supply_Chain dependency exists between entities that have no ownership relationship — it is the physical or service delivery link that creates the structural coupling. Two entities can have a Supply_Chain dependency without any equity stake connecting them.


---

### Macro

`dep.macro`

**Causal Channel**: Economic

**Propagation Mechanism**: A State_Change at the source entity (a macroeconomic policy decision or regime shift) propagates to the target entity through the transmission mechanisms of the broader economic system. The causal channel is the policy or regime transmission itself — the target is affected BECAUSE it operates within an economic environment whose fundamental parameters (interest rates, liquidity conditions, regulatory regime, fiscal stance) have been altered by the source, creating system-wide effects that reach the target through economic transmission channels.

**Directionality**: Unidirectional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Macro dependencies exhibit variable Latency depending on the transmission channel: Day for rate-sensitive instruments, Month to Quarter for real economy effects, and Quarter to Year for structural regime changes to fully propagate through the economic system.

**Example**:
- Source: Federal Reserve rate hike cycle initiation
- Target: US housing market activity
- Mechanism: The Fed's decision to raise rates (`sc.macro.rates`) transmits through the economic system via the mortgage rate channel. Higher policy rates propagate to higher mortgage rates through the banking system's cost of funds, which reduces housing affordability and suppresses transaction volume. The target is affected through the macroeconomic transmission mechanism, not through any direct commercial or ownership relationship with the Fed.

**Differentiation**: Distinguished from `dep.price` by operating through policy or regime transmission across the economic system rather than direct market price linkage between instruments. Macro dependency connects a policy-level source to a downstream target through systemic transmission channels. Price dependency connects two traded instruments through a direct pricing mechanism. The Fed rate decision is not "priced" in the same sense as Brent Crude — it transmits through the economic system's plumbing.

---

### Behavioral

`dep.behavioral`

**Causal Channel**: Informational

**Propagation Mechanism**: A State_Change at the source entity propagates to the target entity through crowd psychology, sentiment contagion, or herding behavior among market participants. The causal channel is the behavioral response itself — the target is affected BECAUSE market participants observe the source's State_Change and respond with imitative or reactive behavior that spills over to the target, CONDITIONAL on the prevailing market psychological state (fear, greed, complacency).

**Directionality**: Conditional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Behavioral dependencies exhibit highly variable Latency (Day to Week) that is conditional on market psychological state. In high-fear environments, behavioral contagion propagates within hours. In complacent environments, the same source State_Change may produce no behavioral spillover at all.

**Example**:
- Source: High-profile hedge fund liquidation announcement
- Target: Similar-strategy fund redemption pressure
- Mechanism: When a prominent fund announces forced liquidation, market participants observe this and behaviorally extrapolate risk to funds with similar strategies. Redemption requests increase at peer funds not because of any operational linkage, but because investors herd toward the exit based on pattern-matching and fear contagion. This propagation is CONDITIONAL — it occurs primarily in elevated-fear market states and may not activate during calm periods.

**Differentiation**: Distinguished from `dep.narrative` by operating through sentiment-driven herding rather than belief and theme propagation. Narrative dependency requires shared membership in an identifiable investment theme and operates through consensus formation about that theme. Behavioral dependency operates through crowd psychology and imitation regardless of thematic connection — the trigger is "others are doing X, so I should too" rather than "the narrative about theme Y has changed."

---

### Regulatory

`dep.regulatory`

**Causal Channel**: Structural

**Propagation Mechanism**: A State_Change at the source entity (a regulatory body, legislative action, or compliance framework change) propagates to the target entity through the imposition or modification of rules, requirements, or constraints. The causal channel is the regulatory authority itself — the target is affected BECAUSE a governing body has altered the rules under which the target operates, CONDITIONAL on the target meeting specific threshold criteria (size, jurisdiction, activity type) that bring it within the regulation's scope.

**Directionality**: Conditional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Regulatory dependencies exhibit Latency of Month to Year, reflecting legislative timelines, comment periods, implementation deadlines, and compliance phase-in schedules. Duration is typically long (Year or longer) as regulatory changes tend to persist until explicitly reversed.

**Example**:
- Source: EU AI Act passage into law
- Target: US technology companies with EU operations
- Mechanism: The EU's legislative action imposes compliance requirements on AI systems deployed within EU jurisdiction. US technology companies are affected CONDITIONAL on having EU operations that deploy AI systems meeting the Act's risk classification thresholds. Companies below the threshold or without EU operations are not affected by this Dependency_Path. The propagation is structural — it operates through legal authority, not market mechanics.

**Differentiation**: Distinguished from `dep.supply_chain` by operating through rule imposition rather than physical delivery. Supply_Chain dependency creates coupling through the need for inputs. Regulatory dependency creates coupling through the authority to impose constraints. The source in a Regulatory dependency is always a rule-making body or framework, never a commercial counterparty.

---

### Butterfly

`dep.butterfly`

**Causal Channel**: Informational

**Propagation Mechanism**: A State_Change at the source entity propagates to the target entity through a non-obvious, cross-domain informational channel that is not immediately apparent from the entities' surface characteristics. The causal channel is an indirect informational linkage — the target is affected BECAUSE the source's State_Change reveals or alters information that, through a chain of non-obvious logical connections, changes the conditions relevant to the target. This propagation is CONDITIONAL on specific contextual circumstances that activate the indirect channel.

**Directionality**: Conditional

**Typical Temporal Profile**: (See: README_temporal_taxonomy, Section: Latency Definition) — Butterfly dependencies exhibit highly variable Latency (Day to Quarter) depending on how quickly market participants recognize the non-obvious connection. Duration is often short once the connection is recognized and priced, but can be long if the indirect channel creates persistent structural effects.

**Example**:
- Source: World Cup tournament hosted in Qatar (winter scheduling)
- Target: European natural gas storage levels
- Mechanism: The World Cup's winter scheduling in Qatar (`sc.events.sporting_events`) causes a shift in global media and political attention patterns. This attention shift reduces political pressure on European energy policy during a critical storage-building period, which indirectly affects the pace of natural gas procurement decisions. The connection is non-obvious — sporting events and energy storage have no direct commercial, ownership, or price linkage. The propagation is CONDITIONAL on the specific geopolitical context (European energy crisis) that activates this indirect informational channel.

**Differentiation**: Distinguished from `dep.behavioral` by operating through non-obvious cross-domain informational channels rather than sentiment-driven herding. Behavioral dependency operates through crowd psychology where participants imitate each other within a recognizable domain. Butterfly dependency operates through indirect logical connections across domains that are not immediately apparent — the source and target appear unrelated on the surface, and the causal channel requires multi-step reasoning to identify.


---

## Multi-Type Edges

When a single Dependency_Path between two nodes exhibits characteristics of more than one Dependency_Type, the following coexistence rules apply.

### Rules

1. Multiple Dependency_Types on a single path are UNORDERED (no inherent priority among co-existing types)
2. One type MAY be designated PRIMARY based on which causal channel dominates the observed propagation
3. Combined types inherit the SHORTEST Latency and LONGEST Duration from constituent types
4. Amplification/Dampening are assessed for the combined effect, not per-type

### Rationale

Coexistence rules prevent false precision. Assigning priority would require scoring — which is prohibited. Instead, the PRIMARY designation is a qualitative judgment about which causal channel carries the dominant explanatory weight for a given path.

### Example

Path: Federal Reserve Rate Decision → US Regional Bank Earnings

- Primary Type: `dep.macro` (dominant causal channel — policy regime transmission through the banking system's cost of funds)
- Secondary Type: `dep.fundamental` (contributing mechanism — altered net interest margins affect reported earnings through operational linkage)
- Combined Temporal: Latency = Day (shortest, from `dep.macro` rate-sensitive instruments), Duration = Year (longest, from `dep.fundamental` multi-quarter earnings impact), Amplification = assessed for combined effect on bank profitability, Dampening = assessed for combined effect as rate environment normalizes

### Designation Criteria

The PRIMARY type is determined by answering: "Through which causal channel does the MAJORITY of the propagated effect travel?" This is a qualitative assessment, not a numeric weighting. If no channel clearly dominates, no PRIMARY designation is required — the types simply coexist as unordered.

---

## Dependency vs. Correlation

### Definition

- **Dependency**: A causal propagation mechanism where a State_Change at source PRODUCES an effect at target through an identifiable channel. The mechanism is nameable, the direction is specified, and the propagation survives regime changes if the mechanism persists.

- **Correlation**: Statistical co-movement where two entities move together without an identifiable causal mechanism connecting them. No direction is specified, no mechanism is named, and the relationship breaks down unpredictably when market regimes change.

### Distinguishing Criteria

| Property | Dependency | Correlation |
|----------|-----------|-------------|
| Causal direction | Specified (A → B) | Not specified |
| Mechanism | Identified and nameable | Not identified |
| Regime resilience | Survives if mechanism persists | Breaks down unpredictably |
| Explanatory power | Answers "why" and "how" | Answers only "how often together" |
| Framework role | Valid edge in Organism_Graph | NOT a valid edge — prohibited as substitute |

### Contrastive Example

Entity Pair: US Dollar Index and Emerging Market Sovereign Bonds

**AS CORRELATION**: "The Dollar Index and EM sovereign bonds move inversely together with a statistical relationship observed in historical data"
  - No causal direction specified
  - No mechanism identified
  - Breaks down when regime changes (e.g., during periods of synchronized global easing where both strengthen)
  - Cannot explain WHY the relationship exists
  - Cannot predict WHEN the relationship will fail

**AS TYPED DEPENDENCY**: "A State_Change in US Dollar strength (`sc.macro.fx`) propagates to Emerging Market sovereign bond conditions through `dep.macro` because dollar strengthening increases the real debt burden for EM sovereigns with dollar-denominated obligations, triggering capital outflows through `dep.flow` as investors reassess credit risk"
  - Causal direction: US Dollar → EM Sovereign Bonds
  - Mechanism: Dollar-denominated debt burden + capital flow reallocation
  - Predictive: survives regime changes if the mechanism persists (EM sovereigns still have dollar debt)
  - Explains WHY: the debt denomination creates structural vulnerability
  - Identifies WHEN it fails: if EM sovereigns eliminate dollar-denominated debt, the mechanism dissolves

### Implication for the Organism_Graph

Correlation matrices are explicitly prohibited as substitutes for Dependency_Paths in the Organism_Graph. Every edge must carry a named Dependency_Type with an identifiable causal mechanism. "These two things move together" is never sufficient justification for an edge.

(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)

---

## Exclusion Constraints

This section consolidates all prohibitions applicable to this deliverable and its usage.

### Prohibited Content

| # | Prohibition | Rationale |
|---|------------|-----------|
| 1 | Engine implementations, Python code, or executable logic | This is a definition document, not an implementation |
| 2 | Scoring algorithms, numeric weights, probabilities, ranking systems, or quantitative models | Weights on an incomplete model produce false confidence |
| 3 | Dashboard designs, report templates, or visualization specifications | Belongs to future implementation phases |
| 4 | Asset lists or ticker symbols as root-level entities | Assets are leaf nodes, never root nodes — the primitive chain is preserved |
| 5 | Correlation matrices or statistical co-movement measures as substitutes for causal Dependency_Paths | Correlation is not causation; every edge requires an identifiable mechanism |

### Unified Rationale

**Weights on an incomplete model produce false confidence.**

The Market Organism Framework defines the conceptual territory. Assigning numeric values to dependency strengths, path probabilities, or type priorities would create an illusion of precision that the definition layer cannot support. Mathematics belongs to future implementation phases (P0, P1, P2, P3) where engines can validate quantitative claims against observed data.

### What IS Permitted

- Qualitative descriptors (e.g., Latency: Month, Amplification: High)
- Structural classifications (e.g., Causal Channel: Economic)
- Enumerated categories (e.g., Directionality: Conditional)
- Concrete examples using real market entities for illustration
- Cross-references to other deliverables

### Enforcement

Any content matching the prohibited categories above constitutes a validation error and must be removed or reformulated before the deliverable is considered complete.

---

## Extension Criteria

### Adding a New Dependency_Type (11th or Beyond)

A proposed new Dependency_Type may be added to this taxonomy ONLY IF it satisfies ALL of the following criteria:

#### 1. Unique Combination Requirement

The proposed type must have a unique combination of:
- **Causal Channel** (Economic, Informational, or Structural)
- **Directionality** (Unidirectional, Bidirectional, or Conditional)
- **Propagation Characteristics** (the specific mechanism by which State_Changes transmit)

The new type MUST NOT share an identical {Channel + Directionality + Propagation} signature with any of the existing 10 types. Refer to the Differentiation Matrix above to verify uniqueness.

#### 2. Mechanism Description Requirement

The proposed type must include a complete Propagation Mechanism description that:
- Identifies the specific causal channel through which effects transmit
- Explains HOW a State_Change at source produces an effect at target
- Is distinguishable from all existing mechanism descriptions

#### 3. Concrete Example Requirement

The proposed type must include at least one concrete example containing:
- Source entity (with canonical ID if applicable)
- Target entity (with canonical ID if applicable)
- Specific mechanism connecting them through the proposed type
- Explanation of why this example cannot be classified under any existing type

#### 4. Differentiation Demonstration

The proposed type must explicitly demonstrate differentiation from the most similar existing type by:
- Naming the most similar existing type
- Explaining the specific distinction in causal channel, directionality, or propagation
- Providing a scenario where the two types would produce different classifications for the same entity pair

#### 5. Format Compliance

The new type definition must follow the established format:
- Canonical ID (e.g., `dep.new_type_name`)
- Causal Channel
- Propagation Mechanism
- Directionality
- Typical Temporal Profile (cross-reference to Temporal_Taxonomy)
- Example (source, target, mechanism)
- Differentiation statement

---

## Explanation Readiness

### Edge Label Traversal

Every Dependency_Type defined in this document is designed to function as an **edge label** in the fractal drilldown explanation traversal. When a user or system traverses the Organism_Graph to explain how a State_Change propagated from source to target, each edge carries its Dependency_Type as the explanatory label that answers: "Through what mechanism did this effect travel?"

### Traversal Contract

For any Dependency_Path in the Organism_Graph:

1. The edge MUST carry exactly one PRIMARY Dependency_Type (or multiple unordered types per Multi-Type Coexistence Rules)
2. The type label MUST be sufficient to generate a human-readable explanation of the causal mechanism
3. The type's Propagation Mechanism description serves as the template for explanation generation
4. No edge may exist without a type label — unlabeled edges are prohibited

### Explanation Pattern

Each type supports the following explanation pattern at any level of fractal drilldown:

```
"[Source] affects [Target] through [Dependency_Type] because [Propagation Mechanism]"
```

This pattern is recursively applicable: at Level 0 (headline), the type name suffices; at deeper levels (Level 1–5), the full mechanism description provides the explanatory detail.

### No Dead Ends

Every Dependency_Type defined here connects to:
- The State_Change_Taxonomy (what initiated the propagation)
- The Temporal_Taxonomy (how fast the propagation occurs)
- The Expansion_Taxonomy (at which order the propagation manifests)

This ensures that explanation traversal never encounters a dead end when following a typed edge — there is always a next level of detail available through cross-reference.

(See: README_market_organism_principles, Section: Principle 1 — Organism over Collection)
(See: README_expansion_taxonomy, Section: Expansion Definition)

---

## Cross-References

This document references and is referenced by the following deliverables:

### Temporal_Taxonomy References
- (See: README_temporal_taxonomy, Section: Latency Definition) — Temporal profiles for each Dependency_Type; combined Latency rule (shortest) for multi-type edges
- (See: README_temporal_taxonomy, Section: Duration Definition) — Duration characteristics per type; combined Duration rule (longest) for multi-type edges
- (See: README_temporal_taxonomy, Section: Amplification Definition) — Amplification behavior per type; combined assessment for multi-type edges
- (See: README_temporal_taxonomy, Section: Dampening Definition) — Dampening behavior per type; combined assessment for multi-type edges

### State_Change_Taxonomy References
- (See: README_state_change_taxonomy, Section: Top-Level Categories) — Source State_Changes that initiate propagation through these dependency types
- (See: README_state_change_taxonomy, Section: Classification Hierarchy) — Mandatory ordering that precedes dependency classification
- (See: README_state_change_taxonomy, Section: Root Node Invariant) — Ensures dependency sources are valid State_Changes, not assets

### Expansion_Taxonomy References
- (See: README_expansion_taxonomy, Section: Expansion Definition) — How these dependency types form the edges traversed during expansion
- (See: README_expansion_taxonomy, Section: Feedback Detection Rule) — How typed edges participate in feedback loop identification

### Market_Organism_Principles References
- (See: README_market_organism_principles, Section: Principle 1 — Organism over Collection) — Constraint that dependencies are causal mechanisms in a living organism
- (See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation) — Constraint that dependencies are causal, not statistical; foundational distinction for Dependency vs. Correlation section
- (See: README_market_organism_principles, Section: Principle 3 — All Propagation is Temporal) — Constraint that all dependency propagation carries temporal properties
- (See: README_market_organism_principles, Section: Principle 5 — Expansion Has Order) — Constraint that typed edges form discrete hops in expansion sequence

