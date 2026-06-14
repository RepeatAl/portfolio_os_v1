# README: Source Authority Matrix

> **Artifact**: `source_authority_matrix.md`
> **Spec**: peer-group-production-registry-creation
> **Audience**: Humans and AI agents operating on this spec

---

## What This Artifact Defines

The Source Authority Matrix classifies every governing document referenced by the peer-group-production-registry-creation spec. It answers one question for each source: **what governance power does this document have over the production registry?**

Every document referenced in the design falls into exactly one of seven authority types:
- Controlling
- Methodology authority
- Terminology authority
- Governance authority
- Boundary authority
- Downstream compatibility authority
- Context only

## What This Artifact Does NOT Do

- It does NOT create registry content
- It does NOT mint canonical peer_group_id values
- It does NOT approve candidate records
- It does NOT execute any production operation
- It does NOT grant new authority to any source — it documents existing authority

---

## Why PGMF Is the Sole Methodology Authority

The Peer Group Methodology Framework (PGMF) is the **only** source authorized to define:
- How peer group families are structured
- What subclusters exist within each family
- How peer roles are assigned
- What comparability criteria apply
- How field rules translate decisions into registry fields

No other document — not the readiness review, not the system architecture, not any downstream framework — may override PGMF methodology decisions. This is by design:

1. **Single point of truth**: If multiple sources could define methodology, conflicts would be unresolvable.
2. **Separation of concerns**: Controlling sources decide WHAT goes into the registry. PGMF decides HOW it is structured.
3. **Auditability**: Any methodology question traces to exactly one source.

If PGMF does not define a methodology rule, that rule does not exist. No agent or process may infer methodology from other sources.

---

## Controlling vs. Context-Only Sources

### Controlling Sources

Controlling sources have **binding governance power**. Their decisions:
- Are non-negotiable
- Must be carried forward into the production registry
- Can block production activation if violated
- Require explicit human/CTO approval to override (which has never been granted)

In this spec, there are exactly two controlling sources:
1. The Production Registry Readiness Review (establishes conditions and prerequisites)
2. The P1–P4 Decision Records (19 owner-verified decisions that are binding)

### Context-Only Sources

Context-only sources have **zero governance power**. They:
- Provide background information
- May be read for understanding
- Must NOT be cited as authority for any decision
- Cannot constrain, authorize, or block any registry operation

In this spec, there are exactly two context-only sources:
1. The Preflight Spec (completed historical phase — informational only)
2. The Future Framework Backlog (planned future capabilities — no current authority)

### The Critical Difference

A controlling source says: "The registry MUST contain X."
A context-only source says: "Here is some background about Y." (No governance implication.)

An agent that treats a context-only source as controlling will produce unauthorized content. An agent that treats a controlling source as context-only will miss mandatory requirements.

---

## Adding a Source Without CTO Approval Is Prohibited

The extension governance rule is absolute:

> **No source may be added to the authority matrix without explicit CTO approval recorded with approver identity and date.**

This means:
- An AI agent cannot decide to reference a new document and grant it governance power
- A spec author cannot silently add a source to justify a decision
- No automated process may expand the authority matrix

Violations of this rule constitute a governance breach that invalidates any downstream work based on the unauthorized source.

### Why This Rule Exists

The authority matrix is the foundation of all spec tasks. If sources can be added without governance:
1. Scope creep becomes invisible
2. Conflicting authorities emerge
3. Audit trails break
4. The registry loses institutional integrity

---

## For AI Agents

When operating on tasks under this spec:
1. Check the source authority matrix before citing any document as justification
2. If a document is classified as "context only," do not use it to authorize decisions
3. If you need to reference a document not in the matrix, STOP and flag for CTO review
4. PGMF is your sole methodology reference — do not derive methodology from other sources
5. Controlling decisions from P1–P4 records are binding — do not reinterpret them

---

## Boundary Confirmations

- [x] This README explains the source authority model
- [x] PGMF sole methodology authority explained
- [x] Controlling vs. context-only distinction documented
- [x] CTO approval requirement for new sources stated
- [x] No registry content created by this artifact

---

*End of README.*
