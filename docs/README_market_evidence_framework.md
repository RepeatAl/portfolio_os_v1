# Market Evidence Framework

---
artifact_id: market_evidence_framework_md
artifact_type: SSOT
primary_domain: ARCH
secondary_domains: [DATA, SIGNALS, SEMANTICS, REASONING, REPORT, STATE]
lifecycle_status: draft
ssot_relationship: canonical
topic: market_evidence_framework
created_date: "2026-06-04"
last_modified: "2026-06-04"
owner_role: Portfolio Architect
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies:
  - market_organism.principles_md
  - narrative_framework_md
  - narrative_registry_yaml
  - signal_calculation_framework_md
  - data_ingestion_normalization_framework_md
---

## 1. Scope Statement

This document defines the canonical evidence layer for Portfolio OS. It establishes the ontological boundaries between observed facts, calculated signals, evidence containers, and the higher-level constructs (narratives, decisions, scores, allocations) that consume evidence.

This is a **definition-layer document**. It declares WHAT evidence IS, how evidence relates to other primitives, and what rules govern the creation, consumption, and interpretation of evidence — nothing more.

**Explicit exclusions**: This document does NOT contain engines, code, data ingestion pipelines, scoring algorithms, portfolio allocations, dashboards, runtime behavior, or executable logic. It defines structure and semantics — not implementation.

(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)

---

## 2. Glossary Reference

All terms used in this document are defined in the canonical glossary unless amended below:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary
(See: README_shared_glossary_reference, Section: Glossary Usage Rules)

### Local Glossary

| Term | Definition | Status |
|------|-----------|--------|
| Observed_Fact | A discrete, verifiable data point originating from an external source (market data feed, regulatory filing, corporate disclosure, economic release). It is immutable once recorded — the observation cannot change retroactively. | CANDIDATE |
| Calculated_Signal | A derived value produced by applying a defined calculation to one or more Observed_Facts. It is reproducible given the same inputs and formula. It is a sensor reading — it detects, it does not cause. | CANDIDATE |
| Evidence_Container | A structured grouping that associates one or more Observed_Facts and/or Calculated_Signals with a specific analytical question or hypothesis. It organizes evidence for consumption by higher layers. | CANDIDATE |
| Evidence_Consumer | Any system, process, or layer that reads evidence to make decisions, assessments, or transitions. Consumers include: narrative lifecycle assessment, regime detection, risk evaluation, allocation logic, and reporting. | CANDIDATE |
| Evidence_Provenance | The complete chain of custody from raw data source through transformation steps to final evidence form. Every piece of evidence must carry provenance. | CANDIDATE |

### Glossary Policy

- New terms MUST be defined before use (glossary-first rule)
- Local glossary candidates are formalized within this document only
- Central glossary update requires separate governance authorization
- This policy is consistent with Narrative Framework v2 glossary handling

---

## 3. The Evidence Hierarchy

Evidence in Portfolio OS exists in a strict three-layer hierarchy. Each layer builds on the one below it. No layer may be skipped.

```
Layer 3: Evidence_Container (organized evidence for consumption)
    ↑ groups
Layer 2: Calculated_Signal (derived/interpreted values)
    ↑ computed from
Layer 1: Observed_Fact (raw verifiable data)
```

### Layer 1: Observed Facts

An Observed_Fact is the atomic unit of evidence. It is a discrete, verifiable data point that originates from the external world.

**Properties:**

| Property | Description |
|----------|-------------|
| Immutable | Once recorded, an Observed_Fact cannot change. If a data source corrects a previous value, the correction is a NEW Observed_Fact — it does not retroactively alter the original. |
| Timestamped | Every Observed_Fact carries the timestamp of observation (when it was recorded) AND the timestamp of the event it describes (when it occurred). |
| Source-attributed | Every Observed_Fact identifies its originating source (exchange feed, filing database, news wire, official release). |
| Verifiable | An Observed_Fact can be independently confirmed by consulting its source. If it cannot be verified, it is not a fact — it is an assertion. |
| Non-interpretive | An Observed_Fact does not contain judgment, opinion, or interpretation. "CPI printed at 3.2%" is a fact. "CPI was surprisingly high" is interpretation. |

**Examples of Observed Facts:**

- Nvidia reported Q4 data center revenue of $18.4 billion (corporate disclosure)
- The Federal Reserve raised the federal funds rate by 25bp to 5.50% (policy action)
- NATO members committed to 3% of GDP defense spending (geopolitical declaration)
- Brent crude oil traded at $92.15/bbl at 16:00 UTC on 2026-01-15 (market data)

**What is NOT an Observed Fact:**

- "The market expects rate cuts" — this is interpretation, not a verifiable atomic data point
- "AI is transforming the economy" — this is a belief (narrative), not an observation
- A calculated moving average — this is derived, not directly observed
- An analyst's price target — this is opinion, not fact (though the existence of the opinion IS a fact)

### Layer 2: Calculated Signals

A Calculated_Signal is a derived value produced by applying a defined, reproducible calculation to one or more Observed_Facts (or to other Calculated_Signals).

**Properties:**

| Property | Description |
|----------|-------------|
| Derived | Produced by computation, not by direct observation. |
| Reproducible | Given the same inputs and the same formula, the same result is always produced. |
| Formula-attributed | Every Calculated_Signal identifies the specific calculation that produced it. |
| Sensor, not cause | A signal DETECTS conditions — it does not CREATE them. A signal that detects narrative strengthening does not cause the strengthening. |
| Timestamped | Carries both the calculation timestamp and the observation window it covers. |

**Examples of Calculated Signals:**

- 20-day moving average of Nvidia closing price = $142.30 (derived from 20 Observed_Facts)
- Relative Strength Index (RSI) of semiconductor ETF = 72 (derived from price observations)
- Year-over-year change in hyperscaler capex guidance = +35% (derived from two corporate disclosures)
- Defense sector aggregate order backlog growth = +22% YoY (derived from multiple filings)

**The Signal Sensor Declaration (canonical):**

> A Calculated_Signal is a sensor. It detects. It does not cause.
> A signal may detect that a narrative is strengthening. The signal does not cause the strengthening. The underlying State_Change causes it.

(See: README_narrative_framework, Section: 14. Signal Sensor Relationship Declaration)

### Layer 3: Evidence Containers

An Evidence_Container is a structured grouping that organizes Observed_Facts and Calculated_Signals around a specific analytical question.

**Properties:**

| Property | Description |
|----------|-------------|
| Question-oriented | Every container answers a specific question (e.g., "What evidence exists that narrative.ai_infrastructure is strengthening?") |
| Non-authoritative | A container presents evidence — it does not make decisions. The decision authority belongs to the consumer layer. |
| Multi-source | A container may group facts and signals from multiple sources and time periods. |
| Versioned | Containers carry a version or timestamp indicating when the evidence set was last assembled. |
| Non-exclusive | The same Observed_Fact or Calculated_Signal may appear in multiple containers simultaneously. |

**Examples of Evidence Containers:**

- "Evidence for narrative.ai_infrastructure lifecycle assessment" — groups capex announcements, semiconductor demand signals, data center construction permits
- "Evidence for regime detection: monetary tightening" — groups rate decisions, yield curve data, credit spread signals
- "Evidence for portfolio health assessment" — groups position-level signals, sector exposure data, drawdown metrics

---

## 4. Evidence Is Not Narrative

This section establishes the categorical distinction between evidence and narrative. Confusing the two is a structural error that collapses the analytical hierarchy.

### The Distinction

| Aspect | Evidence | Narrative |
|--------|----------|-----------|
| **Ontological role** | Sensor output — what was observed or calculated | Explanatory container — what participants believe |
| **Causality** | Does not cause anything — reports what happened | Does not cause State_Changes — organizes understanding of them |
| **Position in chain** | Leaf-node observation layer | 2nd position in primitive chain |
| **Falsifiability** | Facts are not falsifiable (they happened); signals are reproducible | Narratives ARE falsifiable (contradicting evidence can kill them) |
| **Permanence** | Facts are immutable; signals are recalculated | Narratives have lifecycles — they emerge, strengthen, weaken, die |
| **Authority** | Evidence informs decisions | Narratives explain beliefs |

### Key Principle: Evidence Supports or Contradicts Narratives

Evidence does not define narratives. Evidence does not create narratives. Evidence does not kill narratives.

**Only State_Changes create or kill narratives.** Evidence may constitute the observable manifestation of a State_Change's effects, but the evidence itself is not the causal agent. The distinction matters:

- "Nvidia's capex guidance increased by 40%" is an Observed_Fact
- This fact may be evidence that `narrative.ai_infrastructure` is strengthening
- But the CAUSE of the strengthening is the State_Change (`sc.corporate.guidance`) — not the observation of it
- A sensor detecting fever does not cause the fever. Similarly, evidence detecting narrative momentum does not cause the momentum.

### Why This Matters

If evidence and narrative are conflated:
1. Signals become lifecycle triggers (violating Section 14 of Narrative Framework v2)
2. The evidence layer gains causal authority it does not possess
3. Circular reasoning emerges: evidence "proves" narrative → narrative "explains" evidence → evidence "proves" narrative
4. The State_Change as causal root is demoted (violating Principle 2: Taxonomy Precedes Assets)

(See: README_narrative_framework, Section: 5. Narrative vs. State_Change)
(See: README_narrative_framework, Section: 14. Signal Sensor Relationship Declaration)

---

## 5. Signals Are Sensors, Not Causes

This section formalizes the sensor principle for the entire evidence layer — extending the Narrative Framework's Signal Sensor Relationship Declaration to all evidence consumers.

### The Sensor Principle

**Every element in the evidence layer — Observed_Facts, Calculated_Signals, and Evidence_Containers — is a sensor output. None of them possess causal authority.**

| Evidence Element | Detects | Does NOT Cause |
|-----------------|---------|----------------|
| Observed_Fact | That an event occurred | The event itself |
| Calculated_Signal | That a condition exists | The condition itself |
| Evidence_Container | That evidence supports a hypothesis | The truth of the hypothesis |

### Application Across Domains

The sensor principle applies universally across all evidence consumers:

| Consumer | How It Uses Evidence | What Evidence Does NOT Do |
|----------|---------------------|--------------------------|
| Narrative lifecycle assessment | Evidence may show a narrative is strengthening | Evidence does not trigger the lifecycle transition — only State_Changes do |
| Regime detection | Evidence may indicate a regime shift is occurring | Evidence does not create the regime shift — the macroeconomic or geopolitical event does |
| Risk evaluation | Evidence may reveal elevated risk | Evidence does not create the risk — the underlying market condition does |
| Allocation logic | Evidence informs allocation decisions | Evidence does not make the decision — human or authorized system does |
| Reporting | Evidence populates reports | Evidence does not interpret itself — the reasoning layer provides interpretation |

### Prohibition: Evidence Cannot Redefine Itself

No evidence consumer may alter, redefine, or retroactively modify evidence. Evidence is produced by the observation and calculation layers. Consumers read evidence — they do not write it.

- A narrative assessment cannot change an Observed_Fact to fit its conclusion
- A regime detector cannot recalculate a signal to confirm its hypothesis
- An allocation engine cannot select only confirming evidence and discard contradicting evidence without explicitly documenting the selection criteria

---

## 6. Evidence Production Rules

### Rule 1: Provenance is Mandatory

Every piece of evidence must carry complete provenance:

| Provenance Element | Description |
|-------------------|-------------|
| Source | Where the raw data originated (exchange, filing, release, feed) |
| Observation timestamp | When the data was recorded/received |
| Event timestamp | When the underlying event occurred |
| Transformation chain | If calculated: which formula, which inputs, which version of the calculation |
| Authority | Which system/domain produced this evidence |

### Rule 2: Immutability of Facts

Observed_Facts are append-only. If a source issues a correction:
- The original fact remains in the record (with a "superseded" flag)
- The correction is recorded as a NEW Observed_Fact with its own timestamp
- Both facts carry provenance linking them (original → correction)

### Rule 3: Reproducibility of Signals

Every Calculated_Signal must be reproducible:
- Given the same Observed_Facts as inputs
- Using the same formula/algorithm version
- The same output must be produced

If a signal formula changes (new version), the new version produces NEW signals — it does not retroactively alter historical signal values.

### Rule 4: Separation of Production and Consumption

The evidence layer is produced by DATA and SIGNALS domains. It is consumed by SEMANTICS, REASONING, REPORT, and STATE domains. These are separate authorities:

```
PRODUCTION (DATA, SIGNALS):
  → Observes facts
  → Calculates signals
  → Assembles evidence containers

CONSUMPTION (SEMANTICS, REASONING, REPORT, STATE):
  → Reads evidence
  → Interprets evidence
  → Makes decisions informed by evidence
  → Reports evidence-based conclusions
```

No consumption domain may alter evidence. No production domain may make decisions based on evidence it produces (separation of concerns).

### Rule 5: No Circular Evidence

Evidence cannot cite itself as its own justification:
- A signal cannot be input to its own calculation
- An evidence container cannot contain itself
- A fact derived from a signal derived from that same fact is circular and prohibited

---

## 7. How Evidence Supports System Functions

### Narrative Lifecycle Assessment

Evidence supports (but does not trigger) narrative lifecycle transitions:

| Lifecycle Question | Evidence Role | Authority for Transition |
|-------------------|--------------|--------------------------|
| "Is narrative.X emerging?" | Evidence may show early adoption signals | State_Change (T1: Birth) |
| "Is narrative.X strengthening?" | Evidence may show confirming capital flows | State_Change (T2: Confirm) |
| "Is narrative.X dominant?" | Evidence may show consensus positioning | State_Change (T3: Dominate) |
| "Is narrative.X weakening?" | Evidence may show contradicting signals | State_Change (T4: Contradict) |
| "Is narrative.X dead?" | Evidence may show falsification | State_Change (T6: Invalidate) |

Evidence informs the ASSESSMENT of lifecycle state. The TRANSITION itself is caused by a State_Change. This distinction is inviolable.

(See: README_narrative_framework, Section: 6. Narrative Lifecycle State Machine)
(See: README_narrative_framework, Section: 9. State_Change-to-Narrative Interactions)

### Regime Detection

Evidence supports regime identification:

- Observed_Facts (rate decisions, inflation prints, yield curve data) provide raw inputs
- Calculated_Signals (moving averages, spread differentials, momentum indicators) provide derived readings
- Evidence_Containers group regime-relevant signals for assessment
- The regime determination is made by the REASONING layer consuming this evidence — not by the evidence itself

### Risk Evaluation

Evidence supports risk assessment:

- Portfolio exposure facts (positions, weights, sector concentrations)
- Volatility and drawdown signals (calculated from price observations)
- Correlation signals (calculated from return series)
- Liquidity signals (volume, bid-ask spread observations)

Risk is ASSESSED by consuming evidence. Risk is not CREATED by evidence.

### Allocation and Portfolio Health

Evidence supports allocation decisions:

- Current positioning facts (what is held, at what size)
- Performance signals (P&L, relative performance, attribution)
- Capacity signals (available capital, margin utilization)
- Conviction signals (how strongly evidence supports each thesis)

Allocation DECISIONS are made by authorized consumers. Evidence informs but does not dictate.

### Reporting

Evidence populates reports:

- Reports present evidence in human-readable form
- Reports may summarize, aggregate, or highlight evidence
- Reports do NOT alter evidence — they render it
- The report layer is a consumer, not a producer, of evidence

---

## 8. Evidence Layer Boundaries

### What the Evidence Layer IS

- A structured repository of observed facts and calculated signals
- An organizational system for grouping evidence around analytical questions
- A sensor layer that detects and reports market conditions
- A foundation that higher-level reasoning consumes

### What the Evidence Layer is NOT

| It is NOT | Why |
|-----------|-----|
| A narrative | Narratives are shared beliefs. Evidence is observations. |
| A decision engine | Decisions consume evidence. Evidence does not decide. |
| A scoring system | Scores interpret evidence. Evidence does not score itself. |
| A portfolio allocator | Allocation consumes evidence. Evidence does not allocate. |
| A recommendation system | Recommendations are decisions. Evidence informs, does not recommend. |
| A prediction system | Predictions interpret evidence about the future. Evidence reports the past and present. |
| A causal agent | Evidence detects. State_Changes cause. |

### Boundary with Narrative Layer

```
Evidence Layer                          Narrative Layer
─────────────                          ───────────────
Observes facts                          Organizes beliefs
Calculates signals                      Explains why things matter
Groups evidence                         Defines shared interpretive frames
Detects conditions                      Has lifecycle (emerges, dies)
Is immutable (facts)                    Is mutable (narratives evolve)
Has no lifecycle                        Has formal lifecycle states
Is not falsifiable (facts happened)     IS falsifiable (beliefs can be wrong)
```

### Boundary with Decision Layer

```
Evidence Layer                          Decision Layer
─────────────                          ──────────────
Presents facts                          Makes choices
Reports signals                         Allocates capital
Groups evidence                         Sets positions
Is passive (sensor)                     Is active (actor)
Cannot change itself                    Can change portfolios
Has no authority                        Has delegated authority
```

---

## 9. Exclusion Constraints

The following are explicitly excluded from the Market Evidence Framework and from any deliverable produced under its authority:

| # | Prohibition | Rationale |
|---|-------------|-----------|
| EC-E1 | Engine implementations or executable code | Definition-layer document only |
| EC-E2 | Data ingestion pipelines or ETL logic | Implementation belongs to DATA domain execution |
| EC-E3 | Scoring algorithms or numeric weights | Evidence does not score — consumers score |
| EC-E4 | Portfolio allocation logic | Evidence informs allocation — it does not allocate |
| EC-E5 | Dashboard or visualization specifications | Rendering belongs to REPORT domain implementation |
| EC-E6 | Recommendation or optimization logic | Evidence does not recommend — it reports |
| EC-E7 | Causal authority over narratives | Only State_Changes cause narrative transitions |
| EC-E8 | Retroactive fact modification | Observed_Facts are immutable once recorded |
| EC-E9 | Circular evidence dependencies | Evidence cannot justify itself |
| EC-E10 | Confidence values or probabilities on facts | Facts either happened or they didn't — no probability |

---

## 10. Architectural Compatibility

### 12-Domain Model Preservation

The Market Evidence Framework operates WITHIN the existing 12-domain model. It does not add, remove, or redefine any domain.

| Domain | Relationship to Evidence |
|--------|--------------------------|
| DATA | Produces Observed_Facts (primary evidence producer) |
| SIGNALS | Produces Calculated_Signals (derived evidence producer) |
| SEMANTICS | Consumes evidence for meaning extraction |
| REASONING | Consumes evidence for decision support |
| REPORT | Consumes evidence for presentation |
| STATE | Consumes evidence for state assessment |
| ARCH | Defines evidence layer rules (this document) |
| GOV | Reviews evidence governance compliance |
| USER | End consumer of evidence-based outputs |
| DEPLOY | Deploys evidence production systems |
| MEMORY | Stores historical evidence |
| SIM | Consumes evidence for simulation inputs |

### Canonical Chain Preservation

The evidence layer feeds INTO the canonical processing chain but does not alter it:

```
[Evidence Production: DATA → SIGNALS]
         ↓ feeds
SIGNALS → SEMANTICS → REASONING → REPORT
```

Evidence is produced upstream. The canonical chain consumes it. No stage in the chain produces evidence — they consume and interpret it.

### Primitive Chain Compatibility

The evidence layer is orthogonal to the primitive chain:

```
Primitive Chain:   State_Change → Narrative → System → Asset
Evidence Layer:    Observes facts about ALL primitives at ALL levels
```

Evidence can describe State_Changes (observed events), Narratives (observed belief indicators), Systems (observed performance metrics), and Assets (observed prices and flows). The evidence layer is a universal sensor — it does not occupy a position in the primitive chain.

---

## 11. Cross-References

| Target Deliverable | Section Referenced | Context |
|-------------------|-------------------|---------|
| README_narrative_framework | Section 5: Narrative vs. State_Change | Causality direction |
| README_narrative_framework | Section 6: Lifecycle State Machine | Transition triggers |
| README_narrative_framework | Section 14: Signal Sensor Relationship | Sensor principle |
| README_narrative_framework | Section 15: Exclusion Constraints | Prohibition alignment |
| README_market_organism_principles | Principle 1: Organism over Collection | Propagation-based reasoning |
| README_market_organism_principles | Principle 2: Taxonomy Precedes Assets | Classification before assets |
| README_market_organism_principles | Principle 6: Causation over Correlation | Causal mechanisms required |
| README_state_change_taxonomy | Classification Hierarchy | Evidence about State_Changes |
| README_expansion_taxonomy | Expansion Definition | Evidence about propagation |
| README_shared_glossary_reference | Glossary Usage Rules | Term definitions |

---

## 12. Invariants

The following invariants MUST be preserved by all systems that interact with the evidence layer:

| # | Invariant | Source |
|---|-----------|--------|
| 1 | Evidence does not cause — it detects | Sensor Principle |
| 2 | Observed_Facts are immutable once recorded | Production Rule 2 |
| 3 | Calculated_Signals are reproducible given same inputs | Production Rule 3 |
| 4 | Evidence production and consumption are separate authorities | Production Rule 4 |
| 5 | No circular evidence dependencies | Production Rule 5 |
| 6 | Only State_Changes cause narrative transitions — evidence may inform assessment but not trigger transitions | Narrative Framework v2 Section 14 |
| 7 | Evidence carries complete provenance | Production Rule 1 |
| 8 | Consumers read evidence — they do not write or alter it | Consumption principle |
| 9 | Evidence does not interpret itself — interpretation belongs to consumers | Layer boundary |
| 10 | The evidence layer has no lifecycle — facts persist, signals are recalculated, containers are versioned | Structural property |

---

## 13. Purpose

The Market Evidence Framework defines how Portfolio OS captures, normalizes, interprets, and exposes factual market evidence without turning it into narratives or decisions too early.

Evidence is the factual substrate that all higher-level constructs consume. Narratives explain why things matter. Decisions allocate capital. Reports communicate state. But BEFORE any of these can act, they need evidence — observed facts and calculated signals organized into consumable containers.

This framework ensures that:
- Facts remain facts (immutable, verifiable, source-attributed)
- Signals remain sensors (derived, reproducible, non-causal)
- Evidence remains organized (grouped, provenance-linked, consumer-ready)
- Interpretation remains separate from observation (consumers interpret; evidence does not)
- Decisions remain downstream (evidence informs; it does not dictate)

The framework prevents premature collapse — the failure mode where observations, beliefs, and actions merge into a single undifferentiated layer, losing traceability, falsifiability, and governance control.

---

## 14. Scope (Expanded)

### In Scope

- Raw observed facts (source-level data points before and after normalization)
- Normalized facts (source-attributed, timestamped, typed observations)
- Calculated signals (derived values from defined formulas applied to facts)
- Interpreted signal states (qualitative readings: direction, magnitude labels, freshness)
- Evidence containers (structured groupings of facts and signals around analytical questions)
- Provenance (complete chain of custody from source to final evidence form)
- Consumer contracts (how downstream systems consume evidence without altering it)
- Support / contradiction relationships (how evidence relates to narratives, regimes, risks)
- Boundaries between evidence, narratives, regimes, risks, decisions, and reports

### Out of Scope

The following are explicitly excluded from this framework:

| # | Exclusion | Rationale |
|---|-----------|-----------|
| 1 | Data ingestion implementation | Implementation belongs to DATA domain execution |
| 2 | API integrations | Implementation detail |
| 3 | Scraping or crawling logic | Implementation detail |
| 4 | Trading logic | Decision layer, not evidence layer |
| 5 | Portfolio recommendations | Decision layer |
| 6 | Scoring engines | Consumer-side interpretation, not evidence |
| 7 | Ranking engines | Consumer-side interpretation, not evidence |
| 8 | Probability models | Consumer-side computation, not evidence |
| 9 | Confidence scoring | Consumer-side computation, not evidence |
| 10 | Asset-to-narrative mappings | Separate registry (future spec) |
| 11 | Narrative registry population | Separate spec (narrative-population-framework) |
| 12 | Dashboards | REPORT domain implementation |
| 13 | Runtime code | Implementation layer |

---

## 15. Core Primitive Chain

The evidence chain defines the ordered progression from raw observation to downstream action:

```
Raw_Data → Fact → Signal → Evidence_Object → Interpretation_Object → Decision_Object
```

### Primitive Definitions

| # | Primitive | Definition | Layer |
|---|-----------|-----------|-------|
| 1 | **Raw_Data** | Source-level observation before normalization. Untyped, unvalidated, potentially malformed. Exists in the ingestion buffer only. | Pre-evidence |
| 2 | **Fact** | Normalized, source-attributed, timestamped observation. Typed, validated, immutable once recorded. The atomic unit of evidence. | Evidence (Layer 1) |
| 3 | **Signal** | Calculated or interpreted state derived from one or more facts. Reproducible, formula-attributed, sensor-only. | Evidence (Layer 2) |
| 4 | **Evidence_Object** | Structured support/contradiction bundle grouping facts and signals around an analytical question. Question-oriented, non-authoritative. | Evidence (Layer 3) |
| 5 | **Interpretation_Object** | Semantic conclusion produced by a consumer that reads evidence. Used by narrative assessment, regime detection, risk evaluation, and reporting. | Consumer layer |
| 6 | **Decision_Object** | Downstream action logic (allocation, rebalancing, position sizing). Outside this framework entirely. | Decision layer |

### Chain Boundaries

```
THIS FRAMEWORK COVERS:          OUTSIDE THIS FRAMEWORK:
─────────────────────────        ─────────────────────────
Raw_Data                         (pre-evidence, ingestion concern)
Fact                             ← defined here
Signal                           ← defined here
Evidence_Object                  ← defined here
Interpretation_Object            (consumer concern, defined by consumers)
Decision_Object                  (decision concern, outside evidence)
```

The Market Evidence Framework owns Facts, Signals, and Evidence_Objects. Raw_Data is an input concern (DATA domain ingestion). Interpretation_Objects and Decision_Objects are consumer concerns defined by their respective domains.

---

## 16. Relationship to Market Organism Framework

### State_Change Remains Root/Cause

The Market Organism Framework establishes that State_Changes are the causal root of all market propagation. The Market Evidence Framework does NOT alter this:

- State_Changes CAUSE market effects
- Evidence OBSERVES those effects
- Evidence does NOT create causality by itself
- Detecting a fact does not cause the fact
- Calculating a signal does not cause the condition the signal detects

### Evidence Observes, Supports, Contradicts, or Qualifies

Evidence relates to the Market Organism primitives through four verbs:

| Verb | Meaning |
|------|---------|
| **Observes** | Records that something happened (fact creation) |
| **Supports** | Provides factual basis consistent with a hypothesis |
| **Contradicts** | Provides factual basis inconsistent with a hypothesis |
| **Qualifies** | Adds context, nuance, or boundary conditions to an interpretation |

### Complementary Roles

| Framework | Answers | Authority |
|-----------|---------|-----------|
| Market Organism | "How do systems change?" | Causal mechanism and propagation |
| Market Evidence | "What did we observe, and how strongly does it support interpretations?" | Factual substrate and sensor readings |

These frameworks are complementary — not competing. The Organism explains causation. Evidence provides the factual foundation that makes causation assessable.

(See: README_market_organism_principles, Section: Principle 1 — Organism over Collection)
(See: README_market_organism_principles, Section: Principle 6 — Causation over Correlation)

---

## 17. Relationship to Narrative Framework

### Narrative as Explanatory Container

The Narrative Framework v2 defines a narrative as an explanatory container — a shared belief structure. The Market Evidence Framework supports narratives without becoming one:

- **Evidence supports narratives** — facts and signals may confirm that a narrative's thesis is playing out
- **Evidence contradicts narratives** — facts and signals may show a narrative's thesis is failing
- **Evidence does NOT become a narrative** — evidence is observation, not belief
- **A portfolio category is NOT evidence** — grouping assets is not observing facts
- **An asset basket is NOT evidence** — holding positions is not detecting conditions

### Evidence Precedes Narrative Lifecycle Movement

Evidence is REQUIRED before narrative population or lifecycle transitions:

- Before registering a new narrative: evidence of the birth trigger State_Change must exist
- Before transitioning lifecycle state: evidence of the qualifying State_Change must exist
- Evidence informs the assessment — the State_Change causes the transition

(See: README_narrative_framework, Section: 6. Narrative Lifecycle State Machine)
(See: README_narrative_framework, Section: 13. Extension Criteria)
(See: README_narrative_framework, Section: 14. Signal Sensor Relationship Declaration)

---

## 18. Relationship to Narrative Registry

### Division of Responsibility

| Registry/Framework | Question Answered |
|-------------------|-------------------|
| Narrative Registry | "Which narratives officially exist?" |
| Market Evidence Framework | "What factual/signaled evidence exists?" |

### Consumption Rules

- Narrative Population MUST consume evidence before creating registry entries
- No evidence object may DIRECTLY mutate the Narrative Registry
- Evidence informs the human/ARCH decision to register — it does not auto-register
- The registry remains governance-controlled; evidence is sensor-controlled

(See: README_narrative_registry_governance, Section: Creation Procedure)
(See: README_narrative_registry_governance, Section: Inclusion Criteria Gate)

---

## 19. Fact Model

### Canonical Fact Characteristics

Every Fact in the evidence layer carries the following attributes:

| # | Field | Description |
|---|-------|-------------|
| 1 | `fact_id` | Unique identifier for the fact |
| 2 | `source` | Originating data source (exchange, filing, release, feed) |
| 3 | `entity` | The subject of the observation (company, index, macro series, etc.) |
| 4 | `entity_type` | Classification of the entity (asset, index, benchmark, macro_series, etc.) |
| 5 | `fact_type` | Category of observation (earnings, guidance, price, volume, macro_indicator, etc.) |
| 6 | `value` | The observed value (numeric, text, or structured) |
| 7 | `unit` | Unit of measurement (USD, %, bps, ratio, etc.) |
| 8 | `period` | Time period the fact describes (Q4 2025, FY2026, 2026-01-15, etc.) |
| 9 | `timestamp` | When the fact was recorded in the system |
| 10 | `source_timestamp` | When the source published/released the data |
| 11 | `provenance` | Chain of custody from source to system |
| 12 | `normalization_status` | Whether the fact has been normalized (raw / normalized / validated) |

### Fact Categories (Illustrative Only)

The following categories illustrate the types of facts the evidence layer may contain. These are illustrative only — not a canonical exhaustive list, not populated instances, and not registry entries.

**Market Data Facts:**
- Index level
- Index return
- Volume
- Relative strength
- Overbought/oversold condition
- Volatility
- Liquidity
- Correlation to index
- Correlation to benchmark
- Correlation to peers
- Money flow

**Fundamental Facts:**
- Earnings per share
- Revenue growth
- Gross margin
- Operating margin
- Capex
- Guidance
- Valuation multiple

**Macro Facts:**
- Macro indicator
- Inflation data
- Rates data

---

## 20. Signal Model

### Canonical Signal Characteristics

Every Calculated_Signal carries:

| # | Field | Description |
|---|-------|-------------|
| 1 | `signal_id` | Unique identifier for the signal |
| 2 | `input_facts` | List of fact_ids used as inputs |
| 3 | `signal_type` | Classification of the signal (momentum, trend, threshold, composite, etc.) |
| 4 | `entity` | The entity the signal describes |
| 5 | `calculation_window` | Time window over which the signal is calculated |
| 6 | `state` | Qualitative reading (e.g., bullish/neutral/bearish, elevated/normal/depressed) |
| 7 | `direction` | Qualitative direction (increasing/stable/decreasing) |
| 8 | `magnitude_label` | Qualitative magnitude (strong/moderate/weak/negligible) |
| 9 | `freshness` | How current the signal is (current/stale/expired/unknown) |
| 10 | `provenance` | Calculation formula reference and input chain |
| 11 | `limitations` | Known limitations or conditions under which the signal may be unreliable |

### Signal Clarifications

- Signals are **derived observations** — they transform facts into interpretable states
- Signals are **sensors** — they detect conditions, they do not create them
- Signals are **not causes** — a signal detecting narrative strengthening does not cause the strengthening
- Signals are **not recommendations** — a bullish signal does not mean "buy"
- Signals are **not portfolio weights** — signal magnitude is not position sizing

---

## 21. Evidence Object Model

### Canonical Evidence Object Characteristics

Every Evidence_Object carries:

| # | Field | Description |
|---|-------|-------------|
| 1 | `evidence_id` | Unique identifier for the evidence object |
| 2 | `supports` | What hypothesis/narrative/state this evidence supports |
| 3 | `contradicts` | What hypothesis/narrative/state this evidence contradicts |
| 4 | `related_to` | Entities, narratives, or systems this evidence relates to |
| 5 | `input_facts` | List of fact_ids grouped into this evidence |
| 6 | `input_signals` | List of signal_ids grouped into this evidence |
| 7 | `evidence_type` | Classification (narrative_support, regime_indicator, risk_signal, health_metric) |
| 8 | `evidence_readiness` | Qualitative label: high / medium / low / insufficient |
| 9 | `contradiction_level` | Qualitative label: high / medium / low / none |
| 10 | `freshness` | How current the evidence is (current/stale/expired/unknown) |
| 11 | `provenance_chain` | Full chain from source facts through signals to this evidence object |
| 12 | `consumer_scope` | Which consumers may read this evidence (narrative, regime, risk, health, allocation, report) |

### Evidence Quality Clarification

`evidence_readiness` and `contradiction_level` are **qualitative labels only**. They are categorical descriptors — NOT numeric scores, NOT ordinal rankings, NOT confidence intervals. They enable human reasoning about evidence completeness — they are not inputs to computation.

Future scoring governance may authorize numeric models that consume these labels. This framework does not authorize such models. Until separately authorized, these remain qualitative.

---

## 22. Evidence Container Types

Evidence containers are organized by conceptual namespace. These define the TYPES of containers — not populated instances.

| Namespace | Purpose | Example Question |
|-----------|---------|-----------------|
| `evidence.narrative.*` | Evidence supporting/contradicting narrative hypotheses | "What evidence supports narrative.ai_infrastructure strengthening?" |
| `evidence.regime.*` | Evidence indicating regime state | "What evidence indicates monetary tightening regime?" |
| `evidence.risk.*` | Evidence revealing risk conditions | "What evidence shows concentration risk in portfolio?" |
| `evidence.portfolio_health.*` | Evidence about portfolio state | "What is the evidence for portfolio health degradation?" |
| `evidence.asset.*` | Evidence about specific asset conditions | "What evidence exists about NVDA fundamental trajectory?" |
| `evidence.system.*` | Evidence about system-level conditions | "What evidence shows semiconductor system under stress?" |
| `evidence.macro.*` | Evidence about macro conditions | "What evidence indicates inflation persistence?" |

**Clarification**: These are conceptual namespaces defining container TYPES. They are NOT populated registries. No evidence objects are created by this README. Population requires implementation in the DATA and SIGNALS domains.

---

## 23. Consumer Contracts

Downstream consumers use evidence according to defined contracts. Each consumer has specific rights and prohibitions:

| Consumer | Rights | Prohibitions |
|----------|--------|--------------|
| **Narrative Population** | Read evidence to justify candidate inclusion | Cannot create evidence; cannot mutate registry without governance approval |
| **Narrative Lifecycle** | Read evidence to justify state transitions | Cannot trigger transitions directly — only State_Changes do |
| **Asset-to-Narrative** | Read evidence to justify qualitative membership assessment | Cannot create numeric membership weights from evidence |
| **Portfolio Health** | Read evidence for concentration, volatility, correlation, breadth, liquidity assessment | Cannot alter evidence to improve apparent health |
| **Allocation** | Read evidence to inform allocation decisions | Cannot redefine facts or signals to justify positions |
| **Reports** | Read evidence for explanation and presentation | Cannot alter evidence for presentation purposes |
| **Dashboards** | Read rendered states (consumer outputs) | Consume rendered results only — not raw evidence directly |

### Universal Consumer Rules

1. Consumers READ evidence — they do not WRITE or ALTER it
2. Consumers INTERPRET evidence — the interpretation belongs to the consumer, not to the evidence
3. Consumers must CITE evidence — every interpretation must reference specific evidence_ids
4. Consumers must respect PROVENANCE — they cannot use evidence without its chain of custody
5. Consumers must handle CONTRADICTION — contradicting evidence cannot be silently discarded

---

## 24. Boundary Rules

The following hard rules define the boundaries of the evidence layer:

| # | Rule | Rationale |
|---|------|-----------|
| 1 | Facts do not imply recommendations | Observation ≠ Action |
| 2 | Signals do not cause state changes | Sensors ≠ Causes |
| 3 | Evidence does not mutate registries | Evidence informs governance — it does not bypass it |
| 4 | Narratives do not own facts | Facts exist independently of any narrative |
| 5 | Assets do not define narratives | Assets are leaf nodes — never causal roots |
| 6 | Portfolio categories do not define narratives | Categories are convenience groupings — not causal beliefs |
| 7 | Scores and weights are not part of this framework | Scoring is a consumer concern, not an evidence concern |
| 8 | Evidence must remain provenance-linked | No orphan evidence — every piece traces back to source |
| 9 | Every interpretation must be traceable back to facts/signals | No ungrounded claims |

---

## 25. Supported Entity Types

The evidence layer may observe facts and calculate signals about the following entity types:

| Entity Type | Description | Example |
|-------------|-------------|---------|
| `asset` | Individual security or instrument | NVDA, AAPL, BTC |
| `index` | Market index | S&P 500, NASDAQ, DAX |
| `benchmark` | Performance reference | Russell 2000, MSCI World |
| `peer_group` | Comparable entities | Hyperscaler peers, Defense primes |
| `sector` | Economic sector | Technology, Healthcare |
| `industry` | Sub-sector classification | Semiconductors, Cybersecurity |
| `company` | Corporate entity | Nvidia, Microsoft |
| `macro_series` | Macroeconomic data series | CPI, Fed Funds Rate, PMI |
| `commodity` | Physical commodity | Crude Oil, Natural Gas, Copper |
| `currency` | Currency pair or rate | EUR/USD, DXY |
| `rate` | Interest rate | US 10Y Treasury, Fed Funds |
| `country` | Sovereign entity | USA, Germany, Japan |
| `system` | Functional system (per Expansion Taxonomy) | system.semiconductor_manufacturing |
| `narrative_candidate` | Proposed narrative under evaluation | candidate.ai_infrastructure |

**Clarification**: Entity type support does NOT mean all entity registries exist yet. A canonical `system.*` registry does not exist. A canonical `asset.*` registry does not exist. The evidence framework can observe these entity types — it does not require their formal registration first.

---

## 26. Evidence Quality Labels

All quality labels in this framework are **qualitative only**. No numeric scoring is authorized.

### evidence_readiness

| Label | Meaning |
|-------|---------|
| `high` | Multiple confirming facts/signals from primary sources; recent; consistent |
| `medium` | Some facts/signals available; may have gaps or staleness |
| `low` | Limited facts/signals; significant gaps; relies on secondary sources |
| `insufficient` | Not enough evidence to support any interpretation |

### contradiction_level

| Label | Meaning |
|-------|---------|
| `high` | Strong contradicting evidence exists alongside supporting evidence |
| `medium` | Some contradicting signals present; interpretation is contested |
| `low` | Minor contradictions; overall evidence direction is clear |
| `none` | No contradicting evidence detected |

### freshness

| Label | Meaning |
|-------|---------|
| `current` | Evidence is from the most recent available period |
| `stale` | Evidence is from a prior period; newer data may exist |
| `expired` | Evidence is from a period no longer relevant to current assessment |
| `unknown` | Freshness cannot be determined |

### provenance_quality

| Label | Meaning |
|-------|---------|
| `primary` | Direct from authoritative source (exchange, filing, official release) |
| `secondary` | From a reliable intermediary (data aggregator, verified news) |
| `derived` | Calculated from other evidence (signal from facts) |
| `unknown` | Provenance cannot be fully established |

**Prohibition**: These labels MUST NOT be converted to numbers. `high` ≠ 3, `medium` ≠ 2, `low` ≠ 1. They are categorical. Arithmetic operations on these labels are prohibited.

---

## 27. Provenance Requirements

Every piece of evidence must satisfy provenance requirements:

| Requirement | Applies To | Description |
|-------------|-----------|-------------|
| Source identity | All facts | The originating source must be identified (exchange name, filing type, release authority) |
| Source timestamp | All facts | When the source published the data (where available) |
| Calculation window | Calculated signals | The time window over which the calculation operates |
| Input linkage | Signals, Evidence_Objects | Input facts/signals must be explicitly referenced by ID |
| Derivation chain | Interpretations | Any interpretation must expose its full evidence chain back to facts |

### Provenance Anti-Patterns

The following are violations of provenance requirements:

- A signal with no identified input facts
- An evidence object with no provenance chain
- An interpretation citing "general market conditions" without specific evidence_ids
- A fact with no source attribution
- A derived value with no formula reference

---

## 28. Anti-Drift Rules

The following rules prevent the evidence layer from drifting into scoring, ranking, or decision-making territory:

| # | Prohibition | Why |
|---|-------------|-----|
| 1 | No hidden scoring | Quality labels are not scores. Do not compute aggregates from them. |
| 2 | No hidden ranking | Evidence objects have no rank or priority order. |
| 3 | No hidden confidence values | "Evidence_readiness: high" is not "confidence: 0.9". |
| 4 | No hidden portfolio allocation logic | Evidence does not determine position sizes. |
| 5 | No using evidence labels as pseudo-weights | "High evidence_readiness" does not mean "allocate more". |
| 6 | No using narrative popularity as evidence | How many people believe a narrative is not a fact about the narrative's truth. |
| 7 | No using asset performance alone as narrative truth | A stock going up does not prove a narrative is correct. |
| 8 | No collapsing facts, signals, evidence, and narratives into one object | These are separate layers with separate governance. |

---

## 29. Example Flows (Illustrative Only)

The following examples demonstrate how evidence flows through the hierarchy. They are **illustrative only** — not canonical entries, not populated instances, and not registry mutations.

### Example A: AI Infrastructure Evidence

```
FACT: Microsoft announces $50B AI data center capex for FY2027
  → fact_type: capex, entity: Microsoft, value: 50B USD

SIGNAL: Hyperscaler capex acceleration signal
  → input_facts: [Microsoft capex, Google capex, Meta capex]
  → state: accelerating, direction: increasing, magnitude: strong

EVIDENCE OBJECT: AI infrastructure narrative support
  → supports: candidate.ai_infrastructure
  → input_signals: [hyperscaler_capex_acceleration]
  → evidence_readiness: high
  → contradiction_level: none
```

### Example B: Narrative Contradiction Evidence

```
FACT: Company X cuts FY guidance by 20%, citing demand slowdown
  → fact_type: guidance, entity: Company X, value: -20%

SIGNAL: Earnings deterioration signal for Company X
  → input_facts: [Company X guidance cut, Company X EPS miss]
  → state: deteriorating, direction: decreasing, magnitude: strong

EVIDENCE OBJECT: Narrative weakening candidate
  → contradicts: candidate.some_narrative
  → input_signals: [earnings_deterioration]
  → evidence_readiness: medium
  → contradiction_level: high
```

### Example C: Portfolio Health Evidence

```
FACT: Portfolio top-5 positions represent 62% of total value
  → fact_type: concentration, entity: portfolio, value: 62%

SIGNAL: Concentration risk signal
  → input_facts: [position_weights]
  → state: elevated, direction: increasing, magnitude: moderate

EVIDENCE OBJECT: Portfolio health — concentration risk
  → related_to: portfolio_health
  → input_signals: [concentration_risk]
  → evidence_readiness: high
  → consumer_scope: [portfolio_health, risk, report]
```

**All examples above are illustrative only.** They do NOT create facts, signals, or evidence objects. They do NOT populate any registry or data store.

---

## 30. Future Frameworks Enabled

This README enables the following future specs and frameworks by establishing the evidence layer they will consume:

| Future Framework | How This README Enables It |
|-----------------|---------------------------|
| Narrative Population Framework | Provides evidence model for justifying candidate narrative registration |
| Narrative Lifecycle Framework | Provides evidence model for justifying lifecycle state transitions |
| Asset-to-Narrative Registry | Provides evidence model for justifying qualitative membership |
| Market Regime Evidence | Provides container types for regime detection evidence |
| Portfolio Health Evidence | Provides container types for portfolio health assessment |
| Allocation Evidence Contract | Defines how allocation logic consumes evidence without redefining it |
| Report Evidence Rendering | Defines how reports consume and present evidence |

---

## 31. Verification Expectations

Future verification gates for implementations consuming this framework should check:

| # | Verification | Purpose |
|---|-------------|---------|
| 1 | Fact/signal/evidence boundary preservation | Ensure layers are not collapsed |
| 2 | No scoring leakage | Ensure qualitative labels are not converted to numbers |
| 3 | Provenance completeness | Ensure every evidence piece has full provenance |
| 4 | No registry mutation | Ensure evidence consumption does not auto-mutate registries |
| 5 | No asset-first narrative creation | Ensure narratives are not derived from asset lists |
| 6 | Consumer contract clarity | Ensure each consumer respects its rights and prohibitions |

---

## 32. Satisfies / Cross-References (Expanded)

| Target Deliverable | Section Referenced | Context |
|-------------------|-------------------|---------|
| README_market_organism_principles | Principle 1: Organism over Collection | Evidence observes organism-level propagation |
| README_market_organism_principles | Principle 2: Taxonomy Precedes Assets | Evidence does not start from assets |
| README_market_organism_principles | Principle 6: Causation over Correlation | Evidence provides causal substrate, not correlation |
| README_narrative_framework | Section 5: Narrative vs. State_Change | Evidence/narrative boundary |
| README_narrative_framework | Section 6: Lifecycle State Machine | Evidence supports lifecycle assessment |
| README_narrative_framework | Section 13: Extension Criteria | Evidence required before registration |
| README_narrative_framework | Section 14: Signal Sensor Relationship | Sensor principle |
| README_narrative_framework | Section 15: Exclusion Constraints | Prohibition alignment |
| README_narrative_registry_governance | Creation Procedure | Evidence consumed during registration |
| README_narrative_registry_governance | Inclusion Criteria Gate | Evidence justifies criteria satisfaction |
| README_state_change_taxonomy | Classification Hierarchy | Evidence about State_Changes |
| README_expansion_taxonomy | Expansion Definition | Evidence about propagation |
| README_shared_glossary_reference | Glossary Usage Rules | Term definitions |
| signal_calculation_framework_md | (future) | Signal calculation definitions |
| data_ingestion_normalization_framework_md | (future) | Fact normalization procedures |
| portfolio_health_framework_md | (future) | Health evidence consumption |
| correlation_dependency_framework_md | (future) | Correlation evidence boundaries |
| report_reasoning_system_md | (future) | Report evidence rendering |

---

*Last updated: 2026-06-04*
*Authority: ARCH (primary), GOV (review)*
*Ontology alignment: Narrative Framework v2, Market Organism Principles*
*Status: Draft — pending review*
