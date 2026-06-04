# Implementation Plan: Narrative Registry Framework

## Overview

This plan converts the design document into actionable tasks for producing the Narrative Registry schema-only file, artifact registry integration, governance documentation, and verification gates. No narrative instances are populated. No engines or runtime artifacts are created.

**Deliverables**:
- `docs/registries/narrative_registry.yaml` — schema-only registry with empty `narratives: []`
- `docs/registries/README_narrative_registry_governance.md` — governance procedures guide
- `.domainization/artifact_registry.yaml` — updated with registry registration entry

**Branch**: `spec/narrative-registry-framework`
**Constraints**: Schema/governance-only. No population. No engines. No code.

**This plan is safe for unattended execution only after human approval. Do not execute tasks until explicitly instructed.**

## Global Execution Rules

The following rules apply to EVERY task in this plan. They are not optional. They are hard constraints on execution.

1. This spec is schema/governance-only. The deliverable is a YAML registry file with governance metadata and an empty entries container.
2. The registry file may be created, but only as schema-only with `narratives: []`.
3. `narratives: []` MUST remain empty throughout this spec's execution.
4. No placeholder narratives may appear in `narratives: []`.
5. No sample narratives may appear in `narratives: []`.
6. No illustrative narratives may appear inside the actual registry file's `narratives` list.
7. No real `narrative.*` entries may appear in `narratives: []`.
8. YAML examples may appear only in documentation/reports, not inside the actual `narratives` list.
9. No asset-to-narrative mappings.
10. No engines, code, validation scripts, dashboards, scoring, ranking, probabilities, confidence values, optimization, or portfolio logic.
11. No Narrative Framework v2 mutation (`docs/README_narrative_framework.md` must not be modified).
12. No Market Organism Layer 0 SSOT mutation (`docs/market_organism/README_*.md` must not be modified).
13. No central glossary mutation (`.kiro/specs/market-organism-framework/requirements.md` must not be modified).
14. `.domainization/artifact_registry.yaml` may be modified ONLY to register the schema-only narrative registry artifact (Task 2).
15. If ambiguity or blocker occurs, stop and create a blocker report at `.domainization/reports/narrative_registry_framework_blocker_<description>.md`.
16. Every commit must contain BOTH the content changes AND the corresponding execution report for that wave.
17. Before final completion, verify changed files against the allowed file list (Rule 18). If any unauthorized file was modified, create a blocker report and stop.
18. Only the following files may be created or modified:
    - `.kiro/specs/narrative-registry-framework/tasks.md` (task status updates only)
    - `docs/registries/narrative_registry.yaml`
    - `docs/registries/README_narrative_registry_governance.md`
    - `.domainization/artifact_registry.yaml` (registration entry only)
    - `.domainization/reports/narrative_registry_framework_*.md`

## Tasks

- [x] 1. Registry Directory and Schema-Only File
  - [x] 1.1 Create registry directory and schema-only YAML file
    - Create directory `docs/registries/`
    - Create `docs/registries/narrative_registry.yaml` with:
      - YAML metadata header (artifact_id, primary_domain, artifact_type, lifecycle_status, created_date, last_modified, owner_role, ssot_relationship, topic, allowed_writers, allowed_readers, dependencies, version, alignment_spec)
      - Governance section (creation_authority, lifecycle_transition_authority, review_authority, initial_lifecycle_state, collision_check_required, immutable_fields, amendment_rules, prohibited_fields)
      - Empty narratives container: `narratives: []`
      - Optional: `retired_narratives: []`
    - Verify `narratives: []` is empty (zero entries)
    - Verify no placeholder/sample/illustrative/real narrative IDs appear anywhere in the file
    - _Requirements: NRF-REQ-1, NRF-REQ-2, NRF-REQ-5, NRF-REQ-6_

  - [x] 1.2 Create execution report for schema-only file
    - Create `.domainization/reports/narrative_registry_framework_task1_schema_file.md`
    - Document: file created, metadata included, governance section included, `narratives: []` is empty, no entries present, invariants preserved
    - _Requirements: Workflow governance_

  - [x] 1.3 Commit and push schema-only file + report
    - Stage BOTH `docs/registries/narrative_registry.yaml` AND `.domainization/reports/narrative_registry_framework_task1_schema_file.md`
    - Commit with message: `docs(narrative-registry): create schema-only narrative registry file`
    - Push to branch `spec/narrative-registry-framework`
    - _Requirements: Workflow governance, Global Execution Rule 16_

- [x] 2. Artifact Registry Integration
  - [x] 2.1 Register narrative registry in artifact registry
    - Add entry to `.domainization/artifact_registry.yaml` with:
      - artifact_id: narrative_registry_yaml
      - file_path: docs/registries/narrative_registry.yaml
      - primary_domain: ARCH
      - artifact_type: SSOT
      - lifecycle_status: draft
      - created_date: "2026-06-03"
      - last_modified: "2026-06-03"
      - owner_role: Portfolio Architect
      - ssot_relationship: canonical
      - topic: narrative_registry
      - allowed_writers: [ARCH, GOV]
      - allowed_readers: [ALL]
      - dependencies: [narrative_framework_md, market_organism.principles_md, state_change_taxonomy_md]
      - description: "Canonical registry of recognized narratives with governance rules. Schema-only until population spec."
      - tags: [narrative, registry, governance]
    - Do NOT modify lifecycle_state_machine.yaml
    - Do NOT add a REGISTRY artifact type
    - _Requirements: NRF-REQ-8_

  - [x] 2.2 Create execution report for artifact registration
    - Create `.domainization/reports/narrative_registry_framework_task2_artifact_registration.md`
    - Document: registration metadata added, no lifecycle_state_machine.yaml mutation, no new artifact type added, artifact_registry.yaml only modified for this single entry
    - _Requirements: Workflow governance_

  - [x] 2.3 Commit and push artifact registration + report
    - Stage BOTH `.domainization/artifact_registry.yaml` AND `.domainization/reports/narrative_registry_framework_task2_artifact_registration.md`
    - Commit with message: `docs(narrative-registry): register narrative registry in artifact registry`
    - Push to branch `spec/narrative-registry-framework`
    - _Requirements: Workflow governance, Global Execution Rule 16_

- [x] 3. Governance README
  - [x] 3.1 Create governance README
    - Create `docs/registries/README_narrative_registry_governance.md`
    - Include:
      - Purpose statement (supplementary guide — Narrative Framework v2 is the ontology SSOT)
      - How to use the registry governance rules
      - Creation procedure (propose → collision check → inclusion criteria gate → GOV review → register)
      - Collision check procedure (exact match + semantic overlap)
      - Amendment procedure (which fields are mutable, which are immutable)
      - Lifecycle transition procedure (State_Change trigger → evidence → ARCH authorization → audit record)
      - Deprecation and retirement procedure
      - No-population warning: "This file defines governance only. Population requires a separate authorized spec."
      - No scoring/ranking/probability warning
      - Cross-reference to Narrative Framework v2 as ontology SSOT
    - _Requirements: NRF-REQ-3, NRF-REQ-4, NRF-REQ-6, NRF-REQ-7_

  - [x] 3.2 Create execution report for governance README
    - Create `.domainization/reports/narrative_registry_framework_task3_governance_readme.md`
    - Document: README created, procedures documented, warnings included, no population performed
    - _Requirements: Workflow governance_

  - [x] 3.3 Commit and push governance README + report
    - Stage BOTH `docs/registries/README_narrative_registry_governance.md` AND `.domainization/reports/narrative_registry_framework_task3_governance_readme.md`
    - Commit with message: `docs(narrative-registry): create governance procedures README`
    - Push to branch `spec/narrative-registry-framework`
    - _Requirements: Workflow governance, Global Execution Rule 16_

- [ ] 4. Verification Gates VG-1 through VG-9
  - [ ] 4.1 VG-1: Structural Completeness
    - Verify `docs/registries/narrative_registry.yaml` exists
    - Verify YAML metadata header is present and valid
    - Verify governance section is present with all required fields
    - Verify `narratives: []` key exists
    - Produce pass/fail result with evidence
    - _Requirements: VG-1 gate_

  - [ ] 4.2 VG-2: No Population
    - Open actual `docs/registries/narrative_registry.yaml`
    - Verify `narratives` list is empty (length 0)
    - Fail if list contains anything
    - Fail if placeholder/sample/illustrative/real narrative appears anywhere in the file's narratives section
    - Produce pass/fail result with evidence
    - _Requirements: VG-2 gate, Global Execution Rules 3-8_

  - [ ] 4.3 VG-3: No Future-Leak
    - Verify that prohibited fields (`score`, `weight`, `probability`, `confidence`, `rank`, `asset_list`, `ticker_symbols`, `numeric_threshold`, `membership_weight`) do NOT appear as allowed registry entry fields, governance inputs, or schema extensions
    - These terms MAY appear only inside explicit Prohibited Fields / Exclusion Constraints sections where they are listed as forbidden
    - Fail if any prohibited term appears as an allowed field
    - Produce pass/fail result with evidence
    - _Requirements: VG-3 gate, NRF-REQ-9_

  - [ ] 4.4 VG-4: Namespace Correctness
    - Verify governance rules reference `narrative.*` pattern
    - Verify collision_check_required is true
    - Verify immutable_fields includes narrative_id
    - Produce pass/fail result with evidence
    - _Requirements: VG-4 gate, NRF-REQ-3_

  - [ ] 4.5 VG-5: Lifecycle Governance
    - Verify lifecycle_transition_authority is defined
    - Verify initial_lifecycle_state is `narrative.lifecycle.emerging`
    - Verify governance README documents evidence requirements
    - Produce pass/fail result with evidence
    - _Requirements: VG-5 gate, NRF-REQ-6_

  - [ ] 4.6 VG-6: Artifact Registry Compatibility
    - Verify `narrative_registry_yaml` entry exists in `.domainization/artifact_registry.yaml`
    - Verify artifact_type is SSOT
    - Verify topic is `narrative_registry`
    - Verify dependencies list includes narrative_framework_md
    - Produce pass/fail result with evidence
    - _Requirements: VG-6 gate, NRF-REQ-8_

  - [ ] 4.7 VG-7: Rendering Independence
    - Verify no display text is used as identity in governance rules
    - Verify amendment_rules declares display_name as freely_changeable
    - Verify no language-specific text appears as canonical ID
    - Produce pass/fail result with evidence
    - _Requirements: VG-7 gate, NRF-REQ-2.6_

  - [ ] 4.8 VG-8: Market Organism Compatibility
    - Verify 12-domain model is preserved (no new domains added)
    - Verify canonical chain is unchanged
    - Verify no Market Organism Layer 0 SSOT was modified
    - Verify primary_domain is ARCH (existing domain)
    - Produce pass/fail result with evidence
    - _Requirements: VG-8 gate_

  - [ ] 4.9 VG-9: Narrative Framework v2 Compatibility
    - Verify required fields match Narrative Framework v2 Section 13 Extension Criteria
    - Verify lifecycle states reference Section 6 states
    - Verify No Dead Ends is enforceable (birth_trigger + connected_systems required)
    - Verify `docs/README_narrative_framework.md` was NOT modified
    - Produce pass/fail result with evidence
    - _Requirements: VG-9 gate_

  - [ ] 4.10 Create verification gate report
    - Create `.domainization/reports/narrative_registry_framework_verification_gate_report.md`
    - Document pass/fail for each gate (VG-1 through VG-9)
    - Include evidence for each gate
    - Include overall PASS/FAIL determination
    - If any gate FAILS: stop and report to user
    - _Requirements: Verification Gate Governance_

  - [ ] 4.11 Commit and push verification gate report
    - Stage `.domainization/reports/narrative_registry_framework_verification_gate_report.md`
    - Commit with message: `docs(narrative-registry): verification gate report VG-1 through VG-9`
    - Push to branch `spec/narrative-registry-framework`
    - _Requirements: Workflow governance, Global Execution Rule 16_

- [ ] 5. Final Completion
  - [ ] 5.1 Verify all tasks complete and no unauthorized files modified
    - Verify every task (1 through 4) is marked `[x]` in tasks.md
    - Verify `docs/registries/narrative_registry.yaml` exists and `narratives: []` is empty
    - Verify `docs/registries/README_narrative_registry_governance.md` exists
    - Verify `narrative_registry_yaml` entry exists in `.domainization/artifact_registry.yaml`
    - Verify all execution reports exist: task1, task2, task3, verification gate
    - Verify no unauthorized files were modified (check changed files against allowed list, Global Execution Rule 18)
    - If any unauthorized file was modified, create a blocker report and stop
    - _Requirements: Global Execution Rules 17, 18_

  - [ ] 5.2 Create final completion report
    - Create `.domainization/reports/narrative_registry_framework_completion_report_2026-06-03.md`
    - Document: all tasks completed, all verification gates passed, all reports present, registry file is schema-only, `narratives: []` confirmed empty, artifact registered, governance README created, no unauthorized files modified, no population performed, branch ready for review/merge
    - _Requirements: Workflow governance_

  - [ ] 5.3 Final commit and push
    - Stage `.domainization/reports/narrative_registry_framework_completion_report_2026-06-03.md` and updated `tasks.md`
    - Commit with message: `docs(narrative-registry): final completion report and task status update`
    - Push to branch `spec/narrative-registry-framework`
    - _Requirements: Workflow governance, Global Execution Rule 16_

## Notes

- This is a SCHEMA/GOVERNANCE-ONLY implementation. No narrative instances are created.
- `narratives: []` MUST remain empty throughout execution.
- All YAML examples in documentation/reports are illustrative only — never copied into the actual registry file.
- Verification Gate Task (Task 4) is an EXPLICIT gate — it must be independently executed, not auto-completed.
- `.domainization/artifact_registry.yaml` may only be modified to add the single registration entry (Task 2).
- No lifecycle_state_machine.yaml modification is authorized.
- No REGISTRY artifact type is created.
- Commit+push subtasks use branch `spec/narrative-registry-framework`.
- Execution reports go to `.domainization/reports/` with descriptive names per file naming conventions.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["1.3"] },
    { "id": 3, "tasks": ["2.1"] },
    { "id": 4, "tasks": ["2.2"] },
    { "id": 5, "tasks": ["2.3"] },
    { "id": 6, "tasks": ["3.1"] },
    { "id": 7, "tasks": ["3.2"] },
    { "id": 8, "tasks": ["3.3"] },
    { "id": 9, "tasks": ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9"] },
    { "id": 10, "tasks": ["4.10"] },
    { "id": 11, "tasks": ["4.11"] },
    { "id": 12, "tasks": ["5.1"] },
    { "id": 13, "tasks": ["5.2"] },
    { "id": 14, "tasks": ["5.3"] }
  ]
}
```
