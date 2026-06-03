# Requirements Document: Narrative Registry Framework

## Purpose

This spec defines the governance rules and schema for a future Narrative Registry — the canonical data artifact that answers: **"Which narratives officially exist in Portfolio OS?"**

The Narrative Registry is NOT the Narrative Framework. The Narrative Framework v2 (`docs/README_narrative_framework.md`) defines WHAT a narrative IS (ontology). The Narrative Registry defines WHICH narratives exist (population governance).

This is a **definition/governance-layer only** spec. It produces:
- A registry schema (field definitions, constraints)
- A governance model (creation authority, lifecycle transitions, amendment rules)
- Verification gates (structural compliance checks)

It does NOT produce:
- Actual narrative instances
- Runtime behavior
- Executable code

## Scope

### In Scope

- Registry boundary definition (what the Narrative Registry is and is not)
- Canonical registry entry model (required, optional, prohibited fields)
- Narrative ID governance (`narrative.*` namespace rules, collision prevention, immutability, deprecation, retirement)
- Inclusion/exclusion criteria formalization (enforcement of Narrative Framework v2 Section 13)
- Lifecycle governance (who transitions states, what evidence is required, audit trail)
- Amendment/deprecation/retirement rules for registry entries
- Artifact registry integration (registering the registry file itself in domainization system)
- Cross-reference contract (canonical reference format for all external references)
- Verification gates for registry compliance
- Future readiness for Asset-to-Narrative Registry (schema compatibility without implementation)

### Out of Scope

The following are explicitly excluded from this spec:

- Actual narrative instance population (which specific narratives exist)
- Asset-to-narrative mappings (which assets belong to which narratives)
- Engines or runtime code of any kind
- Validation scripts or automated tooling
- Scoring algorithms or numeric weights
- Ranking or priority ordering logic
- Probabilities or confidence values
- Dashboards or visualization specifications
- Recommendation or optimization logic
- Portfolio allocation logic
- Signal-to-narrative mapping
- Central glossary mutation (`.kiro/specs/market-organism-framework/requirements.md`)
- Market Organism Layer 0 SSOT mutation
- Narrative Framework v2 mutation (`docs/README_narrative_framework.md`)

## Definitions / Glossary Policy

### Canonical Glossary Reference

All terms used in this document are defined in the canonical glossary unless amended below:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary
(See: README_shared_glossary_reference, Section: Glossary Usage Rules)

### Local Glossary Candidates

The following terms are defined locally for this spec. They are NOT yet in the central glossary.

| Term | Definition | Status |
|------|-----------|--------|
| Narrative_Registry | A governance-controlled YAML data artifact that stores the canonical list of recognized narratives with their required metadata fields. It is the single source of truth for which narratives officially exist in Portfolio OS. It is a definition-layer artifact — not runtime code, not an engine, not a dashboard. | CANDIDATE |
| Registry_Entry | A single record in the Narrative Registry representing one canonical narrative with all required fields populated. | CANDIDATE |
| Collision_Check | A namespace validation procedure performed before narrative registration to ensure no exact or semantic collision exists with an existing `narrative.*` ID. | CANDIDATE |
| Lifecycle_Transition_Authority | The governance role authorized to change a narrative's lifecycle state, requiring documented evidence and a State_Change reference. | CANDIDATE |

### Glossary Policy

- New terms MUST be defined before use (glossary-first rule)
- Local glossary candidates are formalized within this spec only
- Central glossary update requires separate governance authorization (NOT performed by this spec)
- This policy is consistent with Narrative Framework v2 glossary handling

## Requirements

### NRF-REQ-1: Registry Boundary

**User Story:** As a portfolio architect, I want a clear definition of what the Narrative Registry is and what it is not, so that no consumer confuses it with the Narrative Framework, an engine, or the Asset-to-Narrative Registry.

#### Acceptance Criteria

1. THE Registry Framework SHALL define the Narrative Registry as a governance-controlled YAML data artifact storing canonical narrative definitions
2. THE Registry Framework SHALL explicitly distinguish the Narrative Registry (stores WHICH narratives exist) from the Narrative Framework v2 (defines WHAT a narrative IS)
3. THE Registry Framework SHALL explicitly distinguish the Narrative Registry from a future Asset-to-Narrative Registry (maps assets TO narratives)
4. THE Registry Framework SHALL declare that the Narrative Registry is NOT an engine, dashboard, scoring system, recommendation system, or runtime artifact
5. THE Registry Framework SHALL declare that the Narrative Framework v2 remains the ontology SSOT — the Registry does not redefine narrative theory
6. THE Registry Framework SHALL declare that the Registry file contains schema + governance rules + narrative entries (once populated by a future spec) — nothing else

**Gap Traceability**: NRG-01 (partial), NRG-07 (partial)

---

### NRF-REQ-2: Canonical Entry Fields

**User Story:** As a portfolio architect, I want a formally defined set of required, optional, and prohibited fields per registry entry, so that every narrative registration is complete, consistent, and free of future-leak.

#### Acceptance Criteria

1. THE Registry Framework SHALL define the following REQUIRED fields for every registry entry: `narrative_id` (canonical `narrative.*` ID), `scope_definition` (text describing the shared belief), `birth_trigger` (canonical `sc.*` State_Change ID), `connected_systems` (list of `system.*` IDs, minimum 1), `falsification_condition` (text stating what would invalidate), `lifecycle_state` (canonical `narrative.lifecycle.*` ID), `registered_date` (ISO 8601), `registered_by` (authority role)
2. THE Registry Framework SHALL define the following OPTIONAL qualitative fields: `display_name` (object with language keys — rendering only), `parent_narrative` (`narrative.*` ID or null), `velocity` (Accelerating/Steady/Decelerating — qualitative observation only), `expected_duration` (Temporal_Taxonomy duration value), `evidence_summary` (text), `related_narratives` (list of `narrative.*` IDs)
3. THE Registry Framework SHALL explicitly PROHIBIT the following fields: `score`/`weight`/`numeric_strength`, `probability`/`confidence`, `rank`/`priority_order`, `asset_list`/`ticker_symbols`, `correlation_matrix`, `recommendation`, `numeric_threshold`, `membership_weight`
4. THE Registry Framework SHALL declare that no registry entry may exist without ALL required fields populated
5. THE Registry Framework SHALL declare that `velocity` MUST NOT be used as a lifecycle transition trigger, ranking input, score proxy, or Temporal_Taxonomy extension
6. THE Registry Framework SHALL declare that `display_name` is rendering only — never identity; changing display text does NOT change the canonical ID

**Gap Traceability**: NRG-09 (velocity format)

---

### NRF-REQ-3: ID Governance

**User Story:** As a portfolio architect, I want formal rules for narrative ID assignment, collision prevention, immutability, deprecation, and retirement, so that the `narrative.*` namespace remains clean, stable, and unambiguous.

#### Acceptance Criteria

1. THE Registry Framework SHALL define the ID format as `narrative.[descriptive_token]` where the token is lowercase, underscore-separated, language-neutral, and stable once assigned
2. THE Registry Framework SHALL require a Collision_Check before any new narrative registration: (a) exact match check against all existing `narrative.*` IDs, (b) semantic overlap review to detect different tokens describing the same belief
3. THE Registry Framework SHALL declare canonical IDs as IMMUTABLE — once assigned, a `narrative.*` ID cannot be renamed, reassigned, or recycled
4. THE Registry Framework SHALL define deprecation rules: (a) deprecated IDs remain in the registry permanently, (b) deprecated entries carry `deprecated_date`, `deprecation_reason`, `replacement_narrative_id` (if applicable), (c) deprecation requires a State_Change reference proving falsification or supersession
5. THE Registry Framework SHALL define retirement rules: (a) retirement = removal from active query results (entry remains in archive section), (b) retirement is only permitted after deprecation + governance-defined cooling period, (c) retired IDs are NEVER reassigned
6. THE Registry Framework SHALL define conflict resolution: (a) if two proposed narratives overlap, the more specific one takes precedence, (b) unresolvable overlap triggers meta-narrative/sub-narrative hierarchy proposal, (c) conflicts resolved by ARCH domain with GOV concurrence
7. THE Registry Framework SHALL declare that English tokens in IDs are canonical codes, not English language text — `narrative.ai_infrastructure` is a code, not an English phrase

**Gap Traceability**: NRG-04 (collision prevention)

---

### NRF-REQ-4: Inclusion Criteria

**User Story:** As a portfolio architect, I want the 4 inclusion criteria from Narrative Framework v2 Section 13 formalized as enforceable registration gates, so that no narrative enters the registry without satisfying all criteria.

#### Acceptance Criteria

1. THE Registry Framework SHALL enforce that every new narrative satisfies ALL 4 inclusion criteria before registration: (a) distinct shared belief not already covered, (b) falsifiable with explicit condition, (c) connects at least one State_Change to at least one System, (d) assigned canonical `narrative.*` ID before first use
2. THE Registry Framework SHALL declare that the 4 criteria are CONJUNCTIVE — partial satisfaction is insufficient
3. THE Registry Framework SHALL require that evidence for each criterion is documented at registration time
4. THE Registry Framework SHALL declare that the birth trigger State_Change must reference a real, identifiable market event (not a hypothetical or projected event)
5. THE Registry Framework SHALL declare that falsification conditions must be concrete and testable — "narrative loses relevance" is insufficient; specific contradicting evidence must be stated

**Gap Traceability**: NRG-01 (enforcement mechanism)

---

### NRF-REQ-5: Exclusion Constraints

**User Story:** As a portfolio architect, I want consolidated exclusion constraints for the registry schema and governance, so that prohibitions are reviewable in one location and the definition layer remains pure.

#### Acceptance Criteria

1. THE Registry Framework SHALL include a dedicated "Exclusion Constraints" section consolidating all prohibitions
2. THE Exclusion Constraints SHALL prohibit: (a) numeric scoring, weights, or probabilities in any registry field, (b) ranking or priority ordering logic, (c) engine implementations or executable code, (d) dashboard or visualization specifications, (e) asset lists as root-level organizational structures, (f) correlation matrices, (g) recommendation or optimization logic, (h) numeric lifecycle transition thresholds, (i) numeric membership weights
3. THE Exclusion Constraints SHALL be consistent with Narrative Framework v2 Exclusion Constraints (EC-1 through EC-8)
4. THE Exclusion Constraints SHALL state: "The Narrative Registry defines WHICH narratives exist. Numeric precision belongs to future implementation phases that consume the registry — not to the registry itself."
5. THE Registry Framework SHALL declare that the registry file contains NO executable logic — it is a data artifact only

(See: README_narrative_framework, Section: 15. Exclusion Constraints)

**Gap Traceability**: NRG-03 (artifact type)

---

### NRF-REQ-6: Lifecycle Governance

**User Story:** As a portfolio architect, I want formal rules for who can transition narrative lifecycle states and what evidence is required, so that lifecycle mutations are authorized, documented, and auditable.

#### Acceptance Criteria

1. THE Registry Framework SHALL define Lifecycle_Transition_Authority: ARCH domain as primary authority, GOV domain as review/concurrence authority
2. THE Registry Framework SHALL require that every lifecycle transition references a specific State_Change that caused the transition
3. THE Registry Framework SHALL require that every lifecycle transition is recorded with: (a) previous state, (b) new state, (c) transition date, (d) triggering State_Change reference, (e) authorizing role, (f) evidence summary
4. THE Registry Framework SHALL prohibit automated/programmatic lifecycle transitions without human authorization
5. THE Registry Framework SHALL declare that signals may DETECT evidence of lifecycle transitions but CANNOT trigger them — only State_Changes cause transitions (consistent with Narrative Framework v2 Section 14)
6. THE Registry Framework SHALL define that all narratives enter the registry at `narrative.lifecycle.emerging` — no other initial state is permitted
7. THE Registry Framework SHALL declare that lifecycle state in the registry must always reflect the actual current state as determined by the most recent qualifying State_Change

**Gap Traceability**: NRG-06 (lifecycle transition authority)

---

### NRF-REQ-7: Cross-Reference Contract

**User Story:** As a portfolio architect, I want all references within the registry to use canonical ID formats and cross-reference conventions, so that every reference is machine-navigable and auditable.

#### Acceptance Criteria

1. THE Registry Framework SHALL require that all State_Change references use canonical `sc.*` IDs from the State_Change Taxonomy
2. THE Registry Framework SHALL require that all System references use canonical `system.*` IDs
3. THE Registry Framework SHALL require that all narrative references use canonical `narrative.*` IDs
4. THE Registry Framework SHALL require that all cross-references to external documents use the format: `(See: [Deliverable_Name], Section: [Section_Title])`
5. THE Registry Framework SHALL include a Cross-References section listing all deliverables referenced
6. THE Registry Framework SHALL cross-reference at minimum: README_narrative_framework, README_market_organism_principles, README_state_change_taxonomy, README_dependency_types_v2, README_temporal_taxonomy, README_shared_glossary_reference

(See: README_narrative_framework, Section: 17. Cross-References)

**Gap Traceability**: NRG-05 (hierarchy format), NRG-12 (system reference validation)

---

### NRF-REQ-8: Artifact Registry Integration

**User Story:** As a portfolio architect, I want the Narrative Registry file to be registered in the domainization artifact registry system, so that it follows the same governance lifecycle as all other canonical artifacts.

#### Acceptance Criteria

1. THE Registry Framework SHALL require that the Narrative Registry file is registered in `.domainization/artifact_registry.yaml`
2. THE Registry Framework SHALL specify the following registration metadata: `artifact_type: SSOT`, `primary_domain: ARCH`, `lifecycle_status: draft` (initial), `ssot_relationship: canonical`, `allowed_writers: [ARCH, GOV]`, `allowed_readers: [ALL]`
3. THE Registry Framework SHALL declare that the registry file follows the SSOT lifecycle state machine: draft → review → canonical → deprecated
4. THE Registry Framework SHALL declare that the `topic` field for SSOT conflict detection is `narrative_registry` — ensuring no duplicate SSOT claims the same topic
5. THE Registry Framework SHALL declare dependencies on: `narrative_framework_md`, `market_organism.principles_md`, `state_change_taxonomy_md`

**Gap Traceability**: NRG-07 (artifact registration), NRG-03 (artifact type)

---

### NRF-REQ-9: No Future-Leak

**User Story:** As a portfolio architect, I want an explicit no-future-leak guarantee for the registry schema and governance model, so that the definition layer remains pure and does not seed implementation assumptions.

#### Acceptance Criteria

1. THE Registry Framework SHALL explicitly prohibit any field that implies numeric scoring, weighting, or probability
2. THE Registry Framework SHALL explicitly prohibit any governance rule that requires runtime computation, engine execution, or automated processing
3. THE Registry Framework SHALL declare that qualitative descriptors (Accelerating/Steady/Decelerating for velocity; strong/moderate/weak for future membership) are categorical labels — NOT ordinal numeric proxies
4. THE Registry Framework SHALL explicitly prohibit converting categorical labels to numbers (e.g., strong=3, moderate=2, weak=1)
5. THE Registry Framework SHALL declare that the registry schema is designed for human authorship and human review — not for algorithmic consumption or optimization
6. THE Registry Framework SHALL state: "Weights on an incomplete model produce false confidence. The Registry defines WHICH narratives exist. Numeric precision belongs to future implementation phases."

(See: README_narrative_framework, Section: 8. Multi-Narrative Membership)

**Gap Traceability**: NRG-11 (validation tooling — deferred to backlog)

---

### NRF-REQ-10: Readiness for Future Asset-to-Narrative Registry

**User Story:** As a portfolio architect, I want the Narrative Registry schema and governance to be designed for consumption by a future Asset-to-Narrative Registry, so that the next spec can reference narratives without breaking changes.

#### Acceptance Criteria

1. THE Registry Framework SHALL design the `narrative_id` field as the stable foreign key that a future Asset-to-Narrative Registry will reference
2. THE Registry Framework SHALL ensure that narrative lifecycle state is queryable — a future consumer must be able to filter by `lifecycle_state` (e.g., exclude `narrative.lifecycle.dead` narratives from active mappings)
3. THE Registry Framework SHALL ensure that `connected_systems` is a list (not a single value) — enabling a future Asset-to-Narrative Registry to validate system-narrative connections
4. THE Registry Framework SHALL NOT include any asset-level fields (no `asset_list`, `ticker_symbols`, or membership records) — these belong exclusively to the Asset-to-Narrative Registry
5. THE Registry Framework SHALL declare that the boundary between Narrative Registry and Asset-to-Narrative Registry is: narrative definitions HERE, asset-narrative relationships THERE
6. THE Registry Framework SHALL ensure that deprecation/retirement of a narrative includes a mechanism for downstream consumers (including future Asset-to-Narrative Registry) to detect the change

**Gap Traceability**: NRG-08 (versioning strategy)

---

## Acceptance Criteria Summary

All acceptance criteria are testable by document inspection. No criterion requires:
- Runtime behavior or engine execution
- Actual narrative instance population
- Asset-to-narrative mapping
- Numeric computation or scoring
- Code compilation or script execution

Verification is structural: required sections present, required declarations made, prohibited content absent, governance rules defined.

## Required / Optional / Prohibited Fields

### Required Fields (must be present in every registry entry)

| # | Field | Format | Validation |
|---|-------|--------|-----------|
| 1 | `narrative_id` | `narrative.*` | Unique, follows namespace rules, passes Collision_Check |
| 2 | `scope_definition` | Text | Non-empty, describes shared belief structure |
| 3 | `birth_trigger` | `sc.*` | References valid canonical State_Change |
| 4 | `connected_systems` | List of `system.*` | Minimum 1 entry |
| 5 | `falsification_condition` | Text | Concrete, testable condition |
| 6 | `lifecycle_state` | `narrative.lifecycle.*` | Valid state from state machine |
| 7 | `registered_date` | ISO 8601 | Valid date |
| 8 | `registered_by` | Authority role | ARCH or GOV |

### Optional Qualitative Fields

| # | Field | Format | Constraints |
|---|-------|--------|------------|
| 1 | `display_name` | Object `{en: "...", de: "..."}` | Rendering only — never identity |
| 2 | `parent_narrative` | `narrative.*` or null | Must reference existing registry entry |
| 3 | `velocity` | Accelerating / Steady / Decelerating | Qualitative only — NOT ranking/scoring/trigger |
| 4 | `expected_duration` | Temporal_Taxonomy value | Must be valid temporal duration |
| 5 | `evidence_summary` | Text | Human-readable justification |
| 6 | `related_narratives` | List of `narrative.*` | Must reference existing registry entries |

### Prohibited Fields (MUST NOT appear in schema)

| # | Field | Prohibition Source |
|---|-------|-------------------|
| 1 | `score` / `weight` / `numeric_strength` | EC-2, NRF-REQ-9 |
| 2 | `probability` / `confidence` | EC-2, NRF-REQ-9 |
| 3 | `rank` / `priority_order` | EC-6, NRF-REQ-9 |
| 4 | `asset_list` / `ticker_symbols` | EC-4, NRF-REQ-10 |
| 5 | `correlation_matrix` | EC-5, NRF-REQ-5 |
| 6 | `recommendation` | EC-6, NRF-REQ-5 |
| 7 | `numeric_threshold` | EC-7, NRF-REQ-6 |
| 8 | `membership_weight` | EC-8, NRF-REQ-9 |

## Gap Traceability

| Gap ID | Description | Requirement ID | Severity | Resolution Phase |
|--------|-------------|---------------|----------|-----------------|
| NRG-01 | Extension criteria defined but no enforcement mechanism | NRF-REQ-4 | HIGH | Requirements (this doc) |
| NRG-02 | No explicit NARRATIVE domain — falls under ARCH | NRF-REQ-8 | MEDIUM | Requirements (declared ARCH ownership) |
| NRG-03 | No REGISTRY artifact_type — using SSOT | NRF-REQ-8, NRF-REQ-5 | MEDIUM | Design (confirm SSOT is sufficient) |
| NRG-04 | No collision-check procedure exists | NRF-REQ-3 | HIGH | Requirements (this doc) |
| NRG-05 | Hierarchy declared but no format exists | NRF-REQ-7 | MEDIUM | Design (define format) |
| NRG-06 | No governance model for lifecycle transitions | NRF-REQ-6 | HIGH | Requirements (this doc) |
| NRG-07 | Registry file not yet registered in artifact registry | NRF-REQ-8 | LOW | Tasks (register during creation) |
| NRG-08 | No versioning strategy for entries | NRF-REQ-10 | MEDIUM | Design (define versioning) |
| NRG-09 | Velocity storage format undefined | NRF-REQ-2 | LOW | Design (define valid values) |
| NRG-10 | "Narrative Registry" not in central glossary | Local glossary | MEDIUM | Deferred — requires separate governance authorization |
| NRG-11 | No automated validation tooling | — | LOW | Deferred — backlog (NOT this spec) |
| NRG-12 | System reference validation when system registry may not exist | NRF-REQ-7 | MEDIUM | Design (define validation strategy) |

### Deferred Gaps

| Gap ID | Reason for Deferral | Resolution Timing |
|--------|--------------------|--------------------|
| NRG-10 | Central glossary mutation requires separate governance authorization not granted by this spec | Future governance task |
| NRG-11 | Automated validation tooling is implementation — excluded from definition-layer spec | Backlog (CI hardening phase) |

## Invariants

The following invariants MUST be preserved throughout all deliverables produced by this spec:

| # | Invariant | Source |
|---|-----------|--------|
| 1 | Narrative Framework v2 remains the ontology SSOT — Registry does not redefine theory | Boundary definition |
| 2 | Registry stores canonical narrative definitions only — no engines, no code | NRF-REQ-1, NRF-REQ-5 |
| 3 | No narrative instance population in this spec | Out of Scope declaration |
| 4 | No asset-to-narrative mappings | NRF-REQ-10 boundary |
| 5 | No asset-list-first design — assets are never root entities in the Registry | EC-4, NRF-REQ-5 |
| 6 | State_Change remains root/cause — not demoted | Primitive chain preservation |
| 7 | Narrative remains explanatory container — not cause, not sensor | Primitive chain preservation |
| 8 | Signal remains sensor — detects, does not cause | NRF-REQ-6.5 |
| 9 | `narrative.*` IDs are immutable canonical identity | NRF-REQ-3.3 |
| 10 | Display text is rendering only — never identity | NRF-REQ-2.6 |
| 11 | No numeric scoring, weights, probabilities, or ranking | NRF-REQ-9 |
| 12 | No engines, runtime behavior, or executable code | NRF-REQ-5 |
| 13 | No central glossary mutation | Glossary Policy |
| 14 | No Market Organism Layer 0 SSOT mutation | Out of Scope declaration |

## Verification Gate Plan

| Gate ID | Gate Name | Checks |
|---------|-----------|--------|
| VG-1 | Structural Completeness | Registry schema defined; all required fields present; governance model complete; YAML structure valid |
| VG-2 | No Population | Zero narrative instances in registry file; schema and governance only |
| VG-3 | No Future-Leak | Zero numeric scores, weights, probabilities, ranking logic in schema or governance; categorical labels only |
| VG-4 | Namespace Correctness | All IDs follow `narrative.*` pattern; collision-check procedure defined; immutability declared |
| VG-5 | Lifecycle Governance | Transition authority defined; evidence requirements documented; audit trail specified; initial state = emerging |
| VG-6 | Artifact Registry Compatibility | Registry file registered in artifact_registry.yaml; follows SSOT lifecycle; topic conflict detection configured |
| VG-7 | Rendering Independence | No display text as identity; canonical IDs are language-neutral codes; display_name is optional rendering |
| VG-8 | Market Organism Compatibility | 12-domain model preserved; canonical chain preserved; no new domains added; primitive chain intact |
| VG-9 | Narrative Framework v2 Compatibility | Schema satisfies Extension Criteria (Section 13); No Dead Ends enforceable; lifecycle states match Section 6 |

## Non-Goals

This requirements foundation does NOT authorize:

- Implementation of the registry file
- Population of narrative instances
- Creation of asset-to-narrative mappings
- Design document creation (next phase, pending human review)
- Task list creation (after design, pending human review)
- Engine, runtime, or code creation
- Modification of any existing SSOT

The next step (pending human review of these requirements) is to create `design.md` specifying HOW the Narrative Registry will be structurally implemented to satisfy these requirements.
