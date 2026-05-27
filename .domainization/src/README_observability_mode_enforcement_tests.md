# Observability Mode Enforcement Tests

## Overview

Comprehensive test suite verifying that ALL validation observers respect observability mode during the FAST LANE REPORT MVP phase. The system operates in warning-only mode: violations are detected and logged for visibility, but commits are never blocked.

## What Was Verified

### 1. All 5 Observers Generate Warnings Only

Each observer was tested to confirm it produces `ValidationWarning` objects (not errors or blocking results) when violations are detected:

- **RegistrationValidator** — Unregistered artifacts, missing metadata, invalid schemas all produce warnings
- **DomainAssignmentValidator** — Invalid domains, wrong domain-type combinations produce warnings
- **LifecycleValidator** — Invalid transitions, deprecated modifications produce warnings
- **BoundaryAwarenessValidator** — Authority chain violations, cross-domain writes produce warnings
- **SSOTConsistencyValidator** — Multiple canonical SSOTs, missing references produce warnings

### 2. No Blocking Behavior Exists

- `ValidationResult` has no `success`, `blocked`, or `error` fields
- `ValidationWarning` is inherently non-blocking by design
- Even "critical" severity is still a warning, not a block
- The `ValidationOrchestrator` returns an `ObservabilityReport`, never raises blocking exceptions

### 3. Commits Always Proceed

- Pre-commit hook always exits with code 0
- No `exit 1` exists in the hook script (outside comments)
- Embedded Python script always calls `sys.exit(0)`
- Hook documents non-blocking behavior in comments

### 4. Violations Are Logged for Visibility

- All violations are captured in the warnings list
- Warnings include observer name, artifact ID, file path, warning code, message, and suggestion
- Report groups warnings by observer for clear visibility
- Performance is tracked (< 5 second target)

### 5. Configuration Validates Observability Mode

- `config.yaml` specifies `enforcement_mode: observability`
- `current_phase: fast_lane_report_mvp`
- `commit_gates_deferred: true`
- `report_development_unblocked: true`
- `registry_soft_validation_only: true`
- All 5 observers enabled

## Test Classes

| Class | Tests | Focus |
|-------|-------|-------|
| `TestRegistrationValidatorObservabilityMode` | 4 | Observer 1 warnings only |
| `TestDomainAssignmentValidatorObservabilityMode` | 3 | Observer 2 warnings only |
| `TestLifecycleValidatorObservabilityMode` | 3 | Observer 3 warnings only |
| `TestBoundaryAwarenessValidatorObservabilityMode` | 3 | Observer 4 warnings only |
| `TestSSOTConsistencyValidatorObservabilityMode` | 3 | Observer 5 warnings only |
| `TestValidationOrchestratorObservabilityMode` | 5 | Orchestrator never blocks |
| `TestPreCommitHookObservabilityMode` | 5 | Hook always exits 0 |
| `TestValidationResultSchemaObservability` | 3 | Schema design is non-blocking |
| `TestConfigDrivenEnforcementMode` | 6 | Config enforces observability |
| `TestObservabilityReportFormat` | 3 | Report format for visibility |

**Total: 38 tests**

## Testing

```bash
# Run from project root
.venv/bin/python -m pytest .domainization/src/test_observability_mode_enforcement.py -v

# Run specific test class
.venv/bin/python -m pytest .domainization/src/test_observability_mode_enforcement.py::TestValidationOrchestratorObservabilityMode -v

# Run with coverage
.venv/bin/python -m pytest .domainization/src/test_observability_mode_enforcement.py --cov=.domainization/src -v
```

## Requirements Satisfied

| Requirement | Description | How Verified |
|-------------|-------------|--------------|
| 5.9 | Commit gates deferred until MVP stabilizes | Config test + hook exits 0 |
| 5.10 | Governance shall not block report development | All observers produce warnings only |
| 9.8 | Registry enforcement remains soft-validation only | Config test + no blocking in validators |
| 9.9 | Enforcement relaxed until report value established | Observability mode active, no blocking |

## Related Files

- `.domainization/config.yaml` — Enforcement mode configuration
- `.domainization/src/validation_orchestrator.py` — Orchestrator (runs all observers)
- `.domainization/src/observer_registration.py` — Observer 1
- `.domainization/src/observer_domain_assignment.py` — Observer 2
- `.domainization/src/observer_lifecycle.py` — Observer 3
- `.domainization/src/observer_boundary_awareness.py` — Observer 4
- `.domainization/src/observer_ssot_consistency.py` — Observer 5
- `.domainization/src/validation_result.py` — Warning/Result schema
- `.domainization/hooks/pre-commit` — Pre-commit hook script
