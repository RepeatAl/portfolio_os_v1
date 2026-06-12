# Candidate Record Drafts — PGF-03: Payments / Networks / Merchant Acquiring

> **Peer Group Registry Creation Preflight — Task 10: Candidate Record Drafts**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true
> family_id: PGF-03 | family_name: Payments / Networks / Merchant Acquiring

---

## Document Boundary

This artifact contains non-production candidate record drafts for PGF-03 only. No record constitutes a production registry entry, final peer assignment, or canonical peer_group_id. All tickers, subclusters, and benchmark instruments are sourced exclusively from the scope preflight document.

---

## Source Authority

- **Family/ticker authority**: `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5, Family PGF-03
- **Methodology authority**: PGMF (12/12 tasks, VG-PGMF-1 PASS)
- **Source registry**: `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`

---

## Core Candidate Records (9)

### Record 1: V (Visa Inc.)

```yaml
candidate_record_id: PGF03-CORE-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Visa Inc.
asset_type: company
object_type: company
legal_entity_name: Visa Inc.
instrument_type: equity
ticker_candidates: ["V"]
ISIN_candidates: ["US92826C8394"]
exchange_candidates: ["XNYS"]
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
notes: "Subcluster A — Card Networks"
```

### Record 2: MA (Mastercard Incorporated)

```yaml
candidate_record_id: PGF03-CORE-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Mastercard Incorporated
asset_type: company
object_type: company
legal_entity_name: Mastercard Incorporated
instrument_type: equity
ticker_candidates: ["MA"]
ISIN_candidates: ["US57636Q1040"]
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
notes: "Subcluster A — Card Networks"
```

### Record 3: AXP (American Express Company)

```yaml
candidate_record_id: PGF03-CORE-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: American Express Company
asset_type: company
object_type: company
legal_entity_name: American Express Company
instrument_type: equity
ticker_candidates: ["AXP"]
ISIN_candidates: ["US0258161092"]
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
notes: "Unresolved: AXP hybrid subcluster assignment (closed-loop network + charge card)."
```

### Record 4: FI (Fiserv, Inc.)

```yaml
candidate_record_id: PGF03-CORE-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Fiserv, Inc.
asset_type: company
object_type: company
legal_entity_name: Fiserv, Inc.
instrument_type: equity
ticker_candidates: ["FI"]
ISIN_candidates: ["US3377381088"]
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
notes: "Subcluster B — Merchant Acquirers / Processors"
```

### Record 5: FIS (Fidelity National Information Services, Inc.)

```yaml
candidate_record_id: PGF03-CORE-005
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Fidelity National Information Services, Inc.
asset_type: company
object_type: company
legal_entity_name: Fidelity National Information Services, Inc.
instrument_type: equity
ticker_candidates: ["FIS"]
ISIN_candidates: ["US31620M1062"]
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
notes: "Subcluster B — Merchant Acquirers / Processors"
```

### Record 6: GPN (Global Payments Inc.)

```yaml
candidate_record_id: PGF03-CORE-006
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Global Payments Inc.
asset_type: company
object_type: company
legal_entity_name: Global Payments Inc.
instrument_type: equity
ticker_candidates: ["GPN"]
ISIN_candidates: ["US37940X1028"]
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
notes: "Subcluster B — Merchant Acquirers / Processors"
```


### Record 7: ADYEN (Adyen N.V.)

```yaml
candidate_record_id: PGF03-CORE-007
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Adyen N.V.
asset_type: company
object_type: company
legal_entity_name: Adyen N.V.
instrument_type: equity
ticker_candidates: ["ADYEN"]
ISIN_candidates: ["NL0012969182"]
exchange_candidates: ["XAMS"]
region: Europe
domicile: NL
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
comparability_note: "IFRS reporting in EUR; Amsterdam-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster B — Merchant Acquirers / Processors. Cross-region: Amsterdam-listed / Euronext."
```

### Record 8: PYPL (PayPal Holdings, Inc.)

```yaml
candidate_record_id: PGF03-CORE-008
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: PayPal Holdings, Inc.
asset_type: company
object_type: company
legal_entity_name: PayPal Holdings, Inc.
instrument_type: equity
ticker_candidates: ["PYPL"]
ISIN_candidates: ["US70450Y1038"]
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
notes: "Subcluster C — Wallets / Consumer Fintech"
```

### Record 9: SQ / Block (Block, Inc.)

```yaml
candidate_record_id: PGF03-CORE-009
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Block, Inc.
asset_type: company
object_type: company
legal_entity_name: Block, Inc.
instrument_type: equity
ticker_candidates: ["SQ"]
ISIN_candidates: ["US8522341036"]
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
notes: "Subcluster C — Wallets / Consumer Fintech. Ticker SQ (Block)."
```

---

## Adjacent Candidate Records (4)

### Record 10: TOST (Toast, Inc.)

```yaml
candidate_record_id: PGF03-ADJ-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Toast, Inc.
asset_type: company
object_type: company
legal_entity_name: Toast, Inc.
instrument_type: equity
ticker_candidates: ["TOST"]
ISIN_candidates: ["US88863U1016"]
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
notes: "Subcluster D — Credit-Sensitive Fintech"
```

### Record 11: AFRM (Affirm Holdings, Inc.)

```yaml
candidate_record_id: PGF03-ADJ-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Affirm Holdings, Inc.
asset_type: company
object_type: company
legal_entity_name: Affirm Holdings, Inc.
instrument_type: equity
ticker_candidates: ["AFRM"]
ISIN_candidates: ["US00827B1061"]
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: JUN
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
notes: "Subcluster D — Credit-Sensitive Fintech. Must not be peer-compared with V or MA without subcluster separation."
```

### Record 12: MELI (MercadoLibre, Inc.)

```yaml
candidate_record_id: PGF03-ADJ-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: MercadoLibre, Inc.
asset_type: company
object_type: company
legal_entity_name: MercadoLibre, Inc.
instrument_type: equity
ticker_candidates: ["MELI"]
ISIN_candidates: ["US58733R1023"]
exchange_candidates: ["XNAS"]
region: Latin America
domicile: UY
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
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
field_taxonomy_mapping_status: COMPLETE
peer_role: adjacent_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: false
comparability_note: "Uruguay-domiciled, Nasdaq-listed, reports in USD under GAAP. No accounting standard difference."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "LatAm-focused. Unresolved: whether MELI requires separate regional subcluster."
```

### Record 13: STNE (StoneCo Ltd.)

```yaml
candidate_record_id: PGF03-ADJ-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: StoneCo Ltd.
asset_type: company
object_type: company
legal_entity_name: StoneCo Ltd.
instrument_type: equity
ticker_candidates: ["STNE"]
ISIN_candidates: ["KY81755Q1070"]
exchange_candidates: ["XNAS"]
region: Latin America
domicile: KY
reporting_currency: BRL
trading_currency: USD
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
comparability_note: "IFRS reporting in BRL; Cayman-domiciled / Nasdaq-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "LatAm-focused. Unresolved: whether STNE requires separate regional subcluster."
```

---

## Benchmark Context Records (2)

### Record 14: IPAY (ETFMG Prime Mobile Payments ETF)

```yaml
candidate_record_id: PGF03-BMK-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: ETFMG Prime Mobile Payments ETF
asset_type: etf
object_type: etf
legal_entity_name: ETFMG Prime Mobile Payments ETF
instrument_type: etf
ticker_candidates: ["IPAY"]
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

### Record 15: XLF (Financial Select Sector SPDR — benchmark context)

```yaml
candidate_record_id: PGF03-BMK-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-03
family_name: Payments / Networks / Merchant Acquiring
asset_name: Financial Select Sector SPDR (broad financials context)
asset_type: etf
object_type: etf
legal_entity_name: Financial Select Sector SPDR Fund
instrument_type: etf
ticker_candidates: ["XLF"]
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

---

## PGF-03 Summary

| Category | Count | Status Distribution |
|----------|-------|---------------------|
| Core candidates | 9 | 9 × CANDIDATE_DRAFT |
| Adjacent candidates | 4 | 4 × CANDIDATE_DRAFT |
| Benchmark context | 2 | 2 × CANDIDATE_CONTEXT_ONLY |
| **Total records** | **15** | |

| Cross-Region Records | Comparability Required |
|---------------------|----------------------|
| ADYEN (NL) | Yes — IFRS/EUR vs GAAP/USD |
| STNE (KY/BRL) | Yes — IFRS/BRL vs GAAP/USD |

---

## No-Invention Confirmation

- All 9 core tickers from scope preflight: V, MA, AXP, FI, FIS, GPN, ADYEN, PYPL, SQ ✓
- All 4 adjacent tickers from scope preflight: TOST, AFRM, MELI, STNE ✓
- All 2 benchmark instruments from scope preflight: IPAY, XLF ✓
- No new tickers invented ✓
- No new subclusters invented ✓
- No new benchmark instruments invented ✓

---

*End of PGF-03 candidate record drafts.*
