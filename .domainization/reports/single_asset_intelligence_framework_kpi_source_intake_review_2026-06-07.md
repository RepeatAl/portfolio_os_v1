# SAI Framework — KPI Source Intake Review

**Report date**: 2026-06-07
**Authority**: ARCH
**Purpose**: CTO-provided source review for VG-SAI-11 unblock readiness

---

## 1. Purpose

VG-SAI-11 (KPI Mapping Validation Gate) is BLOCKED because the full canonical KPI-Micro Asset Analysis Sheet was unavailable in the repository. The portfolio operator has now provided two source documents:

1. **KPI-Micro Asset Analysis Sheet** — candidate source for VG-SAI-11
2. **KPI List explained / Macro KPI List** — market/regime monitor source for future macro work

This report records source context, assesses mapping readiness, classifies both sources, and recommends next action. It does NOT re-execute VG-SAI-11. It does NOT change gate status. It does NOT modify existing SAI artifacts.

---

## 2. Source Context Received

| # | Source | Classification | For VG-SAI-11? |
|---|--------|---------------|----------------|
| A | KPI-Micro Asset Analysis Sheet | 20 micro-analysis blocks for single-asset diagnostics | YES — candidate denominator |
| B | KPI List explained / Macro KPI List | Market/regime/risk monitor dashboard categories | NO — separate future source |

---

## 3. KPI-Micro 20-Block Inventory (Source A)

| # | Block Name (German) | English Equivalent | SAI Block(s) |
|---|--------------------|--------------------|-------------|
| 1 | Geschäftsmodell | Business Model | SAI-BLK-02 |
| 2 | Umsatzqualität | Revenue Quality | SAI-BLK-03 |
| 3 | Nachfrage / Pipeline | Demand / Pipeline | SAI-BLK-04 |
| 4 | Margenqualität | Margin Quality | SAI-BLK-05 |
| 5 | Cashflow | Cashflow Quality | SAI-BLK-06 |
| 6 | Bilanzqualität | Balance Sheet Quality | SAI-BLK-07 |
| 7 | Verbindlichkeiten / Off-Balance-Sheet | Hidden Liabilities / Credit | SAI-BLK-08, SAI-BLK-09 |
| 8 | Working Capital | Working Capital | SAI-BLK-11 |
| 9 | Kundenkonzentration | Customer Concentration | SAI-BLK-12 |
| 10 | Supply Chain Stability | Supply Chain Stability | SAI-BLK-13 |
| 11 | Pricing Power | Pricing Power | SAI-BLK-14 |
| 12 | Capex / Produktionskapazität | Capex / Production Capacity | SAI-BLK-06, SAI-BLK-07 |
| 13 | Kapitalallokation | Capital Allocation | SAI-BLK-06, SAI-BLK-07 |
| 14 | M&A / LBO-Risiko | M&A / LBO Risk | SAI-BLK-08 |
| 15 | Stock-Based Compensation / Verwässerung | SBC / Dilution | SAI-BLK-15 |
| 16 | Regulatorik / Litigation | Regulatory / Litigation Risk | SAI-BLK-09 |
| 17 | Markt-/Konsensprognosen | Market / Consensus Forecasts | SAI-BLK-16 |
| 18 | Bewertung | Valuation Context | SAI-BLK-17 |
| 19 | Reverse DCF / implizite Erwartungen | Value Trap Guard / Implied Expectations | SAI-BLK-18 |
| 20 | Portfolio Fit | Portfolio Fit | SAI-BLK-24 |

Key source principles (consistent with SAI-REQ-7 and SAI-REQ-5):
- "A stock is not cheap because it fell."
- "A stock is cheap only if market expectation is below realistic value creation."
- "An operationally excellent company can still be overvalued if price already discounts too much future."
- "Portfolio Fit dominates isolated company quality when the asset worsens portfolio structure."

---

## 4. Mapping Readiness Assessment

All 20 blocks map to valid canonical SAI blocks. No invented blocks needed. No orphan mappings.

If these 20 blocks are the complete canonical denominator: 20/20 = 100% coverage → VG-SAI-11 ≥80% criterion satisfied.

Structural observations:
- SAI-BLK-01 (Asset Identity) is not a KPI block — classification only. Absence is expected.
- SAI-BLK-10 (Pension Obligations) is implicitly covered within Bilanzqualität. Absence as standalone is expected.
- SAI-BLK-19–21 (Market Position) are not in a fundamental KPI sheet. Absence is expected for a company-focused sheet.

The scope is appropriate for a fundamental single-asset analysis framework.

---

## 5. Source Distinction: Micro vs. Macro

### Source A — KPI-Micro (for VG-SAI-11)
20 fundamental single-asset analysis blocks. Covers operational, financial, valuation dimensions. This is the VG-SAI-11 candidate denominator.

### Source B — Macro KPI List (NOT for VG-SAI-11)
Market/regime monitor dashboard containing ETF/index tickers organized by theme:
- Breiter Markt / Risk Appetite: SPY, QQQ, IWM, DIA
- AI / Semiconductors: SMH, SOXX, SOX, XLK, VGT
- Consumer / Retail: XRT, XLY, XLP, PEJ, IBUY
- Financials / Payments: XLF, EUFN, SX7P, KRE, V/MA/AXP
- Industrials / Energy / Infrastructure: XLI, PAVE, XLU, XLE, URA, TAN
- Bonds / Rates / Liquidity: TLT, US2Y, US10Y, US30Y, MOVE, NFCI
- Volatility / Options / Sentiment: VIX, VXN, Put/Call Ratio, VVIX
- Commodities / Hedge / Inflation: USO, CL/WTI, Brent, GLD, SLV, GDX, DXY
- Europe / Germany: DAX, MDAX, SX5E, SXXP, SX7P, EUFN
- Credit / Financing Risk: HYG, JNK/SPHY, LQD, HY Spread
- Crypto / Risk-on: BTC, ETH, SOL, IBIT, COIN, MSTR

Also contains combination reading rules, e.g.: "SPY green + QQQ green + IWM green = real Risk-On", "VIX high + HYG red + TLT red = real stress."

---

## 6. Why Macro KPI List Must Not Be Used for VG-SAI-11

1. Contains market-wide ETF/index tickers, not company-level KPIs
2. Operates at portfolio/regime level, not asset level
3. Combination rules imply market timing signals (prohibited in SAI)
4. CTO explicitly classified it as "market/regime/risk monitor source for future macro KPI / signal / dashboard work"

Including Macro KPI items in VG-SAI-11 would constitute scope contamination. The Macro KPI List is a candidate source for a future separate framework (macro signal contracts, regime detection, dashboard) — not for SAI block architecture.

---

## 7. Remaining Confirmation Needed

The source appears complete, but VG-SAI-11 requires explicit operator declaration:

> **"The 20 analysis blocks in the KPI-Micro Asset Analysis Sheet (Geschäftsmodell through Portfolio Fit) are the full and complete canonical KPI-Micro denominator for VG-SAI-11 purposes."**

The current prompt states the source "contains exactly these 20 micro-analysis blocks" — this is strong evidence of completeness but requires explicit CTO confirmation to serve as governance-level declaration.

---

## 8. Recommended Next Action

1. **CTO confirms completeness** — one explicit statement that 20 Micro blocks = full canonical denominator
2. **After confirmation** — prepare a separate PR to re-execute VG-SAI-11, update `gates/gate_vg_sai_11.md`, `artifacts/kpi_mapping_validation.md`, `README_single_asset_intelligence.md`, and final execution report
3. **Macro KPI List** — scope separately as future macro signal/dashboard contract; not part of VG-SAI-11 path

---

## 9. Readiness Result

### KPI_MICRO_SOURCE_READY_FOR_CTO_COMPLETENESS_DECLARATION

20-block source is coherent, complete-looking, and fully mappable. All 20 blocks map to valid SAI-BLK IDs. Coverage of available items is 100%. Structurally appropriate for a fundamental asset analysis sheet. Awaiting explicit CTO completeness declaration to proceed to VG-SAI-11 re-execution.

---

## 10. Boundary Confirmations

- ✓ VG-SAI-11 NOT re-executed
- ✓ VG-SAI-11 status NOT changed
- ✓ No existing SAI artifacts modified
- ✓ No existing gate artifacts modified
- ✓ No README or final execution report modified
- ✓ No artifact registry mutated
- ✓ No YAML frontmatter added
- ✓ No Peer Group Registry created
- ✓ No implementation code created
- ✓ No scoring/ranking/recommendation/allocation/trading logic
- ✓ No facts/signals/evidence primitives created
- ✓ No asset-to-narrative mappings
- ✓ Macro KPI List NOT mixed into VG-SAI-11 denominator
- ✓ This is a readiness/intake report only

---

*End of report.*
