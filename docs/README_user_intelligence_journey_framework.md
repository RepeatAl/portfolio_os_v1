---
artifact_id: user_intelligence_journey_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines the user journey model through MoneyHorst intelligence
ssot_relationship: canonical
topic: user_intelligence_journey
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_framework, signal_calculation_framework_md]
---

# USER INTELLIGENCE JOURNEY FRAMEWORK

Version: v1
Status: Canonical Concept Document
Relationship: Parallel to Market Organism Framework (not a subset — a second organism model)

---

## PURPOSE

The Market Organism Framework defines how the market works.
This document defines how the user moves through that knowledge.

These are two distinct organism models:

1. **Market Organism** — How state changes propagate through dependency paths
2. **User Organism** — How a human navigates from question to understanding

The system that wins is not the one with the most signals.
It is the one that moves a user from:

> "I have a question"

to:

> "I understand the cause."

This journey is not yet modeled. This document establishes its structure.

---

## CORE PRINCIPLE

MoneyHorst does not present data.
MoneyHorst guides understanding.

Every screen, every signal, every interaction must serve exactly one purpose:
Move the user one step closer to causal understanding.

If a feature does not advance the user along a defined journey,
it does not belong in MoneyHorst.

---

## THE SEVEN JOURNEYS

MoneyHorst supports exactly seven user journeys.
Each journey represents a distinct cognitive mode.
A user may switch between journeys at any time.

---

### Journey 1: Discovery

**Question:** "What should I pay attention to right now?"

**Cognitive Mode:** Scanning, orienting, prioritizing attention.

**Entry Points:**
- App open / Morning Briefing
- Portfolio overview
- State Changes Today feed
- Top Risks / Top Opportunities surface

**Journey Structure:**
```
User opens MoneyHorst
  → System surfaces highest-priority state changes
  → User sees: what changed, what matters, what requires attention
  → User decides: investigate further OR acknowledge and move on
```

**Design Constraints:**
- Discovery must never overwhelm (max 3-5 priority items)
- Every surfaced item must link to an Investigation Journey
- Discovery must be personalized to the user's portfolio exposure
- Discovery must distinguish between: portfolio-relevant vs. market-general

**Signal Bubble Relationship:**
Discovery consumes: Morning Briefing outputs, Risk Alerts, Market Regime, High Priority Candidates, State Change detections.

---

### Journey 2: Investigation

**Question:** "Why is this happening? What causes this?"

**Cognitive Mode:** Drilling down, following causation, building mental models.

**Entry Points:**
- Click on any asset
- Click on any signal
- Click on any state change
- Click on any narrative

**Journey Structure:**
```
User clicks: Nvidia
  → Asset Overview (what is the current state?)
  → Narratives (which stories drive this asset?)
  → AI Infrastructure (which narrative specifically?)
  → Hyperscaler Capex (what is the causal impulse?)
  → Expansion Tree (how does this propagate?)
  → Butterfly Effects (what are the 2nd/3rd/4th order consequences?)
```

**Design Constraints:**
- Investigation must be FRACTAL — every node is expandable
- Every level must answer: "Why?" with one more layer of causation
- The user must never hit a dead end (always one more level available)
- Investigation must connect to the Organism Graph (each drill-down follows a Dependency_Path)
- Assets are never the root — investigation always leads UPWARD to the State_Change that caused the effect

**Signal Bubble Relationship:**
Investigation consumes: Signal details/provenance, Expansion paths, Dependency_Type labels, Temporal_Properties, Static_Asset_Context, Derived_Intelligence.

**Fractal Depth Model:**

| Level | What the user sees | Example |
|-------|-------------------|---------|
| 0 | Asset surface | Nvidia: +4.2% today |
| 1 | Asset context | Narratives: AI Infra, Semiconductor, Datacenter |
| 2 | Narrative detail | AI Infrastructure: Hyperscaler Capex driving demand |
| 3 | Causal impulse | State_Change: "Hyperscaler Capex Guidance Raise" |
| 4 | Expansion tree | 1st Order → 2nd Order → 3rd Order → 4th Order |
| 5 | Feedback loops | Grid demand → Energy prices → Capex pressure → back to Hyperscaler |

---

### Journey 3: Trust

**Question:** "Can I trust this assessment? Show me the evidence."

**Cognitive Mode:** Verifying, challenging, demanding provenance.

**Entry Points:**
- Any score or assessment shown in the UI
- Any recommendation or signal
- "Why?" button on any intelligence object

**Journey Structure:**
```
User sees: ASML — Portfolio Fit: 73
  → User asks: Why 73?
  → System shows: contributing signals, weights (when implemented), provenance
  → User asks: Where does this data come from?
  → System shows: source, calculation method, last refresh, confidence level
  → User asks: Has this been wrong before?
  → System shows: historical accuracy, false positives, regime sensitivity
```

**Design Constraints:**
- MoneyHorst must NEVER say "AI says: Buy X"
- Every assessment must be decomposable into its contributing signals
- Every signal must trace back to its source data and calculation method
- Confidence must always be visible (not hidden behind a clean number)
- The user must be able to challenge any output and receive a structured explanation

**Trust Hierarchy:**
```
Assessment (e.g., "Portfolio Fit: 73")
  → Contributing Signals (which signals produced this?)
  → Signal Provenance (where does each signal come from?)
  → Calculation Method (how was it computed?)
  → Data Source (what raw data feeds it?)
  → Historical Reliability (how often has this been correct?)
```

**Signal Bubble Relationship:**
Trust consumes: Signal detail/provenance (request type 3 from Req 11), Intelligence_Object metadata, Signal_Lifecycle_Definition fields (provenance, input sources, consumers).

---

### Journey 4: Learning

**Question:** "Help me understand this concept at my level."

**Cognitive Mode:** Building knowledge, connecting concepts, deepening expertise.

**Entry Points:**
- Glossary / concept links in any view
- "Explain this" affordance on any metric
- Contextual education within Investigation Journey

**Journey Structure:**
```
Beginner asks: "What is PEG?"
  → System explains: definition, simple example, why it matters

Intermediate asks: "Why is PEG more relevant here than P/E?"
  → System explains: context-dependent valuation, growth premium, sector norms

Expert asks: "Show me historical mispricing when PEG diverged from consensus"
  → System shows: historical data, regime context, signal accuracy
```

**Design Constraints:**
- Same data, different altitude — the system adapts explanation depth
- Learning must never interrupt the primary journey (it's a side-channel)
- Every concept must be linkable from any context where it appears
- Learning content must reference the same Signal Bubble data (not separate educational content)

**Altitude Model:**

| Level | User Profile | Explanation Style |
|-------|-------------|-------------------|
| 1 | Beginner | Definition + simple example |
| 2 | Intermediate | Context + comparison + "why here" |
| 3 | Advanced | Historical evidence + edge cases + regime sensitivity |

**Signal Bubble Relationship:**
Learning consumes: Static_Asset_Context, Signal definitions, historical signal values, Taxonomy definitions from Market Organism.

---

### Journey 5: Scenario

**Question:** "What happens if X occurs?"

**Cognitive Mode:** Simulating, stress-testing, exploring counterfactuals.

**Entry Points:**
- "What if?" interface
- Scenario presets (Oil +20%, Fed Cuts, China Stimulus, etc.)
- State_Change injection into the Organism Graph

**Journey Structure:**
```
User asks: "What if Oil +20%?"
  → System identifies: State_Change category (Macro → Oil)
  → System traces: Expansion through Organism Graph
    → 1st Order: Energy producers, transport costs
    → 2nd Order: Inflation expectations, consumer spending
    → 3rd Order: Rate expectations, growth repricing
    → 4th Order: Portfolio allocation pressure, narrative shifts
  → System shows: Portfolio impact at each Expansion_Order
  → System shows: Temporal dimension (when does each effect arrive?)
  → System shows: Feedback loops (what cycles back?)
```

**Design Constraints:**
- Scenarios must use the Organism Graph as their propagation engine
- Every scenario starts with a State_Change (never with an asset)
- Temporal_Properties must be visible (effects don't happen simultaneously)
- Feedback loops must be shown (not just forward propagation)
- Scenarios must show portfolio-specific impact (not generic market commentary)

**Signal Bubble Relationship:**
Scenario consumes: Expansion_Taxonomy, Dependency_Types, Temporal_Properties, Signal_Bubble_v0 (portfolio state as baseline), Organism_Graph structure.

---

### Journey 6: Decision

**Question:** "I have capital to deploy. What are my options and their consequences?"

**Cognitive Mode:** Evaluating alternatives, weighing tradeoffs, understanding cascading effects.

**Entry Points:**
- "I have 5000 EUR" interface
- Watchlist → "What if I buy this?"
- Rebalancing suggestions
- Opportunity surface

**Journey Structure:**
```
User states: "I have 5000 EUR to invest"
  → System does NOT say: "Buy ASML"
  → System shows:
    Option A: Effect on concentration, narrative dependency, deployment
    Option B: Effect on diversification, new exposure, regime sensitivity
    Option C: Effect on portfolio fit, market fit, model fit
  → For each option:
    → Risks (what could go wrong?)
    → Cascades (what does this change about the portfolio organism?)
    → Dependencies (what new dependencies does this create?)
    → Temporal effects (when do benefits/risks materialize?)
```

**Design Constraints:**
- MoneyHorst NEVER recommends a specific action
- MoneyHorst shows consequences of possible actions
- Every option must show its effect on the portfolio organism (not just the asset)
- Decision support must include: what you gain, what you risk, what dependencies you create
- The user decides — MoneyHorst illuminates

**Signal Bubble Relationship:**
Decision consumes: Portfolio Fit, Market Fit, Model Fit, Concentration signals, Deployment signals, Scenario outputs, Organism_Graph (to show cascade effects of adding exposure).

---

### Journey 7: Memory

**Question:** "What did MoneyHorst know before? When did it first see this?"

**Cognitive Mode:** Recalling, comparing over time, validating institutional knowledge.

**Entry Points:**
- "History" on any signal or assessment
- "When did MoneyHorst first detect X?"
- Portfolio memory timeline
- Signal evolution view

**Journey Structure:**
```
User asks: "Why was ASML on the watchlist 8 months ago?"
  → System shows: the signals active at that time, the reasoning, the context

User asks: "When did MoneyHorst first recognize the AI power grid thesis?"
  → System shows: first State_Change detection, expansion path evolution, signal timeline

User asks: "How has my portfolio's AI dependency changed over 12 months?"
  → System shows: signal evolution, narrative concentration over time, regime context
```

**Design Constraints:**
- Memory is not just data storage — it is institutional knowledge
- Every signal must be historically queryable (when was it first active? when did it change?)
- Memory must connect to the Organism Graph (how did propagation paths evolve over time?)
- Memory must support "forensic replay" — reconstruct what the system knew at any past point
- Memory must distinguish between: what changed in the market vs. what changed in the model

**Signal Bubble Relationship:**
Memory consumes: Historical snapshots (SemanticStateStore), Signal evolution timelines, Organism_Graph state at past timestamps, Portfolio state history, Signal_Lifecycle_Definition history.

---

## JOURNEY INTERCONNECTIONS

The seven journeys are not isolated. They form a network:

```
Discovery → Investigation → Trust
    ↓            ↓            ↓
Scenario ← Learning      Memory
    ↓
Decision → Memory
```

**Common transitions:**
- Discovery → Investigation: "This looks important, tell me more"
- Investigation → Trust: "I see the assessment, but can I trust it?"
- Investigation → Learning: "I don't understand this concept"
- Discovery → Scenario: "What if this trend continues?"
- Scenario → Decision: "Given this scenario, what should I do?"
- Decision → Memory: "Did I face this situation before?"
- Any → Memory: "When did this first appear?"

---

## SIGNAL CONSUMPTION BY JOURNEY

| Journey | Primary Signal Types Consumed |
|---------|------------------------------|
| Discovery | Morning Briefing, Risk Alerts, State Changes, High Priority |
| Investigation | Signal detail/provenance, Expansion paths, Dependency_Types, Temporal_Properties |
| Trust | Provenance, calculation methods, historical accuracy, confidence levels |
| Learning | Static_Asset_Context, definitions, historical examples |
| Scenario | Organism_Graph, Expansion_Taxonomy, Temporal_Properties, portfolio baseline |
| Decision | Portfolio Fit, Market Fit, Model Fit, concentration, deployment, cascades |
| Memory | Historical snapshots, signal timelines, past reasoning, evolution data |

---

## RELATIONSHIP TO MARKET ORGANISM FRAMEWORK

The Market Organism defines the WORLD.
The User Intelligence Journey defines the LENS.

```
Market Organism (the territory)
  ↕
Signal Bubble (the intelligence layer)
  ↕
User Journey (the navigation layer)
```

The user never sees the raw organism.
The user sees the organism THROUGH their current journey.

- In Discovery mode: the organism is filtered to "what matters now"
- In Investigation mode: the organism is traversed depth-first along Dependency_Paths
- In Scenario mode: the organism is simulated with injected State_Changes
- In Memory mode: the organism is replayed at historical timestamps

The Signal Bubble serves as the bridge:
- The organism produces Intelligence_Objects
- The journeys consume Intelligence_Objects
- The user navigates between journeys while the Signal Bubble maintains consistency

---

## DESIGN IMPLICATIONS FOR SIGNAL ARCHITECTURE

This journey model creates specific demands on the Signal Bubble:

1. **Every signal must be explainable** (Trust Journey requires provenance at every level)
2. **Every signal must be historically queryable** (Memory Journey requires temporal access)
3. **Every signal must connect to the Organism Graph** (Investigation Journey follows Dependency_Paths)
4. **Every signal must support altitude switching** (Learning Journey needs multi-level explanation)
5. **Every signal must participate in simulation** (Scenario Journey injects State_Changes)
6. **Every signal must show portfolio impact** (Decision Journey needs consequence modeling)
7. **Every signal must surface when relevant** (Discovery Journey needs priority filtering)

These seven demands validate the Signal_Lifecycle_Definition requirement:
without explicit provenance, consumers, refresh policy, and invalidation rules,
the journeys cannot function.

---

## WHAT THIS DOCUMENT IS NOT

- NOT a UI specification (no wireframes, no layouts, no components)
- NOT an implementation plan (no code, no engines, no APIs)
- NOT a feature backlog (no tickets, no priorities, no sprints)

This document defines the COGNITIVE ARCHITECTURE of the user experience.
It answers: "How does a human move through intelligence?"

Implementation follows after the Market Organism Framework is complete.

---

## FORENSIC FINDING

The current Portfolio OS architecture covers:
- ~80% of the world model (Market Organism)
- ~30-40% of the user journey

This gap means:
- We know HOW the market propagates state changes
- We do NOT yet know HOW the user navigates that knowledge

This document closes that gap at the conceptual level.
The system that wins moves users from questions to causal understanding.
That movement is now formally defined.
