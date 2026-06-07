# SAI Framework — Artifact Registry Readiness Report

**Report date**: 2026-06-06
**Task**: 17.1 Artifact Registry Readiness Check
**Spec**: single-asset-intelligence-framework
**Authority**: ARCH

---

## 1. Purpose

Determine whether SAI framework artifacts require registration in the domainization artifact registry. Document the needed mutation and STOP for human approval. This task does NOT perform the mutation.

---

## 2. Source Lookup

| Source | Path | Status |
|--------|------|--------|
| Artifact Registry | `.domainization/artifact_registry.yaml` | Present (145 entries) |
| Registry schema | Defined in artifact_registry.yaml header comments | Inspected |

---

## 3. Current SAI Artifact Inventory

### Spec Foundation (3 files)
- `.kiro/specs/single-asset-intelligence-framework/requirements.md`
- `.kiro/specs/single-asset-intelligence-framework/design.md`
- `.kiro/specs/single-asset-intelligence-framework/tasks.md`

### Artifacts (16 files)
- `artifacts/block_taxonomy.md`
- `artifacts/fact_consumption_matrix.md`
- `artifacts/signal_consumption_matrix.md`
- `artifacts/output_object_spec.md`
- `artifacts/provenance_contract.md`
- `artifacts/red_flag_taxonomy.md`
- `artifacts/temporal_resolution_matrix.md`
- `artifacts/deferred_interfaces.md`
- `artifacts/valuation_boundary.md`
- `artifacts/credit_solvency.md`
- `artifacts/peer_benchmark.md`
- `artifacts/portfolio_fit_interface.md`
- `artifacts/kpi_mapping_validation.md`
- `artifacts/terminology_audit.md`
- `artifacts/README_single_asset_intelligence.md`
- `artifacts/README_block_taxonomy_artifact.md`

### Gates (12 files)
- `gates/gate_vg_sai_01.md` through `gates/gate_vg_sai_12.md`

**Total**: 31 SAI files

---

## 4. Current Registry Status

| Check | Result |
|-------|--------|
| SAI artifacts in artifact_registry.yaml | **NOT REGISTERED** (0/31) |
| SAI artifacts with YAML frontmatter | **NONE** (0/31) |
| Pre-commit hook warnings | RegistrationValidator flags all SAI files as "not registered in domainization system" |

---

## 5. Governance Policy Interpretation

The artifact registry header states:
- "Markdown files should use YAML frontmatter instead of entries here"
- Required fields include: artifact_id, file_path, primary_domain, artifact_type, lifecycle_status, created_date, last_modified, owner_role, ssot_relationship, allowed_writers, allowed_readers

SAI artifacts are markdown files. Per governance policy, they should either:
1. Embed YAML frontmatter in each file, OR
2. Be added as entries to `.domainization/artifact_registry.yaml`

Currently neither approach is implemented. The pre-commit RegistrationValidator consistently flags this gap.

---

## 6. Required Registry Mutation

### Option A — YAML Frontmatter (Recommended per registry comment)

Add YAML frontmatter to each SAI markdown file. Example pattern:

```yaml
---
artifact_id: sai.block_taxonomy_md
file_path: .kiro/specs/single-asset-intelligence-framework/artifacts/block_taxonomy.md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: draft
created_date: "2026-06-06"
last_modified: "2026-06-06"
owner_role: Portfolio Architect
ssot_relationship: canonical
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
---
```

This would need to be applied to all 31 SAI files (or at least the 16 artifacts + README).

### Option B — Registry YAML Entries

Add entries to `.domainization/artifact_registry.yaml` for each SAI artifact. This is the alternative for non-markdown files, but could be used for markdown files too.

### Recommended Approach

Option A (YAML frontmatter) is recommended per the registry's own governance comment. However, modifying 31 files to add frontmatter is a significant change requiring human approval.

---

## 7. Artifact Groups for Registration

If registration proceeds, the following groups would need metadata:

| Group | Count | Suggested artifact_type | Suggested lifecycle_status |
|-------|-------|------------------------|---------------------------|
| Spec foundation (requirements, design, tasks) | 3 | SSOT | draft |
| Core taxonomy/matrix artifacts | 7 | SSOT | draft |
| Domain boundary artifacts | 5 | SSOT | draft |
| Validation/audit artifacts | 2 | SSOT | draft |
| README artifact | 1 | SSOT | draft |
| Gate execution artifacts | 12 | verification_gate | executed |
| Block taxonomy README | 1 | SSOT | draft |

Common metadata:
- primary_domain: ARCH
- owner_role: Portfolio Architect
- ssot_relationship: canonical (for spec/artifacts), none (for gates)
- allowed_writers: [ARCH, GOV]
- allowed_readers: [ALL]

---

## 8. Result

### REGISTRY_UPDATE_REQUIRED_HUMAN_APPROVAL_NEEDED

SAI artifacts are not registered in the domainization system. The pre-commit RegistrationValidator correctly identifies this gap. Registration requires either frontmatter addition to 31 files or registry YAML entries.

**This task does NOT perform the mutation.** Human/CTO approval is required before modifying the registry or adding frontmatter.

---

## 9. Unresolved Issues

| # | Issue | Resolution Path |
|---|-------|----------------|
| 1 | 31 SAI files not registered | Human approval needed for registration approach (frontmatter vs registry entries) |
| 2 | Pre-commit warnings will persist until registration is completed | Non-blocking (observability mode) |

---

## 10. Boundary Confirmations

- ✓ No registry mutation performed
- ✓ No SSOT mutation
- ✓ No implementation code
- ✓ No artifact content mutation
- ✓ No gate mutation
- ✓ No scoring/recommendation/allocation/trading logic
- ✓ No Task 18.1 execution

---

*End of report.*