---
artifact_id: semantic_signal_registry_md
primary_domain: SIGNALS
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2024-03-20
last_modified: 2026-05-25
owner_role: Defines canonical semantic states and signal vocabulary
ssot_relationship: canonical
topic: semantic_signals
allowed_writers: [SIGNALS]
allowed_readers: [ALL]
dependencies: [system_architecture_md]
---

# PORTFOLIO OS — SEMANTIC SIGNAL REGISTRY
Version: v1
Status: Canonical Semantic SSOT

---

# PURPOSE

This document defines the official semantic states of Portfolio OS.

Semantic signals are:

- language-independent
- deterministic
- explainable
- reusable
- traceable

Semantic signals represent the canonical system truth.

Reports, dashboards, translations, and PM reasoning must use these signals.

The system must NEVER generate reasoning directly from raw numbers.

The system must first generate semantic meaning.

---

# SEMANTIC SIGNAL STRUCTURE

Every semantic signal must contain:

1. signal_id
2. category
3. meaning
4. signal_origin
5. reasoning_impact
6. confidence_behavior

---

# SIGNAL CATEGORIES

Portfolio OS currently uses these semantic domains:

- market_regime
- liquidity
- breadth
- volatility
- allocation
- concentration
- correlation
- narrative_dependency
- momentum
- deployment
- scenario
- portfolio_health
- participation
- risk_structure

---

# MARKET REGIME SIGNALS

---

## market_regime_neutral

Category:
market_regime

Meaning:
Market conditions remain balanced.
No strong risk-on or risk-off structure detected.

Signal Origin:
- regime_engine
- cross_asset_engine

Reasoning Impact:
Selective positioning becomes more important.

Confidence Behavior:
Confidence increases when:
- volatility stable
- liquidity stable
- breadth stable

---

## market_regime_risk_on

Category:
market_regime

Meaning:
Market participation supports risk assets.

Signal Origin:
- regime_engine
- breadth_engine
- liquidity_engine

Reasoning Impact:
Growth exposure becomes structurally supported.

Confidence Behavior:
Confidence increases when:
- breadth broad
- yields stable
- liquidity supportive

---

## market_regime_risk_off

Category:
market_regime

Meaning:
Defensive positioning dominates market structure.

Signal Origin:
- volatility_engine
- cross_asset_engine
- liquidity_engine

Reasoning Impact:
Portfolio resilience becomes more important than growth exposure.

Confidence Behavior:
Confidence increases when:
- volatility elevated
- yields unstable
- breadth weak

---

# CONCENTRATION SIGNALS

---

## concentration_risk_elevated

Category:
concentration

Meaning:
Portfolio exposure depends heavily on a limited number of positions, sectors, or narratives.

Signal Origin:
- allocation_engine
- correlation_engine
- scenario_engine

Reasoning Impact:
Portfolio drawdown sensitivity increases.

Confidence Behavior:
Confidence increases when:
- top holdings dominate allocation
- correlations rise
- narrative overlap increases

---

## concentration_risk_extreme

Category:
concentration

Meaning:
Portfolio exposure is highly dependent on a small number of drivers.

Signal Origin:
- allocation_engine
- scenario_engine
- narrative_dependency_engine

Reasoning Impact:
Single-theme weakness may disproportionately impact total portfolio performance.

Confidence Behavior:
Confidence increases when:
- top allocation exceeds thresholds
- scenario fragility rises
- diversification weakens

---

# NARRATIVE DEPENDENCY SIGNALS

---

## ai_dependency_high

Category:
narrative_dependency

Meaning:
Portfolio performance strongly depends on continued AI-related market leadership.

Signal Origin:
- allocation_engine
- attribution_engine
- correlation_engine

Reasoning Impact:
Portfolio upside remains strong if AI leadership continues,
but dependency risk rises if AI expectations weaken.

Confidence Behavior:
Confidence increases when:
- AI exposure concentrated
- semiconductors dominate
- growth correlation rises

---

## defense_dependency_elevated

Category:
narrative_dependency

Meaning:
Portfolio performance increasingly depends on continued defense-sector strength.

Signal Origin:
- allocation_engine
- attribution_engine

Reasoning Impact:
Portfolio becomes more sensitive to geopolitical and macro-defense narratives.

Confidence Behavior:
Confidence increases when:
- defense allocation dominant
- defense momentum persistent

---

# LIQUIDITY SIGNALS

---

## supportive_liquidity

Category:
liquidity

Meaning:
Liquidity conditions continue supporting risk assets.

Signal Origin:
- liquidity_engine
- cross_asset_engine

Reasoning Impact:
Higher-quality growth exposure remains structurally supported.

Confidence Behavior:
Confidence increases when:
- credit stable
- yields controlled
- volatility contained

---

## deteriorating_liquidity

Category:
liquidity

Meaning:
Liquidity conditions weaken and may pressure risk assets.

Signal Origin:
- liquidity_engine
- volatility_engine

Reasoning Impact:
Portfolio resilience and diversification become increasingly important.

Confidence Behavior:
Confidence increases when:
- yields rise
- volatility rises
- credit spreads widen

---

# BREADTH SIGNALS

---

## participation_broad

Category:
breadth

Meaning:
Market participation remains healthy across sectors and assets.

Signal Origin:
- breadth_engine

Reasoning Impact:
Current market moves appear structurally healthier.

Confidence Behavior:
Confidence increases when:
- multiple sectors participate
- index leadership broadens

---

## participation_narrow

Category:
breadth

Meaning:
Market performance depends on a limited number of leaders.

Signal Origin:
- breadth_engine
- attribution_engine

Reasoning Impact:
Market fragility increases beneath headline index strength.

Confidence Behavior:
Confidence increases when:
- leadership concentrated
- index divergence rises

---

# DEPLOYMENT SIGNALS

---

## deployment_underinvested

Category:
deployment

Meaning:
Portfolio maintains unusually high cash relative to invested capital.

Signal Origin:
- allocation_engine
- capital_engine

Reasoning Impact:
Future deployment flexibility remains high.

Confidence Behavior:
Confidence increases when:
- cash ratio elevated
- portfolio exposure low

---

## deployment_fully_extended

Category:
deployment

Meaning:
Portfolio currently maintains very high invested exposure.

Signal Origin:
- allocation_engine
- capital_engine

Reasoning Impact:
Future flexibility decreases while exposure sensitivity rises.

Confidence Behavior:
Confidence increases when:
- cash low
- concentration elevated

---

# PORTFOLIO HEALTH SIGNALS

---

## portfolio_health_stable

Category:
portfolio_health

Meaning:
Portfolio structure currently remains balanced and resilient.

Signal Origin:
- allocation_engine
- scenario_engine
- breadth_engine

Reasoning Impact:
Current positioning appears structurally sustainable.

Confidence Behavior:
Confidence increases when:
- concentration controlled
- diversification healthy
- scenarios stable

---

## portfolio_health_fragile

Category:
portfolio_health

Meaning:
Portfolio structure may become vulnerable under stress scenarios.

Signal Origin:
- scenario_engine
- correlation_engine
- concentration_engine

Reasoning Impact:
Risk management and exposure discipline become increasingly important.

Confidence Behavior:
Confidence increases when:
- concentration elevated
- scenarios weak
- diversification poor

---

# SEMANTIC GOVERNANCE RULES

1. Semantic signals are language-independent.
2. Reports may only interpret existing semantic signals.
3. Raw data may never bypass semantic interpretation.
4. Signals must remain explainable.
5. Signals must remain deterministic.
6. Signals must remain reusable across reports and dashboards.
7. Multiple engines may confirm the same semantic signal.
8. Semantic signals are the official PM reasoning vocabulary.

---

# HUMAN READABILITY PRINCIPLE

Portfolio OS exists to explain portfolio reality clearly.

The system must always prioritize understanding over sophistication.

The report must be understandable by:

- normal investors
- non-professional users
- long-term investors
- users without institutional vocabulary

Complexity may exist internally.

Explanation must remain simple externally.

---

# EXPLANATION RULES

The report must always explain:

- why something matters
- what causes a signal
- what the consequence could be
- what changes the user should understand

The system must NEVER assume the user understands:

- market jargon
- PM terminology
- institutional language
- macro shorthand

Every important conclusion must be explainable in plain language.

---

# FORBIDDEN REPORT BEHAVIOR

The report must NEVER:

- sound artificially intelligent
- imitate financial television
- imitate hedge fund language
- use complexity to appear sophisticated
- hide weak reasoning behind jargon

If a sentence sounds impressive but explains nothing,
it should be removed.

---

# GOOD EXPLANATION EXAMPLES

Bad:

"Portfolio concentration risk elevated."

Good:

"A large part of your portfolio currently depends
on only a few sectors continuing to perform well."

---

Bad:

"Liquidity conditions deteriorating."

Good:

"Markets may become less supportive for risk assets
if borrowing conditions continue tightening."

---

Bad:

"Participation narrow."

Good:

"Current market strength is driven by only a small
group of companies instead of broad market participation."

---

# REPORT COMMUNICATION PRINCIPLE

The report should feel like:

- a thoughtful PM explanation
- a calm institutional briefing
- an intelligent portfolio conversation

The report should NOT feel like:

- AI-generated text
- market news spam
- financial influencer language
- fear-based commentary

---

# ACCESSIBILITY PRIORITY

Clarity always dominates sophistication.

If forced to choose between:

- sounding intelligent
or
- being understandable

the system must always choose understanding.

Explainability is the product.
---

# LONG-TERM REGISTRY EXPANSION

Future semantic domains may include:

- sentiment
- macro stress
- valuation pressure
- positioning crowding
- earnings quality
- policy sensitivity
- geopolitical exposure
- FX dependency
- commodity dependency
- rate sensitivity

All future signals must follow the same semantic structure.
