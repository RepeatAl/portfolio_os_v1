# Temporal Taxonomy

---
artifact_id: temporal_taxonomy_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Defines temporal properties for all Dependency_Paths in the Organism_Graph
ssot_relationship: canonical
topic: temporal_taxonomy
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [dependency_types_v2_md, expansion_taxonomy_md]
---

## Scope Statement

This document defines the formal temporal properties that characterize how effects propagate along Dependency_Paths in the Organism_Graph. It establishes five canonical temporal properties — Latency, Duration, Amplification, Dampening, and Feedback_Delay — each with enumerated qualitative values and interpretation guides. Every Dependency_Path in the Organism_Graph carries these temporal properties. This document does NOT contain engines, code, scores, weights, probabilities, numeric models, asset lists, correlation matrices, dashboards, or any executable logic.

---

## Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary

This document does not define terms. It consumes them.

---

## Temporal Property Enumeration

The Temporal_Taxonomy defines exactly five properties. Each Dependency_Path in the Organism_Graph carries all five properties as qualitative descriptors.

| # | Property | Canonical ID | Value Type | Valid Values |
|---|----------|-------------|------------|--------------|
| 1 | Latency | `temporal.latency` | Discrete calendar unit | Day, Week, Month, Quarter, Year |
| 2 | Duration | `temporal.duration` | Discrete calendar unit | Day, Week, Month, Quarter, Year |
| 3 | Amplification | `temporal.amplification` | Qualitative 5-level scale | None, Low, Moderate, High, Extreme |
| 4 | Dampening | `temporal.dampening` | Qualitative 5-level scale | None, Low, Moderate, High, Extreme |
| 5 | Feedback_Delay | `temporal.feedback_delay` | Discrete calendar unit | Day, Week, Month, Quarter, Year |

---

## Property Definitions

### Latency

**Definition**: The time delay between an Impulse occurring at the source node and its effect manifesting at the downstream target node along a Dependency_Path. Latency represents when the effect arrives, not how long it lasts.

**Canonical ID**: `temporal.latency`

**Units**: Discrete calendar-based time units selected from an enumerated set of exactly five values.

| Valid Values |
|-------------|
| Day |
| Week |
| Month |
| Quarter |
| Year |

**Interpretation Guide**:

| Value | Meaning | Example Context |
|-------|---------|-----------------|
| Day | Effect manifests within one calendar day of the Impulse | A central bank rate decision immediately reprices short-term bond yields via a Price Dependency_Path |
| Week | Effect manifests within one calendar week of the Impulse | An earnings surprise propagates to sector peers through Narrative Dependency_Paths as analysts revise estimates |
| Month | Effect manifests within one calendar month of the Impulse | A supply chain disruption propagates to downstream manufacturers through Supply_Chain Dependency_Paths as inventory buffers deplete |
| Quarter | Effect manifests within one calendar quarter of the Impulse | A regulatory change propagates to affected industries through Regulatory Dependency_Paths as compliance deadlines approach |
| Year | Effect manifests within one calendar year of the Impulse | A structural shift in energy policy propagates to capital expenditure patterns through Macro Dependency_Paths as investment cycles complete |

**Prohibited**: Numeric scores, weights, probabilities, or quantitative models. Latency is assigned as a discrete calendar unit, never as a numeric value (e.g., "14.5 days" is INVALID; "Week" is VALID).

---

### Duration

**Definition**: The time span over which a propagated effect remains active at the target node. Duration represents how long the effect persists after it arrives, not when it arrives.

**Canonical ID**: `temporal.duration`

**Units**: Discrete calendar-based time units selected from an enumerated set of exactly five values (same units as Latency).

| Valid Values |
|-------------|
| Day |
| Week |
| Month |
| Quarter |
| Year |

**Interpretation Guide**:

| Value | Meaning | Example Context |
|-------|---------|-----------------|
| Day | Effect remains active for approximately one calendar day before dissipating | A flash crash propagates a Price Dependency_Path effect that reverses within the same trading session |
| Week | Effect remains active for approximately one calendar week | An earnings beat sustains elevated sector sentiment through Narrative Dependency_Paths for several trading days before normalizing |
| Month | Effect remains active for approximately one calendar month | A guidance revision sustains altered analyst models through Fundamental Dependency_Paths until the next reporting cycle |
| Quarter | Effect remains active for approximately one calendar quarter | A liquidity injection sustains altered Flow Dependency_Path dynamics through a full business quarter |
| Year | Effect remains active for one calendar year or longer | A regime shift in monetary policy sustains altered Macro Dependency_Path conditions across multiple business cycles |

**Prohibited**: Numeric scores, weights, probabilities, or quantitative models. Duration is assigned as a discrete calendar unit, never as a numeric value (e.g., "3.5 months" is INVALID; "Quarter" is VALID).

---

### Amplification

**Definition**: The degree to which an effect grows stronger as it propagates along a Dependency_Path. Amplification describes whether the signal intensifies between source and target — the effect at the target is larger in scope or impact than the originating Impulse would suggest at the source.

**Canonical ID**: `temporal.amplification`

**Levels**: Qualitative descriptor selected from an enumerated set of exactly five levels.

| Valid Values |
|-------------|
| None |
| Low |
| Moderate |
| High |
| Extreme |

**Interpretation Guide**:

| Level | Meaning | Example Context |
|-------|---------|-----------------|
| None | Effect arrives at target with no intensification relative to source | A dividend announcement propagates through an Ownership Dependency_Path with proportional impact — no amplification occurs |
| Low | Effect arrives slightly intensified — target impact marginally exceeds what source magnitude alone would predict | A moderate earnings beat propagates through Narrative Dependency_Paths with slightly elevated sector attention beyond the single company |
| Moderate | Effect arrives meaningfully intensified — target impact noticeably exceeds source magnitude | An oil supply disruption propagates through Macro Dependency_Paths with amplified impact on energy-dependent industries beyond the direct supply shortfall |
| High | Effect arrives substantially intensified — target impact significantly exceeds source magnitude through reinforcing mechanisms | A sovereign debt concern propagates through Flow Dependency_Paths with amplified capital flight as multiple actors respond simultaneously |
| Extreme | Effect arrives with maximum intensification — target impact dwarfs source magnitude through cascading reinforcement | A bank failure propagates through Behavioral Dependency_Paths with extreme amplification as contagion fear triggers system-wide withdrawal behavior far exceeding the original institution's significance |

**Prohibited**: Numeric scores, weights, probabilities, or quantitative models. Amplification is assigned as a qualitative level, never as a numeric multiplier (e.g., "2.5x amplification" is INVALID; "High" is VALID).

---

### Dampening

**Definition**: The degree to which an effect weakens as it propagates along a Dependency_Path. Dampening describes whether the signal attenuates between source and target — the effect at the target is smaller in scope or impact than the originating Impulse would suggest at the source.

**Canonical ID**: `temporal.dampening`

**Levels**: Qualitative descriptor selected from an enumerated set of exactly five levels.

| Valid Values |
|-------------|
| None |
| Low |
| Moderate |
| High |
| Extreme |

**Interpretation Guide**:

| Level | Meaning | Example Context |
|-------|---------|-----------------|
| None | Effect arrives at target with no attenuation relative to source | A regulatory mandate propagates through a Regulatory Dependency_Path with full force — compliance is binary, no dampening occurs |
| Low | Effect arrives slightly attenuated — target impact marginally less than source magnitude would predict | A central bank rate change propagates through Macro Dependency_Paths with slight dampening as some institutions absorb the change through existing hedges |
| Moderate | Effect arrives meaningfully attenuated — target impact noticeably less than source magnitude | A supply chain disruption propagates through Supply_Chain Dependency_Paths with moderate dampening as firms activate secondary suppliers |
| High | Effect arrives substantially attenuated — target impact significantly less than source magnitude through absorbing mechanisms | A narrative shift propagates through distant Narrative Dependency_Paths with high dampening as the causal connection becomes increasingly indirect |
| Extreme | Effect arrives with maximum attenuation — target impact is barely detectable relative to source magnitude | A geopolitical event propagates through multiple Butterfly Dependency_Paths with extreme dampening — the connection exists but the effect is nearly imperceptible at the target |

**Prohibited**: Numeric scores, weights, probabilities, or quantitative models. Dampening is assigned as a qualitative level, never as a numeric decay factor (e.g., "0.3 dampening coefficient" is INVALID; "High" is VALID).

---

### Feedback_Delay

**Definition**: The qualitative temporal descriptor representing the characteristic time scale required for a downstream effect to propagate back to the source node through a Feedback_Loop. Feedback_Delay characterizes the back-propagation time — how long it takes for a circular Dependency_Path to complete its cycle and influence the originating node.

**Canonical ID**: `temporal.feedback_delay`

**Units**: Discrete calendar-based time units selected from an enumerated set of exactly five values (same units as Latency).

| Valid Values |
|-------------|
| Day |
| Week |
| Month |
| Quarter |
| Year |

**Interpretation Guide**:

| Value | Meaning | Example Context |
|-------|---------|-----------------|
| Day | Back-propagation completes within one calendar day — the feedback cycle is near-immediate | A flash crash triggers stop-losses (Behavioral Dependency_Path) which deepen the crash (Price Dependency_Path) which triggers more stop-losses — the feedback cycle completes intraday |
| Week | Back-propagation completes within one calendar week | A currency depreciation triggers capital outflows (Flow Dependency_Path) which further depreciate the currency — the feedback cycle completes within days |
| Month | Back-propagation completes within one calendar month | A credit downgrade raises borrowing costs (Fundamental Dependency_Path) which weakens fundamentals (Macro Dependency_Path) which invites further downgrades — the cycle completes over weeks |
| Quarter | Back-propagation completes within one calendar quarter | A housing price decline reduces consumer wealth (Macro Dependency_Path) which reduces spending (Flow Dependency_Path) which weakens the economy (Fundamental Dependency_Path) which further depresses housing — the cycle completes over months |
| Year | Back-propagation completes within one calendar year or longer | A structural underinvestment in energy capacity raises prices (Supply_Chain Dependency_Path) which eventually incentivizes new investment (Fundamental Dependency_Path) which eventually increases supply — the feedback cycle completes over multiple quarters |

**Prohibited**: Numeric scores, weights, probabilities, or quantitative models. Feedback_Delay is assigned as a discrete calendar unit, never as a numeric value (e.g., "45 days feedback time" is INVALID; "Month" is VALID).

---

## Numeric Prohibition

This section consolidates the explicit prohibition on quantitative values for all temporal properties defined in this document.

### Prohibition Statement

All temporal properties in this taxonomy are **qualitative only**. The following are explicitly prohibited in any temporal property assignment:

| Prohibited | Example of Violation | Why Prohibited |
|-----------|---------------------|----------------|
| Numeric time values | "Latency: 14.5 days" | Implies false precision; the definition layer uses discrete calendar units only |
| Decimal multipliers | "Amplification: 2.3x" | Introduces quantitative modeling into the definition layer |
| Percentage values | "Dampening: 70%" | Introduces scoring logic into the definition layer |
| Probability values | "Likelihood of amplification: 0.85" | Introduces probability into the definition layer |
| Weighted scores | "Temporal weight: 0.6" | Introduces weighting into the definition layer |
| Confidence intervals | "Latency: Month ± 2 weeks" | Introduces statistical modeling into the definition layer |
| Numeric rankings | "Amplification rank: 3 of 5" | Converts qualitative levels into ordinal scores |

### Rationale

Weights on an incomplete model produce false confidence. The temporal properties defined here establish the qualitative vocabulary for describing propagation timing and intensity. Numeric precision belongs to future implementation phases where the model is complete enough to support quantitative claims.

### Valid Assignment Pattern

```
Latency: Month          ← VALID (discrete calendar unit)
Duration: Quarter       ← VALID (discrete calendar unit)
Amplification: High     ← VALID (qualitative level)
Dampening: Low          ← VALID (qualitative level)
Feedback_Delay: Week    ← VALID (discrete calendar unit)
```

### Invalid Assignment Pattern

```
Latency: 30 days        ← INVALID (numeric time value)
Duration: 2.5 months    ← INVALID (decimal time value)
Amplification: 4/5      ← INVALID (numeric score)
Dampening: 0.7          ← INVALID (decimal coefficient)
Feedback_Delay: 6 weeks ← INVALID (numeric time value)
```

---

## Satisfies

| Requirement | How Satisfied |
|-------------|---------------|
| 5.1 | Defines exactly four Temporal_Properties (Latency, Duration, Amplification, Dampening) plus Feedback_Delay for every Dependency_Path |
| 5.2 | Specifies Latency as time delay expressed using discrete calendar-based time units (Day, Week, Month, Quarter, Year) |
| 5.3 | Specifies Duration as active time span expressed using the same discrete calendar-based time units as Latency |
| 5.4 | Specifies Amplification as qualitative descriptor from exactly five levels (None, Low, Moderate, High, Extreme) |
| 5.5 | Specifies Dampening as qualitative descriptor from exactly five levels (None, Low, Moderate, High, Extreme) |
| 5.6 | Provides complete temporal propagation example (Fed Hawkish Shift) showing all four Temporal_Properties at each Expansion_Order (1st through 4th) with increasing Latency values (Day, Month, Quarter, Year) |
| 5.7 | Explicitly prohibits numeric scores, weights, or probabilities for Temporal_Properties in this definition phase |
| 6.3 | Defines Feedback_Delay as qualitative temporal descriptor for back-propagation time using same calendar units as Latency |
| 8.7 | Contains dedicated Exclusion Constraints section consolidating all prohibitions (engines, code, scores, weights, probabilities, dashboards, asset lists, correlation matrices) |
| 10.8 | Cross-References section identifies source deliverables by name for all referenced concepts (Expansion_Taxonomy, Dependency_Types_v2, State_Change_Taxonomy, Market_Organism_Principles) |


---

## Temporal Propagation Example: Fed Hawkish Shift

This example demonstrates how all four temporal properties manifest at each Expansion_Order as a single Impulse propagates through the Organism_Graph. The Impulse is a Fed Hawkish Shift — a Regime_Shift in monetary policy where the Federal Reserve signals a sustained tightening cycle.

Root_Node: Fed Hawkish Shift (Type: Regime_Shift)
Canonical ID: `sc.macro.rates`

(See: README_state_change_taxonomy, Section: Macro Sub-Categories)

### Propagation Table

| Order | Affected System | Dependency_Type | Latency | Duration | Amplification | Dampening |
|-------|----------------|-----------------|---------|----------|---------------|-----------|
| 1st | Short-Term Bond Yields | Price (`dep.price`) | Day | Quarter | High | None |
| 1st | Interbank Lending Rates | Macro (`dep.macro`) | Day | Quarter | Moderate | None |
| 2nd | Corporate Borrowing Costs | Fundamental (`dep.fundamental`) | Month | Quarter | Moderate | Low |
| 2nd | Mortgage Rate Repricing | Macro (`dep.macro`) | Month | Year | Moderate | Low |
| 3rd | Housing Market Activity | Supply_Chain (`dep.supply_chain`) | Quarter | Year | Low | Moderate |
| 3rd | Capital Expenditure Deferrals | Fundamental (`dep.fundamental`) | Quarter | Year | Low | Moderate |
| 4th | Employment in Rate-Sensitive Sectors | Behavioral (`dep.behavioral`) | Year | Year | None | High |
| 4th | Consumer Confidence Shift | Narrative (`dep.narrative`) | Year | Year | None | High |

### Explanation Readiness — Per-Order Narrative

**1st Order — Direct Effects (Latency: Day)**

Effect arrives at Short-Term Bond Yields within Day BECAUSE the Price Dependency_Path (`dep.price`) transmits rate expectations directly through market pricing mechanisms. The causal channel is economic and unidirectional — the Fed's signal reprices the yield curve immediately.

Effect arrives at Interbank Lending Rates within Day BECAUSE the Macro Dependency_Path (`dep.macro`) transmits policy rate changes through the banking system's overnight funding structure.

Amplification is High at Short-Term Bond Yields because the market prices in not just the current move but the anticipated trajectory (forward guidance amplifies the immediate signal). Dampening is None — no absorbing mechanism exists at this distance.

(See: README_dependency_types_v2, Section: Price)
(See: README_dependency_types_v2, Section: Macro)

**2nd Order — Secondary Effects (Latency: Month)**

Effect arrives at Corporate Borrowing Costs within Month BECAUSE the Fundamental Dependency_Path (`dep.fundamental`) requires credit markets to reprice corporate spreads relative to the new risk-free rate. The delay reflects the time for new issuance to price at updated levels.

Effect arrives at Mortgage Rate Repricing within Month BECAUSE the Macro Dependency_Path (`dep.macro`) transmits through the secondary mortgage market as lenders adjust rate sheets to reflect updated funding costs.

Amplification decreases to Moderate — the signal is still meaningful but no longer compounding. Dampening emerges at Low — some corporations have fixed-rate debt that absorbs the change, and some mortgage holders are locked into existing rates.

(See: README_dependency_types_v2, Section: Fundamental)

**3rd Order — Tertiary Effects (Latency: Quarter)**

Effect arrives at Housing Market Activity within Quarter BECAUSE the Supply_Chain Dependency_Path (`dep.supply_chain`) requires the structural adjustment of buyer behavior — higher mortgage rates must persist long enough to alter purchase decisions and reduce transaction volume.

Effect arrives at Capital Expenditure Deferrals within Quarter BECAUSE the Fundamental Dependency_Path (`dep.fundamental`) requires corporate planning cycles to incorporate the higher cost of capital into investment decisions.

Amplification decreases to Low — the original rate signal is now several causal steps removed. Dampening increases to Moderate — firms with strong balance sheets absorb the cost increase, and housing markets with supply constraints partially offset demand reduction.

(See: README_dependency_types_v2, Section: Supply_Chain)

**4th Order — Quaternary Effects (Latency: Year)**

Effect arrives at Employment in Rate-Sensitive Sectors within Year BECAUSE the Behavioral Dependency_Path (`dep.behavioral`) requires sustained economic slowdown to translate into hiring freezes and layoffs — a process that unfolds over multiple quarters as firms exhaust alternatives.

Effect arrives at Consumer Confidence Shift within Year BECAUSE the Narrative Dependency_Path (`dep.narrative`) requires accumulated evidence of economic impact (job losses, reduced spending, media coverage) to shift the prevailing consumer sentiment narrative.

Amplification is None — the original rate signal has been fully absorbed into structural economic conditions. Dampening is High — multiple absorbing mechanisms (fiscal policy, savings buffers, labor market friction, counter-narratives) attenuate the connection between the original Impulse and these distant effects.

(See: README_dependency_types_v2, Section: Behavioral)
(See: README_dependency_types_v2, Section: Narrative)

### Observations

**Latency increases with distance from Impulse**: Day → Month → Quarter → Year. Each additional Expansion_Order introduces structural delays as the effect must traverse additional causal mechanisms.

**Amplification typically decreases with distance**: High → Moderate → Low → None. As the signal passes through more intermediary systems, the compounding effect diminishes. This is a tendency, not a rule — specific paths may deviate (e.g., a Behavioral Dependency_Path at 3rd Order could exhibit High Amplification if panic dynamics emerge).

**Dampening typically increases with distance**: None → Low → Moderate → High. More distant systems have more absorbing mechanisms between them and the original Impulse. This is a tendency, not a rule — specific paths may deviate (e.g., a Regulatory Dependency_Path at 4th Order could exhibit None Dampening if a binary compliance mandate propagates with full force regardless of distance).

**These are tendencies, not rules.** The pattern described above represents the typical behavior of temporal properties across Expansion_Orders. Individual Dependency_Paths may deviate based on their specific causal mechanisms, the structural characteristics of the affected systems, and the prevailing market regime.

(See: README_expansion_taxonomy, Section: Expansion Definition)


---

## Exclusion Constraints

This section consolidates all prohibitions that apply to the Temporal_Taxonomy deliverable. These constraints ensure the definition layer remains pure and does not drift into premature implementation.

| # | Prohibition | Example of Violation | Rationale |
|---|-------------|---------------------|-----------|
| 1 | No engine implementations, Python code, or executable logic | A function that calculates latency from historical data | Definition layer defines vocabulary, not computation |
| 2 | No scoring algorithms, numeric weights, probabilities, or ranking systems | "Amplification score: 0.85" or "Latency weight: 0.6" | Quantitative models require a complete model; this layer is incomplete by design |
| 3 | No dashboard designs, report templates, or visualization specifications | A chart showing latency distribution across paths | Visualization belongs to future implementation phases |
| 4 | No asset lists as root-level entities | "AAPL temporal profile: Latency = Week" | Assets are leaf nodes; temporal properties attach to Dependency_Paths, not to tickers |
| 5 | No correlation matrices as substitutes for causal Dependency_Paths | "Correlation between latency and sector: 0.72" | Statistical co-movement is not causation; temporal properties describe causal propagation |
| 6 | No numeric time values as property assignments | "Latency: 14.5 days" or "Duration: 2.3 months" | Discrete calendar units only; false precision is prohibited |
| 7 | No confidence intervals or probability distributions | "Latency: Month ± 2 weeks (95% CI)" | Statistical modeling belongs to future implementation phases |

**Consolidated Rationale**: Weights on an incomplete model produce false confidence. The temporal properties defined in this document establish the qualitative vocabulary for describing propagation timing and intensity. Numeric precision, scoring, and quantitative modeling belong to future implementation phases where the model is complete enough to support quantitative claims.

(See: README_market_organism_principles, Section: Content Exclusions)


---

## Cross-References

This section identifies all concepts in this document that are defined authoritatively in other deliverables. Cross-references replace duplication — the referenced deliverable is the single source of truth for the referenced concept.

### References to Expansion_Taxonomy

| Concept Referenced | Source |
|-------------------|--------|
| Expansion_Order (1st through 4th) | (See: README_expansion_taxonomy, Section: Expansion Definition) |
| Worked Example propagation format | (See: README_expansion_taxonomy, Section: Worked Examples) |
| Termination Criteria for propagation paths | (See: README_expansion_taxonomy, Section: Termination Criteria) |
| Feedback Detection Rule (path revisiting a node) | (See: README_expansion_taxonomy, Section: Feedback Detection Rule) |

### References to Dependency_Types_v2

| Concept Referenced | Source |
|-------------------|--------|
| Dependency_Type classification (10 types) | (See: README_dependency_types_v2, Section: Type Enumeration) |
| Causal Channel definitions (Economic, Informational, Structural) | (See: README_dependency_types_v2, Section: Type Enumeration) |
| Multi-Type Coexistence Rules (combined temporal properties) | (See: README_dependency_types_v2, Section: Multi-Type Coexistence Rules) |
| Price Dependency_Type (used in temporal example) | (See: README_dependency_types_v2, Section: Price) |
| Fundamental Dependency_Type (used in temporal example) | (See: README_dependency_types_v2, Section: Fundamental) |
| Macro Dependency_Type (used in temporal example) | (See: README_dependency_types_v2, Section: Macro) |
| Supply_Chain Dependency_Type (used in temporal example) | (See: README_dependency_types_v2, Section: Supply_Chain) |
| Behavioral Dependency_Type (used in temporal example) | (See: README_dependency_types_v2, Section: Behavioral) |
| Narrative Dependency_Type (used in temporal example) | (See: README_dependency_types_v2, Section: Narrative) |

### References to State_Change_Taxonomy

| Concept Referenced | Source |
|-------------------|--------|
| Fed Hawkish Shift (Root_Node used in temporal example) | (See: README_state_change_taxonomy, Section: Macro Sub-Categories) |
| Root_Node Invariant (valid root node types) | (See: README_state_change_taxonomy, Section: Root Node Invariant) |

### References to Market_Organism_Principles

| Concept Referenced | Source |
|-------------------|--------|
| Principle 3: All Propagation is Temporal | (See: README_market_organism_principles, Section: Principle 3 — All Propagation is Temporal) |
| Principle 5: Expansion Has Order | (See: README_market_organism_principles, Section: Principle 5 — Expansion Has Order) |
| Exclusion rationale (weights on incomplete model) | (See: README_market_organism_principles, Section: Content Exclusions) |


---

## Extension Criteria

The Temporal_Taxonomy supports controlled growth through criteria-gated addition. New calendar units or qualitative levels may be added only when the existing granularity is demonstrably insufficient.

### Adding a New Calendar Unit

A new discrete calendar unit (e.g., "Fortnight" between Week and Month) requires ALL of the following:

| Criterion | Requirement |
|-----------|-------------|
| Insufficiency Justification | Demonstrate with a concrete example that the existing 5-unit granularity (Day, Week, Month, Quarter, Year) cannot adequately describe a real temporal property — i.e., the gap between two adjacent units creates meaningful ambiguity |
| Placement in Existing Scale | Specify exactly which two existing units the new unit falls between (e.g., "between Week and Month") |
| Non-Redundancy | The new unit must not be expressible as a synonym or trivial restatement of an existing unit |
| Interpretation Guide Entry | Provide a complete interpretation guide row: Value, Meaning, Example Context |
| Backward Compatibility | All existing temporal property assignments remain valid after the addition |

**Example of Valid Extension Request**:

> "The gap between Week and Month creates ambiguity for Supply_Chain Dependency_Paths where inventory buffers typically deplete in 2-3 weeks — too long for 'Week' but too short for 'Month'. Propose adding 'Fortnight' between Week and Month."

**Example of Invalid Extension Request**:

> "We need '10 Days' as a unit because our model predicts 10-day latency." — INVALID: introduces numeric precision; the definition layer uses discrete qualitative units only.

### Adding a New Qualitative Level

A new qualitative level for Amplification or Dampening (e.g., "Minimal" between None and Low) requires ALL of the following:

| Criterion | Requirement |
|-----------|-------------|
| Insufficiency Justification | Demonstrate with a concrete example that the existing 5-level granularity (None, Low, Moderate, High, Extreme) cannot adequately describe a real amplification or dampening characteristic — i.e., the gap between two adjacent levels creates meaningful ambiguity |
| Placement in Existing Scale | Specify exactly which two existing levels the new level falls between (e.g., "between None and Low") |
| Non-Redundancy | The new level must not be expressible as a synonym or trivial restatement of an existing level |
| Interpretation Guide Entry | Provide a complete interpretation guide row: Level, Meaning, Example Context |
| Backward Compatibility | All existing temporal property assignments remain valid after the addition |

**Example of Valid Extension Request**:

> "The gap between None and Low creates ambiguity for Ownership Dependency_Paths where a minor portfolio rebalancing produces a barely detectable effect — more than 'None' (which implies zero intensification) but less than 'Low' (which implies marginal but noticeable intensification). Propose adding 'Minimal' between None and Low."

**Example of Invalid Extension Request**:

> "We need a '0.5' level between None and Low for our scoring model." — INVALID: introduces numeric scoring; the definition layer uses qualitative descriptors only.

### Extension Prohibition

The following extensions are explicitly prohibited regardless of justification:

| Prohibited Extension | Why |
|---------------------|-----|
| Numeric time values (e.g., "14 Days") | Violates discrete calendar unit constraint |
| Fractional levels (e.g., "2.5 out of 5") | Violates qualitative-only constraint |
| Probability-based levels (e.g., "Likely High") | Introduces probability into definition layer |
| Composite units (e.g., "Week-to-Month") | Ambiguous; must select a single discrete unit |
| Confidence-qualified levels (e.g., "High (80% confidence)") | Introduces statistical modeling into definition layer |
