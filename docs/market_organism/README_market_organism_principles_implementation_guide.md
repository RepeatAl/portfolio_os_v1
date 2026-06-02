# Market Organism Principles — Implementation Guide

---
artifact_id: market_organism.principles_implementation_guide_md
primary_domain: ARCH
artifact_type: operational_readme
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Operational guide for consuming the Market Organism Principles SSOT
ssot_relationship: explains (does not redefine)
topic: market_organism_principles_usage
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism.principles_md]
---

## Purpose

This document explains how to correctly consume and apply the Market Organism Principles SSOT (`README_market_organism_principles.md`). It provides operational guidance for engines, agents, and human developers who need to validate compliance with the six foundational principles.

This guide is EXPLANATORY. The SSOT remains AUTHORITATIVE. This README never redefines canonical truth — it explains how to USE the principles correctly.

---

## Canonical Primitive

**Principle** — a foundational constraint (natural law) that governs market state propagation behavior. The Principles document defines the constraint space within which all other Market Organism deliverables operate.

Namespace: `principle.*`

---

## Scope

This guide covers:
- How to check compliance with each principle during design and implementation
- How to interpret violation conditions
- How to reference principles from downstream documents
- How to extend the principles set (extension criteria)

---

## Exclusions

This guide does NOT cover:
- The definitions of the principles themselves (those live in the SSOT)
- Engine implementation details
- Scoring, weighting, or probability logic
- Asset-level analysis
- Signal implementation
- Any executable code or runtime behavior

---

## Future Consumers

| Consumer | Priority | Consumption Pattern |
|----------|----------|---------------------|
| Propagation Engine | P1 | Validates that forward traversal obeys all 6 principles |
| Relevance Engine | P0 | Validates that relevance filtering preserves organism-over-collection |
| Portfolio-Organism Bridge | P1 | Validates taxonomy-before-assets ordering |
| Concept Registry | P2 | References principles for multi-altitude explanations |
| Model Versioning | P3 | Tracks principle changes as model evolution events |

---

## Required Invariants

1. **Primitive chain preserved**: State_Change → Narrative → System → Asset. No principle may invert this chain.
2. **Assets never root**: No principle example may place an asset as a Root_Node.
3. **No numeric values**: Principles are qualitative constraints only. No scores, weights, or probabilities.
4. **Organism over collection**: All downstream consumers must model propagation, not correlation.
5. **Taxonomy precedes assets**: Classification hierarchy must be respected before any asset association.
6. **Feedback is structural**: Circular causation is mandated; the Organism_Graph is NOT a DAG.

---

## Common Failure Modes

### INVALID: Treating principles as optional guidelines

Principles are HARD CONSTRAINTS. A design that "mostly" follows a principle but introduces a scoring mechanism in one edge case is a violation.

### INVALID: Redefining a principle in a downstream document

If a downstream design doc says "In our context, Principle 3 means X" where X differs from the SSOT definition, that is a redefinition violation. Reference only — never restate with modification.

### INVALID: Introducing numeric values in compliance examples

An example that demonstrates principle compliance by showing "Strength: 0.8" or "Confidence: High (85%)" violates Principle constraints AND the Global Execution Rule 4.

### VALID: Referencing a principle as a constraint on design decisions

`"This engine design satisfies principle.organism_over_collection because it traces propagation paths rather than computing asset correlations."`

### VALID: Citing violation conditions as test criteria

`"Test: Verify that no Root_Node in the graph names a financial instrument without specifying what changed (principle.taxonomy_precedes_assets violation condition)."`

---

## Compatibility Requirements

| Framework | Relationship |
|-----------|-------------|
| 12-Domain Architecture | Principles preserve all 12 domains; no domain added, removed, or redefined |
| Canonical Chain (SIGNALS→SEMANTICS→REASONING→REPORT) | Principles constrain but do not alter the chain |
| Signal_Bubble_v0 | Principles define signals as sensors (leaf-node observations), not causal primitives |
| Narrative Framework | Principles reference narrative as the explanatory container |
| Engine Roadmap | Principles constrain all P0–P3 engine implementations |
| Language Rendering Framework | Principle IDs use stable namespace (`principle.*`), not display text |

---

## Machine-Readable Metadata

```yaml
consumes:
  - market_organism.shared_glossary_reference_md
  - market_organism_framework_requirements

produces:
  - principle.organism_over_collection
  - principle.taxonomy_precedes_assets
  - principle.all_propagation_is_temporal
  - principle.feedback_is_structural
  - principle.expansion_has_order
  - principle.causation_over_correlation

future_consumers:
  - propagation_engine (P1)
  - relevance_engine (P0)
  - portfolio_organism_bridge (P1)
  - concept_registry (P2)
  - model_versioning (P3)

invariants:
  - primitive_chain_preserved
  - assets_never_root
  - no_numeric_values_in_principles
  - organism_over_collection_enforced
  - taxonomy_precedes_assets_enforced
  - feedback_is_structural_mandated

known_future_dependencies:
  - engine_roadmap_framework (P0-P3 capability sequencing)
  - explanation_framework (principle referencing in explanations)
  - signal_lifecycle_definition (principle compliance gate)
```
