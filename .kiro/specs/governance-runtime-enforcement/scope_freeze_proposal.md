# Scope Freeze Proposal: governance-runtime-enforcement

**Date**: 2026-05-29
**Author**: Kiro (CTO-directed)
**Status**: APPROVED (2026-05-29)
**CTO Amendment**: Req 31 moved from FUTURE_BACKLOG to ACTIVE_SCOPE (simplified)
**Principle**: Governance protects MoneyHorst. Governance does not become MoneyHorst.

---

## Classification Summary

| Scope | Count | Purpose |
|-------|-------|---------|
| ACTIVE_SCOPE | 28 | Deployment protection, domain boundaries, data integrity, invariants |
| FUTURE_BACKLOG | 21 | Warning system, advanced hardenings, meta-governance |

---

## ACTIVE_SCOPE (27 Requirements)

### Deployment Protection (Req 1–6, 36, 48)

| Req | Title | Rationale | Dependency Impact | Implementation Impact |
|-----|-------|-----------|-------------------|----------------------|
| 1 | CI Full Test Suite Execution | Prevents broken governance contracts from merging | None — standalone CI step | Task 3.1 |
| 2 | CI All-Directory Syntax Validation | Catches syntax errors before merge | None — standalone CI step | Task 3.2 |
| 3 | CI Governance YAML Validation | Prevents malformed config from reaching main | None — standalone CI step | Task 3.3 |
| 4 | CI All-Engine Import Validation | Catches broken engine imports before merge | None — standalone CI step | Task 3.4 |
| 5 | Deployment Gate Framework | Core enforcement mechanism for all gates | Foundation for Req 6, 7, 26, 32 | Tasks 1.2 (DONE), 5.1 |
| 6 | Deployment Gate Time Budgets | Prevents unbounded CI execution | Depends on Req 5 | Task 5.1 |
| 36 | Runtime/CI Consistency Hashing | Detects deployment drift | Depends on Req 48 (canonicalization) | Tasks 3.5, 3.7 |
| 48 | Runtime Integrity Hash Canonicalization | Platform-independent hashing | Required by Req 36 | Task 3.6 |

### Domain Boundary Protection (Req 16–19, 40)

| Req | Title | Rationale | Dependency Impact | Implementation Impact |
|-----|-------|-----------|-------------------|----------------------|
| 16 | Boundary Enforcement — Allowed Writers | Protects artifact ownership model | Core to domainization integrity | Task 5.3 |
| 17 | Boundary Enforcement — Cannot Own | Prevents domain constraint violations | Depends on Domain_Registry | Task 5.3 |
| 18 | Canonical Boundary Runtime Discovery | Auto-classifies new artifacts | Depends on Artifact_Registry | Task 5.3 |
| 19 | Cross-Domain Interaction Detection | Makes unauthorized flows visible | Depends on Req 16 | Task 5.3 |
| 40 | Shadow Authority Detection | Detects undeclared write paths | Depends on Artifact_Registry | Task 7.5 |

### Data Integrity (Req 7–15, 33, 34)

| Req | Title | Rationale | Dependency Impact | Implementation Impact |
|-----|-------|-----------|-------------------|----------------------|
| 7 | Enforcement Mode Configuration | Config-driven mode transitions | Foundation for all enforcement behavior | Task 11.1 |
| 8 | Lifecycle Transition Enforcement | Prevents invalid state transitions | Depends on Lifecycle_State_Machine | Task 5.2 |
| 9 | Read-Only State Protection | Protects archived/superseded artifacts | Depends on Req 8 | Task 5.2 |
| 10 | Regenerable State Gate | Prevents engine overwrites of non-regenerable artifacts | Depends on Req 8 | Task 5.2 |
| 11 | Lifecycle Transition Audit Logging | Traceability for state changes | Depends on Req 12 (ledger) | Task 11.2 |
| 12 | Mutation Audit Ledger — Registry Changes | Traceability beyond git diff | Standalone persistence module | Task 7.1 |
| 13 | Mutation Audit Ledger — Event Persistence | Historical governance decisions | Depends on Req 12 | Task 7.1 |
| 14 | Mutation Audit Ledger — Policy Change Auditing | Traceable runtime behavior changes | Depends on Req 12 | Task 7.1 |
| 15 | Mutation Audit Ledger — Sunset Recording | Deprecation lifecycle traceability | Depends on Req 12 | Task 7.1 |
| 33 | Mutation Actor Identity Model | Typed audit attribution | Foundation for all ledger entries | Task 1.1 (DONE) |
| 34 | Governance Policy Versioning | Historical decision context | Depends on governance config files | Task 7.2 |

### Foundation — Already Implemented (Req 26, 29, 32, 41, 49)

| Req | Title | Rationale | Dependency Impact | Implementation Impact |
|-----|-------|-----------|-------------------|----------------------|
| 26 | Structured Gate Output Format | Machine-readable gate results | Required by CI consumers | Task 1.2 (DONE) |
| 29 | Governance Fail-Mode Classification | Deterministic degradation behavior | Required by all enforcement components | Tasks 1.3, 1.5 (DONE) |
| 32 | Partial Governance Tolerance | Graceful partial degradation | Required by gate framework | Task 1.2 (DONE) |
| 41 | Governance State Provenance Tagging | Explicit state reliability indicators | Required by gate results | Task 1.4 (DONE) |
| 49 | Governance Self-Disable Protection | Prevents self-weakening during execution | Required by fail-mode registry | Task 1.3 (DONE) |

### Invariants and Structural Constraints (Req 25, 28, 39)

| Req | Title | Rationale | Dependency Impact | Implementation Impact |
|-----|-------|-----------|-------------------|----------------------|
| 25 | Invariant Preservation | Foundational guarantees must hold | Validates all new enforcement logic | Task 11.11 |
| 28 | Property-Based Test Coverage | Verification methodology | Validates all enforcement contracts | Property test tasks |
| 39 | Anti-Ontology Proliferation Constraint | Prevents governance bloat | Structural constraint on all additions | Task 11.12 |

---

## FUTURE_BACKLOG (22 Requirements)

### Warning System (Req 20–24)

| Req | Title | Rationale for Deferral | Risk of Deferral |
|-----|-------|----------------------|------------------|
| 20 | Warning Suppression for Known Warnings | Noise reduction — useful but not blocking | Warnings remain noisy; manageable manually |
| 21 | New Warning Escalation | Visibility improvement — not critical for v1 | New warnings may be missed in noise; low risk at current scale |
| 22 | Warning Deduplication | Volume control — not critical at current warning count | Some duplicate output; cosmetic issue |
| 23 | Warning Trend Tracking | Historical analysis — nice-to-have | No trend visibility; acceptable for v1 |
| 24 | Severity-to-Enforcement-Mode Mapping | Connects severity to blocking — only matters in hard mode | No impact until hard mode is activated |

**Dependency impact of deferral**: Task 7.3 (WarningGovernor) and Task 7.4 (warning_baseline.yaml) removed. No active requirements depend on these.

### Advanced Hardenings (Req 30, 31, 35, 37, 38, 42)

| Req | Title | Rationale for Deferral | Risk of Deferral |
|-----|-------|----------------------|------------------|
| 30 | Governance Recursion Protection | Edge case — only matters when governance governs itself | Theoretical infinite loop; mitigated by simple code structure |
| 31 | Governance Cold-Start Mode | First-run handling — one-time event per clone | Manual initialization on first run; acceptable |
| 35 | Enforcement Deadlock Prevention | Edge case — only matters in hard enforcement mode | Deadlocks impossible in observability/soft mode |
| 37 | Transient Artifact Promotion | Boundary crossing governance — not yet needed | Transient artifacts remain ungoverned; acceptable for v1 |
| 38 | Governance Performance Budget | Overhead tracking — premature optimization | Governance overhead is negligible at current scale |
| 42 | Bounded Fail-Soft Degradation | Escalation tracking — only matters with persistent failures | Manual monitoring sufficient for v1 |

**Dependency impact of deferral**: Tasks 5.4, 5.5, 5.6, 9.7, 9.8, 11.3 (partial), 11.4, 11.10 removed. No active requirements depend on these.

### Meta-Governance (Req 43, 44, 45, 46, 47)

| Req | Title | Rationale for Deferral | Risk of Deferral |
|-----|-------|----------------------|------------------|
| 43 | Governance Layer Complexity Budget | Governance about governance growth — self-referential | Complexity grows unchecked; mitigated by CTO review |
| 44 | Mutation Audit Ledger Rotation | Ledger file management — premature at current volume | Ledger grows unbounded; years before it matters |
| 45 | Warning Baseline Decay | Baseline maintenance — no baseline exists yet | No baseline to decay; zero risk |
| 46 | Scoped Policy Version Domains | Granular versioning — premature optimization | Global version sufficient for v1 |
| 47 | Temporary Authority Declarations | Migration escape hatch — not needed until hard mode | No migrations blocked; no need for escape hatch |

**Dependency impact of deferral**: Tasks 9.1–9.6, 11.5–11.9 removed. No active requirements depend on these.

---

## Implementation Impact Summary

### Tasks Remaining (Active Scope)

| Phase | Tasks | Status |
|-------|-------|--------|
| Foundation | 1.1–1.5 | DONE |
| Foundation Verification | 2 | DONE |
| CI Hardening | 3.1–3.7 | TODO |
| CI Verification | 4 | TODO |
| Enforcement Runtime | 5.1–5.3 only | TODO |
| Enforcement Verification | 6 (reduced) | TODO |
| Audit Ledger | 7.1, 7.2, 7.5 | TODO |
| Audit Verification | 8 (reduced) | TODO |
| Integration | 11.1, 11.2, 11.11, 11.12 | TODO |
| Final Verification | 12 (reduced) | TODO |

### Tasks Removed (Backlog)

- 5.4 (RecursionProtector), 5.5 (ColdStartHandler), 5.6 (DeadlockPreventer)
- 7.3 (WarningGovernor), 7.4 (warning_baseline.yaml)
- 9.1–9.8 (all meta-hardenings)
- 11.3–11.10 (most integration wiring)
- All property tests for deferred requirements (~19 property tests)

### Estimated Reduction

- **Before**: 87 tasks
- **After**: ~35 tasks
- **Reduction**: ~60% fewer tasks

---

## Property Tests: Retained vs. Deferred

### Retained (Active Scope)

| Property | Validates | Status |
|----------|-----------|--------|
| 1: GateResult Round-Trip | Req 5.6, 26.4 | DONE |
| 3: ActorIdentity Round-Trip | Req 33.6 | DONE |
| 4: Enforcement Mode Round-Trip | Req 7.6 | DONE |
| 6: Gate Blocking Correctness | Req 5.1, 5.3, 5.4 | TODO |
| 7: Lifecycle Transition Validation | Req 8.1–8.5 | TODO |
| 8: Read-Only State Protection | Req 9.1–9.4 | TODO |
| 9: Regenerable State Gate | Req 10.1–10.4 | TODO |
| 10: Boundary Enforcement | Req 16.1–16.5 | TODO |
| 11: Cannot-Own Consistency | Req 17.1–17.4 | TODO |
| 18: Policy Version Determinism | Req 34.1, 34.5, 34.6 | TODO |
| 19: Runtime Integrity Hash | Req 36.1, 36.5, 36.6 | TODO |
| 24: Shadow Authority Threshold | Req 40.1, 40.3, 40.5 | TODO |
| 31: Hash Canonicalization | Req 48.1, 48.2, 48.4 | TODO |
| 32: Self-Disable Guard | Req 49.1, 49.2, 49.4 | DONE |

### Deferred (Backlog)

Properties 2, 5, 12–17, 20–23, 25–30 — all relate to deferred requirements.

---

## Approval Request

**CTO Action Required:**

1. Approve or adjust this scope freeze classification
2. After approval, Kiro will:
   - Create `governance_future_backlog.md` with deferred requirements
   - Regenerate design.md (reduced scope)
   - Regenerate tasks.md (reduced scope)
   - Continue implementation with ~60% fewer tasks

**No modifications to requirements.md until approval is given.**
