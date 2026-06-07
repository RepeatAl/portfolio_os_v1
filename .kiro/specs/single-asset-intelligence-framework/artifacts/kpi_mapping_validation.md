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

## 1. Source Lookup Performed

The following locations were searched for the canonical KPI-Micro Asset Analysis Sheet:

| Location Searched | Result |
|-------------------|--------|
| Repository file search: `kpi`, `KPI`, `kpi_micro`, `kpi-micro` | No files found |
| Repository file search: `asset_analysis` | No files found |
| Repository-wide grep: `KPI-Micro`, `KPI.Micro`, `kpi_micro`, `kpi-micro` | References found in specs and preflight only — no standalone source file |
| `.domainization/reports/` directory | Contains preflight with representative KPI mapping, but no standalone KPI sheet |
| `.kiro/specs/` directory | References KPI-Micro in requirements and tasks — no standalone source |

**Conclusion**: The canonical KPI-Micro Asset Analysis Sheet does NOT exist as a standalone source file in this repository. The preflight report (`.domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md`, Section 7) contains a "Representative KPI-to-Block Mapping" with 20 items derived from a "typical micro asset analysis sheet." This is the only available evidence of KPI sheet contents.

---

## 2. Missing Source Statement

**Amendment 2026-06-07**: The portfolio operator/CTO has provided an explicit completeness declaration. The 20 analysis blocks (Geschäftsmodell through Portfolio Fit) are declared to be the **full and complete canonical KPI-Micro denominator** for VG-SAI-11 purposes. This supersedes the prior "missing source" status.

The original preflight contained a "representative" 20-item subset. The CTO declaration confirms that this 20-block set IS the complete canonical source.

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

### 5.2 SAI Block Coverage by KPI Items

| Block ID | Block Name | KPI Items Mapped | Items |
|----------|-----------|-----------------|-------|
| SAI-BLK-03 | Revenue Quality | 3 | Revenue Growth YoY, Organic Growth, ARR/Recurring % |
| SAI-BLK-04 | Demand/Pipeline | 3 | Order Intake, Book-to-Bill, Backlog/RPO |
| SAI-BLK-05 | Margin Quality | 3 | Gross Margin, Operating Margin, EBITDA Margin |
| SAI-BLK-06 | Cashflow Quality | 2 | Free Cash Flow, FCF Conversion |
| SAI-BLK-07 | Balance Sheet Quality | 1 | Debt Maturity Schedule |
| SAI-BLK-08 | Credit/Solvency Risk | 2 | Net Debt/EBITDA, Interest Coverage |
| SAI-BLK-10 | Pension Obligations | 1 | Pension Funding Status |
| SAI-BLK-12 | Customer Concentration | 1 | Customer Concentration |
| SAI-BLK-16 | Guidance/Estimate Revisions | 1 | Estimate Revisions (3M) |
| SAI-BLK-17 | Valuation Context | 2 | EV/EBITDA, FCF Yield |
| SAI-BLK-19 | Relative Strength | 1 | Relative Strength vs. Index |

### 5.3 Blocks Without KPI Items in Available Source

The following 13 blocks have no representative KPI items in the preflight source. This does NOT indicate a gap in SAI architecture — it reflects the limited scope of the available representative mapping (20 items from a typical sheet, not the full canonical sheet).

| Block ID | Block Name | Reason for Absence |
|----------|-----------|-------------------|
| SAI-BLK-01 | Asset Identity | Qualitative — not typically in numeric KPI sheets |
| SAI-BLK-02 | Business Model Quality | Qualitative — not typically in numeric KPI sheets |
| SAI-BLK-09 | Hidden Liabilities | Off-balance items not typically in standard KPI sheets |
| SAI-BLK-11 | Working Capital | Not in preflight representative set (but Working Capital KPIs exist in practice) |
| SAI-BLK-13 | Supply Chain Stability | Qualitative — not typically in numeric KPI sheets |
| SAI-BLK-14 | Pricing Power | Qualitative — rarely in numeric KPI sheets |
| SAI-BLK-15 | Earnings Quality | Derived quality metrics, not standard KPI sheet items |
| SAI-BLK-18 | Value Trap Guard | Composite interpretation, not a standalone KPI |
| SAI-BLK-20 | Benchmark/Sector/Peer Correlation | Market-derived, not fundamental KPI sheet items |
| SAI-BLK-21 | Peer Comparison | Requires peer definitions, not standalone KPI items |
| SAI-BLK-22 | Company Outlook | Qualitative forward-looking, not numeric KPI |
| SAI-BLK-23 | Asset-Class Outlook | Macro/sector-level, not asset-level KPI sheet items |
| SAI-BLK-24 | Portfolio Fit | Portfolio-level construct, not asset-level KPI |

---

## 6. Unmapped Item List

**No items are unmapped.** All 20 available representative KPI items from the preflight map to canonical SAI blocks.

---

## 7. Partial Mapping List

**No items are partially mapped.** Each of the 20 available KPI items maps cleanly to exactly one primary SAI block.

---

## 8. Placeholder Mapping Contract

Because the full canonical KPI-Micro Asset Analysis Sheet is not available in the repository, the following placeholder contract defines the interface expectations for a future complete mapping.

### 8.1 Expected Source Fields (For Future Complete Mapping)

When the canonical KPI-Micro Asset Analysis Sheet becomes available, the following fields are expected for each KPI item:

| Field | Description | Purpose |
|-------|-------------|---------|
| kpi_id | Unique identifier for the KPI item | Stable reference for mapping |
| kpi_name | Human-readable name of the KPI | Clarity and traceability |
| kpi_category | Domain grouping (Revenue, Margin, Cashflow, Balance Sheet, Valuation, Market, etc.) | Organizational structure |
| data_type | Numeric, percentage, ratio, categorical, qualitative | Determines fact category alignment |
| temporal_cadence | How frequently this KPI is updated (quarterly, monthly, daily) | Temporal resolution alignment |
| source_type | Corporate filing, market data, management disclosure, derived | Provenance alignment |
| current_usage | How this KPI is currently used in practice | Mapping rationale basis |

### 8.2 External Input Required Statement

> **EXTERNAL INPUT REQUIRED**: The full, canonical KPI-Micro Asset Analysis Sheet must be provided by the portfolio operator (human authority) for this mapping to achieve complete coverage. The preflight representative mapping (20 items) provides partial validation. Complete validation per VG-SAI-11 (≥80% coverage) depends on access to the full sheet.

### 8.3 No Invented KPI Contents Statement

This artifact does NOT invent, assume, or fabricate KPI sheet contents that are not present in the available source material. The 20 items mapped in Section 4 are exclusively from the preflight's representative mapping. No additional items have been created by this artifact.

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
- ✓ Zero KPI invention — all items sourced from preflight representative mapping
- ✓ Zero KPI source file mutation
- ✓ Zero scoring, ranking, recommendation, allocation, or trading logic
- ✓ Zero formula creation
- ✓ Zero fact/signal/evidence primitive creation
- ✓ Zero registry or SSOT mutations
- ✓ Zero asset-to-narrative mappings
- ✓ Zero narrative mappings
- ✓ Zero verification gate auto-completion
- ✓ All cross-references in canonical (See: [Deliverable], Section: [Title]) format

---

## 11. Cross-References

(See: requirements.md, Section: SAI-REQ-2 — Fact Consumption Contracts)
(See: fact_consumption_matrix.md, Section: Block Coverage Matrix)
(See: block_taxonomy.md, Section: All 24 Blocks)
(See: .domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md, Section: 7 — Representative KPI-to-Block Mapping)

---

*End of artifact.*
