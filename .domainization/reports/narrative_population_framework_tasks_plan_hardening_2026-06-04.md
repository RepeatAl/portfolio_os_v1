# Narrative Population Framework — Tasks Plan Hardening Report

**Date**: 2026-06-04
**Branch**: `spec/narrative-population-framework`
**Type**: Task plan hardening patch (pre-execution audit)
**Status**: COMPLETE

---

## Files Modified

| File | Changes |
|------|---------|
| `.kiro/specs/narrative-population-framework/tasks.md` | 4 corrections applied |
| `.domainization/reports/narrative_population_framework_tasks_plan_2026-06-04.md` | Task count + excluded-candidate wording |

---

## Corrections Applied

### 1. Task Count Correction

**Before**: "Total: 8 waves, 28 tasks"
**After**: "Total: 8 execution waves, 31 subtasks"

Breakdown: Wave 0 (3) + Wave 1 (5) + Wave 2 (5) + Wave 3 (3) + Wave 4 (5) + Wave 5 (4) + Wave 6 (3) + Wave 7 (3) = 31

### 2. Excluded-Candidate Reference Rule Clarification

**Before**: "No excluded candidate may receive a registry entry, candidate template, evidence justification, or mutation step."
**After**: "No excluded candidate may receive a registry entry, candidate template, evidence justification, or mutation step. Excluded candidates may be referenced only in exclusion lists, guardrails, verification checks, and blocker reports."

Rationale: Verification gates and guardrails must name excluded candidates to check they are absent. The prohibition applies to preparation/population, not to referencing in guard rules.

### 3. Invalid Rule Reference Correction

**Before**: Task 0.2 referenced `Global Execution Rules 17`
**After**: Task 0.2 references `Global Execution Rule 15 / workflow governance`

Rationale: Only 15 Global Execution Rules exist in the plan. Rule 17 does not exist.

### 4. Explicit Stop Boundary Before Wave 5

Added `## Execution Stop Boundaries` section with table defining:
- Waves 0-2: prepare freely (no mutation risk)
- Wave 3: STOP if human falsification approval missing
- Before Wave 5: STOP if VG gates not all PASS or approval absent
- Wave 5: STOP and blocker report if any precondition fails

Hard rule added: "If human falsification approval is absent at Wave 3, execution MUST stop. It MUST NOT auto-proceed to Waves 4-7."

---

## Confirmations

| Check | Status |
|-------|--------|
| No task execution occurred | ✅ |
| No registry mutation occurred | ✅ `narratives: []` remains empty |
| No narrative entries added | ✅ |
| No asset mappings created | ✅ |
| No facts/signals/evidence objects created | ✅ |
| No implementation work performed | ✅ |
| No SSOT mutations | ✅ |
| No execution reports for Waves 0-7 created | ✅ |

---

## Recommendation

**Task plan is ready for controlled execution** after this hardening patch. Waves 0-2 may execute immediately (preparation only). Wave 3 will stop for human input. Waves 4-7 are structurally blocked until approval is confirmed.

---

*Report generated: 2026-06-04*
*Authority: ARCH*
