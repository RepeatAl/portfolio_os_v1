# Narrative Framework

---
artifact_id: narrative_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-06-02
owner_role: Defines the ontology of Narrative as a primitive in the MoneyHorst architecture
ssot_relationship: canonical
topic: narrative_ontology
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism.principles_md, dependency_types_v2_md, temporal_taxonomy_md, expansion_taxonomy_md, explanation_framework_md, language_rendering_framework_md]
version: v2
alignment_spec: narrative-framework-alignment
---

## 1. Scope Statement

This document defines the Narrative ontology as a formal primitive in the Market Organism architecture. Narrative occupies the second position in the canonical primitive chain (`State_Change → Narrative → System → Asset`) and serves as the explanatory container that organizes how a State_Change's effects are understood by market participants.

This is a **definition-layer document**. It declares WHAT a Narrative is, how it relates to other primitives, and what rules govern its lifecycle and membership — nothing more.

For consolidated prohibitions on what this document does NOT contain and does NOT authorize, see Section 15: Exclusion Constraints.

**Explicit exclusions**: This document does NOT contain data, engines, scores, implementation details, or runtime behavior. It does not populate registries, execute algorithms, produce dashboards, assign numeric weights, calculate probabilities, or recommend portfolio allocations.

## 2. Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary
(See: README_shared_glossary_reference, Section: Glossary Usage Rules)

This document does not define terms except for the three amendments below.

### Glossary Amendments

| Term | Definition | Status |
|------|-----------|--------|
| Narrative_Container | The structural role of a Narrative as the explanatory grouping that organizes how a State_Change's effects are understood by market participants. Distinguished from `dep.narrative`, which is the propagation mechanism — not the container itself. | CANONICAL |
| Narrative_Membership | The relationship between an Asset and a Narrative, classified by membership type (primary/secondary/emerging/legacy) and qualitative influence descriptor (strong/moderate/weak). These are categorical labels, not ordinal numeric proxies. | CANONICAL |
| Narrative_Interaction | A causal relationship between a State_Change and a Narrative, classified by interaction type (Creates/Strengthens/Weakens/Kills/Revives). State_Changes cause interactions; signals detect their effects. | CANONICAL |

**Disambiguation — Narrative_Container vs `dep.narrative`:**
- **Narrative_Container** refers to the structural ENTITY — the explanatory grouping under which assets are organized. It is a primitive in the chain (`State_Change → Narrative → System → Asset`).
- **`dep.narrative`** refers to the Dependency_Type — a propagation MECHANISM through shared belief. It is one of 10 equal Dependency_Types and does not have special authority over other propagation mechanisms simply because it shares the word "Narrative."

These are orthogonal concepts that happen to share the word "Narrative." A State_Change may propagate THROUGH `dep.narrative` (mechanism) INTO a Narrative_Container (entity). The mechanism and the container are not the same thing.
(See: README_dependency_types_v2, Section: Narrative)

**Governance note**: These amendments are formalized locally inside Narrative Framework v2 for the purpose of this alignment. Updating the central Market Organism glossary (`.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary) is not performed by this spec unless separately authorized by a future governance task. The glossary-first rule remains intact — these terms are defined here before use, and will be proposed for central inclusion as a follow-up action.

## 3. The Primitive Chain

The Market Organism architecture is organized around a canonical primitive chain that defines the causal ordering of all analysis:

```
State_Change → Narrative → System → Asset
```

This chain is not a pipeline or a data flow — it is the ontological ordering of cause and effect. Every analytical traversal moves from left to right: from root cause to observable endpoint.

### Primitive Responsibilities

| Primitive | Position | Responsibility | Question Answered |
|-----------|----------|---------------|-------------------|
| State_Change | Root (1st) | Root cause — the originating event or regime shift that enters the system | "What happened?" |
| Narrative | 2nd | Explanatory container — the shared belief structure that organizes how market participants interpret the State_Change | "Why does it matter? What do participants believe?" |
| System | 3rd | Affected functional domain — the operational or structural system impacted by the narrative's explanatory frame | "Which systems are affected?" |
| Asset | Leaf (4th) | Observable endpoint — the security or instrument where effects ultimately manifest in price or flow | "Which assets are affected?" |

**Invariants:**
- State_Change is ALWAYS the root cause. No other primitive may be promoted to causal root.
- Narrative is ALWAYS the explanatory container. It does not cause; it organizes understanding.
- System is ALWAYS the affected functional domain. It is not conflated with Narrative.
- Asset is ALWAYS the leaf node. It is never root, never causal, never the starting point of analysis.

### Taxonomy-Before-Assets Principle

The primitive chain enforces a strict analytical ordering: classify the change FIRST (State_Change), understand the belief (Narrative), identify the system (System), THEN identify assets (Asset). Analysis never begins from assets and works backward.

This is the **taxonomy-before-assets** principle: the classification hierarchy is mandatory and inviolable. No system may begin reasoning from an asset and work backward to infer a State_Change. Assets are always leaf nodes — endpoints of a causal chain, never origins.

**Violation**: Any design, engine, or analytical process that starts with an asset (ticker, security, position) and attempts to derive or infer the originating State_Change from asset behavior violates this principle.

(See: README_market_organism_principles, Section: Principle 2 — Taxonomy Precedes Assets)

### Position in the Explanation Chain

Narrative occupies Level 4 in the explanation chain, answering the question "Because of which narratives?" This position connects upward to Level 3 (State_Changes — "What caused this?") and downward to Level 5 (Expansion paths — "How does it spread?"). Every canonical narrative must be reachable from at least one State_Change and must connect to at least one System — no dead ends permitted.

(See: README_explanation_framework, Section: Explanation Levels)


## 4. What Is a Narrative? (Definition and Formal Properties)

### Formal Definition

A **Narrative** is an explanatory container — a shared belief structure held by market participants that organizes how a State_Change's effects are understood, interpreted, and acted upon. It is the second primitive in the canonical chain (`State_Change → Narrative → System → Asset`) and answers the question: "Why does it matter? What do participants believe?"

A Narrative does not cause anything. It does not originate events, trigger signals, or generate data. It is the *organizing frame* through which a population of market participants collectively interprets a root-cause State_Change and channels capital accordingly.

**Key ontological properties:**

- A Narrative is always CAUSED by at least one State_Change — it never self-generates.
- A Narrative CONTAINS assets through membership relationships — it is the grouping mechanism.
- A Narrative CONNECTS to at least one System — no dead ends are permitted.
- A Narrative has a LIFECYCLE — it emerges, strengthens, dominates, weakens, goes dormant, or dies.
- A Narrative is FALSIFIABLE — contradicting evidence can invalidate it.

### Canonical ID Format

Every canonical narrative carries a stable, language-independent identifier using the `narrative.*` namespace.

```
Pattern: narrative.[descriptive_token]
```

**Token Rules:**

| # | Rule | Description |
|---|------|-------------|
| 1 | Lowercase only | All characters in the descriptive token must be lowercase |
| 2 | Underscore-separated | Multi-word tokens use underscores as word separators |
| 3 | Language-neutral | English descriptive tokens are canonical codes, not display text |
| 4 | Stable once assigned | Renaming display text does NOT change the canonical ID |

The namespace is flat — hierarchical depth is expressed through naming convention, not through nested IDs. All narratives, regardless of their position in a meta-narrative/sub-narrative hierarchy, occupy the same `narrative.*` namespace.

### Assignment Rules

New canonical narrative IDs must satisfy all of the following assignment rules:

| # | Rule | Rationale |
|---|------|-----------|
| 1 | Unique within namespace | No collisions — each `narrative.*` ID maps to exactly one narrative |
| 2 | Descriptive of the belief structure | Tokens describe the shared belief, not opaque codes (e.g., `narrative.ai_infrastructure` not `narrative.nar_0042`) |
| 3 | Language-neutral | English tokens function as canonical codes, not as English-language display text |
| 4 | Stable once assigned | Immutable after first use in any canonical document — the ID is a permanent key |

Once a `narrative.*` ID is assigned and used in any canonical document, it MUST NOT be changed, reassigned, or recycled. If a narrative's display text is updated in any language, the canonical ID remains unchanged.

If a narrative is referenced in any canonical document, it SHALL carry a `narrative.*` ID from the moment of first reference.

### Rendering Independence Declaration

> Display text in any language is rendering — never identity.
> Renaming a narrative's display text does NOT change its canonical ID.

A narrative's canonical identity is its `narrative.*` ID. All human-readable names — in any language — are renderings of that identity. The rendering may change; the identity is permanent.

**Example (illustrative only, not canonical registry entries, not asset registry population, not system registry population):**

| Canonical ID | English Rendering | German Rendering | Status |
|-------------|-------------------|------------------|--------|
| `narrative.ai_infrastructure` | "AI Infrastructure" | "KI-Infrastruktur" | Same narrative |
| `narrative.higher_for_longer` | "Higher for Longer" | "Höher für Länger" | Same narrative |

Both renderings refer to the same canonical identity. Changing the English display text from "AI Infrastructure" to "AI Compute Infrastructure" does NOT create a new narrative — the canonical ID `narrative.ai_infrastructure` remains unchanged.

(See: README_language_rendering_framework, Section: Rule 4 — Display Text is Never Identity)

### Illustrative Examples

The following examples demonstrate the canonical ID format in practice. These are **illustrative only, not canonical registry entries, not asset registry population, not system registry population.**

```
narrative.ai_infrastructure        — belief that AI requires massive infrastructure buildout
narrative.higher_for_longer        — belief that interest rates will remain elevated
narrative.defense_rearmament       — belief that global defense spending will increase structurally
narrative.compute_sovereignty      — belief that nations will pursue domestic compute capacity
narrative.ai_transformation        — meta-narrative: belief that AI transforms economic structure
```

These examples exist solely to demonstrate the ID format and token rules. They do NOT populate any registry, do NOT create asset memberships, and do NOT establish canonical truth about which narratives exist in the system.

### Qualitative Descriptors Declaration

Narrative membership and influence use qualitative categorical labels:

- **Membership types**: primary, secondary, emerging, legacy
- **Influence descriptors**: strong, moderate, weak

These are **categorical labels — not ordinal numeric proxies.** They classify relationships into discrete categories. They do not imply a numeric scale, do not permit arithmetic operations, and do not authorize conversion to scores.

Converting categorical labels to numbers (e.g., strong=3, moderate=2, weak=1) is explicitly prohibited. These descriptors enable human reasoning about narrative structure — they are not inputs to computation.


## 5. Narrative vs. State_Change

### The Distinction

Narrative and State_Change are both primitives in the canonical chain (`State_Change → Narrative → System → Asset`), but they serve fundamentally different ontological roles:

| Primitive | Role | Question Answered | Ontological Function |
|-----------|------|-------------------|---------------------|
| State_Change | CAUSE | "What happened?" | The originating event or regime shift that enters the system |
| Narrative | CONTAINER | "Why does it matter? What do participants believe?" | The explanatory grouping that organizes how a State_Change's effects are understood |

A **State_Change** is what triggered the belief. A **Narrative** is what the belief is about.

State_Changes CREATE narratives. Narratives do NOT create State_Changes.

### Causality Direction Declaration

The causal arrow between State_Change and Narrative is **unidirectional and irreversible**:

```
State_Change ──causes──▶ Narrative
```

The following invariants govern this relationship:

1. **State_Change remains the causal root.** No Narrative may be promoted to causal root under any circumstance. A Narrative is always the EFFECT of a State_Change — never its cause.

2. **Narratives do not cause State_Changes.** A narrative may be widely believed, dominant, and driving massive capital flows — but it does not originate events. Events originate narratives.

3. **Narratives organize understanding; they do not generate facts.** A narrative is the shared interpretive frame that market participants use to make sense of a State_Change. The frame does not produce the event it explains.

4. **Signals detect effects; they do not cause them.** A signal may observe evidence that a narrative is strengthening or weakening. The signal is a sensor — it reports what has already happened. It does not trigger narrative transitions. Only State_Changes trigger transitions. (See Section 14 for the full Signal Sensor Relationship Declaration.)

### Illustrative Example

The following example demonstrates the causality direction. It is **illustrative only** — it does not populate any registry, does not create canonical entries, and does not establish truth about which narratives or State_Changes exist in the system.

**Scenario**: Hyperscaler capex announcements

```
State_Change:  sc.corporate.capex.hyperscaler_increase
               (Nvidia announces $40B capex guidance for AI infrastructure)

This State_Change CREATES:
  narrative.ai_infrastructure
               (the shared belief that AI requires massive infrastructure buildout)
```

**Reading the causality correctly:**

- The capex announcement (State_Change) **caused** market participants to form and strengthen the belief (Narrative) that AI requires massive infrastructure investment.
- The narrative (belief about AI infrastructure) did **NOT** cause Nvidia to announce $40B in capex. The corporate decision preceded and produced the narrative — not the reverse.
- A signal (e.g., increased options volume on semiconductor ETFs) may **detect** that `narrative.ai_infrastructure` is strengthening. The signal does not cause the strengthening. The underlying State_Change caused it.

### Why This Matters

Confusing the container with the cause is the most common analytical error in narrative-based reasoning. If a Narrative is mistakenly treated as a causal root:

- The primitive chain collapses — analysis begins from a belief rather than from an event
- The taxonomy-before-assets principle is violated — classification starts from interpretation rather than fact
- Falsifiability is lost — beliefs without originating events cannot be invalidated by contradicting events

The distinction is not merely semantic. It preserves the analytical integrity of the entire primitive chain.

(See: README_market_organism_principles, Section: Principle 1 — Everything Connects)
