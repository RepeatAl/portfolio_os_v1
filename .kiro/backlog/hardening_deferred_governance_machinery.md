# Hardening: Deferred Governance Machinery

**Priority:** P4 (Future — only when scale demands)
**Category:** governance/meta-governance
**Owner:** CTO
**Created:** 2026-05-29
**Status:** DEFERRED
**Source:** CTO Recalibration Decision (governance_delta_recalibration_report.md)

## Context

During the deployment-authority-and-domainization-hardening spec creation, the CTO explicitly decided these governance features are NOT needed for MoneyHorst's current scale (2-person team, 12 stable domains, ~132 artifacts). They were removed from the active spec to prevent governance becoming the product.

## Deferred Items

### 1. Authority Inheritance Rules
- Enterprise RBAC-style authority inheritance between roles
- **Trigger:** Team grows beyond 3 actors
- **Rationale:** OWNER/CI/RUNTIME is sufficient for current scale

### 2. Authority Drift Detection
- Concentration analytics for authority distribution
- **Trigger:** Authority graph exceeds 5 nodes
- **Rationale:** Meaningless with 3 actors

### 3. Domain Merge Semantics
- Formal rules for merging two domains into one
- **Trigger:** Domain count changes significantly (merge needed)
- **Rationale:** 12 domains are stable; no merge has ever been needed

### 4. Domain Split Semantics
- Formal rules for splitting one domain into two
- **Trigger:** Domain count changes significantly (split needed)
- **Rationale:** No split has ever been needed or planned

### 5. Domain Freeze Semantics
- Hard override independent of enforcement mode to freeze a domain
- **Trigger:** Regulatory requirements demand it
- **Rationale:** Adds complexity without proven need

### 6. Complex Transition Quorum
- Multi-condition approval workflow for enforcement mode transitions
- **Trigger:** Enforcement mode changes become frequent
- **Rationale:** Simple cooldown (4h default) achieves the same goal

### 7. Enforcement Mode Stabilization Windows
- N-run enterprise stabilization before mode transition
- **Trigger:** Mode oscillation becomes a real problem despite cooldown
- **Rationale:** 4h cooldown is sufficient for current cadence

### 8. Influence Depth Enforcement
- Graph-theory-based depth limits on governance influence chains
- **Trigger:** Governance module count exceeds 30
- **Rationale:** Cycle detection is sufficient for ~20 modules

## Revisit Criteria

These items should be reconsidered ONLY when:
1. Team grows beyond 3 actors
2. Domain count changes significantly (merge/split needed)
3. Regulatory requirements demand enterprise-grade controls
4. Enforcement mode changes become frequent enough to need quorum
5. Governance module count exceeds 30

## CTO Decision

> Advanced governance machinery can be revisited ONLY when scale demands it.
> Until then: lean governance, maximum financial intelligence velocity.
> MoneyHorst gewinnt durch bessere Modelle, nicht durch mehr Governance.
