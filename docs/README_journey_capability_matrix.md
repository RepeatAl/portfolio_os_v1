---
artifact_id: journey_capability_matrix_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines required system capabilities for each user journey to function
ssot_relationship: canonical
topic: journey_capability_matrix
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [user_intelligence_journey_framework_md, market_organism_framework, signal_calculation_framework_md]
---

# JOURNEY CAPABILITY MATRIX

Version: v1
Status: Canonical Architecture Document
Layer: 3 (between Journey Definition and Engine Roadmap)

---

## PURPOSE

This document answers one question:

> What capabilities must the system possess for each journey to function?

It bridges the gap between:
- Layer 1: Market Organism (how the world works) — COMPLETE
- Layer 2: User Intelligence Journey (how humans navigate) — COMPLETE
- Layer 3: THIS DOCUMENT (what the system must be able to do)
- Layer 4: Engine Roadmap (what to build) — FUTURE
- Layer 5: Implementation (how to build it) — FUTURE

Without this matrix, we know WHAT the user needs and HOW the market works,
but not WHAT CAPABILITIES connect the two.

---

## ARCHITECTURAL CONTEXT

```
Layer 1: Market Organism Framework
         (Territory — 13 Requirements, 5 Invariants)
              ↓
Layer 2: User Intelligence Journey Framework
         (Navigation — 7 Journeys)
              ↓
Layer 3: Journey Capability Matrix    ← THIS DOCUMENT
         (System Capabilities Required)
              ↓
Layer 4: Engine Roadmap
         (What to Build)
              ↓
Layer 5: Implementation
         (How to Build It)
```

---

## THE MATRIX

### Journey 1: Discovery

**Question:** "What should I pay attention to right now?"

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| Relevance Filtering | Determine which state changes matter for THIS portfolio based on current exposure | Organism Graph + Signal_Bubble_v0 (allocation signals) |
| Priority Ranking | Order surfaced items by urgency and portfolio impact | Temporal_Properties (latency = how soon does this hit?) |
| Exposure Awareness | Know which narratives, sectors, and dependency paths the portfolio is currently exposed to | Signal_Bubble_v0 (allocation, concentration, narrative dependency) |
| State Change Detection | Identify that a new State_Change has occurred in the organism | State_Change_Taxonomy + external data feeds |
| Personalization | Filter market-general state changes to portfolio-relevant ones | Portfolio state + Organism Graph intersection |

**Gap from Analysis:** Gap C (Priority/Relevance Filtering) lands here.

**Prerequisite Layers:**
- Market Organism: State_Change_Taxonomy (to classify what happened)
- Signal Bubble: Signal_Bubble_v0 (to know portfolio exposure)
- NEW: Relevance engine (connects state changes to portfolio exposure)

---

### Journey 2: Investigation

**Question:** "Why is this happening? What causes this?"

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| Fractal Traversal | Navigate the Organism Graph depth-first from any node, always one more level available | Organism_Graph + Expansion_Taxonomy |
| Dependency Navigation | Follow typed Dependency_Paths between nodes with labeled edges | Dependency_Types (10 types) |
| Narrative Mapping | Connect assets to narratives to state changes (upward traversal) | Asset-to-Narrative registry |
| Expansion Visualization | Show propagation from impulse through 1st/2nd/3rd/4th order | Expansion_Taxonomy |
| Upward Causation | From any asset, trace UPWARD to the originating State_Change | Root_Node_Invariant + reverse graph traversal |
| Temporal Context | Show WHEN each effect arrives at each expansion order | Temporal_Properties |

**Gap from Analysis:** Gap E (Narrative Membership) lands here.

**Prerequisite Layers:**
- Market Organism: Expansion_Taxonomy, Dependency_Types, Temporal_Properties
- NEW: Asset-to-Narrative mapping registry (which assets belong to which narratives)
- NEW: Reverse traversal capability (from leaf to root)

---

### Journey 3: Trust

**Question:** "Can I trust this assessment? Show me the evidence."

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| Provenance Chain | Trace any intelligence object back to its source data and calculation method | Signal_Lifecycle_Definition (provenance field) |
| Decomposition | Break any composite assessment into its contributing signals | Derived_Intelligence dependency declarations |
| Auditability | Show the full calculation path from raw data to final output | Intelligence_Object metadata |
| Historical Accuracy | Show how often this signal/assessment has been correct in the past | Memory layer + signal history |
| Confidence Visibility | Always show confidence level alongside any assessment | Existing confidence_policy + ReasoningObject schema |
| Challenge Response | When user asks "Why?", provide structured explanation at the signal level | Provenance + decomposition combined |

**Gap from Analysis:** Gap A (Explainability Depth) partially lands here (provenance side).

**Prerequisite Layers:**
- Signal Architecture: Signal_Lifecycle_Definition (provenance, input sources)
- Signal Architecture: Intelligence_Object model (decomposable)
- NEW: Historical accuracy tracking per signal
- EXISTING: ReasoningObject.confidence_level, confidence_explanation

---

### Journey 4: Learning

**Question:** "Help me understand this concept at my level."

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| Altitude Switching | Same data explained at beginner/intermediate/expert level | Concept registry with multi-level descriptions |
| Concept Registry | Every metric, signal, and taxonomy term has a formal definition | Glossary (exists in requirements) + extended definitions |
| Contextual Linking | Any concept appearing in any view is linkable to its explanation | UI affordance + concept registry |
| Historical Examples | Show past instances where this concept was relevant | Memory layer + signal history |
| Comparison Context | Explain why THIS metric matters HERE vs. alternatives | Static_Asset_Context + sector/regime context |

**Gap from Analysis:** Gap A (Explainability Depth) fully lands here (altitude side).

**Prerequisite Layers:**
- Market Organism: Taxonomy definitions (provide the concept structure)
- NEW: Concept registry with altitude-adaptive descriptions
- NEW: Educational layer that references Signal Bubble data (not separate content)

---

### Journey 5: Scenario

**Question:** "What happens if X occurs?"

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| State Injection | Accept a hypothetical State_Change and propagate it through the Organism Graph | State_Change_Taxonomy + Organism_Graph |
| Propagation Engine | Trace expansion through all orders with typed dependencies | Expansion_Taxonomy + Dependency_Types |
| Time Simulation | Show WHEN each effect arrives (not flat/simultaneous) | Temporal_Properties (Latency per hop) |
| Feedback Detection | Identify and display feedback loops triggered by the injected state change | Feedback_Loop definitions |
| Portfolio Impact | Show how the propagation affects the user's specific portfolio | Signal_Bubble_v0 (portfolio state) + Organism_Graph intersection |
| Scenario Presets | Offer common scenarios (Oil +20%, Fed Cuts, China Stimulus) as starting points | State_Change_Taxonomy sub-categories |

**Prerequisite Layers:**
- Market Organism: ALL deliverables (taxonomy, expansion, dependencies, temporal, feedback)
- Signal Bubble: Signal_Bubble_v0 (portfolio baseline for impact calculation)
- NEW: Propagation engine (traverses graph with temporal properties)
- NEW: Portfolio-organism intersection logic

---

### Journey 6: Decision

**Question:** "I have capital to deploy. What are my options and their consequences?"

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| Portfolio Impact Projection | Show how adding/removing exposure changes portfolio organism state | Organism_Graph + Signal_Bubble_v0 |
| Consequence Modeling | For each option, show: what you gain, what you risk, what dependencies you create | Dependency_Types + Expansion_Taxonomy |
| Trade-off Visualization | Compare multiple options side-by-side on organism-level effects | Multiple scenario runs |
| Cascade Awareness | Show how a new position changes the portfolio's dependency structure | Organism_Graph (new edges added) |
| Temporal Consequence | Show when benefits and risks materialize for each option | Temporal_Properties |
| Non-Recommendation Constraint | System shows consequences, NEVER recommends specific actions | Architectural constraint (no "Buy X") |

**Gap from Analysis:** Gap D (Portfolio Impact Projection) lands here.

**Prerequisite Layers:**
- Market Organism: Dependency_Types, Expansion_Taxonomy, Temporal_Properties
- Signal Bubble: Signal_Bubble_v0 (current portfolio state)
- Scenario capability (reused from Journey 5)
- NEW: Portfolio-organism bridge (how does adding exposure change the graph?)
- NEW: Multi-option comparison engine

---

### Journey 7: Memory

**Question:** "What did MoneyHorst know before? When did it first see this?"

**Required Capabilities:**

| Capability | Description | Depends On |
|------------|-------------|------------|
| Historical Graph State | Query the Organism Graph as it existed at any past timestamp | Versioned Organism_Graph snapshots |
| Snapshot Replay | Reconstruct what the system knew at any past point in time | SemanticStateStore (existing) + extended versioning |
| Signal Timeline | Show when any signal was first active, when it changed, when it expired | Signal history per Intelligence_Object |
| Reasoning Timeline | Show past reasoning objects and their conclusions at historical points | ReasoningObject history (extends existing) |
| Evolution Tracking | Show how a narrative, dependency, or expansion path evolved over time | Versioned Organism_Graph + diff capability |
| Model vs. Market Distinction | Distinguish between: what changed in the market vs. what changed in the model | Separate versioning for market state and model state |

**Gap from Analysis:** Gap B (Historical Queryability) lands here.

**Prerequisite Layers:**
- EXISTING: SemanticStateStore (immutable snapshots, delta log)
- NEW: Versioned Organism_Graph (graph state at past timestamps)
- NEW: Signal timeline per Intelligence_Object
- NEW: Model versioning (separate from market state versioning)

---

## CAPABILITY DEPENDENCY GRAPH

```
Market Organism (Layer 1)
  |
  |-- State_Change_Taxonomy ----> State Change Detection (Discovery)
  |                           ---> State Injection (Scenario)
  |                           ---> Scenario Presets (Scenario)
  |
  |-- Expansion_Taxonomy -------> Fractal Traversal (Investigation)
  |                           ---> Propagation Engine (Scenario)
  |                           ---> Consequence Modeling (Decision)
  |
  |-- Dependency_Types ---------> Dependency Navigation (Investigation)
  |                           ---> Cascade Awareness (Decision)
  |                           ---> Propagation Engine (Scenario)
  |
  |-- Temporal_Properties ------> Temporal Context (Investigation)
  |                           ---> Time Simulation (Scenario)
  |                           ---> Temporal Consequence (Decision)
  |                           ---> Priority Ranking (Discovery)
  |
  +-- Feedback_Loops -----------> Feedback Detection (Scenario)
                              ---> Evolution Tracking (Memory)

Signal Bubble (Layer 1.5)
  |
  |-- Signal_Lifecycle_Definition ---> Provenance Chain (Trust)
  |                                ---> Decomposition (Trust)
  |                                ---> Signal Timeline (Memory)
  |
  |-- Intelligence_Objects ----------> Auditability (Trust)
  |                                ---> Altitude Switching (Learning)
  |                                ---> Historical Accuracy (Trust)
  |
  +-- Signal_Bubble_v0 -------------> Exposure Awareness (Discovery)
                                   ---> Portfolio Impact (Scenario, Decision)
                                   ---> Personalization (Discovery)
```

---

## GAP RESOLUTION MAP

The 5 gaps identified in the requirements review are now formally placed:

| Gap | Journey | Required Capability | Layer |
|-----|---------|--------------------|----|
| A: Explainability Depth | Learning + Trust | Altitude Switching + Concept Registry | Layer 3 (this doc) -> Layer 4 (engine) |
| B: Historical Queryability | Memory | Versioned Organism_Graph + Signal Timeline | Layer 3 (this doc) -> Layer 4 (engine) |
| C: Priority/Relevance Filtering | Discovery | Relevance Filtering + Exposure Awareness | Layer 3 (this doc) -> Layer 4 (engine) |
| D: Portfolio Impact Projection | Decision | Portfolio-Organism Bridge + Consequence Modeling | Layer 3 (this doc) -> Layer 4 (engine) |
| E: Narrative Membership | Investigation | Asset-to-Narrative Mapping Registry | Layer 3 (this doc) -> Layer 4 (engine) |

None of these gaps belong in the Market Organism requirements (Layer 1).
They belong here (Layer 3) and will drive the Engine Roadmap (Layer 4).

---

## NEW CAPABILITIES IDENTIFIED (Not in Any Existing Layer)

| Capability | First Needed By | Description |
|------------|----------------|-------------|
| Relevance Engine | Discovery | Connects state changes to portfolio exposure for priority filtering |
| Asset-to-Narrative Registry | Investigation | Maps which assets belong to which narratives (reverse of taxonomy) |
| Reverse Graph Traversal | Investigation | From any leaf node, trace upward to originating State_Change |
| Historical Accuracy Tracker | Trust | Per-signal accuracy history (how often correct?) |
| Concept Registry (multi-altitude) | Learning | Every term with beginner/intermediate/expert explanations |
| Propagation Engine | Scenario | Traverses Organism_Graph with temporal properties for simulation |
| Portfolio-Organism Bridge | Decision | How adding/removing exposure changes the graph structure |
| Versioned Organism_Graph | Memory | Graph state queryable at any past timestamp |
| Model Versioning | Memory | Separate tracking of model changes vs. market changes |

These 9 capabilities form the core of the future Engine Roadmap (Layer 4).

---

## WHAT THIS DOCUMENT IS NOT

- NOT requirements for the Market Organism Framework (those are complete at 13)
- NOT an implementation plan (no code, no engines, no APIs)
- NOT a priority ordering (that belongs in the Engine Roadmap)
- NOT a timeline (that belongs in project planning)

This document maps WHAT the system must be able to do.
The Engine Roadmap will determine WHAT to build and in WHAT order.

---

## KEY INSIGHT

The ultimate output of MoneyHorst is not:
- A signal
- An asset score
- A portfolio metric

The ultimate output is:

> **Understanding**

MoneyHorst is an Understanding Engine for markets, portfolios, and capital allocation.

Every capability in this matrix serves one purpose:
Move the user from "I have a question" to "I understand the cause."

The Market Organism provides the causal structure.
The Signal Bubble provides the intelligence objects.
The Journey Framework provides the navigation paths.
This Capability Matrix provides the system requirements.

Together they form the complete architecture of understanding.
