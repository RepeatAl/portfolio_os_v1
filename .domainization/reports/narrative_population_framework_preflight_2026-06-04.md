# Narrative Population Framework — Preflight Report

**Spec**: `narrative-population-framework`
**Date**: 2026-06-04
**Branch**: `spec/narrative-population-framework`
**Type**: Preflight reconnaissance / candidate assessment / governance boundary definition
**Status**: PREFLIGHT ONLY — No registry mutation authorized

---

## 1. Executive Summary

### Readiness

The system is **structurally ready** for controlled narrative population. The Narrative Registry schema, governance procedures, and artifact integration are all canonical on main. The governance model defines clear creation procedures, collision checks, inclusion criteria gates, and lifecycle transition rules. All prerequisite canonical documents are present and aligned.

### Primary Risk

**Portfolio-category-as-narrative contamination.** The candidate list includes areas that may be portfolio basket designs (asset groupings) rather than genuine narrative containers (shared belief structures with identifiable State_Change origins). The boundary between "investment theme" and "canonical narrative" requires explicit human judgment for each candidate.

### Recommendation

**PROCEED** to requirements phase with the following conditions:
1. Human must approve each candidate's narrative-shaped status individually
2. First population wave must be small (3-5 narratives maximum) to validate the governance pipeline
3. Candidates that fail the inclusion criteria gate must be routed to backlog, not forced into the registry
4. No candidate ID may be finalized without explicit human approval

---

## 2. Source Inventory

### Documents Read

| # | Document | Path | Authority Level |
|---|----------|------|-----------------|
| 1 | Narrative Registry (schema-only) | `docs/registries/narrative_registry.yaml` | SSOT (draft) |
| 2 | Registry Governance README | `docs/registries/README_narrative_registry_governance.md` | Governance guide |
| 3 | Narrative Registry Framework — Requirements | `.kiro/specs/narrative-registry-framework/requirements.md` | Spec (canonical) |
| 4 | Narrative Registry Framework — Design | `.kiro/specs/narrative-registry-framework/design.md` | Spec (canonical) |
| 5 | Narrative Registry Framework — Tasks | `.kiro/specs/narrative-registry-framework/tasks.md` | Spec (canonical) |
| 6 | Narrative Registry Framework — Completion Report | `.domainization/reports/narrative_registry_framework_completion_report_2026-06-03.md` | Execution evidence |
| 7 | Narrative Registry Framework — Verification Gate Report | `.domainization/reports/narrative_registry_framework_verification_gate_report.md` | Verification evidence |
| 8 | Narrative Framework v2 | `docs/README_narrative_framework.md` | SSOT (canonical) — ontology |
| 9 | Market Organism Principles | `docs/market_organism/README_market_organism_principles.md` | SSOT (canonical) |
| 10 | State_Change Taxonomy | `docs/market_organism/README_state_change_taxonomy.md` | SSOT (canonical) |
| 11 | Expansion Taxonomy | `docs/market_organism/README_expansion_taxonomy.md` | SSOT (canonical) |

### Canonical Authority Hierarchy

```
Market Organism Principles (Layer 0 — natural laws)
  └── Narrative Framework v2 (SSOT — ontology: WHAT a narrative IS)
        └── Narrative Registry (SSOT — governance: HOW narratives are registered)
              └── Narrative Population Framework (THIS SPEC — WHICH narratives exist)
                    └── Future: Asset-to-Narrative Registry (WHICH assets belong to WHICH narratives)
```

### Missing or Ambiguous Sources

| # | Gap | Impact | Resolution |
|---|-----|--------|------------|
| 1 | No canonical `system.*` registry exists | Cannot validate `connected_systems` references against a registry | Accept on trust per Design Decision D-5; validate in future System Registry spec |
| 2 | Post-merge health check report not found at expected path | Minor — completion report and VG report provide equivalent evidence | Proceed without blocking |
| 3 | No explicit list of all valid `system.*` IDs | Connected systems assessment is based on illustrative examples in Expansion Taxonomy | Flag for human review per candidate |

---

## 3. Boundary Definition

### What Narrative Population IS

- The first authorized addition of actual `narrative.*` entries to the `narratives: []` list in `docs/registries/narrative_registry.yaml`
- Controlled registration of candidates that satisfy ALL 4 inclusion criteria from Narrative Framework v2 Section 13
- Human-authorized, evidence-backed, governance-compliant population
- Each entry must have: `narrative_id`, `scope_definition`, `birth_trigger`, `connected_systems`, `falsification_condition`, `lifecycle_state`, `registered_date`, `registered_by`, `last_modified`

### What Narrative Population is NOT

- It is NOT portfolio basket design (grouping assets by investment theme)
- It is NOT scoring or ranking narratives (no numeric weights, no priority ordering)
- It is NOT creating asset-to-narrative mappings (which assets belong to which narratives)
- It is NOT building engines or runtime code
- It is NOT modifying the Narrative Framework v2 ontology
- It is NOT modifying Market Organism Layer 0 SSOTs
- It is NOT adding validation scripts, dashboards, or automated tooling

### How It Differs from Narrative Registry Framework

| Aspect | Narrative Registry Framework (DONE) | Narrative Population Framework (THIS) |
|--------|--------------------------------------|---------------------------------------|
| Purpose | Define schema + governance | Apply governance to register actual narratives |
| Output | Empty registry with rules | Populated registry with entries |
| `narratives: []` | Must remain empty | May contain entries (first time) |
| Authority needed | ARCH + GOV for schema | ARCH for proposals, GOV for review per entry |
| Risk | Schema incompleteness | Wrong entries, duplicates, asset-list-first contamination |

### How It Differs from Asset-to-Narrative Registry

| Aspect | Narrative Population | Asset-to-Narrative Registry (FUTURE) |
|--------|---------------------|--------------------------------------|
| Question | "Which narratives exist?" | "Which assets belong to which narratives?" |
| Contains | Narrative definitions | Asset-narrative membership records |
| Fields | scope, birth_trigger, systems | asset_id, narrative_id, membership_type, influence |
| Registry | `narrative_registry.yaml` | Future separate registry file |
| Boundary | Defines narrative containers | Maps assets INTO containers |

### How It Differs from Portfolio Category Design

| Aspect | Narrative (canonical) | Portfolio Category (NOT canonical) |
|--------|----------------------|-----------------------------------|
| Origin | State_Change creates it | Human analyst groups assets |
| Structure | Shared market belief | Investment convenience grouping |
| Falsifiable | YES — contradicting State_Change can kill it | NO — categories don't die from evidence |
| Lifecycle | Emerges → Strengthens → Dominant → Weakens → Dormant/Dead | Static unless manually reorganized |
| Identity | `narrative.*` canonical ID | Not in canonical namespace |
| Causal chain | `sc.* → narrative.* → system.* → asset` | Asset grouping without causal grounding |

---

## 4. Candidate Evaluation Model

### Assessment Criteria (derived from Narrative Framework v2 Section 13 + Registry Governance)

Every candidate must be evaluated against ALL of the following criteria. Failure on ANY criterion disqualifies for Wave 1 registration.

| # | Criterion | Source | Verification Method |
|---|-----------|--------|---------------------|
| 1 | **Distinct shared belief** | Inclusion Criterion 1 | Is this a genuine shared market belief held by multiple participants? Or is it an analyst label? |
| 2 | **Falsifiable** | Inclusion Criterion 2 | Can you state what contradicting evidence would kill this narrative? Is the condition concrete and testable? |
| 3 | **Connected to State_Change** | Inclusion Criterion 3 | Can you identify a specific `sc.*` birth trigger? A real, identifiable market event — not hypothetical? |
| 4 | **Connected to at least one System** | Inclusion Criterion 3 | Can you identify at least one `system.*` affected functional domain? |
| 5 | **Not asset-list-first** | EC-4, Principle 2 | Did you derive this from a belief structure, or did you start with a basket of assets and label them? |
| 6 | **Not duplicate** | Collision Check | Does this overlap semantically with any other candidate or existing Framework v2 example? |
| 7 | **Not scoring/ranking/probability-based** | EC-2, NRF-REQ-9 | Does the candidate definition avoid numeric strength, probability, or ranking language? |
| 8 | **Evidence available** | Registry Governance Step 3 | Is there a real, identifiable, past-tense State_Change that birthed this narrative? |
| 9 | **Lifecycle initially emerging** | NRF-REQ-6 | Can you justify lifecycle state = `narrative.lifecycle.emerging` or is it already dominant/weakening? |

---

## 5. Candidate Narrative Assessment Matrix

**Legend:**
- ✅ Likely narrative-shaped
- ⚠️ Needs refinement (ambiguity or scope risk)
- ❌ Likely NOT narrative-shaped (portfolio category risk)

| # | Candidate Area | Narrative-Shaped? | Likely Birth Trigger Type | Likely Connected Systems | Distinctness Risk | Evidence Readiness | Scope Risk | Recommendation |
|---|---------------|-------------------|---------------------------|--------------------------|-------------------|--------------------|------------|----------------|
| 1 | AI Infrastructure | ✅ | `sc.corporate.capex` (hyperscaler capex announcements) | system.semiconductor_manufacturing, system.data_center_infrastructure | LOW — clearly distinct from other candidates | HIGH — multiple concrete capex announcements exist | LOW — well-bounded belief about infrastructure buildout | **Wave 1** |
| 2 | AI Semiconductors | ⚠️ | `sc.corporate.earnings` (Nvidia revenue beats) | system.semiconductor_manufacturing | HIGH — overlaps significantly with AI Infrastructure | HIGH — Nvidia earnings are documented events | HIGH — may be a sub-narrative of AI Infrastructure, not independent | **Needs refinement** — clarify boundary vs. AI Infrastructure |
| 3 | Cloud AI | ⚠️ | `sc.narrative.ai` (AI capability demonstration shifts) | system.cloud_computing | MEDIUM — overlaps with AI Infrastructure on the compute side | MEDIUM — less discrete than capex events | HIGH — may be subsection of AI Infrastructure or a System, not a separate narrative | **Needs refinement** — may be a system (`system.cloud_ai`) rather than a narrative |
| 4 | Defense Rearmament | ✅ | `sc.narrative.defense` (NATO spending commitments, geopolitical escalation) | system.defense_industrial_base, system.government_procurement | LOW — clearly distinct from all other candidates | HIGH — NATO 3% GDP commitment, Ukraine conflict are concrete events | LOW — focused on structural spending increase belief | **Wave 1** |
| 5 | Energy Infrastructure / Grid Expansion | ✅ | `sc.narrative.energy` (grid strain from AI + electrification demand) | system.power_generation, system.grid_infrastructure | MEDIUM — partial overlap with AI Infrastructure at the power demand layer | MEDIUM — multiple data center power strain reports exist, but trigger is diffuse | MEDIUM — risk of being "everything about energy" rather than a specific belief | **Wave 1** (with scope narrowing) |
| 6 | Cybersecurity / Security Infrastructure | ✅ | `sc.narrative.security` (major nation-state cyberattacks) | system.enterprise_security, system.critical_infrastructure_protection | LOW — clearly distinct | HIGH — specific attack events documented | LOW — focused on belief that security spending must increase structurally | **Wave 1** |
| 7 | GLP-1 / Obesity Medicine | ✅ | `sc.corporate.earnings` (Novo Nordisk/Lilly GLP-1 revenue acceleration) | system.pharmaceutical_manufacturing, system.healthcare_delivery | LOW — no overlap with other candidates | HIGH — earnings results and FDA approvals are discrete events | LOW — belief that obesity medicine transforms healthcare economics | **Wave 1** |
| 8 | WM / QSR / Delivery | ❌ | Unclear — no single identifiable State_Change | Unclear — multiple unrelated systems | HIGH — this looks like a portfolio basket of consumer stocks | LOW — no clear triggering event | HIGH — mixing Walmart, quick-service restaurants, and delivery into one container is asset-list-first | **Reject** — not narrative-shaped; appears to be portfolio category |
| 9 | Payments / Money Rails | ⚠️ | `sc.narrative.ai` or `sc.corporate.earnings` (payment volume structural growth) | system.financial_infrastructure | MEDIUM — broad scope risk | LOW — no single identifiable regime-shifting event | HIGH — "payments grow" is too broad and possibly unfalsifiable in current form | **Backlog** — needs a more specific belief structure and triggering event |
| 10 | Maritime / Logistics | ⚠️ | `sc.events.wars` (Houthi Red Sea attacks, trade route disruption) | system.global_shipping, system.supply_chain_logistics | MEDIUM — could be "supply chain disruption" not "maritime" specifically | MEDIUM — Red Sea disruption is concrete but may be temporary | MEDIUM — is this a narrative (belief about structural change) or an event response? | **Needs refinement** — narrow to a specific belief about trade route restructuring |
| 11 | Enterprise Software | ❌ | Unclear — no single identifiable State_Change | system.enterprise_it | HIGH — this is a sector label, not a shared belief | LOW — no triggering event that created a belief about enterprise software | HIGH — "enterprise software companies will do well" is not falsifiable as stated | **Reject** — sector classification, not narrative-shaped |
| 12 | Consumer Re-acceleration | ⚠️ | `sc.macro.rates` (rate cuts enabling consumer spending recovery) | system.consumer_discretionary, system.retail | MEDIUM — broad scope | LOW — the re-acceleration hasn't clearly been triggered by a single event | HIGH — very broad belief that may encompass multiple sub-beliefs | **Backlog** — needs a more specific triggering event and narrower scope |
| 13 | Space Economy / Private Space Infrastructure | ⚠️ | `sc.corporate.capex` (SpaceX/Blue Origin infrastructure investment announcements) | system.aerospace_manufacturing, system.satellite_communications | LOW — distinct from other candidates | MEDIUM — capex announcements exist but narrative adoption is limited | MEDIUM — participant count may be too low for "shared market belief" status | **Backlog** — may be premature (belief not yet broadly shared) |
| 14 | Humanoid Robotics / Physical AI | ⚠️ | `sc.narrative.robotics` (simultaneous robotics demonstrations) | system.industrial_automation, system.semiconductor_manufacturing | MEDIUM — overlaps partially with AI Infrastructure on compute demand side | MEDIUM — multiple demos exist but economic viability unproven | MEDIUM — belief may not yet be broadly shared enough for canonical status | **Backlog** — premature; revisit when participant adoption broadens |

### Summary

| Recommendation | Count | Candidates |
|----------------|-------|------------|
| **Wave 1** | 5 | AI Infrastructure, Defense Rearmament, Energy Infrastructure, Cybersecurity, GLP-1/Obesity Medicine |
| **Needs Refinement** | 4 | AI Semiconductors, Cloud AI, Maritime/Logistics, Consumer Re-acceleration |
| **Backlog** | 3 | Payments/Money Rails, Space Economy, Humanoid Robotics |
| **Reject** | 2 | WM/QSR/Delivery, Enterprise Software |

---

## 6. Proposed First Population Boundary

### Recommendation: Small Controlled Set (3-5 narratives)

**Wave 1 should contain 3-5 narratives maximum.** Not zero, not the full 14, and not candidate templates without actual entries.

### Rationale

1. **Zero would defer value indefinitely.** The governance pipeline is ready. The schema is in place. Continuing to produce empty registries produces no validation of the registration process itself.

2. **The full 14 would be reckless.** Multiple candidates fail inclusion criteria. Registering all of them would contaminate the namespace with portfolio categories masquerading as narratives.

3. **3-5 validates the pipeline.** A small Wave 1 tests the collision check procedure, the inclusion criteria gate, the GOV review process, and the lifecycle audit format — with recoverable risk if any entry proves incorrect.

### Proposed Wave 1 Candidates (subject to human approval)

| # | Candidate | Rationale for Wave 1 |
|---|-----------|---------------------|
| 1 | AI Infrastructure | Clearest narrative in the set — identifiable State_Change, broad market belief, concrete falsification |
| 2 | Defense Rearmament | Geopolitically grounded — NATO commitment is a specific regime shift, belief is falsifiable |
| 3 | GLP-1 / Obesity Medicine | Healthcare-specific — no overlap with tech narratives, clear corporate triggers |
| 4 | Cybersecurity | Security-specific — distinct from all others, identifiable trigger events |
| 5 | Energy Infrastructure | Infrastructure-adjacent — tests whether the governance pipeline can handle narratives that partially overlap with AI Infrastructure |

### Why Not More

- AI Semiconductors and Cloud AI risk being sub-narratives of AI Infrastructure (collision check would flag them)
- Maritime/Logistics and Consumer Re-acceleration need scope narrowing before registration
- Payments and Space Economy lack clear triggering events
- WM/QSR/Delivery and Enterprise Software are sector labels, not narratives

### Human Decision Required

The human must decide:
- Is 5 too many for Wave 1? (3 is also defensible)
- Should Energy Infrastructure be deferred until AI Infrastructure is registered first (to test overlap handling)?
- Should any "Needs Refinement" candidate be promoted to Wave 1 after scope narrowing?

---

## 7. Candidate Field Preparation Model

For each narrative that enters Wave 1, the following fields must be prepared BEFORE actual registration:

### Required Fields (per Registry Schema)

| # | Field | Preparation Work |
|---|-------|-----------------|
| 1 | `narrative_id` | Propose candidate token following `narrative.[lowercase_underscore_token]` rules. Human approves final ID. Once approved, IMMUTABLE. |
| 2 | `scope_definition` | Draft 1-2 sentence description of the shared market belief. Must be falsifiable, not vague. Human reviews for precision. |
| 3 | `birth_trigger` | Identify the specific `sc.*` State_Change that originated this narrative. Must reference a real, past-tense market event. |
| 4 | `connected_systems` | List at least one `system.*` ID. Accept on trust (no system registry exists yet). |
| 5 | `falsification_condition` | Draft a concrete, testable condition. "Narrative loses relevance" is INVALID. Must state specific contradicting evidence. |
| 6 | `lifecycle_state` | Always `narrative.lifecycle.emerging` for new entries. If the narrative is clearly already dominant, document why lifecycle is not already past emerging. |
| 7 | `registered_date` | Date of actual registration (set at registration time). |
| 8 | `registered_by` | `ARCH` (per governance rules). |
| 9 | `last_modified` | Same as `registered_date` initially. |

### Optional Fields Policy

| # | Field | Wave 1 Policy |
|---|-------|---------------|
| 1 | `display_name` | RECOMMENDED — provide at least `{en: "..."}`. Rendering only, not identity. |
| 2 | `parent_narrative` | Include IF a meta-narrative relationship is declared. Otherwise null. |
| 3 | `velocity` | OPTIONAL — include if human can make a qualitative assessment. |
| 4 | `expected_duration` | OPTIONAL — include if Temporal_Taxonomy duration is assessable. |
| 5 | `evidence_summary` | RECOMMENDED — human-readable justification for why this narrative qualifies. |
| 6 | `related_narratives` | Populate AFTER Wave 1 entries exist (cannot reference entries that don't exist yet). |
| 7 | `lifecycle_history` | Empty list initially — no transitions have occurred yet. |

---

## 8. Human Review Decisions Needed

The following decisions MUST be made by the human before any actual population occurs:

| # | Decision | Options | Impact |
|---|----------|---------|--------|
| 1 | Approve candidate scope definitions | Accept / Refine / Reject per candidate | Determines which entries are registered |
| 2 | Approve candidate naming (`narrative_id` tokens) | Accept / Rename per candidate | IDs are IMMUTABLE once approved — no changes after registration |
| 3 | Approve State_Change birth triggers | Accept / Identify different trigger per candidate | Must be a real, identifiable past event |
| 4 | Approve connected systems | Accept / Add / Remove per candidate | Must be at least 1 per entry |
| 5 | Approve falsification conditions | Accept / Strengthen / Rewrite per candidate | Must be concrete and testable |
| 6 | Approve Wave 1 size | 3 / 4 / 5 narratives | Determines scope of first registration batch |
| 7 | AI Infrastructure vs AI Semiconductors boundary | Single narrative / Parent-child / Independent | Determines whether collision check blocks AI Semiconductors |
| 8 | Energy Infrastructure scope | Broad / Narrow to grid/AI-power only | Determines whether overlap with AI Infrastructure is acceptable |
| 9 | Lifecycle state justification | Accept "emerging" / Document "already strengthening" | Some Wave 1 candidates may already be past emerging in reality |
| 10 | Proceed to requirements phase | Yes / Pause / Modify scope | Gates the entire spec creation |

---

## 9. Gap Matrix

| Gap ID | Source | Risk | Severity | Proposed Resolution | Phase |
|--------|--------|------|----------|--------------------|----|
| NPG-01 | No `system.*` registry to validate connected_systems | Invalid system references possible | MEDIUM | Accept on trust; validate retroactively when System Registry exists | Design |
| NPG-02 | Some candidates may already be past "emerging" lifecycle | Incorrect initial lifecycle state | MEDIUM | Document current state assessment; register at emerging with justification OR define lifecycle_history backdating policy | Requirements |
| NPG-03 | AI Infrastructure vs AI Semiconductors overlap | Collision check may flag both | HIGH | Human must decide boundary: one narrative, parent-child, or independent with scope differentiation | Requirements |
| NPG-04 | No precedent for Wave 1 — first-ever population | Process may have unforeseen issues | LOW | Start small (3-5), iterate, learn | Tasks |
| NPG-05 | Falsification conditions for infrastructure narratives may be weak | Vague falsification = unfalsifiable narrative | HIGH | Require specific quantifiable contradicting evidence (e.g., "capex guidance collectively reduced by >30% across hyperscalers") | Requirements |
| NPG-06 | Portfolio category contamination | Asset-list-first entries entering registry | HIGH | Strict inclusion criteria gate enforcement; reject candidates that cannot identify a State_Change origin | Requirements |
| NPG-07 | `birth_trigger` for older narratives may reference events pre-dating taxonomy | No canonical `sc.*` ID for historical events | MEDIUM | Allow human-assigned retrospective `sc.*` IDs with documentation that the event predates formal taxonomy | Design |
| NPG-08 | Related_narratives cannot be populated in Wave 1 | Cross-referencing requires entries to exist first | LOW | Leave empty in Wave 1; populate after all Wave 1 entries are registered | Tasks |
| NPG-09 | Velocity assessment requires human judgment | No algorithmic determination possible | LOW | Make velocity OPTIONAL for Wave 1; human may include if confident | Design |
| NPG-10 | Meta-narrative hierarchy (e.g., `narrative.ai_transformation` parent) | Cannot declare parent if parent doesn't exist in registry | MEDIUM | Either register meta-narrative first, or leave parent_narrative null in Wave 1 | Design |

---

## 10. Candidate Requirements (Draft)

These are proposed requirement IDs for the Narrative Population Framework spec. They are drafts — not finalized.

### NPF-REQ-1: Population Boundary

The population spec SHALL define exactly which candidate narratives are authorized for Wave 1 registration and SHALL explicitly exclude all others from this spec's scope.

### NPF-REQ-2: Candidate Evaluation Model

The population spec SHALL require that every candidate passes ALL 4 inclusion criteria (Narrative Framework v2 Section 13) with documented evidence before registration.

### NPF-REQ-3: Evidence Requirement

The population spec SHALL require that every birth_trigger references a real, identifiable, past-tense State_Change — not a hypothetical or projected event.

### NPF-REQ-4: No Asset-First Population

The population spec SHALL prohibit deriving narratives from asset lists, portfolio baskets, sector labels, or statistical co-movement patterns. Every narrative must be derived from a shared belief structure with a State_Change origin.

### NPF-REQ-5: Candidate Field Preparation

The population spec SHALL require complete field preparation (all 9 required fields) for every candidate BEFORE actual registry mutation. No partial entries may be registered.

### NPF-REQ-6: Human Review Gate

The population spec SHALL require explicit human approval for: (a) each candidate's scope definition, (b) each candidate's canonical ID, (c) each candidate's falsification condition, (d) the Wave 1 set composition.

### NPF-REQ-7: Registry Mutation Control

The population spec SHALL define that `docs/registries/narrative_registry.yaml` is mutated ONLY during the explicitly authorized registration task, and ONLY to append entries to the `narratives` list. No schema modification, no governance modification.

### NPF-REQ-8: Verification Before Population

The population spec SHALL include verification gates that confirm: no prohibited fields, no asset mappings, no scoring, valid `narrative.*` IDs, collision check passed, all required fields populated.

### NPF-REQ-9: Backlog Handling

The population spec SHALL define a backlog section for candidates that need refinement or are premature, with documented reasons and re-evaluation criteria.

### NPF-REQ-10: Future Asset-to-Narrative Readiness

The population spec SHALL ensure that registered narratives are compatible with future Asset-to-Narrative Registry consumption: `narrative_id` as stable foreign key, `lifecycle_state` queryable, `connected_systems` as list.

---

## 11. Verification Gate Proposal

| Gate ID | Gate Name | Checks |
|---------|-----------|--------|
| VG-POP-1 | No Preflight Registry Mutation | `narratives: []` still empty during preflight/design phase |
| VG-POP-2 | Inclusion Criteria Compliance | Every registered entry satisfies all 4 inclusion criteria with documented evidence |
| VG-POP-3 | Candidate-Only Language | All candidate references use "candidate" or "proposed" prefix until registration moment |
| VG-POP-4 | No Asset Mappings | Zero asset-to-narrative membership records anywhere in deliverables |
| VG-POP-5 | No Scoring/Ranking/Probability | Zero numeric scores, weights, probabilities, ranking logic in any deliverable |
| VG-POP-6 | State_Change Linkage Readiness | Every registered entry has a valid `sc.*` birth trigger referencing an identifiable event |
| VG-POP-7 | System Linkage Readiness | Every registered entry has at least one `system.*` in connected_systems |
| VG-POP-8 | Falsification Readiness | Every registered entry has a concrete, testable falsification condition |
| VG-POP-9 | Human Approval Readiness | Evidence that human approved each entry's scope, ID, and falsification condition |
| VG-POP-10 | Narrative Registry Compatibility | Registered entries comply with registry schema (all required fields, no prohibited fields) |
| VG-POP-11 | Collision Check | No two registered entries have overlapping scope definitions without declared parent-child relationship |
| VG-POP-12 | No SSOT Mutation | Narrative Framework v2, Market Organism Layer 0 SSOTs, central glossary unchanged |

---

## 12. Risks and Blockers

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|-----------|-----------|
| 1 | **Portfolio category mistaken for narrative** | HIGH | HIGH | Strict inclusion criteria enforcement; reject WM/QSR/Delivery and Enterprise Software |
| 2 | **Asset basket mistaken for narrative** | HIGH | MEDIUM | Every candidate must pass "Can you identify the State_Change?" test. If no, reject. |
| 3 | **Too many first-wave narratives** | MEDIUM | MEDIUM | Cap Wave 1 at 5 maximum; human must approve size |
| 4 | **Weak falsification criteria** | HIGH | MEDIUM | Require specific contradicting evidence, not vague "loses relevance" language |
| 5 | **Premature canonical IDs** | HIGH | LOW | All IDs are "candidate" until final human approval; immutability begins only after registration |
| 6 | **Insufficient State_Change evidence** | MEDIUM | MEDIUM | Birth triggers must reference concrete past events; hypothetical or projected events are invalid |
| 7 | **Duplicate or overlapping narratives** | MEDIUM | HIGH | AI Infrastructure / AI Semiconductors / Cloud AI overlap is the primary concern; collision check procedure must be applied |
| 8 | **Lifecycle state inaccuracy** | LOW | MEDIUM | Some narratives may already be Strengthening or Dominant; document assessment and register at emerging with lifecycle_history note |
| 9 | **System reference invalidity** | LOW | MEDIUM | No system registry exists; accept on trust per Design Decision D-5 |
| 10 | **Scope creep into asset-to-narrative mapping** | HIGH | LOW | Explicit prohibition in requirements; verification gate VG-POP-4 |

### Blockers

| # | Blocker | Blocking? | Resolution |
|---|---------|-----------|------------|
| 1 | Human must approve Wave 1 composition | YES — cannot proceed without | Present candidates and get explicit approval |
| 2 | AI Infrastructure vs AI Semiconductors boundary decision | YES — for both candidates | Human must decide: merge, parent-child, or independent |
| 3 | No system registry for validation | NO — accepted on trust | Document limitation; validate retroactively |

---

## 13. Final Recommendation

### Proceed to Create

Kiro should proceed to create the following spec documents:

- `.kiro/specs/narrative-population-framework/requirements.md`
- `.kiro/specs/narrative-population-framework/design.md`
- `.kiro/specs/narrative-population-framework/tasks.md`

### Conditions for Proceeding

1. Human approves the Wave 1 candidate set (or modifies it)
2. Human resolves the AI Infrastructure / AI Semiconductors boundary question
3. Human confirms that 3-5 narratives is the correct Wave 1 size
4. All candidate scope definitions are reviewed and approved before task execution
5. All candidate IDs are marked "proposed" until explicit human finalization

### Hard Constraints (carry forward to requirements)

- No registry mutation during requirements/design phase
- No actual narrative entries until explicitly authorized task
- No asset mappings
- No engines, code, runtime artifacts
- No validation scripts, dashboards, scoring, ranking, probabilities
- No SSOT mutation (Narrative Framework v2, Market Organism Layer 0, central glossary)
- All candidate IDs must be marked candidate/proposed only until registration
- All cross-references must use: `(See: [Deliverable_Name], Section: [Section_Title])`
- If ambiguity exists, flag it — do not resolve silently

---

## Cross-References

| Target Deliverable | Section Referenced | Context |
|-------------------|-------------------|---------|
| README_narrative_framework | Section 4: What Is a Narrative? | Narrative definition and ID format |
| README_narrative_framework | Section 6: Lifecycle State Machine | Valid lifecycle states |
| README_narrative_framework | Section 13: Extension Criteria | Inclusion/exclusion criteria |
| README_narrative_framework | Section 15: Exclusion Constraints | Prohibited fields |
| README_market_organism_principles | Principle 2: Taxonomy Precedes Assets | No asset-first design |
| README_state_change_taxonomy | Top-Level Categories | Birth trigger classification |
| README_state_change_taxonomy | Primary Classification Rule | Trigger disambiguation |
| README_expansion_taxonomy | Expansion Definition | System connection validation |
| README_narrative_registry_governance | Creation Procedure | Registration workflow |
| README_narrative_registry_governance | Collision Check Procedure | Overlap detection |
| narrative_registry.yaml | Governance Section | Schema constraints |

---

*Report generated: 2026-06-04*
*Preflight authority: ARCH*
*Status: Reconnaissance complete. Awaiting human approval to proceed.*
*No registry mutation performed. `narratives: []` remains empty.*
