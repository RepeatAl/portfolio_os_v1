# Design Document: Narrative Registry Framework

## Overview

This design specifies HOW the Narrative Registry Framework will satisfy requirements NRF-REQ-1 through NRF-REQ-10. It defines the structural layout, governance procedures, entry schema, and artifact integration for a future Narrative Registry file.

**Scope preservation**:
- This design defines structure and governance ONLY
- No actual registry population is authorized
- Narrative Framework v2 (`docs/README_narrative_framework.md`) remains the ontology SSOT
- The Narrative Registry will store WHICH narratives exist — it does not redefine WHAT a narrative IS
- No code, engines, or runtime behavior is produced by this spec

### Design Constraints

- **Definition-only**: No engines, code, scores, probabilities, validation scripts, or runtime behavior
- **Schema-only delivery**: The registry file created by this spec's tasks will contain structure and governance metadata — zero narrative entries
- **Single file model**: Registry is a single YAML file (rationale in Design Decisions)
- **Layer 0 compliance**: Follows artifact registry patterns established by Market Organism deliverables

### Schema-Only Registry Creation Boundary

The tasks phase may create only a schema-only registry file with an empty `narratives: []` container. It MUST NOT include placeholder narratives, sample narratives, illustrative entries, real narrative IDs, or any populated registry entries. The `narratives: []` list must remain empty until a separate future population spec is authorized and executed.

### Design Decisions Summary

| # | Decision | Resolution | Rationale |
|---|----------|-----------|-----------|
| D-1 | Single YAML vs directory | Single YAML file | Simpler governance, easier VG-2 (no-population) verification, consistent with artifact_registry.yaml pattern |
| D-2 | Schema-only vs empty entries container | Schema + empty `narratives: []` container | Enables VG-2 check (list must be empty in this spec); makes future population additive |
| D-3 | Glossary terms | Local to spec only | Central glossary mutation not authorized |
| D-4 | Artifact type | SSOT (existing type) | No need to create new REGISTRY type; SSOT lifecycle (draft→review→canonical→deprecated) fits |
| D-5 | System reference validation | Accept on trust; validate in future spec | `system.*` registry may not exist yet (NRG-12) |
| D-6 | Entry versioning | `last_modified` field + lifecycle audit log | Simple version tracking without complex versioning infrastructure |
| D-7 | Velocity storage format | Enum: `accelerating` / `steady` / `decelerating` (lowercase) | Consistent with canonical ID conventions; qualitative only |
| D-8 | Lifecycle audit format | Inline `lifecycle_history` list per entry | Keeps audit co-located with entry; avoids separate file governance overhead |
| D-9 | Registry file path | `docs/registries/narrative_registry.yaml` | Groups future registries together; `docs/` prefix is consistent with SSOT documentation |
| D-10 | Hierarchy declaration | `parent_narrative` field referencing existing `narrative.*` ID | Flat namespace preserved; hierarchy expressed through field, not nested structure |

---

## Architecture

### Artifact Position

The Narrative Registry will be located at:

```
docs/registries/narrative_registry.yaml
```

**Rationale**: The `docs/registries/` directory groups all future registry files (Narrative Registry, future Asset-to-Narrative Registry, future System Registry) under a single governance location. The `docs/` prefix is consistent with existing SSOT documentation patterns. The file is a YAML data artifact, not code.

### Authority Hierarchy

```
Market Organism Principles (Layer 0)
  └── Narrative Framework v2 (SSOT — ontology)
        └── Narrative Registry (SSOT — population)
              └── Future: Asset-to-Narrative Registry (SSOT — membership)
```

The Narrative Registry depends on and defers to Narrative Framework v2 for all ontological definitions. It does not redefine, extend, or contradict Framework v2.

---

## Components and Interfaces

### Component 1: Registry File (narrative_registry.yaml)

**Satisfies**: NRF-REQ-1, NRF-REQ-2, NRF-REQ-5, NRF-REQ-8

The primary deliverable — a single YAML file at `docs/registries/narrative_registry.yaml` containing:
- YAML metadata header (artifact registration fields)
- Governance rules section (creation authority, amendment rules, prohibited fields)
- Empty narratives container (`narratives: []`)

**Interface**: Consumed by future specs (Narrative Population, Asset-to-Narrative Registry). Registered in `.domainization/artifact_registry.yaml`. Read by ARCH and GOV domains for governance decisions.

### Component 2: Governance Procedures Documentation

**Satisfies**: NRF-REQ-3, NRF-REQ-4, NRF-REQ-6

Governance procedures embedded in the registry file's governance section and documented in a supplementary README. Defines:
- Creation procedure (6 steps)
- Collision check procedure (4 steps)
- Amendment rules (per-field authority table)
- Lifecycle transition procedure (6 steps)
- Deprecation and retirement procedures

**Interface**: Referenced by ARCH domain when proposing new narratives. Referenced by GOV domain during review.

### Component 3: Cross-Reference Contract

**Satisfies**: NRF-REQ-7

Defines canonical ID formats and document reference conventions used within the registry file:
- `narrative.*` for narrative IDs
- `sc.*` for State_Change references
- `system.*` for System references
- `(See: [Deliverable_Name], Section: [Section_Title])` for document cross-references

**Interface**: Consumed by all registry entries. Validated during VG-4 and VG-9 verification gates.

### Component 4: Artifact Registry Integration

**Satisfies**: NRF-REQ-8

Registration of the narrative_registry.yaml file in `.domainization/artifact_registry.yaml` with full metadata:
- artifact_type: SSOT
- primary_domain: ARCH
- topic: narrative_registry
- lifecycle_status: draft (initial)

**Interface**: Integrates with existing domainization observability system (RegistrationValidator hook).

---

## Data Models

### Narrative Registry Entry Model

This is the conceptual data model for a single registry entry. It is NOT a database schema or implementation specification.

```yaml
# DATA MODEL — conceptual structure for one registry entry
narrative_entry:
  # Required fields (must be present in every entry)
  narrative_id: narrative.[descriptive_token]       # String, immutable, unique
  scope_definition: "..."                           # String, non-empty
  birth_trigger: sc.[category].[subcategory].[event]  # String, references State_Change
  connected_systems: [system.[name]]                # List[String], min 1
  falsification_condition: "..."                    # String, concrete/testable
  lifecycle_state: narrative.lifecycle.[state]       # String, one of 6 valid states
  registered_date: "YYYY-MM-DD"                     # String (ISO 8601), immutable
  registered_by: ARCH                               # String, authority role
  last_modified: "YYYY-MM-DD"                       # String (ISO 8601)

  # Optional qualitative fields
  display_name: {en: "...", de: "..."}              # Object, rendering only
  parent_narrative: narrative.[token]                # String or null
  velocity: accelerating | steady | decelerating    # String enum, qualitative only
  expected_duration: Year                           # String, Temporal_Taxonomy value
  evidence_summary: "..."                           # String
  related_narratives: [narrative.[token]]            # List[String]
  lifecycle_history: [...]                          # List[Object], append-only audit
```

### Lifecycle Audit Record Model

```yaml
# DATA MODEL — single lifecycle transition record
lifecycle_record:
  from: narrative.lifecycle.[state]     # Previous lifecycle state
  to: narrative.lifecycle.[state]       # New lifecycle state
  date: "YYYY-MM-DD"                   # Transition date
  trigger: sc.[category].[event]       # Causing State_Change (canonical ID)
  authorized_by: ARCH                  # Authority role
  evidence: "..."                      # Why State_Change qualifies as trigger
```

### Governance Rules Model

```yaml
# DATA MODEL — governance section structure
governance_model:
  creation_authority: [ARCH, GOV]
  lifecycle_transition_authority: [ARCH]
  review_authority: [GOV]
  initial_lifecycle_state: narrative.lifecycle.emerging
  collision_check_required: true
  immutable_fields: [narrative_id, birth_trigger, registered_date]
  amendment_rules: {...}               # Per-field authority mapping
  prohibited_fields: [...]             # List of forbidden field names
```

**Note**: All models above are illustrative only — not actual registry entries or population.

---

## Correctness Properties

### Property 1: Schema Completeness

All 8 required fields (`narrative_id`, `scope_definition`, `birth_trigger`, `connected_systems`, `falsification_condition`, `lifecycle_state`, `registered_date`, `registered_by`) are present in the registry entry schema definition. Verified by document inspection of the entry schema section.

**Validates: Requirements 2.1, 2.4**

### Property 2: No Prohibited Fields

Zero prohibited fields (`score`, `weight`, `numeric_strength`, `probability`, `confidence`, `rank`, `priority_order`, `asset_list`, `ticker_symbols`, `correlation_matrix`, `recommendation`, `numeric_threshold`, `membership_weight`) appear as allowed fields, optional fields, required fields, governance inputs, lifecycle fields, or future-ready fields in the registry file schema. These terms MAY appear only inside explicit Prohibited Fields / Exclusion Constraints sections where they are listed as forbidden. Verified by text search with context awareness.

**Validates: Requirements 5.2, 9.1**

### Property 3: No Population

The `narratives` list contains zero entries. The registry file is schema-only. Verified by inspecting the narratives section.

**Validates: Requirements 1.6, 5.5**

### Property 4: Namespace Compliance

All narrative IDs in examples follow the `narrative.[token]` format with lowercase, underscore-separated tokens. No display text is used as identity. Verified by document inspection.

**Validates: Requirements 3.1, 3.7**

### Applicability Assessment: Property-Based Testing

PBT does NOT apply to this feature. The deliverable is a YAML schema definition with governance rules — not executable code with inputs/outputs. There are no algorithms, parsers, or business logic functions to test with generated inputs. Verification is structural: required sections present, required declarations made, prohibited content absent.
| P-6 | Initial lifecycle state is always `narrative.lifecycle.emerging` | Inspect governance rules |
| P-7 | No numeric values appear in prohibited-field positions | Text search for numeric patterns |
| P-8 | All cross-references use canonical format | Pattern match on reference format |
| P-9 | Artifact registration metadata is complete | Compare with required fields |

These properties are verified through the Verification Gate Plan (VG-1 through VG-9) rather than through automated property-based tests.

---

## Registry File Structure

The registry file follows a three-section structure:

```yaml
# ============================================================
# SECTION 1: FILE METADATA
# ============================================================
---
artifact_id: narrative_registry_yaml
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: draft
created_date: "2026-06-03"
last_modified: "2026-06-03"
owner_role: Portfolio Architect
ssot_relationship: canonical
topic: narrative_registry
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [narrative_framework_md, market_organism.principles_md, state_change_taxonomy_md]
version: v1
alignment_spec: narrative-registry-framework
---

# ============================================================
# SECTION 2: GOVERNANCE RULES (embedded in file header)
# ============================================================
governance:
  creation_authority: [ARCH, GOV]
  lifecycle_transition_authority: [ARCH]
  review_authority: [GOV]
  initial_lifecycle_state: narrative.lifecycle.emerging
  collision_check_required: true
  immutable_fields: [narrative_id]
  amendment_rules:
    scope_definition: refinable
    connected_systems: additive_only
    falsification_condition: refinable
    display_name: freely_changeable
    narrative_id: immutable
  prohibited_fields:
    - score
    - weight
    - numeric_strength
    - probability
    - confidence
    - rank
    - priority_order
    - asset_list
    - ticker_symbols
    - correlation_matrix
    - recommendation
    - numeric_threshold
    - membership_weight

# ============================================================
# SECTION 3: REGISTRY ENTRIES (empty — population is a future spec)
# ============================================================
narratives: []
```

**Note**: The above is a SCHEMA EXAMPLE illustrating the target file structure. It is NOT the actual registry file. The actual file will be created during the tasks phase. The `narratives: []` empty list is intentional — population happens in a separate future spec. These examples are schema examples only. They are not registry population and MUST NOT be copied as actual entries into `narratives: []`.

---

## Registry Entry Schema

### Required Fields

Every entry in the `narratives` list must contain:

```yaml
# SCHEMA EXAMPLE ONLY — not a real narrative entry
# These examples are schema examples only. They are not registry population
# and MUST NOT be copied as actual entries into narratives: []
- narrative_id: narrative.[descriptive_token]
  scope_definition: "Text describing the shared market belief structure"
  birth_trigger: sc.[category].[subcategory].[event]
  connected_systems:
    - system.[name]
  falsification_condition: "Concrete, testable condition that would invalidate this narrative"
  lifecycle_state: narrative.lifecycle.[state]
  registered_date: "YYYY-MM-DD"
  registered_by: ARCH
  last_modified: "YYYY-MM-DD"
```

| Field | Type | Constraints |
|-------|------|------------|
| `narrative_id` | String | Format: `narrative.[token]`; lowercase, underscore-separated, language-neutral; IMMUTABLE once assigned; must pass Collision_Check |
| `scope_definition` | String | Non-empty; describes what shared belief this narrative represents |
| `birth_trigger` | String | Format: `sc.*`; must reference identifiable market event |
| `connected_systems` | List[String] | Format: `system.*`; minimum 1 entry; additive-only (removals require deprecation) |
| `falsification_condition` | String | Concrete, testable; not vague ("loses relevance" is invalid) |
| `lifecycle_state` | String | Format: `narrative.lifecycle.*`; one of: emerging, strengthening, dominant, weakening, dormant, dead |
| `registered_date` | String (ISO 8601) | Date of initial registration |
| `registered_by` | String | Authority role: ARCH or GOV |
| `last_modified` | String (ISO 8601) | Date of most recent modification |

### Optional Qualitative Fields

```yaml
# SCHEMA EXAMPLE — optional fields shown
# These examples are schema examples only. They are not registry population
# and MUST NOT be copied as actual entries into narratives: []
  display_name:
    en: "Human-readable English name"
    de: "German rendering"
  parent_narrative: narrative.[parent_token]
  velocity: accelerating
  expected_duration: Year
  evidence_summary: "Human-readable justification for inclusion"
  related_narratives:
    - narrative.[related_token]
  lifecycle_history:
    - from: narrative.lifecycle.emerging
      to: narrative.lifecycle.strengthening
      date: "YYYY-MM-DD"
      trigger: sc.[category].[event]
      authorized_by: ARCH
      evidence: "Description of confirming State_Change"
```

| Field | Type | Constraints |
|-------|------|------------|
| `display_name` | Object | Language keys (en, de, etc.); rendering only — NEVER identity |
| `parent_narrative` | String or null | Must reference existing `narrative.*` ID in registry |
| `velocity` | String (enum) | Values: `accelerating` / `steady` / `decelerating`; qualitative only; MUST NOT be used as lifecycle trigger, ranking input, score proxy, or Temporal_Taxonomy extension |
| `expected_duration` | String | Valid Temporal_Taxonomy duration value |
| `evidence_summary` | String | Human-readable justification |
| `related_narratives` | List[String] | Format: `narrative.*`; must reference existing entries |
| `lifecycle_history` | List[Object] | Audit trail of lifecycle transitions (see Lifecycle Audit Model) |

### Prohibited Fields

The following fields MUST NOT appear in any registry entry or schema extension:

| Field | Why Prohibited | Source |
|-------|---------------|--------|
| `score` / `weight` / `numeric_strength` | EC-2: No numeric scoring | NRF-REQ-9 |
| `probability` / `confidence` | EC-2: No probabilities | NRF-REQ-9 |
| `rank` / `priority_order` | EC-6: No ranking | NRF-REQ-9 |
| `asset_list` / `ticker_symbols` | EC-4: No asset-first design | NRF-REQ-10 |
| `correlation_matrix` | EC-5: No correlation | NRF-REQ-5 |
| `recommendation` | EC-6: No recommendation logic | NRF-REQ-5 |
| `numeric_threshold` | EC-7: No numeric lifecycle thresholds | NRF-REQ-6 |
| `membership_weight` | EC-8: No numeric membership weights | NRF-REQ-9 |

### Velocity Guardrails

The `velocity` field is subject to explicit guardrails:

- **Valid values**: `accelerating`, `steady`, `decelerating` (lowercase enum)
- **Nature**: Qualitative observation by human analyst — NOT computed, NOT algorithmic
- **Prohibited uses**: lifecycle transition trigger, ranking input, score proxy, Temporal_Taxonomy extension, sorting criterion, numeric conversion
- **Update authority**: ARCH domain only, with evidence summary

(See: README_narrative_framework, Section: 6. Narrative Lifecycle State Machine — Velocity subsection)
(See: README_temporal_taxonomy, Section: Temporal Property Enumeration)

---

## Governance Procedures

### Creation Procedure

1. **Proposer** (ARCH domain) drafts a candidate entry with all required fields
2. **Collision_Check**: Verify no exact or semantic collision with existing `narrative.*` IDs
   - Exact match: reject immediately
   - Semantic overlap: proposer must differentiate scope or merge with existing entry
3. **Inclusion Criteria Gate**: Verify all 4 criteria are met (distinct belief, falsifiable, connects sc→system, has ID)
4. **Review** (GOV domain): Governance compliance check (naming rules, no future-leak, evidence quality)
5. **Registration**: Entry added to `narratives` list with `lifecycle_state: narrative.lifecycle.emerging`
6. **Artifact registry update**: Not required per entry (registry file is already registered as a whole)

### Collision Check Procedure

1. Extract proposed `narrative_id` token
2. **Exact match**: Search all existing `narrative.*` IDs for identical token → REJECT if found
3. **Semantic overlap**: Review `scope_definition` of all existing entries for overlapping belief structures
   - If overlap detected: proposer must either (a) narrow scope to differentiate, or (b) withdraw in favor of existing entry
   - If overlap is partial: consider parent/sub-narrative hierarchy via `parent_narrative` field
4. **Result**: PASS (no collision) or REJECT (collision found, with explanation)

### Amendment Procedure

| Field | Amendment Rule | Authority |
|-------|---------------|-----------|
| `scope_definition` | May be refined (narrowed/clarified), not expanded | ARCH |
| `connected_systems` | Additive only — new systems may be added, never removed without deprecation | ARCH |
| `falsification_condition` | May be refined (made more specific) | ARCH |
| `display_name` | Freely changeable (rendering, not identity) | ARCH or GOV |
| `velocity` | May be updated with evidence | ARCH |
| `evidence_summary` | May be updated/expanded | ARCH |
| `related_narratives` | May be added/removed | ARCH |
| `narrative_id` | IMMUTABLE — cannot be changed | — |
| `birth_trigger` | IMMUTABLE — historical fact | — |
| `registered_date` | IMMUTABLE — historical fact | — |

Every amendment updates `last_modified` to current date.

### Lifecycle Transition Procedure

1. **Trigger identification**: A State_Change occurs that qualifies as a lifecycle transition trigger per Narrative Framework v2 Section 6
2. **Evidence documentation**: ARCH documents the State_Change reference and how it satisfies transition criteria
3. **Transition execution**: ARCH updates `lifecycle_state` to the new value
4. **Audit record**: A new entry is appended to `lifecycle_history` with: from, to, date, trigger (sc.* ID), authorized_by, evidence
5. **Last modified update**: `last_modified` is updated
6. **Prohibition**: No automated/programmatic transitions. No signal-triggered transitions. Only State_Changes cause transitions; signals may detect them.

### Deprecation Procedure

1. **Trigger**: Falsification condition is met, OR narrative is superseded by a more accurate explanation
2. **Evidence**: Document the State_Change that proves falsification/supersession
3. **Transition**: Set `lifecycle_state: narrative.lifecycle.dead`
4. **Additional fields**: Add `deprecated_date`, `deprecation_reason`, `replacement_narrative_id` (if applicable)
5. **Retention**: Deprecated entries remain in the registry permanently — no deletion
6. **ID preservation**: Deprecated `narrative.*` ID is never reassigned or recycled

### Retirement Procedure

1. **Prerequisite**: Entry must be in `narrative.lifecycle.dead` state for a governance-defined cooling period (recommended: 90 days minimum)
2. **Action**: Move entry from `narratives` to a `retired_narratives` section in the same file
3. **Effect**: Entry excluded from active queries but remains in the file for historical reference
4. **ID preservation**: Retired IDs are NEVER reassigned — they remain permanently reserved

### Conflict/Duplicate Handling

1. **Detection**: During Collision_Check or during ongoing registry review
2. **Resolution hierarchy**:
   - If scopes are identical: reject the newer entry; point to existing entry
   - If one is more specific: keep the more specific; consider making the broader one a parent
   - If genuinely different but confusingly similar: require proposer to differentiate via scope refinement
3. **Authority**: ARCH proposes resolution; GOV concurs
4. **Documentation**: Record conflict resolution in `evidence_summary` of the surviving entry

---

## Lifecycle Audit Model

**Decision D-8**: Lifecycle history is stored INLINE within each registry entry as a `lifecycle_history` list.

**Rationale**: Co-locating audit history with the entry keeps governance self-contained in a single file. A separate audit log would require additional file governance overhead without providing meaningful benefit at definition-layer scale. If the registry grows to hundreds of entries, a future spec may extract the audit trail to a separate artifact.

### Audit Record Structure

```yaml
lifecycle_history:
  - from: narrative.lifecycle.emerging
    to: narrative.lifecycle.strengthening
    date: "2026-07-15"
    trigger: sc.corporate.capex.hyperscaler_increase
    authorized_by: ARCH
    evidence: "Multiple hyperscaler companies confirmed increased AI capex guidance in Q2 2026 earnings"
```

**Note**: The above is a SCHEMA EXAMPLE illustrating audit record structure. It is NOT a real lifecycle transition.

### Audit Requirements

- Every lifecycle transition MUST create an audit record
- Audit records are APPEND-ONLY — previous records cannot be modified or deleted
- The `trigger` field must reference a canonical `sc.*` ID
- The `authorized_by` field must be a valid domain role (ARCH or GOV)
- The `evidence` field must describe why the State_Change qualifies as a transition trigger

---

## Cross-Reference Contract

### ID Reference Formats

| Reference Type | Format | Source |
|---------------|--------|--------|
| Narrative ID | `narrative.[token]` | Narrative Framework v2, Section 4 |
| Lifecycle state | `narrative.lifecycle.[state]` | Narrative Framework v2, Section 6 |
| State_Change | `sc.[category].[subcategory].[event]` | README_state_change_taxonomy |
| System | `system.[name]` | README_expansion_taxonomy |
| Dependency_Type | `dep.[type]` | README_dependency_types_v2 |
| Temporal duration | Valid Temporal_Taxonomy value | README_temporal_taxonomy |

### Document Cross-References

All references to external documents use the format:
`(See: [Deliverable_Name], Section: [Section_Title])`

Required cross-references for the registry file:

| Target Deliverable | Section Referenced | Context |
|-------------------|-------------------|---------|
| README_narrative_framework | Section 4: What Is a Narrative? | ID namespace rules |
| README_narrative_framework | Section 6: Lifecycle State Machine | Valid lifecycle states and transitions |
| README_narrative_framework | Section 13: Extension Criteria | Inclusion/exclusion criteria |
| README_narrative_framework | Section 15: Exclusion Constraints | Prohibited fields rationale |
| README_market_organism_principles | Principle 2: Root Node Invariant | State_Change as causal root |
| README_state_change_taxonomy | Classification Hierarchy | Birth trigger format |
| README_dependency_types_v2 | Narrative | dep.narrative distinction |
| README_temporal_taxonomy | Temporal Property Enumeration | Expected duration values |
| README_shared_glossary_reference | Glossary Usage Rules | Glossary-first policy |

---

## Artifact Registry Integration

### Registration Metadata

When the registry file is created (during tasks phase), it will be registered in `.domainization/artifact_registry.yaml` with:

```yaml
# This is the PLANNED registration — not yet executed
- artifact_id: narrative_registry_yaml
  file_path: docs/registries/narrative_registry.yaml
  primary_domain: ARCH
  artifact_type: SSOT
  lifecycle_status: draft
  created_date: "2026-06-03"
  last_modified: "2026-06-03"
  owner_role: Portfolio Architect
  ssot_relationship: canonical
  topic: narrative_registry
  allowed_writers:
    - ARCH
    - GOV
  allowed_readers:
    - ALL
  dependencies:
    - narrative_framework_md
    - market_organism.principles_md
    - state_change_taxonomy_md
  description: "Canonical registry of recognized narratives with governance rules. Schema-only until population spec."
  tags:
    - narrative
    - registry
    - governance
```

**Note**: This registration will be performed during the tasks phase. The artifact_registry.yaml is NOT modified during design.

### Lifecycle Progression

The registry file follows the SSOT lifecycle state machine:
1. `draft` — created with schema and governance only (this spec)
2. `review` — after human review of schema and governance rules
3. `canonical` — after approval; narrative population authorized by future spec
4. `deprecated` — if superseded (unlikely in near term)

---

## Design Decisions

### D-1: Single YAML vs Directory

**Decision**: Single YAML file at `docs/registries/narrative_registry.yaml`

**Rationale**:
- Simpler governance — one file to track, version, and audit
- Easier VG-2 verification — count entries in one location
- Consistent with `artifact_registry.yaml` pattern (single file, multiple entries)
- At expected scale (10-50 narratives initially), single file is manageable
- If scale exceeds hundreds of entries, a future spec may decompose

### D-2: Schema-Only vs Empty Entries Container

**Decision**: Include `narratives: []` empty list

**Rationale**:
- Makes future population purely additive (append to list)
- Enables VG-2 gate: verify `narratives` list length is 0 in this spec
- Avoids ambiguity about where entries go when population begins
- Empty list is NOT narrative population — it is schema preparation

### D-3: Local Glossary Only

**Decision**: Glossary candidates remain local to this spec

**Rationale**: Central glossary mutation requires separate governance authorization not granted by this spec. Terms (Narrative_Registry, Registry_Entry, Collision_Check, Lifecycle_Transition_Authority) are defined in requirements.md glossary section.

### D-4: SSOT Artifact Type

**Decision**: Use existing `SSOT` artifact type (not a new `REGISTRY` type)

**Rationale**:
- SSOT lifecycle (draft → review → canonical → deprecated) fits registry governance needs
- Avoids lifecycle_state_machine.yaml modification (not authorized by this spec)
- The registry IS a canonical source of truth (for which narratives exist)
- If future needs diverge, a new type can be proposed in a separate governance spec

### D-5: System Reference Validation

**Decision**: Accept `system.*` IDs on trust; validate in future spec

**Rationale**:
- No canonical `system.*` registry exists yet (NRG-12)
- Blocking narrative registration on system validation would prevent any progress
- System IDs used in `connected_systems` are treated as forward references
- A future System Registry spec will enable retroactive validation

### D-6: Entry Versioning

**Decision**: `last_modified` field + inline `lifecycle_history`

**Rationale**:
- Simple version tracking without complex infrastructure
- `last_modified` tracks recency
- `lifecycle_history` provides full state transition audit trail
- No need for semantic versioning (entries are not APIs)
- If more sophisticated versioning is needed, a future spec can add it

### D-7: Velocity Storage Format

**Decision**: Lowercase enum: `accelerating` / `steady` / `decelerating`

**Rationale**:
- Consistent with canonical ID convention (lowercase throughout)
- Three values only — no gradations, no numeric proxy
- Matches Narrative Framework v2 definition: qualitative observation of lifecycle momentum
- Explicit guardrails prevent misuse as ranking/scoring/trigger

### D-8: Lifecycle Audit Format

**Decision**: Inline `lifecycle_history` list per entry

**Rationale**:
- Co-locates audit with entry — no cross-file reference needed
- Each transition is an append-only record
- Avoids separate audit file governance overhead
- At expected transition frequency (few per narrative per year), inline storage is manageable
- Enables single-file governance and backup

### D-9: Registry File Path

**Decision**: `docs/registries/narrative_registry.yaml`

**Rationale**:
- `docs/` prefix: consistent with SSOT documentation artifacts
- `registries/` subdirectory: groups future registries (narrative, system, asset-to-narrative)
- YAML format: consistent with artifact_registry.yaml and domain_registry.yaml
- Descriptive filename per file naming conventions

### D-10: Hierarchy Declaration

**Decision**: `parent_narrative` field (optional) referencing existing `narrative.*` ID

**Rationale**:
- Preserves flat namespace (no nested IDs like `narrative.ai_transformation.ai_infrastructure`)
- Hierarchy is expressed through field value, not ID structure
- Consistent with Narrative Framework v2 Section 7: "hierarchy is expressed through naming convention, not through nested IDs (flat namespace)"
- Simple and queryable — find all sub-narratives of X by filtering on `parent_narrative: narrative.X`

---

## Verification Strategy

### Verification Gate Mapping

| Gate | Design-Level Check | Method |
|------|-------------------|--------|
| VG-1: Structural Completeness | YAML valid; metadata present; governance section present; schema fields defined | Document inspection: verify sections exist |
| VG-2: No Population | `narratives: []` — list must be empty | Text search: verify no entries in narratives list |
| VG-3: No Future-Leak | Prohibited fields (`score`, `weight`, `probability`, `confidence`, `rank`, `asset_list`, `ticker_symbols`, `numeric_threshold`, `membership_weight`) do NOT appear as allowed registry entry fields, governance inputs, or schema extensions. These terms MAY appear only inside explicit Prohibited Fields / Exclusion Constraints sections where they are listed as forbidden. | Text search: scan for prohibited field names outside of prohibition sections |
| VG-4: Namespace Correctness | All example IDs follow `narrative.*`; collision-check procedure defined | Document inspection: verify format compliance |
| VG-5: Lifecycle Governance | Transition authority documented; evidence requirements specified; initial state = emerging | Document inspection: verify governance section |
| VG-6: Artifact Registry Compatibility | Registration metadata matches schema; topic field set; dependencies listed | Document inspection: compare with artifact_registry.yaml patterns |
| VG-7: Rendering Independence | `display_name` marked as rendering-only; no display text in IDs | Document inspection: verify guardrails |
| VG-8: Market Organism Compatibility | 12-domain model preserved; no new domains; primitive chain intact | Document inspection: verify no violations |
| VG-9: NF v2 Compatibility | Required fields match Section 13; lifecycle states match Section 6; No Dead Ends enforced | Cross-reference validation |

### Verification Approach

All verification is structural and document-inspection based. No runtime validation scripts are produced by this spec. Verification gates are executed as checklist-style reviews by the human or by a future CI task (not authorized by this spec).

---

## Requirement Traceability

| Requirement | Design Component | How Satisfied |
|-------------|-----------------|---------------|
| NRF-REQ-1 | Architecture section, Registry File Structure | Boundary defined; distinctions documented; SSOT declared |
| NRF-REQ-2 | Registry Entry Schema (all 3 subsections) | Required, optional, prohibited fields formally defined with types and constraints |
| NRF-REQ-3 | Governance Procedures (Creation, Collision Check, Deprecation, Retirement) | Full ID lifecycle defined |
| NRF-REQ-4 | Governance Procedures (Creation, Step 3: Inclusion Criteria Gate) | 4 criteria enforced at registration |
| NRF-REQ-5 | Registry Entry Schema (Prohibited Fields), Governance section | Exclusion constraints embedded in schema and governance rules |
| NRF-REQ-6 | Governance Procedures (Lifecycle Transition), Lifecycle Audit Model | Authority, evidence, audit trail all defined |
| NRF-REQ-7 | Cross-Reference Contract | ID formats, document references, minimum cross-references specified |
| NRF-REQ-8 | Artifact Registry Integration | Full registration metadata defined; lifecycle, topic, dependencies specified |
| NRF-REQ-9 | Registry Entry Schema (Prohibited Fields), Velocity Guardrails, Design Decision D-7 | No-future-leak guarantee structurally enforced |
| NRF-REQ-10 | Design Decisions D-2, D-6; Registry Entry Schema | narrative_id as stable FK; lifecycle queryable; connected_systems as list; no asset fields |

---

## Testing Strategy

### Applicability Assessment: Property-Based Testing

PBT does NOT apply to this feature. Rationale:

- The deliverable is a YAML schema definition with governance rules — not a function with inputs/outputs
- There is no parser, serializer, algorithm, or business logic to test
- There are no universal properties that hold across a range of generated inputs
- Verification is structural: required sections present, required declarations made, prohibited content absent

### Verification Approach

All acceptance criteria are verifiable by document inspection. The verification gates (VG-1 through VG-9) constitute the testing strategy — each is a structural check that can be performed by reading the registry file and confirming presence/absence of required/prohibited content.

---

## Error Handling

Not applicable. This is a definition-layer design with no runtime behavior. Structural errors in the registry file are handled through the Verification Gate Plan. Governance errors (e.g., attempted registration without meeting inclusion criteria) are handled through the Creation Procedure which requires human review at each step.

---

## Task Generation Guard

The future `tasks.md` MUST include a verification step that opens the actual `docs/registries/narrative_registry.yaml` and confirms `narratives: []` is empty. The same gate must fail if any placeholder narrative, illustrative narrative, or real narrative appears in the list. This is a hard requirement for the tasks phase — not optional.

---

## Satisfies

| Requirement | How Satisfied in Design |
|-------------|------------------------|
| NRF-REQ-1 | Architecture + File Structure: boundary, distinctions, SSOT declaration |
| NRF-REQ-2 | Entry Schema: required/optional/prohibited fields with types and constraints |
| NRF-REQ-3 | Governance Procedures: creation, collision check, deprecation, retirement, conflict handling |
| NRF-REQ-4 | Governance Procedures: inclusion criteria gate (step 3 of creation) |
| NRF-REQ-5 | Entry Schema + Governance: prohibited fields, exclusion constraints |
| NRF-REQ-6 | Governance Procedures + Lifecycle Audit Model: authority, evidence, audit trail |
| NRF-REQ-7 | Cross-Reference Contract: ID formats, document references |
| NRF-REQ-8 | Artifact Registry Integration: full metadata, lifecycle, dependencies |
| NRF-REQ-9 | Entry Schema + Velocity Guardrails: no-future-leak structural enforcement |
| NRF-REQ-10 | Design Decisions D-2, D-6 + Entry Schema: FK readiness, queryable lifecycle, list systems |
