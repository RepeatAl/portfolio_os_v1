# Single Asset Intelligence Framework — Credit / Solvency Artifact

**Artifact**: credit_solvency.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 10.1 Create credit/solvency artifact
**Requirements**: SAI-REQ-8 (Financial Stability / Credit-Solvency Boundary)
**Verification Gate**: VG-SAI-1 (Requirements Completeness Gate)
**Status**: Draft

---

## 1. Purpose and Scope

This artifact defines the comprehensive evidence scope for financial stability assessment within the Single Asset Intelligence Framework. It covers all dimensions of credit risk, solvency trajectory, balance sheet quality, hidden obligations, and pension exposure — the full financial stability boundary mandated by SAI-REQ-8.

This artifact governs four SAI analysis blocks:

- **SAI-BLK-07**: Balance Sheet Quality (quarterly temporal class)
- **SAI-BLK-08**: Credit/Solvency Risk (quarterly temporal class)
- **SAI-BLK-09**: Hidden Liabilities (quarterly temporal class)
- **SAI-BLK-10**: Pension Obligations (quarterly temporal class)

**This is a definition-layer artifact.** It contains no implementation code, no credit scoring models, no default probability calculations, no bankruptcy prediction models, no rating assignment logic, no scoring systems, no ranking algorithms, no recommendation logic, no allocation decisions, no trading signals, no registry mutations, no fact/signal creation, and no asset/narrative mappings.

(See: design.md, Section: Components and Interfaces — Financial Stability Blocks)
(See: requirements.md, Section: SAI-REQ-8 — Financial Stability / Credit-Solvency Boundary)

---

## 2. Core Financial Stability Principles

The following principles govern all credit and solvency interpretation within SAI. They are canonical and immutable. No SAI deliverable, block output, or downstream interpretation may contradict these principles.

### Principle 1 — Credit Ratings Are Input Evidence, Not Truth

Credit ratings issued by external agencies (S&P, Moody's, Fitch, or others) are consumed by SAI as one evidence input among many. SAI does NOT:

- Assign credit ratings
- Endorse credit ratings as authoritative
- Treat ratings as sufficient evidence for solvency conclusions
- Substitute ratings for direct balance sheet analysis
- Assume rating accuracy or timeliness
- Recommend action based on rating changes

Ratings are informative but fallible. They are lagging indicators subject to agency incentives, methodology constraints, and update delays. SAI treats them as evidence inputs requiring corroboration from direct financial statement analysis, bond market signals, and CDS spread evidence.

### Principle 2 — Solvency Is a Survival Precondition

Solvency is not an attribute to be scored — it is a survival precondition. A company that cannot service its obligations faces existential risk regardless of operational quality, earnings trajectory, or valuation attractiveness. Credit/solvency assessment exists to diagnose whether the entity can survive long enough to realize its value creation potential.

### Principle 3 — Leverage Is Contextual

Leverage ratios (net debt/EBITDA, FCF/debt, interest coverage) are diagnostic evidence, not mechanical triggers. The same leverage ratio may be sustainable for a stable-cashflow utility and dangerous for a cyclical industrial. SAI interprets leverage within the context of cashflow stability, asset quality, sector norms, and maturity structure — never as an isolated metric.

### Principle 4 — Hidden Obligations Distort Headline Numbers

Balance sheet obligations as reported may materially understate the true claims on a company's assets and cashflow. Off-balance-sheet commitments, operating leases, purchase obligations, guarantees, contingent liabilities, and pension underfunding represent real economic claims that traditional leverage ratios may fail to capture. SAI explicitly accounts for these hidden obligations.

---

## 3. Covered Blocks

### SAI-BLK-07: Balance Sheet Quality

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-07 |
| **block_name** | Balance Sheet Quality |
| **category** | Financial Stability |
| **temporal_class** | quarterly |
| **purpose** | Diagnose overall balance sheet health, asset quality, and capital structure |
| **primary_fact_families** | Total assets, equity, debt structure, asset composition, goodwill/intangibles |
| **primary_signal_families** | Leverage signals, asset quality signals, capital structure signals |
| **deferred_dependencies** | None |
| **boundary_statement** | Produces balance sheet diagnostic only — never credit scores, ratings, or solvency predictions |

### SAI-BLK-08: Credit/Solvency Risk

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-08 |
| **block_name** | Credit/Solvency Risk |
| **category** | Financial Stability |
| **temporal_class** | quarterly |
| **purpose** | Diagnose credit risk, refinancing exposure, and solvency trajectory |
| **primary_fact_families** | Gross debt, net debt, maturity schedule, interest coverage, credit ratings, covenants |
| **primary_signal_families** | Credit deterioration signals, refinancing risk signals, covenant pressure signals |
| **deferred_dependencies** | None |
| **boundary_statement** | Produces credit risk diagnostic only — never default probabilities, credit scores, or rating assignments |

### SAI-BLK-09: Hidden Liabilities

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-09 |
| **block_name** | Hidden Liabilities |
| **category** | Financial Stability |
| **temporal_class** | quarterly |
| **purpose** | Diagnose off-balance-sheet obligations, contingent liabilities, and undisclosed risks |
| **primary_fact_families** | Operating leases, purchase obligations, guarantees, litigation, off-balance items |
| **primary_signal_families** | Hidden obligation signals, contingent liability signals |
| **deferred_dependencies** | None |
| **boundary_statement** | Produces hidden obligation diagnostic only — never liability quantification models or loss predictions |

### SAI-BLK-10: Pension Obligations

| Field | Value |
|-------|-------|
| **block_id** | SAI-BLK-10 |
| **block_name** | Pension Obligations |
| **category** | Financial Stability |
| **temporal_class** | quarterly |
| **purpose** | Diagnose pension funding status, obligation trajectory, and actuarial risk |
| **primary_fact_families** | Defined benefit obligations, plan assets, funding gap, actuarial assumptions |
| **primary_signal_families** | Pension underfunding signals, obligation growth signals |
| **deferred_dependencies** | None |
| **boundary_statement** | Produces pension funding diagnostic only — never actuarial calculations, liability projections, or funding adequacy scores |

(See: block_taxonomy.md, Section: Financial Stability Blocks)
(See: temporal_resolution_matrix.md, Section: Quarterly Temporal Class)

---

## 4. Credit/Solvency Risk Evidence Scope (SAI-BLK-08)

SAI-BLK-08 covers the primary credit risk, refinancing exposure, and solvency trajectory diagnostic. The following evidence categories are fully within scope per SAI-REQ-8.

### 4.1 Gross Debt

**Diagnostic question**: What is the total face value of financial obligations?

| Field | Value |
|-------|-------|
| **Fact category** | Gross debt |
| **Evidence source** | Balance sheet filings, debt schedules, 10-K/20-F notes |
| **Includes** | Long-term debt, short-term borrowings, revolving credit drawn, term loans, bonds outstanding, convertible debt, capital lease obligations |
| **Diagnostic purpose** | Establishes the absolute scale of financial obligations before netting cash and equivalents |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01 — related coverage via leverage context) |

### 4.2 Net Debt

**Diagnostic question**: What is the economic debt burden after available cash offset?

| Field | Value |
|-------|-------|
| **Fact category** | Net debt |
| **Evidence source** | Balance sheet filings, cash and equivalents, restricted cash disclosures |
| **Includes** | Gross debt minus unrestricted cash and cash equivalents; restricted cash excluded from netting |
| **Diagnostic purpose** | Provides a more realistic view of debt burden by accounting for immediately available cash that could service obligations |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01 — direct coverage) |

### 4.3 Maturity Schedule

**Diagnostic question**: When do obligations come due, and is there a refinancing wall?

| Field | Value |
|-------|-------|
| **Fact category** | Maturity schedule |
| **Evidence source** | Debt maturity tables in 10-K/20-F, bond prospectuses, credit agreements |
| **Includes** | Year-by-year maturity profile, weighted average maturity, bullet maturities, amortizing schedules, nearest material maturity date |
| **Diagnostic purpose** | Identifies concentration of maturities (maturity walls) that create refinancing pressure points where access to capital markets becomes critical |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-07-01 — direct coverage) |

### 4.4 Short-Term Debt

**Diagnostic question**: What is the near-term obligation pressure relative to available resources?

| Field | Value |
|-------|-------|
| **Fact category** | Short-term debt |
| **Evidence source** | Current portion of long-term debt, commercial paper outstanding, revolving credit utilization, short-term bank lines |
| **Includes** | Current maturities of long-term debt, commercial paper, short-term bank borrowings, demand facilities |
| **Diagnostic purpose** | Diagnoses immediate liquidity pressure — short-term debt must be serviced or rolled within the current operating cycle |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-07-01 — related coverage via near-term debt pressure) |

### 4.5 Available Liquidity

**Diagnostic question**: What resources can the company access immediately to meet obligations?

| Field | Value |
|-------|-------|
| **Fact category** | Available liquidity |
| **Evidence source** | Cash on balance sheet, undrawn revolving credit facilities, committed credit lines, liquidity disclosures |
| **Includes** | Unrestricted cash, undrawn committed credit facilities, available capacity under existing agreements |
| **Excludes** | Restricted cash, uncommitted facilities, conditional facilities with unmet covenants |
| **Diagnostic purpose** | Establishes the liquidity buffer available to absorb shocks, fund operations during downturns, and service near-term obligations without capital market access |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-07-01, RF-08-02 — related coverage via maturity wall and coverage context) |

### 4.6 Interest Coverage

**Diagnostic question**: Can the company comfortably service its debt interest from operating earnings?

| Field | Value |
|-------|-------|
| **Fact category** | Interest coverage |
| **Evidence source** | Income statement (interest expense), EBIT or EBITDA from filings |
| **Includes** | EBIT/interest expense ratio, EBITDA/interest expense ratio, fixed charge coverage ratio |
| **Diagnostic purpose** | Diagnoses the margin of safety between earnings capacity and mandatory interest obligations — declining coverage signals deteriorating ability to service debt |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-02 — direct coverage) |

### 4.7 Net Debt/EBITDA

**Diagnostic question**: How many years of current earnings would it take to repay the net debt burden?

| Field | Value |
|-------|-------|
| **Fact category** | Net debt/EBITDA ratio |
| **Evidence source** | Derived from net debt and trailing EBITDA from filings |
| **Includes** | Net debt / trailing twelve-month EBITDA, trend direction over multiple quarters |
| **Diagnostic purpose** | Provides a standardized leverage metric that normalizes debt burden relative to earnings capacity, enabling cross-period and contextual interpretation |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01 — direct coverage) |

### 4.8 FCF/Debt

**Diagnostic question**: What portion of debt could be retired from annual free cashflow generation?

| Field | Value |
|-------|-------|
| **Fact category** | FCF/debt ratio |
| **Evidence source** | Derived from free cashflow and gross/net debt from filings |
| **Includes** | Free cashflow / total debt ratio, free cashflow / net debt ratio, trend direction |
| **Diagnostic purpose** | Diagnoses deleveraging capacity — the ability to organically reduce debt from operations rather than relying on asset sales, equity issuance, or refinancing |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01 — related coverage via deleveraging capacity context) |

### 4.9 LBO History

**Diagnostic question**: Was this company subject to leveraged buyout activity, and does residual financial engineering remain?

| Field | Value |
|-------|-------|
| **Fact category** | LBO history |
| **Evidence source** | Corporate history filings, S-1 prospectuses, debt structure disclosures, ownership structure |
| **Includes** | Prior leveraged buyout events, debt-funded dividend recapitalizations, management buyout history, residual acquisition-related debt structure |
| **Diagnostic purpose** | Identifies whether current capital structure reflects organic business evolution or financial engineering legacy — LBO-originated debt structures often carry elevated leverage, aggressive amortization schedules, and restrictive covenants that persist beyond sponsor exit |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01 — related coverage via LBO leverage context) |

### 4.10 Sponsor Overhang

**Diagnostic question**: Does a financial sponsor still hold a significant equity position with potential exit pressure?

| Field | Value |
|-------|-------|
| **Fact category** | Sponsor overhang |
| **Evidence source** | Ownership disclosures, SEC 13D/13G filings, lock-up schedules, secondary offering history |
| **Includes** | Private equity sponsor ownership percentage, lock-up expiration dates, historical secondary offering cadence, registration rights |
| **Diagnostic purpose** | Diagnoses equity supply risk from sponsor exit — large sponsor positions create predictable selling pressure that may depress equity valuation and signal capital structure stress if sponsors prioritize exit over deleveraging |
| **Canonical red flag reference** | No exact canonical red flag exists for sponsor overhang — coverage note only |

### 4.11 Covenant Pressure

**Diagnostic question**: Is the company approaching or breaching financial maintenance covenants?

| Field | Value |
|-------|-------|
| **Fact category** | Covenant pressure |
| **Evidence source** | Credit agreement terms, quarterly compliance certificates, 10-Q/10-K covenant disclosures, amendment filings |
| **Includes** | Financial maintenance covenant levels (leverage, coverage, tangible net worth), current headroom, trend of headroom erosion, covenant holiday or amendment history, waiver requests |
| **Evidence requirements** | Covenant pressure interpretation requires: (1) specific covenant threshold levels from credit agreements, (2) current metric values from compliance certificates, (3) headroom calculation (threshold vs. actual), (4) trajectory of headroom over prior 4 quarters |
| **Diagnostic purpose** | Diagnoses proximity to covenant breach — covenant violations trigger lender remedies including acceleration, increased pricing, and forced asset sales. Declining headroom indicates increasing financial stress even before breach occurs. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01, RF-08-02 — related coverage via covenant metric thresholds) |

### 4.12 Bond/CDS/Rating Evidence

**Diagnostic question**: What does market pricing of credit risk and agency opinion reveal about solvency perception?

| Field | Value |
|-------|-------|
| **Fact category** | Bond/CDS/rating evidence |
| **Evidence source** | Bond secondary market pricing, CDS spread quotes, credit rating agency publications, rating action notices |
| **Includes** | Bond yield spread vs. benchmark, CDS spread level and trajectory, credit rating (S&P/Moody's/Fitch), rating outlook (positive/negative/stable), recent rating actions (upgrade/downgrade/watch) |
| **Rating treatment** | **Credit ratings are consumed as INPUT EVIDENCE, not as truth.** SAI does not assign ratings, does not endorse ratings, and does not treat ratings as sufficient for solvency conclusions. Ratings are one evidence stream requiring corroboration from direct financial analysis. |
| **Diagnostic purpose** | Provides market-based and agency-based evidence of credit risk perception. Bond spreads and CDS spreads reflect real-time market pricing of default risk. Ratings reflect agency-assessed creditworthiness on a lagging basis. Both inform diagnostic context. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-08-01, RF-08-02 — related coverage via market pricing divergence context) |

(See: fact_consumption_matrix.md, Section: SAI-BLK-08 Fact Mappings)
(See: signal_consumption_matrix.md, Section: SAI-BLK-08 Signal Mappings)

---

## 5. Balance Sheet Quality Evidence Scope (SAI-BLK-07)

SAI-BLK-07 covers overall balance sheet health with particular emphasis on asset quality concerns that intersect with credit/solvency assessment.

### 5.1 Goodwill / Intangibles / Impairment

**Diagnostic question**: How much of the asset base consists of goodwill and intangibles, and is there impairment risk that could destroy equity?

| Field | Value |
|-------|-------|
| **Fact category** | Goodwill/intangibles/impairment |
| **Evidence source** | Balance sheet filings, goodwill and intangible asset notes, impairment testing disclosures, acquisition history |
| **Includes** | Goodwill carrying value, goodwill/total assets ratio, goodwill/equity ratio, intangible asset composition (finite vs. indefinite-lived), impairment testing methodology, recent impairment charges, cumulative impairment history, reporting unit goodwill allocation |
| **Diagnostic purpose** | Goodwill and intangibles represent acquisition premiums that may not be recoverable. Elevated goodwill/equity ratios indicate that a single impairment event could eliminate a material portion of book equity, distorting leverage metrics and potentially triggering covenant breaches. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-07-02 — direct coverage) |

### 5.2 Capital Structure Composition

**Diagnostic question**: How is the balance sheet funded, and what is the quality of the equity base?

| Field | Value |
|-------|-------|
| **Fact category** | Capital structure composition |
| **Evidence source** | Balance sheet filings, equity notes, debt notes, preferred stock disclosures |
| **Includes** | Debt/equity ratio, tangible equity, preferred stock obligations, hybrid instruments, minority interests, treasury stock |
| **Diagnostic purpose** | Establishes the true capitalization quality — distinguishing between companies funded by retained earnings and real equity versus companies whose "equity" consists largely of goodwill created through debt-funded acquisitions |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-07-02 — related coverage via tangible equity context) |

(See: fact_consumption_matrix.md, Section: SAI-BLK-07 Fact Mappings)
(See: block_taxonomy.md, Section: SAI-BLK-07 Balance Sheet Quality)

---

## 6. Hidden Liabilities Evidence Scope (SAI-BLK-09)

SAI-BLK-09 covers off-balance-sheet obligations, contingent liabilities, and undisclosed risks that may materially alter the true economic liability profile. Per SAI-REQ-8 Acceptance Criterion 3, this block must cover: off-balance-sheet, litigation, guarantees, contingencies, and goodwill risk.

### 6.1 Lease Liabilities

**Diagnostic question**: What are the lease obligations not fully reflected in headline debt metrics?

| Field | Value |
|-------|-------|
| **Fact category** | Lease liabilities |
| **Evidence source** | Balance sheet (right-of-use assets, lease liabilities), lease maturity schedules, operating lease disclosures, IFRS 16 / ASC 842 notes |
| **Includes** | Finance lease obligations, operating lease obligations (on-balance under IFRS 16 / ASC 842), lease maturity profile, variable lease payments, short-term lease exclusions, sale-and-leaseback arrangements |
| **Diagnostic purpose** | Lease liabilities represent real economic obligations that reduce financial flexibility. Under IFRS 16 / ASC 842 most leases appear on-balance, but pre-adoption comparisons and variable/short-term lease exclusions may still obscure total obligation magnitude. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-09-01 — related coverage via off-balance obligation context) |

### 6.2 Purchase Obligations

**Diagnostic question**: What non-cancellable purchase commitments create future cash outflow obligations?

| Field | Value |
|-------|-------|
| **Fact category** | Purchase obligations |
| **Evidence source** | Contractual obligation tables in 10-K/20-F, supply agreement disclosures, minimum purchase commitments |
| **Includes** | Non-cancellable purchase orders, take-or-pay contracts, minimum volume commitments, supply agreement obligations, technology licensing minimums |
| **Diagnostic purpose** | Purchase obligations represent committed future cash outflows that reduce financial flexibility and may become onerous if demand declines. They function as off-balance-sheet debt equivalents that are not captured in traditional leverage metrics. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-09-01 — related coverage via off-balance obligation context) |

### 6.3 Off-Balance-Sheet Commitments

**Diagnostic question**: What obligations exist that do not appear on the primary balance sheet?

| Field | Value |
|-------|-------|
| **Fact category** | Off-balance commitments |
| **Evidence source** | Variable interest entity (VIE) disclosures, special purpose entity notes, joint venture obligations, partnership commitments, operating agreement commitments |
| **Includes** | VIE exposures, unconsolidated entity obligations, joint venture capital calls, partnership capital commitments, operating agreement guarantees, securitization residual interests |
| **Diagnostic purpose** | Off-balance commitments represent real economic exposure that traditional debt metrics fail to capture. They create contingent claims on cashflow that may crystallize during stress periods when the company is least able to absorb them. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-09-01 — direct coverage) |

### 6.4 Litigation and Contingencies

**Diagnostic question**: What legal claims and contingent liabilities could crystallize into material obligations?

| Field | Value |
|-------|-------|
| **Fact category** | Litigation and contingencies |
| **Evidence source** | Legal proceedings disclosures, contingent liability notes, loss contingency assessments, class action filings |
| **Includes** | Material litigation exposures, class action status, regulatory investigation exposure, loss contingency provisions, unrecorded loss contingencies (disclosed but not accrued), guarantee obligations, indemnification commitments |
| **Diagnostic purpose** | Litigation and contingent liabilities represent potential cash outflows that may materially alter the solvency trajectory. Even unresolved cases create uncertainty that affects refinancing access and credit market confidence. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-09-02 — direct coverage) |

### 6.5 Guarantees

**Diagnostic question**: What third-party obligations has the company guaranteed that could become direct liabilities?

| Field | Value |
|-------|-------|
| **Fact category** | Guarantees |
| **Evidence source** | Guarantee disclosures in financial statement notes, subsidiary guarantees, joint venture guarantee obligations |
| **Includes** | Parent guarantees of subsidiary debt, performance guarantees, financial guarantees to third parties, residual value guarantees, standby letters of credit, intra-group guarantees for consolidation purposes |
| **Diagnostic purpose** | Guarantees create contingent liabilities that are invisible in headline metrics until triggered. When the guaranteed party defaults, the guarantor's debt effectively increases instantaneously without warning. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-09-02 — related coverage via contingent liabilities context) |

(See: fact_consumption_matrix.md, Section: SAI-BLK-09 Fact Mappings)
(See: red_flag_taxonomy.md, Section: SAI-BLK-09 Red Flags)

---

## 7. Pension Obligations Evidence Scope (SAI-BLK-10)

SAI-BLK-10 covers pension funding status, obligation trajectory, and actuarial risk. Per SAI-REQ-8 Acceptance Criterion 4, this block must cover: defined benefit obligations, funding gap, and plan asset adequacy.

### 7.1 Pension Obligations (Defined Benefit)

**Diagnostic question**: What is the total present value of defined benefit pension promises?

| Field | Value |
|-------|-------|
| **Fact category** | Pension obligations |
| **Evidence source** | Pension and OPEB notes in 10-K/20-F, projected benefit obligation (PBO) or defined benefit obligation (DBO), actuarial valuation reports |
| **Includes** | Projected benefit obligation (PBO/DBO), accumulated benefit obligation (ABO), plan participant demographics, discount rate assumptions, salary growth assumptions, mortality assumptions, benefit payment projections |
| **Diagnostic purpose** | Pension obligations represent contractual promises to employees that function as long-duration debt equivalents. They are sensitive to discount rate assumptions and demographic changes, making them inherently uncertain in magnitude. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-10-01 — direct coverage) |

### 7.2 Pension Funding Gap

**Diagnostic question**: How much of the pension obligation is unfunded, and what is the trajectory?

| Field | Value |
|-------|-------|
| **Fact category** | Pension funding gap |
| **Evidence source** | Plan asset disclosures, funded status reconciliation, contribution history, regulatory funding requirements |
| **Includes** | Plan assets at fair value, funded status (plan assets minus PBO), funding ratio (plan assets / PBO), mandatory contribution requirements, voluntary contribution history, asset allocation (equity/fixed income/alternatives), expected return on plan assets assumption |
| **Diagnostic purpose** | The pension funding gap represents an economic liability that may require material future cash contributions to close. A widening funding gap competes with debt service, capex, and shareholder returns for available cashflow. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-10-01 — direct coverage) |

### 7.3 Plan Asset Adequacy

**Diagnostic question**: Are the pension plan assets appropriately matched to the obligation structure?

| Field | Value |
|-------|-------|
| **Fact category** | Plan asset adequacy |
| **Evidence source** | Plan asset allocation disclosures, investment policy statements, LDI (Liability-Driven Investment) adoption, duration matching disclosures |
| **Includes** | Asset allocation breakdown, equity vs. fixed income mix, duration of fixed income assets vs. obligation duration, use of liability-driven investment strategies, plan asset performance vs. expected return, alternative investment exposure |
| **Diagnostic purpose** | Plan asset adequacy determines whether the funding gap is likely to widen or narrow without sponsor contributions. Aggressive asset allocation (high equity) increases funded status volatility. Mismatched duration creates interest rate risk that can rapidly widen the gap. |
| **Canonical red flag reference** | (See: red_flag_taxonomy.md, RF-10-02 — related coverage via actuarial assumption context) |

(See: fact_consumption_matrix.md, Section: SAI-BLK-10 Fact Mappings)
(See: red_flag_taxonomy.md, Section: SAI-BLK-10 Red Flags)

---

## 8. Credit Rating Treatment

This section formally documents the SAI position on credit ratings, satisfying SAI-REQ-8 Acceptance Criterion 2.

### 8.1 Canonical Statement

> **Credit ratings are consumed as INPUT EVIDENCE, not as truth.**
>
> SAI does not assign credit ratings. SAI does not endorse credit ratings as authoritative conclusions about creditworthiness. SAI does not substitute credit ratings for direct balance sheet and cashflow analysis. A credit rating is one piece of evidence — no more authoritative than bond spread evidence, covenant headroom evidence, or direct leverage ratio observation.

### 8.2 Rating Evidence Usage Rules

| Rule | Description |
|------|-------------|
| **Consumption only** | SAI consumes ratings as observed facts from external sources. SAI never produces or assigns ratings. |
| **No substitution** | A credit rating cannot substitute for direct financial analysis. A BBB+ rating does not prove solvency; a BB- rating does not prove distress. |
| **Lag awareness** | Ratings are known to lag market pricing of credit risk. SAI must note when bond/CDS market evidence diverges materially from current rating, as this divergence is itself diagnostic evidence. |
| **No endorsement** | SAI output must never contain language that endorses or elevates a rating above other evidence (e.g., "the company is investment grade" is a factual observation; "the company is safe because it is investment grade" crosses into endorsement). |
| **Conflict documentation** | When rating evidence conflicts with direct financial analysis (e.g., investment-grade rating but leverage metrics consistent with high-yield profiles), the conflict must be documented explicitly in the interpretation. |
| **Multi-agency divergence** | When agencies disagree (split rating), SAI documents the divergence as evidence of credit risk ambiguity — it does not adjudicate which agency is correct. |

### 8.3 What SAI May State About Ratings

- "Current credit rating is [X] as of [date], assigned by [agency]" (factual observation)
- "Rating outlook is [positive/negative/stable] as of [date]" (factual observation)
- "Rating was [upgraded/downgraded] on [date] from [X] to [Y]" (factual observation)
- "Rating evidence diverges from CDS market pricing of credit risk" (conflict observation)
- "Rating has not been updated in [N months] despite material fundamental changes" (lag observation)

### 8.4 What SAI Must NOT State About Ratings

- "The company is safe/sound/creditworthy because of its rating" (endorsement)
- "The rating confirms adequate solvency" (substitution for analysis)
- "Investment grade status indicates low risk" (inference beyond evidence)
- "A downgrade to [X] would make this company distressed" (prediction)
- "The rating should be [X]" (rating assignment)
- "The rating is wrong/inadequate/generous" (rating adjudication)

(See: requirements.md, Section: SAI-REQ-8, Acceptance Criterion 2)

---

## 9. Red Flag Cross-Reference to Canonical Taxonomy

This artifact does NOT create, define, or add new red flags. The canonical red flag definitions for financial stability blocks reside exclusively in the red flag taxonomy artifact. This section cross-references each SAI-REQ-8 evidence category against the canonical red flag taxonomy to document coverage relationships.

| # | Evidence Category | Primary Block | Related Canonical red_flag_id(s) | Canonical Red Flag Title / Summary | Coverage Status |
|---|------------------|---------------|----------------------------------|-----------------------------------|----------------|
| 1 | Gross debt | SAI-BLK-08 | RF-08-01 | Net Debt/EBITDA Exceeds 4x (covers gross debt leverage context) | related canonical coverage |
| 2 | Net debt | SAI-BLK-08 | RF-08-01 | Net Debt/EBITDA Exceeds 4x | direct canonical coverage |
| 3 | Maturity schedule | SAI-BLK-08 | RF-07-01 | Material Maturity Wall Within 18 Months | direct canonical coverage |
| 4 | Short-term debt | SAI-BLK-08 | RF-07-01 | Material Maturity Wall Within 18 Months (covers near-term debt pressure) | related canonical coverage |
| 5 | Available liquidity | SAI-BLK-08 | RF-07-01, RF-08-02 | Material Maturity Wall / Interest Coverage Below 2x (liquidity context) | related canonical coverage |
| 6 | Interest coverage | SAI-BLK-08 | RF-08-02 | Interest Coverage Below 2x | direct canonical coverage |
| 7 | Net debt/EBITDA | SAI-BLK-08 | RF-08-01 | Net Debt/EBITDA Exceeds 4x | direct canonical coverage |
| 8 | FCF/debt | SAI-BLK-08 | RF-08-01 | Net Debt/EBITDA Exceeds 4x (deleveraging capacity context) | related canonical coverage |
| 9 | LBO history | SAI-BLK-08 | RF-08-01 | Net Debt/EBITDA Exceeds 4x (LBO leverage context) | related canonical coverage |
| 10 | Sponsor overhang | SAI-BLK-08 | — | No exact canonical red flag exists for sponsor overhang | coverage note only |
| 11 | Covenant pressure | SAI-BLK-08 | RF-08-01, RF-08-02 | Net Debt/EBITDA Exceeds 4x / Interest Coverage Below 2x (covenant tests reference these metrics) | related canonical coverage |
| 12 | Bond/CDS/rating | SAI-BLK-08 | RF-08-01, RF-08-02 | Net Debt/EBITDA / Interest Coverage (market pricing divergence context) | related canonical coverage |
| 13 | Goodwill/intangibles/impairment | SAI-BLK-07 | RF-07-02 | Goodwill Exceeding 100% of Tangible Equity | direct canonical coverage |
| 14 | Capital structure | SAI-BLK-07 | RF-07-02 | Goodwill Exceeding 100% of Tangible Equity (tangible equity context) | related canonical coverage |
| 15 | Lease liabilities | SAI-BLK-09 | RF-09-01 | Off-Balance-Sheet Obligations Exceeding 30% of Reported Debt (leases as obligation component) | related canonical coverage |
| 16 | Purchase obligations | SAI-BLK-09 | RF-09-01 | Off-Balance-Sheet Obligations Exceeding 30% of Reported Debt (purchase commitments as obligation component) | related canonical coverage |
| 17 | Off-balance commitments | SAI-BLK-09 | RF-09-01 | Off-Balance-Sheet Obligations Exceeding 30% of Reported Debt | direct canonical coverage |
| 18 | Litigation/contingencies | SAI-BLK-09 | RF-09-02 | Aggregate Contingent Liabilities Exceeding 15% of Equity | direct canonical coverage |
| 19 | Guarantees | SAI-BLK-09 | RF-09-02 | Aggregate Contingent Liabilities Exceeding 15% of Equity (guarantees as contingent liabilities) | related canonical coverage |
| 20 | Pension obligations | SAI-BLK-10 | RF-10-01 | Pension Underfunding Exceeding 20% of Market Cap | direct canonical coverage |
| 21 | Pension funding gap | SAI-BLK-10 | RF-10-01 | Pension Underfunding Exceeding 20% of Market Cap | direct canonical coverage |
| 22 | Plan asset adequacy | SAI-BLK-10 | RF-10-02 | Discount Rate Assumption Exceeding Peer Median by 100bps (actuarial assumption context) | related canonical coverage |

### Coverage Status Legend

| Status | Meaning |
|--------|---------|
| **direct canonical coverage** | A canonical red flag in red_flag_taxonomy.md directly addresses this evidence category |
| **related canonical coverage** | A canonical red flag addresses a closely related condition that encompasses or contextualizes this evidence category |
| **coverage note only** | No exact canonical red flag exists for this evidence category in the current taxonomy. This artifact does NOT create a new red flag to fill the gap. If coverage is needed, it must be proposed as an additive extension to the canonical red flag taxonomy via its own process. |

### Notes

- This artifact does NOT define red flags, assign RF IDs, or establish new red flag conditions.
- All canonical red flag definitions, evidence thresholds, temporal persistence rules, and severity assignments reside in the red flag taxonomy artifact.
- Evidence categories marked "coverage note only" represent areas where the canonical taxonomy may be extended in the future via the additive-only extension mechanism — but that extension is NOT performed by this artifact.

(See: red_flag_taxonomy.md, Section: 5.7 SAI-BLK-07 Red Flags)
(See: red_flag_taxonomy.md, Section: 5.8 SAI-BLK-08 Red Flags)
(See: red_flag_taxonomy.md, Section: 5.9 SAI-BLK-09 Red Flags)
(See: red_flag_taxonomy.md, Section: 5.10 SAI-BLK-10 Red Flags)

---

## 10. Explicit Prohibition Section

The following outputs, labels, conclusions, and language are absolutely prohibited within SAI-BLK-07, SAI-BLK-08, SAI-BLK-09, and SAI-BLK-10. Their presence in any SAI deliverable constitutes architectural drift and boundary violation.

### 10.1 Prohibited Outputs

| # | Prohibited Item | Category | Reason |
|---|----------------|----------|--------|
| 1 | Credit score | Scoring | SAI diagnoses credit risk evidence; it does not produce numeric credit scores |
| 2 | Default probability | Prediction | Default prediction requires statistical models beyond SAI's diagnostic scope |
| 3 | Credit rating assignment | Rating | SAI consumes ratings as evidence; it never assigns, endorses, or challenges ratings |
| 4 | Bankruptcy prediction | Prediction | Bankruptcy modeling (Altman Z-score, distance-to-default) is not SAI's domain |
| 5 | Recovery rate estimate | Prediction | Recovery estimation requires distressed debt valuation methodology not within SAI |
| 6 | Debt capacity calculation | Recommendation | Calculating how much debt a company can sustain implies advisory capacity SAI lacks |
| 7 | Refinancing recommendation | Recommendation | SAI diagnoses refinancing pressure; it does not recommend refinancing actions |
| 8 | Investment grade / high yield classification | Rating | These are rating categories. SAI observes external classifications but does not assign them. |
| 9 | "Safe" / "sound" / "healthy" labels | Scoring | These imply a binary solvency judgment that collapses evidence into a single conclusion |
| 10 | Buy/sell/hold implication from credit evidence | Decision | Credit evidence informs diagnostic context; it never instructs action |
| 11 | Numeric risk score from leverage ratios | Scoring | Leverage ratios are evidence for interpretation, not inputs to scoring formulas |
| 12 | Pension adequacy score | Scoring | Pension funding is diagnostic evidence, not a scoreable attribute |

### 10.2 Prohibited Language

The following words and phrases are forbidden in any SAI-BLK-07, SAI-BLK-08, SAI-BLK-09, or SAI-BLK-10 output:

**Scoring language** (forbidden):
- "credit score", "risk score", "solvency score"
- "high risk", "low risk", "medium risk" (as labels — descriptive context is allowed)
- "creditworthy", "not creditworthy"
- "investment grade quality", "junk quality"

**Prediction language** (forbidden):
- "will default", "likely to default", "probability of default"
- "bankruptcy risk of X%", "survival probability"
- "expected loss", "loss given default"

**Recommendation language** (forbidden):
- "should refinance", "must deleverage"
- "avoid due to leverage", "attractive on credit basis"
- "safe to invest", "too risky"
- "buy", "sell", "hold"

**Rating assignment language** (forbidden):
- "this is effectively investment grade", "this is effectively high yield"
- "the rating should be [X]", "deserves a higher/lower rating"
- "misrated", "under-rated", "over-rated"

### 10.3 Allowed Language

The following language is permitted because it describes diagnostic observations:

**Diagnostic context language** (allowed):
- "leverage metrics consistent with [X] category" (observation, not assignment)
- "covenant headroom declining" (factual trajectory)
- "maturity wall creates refinancing pressure point" (structural observation)
- "interest coverage margin of safety narrowing" (trend observation)
- "CDS market pricing diverges from current agency rating" (conflict observation)
- "pension funding gap trajectory suggests increasing future contributions" (evidence-based projection of cashflow impact, not recommendation)
- "off-balance-sheet obligations materially alter effective leverage profile" (diagnostic conclusion)

(See: output_object_spec.md, Section: Prohibited Fields)
(See: requirements.md, Section: SAI-REQ-5 — Non-Scoring / Non-Recommendation Constraint)

---

## 11. Evidence Category to Block Mapping

This section provides the complete mapping of all SAI-REQ-8 evidence categories to their governing blocks, satisfying Acceptance Criterion 1.

| # | Evidence Category | Primary Block | Secondary Block(s) | Fact Category Mapping |
|---|------------------|---------------|-------------------|----------------------|
| 1 | Gross debt | SAI-BLK-08 | SAI-BLK-07 | Gross debt |
| 2 | Net debt | SAI-BLK-08 | SAI-BLK-07 | Net debt |
| 3 | Maturity schedule | SAI-BLK-08 | — | Maturity schedule |
| 4 | Short-term debt | SAI-BLK-08 | — | Short-term debt |
| 5 | Available liquidity | SAI-BLK-08 | — | Available liquidity |
| 6 | Interest coverage | SAI-BLK-08 | — | Interest coverage |
| 7 | Net debt/EBITDA | SAI-BLK-08 | — | Net debt/EBITDA ratio |
| 8 | FCF/debt | SAI-BLK-08 | — | FCF/debt ratio |
| 9 | Lease liabilities | SAI-BLK-09 | — | Lease liabilities |
| 10 | Purchase obligations | SAI-BLK-09 | — | Purchase obligations |
| 11 | Off-balance commitments | SAI-BLK-09 | — | Off-balance commitments |
| 12 | Pension obligations | SAI-BLK-10 | — | Pension obligations |
| 13 | Pension funding gap | SAI-BLK-10 | — | Pension funding gap |
| 14 | Goodwill/intangibles/impairment | SAI-BLK-07 | SAI-BLK-09 | Goodwill/intangibles/impairment |
| 15 | LBO history | SAI-BLK-08 | — | LBO history |
| 16 | Sponsor overhang | SAI-BLK-08 | — | Sponsor overhang |
| 17 | Covenant pressure | SAI-BLK-08 | — | Covenant pressure |
| 18 | Bond/CDS/rating evidence | SAI-BLK-08 | — | Bond/CDS/rating evidence |

**Coverage confirmation**: All 18 evidence categories listed in SAI-REQ-8 have explicit block assignments with fact category mappings.

(See: fact_consumption_matrix.md, Section: Block Coverage Matrix)

---

## 12. Relationship to Fact Consumption Matrix

The financial stability blocks consume the following fact category groups from the Market Evidence Framework:

| Block | Fact Category Groups Consumed |
|-------|------------------------------|
| SAI-BLK-07 | Total assets, equity, debt structure, asset composition, goodwill/intangibles |
| SAI-BLK-08 | Gross debt, net debt, maturity schedule, interest coverage, credit ratings, covenants, LBO history, sponsor overhang, short-term debt, available liquidity, FCF/debt, net debt/EBITDA |
| SAI-BLK-09 | Operating leases, purchase obligations, guarantees, litigation, off-balance items, goodwill risk |
| SAI-BLK-10 | Defined benefit obligations, plan assets, funding gap, actuarial assumptions |

SAI does not create these facts. It consumes them from the Market Evidence Framework via declarative consumption contracts.

(See: fact_consumption_matrix.md, Section: Financial Stability Block Mappings)

---

## 13. Relationship to Signal Consumption Matrix

The financial stability blocks consume the following signal categories:

| Block | Signal Categories Consumed |
|-------|---------------------------|
| SAI-BLK-07 | Leverage signals, asset quality signals, capital structure signals |
| SAI-BLK-08 | Credit deterioration signals, refinancing risk signals, covenant pressure signals |
| SAI-BLK-09 | Hidden obligation signals, contingent liability signals |
| SAI-BLK-10 | Pension underfunding signals, obligation growth signals |

SAI does not calculate these signals. It consumes them from the Market Evidence Framework via declarative consumption contracts.

(See: signal_consumption_matrix.md, Section: Financial Stability Signal Mappings)

---

## 14. Relationship to Provenance Contract

All financial stability interpretations must satisfy the provenance contract:

- Every credit/solvency observation must trace to specific fact IDs (debt values, coverage ratios, covenant levels)
- Every signal consumption must trace to specific signal IDs (credit deterioration, refinancing risk)
- Timestamp inheritance applies — interpretations inherit temporal context from source filing dates
- No orphan credit interpretations are valid (an interpretation without filing-backed evidence is invalid)
- Staleness thresholds for quarterly temporal class apply: stale after 100 days, expired after 120 days

Financial stability blocks are particularly sensitive to evidence freshness because:
- Covenant compliance can change within a single quarter
- Maturity walls can become imminent between filing dates
- Credit market signals (CDS, bond spreads) may diverge from quarterly fundamental data

When daily credit market signals conflict with quarterly fundamental data, both are reported with their respective timestamps. The conflict itself is diagnostic evidence of potential rapid deterioration or recovery.

(See: provenance_contract.md, Section: Provenance Chain Specification)
(See: provenance_contract.md, Section: Timestamp Inheritance Rules)
(See: temporal_resolution_matrix.md, Section: Quarterly Temporal Class)

---

## 15. Relationship to Output Object Specification

SAI-BLK-07, SAI-BLK-08, SAI-BLK-09, and SAI-BLK-10 produce output objects conforming to the canonical SAI output object specification. The credit/solvency artifact adds the following constraints beyond standard output object rules:

1. The `interpretation_summary` field must reference evidence from the specific financial stability dimension being diagnosed
2. The `evidence_completeness` field must be "insufficient" if primary debt/leverage facts are unavailable for SAI-BLK-08
3. The `red_flags` field must use only categorical severity (informational/elevated/critical) — never numeric
4. The `deferred_dependency_notes` field must document any missing evidence categories from the SAI-REQ-8 scope
5. The `interpretation_summary` field must never contain any language from the prohibited list (Section 10.2)
6. Rating evidence in `consumed_facts` must be accompanied by the canonical statement that ratings are input evidence, not truth

(See: output_object_spec.md, Section: Allowed Fields)
(See: output_object_spec.md, Section: Prohibited Fields)

---

## 16. Relationship to Red Flag Taxonomy

All financial stability blocks produce red flags documented in the canonical red flag taxonomy. This artifact does NOT define, create, or redefine red flags. Section 9 provides cross-references between SAI-REQ-8 evidence categories and their corresponding canonical red flags in the red flag taxonomy artifact. The comprehensive red flag definitions with full evidence thresholds and temporal persistence rules reside exclusively in that artifact.

Red flags in financial stability blocks are diagnostic observations. They MUST NOT:
- Become numeric risk scores
- Trigger automated actions
- Map to buy/sell/hold decisions
- Aggregate into composite credit ratings
- Be weighted or prioritized algorithmically
- Imply "sell" or "avoid" (detection of elevated leverage is an observation, not a recommendation)

(See: red_flag_taxonomy.md, Section: SAI-BLK-07 Red Flags)
(See: red_flag_taxonomy.md, Section: SAI-BLK-08 Red Flags)
(See: red_flag_taxonomy.md, Section: SAI-BLK-09 Red Flags)
(See: red_flag_taxonomy.md, Section: SAI-BLK-10 Red Flags)

---

## 17. Relationship to Valuation Boundary

Credit/solvency evidence is a mandatory input dimension for valuation interpretation (Dimension 2 in the valuation boundary artifact). SAI-BLK-17 (Valuation Context) and SAI-BLK-18 (Value Trap Guard) require credit/solvency evidence before producing any valuation interpretation.

This creates a conceptual evidence dependency (not a block-to-block execution dependency):
- If SAI-BLK-08 has insufficient evidence, SAI-BLK-17 and SAI-BLK-18 must set `evidence_completeness` to "insufficient"
- Valuation interpretation without solvency evidence is explicitly prohibited by SAI-REQ-7
- This artifact defines what constitutes "solvency evidence" for that requirement

Each block remains independently executable — the dependency is at the evidence-availability level, not at the execution order level.

(See: valuation_boundary.md, Section: 4.2 Credit/Solvency Evidence — Dimension 2)
(See: valuation_boundary.md, Section: 5.3 Solvency Evidence Requirement)

---

## 18. Acceptance Criteria Traceability

This section documents how each SAI-REQ-8 acceptance criterion is satisfied by this artifact.

| # | Acceptance Criterion | Artifact Section | Status |
|---|---------------------|-----------------|--------|
| 1 | All listed financial stability categories have explicit fact category mappings | Section 11 — Evidence Category to Block Mapping | Satisfied — all 18 categories mapped |
| 2 | Credit ratings documented as "input evidence, not truth" | Section 8 — Credit Rating Treatment | Satisfied — canonical statement and usage rules defined |
| 3 | Hidden liabilities block covers: off-balance-sheet, litigation, guarantees, contingencies, goodwill risk | Section 6 — Hidden Liabilities Evidence Scope | Satisfied — Sections 6.1–6.5 cover all required items |
| 4 | Pension obligations block covers: defined benefit obligations, funding gap, plan asset adequacy | Section 7 — Pension Obligations Evidence Scope | Satisfied — Sections 7.1–7.3 cover all required items |
| 5 | LBO history and sponsor overhang addressed within Credit/Solvency Risk | Section 4.9 (LBO History), Section 4.10 (Sponsor Overhang) | Satisfied — both within SAI-BLK-08 |
| 6 | Covenant pressure indicators defined with evidence requirements | Section 4.11 — Covenant Pressure | Satisfied — evidence requirements explicitly listed |
| 7 | Each evidence category is cross-referenced against the canonical red flag taxonomy or explicitly marked as a coverage note without creating new red flags | Section 9 — Red Flag Cross-Reference to Canonical Taxonomy | Satisfied — all 18 categories cross-referenced; 8 direct, 9 related, 1 coverage note only |

---

## 19. Verification Gate Evidence

### VG-SAI-1 (Requirements Completeness Gate) Evidence

This artifact provides evidence for VG-SAI-1 (Requirements Completeness Gate) by demonstrating that:

1. All 4 Financial Stability blocks (SAI-BLK-07, SAI-BLK-08, SAI-BLK-09, SAI-BLK-10) are defined with stable identifiers, categories, purposes, fact families, signal families, temporal resolution, and boundary statements (Section 3)
2. All 18 evidence categories mandated by SAI-REQ-8 have explicit fact category mappings (Section 11)
3. Each block has its full evidence scope defined with diagnostic questions and evidence sources (Sections 4–7)
4. The credit rating treatment principle is explicitly documented (Section 8)
5. All 7 acceptance criteria from SAI-REQ-8 are traceable to specific artifact sections (Section 18)
6. Financial-stability red flag relationships are cross-referenced to the canonical red flag taxonomy (Section 9)

**VG-SAI-1 evidence claim**: This artifact demonstrates that the Financial Stability category of the SAI block taxonomy is completely defined with all required evidence categories, fact mappings, signal mappings, and boundary constraints per SAI-REQ-8. VG-SAI-1 gate execution requires this artifact combined with the block taxonomy artifact to confirm full 24-block completeness.

---

## 20. No-Drift Statement

This artifact is a definition-layer document. It has been verified to contain:

- ✓ Zero implementation code
- ✓ Zero credit scoring models or default probability calculations
- ✓ Zero bankruptcy prediction logic
- ✓ Zero credit rating assignment or endorsement
- ✓ Zero scoring, ranking, or recommendation logic
- ✓ Zero allocation decisions or position sizing
- ✓ Zero trading signals or buy/sell/hold instructions
- ✓ Zero registry or SSOT mutations
- ✓ Zero fact/signal/evidence primitive creation
- ✓ Zero asset-to-narrative mappings
- ✓ All cross-references in canonical (See: [Deliverable], Section: [Title]) format
- ✓ Credit ratings documented as input evidence, not truth
- ✓ Zero red flag creation — all red flag references point to canonical red_flag_taxonomy.md

If scope pressure toward implementation, scoring, rating assignment, or recommendation is detected during future task execution, this artifact must be consulted as the authoritative boundary reference for financial stability interpretation within SAI.

---

*End of artifact.*
