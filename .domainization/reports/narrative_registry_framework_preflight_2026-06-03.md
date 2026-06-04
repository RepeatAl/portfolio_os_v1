# Narrative Registry Framework — Preflight Report

**Date**: 2026-06-03
**Branch**: `spec/narrative-registry-framework`
**Type**: Preflight reconnaissance / scope-definition / governance-design
**Status**: PASS — Proceed to spec creation

---

## 1. Executive Summary

**Readiness**: HIGH — All prerequisite canonical sources are in place on main. Narrative Framework v2 defines the ontology, extension criteria, and required fields. The governance infrastructure (artifact registry, domain registry, lifecycle state machine) is mature and well-documented.

**Primary Risk**: Premature population — the strongest gravitational pull will be toward "let's just add a few narratives" before governance rules are locked. The registry framework spec MUST define the container, governance model, and verification gates BEFORE any narrative instance enters.

**Recommendation**: **PROCEED** to spec creation for `narrative-registry-framework`. Create requirements.md, design.md, and tasks.md. Do NOT populate the registry or create narrative instances as part of this spec.

---

## 2. Source Inventory

### Documents Read

| # | Source | Authority | Status |
|---|--------|-----------|--------|
| 1 | `docs/README_narrative_framework.md` | SSOT — Narrative ontology (v2, canonical) | ✅ Present on main |
| 2 | `docs/README_narrative_framework_alignment_implementation_guide.md` | Supplementary guide | ✅ Present on main |
| 3 | `.kiro/specs/narrative-framework-alignment/requirements.md` | Spec requirements (closed) | ✅ Present on main |
| 4 | `.kiro/specs/narrative-framework-alignment/design.md` | Spec design (closed) | ✅ Present on main |
| 5 | `.kiro/specs/narrative-framework-alignment/tasks.md` | Spec tasks (52/52 complete) | ✅ Present on main |
| 6 | `.domainization/reports/post_merge_health_check_narrative_framework_alignment_2026-06-03.md` | Governance report | ✅ Present on main |
| 7 | `docs/market_organism/README_market_organism_principles.md` | SSOT — Market Organism Layer 0 | ✅ Present on main |
| 8 | `docs/market_organism/README_state_change_taxonomy.md` | SSOT — State_Change definitions | ✅ Present on main |
| 9 | `docs/market_organism/README_dependency_types_v2.md` | SSOT — Dependency types | ✅ Present on main |
| 10 | `docs/market_organism/README_temporal_taxonomy.md` | SSOT — Temporal properties | ✅ Present on main |
| 11 | `docs/market_organism/README_expansion_taxonomy.md` | SSOT — Expansion taxonomy | ✅ Present on main |
| 12 | `docs/market_organism/README_shared_glossary_reference.md` | SSOT — Glossary reference | ✅ Present on main |
| 13 | `.domainization/artifact_registry.yaml` | Governance — Artifact registration | ✅ Present on main |
| 14 | `.domainization/domain_registry.yaml` | Governance — 12-domain model | ✅ Present on main |
| 15 | `.domainization/lifecycle_state_machine.yaml` | Governance — Lifecycle states | ✅ Present on main |

### Canonical Authority Hierarchy

```
Market Organism Principles (Layer 0)
  └── Narrative Framework v2 (SSOT — defines ontology)
        └── Narrative Registry Framework (NEW — defines governance + schema)
              └── Future: Narrative Instance Population (NOT THIS SPEC)
```

### Missing or Ambiguous Sources

| Item | Status | Impact |
|------|--------|--------|
| Existing `narrative_registry.yaml` file | DOES NOT EXIST | Expected — this spec defines the governance before the file exists |
| Central glossary entry for "Narrative Registry" | DOES NOT EXIST | Must be defined glossary-first in this spec |
| Asset-to-Narrative mapping spec | DOES NOT EXIST | Intentionally out of scope — future spec |

---

## 3. Registry Boundary Definition

### What the Narrative Registry IS

A governance-controlled YAML/data artifact that stores the canonical list of recognized narratives with their required metadata fields. It is the single source of truth for "which narratives officially exist" in Portfolio OS. It is a definition-layer artifact — not runtime code.

### What the Narrative Registry is NOT

| Not This | Why |
|----------|-----|
| The Narrative Framework itself | The Framework defines WHAT a narrative IS. The Registry stores WHICH narratives exist. |
| An Asset-to-Narrative mapping | The Registry defines narratives. A separate Asset-to-Narrative Registry (future) maps assets to them. |
| An engine or runtime artifact | The Registry is a data file with governance rules. It does not execute, score, or compute. |
| A dashboard or visualization | No UI. The Registry is consumed by future engines, not displayed directly. |
| A recommendation system | The Registry does not recommend, rank, or prioritize narratives. |

### How It Differs from Narrative Framework v2

| Narrative Framework v2 | Narrative Registry |
|------------------------|-------------------|
| Defines the ontology (what IS a narrative) | Stores instances (which narratives exist) |
| Defines lifecycle state machine | Tracks current lifecycle state per narrative |
| Defines extension criteria | Enforces extension criteria at registration |
| Defines required fields | Requires fields to be populated per entry |
| SSOT for narrative theory | SSOT for narrative population |
| Does not contain actual narrative entries | Contains actual narrative entries |

### How It Differs from Asset-to-Narrative Registry

| Narrative Registry | Asset-to-Narrative Registry (future) |
|-------------------|--------------------------------------|
| Stores narrative definitions | Stores asset-narrative membership relationships |
| One entry per narrative | Many entries per narrative (one per asset) |
| Fields: ID, scope, birth trigger, systems, falsification | Fields: asset_id, narrative_id, membership_type, influence |
| No asset references as primary keys | Asset references are primary keys |
| Governance: who can create narratives | Governance: who can assign assets to narratives |

---

## 4. Candidate Registry Entry Model

### Required Fields (from Narrative Framework v2, Section 13)

| # | Field | Format | Source |
|---|-------|--------|--------|
| 1 | `narrative_id` | `narrative.*` canonical ID | NFA-REQ-1 |
| 2 | `scope_definition` | Text — what shared belief this represents | NFA-REQ-8.3 |
| 3 | `birth_trigger` | `sc.*` canonical State_Change ID | NFA-REQ-8.3, NFA-REQ-5.3 |
| 4 | `connected_systems` | List of `system.*` IDs (minimum 1) | NFA-REQ-8.3, NFA-REQ-5.4 |
| 5 | `falsification_condition` | Text — what would invalidate this narrative | NFA-REQ-8.3 |
| 6 | `lifecycle_state` | `narrative.lifecycle.*` canonical ID | NFA-REQ-3 |
| 7 | `registered_date` | ISO 8601 date | Governance requirement |
| 8 | `registered_by` | Authority role | Governance requirement |

### Optional Qualitative Fields (candidates for design review)

| # | Field | Format | Notes |
|---|-------|--------|-------|
| 1 | `display_name` | Object with language keys | Rendering only — never identity (NFA-REQ-1.3) |
| 2 | `parent_narrative` | `narrative.*` ID or null | Hierarchy containment (Section 7) |
| 3 | `velocity` | Accelerating / Steady / Decelerating | Qualitative observation only (Design Decision D-5) |
| 4 | `expected_duration` | Temporal_Taxonomy duration value | Qualitative temporal estimate |
| 5 | `evidence_summary` | Text | Human-readable justification for inclusion |
| 6 | `related_narratives` | List of `narrative.*` IDs | Non-hierarchical relationships |

### Prohibited Fields (MUST NOT appear in registry schema)

| # | Field | Why Prohibited |
|---|-------|---------------|
| 1 | `score` / `weight` / `numeric_strength` | EC-2: No numeric scoring (NFA-REQ-2) |
| 2 | `probability` / `confidence` | EC-2: No probabilities |
| 3 | `rank` / `priority_order` | EC-6: No ranking logic |
| 4 | `asset_list` / `ticker_symbols` | EC-4: Assets are not root entities; belongs in Asset-to-Narrative Registry |
| 5 | `correlation_matrix` | EC-5: No correlation matrices |
| 6 | `recommendation` | EC-6: No recommendation logic |
| 7 | `numeric_threshold` | EC-7: No numeric lifecycle thresholds |
| 8 | `membership_weight` | EC-8: No numeric membership weights |

### Future Implementation Fields (deferred — NOT for this spec)

| # | Field | Why Deferred |
|---|-------|-------------|
| 1 | `asset_count` | Requires Asset-to-Narrative Registry |
| 2 | `signal_detectors` | Requires Signal-to-Narrative mapping |
| 3 | `propagation_paths` | Requires runtime propagation engine |
| 4 | `historical_transitions` | Requires lifecycle tracking engine |

---

## 5. Governance Model

### Creation Authority

| Authority | Role | Conditions |
|-----------|------|-----------|
| Primary | ARCH domain (Portfolio Architect) | Must satisfy all 4 inclusion criteria |
| Secondary | GOV domain (Governance) | Can authorize creation when ARCH proposes |
| Prohibited | Automated systems | No engine or automated process may create narratives without human authorization |

### Review Authority

| Reviewer | Responsibility |
|----------|---------------|
| ARCH | Structural correctness — does it satisfy inclusion criteria? |
| GOV | Governance compliance — does it follow naming rules, no future-leak? |

### Amendment Rules

1. Scope definition may be refined (narrowed or clarified) without changing the canonical ID
2. Connected systems may be added (never removed without deprecation)
3. Falsification conditions may be refined (made more specific)
4. Display text may be changed freely (rendering, not identity)
5. Canonical ID is IMMUTABLE once assigned — amendment requires deprecation + new entry

### Deprecation Rules

1. A narrative may be deprecated when its falsification condition is met
2. Deprecation requires a State_Change reference proving invalidation
3. Deprecated narratives remain in the registry with `lifecycle_state: narrative.lifecycle.dead`
4. Deprecated narratives retain their canonical ID permanently (no recycling)
5. Deprecation date and reason must be recorded

### Retirement Rules

1. Retirement = removal from active registry (moved to historical archive)
2. Retirement is only permitted AFTER deprecation + a governance-defined cooling period
3. Retired narrative IDs are NEVER reassigned
4. Historical references to retired narratives remain valid (ID is stable forever)

### Conflict Handling

1. If two proposed narratives overlap in scope, the more specific one takes precedence
2. If scope overlap cannot be resolved, a meta-narrative/sub-narrative hierarchy is proposed
3. Conflicts are resolved by ARCH with GOV concurrence

### Duplicate Narrative Handling

1. Before any new narrative registration, a namespace collision check is performed
2. If an existing narrative already covers the proposed belief structure, registration is REJECTED
3. The proposer may refine the scope to differentiate from existing narratives
4. Genuine duplicates are resolved by pointing to the existing canonical ID

---

## 6. Inclusion / Exclusion Criteria

Based on Narrative Framework v2, Section 13.

### What Qualifies

A narrative qualifies for canonical registry inclusion when it satisfies ALL of:

1. **Distinct shared belief**: Represents a belief structure not already covered by existing narratives
2. **Falsifiable**: Contradicting evidence can invalidate it (must state condition explicitly)
3. **Connects State_Change to System**: At least one `sc.*` → `narrative.*` → `system.*` path exists
4. **Has canonical ID**: Assigned a `narrative.*` ID before first use

### What Does NOT Qualify

1. A theme without an identifiable originating State_Change
2. A sector classification without a causal belief
3. A statistical pattern without a shared market interpretation

### Evidence Requirements

- Birth trigger State_Change must reference a real, identifiable market event
- Connected System must reference a valid `system.*` ID from the System taxonomy
- Scope definition must be specific enough to distinguish from adjacent narratives
- Falsification condition must be testable — an observer could determine if met

### Falsification Requirements

- Every narrative MUST declare at least one falsification condition at registration
- Falsification conditions must be concrete (not "narrative loses relevance")
- When a falsification condition is met, a State_Change triggers lifecycle transition to weakening or dead

---

## 7. ID Namespace Rules

### `narrative.*` Assignment

- Format: `narrative.[descriptive_token]`
- Token: lowercase, underscore-separated, language-neutral, stable once assigned
- Examples: `narrative.ai_infrastructure`, `narrative.higher_for_longer`
- Lifecycle states: `narrative.lifecycle.[state]`

### Collision Prevention

- Before registration, check entire `narrative.*` namespace for exact and semantic collisions
- Semantic collision: two IDs that describe the same belief (e.g., `narrative.ai_capex` vs `narrative.ai_infrastructure_spend`)
- Resolution: reject the new entry, or merge scopes under one canonical ID

### Display Text Independence

- Display text (EN: "AI Infrastructure", DE: "KI-Infrastruktur") is rendering — never identity
- Changing display text does NOT change the canonical ID
- No display text appears in the ID itself

(See: README_language_rendering_framework, Section: Rule 4 — Display Text is Never Identity)

### Language Rendering Independence

- English tokens in IDs are canonical codes, not English language text
- `narrative.ai_infrastructure` is a code — not an English phrase
- Rendering into any language is a presentation concern

### Rename Policy

- Canonical IDs are IMMUTABLE
- If a rename is needed: deprecate the old ID, create a new one, map the old → new in the registry
- Consumers referencing the old ID receive the deprecation notice

### Deprecated ID Policy

- Deprecated IDs remain in the registry forever (no deletion)
- Deprecated IDs carry: `deprecated_date`, `deprecation_reason`, `replacement_narrative_id` (if applicable)
- Deprecated IDs are never reassigned to different narratives

---

## 8. Integration Surface

### State_Change Taxonomy

- Every narrative references at least one `sc.*` ID as its birth trigger
- Narrative lifecycle transitions are caused by State_Changes
- Integration: Registry entries point TO State_Change taxonomy; State_Change taxonomy does not point to Registry

(See: README_state_change_taxonomy, Section: Classification Hierarchy)

### Dependency_Types_v2

- `dep.narrative` is one of 10 equal Dependency_Types — a propagation MECHANISM
- The Registry defines Narrative Containers (the STRUCTURE)
- Integration: Registry entries are the destination of `dep.narrative` propagation paths
- Registry does NOT define dependency types or modify them

(See: README_dependency_types_v2, Section: Narrative)

### Temporal Taxonomy

- `expected_duration` field (optional) uses Temporal_Taxonomy duration values
- `velocity` is narrative-specific — NOT a Temporal_Taxonomy property
- Integration: Registry may reference temporal properties; does NOT extend the Temporal_Taxonomy

(See: README_temporal_taxonomy, Section: Temporal Property Enumeration)

### Expansion Taxonomy

- Connected systems link narratives to expansion paths
- Integration: Registry references `system.*` IDs; does NOT define systems or expansion paths

(See: README_expansion_taxonomy, Section: Expansion Definition)

### Explanation Framework

- Narratives serve as Level 4 in the explanation chain
- Registry provides the data needed for Level 4 traversal: canonical ID, lifecycle state, birth trigger
- Integration: Registry enables explanation traversal; does NOT modify the Explanation Framework

(See: README_explanation_framework, Section: Explanation Levels)

### Artifact Registry

- The Narrative Registry file itself must be registered in `.domainization/artifact_registry.yaml`
- Proposed artifact_type: SSOT (canonical data, not engine output)
- Proposed primary_domain: ARCH
- Proposed lifecycle_status: draft → review → canonical
- Integration: Registry follows the same lifecycle state machine as other SSOTs

### Future Asset-to-Narrative Registry

- The Narrative Registry is a PREREQUISITE for the Asset-to-Narrative Registry
- The Asset-to-Narrative Registry will reference `narrative.*` IDs from this Registry
- This spec does NOT create the Asset-to-Narrative Registry — it only ensures compatibility

---

## 9. Hard Exclusions

The following are explicitly excluded from the Narrative Registry Framework spec:

| # | Exclusion | Rationale |
|---|-----------|-----------|
| 1 | Actual narrative instance population | Governance must be defined before population |
| 2 | Asset-to-narrative mappings | Separate future spec |
| 3 | Scoring / numeric weights | EC-2 prohibition |
| 4 | Ranking / priority ordering | EC-6 prohibition |
| 5 | Probabilities / confidence values | EC-2 prohibition |
| 6 | Dashboards / visualizations | EC-3 prohibition |
| 7 | Engines / runtime code | EC-1 prohibition |
| 8 | Portfolio recommendations | EC-6 prohibition |
| 9 | Correlation matrices | EC-5 prohibition |
| 10 | Modification of existing SSOTs | Governance boundary |
| 11 | Central glossary mutation | Must be separately authorized |
| 12 | Signal-to-Narrative mapping | Future spec after Registry + Asset-to-Narrative exist |

---

## 10. Gap Matrix

| Gap ID | Source | Description | Risk | Severity | Proposed Resolution | Phase |
|--------|--------|-------------|------|----------|--------------------|----|
| NRG-01 | Narrative Framework v2 §13 | Extension criteria defined but no enforcement mechanism exists | Registry population without validation | HIGH | Define enforcement gate in requirements | Requirements |
| NRG-02 | Domain Registry | No explicit "NARRATIVE" domain — narratives fall under ARCH | Unclear ownership as system grows | MEDIUM | Declare ARCH as narrative governance owner in requirements; evaluate domain addition in backlog | Requirements |
| NRG-03 | Lifecycle State Machine | No `REGISTRY` artifact_type — must use existing SSOT or define new | Schema mismatch risk | MEDIUM | Use SSOT artifact_type for registry file; add REGISTRY type in backlog if needed | Design |
| NRG-04 | Narrative Framework v2 §4 | `narrative.*` namespace defined but no collision-check procedure exists | Duplicate/overlapping narratives | HIGH | Define collision-check procedure in requirements | Requirements |
| NRG-05 | Narrative Framework v2 §7 | Hierarchy is "declared, not computed" but no declaration format exists | Inconsistent parent-child relationships | MEDIUM | Define hierarchy declaration format in design | Design |
| NRG-06 | None | No governance model for "who can transition lifecycle states" | Unauthorized lifecycle mutations | HIGH | Define lifecycle transition authority in requirements | Requirements |
| NRG-07 | Artifact Registry | Narrative Registry file not yet registered | Governance gap at creation time | LOW | Register in artifact registry as part of tasks | Tasks |
| NRG-08 | None | No versioning strategy for registry entries | Breaking changes without tracking | MEDIUM | Define entry versioning in design | Design |
| NRG-09 | Narrative Framework v2 §6 | Velocity field is "qualitative observation" but no storage format defined | Inconsistent velocity annotations | LOW | Define valid values and storage format in design | Design |
| NRG-10 | Central Glossary | "Narrative Registry" not yet defined as a glossary term | Glossary-first violation | MEDIUM | Define term in requirements glossary section | Requirements |
| NRG-11 | None | No automated validation tooling for registry compliance | Manual-only verification is error-prone | LOW | Propose validation script in backlog (NOT this spec) | Backlog |
| NRG-12 | Narrative Framework v2 §12 | No Dead Ends Guarantee requires connected systems, but system registry may not exist yet | Unverifiable connections | MEDIUM | Define system reference validation rules in design | Design |

---

## 11. Candidate Requirements (Draft)

| ID | Title | Summary |
|----|-------|---------|
| NRF-REQ-1 | Registry Boundary | Define what the Narrative Registry is and is not; distinguish from Framework, Asset-to-Narrative, and engines |
| NRF-REQ-2 | Canonical Entry Fields | Define required, optional, and prohibited fields per entry; enforce required field completeness |
| NRF-REQ-3 | ID Governance | Define namespace rules, collision prevention, immutability, deprecation, and retirement policies |
| NRF-REQ-4 | Inclusion Criteria | Formalize the 4 inclusion criteria as enforceable registration gates |
| NRF-REQ-5 | Exclusion Constraints | Consolidate prohibitions: no scoring, ranking, probability, asset-lists-as-root, engines |
| NRF-REQ-6 | Lifecycle Governance | Define who can transition lifecycle states, what evidence is required, and audit trail requirements |
| NRF-REQ-7 | Cross-Reference Contract | All references use canonical format; registry entries reference State_Changes and Systems by canonical ID |
| NRF-REQ-8 | Artifact Registry Integration | Registry file registered in domainization system; follows SSOT lifecycle; domain ownership declared |
| NRF-REQ-9 | No Future-Leak | Explicitly prohibit numeric scoring, ranking, probability, optimization in registry schema and governance |
| NRF-REQ-10 | Readiness for Future Asset-to-Narrative Registry | Schema and governance designed to be consumed by a future Asset-to-Narrative Registry without breaking changes |

---

## 12. Verification Gate Proposal

| Gate ID | Gate Name | Checks |
|---------|-----------|--------|
| VG-1 | Structural Completeness | Registry schema defined; all required fields present; governance model complete |
| VG-2 | No Population | Zero narrative instances in registry file; schema only |
| VG-3 | No Future-Leak | Zero numeric scores, weights, probabilities, ranking logic in schema or governance |
| VG-4 | Namespace Correctness | All IDs follow `narrative.*` pattern; collision-check procedure defined |
| VG-5 | Lifecycle Governance | Transition authority defined; audit trail specified; evidence requirements documented |
| VG-6 | Artifact Registry Compatibility | Registry file registered in artifact_registry.yaml; follows SSOT lifecycle |
| VG-7 | Rendering Independence | No display text as identity; canonical IDs are language-neutral codes |
| VG-8 | Market Organism Compatibility | 12-domain model preserved; canonical chain preserved; no new domains added |
| VG-9 | Narrative Framework v2 Compatibility | Schema satisfies all Extension Criteria (Section 13); No Dead Ends enforceable |

---

## 13. Risks and Blockers

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | Premature narrative population | HIGH | Hard exclusion in spec; VG-2 gate; no instances in deliverable |
| 2 | Accidental asset-first design | HIGH | Prohibited fields list; no asset_list field; explicit boundary with Asset-to-Narrative |
| 3 | Scoring leakage | HIGH | Prohibited fields; VG-3 gate; EC-2 enforcement |
| 4 | Duplicate/overlapping narratives | MEDIUM | Collision-check procedure; semantic overlap review |
| 5 | Unclear ownership | MEDIUM | Explicit ARCH ownership; governance model in requirements |
| 6 | Central glossary mutation risk | MEDIUM | Glossary amendments LOCAL to spec; no central mutation authorized |
| 7 | Registry vs engine confusion | MEDIUM | Explicit boundary definition; Hard Exclusions section; VG-1 checks |
| 8 | System reference validation | MEDIUM | Acknowledge `system.*` IDs may not all exist yet; define validation strategy |
| 9 | Velocity field misuse | LOW | Explicit prohibition on using velocity as ranking/scoring/trigger |
| 10 | Lifecycle transition without evidence | MEDIUM | Require State_Change reference for every transition |

### Blockers

None identified. All prerequisites are in place. Proceed.

---

## 14. Final Recommendation

**PROCEED** to create:
- `.kiro/specs/narrative-registry-framework/requirements.md`
- `.kiro/specs/narrative-registry-framework/design.md`
- `.kiro/specs/narrative-registry-framework/tasks.md`

**Workflow**: Requirements-first (business needs drive technical design)

**Scope**: Definition-layer ONLY. The spec defines the registry schema, governance model, and verification gates. It does NOT populate the registry with actual narrative instances.

**Next steps after this spec**:
1. Create requirements.md — formalize NRF-REQ-1 through NRF-REQ-10
2. Create design.md — specify registry file format, governance procedures, integration contracts
3. Create tasks.md — define implementation steps (create registry file with schema only, register in artifact registry, create governance documentation)

**After this spec is complete and merged**:
- Narrative Registry Population (separate spec) — adds actual narrative instances
- Asset-to-Narrative Registry (separate spec) — maps assets to narratives

---

*Report generated: 2026-06-03*
*Type: Preflight reconnaissance*
*Author: Kiro (automated analysis)*
*No canonical SSOTs were modified.*
*No implementation work was performed.*
