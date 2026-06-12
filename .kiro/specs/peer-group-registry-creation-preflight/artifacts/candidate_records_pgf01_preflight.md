# Candidate Record Drafts — PGF-01: AI Semiconductors / AI Infrastructure

> **Peer Group Registry Creation Preflight — Task 10: Candidate Record Drafts**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true
> family_id: PGF-01 | family_name: AI Semiconductors / AI Infrastructure

---

## Document Boundary

This artifact contains non-production candidate record drafts for PGF-01 only. No record constitutes a production registry entry, final peer assignment, or canonical peer_group_id. All tickers, subclusters, and benchmark instruments are sourced exclusively from the scope preflight document.

---

## Source Authority

- **Family/ticker authority**: `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5, Family PGF-01
- **Methodology authority**: PGMF (12/12 tasks, VG-PGMF-1 PASS)
- **Source registry**: `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`

---

## Core Candidate Records (11)

### Record 1: NVDA (NVIDIA Corporation)

```yaml
candidate_record_id: PGF01-CORE-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: NVIDIA Corporation
asset_type: company
object_type: company
legal_entity_name: NVIDIA Corporation
instrument_type: equity
ticker_candidates: ["NVDA"]
ISIN_candidates: ["US67066G1040"]
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
  - {source_id: "SRC-E-01", authority_domain: "financial_comparability_authority", tier_level: "Tier 1", field_name: "valuation_peer_allowed"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
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
notes: "Subcluster A — Semiconductor Design / Fabless"
```

### Record 2: AVGO (Broadcom Inc.)

```yaml
candidate_record_id: PGF01-CORE-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Broadcom Inc.
asset_type: company
object_type: company
legal_entity_name: Broadcom Inc.
instrument_type: equity
ticker_candidates: ["AVGO"]
ISIN_candidates: ["US11135F1012"]
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: OCT
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
notes: "Subcluster assignment open — AVGO spans A/B (diversified semiconductors + software). Unresolved decision from scope preflight."
```

### Record 3: AMD (Advanced Micro Devices, Inc.)

```yaml
candidate_record_id: PGF01-CORE-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Advanced Micro Devices, Inc.
asset_type: company
object_type: company
legal_entity_name: Advanced Micro Devices, Inc.
instrument_type: equity
ticker_candidates: ["AMD"]
ISIN_candidates: ["US0079031078"]
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
notes: "Subcluster A — Semiconductor Design / Fabless"
```


### Record 4: MRVL (Marvell Technology, Inc.)

```yaml
candidate_record_id: PGF01-CORE-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Marvell Technology, Inc.
asset_type: company
object_type: company
legal_entity_name: Marvell Technology, Inc.
instrument_type: equity
ticker_candidates: ["MRVL"]
ISIN_candidates: ["US5738741041"]
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
notes: "Subcluster A — Semiconductor Design / Fabless"
```

### Record 5: MU (Micron Technology, Inc.)

```yaml
candidate_record_id: PGF01-CORE-005
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Micron Technology, Inc.
asset_type: company
object_type: company
legal_entity_name: Micron Technology, Inc.
instrument_type: equity
ticker_candidates: ["MU"]
ISIN_candidates: ["US5951121038"]
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
notes: "Subcluster assignment open — MU may span A/B. Unresolved decision from scope preflight."
```

### Record 6: TSM (Taiwan Semiconductor Manufacturing Company)

```yaml
candidate_record_id: PGF01-CORE-006
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Taiwan Semiconductor Manufacturing Company
asset_type: company
object_type: company
legal_entity_name: Taiwan Semiconductor Manufacturing Company Limited
instrument_type: adr
ticker_candidates: ["TSM"]
ISIN_candidates: ["US8740391003"]
exchange_candidates: ["XNYS"]
region: Asia-Pacific
domicile: TW
reporting_currency: TWD
trading_currency: USD
accounting_standard: IFRS
fiscal_year_end: DEC
listing_variant_type: ADR
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
comparability_note: "IFRS reporting in TWD; US ADR traded in USD. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster B — Semiconductor Manufacturing / Equipment. Cross-region: Taiwan-listed / NYSE ADR."
```

### Record 7: ASML (ASML Holding N.V.)

```yaml
candidate_record_id: PGF01-CORE-007
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: ASML Holding N.V.
asset_type: company
object_type: company
legal_entity_name: ASML Holding N.V.
instrument_type: adr
ticker_candidates: ["ASML"]
ISIN_candidates: ["USN070592100"]
exchange_candidates: ["XNAS"]
region: Europe
domicile: NL
reporting_currency: EUR
trading_currency: USD
accounting_standard: IFRS
fiscal_year_end: DEC
listing_variant_type: ADR
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
comparability_note: "IFRS reporting in EUR; Nasdaq ADR traded in USD. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster B — Semiconductor Manufacturing / Equipment. Cross-region: Amsterdam-listed / Nasdaq ADR."
```

### Record 8: AMAT (Applied Materials, Inc.)

```yaml
candidate_record_id: PGF01-CORE-008
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Applied Materials, Inc.
asset_type: company
object_type: company
legal_entity_name: Applied Materials, Inc.
instrument_type: equity
ticker_candidates: ["AMAT"]
ISIN_candidates: ["US0382221051"]
exchange_candidates: ["XNAS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: OCT
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
notes: "Subcluster B — Semiconductor Manufacturing / Equipment"
```


### Record 9: LRCX (Lam Research Corporation)

```yaml
candidate_record_id: PGF01-CORE-009
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Lam Research Corporation
asset_type: company
object_type: company
legal_entity_name: Lam Research Corporation
instrument_type: equity
ticker_candidates: ["LRCX"]
ISIN_candidates: ["US5128071082"]
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
notes: "Subcluster B — Semiconductor Manufacturing / Equipment"
```

### Record 10: KLAC (KLA Corporation)

```yaml
candidate_record_id: PGF01-CORE-010
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: KLA Corporation
asset_type: company
object_type: company
legal_entity_name: KLA Corporation
instrument_type: equity
ticker_candidates: ["KLAC"]
ISIN_candidates: ["US4824801009"]
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
notes: "Subcluster B — Semiconductor Manufacturing / Equipment"
```

### Record 11: ARM (Arm Holdings plc)

```yaml
candidate_record_id: PGF01-CORE-011
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Arm Holdings plc
asset_type: company
object_type: company
legal_entity_name: Arm Holdings plc
instrument_type: adr
ticker_candidates: ["ARM"]
ISIN_candidates: ["US0420682058"]
exchange_candidates: ["XNAS"]
region: Europe
domicile: GB
reporting_currency: USD
trading_currency: USD
accounting_standard: IFRS
fiscal_year_end: MAR
listing_variant_type: ADR
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "primary_family"}
  - {source_id: "SRC-G-01", authority_domain: "identity_authority", tier_level: "Tier 1", field_name: "canonical_object_id"}
  - {source_id: "SRC-D-01", authority_domain: "strategic_peer_logic_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-H-01", authority_domain: "accounting_authority", tier_level: "Tier 1", field_name: "accounting_standard"}
methodology_decision_references: ["PGMF-DEC-01", "PGMF-DEC-02", "PGMF-DEC-03", "PGMF-DEC-04", "PGMF-DEC-06", "PGMF-DEC-08"]
field_taxonomy_mapping_status: COMPLETE
peer_role: core_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: true
comparability_note: "IFRS reporting; UK-domiciled / Nasdaq ADR traded in USD. Reports in USD but IFRS accounting standard differs from GAAP peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster A — Semiconductor Design / Fabless. IP licensing business model. Unresolved: whether ARM is primary or adjacent per scope preflight."
```

---

## Adjacent Candidate Records (4)

### Record 12: SMCI (Super Micro Computer, Inc.)

```yaml
candidate_record_id: PGF01-ADJ-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Super Micro Computer, Inc.
asset_type: company
object_type: company
legal_entity_name: Super Micro Computer, Inc.
instrument_type: equity
ticker_candidates: ["SMCI"]
ISIN_candidates: ["US86800U1043"]
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
notes: "Subcluster C — AI Infrastructure / Data Center Adjacent. Unresolved: whether SMCI belongs in PGF-01 or PGF-07."
```

### Record 13: DELL (Dell Technologies Inc.)

```yaml
candidate_record_id: PGF01-ADJ-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Dell Technologies Inc.
asset_type: company
object_type: company
legal_entity_name: Dell Technologies Inc.
instrument_type: equity
ticker_candidates: ["DELL"]
ISIN_candidates: ["US24703L2025"]
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
notes: "Subcluster C — AI Infrastructure / Data Center Adjacent"
```

### Record 14: HPE (Hewlett Packard Enterprise Company)

```yaml
candidate_record_id: PGF01-ADJ-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Hewlett Packard Enterprise Company
asset_type: company
object_type: company
legal_entity_name: Hewlett Packard Enterprise Company
instrument_type: equity
ticker_candidates: ["HPE"]
ISIN_candidates: ["US42824C1099"]
exchange_candidates: ["XNYS"]
region: North America
domicile: US
reporting_currency: USD
trading_currency: USD
accounting_standard: GAAP
fiscal_year_end: OCT
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
notes: "Subcluster C — AI Infrastructure / Data Center Adjacent"
```

### Record 15: VRT (Vertiv Holdings Co)

```yaml
candidate_record_id: PGF01-ADJ-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
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
notes: "Subcluster C — AI Infrastructure / Data Center Adjacent. Cross-family: VRT also appears in PGF-07 scope."
```

---

## Benchmark Context Records (3)

### Record 16: SOX (PHLX Semiconductor Index)

```yaml
candidate_record_id: PGF01-BMK-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: PHLX Semiconductor Index
asset_type: index
object_type: index
legal_entity_name: null
instrument_type: index
ticker_candidates: ["SOX"]
ISIN_candidates: null
exchange_candidates: null
region: North America
domicile: US
reporting_currency: USD
trading_currency: null
accounting_standard: null
fiscal_year_end: null
listing_variant_type: null
source_authority_status: SOURCE_NOT_APPLICABLE_FOR_CONTEXT_ONLY
source_authority_references:
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "family_id"}
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
notes: "Index — benchmark_context only. Never a peer."
```

### Record 17: SMH (VanEck Semiconductor ETF)

```yaml
candidate_record_id: PGF01-BMK-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: VanEck Semiconductor ETF
asset_type: etf
object_type: etf
legal_entity_name: VanEck Semiconductor ETF
instrument_type: etf
ticker_candidates: ["SMH"]
ISIN_candidates: ["US92189F6867"]
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
notes: "ETF in company family — benchmark_context only per PGMF-DEC-05. Not a company peer."
```

### Record 18: QQQ (Invesco QQQ Trust)

```yaml
candidate_record_id: PGF01-BMK-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-01
family_name: AI Semiconductors / AI Infrastructure
asset_name: Invesco QQQ Trust (Nasdaq-100)
asset_type: etf
object_type: etf
legal_entity_name: Invesco QQQ Trust
instrument_type: etf
ticker_candidates: ["QQQ"]
ISIN_candidates: ["US46090E1038"]
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
notes: "ETF in company family — benchmark_context only per PGMF-DEC-05. Not a company peer."
```

---

## PGF-01 Summary

| Category | Count | Status Distribution |
|----------|-------|---------------------|
| Core candidates | 11 | 11 × CANDIDATE_DRAFT |
| Adjacent candidates | 4 | 4 × CANDIDATE_DRAFT |
| Benchmark context | 3 | 3 × CANDIDATE_CONTEXT_ONLY |
| **Total records** | **18** | |

| Cross-Region Records | Comparability Required |
|---------------------|----------------------|
| TSM (TW/ADR) | Yes — IFRS/TWD vs GAAP/USD |
| ASML (NL/ADR) | Yes — IFRS/EUR vs GAAP/USD |
| ARM (GB/ADR) | Yes — IFRS vs GAAP |

| Unresolved Decisions (from scope preflight) |
|---------------------------------------------|
| AVGO subcluster assignment (A/B span) |
| ARM primary vs. adjacent status |
| SMCI family assignment (PGF-01 vs PGF-07) |
| MU subcluster assignment (A/B span) |

---

## No-Invention Confirmation

- All 11 core tickers from scope preflight: NVDA, AVGO, AMD, MRVL, MU, TSM, ASML, AMAT, LRCX, KLAC, ARM ✓
- All 4 adjacent tickers from scope preflight: SMCI, DELL, HPE, VRT ✓
- All 3 benchmark instruments from scope preflight: SOX, SMH, QQQ ✓
- No new tickers invented ✓
- No new subclusters invented ✓
- No new benchmark instruments invented ✓

---

*End of PGF-01 candidate record drafts.*
