# Implementation Plan: Market Organism Framework

## Overview

This plan produces five formal definition documents plus shared infrastructure for the Market Organism Framework. Documents are created in dependency order: Principles first (constrains all others), then State_Change_Taxonomy (root primitives), Dependency_Types_v2 (edge types), Temporal_Taxonomy (temporal properties per edge), and Expansion_Taxonomy last (uses all of the above in worked examples). A final validation task verifies cross-references, explanation readiness, and trust chain completeness across all deliverables.

All deliverables are markdown documents created in `docs/market_organism/`. No engines, no code, no scores, no probabilities.

## Tasks

- [x] 1. Create shared infrastructure and Market Organism Principles
  - [x] 1.1 Create directory structure and shared glossary reference
    - **CTO EXECUTION NOTE**: Task 1 is NOT infrastructure work. It is the semantic foundation plate for all subsequent deliverables. Do not rush. Do not "think ahead." Get this right.
    - **Key principles for this task:**
    - 1. DO NOT DUPLICATE GLOSSARY: `README_shared_glossary_reference.md` is a REFERENCE LAYER, not a DEFINITION LAYER. The SSOT (requirements.md glossary) remains authoritative. This document POINTS to it — never redefines terms.
    - 2. CROSS-REFERENCE CONVENTION IS CRITICAL: The pattern `(See: [Deliverable_Name], Section: [Section_Title])` looks small but is later essential for: Explanation Traversal, Agent Navigation, Historical Reconstruction, Registry Consumption.
    - 3. NEW TERMS GLOSSARY-FIRST: The rule "new terms added to glossary first" prevents semantic drift. Without it: "Dependency_Path" gets defined slightly differently in 3 places. Or "Explanation_Chain" acquires two meanings.
    - 4. TREAT THIS AS A SEMANTIC CONTRACT: `README_shared_glossary_reference.md` is not a documentation file. It is the semantic contract that all future deliverables, agents, registries, and explanation systems will consume.
    - **Expected output**: A document that contains: reference rules, glossary rules, cross-reference convention, canonical-term policy, SSOT pointers. NOT definitions. NOT new content. Only the rules for how all other documents reference shared truth.
    - Create `docs/market_organism/` directory
    - Create a `docs/market_organism/README_shared_glossary_reference.md` that points to the canonical glossary in requirements.md and defines the cross-reference convention: `(See: [Deliverable_Name], Section: [Section_Title])`
    - Define the glossary usage rules: no duplication, consistent term usage, new terms added to glossary first
    - _Requirements: 10.7, 10.8_

  - [x] 1.2 Create Market_Organism_Principles document
    - Create `docs/market_organism/README_market_organism_principles.md`
    - Include YAML metadata header (artifact_id, primary_domain: ARCH, artifact_type: SSOT, lifecycle_status: canonical)
    - Write Scope Statement (one paragraph defining coverage and non-coverage)
    - Write Glossary Reference section pointing to shared glossary
    - Define Principle 1: Organism over Collection — market is organism with propagation, not assets with correlations; include violation condition, compliance example, violation example
    - Define Principle 2: Taxonomy Precedes Assets — classify the change first, then identify affected assets; include violation condition
    - Define Principle 3: All Propagation is Temporal — nothing instantaneous, nothing permanent; include violation condition
    - Define Principle 4: Feedback is Structural — circular causation is the norm; include violation condition
    - Define Principle 5: Expansion Has Order — discrete hops from source; include violation condition
    - Define Principle 6: Causation over Correlation — dependencies are causal mechanisms, not statistical patterns; include violation condition
    - Write Precedence Declaration: principles override implementation decisions; future design documents must reference which principles they satisfy
    - Write Content Exclusions section: no data, assets, scores, implementation details
    - Write consolidated Exclusion Constraints section (per Req 8.1–8.7): prohibit engines, code, scores, weights, probabilities, dashboards, asset lists as root entities, correlation matrices; state rationale
    - Write Architectural Compatibility declarations (per Req 9.1–9.6): 12-domain model preserved, canonical chain preserved, future SIGNALS integration point, signal layer as sensor, runtime state model preserved, conceptual world model relationship
    - Write Cross-References section referencing all other four deliverables
    - Ensure every principle uses the format: Statement, Implication, Violation Condition, Example of Compliance, Example of Violation, Satisfies requirement reference
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 8.1–8.7, 9.1–9.6_

- [x] 2. Create State_Change_Taxonomy document
  - [x] 2.1 Create State_Change_Taxonomy with classification hierarchy and categories
    - Create `docs/market_organism/README_state_change_taxonomy.md`
    - Include YAML metadata header with stable artifact_id
    - Write Scope Statement and Glossary Reference
    - Define the mandatory classification hierarchy: State_Change type → Expansion type → Affected systems → Affected narratives → Affected assets
    - Define exactly 4 top-level categories: Macro, Corporate, Narrative, Events
    - Define Macro sub-categories (minimum: Rates, Inflation, Oil, Liquidity, FX) — each with: one-sentence scope, concrete example with Root_Node type annotation, boundary counter-example with explanation
    - Define Corporate sub-categories (minimum: Earnings, Guidance, Capex, M&A, Buybacks) — same format
    - Define Narrative sub-categories (minimum: AI, Security, Defense, Robotics, Energy) — same format
    - Define Events sub-categories (minimum: Elections, Wars, Pandemics, Sporting_Events) — same format
    - Every sub-category entry must carry a stable ID (e.g., `sc.macro.rates`, `sc.corporate.earnings`)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [x] 2.2 Add primary classification rule, extension criteria, and root node invariant
    - Write Primary Classification Rule: when a State_Change spans categories, assign by originating causal mechanism
    - Write Extension Criteria section: new sub-category requires distinct causal mechanism + scope definition + concrete example + boundary counter-example
    - Write Root Node Invariant section with: valid root nodes table (Fed Hawkish Shift, Nvidia Guidance Raise, Oil Shock, World Cup Start — each with Root_Node type), invalid root nodes table (ticker symbols, asset names — each with explanation and required reformulation), disambiguation rule, classification question ("What kind of state change occurred?" vs prohibited "How do I classify this asset?")
    - Write consolidated Exclusion Constraints section
    - Write Cross-References section (references to Expansion_Taxonomy, Dependency_Types_v2)
    - Ensure all entries support explanation readiness (traversable through explanation levels, no dead ends)
    - _Requirements: 1.8, 1.9, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 8.7, 10.8_

- [x] 3. Create Dependency_Types_v2 document
  - [x] 3.1 Create Dependency_Types_v2 with all 10 type definitions
    - Create `docs/market_organism/README_dependency_types_v2.md`
    - Include YAML metadata header with stable artifact_id
    - Write Scope Statement and Glossary Reference
    - Define exactly 10 Dependency_Types: Price, Fundamental, Narrative, Flow, Ownership, Supply_Chain, Macro, Behavioral, Regulatory, Butterfly
    - For each type, use the design format: Causal Channel (Economic/Informational/Structural), Propagation Mechanism, Directionality, Typical Temporal Profile (cross-ref to Temporal_Taxonomy), Example (source entity, target entity, mechanism), Differentiation from most similar type
    - Every type entry must carry a stable ID (e.g., `dep.price`, `dep.narrative`, `dep.butterfly`)
    - Ensure no two types share identical causal channel + directionality + propagation characteristics
    - _Requirements: 4.1, 4.2, 4.3, 4.6_

  - [x] 3.2 Add multi-type coexistence rules, dependency vs correlation, and shared sections
    - Write Multi-Type Coexistence Rules: unordered types, primary designation by dominant causal channel, combined temporal properties (shortest latency, longest duration)
    - Write Dependency vs. Correlation section: formal definitions, contrastive example showing same entity pair as correlation vs typed dependency
    - Write consolidated Exclusion Constraints section
    - Write Cross-References section (references to Temporal_Taxonomy, State_Change_Taxonomy)
    - Write Extension Criteria: new type requires unique causal channel + directionality + propagation characteristics combination, mechanism description, concrete example
    - Ensure all type definitions support explanation readiness (each type explainable as edge label in fractal drilldown)
    - _Requirements: 4.4, 4.5, 8.7, 10.8_

- [x] 4. Create Temporal_Taxonomy document
  - [x] 4.1 Create Temporal_Taxonomy with all four property definitions
    - Create `docs/market_organism/README_temporal_taxonomy.md`
    - Include YAML metadata header with stable artifact_id
    - Write Scope Statement and Glossary Reference
    - Define Latency: time delay, discrete calendar units (Day, Week, Month, Quarter, Year), interpretation guide per unit
    - Define Duration: active time span, same calendar units, interpretation guide
    - Define Amplification: qualitative 5-level scale (None, Low, Moderate, High, Extreme), interpretation guide per level
    - Define Dampening: qualitative 5-level scale (None, Low, Moderate, High, Extreme), interpretation guide per level
    - Define Feedback_Delay: qualitative temporal descriptor for back-propagation time, same calendar units as Latency
    - Write explicit Numeric Prohibition: no scores, weights, probabilities, quantitative models
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.7, 6.3_

  - [x] 4.2 Add complete temporal propagation example and shared sections
    - Write complete temporal propagation example showing all 4 properties at each Expansion_Order (1st through 4th) with increasing Latency values (e.g., Day, Month, Quarter, Year)
    - Demonstrate Amplification typically decreasing and Dampening typically increasing with distance (as tendencies, not rules)
    - Write consolidated Exclusion Constraints section
    - Write Cross-References section (references to Expansion_Taxonomy, Dependency_Types_v2)
    - Write Extension Criteria: new unit/level requires justification that existing granularity is insufficient + placement in existing scale
    - Ensure temporal properties support explanation readiness ("Effect arrives at Month 1 BECAUSE of this latency")
    - _Requirements: 5.6, 8.7, 10.8_

- [x] 5. Checkpoint - Verify first four documents
  - Ensure all four documents (Principles, State_Change_Taxonomy, Dependency_Types_v2, Temporal_Taxonomy) are complete and internally consistent before creating Expansion_Taxonomy which depends on all of them. Ask the user if questions arise.

- [x] 6. Create Expansion_Taxonomy document
  - [x] 6.1 Create Expansion_Taxonomy with order definitions and worked examples
    - Create `docs/market_organism/README_expansion_taxonomy.md`
    - Include YAML metadata header with stable artifact_id
    - Write Scope Statement and Glossary Reference
    - Define Expansion as ordered sequence of propagation hops via Dependency_Paths
    - Define 1st Order: direct effects, 1 hop from Impulse, distinguishing criterion, nature of connection
    - Define 2nd Order: secondary effects, 2 hops, distinguishing criterion, nature of connection
    - Define 3rd Order: tertiary effects, 3 hops, distinguishing criterion, nature of connection
    - Define 4th Order: quaternary effects, 4 hops, distinguishing criterion, nature of connection
    - Write at least one complete worked example showing an Impulse propagating through all 4 orders with ≥2 concrete affected systems at each order, using Dependency_Types from the Dependency_Types_v2 document and Temporal_Properties from the Temporal_Taxonomy
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 6.2 Add termination criteria, feedback detection, and shared sections
    - Write Termination Criteria: propagation stops when no further identifiable Dependency_Path connects to an additional system not already in the sequence
    - Write Feedback Detection Rule: path revisiting an existing node = Feedback_Loop, not continued expansion; reference Feedback_Loop definition from Req 6
    - Write Feedback_Loop section: define as circular Dependency_Paths forming closed cycles (≥4 nodes), mandate that Organism_Graph is NOT a DAG, provide concrete feedback loop example with real market entities and Dependency_Type labels on each edge, distinguish growth structure (acyclic forward propagation) from feedback structure (back-edges creating cycles)
    - Write consolidated Exclusion Constraints section
    - Write Cross-References section (references to State_Change_Taxonomy, Dependency_Types_v2, Temporal_Taxonomy, Market_Organism_Principles)
    - Write Extension Criteria: new order beyond 4th requires evidence of identifiable Dependency_Path at that distance + complete worked example
    - Ensure all expansion orders support explanation readiness and fractal drilldown
    - _Requirements: 3.5, 3.6, 6.1, 6.2, 6.3, 6.4, 6.5, 8.7, 10.8_

- [x] 7. Add Signal Architecture Compatibility sections
  - [x] 7.1 Add Signal Reusability and Signal Bubble v0 compatibility to all documents
    - In each of the 5 deliverables, add or extend an "Architectural Compatibility" section that declares:
    - Signal Reusability invariant: all signals as Intelligence_Objects, 6 request types, Static_Asset_Context caching, Variable_Signal refresh, Derived_Intelligence invalidation, no private recalculation
    - Signal_Bubble_v0 preservation: existing signals are first-generation sensors (not legacy), enumerate signal categories (Portfolio Core, Allocation, Risk, Performance, Deployment, Regime/PM), prohibit reimplementation, define organism relationship (signals as leaf-node observations detecting propagation)
    - Signal_Lifecycle_Definition gate: 11-field mandatory registration, three implementation statuses (Defined_Signal, Structured_Signal, Implemented_Signal), no bulk implementation
    - Ensure these are REFERENCES and DECLARATIONS only — not implementations
    - _Requirements: 11.1–11.9, 12.1–12.9, 13.1–13.10_

- [ ] 8. Final Validation and Cross-Reference Verification
  - [ ] 8.1 Validate structural completeness across all 5 deliverables
    - Verify State_Change_Taxonomy has: 4 top-level categories, all required sub-categories with scope/example/counter-example, root node invariant section, exclusion constraints
    - Verify Expansion_Taxonomy has: 4 orders defined, worked example with ≥2 systems per order, termination criteria, feedback detection rule, feedback loop example
    - Verify Dependency_Types_v2 has: 10 types defined, each with causal channel/mechanism/example, multi-type rules, dependency vs correlation section
    - Verify Temporal_Taxonomy has: 4 properties defined with correct enumerated values, complete temporal example, numeric prohibition
    - Verify Market_Organism_Principles has: ≥6 principles each with violation condition, precedence declaration, content exclusions
    - Verify all documents have: YAML metadata, scope statement, glossary reference, exclusion constraints, cross-references, stable IDs on every entry
    - _Requirements: 10.1–10.9_

  - [ ] 8.2 Validate cross-references, explanation readiness, and invariant preservation
    - Verify all cross-references use the convention `(See: [Deliverable_Name], Section: [Section_Title])` and point to existing sections
    - Verify no definition is duplicated across deliverables (shared concepts are cross-referenced only)
    - Verify no asset appears as a Root_Node anywhere
    - Verify no numeric scores, weights, or probabilities appear in any property value
    - Verify the Organism_Graph is mandated as non-DAG (feedback loops required)
    - Verify taxonomy-before-assets ordering is preserved in all classification hierarchies
    - Verify explanation readiness: every taxonomy entry is reachable through at least one explanation chain (Level 0–5), no dead ends before Root_Node
    - Verify trust chain completeness: Assessment → Reasoning → Signals → State_Change → Narrative → Expansion traversal uses only canonical IDs
    - Verify rendering independence: no natural language display text or localized strings in canonical IDs
    - Verify architectural compatibility: 12-domain model, canonical chain, runtime state model all preserved (not added to, removed from, or redefined)
    - _Requirements: 2.1, 2.2, 5.7, 6.2, 8.1–8.6, 9.1–9.6, 10.7, 10.8_

  - [ ] 8.3 Architecture Preservation Audit
    - Verify State_Change remains the root primitive (cause) — no deliverable promotes another entity to root status
    - Verify Narrative remains the explanatory container — no deliverable conflates narrative with state change, signal, or asset
    - Verify System remains the affected functional domain — no deliverable uses system as a synonym for narrative or asset
    - Verify Asset remains the observable endpoint — no deliverable promotes assets to causal or explanatory roles
    - Verify Signal remains the sensor — no deliverable gives signals causal authority (they detect, not cause)
    - Verify Reasoning_Object remains the conclusion primitive — no deliverable conflates reasoning with explanation
    - Verify Explanation_Object remains the understanding primitive — no deliverable reduces explanation to a single tooltip or text paragraph
    - Verify no future-leak violations: no scoring logic, ranking logic, confidence values, probability values, weighting values, or optimization logic introduced anywhere (even in examples)
    - Verify all canonical IDs follow the namespace convention (sc.*, narrative.*, system.*, dep.*, order.*, temporal.*, principle.*, signal.*, sem.*)
    - Verify Global Execution Rules 1-4 were respected throughout all tasks
    - INVALID: Any deliverable blurs primitive responsibilities
    - INVALID: Any example introduces numeric scoring or weighting
    - INVALID: Any canonical ID uses display text instead of stable namespace ID
    - PASS: All primitive responsibilities remain distinct and all global rules respected
    - _Requirements: 1.7, 2.1, 2.2, 7.1, 8.1–8.6, 9.6_

  - [ ] 8.4 Documentation Consumption Audit
    - Verify every major deliverable has a companion operational README (`README_<deliverable>_implementation_guide.md`)
    - Verify each operational README contains: purpose, canonical primitive, scope, exclusions, future consumers, required invariants, common failure modes, compatibility requirements, machine-readable metadata section
    - Verify the machine-readable metadata section is valid YAML with: consumes, produces, future_consumers, invariants, known_future_dependencies fields
    - Verify no operational README redefines canonical truth from the SSOT document (it explains usage, not definition)
    - Verify future consumer declarations are consistent with the Engine Roadmap (P0/P1/P2/P3 capabilities)
    - Verify invariant declarations are consistent with the Global Execution Rules
    - INVALID: Deliverable exists without operational guide
    - INVALID: README redefines canonical truth from the SSOT
    - INVALID: Machine-readable metadata missing or malformed
    - PASS: Every deliverable has SSOT + operational README with human-readable explanation and machine-readable metadata
    - _Requirements: 10.7, 10.9_

- [ ] 9. Final checkpoint - All deliverables complete
  - Ensure all 5 documents pass structural validation, cross-reference verification, explanation readiness, and invariant preservation. Ask the user if questions arise.

## Notes

- This is a DEFINITION-ONLY spec. All tasks produce markdown documents, not executable code.
- No property-based tests apply — the design explicitly states PBT is not applicable to definition documents.
- Validation is structural (required sections present, invariants respected, cross-references valid) rather than behavioral.
- The dependency order is critical: Principles → State_Change → Dependency_Types → Temporal → Expansion.
- Every taxonomy entry must carry a stable ID per the Language Rendering Framework.
- All timestamps in UTC with IANA source timezone per Temporal Rendering.
- The verification gate governance rule applies to tasks 8.1, 8.2, 8.3, and 8.4 — they must be explicitly executed with evidence, not auto-completed.

## Global Execution Rules

The following rules apply to EVERY task in this plan. They are not optional. They are not advisory. They are hard constraints on execution.

### Rule 1: SSOT Execution Rule

Every task must treat all approved framework documents as canonical SSOTs. If a task conflicts with any of the following, the task must STOP and reconcile before continuing:

- Market Organism Framework (requirements + design)
- Narrative Framework
- User Intelligence Journey Framework
- Journey Capability Matrix
- Engine Roadmap Framework
- Language Rendering Framework (including Temporal Rendering)
- Explanation Framework
- Market Data Governance Framework

No task may silently redefine architecture. No task may introduce concepts that contradict an existing SSOT. If ambiguity exists, the task must flag it rather than resolve it unilaterally.

### Rule 2: Drift Detection Rule

Before completing any task, verify:

- Primitive chain preserved (State_Change → Narrative → System → Asset)
- Root node invariant preserved (assets never root)
- Language neutrality preserved (no display text as identity)
- Timezone neutrality preserved (all timestamps UTC + IANA source)
- Explanation traversal preserved (no dead ends before Root_Node)
- Taxonomy-before-assets preserved (classification hierarchy intact)

If ANY of these are violated, the task is INCOMPLETE regardless of whether its content was written. A task that produces correct content but damages architecture is a failed task.

### Rule 3: Canonical ID Enforcement

No example, worked example, taxonomy entry, dependency type, state change, narrative, system, signal, or explanation path may be introduced without a canonical ID.

- Display text is OPTIONAL (for human readability)
- Canonical ID is MANDATORY (for machine identity)

**Correct:** `narrative.ai_infrastructure` with display text "AI Infrastructure"
**Incorrect:** "AI Infrastructure" without a canonical ID

Every entity introduced in any task must carry its stable ID from the moment of creation.

### Rule 4: No Silent Future-Leak Rule

Tasks may define future compatibility. Tasks may NOT introduce:

- Engine behavior
- Scoring logic
- Ranking logic
- Confidence logic
- Probability logic
- Recommendation logic
- Optimization logic
- Weighting logic
- Numeric strength values

Even as examples. Even as "illustrative." Even as "conceptual."

If a worked example says "Narrative Strength: High" — that is a VIOLATION (introduces scoring).
If a worked example says "Dependency Weight: 0.7" — that is a VIOLATION (introduces weighting).
If a worked example says "Expansion Confidence: 85%" — that is a VIOLATION (introduces probability).

The definition layer must remain pure. Mathematics belongs to future implementation phases only.

### Rule 5: Human + Machine README Requirement

Every major deliverable must include a companion operational README:

`docs/market_organism/README_<deliverable>_implementation_guide.md`

The guide must define:
- Purpose (why this deliverable exists)
- Canonical primitive (which primitive this document defines)
- Scope (what it covers)
- Exclusions (what it explicitly does NOT cover)
- Future consumers (which engines/systems will consume this)
- Required invariants (which architectural rules must be preserved)
- Common failure modes (examples of INVALID vs VALID usage)
- Compatibility requirements (which frameworks it must remain compatible with)
- Machine-readable metadata section (YAML block with consumes/produces/future_consumers/invariants/known_future_dependencies)

The guide is EXPLANATORY. The SSOT remains AUTHORITATIVE.
The README must NEVER redefine the SSOT — it explains how to USE the SSOT correctly.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["2.1", "2.2"] },
    { "id": 3, "tasks": ["3.1", "3.2"] },
    { "id": 4, "tasks": ["4.1", "4.2"] },
    { "id": 5, "tasks": ["6.1"] },
    { "id": 6, "tasks": ["6.2"] },
    { "id": 7, "tasks": ["7.1"] },
    { "id": 8, "tasks": ["8.1", "8.2", "8.3", "8.4"] }
  ]
}
```
