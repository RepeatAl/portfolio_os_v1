# Single Asset Intelligence Framework — Provenance Contract

**Artifact**: provenance_contract.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 5.1 Create provenance contract
**Requirements**: SAI-REQ-4 (Provenance Chain Requirement)
**Verification Gate**: VG-SAI-3 (Provenance Chain Gate)
**Status**: Draft

---

## 1. Document Purpose

This artifact defines the canonical provenance contract that governs evidence traceability for every SAI analysis block output. It specifies:

- What provenance metadata every SAI interpretation must carry
- How source evidence is referenced and linked to upstream consumption contracts
- How temporal context is inherited from source evidence
- What constitutes an invalid orphan interpretation
- How evidence freshness is determined per temporal class
- How completeness metadata is derived from coverage gap analysis

The provenance contract ensures institutional accountability: every SAI diagnostic interpretation is traceable to specific facts and signals with full temporal context. No interpretation exists without evidence backing.

This is a definition-layer artifact. It contains no implementation code, no JSON Schema, no database schema, no API schema, no runtime validation code, and no executable logic.

(See: design.md, Section: Provenance Design)
(See: requirements.md, Section: SAI-REQ-4 — Provenance Chain Requirement)
(See: output_object_spec.md, Section: 9. Relationship to Provenance Contract)

---

## 2. Provenance Chain Fields

The provenance chain is a structured metadata object attached to every SAI block output. It contains the following fields:

### 2.1 source_fact_ids

**Definition**: A list of canonical fact identifiers consumed by the block to produce the current interpretation.

**Type**: List of strings (fact_id references)

**Constraints**:
- Each entry must reference a valid `fact_id` as defined by the Market Evidence Framework
- Each entry must correspond to a fact category that appears in the block's fact consumption contract (See: fact_consumption_matrix.md)
- The list must contain at least one entry unless `evidence_completeness` is "insufficient"
- Entries are not deduplicated — if the same fact is consumed in multiple temporal instances, each instance is referenced separately

**Relationship to fact_consumption_matrix.md**:
- The Fact Consumption Matrix defines which fact categories a block is authorized to consume (the contract)
- `source_fact_ids` records which specific fact instances were actually consumed for a given evaluation (the actuality)
- Every `source_fact_id` must belong to a fact category that is mapped to the producing block in the Fact Consumption Matrix
- A fact_id referencing a category NOT in the block's consumption contract is a provenance violation

(See: fact_consumption_matrix.md, Section: 2. Fact-to-Block Consumption Matrix)

### 2.2 source_signal_ids

**Definition**: A list of canonical signal identifiers consumed by the block to produce the current interpretation.

**Type**: List of strings (signal_id references)

**Constraints**:
- Each entry must reference a valid `signal_id` as defined by the Market Evidence Framework
- Each entry must correspond to a signal category that appears in the block's signal consumption contract (See: signal_consumption_matrix.md)
- The list must contain at least one entry unless `evidence_completeness` is "insufficient"
- Entries represent specific calculated signal instances, not signal categories

**Relationship to signal_consumption_matrix.md**:
- The Signal Consumption Matrix defines which signal categories a block is authorized to consume (the contract)
- `source_signal_ids` records which specific signal instances were actually consumed for a given evaluation (the actuality)
- Every `source_signal_id` must belong to a signal category that is mapped to the producing block in the Signal Consumption Matrix
- A signal_id referencing a category NOT in the block's consumption contract is a provenance violation

(See: signal_consumption_matrix.md, Section: 2. Signal-to-Block Consumption Matrix)


### 2.3 timestamps

**Definition**: A list of temporal markers inherited from source evidence, recording when the underlying observations were made and when calculations were performed.

**Type**: List of timestamp objects, each containing:
- `observation_timestamp`: When the underlying fact was observed or reported (e.g., filing date, market close date)
- `calculation_timestamp`: When a signal was calculated from its source facts (applicable to signals only; null for raw facts)

**Constraints**:
- At least one timestamp entry must be present in every valid provenance chain
- Observation timestamps are mandatory for all source evidence (facts and signals)
- Calculation timestamps are mandatory for signals; null/absent for raw facts
- Timestamps are inherited from source evidence — SAI does not generate timestamps
- Timestamps use ISO 8601 format (conceptual, not implementation-mandated)

**Inheritance Model**:
- Facts carry their observation_timestamp from the Market Evidence Framework (e.g., the filing date, the market close date, the announcement date)
- Signals carry both: the observation_timestamp of their source facts AND their own calculation_timestamp (when the signal was computed)
- The SAI block output inherits ALL timestamps from its consumed evidence — it does not select or filter timestamps
- The provenance chain's timestamp list is the complete temporal footprint of the interpretation

### 2.4 source_type

**Definition**: Classification of the evidence source within the provenance chain, indicating how directly the evidence relates to the observable world.

**Type**: Enum string per source evidence item

**Taxonomy**:

| Source Type | Definition | Examples |
|-------------|-----------|----------|
| `primary` | Direct observation from authoritative source. Evidence that originates from the company, regulator, exchange, or market itself without intermediate transformation. | SEC filings, earnings transcripts, exchange price data, corporate announcements, regulatory filings, audited financial statements |
| `secondary` | Evidence derived from primary sources by an authorized intermediary. Transformed or aggregated from primary observations but retaining direct lineage. | Analyst consensus estimates (aggregated from individual estimates), credit rating agency assessments (derived from financial data), index compositions (derived from exchange data) |
| `derived` | Evidence calculated from multiple primary and/or secondary sources. Produced by combining, comparing, or computing relationships between other evidence items. | Calculated signals (e.g., revenue growth signal derived from two quarterly revenue facts), composite indicators (e.g., interest coverage derived from EBIT fact and interest expense fact), relative metrics (e.g., peer-relative margin derived from company margin fact and peer margin facts) |

**Constraints**:
- Every source evidence item must be classified as exactly one source_type
- Source type is inherited from the evidence item itself — SAI does not reclassify evidence
- A block's provenance chain may contain a mix of primary, secondary, and derived sources
- Source type does not affect evidence validity — all three types are legitimate input
- Source type is informational metadata for downstream consumers (e.g., a consumer may choose to weight primary sources differently — that is a downstream decision, not SAI's)

### 2.5 evidence_freshness

**Definition**: A categorical indicator of how current the consumed evidence is relative to the producing block's temporal resolution class.

**Type**: Enum string

**Allowed Values**: `current`, `stale`, `expired`, `unknown`

**Determination Rules**:

Evidence freshness is determined by comparing the age of consumed evidence (measured from the most recent observation_timestamp in the provenance chain) against the block's temporal resolution class thresholds.

| Temporal Class | Current | Stale | Expired |
|---------------|---------|-------|---------|
| quarterly | ≤ 100 days from most recent observation | > 100 days and ≤ 120 days | > 120 days |
| monthly | ≤ 35 days from most recent observation | > 35 days and ≤ 45 days | > 45 days |
| daily | ≤ 2 days from most recent observation | > 2 days and ≤ 5 days | > 5 days |
| real-time | ≤ 1 hour from most recent observation | > 1 hour and ≤ 4 hours | > 4 hours |

**Special Value — `unknown`**:
- Used when timestamp information is unavailable or cannot be determined
- An `unknown` freshness does NOT invalidate the interpretation
- It signals that temporal status cannot be assessed — downstream consumers should treat with caution
- `unknown` should be rare; most evidence carries observation timestamps from the Market Evidence Framework

**Relationship to temporal_status in output object**:
- The `evidence_freshness` field in the provenance chain and the `temporal_status` field in the output object must be consistent
- If evidence_freshness is `current`, temporal_status must be `current`
- If evidence_freshness is `stale`, temporal_status must be `stale`
- If evidence_freshness is `expired`, temporal_status must be `expired`
- If evidence_freshness is `unknown`, temporal_status should reflect the best available assessment from other evidence in the chain

(See: design.md, Section: Temporal Resolution Design)
(See: output_object_spec.md, Section: 2. Allowed Fields — temporal_status)

### 2.6 completeness metadata

**Definition**: A qualitative indicator of how fully the block's evidence consumption contract is satisfied by the actually consumed evidence.

**Type**: Enum string

**Allowed Values**: `high`, `medium`, `low`, `insufficient`

**Derivation from Coverage Gap Analysis**:

Completeness is derived by comparing what the block's consumption contracts require (defined in fact_consumption_matrix.md and signal_consumption_matrix.md) against what was actually available and consumed:

| Completeness Level | Criteria |
|-------------------|----------|
| `high` | All required fact categories AND all required signal categories from the block's consumption contracts are represented in source_fact_ids and source_signal_ids. Evidence is current (not stale or expired). Full interpretation is possible. |
| `medium` | Most required evidence is present but one or more of: (a) some fact/signal categories from the consumption contract are missing, (b) some evidence is stale but not expired, (c) a deferred framework dependency limits scope. Interpretation is valid but limited. |
| `low` | Significant gaps exist in required evidence. Multiple fact/signal categories from the consumption contract are unmet. Interpretation is materially constrained and should be consumed with awareness of limitations. |
| `insufficient` | Not enough evidence exists for a valid interpretation. The block cannot produce meaningful diagnostic output. This is the ONLY completeness level that permits empty source_fact_ids AND empty source_signal_ids simultaneously. |

**Constraints**:
- Completeness is categorical ONLY — it is NOT a numeric score
- Completeness must NOT map to action recommendations (insufficient ≠ "do not invest")
- Completeness must NOT be used for ranking assets by data quality
- Stale evidence degrades completeness: evidence that is `stale` may reduce completeness from `high` to `medium`; evidence that is `expired` may reduce completeness from `medium` to `low`
- Completeness reflects the gap between contract (what is required) and actuality (what is available)

**Relationship to evidence_completeness in output object**:
- The `completeness` metadata in the provenance chain governs the `evidence_completeness` field in the output object
- They must be consistent — the output object's evidence_completeness is derived from provenance chain completeness analysis

(See: requirements.md, Section: SAI-REQ-15 — Evidence Sufficiency / Completeness Indicator)
(See: output_object_spec.md, Section: 2. Allowed Fields — evidence_completeness)


---

## 3. No-Orphan-Interpretation Rule

### 3.1 Rule Statement

**An interpretation without provenance is invalid.** Every SAI block output that contains diagnostic content in its `interpretation_summary` field must trace to at least one consumed fact or signal. No interpretation may exist as an orphan — detached from evidence provenance.

This is an architectural validity rule, not a runtime enforcement mechanism. SAI does not implement runtime validators or parsers. The rule is enforced through governance review, verification gate execution (VG-SAI-3), and structural audit.

### 3.2 Definition of an Orphan Interpretation

An SAI block output constitutes an **orphan interpretation** when ALL of the following conditions are simultaneously true:

1. `source_fact_ids` is empty (zero fact references in provenance chain)
2. `source_signal_ids` is empty (zero signal references in provenance chain)
3. `evidence_completeness` is NOT "insufficient"

**Rationale for condition 3**: When evidence_completeness is "insufficient", the block is explicitly declaring that it cannot produce a meaningful interpretation due to lack of evidence. This is a valid state — the block is transparent about its limitation. An orphan occurs when the block claims to have sufficient evidence (completeness = high/medium/low) but provides no provenance linkage to actual evidence. That is the architectural violation.

### 3.3 Valid States (Not Orphans)

The following states are architecturally VALID and do NOT constitute orphan interpretations:

| source_fact_ids | source_signal_ids | evidence_completeness | Valid? | Reason |
|-----------------|-------------------|-----------------------|--------|--------|
| Non-empty | Non-empty | high/medium/low | YES | Full provenance present |
| Non-empty | Empty | high/medium/low | YES | Fact-only provenance is valid (some blocks may not require signals in all evaluations) |
| Empty | Non-empty | high/medium/low | YES | Signal-only provenance is valid (some blocks may rely entirely on calculated signals) |
| Empty | Empty | insufficient | YES | Block transparently declares it cannot produce interpretation |
| Non-empty | Non-empty | insufficient | YES | Evidence exists but is so degraded/stale that interpretation is unreliable — block is transparent |

### 3.4 Invalid States (Orphan Interpretations)

| source_fact_ids | source_signal_ids | evidence_completeness | Valid? | Violation |
|-----------------|-------------------|-----------------------|--------|-----------|
| Empty | Empty | high | NO | Claims high completeness with zero evidence — architectural violation |
| Empty | Empty | medium | NO | Claims medium completeness with zero evidence — architectural violation |
| Empty | Empty | low | NO | Claims low completeness with zero evidence — even low requires SOME evidence |

### 3.5 Governance Consequence

An orphan interpretation is **architecturally invalid**. It represents a governance-level defect in the block's provenance chain. Consequences:

- The output is considered malformed at the specification level
- VG-SAI-3 (Provenance Chain Gate) will FAIL if orphan interpretation paths exist in any block's specification
- The defect must be corrected by either: (a) providing proper evidence references, or (b) setting evidence_completeness to "insufficient" if no evidence is genuinely available
- SAI does NOT implement runtime rejection of orphans — this is a governance/audit concern, not a runtime concern

**Important**: The no-orphan rule is enforced at the governance layer. It is NOT auto-rejected by runtime. There is no runtime validator that rejects orphan outputs. The rule exists for architectural integrity and is verified during gate execution.

(See: requirements.md, Section: SAI-REQ-4 — Acceptance Criterion 2: "No-orphan-interpretation rule is explicitly stated and enforceable")
(See: output_object_spec.md, Section: 5. Validation Principles — Principle 1: No Orphan Interpretations)

---

## 4. Timestamp Inheritance Rules

### 4.1 Inheritance Principle

SAI interpretations do not generate their own timestamps. They inherit temporal context entirely from the evidence they consume. The provenance chain's timestamp list represents the complete temporal footprint of all consumed evidence — it tells downstream consumers exactly when the underlying observations and calculations occurred.

### 4.2 Inheritance Model

| Source Type | What Timestamps Are Inherited |
|-------------|-------------------------------|
| Facts (primary) | observation_timestamp only — the date/time when the fact was observed or reported (e.g., filing date, market close, announcement date) |
| Facts (secondary) | observation_timestamp of the intermediary's publication (e.g., when the analyst consensus was published) |
| Signals (derived) | Both: (a) the observation_timestamps of the underlying facts that fed the signal calculation, AND (b) the calculation_timestamp when the signal was computed |

### 4.3 Timestamp Precedence Rules

When determining the block output's `temporal_status` from the inherited timestamps:

1. **Most recent observation_timestamp governs freshness**: The age of the evidence is measured from the MOST RECENT observation_timestamp in the provenance chain to the current evaluation time. This determines whether the evidence is current, stale, or expired.

2. **Oldest observation_timestamp indicates temporal span**: The OLDEST timestamp in the chain indicates how far back the evidence reaches. This is informational — it does not govern freshness classification.

3. **Calculation timestamps do not override observation timestamps for freshness**: A signal may have been calculated recently (fresh calculation_timestamp) but from stale underlying facts (old observation_timestamps). In this case, the evidence freshness is determined by the underlying fact observation timestamps, NOT the calculation timestamp.

4. **Rationale for "most recent governs"**: The most recent observation represents the latest data point available to the block. If the most recent evidence is stale, the interpretation as a whole is based on stale information — regardless of older historical data that may also be consumed.

### 4.4 How Timestamps Determine temporal_status

The output object's `temporal_status` field is derived from the provenance chain's timestamps using this process:

1. Identify the block's temporal resolution class (quarterly/monthly/daily/real-time) from the Block Taxonomy
2. Identify the most recent `observation_timestamp` across all entries in the provenance chain
3. Calculate the elapsed time between that most recent timestamp and the current evaluation time
4. Compare the elapsed time against the thresholds for the block's temporal class:
   - If elapsed ≤ current threshold → `temporal_status` = "current"
   - If elapsed > current threshold AND ≤ expired threshold → `temporal_status` = "stale"
   - If elapsed > expired threshold → `temporal_status` = "expired"
5. If no valid observation_timestamp exists in the provenance chain → `temporal_status` determination falls to `evidence_freshness` = "unknown"

### 4.5 Cross-Block Provenance Independence

Each block's provenance chain is independent. Timestamps are NOT inherited across blocks:
- Block A's timestamps do not influence Block B's temporal_status
- No block inherits provenance from another block's output
- Each block independently inherits timestamps from its own consumed facts and signals
- Cross-block temporal synthesis is a downstream consumer concern, not SAI's responsibility

(See: design.md, Section: Block Independence Design)
(See: requirements.md, Section: SAI-REQ-4 — Acceptance Criterion 4: "Timestamp inheritance model documented")


---

## 5. Stale/Expired Status Handling

### 5.1 Thresholds per Temporal Class

Evidence freshness thresholds are defined per temporal resolution class. These thresholds determine when consumed evidence transitions from `current` to `stale` to `expired`.

| Temporal Class | Current Threshold | Stale Threshold | Expired Threshold | Typical Blocks |
|---------------|-------------------|-----------------|-------------------|----------------|
| quarterly | ≤ 100 days | > 100 days, ≤ 120 days | > 120 days | SAI-BLK-01 through SAI-BLK-16, SAI-BLK-22, SAI-BLK-23 (Foundation, Operational, Financial Stability, Risk, Earnings, Outlook) |
| monthly | ≤ 35 days | > 35 days, ≤ 45 days | > 45 days | SAI-BLK-11 (Working Capital — if upgraded to monthly cadence) |
| daily | ≤ 2 days | > 2 days, ≤ 5 days | > 5 days | SAI-BLK-17 through SAI-BLK-21, SAI-BLK-24 (Valuation, Market Position, Portfolio Fit) |
| real-time | ≤ 1 hour | > 1 hour, ≤ 4 hours | > 4 hours | None by default — reserved for future streaming signals |

### 5.2 Stale Evidence Handling

When consumed evidence is classified as `stale`:

1. **Interpretation is RETAINED** — SAI continues to produce its diagnostic output
2. **Interpretation is FLAGGED** — `temporal_status` is set to "stale" in the output object; `evidence_freshness` is set to "stale" in the provenance chain
3. **Completeness may be degraded** — Evidence staleness may reduce `evidence_completeness` from "high" to "medium" at governance discretion (staleness introduces uncertainty about current accuracy)
4. **Interpretation remains valid** — A stale interpretation is still diagnostically meaningful; it represents the most recent available assessment even if evidence has aged past the current threshold
5. **No suppression occurs** — SAI does NOT suppress, hide, or remove stale outputs from its results

**Principle**: Staleness is informative, not prohibitive. A stale interpretation with transparent temporal_status is more valuable than a missing interpretation with no diagnostic content.

### 5.3 Expired Evidence Handling

When consumed evidence is classified as `expired`:

1. **Interpretation is RETAINED** — SAI continues to produce its diagnostic output even with expired evidence
2. **Interpretation is explicitly marked** — `temporal_status` is set to "expired" in the output object; `evidence_freshness` is set to "expired" in the provenance chain
3. **Completeness is degraded** — Evidence expiration reduces `evidence_completeness` (typically from "high"/"medium" to "low")
4. **Interpretation carries a clear limitation** — The interpretation reflects conditions that existed at the time of the expired evidence, not necessarily current conditions
5. **No suppression occurs** — SAI does NOT suppress expired outputs. An expired interpretation explicitly communicating its temporal limitation is preferable to no interpretation at all

**Principle**: Expiration does not mean the interpretation is false — it means the interpretation's temporal validity has degraded beyond reliable freshness. The underlying diagnostic may still hold true; SAI cannot confirm or deny that without fresher evidence.

### 5.4 SAI Does NOT Suppress Stale or Expired Outputs

This principle is stated explicitly to prevent scope drift:

- SAI does NOT suppress outputs based on staleness or expiration
- SAI does NOT filter, remove, or conditionally omit outputs that are temporally degraded
- SAI does NOT implement "do not show if stale" logic
- SAI produces the interpretation with full transparency about its temporal status
- Downstream consumers decide how to handle stale/expired information — that decision is NOT SAI's responsibility

**Rationale**: Suppression creates invisible gaps. A downstream consumer that receives no output cannot distinguish between "no evidence exists" and "evidence existed but was too old." Transparent temporal flagging preserves information; suppression destroys it.

### 5.5 SAI Does NOT Refresh Evidence

This principle is stated explicitly to define SAI's responsibility boundary:

- SAI is NOT responsible for data freshness
- SAI does NOT trigger evidence refresh operations
- SAI does NOT request updated facts or signals from upstream frameworks
- SAI does NOT schedule or initiate data pipeline operations
- SAI consumes whatever evidence is available at evaluation time and reports its temporal status truthfully

**Rationale**: Evidence freshness is the responsibility of the Data Ingestion/Normalization Framework and the Signal Calculation Framework. SAI is a diagnostic consumer, not a data acquisition system. Conflating these responsibilities would violate SAI's architectural boundary.

(See: design.md, Section: Error Handling — Stale Evidence)
(See: design.md, Section: Temporal Resolution Design)

---

## 6. Relationship to output_object_spec.md

### 6.1 provenance_chain Field Mapping

The `provenance_chain` field in the SAI output object (defined in output_object_spec.md, Section 2, Field #9) is the structural instantiation of this contract. The mapping is:

| Provenance Contract Field | Output Object provenance_chain Sub-field | Notes |
|--------------------------|------------------------------------------|-------|
| source_fact_ids | provenance_chain.source_facts | Same content; naming convention difference between contract (semantic) and output object (structural) |
| source_signal_ids | provenance_chain.source_signals | Same content; naming convention difference |
| timestamps | provenance_chain.timestamps | List of observation/calculation timestamps inherited from source evidence |
| evidence_freshness | provenance_chain.freshness | Categorical value (current/stale/expired) determined by this contract's rules |
| source_type | (per-item metadata) | Applies to each source_fact and source_signal individually; not a single top-level field |
| completeness | (mapped to evidence_completeness in output object) | Governs the output object's top-level `evidence_completeness` field |

### 6.2 evidence_completeness Governance

The output object's `evidence_completeness` field (Field #7) is governed by this contract's completeness metadata rules (Section 2.6). The completeness value in the output object must be consistent with the provenance chain's coverage gap analysis.

### 6.3 temporal_status Governance

The output object's `temporal_status` field (Field #8) is governed by this contract's timestamp inheritance rules (Section 4) and stale/expired handling rules (Section 5). The temporal_status must be derivable from the provenance chain's timestamps using the block's temporal resolution class thresholds.

(See: output_object_spec.md, Section: 2. Allowed Fields)
(See: output_object_spec.md, Section: 5. Validation Principles — Principle 3: Provenance Chain Completeness)
(See: output_object_spec.md, Section: 5. Validation Principles — Principle 6: Temporal Status Truthfulness)

---

## 7. Relationship to fact_consumption_matrix.md

### 7.1 Contract Enforcement Principle

The `source_fact_ids` in every provenance chain must reference facts that belong to fact categories mapped to the producing block in the Fact Consumption Matrix.

- The Fact Consumption Matrix defines the **authorized fact scope** per block
- The provenance chain's source_fact_ids record the **actual fact consumption** per evaluation
- A provenance chain that references a fact category NOT authorized for the block is a contract violation
- A provenance chain that references NO facts (when completeness is not "insufficient") violates the no-orphan rule

### 7.2 Primary vs. Secondary Consumption

The Fact Consumption Matrix distinguishes between primary and secondary fact consumers. In the provenance chain:

- Facts consumed as PRIMARY evidence for the block are expected in most evaluations (they are the block's core diagnostic input)
- Facts consumed as SECONDARY evidence are contextual and may not appear in every evaluation
- Both primary and secondary consumed facts appear in source_fact_ids without distinction — the provenance chain records all consumed evidence regardless of its primary/secondary designation in the matrix

(See: fact_consumption_matrix.md, Section: 2. Fact-to-Block Consumption Matrix)

---

## 8. Relationship to signal_consumption_matrix.md

### 8.1 Contract Enforcement Principle

The `source_signal_ids` in every provenance chain must reference signals that belong to signal categories mapped to the producing block in the Signal Consumption Matrix.

- The Signal Consumption Matrix defines the **authorized signal scope** per block
- The provenance chain's source_signal_ids record the **actual signal consumption** per evaluation
- A provenance chain that references a signal category NOT authorized for the block is a contract violation
- A provenance chain that references NO signals (when source_fact_ids is also empty and completeness is not "insufficient") contributes to orphan interpretation status

### 8.2 Primary vs. Secondary Consumption

As with facts, the Signal Consumption Matrix distinguishes primary and secondary signal consumers. Both primary and secondary consumed signals appear in source_signal_ids. The distinction is relevant for coverage gap analysis (missing primary signals degrade completeness more than missing secondary signals) but does not affect provenance chain validity.

(See: signal_consumption_matrix.md, Section: 2. Signal-to-Block Consumption Matrix)


---

## 9. Governance Invalidity Statement

### 9.1 Missing Provenance = Invalid Interpretation

An SAI block output that lacks provenance is **architecturally invalid** at the governance level. Specifically:

- An interpretation without `source_fact_ids` AND without `source_signal_ids` (while `evidence_completeness` is not "insufficient") is a governance-level defect
- Missing provenance does not mean the interpretation is factually wrong — it means the interpretation cannot be verified, traced, or audited
- Unverifiable interpretations violate the institutional accountability principle that underpins SAI's design

### 9.2 Governance-Level Enforcement, Not Runtime Enforcement

This contract defines provenance requirements at the **governance layer**:

- Provenance validity is assessed during verification gate execution (VG-SAI-3)
- Provenance validity is assessed during architectural audit and review
- Provenance validity is NOT enforced by runtime validators, auto-rejectors, or parsers
- There is no runtime system that intercepts and rejects outputs with invalid provenance

**Rationale**: Runtime enforcement is an implementation-layer concern. SAI is currently at the definition layer. When SAI progresses to implementation (future, not this spec), runtime enforcement may be added. At this layer, governance rules define what is valid; they do not implement validation.

### 9.3 Institutional Accountability

The provenance contract exists to support institutional accountability:

- Any diagnostic interpretation can be challenged by asking: "What evidence supports this?"
- The answer is always available in the provenance chain: specific fact IDs, specific signal IDs, specific timestamps
- If the answer is "no evidence" but the interpretation claims completeness, the architectural contract is violated
- This traceability supports human oversight, audit, and challenge processes

(See: requirements.md, Section: SAI-REQ-4 — Acceptance Criterion 5: "An interpretation without evidence provenance is explicitly declared invalid")

---

## 10. Verification Gate Evidence Statement

This artifact provides evidence toward **VG-SAI-3 (Provenance Chain Gate)** only. Specifically, it contributes:

1. **Provenance chain field specification**: All 6 provenance metadata fields defined (source_fact_ids, source_signal_ids, timestamps, source_type, evidence_freshness, completeness)
2. **No-orphan-interpretation rule**: Explicitly stated with formal definition of what constitutes an orphan (Section 3)
3. **Timestamp inheritance model**: Documented with precedence rules and cross-block independence (Section 4)
4. **Stale/expired handling**: Thresholds defined per temporal class with explicit non-suppression and non-refresh principles (Section 5)
5. **Consumption matrix linkage**: Provenance chain references validated against fact and signal consumption contracts (Sections 7, 8)
6. **Governance enforcement boundary**: Provenance validity is governance-level, not runtime-enforced (Section 9)

### What This Artifact Does NOT Do

- It does NOT execute VG-SAI-3. Gate execution requires a separate verification artifact (Task 15.3) that validates provenance specification completeness across ALL 24 blocks.
- It does NOT pass VG-SAI-3. Passing requires the gate execution artifact to confirm that every block has a valid provenance path with no orphan interpretation routes.
- It does NOT auto-complete any verification gate. Gates are explicitly executed per verification gate governance policy.

### Evidence Contribution

This artifact can be cited as evidence during VG-SAI-3 execution:
- "provenance_contract.md defines all 6 provenance chain fields with constraints and relationships"
- "provenance_contract.md explicitly states the no-orphan-interpretation rule with formal orphan definition"
- "provenance_contract.md documents timestamp inheritance model with precedence and cross-block independence"
- "provenance_contract.md defines stale/expired thresholds for all 4 temporal classes"
- "provenance_contract.md links provenance to fact_consumption_matrix.md and signal_consumption_matrix.md"
- "provenance_contract.md declares governance-level enforcement without runtime auto-rejection"

(See: tasks.md, Section: Task 15.3 — Execute VG-SAI-3 Provenance Chain Gate)

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
- **Does NOT** implement provenance validators, timestamp parsers, or freshness calculators
- **Does NOT** cross the boundary from diagnostic interpretation into prescriptive action

If any future modification to this artifact introduces scoring language, recommendation logic, allocation signals, implementation code, executable schema, or runtime enforcement logic, that modification constitutes architectural drift and must be rejected. Report drift to ARCH authority immediately.

(See: tasks.md, Section: Task Execution Rules)
(See: design.md, Section: Architecture Boundary)

---

## Cross-Reference Index

| Reference | Location | Relationship |
|-----------|----------|-------------|
| Block Taxonomy | (See: block_taxonomy.md) | Defines the 24 blocks whose outputs carry provenance chains |
| Fact Consumption Matrix | (See: fact_consumption_matrix.md) | Defines authorized fact scope per block — source_fact_ids must reference facts within scope |
| Signal Consumption Matrix | (See: signal_consumption_matrix.md) | Defines authorized signal scope per block — source_signal_ids must reference signals within scope |
| Output Object Specification | (See: output_object_spec.md) | Defines the provenance_chain field structure that this contract governs |
| Temporal Resolution Matrix | (See: Task 7.1 — temporal_resolution_matrix.md, pending) | Will define temporal class assignment per block — governs freshness thresholds |
| SAI-REQ-4 | (See: requirements.md, Section: SAI-REQ-4) | Provenance Chain Requirement — this artifact's governing requirement |
| VG-SAI-3 | (See: tasks.md, Task 15.3) | Provenance Chain Gate — this artifact provides evidence toward |
| Design Provenance Section | (See: design.md, Section: Provenance Design) | Source specification for provenance chain fields |
| Design Temporal Resolution | (See: design.md, Section: Temporal Resolution Design) | Source specification for freshness thresholds |
| Design Error Handling | (See: design.md, Section: Error Handling — Stale Evidence) | Source specification for stale/expired handling principles |
| Design Block Independence | (See: design.md, Section: Block Independence Design) | Source for cross-block provenance independence principle |

---

*End of artifact.*
