---
artifact_id: engine_roadmap_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines capability priority ordering and dependency structure for MoneyHorst engine development
ssot_relationship: canonical
topic: engine_roadmap
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [journey_capability_matrix_md, user_intelligence_journey_framework_md, market_organism_framework]
---

# ENGINE ROADMAP FRAMEWORK

Version: v1
Status: Canonical Architecture Document
Layer: 4 (between Capability Matrix and Implementation)

---

## PURPOSE

This document answers one question:

> Which capabilities must MoneyHorst develop first, and in what order?

The Journey Capability Matrix identified 9 new capabilities.
This document prioritizes them based on:
- Which journeys they unblock
- Which downstream capabilities depend on them
- Which existing infrastructure they can leverage

---

## ARCHITECTURAL POSITION

```
Layer 1: Market Organism Framework       COMPLETE (Territory)
Layer 2: User Intelligence Journey       COMPLETE (Navigation)
Layer 3: Journey Capability Matrix       COMPLETE (Muscles)
Layer 4: Engine Roadmap Framework        THIS DOCUMENT (Training Plan)
Layer 5: Implementation                  FUTURE (Execution)
```

The metaphor:
- Layer 1 = Territory (how the world works)
- Layer 2 = Navigation (how humans move through it)
- Layer 3 = Muscles (what the system must be able to do)
- Layer 4 = Training Plan (which muscles to train first)
- Layer 5 = Execution (the actual training)

---

## PRIORITIZATION FRAMEWORK

Each capability is evaluated on three axes:

### Axis 1: Journey Blocking Factor
How many journeys are non-functional without this capability?

### Axis 2: Downstream Dependency Count
How many other capabilities depend on this one existing first?

### Axis 3: Existing Infrastructure Leverage
How much of this capability can be built on what already exists?

---

## THE 9 CAPABILITIES — FULL ANALYSIS

---

### 1. Asset-to-Narrative Registry

**What it does:** Maps which assets belong to which narratives, enabling upward traversal from any asset to its causal State_Change.

**JTBD:** "I clicked Nvidia. Show me WHY it moved — trace upward to the cause."

**Journeys blocked without it:**
- Investigation (cannot do fractal drill-down without knowing asset to narrative to state change)
- Discovery (cannot personalize state changes to portfolio without knowing which narratives the portfolio is exposed to)
- Scenario (cannot show portfolio impact without knowing which assets connect to which propagation paths)

**Downstream dependencies:**
- Reverse Graph Traversal (needs this registry to know which direction to traverse)
- Relevance Engine (needs this to connect state changes to portfolio exposure)
- Portfolio-Organism Bridge (needs this to map portfolio positions into the organism)

**Existing infrastructure:**
- Partial: SEMANTIC_SIGNAL_REGISTRY already maps some narrative dependencies (ai_dependency_high, defense_dependency_elevated)
- Partial: Allocation engine already categorizes by sector
- Missing: No formal asset to narrative to state_change mapping exists

**Priority:** P0 — Foundation. Without this, Investigation, Discovery, and Scenario are all broken.

---

### 2. Reverse Graph Traversal

**What it does:** From any leaf node (asset, signal, portfolio metric), traces UPWARD through the Organism Graph to the originating State_Change.

**JTBD:** "Nvidia is up 4%. What State_Change caused this? Trace the causation backward."

**Journeys blocked without it:**
- Investigation (the entire fractal drill-down depends on upward traversal)
- Trust (cannot show "why" without tracing back to source)

**Downstream dependencies:**
- None directly (it IS the traversal mechanism)

**Existing infrastructure:**
- Partial: Engine DAG in engine_registry.py defines forward dependencies
- Partial: governance/influence_graph.py has directed graph with DFS
- Missing: No reverse traversal from asset/signal back to causal origin

**Depends on:**
- Asset-to-Narrative Registry (must exist first to know entry points)
- Organism Graph structure (from Market Organism deliverables)

**Priority:** P0 — Foundation. Investigation Journey is the most important journey and it requires this.

---

### 3. Relevance Engine

**What it does:** Connects detected State_Changes to the user's specific portfolio exposure, filtering "what matters to ME right now."

**JTBD:** "Fed went hawkish. Does that matter for MY portfolio? How much?"

**Journeys blocked without it:**
- Discovery (cannot surface personalized priority items)
- Scenario (cannot show portfolio-specific impact without relevance mapping)

**Downstream dependencies:**
- Priority Ranking (needs relevance scores to order items)
- Personalization (is essentially relevance + filtering)

**Existing infrastructure:**
- Partial: Signal_Bubble_v0 knows portfolio allocation and concentration
- Partial: Semantic engine detects narrative dependencies
- Missing: No mechanism to connect external State_Changes to portfolio exposure paths

**Depends on:**
- Asset-to-Narrative Registry (must know which narratives the portfolio is exposed to)
- State_Change_Taxonomy (must classify incoming state changes)

**Priority:** P0 — Foundation. Discovery is the entry point to MoneyHorst. Without relevance, the user sees noise.

---

### 4. Propagation Engine

**What it does:** Traverses the Organism Graph forward from a State_Change through all Expansion_Orders, applying Temporal_Properties at each hop.

**JTBD:** "Oil +20%. Show me the cascade: what happens at Month 1, Month 3, Month 12."

**Journeys blocked without it:**
- Scenario (the entire "What if?" journey depends on propagation)
- Decision (consequence modeling requires forward propagation)

**Downstream dependencies:**
- Portfolio-Organism Bridge (uses propagation to show portfolio impact)
- Time Simulation (is propagation + temporal rendering)
- Feedback Detection (is propagation + cycle detection)

**Existing infrastructure:**
- Partial: Pipeline orchestrator has DAG execution with dependency ordering
- Partial: Expansion_Taxonomy defines the hop structure (from Market Organism)
- Partial: Temporal_Properties define latency/duration (from Market Organism)
- Missing: No engine that traverses the organism graph with temporal simulation

**Depends on:**
- Market Organism deliverables (taxonomy, expansion, dependencies, temporal — all must be written first)
- Asset-to-Narrative Registry (to connect propagation endpoints to assets)

**Priority:** P1 — Organism Core. Requires P0 foundations + Market Organism deliverables to exist first.

---

### 5. Portfolio-Organism Bridge

**What it does:** Maps the user's portfolio positions into the Organism Graph, showing how adding/removing exposure changes the dependency structure.

**JTBD:** "If I buy ASML, what new dependencies do I create? What cascades am I now exposed to?"

**Journeys blocked without it:**
- Decision (cannot show consequences of portfolio changes)
- Scenario (cannot show portfolio-specific impact of state changes)

**Downstream dependencies:**
- Consequence Modeling (needs the bridge to project impact)
- Trade-off Visualization (needs the bridge for each option)

**Existing infrastructure:**
- Partial: Signal_Bubble_v0 has portfolio state (allocation, concentration)
- Partial: Semantic engine maps allocation to narrative dependencies
- Missing: No mechanism to project "what changes if I add X"

**Depends on:**
- Asset-to-Narrative Registry (must know where assets sit in the organism)
- Propagation Engine (must be able to trace forward from new exposure)
- Relevance Engine (must be able to assess impact magnitude)

**Priority:** P1 — Organism Core. Requires P0 foundations + Propagation Engine.

---

### 6. Concept Registry (Multi-Altitude)

**What it does:** Provides every metric, signal, and taxonomy term with beginner/intermediate/expert explanations, all referencing the same Signal Bubble data.

**JTBD:** "What is PEG? Why does it matter HERE? Show me historical mispricing."

**Journeys blocked without it:**
- Learning (entirely depends on altitude-adaptive explanations)

**Downstream dependencies:**
- Contextual Linking (needs the registry to link from)
- Educational Layer (is the registry + rendering)

**Existing infrastructure:**
- Partial: Glossary in requirements.md defines core terms
- Partial: Signal_Lifecycle_Definition has provenance and description fields
- Missing: No multi-altitude explanation system exists

**Depends on:**
- Signal_Lifecycle_Definition (provides the base definitions)
- Market Organism Taxonomy (provides the concept structure)

**Priority:** P2 — Trust and Learning. Important but not blocking core functionality.

---

### 7. Historical Accuracy Tracker

**What it does:** Tracks per-signal accuracy over time — how often was this signal correct? When did it fail? Under what regime?

**JTBD:** "This signal says concentration_risk_elevated. How often has that been accurate historically?"

**Journeys blocked without it:**
- Trust (cannot show historical reliability without tracking it)

**Downstream dependencies:**
- Confidence calibration (future: adjust confidence based on historical accuracy)

**Existing infrastructure:**
- Partial: SemanticStateStore has immutable snapshots and delta log
- Partial: ReasoningObject has confidence_level field
- Missing: No per-signal accuracy tracking or backtesting exists

**Depends on:**
- Signal_Bubble_v0 migration (signals must be registered to track them)
- Memory infrastructure (historical snapshots must be queryable)

**Priority:** P2 — Trust and Learning. Enhances trust but not blocking first version.

---

### 8. Versioned Organism Graph

**What it does:** Stores the Organism Graph state at every timestamp, enabling "what did MoneyHorst know at time T?" queries.

**JTBD:** "When did MoneyHorst first recognize the AI power grid thesis? Show me the graph at that point."

**Journeys blocked without it:**
- Memory (cannot do forensic replay without historical graph state)

**Downstream dependencies:**
- Evolution Tracking (needs versioned graph to compute diffs)
- Snapshot Replay (needs versioned graph + signal state)

**Existing infrastructure:**
- Partial: SemanticStateStore already does immutable snapshots per run
- Partial: Delta log tracks additions/removals/changes
- Missing: No versioned graph structure (only flat signal lists, not graph topology)

**Depends on:**
- Organism Graph must exist first (from Market Organism implementation)
- Propagation Engine (graph must be operational before versioning it)

**Priority:** P3 — Institutional Memory. Critical for long-term value but not for first version.

---

### 9. Model Versioning

**What it does:** Separately tracks changes to the MODEL (taxonomy updates, new dependency types, recalibrated temporal properties) vs. changes to the MARKET (new state changes, new signals).

**JTBD:** "Did my portfolio risk increase because the market changed, or because MoneyHorst's model improved?"

**Journeys blocked without it:**
- Memory (cannot distinguish model evolution from market evolution)

**Downstream dependencies:**
- None directly (it is a meta-capability for institutional knowledge)

**Existing infrastructure:**
- Partial: .domainization/mutation_audit_ledger.yaml tracks governance mutations
- Partial: policy_versioner.py tracks policy versions
- Missing: No separation between "market state changed" and "model definition changed"

**Depends on:**
- Versioned Organism Graph (must version the graph before distinguishing what changed it)

**Priority:** P3 — Institutional Memory. Long-term institutional value.

---

## PRIORITY TIERS

### P0 — Foundations (Must exist for ANY journey to work)

| Capability | Unblocks | Dependency Count |
|------------|----------|-----------------|
| Asset-to-Narrative Registry | Investigation, Discovery, Scenario | 3 downstream |
| Reverse Graph Traversal | Investigation, Trust | 0 downstream (IS the mechanism) |
| Relevance Engine | Discovery, Scenario | 2 downstream |

**Why P0:** Without these three, the user cannot:
- Investigate anything (no upward traversal)
- Discover what matters (no relevance filtering)
- Connect assets to the organism (no narrative mapping)

**Estimated scope:** Definition + data model + initial population. No scoring, no AI.

---

### P1 — Organism Core (Makes the organism operational)

| Capability | Unblocks | Dependency Count |
|------------|----------|-----------------|
| Propagation Engine | Scenario, Decision | 3 downstream |
| Portfolio-Organism Bridge | Decision, Scenario | 2 downstream |

**Why P1:** Without these two, the user cannot:
- Run scenarios ("What if Oil +20%?")
- See decision consequences ("What happens if I buy ASML?")

**Depends on:** P0 complete + Market Organism deliverables written.

---

### P2 — Trust and Learning (Makes the system trustworthy and educational)

| Capability | Unblocks | Dependency Count |
|------------|----------|-----------------|
| Concept Registry (multi-altitude) | Learning | 2 downstream |
| Historical Accuracy Tracker | Trust | 1 downstream |

**Why P2:** Without these two, the user cannot:
- Learn at their level (no altitude switching)
- Verify historical reliability (no accuracy tracking)

**Depends on:** P0 + P1 operational. Signal_Bubble_v0 migrated.

---

### P3 — Institutional Memory (Makes the system remember)

| Capability | Unblocks | Dependency Count |
|------------|----------|-----------------|
| Versioned Organism Graph | Memory | 2 downstream |
| Model Versioning | Memory | 0 downstream |

**Why P3:** Without these two, the user cannot:
- Replay past states ("What did MoneyHorst know in January?")
- Distinguish model changes from market changes

**Depends on:** P1 operational (graph must exist before versioning it).

---

## EXECUTION SEQUENCE

```
Step 0: Market Organism Deliverables (5 documents — definition only)
        State_Change_Taxonomy
        Expansion_Taxonomy
        Dependency_Types
        Temporal_Taxonomy
        Market_Organism_Principles
             |
             v
Step P0: Foundations
         Asset-to-Narrative Registry
         Reverse Graph Traversal
         Relevance Engine
             |
             v
Step P1: Organism Core
         Propagation Engine
         Portfolio-Organism Bridge
             |
             v
Step P2: Trust and Learning
         Concept Registry
         Historical Accuracy Tracker
             |
             v
Step P3: Institutional Memory
         Versioned Organism Graph
         Model Versioning
```

**Critical insight:** The Market Organism spec (design + tasks) should produce the 5 definition documents FIRST. Only after those exist can P0 capabilities be built, because they need the taxonomy and graph structure to operate on.

---

## JOURNEY ACTIVATION BY TIER

| Tier Complete | Journeys Activated |
|---------------|-------------------|
| Market Organism docs only | None (definition only, no runtime) |
| + P0 Foundations | Discovery (basic), Investigation (basic) |
| + P1 Organism Core | Scenario, Decision, Investigation (full) |
| + P2 Trust/Learning | Trust (full), Learning |
| + P3 Memory | Memory (full) |

**Note:** "Basic" means the journey works but with limited depth.
"Full" means the journey works at all fractal levels.

---

## WHAT THIS DOCUMENT IS NOT

- NOT a sprint plan (no dates, no story points)
- NOT a technical design (no APIs, no schemas, no code)
- NOT a feature backlog (no tickets)
- NOT implementation guidance (that belongs to Layer 5)

This document answers ONLY: "Which muscles first?"

---

## KEY INSIGHT

The correct next step is NOT:
```
Requirements then Design then Tasks then Implementation
```

The correct next step IS:
```
Market Organism Deliverables (5 definition documents)
  then P0 Foundation Capabilities
  then P1 Organism Core
  then P2 Trust/Learning
  then P3 Memory
```

The Market Organism spec's design + tasks should produce the 5 DEFINITION DOCUMENTS.
Not engines. Not code. Not scores.
Just the formal taxonomies and principles that P0 capabilities will operate on.

This is the training plan.
Now we know which muscles to train first.
