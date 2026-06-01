# Expansion Taxonomy

---
artifact_id: expansion_taxonomy_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Defines the ordered expansion of Impulses through the Organism_Graph via Dependency_Paths
ssot_relationship: canonical
topic: expansion_taxonomy
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism.principles_md, state_change_taxonomy_md, dependency_types_v2_md, temporal_taxonomy_md]
---

## Scope Statement

This document defines the formal taxonomy of Expansion_Orders — the ordered sequence of propagation hops through which an Impulse propagates outward via Dependency_Paths in the Organism_Graph. It establishes exactly four canonical Expansion_Orders (1st through 4th), each with a distinguishing definition, causal distance, and nature of connection. It provides complete worked examples demonstrating propagation through all four orders using Dependency_Types and Temporal_Properties from their respective canonical documents. This document does NOT contain engines, code, scores, weights, probabilities, numeric models, asset lists, correlation matrices, dashboards, or any executable logic.

---

## Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary

This document does not define terms. It consumes them.

---

## Expansion Definition

**Expansion** is the ordered sequence of propagation hops measured by Expansion_Order, where each hop corresponds to the traversal of exactly one Dependency_Path between two nodes in the Organism_Graph.

An Impulse originates at a Root_Node (which must be a State_Change, Event, Impulse, or Regime_Shift — never an asset) and propagates outward through the Organism_Graph. Each traversal of a Dependency_Path constitutes one hop. The number of hops from the originating Root_Node to a given affected system determines that system's Expansion_Order.

Expansion is:
- **Ordered**: Each hop is discrete and countable. There is no "1.5th Order."
- **Causal**: Each hop traverses an identifiable Dependency_Path with a named Dependency_Type.
- **Temporal**: Each hop carries Temporal_Properties (Latency, Duration, Amplification, Dampening) from the Temporal_Taxonomy.
- **Finite**: Propagation terminates when no further identifiable Dependency_Path connects to an additional system not already in the sequence.

(See: README_market_organism_principles, Section: Principle 5 — Expansion Has Order)
(See: README_dependency_types_v2, Section: Type Enumeration)
(See: README_temporal_taxonomy, Section: Temporal Property Enumeration)

---

## Expansion Order Definitions


### 1st Order Expansion

`order.1st`

**Definition**: Effects that manifest after exactly one Dependency_Path traversal from the originating Impulse. These are the direct, immediate consequences of the Root_Node State_Change — the systems that are causally adjacent to the source.

**Causal Distance**: 1 hop from Root_Node

**Distinguishing Criterion**: An affected system belongs to 1st Order if and only if the shortest path from the originating Impulse traverses exactly one Dependency_Path. The system must be directly connected to the Root_Node through a single identifiable causal mechanism.

**Nature of Connection**: The Dependency_Path connecting the Root_Node to a 1st Order system is a direct causal link — the source State_Change produces an effect at the target through a single, identifiable mechanism without intermediary systems. These connections typically exhibit the shortest Latency values (Day to Week) because no intermediate propagation steps are required.

(See: README_temporal_taxonomy, Section: Latency)
(See: README_dependency_types_v2, Section: Type Enumeration)

---

### 2nd Order Expansion

`order.2nd`

**Definition**: Effects that manifest after exactly two Dependency_Path traversals from the originating Impulse. These are the secondary consequences — systems affected not by the Root_Node directly, but by the 1st Order systems that were themselves affected by the Root_Node.

**Causal Distance**: 2 hops from Root_Node

**Distinguishing Criterion**: An affected system belongs to 2nd Order if and only if the shortest path from the originating Impulse traverses exactly two Dependency_Paths. The system is not directly connected to the Root_Node — it is connected to a 1st Order system, which is itself connected to the Root_Node.

**Nature of Connection**: The Dependency_Path connecting a 1st Order system to a 2nd Order system represents a secondary causal mechanism — the 1st Order system's altered state produces a new effect at the 2nd Order target. The causal channel may differ from the 1st Order connection (e.g., a Macro dependency at 1st Order may produce a Fundamental dependency at 2nd Order). Latency typically increases (Week to Month) because the effect must first manifest at the 1st Order system before propagating further.

(See: README_temporal_taxonomy, Section: Latency)
(See: README_dependency_types_v2, Section: Type Enumeration)

---

### 3rd Order Expansion

`order.3rd`

**Definition**: Effects that manifest after exactly three Dependency_Path traversals from the originating Impulse. These are the tertiary consequences — systems affected through a chain of two intermediate systems, each of which was itself affected by the prior order.

**Causal Distance**: 3 hops from Root_Node

**Distinguishing Criterion**: An affected system belongs to 3rd Order if and only if the shortest path from the originating Impulse traverses exactly three Dependency_Paths. The system is connected to a 2nd Order system, which is connected to a 1st Order system, which is connected to the Root_Node.

**Nature of Connection**: The Dependency_Path connecting a 2nd Order system to a 3rd Order system represents a tertiary causal mechanism — the propagation has now traversed multiple intermediate systems, and the causal connection to the original Impulse becomes increasingly indirect. The Dependency_Type at this distance often shifts toward Behavioral, Narrative, or Supply_Chain channels as the effect diffuses through the broader economic system. Latency typically increases further (Month to Quarter) and Dampening typically emerges as absorbing mechanisms accumulate.

(See: README_temporal_taxonomy, Section: Dampening)
(See: README_dependency_types_v2, Section: Type Enumeration)

---

### 4th Order Expansion

`order.4th`

**Definition**: Effects that manifest after exactly four Dependency_Path traversals from the originating Impulse. These are the quaternary consequences — the most distant effects that can be reliably traced through identifiable causal mechanisms before the signal attenuates beyond identifiability.

**Causal Distance**: 4 hops from Root_Node

**Distinguishing Criterion**: An affected system belongs to 4th Order if and only if the shortest path from the originating Impulse traverses exactly four Dependency_Paths. The system is connected through a chain of three intermediate systems back to the Root_Node.

**Nature of Connection**: The Dependency_Path connecting a 3rd Order system to a 4th Order system represents the outermost identifiable causal mechanism in the propagation sequence. At this distance, the connection to the original Impulse is highly indirect — the effect has traversed multiple causal channels and intermediate systems. Latency is typically at its longest (Quarter to Year), Amplification is typically at its lowest (None to Low), and Dampening is typically at its highest (High to Extreme) as the original signal has been absorbed by multiple intermediate mechanisms. The Dependency_Types at this distance often involve Behavioral or Narrative channels as the effect manifests through broad systemic shifts rather than direct operational linkages.

(See: README_temporal_taxonomy, Section: Amplification)
(See: README_temporal_taxonomy, Section: Dampening)
(See: README_dependency_types_v2, Section: Behavioral)
(See: README_dependency_types_v2, Section: Narrative)

---


## Worked Example: Nvidia Guidance Raise

Root_Node: Nvidia raises data center revenue guidance significantly above consensus expectations (Type: State_Change)
Canonical ID: `sc.corporate.guidance`

(See: README_state_change_taxonomy, Section: Corporate Sub-Categories)

This example demonstrates a Corporate State_Change propagating through all four Expansion_Orders, affecting progressively more distant systems through identifiable Dependency_Paths with named Dependency_Types and Temporal_Properties.

---

### 1st Order (Direct Effects)

Systems directly connected to the Root_Node through a single Dependency_Path traversal.

| Affected System | Dependency_Type | Latency | Duration | Amplification | Dampening |
|----------------|-----------------|---------|----------|---------------|-----------|
| AI Infrastructure Narrative Strengthening | Narrative (`dep.narrative`) | Day | Quarter | High | None |
| TSMC Advanced Node Utilization Expectations | Fundamental (`dep.fundamental`) | Day | Quarter | Moderate | None |

**Explanation — AI Infrastructure Narrative Strengthening**:

Effect arrives within Day BECAUSE the Narrative Dependency_Path (`dep.narrative`) transmits through the informational channel — Nvidia's guidance raise immediately strengthens the prevailing "AI Infrastructure" narrative as market participants update their beliefs about AI spending trajectory. The causal mechanism is shared narrative membership: Nvidia's results serve as the bellwether data point for the entire AI infrastructure investment theme.

Amplification is High because the narrative effect extends beyond Nvidia's specific business — it validates the broader AI spending thesis, amplifying the signal across all entities sharing narrative membership. Dampening is None — no absorbing mechanism exists at this direct distance.

(See: README_dependency_types_v2, Section: Narrative)
(See: README_temporal_taxonomy, Section: Amplification)

**Explanation — TSMC Advanced Node Utilization Expectations**:

Effect arrives within Day BECAUSE the Fundamental Dependency_Path (`dep.fundamental`) transmits through the economic channel — Nvidia is TSMC's largest customer for advanced process nodes. Higher Nvidia revenue guidance directly implies higher chip orders, which alters TSMC's utilization expectations through the operational linkage of their manufacturing agreement.

Amplification is Moderate because the effect is meaningful but bounded by the specific commercial relationship. Dampening is None — the supply relationship is direct and unmediated.

(See: README_dependency_types_v2, Section: Fundamental)

---

### 2nd Order (Secondary Effects)

Systems connected through exactly two Dependency_Path traversals from the Root_Node. Each 2nd Order system is affected by a 1st Order system, not directly by the Root_Node.

| Affected System | Source (1st Order) | Dependency_Type | Latency | Duration | Amplification | Dampening |
|----------------|-------------------|-----------------|---------|----------|---------------|-----------|
| Broadcom Custom AI Chip Program Perception | AI Infrastructure Narrative Strengthening | Narrative (`dep.narrative`) | Week | Quarter | Moderate | Low |
| ASML EUV Equipment Order Pipeline | TSMC Advanced Node Utilization Expectations | Supply_Chain (`dep.supply_chain`) | Month | Quarter | Moderate | Low |
| Data Center REIT Expansion Planning | AI Infrastructure Narrative Strengthening | Fundamental (`dep.fundamental`) | Week | Quarter | Low | Low |

**Explanation — Broadcom Custom AI Chip Program Perception**:

Effect arrives within Week BECAUSE the Narrative Dependency_Path (`dep.narrative`) from the strengthened AI Infrastructure narrative propagates to Broadcom's custom AI chip business through shared narrative membership. Market participants update their assessment of Broadcom's AI opportunity as the broader narrative strengthens. The delay (Week vs Day) reflects the time for analyst coverage and consensus formation to propagate the narrative to adjacent entities.

Amplification decreases to Moderate — the narrative signal is still meaningful but no longer compounding as it did at 1st Order. Dampening emerges at Low — Broadcom's specific business characteristics (different customer base, different chip architecture) partially absorb the narrative signal.

(See: README_dependency_types_v2, Section: Narrative)

**Explanation — ASML EUV Equipment Order Pipeline**:

Effect arrives within Month BECAUSE the Supply_Chain Dependency_Path (`dep.supply_chain`) from TSMC's increased utilization expectations propagates to ASML through the physical delivery dependency — TSMC's capacity expansion requires EUV lithography machines from ASML. The delay reflects the time for TSMC to translate utilization expectations into formal equipment orders through their procurement cycle.

Amplification is Moderate because TSMC's expansion plans affect ASML's entire advanced equipment pipeline. Dampening is Low — ASML's existing order backlog partially absorbs incremental demand signals.

(See: README_dependency_types_v2, Section: Supply_Chain)

**Explanation — Data Center REIT Expansion Planning**:

Effect arrives within Week BECAUSE the Fundamental Dependency_Path (`dep.fundamental`) from the strengthened AI Infrastructure narrative propagates to data center real estate through operational linkage — increased AI compute demand requires physical data center capacity, which drives expansion planning at data center REITs.

Amplification is Low — the connection from narrative to physical infrastructure planning is meaningful but indirect. Dampening is Low — existing capacity and long construction timelines partially absorb demand signals.

(See: README_dependency_types_v2, Section: Fundamental)

---

### 3rd Order (Tertiary Effects)

Systems connected through exactly three Dependency_Path traversals from the Root_Node. Each 3rd Order system is affected by a 2nd Order system.

| Affected System | Source (2nd Order) | Dependency_Type | Latency | Duration | Amplification | Dampening |
|----------------|-------------------|-----------------|---------|----------|---------------|-----------|
| Semiconductor Equipment Supply Chain Strain | ASML EUV Equipment Order Pipeline | Supply_Chain (`dep.supply_chain`) | Quarter | Year | Low | Moderate |
| Regional Power Grid Capacity Planning | Data Center REIT Expansion Planning | Macro (`dep.macro`) | Quarter | Year | Low | Moderate |

**Explanation — Semiconductor Equipment Supply Chain Strain**:

Effect arrives within Quarter BECAUSE the Supply_Chain Dependency_Path (`dep.supply_chain`) from ASML's increased order pipeline propagates to ASML's own component suppliers (optics, laser sources, precision stages) through physical delivery dependencies. The delay reflects the time for increased ASML production schedules to strain their upstream supply chain as component demand exceeds planned capacity.

Amplification is Low — the original Nvidia guidance signal is now three causal steps removed and significantly diffused. Dampening is Moderate — ASML's suppliers maintain inventory buffers and have multiple customers, absorbing part of the demand increase.

(See: README_dependency_types_v2, Section: Supply_Chain)
(See: README_temporal_taxonomy, Section: Dampening)

**Explanation — Regional Power Grid Capacity Planning**:

Effect arrives within Quarter BECAUSE the Macro Dependency_Path (`dep.macro`) from data center expansion planning propagates to regional power infrastructure through the systemic transmission channel — large-scale data center construction requires substantial electrical capacity, which triggers utility planning processes and regulatory filings for grid expansion. The delay reflects the time for construction permits and power purchase agreements to enter the utility planning cycle.

Amplification is Low — the connection from AI chip guidance to power grid planning is highly indirect. Dampening is Moderate — existing grid capacity, efficiency improvements, and multiple demand sources absorb part of the incremental signal.

(See: README_dependency_types_v2, Section: Macro)

---

### 4th Order (Quaternary Effects)

Systems connected through exactly four Dependency_Path traversals from the Root_Node. Each 4th Order system is affected by a 3rd Order system.

| Affected System | Source (3rd Order) | Dependency_Type | Latency | Duration | Amplification | Dampening |
|----------------|-------------------|-----------------|---------|----------|---------------|-----------|
| Rare Earth Mining Investment Cycle | Semiconductor Equipment Supply Chain Strain | Fundamental (`dep.fundamental`) | Year | Year | None | High |
| Energy Policy Narrative Shift | Regional Power Grid Capacity Planning | Narrative (`dep.narrative`) | Year | Year | None | High |

**Explanation — Rare Earth Mining Investment Cycle**:

Effect arrives within Year BECAUSE the Fundamental Dependency_Path (`dep.fundamental`) from semiconductor equipment supply chain strain propagates to upstream mining operations through operational linkage — sustained demand for precision optical components and specialized materials eventually incentivizes new mining investment to expand raw material supply. The delay reflects the multi-quarter timeline for mining investment decisions to respond to downstream demand signals.

Amplification is None — the original Nvidia guidance signal has been fully absorbed into structural economic conditions at this distance. Dampening is High — multiple absorbing mechanisms exist between AI chip guidance and mining investment (inventory buffers at every intermediate stage, alternative material sources, recycling programs, demand from non-semiconductor industries).

(See: README_dependency_types_v2, Section: Fundamental)
(See: README_temporal_taxonomy, Section: Dampening)

**Explanation — Energy Policy Narrative Shift**:

Effect arrives within Year BECAUSE the Narrative Dependency_Path (`dep.narrative`) from regional power grid capacity planning propagates to the broader energy policy discourse through the informational channel — accumulated evidence of data center power demand straining grid capacity shifts the prevailing narrative about energy infrastructure investment priorities. The delay reflects the time for multiple grid planning events to accumulate into a recognizable policy narrative.

Amplification is None — the connection from a single company's guidance raise to national energy policy narrative is maximally indirect. Dampening is High — energy policy narratives are influenced by many factors (climate policy, geopolitics, economics), and the AI-driven demand signal is one input among many.

(See: README_dependency_types_v2, Section: Narrative)

---

### Temporal Properties Summary

| Order | Typical Latency | Typical Amplification | Typical Dampening | Observation |
|-------|----------------|----------------------|-------------------|-------------|
| 1st | Day | High to Moderate | None | Direct causal connection; signal is fresh and unattenuated |
| 2nd | Week to Month | Moderate to Low | Low | One intermediate system; some absorption begins |
| 3rd | Quarter | Low | Moderate | Two intermediate systems; multiple absorbing mechanisms |
| 4th | Year | None | High | Three intermediate systems; signal nearly fully attenuated |

**Observations**:

- Latency increases with distance: Day → Week/Month → Quarter → Year
- Amplification typically decreases with distance: High → Moderate → Low → None
- Dampening typically increases with distance: None → Low → Moderate → High

These are tendencies, not rules. Specific paths may deviate based on their Dependency_Type characteristics and the structural properties of affected systems.

(See: README_temporal_taxonomy, Section: Temporal Propagation Example: Fed Hawkish Shift)

---


## Satisfies

| Requirement | How Satisfied |
|-------------|---------------|
| 3.1 | Defines Expansion as an ordered sequence of propagation hops measured by Expansion_Order, where each hop corresponds to the traversal of exactly one Dependency_Path between two nodes in the Organism_Graph |
| 3.2 | Defines four Expansion_Orders (1st through 4th), each with a distinguishing definition specifying what qualifies an affected system as belonging to that order versus adjacent orders based on the number of Dependency_Path traversals from the originating Impulse |
| 3.3 | Each Expansion_Order specifies the causal distance in hops from the originating Impulse and the nature of the Dependency_Path connecting it to the prior order |
| 3.4 | Provides a complete worked example (Nvidia Guidance Raise) showing an Impulse propagating through all four Expansion_Orders with at least two concrete affected systems identified at each order level |



---

## Termination Criteria

`order.termination`

**Definition**: Propagation along an Expansion sequence terminates at the point where no further identifiable Dependency_Path connects the last affected system to an additional system not already included in the sequence.

**Formal Rule**: Given an Expansion sequence S = [Root_Node, System_1, System_2, ..., System_N], propagation terminates at System_N if and only if:

1. **No outbound Dependency_Path exists** — there is no identifiable causal mechanism (from the 10 canonical Dependency_Types) connecting System_N to any system not already in S, OR
2. **All outbound Dependency_Paths lead to systems already in S** — every identifiable causal mechanism from System_N connects to a node already present in the sequence (in which case, those paths are classified as Feedback_Loops per the Feedback Detection Rule below, not as continued expansion)

**Termination is NOT**:

| Termination is NOT | Why |
|-------------------|-----|
| A numeric threshold (e.g., "stop after 4 orders") | The 4th Order is the current maximum defined order, but termination is determined by the absence of identifiable Dependency_Paths, not by an arbitrary count |
| A dampening threshold (e.g., "stop when Dampening = Extreme") | Dampening describes signal attenuation, not the absence of causal mechanism. A path with Extreme Dampening still propagates — it just propagates weakly |
| A confidence cutoff (e.g., "stop when we're less than 80% sure") | Confidence values are prohibited in the definition layer. Termination is structural (no path exists), not probabilistic |

**Termination IS**:

The structural absence of an identifiable causal mechanism connecting the frontier of the expansion to any new system. If you cannot name the Dependency_Type, you cannot claim the path exists.

**Explanation Readiness**: When explaining why propagation terminated, the explanation must identify what was looked for and why it was not found: "Propagation terminates at [System_N] because no identifiable Dependency_Path of any of the 10 canonical types connects it to a system not already in the expansion sequence."

(See: README_dependency_types_v2, Section: Type Enumeration)
(See: README_market_organism_principles, Section: Principle 5 — Expansion Has Order)

---

## Feedback Detection Rule

`order.feedback_detection`

**Definition**: If a propagation path revisits a node already present in the Expansion sequence, that path is classified as a Feedback_Loop — NOT as a continuation of the Expansion_Order sequence.

**Formal Rule**: Given an Expansion sequence S = [Root_Node, System_1, System_2, ..., System_N], if a Dependency_Path from System_N leads to any node already in S (including the Root_Node), then:

1. The path is classified as a **Feedback_Loop** (a back-edge creating a cycle in the Organism_Graph)
2. The path is **NOT** assigned a new Expansion_Order (there is no "5th Order" created by revisiting a 1st Order node)
3. The revisited node does **NOT** receive a new Expansion_Order designation — it retains its original order assignment
4. The back-edge carries its own Dependency_Type and Temporal_Properties (including Feedback_Delay)

**Detection Criterion**: A path constitutes feedback if and only if its target node has already been assigned an Expansion_Order in the current propagation sequence. The test is membership in the existing sequence, not distance from the Root_Node.

**Distinction from Continued Expansion**:

| Property | Continued Expansion | Feedback Detection |
|----------|--------------------|--------------------|
| Target node | NOT in existing sequence | Already IN existing sequence |
| Effect | Assigns new Expansion_Order to target | Does NOT assign new order; classifies as Feedback_Loop |
| Graph structure | Extends the acyclic forward propagation | Creates a back-edge forming a cycle |
| Temporal property | Carries standard Latency, Duration, Amplification, Dampening | Additionally carries Feedback_Delay |

**Explanation Readiness**: When a feedback path is detected, the explanation must identify: (a) which node is being revisited, (b) what its original Expansion_Order was, (c) what Dependency_Type the back-edge carries, and (d) what Feedback_Delay characterizes the cycle.

(See: README_temporal_taxonomy, Section: Feedback_Delay)
(See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural)

---

## Feedback_Loop

`order.feedback_loop`

### Definition

A Feedback_Loop is a circular Dependency_Path where a sequence of directed edges forms a closed cycle such that a State_Change at node A propagates through one or more intermediate nodes and returns to influence node A. Feedback_Loops are the structural mechanism by which the Organism_Graph captures circular causation — downstream effects eventually influencing the original source.

**Minimum Cycle Length**: A valid Feedback_Loop must contain at least four nodes (≥4 nodes forming a closed cycle). This ensures that feedback represents genuine systemic circular causation rather than trivial bidirectional edges.

**Structural Mandate**: The Organism_Graph is NOT a Directed Acyclic Graph (DAG). Acyclicity constraints are explicitly prohibited in the graph model. The presence of at least one structural cycle is a mandatory property of any valid Organism_Graph. A graph without feedback loops is an incomplete representation of market reality.

(See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural)

### Feedback_Loop Properties

Every Feedback_Loop carries the following properties:

| Property | Description | Source |
|----------|-------------|--------|
| Cycle Nodes | Ordered list of ≥4 nodes forming the closed cycle | Identified from Organism_Graph structure |
| Edge Types | The Dependency_Type label on each edge in the cycle | (See: README_dependency_types_v2, Section: Type Enumeration) |
| Feedback_Delay | Qualitative temporal descriptor for the complete cycle time | (See: README_temporal_taxonomy, Section: Feedback_Delay) |

### Growth Structure vs. Feedback Structure

The Organism_Graph contains two distinct structural components that must be distinguished:

**Growth Structure** (Acyclic Forward Propagation):
- The acyclic subgraph representing forward propagation from a Root_Node through Expansion_Orders 1st through 4th
- Represents the "tree-like" outward expansion of an Impulse
- Each node appears at exactly one Expansion_Order
- No back-edges — all edges point away from the Root_Node (increasing Expansion_Order)
- This is the structure captured by the Expansion_Order definitions above

**Feedback Structure** (Back-Edges Creating Cycles):
- The set of all back-edges that connect downstream nodes back to upstream nodes
- Creates cycles in the Organism_Graph, making it explicitly non-DAG
- Each back-edge carries a Dependency_Type and Feedback_Delay
- Represents circular causation — the mechanism by which effects return to influence their own causes
- This is the structure captured by the Feedback Detection Rule

**Relationship**: The complete Organism_Graph = Growth Structure ∪ Feedback Structure. Neither component alone represents market reality. The growth structure shows how impulses expand outward; the feedback structure shows how the system self-regulates, amplifies, or dampens through circular causation.

| Property | Growth Structure | Feedback Structure |
|----------|-----------------|-------------------|
| Graph type | Acyclic (DAG-like subgraph) | Cyclic (back-edges creating loops) |
| Edge direction | Forward only (increasing Expansion_Order) | Backward (decreasing Expansion_Order or returning to source) |
| Purpose | Models outward propagation of Impulse | Models circular causation and self-regulation |
| Temporal property | Latency, Duration, Amplification, Dampening | Additionally: Feedback_Delay |
| Expansion_Order | Assigned (1st through 4th) | NOT assigned (feedback paths do not create new orders) |


### Concrete Feedback Loop Example: Fed Rate Hike → Dollar → EM Stress → Capital Flight → Fed Policy Pressure

This example demonstrates a complete Feedback_Loop using real market entities from the State_Change taxonomy, with Dependency_Type labels on each edge and a Feedback_Delay characterizing the full cycle time.

**Cycle Nodes** (4 nodes forming a closed cycle):

```
Node A: Fed Rate Hike (sc.macro.rates)
Node B: Dollar Strengthening (sc.macro.fx)
Node C: Emerging Market Sovereign Stress
Node D: Capital Flight to US Fixed Income
```

**Cycle Diagram**:

```
    Fed Rate Hike ──[dep.macro]──→ Dollar Strengthening
         ↑                                    │
         │                                    │
    [dep.macro]                          [dep.macro]
         │                                    │
         │                                    ↓
    Capital Flight  ←──[dep.flow]──  EM Sovereign Stress
    to US Fixed Income
```

**Edge-by-Edge Propagation**:

| Edge | Source Node | Target Node | Dependency_Type | Causal Mechanism |
|------|-------------|-------------|-----------------|------------------|
| A → B | Fed Rate Hike (`sc.macro.rates`) | Dollar Strengthening (`sc.macro.fx`) | Macro (`dep.macro`) | Higher US rates increase dollar-denominated yield attractiveness, drawing capital inflows that strengthen the dollar through the interest rate differential channel |
| B → C | Dollar Strengthening (`sc.macro.fx`) | Emerging Market Sovereign Stress | Macro (`dep.macro`) | A stronger dollar increases the real debt burden for EM sovereigns with dollar-denominated obligations, raising default risk and widening credit spreads through the external debt channel |
| C → D | Emerging Market Sovereign Stress | Capital Flight to US Fixed Income | Flow (`dep.flow`) | Elevated EM sovereign risk triggers institutional capital reallocation from EM debt to US Treasuries as investors seek safety, moving capital through fund flow mechanics |
| D → A | Capital Flight to US Fixed Income | Fed Rate Hike (`sc.macro.rates`) | Macro (`dep.macro`) | Sustained capital inflows to US fixed income compress Treasury yields and tighten financial conditions, creating political and economic pressure on the Fed to moderate its hiking cycle — the downstream effect returns to influence the original source |

**Feedback_Delay**: Quarter

The complete cycle — from Fed rate hike through dollar strengthening, EM stress, capital flight, and back to Fed policy pressure — characteristically completes within one calendar quarter. The delay reflects the time required for: (a) dollar strengthening to manifest in EM debt metrics, (b) EM stress to trigger institutional reallocation decisions, and (c) accumulated capital flows to create observable pressure on Fed policy deliberations.

(See: README_temporal_taxonomy, Section: Feedback_Delay)
(See: README_state_change_taxonomy, Section: Macro Sub-Categories)
(See: README_dependency_types_v2, Section: Macro)
(See: README_dependency_types_v2, Section: Flow)

**Why This Is Feedback, Not Continued Expansion**:

The path from Node D (Capital Flight to US Fixed Income) back to Node A (Fed Rate Hike) revisits the originating node. Per the Feedback Detection Rule, this back-edge is classified as a Feedback_Loop — it does NOT create a "5th Order" expansion. Node A retains its original designation as the Root_Node. The back-edge creates a cycle, making the Organism_Graph explicitly non-DAG.

**Structural Observation**: This feedback loop demonstrates why acyclicity constraints are prohibited. If the Organism_Graph were forced to be a DAG, this circular causation — which is a real structural feature of monetary policy transmission — would be invisible. The organism model captures it because it mandates cycles as structural requirements.

---

## Exclusion Constraints

This section consolidates all prohibitions applicable to the Expansion_Taxonomy deliverable and its usage.

### Prohibited Content

| # | Prohibition | Example of Violation | Rationale |
|---|------------|---------------------|-----------|
| 1 | No engine implementations, Python code, or executable logic | A function that calculates expansion order from graph traversal | This is a definition document, not an implementation |
| 2 | No scoring algorithms, numeric weights, probabilities, ranking systems, or quantitative models | "Expansion probability: 0.7" or "Path strength: 3/5" | Weights on an incomplete model produce false confidence |
| 3 | No dashboard designs, report templates, or visualization specifications | A UI mockup showing expansion tree rendering | Belongs to future implementation phases |
| 4 | No asset lists or ticker symbols as root-level entities | "NVDA → TSMC → ASML" as an expansion chain | Assets are leaf nodes, never root nodes — the primitive chain is preserved. Expansion chains start from State_Changes |
| 5 | No correlation matrices or statistical co-movement measures as substitutes for causal Dependency_Paths | "Correlation between 1st and 2nd order systems: 0.85" | Correlation is not causation; every edge requires an identifiable mechanism |
| 6 | No numeric time values as temporal property assignments | "Latency: 14.5 days between orders" | Discrete calendar units only; false precision is prohibited |
| 7 | No acyclicity constraints on the Organism_Graph | "The expansion graph must be a DAG" | Feedback loops are mandatory structural features; acyclicity is explicitly prohibited |

### Unified Rationale

**Weights on an incomplete model produce false confidence.**

The Expansion_Taxonomy defines the conceptual structure of how impulses propagate. Assigning numeric values to expansion probabilities, path strengths, or order likelihoods would create an illusion of precision that the definition layer cannot support. Mathematics belongs to future implementation phases (P0, P1, P2, P3) where engines can validate quantitative claims against observed data.

### What IS Permitted

- Qualitative temporal descriptors (e.g., Latency: Month, Amplification: High)
- Named Dependency_Types on edges (e.g., `dep.macro`, `dep.flow`)
- Discrete Expansion_Order assignments (1st, 2nd, 3rd, 4th)
- Concrete examples using real market entities for illustration
- Cross-references to other deliverables
- Structural mandates (e.g., "the graph is not a DAG")

### Enforcement

Any content matching the prohibited categories above constitutes a validation error and must be removed or reformulated before the deliverable is considered complete.

(See: README_market_organism_principles, Section: Content Exclusions)

---

## Signal Architecture Compatibility

This section declares the relationship between the Expansion_Taxonomy and the Signal Architecture. These are DECLARATIONS of compatibility — they state what the expansion model preserves and respects. They do NOT implement signal logic.

### Signal Reusability Invariant

Expansion_Orders describe how Intelligence_Objects propagate through the Organism_Graph at increasing distances from the originating Impulse. The following invariant applies:

1. All signals, signal details, static asset facts, derived metrics, and provenance metadata are modeled as reusable **Intelligence_Objects** — addressable, versionable, and served from a canonical source.
2. No Signal_Consumer may privately recalculate Canonical_Signal_Truth. Consumers request intelligence from the authoritative producing domain.
3. Exactly six request types are defined for Signal_Consumers:
   - (a) Single signal value
   - (b) Composite signal bundle
   - (c) Signal detail/provenance
   - (d) Static asset context
   - (e) Variable market context
   - (f) Derived intelligence object
4. **Static_Asset_Context**: Cached intelligence refreshed exclusively by governance policy (not per-request). Refresh policy is declared at the context-type level, not per-consumer.
5. **Variable_Signal**: Intelligence refreshed by one of two mechanisms — scheduled cadence (time-based) or event trigger (reactive invalidation upon upstream State_Change detection).
6. **Derived_Intelligence**: Composite objects invalidated only when declared upstream dependencies change. Each Derived_Intelligence object explicitly declares its dependency set.
7. This invariant applies across all four levels of the canonical chain (SIGNALS, SEMANTICS, REASONING, REPORT). No layer may duplicate intelligence already produced by an upstream layer.

(See: README_market_organism_principles, Section: Signal Architecture Compatibility)

### Signal_Bubble_v0 Preservation

The Expansion_Taxonomy defines how impulses propagate through discrete hops. Signal_Bubble_v0 signals sit at the leaf nodes of expansion paths — they are the sensors that detect propagation has reached the portfolio level. The relationship is:

1. Existing Excel-derived metrics are **first-generation canonical signal objects** (Signal_Bubble_v0). They are NOT legacy artifacts — they are the first real Sensor_Layer of the system.
2. Signal_Bubble_v0 encompasses the following signal categories:
   - **Portfolio Core** — total portfolio value, total P/L, cash EUR, invested capital, total capital, largest position, top performer, worst performer
   - **Allocation** — technology, semiconductors, defense, healthcare, ETFs, USD exposure
   - **Risk** — portfolio health, risk review count, concentration score, max position, max drawdown, portfolio stability, risk alerts
   - **Performance** — portfolio performance, equity curve, 7D return, trend signals
   - **Deployment** — capital deployment, cash readiness, portfolio efficiency, deployment signal
   - **Regime/PM** — market regime, portfolio bias, scenario readiness, high priority candidates, morning briefing outputs
3. No consumer may privately rebuild or recalculate Signal_Bubble_v0 signals. All consumers request these signals from the canonical Signal Bubble registry.
4. **Organism relationship**: Signal_Bubble_v0 signals are leaf-node observations (sensors) in the Organism_Graph. They sit at the terminal points of expansion paths — detecting that an Impulse has propagated through multiple Expansion_Orders and manifested at the portfolio level. They are evidence of propagation, not causes of it.
5. Signal_Bubble_v0 signals are reusable by all future layers including: Morning Briefing, Asset Detail Page, Portfolio Fit, Market Fit, Model Fit, Butterfly Simulation, Scenario Engine, PM Control Center, and Report Pipeline.

### Signal_Lifecycle_Definition Gate

1. Every signal must pass a mandatory **Signal_Lifecycle_Definition** gate before implementation. No bulk signal implementation is permitted — each signal passes its lifecycle individually.
2. The Signal_Lifecycle_Definition contains exactly 11 mandatory fields:
   - `signal_id` — unique identifier within the Signal Bubble namespace
   - `category` — signal category (Portfolio Core, Allocation, Risk, Performance, Deployment, Regime/PM)
   - `owner_domain` — exactly one domain from the 12-domain model (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM)
   - `input_sources` — list of upstream dependencies
   - `classification` — static or variable
   - `refresh_policy` — scheduled cadence or governance-defined refresh interval
   - `cache_policy` — maximum staleness tolerance
   - `provenance` — origin and derivation chain
   - `consumers` — list of downstream consumers
   - `invalidation_rule` — dependency_change, time_expiry, or event_trigger
   - `implementation_status` — one of three statuses (see below)
3. Three implementation statuses:
   - **Defined_Signal** — architecturally positioned, lifecycle complete, no engine yet
   - **Structured_Signal** — architecturally positioned as future Intelligence_Object, must NOT be implemented in this spec
   - **Implemented_Signal** — lifecycle complete and engine producing it
4. Any signal referenced in worked examples within this document must have a Signal_Lifecycle_Definition before implementation.

---

## Cross-References

This section identifies all concepts in this document that are defined authoritatively in other deliverables. Cross-references replace duplication — the referenced deliverable is the single source of truth for the referenced concept.

### References to State_Change_Taxonomy

| Concept Referenced | Source |
|-------------------|--------|
| State_Change classification hierarchy | (See: README_state_change_taxonomy, Section: Classification Hierarchy) |
| Root_Node Invariant (valid root node types) | (See: README_state_change_taxonomy, Section: Root Node Invariant) |
| Nvidia Guidance Raise (Root_Node in worked example) | (See: README_state_change_taxonomy, Section: Corporate Sub-Categories) |
| Fed Rate Hike (Root_Node in feedback loop example) | (See: README_state_change_taxonomy, Section: Macro Sub-Categories) |
| Macro sub-categories (Rates, FX) used in feedback example | (See: README_state_change_taxonomy, Section: Macro Sub-Categories) |

### References to Dependency_Types_v2

| Concept Referenced | Source |
|-------------------|--------|
| Dependency_Type classification (10 canonical types) | (See: README_dependency_types_v2, Section: Type Enumeration) |
| Narrative Dependency_Type (used in worked example) | (See: README_dependency_types_v2, Section: Narrative) |
| Fundamental Dependency_Type (used in worked example) | (See: README_dependency_types_v2, Section: Fundamental) |
| Supply_Chain Dependency_Type (used in worked example) | (See: README_dependency_types_v2, Section: Supply_Chain) |
| Macro Dependency_Type (used in worked and feedback examples) | (See: README_dependency_types_v2, Section: Macro) |
| Flow Dependency_Type (used in feedback loop example) | (See: README_dependency_types_v2, Section: Flow) |
| Behavioral Dependency_Type (referenced in 4th Order) | (See: README_dependency_types_v2, Section: Behavioral) |
| Multi-Type Coexistence Rules | (See: README_dependency_types_v2, Section: Multi-Type Coexistence Rules) |
| Dependency vs. Correlation distinction | (See: README_dependency_types_v2, Section: Dependency vs. Correlation) |

### References to Temporal_Taxonomy

| Concept Referenced | Source |
|-------------------|--------|
| Latency definition and valid values | (See: README_temporal_taxonomy, Section: Latency) |
| Duration definition and valid values | (See: README_temporal_taxonomy, Section: Duration) |
| Amplification definition and valid levels | (See: README_temporal_taxonomy, Section: Amplification) |
| Dampening definition and valid levels | (See: README_temporal_taxonomy, Section: Dampening) |
| Feedback_Delay definition and valid values | (See: README_temporal_taxonomy, Section: Feedback_Delay) |
| Numeric Prohibition (no scores, weights, probabilities) | (See: README_temporal_taxonomy, Section: Numeric Prohibition) |
| Temporal Propagation Example: Fed Hawkish Shift | (See: README_temporal_taxonomy, Section: Temporal Propagation Example: Fed Hawkish Shift) |

### References to Market_Organism_Principles

| Concept Referenced | Source |
|-------------------|--------|
| Principle 4: Feedback is Structural (mandates cycles) | (See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural) |
| Principle 5: Expansion Has Order (discrete hops) | (See: README_market_organism_principles, Section: Principle 5 — Expansion Has Order) |
| Principle 6: Causation over Correlation (edges require mechanisms) | (See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation) |
| Principle 3: All Propagation is Temporal (nothing instantaneous) | (See: README_market_organism_principles, Section: Principle 3 — All Propagation is Temporal) |
| Content Exclusions (no data, assets, scores, implementation) | (See: README_market_organism_principles, Section: Content Exclusions) |
| Exclusion Constraints (consolidated prohibitions) | (See: README_market_organism_principles, Section: Exclusion Constraints) |

---

## Extension Criteria

The Expansion_Taxonomy supports controlled growth through criteria-gated addition. New Expansion_Orders beyond the 4th may be added only when specific evidence criteria are satisfied.

### Adding a New Expansion_Order (5th or Beyond)

A proposed new Expansion_Order may be added to this taxonomy ONLY IF it satisfies ALL of the following criteria:

| # | Criterion | Requirement |
|---|-----------|-------------|
| 1 | Evidence of Identifiable Dependency_Path | Demonstrate with a concrete example that an identifiable Dependency_Path (from the 10 canonical types) connects a 4th Order system to a system not already in the expansion sequence at that distance |
| 2 | Complete Worked Example | Provide a full worked example showing the Impulse propagating through all existing orders AND the proposed new order, with ≥2 affected systems at the new order level, named Dependency_Types on each edge, and Temporal_Properties per the Temporal_Taxonomy |
| 3 | Non-Redundancy | The proposed new order must represent genuinely distinct causal distance — it cannot be a restatement of an existing order or a subdivision of the 4th Order |
| 4 | Termination Justification | Explain why propagation does NOT terminate before reaching the proposed new order (i.e., why the Dependency_Path at that distance is identifiable rather than speculative) |
| 5 | Explanation Readiness | The new order must support fractal drilldown — an explanation chain must be constructible from the new order back to the Root_Node through all intermediate orders |

### Example of Valid Extension Request

> "A Fed Hawkish Shift propagates through 4 orders to Employment in Rate-Sensitive Sectors. From there, an identifiable Behavioral Dependency_Path (`dep.behavioral`) connects to Consumer Spending Pattern Shifts — a system not already in the sequence. The mechanism is: sustained job losses in rate-sensitive sectors alter household spending behavior through income reduction. This represents a genuine 5th hop with identifiable causal mechanism."

### Example of Invalid Extension Request

> "We need a 5th Order because the effect 'probably continues' beyond the 4th Order." — INVALID: "probably continues" is not an identifiable Dependency_Path. Termination criteria require the absence of identifiable paths, and speculation does not satisfy the evidence requirement.

> "The 5th Order effect has a Dependency_Path strength of 0.3." — INVALID: introduces numeric scoring into the definition layer. The evidence must be structural (named Dependency_Type with identifiable mechanism), not quantitative.

### Backward Compatibility

Any new Expansion_Order added via these criteria must NOT:
- Alter the definitions of existing orders (1st through 4th)
- Change the Termination Criteria
- Modify the Feedback Detection Rule
- Invalidate existing worked examples

The new order extends the taxonomy; it does not revise it.

---

## Explanation Readiness and Fractal Drilldown

All Expansion_Orders defined in this document support explanation readiness — the ability to construct a complete explanation chain from any affected system back to the Root_Node through all intermediate orders.

### Explanation Chain Construction

For any system at Expansion_Order N, a valid explanation chain must be constructible:

```
[System at Order N] ← "affected by" ← [System at Order N-1] ← ... ← [System at Order 1] ← "caused by" ← [Root_Node]
```

Each link in the chain must identify:
1. The source system (at the prior order)
2. The Dependency_Type connecting them (from the 10 canonical types)
3. The Temporal_Properties of that connection (Latency, Duration, Amplification, Dampening)
4. The causal mechanism (HOW the source's altered state produces the effect at the target)

### Fractal Drilldown Support

Every Expansion_Order supports fractal drilldown — the ability to zoom into any single hop and explain it at increasing levels of detail:

- **Level 0 (Headline)**: "[System A] is affected by [Root_Node]" — existence of connection
- **Level 1 (Order)**: "[System A] is a [Nth] Order effect of [Root_Node]" — distance classification
- **Level 2 (Path)**: "[System A] is affected through [Dependency_Type] from [System at N-1]" — mechanism identification
- **Level 3 (Temporal)**: "The effect arrives at [Latency] with [Amplification] amplification" — temporal characterization
- **Level 4 (Mechanism)**: "[Full causal explanation of HOW the Dependency_Path transmits the effect]" — complete mechanism
- **Level 5 (Context)**: "[Why this particular Dependency_Type and not another; what structural features of the systems create this connection]" — structural justification

No dead ends exist before the Root_Node. Every system at every order can be traced back to the originating Impulse through a complete, explainable chain.

(See: README_market_organism_principles, Section: Principle 5 — Expansion Has Order)
(See: README_dependency_types_v2, Section: Type Enumeration)
(See: README_temporal_taxonomy, Section: Temporal Property Enumeration)

---

## Satisfies (Continued)

| Requirement | How Satisfied |
|-------------|---------------|
| 3.5 | Defines termination of a propagation path as the point where no further identifiable Dependency_Path connects the last affected system to an additional system not already included in the Expansion sequence |
| 3.6 | Specifies that if a propagation path revisits a node already present in the Expansion sequence, that path is classified as a Feedback_Loop rather than a continuation of the Expansion_Order sequence |
| 6.1 | Defines Feedback_Loops as circular Dependency_Paths where a sequence of directed edges forms a closed cycle such that a State_Change at node A propagates through one or more intermediate nodes and returns to influence node A |
| 6.2 | Mandates that the Organism_Graph is not a DAG by requiring at least one structural cycle and explicitly stating that acyclicity constraints are prohibited |
| 6.3 | References Feedback_Delay as a qualitative temporal descriptor (consistent with Temporal_Properties) representing the characteristic time scale for downstream effects to propagate back to the source (defined authoritatively in Temporal_Taxonomy) |
| 6.4 | Provides a concrete Feedback_Loop example (Fed Rate Hike → Dollar Strengthening → EM Sovereign Stress → Capital Flight to US → Fed Policy Pressure) using real market entities with Dependency_Type labeled on each edge, forming a complete cycle of four nodes |
| 6.5 | Distinguishes between growth structure (acyclic subgraph representing forward propagation) and feedback structure (back-edges creating cycles), defining their properties and relationship |
| 8.7 | Contains a dedicated Exclusion Constraints section consolidating all prohibitions (engines, code, scores, weights, probabilities, dashboards, asset lists, correlation matrices, acyclicity constraints) |
| 10.8 | Cross-References section identifies source deliverables by name and section for all referenced concepts (State_Change_Taxonomy, Dependency_Types_v2, Temporal_Taxonomy, Market_Organism_Principles) |
