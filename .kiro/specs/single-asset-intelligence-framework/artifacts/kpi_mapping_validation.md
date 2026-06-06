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

The KPI-Micro Asset Analysis Sheet is referenced in:
- SAI-REQ-2, Acceptance Criterion 4: "KPI-Micro Asset Analysis Sheet mapping is validated against the fact consumption contracts"
- SAI-GAP-7: "KPI-Micro Asset Analysis Sheet not canonicalized — existing analytical practice not formally mapped to SAI blocks"
- VG-SAI-11: "≥80% of existing KPI-Micro items mapped to canonical blocks"

However, no standalone, canonical KPI-Micro Asset Analysis Sheet file exists in the repository. The preflight's representative mapping (20 items) is the only available partial evidence of the sheet's contents. This partial evidence is sufficient for a best-effort validation but insufficient for a complete canonical mapping.

**External input required**: The full, canonical KPI-Micro Asset Analysis Sheet must be provided as an external input to complete this mapping at 100% coverage.

---

## 3. Available Partial Source: Preflight Representative KPI Mapping

**Source file**: `.domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md`
**Section**: Section 7 — Representative KPI-to-Block Mapping
**Item count**: 20 representative KPI items
**Nature**: Representative subset from "a typical micro asset analysis sheet" — not the full canonical sheet

---

## 4. Mapping Table (Based on Available Preflight Evidence)

The following table maps all 20 available representative KPI items from the preflight to canonical SAI blocks. This mapping does NOT invent additional KPI items.

| # | KPI Item (from Preflight) | Mapped SAI Block ID(s) | Mapping Rationale | Mapping Status | Notes |
|---|--------------------------|------------------------|-------------------|----------------|-------|
| 1 | Revenue Growth YoY | SAI-BLK-03 (Revenue Quality) | Revenue growth is a primary fact consumed by the Revenue Quality block | mapped | Fact: fact.revenue.growth_yoy |
| 2 | Organic Revenue Growth | SAI-BLK-03 (Revenue Quality) | Organic growth distinguishes core business trajectory from M&A-driven growth | mapped | Fact: fact.revenue.organic_growth |
| 3 | ARR / Recurring Revenue % | SAI-BLK-03 (Revenue Quality) | ARR and recurring percentage indicate revenue sustainability and quality | mapped | Facts: fact.revenue.arr, fact.revenue.recurring_pct |
| 4 | Order Intake | SAI-BLK-04 (Demand/Pipeline) | Order intake is a primary demand visibility indicator | mapped | Fact: fact.demand.order_intake |
| 5 | Book-to-Bill Ratio | SAI-BLK-04 (Demand/Pipeline) | Book-to-bill directly measures demand replenishment vs. revenue consumption | mapped | Fact: fact.demand.book_to_bill |
| 6 | Backlog / RPO | SAI-BLK-04 (Demand/Pipeline) | Backlog and RPO provide forward demand visibility | mapped | Facts: fact.demand.backlog, fact.revenue.rpo |
| 7 | Gross Margin | SAI-BLK-05 (Margin Quality) | Gross margin is the primary margin quality indicator | mapped | Fact: fact.margin.gross_margin |
| 8 | Operating Margin | SAI-BLK-05 (Margin Quality) | Operating margin indicates operational efficiency and cost structure | mapped | Fact: fact.margin.operating_margin |
| 9 | EBITDA Margin | SAI-BLK-05 (Margin Quality) | EBITDA margin provides earnings quality context before capital structure effects | mapped | Fact: fact.margin.ebitda_margin |
| 10 | Free Cash Flow | SAI-BLK-06 (Cashflow Quality) | FCF is the primary cash generation quality indicator | mapped | Fact: fact.cashflow.fcf |
| 11 | FCF Conversion | SAI-BLK-06 (Cashflow Quality) | FCF conversion measures how well earnings translate to cash | mapped | Fact: fact.cashflow.fcf_conversion |
| 12 | Net Debt / EBITDA | SAI-BLK-08 (Credit/Solvency Risk) | Leverage ratio is a primary credit/solvency diagnostic metric | mapped | Fact: fact.balance_sheet.net_debt_ebitda |
| 13 | Interest Coverage | SAI-BLK-08 (Credit/Solvency Risk) | Interest coverage measures debt service capacity | mapped | Fact: fact.balance_sheet.interest_coverage |
| 14 | Debt Maturity Schedule | SAI-BLK-07 (Balance Sheet Quality) | Maturity schedule identifies refinancing pressure points | mapped | Fact: fact.balance_sheet.maturity_schedule |
| 15 | Pension Funding Status | SAI-BLK-10 (Pension Obligations) | Pension funding gap is the primary pension obligation metric | mapped | Fact: fact.obligations.pension_funding_gap |
| 16 | Customer Concentration | SAI-BLK-12 (Customer Concentration) | Customer concentration directly measures single-customer dependency risk | mapped | Fact: fact.concentration.top_customer_pct |
| 17 | EV/EBITDA Multiple | SAI-BLK-17 (Valuation Context) | EV/EBITDA is a primary valuation multiple for diagnostic context | mapped | Fact: fact.valuation.ev_ebitda; Deferred: Valuation Framework |
| 18 | FCF Yield | SAI-BLK-17 (Valuation Context) | FCF yield provides cash-based valuation context | mapped | Fact: fact.valuation.fcf_yield; Deferred: Valuation Framework |
| 19 | Relative Strength vs. Index | SAI-BLK-19 (Relative Strength) | Relative strength is the primary market position diagnostic | mapped | Fact: fact.market.relative_strength_vs_benchmark |
| 20 | Estimate Revisions (3M) | SAI-BLK-16 (Guidance/Estimate Revisions) | Estimate revision trajectory is a primary earnings outlook indicator | mapped | Fact: fact.earnings.estimate_revision_3m; Deferred: Earnings Intelligence Framework |

---

## 5. Mapping Coverage Assessment

### 5.1 Coverage Percentage

| Metric | Value |
|--------|-------|
| **Total available KPI items** | 20 (from preflight representative mapping) |
| **Items mapped to canonical SAI blocks** | 20 |
| **Items partially mapped** | 0 |
| **Items unmapped** | 0 |
| **Mapping coverage** | **100% of available items** (20/20) |

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

### 9.1 Current Gate Readiness

| Criterion | Status | Evidence |
|-----------|--------|----------|
| ≥80% of KPI-Micro items mapped to canonical blocks | **CONDITIONAL** | 100% of 20 available items are mapped. However, 20 items represent only the preflight's representative subset — the full canonical sheet may contain additional items. |
| Complete KPI source available | **BLOCKED** | Full canonical KPI-Micro Asset Analysis Sheet not found in repository |
| All mapped items reference valid SAI blocks | READY | All 20 mappings reference canonical block IDs (SAI-BLK-01 through SAI-BLK-24) |

### 9.2 Gate Assessment

VG-SAI-11 cannot be definitively PASSED until the full canonical KPI-Micro Asset Analysis Sheet is available and ≥80% of its items are mapped. Based on available evidence:

- If the preflight's 20 representative items ARE the complete set: VG-SAI-11 is READY for gate execution (100% coverage)
- If the full sheet contains additional items beyond the preflight sample: VG-SAI-11 remains PENDING until the full sheet is provided and mapped

**Recommendation**: VG-SAI-11 gate execution (Task 15.11) should determine whether the 20 preflight items constitute sufficient coverage or whether external input is needed for the full sheet.

### 9.3 No-Auto-Completion Statement

This artifact provides **preparatory evidence only** toward VG-SAI-11 (KPI Mapping Validation Gate). It does NOT execute or pass VG-SAI-11. Gate execution requires a separate, explicit Task 15.11 verification artifact with PASS/FAIL/BLOCKED evidence.

(See: tasks.md, Section: 15.11 Execute VG-SAI-11 KPI Mapping Validation Gate)

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
