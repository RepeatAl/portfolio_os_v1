# Narrative Population Framework — Falsification Condition Hardening Report

**Date**: 2026-06-04
**Branch**: `spec/narrative-population-framework`
**Type**: Falsification condition hardening (pre-approval revision)
**Status**: COMPLETE — conditions hardened, still PENDING HUMAN APPROVAL

---

## Files Modified

| File | Change |
|------|--------|
| `.domainization/reports/narrative_population_framework_falsification_drafts_for_review.md` | Replaced all 3 conditions with hardened versions |
| `.domainization/reports/narrative_population_framework_falsification_approval_blocker.md` | Updated condition summaries to reflect hardened v2 |

---

## Previous Condition Summary

| Candidate | Previous Logic | Previous Condition |
|-----------|---------------|-------------------|
| AI Infrastructure | AND (2 conditions) | Capex guidance reduced >30% YoY AND construction starts decline >40% within 12 months |
| Defense Rearmament | AND (2 conditions) | NATO formally reverses 3% GDP commitment AND major conflict de-escalation |
| GLP-1 / Obesity Medicine | OR (2 conditions) | FDA safety action OR clinical evidence shows failure |

---

## Revised Condition Summary

| Candidate | Revised Logic | Revised Condition |
|-----------|--------------|-------------------|
| AI Infrastructure | TWO-OF-FOUR | (1) Capex guidance reduced >30% YoY, (2) Construction starts decline >40% YoY, (3) Order backlog/lead-time normalization, (4) Explicit overcapacity statements — any 2 within 12 months |
| Defense Rearmament | BOTH | (1) NATO/allied spending commitments formally reduced/delayed/deprioritized, (2) Actual procurement indicators weaken materially for 12+ months — must distinguish political noise from procurement-cycle reversal |
| GLP-1 / Obesity Medicine | ANY-OF-THREE | (1) Major regulator restricts GLP-1 usage for safety, (2) Long-term clinical evidence shows efficacy/safety failure, (3) Payor/reimbursement restrictions materially reduce addressable adoption — falsifies investable narrative, not science alone |

---

## Rationale for Each Revision

### AI Infrastructure

**Before**: Single AND gate with 2 conditions — vulnerable to false non-falsification if one metric is noisy.
**After**: TWO-OF-FOUR gate — requires convergence of multiple independent indicators. Adds demand normalization and explicit corporate statements as additional falsification paths. Prevents single-metric dependency.

### Defense Rearmament

**Before**: Single numeric NATO target + vague "conflict de-escalation".
**After**: Broadened to "NATO/allied spending cohort" rather than single target. Added 12-month observation requirement for procurement indicators. Explicitly requires distinguishing political noise from actual procurement reversal.

### GLP-1 / Obesity Medicine

**Before**: Binary OR between regulatory action and clinical failure.
**After**: Expanded to THREE independent failure paths including payor/adoption failure. Recognizes that a narrative can die from market access barriers even if science remains valid. Explicitly notes this falsifies the investable narrative, not the underlying science.

---

## Confirmations

| Check | Status |
|-------|--------|
| All 3 conditions remain PENDING HUMAN APPROVAL | ✅ |
| Wave 4 remains blocked | ✅ |
| Wave 5 registry append remains blocked | ✅ |
| No approval has been granted | ✅ |
| No registry mutation occurred | ✅ `narratives: []` empty |
| No narrative entries added | ✅ |
| No asset mappings created | ✅ |
| No facts/signals/evidence objects created | ✅ |
| No implementation work performed | ✅ |

---

## Recommendation

**Conditions are ready for human approval review.** The hardened falsification conditions are more robust, multi-dimensional, and resistant to false signals. Human may now:

1. Approve all 3 conditions as written → execution resumes at Wave 4
2. Request further revision → another hardening patch
3. Partially approve → execution blocked until all 3 approved

---

*Report generated: 2026-06-04*
*Authority: ARCH*
