# Family Universe Intake Specification

> **Peer Group Registry Creation Preflight — Task 2: Family Universe Intake**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true

---

## Document Boundary

This artifact documents family universe intake structure only. It does not create candidate records, does not assign peers, does not create peer_group_id values, and does not create registry content. All data is sourced exclusively from the scope preflight document.

## Source Authority

**Sole family universe authority**: `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md`

**Rule**: No new family universe, ticker, subcluster, or benchmark instrument may be invented, added, or implied by this artifact. All content traces directly to the scope preflight Section 5.

---

## PGF-01 — AI Semiconductors / AI Infrastructure

| Field | Value |
|-------|-------|
| family_id | PGF-01 |
| family_name | AI Semiconductors / AI Infrastructure |
| source_section_reference | Section 5, Family PGF-01 |
| core_universe_count | 11 |
| adjacent_universe_count | 4 |
| core_candidate_tickers_from_source | NVDA, AVGO, AMD, MRVL, MU, TSM, ASML, AMAT, LRCX, KLAC, ARM |
| adjacent_candidate_tickers_from_source | SMCI, DELL, HPE, VRT |
| benchmark_context_candidates_from_source | SOX (PHLX Semiconductor Index), SMH (VanEck Semiconductor ETF), QQQ (Nasdaq-100) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-01", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Semiconductor Design / Fabless: NVDA, AMD, MRVL, ARM
- Subcluster B — Semiconductor Manufacturing / Equipment: TSM, ASML, AMAT, LRCX, KLAC
- Subcluster C — AI Infrastructure / Data Center Adjacent: SMCI, DELL, HPE, VRT
- Note: AVGO and MU may span subcluster A/B depending on classification approach

**Unresolved decisions from source**:
- Whether AVGO (diversified semiconductors + software) belongs in PGF-01 or warrants its own subcluster
- Whether ARM (IP licensing model) is primary or adjacent
- Whether SMCI belongs in PGF-01 or in PGF-07 (Industrials/Power/Grid/Cooling)

**Boundary notes from source**:
- TSM (Taiwan-listed / NYSE ADR) requires ADR normalization decision
- ASML (Amsterdam-listed / Nasdaq ADR) same
- European-listed tickers require explicit cross-region peer handling decision

---

## PGF-02 — Cybersecurity / SaaS Security

| Field | Value |
|-------|-------|
| family_id | PGF-02 |
| family_name | Cybersecurity / SaaS Security |
| source_section_reference | Section 5, Family PGF-02 |
| core_universe_count | 9 |
| adjacent_universe_count | 3 |
| core_candidate_tickers_from_source | CRWD, PANW, ZS, FTNT, CYBR, S, OKTA, NET, CHKP |
| adjacent_candidate_tickers_from_source | DDOG, TENB, RPD |
| benchmark_context_candidates_from_source | CIBR (First Trust Cybersecurity ETF), HACK (ETFMG Prime Cyber Security ETF), IGV (iShares Expanded Tech-Software Sector ETF) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-02", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Endpoint / XDR / Cloud Security: CRWD, PANW, ZS, S
- Subcluster B — Network / Perimeter Security: FTNT, CHKP
- Subcluster C — Identity / Access Management: CYBR, OKTA
- Subcluster D — Security-Adjacent Observability / Vulnerability Management: DDOG, NET, TENB, RPD

**Unresolved decisions from source**:
- Whether NET (Cloudflare) belongs in PGF-02 or PGF-01 (infrastructure adjacent)
- Whether DDOG is a security peer or observability-only peer
- Whether TENB and RPD are adjacent peers or benchmark context only within PGF-02
- Whether CHKP (Israeli-listed / Nasdaq) requires cross-region normalization

**Boundary notes from source**: (none explicitly listed)

---

## PGF-03 — Payments / Networks / Merchant Acquiring

| Field | Value |
|-------|-------|
| family_id | PGF-03 |
| family_name | Payments / Networks / Merchant Acquiring |
| source_section_reference | Section 5, Family PGF-03 |
| core_universe_count | 9 |
| adjacent_universe_count | 4 |
| core_candidate_tickers_from_source | V, MA, AXP, FI, FIS, GPN, ADYEN, PYPL, SQ (Block) |
| adjacent_candidate_tickers_from_source | TOST, AFRM, MELI, STNE |
| benchmark_context_candidates_from_source | IPAY (ETFMG Prime Mobile Payments ETF), XLF (broad financials context) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-03", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Card Networks: V, MA
- Subcluster B — Merchant Acquirers / Processors: FI (Fiserv), FIS, GPN, ADYEN
- Subcluster C — Wallets / Consumer Fintech: PYPL, SQ/Block
- Subcluster D — Credit-Sensitive Fintech: AFRM, TOST

**Unresolved decisions from source**:
- Whether AXP (closed-loop network + charge card) belongs in Subcluster A or a hybrid subcluster
- Whether ADYEN (Amsterdam-listed / Euronext) requires cross-region normalization
- Whether STNE / MELI (LatAm-focused) require a separate regional subcluster
- AFRM must not be peer-compared with V or MA without subcluster separation

**Boundary notes from source**: (none explicitly listed beyond subcluster separation requirement)

---

## PGF-04 — Mobility / Delivery / Local Commerce Platforms

| Field | Value |
|-------|-------|
| family_id | PGF-04 |
| family_name | Mobility / Delivery / Local Commerce Platforms |
| source_section_reference | Section 5, Family PGF-04 |
| core_universe_count | 9 |
| adjacent_universe_count | 4 |
| core_candidate_tickers_from_source | UBER, DASH, LYFT, ABNB, BKNG, EXPE, DHER, MEIT, GRAB |
| adjacent_candidate_tickers_from_source | RCL, CCL, MAR, HLT |
| benchmark_context_candidates_from_source | JETS (US Global Jets ETF) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-04", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Mobility Platforms: UBER, LYFT
- Subcluster B — Delivery / Local Commerce: DASH, DHER, MEIT
- Subcluster C — Travel Platforms: ABNB, BKNG, EXPE
- Subcluster D — Travel Demand Adjacent: RCL, CCL, MAR, HLT

**Unresolved decisions from source**:
- Whether UBER belongs in Subcluster A only or spans A and B as a platform
- Whether GRAB (Singapore-listed / NYSE ADR) warrants a regional subcluster
- Whether travel demand adjacent (RCL, MAR) are core peers or benchmark context only

**Boundary notes from source**: (none explicitly listed)

---

## PGF-05 — Consumer / Retail / Event Consumption

| Field | Value |
|-------|-------|
| family_id | PGF-05 |
| family_name | Consumer / Retail / Event Consumption |
| source_section_reference | Section 5, Family PGF-05 |
| core_universe_count | 11 |
| adjacent_universe_count | 5 |
| core_candidate_tickers_from_source | WMT, COST, TGT, AMZN, NKE, ADS, MCD, QSR, SBUX, KO, PEP |
| adjacent_candidate_tickers_from_source | LULU, TJX, HD, LOW, CMG |
| benchmark_context_candidates_from_source | XRT (SPDR S&P Retail ETF), XLP (Consumer Staples Select Sector SPDR), XLY (Consumer Discretionary Select Sector SPDR) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-05", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Retail (Mass / Warehouse): WMT, COST, TGT
- Subcluster B — E-Commerce / Omnichannel: AMZN (retail segment only)
- Subcluster C — Consumer Brands / Athletic: NKE, ADS, LULU
- Subcluster D — Restaurants / QSR: MCD, QSR, SBUX, CMG
- Subcluster E — Consumer Staples / Beverages: KO, PEP
- Subcluster F — Home Improvement / Specialty Retail: HD, LOW, TJX

**Unresolved decisions from source**:
- How to handle multi-segment companies like AMZN (retail vs. cloud vs. logistics)
- Whether ADS (Frankfurt-listed) requires cross-region normalization
- How to define subcluster boundaries within PGF-05 given the breadth of the family

**Boundary notes from source**: (none explicitly listed)

---

## PGF-06 — Defense / Security / C-UAS / Public Safety AI

| Field | Value |
|-------|-------|
| family_id | PGF-06 |
| family_name | Defense / Security / C-UAS / Public Safety AI |
| source_section_reference | Section 5, Family PGF-06 |
| core_universe_count | 12 |
| adjacent_universe_count | 4 |
| core_candidate_tickers_from_source | PLTR, AXON, MSI, RTX, LMT, NOC, GD, Rheinmetall, Hensoldt, Thales, Leonardo, Saab |
| adjacent_candidate_tickers_from_source | KTOS, AVAV, LHX, BAE Systems |
| benchmark_context_candidates_from_source | ITA (iShares U.S. Aerospace and Defense ETF), XAR (SPDR S&P Aerospace and Defense ETF) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-06", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Defense Software / AI / Analytics: PLTR, AXON
- Subcluster B — US Defense Primes: RTX, LMT, NOC, GD, LHX
- Subcluster C — European Defense: Rheinmetall, Hensoldt, Thales, Leonardo, Saab, BAE Systems
- Subcluster D — Drone / C-UAS / Unmanned Systems: KTOS, AVAV

**Unresolved decisions from source**:
- Whether PLTR belongs in PGF-06 or warrants its own software/AI platform family
- Whether public safety AI (AXON) is a primary peer for defense primes or adjacent only
- How to handle European defense rearmament context in peer group versioning (rapidly changing market caps)

**Boundary notes from source**:
- Rheinmetall, Hensoldt, Thales, Leonardo, Saab, BAE Systems are European-listed; cross-region normalization required
- Currency normalization required for EUR/GBP/SEK-denominated peers

---

## PGF-07 — Industrials / Power / Grid / Cooling

| Field | Value |
|-------|-------|
| family_id | PGF-07 |
| family_name | Industrials / Power / Grid / Cooling |
| source_section_reference | Section 5, Family PGF-07 |
| core_universe_count | 9 |
| adjacent_universe_count | 4 |
| core_candidate_tickers_from_source | ETN, Schneider Electric, Siemens, ABB, VRT, Trane, Carrier, CAT, URI |
| adjacent_candidate_tickers_from_source | GE Vernova, Prysmian, Hubbell, Quanta Services |
| benchmark_context_candidates_from_source | XLI (Industrials Select Sector SPDR), GRID (First Trust NASDAQ Clean Edge Smart Grid and Energy Innovation ETF) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-07", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — Electrification / Grid Infrastructure: ETN, Schneider Electric, Siemens, ABB, GE Vernova, Prysmian, Hubbell, Quanta Services
- Subcluster B — AI Data Center Power / Cooling: VRT, Trane, Carrier
- Subcluster C — Industrial Capital Equipment / Rental: CAT, URI

**Unresolved decisions from source**:
- Whether VRT belongs primarily in PGF-01, PGF-07, or spans both families (primary/secondary membership)
- Whether SMCI (from PGF-01 adjacent) overlaps with PGF-07
- Whether GE Vernova is core or adjacent given recent spinoff recency

**Boundary notes from source**:
- Schneider Electric (Paris-listed), Siemens (Frankfurt-listed), ABB (Zurich-listed), Prysmian (Milan-listed) are European-listed; cross-region normalization required
- Currency exposure: EUR/CHF-denominated peers

---

## PGF-08 — Banks / Financials

| Field | Value |
|-------|-------|
| family_id | PGF-08 |
| family_name | Banks / Financials |
| source_section_reference | Section 5, Family PGF-08 |
| core_universe_count | 10 |
| adjacent_universe_count | 0 |
| core_candidate_tickers_from_source | JPM, BAC, C, WFC, GS, MS, SAN, BNP, DB, UBS |
| adjacent_candidate_tickers_from_source | NONE_IN_SOURCE |
| benchmark_context_candidates_from_source | XLF (Financial Select Sector SPDR), EUFN (iShares MSCI Europe Financials ETF), SX7P (STOXX Europe 600 Banks Index), KRE (SPDR S&P Regional Banking ETF) |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-08", accessed_date: "2026-06-10"}` |

**Subcluster definitions from source**:
- Subcluster A — US Money-Center Banks: JPM, BAC, C, WFC
- Subcluster B — US Investment Banks / Universal Banks: GS, MS
- Subcluster C — European Banks: SAN, BNP, DB, UBS
- Subcluster D — Regional Banks: separate subcluster required (no specific tickers confirmed in source)

**Unresolved decisions from source**:
- Whether European banks belong in a dedicated PGF-08E subcluster or require their own family
- How to handle UBS given recent structural change (Credit Suisse absorption)
- Whether regional banks (KRE universe) require a PGF-08R subcluster or separate family

**Boundary notes from source**:
- SAN, BNP, DB are European-listed (EUR-denominated); UBS is CHF-denominated; cross-region handling required
- XLF, EUFN, SX7P, KRE are benchmark context only — not company peers

---

## PGF-09 — ETF / Fund Peer Rule (Rule-Based)

| Field | Value |
|-------|-------|
| family_id | PGF-09 |
| family_name | ETF / Fund Peer Rule |
| source_section_reference | Section 5, Family PGF-09 |
| core_universe_count | N/A (rule-based, not ticker-based) |
| adjacent_universe_count | N/A (rule-based) |
| core_candidate_tickers_from_source | N/A — PGF-09 is a rule-based methodology family, not a company ticker universe |
| adjacent_candidate_tickers_from_source | N/A |
| benchmark_context_candidates_from_source | N/A — ETFs are compared to other ETFs, not to benchmark instruments of their own |
| source_trace | `{file_path: ".domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md", section: "Section 5, Family PGF-09", accessed_date: "2026-06-10"}` |

**Rule statement from source**: ETFs and funds do NOT receive company peer groups. Comparing an ETF with a constituent company is a category error and is architecturally prohibited.

**ETF/fund comparison dimensions from source** (10 dimensions):
1. Benchmark / index tracked
2. TER / fees
3. AUM
4. Tracking error
5. Liquidity / bid-ask spread
6. Holdings overlap
7. Domicile (UCITS vs. 1940 Act vs. other)
8. Distribution policy (accumulating vs. distributing)
9. Replication method (physical full, physical sampled, synthetic)
10. Concentration / look-through exposures

**ETF/fund methodology rules from source**:
- ETFs/funds never receive company peer groups
- ETFs as benchmark_context in company families; as etf_peer only within PGF-09
- No ETF-to-company peer fallback permitted
- No company-to-ETF peer fallback permitted

**Benchmark/context role separation from source**:
- ETFs appearing in PGF-01 through PGF-08 carry peer_role = benchmark_context only
- ETFs within PGF-09 carry peer_role = etf_peer
- Indices are always benchmark_context — never peers

**Subcluster definitions from source**:
- Subcluster ETF-A — Thematic ETFs: Technology, AI, cybersecurity, defense, clean energy
- Subcluster ETF-B — Broad Market / Index ETFs: S&P 500, Nasdaq-100, MSCI World, total market
- Subcluster ETF-C — Sector ETFs: XLF, XLI, XLY, XLK, XLE etc.
- Subcluster ETF-D — Active / Semi-Active Funds: expense ratio and active share context

**Unresolved decisions from source**:
- How to handle UCITS vs. US-domiciled ETF peers (same index, different domicile)
- Whether leveraged/inverse ETFs require entirely separate peer universe
- How to normalize AUM and TER across USD and EUR-denominated fund share classes

---

## Intake Summary

| Family ID | Family Name | Core | Adjacent | Benchmark Instruments | Subclusters |
|-----------|-------------|------|----------|----------------------|-------------|
| PGF-01 | AI Semiconductors / AI Infrastructure | 11 | 4 | 3 (SOX, SMH, QQQ) | 3 (A, B, C) |
| PGF-02 | Cybersecurity / SaaS Security | 9 | 3 | 3 (CIBR, HACK, IGV) | 4 (A, B, C, D) |
| PGF-03 | Payments / Networks / Merchant Acquiring | 9 | 4 | 2 (IPAY, XLF) | 4 (A, B, C, D) |
| PGF-04 | Mobility / Delivery / Local Commerce | 9 | 4 | 1 (JETS) | 4 (A, B, C, D) |
| PGF-05 | Consumer / Retail / Event Consumption | 11 | 5 | 3 (XRT, XLP, XLY) | 6 (A, B, C, D, E, F) |
| PGF-06 | Defense / Security / C-UAS / Public Safety AI | 12 | 4 | 2 (ITA, XAR) | 4 (A, B, C, D) |
| PGF-07 | Industrials / Power / Grid / Cooling | 9 | 4 | 2 (XLI, GRID) | 3 (A, B, C) |
| PGF-08 | Banks / Financials | 10 | 0 | 4 (XLF, EUFN, SX7P, KRE) | 4 (A, B, C, D) |
| PGF-09 | ETF / Fund Peer Rule | N/A | N/A | N/A | 4 (ETF-A, ETF-B, ETF-C, ETF-D) |

**Totals**: 80 core candidates + 28 adjacent candidates = 108 company-level candidates across 8 company families, plus 1 rule-based ETF/Fund family.

---

## No-Invention Rule

This artifact does NOT:
- Invent new family universes beyond PGF-01 through PGF-09
- Add tickers not present in the scope preflight
- Create subclusters not defined in the scope preflight
- Add benchmark instruments not listed in the scope preflight
- Resolve unresolved decisions (those require human/CTO approval)
- Create candidate records
- Assign peer roles
- Create peer_group_id values
- Create registry content

All content traces exclusively to `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` Section 5.

---

## Final Status

```
FAMILY_UNIVERSE_INTAKE_PREFLIGHT_COMPLETE
```

---

*End of family universe intake artifact.*
