# Expansion Taxonomy — Implementation Guide

---
artifact_id: expansion_taxonomy_implementation_guide_md
primary_domain: ARCH
artifact_type: operational_readme
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Operational guide for consuming the Expansion Taxonomy SSOT
ssot_relationship: explains (does not redefine)
topic: expansion_taxonomy_usage
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [expansion_taxonomy_md]
---

## Purpose

This document explains how to correctly consume and apply the Expansion Taxonomy SSOT (`README_expansion_taxonomy.md`). It provides operational guidance for engines, agents, and human developers who need to trace propagation through expansion orders, apply termination criteria, detect feedback loops, and construct worked examples.

This guide is EXPLANATORY. The SSOT remains AUTHORITATIVE. This README never redefines canonical truth — it explains how to USE the expansion taxonomy correctly.

---

## Canonical Primitive

**Expansion_Order** — the distance from the originating Impulse measured in propagation hops. Each hop traverses exactly one Dependency_Path. The Expansion Taxonomy defines exactly four canonical orders (1st through 4th).

Namespace: `order.*` (e.g., `order.first`, `order.second`, `order.third`, `order.fourth`)

---

## Scope

This guide covers:
- How to assign Expansion_Orders to affected systems during propagation
- How to apply termination criteria (when propagation stops)
- How to detect and classify feedback loops vs. continued expansion
- How to construct valid worked examples
- How to extend beyond 4th order (extension criteria)

---

## Exclusions

This guide does NOT cover:
- The definitions of the 4 expansion orders themselves (those live in the SSOT)
- How to simulate propagation computationally (that is engine behavior — future P1)
- Scoring or ranking of affected systems by importance
- Probability of propagation reaching a given order
- Signal implementation
- Any executable code or runtime behavior

---

## Future Consumers

| Consumer | Priority | Consumption Pattern |
|----------|----------|---------------------|
| Reverse Graph Traversal | P0 | Traces expansion orders backward from leaf to root |
| Relevance Engine | P0 | Identifies which expansion orders affect user's portfolio |
| Propagation Engine | P1 | Traverses forward through orders applying temporal properties |
| Portfolio-Organism Bridge | P1 | Maps portfolio positions to their expansion order from active State_Changes |
| Versioned Organism Graph | P3 | Snapshots expansion state at each timestamp |

---

## Required Invariants

1. **Exactly 4 orders**: 1st, 2nd, 3rd, 4th. No additions without meeting extension criteria (evidence of identifiable Dependency_Path at that distance + complete worked example).
2. **Discrete hops**: Expansion is counted in whole numbers. There is no "1.5th Order."
3. **Shortest path determines order**: An affected system belongs to Nth Order if and only if the shortest path from Root_Node traverses exactly N Dependency_Paths.
4. **Termination is explicit**: Propagation stops when no further identifiable Dependency_Path connects to an additional system not already in the sequence.
5. **Feedback ≠ Expansion**: A path revisiting an existing node is a Feedback_Loop, NOT continued expansion. The Organism_Graph is NOT a DAG.
6. **No numeric scoring**: No expansion order may carry probability of reaching, strength of effect, or confidence values.

---

## Common Failure Modes

### INVALID: Treating feedback as 5th order expansion

If a 3rd-order effect propagates back to influence the Root_Node, that is a Feedback_Loop (circular Dependency_Path), not 4th or 5th order expansion. Classify per Feedback Detection Rule.

### INVALID: Assigning order by effect magnitude rather than hop count

`"This is 1st Order because the effect is large"` — Order is determined by hop count (shortest path distance), not by magnitude. A small effect 1 hop away is 1st Order; a large effect 3 hops away is 3rd Order.

### INVALID: Skipping orders in a worked example

A worked example showing 1st Order → 3rd Order without 2nd Order systems is structurally incomplete. Each order must have identifiable affected systems.

### INVALID: Claiming propagation cannot terminate

`"Effects always propagate to 4th Order"` — Not all State_Changes reach 4th Order. Termination criteria apply when no further Dependency_Path exists.

### VALID: Hop-count-based assignment

`"TSMC (2nd Order) because the shortest path from 'Fed Hawkish Shift' traverses Fed→Bank_Lending (dep.macro) → Semiconductor_Capex (dep.fundamental) → TSMC = 2 hops."`

### VALID: Feedback loop detection

`"Path from 4th Order 'Consumer_Spending' back to 1st Order 'Retail_Revenue' via dep.flow constitutes a Feedback_Loop. This is NOT 5th Order expansion."`

---

## Compatibility Requirements

| Framework | Relationship |
|-----------|-------------|
| 12-Domain Architecture | Expansion operates within ARCH domain; no domain boundary change |
| Canonical Chain | Expansion provides the propagation model that SIGNALS/SEMANTICS traverse |
| Signal_Bubble_v0 | Signals are leaf-node observations at various expansion orders |
| Narrative Framework | Narratives carry propagation; expansion traces how narratives are affected |
| Dependency Types v2 | Each expansion hop traverses a typed Dependency_Path |
| Temporal Taxonomy | Each hop carries temporal properties (latency increases with order) |
| Engine Roadmap | Expansion consumed by P0 (traversal) and P1 (propagation engine) |

---

## Machine-Readable Metadata

```yaml
consumes:
  - market_organism.shared_glossary_reference_md
  - market_organism.principles_md
  - state_change_taxonomy_md
  - dependency_types_v2_md
  - temporal_taxonomy_md

produces:
  - order.first
  - order.second
  - order.third
  - order.fourth
  - expansion.termination_criteria
  - expansion.feedback_detection_rule

future_consumers:
  - reverse_graph_traversal (P0)
  - relevance_engine (P0)
  - propagation_engine (P1)
  - portfolio_organism_bridge (P1)
  - versioned_organism_graph (P3)

invariants:
  - exactly_four_orders
  - discrete_hops_only
  - shortest_path_determines_order
  - termination_is_explicit
  - feedback_not_expansion
  - no_numeric_scoring

known_future_dependencies:
  - engine_roadmap_framework (P0 traversal and P1 propagation consume expansion orders)
  - state_change_taxonomy_md (Root_Nodes originate from classified State_Changes)
  - dependency_types_v2_md (each hop traverses a typed path)
  - temporal_taxonomy_md (temporal properties per order)
```
