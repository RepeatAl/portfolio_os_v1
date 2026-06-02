# Governance Stabilization Audit Report

**Date**: 2026-05-25  
**Scope**: Full forensic review of the domainization system  
**Auditor**: Automated governance audit (governance_stabilization_audit.py)  
**Objective**: Prove the governance model survives contact with reality  

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Findings | **147** |
| CRITICAL | 1 |
| HIGH | 91 |
| MEDIUM | 55 |
| LOW | 0 |
| Authority Chain | ✅ CLEAN |
| Circular Dependencies | ✅ NONE |

The governance model has **structural integrity** in its authority chain (SIGNALS → SEMANTICS → REASONING → REPORT is properly maintained). However, it suffers from **two systemic problems** that must be fixed before adding more features:

1. **Massive dependency gap** — 89 SSOT documents referenced as dependencies are not registered in the artifact registry
2. **Lifecycle model contradiction** — "current" and "captured" are defined as read-only states, but all DATA_OUT/REPORT_OUT/SNAPSHOT artifacts need write access to be regenerated daily

---

## Audit 1: Registry Truth Consistency

### 1.1 Duplicate artifact_id (CRITICAL)

| Finding | Severity |
|---------|----------|
| `data_json` appears twice (positions 58 and 74) | CRITICAL |

**Root cause**: During Task 11.2 (Register portfolio state data files), a new `data_json` entry was added in the PORTFOLIO STATE section, but the original "Example 9" entry was not removed.

**Fix**: Remove the duplicate entry at position 74 (the "Example 9: CONFIG" leftover).

---

### 1.2 Missing Dependencies (HIGH — 89 findings)

All SSOT framework documents referenced as dependencies are **not registered** in the artifact registry. These are markdown files in `docs/` that should either use YAML frontmatter (preferred for markdown) or be registered in the artifact registry.

**Unique missing dependency IDs (17 distinct documents):**

| Missing artifact_id | Expected file_path | Referenced by |
|--------------------|--------------------|---------------|
| `signal_calculation_framework_md` | docs/signal_calculation_framework.md | 14 artifacts |
| `report_reasoning_system_md` | docs/report_reasoning_system.md | 14 artifacts |
| `correlation_dependency_framework_md` | docs/correlation_dependency_framework.md | 8 artifacts |
| `market_regime_framework_md` | docs/market_regime_framework.md | 6 artifacts |
| `portfolio_memory_architecture_md` | docs/portfolio_memory_architecture.md | 8 artifacts |
| `portfolio_health_framework_md` | docs/portfolio_health_framework.md | 3 artifacts |
| `scoring_methodology_framework_md` | docs/scoring_methodology_framework.md | 1 artifact |
| `semantic_signal_registry_md` | docs/semantic_signal_registry.md | 1 artifact |
| `semantic_reasoning_rules_md` | docs/semantic_reasoning_rules.md | 4 artifacts |
| `decision_governance_md` | docs/decision_governance.md | 4 artifacts |
| `report_section_specification_md` | docs/report_section_specification.md | 4 artifacts |
| `simulation_architecture_md` | docs/simulation_architecture.md | 2 artifacts |
| `dashboard_philosophy_md` | docs/dashboard_philosophy.md | 1 artifact |
| `engine_design_principles_md` | docs/engine_design_principles.md | 2 artifacts |
| `portfolio_state_model_md` | docs/portfolio_state_model.md | 5 artifacts |
| `watchlist_asset_registry_framework_md` | docs/watchlist_asset_registry_framework.md | 1 artifact |
| `data_ingestion_normalization_framework_md` | docs/data_ingestion_normalization_framework.md | 1 artifact |

**Root cause**: The registry's dependency resolution only checks `artifact_id` in the registry YAML. Markdown files use frontmatter instead of registry entries (by design), but the dependency graph doesn't resolve frontmatter-based IDs.

**Decision needed**:
- Option A: Register these markdown docs in the registry (creates dual-source-of-truth risk)
- Option B: Change dependency resolution to also scan frontmatter `artifact_id` fields (recommended)
- Option C: Accept that markdown deps are "soft references" and downgrade severity to MEDIUM

---

### 1.3 Circular Dependencies

✅ **NONE DETECTED** — The dependency graph is acyclic.

---

### 1.4 File Path Consistency (MEDIUM — 2 findings)

| artifact_id | Registered path | Status |
|-------------|----------------|--------|
| `kiro_calibration_report_md` | `docs/kiro_calibration_report.md` | FILE NOT FOUND |
| `execution_governance_baseline_md` | `.kiro/steering/execution-governance-baseline.md` | FILE NOT FOUND |

**Fix**: Verify correct file paths and update registry entries.

---

### 1.5 Domain-Type Violations (HIGH — 1 finding)

| artifact_id | Domain | Type | Issue |
|-------------|--------|------|-------|
| `visual_engine_py` | USER | ENGINE | USER domain `cannot_own` includes ENGINE |

**Fix options**:
- Move `visual_engine_py` to ARCH domain (if it's infrastructure)
- Update `domain_registry.yaml` to allow USER to own ENGINE (if visualization logic intentionally lives in USER)
- Create a new ENGINE type like `UI_ENGINE` that USER can own

---

## Audit 2: Lifecycle Integrity

### 2.1 Valid Lifecycle States

✅ All artifacts have valid lifecycle states for their artifact type.

---

### 2.2 Read-Only States with Writers (MEDIUM — 52 findings)

This is a **systemic design issue**, not individual bugs.

**The contradiction:**

The lifecycle state machine defines these as read-only:
- `REPORT_OUT.current` → read_only
- `REPORT_OUT.generated` → read_only
- `DATA_OUT.current` → read_only
- `DATA_OUT.generated` → read_only
- `SNAPSHOT.captured` → read_only
- `SNAPSHOT.archived` → read_only

But ALL these artifacts have `allowed_writers` set because they **need to be regenerated daily**.

**Breakdown:**

| State | Type | Count | Example |
|-------|------|-------|---------|
| current | REPORT_OUT | 16 | `portfolio_report_txt` |
| current | DATA_OUT | 28 | `allocation_engine_xlsx` |
| captured | SNAPSHOT | 3 | `portfolio_history_xlsx` |
| archived | SNAPSHOT | 5 | `briefing_2026_05_23_txt` |

**Root cause**: The state machine was designed with a "document versioning" mental model (once current, it's frozen). But data outputs are **overwritten in place** — `allocation_engine.xlsx` gets regenerated every engine run.

**Fix options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A (recommended) | Make `current` a modifiable state for DATA_OUT and REPORT_OUT | Matches reality, minimal change | Weakens immutability guarantee |
| B | Each run creates versioned artifacts, old transitions to `archived` | Strong audit trail | Massive file proliferation |
| C | Add `regenerable` flag | Separates immutability from write permission | Schema change, more complexity |

---

### 2.3 Active Engines Without Dependencies

✅ All active engines have at least one dependency declared.

---

## Audit 3: Authority Chain Integrity

### Core Chain: SIGNALS → SEMANTICS → REASONING → REPORT

✅ **CLEAN** — No reverse authority flow detected.

No artifact in a lower-authority domain depends on a higher-authority domain artifact. The information flow is strictly unidirectional:

```
SIGNALS (level 1) → SEMANTICS (level 2) → REASONING (level 3) → REPORT (level 4)
```

### Cross-Domain Dependency Direction

✅ All cross-domain dependencies flow in the correct direction (lower level → higher level consumption).

### Semantic Contamination Check

| Domain | Contamination | Status |
|--------|--------------|--------|
| SIGNALS contains semantic interpretation? | No | ✅ |
| SIGNALS contains decision logic? | No | ✅ |
| REPORT contains decision logic? | No | ✅ |
| REASONING generates report text? | No | ✅ |

### Minor Concern (False Positive)

`report_engine_py` description contains "reasoning" keyword — but in context it says "from reasoning outputs" (consuming reasoning, not performing it). The authority chain is intact.

---

## Audit 4: Observer Noise Audit

### Observer Assessment

| Observer | Noise Risk | Current Behavior | Recommendation |
|----------|-----------|-----------------|----------------|
| RegistrationValidator | LOW | Catches unregistered files | Keep as-is |
| DomainAssignmentValidator | LOW | Catches domain mismatches | Keep as-is |
| LifecycleValidator | **CRITICAL NOISE** | Fires on ALL 52 "current with writers" artifacts | Fix lifecycle model first |
| BoundaryAwarenessValidator | LOW | Catches cross-domain writes | Keep as-is |
| SSOTConsistencyValidator | LOW | Catches topic conflicts | Keep as-is |

### Noise Impact Analysis

The LifecycleValidator will produce **52 warnings every single run**. This creates:
- Developer fatigue → all warnings ignored
- Signal-to-noise ratio collapse → real problems hidden
- False sense of "everything is broken" → governance loses credibility

**Recommendation**: Fix the lifecycle model (Audit 2.2) BEFORE relying on observer output. Until then, the LifecycleValidator should either be suppressed or its severity for "current with writers" downgraded to INFO.

---

## Audit 5: Health Report Reality Check

### What the Health Report Currently Detects

| Capability | Status |
|-----------|--------|
| Registry completeness issues | ✅ Detects |
| Domain assignment violations | ✅ Detects |
| Lifecycle state violations | ⚠️ Detects but 52 are false positives |
| SSOT topic conflicts | ✅ Detects |
| Boundary awareness violations | ✅ Detects |

### What the Health Report Does NOT Detect

| Missing Capability | Risk | Impact |
|-------------------|------|--------|
| Orphaned engines (no consumers) | MEDIUM | Dead code accumulates silently |
| Dead artifacts (registered but file deleted) | HIGH | Registry becomes unreliable |
| Dependency staleness (dep exists but is deprecated) | MEDIUM | Engines depend on abandoned specs |
| Runtime risks (engine fails → what breaks downstream?) | HIGH | No blast radius visibility |
| Unused DATA_OUT files (generated but never consumed) | LOW | Disk waste, confusion |
| Cross-domain write attempts (actual file modifications) | HIGH | Governance violation at runtime |

### Operational Usefulness Score

**Current: 4/10** — The health report catches registry-level problems but misses runtime and operational risks entirely.

**Target: 8/10** — Add dead artifact detection, dependency staleness, and orphan detection.

---

## Audit 6: CLI Governance Drift

### 6.1 Cross-Domain Writer Bypass (HIGH)

The CLI `register` and `update` commands allow `--allowed-writers` to be set to **any domain** without validating that the writer domain has legitimate authority over the artifact's type.

**Example of governance bypass:**
```bash
# This SHOULD be blocked but ISN'T:
domainization register my_artifact file.py SIGNALS ENGINE --allowed-writers REPORT USER

# This grants REPORT domain write access to a SIGNALS artifact
# violating the authority chain
```

**Fix**: Add validation in `cli_registry_commands.py`:
- `--allowed-writers` domains must be able to own the artifact's type
- OR the artifact's primary domain must be in the writers list
- Cross-domain writers require explicit `--force` flag with audit log

---

### 6.2 Missing Safeguards

| Gap | Risk | Recommendation |
|-----|------|----------------|
| No `--force` flag for destructive operations | MEDIUM | Add confirmation for delete/purge |
| No audit trail for `update` commands | HIGH | Log who changed what, when |
| No confirmation for domain reassignment | MEDIUM | Require `--force` for domain changes |
| No validation of writer-domain authority | HIGH | Enforce domain-type ownership rules |
| No `delete` command exists yet | LOW | When added, must require `--force` |

---

### 6.3 What the CLI Correctly Enforces

| Enforcement | Status |
|-------------|--------|
| Domain existence validation on register | ✅ |
| Domain-type ownership on register | ✅ |
| Lifecycle transition validation on update | ✅ |
| Duplicate artifact_id prevention | ✅ |
| Metadata schema validation | ✅ |

---

## Priority Fix Order

| # | Issue | Severity | Impact | Effort | Dependency |
|---|-------|----------|--------|--------|------------|
| 1 | Remove duplicate `data_json` | CRITICAL | Breaks uniqueness constraint | 5 min | None |
| 2 | Fix lifecycle model for DATA_OUT/REPORT_OUT/SNAPSHOT | HIGH | Eliminates 52 false warnings | 30 min | None |
| 3 | Fix `visual_engine_py` domain assignment | HIGH | Domain-type violation | 5 min | None |
| 4 | Fix 2 broken file_path references | MEDIUM | Registry accuracy | 10 min | None |
| 5 | Add CLI writer validation | HIGH | Governance bypass risk | 30 min | None |
| 6 | Register SSOT docs or fix dependency resolution | HIGH | 89 broken dependency links | 1-2 hours | Decision on approach |
| 7 | Add dead artifact detection to health reporter | MEDIUM | Operational usefulness | 1 hour | None |
| 8 | Suppress LifecycleValidator noise until fix #2 | MEDIUM | Developer trust | 15 min | Fix #2 |

---

## Conclusion

The domainization system's **authority chain is sound** — the most critical architectural invariant (SIGNALS → SEMANTICS → REASONING → REPORT) is properly maintained with no reverse flows or contamination.

However, the system has **operational debt** that will erode trust if not addressed:
- The lifecycle model contradicts daily operations (52 permanent false warnings)
- The dependency graph is incomplete (89 dangling references)
- The CLI has a governance bypass vector (cross-domain writer assignment)

**Recommendation**: Execute fixes 1-5 immediately (total effort: ~1.5 hours). These are non-breaking, stabilization-only changes that prove the governance model works in practice. Fix 6 requires an architectural decision on how to handle markdown frontmatter dependencies.

---

## Appendix: Audit Script

The automated audit script is located at:
`.domainization/src/governance_stabilization_audit.py`

Run with:
```bash
cd .domainization/src
../../.venv/bin/python governance_stabilization_audit.py
```

Exit code: 0 = no CRITICAL findings, 1 = CRITICAL findings present.
