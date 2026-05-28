# Domainization-Governance-Hardening Spec Requirements Foundation

## Document Purpose

Synthesis of all pre-flight findings into a structured requirements foundation for Domainization-Governance-Hardening.
Defines scope, constraints, invariants, and expectations. No implementation approaches.

---

## 1. Findings Synthesis

### From Artifact 1 (Governance Runtime Pre-Flight Report)

- Governance maturity is at Level 1 (Observability Only) — no path to Level 2+
- 4 CRITICAL gaps, 6 HIGH gaps, 4 MEDIUM gaps, 1 LOW gap identified
- Zero enforcement exists — all governance is advisory
- CI validates ~10% of what runtime depends on
- Pipeline orchestrator depends on deprecated engine_runner (circular dependency)
- Confidence policy hot-reloads during execution without deployment

### From Artifact 2 (Domainization Runtime Boundary Analysis)

- `allowed_writers` and `allowed_readers` fields exist on all 132 artifacts but are never enforced
- `cannot_own` domain constraints are declarative only
- Artifacts can be mutated in any lifecycle state without prevention
- Canonical boundary operates on instance names; lifecycle operates on type names — no bridge
- Only 1 of 14 signal categories has full chain coverage (allocation)
- The governance system does not govern its own artifacts

### From Artifact 3 (Governance Entropy Risk Assessment)

- 29-53+ warnings per pipeline execution with no deduplication
- Three separate classification systems with no formal mapping
- REPORT_OUT has 6x the lifecycle complexity of SNAPSHOT
- Governance system's own files (40+ in `.domainization/src/`) are ungoverned
- O(n²) scaling risk in sunset evaluation at 500+ artifacts
- No mechanism to transition from observability to enforcement mode

### From Artifact 4 (Deployment Governance Gap Analysis)

- Deployment integrity score: ~1.0/10
- 27 property-based tests never execute in CI
- 4 YAML governance files never validated in CI
- 8 of 12 engines have no import validation
- Runtime assumes comprehensive integrity; CI provides minimal guarantees
- Divergence between CI validation and runtime assumptions is the primary risk

---

## 2. Domainization-Governance-Hardening Hardening Scope

### What Domainization-Governance-Hardening MUST Address

| Area | Scope Definition | Priority |
|------|-----------------|----------|
| A. CI Governance Integration | Tests and governance checks must execute in CI | P0 |
| B. Enforcement Mode Transition | Define and implement path from observability → soft → hard | P1 |
| C. Deployment Gate Framework | Blocking gates for critical governance violations | P1 |
| D. Lifecycle Enforcement | Prevent invalid transitions and read-only state mutations | P2 |
| E. Mutation Governance | Audit trail for artifact registry changes | P2 |
| F. Boundary Enforcement | Runtime checks for domain ownership and writer permissions | P2 |
| G. Warning Governance | Deduplication, escalation, and suppression of known warnings | P3 |

### What Domainization-Governance-Hardening MUST NOT Do

| Constraint | Rationale | Evidence |
|------------|-----------|----------|
| Must NOT break existing pipeline execution | Pipeline orchestrator is the production entry point | `engines/pipeline_orchestrator.py` — 10-step flow must continue working |
| Must NOT remove observability mode | Observability is the safety net during transition | `.domainization/config.yaml` — mode must remain available |
| Must NOT modify the 4-layer chain model | Chain model is architecturally stable | `domain_registry.yaml` — SIGNALS→SEMANTICS→REASONING→REPORT is canonical |
| Must NOT alter artifact registry schema | 132 artifacts depend on current schema | `.domainization/artifact_registry.yaml` — schema is stable |
| Must NOT remove deprecated engine_runner | Backward compatibility required | `engines/engine_runner.py` — emits DeprecationWarning but must remain callable |
| Must NOT change severity taxonomy values | Property tests verify ordering | `runtime/severity_taxonomy.py` — IntEnum values are tested |
| Must NOT change runtime state model values | Property tests verify aggregation | `runtime/runtime_state_model.py` — StrEnum values are tested |
| Must NOT block pipeline in observability mode | Core design principle | `.domainization/config.yaml`: "Governance shall not block report development" |

---

## 3. Governance Invariants

### Invariants That Must Always Be True

| ID | Invariant | Current Status | Evidence |
|----|-----------|----------------|----------|
| INV-1 | Every registered artifact has exactly one primary_domain | TRUE | `artifact_registry.yaml` schema requires `primary_domain` |
| INV-2 | Every artifact type has a defined lifecycle state machine | TRUE | `lifecycle_state_machine.yaml` defines all 10 types |
| INV-3 | The chain model is SIGNALS(L1)→SEMANTICS(L2)→REASONING(L3)→REPORT(L4) | TRUE | `domain_registry.yaml` authority_level field |
| INV-4 | Severity levels are strictly ordered (INFO < WARNING < ... < DETERMINISTIC_FAILURE) | TRUE | `severity_taxonomy.py` IntEnum ordering |
| INV-5 | Runtime states belong to orthogonal integrity dimensions | TRUE | `runtime_state_model.py` STATE_DIMENSIONS mapping |
| INV-6 | Provenance truth lives in sidecar YAML, not markdown | TRUE | `governance/provenance_schema.py` — `persist()` writes sidecar |
| INV-7 | Pipeline execution must complete (degraded output preferred over no output) | TRUE | `pipeline_orchestrator.py` — `handle_engine_failure()` continues |
| INV-8 | Observability mode never blocks commits or pipeline execution | TRUE | `.domainization/config.yaml` + pre-commit hook always exits 0 |
| INV-9 | Schema versions use semantic versioning (MAJOR.MINOR.PATCH) | TRUE | `schema_version_registry.py` — `_parse_version()` enforces format |
| INV-10 | Canonical artifacts are subject to full governance; transient are exempt | TRUE (declared) | `governance/canonical_boundary.py` — classification exists |

### Invariants That Domainization-Governance-Hardening Must Establish

| ID | New Invariant | Rationale |
|----|---------------|-----------|
| INV-11 | CI must execute all property-based tests on every push/PR | Currently 0% CI test coverage |
| INV-12 | Enforcement mode transitions must be explicit and auditable | No transition mechanism exists |
| INV-13 | Lifecycle state changes must be validated before persistence | Currently post-hoc only |
| INV-14 | Governance events must be persisted beyond single execution | Currently in-memory only |
| INV-15 | Warning volume must not grow unbounded (deduplication required) | Currently 29-53+ per run |

---

## 4. Required Runtime Guarantees

### Guarantees the System Must Enforce

| ID | Guarantee | Current State | Required State |
|----|-----------|---------------|----------------|
| RG-1 | All Python files compile without syntax errors | Partial (engines/ only) | All directories |
| RG-2 | All governance YAML files parse without errors | Not checked | Validated in CI |
| RG-3 | All property-based tests pass | Not run in CI | Run and pass in CI |
| RG-4 | Unregistered artifact count does not increase | Warning only (W801) | Blocking in CI |
| RG-5 | Lifecycle transitions follow state machine rules | Warning only | Blocking in soft/hard mode |
| RG-6 | Chain validator produces no CRITICAL violations | Warning only | Blocking in hard mode |
| RG-7 | Health report generates within 10-second budget | Not checked in CI | Verified in CI |
| RG-8 | Confidence policy formula produces valid results | Not checked in CI | Property test in CI |

---

## 5. Deployment Governance Expectations

### What CI Must Check (Minimum Viable Governance)

| Check | Type | Failure Behavior |
|-------|------|-----------------|
| `python -m compileall engines/ runtime/ governance/ -q` | Syntax | Block merge |
| `.venv/bin/python -m pytest tests/ -v` | Tests | Block merge |
| YAML parse of 4 governance files | Schema | Block merge |
| Import validation of all engines | Import | Block merge |
| Health report generation (time-bounded) | Governance | Warn (initially) |
| Registration enforcement baseline check | Governance | Warn (initially) |

### CI Pipeline Structure (Expected)

| Stage | Gates | Mode |
|-------|-------|------|
| Stage 1: Syntax & Imports | All-directory compile, all-engine imports | Always blocking |
| Stage 2: Tests | Full pytest suite (27+ property tests) | Always blocking |
| Stage 3: Governance | Health report, registration check, YAML validation | Configurable (warn → block) |
| Stage 4: Audit | Sunset report, boundary audit, mutation log | Informational |

---

## 6. Lifecycle Enforcement Expectations

### Transitions That Must Be Prevented

| From State | To State | Artifact Type | Why Prevent |
|------------|----------|---------------|-------------|
| `archived` | Any | All types | Archived = frozen; no modification allowed |
| `superseded` | Any | REPORT_OUT, CALIBRATION | Superseded = replaced; no resurrection |
| `deprecated` | `active`/`current` | All types | Deprecated cannot un-deprecate without explicit governance decision |
| Any `read_only_state` | Content modification | All types | Read-only means metadata-only changes |

### Transitions That Must Be Audited (Not Prevented)

| From State | To State | Artifact Type | Why Audit |
|------------|----------|---------------|-----------|
| `canonical` | `draft` | SSOT | Major revision — requires justification |
| `active` | `deprecated` | ENGINE | Engine removal — requires replacement path |
| `current` | `deprecated` | REPORT_OUT | Report deprecation — requires sunset plan |
| Any state | `deprecated` | Any | All deprecations should be tracked |

---

## 7. Mutation Governance Expectations

### What Audit Trail Is Needed

| Mutation Type | Required Tracking | Persistence |
|---------------|-------------------|-------------|
| Artifact registry entry added | Who, when, which artifact, initial state | Per-commit structured log |
| Artifact registry entry modified | Who, when, which fields changed, old→new values | Per-commit structured log |
| Lifecycle state transition | Who, when, from→to, whether valid per state machine | Governance event store |
| Domain assignment change | Who, when, old domain→new domain | Governance event store |
| Enforcement mode change | Who, when, old mode→new mode, justification | Governance event store |
| Sunset date reached | When, which artifact, dependency count, action taken | Governance event store |

### Mutation Sources to Track

| Source | Current Tracking | Required Tracking |
|--------|-----------------|-------------------|
| Human edit of `artifact_registry.yaml` | Git diff only | Structured change record |
| Pipeline-generated artifacts | `_generated_artifacts` list (in-memory) | Persisted generation log |
| Confidence policy reload | `_policy_change_log` (in-memory) | Persisted policy audit |
| Health report findings | Printed to stdout | Persisted governance event |
| Pre-commit hook warnings | Printed to terminal | Persisted (optional) |

---

## 8. Requirement Areas (A through G)

### Area A: CI Governance Integration

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| A.1 | CI must execute full pytest suite on push and PR | P0 | 27 property tests never run in CI |
| A.2 | CI must validate syntax of all Python directories | P0 | Only `engines/` checked currently |
| A.3 | CI must validate all governance YAML files parse correctly | P0 | 4 YAML files never validated |
| A.4 | CI must validate all engine imports (not just 4) | P0 | 8 engines unchecked |
| A.5 | CI must generate health report within time budget | P1 | No health visibility at deploy |
| A.6 | CI must report registration enforcement status | P1 | W801 baseline tracking needed |

### Area B: Enforcement Mode Transition

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| B.1 | Define explicit criteria for observability→soft transition | P1 | No criteria exist in config |
| B.2 | Define explicit criteria for soft→hard transition | P1 | No criteria exist in config |
| B.3 | Enforcement mode changes must be auditable | P1 | No audit trail for mode changes |
| B.4 | Each mode must have defined behavior for each observer | P1 | Observers only know "warning" behavior |
| B.5 | Mode transition must not require code changes | P2 | Should be config-driven |

### Area C: Deployment Gate Framework

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| C.1 | Define blocking vs warning gates per enforcement mode | P1 | No gate framework exists |
| C.2 | Gates must be independently configurable | P1 | All-or-nothing is too rigid |
| C.3 | Gate failures must produce structured output | P1 | Current output is unstructured text |
| C.4 | Gates must complete within defined time budgets | P1 | Performance targets exist but aren't enforced |
| C.5 | Gate results must be persisted for audit | P2 | Currently ephemeral |

### Area D: Lifecycle Enforcement

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| D.1 | Invalid lifecycle transitions must be prevented (not just warned) in soft/hard mode | P2 | Currently warning-only |
| D.2 | Read-only state artifacts must reject content modifications | P2 | No write-time check exists |
| D.3 | Regenerable state must be checked before engine overwrites | P2 | No regeneration gate exists |
| D.4 | Transition conditions must have machine-evaluable criteria | P3 | Currently human-readable strings only |
| D.5 | All state transitions must be logged with timestamp and actor | P2 | No transition persistence |

### Area E: Mutation Governance

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| E.1 | Artifact registry changes must produce structured change records | P2 | Only git diff available |
| E.2 | Governance events must persist beyond single execution | P2 | Currently in-memory only |
| E.3 | Policy changes (confidence, enforcement mode) must be audited | P2 | `_policy_change_log` is ephemeral |
| E.4 | Sunset date transitions must be recorded | P2 | Phase changes are evaluated but not persisted |
| E.5 | Generated artifact list must be persisted per run | P3 | `_generated_artifacts` is ephemeral |

### Area F: Boundary Enforcement

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| F.1 | `allowed_writers` must be checked before artifact modification in soft/hard mode | P2 | Field exists but never enforced |
| F.2 | `cannot_own` must be checked before domain assignment in soft/hard mode | P2 | Field exists but never enforced |
| F.3 | Canonical boundary must support runtime discovery (not hardcoded sets) | P2 | `CANONICAL_ARTIFACTS` frozenset has only 6 items |
| F.4 | Cross-domain interactions must be detected and logged | P3 | No cross-domain detection exists |
| F.5 | Transient→canonical promotion must be automatic when boundary is crossed | P3 | `enforce_boundary()` is opt-in |

### Area G: Warning Governance

| Req ID | Requirement | Priority | Evidence for Need |
|--------|-------------|----------|-------------------|
| G.1 | Known/accepted warnings must be suppressible | P3 | Same 13 forbidden flow warnings repeat every run |
| G.2 | New/unexpected warnings must be escalated | P3 | All warnings treated equally |
| G.3 | Warning volume must be bounded (deduplication) | P3 | 29-53+ warnings per run |
| G.4 | Warning trends must be trackable over time | P3 | No historical warning data |
| G.5 | Warning severity must map to enforcement mode behavior | P2 | `SEVERITY_DEFINITIONS` defines `blocks_pipeline_hard_mode` but nothing reads it |

---

## 9. Dependency Order for Implementation

### Domainization-Governance-Hardening Internal Dependencies

```
A (CI Integration) ← independent, can start immediately
B (Enforcement Mode) ← depends on A (CI must run checks before they can block)
C (Deployment Gates) ← depends on A + B (gates need CI + mode awareness)
D (Lifecycle Enforcement) ← depends on B (needs enforcement mode to determine behavior)
E (Mutation Governance) ← depends on D (lifecycle changes are primary mutation source)
F (Boundary Enforcement) ← depends on B + D (needs mode + lifecycle awareness)
G (Warning Governance) ← depends on A + B + C (needs CI + mode + gates to be meaningful)
```

### Critical Path

```
A → B → C → D → E
         ↘ F
              → G
```

**Area A is the foundation.** Without CI executing tests and governance checks, no other area can be verified continuously.

---

## 10. Success Criteria for Domainization-Governance-Hardening

| Criterion | Measurable Target |
|-----------|-------------------|
| CI test execution | 27/27 property tests pass in CI on every push |
| CI syntax coverage | All Python directories validated (not just engines/) |
| CI YAML validation | All 4 governance YAML files validated |
| Enforcement mode path | Documented criteria for observability→soft→hard with config-only transition |
| Lifecycle enforcement | At least `archived` and `superseded` states prevent content modification |
| Mutation audit | Registry changes produce structured change records |
| Warning governance | Known warnings deduplicated; new warnings escalated |
| Deployment integrity score | Improve from 1.0/10 to ≥6.0/10 |
| Governance maturity | Advance from Level 1 (Observable) to Level 2 (Auditable) minimum |
