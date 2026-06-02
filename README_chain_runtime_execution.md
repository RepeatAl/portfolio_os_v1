# Phase B — Chain Runtime: Execute the Chain

## Overview

Phase B transforms the Phase A data contracts into a running pipeline that enforces the canonical authority flow: SIGNALS → SEMANTICS → REASONING → REPORT. It replaces the flat engine-runner model with chain-aware orchestration, runtime provenance verification, and graceful degradation.

## Completed Tasks (3–6)

| Task | Description | Status |
|------|-------------|--------|
| 3 | Phase A Output Contract Verification | ✓ CI green |
| 4.1 | Inspect engine_runner behavior, identify 16 Signal→Report shortcuts | ✓ Documented |
| 5.1 | Pipeline_Orchestrator (10-step chain-aware execution) | ✓ Implemented |
| 5.2 | Property test: Forbidden Flow Detection (5 properties) | ✓ Passing |
| 5.3 | Property test: Graceful Degradation Propagation (5 properties) | ✓ Passing |
| 5.4 | Property test: Non-Determinism Injection (6 properties) | ✓ Passing |
| 5.5 | Chain_Validator (pre-normalized graph, O(1) lookups) | ✓ Implemented |
| 5.6 | Property test: Chain Provenance Integrity (5 properties) | ✓ Passing |
| 5.7 | Report Engine sub-components (4 composable modules) | ✓ Implemented |
| 5.8 | Property test: Section Completeness Classification (5 properties) | ✓ Passing |
| 5.9 | Report Engine orchestrator with render() method | ✓ Implemented |
| 5.10 | Property test: Report Structure Invariant (3 properties) | ✓ Passing |
| 5.11 | Property test: Reasoning Object → Section Mapping (3 properties) | ✓ Passing |
| 5.12 | Degradation propagation with ConfidenceDegradationPolicy | ✓ Implemented |
| 5.13 | Property test: Data Availability Summary Completeness (3 properties) | ✓ Passing |
| 5.14 | Deterministic ordering enforcement (sort_keys, sorted lists) | ✓ Implemented |
| 5.15 | Property test: Pipeline Determinism (4 properties) | ✓ Passing |
| 5.16 | First daily_report.md (HARDENING 5 — 7 gates verified) | ✓ Generated |
| 5.17 | Property test: Governance Event Completeness (5 properties) | ✓ Passing |
| 6 | Phase B Output Contract Verification | ✓ All tests pass |

## Architecture

```
engines/
├── pipeline_orchestrator.py    # 10-step chain-aware orchestration (wraps engine_runner.py)
├── report_engine.py            # 4 sub-components + ReportEngine orchestrator + deprecated legacy
├── test_pipeline_orchestrator.py
├── test_report_engine.py
├── test_degradation_propagation.py
└── test_hardening_5_daily_report.py

runtime/
└── chain_validator.py          # Pre-normalized graph-based provenance verification

tests/
├── test_property_forbidden_flow_detection.py
├── test_property_graceful_degradation.py
├── test_property_non_determinism_injection.py
├── test_property_chain_provenance_integrity.py
├── test_property_section_completeness.py
├── test_property_report_structure_invariant.py
├── test_property_reasoning_object_section_mapping.py
├── test_property_data_availability_summary.py
├── test_property_pipeline_determinism.py
├── test_property_governance_event_completeness.py
└── test_deterministic_ordering_enforcement.py
```

## Key Components

### Pipeline_Orchestrator (`engines/pipeline_orchestrator.py`)

10-step execution flow:
1. Create RunContext → 2. Signal Engines → 3. Semantic Engine → 4. Persist states → 5. Reasoning Engines → 6. Report Engine → 7. Provenance sidecar → 8. Chain Validator → 9. Persist RunContext → 10. Return PipelineResult

Features:
- Wraps existing `engine_runner.py` (backward compatible)
- 60-second engine timeout with threading
- Forbidden flow detection (13 uncovered categories + report shortcut)
- Graceful degradation: engine failures mark categories unavailable
- Confidence capping via `ConfidenceDegradationPolicy`
- All-engines-fail scenario: only Data Availability summary rendered

### Chain_Validator (`runtime/chain_validator.py`)

- Pre-normalized `IdentifierGraph` built once per run (Hardening 4)
- O(1) dict lookups for validation (no recursive traversal)
- Validates all 9 sections within 2-second budget
- Reads from provenance sidecar file (not markdown)
- Observability mode: warnings only, never blocks

### Report Engine (`engines/report_engine.py`)

Decomposed into 4 sub-components (Hardening 2):
- `SectionCompletenessClassifier` → complete/partial/degraded/unavailable/invalid
- `ProvenanceAssembler` → builds provenance metadata per section
- `SectionRenderer` → renders markdown based on completeness state
- `DegradationRenderer` → renders notices, warnings, errors

HARDENING 7 enforced: render only, no inference, no synthesis.

### Deterministic Ordering

- All `yaml.safe_dump()` calls use `sort_keys=True`
- Identifier lists sorted before serialization
- SHA-256 report hash computed and recorded in RunContext
- Byte-identical YAML for same inputs (verified by property tests)

## HARDENING 5 Gates (Daily Report Generation)

All 7 gates must pass:
1. ✓ Run_Context works (creates, persists, validates)
2. ✓ Reasoning_Object validation works
3. ✓ Provenance sidecar exists
4. ✓ Chain_Validator passes
5. ✓ ReportEngine renders all 9 sections
6. ✓ Data Availability summary complete (14 categories)
7. ✓ Determinism passes

## Running Tests

```bash
# Phase B unit tests
.venv/bin/python -m pytest engines/ runtime/test_chain_validator.py -v

# Phase B property tests
.venv/bin/python -m pytest tests/test_property_forbidden_flow_detection.py tests/test_property_graceful_degradation.py tests/test_property_non_determinism_injection.py tests/test_property_chain_provenance_integrity.py tests/test_property_section_completeness.py tests/test_property_report_structure_invariant.py tests/test_property_reasoning_object_section_mapping.py tests/test_property_data_availability_summary.py tests/test_property_pipeline_determinism.py tests/test_property_governance_event_completeness.py -v

# Full suite (Phase A + B)
.venv/bin/python -m pytest runtime/ governance/ engines/ tests/ -v
```

## Preflight Findings (Task 4.1)

- 16 total forbidden Signal→Report flows identified
- `engine_runner.py` calls `run_report_engine()` directly (no semantic layer)
- Semantic engine only covers allocation (3 states)
- 14 briefing files bypass the canonical chain entirely
- Report engine is a pure string formatter (no schema validation)
