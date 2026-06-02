---
artifact_id: narrative_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines the ontology of Narrative as a primitive in the MoneyHorst architecture
ssot_relationship: canonical
topic: narrative_ontology
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_framework, engine_roadmap_framework_md, journey_capability_matrix_md]
---

# NARRATIVE FRAMEWORK

Version: v1
Status: Canonical Ontology Document
Position: Foundational primitive definition — required before P0 implementation

---

## WHY THIS DOCUMENT EXISTS

The Engine Roadmap identifies Asset-to-Narrative Registry as the first P0 capability.
But nowhere in the architecture is "Narrative" formally defined.

It appears everywhere:
- State_Change_Taxonomy has a "Narrative" top-level category
- Semantic engine detects "narrative_dependency"
- Investigation Journey traverses "asset to narrative to state change"
- Dependency_Types includes "Narrative" as a propagation mechanism

Yet the fundamental questions remain unanswered:
- What IS a narrative?
- How does it relate to State_Change?
- How does it relate to Assets?
- When does it begin and end?
- Can narratives contain other narratives?

Without this definition, the Asset-to-Narrative Registry cannot be built correctly.
Without the registry, P0 cannot function.
Without P0, no journey works.

This is the last foundational primitive.

---

## THE PRIMITIVE CHAIN

The complete ontological hierarchy of MoneyHorst:

```
State_Change (Cause — the impulse that starts everything)
     |
     v
Narrative (Container — the explanatory structure that makes expansion legible)
     |
     v
System (Domain — the affected functional area)
     |
     v
Asset (Observation — the measurable endpoint where effects manifest)
```

- State_Change is the cause.
- Narrative is the container that makes propagation understandable.
- System is the affected functional domain.
- Asset is the observation point.

The State_Change creates the impulse.
The Narrative explains WHY the impulse propagates in a particular direction.
The System identifies WHICH functional area is affected.
The Asset is WHERE the effect becomes measurable.

---

## WHAT IS A NARRATIVE?

### Definition

A Narrative is a shared market belief structure that connects a State_Change to a set of affected Systems and Assets by providing the causal explanation for WHY the propagation follows a particular path.

A Narrative is NOT:
- A theme (too vague)
- A sector (too structural)
- A trend (too temporal)
- A signal (too atomic)
- A State_Change (too causal)

A Narrative IS:
- A collective market interpretation of WHY certain assets benefit or suffer from a State_Change
- The explanatory bridge between cause (State_Change) and effect (Asset movement)
- The reason capital flows in a particular direction after an impulse

### Formal Properties

| Property | Description |
|----------|-------------|
| Explanatory | A narrative explains WHY capital flows from A to B after a State_Change |
| Shared | A narrative exists because multiple market participants believe it |
| Temporal | A narrative has a birth, a peak, and a death |
| Directional | A narrative channels propagation in a specific direction |
| Falsifiable | A narrative can be invalidated by contradicting evidence |
| Composable | A narrative can contain sub-narratives |
| Multi-asset | A narrative connects to multiple assets simultaneously |

---

## NARRATIVE vs. STATE_CHANGE

This is the critical distinction:

| Aspect | State_Change | Narrative |
|--------|---|---|
| Nature | An event that happened | A belief about what the event means |
| Temporality | Discrete moment | Extended duration |
| Objectivity | Observable fact | Shared interpretation |
| Example | "Hyperscaler Capex +40% YoY" | "AI Infrastructure buildout will drive demand for power, cooling, and networking for years" |
| Role in organism | Root node (cause) | Propagation channel (explanation) |
| Can be wrong? | No (it happened) | Yes (the belief can be invalidated) |

A State_Change triggers a Narrative.
A Narrative channels the expansion.

The State_Change is: "What happened?"
The Narrative is: "What does the market believe this means?"

---

## WHEN DOES A NARRATIVE BEGIN?

A Narrative is born when:
1. A State_Change occurs that creates a new causal explanation
2. Multiple market participants adopt this explanation
3. Capital begins flowing based on this explanation

**Example:**
- State_Change: "OpenAI launches GPT-4" (March 2023)
- Narrative born: "AI will transform every industry — companies building AI infrastructure will see massive demand growth"
- Evidence of birth: Capital flows into Nvidia, AMD, MSFT accelerate; analyst reports adopt the framing

A Narrative does NOT require:
- Universal agreement (some participants may disagree)
- Formal announcement (it emerges organically)
- Precise start date (it crystallizes over days/weeks)

---

## WHEN DOES A NARRATIVE DIE?

A Narrative dies when:
1. The underlying belief is invalidated by contradicting evidence
2. Capital stops flowing based on this explanation
3. A new Narrative replaces it as the dominant explanation

**Example:**
- Narrative: "Crypto will replace traditional finance"
- Death trigger: FTX collapse + regulatory crackdown (2022)
- Evidence of death: Capital outflows, narrative replaced by "crypto is speculative, not systemic"

A Narrative death is NOT:
- Instantaneous (it fades over weeks/months)
- Permanent (narratives can be reborn with new evidence)
- Binary (it can weaken without fully dying)

### Narrative Lifecycle States

```
Emerging --> Strengthening --> Dominant --> Weakening --> Dormant --> Dead
                                                           ^
                                                       (can revive)
```

| State | Description | Capital Flow |
|-------|-------------|-------------|
| Emerging | New explanation gaining initial believers | Early movers positioning |
| Strengthening | Growing consensus, more participants adopting | Accelerating inflows |
| Dominant | Widely accepted as "obvious truth" | Peak positioning, crowding risk |
| Weakening | Contradicting evidence appearing, some participants exiting | Outflows beginning |
| Dormant | No longer driving capital flows but not disproven | Neutral |
| Dead | Fully invalidated, no believers remain | Complete reversal |

---

## CAN AN ASSET BELONG TO MULTIPLE NARRATIVES?

Yes. This is the norm, not the exception.

Example — Nvidia belongs to:
- AI Infrastructure (primary)
- Semiconductor Cycle (structural)
- Datacenter Buildout (derivative)
- Gaming (legacy, weakening)
- Autonomous Driving (emerging)

### Multi-Narrative Rules

1. Every asset has a **primary narrative** — the dominant explanation for its current capital flows
2. Every asset may have **secondary narratives** — additional explanations that contribute to flows
3. Narrative membership is **time-dependent** — an asset's primary narrative can change
4. Narrative membership is **strength-weighted** — some narratives matter more than others for a given asset
5. When narratives conflict, the **dominant narrative** determines the asset's primary propagation path

### Narrative Membership Record

For the Asset-to-Narrative Registry, each membership requires:

```
asset_id
narrative_id
membership_type: primary | secondary | emerging | legacy
strength: strong | moderate | weak
since: date when membership began
evidence: what connects this asset to this narrative
```

---

## CAN A NARRATIVE CONTAIN OTHER NARRATIVES?

Yes. Narratives are hierarchical.

Example:
```
AI Transformation (meta-narrative)
  |
  |-- AI Infrastructure (sub-narrative)
  |     |-- Datacenter Buildout
  |     |-- Power Grid Expansion
  |     |-- Cooling Infrastructure
  |     +-- Semiconductor Supply Chain
  |
  |-- AI Applications (sub-narrative)
  |     |-- Enterprise SaaS AI
  |     |-- Consumer AI
  |     +-- Autonomous Systems
  |
  +-- AI Regulation (sub-narrative)
        |-- Compute Sovereignty
        +-- AI Safety Compliance
```

### Hierarchy Rules

1. A meta-narrative contains multiple sub-narratives
2. Sub-narratives can exist independently (if the meta-narrative weakens, sub-narratives may survive)
3. A State_Change may activate a sub-narrative without activating the meta-narrative
4. Hierarchy depth is unlimited but practically 2-3 levels
5. An asset connects to the MOST SPECIFIC narrative level (not the meta-narrative)

---

## IS A NARRATIVE TIME-DEPENDENT?

Yes. Absolutely.

Narratives have:
- **Birth date** — when the explanation first emerged
- **Peak date** — when maximum capital was flowing based on this explanation
- **Duration** — how long the narrative has been active
- **Expected lifespan** — qualitative estimate (months, years, decades)
- **Regime sensitivity** — which market regimes strengthen or weaken this narrative

### Temporal Properties of Narratives

| Property | Description | Example |
|----------|-------------|---------|
| Age | Time since narrative birth | AI Infrastructure: ~2 years (since GPT-4) |
| Maturity | Position in lifecycle | AI Infrastructure: Dominant |
| Velocity | Speed of strengthening/weakening | AI Infrastructure: Still accelerating |
| Regime sensitivity | Which conditions threaten it | Rate hikes threaten growth narratives |
| Expected duration | Qualitative lifespan estimate | AI Infrastructure: Multi-year (capex cycles are long) |

---

## IS A NARRATIVE A STATE_CHANGE?

No. But a State_Change can CREATE, STRENGTHEN, WEAKEN, or KILL a narrative.

The relationship is:

```
State_Change --[creates]--> Narrative (new)
State_Change --[strengthens]--> Narrative (existing)
State_Change --[weakens]--> Narrative (existing)
State_Change --[kills]--> Narrative (existing)
State_Change --[revives]--> Narrative (dormant)
```

**Examples:**
- "Nvidia Guidance Raise" (State_Change) STRENGTHENS "AI Infrastructure" (Narrative)
- "FTX Collapse" (State_Change) KILLS "Crypto replaces TradFi" (Narrative)
- "China AI chip ban" (State_Change) CREATES "Compute Sovereignty" (Narrative)
- "AI model scaling hits diminishing returns" (State_Change) WEAKENS "AI Transformation" (Narrative)

### State_Change to Narrative Interaction Types

| Interaction | Description | Effect on Narrative Lifecycle |
|-------------|-------------|-------------------------------|
| Creates | State_Change births a new narrative | Narrative enters "Emerging" state |
| Strengthens | State_Change provides confirming evidence | Narrative moves toward "Dominant" |
| Weakens | State_Change provides contradicting evidence | Narrative moves toward "Weakening" |
| Kills | State_Change fully invalidates the belief | Narrative enters "Dead" state |
| Revives | State_Change provides new evidence for dormant narrative | Narrative moves from "Dormant" to "Emerging" |

---

## HOW DOES NARRATIVE RELATE TO DEPENDENCY_TYPES?

In the Market Organism Framework, "Narrative" is one of 10 Dependency_Types.

But here we distinguish two uses:

- **Narrative as Dependency_Type** = the propagation MECHANISM (how effects spread through shared belief)
- **Narrative as Container** = the explanatory STRUCTURE (what connects state changes to assets)

These are two different uses of the same word:

| Context | Meaning | Example |
|---------|---------|---------|
| Dependency_Type: Narrative | The mechanism by which belief propagates effects | "AI hype drives Nvidia price because market believes AI = Nvidia" |
| Narrative as Container | The structural grouping that organizes assets under a causal explanation | "AI Infrastructure" as a category containing Nvidia, AMD, Broadcom, Vertiv |

Both are valid. They operate at different levels:
- Dependency_Type describes HOW propagation works (through shared belief)
- Narrative Container describes WHAT the belief IS (the explanatory structure)

---

## NARRATIVE TAXONOMY (Initial Structure)

Based on the State_Change_Taxonomy categories, narratives cluster into families:

### Macro-Driven Narratives
Born from Macro State_Changes (Rates, Inflation, Oil, Liquidity, FX)

Examples:
- "Higher for longer" (rates narrative)
- "Deglobalization drives inflation" (inflation narrative)
- "Energy transition" (oil/energy narrative)
- "Dollar wrecking ball" (FX narrative)

### Corporate-Driven Narratives
Born from Corporate State_Changes (Earnings, Guidance, Capex, M&A)

Examples:
- "AI Infrastructure buildout" (capex narrative)
- "Semiconductor supercycle" (earnings narrative)
- "Defense spending boom" (guidance narrative)

### Thematic Narratives
Born from Narrative-category State_Changes (AI, Security, Defense, Robotics, Energy)

Examples:
- "AI Transformation" (meta-narrative)
- "Cybersecurity as critical infrastructure" (security narrative)
- "European defense rearmament" (defense narrative)
- "Humanoid robotics revolution" (robotics narrative)
- "Electrification of everything" (energy narrative)

### Event-Driven Narratives
Born from Event State_Changes (Elections, Wars, Pandemics, Sporting Events)

Examples:
- "Trump trade" (election narrative)
- "Defense premium" (war narrative)
- "Remote work permanent" (pandemic narrative)
- "Infrastructure spending" (event narrative)

---

## IMPLICATIONS FOR ASSET-TO-NARRATIVE REGISTRY

The P0 capability "Asset-to-Narrative Registry" must implement:

1. **Narrative as first-class entity** with lifecycle state, hierarchy, and temporal properties
2. **Asset-Narrative membership** with type (primary/secondary/emerging/legacy) and strength
3. **Narrative-State_Change linkage** with interaction type (creates/strengthens/weakens/kills/revives)
4. **Narrative hierarchy** with meta-narratives containing sub-narratives
5. **Temporal tracking** — when did this asset join this narrative? When did the narrative's lifecycle change?

### Registry Structure (Conceptual)

```
Narrative Registry:
  narrative_id
  name
  parent_narrative (nullable — for hierarchy)
  lifecycle_state (emerging/strengthening/dominant/weakening/dormant/dead)
  birth_date
  birth_trigger (State_Change that created it)
  expected_duration
  regime_sensitivity

Asset-Narrative Membership:
  asset_id
  narrative_id
  membership_type (primary/secondary/emerging/legacy)
  strength (strong/moderate/weak)
  since_date
  evidence

Narrative-StateChange Interactions:
  state_change_id
  narrative_id
  interaction_type (creates/strengthens/weakens/kills/revives)
  timestamp
  evidence
```

---

## WHAT THIS DOCUMENT IS NOT

- NOT an implementation specification (no code, no APIs)
- NOT a data model (conceptual structure only)
- NOT a scoring system (no narrative strength scores)
- NOT a prediction model (narratives are observed, not predicted)

This document defines WHAT a narrative IS ontologically.
Implementation details belong to the P0 spec for Asset-to-Narrative Registry.

---

## KEY INSIGHT

The four primitives of MoneyHorst are now formally defined:

```
State_Change --> Narrative --> System --> Asset
(Cause)         (Container)   (Domain)   (Observation)
```

- State_Change: What happened? (objective, discrete, observable)
- Narrative: What does the market believe this means? (shared, temporal, falsifiable)
- System: Which functional area is affected? (structural, stable)
- Asset: Where is the effect measurable? (specific, quantifiable)

The Narrative is the missing link between cause and observation.
Without it, the organism has impulses and endpoints but no explanation
for WHY propagation follows a particular path.

Now the architecture is complete:
- Layer 1 defines the territory (Market Organism)
- Layer 2 defines the navigation (User Journey)
- Layer 3 defines the muscles (Capability Matrix)
- Layer 4 defines the training plan (Engine Roadmap)
- This document defines the last primitive (Narrative Ontology)

Design and tasks may now proceed.
