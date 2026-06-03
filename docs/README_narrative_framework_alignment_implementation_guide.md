# Narrative Framework v2 — Implementation Guide

> **This document is supplementary.** The canonical source of truth is `docs/README_narrative_framework.md` (Narrative Framework v2). This guide does NOT redefine, override, or extend any canonical truth declared in that document. It exists solely to help users navigate, apply, and verify compliance with the Narrative Framework v2.

---

## Purpose

This guide helps practitioners USE the Narrative Framework v2 document effectively. It answers:

- How is the document organized?
- How do I find what I need?
- How do I register a new narrative?
- How do I read the lifecycle state machine?
- How do I traverse cross-references?
- How do I verify my work complies with the framework's constraints?

If you need to know WHAT a narrative is, read the Narrative Framework v2 itself. If you need to know HOW to work with it, read this guide.

---

## Document Structure — The 17 Sections

The Narrative Framework v2 is organized into 17 sections plus a YAML metadata header and a traceability table. The sections follow a logical progression: understand the ontology first, then the formalization, then the integration contracts, then the constraints.

### Quick Navigation Map

| # | Section | What It Tells You |
|---|---------|-------------------|
| — | YAML Metadata Header | Artifact identity, domain, dependencies, version |
| 1 | Scope Statement | What this document IS and IS NOT |
| 2 | Glossary Reference + Amendments | Canonical term definitions (Narrative_Container, Narrative_Membership, Narrative_Interaction) |
| 3 | The Primitive Chain | `State_Change → Narrative → System → Asset` and each primitive's role |
| 4 | What Is a Narrative? | Formal definition, canonical ID format, rendering independence |
| 5 | Narrative vs. State_Change | Why Narrative is container (not cause), State_Change is cause (not container) |
| 6 | Narrative Lifecycle State Machine | 6 states, 7 transitions, velocity observation, constraints |
| 7 | Narrative Hierarchy | Meta-narratives, sub-narratives, flat namespace with naming convention |
| 8 | Multi-Narrative Membership | 5 membership rules, membership record structure, influence categories |
| 9 | State_Change-to-Narrative Interactions | 5 interaction types (Creates/Strengthens/Weakens/Kills/Revives) |
| 10 | Dependency_Type Integration | `dep.narrative` (mechanism) vs. `narrative.*` (container) distinction |
| 11 | Feedback Loop Integration | Self-reinforcing narrative loops vs. linear lifecycle progression |
| 12 | Explanation Readiness Contract | Level 4 in the explanation chain — upward/downward traversal |
| 13 | Narrative Extension Criteria | How to qualify a new narrative for canonical inclusion |
| 14 | Signal Sensor Relationship | Signals detect effects; they do NOT cause transitions |
| 15 | Exclusion Constraints | 8 things this framework explicitly prohibits |
| 16 | Architectural Compatibility | 6 declarations of preservation with existing architecture |
| 17 | Cross-References | Complete index of all external deliverable references |
| — | Satisfies (traceability) | Mapping of requirements to sections |

### Reading Strategies

- **First-time reader**: Read sections 1–5 sequentially for the conceptual foundation, then jump to whichever section addresses your immediate question.
- **Narrative registrar**: Go directly to Section 13 (Extension Criteria), then Section 4 (ID format), then Section 6 (initial lifecycle state).
- **Integration engineer**: Start with Section 10 (Dependency_Type distinction), then Section 12 (Explanation Readiness), then Section 17 (Cross-References).
- **Compliance auditor**: Start with Section 15 (Exclusion Constraints), then Section 16 (Architectural Compatibility), then verify against the constraints.

---

## How to Register a New Narrative

Registering a new narrative is a controlled process. Not every market concept qualifies. Follow these steps, referencing Section 13 (Narrative Extension Criteria) as the authoritative source.

### Step 1: Verify Inclusion Criteria (Section 13)

Your candidate narrative must satisfy ALL four inclusion criteria:

1. **Distinct shared belief** — It represents a belief structure not already covered by an existing `narrative.*` entry. Check the namespace for overlap.
2. **Falsifiable** — You can state a specific condition under which the narrative would be invalidated. If you cannot articulate what would kill it, it is not a narrative.
3. **Connects State_Change to System** — There must be an identifiable causal path: at least one `sc.*` origin leading through the narrative to at least one `system.*` destination.
4. **Canonical ID assigned before first use** — The ID must follow namespace rules (Section 4) and be assigned before the narrative appears in any canonical document.

### Step 2: Verify It Does NOT Match Exclusion Criteria (Section 13)

Reject the candidate if it matches any of:

- A theme without an identifiable originating State_Change (no causal root = not a narrative)
- A sector classification without a causal belief (structural category, not explanatory container)
- A statistical pattern without shared market interpretation (correlation without causal explanation)

### Step 3: Assign Canonical ID (Section 4)

Format: `narrative.[descriptive_token]`

Rules:
- Lowercase only
- Underscore-separated words
- Language-neutral (English tokens are codes, not display text)
- Stable once assigned (never rename the ID; display text can change freely)
- Unique within `narrative.*` namespace

### Step 4: Complete Required Fields (Section 13)

Every new narrative registration must include:

| Field | Format | Example |
|-------|--------|---------|
| Canonical ID | `narrative.*` | `narrative.compute_sovereignty` |
| Scope definition | Plain text describing the belief structure | "Government-driven investment in domestic compute capacity" |
| Birth trigger | `sc.*` ID | `sc.policy.industrial.chips_act` |
| Connected System(s) | `system.*` ID(s) | `system.semiconductor_supply` |
| Falsification condition | Plain text | "Governments abandon reshoring and return to global supply chains" |
| Initial lifecycle state | Always fixed | `narrative.lifecycle.emerging` |

### Step 5: Validate Explanation Chain (Section 12)

Confirm the new narrative satisfies the No Dead Ends Guarantee:
- Reachable FROM at least one State_Change (upward path exists)
- Connected TO at least one System (downward path exists)

If either condition fails, the narrative is not valid for canonical inclusion.

---

## How to Read the Lifecycle State Machine (Section 6)

The lifecycle state machine describes how narratives evolve over time. Here is how to interpret it.

### The 6 States

Every canonical narrative exists in exactly one of these states at any given time:

```
narrative.lifecycle.emerging        → New belief gaining initial believers
narrative.lifecycle.strengthening   → Growing consensus, accelerating adoption
narrative.lifecycle.dominant        → Widely accepted, peak positioning
narrative.lifecycle.weakening       → Contradicting evidence, some participants exiting
narrative.lifecycle.dormant         → No longer driving flows, not fully invalidated
narrative.lifecycle.dead            → Fully invalidated, no believers remain
```

### The 7 Transitions (T1–T7)

Transitions move a narrative from one state to another. The key rules:

- **Every transition is triggered by a State_Change** — never by a signal, score, or time alone
- **No numeric thresholds** — there is no "reaches score 0.7 → transitions to Dominant"
- **Signals detect transitions; they do not cause them** — if you see a signal firing, that is observation, not causation

The transition graph flows:

```
[Birth] → Emerging → Strengthening → Dominant → Weakening → Dormant
                                                    ↓
                                                   Dead
                                    Dormant → Emerging (Revival)
```

### Velocity (Observational Only)

Velocity describes how quickly a narrative's lifecycle is progressing:
- **Accelerating** — belief adoption/erosion speeding up
- **Steady** — stable rate of change
- **Decelerating** — momentum slowing

**Critical constraint**: Velocity is an observational annotation ONLY. It is:
- NOT a Temporal_Taxonomy extension
- NOT a lifecycle transition trigger
- NOT a ranking input or score proxy

### Reading a Narrative's Current State

To determine what a narrative's lifecycle state means practically:
1. Find the narrative's current state (one of the 6 canonical states)
2. Read the transition triggers for the NEXT valid transitions from that state
3. Ask: "Has a State_Change occurred that matches any of those triggers?"
4. If yes → the narrative may be transitioning. If no → it remains in current state.

---

## How to Use Cross-References for Traversal (Section 17)

The Narrative Framework v2 does not exist in isolation. It connects to 6 other Layer 0 deliverables through a formal cross-reference system. Understanding this system lets you traverse between documents efficiently.

### The Cross-Reference Format

Every reference in the document uses this pattern:

```
(See: [Deliverable_Name], Section: [Section_Title])
```

Examples:
- `(See: README_market_organism_principles, Section: Principle 4 — Feedback is Structural)`
- `(See: README_temporal_taxonomy, Section: Feedback_Delay)`
- `(See: README_explanation_framework, Section: Explanation Levels)`

### How to Follow a Cross-Reference

1. **Identify the deliverable** — The first part after `See:` tells you which document to open. All Layer 0 deliverables are in the `docs/` directory with the pattern `docs/README_[name].md`.
2. **Find the section** — The second part after `Section:` tells you exactly which heading to navigate to within that document.
3. **Read in context** — The cross-reference provides authoritative detail that the Narrative Framework intentionally does not duplicate.

### The Cross-Reference Index (Section 17)

Section 17 provides a complete table of ALL external references used throughout the document. Use it as:
- A **dependency map** — which documents does the Narrative Framework depend on?
- A **lookup table** — where in this document is each external deliverable referenced?
- A **verification tool** — every `(See: ...)` in the body must appear in Section 17

### Key Traversal Paths

| If You Need To Understand... | Follow This Path |
|------------------------------|-----------------|
| How State_Changes are classified | (See: README_state_change_taxonomy, Section: Classification Hierarchy) |
| How `dep.narrative` works as a mechanism | (See: README_dependency_types_v2, Section: Narrative) |
| How feedback loops are temporal | (See: README_temporal_taxonomy, Section: Feedback_Delay) |
| How explanation levels connect | (See: README_explanation_framework, Section: Explanation Levels) |
| Why display text is never identity | (See: README_language_rendering_framework, Section: Rule 4 — Display Text is Never Identity) |
| What the Exclusion Constraints align with | (See: README_market_organism_principles, Section: Exclusion Constraints) |

---

## How to Verify Compliance with Exclusion Constraints (Section 15)

The Exclusion Constraints define 8 things the Narrative Framework explicitly prohibits. Any artifact, implementation, or extension that touches narrative ontology must comply with these constraints.

### The 8 Exclusion Constraints

| EC# | Prohibition | What to Check For |
|-----|-------------|-------------------|
| EC-1 | Engine implementations | No Python code, executable logic, or engine behavior referencing narrative primitives |
| EC-2 | Scoring algorithms | No numeric weights, probabilities, ranking systems, or confidence scores applied to narratives |
| EC-3 | Dashboard specifications | No dashboard designs or visualization specs that treat narratives as scoreable entities |
| EC-4 | Asset lists as root entities | No asset lists or ticker symbols used as organizational roots for narrative structures |
| EC-5 | Correlation matrices | No statistical co-movement measures between narratives or narrative members |
| EC-6 | Recommendation/optimization logic | No recommendation engines, portfolio allocation, or optimization using narrative membership |
| EC-7 | Numeric lifecycle thresholds | No numeric threshold values (e.g., "score > 0.7") used as lifecycle transition triggers |
| EC-8 | Numeric membership weights | No numeric weights (e.g., "strong=3, moderate=2, weak=1") for narrative membership influence |

### Compliance Verification Checklist

When verifying that an artifact complies with the Narrative Framework's exclusion constraints, ask these questions:

1. **Does it introduce numeric scoring for narratives?** → Violates EC-2, EC-8
2. **Does it use thresholds to trigger lifecycle transitions?** → Violates EC-7
3. **Does it convert categorical labels to ordinal numbers?** → Violates EC-8
4. **Does it recommend assets based on narrative membership?** → Violates EC-6
5. **Does it compute correlations between narrative members?** → Violates EC-5
6. **Does it treat asset lists as the starting point rather than State_Changes?** → Violates EC-4
7. **Does it specify how a dashboard should render narrative data?** → Violates EC-3
8. **Does it implement runtime behavior that executes narrative logic?** → Violates EC-1

### The Unified Rationale

All 8 constraints share one rationale: **Weights on an incomplete model produce false confidence.** The Narrative Framework defines WHAT a narrative IS ontologically. Numeric precision belongs to future implementation phases that will build upon this foundation — not within the foundation itself.

### Consistency Check

The Narrative Framework's Exclusion Constraints are derived from and consistent with Market Organism Exclusion Constraints (Req 8.1–8.7). If your work touches both frameworks, verify against both sets of constraints.

(See: README_market_organism_principles, Section: Exclusion Constraints)

---

## Relationship to Other Documents

| Document | Relationship to This Guide |
|----------|---------------------------|
| `docs/README_narrative_framework.md` | **The SSOT.** This guide helps you USE that document. |
| `.kiro/specs/narrative-framework-alignment/requirements.md` | The requirements that drove the v2 alignment. |
| `.kiro/specs/narrative-framework-alignment/design.md` | The design decisions behind the v2 structure. |
| `.domainization/reports/narrative_framework_alignment_*.md` | Execution reports documenting how the alignment was performed. |

---

## Summary

- The Narrative Framework v2 (`docs/README_narrative_framework.md`) is the single source of truth for narrative ontology.
- This guide is supplementary — it helps you work with the SSOT, not replace it.
- When in doubt, the Narrative Framework v2 document wins. Always.
