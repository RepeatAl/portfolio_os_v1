# Narrative Registry Framework — Requirements Foundation Report

**Date**: 2026-06-03
**Branch**: `spec/narrative-registry-framework`
**Phase**: Requirements foundation
**Status**: COMPLETE

---

## 1. Files Created

| File | Purpose |
|------|---------|
| `.kiro/specs/narrative-registry-framework/.config.kiro` | Spec configuration (feature, requirements-first) |
| `.kiro/specs/narrative-registry-framework/requirements.md` | Requirements document (10 requirements, NRF-REQ-1 through NRF-REQ-10) |
| `.domainization/reports/narrative_registry_framework_requirements_foundation_2026-06-03.md` | This report |

## 2. Sources Consumed

| Source | Used For |
|--------|----------|
| `.domainization/reports/narrative_registry_framework_preflight_2026-06-03.md` | Primary source — gap matrix, candidate requirements, governance model, field model |
| `docs/README_narrative_framework.md` (Section 13: Extension Criteria) | Inclusion criteria, required fields, exclusion criteria |
| `docs/README_narrative_framework.md` (Section 6: Lifecycle) | Lifecycle states and transitions |
| `docs/README_narrative_framework.md` (Section 4: Definition) | ID namespace rules |
| `.domainization/artifact_registry.yaml` | Artifact registration pattern |
| `.domainization/domain_registry.yaml` | Domain ownership model (ARCH) |
| `.domainization/lifecycle_state_machine.yaml` | SSOT lifecycle (draft → review → canonical → deprecated) |

## 3. Requirements Created

| ID | Title | Acceptance Criteria Count |
|----|-------|--------------------------|
| NRF-REQ-1 | Registry Boundary | 6 |
| NRF-REQ-2 | Canonical Entry Fields | 6 |
| NRF-REQ-3 | ID Governance | 7 |
| NRF-REQ-4 | Inclusion Criteria | 5 |
| NRF-REQ-5 | Exclusion Constraints | 5 |
| NRF-REQ-6 | Lifecycle Governance | 7 |
| NRF-REQ-7 | Cross-Reference Contract | 6 |
| NRF-REQ-8 | Artifact Registry Integration | 5 |
| NRF-REQ-9 | No Future-Leak | 6 |
| NRF-REQ-10 | Readiness for Future Asset-to-Narrative Registry | 6 |

**Total**: 10 requirements, 59 acceptance criteria

## 4. Gap-to-Requirement Traceability Summary

| Gap ID | Mapped To | Status |
|--------|-----------|--------|
| NRG-01 | NRF-REQ-4 | Resolved in requirements |
| NRG-02 | NRF-REQ-8 | Resolved (ARCH ownership declared) |
| NRG-03 | NRF-REQ-8, NRF-REQ-5 | Partially resolved (SSOT type confirmed; final validation in design) |
| NRG-04 | NRF-REQ-3 | Resolved in requirements |
| NRG-05 | NRF-REQ-7 | Partially resolved (format deferred to design) |
| NRG-06 | NRF-REQ-6 | Resolved in requirements |
| NRG-07 | NRF-REQ-8 | Resolved (registration specified; actual registration in tasks) |
| NRG-08 | NRF-REQ-10 | Partially resolved (versioning deferred to design) |
| NRG-09 | NRF-REQ-2 | Partially resolved (values specified; storage format in design) |
| NRG-10 | Local glossary | DEFERRED — requires separate governance authorization |
| NRG-11 | — | DEFERRED — backlog (not this spec) |
| NRG-12 | NRF-REQ-7 | Partially resolved (validation strategy deferred to design) |

## 5. Confirmations

- ✅ **No registry file was created** — schema and governance defined in requirements only
- ✅ **No narrative instances were populated** — zero entries exist
- ✅ **No canonical SSOT was mutated** — Narrative Framework v2, Market Organism Layer 0, and central glossary untouched
- ✅ **No implementation work was performed** — no code, engines, scripts, dashboards, or runtime artifacts
- ✅ **No asset-to-narrative mappings created**
- ✅ **No scoring, ranking, or probability logic introduced**

## 6. Open Questions for Human Review

| # | Question | Impact | Default if Unresolved |
|---|----------|--------|----------------------|
| 1 | Should a `system.*` registry exist before narrative registration requires `connected_systems` references? | NRG-12: unverifiable connections | Accept system IDs on trust; validate in future spec |
| 2 | Should there be a maximum number of `connected_systems` per narrative? | Schema design | No maximum (list is unbounded) |
| 3 | Should `velocity` be a required field or remain optional? | NRF-REQ-2 | Optional (current design) |
| 4 | Should lifecycle transition history be stored inline in the registry entry or in a separate audit log? | NRF-REQ-6 | Design decision — recommend separate audit log |
| 5 | Should the registry file be a single YAML file or a directory of per-narrative files? | Design decision | Single YAML file (simpler governance, easier VG-2 verification) |

## 7. Recommendation

**Proceed to `design.md`** — The requirements foundation is stable. All 10 requirements have explicit acceptance criteria verifiable by document inspection. The gap matrix is resolved or explicitly deferred. No blockers exist.

The design phase should address:
- Registry file format (YAML structure)
- Hierarchy declaration format (NRG-05)
- Entry versioning strategy (NRG-08)
- System reference validation rules (NRG-12)
- Velocity storage format (NRG-09)
- Lifecycle audit trail structure (Question 4)
- Single-file vs directory decision (Question 5)

---

*Report generated: 2026-06-03*
*Phase: Requirements foundation*
*Author: Kiro (automated)*
*No canonical SSOTs were modified.*
