# Candidate Record Draft Schema Specification

> **Peer Group Registry Creation Preflight — Task 3: Candidate Record Schema**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> report_type: Candidate Schema Report
> production_authority: NONE | preliminary: true | status: DRAFT_SCHEMA_ONLY

---

## Document Boundary

This artifact defines the non-production candidate record schema only. It does not instantiate candidate records, does not assign peers, does not create canonical peer_group_id values, does not create registry content, and does not activate production use.

---

## Schema Purpose

The schema provides the controlled shape for future candidate draft artifacts (Task 10). Candidate records are:

- Non-production preflight documentation objects
- Unable to satisfy production SAI registry requirements
- Unable to become production registry entries inside this preflight
- Subject to human/CTO review before any future production registry spec

---

## Candidate Record Field Table

| # | Field | Type | Required | Default Value | Allowed Values / Pattern | Source Authority Requirement | Production Safety Rule | PGMF / SAI Reference |
|---|-------|------|----------|---------------|--------------------------|------------------------------|------------------------|---------------------|
| 1 | `candidate_record_id` | string | Required | Generated during task execution | UUID or preflight-scoped identifier | N/A — generated | Must be non-production; no canonical registry ID | — |
| 2 | `candidate_record_id_status` | enum | Required | PREFLIGHT_NON_PRODUCTION | PREFLIGHT_NON_PRODUCTION | N/A | Must always be PREFLIGHT_NON_PRODUCTION | — |
| 3 | `production_authority` | enum | Required | NONE | NONE | N/A | Must always be NONE in preflight | — |
| 4 | `preliminary` | boolean | Required | true | true | N/A | Must always be true in preflight | — |
| 5 | `Candidate_Status` | enum | Required | CANDIDATE_DRAFT | See Allowed Status Values section | N/A | No ACTIVE/APPROVED/PRODUCTION states | R3 |
| 6 | `family_id` | string | Required | — | PGF-01 through PGF-09 | Scope preflight (sole family authority) | Must match scope preflight families only | R2 |
| 7 | `family_name` | string | Required | — | Human-readable family name from scope preflight | Scope preflight | Must match scope preflight naming | R2 |
| 8 | `asset_name` | string | Required | — | Human-readable asset name | Scope preflight (ticker source) | No invented names | R2 |
| 9 | `asset_type` | enum | Required | — | company / etf / fund / index / private_company / unsupported_asset_class | PGMF-DEC-04 (identity model) | Determines field applicability | PGMF-DEC-04 |
| 10 | `object_type` | enum | Required | — | company / etf / fund / index / private_company / unsupported_asset_class | PGMF-DEC-04 | Mirrors asset_type for PGMF field applicability | PGMF-DEC-04 |
| 11 | `legal_entity_name` | string | Nullable | — | Legal entity or fund name | REQUIRED_IF_AVAILABLE per PGMF | Gap must be documented if missing | PGMF-DEC-04 |
| 12 | `instrument_type` | enum | Required | — | equity / etf / fund / adr / gdr / index / other | PGMF-DEC-04 | Must match asset_type constraints | PGMF-DEC-04 |
| 13 | `ticker_candidates` | list[string] | Nullable | — | Known ticker symbols from scope preflight | Scope preflight | Not stable primary keys; for reference only | PGMF-DEC-04 |
| 14 | `ISIN_candidates` | list[string] | Nullable | — | ISO 6166 format | REQUIRED_IF_AVAILABLE per PGMF-DEC-04 | Gap documented if unavailable | PGMF-DEC-04 |
| 15 | `exchange_candidates` | list[string] | Nullable | — | ISO 10383 MIC codes | REQUIRED_IF_LISTED per PGMF-DEC-04 | Gap documented if unavailable | PGMF-DEC-04 |
| 16 | `region` | string | Required | — | Geographic region identifier | Scope preflight / PGMF | Required for cross-region handling | PGMF-DEC-08 |
| 17 | `domicile` | string | Required (company/etf/fund) | — | ISO 3166-1 alpha-2 | REQUIRED per PGMF-DEC-04 (company) | NOT_APPLICABLE for index/unsupported | PGMF-DEC-04 |
| 18 | `reporting_currency` | string | Required (company) | — | ISO 4217 | REQUIRED per PGMF-DEC-04 (company) | Required for cross-region comparability | PGMF-DEC-08 |
| 19 | `trading_currency` | string | Nullable | — | ISO 4217 | REQUIRED_IF_LISTED per PGMF-DEC-04 | Required for cross-region comparability | PGMF-DEC-08 |
| 20 | `accounting_standard` | enum | Required (company) | — | GAAP / IFRS / other | REQUIRED per PGMF-DEC-08 | Required for comparability checks | PGMF-DEC-08 |
| 21 | `fiscal_year_end` | string | Required (company) | — | Three-letter month (e.g., DEC) | REQUIRED per PGMF-DEC-04 (company) | Required for cross-region alignment | PGMF-DEC-08 |
| 22 | `listing_variant_type` | enum | Nullable | — | primary / ADR / GDR / secondary | REQUIRED_IF_LISTED per PGMF-DEC-04 | Required for multi-venue assets | PGMF-DEC-04 |
| 23 | `source_authority_status` | enum | Required | — | See Source Authority section | Every CURRENT_METHODOLOGY field | Missing evidence must not be silently normalized | R4 |
| 24 | `source_authority_references` | list[object] | Required | — | `[{source_id, authority_domain, tier_level, field_name}]` | PGMF source registry | Must trace to approved sources only | R4 |
| 25 | `methodology_decision_references` | list[string] | Required | — | PGMF-DEC-01 through PGMF-DEC-10 | PGMF requirements/design | Links record to governing decisions | R1 |
| 26 | `field_taxonomy_mapping_status` | enum | Required | — | COMPLETE / INCOMPLETE / BLOCKED | PGMF field taxonomy | Determines readiness for review | R5 |
| 27 | `peer_role` | enum | Nullable | — | core_peer / adjacent_peer / benchmark_context / etf_peer / excluded_non_peer / private_comparable_context | PGMF-DEC-03 (peer role taxonomy) | PRELIMINARY ONLY — not final assignment | PGMF-DEC-03 |
| 28 | `peer_group_id` | string | Required | PREFLIGHT_PLACEHOLDER_NOT_CANONICAL | PREFLIGHT_PLACEHOLDER_NOT_CANONICAL | N/A | Must NEVER be canonical; any other value triggers BLOCK_PEER_GROUP_ID_CREATION | R5, R15 |
| 29 | `peer_group_id_status` | enum | Required | NOT_CREATED | NOT_CREATED | N/A | Must always be NOT_CREATED in preflight | R5, R15 |
| 30 | `peer_comparison_allowed` | boolean | Required | false | false | N/A | Must be false until production registry exists | R11, SAI |
| 31 | `blocked_reason` | string | Nullable | null | Block state identifier or null | N/A | Populated when Candidate_Status = CANDIDATE_BLOCKED | R15 |
| 32 | `unsupported_status` | string | Nullable | null | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION / null | PGMF Section 7 | Populated for unsupported assets | R8 |
| 33 | `comparability_adjustment_required` | boolean | Nullable | — | true / false | PGMF-DEC-08 | Required for cross-region records | PGMF-DEC-08 |
| 34 | `comparability_note` | string | Nullable | — | Free text | Required when comparability_adjustment_required = true | Empty note + required flag = CANDIDATE_BLOCKED | PGMF-DEC-08 |
| 35 | `market_data_fields_status` | enum | Required | NOT_POPULATED_IN_PREFLIGHT | NOT_POPULATED_IN_PREFLIGHT | N/A | Must not affect peer_role or Candidate_Status | R9 |
| 36 | `trading_governance_fields_status` | enum | Required | FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL | FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL | N/A | Must not imply tradability or execution eligibility | R10 |
| 37 | `SAI_contract_status` | enum | Required | PREFLIGHT_NOT_CANONICAL | PREFLIGHT_NOT_CANONICAL | N/A | SAI cannot consume as production | R11 |
| 38 | `human_review_status` | enum | Required | NOT_REVIEWED | NOT_REVIEWED / REVIEW_REQUESTED / REVIEWED | N/A | Tracks human review state | R12 |
| 39 | `CTO_approval_status` | enum | Required | NOT_APPROVED | NOT_APPROVED / APPROVAL_REQUESTED / CONDITIONAL / DENIED | N/A | Tracks CTO approval state | R12 |
| 40 | `notes` | string | Nullable | null | Free text | N/A | For human reviewers | — |

---

## Candidate_Status Allowed Values

**Exhaustive permitted set** (no other values allowed):

| Status | Description | Terminal? |
|--------|-------------|----------|
| `CANDIDATE_DRAFT` | Initial state; record created but not yet fully validated | No |
| `CANDIDATE_READY_FOR_REVIEW` | Record passes all checks; awaits human/CTO review | No (within preflight) |
| `CANDIDATE_BLOCKED` | Blocking condition prevents progress | No (may return to DRAFT after remediation) |
| `CANDIDATE_DEFERRED` | Requires future methodology extension | Yes (within preflight) |
| `CANDIDATE_CONTEXT_ONLY` | Context role only (private_comparable_context or benchmark_context) | Yes (within preflight) |

**Explicitly prohibited status values**:
- ACTIVE
- APPROVED
- PRODUCTION
- VALIDATED
- FINAL
- ASSIGNED
- TRADEABLE
- TRADING_ENABLED

**Lifecycle boundary**: This schema defines allowed lifecycle values only. It does not transition any record state. No automated promotion path exists from candidate to production.

---

## peer_group_id Boundary

**Rule**: No canonical peer_group_id value may be created in this preflight.

Every candidate record must use:
- `peer_group_id`: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
- `peer_group_id_status`: NOT_CREATED

Any other peer_group_id value must trigger: **BLOCK_PEER_GROUP_ID_CREATION**

---

## Peer Role Boundary

`peer_role` is **preliminary only**. It represents the candidate's expected role based on methodology but is not a final peer assignment.

**Allowed preliminary peer_role values** (from PGMF-DEC-03 taxonomy):
- `core_peer` — preliminary; subject to financial comparability gate verification
- `adjacent_peer` — preliminary; requires comparability_note
- `benchmark_context` — for ETFs/indices in company families
- `etf_peer` — for ETF/fund assets within PGF-09 only
- `excluded_non_peer` — explicitly excluded with rationale
- `private_comparable_context` — private company context only; valuation_peer_allowed = false

**Rule**: peer_role is not a final peer assignment and may not be used as production registry truth.

---

## Source Authority Fields

### source_authority_status

| Value | Meaning |
|-------|---------|
| `SOURCE_AUTHORITY_PRESENT` | At least one valid source reference exists for all CURRENT_METHODOLOGY fields |
| `SOURCE_EVIDENCE_MISSING` | One or more CURRENT_METHODOLOGY fields cannot trace to PGMF source registry |
| `SOURCE_DOMAIN_SCOPE_CONFLICT` | A source is cited outside its designated authority domain |
| `SOURCE_EXTENSION_REQUIRED` | Field requires a source not in current PGMF source registry (human/CTO approval needed) |
| `SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY` | Record is CANDIDATE_CONTEXT_ONLY; full source authority not required |

### source_authority_references

Structure: `[{source_id, authority_domain, tier_level, field_name}]`

Example: `[{source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}]`

### Rules

1. Every CURRENT_METHODOLOGY field requires source authority
2. Missing evidence must not be silently normalized
3. Missing evidence produces SOURCE_EVIDENCE_MISSING and flows into Task 11 Evidence Gap Register
4. No new source may be introduced without human/CTO approval (recorded with approver identity, approval date)

---

## Field Taxonomy Compatibility

| PGMF Scope Label | Schema Behavior | Value in Candidate Record |
|------------------|----------------|---------------------------|
| `CURRENT_METHODOLOGY` | Populate from source authority; requires PGMF source registry reference | Actual methodology-derived value |
| `CURRENT_MODEL_NULLABLE` | Field exists; value remains null with explanation | `null` |
| `DEFERRED` | Field exists; carries mandated deferred value | e.g., `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED` |
| `FUTURE_SCOPE` | Field placeholder; not populated | `NOT_POPULATED_IN_PREFLIGHT` |
| `FUTURE_VENDOR_INTEGRATION` | Field placeholder; requires commercial agreement | `NOT_POPULATED_IN_PREFLIGHT` |
| `FUTURE_COMPLIANCE_REFERENCE` | Vocabulary reference only; no operational weight | `FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL` |

---

## SAI Compatibility Fields

The following 17 SAI output contract fields must be present in every candidate record shape (from PGMF Section 10.3 / deferred_interfaces.md Section 2.3):

| SAI Field | Preflight Value | Production Safety |
|-----------|----------------|-------------------|
| `peer_group_available` | false | Not satisfied by preflight |
| `peer_comparison_allowed` | false | BLOCK_FINAL_PEER_ASSIGNMENT active |
| `blocked_reason` | "Peer Group Registry not yet available" | Candidate records do not unblock SAI-BLK-21 |
| `unsupported_status` | null or specific status | Per record |
| `primary_family` | PREFLIGHT_NOT_CANONICAL | Candidate only |
| `secondary_family` | PREFLIGHT_NOT_CANONICAL | Candidate only |
| `peer_role` | PREFLIGHT_NOT_CANONICAL | Not final assignment |
| `core_peer_set` | PREFLIGHT_NOT_CANONICAL | Not populated |
| `adjacent_peer_set` | PREFLIGHT_NOT_CANONICAL | Not populated |
| `benchmark_context_set` | PREFLIGHT_NOT_CANONICAL | Candidate only |
| `etf_peer_set` | PREFLIGHT_NOT_CANONICAL | PGF-09 only |
| `comparison_mode_allowed` | PREFLIGHT_NOT_CANONICAL | Not active |
| `financial_comparability_gate_status` | PREFLIGHT_NOT_CANONICAL | Not evaluated |
| `comparability_note` | PREFLIGHT_NOT_CANONICAL | Per record |
| `data_quality_status` | PREFLIGHT_NOT_CANONICAL | Not evaluated |
| `as_of_date` | PREFLIGHT_NOT_CANONICAL | Candidate date |
| `methodology_version` | PREFLIGHT_NOT_CANONICAL | PGMF v1 |

**SAI Contract Rule**: Candidate records do not satisfy the production SAI deferred peer group registry interface. SAI-BLK-21 remains in BLOCK_FINAL_PEER_ASSIGNMENT state.

---

## Market Data Boundary

- `market_data_fields_status` = NOT_POPULATED_IN_PREFLIGHT
- Market data fields may not affect Candidate_Status, peer_role, peer_comparison_allowed, or source_authority_status
- Any use of market data availability as methodology proxy triggers: **BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY**

---

## Trading Governance Boundary

- `trading_governance_fields_status` = FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
- No tradability, execution eligibility, broker connectivity, order-routing, or trading readiness defined
- Any inference of tradability triggers: **BLOCK_TRADING_ELIGIBILITY_INFERENCE**

---

## Unsupported Asset Schema Behavior

| Asset Category | Candidate_Status | unsupported_status | peer_role |
|----------------|-----------------|-------------------|-----------|
| Derivatives / options / warrants / certificates | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| Leveraged / structured products | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| Crypto / tokenized assets | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| Commodities | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| FX pairs | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| Bonds / fixed-income / money-market | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| Baskets / synthetic exposures | CANDIDATE_BLOCKED | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION | excluded_non_peer |
| Private companies | CANDIDATE_CONTEXT_ONLY | null | private_comparable_context |
| Indices | CANDIDATE_CONTEXT_ONLY | null | benchmark_context |
| ETFs / funds (in company families) | CANDIDATE_CONTEXT_ONLY | null | benchmark_context |
| ETFs / funds (in PGF-09) | CANDIDATE_DRAFT | null | etf_peer |
| Unresolved identity | CANDIDATE_BLOCKED | IDENTITY_UNRESOLVED | excluded_non_peer |

---

## Cross-Region Comparability Fields

Required for any asset where cross-region differences exist within the same family:

| Field | Required When | Rule |
|-------|--------------|------|
| `region` | Always | Geographic context |
| `domicile` | company / etf / fund | ISO 3166-1 alpha-2 |
| `reporting_currency` | company | ISO 4217 |
| `trading_currency` | listed assets | ISO 4217 |
| `accounting_standard` | company | GAAP / IFRS / other |
| `fiscal_year_end` | company | Three-letter month |
| `listing_variant_type` | multi-venue assets | primary / ADR / GDR / secondary |
| `comparability_adjustment_required` | cross-region records | true when accounting_standard differs between peers |
| `comparability_note` | when comparability_adjustment_required = true | Documents adjustments needed |

**Rule**: Cross-region differences must remain visible. They may not be silently normalized.

---

## Example Schema Template (Non-Instantiated)

```yaml
candidate_record_id: "<candidate_record_id>"
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: "<family_id>"
family_name: "<family_name>"
asset_name: "<asset_name>"
asset_type: "<asset_type>"
object_type: "<object_type>"
legal_entity_name: "<legal_entity_name>"
instrument_type: "<instrument_type>"
ticker_candidates: ["<ticker>"]
ISIN_candidates: ["<isin>"]
exchange_candidates: ["<exchange_mic>"]
region: "<region>"
domicile: "<domicile>"
reporting_currency: "<currency>"
trading_currency: "<currency>"
accounting_standard: "<standard>"
fiscal_year_end: "<month>"
listing_variant_type: "<variant>"
source_authority_status: "<status>"
source_authority_references:
  - source_id: "<source_id>"
    authority_domain: "<domain>"
    tier_level: "<tier>"
    field_name: "<field>"
methodology_decision_references: ["<PGMF-DEC-XX>"]
field_taxonomy_mapping_status: "<status>"
peer_role: "<peer_role>"
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: null
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: null
```

**Note**: This template contains placeholder values only. It does not represent a real asset. No real tickers, ISINs, or asset names are used.

---

## Prohibited Outputs

This artifact does NOT produce:
- Actual candidate records for PGF-01 through PGF-09
- peer_group_registry.yaml
- Production registry files
- Canonical peer_group_id values
- Final peer assignments
- SAI mutations
- Runtime code
- Validation code
- Market data integrations
- Trading or execution outputs

---

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Complete candidate record field table documented | YES |
| 2 | Required defaults defined (10 fields with mandatory defaults) | YES |
| 3 | Candidate_Status allowed values exhaustive (5 states) | YES |
| 4 | Production states explicitly prohibited | YES |
| 5 | peer_group_id placeholder rule defined | YES |
| 6 | SAI compatibility boundary defined (17 fields) | YES |
| 7 | Market data boundary defined | YES |
| 8 | Trading boundary defined | YES |
| 9 | Unsupported asset behavior defined | YES |
| 10 | Cross-region fields defined | YES |
| 11 | Schema template contains no real assets or tickers | YES |
| 12 | production_authority: NONE present | YES |

---

## Boundary Confirmation

| Boundary | Status |
|----------|--------|
| No candidate records created | CONFIRMED |
| No PGF candidate artifacts created | CONFIRMED |
| No registry created | CONFIRMED |
| No peer assignments created | CONFIRMED |
| No peer_group_id values created | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No runtime code | CONFIRMED |
| No validation code | CONFIRMED |
| No market data integration | CONFIRMED |
| No trading or execution scope | CONFIRMED |
| Task 4 not started | CONFIRMED |

---

## Final Status

```
CANDIDATE_RECORD_SCHEMA_PREFLIGHT_COMPLETE
```

---

*End of candidate record schema artifact.*
