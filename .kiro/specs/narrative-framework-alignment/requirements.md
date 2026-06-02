# Requirements Document

## Introduction

This spec aligns the existing Narrative Framework (`docs/README_narrative_framework.md`) to the Market Organism Layer 0 definition standard. The Narrative Framework already correctly positions Narrative as the explanatory container in the primitive chain (`State_Change → Narrative → System → Asset`). This alignment formalizes the conventions, canonical IDs, cross-references, and architectural compatibility declarations required by Market Organism Layer 0.

This is a **definition-layer alignment only**. No engines, code, scoring, or runtime behavior is produced. The existing Narrative ontology is preserved and strengthened — not replaced or restructured.

## Glossary

This document does NOT duplicate the Market Organism glossary.

**Canonical glossary location**: `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary
(See: README_shared_glossary_reference, Section: Glossary Usage Rules)

- **Narrative_Container** (CANDIDATE): The structural role of Narrative as the explanatory grouping that organizes how a State_Change's effects are understood by market participants.
- **Narrative_Membership** (CANDIDATE): The relationship between an Asset and a Narrative, classified by type (primary/secondary/emerging/legacy) and qualitative strength.
- **Narrative_Interaction** (CANDIDATE): A causal relationship between a State_Change and a Narrative, classified by type (Creates/Strengthens/Weakens/Kills/Revives).

**Flagged terminology**:
- `strength-weighted`: REJECTED — future-leak risk. Must NOT be preserved as accepted terminology.
- `velocity`: NOT a Temporal_Taxonomy property. If retained, must be explicitly treated as a narrative-specific qualitative observation candidate pending design review.

## Scope

### In Scope

- Canonical `narrative.*` identity namespace definition and assignment rules
- Lifecycle state canonical IDs (`narrative.lifecycle.*`)
- State_Change-to-Narrative interaction formalization with canonical IDs
- Narrative-as-Container vs `dep.narrative` dependency mechanism distinction
- Cross-reference convention adoption: `(See: [Deliverable_Name], Section: [Section_Title])`
- Explanation traversal contract (Level 4 in the explanation chain)
- Signal_Bubble_v0 sensor relationship declaration
- Exclusion constraints section (consolidated prohibitions)
- Architectural compatibility declarations (12-domain, canonical chain, runtime state model)
- Rendering independence (canonical ID ≠ display text)
- Narrative extension criteria (what qualifies a new narrative for canonical registry)
- Narrative feedback loop integration with non-DAG mandate
- YAML metadata header conforming to Layer 0 pattern

### Out of Scope

See Section "Out of Scope" below.

## Requirements

The following are explicitly excluded from this spec:

- Engine implementations (Asset-to-Narrative Registry, Relevance Engine, Propagation Engine)
- Runtime code, Python code, or any executable logic
- Actual narrative instance population (which specific narratives exist in the registry)
- Scoring algorithms or numeric strength values for narratives
- Ranking logic for narrative priority or dominance
- Probability assignments to narrative lifecycle transitions
- Optimization logic for narrative-based portfolio allocation
- Dashboard designs or visualization specifications
- Recommendation logic for portfolio action based on narratives
- Prediction logic for narrative lifecycle forecasting
- Data ingestion or external data source integration
- Modification of the Temporal_Taxonomy (`velocity` is NOT a new temporal property)

## Out of Scope

### Requirement 1: Canonical Narrative ID Namespace

**User Story:** As a portfolio architect, I want every canonical narrative to carry a stable, language-independent identifier, so that narrative identity is preserved across language rendering, version changes, and consumer integrations.

#### Acceptance Criteria

1. THE Narrative Framework SHALL define a `narrative.*` namespace for all canonical narrative identifiers
2. THE Narrative Framework SHALL specify the ID format as `narrative.[name]` where `[name]` is a lowercase, underscore-separated, language-neutral token (e.g., `narrative.ai_infrastructure`, `narrative.higher_for_longer`)
3. THE Narrative Framework SHALL declare that display text in any language is rendering — never identity
4. THE Narrative Framework SHALL declare that renaming a narrative's display text does NOT change its canonical ID
5. THE Narrative Framework SHALL define assignment rules for new narrative IDs: (a) unique within namespace, (b) descriptive of the belief structure, (c) language-neutral, (d) stable once assigned
6. THE Narrative Framework SHALL assign canonical IDs to all narrative hierarchy levels (meta-narratives and sub-narratives use the same namespace, e.g., `narrative.ai_transformation`, `narrative.ai_infrastructure`)
7. IF a narrative is referenced in any canonical document, THEN it SHALL carry a `narrative.*` ID from the moment of first reference

**Gap Traceability**: NAG-01, NAG-14

---

### Requirement 2: Future-Leak Prohibition

**User Story:** As a portfolio architect, I want the Narrative Framework to explicitly prohibit numeric scoring and weighting, so that the definition layer remains pure and does not seed implementation assumptions.

#### Acceptance Criteria

1. THE Narrative Framework SHALL explicitly prohibit numeric scores, weights, or probabilities assigned to narrative strength, lifecycle transitions, or membership assessment
2. THE Narrative Framework SHALL explicitly prohibit ranking logic that orders narratives by computed priority
3. THE Narrative Framework SHALL explicitly prohibit optimization logic that allocates based on narrative properties
4. THE Narrative Framework SHALL declare that qualitative descriptors (e.g., primary/secondary, strong/moderate/weak) are categorical labels — not ordinal numeric proxies
5. THE Narrative Framework SHALL explicitly reject the term "strength-weighted" and replace it with qualitative membership classification language
6. THE Narrative Framework SHALL state a unified rationale consistent with Market Organism Exclusion Constraint EC-2: weights on an incomplete model produce false confidence

**Gap Traceability**: NAG-02, NAG-11

---

### Requirement 3: Lifecycle State Machine Canonicalization

**User Story:** As a portfolio architect, I want each narrative lifecycle state to carry a canonical ID and formal transition definition, so that consumers reference states unambiguously.

#### Acceptance Criteria

1. THE Narrative Framework SHALL assign a canonical ID to each lifecycle state using the pattern `narrative.lifecycle.[state]`: `narrative.lifecycle.emerging`, `narrative.lifecycle.strengthening`, `narrative.lifecycle.dominant`, `narrative.lifecycle.weakening`, `narrative.lifecycle.dormant`, `narrative.lifecycle.dead`
2. THE Narrative Framework SHALL define each lifecycle state with: (a) canonical ID, (b) one-sentence definition, (c) qualitative transition trigger from the previous state, (d) qualitative transition trigger to the next state
3. THE Narrative Framework SHALL define valid transitions as a directed graph (which states can transition to which other states)
4. THE Narrative Framework SHALL specify that lifecycle transitions are triggered by State_Changes (not by signals, scores, or time alone)
5. THE Narrative Framework SHALL define the revival transition (`narrative.lifecycle.dormant` → `narrative.lifecycle.emerging`) as requiring a new State_Change that provides fresh evidence for the dormant belief
6. THE Narrative Framework SHALL explicitly prohibit numeric thresholds as transition triggers (e.g., "transitions to Dominant when score > 0.8" is INVALID)

**Gap Traceability**: NAG-12

---

### Requirement 4: Signal Sensor Relationship Declaration

**User Story:** As a portfolio architect, I want the Narrative Framework to explicitly declare the relationship between narratives and signals, so that no consumer confuses signals as causal agents of narrative transitions.

#### Acceptance Criteria

1. THE Narrative Framework SHALL declare that signals are sensors that detect narrative-level effects — evidence that propagation has manifested
2. THE Narrative Framework SHALL declare that signals do NOT cause narrative lifecycle transitions; only State_Changes cause transitions
3. THE Narrative Framework SHALL declare that Signal_Bubble_v0 signals are leaf-node observations in the Organism_Graph that may detect evidence of narrative membership or narrative lifecycle state — but they do not define or control those states
4. THE Narrative Framework SHALL explicitly state: "A signal may detect that a narrative is strengthening. The signal does not cause the strengthening. The underlying State_Change causes it."
5. THE Narrative Framework SHALL cross-reference the Signal Reusability invariant from Market Organism Layer 0
(See: README_market_organism_principles, Section: Architectural Compatibility)

**Gap Traceability**: NAG-06

---

### Requirement 5: Explanation Readiness Contract

**User Story:** As a portfolio architect, I want the Narrative Framework to define how narratives participate in the explanation chain, so that the Explanation Framework can traverse through Level 4 without dead ends.

#### Acceptance Criteria

1. THE Narrative Framework SHALL define that narratives serve as Level 4 in the 6-level explanation chain, answering the question: "Because of which narratives?"
(See: README_explanation_framework, Section: Explanation Levels)
2. THE Narrative Framework SHALL specify what information is provided at Level 4: narrative canonical ID, lifecycle state, birth trigger (State_Change), and membership evidence
3. THE Narrative Framework SHALL specify how Level 4 connects upward to Level 3 (State_Changes): every narrative must reference at least one originating State_Change
4. THE Narrative Framework SHALL specify how Level 4 connects downward to Level 5 (Expansion paths): narrative membership channels propagation into specific expansion paths
5. THE Narrative Framework SHALL guarantee no dead ends: every canonical narrative must be reachable from at least one State_Change and must connect to at least one System
6. THE Narrative Framework SHALL declare that explanation traversal uses only canonical IDs (`narrative.*`, `sc.*`, `system.*`) — never display text

**Gap Traceability**: NAG-07

---

### Requirement 6: Cross-Reference Convention Adoption

**User Story:** As a portfolio architect, I want the Narrative Framework to use the canonical cross-reference convention, so that all references to other deliverables are machine-navigable and auditable.

#### Acceptance Criteria

1. THE Narrative Framework SHALL use the cross-reference format `(See: [Deliverable_Name], Section: [Section_Title])` for all references to Market Organism deliverables
2. THE Narrative Framework SHALL include a Cross-References section listing all deliverables it references and the sections cited
3. THE Narrative Framework SHALL cross-reference at minimum: README_market_organism_principles, README_state_change_taxonomy, README_dependency_types_v2, README_temporal_taxonomy, README_expansion_taxonomy, README_shared_glossary_reference
4. THE Narrative Framework SHALL ensure all cross-references point to sections that exist in the target document
5. IF the Narrative Framework introduces a concept that exists in another deliverable, THEN it SHALL cross-reference rather than duplicate the definition

**Gap Traceability**: NAG-04, NAG-13

---

### Requirement 7: Exclusion Constraints Section

**User Story:** As a portfolio architect, I want the Narrative Framework to include a consolidated exclusion constraints section, so that prohibitions are reviewable in one location.

#### Acceptance Criteria

1. THE Narrative Framework SHALL include a dedicated "Exclusion Constraints" section consolidating all prohibitions
2. THE Exclusion Constraints SHALL prohibit: (a) engine implementations, (b) Python code or executable logic, (c) scoring algorithms or numeric weights, (d) probabilities or confidence values, (e) dashboard or visualization specifications, (f) asset lists as root-level entities, (g) correlation matrices, (h) recommendation or optimization logic
3. THE Exclusion Constraints SHALL state a unified rationale: weights on an incomplete model produce false confidence
4. THE Exclusion Constraints SHALL be consistent with Market Organism Exclusion Constraints (Req 8.1–8.7)
(See: README_market_organism_principles, Section: Exclusion Constraints)

**Gap Traceability**: NAG-05

---

### Requirement 8: Narrative Extension Criteria

**User Story:** As a portfolio architect, I want formal criteria for adding new narratives to the canonical registry, so that growth is controlled and consistent.

#### Acceptance Criteria

1. THE Narrative Framework SHALL define the criteria a new narrative must satisfy for canonical inclusion: (a) it represents a distinct, shared market belief structure not already covered by existing narratives, (b) it is falsifiable — contradicting evidence can invalidate it, (c) it connects at least one State_Change to at least one System through an identifiable causal explanation, (d) it is assigned a canonical `narrative.*` ID before first use
2. THE Narrative Framework SHALL define what does NOT qualify as a new canonical narrative: (a) a theme without an identifiable originating State_Change, (b) a sector classification without a causal belief, (c) a statistical pattern without a shared market interpretation
3. THE Narrative Framework SHALL require that new narratives include: scope definition, birth trigger State_Change, at least one connected System, and at least one falsification condition

**Gap Traceability**: NAG-09

---

### Requirement 9: Dependency_Type Integration

**User Story:** As a portfolio architect, I want the Narrative Framework to explicitly distinguish the Narrative dependency mechanism from Narrative-as-Container, so that consumers do not conflate these two uses of the word "Narrative."

#### Acceptance Criteria

1. THE Narrative Framework SHALL include an explicit disambiguation section distinguishing `dep.narrative` (the Dependency_Type — a propagation MECHANISM through shared belief) from Narrative-as-Container (the structural ENTITY that groups assets under a causal explanation)
2. THE Narrative Framework SHALL cross-reference the `dep.narrative` definition from Dependency_Types_v2
(See: README_dependency_types_v2, Section: Narrative)
3. THE Narrative Framework SHALL provide at least one example showing both uses simultaneously: a State_Change propagating THROUGH `dep.narrative` mechanism INTO a Narrative Container
4. THE Narrative Framework SHALL declare that `dep.narrative` is one of 10 equal Dependency_Types — it does not have special authority over other propagation mechanisms simply because it shares the word "Narrative"

**Gap Traceability**: NAG-13

---

### Requirement 10: Feedback Loop Integration

**User Story:** As a portfolio architect, I want the Narrative Framework to describe how narratives participate in feedback loops, so that the non-DAG mandate is respected and circular causation is modeled.

#### Acceptance Criteria

1. THE Narrative Framework SHALL describe how narratives can participate in Feedback_Loops within the Organism_Graph
2. THE Narrative Framework SHALL provide at least one concrete example of narrative-driven circular causation (e.g., narrative strengthens → more capital flows → asset prices confirm belief → narrative strengthens further)
3. THE Narrative Framework SHALL declare that narrative feedback is a structural norm consistent with Principle 4 (Feedback is Structural)
(See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural)
4. THE Narrative Framework SHALL specify that narrative feedback loops carry Feedback_Delay as a qualitative temporal descriptor
(See: README_temporal_taxonomy, Section: Feedback_Delay)
5. THE Narrative Framework SHALL distinguish narrative feedback (self-reinforcing belief) from narrative lifecycle progression (state transitions caused by State_Changes)

**Gap Traceability**: NAG-10

---

### Requirement 11: Architectural Compatibility

**User Story:** As a portfolio architect, I want the Narrative Framework to declare explicit architectural compatibility, so that integration with the existing Portfolio OS ecosystem is preserved.

#### Acceptance Criteria

1. THE Narrative Framework SHALL declare compatibility with the existing 12-domain model (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM) — no domains added, removed, or redefined
2. THE Narrative Framework SHALL declare compatibility with the existing canonical chain (SIGNALS → SEMANTICS → REASONING → REPORT) — sequence, direction, and responsibilities unchanged
3. THE Narrative Framework SHALL declare compatibility with the existing runtime state model (8 states, 5 integrity dimensions) — no states or dimensions added, removed, or redefined
4. THE Narrative Framework SHALL declare compatibility with Signal_Bubble_v0 (existing signals preserved as first-generation sensors, not replaced)
5. THE Narrative Framework SHALL declare compatibility with Signal Reusability (all signals as Intelligence_Objects, 6 request types preserved)
6. THE Narrative Framework SHALL declare compatibility with Signal_Lifecycle_Definition (11-field mandatory registration gate preserved)
7. THE Narrative Framework SHALL include YAML metadata header with: artifact_id, primary_domain (ARCH), artifact_type (SSOT), lifecycle_status (canonical), and all standard fields per Layer 0 pattern

**Gap Traceability**: NAG-03

---

## Acceptance Criteria Summary

All acceptance criteria are testable by document inspection. No criterion requires runtime behavior, engine execution, or code compilation. Verification is structural: required sections present, required declarations made, prohibited content absent.

## Gap Traceability

| Gap ID | Description | Requirement ID | Severity | Resolution Location | Verification Gate |
|--------|-------------|---------------|----------|---------------------|-------------------|
| NAG-01 | No `narrative.*` IDs | NFA-REQ-1 | HIGH | Narrative Framework v2 | VG-5 Rendering Independence |
| NAG-02 | "strength-weighted" language | NFA-REQ-2 | HIGH | Narrative Framework v2 | VG-4 No Future-Leak |
| NAG-03 | No YAML metadata | NFA-REQ-11 | MEDIUM | Narrative Framework v2 | VG-1 Structural Completeness |
| NAG-04 | No cross-reference convention | NFA-REQ-6 | MEDIUM | Narrative Framework v2 | VG-2 Cross-Reference Correctness |
| NAG-05 | No exclusion constraints section | NFA-REQ-7 | MEDIUM | Narrative Framework v2 | VG-1 Structural Completeness |
| NAG-06 | No Signal_Bubble_v0 declaration | NFA-REQ-4 | MEDIUM | Narrative Framework v2 | VG-8 Signal Sensor Relationship |
| NAG-07 | No explanation readiness | NFA-REQ-5 | MEDIUM | Narrative Framework v2 | VG-6 Explanation Readiness |
| NAG-08 | Narrative "velocity" property | DEFERRED | MEDIUM | Design review decision | — |
| NAG-09 | No extension criteria | NFA-REQ-8 | LOW | Narrative Framework v2 | VG-1 Structural Completeness |
| NAG-10 | No Feedback_Loop integration | NFA-REQ-10 | LOW | Narrative Framework v2 | VG-7 Layer 0 Compatibility |
| NAG-11 | "strength: strong/moderate/weak" | NFA-REQ-2 | LOW | Narrative Framework v2 | VG-4 No Future-Leak |
| NAG-12 | Lifecycle state machine lacks IDs | NFA-REQ-3 | MEDIUM | Narrative Framework v2 | VG-5 Rendering Independence |
| NAG-13 | No `dep.narrative` cross-reference | NFA-REQ-9 | LOW | Narrative Framework v2 | VG-2 Cross-Reference Correctness |
| NAG-14 | No rendering independence | NFA-REQ-1 | HIGH | Narrative Framework v2 | VG-5 Rendering Independence |

### Deferred Gaps

| Gap ID | Reason for Deferral | Resolution Timing |
|--------|--------------------|--------------------|
| NAG-08 | "velocity" is NOT a Temporal_Taxonomy property. Design review must determine whether to reject it entirely or treat it as a narrative-specific qualitative observation. This cannot be resolved at requirements level. | Design phase |

---

## Invariants

The following invariants MUST be preserved throughout all deliverables produced by this spec:

| # | Invariant | Source |
|---|-----------|--------|
| 1 | State_Change remains root/cause — no narrative promoted to causal root | Principle 1, Principle 2 |
| 2 | Narrative remains explanatory container — not cause, not sensor, not endpoint | Primitive chain definition |
| 3 | System remains affected functional domain — not conflated with narrative | Primitive chain definition |
| 4 | Asset remains observable endpoint — never root, never causal | Principle 2, Root Node Invariant |
| 5 | Signal remains sensor — detects propagation, does not cause it | Signal_Bubble_v0 preservation |
| 6 | Reasoning_Object remains conclusion primitive — not conflated with explanation | Canonical chain separation |
| 7 | Explanation_Object remains understanding primitive — multi-level, not single tooltip | Explanation Framework |
| 8 | No display text as canonical identity — `narrative.*` IDs are primary keys | Language Rendering Framework |
| 9 | No numeric narrative strength or weights — qualitative descriptors only | Rule 4: No Silent Future-Leak |
| 10 | Taxonomy-before-assets preserved — classify the change first, then identify assets | Principle 2 |
| 11 | Non-DAG feedback mandate preserved — narrative feedback loops are structural | Principle 4 |
| 12 | 12-domain model unchanged — no domains added, removed, or redefined | Req 9.1 |
| 13 | Canonical chain unchanged — SIGNALS→SEMANTICS→REASONING→REPORT | Req 9.2 |
| 14 | Runtime state model unchanged — 8 states, 5 dimensions | Req 9.5 |

---

## Verification Gate Plan

| Gate ID | Gate Name | Checks |
|---------|-----------|--------|
| VG-1 | Structural Completeness | All required sections present; YAML metadata valid; exclusion constraints section exists; extension criteria defined |
| VG-2 | Cross-Reference Correctness | All `(See: ...)` references point to existing sections in existing documents; no broken references |
| VG-3 | Primitive Responsibility Preservation | Narrative remains container (not cause, not sensor, not endpoint); State_Change remains root; Asset remains leaf |
| VG-4 | No Future-Leak Scan | Zero numeric scores, weights, probabilities, or optimization logic; "strength-weighted" absent; no numeric thresholds |
| VG-5 | Rendering Independence | All narrative identities use `narrative.*` canonical IDs; no display text as primary identity; lifecycle states carry IDs |
| VG-6 | Explanation Readiness | Level 4 explanation contract complete; connects to Level 3 (State_Changes) and Level 5 (Expansion); no dead ends |
| VG-7 | Market Organism Layer 0 Compatibility | All 6 principles satisfied; root node invariant preserved; taxonomy-before-assets preserved; non-DAG mandate respected; architectural compatibility declared |
| VG-8 | Signal Sensor Relationship | Signals explicitly declared as sensors; no signal given causal authority over narrative transitions; Signal_Bubble_v0 preserved |

---

## Non-Goals

This requirements foundation does NOT authorize implementation. Specifically:

- No design document is created by this requirements phase
- No task list is created by this requirements phase
- No existing SSOT document is modified
- No engine, registry, or runtime artifact is produced
- No narrative instances are populated
- No code is written
- This document establishes the CONTRACT for future alignment work — it does not perform the alignment

The next step (pending human review of these requirements) is to create `design.md` specifying how the Narrative Framework will be structurally modified to satisfy these requirements.
