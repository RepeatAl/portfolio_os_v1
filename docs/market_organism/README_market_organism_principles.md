# Market Organism Principles

---
artifact_id: market_organism.principles_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Defines the foundational natural laws governing market state propagation
ssot_relationship: canonical
topic: market_organism_principles
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism.shared_glossary_reference]
---

## Scope Statement

This document defines the foundational principles — the natural laws — that govern how markets propagate state changes as an organism. It establishes six formal constraints on system behavior: organism-over-collection, taxonomy-before-assets, temporal propagation, structural feedback, ordered expansion, and causation-over-correlation. These principles constrain all future design and implementation decisions across the Market Organism Framework. This document does NOT contain data, asset lists, scoring algorithms, implementation details, engine behavior, numeric weights, probabilities, or any executable logic.

---

## Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary

This document does not define terms. It consumes them.

---

## Principles


### Principle 1: Organism over Collection

`principle.organism_over_collection`

**Statement**: The market is a living organism where State_Changes propagate through Dependency_Paths, not a collection of assets with correlations.

**Implication**: System design must model propagation mechanics (impulses, expansion, feedback) rather than asset-level statistical relationships. The fundamental unit of analysis is the State_Change and its causal propagation, never the asset and its price movement.

**Violation Condition**: Any design, model, or analysis that treats assets as independent entities connected only by statistical correlation — rather than as downstream observation points in a propagating organism — violates this principle.

**Example of Compliance**: A system detects a "Fed Hawkish Shift" (State_Change) and traces its propagation through the Organism_Graph via Dependency_Paths to identify which systems and narratives are affected, eventually reaching specific assets as leaf-node observations.

**Example of Violation**: A system observes that two assets moved together historically and infers a relationship between them without identifying the causal State_Change or Dependency_Path that connects them through the organism.

**Satisfies**: Requirement 7.3

---

### Principle 2: Taxonomy Precedes Assets

`principle.taxonomy_precedes_assets`

**Statement**: Every analysis must classify the State_Change first, then identify affected assets — never the reverse.

**Implication**: The classification hierarchy is mandatory and inviolable: State_Change type → Expansion type → Affected systems → Affected narratives → Affected assets. Assets are always leaf nodes in this hierarchy. No system may begin reasoning from an asset and work backward to infer a State_Change.

**Violation Condition**: Any design that begins with an asset (ticker, security, position) and attempts to derive or infer the originating State_Change from asset behavior violates this principle. Any system that uses an asset as a Root_Node violates this principle.

**Example of Compliance**: An analyst observes unusual market activity and asks "What kind of state change occurred?" — classifying the impulse as `sc.macro.rates` (a rate regime shift) before tracing its expansion to affected systems, narratives, and ultimately assets.

**Example of Violation**: An analyst observes that a specific equity declined and asks "How do I classify this asset's movement?" — starting from the asset and attempting to reverse-engineer the cause, treating the asset as the root of analysis.

**Satisfies**: Requirement 7.4

---

### Principle 3: All Propagation is Temporal

`principle.all_propagation_temporal`

**Statement**: Every propagation through a Dependency_Path carries Temporal_Properties — nothing is instantaneous, nothing is permanent.

**Implication**: Every edge in the Organism_Graph must carry Latency (time delay before effect manifests), Duration (how long the effect persists), Amplification (whether the effect intensifies), and Dampening (whether the effect attenuates). No propagation may be modeled as simultaneous across all affected systems. No effect may be modeled as eternal.

**Violation Condition**: Any design that models propagation as instantaneous (all effects manifest simultaneously) or permanent (effects never decay) violates this principle. Any Dependency_Path that lacks explicit Temporal_Properties violates this principle.

**Example of Compliance**: A system models a "Corporate Guidance Raise" propagating to direct suppliers with Latency of Day, then to sector peers with Latency of Week, then to narrative membership with Latency of Month — each hop carrying distinct temporal characteristics.

**Example of Violation**: A system models a State_Change as affecting all connected systems simultaneously without distinguishing when each effect manifests, or models an effect as persisting indefinitely without a Duration boundary.

**Satisfies**: Requirement 7.5

---

### Principle 4: Feedback is Structural

`principle.feedback_structural`

**Statement**: Circular causation through Feedback_Loops is the structural norm of the Organism_Graph, not an exception or error condition.

**Implication**: The Organism_Graph is explicitly NOT a Directed Acyclic Graph (DAG). Cycles are mandatory structural features. Any model that enforces acyclicity misrepresents the organism. Feedback_Loops are how the organism self-regulates — downstream effects propagate back to influence upstream sources through identifiable Dependency_Paths with measurable Feedback_Delay.

**Violation Condition**: Any design that enforces acyclicity constraints on the Organism_Graph, treats feedback as an error condition to be eliminated, or models propagation as strictly forward-only without back-edges violates this principle.

**Example of Compliance**: A system models the cycle: Rate Hike → Dollar Strengthens → Emerging Market Stress → Capital Flight to US → Fed Policy Pressure — recognizing this as a structural Feedback_Loop with a characteristic Feedback_Delay, not an error in the graph.

**Example of Violation**: A system detects that a propagation path revisits a previously affected node and discards the path as "circular" or "invalid" rather than classifying it as a Feedback_Loop with its own temporal characteristics.

**Satisfies**: Requirement 7.6

---

### Principle 5: Expansion Has Order

`principle.expansion_has_order`

**Statement**: Effects propagate in discrete Expansion_Order hops from the originating Impulse — each hop traverses exactly one Dependency_Path.

**Implication**: Propagation is not a diffuse wave but a structured sequence of discrete hops. 1st Order effects are exactly 1 hop from the Root_Node. 2nd Order effects are exactly 2 hops. The Expansion_Order of any affected system is determined by the shortest path from the originating Impulse measured in Dependency_Path traversals.

**Violation Condition**: Any design that models propagation as a continuous diffusion without discrete hop boundaries, or that fails to distinguish between effects at different Expansion_Orders, violates this principle. Any system that assigns an Expansion_Order without counting the actual number of Dependency_Path traversals from the Root_Node violates this principle.

**Example of Compliance**: A system traces a "Macro Liquidity Tightening" through 1st Order (direct rate-sensitive systems), 2nd Order (systems dependent on 1st-order systems via identified Dependency_Paths), 3rd Order (systems connected to 2nd-order via further paths), maintaining clear boundaries between each order.

**Example of Violation**: A system labels all affected systems as "impacted" without distinguishing whether they are 1 hop, 2 hops, or 4 hops from the originating Impulse — treating propagation as a flat, undifferentiated event.

**Satisfies**: Requirement 7.7

---

### Principle 6: Causation over Correlation

`principle.causation_over_correlation`

**Statement**: Dependencies in the Organism_Graph are causal mechanisms with identifiable propagation channels, not statistical patterns of co-movement.

**Implication**: Every Dependency_Path must identify a specific causal channel (economic, informational, or structural) through which a State_Change at the source produces an effect at the target. Statistical correlation — no matter how strong — is never a substitute for a typed, causal Dependency_Path. Two entities that move together without an identifiable causal mechanism are NOT connected in the Organism_Graph.

**Violation Condition**: Any design that uses correlation coefficients, statistical co-movement measures, or pattern-matching as the basis for establishing Dependency_Paths violates this principle. Any Dependency_Path that cannot identify its specific causal channel and propagation mechanism violates this principle.

**Example of Compliance**: A system establishes a Dependency_Path between an oil producer and an airline by identifying the causal channel (economic: input cost propagation via Supply_Chain Dependency_Type) and the specific mechanism (crude oil price increase raises jet fuel costs, compressing airline operating margins).

**Example of Violation**: A system observes that an oil producer and an airline have historically moved inversely and establishes a "negative correlation dependency" between them without identifying the causal mechanism, channel, or Dependency_Type that connects them.

**Satisfies**: Requirements 4.5, 7.3

---

## Precedence Declaration

These six principles constitute the foundational natural laws of the Market Organism Framework. They take absolute precedence over any implementation decision, engine design, scoring algorithm, or system architecture choice made in any downstream layer.

**Binding constraints:**

1. Any future design document MUST explicitly reference which principles it satisfies.
2. Any implementation that conflicts with a principle MUST be redesigned to comply — the principle is never relaxed to accommodate implementation convenience.
3. If a design decision cannot satisfy a principle, the decision MUST be escalated for architectural review rather than silently violating the principle.
4. Principles are ordered by number for reference purposes only — they are co-equal in authority. No principle overrides another.

---

## Content Exclusions

This document is a **constraints-only** document. It defines what the system MUST obey, not how the system operates.

The following are explicitly excluded from this document:

| Excluded Content | Rationale |
|-----------------|-----------|
| Data (market data, price feeds, historical series) | Principles constrain behavior, not data |
| Assets (tickers, securities, positions, portfolios) | Assets are leaf-node observations, not principles |
| Scores (numeric rankings, confidence values, weights) | Principles are qualitative constraints, not quantitative measures |
| Implementation details (code, algorithms, engines) | Principles define WHAT must hold, not HOW to achieve it |
| Dashboards or visualizations | Principles are consumed by systems, not displayed to users |
| Temporal values (specific dates, durations, latencies) | Principles define that temporality exists, not specific temporal values |

---

## Exclusion Constraints

This section consolidates all prohibitions that apply to this document and to any system claiming compliance with these principles. These constraints derive from Requirements 8.1 through 8.7.

### Prohibited Content

| # | Prohibition | Description |
|---|-------------|-------------|
| EC-1 | Engine implementations | No Python code, executable logic, or engine behavior may appear in this document or be justified by reference to these principles alone |
| EC-2 | Scoring algorithms | No numeric weights, probabilities, ranking systems, confidence scores, or quantitative models that assign numeric values to entities or paths |
| EC-3 | Dashboard specifications | No dashboard designs, report templates, visualization specifications, or UI mockups |
| EC-4 | Asset lists as root entities | No asset lists, ticker symbols, or position sizing may appear as root-level entities, classification anchors, or organizational structures. Assets are permitted ONLY as illustrative leaf-node examples within worked propagation scenarios |
| EC-5 | Correlation matrices | No correlation matrices or statistical co-movement measures may substitute for causal Dependency_Paths |

### Rationale

All exclusions share a single rationale: **weights on an incomplete model produce false confidence**. The definition layer must remain pure so that future implementation layers can build on solid conceptual foundations without inheriting premature quantitative commitments.

### Enforcement

Any content matching the prohibited categories above constitutes a hard error. The document is invalid until the prohibited content is removed and replaced with either:
- A qualitative description (for concepts that need expression), or
- A cross-reference to a future implementation layer (for concepts that belong elsewhere)

---

## Architectural Compatibility

This section declares the relationship between the Market Organism Principles and the existing Portfolio OS architecture. These principles provide the conceptual world model that sits ABOVE the existing architecture. They do not replace, subsume, or restructure any existing domain or pipeline.

### 12-Domain Model Preservation (Req 9.1)

The existing 12-domain model is preserved without modification:

| Domain | Status |
|--------|--------|
| GOV | Unchanged — no interfaces, responsibilities, or boundaries redefined |
| ARCH | Unchanged — this framework operates within ARCH's authority |
| SIGNALS | Unchanged — future integration point (see below) |
| SEMANTICS | Unchanged — responsibilities preserved |
| REASONING | Unchanged — responsibilities preserved |
| REPORT | Unchanged — responsibilities preserved |
| STATE | Unchanged — responsibilities preserved |
| DATA | Unchanged — responsibilities preserved |
| USER | Unchanged — responsibilities preserved |
| DEPLOY | Unchanged — responsibilities preserved |
| MEMORY | Unchanged — responsibilities preserved |
| SIM | Unchanged — responsibilities preserved |

No domain interfaces, responsibilities, or boundaries are added, removed, or redefined by these principles.

### Canonical Chain Preservation (Req 9.2)

The canonical processing chain remains unchanged:

```
SIGNALS → SEMANTICS → REASONING → REPORT
```

The chain's sequence, direction, and domain responsibilities remain exactly as defined in the existing architecture. These principles constrain what flows through the chain but do not alter the chain itself.

### Future SIGNALS Integration Point (Req 9.3)

The SIGNALS domain will use this framework to detect State_Changes. Specifically:
- The State_Change_Taxonomy provides the classification model that SIGNALS sensors will detect
- The Expansion_Taxonomy provides the propagation model that SIGNALS will trace
- The Dependency_Types provide the edge labels that SIGNALS will identify

This is a FUTURE integration declaration. No implementation exists in this document.

### Signal Layer as Sensor (Req 9.4)

The signal layer's future role is defined as a **sensor** — it detects where in the organism a State_Change has begun. Signals are leaf-node observations in the Organism_Graph. They provide evidence that propagation has occurred at a specific point. They do not themselves cause propagation.

Existing Signal_Bubble_v0 signals are the first-generation Sensor_Layer. They are NOT legacy artifacts to be discarded — they are the first real sensors of the system.

### Runtime State Model Preservation (Req 9.5)

The existing runtime state model (8 states across 5 integrity dimensions) and pipeline orchestrator pattern are preserved without modification. No states, dimensions, or orchestration sequences are added, removed, or redefined by these principles.

### Conceptual World Model Relationship (Req 9.6)

This framework provides the **conceptual world model** that sits above the existing architecture:

```
Layer 0: Market Organism Framework (THIS — Territory Definition)
         ↓ constrains
Layer 1+: Existing Architecture (12 domains, canonical chain, runtime state model)
```

The framework does NOT:
- Replace any existing domain
- Subsume any existing pipeline
- Restructure any existing interface
- Override any existing domain responsibility

The framework DOES:
- Define the conceptual territory that the architecture operates within
- Provide the causal model that future SIGNALS implementations will detect
- Constrain future design decisions through these principles

### Signal Architecture Compatibility

This subsection declares the relationship between the Market Organism Principles and the Signal Architecture. These are DECLARATIONS of compatibility — they state what the organism framework preserves and respects. They do NOT implement signal logic.

#### Signal Reusability Invariant

The following invariant applies across all four levels of the canonical chain (SIGNALS, SEMANTICS, REASONING, REPORT):

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
7. No layer in the canonical chain may duplicate intelligence already produced by an upstream layer.

(See: README_state_change_taxonomy, Section: Signal Architecture Compatibility)
(See: README_dependency_types_v2, Section: Signal Architecture Compatibility)
(See: README_temporal_taxonomy, Section: Signal Architecture Compatibility)
(See: README_expansion_taxonomy, Section: Signal Architecture Compatibility)

#### Signal_Bubble_v0 Preservation

1. Existing Excel-derived metrics are **first-generation canonical signal objects** (Signal_Bubble_v0). They are NOT legacy artifacts to be discarded — they are the first real Sensor_Layer of the system.
2. Signal_Bubble_v0 encompasses the following signal categories:
   - **Portfolio Core** — total portfolio value, total P/L, cash EUR, invested capital, total capital, largest position, top performer, worst performer
   - **Allocation** — technology, semiconductors, defense, healthcare, ETFs, USD exposure
   - **Risk** — portfolio health, risk review count, concentration score, max position, max drawdown, portfolio stability, risk alerts
   - **Performance** — portfolio performance, equity curve, 7D return, trend signals
   - **Deployment** — capital deployment, cash readiness, portfolio efficiency, deployment signal
   - **Regime/PM** — market regime, portfolio bias, scenario readiness, high priority candidates, morning briefing outputs
3. No consumer (dashboard, report, scenario module, or future engine) may privately rebuild or recalculate Signal_Bubble_v0 signals. All consumers request these signals from the canonical Signal Bubble registry.
4. **Organism relationship**: Signal_Bubble_v0 signals are leaf-node observations (sensors) in the Organism_Graph. They detect that a State_Change has propagated to the portfolio level. They are evidence of propagation, not causes of it.
5. Signal_Bubble_v0 signals are reusable by all future layers including: Morning Briefing, Asset Detail Page, Portfolio Fit, Market Fit, Model Fit, Butterfly Simulation, Scenario Engine, PM Control Center, and Report Pipeline.

#### Signal_Lifecycle_Definition Gate

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
4. Any signal referenced in worked examples must have a Signal_Lifecycle_Definition before implementation.

---

## Cross-References

This document references and is referenced by the following deliverables:

| Deliverable | Relationship | Specific References |
|-------------|-------------|---------------------|
| README_state_change_taxonomy | Constrains | (See: README_state_change_taxonomy, Section: Classification Hierarchy) — Principle 2 (Taxonomy Precedes Assets) governs the mandatory classification ordering |
| README_dependency_types_v2 | Constrains | (See: README_dependency_types_v2, Section: Dependency vs. Correlation) — Principle 6 (Causation over Correlation) governs how dependencies are established |
| README_temporal_taxonomy | Constrains | (See: README_temporal_taxonomy, Section: Latency Definition) — Principle 3 (All Propagation is Temporal) mandates temporal properties on every path |
| README_expansion_taxonomy | Constrains | (See: README_expansion_taxonomy, Section: Expansion Definition) — Principle 5 (Expansion Has Order) governs discrete hop structure |
| README_shared_glossary_reference | Consumes | (See: README_shared_glossary_reference, Section: Cross-Reference Convention) — This document follows the shared semantic contract |

### Constraint Direction

These principles **constrain all** other deliverables. The constraint is unidirectional:

```
Market_Organism_Principles
    ↓ constrains
State_Change_Taxonomy
Dependency_Types_v2
Temporal_Taxonomy
Expansion_Taxonomy
```

No taxonomy document may introduce content that violates any principle defined here. If a conflict arises, the principle prevails and the taxonomy must be revised.

---

## Satisfies

This document satisfies the following requirements:

| Requirement | How Satisfied |
|-------------|---------------|
| 7.1 | Six foundational principles defined, each with a violation condition |
| 7.2 | Content Exclusions section explicitly excludes data, assets, scores, implementation details |
| 7.3 | Principle 1 (Organism over Collection) and Principle 6 (Causation over Correlation) |
| 7.4 | Principle 2 (Taxonomy Precedes Assets) |
| 7.5 | Principle 3 (All Propagation is Temporal) |
| 7.6 | Principle 4 (Feedback is Structural) |
| 7.7 | Principle 5 (Expansion Has Order) |
| 7.8 | Precedence Declaration section |
| 8.1 | Exclusion Constraints EC-1: engine implementations prohibited |
| 8.2 | Exclusion Constraints EC-2: scoring algorithms prohibited |
| 8.3 | Exclusion Constraints EC-3: dashboard specifications prohibited |
| 8.4 | Exclusion Constraints EC-4: asset lists as root entities prohibited |
| 8.5 | Exclusion Constraints EC-5: correlation matrices prohibited |
| 8.6 | Exclusion Constraints Rationale: weights on incomplete model produce false confidence |
| 8.7 | Exclusion Constraints section consolidates all prohibitions in one reviewable location |
| 9.1 | Architectural Compatibility: 12-domain model preserved |
| 9.2 | Architectural Compatibility: canonical chain preserved |
| 9.3 | Architectural Compatibility: future SIGNALS integration point declared |
| 9.4 | Architectural Compatibility: signal layer as sensor defined |
| 9.5 | Architectural Compatibility: runtime state model preserved |
| 9.6 | Architectural Compatibility: conceptual world model relationship stated |
| 11.1 | Signal Architecture Compatibility: all signals defined as reusable Intelligence_Objects (addressable, versionable, canonical source) |
| 11.2 | Signal Architecture Compatibility: prohibits private recalculation of Canonical_Signal_Truth |
| 11.3 | Signal Architecture Compatibility: defines exactly six request types for Signal_Consumers |
| 11.4 | Signal Architecture Compatibility: defines Static_Asset_Context as cached, refreshed by governance policy |
| 11.5 | Signal Architecture Compatibility: defines Variable_Signals refreshed by cadence or event trigger |
| 11.6 | Signal Architecture Compatibility: defines Derived_Intelligence invalidated only when upstream dependencies change |
| 11.7 | Signal Architecture Compatibility: invariant applies across all four canonical chain levels |
| 11.8 | Signal Architecture Compatibility: requires formal registration before consumer use |
| 11.9 | Signal Architecture Compatibility: defines Intelligence_Object relationship to Organism_Graph |
| 12.1 | Signal Architecture Compatibility: defines Signal_Bubble_v0 as first-generation canonical signal objects (NOT legacy) |
| 12.2 | Signal Architecture Compatibility: enumerates six signal categories (Portfolio Core, Allocation, Risk, Performance, Deployment, Regime/PM) |
| 12.3 | Signal Architecture Compatibility: prohibits private rebuilding or recalculation of Signal_Bubble_v0 signals |
| 12.4 | Signal Architecture Compatibility: defines organism relationship (signals as sensors detecting propagation) |
| 12.5 | Signal Architecture Compatibility: declares reusability by all future layers |
| 12.6 | Signal Architecture Compatibility: requires migration into Signal Bubble as Intelligence_Objects |
| 12.7 | Signal Architecture Compatibility: defines migration principle (retain semantics, gain addressability) |
| 12.8 | Signal Architecture Compatibility: defines signals as leaf-node observations (evidence of propagation, not causes) |
| 12.9 | Signal Architecture Compatibility: prohibits reimplementation of existing signals |
| 13.1 | Signal Architecture Compatibility: prohibits bulk signal implementation, requires individual lifecycle gate |
| 13.2 | Signal Architecture Compatibility: defines 11-field mandatory Signal_Lifecycle_Definition |
| 13.3 | Signal Architecture Compatibility: requires unique signal_id within Signal Bubble namespace |
| 13.4 | Signal Architecture Compatibility: requires exactly one owner domain from 12-domain model |
| 13.5 | Signal Architecture Compatibility: classification determines caching vs refresh rules |
| 13.6 | Signal Architecture Compatibility: refresh_policy and cache_policy fields specified |
| 13.7 | Signal Architecture Compatibility: consumers field enumerates downstream consumers |
| 13.8 | Signal Architecture Compatibility: invalidation_rule specifies exact invalidation conditions |
| 13.9 | Signal Architecture Compatibility: defines three implementation statuses (Defined_Signal, Structured_Signal, Implemented_Signal) |
| 13.10 | Signal Architecture Compatibility: incomplete lifecycle definition prohibits implementation |
