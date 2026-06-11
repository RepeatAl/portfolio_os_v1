# Field Taxonomy Mapping Specification

> **Peer Group Registry Creation Preflight — Task 5: Field Taxonomy Mapping**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true

---

## Document Boundary

This artifact defines taxonomy mapping rules only; it does not apply them to records. No candidate records are mapped, created, or modified by this document. No registry files are produced. No canonical peer_group_id values are minted. No production content is created.

All rules defined herein govern how future preflight task execution will populate candidate record fields against the PGMF field taxonomy reference (`field_taxonomy_reference_2026-06-08.md`).

---

## 1. Scope Label Handling Rules

The PGMF field taxonomy classifies every field into one of 6 scope labels. Each scope label carries a specific preflight handling rule that governs how future candidate records will treat fields of that category.

### 1.1 CURRENT_METHODOLOGY

| Attribute | Value |
|-----------|-------|
| **Scope label** | CURRENT_METHODOLOGY |
| **Field count** | ~60 fields |
| **Preflight behavior** | Populate from source authority with PGMF source registry reference |
| **Value in candidate record** | Actual methodology-derived value (e.g., peer_role, accounting_standard, family_id) |
| **Source requirement** | At least one source_authority_reference per field linking to the PGMF source registry |
| **Governing reference** | `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` |
| **Methodology decisions** | PGMF-DEC-01 through PGMF-DEC-10 as applicable per field |
| **Missing field rule** | If REQUIRED and not populated → CANDIDATE_BLOCKED (BLOCK_SOURCE_INSUFFICIENT) |
| **Domain constraint** | Source must be cited within its designated authority_domain only (per DOMAIN_SCOPE_VIOLATION rule) |

**Key fields in this scope**: canonical_object_id, object_type, object_name, domicile, reporting_currency, fiscal_year_end, accounting_standard, taxonomy_reference, family_id, family_name, primary_family, peer_role, comparison_mode_allowed, effective_date, lifecycle_status, methodology_version, all financial comparability gate fields, all governance/versioning fields, all SAI output contract fields.

### 1.2 CURRENT_MODEL_NULLABLE

| Attribute | Value |
|-----------|-------|
| **Scope label** | CURRENT_MODEL_NULLABLE |
| **Field count** | 8 fields |
| **Preflight behavior** | Field exists in record structure; value remains null |
| **Value in candidate record** | `null` |
| **Source requirement** | None — structural placeholder only |
| **Population timing** | Not populated until market data vendor agreement exists |
| **Blocking rule** | Null value does NOT trigger CANDIDATE_BLOCKED |

**Fields in this scope**: exchange_mic (Layer 2 context), market_data_source, data_vendor, data_latency_class, exchange_timezone, trading_calendar_id, derived_data_policy, index_license_required.

**Rationale**: These fields must exist in the v1 schema to prevent architectural rewrite when market data is added later, but carry no value during preflight.

### 1.3 DEFERRED

| Attribute | Value |
|-----------|-------|
| **Scope label** | DEFERRED |
| **Field count** | 1 field (fixed value) |
| **Preflight behavior** | Field exists; carries mandated deferred value |
| **Value in candidate record** | `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED` |
| **Source requirement** | SRC-E-01 (financial_comparability_authority) — documents the deferral decision |
| **Blocking rule** | Deferred value does NOT trigger CANDIDATE_BLOCKED; value is explicitly mandated |
| **Rationale** | Numeric market-cap and liquidity thresholds are not finalized in v1; calibration requires additional sourcing from Russell/MSCI index construction methodology |

**Fields in this scope**: threshold_calibration_status.

**Mandatory value**: ALL v1 candidate records must carry `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED`. No other value is permitted for this field during preflight.

### 1.4 FUTURE_SCOPE

| Attribute | Value |
|-----------|-------|
| **Scope label** | FUTURE_SCOPE |
| **Field count** | Fields with requirement status FUTURE_SCOPE in the field taxonomy |
| **Preflight behavior** | Field placeholder reserved; not populated |
| **Value in candidate record** | `NOT_POPULATED_IN_PREFLIGHT` |
| **Source requirement** | None — placeholder only |
| **Blocking rule** | NOT_POPULATED_IN_PREFLIGHT value does NOT trigger CANDIDATE_BLOCKED |
| **Prohibition** | No value other than NOT_POPULATED_IN_PREFLIGHT may be assigned |
| **Activation condition** | Future methodology extension or scope expansion (separate spec required) |

### 1.5 FUTURE_VENDOR_INTEGRATION

| Attribute | Value |
|-----------|-------|
| **Scope label** | FUTURE_VENDOR_INTEGRATION |
| **Field count** | 9 fields |
| **Preflight behavior** | Field placeholder reserved; requires commercial agreement before population |
| **Value in candidate record** | `NOT_POPULATED_IN_PREFLIGHT` |
| **Source requirement** | None — placeholder only |
| **Blocking rule** | NOT_POPULATED_IN_PREFLIGHT value does NOT trigger CANDIDATE_BLOCKED |
| **Prohibition** | No value other than NOT_POPULATED_IN_PREFLIGHT may be assigned |
| **Activation condition** | Active commercial data vendor agreement per exchange/data provider |

**Fields in this scope**: realtime_entitlement_required, display_usage_allowed, non_display_usage_allowed, redistribution_allowed, professional_user_flag, market_data_audit_required, bid_ask_source, stale_quote_threshold, quote_timestamp_required.

### 1.6 FUTURE_COMPLIANCE_REFERENCE

| Attribute | Value |
|-----------|-------|
| **Scope label** | FUTURE_COMPLIANCE_REFERENCE |
| **Field count** | 15 fields |
| **Preflight behavior** | Field is vocabulary reference only; no operational weight |
| **Value in candidate record** | `FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL` |
| **Source requirement** | None — reserved vocabulary only |
| **Blocking rule** | FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL value does NOT trigger CANDIDATE_BLOCKED |
| **Prohibition** | No value other than FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL may be assigned |
| **Legal statement** | Creates NO current legal obligations. MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue. |
| **Activation condition** | Regulatory engagement and compliance infrastructure implementation (not in scope) |

**Fields in this scope**: tradability_status, trading_enabled, trade_block_reason, execution_venue_eligible, best_execution_required, order_routing_policy_required, pre_trade_controls_required, price_collar_policy, max_order_value_policy, kill_switch_required, audit_log_required, surveillance_required, market_abuse_monitoring_required, algo_trading_flag, manual_trade_only_flag.

---

## 2. Scope Label Summary Table

| Scope Label | Preflight Value | Blocking? | Source Required? | Field Count |
|-------------|-----------------|-----------|------------------|-------------|
| CURRENT_METHODOLOGY | Actual methodology-derived value from PGMF source authority | Yes — if REQUIRED and missing | Yes — at least one source_authority_reference | ~60 |
| CURRENT_MODEL_NULLABLE | `null` | No | No | 8 |
| DEFERRED | Mandated deferred value (NUMERIC_THRESHOLDS_DEFERRED) | No | Yes (documents deferral decision) | 1 |
| FUTURE_SCOPE | `NOT_POPULATED_IN_PREFLIGHT` | No | No | Variable |
| FUTURE_VENDOR_INTEGRATION | `NOT_POPULATED_IN_PREFLIGHT` | No | No | 9 |
| FUTURE_COMPLIANCE_REFERENCE | `FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL` | No | No | 15 |

---

## 3. Required Field Completeness Rules

### 3.1 Core Completeness Rule

**Rule**: Every CURRENT_METHODOLOGY field with requirement status REQUIRED for the candidate record's asset_type MUST be populated with a non-empty value, OR the record's Candidate_Status SHALL be set to CANDIDATE_BLOCKED.

### 3.2 Completeness by Requirement Status

| Requirement Status | Completeness Rule | Blocking Behavior |
|--------------------|-------------------|-------------------|
| REQUIRED | Must be present and non-empty for the record's asset_type | CANDIDATE_BLOCKED if missing; blocked_reason = BLOCK_SOURCE_INSUFFICIENT |
| REQUIRED_IF_LISTED | Must be present when the asset has an active exchange listing | CANDIDATE_BLOCKED if listed and missing |
| REQUIRED_IF_AVAILABLE | Must be populated OR carry a documented gap rationale | CANDIDATE_BLOCKED only if gap rationale is also missing |
| REQUIRED_IF_APPLICABLE | Must be present when the field's subject applies to this record | CANDIDATE_BLOCKED if applicable and missing |
| OPTIONAL | May be present; absence does NOT block | Never blocks |
| NOT_APPLICABLE | Must be absent or explicitly marked NOT_APPLICABLE | Never blocks; presence of a value is an error |
| FUTURE_SCOPE | Carries NOT_POPULATED_IN_PREFLIGHT | Never blocks |

### 3.3 Blocking Documentation Requirements

When a REQUIRED field is missing and CANDIDATE_BLOCKED is triggered, the following must be documented:

| Field | Content |
|-------|---------|
| `Candidate_Status` | CANDIDATE_BLOCKED |
| `blocked_reason` | BLOCK_SOURCE_INSUFFICIENT |
| `missing_field_name` | The specific REQUIRED field that is missing |
| `asset_type_requiring_it` | The record's asset_type that mandates this field |
| `source_authority_domain_responsible` | The authority domain from which the source must come |
| `remediation` | Identify and provide a valid source from PGMF source registry within the correct authority domain |

### 3.4 REQUIRED_IF_AVAILABLE Gap Rationale

When a REQUIRED_IF_AVAILABLE field cannot be populated, the gap rationale must include:

| Element | Description |
|---------|-------------|
| `field_name` | The specific field |
| `gap_reason` | Why the data is not available (e.g., "Private company — no public ISIN issued") |
| `source_searched` | Which PGMF sources were consulted |
| `remediation_expectation` | Whether future availability is expected |

---

## 4. Asset-Type Applicability Rules

### 4.1 Core Principle (PGMF-DEC-04)

Field requirements vary by object_type. The record's `asset_type` value determines which fields are REQUIRED, OPTIONAL, or NOT_APPLICABLE for that specific record. Field applicability is determined by referencing the asset_type applicability column in the PGMF field taxonomy (`field_taxonomy_reference_2026-06-08.md`, Section 13).

### 4.2 Asset-Type Applicability Matrix

| Field Category | company | etf | fund | index | private_company | unsupported_asset_class |
|----------------|---------|-----|------|-------|-----------------|-------------------------|
| **Layer 1 Identity** (canonical_object_id, object_type, object_name) | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| **Domicile, reporting_currency** | REQUIRED | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| **fiscal_year_end** | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| **accounting_standard** | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| **taxonomy_reference** | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **Layer 2 Security** (isin, figi) | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **Layer 2 Listing** (ticker, exchange_mic, primary_listing, listing_variant_type) | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **adr_flag** | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **trading_currency** | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **Layer 3 Assignment** (family_id, family_name, primary_family, asset_type, peer_role, comparison_mode_allowed) | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| **secondary_family** | OPTIONAL | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **subcluster_id, subcluster_name** | REQUIRED_IF_APPLICABLE | REQUIRED_IF_APPLICABLE | REQUIRED_IF_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **ETF/Fund fields** (benchmark_index, TER, AUM, tracking_difference, tracking_error, spread, holdings_overlap, replication_method, distribution_policy, lookthrough_concentration) | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **Financial Comparability Gate fields** | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **Cross-Region fields** (comparability_adjustment_required, comparability_note) | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| **Governance fields** (effective_date, lifecycle_status, review_cycle, etc.) | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| **Unsupported fields** (unsupported_status) | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | REQUIRED |
| **peer_comparison_allowed, peer_group_available, blocked_reason** | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |

### 4.3 Peer Role Validity by Asset Type

| asset_type | Valid peer_role Values |
|------------|----------------------|
| company | core_peer, adjacent_peer, benchmark_context, excluded_non_peer |
| etf | etf_peer, benchmark_context, excluded_non_peer |
| fund | etf_peer, benchmark_context, excluded_non_peer |
| index | benchmark_context ONLY |
| private_company | private_comparable_context ONLY |
| unsupported_asset_class | excluded_non_peer ONLY (or null) |

### 4.4 Asset-Type Determination Rule

When mapping fields for a candidate record, the record's `asset_type` value SHALL be determined FIRST. Only after asset_type is confirmed may field applicability be evaluated. The asset_type determines:
1. Which fields are REQUIRED vs. NOT_APPLICABLE
2. Which peer_role values are valid
3. Which comparison_mode_allowed values are permitted
4. Which boundary rules apply (ETF/Fund, cross-region, unsupported)

---

## 5. Peer Group ID Placeholder Rule

### 5.1 Core Rule

**The `peer_group_id` field in ALL candidate records SHALL carry the value `PREFLIGHT_PLACEHOLDER_NOT_CANONICAL`.** No canonical peer_group_id values are permitted during preflight.

### 5.2 Enforcement

| Attribute | Value |
|-----------|-------|
| Field | `peer_group_id` |
| Preflight value | `PREFLIGHT_PLACEHOLDER_NOT_CANONICAL` |
| peer_group_id_status | `NOT_CREATED` |
| Canonical IDs permitted | **NO** — zero canonical values allowed |
| Blocking trigger | Any attempt to mint or assign a canonical peer_group_id → BLOCK_PEER_GROUP_ID_CREATION |
| Candidate_Status outcome | CANDIDATE_BLOCKED |
| Remediation | Remove canonical ID; restore placeholder value |

### 5.3 Rationale

Canonical peer_group_id values are minted only during future production registry creation (a separate spec requiring human/CTO approval). The preflight phase establishes candidate records with placeholder values to demonstrate structural readiness without creating production-weight identifiers.

### 5.4 No Canonical ID Values Permitted — Absolute Rule

The following ID-like values are FORBIDDEN in any candidate record during preflight:

| Forbidden Pattern | Reason |
|-------------------|--------|
| Any value resembling a production ID (e.g., PG-001, PGR-2026-001) | Implies production registry exists |
| UUID-format values assigned as peer_group_id | Implies canonical identification |
| Sequential numeric IDs as peer_group_id | Implies canonical ordering |
| Any peer_group_id value other than PREFLIGHT_PLACEHOLDER_NOT_CANONICAL | Violates preflight boundary |

---

## 6. Scope Label to Source Authority Linkage

### 6.1 Source Authority Requirements by Scope Label

| Scope Label | Source Authority Required? | Source Registry Reference |
|-------------|---------------------------|---------------------------|
| CURRENT_METHODOLOGY | **YES** — mandatory per field | `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` |
| CURRENT_MODEL_NULLABLE | No — structural placeholder | N/A |
| DEFERRED | Yes — documents deferral decision | SRC-E-01 (financial_comparability_authority) |
| FUTURE_SCOPE | No — placeholder reserved | N/A |
| FUTURE_VENDOR_INTEGRATION | No — placeholder reserved | N/A |
| FUTURE_COMPLIANCE_REFERENCE | No — vocabulary reference only | N/A |

### 6.2 CURRENT_METHODOLOGY Source Authority Enforcement

For every CURRENT_METHODOLOGY field on a candidate record:

1. **Source reference required**: At least one `source_authority_reference` entry must link the field to a source in the PGMF source registry
2. **Domain match required**: The source's `authority_domain` must match the field's required `source_authority_domain` from the field taxonomy
3. **Tier hierarchy respected**: Tier 1 sources produce hard rules; Tier 2/3 support only
4. **Missing source → CANDIDATE_BLOCKED**: If no valid source exists → SOURCE_EVIDENCE_MISSING → CANDIDATE_BLOCKED
5. **Domain violation → CANDIDATE_BLOCKED**: If source cited outside its domain → DOMAIN_SCOPE_VIOLATION → CANDIDATE_BLOCKED

### 6.3 Source Authority Domain Assignments (Summary)

| Authority Domain | Fields Governed | Tier 1 Sources |
|-----------------|----------------|----------------|
| identity_authority | canonical_object_id, object_type, object_name, security_id, isin, figi, ticker, exchange_mic, primary_listing, listing_variant_type, adr_flag, asset_type | SRC-G-01, SRC-I-01 |
| classification_authority | family_id, family_name, primary_family, taxonomy_reference, subcluster_id, subcluster_name, index_provider, benchmark_index_id, peer_group_available, unsupported_status | SRC-B-01, SRC-B-02, SRC-B-03, SRC-C-01 |
| strategic_peer_logic_authority | peer_role, secondary_family, comparison_mode_allowed, peer_comparison_allowed | SRC-D-01 |
| financial_comparability_authority | business_model_similarity, market_cap_band, liquidity_band, growth_profile_comparable, margin_structure_comparable, capital_intensity_comparable, leverage_comparable, valuation_peer_allowed, financial_comparability_gate_status, comparability_note_required, threshold_calibration_status | SRC-E-01, SRC-E-03 |
| ETF_methodology_authority | benchmark_index, TER, AUM, tracking_difference, tracking_error, spread, holdings_overlap, replication_method, distribution_policy, lookthrough_concentration | SRC-F-01 |
| accounting_authority | domicile, reporting_currency, fiscal_year_end, accounting_standard, trading_currency, comparability_adjustment_required, comparability_note | SRC-H-01, SRC-H-02, SRC-H-03 |
| governance_authority | effective_date, end_date, lifecycle_status, review_cycle, approved_by, source_authority, change_reason, challenge_status, review_status, methodology_version, blocked_reason | SRC-A-01, SRC-A-02, SRC-A-03 |

---

## 7. Mapping Validation Rules

### 7.1 Field Taxonomy Mapping Status

Each candidate record SHALL carry a `field_taxonomy_mapping_status` field with one of the following values:

| Status | Definition | Candidate_Status Impact |
|--------|-----------|------------------------|
| `COMPLETE` | All REQUIRED fields for the record's asset_type are populated with valid values and source references | Permits transition to CANDIDATE_READY_FOR_REVIEW |
| `INCOMPLETE` | One or more REQUIRED_IF_AVAILABLE fields lack values but have documented gap rationales | Does NOT block; record may remain CANDIDATE_DRAFT |
| `BLOCKED` | One or more REQUIRED fields are missing → CANDIDATE_BLOCKED | Record is CANDIDATE_BLOCKED until gaps resolved |

### 7.2 Mapping Completeness Validation Sequence

Future preflight task execution SHALL validate field taxonomy mapping in the following order:

1. **Determine asset_type** — establishes which fields are applicable
2. **Check REQUIRED fields** — all must be populated or record is CANDIDATE_BLOCKED
3. **Check REQUIRED_IF_LISTED fields** — required if asset has exchange listing
4. **Check REQUIRED_IF_AVAILABLE fields** — populated or gap rationale documented
5. **Check REQUIRED_IF_APPLICABLE fields** — required when field subject applies
6. **Verify CURRENT_MODEL_NULLABLE fields exist** — structural presence with null value
7. **Verify DEFERRED field value** — threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED
8. **Verify FUTURE_SCOPE/FUTURE_VENDOR_INTEGRATION fields** — carry NOT_POPULATED_IN_PREFLIGHT
9. **Verify FUTURE_COMPLIANCE_REFERENCE fields** — carry FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
10. **Verify peer_group_id** — must be PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
11. **Set field_taxonomy_mapping_status** — COMPLETE, INCOMPLETE, or BLOCKED

### 7.3 Cross-Reference to Source Authority Mapping

Field taxonomy mapping validation works in conjunction with the Source Authority Mapping rules (Task 4 artifact: `source_authority_mapping_preflight.md`):

- Every CURRENT_METHODOLOGY field populated in step 2–5 must also satisfy the source authority requirement
- A field may be structurally present (taxonomy mapping satisfied) but lack source authority (source authority mapping unsatisfied) — both conditions must be met for CANDIDATE_READY_FOR_REVIEW
- field_taxonomy_mapping_status = COMPLETE requires BOTH structural completeness AND source authority coverage

---

## 8. Prohibited Actions

This section confirms what this field taxonomy mapping specification does NOT do and does NOT permit:

| Prohibition | Rationale |
|-------------|-----------|
| No candidate records mapped | This artifact defines rules only |
| No candidate records created | Creation occurs in future Task 10 |
| No field values assigned to records | Assignment occurs during future task execution |
| No peer_group_id values minted | Canonical IDs are not created in preflight |
| No production registry content | Production registry requires a separate spec |
| No source authority references applied | Application occurs during future task execution |
| No ACTIVE or APPROVED lifecycle states | Prohibited during preflight |
| No production_authority other than NONE | All preflight artifacts carry production_authority: NONE |
| No SAI artifact modification | SAI remains stable |
| No market data integration | Market data fields reserved only |
| No trading governance activation | Trading fields carry FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL only |

---

## 9. Reference Documents

| Document | Path | Role in This Specification |
|----------|------|---------------------------|
| PGMF Field Taxonomy Reference | `.kiro/specs/peer-group-registry-methodology-framework/artifacts/field_taxonomy_reference_2026-06-08.md` | Primary reference — defines all fields, scope labels, and asset-type applicability |
| PGMF Source Registry | `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` | Source authority for CURRENT_METHODOLOGY fields |
| Source Authority Mapping (Task 4) | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/source_authority_mapping_preflight.md` | Defines field-to-source domain assignments |
| Source Alignment (Task 1) | `.kiro/specs/peer-group-registry-creation-preflight/artifacts/source_alignment_preflight.md` | Confirms all source artifacts exist and are accessible |
| Design Document | `.kiro/specs/peer-group-registry-creation-preflight/design.md` | Field Taxonomy Mapping Design section — governs this artifact |
| Requirements Document | `.kiro/specs/peer-group-registry-creation-preflight/requirements.md` | R5 (Field Taxonomy Mapping) — this artifact satisfies R5 |

---

## 10. Acceptance Criteria Verification

| Criterion | Status | Evidence |
|-----------|--------|----------|
| All 6 scope labels have clear handling rules | **SATISFIED** | Section 1 (1.1–1.6) defines handling for CURRENT_METHODOLOGY, CURRENT_MODEL_NULLABLE, DEFERRED, FUTURE_SCOPE, FUTURE_VENDOR_INTEGRATION, FUTURE_COMPLIANCE_REFERENCE |
| Asset-type-aware field applicability documented | **SATISFIED** | Section 4 documents field applicability per asset_type per PGMF-DEC-04 |
| Blocking conditions for missing REQUIRED fields are explicit | **SATISFIED** | Section 3 defines completeness rules; Section 3.3 documents blocking requirements |
| Document carries production_authority: NONE | **SATISFIED** | Header declares production_authority: NONE |

---

## 11. Hard Boundary Confirmation

| Boundary | Confirmed |
|----------|-----------|
| Rule definition only — no records mapped | YES |
| No candidate records created or modified | YES |
| No registry files produced | YES |
| No canonical peer_group_id values | YES |
| No production content | YES |
| No SAI artifact mutation | YES |
| No runtime code | YES |
| No market data integration | YES |
| No trading governance activation | YES |

---

## Artifact Status

```
FIELD_TAXONOMY_MAPPING_PREFLIGHT_COMPLETE
```

---

*End of field taxonomy mapping specification.*
