# Candidate Lifecycle and Block State Specification

> **Peer Group Registry Creation Preflight — Task 7: Candidate Lifecycle and Block State Specification**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture

---

## 1. Document Metadata

| Key | Value |
|-----|-------|
| title | Candidate Lifecycle and Block State Specification |
| spec | peer-group-registry-creation-preflight |
| task | Task 7 |
| report_type | Candidate Lifecycle and Block State Report |
| production_authority | NONE |
| preliminary | true |
| status | RULE_DEFINITION_ONLY |

---

## 2. Document Boundary Statement

This artifact defines candidate lifecycle and block-state rules only. It does not:

- Create candidate records
- Transition candidate records between states
- Assign peers
- Create peer_group_id values
- Create registry content
- Activate production use

All lifecycle states, transitions, and block-state rules defined herein govern future preflight task execution (Task 10 candidate record drafts). Task 7 itself does not execute any state transition — it defines the rule model only.

---

## 3. Candidate_Status Allowed Values (Exhaustive)

### 3.1 Permitted States

The following 5 states constitute the complete, exhaustive set of permitted Candidate_Status values. No other values are allowed.

| # | Status | Description |
|---|--------|-------------|
| 1 | `CANDIDATE_DRAFT` | Initial state; record created but not yet fully validated |
| 2 | `CANDIDATE_READY_FOR_REVIEW` | Record passes all checks; awaits human/CTO review |
| 3 | `CANDIDATE_BLOCKED` | Blocking condition prevents progress; requires remediation |
| 4 | `CANDIDATE_DEFERRED` | Requires future methodology extension; not actionable in this preflight |
| 5 | `CANDIDATE_CONTEXT_ONLY` | Context role only (benchmark_context / private_comparable_context / excluded_non_peer) |

### 3.2 Explicitly Prohibited States

The following states are FORBIDDEN in any candidate record during preflight. No automated or manual process within this preflight may assign these values:

| Prohibited Status | Reason for Prohibition |
|-------------------|----------------------|
| `ACTIVE` | Production lifecycle — requires separate production registry spec |
| `APPROVED` | Production lifecycle — requires human/CTO approval AND production registry spec |
| `PRODUCTION` | Production lifecycle — no production content exists in preflight |
| `VALIDATED` | Implies production validation — not achievable in preflight |
| `FINAL` | Implies immutability and production authority — contradicts preliminary: true |
| `ASSIGNED` | Implies final peer assignment — preflight peer_role is preliminary only |
| `TRADEABLE` | Trading inference — violates trading boundary (R10) |
| `TRADING_ENABLED` | Trading inference — violates trading boundary (R10) |

### 3.3 No Automated Promotion Path

There is NO automated promotion path from any candidate status to any production status. The boundary between candidate lifecycle and production lifecycle requires:

1. Completion of all preflight tasks (Tasks 1–14)
2. VG-PGRC-PREFLIGHT-1 PASS
3. Human/CTO review and approval
4. A separate production registry creation spec (not part of this preflight)
5. Independent production registry spec approval


---

## 4. Lifecycle State Definitions

### 4.1 CANDIDATE_DRAFT

| Attribute | Value |
|-----------|-------|
| **Definition** | Initial state assigned to every candidate record upon creation during future Task 10 execution. Represents a record that has been structurally created but not yet fully validated against field taxonomy, source authority, and boundary rules. |
| **Entry conditions** | Record is created during preflight task execution with all mandatory structural fields populated per the candidate record schema (Task 3). |
| **Exit conditions** | Record transitions to another state based on validation outcomes (all checks pass → READY_FOR_REVIEW; blocking condition → BLOCKED; future methodology needed → DEFERRED; context role only → CONTEXT_ONLY). |
| **Terminal behavior** | Non-terminal. CANDIDATE_DRAFT is always a transitory state that must resolve to another state after validation. |
| **Required fields** | All REQUIRED fields per asset_type from field taxonomy (Task 5); candidate_record_id, candidate_record_id_status, production_authority, preliminary, Candidate_Status, family_id, family_name, asset_name, asset_type, object_type |
| **Allowed next states** | CANDIDATE_READY_FOR_REVIEW, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY |
| **Prohibited next states** | ACTIVE, APPROVED, PRODUCTION, VALIDATED, FINAL, ASSIGNED, TRADEABLE, TRADING_ENABLED |
| **Human/CTO review relevance** | Not yet eligible for review — must pass all checks first |
| **Production safety rule** | Record carries production_authority: NONE; preliminary: true; peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL |

### 4.2 CANDIDATE_READY_FOR_REVIEW

| Attribute | Value |
|-----------|-------|
| **Definition** | Record has passed all field taxonomy completeness checks, source authority validation, and boundary rule compliance. It is structurally ready for human/CTO review. This state does NOT imply approval, production readiness, or final peer assignment. |
| **Entry conditions** | All CURRENT_METHODOLOGY fields populated with source authority references; field_taxonomy_mapping_status = COMPLETE; zero boundary violations (ETF, market data, trading, SAI, unsupported, cross-region); zero drift violations; all REQUIRED fields present per asset_type. |
| **Exit conditions** | Within preflight scope: terminal (awaits future human/CTO approval process). After future human review: may return to CANDIDATE_DRAFT if denied or conditional. |
| **Terminal behavior** | Terminal within preflight scope. The record awaits future human/CTO approval which occurs outside this preflight's authority. |
| **Required fields** | All fields from CANDIDATE_DRAFT plus: field_taxonomy_mapping_status = COMPLETE, source_authority_status = SOURCE_AUTHORITY_PRESENT, zero active block states |
| **Allowed next states** | Future human/CTO approval (outside preflight scope); CANDIDATE_DRAFT (if review denied or conditional — future process) |
| **Prohibited next states** | ACTIVE, APPROVED, PRODUCTION, VALIDATED, FINAL, ASSIGNED, TRADEABLE, TRADING_ENABLED |
| **Human/CTO review relevance** | Primary state for human/CTO review eligibility. Human review addresses candidate readiness only — not production activation. |
| **Production safety rule** | CANDIDATE_READY_FOR_REVIEW does NOT equal production readiness. Record still carries production_authority: NONE. Human/CTO approval of readiness does not create production authority. |

### 4.3 CANDIDATE_BLOCKED

| Attribute | Value |
|-----------|-------|
| **Definition** | Record has at least one blocking condition that prevents progress toward CANDIDATE_READY_FOR_REVIEW. The record cannot advance until the blocking condition is resolved through documented remediation. |
| **Entry conditions** | At least one of the 14 block states (Section 6) is triggered; blocked_reason field populated with the specific block state identifier. |
| **Exit conditions** | Blocking condition resolved and documented with resolution evidence; record returns to CANDIDATE_DRAFT for re-validation. |
| **Terminal behavior** | Non-terminal. CANDIDATE_BLOCKED records may return to CANDIDATE_DRAFT after remediation. However, if remediation is not achievable within preflight scope, the record may be manually reclassified as CANDIDATE_DEFERRED by human/CTO decision. |
| **Required fields** | All fields from CANDIDATE_DRAFT plus: blocked_reason (non-null, specific block state identifier), Candidate_Status = CANDIDATE_BLOCKED |
| **Allowed next states** | CANDIDATE_DRAFT (after remediation with documented resolution evidence) |
| **Prohibited next states** | CANDIDATE_READY_FOR_REVIEW (cannot skip DRAFT after remediation), ACTIVE, APPROVED, PRODUCTION, VALIDATED, FINAL, ASSIGNED, TRADEABLE, TRADING_ENABLED |
| **Human/CTO review relevance** | Human/CTO may review blocked records to understand gaps. May authorize reclassification to CANDIDATE_DEFERRED if remediation requires future methodology extension. |
| **Production safety rule** | Blocked records are never eligible for production. Blocking condition must be fully resolved before any future production consideration. |

### 4.4 CANDIDATE_DEFERRED

| Attribute | Value |
|-----------|-------|
| **Definition** | Record requires future methodology extension that is not available in the current PGMF v1 scope. The record is not actionable within this preflight and requires a separate future spec to address the methodology gap. |
| **Entry conditions** | Record's blocking condition requires methodology not covered by PGMF-DEC-01 through PGMF-DEC-10; OR asset requires scope expansion beyond current v1 methodology; OR human/CTO determines that remediation requires future work outside preflight scope. |
| **Exit conditions** | Terminal within preflight. No exit from CANDIDATE_DEFERRED is permitted during this preflight phase. Future methodology extension spec may address deferred records. |
| **Terminal behavior** | Terminal within preflight scope. Once a record is CANDIDATE_DEFERRED, it remains in that state until a future methodology extension spec addresses the gap. |
| **Required fields** | All fields from CANDIDATE_DRAFT plus: blocked_reason or deferred_reason documenting the specific methodology gap, reference to which PGMF decisions were evaluated and found insufficient |
| **Allowed next states** | None within preflight (terminal). Future methodology extension spec may re-activate. |
| **Prohibited next states** | CANDIDATE_DRAFT (within preflight), CANDIDATE_READY_FOR_REVIEW, CANDIDATE_BLOCKED (reversal), ACTIVE, APPROVED, PRODUCTION, VALIDATED, FINAL, ASSIGNED, TRADEABLE, TRADING_ENABLED |
| **Human/CTO review relevance** | Human/CTO reviews deferred records to understand methodology gaps. May prioritize future extension work. Cannot override deferral within preflight. |
| **Production safety rule** | Deferred records are never eligible for production within this preflight. No shortcut exists. |

### 4.5 CANDIDATE_CONTEXT_ONLY

| Attribute | Value |
|-----------|-------|
| **Definition** | Record provides context information only (benchmark_context, private_comparable_context, or excluded_non_peer role). The record is structurally complete for its context role but does not participate in peer comparison and will never receive a production peer_group_id assignment within this preflight. |
| **Entry conditions** | Record's asset_type or peer_role assignment restricts it to a context-only role: benchmark_context (ETFs/indices in company families), private_comparable_context (private companies), excluded_non_peer (unsupported assets correctly classified). |
| **Exit conditions** | Terminal within preflight. Context-only records do not transition to other states. |
| **Terminal behavior** | Terminal within preflight scope. Context-only records serve as reference material for peer group methodology but do not become peer members. |
| **Required fields** | All fields from CANDIDATE_DRAFT plus: peer_role ∈ {benchmark_context, private_comparable_context, excluded_non_peer}, peer_comparison_allowed = false |
| **Allowed next states** | None within preflight (terminal). |
| **Prohibited next states** | CANDIDATE_DRAFT (reversal), CANDIDATE_READY_FOR_REVIEW, CANDIDATE_BLOCKED, ACTIVE, APPROVED, PRODUCTION, VALIDATED, FINAL, ASSIGNED, TRADEABLE, TRADING_ENABLED |
| **Human/CTO review relevance** | Human/CTO may review context-only records to validate context role assignment. Review does not change terminal status within preflight. |
| **Production safety rule** | Context-only records carry peer_comparison_allowed = false. They provide ecosystem context only. No peer comparison or trading derivation permitted. |


---

## 5. Lifecycle Transition Matrix

### 5.1 Allowed Transitions

| # | From Status | To Status | Allowed | Condition | Required Evidence | Human/CTO Involvement | Production Safety Note |
|---|-------------|-----------|---------|-----------|-------------------|----------------------|----------------------|
| 1 | CANDIDATE_DRAFT | CANDIDATE_READY_FOR_REVIEW | YES | All CURRENT_METHODOLOGY fields populated; field_taxonomy_mapping_status = COMPLETE; zero boundary violations; zero drift violations; source_authority_status = SOURCE_AUTHORITY_PRESENT | Completed field taxonomy mapping; all source authority references present; boundary compliance confirmation | Not required for transition; human review occurs AFTER transition | Record remains production_authority: NONE; readiness ≠ production |
| 2 | CANDIDATE_DRAFT | CANDIDATE_BLOCKED | YES | At least one block state triggered (any of the 14 block states) | Block state identifier documented in blocked_reason; trigger condition documented | Not required for transition; may review blocked records | Blocked records cannot progress toward production |
| 3 | CANDIDATE_DRAFT | CANDIDATE_DEFERRED | YES | Methodology gap identified that requires PGMF extension beyond DEC-01 through DEC-10 | Documentation of evaluated PGMF decisions; explanation of methodology insufficiency | Recommended — human/CTO confirms deferral decision | Deferred records are terminal within preflight |
| 4 | CANDIDATE_DRAFT | CANDIDATE_CONTEXT_ONLY | YES | Record's asset_type/peer_role restricts to context role (benchmark_context, private_comparable_context, excluded_non_peer) | Context role assignment rationale documented; peer_comparison_allowed = false confirmed | Not required for transition | Context-only records provide reference only |
| 5 | CANDIDATE_BLOCKED | CANDIDATE_DRAFT | YES | Blocking condition fully resolved with documented remediation evidence | Resolution evidence: what was fixed, how it was fixed, confirmation that block state no longer applies | Required if block state involved source authority gap or boundary interpretation | Record re-enters validation cycle from DRAFT |

### 5.2 Prohibited Transitions

| # | From Status | To Status | Allowed | Reason | Production Safety Note |
|---|-------------|-----------|---------|--------|----------------------|
| 6 | CANDIDATE_READY_FOR_REVIEW | ACTIVE | PROHIBITED | Production state — not achievable within preflight | No automated promotion path exists |
| 7 | CANDIDATE_READY_FOR_REVIEW | APPROVED | PROHIBITED | Production state — requires separate production registry spec | Approval within preflight = readiness acknowledgment only |
| 8 | CANDIDATE_READY_FOR_REVIEW | PRODUCTION | PROHIBITED | Production state — requires separate production registry spec | No production authority exists in preflight |
| 9 | CANDIDATE_DRAFT | ACTIVE | PROHIBITED | Production state — no direct path from draft to production | Draft records are never production-eligible |
| 10 | CANDIDATE_DRAFT | APPROVED | PROHIBITED | Production state — approval requires READY_FOR_REVIEW first | Cannot skip validation |
| 11 | CANDIDATE_BLOCKED | CANDIDATE_READY_FOR_REVIEW | PROHIBITED | Must return to DRAFT first for re-validation | Cannot skip re-validation after remediation |
| 12 | CANDIDATE_BLOCKED | ACTIVE | PROHIBITED | Production state — blocked records cannot reach production | Blocking must be resolved first |
| 13 | CANDIDATE_DEFERRED | CANDIDATE_DRAFT | PROHIBITED (within preflight) | Terminal within preflight; requires future methodology extension | Deferral cannot be reversed without new methodology |
| 14 | CANDIDATE_DEFERRED | CANDIDATE_READY_FOR_REVIEW | PROHIBITED | Terminal within preflight | Cannot bypass methodology gap |
| 15 | CANDIDATE_DEFERRED | ACTIVE | PROHIBITED | Production state | Deferred records are never production-eligible in this preflight |
| 16 | CANDIDATE_CONTEXT_ONLY | CANDIDATE_DRAFT | PROHIBITED | Terminal within preflight | Context role is architectural, not remediable |
| 17 | CANDIDATE_CONTEXT_ONLY | CANDIDATE_READY_FOR_REVIEW | PROHIBITED | Terminal within preflight | Context records do not enter review pipeline |
| 18 | CANDIDATE_CONTEXT_ONLY | ACTIVE | PROHIBITED | Production state | Context-only records are never production peers |
| 19 | ANY candidate status | VALIDATED | PROHIBITED | Production state | Not achievable in preflight |
| 20 | ANY candidate status | FINAL | PROHIBITED | Production state | Not achievable in preflight |
| 21 | ANY candidate status | ASSIGNED | PROHIBITED | Production state | peer_role is preliminary only |
| 22 | ANY candidate status | TRADEABLE | PROHIBITED | Trading inference — violates R10 | No trading derivation from peer methodology |
| 23 | ANY candidate status | TRADING_ENABLED | PROHIBITED | Trading inference — violates R10 | No trading derivation from peer methodology |

### 5.3 State Transition Diagram

```
                    ┌─────────────────────────────────┐
                    │         CANDIDATE_DRAFT          │
                    │  (Initial state, non-terminal)   │
                    └──────┬──────┬──────┬──────┬─────┘
                           │      │      │      │
            All checks pass│      │      │      │Context role
                           │      │Block │      │assignment
                           ▼      │state │      ▼
          ┌────────────────────┐  │      │  ┌──────────────────────┐
          │CANDIDATE_READY_FOR │  │      │  │ CANDIDATE_CONTEXT_ONLY│
          │      REVIEW        │  │      │  │    (Terminal)         │
          │  (Terminal in       │  │      │  └──────────────────────┘
          │   preflight)       │  │      │
          └────────────────────┘  │      │Methodology
                                  │      │gap found
                                  ▼      ▼
                    ┌──────────────────┐  ┌──────────────────────┐
                    │CANDIDATE_BLOCKED │  │ CANDIDATE_DEFERRED   │
                    │  (Non-terminal)  │  │    (Terminal)         │
                    └────────┬─────────┘  └──────────────────────┘
                             │
                  Remediation│
                  complete   │
                             ▼
                    ┌─────────────────────────────────┐
                    │         CANDIDATE_DRAFT          │
                    │     (Re-enters validation)       │
                    └─────────────────────────────────┘

    ╔══════════════════════════════════════════════════════════════╗
    ║  PRODUCTION BOUNDARY — NO TRANSITION CROSSES THIS LINE     ║
    ║  ACTIVE, APPROVED, PRODUCTION, VALIDATED, FINAL,           ║
    ║  ASSIGNED, TRADEABLE, TRADING_ENABLED                      ║
    ║  → Requires separate production registry spec              ║
    ╚══════════════════════════════════════════════════════════════╝
```


---

## 6. Block State Registry — All 14 Block States

### 6.1 BLOCK_SOURCE_INSUFFICIENT

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_SOURCE_INSUFFICIENT |
| **Trigger condition** | A CURRENT_METHODOLOGY field cannot trace to any source in the PGMF source registry, OR the only available source is outside its designated authority domain (DOMAIN_SCOPE_VIOLATION) |
| **Related boundary area** | Source Authority Boundary (Task 4, Task 6 Section 12) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Identify and provide a valid source from the PGMF source registry within the correct authority domain. If no source exists, document the gap and route to Evidence Gap Register (Task 11). If a source extension is needed, obtain human/CTO approval with approver identity and approval date. |
| **Terminal or remediable** | Remediable — record returns to CANDIDATE_DRAFT after valid source is identified |
| **Required evidence** | Source gap documentation: missing field name, asset_type requiring it, authority domain responsible, sources searched, reason no valid source found |
| **Related requirement** | R4 (Source Authority Mapping) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/source_authority_mapping_preflight.md` |

### 6.2 BLOCK_IDENTITY_UNRESOLVED

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_IDENTITY_UNRESOLVED |
| **Trigger condition** | The asset's canonical_object_id cannot be confirmed through any verified institutional identifier (FIGI, ISIN, or equivalent). The record's identity cannot be established. |
| **Related boundary area** | Identity / Unsupported Asset Protection (Task 6 Section 5) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Resolve identity through verified institutional identifier. If identity cannot be resolved, record may be reclassified as unsupported_asset_class with IDENTITY_UNRESOLVED status. |
| **Terminal or remediable** | Remediable if identity can be resolved; may become CANDIDATE_DEFERRED if resolution requires future data source |
| **Required evidence** | Identity resolution attempt documentation: identifiers searched, databases consulted, reason for failure |
| **Related requirement** | R8 (Unsupported Asset Protection, criterion 4) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/candidate_record_schema_preflight.md` |

### 6.3 BLOCK_UNSUPPORTED_ASSET_CLASS

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_UNSUPPORTED_ASSET_CLASS |
| **Trigger condition** | Asset's object_type matches the unsupported asset class list (derivatives, options, warrants, certificates, leveraged products, structured products, crypto/tokenized, commodities, FX pairs, bonds/fixed-income, money-market, baskets, synthetic exposures) |
| **Related boundary area** | Unsupported Asset Protection Boundary (Task 6 Section 5) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED (default) or CANDIDATE_DEFERRED (if future methodology extension pathway identified) |
| **Required remediation** | Requires future methodology extension spec with human/CTO approval. No remediation possible within current PGMF v1 scope for unsupported asset classes. |
| **Terminal or remediable** | Not remediable within preflight — may transition to CANDIDATE_DEFERRED with human/CTO approval |
| **Required evidence** | Asset class identification documentation: object_type, why it matches unsupported list, PGMF Task 9 reference |
| **Related requirement** | R8 (Unsupported Asset Protection) |
| **Related artifact** | `.kiro/specs/peer-group-registry-methodology-framework/artifacts/unsupported_asset_class_handling_2026-06-08.md` |

### 6.4 BLOCK_ETF_COMPANY_FALLBACK

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_ETF_COMPANY_FALLBACK |
| **Trigger condition** | ETF/fund asset (asset_type ∈ {etf, fund}) assigned peer_role ∈ {core_peer, adjacent_peer} against a company asset, OR company asset (asset_type = company) assigned peer_role = etf_peer |
| **Related boundary area** | ETF/Fund Boundary (Task 6 Section 3, PGMF-DEC-05) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Correct peer_role assignment to respect ETF/company boundary. ETFs in company families → benchmark_context. ETFs in PGF-09 → etf_peer. Companies → never etf_peer. |
| **Terminal or remediable** | Remediable — correct the peer_role assignment and return to CANDIDATE_DRAFT |
| **Required evidence** | Violation documentation: violating asset, invalid peer_role, target asset, correct peer_role per PGMF-DEC-05 |
| **Related requirement** | R6 (ETF/Fund Boundary Preservation) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.5 BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED |
| **Trigger condition** | comparability_adjustment_required = true but comparability_note is null/empty (CROSS_REGION_COMPARABILITY_INCOMPLETE), OR any of the 9 required cross-region fields are missing (CROSS_REGION_FIELDS_INCOMPLETE) |
| **Related boundary area** | Cross-Region Comparability Boundary (Task 6 Section 4, PGMF-DEC-08) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Populate all required cross-region fields with valid values. Provide comparability_note documenting which adjustments are needed when comparability_adjustment_required = true. |
| **Terminal or remediable** | Remediable — populate missing fields and return to CANDIDATE_DRAFT |
| **Required evidence** | Cross-region gap documentation: which fields are missing, which accounting standard applies, which currencies are involved, what comparability adjustments are needed |
| **Related requirement** | R7 (Cross-Region Comparability) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.6 BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY |
| **Trigger condition** | Market data availability (price feeds, data vendor coverage, exchange connectivity) used as a criterion for peer_role assignment, Candidate_Status determination, or financial_comparability_gate_status decision |
| **Related boundary area** | Market Data Boundary (Task 6 Section 9, R9) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Remove market data dependency from methodology decision. Re-evaluate on methodology grounds only using PGMF source registry as authority. |
| **Terminal or remediable** | Remediable — remove market data inference, re-derive decision on methodology-only basis |
| **Required evidence** | Violation documentation: which decision referenced market data, what market data factor was used, correct methodology-only basis for the decision |
| **Related requirement** | R9 (Market Data Boundary) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.7 BLOCK_TRADING_ELIGIBILITY_INFERENCE

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_TRADING_ELIGIBILITY_INFERENCE |
| **Trigger condition** | Any trading governance field set to a value other than FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL, OR any output that derives, calculates, or stores tradability, execution eligibility, broker connectivity, order-routing authority, or trading readiness |
| **Related boundary area** | Trading Governance Boundary (Task 6 Section 10, R10) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Reset all trading governance fields to FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL. Remove any inference of tradability or execution eligibility. |
| **Terminal or remediable** | Remediable — reset fields to safe values and return to CANDIDATE_DRAFT |
| **Required evidence** | Violation documentation: which trading governance field was set, what invalid value was assigned, confirmation of reset to FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL |
| **Related requirement** | R10 (Trading Boundary) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.8 BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT |
| **Trigger condition** | Private company (asset_type = private_company) assigned peer_role ∈ {core_peer, adjacent_peer, etf_peer} — only private_comparable_context is permitted |
| **Related boundary area** | Private Company Handling (Task 6 Section 6, PGMF-DEC-07) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Change peer_role to private_comparable_context. Set valuation_peer_allowed = false. Set comparison_mode_allowed = ecosystem_context_only. |
| **Terminal or remediable** | Remediable — correct peer_role to private_comparable_context and return to CANDIDATE_DRAFT |
| **Required evidence** | Violation documentation: private company name, invalid peer_role assigned, correct role per PGMF-DEC-07 |
| **Related requirement** | R8 (Unsupported Asset Protection) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.9 BLOCK_DERIVATIVE_AS_PEER_MEMBER

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_DERIVATIVE_AS_PEER_MEMBER |
| **Trigger condition** | Derivative, option, warrant, certificate, leveraged product, or structured product assigned peer_role other than excluded_non_peer |
| **Related boundary area** | Derivative and Structured Product Handling (Task 6 Section 7) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Reclassify as excluded_non_peer per PGMF Task 9. Set unsupported_status = UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION. |
| **Terminal or remediable** | Remediable (correct classification) — record may then transition to CANDIDATE_CONTEXT_ONLY with peer_role = excluded_non_peer |
| **Required evidence** | Violation documentation: instrument type, invalid peer_role, correct classification per PGMF Task 9 Section 6 |
| **Related requirement** | R8 (Unsupported Asset Protection) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.10 BLOCK_PEER_GROUP_ID_CREATION

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_PEER_GROUP_ID_CREATION |
| **Trigger condition** | Any attempt to mint or assign a canonical peer_group_id during preflight. Any peer_group_id value other than PREFLIGHT_PLACEHOLDER_NOT_CANONICAL. |
| **Related boundary area** | peer_group_id Boundary (Task 6 Section 14) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Remove canonical ID value. Restore peer_group_id = PREFLIGHT_PLACEHOLDER_NOT_CANONICAL. Restore peer_group_id_status = NOT_CREATED. |
| **Terminal or remediable** | Remediable — restore placeholder value and return to CANDIDATE_DRAFT |
| **Required evidence** | Violation documentation: what canonical ID was attempted, why it was invalid, confirmation of placeholder restoration |
| **Related requirement** | R3 (Candidate-Only Record Status), R5 (Field Taxonomy Mapping) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/field_taxonomy_mapping_preflight.md` |

### 6.11 BLOCK_REGISTRY_CREATION

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_REGISTRY_CREATION |
| **Trigger condition** | Any attempt to create peer_group_registry.yaml or production registry file, OR any file whose name contains "registry" without candidate_ prefix or _preflight suffix |
| **Related boundary area** | Registry Boundary (Task 6 Section 15) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Remove forbidden artifact. Restrict all output to candidate_ prefix or _preflight suffix naming convention. |
| **Terminal or remediable** | Remediable — remove forbidden artifact and rename correctly |
| **Required evidence** | Violation documentation: forbidden file name, output restriction rule violated, correct naming convention |
| **Related requirement** | R3 (Candidate-Only Record Status), R13 (Output Restrictions) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.12 BLOCK_SAI_CONTRACT_SHAPE_VIOLATION

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION |
| **Trigger condition** | Candidate record output shape omits any of the 17 SAI output contract fields, OR assigns a production-authority value to any SAI field |
| **Related boundary area** | SAI Boundary (Task 6 Section 11, R11) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Add missing SAI output contract fields with PREFLIGHT_NOT_CANONICAL values. Remove any production-authority values from SAI fields. |
| **Terminal or remediable** | Remediable — add missing fields with correct placeholder values and return to CANDIDATE_DRAFT |
| **Required evidence** | Violation documentation: which SAI field(s) were missing or had production values, correct PREFLIGHT_NOT_CANONICAL values applied |
| **Related requirement** | R11 (SAI Compatibility Boundary) |
| **Related artifact** | `.kiro/specs/peer-group-registry-methodology-framework/artifacts/sai_compatibility_verification_2026-06-08.md` |

### 6.13 BLOCK_OUTPUT_RESTRICTION_VIOLATION

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_OUTPUT_RESTRICTION_VIOLATION |
| **Trigger condition** | Output artifact violates naming conventions (missing candidate_ prefix or _preflight suffix), contains forbidden field values (ACTIVE, APPROVED, production_authority other than NONE), or implies final peer assignments |
| **Related boundary area** | Output Restriction / Registry Boundary (Task 6 Sections 15–16) |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Rename artifact with candidate_ prefix or _preflight suffix. Remove forbidden values. Remove any implication of final peer assignment. |
| **Terminal or remediable** | Remediable — correct naming and values, return to CANDIDATE_DRAFT |
| **Required evidence** | Violation documentation: artifact name, forbidden values found, naming convention rule violated, corrective action taken |
| **Related requirement** | R13 (Output Restrictions), R15 (Drift Prevention) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |

### 6.14 BLOCK_DRIFT_VIOLATION

| Attribute | Value |
|-----------|-------|
| **Block state** | BLOCK_DRIFT_VIOLATION |
| **Trigger condition** | Any of the 8 drift categories detected: registry drift, ID drift, peer assignment drift, source authority drift, market data drift, SAI drift, runtime drift, or trading drift |
| **Related boundary area** | All boundary areas — drift is a cross-cutting concern |
| **Candidate_Status outcome** | CANDIDATE_BLOCKED |
| **Required remediation** | Halt processing. Document the drift violation category, affected record, drift evidence. Resolve the drift condition (restore correct values, remove forbidden content). Return to CANDIDATE_DRAFT after drift is eliminated. |
| **Terminal or remediable** | Remediable — resolve drift condition and return to CANDIDATE_DRAFT |
| **Required evidence** | Drift violation documentation: drift category, what drifted, expected safe value, actual value found, remediation action, confirmation drift is eliminated |
| **Related requirement** | R15 (Drift Prevention) |
| **Related artifact** | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/boundary_rules_preflight.md` |


---

## 7. Block-State-to-Candidate_Status Mapping Table

| # | Block State | Default Candidate_Status | Allowed Alternative | Remediation Path | Evidence Gap Register Routing | Human/CTO Decision Requirement |
|---|-------------|--------------------------|--------------------|--------------------|-------------------------------|-------------------------------|
| 1 | BLOCK_SOURCE_INSUFFICIENT | CANDIDATE_BLOCKED | CANDIDATE_DEFERRED (if source extension requires future methodology) | Identify valid source → document → return to CANDIDATE_DRAFT | YES — routes as SOURCE_EVIDENCE_MISSING | Required if source extension needed |
| 2 | BLOCK_IDENTITY_UNRESOLVED | CANDIDATE_BLOCKED | CANDIDATE_DEFERRED (if identity resolution requires future data source) | Resolve identity via FIGI/ISIN → document → return to CANDIDATE_DRAFT | YES — routes as IDENTITY_UNRESOLVED | Required if reclassification to DEFERRED |
| 3 | BLOCK_UNSUPPORTED_ASSET_CLASS | CANDIDATE_BLOCKED | CANDIDATE_DEFERRED (future methodology extension needed) | Requires future methodology extension spec → human/CTO approval | YES — routes as UNSUPPORTED_ASSET_CLASS | Required — human/CTO must approve deferral or confirm block |
| 4 | BLOCK_ETF_COMPANY_FALLBACK | CANDIDATE_BLOCKED | None — must be remediated | Correct peer_role → return to CANDIDATE_DRAFT | YES — routes as ETF_COMPANY_BOUNDARY_ISSUE | Not required — remediation is mechanical |
| 5 | BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED | CANDIDATE_BLOCKED | None — must be remediated | Populate cross-region fields → return to CANDIDATE_DRAFT | YES — routes as CROSS_REGION_COMPARABILITY_INCOMPLETE or CROSS_REGION_FIELDS_INCOMPLETE | Not required — remediation is data completion |
| 6 | BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY | CANDIDATE_BLOCKED | None — must be remediated | Remove market data dependency → re-derive on methodology basis → return to CANDIDATE_DRAFT | NO — this is a process violation, not an evidence gap | Not required — remediation is methodology correction |
| 7 | BLOCK_TRADING_ELIGIBILITY_INFERENCE | CANDIDATE_BLOCKED | None — must be remediated | Reset trading fields to FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL → return to CANDIDATE_DRAFT | NO — this is a boundary violation, not an evidence gap | Not required — remediation is mechanical reset |
| 8 | BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT | CANDIDATE_BLOCKED | CANDIDATE_CONTEXT_ONLY (after correct peer_role = private_comparable_context) | Change peer_role → set valuation_peer_allowed = false → return to CANDIDATE_DRAFT → may resolve to CONTEXT_ONLY | NO — correct classification resolves it | Not required — remediation is mechanical |
| 9 | BLOCK_DERIVATIVE_AS_PEER_MEMBER | CANDIDATE_BLOCKED | CANDIDATE_CONTEXT_ONLY (after peer_role = excluded_non_peer) | Reclassify as excluded_non_peer → return to CANDIDATE_DRAFT → may resolve to CONTEXT_ONLY | NO — correct classification resolves it | Not required — remediation is mechanical |
| 10 | BLOCK_PEER_GROUP_ID_CREATION | CANDIDATE_BLOCKED | None — must be remediated | Restore PREFLIGHT_PLACEHOLDER_NOT_CANONICAL → return to CANDIDATE_DRAFT | NO — this is a process violation | Not required — remediation is mechanical |
| 11 | BLOCK_REGISTRY_CREATION | CANDIDATE_BLOCKED | None — must be remediated | Remove forbidden artifact → rename with correct convention → return to CANDIDATE_DRAFT | YES — routes as OUTPUT_RESTRICTION_VIOLATION | Required if systemic pattern detected |
| 12 | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | CANDIDATE_BLOCKED | None — must be remediated | Add missing SAI fields with PREFLIGHT_NOT_CANONICAL → return to CANDIDATE_DRAFT | YES — routes as SAI_CONTRACT_SHAPE_VIOLATION | Not required — remediation is structural completion |
| 13 | BLOCK_OUTPUT_RESTRICTION_VIOLATION | CANDIDATE_BLOCKED | None — must be remediated | Rename artifact → remove forbidden values → return to CANDIDATE_DRAFT | YES — routes as OUTPUT_RESTRICTION_VIOLATION | Required if systemic pattern detected |
| 14 | BLOCK_DRIFT_VIOLATION | CANDIDATE_BLOCKED | None — must be remediated | Resolve drift → restore correct values → return to CANDIDATE_DRAFT | YES — routes as DRIFT_VIOLATION | Required if drift indicates architectural issue |

### 7.1 Absolute Rule

No block state may result in any of the following Candidate_Status values:
- ACTIVE
- APPROVED
- PRODUCTION
- VALIDATED
- FINAL
- ASSIGNED
- TRADEABLE
- TRADING_ENABLED

Block states always resolve to one of: CANDIDATE_BLOCKED (default), CANDIDATE_DEFERRED (with human/CTO approval), or CANDIDATE_CONTEXT_ONLY (for correct context-role classification after remediation).


---

## 8. Remediation Rules

### 8.1 Remediation Pattern

All block state remediation follows a consistent pattern:

```
1. IDENTIFY    → Detect block state and document the specific trigger condition
2. DOCUMENT    → Record the evidence gap (blocked_reason, missing field/value, affected record)
3. SAFE VALUE  → Document the required safe value that would resolve the block
4. ROUTE       → Route to Evidence Gap Register (Task 11) for tracking
5. REMEDIATE   → Apply correction (or request human/CTO decision if required)
6. RETURN      → Return record to CANDIDATE_DRAFT state
7. RE-RUN      → Re-run all validation checks from CANDIDATE_DRAFT
```

### 8.2 Remediation Constraints

| Constraint | Rule |
|------------|------|
| No automated remediation | All remediation requires documented human action or explicit rule application |
| No automatic transition to READY_FOR_REVIEW | After remediation, record returns to CANDIDATE_DRAFT and must pass all checks again |
| No automatic production elevation | Even after successful remediation, no path to production exists within preflight |
| Evidence required | Every remediation must produce documented evidence of what was changed and why |
| Source authority required | If remediation involves a CURRENT_METHODOLOGY field, source authority reference must be provided |
| Boundary re-check required | After remediation, all boundary rules (ETF, market data, trading, SAI, etc.) must be re-verified |

### 8.3 Remediation by Block State Category

#### Hard Violations (Must Be Remediated)

These block states result from clear rule violations that can be mechanically corrected:

| Block State | Remediation Type | Complexity |
|-------------|-----------------|------------|
| BLOCK_ETF_COMPANY_FALLBACK | Correct peer_role assignment | Low — mechanical correction |
| BLOCK_TRADING_ELIGIBILITY_INFERENCE | Reset fields to safe values | Low — mechanical reset |
| BLOCK_PEER_GROUP_ID_CREATION | Restore placeholder value | Low — mechanical correction |
| BLOCK_REGISTRY_CREATION | Remove/rename forbidden artifact | Low — mechanical correction |
| BLOCK_OUTPUT_RESTRICTION_VIOLATION | Rename artifact, remove forbidden values | Low — mechanical correction |
| BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY | Remove data dependency, re-derive decision | Medium — requires methodology re-evaluation |
| BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | Add missing fields with placeholder values | Low — structural completion |

#### Evidence Gaps (Require Research/Documentation)

These block states result from missing information that must be located or documented:

| Block State | Remediation Type | Complexity |
|-------------|-----------------|------------|
| BLOCK_SOURCE_INSUFFICIENT | Identify valid source in PGMF registry | Medium — requires source research |
| BLOCK_IDENTITY_UNRESOLVED | Resolve institutional identifier | Medium — requires identity research |
| BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED | Complete cross-region field documentation | Medium — requires cross-region analysis |
| BLOCK_DRIFT_VIOLATION | Identify and resolve drift source | Variable — depends on drift category |

#### Future Methodology Required (May Become DEFERRED)

These block states may not be resolvable within the current PGMF v1 scope:

| Block State | Remediation Type | Complexity |
|-------------|-----------------|------------|
| BLOCK_UNSUPPORTED_ASSET_CLASS | Future methodology extension spec | High — requires new spec and human/CTO approval |
| BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT | Correct to context role OR defer | Low (if context) / High (if methodology extension needed) |
| BLOCK_DERIVATIVE_AS_PEER_MEMBER | Correct to excluded_non_peer | Low — mechanical correction |

### 8.4 Remediation Evidence Structure

Every remediation action must produce the following evidence record:

| Field | Content |
|-------|---------|
| `remediation_id` | Unique identifier for the remediation action |
| `affected_record` | candidate_record_id of the affected record |
| `block_state_resolved` | The specific block state that was resolved |
| `original_value` | What the field/artifact contained before remediation |
| `corrected_value` | What the field/artifact contains after remediation |
| `remediation_rationale` | Why this correction is valid |
| `source_authority_reference` | Source reference (if CURRENT_METHODOLOGY field) |
| `human_CTO_approval` | Yes/No — whether human/CTO was involved |
| `remediation_date` | Date of remediation |
| `re_validation_status` | Outcome of re-running checks from CANDIDATE_DRAFT |

---

## 9. Human/CTO Review Boundary

### 9.1 What Human/CTO Review CAN Do Within Preflight

| Permitted Action | Scope |
|-----------------|-------|
| Mark candidate readiness for review | Acknowledge CANDIDATE_READY_FOR_REVIEW status |
| Approve source extension requests | Allow new source not in PGMF registry (with documented justification) |
| Authorize deferral decisions | Confirm that a blocked record should become CANDIDATE_DEFERRED |
| Review evidence gaps | Assess completeness of Evidence Gap Register |
| Validate context-only classifications | Confirm context role assignments are correct |
| Prioritize remediation work | Guide which blocked records to remediate first |

### 9.2 What Human/CTO Review CANNOT Do Within Preflight

| Prohibited Action | Reason |
|-------------------|--------|
| Activate production registry | Production registry requires a separate spec |
| Create canonical peer_group_id | ID creation is prohibited in preflight |
| Assign final peers inside preflight | peer_role is preliminary only |
| Convert candidates to production entries | No automated or manual promotion path within preflight |
| Override trading boundary | Trading inference is absolutely prohibited |
| Override market data boundary | Market data as methodology proxy is absolutely prohibited |
| Mutate SAI artifacts | SAI remains stable throughout preflight |
| Skip verification gate (VG-PGRC-PREFLIGHT-1) | Gate must be explicitly executed |

### 9.3 Future Production Registry Requirement

Human/CTO approval within this preflight addresses candidate readiness only. For production registry creation:

1. This preflight must complete (all tasks, VG-PGRC-PREFLIGHT-1 PASS)
2. A separate production registry creation spec must be authored
3. That spec must receive independent human/CTO approval
4. Only that future spec may create canonical peer_group_id values
5. Only that future spec may create production registry files
6. Only that future spec may transition records to production states

---

## 10. Evidence Gap Register Routing

### 10.1 Routing Rule

Blocked, deferred, and context-only results from Task 10 (candidate record drafts) flow into Task 11 (Evidence Gap Register). The following gap types are routed:

| # | Gap Type | Source Block State(s) | Task 11 Column |
|---|----------|----------------------|----------------|
| 1 | SOURCE_EVIDENCE_MISSING | BLOCK_SOURCE_INSUFFICIENT | gap_type = SOURCE_EVIDENCE_MISSING |
| 2 | DOMAIN_SCOPE_VIOLATION | BLOCK_SOURCE_INSUFFICIENT | gap_type = DOMAIN_SCOPE_VIOLATION |
| 3 | IDENTITY_UNRESOLVED | BLOCK_IDENTITY_UNRESOLVED | gap_type = IDENTITY_UNRESOLVED |
| 4 | CROSS_REGION_COMPARABILITY_INCOMPLETE | BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED | gap_type = CROSS_REGION_COMPARABILITY_INCOMPLETE |
| 5 | CROSS_REGION_FIELDS_INCOMPLETE | BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED | gap_type = CROSS_REGION_FIELDS_INCOMPLETE |
| 6 | UNSUPPORTED_ASSET_CLASS | BLOCK_UNSUPPORTED_ASSET_CLASS | gap_type = UNSUPPORTED_ASSET_CLASS |
| 7 | ETF_COMPANY_BOUNDARY_ISSUE | BLOCK_ETF_COMPANY_FALLBACK | gap_type = ETF_COMPANY_BOUNDARY_ISSUE |
| 8 | SAI_CONTRACT_SHAPE_VIOLATION | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | gap_type = SAI_CONTRACT_SHAPE_VIOLATION |
| 9 | OUTPUT_RESTRICTION_VIOLATION | BLOCK_OUTPUT_RESTRICTION_VIOLATION, BLOCK_REGISTRY_CREATION | gap_type = OUTPUT_RESTRICTION_VIOLATION |
| 10 | DRIFT_VIOLATION | BLOCK_DRIFT_VIOLATION | gap_type = DRIFT_VIOLATION |

### 10.2 Routing Structure

Each routed gap carries:

| Field | Content |
|-------|---------|
| gap_id | Unique identifier (GAP-PGF-XX-NNN format) |
| affected_family | PGF-01 through PGF-09 |
| affected_candidate_record | candidate_record_id |
| gap_type | From the gap type list above |
| missing_field_or_evidence | Specific field or evidence that is missing |
| blocking_status | CANDIDATE_BLOCKED / CANDIDATE_DEFERRED / CANDIDATE_CONTEXT_ONLY |
| required_remediation | What must be done to resolve |
| source_authority_domain | Which authority domain is responsible |
| human_CTO_review_note | Whether human/CTO decision is needed |

### 10.3 Non-Routed Block States

The following block states represent process violations (not evidence gaps) and are resolved through mechanical correction rather than Evidence Gap Register routing:

- BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY — process violation, correct immediately
- BLOCK_TRADING_ELIGIBILITY_INFERENCE — boundary violation, reset fields immediately
- BLOCK_PEER_GROUP_ID_CREATION — process violation, restore placeholder immediately
- BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT — classification correction (unless source gap exists)
- BLOCK_DERIVATIVE_AS_PEER_MEMBER — classification correction

---

## 11. Relationship to Task 10

### 11.1 How Task 10 Uses This Specification

Task 10 (Create Candidate Record Draft Artifacts for PGF-01 through PGF-09) SHALL use this lifecycle and block-state specification as follows:

| Task 10 Activity | This Specification Governs |
|-----------------|---------------------------|
| Assigning initial Candidate_Status | Must be CANDIDATE_DRAFT (Section 4.1) |
| Detecting blocking conditions | Must use the 14 block states defined in Section 6 |
| Setting blocked_reason | Must use exact block state identifiers from Section 6 |
| Determining terminal states | Must follow terminal/non-terminal rules from Section 4 |
| Assigning CANDIDATE_CONTEXT_ONLY | Must follow entry conditions from Section 4.5 |
| Assigning CANDIDATE_DEFERRED | Must follow entry conditions from Section 4.4 |
| Documenting transitions | Must follow transition matrix from Section 5 |

### 11.2 What Task 7 Does NOT Do

Task 7 (this artifact) does NOT:
- Create any candidate records
- Transition any records between states
- Execute any block state detection
- Apply any remediation
- Produce any Evidence Gap Register entries
- Create any PGF family artifacts

---

## 12. Relationship to Task 11

### 12.1 How Task 11 Uses This Specification

Task 11 (Evidence Gap Register) SHALL use this lifecycle and block-state specification as follows:

| Task 11 Activity | This Specification Governs |
|-----------------|---------------------------|
| Identifying gap types | Uses the gap types defined in Section 10.1 |
| Routing blocked records | Uses the routing structure from Section 10.2 |
| Documenting remediation expectations | References remediation rules from Section 8 |
| Classifying gap severity | References terminal vs. remediable from Section 6 |
| Human/CTO review requirements | References Section 9 for review scope |

### 12.2 Flow Direction

```
Task 7 (THIS ARTIFACT) → defines rules
    ↓
Task 10 (Candidate Records) → applies rules, produces blocked/deferred/context-only records
    ↓
Task 11 (Evidence Gap Register) → documents unresolved blockers, deferred cases, context limitations
```

Task 7 is upstream of both Task 10 and Task 11. It provides the rule model that Task 10 applies and Task 11 documents gaps from.


---

## 13. Prohibited Outputs

This artifact explicitly does NOT produce and CANNOT produce:

| # | Prohibited Output | Reason |
|---|-------------------|--------|
| 1 | Candidate records for PGF-01 through PGF-09 | Record creation is Task 10 scope |
| 2 | PGF candidate artifacts | Artifact creation is Task 10 scope |
| 3 | peer_group_registry.yaml | Production registry — absolutely prohibited |
| 4 | Production registry files | No production content in preflight |
| 5 | Canonical peer_group_id values | ID creation prohibited in preflight |
| 6 | Final peer assignments | peer_role is preliminary only |
| 7 | Lifecycle transitions executed | This is a rule model, not an execution engine |
| 8 | SAI mutations | SAI remains stable |
| 9 | Runtime code | No executable implementations |
| 10 | Validation code | No validation implementations |
| 11 | Market data integrations | Market data not populated in preflight |
| 12 | Trading or execution outputs | Trading boundary is absolute |
| 13 | Evidence Gap Register entries | Evidence gaps are Task 11 scope (based on Task 10 results) |

---

## 14. Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | All 5 lifecycle states defined with transition rules | SATISFIED | Section 4 defines CANDIDATE_DRAFT, CANDIDATE_READY_FOR_REVIEW, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY with full attribute tables |
| 2 | Prohibited states explicitly listed | SATISFIED | Section 3.2 lists all 8 prohibited states with reasons |
| 3 | Transition matrix included (allowed and prohibited) | SATISFIED | Section 5 provides complete transition matrix with 5 allowed and 18 prohibited transitions |
| 4 | All 14 block states documented | SATISFIED | Section 6 defines all 14 block states with trigger, response, status outcome, and remediation |
| 5 | Block-to-status mapping included | SATISFIED | Section 7 maps all 14 block states to Candidate_Status with alternatives and remediation paths |
| 6 | Remediation rules documented | SATISFIED | Section 8 defines remediation pattern, constraints, categories, and evidence structure |
| 7 | Human/CTO boundary documented | SATISFIED | Section 9 defines permitted and prohibited actions for human/CTO review |
| 8 | Task 10 relationship documented | SATISFIED | Section 11 defines how Task 10 uses this specification |
| 9 | Task 11 relationship documented | SATISFIED | Section 12 defines how Task 11 uses this specification |
| 10 | Evidence Gap Register routing documented | SATISFIED | Section 10 defines routing rules and gap types |
| 11 | No production lifecycle states appear | SATISFIED | Sections 3.2, 5.2, 7.1 explicitly prohibit all production states |
| 12 | production_authority: NONE present | SATISFIED | Section 1 metadata declares production_authority: NONE |
| 13 | Final status marker present | SATISFIED | Section 16 contains CANDIDATE_LIFECYCLE_BLOCK_STATES_PREFLIGHT_COMPLETE |

---

## 15. Hard Boundary Confirmation

| # | Boundary | Status |
|---|----------|--------|
| 1 | No candidate records created | CONFIRMED — this is a rule model only |
| 2 | No PGF candidate artifacts created | CONFIRMED — artifact creation is Task 10 |
| 3 | No registry created | CONFIRMED — no peer_group_registry.yaml or production files |
| 4 | No peers assigned | CONFIRMED — peer_role is preliminary, defined as rule only |
| 5 | No peer_group_id values created | CONFIRMED — only PREFLIGHT_PLACEHOLDER_NOT_CANONICAL permitted |
| 6 | No lifecycle transitions executed | CONFIRMED — transitions are defined, not executed |
| 7 | No SAI mutation | CONFIRMED — SAI remains stable |
| 8 | No runtime code | CONFIRMED — documentation-only artifact |
| 9 | No validation code | CONFIRMED — no executable implementations |
| 10 | No market data | CONFIRMED — market data boundary absolute |
| 11 | No trading or execution | CONFIRMED — trading boundary absolute |
| 12 | Task 8 not started | CONFIRMED — only Task 7 was executed |

---

## 16. Final Status Marker

```
CANDIDATE_LIFECYCLE_BLOCK_STATES_PREFLIGHT_COMPLETE
```

---

*End of candidate lifecycle and block state specification.*
