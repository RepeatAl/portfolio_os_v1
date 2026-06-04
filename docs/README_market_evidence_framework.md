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

*Last updated: 2026-06-04*
*Authority: ARCH (primary), GOV (review)*
*Ontology alignment: Narrative Framework v2, Market Organism Principles*
*Status: Draft — pending review*
