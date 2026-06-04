# Narrative Population Framework — Requirements Foundation Report

**Date**: 2026-06-04
**Branch**: `spec/narrative-population-framework`
**Type**: Requirements foundation
**Status**: COMPLETE

---

## Files Created

| File | Purpose |
|------|---------|
| `.kiro/specs/narrative-population-framework/.config.kiro` | Spec configuration |
| `.kiro/specs/narrative-population-framework/requirements.md` | Requirements document |
| `.domainization/reports/narrative_population_framework_requirements_foundation_2026-06-04.md` | This report |

---

## Sources Consumed

| # | Source | Consumed? |
|---|--------|-----------|
| 1 | `.domainization/reports/narrative_population_framework_preflight_2026-06-04.md` | ✅ Yes — candidate classifications used as draft input |
| 2 | `docs/registries/narrative_registry.yaml` | ✅ Yes — schema and governance rules referenced |
| 3 | `docs/registries/README_narrative_registry_governance.md` | ✅ Yes — creation procedure, collision check, inclusion criteria |
| 4 | `docs/README_narrative_framework.md` | ✅ Yes — Sections 4, 6, 13, 14, 15 referenced |
| 5 | `docs/README_market_evidence_framework.md` | ✅ Yes — Sections 4, 23, 30, 31 referenced |
| 6 | `.domainization/reports/market_evidence_framework_credit_solvency_hardening_2026-06-04.md` | ✅ Yes — credit/solvency requirements incorporated |
| 7 | `docs/market_organism/README_market_organism_principles.md` | ✅ Yes — Principles 1, 2, 6 referenced |
| 8 | `docs/market_organism/README_state_change_taxonomy.md` | ✅ Yes — birth trigger format |
| 9 | `docs/market_organism/README_expansion_taxonomy.md` | ✅ Yes — system connections |
| 10 | `docs/market_organism/README_shared_glossary_reference.md` | ✅ Yes — glossary policy |

---

## Requirements Created

| Requirement ID | Title | Acceptance Criteria Count |
|---------------|-------|--------------------------|
| NPF-REQ-1 | Population Boundary | 5 |
| NPF-REQ-2 | Candidate Evaluation Model | 5 |
| NPF-REQ-3 | Evidence Requirement | 7 |
| NPF-REQ-4 | No Asset-First Population | 5 |
| NPF-REQ-5 | Candidate Field Preparation | 4 |
| NPF-REQ-6 | Human Review Gate | 10 |
| NPF-REQ-7 | Registry Mutation Control | 5 |
| NPF-REQ-8 | Verification Before Population | 5 |
| NPF-REQ-9 | Backlog Handling | 5 |
| NPF-REQ-10 | Future Asset-to-Narrative Readiness | 5 |
| NPF-REQ-11 | Market Evidence Compatibility | 6 |
| NPF-REQ-12 | Credit/Solvency Evidence Awareness | 6 |

**Total**: 12 requirements, 68 acceptance criteria

---

## Acceptance Criteria Summary

All acceptance criteria are verifiable by document inspection. No criterion requires:
- Runtime behavior or engine execution
- Actual narrative instance population during requirements phase
- Asset-to-narrative mapping
- Numeric computation or scoring
- Code compilation or script execution

---

## Gap-to-Requirement Traceability

| Gap ID | Mapped To | Status |
|--------|-----------|--------|
| NPG-01 | NPF-REQ-5 | Accept on trust — design phase |
| NPG-02 | NPF-REQ-6.10 | Human decision — design phase |
| NPG-03 | NPF-REQ-6.8 | Human decision — design phase |
| NPG-04 | NPF-REQ-1 | Addressed — small Wave 1 validates pipeline |
| NPG-05 | NPF-REQ-2.1b, NPF-REQ-5 | Addressed — concrete falsification required |
| NPG-06 | NPF-REQ-4 | Addressed — explicit prohibition |
| NPG-07 | NPF-REQ-3, NPF-REQ-5 | Design phase — retrospective ID policy |
| NPG-08 | NPF-REQ-5 | Tasks phase — populate after entries exist |
| NPG-09 | NPF-REQ-5.2 | Design phase — optional field |
| NPG-10 | NPF-REQ-5.2 | Design phase — hierarchy policy |
| NPG-11 | NPF-REQ-11 | Addressed — consumed as draft from branch |
| NPG-12 | NPF-REQ-12 | Addressed — valuation trap guard rule |

All 12 gaps mapped. No gaps deferred without explicit resolution path.

---

## Confirmations

| Check | Status |
|-------|--------|
| No registry mutation occurred | ✅ `narratives: []` remains empty |
| No narrative entries added | ✅ |
| No asset mappings created | ✅ |
| No facts/signals/evidence objects created | ✅ |
| No implementation work performed | ✅ |
| No engines, code, dashboards, scoring | ✅ |
| No Narrative Framework v2 modification | ✅ |
| No Market Organism Layer 0 modification | ✅ |
| No central glossary modification | ✅ |
| No Market Evidence Framework modification | ✅ |
| All candidate IDs remain candidate/proposed only | ✅ |
| All cross-references use canonical format | ✅ |

---

## Market Evidence Framework Availability

**Status**: Available and consumed.

Market Evidence Framework (`docs/README_market_evidence_framework.md`) is not yet merged to `main` (still on `spec/market-evidence-framework-foundation`). It was merged into this working branch to satisfy the requirement that it be consumed as input. Requirements explicitly reference it as a draft dependency and note this status in Gap NPG-11.

Once Market Evidence Framework is merged to `main`, this gap closes automatically.

---

## Open Questions for Human Review

| # | Question | Impact |
|---|----------|--------|
| 1 | Is 5 the right Wave 1 size, or should it be 3-4? | Determines scope of first registration batch |
| 2 | Should Energy Infrastructure be in Wave 1 given partial overlap with AI Infrastructure? | May need scope narrowing first |
| 3 | Should AI Semiconductors be a sub-narrative of AI Infrastructure or independent? | Collision check implication |
| 4 | What lifecycle state approach for narratives clearly past "emerging"? | Register at emerging with note, or document lifecycle_history backdating? |
| 5 | Should Market Evidence Framework be merged to main before proceeding to design? | Affects canonical dependency status |

---

## Recommendation

**Proceed to `design.md` next.** Requirements are complete and cover all required areas:
- Population boundary defined
- Candidate evaluation model formalized
- Evidence requirements established (including Market Evidence Framework integration)
- Credit/solvency/valuation trap guard in place
- Human review gate defined
- All preflight gaps mapped to requirements
- Verification gate plan established

The design phase should detail: candidate field templates, collision check procedures for specific candidates, evidence justification format, and task execution boundaries.

---

*Report generated: 2026-06-04*
*Authority: ARCH*
