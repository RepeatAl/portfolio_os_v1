# Market Evidence Framework — Credit and Solvency Hardening Report

**Date**: 2026-06-04
**Branch**: `spec/market-evidence-framework-foundation`
**Type**: README hardening (credit/solvency/balance-sheet evidence)
**Status**: COMPLETE

---

## Files Modified

| File | Change Type |
|------|-------------|
| `docs/README_market_evidence_framework.md` | Expanded with credit/solvency sections |

---

## Credit/Solvency Sections Added

| # | Section | Content |
|---|---------|---------|
| 1 | Section 30: Credit, Solvency, and Balance Sheet Evidence | First-class evidence domain; credit ≠ valuation; value trap warning; evidence categories; framework limitations |
| 2 | Section 31: Valuation Trap Boundary | Core rule; interpretation boundary; authorized vs unauthorized actions; anti-pattern |

---

## Fact Categories Added (Illustrative Only)

40 credit/solvency/balance-sheet fact categories added to Section 19:

- Debt structure: gross_debt, net_debt, short_term_debt_due, long_term_debt_due, debt_maturity_schedule
- Liquidity: cash_and_equivalents, available_liquidity, undrawn_credit_facilities
- Cashflow: operating_cash_flow, free_cash_flow
- Coverage: interest_expense, interest_coverage, debt_to_ebitda, net_debt_to_ebitda, fcf_to_debt
- Ratios: current_ratio, quick_ratio
- Refinancing: refinancing_wall, covenant_headroom
- Credit market: credit_rating, credit_rating_outlook, cds_spread, bond_yield, bond_price
- Off-balance: lease_liabilities, purchase_obligations, off_balance_sheet_commitments
- Pension: pension_obligations, pension_plan_assets, pension_funding_gap, post_retirement_benefit_obligations
- Asset quality: goodwill, intangible_assets, impairment_charges, goodwill_to_equity
- LBO/Sponsor: lbo_history, lbo_debt_burden, sponsor_ownership_overhang
- Commitments: dividend_commitments, buyback_commitments, working_capital_stress

---

## Signal Categories Added (Illustrative Only)

15 credit/solvency signal categories added to Section 20:

- liquidity_stress_signal
- refinancing_risk_signal
- cashflow_debt_coverage_signal
- interest_coverage_deterioration_signal
- debt_maturity_wall_signal
- covenant_pressure_signal
- pension_underfunding_signal
- off_balance_sheet_leverage_signal
- lease_adjusted_leverage_signal
- lbo_balance_sheet_stress_signal
- credit_spread_widening_signal
- bond_market_distress_signal
- rating_downgrade_risk_signal
- goodwill_impairment_risk_signal
- valuation_trap_risk_signal

---

## Evidence Container Families Added

6 new container namespaces added to Section 22:

- `evidence.credit_risk.*`
- `evidence.solvency.*`
- `evidence.balance_sheet_quality.*`
- `evidence.liquidity.*`
- `evidence.pension_obligation.*`
- `evidence.off_balance_sheet.*`

---

## Valuation Trap Boundary Added

Section 31 defines:
- Low valuation is not automatically undervaluation
- Valuation interpretation MUST consume credit/solvency evidence
- Companies can appear cheap because market prices default/refinancing risk
- Explicit anti-pattern showing prohibited vs required interpretation flow

---

## Anti-Drift Rules Added

6 new prohibitions added (rules 9-14 in Section 28):

- No treating low multiples as undervaluation without solvency evidence
- No ignoring pension/lease liabilities in balance sheet assessment
- No treating credit ratings as final truth
- No treating LBO/sponsor history as automatically bad without evidence
- No converting credit-risk evidence to buy/sell recommendations
- No turning credit-risk labels into hidden numeric scores

---

## Consumer Contracts Expanded

Added 2 new consumers to Section 23:
- Company Quality Assessment (consumes solvency and balance sheet evidence)
- Valuation Interpretation (must consume credit evidence before labeling undervaluation)

---

## Verification Expectations Expanded

6 new verification checks added (items 7-12 in Section 33):
- Credit/solvency boundary preservation
- No valuation shortcut from multiples to undervaluation
- No hidden credit scoring
- No hidden default probability model
- Pension/off-balance obligations as evidence categories
- LBO-related leverage as evidence category only

---

## Example Flow Added

Example D: "Apparent Undervaluation vs Credit Risk" — demonstrates full evidence flow from low-multiple fact through credit signals to value-trap interpretation. Marked as illustrative only.

---

## Confirmations

| Check | Status |
|-------|--------|
| No facts created | ✅ |
| No signals created | ✅ |
| No evidence objects created | ✅ |
| No evidence registry files created | ✅ |
| No narrative registry mutation | ✅ |
| No narrative entries added | ✅ |
| No asset-to-narrative mappings created | ✅ |
| No implementation work performed | ✅ |
| No engines, code, dashboards, scoring, ranking, probabilities | ✅ |
| No Market Organism Layer 0 SSOT modification | ✅ |
| No Narrative Framework v2 modification | ✅ |
| No central glossary modification | ✅ |
| All examples marked illustrative only | ✅ |
| All cross-references use canonical format | ✅ |

---

## Recommendation

The Market Evidence Framework README is **ready for human review** after this hardening. It now comprehensively covers:
- Core evidence hierarchy (facts, signals, containers)
- All relationship boundaries (Organism, Narrative, Registry)
- Credit, solvency, and balance sheet evidence as a first-class domain
- Valuation trap boundary preventing premature undervaluation conclusions
- Expanded anti-drift rules preventing hidden scoring
- Consumer contracts including quality assessment and valuation interpretation

The document is suitable as input for:
- Narrative Population Preflight (evidence justification model)
- Future Company Credit Evidence Framework
- Future Portfolio Health Framework

---

*Report generated: 2026-06-04*
*Authority: ARCH*
