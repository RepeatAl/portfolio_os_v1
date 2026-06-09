---
artifact_id: tactical_momentum_execution_gate_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-06-09
last_modified: 2026-06-09
owner_role: Defines the Tactical Momentum Execution Gate Framework — entry-readiness assessment between Opportunity and Deployment
ssot_relationship: canonical
topic: tactical_execution_gate
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies:
  - system_architecture_md
  - decision_governance_md
  - deployment_intelligence_framework_md
  - market_regime_framework_md
  - opportunity_engine_design_md
  - portfolio_health_framework_md
  - semantic_signal_registry_md
  - semantic_reasoning_rules_md
  - signal_calculation_framework_md
---

# PORTFOLIO OS — TACTICAL MOMENTUM EXECUTION GATE FRAMEWORK
Version: v1
Status: Canonical SSOT — Architecture Definition

---

# PURPOSE

This document defines the Tactical Momentum Execution Gate Framework.

The framework is NOT a trading layer.
The framework is NOT an execution engine.
The framework does NOT generate orders.

The framework answers exactly one question:

**"Is there a technically clean entry path for an asset that has already been qualified by Portfolio OS portfolio-, regime-, and quality-side analysis — and are the risk, product, and market-structure gates satisfied for preparing a Human Execution Package?"**

The output is:

```
execution_readiness_status
```

Not:

```
Buy.
```

---

# CORE PRINCIPLE

Momentum is NOT a purchase command.

Momentum is an Entry Gate.

The Tactical Momentum Execution Gate Framework occupies one specific position in the Portfolio OS reasoning chain:

```
Portfolio State
→ Market Regime Gate
→ Asset Quality (SAI)
→ Opportunity Score
→ Tactical Momentum Execution Gate      ← THIS FRAMEWORK
→ Deployment Readiness
→ Human Execution Package
→ Human Decision
```

The human remains the final decision-maker.

Portfolio OS does not execute trades.
Portfolio OS does not route orders.
Portfolio OS does not connect to brokers, exchanges, or trading venues.

This framework prepares the reasoning package for human execution.
It does not initiate execution.

---

# ARCHITECTURE POSITION

## Where This Framework Fits

This framework is positioned between the Opportunity Engine and the Deployment Intelligence Framework.

It does NOT:
- Replace Asset Quality assessment (that is SAI)
- Replace Portfolio Fit analysis (that is SAI-BLK-24 and Portfolio Health Framework)
- Replace Opportunity Engine output (that is the Opportunity Engine Design)
- Replace Market Regime interpretation (that is the Market Regime Framework)
- Constitute deployment authority (that is the Deployment Intelligence Framework)
- Constitute a trade instruction (that is the Human Execution Package, always human-approved)

It ONLY:
- Checks whether the entry timing is technically clean for an already-qualified asset
- Checks whether risk, liquidity, event, and market-structure gates are satisfied
- Checks whether derivative product review is appropriate (not execution — review only)
- Produces an execution_readiness_status for the Human Execution Package

---

# RELATIONSHIP TO EXISTING SIGNAL HIERARCHY

Signal hierarchy from decision_governance.md (canonical):

```
1. Structural portfolio signals
2. Market structure signals
3. Liquidity conditions
4. Breadth confirmation
5. Cross-asset confirmation
6. Scenario sensitivity
7. Correlation structure
8. Narrative dependency
9. Tactical momentum          ← THIS FRAMEWORK
10. Financial news
```

Tactical momentum is rank 9 of 10.

It does not dominate structure.
It does not override portfolio quality.
It does not override regime conditions.
It does not create its own opportunity assessment.

It is the final gate before a Human Execution Package is prepared.

---

# MARKET AMPEL

## Definition

The market_ampel is the aggregated market readiness signal derived from existing regime, breadth, liquidity, volatility, and credit state engines.

The market_ampel is NOT:
- A separate regime interpretation
- A parallel market logic
- An AI-estimated market condition

The market_ampel IS derived from:

```
market_regime_state
+ liquidity_state
+ breadth_state
+ volatility_state
+ credit_state
→ market_ampel
```

The market_ampel must not create a second, independent market truth.
All inputs to market_ampel must originate from canonical signal engines.
Semantics are truth. The market_ampel is derived semantic output.

## Market Ampel States

| market_ampel | Meaning | Effect |
|-------------|---------|--------|
| `AKTIV` | Risk-on: broad participation, stable credit, controlled volatility, positive market regime | Equity entries allowed; derivative review possible |
| `SELEKTIV` | Positive base trend but uneven participation, stretched conditions, or elevated event risk | Only high-quality setups; reduced sizing; derivatives only conservative |
| `DEFENSIV` | Credit stress, elevated volatility, impaired trend, or structural deterioration | No new long leverage instruments; equity entries only exceptional or defensive context |

## Critical Rule

`DEFENSIV` is a hard block for new long leverage instruments.

This is consistent with the Deployment Intelligence Framework principle:
"The system evaluates when flexibility matters, when exposure matters."

A DEFENSIV market_ampel means leverage instruments amplify tail risk
in an already-stressed structural environment.

---

# ENTRY GATES

## Entry Type Taxonomy

| entry_type | Definition |
|-----------|-----------|
| `BREAKOUT` | Asset breaks above a defined technical structure with volume confirmation and relative strength support |
| `PULLBACK` | Asset retreats to a defined support level within an intact primary trend with controlled momentum loss |
| `NONE` | No clean entry type currently identifiable — no setup ready |

The entry type does NOT imply a purchase decision.
The entry type is one gate input to execution_readiness_status.

## Entry Gate Dimensions

**Market Gate:**

| Field | Description |
|-------|-------------|
| `market_ampel` | Aggregated market readiness (AKTIV / SELEKTIV / DEFENSIV) |
| `market_ampel_reason` | Derived reasoning from regime/breadth/liquidity/volatility/credit |
| `regime_state_source` | Which regime engine produced the underlying state |
| `liquidity_state` | Liquidity signal input to market_ampel |
| `breadth_state` | Breadth signal input to market_ampel |
| `volatility_state` | Volatility signal input to market_ampel |
| `credit_state` | Credit signal input to market_ampel |

**Technical Entry Gate:**

| Field | Description |
|-------|-------------|
| `entry_type` | BREAKOUT / PULLBACK / NONE |
| `relative_strength_score` | Relative strength vs. benchmark and sector |
| `volume_confirmation` | Whether volume supports the entry signal |
| `trend_status` | Intact / damaged / reversal |
| `breakout_level` | Price level defining breakout trigger |
| `pullback_support` | Price level defining pullback support |
| `entry_trigger` | Specific condition that activates entry readiness |
| `invalid_level` | Price level that invalidates the setup |
| `technical_confidence` | Qualitative confidence in technical entry conditions |
| `tactical_confidence` | Aggregated entry confidence including signal conflict assessment |
| `signal_conflict_flags` | Any signals contradicting the entry setup |
| `entry_confidence_reason` | Explanation of what drives or limits tactical confidence |

**Portfolio Fit Gate:**

| Field | Description |
|-------|-------------|
| `asset_quality_score` | From SAI / Opportunity Engine — not recalculated here |
| `regime_fit_score` | Alignment of asset with current regime |
| `opportunity_score` | From Opportunity Engine — not recalculated here |
| `portfolio_fit_status` | From Portfolio Health Framework — not recalculated here |
| `dependency_conflict_flag` | Whether this entry increases portfolio dependency concentration |
| `concentration_conflict_flag` | Whether this entry increases portfolio concentration |

---

# CONFIDENCE MODEL INTEGRATION

## Tactical Confidence Is Not Prediction Certainty

Consistent with decision_governance.md:

"Confidence measures: signal alignment, structural consistency, regime stability, scenario coherence."

Tactical confidence means:
- Multiple technical dimensions currently agree
- No material signal conflicts exist
- Market structure supports the entry context

Tactical confidence does NOT mean:
- The trade will succeed
- The target will be reached
- Future performance is predictable

## Signal Conflict Handling

A BREAKOUT setup can appear technically strong while:
- Market breadth is deteriorating
- Volatility regime is unstable
- Cross-asset signals are deteriorating (rates, oil, credit)

When signal conflicts are detected:
- `signal_conflict_flags` are populated
- `tactical_confidence` is reduced
- `entry_confidence_reason` documents the conflict
- The execution_readiness_status reflects the conflict

A technically good setup with conflicting structural signals produces
LIMIT_READY with reduced confidence, not unconditional readiness.

---

# RISK AND SIZING GATE

## Principle

The Tactical Momentum Execution Gate does NOT determine how much capital is at risk.
It determines only whether the requested risk falls within available budget.

```
requested_risk_per_trade_eur <= available_risk_budget_eur → risk gate passes
```

The risk budget must come from Position Sizing Governance / Deployment Governance.
This framework consumes the budget; it does not set it.

## Allocation Policy

Budget parameters are policy configuration, not engine constants.
They are versioned separately to allow MoneyHorst to run different campaign sizes
without modifying the engine logic.

Example policy structure (not canonical values — set by active policy version):

```yaml
allocation_round_policy:
  policy_version: tactical_budget_policy_v1
  allocation_round_eur: [configured externally]
  core_budget_eur: [configured externally]
  speculative_budget_eur: [configured externally]
  aggressive_risk_budget_eur: [configured externally]
```

The engine reads the active policy version.
It does not hardcode allocation amounts.

## Risk Gate Dimensions

| Field | Description |
|-------|-------------|
| `risk_per_trade_eur` | Requested maximum capital at risk for this trade |
| `risk_budget_available_eur` | Available risk budget from active policy |
| `position_size` | Proposed size consistent with risk parameters |
| `max_position_size` | Maximum size allowed by policy |
| `risk_budget_status` | Whether requested risk fits within available budget |
| `speculation_budget_bucket` | Which budget bucket this trade draws from (core / speculative / aggressive) |

---

# DERIVATIVE GATE

## Principle

This framework supports derivative product review, not derivative execution authorization.

The principle from the existing Leverage Product Handbook (Hebelprodukt-Handbuch) applies:

First underlying probability, then movement path, then instrument.
Never the other way around.

The correct assessment order is:

```
Signal
→ Scenario
→ Underlying
→ Expected movement
→ Time window
→ Volatility state
→ Product mechanics
→ 3x-Payoff-Test
→ Kill-Switch
```

## Regulatory Awareness Note

**FUTURE_COMPLIANCE_REFERENCE only — not current obligations:**

These considerations are documented to prevent architectural drift.
MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated
trading venue. Nothing in this framework creates current legal obligations, regulated status,
compliance claims, or trading enablement.

For future reference: ESMA has restricted retail leverage for CFDs across asset classes.
Relevant national supervisors (e.g., BaFin) have intensified scrutiny of retail leverage
instruments. Any future product offering to retail clients requires explicit regulatory
analysis and compliance review — this framework does not provide that analysis.

## Derivative Gate Dimensions

| Field | Description |
|-------|-------------|
| `derivative_review_allowed` | Boolean: underlying confirmed, market gate AKTIV or SELEKTIV |
| `underlying_confirmed` | Boolean: underlying asset is SAI-qualified and regime-appropriate |
| `product_spread_status` | Whether spread is acceptable for product type |
| `time_to_expiry_status` | Whether time horizon is appropriate |
| `strike_distance_status` | Whether strike level has adequate buffer |
| `knockout_distance_status` | Whether knockout/barrier level has adequate buffer |
| `derivative_risk_class` | Product risk level classification |
| `stop_defined` | Whether a stop loss is defined at the underlying level |
| `target_defined` | Whether a price target is defined at the underlying level |
| `invalid_level_defined` | Whether the setup invalidation level is defined |
| `product_mechanics_status` | Whether leverage product mechanics are understood and appropriate |
| `derivative_trade_ready` | Boolean: all derivative gates pass; product review complete |

## Distinction: derivative_review_allowed vs. derivative_trade_ready

`derivative_review_allowed = true` means:
underlying confirmed, market structure supports review, no hard blocks.

`derivative_trade_ready = true` means:
all derivative-specific gates (spread, expiry, strike/KO distance, mechanics,
stop, target, invalid level) have been individually assessed and confirmed.

A leverage product may only be considered for inclusion in a Human Execution Package
after `derivative_trade_ready = true`. Even then, it requires human approval.

## Hard Rule

When market_ampel = `DEFENSIV`:
- `derivative_review_allowed = false`
- New long leverage instruments are blocked
- This is a hard block, not a soft suggestion

---

# EXECUTION READINESS STATUS

## Status Values

| execution_readiness_status | Meaning |
|---------------------------|---------|
| `WAIT` | Gates not satisfied; no entry setup ready |
| `LIMIT_READY` | Entry setup confirmed; limit price determined; awaiting price level trigger |
| `HUMAN_APPROVAL_REQUIRED` | Setup confirmed and within risk parameters; human decision required before any action |
| `EXECUTED_EXTERNAL` | Human has executed outside the system; status recorded for audit trail (not a system action) |
| `BLOCKED` | One or more gates hard-blocked (e.g., DEFENSIV market_ampel, derivative_review_allowed = false) |
| `EXPIRED` | Setup was valid but price action has passed the valid entry window |

## What MoneyHorst May Conclude

MoneyHorst MAY say:

```
Setup is confirmed / not confirmed.
Entry type is BREAKOUT / PULLBACK.
Market ampel is AKTIV / SELEKTIV / DEFENSIV.
Risk and product gates are satisfied / not satisfied.
Human Approval required.
Action Space remains open.
```

MoneyHorst must NEVER say:

```
Buy.
```

---

# HUMAN EXECUTION PACKAGE

The Human Execution Package is the structured output of this framework.
It is never an order. It is never an instruction. It is a reasoning package for human decision.

## Human Execution Package Contents

| Section | Content |
|---------|---------|
| Market Gate Summary | market_ampel, market_ampel_reason, regime_state_source |
| Technical Entry Summary | entry_type, entry_trigger, breakout_level / pullback_support, invalid_level, technical_confidence, signal_conflict_flags |
| Portfolio Fit Summary | asset_quality_score, portfolio_fit_status, dependency_conflict_flag, concentration_conflict_flag |
| Risk Summary | risk_per_trade_eur, risk_budget_available_eur, position_size, speculation_budget_bucket |
| Derivative Summary (if applicable) | derivative_review_allowed, derivative_trade_ready, product_mechanics_status |
| Execution Readiness | execution_readiness_status, blocked_reason, valid_until |
| Human Decision | human_approval_required = true (always); order_type_allowed; limit_price_reference |
| Action Space Options | Option A, Option B, Option C with rationale and tradeoffs |

## human_approval_required

`human_approval_required` is always `true`.

This field is structural. It reflects that Portfolio OS is a PM reasoning system,
not an autonomous investment AI. The human remains the final allocator,
final risk owner, and final execution authority.

This field is never `false`.

---

# INTEGRATION WITH EXISTING FRAMEWORKS

## Opportunity Engine

The Opportunity Engine determines whether an asset is a structural opportunity.
This framework receives `opportunity_score` and `portfolio_fit_status` as inputs.
The entry gate only triggers for assets already qualified by the Opportunity Engine.
No opportunity re-evaluation occurs here.

## Deployment Intelligence Framework

The Deployment Intelligence Framework determines deployment posture:
`deployment_underinvested`, `deployment_balanced`, `deployment_fully_extended`, `deployment_fragile`.
This framework is downstream of the Deployment Intelligence Framework.
`deployment_fully_extended` restricts position sizing.
`deployment_fragile` may block new entries depending on dependency_conflict_flag.

## Market Regime Framework

This framework derives market_ampel from the Market Regime Framework signals.
It does NOT create an independent regime interpretation.
The Market Regime Framework remains the single source of regime truth.

## SAI (Single Asset Intelligence)

Asset quality, valuation context, financial stability, earnings quality, and peer comparison
are produced by the 24 SAI analysis blocks. This framework receives SAI outputs as inputs.
It does not re-run SAI analysis.

## Portfolio Health Framework

Portfolio fit context (concentration contribution, dependency overlap, macro sensitivity)
is produced by the Portfolio Health Framework.
This framework receives portfolio_fit_status as an input.
It does not duplicate portfolio health logic.

## Signal Hierarchy Respect

Tactical momentum is signal rank 9.
This framework never overrides structural signals (ranks 1–8).
If structural signals (regime, liquidity, breadth, cross-asset) indicate risk,
this framework's output is BLOCKED or WAIT regardless of entry signal strength.

---

# FUTURE SPEC: tactical-momentum-execution-gate-framework

This document is the architectural SSOT defining scope, field vocabulary,
and governance rules for the Tactical Momentum Execution Gate Framework.

The full framework implementation requires a dedicated spec:
`.kiro/specs/tactical-momentum-execution-gate-framework/`

That spec must produce:
- requirements.md: formalized requirements for all gate dimensions
- design.md: methodology chain, data model, field taxonomy, component interfaces
- tasks.md: documentation and verification tasks (definition-layer only in v1)

The spec must NOT:
- Create runtime trading code
- Connect to any broker, exchange, or ATS
- Create order routing logic
- Create execution logic
- Create pre-trade controls (those are FUTURE_COMPLIANCE_REFERENCE vocabulary)
- Claim regulatory compliance

The spec must begin with a preflight / requirements phase, not implementation.

---

# WHAT THIS FRAMEWORK DOES NOT DO

| Prohibition | Reason |
|-------------|--------|
| Generate buy/sell orders | MoneyHorst is not a regulated trading entity |
| Connect to brokers, exchanges, or ATSs | No trading venue connectivity |
| Execute trades or route orders | Execution authority remains with the human |
| Define opportunity quality | That is the Opportunity Engine domain |
| Define asset quality | That is SAI domain |
| Define portfolio health | That is the Portfolio Health Framework domain |
| Define market regime | That is the Market Regime Framework domain |
| Create a second, parallel market interpretation | market_ampel is derived, not independent |
| Define absolute position sizes | Position sizing requires Position Sizing Governance |
| Grant regulatory compliance | Nothing here creates regulated-entity status |
| Claim derivative suitability for the client | Suitability requires regulatory analysis outside this framework |
| Produce probability estimates | Confidence is signal alignment, not probability of outcome |

---

# FUTURE TRADING READINESS

If MoneyHorst activates trading functionality in the future, this framework must be extended
with the following fields (defined in the system trading governance boundary vocabulary):

- `pre_trade_controls` (price collars, max order value, max order volume, message throttles)
- `execution_venue_eligible`
- `best_execution_policy` (FINRA Rule 5310 / MiFID II Art. 27)
- `kill_switch`
- `audit_log`
- `surveillance` and market abuse monitoring
- client suitability assessment for leverage products

All trading fields are `FUTURE_COMPLIANCE_REFERENCE` only.
They are reserved vocabulary, not current obligations.

MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated
trading venue. None of these fields are active until explicit regulatory, technical,
and governance activation occurs through the three-gate model:
1. Regulatory Status Gate
2. Jurisdiction Gate
3. Implementation Gate

---

# GOVERNANCE RULES

1. Signals determine entry truth — semantics determine entry meaning.
2. market_ampel is derived, never independently estimated.
3. entry_type is BREAKOUT, PULLBACK, or NONE — no other values.
4. execution_readiness_status is never "Buy" or any equivalent command.
5. human_approval_required is always true.
6. Tactical momentum is rank 9 — structural conditions always dominate.
7. DEFENSIV market_ampel is a hard block for new long leverage instruments.
8. All derivative gates must pass before derivative_trade_ready = true.
9. derivative_trade_ready = true does not authorize execution — only human review.
10. Budget parameters are policy configuration, not engine constants.
11. No allocation decision may originate from this framework.
12. Every output must remain explainable and signal-traceable.

---

# FRAMEWORK PHILOSOPHY

The Tactical Momentum Execution Gate Framework exists to give tactical precision
to assets that have already earned their place in the Human Execution Package
through fundamental, regime, and portfolio-fit qualification.

It does not create opportunities.
It does not override structure.
It does not execute decisions.

It creates one clear, explainable answer to one clean question:

Given everything Portfolio OS knows about this asset, this portfolio,
and this market — is the entry timing clean enough to prepare
a reasoning package for human decision?

The answer is one of six states.
The action remains with the human.

---

*End of framework.*
