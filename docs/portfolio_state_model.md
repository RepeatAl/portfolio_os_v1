---
artifact_id: portfolio_state_model_md
primary_domain: STATE
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2024-05-20
last_modified: 2026-05-25
owner_role: Defines canonical portfolio state structure and hierarchy
ssot_relationship: canonical
topic: portfolio_state
allowed_writers: [STATE]
allowed_readers: [ALL]
dependencies: [system_architecture_md]
---

# PORTFOLIO OS — PORTFOLIO STATE MODEL
Version: v1
Status: Canonical Portfolio SSOT

---

# PURPOSE

This document defines the official portfolio state structure of Portfolio OS.

The portfolio state is the canonical representation of:

- positions
- exposure
- capital
- portfolio structure
- dependencies
- allocation
- risk distribution
- portfolio conditions

All engines, reports, simulations, and dashboards must reference this structure.

No component may create its own portfolio truth.

---

# CORE PRINCIPLE

Portfolio state is NOT:

- a spreadsheet
- a watchlist
- a dashboard table

Portfolio state is a structured representation of portfolio reality.

The portfolio state represents:

- what the user owns
- what drives the portfolio
- what risks dominate
- what narratives dominate
- how capital is deployed
- how resilient the structure is

---

# PORTFOLIO STATE HIERARCHY

Portfolio OS uses 4 portfolio-state layers.

---

# LAYER 1 — POSITION STATE

Purpose:
Represent individual holdings.

Each position contains:

- ticker
- quantity
- entry price
- current price
- market value
- category
- sector
- currency
- allocation weight
- unrealized P/L
- thesis
- conviction level
- risk classification

Examples:

- Microsoft
- NVIDIA
- Rheinmetall
- ASML

This is the atomic portfolio layer.

---

# LAYER 2 — EXPOSURE STATE

Purpose:
Represent aggregated exposure structures.

Examples:

- sector exposure
- geographic exposure
- currency exposure
- thematic exposure
- AI exposure
- defense exposure
- semiconductor exposure

Exposure state explains:

"What currently drives portfolio behavior?"

---

# LAYER 3 — CAPITAL STATE

Purpose:
Represent capital deployment conditions.

Examples:

- invested capital
- cash position
- deployment ratio
- deployment flexibility
- idle capital
- capital efficiency

Capital state explains:

"How much flexibility currently exists?"

---

# LAYER 4 — STRUCTURAL STATE

Purpose:
Represent portfolio architecture and resilience.

Examples:

- concentration risk
- diversification quality
- dependency risk
- narrative fragility
- correlation structure
- scenario vulnerability
- liquidity sensitivity

Structural state explains:

"How stable is the portfolio under changing conditions?"

---

# POSITION STATE RULES

Every position must contain:

1. Identity
2. Exposure
3. Value
4. Thesis
5. Risk
6. Allocation impact

The system must NEVER treat positions as isolated assets.

Every position must be interpreted in portfolio context.

Example:

Microsoft alone is not the risk.

Portfolio dependency on a limited number of growth drivers may become the risk.

---

# EXPOSURE MODEL

Exposure is NOT limited to sectors.

Portfolio OS recognizes multiple exposure dimensions:

- sector exposure
- narrative exposure
- macro exposure
- rate sensitivity
- liquidity sensitivity
- geographic concentration
- currency dependency

A portfolio may appear diversified by sector,
while remaining highly concentrated by narrative.

Example:

AI infrastructure
Semiconductors
Cloud AI

may all depend on the same macro driver.

---

# CAPITAL MODEL

Capital is treated as strategic flexibility.

Cash is NOT automatically considered negative.

High cash may represent:

- deployment flexibility
- defensive posture
- uncertainty management
- optionality

The system must interpret capital contextually.

---

# RISK MODEL

Portfolio risk is NOT asset quality.

Portfolio risk represents:

- structural fragility
- concentration
- dependency overlap
- scenario sensitivity
- diversification weakness

A portfolio of high-quality companies may still create elevated structural risk.

---

# PORTFOLIO HEALTH MODEL

Portfolio health represents:

- resilience
- diversification
- flexibility
- dependency structure
- scenario stability

Portfolio health does NOT represent short-term performance.

The system must avoid performance-chasing logic.

---

# PORTFOLIO MEMORY PRINCIPLE

The portfolio state should evolve historically over time.

Future phases may track:

- historical positioning
- allocation changes
- exposure shifts
- deployment behavior
- scenario transitions
- PM decisions

Portfolio state is intended to become longitudinal.

---

# WATCHLIST RELATIONSHIP

Watchlist state is NOT portfolio state.

Watchlists represent:

- potential future exposure
- opportunity monitoring
- deployment candidates
- future capital options

Portfolio state represents current exposure reality.

---

# SIMULATION RELATIONSHIP

All simulations must derive from portfolio state.

Examples:

- what happens if exposure changes
- what happens if capital deploys
- what happens under stress scenarios
- what happens under narrative breakdown

No simulation may bypass canonical portfolio state.

---

# GOVERNANCE RULES

1. Portfolio state is the single source of truth.
2. Engines may interpret portfolio state, not replace it.
3. Reports may explain portfolio state, not invent it.
4. Dashboards visualize portfolio state.
5. Simulations derive from portfolio state.
6. Exposure always matters more than isolated assets.
7. Structural risk dominates short-term noise.

---

# LONG-TERM STATE EVOLUTION

Future portfolio state extensions may include:

- transaction history
- realized gains
- tax exposure
- portfolio journaling
- thesis tracking
- conviction scoring
- behavioral tracking
- allocation history
- macro sensitivity
- stress-test persistence

All future extensions must remain compatible with canonical portfolio state.