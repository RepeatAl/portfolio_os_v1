---
artifact_id: report_reasoning_system_md
primary_domain: REPORT
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2024-05-05
last_modified: 2026-05-25
owner_role: Defines report reasoning orchestration and PM interpretation rules
ssot_relationship: canonical
topic: report_reasoning
allowed_writers: [REPORT]
allowed_readers: [ALL]
dependencies: [semantic_reasoning_rules_md, report_pipeline_architecture_md]
---

# PORTFOLIO OS — REPORT REASONING SYSTEM
Version: v1
Status: Active SSOT

---

# PURPOSE

The report system is not a text generator.

The report system is a portfolio reasoning orchestrator.

Its purpose is to:

- synthesize portfolio signals
- explain portfolio state
- explain market conditions
- explain dependencies
- explain tradeoffs
- explain scenario risks
- explain action space

The report must help the user understand:

- what matters
- why it matters
- what changed
- what risks exist
- what options exist

The report must NEVER generate empty narrative.

---

# PRIMARY REPORT PRINCIPLE

The report must always follow this chain:

Raw Signals
→ Semantic Meaning
→ PM Interpretation
→ Human Language

The report must NEVER skip semantic interpretation.

---

# REPORT OBJECTIVE

The report exists to reduce uncertainty.

The report does NOT exist to:

- predict markets
- generate hype
- create fear
- imitate financial media
- produce generic AI summaries

---

# REPORT STRUCTURE

Every report must contain 4 reasoning layers.

---

# LAYER 1 — MARKET STATE

Purpose:
Explain current market environment.

The report must explain:

- liquidity conditions
- regime conditions
- market breadth
- cross-asset relationships
- volatility environment
- macro participation
- divergence conditions

The report must explain WHY the regime exists.

Bad Example:

"Neutral regime."

Good Example:

"Equities continue rising while yields decline.
Liquidity conditions remain supportive.
No major divergence signals detected.
This creates a stable but selective risk environment."

---

# LAYER 2 — PORTFOLIO STATE

Purpose:
Explain current portfolio structure.

The report must explain:

- concentration
- exposure
- dependency
- narrative exposure
- strongest drivers
- weakest drivers
- capital distribution
- correlation structure

Important:

Portfolio risk is NOT asset quality.

A high-quality company can still create concentration risk.

The report must explain:

- dependency risk
- exposure imbalance
- narrative fragility

NOT:
"Bad asset."

---

# LAYER 3 — DECISION STATE

Purpose:
Explain what currently matters most.

The report must explain:

- why a signal matters
- why concentration matters
- why a scenario matters
- why a regime matters
- why exposure matters

The report must explain consequences.

Bad Example:

"Reduce Semiconductor exposure."

Good Example:

"Semiconductor exposure currently drives
portfolio upside, but also increases dependency
on continued AI-capex strength."

---

# LAYER 4 — ACTION SPACE

Purpose:
Explain possible portfolio actions.

The system must NEVER provide only one action.

The report should generate:

- Option A
- Option B
- Option C

Each option must explain:

- rationale
- tradeoffs
- benefits
- risks
- portfolio implications

Example:

Option A:
Reduce concentration gradually.

Option B:
Redirect future capital toward underrepresented sectors.

Option C:
Maintain current exposure but avoid increasing concentration further.

---

# REPORT LANGUAGE RULES

The report must NEVER use:

- generic AI filler
- dramatic language
- fear-based framing
- vague PM wording
- empty strategic statements

Examples of forbidden wording:

- "remain cautious"
- "monitor closely"
- "volatile environment"
- "stay alert"

unless supported by actual signals.

---

# REPORT STYLE PRINCIPLES

The report must always be:

- explainable
- signal-based
- evidence-based
- concise
- PM-oriented
- tradeoff-aware
- understandable
- non-academic
- non-hype
- non-alarmist

---

# REPORT SEMANTICS

The report must always separate:

1. Asset Quality
2. Portfolio Exposure Risk

Example:

Microsoft may be a high-quality asset.

However:

If Microsoft dominates portfolio exposure,
portfolio dependency risk still rises.

This distinction is mandatory.

---

# REPORT CONFIDENCE

Confidence does NOT mean prediction certainty.

Confidence means:

How strongly current signals align.

High confidence means:

- multiple engines confirm similar conditions
- regime signals align
- allocation signals align
- scenario signals align
- concentration signals align

Low confidence means:

- conflicting signals
- unstable regime
- inconsistent participation
- unclear market structure

---

# REPORT TRANSLATION RULE

Language must NEVER contain business logic.

Business logic belongs to:

- semantic interpretation
- PM reasoning layer

The report must support:

- English
- German
- future multilingual rendering

using the SAME semantic reasoning structure.

Meaning first.
Language second.

---

# LONG-TERM REPORT VISION

Future report system should support:

- daily morning briefing
- weekly PM report
- stress scenario report
- deployment report
- opportunity report
- portfolio posture report
- watchlist intelligence report
- rebalancing report

All reports must use the same reasoning architecture.

---

# REPORT SYSTEM IDENTITY

Portfolio OS reports are:

- explainable
- institutional-style
- signal-driven
- PM-oriented
- reasoning-first

Portfolio OS reports are NOT:

- AI-generated blog text
- market commentary spam
- prediction systems
- trading signal feeds
- emotional narratives