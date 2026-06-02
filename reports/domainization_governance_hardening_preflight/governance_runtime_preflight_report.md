# Governance Runtime Pre-Flight Report — Domainization-Governance-Hardening

## Document Purpose

Pre-flight analysis of the governance runtime system state prior to Domainization-Governance-Hardening hardening.
All findings are evidence-backed with file references. No implementation recommendations.

---

## 1. Dependency Map

### Core Runtime Dependencies

| Component | Depends On | Depended On By |
|-----------|-----------|----------------|
| `engines/pipeline_orchestrator.py` | `runtime/run_context.py`, `runtime/reasoning_object.py`, `runtime/confidence_policy.py`, `runtime/pipeline_result.py`, `runtime/runtime_state_model.py`, `runtime/semantic_state_store.py`, `runtime/severity_taxonomy.py`, `governance/provenance_schema.py`, `engines/engine_runner.py`, `engines/semantic_engine.py` | External callers (entry point) |
| `runtime/chain_validator.py` | `runtime/severity_taxonomy.py` (implicit via governance violations) | `engines/pipeline_orchestrator.py` (Step 8) |
| `runtime/runtime_state_model.py` | None (leaf module) | `engines/pipeline_orchestrator.py`, `runtime/pipeline_result.py` |
| `runtime/confidence_policy.py` | `governance/confidence_policy.yaml` | `engines/pipeline_orchestrator.py` (Step 5) |
| `governance/sunset_governance.py` | `.domainization/artifact_registry.yaml` | `.domainization/src/health_reporter.py` |
| `governance/canonical_boundary.py` | None (hardcoded sets) | Runtime classification callers |
| `.domainization/src/validation_orchestrator.py` | `artifact_registry.py`, `domain_registry.py`, `lifecycle_manager.py`, 5 observer modules | `.domainization/hooks/pre-commit` |

### Configuration Dependencies

| Config File | Consumed By |
|-------------|-------------|
| `.domainization/config.yaml` | `engines/pipeline_orchestrator.py`, `.domainization/hooks/pre-commit` |
| `.domainization/domain_registry.yaml` | `.domainization/src/validation_orchestrator.py`, `.domainization/src/health_reporter.py` |
| `.domainization/artifact_registry.yaml` | `governance/sunset_governance.py`, `.domainization/src/validation_orchestrator.py` |
| `.domainization/lifecycle_state_machine.yaml` | `.domainization/src/validation_orchestrator.py` |
| `governance/confidence_policy.yaml` | `runtime/confidence_policy.py` |

---

## 2. Identified Gaps

### CRITICAL Severity

| # | Gap | Evidence | Impact |
|---|-----|----------|--------|
| 1 | CI does NOT run tests | `.github/workflows/python-app.yml` — only `compileall` and 4 import checks | 27 property-based tests never execute in CI; governance contracts unverified |
| 2 | CI does NOT run governance checks | `.github/workflows/python-app.yml` — no health report, no registration enforcement step | Governance violations can merge to main undetected |
| 3 | No deployment gates | `.github/workflows/python-app.yml` — no blocking step exists | Broken governance can deploy without any barrier |
| 4 | Enforcement mode permanently `observability` | `.domainization/config.yaml` line: `enforcement_mode: observability` — no transition logic exists | Governance system can never enforce; all violations are advisory forever |

### HIGH Severity

| # | Gap | Evidence | Impact |
|---|-----|----------|--------|
| 5 | Pre-commit hook is optional and bypassable | `.domainization/hooks/pre-commit` — requires manual install via `install_hook.sh`, always exits 0, bypassable with `--no-verify` | Local governance checks are entirely opt-in |
| 6 | Lifecycle transitions are descriptive only | `.domainization/lifecycle_state_machine.yaml` — defines transitions but `lifecycle_manager.py` validates without preventing | Artifacts can be mutated in read-only states without enforcement |
| 7 | Registration enforcement is warning-only | `.domainization/src/validation_orchestrator.py` lines W800/W801/W802 — all emit warnings, never block | Unregistered artifacts accumulate without consequence |
| 8 | Sunset governance is read-only | `governance/sunset_governance.py` — `should_generate()` returns bool but nothing calls it to prevent generation | Deprecated artifacts continue generating past sunset date |
| 9 | No artifact mutation audit trail | `.domainization/artifact_registry.yaml` — no commit-level tracking of changes | Registry modifications are invisible in git history beyond diff |
| 10 | Canonical boundary is hardcoded | `governance/canonical_boundary.py` — `CANONICAL_ARTIFACTS` frozenset with 6 items, `TRANSIENT_ARTIFACTS` with 4 items | New artifact types raise ValueError; no runtime discovery |

### MEDIUM Severity

| # | Gap | Evidence | Impact |
|---|-----|----------|--------|
| 11 | Schema versions all at 1.0.0 | `governance/schema_version_registry.py` — all 5 schemas at "1.0.0" | No version evolution strategy; breaking changes have no migration path |
| 12 | No governance event persistence | `engines/pipeline_orchestrator.py` — `_severity_events` is a list that exists only during execution | Events lost after pipeline run; no historical governance audit |
| 13 | State transitions not persisted | `.domainization/src/validation_orchestrator.py` — validates transitions but doesn't persist state change records | Lifecycle history is invisible |
| 14 | Domain ownership not enforced at write time | `.domainization/artifact_registry.yaml` — `allowed_writers` field exists but no runtime check prevents writes | Any domain can modify any artifact |

### LOW Severity

| # | Gap | Evidence | Impact |
|---|-----|----------|--------|
| 15 | No mutation tracking | `.domainization/artifact_registry.yaml` — `last_modified` field is manually maintained | Modification dates may be stale or incorrect |

---

## 3. Risk Classification Summary

| Severity | Count | Percentage |
|----------|-------|------------|
| CRITICAL | 4 | 27% |
| HIGH | 6 | 40% |
| MEDIUM | 4 | 27% |
| LOW | 1 | 6% |

---

## 4. Governance Maturity Analysis

### Current Position: Level 1 — Observability Only

The governance system is at the lowest maturity level:

| Maturity Level | Description | Current State |
|----------------|-------------|---------------|
| Level 0: Absent | No governance infrastructure | ✗ Passed |
| Level 1: Observable | Governance detects violations, reports them, never blocks | ✓ **Current** |
| Level 2: Auditable | Governance persists events, creates audit trails | ✗ Not reached |
| Level 3: Enforceable | Governance can block invalid operations | ✗ Not reached |
| Level 4: Autonomous | Governance self-heals and auto-remediates | ✗ Not reached |

**Evidence**: `.domainization/config.yaml` explicitly states `enforcement_mode: observability` with documented phases (`fast_lane_report_mvp` → `post_mvp_transition` → `full_enforcement`) but no transition mechanism exists.

### Maturity Gaps

1. **No event persistence** — Cannot audit historical governance decisions (blocks Level 2)
2. **No enforcement mechanism** — Config supports `soft`/`hard` modes but no code path implements blocking (blocks Level 3)
3. **No transition trigger** — No criteria defined for moving from `observability` to `soft` mode

---

## 5. Runtime Enforcement Analysis

### What Enforces (Blocks Execution)

| Component | Enforcement | Evidence |
|-----------|-------------|----------|
| `runtime/chain_validator.py` | 2-second budget timeout | Line: `VALIDATION_BUDGET_SECONDS: float = 2.0` — marks remaining sections unvalidated but does NOT stop pipeline |
| `engines/pipeline_orchestrator.py` | 60-second engine timeout | `ENGINE_TIMEOUT_SECONDS = 60` — raises `EngineTimeoutError` but `handle_engine_failure()` continues pipeline |
| `runtime/reasoning_object.py` | Schema validation | `validate()` method raises on invalid schema — actual enforcement |
| `runtime/deployment_matrix.py` | Schema validation | `validate()` returns errors list — caller must check |

### What Only Warns (Never Blocks)

| Component | Warning Type | Evidence |
|-----------|-------------|----------|
| `engines/pipeline_orchestrator.py` | Forbidden flow detection | `detect_forbidden_flows()` — logs `Severity.WARNING`, never blocks |
| `.domainization/hooks/pre-commit` | All validation | Always exits 0 regardless of findings |
| `.domainization/src/validation_orchestrator.py` | All 5 observers | `ObservabilityReport` — reports warnings, never raises |
| `governance/sunset_governance.py` | Deprecation warnings | `emit_deprecation_warnings()` — uses `warnings.warn()`, never blocks |
| `governance/canonical_boundary.py` | Boundary classification | `classify()` raises ValueError for unknown artifacts but `enforce_boundary()` only returns strings |
| `runtime/chain_validator.py` | Chain violations | All violations have `"severity": "warning"` hardcoded |

---

## 6. Deployment Integrity Analysis

### Current Deployment Guarantees

| Check | Scope | Blocks Deploy? | Evidence |
|-------|-------|----------------|----------|
| Python syntax validation | `engines/` only | Yes | `.github/workflows/python-app.yml`: `python -m compileall engines/ -q` |
| 4 critical imports | allocation, report, regime, scoring engines | Yes | `.github/workflows/python-app.yml`: 4 `python -c` import statements |

### Missing Deployment Guarantees

| Missing Check | Impact |
|---------------|--------|
| Test execution (27 property-based tests) | Governance contracts unverified |
| Health report generation | System health unknown at deploy time |
| Registration enforcement | Unregistered artifacts can deploy |
| Chain validator execution | Provenance integrity unverified |
| Lifecycle state validation | Invalid transitions can deploy |
| Sunset governance evaluation | Expired artifacts continue generating |
| Runtime state model verification | State dimension integrity unverified |

---

## 7. Lifecycle Enforcement Analysis

### Descriptive vs Enforceable

| Lifecycle Aspect | Status | Evidence |
|------------------|--------|----------|
| State definitions | Descriptive | `.domainization/lifecycle_state_machine.yaml` — defines states per type |
| Transition rules | Descriptive | Same file — `transitions` array with `condition` strings (human-readable, not machine-evaluated) |
| Modifiable states | Descriptive | Same file — `modifiable_states` lists exist but nothing checks before write |
| Read-only states | Descriptive | Same file — `read_only_states` lists exist but nothing prevents modification |
| Regenerable states | Descriptive | Same file — `regenerable_states` defined but no runtime gate |

### Lifecycle Inconsistencies

| Artifact Type | States Count | Complexity |
|---------------|-------------|------------|
| REPORT_OUT | 6 states | Highest — includes `superseded`, `sunset_pending` |
| SSOT | 4 states | Standard |
| ENGINE | 4 states | Standard |
| DATA_IN | 3 states | Minimal |
| DATA_OUT | 3 states | Minimal |
| SNAPSHOT | 2 states | Minimal |
| CONFIG | 3 states | Standard |
| CALIBRATION | 3 states | Standard |
| STEERING | 3 states | Standard |
| RUNTIME | 3 states | Standard |
| DASHBOARD | 3 states | Standard |

**Observation**: REPORT_OUT has 2x the state complexity of most types, with unique states (`sunset_pending`, `superseded`) not shared by any other type. This creates asymmetric governance burden.

---

## 8. Cross-System Coupling Analysis

### Hidden Coupling Points

1. **Pipeline Orchestrator ↔ Engine Runner**: `pipeline_orchestrator.py` imports and calls `run_all_engines()` from the deprecated `engine_runner.py` — the "new" system depends on the "old" system.

2. **Confidence Policy ↔ YAML Config**: `runtime/confidence_policy.py` hot-reloads from `governance/confidence_policy.yaml` during pipeline execution (Step 5) — runtime behavior changes without code deployment.

3. **Validation Orchestrator ↔ File System**: `.domainization/src/validation_orchestrator.py` scans `runtime/`, `governance/`, `tests/` directories at runtime — file system structure is a governance contract.

4. **Sunset Governance ↔ Artifact Registry**: `governance/sunset_governance.py` reads the full artifact registry to evaluate phases — registry size directly impacts sunset evaluation performance.

5. **Chain Validator ↔ Provenance Sidecar**: `runtime/chain_validator.py` depends on sidecar YAML file existence — if Step 7 (persist provenance) fails, Step 8 (chain validation) cannot execute.

---

## 9. Summary Assessment

The governance runtime system has comprehensive **detection** capabilities but zero **enforcement** capabilities. It can identify 15+ categories of violations across 5 observers but cannot prevent any of them. The CI pipeline validates only that Python files compile and 4 engines import successfully — it does not verify any governance contract, run any test, or evaluate any health metric.

The system is architecturally ready for enforcement (config supports modes, observers exist, severity taxonomy is defined) but operationally stuck at observability level with no defined transition criteria or mechanism.
