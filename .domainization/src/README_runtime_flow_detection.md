# Runtime Flow Detection

## Overview

The Runtime Flow Detector validates runtime flows between domains based on artifact dependencies. It enforces authority chains — who can create meaning, not just data movement — and operates in **observability mode** (warnings only, no blocking).

## Core Concept: Authority Chains

The system enforces a core reasoning chain with strict authority levels:

```
SIGNALS (L1) → SEMANTICS (L2) → REASONING (L3) → REPORT (L4)
```

- **SIGNALS** (Level 1): Creates raw structured signals from market data
- **SEMANTICS** (Level 2): Interprets signals into semantic meaning
- **REASONING** (Level 3): Creates conclusions from semantic states
- **REPORT** (Level 4): Renders reasoning into human-readable text

Authority flows **forward only**. Each domain can only create meaning at its own level.

## Allowed Flows

| Source | Target | Reason |
|--------|--------|--------|
| SIGNALS | SEMANTICS | Adjacent authority step (L1 → L2) |
| SEMANTICS | REASONING | Adjacent authority step (L2 → L3) |
| REASONING | REPORT | Adjacent authority step (L3 → L4) |
| Same domain | Same domain | Internal flow |
| Surface | Surface | No authority chain constraint |

## Forbidden Flows

| Source | Target | Requirement | Reason |
|--------|--------|-------------|--------|
| SIGNALS | REPORT | 14.2 | Skips semantic interpretation and reasoning |
| SIGNALS | REASONING | 14.3 | Skips semantic interpretation |
| USER (Dashboard) | SEMANTICS | 14.4 | Dashboard cannot create semantic truth |
| USER (Dashboard) | SIGNALS | 14.5 | Dashboard cannot generate signals |
| Any backward flow | — | 14.8 | Authority flows forward only |
| Surface domain | Core domain | 14.10 | Cannot create meaning outside authority |

## Files

| File | Purpose |
|------|---------|
| `runtime_flow_detector.py` | Main implementation |
| `test_runtime_flow_detector.py` | Unit tests (49 tests) |

## Usage

```python
from runtime_flow_detector import RuntimeFlowDetector, FlowStatus

detector = RuntimeFlowDetector()

# Check a single flow
flow = detector.detect_flow("SIGNALS", "SEMANTICS")
assert flow.status == FlowStatus.ALLOWED

# Validate a full path
result = detector.validate_flow_path(["SIGNALS", "SEMANTICS", "REASONING", "REPORT"])
assert not result.has_violations()

# Detect flows from artifact dependencies
result = detector.detect_flows_from_dependencies(
    artifact_id="semantic-state-1",
    artifact_domain="SEMANTICS",
    dependencies=[{"artifact_id": "signal-1", "domain": "SIGNALS"}]
)

# Visualize authority chain
viz = detector.visualize_authority_chain(["SIGNALS", "SEMANTICS", "REASONING", "REPORT"])
print(viz.render_ascii())
# Authority Chain: SIGNALS (L1) → SEMANTICS (L2) → REASONING (L3) → REPORT (L4)
# Status: ✓ VALID
```

## API Reference

### `RuntimeFlowDetector`

- `detect_flow(source_domain, target_domain, artifact_id=None)` → `RuntimeFlow`
- `detect_flows_from_dependencies(artifact_id, artifact_domain, dependencies)` → `FlowDetectionResult`
- `validate_flow_path(flow_path)` → `FlowDetectionResult`
- `visualize_authority_chain(flow_path)` → `AuthorityChainVisualization`
- `get_allowed_flow_definitions()` → `List[Dict]`
- `get_forbidden_flow_definitions()` → `List[Dict]`

### Data Classes

- `RuntimeFlow`: Detected flow with status, reason, and suggestion
- `FlowDetectionResult`: Collection of flows with counts and timing
- `AuthorityChainVisualization`: Visual representation with validity check
- `FlowStep`: Single step in a chain with domain and authority level

## Requirements Coverage

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| 14.1 | Signal → Semantic → Reasoning → Report allowed | `ALLOWED_FLOWS` set + `validate_flow_path()` |
| 14.2 | Signal → Report forbidden | `FORBIDDEN_FLOWS` dict |
| 14.3 | Signal → Reasoning forbidden | `FORBIDDEN_FLOWS` dict |
| 14.4 | Dashboard → Semantic Truth forbidden | `FORBIDDEN_FLOWS` dict |
| 14.5 | Dashboard → Signal Generation forbidden | `FORBIDDEN_FLOWS` dict |
| 14.8 | Flows represent authority chains | Forward-only enforcement in `detect_flow()` |
| 14.9 | Meaning follows authority chain | `validate_flow_path()` validates full chain |
| 14.10 | Block meaning outside authority | Surface-to-core detection in `detect_flow()` |

## Observability Mode

All detection operates in **warning mode only**. The detector:
- Returns `FlowStatus.FORBIDDEN` for invalid flows
- Provides actionable suggestions for resolution
- Never blocks execution
- Tracks execution time for performance monitoring
