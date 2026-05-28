# Phase A — Foundation: Data Contracts

## Overview

Phase A establishes the data contracts and shared vocabulary for the Portfolio OS report runtime integrity system. These modules form the foundation upon which the Chain Runtime (Phase B), Semantic Expansion (Phase C), and Compatibility Cleanup (Phase D) are built.

All modules enforce the **FAST LANE REPORT MVP** constraint: no plugin systems, no generic orchestration kernels, no enterprise governance engines. Each component is a concrete Python module with a single responsibility.

## Architecture

```
portfolio_os_v1/
├── runtime/                          # Runtime data contracts (ARCH/GOV domain)
│   ├── __init__.py
│   ├── severity_taxonomy.py          # Canonical severity levels (IntEnum)
│   ├── runtime_state_model.py        # Multi-dimensional runtime states (StrEnum)
│   ├── reasoning_object.py           # Reasoning Object schema + TemporalValidity
│   ├── run_context.py                # Temporal snapshot for pipeline consistency
│   ├── semantic_state_store.py       # Immutable archive persistence layer
│   ├── pipeline_result.py            # Typed pipeline output contract
│   └── confidence_policy.py          # Configurable degradation formula
├── governance/                       # Governance contracts (GOV domain)
│   ├── __init__.py
│   ├── schema_version_registry.py    # Version tracking for all schemas
│   ├── provenance_schema.py          # Provenance structure + sidecar persistence
│   ├── canonical_boundary.py         # Canonical vs transient classification
│   └── confidence_policy.yaml        # Default confidence degradation config
└── tests/                            # Property-based tests (Hypothesis)
    ├── test_property_pipeline_state_aggregation.py
    ├── test_property_reasoning_object_schema.py
    ├── test_property_schema_version_compatibility.py
    ├── test_property_run_context_temporal_consistency.py
    ├── test_property_provenance_parseability.py
    ├── test_property_confidence_degradation.py
    ├── test_property_canonical_boundary_enforcement.py
    ├── test_property_semantic_state_round_trip.py
    └── test_property_semantic_delta_correctness.py
```

## Components

### Runtime Domain (`runtime/`)

| Module | Responsibility | Requirements |
|--------|---------------|--------------|
| `severity_taxonomy.py` | Single canonical location for 6 severity levels (INFO → DETERMINISTIC_FAILURE) | 17.1, 17.3, 17.5 |
| `runtime_state_model.py` | 8 runtime states across 5 orthogonal integrity dimensions + aggregation | 18.1, 18.2, 18.3, 18.5 |
| `reasoning_object.py` | Formal schema for REASONING→REPORT interface with validation | 9.1, 9.2 |
| `run_context.py` | Temporal snapshot with SHA-256 hashing for pipeline consistency | 8.1, 8.2, 8.4, 8.6 |
| `semantic_state_store.py` | Immutable snapshot archive with delta computation and historical replay | 12.1–12.6 |
| `pipeline_result.py` | Typed dataclass contract for pipeline execution output | 15.1 |
| `confidence_policy.py` | Configurable formula: `max(floor, ceiling - penalty × N)` | 19.1–19.4 |

### Governance Domain (`governance/`)

| Module | Responsibility | Requirements |
|--------|---------------|--------------|
| `schema_version_registry.py` | Version constants for 5 schemas + compatibility validation | 23.1–23.4 |
| `provenance_schema.py` | Section provenance structure + canonical sidecar file persistence | 13.1, 13.3, 13.5 |
| `canonical_boundary.py` | Classify artifacts as canonical/transient with promotion logic | 16.1–16.5 |

## Design Decisions (Hardenings)

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Multi-dimensional state model | Runtime states are NOT linearly ordered — orthogonal integrity dimensions |
| 5 | Explicit TemporalValidity model | Named fields (valid_from, valid_until, stale_after) replace anonymous tuples |
| 6 | Immutable snapshot archive | Semantic snapshots are NEVER destructively overwritten |
| 7 | Typed PipelineResult | Explicit dataclass replaces implicit dict-based orchestration outputs |
| 8 | Semantic determinism scope | Byte-identity for governed YAML; semantic determinism for markdown |

## Property-Based Tests

All correctness properties use **Hypothesis** (mandatory). Each property validates specific requirements:

| Property | Test File | Validates |
|----------|-----------|-----------|
| P20: Pipeline State Aggregation | `test_property_pipeline_state_aggregation.py` | Req 18.5 |
| P11: Reasoning Object Schema | `test_property_reasoning_object_schema.py` | Req 9.1, 9.4, 9.5 |
| P21: Schema Version Compatibility | `test_property_schema_version_compatibility.py` | Req 23.2, 23.4 |
| P14: Run_Context Temporal Consistency | `test_property_run_context_temporal_consistency.py` | Req 8.1, 8.3 |
| P10: Provenance Parseability | `test_property_provenance_parseability.py` | Req 13.3, 24.3 |
| P12: Confidence Degradation | `test_property_confidence_degradation.py` | Req 11.3, 19.3 |
| P18: Canonical Boundary Enforcement | `test_property_canonical_boundary_enforcement.py` | Req 16.4, 16.5 |
| P15: Semantic State Round-Trip | `test_property_semantic_state_round_trip.py` | Req 12.1, 12.2 |
| P16: Semantic Delta Correctness | `test_property_semantic_delta_correctness.py` | Req 12.3, 12.5 |

## Running Tests

```bash
# All Phase A unit tests
.venv/bin/python -m pytest runtime/ governance/ -v

# All Phase A property tests
.venv/bin/python -m pytest tests/ -v

# Full suite
.venv/bin/python -m pytest runtime/ governance/ tests/ -v
```

## Dependencies

- Python 3.13.7 (`.venv/bin/python`)
- PyYAML (YAML serialization)
- Hypothesis (property-based testing)

## Next Phase

Phase B (Chain Runtime) builds on these contracts to implement:
- Pipeline_Orchestrator (chain-aware execution)
- Chain_Validator (provenance verification)
- Report Engine rewrite (4 sub-components)
- Deterministic ordering enforcement
- First correct daily_report.md generation
