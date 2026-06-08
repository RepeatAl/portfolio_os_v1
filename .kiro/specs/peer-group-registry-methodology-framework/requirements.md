# Peer Group Registry Methodology Framework — Requirements

**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: draft — ready for human review
**Branch**: spec/peer-group-registry-methodology-framework

---

## 1. Purpose and Scope

This specification defines the methodology framework that governs how a future Peer Group Registry will be constructed, maintained, versioned, and consumed. It does not create the Peer Group Registry. It does not assign canonical peer groups to assets. It establishes the rules, field taxonomy, governance model, and architectural constraints that any future registry must satisfy.

The framework answers Q1–Q10 canonically, establishes source authority, defines the peer role taxonomy, specifies the entity/security/listing model, sets the ETF/fund/index boundary, addresses cross-region accounting comparability, reserves market data readiness fields, and declares the future trading governance boundary.

### 1.1 Scope

- Methodology rules for peer group organization, membership, role assignment, and versioning
- Field taxonomy: current methodology fields, data-model readiness fields, future market data fields, future trading governance fields
- Governance model: review cycles, change management, audit trail requirements
- Compatibility specification for SAI-BLK-19, SAI-BLK-20, SAI-BLK-21
- Source authority hierarchy
- Unsupported asset class handling rules

### 1.2 Non-Goals

This spec does NOT:

- Create `peer_group_registry.yaml` or any registry data file
- Assign canonical `peer_group_id` values to any asset
- Create final peer groups
- Implement runtime code, services, APIs, or database schemas
- Integrate real-time or delayed market data
- Connect to any broker, exchange, or trading venue
- Create order routing, execution logic, or pre-trade controls
- Claim regulatory compliance or create compliance obligations
- Modify SAI artifacts, SAI gates, or SAI requirements
- Mutate `artifact_registry.yaml` or any SSOT file
- Create scoring, ranking, recommendation, allocation, or trading logic

---

## 2. Evidence Foundation

All decisions in this spec trace to the Peer Group Methodology Source Screening evidence artifacts.

| Artifact | Path | Role |
|----------|------|------|
| Source Registry | `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` | 35 institutional sources across 9 categories |
| Evidence Matrix | `.domainization/reports/peer_group_methodology_evidence_matrix_2026-06-08.md` | Q1–Q10 evidence mapping and readiness status |
| Screening Report | `.domainization/reports/peer_group_methodology_screening_report_2026-06-08.md` | Human-readable synthesis and recommended decisions |
| Market Data Appendix | `.domainization/reports/market_data_exchange_and_trading_readiness_evidence_2026-06-08.md` | Exchange, market data, and trading governance field vocabulary |
| Scope Preflight | `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` | 9 confirmed peer group families (candidate scope) |

---

## 3. Source Authority Hierarchy

| Tier | Definition | Examples | Rule Weight |
|------|-----------|----------|-------------|
| Tier 1 | Official standards, regulatory bodies, internationally recognized methodology publishers | CFA/GIPS, MSCI/GICS, FTSE/ICB, ESMA, SEC, FINRA, IFRS Foundation, ISO, OpenFIGI, KPMG, PwC | Hard rule authority |
| Tier 2 | Institutional research from recognized organizations | Morningstar, Columbia Law, LSEG, Intrinio, etf.com | Supporting evidence |
| Tier 3 | Educational references | Investopedia | Context only — not standalone rule authority |

---

## 4. Methodology Boundary

### 4.1 What This Framework Governs

- How economic entities are identified (canonical_entity_id principle)
- How assets are classified into primary and secondary peer families
- What roles peers may have (core_peer, adjacent_peer, benchmark_context, excluded_non_peer, private_comparable_context)
- What financial comparability gates must be assessed before peer assignment
- How cross-region peers are handled
- How ETFs, funds, and indices are stored separately from company peers
- How peer groups are versioned and reviewed
- What fields are required now vs. reserved for future data or trading integration

### 4.2 What This Framework Does Not Govern

- Which specific companies belong to which specific peer groups
- Which data vendor provides market data
- How SAI calculates peer-relative metrics
- Whether MoneyHorst is a regulated firm (it is not)

---

## 5. Q1–Q10 Canonical Decisions

### PGMF-DEC-01 (Q1) — Peer Group Organization Principle

**Decision**: Asset-level primary organization using `canonical_entity_id` as primary key, with one `primary_family` and optional `secondary_family` overlay.

**Rationale**: GICS (SRC-B-01) and ICB (SRC-C-01) establish one-primary-classification-per-company as the global institutional standard. Porter (SRC-D-01) establishes that competitive context spans multiple arenas, requiring the secondary_family overlay for cross-family candidates such as UBER, AMZN, and VRT. Narrative-level organization is deferred until the Narrative Registry exists.

**Source evidence**: SRC-B-01, SRC-C-01, SRC-D-01

---

### PGMF-DEC-02 (Q2) — Multi-Family Membership

**Decision**: Multi-family membership is allowed only as `primary_family` + optional `secondary_family`. Uncontrolled multi-tag without hierarchy is prohibited.

**Rationale**: SAI-BLK-21 requires a stable primary anchor for peer comparison. Unlimited multi-tagging without hierarchy produces ambiguous peer sets that cannot be consistently consumed. The primary/secondary structure gives SAI a deterministic query path while accommodating cross-family candidates.

**Source evidence**: SRC-B-01 (GICS: one primary classification), SRC-D-01 (Porter: multiple competitive arenas)

---

### PGMF-DEC-03 (Q3) — Peer Role Taxonomy

**Decision**: Every peer assignment must carry exactly one `peer_role` value from the following exhaustive taxonomy:

| peer_role | Definition |
|-----------|-----------|
| `core_peer` | Direct rival; meets all financial comparability gates |
| `adjacent_peer` | Partial competitor or substitute; partially comparable; requires comparability_note |
| `benchmark_context` | ETF, index, or sector fund used as reference instrument; never a company peer |
| `excluded_non_peer` | Explicitly excluded with documented rationale |
| `private_comparable_context` | Non-listed company noted as competitive context only; never used in valuation peer comparison in v1 |

**Source evidence**: SRC-D-01 (Porter), SRC-E-01 (Damodaran), SRC-F-01 (Morningstar ETF)

---

### PGMF-DEC-04 (Q4) — Entity / Security / Listing Identity Model

**Decision**: `canonical_entity_id` is the primary identity key. All listing-level identifiers are attributes of a security/listing record linked to the canonical entity. Ticker-only identity is prohibited.

**Required identity fields**:

| Field | Level | Required |
|-------|-------|----------|
| `canonical_entity_id` | Entity | Yes |
| `security_id` | Security | Yes |
| `isin` | Security | Yes |
| `figi` | Listing | Yes |
| `ticker` | Listing | Yes |
| `exchange_mic` | Listing | Yes |
| `primary_listing` | Entity | Yes |
| `listing_variant_type` | Listing | Yes |
| `adr_flag` | Listing | Conditional |
| `trading_currency` | Listing | Yes |
| `reporting_currency` | Entity | Yes |
| `domicile` | Entity | Yes |

**Source evidence**: SRC-G-01 (OpenFIGI), SRC-G-02 (Intrinio), SRC-G-03 (OpenSanctions), SRC-I-01 (ISO MIC)

---

### PGMF-DEC-05 (Q5) — ETF / Fund / Index Boundary

**Decision**: ETFs and funds are never company peers. They are stored with `asset_type = etf` or `asset_type = fund` and `peer_role = etf_peer` (within PGF-09) or `peer_role = benchmark_context`. Indices are `asset_type = index` and `peer_role = benchmark_context` only.

**Required ETF/fund comparison fields**: `benchmark_index`, `TER`, `AUM`, `tracking_difference`, `tracking_error`, `spread`, `holdings_overlap`, `domicile`, `replication_method`, `distribution_policy`, `lookthrough_concentration`.

**Source evidence**: SRC-F-01 (Morningstar), SRC-F-02 (Columbia Law), SRC-F-03 (etf.com), SRC-F-04 (Morningstar)

---

### PGMF-DEC-06 (Q6) — Liquidity / Market-Cap Thresholds

**Decision**: Soft threshold governance for v1. Use categorical `liquidity_band` and `market_cap_band` fields plus `comparability_note_required` flag. Numeric threshold calibration is deferred — EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED.

**liquidity_band values**: `large_liquid` / `mid_liquid` / `small_illiquid` / `micro_thin`
**market_cap_band values**: `mega` (>$200B) / `large` ($10B–$200B) / `mid` ($2B–$10B) / `small` (<$2B)

**Source evidence**: SRC-E-01 (Damodaran)
**Deferred**: Numeric thresholds pending additional index construction methodology sourcing

---

### PGMF-DEC-07 (Q7) — Private / Non-Listed Comparables

**Decision**: Private comparables are a deferred non-blocking future extension. In v1, private companies may only carry `peer_role = private_comparable_context` and `valuation_peer_allowed = false`. Full private comparable methodology is out of scope for v1.

**Source evidence**: SRC-E-01 (Damodaran), SRC-G-01 (OpenFIGI)
**Deferred**: Full private comparable methodology — EVIDENCE_INSUFFICIENT

---

### PGMF-DEC-08 (Q8) — Cross-Region Peer Handling

**Decision**: Cross-region peers are allowed with explicit normalization fields and flags. Raw GAAP vs. IFRS metric comparison without adjustment is prohibited.

**Required cross-region fields**:

| Field | Description |
|-------|-------------|
| `accounting_standard` | GAAP / IFRS / other |
| `reporting_currency` | ISO 4217 code |
| `trading_currency` | ISO 4217 code |
| `fiscal_year_end` | Month of fiscal year end |
| `taxonomy_reference` | GICS / ICB / other |
| `comparability_adjustment_required` | Boolean — true when cross-standard adjustment is needed |

**Source evidence**: SRC-H-01 (IFRS Foundation), SRC-H-02 (KPMG), SRC-H-03 (PwC), SRC-C-01 (ICB)

---

### PGMF-DEC-09 (Q9) — Subcluster Governance and Validation

**Decision**: Annual review plus event-triggered review. All peer assignment records must carry governance metadata.

**Required governance fields**: `review_cycle`, `effective_date`, `approved_by`, `source_authority`, `change_reason`, `challenge_status`, `review_status`, `lifecycle_status`.

**Event triggers**: material M&A, revenue mix shift >30%, business model restructuring, primary listing change, accounting standard change.

**Source evidence**: SRC-A-01 (GIPS), SRC-B-03 (GICS versioning), SRC-C-01 (ICB challenge/appeal)

---

### PGMF-DEC-10 (Q10) — Peer Group Versioning

**Decision**: Effective_date / end_date versioning at record level. Every membership or role change creates a new versioned record. Historical peer definitions must be reproducible for any past date.

**Required versioning fields**: `effective_date`, `end_date`, `lifecycle_status`, `change_reason`, `methodology_version`.

**Source evidence**: SRC-A-01 (GIPS), SRC-B-01 (GICS), SRC-B-03 (GICS versioning)

---

## 6. Financial Comparability Gate

Before an asset may be assigned `peer_role = core_peer`, the following gate dimensions must be assessed and documented:

| Gate Dimension | Field | Notes |
|----------------|-------|-------|
| Business model similarity | `business_model_similarity` | Same product, customer, distribution |
| Market cap band | `market_cap_band` | Categorical (see PGMF-DEC-06) |
| Liquidity band | `liquidity_band` | Categorical (see PGMF-DEC-06) |
| Growth profile | `growth_profile_comparable` | Boolean with note |
| Margin structure | `margin_structure_comparable` | Boolean with note |
| Capital intensity | `capital_intensity_comparable` | Boolean with note |
| Leverage | `leverage_comparable` | Boolean with note |
| Accounting standard | `accounting_standard` | GAAP / IFRS / other |
| Cross-region adjustment | `comparability_adjustment_required` | Boolean — must be documented |
| Valuation peer allowed | `valuation_peer_allowed` | false for private_comparable_context |

If any gate dimension produces a material comparability gap, `peer_role` must be `adjacent_peer` and a `comparability_note` must be recorded.

Source authority: SRC-E-01 (Damodaran), SRC-E-03 (Damodaran relative valuation)

---

## 7. Unsupported Asset Class Handling

Assets that do not fit any v0 peer group family, or that belong to an asset class requiring different comparison logic, must be classified as:

- `UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION`
- or `PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON`

Ad-hoc peer invention is prohibited. No peer comparison may be performed until scope is defined and approved.

**Asset classes requiring separate future methodology**:

| Asset Class | Status in v1 |
|-------------|-------------|
| Commodities | FUTURE_SCOPE |
| Crypto | FUTURE_SCOPE |
| Bonds / Credit | FUTURE_SCOPE |
| Derivatives / Structured Products | FUTURE_SCOPE |
| FX / Cash | FUTURE_SCOPE |
| Private companies | private_comparable_context only |
| ETFs / Funds | CURRENT_SCOPE — PGF-09 rules |
| Indices | CURRENT_SCOPE — benchmark_context only |

---

## 8. Market Data Readiness Fields

The following fields must be reserved in the registry data model now to prevent architectural rewrite when market data is added. They are NOT currently populated or integrated.

**Scope**: CURRENT_SCOPE_FOR_DATA_MODEL / FUTURE_SCOPE_FOR_VENDOR_INTEGRATION

| Field | Description |
|-------|-------------|
| `exchange_mic` | ISO 10383 MIC for listing venue |
| `market_data_source` | Exchange origin of price data |
| `data_vendor` | Aggregator/distributor (LSEG, Bloomberg, etc.) |
| `data_latency_class` | real_time / delayed_15min / end_of_day |
| `exchange_timezone` | Timezone of primary listing |
| `trading_calendar_id` | Reference to exchange trading calendar |
| `derived_data_policy` | Whether analytics from this data require non-display license |
| `index_license_required` | Whether an index data license is required |
| `quote_timestamp_required` | Whether bid/ask timestamps must be stored |
| `realtime_entitlement_required` | Whether real-time entitlement is required |
| `display_usage_allowed` | Whether data may be displayed without additional license |
| `non_display_usage_allowed` | Whether non-display (derived analytics) usage is licensed |
| `redistribution_allowed` | Whether data may be redistributed |

Source authority: SRC-I-01 (ISO MIC), SRC-I-02 (Euronext), SRC-I-03 (Deutsche Börse), SRC-I-04 (Nasdaq), SRC-I-06 (LSEG), SRC-I-07 (Euronext non-display policy)

---

## 9. Trading Governance Boundary

The following fields are reserved as future trading governance fields only. They create NO current legal obligation.

MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue.

**Scope**: FUTURE_SCOPE_TRADING_GOVERNANCE / FUTURE_COMPLIANCE_REFERENCE / NOT_CURRENT_LEGAL_OBLIGATION

| Field | Source Reference |
|-------|-----------------|
| `execution_venue_eligible` | SRC-I-08 (MiFID II Art.27) |
| `best_execution_required` | SRC-I-08/09 (MiFID II / FINRA 5310) |
| `order_routing_policy_required` | SRC-I-08/09 |
| `pre_trade_controls_required` | SRC-I-10/11 (SEC 15c3-5 / RTS 6) |
| `price_collar_policy` | SRC-I-10 |
| `max_order_value_policy` | SRC-I-10 |
| `kill_switch_required` | SRC-I-10/11 |
| `audit_log_required` | SRC-I-10/11 |
| `surveillance_required` | SRC-I-10/11 |
| `market_abuse_monitoring_required` | SRC-I-11 (MiFID II RTS 6) |
| `tradability_status` | SRC-I-10/11 |
| `trading_enabled` | SRC-I-10/11 |
| `trade_block_reason` | SRC-I-10 |

---

## 10. SAI Compatibility

### 10.1 Affected Blocks

| Block | Impact | Current Status |
|-------|--------|---------------|
| SAI-BLK-19 | Partial — peer-relative strength blocked | Benchmark/sector operational |
| SAI-BLK-20 | Partial — peer correlation blocked | Benchmark/sector operational |
| SAI-BLK-21 | Severe — primary function blocked | No canonical peers |

### 10.2 SAI Interface Contract

The interface contract is already declared in `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` Section 2.3. This methodology framework defines exactly the elements SAI expects to consume. When the registry is created (a future task), it will satisfy the existing SAI interface contract without modifying any SAI artifact.

### 10.3 No-Ad-Hoc-Peer Rule

If no canonical peer group definition exists for an asset, SAI-BLK-21 must produce:

```
deferred_dependency_notes: "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."
```

This rule is absolute and unchanged by this methodology framework.

---

## 11. Future Extension Mechanism

1. All extensions are additive-only. Existing canonical records may not be silently modified.
2. Every extension requires human/CTO approval.
3. New fields must be backward-compatible with existing records.
4. `methodology_version` must be incremented on any material change.
5. Numeric threshold calibration (Q6) requires additional index construction methodology sourcing before becoming a hard rule.
6. Private comparable methodology (Q7) requires a separate evidence sourcing task.

---

*End of requirements document.*
