# Temporal Taxonomy — Implementation Guide

---
artifact_id: temporal_taxonomy_implementation_guide_md
primary_domain: ARCH
artifact_type: operational_readme
lifecycle_status: canonical
created_date: 2026-06-01
last_modified: 2026-06-01
owner_role: Operational guide for consuming the Temporal Taxonomy SSOT
ssot_relationship: explains (does not redefine)
topic: temporal_taxonomy_usage
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [temporal_taxonomy_md]
---

## Purpose

This document explains how to correctly consume and apply the Temporal Taxonomy SSOT (`README_temporal_taxonomy.md`). It provides operational guidance for engines, agents, and human developers who need to assign temporal properties to Dependency_Paths, validate qualitative-only constraints, and interpret temporal propagation patterns.

This guide is EXPLANATORY. The SSOT remains AUTHORITATIVE. This README never redefines canonical truth — it explains how to USE the temporal properties correctly.

---

## Canonical Primitive

**Temporal_Property** — a qualitative descriptor characterizing how effects propagate along a Dependency_Path over time. The Temporal Taxonomy defines exactly five properties that every Dependency_Path carries.

Namespace: `temporal.*` (e.g., `temporal.latency`, `temporal.amplification`)

---

## Scope

This guide covers:
- How to assign temporal properties to Dependency_Paths in the Organism_Graph
- How to interpret the qualitative scales (calendar units and 5-level scales)
- How to apply temporal properties per Expansion_Order
- How to validate the numeric prohibition constraint
- How to extend temporal units or levels (extension criteria)

---

## Exclusions

This guide does NOT cover:
- The definitions of the 5 temporal properties themselves (those live in the SSOT)
- How to compute temporal values algorithmically (prohibited — qualitative assignment only)
- Numeric time-series modeling or simulation
- Probability distributions over temporal outcomes
- Signal implementation
- Any executable code or runtime behavior

---

## Future Consumers

| Consumer | Priority | Consumption Pattern |
|----------|----------|---------------------|
| Propagation Engine | P1 | Applies temporal properties at each hop during forward traversal |
| Portfolio-Organism Bridge | P1 | Shows time-to-impact for portfolio exposure |
| Concept Registry | P2 | Explains temporal concepts at multiple altitudes |
| Historical Accuracy Tracker | P2 | Validates temporal predictions against historical outcomes |
| Versioned Organism Graph | P3 | Tracks temporal property changes over time |

---

## Required Invariants

1. **Numeric prohibition**: No temporal property may carry a numeric score, weight, probability, or quantitative model value. All values are qualitative descriptors only.
2. **Exactly 5 properties**: Latency, Duration, Amplification, Dampening, Feedback_Delay. No additions without meeting extension criteria.
3. **Calendar units for time**: Latency, Duration, and Feedback_Delay use discrete calendar units only (Day, Week, Month, Quarter, Year).
4. **5-level qualitative scale**: Amplification and Dampening use exactly 5 levels (None, Low, Moderate, High, Extreme).
5. **Every Dependency_Path carries all 5**: No temporal property may be omitted from a Dependency_Path assignment.
6. **Tendencies, not rules**: Amplification typically decreasing and Dampening typically increasing with distance are observations, not hard constraints.

---

## Common Failure Modes

### INVALID: Using numeric values for temporal properties

`"Latency: 3.5 days"` or `"Amplification: 0.8"` — These introduce numeric values. Correct: `"Latency: Day"` and `"Amplification: High"`.

### INVALID: Treating temporal tendencies as rules

`"Amplification MUST decrease at each order"` — This is not a rule. The SSOT states these are tendencies that specific paths may deviate from.

### INVALID: Omitting temporal properties from a Dependency_Path

A path labeled `dep.macro` with only Latency and Duration assigned (missing Amplification, Dampening, Feedback_Delay) is incomplete.

### INVALID: Adding quantitative models to temporal descriptions

`"Latency follows an exponential decay curve with half-life of 2 months"` — This introduces quantitative modeling. Temporal properties are qualitative descriptors only.

### VALID: Qualitative assignment with calendar units

`"Latency: Month, Duration: Quarter, Amplification: Moderate, Dampening: Low, Feedback_Delay: Quarter"`

### VALID: Temporal propagation across orders showing tendencies

`"1st Order: Latency=Day, Amp=High; 2nd Order: Latency=Month, Amp=Moderate; 3rd Order: Latency=Quarter, Amp=Low"` — Shows the typical pattern without claiming it as a rule.

---

## Compatibility Requirements

| Framework | Relationship |
|-----------|-------------|
| 12-Domain Architecture | Temporal properties operate within ARCH domain; no domain change |
| Canonical Chain | Temporal properties characterize propagation speed through the chain |
| Signal_Bubble_v0 | Signals detect effects; temporal taxonomy describes WHEN effects arrive |
| User Intelligence Journey | Temporal model consumed by Scenario Journey for time-based reasoning |
| Dependency Types v2 | Each dependency type has a typical temporal profile |
| Engine Roadmap | Temporal consumed by P1 (Propagation Engine) for time simulation |

---

## Machine-Readable Metadata

```yaml
consumes:
  - market_organism.shared_glossary_reference_md
  - dependency_types_v2_md
  - expansion_taxonomy_md

produces:
  - temporal.latency
  - temporal.duration
  - temporal.amplification
  - temporal.dampening
  - temporal.feedback_delay

future_consumers:
  - propagation_engine (P1)
  - portfolio_organism_bridge (P1)
  - concept_registry (P2)
  - historical_accuracy_tracker (P2)
  - versioned_organism_graph (P3)

invariants:
  - numeric_prohibition_enforced
  - exactly_five_properties
  - calendar_units_for_time
  - five_level_qualitative_scale
  - all_properties_on_every_path
  - tendencies_not_rules

known_future_dependencies:
  - engine_roadmap_framework (P1 propagation engine applies temporal properties)
  - expansion_taxonomy_md (temporal properties assigned per expansion order)
  - dependency_types_v2_md (each type has typical temporal profile)
```
