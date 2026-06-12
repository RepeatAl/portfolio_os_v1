# Candidate Record Drafts — PGF-05: Consumer / Retail / Event Consumption

> **Peer Group Registry Creation Preflight — Task 10: Candidate Record Drafts**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true
> family_id: PGF-05 | family_name: Consumer / Retail / Event Consumption

---

## Document Boundary

This artifact contains non-production candidate record drafts for PGF-05 only. No record constitutes a production registry entry, final peer assignment, or canonical peer_group_id. All tickers, subclusters, and benchmark instruments are sourced exclusively from the scope preflight document.

---

## Source Authority

- **Family/ticker authority**: `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5, Family PGF-05
- **Methodology authority**: PGMF (12/12 tasks, VG-PGMF-1 PASS)
- **Source registry**: `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`

---

## Core Candidate Records (11)

### Record 1: WMT (Walmart Inc.)

```yaml
candidate_record_id: PGF05-CORE-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Walmart Inc.
asset_type: company
object_type: company
legal_entity_name: Walmart Inc.
instrument_type: equity
ticker_candidates: ["WMT"]
ISIN_candidates: ["US9311421039"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JAN
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
notes: "Subcluster A — Retail (Mass / Warehouse)"
```

### Record 2: COST (Costco Wholesale Corporation)

```yaml
candidate_record_id: PGF05-CORE-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Costco Wholesale Corporation
asset_type: company
object_type: company
legal_entity_name: Costco Wholesale Corporation
instrument_type: equity
ticker_candidates: ["COST"]
ISIN_candidates: ["US22160K1051"]
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: AUG
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
notes: "Subcluster A — Retail (Mass / Warehouse)"
```

### Record 3: TGT (Target Corporation)

```yaml
candidate_record_id: PGF05-CORE-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Target Corporation
asset_type: company
object_type: company
legal_entity_name: Target Corporation
instrument_type: equity
ticker_candidates: ["TGT"]
ISIN_candidates: ["US87612E1064"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JAN
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
notes: "Subcluster A — Retail (Mass / Warehouse)"
```

### Record 4: AMZN (Amazon.com, Inc.)

```yaml
candidate_record_id: PGF05-CORE-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Amazon.com, Inc.
asset_type: company
object_type: company
legal_entity_name: Amazon.com, Inc.
instrument_type: equity
ticker_candidates: ["AMZN"]
ISIN_candidates: ["US0231351067"]
exchange_candidates: ["XNAS"]
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
notes: "Subcluster B — E-Commerce / Omnichannel. Unresolved: multi-segment (retail vs cloud vs logistics)"
```

### Record 5: NKE (NIKE, Inc.)

```yaml
candidate_record_id: PGF05-CORE-005
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: NIKE, Inc.
asset_type: company
object_type: company
legal_entity_name: NIKE, Inc.
instrument_type: equity
ticker_candidates: ["NKE"]
ISIN_candidates: ["US6541061031"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: MAY
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
notes: "Subcluster C — Consumer Brands / Athletic"
```

### Record 6: ADS (adidas AG)

```yaml
candidate_record_id: PGF05-CORE-006
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: adidas AG
asset_type: company
object_type: company
legal_entity_name: adidas AG
instrument_type: equity
ticker_candidates: ["ADS"]
ISIN_candidates: ["DE000A1EWWW0"]
exchange_candidates: ["XETR"]
region: Europe
domicile: DE
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
comparability_note: "IFRS reporting in EUR; Frankfurt-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster C — Consumer Brands / Athletic. Cross-region inclusion (IFRS/EUR)."
```

### Record 7: MCD (McDonald's Corporation)

```yaml
candidate_record_id: PGF05-CORE-007
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: McDonald's Corporation
asset_type: company
object_type: company
legal_entity_name: McDonald's Corporation
instrument_type: equity
ticker_candidates: ["MCD"]
ISIN_candidates: ["US5801351017"]
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
notes: "Subcluster D — Restaurants / QSR"
```

### Record 8: QSR (Restaurant Brands International Inc.)

```yaml
candidate_record_id: PGF05-CORE-008
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Restaurant Brands International Inc.
asset_type: company
object_type: company
legal_entity_name: Restaurant Brands International Inc.
instrument_type: equity
ticker_candidates: ["QSR"]
ISIN_candidates: ["CA76131D1033"]
exchange_candidates: ["XNYS"]
region: North America
domicile: CA
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
notes: "Subcluster D — Restaurants / QSR. Domiciled in Canada; reports in USD under GAAP."
```

### Record 9: SBUX (Starbucks Corporation)

```yaml
candidate_record_id: PGF05-CORE-009
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Starbucks Corporation
asset_type: company
object_type: company
legal_entity_name: Starbucks Corporation
instrument_type: equity
ticker_candidates: ["SBUX"]
ISIN_candidates: ["US8552441094"]
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: SEP
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
notes: "Subcluster D — Restaurants / QSR"
```

### Record 10: KO (The Coca-Cola Company)

```yaml
candidate_record_id: PGF05-CORE-010
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: The Coca-Cola Company
asset_type: company
object_type: company
legal_entity_name: The Coca-Cola Company
instrument_type: equity
ticker_candidates: ["KO"]
ISIN_candidates: ["US1912161007"]
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
notes: "Subcluster E — Consumer Staples / Beverages"
```

### Record 11: PEP (PepsiCo, Inc.)

```yaml
candidate_record_id: PGF05-CORE-011
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: PepsiCo, Inc.
asset_type: company
object_type: company
legal_entity_name: PepsiCo, Inc.
instrument_type: equity
ticker_candidates: ["PEP"]
ISIN_candidates: ["US7134481081"]
exchange_candidates: ["XNAS"]
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
notes: "Subcluster E — Consumer Staples / Beverages"
```

---

## Adjacent Candidate Records (5)

### Record 12: LULU (Lululemon Athletica Inc.)

```yaml
candidate_record_id: PGF05-ADJ-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Lululemon Athletica Inc.
asset_type: company
object_type: company
legal_entity_name: Lululemon Athletica Inc.
instrument_type: equity
ticker_candidates: ["LULU"]
ISIN_candidates: ["US5500211090"]
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JAN
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
notes: "Subcluster C — Consumer Brands / Athletic (adjacent peer)"
```

### Record 13: TJX (The TJX Companies, Inc.)

```yaml
candidate_record_id: PGF05-ADJ-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: The TJX Companies, Inc.
asset_type: company
object_type: company
legal_entity_name: The TJX Companies, Inc.
instrument_type: equity
ticker_candidates: ["TJX"]
ISIN_candidates: ["US8725401090"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JAN
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
notes: "Subcluster F — Home Improvement / Specialty Retail (adjacent peer)"
```

### Record 14: HD (The Home Depot, Inc.)

```yaml
candidate_record_id: PGF05-ADJ-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: The Home Depot, Inc.
asset_type: company
object_type: company
legal_entity_name: The Home Depot, Inc.
instrument_type: equity
ticker_candidates: ["HD"]
ISIN_candidates: ["US4370761029"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JAN
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
notes: "Subcluster F — Home Improvement / Specialty Retail (adjacent peer)"
```

### Record 15: LOW (Lowe's Companies, Inc.)

```yaml
candidate_record_id: PGF05-ADJ-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Lowe's Companies, Inc.
asset_type: company
object_type: company
legal_entity_name: Lowe's Companies, Inc.
instrument_type: equity
ticker_candidates: ["LOW"]
ISIN_candidates: ["US5486611073"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JAN
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
notes: "Subcluster F — Home Improvement / Specialty Retail (adjacent peer)"
```

### Record 16: CMG (Chipotle Mexican Grill, Inc.)

```yaml
candidate_record_id: PGF05-ADJ-005
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Chipotle Mexican Grill, Inc.
asset_type: company
object_type: company
legal_entity_name: Chipotle Mexican Grill, Inc.
instrument_type: equity
ticker_candidates: ["CMG"]
ISIN_candidates: ["US1696561059"]
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
notes: "Subcluster D — Restaurants / QSR (adjacent peer)"
```

---

## Benchmark Context Records (3)

### Record 17: XRT (SPDR S&P Retail ETF)

```yaml
candidate_record_id: PGF05-BMK-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: SPDR S&P Retail ETF
asset_type: etf
object_type: etf
legal_entity_name: SPDR S&P Retail ETF
instrument_type: etf
ticker_candidates: ["XRT"]
ISIN_candidates: ["US78464A8707"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "benchmark_context"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: benchmark_context
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
notes: "Benchmark context — S&P Retail ETF for sector-level comparison"
```

### Record 18: XLP (Consumer Staples Select Sector SPDR)

```yaml
candidate_record_id: PGF05-BMK-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Consumer Staples Select Sector SPDR
asset_type: etf
object_type: etf
legal_entity_name: Consumer Staples Select Sector SPDR Fund
instrument_type: etf
ticker_candidates: ["XLP"]
ISIN_candidates: ["US81369Y5069"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "benchmark_context"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: benchmark_context
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
notes: "Benchmark context — Consumer Staples sector ETF for broad sector comparison"
```

### Record 19: XLY (Consumer Discretionary Select Sector SPDR)

```yaml
candidate_record_id: PGF05-BMK-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-05
family_name: Consumer / Retail / Event Consumption
asset_name: Consumer Discretionary Select Sector SPDR
asset_type: etf
object_type: etf
legal_entity_name: Consumer Discretionary Select Sector SPDR Fund
instrument_type: etf
ticker_candidates: ["XLY"]
ISIN_candidates: ["US81369Y8030"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: DEC
listing_variant_type: primary
source_authority_status: SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "benchmark_context"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: benchmark_context
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
notes: "Benchmark context — Consumer Discretionary sector ETF for broad sector comparison"
```

---

## Summary

| Category | Count | ID Range |
|----------|-------|----------|
| Core Peers | 11 | PGF05-CORE-001 to PGF05-CORE-011 |
| Adjacent Peers | 5 | PGF05-ADJ-001 to PGF05-ADJ-005 |
| Benchmark Context | 3 | PGF05-BMK-001 to PGF05-BMK-003 |
| **Total** | **19** | |

### Subcluster Distribution

| Subcluster | Description | Core | Adjacent |
|------------|-------------|------|----------|
| A | Retail (Mass / Warehouse) | WMT, COST, TGT | — |
| B | E-Commerce / Omnichannel | AMZN | — |
| C | Consumer Brands / Athletic | NKE, ADS | LULU |
| D | Restaurants / QSR | MCD, QSR, SBUX | CMG |
| E | Consumer Staples / Beverages | KO, PEP | — |
| F | Home Improvement / Specialty Retail | — | TJX, HD, LOW |

---

## Cross-Region Comparability Adjustments

| Ticker | Record ID | Domicile | Accounting | Currency | Adjustment Required |
|--------|-----------|----------|------------|----------|---------------------|
| ADS | PGF05-CORE-006 | DE | IFRS | EUR | Yes — IFRS/EUR vs GAAP/USD peers |

---

## No-Invention Confirmation

All tickers, subclusters, benchmark instruments, and family assignments in this document are sourced exclusively from:

1. `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` — Section 5, Family PGF-05
2. `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` — Source authority references
3. PGMF methodology framework (12/12 tasks, VG-PGMF-1 PASS) — Decision references

No tickers, companies, or peer relationships have been invented or inferred beyond the scope preflight authority.

---

*End of PGF-05 candidate record drafts.*
