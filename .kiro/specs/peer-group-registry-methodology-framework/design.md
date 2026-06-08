# Peer Group Registry Methodology Framework — Design

**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: draft — ready for human review after requirements hardening

---

## Overview

This document defines the conceptual architecture of the Peer Group Registry Methodology Framework. It covers the methodology chain, three-layer data model, field taxonomy grouped by scope, decision rationale for Q1–Q10, and the boundary between this methodology framework and the future Peer Group Registry creation task.

This is a specification-layer artifact only. No registry data is created. No runtime code is defined. No SAI artifacts are modified. No market data is integrated. No trading logic is created.

The framework answers how peer groups should be organized, identified, assigned, governed, and versioned — so that when a Peer Group Registry is eventually created, it is built on a sound, institutionally grounded methodology rather than ad-hoc conventions.

**Note**: This design document is pending requirements hardening. The requirements.md v2 hardening patch resolves peer_role taxonomy inconsistency, Q6 numeric threshold contradiction, asset-type-aware field requirements, source authority domain mapping, and SAI output contract strengthening. Design artifacts referencing those decisions will be updated after requirements v2 is approved.

---

## Architecture

### Methodology Chain

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
   (core_peer / adjacent_peer / benchmark_context / etf_peer /
    excluded_non_peer / private_comparable_context)
        ↓
6. Financial Comparability Gate Assessment
   (business model, market_cap_band, liquidity_band,
    margin, leverage, accounting_standard,
    comparability_adjustment_required)
        ↓
7. Benchmark Context and ETF Separation
   (ETFs/funds → etf_peer within PGF-09 or benchmark_context;
    indices → benchmark_context;
    never mixed into company peer groups as core_peer or adjacent_peer)
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

### Three-Layer Model

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
    peer_role, comparison_mode_allowed, effective_date, end_date
    financial comparability gate fields
    governance fields
    data model readiness fields
    trading governance reserved fields
```

Layers 1 and 2 form the entity/security identity foundation. Layer 3 is built on top. No Layer 3 assignment is valid without a resolved Layer 1 entity.

### Key Architectural Decisions

| Decision | Principle | Rationale |
|----------|-----------|-----------|
| A — Ticker is never a primary key | canonical_entity_id as Layer 1 key | Tickers are unstable; change on relisting/acquisition |
| B — One primary family per entity | GICS/ICB institutional precedent | SAI-BLK-21 requires stable primary anchor |
| C — Peer role is exhaustive and non-overlapping | Six-role taxonomy (including etf_peer) | Prevents ambiguous peer set queries and ETF/company mixing |
| D — ETF/company boundary enforced at data model level | asset_type + peer_role constraint | etf_peer only valid when asset_type ∈ {etf, fund} |
| E — Record-level versioning | effective_date / end_date per record | Enables as-of-date historical reproducibility |
| F — Identity fields are asset-type-aware | Field requirements vary by asset_type | Not all instruments have FIGI/ISIN/MIC in all contexts |

---

## Components and Interfaces

### Component 1 — Entity Identity Resolution

**Responsibility**: Resolve a ticker, ISIN, or FIGI reference to a stable canonical_entity_id. Prevent duplicate exposure from cross-listed securities and ADRs.

**Inputs**: ticker, exchange_mic, isin, figi (any combination)
**Outputs**: canonical_entity_id, resolved security_id, primary_listing flag, listing_variant_type

**Interface with Layer 2**: Each listing record (security_id + exchange_mic) maps to exactly one canonical_entity_id. One entity may have multiple listing records (e.g., ASML on XAMS and XNAS).

**Asset-type awareness**: Identity field requirements vary by asset_type. Private companies have no FIGI or exchange_mic. Indices have no ISIN unless the index itself is exchange-traded. See asset-type-aware identity matrix in requirements.md PGMF-DEC-04.

### Component 2 — Primary Classification Engine

**Responsibility**: Assign a primary_family and optional secondary_family to each economic entity, based on revenue-primary classification following GICS/ICB institutional practice.

**Inputs**: canonical_entity_id, principal business activity, revenue_basis, earnings_basis, taxonomy_reference
**Outputs**: primary_family, secondary_family (optional), subcluster_id, subcluster_name

**Classification authority**: GICS (SRC-B-01, SRC-B-02) and ICB (SRC-C-01) — these sources have classification_authority, not general hard-rule authority across all domains.

**Key rule**: One primary_family per entity. Secondary_family is optional and requires documented rationale.

### Component 3 — Peer Role Assignment

**Responsibility**: Assign a peer_role from the exhaustive six-role taxonomy to every peer in an assignment record.

**Inputs**: canonical_entity_id, asset_type, primary_family, financial comparability gate results
**Outputs**: peer_role, comparison_mode_allowed

**Peer role taxonomy** (exhaustive, non-overlapping):

| peer_role | Valid asset_type | comparison_mode_allowed | Definition |
|-----------|-----------------|------------------------|-----------|
| `core_peer` | company | valuation_comparison (if gate passes), operating_metric_comparison, market_behavior_comparison | Direct rival meeting all financial comparability gates |
| `adjacent_peer` | company | operating_metric_comparison, market_behavior_comparison | Partial competitor or substitute; comparability_note required |
| `benchmark_context` | etf, fund, index, company (sector ETF context) | benchmark_context_comparison | Reference instrument; never a company peer |
| `etf_peer` | etf, fund only | ETF_fund_comparison | Valid only within PGF-09 or ETF/fund comparison logic |
| `excluded_non_peer` | any | blocked | Explicitly excluded with documented rationale |
| `private_comparable_context` | private_company | ecosystem_context_only | Non-listed company as competitive context only; valuation_peer_allowed = false |

**Hard constraints**:
- company assets must never receive `etf_peer`
- ETFs/funds must never receive `core_peer` or `adjacent_peer` against company assets
- `etf_peer` is only valid when asset_type ∈ {etf, fund}

### Component 4 — Financial Comparability Gate

**Responsibility**: Assess whether an entity meets the criteria for core_peer assignment. Gate authority: Damodaran/NYU Stern (SRC-E-01, SRC-E-03) — financial_comparability_authority.

**Inputs**: canonical_entity_id, business model, market_cap_band, liquidity_band, growth profile, margin structure, capital intensity, leverage, accounting_standard
**Outputs**: gate_pass (boolean), peer_role recommendation, comparability_note

**Gate dimensions**: business_model_similarity, market_cap_band, liquidity_band, growth_profile_comparable, margin_structure_comparable, capital_intensity_comparable, leverage_comparable, accounting_standard, comparability_adjustment_required, valuation_peer_allowed

**Threshold calibration**: market_cap_band and liquidity_band use categorical values only in v1. Numeric cutoffs are DEFERRED — threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED.

### Component 5 — ETF / Fund Handler (PGF-09)

**Responsibility**: Handle ETF and fund assets using the distinct PGF-09 comparison methodology. Enforce the ETF/company boundary. ETF methodology authority: Morningstar (SRC-F-01), Columbia Law (SRC-F-02).

**Inputs**: asset_type (etf / fund / index), benchmark_index, TER, AUM, tracking_difference, tracking_error, spread, replication_method, domicile, distribution_policy
**Outputs**: peer_role = etf_peer (within PGF-09) or benchmark_context, populated ETF-specific fields

**Interface rule**: No ETF or index record may receive peer_role = core_peer or adjacent_peer within a company peer family. Enforced as a data model constraint on asset_type + peer_role combination.

### Component 6 — Cross-Region Normalization Handler

**Responsibility**: Ensure all cross-region peer records carry the normalization flags required to prevent silent misleading cross-standard comparisons. Accounting authority: IFRS Foundation (SRC-H-01), KPMG (SRC-H-02), PwC (SRC-H-03).

**Inputs**: accounting_standard, reporting_currency, trading_currency, fiscal_year_end, taxonomy_reference
**Outputs**: comparability_adjustment_required flag, normalization metadata

### Component 7 — Governance and Versioning Engine

**Responsibility**: Manage the lifecycle of peer group assignment records. Governance authority analogy: CFA/GIPS (SRC-A-01) — governance_authority.

**Inputs**: assignment record, review trigger event, change_reason, approved_by
**Outputs**: new versioned record with effective_date, deprecation of old record with end_date

**Interface with SAI-BLK-21**: SAI queries must specify an as-of-date to retrieve the correct version of peer definitions.

### Component 8 — SAI Consumption Interface

**Responsibility**: Provide the peer group definitions that SAI-BLK-21, SAI-BLK-19, and SAI-BLK-20 consume. Satisfy the existing interface contract declared in deferred_interfaces.md Section 2.3.

**Future Registry Output Contract for SAI** (fields SAI may expect once registry exists):

| Field | Description |
|-------|-------------|
| `peer_group_available` | Boolean — whether a canonical peer group exists for this asset |
| `peer_comparison_allowed` | Boolean — whether peer comparison may be performed |
| `blocked_reason` | Why peer comparison is blocked (if applicable) |
| `unsupported_status` | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION or null |
| `primary_family` | Primary peer family assignment |
| `secondary_family` | Secondary family (optional) |
| `peer_role` | Role of this asset in the peer set |
| `core_peer_set` | List of canonical_entity_ids with peer_role = core_peer |
| `adjacent_peer_set` | List of canonical_entity_ids with peer_role = adjacent_peer |
| `benchmark_context_set` | List of reference instruments |
| `etf_peer_set` | List of ETF/fund peers (PGF-09 only) |
| `comparison_mode_allowed` | Which comparison types are permitted |
| `financial_comparability_gate_status` | Pass / partial / blocked |
| `comparability_note` | Adjustment notes for cross-region or adjacent peers |
| `data_quality_status` | Completeness of peer data |
| `as_of_date` | Date for which this peer definition is valid |
| `methodology_version` | Version of methodology framework used |

**Graceful degradation**: If peer_group_available = false or peer_comparison_allowed = false, SAI-BLK-21 must degrade gracefully and produce the standard deferred_dependency_notes message. SAI must not create ad-hoc peers.

---

## Data Models

### Entity Record (Layer 1)

```
canonical_entity_id    : string       -- primary key
entity_name            : string
domicile               : string       -- country of incorporation
accounting_standard    : enum         -- GAAP / IFRS / other
reporting_currency     : string       -- ISO 4217
fiscal_year_end        : string       -- month (e.g., DEC, SEP)
taxonomy_reference     : enum         -- GICS / ICB / other
```

### Listing Record (Layer 2) — asset-type-aware requirements

```
security_id            : string       -- REQUIRED for all listed assets
canonical_entity_id    : string       -- REQUIRED for all (FK to entity)
isin                   : string       -- REQUIRED_IF_AVAILABLE (listed company / ETF / fund)
                                     -- NOT_APPLICABLE for index, private_company
figi                   : string       -- REQUIRED_IF_AVAILABLE (listed company / ETF / fund)
                                     -- NOT_APPLICABLE for private_company
ticker                 : string       -- REQUIRED_IF_LISTED
exchange_mic           : string       -- REQUIRED_IF_LISTED (ISO 10383)
                                     -- NOT_APPLICABLE for index (unless exchange-traded product)
                                     -- NOT_APPLICABLE for private_company
primary_listing        : boolean      -- REQUIRED_IF_LISTED
listing_variant_type   : enum         -- primary / ADR / GDR / secondary
adr_flag               : boolean      -- REQUIRED_IF_LISTED
trading_currency       : string       -- REQUIRED_IF_LISTED (ISO 4217)
-- data model readiness fields (null in v1) --
market_data_source     : string       -- FUTURE_SCOPE (listed assets only)
data_vendor            : string       -- FUTURE_SCOPE
data_latency_class     : enum         -- FUTURE_SCOPE
exchange_timezone      : string       -- CURRENT_MODEL (listed assets)
trading_calendar_id    : string       -- CURRENT_MODEL (listed assets)
derived_data_policy    : enum         -- CURRENT_MODEL
index_license_required : boolean      -- CURRENT_MODEL (index / ETF)
```

### Peer Group Assignment Record (Layer 3)

```
-- identity --
peer_group_id          : string       -- future canonical ID (not assigned in this spec)
canonical_entity_id    : string       -- REQUIRED (FK to entity record)
family_id              : string       -- e.g., PGF-01
family_name            : string
primary_family         : string
secondary_family       : string       -- optional
subcluster_id          : string
subcluster_name        : string
peer_role              : enum         -- core_peer / adjacent_peer / benchmark_context /
                                     --   etf_peer / excluded_non_peer / private_comparable_context
asset_type             : enum         -- company / etf / index / fund / private_company /
                                     --   unsupported_asset_class / other
comparison_mode_allowed: enum         -- valuation_comparison / operating_metric_comparison /
                                     --   market_behavior_comparison / benchmark_context_comparison /
                                     --   ETF_fund_comparison / ecosystem_context_only / blocked

-- financial comparability gate --
business_model_similarity         : string
market_cap_band                   : enum    -- mega / large / mid / small / micro / unknown
liquidity_band                    : enum    -- large_liquid / mid_liquid / small_illiquid /
                                           --   micro_thin / unknown
threshold_calibration_status      : enum    -- NUMERIC_THRESHOLDS_DEFERRED (v1)
growth_profile_comparable         : boolean
margin_structure_comparable       : boolean
capital_intensity_comparable      : boolean
leverage_comparable               : boolean
comparability_adjustment_required : boolean
comparability_note                : string
comparability_note_required       : boolean  -- true when band mismatch is material
valuation_peer_allowed            : boolean

-- ETF/fund-specific (when asset_type = etf or fund) --
benchmark_index        : string       -- REQUIRED_IF_APPLICABLE
TER                    : decimal      -- REQUIRED_IF_AVAILABLE
AUM                    : decimal      -- REQUIRED_IF_AVAILABLE
tracking_difference    : decimal      -- REQUIRED_IF_AVAILABLE
tracking_error         : decimal      -- REQUIRED_IF_AVAILABLE
spread                 : decimal      -- REQUIRED_IF_AVAILABLE
holdings_overlap       : decimal      -- REQUIRED_IF_AVAILABLE
replication_method     : enum         -- physical_full / physical_sampled / synthetic
distribution_policy    : enum         -- accumulating / distributing
lookthrough_concentration : decimal   -- REQUIRED_IF_AVAILABLE

-- governance / versioning --
effective_date         : date         -- REQUIRED
end_date               : date         -- null = currently active
lifecycle_status       : enum         -- active / deprecated / under_review
review_cycle           : enum         -- annual / semi_annual / event_triggered
approved_by            : string       -- REQUIRED
source_authority       : string       -- REQUIRED
change_reason          : string
challenge_status       : enum         -- none / under_review / resolved
review_status          : enum         -- current / due_for_review / overdue
methodology_version    : string       -- REQUIRED

-- unsupported asset handling --
unsupported_status     : enum         -- UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION /
                                     --   PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON / null
peer_comparison_allowed: boolean      -- false when unsupported or blocked
peer_group_available   : boolean      -- false when no canonical peer group exists
blocked_reason         : string       -- populated when peer_comparison_allowed = false
```

### Future Trading Governance Fields (FUTURE_COMPLIANCE_REFERENCE — not in v1 schema)

MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue. These fields are planning vocabulary only. Nothing in this framework creates current legal obligations, regulated status, compliance claims, broker-dealer activity, investment-firm activity, exchange participation, order routing, market access, or trading enablement.

```
tradability_status               : enum    -- FUTURE_COMPLIANCE_REFERENCE
trading_enabled                  : boolean -- FUTURE_COMPLIANCE_REFERENCE
trade_block_reason               : string  -- FUTURE_COMPLIANCE_REFERENCE
execution_venue_eligible         : boolean -- FUTURE_COMPLIANCE_REFERENCE
best_execution_required          : boolean -- FUTURE_COMPLIANCE_REFERENCE
pre_trade_controls_required      : boolean -- FUTURE_COMPLIANCE_REFERENCE
kill_switch_required             : boolean -- FUTURE_COMPLIANCE_REFERENCE
audit_log_required               : boolean -- FUTURE_COMPLIANCE_REFERENCE
surveillance_required            : boolean -- FUTURE_COMPLIANCE_REFERENCE
market_abuse_monitoring_required : boolean -- FUTURE_COMPLIANCE_REFERENCE
price_collar_policy              : string  -- FUTURE_COMPLIANCE_REFERENCE
max_order_value_policy           : string  -- FUTURE_COMPLIANCE_REFERENCE
algo_trading_flag                : boolean -- FUTURE_COMPLIANCE_REFERENCE
manual_trade_only_flag           : boolean -- FUTURE_COMPLIANCE_REFERENCE
```

---

## Correctness Properties

The following properties must hold for any valid peer group assignment produced under this methodology framework:

Property 1: Entity identity integrity — Every peer group assignment record must reference a resolved canonical_entity_id. No orphan assignments without a Layer 1 entity record.
**Validates: Requirements 5**

Property 2: One primary family per entity — Each canonical_entity_id has exactly one primary_family at any given effective_date.
**Validates: Requirements 5**

Property 3: Peer role completeness — Every peer group assignment record carries exactly one peer_role value from the six-role taxonomy. Null peer_role is invalid except for unsupported_asset_class records.
**Validates: Requirements 5**

Property 4: ETF/company boundary — No record where asset_type ∈ {etf, fund, index} may carry peer_role = core_peer or adjacent_peer within a company peer family.
**Validates: Requirements 5**

Property 5: etf_peer constraint — peer_role = etf_peer is only valid when asset_type ∈ {etf, fund}. Company assets must never receive etf_peer.
**Validates: Requirements 5**

Property 6: Comparability gate consistency — Any record with peer_role = core_peer must have all comparability gate boolean fields assessed. comparability_adjustment_required = true requires a non-empty comparability_note.
**Validates: Requirements 6**

Property 7: Versioning continuity — For any canonical_entity_id + family_id combination, there must be no gap in the effective_date / end_date sequence.
**Validates: Requirements 5**

Property 8: No ad-hoc peer assignment — Peer group assignments may only be created under this methodology framework with human/CTO approval.
**Validates: Requirements 10.3**

Property 9: Unsupported asset handling — Assets not covered by any v0 family must carry unsupported_status and peer_comparison_allowed = false.
**Validates: Requirements 7**

Property 10: Private comparable isolation — Records with peer_role = private_comparable_context must have valuation_peer_allowed = false and comparison_mode_allowed = ecosystem_context_only.
**Validates: Requirements 5**

Property 11: Threshold calibration transparency — market_cap_band and liquidity_band records in v1 must carry threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED. No record may assert a hard numeric threshold without an updated methodology_version reflecting numeric calibration completion.
**Validates: Requirements 6**

Property 12: Methodology version traceability — Every record must carry the methodology_version of the framework version under which it was created.
**Validates: Requirements 11**

---

## Error Handling

### Unsupported Asset Class

When an asset does not fit any v0 family:
- Set unsupported_status = UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION
- Set peer_comparison_allowed = false
- Set peer_group_available = false
- Record blocked_reason = "Asset class not covered by Peer Group Methodology Framework v0"
- SAI-BLK-21 returns: deferred_dependency_notes = "PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON"

### Missing Canonical Entity ID

When a ticker or ISIN cannot be resolved to a canonical_entity_id:
- Block the peer group assignment
- Flag entity for identity resolution before proceeding
- Ticker-only fallback is prohibited

### Comparability Gate Failure

When the financial comparability gate produces a material gap for a proposed core_peer:
- Downgrade peer_role to adjacent_peer
- Record comparability_note with the specific gate dimension that failed
- Set comparability_note_required = true
- Assignment proceeds as adjacent_peer

### ETF/Company Boundary Violation

When an ETF or index is proposed as core_peer or adjacent_peer in a company family:
- Reject the assignment
- Reassign to peer_role = benchmark_context or etf_peer (PGF-09)
- Record blocked_reason

### Cross-Region Adjustment Required

When comparability_adjustment_required = true:
- Record is valid and may proceed
- SAI-BLK-21 must surface the comparability_note when producing peer-relative observations
- Raw metric comparison without the adjustment note is prohibited

### Peer Group Registry Unavailable

When the Peer Group Registry has not yet been created:
- peer_group_available = false
- peer_comparison_allowed = false
- SAI-BLK-21 produces: "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."

### peer_role / asset_type Constraint Violation

When peer_role = etf_peer is assigned to a company asset, or peer_role = core_peer is assigned to an ETF:
- Reject the record
- Log constraint violation
- Require manual review before any assignment proceeds

---

## Testing Strategy

This is a methodology specification. There is no runtime code to unit-test. Verification covers document completeness and methodology consistency.

### Verification Gate VG-PGMF-1 (Document Completeness)

Verify that all required artifact tasks (Tasks 1–10) are complete. Gate checklist in artifacts/gate_vg_pgmf_1.md.

### Source Traceability Verification (Task 2)

Every PGMF-DEC-XX decision must trace to at least one source within its authoritative domain (classification_authority, governance_authority, financial_comparability_authority, etc.). Verified via artifacts/source_authority_verification_2026-06-08.md.

### Correctness Property Spot-Checks

For each of the 12 correctness properties, verify satisfiability given the data model and methodology rules.

### Peer Role Taxonomy Exhaustiveness

Confirm the six-role taxonomy covers all peer relationship types:
- Direct rival → core_peer
- Substitute / partial competitor → adjacent_peer
- ETF / index / sector fund → benchmark_context or etf_peer
- Explicitly excluded → excluded_non_peer
- Private company context → private_comparable_context
- ETF/fund within PGF-09 → etf_peer

### Cross-Region Normalization Coverage

Confirm every European-listed peer in the 9 confirmed families has a documented exchange_mic, accounting_standard, and comparability_adjustment_required assessment.

### ETF/Company Boundary Enforcement

Confirm no benchmark context instrument appears as core_peer or adjacent_peer in any example.

### Asset-Type Identity Matrix Completeness

Confirm that identity field requirements are defined for all six asset_types (company, etf, fund, index, private_company, unsupported_asset_class).

---

## Decision Rationale Summary

| Decision | Key Rationale |
|----------|--------------|
| Q1 — Asset-level primary + secondary family | Satisfies GICS/ICB one-primary discipline + Porter cross-family reality |
| Q2 — Controlled multi-family | secondary_family is minimum extension for UBER/AMZN/VRT without losing primary anchor |
| Q3 — Six-role peer taxonomy (incl. etf_peer) | etf_peer resolves the PGF-09 inconsistency; comparison_mode_allowed links role to permitted comparisons |
| Q4 — canonical_entity_id + asset-type-aware identity | Not all instruments have FIGI/ISIN/MIC; requirements must reflect this |
| Q5 — ETF/fund boundary enforced in data model | etf_peer constraint on asset_type prevents category errors at schema level |
| Q6 — Soft thresholds, no hard dollar values in v1 | Principle evidenced; numeric calibration requires index construction methodology not yet sourced |
| Q7 — Private comparables: context only | private_comparable_context with ecosystem_context_only prevents false valuation comparison |
| Q8 — Cross-region: flag-based | Flags document limitation without blocking structurally necessary European peers |
| Q9 — Annual + event-triggered governance | GICS/GIPS precedent; challenge_status fields detect drift |
| Q10 — Record-level effective_date/end_date | Minimum standard for as-of-date historical reproducibility |

---

## Explicit Prohibitions

| Prohibition | Reason |
|-------------|--------|
| No ticker-only identity | Tickers are not stable identifiers |
| No ETF/company peer mixing | Category error — etf_peer constraint prevents this at schema level |
| No hard numeric thresholds in v1 | NUMERIC_THRESHOLDS_DEFERRED; illustrative bands only |
| No raw GAAP/IFRS comparison without adjustment flag | Creates misleading cross-region comparisons |
| No ad-hoc peer groups | Violates SAI architecture |
| No trading enablement | MoneyHorst is not a regulated trading entity |
| No runtime code | Methodology specification only |
| No registry data creation | Separate future task |
| No SAI artifact modification | Interface contract already declared and correct |
| No regulatory compliance claim | Regulatory sources used only to reserve future vocabulary |

---

*End of design document.*
