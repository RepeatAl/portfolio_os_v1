# State Change Taxonomy — Implementation Guide

---
artifact_id: state_change_taxonomy_implementation_guide_md
primary_domain: ARCH
artifact_type: operational_readme
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Operational guide for consuming the State Change Taxonomy SSOT
ssot_relationship: explains (does not redefine)
topic: state_change_taxonomy_usage
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [state_change_taxonomy_md]
---

## Purpose

This document explains how to correctly consume and apply the State Change Taxonomy SSOT (`README_state_change_taxonomy.md`). It provides operational guidance for engines, agents, and human developers who need to classify State_Changes, validate Root_Node invariants, and extend the taxonomy.

This guide is EXPLANATORY. The SSOT remains AUTHORITATIVE. This README never redefines canonical truth — it explains how to USE the taxonomy correctly.

---

## Canonical Primitive

**State_Change** — the root-level causal primitive that initiates all propagation in the organism. Every cascade begins with a classified State_Change.

Namespace: `sc.*` (e.g., `sc.macro.rates`, `sc.corporate.earnings`)

---

## Scope

This guide covers:
- How to classify incoming State_Changes using the 4-category taxonomy
- How to apply the Primary Classification Rule for ambiguous cases
- How to validate that Root_Node invariant is preserved
- How to extend the taxonomy with new sub-categories
- How to reference State_Change classifications from downstream systems

---

## Exclusions

This guide does NOT cover:
- The definitions of categories and sub-categories themselves (those live in the SSOT)
- How to detect State_Changes (that is engine behavior — future P0)
- Scoring or ranking of State_Changes by importance
- Asset-level classification or ticker mapping
- Signal implementation
- Any executable code or runtime behavior

---

## Future Consumers

| Consumer | Priority | Consumption Pattern |
|----------|----------|---------------------|
| Relevance Engine | P0 | Classifies detected State_Changes before relevance filtering |
| Asset-to-Narrative Registry | P0 | Uses taxonomy IDs as entry points for upward traversal |
| Propagation Engine | P1 | Uses classified Root_Nodes as starting points for forward propagation |
| Concept Registry | P2 | References sub-category definitions for multi-altitude explanations |
| Versioned Organism Graph | P3 | Tracks which State_Change classifications were active at each timestamp |

---

## Required Invariants

1. **Root Node Invariant**: Assets, tickers, and securities NEVER serve as Root_Nodes. Only State_Changes, Events, Impulses, or Regime_Shifts qualify.
2. **Classification hierarchy preserved**: State_Change type → Expansion type → Affected systems → Affected narratives → Affected assets. This ordering is inviolable.
3. **Taxonomy before assets**: The classification question is "What kind of state change occurred?" — NEVER "How do I classify this asset?"
4. **Exactly 4 top-level categories**: Macro, Corporate, Narrative, Events. No additions to or removals from this set.
5. **Stable IDs mandatory**: Every sub-category entry carries a canonical ID (`sc.*`). Display text is optional; the ID is mandatory.
6. **No numeric scoring**: No sub-category may carry weight, probability, confidence, or importance scores.

---

## Common Failure Modes

### INVALID: Using a ticker as a Root_Node

`Root_Node: "NVDA"` — This names a financial instrument without specifying what changed. Required reformulation: `"Nvidia Guidance Raise"` (sc.corporate.guidance).

### INVALID: Skipping the classification hierarchy

Jumping directly from State_Change to Assets without passing through Expansion type, Affected systems, and Affected narratives violates the mandatory hierarchy.

### INVALID: Classifying by affected asset instead of originating mechanism

If a State_Change affects oil companies, classifying it as "Corporate" when the originating mechanism is a geopolitical event (sc.events.wars) is incorrect. The Primary Classification Rule assigns by originating causal mechanism.

### INVALID: Adding a sub-category without meeting extension criteria

A new sub-category requires: (a) distinct causal mechanism not already covered, (b) scope definition, (c) concrete example, (d) boundary counter-example. Missing any element is invalid.

### VALID: Classifying by originating mechanism

`"Fed Hawkish Shift" → sc.macro.rates` — The originating mechanism is a change in monetary policy (rates), regardless of which downstream assets are affected.

### VALID: Extending with proper criteria

Adding `sc.macro.housing` with: distinct causal mechanism (housing market dynamics), scope definition, concrete example (housing starts collapse), boundary counter-example (REIT earnings miss → belongs to sc.corporate.earnings).

---

## Compatibility Requirements

| Framework | Relationship |
|-----------|-------------|
| 12-Domain Architecture | State_Change_Taxonomy operates within ARCH domain; does not alter other domains |
| Canonical Chain | State_Changes feed into SIGNALS detection; they are detected, not created, by signals |
| Signal_Bubble_v0 | Signals detect State_Changes as sensors; taxonomy classifies what was detected |
| Narrative Framework | Narratives are downstream containers for State_Changes (per primitive chain) |
| Market Data Governance | State_Change_Taxonomy content is Class A (proprietary intellectual property) |
| Engine Roadmap | Taxonomy consumed by P0 (Relevance Engine) and P1 (Propagation Engine) |

---

## Machine-Readable Metadata

```yaml
consumes:
  - market_organism.shared_glossary_reference_md
  - market_organism.principles_md

produces:
  - sc.macro.rates
  - sc.macro.inflation
  - sc.macro.oil
  - sc.macro.liquidity
  - sc.macro.fx
  - sc.corporate.earnings
  - sc.corporate.guidance
  - sc.corporate.capex
  - sc.corporate.ma
  - sc.corporate.buybacks
  - sc.narrative.ai
  - sc.narrative.security
  - sc.narrative.defense
  - sc.narrative.robotics
  - sc.narrative.energy
  - sc.events.elections
  - sc.events.wars
  - sc.events.pandemics
  - sc.events.sporting_events

future_consumers:
  - relevance_engine (P0)
  - asset_to_narrative_registry (P0)
  - propagation_engine (P1)
  - concept_registry (P2)
  - versioned_organism_graph (P3)

invariants:
  - root_node_invariant_enforced
  - classification_hierarchy_preserved
  - taxonomy_before_assets
  - exactly_four_top_level_categories
  - stable_ids_mandatory
  - no_numeric_scoring

known_future_dependencies:
  - engine_roadmap_framework (P0 relevance engine consumes taxonomy)
  - expansion_taxonomy_md (expansion references state_change types)
  - dependency_types_v2_md (dependency paths originate from state_changes)
```
