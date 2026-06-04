# Requirements Document: Narrative Population Framework

## 1. Purpose

This spec governs the first controlled population of the Narrative Registry. It answers the question: **"Which first narratives may officially exist in Portfolio OS?"**

This is a requirements-only document. It defines WHAT must be true before narratives can be registered. It does NOT authorize actual population — that occurs only in an explicitly authorized task phase after design approval.

**Authority hierarchy:**
- **Narrative Framework v2** (`docs/README_narrative_framework.md`) remains the ontology SSOT — defines WHAT a narrative IS
- **Narrative Registry Framework** (`docs/registries/narrative_registry.yaml` + governance README) remains the schema/governance SSOT — defines HOW narratives are registered
- **Market Evidence Framework** (`docs/README_market_evidence_framework.md`) defines evidence requirements — HOW factual support is organized and consumed
- **This spec** defines WHICH narratives may be proposed for first registration and UNDER WHAT CONDITIONS

(See: README_narrative_framework, Section: 4. What Is a Narrative?)
(See: README_narrative_registry_governance, Section: Creation Procedure)
(See: README_market_evidence_framework, Section: 23. Consumer Contracts)

---

## 2. Scope

### In Scope

- Wave 1 candidate selection rules
- Candidate evaluation model (inclusion criteria enforcement)
- Evidence requirement (Market Evidence consumption for candidate justification)
- State_Change birth trigger requirement (real identifiable events)
- Connected systems requirement (at least one `system.*`)
- Falsification condition requirement (concrete, testable)
- Human approval gate (every candidate requires explicit human sign-off)
- Registry mutation boundary (when and how mutation is authorized)
- Backlog handling (candidates not ready for Wave 1)
- Future Asset-to-Narrative readiness (schema compatibility)
- Market Evidence consumption requirements (facts, signals, evidence containers)
- Credit/solvency evidence awareness for valuation-sensitive candidates

### Out of Scope

| # | Exclusion | Rationale |
|---|-----------|-----------|
| 1 | Actual registry mutation during requirements phase | Mutation requires authorized task execution |
| 2 | Adding narrative entries to `narratives: []` | Not authorized until task phase |
| 3 | Asset-to-narrative mappings | Future separate spec |
| 4 | Facts/signals/evidence object creation | Market Evidence implementation concern |
| 5 | Evidence registry file creation | Not authorized by this spec |
| 6 | Engines or runtime code | Definition-layer spec |
| 7 | Validation scripts | Implementation concern |
| 8 | Dashboards | REPORT domain implementation |
| 9 | Scoring, ranking, probabilities, confidence values | Prohibited |
| 10 | Optimization or portfolio recommendations | Decision layer |
| 11 | Narrative Framework v2 mutation | Not authorized |
| 12 | Market Organism Layer 0 mutation | Not authorized |
| 13 | Central glossary mutation | Not authorized |
| 14 | Market Evidence Framework mutation | Not authorized by this spec |

---

## 3. Definitions / Glossary Policy

### Glossary Reference

All terms used in this document are defined in the canonical glossary unless amended below:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary
(See: README_shared_glossary_reference, Section: Glossary Usage Rules)

### Local Glossary Candidates

| Term | Definition | Status |
|------|-----------|--------|
| Wave_1 | The first controlled batch of narrative entries proposed for canonical registration in the Narrative Registry. Limited to 3-5 entries to validate the governance pipeline. | CANDIDATE |
| Candidate_Narrative | A proposed narrative under evaluation that has not yet passed all inclusion criteria gates or received human approval. It is NOT a canonical registry entry until registration. | CANDIDATE |
| Evidence_Justification | A structured reference to Market Evidence Framework elements (facts, signals, evidence containers) that supports or contradicts a candidate narrative's inclusion. | CANDIDATE |
| Valuation_Trap_Guard | The requirement that company-specific or valuation-sensitive narrative candidates must consume credit/solvency/balance-sheet evidence before being justified. | CANDIDATE |

### Glossary Policy

- Central glossary mutation is NOT authorized by this spec
- Existing Narrative Framework v2 and Market Evidence Framework terminology is used as-is
- New terms are local glossary candidates only
- Candidate narrative names are NOT canonical IDs until human approval AND registration
- The word "candidate" MUST precede any narrative reference that is not yet registered

---

## 4. Requirements

### NPF-REQ-1: Population Boundary

**User Story:** As a portfolio architect, I want explicit rules defining which narratives are authorized for Wave 1 registration, so that the first population is controlled, recoverable, and governance-compliant.

#### Acceptance Criteria

1. THE Population Framework SHALL define Wave 1 as the first controlled batch of 3-5 narrative entries
2. THE Population Framework SHALL require that every Wave 1 candidate passes ALL 4 inclusion criteria from Narrative Framework v2 Section 13
3. THE Population Framework SHALL explicitly list which candidates are proposed for Wave 1 and which are deferred to backlog
4. THE Population Framework SHALL declare that requirements alone do NOT authorize population — task-phase authorization is required
5. THE Population Framework SHALL declare that any candidate that fails a single inclusion criterion is excluded from Wave 1

---

### NPF-REQ-2: Candidate Evaluation Model

**User Story:** As a portfolio architect, I want a formal evaluation model defining the gates every candidate must pass, so that registration decisions are consistent and auditable.

#### Acceptance Criteria

1. THE Population Framework SHALL require every candidate to satisfy: (a) distinct shared belief, (b) falsifiable, (c) connected to real State_Change, (d) connected to at least one System
2. THE Population Framework SHALL additionally require: (e) not asset-list-first, (f) not portfolio-basket-first, (g) not duplicate/overlapping without declared parent-child, (h) not scoring/ranking/probability-based
3. THE Population Framework SHALL require: (i) evidence available or explicitly marked insufficient, (j) lifecycle state justified, (k) Market Evidence support available or marked insufficient
4. THE Population Framework SHALL declare that ALL gates are conjunctive — failure on ANY gate disqualifies the candidate from Wave 1
5. THE Population Framework SHALL require documented evidence for each gate passage per candidate

---

### NPF-REQ-3: Evidence Requirement

**User Story:** As a portfolio architect, I want every candidate narrative to be supported by Market Evidence Framework-compatible evidence, so that registration decisions are fact-based rather than opinion-based.

#### Acceptance Criteria

1. THE Population Framework SHALL require that every candidate entry references observed facts supporting its existence
2. THE Population Framework SHALL require that calculated/interpreted signals are cited where applicable
3. THE Population Framework SHALL require evidence containers or evidence summaries per candidate
4. THE Population Framework SHALL require provenance readiness assessment per candidate
5. THE Population Framework SHALL require contradiction review — any contradicting evidence must be documented alongside supporting evidence
6. THE Population Framework SHALL require credit/solvency/balance-sheet evidence where company valuation or company quality is relevant to the candidate narrative
7. THE Population Framework SHALL declare: "No narrative may be justified solely by asset price performance, portfolio basket construction, or low valuation multiples."

(See: README_market_evidence_framework, Section: 23. Consumer Contracts)
(See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)

---

### NPF-REQ-4: No Asset-First Population

**User Story:** As a portfolio architect, I want an explicit prohibition against deriving narratives from asset lists, so that the primitive chain invariant is preserved.

#### Acceptance Criteria

1. THE Population Framework SHALL prohibit deriving narrative candidates from asset lists, portfolio baskets, sector ETFs, or statistical co-movement patterns
2. THE Population Framework SHALL require that every candidate is derived from a shared market belief structure with an identifiable State_Change origin
3. THE Population Framework SHALL declare that the primitive chain (`State_Change → Narrative → System → Asset`) is inviolable — analysis never starts from assets
4. THE Population Framework SHALL reject any candidate whose scope definition references asset tickers as primary justification
5. THE Population Framework SHALL reject any candidate that is a relabeled portfolio category or sector classification

(See: README_market_organism_principles, Section: Principle 2 — Taxonomy Precedes Assets)
(See: README_narrative_framework, Section: 13. Narrative Extension Criteria)

---

### NPF-REQ-5: Candidate Field Preparation

**User Story:** As a portfolio architect, I want complete field preparation for every Wave 1 candidate before registration, so that no partial entries are created.

#### Acceptance Criteria

1. THE Population Framework SHALL require preparation of all required fields before registration: `narrative_id` (candidate), `scope_definition`, `birth_trigger`, `connected_systems`, `falsification_condition`, `lifecycle_state`, `registered_date` policy, `registered_by`, `last_modified`
2. THE Population Framework SHALL require optional field policy decisions: `display_name` (recommended), `evidence_summary` (recommended), `velocity` (optional), `expected_duration` (optional), `parent_narrative` (if hierarchy declared), `lifecycle_history` (empty initially)
3. THE Population Framework SHALL declare that `narrative_id` tokens are CANDIDATE status until human approval — they become immutable only upon registration
4. THE Population Framework SHALL declare that no partial entries may be registered — ALL required fields must be populated at registration time

---

### NPF-REQ-6: Human Review Gate

**User Story:** As a portfolio architect, I want explicit human approval requirements for every registration decision, so that no automated process can populate the registry without governance oversight.

#### Acceptance Criteria

1. THE Population Framework SHALL require human approval for Wave 1 size (3/4/5 entries)
2. THE Population Framework SHALL require human approval for each candidate's inclusion in Wave 1
3. THE Population Framework SHALL require human approval for each candidate's canonical `narrative_id`
4. THE Population Framework SHALL require human approval for each candidate's `scope_definition`
5. THE Population Framework SHALL require human approval for each candidate's `birth_trigger` State_Change
6. THE Population Framework SHALL require human approval for each candidate's `connected_systems`
7. THE Population Framework SHALL require human approval for each candidate's `falsification_condition`
8. THE Population Framework SHALL require human review of the AI Infrastructure vs AI Semiconductors boundary decision
9. THE Population Framework SHALL require human review of the Energy Infrastructure overlap boundary
10. THE Population Framework SHALL require human decision on lifecycle state approach for narratives that may already be past "emerging" in market reality

---

### NPF-REQ-7: Registry Mutation Control

**User Story:** As a portfolio architect, I want strict controls on when and how the Narrative Registry is mutated, so that unauthorized population cannot occur.

#### Acceptance Criteria

1. THE Population Framework SHALL declare that `docs/registries/narrative_registry.yaml` is mutated ONLY during an explicitly authorized task phase
2. THE Population Framework SHALL declare that mutation appends entries to the `narratives` list only — no schema modification, no governance modification
3. THE Population Framework SHALL declare that requirements and design phases produce NO registry mutation
4. THE Population Framework SHALL declare that every mutation is committed with an execution report documenting what was added
5. THE Population Framework SHALL declare that `narratives: []` remains empty until the authorized task phase executes

---

### NPF-REQ-8: Verification Before Population

**User Story:** As a portfolio architect, I want verification gates that confirm readiness before any population occurs, so that structural errors are caught before they enter the canonical registry.

#### Acceptance Criteria

1. THE Population Framework SHALL define verification gates that run BEFORE any registry mutation
2. THE Population Framework SHALL verify: no prohibited fields, valid `narrative.*` IDs, collision check passed, all required fields populated, no scoring/ranking/probability leakage
3. THE Population Framework SHALL verify: State_Change linkage readiness, System linkage readiness, falsification readiness
4. THE Population Framework SHALL verify: human approval documented, Market Evidence referenced, no asset-first contamination
5. THE Population Framework SHALL verify: Narrative Registry schema compatibility (entry matches registry schema)

---

### NPF-REQ-9: Backlog Handling

**User Story:** As a portfolio architect, I want clear backlog rules for candidates not ready for Wave 1, so that they are preserved for future evaluation without being lost or prematurely registered.

#### Acceptance Criteria

1. THE Population Framework SHALL define a backlog section for candidates that need refinement or are premature
2. THE Population Framework SHALL require documented reasons for backlog placement per candidate
3. THE Population Framework SHALL define re-evaluation criteria for backlog candidates
4. THE Population Framework SHALL declare that backlog candidates are NOT rejected — they are deferred with documented justification
5. THE Population Framework SHALL declare that rejected candidates (not narrative-shaped) are excluded from backlog — they require fundamental reconceptualization

---

### NPF-REQ-10: Future Asset-to-Narrative Readiness

**User Story:** As a portfolio architect, I want Wave 1 entries to be compatible with future Asset-to-Narrative Registry consumption, so that no breaking changes are needed later.

#### Acceptance Criteria

1. THE Population Framework SHALL ensure `narrative_id` is designed as a stable foreign key for future consumer reference
2. THE Population Framework SHALL ensure `lifecycle_state` is queryable by future consumers
3. THE Population Framework SHALL ensure `connected_systems` is a list (not single value) for future validation
4. THE Population Framework SHALL NOT include any asset-level fields in registered entries
5. THE Population Framework SHALL declare the boundary: narrative definitions HERE, asset-narrative relationships in future Asset-to-Narrative Registry

(See: README_narrative_registry_governance, Section: Cross-References)

---

### NPF-REQ-11: Market Evidence Compatibility

**User Story:** As a portfolio architect, I want the population process to be compatible with the Market Evidence Framework, so that evidence consumption is structured and traceable.

#### Acceptance Criteria

1. THE Population Framework SHALL declare Market Evidence Framework as a required input source for candidate justification
2. THE Population Framework SHALL require that evidence justification follows the Evidence Hierarchy (facts → signals → evidence containers)
3. THE Population Framework SHALL require that evidence provenance is cited per candidate
4. THE Population Framework SHALL require that contradiction evidence is documented alongside supporting evidence
5. THE Population Framework SHALL declare that evidence INFORMS registration decisions but does not AUTO-REGISTER candidates
6. THE Population Framework SHALL declare that no evidence object may directly mutate the Narrative Registry

(See: README_market_evidence_framework, Section: 4. Evidence Is Not Narrative)
(See: README_market_evidence_framework, Section: 6. Evidence Production Rules)

---

### NPF-REQ-12: Credit/Solvency Evidence Awareness

**User Story:** As a portfolio architect, I want valuation-sensitive or company-specific narrative candidates to consider credit and solvency evidence, so that value-trap narratives are not accidentally registered.

#### Acceptance Criteria

1. THE Population Framework SHALL declare that low valuation is not automatically undervaluation
2. THE Population Framework SHALL require that company-specific or valuation-sensitive narrative candidates consume credit, solvency, cashflow, liquidity, and obligation evidence where relevant
3. THE Population Framework SHALL declare that credit ratings are evidence inputs — not final truth
4. THE Population Framework SHALL prohibit default probability models, credit scores, or buy/sell recommendations within this spec
5. THE Population Framework SHALL reference Market Evidence Framework Section 30 and Section 31 for credit/solvency evidence requirements
6. THE Population Framework SHALL declare: "No narrative may be justified solely by low valuation multiples without solvency context."

(See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)
(See: README_market_evidence_framework, Section: 31. Valuation Trap Boundary)


---

## 5. Candidate Evaluation Model

### Required Gates (Conjunctive — ALL must pass)

| # | Gate | Source | Verification |
|---|------|--------|--------------|
| 1 | Distinct shared belief | Inclusion Criterion 1 | Does this represent a genuine shared market belief held by multiple participants? |
| 2 | Falsifiable | Inclusion Criterion 2 | Can a specific contradicting State_Change invalidate this narrative? |
| 3 | Connected to real State_Change | Inclusion Criterion 3 | Can you identify a specific, past-tense `sc.*` birth trigger? |
| 4 | Connected to at least one System | Inclusion Criterion 3 | Can you identify at least one `system.*` affected domain? |
| 5 | Not asset-list-first | EC-4, Principle 2 | Was this derived from a belief, not from a basket of stocks? |
| 6 | Not portfolio-basket-first | EC-4, Principle 2 | Is this NOT a relabeled portfolio category? |
| 7 | Not duplicate | Collision Check | Does this not overlap semantically with another candidate or existing entry? |
| 8 | Not scoring/ranking/probability-based | EC-2, NRF-REQ-9 | Does the definition avoid numeric strength or ranking language? |
| 9 | Evidence available | NPF-REQ-3 | Are observed facts and signals available to support this candidate? |
| 10 | Lifecycle state justified | NRF-REQ-6 | Is `narrative.lifecycle.emerging` correct, or is justification needed for a different initial state? |
| 11 | Market Evidence support | NPF-REQ-11 | Is Market Evidence Framework-compatible evidence available or explicitly marked insufficient? |

### Gate Application

Every Wave 1 candidate must be evaluated against ALL 11 gates. Results are documented per candidate in the design phase. Gate failures are documented with specific reasons. Partial gate passage does not qualify a candidate.

(See: README_narrative_framework, Section: 13. Narrative Extension Criteria)
(See: README_narrative_registry_governance, Section: Inclusion Criteria Gate)

---

## 6. Wave 1 Candidate Policy

### Preflight Input (Draft Classifications — NOT Final)

The following classifications are from the preflight assessment. They are requirements-input only — NOT registry entries, NOT approved candidates, NOT canonical IDs.

**Wave 1 Proposed:**
- AI Infrastructure
- Defense Rearmament
- Energy Infrastructure / Grid Expansion
- Cybersecurity / Security Infrastructure
- GLP-1 / Obesity Medicine

**Needs Refinement (not yet Wave 1 ready):**
- AI Semiconductors (overlap risk with AI Infrastructure)
- Cloud AI (may be a system, not a narrative)
- Maritime / Logistics (needs scope narrowing)
- Consumer Re-acceleration (needs triggering event)

**Backlog (premature or insufficient evidence):**
- Payments / Money Rails
- Space Economy / Private Space Infrastructure
- Humanoid Robotics / Physical AI

**Rejected as Currently Not Narrative-Shaped:**
- WM / QSR / Delivery (portfolio category, not shared belief)
- Enterprise Software (sector label, not narrative)

### Policy Declarations

1. These classifications are draft input from preflight reconnaissance — they are NOT final
2. Final Wave 1 composition is NOT approved by requirements alone — human review gate applies
3. Any candidate may be promoted, demoted, or rejected during design phase based on evidence review
4. Rejected candidates require fundamental reconceptualization to be reconsidered (not just minor refinement)
5. "Needs Refinement" candidates may be promoted to Wave 1 if scope issues are resolved before task phase

---

## 7. Market Evidence Requirement

### Evidence Justification Model

Every candidate that reaches the design phase must have evidence support referencing:

| Evidence Element | Required? | Source |
|-----------------|-----------|--------|
| Observed facts supporting birth trigger | YES | Market Evidence Framework Layer 1 |
| Calculated/interpreted signals where applicable | WHERE APPLICABLE | Market Evidence Framework Layer 2 |
| Evidence containers or evidence summaries | YES (at minimum a summary) | Market Evidence Framework Layer 3 |
| Provenance readiness | YES — at minimum source identity | Market Evidence Framework Section 27 |
| Contradiction review | YES — must document any contradicting evidence | Market Evidence Framework Section 21 |
| Credit/solvency/balance-sheet evidence | WHERE RELEVANT — for valuation-sensitive candidates | Market Evidence Framework Section 30 |

### Explicit Rule

> "No narrative may be justified solely by asset price performance, portfolio basket construction, or low valuation multiples."

This rule prevents the following anti-patterns:
- "NVDA went up 300% so AI Infrastructure is a narrative" (asset performance ≠ narrative truth)
- "My portfolio basket is called 'Defense' so defense is a narrative" (portfolio category ≠ narrative)
- "These stocks trade at low P/E so they must be a narrative" (valuation ≠ narrative)

---

## 8. Credit / Solvency / Valuation Trap Guard

### Core Rules

1. **Low valuation is not automatically undervaluation.** The market may correctly price default risk, refinancing risk, pension burden, or balance sheet impairment.

2. **Company-specific or valuation-sensitive narrative candidates** must consider credit, solvency, cashflow, liquidity, pension obligations, leases, off-balance-sheet commitments, and LBO/sponsor leverage where relevant.

3. **Credit ratings are evidence inputs, not final truth.** They are Observed_Facts in the Market Evidence Framework — not authoritative conclusions within this spec.

4. **No default probability model, credit score, or buy/sell recommendation** is authorized by this spec.

5. **This requirement references Market Evidence Framework** but does NOT create evidence objects, does NOT create signals, does NOT create facts.

### Application to Candidates

- Most Wave 1 candidates (AI Infrastructure, Defense Rearmament, GLP-1) are macro-thematic and do NOT require company-level credit assessment at the narrative level
- If a future candidate is company-specific or valuation-driven (e.g., "undervalued industrial conglomerate"), the Valuation Trap Guard MUST be applied
- Energy Infrastructure candidates should note that individual company credit risk does not invalidate the narrative — but company-level evidence should not be confused with narrative-level evidence

(See: README_market_evidence_framework, Section: 30. Credit, Solvency, and Balance Sheet Evidence)
(See: README_market_evidence_framework, Section: 31. Valuation Trap Boundary)

---

## 9. Gap Traceability

| Gap ID | Source | Risk | Severity | Requirement Mapping | Resolution Phase | Deferred? |
|--------|--------|------|----------|--------------------|-----------------|----|
| NPG-01 | No `system.*` registry to validate connected_systems | Invalid system references | MEDIUM | NPF-REQ-5 | Design | No — accept on trust |
| NPG-02 | Some candidates may already be past "emerging" lifecycle | Incorrect initial state | MEDIUM | NPF-REQ-6.10 | Design | No |
| NPG-03 | AI Infrastructure vs AI Semiconductors overlap | Collision check may flag both | HIGH | NPF-REQ-6.8 | Design (human decision) | No |
| NPG-04 | No precedent for Wave 1 — first population | Process untested | LOW | NPF-REQ-1 | Tasks | No |
| NPG-05 | Weak falsification criteria risk | Vague falsification = unfalsifiable | HIGH | NPF-REQ-2.1b, NPF-REQ-5 | Design | No |
| NPG-06 | Portfolio category contamination | Asset-list-first entries | HIGH | NPF-REQ-4 | Requirements (addressed) | No |
| NPG-07 | Birth trigger for older narratives may predate taxonomy | No canonical `sc.*` ID | MEDIUM | NPF-REQ-3, NPF-REQ-5 | Design | No |
| NPG-08 | Related_narratives empty in Wave 1 | Cannot cross-reference | LOW | NPF-REQ-5 | Tasks | No |
| NPG-09 | Velocity assessment requires human judgment | No algorithmic determination | LOW | NPF-REQ-5.2 | Design | No |
| NPG-10 | Meta-narrative hierarchy unclear | Parent may not exist yet | MEDIUM | NPF-REQ-5.2 | Design | No |
| NPG-11 | Market Evidence Framework not yet canonical on main | Draft status dependency | MEDIUM | NPF-REQ-11 | Requirements (consumed as draft) | No — consumed from branch |
| NPG-12 | Credit/solvency evidence required for valuation-sensitive narratives | Missing evidence may block candidates | LOW | NPF-REQ-12 | Design | No — addressed by guard rule |

---

## 10. Invariants

The following invariants MUST be preserved throughout all deliverables of this spec:

| # | Invariant | Source |
|---|-----------|--------|
| 1 | Narrative Framework v2 remains ontology SSOT | Authority hierarchy |
| 2 | Narrative Registry remains registry/governance SSOT | Authority hierarchy |
| 3 | Market Evidence Framework remains evidence SSOT | Authority hierarchy |
| 4 | Evidence informs registration but does not mutate registry | NPF-REQ-11, Market Evidence boundary |
| 5 | State_Change remains root/cause | Market Organism Principle 1, 2 |
| 6 | Signal remains sensor — detects, does not cause | Narrative Framework Section 14 |
| 7 | Narrative remains explanatory container — not cause, not sensor | Narrative Framework Section 4 |
| 8 | Registry mutation only occurs in explicitly authorized task phase | NPF-REQ-7 |
| 9 | No asset-to-narrative mappings | Out of Scope |
| 10 | No scoring, ranking, probabilities, confidence values, or hidden weights | Exclusion Constraints |
| 11 | No valuation shortcut from multiples to undervaluation | NPF-REQ-12, Valuation Trap Guard |
| 12 | No central glossary mutation | Glossary Policy |
| 13 | No Market Organism Layer 0 mutation | Out of Scope |
| 14 | Candidate IDs remain candidate/proposed until human-approved registration | NPF-REQ-5.3, NPF-REQ-6 |

---

## 11. Verification Gate Plan

| Gate ID | Gate Name | Checks |
|---------|-----------|--------|
| VG-POP-1 | No Requirements-Phase Registry Mutation | `narratives: []` still empty; no entries added during requirements/design |
| VG-POP-2 | Candidate-Only Language | All candidate references use "candidate" prefix; no final canonical IDs declared |
| VG-POP-3 | Inclusion Criteria Completeness | Every registered entry satisfies all 4 inclusion criteria with evidence |
| VG-POP-4 | Market Evidence Readiness | Evidence justification cited per candidate; provenance referenced |
| VG-POP-5 | No Asset-First Contamination | No candidate derived from asset lists or portfolio baskets |
| VG-POP-6 | No Scoring/Ranking/Probability | Zero numeric scores, weights, probabilities in any deliverable |
| VG-POP-7 | State_Change Linkage Readiness | Every candidate has identified `sc.*` birth trigger |
| VG-POP-8 | System Linkage Readiness | Every candidate has at least one `system.*` in connected_systems |
| VG-POP-9 | Falsification Readiness | Every candidate has concrete, testable falsification condition |
| VG-POP-10 | Human Approval Readiness | Evidence that human approved each candidate's scope, ID, falsification |
| VG-POP-11 | Narrative Registry Compatibility | Entries comply with registry schema; all required fields present |
| VG-POP-12 | Collision Check Readiness | No two entries overlap without declared parent-child relationship |
| VG-POP-13 | Credit/Solvency/Valuation Trap Guard | Valuation-sensitive candidates have solvency evidence or explicit waiver |
| VG-POP-14 | No SSOT Mutation | Narrative Framework v2, Market Organism Layer 0, central glossary unchanged |

---

## 12. Non-Goals

This requirements document does NOT authorize:

- Registry mutation (no entries added to `narratives: []`)
- Wave 1 approval (human review still required)
- Canonical narrative ID assignment (IDs remain candidate/proposed)
- Fact/signal/evidence object creation (Market Evidence implementation concern)
- Asset-to-narrative mapping (future separate spec)
- Design document creation (next phase, pending human review)
- Task list creation (after design)
- Engine, runtime, or code creation
- Modification of any existing SSOT

The next step (pending human review of these requirements) is to create `design.md` specifying HOW the first population will structurally satisfy these requirements.

---

## Cross-References

| Target Deliverable | Section Referenced | Context |
|-------------------|-------------------|---------|
| README_narrative_framework | Section 4: What Is a Narrative? | Narrative definition |
| README_narrative_framework | Section 6: Lifecycle State Machine | Valid lifecycle states |
| README_narrative_framework | Section 13: Extension Criteria | Inclusion criteria |
| README_narrative_framework | Section 14: Signal Sensor Relationship | Signal ≠ cause |
| README_narrative_framework | Section 15: Exclusion Constraints | Prohibited fields |
| README_market_organism_principles | Principle 1: Organism over Collection | Propagation, not correlation |
| README_market_organism_principles | Principle 2: Taxonomy Precedes Assets | No asset-first |
| README_market_organism_principles | Principle 6: Causation over Correlation | Causal mechanism required |
| README_narrative_registry_governance | Creation Procedure | Registration workflow |
| README_narrative_registry_governance | Collision Check Procedure | Overlap detection |
| README_narrative_registry_governance | Inclusion Criteria Gate | 4-criterion gate |
| README_market_evidence_framework | Section 4: Evidence Is Not Narrative | Evidence/narrative boundary |
| README_market_evidence_framework | Section 23: Consumer Contracts | Evidence consumption rules |
| README_market_evidence_framework | Section 30: Credit, Solvency, and Balance Sheet Evidence | Credit evidence |
| README_market_evidence_framework | Section 31: Valuation Trap Boundary | Valuation trap prevention |
| README_state_change_taxonomy | Classification Hierarchy | Birth trigger format |
| README_expansion_taxonomy | Expansion Definition | System connections |
| README_shared_glossary_reference | Glossary Usage Rules | Term definitions |
