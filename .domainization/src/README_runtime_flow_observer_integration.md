# Runtime Flow Observer Integration

## Overview

This document describes the integration of runtime flow detection into Observer 4
(Boundary Awareness Validator). The integration enables automatic detection of
forbidden authority chain flows when validating artifact dependencies.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           Observer 4: Boundary Awareness Validator           │
│                                                             │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │ Authority Chain  │    │   Runtime Flow Detector      │   │
│  │ Validation       │    │   (integrated from 18.1)     │   │
│  └─────────────────┘    └──────────────────────────────┘   │
│           │                          │                       │
│           ▼                          ▼                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ValidationWarning (W700-W704)           │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Health Reporter                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Runtime Flow Analysis Section                │   │
│  │  - Total flows detected                             │   │
│  │  - Allowed vs forbidden counts                      │   │
│  │  - Flow health percentage                           │   │
│  │  - Forbidden flow details                           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components Modified

### 1. `observer_boundary_awareness.py`

Added runtime flow detection to the validation pipeline:

- **`_check_runtime_flow_violations(artifact)`**: Checks artifact dependencies for
  forbidden flows using `RuntimeFlowDetector`. Generates W700-W704 warnings.
- **`_create_flow_violation_warning(artifact, flow)`**: Creates structured warnings
  with appropriate codes based on violation type.
- **`_get_flow_warning_code(flow)`**: Maps flow violations to specific warning codes.
- **`get_flow_traceability(artifact_id)`**: Traces the complete dependency chain
  showing the signal-to-report path (Req 14.7).
- **`_trace_dependency_chain(artifact_id, visited)`**: Recursive depth-first traversal
  of artifact dependencies with cycle prevention.
- **`detect_all_runtime_flows()`**: Scans all registered artifacts for flow analysis.

### 2. `health_reporter.py`

Added runtime flow analysis section to health reports:

- **`get_runtime_flow_analysis()`**: Scans all artifacts with dependencies, detects
  flows, and returns aggregated metrics including total/allowed/forbidden counts,
  health percentage, and forbidden flow details.
- **`generate_health_report()`**: Now includes `runtime_flow_analysis` section and
  summary fields `total_flows_detected` and `forbidden_flows_detected`.
- **`format_report_text()`**: Renders the "RUNTIME FLOW ANALYSIS" section in the
  human-readable text report with forbidden flow details.

### 3. `validation_result.py` (pre-existing)

Warning codes W700-W704 were already defined in task 18.1:

| Code | Meaning |
|------|---------|
| W700 | Generic forbidden runtime flow |
| W701 | Authority chain level skip |
| W702 | Backward authority flow |
| W703 | Surface domain to core domain flow |
| W704 | Meaning creation outside authority |

## Observability Mode

The system operates in **OBSERVABILITY MODE**:
- All forbidden flows generate **warnings only** (never block)
- Warnings are logged with full details (source, target, reason, suggestion)
- The `validate()` method always completes successfully
- Health reports visualize flow status for awareness

## Requirements Coverage

| Requirement | Implementation |
|-------------|---------------|
| 14.1 | Valid chain (SIGNALS→SEMANTICS→REASONING→REPORT) produces no warnings |
| 14.2 | Signal→Report dependency generates W700/W701 warning |
| 14.3 | Signal→Reasoning dependency generates W700/W701 warning |
| 14.4 | Dashboard→Semantic dependency generates W703 warning |
| 14.5 | Dashboard→Signal dependency generates W703 warning |
| 14.6 | Forbidden flows logged with details via Python logging |
| 14.7 | `get_flow_traceability()` shows complete signal-to-report chain |

## Usage

### Automatic Detection (via validate)

```python
from observer_boundary_awareness import BoundaryAwarenessValidator

validator = BoundaryAwarenessValidator(artifact_registry, domain_registry)
result = validator.validate()

# Check for flow warnings
flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
```

### Flow Traceability

```python
trace = validator.get_flow_traceability("my-report-artifact")
print(trace["visualization"])  # ASCII authority chain
print(trace["is_valid"])       # True/False
print(trace["violations"])     # List of violation descriptions
```

### Health Report

```python
from health_reporter import HealthReporter

reporter = HealthReporter(artifact_registry=registry, domain_registry=domains)
report = reporter.generate_health_report()

# Access flow analysis
flow_analysis = report["runtime_flow_analysis"]
print(f"Forbidden flows: {flow_analysis['forbidden_flows']}")
print(f"Flow health: {flow_analysis['flow_health_percentage']}%")
```

## Testing

Integration tests are in `test_runtime_flow_observer_integration.py` (23 tests):

```bash
.venv/bin/python -m pytest .domainization/src/test_runtime_flow_observer_integration.py -v
```

Test classes:
- `TestAllowedFlowsIntegration` - Valid authority chain produces no warnings
- `TestSignalToReportForbiddenIntegration` - Req 14.2
- `TestSignalToReasoningForbiddenIntegration` - Req 14.3
- `TestDashboardToSemanticForbiddenIntegration` - Req 14.4
- `TestDashboardToSignalForbiddenIntegration` - Req 14.5
- `TestForbiddenFlowLogging` - Req 14.6
- `TestFlowTraceability` - Req 14.7
- `TestHealthReportFlowVisualization` - Flow visualization in reports
- `TestEndToEndFlowDetection` - Full integration end-to-end
