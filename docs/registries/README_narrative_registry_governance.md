# Narrative Registry Governance

## Purpose

This document is a **supplementary governance guide** for the Narrative Registry (`docs/registries/narrative_registry.yaml`). It defines procedures for creating, amending, transitioning, deprecating, and retiring narrative registry entries.

**Narrative Framework v2 (`docs/README_narrative_framework.md`) is the ontology SSOT.** It defines WHAT a narrative IS. This governance document defines HOW narratives are registered, maintained, and retired within the registry. It does not redefine narrative theory, lifecycle semantics, or ontological boundaries.

The Narrative Registry stores WHICH narratives officially exist in Portfolio OS. This governance document ensures that the registry remains clean, auditable, and free of unauthorized mutations.

(See: README_narrative_framework, Section: 4. What Is a Narrative?)
(See: README_narrative_framework, Section: 6. Narrative Lifecycle State Machine)
(See: README_narrative_framework, Section: 13. Extension Criteria)

---

## How to Use This Document

This governance guide is referenced by:

- **ARCH domain** — when proposing new narratives or amending existing entries
- **GOV domain** — when reviewing proposals for governance compliance
- **Any consumer** — when verifying that a registry entry followed proper procedure

**Workflow**: Before any registry mutation, the responsible party MUST consult the relevant procedure section below and follow ALL steps in order. No steps may be skipped. No procedure may be abbreviated.

**Authority model**:
- ARCH domain: proposes entries, executes amendments, executes lifecycle transitions
- GOV domain: reviews proposals for compliance, concurs on conflict resolution

---

## ⚠️ No-Population Warning

**This file defines governance procedures only. Population of the Narrative Registry (adding actual narrative entries) requires a separate authorized spec.**

The governance procedures described here are structural definitions. They do NOT authorize any party to add narrative entries to the `narratives: []` list. A dedicated population spec must be created, reviewed, and approved before any entries are registered.

---

## ⚠️ No Scoring / Ranking / Probability Warning

**The Narrative Registry contains NO numeric scoring, weighting, ranking, probabilities, confidence values, optimization logic, or portfolio allocation logic.**

These belong to future implementation phases that CONSUME the registry — not to the registry itself. Weights on an incomplete model produce false confidence. The Registry defines WHICH narratives exist. Numeric precision belongs to future implementation phases.

Prohibited fields include: `score`, `weight`, `numeric_strength`, `probability`, `confidence`, `rank`, `priority_order`, `asset_list`, `ticker_symbols`, `correlation_matrix`, `recommendation`, `numeric_threshold`, `membership_weight`.

---

## Creation Procedure

The following procedure MUST be followed when proposing a new narrative for registration.

### Step 1: Proposal

The **Proposer** (ARCH domain) drafts a candidate entry with ALL required fields:

- `narrative_id`: Format `narrative.[descriptive_token]` — lowercase, underscore-separated, language-neutral
- `scope_definition`: Text describing the shared market belief structure
- `birth_trigger`: Canonical `sc.*` State_Change ID referencing a real, identifiable market event
- `connected_systems`: List of `system.*` IDs (minimum 1)
- `falsification_condition`: Concrete, testable condition that would invalidate the narrative
- `lifecycle_state`: Must be `narrative.lifecycle.emerging` (no other initial state permitted)
- `registered_date`: ISO 8601 date
- `registered_by`: Authority role (ARCH)
- `last_modified`: ISO 8601 date

### Step 2: Collision Check

Before registration, the proposed entry MUST pass the Collision Check procedure (see dedicated section below). If collision is detected, the proposal is REJECTED until resolved.

### Step 3: Inclusion Criteria Gate

ALL 4 inclusion criteria must be satisfied (conjunctive — partial satisfaction is insufficient):

1. **Distinct shared belief** — not already covered by an existing registry entry
2. **Falsifiable** — explicit falsification condition stated (vague conditions like "loses relevance" are invalid)
3. **Connects State_Change to System** — at least one `sc.*` trigger connected to at least one `system.*`
4. **Has canonical ID** — assigned `narrative.*` ID before first use

Evidence for each criterion MUST be documented at registration time.

(See: README_narrative_framework, Section: 13. Extension Criteria)

### Step 4: GOV Review

The **GOV domain** performs a governance compliance check:

- Naming rules followed (lowercase, underscore-separated, language-neutral token)
- No future-leak (no prohibited fields present)
- Evidence quality sufficient (birth trigger references real market event)
- No unauthorized scope expansion

### Step 5: Registration

Upon passing all gates, the entry is added to the `narratives` list with:
- `lifecycle_state: narrative.lifecycle.emerging`
- All required fields populated
- `registered_date` set to current date

### Step 6: Artifact Registry Update

Not required per individual entry. The registry file is already registered as a whole in `.domainization/artifact_registry.yaml`.

---

## Collision Check Procedure

The Collision Check prevents namespace pollution and semantic duplication. It MUST be performed before every new narrative registration.

### Step 1: Extract Token

Extract the proposed `narrative_id` token (the portion after `narrative.`).

### Step 2: Exact Match Check

Search ALL existing `narrative.*` IDs in the registry for an identical token.

- **If exact match found**: REJECT immediately. The proposed ID already exists.

### Step 3: Semantic Overlap Check

Review the `scope_definition` of ALL existing entries for overlapping belief structures.

- **If overlap detected**: The proposer must either:
  - (a) Narrow scope to clearly differentiate from the existing entry, OR
  - (b) Withdraw the proposal in favor of the existing entry
- **If overlap is partial**: Consider parent/sub-narrative hierarchy via `parent_narrative` field
- **If genuinely different but confusingly similar**: Require proposer to differentiate via scope refinement

### Step 4: Result

- **PASS**: No collision detected (exact or semantic). Proceed to Inclusion Criteria Gate.
- **REJECT**: Collision found. Explanation of the collision MUST be documented. Proposer must resolve before re-submitting.

---

## Amendment Procedure

Amendments modify existing registry entries. Not all fields are mutable. The following table defines amendment rules:

### Mutable Fields

| Field | Amendment Rule | Authority |
|-------|---------------|-----------|
| `scope_definition` | May be refined (narrowed/clarified), NOT expanded | ARCH |
| `connected_systems` | Additive only — new systems may be added, never removed without deprecation | ARCH |
| `falsification_condition` | May be refined (made more specific), NOT weakened | ARCH |
| `display_name` | Freely changeable (rendering only, not identity) | ARCH or GOV |
| `velocity` | May be updated with documented evidence | ARCH |
| `evidence_summary` | May be updated/expanded | ARCH |
| `related_narratives` | May be added/removed | ARCH |

### Immutable Fields

| Field | Rule | Rationale |
|-------|------|-----------|
| `narrative_id` | IMMUTABLE — cannot be changed, reassigned, or recycled | Canonical identity must be stable for all downstream consumers |
| `birth_trigger` | IMMUTABLE — historical fact | The originating State_Change is a historical event that cannot be altered |
| `registered_date` | IMMUTABLE — historical fact | Registration date is a fixed historical record |

### Amendment Requirements

- Every amendment MUST update `last_modified` to the current date
- Every amendment MUST be performed by an authorized role (see Authority column)
- Scope expansion is PROHIBITED — scope may only be narrowed or clarified
- System removal from `connected_systems` requires full deprecation procedure, not simple amendment

---

## Lifecycle Transition Procedure

Lifecycle transitions change a narrative's `lifecycle_state` field. They are governance-controlled mutations requiring evidence and authorization.

Valid lifecycle states (per Narrative Framework v2, Section 6):
- `narrative.lifecycle.emerging`
- `narrative.lifecycle.strengthening`
- `narrative.lifecycle.dominant`
- `narrative.lifecycle.weakening`
- `narrative.lifecycle.dormant`
- `narrative.lifecycle.dead`

### Step 1: Trigger Identification

A **State_Change** occurs that qualifies as a lifecycle transition trigger per Narrative Framework v2 Section 6.

- Only State_Changes cause transitions
- Signals may DETECT evidence of lifecycle transitions but CANNOT trigger them
- No automated/programmatic transitions are permitted

(See: README_narrative_framework, Section: 6. Narrative Lifecycle State Machine)
(See: README_narrative_framework, Section: 14. Signal-Narrative Relationship)

### Step 2: Evidence Documentation

ARCH documents:
- The specific State_Change reference (canonical `sc.*` ID)
- How the State_Change satisfies the transition criteria defined in Narrative Framework v2
- Why the current lifecycle state is no longer accurate

### Step 3: Transition Execution

ARCH updates `lifecycle_state` to the new value. Only valid transitions per the lifecycle state machine are permitted.

### Step 4: Audit Record

A new entry is APPENDED to `lifecycle_history` with:

```yaml
- from: narrative.lifecycle.[previous_state]
  to: narrative.lifecycle.[new_state]
  date: "YYYY-MM-DD"
  trigger: sc.[category].[subcategory].[event]
  authorized_by: ARCH
  evidence: "Description of why the State_Change qualifies as transition trigger"
```

Audit records are APPEND-ONLY — previous records cannot be modified or deleted.

### Step 5: Last Modified Update

`last_modified` is updated to the current date.

### Step 6: Prohibition

The following are explicitly prohibited:
- Automated/programmatic lifecycle transitions
- Signal-triggered transitions (signals detect, they do not cause)
- Transitions without a documented State_Change reference
- Transitions without ARCH authorization
- Skipping the audit record step

---

## Deprecation Procedure

Deprecation marks a narrative as no longer valid but retains it permanently in the registry for historical reference.

### Step 1: Trigger

Deprecation is triggered when:
- The **falsification condition** is met (the narrative has been proven invalid), OR
- The narrative is **superseded** by a more accurate explanation

### Step 2: Evidence

ARCH documents the State_Change that proves falsification or supersession:
- Canonical `sc.*` ID of the triggering event
- How the event satisfies the falsification condition or proves supersession
- If superseded: identify the replacement narrative

### Step 3: Transition

Set `lifecycle_state: narrative.lifecycle.dead`

Follow the full Lifecycle Transition Procedure (Steps 1-6 above) for the state change to `dead`.

### Step 4: Additional Fields

Add the following fields to the deprecated entry:
- `deprecated_date`: ISO 8601 date of deprecation
- `deprecation_reason`: Text explaining why the narrative was deprecated
- `replacement_narrative_id`: The `narrative.*` ID of the replacing narrative (if applicable; null if simply falsified)

### Step 5: Retention

**Deprecated entries remain in the registry permanently.** They are NEVER deleted. This ensures:
- Historical auditability
- Downstream consumers can detect the deprecation
- The narrative ID remains reserved (never reassigned)

### Step 6: ID Preservation

A deprecated `narrative.*` ID is NEVER reassigned or recycled. The ID remains permanently reserved even after the narrative is proven invalid.

---

## Retirement Procedure

Retirement moves a deprecated narrative from active queries to an archive section. It is a housekeeping action, not a governance decision about validity.

### Step 1: Prerequisite

The entry MUST be in `narrative.lifecycle.dead` state for a minimum **cooling period of 90 days**.

- If the cooling period has not elapsed, retirement is NOT permitted
- The cooling period begins on the `deprecated_date`

### Step 2: Action

Move the entry from the `narratives` list to the `retired_narratives` section in the same file.

### Step 3: Effect

- The retired entry is excluded from active queries
- The entry remains in the file for historical reference
- All fields are preserved as-is (no data loss)

### Step 4: ID Preservation

Retired IDs are NEVER reassigned. They remain permanently reserved in the namespace. No future narrative may reuse a retired `narrative.*` ID.

---

## Conflict and Duplicate Handling

When overlapping or duplicate narratives are detected (during Collision Check or ongoing registry review):

### Resolution Hierarchy

1. **If scopes are identical**: Reject the newer entry; point to the existing entry
2. **If one is more specific**: Keep the more specific; consider making the broader one a parent via `parent_narrative` field
3. **If genuinely different but confusingly similar**: Require the proposer to differentiate via scope refinement

### Authority

- ARCH proposes the resolution
- GOV concurs with the resolution

### Documentation

Record conflict resolution in the `evidence_summary` field of the surviving entry.

---

## Cross-References

### Ontology SSOT

**Narrative Framework v2 (`docs/README_narrative_framework.md`) is the ontology SSOT for all narrative-related concepts.** The Narrative Registry defers to Framework v2 for:

- What a narrative IS (Section 4)
- Valid lifecycle states and transitions (Section 6)
- Extension/inclusion criteria (Section 13)
- Signal-narrative relationship boundaries (Section 14)
- Exclusion constraints (Section 15)

The Narrative Registry does NOT redefine, extend, or contradict Framework v2.

### Referenced Deliverables

| Deliverable | Section Referenced | Context |
|-------------|-------------------|---------|
| README_narrative_framework | Section 4: What Is a Narrative? | ID namespace rules, narrative definition |
| README_narrative_framework | Section 6: Lifecycle State Machine | Valid lifecycle states and transitions |
| README_narrative_framework | Section 13: Extension Criteria | Inclusion/exclusion criteria for registration |
| README_narrative_framework | Section 15: Exclusion Constraints | Prohibited fields rationale |
| README_market_organism_principles | Principle 2: Root Node Invariant | State_Change as causal root |
| README_state_change_taxonomy | Classification Hierarchy | Birth trigger format (`sc.*`) |
| README_dependency_types_v2 | Narrative | `dep.narrative` distinction |
| README_temporal_taxonomy | Temporal Property Enumeration | Expected duration values |
| README_shared_glossary_reference | Glossary Usage Rules | Glossary-first policy |

### ID Reference Formats

| Reference Type | Format | Source |
|---------------|--------|--------|
| Narrative ID | `narrative.[token]` | Narrative Framework v2, Section 4 |
| Lifecycle state | `narrative.lifecycle.[state]` | Narrative Framework v2, Section 6 |
| State_Change | `sc.[category].[subcategory].[event]` | README_state_change_taxonomy |
| System | `system.[name]` | README_expansion_taxonomy |
| Dependency_Type | `dep.[type]` | README_dependency_types_v2 |
| Temporal duration | Valid Temporal_Taxonomy value | README_temporal_taxonomy |

### Document Cross-Reference Format

All references to external documents within the registry use the format:

```
(See: [Deliverable_Name], Section: [Section_Title])
```

---

## Summary of Governance Constraints

| Constraint | Rule |
|-----------|------|
| Population | NOT authorized by this document — requires separate spec |
| Scoring/Ranking | PROHIBITED — no numeric values in registry |
| Automated transitions | PROHIBITED — human authorization required |
| ID mutation | PROHIBITED — narrative IDs are immutable |
| Scope expansion | PROHIBITED — scope may only be narrowed |
| Entry deletion | PROHIBITED — deprecated entries remain permanently |
| ID recycling | PROHIBITED — deprecated/retired IDs are never reassigned |
| Initial state | FIXED — all entries begin at `narrative.lifecycle.emerging` |
| Ontology SSOT | Narrative Framework v2 — this governance document defers to it |

---

*Last updated: 2026-06-03*
*Governance authority: ARCH (primary), GOV (review)*
*Ontology SSOT: `docs/README_narrative_framework.md` (Narrative Framework v2)*
