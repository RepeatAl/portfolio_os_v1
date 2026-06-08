# Peer Group Registry Methodology Framework — Q1–Q10 Decision Intake Review

**Artifact**: decision_intake_review_2026-06-08.md
**Task**: Task 1 — Produce Q1–Q10 Decision Intake Document
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_1_DECISION_INTAKE_READY_FOR_HUMAN_REVIEW

**Purpose**: This document is decision intake only. It does not create a Peer Group Registry. It does not assign canonical peer groups to any asset. It does not create peer_group_id values. It consolidates the 10 canonical methodology decisions from requirements.md v2 into a single human-reviewable document with evidence citations, rationale, deferred items, and downstream implications.

**Hard boundaries confirmed**:
- No peer_group_registry.yaml created
- No peer assignments made
- No canonical peer_group_id values created
- No registry or SSOT mutation
- No SAI artifact modification
- No implementation code
- No market data integration
- No broker, exchange, or trading venue connection
- No trading logic

---

## Summary Table

| # | Question | Decision | Authority Domain | Deferred | Status |
|---|----------|----------|-----------------|----------|--------|
| Q1 | Organization principle | Asset-level primary + optional secondary_family; canonical_object_id as primary key | classification_authority, strategic_peer_logic_authority | Narrative-level organization deferred | DECIDED |
| Q2 | Multi-family membership | primary_family + optional secondary_family only; no uncontrolled multi-tag | classification_authority, strategic_peer_logic_authority | None | DECIDED |
| Q3 | Peer role taxonomy | Six-role exhaustive taxonomy incl. etf_peer | strategic_peer_logic_authority, financial_comparability_authority, ETF_methodology_authority | None | DECIDED |
| Q4 | Entity / identity model | canonical_object_id as polymorphic primary key; asset-type-aware field requirements | identity_authority | Private company identifier standard deferred | DECIDED |
| Q5 | ETF / fund / index boundary | ETFs/funds never company peers; etf_peer within PGF-09; indices = benchmark_context only | ETF_methodology_authority | UCITS vs. 1940-Act subcluster detail deferred | DECIDED |
| Q6 | Liquidity / market-cap thresholds | Soft categorical bands; NUMERIC_THRESHOLDS_DEFERRED | financial_comparability_authority | Numeric calibration — EVIDENCE_PARTIAL | DEFERRED (partial) |
| Q7 | Private comparables | private_comparable_context only; valuation_peer_allowed = false | financial_comparability_authority, identity_authority | Full methodology — EVIDENCE_INSUFFICIENT | DEFERRED |
| Q8 | Cross-region peer handling | Allowed with accounting_standard + comparability_adjustment_required flags | accounting_authority, classification_authority | Fiscal year-end alignment automation deferred | DECIDED |
| Q9 | Subcluster governance | Annual + event-triggered review; challenge_status and review_status fields | governance_authority, classification_authority | External advisory process design deferred | DECIDED |
| Q10 | Peer group versioning | Record-level effective_date / end_date; non-overlap property; gaps allowed when documented | governance_authority, classification_authority | Full audit trail (Option C) deferred | DECIDED |

---

## Q1 — Peer Group Organization Principle

**Decision**: Asset-level primary organization using `canonical_object_id` as the primary key, with one `primary_family` and an optional `secondary_family` overlay.

**Evidence citations**:
- SRC-B-01, SRC-B-02 (classification_authority — GICS): One primary classification per company per tier. Revenue drives primary assignment. Earnings and market perception are supplemental.
- SRC-C-01 (classification_authority — ICB): Same single-classification-per-company principle used by European exchanges.
- SRC-D-01 (strategic_peer_logic_authority — Porter): Platform companies (UBER, AMZN, VRT) compete simultaneously in multiple markets that no single GICS sub-industry captures. This justifies a secondary_family overlay.

**Key rationale**: GICS and ICB both establish one primary classification as the global institutional standard. The primary/secondary structure gives SAI-BLK-21 a deterministic primary query anchor while accommodating cross-family candidates with a controlled secondary assignment.

**Deferred items**: Narrative-level organization is deferred until the Narrative Registry exists. When available, narrative tagging may be added as an additive-only extension.

**Downstream implications**:
- SAI-BLK-21 queries peer definitions by canonical_object_id + primary_family as its deterministic anchor.
- Cross-family candidates (UBER, AMZN, VRT) require documented secondary_family assignments with explicit rationale in change_reason.
- The canonical_object_id rename from canonical_entity_id is a design-layer clarification: "entity" is legally specific and does not apply to indices and abstract instruments. requirements.md v2 references to canonical_entity_id are interpreted as canonical_object_id in design.

---

## Q2 — Multi-Family Membership

**Decision**: Multi-family membership is allowed only as `primary_family` + optional `secondary_family`. Uncontrolled multi-tag without hierarchy is prohibited.

**Evidence citations**:
- SRC-B-01 (classification_authority — GICS): One primary classification per company. GICS does not support multi-family; MoneyHorst extends minimally with a documented secondary overlay.
- SRC-D-01 (strategic_peer_logic_authority — Porter): Multiple competitive arenas justify secondary family context but unlimited tagging without a primary anchor produces ambiguous peer sets SAI cannot deterministically consume.

**Key rationale**: SAI-BLK-21 requires exactly one primary peer family to anchor peer queries. The primary + optional secondary structure is the minimum extension that solves cross-family candidates without losing the primary anchor discipline.

**Deferred items**: None. Decision is complete.

**Downstream implications**:
- Every registry record must declare primary_family. secondary_family is optional and requires a documented rationale in change_reason.
- SAI-BLK-21 uses primary_family peers for primary peer comparison. secondary_family peers may be used for supplementary context in a future SAI interface extension.

---

## Q3 — Peer Role Taxonomy

**Decision**: Every peer assignment carries exactly one `peer_role` from the following exhaustive, non-overlapping six-role taxonomy.

| peer_role | Valid asset_type | comparison_mode_allowed | Definition |
|-----------|-----------------|------------------------|-----------|
| `core_peer` | company | valuation_comparison (gate-conditional), operating_metric_comparison, market_behavior_comparison | Direct rival; all financial comparability gates pass |
| `adjacent_peer` | company | operating_metric_comparison, market_behavior_comparison | Partial competitor or substitute; comparability_note required |
| `benchmark_context` | etf, fund, index, any | benchmark_context_comparison | Reference instrument; never a company peer |
| `etf_peer` | etf, fund ONLY | ETF_fund_comparison | Valid only within PGF-09 or ETF/fund comparison logic |
| `excluded_non_peer` | any | blocked | Explicitly excluded; documented rationale required |
| `private_comparable_context` | private_company | ecosystem_context_only | Non-listed company as context only; valuation_peer_allowed = false |

**Hard constraints**:
- Company assets must NEVER receive `etf_peer`
- ETFs/funds must NEVER receive `core_peer` or `adjacent_peer` against company assets
- `etf_peer` valid ONLY when asset_type ∈ {etf, fund}
- `private_comparable_context` must always have `valuation_peer_allowed = false`

**Evidence citations**:
- SRC-D-01 (strategic_peer_logic_authority — Porter): Direct rivals, substitutes, and ecosystem participants have different competitive relationships requiring different role labels.
- SRC-E-01 (financial_comparability_authority — Damodaran): Financial comparability gates distinguish core (direct rival, all gates pass) from adjacent (partial comparability).
- SRC-F-01 (ETF_methodology_authority — Morningstar): ETF comparison is a fundamentally distinct methodology requiring its own role (etf_peer) with a distinct comparison field set.

**Key rationale**: The original five-role taxonomy omitted `etf_peer`, creating an inconsistency: PGF-09 needed a role for ETF-vs-ETF comparison that was neither core_peer nor benchmark_context. Adding etf_peer with a strict asset_type constraint resolves this without breaking the ETF/company boundary.

**Deferred items**: None. Decision and comparison_mode taxonomy (7 modes) are complete.

**Downstream implications**:
- Every peer group assignment record must declare peer_role. Null is only valid for unsupported_asset_class records.
- comparison_mode_allowed drives what SAI-BLK-21 may produce: a core_peer enables valuation_comparison (if gate passes); adjacent_peer does not.
- Correctness property 13 in design.md enforces object_type / peer_role / asset_type tri-field consistency.

---

## Q4 — Entity / Security / Listing Identity Model

**Decision**: `canonical_object_id` is the polymorphic primary key at Layer 1. All listing-level identifiers (FIGI, ISIN, ticker, MIC) are Layer 2 attributes. Ticker-only identity is prohibited. Identity field requirements are asset-type-aware.

**Asset-type identity summary**:

| Asset type | canonical_object_id | ISIN | FIGI | exchange_mic |
|------------|---------------------|------|------|-------------|
| company (listed) | REQUIRED | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_LISTED |
| etf / fund | REQUIRED | REQUIRED_IF_AVAILABLE | REQUIRED_IF_AVAILABLE | REQUIRED_IF_LISTED |
| index | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE (unless exchange-traded) |
| private_company | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| unsupported_asset_class | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |

**Evidence citations**:
- SRC-G-01 (identity_authority — OpenFIGI): One FIGI per instrument per listing venue. ASML has distinct FIGIs on XAMS and XNAS — both represent the same object. A canonical object layer is required above FIGIs.
- SRC-G-02 (identity_authority — Intrinio): Internal entity identifier as primary key; FIGI/ISIN/ticker are mapped attributes. Ticker symbols are not stable — they change on relisting and acquisition.
- SRC-G-03 (identity_authority — OpenSanctions): ISINs are security-level identifiers, not object-level.
- SRC-I-01 (identity_authority — ISO 10383 MIC): Four-character MIC is the canonical venue identifier. XETR, XNAS, XNYS, XAMS each have distinct MICs.

**Key rationale**: Tickers are not stable primary keys. ISINs are security-level. FIGI identifies listings per venue. Only canonical_object_id above all listing attributes provides a stable primary key that survives relisting, ADR changes, and cross-venue duplication. "Entity" was avoided because it has legal/corporate meaning inapplicable to abstract instruments like the S&P 500 index.

**Deferred items**: Private company identifier standard (what external identifier to use for canonical_object_id when no FIGI/ISIN is available) is deferred. In v1, private companies use an internally assigned canonical_object_id.

**Downstream implications**:
- The registry must maintain a Layer 1 object record before any Layer 3 peer group assignment.
- Cross-listed securities must map multiple Layer 2 listing records to one Layer 1 canonical_object_id to prevent duplicate exposure.
- exchange_mic, exchange_timezone, trading_calendar_id are CURRENT_MODEL_NULLABLE — must exist in Layer 2 schema now to prevent future architectural rewrite.

---

## Q5 — ETF / Fund / Index Boundary

**Decision**: ETFs and funds are never company peers. Within PGF-09, ETF/fund assets receive `peer_role = etf_peer`. As reference instruments in company families, they receive `peer_role = benchmark_context`. Indices receive `asset_type = index` and `peer_role = benchmark_context` only.

**Required ETF/fund fields** (asset_type ∈ {etf, fund}): `benchmark_index`, `TER`, `AUM`, `tracking_difference`, `tracking_error`, `spread`, `holdings_overlap`, `replication_method`, `distribution_policy`, `lookthrough_concentration` — all REQUIRED_IF_AVAILABLE.

**Evidence citations**:
- SRC-F-01 (ETF_methodology_authority — Morningstar): Tracking difference and tracking error are primary ETF comparison dimensions — fundamentally different from company peer comparison.
- SRC-F-02 (ETF_methodology_authority — Columbia Law): ETF name/theme similarity alone is insufficient; multi-dimensional assessment is required.
- SRC-F-03 (ETF_methodology_authority — etf.com): Funds tracking the same index form the most natural ETF peer group.
- SRC-F-04 (ETF_methodology_authority — Morningstar): Domicile (UCITS vs. 1940-Act) affects TER ranges and distribution policy.

**Key rationale**: Mixing QQQ with NVDA as company peers is a category error. The ETF/company boundary is enforced as a data model constraint: asset_type ∈ {etf, fund} can NEVER receive core_peer or adjacent_peer against company assets.

**Deferred items**: UCITS vs. 1940-Act domicile sub-classification governance detail is deferred to Task 4 (ETF/fund peer rule specification).

**Downstream implications**:
- QQQ, SMH, CIBR, XLF, XLI and all benchmark context instruments must be stored with peer_role = benchmark_context, never as company peers.
- SAI-BLK-19 and SAI-BLK-20 consume benchmark_context instruments as reference frames. SAI-BLK-21 consumes core_peer and adjacent_peer only.

---

## Q6 — Liquidity / Market-Cap Thresholds

**Decision**: Soft threshold governance for v1. `market_cap_band` and `liquidity_band` are required categorical fields. Numeric cutoffs are NOT finalized in v1.

**Status**: EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED

**Categorical values (non-canonical illustrative categories — numeric cutoffs NOT finalized)**:
- market_cap_band: mega / large / mid / small / micro / unknown
- liquidity_band: large_liquid / mid_liquid / small_illiquid / micro_thin / unknown

**Required fields on all v1 records**:
- `threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED`
- `comparability_note_required = true` when band mismatch between proposed peers is material

**Evidence citations**:
- SRC-E-01 (financial_comparability_authority — Damodaran): Size comparability is a core financial comparability gate. A $1B and $500B company in the same GICS sub-industry have different risk, liquidity, and multiple profiles — not directly comparable without adjustment.

**Key rationale**: The principle that size comparability matters is well-evidenced. Specific numeric cutoffs are not prescribed by any current source. Russell index methodology and MSCI index construction rules are the appropriate additional sources but have not yet been sourced.

**Deferred items**:
- Numeric threshold calibration requires additional sourcing from index construction methodology (Russell index methodology, MSCI index construction rules).
- Hard dollar values have been removed. They were illustrative only and must not become canonical without sourcing.
- This is a future additive-only extension requiring human/CTO approval.

**Downstream implications**:
- In v1, all peer assignments carry threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED.
- When a band mismatch is material, comparability_note_required = true and a comparability_note must document the gap.
- The financial comparability gate can still function with categorical bands — it can flag material size gaps and downgrade core_peer to adjacent_peer.

---

## Q7 — Private / Non-Listed Comparables

**Decision**: Private comparables are a deferred, non-blocking future extension. In v1:
- `peer_role = private_comparable_context` only
- `comparison_mode_allowed = ecosystem_context_only`
- `valuation_peer_allowed = false`

**Status**: EVIDENCE_INSUFFICIENT

**Evidence citations**:
- SRC-E-01 (financial_comparability_authority — Damodaran): Comparable company analysis is fundamentally a public markets exercise. Private comparable valuation requires different techniques. Direct comparison of public and private companies on market multiples is not valid.
- SRC-G-01 (identity_authority — OpenFIGI): Private companies have no FIGI. The identification infrastructure for private companies is fundamentally different from exchange-listed securities.

**Key rationale**: SpaceX (PGF-06), Stripe (PGF-03), and ByteDance (PGF-05) are competitive peers with no public listing. Their exclusion creates systematic coverage gaps, but the methodology to handle them safely has not been sourced.

**Deferred items**:
- Full private comparable methodology requires a separate evidence sourcing task from M&A advisory or private equity valuation methodology sources.
- Private company identifier approach (canonical_object_id for private companies) requires separate research.

**Downstream implications**:
- Private company records may exist in the registry with peer_role = private_comparable_context for competitive landscape documentation purposes only.
- SAI-BLK-21 must not produce valuation comparisons using private_comparable_context records.
- comparison_mode_allowed = ecosystem_context_only — record can be surfaced as competitive landscape context but not as a formal peer comparison input.

---

## Q8 — Cross-Region Peer Handling

**Decision**: Cross-region peers are allowed with explicit normalization fields and flags. Raw GAAP vs. IFRS metric comparison without the comparability_adjustment_required flag is prohibited.

**Required cross-region fields**:

| Field | Description |
|-------|-------------|
| `accounting_standard` | GAAP / IFRS / other |
| `reporting_currency` | ISO 4217 code |
| `trading_currency` | ISO 4217 code |
| `fiscal_year_end` | Month (e.g., DEC, SEP) |
| `taxonomy_reference` | GICS / ICB / other |
| `comparability_adjustment_required` | Boolean — true when cross-standard adjustment needed |
| `comparability_note` | Required when comparability_adjustment_required = true |

**Evidence citations**:
- SRC-H-01 (accounting_authority — IFRS Foundation / IFRS 8): Management approach segment reporting may differ from external GAAP statement figures. Cross-region segment comparisons require care.
- SRC-H-02 (accounting_authority — KPMG): R&D capitalization differs (IFRS allows development phase; GAAP does not), lease accounting differs in short-term lease detail, financial instrument classification differs — creating material non-comparability.
- SRC-H-03 (accounting_authority — PwC): LIFO inventory prohibited under IFRS; permitted under GAAP. Revenue recognition substantially converged but industry-specific differences remain.
- SRC-C-01 (classification_authority — ICB): ICB and GICS do not map 1:1. European assets may be ICB-classified; cross-taxonomy reconciliation is required.

**Key rationale**: European peers are structurally necessary across PGF-06 (Rheinmetall, Thales), PGF-07 (Schneider Electric, Siemens), and PGF-08 (SAN, BNP, DB). Blocking cross-region peers entirely would create critical coverage gaps. The flag-based approach documents the comparability limitation at record level without blocking valid peer assignments.

**Deferred items**: Fiscal year-end alignment automation deferred to Task 5 (cross-region comparability specification).

**Downstream implications**:
- Every European-listed peer record must carry accounting_standard = IFRS, reporting_currency, and taxonomy_reference = ICB.
- When comparability_adjustment_required = true, SAI-BLK-21 must surface the comparability_note — raw metric comparison without the note is prohibited.
- XETR and XAMS/XPAR/XMIL MIC codes and CET timezone must be recorded in the Layer 2 listing record.

---

## Q9 — Subcluster Governance and Validation

**Decision**: Annual review plus event-triggered review. All peer assignment records must carry full governance metadata.

**Required governance fields**: `review_cycle`, `effective_date`, `approved_by`, `source_authority`, `change_reason`, `challenge_status`, `review_status`, `lifecycle_status`.

**Event triggers for out-of-cycle review**:
- Material M&A (acquisition, merger, spinoff)
- Revenue mix shift >30%
- Business model restructuring
- Primary listing change
- Accounting standard change

**Evidence citations**:
- SRC-A-01 (governance_authority — CFA/GIPS): Methodology choices must be documented, versioned, and periodically reviewed. Cherry-picking subcluster definitions for favorable outcomes is prohibited.
- SRC-B-03 (classification_authority — MSCI GICS versioning): Classification changes require advance notice and documented transition. The 2018 Communication Services reclassification has material downstream effects on portfolio composition and risk — demonstrating why version-controlled peer group governance is essential.
- SRC-C-01 (classification_authority — ICB): External advisory process and challenge/appeal concept prevent classification capture.

**Key rationale**: Without governance, subclusters drift as companies evolve. The annual review + event-triggered model is consistent with GICS annual review (SRC-B-01) and GIPS methodology documentation requirements (SRC-A-01).

**Deferred items**: External advisory process design (ICB-style challenge/appeal with an external body) is deferred. v1 uses CTO/internal governance with documented challenge_status workflow.

**Downstream implications**:
- Every peer assignment record must carry effective_date and approved_by. Records without these fields are invalid.
- challenge_status (none / under_review / resolved) creates a formal process for identifying subcluster drift.
- When an event trigger occurs, lifecycle_status is set to under_review and a new versioned record is created after review.

---

## Q10 — Peer Group Versioning

**Decision**: Record-level effective_date / end_date versioning. Every membership or role change creates a new versioned record. The superseded record receives an end_date. Historical peer definitions must be reproducible for any past date.

**Versioning non-overlap property**: Active version records must not overlap in time. Gaps in the effective_date / end_date sequence are allowed only when lifecycle_status, blocked_reason, or unsupported_status explicitly documents why no active peer assignment exists for that period.

**Required versioning fields**: `effective_date`, `end_date` (null = currently active), `lifecycle_status`, `change_reason`, `methodology_version`.

**Evidence citations**:
- SRC-A-01 (governance_authority — CFA/GIPS): Versioning is a prerequisite for fair representation of historical methodology. Historical versions must be retained for comparability.
- SRC-A-03 (governance_authority — CFA GIPS 2024): Both methodology and output must be transparent; versioning applies to both layers.
- SRC-B-01, SRC-B-03 (classification_authority — GICS): GICS undergoes annual review with documented effective dates and transitions. Historical classification data is retained for backtesting.

**Key rationale**: Without versioning, peer groups will be stale within 12 months and historical diagnostic reproduction is impossible. Effective_date / end_date versioning (Option B) is the minimum standard enabling as-of-date historical queries. Full audit trail (Option C) is deferred as an additive-only future extension.

**Deferred items**: Full audit trail versioning (Option C — every field change creates a new version record) is deferred to a future additive-only extension.

**Downstream implications**:
- SAI-BLK-21 must specify an as-of-date when querying peer definitions.
- Every new registry record must carry methodology_version.
- The non-overlap property (not the original no-gap formulation) allows assets under review, delisted, or unsupported to have documented gaps in peer assignment history.

---

## Market Data Readiness Summary

### CURRENT_MODEL_NULLABLE — Must Exist in v1 Schema, Value Is Null

These 8 fields must be present in the Layer 2 registry schema now to prevent architectural rewrite when market data integration is added:

| Field | Why It Must Exist Now |
|-------|----------------------|
| `exchange_mic` | Cross-listing normalization: ASML on XAMS vs. XNAS are distinct listings of one object |
| `exchange_timezone` | Quote timestamp normalization: XETR (CET) and XNAS (ET) cannot be compared without this |
| `trading_calendar_id` | Quote staleness: required to determine session boundaries |
| `derived_data_policy` | Prevents silent non-display license violations when analytics are computed from licensed data |
| `index_license_required` | Prevents unlicensed index data consumption for index and ETF objects |
| `market_data_source` | Exchange origin of price data — distinct from data_vendor |
| `data_vendor` | Data aggregator/distributor — distinct from market_data_source |
| `data_latency_class` | Declares real-time / delayed / end_of_day at record level |

### FUTURE_VENDOR_INTEGRATION — Not in v1 Schema

These 9 fields require active commercial vendor agreements before they can be populated:

| Field | Activation Condition |
|-------|---------------------|
| `realtime_entitlement_required` | Active real-time data contract per exchange |
| `display_usage_allowed` | Explicit display usage license per exchange |
| `non_display_usage_allowed` | Explicit non-display/derived-data license |
| `redistribution_allowed` | Redistribution authorization per exchange |
| `professional_user_flag` | User classification infrastructure |
| `market_data_audit_required` | Audit and compliance reporting infrastructure |
| `bid_ask_source` | Live feed subscription |
| `stale_quote_threshold` | Session-aware data infrastructure |
| `quote_timestamp_required` | Feed integration before timestamps can be stored |

---

## Trading Governance Boundary Confirmation

All 14 trading governance fields are **FUTURE_COMPLIANCE_REFERENCE only**:
- Reserved in methodology vocabulary only
- Not part of v1 registry schema
- Not populated
- Not operational
- No current legal obligations created

**Explicit statement**: MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue. Regulatory sources (SEC Rule 15c3-5, FINRA Rule 5310, MiFID II Article 27, MiFID II RTS 6) are used only to reserve future vocabulary and prevent architectural drift. Nothing in this framework creates current legal obligations, regulated status, compliance claims, broker-dealer activity, investment-firm activity, exchange participation, order routing, market access, or trading enablement.

**Three-gate activation model**: Trading governance fields may only become operational after:
1. Regulatory Status Gate: MoneyHorst becomes a regulated entity
2. Jurisdiction Gate: Applicable regulatory framework identified per asset/venue
3. Implementation Gate: Trading system, pre-trade controls, order routing, and audit systems built and certified

**Fourteen fields reserved** (FUTURE_COMPLIANCE_REFERENCE):
`tradability_status`, `trading_enabled`, `trade_block_reason`, `execution_venue_eligible`, `best_execution_required`, `order_routing_policy_required`, `pre_trade_controls_required`, `price_collar_policy`, `max_order_value_policy`, `kill_switch_required`, `audit_log_required`, `surveillance_required`, `market_abuse_monitoring_required`, `algo_trading_flag`

---

## Document Status

This document is **decision intake only**. It does not create a Peer Group Registry. It does not assign any peer to any asset. It does not create canonical peer_group_id values.

```
PGMF_TASK_1_DECISION_INTAKE_READY_FOR_HUMAN_REVIEW
```

---

*End of decision intake document.*
