# Implementation Plan: Report Runtime Integrity

## Overview

This plan transforms the Portfolio OS report pipeline from a flat engine-runner model into a layered chain-compliant architecture enforcing the canonical authority flow: SIGNALS → SEMANTICS → REASONING → REPORT. Implementation follows CTO-mandated phasing: Foundation data contracts first, then Chain Runtime execution, then Semantic Expansion, then Compatibility Cleanup.

All code is Python 3.13.7, executed via `.venv/bin/python`. Tests use `.venv/bin/python -m pytest`. Property-based tests use Hypothesis (MANDATORY, not optional).

**Global Constraint (HARDENING 10 — NO FRAMEWORK ESCALATION):** No plugin architecture, event bus, generic runtime kernel, dynamic policy engine, distributed orchestration, async scheduler, dashboard layer, email delivery. Each phase ends at local deterministic `daily_report.md`.

## Tasks

- [x] 1. Phase A Preflight — Verify Foundation Prerequisites
  - [x] 1.1 Inspect existing governance and runtime modules
    - Verify `.domainization/src/report_value_detector.py` exists and assess reuse (EXTEND)
    - Verify `.domainization/src/runtime_flow_detector.py` exists and assess reuse (EXTEND)
    - Verify `.domainization/src/health_reporter.py` exists and assess reuse (EXTEND)
    - Verify `.domainization/src/validation_orchestrator.py` exists and assess reuse (EXTEND)
    - Confirm `runtime/` directory does NOT exist (CREATE)
    - Confirm `governance/` directory does NOT exist (CREATE)
    - Confirm `output/` directory does NOT exist (CREATE)
    - Confirm `state/` directory does NOT exist (CREATE)
    - Verify no duplicate schemas exist in `.domainization/` that conflict with planned `runtime/` schemas
    - Document registry location: `.domainization/artifact_registry.yaml`
    - _Requirements: 3.1, 3.2_

- [x] 2. Phase A — Foundation: Data Contracts
  - [x] 2.1 Implement Severity Taxonomy (`runtime/severity_taxonomy.py`)
    - **Infrastructure:** CREATE `runtime/severity_taxonomy.py` (no existing equivalent)
    - Create `Severity` IntEnum with 6 levels: INFO, WARNING, DEGRADED, CRITICAL, CANONICAL_BREAK, DETERMINISTIC_FAILURE
    - Define `SEVERITY_DEFINITIONS` dict with meaning, blocks_pipeline_hard_mode, triggers_audit_log, appears_in_data_availability for each level
    - Single canonical location — all other components import from here
    - **Registry update:** Add `runtime/severity_taxonomy.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 17.1, 17.3, 17.5_

  - [x] 2.2 Implement Runtime State Model (`runtime/runtime_state_model.py`)
    - **Infrastructure:** CREATE `runtime/runtime_state_model.py` (no existing equivalent)
    - Create `RuntimeState` StrEnum with 8 states: HEALTHY, DEGRADED, UNAVAILABLE, INVALID, INCONSISTENT, COLLAPSED, DETERMINISTIC_FAILURE, CANONICAL_BREAK
    - Create `IntegrityDimension` StrEnum with 5 orthogonal dimensions: DATA_AVAILABILITY, STRUCTURAL_VALIDITY, RUNTIME_CONSISTENCY, REPLAY_INTEGRITY, CHAIN_INTEGRITY
    - Define `STATE_DIMENSIONS` mapping states to their affected dimensions (multi-dimensional, NOT linear)
    - Implement `aggregate_pipeline_state()` function using worst-state-per-dimension logic
    - **Registry update:** Add `runtime/runtime_state_model.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 18.1, 18.2, 18.3, 18.5_

  - [x] 2.3 Write property test for Pipeline State Aggregation
    - **Property 20: Pipeline State Aggregation**
    - **Validates: Requirements 18.5**
    - Test that for any set of component runtime states, the aggregated pipeline state equals the highest-severity component state
    - Hypothesis generates random lists of RuntimeState values; verify aggregation is idempotent and monotonic

  - [x] 2.4 Implement TemporalValidity model and Reasoning_Object schema (`runtime/reasoning_object.py`)
    - **Infrastructure:** CREATE `runtime/reasoning_object.py` (no existing equivalent)
    - Create `TemporalValidity` dataclass with valid_from, valid_until, stale_after fields and `validity_state` property
    - Create `ActionImplication` dataclass with action and rationale fields
    - Create `Conclusion` dataclass with summary (1-1000 chars) and category fields
    - Create `ReasoningObject` dataclass with all schema fields: reasoning_id, source_semantic_states, conclusion, confidence_level, confidence_explanation, action_implications, temporal_validity, producing_engine, schema_version
    - Implement `validate()` method returning list of validation errors
    - **Registry update:** Add `runtime/reasoning_object.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 9.1, 9.2_

  - [x] 2.5 Write property test for Reasoning Object Schema Enforcement
    - **Property 11: Reasoning Object Schema Enforcement**
    - **Validates: Requirements 9.1, 9.4, 9.5**
    - Test that invalid objects (missing fields, out-of-range values) are correctly rejected by validate()
    - Hypothesis generates random ReasoningObject fields; verify validate() catches all constraint violations

  - [x] 2.6 Implement Schema Version Registry (`governance/schema_version_registry.py`)
    - **Infrastructure:** CREATE `governance/schema_version_registry.py` (no existing equivalent)
    - Define version constants for all 5 schemas: Semantic_State, Reasoning_Object, Run_Context, Deployment_Matrix, Provenance (all starting at "1.0.0")
    - Implement `validate_compatibility(producer_version, consumer_version)` checking same MAJOR version
    - Implement `log_version_mismatch()` for MINOR version differences
    - **Registry update:** Add `governance/schema_version_registry.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 23.1, 23.2, 23.3, 23.4_

  - [x] 2.7 Write property test for Schema Version Compatibility
    - **Property 21: Schema Version Compatibility**
    - **Validates: Requirements 23.2, 23.4**
    - Test that same MAJOR versions are compatible, different MAJOR versions are incompatible, MINOR differences produce warnings

  - [x] 2.8 Implement Run_Context (`runtime/run_context.py`)
    - **Infrastructure:** CREATE `runtime/run_context.py` (no existing equivalent)
    - Create `DataSourceReference` dataclass with file_path, content_hash (SHA-256), status
    - Create `RunContext` dataclass with run_id (UUID v4), timestamp (ISO 8601 UTC), data_sources, schema_version, pipeline_state, report_hash
    - Implement `create()` class method that snapshots input files and computes hashes
    - Implement `validate_source()` to verify file content hash matches recorded hash
    - Implement `persist()` to write as YAML to output directory
    - Implement `load()` class method to reload from persisted YAML
    - **Registry update:** Add `runtime/run_context.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 8.1, 8.2, 8.4, 8.6_

  - [x] 2.9 Write property test for Run_Context Temporal Consistency
    - **Property 14: Run_Context Temporal Consistency**
    - **Validates: Requirements 8.1, 8.3**
    - Test that hash mismatches between recorded and current content are detected and rejected
    - Hypothesis generates file content pairs; verify hash validation catches any mutation

  - [x] 2.10 Implement Provenance Schema (`governance/provenance_schema.py`)
    - **Infrastructure:** CREATE `governance/provenance_schema.py` (no existing equivalent)
    - Create `SectionProvenance` dataclass with section_name, reasoning_object_ids, semantic_state_ids, signal_engine_ids, completeness_state, unavailable_layers, schema_version
    - Implement `to_yaml()` and `to_json()` serialization methods
    - Create `ReportProvenance` dataclass with run_context_id, timestamp, sections, schema_version
    - Implement `persist()` to write canonical sidecar file (`<run_id>_provenance.yaml`)
    - Implement `embed_in_markdown()` for human-readable informational embedding
    - Canonical truth lives in sidecar file, markdown embedding is informational only
    - **Registry update:** Add `governance/provenance_schema.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 13.1, 13.3, 13.5_

  - [x] 2.11 Write property test for Provenance Parseability
    - **Property 10: Provenance Parseability**
    - **Validates: Requirements 13.3, 24.3**
    - Test that any provenance block serialized to YAML/JSON parses successfully with standard parser and contains completeness state

  - [x] 2.12 Implement Semantic_State_Store (`runtime/semantic_state_store.py`)
    - **Infrastructure:** CREATE `runtime/semantic_state_store.py` (EXTEND existing `engines/semantic_engine.py` concepts but new persistence layer)
    - Inspect existing `engines/semantic_engine.py` — confirm it only handles allocation signals, no persistence
    - Implement `__init__()` with state_dir parameter for snapshot and delta files
    - Implement `save_snapshot()` that archives previous snapshot immutably (never destructive overwrite), computes delta, updates latest pointer
    - Implement `load_snapshot()` returning current canonical states and run_id (within 5 seconds)
    - Implement `load_historical()` for forensic replay of specific run_id snapshots
    - Implement `get_delta()` returning additions, removals, changes for a specific run
    - Storage: `state/snapshots/<run_id>_semantic_snapshot.yaml` (immutable), `state/latest_snapshot.yaml` (pointer), `state/semantic_delta_log.yaml` (append-only)
    - **HARDENING 8 — SEMANTIC STATE PROTECTION:** Snapshot protected states before any modification; structural change to protected states fails the phase
    - **Registry update:** Add `runtime/semantic_state_store.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

  - [x] 2.13 Write property test for Semantic State Persistence Round-Trip
    - **Property 15: Semantic State Persistence Round-Trip**
    - **Validates: Requirements 12.1, 12.2**
    - Test that persisting and loading states returns structurally identical results
    - Hypothesis generates random semantic state lists; verify save→load round-trip preserves all fields

  - [x] 2.14 Write property test for Semantic Delta Correctness
    - **Property 16: Semantic Delta Correctness**
    - **Validates: Requirements 12.3, 12.5**
    - Test that deltas correctly identify additions, removals, and changes between consecutive snapshots
    - Hypothesis generates pairs of state lists; verify delta captures all differences

  - [x] 2.15 Implement PipelineResult contract (`runtime/pipeline_result.py`)
    - **Infrastructure:** CREATE `runtime/pipeline_result.py` (no existing equivalent)
    - Create `PipelineResult` dataclass with: run_id, runtime_state, generated_artifacts, degraded_categories, severity_events, report_path, provenance_path, run_context_path, deterministic_integrity_state, semantic_snapshot_path
    - All fields typed — no implicit dict-based orchestration outputs
    - **Registry update:** Add `runtime/pipeline_result.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 15.1 (typed contract for deterministic pipeline output)_

  - [x] 2.16 Implement Confidence Degradation Policy (`runtime/confidence_policy.py`)
    - **Infrastructure:** CREATE `runtime/confidence_policy.py` (no existing equivalent)
    - Create `ConfidenceDegradationPolicy` dataclass with base_ceiling=50, penalty_per_missing_category=10, minimum_floor=0, version="1.0.0"
    - Implement `compute(missing_category_count)` returning degraded confidence level
    - Implement `load()` class method to load from `governance/confidence_policy.yaml`
    - Policy is configurable without modifying schema or engine source code
    - **Registry update:** Add `runtime/confidence_policy.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 19.1, 19.2, 19.3, 19.4_

  - [x] 2.17 Write property test for Confidence Degradation Computation
    - **Property 12: Confidence Degradation Computation**
    - **Validates: Requirements 11.3, 19.3**
    - Test that for any N missing categories (0-14), confidence = max(floor, ceiling - penalty × N)
    - Hypothesis generates random N values; verify formula holds and result is within [0, 50]

  - [x] 2.18 Implement Canonical Boundary (`governance/canonical_boundary.py`)
    - **Infrastructure:** CREATE `governance/canonical_boundary.py` (no existing equivalent)
    - Define `CANONICAL_ARTIFACTS` set: semantic_state_snapshot, reasoning_object, daily_report, deployment_matrix, run_context, provenance_metadata
    - Define `TRANSIENT_ARTIFACTS` set: orchestration_buffer, in_memory_transform, pre_validation_staging, intermediate_draft_reasoning
    - Implement `classify()` returning "canonical" or "transient" (raises ValueError for unknown)
    - Implement `enforce_boundary()` that promotes transient to canonical if persisted or passed downstream
    - **Registry update:** Add `governance/canonical_boundary.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

  - [x] 2.19 Write property test for Canonical Boundary Enforcement
    - **Property 18: Canonical Boundary Enforcement**
    - **Validates: Requirements 16.4, 16.5**
    - Test that transient artifacts are promoted to canonical when persisted or passed downstream
    - Hypothesis generates random artifact names from both sets; verify classification is deterministic

- [x] 3. Phase A Output Contract Verification
  - Verify all Phase A outputs meet HARDENING 9 contract:
    - All schemas importable from `runtime/` and `governance/` without errors
    - All property tests pass (`.venv/bin/python -m pytest tests/ -v`)
    - Registry entries exist in `.domainization/artifact_registry.yaml` for every new file created in Phase A
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Phase B Preflight — Verify Chain Runtime Prerequisites
  - [x] 4.1 Inspect engine_runner behavior and identify Signal→Report shortcuts
    - Read `engines/engine_runner.py` — confirm `run_all_engines()` calls `run_report_engine(regime, decision, quality)` directly (Signal→Report shortcut)
    - Read `engines/report_engine.py` — confirm it takes raw engine outputs, formats text directly (no semantic layer)
    - Map all 8 forbidden briefing flows: allocation, attribution, correlation, cross_asset, divergence, early_warning, flow, liquidity
    - Map additional briefing producers: regime, market_breadth, narrative_dependency, relative_strength, scenario, portfolio_memory
    - Confirm `engines/semantic_engine.py` only handles allocation signals (3 states: defense_dependency_elevated, semiconductor_dependency_elevated, concentration_risk_elevated)
    - Document which engines produce which briefing files
    - _Requirements: 1.1, 1.5, 2.4_

- [x] 5. Phase B — Chain Runtime: Execute the Chain
  - [x] 5.1 Implement Pipeline_Orchestrator (`engines/pipeline_orchestrator.py`)
    - **Infrastructure:** CREATE `engines/pipeline_orchestrator.py`; WRAP existing `engines/engine_runner.py` (does NOT delete it, preserves current working outputs)
    - **HARDENING 6 — ENGINE_RUNNER COMPATIBILITY:** `pipeline_orchestrator.py` wraps existing engine execution, emits deprecation for direct briefing outputs
    - Inspect existing `engines/engine_runner.py` — confirm `run_all_engines()` signature and return dict structure
    - Create `PipelineOrchestrator` class with config loading from `.domainization/config.yaml`
    - Implement `execute()` method with full 10-step pipeline: create RunContext → Signal Engines → Semantic Engine → persist states → Reasoning Engines → Report Engine → persist provenance sidecar → Chain Validator → persist RunContext → return typed PipelineResult
    - Implement `detect_forbidden_flows()` checking Signal→Report shortcuts
    - Implement `handle_engine_failure()` marking affected categories as unavailable
    - Engine timeout: 60 seconds per engine
    - Returns typed `PipelineResult` (not dict)
    - **Registry update:** Add `engines/pipeline_orchestrator.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 8.1, 8.2, 11.1, 15.5, 15.6_

  - [x] 5.2 Write property test for Forbidden Flow Detection
    - **Property 2: Forbidden Flow Detection**
    - **Validates: Requirements 1.2, 1.3, 10.4**
    - Test that any Signal→Report shortcut is detected with source engine, target section, and skipped layers
    - Hypothesis generates random engine output routing; verify all shortcuts are caught

  - [x] 5.3 Write property test for Graceful Degradation Propagation
    - **Property 3: Graceful Degradation Propagation**
    - **Validates: Requirements 1.4, 2.6, 8.5, 11.1, 11.2**
    - Test that engine failures mark categories unavailable and remaining categories continue independently
    - Hypothesis generates random subsets of failing engines; verify non-failing categories still produce output

  - [x] 5.4 Write property test for Non-Determinism Injection
    - **Property 25: Non-Determinism Injection**
    - **Validates: Requirements 15.5, 15.6**
    - Test that non-deterministic values are replaced with Run_Context substitutes and report hash is recorded

  - [x] 5.5 Implement Chain_Validator (`runtime/chain_validator.py`)
    - **Infrastructure:** CREATE `runtime/chain_validator.py` (EXTEND concepts from `.domainization/src/runtime_flow_detector.py` but new runtime implementation)
    - Inspect existing `.domainization/src/runtime_flow_detector.py` — assess `detect_flow()` and `validate_flow_path()` for reuse patterns
    - Create `IdentifierGraph` dataclass with pre-normalized immutable maps: reasoning_to_semantics, semantics_to_signals, all_reasoning_ids (frozenset), all_semantic_ids (frozenset), all_signal_engine_ids (frozenset)
    - Create `ProvenanceBlock` dataclass with section_name, reasoning_object_ids, semantic_state_ids, signal_engine_ids, completeness_state, unavailability_reasons
    - Implement `build_graph()` — called once per run, builds immutable identifier graph with O(1) lookups
    - Implement `validate_section()` — verifies chain completeness using dict lookups only (no recursive traversal)
    - Implement `validate_all()` — validates all 9 sections within 2-second budget
    - Reads from provenance sidecar file, NOT from markdown parsing
    - **Registry update:** Add `runtime/chain_validator.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 20.1, 20.2, 20.3, 20.4, 20.5_

  - [x] 5.6 Write property test for Chain Provenance Integrity
    - **Property 1: Chain Provenance Integrity**
    - **Validates: Requirements 1.1, 10.1, 13.1, 13.4, 13.6**
    - Test that complete/partial sections have unbroken chain from SIGNALS through SEMANTICS through REASONING to REPORT
    - Hypothesis generates random provenance graphs; verify all complete sections have full chain

  - [x] 5.7 Implement Report Engine sub-components (`engines/report_engine.py`)
    - **Infrastructure:** DEPRECATE existing `engines/report_engine.py` `run_report_engine()` function; CREATE new `ReportEngine` class in same file
    - **HARDENING 7 — REPORT ENGINE BOUNDARY:** ReportEngine must NOT create semantics, NOT create reasoning, NOT infer missing conclusions. May ONLY render Reasoning_Object content and degradation notices.
    - Inspect existing `engines/report_engine.py` — confirm it directly formats raw data into text (the shortcut we eliminate)
    - Create `SectionCompletenessClassifier` — classifies sections into complete/partial/degraded/unavailable/invalid
    - Create `ProvenanceAssembler` — assembles provenance metadata from Reasoning Objects and Semantic States
    - Create `SectionRenderer` — renders markdown content based on completeness state
    - Create `DegradationRenderer` — renders degradation notices, confidence warnings, error notices
    - **Registry update:** Update `engines/report_engine.py` entry in `.domainization/artifact_registry.yaml`
    - _Requirements: 24.1, 24.2, 24.4_

  - [x] 5.8 Write property test for Section Completeness State Classification
    - **Property 13: Section Completeness State Classification**
    - **Validates: Requirements 24.1, 24.2**
    - Test that each section is classified into exactly one state and rendering behavior follows from that state

  - [x] 5.9 Implement Report Engine orchestrator (`engines/report_engine.py`)
    - **Infrastructure:** EXTEND `engines/report_engine.py` with new `ReportEngine` class (old `run_report_engine()` remains for backward compat, marked deprecated)
    - **HARDENING 7 — REPORT ENGINE BOUNDARY:** Enforced — render only, no inference
    - Create `ReportEngine` class composing the 4 sub-components
    - Define `CANONICAL_SECTIONS` list with 9 sections in fixed order
    - Implement `render()` method accepting reasoning_objects, deployment_matrix, portfolio_state, watchlist, run_context — must complete within 30 seconds
    - Implement `render_section()` orchestrating classification → rendering → provenance assembly per section
    - Rendering rules: complete→full content, partial→content+notice, degraded→content+warning, unavailable→notice only, invalid→error+remediation
    - _Requirements: 6.1, 6.2, 6.4, 6.6, 6.7, 13.1, 13.2_

  - [x] 5.10 Write property test for Report Structure Invariant
    - **Property 8: Report Structure Invariant**
    - **Validates: Requirements 6.1, 6.4**
    - Test that all 9 sections appear in fixed order with either content or degradation notice
    - Hypothesis generates random sets of available/unavailable Reasoning Objects; verify section order is always preserved

  - [x] 5.11 Write property test for Reasoning Object to Report Section Mapping
    - **Property 5: Reasoning Object to Report Section Mapping**
    - **Validates: Requirements 2.3, 13.2**
    - Test that each Reasoning Object's category maps to the correct Report Section with provenance reference

  - [x] 5.12 Implement degradation propagation through the chain
    - **Infrastructure:** EXTEND `engines/pipeline_orchestrator.py` and `engines/report_engine.py`
    - Wire unavailability markers from Pipeline_Orchestrator through Semantic_Engine to Reasoning_Engines to Report_Engine
    - Implement confidence capping using active ConfidenceDegradationPolicy
    - Render degradation notices for sections with confidence < 50
    - Include "Data Availability" summary in daily_report.md listing all 14 categories with status
    - Handle all-engines-fail scenario (only Data Availability summary rendered)
    - _Requirements: 11.2, 11.3, 11.4, 11.5, 11.6_

  - [x] 5.13 Write property test for Data Availability Summary Completeness
    - **Property 24: Data Availability Summary Completeness**
    - **Validates: Requirements 11.5**
    - Test that every pipeline execution includes Data Availability summary with all 14 categories having exactly one status

  - [x] 5.14 Implement deterministic ordering enforcement
    - **Infrastructure:** EXTEND `runtime/run_context.py`, `governance/provenance_schema.py`, `runtime/semantic_state_store.py`
    - Ensure all YAML serializations (Run_Context, provenance sidecar, Reasoning Objects, Semantic State snapshots) are byte-identical for same inputs
    - Inject deterministic substitutes for timestamps, random seeds, unordered collections from Run_Context
    - Compute SHA-256 hash of daily_report.md and record in Run_Context metadata
    - Markdown uses canonical normalization (consistent section ordering, deterministic content) — not byte-identical for insignificant whitespace
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 22.1, 22.2, 22.3_

  - [x] 5.15 Write property test for Pipeline Determinism
    - **Property 9: Pipeline Determinism**
    - **Validates: Requirements 6.5, 15.1, 15.2, 15.3, 15.4, 22.1, 22.2**
    - Test that identical Run_Context inputs produce semantically equivalent outputs; byte-identity for governed YAML serializations
    - Hypothesis generates random valid inputs; verify two executions produce identical YAML outputs

  - [x] 5.16 Generate first daily_report.md (HARDENING 5 — DAILY REPORT GATED)
    - **Infrastructure:** EXTEND `engines/pipeline_orchestrator.py`
    - **HARDENING 5 — DAILY REPORT GATED:** Generation requires ALL of the following gates to pass:
      - Run_Context works (creates, persists, validates sources)
      - Reasoning_Object validation works (schema enforcement passes)
      - Provenance sidecar exists (canonical provenance file written)
      - Chain_Validator passes (no broken chains in any section)
      - ReportEngine renders all 9 sections (content or degradation notice)
      - Data Availability summary exists (all 14 categories listed)
      - Determinism test passes (same inputs → same YAML outputs)
    - Wire full pipeline end-to-end: raw data → Signal Engines → Semantic Engine → Reasoning Engines → Report Engine → daily_report.md
    - Output to configurable local file path (default: `output/daily_report.md`)
    - Include all 9 canonical sections with provenance blocks
    - Persist provenance sidecar file alongside report
    - _Requirements: 6.1, 6.2, 6.3, 13.1_

  - [x] 5.17 Write property test for Governance Event Completeness
    - **Property 19: Governance Event Completeness**
    - **Validates: Requirements 17.2, 17.4, 18.2, 18.4**
    - Test that every governance event includes severity, description, component identifier, and timestamp

- [x] 6. Phase B Output Contract Verification
  - Verify all Phase B outputs meet HARDENING 9 contract:
    - Chain-compliant daily report prototype exists at `output/daily_report.md`
    - Provenance sidecar file exists at `output/<run_id>_provenance.yaml`
    - Chain validation result shows zero broken chains (or documented degradation)
    - No Signal→Report shortcuts in canonical report (forbidden flow detection returns empty list)
    - All property tests pass (`.venv/bin/python -m pytest tests/ -v`)
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Phase C Preflight — Verify Semantic Expansion Prerequisites
  - [x] 7.1 Inspect semantic signal registry and existing states
    - Verify `engines/semantic_engine.py` current state coverage (only 3 states: defense_dependency_elevated, semiconductor_dependency_elevated, concentration_risk_elevated)
    - Verify Semantic_State_Store structure is operational from Phase B
    - **HARDENING 8 — SEMANTIC STATE PROTECTION:** Snapshot the 5 protected states before any modification:
      - ai_dependency_high
      - deployment_fully_extended
      - concentration_risk_elevated
      - portfolio_health_fragile
      - defense_dependency_elevated
    - Confirm no mutation to protected state signal structures will occur
    - Verify no accidental structural change to protected states (compare before/after)
    - _Requirements: 7.4_

- [x] 8. Phase C — Semantic Expansion
  - [x] 8.1 Implement new semantic states
    - **Infrastructure:** EXTEND `engines/semantic_engine.py` (add new states alongside existing 3)
    - Inspect existing `engines/semantic_engine.py` — confirm `interpret_allocation_signals()` structure
    - Add `semiconductor_dependency_high` (category: narrative_dependency) to Semantic Signal Registry
    - Add `energy_grid_dependency` (category: narrative_dependency) to Semantic Signal Registry
    - Add `datacenter_infrastructure_exposure` (category: narrative_dependency) to Semantic Signal Registry
    - Each state has complete signal structure: signal_id, category, meaning, signal_origin, reasoning_impact, confidence_behavior
    - **HARDENING 8 — SEMANTIC STATE PROTECTION:** Existing states (ai_dependency_high, deployment_fully_extended, concentration_risk_elevated, portfolio_health_fragile, defense_dependency_elevated) remain UNCHANGED — verify with snapshot comparison
    - **Registry update:** Update `engines/semantic_engine.py` entry in `.domainization/artifact_registry.yaml`
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 8.2 Write property test for Semantic Coverage Invariant
    - **Property 4: Semantic Coverage Invariant**
    - **Validates: Requirements 2.1, 2.2**
    - Test that for valid signal outputs covering all 14 categories, at least one Semantic State per category and exactly one Reasoning Object per category are produced
    - Hypothesis generates random valid signal outputs for all 14 categories; verify coverage completeness

  - [x] 8.3 Implement Deployment Matrix (`runtime/deployment_matrix.py`)
    - **Infrastructure:** CREATE `runtime/deployment_matrix.py` (no existing equivalent)
    - Create `PositionAssignment` dataclass with position_id, basket, rationale, semantic_state_refs, confidence_level, temporal_validity
    - Create `DeploymentMatrix` dataclass with positions, run_context_id, schema_version
    - Implement `get_basket()` returning positions for a given basket name
    - Implement `validate()` ensuring each position is in exactly one basket
    - Baskets: momentum_core, diversification_candidates, risk_thresholds, unclassified
    - **Registry update:** Add `runtime/deployment_matrix.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

  - [x] 8.4 Write property test for Deployment Matrix Partition Invariant
    - **Property 17: Deployment Matrix Partition Invariant**
    - **Validates: Requirements 14.2, 14.3**
    - Test that each position is assigned to exactly one basket with confidence_level, semantic_state_refs, and valid temporal_validity
    - Hypothesis generates random position lists; verify partition is exhaustive and exclusive

  - [x] 8.5 Implement Portfolio State / Watchlist separation in report output
    - **Infrastructure:** EXTEND `engines/report_engine.py` ReportEngine class
    - Add "Current Portfolio Reality" block to daily_report.md (appears before Watchlist block)
    - Add "Watchlist and Deployment Candidates" block to daily_report.md
    - Source portfolio block exclusively from Portfolio_State data through Canonical Chain
    - Source watchlist block exclusively from Watchlist data through Canonical Chain
    - Handle position transitions with transition notice (position_id, previous classification, new classification)
    - Handle duplicate positions: classify per Portfolio_State, omit from Watchlist, log data conflict warning
    - Handle empty states: render explicit empty-state notice
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 8.6 Write property test for Portfolio/Watchlist Separation
    - **Property 7: Portfolio/Watchlist Separation**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.6**
    - Test that portfolio block appears before watchlist, positions are exclusive to their block, duplicates resolve to Portfolio_State
    - Hypothesis generates random position sets with overlaps; verify separation invariant holds

  - [x] 8.7 Write property test for Position Transition Rendering
    - **Property 23: Position Transition Rendering**
    - **Validates: Requirements 5.5**
    - Test that transitions include notice with position_id, previous classification, and new classification

  - [x] 8.8 Integrate confidence governance with configurable policy
    - **Infrastructure:** EXTEND `engines/pipeline_orchestrator.py` and Reasoning Engines
    - Wire `ConfidenceDegradationPolicy.load()` into Reasoning Engines
    - Log policy changes with previous version, new version, effective timestamp
    - Ensure policy updates do not require schema or engine source code changes
    - _Requirements: 19.4, 19.5_

- [x] 9. Phase C Output Contract Verification
  - Verify all Phase C outputs meet HARDENING 9 contract:
    - New semantic states active (semiconductor_dependency_high, energy_grid_dependency, datacenter_infrastructure_exposure emitted when conditions met)
    - Deployment matrix generated with valid partition (all positions in exactly one basket)
    - Portfolio/Watchlist separation visible in daily_report.md (two distinct blocks, correct ordering)
    - **HARDENING 8 verification:** Protected states unchanged — compare current signal structures against Phase C preflight snapshot
    - All property tests pass (`.venv/bin/python -m pytest tests/ -v`)
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Phase D Preflight — Verify Compatibility Cleanup Prerequisites
  - [x] 10.1 Inspect briefing file compatibility and downstream consumers
    - Verify all 14 briefing `.txt` files still exist on disk (coexistence during transition)
    - Identify any downstream consumers of briefing files (scripts, imports, references)
    - Verify artifact registry coverage — count registered vs unregistered artifacts
    - Confirm `.domainization/artifact_registry.yaml` structure supports deprecation fields
    - _Requirements: 2.5, 3.1, 25.1_

- [x] 11. Phase D — Compatibility Cleanup
  - [x] 11.1 Extend REPORT_OUT lifecycle model with deprecation and sunset states (HARDENING 11)
    - **Infrastructure:** EXTEND `.domainization/lifecycle_state_machine.yaml` REPORT_OUT section
    - **HARDENING 11 — LIFECYCLE MODEL EXTENSION:** REPORT_OUT currently only supports `generated → current → archived`. This is insufficient for governance-aware deprecation.
    - Extend REPORT_OUT states to: `generated`, `current`, `deprecated`, `sunset_pending`, `archived`, `superseded`
    - Add transitions: `current → deprecated` (condition: "Replaced by chain-compliant output"), `deprecated → sunset_pending` (condition: "Sunset target date reached, evaluating dependencies"), `sunset_pending → archived` (condition: "Zero downstream dependencies confirmed"), `current → superseded` (condition: "Replaced by structurally different artifact type")
    - Add `deprecated` and `sunset_pending` to `modifiable_states` (metadata updates allowed during sunset evaluation)
    - Add `archived` and `superseded` to `read_only_states`
    - Verify no existing REPORT_OUT artifacts break under new state machine (all currently `current` — valid in new model)
    - _Requirements: 2.5, 25.1_

  - [x] 11.2 Implement sunset governance fields and policy (`governance/sunset_governance.py`) (HARDENING 12)
    - **Infrastructure:** CREATE `governance/sunset_governance.py`; EXTEND `.domainization/artifact_registry.yaml` schema
    - **HARDENING 12 — SUNSET GOVERNANCE:** Mandatory deprecation governance fields prevent artifact zombie sprawl.
    - Add optional deprecation governance fields to artifact registry schema: `deprecated_date` (ISO 8601), `sunset_date` (ISO 8601), `replacement_artifact` (artifact_id reference), `deprecation_reason` (string, max 200 chars), `compatibility_impact` (enum: none, minor, breaking)
    - Implement `SunsetGovernance` class in `governance/sunset_governance.py` with 4-phase sunset model:
      - Phase 1 (WARNING_ONLY): `deprecated_date` set, artifact still generated, deprecation warning emitted
      - Phase 2 (REPLACEMENT_PATH): warning + replacement_artifact reference provided to consumers
      - Phase 3 (RUNTIME_DISABLED): artifact generation stops IF `downstream_dependency_count == 0`; continues + CRITICAL warning if dependencies remain (sunset-blocked)
      - Phase 4 (ARCHIVED): lifecycle_status transitions to `archived`, artifact frozen
    - Implement `evaluate_sunset_phase(artifact_id)` returning current phase based on dates and dependency count
    - Implement `get_sunset_report()` returning all artifacts in deprecation pipeline with phase, age, remaining days
    - Annotate each of the 15 legacy Briefing_Files with: `deprecated_date`, `sunset_date`, `replacement_artifact`, `deprecation_reason`, `compatibility_impact`
    - **HARDENING 6 — ENGINE_RUNNER COMPATIBILITY:** `engine_runner.py` remains functional, emits deprecation warnings for direct briefing outputs
    - **Registry update:** Add `governance/sunset_governance.py` to `.domainization/artifact_registry.yaml`
    - _Requirements: 2.5, 25.1, 25.2, 25.3, 25.4_

  - [x] 11.3 Write property test for Sunset Governance Behavior
    - **Property 22: Sunset Governance Behavior**
    - **Validates: Requirements 25.3, 25.4**
    - Test that Phase 1→2→3→4 transitions follow date and dependency rules
    - Test that files at sunset with zero deps transition to RUNTIME_DISABLED; files at sunset with deps remain in sunset-blocked state + CRITICAL warning
    - Test that phase evaluation is deterministic given same dates and dependency counts
    - Hypothesis generates random sunset dates, dependency counts, and current dates; verify phase assignment matches policy

  - [x] 11.4 Evaluate REPORT_OUT type splitting (HARDENING 13 — evaluation only)
    - **Infrastructure:** CREATE `reports/report_out_type_evaluation.md` (evaluation document, NOT implementation)
    - **HARDENING 13 — REPORT_OUT SEMANTIC BREADTH:** REPORT_OUT currently covers 15 briefing files, daily_report.md, and health reports — semantically too broad.
    - Evaluate whether REPORT_OUT should split into sub-types:
      - `REPORT_RUNTIME_OUTPUT` — chain-compliant daily_report.md and provenance sidecars
      - `GOVERNANCE_BRIEFING` — legacy briefing .txt files (deprecated path)
      - `HISTORICAL_REPORT` — archived reports and snapshots
      - `SNAPSHOT_OUTPUT` — semantic state snapshots and delta logs
      - `TRANSIENT_RUNTIME_OUTPUT` — intermediate pipeline artifacts
    - Document: current artifact count per proposed sub-type, migration impact, registry schema changes needed, backward compatibility risks
    - Produce recommendation: split now, split later, or keep unified with tags
    - **NOTE:** This is an EVALUATION task. Do NOT implement the split. Document findings only.
    - _Requirements: 16.1, 16.2_

  - [x] 11.5 Register unregistered artifacts and implement registration enforcement (HARDENING 14)
    - **Infrastructure:** EXTEND `.domainization/artifact_registry.yaml`; EXTEND existing `.domainization/src/validation_orchestrator.py`
    - **HARDENING 14 — UNREGISTERED ARTIFACT GOVERNANCE:** 40+ unregistered files is a governance trigger. Growth must stop.
    - Inspect existing `.domainization/artifact_registry.yaml` — identify the 13 unregistered artifacts from baseline health report
    - Add all 13 currently unregistered artifacts with all required schema fields: artifact_id, file_path, primary_domain, artifact_type, lifecycle_status, created_date, last_modified, owner_role, ssot_relationship, allowed_writers, allowed_readers, metadata_source, registry_mode, dependencies, report_value
    - Register any new artifacts created during this feature implementation that are not yet registered
    - Implement artifact registration enforcement policy in `.domainization/src/validation_orchestrator.py`:
      - All new `runtime/` and `governance/` artifacts REQUIRE registration before merge
      - Test files (`tests/`) use simplified registration class (artifact_id, file_path, primary_domain, artifact_type only)
      - Transient artifacts explicitly marked with `registry_mode: transient_exempt`
      - Emit CI-compatible warning if unregistered artifact count increases from baseline
    - **HARDENING 1 — EXISTING INFRASTRUCTURE CHECK:** EXTEND existing `.domainization/src/validation_orchestrator.py` for registration validation (do not create duplicate validator)
    - **Registry update:** Self-referential — registry entries added to `.domainization/artifact_registry.yaml`
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 11.6 Add report_value metadata to all artifacts (100% coverage)
    - **Infrastructure:** EXTEND `.domainization/artifact_registry.yaml`; EXTEND existing `.domainization/src/report_value_detector.py`
    - Inspect existing `.domainization/src/report_value_detector.py` — confirm `assess_artifact()`, `detect_missing_report_value()`, `_is_speculative_claim()` methods exist and can be reused
    - Add report_value field (category + justification) to every registered artifact
    - Wire existing Report_Value_Detector to validate category against 10 accepted categories
    - Flag invalid categories, speculative language ("might improve", "could help", "potentially", "in the future", "indirectly"), and missing/empty fields
    - Achieve 100% report_value field population
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [x] 11.7 Write property test for Report Value Validation
    - **Property 6: Report Value Validation**
    - **Validates: Requirements 4.2, 4.4**
    - Test that invalid categories are flagged and speculative language patterns are detected
    - Hypothesis generates random category strings and justification text; verify detection accuracy

  - [x] 11.8 Observability polish (health report integration)
    - **Infrastructure:** EXTEND existing `.domainization/src/health_reporter.py` (do not create new health reporter)
    - Inspect existing `.domainization/src/health_reporter.py` — confirm `generate_health_report()`, `get_report_value_health_score()`, `get_runtime_flow_analysis()` methods
    - Integrate governance events into existing health report
    - Integrate sunset governance report into health report (deprecated artifacts, sunset phases, blocked sunsets)
    - Ensure all validators emit structured events with severity, description, component, timestamp
    - Wire state transitions to include previous state, new state, reason, timestamp
    - Verify zero forbidden flows, zero unregistered artifacts, 100% report_value coverage in health report
    - _Requirements: 1.5, 3.4, 4.6, 17.4, 18.4_

- [x] 12. Phase D Output Contract Verification (Final)
  - Verify all Phase D outputs meet HARDENING 9 contract:
    - REPORT_OUT lifecycle model extended: `generated → current → deprecated → sunset_pending → archived` + `superseded` (HARDENING 11)
    - Sunset governance operational: all 15 briefings annotated with `deprecated_date`, `sunset_date`, `replacement_artifact`, `deprecation_reason`, `compatibility_impact` (HARDENING 12)
    - Sunset phases functional: Phase 1→2→3→4 transitions verified by property test (HARDENING 12)
    - REPORT_OUT type evaluation document produced with recommendation (HARDENING 13)
    - Registration enforcement policy active: new runtime/governance artifacts require registration, CI warning on count increase (HARDENING 14)
    - Registry complete: zero unregistered-artifact warnings in health report
    - report_value tracked: 100% field population, zero speculative justifications
    - Observability updated: health report shows zero forbidden flows, full coverage, sunset status
    - **HARDENING 6 verification:** `engine_runner.py` still functional (backward compat preserved)
    - All property tests pass (`.venv/bin/python -m pytest tests/ -v`)
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- **HARDENING 2 — PROPERTY TESTS ARE MANDATORY:** Property tests are required before phase completion. They validate canonical runtime guarantees. They are NOT optional.
- **HARDENING 3 — REGISTRY UPDATED CONTINUOUSLY:** Every task creating a canonical artifact includes a registry update substep. Do NOT batch registry updates to Phase D.
- **HARDENING 10 — NO FRAMEWORK ESCALATION:** No plugin architecture, event bus, generic runtime kernel, dynamic policy engine, distributed orchestration, async scheduler, dashboard layer, email delivery. Phase ends at local deterministic `daily_report.md`.
- **HARDENING 11 — LIFECYCLE MODEL EXTENSION:** REPORT_OUT lifecycle must support full deprecation flow: `generated → current → deprecated → sunset_pending → archived` + `superseded`. `deprecated ≠ archived`.
- **HARDENING 12 — SUNSET GOVERNANCE:** Mandatory 4-phase sunset model (WARNING_ONLY → REPLACEMENT_PATH → RUNTIME_DISABLED → ARCHIVED). Prevents artifact zombie sprawl. Requires `deprecated_date`, `sunset_date`, `replacement_artifact`, `deprecation_reason`, `compatibility_impact` fields.
- **HARDENING 13 — REPORT_OUT SEMANTIC BREADTH:** REPORT_OUT is semantically too broad for 15+ heterogeneous artifacts. Evaluate sub-type splitting (evaluation only, not implementation in this phase).
- **HARDENING 14 — UNREGISTERED ARTIFACT GOVERNANCE:** 40+ unregistered files triggers enforcement policy. All new runtime/governance artifacts require registration. CI warning on count increase. Tests use simplified registration. Transient artifacts explicitly marked.
- **HARDENING 15 — DEPRECATED ≠ IGNORED:** Deprecated artifacts MUST NOT emit warnings forever. They progress through sunset phases with clear terminal state. Pipeline behavior changes at each phase boundary.
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation between phases with explicit output contracts (HARDENING 9)
- Phase preflights (HARDENING 4) verify prerequisites before each phase begins
- Every task states infrastructure disposition: CREATE, EXTEND, WRAP, or DEPRECATE (HARDENING 1)
- Python 3.13.7 via `.venv/bin/python` — tests via `.venv/bin/python -m pytest`
- Property-based tests use Hypothesis library with minimum 100 iterations per property
- All YAML serializations must be deterministic (sorted keys, consistent formatting)
- Provenance canonical truth lives in sidecar file — markdown embedding is informational only
- Runtime states are multi-dimensional (IntegrityDimension), NOT a linear severity ladder
- Semantic snapshots are immutable archives — never destructively overwritten
- Protected semantic states (HARDENING 8) must be snapshotted before modification; structural changes fail the phase
- Daily report generation is gated (HARDENING 5) — all 7 prerequisites must pass before `daily_report.md` is written
- `engine_runner.py` is preserved for backward compatibility (HARDENING 6) — never deleted

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1", "2.2"] },
    { "id": 2, "tasks": ["2.3", "2.4", "2.6"] },
    { "id": 3, "tasks": ["2.5", "2.7", "2.8", "2.15", "2.18"] },
    { "id": 4, "tasks": ["2.9", "2.10", "2.16", "2.19"] },
    { "id": 5, "tasks": ["2.11", "2.12", "2.17"] },
    { "id": 6, "tasks": ["2.13", "2.14"] },
    { "id": 7, "tasks": ["4.1"] },
    { "id": 8, "tasks": ["5.1", "5.5"] },
    { "id": 9, "tasks": ["5.2", "5.3", "5.4", "5.6", "5.7"] },
    { "id": 10, "tasks": ["5.8", "5.9"] },
    { "id": 11, "tasks": ["5.10", "5.11", "5.12"] },
    { "id": 12, "tasks": ["5.13", "5.14"] },
    { "id": 13, "tasks": ["5.15", "5.16"] },
    { "id": 14, "tasks": ["5.17"] },
    { "id": 15, "tasks": ["7.1"] },
    { "id": 16, "tasks": ["8.1", "8.3"] },
    { "id": 17, "tasks": ["8.2", "8.4", "8.5"] },
    { "id": 18, "tasks": ["8.6", "8.7", "8.8"] },
    { "id": 19, "tasks": ["10.1"] },
    { "id": 20, "tasks": ["11.1"] },
    { "id": 21, "tasks": ["11.2", "11.4", "11.5"] },
    { "id": 22, "tasks": ["11.3", "11.6"] },
    { "id": 23, "tasks": ["11.7", "11.8"] }
  ]
}
```
