# Implementation Plan: Narrative Framework Alignment

## Overview

This plan converts the design document into actionable tasks for producing the aligned `docs/README_narrative_framework.md` (in-place replacement). The document is structured as 17 top-level sections plus YAML metadata, organized into 4 logical task groups: Foundation & Ontology (sections 1–5), Formalization (sections 6–9), Integration Contracts (sections 10–14), and Constraints & Compatibility (sections 15–17). Each group concludes with a commit+push and execution report. A final verification gate validates all 8 VG gates.

**Deliverable**: Single file `docs/README_narrative_framework.md` — complete in-place replacement
**Branch**: `spec/narrative-framework-alignment`
**Constraints**: Definition-only. No engines, code, scores, probabilities, or runtime behavior.

## Global Execution Rules

The following rules apply to EVERY task in this plan. They are not optional. They are hard constraints on execution.

1. This spec is definition-only. The deliverable is a markdown document.
2. Only the following files may be created or modified:
   - `docs/README_narrative_framework.md`
   - `docs/README_narrative_framework_alignment_implementation_guide.md`
   - `.domainization/reports/narrative_framework_alignment_*.md`
   - `.kiro/specs/narrative-framework-alignment/tasks.md` (task status updates only)
3. Do NOT modify the central Market Organism glossary (`.kiro/specs/market-organism-framework/requirements.md`).
4. Do NOT modify Market Organism Layer 0 SSOTs (`docs/market_organism/README_*.md`).
5. Do NOT add engines, code, runtime behavior, dashboards, registry population, scoring, ranking, probabilities, optimization, or portfolio recommendation logic.
6. Preserve the primitive chain: `State_Change → Narrative → System → Asset`.
7. Narrative remains explanatory container, never causal root.
8. Signal remains sensor, never cause.
9. All examples are illustrative only and do NOT create canonical registry entries, asset registry entries, or system registry entries.
10. All canonical narrative identities must use `narrative.*` namespace.
11. `strength-weighted` must NOT appear in `docs/README_narrative_framework.md`.
12. `velocity` must remain narrative-specific qualitative observation only and must NOT become a lifecycle trigger, ranking input, score proxy, or Temporal_Taxonomy extension.
13. Every commit must contain BOTH the content changes AND the corresponding execution report for that wave.
14. If a blocker or ambiguity occurs, stop execution, create a blocker report at `.domainization/reports/narrative_framework_alignment_blocker_<description>.md`, and do not continue silently.
15. Do NOT ask the user during execution unless a blocker occurs. If no ambiguity exists, continue autonomously.
16. Before final completion, verify changed files against the allowed file list (Rule 2). If any unauthorized file was modified, stop and create a blocker report.
17. Before final completion, mark all completed tasks with `[x]`. Do not mark failed or skipped tasks as complete.

## Tasks

- [x] 1. Foundation and Ontology (Sections 1–5)
  - [x] 1.1 Write YAML metadata header and Section 1: Scope Statement
    - Create `docs/README_narrative_framework.md` with the YAML metadata header containing all required fields: `artifact_id: narrative_framework_md`, `primary_domain: ARCH`, `artifact_type: SSOT`, `lifecycle_status: canonical`, `created_date`, `last_modified`, `owner_role`, `ssot_relationship: canonical`, `topic: narrative_ontology`, `allowed_writers: [ARCH, GOV]`, `allowed_readers: [ALL]`, `dependencies` (list all 6 Layer 0 deliverables), `version: v2`, `alignment_spec: narrative-framework-alignment`
    - Write Section 1 (Scope Statement): Declare the document defines the Narrative ontology as a formal primitive; declare definition-layer only; forward pointer to Exclusion Constraints section for consolidated prohibitions; explicit exclusion of data, engines, scores, implementation, and runtime behavior
    - Follow the pattern from `README_market_organism_principles.md`
    - _Requirements: NFA-REQ-11.7, NFA-REQ-7 (partial), NFA-REQ-2 (partial)_

  - [x] 1.2 Write Section 2: Glossary Reference + Amendments
    - Write canonical glossary reference pointing to `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary
    - Include cross-reference: `(See: README_shared_glossary_reference, Section: Glossary Usage Rules)`
    - Write Glossary Amendments table with three terms: Narrative_Container (structural role as explanatory grouping), Narrative_Membership (relationship between Asset and Narrative, classified by type and qualitative strength), Narrative_Interaction (causal relationship between State_Change and Narrative, classified by interaction type)
    - Include governance note: amendments are LOCAL to this document; central glossary sync not authorized by this spec
    - Explicitly distinguish Narrative_Container from `dep.narrative`
    - _Requirements: NFA-REQ-6.1, NFA-REQ-6.5, NFA-REQ-9 (partial)_

  - [x] 1.3 Write Section 3: The Primitive Chain
    - State the canonical primitive chain: `State_Change → Narrative → System → Asset`
    - Declare each primitive's responsibility: State_Change = root cause, Narrative = explanatory container, System = affected functional domain, Asset = observable endpoint
    - Declare the taxonomy-before-assets principle
    - Include cross-reference to Market Organism principles
    - _Requirements: NFA-REQ-11 (partial), NFA-REQ-5 (partial)_

  - [x] 1.4 Write Section 4: What Is a Narrative? (Definition + Formal Properties)
    - Write the formal definition of a Narrative as an explanatory container
    - Declare canonical ID format: `narrative.[descriptive_token]` with all 4 token rules (lowercase, underscore-separated, language-neutral, stable once assigned)
    - Declare assignment rules: unique within namespace, descriptive of belief structure, language-neutral, stable once assigned
    - Write Rendering Independence Declaration: display text in any language is rendering — never identity; renaming display text does NOT change canonical ID
    - Include illustrative examples (e.g., `narrative.ai_infrastructure`, `narrative.higher_for_longer`) — mark explicitly as "illustrative only, not canonical registry entries, not asset registry population, not system registry population"
    - Cross-reference: `(See: README_language_rendering_framework, Section: Rule 4 — Display Text is Never Identity)`
    - Declare qualitative descriptors (primary/secondary, strong/moderate/weak) are categorical labels — not ordinal numeric proxies
    - _Requirements: NFA-REQ-1 (all acceptance criteria), NFA-REQ-2.4_

  - [x] 1.5 Write Section 5: Narrative vs. State_Change
    - Write the distinction: Narrative is the explanatory CONTAINER (what the belief is); State_Change is the CAUSE (what triggered the belief)
    - Declare State_Change remains causal root; Narrative is never promoted to causal root
    - Declare that narratives do not cause State_Changes; State_Changes cause narratives
    - Include at least one illustrative example showing the distinction
    - _Requirements: NFA-REQ-4 (partial — establishes causality direction)_

  - [x] 1.6 Create execution report for Foundation and Ontology
    - Create `.domainization/reports/narrative_framework_alignment_task1_foundation_ontology.md`
    - Document: which sections were written (1–5 + YAML metadata), which requirements are satisfied (NFA-REQ-1, NFA-REQ-2.4, NFA-REQ-6.1, NFA-REQ-6.5, NFA-REQ-7 partial, NFA-REQ-9 partial, NFA-REQ-11.7), confirmation that invariants 1–10 are preserved, any decisions made during writing
    - _Requirements: Workflow governance_

  - [x] 1.7 Commit and push Foundation and Ontology sections + report
    - Stage BOTH `docs/README_narrative_framework.md` AND `.domainization/reports/narrative_framework_alignment_task1_foundation_ontology.md`
    - Commit with message: `docs(narrative-framework): write foundation and ontology sections 1-5`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance, Global Execution Rule 13_

- [x] 2. Formalization (Sections 6–9)
  - [x] 2.1 Write Section 6: Narrative Lifecycle State Machine (Formalized)
    - Write the 6 lifecycle states with canonical IDs: `narrative.lifecycle.emerging`, `narrative.lifecycle.strengthening`, `narrative.lifecycle.dominant`, `narrative.lifecycle.weakening`, `narrative.lifecycle.dormant`, `narrative.lifecycle.dead`
    - For each state include: canonical ID, one-sentence definition, qualitative transition trigger from previous state, qualitative transition trigger to next state
    - Write the transition graph (Mermaid stateDiagram-v2) showing all 7 valid transitions (T1–T7)
    - Write the Transition Definitions table with columns: Transition, From, To, Trigger, Prohibition (all "No numeric threshold")
    - Write Key Constraints: all transitions triggered by State_Changes only; no numeric thresholds; signals may DETECT transitions but do not CAUSE them
    - Write Velocity subsection: qualitative observation property (Accelerating/Steady/Decelerating); explicitly declare it is NOT a Temporal_Taxonomy extension; declare it MUST NOT be used as lifecycle transition trigger, ranking input, score proxy, or Temporal_Taxonomy extension
    - Cross-reference: `(See: README_temporal_taxonomy, Section: Temporal Property Enumeration)`
    - _Requirements: NFA-REQ-3 (all acceptance criteria), NFA-REQ-2.6_

  - [x] 2.2 Write Section 7: Narrative Hierarchy (Containment Rules)
    - Define meta-narratives and sub-narratives using the same `narrative.*` namespace
    - Declare that hierarchy is expressed through naming convention, not through nested IDs (flat namespace)
    - Define containment rules: a sub-narrative is contained within a parent meta-narrative; parent-child relationships are declared, not computed
    - Include illustrative example: `narrative.ai_transformation` (meta) contains `narrative.ai_infrastructure` (sub) — mark as "illustrative only, not canonical registry entries"
    - Declare all hierarchy levels carry canonical IDs per the same namespace rules
    - _Requirements: NFA-REQ-1.6, NFA-REQ-8 (partial — hierarchy informs extension criteria)_

  - [x] 2.3 Write Section 8: Multi-Narrative Membership
    - Write the 5 revised Multi-Narrative Rules (primary narrative, secondary narratives, time-dependent, qualitatively classified, dominant narrative determines primary propagation path)
    - Explicitly replace "strength-weighted" with "qualitatively classified" in Rule 4
    - Write the Membership Record structure: asset_id, narrative_id (canonical `narrative.*` ID), membership_type (primary/secondary/emerging/legacy), influence (strong/moderate/weak as categorical labels), since, evidence
    - Include explicit prohibition: "Converting categorical labels to numbers (strong=3, moderate=2, weak=1) is explicitly prohibited"
    - Note field rename: `strength` → `influence` to eliminate scoring-adjacent language
    - Mark ALL examples as "illustrative only, not canonical registry entries, not asset registry population"
    - _Requirements: NFA-REQ-2.4, NFA-REQ-2.5, NFA-REQ-1 (IDs used throughout)_

  - [x] 2.4 Write Section 9: State_Change-to-Narrative Interactions
    - Define the 5 interaction types: Creates, Strengthens, Weakens, Kills, Revives
    - Write the Narrative Interaction model structure: state_change_id (`sc.*`), narrative_id (`narrative.*`), interaction_type, evidence
    - Declare that all interactions are caused by State_Changes — consistent with lifecycle transition triggers
    - Cross-reference: `(See: README_state_change_taxonomy, Section: Classification Hierarchy)`
    - Mark ALL examples as "illustrative only, not canonical registry entries"
    - _Requirements: NFA-REQ-3.4, NFA-REQ-6 (cross-reference)_

  - [x] 2.5 Create execution report for Formalization
    - Create `.domainization/reports/narrative_framework_alignment_task2_formalization.md`
    - Document: which sections were written (6–9), which requirements are now satisfied (NFA-REQ-3 complete, NFA-REQ-2.4–2.6 complete), confirmation that velocity is treated correctly (NOT Temporal_Taxonomy extension), confirmation "strength-weighted" is fully eliminated, invariants preserved
    - _Requirements: Workflow governance_

  - [x] 2.6 Commit and push Formalization sections + report
    - Stage BOTH `docs/README_narrative_framework.md` AND `.domainization/reports/narrative_framework_alignment_task2_formalization.md`
    - Commit with message: `docs(narrative-framework): write formalization sections 6-9`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance, Global Execution Rule 13_

- [x] 3. Checkpoint — Verify foundation and formalization integrity
  - [x] 3.1 Verify sections 1–9 structural presence and correctness
    - Verify all 9 sections (Scope, Glossary, Primitive Chain, Definition, Narrative vs State_Change, Lifecycle, Hierarchy, Membership, Interactions) are present in `docs/README_narrative_framework.md`
    - Verify no numeric scores, weights, or probabilities appear in any section
    - Verify `strength-weighted` does NOT appear anywhere in the document
    - Verify `velocity` guardrails are present (NOT Temporal_Taxonomy extension, NOT lifecycle trigger/ranking/score proxy)
    - Verify all canonical IDs follow `narrative.*` or `narrative.lifecycle.*` pattern
    - Verify all cross-references use `(See: [Deliverable_Name], Section: [Section_Title])` format
    - Verify all examples are marked as "illustrative only"
    - If any check fails: stop execution and create blocker report
    - _Requirements: Mid-point integrity verification_

  - [x] 3.2 Create checkpoint report
    - Create `.domainization/reports/narrative_framework_alignment_checkpoint_sections_1_9.md`
    - Document: pass/fail for each verification item, evidence of compliance, any issues found
    - _Requirements: Workflow governance_

  - [x] 3.3 Commit and push checkpoint report
    - Stage `.domainization/reports/narrative_framework_alignment_checkpoint_sections_1_9.md`
    - Commit with message: `docs(narrative-framework): checkpoint verification sections 1-9`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance, Global Execution Rule 13_

- [x] 4. Integration Contracts (Sections 10–14)
  - [x] 4.1 Write Section 10: Dependency_Type Integration (dep.narrative distinction)
    - Write the Dual-Use Distinction Table: `dep.narrative` (propagation MECHANISM, one of 10 equal Dependency_Types) vs. `narrative.*` (explanatory STRUCTURE, the container)
    - Write the worked example showing both uses simultaneously: a State_Change propagating THROUGH `dep.narrative` INTO a Narrative Container (use the Nvidia/AI Infrastructure example from design)
    - Write Authority Declaration: `dep.narrative` is one of 10 equal Dependency_Types; no special authority over other mechanisms
    - Cross-reference: `(See: README_dependency_types_v2, Section: Narrative)`
    - Mark worked example as "illustrative only, not canonical registry entries, not asset registry population, not system registry population"
    - _Requirements: NFA-REQ-9 (all acceptance criteria)_

  - [x] 4.2 Write Section 11: Feedback Loop Integration
    - Declare narrative feedback is a structural norm consistent with Principle 4
    - Write concrete example of narrative-driven circular causation (self-reinforcing AI infrastructure belief loop from design)
    - Declare Feedback_Delay as qualitative temporal descriptor for narrative feedback loops
    - Write distinction between narrative feedback (self-reinforcing belief, circular, structural) and narrative lifecycle progression (linear state transitions caused by State_Changes)
    - Cross-references: `(See: README_temporal_taxonomy, Section: Feedback_Delay)` and `(See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural)`
    - _Requirements: NFA-REQ-10 (all acceptance criteria)_

  - [x] 4.3 Write Section 12: Explanation Readiness Contract (Level 4)
    - Write the Level 4 Contract table: Level=4, Question="Because of which narratives?", Position between Level 3 (State_Changes) and Level 5 (Expansion paths), Information provided (narrative canonical ID, lifecycle state, birth trigger State_Change, membership evidence), Traversal ID type (`narrative.*` canonical IDs only)
    - Write Upward Connection (Level 4 → Level 3): every narrative MUST reference at least one originating State_Change
    - Write Downward Connection (Level 4 → Level 5): every narrative MUST connect to at least one System
    - Write No Dead Ends Guarantee: every canonical narrative must be reachable FROM at least one State_Change AND connected TO at least one System
    - Declare explanation traversal uses only canonical IDs — never display text
    - Cross-reference: `(See: README_explanation_framework, Section: Explanation Levels)`
    - _Requirements: NFA-REQ-5 (all acceptance criteria)_

  - [x] 4.4 Write Section 13: Narrative Extension Criteria
    - Write Inclusion Criteria table (4 criteria): distinct shared belief, falsifiable, connects State_Change to System, assigned canonical ID before first use
    - Write Exclusion Criteria table (3 non-qualifying concepts): theme without State_Change, sector classification without causal belief, statistical pattern without shared interpretation
    - Write Required Fields for new narrative registration: canonical ID, scope definition, birth trigger State_Change, at least one connected System, at least one falsification condition, initial lifecycle state (always `narrative.lifecycle.emerging`)
    - _Requirements: NFA-REQ-8 (all acceptance criteria)_

  - [x] 4.5 Write Section 14: Signal Sensor Relationship Declaration
    - Write the 4 explicit declarations: (1) signals are sensors detecting narrative-level effects, (2) signals do NOT cause lifecycle transitions — only State_Changes do, (3) Signal_Bubble_v0 signals are leaf-node observations that may detect evidence but do not define/control states, (4) verbatim statement: "A signal may detect that a narrative is strengthening. The signal does not cause the strengthening. The underlying State_Change causes it."
    - Cross-references: `(See: README_market_organism_principles, Section: Architectural Compatibility)` and `(See: README_market_organism_principles, Section: Signal Layer as Sensor (Req 9.4))`
    - _Requirements: NFA-REQ-4 (all acceptance criteria)_

  - [x] 4.6 Create execution report for Integration Contracts
    - Create `.domainization/reports/narrative_framework_alignment_task4_integration_contracts.md`
    - Document: which sections were written (10–14), which requirements are now fully satisfied (NFA-REQ-4, NFA-REQ-5, NFA-REQ-8, NFA-REQ-9, NFA-REQ-10), confirmation that dep.narrative distinction is clear, explanation chain has no dead ends, signal causality is correctly attributed, invariants preserved
    - _Requirements: Workflow governance_

  - [x] 4.7 Commit and push Integration Contracts sections + report
    - Stage BOTH `docs/README_narrative_framework.md` AND `.domainization/reports/narrative_framework_alignment_task4_integration_contracts.md`
    - Commit with message: `docs(narrative-framework): write integration contracts sections 10-14`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance, Global Execution Rule 13_

- [x] 5. Constraints and Compatibility (Sections 15–17)
  - [x] 5.1 Write Section 15: Exclusion Constraints
    - Write the 8 exclusion constraints in table format: EC-1 (engine implementations), EC-2 (scoring algorithms/numeric weights/probabilities), EC-3 (dashboard specifications), EC-4 (asset lists as root entities), EC-5 (correlation matrices), EC-6 (recommendation/optimization logic), EC-7 (numeric lifecycle thresholds), EC-8 (numeric membership weights)
    - Write unified rationale: "Weights on an incomplete model produce false confidence. The Narrative Framework defines WHAT a narrative IS ontologically. Numeric precision belongs to future implementation phases."
    - Declare consistency with Market Organism Exclusion Constraints (Req 8.1–8.7)
    - Cross-reference: `(See: README_market_organism_principles, Section: Exclusion Constraints)`
    - _Requirements: NFA-REQ-7 (all acceptance criteria), NFA-REQ-2 (consolidation)_

  - [x] 5.2 Write Section 16: Architectural Compatibility
    - Write 6 compatibility declarations each with one-line statement + cross-reference:
      - 12-Domain Model Preservation (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM — no domains added/removed/redefined)
      - Canonical Chain Preservation (SIGNALS→SEMANTICS→REASONING→REPORT unchanged)
      - Runtime State Model Preservation (8 states, 5 integrity dimensions unchanged)
      - Signal_Bubble_v0 Preservation (existing signals preserved as first-generation sensors)
      - Signal Reusability Preservation (all signals as Intelligence_Objects, 6 request types preserved)
      - Signal_Lifecycle_Definition Preservation (11-field mandatory registration gate preserved)
    - _Requirements: NFA-REQ-11.1–11.6_

  - [x] 5.3 Write Section 17: Cross-References
    - Write the complete cross-reference table listing ALL deliverables referenced and sections cited
    - Minimum 10 cross-references per design Component 14 table: README_market_organism_principles (4 sections), README_state_change_taxonomy, README_dependency_types_v2, README_temporal_taxonomy, README_expansion_taxonomy, README_shared_glossary_reference, README_explanation_framework, README_language_rendering_framework
    - Verify every `(See: ...)` reference used throughout the document appears in this table
    - _Requirements: NFA-REQ-6 (all acceptance criteria)_

  - [x] 5.4 Write Satisfies traceability table (document footer)
    - Append a `--- Satisfies ---` section at the end of the document
    - Write a traceability table mapping each NFA-REQ to the section(s) that satisfy it
    - Ensure all 11 requirements (NFA-REQ-1 through NFA-REQ-11) are covered
    - _Requirements: NFA-REQ-6 (traceability)_

  - [x] 5.5 Create execution report for Constraints and Compatibility
    - Create `.domainization/reports/narrative_framework_alignment_task5_constraints_compatibility.md`
    - Document: which sections were written (15–17 + traceability table), which requirements are now fully satisfied (NFA-REQ-2 complete, NFA-REQ-6 complete, NFA-REQ-7 complete, NFA-REQ-11 complete), full requirements coverage confirmation (all 11 NFA-REQs addressed), invariants 11–14 preserved
    - _Requirements: Workflow governance_

  - [x] 5.6 Commit and push Constraints and Compatibility sections + report
    - Stage BOTH `docs/README_narrative_framework.md` AND `.domainization/reports/narrative_framework_alignment_task5_constraints_compatibility.md`
    - Commit with message: `docs(narrative-framework): write constraints and compatibility sections 15-17 plus traceability`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance, Global Execution Rule 13_

- [x] 6. Verification Gate — Full VG-1 through VG-8 validation
  - [x] 6.1 VG-1: Structural Completeness verification
    - Verify all 17 sections present in `docs/README_narrative_framework.md`
    - Verify YAML metadata header is valid and contains all required fields
    - Verify Exclusion Constraints section exists with 8 prohibitions
    - Verify Extension Criteria section is defined with inclusion/exclusion rules
    - Produce pass/fail result with evidence
    - _Requirements: VG-1 gate_

  - [x] 6.2 VG-2: Cross-Reference Correctness verification
    - Verify every `(See: [Deliverable_Name], Section: [Section_Title])` reference in the document points to a section that exists in the target document
    - Check all deliverables referenced in Section 17 exist in the repository
    - Identify any broken or dangling cross-references
    - Produce pass/fail result with list of all references checked
    - _Requirements: VG-2 gate_

  - [x] 6.3 VG-3: Primitive Responsibility Preservation verification
    - Verify Narrative remains explanatory container (not cause, not sensor, not endpoint)
    - Verify State_Change remains causal root (never demoted)
    - Verify Asset remains observable endpoint (never root, never causal)
    - Verify Signal remains sensor (detects, does not cause)
    - Scan document for any language that violates these responsibilities
    - Produce pass/fail result with evidence
    - _Requirements: VG-3 gate, Invariants 1–5_

  - [x] 6.4 VG-4: No Future-Leak Scan
    - Text search `docs/README_narrative_framework.md` for prohibited terms: numeric scores, weights, probabilities, optimization, ranking, "strength-weighted", numeric thresholds, confidence values
    - Verify "strength-weighted" has ZERO matches in `docs/README_narrative_framework.md` (historical references in reports/tasks/design explaining the rejection are allowed — only the final deliverable must be clean)
    - Verify no numeric threshold language in lifecycle transition triggers
    - Verify categorical labels are not described as ordinal proxies
    - Produce pass/fail result with search evidence (zero matches required in final document)
    - _Requirements: VG-4 gate, Invariant 9_

  - [x] 6.5 VG-5: Rendering Independence verification
    - Verify all narrative identities use `narrative.*` canonical IDs as primary identity
    - Verify no display text is used as canonical identity anywhere
    - Verify lifecycle states all carry `narrative.lifecycle.*` IDs
    - Verify Rendering Independence Declaration is present and correct
    - Produce pass/fail result with evidence
    - _Requirements: VG-5 gate, Invariant 8_

  - [x] 6.6 VG-6: Explanation Readiness verification
    - Verify Level 4 explanation contract is complete (question, position, information provided, traversal ID type)
    - Verify upward connection to Level 3 (State_Changes) is specified
    - Verify downward connection to Level 5 (Expansion paths) is specified
    - Verify No Dead Ends Guarantee is stated
    - Produce pass/fail result with evidence
    - _Requirements: VG-6 gate_

  - [x] 6.7 VG-7: Market Organism Layer 0 Compatibility verification
    - Verify all 6 principles are satisfied (check Architectural Compatibility section)
    - Verify root node invariant preserved (State_Change = root)
    - Verify taxonomy-before-assets preserved
    - Verify non-DAG mandate respected (feedback loops structural)
    - Verify architectural compatibility declarations are present for all 6 items
    - Produce pass/fail result with evidence
    - _Requirements: VG-7 gate, Invariants 11–14_

  - [x] 6.8 VG-8: Signal Sensor Relationship verification
    - Verify signals explicitly declared as sensors (not causes)
    - Verify no signal is given causal authority over narrative transitions
    - Verify Signal_Bubble_v0 preservation is declared
    - Verify the 4 explicit declarations from Section 14 are present
    - Produce pass/fail result with evidence
    - _Requirements: VG-8 gate, Invariant 5_

  - [x] 6.9 Create verification gate report
    - Create `.domainization/reports/narrative_framework_alignment_verification_gate_report.md`
    - Document pass/fail status for each gate (VG-1 through VG-8)
    - Include evidence for each gate check
    - Include overall PASS/FAIL determination
    - If any gate FAILS: stop and report to user with specific failure details
    - _Requirements: Verification Gate Governance_

  - [x] 6.10 Commit and push verification gate results
    - Stage verification gate report
    - Commit with message: `docs(narrative-framework): verification gate report VG-1 through VG-8`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance_

- [x] 7. Final Documentation and Completion
  - [x] 7.1 Create implementation guide README
    - Create `docs/README_narrative_framework_alignment_implementation_guide.md`
    - Document: how to USE the aligned Narrative Framework document (not redefine canonical truth)
    - Include: purpose of the document, how to navigate the 17 sections, how to register a new narrative (referencing Extension Criteria), how to read lifecycle state machine, how to use cross-references for traversal, how to verify compliance with Exclusion Constraints
    - Declare this guide is supplementary — the Narrative Framework v2 is the SSOT
    - _Requirements: User-requested README documentation_

  - [x] 7.2 Final commit and push
    - Stage all remaining files (implementation guide README, any outstanding reports)
    - Commit with message: `docs(narrative-framework): implementation guide and final artifacts`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance_

- [x] 8. Final Checkpoint — Confirm completion
  - [x] 8.1 Verify all tasks complete and no unauthorized files modified
    - Verify every task (1 through 7) is marked `[x]` in tasks.md
    - Verify `docs/README_narrative_framework.md` exists and is the complete 17-section document
    - Verify `docs/README_narrative_framework_alignment_implementation_guide.md` exists
    - Verify all execution reports exist: task1, task2, checkpoint, task4, task5, verification gate
    - Verify no unauthorized files were modified by checking changed files against allowed list (Global Execution Rule 2). If any file outside the allowed list was modified, create a blocker report and stop.
    - If any task was skipped, document the reason in the completion report
    - _Requirements: Global Execution Rules 2, 16, 17_

  - [x] 8.2 Create final completion report
    - Create `.domainization/reports/narrative_framework_alignment_completion_report_2026-06-02.md`
    - Document: all tasks completed, all verification gates passed, all execution reports present, implementation guide created, no unauthorized files modified, no canonical SSOT mutated, branch ready for review/merge
    - _Requirements: Workflow governance_

  - [x] 8.3 Final commit and push completion report
    - Stage `.domainization/reports/narrative_framework_alignment_completion_report_2026-06-02.md` and updated `tasks.md` (with all `[x]` marks)
    - Commit with message: `docs(narrative-framework): final completion report and task status update`
    - Push to branch `spec/narrative-framework-alignment`
    - _Requirements: Workflow governance_

## Notes

- This is a DEFINITION-ONLY implementation. The deliverable is a single markdown file replacing `docs/README_narrative_framework.md`.
- No engines, code, scores, probabilities, or runtime behavior are produced.
- All examples in the document are illustrative only — not canonical registry entries.
- "strength-weighted" is REJECTED throughout; replaced with "qualitatively classified."
- Velocity is narrative-specific qualitative observation ONLY — NOT a Temporal_Taxonomy extension.
- Velocity MUST NOT be used as lifecycle transition trigger, ranking input, score proxy, or Temporal_Taxonomy extension.
- Glossary amendments (Narrative_Container, Narrative_Membership, Narrative_Interaction) are LOCAL to this document; central glossary sync not authorized.
- Cross-references use format: `(See: [Deliverable_Name], Section: [Section_Title])`
- Commit+push subtasks use branch `spec/narrative-framework-alignment`.
- Execution reports go to `.domainization/reports/` with descriptive names per file naming conventions.
- Verification gate task (Task 6) is an EXPLICIT gate — it must be independently executed, not auto-completed or auto-inferred from subtask completion.
- Each task references specific NFA-REQ requirements for traceability.
- Market Organism Layer 0 constrains all work — primitive chain and invariants must be preserved.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["1.4", "1.5"] },
    { "id": 3, "tasks": ["1.6"] },
    { "id": 4, "tasks": ["1.7"] },
    { "id": 5, "tasks": ["2.1"] },
    { "id": 6, "tasks": ["2.2", "2.3"] },
    { "id": 7, "tasks": ["2.4"] },
    { "id": 8, "tasks": ["2.5"] },
    { "id": 9, "tasks": ["2.6"] },
    { "id": 10, "tasks": ["3.1"] },
    { "id": 11, "tasks": ["3.2"] },
    { "id": 12, "tasks": ["3.3"] },
    { "id": 13, "tasks": ["4.1", "4.2"] },
    { "id": 14, "tasks": ["4.3", "4.4", "4.5"] },
    { "id": 15, "tasks": ["4.6"] },
    { "id": 16, "tasks": ["4.7"] },
    { "id": 17, "tasks": ["5.1"] },
    { "id": 18, "tasks": ["5.2", "5.3"] },
    { "id": 19, "tasks": ["5.4"] },
    { "id": 20, "tasks": ["5.5"] },
    { "id": 21, "tasks": ["5.6"] },
    { "id": 22, "tasks": ["6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8"] },
    { "id": 23, "tasks": ["6.9"] },
    { "id": 24, "tasks": ["6.10"] },
    { "id": 25, "tasks": ["7.1"] },
    { "id": 26, "tasks": ["7.2"] },
    { "id": 27, "tasks": ["8.1"] },
    { "id": 28, "tasks": ["8.2"] },
    { "id": 29, "tasks": ["8.3"] }
  ]
}
```
