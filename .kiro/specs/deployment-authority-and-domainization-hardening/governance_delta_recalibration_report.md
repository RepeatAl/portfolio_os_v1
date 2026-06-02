# Governance Delta Recalibration Report

## CTO Decision Summary

MoneyHorst is a **Financial Intelligence Compiler** — not an enterprise governance platform. The governance layer must protect correctness, determinism, auditability, and deployment safety, but it must NOT become the product.

**Target ratio:** 70% Financial Intelligence / 20% Runtime Integrity / 10% Governance

The original delta spec (21 requirements) was over-engineered for the actual product nature. It modeled enterprise-grade authority inheritance, bank-style transition quorums, and complex domain lifecycle machinery that a 2-person team (Rabieb + Kiro) does not need.

---

## What Was Too Much

| Removed Requirement | Reason |
|---|---|
| Authority Inheritance Rules (Req 7) | Enterprise RBAC for a 2-person team. OWNER/CI/RUNTIME is sufficient. |
| Authority Drift Detection (Req 9) | Concentration analytics for a system with 3 actors is meaningless. |
| Enforcement Mode Transition Quorum (Req 12) | Bank-grade multi-condition approval workflow. Anti-flapping + cooldown is sufficient. |
| Enforcement Mode Stabilization Window (Req 11) | 10-run enterprise stabilization. Simple cooldown achieves the same goal. |
| Enforcement Mode Rollback Semantics (Req 13) | Double cooldowns, frequency tracking, 30-day windows — overkill. Simple rollback logging is enough. |
| Domain Freeze Semantics (Req 17) | Hard override independent of enforcement mode — adds complexity without proven need. |
| Domain Merge Semantics (Req 18) | 12 domains are stable. No merge has ever been needed or planned. |
| Domain Split Semantics (Req 19) | Same — no split has ever been needed or planned. |
| Domain Ownership Migration (Req 20) | Individual artifact transfers are already possible via registry edits + audit ledger. |
| Influence Depth Enforcement (Req 3) | Heavy graph theory for a governance layer with ~20 modules. Cycle detection is sufficient. |

---

## What Remains Necessary

| Kept Area | Justification |
|---|---|
| Circular Influence Protection | Cheap to implement, prevents real structural catastrophe. Governance modules influencing each other in cycles would create non-deterministic enforcement. |
| Minimal Deployment Authority | Prevents a single actor from both deploying AND mutating governance rules. Real safety for CI/CD integrity. |
| Simple Enforcement Stability | Anti-flapping prevents mode oscillation that would confuse developers and create inconsistent enforcement behavior. |
| Minimal Domain Lifecycle | Domains need deprecation + archival paths. Without this, dead domains accumulate forever with orphaned artifacts. |
| Property-Based Tests | Hypothesis tests for the above — mandatory per project standards. |

---

## What Moves to Future Backlog

These items are NOT needed now but MAY be revisited when scale requires:

- Authority inheritance (when team grows beyond 3 actors)
- Authority drift analytics (when authority graph has >5 nodes)
- Complex transition quorum (when enforcement mode changes become frequent)
- Domain merge/split mechanics (when domain count changes significantly)
- Domain freeze (when regulatory requirements demand it)
- Influence depth enforcement (when governance module count exceeds 30)

**Trigger for revisiting:** Only when MoneyHorst reaches multi-team scale OR regulatory requirements demand it.

---

## Simplified Spec Scope

**Before:** 21 requirements, 95+ acceptance criteria
**After:** 12 requirements, ~45 acceptance criteria

| Area | Requirements | Focus |
|---|---|---|
| Circular Governance Protection | 3 | Declaration, cycle detection, directionality |
| Minimal Deployment Authority | 3 | Structure, topology, provenance |
| Simple Enforcement Stability | 2 | Cooldown, rollback logging |
| Minimal Domain Lifecycle | 2 | State model (active/deprecated/archived), deprecation reassignment |
| Property-Based Tests | 1 | 5 Hypothesis properties |
| Invariant Preservation | 1 | Delta-layer non-interference guarantee |

---

## Risk Justification

| Risk | Mitigation |
|---|---|
| Circular governance influence | Cycle detection catches this at initialization |
| Single actor deploys + mutates governance | Topology constraint prevents this |
| Mode oscillation (soft↔hard flapping) | 24h cooldown prevents this |
| Dead domains with orphaned artifacts | Deprecation + reassignment plan prevents this |
| Governance becomes the product | This recalibration explicitly prevents this |

---

## CTO Decision

Advanced governance machinery can be revisited ONLY when:
1. Team grows beyond 3 actors
2. Domain count changes significantly (merge/split needed)
3. Regulatory requirements demand enterprise-grade controls
4. Enforcement mode changes become frequent enough to need quorum

Until then: **lean governance, maximum financial intelligence velocity.**
