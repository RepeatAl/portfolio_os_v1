# Single Asset Intelligence Framework — Red Flag Taxonomy

**Artifact**: red_flag_taxonomy.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 6.1 Create red flag taxonomy
**Requirements**: SAI-REQ-13 (Red Flag Taxonomy per Analysis Block)
**Verification Gate**: VG-SAI-8 (Red Flag Taxonomy Gate)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the complete red flag taxonomy for the Single Asset Intelligence Framework. It enumerates all evidence-based diagnostic warning conditions across all 24 canonical analysis blocks. Each red flag specifies what condition triggers it, what evidence must be present, how long the condition must persist, what severity category applies, and what provenance is required.

Red flags are categorical, evidence-based warnings. They identify conditions that require review, investigation, or attention. They do NOT trigger actions, produce scores, recommend positions, or aggregate into composite risk ratings.

This is a definition-layer artifact. It contains no implementation code, no scoring logic, no allocation decisions, and no executable architecture.

(See: design.md, Section: Data Models — Red Flag Design)
(See: requirements.md, Section: SAI-REQ-13 — Red Flag Taxonomy per Analysis Block)
(See: output_object_spec.md, Section: 2 — Allowed Fields, Field #6 red_flags)

---

## 2. Severity Taxonomy

Red flag severity is categorical only. Severity levels are qualitative indicators of diagnostic concern — they are NOT numeric scores, NOT weighted priorities, and NOT action triggers.

| Severity | Definition | Implication |
|----------|-----------|-------------|
| **informational** | Notable condition worth monitoring — does not require action | Condition is present and documented; no immediate diagnostic concern but worth periodic review |
| **elevated** | Condition indicating material risk requiring attention — warrants deeper investigation | Condition exceeds normal operating range and indicates material risk that requires focused review and monitoring |
| **critical** | Condition indicating severe risk requiring immediate attention — demands urgent review | Condition indicates severe diagnostic concern that demands urgent investigation and close ongoing monitoring |

### Severity Boundary Rules

- Severity levels are NOT numeric and MUST NOT be converted to numbers (e.g., informational=1, elevated=2, critical=3 is PROHIBITED)
- Severity levels MUST NOT be aggregated across blocks (e.g., "total critical flags = X" is informational metadata, NOT a risk score)
- Severity levels MUST NOT be weighted, averaged, or combined into composite ratings
- Severity levels MUST NOT trigger automated actions, position changes, or portfolio decisions
- Severity assignment is evidence-based and condition-specific — the same block may have both informational and critical flags depending on the specific condition

---

## 3. Red Flag ID Convention

All red flags follow the format: **RF-NN-XX**

| Component | Meaning | Example |
|-----------|---------|---------|
| RF | Red Flag prefix | RF |
| NN | Block number (01–24), matching SAI-BLK-NN | 08 = Credit/Solvency Risk |
| XX | Sequential flag number within the block (01, 02, 03...) | 01 = first flag, 02 = second flag |

**Examples**:
- `RF-01-01` = First red flag for SAI-BLK-01 (Asset Identity)
- `RF-08-02` = Second red flag for SAI-BLK-08 (Credit/Solvency Risk)
- `RF-24-01` = First red flag for SAI-BLK-24 (Portfolio Fit)

ID assignment is stable and additive-only. Once assigned, a red flag ID is never reused or reassigned. New flags receive the next sequential XX number within their block.

---

## 4. Red Flag Field Definitions

Each red flag contains exactly 8 fields:

| # | Field | Description |
|---|-------|-------------|
| 1 | red_flag_id | Unique identifier in RF-NN-XX format |
| 2 | block_id | Reference to the canonical block (SAI-BLK-NN) |
| 3 | condition | The diagnostic condition that triggers this flag — what observable state constitutes the warning |
| 4 | required_evidence | Which specific facts and/or signals must be present to assert this flag — the evidentiary threshold |
| 5 | temporal_persistence | How long the condition must persist before the flag is asserted — prevents transient noise from triggering flags |
| 6 | severity | Categorical severity: informational, elevated, or critical |
| 7 | provenance_requirement | What evidence sources must be cited when asserting this flag — ensures traceability |
| 8 | non_action_statement | Explicit declaration that this flag does NOT trigger portfolio action, trading decisions, or position changes |

---

## 5. Red Flag Definitions by Block

### 5.1 SAI-BLK-01: Asset Identity (Foundation)

#### RF-01-01: Corporate Structure Opacity

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-01-01 |
| **block_id** | SAI-BLK-01 |
| **condition** | Corporate structure is materially opaque — significant subsidiaries, holding layers, or cross-holdings that prevent clear identification of economic exposure and beneficial ownership |
| **required_evidence** | Company filings showing multi-layered holding structure with ≥3 intermediate entities; OR missing subsidiary disclosures where peer companies provide them; OR regulatory filings indicating complex cross-border ownership chains |
| **temporal_persistence** | Sustained across 2+ consecutive annual filings |
| **severity** | elevated |
| **provenance_requirement** | Annual report corporate structure disclosures, subsidiary listings, regulatory filings (SEC 10-K Exhibit 21, equivalent for non-US) |
| **non_action_statement** | This flag indicates evidence limitation requiring investigation. It does NOT trigger position reduction, avoidance, or any portfolio action. |

#### RF-01-02: Sector Classification Conflict

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-01-02 |
| **block_id** | SAI-BLK-01 |
| **condition** | Material disagreement between major classification systems (GICS, ICB, NAICS) on the primary sector/industry assignment, indicating ambiguous business model boundaries |
| **required_evidence** | At least 2 recognized classification systems assigning the asset to different sectors at the top level (not sub-industry level); OR the company's self-described primary business does not match any classification system's primary assignment |
| **temporal_persistence** | Present in current classification period — single observation sufficient given classification stability |
| **severity** | informational |
| **provenance_requirement** | GICS classification data, ICB classification data, company self-description from latest filing, NAICS code assignment |
| **non_action_statement** | This flag indicates a classification ambiguity requiring review for correct peer group assignment. It does NOT trigger any portfolio action or position change. |

---

### 5.2 SAI-BLK-02: Business Model Quality (Foundation)

#### RF-02-01: Revenue Model Fragility

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-02-01 |
| **block_id** | SAI-BLK-02 |
| **condition** | Revenue model demonstrates structural fragility — high dependency on non-recurring revenue sources, project-based revenue without visible pipeline, or transactional revenue without demonstrated repeat purchase behavior |
| **required_evidence** | Non-recurring or project-based revenue exceeding 60% of total revenue; OR recurring revenue ratio declining for 3+ consecutive quarters; OR revenue model lacks contractual visibility beyond current quarter |
| **temporal_persistence** | 3+ consecutive quarters showing fragility pattern |
| **severity** | elevated |
| **provenance_requirement** | Quarterly revenue breakdowns from filings, segment disclosures, management commentary on revenue composition, backlog/RPO disclosures |
| **non_action_statement** | This flag indicates diagnostic concern about business model sustainability requiring deeper investigation. It does NOT trigger any portfolio action or position change. |

#### RF-02-02: Competitive Moat Erosion

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-02-02 |
| **block_id** | SAI-BLK-02 |
| **condition** | Evidence of sustained competitive advantage erosion — declining market share, pricing power deterioration, loss of proprietary technology advantage, or regulatory elimination of barriers to entry |
| **required_evidence** | Market share declining for 4+ consecutive quarters; OR gross margin compression coincident with new competitor entry; OR loss of patent/regulatory exclusivity within 18 months; OR management commentary acknowledging competitive position deterioration |
| **temporal_persistence** | Sustained 4+ consecutive quarters or confirmed structural change |
| **severity** | elevated |
| **provenance_requirement** | Market share data, competitive landscape filings, patent expiration schedules, regulatory filings, management commentary, industry reports |
| **non_action_statement** | This flag indicates diagnostic concern about long-term business model durability requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.3 SAI-BLK-03: Revenue Quality (Operational)

#### RF-03-01: Organic Growth Negative While Total Growth Positive

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-03-01 |
| **block_id** | SAI-BLK-03 |
| **condition** | Organic revenue growth is negative while total reported revenue growth is positive, indicating that growth is entirely acquisition-driven and the core business is contracting |
| **required_evidence** | Reported total revenue growth positive (>0%); AND organic revenue growth (excluding acquisitions, currency, divestitures) negative; AND this divergence present in reported segment data or management disclosure |
| **temporal_persistence** | 2+ consecutive quarters showing the divergence |
| **severity** | elevated |
| **provenance_requirement** | Quarterly filings with organic/inorganic revenue breakdown, M&A disclosures, management commentary on organic growth, currency impact disclosures |
| **non_action_statement** | This flag indicates a diagnostic concern about revenue quality requiring investigation into acquisition dependency. It does NOT trigger any portfolio action or position change. |

#### RF-03-02: ARR Growth Decelerating

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-03-02 |
| **block_id** | SAI-BLK-03 |
| **condition** | Annual Recurring Revenue (ARR) growth rate is decelerating quarter-over-quarter for SaaS/subscription businesses, indicating demand saturation or competitive pressure on the recurring revenue base |
| **required_evidence** | ARR growth rate declining for 3+ consecutive quarters; AND net revenue retention declining or flat during the same period; AND the deceleration is not explained by deliberate strategic shift (e.g., moving upmarket to larger deals with longer cycles) |
| **temporal_persistence** | 3+ consecutive quarters of deceleration |
| **severity** | elevated |
| **provenance_requirement** | ARR/MRR disclosures from quarterly filings, net revenue retention metrics, management guidance commentary, earnings call transcripts explaining trends |
| **non_action_statement** | This flag indicates a diagnostic concern about recurring revenue momentum requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.4 SAI-BLK-04: Demand/Pipeline (Operational)

#### RF-04-01: Book-to-Bill Sustained Below 1.0

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-04-01 |
| **block_id** | SAI-BLK-04 |
| **condition** | Book-to-bill ratio sustained below 1.0, indicating that new orders are consistently below current revenue run rate — the company is depleting its backlog without replenishment |
| **required_evidence** | Book-to-bill ratio below 1.0 for 3+ consecutive quarters; AND absolute backlog declining; AND management has not disclosed a structural reason (e.g., deliberate shift from long-term to short-cycle contracts) |
| **temporal_persistence** | 3+ consecutive quarters below 1.0 |
| **severity** | elevated |
| **provenance_requirement** | Order intake/booking disclosures, backlog/RPO filings, revenue recognition schedule, management commentary on demand trends |
| **non_action_statement** | This flag indicates a diagnostic concern about future demand visibility requiring investigation. It does NOT trigger any portfolio action or position change. |

#### RF-04-02: Backlog Declining While Revenue Maintained

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-04-02 |
| **block_id** | SAI-BLK-04 |
| **condition** | Backlog/RPO is declining while current-period revenue remains stable or growing, indicating the company is consuming its demand cushion — future revenue visibility is deteriorating even as current performance appears stable |
| **required_evidence** | Backlog or RPO declining >10% year-over-year; AND current-quarter revenue flat or growing; AND remaining performance obligation short-term proportion increasing (front-loading) |
| **temporal_persistence** | 2+ consecutive quarters showing the pattern |
| **severity** | critical |
| **provenance_requirement** | RPO disclosures from quarterly filings, backlog trend data, revenue recognition schedules, ASC 606 disclosures |
| **non_action_statement** | This flag demands urgent review of demand pipeline sustainability. It does NOT trigger any portfolio action or position change. |

---

### 5.5 SAI-BLK-05: Margin Quality (Operational)

#### RF-05-01: Gross Margin Compression Exceeding 200bps

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-05-01 |
| **block_id** | SAI-BLK-05 |
| **condition** | Gross margin has compressed by more than 200 basis points year-over-year without a disclosed structural reason (e.g., deliberate mix shift, new low-margin segment launch) |
| **required_evidence** | Gross margin declined >200bps YoY; AND the compression is not attributable to a disclosed strategic decision; AND input cost increases or pricing pressure are evident from filings or management commentary |
| **temporal_persistence** | 2+ consecutive quarters showing compression trend |
| **severity** | elevated |
| **provenance_requirement** | Quarterly income statements, cost of goods sold breakdown, management commentary on margin drivers, segment margin disclosures |
| **non_action_statement** | This flag indicates a diagnostic concern about margin durability requiring investigation into structural versus transient causes. It does NOT trigger any portfolio action or position change. |

#### RF-05-02: Operating Leverage Negative

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-05-02 |
| **block_id** | SAI-BLK-05 |
| **condition** | Operating expenses growing faster than revenue for a sustained period, indicating negative operating leverage — the company cannot translate revenue growth into profit growth |
| **required_evidence** | Operating expense growth exceeding revenue growth for 3+ consecutive quarters; AND operating margin declining; AND the gap is not attributable to disclosed one-time investments with clear payback timeline |
| **temporal_persistence** | 3+ consecutive quarters of negative operating leverage |
| **severity** | elevated |
| **provenance_requirement** | Quarterly income statements, operating expense breakdown (SGA, R&D, other), management commentary on investment plans, operating margin trajectory |
| **non_action_statement** | This flag indicates a diagnostic concern about cost structure scalability requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.6 SAI-BLK-06: Cashflow Quality (Operational)

#### RF-06-01: FCF Conversion Below 50% for 3 Quarters

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-06-01 |
| **block_id** | SAI-BLK-06 |
| **condition** | Free cash flow conversion ratio (FCF/Net Income or FCF/EBITDA) persistently below 50%, indicating that reported earnings are not translating into actual cash generation |
| **required_evidence** | FCF/Net Income or FCF/EBITDA below 50% for 3+ consecutive quarters; AND working capital changes or capex intensity are not fully explained by disclosed growth investments with clear payback periods |
| **temporal_persistence** | 3+ consecutive quarters below the threshold |
| **severity** | elevated |
| **provenance_requirement** | Cash flow statements, capex disclosures, working capital breakdowns, management commentary on cash conversion, reconciliation of net income to operating cash flow |
| **non_action_statement** | This flag indicates a diagnostic concern about earnings quality and cash generation requiring investigation. It does NOT trigger any portfolio action or position change. |

#### RF-06-02: Negative FCF Despite Positive EBITDA

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-06-02 |
| **block_id** | SAI-BLK-06 |
| **condition** | Free cash flow is negative while EBITDA is positive, indicating a structural gap between accounting profitability and actual cash generation — potentially due to high capex, working capital consumption, or hidden cash outflows |
| **required_evidence** | EBITDA positive; AND FCF negative (operating cash flow minus capex); AND the divergence is not explained by a disclosed, time-limited capex cycle with clear visibility into normalization |
| **temporal_persistence** | 2+ consecutive quarters showing the divergence |
| **severity** | critical |
| **provenance_requirement** | Income statement (EBITDA), cash flow statement (OCF, capex, FCF), capex guidance, working capital disclosures, management commentary on cash flow drivers |
| **non_action_statement** | This flag demands urgent review of the structural gap between reported profitability and cash generation. It does NOT trigger any portfolio action or position change. |


---

### 5.7 SAI-BLK-07: Balance Sheet Quality (Financial Stability)

#### RF-07-01: Material Maturity Wall Within 18 Months

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-07-01 |
| **block_id** | SAI-BLK-07 |
| **condition** | A material portion of total debt (>25%) matures within 18 months without evidence of committed refinancing, indicating acute refinancing risk |
| **required_evidence** | Debt maturity schedule showing >25% of total debt due within 18 months; AND no disclosed committed credit facility or refinancing agreement covering the maturing amount; AND current credit market conditions or company-specific credit indicators suggest refinancing may not be straightforward |
| **temporal_persistence** | Single observation sufficient given the acute nature of maturity risk — verified against latest filing |
| **severity** | critical |
| **provenance_requirement** | Debt maturity schedule from annual/quarterly filings, credit facility disclosures, bond prospectus terms, management commentary on refinancing plans |
| **non_action_statement** | This flag demands urgent review of refinancing risk and liquidity adequacy. It does NOT trigger any portfolio action or position change. |

#### RF-07-02: Goodwill Exceeding 100% of Tangible Equity

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-07-02 |
| **block_id** | SAI-BLK-07 |
| **condition** | Goodwill and intangible assets exceed 100% of tangible equity, indicating the balance sheet is heavily dependent on non-impaired goodwill assumptions — a single large impairment could eliminate equity |
| **required_evidence** | Goodwill + intangible assets > tangible equity (total equity minus goodwill and intangibles); AND no recent impairment testing disclosed; OR impairment testing assumptions are materially optimistic relative to current business trajectory |
| **temporal_persistence** | Present in latest annual filing — sustained condition |
| **severity** | elevated |
| **provenance_requirement** | Balance sheet data, goodwill/intangibles breakdown, impairment testing disclosures (IAS 36 / ASC 350), acquisition history, CGU/reporting unit performance |
| **non_action_statement** | This flag indicates a diagnostic concern about balance sheet fragility requiring investigation into impairment risk. It does NOT trigger any portfolio action or position change. |

---

### 5.8 SAI-BLK-08: Credit/Solvency Risk (Financial Stability)

#### RF-08-01: Net Debt/EBITDA Exceeds 4x

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-08-01 |
| **block_id** | SAI-BLK-08 |
| **condition** | Net debt to EBITDA ratio exceeds 4.0x, indicating high financial leverage that constrains operational flexibility and increases vulnerability to earnings volatility or refinancing difficulty |
| **required_evidence** | Net debt / LTM EBITDA > 4.0x based on reported figures; AND the elevated leverage is not attributable to a recently closed transformative acquisition with disclosed deleveraging plan and timeline |
| **temporal_persistence** | 2+ consecutive quarters above the threshold |
| **severity** | critical |
| **provenance_requirement** | Balance sheet (gross debt, cash), income statement (EBITDA), management leverage targets, covenant disclosures, rating agency commentary |
| **non_action_statement** | This flag demands urgent review of leverage sustainability and deleveraging capacity. It does NOT trigger any portfolio action or position change. |

#### RF-08-02: Interest Coverage Below 2x

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-08-02 |
| **block_id** | SAI-BLK-08 |
| **condition** | Interest coverage ratio (EBIT/Interest Expense) is below 2.0x, indicating that operating earnings barely cover debt service obligations — limited margin of safety for earnings decline |
| **required_evidence** | EBIT / Interest Expense < 2.0x for the latest reporting period; AND the deterioration is not attributable to a one-time non-cash charge that depressed EBIT temporarily |
| **temporal_persistence** | 2+ consecutive quarters below the threshold |
| **severity** | critical |
| **provenance_requirement** | Income statement (EBIT, interest expense), debt disclosures, interest rate exposure, management commentary on debt service capacity |
| **non_action_statement** | This flag demands urgent review of debt service capacity and solvency trajectory. It does NOT trigger any portfolio action or position change. |

---

### 5.9 SAI-BLK-09: Hidden Liabilities (Financial Stability)

#### RF-09-01: Off-Balance-Sheet Obligations Exceeding 30% of Reported Debt

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-09-01 |
| **block_id** | SAI-BLK-09 |
| **condition** | Off-balance-sheet obligations (operating leases not capitalized, purchase commitments, guarantees, unconsolidated JV debt) exceed 30% of reported on-balance-sheet debt, indicating materially understated financial obligations |
| **required_evidence** | Sum of off-balance-sheet items (non-cancellable purchase obligations, guarantees, unconsolidated debt, other commitments) > 30% of reported debt; AND disclosures from notes to financial statements, commitment schedules, or related party transactions |
| **temporal_persistence** | Present in latest annual filing — structural condition |
| **severity** | critical |
| **provenance_requirement** | Notes to financial statements, commitment and contingency disclosures, operating lease schedules, guarantee disclosures, unconsolidated entity disclosures |
| **non_action_statement** | This flag demands urgent review of total financial obligation burden. It does NOT trigger any portfolio action or position change. |

#### RF-09-02: Aggregate Contingent Liabilities Exceeding 15% of Equity

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-09-02 |
| **block_id** | SAI-BLK-09 |
| **condition** | Total disclosed contingent liabilities (litigation, regulatory proceedings, environmental obligations, warranty provisions) exceed 15% of total equity, indicating material crystallization risk |
| **required_evidence** | Aggregate contingent liabilities disclosed in notes to financial statements > 15% of total equity; AND at least one contingency is classified as "reasonably possible" or higher probability of crystallization |
| **temporal_persistence** | Present in latest annual filing — assessed against most recent disclosure |
| **severity** | elevated |
| **provenance_requirement** | Contingent liability disclosures (IAS 37 / ASC 450), litigation disclosures, environmental provision notes, warranty obligation schedules |
| **non_action_statement** | This flag indicates a diagnostic concern about potential liability crystallization requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.10 SAI-BLK-10: Pension Obligations (Financial Stability)

#### RF-10-01: Pension Underfunding Exceeding 20% of Market Cap

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-10-01 |
| **block_id** | SAI-BLK-10 |
| **condition** | Net pension deficit (defined benefit obligation minus plan assets) exceeds 20% of current market capitalization, indicating the pension obligation represents a material economic burden relative to the company's total value |
| **required_evidence** | Defined benefit obligation minus fair value of plan assets > 20% of market capitalization; AND the funding status is based on the latest actuarial valuation; AND no committed plan to close the deficit within a defined timeline |
| **temporal_persistence** | Present in latest annual actuarial valuation — assessed annually |
| **severity** | critical |
| **provenance_requirement** | Pension disclosures (IAS 19 / ASC 715), actuarial valuation reports, plan asset allocation, contribution schedules, market capitalization data |
| **non_action_statement** | This flag demands urgent review of pension obligation impact on enterprise value. It does NOT trigger any portfolio action or position change. |

#### RF-10-02: Discount Rate Assumption Exceeding Peer Median by 100bps

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-10-02 |
| **block_id** | SAI-BLK-10 |
| **condition** | Pension discount rate assumption exceeds same-jurisdiction peer median by more than 100 basis points, indicating potentially optimistic actuarial assumptions that understate the true obligation |
| **required_evidence** | Company discount rate > peer median + 100bps for same jurisdiction and currency; AND no disclosed justification for the deviation (e.g., materially different duration profile); AND the higher discount rate results in materially lower reported obligation |
| **temporal_persistence** | Present in latest actuarial disclosure — single observation sufficient given annual cadence |
| **severity** | elevated |
| **provenance_requirement** | Pension discount rate disclosures, peer company pension disclosures for same jurisdiction, actuarial assumption notes, sensitivity analysis disclosures |
| **non_action_statement** | This flag indicates a diagnostic concern about actuarial assumption credibility requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.11 SAI-BLK-11: Working Capital (Operational)

#### RF-11-01: Inventory Build Exceeding Revenue Growth

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-11-01 |
| **block_id** | SAI-BLK-11 |
| **condition** | Inventory growth significantly exceeds revenue growth, indicating potential demand weakness, obsolescence risk, or channel stuffing — inventory is building without proportionate demand |
| **required_evidence** | Inventory growth (YoY) exceeding revenue growth (YoY) by more than 10 percentage points; AND inventory days outstanding increasing; AND management has not disclosed a deliberate build-ahead strategy with confirmed orders |
| **temporal_persistence** | 2+ consecutive quarters showing the divergence |
| **severity** | elevated |
| **provenance_requirement** | Balance sheet inventory data, revenue data, inventory days outstanding calculation, management commentary on inventory strategy, segment inventory breakdowns |
| **non_action_statement** | This flag indicates a diagnostic concern about demand-supply alignment requiring investigation. It does NOT trigger any portfolio action or position change. |

#### RF-11-02: DSO Increasing by More Than 10 Days Over 4 Quarters

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-11-02 |
| **block_id** | SAI-BLK-11 |
| **condition** | Days Sales Outstanding (DSO) has increased by more than 10 days over 4 quarters, indicating deteriorating collection efficiency, potential revenue quality issues, or customer financial stress |
| **required_evidence** | DSO increased by >10 days comparing current quarter to same quarter prior year; AND the increase is not explained by a disclosed change in payment terms or customer mix shift to longer-cycle customers |
| **temporal_persistence** | Trend observed over 4 consecutive quarters |
| **severity** | elevated |
| **provenance_requirement** | Accounts receivable data, revenue data, DSO calculation, aging schedule disclosures, management commentary on collection trends, customer payment term disclosures |
| **non_action_statement** | This flag indicates a diagnostic concern about receivable quality and collection efficiency requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.12 SAI-BLK-12: Customer Concentration (Risk)

#### RF-12-01: Single Customer Exceeding 30% of Revenue

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-12-01 |
| **block_id** | SAI-BLK-12 |
| **condition** | A single customer accounts for more than 30% of total revenue, creating critical dependency where loss of that customer would cause immediate, material revenue decline |
| **required_evidence** | Disclosed customer concentration showing one customer > 30% of revenue; OR regulatory filing (10-K) major customer disclosure exceeding this threshold; AND no multi-year contract providing forward visibility beyond 12 months |
| **temporal_persistence** | Present in latest annual filing — structural condition |
| **severity** | critical |
| **provenance_requirement** | Major customer disclosures from annual filings, segment revenue breakdowns, contract duration disclosures, related party transaction notes |
| **non_action_statement** | This flag demands urgent review of customer dependency risk and contract security. It does NOT trigger any portfolio action or position change. |

#### RF-12-02: Top-5 Customers Exceeding 70% with Short Contracts

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-12-02 |
| **block_id** | SAI-BLK-12 |
| **condition** | Top 5 customers collectively account for more than 70% of revenue AND average contract duration with these customers is less than 2 years, indicating concentrated dependency with limited forward visibility |
| **required_evidence** | Customer concentration data showing top-5 > 70% of revenue; AND contract duration/renewal evidence showing average remaining term < 2 years; OR absence of long-term contractual commitments disclosed |
| **temporal_persistence** | Present in latest annual filing — structural condition |
| **severity** | elevated |
| **provenance_requirement** | Customer concentration disclosures, contract term/duration notes, backlog composition by customer, customer loss history |
| **non_action_statement** | This flag indicates a diagnostic concern about revenue security and customer diversification requiring investigation. It does NOT trigger any portfolio action or position change. |


---

### 5.13 SAI-BLK-13: Supply Chain Stability (Risk)

#### RF-13-01: Single-Source Dependency for Critical Input

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-13-01 |
| **block_id** | SAI-BLK-13 |
| **condition** | The company depends on a single supplier for a critical input material, component, or service with no qualified alternative source — loss of this supplier would cause material operational disruption |
| **required_evidence** | Disclosed single-source supplier dependency in filings (risk factors, supply chain disclosures); OR evidence from industry analysis showing sole-source dependency for a critical input; AND no disclosed qualification of alternative suppliers |
| **temporal_persistence** | Present in latest annual filing — structural condition |
| **severity** | critical |
| **provenance_requirement** | Risk factor disclosures, supply chain/procurement disclosures, management commentary on supplier diversification, industry supply chain analysis |
| **non_action_statement** | This flag demands urgent review of supply chain fragility and disruption exposure. It does NOT trigger any portfolio action or position change. |

#### RF-13-02: Geographic Concentration in High-Risk Jurisdiction

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-13-02 |
| **block_id** | SAI-BLK-13 |
| **condition** | Critical supply chain operations (manufacturing, sourcing, logistics) are concentrated in a jurisdiction with elevated geopolitical, regulatory, or natural disaster risk without disclosed diversification plans |
| **required_evidence** | >50% of critical supply chain capacity located in a single high-risk jurisdiction (identified by geopolitical instability, trade restriction risk, or natural disaster frequency); AND no disclosed mitigation or diversification strategy; AND the concentration is disclosed in risk factors or operational descriptions |
| **temporal_persistence** | Present in latest annual filing — structural condition |
| **severity** | elevated |
| **provenance_requirement** | Manufacturing/operations disclosures, geographic revenue/asset breakdowns, risk factor disclosures, geopolitical risk assessments from filings |
| **non_action_statement** | This flag indicates a diagnostic concern about geographic supply chain risk requiring investigation into mitigation strategies. It does NOT trigger any portfolio action or position change. |

---

### 5.14 SAI-BLK-14: Pricing Power (Operational)

#### RF-14-01: Volume Decline Following Price Increase

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-14-01 |
| **block_id** | SAI-BLK-14 |
| **condition** | Unit volumes declined materially following a price increase, indicating limited pricing power — customers are price-sensitive and the company cannot maintain volume while raising prices |
| **required_evidence** | Disclosed or calculable price increase (average selling price up); AND unit volume declined in the same or immediately following period; AND management commentary acknowledging volume-price tradeoff or customer pushback |
| **temporal_persistence** | Observable in 2+ consecutive quarters following price action |
| **severity** | elevated |
| **provenance_requirement** | Revenue decomposition (price vs. volume), unit volume disclosures, management commentary on pricing strategy, competitive pricing data |
| **non_action_statement** | This flag indicates a diagnostic concern about pricing power sustainability requiring investigation. It does NOT trigger any portfolio action or position change. |

#### RF-14-02: Cost Pass-Through Failure

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-14-02 |
| **block_id** | SAI-BLK-14 |
| **condition** | Input costs have increased materially but the company has failed to pass through cost increases to customers, resulting in margin compression — indicating weak pricing power in the value chain |
| **required_evidence** | Input cost inflation evident (COGS/revenue ratio increasing); AND pricing actions insufficient to offset (gross margin declining); AND peer companies in the same industry have demonstrated better pass-through ability during the same period |
| **temporal_persistence** | 2+ consecutive quarters showing pass-through failure |
| **severity** | elevated |
| **provenance_requirement** | Cost of goods sold trends, gross margin trajectory, management commentary on input costs, peer margin comparison, industry cost inflation data |
| **non_action_statement** | This flag indicates a diagnostic concern about value chain positioning and pricing ability requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.15 SAI-BLK-15: Earnings Quality (Earnings)

#### RF-15-01: Persistent GAAP-to-Adjusted Gap Exceeding 30% for 4+ Quarters

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-15-01 |
| **block_id** | SAI-BLK-15 |
| **condition** | The gap between GAAP earnings and management-adjusted earnings persistently exceeds 30%, indicating that reported "adjusted" results materially diverge from accounting reality — recurring adjustments may be masking true profitability |
| **required_evidence** | (Adjusted EPS - GAAP EPS) / GAAP EPS > 30% for 4+ consecutive quarters; AND adjustments include items that recur each quarter (stock-based compensation, restructuring, acquisition costs, amortization); AND the nature of exclusions is not declining over time |
| **temporal_persistence** | 4+ consecutive quarters with the gap exceeding the threshold |
| **severity** | critical |
| **provenance_requirement** | GAAP income statements, non-GAAP reconciliation tables, management earnings presentations, SEC/regulatory comment letters on non-GAAP metrics |
| **non_action_statement** | This flag demands urgent review of earnings quality and adjustment credibility. It does NOT trigger any portfolio action or position change. |

#### RF-15-02: Accrual Ratio Rising While Cash Conversion Declining

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-15-02 |
| **block_id** | SAI-BLK-15 |
| **condition** | Accrual ratio (accruals/average net operating assets) is rising while cash conversion (OCF/Net Income) is declining simultaneously, indicating potential earnings manipulation or aggressive revenue recognition |
| **required_evidence** | Accrual ratio trending upward for 3+ consecutive quarters; AND cash conversion ratio (OCF/Net Income) declining over the same period; AND the divergence is not explained by a disclosed working capital cycle shift or capex ramp |
| **temporal_persistence** | 3+ consecutive quarters showing the dual deterioration |
| **severity** | elevated |
| **provenance_requirement** | Income statements, cash flow statements, balance sheet working capital items, accrual ratio calculation inputs, management cash flow commentary |
| **non_action_statement** | This flag indicates a diagnostic concern about earnings sustainability and accounting quality requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.16 SAI-BLK-16: Guidance/Estimate Revisions (Earnings)

#### RF-16-01: Guidance Missed 3+ Consecutive Quarters

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-16-01 |
| **block_id** | SAI-BLK-16 |
| **condition** | Management has missed its own guidance (revenue or EPS below guided range) for 3 or more consecutive quarters, indicating systematic guidance credibility erosion |
| **required_evidence** | Actual reported revenue or EPS below the low end of management guidance for 3+ consecutive quarters; AND the misses are not attributable to a single disclosed extraordinary event; AND management has not formally reset expectations with credible rationale |
| **temporal_persistence** | 3+ consecutive quarters of guidance misses |
| **severity** | elevated |
| **provenance_requirement** | Management guidance from earnings releases/presentations, actual reported results, earnings call transcripts explaining misses, analyst consensus relative to guidance |
| **non_action_statement** | This flag indicates a diagnostic concern about management forecasting credibility requiring investigation. It does NOT trigger any portfolio action or position change. |

#### RF-16-02: Negative Estimate Revision Trend Accelerating

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-16-02 |
| **block_id** | SAI-BLK-16 |
| **condition** | Analyst consensus estimate revisions are negative AND accelerating in magnitude — estimates are being cut with increasing severity over successive revision periods |
| **required_evidence** | Consensus EPS or revenue estimates revised downward for 3+ consecutive months; AND the magnitude of cuts is increasing (e.g., -2% month 1, -4% month 2, -7% month 3); AND revision breadth is widening (increasing proportion of analysts cutting) |
| **temporal_persistence** | 3+ consecutive months of accelerating negative revisions |
| **severity** | elevated |
| **provenance_requirement** | Consensus estimate data, revision history (3-month and 6-month trends), analyst count and direction, earnings revision breadth metrics |
| **non_action_statement** | This flag indicates a diagnostic concern about deteriorating earnings expectations requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.17 SAI-BLK-17: Valuation Context (Valuation)

#### RF-17-01: Multiple Exceeding 2 Standard Deviations Above Historical Median

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-17-01 |
| **block_id** | SAI-BLK-17 |
| **condition** | Primary valuation multiple (P/E or EV/EBITDA) exceeds 2 standard deviations above its own 5-year historical median, indicating the market is pricing significantly above the asset's normal valuation range |
| **required_evidence** | Current multiple > historical 5-year median + 2 standard deviations; AND the expansion is not fully explained by a structural business model improvement (e.g., successful transition to higher-quality recurring revenue); AND peer multiples have not expanded proportionally |
| **temporal_persistence** | Sustained for 20+ trading days above the threshold |
| **severity** | elevated |
| **provenance_requirement** | Historical multiple data (5-year), current multiple calculation, peer multiple comparison, earnings/cash flow basis for multiple, business model change disclosures |
| **non_action_statement** | This flag indicates a diagnostic concern about valuation context requiring investigation into whether fundamental improvement justifies the premium. It does NOT trigger any portfolio action or position change. |

#### RF-17-02: FCF Yield Below Risk-Free Rate

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-17-02 |
| **block_id** | SAI-BLK-17 |
| **condition** | Free cash flow yield (FCF/Market Cap) is below the prevailing risk-free rate (10-year government bond yield), indicating the market assigns virtually no risk premium to equity cash flows — extreme valuation relative to riskless alternatives |
| **required_evidence** | FCF yield (trailing or NTM) < 10-year government bond yield for the relevant currency; AND FCF is positive (not a meaningless ratio from negative FCF); AND the condition persists beyond short-term market volatility |
| **temporal_persistence** | Sustained for 30+ trading days |
| **severity** | elevated |
| **provenance_requirement** | FCF data from cash flow statements, market capitalization, 10-year government bond yield for relevant currency, peer FCF yield comparison |
| **non_action_statement** | This flag indicates a diagnostic concern about valuation extremity requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.18 SAI-BLK-18: Value Trap Guard (Valuation)

#### RF-18-01: Low Multiple with Declining FCF and Rising Leverage

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-18-01 |
| **block_id** | SAI-BLK-18 |
| **condition** | Valuation multiple is low (appears cheap) BUT free cash flow is declining AND leverage is rising simultaneously — classic value trap pattern where cheapness reflects fundamental deterioration, not opportunity |
| **required_evidence** | Primary multiple (P/E or EV/EBITDA) below sector median; AND FCF declining for 2+ consecutive quarters; AND net debt/EBITDA increasing over the same period; AND no disclosed turnaround plan with credible evidence of execution |
| **temporal_persistence** | 2+ consecutive quarters showing the triple-deterioration pattern |
| **severity** | critical |
| **provenance_requirement** | Valuation multiple data, FCF trend, leverage trend, sector median multiple, management turnaround commentary, capital allocation disclosures |
| **non_action_statement** | This flag demands urgent review — apparent cheapness may mask structural impairment. It does NOT trigger any portfolio action or position change. |

#### RF-18-02: High Dividend Yield from Price Decline with Deteriorating Coverage

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-18-02 |
| **block_id** | SAI-BLK-18 |
| **condition** | Dividend yield appears attractive BUT is elevated primarily due to price decline (not dividend growth) AND dividend coverage (FCF/Dividends or EPS/DPS) is deteriorating — suggesting the dividend may not be sustainable |
| **required_evidence** | Dividend yield above sector median; AND yield increase driven primarily by price decline (>60% of yield expansion from price, not dividend growth); AND dividend coverage ratio declining for 2+ consecutive quarters; AND FCF payout ratio approaching or exceeding 100% |
| **temporal_persistence** | 2+ consecutive quarters showing deteriorating coverage |
| **severity** | critical |
| **provenance_requirement** | Dividend payment history, price history, FCF data, EPS data, payout ratio calculations, management dividend policy statements, peer dividend yield comparison |
| **non_action_statement** | This flag demands urgent review of dividend sustainability. It does NOT trigger any portfolio action or position change. |


---

### 5.19 SAI-BLK-19: Relative Strength (Market Position)

#### RF-19-01: Persistent Underperformance Despite Sector Tailwind

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-19-01 |
| **block_id** | SAI-BLK-19 |
| **condition** | The asset persistently underperforms its sector index despite the sector experiencing positive momentum — indicating asset-specific weakness that is masked or offset by sector-level strength |
| **required_evidence** | Asset total return underperforming sector index by >10% over 6 months; AND sector index performance is positive over the same period; AND underperformance is not explained by a disclosed, time-limited event (e.g., one-time regulatory fine) |
| **temporal_persistence** | Sustained 6+ months of relative underperformance |
| **severity** | elevated |
| **provenance_requirement** | Asset price performance data, sector index performance, relative return calculation, event/news analysis for disclosed explanations |
| **non_action_statement** | This flag indicates a diagnostic concern about asset-specific weakness requiring investigation into fundamental drivers. It does NOT trigger any portfolio action or position change. |

#### RF-19-02: Maximum Drawdown Exceeding 2x Sector Drawdown

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-19-02 |
| **block_id** | SAI-BLK-19 |
| **condition** | The asset's maximum drawdown from peak exceeds 2x the sector's maximum drawdown over the same period, indicating disproportionate downside exposure that is not shared by sector peers |
| **required_evidence** | Asset maximum drawdown > 2x sector maximum drawdown measured over the same time window (minimum 3-month lookback); AND the excess drawdown is not attributable to a disclosed one-time event that has been resolved |
| **temporal_persistence** | Drawdown sustained for 20+ trading days without meaningful recovery |
| **severity** | elevated |
| **provenance_requirement** | Asset price data (peak-to-trough), sector index data, drawdown calculations, event analysis for disclosed explanations |
| **non_action_statement** | This flag indicates a diagnostic concern about asymmetric downside risk requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.20 SAI-BLK-20: Benchmark/Sector/Peer Correlation (Market Position)

#### RF-20-01: Correlation Regime Shift Exceeding 0.3 Over 60 Days

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-20-01 |
| **block_id** | SAI-BLK-20 |
| **condition** | Rolling correlation with primary benchmark has shifted by more than 0.3 (absolute change) over 60 trading days, indicating a fundamental change in co-movement regime — the asset's behavior relative to the market has changed materially |
| **required_evidence** | 60-day rolling correlation with benchmark changed by >0.3 (up or down) compared to the prior 60-day period; AND the shift is not attributable to a single extreme event day that distorts the calculation |
| **temporal_persistence** | Shift sustained for 20+ trading days after initial detection |
| **severity** | informational |
| **provenance_requirement** | Daily return data, rolling correlation calculations, benchmark return data, event calendar for potential explanatory events |
| **non_action_statement** | This flag indicates a notable change in correlation structure worth monitoring. It does NOT trigger any portfolio action or position change. |

#### RF-20-02: Asymmetric Beta — Upside Participation Ratio Below 0.7

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-20-02 |
| **block_id** | SAI-BLK-20 |
| **condition** | The asset demonstrates asymmetric beta — it captures less than 70% of benchmark upside moves while capturing a disproportionately larger share of downside moves, indicating poor risk-reward characteristics |
| **required_evidence** | Upside capture ratio < 0.7 (asset up-day returns / benchmark up-day returns); AND downside capture ratio > 1.0 (asset down-day returns / benchmark down-day returns); AND measured over minimum 60 trading days |
| **temporal_persistence** | Pattern sustained over 60+ trading days |
| **severity** | elevated |
| **provenance_requirement** | Daily return data, up-market/down-market day classification, capture ratio calculations, benchmark daily returns |
| **non_action_statement** | This flag indicates a diagnostic concern about asymmetric market participation requiring investigation. It does NOT trigger any portfolio action or position change. |

---

### 5.21 SAI-BLK-21: Peer Comparison (Market Position)

#### RF-21-01: Fundamental Divergence Exceeding 2 Standard Deviations from Peer Median

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-21-01 |
| **block_id** | SAI-BLK-21 |
| **condition** | A key fundamental metric (margin, growth, leverage, or return on capital) diverges by more than 2 standard deviations from the defined peer group median — indicating the asset is an outlier requiring investigation into whether divergence reflects strength or weakness |
| **required_evidence** | At least one key fundamental metric > 2 standard deviations from peer median; AND peer group is defined and contains ≥4 comparable companies; AND the divergence is persistent (not single-quarter anomaly) |
| **temporal_persistence** | 2+ consecutive quarters showing the divergence |
| **severity** | elevated |
| **provenance_requirement** | Peer group definition, fundamental metric data for asset and all peers, peer median and standard deviation calculation, peer group source documentation |
| **non_action_statement** | This flag indicates a diagnostic concern about peer-relative positioning requiring investigation into divergence drivers. It does NOT trigger any portfolio action or position change. |

#### RF-21-02: Valuation Premium Exceeding 50% Above Peers Without Fundamental Justification

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-21-02 |
| **block_id** | SAI-BLK-21 |
| **condition** | Primary valuation multiple exceeds the peer group median by more than 50% without corresponding fundamental superiority in growth, margins, or returns — indicating the market may be assigning a premium not supported by relative fundamentals |
| **required_evidence** | Asset multiple > 1.5x peer median multiple; AND asset growth rate, margins, and ROIC are not proportionally superior to peers; AND no unique structural advantage (IP, market position, regulatory moat) is disclosed that would justify the premium |
| **temporal_persistence** | Sustained for 30+ trading days |
| **severity** | informational |
| **provenance_requirement** | Peer group valuation multiples, peer group fundamental metrics (growth, margins, ROIC), premium calculation, peer group composition and source |
| **non_action_statement** | This flag indicates a notable valuation premium relative to peers worth monitoring. It does NOT trigger any portfolio action or position change. |

---

### 5.22 SAI-BLK-22: Company Outlook (Outlook)

#### RF-22-01: Management Guidance Credibility Collapse

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-22-01 |
| **block_id** | SAI-BLK-22 |
| **condition** | Management has demonstrated a pattern of issuing guidance that is not credible — combination of repeated guidance misses, guidance withdrawals, or material guidance revisions that collectively indicate forward-looking statements cannot be relied upon for diagnostic purposes |
| **required_evidence** | Guidance missed in 3+ of last 6 quarters; OR guidance withdrawn/suspended without replacement; OR guidance materially revised downward mid-quarter on 2+ occasions; AND no external force majeure event explains the pattern |
| **temporal_persistence** | Pattern observed over 6+ quarters of guidance history |
| **severity** | elevated |
| **provenance_requirement** | Guidance history (issued vs. actual), guidance withdrawal disclosures, mid-quarter revision history, earnings call transcripts, press releases |
| **non_action_statement** | This flag indicates a diagnostic concern about forward-looking statement reliability requiring investigation. It does NOT trigger any portfolio action or position change. |

#### RF-22-02: Strategic Pivot Without Execution Evidence

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-22-02 |
| **block_id** | SAI-BLK-22 |
| **condition** | Management has announced a significant strategic pivot (new market, new business model, major restructuring) but after 4+ quarters there is no measurable evidence of execution — the pivot exists as narrative only |
| **required_evidence** | Disclosed strategic pivot or transformation initiative; AND 4+ quarters elapsed since announcement; AND no measurable KPIs showing progress (revenue from new segment, cost savings realized, market entry evidence); AND management continues to reference the pivot without quantifiable milestones achieved |
| **temporal_persistence** | 4+ quarters since pivot announcement without execution evidence |
| **severity** | informational |
| **provenance_requirement** | Strategic pivot announcement (press releases, investor days), subsequent quarterly results, segment disclosures, management commentary on execution progress, KPI disclosures |
| **non_action_statement** | This flag indicates a notable gap between stated strategy and observable execution worth monitoring. It does NOT trigger any portfolio action or position change. |

---

### 5.23 SAI-BLK-23: Asset-Class Outlook (Outlook)

#### RF-23-01: Adverse Regulatory Development

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-23-01 |
| **block_id** | SAI-BLK-23 |
| **condition** | A material adverse regulatory development has been proposed or enacted that directly affects the asset's industry — potentially impacting revenue model, cost structure, or competitive dynamics at the sector level |
| **required_evidence** | Proposed or enacted regulation with direct impact on the asset's primary industry; AND regulatory impact is material (affects >10% of industry revenue or materially changes cost structure); AND regulatory timeline is within 24 months of implementation |
| **temporal_persistence** | From proposal/enactment date — single observation sufficient given regulatory significance |
| **severity** | elevated |
| **provenance_requirement** | Regulatory filings/proposals, industry impact assessments, company risk factor updates, management regulatory commentary, industry association responses |
| **non_action_statement** | This flag indicates a diagnostic concern about regulatory environment change requiring investigation into company-specific impact. It does NOT trigger any portfolio action or position change. |

#### RF-23-02: Industry Cycle Late-Stage Indicators

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-23-02 |
| **block_id** | SAI-BLK-23 |
| **condition** | Multiple indicators suggest the asset's industry is in late-cycle phase — capacity utilization at historical highs, margin peaks, aggressive M&A activity, and new entrant proliferation typically associated with cycle peaks |
| **required_evidence** | At least 3 of the following present: industry capacity utilization >90%; sector margins at/near 5-year highs; M&A activity elevated (deal volume >2x 5-year average); new market entrants/IPOs accelerating; customer inventory builds above normal levels |
| **temporal_persistence** | Multiple indicators present simultaneously for 2+ consecutive quarters |
| **severity** | informational |
| **provenance_requirement** | Industry data (capacity utilization, margins), M&A activity data, IPO/new entrant data, inventory channel checks, industry cycle analysis from filings |
| **non_action_statement** | This flag indicates notable industry cycle positioning worth monitoring for diagnostic context. It does NOT trigger any portfolio action or position change. |

---

### 5.24 SAI-BLK-24: Portfolio Fit (Portfolio Context)

#### RF-24-01: Concentration Contribution Breach Exceeding 15%

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-24-01 |
| **block_id** | SAI-BLK-24 |
| **condition** | The asset's contribution to portfolio-level concentration (sector, geographic, factor, or narrative dimension) exceeds 15% of total portfolio exposure in any single dimension — indicating the asset disproportionately drives portfolio-level concentration risk |
| **required_evidence** | Position contributes >15% to portfolio concentration in at least one dimension (sector weight, geographic exposure, factor loading, or narrative exposure); AND the concentration is not intentional and disclosed in portfolio mandate |
| **temporal_persistence** | Present for 10+ trading days |
| **severity** | elevated |
| **provenance_requirement** | Portfolio composition data, sector/geographic/factor exposure calculations, position weight data, portfolio mandate parameters |
| **non_action_statement** | This flag indicates a diagnostic concern about portfolio concentration contribution requiring review. It does NOT trigger any portfolio action, rebalancing, or position change. |

#### RF-24-02: Liquidity Mismatch — Position Exceeding 5 Days ADV

| Field | Value |
|-------|-------|
| **red_flag_id** | RF-24-02 |
| **block_id** | SAI-BLK-24 |
| **condition** | Current position size exceeds 5 days of average daily volume (ADV), indicating a material liquidity mismatch — the position cannot be adjusted within normal timeframes without potential market impact |
| **required_evidence** | Position size (shares or notional) > 5x 20-day average daily volume; AND no block-trade or secondary-market exit option is readily available; AND the ADV calculation uses recent and representative trading data |
| **temporal_persistence** | Present for 5+ trading days (allowing for temporary volume spikes) |
| **severity** | elevated |
| **provenance_requirement** | Position size data, 20-day ADV calculation, trading volume history, market microstructure data |
| **non_action_statement** | This flag indicates a diagnostic concern about position liquidity requiring review. It does NOT trigger any portfolio action, forced liquidation, or position change. |


---

## 6. Coverage Summary

### 6.1 Total Red Flag Count

| Metric | Value |
|--------|-------|
| Total red flags defined | 48 |
| Blocks covered | 24 / 24 (100%) |
| Minimum flags per block | 2 |
| Maximum flags per block | 2 |

### 6.2 Severity Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| informational | 5 | 10.4% |
| elevated | 31 | 64.6% |
| critical | 12 | 25.0% |

### 6.3 Informational Flags

| Flag ID | Block | Condition Summary |
|---------|-------|-------------------|
| RF-01-02 | Asset Identity | Sector classification conflict |
| RF-20-01 | Benchmark/Sector/Peer Correlation | Correlation regime shift >0.3 |
| RF-21-02 | Peer Comparison | Valuation premium >50% without justification |
| RF-22-02 | Company Outlook | Strategic pivot without execution evidence |
| RF-23-02 | Asset-Class Outlook | Industry cycle late-stage indicators |

### 6.4 Critical Flags

| Flag ID | Block | Condition Summary |
|---------|-------|-------------------|
| RF-04-02 | Demand/Pipeline | Backlog declining while revenue maintained |
| RF-06-02 | Cashflow Quality | Negative FCF despite positive EBITDA |
| RF-07-01 | Balance Sheet Quality | Material maturity wall within 18 months |
| RF-08-01 | Credit/Solvency Risk | Net debt/EBITDA exceeds 4x |
| RF-08-02 | Credit/Solvency Risk | Interest coverage below 2x |
| RF-09-01 | Hidden Liabilities | Off-balance-sheet obligations >30% of reported debt |
| RF-10-01 | Pension Obligations | Pension underfunding >20% of market cap |
| RF-12-01 | Customer Concentration | Single customer >30% of revenue |
| RF-13-01 | Supply Chain Stability | Single-source dependency for critical input |
| RF-15-01 | Earnings Quality | Persistent GAAP-to-adjusted gap >30% for 4+ quarters |
| RF-18-01 | Value Trap Guard | Low multiple with declining FCF and rising leverage |
| RF-18-02 | Value Trap Guard | High dividend yield from price decline with deteriorating coverage |

### 6.5 Coverage by Category

| Category | Blocks | Red Flags | Critical | Elevated | Informational |
|----------|--------|-----------|----------|----------|---------------|
| Foundation | 2 (BLK-01, BLK-02) | 4 | 0 | 3 | 1 |
| Operational | 6 (BLK-03, BLK-04, BLK-05, BLK-06, BLK-11, BLK-14) | 12 | 2 | 10 | 0 |
| Financial Stability | 4 (BLK-07, BLK-08, BLK-09, BLK-10) | 8 | 5 | 3 | 0 |
| Risk | 2 (BLK-12, BLK-13) | 4 | 2 | 2 | 0 |
| Earnings | 2 (BLK-15, BLK-16) | 4 | 1 | 3 | 0 |
| Valuation | 2 (BLK-17, BLK-18) | 4 | 2 | 2 | 0 |
| Market Position | 3 (BLK-19, BLK-20, BLK-21) | 6 | 0 | 4 | 2 |
| Outlook | 2 (BLK-22, BLK-23) | 4 | 0 | 2 | 2 |
| Portfolio Context | 1 (BLK-24) | 2 | 0 | 2 | 0 |

---

## 7. Boundary Statement

This red flag taxonomy is EXCLUSIVELY diagnostic. The following statements define its absolute boundaries:

### 7.1 What Red Flags ARE

- Evidence-based diagnostic conditions that identify elevated risk within a specific analysis block
- Categorical warnings that indicate the need for investigation, review, or monitoring
- Provenance-linked assertions backed by specific facts and signals
- Temporal conditions that persist over defined observation periods

### 7.2 What Red Flags ARE NOT

- Red flags are NOT numeric risk scores
- Red flags do NOT trigger automated actions
- Red flags do NOT map to buy/sell/hold decisions
- Red flags do NOT aggregate into composite risk ratings
- Red flags do NOT imply position size changes
- Red flags do NOT create portfolio rebalancing triggers
- Red flags do NOT rank assets against each other
- Red flags do NOT produce probabilities of default, loss, or gain
- Red flags are NOT weighted or prioritized algorithmically
- Red flags do NOT create "risk scores" by severity counting

### 7.3 Downstream Consumption Boundary

Downstream consumers (Portfolio Health Framework, future Scoring Layer, Reporting Layer) MAY consume red flags as inputs to their own processes. SAI does NOT control or prescribe how downstream consumers interpret red flags. The boundary is:

- SAI produces red flags → diagnostic output
- Downstream layers consume red flags → their decision, not SAI's
- SAI NEVER prescribes what action a red flag should trigger
- The gap between "condition identified" and "action taken" belongs entirely to downstream layers

---

## 8. Relationship to output_object_spec.md

Red flags appear in the SAI output object as field #6 (`red_flags`). The output object specification defines:

- Each entry contains: `flag_id` (RF-NN-XX format), `severity` (informational/elevated/critical), `evidence` (list of fact/signal references), `description` (evidence-based warning text)
- The `red_flags` list may be empty if no red flag conditions are detected for a given block/asset/evaluation cycle
- Red flags are part of the canonical output object — they are not a separate system

(See: output_object_spec.md, Section: 2 — Allowed Fields, Field #6)

This taxonomy defines WHAT red flags exist and WHAT conditions trigger them. The output object specification defines HOW red flags are represented in the output data structure.

---

## 9. Relationship to provenance_contract.md

Every red flag assertion requires provenance. When a red flag is asserted in an output object:

- The `evidence` field within the red flag must reference specific fact_ids and/or signal_ids
- Those referenced IDs must exist in the output object's `consumed_facts` and `consumed_signals` lists
- The provenance chain for the entire output object must include the evidence cited by each asserted flag
- A red flag without provenance (no cited evidence) is an invalid orphan assertion and MUST be rejected

(See: provenance_contract.md, Section: 2 — Provenance Chain Fields)
(See: provenance_contract.md, Section: 4 — Invalid Orphan Interpretation Rule)

The `provenance_requirement` field in each red flag definition (this document) specifies what type of evidence sources must be cited. The provenance contract (provenance_contract.md) specifies the structural requirements for how that citation must be recorded.

---

## 10. Relationship to Fact/Signal Consumption Matrices

Red flags are triggered by evidence — facts and signals consumed by their parent blocks. The consumption matrices define which evidence categories each block is authorized to consume:

- **fact_consumption_matrix.md**: Defines which fact categories each block consumes → red flags within a block can ONLY reference facts from categories mapped to that block
- **signal_consumption_matrix.md**: Defines which signal categories each block consumes → red flags within a block can ONLY reference signals from categories mapped to that block

A red flag that requires evidence from a fact/signal category not mapped to its parent block is a design error and must be corrected.

(See: fact_consumption_matrix.md, Section: 2 — Fact-to-Block Consumption Matrix)
(See: signal_consumption_matrix.md, Section: 2 — Signal-to-Block Consumption Matrix)

---

## 11. VG-SAI-8 Evidence Statement

This artifact provides evidence for Verification Gate VG-SAI-8 (Red Flag Taxonomy Gate). The gate criteria require:

| Gate Criterion | Status | Evidence |
|----------------|--------|----------|
| ≥2 red flags per block | MET | All 24 blocks have exactly 2 red flags defined (48 total) |
| Minimum 48 total red flags | MET | 48 red flags defined across all blocks |
| Evidence-based flags | MET | Every red flag specifies `required_evidence` field with explicit conditions |
| Categorical severity only | MET | All flags use only informational/elevated/critical — no numeric scores |
| No scoring language | MET | All `non_action_statement` fields explicitly prohibit action triggers |
| Provenance requirement per flag | MET | Every flag specifies `provenance_requirement` field |

**Gate Status**: EVIDENCE PREPARED — gate execution artifact (gate_vg_sai_08.md) required for formal pass.

This artifact prepares evidence for VG-SAI-8 but does NOT constitute gate completion. The gate must be explicitly executed as Task 15.8 with its own pass/fail artifact.

---

## 12. No-Drift Statement

This artifact:

- ✓ Contains ONLY definition-layer content (no implementation code)
- ✓ Contains NO numeric risk scores or scoring algorithms
- ✓ Contains NO buy/sell/hold recommendations or position sizing
- ✓ Contains NO allocation decisions or portfolio rebalancing triggers
- ✓ Contains NO price targets, fair value estimates, or expected returns
- ✓ Contains NO registry mutations or SSOT modifications
- ✓ Contains NO fact/signal creation or Market Evidence Framework modifications
- ✓ Contains NO asset-to-narrative mappings
- ✓ Uses ONLY approved diagnostic language ("requires review", "requires investigation", "warrants attention", "demands urgent review")
- ✓ Every non_action_statement explicitly prohibits portfolio action

If any future modification to this artifact introduces scoring, recommendation, allocation, or action-triggering language, that modification constitutes architectural drift and must be rejected.

---

## Document End

**Total Red Flags**: 48
**Blocks Covered**: 24/24
**Requirement Satisfied**: SAI-REQ-13
**Gate Evidence Prepared**: VG-SAI-8
**Drift Status**: Clean — no implementation, scoring, or action language detected
