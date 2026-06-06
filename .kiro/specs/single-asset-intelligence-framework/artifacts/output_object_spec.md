# Single Asset Intelligence Framework — Output Object Specification

**Artifact**: output_object_spec.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 4.1 Create output object specification
**Requirements**: SAI-REQ-5 (Non-Scoring / Non-Recommendation Constraint)
**Verification Gates**: VG-SAI-2 (Boundary Enforcement Gate)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the canonical output object that every SAI analysis block produces. It specifies exactly which fields are allowed, which fields are explicitly prohibited, and the governance rules that enforce the diagnostic-only boundary.

The output object is the single data contract between SAI analysis blocks and any downstream consumer. Every block produces one output object per asset per evaluation cycle. The object carries diagnostic interpretation, evidence provenance, and completeness metadata — never scores, recommendations, or allocation signals.

This is a definition-layer artifact. It contains no implementation code, no JSON Schema, no database schema, no API schema, no runtime validation code, and no executable logic.

(See: design.md, Section: Data Models — Output Object Design)
(See: requirements.md, Section: SAI-REQ-5 — Non-Scoring / Non-Recommendation Constraint)

---

## 2. Allowed Fields

The following 10 fields constitute the complete output object for every SAI analysis block. No additional fields may be added without a formal extension proposal satisfying SAI-REQ-14 (Additive-Only Extension Mechanism).

| # | Field Name | Type | Description | Constraints |
|---|-----------|------|-------------|-------------|
| 1 | `block_id` | String | Stable identifier of the producing block | Format: `SAI-BLK-NN` where NN is 01–24 (or 25+ for extensions). Must match a canonical block from the Block Taxonomy. Immutable once assigned. |
| 2 | `asset_id` | String | Canonical identifier of the asset under analysis | Must reference a valid asset identifier as defined by the Data Ingestion/Normalization Framework interface contract. One output object per (block_id, asset_id) pair per evaluation cycle. |
| 3 | `consumed_facts` | List of strings | Fact IDs consumed by this block for this interpretation | References canonical fact_id values from the Market Evidence Framework. Must contain ≥1 entry unless evidence_completeness is "insufficient". (See: fact_consumption_matrix.md) |
| 4 | `consumed_signals` | List of strings | Signal IDs consumed by this block for this interpretation | References canonical signal_id values from the Market Evidence Framework. Must contain ≥1 entry unless evidence_completeness is "insufficient". (See: signal_consumption_matrix.md) |
| 5 | `interpretation_summary` | String | Diagnostic interpretation text | Free-form diagnostic text describing the block's evidence-based interpretation. Must NOT contain scoring language, recommendations, buy/sell/hold statements, or numeric ratings. Must be evidence-backed — not speculative. |
| 6 | `red_flags` | List of objects | Evidence-based warning conditions detected | Each entry contains: flag_id (format: RF-NN-XX), severity (informational/elevated/critical), evidence (list of fact/signal references), description (evidence-based warning text). May be empty if no red flag conditions are detected. |
| 7 | `evidence_completeness` | Enum string | Qualitative indicator of evidence coverage | Allowed values: `high`, `medium`, `low`, `insufficient`. Indicates degree to which available evidence covers the block's consumption contracts. NOT a numeric score. |
| 8 | `temporal_status` | Enum string | Freshness indicator of consumed evidence | Allowed values: `current`, `stale`, `expired`. Determined by the block's temporal resolution class thresholds. Indicates whether consumed evidence is within acceptable freshness bounds. |
| 9 | `provenance_chain` | Object | Full evidence lineage for this interpretation | Contains: source_facts (list of fact_ids), source_signals (list of signal_ids), timestamps (list of observation/calculation timestamps inherited from source evidence), freshness (current/stale/expired). Ensures no orphan interpretations. (See: Task 5.1 — Provenance Contract for detailed specification) |
| 10 | `deferred_dependency_notes` | String or null | Documentation of limitations from unavailable frameworks | Records which deferred frameworks are unavailable and how this limits the interpretation. Null only when all required frameworks are available and the block operates at full capability. |


---

## 3. Prohibited Fields

The following 20 fields are explicitly prohibited from appearing in any SAI output object, any block definition, or any SAI artifact. Their inclusion would violate SAI-REQ-5 (Non-Scoring / Non-Recommendation Constraint) and constitute architectural drift toward scoring, recommendation, or allocation territory.

| # | Prohibited Field | Category | Reason for Prohibition |
|---|-----------------|----------|----------------------|
| 1 | `score` | Scoring | SAI is diagnostic — it interprets evidence, not scores it. Numeric scores compress multi-dimensional diagnostic information into a single number, destroying interpretive nuance and implying ordinal comparison. |
| 2 | `rank` | Scoring | Rankings imply relative merit ordering across assets. SAI evaluates a single asset in isolation and does not compare, order, or prioritize assets against each other. |
| 3 | `recommendation` | Decision | Recommendations prescribe action. SAI describes evidence-based conditions; it never tells consumers what to do. The gap between interpretation and action belongs to a future Decision Engine. |
| 4 | `target_weight` | Allocation | Target weights are portfolio allocation decisions. SAI diagnoses asset-level conditions; portfolio construction is the exclusive domain of the Portfolio Health Framework. |
| 5 | `position_size` | Allocation | Position sizing is capital allocation. SAI does not determine how much capital to commit to any asset under any circumstances. |
| 6 | `price_target` | Valuation | Price targets imply fair value knowledge and predict future prices. SAI provides valuation context but never estimates what an asset should be worth. |
| 7 | `fair_value` | Valuation | Fair value estimates require valuation models outside SAI's scope. SAI observes current pricing relative to fundamentals; it does not calculate intrinsic worth. |
| 8 | `buy/sell/hold` | Decision | Buy/sell/hold labels are trading instructions. SAI diagnoses conditions; it never instructs action. These labels collapse all diagnostic nuance into a single directional signal. |
| 9 | `probability_of_success` | Scoring | Probability estimates require predictive models. SAI is backward-looking and current-state diagnostic. It does not predict future outcomes or assign likelihoods. |
| 10 | `expected_return` | Scoring | Expected return calculations require forecasting models and risk premiums. SAI does not forecast returns or model future performance. |
| 11 | `alpha_estimate` | Scoring | Alpha implies excess return relative to a benchmark model. SAI does not model expected returns, benchmark models, or performance attribution. |
| 12 | `confidence_score` | Scoring | Confidence scores compress uncertainty into a numeric value. SAI expresses uncertainty through evidence_completeness (categorical) and deferred_dependency_notes (narrative) — never as a number. |
| 13 | `conviction_level` | Scoring | Conviction implies a directional view strength. SAI does not hold views, does not have directional bias, and does not express strength of opinion. |
| 14 | `risk_score` | Scoring | Numeric risk scores compress multi-dimensional risk into a single number. SAI expresses risk through red_flags (categorical severity with evidence) — never as a composite score. |
| 15 | `overvalued` | Valuation | "Overvalued" is a conclusion about fair value that requires valuation methodology outside SAI's scope. SAI provides valuation context but never labels assets as over/under/fairly valued. |
| 16 | `undervalued` | Valuation | "Undervalued" implies the market is wrong about pricing. SAI does not judge market correctness — it reports diagnostic context about current pricing versus available fundamentals. |
| 17 | `fairly_valued` | Valuation | "Fairly valued" implies knowledge of intrinsic value. SAI does not estimate intrinsic value or determine whether current pricing is correct. |
| 18 | `buy_signal` | Decision | Buy signals are trading triggers. SAI does not generate triggers, signals-to-action, or trading logic of any kind. |
| 19 | `sell_signal` | Decision | Sell signals are trading triggers. Same prohibition as buy_signal — SAI does not produce action signals. |
| 20 | `hold_signal` | Decision | Hold signals imply a position management instruction. SAI does not manage positions or instruct inaction any more than it instructs action. |

### Prohibition Categories Summary

| Category | Count | Principle |
|----------|-------|-----------|
| Scoring | 8 | SAI interprets evidence; it does not compress interpretation into numeric values |
| Decision | 5 | SAI diagnoses conditions; it does not prescribe actions or trading instructions |
| Allocation | 2 | SAI is asset-level diagnostic; portfolio construction is outside its boundary |
| Valuation | 5 | SAI provides valuation context; it does not estimate worth or label pricing correctness |

---

## 4. Conceptual YAML Example

> **NON-EXECUTABLE — conceptual illustration only.**
> This YAML is a human-readable representation of the output object structure. It is NOT a JSON Schema, NOT a database schema, NOT an API contract, and NOT executable in any runtime. It exists solely to illustrate field relationships for specification readers.

```yaml
# NON-EXECUTABLE — conceptual illustration only
# This is a definition-layer specification example, not implementation code

sai_block_output:
  block_id: "SAI-BLK-08"
  asset_id: "ASSET-EXAMPLE-001"
  consumed_facts:
    - "FACT-DEBT-001"
    - "FACT-DEBT-002"
    - "FACT-MATURITY-001"
    - "FACT-COVERAGE-001"
  consumed_signals:
    - "SIG-CREDIT-DETERIORATION-001"
    - "SIG-REFINANCING-RISK-001"
  interpretation_summary: >
    Credit profile shows elevated refinancing exposure with 40% of gross debt
    maturing within 18 months. Interest coverage remains adequate at 3.2x but
    has declined from 4.1x over the prior four quarters. Net debt/EBITDA at
    3.8x approaches the 4.0x covenant threshold. Bond market spreads have
    widened 85bps over 6 months, consistent with market recognition of
    deteriorating credit trajectory. No immediate solvency concern, but
    trajectory warrants close monitoring.
  red_flags:
    - flag_id: "RF-08-01"
      severity: elevated
      evidence:
        - "FACT-DEBT-002"
        - "SIG-REFINANCING-RISK-001"
      description: >
        Near-term maturity wall: 40% of gross debt matures within 18 months
        while credit spreads are widening. Refinancing at favorable terms
        may be challenged.
    - flag_id: "RF-08-02"
      severity: informational
      evidence:
        - "FACT-COVERAGE-001"
      description: >
        Interest coverage declining from 4.1x to 3.2x over four quarters.
        Still adequate but trajectory negative.
  evidence_completeness: medium
  temporal_status: current
  provenance_chain:
    source_facts:
      - "FACT-DEBT-001"
      - "FACT-DEBT-002"
      - "FACT-MATURITY-001"
      - "FACT-COVERAGE-001"
    source_signals:
      - "SIG-CREDIT-DETERIORATION-001"
      - "SIG-REFINANCING-RISK-001"
    timestamps:
      - "2026-03-31T00:00:00Z"   # Filing date for debt facts
      - "2026-06-04T16:30:00Z"   # Signal calculation timestamp
    freshness: current
  deferred_dependency_notes: null
```

> **Reminder**: The above is a conceptual illustration. It does not constitute implementation, does not define runtime behavior, and does not serve as a parseable schema. It demonstrates how the 10 allowed fields relate to each other in a single block evaluation.


---

## 5. Validation Principles (Governance Rules)

The following principles govern the validity of any SAI output object. These are stated as governance rules for artifact review and gate execution — they are NOT runtime validators, parsers, or executable code.

### Principle 1: No Orphan Interpretations

An output object is invalid if `consumed_facts` and `consumed_signals` are both empty while `evidence_completeness` is anything other than "insufficient". Every interpretation must trace to at least one piece of source evidence.

**Governance rule**: If interpretation_summary contains diagnostic content, the output must reference at least one consumed fact or signal. An interpretation without evidence provenance is architecturally invalid.

(See: requirements.md, Section: SAI-REQ-4 — Provenance Chain Requirement)

### Principle 2: No Scoring Language in Interpretation

The `interpretation_summary` field must contain only diagnostic, evidence-based language. It must never contain numeric scores, rankings, buy/sell/hold labels, price targets, probability estimates, or any language from the Prohibited Fields list (Section 3).

**Governance rule**: Any interpretation_summary that includes prohibited field concepts — even expressed as natural language rather than structured data — violates the boundary constraint.

(See: requirements.md, Section: SAI-REQ-5 — Non-Scoring / Non-Recommendation Constraint)

### Principle 3: Provenance Chain Completeness

The `provenance_chain` object must reference the same evidence items listed in `consumed_facts` and `consumed_signals`. Provenance must include at least one timestamp. The freshness value must be consistent with `temporal_status`.

**Governance rule**: provenance_chain.source_facts must be a superset of (or equal to) consumed_facts. provenance_chain.source_signals must be a superset of (or equal to) consumed_signals. Freshness and temporal_status must be consistent (both cannot simultaneously indicate contradictory states).

(See: Task 5.1 — Provenance Contract for detailed provenance specification)

### Principle 4: Red Flag Evidence Requirement

Every red flag in the `red_flags` list must reference at least one fact or signal in its `evidence` field. A red flag without evidence backing is invalid. Severity must be one of: informational, elevated, critical.

**Governance rule**: A red flag that cannot cite specific evidence is speculation, not diagnosis. Red flags are evidence-based warnings, never subjective assessments.

(See: requirements.md, Section: SAI-REQ-13 — Red Flag Taxonomy per Analysis Block)

### Principle 5: Evidence Completeness Consistency

The `evidence_completeness` value must be logically consistent with the actual evidence consumed:
- `high`: consumed_facts and consumed_signals collectively cover the block's consumption contract requirements
- `medium`: most required evidence is present but gaps or staleness exists
- `low`: significant gaps in required evidence
- `insufficient`: not enough evidence for valid interpretation

**Governance rule**: evidence_completeness must not be "high" when substantial portions of the block's fact/signal consumption contract are unmet. It must not be "insufficient" when rich evidence is available.

### Principle 6: Temporal Status Truthfulness

The `temporal_status` must accurately reflect the freshness of consumed evidence relative to the block's temporal resolution class:
- Quarterly blocks: current ≤ 100 days, stale 100–120 days, expired > 120 days
- Monthly blocks: current ≤ 35 days, stale 35–45 days, expired > 45 days
- Daily blocks: current ≤ 2 days, stale 2–5 days, expired > 5 days

**Governance rule**: temporal_status must be determined by the block's temporal resolution class and the age of the most recent consumed evidence. It cannot be set arbitrarily.

(See: design.md, Section: Temporal Resolution Design)

### Principle 7: Deferred Dependency Transparency

When a block depends on a framework that does not yet exist, `deferred_dependency_notes` must explicitly name the unavailable framework and describe how the interpretation is limited.

**Governance rule**: Silent omission of deferred dependency limitations is a governance violation. The output must be transparent about what it cannot do.

(See: design.md, Section: Error Handling — Deferred Framework Unavailability)

---

## 6. Boundary Statement

### What the Output Object IS

- A diagnostic evidence container
- A provenance-linked interpretation record
- A categorical completeness and freshness indicator
- An evidence-based warning carrier (red flags)
- A transparent limitation reporter (deferred dependency notes)

### What the Output Object IS NOT

- A score or rating
- A recommendation or instruction
- An allocation signal
- A trading trigger
- A predictive model output
- A probability estimate
- A fair value calculation
- A ranking mechanism

### Boundary Enforcement Principle

The output object boundary is absolute. No field, no interpretation_summary content, no red_flag description, and no deferred_dependency_note may cross from diagnostic territory into scoring, recommendation, allocation, or trading territory. This boundary is enforced by VG-SAI-2 (Boundary Enforcement Gate) and applies uniformly to all 24 analysis blocks.

If a downstream consumer needs scores, recommendations, or allocation decisions, those must be produced by frameworks outside SAI's boundary (future Scoring Layer, future Decision Engine, future Portfolio Optimizer). SAI provides the diagnostic foundation — never the decision.

(See: design.md, Section: Architecture Boundary)
(See: requirements.md, Section: Hard Exclusions)

---

## 7. Relationship to Fact Consumption Matrix

The `consumed_facts` field in the output object references specific fact_id values that correspond to the fact categories mapped in the Fact Consumption Matrix.

### How consumed_facts References the Matrix

1. The Fact Consumption Matrix (See: fact_consumption_matrix.md) maps 68 canonical fact categories to the 24 analysis blocks
2. Each block's consumption contract declares which fact categories it requires
3. At runtime (future implementation layer, not defined by SAI), facts from those categories would carry individual fact_id identifiers
4. The output object's `consumed_facts` field lists the specific fact_id values that were actually available and consumed for this particular evaluation
5. The provenance_chain.source_facts field mirrors this list to ensure traceability

### Coverage Relationship

- The Fact Consumption Matrix defines what a block CAN consume (the contract)
- The output object's consumed_facts records what a block DID consume (the actuality)
- The gap between contract and actuality determines evidence_completeness

(See: fact_consumption_matrix.md, Section: Fact-to-Block Mapping)
(See: requirements.md, Section: SAI-REQ-2 — Fact Consumption Contracts)

---

## 8. Relationship to Signal Consumption Matrix

The `consumed_signals` field in the output object references specific signal_id values that correspond to the signal categories mapped in the Signal Consumption Matrix.

### How consumed_signals References the Matrix

1. The Signal Consumption Matrix (See: signal_consumption_matrix.md) maps 23 canonical signal categories to the 24 analysis blocks
2. Each block's consumption contract declares which signal categories it requires
3. At runtime (future implementation layer, not defined by SAI), signals from those categories would carry individual signal_id identifiers
4. The output object's `consumed_signals` field lists the specific signal_id values that were actually available and consumed for this particular evaluation
5. The provenance_chain.source_signals field mirrors this list to ensure traceability

### Coverage Relationship

- The Signal Consumption Matrix defines what a block CAN consume (the contract)
- The output object's consumed_signals records what a block DID consume (the actuality)
- The gap between contract and actuality contributes to evidence_completeness determination

(See: signal_consumption_matrix.md, Section: Signal-to-Block Mapping)
(See: requirements.md, Section: SAI-REQ-3 — Signal Consumption Contracts)


---

## 9. Relationship to Provenance Contract

The `provenance_chain` field in the output object is the structural anchor for full evidence traceability. Task 5.1 (Create Provenance Contract) will define the detailed provenance specification, including:

- Source type taxonomy (primary/secondary/derived)
- Timestamp inheritance rules (how interpretations inherit temporal context from source evidence)
- No-orphan-interpretation enforcement mechanics
- Stale/expired status determination per temporal class
- Evidence freshness calculation methodology
- Completeness metadata derivation

### Current State

This output object specification defines the provenance_chain field structure (source_facts, source_signals, timestamps, freshness). The Provenance Contract artifact (Task 5.1) will elaborate on:

1. **Source type classification**: How to categorize evidence as primary (direct observation), secondary (derived from primary), or derived (calculated from multiple sources)
2. **Timestamp inheritance**: How the output object's temporal context is determined from source evidence timestamps
3. **Freshness determination**: How the freshness value (current/stale/expired) is calculated from evidence age and temporal resolution class thresholds
4. **Orphan detection governance**: How to identify and prevent interpretations without valid provenance
5. **Cross-block provenance independence**: How provenance chains remain block-independent (no block inherits provenance from another block's output)

### Dependency Declaration

This artifact declares the provenance_chain field structure. The Provenance Contract artifact (Task 5.1) provides the governance rules for that structure's semantic validity. Neither artifact creates implementation code.

(See: design.md, Section: Provenance Design)
(See: requirements.md, Section: SAI-REQ-4 — Provenance Chain Requirement)

---

## 10. Verification Gate Evidence Statement

This artifact provides evidence toward **VG-SAI-2 (Boundary Enforcement Gate)** only. Specifically, it contributes:

1. **Allowed fields definition**: All 10 fields are diagnostic, provenance-linked, and non-scoring
2. **Prohibited fields definition**: All 20 prohibited fields are explicitly named with rationale
3. **Boundary statement**: Explicit declaration that no scoring, recommendation, allocation, or trading logic exists in the output object specification
4. **Validation principles**: Governance rules that enforce boundary compliance without implementing runtime validators

### What This Artifact Does NOT Do

- It does NOT execute VG-SAI-2. Gate execution requires a separate verification artifact (Task 15.2) that scans ALL SAI artifacts for boundary violations.
- It does NOT pass VG-SAI-2. Passing requires the gate execution artifact to record explicit PASS with evidence covering all SAI deliverables.
- It does NOT auto-complete any verification gate. Gates are explicitly executed per verification gate governance policy.

### Evidence Contribution

This artifact can be cited as evidence during VG-SAI-2 execution:
- "output_object_spec.md defines 10 allowed fields — none are scoring/recommendation/allocation fields"
- "output_object_spec.md explicitly prohibits 20 scoring/recommendation/allocation fields with rationale"
- "output_object_spec.md conceptual YAML example contains zero prohibited field usage"
- "output_object_spec.md validation principles prohibit scoring language in interpretation_summary"

(See: tasks.md, Section: Task 15.2 — Execute VG-SAI-2 Boundary Enforcement Gate)

---

## 11. No-Drift Statement

This artifact:

- **Does NOT** contain implementation code of any kind
- **Does NOT** define JSON Schema, database schema, API schema, or any executable schema
- **Does NOT** implement runtime validation, parsing, or enforcement logic
- **Does NOT** produce scores, rankings, recommendations, or allocation signals
- **Does NOT** create facts, signals, or evidence primitives
- **Does NOT** mutate any registry, SSOT, glossary, or upstream framework
- **Does NOT** create asset-to-narrative mappings
- **Does NOT** define calculation formulas or signal derivation rules
- **Does NOT** cross the boundary from diagnostic interpretation into prescriptive action

If any future modification to this artifact introduces scoring language, recommendation logic, allocation signals, implementation code, or executable schema, that modification constitutes architectural drift and must be rejected. Report drift to ARCH authority immediately.

(See: tasks.md, Section: Task Execution Rules)
(See: design.md, Section: Architecture Boundary)

---

## Cross-Reference Index

| Reference | Location | Relationship |
|-----------|----------|-------------|
| Block Taxonomy | (See: block_taxonomy.md) | Defines the 24 blocks that produce output objects |
| Fact Consumption Matrix | (See: fact_consumption_matrix.md) | Defines what consumed_facts may reference |
| Signal Consumption Matrix | (See: signal_consumption_matrix.md) | Defines what consumed_signals may reference |
| Provenance Contract | (See: Task 5.1 — provenance_contract.md, pending) | Will define detailed provenance governance |
| Red Flag Taxonomy | (See: Task 6.1 — red_flag_taxonomy.md, pending) | Will define all red_flags entries per block |
| Temporal Resolution Matrix | (See: Task 7.1 — temporal_resolution_matrix.md, pending) | Will define temporal_status thresholds |
| SAI-REQ-5 | (See: requirements.md, Section: SAI-REQ-5) | Non-Scoring / Non-Recommendation Constraint |
| VG-SAI-2 | (See: tasks.md, Task 15.2) | Boundary Enforcement Gate — this artifact provides evidence |
| Design Output Object | (See: design.md, Section: Data Models — Output Object Design) | Source specification for this artifact |

---

*End of artifact.*
