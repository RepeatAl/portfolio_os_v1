# Peer Group Registry Methodology Framework — Design

**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: draft — ready for human review

---

## 1. Purpose

This document defines the conceptual architecture of the Peer Group Registry Methodology Framework. It proposes the methodology chain, data model, field taxonomy, and decision rationale for Q1–Q10. It does not define runtime implementation, database schemas, APIs, services, or any executable artifact.

**Boundary**: This design document is a specification-layer artifact. No registry data is created. No implementation code is defined. No SAI artifacts are modified.

---

## 2. Methodology Chain

The methodology chain defines the sequence of decisions and transformations that produce a valid peer group assignment. Every assignment must pass through every step in sequence.

```
1. Evidence Sources (Tier 1 institutional)
        ↓
2. Canonical Entity Identity Resolution
   (canonical_entity_id, ISIN, FIGI, MIC, listing_variant_type)
        ↓
3. Primary Classification Assignment
   (primary_family, revenue_basis, earnings_basis, taxonomy_reference)
        ↓
4. Secondary Family Overlay (optional)
   (secondary_family for cross-family candidates only)
        ↓
5. Peer Role Assignment
   (core_peer / adjacent_peer / benchmark_context /
    excluded_non_peer / private_comparable_context)
        ↓
6. Financial Comparability Gate Assessment
   (business model, market_cap_band, liquidity_band,
    margin, leverage, accounting_standard,
    comparability_adjustment_required)
        ↓
7. Benchmark Context Separation
   (ETFs, indices, sector funds → benchmark_context;
    never mixed into company peer groups)
        ↓
8. Cross-Region Normalization
   (accounting_standard, reporting_currency,
    trading_currency, fiscal_year_end, taxonomy_reference)
        ↓
9. Governance / Versioning
   (effective_date, end_date, approved_by,
    source_authority, review_cycle, lifecycle_status)
        ↓
10. SAI Consumption Contract
    (consumed by SAI-BLK-21 via deferred_interfaces.md Section 2.3)
```

---

## 3. Conceptual Architecture

### 3.1 Three-Layer Model

```
Layer 1 — Economic Entity
    canonical_entity_id (primary key)
    entity_name, domicile, reporting_currency, fiscal_year_end
    accounting_standard, taxonomy_reference

Layer 2 — Security / Listing
    security_id, isin, figi, ticker, exchange_mic
    listing_variant_type (primary / ADR / GDR / secondary)
    trading_currency, adr_flag
    market_data_source, data_vendor, data_latency_class
    exchange_timezone, trading_calendar_id

Layer 3 — Peer Group Assignment
    peer_group_id (future — not assigned in this spec)
    family_id, family_name, primary_family, secondary_family
    subcluster_id, subcluster_name
    peer_role, effective_date, end_date
    financial comparability gate fields
    governance fields
    data model readiness fields
    trading governance reserved fields
```

Layers 1 and 2 form the entity/security identity foundation. Layer 3 is built on top. No Layer 3 assignment is valid without a resolved Layer 1 entity.

### 3.2 Key Architectural Decisions

| Decision | Principle | Rationale |
|----------|-----------|-----------|
| A — Ticker is never a primary key | canonical_entity_id as Layer 1 key | Tickers are unstable; change on relisting/acquisition |
| B — One primary family per entity | GICS/ICB institutional precedent | SAI-BLK-21 requires stable primary anchor |
| C — Peer role is exhaustive and non-overlapping | Five-role taxonomy | Prevents ambiguous peer set queries |
| D — ETF/company boundary enforced at data model level | asset_type required field | Prevents category errors (QQQ vs NVDA as peers) |
| E — Record-level versioning | effective_date / end_date per record | Enables as-of-date historical reproducibility |

---

## 4. Field Taxonomy

### 4.1 Current Methodology Fields (Required in any v1 registry record)

**Entity identity**:

| Field | Type | Description |
|-------|------|-------------|
| `canonical_entity_id` | string | Primary key — stable entity identifier |
| `entity_name` | string | Legal entity name |
| `domicile` | string | Country of incorporation |
| `accounting_standard` | enum | GAAP / IFRS / other |
| `reporting_currency` | string | ISO 4217 code |
| `fiscal_year_end` | string | Month (e.g., DEC, SEP) |
| `taxonomy_reference` | enum | GICS / ICB / other |

**Security / listing identity**:

| Field | Type | Description |
|-------|------|-------------|
| `security_id` | string | Internal security identifier |
| `isin` | string | ISO 6166 ISIN |
| `figi` | string | OpenFIGI Financial Instrument Global Identifier |
| `ticker` | string | Exchange ticker symbol |
| `exchange_mic` | string | ISO 10383 Market Identifier Code |
| `primary_listing` | boolean | Whether this is the primary listing |
| `listing_variant_type` | enum | primary / ADR / GDR / secondary |
| `adr_flag` | boolean | Whether this is an ADR |
| `trading_currency` | string | ISO 4217 code |

**Peer group assignment**:

| Field | Type | Description |
|-------|------|-------------|
| `peer_group_id` | string | Future canonical ID (not assigned in this spec) |
| `family_id` | string | Parent family (e.g., PGF-01) |
| `family_name` | string | Human-readable family name |
| `primary_family` | string | Primary family assignment |
| `secondary_family` | string | Optional — cross-family candidates only |
| `subcluster_id` | string | Subcluster within family |
| `subcluster_name` | string | Human-readable subcluster name |
| `peer_role` | enum | core_peer / adjacent_peer / benchmark_context / excluded_non_peer / private_comparable_context |
| `asset_type` | enum | company / etf / index / fund / private / other |

**Financial comparability gate**:

| Field | Type | Description |
|-------|------|-------------|
| `business_model_similarity` | string | Comparability basis description |
| `market_cap_band` | enum | mega / large / mid / small |
| `liquidity_band` | enum | large_liquid / mid_liquid / small_illiquid / micro_thin |
| `growth_profile_comparable` | boolean | With note if false |
| `margin_structure_comparable` | boolean | With note if false |
| `capital_intensity_comparable` | boolean | With note if false |
| `leverage_comparable` | boolean | With note if false |
| `comparability_adjustment_required` | boolean | True when cross-standard adjustment needed |
| `comparability_note` | string | Explanation of comparability limitations |
| `valuation_peer_allowed` | boolean | False for private_comparable_context |

**ETF/fund-specific** (when `asset_type = etf` or `asset_type = fund`):

| Field | Type | Description |
|-------|------|-------------|
| `benchmark_index` | string | Index tracked |
| `TER` | decimal | Total Expense Ratio |
| `AUM` | decimal | Assets Under Management |
| `tracking_difference` | decimal | Annual fund return minus benchmark return |
| `tracking_error` | decimal | Std dev of daily return differences |
| `spread` | decimal | Bid-ask spread |
| `holdings_overlap` | decimal | Overlap with peer ETFs (0–1) |
| `replication_method` | enum | physical_full / physical_sampled / synthetic |
| `distribution_policy` | enum | accumulating / distributing |
| `lookthrough_concentration` | decimal | Top-10 holdings weight (0–1) |

**Cross-region normalization**:

| Field | Type | Description |
|-------|------|-------------|
| `comparability_adjustment_required` | boolean | (also in gate above) |
| `fiscal_year_end` | string | (also in entity layer) |
| `taxonomy_reference` | enum | GICS / ICB / other |

**Governance / versioning**:

| Field | Type | Description |
|-------|------|-------------|
| `effective_date` | date | Date assignment becomes active |
| `end_date` | date | Supersession date (null = active) |
| `lifecycle_status` | enum | active / deprecated / under_review |
| `review_cycle` | enum | annual / semi_annual / event_triggered |
| `approved_by` | string | Approving authority |
| `source_authority` | string | Source reference supporting assignment |
| `change_reason` | string | Rationale for creation or change |
| `challenge_status` | enum | none / under_review / resolved |
| `review_status` | enum | current / due_for_review / overdue |
| `methodology_version` | string | Version of methodology framework |

### 4.2 Current Data-Model Readiness Fields (Reserved — null in v1)

These fields must exist in the schema to prevent architectural rewrite when market data is integrated. They carry no data in v1.

| Field | Type | Description |
|-------|------|-------------|
| `market_data_source` | string | Exchange origin of price data |
| `data_vendor` | string | Aggregator/distributor |
| `data_latency_class` | enum | real_time / delayed_15min / end_of_day |
| `exchange_timezone` | string | IANA timezone |
| `trading_calendar_id` | string | Exchange trading calendar reference |
| `derived_data_policy` | enum | open / non_display_license_required / restricted |
| `index_license_required` | boolean | Index data license needed |
| `quote_timestamp_required` | boolean | Bid/ask timestamps required |
| `realtime_entitlement_required` | boolean | Real-time entitlement required |
| `display_usage_allowed` | boolean | Data may be displayed without additional license |
| `non_display_usage_allowed` | boolean | Non-display derived analytics licensed |
| `redistribution_allowed` | boolean | Data may be redistributed |

### 4.3 Future Market Data Integration Fields (Placeholder only — not in v1 schema)

| Field | Description | Source |
|-------|-------------|--------|
| `bid_ask_source` | Venue providing bid/ask quotes | SRC-I-02/04/05 |
| `last_trade_timestamp_required` | Last trade timestamp required | SRC-I-04 |
| `professional_user_flag` | Professional vs. non-professional user | SRC-I-04 |
| `market_data_audit_required` | Compliance audit trail for data usage | SRC-I-02 |
| `stale_quote_threshold` | Minutes after which quote is stale | SRC-I-12/13 |
| `market_session_status` | Session state | SRC-I-12/13 |
| `corporate_action_source` | Source for corporate action adjustments | SRC-I-05/13 |

### 4.4 Future Trading Governance Fields (FUTURE_COMPLIANCE_REFERENCE — not in v1 schema)

MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue. These fields are planning references only.

| Field | Source |
|-------|--------|
| `tradability_status` | SRC-I-10/11 |
| `trading_enabled` | SRC-I-10/11 |
| `trade_block_reason` | SRC-I-10 |
| `execution_venue_eligible` | SRC-I-08 |
| `best_execution_required` | SRC-I-08/09 |
| `pre_trade_controls_required` | SRC-I-10/11 |
| `kill_switch_required` | SRC-I-10/11 |
| `audit_log_required` | SRC-I-10/11 |
| `surveillance_required` | SRC-I-10/11 |
| `market_abuse_monitoring_required` | SRC-I-11 |
| `price_collar_policy` | SRC-I-10 |
| `max_order_value_policy` | SRC-I-10 |
| `algo_trading_flag` | SRC-I-11 |
| `manual_trade_only_flag` | SRC-I-10/11 |

---

## 5. Decision Rationale Summary

| Decision | Key Rationale |
|----------|--------------|
| Q1 — Asset-level primary + secondary family | Satisfies GICS/ICB one-primary discipline + Porter cross-family reality; SAI-BLK-21 needs stable primary anchor |
| Q2 — Controlled multi-family (primary + secondary only) | Unlimited multi-tag produces ambiguous peer sets; secondary_family is minimum extension for UBER/AMZN/VRT |
| Q3 — Five-role peer taxonomy | Resolves Porter's direct/substitute/ecosystem distinction; prevents ETF/company mixing; handles private comparables |
| Q4 — canonical_entity_id + FIGI + MIC | Only architecture that handles cross-listed securities, ADRs, and future exchange data without registry rewrite |
| Q5 — ETF/fund boundary enforced in data model | Fundamentally different comparison field set; benchmark_context vs. etf_peer roles prevent category errors |
| Q6 — Soft thresholds for v1 | Principle well-evidenced (Damodaran); numeric cutoffs not yet sourced; flags preserve principle without false precision |
| Q7 — Private comparables: context only in v1 | Evidence insufficient for full methodology; private_comparable_context role reserves conceptual space safely |
| Q8 — Cross-region: flag-based, not blocking | European peers are structurally necessary for PGF-06/07/08; blocking creates coverage gaps; flags document limitation |
| Q9 — Annual + event-triggered governance | GICS/GIPS precedent; challenge_status and review_status fields create formal drift-detection process |
| Q10 — Record-level effective_date/end_date versioning | Minimum standard for historical reproducibility; GICS 2018 reclassification as canonical versioning precedent |

---

## 6. Separation from Registry Creation

This methodology framework is a rules specification. Registry data creation is a separate future task. The gate for registry creation:

1. Human/CTO approval of this methodology framework
2. Registry creation preflight: map 9 family universes to methodology fields
3. Human/CTO approval of candidate registry records
4. Explicit registry creation task execution

---

## 7. SAI Compatibility

SAI-BLK-21 will consume the registry via the existing interface contract in `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` Section 2.3. This design satisfies all elements of that contract without modifying any SAI artifact.

| SAI-BLK-21 expects | This framework provides |
|--------------------|------------------------|
| Canonical peer group definitions per asset | peer_group_id, family_id, subcluster_id, peer_role |
| Peer selection methodology | Financial comparability gate (Section 4.1) |
| Peer rotation rules | review_cycle, event triggers (Section 4.1 governance) |
| Peer group versioning | effective_date, end_date, lifecycle_status (Section 4.1) |
| Peer group validity metadata | review_status, challenge_status, methodology_version |
| Multi-level peer classification | primary_family, secondary_family, peer_role, subcluster |

---

## 8. Explicit Prohibitions

| Prohibition | Reason |
|-------------|--------|
| No ticker-only identity | Tickers are not stable identifiers |
| No ETF/company peer mixing | Category error — fundamentally different comparison logic |
| No raw GAAP/IFRS comparison without adjustment flag | Creates misleading cross-region comparisons |
| No ad-hoc peer groups without registry authorization | Violates SAI architecture |
| No trading enablement in this spec | MoneyHorst is not a regulated trading entity |
| No runtime code | Methodology specification, not implementation |
| No registry data creation | Separate future task |
| No SAI artifact modification | SAI interface contract already declared and correct |

---

*End of design document.*
