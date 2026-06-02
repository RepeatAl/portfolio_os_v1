# Initial Health Report Baseline

## Overview

This document records the baseline health report for the Portfolio OS domainization system, generated on 2026-05-26. The report establishes the initial state of artifact governance after completing all registration tasks (Tasks 8-12) and serves as the reference point for measuring future improvements.

## Baseline Metrics Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total Artifacts | 93 | ✅ |
| Registered Artifacts | 93 | ✅ |
| Registration Coverage | 100.0% | ✅ |
| Total Domains | 12 | ✅ |
| Domains with Artifacts | 12 | ✅ |
| Enforcement Mode | OBSERVABILITY | ✅ |
| Total Violations | 14 | ⚠️ |
| Critical Violations | 0 | ✅ |
| High Violations | 14 | ⚠️ |
| Runtime Flow Health | 85.3% | ⚠️ |
| Forbidden Flows | 16 | ⚠️ |
| Report Value Coverage | 0.0% | ℹ️ |
| Infrastructure Drift | 9.7% | ℹ️ |

## Domain Coverage Distribution

All 12 canonical domains have at least one registered artifact:

| Domain | Priority | Artifact Count | Primary Types |
|--------|----------|---------------|---------------|
| SIGNALS | Core | 33 | DATA_OUT (24), ENGINE (4), SSOT (5) |
| REPORT | Core | 22 | ENGINE (4), REPORT_OUT (16), SSOT (2) |
| MEMORY | Surface | 9 | SNAPSHOT (8), SSOT (1) |
| STATE | Surface | 8 | CONFIG (1), DATA_IN (1), DATA_OUT (4), SSOT (2) |
| ARCH | Surface | 6 | CALIBRATION (1), ENGINE (3), SSOT (2) |
| SEMANTICS | Core | 3 | ENGINE (1), SSOT (2) |
| REASONING | Core | 3 | ENGINE (3) |
| USER | Surface | 3 | DASHBOARD (1), ENGINE (1), SSOT (1) |
| GOV | Surface | 2 | SSOT (1), STEERING (1) |
| DATA | Surface | 2 | DATA_IN (1), SSOT (1) |
| SIM | Surface | 2 | ENGINE (1), SSOT (1) |
| DEPLOY | Surface | 1 | RUNTIME (1) |


## Lifecycle Distribution

| Artifact Type | Total | States |
|--------------|-------|--------|
| CALIBRATION | 1 | active (1) |
| CONFIG | 1 | active (1) |
| DASHBOARD | 1 | active (1) |
| DATA_IN | 2 | active (2) |
| DATA_OUT | 28 | current (28) |
| ENGINE | 16 | active (15), development (1) |
| REPORT_OUT | 16 | current (16) |
| RUNTIME | 1 | active (1) |
| SNAPSHOT | 8 | archived (5), captured (3) |
| SSOT | 18 | canonical (18) |
| STEERING | 1 | active (1) |

## Violations Identified

### Summary

- **Total Violations**: 14
- **Critical**: 0
- **High**: 14
- **Medium**: 0
- **Low**: 0

### Unregistered Artifacts (13 violations, severity: high)

The following files in `docs/` and `reports/` directories lack YAML frontmatter metadata:

1. `docs/action_space_framework.md`
2. `docs/opportunity_engine_design.md`
3. `docs/portfolio_os_domainization_steering.md`
4. `docs/future_framework_backlog.md`
5. `docs/confidence_model.md`
6. `docs/report_pipeline_architecture.md`
7. `docs/deployment_intelligence_framework.md`
8. `docs/multilingual_rendering_framework.md`
9. `docs/trusted_signal_sources.md`
10. `reports/governance_stabilization_verification_2026-05-25.md`
11. `reports/task_1_execution_report.md`
12. `reports/governance_stabilization_preflight_2026-05-25.md`
13. `reports/governance_stabilization_audit_2026-05-25.md`

**Recommendation**: Add YAML frontmatter metadata or register in `artifact_registry.yaml`.

### Missing SSOT Reference (1 violation, severity: high)

- `main.py` (artifact_id: `main_py`) — Implementation artifact dependencies do not include SSOT reference.

**Recommendation**: Add SSOT specification artifact_id to dependencies field.

## Runtime Flow Analysis

| Metric | Value |
|--------|-------|
| Total Flows Detected | 109 |
| Allowed Flows | 93 |
| Forbidden Flows | 16 |
| Flow Health | 85.3% |
| Authority Chain Status | VIOLATIONS_DETECTED |

### Forbidden Flow Categories

1. **GOV → REASONING** (3 flows): Surface domain GOV cannot create meaning in core domain REASONING. Affects: `decision_engine_py`, `quality_engine_py`, `priority_engine_py`.

2. **SIGNALS → REPORT** (9 flows): Signal → Report skips semantic interpretation and reasoning. Affects multiple briefing outputs (allocation, attribution, correlation, early_warning, liquidity, narrative_dependency, regime).

3. **MEMORY → REPORT** (1 flow): Surface domain MEMORY cannot create meaning in core domain REPORT. Affects: `portfolio_memory_briefing_txt`.

4. **SIM → REPORT** (2 flows): Surface domain SIM cannot create meaning in core domain REPORT. Affects: `scenario_briefing_txt`.

5. **SIM → SIGNALS** (1 flow): Surface domain SIM cannot create meaning in core domain SIGNALS. Affects: `scenario_engine_xlsx`.

## Report-Value Health Score

| Metric | Value |
|--------|-------|
| Total Artifacts Assessed | 93 |
| With Report Value Declared | 0 |
| With Valid Report Value | 0 |
| Missing Report Value | 93 |
| Infrastructure-Heavy (drift) | 9 |
| Coverage Percentage | 0.0% |
| Infrastructure Drift | 9.7% |

**Note**: Report-value metadata is not yet populated for any artifact. This is expected at baseline — report-value justification will be added incrementally as the system matures.

## Recommendations

1. **[HIGH]** Register 13 unregistered artifact(s) — Unregistered artifacts lack governance and lifecycle tracking.
2. **[MEDIUM]** Add SSOT references to 1 artifact(s) — Derived and implementation artifacts must reference their canonical SSOT.

## Health Status Assessment

The system is in a **HEALTHY** state for the OBSERVABILITY phase:

- ✅ **Registration Coverage**: 100% of known artifacts are registered (93/93)
- ✅ **Domain Coverage**: All 12 domains have at least one artifact
- ✅ **Lifecycle Tracking**: All registered artifacts have valid lifecycle states
- ✅ **No Critical Violations**: Zero critical-severity violations
- ⚠️ **Unregistered Files**: 13 docs/reports files need frontmatter (new files added after registration tasks)
- ⚠️ **Runtime Flow Violations**: 16 forbidden flows detected (expected during FAST LANE phase)
- ℹ️ **Report Value**: Not yet populated (future enhancement)

## Requirements Satisfied

| Requirement | Description | Status |
|-------------|-------------|--------|
| 10.1 | Health report shows total/registered/unregistered artifacts | ✅ |
| 10.2 | Health report shows domain coverage distribution | ✅ |
| 10.3 | Health report shows lifecycle distribution | ✅ |
| 10.4 | Health report shows violations with severity levels | ✅ |
| 10.5 | Health report provides actionable recommendations | ✅ |
| 10.6 | Health report includes timestamp and version | ✅ |
| 10.7 | Health report indicates healthy/unhealthy status | ✅ |

## Related Files

- **Report Output**: `.domainization/reports/baseline_health_report_2026-05-26.yaml`
- **Health Reporter**: `.domainization/src/health_reporter.py`
- **CLI Health Commands**: `.domainization/src/cli_health_commands.py`
- **Violation Detector**: `.domainization/src/violation_detector.py`
- **Artifact Registry**: `.domainization/artifact_registry.yaml`
- **Domain Registry**: `.domainization/domain_registry.yaml`

## Usage

```bash
# Generate full health report
.domainization/domainization health

# Save report to file
.domainization/domainization health --output .domainization/reports/health_report.yaml

# Filter by domain
.domainization/domainization health --domain SIGNALS

# Show violations only
.domainization/domainization health --violations-only

# Exclude violations
.domainization/domainization health --no-violations
```

## Testing

```bash
# Run health reporter tests
.venv/bin/python -m pytest .domainization/src/test_health_reporter.py -v

# Run CLI health command tests
.venv/bin/python -m pytest .domainization/src/test_cli_health_commands.py -v
```
