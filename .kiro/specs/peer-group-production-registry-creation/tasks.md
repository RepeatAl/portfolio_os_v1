# Implementation Plan: Peer Group Production Registry Creation

## Overview

This plan covers all documentation-only preparation tasks required before a future production registry may be created. All tasks produce Markdown documentation artifacts only. No production registry is created. No canonical peer_group_id values are minted. No candidate records are approved. No SAI mutation occurs.

**Requirements source**: requirements.md v2 (hardened against MoneyHorst SSOT)
**Design source**: design.md v1
**Status**: DOCUMENTATION_ONLY_PREPARATION

## Commit and Review Protocol

1. Execute exactly one task per implementation cycle unless explicitly instructed otherwise.
2. After completing a task, update only the task's declared output artifact and the tasks.md checkbox.
3. Commit after each completed task.
4. Do not combine multiple tasks in one commit unless explicitly instructed.
5. Do not start the next task automatically.
6. Wait for human instruction before starting the next task.
7. Task 14 (Final Spec Readiness Review) must have its own commit/PR and must not run until Tasks 1–13 are complete.

## Commit Message Format

Use: `docs(peer-group-production-registry-creation): Task N: <description>`

## Hard Boundaries — No Task May Produce

- peer_group_registry.yaml or any production registry file
- Canonical peer_group_id values
- Candidate record approvals or Candidate_Status mutations
- SAI artifact mutations
- Runtime code, validation code, or executable implementations
- Market data integrations or vendor connections
- Trading, broker, exchange, ATS, routing, allocation, or execution logic
- Portfolio recommendations, conviction scores, target prices, or expected returns
- Scoring, ranking, or opportunity prioritization outputs
- Semantic state activation or PM reasoning generation
- Report text rendering or dashboard rendering
- Correlation, beta, covariance, or factor exposure calculations
- Portfolio health calculations

## README Requirements

Tasks that produce README files must explain the relevant concept for both humans and future AI agents in a way that prevents drift. Each README must:
- State what the artifact defines
- State what it does NOT do
- Reference controlling sources
- Include boundary confirmations

## Tasks

- [x] 1. Create Source Authority Matrix
  - **Purpose**: Document the complete source authority classification for every governing document referenced by this spec.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/source_authority_matrix.md`
  - **Required content**:
    - Every source from design.md Section 3 classified as: controlling, methodology authority, terminology authority, governance authority, boundary authority, downstream compatibility authority, or context only
    - Authority chain showing how decisions flow from controlling sources through methodology to field rules
    - Extension governance: how new sources may be added (CTO approval required)
    - Statement: this artifact classifies sources only; it does not create registry content
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_source_authority_matrix.md`
    - Explains what source authority means in this spec context
    - Explains why PGMF is sole methodology authority
    - Explains the difference between controlling and context-only sources
    - States that adding a source without CTO approval is prohibited
  - **Acceptance criteria**:
    - All 27+ sources from design.md classified
    - No source introduced without documented authority type
    - Extension governance documented
    - README explains the model for humans and agents
  - **Hard boundaries**: Documentation only. No registry content.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 1: Add source authority matrix`
  - _Requirements: R12_

- [ ] 2. Create Registry Schema Specification
  - **Purpose**: Define the complete production registry schema (YAML structure, field definitions, types, constraints) as a specification document without creating the actual registry file.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/registry_schema_specification.md`
  - **Required content**:
    - Complete field table with: field_name, type, required/optional, default_value, description, source_requirement
    - YAML structure definition (root metadata, family sections, record format)
    - Multi-segment representation model (primary_context, secondary_context, dependency_context, benchmark_context)
    - Regional context field structure
    - Structural break caveat field structure
    - Dependency relationships array structure with all governed relationship_type and target_type values
    - Authority fields (production_authority, lifecycle_state, approver_identity, approval_date)
    - Source traceability fields
    - Confidence/evidence fields
    - Field that must NOT exist in schema (prohibited fields table)
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_registry_schema_specification.md`
    - Explains the schema is a specification, not the registry itself
    - Explains multi-segment representation purpose (AMZN use case)
    - Explains regional_context purpose (MELI, STNE, GRAB)
    - Explains structural_break_caveat purpose (GEV, UBS)
    - States that creating peer_group_registry.yaml from this schema requires separate Human_Approval_Gate passage
  - **Acceptance criteria**:
    - All fields from design.md Section 7 documented with types and constraints
    - Multi-segment representation fully specified
    - Dependency relationship structure matches design.md Section 12
    - Prohibited fields table present
    - README prevents agent drift on schema vs registry distinction
  - **Hard boundaries**: Schema specification only. No peer_group_registry.yaml created.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 2: Add registry schema specification`
  - _Requirements: R1, R15, R16_

- [ ] 3. Create Layer Separation and Boundary Specification
  - **Purpose**: Define the explicit architectural layer boundaries showing what the registry owns vs what belongs to other Portfolio OS layers.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/layer_separation_boundary_specification.md`
  - **Required content**:
    - Layer separation table from design.md Section 5
    - For each layer: what it owns, what it does NOT own, interaction mode with registry
    - Prohibited cross-layer behaviors table
    - Registry schema boundaries (contains vs excludes) from design.md Section 6
    - No-Authority-Simulation rules
    - Correlation Calculation Prohibition Table from design.md Section 16
    - Dependency Boundary Table from design.md Section 15
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_layer_separation_boundary.md`
    - Explains why the registry must not calculate correlations, scores, or portfolio health
    - Explains the difference between providing structural context and performing reasoning
    - States that each downstream system owns its own calculations
    - Prevents agent drift on registry scope
  - **Acceptance criteria**:
    - All 10 layers from design.md documented with boundaries
    - Prohibited behaviors explicitly listed
    - Correlation prohibition table present
    - No-Authority-Simulation confirmed
  - **Hard boundaries**: Documentation only. No calculations implemented.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 3: Add layer separation and boundary specification`
  - _Requirements: R13, R17, R27, R28, R29_

- [ ] 4. Create Canonical ID Minting Rules Specification
  - **Purpose**: Define the rules governing how canonical peer_group_id values will be minted in the future, without minting any IDs.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/canonical_id_minting_rules.md`
  - **Required content**:
    - ID format: PG-{FAMILY}-{SEQ:4}-{CHECK:2}
    - Immutability rule: once minted, never reused or reassigned
    - Minting prerequisites: Human_Approval_Gate Stage 3 must pass
    - Minting record fields: timestamp, approver_identity, source_candidate_record_ref, verification_gate_evidence_ref
    - Sequence numbering rules per family
    - Checksum algorithm specification
    - Prohibition: no IDs minted during spec preparation
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_canonical_id_minting_rules.md`
    - Explains that IDs are permanent institutional identifiers
    - Explains why premature minting is dangerous (irreversible)
    - States that Human_Approval_Gate Stage 3 must pass before any minting
    - Prevents agent drift on ID creation authority
  - **Acceptance criteria**:
    - Format fully specified
    - All prerequisites documented
    - Minting record structure complete
    - No IDs minted
  - **Hard boundaries**: Rules specification only. Zero IDs minted.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 4: Add canonical ID minting rules`
  - _Requirements: R2_

- [ ] 5. Create P1–P4 Carry-Forward Matrix
  - **Purpose**: Document all 19 owner-verified decisions in a structured matrix format that can be deterministically validated against future registry content.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/p1_p4_carry_forward_matrix.md`
  - **Required content**:
    - Complete decision table from design.md Section 9 (all 19 entries)
    - For each decision: gap_id, asset, family, role/subcluster, context fields, conditions, status
    - Approved decisions: explicit field values expected in production registry
    - Conditional decisions: conditions that must be verified before production activation
    - Deferred decisions: blocking criteria that prevent production until resolved
    - Traceability to P1–P4 source decision records
  - **Acceptance criteria**:
    - All 19 decisions documented
    - Each decision traceable to source record
    - Conditions and caveats preserved
    - Deferred items explicitly blocked
  - **Hard boundaries**: Documentation only. No candidate records modified.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 5: Add P1-P4 carry-forward matrix`
  - _Requirements: R3, R4, R5, R6, R7_

- [ ] 6. Create Deferred Decision Resolution Model
  - **Purpose**: Document the resolution path, governance requirements, and blocking criteria for all deferred decisions.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/deferred_decision_resolution_model.md`
  - **Required content**:
    - PLTR / PGF-10 architecture requirement: resolution paths, CTO decision criteria, blocking until resolved
    - PGF-09 ETF/fund data feed precondition: 10 required feeds, approval criteria, blocking until feeds defined
    - AMZN multi-segment fallback: schema capability verification, fallback to context/benchmark
    - For each: owner (CTO), resolution evidence required, what happens if unresolved
    - Governance: no silent promotion rule
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_deferred_decision_resolution.md`
    - Explains what "deferred" means in this governance model
    - Explains why silent promotion is the primary risk
    - States that CTO must explicitly resolve each deferred item with identity and date
    - Prevents agent drift on deferred-to-production transitions
  - **Acceptance criteria**:
    - All 3 deferred items documented with resolution paths
    - Blocking criteria explicit
    - CTO ownership clear
    - No silent promotion possible
  - **Hard boundaries**: Documentation only. No decisions resolved.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 6: Add deferred decision resolution model`
  - _Requirements: R8_

- [ ] 7. Create Dependency Relationship Specification
  - **Purpose**: Define the complete dependency_relationships model including all governed types, structures, extension governance, and graph-readiness properties.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/dependency_relationship_model_specification.md`
  - **Required content**:
    - Full YAML structure from design.md Section 12
    - All 10 relationship_type values with definitions and examples
    - All 8 target_type values with definitions
    - relationship_direction rules (depends_on, depended_by, bidirectional)
    - evidence_status and confidence_context allowed values
    - Graph-readiness model from design.md Section 13
    - Extension governance from design.md Section 14
    - Dependency boundary table from design.md Section 15
    - What the registry provides vs what downstream systems calculate
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_dependency_relationship_model.md`
    - Explains that dependencies are structural context, not calculations
    - Explains graph-readiness without graph-calculation
    - States that correlations, beta, factor exposure belong to other layers
    - Explains extension governance (CTO approval for new types)
    - Prevents agent drift on dependency scope
  - **Acceptance criteria**:
    - All types fully defined
    - Graph-readiness documented
    - Extension governance clear
    - Boundary between context and calculation explicit
  - **Hard boundaries**: Documentation only. No correlations calculated. No graph algorithms executed.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 7: Add dependency relationship specification`
  - _Requirements: R11, R30, R31, R32_

- [ ] 8. Create SAI Read-Only Interface Contract
  - **Purpose**: Define the contract boundary through which SAI consumes peer group data without mutating the registry or SAI artifacts.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/sai_read_only_interface_contract.md`
  - **Required content**:
    - SAI deferred interface fields: peer_group_available, peer_comparison_allowed, peer_role, core_peer_set, adjacent_peer_set, benchmark_context_set, comparability_note, methodology_version
    - Data format and delivery mechanism
    - Read-only constraint: SAI may not write back to registry
    - No SAI mutation rule: no SAI requirement, design, artifact, or gate modified
    - SAI boundary rules preserved: no-scoring, no-recommendation, no-allocation, no-trading
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_sai_read_only_contract.md`
    - Explains that SAI is a downstream consumer, not a registry controller
    - Explains the deferred interface model
    - States that no SAI artifact may be modified during registry creation
    - Prevents agent drift on SAI mutation
  - **Acceptance criteria**:
    - All interface fields documented
    - Read-only boundary explicit
    - No-SAI-mutation confirmed
    - SAI boundary rules preserved
  - **Hard boundaries**: Documentation only. No SAI mutation. No SAI artifacts modified.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 8: Add SAI read-only interface contract`
  - _Requirements: R10_

- [ ] 9. Create Verification Gate Definition (VG-PGRC-PRODUCTION-1)
  - **Purpose**: Define the 16 deterministic checks that must pass before production registry activation.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/verification_gate_vg_pgrc_production_1.md`
  - **Required content**:
    - All 16 checks (A–P) from design.md Section 22 with detailed pass/fail criteria
    - For each check: what is verified, how verification is performed, what constitutes failure
    - Gate result states: PASS, FAIL, BLOCKED_PENDING_REMEDIATION
    - Failure handling: block production activation, report to CTO
    - Evidence artifact requirements
    - Explicit execution requirement: gate must be run as leaf task, not auto-completed
  - **Acceptance criteria**:
    - All 16 checks documented with deterministic criteria
    - Failure handling explicit
    - No auto-completion allowed
    - Evidence requirements clear
  - **Hard boundaries**: Gate definition only. Gate not executed in this task.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 9: Add verification gate definition`
  - _Requirements: R11_

- [ ] 10. Create Human/CTO Approval Gate Specification
  - **Purpose**: Define the 4-stage human approval model with artifact requirements and governance rules.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/human_cto_approval_gate_specification.md`
  - **Required content**:
    - Stage 1: Spec Initiation Approval — what it gates, artifact format
    - Stage 2: Schema Finalization Approval — what it gates, artifact format
    - Stage 3: Canonical ID Minting Authorization — what it gates, artifact format
    - Stage 4: Production Registry Activation — what it gates, artifact format
    - Each stage: approver identity, date, scope, conditions, VG evidence
    - No-bypass rule: no automated pathway around human approval
    - Signed approval artifact format
  - **README output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/README_human_cto_approval_gates.md`
    - Explains the 4-stage model in plain language
    - Explains why each stage exists and what it prevents
    - States that no automated process may create production authority
    - Prevents agent drift on approval shortcuts
  - **Acceptance criteria**:
    - All 4 stages documented with artifact formats
    - No-bypass rule explicit
    - Approval artifact structure defined
  - **Hard boundaries**: Documentation only. No approval gates executed.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 10: Add human CTO approval gate specification`
  - _Requirements: R9_

- [ ] 11. Create ETF/Fund PGF-09 Data Feed Specification
  - **Purpose**: Define the 10 required production data feeds for PGF-09 ETF/fund membership population.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/etf_fund_pgf09_data_feed_specification.md`
  - **Required content**:
    - All 10 feeds from design.md Section 20: AUM, TER, holdings date, holdings composition, benchmark methodology, issuer, domicile, liquidity/spread, replication method, fund structure
    - For each: field name, data type, provenance requirements, update frequency, quality validation rules
    - CTO approval requirement before feed activation
    - Asset Type and Sentiment Guidance alignment
    - No-manual-finalization rule
    - No fund scoring, ranking, or recommendation
  - **Acceptance criteria**:
    - All 10 feeds specified with provenance
    - CTO approval required
    - No manual finalization allowed
    - Asset Type Guidance referenced
  - **Hard boundaries**: Specification only. No data feeds implemented. No APIs created.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 11: Add ETF fund PGF-09 data feed specification`
  - _Requirements: R14_

- [ ] 12. Create Downstream Compatibility Map
  - **Purpose**: Document how each downstream Portfolio OS system may consume registry data and what boundaries apply.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/downstream_compatibility_map.md`
  - **Required content**:
    - All 8 downstream systems from design.md Section 17
    - For each: consumption mode (read-only), what calculations they own, what registry provides
    - Prohibited Output Table from design.md Section 24 (all 12 categories)
    - Confidence and Evidence model from design.md Section 19
    - Multilingual/rendering boundary from design.md Section 21
  - **Acceptance criteria**:
    - All 8 systems documented
    - Read-only consumption confirmed for each
    - Prohibited outputs table present
    - Confidence model documented (methodology alignment, not prediction)
  - **Hard boundaries**: Documentation only. No downstream integrations implemented.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 12: Add downstream compatibility map`
  - _Requirements: R13, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26_

- [ ] 13. Create Spec README
  - **Purpose**: Document the spec purpose, boundaries, artifact inventory, and navigation for humans and future agents.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/README_peer_group_production_registry_creation.md`
  - **README location**: Spec root (NOT in artifacts/ directory)
  - **Required content**:
    - Spec purpose: documentation-only preparation for future production registry creation
    - Relationship to completed preflight, P1–P4 decisions, readiness review
    - Requirements / design / tasks / artifact inventory
    - All hard boundaries restated
    - MoneyHorst / Portfolio OS architectural position
    - Layer separation summary
    - Dependency relationship model summary
    - What comes after this spec (Human_Approval_Gate → future execution phase)
    - Statement: this spec defines the path; it does not walk it
  - **Acceptance criteria**:
    - All artifacts documented
    - All boundaries confirmed
    - Navigation clear for humans and agents
    - No scope expansion
  - **Hard boundaries**: Documentation only. No registry.
  - **Commit**: `docs(peer-group-production-registry-creation): Task 13: Add spec README`
  - _Requirements: All (R1–R32 summary)_

- [ ] 14. Final Spec Readiness Review
  - **Purpose**: Verify all Tasks 1–13 artifacts are complete, consistent, and non-production before any future execution phase may be proposed.
  - **Output**: `.kiro/specs/peer-group-production-registry-creation/artifacts/spec_readiness_review.md`
  - **Required content**:
    - All task artifacts (Tasks 1–13) verified present
    - Requirements traceability: each R1–R32 mapped to producing task(s)
    - Design traceability: each design section mapped to producing task(s)
    - Boundary confirmations: zero prohibited outputs
    - Deferred decisions still deferred (no silent promotion)
    - P1–P4 carry-forward verified present
    - Verification gate definition present (not executed)
    - Human/CTO approval gate specification present (not executed)
    - README present and complete
    - Final recommendation: SPEC_PREPARATION_COMPLETE_READY_FOR_HUMAN_CTO_REVIEW
  - **Acceptance criteria**:
    - All 13 prior task artifacts confirmed present
    - Zero boundary violations
    - No premature execution
    - Requirements and design traceability complete
  - **Hard boundaries**: Review only. No production activation. Must not complete until Tasks 1–13 are done.
  - **Final status marker**: `PEER_GROUP_PRODUCTION_REGISTRY_CREATION_SPEC_PREPARATION_COMPLETE`
  - **Commit**: `docs(peer-group-production-registry-creation): Task 14: Add final spec readiness review`
  - _Requirements: All (R1–R32 final verification)_

## Task Dependency Graph

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": [1],
      "description": "Source authority must be established before any downstream specification"
    },
    {
      "wave": 2,
      "tasks": [2, 3, 4, 5],
      "description": "Schema, layer boundaries, ID rules, and P1-P4 matrix — independent after source authority"
    },
    {
      "wave": 3,
      "tasks": [6, 7, 8],
      "description": "Deferred decisions, dependency model, and SAI contract — depend on schema and P1-P4"
    },
    {
      "wave": 4,
      "tasks": [9, 10, 11, 12],
      "description": "Verification gate, approval gates, ETF feeds, downstream map — depend on schema and boundaries"
    },
    {
      "wave": 5,
      "tasks": [13],
      "description": "Spec README depends on all specification tasks complete"
    },
    {
      "wave": 6,
      "tasks": [14],
      "description": "Final readiness review depends on ALL Tasks 1–13 complete"
    }
  ]
}
```

## Notes

- All tasks produce Markdown documentation artifacts under `.kiro/specs/peer-group-production-registry-creation/artifacts/` except Task 13 which creates the README at spec root
- Tasks that produce README files create them to prevent drift by future agents
- No task creates production content: no peer_group_registry.yaml, no canonical peer_group_id values, no candidate approvals, no SAI mutations, no runtime code, no market data integrations, no trading functionality
- Task 14 is the final readiness review and cannot be marked complete until Tasks 1–13 are confirmed complete
- After Task 14, a separate Human_Approval_Gate (Stage 1: Spec Initiation) must pass before any execution phase begins

---

```
PEER_GROUP_PRODUCTION_REGISTRY_CREATION_TASKS_READY
```

---

*End of tasks document.*
