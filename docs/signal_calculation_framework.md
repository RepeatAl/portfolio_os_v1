---
artifact_id: signal_calculation_framework_md
primary_domain: SIGNALS
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2024-04-05
last_modified: 2026-05-25
owner_role: Defines signal calculation rules and threshold governance
ssot_relationship: canonical
topic: signal_calculation
allowed_writers: [SIGNALS]
allowed_readers: [ALL]
dependencies: [semantic_signal_registry_md]
---

# PORTFOLIO OS — SIGNAL CALCULATION FRAMEWORK

Version: v1
Status: Canonical Signal Calculation SSOT

---

# PURPOSE

This document defines how Portfolio OS calculates signals.

Portfolio OS is NOT a narrative-first system.

Portfolio OS is a deterministic signal system.

This framework defines:

* signal calculation rules
* threshold governance
* scoring normalization
* signal validation
* cross-engine consistency
* semantic trigger conditions

The goal is:

* stable reasoning
* explainable semantics
* reproducible outputs
* deterministic PM interpretation

---

# CORE PRINCIPLE

Signals must emerge from measurable conditions.

Signals must NEVER emerge from:

* intuition
* AI improvisation
* vague interpretation
* narrative preference
* emotional framing

The system must always follow:

Raw Data
→ Calculation
→ Threshold Evaluation
→ Semantic Trigger
→ PM Reasoning

---

# SIGNAL CALCULATION OBJECTIVE

The framework should answer:

* when a signal activates
* why a signal activates
* how strongly a signal activates
* which engines confirm the signal
* how signal confidence changes
* how conflicts are handled

The framework creates:

deterministic semantic truth.

---

# SIGNAL CALCULATION LAYERS

Portfolio OS uses 5 signal-calculation layers.

---

# LAYER 1 — RAW DATA INPUT

Purpose:
Collect measurable conditions.

Examples:

* allocation %
* volatility
* sector exposure
* breadth metrics
* yields
* VIX
* liquidity metrics
* correlation coefficients
* cash ratio
* deployment ratio

This layer contains NO interpretation.

---

# LAYER 2 — DERIVED CALCULATIONS

Purpose:
Generate structural metrics.

Examples:

* top-3 concentration
* AI narrative exposure
* sector overlap ratio
* deployment rigidity
* breadth participation score
* liquidity pressure score
* diversification quality score

Derived calculations are still NOT semantics.

They are measurable structural conditions.

---

# LAYER 3 — THRESHOLD EVALUATION

Purpose:
Evaluate whether conditions exceed structural boundaries.

Examples:

Concentration:

* LOW
* MODERATE
* ELEVATED
* EXTREME

Breadth:

* BROAD
* NEUTRAL
* NARROW

Liquidity:

* SUPPORTIVE
* MIXED
* DETERIORATING

Thresholds create semantic eligibility.

---

# LAYER 4 — SEMANTIC TRIGGERING

Purpose:
Activate official semantic states.

Examples:

If:

* AI Exposure > 45%
  AND
* Semiconductor Correlation High

Then:

* ai_dependency_high

---

If:

* Top Position > 20%
  OR
* Top 3 Positions > 55%

Then:

* concentration_risk_elevated

---

# LAYER 5 — CROSS-ENGINE VALIDATION

Purpose:
Confirm semantic stability.

Example:

concentration_risk_elevated may require confirmation from:

* allocation_engine
* correlation_engine
* scenario_engine

Confidence increases through multi-engine alignment.

---

# SIGNAL DESIGN PRINCIPLE

Signals must remain:

* deterministic
* explainable
* measurable
* stable
* traceable

Signals must NEVER become:

* subjective
* emotional
* narrative-dependent
* AI-generated opinions

---

# THRESHOLD GOVERNANCE

Thresholds represent structural boundaries.

Thresholds are NOT arbitrary numbers.

Thresholds should reflect:

* portfolio fragility
* diversification breakdown
* liquidity deterioration
* dependency escalation
* regime instability

Thresholds must remain:

* explainable
* reviewable
* versioned
* stable

---

# CONCENTRATION CALCULATION MODEL

Example framework:

---

## concentration_risk_low

Conditions:

* largest position < 10%
* top 3 positions < 35%

Meaning:

Portfolio concentration structurally manageable.

---

## concentration_risk_moderate

Conditions:

* largest position between 10–20%
  OR
* top 3 positions between 35–50%

Meaning:

Concentration increasing,
but diversification remains functional.

---

## concentration_risk_elevated

Conditions:

* largest position > 20%
  OR
* top 3 positions > 50%

Meaning:

Portfolio increasingly depends on limited drivers.

---

## concentration_risk_extreme

Conditions:

* largest position > 35%
  OR
* top 3 positions > 70%

Meaning:

Portfolio structurally fragile under stress.

---

# DEPLOYMENT CALCULATION MODEL

---

## deployment_underinvested

Conditions:

* cash ratio > 40%

Meaning:

Portfolio preserves strong flexibility.

---

## deployment_balanced

Conditions:

* cash ratio between 15–40%

Meaning:

Balanced participation and optionality.

---

## deployment_fully_extended

Conditions:

* cash ratio < 15%

Meaning:

High exposure with reduced flexibility.

---

# BREADTH CALCULATION MODEL

Example indicators:

* advancing vs declining sectors
* equal-weight vs cap-weight divergence
* index participation quality

---

## participation_broad

Conditions:

* broad sector participation
* equal-weight confirmation healthy

Meaning:

Market participation structurally healthy.

---

## participation_narrow

Conditions:

* leadership concentrated
* weak broad participation

Meaning:

Market strength increasingly dependent on limited leaders.

---

# LIQUIDITY CALCULATION MODEL

Example inputs:

* yield movement
* volatility trend
* credit spreads
* liquidity proxies

---

## supportive_liquidity

Conditions:

* stable yields
* controlled volatility
* stable credit conditions

Meaning:

Markets structurally support risk assets.

---

## deteriorating_liquidity

Conditions:

* rising yields
* widening spreads
* rising volatility

Meaning:

Financial conditions weakening.

---

# DEPENDENCY CALCULATION MODEL

Dependency should evaluate:

* thematic overlap
* narrative overlap
* macro overlap
* correlation overlap

Example:

If:

* AI exposure high
  AND
* semiconductor overlap elevated
  AND
* growth correlation high

Then:

* ai_dependency_high

---

# SIGNAL WEIGHTING RULE

Not all signals carry equal importance.

Priority order:

1. Structural fragility
2. Liquidity deterioration
3. Correlation escalation
4. Breadth weakness
5. Narrative dependency
6. Tactical momentum
7. News sentiment

Structural signals dominate tactical signals.

---

# SIGNAL CONFLICT RULE

Conflicting signals reduce confidence.

Example:

* supportive_liquidity
  BUT
* participation_narrow
  AND
* rising_volatility

Result:

* reduced confidence
* wider action-space
* fragile regime classification

The system must NEVER force certainty.

---

# SIGNAL STABILITY RULE

Signals should avoid excessive flipping.

The system should prefer:

* structural persistence
  over
* hypersensitive short-term noise

Example:

Temporary volatility spikes should not instantly trigger:

market_regime_risk_off

without broader confirmation.

---

# SIGNAL VERSIONING RULE

Threshold logic must remain version-controlled.

Every major threshold update should track:

* previous thresholds
* new thresholds
* rationale
* expected behavioral change

This preserves reasoning auditability.

---

# SIGNAL TRACEABILITY RULE

Every semantic signal must remain traceable to:

* source data
* calculation method
* threshold condition
* engine origin
* semantic trigger

No semantic state may become a black box.

---

# HUMAN READABILITY RULE

Signal explanations must remain understandable.

The system should explain:

* what triggered the signal
* why the signal matters
* what structurally changed
* what conditions worsened or improved

The user must NEVER see signals as magical AI outputs.

---

# REPORT RELATIONSHIP

Reports interpret signal meaning.

Reports must NEVER invent signals.

Reports should explain:

* why signals activated
* what conditions caused activation
* what implications emerged
* what tradeoffs changed

Signals remain the canonical truth layer.

---

# DASHBOARD RELATIONSHIP

Dashboards visualize:

* signal activation
* threshold escalation
* concentration evolution
* regime transitions
* deployment shifts
* confidence changes

Dashboards visualize signal architecture,
not emotional narratives.

---

# MEMORY RELATIONSHIP

Portfolio memory should eventually preserve:

* historical signal activations
* threshold transitions
* recurring fragility
* persistent dependencies
* regime evolution

The system should remember:

structural behavior over time.

---

# LONG-TERM SIGNAL EVOLUTION

Future signal systems may include:

* adaptive threshold weighting
* volatility-adjusted thresholds
* regime-sensitive calculations
* macro-adjusted scoring
* historical persistence weighting
* dynamic dependency graphs

All future systems must remain:

* explainable
* deterministic
* structurally grounded
* semantically consistent

---

# SIGNAL CALCULATION PHILOSOPHY

Portfolio OS does not generate meaning from AI intuition.

Portfolio OS generates meaning from:

* measurable structure
* deterministic calculations
* semantic interpretation
* cross-engine confirmation

Signals create semantic truth.

Semantic truth creates reasoning.

Reasoning creates understanding.
