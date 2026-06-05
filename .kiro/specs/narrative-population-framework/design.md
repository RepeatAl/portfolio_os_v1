# Design Document — Narrative Population Framework

## Overview

This design defines the structure for the first controlled registry population of the Narrative Registry within Portfolio OS.

### Design Authority

- **Narrative Framework v2** (`docs/README_narrative_framework.md`) = ontology SSOT — defines WHAT a narrative IS
- **Narrative Registry** (`docs/registries/narrative_registry.yaml` + governance README) = schema/governance SSOT — defines HOW narratives are registered
- **Market Evidence Framework** (`docs/README_market_evidence_framework.md`) = evidence SSOT — defines HOW factual support is organized and consumed
- **This design** = defines the structural approach for WHICH narratives may be proposed and HOW the population pipeline operates

### Critical Boundary

- **No registry mutation is authorized by design creation.** This document is a structural blueprint only.
- Actual narrative entries are only created in a later explicitly approved task phase.
- The `narratives: []` list in the Narrative Registry remains empty throughout requirements AND design phases.
- Any candidate IDs referenced herein are PROPOSED/CANDIDATE status only — they are NOT canonical until human-approved registration.

(See: README_narrative_framework, Section: 4. What Is a Narrative?)
(See: README_narrative_registry_governance, Section: Creation Procedure)
(See: README_market_evidence_framework, Section: 23. Consumer Contracts)

---

## Architecture

### Population Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ DESIGN/PLANNING PHASE (Steps 1-4)                                           │
│                                                                             │
│ Step 1: Candidate Review                                                    │
│   → Evaluate preflight candidates against 11 inclusion gates                │
│   → Document gate passage/failure per candidate                             │
│                                                                             │
│ Step 2: Field Preparation                                                   │
│   → Prepare all required fields per candidate (template-based)              │
│   → Assign candidate IDs (PROPOSED status only)                             │
│                                                                             │
│ Step 3: Evidence Justification                                              │
│   → Document Market Evidence support per candidate                          │
│   → Reference facts, signals, evidence containers                           │
│   → Perform contradiction review                                            │
│                                                                             │
│ Step 4: Human Approval                                                      │
│   → Present prepared candidates for human review                            │
│   → Obtain explicit sign-off on scope, ID, falsification per candidate      │
│   → Confirm Wave 1 size and composition                                     │
└─────────────────────────────────────────────────────────────────────────────┘


```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FUTURE TASK EXECUTION PHASE (Steps 5-7) — NOT AUTHORIZED BY THIS DESIGN     │
│                                                                             │
│ Step 5: Pre-Mutation Verification                                           │
│   → Run all VG-POP gates                                                    │
│   → Confirm no prohibited fields, no collisions, no asset-first             │
│   → Verify schema compatibility with narrative_registry.yaml                │
│                                                                             │
│ Step 6: Registry Append                                                     │
│   → Append approved entries to narratives: [] list                          │
│   → Commit with execution report                                            │
│   → No schema change, no governance change                                  │
│                                                                             │
│ Step 7: Post-Mutation Verification                                          │
│   → Verify registry integrity after append                                  │
│   → Confirm no unintended changes                                           │
│   → Produce final verification artifact                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase Boundary

| Phase | Steps | Authority | Registry Impact |
|-------|-------|-----------|----------------|
| Design/Planning | 1-4 | This design document | NONE — registry unchanged |
| Task Execution | 5-7 | Future authorized tasks.md | Append entries to `narratives: []` |

**This design document covers Steps 1-4 ONLY.** Steps 5-7 are documented structurally for completeness but are NOT authorized until an explicit task phase is approved.

---

## Components and Interfaces

### Status: WAVE 1 HUMAN-APPROVED (3 candidates)

Wave 1 composition has been approved by the Portfolio Architect. The following classifications reflect human decisions captured in the Human Decisions Captured section.

### Wave 1 APPROVED (Human-Approved for Task Planning)

| # | Candidate Label | Proposed ID | Status |
|---|----------------|-------------|--------|
| 1 | AI Infrastructure | `narrative.ai_infrastructure` | APPROVED for Wave 1 task planning — PROPOSED until registration |
| 2 | Defense Rearmament | `narrative.defense_rearmament` | APPROVED for Wave 1 task planning — PROPOSED until registration |
| 3 | GLP-1 / Obesity Medicine | `narrative.glp1_obesity_medicine` | APPROVED for Wave 1 task planning — PROPOSED until registration |

**Note**: These IDs are approved for task planning only. They become canonical ONLY when registry mutation is explicitly executed in the authorized task phase.

### Wave 1 NOT APPROVED — Deferred

| # | Candidate Label | Decision | Disposition |
|---|----------------|----------|-------------|
| 4 | Energy Infrastructure / Grid Expansion | NOT approved for Wave 1 | Moved to needs_refinement/backlog. Await AI Infrastructure registration before evaluating overlap boundary. Do NOT merge into AI Infrastructure. |
| 5 | Cybersecurity / Security Infrastructure | NOT approved for Wave 1 | Moved to backlog for later wave consideration. |

### Needs Refinement (Not Yet Wave 1 Ready)

| # | Candidate Label | Issue | Path to Resolution |
|---|----------------|-------|-------------------|
| 1 | Energy Infrastructure / Grid Expansion | Deferred from Wave 1; overlap with AI Infrastructure boundary unclear | Re-evaluate after AI Infrastructure is registered |
| 2 | AI Semiconductors | NOT in Wave 1. Possible future sub-narrative or system-level exposure under AI Infrastructure. Do not register independently. | Boundary decision deferred |
| 3 | Cloud AI | May be a system (`system.cloud_compute`), not a narrative | Reconceptualization needed |
| 4 | Maritime / Logistics | Scope too broad, needs triggering event isolation | Scope narrowing required |
| 5 | Consumer Re-acceleration | No clear State_Change birth trigger identified | Trigger identification needed |

### Backlog (Premature or Insufficient Evidence)

| # | Candidate Label | Reason for Deferral |
|---|----------------|-------------------|
| 1 | Cybersecurity / Security Infrastructure | Deferred from Wave 1; later wave candidate |
| 2 | Payments / Money Rails | Insufficient narrative-shaping evidence; may be a system domain |
| 3 | Space Economy / Private Space Infrastructure | Premature for canonical status; emerging but unproven shared belief |
| 4 | Humanoid Robotics / Physical AI | Too early; narrative not yet widely shared; limited evidence base |

### Rejected (Currently Not Narrative-Shaped)

| # | Candidate Label | Rejection Reason | Reconceptualization Required |
|---|----------------|-----------------|------------------------------|
| 1 | WM / QSR / Delivery | Portfolio category, not shared belief structure. Fails inclusion criterion 1 (distinct shared belief) and criterion 4 (asset-list-first). | Must demonstrate shared belief origin independent of portfolio construction |
| 2 | Enterprise Software | Sector label, not narrative. Fails inclusion criterion 1 (distinct shared belief). No identifiable State_Change origin. | Must identify a specific State_Change that makes "enterprise software" a narrative rather than a sector classification |

### Task-Generation Guard

**Future `tasks.md` may ONLY prepare entries for the 3 approved Wave 1 candidates:**
- AI Infrastructure
- Defense Rearmament
- GLP-1 / Obesity Medicine

**tasks.md MUST NOT prepare entries for:**
- Energy Infrastructure / Grid Expansion
- Cybersecurity / Security Infrastructure
- AI Semiconductors
- Cloud AI
- Maritime / Logistics
- Consumer Re-acceleration
- Payments / Money Rails
- Space Economy / Private Space Infrastructure
- Humanoid Robotics / Physical AI
- WM / QSR / Delivery
- Enterprise Software

---

## Wave 1 Decision Model

### Decisions — Human-Resolved

Human decisions have been captured (see Human Decisions Captured section). The following table reflects current status:

| # | Decision | Resolution | Status |
|---|----------|-----------|--------|
| 1 | Wave 1 size | **3 narratives** | ✅ RESOLVED |
| 2 | Candidate inclusion set | **AI Infrastructure, Defense Rearmament, GLP-1 / Obesity Medicine** | ✅ RESOLVED |
| 3 | AI Infra vs AI Semi boundary | **AI Semiconductors excluded from Wave 1; future sub-narrative evaluation** | ✅ RESOLVED |
| 4 | Energy overlap with AI | **Energy Infrastructure deferred to needs_refinement/backlog** | ✅ RESOLVED |
| 5 | Lifecycle approach | **All `narrative.lifecycle.emerging` with lifecycle history note** | ✅ RESOLVED |
| 6 | Canonical ID naming approval | **IDs approved for task planning (proposed until mutation)** | ✅ RESOLVED |
| 7 | Falsification condition approval | **Drafts may be prepared; final approval required before mutation** | ⚠️ PARTIALLY RESOLVED |

### Decision Process (Completed Steps)

1. ✅ Design prepared candidate field templates
2. ✅ Human reviewed prepared materials
3. ✅ Human made binding decisions on items 1-6
4. ⚠️ Item 7 (falsification) requires final approval before task phase executes
5. → `tasks.md` may now be created for the 3 approved Wave 1 candidates


---

## Data Models

### Status: TEMPLATE ONLY — NOT A REGISTRY ENTRY

The following is a reusable field preparation template. It defines the structure that each candidate must have populated BEFORE registry mutation can occur. **This template does NOT create, register, or authorize any narrative entry.**

```yaml
# ============================================================
# CANDIDATE FIELD TEMPLATE — PROPOSED STATUS ONLY
# This is NOT a registry entry. It becomes one ONLY after:
#   1. All fields populated
#   2. All inclusion gates passed
#   3. Human approval obtained
#   4. Task phase execution authorized
# ============================================================

candidate_label: "<Human-readable label from preflight>"
proposed_narrative_id: "narrative.<proposed_snake_case_id>"  # CANDIDATE — not canonical until registered
display_name: "<Short display name for human consumption>"

scope_definition: |
  <Natural language description of what this narrative encompasses.
   Must define boundaries clearly enough to distinguish from adjacent narratives.
   Must NOT reference asset tickers as primary justification.>

birth_trigger: |
  state_change_reference: "sc.<proposed_trigger_id>"  # CANDIDATE reference
  description: "<Specific, past-tense event that catalyzed this narrative>"
  approximate_date: "<YYYY-MM or YYYY-MM-DD>"

connected_systems:
  - "system.<system_id_1>"  # At least one required
  - "system.<system_id_2>"  # Additional connections

falsification_condition: |
  <Concrete, testable condition that would invalidate this narrative.
   Must be specific enough that an observer could determine truth/falsehood.
   Example: "If X occurs within Y timeframe, this narrative is invalidated.">

lifecycle_state: "narrative.lifecycle.emerging"  # Default; human may override
registered_date_policy: "Set at registration time (task phase), not design time"
registered_by: "human:<approver_id>"  # Human who approves final registration
last_modified_policy: "Set at registration time, updated on any future mutation"

evidence_summary: |
  <Brief summary of Market Evidence Framework support.
   References to facts, signals, evidence containers.
   NOT the evidence itself — just pointers to where evidence lives.>

contradiction_review: |
  <Any contradicting evidence documented here.
   Must be present even if conclusion is "no material contradiction found.">

human_approval_status: "PENDING"  # → APPROVED only after human sign-off
backlog_or_reject_reason: null  # Only populated for non-Wave-1 candidates
```

### Template Usage Rules

1. One template instance is prepared per Wave 1 candidate during design/planning phase
2. Template instances are CANDIDATE documents — NOT registry entries
3. The `proposed_narrative_id` becomes canonical ONLY upon human-approved registration
4. Fields marked "policy" indicate HOW the value will be set, not the value itself
5. Template instances may be revised unlimited times before human approval
6. No template instance may be converted to a registry entry without explicit task-phase authorization

---

## Evidence Justification Format

### Purpose

Every candidate that reaches human review must be accompanied by an evidence justification document. This document references Market Evidence Framework elements WITHOUT creating any new evidence objects.

### Evidence Justification Structure

For each Wave 1 candidate, the following evidence summary must be prepared:

```yaml
# ============================================================
# EVIDENCE JUSTIFICATION — REFERENCE ONLY
# This does NOT create facts, signals, or evidence objects.
# It REFERENCES existing or future Market Evidence Framework content.
# ============================================================

candidate_label: "<Candidate name>"

observed_facts_summary: |
  <Summary of observable, verifiable facts supporting this narrative's existence.
   Source: Market Evidence Framework Layer 1 (Observed Facts).
   Must reference identifiable real-world events, data points, or disclosures.>

calculated_signals_summary: |
  <Summary of interpreted/calculated signals where applicable.
   Source: Market Evidence Framework Layer 2 (Calculated Signals).
   May be marked "N/A — no calculated signals required for initial justification.">

evidence_container_reference: |
  <Reference to where full evidence documentation will live.
   Format: "evidence_container.<proposed_id>" (CANDIDATE reference only)
   Or: "evidence summary provided inline — no separate container required">

provenance_readiness: |
  <Assessment of evidence source quality.
   At minimum: source identity, observation date range, data freshness.
   References Market Evidence Framework Section 27 (Provenance).>

contradiction_review: |
  <Explicit documentation of any evidence that CONTRADICTS this candidate.
   Must be present for every candidate.
   "No material contradiction identified" is acceptable with justification.
   References Market Evidence Framework Section 21 (Contradiction).>

evidence_limitations: |
  <Honest assessment of evidence gaps or weaknesses.
   What evidence is NOT yet available? What assumptions are being made?
   This prevents over-confidence in justification quality.>

credit_solvency_relevance: |
  <Assessment of whether this candidate requires credit/solvency evidence.
   For macro-thematic narratives: "Not applicable — narrative operates at
   thematic level, not company-specific valuation level."
   For company-specific candidates: Full credit/solvency review required.>

valuation_trap_guard_status: |
  <Confirmation that this candidate is NOT derived from:
   - Asset price performance alone
   - Low valuation multiples alone
   - Portfolio basket construction
   Status: CLEAR / REQUIRES_REVIEW / FLAGGED>
```

### Rules

1. Evidence justifications are REFERENCE documents — they do NOT create Market Evidence objects
2. No `observed_fact.*`, `signal.*`, or `evidence_container.*` objects are created by this spec
3. Evidence justifications inform human decision-making but do NOT auto-approve candidates
4. Contradiction review is MANDATORY — cannot be skipped even for strong candidates
5. Evidence limitations must be honestly documented — over-confidence is a governance risk

(See: README_market_evidence_framework, Section: 23. Consumer Contracts)
(See: README_market_evidence_framework, Section: 4. Evidence Is Not Narrative)
(See: README_market_evidence_framework, Section: 6. Evidence Production Rules)


---

## Credit / Solvency / Valuation Trap Integration

### Purpose

This section defines how credit, solvency, and valuation trap considerations integrate with the candidate evaluation process. It ensures that no narrative is registered based solely on low valuations without proper solvency context.

### Core Principles

1. **Low valuation is not automatically undervaluation.** The market may correctly price default risk, refinancing risk, pension burden, or balance sheet impairment.

2. **Company-specific or valuation-sensitive candidates** must review credit/solvency evidence before being justified. This includes:
   - Cashflow sustainability
   - Liquidity position
   - Pension and lease obligations
   - Off-balance-sheet commitments
   - LBO/sponsor leverage
   - Refinancing risk timeline

3. **Credit ratings are evidence inputs, not final truth.** They are Observed_Facts in the Market Evidence Framework — useful context but not authoritative conclusions within this spec.

4. **No default probability model, no credit score, no buy/sell recommendation** is authorized by this spec or any deliverable thereof.

5. **Macro-thematic narratives may mark credit/solvency as "not applicable"** with documented justification. Example: "AI Infrastructure operates at the thematic level — individual company credit risk does not invalidate or validate the narrative itself."

### Application Matrix

| Candidate Type | Credit/Solvency Required? | Justification |
|---------------|--------------------------|---------------|
| Macro-thematic (AI Infra, Defense, Energy) | No — mark "not applicable" | Narrative is about shared belief, not company valuation |
| Company-specific | YES — full review | Company quality directly relevant to narrative validity |
| Valuation-driven | YES — full review | Low multiples without solvency = potential value trap |
| Sector-level with company exemplars | Partial — note boundary | Narrative-level evidence ≠ company-level evidence |

### Integration with Evidence Justification

The `credit_solvency_relevance` field in the Evidence Justification Format (Section 6) captures this assessment per candidate. For Wave 1 candidates:

- **AI Infrastructure**: Not applicable — macro-thematic
- **Defense Rearmament**: Not applicable — macro-thematic (geopolitical driver)
- **Energy Infrastructure / Grid Expansion**: Not applicable at narrative level; note that individual energy company credit ≠ narrative evidence
- **Cybersecurity / Security Infrastructure**: Not applicable — macro-thematic
- **GLP-1 / Obesity Medicine**: Not applicable — scientific breakthrough narrative; individual pharma company credit ≠ narrative validity

### Valuation Trap Guard Rule

> "No narrative may be justified solely by low valuation multiples without solvency context."

This guard prevents:
- Registering "undervalued industrials" as a narrative (valuation ≠ narrative)
- Confusing cheap stocks with shared market beliefs
- Ignoring legitimate reasons for low prices (debt, declining cashflow, secular decline)

(See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)
(See: README_market_evidence_framework, Section: 31. Valuation Trap Boundary)

---

## Collision Check Design

### Purpose

Before any candidate is registered, it must pass a collision check to ensure it does not overlap with existing entries or other candidates in the same wave. This prevents semantic duplication and maintains registry integrity.

### Collision Check Procedure

#### 8.1 Exact ID Collision Check

- Verify that `proposed_narrative_id` does not already exist in `narratives: []`
- For Wave 1 (first population), this check is trivially satisfied (registry is empty)
- For future waves, this becomes a hard gate

#### 8.2 Semantic Overlap Check

- Compare each candidate's `scope_definition` against all other candidates
- Identify areas where two candidates describe substantially the same shared belief
- Flag candidates whose falsification conditions would trigger simultaneously

#### 8.3 Parent-Child / Sub-Narrative Possibility

- If two candidates overlap but one is clearly a subset of the other:
  - Consider declaring parent-child relationship
  - Consider registering only the parent in Wave 1 and deferring the child
  - Document the relationship for future reference

#### 8.4 Merge / Defer / Reject Outcomes

| Outcome | When Applied | Action |
|---------|-------------|--------|
| PASS | No collision detected | Proceed to registration |
| MERGE | Two candidates describe same narrative differently | Combine into single entry with broader scope |
| DEFER | Candidate is sub-narrative of another Wave 1 entry | Move to backlog with parent reference |
| REJECT | Candidate is duplicate of existing entry | Reject with documented collision evidence |

#### 8.5 Special Check: AI Infrastructure vs AI Semiconductors vs Cloud AI

This is the highest-risk collision area in the current candidate set:

| Pair | Risk | Design Position |
|------|------|----------------|
| AI Infrastructure vs AI Semiconductors | HIGH — may be parent-child | Recommend: AI Semi excluded from Wave 1; boundary decision deferred to human |
| AI Infrastructure vs Cloud AI | MEDIUM — Cloud AI may be a system | Recommend: Cloud AI reclassified as `system.cloud_compute`, not narrative |
| AI Semiconductors vs Cloud AI | LOW — different domains | No collision if both excluded from Wave 1 |

**Human Decision Required:** The AI Infrastructure boundary is the single most important collision decision for Wave 1. The design recommends excluding AI Semiconductors from Wave 1 and treating it as a potential sub-narrative for future evaluation.

#### 8.6 Special Check: Energy Infrastructure vs AI Infrastructure

| Overlap Area | Analysis |
|-------------|----------|
| Data center power demand | Shared connection point — but different narratives |
| Grid modernization for AI | Energy narrative driven by broader infrastructure need, not AI alone |
| Recommended approach | Separate narratives; note `connected_systems` overlap; no parent-child |

**Design Position:** Energy Infrastructure and AI Infrastructure are separate narratives with a shared connection point (power demand). They should be registered separately with documented awareness of their intersection.

(See: README_narrative_registry_governance, Section: Collision Check Procedure)

---

## Backlog and Rejection Design

### Purpose

Not all candidates qualify for Wave 1. This section defines the governance model for candidates that are deferred or rejected, ensuring they are properly documented and can be re-evaluated in future waves.

### Classification Definitions

#### 9.1 Needs Refinement (`needs_refinement`)

**Definition:** Candidate has narrative potential but scope, trigger, or evidence issues prevent Wave 1 inclusion.

**Characteristics:**
- May have valid shared belief structure
- Scope definition needs narrowing or boundary clarification
- Birth trigger not yet precisely identified
- May overlap with another candidate (collision unresolved)

**Path Forward:**
- May return to Wave 1 consideration if scope issues are resolved before task phase
- Refinement may occur during design phase review
- Human may promote directly if they judge issues are resolvable

**Current Candidates:**
- AI Semiconductors (overlap with AI Infrastructure)
- Cloud AI (may be system, not narrative)
- Maritime / Logistics (scope too broad)
- Consumer Re-acceleration (no clear birth trigger)

#### 9.2 Backlog (`backlog`)

**Definition:** Candidate is premature or has insufficient evidence for canonical registration at this time. Deferred with documented reason.

**Characteristics:**
- Shared belief may exist but is not yet widely held
- Evidence base is insufficient for justification
- Narrative may be too early in formation
- Not rejected — explicitly preserved for future evaluation

**Re-evaluation Criteria:**
- New State_Change event provides clearer birth trigger
- Evidence base grows to meet Market Evidence requirements
- Shared belief becomes more widely held and identifiable
- Related narratives are registered, creating context for this candidate

**Current Candidates:**
- Payments / Money Rails (insufficient narrative-shaping evidence)
- Space Economy / Private Space Infrastructure (premature)
- Humanoid Robotics / Physical AI (too early, limited evidence)

#### 9.3 Rejected (`rejected_as_not_narrative_shaped`)

**Definition:** Candidate fundamentally fails to meet the definition of a narrative. It is a portfolio category, sector label, or other non-narrative construct.

**Characteristics:**
- Fails inclusion criterion 1 (distinct shared belief) at a fundamental level
- Cannot be fixed by scope narrowing alone
- Requires reconceptualization from first principles
- Is NOT in the backlog — it is excluded until fundamentally rethought

**Reconceptualization Required:**
- Must demonstrate shared belief origin independent of portfolio construction
- Must identify a specific State_Change that creates the narrative
- Must show it is NOT a relabeled sector classification or portfolio basket
- Must pass ALL 11 inclusion gates after reconceptualization

**Current Candidates:**
- WM / QSR / Delivery (portfolio category)
- Enterprise Software (sector label)

### Re-evaluation Governance

| Status | Can Return to Wave 1? | Required For Return |
|--------|----------------------|---------------------|
| needs_refinement | YES — during design phase | Scope/trigger issues resolved |
| backlog | YES — in future waves | New evidence or State_Change event |
| rejected | Only after reconceptualization | Fundamental rethinking + all 11 gates |


---

## Registry Mutation Design

### Purpose

This section defines the structural rules governing HOW the Narrative Registry will be mutated during the future task execution phase. It establishes boundaries that prevent unauthorized, incomplete, or structurally invalid mutations.

### Mutation Scope

| Allowed | Prohibited |
|---------|-----------|
| Append entries to `narratives: []` list | Schema modification |
| Set all required fields per entry | Governance rule modification |
| Set `registered_date` at mutation time | Changes to `retired_narratives` |
| Set `registered_by` to approving human | Adding prohibited fields |
| Set `last_modified` at mutation time | Adding asset-level fields |
| | Adding scoring/ranking/probability/confidence fields |
| | Modifying any non-`narratives` section |
| | Removing or modifying existing entries (none exist yet) |

### Mutation Rules

1. **Append-only operation:** The task phase may ONLY append new entries to the `narratives: []` list. No other registry section is modified.

2. **Complete entries only:** No partial entries may be appended. ALL required fields must be populated at mutation time.

3. **Human-approved entries only:** Every entry appended must have documented human approval for ALL fields (scope, ID, falsification, systems, trigger).

4. **Execution report mandatory:** Every mutation must be committed alongside an execution report documenting:
   - What entries were added
   - Who approved them
   - What verification gates passed
   - Timestamp of mutation

5. **Registry remains unchanged during design phase:** The `narratives: []` list remains empty until the authorized task phase executes. This design document produces ZERO registry changes.

### Mutation Sequence (Future Task Phase)

```
1. Load current narrative_registry.yaml
2. Verify narratives: [] is empty (first population)
3. Prepare entries from human-approved candidate templates
4. Run pre-mutation VG-POP gates (Section 11)
5. Append entries to narratives: []
6. Write updated narrative_registry.yaml
7. Run post-mutation VG-POP gates (Section 11)
8. Generate execution report
9. Commit with descriptive message
```

### What This Design Does NOT Do

- Does NOT execute Steps 1-9 above
- Does NOT modify `narrative_registry.yaml`
- Does NOT add any entries to `narratives: []`
- Does NOT set any `registered_date` values
- Does NOT finalize any `narrative_id` values
- The registry remains EXACTLY as it was before this design was created

---

## Correctness Properties

### Property 1: Registry Immutability During Design

The `narratives: []` list in `docs/registries/narrative_registry.yaml` must remain empty throughout requirements and design phases. Verified by inspecting the registry file after design completion.

**Validates: Requirements 7.3, 7.5**

### Property 2: Candidate-Only Language

All narrative references in design deliverables use "candidate" or "proposed" prefix. No final canonical `narrative.*` ID is declared before human approval. Verified by text search for unqualified `narrative.*` declarations.

**Validates: Requirements 5.3, 6.3**

### Property 3: Inclusion Criteria Conjunctivity

Every Wave 1 candidate must satisfy ALL 11 evaluation gates simultaneously. Failure on ANY single gate disqualifies the candidate. Verified by gate checklist execution per candidate.

**Validates: Requirements 2.4, 1.2**

### Property 4: Evidence-Before-Registration

No candidate may be registered without documented Market Evidence justification. Evidence must reference observed facts, provenance, and contradiction review. Verified by evidence justification document inspection.

**Validates: Requirements 3.1, 11.2**

### Property 5: No Asset-First Contamination

No registered narrative may be derived from asset lists, portfolio baskets, or statistical co-movement. Every narrative must trace to a shared belief with State_Change origin. Verified by reviewing each candidate's derivation path.

**Validates: Requirements 4.1, 4.2**

### Property 6: Human Approval Completeness

Every registered entry must have documented human approval for scope, canonical ID, falsification condition, connected systems, and birth trigger. Verified by approval record inspection.

**Validates: Requirements 6.1, 6.2**

### Property 7: No SSOT Mutation

Narrative Framework v2, Market Organism Layer 0, central glossary, and Market Evidence Framework remain unchanged after population. Only `narratives: []` is modified. Verified by diff against main.

**Validates: Requirements 7.1, 8.1**

### Verification Gate Mapping

| Gate ID | Gate Name | Check Description | Phase |
|---------|-----------|-------------------|-------|
| VG-POP-1 | No Design-Phase Registry Mutation | Verify `narratives: []` remains empty after requirements and design phases complete. No entries added during planning. | Pre-mutation |
| VG-POP-2 | Candidate-Only Language | Verify all candidate references use "candidate" or "proposed" prefix. No deliverable declares a final canonical ID before human approval. | Pre-mutation |
| VG-POP-3 | Inclusion Criteria Completeness | Verify every entry being registered satisfies ALL 4 inclusion criteria (shared belief, falsifiable, State_Change connected, system connected) with documented evidence per gate. | Pre-mutation |
| VG-POP-4 | Market Evidence Readiness | Verify evidence justification is cited per candidate. Provenance referenced. Contradiction review completed. Market Evidence Framework consumption documented. | Pre-mutation |
| VG-POP-5 | No Asset-First Contamination | Verify no candidate was derived from asset lists, portfolio baskets, sector ETFs, or statistical co-movement patterns. Primitive chain preserved. | Pre-mutation |
| VG-POP-6 | No Scoring/Ranking/Probability | Verify zero numeric scores, weights, probabilities, confidence values, or hidden ranking systems appear in any deliverable or registry entry. | Pre-mutation |
| VG-POP-7 | State_Change Linkage | Verify every candidate has an identified `sc.*` birth trigger — a specific, past-tense event that catalyzed the narrative. | Pre-mutation |
| VG-POP-8 | System Linkage | Verify every candidate has at least one `system.*` in `connected_systems`. Systems are accepted on trust (no system registry yet). | Pre-mutation |
| VG-POP-9 | Falsification | Verify every candidate has a concrete, testable falsification condition. Condition must be specific enough for an observer to determine truth/falsehood. | Pre-mutation |
| VG-POP-10 | Human Approval | Verify documented evidence that a human approved each candidate's scope, canonical ID, falsification condition, connected systems, and birth trigger. | Pre-mutation |
| VG-POP-11 | Registry Compatibility | Verify every entry complies with `narrative_registry.yaml` schema. All required fields present. No prohibited fields. Valid YAML structure. | Pre-mutation |
| VG-POP-12 | Collision Check | Verify no two entries overlap semantically without a declared parent-child relationship. AI Infra/AI Semi boundary confirmed. Energy/AI overlap confirmed. | Pre-mutation |
| VG-POP-13 | Credit/Solvency Guard | Verify valuation-sensitive candidates have solvency evidence or explicit "not applicable" waiver with justification. No narrative justified solely by low multiples. | Pre-mutation |
| VG-POP-14 | No SSOT Mutation | Verify Narrative Framework v2, Market Organism Layer 0, central glossary, and Market Evidence Framework documents are unchanged. Only `narratives: []` was modified. | Post-mutation |

### Gate Execution Timing

```
┌──────────────────────────────────────────────────┐
│ PRE-MUTATION GATES (VG-POP-1 through VG-POP-13)  │
│ Run BEFORE any entry is appended to registry     │
│ ALL must pass — failure blocks mutation           │
└──────────────────────────────────────────────────┘
                        │
                        ▼
              [Registry Mutation]
                        │
                        ▼
┌──────────────────────────────────────────────────┐
│ POST-MUTATION GATE (VG-POP-14)                   │
│ Run AFTER entries appended                       │
│ Confirms no collateral damage                    │
└──────────────────────────────────────────────────┘
```

### Gate Failure Policy

- If ANY pre-mutation gate fails: mutation is BLOCKED. No entries are appended.
- If post-mutation gate fails: ROLLBACK required. Revert registry to pre-mutation state.
- All gate results are documented in the execution report.
- Gate failures are reported to human for resolution before retry.


---

## Error Handling

### Gate Failure Handling

- If ANY pre-mutation verification gate fails: registry mutation is BLOCKED. No entries are appended. Failure is reported to human with specific gate ID and failure reason.
- If post-mutation gate (VG-POP-14) fails: ROLLBACK required. Revert `narrative_registry.yaml` to pre-mutation state. Report to human.
- Gate failures during design/planning phase (VG-POP-1, VG-POP-2): stop and report — do not proceed to task phase.

### Collision Detection Handling

- If exact ID collision detected: REJECT candidate immediately. Cannot proceed.
- If semantic overlap detected: flag for human review. Human decides: merge, defer, or redefine scope.
- If unresolvable overlap: both candidates are deferred until human provides boundary decision.

### Evidence Insufficiency Handling

- If evidence is insufficient for a candidate: mark `evidence_readiness: insufficient` and move candidate to backlog.
- Do NOT proceed with registration if evidence gaps cannot be documented and justified.
- Contradiction evidence that cannot be resolved: flag for human — do not suppress.

### Ambiguity Policy

- If ambiguity exists in scope, trigger, or classification: flag explicitly. Do NOT resolve silently.
- Create a blocker note in the execution report.
- Human must resolve before registration can proceed.

---

## Testing Strategy

### Verification Approach

This spec produces documentation and governance artifacts — not executable code. Therefore, traditional unit/integration testing does not apply. Verification is structural:

1. **Document inspection** — verify all required sections and fields are present
2. **Gate checklist execution** — run VG-POP-1 through VG-POP-14 as verification gates
3. **Schema compliance** — verify candidate entries match `narrative_registry.yaml` schema
4. **Cross-reference validation** — verify all `(See: ...)` references point to existing documents
5. **Collision check execution** — verify no semantic overlap between Wave 1 candidates

### Property-Based Testing Applicability

PBT does NOT apply to this feature. The deliverable is a governance-controlled registry population — not executable code with inputs/outputs. There are no algorithms, parsers, or business logic functions to test with generated inputs. Verification is structural: required fields present, prohibited fields absent, gates passed, human approvals documented.

---

## Requirement Traceability

### Purpose

This section maps every requirement (NPF-REQ-1 through NPF-REQ-12) to the design sections that satisfy it, ensuring complete coverage with no orphaned requirements.

### Traceability Matrix

| Requirement | Title | Design Section(s) | Coverage |
|-------------|-------|-------------------|----------|
| NPF-REQ-1 | Population Boundary | Section 2 (Population Architecture), Section 3 (Candidate Classification Model), Section 4 (Wave 1 Decision Model) | Wave 1 size 3-5, inclusion gate enforcement, candidate listing, design ≠ authorization |
| NPF-REQ-2 | Candidate Evaluation Model | Section 3 (Candidate Classification Model), Section 5 (Candidate Field Template), Section 8 (Collision Check Design) | 11 gates conjunctive, documented evidence per gate, collision handling |
| NPF-REQ-3 | Evidence Requirement | Section 6 (Evidence Justification Format), Section 7 (Credit/Solvency/Valuation Trap Integration) | Facts, signals, containers referenced; provenance; contradiction review; credit/solvency |
| NPF-REQ-4 | No Asset-First Population | Section 3 (Candidate Classification Model — rejection criteria), Section 6 (Evidence Justification — valuation_trap_guard_status), Section 11 (VG-POP-5) | Asset-first prohibition enforced at classification, evidence, and verification levels |
| NPF-REQ-5 | Candidate Field Preparation | Section 5 (Candidate Field Template) | All required and optional fields defined; candidate status declared; no partial entries |
| NPF-REQ-6 | Human Review Gate | Section 4 (Wave 1 Decision Model), Section 13 (Open Human Decisions) | 10 explicit human decisions; approval required per candidate per field |
| NPF-REQ-7 | Registry Mutation Control | Section 2 (Population Architecture — phase boundary), Section 10 (Registry Mutation Design) | Append-only; task-phase-only; execution report; design = zero mutation |
| NPF-REQ-8 | Verification Before Population | Section 11 (Verification Strategy) | 14 VG-POP gates mapped; pre-mutation blocking; post-mutation rollback |
| NPF-REQ-9 | Backlog Handling | Section 9 (Backlog and Rejection Design) | Three statuses defined; re-evaluation criteria; reconceptualization for rejected |
| NPF-REQ-10 | Future Asset-to-Narrative Readiness | Section 5 (Candidate Field Template — stable ID design), Section 10 (Registry Mutation Design — no asset fields) | narrative_id as foreign key; connected_systems as list; no asset-level fields |
| NPF-REQ-11 | Market Evidence Compatibility | Section 6 (Evidence Justification Format) | Evidence hierarchy consumption; provenance; contradiction; no auto-registration; no evidence object mutation |
| NPF-REQ-12 | Credit/Solvency Evidence Awareness | Section 7 (Credit/Solvency/Valuation Trap Integration) | Low valuation ≠ undervaluation; credit as input; no models/scores/recommendations; guard rule |

### Coverage Summary

- **12/12 requirements** have at least one design section providing structural coverage
- **0 orphaned requirements** — every NPF-REQ has a traceable design response
- **0 design sections without requirement backing** — every section traces to at least one requirement

---

## Human Decisions Captured

**Date**: 2026-06-04
**Authority**: Portfolio Architect (CTO)
**Status**: Decisions 1-6 RESOLVED. Decision 7 PARTIALLY RESOLVED.

### Decision 1 — Wave 1 Size

**RESOLVED**: Wave 1 size = **3 narratives**.

### Decision 2 — Wave 1 Candidate Inclusion Set

**RESOLVED**:
- ✅ **APPROVED for Wave 1**: AI Infrastructure, Defense Rearmament, GLP-1 / Obesity Medicine
- ❌ **NOT approved for Wave 1**: Energy Infrastructure / Grid Expansion, Cybersecurity / Security Infrastructure

### Decision 3 — AI Infrastructure vs AI Semiconductors Boundary

**RESOLVED**:
- AI Semiconductors is NOT included in Wave 1
- Treat as a possible future sub-narrative or system-level exposure under AI Infrastructure
- Do not register AI Semiconductors independently in Wave 1

### Decision 4 — Energy Infrastructure Overlap Boundary

**RESOLVED**:
- Energy Infrastructure / Grid Expansion is NOT included in Wave 1
- Keep as needs_refinement/backlog until AI Infrastructure is registered and energy boundary is clearer
- Do NOT merge into AI Infrastructure
- Do NOT register as a separate narrative in Wave 1

### Decision 5 — Lifecycle Approach

**RESOLVED**:
- All Wave 1 entries use `narrative.lifecycle.emerging` as initial canonical registry state
- Each Wave 1 entry must include or reference a lifecycle history note: *"Registered as initial canonical state despite existing market maturity; lifecycle history predates registry."*
- Do NOT backdate lifecycle transitions in Wave 1

### Decision 6 — Candidate ID Naming Approval

**RESOLVED** (for task planning; become canonical only at registry mutation):
- `narrative.ai_infrastructure` — APPROVED for task planning
- `narrative.defense_rearmament` — APPROVED for task planning
- `narrative.glp1_obesity_medicine` — APPROVED for task planning

### Decision 7 — Falsification Condition Approval

**PARTIALLY RESOLVED**:
- Detailed candidate-specific falsification conditions are NOT finalized
- `tasks.md` may prepare falsification DRAFTS per candidate
- Final human approval is required before any registry mutation can proceed

---

## Open Human Decisions

### Current Status

Decisions 1-6 are RESOLVED. One item remains before registry mutation is authorized.

### Remaining Decision

| # | Decision | Status | Blocking? |
|---|----------|--------|-----------|
| 7 | Falsification condition approval per candidate | ⚠️ PARTIALLY RESOLVED — drafts needed | YES — blocks registry mutation |

### What Remains Before tasks.md → Registry Mutation

1. `tasks.md` prepares falsification condition drafts for the 3 approved candidates
2. Human reviews and approves each falsification condition
3. ONLY after falsification approval does registry mutation proceed

### What is NOW Unblocked

- `tasks.md` creation for the 3 approved Wave 1 candidates
- Candidate field template population (AI Infrastructure, Defense Rearmament, GLP-1)
- Evidence justification documentation per candidate
- Falsification draft preparation (for human review, not for immediate mutation)

---

## Cross-References

| Target Deliverable | Section Referenced | Context |
|-------------------|-------------------|---------|
| README_narrative_framework | Section 4: What Is a Narrative? | Narrative ontology definition |
| README_narrative_framework | Section 6: Lifecycle State Machine | Valid lifecycle states |
| README_narrative_framework | Section 13: Extension Criteria | Inclusion criteria gates |
| README_narrative_registry_governance | Creation Procedure | How entries are added |
| README_narrative_registry_governance | Collision Check Procedure | Overlap detection |
| README_narrative_registry_governance | Cross-References | Foreign key readiness |
| README_market_evidence_framework | Section 4: Evidence Is Not Narrative | Boundary between evidence and narrative |
| README_market_evidence_framework | Section 6: Evidence Production Rules | How evidence is created (not by this spec) |
| README_market_evidence_framework | Section 21: Contradiction | Contradiction review requirements |
| README_market_evidence_framework | Section 23: Consumer Contracts | How consumers reference evidence |
| README_market_evidence_framework | Section 27: Provenance | Source quality requirements |
| README_market_evidence_framework | Section 30: Credit, Solvency, and Balance Sheet Evidence | Credit/solvency integration |
| README_market_evidence_framework | Section 31: Valuation Trap Boundary | Guard against value-trap narratives |
| README_market_organism_principles | Principle 2: Taxonomy Precedes Assets | Primitive chain invariant |
| requirements.md (this spec) | All sections | Requirements traceability |

---

## Document Metadata

| Field | Value |
|-------|-------|
| Spec | narrative-population-framework |
| Phase | Design |
| Status | HUMAN-APPROVED (Wave 1 decisions captured) — ready for tasks.md |
| Branch | `spec/narrative-population-framework` |
| Created | 2026-06-04 |
| Author | Kiro (design generation) |
| Authority | CTO / Portfolio Architect |
| Registry Impact | NONE — design produces zero mutation |
| Next Step | tasks.md creation for 3 approved Wave 1 candidates (after falsification drafts prepared) |
