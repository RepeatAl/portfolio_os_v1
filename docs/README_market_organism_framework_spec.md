---
artifact_id: market_organism_framework_spec_readme_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Describes the Market Organism Framework spec scope, decisions, and roadmap
ssot_relationship: canonical
topic: market_organism_framework_overview
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_framework, user_intelligence_journey_framework_md, signal_calculation_framework_md, correlation_dependency_framework_md]
---

# MARKET ORGANISM FRAMEWORK — SPEC OVERVIEW

Version: v1
Status: Active Spec (Requirements Phase Complete)
Spec Location: `.kiro/specs/market-organism-framework/`

---

## WHY THIS SPEC EXISTS

Portfolio OS currently operates on a signal-centric architecture:

```
Signal → Interpretation → Action
```

This works for state recognition — detecting WHAT the portfolio looks like right now.

But it cannot answer the deeper question:

```
WHY is the portfolio in this state?
WHERE did the impulse originate?
HOW did it propagate?
WHEN will downstream effects arrive?
```

The CTO forensic finding:

> Almost everything in Portfolio OS is built on state recognition.
> Nothing is built on propagation recognition.

This spec defines the foundational world model that shifts the primitive from:

```
Asset / Signal (current)
```

to:

```
State Change (new primitive)
```

The market is not a collection of assets with correlations.
The market is an organism where state changes propagate through dependency paths
with latency, amplification, dampening, and feedback loops.

---

## WHAT THIS SPEC PRODUCES

This is a DEFINITION-ONLY spec. No engines. No code. No scores.

### Five Deliverable Documents

| # | Deliverable | Question It Answers |
|---|-------------|---------------------|
| 1 | State Change Taxonomy | What kinds of impulses exist? |
| 2 | Expansion Taxonomy | How do impulses propagate? |
| 3 | Dependency Types v2 | What kinds of causal connections exist? |
| 4 | Temporal Taxonomy | How fast do effects propagate? |
| 5 | Market Organism Principles | What are the natural laws? |

### Plus: Signal Architecture Foundation

| # | Deliverable | Question It Answers |
|---|-------------|---------------------|
| 6 | Signal Bubble v0 Registry | What signals already exist as reusable objects? |
| 7 | Signal Lifecycle Definition | What must every signal declare before implementation? |
| 8 | Intelligence Object Model | How do consumers request signal truth? |

---

## HARD INVARIANTS (Non-Negotiable)

These five invariants constrain ALL work in this spec:

### Invariant 1: Assets Are Never Root Nodes

Root nodes are exclusively: State Changes, Events, Impulses, Regime Shifts.
Never: "Nvidia", "AAPL", "Gold".
Always: "Fed Hawkish Shift", "Nvidia Guidance Raise", "Oil Shock".

### Invariant 2: Feedback Loops Are Mandatory

The market is not a tree. It is an organism.
A → B → C → D → A (cycles are structural, not exceptional).
The Organism Graph is explicitly NOT a DAG.

### Invariant 3: Taxonomy Before Assets

Classification hierarchy is always:
1. State Change type
2. Expansion type
3. Affected systems
4. Affected narratives
5. Affected assets

Never the reverse.

### Invariant 4: Every Expansion Path Has Temporal Properties

- Latency (Day, Week, Month, Quarter, Year)
- Duration (same units)
- Amplification (None, Low, Moderate, High, Extreme)
- Dampening (None, Low, Moderate, High, Extreme)

Nothing is instantaneous. Nothing is permanent.

### Invariant 5: No Mathematics in Phase 1

Explicitly forbidden: scores, weights, probabilities, ranking systems.
Reason: weights on an incomplete model produce false confidence.

---

## SIGNAL ARCHITECTURE DECISIONS

### Signal Reusability Invariant

All signals are modeled as reusable Intelligence Objects.
No consumer may privately recalculate canonical signal truth.

Six request types:
1. Single signal value
2. Composite signal bundle
3. Signal detail/provenance
4. Static asset context
5. Variable market context
6. Derived intelligence object

### Signal Bubble v0 (Legacy Preservation)

Existing Excel/dashboard signals are NOT legacy artifacts.
They are the first real Sensor Layer of MoneyHorst.

The organism does NOT replace these signals.
The organism USES them as sensors.

Preserved signal categories:
- Portfolio Core (value, P/L, cash, capital, positions)
- Allocation (tech, semis, defense, healthcare, ETFs, USD)
- Risk (health, concentration, drawdown, stability, alerts)
- Performance (equity curve, 7D return, trends)
- Deployment (capital deployment, cash readiness, efficiency)
- Regime/PM (regime, bias, scenario readiness, candidates, briefing)

### Signal Lifecycle Gate

No bulk implementation. Every signal must pass an 11-field lifecycle definition:

```
signal_id | category | owner domain | input sources | static/variable |
refresh policy | cache policy | provenance | consumers | invalidation rule |
implementation status
```

Three statuses:
- **Defined_Signal** — Architecturally positioned, lifecycle complete, no engine yet
- **Structured_Signal** — Future Intelligence_Object, must NOT be implemented now
- **Implemented_Signal** — Lifecycle complete AND engine producing it

---

## RELATIONSHIP TO USER INTELLIGENCE JOURNEY

This spec defines the TERRITORY (how the market works).
The User Intelligence Journey Framework defines the LENS (how humans navigate it).

```
Market Organism (this spec)
  ↕
Signal Bubble (intelligence layer)
  ↕
User Journey (navigation layer — 7 journeys)
```

### How Each Journey Consumes This Spec

| Journey | What It Needs From Market Organism |
|---------|-----------------------------------|
| Discovery | State Change detection → "What changed today?" |
| Investigation | Expansion paths + Dependency_Types → fractal drill-down |
| Trust | Signal provenance + lifecycle → "Why should I believe this?" |
| Learning | Taxonomy definitions + historical examples → altitude-adaptive explanation |
| Scenario | Organism Graph + Temporal_Properties → "What if Oil +20%?" |
| Decision | Cascade modeling + portfolio impact → "What are consequences?" |
| Memory | Historical graph state + signal evolution → "When did MoneyHorst first see this?" |

### Design Implications

The seven journeys validate why this spec requires:
1. Every signal must be explainable (Trust)
2. Every signal must be historically queryable (Memory)
3. Every signal must connect to the Organism Graph (Investigation)
4. Every signal must support altitude switching (Learning)
5. Every signal must participate in simulation (Scenario)
6. Every signal must show portfolio impact (Decision)
7. Every signal must surface when relevant (Discovery)

Without the Signal_Lifecycle_Definition, the journeys cannot function.
Without the Organism Graph, Investigation hits dead ends.
Without Temporal_Properties, Scenarios become flat.
Without Feedback Loops, the model is incomplete.

---

## WHAT THIS SPEC EXPLICITLY DOES NOT DO

| Excluded | Reason |
|----------|--------|
| Engine implementations | Definition phase — structure before code |
| Python code | No executable logic in framework documents |
| Scoring algorithms | No math until structure is complete |
| Dashboard designs | UI follows after world model + journey model |
| Report templates | Reports consume signals, not define them |
| Asset lists as primary entities | Assets are leaf nodes, never roots |
| Correlation matrices | Replaced by typed causal Dependency_Paths |
| Position sizing | Belongs to Decision Journey, not world model |

---

## ARCHITECTURAL COMPATIBILITY

This spec preserves the existing Portfolio OS architecture:

- 12 canonical domains unchanged (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM)
- Canonical chain unchanged (SIGNALS → SEMANTICS → REASONING → REPORT)
- Runtime state model unchanged (8 states, 5 integrity dimensions)
- Pipeline orchestrator pattern unchanged
- Governance model unchanged (OWNER, CI, RUNTIME roles)

The framework sits ABOVE the existing architecture as the conceptual world model.
It does not replace, subsume, or restructure any existing domain or pipeline.

Future integration point: the SIGNALS domain will use this framework to detect state changes.
The signal layer becomes a "sensor" that detects where in the organism a change has begun.

---

## CURRENT STATUS

| Layer | Document | Status |
|-------|----------|--------|
| Layer 1 | Market Organism Framework (13 Requirements) | COMPLETE |
| Layer 2 | User Intelligence Journey (7 Journeys) | COMPLETE |
| Layer 3 | Journey Capability Matrix (9 New Capabilities) | COMPLETE |
| Layer 4 | Engine Roadmap Framework (P0-P3 Prioritization) | COMPLETE |
| Layer 5 | Implementation | FUTURE |

| Spec Phase | Status |
|------------|--------|
| Pre-Flight (Architecture Scan) | Complete |
| Requirements (13 requirements) | Complete |
| Technical Design | Pending — produces 5 definition documents |
| Task List | Pending — ordered by Market Organism deliverables |
| Implementation | Blocked until design + tasks complete |

### Requirements Summary

| Req | Title | Invariant Covered |
|-----|-------|-------------------|
| 1 | State Change Taxonomy | 4 categories (Macro, Corporate, Narrative, Events) |
| 2 | Root Node Invariant | Assets never root nodes |
| 3 | Expansion Taxonomy | Ordered propagation hops (1st-4th) |
| 4 | Dependency Types | 10 causal mechanisms |
| 5 | Temporal Properties | Latency, Duration, Amplification, Dampening |
| 6 | Feedback Loop Mandate | Graph is NOT a DAG |
| 7 | Organism Principles | Constitution with violation conditions |
| 8 | Exclusion Constraints | No scores, no code, no dashboards |
| 9 | Architectural Compatibility | Preserves 12 domains + canonical chain |
| 10 | Deliverable Structure | 5 self-contained documents |
| 11 | Signal Reusability | Intelligence Objects, 6 request types, caching |
| 12 | Signal Bubble v0 | Legacy signals preserved as sensors |
| 13 | Signal Lifecycle Gate | 11-field definition before implementation |

---

## NEXT STEPS

1. **Generate Technical Design** — Structure for the 5 definition documents (taxonomies + principles)
2. **Generate Task List** — Ordered tasks to write the 5 Market Organism deliverables
3. **Execute Tasks** — Write the actual taxonomy and principles documents
4. **P0 Foundation Spec** — Separate spec for Asset-to-Narrative Registry, Reverse Traversal, Relevance Engine
5. **P1 Organism Core Spec** — Separate spec for Propagation Engine, Portfolio-Organism Bridge

---

## RELATED DOCUMENTS

| Document | Location | Layer | Relationship |
|----------|----------|-------|--------------|
| User Intelligence Journey Framework | `docs/README_user_intelligence_journey_framework.md` | Layer 2 | Defines how users navigate the organism |
| Journey Capability Matrix | `docs/README_journey_capability_matrix.md` | Layer 3 | Defines what capabilities each journey requires |
| Engine Roadmap Framework | `docs/README_engine_roadmap_framework.md` | Layer 4 | Prioritizes capabilities into P0-P3 tiers |
| Signal Calculation Framework | `docs/signal_calculation_framework.md` | Existing | Defines current signal calculation rules |
| Correlation and Dependency Framework | `docs/correlation_dependency_framework.md` | Existing | To be superseded by Dependency Types v2 |
| System Architecture | `docs/system_architecture.md` | Existing | Preserved, organism sits above |
| Domain Registry | `.domainization/domain_registry.yaml` | Existing | 12 domains unchanged |
| Semantic Engine | `engines/semantic_engine.py` | Existing | Future sensor for state change detection |
| Pipeline Orchestrator | `engines/pipeline_orchestrator.py` | Existing | Pattern preserved |

---

## FORENSIC SUMMARY

The fundamental insight driving this spec:

> The current architecture answers: "What IS the state?"
> The new architecture answers: "WHY is this the state, WHERE did it start, HOW did it get here, and WHEN will downstream effects arrive?"

This is not an incremental improvement.
This is a paradigm shift in the system's primitive unit of reality.

The tree must be defined before we count more fruit.
