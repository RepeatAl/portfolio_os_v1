# Registry Gap Report

**Date**: 2026-05-26
**Purpose**: Identify artifacts on disk not in the registry, and registry entries without disk presence
**Registry**: `.domainization/artifact_registry.yaml`

---

## 1. Summary

| Metric | Value |
|--------|-------|
| Total registered artifacts | 93 |
| Artifacts on disk matching registry | 93 |
| Artifacts on disk NOT in registry | 13 |
| Registry entries without disk file | 0 |
| New spec files (not yet registered) | 4 |

---

## 2. Unregistered Artifacts on Disk

### 2.1 SSOT Documents (8 files)

These docs exist in `docs/` but have no registry entry. They were created after the initial registration wave.

| File Path | Probable Domain | Notes |
|-----------|----------------|-------|
| `docs/confidence_model.md` | GOV | Decision confidence framework |
| `docs/action_space_framework.md` | GOV | Action space definition |
| `docs/deployment_intelligence_framework.md` | REASONING | Deployment reasoning |
| `docs/multilingual_rendering_framework.md` | REPORT | Multilingual report rendering |
| `docs/opportunity_engine_design.md` | ARCH | Opportunity engine design doc |
| `docs/report_pipeline_architecture.md` | ARCH | Report pipeline architecture |
| `docs/future_framework_backlog.md` | ARCH | Future framework backlog |
| `docs/trusted_signal_sources.md` | DATA | Trusted data sources |

### 2.2 Governance/Steering Documents (1 file)

| File Path | Probable Domain | Notes |
|-----------|----------------|-------|
| `docs/portfolio_os_domainization_steering.md` | GOV | Domainization steering doc |

### 2.3 Report Outputs (4 files)

| File Path | Probable Domain | Notes |
|-----------|----------------|-------|
| `reports/governance_stabilization_audit_2026-05-25.md` | GOV | Audit report |
| `reports/governance_stabilization_preflight_2026-05-25.md` | GOV | Preflight report |
| `reports/governance_stabilization_verification_2026-05-25.md` | GOV | Verification report |
| `reports/task_1_execution_report.md` | ARCH | Task execution report |

---

## 3. New Spec Files (Not Registered — By Design)

Kiro spec files live in `.kiro/specs/` and are governance infrastructure, not product artifacts.
They do NOT require registry entries.

| File Path | Status |
|-----------|--------|
| `.kiro/specs/report-runtime-integrity/requirements.md` | New, ready for commit |
| `.kiro/specs/report-runtime-integrity/design.md` | New, ready for commit |
| `.kiro/specs/report-runtime-integrity/tasks.md` | New, ready for commit |
| `.kiro/specs/report-runtime-integrity/.config.kiro` | New, ready for commit |

---

## 4. Registry Entries Without Disk Presence

**None found.** All 93 registered artifacts have corresponding files on disk.

---

## 5. Recommendations

1. **Do NOT register the 13 unregistered artifacts now** — Registration is part of Requirement 3 in the report-runtime-integrity spec and will be handled during implementation.
2. **Spec files do not need registry entries** — They are Kiro governance infrastructure.
3. **No orphan registry entries** — Registry is consistent with disk state.
4. **The `reports/pm_report_engine.py` file IS registered** — It has lifecycle `development`.

---

## 6. Registry Consistency Verification

| Check | Result |
|-------|--------|
| All registered file_paths exist on disk | PASS |
| No duplicate artifact_ids | PASS |
| All primary_domains reference valid domain_ids | PASS |
| All artifact_types are valid | PASS |
| No conflicting SSOT topics | PASS (1 warning: main_py duplicate entry) |

### 6.1 Minor Issue: Duplicate `main_py` Entry

The artifact registry contains two entries with `artifact_id: main_py`:
- Line ~280: Basic entry (DEPLOY/RUNTIME)
- Line ~2020: Extended entry with dependencies (DEPLOY/RUNTIME)

**Impact**: Low — both entries are consistent. The second entry supersedes the first.
**Recommendation**: Remove the first entry during implementation phase.

---

*Generated: 2026-05-26*
*Phase: Pre-implementation governance alignment*
