---
artifact_id: engine_design_principles_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2024-02-10
last_modified: 2026-05-25
owner_role: Defines engine design patterns and modularity principles
ssot_relationship: canonical
topic: engine_design
allowed_writers: [ARCH]
allowed_readers: [ALL]
dependencies: [system_architecture_md]
---

# PORTFOLIO OS — ENGINE DESIGN PRINCIPLES
Version: v1
Status: Active Engineering SSOT

---

# PURPOSE

This document defines how engines inside Portfolio OS must be designed.

The goal is to ensure:

- explainability
- modularity
- deterministic behavior
- semantic consistency
- stable reasoning architecture

Portfolio OS is a signal orchestration system.

Engines must generate structured intelligence,
not uncontrolled narrative.

---

# CORE PRINCIPLE

Each engine must have exactly ONE responsibility.

Engines must remain:

- focused
- explainable
- deterministic
- composable

Engines must NEVER become:

- multi-purpose AI blobs
- narrative generators
- uncontrolled reasoning systems

---

# ENGINE RESPONSIBILITY MODEL

Every engine must answer ONE question only.

Examples:

Allocation Engine:
"What does the portfolio currently look like?"

Regime Engine:
"What market regime currently exists?"

Breadth Engine:
"How broad is market participation?"

Liquidity Engine:
"How supportive are liquidity conditions?"

Correlation Engine:
"Which dependencies dominate?"

Scenario Engine:
"What stress conditions matter?"

Attribution Engine:
"What currently drives portfolio behavior?"

---

# ENGINE OUTPUT RULE

Engines must produce:

- signals
- measurements
- classifications
- semantic candidates

Engines must NOT produce:

- final PM conclusions
- emotional narrative
- broad recommendations
- financial storytelling

Reasoning belongs to the PM reasoning layer.

---

# ENGINE OUTPUT STRUCTURE

Engine outputs should remain structured.

Preferred outputs:

- dictionaries
- semantic states
- scored outputs
- classified outputs
- measurable conditions

Avoid:

- uncontrolled text blocks
- vague summaries
- natural-language-heavy outputs

---

# ENGINE CHAIN

Portfolio OS follows this chain:

Raw Data
→ Signal Engine
→ Semantic Interpretation
→ PM Reasoning
→ Report Rendering

No engine may bypass this structure.

---

# ENGINE TYPES

Portfolio OS uses multiple engine classes.

---

# TYPE 1 — RAW SIGNAL ENGINES

Purpose:
Generate measurable conditions.

Examples:

- allocation_engine
- liquidity_engine
- breadth_engine
- volatility_engine

Output:
Raw or semi-structured signals.

---

# TYPE 2 — INTERPRETATION ENGINES

Purpose:
Transform signals into semantic states.

Examples:

- semantic_mapper
- concentration_interpreter
- narrative_dependency_interpreter

Output:
Semantic portfolio meaning.

---

# TYPE 3 — PM REASONING ENGINES

Purpose:
Explain semantic meaning.

Examples:

- report_reasoning_engine
- action_space_engine
- scenario_reasoning_engine

Output:
Explainable PM interpretation.

---

# TYPE 4 — RENDERING ENGINES

Purpose:
Transform PM reasoning into presentation.

Examples:

- report_renderer_en
- report_renderer_de
- dashboard_renderer

Output:
Human-readable presentation.

---

# ENGINE ISOLATION RULE

Engines must remain isolated by responsibility.

Example:

Allocation Engine must NOT:

- interpret macro conditions
- generate PM commentary
- generate narrative

Regime Engine must NOT:

- interpret position sizing
- suggest trades
- generate allocation actions

This prevents logic drift.

---

# SEMANTIC GOVERNANCE RULE

Engines must use official semantic states.

Engines may NOT invent:

- ad-hoc labels
- inconsistent terminology
- duplicate semantic meanings

All semantics must originate from:

semantic_signal_registry.md

---

# LANGUAGE GOVERNANCE RULE

Engines must remain language-independent whenever possible.

Business logic must NEVER depend on:

- English wording
- German wording
- report phrasing

Meaning must exist before language rendering.

---

# DETERMINISM RULE

Engines must remain deterministic.

Given identical inputs,
engines should produce identical outputs.

The system must avoid:

- random reasoning
- unstable interpretation
- emotional variability
- inconsistent conclusions

Explainability requires stability.

---

# CROSS-ENGINE VALIDATION

Important conclusions should ideally be confirmed by multiple engines.

Example:

Concentration risk may be confirmed by:

- allocation_engine
- correlation_engine
- scenario_engine
- narrative_dependency_engine

Confidence increases through alignment.

---

# ENGINE COMPLEXITY RULE

Simple engines are preferred over giant engines.

Portfolio OS should favor:

- many explainable components
instead of
- few opaque components

Complexity should emerge through orchestration,
not through monolithic logic.

---

# ENGINE FAILURE PRINCIPLE

Engines should fail gracefully.

If one engine fails:

- the portfolio state should survive
- reports should degrade safely
- dashboards should remain operational

No single engine should collapse the entire system.

---

# REPORT RELATIONSHIP

Reports do NOT replace engines.

Reports synthesize engine outputs.

Reports are downstream reasoning products.

Engines remain the canonical truth generators.

---

# FUTURE ENGINE EXPANSION

Future engine classes may include:

- valuation_engine
- sentiment_engine
- options_flow_engine
- macro_stress_engine
- earnings_quality_engine
- deployment_engine
- opportunity_engine
- thesis_engine
- behavioral_engine

All future engines must follow the same principles.

---

# ENGINE DESIGN PHILOSOPHY

Portfolio OS is not designed to simulate intelligence.

Portfolio OS is designed to:

- structure signals
- explain portfolio reality
- reduce ambiguity
- support PM reasoning
- make portfolio conditions understandable

Clarity dominates sophistication.