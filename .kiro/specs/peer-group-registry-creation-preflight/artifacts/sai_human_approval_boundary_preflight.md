# SAI and Human Approval Boundary Specification

> **Peer Group Registry Creation Preflight — Task 8: SAI and Human Approval Boundary Specification**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture

---

## 1. Document Metadata

| Key | Value |
|-----|-------|
| title | SAI and Human Approval Boundary Specification |
| spec | peer-group-registry-creation-preflight |
| task | Task 8 |
| report_type | SAI and Human Approval Boundary Report |
| production_authority | NONE |
| preliminary | true |
| status | BOUNDARY_DEFINITION_ONLY |

---

## 2. Document Boundary Statement

This artifact defines SAI read-only interpretation boundaries and human/CTO approval requirements only. It does not:

- Mutate any SAI artifact, gate, requirement, task plan, or verification status
- Interact with SAI runtime or SAI block execution
- Execute any approval action
- Create candidate records
- Assign peers or peer_group_id values
- Create registry content
- Activate production use

**Statement**: This artifact defines boundaries only; no SAI interaction or approval action occurs.

---

## 3. SAI Non-Mutation Confirmation

### 3.1 Explicit Non-Mutation Declaration

The following SAI elements are NOT modified by this preflight:

| SAI Element | Mutation Status | Confirmation |
|-------------|-----------------|--------------|
| SAI artifacts (all 24 block definitions) | NOT MUTATED | No SAI artifact file is created, modified, or deleted |
| SAI gates (VG-SAI-1 through VG-SAI-5) | NOT MUTATED | No verification gate status is changed |
| SAI requirements (SAI-REQ-01 through SAI-REQ-14) | NOT MUTATED | No requirement text, status, or acceptance criteria is altered |
| SAI task plan (Tasks 1–12) | NOT MUTATED | No task status, description, or dependency is modified |
| SAI verification status | NOT MUTATED | No pass/fail result is changed or invented |
| SAI deferred interfaces (deferred_interfaces.md) | NOT MUTATED | No interface contract is modified or extended |
| SAI block states (SAI-BLK-01 through SAI-BLK-24) | NOT MUTATED | No block state transitions are triggered |

### 3.2 SAI-BLK-21 Status

**SAI-BLK-21 (Peer Comparison)** remains in `BLOCK_FINAL_PEER_ASSIGNMENT` state.

| Attribute | Value |
|-----------|-------|
| Block ID | SAI-BLK-21 |
| Block Name | Peer Comparison |
| Current State | BLOCK_FINAL_PEER_ASSIGNMENT |
| peer_comparison_allowed | false |
| blocked_reason | "Peer Group Registry not yet available — candidate records in preflight do not constitute production registry" |
| Unblock condition | Production peer group registry created AND human/CTO approved (outside this preflight scope) |
| This preflight's effect on SAI-BLK-21 | NONE — state unchanged |

### 3.3 Why Candidate Records Do Not Satisfy SAI Deferred Interface (Section 2.3)

Per `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` Section 2.3, SAI expects the Peer Group Registry to provide:

- Canonical peer group definitions per asset
- Peer selection methodology (criteria used to determine peer group membership)
- Peer rotation rules (when and why peers are added/removed)
- Peer group versioning (temporal tracking of composition changes)
- Peer group validity metadata (confidence, staleness indicators)
- Multi-level peer classification (primary, secondary, aspirational peers)

**Candidate records fail ALL six expectations:**

| SAI Expectation | Candidate Record Reality | Satisfied? |
|-----------------|--------------------------|-----------|
| Canonical peer group definitions | peer_group_id = PREFLIGHT_PLACEHOLDER_NOT_CANONICAL; no canonical groups exist | NO |
| Peer selection methodology | peer_role is preliminary only; not final peer selection | NO |
| Peer rotation rules | No rotation rules exist; no production lifecycle | NO |
| Peer group versioning | No version tracking; candidate records are non-production documentation | NO |
| Peer group validity metadata | No confidence or staleness indicators; PREFLIGHT_NOT_CANONICAL values only | NO |
| Multi-level peer classification | peer_role is single preliminary assignment; no primary/secondary/aspirational hierarchy | NO |

**Conclusion**: Candidate records produced by this preflight do not satisfy the SAI deferred peer group registry interface. SAI-BLK-21 cannot be unblocked by candidate records.


---

## 4. SAI Read-Only Interpretation Boundaries

### 4.1 What SAI May Read (Informational Only)

SAI may read candidate statuses as context. This is a one-way informational flow — SAI consumes no production authority from candidate records.

| SAI Read Capability | Allowed | Constraint |
|---------------------|---------|-----------|
| Read Candidate_Status values | YES | Informational only; no operational decision derived |
| Read blocked_reason values | YES | SAI may surface blocked/deferred/context-only reasons to users |
| Read deferred_reason values | YES | SAI may surface deferred methodology gaps |
| Read peer_role (preliminary) | YES | SAI must NOT treat as final peer assignment |
| Read family_id assignments | YES | SAI must NOT treat as canonical family membership |
| Read source_authority_status | YES | SAI may report evidence coverage as context |
| Read comparability_note | YES | SAI may surface cross-region context |

### 4.2 What SAI May Surface

SAI may surface the following from candidate records as informational context:

- Blocked reasons explaining why peer comparison is unavailable
- Deferred reasons explaining which methodology extensions are needed
- Context-only role explanations (why an asset is benchmark_context or private_comparable_context)
- Evidence gap summaries (which fields lack source authority)
- Cross-region comparability notes (what adjustments would be needed)

### 4.3 What SAI Must NOT Do With Candidate Records

SAI is absolutely prohibited from the following actions based on candidate records:

| Prohibited Action | Rule | Block State if Violated |
|-------------------|------|------------------------|
| Create peers from candidate records | SAI must not use candidate peer_role as production peer assignment | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION |
| Create peer_group_id values | SAI must not mint canonical IDs from candidate PREFLIGHT_PLACEHOLDER values | BLOCK_PEER_GROUP_ID_CREATION |
| Create registry entries | SAI must not construct production registry entries from candidate data | BLOCK_REGISTRY_CREATION |
| Create runtime behavior | SAI must not activate peer comparison logic based on candidate records | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION |
| Create trading implications | SAI must not derive tradability or execution eligibility from candidate records | BLOCK_TRADING_ELIGIBILITY_INFERENCE |
| Create ad-hoc peer sets | SAI must never create ad-hoc peers to compensate for missing production registry | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION |
| Unblock SAI-BLK-21 | SAI must not treat candidate records as sufficient to unblock peer comparison | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION |
| Modify SAI deferred interface expectations | SAI interface contract remains unchanged by candidate records | SAI drift violation |

### 4.4 No-Ad-Hoc-Peer Rule

The no-ad-hoc-peer rule from SAI architecture is preserved:

- SAI must NEVER create ad-hoc peers to compensate for a missing or candidate-only registry entry
- Per deferred_interfaces.md Section 2.3 "What SAI Must NOT Define": SAI must not define peer selection criteria or algorithms, peer group composition decisions, peer rotation triggers or rules, peer group creation methodology, peer ranking or scoring, or statistical peer clustering algorithms
- Candidate records do not constitute a registry — they are non-production documentation artifacts
- SAI-BLK-21 blocked_reason explicitly states: "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture"

---

## 5. SAI Output Contract Fields — 17 Fields with PREFLIGHT_NOT_CANONICAL Values

All 17 SAI output contract fields (from PGMF Section 10.3) must be present in every candidate record shape. Each field carries either a derivable preflight value or the explicit placeholder PREFLIGHT_NOT_CANONICAL.

### 5.1 Complete Field Registry

| # | Field | Type | Preflight Value | Production Safety Rule | SAI Consumption Status |
|---|-------|------|----------------|------------------------|----------------------|
| 1 | `peer_group_available` | boolean | `false` | No peer group registry exists in preflight | SAI reads as: no registry available |
| 2 | `peer_comparison_allowed` | boolean | `false` | BLOCK_FINAL_PEER_ASSIGNMENT active; no comparison permitted | SAI reads as: comparison blocked |
| 3 | `blocked_reason` | string | `"Peer Group Registry not yet available"` | Explains why SAI-BLK-21 remains blocked | SAI may surface to users |
| 4 | `unsupported_status` | string | `null` or specific status per asset | Populated for unsupported asset classes | SAI may read as context |
| 5 | `primary_family` | string | `PREFLIGHT_NOT_CANONICAL` | Candidate family assignment only; not production truth | SAI must NOT treat as canonical |
| 6 | `secondary_family` | string | `PREFLIGHT_NOT_CANONICAL` | Cross-family membership (if applicable); not production | SAI must NOT treat as canonical |
| 7 | `peer_role` | enum | `PREFLIGHT_NOT_CANONICAL` | Preliminary role only; not final peer assignment | SAI must NOT treat as final |
| 8 | `core_peer_set` | list[string] | `PREFLIGHT_NOT_CANONICAL` | Not populated — requires production registry with canonical IDs | SAI must NOT construct peer set |
| 9 | `adjacent_peer_set` | list[string] | `PREFLIGHT_NOT_CANONICAL` | Not populated — requires production registry | SAI must NOT construct peer set |
| 10 | `benchmark_context_set` | list[string] | `PREFLIGHT_NOT_CANONICAL` | Candidate benchmark instruments; not canonical | SAI must NOT treat as production |
| 11 | `etf_peer_set` | list[string] | `PREFLIGHT_NOT_CANONICAL` | PGF-09 candidate ETF peers only; not canonical | SAI must NOT treat as production |
| 12 | `comparison_mode_allowed` | enum | `PREFLIGHT_NOT_CANONICAL` | No comparison mode active in preflight | SAI must NOT enable comparison |
| 13 | `financial_comparability_gate_status` | enum | `PREFLIGHT_NOT_CANONICAL` | Not evaluated in preflight; requires production registry | SAI must NOT treat as evaluated |
| 14 | `comparability_note` | string | `PREFLIGHT_NOT_CANONICAL` | Populated per record for cross-region context; not production gate | SAI may read as context only |
| 15 | `data_quality_status` | enum | `PREFLIGHT_NOT_CANONICAL` | Not evaluated in preflight; requires data ingestion framework | SAI must NOT treat as quality-assessed |
| 16 | `as_of_date` | date | `PREFLIGHT_NOT_CANONICAL` | Candidate preparation date; not production registry date | SAI must NOT treat as production date |
| 17 | `methodology_version` | string | `PREFLIGHT_NOT_CANONICAL` | PGMF v1 methodology reference; not production version | SAI reads as methodology source reference |

### 5.2 Field Enforcement Rules

1. Every candidate record MUST include all 17 SAI output contract fields
2. Each field carries either a derivable candidate value OR PREFLIGHT_NOT_CANONICAL
3. No field may carry a production-authority value (any value implying canonical, approved, or active status)
4. If any of the 17 fields is missing → `BLOCK_SAI_CONTRACT_SHAPE_VIOLATION`
5. If any field carries a production-authority value → `BLOCK_SAI_CONTRACT_SHAPE_VIOLATION`
6. Candidate_Status must be set to CANDIDATE_BLOCKED upon violation detection
7. Resolution requires adding the missing field with PREFLIGHT_NOT_CANONICAL value or removing the production-authority value

### 5.3 SAI Contract Shape Compliance Summary

| Compliance Dimension | Status |
|---------------------|--------|
| All 17 fields defined with preflight values | YES |
| No production-authority values permitted | ENFORCED |
| BLOCK_SAI_CONTRACT_SHAPE_VIOLATION defined for violations | YES |
| SAI-BLK-21 remains blocked | CONFIRMED |
| No ad-hoc peer creation permitted | CONFIRMED |
| Candidate records do not satisfy SAI deferred interface | CONFIRMED |


---

## 6. Human/CTO Approval Gate Definition

### 6.1 Approval Gate Purpose

The human/CTO approval gate is a mandatory readiness checkpoint before candidate records may be considered by a future, separate production registry creation spec. Approval inside this preflight does not transition candidate records to production status, does not activate production authority, and does not create production registry entries. No automated process may bypass this gate.

### 6.2 Approval Record Structure

Every approval decision must be recorded with the following fields:

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | `approver_identity` | string | YES | CTO or explicitly CTO-delegated reviewer; must be a named individual with documented delegation authority |
| 2 | `approval_decision` | enum | YES | One of: APPROVED, DENIED, CONDITIONAL |
| 3 | `approval_date` | date (ISO 8601) | YES | Date of the approval decision |
| 4 | `approval_scope` | string | YES | Which specific records and/or families are covered by this decision |
| 5 | `conditions` | list[string] | CONDITIONAL | Required only if approval_decision = CONDITIONAL; structured list of conditions that must be satisfied before re-submission |

### 6.3 Approval Decision Values

| Decision | Meaning | Required Follow-Up |
|----------|---------|-------------------|
| `APPROVED` | Candidate records within scope are confirmed ready for future production registry spec consideration | None within this preflight; records remain non-production until separate production registry spec |
| `DENIED` | Candidate records within scope are rejected; specific issues documented | Records return to CANDIDATE_DRAFT or CANDIDATE_BLOCKED with rejection rationale; rework required |
| `CONDITIONAL` | Records partially acceptable but conditions must be met before re-submission | All conditions must be resolved and documented; records re-enter approval gate through CANDIDATE_READY_FOR_REVIEW |

### 6.4 Approval Decision Handling

**When APPROVED:**
- Candidate records within approval_scope are acknowledged as methodology-ready
- Records remain non-production (production_authority: NONE persists)
- A separate production registry creation spec is still required for production elevation
- APPROVED does not activate production use, runtime behavior, or SAI unblocking

**When DENIED:**
- Records return to CANDIDATE_DRAFT or CANDIDATE_BLOCKED
- Rejection rationale must document: specific issues, affected fields, required corrections
- Reworked records must re-enter the approval gate by transitioning back through CANDIDATE_READY_FOR_REVIEW
- No partial denial — entire approval_scope is denied; specific sub-scoping requires separate approval decisions

**When CONDITIONAL:**
- Conditions must be structured (not free-text only) with: condition_id, condition_description, resolution_criteria
- All conditions must be resolved before re-submission
- Resolution must be documented with: condition_id, resolution_evidence, resolution_date
- Records re-enter approval gate with updated approval request artifact
- Conditional approval does not grant partial production authority

### 6.5 Important Distinction: approval_decision vs Candidate_Status

`approval_decision = APPROVED` is an approval-record decision value only. It is **not** a Candidate_Status value. `Candidate_Status = APPROVED` remains prohibited throughout this preflight.

An APPROVED approval_decision confirms readiness for future production registry spec consideration only; it does not:

- Create production_authority
- Mint peer_group_id values
- Unblock SAI-BLK-21
- Convert candidate records into production entries
- Transition Candidate_Status to any production lifecycle state

The only permitted Candidate_Status values remain: CANDIDATE_DRAFT, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY, CANDIDATE_READY_FOR_REVIEW. No production lifecycle status (ACTIVE, APPROVED) is reachable within this preflight regardless of approval_decision value.

---

## 7. Approval Scope Clarification

### 7.1 What Human/CTO Approval Approves

| Approved Element | Meaning |
|-----------------|---------|
| Candidate readiness | Records have been prepared according to PGMF methodology, source authority rules, field taxonomy, and boundary compliance |
| Structural completeness | All required fields are populated per asset_type |
| Source authority coverage | All CURRENT_METHODOLOGY fields have documented source references |
| Boundary compliance | Zero active boundary violations |
| Evidence gap acknowledgment | Remaining gaps (if any) are explicitly documented and accepted as known risks |

### 7.2 What Human/CTO Approval Does NOT Approve

| Not Approved | Explicit Clarification |
|--------------|----------------------|
| Production activation | Approval does NOT activate production registry use |
| Candidate-to-production conversion | Approval does NOT convert candidate records into production registry entries |
| SAI unblocking | Approval does NOT unblock SAI-BLK-21 or any SAI block state |
| peer_group_id creation | Approval does NOT authorize minting canonical peer_group_id values |
| Runtime activation | Approval does NOT authorize runtime code, APIs, or validation logic |
| Trading implications | Approval does NOT create tradability, execution eligibility, or broker connectivity |
| Market data integration | Approval does NOT authorize vendor connections or data feeds |

### 7.3 Separate Production Registry Spec Requirement

After human/CTO approval of candidate readiness:

1. A **separate production registry creation spec** must be authored
2. That spec must define its own requirements, design, and tasks
3. That spec must have its own human/CTO approval cycle
4. That spec must define the canonical peer_group_id minting process
5. That spec must define the SAI-BLK-21 unblocking conditions
6. That spec must define production lifecycle states (ACTIVE, APPROVED)
7. Only after THAT spec's approval and execution do candidate records become production entries

**The boundary between this preflight and production is absolute.** Human/CTO approval within this preflight is a readiness checkpoint, not a production activation.

---

## 8. No Automated Approval Pathway

### 8.1 Prohibition Statement

There is NO automated pathway that bypasses human/CTO approval for production elevation. This prohibition is absolute and cannot be overridden by:

- Passing all field taxonomy checks
- Passing all boundary compliance checks
- Passing all source authority verifications
- Passing VG-PGRC-PREFLIGHT-1 verification gate
- Any combination of the above

### 8.2 Why Automation Is Prohibited

| Reason | Explanation |
|--------|------------|
| Methodology judgment | Human expertise required to assess whether methodology application is appropriate for specific assets |
| Risk assessment | Automated systems cannot assess institutional risk appetite for peer group composition |
| Edge case handling | Boundary cases (cross-region, multi-segment, hybrid assets) require human judgment |
| Source authority validation | Human review validates that source citations are genuinely supportive, not merely structurally present |
| Downstream impact | Production registry activation has SAI, trading, and portfolio implications requiring human oversight |

### 8.3 Enforcement

- No script, automation, CI pipeline, or SAI process may mark approval_decision as APPROVED
- approval_decision must be recorded by a named human (approver_identity)
- Delegated reviewers must have explicit written delegation from CTO
- System-generated approval suggestions are informational only — the decision remains human


---

## 9. SAI and Approval Boundary Integration

### 9.1 Relationship Between SAI Boundary and Approval Gate

| Boundary Aspect | SAI Boundary | Human Approval Gate |
|----------------|-------------|---------------------|
| Governs | SAI read-only access to candidate data | Readiness checkpoint for future production registry spec consideration |
| Trigger | SAI attempts to consume candidate records | Candidate records reach CANDIDATE_READY_FOR_REVIEW |
| Outcome if respected | SAI reads context only; no operational action | Approval decision recorded; records remain non-production |
| Outcome if violated | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | No violation possible — gate cannot be bypassed |
| Production authority granted | NONE | NONE (even after APPROVED) |

### 9.2 Combined Boundary Flow

```
Candidate Records (production_authority: NONE)
    │
    ├─── SAI Boundary ────────────────────────────────────────────┐
    │    SAI may READ candidate statuses (informational only)     │
    │    SAI may SURFACE blocked/deferred/context reasons          │
    │    SAI must NOT create peers, IDs, registry, runtime        │
    │    SAI-BLK-21 remains BLOCK_FINAL_PEER_ASSIGNMENT           │
    │    No-ad-hoc-peer rule preserved                            │
    └─────────────────────────────────────────────────────────────┘
    │
    ├─── Human/CTO Approval Gate ─────────────────────────────────┐
    │    Approves CANDIDATE READINESS only                         │
    │    Does NOT activate production                              │
    │    Does NOT convert to production entries                    │
    │    Separate production registry spec still required          │
    │    No automated pathway                                      │
    └─────────────────────────────────────────────────────────────┘
    │
    ▼
Records remain: production_authority: NONE | preliminary: true
```

---

## 10. Dependency Traceability

### 10.1 Task Dependencies

| Dependency | Artifact | What This Task Uses |
|------------|----------|-------------------|
| Task 3 | `candidate_record_schema_preflight.md` | SAI compatibility fields definition (17 fields); candidate record shape |
| Task 6 | `boundary_rules_preflight.md` | SAI boundary rules (Section 11); block state definitions |
| Task 7 | `candidate_lifecycle_block_states_preflight.md` | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION definition; lifecycle state machine |

### 10.2 Requirements Traceability

| Requirement | Acceptance Criteria Addressed |
|-------------|------------------------------|
| R11 (SAI Compatibility Boundary) | AC 1: SAI non-mutation (Section 3); AC 2: Compatibility dimensions (Section 3.3); AC 3: 17 fields (Section 5); AC 4: SAI-BLK-21 status (Section 3.2); AC 5: No-ad-hoc-peer (Section 4.4); AC 6: Shape violation handling (Section 5.2) |
| R12 (Human Approval Gate) | AC 1: Approval gate defined (Section 6); AC 2: Approval record structure (Section 6.2); AC 3: No automated pathway (Section 8); AC 4: Family-level approval request (referenced); AC 5: Denial/conditional handling (Section 6.4); AC 6: Conditional resolution (Section 6.4) |

### 10.3 Design Traceability

| Design Section | This Artifact Section |
|----------------|----------------------|
| SAI Compatibility Design | Sections 3, 4, 5 |
| Human/CTO Approval Design | Sections 6, 7, 8 |
| Component 6: Governance Layer | Sections 6, 7, 8, 9 |
| Design Invariant #4 (No SAI mutation) | Section 3 |
| Block State: BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | Section 5.2 |

---

## 11. Acceptance Criteria Verification

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | SAI non-mutation explicitly confirmed | YES | Section 3.1 — all 7 SAI element categories confirmed NOT MUTATED |
| 2 | All 17 SAI output fields documented with preflight values | YES | Section 5.1 — complete field registry with types, values, and safety rules |
| 3 | Human/CTO approval model complete with scope clarification | YES | Sections 6, 7 — approval structure, decision values, scope clarification |
| 4 | Document carries production_authority: NONE | YES | Section 1 metadata table |

---

## 12. Boundary Confirmation

| Boundary | Status |
|----------|--------|
| No SAI interaction occurs | CONFIRMED |
| No SAI artifacts mutated | CONFIRMED |
| No approval actions executed | CONFIRMED |
| No candidate records created | CONFIRMED |
| No peer assignments made | CONFIRMED |
| No peer_group_id values created | CONFIRMED |
| No registry content created | CONFIRMED |
| No runtime code created | CONFIRMED |
| No market data integration | CONFIRMED |
| No trading or execution scope | CONFIRMED |
| No PGF candidate artifacts created | CONFIRMED |
| No validation code created | CONFIRMED |
| production_authority: NONE | CONFIRMED |
| Boundary definition only | CONFIRMED |
| Task 9 not started | CONFIRMED |

---

## 13. Final Status

```
SAI_HUMAN_APPROVAL_BOUNDARY_PREFLIGHT_COMPLETE
```

---

*End of SAI and Human Approval Boundary Specification artifact.*
