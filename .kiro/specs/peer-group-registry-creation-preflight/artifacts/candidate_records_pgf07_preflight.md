# Candidate Record Drafts — PGF-07: Industrials / Power / Grid / Cooling

> **Peer Group Registry Creation Preflight — Task 10: Candidate Record Drafts**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true
> family_id: PGF-07 | family_name: Industrials / Power / Grid / Cooling

---

## Document Boundary

This artifact contains non-production candidate record drafts for PGF-07 only. No record constitutes a production registry entry, final peer assignment, or canonical peer_group_id. All tickers, subclusters, and benchmark instruments are sourced exclusively from the scope preflight document.

---

## Source Authority

- **Family/ticker authority**: `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5, Family PGF-07
- **Methodology authority**: PGMF (12/12 tasks, VG-PGMF-1 PASS)
- **Source registry**: `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`

---

## Core Candidate Records (9)

### Record 1: ETN (Eaton Corporation plc)

```yaml
candidate_record_id: PGF07-CORE-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Eaton Corporation plc
asset_type: company
object_type: company
legal_entity_name: Eaton Corporation plc
instrument_type: equity
ticker_candidates: ["ETN"]
ISIN_candidates: ["IE00B8KQN827"]
exchange_candidates: ["XNYS"]
region: North America
domicile: IE
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: "Ireland-domiciled but reports in USD under GAAP. No accounting standard difference vs. US GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure. Ireland domicile; primary listing NYSE."
```

### Record 2: Schneider Electric (Schneider Electric SE)

```yaml
candidate_record_id: PGF07-CORE-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Schneider Electric SE
asset_type: company
object_type: company
legal_entity_name: Schneider Electric SE
instrument_type: equity
ticker_candidates: ["Schneider Electric"]
ISIN_candidates: ["FR0000121972"]
exchange_candidates: ["XPAR"]
region: Europe
domicile: FR
reporting_currency: EUR
trading_currency: EUR
accounting_standard: IFRS
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-H-01", authority_domain: "accounting_authority", tier_level: "Tier 1", field_name: "accounting_standard"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: true
comparability_note: "IFRS reporting in EUR; Paris-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure. Cross-region: Paris-listed / Euronext."
```

### Record 3: Siemens (Siemens AG)

```yaml
candidate_record_id: PGF07-CORE-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Siemens AG
asset_type: company
object_type: company
legal_entity_name: Siemens AG
instrument_type: equity
ticker_candidates: ["Siemens"]
ISIN_candidates: ["DE0007236101"]
exchange_candidates: ["XETR"]
region: Europe
domicile: DE
reporting_currency: EUR
trading_currency: EUR
accounting_standard: IFRS
fiscal_year_end: SEP
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-H-01", authority_domain: "accounting_authority", tier_level: "Tier 1", field_name: "accounting_standard"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: true
comparability_note: "IFRS reporting in EUR; Frankfurt-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure. Cross-region: Frankfurt-listed / XETRA."
```

### Record 4: ABB (ABB Ltd)

```yaml
candidate_record_id: PGF07-CORE-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: ABB Ltd
asset_type: company
object_type: company
legal_entity_name: ABB Ltd
instrument_type: equity
ticker_candidates: ["ABB"]
ISIN_candidates: ["CH0012221716"]
exchange_candidates: ["XSWX"]
region: Europe
domicile: CH
reporting_currency: USD
trading_currency: CHF
accounting_standard: IFRS
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-H-01", authority_domain: "accounting_authority", tier_level: "Tier 1", field_name: "accounting_standard"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: true
comparability_note: "IFRS reporting in USD; Zurich-listed. Swiss-domiciled but reports in USD. IFRS accounting standard differs from GAAP peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure. Cross-region: Zurich-listed / SIX Swiss Exchange."
```

### Record 5: VRT (Vertiv Holdings Co)

```yaml
candidate_record_id: PGF07-CORE-005
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Vertiv Holdings Co
asset_type: company
object_type: company
legal_entity_name: Vertiv Holdings Co
instrument_type: equity
ticker_candidates: ["VRT"]
ISIN_candidates: ["US92537N1081"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-02", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster B — AI Data Center Power / Cooling. Cross-family: VRT also appears in PGF-01 scope."
```

### Record 6: Trane (Trane Technologies plc)

```yaml
candidate_record_id: PGF07-CORE-006
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Trane Technologies plc
asset_type: company
object_type: company
legal_entity_name: Trane Technologies plc
instrument_type: equity
ticker_candidates: ["TT"]
ISIN_candidates: ["IE00BK9ZQ967"]
exchange_candidates: ["XNYS"]
region: North America
domicile: IE
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: "Ireland-domiciled but reports in USD under GAAP. No accounting standard difference vs. US GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster B — AI Data Center Power / Cooling. Ireland domicile; primary listing NYSE."
```

### Record 7: Carrier (Carrier Global Corporation)

```yaml
candidate_record_id: PGF07-CORE-007
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Carrier Global Corporation
asset_type: company
object_type: company
legal_entity_name: Carrier Global Corporation
instrument_type: equity
ticker_candidates: ["CARR"]
ISIN_candidates: ["US14448C1045"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster B — AI Data Center Power / Cooling"
```

### Record 8: CAT (Caterpillar Inc.)

```yaml
candidate_record_id: PGF07-CORE-008
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Caterpillar Inc.
asset_type: company
object_type: company
legal_entity_name: Caterpillar Inc.
instrument_type: equity
ticker_candidates: ["CAT"]
ISIN_candidates: ["US1491231015"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster C — Industrial Capital Equipment / Rental"
```

### Record 9: URI (United Rentals, Inc.)

```yaml
candidate_record_id: PGF07-CORE-009
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: United Rentals, Inc.
asset_type: company
object_type: company
legal_entity_name: United Rentals, Inc.
instrument_type: equity
ticker_candidates: ["URI"]
ISIN_candidates: ["US9113631090"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster C — Industrial Capital Equipment / Rental"
```

---

## Adjacent Candidate Records (4)

### Record 10: GE Vernova (GE Vernova Inc.)

```yaml
candidate_record_id: PGF07-ADJ-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: GE Vernova Inc.
asset_type: company
object_type: company
legal_entity_name: GE Vernova Inc.
instrument_type: equity
ticker_candidates: ["GEV"]
ISIN_candidates: ["US36828A1016"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-02", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: adjacent_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure. Unresolved: core or adjacent given recent spinoff from GE."
```

### Record 11: Prysmian (Prysmian S.p.A.)

```yaml
candidate_record_id: PGF07-ADJ-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Prysmian S.p.A.
asset_type: company
object_type: company
legal_entity_name: Prysmian S.p.A.
instrument_type: equity
ticker_candidates: ["Prysmian"]
ISIN_candidates: ["IT0004176001"]
exchange_candidates: ["XMIL"]
region: Europe
domicile: IT
reporting_currency: EUR
trading_currency: EUR
accounting_standard: IFRS
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-H-01", authority_domain: "accounting_authority", tier_level: "Tier 1", field_name: "accounting_standard"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
field_taxonomy_mapping_status: COMPLETE
peer_role: adjacent_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: true
comparability_note: "IFRS reporting in EUR; Milan-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure. Cross-region: Milan-listed / Borsa Italiana."
```

### Record 12: Hubbell (Hubbell Incorporated)

```yaml
candidate_record_id: PGF07-ADJ-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Hubbell Incorporated
asset_type: company
object_type: company
legal_entity_name: Hubbell Incorporated
instrument_type: equity
ticker_candidates: ["HUBB"]
ISIN_candidates: ["US4435106079"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: adjacent_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure"
```

### Record 13: Quanta Services (Quanta Services, Inc.)

```yaml
candidate_record_id: PGF07-ADJ-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Quanta Services, Inc.
asset_type: company
object_type: company
legal_entity_name: Quanta Services, Inc.
instrument_type: equity
ticker_candidates: ["PWR"]
ISIN_candidates: ["US74762E1029"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06"]
field_taxonomy_mapping_status: COMPLETE
peer_role: adjacent_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Electrification / Grid Infrastructure"
```

---

## Benchmark Context Records (2)

### Record 14: XLI (Industrials Select Sector SPDR)

```yaml
candidate_record_id: PGF07-BMK-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: Industrials Select Sector SPDR
asset_type: etf
object_type: etf
legal_entity_name: Industrials Select Sector SPDR Fund
instrument_type: etf
ticker_candidates: ["XLI"]
ISIN_candidates: null
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: null
fiscal_year_end: null
listing_variant_type: primary
source_authority_status: SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: benchmark_context
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
notes: "ETF in company family — benchmark_context only per PGMF-DEC-05."
```

### Record 15: GRID (First Trust NASDAQ Clean Edge Smart Grid and Energy Innovation ETF)

```yaml
candidate_record_id: PGF07-BMK-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-07
family_name: Industrials / Power / Grid / Cooling
asset_name: First Trust NASDAQ Clean Edge Smart Grid and Energy Innovation ETF
asset_type: etf
object_type: etf
legal_entity_name: First Trust NASDAQ Clean Edge Smart Grid and Energy Innovation ETF
instrument_type: etf
ticker_candidates: ["GRID"]
ISIN_candidates: null
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: null
fiscal_year_end: null
listing_variant_type: primary
source_authority_status: SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "peer_role"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: benchmark_context
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
notes: "ETF in company family — benchmark_context only per PGMF-DEC-05."
```

---

## PGF-07 Summary

| Category | Count | Status Distribution |
|----------|-------|---------------------|
| Core candidates | 9 | 9 × CANDIDATE_DRAFT |
| Adjacent candidates | 4 | 4 × CANDIDATE_DRAFT |
| Benchmark context | 2 | 2 × CANDIDATE_CONTEXT_ONLY |
| **Total records** | **15** | |

| Cross-Region Records | Comparability Required | Reason |
|---------------------|----------------------|--------|
| Schneider Electric (FR) | Yes | IFRS/EUR vs GAAP/USD |
| Siemens (DE) | Yes | IFRS/EUR vs GAAP/USD |
| ABB (CH) | Yes | IFRS vs GAAP (reports in USD but IFRS standard) |
| Prysmian (IT) | Yes | IFRS/EUR vs GAAP/USD |

| Irish-Domiciled (GAAP/USD) | Comparability Required | Reason |
|---------------------------|----------------------|--------|
| ETN (IE) | No | GAAP/USD — no standard difference |
| Trane (IE) | No | GAAP/USD — no standard difference |

---

## No-Invention Confirmation

- All 9 core tickers from scope preflight: ETN, Schneider Electric, Siemens, ABB, VRT, Trane, Carrier, CAT, URI ✓
- All 4 adjacent tickers from scope preflight: GE Vernova, Prysmian, Hubbell, Quanta Services ✓
- All 2 benchmark instruments from scope preflight: XLI, GRID ✓
- No new tickers invented ✓
- No new subclusters invented ✓
- No new benchmark instruments invented ✓

---

*End of PGF-07 candidate record drafts.*
