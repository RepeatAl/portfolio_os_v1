# Shared Glossary Reference — Semantic Contract

---
artifact_id: market_organism.shared_glossary_reference
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
spec_source: .kiro/specs/market-organism-framework/requirements.md
---

## Purpose

This document is the **semantic contract** for the Market Organism Framework. It defines how all deliverables reference shared terminology, how cross-references work between documents, and how new terms enter the system.

This document contains **rules only**. It does not define terms. It does not introduce new concepts. It points to the single source of truth and establishes the protocol for consuming it.

---

## 1. Single Source of Truth (SSOT) Declaration

The canonical glossary for the Market Organism Framework lives in exactly one location:

```
.kiro/specs/market-organism-framework/requirements.md → ## Glossary
```

This section is the **sole authoritative definition layer** for all terms used across the five framework deliverables. No other document may define, redefine, extend, or paraphrase glossary terms.

---

## 2. Glossary Usage Rules

### Rule 2.1 — No Duplication

No deliverable may redefine a term that exists in the canonical glossary. If a deliverable uses a term, it uses the term **as defined in the SSOT**. Inline definitions, paraphrases, or "local glossaries" are prohibited.

### Rule 2.2 — Consistent Term Usage

All deliverables must use the exact term form as it appears in the canonical glossary. This includes:

- Exact casing (e.g., `State_Change`, not `state change` or `StateChange`)
- Exact underscore conventions (e.g., `Dependency_Path`, not `dependency path`)
- Exact compound forms (e.g., `Feedback_Loop`, not `feedback loop` or `Feedback`)

### Rule 2.3 — New Terms Glossary-First

If any deliverable requires a term that does not yet exist in the canonical glossary:

1. The term MUST be added to the canonical glossary FIRST
2. The term MUST include a complete definition following the existing glossary format
3. Only AFTER the glossary is updated may the term be used in any deliverable

This prevents semantic drift where the same concept acquires different meanings across documents.

### Rule 2.4 — Glossary Reference Section

Each deliverable MUST include a "Glossary Reference" section containing:

```markdown
## Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary

This document does not define terms. It consumes them.
```

---

## 3. Cross-Reference Convention

### Convention Format

When a deliverable references a concept, section, or classification defined in another deliverable, it MUST use the following cross-reference pattern:

```
(See: [Deliverable_Name], Section: [Section_Title])
```

### Examples

```
(See: README_state_change_taxonomy, Section: Primary Classification Rule)
(See: README_dependency_types_v2, Section: Multi-Type Coexistence Rules)
(See: README_temporal_taxonomy, Section: Latency Definitions)
(See: README_expansion_taxonomy, Section: Worked Examples)
(See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural)
```

### Convention Rules

| Rule | Description |
|------|-------------|
| Deliverable_Name is the filename without extension | e.g., `README_state_change_taxonomy` not `README_state_change_taxonomy.md` |
| Section_Title matches the heading exactly | Copy the heading text as-is from the target document |
| One cross-reference per concept | Do not chain multiple cross-references for the same concept |
| Cross-reference replaces duplication | If you would otherwise copy a definition, use a cross-reference instead |
| Cross-references are human-readable | They must make sense to a reader who has not opened the target document |

### Why This Convention Matters

This pattern enables:

1. **Explanation Traversal** — Agents and systems can follow cross-references to build multi-level explanations without dead ends
2. **Agent Navigation** — Automated systems can resolve references to locate authoritative content
3. **Historical Reconstruction** — Auditors can trace how a concept was used across the framework
4. **Registry Consumption** — Downstream registries can parse cross-references to build dependency graphs between documents

---

## 4. Canonical Term Policy

### Policy 4.1 — Term Authority

The canonical glossary is the sole authority for term meaning. If a deliverable's usage appears to conflict with the glossary definition, the glossary definition prevails.

### Policy 4.2 — Term Stability

Once a term is added to the canonical glossary, its definition may only be changed through an explicit glossary amendment. Deliverables may not implicitly redefine terms through contextual usage.

### Policy 4.3 — Term Scope

Terms in the canonical glossary apply to ALL five deliverables equally. No deliverable may claim a "local interpretation" of a glossary term.

### Policy 4.4 — Undefined Terms

If a deliverable uses a term that is NOT in the canonical glossary and is NOT a common English word, this constitutes a contract violation. The term must either:

1. Be added to the canonical glossary (per Rule 2.3), or
2. Be replaced with an existing glossary term that covers the intended meaning

---

## 5. SSOT Pointers — Deliverable Registry

The five deliverables governed by this semantic contract:

| # | Deliverable | Location | Single Concern |
|---|-------------|----------|----------------|
| 1 | README_market_organism_principles | `docs/market_organism/README_market_organism_principles.md` | Foundational constraints on system behavior |
| 2 | README_state_change_taxonomy | `docs/market_organism/README_state_change_taxonomy.md` | Classification of impulse types |
| 3 | README_dependency_types_v2 | `docs/market_organism/README_dependency_types_v2.md` | Classification of causal connection types |
| 4 | README_temporal_taxonomy | `docs/market_organism/README_temporal_taxonomy.md` | Temporal properties of propagation |
| 5 | README_expansion_taxonomy | `docs/market_organism/README_expansion_taxonomy.md` | Expansion orders and worked examples |

### SSOT Chain

```
Canonical Glossary (requirements.md § Glossary)
    ↓ consumed by
This Semantic Contract (README_shared_glossary_reference.md)
    ↓ governs
Five Framework Deliverables (listed above)
    ↓ referenced by
Downstream systems (engines, registries, explanation layers — FUTURE)
```

---

## 6. Compliance Checklist

Before any deliverable is considered complete, verify:

- [ ] All terms used match the canonical glossary exactly (casing, underscores, compound forms)
- [ ] No inline definitions or paraphrases of glossary terms appear
- [ ] A "Glossary Reference" section exists pointing to the SSOT
- [ ] All cross-references to other deliverables use the `(See: [Deliverable_Name], Section: [Section_Title])` format
- [ ] No new terms are introduced without first being added to the canonical glossary
- [ ] The document stays within its single concern boundary

---

## 7. What This Document Is NOT

| This document is NOT | Because |
|---------------------|---------|
| A glossary | Definitions live in requirements.md only |
| A summary of the framework | Summaries duplicate content |
| An introduction to the organism model | Introductions belong in individual deliverables |
| A design document | Design decisions live in design.md |
| An implementation guide | No implementation exists in this spec |

---

## Satisfies

- **Requirement 10.7**: Each deliverable references the shared Glossary for term definitions (this contract defines how)
- **Requirement 10.8**: Cross-references identify the source deliverable by name rather than duplicating definitions (this contract defines the convention)
