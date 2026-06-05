# Narrative Population Framework — Wave 1: Candidate Field Preparation

**Date**: 2026-06-04
**Spec**: narrative-population-framework
**Tasks**: 1.1, 1.2, 1.3, 1.4
**Status**: COMPLETE — All 3 candidate field templates documented

---

## Important Governance Notes

- All candidate IDs are **PROPOSED** — no registry mutation has occurred
- All falsification conditions are **DRAFT — PENDING HUMAN APPROVAL**
- Templates are documented in this report ONLY — NOT written to `narrative_registry.yaml`
- Registry remains empty: `narratives: []`

---

## Candidate 1: AI Infrastructure

**Task**: 1.1

| Field | Value |
|-------|-------|
| candidate_label | AI Infrastructure |
| proposed_narrative_id | `narrative.ai_infrastructure` |
| display_name | AI Infrastructure |
| scope_definition | The structural belief that artificial intelligence adoption requires massive, sustained infrastructure investment (compute, data centers, networking, semiconductors) creating a multi-year capital expenditure supercycle across hyperscalers and their supply chains. |
| birth_trigger | `sc.narrative.ai` — ChatGPT launch (November 2022) and subsequent LLM scaling revolution triggering widespread infrastructure belief |
| connected_systems | `[system.semiconductor_manufacturing, system.data_center_infrastructure, system.cloud_computing]` |
| falsification_condition | **DRAFT — PENDING HUMAN APPROVAL**: "Hyperscaler collective capex guidance reduced >30% YoY AND data center construction starts decline >40% within 12 months" |
| lifecycle_state | `narrative.lifecycle.emerging` |
| lifecycle_history_note | Registered as initial canonical state despite existing market maturity; lifecycle history predates registry. |
| registered_date_policy | Set at registry mutation time (Wave 5) |
| registered_by_policy | Set at registry mutation time (Wave 5) — Portfolio Architect |
| last_modified_policy | Set at registry mutation time (Wave 5) |
| evidence_summary | Hyperscaler capex announcements (MSFT $50B+, GOOG $30B+, META $35B+, AMZN $75B+), ChatGPT launch Nov 2022, LLM scaling breakthroughs, data center construction surge |
| contradiction_review | Potential capex slowdown signals if AI ROI disappoints; bubble/overinvestment concerns |
| credit_solvency_relevance | Not applicable — macro-thematic narrative |
| valuation_trap_guard_status | CLEAR |
| human_approval_status | PENDING (falsification condition requires human approval) |

---

## Candidate 2: Defense Rearmament

**Task**: 1.2

| Field | Value |
|-------|-------|
| candidate_label | Defense Rearmament |
| proposed_narrative_id | `narrative.defense_rearmament` |
| display_name | Defense Rearmament |
| scope_definition | The structural belief that geopolitical conflict (primarily Russia-Ukraine, broader great power competition) has triggered a sustained, multi-decade rearmament cycle across NATO and allied nations, requiring fundamental increases in defense industrial capacity and government procurement. |
| birth_trigger | `sc.events.wars` — Russia-Ukraine conflict (February 2022) triggering structural defense spending belief and NATO rearmament commitment |
| connected_systems | `[system.defense_industrial_base, system.government_procurement]` |
| falsification_condition | **DRAFT — PENDING HUMAN APPROVAL**: "NATO formally reverses 3% GDP commitment AND major conflict de-escalation removes structural rearmament rationale" |
| lifecycle_state | `narrative.lifecycle.emerging` |
| lifecycle_history_note | Registered as initial canonical state despite existing market maturity; lifecycle history predates registry. |
| registered_date_policy | Set at registry mutation time (Wave 5) |
| registered_by_policy | Set at registry mutation time (Wave 5) — Portfolio Architect |
| last_modified_policy | Set at registry mutation time (Wave 5) |
| evidence_summary | NATO 3% GDP commitment, Germany €100B special fund, EU defense spending packages, Ukraine conflict duration, defense order backlog growth |
| contradiction_review | Ceasefire/peace scenarios reducing urgency; budget constraints competing with defense spending |
| credit_solvency_relevance | Not applicable — geopolitical macro-thematic narrative |
| valuation_trap_guard_status | CLEAR |
| human_approval_status | PENDING (falsification condition requires human approval) |

---

## Candidate 3: GLP-1 / Obesity Medicine

**Task**: 1.3

| Field | Value |
|-------|-------|
| candidate_label | GLP-1 / Obesity Medicine |
| proposed_narrative_id | `narrative.glp1_obesity_medicine` |
| display_name | GLP-1 / Obesity Medicine |
| scope_definition | The structural belief that GLP-1 receptor agonist breakthroughs have initiated a fundamental transformation of obesity medicine, creating a new pharmaceutical category with massive total addressable market expansion and reshaping healthcare delivery for metabolic disease. |
| birth_trigger | `sc.corporate.guidance` — Novo Nordisk/Lilly clinical breakthrough + FDA approvals (Wegovy 2021, Mounjaro 2022, Zepbound 2023) triggering obesity medicine transformation belief |
| connected_systems | `[system.pharmaceutical_manufacturing, system.healthcare_delivery]` |
| falsification_condition | **DRAFT — PENDING HUMAN APPROVAL**: "FDA safety action materially restricts GLP-1 usage OR clinical evidence shows long-term efficacy/safety failure" |
| lifecycle_state | `narrative.lifecycle.emerging` |
| lifecycle_history_note | Registered as initial canonical state despite existing market maturity; lifecycle history predates registry. |
| registered_date_policy | Set at registry mutation time (Wave 5) |
| registered_by_policy | Set at registry mutation time (Wave 5) — Portfolio Architect |
| last_modified_policy | Set at registry mutation time (Wave 5) |
| evidence_summary | Ozempic/Wegovy FDA approvals, Mounjaro/Zepbound approvals, STEP trials, SURMOUNT trials, prescription volume surge, Novo/Lilly revenue acceleration from GLP-1 segment |
| contradiction_review | Safety signal emergence, insurance coverage pushback, supply constraints limiting adoption |
| credit_solvency_relevance | Not applicable — scientific breakthrough narrative, not valuation-driven |
| valuation_trap_guard_status | CLEAR |
| human_approval_status | PENDING (falsification condition requires human approval) |

---

## Verification Checklist

| Check | Result |
|-------|--------|
| All 3 candidates documented | ✅ |
| All falsification conditions marked DRAFT / PENDING HUMAN APPROVAL | ✅ |
| No registry mutation occurred | ✅ — `narratives: []` remains empty |
| No excluded candidates prepared | ✅ |
| All IDs marked PROPOSED | ✅ |
| No `fact.*`, `signal.*`, or `evidence.*` objects created | ✅ |
| credit_solvency_relevance: "Not applicable" for all 3 | ✅ |
| valuation_trap_guard_status: CLEAR for all 3 | ✅ |

---

## Next Steps

Wave 2: Evidence Justification Preparation — write evidence summaries for each candidate (report only, no evidence objects).
