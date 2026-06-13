# MoneyHorst Research Mechanism SSOT

> **Single Source of Truth — Research Mechanism Guidance**
> Scope: MoneyHorst research-system development | Type: Documentation-only guidance | Date: 2026-06-12

---

## 1. Executive Summary

MoneyHorst is not a trading bot.
MoneyHorst is not an autonomous investment AI.

MoneyHorst is an institutional research, signal, evidence, and decision-governance operating system.

AI accelerates research, but does not own the investment decision. Signals, evidence, and human governance decide.

The purpose of this document is to establish durable principles for how MoneyHorst evaluates AI — not as a market story alone, but as a verifiable research-process, evidence-quality, signal-quality, and decision-governance layer.

---

## 2. Morningstar-Derived Lesson

### Key Insight

Morningstar-style institutional analysis evaluates whether AI is actually embedded in research and investment processes, not merely claimed in marketing language.

### Separation Framework

| Dimension | Question |
|-----------|----------|
| AI Claim | What does the company, manager, or narrative assert about AI capabilities? |
| AI Process Evidence | Is there verifiable evidence that AI is integrated into the actual research or investment workflow? |
| AI Investment Relevance | Does the AI integration produce measurable economic outcomes (revenue, margin, efficiency, accuracy)? |
| AI Governance and Human Oversight | Is there a human governance layer that validates, audits, and constrains AI-derived outputs? |

The lesson: AI claims without process evidence are marketing. AI process evidence without investment relevance is experimentation. AI investment relevance without governance is risk. All four dimensions must be present for institutional confidence.

---

## 3. Claim vs Evidence Principle

### Permanent MoneyHorst Rule

Every strong narrative must be split into four components:

| Component | Definition |
|-----------|-----------|
| **Claim** | What the company, manager, analyst, market, or narrative says |
| **Evidence** | What verifiable sources and signals support the claim |
| **Contradictions** | What evidence weakens or disputes the claim |
| **Portfolio Relevance** | Why it matters for allocation, risk, correlation, or thesis quality |

### Enforcement Rule

**No claim may become a MoneyHorst signal without evidence mapping.**

A claim without evidence is a hypothesis. A hypothesis without contradiction analysis is incomplete. An incomplete hypothesis without portfolio relevance assessment has no place in signal generation.

---

## 4. Research Memory Principle

MoneyHorst must preserve historical theses, signal changes, rejected assumptions, analyst notes, source references, and decision context.

The system must be able to answer:

> "What did we believe before, why did we believe it, what changed, and what evidence supports the change?"

### Design Requirements

- Historical thesis preservation: no thesis is deleted; superseded theses are marked with reason and date
- Signal change audit trail: every signal state change records the triggering evidence
- Rejected assumption register: assumptions evaluated and rejected are preserved with rationale
- Source reference durability: sources remain accessible and linked even when conclusions change
- Decision context: the reasoning environment (market conditions, available evidence, confidence level) at time of decision is recorded

**Portfolio Memory is a core system, not an optional note layer.**

---

## 5. Semantic Research Engine Principle

MoneyHorst should use semantic search and semantic signal extraction to identify concepts, not just keywords.

### Example Concepts for Semantic Extraction

| Concept | What It Captures |
|---------|-----------------|
| AI-capex conversion | Whether AI capital expenditure translates into measurable output |
| AI productivity leverage | Degree to which AI amplifies human research capacity |
| Margin impact | Effect on operating or net margins from AI integration |
| Revenue visibility | Whether AI improves revenue forecasting accuracy |
| Pricing power | AI's contribution to pricing authority or competitive moat |
| Customer adoption | Evidence of customer uptake driven by AI features |
| Process integration | Depth of AI embedding in core business workflows |
| Operating leverage | AI-driven scalability of operations without proportional cost |
| Governance maturity | Sophistication of human oversight over AI-derived outputs |
| Evidence density | Volume and quality of verifiable evidence per claim |
| Contradiction density | Volume of counterfactual or conflicting evidence per thesis |

### Design Implication

Keyword matching alone misses conceptual relationships. Semantic extraction enables identification of themes across filings, transcripts, analyst reports, and news — regardless of exact terminology used by the source.

---

## 6. AI Adoption Quality Score

### Purpose

A future scoring model to evaluate thesis quality and AI-process maturity for any asset claiming AI integration. This is not a buy/sell signal by itself. It is a thesis-quality and process-maturity signal.

### Scoring Dimensions

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | Process Integration | How deeply AI is embedded in actual workflows (not demos) |
| 2 | Evidence Density | Volume and quality of verifiable evidence supporting AI claims |
| 3 | Productivity Link | Measurable connection between AI and operational efficiency |
| 4 | Revenue / Monetization Visibility | Evidence that AI contributes to top-line or monetization |
| 5 | Margin / Cost Impact | Measurable margin improvement attributable to AI |
| 6 | Governance and Human Oversight | Presence and maturity of human governance over AI outputs |
| 7 | Infrastructure Depth | Quality and scale of underlying AI infrastructure (data, compute, talent) |
| 8 | Data Advantage | Proprietary or structural data advantages that enhance AI effectiveness |
| 9 | Repeatability | Whether AI benefits are repeatable, scalable, and durable |
| 10 | Contradiction Risk | Volume and severity of evidence that contradicts or limits AI claims |

### Clarification

This score measures how well an AI narrative is supported by process evidence and economic reality. A high score means the thesis is well-grounded. A low score means the thesis relies on claims without sufficient evidence. Neither score directly implies a portfolio action.

---

## 7. AI Narrative Filter

### Classification Labels

Every AI-related narrative encountered by MoneyHorst research processes receives one of the following labels:

| Label | Definition |
|-------|-----------|
| `AI_MARKETING_ONLY` | AI mentioned in investor communications without process evidence |
| `AI_PRODUCT_FEATURE` | AI exists as a product feature but limited economic evidence |
| `AI_INTERNAL_PRODUCTIVITY` | AI improves internal processes with measurable efficiency gains |
| `AI_REVENUE_DRIVER` | AI directly contributes to revenue generation with evidence |
| `AI_MARGIN_DRIVER` | AI directly improves margins with cost or efficiency evidence |
| `AI_PLATFORM_ADVANTAGE` | AI creates structural platform advantages (network effects, data moats) |
| `AI_INFRASTRUCTURE_DEPENDENCY` | Company provides AI infrastructure to others (picks and shovels) |
| `AI_UNVERIFIED_CLAIM` | AI claim exists but no verifiable evidence found |
| `AI_CONTRADICTED_BY_EVIDENCE` | AI claim is actively contradicted by available evidence |

### Filter Rule

**AI narrative must be downgraded unless evidence proves process integration or economic effect.**

Default classification for any new AI narrative without supporting evidence: `AI_UNVERIFIED_CLAIM`. Upgrade requires source-linked evidence of process integration or measurable economic impact.

---

## 8. Research Evidence Engine

### Future Artifact/Model Shape

Each evidence object in the MoneyHorst research system carries the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `asset_id` | string | Canonical asset identifier |
| `claim_id` | string | Unique identifier for the claim being evidenced |
| `claim` | string | The narrative or assertion being evaluated |
| `claim_type` | enum | Category of claim (financial, operational, strategic, technical) |
| `source` | string | Source document, filing, transcript, or report reference |
| `source_authority` | enum | Institutional authority tier of the source |
| `source_date` | date | Publication or observation date of the source |
| `evidence_strength` | enum | strong / moderate / weak / insufficient |
| `evidence_type` | enum | quantitative / qualitative / mixed / anecdotal |
| `contradiction_status` | enum | none / partial / full / unresolved |
| `time_validity` | object | Valid-from, valid-to, decay expectation |
| `related_signals` | list[string] | Canonical signal identifiers affected by this evidence |
| `confidence_impact` | enum | increases / decreases / neutral / uncertain |
| `portfolio_relevance` | enum | high / moderate / low / none / undetermined |
| `human_review_required` | boolean | Whether human analyst must validate before signal use |

### Evidence Engine Rules

1. Every evidence object must be source-linked — no floating evidence without provenance
2. Evidence must be time-aware — stale evidence decays in confidence weight
3. Evidence strength must affect confidence — weak evidence produces uncertainty, not conviction
4. Contradictions must be preserved, not overwritten — conflicting evidence coexists with explicit contradiction_status

---

## 9. Analyst Verification Log

### Future Verification Fields

Every AI-generated research output that may influence signals requires human verification:

| Field | Type | Description |
|-------|------|-------------|
| `AI_output` | string | The AI-generated research content or conclusion |
| `human_check_required` | boolean | Whether human review is mandatory (default: true) |
| `source_verified` | boolean | Human confirmed source references are accurate |
| `contradiction_checked` | boolean | Human evaluated contradicting evidence |
| `portfolio_relevance_checked` | boolean | Human assessed portfolio impact |
| `risk_context_checked` | boolean | Human evaluated risk implications |
| `decision_allowed` | boolean | Whether this output may inform decision governance |
| `reviewer` | string | Identity of the human reviewer |
| `review_date` | date | Date of human review completion |

### Verification Rule

**AI output is not decision authority. Human verification is part of the system design.**

No AI-generated output transitions to signal status without at least one human verification pass. The verification log is an audit artifact, not a rubber stamp.

---

## 10. Separation of Research, Signal, and Decision

### Permanent Boundary Definition

| Layer | Responsibility | Boundary |
|-------|---------------|----------|
| **Research** | Collects and structures information from sources | Does NOT generate signals or make decisions |
| **Signals** | Translate evidence into canonical semantic indicators | Does NOT make portfolio decisions or execute trades |
| **Decision Governance** | Evaluates signal quality, portfolio fit, risk, exposure, correlation, confidence, and human intent | Does NOT execute without human approval |
| **Portfolio Action** | Requires human decision | NEVER automated from AI output alone |

### Explicit Prohibition

**No AI output directly creates a portfolio action.**

The chain is always: Research → Evidence → Signal → Decision Governance → Human Decision → Action. No layer may be skipped. No shortcut from AI output to portfolio action exists.

---

## 11. Research Coverage Expansion with Verification

AI may expand coverage across assets, regions, languages, filings, transcripts, reports, and analyst notes.

### Expansion Rules

| Rule | Rationale |
|------|-----------|
| More coverage does not mean more trades | Coverage expansion serves research depth, not trading volume |
| Coverage expansion requires source validation | New sources must be authority-assessed before evidence extraction |
| Weak evidence must produce uncertainty, not confidence | Low-quality sources increase uncertainty rather than generating conviction |
| Unknowns must remain visible | Gaps in coverage are documented, not hidden behind interpolation |

### Design Implication

Coverage breadth is valuable only when coupled with evidence-quality assessment. A system that covers 500 assets with unverified evidence is worse than one that covers 50 assets with source-validated evidence.

---

## 12. Development Implications for MoneyHorst

### Recommended Future Modules

| # | Module | Purpose |
|---|--------|---------|
| 1 | Research Evidence Engine | Source-linked evidence storage and retrieval |
| 2 | AI Narrative Filter | Classification of AI claims by evidence level |
| 3 | AI Adoption Quality Score | Thesis-quality and process-maturity scoring |
| 4 | Analyst Verification Log | Human review audit trail for AI outputs |
| 5 | Claim vs Evidence Mapper | Structured decomposition of narratives into claims and evidence |
| 6 | Contradiction Register | Preservation and tracking of conflicting evidence |
| 7 | Portfolio Memory Linker | Historical thesis and decision-context preservation |
| 8 | Semantic Signal Extractor | Concept-level extraction from unstructured sources |

### Module Development Rules

Each module must:

1. Be documentation-first — spec and design before implementation
2. Preserve source authority — every output traces to institutional sources
3. Avoid autonomous decisions — no module makes portfolio decisions without human governance
4. Preserve human governance — human verification is structural, not optional
5. Avoid trading/execution logic — unless explicitly scoped in a separate future compliance spec with appropriate regulatory review

---

## 13. Non-Negotiable Boundaries

The following boundaries apply permanently to MoneyHorst research-system development:

| # | Boundary |
|---|----------|
| 1 | No autonomous investment decisions |
| 2 | No direct buy/sell commands |
| 3 | No trading bot behavior |
| 4 | No broker or execution integration |
| 5 | No market data as unsupported methodology proxy |
| 6 | No AI-generated conviction without source evidence |
| 7 | No hidden thesis changes |
| 8 | No untraceable signal generation |
| 9 | No claim without evidence mapping |
| 10 | No portfolio action without human governance |

These boundaries are architectural constraints, not implementation choices. They define what MoneyHorst is and what it is not.

---

## 14. SSOT Usage Rule

This README is a guidance SSOT for future MoneyHorst research-system development.

Future specs involving research, AI adoption, semantic evidence, portfolio memory, signal extraction, or analyst workflow should reference this document as the governing guidance artifact.

When designing new modules or features that touch research, evidence, signals, or decision governance, consult this document for permanent principles and non-negotiable boundaries.

---

## Investment Taxonomy Guidance

MoneyHorst must not be described as a single Growth, Value, Quant, or Stock Investment strategy. MoneyHorst operates at the Portfolio Intelligence / Decision Governance layer and may evaluate many investment styles, factors, methods, and asset allocation choices. Canonical taxonomy is defined in:

- `docs/moneyhorst/investment_style_method_taxonomy_ssot.md`

---

## 15. Final Status

```
MONEYHORST_RESEARCH_MECHANISM_SSOT_COMPLETE
```

---

*End of MoneyHorst Research Mechanism SSOT.*
