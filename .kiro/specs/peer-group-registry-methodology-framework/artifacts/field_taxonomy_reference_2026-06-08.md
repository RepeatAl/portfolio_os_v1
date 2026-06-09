# Peer Group Registry Methodology Framework — Field Taxonomy Reference

**Artifact**: field_taxonomy_reference_2026-06-08.md
**Task**: Task 3 — Create Field Taxonomy Reference
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_3_FIELD_TAXONOMY_READY_FOR_HUMAN_REVIEW

**Purpose**: This document catalogs every field in the Peer Group Registry Methodology Framework, organized by scope classification, with type, allowed values, asset-type applicability, requirement status, and source authority domain for each field.

**Hard boundaries confirmed**:
- No peer_group_registry.yaml created
- No peer assignments made
- No canonical peer_group_id values created
- No SAI artifact modification
- No implementation code
- No market data integration
- No broker, exchange, ATS, or trading venue connection
- No order routing or execution logic

**Carry-forward decisions**:
- `canonical_object_id` is the primary key — NOT canonical_entity_id
- Q6 numeric thresholds: `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED` on all v1 records
- Q7 private comparables: `peer_role = private_comparable_context`, `valuation_peer_allowed = false`, `comparison_mode_allowed = ecosystem_context_only`
- `etf_peer` valid ONLY when `asset_type ∈ {etf, fund}` — company assets NEVER receive `etf_peer`
- ETFs/funds NEVER receive `core_peer` or `adjacent_peer` against company assets
- `benchmark_context` is NOT a valuation peer role
- All trading governance fields are `FUTURE_COMPLIANCE_REFERENCE` — no current legal obligations

---

## Scope Classification Taxonomy

| Scope Label | Meaning |
|-------------|---------|
| `CURRENT_METHODOLOGY` | Required field in any v1 registry record — must be populated |
| `CURRENT_MODEL_NULLABLE` | Must exist in v1 schema; value is null until market data vendor agreement exists |
| `FUTURE_VENDOR_INTEGRATION` | Not in v1 schema; requires active commercial data agreement before population |
| `FUTURE_COMPLIANCE_REFERENCE` | Not in v1 schema; reserved vocabulary only; no current obligations |
| `DEFERRED` | Decision or value deferred — field exists but calibration is incomplete |
| `NOT_APPLICABLE` | Field does not apply to this asset_type |

## Field Requirement Status Taxonomy

| Status | Meaning |
|--------|---------|
| `REQUIRED` | Must be present in every record of this asset_type |
| `REQUIRED_IF_LISTED` | Required when the asset has an active exchange listing |
| `REQUIRED_IF_AVAILABLE` | Best-effort required; gap must be documented if missing |
| `REQUIRED_IF_APPLICABLE` | Required when the field's subject applies to this record |
| `OPTIONAL` | May be present; not required |
| `NOT_APPLICABLE` | Field does not apply to this asset_type or context |
| `FUTURE_SCOPE` | Placeholder reserved; not populated in v1 |

## Asset Type Taxonomy

| asset_type | Description |
|-----------|-------------|
| `company` | Publicly listed equity (the economic entity, not the listing) |
| `etf` | Exchange-traded fund |
| `fund` | Non-ETF investment fund |
| `index` | Market index (S&P 500, Nasdaq-100, DAX, etc.) |
| `private_company` | Non-publicly-listed company or entity |
| `unsupported_asset_class` | Asset that does not fit any v0 peer group family |

---

## Section 1 — Current Methodology Fields

These fields are required in any v1 registry record. They must be populated at the time of record creation.

### 1.1 Layer 1 — Object Identity Fields

| Field | Type | Requirement | Allowed Values / Format | asset_type Applicability | Source Authority Domain | Validation Note |
|-------|------|-------------|------------------------|--------------------------|------------------------|-----------------|
| `canonical_object_id` | string | REQUIRED | Stable internal or external identifier; unique per object | All asset types | identity_authority | Primary key for the entire three-layer model. NOT ticker-only. NOT ISIN. Polymorphic across all object types. |
| `object_type` | enum | REQUIRED | company / etf / fund / index / private_company / unsupported_asset_class / other | All asset types | identity_authority | Determines which other fields apply. Must be consistent with asset_type in Layer 3. |
| `object_name` | string | REQUIRED | Legal entity name or index/fund name | All asset types | identity_authority | Human-readable name; not the primary identity key. |
| `domicile` | string | REQUIRED | ISO 3166-1 alpha-2 country code | company, etf, fund | accounting_authority | Country of incorporation. |
| `reporting_currency` | string | REQUIRED | ISO 4217 currency code | company, etf, fund | accounting_authority | Primary financial reporting currency. Distinct from trading_currency. |
| `fiscal_year_end` | string | REQUIRED | Three-letter month abbreviation (e.g., DEC, SEP) | company | accounting_authority | Fiscal year-end misalignment affects period comparability. |
| `accounting_standard` | enum | REQUIRED | GAAP / IFRS / other | company | accounting_authority | Determines whether comparability_adjustment_required must be true for cross-standard comparison. |
| `taxonomy_reference` | enum | REQUIRED | GICS / ICB / other | company | classification_authority | European assets often ICB; US assets often GICS. GICS and ICB do not map 1:1. |
| `index_provider` | string | REQUIRED_IF_APPLICABLE | Free text (e.g., S&P, MSCI, FTSE Russell, Nasdaq) | index | classification_authority | Required for index object_type. NOT_APPLICABLE for company, etf, fund, private_company. |
| `benchmark_index_id` | string | REQUIRED_IF_APPLICABLE | Stable identifier for the index definition | index | classification_authority | Stable ID for the index definition (distinct from any ETF that tracks it). |

### 1.2 Layer 2 — Security / Listing Identity Fields

| Field | Type | Requirement | Allowed Values / Format | asset_type Applicability | Source Authority Domain | Validation Note |
|-------|------|-------------|------------------------|--------------------------|------------------------|-----------------|
| `security_id` | string | REQUIRED | Stable internal security identifier | company, etf, fund (listed) | identity_authority | Internal security-level ID linking Layer 2 to Layer 1 canonical_object_id. |
| `isin` | string | REQUIRED_IF_AVAILABLE | ISO 6166 format | company, etf, fund | identity_authority (SRC-G-03) | Security-level, NOT object-level. NOT_APPLICABLE for index, private_company. |
| `figi` | string | REQUIRED_IF_AVAILABLE | OpenFIGI 12-character alphanumeric | company, etf, fund | identity_authority (SRC-G-01) | One FIGI per instrument per listing venue. Multiple FIGIs may link to one canonical_object_id. NOT_APPLICABLE for private_company. |
| `ticker` | string | REQUIRED_IF_LISTED | Exchange ticker symbol | company, etf, fund | identity_authority (SRC-G-02) | Not a stable primary key — changes on relisting or acquisition. Must be paired with exchange_mic. |
| `exchange_mic` | string | REQUIRED_IF_LISTED | ISO 10383 four-character MIC (e.g., XNAS, XETR, XAMS, XNYS) | company, etf, fund | identity_authority (SRC-I-01) | Canonical venue identifier. NOT_APPLICABLE for non-exchange-traded index, private_company. |
| `primary_listing` | boolean | REQUIRED_IF_LISTED | true / false | company, etf, fund | identity_authority | Whether this Layer 2 record is the primary listing venue for this object. |
| `listing_variant_type` | enum | REQUIRED_IF_LISTED | primary / ADR / GDR / secondary | company, etf, fund | identity_authority | Type of listing: primary equity, ADR, GDR, or secondary cross-listing. |
| `adr_flag` | boolean | REQUIRED_IF_LISTED | true / false | company | identity_authority | Whether this listing is an ADR for a non-US-domiciled company. NOT_APPLICABLE for etf, fund, index, private_company. |
| `trading_currency` | string | REQUIRED_IF_LISTED | ISO 4217 currency code | company, etf, fund | accounting_authority | Currency in which shares trade at this venue. May differ from reporting_currency. |

### 1.3 Layer 3 — Peer Group Assignment Fields

| Field | Type | Requirement | Allowed Values / Format | asset_type Applicability | Source Authority Domain | Validation Note |
|-------|------|-------------|------------------------|--------------------------|------------------------|-----------------|
| `peer_group_id` | string | OPTIONAL | Future canonical ID — format TBD | All asset types | classification_authority | NOT assigned in this spec. Assigned when Peer Group Registry is created. |
| `family_id` | string | REQUIRED | e.g., PGF-01 through PGF-09 | All asset types | classification_authority | Parent family from the 9 confirmed families. |
| `family_name` | string | REQUIRED | Human-readable family name | All asset types | classification_authority | e.g., "AI Semiconductors / AI Infrastructure" |
| `primary_family` | string | REQUIRED | Family ID | All asset types | classification_authority (SRC-B-01) | One primary_family per canonical_object_id at any given effective_date. Revenue-primary. |
| `secondary_family` | string | OPTIONAL | Family ID | company | strategic_peer_logic_authority (SRC-D-01) | Optional second family for cross-family candidates (UBER, AMZN, VRT). Requires change_reason. NOT_APPLICABLE for etf, fund, index. |
| `subcluster_id` | string | REQUIRED_IF_APPLICABLE | e.g., PGF-01-SC-A | All asset types | classification_authority | Subcluster within family preventing false peer comparisons. |
| `subcluster_name` | string | REQUIRED_IF_APPLICABLE | Human-readable subcluster name | All asset types | classification_authority | e.g., "Semiconductor Design / Fabless" |
| `asset_type` | enum | REQUIRED | company / etf / fund / index / private_company / unsupported_asset_class / other | All asset types | identity_authority | Must be consistent with object_type in Layer 1. Governs which peer_role values are valid. |
| `peer_role` | enum | REQUIRED | See peer_role taxonomy (Section 2.1) | All asset types | strategic_peer_logic_authority (SRC-D-01), financial_comparability_authority (SRC-E-01), ETF_methodology_authority (SRC-F-01) | Exhaustive six-role taxonomy. See hard constraints in Section 2.1. |
| `comparison_mode_allowed` | enum | REQUIRED | See comparison_mode taxonomy (Section 2.2) | All asset types | financial_comparability_authority | Determines what SAI-BLK-21 may produce for this peer. Derived from peer_role. |

---

## Section 2 — Peer Role and Comparison Mode Taxonomy

### 2.1 Peer Role Taxonomy (exhaustive, non-overlapping)

| peer_role | Valid asset_type | comparison_mode_allowed | Definition | Hard Constraints |
|-----------|-----------------|------------------------|-----------|-----------------|
| `core_peer` | company ONLY | valuation_comparison (gate-conditional), operating_metric_comparison, market_behavior_comparison | Direct rival; meets all financial comparability gates | Company assets ONLY. ETFs/funds MUST NEVER receive core_peer against company assets. |
| `adjacent_peer` | company ONLY | operating_metric_comparison, market_behavior_comparison | Partial competitor or substitute; comparability_note REQUIRED | Company assets ONLY. ETFs/funds MUST NEVER receive adjacent_peer against company assets. |
| `benchmark_context` | etf, fund, index, any | benchmark_context_comparison | Reference instrument; NEVER a valuation peer | NOT a valuation peer role. May be assigned to ETFs, indices, sector funds serving as reference instruments. |
| `etf_peer` | etf, fund ONLY | ETF_fund_comparison | Valid ONLY within PGF-09 or ETF/fund comparison logic | ONLY valid when asset_type ∈ {etf, fund}. Company assets MUST NEVER receive etf_peer. |
| `excluded_non_peer` | any | blocked | Explicitly excluded; documented rationale required | Any asset type; requires change_reason documentation. |
| `private_comparable_context` | private_company ONLY | ecosystem_context_only | Non-listed company as competitive context only | ALWAYS: valuation_peer_allowed = false; comparison_mode_allowed = ecosystem_context_only. |

### 2.2 Comparison Mode Taxonomy

| comparison_mode | Permitted peer_role(s) | Description |
|-----------------|----------------------|-------------|
| `valuation_comparison` | core_peer only (all gates pass) | Financial multiple comparison (P/E, EV/EBITDA, P/FCF, P/B) |
| `operating_metric_comparison` | core_peer, adjacent_peer | Revenue growth, margin, return metrics comparison |
| `market_behavior_comparison` | core_peer, adjacent_peer | Relative price performance, beta, correlation |
| `benchmark_context_comparison` | benchmark_context | Benchmark/index reference comparison only |
| `ETF_fund_comparison` | etf_peer | tracking_difference, tracking_error, TER, AUM, domicile comparison |
| `ecosystem_context_only` | private_comparable_context | Competitive landscape context only; no financial metric comparison |
| `blocked` | excluded_non_peer, unsupported assets | No comparison permitted |

---

## Section 3 — Financial Comparability Gate Fields

Gate authority: SRC-E-01, SRC-E-03 (financial_comparability_authority). All gate dimensions must be documented before any peer_role = core_peer assignment. If any dimension produces a material gap, peer_role must be adjacent_peer and comparability_note must be recorded.

| Field | Type | Requirement | Allowed Values / Format | Scope | Validation Note |
|-------|------|-------------|------------------------|-------|-----------------|
| `business_model_similarity` | string | REQUIRED | Free text | CURRENT_METHODOLOGY | Must describe: same product category, similar customer type, similar distribution channel. |
| `market_cap_band` | enum | REQUIRED | mega / large / mid / small / micro / unknown | CURRENT_METHODOLOGY + DEFERRED | Non-canonical illustrative categories — numeric cutoffs NOT finalized in v1. See Q6 validation note. |
| `liquidity_band` | enum | REQUIRED | large_liquid / mid_liquid / small_illiquid / micro_thin / unknown | CURRENT_METHODOLOGY + DEFERRED | Non-canonical illustrative categories — numeric cutoffs NOT finalized in v1. See Q6 validation note. |
| `threshold_calibration_status` | enum | REQUIRED | NUMERIC_THRESHOLDS_DEFERRED | DEFERRED | **Must be NUMERIC_THRESHOLDS_DEFERRED on ALL v1 records.** No hard dollar values are canonical in v1. Numeric calibration requires additional sourcing (Russell/MSCI index construction methodology). |
| `growth_profile_comparable` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | If false, comparability_note must document the growth profile gap. |
| `margin_structure_comparable` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | If false, comparability_note must document the margin structure gap. |
| `capital_intensity_comparable` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | If false, comparability_note must document capital intensity differences. |
| `leverage_comparable` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | If false, comparability_note must document leverage/balance sheet differences. |
| `comparability_adjustment_required` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | True when accounting standard (GAAP vs. IFRS) or other material cross-region difference requires adjustment. When true, comparability_note is mandatory. |
| `comparability_note` | string | REQUIRED_IF_APPLICABLE | Free text | CURRENT_METHODOLOGY | Required whenever comparability_adjustment_required = true OR any gate boolean = false. Documents the specific comparability limitation. |
| `comparability_note_required` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | True when band mismatch between proposed peers is material. Signals that comparability_note must be populated. |
| `valuation_peer_allowed` | boolean | REQUIRED | true / false | CURRENT_METHODOLOGY | Must be false for private_comparable_context. If false, valuation_comparison is blocked for this peer. |
| `financial_comparability_gate_status` | enum | REQUIRED | pass / partial / blocked | CURRENT_METHODOLOGY | Aggregate gate result. pass = all dimensions satisfied; partial = adjacent_peer assignment with comparability_note; blocked = no peer comparison permitted. |

**Q6 Validation Note**: market_cap_band and liquidity_band categorical values are NON-CANONICAL illustrative categories in v1. Hard dollar values (e.g., ">$200B for mega") are explicitly NOT part of this framework v1. threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED is mandatory on all v1 records. Numeric calibration is deferred pending additional sourcing from Russell index methodology and MSCI index construction rules.

---

## Section 4 — ETF / Fund Boundary Fields

These fields apply exclusively when asset_type ∈ {etf, fund}. They support PGF-09 (ETF/Fund Peer Rule) and the etf_peer role.

ETF methodology authority: SRC-F-01 (Morningstar), SRC-F-02 (Columbia Law), SRC-F-03 (etf.com), SRC-F-04 (Morningstar).

| Field | Type | Requirement | Allowed Values / Format | asset_type Applicability | Validation Note |
|-------|------|-------------|------------------------|--------------------------|-----------------|
| `benchmark_index` | string | REQUIRED_IF_APPLICABLE | Index name or stable ID | etf, fund | The index the ETF/fund tracks. Required for tracking_difference and tracking_error comparison. NOT_APPLICABLE for company, private_company. |
| `TER` | decimal | REQUIRED_IF_AVAILABLE | Percentage (e.g., 0.0020 = 0.20%) | etf, fund | Total Expense Ratio. Valid ETF peer comparison requires same benchmark_index. UCITS and 1940-Act domicile variants may have materially different TERs. |
| `AUM` | decimal | REQUIRED_IF_AVAILABLE | Numeric in millions (reporting currency) | etf, fund | Assets Under Management. Scale and liquidity signal for ETF peer comparison. |
| `tracking_difference` | decimal | REQUIRED_IF_AVAILABLE | Percentage; can be negative | etf, fund | Annual fund return minus benchmark return. The most comprehensive ETF cost measure. Distinct from tracking_error. |
| `tracking_error` | decimal | REQUIRED_IF_AVAILABLE | Percentage (annualized) | etf, fund | Standard deviation of daily return differences vs benchmark. A consistency measure, not a cost measure. |
| `spread` | decimal | REQUIRED_IF_AVAILABLE | Percentage or basis points | etf, fund | Bid-ask spread. Market microstructure quality signal. |
| `holdings_overlap` | decimal | REQUIRED_IF_AVAILABLE | 0.0 to 1.0 | etf, fund | Overlap with other ETFs covering the same theme. Hidden concentration risk indicator. |
| `replication_method` | enum | REQUIRED_IF_AVAILABLE | physical_full / physical_sampled / synthetic | etf, fund | Physical full: holds all index constituents. Physical sampled: representative subset. Synthetic: uses swaps. |
| `distribution_policy` | enum | REQUIRED_IF_AVAILABLE | accumulating / distributing | etf, fund | Accumulating: reinvests dividends. Distributing: pays dividends to holders. |
| `lookthrough_concentration` | decimal | REQUIRED_IF_AVAILABLE | 0.0 to 1.0 | etf, fund | Top-10 holdings weight. Single-name concentration look-through measure. |

**ETF/Fund Boundary Validation Notes**:
- etf_peer role is ONLY valid when asset_type ∈ {etf, fund}
- ETFs/funds with peer_role = benchmark_context appear in company family records as reference instruments — ETF-specific comparison fields are not used in that context
- ETF peer groups are defined by same benchmark_index — same-index ETFs form a natural peer group for tracking_difference comparison
- UCITS vs. 1940-Act domicile variants require explicit domicile field documentation

---

## Section 5 — Cross-Region Normalization Fields

These fields ensure cross-region peers carry explicit flags preventing silent misleading cross-standard comparisons. Required whenever reporting_currency ≠ USD or accounting_standard ≠ GAAP.

Accounting authority: SRC-H-01 (IFRS Foundation), SRC-H-02 (KPMG), SRC-H-03 (PwC). Classification authority: SRC-C-01 (ICB).

| Field | Type | Requirement | Allowed Values / Format | asset_type Applicability | Validation Note |
|-------|------|-------------|------------------------|--------------------------|-----------------|
| `accounting_standard` | enum | REQUIRED | GAAP / IFRS / other | company | Raw GAAP/IFRS comparison without comparability_adjustment_required = true is prohibited. Key differences: R&D capitalization (IFRS allows development phase; GAAP does not), lease accounting differences, LIFO prohibition under IFRS. |
| `reporting_currency` | string | REQUIRED | ISO 4217 | company, etf, fund | Distinct from trading_currency. European peers report in EUR/GBP/SEK/CHF. |
| `trading_currency` | string | REQUIRED_IF_LISTED | ISO 4217 | company, etf, fund | May differ from reporting_currency (e.g., ASML reports in EUR, ADR trades in USD). |
| `fiscal_year_end` | string | REQUIRED | Three-letter month | company | Fiscal year-end misalignment affects period comparability. |
| `taxonomy_reference` | enum | REQUIRED | GICS / ICB / other | company | European assets typically ICB-classified; US assets GICS-classified. Cross-taxonomy reconciliation required. |
| `comparability_adjustment_required` | boolean | REQUIRED | true / false | company | Must be true for all cross-standard (GAAP/IFRS) peer comparisons. When true, comparability_note is mandatory. |
| `comparability_note` | string | REQUIRED_IF_APPLICABLE | Free text | company | Required when comparability_adjustment_required = true. |

---

## Section 6 — Governance and Versioning Fields

These fields ensure all peer assignment records carry full governance metadata and support as-of-date historical reproducibility.

Governance authority: SRC-A-01, SRC-A-02, SRC-A-03 (CFA/GIPS). Classification authority: SRC-B-03 (GICS versioning), SRC-C-01 (ICB challenge/appeal).

| Field | Type | Requirement | Allowed Values / Format | Scope | Validation Note |
|-------|------|-------------|------------------------|-------|-----------------|
| `effective_date` | date | REQUIRED | ISO 8601 (YYYY-MM-DD) | CURRENT_METHODOLOGY | Date the assignment becomes active. Every record must carry this field. No record without effective_date is valid. |
| `end_date` | date | OPTIONAL | ISO 8601 or null | CURRENT_METHODOLOGY | Null = currently active. Non-overlap property: active records for same canonical_object_id + family_id MUST NOT have overlapping date ranges. Gaps are allowed when documented. |
| `lifecycle_status` | enum | REQUIRED | active / deprecated / under_review | CURRENT_METHODOLOGY | active = currently valid; deprecated = superseded; under_review = event trigger active. |
| `review_cycle` | enum | REQUIRED | annual / semi_annual / event_triggered | CURRENT_METHODOLOGY | Event triggers: material M&A, revenue mix shift >30%, business model restructuring, primary listing change, accounting standard change. |
| `approved_by` | string | REQUIRED | Role or identifier | CURRENT_METHODOLOGY | Who approved this assignment. Required on all records. |
| `source_authority` | string | REQUIRED | Source reference | CURRENT_METHODOLOGY | Which source supports the primary_family assignment (e.g., SRC-B-01 GICS, SRC-D-01 Porter). |
| `change_reason` | string | OPTIONAL | Free text | CURRENT_METHODOLOGY | Rationale for a new versioned record or secondary_family rationale on initial assignment. |
| `challenge_status` | enum | REQUIRED | none / under_review / resolved | CURRENT_METHODOLOGY | Formal challenge/appeal process status (ICB-style governance). |
| `review_status` | enum | REQUIRED | current / due_for_review / overdue | CURRENT_METHODOLOGY | Whether this assignment has been reviewed within its review_cycle schedule. |
| `methodology_version` | string | REQUIRED | Semantic version (e.g., v1.0.0) | CURRENT_METHODOLOGY | Version of the methodology framework under which this record was created. All v1 records carry the current framework version. |

**Versioning Non-Overlap Validation Note**: Active version records for any canonical_object_id + family_id combination MUST NOT overlap in time. Two records with the same canonical_object_id + family_id that are both active (end_date = null) at the same point in time is invalid. Gaps are allowed — but only when lifecycle_status, blocked_reason, or unsupported_status documents why no active peer assignment exists for that period.

---

## Section 7 — Unsupported Asset Class Fields

| Field | Type | Requirement | Allowed Values / Format | asset_type Applicability | Validation Note |
|-------|------|-------------|------------------------|--------------------------|-----------------|
| `unsupported_status` | enum | REQUIRED_IF_APPLICABLE | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION / PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON / null | unsupported_asset_class | When non-null, peer_comparison_allowed MUST be false and peer_group_available MUST be false. |
| `peer_comparison_allowed` | boolean | REQUIRED | true / false | All asset types | false when: unsupported_status is non-null, or peer_group_available = false. SAI-BLK-21 must degrade gracefully when false. |
| `peer_group_available` | boolean | REQUIRED | true / false | All asset types | false when no canonical peer group definition exists. Triggers standard deferred_dependency_notes in SAI-BLK-21. |
| `blocked_reason` | string | REQUIRED_IF_APPLICABLE | Free text | All asset types | Required when peer_comparison_allowed = false. Documents the specific reason. |

**Q7 Validation Note**: Private companies receive peer_role = private_comparable_context, valuation_peer_allowed = false, comparison_mode_allowed = ecosystem_context_only. These constraints are fixed and cannot be overridden in v1. Full private comparable methodology is deferred (EVIDENCE_INSUFFICIENT). Private companies use an internally assigned canonical_object_id only — no FIGI, ISIN, or exchange_mic.

---

## Section 8 — Market Data Readiness Fields (CURRENT_MODEL_NULLABLE)

These fields MUST EXIST in the v1 registry schema with null values. They are structural placeholders to prevent architectural rewrite when market data is added later.

Source authorities: SRC-I-01 (ISO MIC), SRC-I-02/03/04/05 (exchange licensing), SRC-I-06 (LSEG data vendor), SRC-I-07 (Euronext non-display policy).

| Field | Type | v1 Value | asset_type Applicability | Why It Must Exist Now |
|-------|------|----------|--------------------------|----------------------|
| `exchange_mic` | string | null | company, etf, fund (listed) | Cross-listing normalization: ASML on XAMS vs. XNAS are distinct listings of one object. Without this, the registry breaks when quote data is added. |
| `market_data_source` | string | null | company, etf, fund (listed) | Exchange origin of price data — distinct from data_vendor. Must be separate fields. |
| `data_vendor` | string | null | company, etf, fund (listed) | Data aggregator/distributor — distinct from market_data_source. |
| `data_latency_class` | enum | null | company, etf, fund (listed) | Declares data freshness class at record level (real_time / delayed_15min / end_of_day). |
| `exchange_timezone` | string | null | company, etf, fund (listed) | Quote timestamp normalization: XETR (CET) and XNAS (ET) timestamps cannot be compared without this. |
| `trading_calendar_id` | string | null | company, etf, fund (listed) | Quote staleness calculation requires session boundary knowledge. |
| `derived_data_policy` | enum | null | etf, fund, index | Whether analytics derived from this data require non-display license (open / non_display_license_required / restricted). |
| `index_license_required` | boolean | null | index, etf | Prevents unlicensed index data consumption. |

---

## Section 9 — Future Vendor Integration Fields (FUTURE_VENDOR_INTEGRATION)

Not in v1 schema. Require active commercial data vendor agreements before population.

| Field | Description | Activation Condition |
|-------|-------------|---------------------|
| `realtime_entitlement_required` | Whether real-time entitlement is required for this asset | Active real-time data contract per exchange |
| `display_usage_allowed` | Whether data may be displayed to users without additional license | Explicit display usage license per exchange |
| `non_display_usage_allowed` | Whether non-display derived analytics usage is licensed | Explicit non-display/derived-data license |
| `redistribution_allowed` | Whether data may be redistributed to third parties | Redistribution authorization per exchange |
| `professional_user_flag` | Professional vs. non-professional user classification | User classification infrastructure |
| `market_data_audit_required` | Whether compliance audit trail for data usage is required | Audit and compliance reporting infrastructure |
| `bid_ask_source` | Venue providing bid/ask quote data | Live feed subscription |
| `stale_quote_threshold` | Minutes after which a quote is considered stale | Session-aware data infrastructure |
| `quote_timestamp_required` | Whether bid/ask timestamps must be stored | Feed integration before timestamps can be stored |

---

## Section 10 — Future Trading Governance Fields (FUTURE_COMPLIANCE_REFERENCE)

**Boundary statement**: These fields are reserved in methodology vocabulary only. NOT part of v1 registry schema. NOT populated. NOT operational. Create NO current legal obligations.

MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue. Regulatory references are FUTURE_COMPLIANCE_REFERENCE only.

Source authorities (future_trading_reference domain): SRC-I-08 (ESMA MiFID II Art.27), SRC-I-09 (FINRA Rule 5310), SRC-I-10 (SEC Rule 15c3-5), SRC-I-11 (ESMA MiFID II RTS 6).

| Field | Regulatory Reference | Activation Condition |
|-------|---------------------|---------------------|
| `tradability_status` | SRC-I-10/11 | Asset-level trading enablement |
| `trading_enabled` | SRC-I-10/11 | Trading system implementation |
| `trade_block_reason` | SRC-I-10 | Restricted security list maintenance |
| `execution_venue_eligible` | SRC-I-08 (MiFID II Art.27) | EU order routing implementation |
| `best_execution_required` | SRC-I-08/09 (MiFID II / FINRA 5310) | Client order routing implementation |
| `order_routing_policy_required` | SRC-I-08/09 | Order routing implementation |
| `pre_trade_controls_required` | SRC-I-10/11 (SEC 15c3-5 / RTS 6) | Electronic market access |
| `price_collar_policy` | SRC-I-10 | Pre-trade risk controls |
| `max_order_value_policy` | SRC-I-10 | Pre-trade risk controls |
| `kill_switch_required` | SRC-I-10/11 | Automated trading |
| `audit_log_required` | SRC-I-10/11 | Any regulated activity commencement |
| `surveillance_required` | SRC-I-10/11 | Market access implementation |
| `market_abuse_monitoring_required` | SRC-I-11 (MiFID II RTS 6) | Algorithmic trading |
| `algo_trading_flag` | SRC-I-11 | Algorithmic strategies deployment |
| `manual_trade_only_flag` | SRC-I-10/11 | Manual-only execution enforcement |

---

## Section 11 — SAI Output Contract Fields

Fields produced by the Peer Group Registry and consumed by SAI-BLK-21. Documented as the output interface the registry will eventually expose.

| Field | Type | Description | Scope |
|-------|------|-------------|-------|
| `peer_group_available` | boolean | Whether a canonical peer group exists for this asset | CURRENT_METHODOLOGY |
| `peer_comparison_allowed` | boolean | Whether SAI-BLK-21 may perform peer-relative interpretation | CURRENT_METHODOLOGY |
| `blocked_reason` | string | Why peer comparison is blocked (if applicable) | CURRENT_METHODOLOGY |
| `unsupported_status` | enum | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION / PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON / null | CURRENT_METHODOLOGY |
| `core_peer_set` | list | canonical_object_id values with peer_role = core_peer | CURRENT_METHODOLOGY |
| `adjacent_peer_set` | list | canonical_object_id values with peer_role = adjacent_peer | CURRENT_METHODOLOGY |
| `benchmark_context_set` | list | canonical_object_id values with peer_role = benchmark_context | CURRENT_METHODOLOGY |
| `etf_peer_set` | list | canonical_object_id values for ETF/fund objects (PGF-09 only) | CURRENT_METHODOLOGY |
| `comparison_mode_allowed` | enum | Which comparison types are permitted for this asset | CURRENT_METHODOLOGY |
| `financial_comparability_gate_status` | enum | pass / partial / blocked | CURRENT_METHODOLOGY |
| `comparability_note` | string | Adjustment notes for cross-region or adjacent peers | CURRENT_METHODOLOGY |
| `data_quality_status` | enum | Completeness of peer data for this asset | CURRENT_METHODOLOGY |
| `as_of_date` | date | ISO 8601 date for which this peer definition is valid | CURRENT_METHODOLOGY |
| `methodology_version` | string | Version of the methodology framework used | CURRENT_METHODOLOGY |

**SAI graceful degradation**: When peer_group_available = false or peer_comparison_allowed = false, SAI-BLK-21 must produce: `"Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."`

---

## Section 12 — Scope Classification Summary

| Scope | Count | Key Fields |
|-------|-------|-----------|
| CURRENT_METHODOLOGY | ~60 fields | All Layer 1/2/3 fields, gate fields, governance fields, SAI output contract fields |
| CURRENT_MODEL_NULLABLE | 8 fields | exchange_mic, exchange_timezone, trading_calendar_id, market_data_source, data_vendor, data_latency_class, derived_data_policy, index_license_required |
| FUTURE_VENDOR_INTEGRATION | 9 fields | realtime_entitlement_required, display_usage_allowed, non_display_usage_allowed, redistribution_allowed, professional_user_flag, market_data_audit_required, bid_ask_source, stale_quote_threshold, quote_timestamp_required |
| FUTURE_COMPLIANCE_REFERENCE | 15 fields | tradability_status, trading_enabled, trade_block_reason, execution_venue_eligible, best_execution_required, order_routing_policy_required, pre_trade_controls_required, price_collar_policy, max_order_value_policy, kill_switch_required, audit_log_required, surveillance_required, market_abuse_monitoring_required, algo_trading_flag, manual_trade_only_flag |
| DEFERRED | 1 field (fixed value) | threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED on all v1 records |

---

## Section 13 — Asset-Type Applicability Summary

| Field | company | etf | fund | index | private_company | unsupported |
|-------|---------|-----|------|-------|-----------------|-------------|
| `canonical_object_id` | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| `isin` | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `figi` | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `ticker` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `exchange_mic` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `accounting_standard` | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| `reporting_currency` | REQUIRED | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| `peer_role` | core_peer / adjacent_peer / benchmark_context / excluded_non_peer | etf_peer / benchmark_context / excluded_non_peer | etf_peer / benchmark_context / excluded_non_peer | benchmark_context ONLY | private_comparable_context ONLY | excluded_non_peer / null |
| `benchmark_index` | NOT_APPLICABLE | REQUIRED_IF_APPLICABLE | REQUIRED_IF_APPLICABLE | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE |
| `TER, tracking_difference, tracking_error` | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `comparability_adjustment_required` | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `secondary_family` | OPTIONAL | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `unsupported_status` | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | REQUIRED |
| `market_data fields (Section 8)` | CURRENT_MODEL_NULLABLE | CURRENT_MODEL_NULLABLE | CURRENT_MODEL_NULLABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |

---

## Artifact Status

```
PGMF_TASK_3_FIELD_TAXONOMY_READY_FOR_HUMAN_REVIEW
```

---

*End of field taxonomy reference document.*
