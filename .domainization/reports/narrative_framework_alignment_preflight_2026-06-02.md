# Narrative Framework Alignment — Preflight Report

**Date**: 2026-06-02
**Branch**: `spec/narrative-framework-alignment`
**Status**: PREFLIGHT — reconnaissance only, no implementation
**Author**: Kiro (CTO delegation)

---

## 1. Executive Summary

### Overall Readiness: HIGH — Proceed with alignment spec

The existing Narrative Framework (`docs/README_narrative_framework.md`) is well-structured and already largely compatible with the Market Organism Layer 0. It correctly positions Narrative as the explanatory container in the primitive chain and explicitly distinguishes it from State_Change, Signal, and Asset. However, several alignment gaps exist that require formalization.

### Primary Alignment Risk

The Narrative Framework uses **natural language display text as identity** (e.g., "AI Infrastructure" as a narrative name rather than a canonical `narrative.ai_infrastructure` ID). This violates the Language Rendering Framework's canonical ID rules and the Market Organism's Rule 3 (Canonical ID Enforcement). The framework also lacks YAML metadata in its current form that conforms to the cross-reference convention established by the Market Organism deliverables.

### Recommendation: PROCEED

The alignment spec should be created. The work is primarily:
1. Canonical ID namespace formalization (`narrative.*`)
2. Cross-reference convention adoption
3. Lifecycle state formalization with canonical IDs
4. Explicit Explanation Framework integration contract
5. Signal_Bubble_v0 sensor relationship declaration
6. No structural rewrite needed — the ontology is sound

---

## 2. Source Inventory

### Documents Read

| # | Document | Path | Authority |
|---|----------|------|-----------|
| 1 | Market Organism Requirements | `.kiro/specs/market-organism-framework/requirements.md` | Canonical (Layer 0) |
| 2 | Market Organism Design | `.kiro/specs/market-organism-framework/design.md` | Canonical (Layer 0) |
| 3 | Market Organism Tasks | `.kiro/specs/market-organism-framework/tasks.md` | Reference |
| 4 | Market Organism Principles | `docs/market_organism/README_market_organism_principles.md` | Canonical SSOT |
| 5 | State Change Taxonomy | `docs/market_organism/README_state_change_taxonomy.md` | Canonical SSOT |
| 6 | Dependency Types v2 | `docs/market_organism/README_dependency_types_v2.md` | Canonical SSOT |
| 7 | Temporal Taxonomy | `docs/market_organism/README_temporal_taxonomy.md` | Canonical SSOT |
| 8 | Expansion Taxonomy | `docs/market_organism/README_expansion_taxonomy.md` | Canonical SSOT |
| 9 | Shared Glossary Reference | `docs/market_organism/README_shared_glossary_reference.md` | Canonical SSOT |
| 10 | Narrative Framework | `docs/README_narrative_framework.md` | Canonical SSOT (Layer 1) |
| 11 | User Intelligence Journey | `docs/README_user_intelligence_journey_framework.md` | Canonical SSOT |
| 12 | Journey Capability Matrix | `docs/README_journey_capability_matrix.md` | Canonical SSOT |
| 13 | Engine Roadmap | `docs/README_engine_roadmap_framework.md` | Canonical SSOT |
| 14 | Language Rendering Framework | `docs/README_language_rendering_framework.md` | Canonical SSOT |
| 15 | Explanation Framework | `docs/README_explanation_framework.md` | Canonical SSOT |
| 16 | Market Data Governance | `docs/README_market_data_governance_framework.md` | Canonical SSOT |

### Canonical Authority Hierarchy

```
Layer 0: Market Organism Framework (5 deliverables) — CONSTRAINS ALL BELOW
Layer 1: Narrative Framework ← THIS ALIGNMENT TARGET
Layer 2: User Intelligence Journey
Layer 3: Journey Capability Matrix
Layer 4: Engine Roadmap
Layer 5: Implementation (future)
```

### Missing or Ambiguous Sources

- No formal `narrative.*` canonical ID registry exists yet
- No explicit cross-reference from Narrative Framework back to Market Organism deliverables
- No Signal_Bubble_v0 relationship declaration in the Narrative Framework
- The Narrative Framework references Market Organism concepts but uses its own terminology conventions

---

## 3. Current Narrative Framework Assessment

### What the Current Framework Already Does Well

1. **Correct primitive positioning**: Narrative is explicitly defined as the "explanatory container" — second in the primitive chain after State_Change
2. **Clear distinction from State_Change**: Detailed table contrasting the two primitives (event vs belief, discrete vs extended, objective vs interpreted)
3. **Lifecycle model defined**: Six lifecycle states (Emerging → Strengthening → Dominant → Weakening → Dormant → Dead) with descriptions and capital flow implications
4. **State_Change-to-Narrative interactions defined**: Five interaction types (Creates, Strengthens, Weakens, Kills, Revives) with examples
5. **Hierarchy rules established**: Meta-narratives contain sub-narratives, depth is practical (2-3 levels)
6. **Multi-narrative membership defined**: Primary/secondary/emerging/legacy with strength qualifiers
7. **Temporal properties acknowledged**: Birth, peak, duration, expected lifespan, regime sensitivity
8. **Explicit non-goals stated**: Not implementation, not data model, not scoring, not prediction
9. **Dependency_Type dual-use explained**: Distinguishes `dep.narrative` (mechanism) from Narrative-as-Container (structure)
10. **Falsifiability defined**: A narrative can be invalidated — this is formally correct for the organism model

### What Is Missing Relative to Market Organism Layer 0

| Gap | Severity | Description |
|-----|----------|-------------|
| No canonical `narrative.*` IDs | HIGH | Narrative instances use display text ("AI Infrastructure") instead of stable IDs (`narrative.ai_infrastructure`) |
| No YAML metadata header | MEDIUM | Document lacks the artifact_id/primary_domain/lifecycle_status metadata block that all Layer 0 docs carry |
| No cross-reference convention | MEDIUM | Does not use `(See: [Deliverable_Name], Section: [Section_Title])` format |
| No exclusion constraints section | MEDIUM | Missing the consolidated prohibitions section required by Layer 0 pattern |
| No Signal_Bubble_v0 relationship | MEDIUM | Does not declare how narratives relate to signals-as-sensors |
| No explanation readiness section | MEDIUM | Does not define how narratives participate in the 6-level explanation chain |
| No extension criteria | LOW | Missing formal criteria for adding new narratives (what qualifies a narrative for canonical registry) |
| No Feedback_Loop integration | LOW | Does not explain how narrative feedback loops work within the non-DAG mandate |
| "strength-weighted" language | HIGH | Multi-Narrative Rule 4 uses "strength-weighted" — potential future-leak into numeric scoring territory |
| Membership strength values | MEDIUM | Uses "strong/moderate/weak" without declaring these as qualitative-only (could drift toward numeric) |

### Where Terminology May Drift

| Term in Narrative Framework | Market Organism Canonical | Risk |
|----------------------------|--------------------------|------|
| "strength-weighted" (Rule 4) | No numeric weights permitted (Principle/Exclusion EC-2) | HIGH — implies future scoring |
| "primary narrative" | Could confuse with "primary classification" in State_Change_Taxonomy | LOW |
| "narrative_id" (in conceptual schema) | Correct direction, but needs `narrative.*` namespace | MEDIUM |
| "regime sensitivity" | Overlaps with Market Regime Framework; needs cross-reference | LOW |
| "velocity" (temporal property) | Not in canonical Temporal_Taxonomy (which uses Latency/Duration/Amplification/Dampening) | MEDIUM |

---

## 4. Primitive Responsibility Audit

| Primitive | Expected Role | Current Narrative Framework | Status |
|-----------|---------------|----------------------------|--------|
| State_Change | Cause / Root | ✅ Explicitly NOT a narrative; "a State_Change is an event that happened" | **PASS** |
| Narrative | Explanatory Container | ✅ "A shared market belief structure that connects a State_Change to a set of affected Systems and Assets" | **PASS** |
| System | Affected Functional Domain | ✅ Referenced as the intermediate layer between Narrative and Asset | **PASS** |
| Asset | Observable Endpoint | ✅ "Assets are observation points"; multi-narrative membership is on assets, not from assets | **PASS** |
| Signal | Sensor | ⚠️ Not explicitly addressed. The framework says "A Narrative is NOT a signal (too atomic)" but does not declare signals-as-sensors role | **NEEDS DECLARATION** |
| Reasoning_Object | Conclusion Primitive | ✅ Not mentioned — correctly left to REASONING domain | **PASS** |
| Explanation_Object | Understanding Primitive | ⚠️ Explanation Framework shows Narrative at Level 4, but Narrative Framework doesn't reference this contract | **NEEDS CROSS-REF** |

### Audit Result: PASS with 2 declarations needed

No primitive responsibility is violated. The framework does not promote Narrative to causal root status. Two explicit declarations are missing:
1. Signal sensor relationship (narratives are NOT signals; signals detect narrative-level effects)
2. Explanation traversal contract (narratives serve as Level 4 in the explanation chain)

---

## 5. Alignment Gap Matrix

| Gap ID | Current Source | Market Organism Requirement/Invariant | Severity | Proposed Resolution | Phase |
|--------|---------------|--------------------------------------|----------|---------------------|-------|
| NAG-01 | No `narrative.*` IDs | Rule 3: Canonical ID Enforcement | HIGH | Define `narrative.*` namespace with stable IDs for all canonical narratives | Requirements |
| NAG-02 | "strength-weighted" (Rule 4) | Rule 4: No Silent Future-Leak (no weights) | HIGH | Replace with qualitative descriptor or remove; declare narrative membership as qualitative-only | Requirements |
| NAG-03 | No YAML metadata | Layer 0 pattern: all deliverables carry metadata | MEDIUM | Add standard YAML header to Narrative Framework | Tasks |
| NAG-04 | No cross-reference convention | Req 10.8: explicit cross-references | MEDIUM | Add `(See: ...)` references to all Market Organism deliverables | Tasks |
| NAG-05 | No exclusion constraints section | Req 8.7: consolidated prohibitions | MEDIUM | Add Exclusion Constraints section prohibiting engines/scores/numeric weights | Requirements |
| NAG-06 | No Signal_Bubble_v0 declaration | Req 12.4: organism does not replace signals | MEDIUM | Add Architectural Compatibility section declaring signals-as-sensors | Requirements |
| NAG-07 | No explanation readiness | Req 10.8: explanation readiness | MEDIUM | Add section defining how narratives participate in Level 4 explanation traversal | Design |
| NAG-08 | Narrative "velocity" property | Temporal_Taxonomy uses Latency/Duration/Amp/Damp only | MEDIUM | Map "velocity" to canonical temporal properties or declare as narrative-specific (non-temporal) | Design |
| NAG-09 | No extension criteria | Layer 0 pattern: criteria-gated additions | LOW | Define what qualifies a new narrative for canonical registry (distinct belief + evidence + falsifiability) | Requirements |
| NAG-10 | No Feedback_Loop integration | Principle 4: Feedback is Structural | LOW | Add section explaining narrative feedback loops (e.g., narrative strengthens → more capital → narrative strengthens further) | Design |
| NAG-11 | "strength: strong/moderate/weak" | Rule 4: no numeric scoring | LOW | Declare explicitly as qualitative-only; add prohibition on converting to numeric scale | Requirements |
| NAG-12 | Lifecycle state machine lacks IDs | Rule 3: Canonical ID Enforcement | MEDIUM | Assign `narrative.lifecycle.*` or similar IDs to each lifecycle state | Requirements |
| NAG-13 | No `dep.narrative` cross-reference | Req 10.8: cross-reference to Dependency_Types_v2 | LOW | Add explicit reference to `dep.narrative` definition and distinguish mechanism from container | Tasks |
| NAG-14 | No rendering independence | Language Rendering Framework: `narrative.*` IDs are primary keys, display text is rendering | HIGH | Formalize separation of canonical identity from display text | Requirements |

---

## 6. Proposed Spec Boundary

### In Scope

- Formalize `narrative.*` canonical ID namespace
- Add YAML metadata header conforming to Layer 0 pattern
- Add cross-reference convention usage to/from all Market Organism deliverables
- Add exclusion constraints section
- Add Signal_Bubble_v0 and Signal Reusability architectural compatibility declarations
- Add explanation readiness section (Level 4 explanation chain contract)
- Replace "strength-weighted" language with qualitative-only descriptors
- Define narrative extension criteria (what qualifies a new narrative for registry)
- Define narrative feedback loop integration with non-DAG mandate
- Formalize lifecycle state machine with canonical IDs
- Declare rendering independence (identity ≠ display text)
- Cross-reference `dep.narrative` from Dependency_Types_v2

### Out of Scope

- Engine implementation (Asset-to-Narrative Registry is P0, not this spec)
- Actual narrative instance registry population (which specific narratives exist)
- Scoring, ranking, or numeric confidence for narrative strength
- Dashboard or visualization specifications
- Data integration or external data sources
- Narrative prediction or forecasting logic
- Temporal_Taxonomy extension (velocity is NOT a new temporal property — it's a narrative-specific observation)

### Explicit Exclusions

- No Python code, engines, or executable logic
- No numeric scores, weights, or probabilities assigned to narratives
- No recommendation logic for narrative-based portfolio decisions
- No optimization logic for narrative portfolio allocation
- No correlation matrices between narratives
- No dashboard designs for narrative visualization
- No actual narrative data population

### Non-Goals

- This spec does NOT create the Asset-to-Narrative Registry (that's P0 engine work)
- This spec does NOT define specific narrative instances (that's registry population)
- This spec does NOT score narratives (that's future engine logic)
- This spec does NOT predict narrative lifecycle transitions (that's future intelligence)

### Future Implementation Boundaries

| Boundary | Belongs To |
|----------|-----------|
| Building the Asset-to-Narrative Registry engine | P0 spec (Engine Roadmap) |
| Populating narrative instances with real data | Post-P0 operational task |
| Scoring narrative strength | Future engine (post-P1) |
| Predicting narrative transitions | Future intelligence layer |
| Narrative sentiment analysis | Signal layer (sensors) |

---

## 7. Candidate Deliverables

The following deliverables are proposed for the actual spec. They are NOT created yet.

| # | Candidate Deliverable | Purpose |
|---|----------------------|---------|
| 1 | Narrative Framework v2 (aligned) | Updated SSOT with all alignment gaps resolved |
| 2 | Narrative Canonical ID Namespace Registry | Formal `narrative.*` ID scheme with assignment rules |
| 3 | Narrative Explanation Traversal Contract | Defines Level 4 explanation chain participation |
| 4 | Narrative-to-State_Change Mapping Rules | Formalizes the 5 interaction types with canonical IDs |
| 5 | Narrative Lifecycle State Machine (formal) | Lifecycle states with canonical IDs and transition rules |
| 6 | Narrative Architectural Compatibility Declaration | Signal Reusability, Signal_Bubble_v0, 12-domain preservation |
| 7 | Narrative Extension Criteria | What qualifies a new narrative for canonical status |

**Note**: These may be consolidated into fewer documents during design phase. The Narrative Framework v2 may absorb several of these as sections rather than standalone documents.

---

## 8. Candidate Requirements

The following are DRAFT candidate requirements. They are NOT finalized.

### CR-1: Canonical ID Namespace Formalization

THE Narrative Framework SHALL assign every canonical narrative a stable, language-independent identifier using the `narrative.*` namespace pattern, and SHALL declare that display text (in any language) is rendering, not identity.

### CR-2: Future-Leak Prohibition

THE Narrative Framework SHALL explicitly prohibit numeric scores, weights, probabilities, ranking logic, and optimization logic for narrative strength, lifecycle transitions, or membership assessment within the definition layer.

### CR-3: Lifecycle State Machine Formalization

THE Narrative Framework SHALL define each lifecycle state (Emerging, Strengthening, Dominant, Weakening, Dormant, Dead) with a canonical ID, a formal transition trigger, and a qualitative descriptor — never a numeric threshold.

### CR-4: Signal Sensor Relationship Declaration

THE Narrative Framework SHALL declare that signals are sensors that detect narrative-level effects (evidence of propagation), not causes of narrative transitions. Narrative lifecycle transitions are caused by State_Changes, not by signals.

### CR-5: Explanation Readiness Contract

THE Narrative Framework SHALL define how narratives participate in the 6-level explanation chain (Level 4: "Because of which narratives?"), including what information is provided at that level and how it connects to Level 3 (State_Changes) and Level 5 (Expansion paths).

### CR-6: Cross-Reference Convention Adoption

THE Narrative Framework SHALL use the cross-reference convention `(See: [Deliverable_Name], Section: [Section_Title])` for all references to Market Organism deliverables and other canonical frameworks.

### CR-7: Exclusion Constraints Section

THE Narrative Framework SHALL include a consolidated exclusion constraints section prohibiting engines, code, scores, weights, probabilities, dashboards, asset lists as root entities, and correlation matrices — consistent with Market Organism Layer 0 exclusion patterns.

### CR-8: Extension Criteria Definition

THE Narrative Framework SHALL define the criteria a new narrative must satisfy for inclusion in the canonical registry: (a) it represents a distinct, shared market belief structure, (b) it is falsifiable, (c) it connects at least one State_Change to at least one System, (d) it is assigned a canonical `narrative.*` ID.

### CR-9: Dependency_Type Integration

THE Narrative Framework SHALL explicitly cross-reference `dep.narrative` from Dependency_Types_v2, distinguishing the Narrative dependency mechanism (how belief propagates) from Narrative-as-Container (what the belief IS).

### CR-10: Feedback Loop Integration

THE Narrative Framework SHALL describe how narratives participate in Feedback_Loops within the non-DAG Organism_Graph, providing at least one concrete example of narrative-driven circular causation.

### CR-11: Architectural Compatibility

THE Narrative Framework SHALL declare compatibility with: 12-domain model (unchanged), canonical chain (unchanged), runtime state model (unchanged), Signal_Bubble_v0 (preserved as sensors), Signal Reusability (Intelligence_Objects preserved), and Signal_Lifecycle_Definition (gate preserved).

---

## 9. Verification Gate Proposal

| Gate ID | Gate Name | Checks |
|---------|-----------|--------|
| VG-1 | Structural Completeness | All required sections present, YAML metadata valid, exclusion constraints section exists |
| VG-2 | Cross-Reference Correctness | All `(See: ...)` references point to existing sections in existing documents |
| VG-3 | Primitive Responsibility Preservation | Narrative remains container (not cause, not sensor, not endpoint); State_Change remains root |
| VG-4 | No Future-Leak Scan | Zero numeric scores, weights, probabilities, or optimization logic anywhere in the document |
| VG-5 | Rendering Independence | All narrative identities use `narrative.*` canonical IDs; no display text as primary identity |
| VG-6 | Explanation Readiness | Narrative Level 4 explanation contract is complete and connects to Level 3 and Level 5 |
| VG-7 | Market Organism Layer 0 Compatibility | All 6 principles satisfied; root node invariant preserved; taxonomy-before-assets preserved; non-DAG mandate respected |
| VG-8 | Signal Sensor Relationship | Signals explicitly declared as sensors; no signal given causal authority over narrative transitions |

---

## 10. Risks and Blockers

### HIGH Risk

| Risk | Description | Mitigation |
|------|-------------|-----------|
| "strength-weighted" language | Current Rule 4 uses scoring-adjacent language that could seed numeric weight expectations in P0 implementation | Must be replaced with qualitative-only terminology in alignment spec |
| Display text as identity | Current framework uses "AI Infrastructure" as both name and identity; breaking change if P0 builds on this | Canonical ID migration must happen BEFORE P0 begins |

### MEDIUM Risk

| Risk | Description | Mitigation |
|------|-------------|-----------|
| Narrative "velocity" property | Not in Temporal_Taxonomy; could create parallel temporal system | Explicitly declare as narrative-specific observation property, NOT a temporal taxonomy extension |
| Lifecycle transition triggers | Currently described in prose; could be interpreted differently by different consumers | Formalize with canonical IDs and explicit transition conditions |
| Dual-use confusion (`dep.narrative` vs Narrative Container) | Developers may conflate the propagation mechanism with the structural container | Explicit disambiguation section with examples |

### LOW Risk

| Risk | Description | Mitigation |
|------|-------------|-----------|
| Hierarchy depth undefined | "Unlimited but practically 2-3 levels" is informal | Define maximum depth or declare formally unbounded with practical guidance |
| Narrative death vs dormancy boundary | "Dormant" vs "Dead" distinction is subtle | Formalize with explicit transition trigger |
| Future namespace collisions | `narrative.*` namespace established but not collision-protected | Define reservation rules and naming convention |

### Blockers

None identified. The alignment spec can proceed immediately.

---

## 11. Final Recommendation

**PROCEED** — Create the actual spec files:
- `.kiro/specs/narrative-framework-alignment/requirements.md`
- `.kiro/specs/narrative-framework-alignment/design.md`
- `.kiro/specs/narrative-framework-alignment/tasks.md`

**Rationale**:
1. The existing Narrative Framework is ontologically sound — it correctly positions Narrative as the explanatory container
2. The gaps are primarily formalization issues (IDs, metadata, cross-references), not structural rewrites
3. The "strength-weighted" language is the only architectural risk and is easily resolved
4. No blockers exist — all prerequisite frameworks are complete and canonical
5. P0 (Asset-to-Narrative Registry) cannot proceed without this alignment — it needs canonical IDs and formal lifecycle contracts

**Recommended spec approach**: Requirements-First workflow (business requirements drive the formalization; technical design follows from gaps identified in this preflight)

**Estimated scope**: SMALL-MEDIUM — primarily document formalization, no engine work, no code

---

## Appendix: Preflight Compliance Checklist

| Requirement | Status |
|-------------|--------|
| Preflight report created | ✅ |
| All relevant canonical sources inspected (16 documents) | ✅ |
| Alignment risks documented | ✅ |
| Proposed spec boundary documented | ✅ |
| Candidate requirements proposed (11) | ✅ |
| Candidate verification gates proposed (8) | ✅ |
| No canonical SSOT mutated | ✅ |
| No implementation work performed | ✅ |
| No engines, code, scores, probabilities, dashboards | ✅ |
| All new terms glossary-first | ✅ (no new terms introduced) |
| Cross-reference convention used where applicable | ✅ |
| Ambiguities flagged (not resolved silently) | ✅ |
