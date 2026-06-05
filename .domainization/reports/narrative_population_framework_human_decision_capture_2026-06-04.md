# Narrative Population Framework — Human Decision Capture Report

**Date**: 2026-06-04
**Branch**: `spec/narrative-population-framework`
**Type**: Human decision capture / design approval patch
**Authority**: Portfolio Architect (CTO)
**Status**: COMPLETE — Decisions 1-6 resolved; Decision 7 partially resolved

---

## Files Modified / Created

| File | Change |
|------|--------|
| `.kiro/specs/narrative-population-framework/design.md` | Updated Components and Interfaces, Wave 1 Decision Model, Open Human Decisions; added Human Decisions Captured section |
| `.domainization/reports/narrative_population_framework_human_decision_capture_2026-06-04.md` | Created (this report) |

---

## Human Decisions Captured

| # | Decision | Resolution | Status |
|---|----------|-----------|--------|
| 1 | Wave 1 size | 3 narratives | ✅ RESOLVED |
| 2 | Wave 1 candidate inclusion set | AI Infrastructure, Defense Rearmament, GLP-1 / Obesity Medicine | ✅ RESOLVED |
| 3 | AI Infrastructure vs AI Semiconductors boundary | AI Semi excluded; future sub-narrative evaluation | ✅ RESOLVED |
| 4 | Energy Infrastructure overlap boundary | Deferred to needs_refinement/backlog; no merge with AI Infra | ✅ RESOLVED |
| 5 | Lifecycle approach | All `narrative.lifecycle.emerging` with lifecycle history note | ✅ RESOLVED |
| 6 | Candidate ID naming approval | 3 IDs approved for task planning (proposed until mutation) | ✅ RESOLVED |
| 7 | Falsification condition approval | Drafts may be prepared; final approval before mutation | ⚠️ PARTIALLY RESOLVED |

---

## Wave 1 Final Planning Set

| # | Candidate | Proposed ID | Status |
|---|-----------|-------------|--------|
| 1 | AI Infrastructure | `narrative.ai_infrastructure` | Approved for task planning — proposed until registration |
| 2 | Defense Rearmament | `narrative.defense_rearmament` | Approved for task planning — proposed until registration |
| 3 | GLP-1 / Obesity Medicine | `narrative.glp1_obesity_medicine` | Approved for task planning — proposed until registration |

---

## Candidates Explicitly Excluded from Wave 1

| # | Candidate | Disposition | Future Path |
|---|-----------|-------------|-------------|
| 1 | Energy Infrastructure / Grid Expansion | needs_refinement/backlog | Re-evaluate after AI Infrastructure registered |
| 2 | Cybersecurity / Security Infrastructure | Backlog — later wave | Future wave consideration |
| 3 | AI Semiconductors | Needs refinement — NOT Wave 1 | Possible future sub-narrative under AI Infrastructure |
| 4 | Cloud AI | Needs refinement | Possible reclassification as `system.cloud_compute` |
| 5 | Maritime / Logistics | Needs refinement | Scope narrowing required |
| 6 | Consumer Re-acceleration | Needs refinement | Birth trigger identification needed |
| 7 | Payments / Money Rails | Backlog | Insufficient evidence |
| 8 | Space Economy / Private Space Infrastructure | Backlog | Premature |
| 9 | Humanoid Robotics / Physical AI | Backlog | Too early |
| 10 | WM / QSR / Delivery | REJECTED | Portfolio category — not narrative-shaped |
| 11 | Enterprise Software | REJECTED | Sector label — not narrative-shaped |

---

## Remaining Unresolved Item

**Decision 7 — Falsification Condition Approval**:
- Candidate-specific falsification conditions are NOT finalized
- `tasks.md` may prepare falsification DRAFTS for the 3 approved candidates
- Final human approval of each falsification condition is **required before any registry mutation**

This is the ONLY item blocking registry mutation. All other Wave 1 decisions are resolved.

---

## Confirmations

| Check | Status |
|-------|--------|
| No registry mutation occurred | ✅ `narratives: []` still empty |
| No narrative entries added | ✅ |
| No asset mappings created | ✅ |
| No facts/signals/evidence objects created | ✅ |
| No implementation work performed | ✅ |
| No tasks.md created | ✅ |
| No SSOT mutations (Narrative Framework, Market Evidence, Market Organism Layer 0) | ✅ |
| All candidate IDs remain proposed (not canonical) | ✅ |

---

## Recommendation

**Design is ready for `tasks.md` creation.** The following conditions are met:

- Wave 1 size approved (3)
- Wave 1 candidate set approved (AI Infrastructure, Defense Rearmament, GLP-1)
- Candidate IDs approved for task planning
- Lifecycle approach resolved
- Boundary decisions resolved (AI Semi, Energy)

The `tasks.md` may be created to:
1. Populate candidate field templates for the 3 approved candidates
2. Document evidence justification per candidate
3. Prepare falsification condition DRAFTS (for human review)
4. Define pre-mutation verification gate execution
5. Define registry append operation (blocked until falsification approval)
6. Define post-mutation verification

**Registry mutation remains blocked until Decision 7 (falsification approval) is finalized.**

---

*Report generated: 2026-06-04*
*Authority: ARCH*
