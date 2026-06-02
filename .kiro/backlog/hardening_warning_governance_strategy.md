# Hardening: Warning Governance Strategy

**Priority:** MEDIUM  
**Category:** governance/observability  
**Owner:** CTO  
**Created:** 2026-05-27  
**Status:** OPEN  

## Problem

The test suite currently produces 280 warnings. All are DeprecationWarnings from legacy briefing files — expected and tolerated during the migration period. However, without governance:

- **Warning blindness:** Developers stop reading warnings entirely
- **Signal loss:** New, actionable warnings get buried in noise
- **Growth risk:** Warning count increases silently over time
- **No accountability:** No one owns warning reduction

## Current Warning Breakdown

| Source | Count | Type | Tolerated? |
|--------|-------|------|-----------|
| Legacy briefing deprecation | ~280 | DeprecationWarning | Yes (until Phase D sunset) |
| Other | 0 | — | — |

## Required Work

### Phase 1: Categorization (immediate)

1. Create `governance/warning_budget.yaml`:
   ```yaml
   warning_budget:
     total_max: 300
     categories:
       legacy_briefing_deprecation:
         max: 280
         tolerated_until: "2026-07-01"
         owner: "Phase D cleanup"
       unregistered_artifact:
         max: 0
         tolerated_until: null
         owner: "Registration validator"
   ```

2. Distinguish tolerated vs active warnings in test output

### Phase 2: Budget Enforcement (after Phase D)

1. Add pytest plugin or conftest.py filter for tolerated warnings
2. Fail CI if warning count exceeds budget
3. Reduce budget as legacy briefings are sunset

### Phase 3: Zero-Warning Target (post-migration)

1. All legacy briefing deprecations resolved (Phase D)
2. Warning budget reduced to 0
3. Any new warning requires explicit budget allocation

## Acceptance Criteria

- [ ] `governance/warning_budget.yaml` exists with categorized warnings
- [ ] Tolerated warnings are documented with sunset dates
- [ ] Warning count does not grow beyond current baseline (280)
- [ ] Future CI enforces warning budget (post Phase D)

## NOT Required Now

- Full warning cleanup (that's Phase D's job)
- CI enforcement (premature before Phase D)
- Suppressing warnings in test output (they serve as migration reminders)
