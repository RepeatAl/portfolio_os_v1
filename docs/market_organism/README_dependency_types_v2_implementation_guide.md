# Dependency Types v2 — Implementation Guide

---
artifact_id: dependency_types_v2_implementation_guide_md
primary_domain: ARCH
artifact_type: operational_readme
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Operational guide for consuming the Dependency Types v2 SSOT
ssot_relationship: explains (does not redefine)
topic: dependency_types_v2_usage
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [dependency_types_v2_md]
---

## Purpose

This document explains how to correctly consume and apply the Dependency Types v2 SSOT (`README_dependency_types_v2.md`). It provides operational guidance for engines, agents, and human developers who need to label edges in the Organism_Graph, apply multi-type coexistence rules, and distinguish dependencies from correlations.

This guide is EXPLANATORY. The SSOT remains AUTHORITATIVE. This README never redefines canonical truth — it explains how to USE the dependency types correctly.

---

## Canonical Primitive

**Dependency_Type** — a classification of the causal mechanism (edge label) through which a State_Change at one node propagates to produce an effect at another node in the Organism_Graph.

Namespace: `dep.*` (e.g., `dep.price`, `dep.narrative`, `dep.butterfly`)

---

## Scope

This guide covers:
- How to assign Dependency_Types to edges in the Organism_Graph
- How to apply multi-type coexistence rules when multiple types exist on a single path
- How to distinguish dependencies from correlations
- How to extend the type set (extension criteria)
- How to reference Dependency_Types from Expansion and Temporal documents

---

## Exclusions

This guide does NOT cover:
- The definitions of the 10 types themselves (those live in the SSOT)
- How to compute dependency strength (that would be numeric scoring — prohibited)
- How to weight dependencies (prohibited)
- Asset-level edge creation logic
- Signal implementation
- Any executable code or runtime behavior

---

## Future Consumers

| Consumer | Priority | Consumption Pattern |
|----------|----------|---------------------|
| Asset-to-Narrative Registry | P0 | Uses dependency types to map upward traversal paths |
| Reverse Graph Traversal | P0 | Traverses edges labeled with dependency types |
| Propagation Engine | P1 | Applies dependency-type-specific propagation logic |
| Portfolio-Organism Bridge | P1 | Identifies which dependency types connect portfolio to organism |
| Historical Accuracy Tracker | P2 | Tracks accuracy per dependency type |

---

## Required Invariants

1. **Exactly 10 types**: Price, Fundamental, Narrative, Flow, Ownership, Supply_Chain, Macro, Behavioral, Regulatory, Butterfly. No additions without meeting extension criteria.
2. **Unique type differentiation**: No two types share identical causal channel + directionality + propagation characteristics combination.
3. **Dependency ≠ Correlation**: Every labeled edge must have an identifiable causal mechanism. Statistical co-movement alone is never sufficient.
4. **Multi-type coexistence is unordered**: When multiple types exist on a single path, no inherent priority ordering exists.
5. **Temporal properties inherited**: Combined types inherit shortest Latency and longest Duration from constituent types.
6. **No numeric weights**: No dependency may carry a numeric strength, weight, or probability value.

---

## Common Failure Modes

### INVALID: Labeling an edge as "correlated" without causal mechanism

`"NVDA and AMD are correlated"` — This is a statistical observation, not a typed dependency. Required: identify the causal mechanism (e.g., `dep.narrative` through shared AI narrative, or `dep.supply_chain` through shared TSMC dependency).

### INVALID: Inventing a new type without extension criteria

Adding `dep.sentiment` without demonstrating: (a) unique causal channel + directionality + propagation combination not already covered by `dep.behavioral`, (b) mechanism description, (c) concrete example.

### INVALID: Assigning numeric strength to a dependency type

`"dep.price with strength 0.7"` — Numeric values are prohibited. Qualitative temporal properties (from Temporal_Taxonomy) describe propagation characteristics instead.

### INVALID: Treating multi-type edges as ordered

`"Primary: dep.price, Secondary: dep.flow"` implies priority. Multi-type edges are unordered. One type MAY be designated as dominant causal channel, but this is a description, not a ranking.

### VALID: Labeling with causal mechanism

`"Federal Reserve rate change → Bank lending costs via dep.macro (Economic channel, Unidirectional)"` — Identifies the specific causal mechanism.

### VALID: Multi-type with combined temporal properties

`"Path carries dep.price + dep.narrative. Combined temporal: Latency=Day (shortest), Duration=Quarter (longest)."`

---

## Compatibility Requirements

| Framework | Relationship |
|-----------|-------------|
| 12-Domain Architecture | Dependency types classify edges within ARCH domain; no domain boundary change |
| Canonical Chain | Dependency_Paths are traversed by the chain (SIGNALS detects, SEMANTICS classifies, REASONING interprets) |
| Signal_Bubble_v0 | Signals detect effects at endpoints of dependency paths |
| Narrative Framework | `dep.narrative` type references Narrative Framework ontological definition |
| Temporal Taxonomy | Each dependency type has a typical temporal profile cross-referenced to Temporal_Taxonomy |
| Engine Roadmap | Types consumed by P0 (traversal) and P1 (propagation engine) |

---

## Machine-Readable Metadata

```yaml
consumes:
  - market_organism.shared_glossary_reference_md
  - market_organism.principles_md
  - temporal_taxonomy_md

produces:
  - dep.price
  - dep.fundamental
  - dep.narrative
  - dep.flow
  - dep.ownership
  - dep.supply_chain
  - dep.macro
  - dep.behavioral
  - dep.regulatory
  - dep.butterfly

future_consumers:
  - asset_to_narrative_registry (P0)
  - reverse_graph_traversal (P0)
  - propagation_engine (P1)
  - portfolio_organism_bridge (P1)
  - historical_accuracy_tracker (P2)

invariants:
  - exactly_ten_types
  - unique_type_differentiation
  - dependency_not_correlation
  - multi_type_coexistence_unordered
  - temporal_properties_inherited
  - no_numeric_weights

known_future_dependencies:
  - engine_roadmap_framework (P0 traversal and P1 propagation consume types)
  - expansion_taxonomy_md (expansion paths use dependency types as edge labels)
  - temporal_taxonomy_md (each type has typical temporal profile)
```
