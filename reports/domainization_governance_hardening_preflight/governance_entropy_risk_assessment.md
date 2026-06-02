# Governance Entropy Risk Assessment — Domainization-Governance-Hardening

## Document Purpose

Analysis of entropy sources, scaling risks, and governance drift potential.
All findings are evidence-backed with file references. No implementation recommendations.

---

## 1. Future Scaling Risks

### Current Scale

| Metric | Current Value | Source |
|--------|--------------|--------|
| Registered artifacts | 132 | `.domainization/artifact_registry.yaml` |
| Canonical domains | 12 | `.domainization/domain_registry.yaml` |
| Artifact types | 10 | `.domainization/lifecycle_state_machine.yaml` |
| Lifecycle states (total across types) | 38 | Same file — sum of all states |
| Deprecated artifacts with sunset dates | 15 | Repository state summary |
| Property-based tests | 27 | Repository state summary |
| Validation observers | 5 | `.domainization/src/validation_orchestrator.py` |

### Scaling Projections

| Scale Point | Artifacts | Impact on Current Architecture |
|-------------|-----------|-------------------------------|
| Current | 132 | Manageable — single YAML file, linear scans |
| 2x growth | ~264 | `artifact_registry.yaml` becomes unwieldy; `sunset_governance.py` scans all artifacts per evaluation |
| 500 artifacts | 500 | Linear scan in `_get_downstream_dependency_count()` becomes O(n²) per sunset evaluation; YAML file exceeds 5000+ lines |
| 1000 artifacts | 1000 | Health report generation may exceed 10-second budget; pre-commit hook validation slows significantly |

### Specific Scaling Bottlenecks

| Component | Scaling Concern | Evidence |
|-----------|----------------|----------|
| `governance/sunset_governance.py` | `_get_downstream_dependency_count()` iterates all artifacts for each deprecated artifact — O(n×d) where d=deprecated count | Lines scanning `self._artifacts` in nested loop |
| `.domainization/src/validation_orchestrator.py` | `_get_trackable_files_for_enforcement()` uses `rglob("*")` on 3 directories | File system scan grows with file count |
| `runtime/chain_validator.py` | `validate_all()` has 2-second budget — fixed regardless of section count | `VALIDATION_BUDGET_SECONDS: float = 2.0` |
| `.domainization/artifact_registry.yaml` | Single monolithic YAML file for all 132 artifacts | No sharding, no indexing, full parse on every load |
| `engines/pipeline_orchestrator.py` | `_emit_briefing_deprecation_warnings()` checks 14 files on disk per run | `os.path.exists()` × 14 per execution |

---

## 2. Ontology Risks

### Combinatorial Explosion Analysis

**Current ontology dimensions:**
- 10 artifact types × 12 domains × variable states per type

**State space calculation:**

| Artifact Type | States | × 12 Domains | Possible Combinations |
|---------------|--------|--------------|----------------------|
| SSOT | 4 | 12 | 48 |
| ENGINE | 4 | 12 | 48 |
| REPORT_OUT | 6 | 12 | 72 |
| DATA_IN | 3 | 12 | 36 |
| DATA_OUT | 3 | 12 | 36 |
| RUNTIME | 3 | 12 | 36 |
| DASHBOARD | 3 | 12 | 36 |
| SNAPSHOT | 2 | 12 | 24 |
| CONFIG | 3 | 12 | 36 |
| CALIBRATION | 3 | 12 | 36 |
| STEERING | 3 | 12 | 36 |
| **Total** | **37 unique** | | **444 possible type×domain×state combinations** |

**Current coverage**: 132 artifacts occupy 132 of 444 possible slots (30% coverage).

### Ontology Inconsistencies

| Inconsistency | Evidence | Entropy Risk |
|---------------|----------|--------------|
| REPORT_OUT has 6 states; most types have 3 | `lifecycle_state_machine.yaml` | Asymmetric governance complexity — REPORT_OUT requires 2x the transition logic |
| `regenerable_states` only defined for 3 types | REPORT_OUT, DATA_OUT, SNAPSHOT have it; 8 types don't | Unclear whether other types can be regenerated |
| `superseded` state exists only in REPORT_OUT and CALIBRATION | Different semantics in each | State name reuse with different meaning |
| Domain `cannot_own` vs `allowed_artifact_types` | Both constrain ownership from different angles | Redundant constraint systems that could diverge |

### Type System Fragmentation

| Classification System | Scope | Names Used |
|----------------------|-------|------------|
| `lifecycle_state_machine.yaml` types | 10 types | SSOT, ENGINE, REPORT_OUT, DATA_IN, DATA_OUT, RUNTIME, DASHBOARD, SNAPSHOT, CONFIG, CALIBRATION, STEERING |
| `canonical_boundary.py` names | 10 names | semantic_state_snapshot, reasoning_object, daily_report, deployment_matrix, run_context, provenance_metadata, orchestration_buffer, in_memory_transform, pre_validation_staging, intermediate_draft_reasoning |
| `domain_registry.yaml` types | Same 10 | References lifecycle types |
| `severity_taxonomy.py` levels | 6 levels | INFO, WARNING, DEGRADED, CRITICAL, CANONICAL_BREAK, DETERMINISTIC_FAILURE |
| `runtime_state_model.py` states | 8 states | HEALTHY, DEGRADED, UNAVAILABLE, INVALID, INCONSISTENT, COLLAPSED, DETERMINISTIC_FAILURE, CANONICAL_BREAK |

**Finding**: Three separate classification systems (lifecycle types, canonical boundary names, runtime states) operate independently with no formal mapping between them.

---

## 3. Governance Drift Risks

### Observability Mode Forever

**Current state**: `.domainization/config.yaml` sets `enforcement_mode: observability` with documented transition phases but no transition mechanism.

| Drift Scenario | Likelihood | Evidence |
|----------------|-----------|----------|
| Observability mode never transitions to `soft` | HIGH | No code reads `current_phase` to trigger transition; no criteria defined |
| Warnings accumulate without action | HIGH | All 5 observers emit warnings; no escalation path exists |
| New code ignores governance entirely | HIGH | CI doesn't run governance checks; developers may not install pre-commit hook |
| Governance config becomes stale | MEDIUM | `fast_lane_rules` section documents constraints that may no longer apply |
| Observer results diverge from reality | MEDIUM | Observers validate against registry; if registry is stale, validation is meaningless |

### Warning Fatigue Trajectory

| Time Period | Expected Warning Volume | Developer Response |
|-------------|------------------------|-------------------|
| Initial (now) | Low — system is new | Awareness, curiosity |
| 3 months | Growing — more artifacts, more violations | Selective attention |
| 6 months | High — accumulated technical debt | Warning blindness |
| 12 months | Very high — governance becomes noise | Complete disregard |

**Evidence for trajectory**: Pre-commit hook already exits 0 regardless of findings (`.domainization/hooks/pre-commit` final line: `exit 0`). The system is architecturally designed to be ignorable.

---

## 4. Artifact Explosion Risks

### Uncontrolled Growth Vectors

| Growth Vector | Current Rate | Control Mechanism |
|---------------|-------------|-------------------|
| New engine files in `engines/` | ~12 engines exist | Registration enforcement (warning only — W800) |
| New runtime files in `runtime/` | ~9 files exist | Registration enforcement (warning only — W800) |
| New governance files in `governance/` | ~5 files exist | Registration enforcement (warning only — W800) |
| New test files in `tests/` | ~27 files exist | Simplified registration (warning only — W802) |
| New `.domainization/src/` files | ~40+ files exist | **No registration enforcement at all** |
| Backup files in `.domainization/backups/` | 10 backups exist | **No governance awareness** |

### Self-Referential Growth

The domainization system itself creates artifacts that are not governed:

| Domainization Artifact | Governed? | Evidence |
|------------------------|-----------|----------|
| `.domainization/src/*.py` (40+ files) | No | Not in `full_registration_dirs` list in `RegistrationEnforcementPolicy` |
| `.domainization/reports/*.md` | No | Generated reports not registered |
| `.domainization/backups/*.yaml` | No | Backup files accumulate without governance |
| `.domainization/logs/` | No | Log directory exists but no retention policy |

**Finding**: The governance system does not govern itself. Its own artifacts (source code, reports, backups, logs) are outside the registration enforcement scope.

---

## 5. Lifecycle Complexity Risks

### State Count Asymmetry

| Artifact Type | States | Transitions | Complexity Score (states × transitions) |
|---------------|--------|-------------|----------------------------------------|
| REPORT_OUT | 6 | 6 | 36 |
| SSOT | 4 | 5 | 20 |
| ENGINE | 4 | 6 | 24 |
| DATA_IN | 3 | 3 | 9 |
| DATA_OUT | 3 | 2 | 6 |
| RUNTIME | 3 | 4 | 12 |
| DASHBOARD | 3 | 4 | 12 |
| SNAPSHOT | 2 | 1 | 2 |
| CONFIG | 3 | 4 | 12 |
| CALIBRATION | 3 | 3 | 9 |
| STEERING | 3 | 4 | 12 |

**REPORT_OUT complexity is 6x that of SNAPSHOT and 3x that of DATA_OUT.** This asymmetry means governance logic for REPORT_OUT artifacts requires significantly more validation paths.

### Transition Condition Ambiguity

All transition conditions in `lifecycle_state_machine.yaml` are human-readable strings:

```yaml
condition: "Author completes initial version and requests review"
condition: "Domain owner approves document as authoritative"
condition: "Superseded by new version or no longer applicable"
```

**Finding**: These conditions cannot be machine-evaluated. There is no programmatic way to determine if a transition condition is satisfied. Transitions are validated by checking if the from→to pair exists in the allowed list, but the *condition* itself is never evaluated.

---

## 6. CI Governance Risks

### Current CI Coverage

Source: `.github/workflows/python-app.yml`

| What CI Checks | What CI Misses |
|----------------|----------------|
| Python syntax (`compileall engines/`) | All other directories (runtime/, governance/, tests/) |
| 4 engine imports | 8+ other engine imports |
| — | 27 property-based tests |
| — | Health report generation |
| — | Registration enforcement |
| — | Lifecycle validation |
| — | Chain validator execution |
| — | Sunset governance evaluation |
| — | Schema version compatibility |
| — | Domain boundary validation |

### CI Governance Gap Quantification

| Governance Contract | Tests Exist? | CI Runs Them? |
|--------------------|-------------|---------------|
| Chain integrity (SIGNALS→SEMANTICS→REASONING→REPORT) | Yes (property tests) | **No** |
| Provenance parseability | Yes (`test_property_provenance_parseability.py`) | **No** |
| Runtime state model correctness | Yes (property tests) | **No** |
| Reasoning object schema | Yes (property tests) | **No** |
| Deployment matrix validation | Yes (property tests) | **No** |
| Confidence degradation formula | Yes (property tests) | **No** |
| Severity taxonomy ordering | Yes (property tests) | **No** |

**Finding**: 27 property-based tests exist that verify governance contracts. None execute in CI. The governance system has invested in verification but not in continuous verification.

---

## 7. Warning Blindness Risks

### Current Warning Sources

| Source | Warning Types | Volume per Run |
|--------|--------------|----------------|
| `validation_orchestrator.py` | W800, W801, W802 + 5 observer warnings | Variable — depends on violations |
| `pipeline_orchestrator.py` | Forbidden flow warnings (13 categories) | 13+ per pipeline run (fixed) |
| `pipeline_orchestrator.py` | Briefing deprecation warnings (14 files) | Up to 14 per run |
| `sunset_governance.py` | Deprecation warnings for 15 artifacts | 15 per evaluation |
| `engine_runner.py` | Single DeprecationWarning | 1 per call |
| `chain_validator.py` | Chain violation warnings | Variable |

### Estimated Warning Volume Per Pipeline Execution

| Warning Category | Minimum Count | Maximum Count |
|------------------|---------------|---------------|
| Forbidden flow warnings | 13 | 14 |
| Briefing deprecation warnings | 0 (files may not exist) | 14 |
| Engine runner deprecation | 1 | 1 |
| Sunset deprecation warnings | 15 | 15 |
| Chain validation violations | 0 | 9+ (one per section) |
| **Total per run** | **29** | **53+** |

**Finding**: A single pipeline execution can produce 29-53+ warnings, all of which are advisory. At this volume, individual warnings lose signal value. The system produces more governance noise than a developer can reasonably process per execution.

### Warning Deduplication

**No deduplication exists.** The same 13 forbidden flow warnings are emitted on every pipeline run. The same 15 sunset warnings are emitted on every evaluation. There is no mechanism to suppress known/accepted warnings or to escalate new/unexpected ones.

---

## 8. Entropy Summary

| Entropy Source | Current Severity | Trajectory |
|----------------|-----------------|------------|
| Observability-only mode (no enforcement path) | HIGH | Worsening — governance becomes noise over time |
| Warning volume (29-53+ per run) | HIGH | Worsening — grows with artifact count |
| Ontology fragmentation (3 classification systems) | MEDIUM | Stable — but blocks future integration |
| Lifecycle asymmetry (REPORT_OUT 6x complexity) | MEDIUM | Stable — but increases validation burden |
| Self-ungoverned governance system | MEDIUM | Worsening — governance artifacts grow without tracking |
| CI gap (0% governance verification) | CRITICAL | Stable — but means all other entropy is undetected in CI |
| Scaling bottlenecks (O(n²) sunset evaluation) | LOW (at current scale) | Worsening — becomes HIGH at 500+ artifacts |
| No warning deduplication | HIGH | Worsening — same warnings repeat indefinitely |

The primary entropy risk is the combination of high warning volume + no enforcement + no CI verification. This creates a system that generates governance information but has no mechanism to act on it, verify it, or reduce it over time.
