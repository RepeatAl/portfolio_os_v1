# Requirements Document

## Introduction

The Market Organism Framework defines the foundational world model for Portfolio OS. It establishes the formal definition of how markets propagate state changes as an organism — where impulses expand through dependency paths with latency, amplification, dampening, and feedback loops. This is a DEFINITION-ONLY specification (no engines, no code, no scores) that shifts the fundamental primitive from `Signal → Interpretation → Action` to `Impulse → Expansion → Cascade → Feedback → New State`.

This framework preserves the existing 12-domain architecture and canonical chain (SIGNALS → SEMANTICS → REASONING → REPORT) while providing the deeper conceptual foundation that the SIGNALS domain will eventually use to detect state changes.

## Glossary

- **State_Change**: A first-class primitive representing a discrete shift in market conditions. Root-level entity that initiates propagation. Never an asset.
- **Impulse**: The initial force or event that triggers a State_Change. The atomic unit of causation in the organism.
- **Expansion**: The process by which an Impulse propagates outward through dependency paths, affecting progressively more distant systems.
- **Cascade**: A chain of Expansions where one State_Change triggers subsequent State_Changes in connected systems.
- **Feedback_Loop**: A circular dependency path where downstream effects eventually influence the original source, creating Rückkopplung (feedback coupling).
- **Dependency_Path**: A directed connection between two nodes in the organism through which state changes propagate.
- **Temporal_Property**: A set of four attributes (Latency, Duration, Amplification, Dampening) that characterize how effects propagate along a Dependency_Path.
- **Latency**: The time delay between an Impulse occurring and its effect manifesting at a downstream node.
- **Duration**: The time span over which a propagated effect remains active.
- **Amplification**: The degree to which an effect grows stronger as it propagates (effect intensifies).
- **Dampening**: The degree to which an effect weakens as it propagates (effect attenuates).
- **Expansion_Order**: The distance from the originating Impulse measured in propagation hops (1st Order, 2nd Order, etc.).
- **Root_Node**: The origin point of a Cascade. Exclusively a State_Change, Event, Impulse, or Regime_Shift. Never an asset.
- **Organism_Graph**: The complete directed graph of all Dependency_Paths including feedback connections. Not a tree — a living network.
- **Dependency_Type**: A classification of the nature of a Dependency_Path (e.g., Price, Fundamental, Narrative, Flow, Supply_Chain).
- **Taxonomy**: A hierarchical classification system that categorizes entities by type before associating them with specific assets.
- **Framework_Document**: A formal definition document that establishes structure, classification, and principles without implementation.
- **Portfolio_OS**: The existing portfolio management system with 12 canonical domains and a SIGNALS → SEMANTICS → REASONING → REPORT chain.
- **Intelligence_Object**: A reusable, addressable unit of signal truth (single value, composite bundle, detail/provenance, static context, variable context, or derived intelligence) that consumers request rather than privately recalculate.
- **Static_Asset_Context**: Immutable or slowly-changing facts about an asset (sector, market cap tier, supply chain position, narrative membership) that are cached and refreshed by governance policy rather than recomputed per request.
- **Variable_Signal**: A signal value that changes with market conditions and must be refreshed by cadence (scheduled) or event trigger (reactive invalidation).
- **Derived_Intelligence**: A composite intelligence object computed from one or more upstream signals or contexts, invalidated only when its declared dependencies change.
- **Signal_Consumer**: Any engine, reasoning layer, or report renderer that requests signal truth from the canonical source rather than privately recalculating it.
- **Canonical_Signal_Truth**: The single authoritative value of a signal at a given point in time, owned by exactly one producing domain, and served to all consumers without duplication.
- **Signal_Bubble**: The unified registry of all canonical signal objects in Portfolio OS, serving as the single addressable namespace from which all consumers request intelligence. Signal_Bubble_v0 refers to the first-generation signals already extracted from Excel/dashboard data.
- **Portfolio_Core_Signal**: A first-generation signal derived from portfolio data (value, P/L, cash, invested capital, largest position, top/worst performer) that represents observable portfolio state.
- **Sensor_Layer**: The role that existing signals play within the Market Organism — they detect that a state change has occurred somewhere in the organism, without themselves being the causal primitive.
- **Signal_Lifecycle_Definition**: A mandatory registration record that every signal must pass before implementation, containing: signal_id, category, owner domain, input sources, static/variable classification, refresh policy, cache policy, provenance, consumers, invalidation rule, and implementation status.
- **Defined_Signal**: A signal that exists architecturally in the Signal Bubble registry with a complete Signal_Lifecycle_Definition but has no implementing engine yet.
- **Plain_Vanilla_Signal**: A simple, self-contained signal that may be individually implemented once its Signal_Lifecycle_Definition is complete and its lifecycle is clear.
- **Structured_Signal**: A complex signal (Narrative, Butterfly, Consensus-Lag, Model Fit, Game Theory, Convexity) that is architecturally positioned in the Signal Bubble as a future Intelligence_Object but must NOT be fully implemented in this spec.
- **Implemented_Signal**: A signal that has passed its full Signal_Lifecycle_Definition (owner, input, output, refresh, cache, provenance, consumers, invalidation all defined) and has a functioning engine producing it.

## Requirements

### Requirement 1: State Change Taxonomy Definition

**User Story:** As a portfolio architect, I want a formal taxonomy of all state change types, so that every market impulse can be classified by its nature before any asset association occurs.

#### Acceptance Criteria

1. THE Framework_Document SHALL define a State_Change taxonomy with exactly four top-level categories: Macro, Corporate, Narrative, and Events
2. THE Framework_Document SHALL enumerate the Macro category with at minimum the following sub-categories: Rates, Inflation, Oil, Liquidity, and FX
3. THE Framework_Document SHALL enumerate the Corporate category with at minimum the following sub-categories: Earnings, Guidance, Capex, M&A, and Buybacks
4. THE Framework_Document SHALL enumerate the Narrative category with at minimum the following sub-categories: AI, Security, Defense, Robotics, and Energy
5. THE Framework_Document SHALL enumerate the Events category with at minimum the following sub-categories: Elections, Wars, Pandemics, and Sporting_Events
6. THE Framework_Document SHALL define each sub-category with a description containing: (a) a one-sentence definition of the sub-category scope, (b) at least one concrete example of a State_Change belonging to that sub-category, and (c) at least one boundary example that does NOT belong to that sub-category
7. THE Framework_Document SHALL specify that every State_Change classification follows the mandatory hierarchy: State_Change type → Expansion type → Affected systems → Affected narratives → Affected assets
8. IF a State_Change could be classified under more than one top-level category, THEN THE Framework_Document SHALL specify a primary classification rule that assigns exactly one primary category based on the originating causal mechanism of the impulse
9. THE Framework_Document SHALL specify that each top-level category supports extension with additional sub-categories, and SHALL define the criteria a new sub-category must satisfy for inclusion: (a) it represents a distinct causal mechanism not already covered by existing sub-categories, and (b) it includes the same descriptive elements required by criterion 6

### Requirement 2: Root Node Invariant Enforcement

**User Story:** As a portfolio architect, I want the framework to enforce that assets are never root nodes, so that the system always reasons from causes to effects rather than from tickers to interpretations.

#### Acceptance Criteria

1. THE Framework_Document SHALL define Root_Nodes as exclusively one of: State_Changes, Events, Impulses, or Regime_Shifts, where Regime_Shift is defined as a fundamental change in the prevailing market structure or policy environment that redefines the operating context for multiple systems simultaneously
2. THE Framework_Document SHALL explicitly prohibit individual assets, tickers, or securities from serving as Root_Nodes
3. THE Framework_Document SHALL provide at least 4 examples of valid Root_Nodes including "Fed Hawkish Shift", "Nvidia Guidance Raise", "Oil Shock", and "World Cup Start", each annotated with which valid Root_Node type it represents
4. THE Framework_Document SHALL provide at least 2 examples of invalid Root_Nodes including individual ticker symbols and asset names, each annotated with an explanation of why it violates the invariant
5. THE Framework_Document SHALL define the classification question as "What kind of state change occurred?" and explicitly prohibit the inverse question "How do I classify this asset?"
6. THE Framework_Document SHALL define a disambiguation rule stating that a candidate Root_Node is valid only if it describes an observable shift in conditions or context, and invalid if it names a financial instrument without specifying what changed about it
7. IF a candidate Root_Node names a specific asset without describing a state change, THEN THE Framework_Document SHALL classify it as an invariant violation and require reformulation as the underlying state change that affected that asset

### Requirement 3: Expansion Taxonomy Definition

**User Story:** As a portfolio architect, I want a formal taxonomy of expansion types, so that the system can classify how state changes propagate through the market organism.

#### Acceptance Criteria

1. THE Framework_Document SHALL define Expansion as an ordered sequence of propagation hops measured by Expansion_Order, where each hop corresponds to the traversal of exactly one Dependency_Path between two nodes in the Organism_Graph
2. THE Framework_Document SHALL define at minimum four Expansion_Orders (1st through 4th), each with a distinguishing definition that specifies what qualifies an affected system as belonging to that order versus adjacent orders based on the number of Dependency_Path traversals from the originating Impulse
3. WHEN an Expansion_Order is defined, THE Framework_Document SHALL specify the causal distance in hops from the originating Impulse and the nature of the Dependency_Path connecting it to the prior order
4. THE Framework_Document SHALL provide at least one complete worked example showing an Impulse propagating through all four Expansion_Orders with at least two concrete affected systems identified at each order level
5. THE Framework_Document SHALL define termination of a propagation path as the point where no further identifiable Dependency_Path connects the last affected system to an additional system not already included in the Expansion sequence
6. IF a propagation path revisits a node already present in the Expansion sequence, THEN THE Framework_Document SHALL classify that path as a Feedback_Loop rather than a continuation of the Expansion_Order sequence

### Requirement 4: Dependency Type Classification

**User Story:** As a portfolio architect, I want a formal classification of dependency types, so that the system can distinguish between fundamentally different propagation mechanisms.

#### Acceptance Criteria

1. THE Framework_Document SHALL define exactly ten Dependency_Types: Price, Fundamental, Narrative, Flow, Ownership, Supply_Chain, Macro, Behavioral, Regulatory, and Butterfly
2. WHEN a Dependency_Type is defined, THE Framework_Document SHALL provide a description of its propagation mechanism that identifies the causal channel (economic, informational, or structural) through which a State_Change at the source produces an effect at the target
3. WHEN a Dependency_Type is defined, THE Framework_Document SHALL provide at least one concrete example that identifies the source entity, the target entity, and the specific mechanism connecting them
4. THE Framework_Document SHALL define how multiple Dependency_Types can coexist on a single Dependency_Path by specifying whether co-existing types are ordered or unordered, whether one type is designated as primary, and how combined types relate to the path's Temporal_Properties
5. THE Framework_Document SHALL distinguish Dependency_Types from correlation by defining dependencies as causal propagation mechanisms rather than statistical co-movement, and SHALL provide at least one contrastive example showing the same entity pair interpreted as correlation versus as a typed dependency
6. THE Framework_Document SHALL define differentiation criteria between each Dependency_Type such that no two types share identical causal channel, directionality, and propagation characteristics

### Requirement 5: Temporal Property Specification

**User Story:** As a portfolio architect, I want every expansion path to carry temporal properties, so that the system models propagation as a time-dependent process rather than a flat simultaneous event.

#### Acceptance Criteria

1. THE Framework_Document SHALL define exactly four Temporal_Properties for every Dependency_Path: Latency, Duration, Amplification, and Dampening
2. WHEN Latency is defined, THE Framework_Document SHALL specify it as the time delay between an Impulse occurring and its effect manifesting at the downstream node, expressed using discrete calendar-based time units (Day, Week, Month, Quarter, Year)
3. WHEN Duration is defined, THE Framework_Document SHALL specify it as the time span over which the propagated effect remains active, expressed using the same discrete calendar-based time units as Latency (Day, Week, Month, Quarter, Year)
4. WHEN Amplification is defined, THE Framework_Document SHALL specify it as a qualitative descriptor selected from an enumerated set of exactly five levels (None, Low, Moderate, High, Extreme) indicating whether and to what degree the effect intensifies during propagation
5. WHEN Dampening is defined, THE Framework_Document SHALL specify it as a qualitative descriptor selected from an enumerated set of exactly five levels (None, Low, Moderate, High, Extreme) indicating whether and to what degree the effect attenuates during propagation
6. THE Framework_Document SHALL provide at least one complete temporal propagation example showing all four Temporal_Properties (Latency, Duration, Amplification, and Dampening) at each Expansion_Order, with different Latency values demonstrating increasing time delay (e.g., Day 0, Month 1, Month 2, Month 3, Month 12)
7. THE Framework_Document SHALL explicitly prohibit numeric scores, weights, or probabilities for Temporal_Properties in this definition phase

### Requirement 6: Feedback Loop Mandate

**User Story:** As a portfolio architect, I want the framework to mandate feedback loops as a structural requirement, so that the organism model captures circular causation rather than reducing to a simple dependency tree.

#### Acceptance Criteria

1. THE Framework_Document SHALL define Feedback_Loops as circular Dependency_Paths where a sequence of directed edges forms a closed cycle such that a State_Change at node A propagates through one or more intermediate nodes and returns to influence node A
2. THE Framework_Document SHALL mandate that the Organism_Graph is not a Directed Acyclic Graph (DAG) by requiring the definition of at least one structural cycle, and by explicitly stating that acyclicity constraints are prohibited in the graph model
3. THE Framework_Document SHALL define a Feedback_Delay property as a qualitative temporal descriptor (consistent with Temporal_Properties) representing the characteristic time scale required for a downstream effect to propagate back to the source, expressed using the same qualitative categories as Latency (e.g., days, weeks, months, quarters)
4. THE Framework_Document SHALL provide at least one concrete example of a Feedback_Loop using real market entities from the State_Change taxonomy, showing a complete cycle of at least four nodes (e.g., Fed Rate Hike → Dollar Strengthens → Emerging Market Stress → Capital Flight to US → Fed Policy Pressure) with the Dependency_Type labeled on each edge
5. THE Framework_Document SHALL distinguish between the visible growth structure and the underlying feedback structure by defining that the growth structure is the acyclic subgraph representing forward propagation (Expansion_Orders 1 through N from a Root_Node), while the feedback structure consists of all back-edges that create cycles by connecting downstream nodes back to upstream nodes

### Requirement 7: Market Organism Principles Document

**User Story:** As a portfolio architect, I want a formal constitution of market organism principles, so that all future implementation decisions are constrained by these natural laws.

#### Acceptance Criteria

1. THE Framework_Document SHALL define at minimum five foundational principles that govern how markets propagate state changes, and each principle SHALL include a violation condition that describes what would constitute a breach of that principle
2. THE Framework_Document SHALL explicitly exclude data, assets, scores, and implementation details from the principles document
3. THE Framework_Document SHALL state that the market is an organism where state changes propagate through dependency paths, not a collection of assets with correlations
4. THE Framework_Document SHALL define the principle that taxonomy precedes asset association (classify the change, then identify affected assets)
5. THE Framework_Document SHALL define the principle that all propagation is temporal (nothing is instantaneous, nothing is permanent)
6. THE Framework_Document SHALL define the principle that feedback is structural (circular causation is the norm, not the exception)
7. THE Framework_Document SHALL define the principle that expansion has order (effects propagate in discrete Expansion_Order hops from source)
8. THE Framework_Document SHALL declare that these principles take precedence over any implementation decision, and SHALL require that any future design document reference which principles it satisfies

### Requirement 8: Exclusion Constraints

**User Story:** As a portfolio architect, I want explicit exclusion constraints documented, so that this definition phase remains pure and does not drift into premature implementation.

#### Acceptance Criteria

1. THE Framework_Document SHALL explicitly prohibit engine implementations, Python code, or executable logic within the framework deliverables
2. THE Framework_Document SHALL explicitly prohibit scoring algorithms, numeric weights, probabilities, ranking systems, or quantitative models that assign numeric values to entities or paths
3. THE Framework_Document SHALL explicitly prohibit dashboard designs, report templates, or visualization specifications
4. THE Framework_Document SHALL explicitly prohibit asset lists, ticker symbols, or position sizing from appearing as root-level entities, classification anchors, or organizational structures, while permitting their use solely as illustrative examples within worked propagation scenarios
5. THE Framework_Document SHALL explicitly prohibit correlation matrices or statistical co-movement measures as substitutes for causal Dependency_Paths
6. THE Framework_Document SHALL state a single rationale covering all exclusions defined in criteria 1 through 5: weights on an incomplete model produce false confidence
7. THE Framework_Document SHALL contain a dedicated exclusion constraints section that consolidates all prohibitions from criteria 1 through 5 in one reviewable location

### Requirement 9: Architectural Compatibility

**User Story:** As a portfolio architect, I want the framework to preserve compatibility with the existing Portfolio OS architecture, so that future integration does not require rebuilding the 12-domain model.

#### Acceptance Criteria

1. THE Framework_Document SHALL declare compatibility with the existing 12-domain model (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM) by explicitly stating that no domain interfaces, responsibilities, or boundaries are added, removed, or redefined by this framework
2. THE Framework_Document SHALL declare compatibility with the existing canonical chain (SIGNALS → SEMANTICS → REASONING → REPORT) by explicitly stating that the chain's sequence, direction, and domain responsibilities remain unchanged
3. THE Framework_Document SHALL define the future integration point: the SIGNALS domain will use this framework to detect state changes
4. THE Framework_Document SHALL define the signal layer's future role as a "sensor" that detects where in the organism a change has begun
5. THE Framework_Document SHALL preserve the existing runtime state model (8 states across 5 integrity dimensions) and pipeline orchestrator pattern by explicitly stating that no states, dimensions, or orchestration sequences are added, removed, or redefined
6. THE Framework_Document SHALL explicitly state its architectural relationship to Portfolio OS: the framework provides the conceptual world model that sits above the existing architecture, and does not replace, subsume, or restructure any existing domain or pipeline

### Requirement 10: Deliverable Structure

**User Story:** As a portfolio architect, I want the framework organized as five distinct definition documents, so that each aspect of the organism model is independently reviewable and maintainable.

#### Acceptance Criteria

1. THE Framework_Document SHALL be organized into exactly five deliverables: State_Change_Taxonomy, Expansion_Taxonomy, Dependency_Types, Temporal_Taxonomy, and Market_Organism_Principles
2. WHEN the State_Change_Taxonomy deliverable is defined, THE Framework_Document SHALL contain a complete hierarchical classification that answers the question "What kinds of impulses exist?" by enumerating all top-level categories and their sub-categories with descriptions
3. WHEN the Expansion_Taxonomy deliverable is defined, THE Framework_Document SHALL contain a complete ordered classification that answers the question "What kinds of expansion/propagation exist?" by defining each Expansion_Order with criteria and at least one worked example
4. WHEN the Dependency_Types deliverable is defined, THE Framework_Document SHALL contain a complete type enumeration that answers the question "What kinds of causal connections exist?" by defining each Dependency_Type with its propagation mechanism and at least one concrete example
5. WHEN the Temporal_Taxonomy deliverable is defined, THE Framework_Document SHALL contain definitions of all four Temporal_Properties that answer the question "How fast do effects propagate?" by specifying Latency, Duration, Amplification, and Dampening with at least one temporal propagation example
6. WHEN the Market_Organism_Principles deliverable is defined, THE Framework_Document SHALL contain a set of foundational principles that answer the question "What are the natural laws of market state propagation?" by stating each principle as a testable constraint on system behavior
7. THE Framework_Document SHALL structure each deliverable as a self-contained document that includes its own scope statement, references the shared Glossary for term definitions, and does not require reading other deliverables to be understood in isolation
8. IF a deliverable references a concept defined in another deliverable, THEN THE Framework_Document SHALL include an explicit cross-reference identifying the source deliverable by name rather than duplicating the definition
9. THE Framework_Document SHALL ensure that no deliverable exceeds a single concern boundary: taxonomy documents define classifications only, and the principles document defines constraints only

### Requirement 11: Signal Reusability and Cached Context Invariant

**User Story:** As a portfolio architect, I want all signals, signal details, static asset facts, derived metrics, and provenance metadata modeled as reusable intelligence objects, so that no consumer privately recalculates canonical signal truth and the system maintains a single authoritative source for every piece of intelligence.

#### Acceptance Criteria

1. THE Framework_Document SHALL define all signals, signal details, static asset facts, derived metrics, and provenance metadata as reusable Intelligence_Objects that are addressable, versionable, and served from a canonical source
2. THE Framework_Document SHALL explicitly prohibit any Signal_Consumer from privately recalculating Canonical_Signal_Truth, and SHALL require that consumers request intelligence from the authoritative producing domain
3. THE Framework_Document SHALL define exactly six request types that a Signal_Consumer may issue: (a) single signal value, (b) composite signal bundle, (c) signal detail/provenance, (d) static asset context, (e) variable market context, and (f) derived intelligence object
4. THE Framework_Document SHALL define Static_Asset_Context as cached intelligence that is refreshed exclusively by governance policy (not per-request), and SHALL specify that the refresh policy is declared at the context-type level rather than per-consumer
5. THE Framework_Document SHALL define Variable_Signals as intelligence that must be refreshed by one of two mechanisms: scheduled cadence (time-based refresh) or event trigger (reactive invalidation upon upstream State_Change detection)
6. THE Framework_Document SHALL define Derived_Intelligence as composite objects that are invalidated only when one or more of their declared upstream dependencies change, and SHALL require that each Derived_Intelligence object explicitly declares its dependency set
7. THE Framework_Document SHALL specify that the Signal Reusability invariant applies across all four levels of the canonical chain (SIGNALS, SEMANTICS, REASONING, REPORT), ensuring that no layer duplicates intelligence already produced by an upstream layer
8. IF a Signal_Consumer requires intelligence that does not yet exist as a canonical Intelligence_Object, THEN THE Framework_Document SHALL require that the intelligence be formally registered with a producing domain before any consumer may use it, prohibiting ad-hoc private computation as a substitute
9. THE Framework_Document SHALL define the relationship between Intelligence_Objects and the Organism_Graph: each node in the Organism_Graph that represents an observable state produces Intelligence_Objects that downstream nodes consume through declared Dependency_Paths

### Requirement 12: Legacy Signal Preservation and Signal Bubble v0

**User Story:** As a portfolio architect, I want all existing Excel-derived dashboard metrics preserved as first-generation canonical signal objects in the Signal Bubble, so that the Market Organism Framework treats them as sensors rather than replacing them, and all future consumers reuse them from a single registry.

#### Acceptance Criteria

1. THE Framework_Document SHALL define all existing Excel-derived dashboard metrics as first-generation canonical signal objects collectively designated Signal_Bubble_v0, and SHALL explicitly state that these signals are NOT legacy artifacts to be discarded but the first real Sensor_Layer of the system
2. THE Framework_Document SHALL enumerate the following signal categories as part of Signal_Bubble_v0: (a) Portfolio Core Signals (total portfolio value, total P/L, cash EUR, invested capital, total capital, largest position, top performer, worst performer), (b) Allocation Signals (technology, semiconductors, defense, healthcare, ETFs, USD exposure), (c) Risk Signals (portfolio health, risk review count, concentration score, max position, max drawdown, portfolio stability, risk alerts), (d) Performance Signals (portfolio performance, equity curve, 7D return, trend signals), (e) Deployment Signals (capital deployment, cash readiness, portfolio efficiency, deployment signal), and (f) Regime/PM Signals (market regime, portfolio bias, scenario readiness, high priority candidates, morning briefing outputs)
3. THE Framework_Document SHALL explicitly prohibit any consumer (dashboard, report, scenario module, or future engine) from privately rebuilding or recalculating Signal_Bubble_v0 signals, and SHALL require that all consumers request these signals from the canonical Signal Bubble registry
4. THE Framework_Document SHALL define the architectural relationship between Signal_Bubble_v0 and the Market Organism: the organism does NOT replace these signals — it uses them as sensors that detect where in the organism a state change has manifested at the portfolio level
5. THE Framework_Document SHALL declare that Signal_Bubble_v0 signals are reusable by all future layers including but not limited to: Morning Briefing, Asset Detail Page, Portfolio Fit, Market Fit, Model Fit, Butterfly Simulation, Scenario Engine, PM Control Center, and Report Pipeline
6. THE Framework_Document SHALL require that Signal_Bubble_v0 signals be migrated into the Signal Bubble / Signal Registry as Intelligence_Objects (per Requirement 11) rather than remaining as privately computed values inside individual Excel sheets or dashboard components
7. THE Framework_Document SHALL define the migration principle: existing signals retain their semantic meaning and calculation logic but gain addressability, versioning, caching policy, and provenance metadata through registration in the Signal Bubble
8. THE Framework_Document SHALL explicitly state that the Market Organism Graph consumes Signal_Bubble_v0 signals as leaf-node observations — they represent the portfolio's response to upstream State_Changes propagating through the organism, making them evidence of propagation rather than causes of it
9. IF a future engine or layer requires a signal that already exists in Signal_Bubble_v0, THEN THE Framework_Document SHALL prohibit reimplementation and require consumption from the canonical registry, enforcing the single-source-of-truth principle across all system generations

### Requirement 13: Signal Lifecycle Definition Gate

**User Story:** As a portfolio architect, I want every signal to pass a mandatory Signal Lifecycle Definition before implementation, so that no bulk signal implementation occurs and every signal enters the system with full architectural clarity about its ownership, refresh behavior, consumers, and invalidation rules.

#### Acceptance Criteria

1. THE Framework_Document SHALL explicitly prohibit bulk signal implementation, and SHALL require that every signal passes a complete Signal_Lifecycle_Definition gate before any implementation work begins
2. THE Framework_Document SHALL define the Signal_Lifecycle_Definition as a mandatory registration record containing exactly the following fields: (a) signal_id, (b) category, (c) owner domain, (d) input sources, (e) static or variable classification, (f) refresh policy, (g) cache policy, (h) provenance, (i) consumers, (j) invalidation rule, and (k) implementation status
3. THE Framework_Document SHALL require that the signal_id field uniquely identifies the signal within the Signal Bubble namespace and follows a consistent naming convention
4. THE Framework_Document SHALL require that the owner domain field identifies exactly one domain from the existing 12-domain model (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM) that is authoritative for producing this signal
5. THE Framework_Document SHALL require that the static or variable classification determines whether the signal follows Static_Asset_Context caching rules (refreshed by governance policy) or Variable_Signal refresh rules (refreshed by cadence or event trigger)
6. THE Framework_Document SHALL require that the refresh policy field specifies either a scheduled cadence (for Variable_Signals) or a governance-defined refresh interval (for Static_Asset_Context), and that the cache policy field specifies the maximum staleness tolerance before the signal is considered expired
7. THE Framework_Document SHALL require that the consumers field enumerates all known downstream consumers that will request this signal, establishing the dependency graph for invalidation propagation
8. THE Framework_Document SHALL require that the invalidation rule field specifies the exact conditions under which the signal's cached value becomes invalid and must be recomputed (dependency change, time expiry, or event trigger)
9. THE Framework_Document SHALL define three implementation statuses: (a) Defined_Signal (architecturally positioned, lifecycle complete, no engine yet), (b) Implemented_Signal (lifecycle complete and engine producing it), and (c) Structured_Signal (architecturally positioned as future Intelligence_Object, must NOT be implemented in this spec)
10. IF a signal lacks any one of the eleven required Signal_Lifecycle_Definition fields, THEN THE Framework_Document SHALL classify it as incomplete and prohibit its implementation until all fields are specified
