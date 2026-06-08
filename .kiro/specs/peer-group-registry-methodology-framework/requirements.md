# Requirements Document

> **Peer Group Registry Methodology Framework — Requirements v2**
> Spec: peer-group-registry-methodology-framework | Date: 2026-06-08 | Revision: v2 | Authority: CTO / Architecture | Status: hardened — ready for human review

---

## Introduction

This document specifies the methodology framework requirements that govern how a future Peer Group Registry will be constructed, maintained, versioned, and consumed. All decisions trace to institutional evidence sources. No registry data is created by this document. No peer groups are assigned.

---

## 1. Purpose and Scope

This specification defines the methodology framework that governs how a future Peer Group Registry will be constructed, maintained, versioned, and consumed. It does not create the Peer Group Registry. It does not assign canonical peer groups to assets. It establishes the rules, field taxonomy, governance model, and architectural constraints that any future registry must satisfy.

The framework answers Q1–Q10 canonically, establishes source authority by domain, defines the peer role taxonomy, specifies the asset-type-aware entity/security/listing model, sets the ETF/fund/index boundary, addresses cross-region accounting comparability, reserves market data readiness fields, and declares the future trading governance boundary.

### 1.1 Scope

- Methodology rules for peer group organization, membership, role assignment, and versioning
- Field taxonomy: current methodology fields, data-model readiness fields, future market data fields, future trading governance fields
- Governance model: review cycles, change management, audit trail requirements
- Compatibility specification for SAI-BLK-19, SAI-BLK-20, SAI-BLK-21
- Domain-specific source authority hierarchy
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
- Claim regulatory compliance or create current compliance obligations
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

Source authority is domain-specific. A Tier 1 source is authoritative within its domain only. It does not create hard rules outside that domain.

| Authority Domain | Domain | Tier 1 Sources |
|-----------------|--------|----------------|
| `classification_authority` | Peer family and sector classification | GICS (SRC-B-01, SRC-B-02), ICB (SRC-C-01, SRC-C-02) |
| `governance_authority` | Methodology versioning, disclosure, review cycles | CFA/GIPS (SRC-A-01, SRC-A-02, SRC-A-03) |
| `strategic_peer_logic_authority` | Peer role taxonomy, direct vs. substitute vs. ecosystem | Porter / HBR (SRC-D-01) |
| `financial_comparability_authority` | Comparability gates, size/growth/margin/leverage | Damodaran / NYU Stern (SRC-E-01, SRC-E-03) |
| `ETF_methodology_authority` | ETF/fund comparison field set | Morningstar (SRC-F-01, SRC-F-04), Columbia Law (SRC-F-02) |
| `identity_authority` | Canonical entity ID, FIGI, MIC, ISIN | ISO (SRC-I-01), OpenFIGI (SRC-G-01), Intrinio (SRC-G-02), OpenSanctions (SRC-G-03) |
| `accounting_authority` | GAAP/IFRS comparability | IFRS Foundation (SRC-H-01), KPMG (SRC-H-02), PwC (SRC-H-03) |
| `future_trading_reference` | Future trading governance vocabulary only | SEC (SRC-I-10), FINRA (SRC-I-09), ESMA (SRC-I-08, SRC-I-11) |

**Rule**: Tier 1 does not automatically create a hard rule outside its domain. Tier 2 sources may support Tier 1 but not override them. Tier 3 sources (e.g., Investopedia) may never be standalone rule authority for any methodology decision.

---

## 4. Methodology Boundary

### 4.1 What This Framework Governs

- How economic entities are identified (canonical_entity_id principle, asset-type-aware)
- How assets are classified into primary and secondary peer families
- What roles peers may have (six-role peer_role taxonomy)
- What financial comparability gates must be assessed before peer assignment
- How cross-region peers are handled
- How ETFs, funds, and indices are stored separately from company peers
- How peer groups are versioned and reviewed
- What fields are required now vs. reserved for future data or trading integration
- What comparison modes are permitted per peer role

### 4.2 What This Framework Does Not Govern

- Which specific companies belong to which specific peer groups
- Which data vendor provides market data
- How SAI calculates peer-relative metrics
- Whether MoneyHorst is a regulated firm (it is not)

---

## Requirements

### 5. Q1–Q10 Canonical Decisions

### PGMF-DEC-01 (Q1) — Peer Group Organization Principle

**Decision**: Asset-level primary organization using `canonical_entity_id` as primary key, with one `primary_family` and optional `secondary_family` overlay.

**Rationale**: GICS (SRC-B-01) and ICB (SRC-C-01) — both classification_authority sources — establish one-primary-classification-per-company as the global institutional standard. Porter (SRC-D-01) — strategic_peer_logic_authority — establishes that competitive context spans multiple arenas, requiring the secondary_family overlay for cross-family candidates (UBER, AMZN, VRT). Narrative-level organization is deferred until the Narrative Registry exists.

**Source evidence**: SRC-B-01 (classification_authority), SRC-C-01 (classification_authority), SRC-D-01 (strategic_peer_logic_authority)

---

### PGMF-DEC-02 (Q2) — Multi-Family Membership

**Decision**: Multi-family membership is allowed only as `primary_family` + optional `secondary_family`. Uncontrolled multi-tag without hierarchy is prohibited.

**Rationale**: SAI-BLK-21 requires a stable primary anchor for peer comparison. Unlimited multi-tagging produces ambiguous peer sets. The primary/secondary structure gives SAI a deterministic query path while accommodating cross-family candidates.

**Source evidence**: SRC-B-01 (classification_authority), SRC-D-01 (strategic_peer_logic_authority)

---

### PGMF-DEC-03 (Q3) — Peer Role Taxonomy

**Decision**: Every peer assignment carries exactly one `peer_role` from the following exhaustive, non-overlapping six-role taxonomy. The taxonomy was extended from v1 draft to include `etf_peer` to resolve the inconsistency between PGMF-DEC-03 and PGMF-DEC-05.

| peer_role | Valid asset_type | comparison_mode_allowed | Definition |
|-----------|-----------------|------------------------|-----------|
| `core_peer` | company | valuation_comparison (gate-conditional), operating_metric_comparison, market_behavior_comparison | Direct rival; meets all financial comparability gates |
| `adjacent_peer` | company | operating_metric_comparison, market_behavior_comparison | Partial competitor or substitute; comparability_note required |
| `benchmark_context` | etf, fund, index, any | benchmark_context_comparison | Reference instrument; never a company peer |
| `etf_peer` | etf, fund **only** | ETF_fund_comparison | Valid only within PGF-09 or ETF/fund comparison logic |
| `excluded_non_peer` | any | blocked | Explicitly excluded; documented rationale required |
| `private_comparable_context` | private_company | ecosystem_context_only | Non-listed company as competitive context only; valuation_peer_allowed = false |

**Hard constraints on peer_role**:
- Company assets must **never** receive `etf_peer`
- ETFs and funds must **never** receive `core_peer` or `adjacent_peer` against company assets
- `etf_peer` is valid **only** when `asset_type ∈ {etf, fund}`
- `private_comparable_context` must always have `valuation_peer_allowed = false`

**Comparison mode taxonomy** (full set):

| comparison_mode | Permitted for peer_role |
|-----------------|------------------------|
| `valuation_comparison` | core_peer (all comparability gates pass) |
| `operating_metric_comparison` | core_peer, adjacent_peer |
| `market_behavior_comparison` | core_peer, adjacent_peer |
| `benchmark_context_comparison` | benchmark_context |
| `ETF_fund_comparison` | etf_peer |
| `ecosystem_context_only` | private_comparable_context |
| `blocked` | excluded_non_peer, unsupported assets |

**Source evidence**: SRC-D-01 (strategic_peer_logic_authority), SRC-E-01 (financial_comparability_authority), SRC-F-01 (ETF_methodology_authority)

---

### PGMF-DEC-04 (Q4) — Entity / Security / Listing Identity Model

**Decision**: `canonical_entity_id` is the primary identity key. All listing-level identifiers are attributes of a security/listing record linked to the canonical entity. Ticker-only identity is prohibited.

Identity field requirements are **asset-type-aware**. Not all instruments have FIGI, ISIN, or exchange_mic in all contexts.

**Asset-type-aware identity matrix**:

| Field | company (listed) | etf / fund | index | private_company | unsupported_asset_class |
|-------|-----------------|-----------|-------|-----------------|------------------------|
| `canonical_entity_id` | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| `security_id` | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED_IF_AVAILABLE |
| `isin` | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `figi` | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE (unless exchange-traded product) | NOT_APPLICABLE | NOT_APPLICABLE |
| `ticker` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE (unless traded) | NOT_APPLICABLE | NOT_APPLICABLE |
| `exchange_mic` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE (unless exchange-traded index) | NOT_APPLICABLE | NOT_APPLICABLE |
| `primary_listing` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `listing_variant_type` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `adr_flag` | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `trading_currency` | REQUIRED_IF_LISTED | REQUIRED_IF_LISTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| `reporting_currency` | REQUIRED | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| `domicile` | REQUIRED | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE | REQUIRED_IF_AVAILABLE | NOT_APPLICABLE |
| `market_data fields` | FUTURE_SCOPE | FUTURE_SCOPE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |

**Field requirement status definitions**:
- `REQUIRED`: Must be present in every record of this asset_type
- `REQUIRED_IF_LISTED`: Required when the asset has an active exchange listing
- `REQUIRED_IF_AVAILABLE`: Best-effort required; gap must be documented if missing
- `NOT_APPLICABLE`: Field does not apply to this asset_type
- `FUTURE_SCOPE`: Placeholder reserved; not populated in v1

**Source evidence**: SRC-G-01 (identity_authority: OpenFIGI), SRC-G-02 (identity_authority: Intrinio), SRC-G-03 (identity_authority: OpenSanctions), SRC-I-01 (identity_authority: ISO MIC)

---

### PGMF-DEC-05 (Q5) — ETF / Fund / Index Boundary

**Decision**: ETFs and funds are never company peers. Within PGF-09, ETF/fund assets use `peer_role = etf_peer`. As reference instruments in company families, they use `peer_role = benchmark_context`. Indices are `asset_type = index` and `peer_role = benchmark_context` only.

The `etf_peer` role is defined in PGMF-DEC-03. This decision governs when it applies: exclusively within PGF-09 or ETF/fund comparison logic.

**Required ETF/fund comparison fields** (when `asset_type ∈ {etf, fund}`):

| Field | Requirement |
|-------|-------------|
| `benchmark_index` | REQUIRED_IF_APPLICABLE |
| `TER` | REQUIRED_IF_AVAILABLE |
| `AUM` | REQUIRED_IF_AVAILABLE |
| `tracking_difference` | REQUIRED_IF_AVAILABLE |
| `tracking_error` | REQUIRED_IF_AVAILABLE |
| `spread` | REQUIRED_IF_AVAILABLE |
| `holdings_overlap` | REQUIRED_IF_AVAILABLE |
| `replication_method` | REQUIRED_IF_AVAILABLE |
| `distribution_policy` | REQUIRED_IF_AVAILABLE |
| `lookthrough_concentration` | REQUIRED_IF_AVAILABLE |

**Source evidence**: SRC-F-01 (ETF_methodology_authority), SRC-F-02 (ETF_methodology_authority), SRC-F-03, SRC-F-04

---

### PGMF-DEC-06 (Q6) — Liquidity / Market-Cap Thresholds

**Decision**: Soft threshold governance for v1. `market_cap_band` and `liquidity_band` are required categorical fields. **Numeric threshold calibration is deferred** — `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED` must be set on all v1 records.

**market_cap_band categorical values** (non-canonical illustrative categories — numeric cutoffs NOT finalized in v1):
- `mega` — approximately very large cap (illustrative only)
- `large` — approximately large cap (illustrative only)
- `mid` — approximately mid cap (illustrative only)
- `small` — approximately small cap (illustrative only)
- `micro` — approximately micro cap (illustrative only)
- `unknown` — band cannot be determined

**liquidity_band categorical values**:
- `large_liquid`
- `mid_liquid`
- `small_illiquid`
- `micro_thin`
- `unknown`

**Additional fields**:
- `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED` — required on all v1 records
- `comparability_note_required = true` — required when band mismatch between peers is material

**Deferred**: Numeric cutoff calibration requires additional sourcing from index construction methodology (Russell index methodology, MSCI index construction rules) before numeric bands become canonical. Hard dollar values are explicitly **not part of this framework v1**.

**Source evidence**: SRC-E-01 (financial_comparability_authority)
**Deferred item**: EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED — numeric threshold values

---

### PGMF-DEC-07 (Q7) — Private / Non-Listed Comparables

**Decision**: Private comparables are a deferred non-blocking future extension. In v1, private companies may only carry `peer_role = private_comparable_context`, `comparison_mode_allowed = ecosystem_context_only`, and `valuation_peer_allowed = false`. Full private comparable methodology is out of scope for v1.

**Source evidence**: SRC-E-01 (financial_comparability_authority), SRC-G-01 (identity_authority)
**Deferred**: Full private comparable methodology — EVIDENCE_INSUFFICIENT

---

### PGMF-DEC-08 (Q8) — Cross-Region Peer Handling

**Decision**: Cross-region peers are allowed with explicit normalization fields and flags. Raw GAAP vs. IFRS metric comparison without adjustment flag is prohibited.

**Required cross-region fields**:

| Field | Description |
|-------|-------------|
| `accounting_standard` | GAAP / IFRS / other |
| `reporting_currency` | ISO 4217 code |
| `trading_currency` | ISO 4217 code |
| `fiscal_year_end` | Month of fiscal year end |
| `taxonomy_reference` | GICS / ICB / other |
| `comparability_adjustment_required` | Boolean — true when cross-standard adjustment needed |
| `comparability_note` | Required when comparability_adjustment_required = true |

**Source evidence**: SRC-H-01 (accounting_authority), SRC-H-02 (accounting_authority), SRC-H-03 (accounting_authority), SRC-C-01 (classification_authority)

---

### PGMF-DEC-09 (Q9) — Subcluster Governance and Validation

**Decision**: Annual review plus event-triggered review. All peer assignment records must carry governance metadata.

**Required governance fields**: `review_cycle`, `effective_date`, `approved_by`, `source_authority`, `change_reason`, `challenge_status`, `review_status`, `lifecycle_status`.

**Event triggers for out-of-cycle review**: material M&A, revenue mix shift >30%, business model restructuring, primary listing change, accounting standard change.

**Source evidence**: SRC-A-01 (governance_authority), SRC-B-03 (classification_authority — versioning precedent), SRC-C-01 (classification_authority — challenge/appeal model)

---

### PGMF-DEC-10 (Q10) — Peer Group Versioning

**Decision**: Effective_date / end_date versioning at record level. Every membership or role change creates a new versioned record. Historical peer definitions must be reproducible for any past date.

**Required versioning fields**: `effective_date`, `end_date`, `lifecycle_status`, `change_reason`, `methodology_version`.

**Source evidence**: SRC-A-01 (governance_authority), SRC-B-01 (classification_authority), SRC-B-03 (classification_authority — versioning precedent)

---

## 6. Financial Comparability Gate

Before an asset may be assigned `peer_role = core_peer`, the following gate dimensions must be assessed and documented. Gate authority: SRC-E-01, SRC-E-03 (financial_comparability_authority).

| Gate Dimension | Field | Notes |
|----------------|-------|-------|
| Business model similarity | `business_model_similarity` | Same product, customer, distribution |
| Market cap band | `market_cap_band` | Categorical — numeric thresholds DEFERRED |
| Liquidity band | `liquidity_band` | Categorical — numeric thresholds DEFERRED |
| Growth profile | `growth_profile_comparable` | Boolean with note |
| Margin structure | `margin_structure_comparable` | Boolean with note |
| Capital intensity | `capital_intensity_comparable` | Boolean with note |
| Leverage | `leverage_comparable` | Boolean with note |
| Accounting standard | `accounting_standard` | GAAP / IFRS / other |
| Cross-region adjustment | `comparability_adjustment_required` | Must be documented |
| Band mismatch flag | `comparability_note_required` | true when band mismatch is material |
| Valuation peer | `valuation_peer_allowed` | false for private_comparable_context |
| Threshold calibration | `threshold_calibration_status` | NUMERIC_THRESHOLDS_DEFERRED in v1 |

If any gate dimension produces a material comparability gap, `peer_role` must be `adjacent_peer` and a `comparability_note` must be recorded.

---

## 7. Unsupported Asset Class Handling

Assets not fitting any v0 family must be classified as:

- `UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION`
- or `PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON`

These status values set `peer_comparison_allowed = false` and `peer_group_available = false`. Ad-hoc peer invention is prohibited.

**Asset classes requiring separate future methodology**:

| Asset Class | v1 Status | peer_role in v1 |
|-------------|------------|-----------------|
| Commodities | FUTURE_SCOPE | UNSUPPORTED |
| Crypto | FUTURE_SCOPE | UNSUPPORTED |
| Bonds / Credit | FUTURE_SCOPE | UNSUPPORTED |
| Derivatives / Structured Products | FUTURE_SCOPE | UNSUPPORTED |
| FX / Cash | FUTURE_SCOPE | UNSUPPORTED |
| Private companies | private_comparable_context only | private_comparable_context |
| ETFs / Funds | CURRENT_SCOPE — PGF-09 rules | etf_peer or benchmark_context |
| Indices | CURRENT_SCOPE — benchmark_context only | benchmark_context |

---

## 8. Market Data Readiness Fields

Reserved in the registry data model now. NOT currently populated or integrated.

**Scope**: CURRENT_SCOPE_FOR_DATA_MODEL / FUTURE_SCOPE_FOR_VENDOR_INTEGRATION

| Field | Description | Scope |
|-------|-------------|-------|
| `exchange_mic` | ISO 10383 MIC for listing venue | CURRENT_MODEL |
| `market_data_source` | Exchange origin of price data | CURRENT_MODEL |
| `data_vendor` | Aggregator/distributor | CURRENT_MODEL |
| `data_latency_class` | real_time / delayed_15min / end_of_day | CURRENT_MODEL |
| `exchange_timezone` | IANA timezone of primary listing | CURRENT_MODEL |
| `trading_calendar_id` | Reference to exchange trading calendar | CURRENT_MODEL |
| `derived_data_policy` | Whether analytics require non-display license | CURRENT_MODEL |
| `index_license_required` | Whether index data license is required | CURRENT_MODEL |
| `quote_timestamp_required` | Whether bid/ask timestamps must be stored | FUTURE_DATA |
| `realtime_entitlement_required` | Whether real-time entitlement is required | FUTURE_DATA |
| `display_usage_allowed` | Whether data may be displayed without additional license | FUTURE_DATA |
| `non_display_usage_allowed` | Whether non-display derived analytics usage is licensed | FUTURE_DATA |
| `redistribution_allowed` | Whether data may be redistributed | FUTURE_DATA |

Source authority: SRC-I-01 (identity_authority), SRC-I-02, SRC-I-03, SRC-I-04 (exchange licensing), SRC-I-06, SRC-I-07

---

## 9. Trading Governance Boundary

The following fields are reserved for future trading governance only. They create NO current legal obligation.

**Regulatory sources are used only to reserve future vocabulary and prevent architectural drift. Nothing in this framework creates current legal obligations, regulated status, compliance claims, broker-dealer activity, investment-firm activity, exchange participation, order routing, market access, or trading enablement. MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue.**

**Scope**: FUTURE_SCOPE_TRADING_GOVERNANCE / FUTURE_COMPLIANCE_REFERENCE / NOT_CURRENT_LEGAL_OBLIGATION

| Field | Regulatory Reference | When Applicable |
|-------|---------------------|----------------|
| `execution_venue_eligible` | SRC-I-08 (future_trading_reference: MiFID II Art.27) | EU order routing |
| `best_execution_required` | SRC-I-08/09 (future_trading_reference: MiFID II / FINRA 5310) | Client order routing |
| `order_routing_policy_required` | SRC-I-08/09 | Order routing |
| `pre_trade_controls_required` | SRC-I-10/11 (future_trading_reference: SEC 15c3-5 / RTS 6) | Electronic market access |
| `price_collar_policy` | SRC-I-10 | Pre-trade risk controls |
| `max_order_value_policy` | SRC-I-10 | Pre-trade risk controls |
| `kill_switch_required` | SRC-I-10/11 | Automated trading |
| `audit_log_required` | SRC-I-10/11 | Regulated activity |
| `surveillance_required` | SRC-I-10/11 | Market access |
| `market_abuse_monitoring_required` | SRC-I-11 (future_trading_reference: MiFID II RTS 6) | Algorithmic trading |
| `tradability_status` | SRC-I-10/11 | Asset-level trading enablement |
| `trading_enabled` | SRC-I-10/11 | Trading implementation |
| `trade_block_reason` | SRC-I-10 | Restricted security lists |

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

### 10.3 Future Registry Output Contract for SAI

When the Peer Group Registry is created under this framework, SAI may expect the following output fields per asset:

| Field | Description |
|-------|-------------|
| `peer_group_available` | Boolean — whether a canonical peer group exists for this asset |
| `peer_comparison_allowed` | Boolean — whether peer comparison may be performed |
| `blocked_reason` | Why peer comparison is blocked, if applicable |
| `unsupported_status` | UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION or null |
| `primary_family` | Primary peer family assignment |
| `secondary_family` | Optional secondary family |
| `peer_role` | This asset's role in the peer set |
| `core_peer_set` | List of canonical_object_id values with peer_role = core_peer |
| `adjacent_peer_set` | List of canonical_object_id values with peer_role = adjacent_peer |
| `benchmark_context_set` | List of reference instruments |
| `etf_peer_set` | List of ETF/fund peers (PGF-09 only) |
| `comparison_mode_allowed` | Which comparison types are permitted for this asset |
| `financial_comparability_gate_status` | pass / partial / blocked |
| `comparability_note` | Adjustment notes for cross-region or adjacent peers |
| `data_quality_status` | Completeness of peer data |
| `as_of_date` | Date for which this peer definition is valid |
| `methodology_version` | Version of methodology framework used |

**Graceful degradation rules**:
- If `peer_group_available = false`: SAI-BLK-21 must produce the standard deferred_dependency_notes message and not generate peer-relative interpretations.
- If `peer_comparison_allowed = false`: No peer-relative interpretation may be generated regardless of available data.
- SAI must never create ad-hoc peers to compensate for a missing registry entry.

### 10.4 No-Ad-Hoc-Peer Rule

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
5. Numeric threshold calibration (Q6 extension) requires additional index construction methodology sourcing before numeric bands become canonical.
6. Private comparable methodology (Q7 extension) requires a separate evidence sourcing task.
7. New asset class methodology modules require a dedicated evidence sourcing task and human/CTO scope decision before any peer assignments are made.

---

## 12. Requirements Readiness Status

```
PEER_GROUP_REGISTRY_METHODOLOGY_REQUIREMENTS_READY_FOR_DESIGN_AFTER_HARDENING
```

**Hardening changes applied in v2**:
- PGMF-DEC-03: `etf_peer` added to official six-role peer_role taxonomy with strict asset_type constraint and comparison_mode_allowed taxonomy
- PGMF-DEC-06: Hard dollar values removed; numeric thresholds explicitly marked as non-canonical, illustrative, and DEFERRED; `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED` required on all v1 records
- PGMF-DEC-04: Simple Required/Not-Required table replaced with asset-type-aware identity matrix (six asset_types × field requirements)
- Section 3: Source authority hierarchy restructured as domain-specific mapping (classification_authority, governance_authority, financial_comparability_authority, etc.); Tier 1 no longer implies blanket hard-rule authority outside its domain
- Section 10.3: Future Registry Output Contract for SAI added with 17 output fields and graceful degradation rules
- Section 9: Explicit no-regulatory-compliance-claim language added

**Remaining deferred items**:
- Q6: Numeric threshold calibration — EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED
- Q7: Full private comparable methodology — EVIDENCE_INSUFFICIENT
- Registry creation still prohibited — requires separate preflight and CTO approval

**design.md may proceed only after these hardening fixes are accepted.**

---

*End of requirements document v2.*

## Glossary

| Term | Definition |
|------|-----------|
| `canonical_entity_id` | Stable primary key identifying an economic entity — interpreted as `canonical_object_id` in design.md (polymorphic across companies, ETFs, funds, indices, private companies) |
| `peer_role` | The role a given asset plays in a peer group: core_peer, adjacent_peer, benchmark_context, etf_peer, excluded_non_peer, or private_comparable_context |
| `primary_family` | The single primary peer group family assignment for an economic entity (e.g., PGF-01) |
| `secondary_family` | Optional secondary peer group family for cross-family candidates (e.g., UBER spanning mobility and delivery) |
| `comparison_mode_allowed` | The set of comparison types permitted for a peer_role (e.g., valuation_comparison, ETF_fund_comparison) |
| `exchange_mic` | ISO 10383 Market Identifier Code — four-character code uniquely identifying a trading venue |
| `FIGI` | Financial Instrument Global Identifier — open standard 12-character identifier per instrument per listing venue (OpenFIGI) |
| `ISIN` | International Securities Identification Number — security-level identifier (ISO 6166), not entity-level |
| `comparability_adjustment_required` | Boolean flag indicating that cross-standard (GAAP/IFRS) adjustment documentation is required before direct metric comparison |
| `threshold_calibration_status` | Indicator for whether numeric market-cap or liquidity thresholds have been calibrated; v1 value: NUMERIC_THRESHOLDS_DEFERRED |
| `core_peer` | A direct rival that meets all financial comparability gates; valuation comparison permitted if gate passes |
| `adjacent_peer` | A partial competitor or substitute; comparability_note required; valuation comparison requires explicit approval |
| `benchmark_context` | Reference instrument (ETF, index, sector fund) used for comparison framing; never a company peer |
| `etf_peer` | An ETF or fund peer within PGF-09 comparison logic; valid only when asset_type ∈ {etf, fund} |
| `private_comparable_context` | Non-listed company noted as competitive context only; comparison_mode = ecosystem_context_only; valuation_peer_allowed = false |
| `PGF-09` | Peer Group Family 09 — ETF/Fund Peer Rule; governs all ETF and fund peer comparison logic |
| `SAI-BLK-21` | Single Asset Intelligence Block 21 — Peer Comparison; the SAI block that consumes canonical peer group definitions |
| `UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION` | Status value for assets that do not fit any v0 peer family; peer comparison blocked until CTO/human scope decision |
| `PEER_GROUP_SCOPE_REQUIRED_BEFORE_COMPARISON` | Alternative status value for the same unsupported asset condition |
| `methodology_version` | Version identifier of this framework; must be incremented on any material methodology change |
| `peer_group_available` | Boolean registry output field indicating whether a canonical peer group exists for an asset |
| `peer_comparison_allowed` | Boolean registry output field indicating whether SAI-BLK-21 may perform peer-relative interpretation |
