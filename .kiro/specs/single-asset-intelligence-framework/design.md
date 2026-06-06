# Design Document

## Overview

**Spec**: single-asset-intelligence-framework
**Phase**: Design
**Status**: Draft / Design Foundation
**Authority**: ARCH
**Source References**:
- `.domainization/reports/single_asset_intelligence_framework_preflight_2026-06-05.md`
- `.kiro/specs/single-asset-intelligence-framework/requirements.md`

SAI is the canonical asset-level diagnostic layer between Market Evidence Framework (facts/signals) and downstream portfolio/reporting layers. It organizes evidence about individual assets into 24 structured analysis blocks for diagnostic interpretation.

### Architecture Boundary

SAI is diagnostic and interpretive ONLY. It MUST NOT:
- Score, rank, or produce numeric ratings
- Recommend buy/sell/hold
- Allocate capital or size positions
- Produce price targets or fair value estimates
- Create probabilities or confidence scores
- Create asset-to-narrative mappings
- Mutate any registry or SSOT
- Implement executable code

## Architecture

### Layer Model

```
Market Evidence Framework
  → Observed Facts (Layer 1)
  → Calculated Signals (Layer 2)
      ↓ consumed by
SAI Analysis Blocks (24 blocks)
      ↓ produce
SAI Interpretive Outputs
      ↓ consumed by (downstream, NOT owned by SAI)
Portfolio Health Framework | Reporting Layer | Future Scoring | Future Decision Engine
```

SAI does not depend on downstream layers. It is self-contained at the definition layer.

### Evidence Consumption Design

SAI consumes evidence declaratively:
- Fact Consumption Contract: declares which fact categories a block requires (no retrieval logic)
- Signal Consumption Contract: declares which signal categories a block requires (no calculation)
- SAI does NOT create facts or signals
- SAI does NOT define calculation formulas
- SAI does NOT implement data retrieval

### Provenance Design

Every SAI output preserves:
- source_fact_ids: list of consumed fact IDs
- source_signal_ids: list of consumed signal IDs
- timestamps: observation and calculation timestamps inherited from source
- source_type: primary/secondary/derived
- evidence_freshness: current/stale/expired/unknown
- completeness: high/medium/low/insufficient

No orphan interpretations are valid. An output without provenance is invalid.


## Components and Interfaces

### Analysis Block Architecture

Each of the 24 blocks follows this canonical structure:

| Field | Description |
|-------|-------------|
| block_id | Stable identifier (SAI-BLK-01 through SAI-BLK-24) |
| block_name | Human-readable name |
| category | Foundation/Operational/Financial Stability/Risk/Earnings/Valuation/Market Position/Outlook/Portfolio Context |
| purpose | One-sentence diagnostic purpose |
| primary_fact_families | Which fact domains this block consumes |
| primary_signal_families | Which signal types this block consumes |
| output_type | Diagnostic interpretation (never score/recommendation) |
| temporal_resolution | quarterly/monthly/daily/real-time |
| provenance_requirement | What source evidence must be cited |
| red_flag_requirement | Minimum 2 red flags with evidence thresholds |
| deferred_dependencies | External frameworks needed (if any) |

### Block Definitions (All 24)

#### Foundation Blocks

| Field | SAI-BLK-01 | SAI-BLK-02 |
|-------|------------|------------|
| block_name | Asset Identity | Business Model Quality |
| category | Foundation | Foundation |
| purpose | Establish canonical identity and classification of the asset | Diagnose the structural quality and sustainability of the business model |
| primary_fact_families | Company filings, sector classification, listing data, corporate structure | Revenue composition, segment breakdown, competitive position, moat indicators |
| primary_signal_families | Classification signals, sector rotation signals | Business model durability signals, competitive advantage signals |
| temporal_resolution | quarterly | quarterly |
| deferred_dependencies | None | None |

#### Operational Blocks

| Field | SAI-BLK-03 | SAI-BLK-04 | SAI-BLK-05 | SAI-BLK-06 |
|-------|------------|------------|------------|------------|
| block_name | Revenue Quality | Demand/Pipeline | Margin Quality | Cashflow Quality |
| category | Operational | Operational | Operational | Operational |
| purpose | Diagnose revenue sustainability, concentration, and organic vs inorganic growth | Diagnose demand visibility, backlog health, and pipeline trajectory | Diagnose margin structure, compression risk, and operating leverage | Diagnose cash generation quality, FCF conversion, and cash vs accrual divergence |
| primary_fact_families | Revenue breakdown, geographic mix, customer concentration, recurring vs one-time | Backlog, bookings, order intake, pipeline disclosures, guidance commentary | Gross margin, operating margin, SGA ratio, R&D ratio, margin trajectory | Operating cashflow, FCF, capex, working capital changes, cash conversion |
| primary_signal_families | Revenue growth signals, organic growth signals, concentration signals | Demand momentum signals, pipeline signals, booking trend signals | Margin expansion/compression signals, operating leverage signals | Cash conversion signals, FCF yield signals, capex intensity signals |
| temporal_resolution | quarterly | quarterly | quarterly | quarterly |
| deferred_dependencies | None | None | None | None |

| Field | SAI-BLK-11 | SAI-BLK-14 |
|-------|------------|------------|
| block_name | Working Capital | Pricing Power |
| category | Operational | Operational |
| purpose | Diagnose working capital efficiency, cash cycle health, and liquidity pressure | Diagnose ability to maintain or increase prices without demand destruction |
| primary_fact_families | Receivables, payables, inventory, cash conversion cycle, days outstanding | Pricing history, contract escalation clauses, volume vs price mix, competitor pricing |
| primary_signal_families | Working capital efficiency signals, inventory buildup signals | Pricing power signals, pass-through ability signals, elasticity indicators |
| temporal_resolution | quarterly | quarterly |
| deferred_dependencies | None | None |

#### Financial Stability Blocks

| Field | SAI-BLK-07 | SAI-BLK-08 | SAI-BLK-09 | SAI-BLK-10 |
|-------|------------|------------|------------|------------|
| block_name | Balance Sheet Quality | Credit/Solvency Risk | Hidden Liabilities | Pension Obligations |
| category | Financial Stability | Financial Stability | Financial Stability | Financial Stability |
| purpose | Diagnose overall balance sheet health, asset quality, and capital structure | Diagnose credit risk, refinancing exposure, and solvency trajectory | Diagnose off-balance-sheet obligations, contingent liabilities, and undisclosed risks | Diagnose pension funding status, obligation trajectory, and actuarial risk |
| primary_fact_families | Total assets, equity, debt structure, asset composition, goodwill/intangibles | Gross debt, net debt, maturity schedule, interest coverage, credit ratings, covenants | Operating leases, purchase obligations, guarantees, litigation, off-balance items | Defined benefit obligations, plan assets, funding gap, actuarial assumptions |
| primary_signal_families | Leverage signals, asset quality signals, capital structure signals | Credit deterioration signals, refinancing risk signals, covenant pressure signals | Hidden obligation signals, contingent liability signals | Pension underfunding signals, obligation growth signals |
| temporal_resolution | quarterly | quarterly | quarterly | quarterly |
| deferred_dependencies | None | None | None | None |

#### Risk Blocks

| Field | SAI-BLK-12 | SAI-BLK-13 |
|-------|------------|------------|
| block_name | Customer Concentration | Supply Chain Stability |
| category | Risk | Risk |
| purpose | Diagnose revenue dependency on key customers and concentration risk | Diagnose supply chain fragility, single-source risk, and disruption exposure |
| primary_fact_families | Top customer revenue share, customer count, contract duration, switching costs | Supplier concentration, geographic sourcing, inventory buffer, lead times |
| primary_signal_families | Concentration trend signals, customer loss signals | Supply disruption signals, lead time signals, inventory adequacy signals |
| temporal_resolution | quarterly | quarterly |
| deferred_dependencies | None | None |


#### Earnings Blocks

| Field | SAI-BLK-15 | SAI-BLK-16 |
|-------|------------|------------|
| block_name | Earnings Quality | Guidance/Estimate Revisions |
| category | Earnings | Earnings |
| purpose | Diagnose earnings sustainability, accrual quality, and manipulation risk | Diagnose management guidance credibility and analyst estimate trajectory |
| primary_fact_families | EPS composition, non-recurring items, accrual ratios, audit opinions | Management guidance history, analyst estimates, revision history, beat/miss pattern |
| primary_signal_families | Earnings quality signals, accrual anomaly signals | Guidance credibility signals, estimate revision momentum signals |
| temporal_resolution | quarterly | quarterly |
| deferred_dependencies | Earnings Intelligence Framework | Earnings Intelligence Framework |

#### Valuation Blocks

| Field | SAI-BLK-17 | SAI-BLK-18 |
|-------|------------|------------|
| block_name | Valuation Context | Value Trap Guard |
| category | Valuation | Valuation |
| purpose | Provide diagnostic context on current market pricing relative to fundamentals | Detect conditions where apparent cheapness masks structural impairment |
| primary_fact_families | P/E, EV/EBITDA, P/FCF, P/B, dividend yield, historical multiples | Same as Valuation Context plus cashflow quality, credit risk, fundamental trajectory |
| primary_signal_families | Valuation compression/expansion signals, multiple trajectory signals | Value trap indicator signals, fundamental deterioration signals |
| temporal_resolution | daily | daily |
| deferred_dependencies | Valuation Framework | Valuation Framework |

#### Market Position Blocks

| Field | SAI-BLK-19 | SAI-BLK-20 | SAI-BLK-21 |
|-------|------------|------------|------------|
| block_name | Relative Strength | Benchmark/Sector/Peer Correlation | Peer Comparison |
| category | Market Position | Market Position | Market Position |
| purpose | Diagnose price strength relative to benchmark, sector, and peers | Diagnose correlation structure and beta decomposition | Diagnose competitive positioning relative to peer group |
| primary_fact_families | Price performance vs benchmark, sector performance, drawdown history | Correlation coefficients, rolling beta, R-squared, factor exposures | Peer financial metrics, market share, growth differentials, margin differentials |
| primary_signal_families | Relative strength signals, momentum signals, drawdown signals | Correlation regime signals, beta decomposition signals | Peer rank signals, competitive position signals |
| temporal_resolution | daily | daily | daily |
| deferred_dependencies | None | Correlation/Dependency Framework | Peer Group Registry |

#### Outlook Blocks

| Field | SAI-BLK-22 | SAI-BLK-23 |
|-------|------------|------------|
| block_name | Company Outlook | Asset-Class Outlook |
| category | Outlook | Outlook |
| purpose | Synthesize forward-looking company-specific diagnostic from all available evidence | Diagnose asset-class level conditions affecting this asset |
| primary_fact_families | Management commentary, capital allocation plans, strategic initiatives, M&A activity | Sector fundamentals, regulatory environment, macro sensitivity, industry cycle position |
| primary_signal_families | Forward momentum signals, strategic execution signals | Sector rotation signals, regulatory risk signals, cycle position signals |
| temporal_resolution | quarterly | quarterly |
| deferred_dependencies | None | None |

#### Portfolio Context Block

| Field | SAI-BLK-24 |
|-------|------------|
| block_name | Portfolio Fit |
| category | Portfolio Context |
| purpose | Diagnose how this asset relates to portfolio-level constructs (concentration, overlap, sensitivity) |
| primary_fact_families | Position weight, sector allocation, geographic allocation, factor exposure |
| primary_signal_families | Concentration contribution signals, diversification signals, liquidity signals |
| temporal_resolution | daily |
| deferred_dependencies | Portfolio Health Framework |

### Deferred Interface Design

For each deferred framework, SAI declares ONLY what it expects as input. SAI does NOT define these frameworks.

#### 1. Valuation Framework
**SAI expects**: Canonical valuation methodology definitions — which multiples are primary, how to handle negative earnings, sector-appropriate valuation approaches. SAI consumes these definitions to contextualize valuation facts. SAI does NOT calculate fair value.

#### 2. Earnings Intelligence Framework
**SAI expects**: Earnings quality calculation rules — accrual ratio thresholds, non-recurring item classification, earnings manipulation detection heuristics. SAI consumes these rules to interpret earnings facts. SAI does NOT score earnings.

#### 3. Peer Group Registry
**SAI expects**: Canonical peer group definitions per asset — which companies constitute valid peers, peer selection methodology, peer rotation rules. SAI consumes these definitions for peer comparison context. SAI does NOT define peer groups.

#### 4. Portfolio Health Framework
**SAI expects**: Portfolio-level construct definitions — how concentration is measured, what constitutes overlap, sensitivity metrics. SAI consumes these definitions for portfolio fit interpretation. SAI does NOT allocate or rebalance.

#### 5. Correlation/Dependency Framework
**SAI expects**: Correlation calculation methodology — rolling window parameters, regime detection rules, beta decomposition approach. SAI consumes these definitions for correlation interpretation. SAI does NOT calculate correlations.

#### 6. Signal Calculation Framework
**SAI expects**: Signal derivation formulas — how each signal is calculated from facts, thresholds, normalization rules. SAI consumes calculated signals. SAI does NOT implement signal calculation.

#### 7. Data Ingestion/Normalization Framework
**SAI expects**: Normalized fact delivery — standardized fact objects with provenance metadata, temporal alignment, currency normalization. SAI consumes normalized facts. SAI does NOT implement data retrieval or normalization.


## Data Models

### Output Object Design

SAI analysis block output object (conceptual, not implementation):

```yaml
sai_block_output:
  block_id: "SAI-BLK-NN"
  asset_id: "<asset identifier>"
  consumed_facts: [list of fact_ids]
  consumed_signals: [list of signal_ids]
  interpretation_summary: "Diagnostic text — no score, no recommendation"
  red_flags:
    - flag_id: "RF-NN-01"
      severity: informational | elevated | critical
      evidence: [fact/signal references]
      description: "Evidence-based warning"
  evidence_completeness: high | medium | low | insufficient
  temporal_status: current | stale | expired
  provenance_chain:
    source_facts: [...]
    source_signals: [...]
    timestamps: [...]
    freshness: current | stale | expired
  deferred_dependency_notes: "Valuation Framework not yet available — interpretation limited"
```

PROHIBITED fields (must NEVER appear in any SAI output object):
- score, rank, recommendation, target_weight, position_size
- price_target, fair_value, buy/sell/hold
- probability_of_success, expected_return, alpha_estimate
- confidence_score, conviction_level, risk_score
- overvalued, undervalued, fairly_valued
- buy_signal, sell_signal, hold_signal

### Red Flag Design

Red flags are categorical, evidence-based warnings:
- **informational**: notable condition worth monitoring — does not require action
- **elevated**: condition indicating material risk requiring attention — warrants deeper investigation
- **critical**: condition indicating severe risk requiring immediate attention — demands urgent review

Red flags MUST NOT:
- Become numeric risk scores
- Trigger automated actions
- Map to buy/sell/hold decisions
- Aggregate into composite risk ratings
- Be weighted or prioritized algorithmically

Red flag examples (illustrative, not exhaustive):
- RF-08-01 (Credit/Solvency): "Net debt/EBITDA exceeds 4x with near-term maturity wall" — elevated
- RF-09-01 (Hidden Liabilities): "Off-balance-sheet obligations exceed 30% of reported debt" — critical
- RF-06-01 (Cashflow Quality): "FCF conversion below 50% for 3 consecutive quarters" — elevated
- RF-18-01 (Value Trap Guard): "Low multiple coincides with declining FCF and rising leverage" — critical

### Evidence Completeness Design

Categories (metadata only, NOT a score):
- **high**: all required facts/signals available and current — full interpretation possible
- **medium**: most evidence available but gaps or staleness present — interpretation valid but limited
- **low**: significant gaps in required evidence — interpretation is materially constrained
- **insufficient**: not enough evidence for valid interpretation — block output should note severe limitation

Evidence completeness MUST NOT:
- Map to action recommendations (insufficient ≠ "do not invest")
- Become a numeric completeness score
- Be used for ranking assets by data quality
- Trigger automated data acquisition

### Temporal Resolution Design

| Class | Refresh Requirement | Block Types | Rationale |
|-------|-------------------|-------------|-----------|
| quarterly | Updated after each earnings cycle | Foundation, Operational, Financial Stability, Risk, Earnings, Outlook | Corporate disclosures drive these blocks — filing cadence determines freshness |
| monthly | Updated monthly for trend detection | Working Capital (optional upgrade) | Working capital can shift within quarters; monthly provides earlier warning |
| daily | Updated daily from market data | Valuation, Market Position, Portfolio Fit | Prices, correlations, and portfolio weights change daily |
| real-time | Exceptional; not default | None by default — reserved for future streaming signals | Creates false precision and infrastructure burden without proportional diagnostic value |

Temporal resolution governs when evidence is considered "stale" or "expired":
- quarterly blocks: stale after 100 days, expired after 120 days
- monthly blocks: stale after 35 days, expired after 45 days
- daily blocks: stale after 2 days, expired after 5 days
- real-time blocks: stale after 1 hour, expired after 4 hours (future, if implemented)

### Block Independence Design

Each block MUST function independently:
- No block requires another block's output as input
- Blocks consume facts and signals directly from the Evidence Framework
- Cross-block synthesis is a downstream consumer concern (not SAI's responsibility)
- Removal of any single block does not break other blocks

This independence enables:
- Partial interpretation when some blocks lack evidence
- Parallel evaluation of all blocks
- Additive extension (new blocks do not affect existing ones)
- Downstream consumers to select any subset of blocks


## Correctness Properties

### Property 1: Block Taxonomy Stability

All 24 blocks must maintain stable identifiers (SAI-BLK-01 through SAI-BLK-24). No block may be removed or renamed. Extension is additive only — new blocks receive identifiers SAI-BLK-25+.

**Invariant**: `count(blocks) == 24 AND all block_ids in {SAI-BLK-01..SAI-BLK-24} AND no block_id reused or reassigned`

**Validates: Requirements 1, 14**

### Property 2: Boundary Enforcement

Zero scoring, recommendation, allocation, or trading language exists in any SAI output object or block definition. No field in any SAI data model contains numeric scores, buy/sell/hold signals, price targets, fair value estimates, or probability assessments.

**Invariant**: `for all fields F in SAI output objects: F.name NOT IN {score, rank, recommendation, target_weight, position_size, price_target, fair_value, probability_of_success, expected_return, alpha_estimate, confidence_score, buy_signal, sell_signal}`

**Validates: Requirements 5**

### Property 3: Provenance Completeness

Every SAI output traces to specific fact/signal IDs with timestamps. No orphan interpretations exist. Every interpretation_summary is backed by at least one consumed_fact or consumed_signal reference.

**Invariant**: `for all outputs O: len(O.consumed_facts) + len(O.consumed_signals) >= 1 AND O.provenance_chain.timestamps is non-empty`

**Validates: Requirements 4**

### Property 4: Evidence Coverage

Every block has at least one fact family and at least one signal family mapped. The union of all block fact family mappings covers all 68 canonical fact categories. The union of all block signal family mappings covers all 23 canonical signal categories.

**Invariant**: `for all blocks B: len(B.primary_fact_families) >= 1 AND len(B.primary_signal_families) >= 1 AND union(all B.primary_fact_families) ⊇ {68 canonical facts} AND union(all B.primary_signal_families) ⊇ {23 canonical signals}`

**Validates: Requirements 2, 3**

### Property 5: Temporal Consistency

Every block has an assigned temporal resolution class (quarterly/monthly/daily/real-time) with documented rationale. No block exists without temporal assignment.

**Invariant**: `for all blocks B: B.temporal_resolution IN {quarterly, monthly, daily, real-time} AND B.temporal_rationale is non-empty`

**Validates: Requirements 6**

### Property 6: Red Flag Presence

Every block supports at least 2 red flags with evidence thresholds. Flags are categorical only (informational/elevated/critical). No flag produces a numeric score.

**Invariant**: `for all blocks B: len(B.red_flags) >= 2 AND for all flags F in B.red_flags: F.severity IN {informational, elevated, critical} AND F.evidence is non-empty`

**Validates: Requirements 13**

### Property 7: No SSOT Mutation

No SAI deliverable modifies Market Evidence Framework, Narrative Framework v2, Narrative Registry, Market Organism Layer 0, central glossary, or any artifact registry. SAI is read-only with respect to all upstream canonical sources.

**Invariant**: `SAI write operations ∩ {market_evidence_framework, narrative_framework_v2, narrative_registry, market_organism_principles, shared_glossary, artifact_registry} == ∅`

**Validates: Requirements 5**

### Property 8: Block Independence

No block's output appears as input to another block's fact or signal consumption contract. Cross-block dependencies are zero within SAI.

**Invariant**: `for all blocks B1, B2 where B1 ≠ B2: B2.output NOT IN B1.primary_fact_families AND B2.output NOT IN B1.primary_signal_families`

**Validates: Requirements 1**

### Property 9: Deferred Interface Completeness

Every block with a deferred dependency has an explicit interface contract declaring what it expects from the deferred framework. No block silently depends on an undefined framework.

**Invariant**: `for all blocks B where B.deferred_dependencies is non-empty: for all D in B.deferred_dependencies: interface_contract(D) is defined`

**Validates: Requirements 14**

### Property 10: Output Completeness

Every SAI block output object contains all required fields: block_id, asset_id, consumed_facts, consumed_signals, interpretation_summary, red_flags, evidence_completeness, temporal_status, provenance_chain, deferred_dependency_notes.

**Invariant**: `for all outputs O: all required fields are present AND no required field is null`

**Validates: Requirements 4, 15**


## Error Handling

### Missing Evidence

If a block's required facts/signals are unavailable:
- Set evidence_completeness to "low" or "insufficient"
- Document which facts/signals are missing in deferred_dependency_notes
- Do NOT produce interpretation without evidence (no orphan outputs)
- Do NOT substitute assumptions for missing data
- Do NOT infer facts from signals or signals from facts
- Do NOT use industry averages or defaults as substitutes

The block output remains structurally valid but explicitly communicates the limitation. Downstream consumers decide how to handle incomplete blocks — SAI does not make that decision.

### Deferred Framework Unavailability

If a deferred framework (Valuation, Earnings, Peer Group, etc.) does not yet exist:
- Block operates with available evidence only
- deferred_dependency_notes field documents the limitation clearly
- Block output is still valid but marked as limited in scope
- Do NOT invent methodology to fill the gap
- Do NOT approximate the deferred framework's expected output
- Do NOT silently omit the block from output

Example: If Valuation Framework is unavailable, SAI-BLK-17 (Valuation Context) still produces output using raw multiple facts, but notes: "Valuation Framework not yet available — interpretation limited to raw multiple observation without canonical methodology context."

### Stale Evidence

If evidence is older than the block's temporal resolution threshold:
- Set temporal_status to "stale" or "expired" based on threshold
- Retain the interpretation but flag staleness explicitly
- Do NOT suppress stale outputs — staleness itself is informative
- Do NOT refresh evidence (SAI is not responsible for data freshness)
- Do NOT extrapolate or project stale data forward

Staleness thresholds (from Temporal Resolution Design):
- quarterly blocks: stale > 100 days, expired > 120 days
- monthly blocks: stale > 35 days, expired > 45 days
- daily blocks: stale > 2 days, expired > 5 days

### Invalid Evidence

If consumed facts/signals fail structural validation (malformed IDs, impossible values, broken provenance):
- Reject the invalid evidence item (do not consume it)
- Note the rejection in deferred_dependency_notes
- Proceed with remaining valid evidence
- Set evidence_completeness to reflect the gap
- Do NOT attempt to repair invalid evidence

### Conflicting Evidence

If multiple facts/signals within a block provide contradictory information:
- Present both/all conflicting evidence items in consumed_facts/consumed_signals
- Note the conflict explicitly in interpretation_summary
- Do NOT resolve the conflict by picking one side
- Do NOT average or blend conflicting values
- The conflict itself is diagnostic information

## Testing Strategy

### Verification Approach

SAI produces definition-layer architecture — not executable code. Verification is structural:

1. **Document inspection** — verify all 24 blocks are defined with all required fields populated
2. **Coverage matrix validation** — verify fact/signal-to-block mappings are complete (68 facts, 23 signals, all assigned)
3. **Boundary scan** — verify zero scoring/recommendation/allocation language in any output definition
4. **Provenance chain check** — verify every output object specification references source evidence fields
5. **Gate execution** — run VG-SAI-1 through VG-SAI-12 as explicit verification tasks with pass/fail evidence
6. **Independence verification** — verify no block-to-block input dependencies exist
7. **Deferred contract completeness** — verify all deferred dependencies have explicit interface contracts

### Property-Based Testing Applicability

PBT does NOT apply to this design phase. SAI is a definition-layer architecture, not executable code with inputs/outputs that can be fuzzed or property-tested. Verification is structural: blocks present, fields defined, boundaries enforced, provenance documented.

When SAI progresses to implementation (future, not in this spec), PBT will apply to:
- Output object validation (generated outputs conform to schema)
- Boundary enforcement (no prohibited fields in generated outputs)
- Provenance completeness (all outputs have valid provenance chains)
- Red flag categorization (flags always have valid severity + evidence)

### Verification Gate Alignment

| Gate ID | Gate Name | Design-Phase Executable? | Verification Method |
|---------|-----------|-------------------------|---------------------|
| VG-SAI-1 | Requirements Completeness Gate | YES | Verify all 24 blocks defined with required fields |
| VG-SAI-2 | Boundary Enforcement Gate | YES | Scan all definitions for scoring/recommendation language |
| VG-SAI-3 | Provenance Chain Gate | YES | Verify provenance specification per block output object |
| VG-SAI-4 | Interface Contract Gate | YES | Verify all 7 deferred contracts declared with expectations |
| VG-SAI-5 | Taxonomy Stability Gate | YES | Verify block IDs frozen, additive extension documented |
| VG-SAI-6 | Fact Coverage Gate | TASK PHASE | Requires detailed coverage matrix (68 facts → 24 blocks) |
| VG-SAI-7 | Signal Coverage Gate | TASK PHASE | Requires detailed signal mapping (23 signals → 24 blocks) |
| VG-SAI-8 | Red Flag Taxonomy Gate | TASK PHASE | Requires 2+ red flags defined per block with thresholds |
| VG-SAI-9 | Temporal Resolution Gate | YES | Verify all blocks have temporal assignment with rationale |
| VG-SAI-10 | Cross-Framework Consistency Gate | TASK PHASE | Requires terminology audit against canonical glossary |
| VG-SAI-11 | KPI Mapping Validation Gate | TASK PHASE | Requires KPI sheet mapping per block |
| VG-SAI-12 | Portfolio Fit Interface Gate | YES | Verify output schema contains no allocation language |

### Design-Phase Gate Execution Summary

Gates executable NOW (design phase):
- VG-SAI-1: PASS — all 24 blocks defined with identifiers, categories, purposes, fact/signal families
- VG-SAI-2: PASS — zero scoring/recommendation language in design document
- VG-SAI-3: PASS — provenance chain specified in output object schema
- VG-SAI-4: PASS — all 7 deferred interface contracts declared
- VG-SAI-5: PASS — block IDs SAI-BLK-01 through SAI-BLK-24 frozen, extension additive only
- VG-SAI-9: PASS — all blocks assigned temporal resolution with rationale
- VG-SAI-12: PASS — Portfolio Fit output contains no allocation/sizing language

Gates requiring task-phase completion:
- VG-SAI-6, VG-SAI-7, VG-SAI-8, VG-SAI-10, VG-SAI-11 — require detailed mapping artifacts


## Valuation / Value Trap Design

"Low valuation is not automatically undervaluation. A stock is not cheap because it fell. A stock is cheap only if market expectation is below realistic value creation."

### Valuation Context (SAI-BLK-17)

Purpose: Provide diagnostic context — NOT fair value calculation.

Valuation Context requires cross-reference evidence from:
1. Cashflow Quality (SAI-BLK-06) — is the business generating real cash?
2. Credit/Solvency (SAI-BLK-08) — is the balance sheet sound enough to sustain operations?
3. Hidden Liabilities (SAI-BLK-09) — are there obligations not reflected in headline multiples?
4. Earnings Quality (SAI-BLK-15) — are reported earnings trustworthy?
5. Company Outlook (SAI-BLK-22) — is forward trajectory consistent with current pricing?
6. Peer Context (SAI-BLK-21) — how does this asset's pricing compare to peers?

NOTE: These are consumption references for interpretive context, NOT block-to-block dependencies. SAI-BLK-17 consumes the same underlying facts/signals as these blocks — it does not consume their outputs.

Valuation Context outputs:
- Current multiple context (P/E, EV/EBITDA, P/FCF relative to own history and sector)
- Valuation compression/expansion trajectory
- Evidence gaps that limit interpretation
- Deferred dependency note if Valuation Framework unavailable

Valuation Context does NOT output:
- Fair value estimate
- Target price
- "Undervalued" / "Overvalued" / "Fairly valued" labels
- Probability of revaluation
- Expected return

### Value Trap Guard (SAI-BLK-18)

Purpose: Detect conditions where statistical cheapness masks structural impairment.

Value Trap Guard detects these diagnostic patterns:
- Low multiple + weak cashflow = potential value trap (FCF quality deteriorating while headline earnings maintained)
- Low multiple + refinancing risk = structural impairment (debt maturity wall, rising credit spreads)
- Low multiple + declining fundamentals = justified discount (market correctly pricing deterioration)
- Statistical cheapness without operational substance (multiple compression without earnings growth path)
- Dividend yield trap (high yield from price decline, not sustainable payout)

Value Trap Guard does NOT:
- Label anything as "undervalued" or "overvalued"
- Recommend buy, sell, or hold
- Calculate probability of being a value trap
- Score "trap-ness" on a numeric scale
- Produce a binary trap/not-trap classification

Value Trap Guard output is diagnostic narrative explaining which trap conditions are present or absent, with evidence citations.

## Credit / Solvency Design

### Full Scope (SAI-BLK-08)

Credit/Solvency Risk covers the complete debt and solvency picture:

**Debt Structure Facts**:
- Gross debt (total borrowings)
- Net debt (gross debt minus cash and equivalents)
- Maturity schedule (when debt comes due)
- Short-term debt (due within 12 months)
- Available liquidity (undrawn facilities, cash reserves)
- Secured vs unsecured debt composition

**Coverage and Capacity Facts**:
- Interest coverage ratio (EBIT/interest expense)
- Net debt/EBITDA ratio
- FCF/total debt ratio
- Debt service coverage ratio

**Off-Balance and Hidden Obligations**:
- Lease liabilities (operating and finance)
- Purchase obligations (committed future spending)
- Off-balance-sheet commitments (guarantees, SPVs)
- Pension obligations and funding gap (cross-reference SAI-BLK-10)
- Goodwill, intangibles, and impairment risk

**Structural and Market Evidence**:
- LBO history and sponsor overhang
- Covenant pressure (proximity to covenant breach)
- Bond spread trajectory
- CDS spread trajectory
- Credit rating and rating trajectory

**Critical Principle**: Credit ratings are INPUTS to SAI, NOT truth. SAI does not endorse, validate, or rely on credit ratings as authoritative. Ratings are one evidence input among many. A company can have investment-grade ratings and still exhibit material credit risk.

### Cross-Reference to Hidden Liabilities (SAI-BLK-09)

SAI-BLK-08 and SAI-BLK-09 share fact families in the off-balance-sheet domain. The distinction:
- SAI-BLK-08 uses these facts for solvency trajectory diagnosis
- SAI-BLK-09 uses these facts for disclosure adequacy diagnosis

Both blocks independently consume the same underlying facts — no block-to-block dependency.

## Peer / Benchmark Design

### Scope (SAI-BLK-19, SAI-BLK-20, SAI-BLK-21)

Market Position blocks diagnose:
- Relative strength vs benchmark, sector, and peer group (SAI-BLK-19)
- Correlation structure, beta decomposition, co-movement analysis (SAI-BLK-20)
- Competitive positioning and peer-relative metrics (SAI-BLK-21)

**Relative Strength (SAI-BLK-19)**:
- Price performance vs benchmark over multiple timeframes
- Sector-relative performance
- Drawdown history and recovery characteristics
- Momentum trajectory (without momentum score)
- Own-strength vs beta-driven movement decomposition

**Correlation (SAI-BLK-20)**:
- Rolling correlation to benchmark
- Sector correlation vs idiosyncratic movement
- Factor exposure decomposition
- Correlation regime changes over time
- Volatility-adjusted relative performance

**Peer Comparison (SAI-BLK-21)**:
- Financial metric comparison (margins, growth, returns)
- Market share and competitive position
- Valuation differential vs peers
- Growth differential vs peers
- Quality metric differential vs peers

### Peer Group Dependency

Peer groups are NON-CANONICAL until the Peer Group Registry exists as a separate framework. Until then:
- Ad-hoc peer comparisons are flagged as "lower confidence — non-canonical peer group"
- Peer selection methodology is not SAI's responsibility
- SAI consumes peer definitions; it does not create them
- Any peer comparison without canonical peer group reference carries a deferred_dependency_note


## Portfolio Fit Design

### Scope (SAI-BLK-24)

Portfolio Fit diagnoses how an individual asset relates to portfolio-level constructs. It is the bridge between single-asset analysis and portfolio-level health — but it does NOT cross into portfolio management.

**Allowed Diagnostic Dimensions**:
- Concentration contribution: how much portfolio concentration this asset adds
- Dependency overlap: shared dependencies with other portfolio positions (suppliers, customers, geographies)
- Future narrative overlap interface: placeholder for narrative exposure linkage (deferred until Narrative Framework integration)
- Macro sensitivity: how sensitive this asset is to macro factors shared with other positions
- Liquidity sensitivity: how this asset's liquidity profile affects portfolio-level liquidity
- Diversification contribution: what independent risk this asset contributes
- Fragility contribution: how this asset's tail risk compounds portfolio-level fragility

**Forbidden Outputs** (Portfolio Fit MUST NOT produce):
- Target weight or suggested allocation
- Position size recommendation
- Capital allocation instruction
- Buy/sell/hold decision
- Optimization output (mean-variance, risk parity, etc.)
- Rebalance instruction or trigger
- "Overweight" / "Underweight" / "Neutral" labels
- Portfolio-level score incorporating this asset

**Interface Contract with Portfolio Health Framework** (deferred):
- SAI-BLK-24 declares what it will PRODUCE (diagnostic dimensions above)
- Portfolio Health Framework will consume these diagnostics
- SAI does NOT consume Portfolio Health Framework outputs (no circular dependency)
- When Portfolio Health Framework exists, SAI-BLK-24 may additionally consume portfolio-level context definitions

### Independence Preservation

Portfolio Fit maintains block independence:
- It consumes facts about this asset's portfolio membership (weight, sector, geography)
- It consumes signals about concentration and correlation
- It does NOT consume other SAI block outputs
- It does NOT require portfolio-level optimization context to function
- It provides diagnostic observations; downstream frameworks act on them

## Design Non-Goals

The following are explicitly out of scope for this design document. They are documented to prevent scope creep and to clarify the boundary of SAI's definition-layer architecture.

- **No implementation or runtime architecture**: No class hierarchies, service boundaries, API endpoints, or execution flows
- **No database schema or storage design**: No table definitions, index strategies, or persistence mechanisms
- **No scoring methodology**: No numeric scores, composite ratings, or weighted aggregations
- **No investment recommendation logic**: No buy/sell/hold rules, no decision trees, no threshold-based actions
- **No dashboard or UI design**: No visualization specifications, layout designs, or user interaction flows
- **No registry mutation**: No changes to Narrative Registry, artifact registry, or domain registry
- **No asset-to-narrative mapping**: SAI does not link assets to narratives — that is the Narrative Framework's domain
- **No narrative mapping**: SAI does not create, modify, or consume narrative mappings
- **No code generation**: No executable code, scripts, classes, functions, or algorithms
- **No data pipeline design**: No ETL flows, scheduling, or data movement architecture
- **No API design**: No REST endpoints, GraphQL schemas, or service interfaces
- **No infrastructure design**: No deployment topology, scaling rules, or infrastructure-as-code

## Extension Mechanism

### Additive-Only Extension Rules

SAI taxonomy is extendable under strict rules:

1. **New blocks**: May be added as SAI-BLK-25, SAI-BLK-26, etc. — IDs are never reused
2. **New fact families**: May be added to existing blocks without removing existing mappings
3. **New signal families**: May be added to existing blocks without removing existing mappings
4. **New red flags**: May be added to existing blocks — minimum 2 per block is a floor, not a ceiling
5. **New categories**: May be added if a new block does not fit existing categories
6. **New temporal resolution classes**: May be added (e.g., weekly) with documented rationale

### Prohibited Mutations

1. **Block removal**: No existing block may be removed or deprecated
2. **Block renaming**: No existing block name may change (identifier or human-readable)
3. **Category reassignment**: No existing block may change category
4. **Fact family removal**: No existing fact family mapping may be removed from a block
5. **Signal family removal**: No existing signal family mapping may be removed from a block
6. **Temporal downgrade**: No block may reduce its temporal resolution (daily → quarterly)

### Extension Governance

All extensions require:
- Documented rationale for the addition
- Verification that no existing block is modified
- Verification that the new element does not introduce scoring/recommendation language
- Update to the design document (this file) with the new element documented
- Update to requirements document if new requirements are implied

## Cross-References

(See: README_market_evidence_framework, Section: 1. Scope Statement)
(See: README_market_evidence_framework, Section: 3. The Evidence Hierarchy)
(See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)
(See: README_market_evidence_framework, Section: 31. Valuation Trap Boundary)
(See: README_market_organism_principles, Section: Principle 2 — Taxonomy Precedes Assets)
(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 6. Core Analysis Blocks)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 8. Required Fact Categories)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 9. Required Signal Categories)
(See: single_asset_intelligence_framework_preflight_2026-06-05, Section: 10. Verification Gates)
(See: single_asset_intelligence_framework_requirements_report_2026-06-06, Section: Requirements Coverage)
(See: README_narrative_framework_v2, Section: Connected Systems)
(See: shared_glossary_reference, Section: Evidence Terminology)

---

*Document generated: 2026-06-06*
*Authority: ARCH*
*Phase: Design Foundation — Definition Layer Only*
*Next: Human review → tasks.md generation*
