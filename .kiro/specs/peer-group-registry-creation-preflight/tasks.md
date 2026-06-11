# Implementation Plan: Peer Group Registry Creation Preflight

## Overview

This plan covers all documentation-only preflight tasks required to prepare candidate registry records for future human/CTO review. All tasks produce Markdown documentation artifacts only.

**Requirements source**: requirements.md v2 (hardened)
**Design source**: design.md (hardened)
**Status**: PEER_GROUP_REGISTRY_CREATION_PREFLIGHT_TASKS_HARDENED_READY_FOR_HUMAN_REVIEW

## Commit and Review Protocol

1. Execute exactly one task per implementation cycle unless explicitly instructed otherwise.
2. After completing a task, update only the task's declared output artifact and the tasks.md checkbox.
3. Commit after each completed task.
4. Do not combine multiple tasks in one commit unless explicitly instructed.
5. Do not start the next task automatically.
6. Open or prepare a PR after each task commit if project workflow requires PR-based review.
7. Wait for human instruction before starting the next task.
8. Task 12 (VG-PGRC-PREFLIGHT-1) must be executed as a leaf task and must have its own commit/PR.
9. Task 14 (Final Completion Review) must have its own commit/PR and must not run until Tasks 1–13 are complete.

## Commit Message Format

Use: `docs(peer-group-registry-creation-preflight): Task N: <description>`

Examples:
- `docs(peer-group-registry-creation-preflight): Task 1: Add preflight source alignment artifact`
- `docs(peer-group-registry-creation-preflight): Task 10: Add candidate record draft artifacts`
- `docs(peer-group-registry-creation-preflight): Task 12: Add VG-PGRC-PREFLIGHT-1 verification gate`
- `docs(peer-group-registry-creation-preflight): Task 14: Add final preflight completion review`

## PR Body Requirements

Each task PR body must include:
- Task executed (number and title)
- Files changed
- Artifact/report created
- Dependencies satisfied
- Acceptance criteria summary
- Boundary confirmations
- Explicit no-registry / no-final-peer-assignment / no-peer_group_id / no-SAI-mutation / no-runtime / no-validation-code / no-market-data / no-trading confirmations
- CI status
- Recommended next step
- Confirmation that the next task was not started

## Hard Boundaries — No Task May Produce

- Production peer_group_registry.yaml or any production registry file
- Final peer group assignments
- Canonical peer_group_id values
- SAI artifact mutations
- Runtime code, services, APIs, or database schemas
- Validation code or executable implementations
- Market data integrations or vendor connections
- Broker, exchange, ATS, or trading venue connections
- Order routing or execution logic
- Compliance claims or regulated-entity status assertions
- Tactical Momentum Execution Gate Framework work
- Production registry creation

## Candidate Artifact Rules

When tasks produce artifacts, they must:
- Use `candidate_` prefix or `_preflight` suffix in filenames
- Carry `production_authority: NONE`
- Carry `preliminary: true`
- Use only permitted Candidate_Status values (CANDIDATE_DRAFT, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY, CANDIDATE_READY_FOR_REVIEW)
- Use `peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL`
- Remain non-production documentation artifacts

## Tasks

- [x] 1. Create Preflight Source Alignment Artifact
  - **Purpose**: Confirm that PGMF is complete, VG-PGMF-1 is PASS, and all authoritative input artifacts exist and are accessible.
  - **Report type**: Source Alignment Report
  - **Depends on**: requirements.md, design.md, tasks.md
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/source_alignment_preflight.md`
  - **Required content**:
    - PGMF 12/12 tasks complete confirmation
    - VG-PGMF-1 PASS confirmation with artifact path reference
    - Scope preflight exists and accessible (`.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md`)
    - PGMF source registry exists (`.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`)
    - Evidence matrix exists (`.domainization/reports/peer_group_methodology_evidence_matrix_2026-06-08.md`)
    - Field taxonomy reference exists (`.kiro/specs/peer-group-registry-methodology-framework/artifacts/field_taxonomy_reference_2026-06-08.md`)
    - SAI deferred interfaces reference exists (`.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md`)
    - SAI compatibility verification exists (`.kiro/specs/peer-group-registry-methodology-framework/artifacts/sai_compatibility_verification_2026-06-08.md`)
    - No missing authority source — all source foundation artifacts confirmed present
    - Source authority model summary from design.md
    - Explicit statement: this artifact confirms source alignment only; it does not create candidate records or registry content
  - **Acceptance criteria**:
    - All 8 authority source artifacts confirmed present with correct file paths
    - VG-PGMF-1 PASS explicitly confirmed
    - No missing source that would block downstream tasks
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Documentation only. No candidate records created. No registry files.
  - **Final status marker**: `SOURCE_ALIGNMENT_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R1 (PGMF Dependency)_

- [x] 2. Create Family Universe Intake Specification
  - **Purpose**: Document the 9 confirmed family universes PGF-01 through PGF-09 from the scope preflight without inventing new tickers, families, subclusters, or benchmark instruments.
  - **Report type**: Family Universe Intake Report
  - **Depends on**: Task 1
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/family_universe_intake_preflight.md`
  - **Required content**:
    - PGF-01 through PGF-09 intake records following design.md Family Universe Intake structure
    - Each family: family_id, family_name, source_section_reference, core_universe_count, adjacent_universe_count, core_candidate_tickers_from_source, adjacent_candidate_tickers_from_source, benchmark_context_candidates_from_source, subcluster_definitions_from_source, unresolved_decisions_from_source, boundary_notes_from_source, source_trace
    - PGF-09 as rule-based ETF/Fund family (no core ticker list, ETF/fund comparison dimensions, methodology rules, benchmark/context separation)
    - PGF-08 explicitly records adjacent_universe_count = 0 as NONE_IN_SOURCE
    - Explicit no-new-family / no-new-ticker / no-new-subcluster / no-new-benchmark-instrument rule
    - Source traceability to `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5
    - Statement: this artifact documents intake structure only; it does not create candidate records
  - **Acceptance criteria**:
    - All 9 families documented with correct counts matching scope preflight
    - Every ticker, subcluster, benchmark instrument traces to scope preflight
    - No invented content
    - PGF-09 correctly represented as rule-based
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: No new tickers/families/subclusters invented. No candidate records created.
  - **Final status marker**: `FAMILY_UNIVERSE_INTAKE_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R2 (Family Universe Intake)_

- [ ] 3. Create Candidate Record Draft Schema Specification
  - **Purpose**: Define the non-production candidate record schema and lifecycle model that future tasks will use.
  - **Report type**: Candidate Schema Report
  - **Depends on**: Task 1
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_record_schema_preflight.md`
  - **Required content**:
    - Complete candidate record field table from design.md Component 2
    - candidate_record_id as non-production (candidate_record_id_status = PREFLIGHT_NON_PRODUCTION)
    - production_authority = NONE
    - preliminary = true
    - Candidate_Status allowed values: CANDIDATE_DRAFT, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY, CANDIDATE_READY_FOR_REVIEW
    - peer_group_id = PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
    - peer_group_id_status = NOT_CREATED
    - source_authority_status / source_authority_references fields
    - methodology_decision_references fields
    - SAI contract fields (SAI_contract_status = PREFLIGHT_NOT_CANONICAL)
    - market_data_fields_status = NOT_POPULATED_IN_PREFLIGHT
    - trading_governance_fields_status = FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
    - human_review_status / CTO_approval_status fields
    - Explicit prohibition: no ACTIVE, APPROVED, or production lifecycle status
    - Statement: this artifact defines the schema only; it does not instantiate records
  - **Acceptance criteria**:
    - All fields from design.md Component 2 documented with types and defaults
    - No production states or canonical IDs present
    - Schema is structurally compatible with PGMF field taxonomy and SAI output contract
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Schema definition only. No records instantiated.
  - **Final status marker**: `CANDIDATE_RECORD_SCHEMA_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R3 (Candidate-Only Record Status), R5 (Field Taxonomy Mapping)_

- [ ] 4. Create Source Authority Mapping Specification
  - **Purpose**: Define how every candidate record methodology-decision field maps to the PGMF source registry.
  - **Report type**: Source Authority Mapping Report
  - **Depends on**: Task 1
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/source_authority_mapping_preflight.md`
  - **Required content**:
    - Field-level source authority requirement: every CURRENT_METHODOLOGY field requires at least one source reference
    - Source reference structure: source_id (e.g., SRC-B-01), authority_domain (e.g., classification_authority), tier_level (Tier 1/2/3)
    - Methodology-decision field mapping table: which PGMF-DEC governs which fields
    - DOMAIN_SCOPE_VIOLATION rule: source may not be cited outside its designated authority domain
    - SOURCE_EVIDENCE_MISSING rule: if a field cannot trace to any PGMF source → CANDIDATE_BLOCKED
    - Tier hierarchy enforcement: Tier 1 produces hard rules within its domain only; Tier 2/3 support but do not override
    - Extension rule: no external source without human/CTO approval recorded with approver identity and approval date
    - Statement: this artifact defines mapping rules only; it does not populate source references on records
  - **Acceptance criteria**:
    - All CURRENT_METHODOLOGY fields from PGMF field taxonomy have source authority domain assignments
    - Domain-scope and evidence-missing blocking rules are clear and testable
    - Extension rule matches requirements.md R4 and R15
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Rule definition only. No candidate records populated.
  - **Final status marker**: `SOURCE_AUTHORITY_MAPPING_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R4 (Source Authority Mapping)_

- [ ] 5. Create Field Taxonomy Mapping Specification
  - **Purpose**: Define how future candidate records map to the PGMF field taxonomy by scope label.
  - **Report type**: Field Taxonomy Mapping Report
  - **Depends on**: Task 1
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/field_taxonomy_mapping_preflight.md`
  - **Required content**:
    - CURRENT_METHODOLOGY handling: populate from source authority with PGMF source registry reference
    - CURRENT_MODEL_NULLABLE handling: field exists, value remains null
    - DEFERRED handling: field carries mandated deferred value (e.g., threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED)
    - FUTURE_SCOPE handling: NOT_POPULATED_IN_PREFLIGHT
    - FUTURE_VENDOR_INTEGRATION handling: NOT_POPULATED_IN_PREFLIGHT
    - FUTURE_COMPLIANCE_REFERENCE handling: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
    - Required field completeness rules: REQUIRED fields must be populated or record is CANDIDATE_BLOCKED
    - Asset_type applicability rules: field requirements vary by object_type per PGMF-DEC-04
    - peer_group_id placeholder rule: always PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
    - No canonical ID values permitted
    - Statement: this artifact defines taxonomy mapping rules only; it does not apply them to records
  - **Acceptance criteria**:
    - All 6 scope labels have clear handling rules
    - Asset-type-aware field applicability documented
    - Blocking conditions for missing REQUIRED fields are explicit
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Rule definition only. No records mapped.
  - **Final status marker**: `FIELD_TAXONOMY_MAPPING_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R5 (Field Taxonomy Mapping)_

- [ ] 6. Create Boundary Rules Specification
  - **Purpose**: Define all boundary protections that apply to candidate preflight records.
  - **Report type**: Boundary Rules Report
  - **Depends on**: Tasks 3 and 5
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md`
  - **Required content**:
    - ETF/Fund boundary: ETFs/funds never company peers; PGF-09 uses etf_peer; ETFs in company families are benchmark_context only; no ETF-to-company fallback; no company-to-ETF fallback
    - Cross-region comparability: 7 required fields; comparability_adjustment_required = true for GAAP/IFRS differences; listing_variant_type for multi-venue assets
    - Unsupported asset protection: all unsupported classes listed; Candidate_Status = CANDIDATE_BLOCKED or CANDIDATE_DEFERRED; unsupported_status field populated
    - Private company handling: peer_role restricted to private_comparable_context; valuation_peer_allowed = false
    - Derivative handling: excluded_non_peer only
    - Index/basket handling: benchmark_context only
    - Market data boundary: market data availability never affects peer_role or Candidate_Status
    - Trading boundary: all 13 trading governance fields carry FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
    - SAI boundary: SAI not mutated; candidate records do not satisfy SAI deferred interface
    - No ETF-to-company fallback rule with BLOCK_ETF_COMPANY_FALLBACK
    - No market-data-as-methodology-proxy rule with BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY
    - No trading-eligibility-inference rule with BLOCK_TRADING_ELIGIBILITY_INFERENCE
    - Statement: this artifact defines boundary rules only; it does not enforce them on records
  - **Acceptance criteria**:
    - All boundaries from design.md documented with block states
    - Cross-reference to PGMF decisions (DEC-05, DEC-07, DEC-08)
    - Market data and trading boundaries are absolute
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Rule definition only. No boundary enforcement executed.
  - **Final status marker**: `BOUNDARY_RULES_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R6, R7, R8, R9, R10 (ETF/Fund, Cross-Region, Unsupported, Market Data, Trading)_

- [ ] 7. Create Candidate Lifecycle and Block State Specification
  - **Purpose**: Define the lifecycle state machine and all 14 block states for future candidate task execution.
  - **Report type**: Lifecycle and Block State Report
  - **Depends on**: Tasks 3, 5, and 6
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_lifecycle_block_states_preflight.md`
  - **Required content**:
    - Lifecycle states: CANDIDATE_DRAFT, CANDIDATE_READY_FOR_REVIEW, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY
    - State transition rules from design.md Candidate Lifecycle Rule Model
    - Explicit prohibition: no ACTIVE, APPROVED, or production transition
    - All 14 block states from design.md: BLOCK_SOURCE_INSUFFICIENT, BLOCK_IDENTITY_UNRESOLVED, BLOCK_UNSUPPORTED_ASSET_CLASS, BLOCK_ETF_COMPANY_FALLBACK, BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED, BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY, BLOCK_TRADING_ELIGIBILITY_INFERENCE, BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT, BLOCK_DERIVATIVE_AS_PEER_MEMBER, BLOCK_PEER_GROUP_ID_CREATION, BLOCK_REGISTRY_CREATION, BLOCK_SAI_CONTRACT_SHAPE_VIOLATION, BLOCK_OUTPUT_RESTRICTION_VIOLATION, BLOCK_DRIFT_VIOLATION
    - For each block state: trigger, required response, candidate status outcome, remediation expectation
    - Statement: this artifact defines lifecycle/block rules only; no records transition states
  - **Acceptance criteria**:
    - All 5 lifecycle states documented with transition rules
    - All 14 block states documented with all 4 required columns
    - No production lifecycle states appear
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Rule model definition only. No state transitions executed.
  - **Final status marker**: `CANDIDATE_LIFECYCLE_BLOCK_STATES_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R3, R15 (Candidate Status, Drift Prevention)_

- [ ] 8. Create SAI and Human Approval Boundary Specification
  - **Purpose**: Define SAI read-only interpretation boundaries and human/CTO approval requirements.
  - **Report type**: SAI and Human Approval Boundary Report
  - **Depends on**: Tasks 3, 6, and 7
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/sai_human_approval_boundary_preflight.md`
  - **Required content**:
    - SAI not mutated: no SAI artifact, gate, requirement, task plan, or verification status modified
    - SAI-BLK-21 remains in BLOCK_FINAL_PEER_ASSIGNMENT state
    - Candidate records do not satisfy SAI deferred interface (Section 2.3)
    - SAI may read candidate statuses as context (informational only)
    - SAI may surface blocked/deferred/context-only reasons
    - SAI must not create peers, IDs, registry entries, runtime behavior, or trading implications
    - 17 SAI output contract fields listed with PREFLIGHT_NOT_CANONICAL values
    - No-ad-hoc-peer rule preserved
    - Human/CTO approval gate definition: approver_identity, approval_decision (APPROVED/DENIED/CONDITIONAL), approval_date, approval_scope, conditions
    - Approval scope clarification: approves candidate readiness only; does not activate production; does not convert candidates to production entries; separate production registry spec still required
    - No automated approval pathway
    - Statement: this artifact defines boundaries only; no SAI interaction or approval action occurs
  - **Acceptance criteria**:
    - SAI non-mutation explicitly confirmed
    - All 17 SAI output fields documented with preflight values
    - Human/CTO approval model complete with scope clarification
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Boundary definition only. No SAI interaction. No approval actions.
  - **Final status marker**: `SAI_HUMAN_APPROVAL_BOUNDARY_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R11 (SAI Compatibility), R12 (Human Approval Gate)_

- [ ] 9. Create Output Restrictions and Drift Prevention Specification
  - **Purpose**: Define allowed/forbidden outputs and 8-category drift-prevention rules.
  - **Report type**: Output Restrictions and Drift Prevention Report
  - **Depends on**: Tasks 6, 7, and 8
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/output_restrictions_drift_prevention_preflight.md`
  - **Required content**:
    - Allowed outputs: preflight documentation, candidate draft artifacts, mapping worksheets, evidence gap documentation, verification gate artifacts
    - Naming convention: candidate_ prefix or _preflight suffix required; gate_ prefix for gate artifacts
    - Forbidden outputs: peer_group_registry.yaml, production registry files, files with "registry" lacking candidate_ prefix or _preflight suffix, canonical peer_group_id values, runtime code, validation code, executable implementations, ACTIVE/APPROVED lifecycle states, production_authority other than NONE
    - 8 drift categories: registry drift, ID drift, peer assignment drift, source authority drift, market data drift, SAI drift, runtime drift, trading drift
    - Each drift category: what it prevents, detection mechanism, result if detected (CANDIDATE_BLOCKED + DRIFT_VIOLATION)
    - DRIFT_VIOLATION response pattern: halt, block, document, remediate
    - No runtime / no market data / no trading / no SAI mutation confirmations
    - Statement: this artifact defines rules only; no enforcement is executed
  - **Acceptance criteria**:
    - All allowed and forbidden outputs explicitly listed
    - All 8 drift categories documented with detection and response
    - Naming convention rules are unambiguous
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Rule definition only. No enforcement executed.
  - **Final status marker**: `OUTPUT_RESTRICTIONS_DRIFT_PREVENTION_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R13 (Output Restrictions), R15 (Drift Prevention)_

- [ ] 10. Create Candidate Record Draft Artifacts for PGF-01 through PGF-09
  - **Purpose**: Produce non-production candidate record draft artifacts for all 9 confirmed family universes using only the scope preflight as family/ticker authority and PGMF as methodology authority.
  - **Report type**: Candidate Record Draft Report Set
  - **Depends on**: Tasks 1–9
  - **Output**:
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf01_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf02_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf03_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf04_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf05_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf06_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf07_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf08_preflight.md`
    - `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_records_pgf09_preflight.md`
  - **Required content per artifact**:
    - One candidate record draft (or explicit CANDIDATE_BLOCKED / CANDIDATE_DEFERRED / CANDIDATE_CONTEXT_ONLY record) for each in-scope element from the scope preflight for that family
    - Every record carries: production_authority: NONE, preliminary: true
    - Candidate_Status from allowed set only
    - peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
    - peer_group_id_status: NOT_CREATED
    - source_authority_references (or SOURCE_EVIDENCE_MISSING where gaps exist)
    - methodology_decision_references (PGMF-DEC-01 through PGMF-DEC-10 as applicable)
    - field_taxonomy_mapping_status per record
    - peer_role as preliminary only (not final assignment)
    - SAI output contract fields with PREFLIGHT_NOT_CANONICAL values
    - market_data_fields_status = NOT_POPULATED_IN_PREFLIGHT
    - trading_governance_fields_status = FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
    - unsupported_status where applicable
    - blocked_reason where applicable
    - human_review_status = NOT_REVIEWED
    - CTO_approval_status = NOT_APPROVED
    - PGF-09 handled as rule-based ETF/Fund candidate logic
    - Unsupported/private/derivative/index/basket cases blocked, deferred, context-only, or benchmark_context as required
    - No new family, ticker, subcluster, or benchmark instrument invented
  - **Acceptance criteria**:
    - All 9 family universes (PGF-01 through PGF-09) have a candidate draft artifact
    - Every record carries production_authority: NONE and preliminary: true
    - Every record uses only allowed Candidate_Status values
    - No record contains lifecycle_status = ACTIVE or APPROVED
    - No record contains canonical peer_group_id values
    - No new family, ticker, subcluster, or benchmark instrument is invented
    - PGF-09 correctly represented as rule-based
    - Unsupported/private/derivative/index/basket cases handled per PGMF rules
  - **Hard boundaries**: Non-production candidate drafts only. No production registry. No final peer assignments. No canonical IDs.
  - **Final status marker**: `CANDIDATE_RECORD_DRAFTS_PREFLIGHT_READY_FOR_REVIEW`
  - **Completion rule**: Complete this task only after all 9 declared artifacts exist, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R2, R3, R4, R5, R6, R7, R8, R9, R10, R11 (Family Intake, Candidate Status, Source Authority, Field Taxonomy, all Boundaries)_

- [ ] 11. Create Evidence Gap Register
  - **Purpose**: Document all missing evidence, blocked fields, unresolved identities, unsupported assets, cross-region comparability gaps, source authority gaps, and human review issues discovered during candidate record draft creation.
  - **Report type**: Evidence Gap Register
  - **Depends on**: Task 10
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_evidence_gaps_preflight.md`
  - **Required content**:
    - Gap register table with columns: gap_id, affected_family, affected_candidate_record, gap_type, missing_field_or_evidence, blocking_status, required_remediation, source_authority_domain, human_CTO_review_note
    - Gap types: SOURCE_EVIDENCE_MISSING, IDENTITY_UNRESOLVED, UNSUPPORTED_ASSET_CLASS, CROSS_REGION_COMPARABILITY_INCOMPLETE, CROSS_REGION_FIELDS_INCOMPLETE, DOMAIN_SCOPE_VIOLATION, FIELD_TAXONOMY_INCOMPLETE, ETF_COMPANY_BOUNDARY_ISSUE
    - Every CANDIDATE_BLOCKED record from Task 10 must have a corresponding gap entry
    - Every CANDIDATE_DEFERRED record must have a gap entry explaining deferred methodology need
    - Summary: total gaps by family, total gaps by type, total blocked vs. deferred vs. context-only
    - Remediation priority guidance
    - Statement: this artifact documents evidence gaps only; it does not remediate them
  - **Acceptance criteria**:
    - Every CANDIDATE_BLOCKED and CANDIDATE_DEFERRED record from Task 10 has a corresponding gap entry
    - All gap types are from the defined set
    - Summary statistics are consistent with Task 10 artifacts
    - Remediation expectations are actionable
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Gap documentation only. No remediation executed. No production content.
  - **Final status marker**: `CANDIDATE_EVIDENCE_GAPS_PREFLIGHT_COMPLETE`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: R4, R14, R15 (Source Authority, Verification Gate, Drift Prevention)_

- [ ] 12. Execute Verification Gate VG-PGRC-PREFLIGHT-1
  - **Purpose**: Verify that the preflight specification and candidate draft artifacts are complete, non-production, and safe before any future production registry creation spec begins.
  - **Report type**: Verification Gate Report
  - **Depends on**: Tasks 1–11
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/gate_vg_pgrc_preflight_1.md`
  - **Required content**:
    - Gate identifier: VG-PGRC-PREFLIGHT-1
    - Aggregate result: PASS / FAIL / BLOCKED_PENDING_REMEDIATION / READY_FOR_HUMAN_REVIEW
    - 8 check categories (A–H):
      - A: Family Universe Coverage — all 9 candidate record draft artifacts exist; each family has at least one candidate record or explicit CANDIDATE_BLOCKED/DEFERRED/CONTEXT_ONLY record
      - B: Candidate Status Validity — every record uses only permitted Candidate_Status values; no ACTIVE or APPROVED states
      - C: Production Authority — every record carries production_authority: NONE and preliminary: true
      - D: Peer Group ID Non-Creation — every peer_group_id is PREFLIGHT_PLACEHOLDER_NOT_CANONICAL; zero canonical values
      - E: Source Authority Coverage — all CURRENT_METHODOLOGY fields have source authority references or documented gaps in evidence gap register
      - F: Field Taxonomy Compliance — all CURRENT_METHODOLOGY fields populated or documented as gaps with CANDIDATE_BLOCKED status
      - G: Boundary Violation Zero — zero unresolved boundary violations; all violations documented as CANDIDATE_BLOCKED
      - H: Human Approval Gate Defined — approval model documented and referenceable
    - 8 drift detection categories with per-category pass/fail
    - Evidence references to Tasks 1–11 artifacts
    - Candidate record statistics: total records, by-family, status distribution
    - Evidence gap summary from Task 11
    - Failure report structure (if applicable)
    - Execution timestamp
    - Gate must be explicitly executed as leaf task — not auto-completed
    - Statement: this gate verifies the specification and candidate draft chain; it does not create production content
  - **Acceptance criteria**:
    - All 8 check categories evaluated with explicit pass/fail
    - All 8 drift categories evaluated with zero violations
    - Evidence traces to specific artifacts from Tasks 1–11
    - Candidate record statistics confirm all 9 families covered
    - Gate result clearly stated
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Verification only. No production content created. Must be explicitly executed as leaf task.
  - **Final status marker**: `VG_PGRC_PREFLIGHT_1_READY_FOR_HUMAN_REVIEW`
  - **Completion rule**: Complete this task only after the declared artifact exists, all 8 check categories are evaluated, all 8 drift categories show zero violations, the aggregate verdict is recorded, and the final status marker is present. Do not start the next task. This task must have its own commit and PR.
  - _Requirements: R14 (Verification Gate)_

- [ ] 13. Create Preflight README
  - **Purpose**: Document the spec purpose, boundaries, artifact inventory, and next-step constraints.
  - **Report type**: Framework README
  - **Depends on**: Tasks 1–12
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/README_peer_group_registry_creation_preflight.md`
  - **README location**: Spec root (NOT in artifacts/ directory)
  - **Required content**:
    - Spec purpose: preflight preparation for future peer group registry creation
    - Relationship to completed PGMF (12/12 tasks, VG-PGMF-1 PASS)
    - Requirements / design / tasks / artifact inventory (all 14 tasks and their outputs)
    - Candidate-only boundary: no production registry, no final assignments, no canonical IDs
    - Source authority model: PGMF methodology authority + scope preflight family universe authority
    - Family universe authority rule: scope preflight is sole authority; no new tickers/families invented
    - SAI boundary: not mutated; SAI-BLK-21 stays blocked
    - Human/CTO approval boundary: approves candidate readiness only; separate production spec required
    - Output restrictions: candidate_ prefix or _preflight suffix; forbidden production outputs
    - Verification gate summary: VG-PGRC-PREFLIGHT-1 with 8 checks + 8 drift categories
    - Candidate record draft summary: 9 family artifacts with non-production candidate records
    - Evidence gap summary: documented gaps and remediation status
    - Next-step constraints: after human review, a separate production registry creation spec may be proposed
    - Design invariants summary
    - Statement: Task 14 remains the final completion review and is not replaced by this README
    - Final navigation for future agents: which tasks are complete, what comes next
  - **Acceptance criteria**:
    - All artifact paths documented (Tasks 1–12 outputs)
    - All boundaries confirmed
    - Candidate draft and evidence gap artifacts referenced
    - Next steps clearly constrained
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Documentation only. No execution. No registry.
  - **Final status marker**: `PEER_GROUP_REGISTRY_CREATION_PREFLIGHT_README_READY_FOR_HUMAN_REVIEW`
  - **Completion rule**: Complete this task only after the declared artifact exists, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. Do not start the next task.
  - _Requirements: All (R1–R15 summary)_

- [ ] 14. Create Final Preflight Completion Review
  - **Purpose**: Final review confirming all Tasks 1–13 artifacts are complete, consistent, and non-production.
  - **Report type**: Final Completion Review Report
  - **Depends on**: Tasks 1–13
  - **Output**: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/preflight_completion_review.md`
  - **Required content**:
    - All task artifacts (Tasks 1–13) verified present and complete
    - Requirements traceability: each of R1–R15 mapped to producing task(s)
    - Design traceability: each design section mapped to producing task(s)
    - Candidate record draft verification: all 9 PGF artifacts exist, all records non-production
    - Evidence gap register verification: all blocked/deferred records documented
    - VG-PGRC-PREFLIGHT-1 gate result referenced (must be PASS or READY_FOR_HUMAN_REVIEW)
    - Boundary confirmations:
      - No peer_group_registry.yaml created
      - No final peer assignments made
      - No canonical peer_group_id values minted
      - No SAI artifacts mutated
      - No runtime code created
      - No validation code created
      - No market data integrated
      - No trading/execution logic created
      - No broker/exchange/ATS connections
      - No Tactical Momentum work
    - Recommended next step: Human review, then separate production registry creation spec only after approval
    - Statement: this review confirms specification and candidate draft completeness; it does not activate production use
  - **Acceptance criteria**:
    - All 13 task artifacts confirmed present with status markers
    - All 9 candidate record draft artifacts verified non-production
    - Zero boundary violations found
    - Requirements and design traceability complete
    - VG-PGRC-PREFLIGHT-1 result is PASS or READY_FOR_HUMAN_REVIEW
    - Document carries `production_authority: NONE`
  - **Hard boundaries**: Review only. No production activation. Must not complete until Tasks 1–13 are done.
  - **Final status marker**: `PEER_GROUP_REGISTRY_CREATION_PREFLIGHT_COMPLETE_READY_FOR_HUMAN_REVIEW`
  - **Completion rule**: Complete this task only after the declared artifact exists, all 13 prior task artifacts are confirmed present, acceptance criteria are satisfied, hard boundaries are confirmed, and the final status marker is present. This task must have its own commit and PR.
  - _Requirements: All (R1–R15 final verification)_

## Task Dependency Graph

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": [1],
      "description": "Source alignment must be confirmed before any downstream tasks"
    },
    {
      "wave": 2,
      "tasks": [2, 3, 4, 5],
      "description": "Independent specification tasks — may execute in parallel after source alignment"
    },
    {
      "wave": 3,
      "tasks": [6, 7, 8, 9],
      "description": "Boundary, lifecycle, SAI/approval, and output/drift rules — depend on schema (Task 3) and taxonomy (Task 5)"
    },
    {
      "wave": 4,
      "tasks": [10],
      "description": "Candidate record draft generation — depends on all rule/specification tasks (Tasks 1–9)"
    },
    {
      "wave": 5,
      "tasks": [11],
      "description": "Evidence gap register — depends on candidate record drafts (Task 10)"
    },
    {
      "wave": 6,
      "tasks": [12, 13],
      "description": "Gate verification (Task 12) and README (Task 13) depend on Tasks 1–11 complete"
    },
    {
      "wave": 7,
      "tasks": [14],
      "description": "Final completion review depends on ALL Tasks 1–13 complete"
    }
  ]
}
```

## Notes

- All tasks produce Markdown documentation artifacts under `.kiro/specs/peer-group-registry-creation-preflight/artifacts/` except Task 13 which creates the README at the spec root
- Task 10 produces 9 candidate record draft artifacts (one per family) — these are non-production drafts, not production registry entries
- Task 11 produces an evidence gap register documenting all blocked/deferred/missing-evidence records
- Task 12 is a verification gate that must be explicitly executed — it inspects actual candidate draft artifacts, not just rule definitions
- Task 14 is the final completion review and cannot be marked complete until Tasks 1–13 are all confirmed complete
- No task creates production content: no peer_group_registry.yaml, no canonical peer_group_id values, no final peer assignments, no SAI mutations, no runtime code, no market data integrations, no trading functionality
- Candidate artifacts use candidate_ prefix or _preflight suffix to distinguish from production content
- The scope preflight document is the sole authority for family universe content — no new tickers, families, subclusters, or benchmark instruments may be invented

## Final Planning Status

```
PEER_GROUP_REGISTRY_CREATION_PREFLIGHT_TASKS_HARDENED_READY_FOR_HUMAN_REVIEW
```

---

*End of tasks document.*
