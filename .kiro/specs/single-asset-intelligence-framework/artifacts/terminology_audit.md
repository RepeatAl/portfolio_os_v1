# Single Asset Intelligence Framework — Cross-Framework Terminology Audit

**Artifact**: terminology_audit.md
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH
**Phase**: Task Execution — Definition Layer Only
**Task**: 14.1 Create terminology audit artifact
**Requirements**: SAI-REQ-4 (Provenance Chain Requirement)
**Verification Gate**: VG-SAI-10 (Cross-Framework Consistency Gate)
**Status**: Draft

---

## 1. Source Lookup Performed

The following canonical framework sources were inspected for terminology comparison:

| # | Framework | File Path | Status |
|---|-----------|-----------|--------|
| 1 | Market Evidence Framework | `docs/README_market_evidence_framework.md` | Inspected |
| 2 | Narrative Framework v2 | `docs/README_narrative_framework.md` | Inspected |
| 3 | Market Organism Principles | `docs/market_organism/README_market_organism_principles.md` | Inspected |
| 4 | Shared Glossary Reference | `docs/market_organism/README_shared_glossary_reference.md` | Inspected |
| 5 | Canonical Glossary (SSOT) | `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary | Inspected |

---

## 2. SAI Terminology Inventory

The following terms are used within SAI framework artifacts and require cross-framework consistency verification:

| # | SAI Term | SAI Usage Context | Primary SAI Artifact(s) |
|---|----------|-------------------|------------------------|
| 1 | fact | Atomic evidence unit consumed by blocks | All artifacts, fact_consumption_matrix.md |
| 2 | signal | Derived/calculated value consumed by blocks | All artifacts, signal_consumption_matrix.md |
| 3 | evidence | Umbrella term for facts + signals consumed by blocks | output_object_spec.md, provenance_contract.md |
| 4 | observed fact | Verifiable data point from external source | fact_consumption_matrix.md, design.md |
| 5 | calculated signal | Derived value from computation on facts | signal_consumption_matrix.md, design.md |
| 6 | provenance | Chain of custody from source to interpretation | provenance_contract.md, output_object_spec.md |
| 7 | completeness | Qualitative indicator of evidence availability (high/medium/low/insufficient) | output_object_spec.md, design.md |
| 8 | interpretation | Diagnostic observation produced by a block from consumed evidence | output_object_spec.md, design.md |
| 9 | narrative | Referenced as future interface only — narrative exposure context | deferred_interfaces.md, portfolio_fit_interface.md |
| 10 | asset | The individual company/security being analyzed | All artifacts |
| 11 | block | Discrete diagnostic dimension (SAI-BLK-NN) | block_taxonomy.md, all artifacts |
| 12 | red flag | Evidence-based diagnostic warning condition | red_flag_taxonomy.md |
| 13 | market regime | Not used directly by SAI — referenced only via deferred correlation context | deferred_interfaces.md |
| 14 | portfolio fit | Diagnostic output about asset-to-portfolio relationship | portfolio_fit_interface.md |
| 15 | dependency | Shared exposure between assets or deferred framework relationship | portfolio_fit_interface.md, deferred_interfaces.md |
| 16 | correlation | Statistical co-movement observed between assets | peer_benchmark.md, deferred_interfaces.md |
| 17 | valuation context | Diagnostic interpretation of market pricing relative to fundamentals | valuation_boundary.md |
| 18 | recommendation | Explicitly PROHIBITED within SAI | All prohibition sections |
| 19 | scoring | Explicitly PROHIBITED within SAI | All prohibition sections |
| 20 | registry | External canonical data stores SAI consumes but does not mutate | deferred_interfaces.md |
| 21 | SSOT | Single Source of Truth — external authoritative document | All governance references |

---

## 3. Cross-Framework Comparison Table

| # | SAI Term | Market Evidence Framework | Narrative Framework v2 | Market Organism Glossary | Compatibility |
|---|----------|--------------------------|----------------------|-------------------------|---------------|
| 1 | fact | Observed_Fact (formal) | (consumed via MEF) | (not in MO glossary) | **Compatible** — SAI shorthand for Observed_Fact |
| 2 | signal | Calculated_Signal (formal) | (consumed via MEF) | Variable_Signal, Canonical_Signal_Truth | **Compatible with note** — see Section 5 |
| 3 | evidence | Evidence_Container (broader grouping) | (not directly used) | (not in glossary) | **Compatible** — SAI umbrella; MEF structured grouping |
| 4 | observed fact | Observed_Fact (identical) | (not directly used) | (not in glossary) | **Identical** |
| 5 | calculated signal | Calculated_Signal (identical) | (not directly used) | (not in glossary) | **Identical** |
| 6 | provenance | Evidence_Provenance (aligned) | (not directly used) | (not in glossary) | **Compatible** |
| 7 | completeness | (not formally defined) | (not used) | (not in glossary) | **SAI-local** — no conflict |
| 8 | interpretation | (not formally defined) | (not used) | (not in glossary) | **SAI-local** — no conflict |
| 9 | narrative | (evidence about narratives) | Narrative_Container (formal primitive) | (not in MO glossary) | **Compatible with boundary** — SAI interface-only |
| 10 | asset | (not formally defined) | Asset (leaf node primitive) | (not in glossary) | **Compatible** |
| 11 | block | (not used) | (not used) | (not in glossary) | **SAI-local** — no conflict |
| 12 | red flag | (not formally defined) | (not used) | (not in glossary) | **SAI-local** — no conflict |
| 13 | market regime | (not formally defined) | (not used) | (implied by State_Change) | **Ambiguous** — Finding #1 |
| 14 | portfolio fit | (not used) | (not used) | (not in glossary) | **SAI-local** — no conflict |
| 15 | dependency | (not formally defined) | (not used in this sense) | Dependency_Path (formal) | **Ambiguous** — Finding #2 |
| 16 | correlation | (not formally defined) | (not used) | (implied in propagation) | **Compatible** |
| 17 | valuation context | (not formally defined) | (not used) | (not in glossary) | **SAI-local** — no conflict |
| 18 | recommendation | (explicitly excluded) | (explicitly excluded) | (not relevant) | **Aligned** — prohibition shared |
| 19 | scoring | (explicitly excluded) | (explicitly excluded) | (not relevant) | **Aligned** — prohibition shared |
| 20 | registry | (Narrative Registry referenced) | Narrative Registry (formal) | (not in glossary) | **Compatible** |
| 21 | SSOT | (used consistently) | (used consistently) | (governance term) | **Compatible** |

---

## 4. Conflict Findings

### Finding #1: "Market Regime" — Ambiguity

| Field | Value |
|-------|-------|
| **SAI usage** | SAI does not directly use "market regime" as a defined term. deferred_interfaces.md references "regime detection" in Correlation/Dependency Framework context. |
| **Market Organism usage** | State_Change is the causal primitive; "regime" is implied within sub-categories (e.g., rate regime shift). No formal "market regime" term in canonical glossary. |
| **Conflict type** | Terminological ambiguity — "regime" used informally without canonical definition |
| **Severity** | LOW — SAI does not define or consume "market regime" as a formal primitive |
| **Resolution** | No mutation required. If "market regime" becomes formal, it should enter canonical glossary first. |

### Finding #2: "Dependency" — Dual Usage

| Field | Value |
|-------|-------|
| **SAI usage** | (a) "deferred dependency" — framework SAI depends on; (b) "dependency overlap" — shared operational dependencies between portfolio assets |
| **Market Organism usage** | Dependency_Path — formal primitive: "A directed connection between two nodes in the organism through which state changes propagate" |
| **Conflict type** | Terminological overload — same word, different meanings |
| **Severity** | LOW — SAI always qualifies usage ("deferred dependency", "dependency overlap"); contextually unambiguous |
| **Resolution** | No mutation required. Contextual qualification prevents confusion. |

---

## 5. Ambiguous Terms

| # | Term | Ambiguity | SAI Context | Other Framework Context | Risk |
|---|------|-----------|-------------|------------------------|------|
| 1 | regime | Informal, no canonical definition | "correlation regime shift", "regime detection" | MO implies via State_Change taxonomy | LOW |
| 2 | dependency | Dual meaning across frameworks | "deferred dependency", "dependency overlap" | MO: Dependency_Path (causal propagation) | LOW |
| 3 | signal | Slightly different abstraction layers | Any calculated signal consumed from MEF | MO: Variable_Signal with lifecycle/refresh | LOW |

---

## 6. Compatibility Notes

### 6.1 Strong Compatibility (No Action Needed)

- fact / Observed_Fact — identical concept
- calculated signal / Calculated_Signal — identical concept
- observed fact / Observed_Fact — identical concept
- provenance / Evidence_Provenance — aligned concept
- asset — aligned with Narrative Framework leaf-node
- SSOT — consistent governance usage
- recommendation (prohibited) — aligned exclusion
- scoring (prohibited) — aligned exclusion
- registry — consistent reference usage

### 6.2 SAI-Local Terms (No Conflict)

- block, red flag, completeness, interpretation, portfolio fit, valuation context

### 6.3 Interface-Only Terms (Boundary Respected)

- narrative — SAI references only; Narrative Framework v2 owns definition
- correlation — SAI consumes from deferred framework; does not calculate
- registry — SAI references but does not mutate

---

## 7. Deferred Glossary Recommendations

Documented for future governance consideration only. This artifact does NOT implement these.

| # | Recommendation | Rationale | Priority |
|---|---------------|-----------|----------|
| 1 | Consider adding "Evidence_Completeness" to canonical glossary | Used by SAI; may be needed by other frameworks | LOW |
| 2 | Consider adding "Red_Flag" if other frameworks adopt it | Currently SAI-specific | LOW |
| 3 | Consider formalizing "market regime" if consumed as primitive | Currently informal | LOW |
| 4 | Consider disambiguating "dependency" if confusion arises | Currently contextually clear | LOW |

---

## 8. No-Mutation Statement

This artifact does NOT mutate:
- Canonical glossary (`.kiro/specs/market-organism-framework/requirements.md`)
- Market Evidence Framework (`docs/README_market_evidence_framework.md`)
- Narrative Framework v2 (`docs/README_narrative_framework.md`)
- Market Organism Principles (`docs/market_organism/README_market_organism_principles.md`)
- Shared Glossary Reference (`docs/market_organism/README_shared_glossary_reference.md`)

No SAI terms are renamed. No canonical terminology is created. All findings are observations only.

---

## 9. Verification Gate Evidence

### VG-SAI-10 (Cross-Framework Consistency Gate) Evidence

| Gate Criterion | Evidence |
|---------------|----------|
| SAI terminology compared against Market Evidence Framework | Section 3 — 21 terms |
| SAI terminology compared against Narrative Framework v2 | Section 3 — 21 terms |
| SAI terminology compared against Market Organism Principles | Section 3 — 21 terms |
| SAI terminology compared against Shared Glossary | Section 3 — 21 terms |
| Conflicts documented | Section 4 — 2 findings (LOW) |
| No mutations performed | Section 8 |

**Overall**: SAI terminology is consistent with upstream frameworks. Two LOW-severity ambiguities (regime, dependency) are contextually unambiguous.

### No-Auto-Completion Statement

This artifact provides **evidence only** toward VG-SAI-10. It does NOT execute or pass VG-SAI-10. Gate execution requires Task 15.10.

---

## 10. Boundary Confirmations

- ✓ Zero implementation code
- ✓ Zero glossary mutation
- ✓ Zero framework mutation
- ✓ Zero terminology rewrite or canonical rename
- ✓ Zero registry or SSOT mutation
- ✓ Zero scoring/ranking/recommendation/allocation/trading logic
- ✓ Zero fact/signal/evidence primitive creation
- ✓ Zero asset or narrative mappings
- ✓ Zero verification gate auto-completion

---

*End of artifact.*
