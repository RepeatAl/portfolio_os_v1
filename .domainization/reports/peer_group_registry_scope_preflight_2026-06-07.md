# Peer Group Registry Scope Preflight

**Report date**: 2026-06-07
**Branch**: spec/peer-group-registry-scope-preflight
**Authority**: CTO/operator scope confirmation
**Status**: preflight / candidate scope — NOT canonical registry
**Human confirmation required before any Peer Group Registry is created**

---

## 1. Purpose

This report prepares the scope for a future Peer Group Registry. It does NOT create canonical peer groups, does NOT finalize peer group IDs, and does NOT constitute a registry in any form.

The Peer Group Registry is a deferred framework dependency identified during Single Asset Intelligence Framework (SAI) task execution. SAI-BLK-21 (Peer Comparison) declared the registry dependency in its interface contract. This preflight documents the CTO-approved family scope, candidate universes, subcluster rules, benchmark/context rules, and open design questions that must be resolved by human/CTO decision before registry creation begins.

**This report is a governance preflight document only.** All 9 peer group families documented here are candidate scope, not canonical output.

---

## 2. Authority and Status

| Field | Value |
|-------|-------|
| Authority | CTO/operator scope confirmation (as of 2026-06-07) |
| Status | preflight / candidate scope |
| Canonical registry | NOT created by this report |
| Peer group IDs | NOT finalized |
| Human confirmation | REQUIRED before registry creation |
| Registry mutation | NONE performed |
| SAI artifact modification | NONE performed |
| Implementation code | NONE |

---

## 3. Source Files Inspected

The following repository files were inspected to produce this preflight report. Every claim in this document traces to one or more of these sources.

| # | File Path | Purpose |
|---|-----------|---------|
| 1 | `.kiro/specs/single-asset-intelligence-framework/artifacts/peer_benchmark.md` | SAI peer/benchmark artifact — defines SAI-BLK-21 interpretation scope, Peer Group Registry dependency, graceful degradation rules |
| 2 | `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` | SAI deferred interface contracts — Section 2.3 defines the Peer Group Registry interface contract from SAI perspective |
| 3 | `.kiro/specs/single-asset-intelligence-framework/artifacts/portfolio_fit_interface.md` | SAI portfolio fit interface — defines SAI-BLK-24 output dimensions and Portfolio Health Framework dependency |
| 4 | `.kiro/specs/single-asset-intelligence-framework/artifacts/README_single_asset_intelligence.md` | SAI framework README — canonical artifact map, 24-block list, unresolved items, deferred interface summary |
| 5 | `.domainization/reports/single_asset_intelligence_framework_task_execution_report_2026-06-06.md` | SAI final execution report — confirms SAI_TASK_EXECUTION_COMPLETE_WITH_REGISTRY_APPROVAL_PENDING, lists 3 unresolved gaps including Peer Group Registry |
| 6 | `.kiro/specs/single-asset-intelligence-framework/requirements.md` | SAI requirements — SAI-REQ-10 (Peer/Benchmark Reality Boundary); deferred dependency table listing peer_group_registry_yaml |
| 7 | `.domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md` | SAI preflight — cites peer_group_registry_yaml as MEDIUM priority missing upstream input |
| 8 | `.kiro/specs/single-asset-intelligence-framework/tasks.md` | SAI task plan — Task 11 (Peer/Benchmark Artifact) and Task 8 (Deferred Interface Contracts) |

### Repo-wide pattern search performed for:

- `peer group` — matches in peer_benchmark.md, deferred_interfaces.md, requirements.md, README_single_asset_intelligence.md, task execution reports
- `Peer Group Registry` — matches in deferred_interfaces.md (Section 2.3), requirements.md, SAI README, task execution report
- `benchmark` — matches in peer_benchmark.md, README_performance_benchmarks.md (domainization system performance tests — unrelated to financial benchmarks), deferred_interfaces.md
- `SAI-BLK-21` — matches in peer_benchmark.md, deferred_interfaces.md, README_single_asset_intelligence.md
- `correlation` — matches in peer_benchmark.md (SAI-BLK-20), README_report_output_registration.md, README_ssot_document_registration.md, README_engine_registration.md
- `portfolio fit` — matches in portfolio_fit_interface.md, README_single_asset_intelligence.md
- `peer_group_registry` — matches in requirements.md (deferred dependency table), SAI preflight 2026-06-05

**No existing Peer Group Registry artifact was found anywhere in the repository.** No peer group definitions, no peer group YAML files, no peer group spec exist at this time. This confirms that this preflight is the correct first step.

---

## 4. Relationship to SAI

### 4.1 SAI-BLK-21 Limitation

SAI-BLK-21 (Peer Comparison) is currently operating in severely limited mode because the Peer Group Registry is unavailable. Per the SAI deferred interface contract (`.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md`, Section 2.3):

> "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."

The block cannot produce peer-relative financial metric observations, competitive position interpretation, or peer-relative red flag assessment without canonical peer definitions.

### 4.2 SAI Consumes, Does Not Create

SAI expects the Peer Group Registry to provide canonical peer group definitions per asset, peer selection methodology, peer rotation rules, peer group versioning, and peer group validity metadata. SAI does NOT define peer groups, does NOT select peers, and does NOT create ad-hoc peer sets. This boundary is absolute per SAI-REQ-10.

### 4.3 Peer Group Registry Is a Deferred Framework Dependency

The Peer Group Registry is listed as Deferred Framework #3 in the SAI execution report, with status "Deferred — interface contract declared" and affected block SAI-BLK-21. It is also cited in the SAI preflight (2026-06-05) as a MEDIUM priority missing upstream input under artifact_id `peer_group_registry_yaml`.

### 4.4 This Preflight Does Not Modify SAI

This preflight report does not modify any SAI artifact, does not change any SAI verification gate, does not update any SAI requirement, and does not alter the SAI task plan. The SAI status remains SAI_TASK_EXECUTION_COMPLETE_WITH_REGISTRY_APPROVAL_PENDING. The 3 unresolved items documented in the SAI execution report remain unchanged.

### 4.5 Affected SAI Blocks (Summary)

| Block | Block Name | Impact | Status |
|-------|-----------|--------|--------|
| SAI-BLK-19 | Relative Strength | Partial — peer-relative strength unavailable | Benchmark and sector dimensions operational |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Partial — peer correlation unavailable | Benchmark and sector correlation operational |
| SAI-BLK-21 | Peer Comparison | Severe — primary function blocked | Only general competitive context without formal peer-relative metrics |

---

## 5. Confirmed Peer Group Families v0

The CTO/operator has confirmed 9 peer group families for candidate scope. These are candidate families only. No canonical peer group IDs are created here. Human/CTO confirmation is required before any of these become canonical registry entries.

---

### Family PGF-01 — AI Semiconductors / AI Infrastructure

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-01 |
| **family_name** | AI Semiconductors / AI Infrastructure |
| **purpose** | Peer context for assets in AI chip design, GPU architecture, semiconductor manufacturing equipment, and AI data center infrastructure adjacent to semiconductor supply chains |

**Core candidate universe:**
NVDA, AVGO, AMD, MRVL, MU, TSM, ASML, AMAT, LRCX, KLAC, ARM

**Adjacent / subcluster candidates:**
SMCI, DELL, HPE, VRT

**Subcluster notes:**
This family requires separation into at minimum two subclusters:
- *Subcluster A — Semiconductor Design / Fabless*: NVDA, AMD, MRVL, ARM (chip designers / fabless)
- *Subcluster B — Semiconductor Manufacturing / Equipment*: TSM (foundry), ASML, AMAT, LRCX, KLAC (equipment)
- *Subcluster C — AI Infrastructure / Data Center Adjacent*: SMCI, DELL, HPE, VRT (data center hardware, cooling, servers)

AVGO and MU may span subcluster A/B depending on portfolio classification approach.

**Benchmark/context instruments (candidate):** SOX (PHLX Semiconductor Index), SMH (VanEck Semiconductor ETF), QQQ (Nasdaq-100 — broad tech context)

**Boundary notes:**
- TSM (Taiwan-listed / NYSE ADR) requires ADR normalization decision (see Section 9, Q4)
- ASML (Amsterdam-listed / Nasdaq ADR) same
- European-listed tickers require explicit cross-region peer handling decision

**Unresolved decisions:**
- Whether AVGO (diversified semiconductors + software) belongs in PGF-01 or warrants its own subcluster
- Whether ARM (IP licensing model) is primary or adjacent
- Whether SMCI belongs in PGF-01 or in PGF-07 (Industrials/Power/Grid/Cooling)

---

### Family PGF-02 — Cybersecurity / SaaS Security

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-02 |
| **family_name** | Cybersecurity / SaaS Security |
| **purpose** | Peer context for assets in endpoint security, cloud security, network security, identity/access management, and security-adjacent observability platforms |

**Core candidate universe:**
CRWD, PANW, ZS, FTNT, CYBR, S, OKTA, NET, CHKP

**Adjacent / subcluster candidates:**
DDOG, TENB, RPD

**Subcluster notes:**
This family requires separation into at minimum three subclusters:
- *Subcluster A — Endpoint / XDR / Cloud Security*: CRWD, PANW (broad platform), ZS (cloud-native SASE), S (SentinelOne — endpoint/XDR platform candidate)
- *Subcluster B — Network / Perimeter Security*: FTNT, CHKP (legacy + next-gen network)
- *Subcluster C — Identity / Access Management*: CYBR (privileged access), OKTA (identity platform)
- *Subcluster D — Security-Adjacent Observability / Vulnerability Management*: DDOG, NET (observability and networking with security overlap — may be adjacent only), TENB (Tenable — vulnerability management), RPD (Rapid7 — exposure management / SIEM-adjacent)

CYBR prevents false peer comparison: CYBR privileged access management vs. CRWD endpoint detection are distinct competitive markets.

**Benchmark/context instruments (candidate):** CIBR (First Trust Cybersecurity ETF), HACK (ETFMG Prime Cyber Security ETF), IGV (iShares Expanded Tech-Software Sector ETF — broad SaaS context)

**Unresolved decisions:**
- Whether NET (Cloudflare) belongs in PGF-02 or PGF-01 (infrastructure adjacent)
- Whether DDOG is a security peer or observability-only peer (affects subcluster assignment)
- Whether TENB and RPD are adjacent peers or benchmark context only within PGF-02
- Whether CHKP (Israeli-listed / Nasdaq) requires cross-region normalization

---

### Family PGF-03 — Payments / Networks / Merchant Acquiring

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-03 |
| **family_name** | Payments / Networks / Merchant Acquiring |
| **purpose** | Peer context for assets across the payment value chain: card networks, merchant acquirers, payment processors, digital wallets, and credit-sensitive fintech platforms |

**Core candidate universe:**
V, MA, AXP, FI, FIS, GPN, ADYEN, PYPL, SQ (Block)

**Adjacent / subcluster candidates:**
TOST, AFRM, MELI, STNE

**Subcluster notes:**
This family requires clear separation to prevent false peer comparisons:
- *Subcluster A — Card Networks*: V, MA (duopoly network rails; asset-light, network effects model)
- *Subcluster B — Merchant Acquirers / Processors*: FI (Fiserv), FIS, GPN, ADYEN (transaction processing, gateway, acquiring)
- *Subcluster C — Wallets / Consumer Fintech*: PYPL, SQ/Block (consumer-facing digital payments)
- *Subcluster D — Credit-Sensitive Fintech*: AFRM, TOST (BNPL / credit exposure distinguishes from pure payment networks)

AFRM should never be directly peer-compared with V or MA without subcluster separation — materially different risk profiles.

**Benchmark/context instruments (candidate):** IPAY (ETFMG Prime Mobile Payments ETF), XLF (broad financials context)

**Unresolved decisions:**
- Whether AXP (closed-loop network + charge card) belongs in Subcluster A or a hybrid subcluster
- Whether ADYEN (Amsterdam-listed / Euronext) requires cross-region normalization
- Whether STNE / MELI (LatAm-focused) require a separate regional subcluster
- AFRM remains credit-sensitive fintech — must not be peer-compared with V or MA without subcluster separation

---

### Family PGF-04 — Mobility / Delivery / Local Commerce Platforms

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-04 |
| **family_name** | Mobility / Delivery / Local Commerce Platforms |
| **purpose** | Peer context for assets in rideshare, food/grocery delivery, travel platform, and local commerce aggregation |

**Core candidate universe:**
UBER, DASH, LYFT, ABNB, BKNG, EXPE, DHER, MEIT, GRAB

**Adjacent / subcluster candidates:**
RCL, CCL, MAR, HLT

**Subcluster notes:**
This family requires separation across distinct demand categories:
- *Subcluster A — Mobility Platforms*: UBER, LYFT (rideshare); UBER also spans delivery (multi-subcluster candidate)
- *Subcluster B — Delivery / Local Commerce*: DASH, DHER, MEIT (food/grocery/local commerce delivery marketplaces; MEIT = Meituan — China local commerce platform)
- *Subcluster C — Travel Platforms*: ABNB (short-term rental), BKNG, EXPE (OTA aggregators)
- *Subcluster D — Travel Demand Adjacent*: RCL, CCL (cruise), MAR, HLT (lodging chains — demand beneficiaries from travel platform volume, not platform operators)

GRAB (Southeast Asia super-app) spans mobility + delivery + payments — cross-region and cross-subcluster candidate.

**Benchmark/context instruments (candidate):** JETS (US Global Jets ETF — travel demand context)

**Unresolved decisions:**
- Whether UBER belongs in Subcluster A only or spans A and B as a platform
- Whether GRAB (Singapore-listed / NYSE ADR) warrants a regional subcluster
- Whether travel demand adjacent (RCL, MAR) are core peers or benchmark context only

---

### Family PGF-05 — Consumer / Retail / Event Consumption

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-05 |
| **family_name** | Consumer / Retail / Event Consumption |
| **purpose** | Peer context for assets in retail (mass, warehouse, specialty, e-commerce), consumer brands, restaurant chains, and event/experience consumption |

**Core candidate universe:**
WMT, COST, TGT, AMZN, NKE, ADS, MCD, QSR, SBUX, KO, PEP

**Adjacent / subcluster candidates:**
LULU, TJX, HD, LOW, CMG

**Subcluster notes:**
This is the broadest family and will likely require the most granular subcluster definitions:
- *Subcluster A — Retail (Mass / Warehouse)*: WMT, COST, TGT
- *Subcluster B — E-Commerce / Omnichannel*: AMZN (retail segment only — AMZN AWS is PGF-01 adjacent)
- *Subcluster C — Consumer Brands / Athletic*: NKE, ADS (Adidas — cross-region), LULU
- *Subcluster D — Restaurants / QSR*: MCD, QSR, SBUX, CMG
- *Subcluster E — Consumer Staples / Beverages*: KO, PEP
- *Subcluster F — Home Improvement / Specialty Retail*: HD, LOW, TJX

AMZN is a cross-family candidate: retail segment belongs in PGF-05 while AWS/cloud belongs adjacent to PGF-01; peer comparison requires segment-level scoping decision.

**Benchmark/context instruments (candidate):** XRT (SPDR S&P Retail ETF), XLP (Consumer Staples Select Sector SPDR), XLY (Consumer Discretionary Select Sector SPDR)

**Unresolved decisions:**
- How to handle multi-segment companies like AMZN (retail vs. cloud vs. logistics)
- Whether ADS (Frankfurt-listed) requires cross-region normalization
- How to define subcluster boundaries within PGF-05 given the breadth of the family

---

### Family PGF-06 — Defense / Security / C-UAS / Public Safety AI

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-06 |
| **family_name** | Defense / Security / C-UAS / Public Safety AI |
| **purpose** | Peer context for assets in defense prime contracting, advanced systems, counter-drone/C-UAS technology, public safety AI platforms, and European defense |

**Core candidate universe:**
PLTR, AXON, MSI, RTX, LMT, NOC, GD, Rheinmetall, Hensoldt, Thales, Leonardo, Saab

**Adjacent / subcluster candidates:**
KTOS, AVAV, LHX, BAE Systems

**Subcluster notes:**
This family spans distinct competitive markets that must not be collapsed:
- *Subcluster A — Defense Software / AI / Analytics*: PLTR (data analytics, defense AI), AXON (public safety technology)
- *Subcluster B — US Defense Primes*: RTX, LMT, NOC, GD, LHX (Tier-1 US defense contractors with full platform integration)
- *Subcluster C — European Defense*: Rheinmetall (Germany), Hensoldt (Germany — sensors/electronic warfare), Thales (France — defense electronics), Leonardo (Italy), Saab (Sweden), BAE Systems (UK)
- *Subcluster D — Drone / C-UAS / Unmanned Systems*: KTOS (Kratos Defense — unmanned systems, C-UAS), AVAV (AeroVironment — tactical UAS/C-UAS); AXON straddles public safety AI and law enforcement technology

PLTR should never be directly compared with LMT: analytics platform vs. defense prime are materially different business models and risk profiles.

**Benchmark/context instruments (candidate):** ITA (iShares U.S. Aerospace and Defense ETF), XAR (SPDR S&P Aerospace and Defense ETF)

**Boundary notes:**
- Rheinmetall, Hensoldt, Thales, Leonardo, Saab, BAE Systems are European-listed; cross-region normalization required (see Section 9, Q4 and Q8)
- Currency normalization required for EUR/GBP/SEK-denominated peers

**Unresolved decisions:**
- Whether PLTR belongs in PGF-06 or warrants its own software/AI platform family
- Whether public safety AI (AXON) is a primary peer for defense primes or adjacent only
- How to handle European defense rearmament context in peer group versioning (rapidly changing market caps)

---

### Family PGF-07 — Industrials / Power / Grid / Cooling

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-07 |
| **family_name** | Industrials / Power / Grid / Cooling |
| **purpose** | Peer context for assets in power infrastructure, grid electrification, AI data center power and cooling, industrial capital equipment, and building/climate systems |

**Core candidate universe:**
ETN, Schneider Electric, Siemens, ABB, VRT, Trane, Carrier, CAT, URI

**Adjacent / subcluster candidates:**
GE Vernova, Prysmian, Hubbell, Quanta Services

**Subcluster notes:**
This family spans capital goods, infrastructure, and AI-adjacent themes:
- *Subcluster A — Electrification / Grid Infrastructure*: ETN, Schneider Electric, Siemens, ABB, GE Vernova, Prysmian, Hubbell, Quanta Services (grid buildout, power distribution, HV cables, transmission construction)
- *Subcluster B — AI Data Center Power / Cooling*: VRT (Vertiv — power and cooling for data centers), Trane, Carrier (HVAC / thermal management with data center exposure)
- *Subcluster C — Industrial Capital Equipment / Rental*: CAT (construction/mining equipment), URI (United Rentals — equipment rental)

VRT appears in both PGF-01 (AI Infrastructure adjacent) and PGF-07 (Industrials/Power/Cooling) — cross-family assignment decision required.

**Benchmark/context instruments (candidate):** XLI (Industrials Select Sector SPDR), GRID (First Trust NASDAQ Clean Edge Smart Grid and Energy Innovation ETF)

**Boundary notes:**
- Schneider Electric (Paris-listed), Siemens (Frankfurt-listed), ABB (Zurich-listed), Prysmian (Milan-listed) are European-listed; cross-region normalization required
- Currency exposure: EUR/CHF-denominated peers

**Unresolved decisions:**
- Whether VRT belongs primarily in PGF-01, PGF-07, or spans both families (primary/secondary membership)
- Whether SMCI (from PGF-01 adjacent) overlaps with PGF-07
- Whether GE Vernova is core or adjacent given recent spinoff recency

---

### Family PGF-08 — Banks / Financials

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-08 |
| **family_name** | Banks / Financials |
| **purpose** | Peer context for assets in US money-center banking, investment banking, European banking, and regional banking; benchmark/context instruments for the broader financial sector |

**Core candidate universe:**
JPM, BAC, C, WFC, GS, MS, SAN, BNP, DB, UBS

**Benchmark/context instruments (candidate — not company peers):**
XLF (Financial Select Sector SPDR), EUFN (iShares MSCI Europe Financials ETF), SX7P (STOXX Europe 600 Banks Index — European banks benchmark context), KRE (SPDR S&P Regional Banking ETF — regional context)

**Subcluster notes:**
- *Subcluster A — US Money-Center Banks*: JPM, BAC, C, WFC (deposit base, retail/commercial banking scale)
- *Subcluster B — US Investment Banks / Universal Banks*: GS, MS (capital markets, wealth management focus)
- *Subcluster C — European Banks*: SAN (Santander — Spain/LatAm), BNP (France), DB (Deutsche Bank — Germany), UBS (Switzerland — post-Credit Suisse absorption)
- *Subcluster D — Regional Banks*: Separate subcluster required; regional banks have materially different risk profiles from money-center banks (deposit concentration, CRE exposure, liquidity dynamics)

GS and MS should not be directly peer-compared with retail-focused WFC or BAC without subcluster discipline; capital markets revenue mix is structurally different.

**Boundary notes:**
- SAN, BNP, DB are European-listed (EUR-denominated); UBS is CHF-denominated; cross-region handling required
- XLF, EUFN, SX7P, KRE are benchmark context only — not company peers

**Unresolved decisions:**
- Whether European banks belong in a dedicated PGF-08E subcluster or require their own family
- How to handle UBS given recent structural change (Credit Suisse absorption)
- Whether regional banks (KRE universe) require a PGF-08R subcluster or separate family

---

### Family PGF-09 — ETF / Fund Peer Rule

| Field | Value |
|-------|-------|
| **family_id candidate** | PGF-09 |
| **family_name** | ETF / Fund Peer Rule |
| **purpose** | Define peer comparison rules for ETF and fund assets; ETFs/funds do not receive company peer groups and must be compared against fund/ETF peers and benchmark context only |

**Rule statement:**
ETFs and funds do NOT receive company peer groups. Comparing an ETF with a constituent company is a category error and is architecturally prohibited.

**Required ETF/fund comparison dimensions (when Peer Group Registry is available):**

| Dimension | Description |
|-----------|-------------|
| Benchmark / index tracked | What index the ETF replicates |
| TER / fees | Total Expense Ratio — cost competitiveness vs. peer funds |
| AUM | Assets Under Management — scale and liquidity signal |
| Tracking error | Deviation from benchmark — replication quality |
| Liquidity / bid-ask spread | Market microstructure quality |
| Holdings overlap | Portfolio overlap with other ETFs covering same theme |
| Domicile | UCITS vs. 1940 Act vs. other regulatory structure |
| Distribution policy | Accumulating vs. distributing |
| Replication method | Physical full, physical sampled, synthetic (swap-based) |
| Concentration / look-through exposures | Top holdings weight, single-name concentration |

**Example — QQQ:**
QQQ (Invesco QQQ Trust) tracks the Nasdaq-100 Index. Its valid peers are other Nasdaq-100 / large-cap growth ETFs (e.g., QQQM, ONEQ, and Nasdaq-100 UCITS equivalents). QQQ must NOT be peer-compared with NVDA, MSFT, or AAPL as company peers — those are constituents, not peers. QQQ may use the Nasdaq-100 index as a benchmark/context instrument.

**Subcluster rule:**
ETF peer groups should be organized by:
- *Subcluster ETF-A — Thematic ETFs*: Technology, AI, cybersecurity, defense, clean energy
- *Subcluster ETF-B — Broad Market / Index ETFs*: S&P 500, Nasdaq-100, MSCI World, total market
- *Subcluster ETF-C — Sector ETFs*: XLF, XLI, XLY, XLK, XLE etc.
- *Subcluster ETF-D — Active / Semi-Active Funds*: Where fund comparison requires expense ratio and active share context

**Unresolved decisions:**
- How to handle UCITS vs. US-domiciled ETF peers (same index, different domicile)
- Whether leveraged/inverse ETFs require entirely separate peer universe
- How to normalize AUM and TER across USD and EUR-denominated fund share classes

---

## 6. Subcluster Rule (Global)

Each family documented in Section 5 may contain subclusters. Subclusters prevent false peer comparisons that arise when business models, risk profiles, or financial structures differ materially within a family.

**Prohibited false peer comparisons (examples):**

| Asset A | Asset B | False Comparison Reason |
|---------|---------|------------------------|
| PLTR | LMT | Analytics software platform vs. defense prime contractor |
| DELL | NVDA | Server/PC OEM vs. GPU/AI chip designer |
| DDOG | CRWD | Observability platform vs. endpoint security platform |
| AFRM | V or MA | BNPL with credit exposure vs. card network (asset-light rails) |
| QQQ | MSFT or NVDA | ETF vs. constituent company |

A subcluster assignment does NOT prevent cross-subcluster observation for specific diagnostic purposes (e.g., observing NVDA chip supply relative to semiconductor equipment peers). It prevents structural peer-ranking comparisons across dissimilar business models.

---

## 7. Benchmark / Context Rule (Global)

ETFs, indices, and sector funds may serve as benchmark or context instruments. They are NOT company peers unless the asset under analysis is itself an ETF or fund.

**Rules:**
1. Benchmark context instruments must be clearly labeled with `role: benchmark_context`
2. Benchmark context instruments must never be members of a company peer group
3. If an asset is an ETF/fund, it must be compared using PGF-09 rules, not company peer family rules
4. Index instruments (e.g., S&P 500, Nasdaq-100, STOXX 600) are benchmark context only — never peers
5. Sector ETFs (XLF, XLI, XLK, etc.) are benchmark context only for company assets; they are ETF peers only when the asset under analysis is a competing sector ETF

The benchmark/context instruments listed in each family profile (Section 5) are candidates for benchmark context only. They are not candidate company peers.

---

## 8. Proposed Future Artifact Model (Preliminary Only)

This section proposes a preliminary artifact model for the future Peer Group Registry. This is a suggestion only. No file is created by this report. Human/CTO design confirmation required before any registry artifact is created.

**Candidate future file locations:**
- `.kiro/specs/peer-group-registry-framework/` (spec-based approach, consistent with SAI)
- `.domainization/registries/peer_group_registry.yaml` (domainization registry approach)

**Candidate field model:**

| Field | Description |
|-------|-------------|
| `peer_group_id` | Canonical ID (e.g., PG-NVDA-AI-SEMI-01) |
| `family_id` | Parent family (e.g., PGF-01) |
| `family_name` | Human-readable family name |
| `subcluster_id` | Subcluster within family (e.g., PGF-01-SC-A) |
| `subcluster_name` | Human-readable subcluster name |
| `asset_id` / ticker / exchange | Asset identifier with exchange normalization |
| `role` | `core` / `adjacent` / `benchmark_context` / `excluded` |
| `asset_type` | `company` / `etf` / `index` / `fund` / `other` |
| `region` | US / EU / APAC / global |
| `currency` | Primary trading currency |
| `listing_exchange` | NYSE / Nasdaq / LSE / Xetra / Euronext / etc. |
| `source_authority` | Who approved this peer assignment |
| `effective_date` | When this assignment became active |
| `lifecycle_status` | `active` / `deprecated` / `under_review` |
| `notes` | Free-text context |
| `exclusions` / `non_peers` | Explicit exclusions with rationale |

**Not created here. Candidate only.**

---

## 9. Required Future Registry Design Questions

The following open questions require human/CTO decision before a Peer Group Registry can be created. No canonical answers exist at the time of this preflight.

| # | Question | Why It Matters |
|---|----------|---------------|
| Q1 | Should peer groups be asset-level, narrative-level, sector-level, or multi-tag? | Determines the primary organization principle of the registry |
| Q2 | Should one asset belong to multiple peer families? | UBER, AMZN, VRT are cross-family candidates — primary vs. secondary membership rule needed |
| Q3 | Should peers have primary vs. secondary membership tiers? | Affects how SAI-BLK-21 weights peer observations from different tiers |
| Q4 | How should ADRs / European tickers / US listings be normalized? | ASML, Rheinmetall, ADYEN, ADS are non-US primary listings with US ADRs |
| Q5 | How should ETFs and indices be stored as benchmark context rather than peers? | Prevents category errors in registry structure |
| Q6 | How should liquidity / market-cap thresholds be handled? | Small-cap peers may be inappropriate comparisons for large-cap assets |
| Q7 | How should private / non-listed comparables be handled? | Some competitive peers may not be publicly listed |
| Q8 | How should cross-region peers be handled? | USD vs. EUR vs. JPY reporting; GAAP vs. IFRS accounting standards |
| Q9 | How should subcluster membership be validated and governed? | Prevents subcluster drift over time; requires explicit governance |
| Q10 | Should peer groups version over time? | Companies change business models; peer composition should reflect current competitive reality |

---

## 10. Boundary Confirmations

| Item | Confirmed |
|------|-----------|
| No registry created | CONFIRMED |
| No peer group finalized | CONFIRMED |
| No canonical peer group IDs finalized | CONFIRMED |
| No SAI artifact modified | CONFIRMED |
| No registry / SSOT mutation | CONFIRMED |
| No implementation code | CONFIRMED |
| No scoring / ranking / recommendation / allocation / trading logic | CONFIRMED |
| No asset-to-narrative mapping | CONFIRMED |
| No ETF / company peer mixing | CONFIRMED |
| No new canonical registry creation | CONFIRMED |
| No SSOT mutation | CONFIRMED |

---

## 11. Preflight Result

```
PEER_GROUP_SCOPE_READY_FOR_HUMAN_REVIEW
```

**Rationale:**
- 9 peer group families confirmed by CTO/operator with explicit scope
- Candidate universes documented for all 9 families
- Subcluster rules identified for all families
- ETF/Fund peer rule defined (PGF-09)
- Benchmark/context rule documented globally
- Open design questions documented for human/CTO decision (Section 9, Q1–Q10)
- No blocking conflicts or contradictions detected
- No ambiguity in boundary scope — no registry created, no canonical groups finalized
- Source inspection complete — no pre-existing Peer Group Registry found in repository

Human/CTO confirmation is required before proceeding to registry creation.

---

*End of preflight report.*
