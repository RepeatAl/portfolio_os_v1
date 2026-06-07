# Single Asset Intelligence Framework — KPI Mapping Validation Artifact

**Artifact**: kpi_mapping_validation.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 13.1 Create KPI mapping artifact
**Requirements**: SAI-REQ-2 (Fact Consumption Contracts, Acceptance Criterion 4)
**Verification Gate**: VG-SAI-11 (KPI Mapping Validation Gate)
**Status**: Draft

---

## 1. Source Declaration

**Status (as of 2026-06-07)**: CTO/operator completeness declaration received. The 20 analysis blocks (Geschäftsmodell through Portfolio Fit) are the full and complete canonical KPI-Micro denominator for VG-SAI-11. This declaration supersedes the original source-lookup status.

**Original source lookup**: A standalone KPI-Micro Asset Analysis Sheet file was not found in the repository at initial execution. The preflight contained a 20-item subset described as "representative." The CTO/operator declaration on 2026-06-07 established the 20-block set as the canonical and complete denominator.

---

## 2. Canonical Source Completeness Statement

**CTO/operator declaration received**: 2026-06-07

> "The 20 analysis blocks in the KPI-Micro Asset Analysis Sheet — from Geschäftsmodell through Portfolio Fit — are hereby declared to be the full and complete canonical KPI-Micro denominator for VG-SAI-11 purposes."

The 20 KPI-Micro blocks are complete for VG-SAI-11. No further KPI denominator input is required. Macro KPI List (market/regime monitor categories: SPY, QQQ, VIX, GLD, HYG, BTC, etc.) is explicitly out of scope for VG-SAI-11 and future-use only.

---

## 3. Canonical KPI-Micro 20-Block Source (CTO-Declared Complete)

**Source**: KPI-Micro Asset Analysis Sheet — CTO/operator declared complete canonical denominator (2026-06-07)
**Item count**: 20 blocks
**Status**: Canonical — completeness declared by CTO/operator

The following 20 blocks constitute the full KPI-Micro denominator per the CTO declaration:

| # | Block Name (German) | English Equivalent |
|---|--------------------|--------------------|
| 1 | Geschäftsmodell | Business Model |
| 2 | Umsatzqualität | Revenue Quality |
| 3 | Nachfrage / Pipeline | Demand / Pipeline |
| 4 | Margenqualität | Margin Quality |
| 5 | Cashflow | Cashflow Quality |
| 6 | Bilanzqualität | Balance Sheet Quality |
| 7 | Verbindlichkeiten / Off-Balance-Sheet | Hidden Liabilities / Credit |
| 8 | Working Capital | Working Capital |
| 9 | Kundenkonzentration | Customer Concentration |
| 10 | Supply Chain Stability | Supply Chain Stability |
| 11 | Pricing Power | Pricing Power |
| 12 | Capex / Produktionskapazität | Capex / Production Capacity |
| 13 | Kapitalallokation | Capital Allocation |
| 14 | M&A / LBO-Risiko | M&A / LBO Risk |
| 15 | Stock-Based Compensation / Verwässerung | SBC / Dilution |
| 16 | Regulatorik / Litigation | Regulatory / Litigation Risk |
| 17 | Markt-/Konsensprognosen | Market / Consensus Forecasts |
| 18 | Bewertung | Valuation Context |
| 19 | Reverse DCF / implizite Erwartungen | Value Trap Guard / Implied Expectations |
| 20 | Portfolio Fit | Portfolio Fit |

**Macro KPI List exclusion**: The Macro KPI List (market/regime monitor categories: SPY, QQQ, VIX, GLD, etc.) is NOT part of this denominator. It is classified as a future macro signal/dashboard contract source.

---

## 4. Mapping Table (Based on CTO-Declared Canonical 20-Block Source)

All 20 canonical KPI-Micro blocks are mapped to valid SAI blocks. No KPI items invented.

| # | KPI-Micro Block | Mapped SAI Block ID(s) | Mapping Status |
|---|----------------|----------------------|----------------|
| 1 | Geschäftsmodell | SAI-BLK-02 (Business Model Quality) | mapped |
| 2 | Umsatzqualität | SAI-BLK-03 (Revenue Quality) | mapped |
| 3 | Nachfrage / Pipeline | SAI-BLK-04 (Demand/Pipeline) | mapped |
| 4 | Margenqualität | SAI-BLK-05 (Margin Quality) | mapped |
| 5 | Cashflow | SAI-BLK-06 (Cashflow Quality) | mapped |
| 6 | Bilanzqualität | SAI-BLK-07 (Balance Sheet Quality) | mapped |
| 7 | Verbindlichkeiten / Off-Balance-Sheet | SAI-BLK-08 (Credit/Solvency Risk), SAI-BLK-09 (Hidden Liabilities) | mapped |
| 8 | Working Capital | SAI-BLK-11 (Working Capital) | mapped |
| 9 | Kundenkonzentration | SAI-BLK-12 (Customer Concentration) | mapped |
| 10 | Supply Chain Stability | SAI-BLK-13 (Supply Chain Stability) | mapped |
| 11 | Pricing Power | SAI-BLK-14 (Pricing Power) | mapped |
| 12 | Capex / Produktionskapazität | SAI-BLK-06, SAI-BLK-07 | mapped |
| 13 | Kapitalallokation | SAI-BLK-06, SAI-BLK-07 | mapped |
| 14 | M&A / LBO-Risiko | SAI-BLK-08 (Credit/Solvency Risk) | mapped |
| 15 | Stock-Based Compensation / Verwässerung | SAI-BLK-15 (Earnings Quality) | mapped |
| 16 | Regulatorik / Litigation | SAI-BLK-09 (Hidden Liabilities) | mapped |
| 17 | Markt-/Konsensprognosen | SAI-BLK-16 (Guidance/Estimate Revisions) | mapped |
| 18 | Bewertung | SAI-BLK-17 (Valuation Context) | mapped |
| 19 | Reverse DCF / implizite Erwartungen | SAI-BLK-18 (Value Trap Guard) | mapped |
| 20 | Portfolio Fit | SAI-BLK-24 (Portfolio Fit) | mapped |

---

## 5. Mapping Coverage Assessment

### 5.1 Coverage Percentage

| Metric | Value |
|--------|-------|
| **Total canonical KPI-Micro blocks** | 20 (CTO/operator-declared complete) |
| **Items mapped to canonical SAI blocks** | 20 |
| **Items unmapped** | 0 |
| **Coverage** | **100%** (20/20) — ≥80% criterion satisfied |

### 5.2 SAI Block Coverage by Canonical KPI-Micro Items

VG-SAI-11 validates the mapping of the canonical KPI-Micro denominator to SAI blocks — it does not require every SAI block to have a KPI-Micro item. The denominator is the KPI-Micro sheet (20 blocks), not the full 24-block SAI taxonomy.

The following SAI blocks receive direct KPI-Micro coverage:

| Block ID | Block Name | KPI-Micro Items Mapped |
|----------|-----------|----------------------|
| SAI-BLK-02 | Business Model Quality | Geschäftsmodell |
| SAI-BLK-03 | Revenue Quality | Umsatzqualität |
| SAI-BLK-04 | Demand/Pipeline | Nachfrage / Pipeline |
| SAI-BLK-05 | Margin Quality | Margenqualität |
| SAI-BLK-06 | Cashflow Quality | Cashflow, Capex / Produktionskapazität, Kapitalallokation |
| SAI-BLK-07 | Balance Sheet Quality | Bilanzqualität, Capex / Produktionskapazität, Kapitalallokation |
| SAI-BLK-08 | Credit/Solvency Risk | Verbindlichkeiten / Off-Balance-Sheet, M&A / LBO-Risiko |
| SAI-BLK-09 | Hidden Liabilities | Verbindlichkeiten / Off-Balance-Sheet, Regulatorik / Litigation |
| SAI-BLK-11 | Working Capital | Working Capital |
| SAI-BLK-12 | Customer Concentration | Kundenkonzentration |
| SAI-BLK-13 | Supply Chain Stability | Supply Chain Stability |
| SAI-BLK-14 | Pricing Power | Pricing Power |
| SAI-BLK-15 | Earnings Quality | Stock-Based Compensation / Verwässerung |
| SAI-BLK-16 | Guidance/Estimate Revisions | Markt-/Konsensprognosen |
| SAI-BLK-17 | Valuation Context | Bewertung |
| SAI-BLK-18 | Value Trap Guard | Reverse DCF / implizite Erwartungen |
| SAI-BLK-24 | Portfolio Fit | Portfolio Fit |

### 5.3 SAI Blocks Without Direct KPI-Micro Items

The following SAI blocks have no direct KPI-Micro item. This is not a coverage gap — the denominator is the KPI-Micro sheet, not the SAI taxonomy. These blocks are identity, market-position, outlook, pension-specific, or portfolio-framework blocks that are outside the scope of a fundamental company KPI sheet by design.

| Block ID | Block Name | Reason for Absence from KPI-Micro Sheet |
|----------|-----------|----------------------------------------|
| SAI-BLK-01 | Asset Identity | Classification block, not a diagnostic KPI |
| SAI-BLK-10 | Pension Obligations | Covered implicitly via Bilanzqualität |
| SAI-BLK-19 | Relative Strength | Market-position metric, not fundamental KPI |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Market-derived, not fundamental KPI |
| SAI-BLK-21 | Peer Comparison | Requires peer definitions, not standalone KPI |
| SAI-BLK-22 | Company Outlook | Qualitative forward-looking, out of scope for KPI sheet |
| SAI-BLK-23 | Asset-Class Outlook | Macro/sector-level, not asset-level KPI |

---

## 6. Unmapped Item List

**No items are unmapped.** All 20 canonical KPI-Micro items map to valid SAI blocks.

---

## 7. Partial Mapping List

**No items are partially mapped.** Each of the 20 canonical KPI-Micro items maps to at least one primary SAI block.

---

## 8. Macro KPI List Exclusion

The Macro KPI List (market/regime monitor categories including SPY, QQQ, VIX, GLD, HYG, BTC, combination reading rules, etc.) is **NOT** part of the VG-SAI-11 denominator. It is classified as a future macro signal/dashboard contract source. No Macro KPI items are included in this artifact or in VG-SAI-11.

(See: .domainization/reports/single_asset_intelligence_framework_kpi_source_intake_review_2026-06-07.md)

---

## 9. VG-SAI-11 Gate Status

### 9.1 Current Gate Status (After Re-execution 2026-06-07)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| ≥80% of canonical KPI-Micro items mapped | **SATISFIED** | 20/20 = 100% |
| Complete KPI source declared by operator | **CONFIRMED** | CTO/operator completeness declaration received 2026-06-07 |
| All mapped items reference valid SAI blocks | **VERIFIED** | All 20 map to canonical block IDs |
| Macro KPI List excluded from denominator | **CONFIRMED** | Excluded per CTO source distinction |

### 9.2 Gate Status: PASS

VG-SAI-11 result changed from BLOCKED to **PASS** on 2026-06-07 following CTO/operator completeness declaration.

### 9.3 No-Auto-Completion Statement

This artifact provides the mapping evidence for VG-SAI-11. The gate execution artifact is `gates/gate_vg_sai_11.md` which records the formal PASS result with full evidence.

---

## 10. Boundary Confirmations

This artifact is a definition-layer document. It has been verified to contain:

- ✓ Zero implementation code
- ✓ Zero KPI invention — all 20 items are from the CTO/operator-declared canonical KPI-Micro denominator
- ✓ No Macro KPI items included
- ✓ Zero KPI source file mutation
- ✓ Zero scoring, ranking, recommendation, allocation, or trading logic
- ✓ Zero formula creation
- ✓ Zero fact/signal/evidence primitive creation
- ✓ Zero registry or SSOT mutations
- ✓ Zero asset-to-narrative mappings
- ✓ Zero narrative mappings
- ✓ All cross-references in canonical (See: [Deliverable], Section: [Title]) format

---

## 11. Cross-References

(See: requirements.md, Section: SAI-REQ-2 — Fact Consumption Contracts)
(See: fact_consumption_matrix.md, Section: Block Coverage Matrix)
(See: block_taxonomy.md, Section: All 24 Blocks)
(See: gates/gate_vg_sai_11.md, Section: VG-SAI-11 Gate Execution)
(See: .domainization/reports/single_asset_intelligence_framework_kpi_source_intake_review_2026-06-07.md)

---

*End of artifact.*
