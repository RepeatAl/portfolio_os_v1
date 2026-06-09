# Peer Group Registry Methodology Framework — Cross-Region Comparability Specification

**Artifact**: cross_region_comparability_specification_2026-06-08.md
**Task**: Task 5 — Create Cross-Region Comparability Specification
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_5_CROSS_REGION_COMPARABILITY_READY_FOR_HUMAN_REVIEW

**Purpose**: This document specifies the complete methodology for handling cross-region peers. It defines accounting-standard normalization, currency handling, taxonomy reconciliation, listing/venue handling, and the comparability_adjustment_required logic preventing silent misleading cross-standard comparisons.

**Hard boundaries confirmed**: No peer_group_registry.yaml. No final peer assignments. No canonical peer_group_id. No SAI mutation. No code. No market data. No broker/exchange/ATS. No trading logic.

---

## 1. Why Cross-Region Peers Require Normalization

Multiple families include European peers (Rheinmetall, ASML, Siemens, SAN, etc.). Blocking them creates coverage gaps. Comparing raw IFRS vs. GAAP financials produces misleading outputs. Solution: peers allowed with explicit normalization flags.

Source: SRC-H-01 (IFRS Foundation), SRC-H-02 (KPMG), SRC-H-03 (PwC), SRC-C-01 (ICB)


---

## 2. Required Cross-Region Normalization Fields

| Field | Type | Requirement | Description |
|-------|------|-------------|-------------|
| `domicile` | string | REQUIRED | ISO 3166-1 alpha-2 country code |
| `reporting_currency` | string | REQUIRED | ISO 4217 currency of filed financial reports |
| `trading_currency` | string | REQUIRED_IF_LISTED | ISO 4217 currency at listing venue |
| `accounting_standard` | enum | REQUIRED | GAAP / IFRS / other |
| `fiscal_year_end` | string | REQUIRED | Three-letter month abbreviation |
| `taxonomy_reference` | enum | REQUIRED | GICS / ICB / other |
| `comparability_adjustment_required` | boolean | REQUIRED | true when cross-standard adjustment needed |
| `comparability_note` | string | REQUIRED_IF_APPLICABLE | Mandatory when comparability_adjustment_required = true |

---

## 3. Accounting-Standard Differences (GAAP vs. IFRS)

### 3.1 Material Differences

| Area | GAAP | IFRS | Peer Comparison Impact | Affected Metrics |
|------|------|------|----------------------|------------------|
| R&D Capitalization | All R&D expensed | Development-phase capitalized | IFRS shows higher margins/earnings | Op margin, EBITDA, EPS, P/E |
| Lease Accounting | ASC 842 | IFRS 16 | EBITDA and leverage differ | EBITDA, Net Debt/EBITDA, Interest Coverage |
| Inventory Methods | LIFO permitted | LIFO prohibited | LIFO companies report lower gross profit in inflation | Gross margin, inventory turnover |
| Financial Instruments | ASC 320/326 (CECL) | IFRS 9 (ECL stages) | P/B, ROE differ for banks | P/B, ROE, Total Equity |
| Revenue Recognition | ASC 606 | IFRS 15 | Substantially converged; industry-specific differences remain | Revenue, revenue growth |
| Segment Reporting | ASC 280 | IFRS 8 (CODM view) | Geographic granularity may differ | Segment revenue/margin |
| Impairment | Two-step; no reversal | Single-step; reversal allowed (not goodwill) | Historical P/L affected in reversal years | Operating income |

### 3.2 When comparability_adjustment_required = true

1. Peer IFRS, subject GAAP (or vice versa) AND affected metrics compared
2. Material R&D expenditure (>5% revenue) with capitalization effect
3. Material operating leases affecting EBITDA/leverage
4. LIFO vs. FIFO in inflationary context
5. Banks/financials: IFRS 9 vs. ASC 320/326 equity differences

### 3.3 comparability_note Must Document

- Which accounting difference applies
- Which metrics are affected
- Direction of distortion (peer appears better or worse?)
- Qualitative magnitude (material / moderate / minor)

Example: "Rheinmetall (IFRS) capitalizes development R&D; LMT (GAAP) expenses all. Margin comparison requires ~2-3% IFRS uplift adjustment."

---

## 4. Currency Handling

### 4.1 Distinct Fields

| Field | Represents | Example |
|-------|-----------|---------|
| `reporting_currency` | Currency of filed financials | ASML: EUR |
| `trading_currency` | Currency shares trade in at venue | ASML on XAMS: EUR; ADR on XNAS: USD |

### 4.2 Rules

- Financial metric comparison acknowledges reporting_currency — no silent conversion
- Multiple comparison (P/E, EV/EBITDA) is currency-neutral if same-currency numerator/denominator
- Absolute size comparison (EUR revenue vs. USD revenue) requires FX context
- ADR: reporting_currency = company's currency (EUR); trading_currency = USD at ADR venue

---

## 5. Taxonomy Handling (GICS vs. ICB)

### 5.1 Non-1:1 Mapping

US-listed: typically GICS. European-listed: typically ICB. These DO NOT map 1:1. A company may be classified differently depending on which taxonomy is applied.

### 5.2 taxonomy_reference Required

Every company record must carry `taxonomy_reference = GICS` or `taxonomy_reference = ICB`. Documents which taxonomy was used and enables cross-taxonomy reconciliation.

### 5.3 MoneyHorst Family Is Canonical

MoneyHorst family assignment (PGF-01 through PGF-09) is the canonical peer universe boundary. GICS and ICB are reference inputs, not arbiters.

---

## 6. Listing and Venue Handling

### 6.1 canonical_object_id Unifies Cross-Listings

One company = one canonical_object_id = multiple Layer 2 listing records (primary + ADR). Prevents duplicate peer assignment.

### 6.2 Required Fields

| Field | Requirement | Description |
|-------|-------------|-------------|
| `primary_listing` | REQUIRED_IF_LISTED | Boolean: primary venue |
| `listing_variant_type` | REQUIRED_IF_LISTED | primary / ADR / GDR / secondary |
| `adr_flag` | REQUIRED_IF_LISTED (company) | Boolean: ADR |
| `exchange_mic` | REQUIRED_IF_LISTED | ISO 10383 four-character code |

### 6.3 Comparison Uses Primary Listing Context

Financial metrics: use reporting_currency from primary listing. Price ratios: use primary listing price. ADR trading_currency does not override reporting context.

---

## 7. Comparability Adjustment Logic

### 7.1 Trigger Conditions

| Condition | Action |
|-----------|--------|
| Accounting standard differs (GAAP ≠ IFRS) | comparability_adjustment_required = true |
| Reporting currency differs (for absolute metrics) | comparability_adjustment_required = true |
| Fiscal year-end differs by >3 months | comparability_adjustment_required = true |
| Material R&D capitalization effect | comparability_adjustment_required = true |
| Material lease treatment difference | comparability_adjustment_required = true |
| LIFO vs. FIFO in inflation | comparability_adjustment_required = true |
| IFRS 9 vs. ASC 320 for banks | comparability_adjustment_required = true |
| Taxonomy reference differs | Note in comparability_note (soft) |

### 7.2 Raw Comparison Prohibition

Raw GAAP vs. IFRS metric comparison WITHOUT flag is PROHIBITED for:
- Operating margin when R&D capitalization differs
- EBITDA when lease accounting differs
- Gross margin when LIFO/FIFO differs
- Bank equity (P/B, ROE) when IFRS 9 vs. ASC 320 applies

### 7.3 Downgrade Rules

- comparability_adjustment_required = true + empty comparability_note → INVALID record
- Material standard differences may justify downgrading core_peer → adjacent_peer
- Unquantifiable adjustment → financial_comparability_gate_status = partial

---

## 8. SAI-BLK-21 Behavior

### 8.1 No Silent Cross-Region Comparison

SAI-BLK-21 must NEVER silently compare GAAP and IFRS metrics. Every cross-region observation must surface the comparability_note.

### 8.2 Allowed Partial Comparison

- Relative price performance (currency-neutral) — unaffected by accounting standard
- Beta, correlation — unaffected by accounting standard
- Operating metrics WITH comparability_note surfaced
- Valuation multiples WITH adjustment context

### 8.3 Prohibited

- GAAP margin vs. IFRS margin without R&D capitalization flag
- GAAP EBITDA vs. IFRS EBITDA without lease flag
- "Peer outperforms on margins" without cross-standard check
- Suppressing the comparability_note

---

## 9. Examples

### 9.1 Allowed: Price/Market Behavior (Cross-Standard Safe)

Rheinmetall (XETR/IFRS/EUR) vs. LMT (XNYS/GAAP/USD) — relative price performance: ALLOWED without adjustment (price returns as ratios are currency-neutral). Beta, correlation: ALLOWED.

### 9.2 Partial: Operating Metric (Adjustment Required)

Rheinmetall vs. LMT — operating margin: comparability_adjustment_required = true. Note: "IFRS R&D capitalization ~2-3% uplift." SAI surfaces note. Result: PARTIAL.

### 9.3 Partial: Valuation (Adjustment Required)

ASML (XAMS/IFRS/EUR) vs. AMAT (XNAS/GAAP/USD) — EV/EBITDA: comparability_adjustment_required = true. Note: "EBITDA definition difference ~1-2x effect." Result: PARTIAL.

### 9.4 Blocked: Raw GAAP/IFRS Without Flag

DB (XETR/IFRS) vs. JPM (XNYS/GAAP) — ROE without flag: BLOCKED. Must set comparability_adjustment_required = true and document IFRS 9 vs. ASC 320 first.

### 9.5 Allowed: Same-Standard Cross-Region

Rheinmetall (XETR/IFRS/EUR) vs. Thales (XPAR/IFRS/EUR): Both IFRS, both EUR. comparability_adjustment_required = false. ALLOWED.

### 9.6 Edge Case: Different Fiscal Year-End

Siemens (XETR/IFRS/EUR/FY SEP) vs. ABB (XSWX/IFRS/CHF/FY DEC): Both IFRS but currency differs (EUR vs. CHF) and FY-end differs by 3 months. comparability_adjustment_required = true. Note documents both.

---

## 10. European-Listed Peers in Confirmed Families (Illustrative)

| Company | Family | MIC | Standard | Currency | Domicile | adjustment vs. US GAAP |
|---------|--------|-----|----------|----------|----------|----------------------|
| Rheinmetall | PGF-06 | XETR | IFRS | EUR | DE | true (R&D, leases) |
| Hensoldt | PGF-06 | XETR | IFRS | EUR | DE | true (R&D) |
| Thales | PGF-06 | XPAR | IFRS | EUR | FR | true (R&D, defense contracts) |
| Leonardo | PGF-06 | XMIL | IFRS | EUR | IT | true (R&D) |
| Saab | PGF-06 | STO | IFRS | SEK | SE | true (R&D, currency) |
| BAE Systems | PGF-06 | XLON | IFRS | GBP | GB | true (R&D, currency) |
| Schneider Electric | PGF-07 | XPAR | IFRS | EUR | FR | true (leases, R&D) |
| Siemens | PGF-07 | XETR | IFRS | EUR | DE | true (R&D, FY SEP) |
| ABB | PGF-07 | XSWX | IFRS | CHF | CH | true (currency, FY DEC) |
| Prysmian | PGF-07 | XMIL | IFRS | EUR | IT | true (leases) |
| SAN | PGF-08 | XMAD | IFRS | EUR | ES | true (IFRS 9) |
| BNP | PGF-08 | XPAR | IFRS | EUR | FR | true (IFRS 9) |
| DB | PGF-08 | XETR | IFRS | EUR | DE | true (IFRS 9) |
| UBS | PGF-08 | XSWX | IFRS | CHF | CH | true (IFRS 9, currency) |
| ASML | PGF-01 | XAMS | IFRS | EUR | NL | true (R&D — semi equipment) |
| ADYEN | PGF-03 | XAMS | IFRS | EUR | NL | true (leases, R&D) |
| ADS (Adidas) | PGF-05 | XETR | IFRS | EUR | DE | true (LIFO prohibition) |

---

## 11. Source Authority Mapping

| Principle | Source | Domain | Tier |
|-----------|--------|--------|------|
| R&D capitalization difference | SRC-H-02 (KPMG) | accounting_authority | 1 |
| Lease accounting differences | SRC-H-02 (KPMG) | accounting_authority | 1 |
| LIFO prohibition under IFRS | SRC-H-03 (PwC) | accounting_authority | 1 |
| Financial instruments (IFRS 9 vs ASC 320) | SRC-H-02 (KPMG) | accounting_authority | 1 |
| Revenue recognition convergence | SRC-H-03 (PwC) | accounting_authority | 1 |
| IFRS 8 segment reporting | SRC-H-01 (IFRS Foundation) | accounting_authority | 1 |
| ICB/GICS non-1:1 mapping | SRC-C-01 (FTSE Russell) | classification_authority | 1 |
| ISO 10383 MIC | SRC-I-01 (ISO/SWIFT) | identity_authority | 1 |
| Entity vs. listing | SRC-G-01 (OpenFIGI) | identity_authority | 1 |

---

## 12. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml | CONFIRMED |
| No final peer assignments | CONFIRMED |
| No canonical peer_group_id | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No code | CONFIRMED |
| No market data | CONFIRMED |
| No broker/exchange/ATS | CONFIRMED |
| Tasks 1–4 unchanged | CONFIRMED |
| Task 6 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_5_CROSS_REGION_COMPARABILITY_READY_FOR_HUMAN_REVIEW
```

---

*End of cross-region comparability specification.*
