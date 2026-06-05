# Implementation Plan: Narrative Population Framework

## Overview

This plan defines the task structure for the first controlled population of the Narrative Registry. It covers candidate field preparation, evidence justification, human falsification approval, pre-mutation verification, registry append, and post-mutation verification.

**Approved Wave 1 Candidates:**
- AI Infrastructure → proposed ID: `narrative.ai_infrastructure`
- Defense Rearmament → proposed ID: `narrative.defense_rearmament`
- GLP-1 / Obesity Medicine → proposed ID: `narrative.glp1_obesity_medicine`

**This plan is safe for unattended execution only until the falsification approval blocker. Registry mutation requires explicit human approval. Do not execute tasks until explicitly instructed.**

## Global Execution Rules

The following rules apply to EVERY task in this plan:

1. Only the 3 approved Wave 1 candidates may be prepared: AI Infrastructure, Defense Rearmament, GLP-1 / Obesity Medicine.
2. No excluded candidate may receive a registry entry, candidate template, evidence justification, or mutation step. Excluded candidates may be referenced only in exclusion lists, guardrails, verification checks, and blocker reports.
3. Candidate IDs remain PROPOSED until actual registry mutation: `narrative.ai_infrastructure`, `narrative.defense_rearmament`, `narrative.glp1_obesity_medicine`.
4. Registry mutation is BLOCKED until final human approval of candidate-specific falsification conditions.
5. `tasks.md` creation does not authorize execution.
6. No asset-to-narrative mappings.
7. No `fact.*`, `signal.*`, or `evidence.*` objects may be created. Evidence is summarized/referenced only.
8. No engines, code, validation scripts, dashboards, scoring, ranking, probabilities, confidence values, optimization, or portfolio logic.
9. No Narrative Framework v2 mutation.
10. No Narrative Registry schema/governance mutation.
11. No Market Evidence Framework mutation.
12. No Market Organism Layer 0 mutation.
13. No central glossary mutation.
14. If ambiguity or blocker occurs, stop and create a blocker report at `.domainization/reports/narrative_population_framework_blocker_<description>.md`.
15. Every commit must contain BOTH content changes AND the corresponding execution report.

## Allowed Files

The following files may be created or modified during task execution:

- `.kiro/specs/narrative-population-framework/tasks.md` (task status updates only)
- `.domainization/reports/narrative_population_framework_*.md`
- `docs/registries/narrative_registry.yaml` — ONLY in Wave 5, ONLY after explicit human approval of all 3 falsification conditions

## Tasks

- [ ] 0. Pre-Execution Safety Verification
  - [x] 0.1 Verify branch state and registry preconditions
    - Confirm branch is `spec/narrative-population-framework` and up to date with main
    - Confirm `docs/registries/narrative_registry.yaml` exists
    - Confirm `narratives: []` is empty (zero entries)
    - Confirm `retired_narratives: []` is empty
    - Confirm `docs/README_market_evidence_framework.md` exists on main
    - Confirm `.domainization/reports/narrative_population_framework_human_decision_capture_2026-06-04.md` exists
    - Confirm Wave 1 approved set is exactly 3 candidates (AI Infrastructure, Defense Rearmament, GLP-1)
    - Confirm no excluded candidates have been prepared
    - _Requirements: Global Execution Rules 1-5_

  - [x] 0.2 Create pre-execution safety report
    - Create `.domainization/reports/narrative_population_framework_task0_pre_execution_safety.md`
    - Document all verification results
    - Confirm registry state: `narratives: []` empty, `retired_narratives: []` empty
    - Confirm human decision capture report exists and is valid
    - _Requirements: Global Execution Rule 15 / workflow governance_

  - [x] 0.3 Commit and push pre-execution safety report
    - Stage `.domainization/reports/narrative_population_framework_task0_pre_execution_safety.md` and updated `tasks.md`
    - Commit: `docs(narrative-population): pre-execution safety verification wave 0`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 1. Candidate Field Preparation
  - [x] 1.1 Prepare field template: AI Infrastructure
    - Prepare all candidate fields for `narrative.ai_infrastructure` (PROPOSED ID):
      - candidate_label, proposed_narrative_id, display_name
      - scope_definition draft
      - birth_trigger draft (sc.* reference)
      - connected_systems draft (system.* references, minimum 1)
      - falsification_condition draft — MUST be concrete and testable — PENDING HUMAN APPROVAL
      - lifecycle_state: `narrative.lifecycle.emerging`
      - lifecycle_history_note: "Registered as initial canonical state despite existing market maturity; lifecycle history predates registry."
      - registered_date_policy, registered_by policy, last_modified_policy
      - evidence_summary draft
      - contradiction_review draft
      - credit_solvency_relevance: "Not applicable — macro-thematic narrative"
      - valuation_trap_guard_status: CLEAR
      - human_approval_status: PENDING (falsification only)
    - Document in execution report only — do NOT write to registry
    - _Requirements: NPF-REQ-5, NPF-REQ-6, Design Section: Data Models_

  - [x] 1.2 Prepare field template: Defense Rearmament
    - Prepare all candidate fields for `narrative.defense_rearmament` (PROPOSED ID):
      - All same fields as 1.1 for Defense Rearmament
      - birth_trigger draft: sc.narrative.defense or sc.events.wars based on specific triggering event
      - connected_systems: system.defense_industrial, system.government_procurement minimum
      - falsification_condition draft — PENDING HUMAN APPROVAL
      - credit_solvency_relevance: "Not applicable — geopolitical macro-thematic narrative"
      - valuation_trap_guard_status: CLEAR
    - Document in execution report only — do NOT write to registry
    - _Requirements: NPF-REQ-5, NPF-REQ-6_

  - [x] 1.3 Prepare field template: GLP-1 / Obesity Medicine
    - Prepare all candidate fields for `narrative.glp1_obesity_medicine` (PROPOSED ID):
      - All same fields as 1.1 for GLP-1
      - birth_trigger draft: sc.corporate.earnings or sc.corporate.guidance based on specific FDA/clinical breakthrough
      - connected_systems: system.pharmaceutical_manufacturing, system.healthcare_delivery minimum
      - falsification_condition draft — PENDING HUMAN APPROVAL
      - credit_solvency_relevance: "Not applicable — scientific breakthrough narrative, not valuation-driven"
      - valuation_trap_guard_status: CLEAR
    - Document in execution report only — do NOT write to registry
    - _Requirements: NPF-REQ-5, NPF-REQ-6_

  - [x] 1.4 Create candidate field preparation report
    - Create `.domainization/reports/narrative_population_framework_task1_candidate_field_preparation.md`
    - Document all 3 candidate field templates
    - Mark all falsification conditions as DRAFT / PENDING HUMAN APPROVAL
    - Confirm no registry mutation occurred
    - _Requirements: NPF-REQ-5, workflow governance_

  - [x] 1.5 Commit and push candidate field preparation + report
    - Stage report and updated `tasks.md`
    - Commit: `docs(narrative-population): candidate field preparation wave 1`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 2. Evidence Justification Preparation
  - [x] 2.1 Prepare evidence justification: AI Infrastructure
    - Write evidence justification summary for `narrative.ai_infrastructure`:
      - observed_facts_summary: hyperscaler capex announcements, LLM launch events, data center construction surge
      - calculated_signals_summary: capex acceleration signal (where applicable), sector demand signals
      - evidence_container_reference: "evidence.narrative.ai_infrastructure (CANDIDATE reference — not an evidence object)"
      - provenance_readiness: primary sources (corporate disclosures, earnings calls)
      - contradiction_review: any contradicting signals (capex slowdown signals, etc.)
      - evidence_limitations: evidence covers broad theme; individual company credit risk is not narrative evidence
      - credit_solvency_relevance: not applicable (macro-thematic)
      - valuation_trap_guard_status: CLEAR — not justified by asset prices alone
    - Write to report ONLY — no Market Evidence objects created
    - _Requirements: NPF-REQ-3, NPF-REQ-11, Design Section: Evidence Justification Format_

  - [x] 2.2 Prepare evidence justification: Defense Rearmament
    - Write evidence justification summary for `narrative.defense_rearmament`:
      - observed_facts_summary: NATO spending commitments, Ukraine conflict, national defense budget increases
      - birth trigger identification from sc.narrative.defense or sc.events.wars taxonomy
      - provenance_readiness: government budget disclosures, official NATO commitments
      - contradiction_review: any signals of de-escalation or defense budget cuts
      - credit_solvency_relevance: not applicable (geopolitical macro-thematic)
      - valuation_trap_guard_status: CLEAR
    - Write to report ONLY — no Market Evidence objects created
    - _Requirements: NPF-REQ-3, NPF-REQ-11_

  - [x] 2.3 Prepare evidence justification: GLP-1 / Obesity Medicine
    - Write evidence justification summary for `narrative.glp1_obesity_medicine`:
      - observed_facts_summary: FDA approvals (Ozempic/Wegovy/Mounjaro), clinical trial results, prescription volume data
      - birth trigger: specific FDA approval event or Phase 3 trial results
      - provenance_readiness: FDA filings, company earnings, clinical study publications
      - contradiction_review: safety concerns, insurance coverage limitations, supply constraints
      - credit_solvency_relevance: not applicable (scientific breakthrough narrative)
      - valuation_trap_guard_status: CLEAR
    - Write to report ONLY — no Market Evidence objects created
    - _Requirements: NPF-REQ-3, NPF-REQ-11_

  - [x] 2.4 Create evidence justification report
    - Create `.domainization/reports/narrative_population_framework_task2_evidence_justification.md`
    - Document all 3 evidence summaries
    - Confirm no `fact.*`, `signal.*`, or `evidence.*` objects were created
    - Confirm no evidence registry files were created
    - _Requirements: NPF-REQ-3, NPF-REQ-11_

  - [x] 2.5 Commit and push evidence justification + report
    - Stage report and updated `tasks.md`
    - Commit: `docs(narrative-population): evidence justification preparation wave 2`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 3. Human Falsification Approval Gate
  - [x] 3.1 Present falsification condition drafts for human review
    - Create `.domainization/reports/narrative_population_framework_falsification_drafts_for_review.md`
    - Present each candidate's falsification condition draft:
      - AI Infrastructure: DRAFT condition — PENDING HUMAN APPROVAL
      - Defense Rearmament: DRAFT condition — PENDING HUMAN APPROVAL
      - GLP-1 / Obesity Medicine: DRAFT condition — PENDING HUMAN APPROVAL
    - Mark each: `human_approval_status: PENDING`
    - _Requirements: NPF-REQ-6, NPF-REQ-8_

  - [x] 3.2 Verify human falsification approval before proceeding
    - CHECK: Has human explicitly approved all 3 falsification conditions?
    - If YES for all 3: update `human_approval_status: APPROVED` per candidate, proceed to Wave 4
    - If ANY are not approved: create blocker report and STOP:
      `.domainization/reports/narrative_population_framework_falsification_approval_blocker.md`
    - Registry mutation MUST NOT proceed without all 3 conditions approved
    - _Requirements: NPF-REQ-6, NPF-REQ-8, Design Section: Human Decisions Captured_

  - [x] 3.3 Commit and push approval gate artifacts
    - Stage all reports and updated `tasks.md`
    - Commit: `docs(narrative-population): falsification approval gate wave 3`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 4. Pre-Mutation Verification Gates
  - [x] 4.1 Execute VG-POP-1 through VG-POP-4
    - VG-POP-1: Confirm `narratives: []` is empty — no design/task-prep mutation occurred
    - VG-POP-2: Confirm all narrative references use candidate/proposed prefix — no premature canonical IDs
    - VG-POP-3: Confirm each of the 3 candidates satisfies all 4 inclusion criteria with documented evidence
    - VG-POP-4: Confirm Market Evidence justification is cited per candidate with provenance and contradiction review
    - Record pass/fail per gate with evidence
    - _Requirements: NPF-REQ-8, Design Section: Correctness Properties_

  - [x] 4.2 Execute VG-POP-5 through VG-POP-9
    - VG-POP-5: Confirm no candidate was derived from asset lists, portfolio baskets, or co-movement patterns
    - VG-POP-6: Confirm zero numeric scores, weights, probabilities, confidence values anywhere
    - VG-POP-7: Confirm each candidate has an identified `sc.*` birth trigger
    - VG-POP-8: Confirm each candidate has at least one `system.*` in connected_systems
    - VG-POP-9: Confirm each candidate has a concrete, human-APPROVED falsification condition
    - Record pass/fail per gate with evidence
    - _Requirements: NPF-REQ-8_

  - [x] 4.3 Execute VG-POP-10 through VG-POP-13
    - VG-POP-10: Confirm documented human approval for scope, ID, falsification per candidate
    - VG-POP-11: Confirm each entry complies with `narrative_registry.yaml` schema (all required fields, no prohibited fields)
    - VG-POP-12: Confirm no semantic overlap between the 3 entries without declared parent-child
    - VG-POP-13: Confirm valuation-sensitive candidates have "not applicable" credit/solvency waiver with justification
    - Record pass/fail per gate with evidence
    - _Requirements: NPF-REQ-8_

  - [x] 4.4 Create pre-mutation verification report
    - Create `.domainization/reports/narrative_population_framework_pre_mutation_verification_report.md`
    - Document pass/fail for VG-POP-1 through VG-POP-13
    - Include evidence for each gate
    - If any gate FAILS: stop and report to user — do NOT proceed to Wave 5
    - _Requirements: NPF-REQ-8, Design Section: Correctness Properties_

  - [x] 4.5 Commit and push verification report
    - Stage report and updated `tasks.md`
    - Commit: `docs(narrative-population): pre-mutation verification gates wave 4`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 5. Registry Append Operation
  - [x] 5.1 Verify pre-conditions before registry mutation
    - Confirm all VG-POP-1 through VG-POP-13 PASSED
    - Confirm human approved all 3 falsification conditions (no PENDING status remaining)
    - Confirm `narratives: []` is still empty
    - If any precondition fails: STOP. Create blocker report. Do NOT mutate registry.
    - _Requirements: NPF-REQ-7, NPF-REQ-8_

  - [x] 5.2 Append 3 approved narrative entries to registry
    - Load `docs/registries/narrative_registry.yaml`
    - Append entry 1: `narrative.ai_infrastructure` with all required fields and human-approved falsification
    - Append entry 2: `narrative.defense_rearmament` with all required fields and human-approved falsification
    - Append entry 3: `narrative.glp1_obesity_medicine` with all required fields and human-approved falsification
    - Each entry must include: all 9 required fields, lifecycle_state: `narrative.lifecycle.emerging`, lifecycle_history_note
    - No prohibited fields, no asset fields, no scoring/ranking/probability/confidence values
    - _Requirements: NPF-REQ-7, Design Section: Registry Mutation Design_

  - [x] 5.3 Create registry append execution report
    - Create `.domainization/reports/narrative_population_framework_task5_registry_append.md`
    - Document: 3 entries appended, field values per entry, gates passed, human approvals documented
    - Confirm `narratives` list now contains exactly 3 entries
    - Confirm `retired_narratives: []` still empty
    - _Requirements: NPF-REQ-7, workflow governance_

  - [x] 5.4 Commit and push registry append + report
    - Stage `docs/registries/narrative_registry.yaml` AND execution report AND `tasks.md`
    - Commit: `docs(narrative-population): Wave 1 registry append — 3 approved narratives`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 6. Post-Mutation Verification
  - [x] 6.1 Execute post-mutation verification checks
    - Confirm registry contains exactly 3 narratives after append
    - Confirm IDs match: `narrative.ai_infrastructure`, `narrative.defense_rearmament`, `narrative.glp1_obesity_medicine`
    - Confirm no excluded candidates appear in `narratives`
    - Confirm `retired_narratives: []` remains empty
    - Confirm no schema/governance mutation occurred
    - Confirm no asset mappings created
    - Confirm no Market Evidence mutation
    - Confirm no Narrative Framework v2 mutation
    - Confirm no Market Organism Layer 0 mutation
    - Confirm no central glossary mutation
    - Execute VG-POP-14: diff against main confirms only `narratives: []` changed
    - _Requirements: NPF-REQ-7, NPF-REQ-8_

  - [x] 6.2 Create post-mutation verification report
    - Create `.domainization/reports/narrative_population_framework_post_mutation_verification_report.md`
    - Document all post-mutation checks with evidence
    - Confirm overall PASS/FAIL
    - If any check FAILS: stop and report to user
    - _Requirements: NPF-REQ-8, workflow governance_

  - [x] 6.3 Commit and push post-mutation verification report
    - Stage report and updated `tasks.md`
    - Commit: `docs(narrative-population): post-mutation verification wave 6`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

- [ ] 7. Final Completion
  - [~] 7.1 Verify all tasks complete and no unauthorized files modified
    - Verify tasks 0 through 6 are all marked `[x]`
    - Verify `docs/registries/narrative_registry.yaml` contains exactly 3 narratives
    - Verify all execution reports exist (task0, task1, task2, task5, pre-mutation VG, post-mutation VG)
    - Verify no unauthorized files were modified
    - Verify no excluded candidates appear anywhere in registry
    - _Requirements: Global Execution Rules 14, 15_

  - [~] 7.2 Create final completion report
    - Create `.domainization/reports/narrative_population_framework_completion_report_2026-06-04.md`
    - Document: all tasks complete, all VGs passed, registry contains 3 narratives, all human approvals documented, no unauthorized mutations, branch ready for review/merge
    - _Requirements: workflow governance_

  - [~] 7.3 Final commit and push
    - Stage completion report and updated `tasks.md`
    - Commit: `docs(narrative-population): final completion report and task status update`
    - Push to `spec/narrative-population-framework`
    - _Requirements: Global Execution Rule 15_

## Notes

- This is the first controlled Narrative Registry population.
- `narratives: []` MUST remain empty until Wave 5 Task 5.2 is explicitly authorized.
- All candidate IDs are PROPOSED until registry mutation occurs.
- Registry mutation is hard-blocked by human falsification approval gate (Wave 3).
- Excluded candidates MUST NOT appear in any template, evidence justification, or mutation step. They may be referenced only in exclusion lists, guardrails, verification checks, and blocker reports.
- No Market Evidence objects, engines, or code are created by this spec.
- Commit+push subtasks use branch `spec/narrative-population-framework`.
- Execution reports go to `.domainization/reports/` with descriptive names.

## Execution Stop Boundaries

| Boundary | Condition | Action if Not Met |
|----------|-----------|-------------------|
| Before Wave 3 completes | Waves 0–2 prepare documentation only — no mutation risk | Execute freely |
| Wave 3 (Task 3.2) | Human must approve all 3 falsification conditions | STOP — create blocker report, do NOT proceed to Wave 4 |
| Before Wave 5 (Task 5.1) | All VG-POP-1 through VG-POP-13 must PASS AND human falsification approval documented | STOP — do NOT mutate registry |
| Wave 5 (Task 5.2) | Registry append authorized ONLY if ALL preconditions confirmed | STOP — create blocker report if any precondition fails |

**Hard rule**: If human falsification approval is absent at Wave 3, execution MUST stop. It MUST NOT auto-proceed to Waves 4-7. A blocker report must be created and the human must explicitly resume execution after providing approval.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["0.1"] },
    { "id": 1, "tasks": ["0.2", "0.3"] },
    { "id": 2, "tasks": ["1.1", "1.2", "1.3"] },
    { "id": 3, "tasks": ["1.4", "1.5"] },
    { "id": 4, "tasks": ["2.1", "2.2", "2.3"] },
    { "id": 5, "tasks": ["2.4", "2.5"] },
    { "id": 6, "tasks": ["3.1"] },
    { "id": 7, "tasks": ["3.2", "3.3"],
      "human_gate": "HARD BLOCK — Human must approve all 3 falsification conditions. Task 3.2 stops if approval missing." },
    { "id": 8, "tasks": ["4.1", "4.2", "4.3"] },
    { "id": 9, "tasks": ["4.4", "4.5"] },
    { "id": 10, "tasks": ["5.1"],
      "precondition": "All VG-POP-1 through VG-POP-13 MUST PASS. Human falsification approval MUST be confirmed." },
    { "id": 11, "tasks": ["5.2", "5.3", "5.4"],
      "mutation_gate": "Registry mutation authorized ONLY by explicit human approval of all 3 falsification conditions" },
    { "id": 12, "tasks": ["6.1", "6.2", "6.3"] },
    { "id": 13, "tasks": ["7.1", "7.2", "7.3"] }
  ]
}
```
