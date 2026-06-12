# Candidate Record Drafts — PGF-08: Banks / Financials

> **Peer Group Registry Creation Preflight — Task 10: Candidate Record Drafts**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true
> family_id: PGF-08 | family_name: Banks / Financials

---

## Document Boundary

This artifact contains non-production candidate record drafts for PGF-08 only. No record constitutes a production registry entry, final peer assignment, or canonical peer_group_id. All tickers, subclusters, and benchmark instruments are sourced exclusively from the scope preflight document.

---

## Source Authority

- **Family/ticker authority**: `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5, Family PGF-08
- **Methodology authority**: PGMF (12/12 tasks, VG-PGMF-1 PASS)
- **Source registry**: `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`

---

## Core Candidate Records (10)

### Record 1: JPM (JPMorgan Chase & Co.)

```yaml
candidate_record_id: PGF08-CORE-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: JPMorgan Chase & Co.
asset_type: company
object_type: company
legal_entity_name: JPMorgan Chase & Co.
instrument_type: equity
ticker_candidates: ["JPM"]
ISIN_candidates: ["US46625H1005"]
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
notes: "Subcluster A — US Money-Center Banks"
```

### Record 2: BAC (Bank of America Corporation)

```yaml
candidate_record_id: PGF08-CORE-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: Bank of America Corporation
asset_type: company
object_type: company
legal_entity_name: Bank of America Corporation
instrument_type: equity
ticker_candidates: ["BAC"]
ISIN_candidates: ["US0605051046"]
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
notes: "Subcluster A — US Money-Center Banks"
```

### Record 3: C (Citigroup Inc.)

```yaml
candidate_record_id: PGF08-CORE-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: Citigroup Inc.
asset_type: company
object_type: company
legal_entity_name: Citigroup Inc.
instrument_type: equity
ticker_candidates: ["C"]
ISIN_candidates: ["US1729674242"]
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
notes: "Subcluster A — US Money-Center Banks"
```

### Record 4: WFC (Wells Fargo & Company)

```yaml
candidate_record_id: PGF08-CORE-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: Wells Fargo & Company
asset_type: company
object_type: company
legal_entity_name: Wells Fargo & Company
instrument_type: equity
ticker_candidates: ["WFC"]
ISIN_candidates: ["US9497461015"]
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
notes: "Subcluster A — US Money-Center Banks"
```

### Record 5: GS (The Goldman Sachs Group, Inc.)

```yaml
candidate_record_id: PGF08-CORE-005
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: The Goldman Sachs Group, Inc.
asset_type: company
object_type: company
legal_entity_name: The Goldman Sachs Group, Inc.
instrument_type: equity
ticker_candidates: ["GS"]
ISIN_candidates: ["US38141G1040"]
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
notes: "Subcluster B — US Investment Banks / Universal Banks"
```

### Record 6: MS (Morgan Stanley)

```yaml
candidate_record_id: PGF08-CORE-006
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: Morgan Stanley
asset_type: company
object_type: company
legal_entity_name: Morgan Stanley
instrument_type: equity
ticker_candidates: ["MS"]
ISIN_candidates: ["US6174464486"]
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
notes: "Subcluster B — US Investment Banks / Universal Banks"
```

### Record 7: SAN (Banco Santander, S.A.)

```yaml
candidate_record_id: PGF08-CORE-007
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: Banco Santander, S.A.
asset_type: company
object_type: company
legal_entity_name: Banco Santander, S.A.
instrument_type: equity
ticker_candidates: ["SAN"]
ISIN_candidates: ["ES0113900J37"]
exchange_candidates: ["XMAD"]
region: Europe
domicile: ES
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
comparability_note: "IFRS reporting in EUR; Madrid-listed. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster C — European Banks. Cross-region: Madrid-listed / BME."
```

### Record 8: BNP (BNP Paribas S.A.)

```yaml
candidate_record_id: PGF08-CORE-008
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: BNP Paribas S.A.
asset_type: company
object_type: company
legal_entity_name: BNP Paribas S.A.
instrument_type: equity
ticker_candidates: ["BNP"]
ISIN_candidates: ["FR0000131104"]
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
notes: "Subcluster C — European Banks. Cross-region: Paris-listed / Euronext."
```

### Record 9: DB (Deutsche Bank AG)

```yaml
candidate_record_id: PGF08-CORE-009
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: Deutsche Bank AG
asset_type: company
object_type: company
legal_entity_name: Deutsche Bank AG
instrument_type: equity
ticker_candidates: ["DB"]
ISIN_candidates: ["DE0005140008"]
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
notes: "Subcluster C — European Banks. Cross-region: Frankfurt-listed / Xetra."
```

### Record 10: UBS (UBS Group AG)

```yaml
candidate_record_id: PGF08-CORE-010
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-08
family_name: Banks / Financials
asset_name: UBS Group AG
asset_type: company
object_type: company
legal_entity_name: UBS Group AG
instrument_type: equity
ticker_candidates: ["UBS"]
ISIN_candidates: ["CH0244767585"]
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
comparability_note: "IFRS reporting in USD; Zurich-listed. Swiss-domiciled, uses IFRS. Cross-region comparability adjustment required vs. GAAP/USD peers."
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Subcluster C — European Banks. Cross-region: Zurich-listed / SIX Swiss Exchange. Unresolved: UBS structural change (Credit Suisse absorption)."
```

---

## Adjacent Candidate Records (0)

> **adjacent_universe_count = 0**. NONE_IN_SOURCE per scope preflight.
> PGF-08 has zero adjacent candidates per scope preflight (adjacent_universe_count = 0).
> No adjacent records to draft.

---

## Benchmark Context Records (4)

### Record 11: XLF (Financial Select Sector SPDR)

```yaml
candidate_record_id: PGF08-BMK-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-08
family_name: Banks / Financials
asset_name: Financial Select Sector SPDR
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

### Record 12: EUFN (iShares MSCI Europe Financials ETF)

```yaml
candidate_record_id: PGF08-BMK-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-08
family_name: Banks / Financials
asset_name: iShares MSCI Europe Financials ETF
asset_type: etf
object_type: etf
legal_entity_name: iShares MSCI Europe Financials ETF
instrument_type: etf
ticker_candidates: ["EUFN"]
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

### Record 13: SX7P (STOXX Europe 600 Banks Index)

```yaml
candidate_record_id: PGF08-BMK-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-08
family_name: Banks / Financials
asset_name: STOXX Europe 600 Banks Index
asset_type: index
object_type: index
legal_entity_name: STOXX Europe 600 Banks Index
instrument_type: index
ticker_candidates: ["SX7P"]
ISIN_candidates: null
exchange_candidates: null
region: Europe
domicile: null
reporting_currency: null
trading_currency: null
accounting_standard: null
fiscal_year_end: null
listing_variant_type: null
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
notes: "INDEX (not ETF) in company family — benchmark_context only per PGMF-DEC-05. Not tradeable; no exchange, ISIN, or trading currency."
```

### Record 14: KRE (SPDR S&P Regional Banking ETF)

```yaml
candidate_record_id: PGF08-BMK-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_CONTEXT_ONLY
family_id: PGF-08
family_name: Banks / Financials
asset_name: SPDR S&P Regional Banking ETF
asset_type: etf
object_type: etf
legal_entity_name: SPDR S&P Regional Banking ETF
instrument_type: etf
ticker_candidates: ["KRE"]
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

## PGF-08 Summary

| Category | Count | Status Distribution |
|----------|-------|---------------------|
| Core candidates | 10 | 10 × CANDIDATE_DRAFT |
| Adjacent candidates | 0 | NONE_IN_SOURCE |
| Benchmark context | 4 | 4 × CANDIDATE_CONTEXT_ONLY |
| **Total records** | **14** | |

| Cross-Region Records | Domicile | Accounting | Reporting Currency | Comparability Required |
|---------------------|----------|------------|-------------------|----------------------|
| SAN (ES) | ES | IFRS | EUR | Yes — IFRS/EUR vs GAAP/USD |
| BNP (FR) | FR | IFRS | EUR | Yes — IFRS/EUR vs GAAP/USD |
| DB (DE) | DE | IFRS | EUR | Yes — IFRS/EUR vs GAAP/USD |
| UBS (CH) | CH | IFRS | USD | Yes — IFRS vs GAAP (Swiss-domiciled, reports in USD) |

---

## No-Invention Confirmation

- All 10 core tickers from scope preflight: JPM, BAC, C, WFC, GS, MS, SAN, BNP, DB, UBS ✓
- Adjacent candidates: 0 (adjacent_universe_count = 0 per scope preflight) ✓
- All 4 benchmark instruments from scope preflight: XLF, EUFN, SX7P, KRE ✓
- No new tickers invented ✓
- No new subclusters invented ✓
- No new benchmark instruments invented ✓

---

*End of PGF-08 candidate record drafts.*
