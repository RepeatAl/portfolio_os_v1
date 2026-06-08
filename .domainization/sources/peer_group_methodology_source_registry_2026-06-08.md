# Peer Group Methodology Source Registry

**Artifact**: peer_group_methodology_source_registry_2026-06-08.md
**Date**: 2026-06-08
**Branch**: spec/peer-group-methodology-source-screening
**Authority**: Research / Source Screening
**Status**: screening complete — NOT canonical methodology
**Purpose**: Canonical source registry for all institutional sources inspected for Peer Group Registry Methodology evidence.

This registry records every source inspected during the Peer Group Methodology Source Screening task. Sources are evaluated for authority tier, MoneyHorst applicability, Q1–Q10 mapping, and whether they support hard rules, soft context, or reference-only use.

**Hard boundaries**: This registry does not create peer groups, does not answer Q1–Q10 canonically, does not mutate any registry, and does not constitute a methodology decision. It is evidence only.

---

## Source Category A — GIPS Standards (Governance / Disclosure Authority)

---

### SRC-A-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-A-01 |
| **institution** | CFA Institute |
| **title** | GIPS Standards — Global Investment Performance Standards |
| **url** | https://rpc.cfainstitute.org/gips-standards |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Governance and disclosure authority for methodology transparency, versioning, and review governance. Not a peer classification system. |
| **Q1_Q10_mapping** | Q9 (subcluster governance and validation), Q10 (peer group versioning) |
| **extracted_principles** | (1) Fair representation principle: performance and methodology must be presented honestly, without cherry-picking. (2) Full disclosure principle: all relevant methodology choices, exceptions, and limitations must be disclosed. (3) Comparability principle: standardized calculation and presentation enables meaningful comparison. (4) Ethical presentation: prevents misleading outputs through methodology manipulation. (5) Voluntary adoption as credibility signal. (6) Versioning and review governance: standards are periodically updated with documented rationale. |
| **registry_fields_impacted** | source_authority, approved_by, effective_date, review_cycle, change_reason, disclosure_notes, methodology_version, exception_handling |
| **limitations** | GIPS governs investment performance reporting, not peer group classification. Principles apply by analogy to MoneyHorst methodology governance. Not a direct peer selection standard. |
| **licensing_or_access_notes** | CFA Institute copyright. Summary and principles may be cited; verbatim reproduction limited. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — principles of fair representation and full disclosure are directly applicable to peer group methodology disclosure requirements. |
| **rule_type** | soft_context — governance analogy; does not directly govern peer classification |

---

### SRC-A-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-A-02 |
| **institution** | CFA Institute |
| **title** | Standard III(D) — Performance Presentation |
| **url** | https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-d |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Analogy source for credible information presentation and avoiding misleading claims. Applicable to how peer group membership is communicated to end users. |
| **Q1_Q10_mapping** | Q9 (governance), Q10 (versioning) |
| **extracted_principles** | (1) Members must provide credible information and avoid misstating or misleading. (2) Performance claims must be supported by evidence. (3) Prohibition on cherry-picking favorable subsets. Analogy: peer group selection must not be cherry-picked to make an asset look strong or weak relative to peers. |
| **registry_fields_impacted** | disclosure_notes, methodology_version, source_authority |
| **limitations** | Applies to individual analyst conduct, not directly to system-level peer classification. Analogy use only. |
| **licensing_or_access_notes** | CFA Institute copyright. Publicly accessible summary. |
| **can_be_cited_in_methodology** | Yes — as governance analogy for disclosure standards. |
| **rule_type** | soft_context — governance analogy |

---

### SRC-A-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-A-03 |
| **institution** | CFA Institute |
| **title** | Introduction to the Global Investment Performance Standards (GIPS) — 2024 Refresher Reading |
| **url** | https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2024/introduction-gips |
| **access_date** | 2026-06-08 |
| **source_type** | educational_reference |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Clarifies that fair representation and full disclosure apply to methodology AND output. Directly applicable to peer group methodology transparency requirements. |
| **Q1_Q10_mapping** | Q9, Q10 |
| **extracted_principles** | (1) Standards govern both calculation (methodology) and presentation (output) — both layers must be transparent. (2) Comparability requires consistency: comparable entities must use the same methodology. (3) Annual review and update cycle as institutional practice. |
| **registry_fields_impacted** | methodology_version, review_cycle, disclosure_notes, effective_date |
| **limitations** | Performance-focused; classification-adjacent by analogy only. |
| **licensing_or_access_notes** | CFA Institute copyright. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | soft_context |

---

## Source Category B — GICS (Primary Taxonomy Reference)

---

### SRC-B-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-B-01 |
| **institution** | MSCI / S&P Dow Jones Indices |
| **title** | Global Industry Classification Standard (GICS) — Methodology |
| **url** | https://www.msci.com/our-solutions/indexes/gics/ |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Base taxonomy discipline reference. GICS provides the authoritative precedent for one primary classification per company, hierarchical organization (sector to sub-industry), revenue-based assignment, and annual review. MoneyHorst peer families should be compatible with or consciously depart from GICS with documented rationale. |
| **Q1_Q10_mapping** | Q1 (organization principle), Q2 (multi-family membership), Q3 (primary/secondary tiers), Q6 (liquidity/market-cap thresholds), Q10 (versioning) |
| **extracted_principles** | (1) Four-tier hierarchy: Sector, Industry Group, Industry, Sub-Industry. (2) One primary classification per company per tier — companies do not belong to multiple sectors simultaneously. (3) Principal business activity is the classification basis. (4) Revenue is the primary factor for determining principal business activity. (5) Earnings and market perception are secondary factors used during review. (6) Global standardized application across regions and exchanges. (7) Annual review process managed jointly by MSCI and S&P Global. (8) Portfolio use cases: sector exposure analysis, peer/index comparison, contribution analysis, factor-based strategies, sector rotation. |
| **registry_fields_impacted** | primary_family, primary_subcluster, sector_reference, industry_reference, revenue_basis, earnings_basis, market_perception_basis, review_cycle |
| **limitations** | GICS assigns one primary classification per company; does not support multi-family membership. MoneyHorst may depart for cross-family candidates (UBER, AMZN, VRT). Departure requires explicit documented rationale. GICS does not cover ETFs/funds or non-equity asset classes as company peers. |
| **licensing_or_access_notes** | GICS is a registered trademark of MSCI Inc. and S&P Global. Methodology document publicly available via MSCI and S&P. |
| **can_be_cited_in_methodology** | Yes — as reference taxonomy with explicit departure documentation where MoneyHorst diverges. |
| **rule_type** | hard_rule — one primary classification per company unless MoneyHorst explicitly decides to support multi-family with documented rationale per Q2 |

---

### SRC-B-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-B-02 |
| **institution** | S&P Global |
| **title** | GICS — Corporate Governance / Classification Methodology Detail |
| **url** | https://www.spglobal.com/spdji/en/landing/topic/gics |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Confirms the tripartite basis for GICS classification: revenue (primary), earnings (secondary), market perception (tertiary). Also confirms institutional legitimacy through engagement with asset owners and investment analysts. |
| **Q1_Q10_mapping** | Q1, Q6, Q10 |
| **extracted_principles** | (1) Revenue as key determinant of principal business activity. (2) Earnings and market perception as supplemental factors — prevents pure revenue-based errors when strategic identity diverges from largest revenue segment. (3) Global engagement with investment professionals as design input. |
| **registry_fields_impacted** | revenue_basis, earnings_basis, market_perception_basis, classification_rationale |
| **limitations** | Specific threshold criteria are not publicly disclosed in the methodology summary. |
| **licensing_or_access_notes** | S&P Global copyright. Publicly accessible methodology summary. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — revenue-primary classification basis |

---

### SRC-B-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-B-03 |
| **institution** | MSCI |
| **title** | GICS Changes: Risk Depends on How It Is Measured |
| **url** | https://www.msci.com/research-and-insights/blog-post/gics-changes-risk-depends-on-how-it-measured |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Confirms that GICS undergoes periodic structural changes with material downstream effects on portfolio composition and benchmarking. Directly relevant to Q10: peer group changes must be version-controlled to avoid silent drift in benchmark composition. |
| **Q1_Q10_mapping** | Q10 (versioning), Q9 (governance) |
| **extracted_principles** | (1) Classification changes have material impacts on index composition and risk measurement. (2) Changes require advance notice and transition periods. (3) Versionability of taxonomy is critical for historical consistency and audit trail. |
| **registry_fields_impacted** | review_cycle, effective_date, change_reason, methodology_version, lifecycle_status |
| **limitations** | Focused on index-level impact rather than individual company peer group implications. |
| **licensing_or_access_notes** | MSCI copyright. Publicly accessible research post. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — versioning and change management required |

---

## Source Category C — ICB (Second Taxonomy Reference)

---

### SRC-C-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-C-01 |
| **institution** | FTSE Russell / LSEG |
| **title** | Industry Classification Benchmark (ICB) — Methodology Overview |
| **url** | https://lseg.com/en/ftse-russell/industry-classification-benchmark-icb |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Second taxonomy benchmark. ICB is rules-based and transparent, used by LSE, Euronext, and major European markets. Relevant for Q8 since European assets may be ICB-classified, not GICS. Also provides external advisory process and challenge/appeal concept for Q9. |
| **Q1_Q10_mapping** | Q1 (organization principle), Q8 (cross-region handling), Q9 (governance and validation), Q10 (versioning) |
| **extracted_principles** | (1) Rules-based and transparent methodology — classification criteria are publicly documented. (2) Four-tier taxonomy: Industry, Supersector, Sector, Subsector. (3) Primary source of revenue and other publicly available information as classification basis. (4) External advisory / governance process — classification decisions reviewed by external body. (5) Classification challenge / appeal concept — formal documented review process. (6) Used by London Stock Exchange, Euronext, and multiple major European exchanges. |
| **registry_fields_impacted** | taxonomy_reference, public_evidence_basis, classification_rationale, challenge_status, review_status, listing_exchange |
| **limitations** | ICB and GICS do not map 1:1. Cross-taxonomy reconciliation required when comparing US-listed (GICS) and European-listed (ICB) peers. Material complexity for PGF-06, PGF-07, PGF-08. |
| **licensing_or_access_notes** | FTSE Russell / LSEG copyright. Methodology overview publicly accessible. Full rulebook may require LSEG access. |
| **can_be_cited_in_methodology** | Yes — as secondary taxonomy reference and governance model |
| **rule_type** | hard_rule — cross-region taxonomy reconciliation required; challenge/appeal process as governance precedent |

---

### SRC-C-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-C-02 |
| **institution** | FTSE Russell / LSEG |
| **title** | ADX Adopts FTSE Russell Industry Classification Benchmark — Press Release |
| **url** | https://www.lseg.com/en/media-centre/press-releases/ftse-russell/2022/adx-adopts-ftse-russell-industry-classification-benchmark |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Confirms that each company is allocated to the subsector most closely representing its business, by primary revenue source. Also confirms global exchange adoption of ICB. |
| **Q1_Q10_mapping** | Q1, Q8 |
| **extracted_principles** | (1) One subsector assignment per company — same single-classification principle as GICS. (2) Primary revenue source as classification basis. (3) Global exchange adoption signals institutional legitimacy. |
| **registry_fields_impacted** | primary_family, revenue_basis, listing_exchange |
| **limitations** | Press release — limited methodology depth. Supplementary to SRC-C-01. |
| **licensing_or_access_notes** | LSEG copyright. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as supplementary evidence |
| **rule_type** | soft_context |

---

## Source Category D — Porter's Five Forces (Strategic Peer Logic)

---

### SRC-D-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-D-01 |
| **institution** | Harvard Business Review / Michael E. Porter |
| **title** | The Five Competitive Forces That Shape Strategy |
| **url** | https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy |
| **access_date** | 2026-06-08 |
| **source_type** | academic |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Strategic peer logic authority. Porter establishes that competition for profits goes beyond direct rivals. Directly relevant to Q2 and Q3: a company may have direct peers, substitute peers, and ecosystem context (suppliers, customers, platforms). These roles must not be collapsed into one undifferentiated peer set. |
| **Q1_Q10_mapping** | Q1 (organization principle — direct vs. substitute vs. ecosystem), Q2 (multi-family membership), Q3 (primary/secondary tiers), Q9 (subcluster governance) |
| **extracted_principles** | (1) Competition is often defined too narrowly — direct rivals are only one of five competitive forces. (2) Five forces: direct rivalry, threat of new entrants, bargaining power of buyers, bargaining power of suppliers, threat of substitutes. (3) Direct rivals are not the only competitive threat — substitutes can erode profitability even outside the same GICS sub-industry. (4) Ecosystem context (suppliers and customers) creates strategic interdependency that must not be confused with peer comparability. (5) Understanding industry structure is prerequisite to defining a valid peer universe. |
| **registry_fields_impacted** | peer_role, direct_peer, substitute_peer, supplier_customer_context, platform_adjacent, ecosystem_context, blocked_comparison_reason |
| **limitations** | Five Forces is a strategic analysis framework, not a peer selection algorithm. Provides conceptual logic for distinguishing peer roles but does not produce peer lists or selection criteria. |
| **licensing_or_access_notes** | HBR copyright. Article available via HBR subscription. Widely cited in open educational resources. |
| **can_be_cited_in_methodology** | Yes — as strategic logic authority for peer role taxonomy |
| **rule_type** | hard_rule — direct peers and substitute peers must not be mixed without role labeling; ecosystem context must not automatically become peer context |

---

## Source Category E — Comparable Company Analysis (Financial Comparability Gates)

---

### SRC-E-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-E-01 |
| **institution** | NYU Stern / Aswath Damodaran |
| **title** | The Little Book of Valuation — Comparable Company Analysis |
| **url** | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook.htm |
| **access_date** | 2026-06-08 |
| **source_type** | academic |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Defines the financial comparability gates that determine whether a peer comparison is valid. Comparable companies must share similar business models, growth profiles, margin structures, and risk profiles. Governs Q3, Q6, Q8. |
| **Q1_Q10_mapping** | Q3 (primary/secondary tiers), Q6 (liquidity/market-cap thresholds), Q8 (cross-region GAAP/IFRS) |
| **extracted_principles** | (1) Comparable company analysis requires similar business models — similar products, customers, distribution, competitive dynamics. (2) Size comparability: a $1B and $500B company may be same sub-industry but have different risk, liquidity, and multiple profiles. (3) Growth profile comparability: high-growth vs. mature company multiples are not directly comparable. (4) Margin structure comparability: high-margin SaaS vs. low-margin hardware are not valid comps. (5) Capital intensity comparability: asset-light vs. asset-heavy produce structurally different return profiles. (6) Leverage/balance sheet: highly leveraged peers distort EV/EBITDA comparisons. (7) Accounting comparability: GAAP vs. IFRS differences in revenue recognition, R&D capitalization, lease treatment, and stock compensation create non-comparable financials. (8) Geography/currency: cross-region peers require adjustment for tax rates, cost structures, and currency exposure. (9) Relative valuation requires a normalized peer set. |
| **registry_fields_impacted** | comparability_score_inputs, allowed_metric_set, blocked_metric_set, financial_comparability_gate, valuation_peer_allowed |
| **limitations** | Peer selection criteria are implicit in the comparable company analysis framework rather than explicitly formalized as a selection algorithm. |
| **licensing_or_access_notes** | Publicly available via NYU Stern website. Books available commercially. Educational materials freely accessible. |
| **can_be_cited_in_methodology** | Yes — as primary financial comparability authority |
| **rule_type** | hard_rule — financial comparability gates are prerequisite to valid peer comparison |

---

### SRC-E-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-E-02 |
| **institution** | Investopedia (educational reference) |
| **title** | The Comparables Approach — Equity Valuation |
| **url** | https://www.investopedia.com/articles/investing/080913/equity-valuation-comparables-approach.asp |
| **access_date** | 2026-06-08 |
| **source_type** | educational_reference |
| **authority_tier** | Tier 3 |
| **MoneyHorst_use_case** | Secondary reference confirming that comparables must share industry, business model, growth, and financial profile. Useful for cross-referencing Damodaran principles. Not authoritative on its own. |
| **Q1_Q10_mapping** | Q3, Q6 |
| **extracted_principles** | (1) Comps require same industry, similar business model, similar growth, similar financial profile. (2) P/B, P/E, EV/EBITDA, PEG ratios are standard multiple families. (3) Multiple selection depends on what is meaningful for the asset class / sector. |
| **registry_fields_impacted** | allowed_metric_set, financial_comparability_gate |
| **limitations** | Tier 3 educational reference. Not a primary authority. Confirms widely accepted principles only. |
| **licensing_or_access_notes** | Investopedia — publicly accessible. |
| **can_be_cited_in_methodology** | Context reference only — not as standalone authority |
| **rule_type** | soft_context |

---

### SRC-E-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-E-03 |
| **institution** | Damodaran / NYU Stern |
| **title** | Damodaran on Relative Valuation |
| **url** | https://www.scribd.com/document/13346213/Damodaran-on-Relval |
| **access_date** | 2026-06-08 |
| **source_type** | academic |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Confirms that relative valuation requires adjusting for differences in fundamentals when peers are not perfectly comparable. Four-step framework: define multiple, describe statistical properties, analyze fundamental drivers, apply to comparable firms with adjustments. Relevant to how MoneyHorst should handle partial comparability. |
| **Q1_Q10_mapping** | Q3, Q6 |
| **extracted_principles** | (1) Relative valuation compares an asset's value to similar assets using standardized multiples. (2) Four-step process: define, describe statistically, analyze fundamentals, apply with adjustments. (3) Adjusting for differences in fundamentals is required when using imperfect comparables. (4) The better the peer set, the less adjustment required. |
| **registry_fields_impacted** | comparability_score_inputs, financial_comparability_gate, allowed_metric_set |
| **limitations** | Scribd-hosted document. Content is authentic Damodaran but accessed via third-party platform. |
| **licensing_or_access_notes** | Available via scribd.com and NYU Stern. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — relative valuation requires adjustment for fundamental differences |

---

## Source Category F — ETF / Fund Comparison Methodology

---

### SRC-F-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-F-01 |
| **institution** | Morningstar |
| **title** | Tracking Difference vs. Tracking Error: How to Analyze ETFs |
| **url** | https://morningstar.com/business/insights/blog/funds/etf-tracking-difference-error |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Establishes the primary ETF comparison metrics for PGF-09 and the fund_peer_group registry field set. Morningstar's framework is the institutional standard for ETF peer comparison. |
| **Q1_Q10_mapping** | Q5 (ETF/index storage), Q6 (liquidity) |
| **extracted_principles** | (1) Tracking difference measures cumulative deviation from benchmark — the most comprehensive cost measure. (2) Tracking error measures standard deviation of daily return differences — a risk/consistency measure. Both metrics are required. (3) ETFs with less liquid underlying securities exhibit larger tracking errors. (4) Replication method affects both tracking difference and tracking error. |
| **registry_fields_impacted** | tracking_error, tracking_difference, replication_method, fund_peer_group, benchmark_index |
| **limitations** | Focused on passive ETFs. Active ETF comparison requires additional metrics. |
| **licensing_or_access_notes** | Morningstar copyright. Publicly accessible via Morningstar Business Insights. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — tracking difference and tracking error are mandatory ETF peer comparison dimensions |

---

### SRC-F-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-F-02 |
| **institution** | Columbia Law School Blue Sky Blog |
| **title** | Exchange-Traded Confusion: How Industry Practices Undermine Product Comparisons in ETFs |
| **url** | https://clsbluesky.law.columbia.edu/2020/09/22/exchange-traded-confusion-how-industry-practices-undermine-product-comparisons-in-exchange-traded-funds |
| **access_date** | 2026-06-08 |
| **source_type** | academic |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Documents that similarly named ETFs can have very different tracking errors, expense ratios, and replication approaches. Supports the requirement that ETF peer comparison must use multiple dimensions, not name/theme similarity alone. |
| **Q1_Q10_mapping** | Q5 (ETF/index storage) |
| **extracted_principles** | (1) ETF naming conventions do not guarantee comparable products. (2) Tracking error varies significantly across similarly named ETFs. (3) Multi-dimensional comparison is required. (4) Expense ratios, replication method, and domicile create material differences among funds tracking the same index. |
| **registry_fields_impacted** | TER, tracking_error, replication_method, domicile, fund_peer_group |
| **limitations** | Academic/legal commentary. Not a formal methodology standard. |
| **licensing_or_access_notes** | Columbia Law School blog. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as evidence for multi-dimensional ETF comparison requirement |
| **rule_type** | hard_rule — ETF peer comparison must use multiple dimensions; name/theme similarity alone is insufficient |

---

### SRC-F-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-F-03 |
| **institution** | etf.com |
| **title** | Tracking Difference: The Perfect ETF Metric |
| **url** | https://etf.com/sections/blog/tracking-difference-perfect-etf-metric |
| **access_date** | 2026-06-08 |
| **source_type** | educational_reference |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Confirms tracking difference as the most comprehensive single metric for ETF cost comparison among ETFs tracking the same index. Supports the fund_peer_group field logic. |
| **Q1_Q10_mapping** | Q5 |
| **extracted_principles** | (1) Tracking difference calculated by comparing fund total return to benchmark total return over rolling 12-month windows. (2) Unlike TER, tracking difference captures all real costs including transaction costs, lending income, and optimization effects. (3) Funds tracking the same index form the most meaningful peer group for tracking difference comparison. |
| **registry_fields_impacted** | tracking_difference, benchmark_index, fund_peer_group |
| **limitations** | Tier 2 practitioner reference. Relies on FactSet data methodology. |
| **licensing_or_access_notes** | etf.com — publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as supporting reference |
| **rule_type** | soft_context |

---

### SRC-F-04

| Field | Value |
|-------|-------|
| **source_id** | SRC-F-04 |
| **institution** | Morningstar |
| **title** | One Year In, How Do Vanguard's ETFs Measure Up? |
| **url** | https://www.morningstar.co.uk/uk/news/109238/one-year-in-how-do-vanguards-etfs-measure-up.aspx |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Demonstrates TER comparison across ETFs tracking the same index. Confirms that domicile affects TER ranges. Supports Q5 and PGF-09 with domicile and UCITS/1940-Act distinction. |
| **Q1_Q10_mapping** | Q5 (ETF/index storage), Q6 (liquidity) |
| **extracted_principles** | (1) TER comparison is valid only among ETFs tracking the same underlying index. (2) European-domiciled (UCITS) and US-domiciled ETFs tracking the same index may have materially different TERs. (3) Domicile affects regulatory treatment, tax efficiency, and distribution policy. |
| **registry_fields_impacted** | TER, domicile, distribution_policy, benchmark_index, fund_peer_group |
| **limitations** | Older reference (2013). TER levels have changed. Principles remain valid. |
| **licensing_or_access_notes** | Morningstar copyright. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as supporting evidence for domicile field |
| **rule_type** | soft_context |

---

## Source Category G — Security Identification / ADR Normalization

---

### SRC-G-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-G-01 |
| **institution** | OpenFIGI (Bloomberg / OMG standard) |
| **title** | OpenFIGI — About and Features |
| **url** | https://www.openfigi.com/about |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | FIGI provides unique identification for financial instruments across all venues. A single economic entity may have a primary listing and multiple ADRs, each with a distinct FIGI. Enables canonical entity identification independent of listing venue. Directly supports Q4 and Q8. |
| **Q1_Q10_mapping** | Q4 (ADR / European ticker normalization), Q8 (cross-region handling) |
| **extracted_principles** | (1) FIGI is a 12-character alphanumeric identifier issued under OMG standard. (2) One FIGI per instrument per listing venue — a company on multiple exchanges has multiple FIGIs but represents one economic entity. (3) OpenFIGI API enables mapping from ticker / CUSIP / SEDOL / ISIN to FIGI. (4) FIGI included in ISO 20022 messaging standard and FIX protocol. (5) Recognized as official US data standard. (6) Covers equities, ETFs, indices, futures, options, and other instruments. |
| **registry_fields_impacted** | canonical_entity_id, figi, ticker, exchange, listing_variant_type |
| **limitations** | FIGI identifies listings (instrument + venue), not economic entities. A canonical entity identifier mapping multiple FIGIs to one company requires an additional master entity layer. |
| **licensing_or_access_notes** | OpenFIGI is open standard. API publicly accessible at no cost. |
| **can_be_cited_in_methodology** | Yes — as canonical instrument identification standard |
| **rule_type** | hard_rule — FIGI-based instrument identification required for cross-listed security normalization |

---

### SRC-G-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-G-02 |
| **institution** | Intrinio |
| **title** | Modern Security Master Architecture for Financial Data |
| **url** | https://intrinio.com/blog/modern-security-master-architecture-unifying-ticker-cusip-isin-and-figi-data-at-scale |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Describes the canonical security master architecture: internal entity identifier as primary key, with FIGI, CUSIP, ISIN, SEDOL, and ticker as external identifier attributes. This is the architectural pattern MoneyHorst must adopt to prevent duplicate exposure from cross-listed securities. |
| **Q1_Q10_mapping** | Q4, Q8 |
| **extracted_principles** | (1) Internal entity identifier as primary key — external identifiers are mapped attributes. (2) Ticker symbols are not stable — they change on acquisition, relisting, exchange transfer. (3) ISIN is more stable than ticker but still listing-specific. (4) Security master must distinguish between economic entity and its listing vehicles. |
| **registry_fields_impacted** | canonical_entity_id, primary_listing, security_id, isin, figi, ticker, exchange, listing_variant_type |
| **limitations** | Commercial fintech provider perspective. Architecture is sound but implementation-specific details vary. |
| **licensing_or_access_notes** | Intrinio blog. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as architecture reference |
| **rule_type** | hard_rule — canonical entity ID is required; ticker alone is insufficient as stable peer identifier |

---

### SRC-G-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-G-03 |
| **institution** | OpenSanctions |
| **title** | Securities Data in OpenSanctions |
| **url** | https://www.opensanctions.org/docs/data/securities |
| **access_date** | 2026-06-08 |
| **source_type** | educational_reference |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Confirms that ISINs are attributes of Security objects, not Company objects. The ISIN identifies the instrument, not the issuer. Peer groups should reference economic entities (companies), not individual listings. |
| **Q1_Q10_mapping** | Q4 |
| **extracted_principles** | (1) ISIN is a security-level identifier, not a company-level identifier. (2) A single company may have multiple ISIN-bearing securities. (3) Company identity and security identity must be modeled separately. |
| **registry_fields_impacted** | canonical_entity_id, isin, security_id, listing_variant_type |
| **limitations** | OpenSanctions context is compliance/sanctions, not financial analysis. Architecture principle is broadly applicable. |
| **licensing_or_access_notes** | Publicly accessible documentation. |
| **can_be_cited_in_methodology** | Yes — as entity/security distinction reference |
| **rule_type** | hard_rule — entity-level vs. security-level distinction must be preserved |

---

## Source Category H — Accounting Comparability

---

### SRC-H-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-H-01 |
| **institution** | IFRS Foundation |
| **title** | IFRS 8 — Operating Segments |
| **url** | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ifrs8.html |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | IFRS 8 requires segment disclosures enabling users to evaluate business activity nature across geographies. Relevant to Q8: when comparing US GAAP to IFRS companies, segment reporting bases may differ. IFRS 8 uses a management approach (what the CODM sees) vs. ASC 280's similar but differently aggregated approach. |
| **Q1_Q10_mapping** | Q8 (GAAP vs. IFRS handling) |
| **extracted_principles** | (1) IFRS 8 requires operating segment disclosures evaluating business activity nature and geographic economic environments. (2) Management approach: segments defined as what the CODM reviews — may differ from external financial statement figures. (3) Quantitative information uses internal management measures. (4) Geographic segment aggregation varies between companies. |
| **registry_fields_impacted** | accounting_standard, reporting_currency, fiscal_year_end, comparability_adjustment_required |
| **limitations** | IFRS 8 governs disclosure, not peer selection. Comparability implications must be interpreted. |
| **licensing_or_access_notes** | IFRS Foundation copyright. IFRS standards publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as accounting standard reference |
| **rule_type** | hard_rule — accounting standard must be recorded per peer; cross-standard comparison requires explicit comparability_adjustment_required flag |

---

### SRC-H-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-H-02 |
| **institution** | KPMG |
| **title** | IFRS Compared to US GAAP |
| **url** | https://kpmg.com/be/en/insights/ifrs-insights/climate/ifrs-compared-to-us-gaap.html |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Documents primary IFRS/GAAP comparability gaps: lease accounting (IFRS 16 vs. ASC 842 ROU asset treatment), R&D capitalization (IFRS allows development phase; GAAP expenses all), revenue recognition (substantially converged via IFRS 15 / ASC 606 but implementation differences remain), financial instrument classification, and disclosure granularity. These create non-comparability when cross-region peers are directly compared on raw financials. |
| **Q1_Q10_mapping** | Q8 (GAAP vs. IFRS handling) |
| **extracted_principles** | (1) Lease: IFRS 16 and ASC 842 both require ROU assets but treatment of short-term leases differs — affects EBITDA and leverage. (2) R&D: IFRS allows development-phase capitalization; GAAP does not — non-comparable P&L and balance sheet for R&D-intensive companies. (3) Revenue: IFRS 15 and ASC 606 substantially converged but implementation differences remain. (4) Financial instruments: classification categories differ. (5) Disclosure granularity differs across regions. |
| **registry_fields_impacted** | accounting_standard, comparability_adjustment_required, restatement_flag, fiscal_year_end |
| **limitations** | Focused on technical accounting differences. Practical comparability impact on multiples requires additional context. |
| **licensing_or_access_notes** | KPMG copyright. Publicly accessible via KPMG website. |
| **can_be_cited_in_methodology** | Yes — as primary GAAP/IFRS comparability reference |
| **rule_type** | hard_rule — GAAP/IFRS standard must be documented; raw cross-standard metric comparison requires comparability_adjustment_required flag |

---

### SRC-H-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-H-03 |
| **institution** | PwC |
| **title** | IFRS and US GAAP: Similarities and Differences Guide |
| **url** | https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/ifrs_and_us_gaap_sim/ifrs_and_us_gaap_sim_US/About-this-guide.html |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Supplements SRC-H-02 with additional GAAP/IFRS coverage including inventory (LIFO prohibited under IFRS), revenue, financial instruments, and impairment. Together with SRC-H-02, establishes a complete picture of cross-standard comparability requirements for the methodology framework. |
| **Q1_Q10_mapping** | Q8 |
| **extracted_principles** | (1) Inventory: LIFO prohibited under IFRS; permitted under GAAP — significant for companies with large inventory. (2) Financial instruments classification differs — affects balance sheet and OCI treatment. (3) Impairment: IFRS uses expected loss model; GAAP uses incurred loss for most non-financial assets. (4) Revenue recognition: IFRS 15 / ASC 606 substantially converged but industry-specific differences remain. |
| **registry_fields_impacted** | accounting_standard, comparability_adjustment_required |
| **limitations** | PwC reference is practitioner-facing. Requires professional judgment in application. |
| **licensing_or_access_notes** | PwC copyright. Guide accessible via PwC Viewpoint. |
| **can_be_cited_in_methodology** | Yes — as secondary GAAP/IFRS reference |
| **rule_type** | hard_rule — supplementary to SRC-H-02 |

---

## Source Registry Summary

| source_id | Institution | Category | Authority | Q-Mapping | Rule Type |
|-----------|-------------|----------|-----------|-----------|-----------|
| SRC-A-01 | CFA Institute | GIPS | Tier 1 | Q9, Q10 | soft_context |
| SRC-A-02 | CFA Institute | GIPS | Tier 1 | Q9, Q10 | soft_context |
| SRC-A-03 | CFA Institute | GIPS | Tier 1 | Q9, Q10 | soft_context |
| SRC-B-01 | MSCI / S&P | GICS | Tier 1 | Q1, Q2, Q3, Q6, Q10 | hard_rule |
| SRC-B-02 | S&P Global | GICS | Tier 1 | Q1, Q6, Q10 | hard_rule |
| SRC-B-03 | MSCI | GICS | Tier 1 | Q9, Q10 | hard_rule |
| SRC-C-01 | FTSE Russell / LSEG | ICB | Tier 1 | Q1, Q8, Q9, Q10 | hard_rule |
| SRC-C-02 | FTSE Russell / LSEG | ICB | Tier 2 | Q1, Q8 | soft_context |
| SRC-D-01 | HBR / Porter | Five Forces | Tier 1 | Q1, Q2, Q3, Q9 | hard_rule |
| SRC-E-01 | NYU Stern / Damodaran | Comps | Tier 1 | Q3, Q6, Q8 | hard_rule |
| SRC-E-02 | Investopedia | Comps | Tier 3 | Q3, Q6 | soft_context |
| SRC-E-03 | Damodaran / NYU | Comps | Tier 1 | Q3, Q6 | hard_rule |
| SRC-F-01 | Morningstar | ETF | Tier 1 | Q5, Q6 | hard_rule |
| SRC-F-02 | Columbia Law | ETF | Tier 2 | Q5 | hard_rule |
| SRC-F-03 | etf.com | ETF | Tier 2 | Q5 | soft_context |
| SRC-F-04 | Morningstar | ETF | Tier 2 | Q5, Q6 | soft_context |
| SRC-G-01 | OpenFIGI | Identification | Tier 1 | Q4, Q8 | hard_rule |
| SRC-G-02 | Intrinio | Identification | Tier 2 | Q4, Q8 | hard_rule |
| SRC-G-03 | OpenSanctions | Identification | Tier 2 | Q4 | hard_rule |
| SRC-H-01 | IFRS Foundation | Accounting | Tier 1 | Q8 | hard_rule |
| SRC-H-02 | KPMG | Accounting | Tier 1 | Q8 | hard_rule |
| SRC-H-03 | PwC | Accounting | Tier 1 | Q8 | hard_rule |

**Total sources**: 22
**Tier 1 sources**: 15
**Tier 2 sources**: 5
**Tier 3 sources**: 2 (context reference only)
**Hard rules identified**: 14 source entries
**Soft context sources**: 8 source entries

---

*End of source registry. Content was rephrased for compliance with licensing restrictions.*

---

## Source Category I — Exchange Market Data, Identification, and Trading Readiness

**Boundary statement**: Market data and trading readiness evidence is included to prevent architectural drift. It does not authorize real-time market data consumption, broker integration, trading enablement, order-routing logic, or regulated activity. All regulatory references in this category are FUTURE_COMPLIANCE_REFERENCE only, not current legal obligations for MoneyHorst.

Category I sources are documented in full in the dedicated artifact:
`.domainization/reports/market_data_exchange_and_trading_readiness_evidence_2026-06-08.md`

The following summary registers all 13 Category I sources in the master source registry for cross-referencing.

| source_id | Institution | Subcategory | Authority | Q-Mapping | Rule Type | Scope |
|-----------|-------------|------------|-----------|-----------|-----------|-------|
| SRC-I-01 | ISO / SWIFT | Exchange ID (MIC) | Tier 1 | Q4, Q8 | hard_rule | CURRENT_SCOPE |
| SRC-I-02 | Euronext | Data Licensing | Tier 1 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-03 | Deutsche Börse / Xetra | Data Licensing | Tier 1 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-04 | NasdaqTrader | Data Licensing | Tier 1 | Q4, Q6 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-05 | NYSE Group | Data Licensing | Tier 1 | Q4, Q6 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-06 | LSEG Data Analytics | Data Vendor | Tier 1 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-07 | Euronext Athens | Non-Display Policy | Tier 2 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-08 | ESMA | MiFID II Best Execution | Tier 1 | Q4, Q6, Q8, Q9 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-09 | FINRA | Rule 5310 Best Execution | Tier 1 | Q4, Q6, Q8 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-10 | SEC | Rule 15c3-5 Market Access | Tier 1 | Q6, Q8, Q9 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-11 | ESMA | MiFID II RTS 6 Algo Trading | Tier 1 | Q6, Q9 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-12 | Deutsche Börse | Xetra Trading Calendar | Tier 1 | Q4, Q8 | hard_rule | CURRENT_SCOPE |
| SRC-I-13 | JD Supra / Nasdaq | Nasdaq Extended Hours | Tier 2 | Q4, Q6 | soft_context | CURRENT_SCOPE |

---

## Updated Source Registry Grand Total

| Category | Sources | Tier 1 | Hard Rules | Future Compliance |
|----------|---------|--------|-----------|-------------------|
| A — GIPS / CFA | 3 | 3 | 0 | 0 |
| B — GICS | 3 | 3 | 2 | 0 |
| C — ICB | 2 | 1 | 1 | 0 |
| D — Porter Five Forces | 1 | 1 | 1 | 0 |
| E — Comparable Company Analysis | 3 | 2 | 2 | 0 |
| F — ETF / Fund Methodology | 4 | 1 | 2 | 0 |
| G — Security Identification / ADR | 3 | 1 | 3 | 0 |
| H — Accounting Comparability | 3 | 3 | 3 | 0 |
| I — Exchange / Market Data / Trading | 13 | 11 | 7 | 4 |
| **Grand Total** | **35** | **26** | **21** | **4** |

---

*End of source registry addendum. Content was rephrased for compliance with licensing restrictions.*
