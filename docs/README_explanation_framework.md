---
artifact_id: explanation_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines the Explanation Object as a primitive and the fractal explainability architecture
ssot_relationship: canonical
topic: explanation_architecture
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_framework, narrative_framework_md, user_intelligence_journey_framework_md, language_rendering_framework_md]
---

# EXPLANATION FRAMEWORK

Version: v1
Status: Canonical Architecture Document
Position: Foundational primitive — defines HOW understanding is structured

---

## WHY THIS DOCUMENT EXISTS

MoneyHorst defines itself as an Understanding Engine.

The architecture already defines:
- WHAT the world looks like (Market Organism)
- HOW users navigate it (User Journey)
- WHAT capabilities are needed (Capability Matrix)
- WHAT to build first (Engine Roadmap)
- HOW to render output (Language + Time Rendering)

But nowhere is it defined:

> HOW does an explanation work?

A signal saying `ai_dependency_high` is not understanding.
A reasoning object with `confidence_level: 70` is not understanding.

Understanding requires:
- WHY is it high?
- BECAUSE of which signals?
- BECAUSE of which state changes?
- BECAUSE of which narratives?
- HOW DEEP can I go?

This is not rendering. This is a structural primitive.

---

## THE MISSING PRIMITIVE

Current primitives:

```
State_Change -> Narrative -> System -> Asset -> Signal -> Semantic_State -> Reasoning_Object
```

Missing:

```
Reasoning_Object -> Explanation_Object -> Altitude_Renderer -> Language_Renderer -> UI
```

The Explanation_Object is the bridge between machine reasoning and human understanding.
Without it, the system produces conclusions.
With it, the system produces comprehension.

---

## WHAT IS AN EXPLANATION?

### Definition

An Explanation_Object is a structured, fractal decomposition of a Reasoning_Object
(or any Intelligence_Object) into progressively deeper causal layers,
where each layer answers "Why?" with one more level of causation.

An Explanation is NOT:
- A tooltip (too flat)
- A paragraph of text (too unstructured)
- A data dump (too raw)
- A single "because" statement (too shallow)

An Explanation IS:
- A tree of causal layers, each answering "Why?" for the layer above
- Fractal — every node is expandable to the next level
- Finite — terminates at the Root_Node (State_Change) or at data source
- Altitude-aware — each level can be rendered at beginner/intermediate/expert
- Language-neutral — the structure exists independently of display language

---

## EXPLANATION LEVELS

Every explainable object in MoneyHorst supports exactly six levels of depth:

| Level | Question | What It Shows | Example |
|-------|----------|---------------|---------|
| 0 | What? | The current state/value | "AI Dependency: HIGH" |
| 1 | Why? | The contributing signals | "Because: Nvidia 32%, Broadcom 11%, TSMC indirect" |
| 2 | Because of which signals? | The signal decomposition | "Allocation > 25% in semiconductor + AI correlation elevated" |
| 3 | Because of which state changes? | The causal impulses | "Hyperscaler Capex Guidance Raise (sc.corporate.capex.hyperscaler_increase)" |
| 4 | Because of which narratives? | The explanatory containers | "AI Infrastructure narrative (narrative.ai_infrastructure) — Dominant lifecycle" |
| 5 | Because of which propagation? | The expansion tree | "1st Order -> 2nd Order -> 3rd Order with temporal properties" |

### Level Properties

- Level 0 is always visible (the surface)
- Levels 1-5 are revealed on demand (progressive disclosure)
- Each level is independently renderable at any altitude (beginner/intermediate/expert)
- Each level is independently renderable in any language
- The user controls depth — the system never forces all levels at once

---

## FRACTAL DRILLDOWN STRUCTURE

The explanation tree is fractal — every node at every level can be expanded:

```
Level 0: AI Dependency = HIGH
  |
  +-- Level 1: Why?
        |-- Nvidia allocation: 32% (signal.allocation.nvidia)
        |     |
        |     +-- Level 2: Why does this matter?
        |           |-- Threshold: >25% triggers concentration
        |           |-- Cross-confirmation: correlation_engine agrees
        |           |
        |           +-- Level 3: What caused this allocation?
        |                 |-- State_Change: sc.corporate.capex.hyperscaler_increase
        |                 |
        |                 +-- Level 4: Which narrative?
        |                       |-- narrative.ai_infrastructure (Dominant)
        |                       |
        |                       +-- Level 5: Expansion path?
        |                             |-- 1st: GPU demand (Latency: Day)
        |                             |-- 2nd: Networking (Latency: Month)
        |                             |-- 3rd: Cooling (Latency: Quarter)
        |                             +-- 4th: Grid (Latency: Year)
        |
        |-- Broadcom allocation: 11% (signal.allocation.broadcom)
        |     +-- [same fractal structure]
        |
        +-- TSMC indirect exposure (signal.dependency.tsmc_indirect)
              +-- [same fractal structure]
```

### Fractal Rules

1. Every node is expandable (no dead ends until Root_Node or data source)
2. Expansion follows the primitive chain: Signal -> State_Change -> Narrative -> Expansion
3. The user controls depth (system never auto-expands beyond Level 0)
4. Each expansion loads on demand (not pre-rendered)
5. Back-navigation is always available (collapse to parent level)

---

## EXPLANATION OBJECT SCHEMA (Conceptual)

```
Explanation_Object:
  explanation_id: string (unique identifier)
  target_object_id: string (what is being explained)
  target_object_type: signal | reasoning_object | semantic_state | narrative | assessment
  
  levels:
    - level: 0
      question: "What?"
      content_id: string (stable ID for this explanation node)
      children: [list of level-1 explanation nodes]
    
    - level: 1
      question: "Why?"
      content_id: string
      contributing_signals: [list of signal_ids]
      children: [list of level-2 explanation nodes]
    
    - level: 2
      question: "Because of which signals?"
      content_id: string
      signal_decomposition: [signal_id, threshold, cross_confirmation]
      children: [list of level-3 explanation nodes]
    
    - level: 3
      question: "Because of which state changes?"
      content_id: string
      state_changes: [list of state_change_ids]
      children: [list of level-4 explanation nodes]
    
    - level: 4
      question: "Because of which narratives?"
      content_id: string
      narratives: [list of narrative_ids with lifecycle_state]
      children: [list of level-5 explanation nodes]
    
    - level: 5
      question: "Because of which propagation?"
      content_id: string
      expansion_path: [ordered list of expansion orders with temporal properties]
      children: [] (terminal — or links to feedback loops)
```

---

## TRUST CHAIN

The Explanation_Object directly serves the Trust Journey.

Every explanation level provides evidence:

| Level | Trust Question | Evidence Provided |
|-------|---------------|-------------------|
| 0 | "Is this true?" | Current value + confidence level |
| 1 | "Why should I believe this?" | Contributing signals with provenance |
| 2 | "Where does this come from?" | Signal sources, calculation methods, thresholds |
| 3 | "What caused this?" | Observable State_Changes with timestamps |
| 4 | "What is the market interpretation?" | Narrative lifecycle state + evidence |
| 5 | "How does this propagate?" | Expansion tree with temporal properties |

The Trust Chain is complete when the user can trace from any assessment
back to an observable State_Change through a fully explained path.

---

## ALTITUDE COMPATIBILITY

Each explanation level renders differently at each altitude:

### Example: Level 1 ("Why is AI Dependency HIGH?")

**Beginner:**
> "Your portfolio has a lot of money in AI-related companies like Nvidia.
> If AI spending slows down, these companies could be affected."

**Intermediate:**
> "32% allocation to Nvidia + 11% Broadcom creates concentrated semiconductor exposure.
> Combined with elevated AI narrative correlation, this triggers the dependency signal."

**Expert:**
> "Allocation engine detects >25% single-narrative concentration.
> Cross-confirmed by correlation_engine (AI cluster r=0.87) and scenario_engine
> (AI-weakness scenario shows -18% portfolio drawdown). Signal confidence: 70%
> based on 3-engine alignment with placeholder semantic coverage for 2 categories."

Same explanation level. Same structural content. Different rendering depth.

---

## LANGUAGE COMPATIBILITY

Explanation_Objects are language-neutral in structure.
Every `content_id` maps to renderings in all supported languages.

```
content_id: explanation.ai_dependency.level1.nvidia_allocation
  EN: "Nvidia represents 32% of your portfolio..."
  DE: "Nvidia macht 32% deines Portfolios aus..."
```

The explanation STRUCTURE (which signals, which state changes, which narratives)
is language-independent. Only the RENDERING of each node is language-specific.

---

## REASONING COMPATIBILITY

The Explanation_Object extends (not replaces) the existing Reasoning_Object:

```
Reasoning_Object (existing):
  reasoning_id
  source_semantic_states
  conclusion
  confidence_level
  confidence_explanation
  action_implications
  temporal_validity
  producing_engine

Explanation_Object (new — wraps Reasoning_Object):
  explanation_id
  target_object_id -> reasoning_id
  levels: [fractal decomposition of WHY this conclusion was reached]
```

The Reasoning_Object answers: "What did the system conclude?"
The Explanation_Object answers: "Why did the system conclude this, and how deep can I go?"

---

## RELATIONSHIP TO INVESTIGATION JOURNEY

The Investigation Journey IS the Explanation_Object traversed interactively:

```
User clicks: Nvidia
  -> Level 0: Asset Overview (Explanation_Object for asset state)
  -> Level 1: Why? (contributing signals)
  -> Level 2: Signal decomposition (thresholds, cross-confirmation)
  -> Level 3: State Changes (causal impulses)
  -> Level 4: Narratives (explanatory containers)
  -> Level 5: Expansion Tree (propagation paths)
```

The Investigation Journey is the UI manifestation of fractal explanation traversal.
The Explanation_Object is the data structure that makes it possible.

---

## ANTI-PATTERNS (What This Prevents)

### Anti-Pattern 1: Tooltip Hell
Without Explanation_Objects, UI defaults to:
```
[?] AI Dependency: HIGH
    -> Tooltip: "Your AI dependency is elevated because of concentrated exposure"
```
This is Level 1 only. No deeper. No fractal. No trust chain.

### Anti-Pattern 2: Text Wall
Without structured levels, explanations become:
```
"AI Dependency is HIGH because Nvidia is 32% and Broadcom is 11% and the
correlation engine shows 0.87 and the scenario engine projects -18% drawdown
under AI weakness and the narrative is Dominant and the expansion path shows..."
```
All levels collapsed into one paragraph. Unusable.

### Anti-Pattern 3: Dead Ends
Without fractal structure, drill-down stops:
```
User: "Why is AI Dependency HIGH?"
System: "Because of concentrated AI exposure."
User: "Why is exposure concentrated?"
System: [no answer — dead end]
```

The Explanation_Object guarantees: every "Why?" has an answer until Root_Node.

---

## WHAT THIS DOES NOT REQUIRE (NOW)

- Explanation rendering engine (future — P2 Concept Registry)
- Pre-computed explanation trees for all signals (future — on-demand generation)
- Natural language generation for explanations (future — rendering layer)
- UI components for fractal navigation (future — Figma/frontend)

What it DOES require NOW:
- Recognition that Explanation_Object is a first-class primitive
- Structural definition of 6 levels
- Fractal drilldown rules
- Compatibility with altitude, language, and timezone rendering
- Integration point with Reasoning_Object

---

## IMPLICATIONS FOR DESIGN

The Technical Design for the Market Organism Framework must ensure:

1. Every taxonomy entry (State_Change, Expansion, Dependency_Type) is structured
   to be EXPLAINABLE at all 6 levels
2. Worked examples in the taxonomy documents demonstrate the explanation chain
3. Cross-references between deliverables follow the explanation level structure
   (State_Change_Taxonomy provides Level 3, Narrative provides Level 4, Expansion provides Level 5)
4. The Temporal_Taxonomy provides the temporal context needed at Level 5

---

## KEY INSIGHT

MoneyHorst's primitives are now complete:

```
Knowledge Primitives:
  State_Change -> Narrative -> System -> Asset

Intelligence Primitives:
  Signal -> Semantic_State -> Reasoning_Object

Understanding Primitive:
  Explanation_Object (fractal decomposition of any intelligence into causal layers)

Rendering Dimensions:
  Language x Altitude x Timezone x Locale
```

The Explanation_Object is what transforms MoneyHorst from a signal system
into an Understanding Engine.

Without it: "AI Dependency = HIGH" (a fact)
With it: "AI Dependency is HIGH because... because... because..." (understanding)

The system that wins moves users from questions to causal understanding.
The Explanation_Object is the structural primitive that makes that movement possible.
