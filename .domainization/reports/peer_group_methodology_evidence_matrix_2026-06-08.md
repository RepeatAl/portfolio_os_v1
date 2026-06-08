# Peer Group Methodology Evidence Matrix

**Artifact**: peer_group_methodology_evidence_matrix_2026-06-08.md
**Date**: 2026-06-08
**Branch**: spec/peer-group-methodology-source-screening
**Authority**: Research / Source Screening
**Status**: evidence mapping complete — NOT canonical methodology decisions
**Purpose**: Evidence matrix mapping source findings to MoneyHorst design questions Q1–Q10 and future registry fields.

This matrix maps the 22 sources in the source registry to design questions Q1–Q10. For each question it records: why it matters, relevant sources, extracted evidence, possible decision directions, risks of wrong decision, future registry fields affected, open issues, and readiness status.

**Hard boundaries**: This matrix does not answer Q1–Q10 canonically. It maps evidence to inform human/CTO decisions. No peer groups are created. No registry is mutated.

---

## Q1 — Peer Group Organization Principle

**Question**: Should peer groups be asset-level, narrative-level, sector-level, or multi-tag?

**Why it matters**: The organization principle determines the primary key of the registry and governs how SAI-BLK-21 queries peer definitions. An asset-level approach is simple but misses portfolio-level narrative clustering. A narrative-level approach requires the Narrative Registry to exist first. A sector-level approach may be too coarse for MoneyHorst's diagnostic depth.

**Relevant sources**: SRC-B-01, SRC-B-02, SRC-C-01, SRC-C-02, SRC-D-01

**Extracted evidence**:
- GICS (SRC-B-01, SRC-B-02): One primary sector/sub-industry classification per company per tier. Organization is asset-level with hierarchical sector context. Revenue drives the primary assignment. Earnings and market perception are supplemental. This establishes the global institutional precedent for asset-level primary classification with a four-tier hierarchy.
- ICB (SRC-C-01): Same single-classification-per-company principle with a four-tier hierarchy used by European exchanges. Confirms global convergence on asset-level primary classification.
- Porter (SRC-D-01): Competition for profits involves multiple competitive arenas. A platform company may compete in mobility, delivery, and payments simultaneously. No single GICS sub-industry captures UBER's full competitive context. This creates the case for a primary/adjacent structure that extends beyond a pure single-family taxonomy.

**Possible decision directions**:
- Option A: Asset-level with single primary family (GICS-consistent). Simple. Compatible with SAI interface. Cannot handle UBER/AMZN cross-family reality correctly.
- Option B: Asset-level with primary + secondary families. Extends GICS principle with role tiers. Supports cross-family candidates. Requires Q3 tier decision.
- Option C: Multi-tag without hierarchy. Maximum flexibility. No institutional precedent. Risk of ambiguity in SAI-BLK-21 peer consumption.
- Option D: Narrative-level organization. Not feasible until Narrative Registry exists. Deferred.

**Risks of wrong decision**:
- Option A: UBER, AMZN, VRT receive inadequate peer comparison due to forced single-family assignment.
- Option C: No stable primary family for SAI-BLK-21 to anchor peer comparison.
- Option D: Blocks registry creation indefinitely pending Narrative Registry.

**Future registry fields affected**: primary_family, secondary_family, peer_role, sector_reference, industry_reference, revenue_basis

**Open issues**: Whether narrative-level tagging should be a future additive-only extension to Option B rather than the primary organization principle.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q2 — Multi-Family Membership

**Question**: Should one asset belong to multiple peer families?

**Why it matters**: UBER spans mobility and delivery. AMZN spans retail, cloud, and logistics. VRT spans AI infrastructure and industrials/power. Without a multi-family decision, these assets receive either a narrowed peer set (incorrect) or trigger ad-hoc peer invention (prohibited).

**Relevant sources**: SRC-B-01, SRC-D-01

**Extracted evidence**:
- GICS (SRC-B-01): One primary classification per tier. GICS does NOT support multi-family membership. However, GICS acknowledges that revenue and earnings can diverge, which is the source of cross-family complexity that single-family approaches cannot resolve.
- Porter (SRC-D-01): A platform company competes in multiple competitive arenas simultaneously. Collapsing all competitive contexts into one peer group loses diagnostic precision. The five-forces framework implies that competitive context has multiple dimensions requiring separate treatment.

**Possible decision directions**:
- Option A: Single primary family only (GICS-consistent). Cannot handle UBER, AMZN, VRT correctly.
- Option B: Primary family + optional secondary family, with defined roles (core peer / adjacent / benchmark_context). Solves cross-family candidates. Requires Q3 tier decision.
- Option C: Full multi-tag with no role hierarchy. No institutional precedent. Uncontrolled proliferation risk.

**Risks of wrong decision**:
- Option A: UBER compared only to rideshare peers; its delivery platform competitive position is invisible.
- Option C: SAI-BLK-21 cannot determine which peers to prioritize.

**Future registry fields affected**: primary_family, secondary_family, peer_role (core / adjacent / benchmark_context / excluded)

**Open issues**: How many secondary families are allowed per asset. Whether secondary family assignments require the same level of governance as primary assignments.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q3 — Primary vs. Secondary Membership Tiers

**Question**: Should peers have primary vs. secondary membership tiers?

**Why it matters**: Not all peers in a family are equally comparable. A direct competitor (CRWD vs. PANW) is more meaningful than an adjacent observability platform (DDOG). SAI-BLK-21 needs to know which peers to weight more heavily in peer-relative diagnostic observations.

**Relevant sources**: SRC-D-01, SRC-E-01, SRC-E-03, SRC-B-01

**Extracted evidence**:
- Porter (SRC-D-01): Direct rivals are the closest competitive peers. Substitutes and ecosystem participants are secondary competitive context. Maps directly to core peer (direct rival) vs. adjacent peer (substitute or ecosystem adjacent).
- Damodaran (SRC-E-01, SRC-E-03): Comparable company analysis requires adjusting for differences in fundamentals when peers are not perfectly comparable. The better the peer set, the less adjustment required. Implicitly supports a tiered structure where core peers meet all financial comparability gates and adjacent peers require adjustment notes.
- GICS (SRC-B-01): Does not define membership tiers within a sub-industry — a known limitation for heterogeneous sub-industries.

**Possible decision directions**:
- Option A: No tiers — all peers in a family are equal. Loses precision.
- Option B: Two tiers — core peer (direct rival, meets all comparability gates) and adjacent peer (partially comparable, requires note). Supported by Porter and Damodaran.
- Option C: Three tiers — core, adjacent, benchmark_context. Benchmark_context is already a separate non-peer role. Three tiers for company peers adds governance complexity.

**Risks of wrong decision**:
- Option A: SAI-BLK-21 cannot distinguish NVDA/AMD as direct peers from SMCI as adjacent infrastructure peer.
- Option C: Over-engineered; increases registry maintenance burden.

**Future registry fields affected**: peer_role (core / adjacent / benchmark_context / excluded), financial_comparability_gate, comparability_score_inputs

**Open issues**: Whether the peer_role field uses human-assigned labels or rule-derived labels from financial comparability gates. Whether adjacency requires formal documentation of the comparability limitation.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q4 — ADR / European Ticker / Cross-Listing Normalization

**Question**: How should ADRs, European tickers, and US listings of the same economic entity be normalized?

**Why it matters**: ASML has a primary Euronext listing and a Nasdaq ADR. Rheinmetall is on Frankfurt only. If the registry stores them as separate entities by ticker, peer comparison will double-count economic exposure and break when tickers change.

**Relevant sources**: SRC-G-01, SRC-G-02, SRC-G-03

**Extracted evidence**:
- OpenFIGI (SRC-G-01): One FIGI per instrument per listing venue. ASML has a distinct FIGI for Euronext and for Nasdaq. Both represent the same economic entity. A canonical entity layer above individual FIGIs is required to represent the company.
- Security master architecture (SRC-G-02): Canonical pattern is an internal entity identifier as primary key, with FIGI/ISIN/ticker as mapped attributes. Ticker symbols are not stable — they change on relisting and acquisition.
- OpenSanctions (SRC-G-03): ISINs are security-level identifiers, not company-level. The ISIN identifies the instrument; the issuer is a separate entity object.

**Possible decision directions**:
- Option A: Use ticker + exchange as peer identifier. Not stable. Will break on relisting.
- Option B: Use ISIN as peer identifier. More stable than ticker but still security-level.
- Option C: Use canonical_entity_id as primary key (internal or external company ID), with FIGI/ISIN/ticker as lookup attributes. Correct. Requires entity master layer.
- Option D: Use FIGI as peer identifier. Open standard. Still listing-level; requires aggregation layer.

**Risks of wrong decision**:
- Option A/B: Registry will contain duplicate entries for cross-listed companies. Peer comparison double-counts economic exposure.
- Option C infrastructure risk: Entity master layer adds implementation dependency.

**Future registry fields affected**: canonical_entity_id, primary_listing, security_id, isin, figi, ticker, exchange, trading_currency, reporting_currency, domicile, listing_variant_type

**Open issues**: What external entity identifier to use as canonical_entity_id (LEI via GLEIF, proprietary company ID, or OpenFIGI composite?). Whether the registry layer or a separate entity master layer owns the entity-to-listing mapping.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q5 — ETF / Index Storage as Benchmark Context vs. Peers

**Question**: How should ETFs and indices be stored as benchmark context rather than peers?

**Why it matters**: ETFs and indices must not be company peers. They simultaneously serve as essential reference instruments. The registry must store them with a role that prevents peer comparison use while enabling benchmark_context use.

**Relevant sources**: SRC-F-01, SRC-F-02, SRC-F-03, SRC-F-04

**Extracted evidence**:
- Morningstar (SRC-F-01, SRC-F-04): ETF comparison requires a distinct field set (TER, tracking difference, tracking error, AUM, domicile, replication method, distribution policy, look-through concentration). These fields have no analogue in company peer comparison.
- Columbia Law (SRC-F-02): Similarly named ETFs can have materially different tracking errors and expense ratios. Multi-dimensional comparison is required; name/theme similarity alone does not create a valid peer group.
- etf.com (SRC-F-03): Funds tracking the same index form the most natural peer group for tracking difference comparison. This defines the ETF peer universe boundary: same index = peer group.

**Possible decision directions**:
- Option A: Store ETFs only in PGF-09 with role: `benchmark_context` or `etf_peer`. Company peer groups never contain ETFs.
- Option B: Store ETFs in both company families (as benchmark_context) and PGF-09 (as etf_peer), with explicit role labeling preventing category errors.

**Risks of wrong decision**:
- Mixing ETFs into company peer groups without role labeling produces category errors (QQQ compared as a peer to NVDA).
- Excluding ETFs entirely from company families removes formally recorded benchmark context instruments.

**Future registry fields affected**: fund_peer_group, benchmark_index, TER, AUM, tracking_error, tracking_difference, spread, holdings_overlap, domicile, replication_method, distribution_policy, lookthrough_concentration, asset_type, role

**Open issues**: Whether indices (S&P 500, Nasdaq-100) can be stored in the peer group registry with asset_type: `index` and role: `benchmark_context`. Whether UCITS and 1940-Act variants of the same index ETF are separate peer group members or linked variants.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q6 — Liquidity / Market-Cap Thresholds

**Question**: How should liquidity and market-cap thresholds be handled in peer group assignment?

**Why it matters**: A $1B mid-cap assigned to the same peer group as a $3T mega-cap produces misleading multiples. Liquidity thresholds affect whether peer comparison data is available at all.

**Relevant sources**: SRC-E-01, SRC-E-02, SRC-F-01

**Extracted evidence**:
- Damodaran (SRC-E-01): Size comparability is one of the core financial comparability gates. A small-cap and a mega-cap in the same GICS sub-industry have different risk, liquidity, and multiple profiles. They are not directly comparable without adjustment. The quality of the peer set determines the quality of relative valuation.
- Investopedia (SRC-E-02): Standard comps practice requires similar financial profile including size.
- Morningstar (SRC-F-01): ETF liquidity (ADV, bid-ask spread) is a required ETF comparison dimension. By analogy, company liquidity thresholds should be documented in the registry.

**Possible decision directions**:
- Option A: No explicit thresholds — all companies in a family can peer any other regardless of size.
- Option B: Soft thresholds — document market-cap range and liquidity profile per peer group; flag materially out-of-range peers as comparability_note_required.
- Option C: Hard thresholds — companies outside a defined market-cap range are excluded from core membership. Requires explicit numeric threshold definitions.

**Risks of wrong decision**:
- Option A: NVDA at $3T compared to a $5B AI chip designer produces structurally misleading multiple comparisons.
- Option C: Wrong thresholds exclude valid peers. Threshold definitions require index construction methodology sourcing not yet in this registry.

**Future registry fields affected**: comparability_score_inputs, financial_comparability_gate, allowed_metric_set, blocked_metric_set

**Open issues**: Who defines market-cap and liquidity threshold values. Whether thresholds are updated annually with peer group review. Whether adjacent peers can span broader size ranges than core peers.

**Readiness status**: EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED — the principle is well-evidenced but specific numeric threshold definitions require additional sourcing from index construction methodology documents (e.g., Russell index methodology, MSCI index construction rules).

---

## Q7 — Private / Non-Listed Comparables

**Question**: How should private and non-listed comparables be handled?

**Why it matters**: Some competitive peers of MoneyHorst-covered companies are not publicly listed. Treating absence from the registry as absence from competitive reality is a diagnostic gap.

**Relevant sources**: SRC-E-01 (by implication — comps framework is public-markets focused), SRC-G-01 (by implication — FIGI covers listed instruments only)

**Extracted evidence**:
- Damodaran (SRC-E-01): Comparable company analysis is fundamentally a public markets exercise. Private comparable valuation uses different techniques (private company discounts, lack of marketability adjustments). Direct comparison of public and private companies on market multiples is not valid.
- OpenFIGI (SRC-G-01): FIGI covers financial instruments on exchanges. Private companies do not have FIGIs. The identification infrastructure for private companies is fundamentally different.

**Possible decision directions**:
- Option A: Exclude private companies entirely from the registry.
- Option B: Store private comparables in a separate role (asset_type: `private`, role: `private_comparable`). Never used in valuation-based peer comparison but noted as competitive context.
- Option C: Defer to a future registry extension. Reasonable given the infrastructure complexity.

**Risks of wrong decision**:
- Option A: SpaceX (PGF-06 context), ByteDance (PGF-05 context), Stripe (PGF-03 context) are competitive peers with no public listing. Their exclusion creates systematic coverage gaps.
- Option B risk: Private company data freshness and reliability are difficult to maintain systematically.

**Future registry fields affected**: asset_type (private), role (private_comparable), canonical_entity_id (requires non-FIGI/ISIN approach)

**Open issues**: What identifier to use for private companies. Who maintains private comparable data. Whether private comparables affect SAI-BLK-21 peer comparison outputs or are documentation-only.

**Readiness status**: EVIDENCE_INSUFFICIENT — no source in the current registry addresses private comparable methodology at the required depth. Additional research required from M&A advisory or private equity valuation methodology sources.

---

## Q8 — Cross-Region Peer Handling (GAAP vs. IFRS / Currency / Taxonomy)

**Question**: How should cross-region peers be handled?

**Why it matters**: Multiple MoneyHorst families include non-US peers. Direct comparison of EUR/IFRS-reporting European companies to USD/GAAP-reporting US companies on raw financials produces misleading outputs.

**Relevant sources**: SRC-C-01, SRC-G-01, SRC-G-02, SRC-H-01, SRC-H-02, SRC-H-03

**Extracted evidence**:
- ICB (SRC-C-01): European exchanges use ICB; US exchanges use GICS. Cross-taxonomy reconciliation is required when comparing US-listed and European-listed peers.
- FIGI / Security master (SRC-G-01, SRC-G-02): Trading currency and reporting currency must be stored separately. Canonical entity ID must be independent of listing venue.
- IFRS 8 (SRC-H-01): Segment reporting under IFRS uses management approach (CODM view), which may differ from external IFRS statement figures. Geographic segment aggregation varies.
- KPMG (SRC-H-02): R&D capitalization differs (IFRS allows development phase; GAAP does not), lease accounting differs in detail, and financial instrument classification differs. These create material P&L and balance sheet non-comparability across regions.
- PwC (SRC-H-03): LIFO inventory method is prohibited under IFRS; permitted under GAAP. Significant for manufacturing peers.

**Possible decision directions**:
- Option A: Accept cross-region peers with comparability_adjustment_required flag and accounting_standard field per peer. Audit trail created; comparison not blocked.
- Option B: Separate European peers into distinct regional subclusters within families.
- Option C: Block cross-region peers from core peer role; adjacent only. Cannot be applied to ASML or Rheinmetall without creating critical coverage gaps.

**Risks of wrong decision**:
- Option A without enforcement: The flag becomes decorative, not functional.
- Option C: ASML and Rheinmetall cannot be excluded from their respective families without creating significant coverage gaps.

**Future registry fields affected**: accounting_standard, reporting_currency, trading_currency, fiscal_year_end, restatement_flag, comparability_adjustment_required, domicile, listing_exchange, taxonomy_reference (GICS vs. ICB)

**Open issues**: Whether fiscal year-end misalignment requires an additional alignment_period field. Whether currency-adjusted metrics are computed at the registry layer or at the SAI-BLK-21 consumption layer.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q9 — Subcluster Governance and Validation

**Question**: How should subcluster membership be validated and governed?

**Why it matters**: Without governance, subclusters drift as companies evolve, merge, or change business models. Silent subcluster drift means the system reports peer comparisons that no longer reflect competitive reality.

**Relevant sources**: SRC-A-01, SRC-A-02, SRC-A-03, SRC-B-03, SRC-C-01

**Extracted evidence**:
- GIPS (SRC-A-01, SRC-A-02, SRC-A-03): Fair representation and full disclosure require that methodology choices (including subcluster definitions) be documented, versioned, and periodically reviewed. Cherry-picking is prohibited — subcluster definitions must not be altered to favor a particular diagnostic outcome.
- GICS versioning (SRC-B-03): Classification changes require advance notice and transition periods. Historical classification data is retained for backtesting. The 2018 GICS Communication Services reclassification is a documented precedent for managed, versioned taxonomy change.
- ICB governance (SRC-C-01): External advisory process and challenge/appeal concept. A formal review process prevents classification capture.

**Possible decision directions**:
- Option A: Manual CTO governance only — ad-hoc approval of subcluster changes. Simple. Risk of inconsistent standards over time.
- Option B: Annual review cycle — all subcluster assignments reviewed annually using a documented criteria set. Aligned with GICS and GIPS precedent.
- Option C: Event-triggered review — subcluster assignments reviewed when material business model change occurs. More responsive. Requires trigger definition.

**Risks of wrong decision**:
- Option A: Subcluster drift goes undetected. No systematic process catches reclassification needs.
- Option B: Annual review may be too infrequent for fast-moving tech sectors.

**Future registry fields affected**: lifecycle_status, review_cycle, effective_date, change_reason, source_authority, approved_by, challenge_status, review_status, methodology_version

**Open issues**: Whether to adopt an ICB-style external advisory process or keep governance CTO-internal. Trigger criteria for event-driven review need explicit definition.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Q10 — Peer Group Versioning

**Question**: Should peer groups version over time?

**Why it matters**: Companies change business models. If peer groups do not version, historical peer comparisons become meaningless — an asset is retrospectively compared to peers it was never in competition with.

**Relevant sources**: SRC-A-01, SRC-A-03, SRC-B-01, SRC-B-03, SRC-C-01

**Extracted evidence**:
- GIPS (SRC-A-01, SRC-A-03): Standards are periodically updated with documented rationale. Historical versions are retained for comparability. Versioning is a prerequisite for fair representation of historical performance.
- GICS annual review (SRC-B-01, SRC-B-03): GICS undergoes an annual review process. Changes are announced in advance, take effect on a specified date, and require transition periods. Historical classification data is retained for backtesting. The 2018 Communication Services reclassification is a documented example of a major versioned reclassification with material downstream effects.
- ICB (SRC-C-01): Rules-based methodology with documented review cycle. Version control is implicit in the external advisory process.

**Possible decision directions**:
- Option A: No versioning — peer groups are live records only. Historical comparability impossible.
- Option B: Effective_date versioning — each peer group record has an effective_date and optional end_date. Queries can retrieve peer groups as of any date. Aligned with GICS and GIPS precedent.
- Option C: Full audit trail versioning — every change creates a new version record. Maximum traceability. Higher storage/query complexity. Can be added later as an extension.

**Risks of wrong decision**:
- Option A: Registry will be stale within 12 months. Backtesting and historical diagnostic reproduction are impossible.
- Option C risk: Over-engineered for current phase. Option B can be extended to Option C later (additive-only).

**Future registry fields affected**: effective_date, end_date, lifecycle_status (active / deprecated / under_review), change_reason, methodology_version, review_cycle, approved_by

**Open issues**: Whether a subcluster composition change (adding one peer) triggers a new version of the entire peer group or only the modified record. Whether versioning applies to role changes (core to adjacent) or only to membership changes.

**Readiness status**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION

---

## Evidence Readiness Summary

| # | Question | Topic | Readiness Status |
|---|----------|-------|-----------------|
| Q1 | Organization principle | Asset-level vs. narrative-level | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q2 | Multi-family membership | Single vs. multi-family | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q3 | Membership tiers | Core vs. adjacent | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q4 | ADR / cross-listing | Canonical entity ID | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q5 | ETF/index storage | Benchmark_context role separation | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q6 | Liquidity / market-cap | Threshold definition | EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED |
| Q7 | Private comparables | Non-listed peer handling | EVIDENCE_INSUFFICIENT |
| Q8 | Cross-region GAAP/IFRS | Accounting comparability flags | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q9 | Subcluster governance | Review cycle and validation | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |
| Q10 | Versioning | Effective_date versioning | EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION |

**8 of 10 questions**: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION
**1 of 10 questions**: EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED (Q6)
**1 of 10 questions**: EVIDENCE_INSUFFICIENT (Q7)

---

*End of evidence matrix. Content was rephrased for compliance with licensing restrictions.*

---

## Addendum — Exchange / Market Data / Trading Readiness Relevance by Q1–Q10

**Boundary statement**: Market data and trading readiness evidence is included to prevent architectural drift. It does not authorize real-time market data consumption, broker integration, trading enablement, order-routing logic, or regulated activity.

The following table maps each design question Q1–Q10 to its market data, exchange, and trading readiness relevance. The scope classification distinguishes fields needed now in the data model (CURRENT_SCOPE) from fields only relevant when trading is enabled (FUTURE_SCOPE).

---

### Q1 — Peer Group Organization Principle

| Attribute | Value |
|-----------|-------|
| **relevance** | MEDIUM |
| **why it matters** | The organization principle must ensure the registry can distinguish economic entity from listing/security/venue. If peer groups are indexed by ticker rather than canonical_entity_id, the addition of real-time quote data will produce venue-specific duplicates for cross-listed assets. The choice of organization principle now determines whether the data model is compatible with future exchange connectivity. |
| **source evidence** | SRC-I-01 (ISO 10383 MIC — venue is not entity), SRC-I-02/03 (Euronext/Xetra: same company may have listings on multiple MIC-identified venues) |
| **future registry fields** | canonical_entity_id, exchange_mic, primary_listing |
| **hard requirement now or future-readiness** | CURRENT_SCOPE — canonical_entity_id as primary key (not ticker) must be in the current registry design to support future quote integration without architectural rewrite |
| **blocks methodology decisions** | No — organization principle decision is unblocked; but must include canonical_entity_id commitment |

---

### Q2 — Multi-Family Membership

| Attribute | Value |
|-----------|-------|
| **relevance** | LOW |
| **why it matters** | Multi-family membership does not directly affect exchange or market data architecture. However, if an asset has primary and secondary family assignments, each listing may have a different exchange_mic and data feed. The registry must be able to handle quote data from multiple venues for the same economic entity. |
| **source evidence** | SRC-I-01 (one FIGI/MIC per listing venue — same entity, multiple venues) |
| **future registry fields** | exchange_mic (per listing, not per family assignment) |
| **hard requirement now or future-readiness** | FUTURE_READINESS_ONLY — multi-family logic does not change exchange data model; it only requires that the entity-level quote aggregation layer handles multiple listings |
| **blocks methodology decisions** | No |

---

### Q3 — Primary vs. Secondary Membership Tiers

| Attribute | Value |
|-----------|-------|
| **relevance** | LOW |
| **why it matters** | Tier assignment (core vs. adjacent) does not directly affect market data architecture. Adjacent peers may have different liquidity profiles and exchange venues, which affects the data_latency_class and bid_ask_source fields for those peers, but this is a data quality note rather than a structural dependency. |
| **source evidence** | SRC-I-04 (Nasdaq: professional vs. non-professional data quality distinction applies to all listed assets regardless of peer role) |
| **future registry fields** | data_latency_class (relevant to comparability of quotes across core vs. adjacent peers) |
| **hard requirement now or future-readiness** | FUTURE_READINESS_ONLY — data quality flags per peer are a future enhancement, not blocking current tier design |
| **blocks methodology decisions** | No |

---

### Q4 — ADR / European Ticker / Cross-Listing Normalization

| Attribute | Value |
|-----------|-------|
| **relevance** | HIGH |
| **why it matters** | This is the question most directly affected by exchange and market data architecture. ASML has a primary listing on Euronext Amsterdam (XAMS, ISIN NL0010273215) and a secondary listing as a Nasdaq ADR. Rheinmetall is listed on Xetra (XETR). Each listing has a distinct MIC, distinct trading timezone, distinct market data licensing requirements, and potentially distinct bid/ask data sources. Without a canonical entity architecture and exchange_mic field in place now, adding real-time quote data later will require a structural registry rewrite. |
| **source evidence** | SRC-I-01 (ISO MIC), SRC-I-02 (Euronext data licensing for XAMS), SRC-I-03 (Deutsche Börse/Xetra for XETR), SRC-I-04 (Nasdaq for XNAS ADR listings), SRC-I-12 (Xetra timezone and calendar) |
| **future registry fields** | canonical_entity_id, exchange_mic, primary_listing, listing_variant_type (ADR, primary, GDR), trading_currency, reporting_currency, exchange_timezone, trading_calendar_id, adr_flag, depositary_receipt_ratio, market_data_source, data_vendor, data_latency_class |
| **hard requirement now or future-readiness** | CURRENT_SCOPE — canonical_entity_id, exchange_mic, primary_listing, trading_currency, exchange_timezone, and trading_calendar_id must be in the current registry design to prevent architectural rewrite when quote data is added |
| **blocks methodology decisions** | No — does not block Q4 methodology decision; strengthens the case for Option C (canonical_entity_id architecture) |

---

### Q5 — ETF / Index Storage as Benchmark Context vs. Peers

| Attribute | Value |
|-----------|-------|
| **relevance** | MEDIUM |
| **why it matters** | ETF benchmark instruments (QQQ, SMH, CIBR, XLF) each have their own MIC-identified listing venue and distinct market data licensing requirements. Index data (Nasdaq-100 index values) requires an index data license separate from the ETF quote data license. If the registry stores ETFs as benchmark_context without tracking their exchange_mic and index_license_required fields, adding real-time index and ETF data later will require a structural addition to existing records. |
| **source evidence** | SRC-I-04 (Nasdaq: index data license separate from quote data), SRC-I-02 (Euronext: index data licensing separate), SRC-I-07 (non-display derived data from indices requires non-display license) |
| **future registry fields** | exchange_mic (for ETF listings), index_license_required, data_latency_class, benchmark_index (canonical index name), tracking_difference (ETF-specific) |
| **hard requirement now or future-readiness** | CURRENT_SCOPE_FOR_DATA_MODEL — exchange_mic and index_license_required fields must be reserved in ETF/benchmark_context records; FUTURE_SCOPE for actual license acquisition |
| **blocks methodology decisions** | No |

---

### Q6 — Liquidity / Market-Cap Thresholds

| Attribute | Value |
|-----------|-------|
| **relevance** | HIGH |
| **why it matters** | Liquidity assessment for peer group thresholds depends on real-time or delayed bid/ask spread data and ADV (average daily volume) data. The quality of this data depends on the data_latency_class and bid_ask_source. A peer assessed for liquidity using delayed or low-quality data may be misclassified. Additionally, pre-trade controls (SEC Rule 15c3-5) impose max order value and price collar constraints that are directly linked to the liquidity profile of the asset. The liquidity threshold decision (Q6) and the pre-trade control vocabulary (SRC-I-10) use overlapping field concepts. |
| **source evidence** | SRC-I-04/05 (Nasdaq/NYSE: real-time data quality affects spread and volume measurement), SRC-I-10 (SEC 15c3-5: price collars and max order value as pre-trade controls linked to liquidity), SRC-I-09 (FINRA 5310: market character — liquidity, depth, volatility — as best execution factor) |
| **future registry fields** | data_latency_class, bid_ask_source, spread (ETF and company), ADV-based liquidity flag, price_collar_policy, max_order_value_policy |
| **hard requirement now or future-readiness** | CURRENT_SCOPE_FOR_DATA_MODEL — data_latency_class and bid_ask_source fields must be reserved; numeric threshold values remain a future decision (Q6 EVIDENCE_PARTIAL status unchanged) |
| **blocks methodology decisions** | No — but Q6's EVIDENCE_PARTIAL status extends to numeric threshold definitions, which depend on the quality of the liquidity data feed |

---

### Q7 — Private / Non-Listed Comparables

| Attribute | Value |
|-----------|-------|
| **relevance** | LOW |
| **why it matters** | Private companies have no exchange listing, no MIC, no real-time data entitlement, and no FIGI. They are structurally excluded from exchange-based market data architecture. This reinforces the EVIDENCE_INSUFFICIENT finding for Q7 and confirms that private comparable handling requires a separate data model that does not depend on exchange data infrastructure. |
| **source evidence** | SRC-I-01 (ISO MIC covers regulated and non-regulated markets — not private companies), SRC-G-01 (FIGI covers listed instruments only) |
| **future registry fields** | asset_type: private (no exchange_mic, no figi, no realtime_entitlement_required) |
| **hard requirement now or future-readiness** | FUTURE_READINESS_ONLY — private comparable architecture is explicitly out of scope for exchange-based data model |
| **blocks methodology decisions** | No — confirms that private comparables are a separate architecture track |

---

### Q8 — Cross-Region Peer Handling (GAAP / IFRS / Currency)

| Attribute | Value |
|-----------|-------|
| **relevance** | HIGH |
| **why it matters** | Cross-region peers have different exchange_mic values, different exchange_timezone settings, different trading calendars, and different data licensing frameworks (Euronext/MiFIR for EU peers vs. SEC/FINRA for US peers). Quote timestamps from XETR (CET) and XNAS (ET) must be normalized to a canonical reference time. Market data licensing regimes differ materially: EU markets operate under MiFIR data licensing; US markets under SEC/FINRA/exchange rules. Best execution obligations also differ between MiFID II (EU) and FINRA Rule 5310 (US). Cross-region peer data cannot be treated as homogeneous without explicit field-level normalization. |
| **source evidence** | SRC-I-01 (MIC per venue), SRC-I-02/03 (EU licensing framework), SRC-I-04/05 (US licensing framework), SRC-I-08 (MiFID II best execution — EU), SRC-I-09 (FINRA best execution — US), SRC-I-12 (Xetra CET timezone), SRC-I-13 (Nasdaq ET timezone) |
| **future registry fields** | exchange_mic, exchange_timezone, trading_calendar_id, market_data_source, data_vendor, data_latency_class, reporting_currency, trading_currency, timestamp_normalization_rules |
| **hard requirement now or future-readiness** | CURRENT_SCOPE — exchange_mic, exchange_timezone, and trading_calendar_id are current-scope fields; cross-region data normalization must be in the data model before any quote display is implemented |
| **blocks methodology decisions** | No — reinforces flag-based approach (comparability_adjustment_required) already supported by Q8 evidence |

---

### Q9 — Subcluster Governance and Validation

| Attribute | Value |
|-----------|-------|
| **relevance** | MEDIUM |
| **why it matters** | Exchange and regulatory frameworks establish the institutional precedent for governance processes that directly apply to subcluster management: annual review cycles (GICS, GIPS, MiFID II Article 27), documented change rationale (SEC 15c3-5), audit trails (SEC 15c3-5, MiFID II RTS 6), and challenge/appeal processes (ICB). These governance patterns confirm that the annual review + event-triggered review model for subcluster governance (Q9 decision direction) is consistent with institutional practice across multiple regulatory domains. |
| **source evidence** | SRC-I-08 (MiFID II Article 27: execution policy reviewed at least annually), SRC-I-10 (SEC 15c3-5: risk management controls reviewed regularly with documented remediation), SRC-I-11 (MiFID II RTS 6: annual certification of algorithmic trading systems) |
| **future registry fields** | review_cycle, effective_date, change_reason, audit_log_required, source_authority, approved_by |
| **hard requirement now or future-readiness** | CURRENT_SCOPE — governance fields (review_cycle, effective_date, approved_by, change_reason) are current-scope registry fields; audit_log_required is future-scope when regulated activity begins |
| **blocks methodology decisions** | No — strengthens the evidence base for annual + event-triggered review governance model |

---

### Q10 — Peer Group Versioning

| Attribute | Value |
|-----------|-------|
| **relevance** | MEDIUM |
| **why it matters** | Exchange data versioning and corporate action handling (stock splits, spinoffs, mergers) are well-established practices in market data infrastructure. The Nasdaq maintenance gap is explicitly designed for corporate action processing. Exchange listing changes (delistings, transfers, ADR terminations) require version-controlled peer group updates just as they require security master updates. The GICS and GIPS versioning patterns (Q10 primary evidence) are reinforced by exchange data lifecycle management practice. |
| **source evidence** | SRC-I-05 (NYSE: corporate actions governed by NYSE Regulation — events that may change a company's listing status), SRC-I-13 (Nasdaq: maintenance gap for corporate action processing) |
| **future registry fields** | effective_date, end_date, lifecycle_status, change_reason, corporate_action_source |
| **hard requirement now or future-readiness** | CURRENT_SCOPE — effective_date versioning is already the recommended Q10 approach; corporate_action_source field is reserved for future data integration |
| **blocks methodology decisions** | No — reinforces effective_date versioning as minimum standard |

---

## Addendum Readiness Summary

| Question | Trading/Market Data Relevance | Current Scope Fields Added | Future Scope Fields |
|----------|------------------------------|---------------------------|---------------------|
| Q1 | MEDIUM | canonical_entity_id commitment | — |
| Q2 | LOW | exchange_mic per listing | — |
| Q3 | LOW | data_latency_class note | — |
| Q4 | HIGH | exchange_mic, exchange_timezone, trading_calendar_id, market_data_source, data_vendor, data_latency_class | realtime_entitlement_required, bid_ask_source |
| Q5 | MEDIUM | exchange_mic, index_license_required | realtime_entitlement_required, non_display_usage_allowed |
| Q6 | HIGH | data_latency_class, bid_ask_source | price_collar_policy, max_order_value_policy |
| Q7 | LOW | asset_type: private (no exchange fields) | — |
| Q8 | HIGH | exchange_mic, exchange_timezone, trading_calendar_id, timestamp_normalization_rules | data licensing regime flags |
| Q9 | MEDIUM | review_cycle, effective_date, approved_by, change_reason | audit_log_required |
| Q10 | MEDIUM | effective_date, corporate_action_source | end_date, lifecycle_status |

**Conclusion**: Q4 and Q8 are the two questions with HIGH market data relevance. Both require current-scope registry fields (exchange_mic, exchange_timezone, trading_calendar_id) to be defined now to prevent architectural rewrite when quote data is added. These fields are compatible with the methodology decisions already supported by evidence. No methodology decision is blocked by the trading readiness addendum.

---

*End of evidence matrix addendum. Market data and trading readiness evidence is included to prevent architectural drift. It does not authorize real-time market data consumption, broker integration, trading enablement, order-routing logic, or regulated activity.*
