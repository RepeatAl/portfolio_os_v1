# Requirements Document

## Introduction

This feature closes the gap between the Domainization governance rules and the actual runtime behavior of the Portfolio OS report pipeline. The Implementation Report (2026-05-26) identified 16 forbidden runtime flows, 13 unregistered artifacts, and 0% report value metadata coverage. Briefing files currently bypass the canonical reasoning chain (SIGNALS → SEMANTICS → REASONING → REPORT) by flowing directly from Signal Engines to Report outputs. This feature eliminates those shortcuts, registers all artifacts, adds report value justification metadata, separates Portfolio State from Watchlist, produces the first correct daily report through the full chain, and expands semantic coverage for real portfolio themes.

**Critical Execution Constraint:** This phase remains FAST LANE REPORT MVP. Implementation SHALL produce the minimum concrete runtime structures required to satisfy canonical chain integrity, deterministic report generation, provenance validation, graceful degradation, and semantic consistency. Implementation SHALL NOT convert the governance model into a generalized framework platform, plugin system, generic orchestration kernel, enterprise governance engine, or premature scalability infrastructure. Governance exists to protect report truth, not to become the product itself.

## Glossary

- **Canonical_Chain**: The authority flow SIGNALS (Level 1) → SEMANTICS (Level 2) → REASONING (Level 3) → REPORT (Level 4). No domain may skip levels.
- **Semantic_State**: A language-independent, deterministic, explainable signal representing canonical system truth. Defined in the Semantic Signal Registry.
- **Reasoning_Object**: A structured conclusion produced by a Reasoning Engine from one or more Semantic States. Contains portfolio-level interpretation, confidence, and action implications.
- **Report_Section**: A human-readable output rendered from Reasoning Objects according to the Report Section Specification.
- **Signal_Engine**: An engine in the SIGNALS domain that produces structured quantitative outputs from raw data.
- **Semantic_Engine**: An engine in the SEMANTICS domain that interprets Signal Engine outputs into Semantic States.
- **Reasoning_Engine**: An engine in the REASONING domain that produces Reasoning Objects from Semantic States.
- **Report_Engine**: An engine in the REPORT domain that renders Reasoning Objects into human-readable Report Sections.
- **Briefing_File**: A text file (e.g., allocation_briefing.txt) currently produced directly by Signal Engines, bypassing the Canonical Chain.
- **Run_Context**: A temporal snapshot identifier ensuring all engines in a single pipeline execution operate on the same data.
- **Report_Value_Metadata**: A metadata field on every artifact answering "How does this artifact improve the daily email report?"
- **Portfolio_State**: The canonical reality of current holdings, dominant drivers, and risk structure.
- **Watchlist**: Potential future exposures and deployment candidates not yet in the portfolio.
- **Chain_Provenance**: Metadata on each Report Section tracing which Semantic States and Reasoning Objects produced it.
- **Artifact_Registry**: The central index of all registered artifacts in `.domainization/artifact_registry.yaml`.
- **Observability_Mode**: The current enforcement mode where violations generate warnings only, never block commits.
- **Daily_Report**: The canonical daily output file (`daily_report.md`) produced through the full Canonical Chain.
- **Deployment_Matrix**: The three-basket capital allocation model (Momentum Core, Diversification Candidates, Risk Thresholds).
- **Canonical_Artifact**: A persisted or emitted artifact that represents system truth (Semantic States, Reasoning Objects, Daily Report, Deployment Matrix, Run Context snapshots). Subject to full governance enforcement.
- **Transient_Artifact**: An internal, non-persisted processing structure (orchestration buffers, in-memory transforms, staging data) that never crosses runtime boundaries and is exempt from canonical governance.
- **Severity_Level**: A classification from the canonical severity taxonomy (info, warning, degraded, critical, canonical_break, deterministic_failure) used consistently across all validators and components.
- **Runtime_State**: A shared state identifier (healthy, degraded, unavailable, invalid, inconsistent, collapsed, deterministic_failure, canonical_break) used by all governance-aware components.
- **Section_Completeness_State**: A classification of report section rendering quality (complete, partial, degraded, unavailable, invalid).
- **Confidence_Degradation_Policy**: A configurable and versionable policy defining how confidence_level is reduced when upstream inputs are missing or degraded.
- **Schema_Version**: A version identifier attached to every persisted canonical artifact schema (Semantic_State, Reasoning_Object, Provenance, Run_Context, Deployment_Matrix).

## Requirements

### Requirement 1: Eliminate Forbidden Signal-to-Report Flows

**User Story:** As a system architect, I want all briefing outputs routed through the full Canonical Chain, so that no report content bypasses semantic interpretation and reasoning.

#### Acceptance Criteria

1. WHEN a Signal Engine produces output, THE Report_Engine SHALL consume that output only after the Semantic_Engine has interpreted the output into Semantic States and a Reasoning_Engine has produced Reasoning Objects from those Semantic States.
2. WHILE Observability_Mode is active, THE Pipeline_Orchestrator SHALL detect any data flow where a Signal Engine output reaches a Report Section without passing through both the SEMANTICS and REASONING layers, log a governance violation warning, and continue pipeline execution without blocking.
3. WHEN the Pipeline_Orchestrator detects a forbidden flow at runtime, THE Pipeline_Orchestrator SHALL log a warning containing the source Signal Engine identifier, the target Report Section name, and the list of skipped layers (SEMANTICS, REASONING, or both).
4. IF a Semantic_Engine or Reasoning_Engine is unavailable for a given signal category (defined as: the engine is not registered in the Artifact_Registry, fails to initialize, or returns an error during execution), THEN THE Pipeline_Orchestrator SHALL omit the corresponding Report Section and log a degradation warning rather than fall back to a direct Signal-to-Report flow.
5. WHEN the migration is complete, THE Pipeline_Orchestrator SHALL report zero forbidden Signal-to-Report flows across all 16 previously identified shortcuts (8 Signal Engines × 2 briefing file outputs each).

### Requirement 2: Replace Briefing Files with Chain-Compliant Outputs

**User Story:** As a portfolio manager, I want briefing content produced through the full reasoning chain, so that every insight is semantically grounded and traceable.

#### Acceptance Criteria

1. WHEN the report pipeline executes, THE Semantic_Engine SHALL produce at least one Semantic State per signal category currently served by a Briefing File (allocation, attribution, correlation, cross-asset, divergence, early-warning, flow, liquidity, market-breadth, narrative-dependency, regime, relative-strength, scenario, portfolio-memory), totaling coverage of all 14 categories.
2. WHEN Semantic States exist for a signal category, THE Reasoning_Engine SHALL produce exactly one Reasoning Object per signal category that synthesizes those states into a portfolio-level conclusion.
3. WHEN a Reasoning Object exists for a signal category, THE Report_Engine SHALL render the content from that Reasoning Object into the Report Section to which the signal category is mapped, where multiple signal categories may contribute to a single Report Section.
4. WHEN all 14 signal categories have chain-compliant outputs (Semantic State, Reasoning Object, and rendered Report Section exist for each), THE Pipeline_Orchestrator SHALL produce zero Briefing Files as direct outputs.
5. WHILE Observability_Mode is active, THE Pipeline_Orchestrator SHALL allow legacy Briefing Files to coexist alongside chain-compliant outputs and log a deprecation warning for each legacy file still generated, identifying the file name and the signal category it serves.
6. IF the Semantic_Engine fails to produce a Semantic State for one or more of the 14 signal categories, THEN THE Pipeline_Orchestrator SHALL continue processing the remaining categories and log a coverage gap warning identifying the missing categories.

### Requirement 3: Register Unregistered Artifacts

**User Story:** As a governance maintainer, I want all artifacts registered with complete metadata, so that the system has full visibility into its own structure.

#### Acceptance Criteria

1. THE Artifact_Registry SHALL contain entries for all 13 currently unregistered artifacts (as identified in the baseline health report) with all required schema fields populated: artifact_id, file_path, primary_domain, artifact_type, lifecycle_status, created_date, last_modified, owner_role, ssot_relationship, allowed_writers, allowed_readers, metadata_source, registry_mode, dependencies, and report_value.
2. WHEN a new artifact is created during this feature implementation, THE Artifact_Registry SHALL register that artifact with all required schema fields before the final commit of the implementation branch is merged.
3. WHILE Observability_Mode is active, THE Registration_Validator SHALL emit a warning entry to the validation log for each unregistered artifact detected, including the file_path and a recommendation to register, without blocking pipeline execution or commit operations.
4. WHEN all 13 artifacts have been registered, THE Registration_Validator SHALL report zero unregistered-artifact warnings in the health report violations section.

### Requirement 4: Add Report Value Metadata to All Artifacts

**User Story:** As a system architect, I want every artifact to declare its contribution to the daily report, so that the system can identify and deprecate artifacts without report value.

#### Acceptance Criteria

1. THE Artifact_Registry SHALL contain a report_value field for every registered artifact, structured as an object with a category sub-field (string) and a justification sub-field (string, maximum 200 characters).
2. WHEN a report_value field is populated, THE Report_Value_Detector SHALL validate that the category sub-field matches one of the 10 accepted categories: semantic_interpretation, pm_reasoning, concentration_explanation, dependency_explanation, scenario_interpretation, confidence_explanation, action_space_clarity, multilingual_rendering, traceability, user_understanding.
3. IF a report_value field contains a category not in the accepted list, THEN THE Report_Value_Detector SHALL flag the artifact with a warning indicating the category is invalid and requires revision.
4. IF a report_value justification sub-field contains speculative language (e.g., "might improve", "could help", "potentially", "in the future", "indirectly"), THEN THE Report_Value_Detector SHALL flag the artifact with a warning indicating the justification is speculative and requires a direct claim.
5. WHEN the Report_Value_Detector identifies an artifact with a missing or empty report_value field, THE Report_Value_Detector SHALL flag the artifact with a warning indicating missing report value metadata.
6. THE Artifact_Registry SHALL achieve 100% report_value field population across all registered artifacts within 30 days of feature activation.

### Requirement 5: Separate Portfolio State from Watchlist in Report Output

**User Story:** As a portfolio manager, I want the daily report to clearly separate current portfolio reality from watchlist candidates, so that I can distinguish between what I own and what I might deploy.

#### Acceptance Criteria

1. THE Daily_Report SHALL contain a "Current Portfolio Reality" block that presents only holdings, drivers, and risks for positions currently in the portfolio, with the "Current Portfolio Reality" block appearing before the "Watchlist and Deployment Candidates" block in the report.
2. THE Daily_Report SHALL contain a "Watchlist and Deployment Candidates" block that presents potential future exposures, deployment candidates, and their entry conditions.
3. THE Report_Engine SHALL source the "Current Portfolio Reality" block exclusively from Portfolio_State data that has passed through the Canonical Chain.
4. THE Report_Engine SHALL source the "Watchlist and Deployment Candidates" block exclusively from Watchlist data that has passed through the Canonical Chain.
5. WHEN a position transitions from Watchlist to Portfolio_State (or vice versa), THE Report_Engine SHALL render the position in its new block and include a transition notice stating the position identifier, the previous classification, and the new classification in the next report generation cycle.
6. IF a position identifier exists in both Portfolio_State and Watchlist data within the same Run_Context, THEN THE Report_Engine SHALL classify the position according to Portfolio_State, omit it from the Watchlist block, and log a data conflict warning identifying the duplicated position.
7. IF Portfolio_State or Watchlist contains zero positions for a given Run_Context, THEN THE Report_Engine SHALL render the corresponding block with an explicit empty-state notice indicating no positions are present in that category.

### Requirement 6: Generate First Correct Daily Report

**User Story:** As a portfolio manager, I want a locally generated daily report that is semantically correct and fully traceable, so that I can validate the reasoning chain produces useful output.

#### Acceptance Criteria

1. THE Report_Engine SHALL produce a `daily_report.md` file containing all 9 canonical sections in the following fixed order: Executive Summary, Market Regime, Portfolio Structure, Concentration and Dependency, Deployment Analysis, Scenario Analysis, Action Space, Confidence Interpretation, PM Summary, where each section contains at least one Reasoning Object-derived paragraph of content or a degradation notice.
2. WHEN the report pipeline executes, THE Daily_Report SHALL be written to a configurable local file path without email delivery, defaulting to the project output directory.
3. THE Daily_Report SHALL include a machine-readable Chain_Provenance metadata block (structured YAML or JSON) for each section, listing the Reasoning Object identifiers and Semantic State identifiers that produced the section content.
4. IF a Reasoning Object is missing for a canonical section, THEN THE Report_Engine SHALL render a clearly labeled degradation notice within that section header stating which Reasoning Objects and upstream Semantic States are unavailable, and SHALL NOT generate synthetic or placeholder analytical content for that section.
5. WHEN the same Run_Context inputs are provided twice, THE Report_Engine SHALL produce byte-identical Daily_Report output.
6. THE Daily_Report SHALL use plain-language explanations free of unexplained financial jargon, defining or contextualizing any domain-specific term on first use so that a non-professional investor can interpret each section without external reference material.
7. WHEN the Report_Engine renders the Daily_Report, THE Report_Engine SHALL complete the full rendering of all 9 sections within 30 seconds of receiving the complete set of Reasoning Objects.

### Requirement 7: Expand Semantic State Coverage

**User Story:** As a portfolio manager, I want semantic states for all real portfolio themes, so that the reasoning chain can interpret my actual exposures rather than operating on incomplete vocabulary.

#### Acceptance Criteria

1. THE Semantic_Signal_Registry SHALL define the following new Semantic States with complete signal structure (signal_id, category, meaning, signal_origin, reasoning_impact, confidence_behavior): semiconductor_dependency_high (category: narrative_dependency), energy_grid_dependency (category: narrative_dependency), datacenter_infrastructure_exposure (category: narrative_dependency).
2. WHEN the signal_origin engines for a new Semantic State produce outputs that satisfy the confidence_behavior conditions defined in that state's registry entry, THE Semantic_Engine SHALL detect and emit that Semantic State.
3. WHEN a new Semantic State is added to the registry, THE Semantic_Engine SHALL produce that state deterministically given the same input signals.
4. THE Semantic_Signal_Registry SHALL maintain existing Semantic States (ai_dependency_high, deployment_fully_extended, concentration_risk_elevated, portfolio_health_fragile, defense_dependency_elevated) without modification to their signal structure.
5. IF a signal_origin engine referenced by a new Semantic State is unavailable during pipeline execution, THEN THE Semantic_Engine SHALL skip emission of that state and propagate the unavailability to downstream Reasoning Engines with an explanation identifying the missing engine.

### Requirement 8: Implement Run Context for Temporal Consistency

**User Story:** As a system architect, I want all engines in a single pipeline execution to operate on the same data snapshot, so that the report reflects a consistent point-in-time view.

#### Acceptance Criteria

1. WHEN the Pipeline_Orchestrator initiates a report generation cycle, THE Pipeline_Orchestrator SHALL create a Run_Context containing a unique run identifier, an ISO 8601 UTC timestamp with second precision, and a reference to each input data source consisting of the source file path and a content hash computed at the moment of Run_Context creation.
2. WHILE a Run_Context is active, THE Pipeline_Orchestrator SHALL pass the same Run_Context to every engine in the chain (Signal, Semantic, Reasoning, Report).
3. IF an engine attempts to read an input data source whose current content hash differs from the hash recorded in the Run_Context, THEN THE Pipeline_Orchestrator SHALL reject the read, mark the affected data source as inconsistent, and log a temporal consistency violation identifying the engine, the data source, and the hash mismatch.
4. WHEN a report generation cycle completes successfully, THE Pipeline_Orchestrator SHALL persist the Run_Context metadata as a structured file (YAML or JSON) in the same output directory as the Daily_Report, named with the run identifier as prefix.
5. IF an input data source becomes unavailable or unreadable during an active Run_Context, THEN THE Pipeline_Orchestrator SHALL mark the affected signal categories as degraded, continue processing remaining categories, and include the unavailability in the Run_Context persisted metadata.
6. WHEN a previously persisted Run_Context is provided as input to the Pipeline_Orchestrator, THE Pipeline_Orchestrator SHALL use the recorded data source references to verify that identical inputs are available before re-executing the pipeline.

### Requirement 9: Define Reasoning Object Schema

**User Story:** As a system architect, I want a formal schema for Reasoning Objects, so that the interface between the SEMANTICS and REPORT layers is explicit and testable.

#### Acceptance Criteria

1. THE Reasoning_Object schema SHALL contain the following fields with types and constraints: reasoning_id (unique string, 1-128 characters), source_semantic_states (list of signal_ids, minimum 1 entry, maximum 50 entries), conclusion (key-value map containing at minimum a summary string of 1-1000 characters and a category string), confidence_level (integer 0-100), confidence_explanation (string, 1-500 characters), action_implications (list of key-value maps each containing at minimum an action string and a rationale string, 0-20 entries), temporal_validity (start and end timestamps in ISO 8601 format), producing_engine (string matching one of the registered Reasoning Engine identifiers: decision_engine, quality_engine, priority_engine).
2. WHEN a Reasoning_Engine produces a Reasoning Object, THE Reasoning_Engine SHALL populate all schema fields defined in criterion 1.
3. IF a Reasoning_Engine cannot determine a confidence_level, THEN THE Reasoning_Engine SHALL set confidence_level to 0 and provide an explanation in confidence_explanation stating why confidence cannot be assessed.
4. IF the Report_Engine receives a Reasoning Object that does not conform to the Reasoning_Object schema, THEN THE Report_Engine SHALL reject the non-conforming object, log a validation error identifying the failing field and the producing engine, and render a degradation notice in the affected Report Section.
5. WHEN a Reasoning_Engine produces a Reasoning Object, THE Reasoning_Engine SHALL include at least one valid signal_id in source_semantic_states that references an existing Semantic State from the current or most recent Run_Context.

### Requirement 10: Implement Chain Validation at Runtime

**User Story:** As a governance maintainer, I want runtime verification that every report section was produced through the full chain, so that shortcuts cannot silently reappear.

#### Acceptance Criteria

1. WHEN the Report_Engine renders a section, THE Chain_Validator SHALL verify that the section's Chain_Provenance metadata references at least one Reasoning Object identifier, that each referenced Reasoning Object's source_semantic_states field contains at least one Semantic State identifier, and that each referenced Semantic State traces to at least one Signal Engine identifier.
2. IF the Chain_Validator detects a broken provenance chain (a missing or empty reference at any layer), THEN THE Chain_Validator SHALL log a structured governance violation containing: the section name, the specific layer where the chain breaks (SIGNALS, SEMANTICS, or REASONING), the last valid identifier in the chain, and a suggested remediation action describing which engine must produce the missing link.
3. IF the Chain_Provenance metadata for a section is absent or malformed (missing required fields per the provenance schema defined in Requirement 13), THEN THE Chain_Validator SHALL treat the section as having a fully broken chain at the REASONING layer and log a governance violation.
4. WHILE Observability_Mode is active, THE Chain_Validator SHALL emit warnings for broken chains without preventing report generation and without modifying the rendered section content.
5. THE Chain_Validator SHALL complete validation of all sections within 2 seconds total, contributing no more than 2 seconds to the 30-second full pipeline budget for a daily report containing up to 9 canonical sections.

### Requirement 11: Implement Error Propagation and Graceful Degradation

**User Story:** As a portfolio manager, I want the report to degrade gracefully when upstream engines fail, so that I receive partial but honest output rather than silence or fabrication.

#### Acceptance Criteria

1. IF a Signal_Engine fails during execution (raises an unhandled exception, returns no output, or exceeds a 60-second execution timeout), THEN THE Pipeline_Orchestrator SHALL mark the affected signal categories as unavailable and continue processing remaining categories independently.
2. WHEN a signal category is marked unavailable, THE Semantic_Engine SHALL skip interpretation for that category and propagate a structured unavailability marker (containing the failed engine identifier, failure reason, and affected signal category) downstream to the Reasoning layer.
3. WHEN a Reasoning_Engine receives incomplete Semantic States due to one or more unavailability markers, THE Reasoning_Engine SHALL produce a Reasoning Object with confidence_level capped at 50 minus 10 per missing signal category (minimum 0), and an explicit confidence_explanation listing each missing input and its impact on the conclusion.
4. WHEN the Report_Engine encounters a Reasoning Object with confidence_level below 50, THE Report_Engine SHALL render the section with a degradation notice at the beginning of the section stating which signal categories were unavailable and which Signal Engines failed.
5. THE Daily_Report SHALL include a "Data Availability" summary listing all signal categories with one of the following statuses for the current Run_Context: "available", "unavailable_engine_failure", "unavailable_timeout", or "unavailable_no_output".
6. IF all Signal_Engines fail during a single Run_Context, THEN THE Pipeline_Orchestrator SHALL produce a Daily_Report containing only the "Data Availability" summary with all categories marked unavailable, and no fabricated section content.

### Requirement 12: Implement Semantic State Persistence

**User Story:** As a system architect, I want semantic states persisted between engine runs, so that the system maintains a canonical snapshot of current portfolio meaning.

#### Acceptance Criteria

1. WHEN the Semantic_Engine produces Semantic States, THE Semantic_State_Store SHALL persist those states with their Run_Context identifier and timestamp in structured YAML/JSON format.
2. THE Semantic_State_Store SHALL maintain the most recent canonical snapshot containing all Semantic States produced by the last successfully completed pipeline run, superseding any prior snapshot.
3. WHEN a new pipeline run completes and produces Semantic States that differ from the previous canonical snapshot, THE Semantic_State_Store SHALL record a delta entry listing each state addition, removal, or value change.
4. THE Semantic_State_Store SHALL support retrieval of the current canonical snapshot without re-running the Semantic_Engine, returning the complete snapshot within 5 seconds.
5. WHEN the Semantic_State_Store records a delta, THE Semantic_State_Store SHALL log each added state with its new value, each removed state with its last known value, and each changed state with both its previous and current values.
6. IF the Semantic_State_Store fails to persist states due to a write error, THEN THE Semantic_State_Store SHALL retain the previous canonical snapshot unchanged, log a persistence failure warning with the Run_Context identifier and error reason, and propagate the failure status to the Pipeline_Orchestrator.

### Requirement 13: Implement Report Provenance Metadata

**User Story:** As a portfolio manager, I want each report section to carry metadata about its sources, so that I can trace any conclusion back to its structural origin.

#### Acceptance Criteria

1. THE Daily_Report SHALL include a provenance block for each canonical section containing: the list of Reasoning Object identifiers (reasoning_id values) that produced the section, the list of Semantic State identifiers (signal_id values) consumed by those Reasoning Objects, and the list of Signal Engine identifiers that produced the original signals.
2. WHEN a report section is rendered from multiple Reasoning Objects, THE Report_Engine SHALL list all contributing Reasoning Objects in the provenance block in the order they were consumed during rendering.
3. THE provenance metadata SHALL be embedded as a single fenced code block (annotated with the language identifier "yaml" or "json") at the end of each report section, parseable by a standard YAML or JSON parser without additional transformation.
4. THE provenance metadata for each section SHALL contain a non-empty entry for each chain layer (at least one Signal Engine identifier, at least one Semantic State identifier, and at least one Reasoning Object identifier), such that the Chain_Validator can confirm no layer of the Canonical Chain was skipped by verifying all three layers are populated.
5. IF a report section is rendered in a degraded state due to upstream engine failure, THEN THE Report_Engine SHALL include a provenance block with the available chain identifiers populated and the unavailable layers marked with an explicit unavailability indicator and the reason for absence.
6. WHEN the Chain_Validator parses a provenance block, THE Chain_Validator SHALL confirm that every listed Reasoning Object identifier references at least one listed Semantic State identifier, and every listed Semantic State identifier references at least one listed Signal Engine identifier.

### Requirement 14: Define Deployment Matrix Data Structure

**User Story:** As a portfolio manager, I want the three-basket deployment model formalized as a data structure, so that deployment reasoning is explicit and traceable through the chain.

#### Acceptance Criteria

1. THE Deployment_Matrix schema SHALL define three baskets: Momentum_Core (high-conviction current positions), Diversification_Candidates (positions improving portfolio resilience), and Risk_Thresholds (positions requiring monitoring or reduction).
2. WHEN the Reasoning_Engine evaluates deployment posture, THE Reasoning_Engine SHALL classify each position into exactly one basket of the Deployment_Matrix with a confidence_level (integer 0-100) for the assignment.
3. THE Deployment_Matrix SHALL include for each position: position identifier, basket assignment, assignment rationale (referencing at least one Semantic State identifier), confidence level, and temporal_validity (ISO 8601 start and end timestamps indicating the period for which the assignment is considered valid).
4. THE Report_Engine SHALL use the Deployment_Matrix as the source for the Deployment Analysis section of the Daily_Report.
5. IF the Reasoning_Engine cannot classify a position into any basket due to insufficient Semantic States, THEN THE Reasoning_Engine SHALL assign the position to a special "unclassified" category with confidence_level 0 and an explanation of which Semantic States are missing.

### Requirement 15: Pipeline Idempotency

**User Story:** As a system architect, I want the report pipeline to produce identical outputs when run twice with the same inputs, so that report generation is deterministic and reproducible.

#### Acceptance Criteria

1. WHEN the Pipeline_Orchestrator executes with an identical Run_Context (same input data files, same timestamp, same deterministic substitutes), THE Pipeline_Orchestrator SHALL produce byte-identical Daily_Report output including all content and provenance metadata.
2. WHEN the Semantic_Engine receives identical Signal Engine outputs (field-by-field structural equality with identical ordering), THE Semantic_Engine SHALL produce Semantic States that are structurally identical in content, field values, and field ordering.
3. WHEN the Reasoning_Engine receives identical Semantic States (field-by-field structural equality with identical ordering), THE Reasoning_Engine SHALL produce Reasoning Objects that are structurally identical in content, field values, and field ordering.
4. WHEN the Report_Engine receives identical Reasoning Objects (field-by-field structural equality with identical ordering), THE Report_Engine SHALL produce Report Sections that are byte-identical in rendered output.
5. IF any engine requires a value that would introduce non-determinism (random seeds, wall-clock timestamps, iteration over unordered collections, floating-point formatting variations, or external data not captured in input files), THEN THE Pipeline_Orchestrator SHALL inject a deterministic substitute from the Run_Context before that engine executes.
6. WHEN the Pipeline_Orchestrator completes a report generation cycle, THE Pipeline_Orchestrator SHALL compute a SHA-256 hash of the Daily_Report output and record it in the Run_Context metadata to enable automated idempotency verification across repeated executions.


### Requirement 16: Canonical vs. Transient Artifact Boundary (Hardening: Semantic Atomicity Scope)

**User Story:** As a system architect, I want an explicit distinction between canonical and transient artifacts, so that governance enforcement does not create massive orchestration overhead on internal processing structures.

#### Acceptance Criteria

1. THE system SHALL classify all runtime artifacts into exactly one of two categories: Canonical_Artifact (subject to full governance enforcement) or Transient_Artifact (exempt from canonical governance).
2. THE following SHALL be classified as Canonical_Artifacts and subject to full atomic semantic integrity, determinism, and provenance requirements: persisted Semantic_State snapshots, emitted Reasoning_Objects, Daily_Report outputs, Deployment_Matrix outputs, persisted Run_Context metadata, and canonical provenance structures.
3. THE following SHALL be classified as Transient_Artifacts and exempt from full governance enforcement: internal orchestration buffers, temporary in-memory transforms, pre-validation staging structures, and intermediate draft reasoning objects.
4. Transient_Artifacts SHALL NOT cross runtime boundaries, SHALL NOT be persisted to disk, and SHALL NOT be exposed to downstream engines as canonical truth.
5. IF a Transient_Artifact is persisted or passed to a downstream engine as input, THEN THE Pipeline_Orchestrator SHALL reclassify it as a Canonical_Artifact and apply full governance enforcement from that point forward.

### Requirement 17: Canonical Severity Taxonomy (Hardening: Missing Severity Hierarchy)

**User Story:** As a governance maintainer, I want a single canonical severity taxonomy used across all validators and components, so that event classification is consistent and actionable system-wide.

#### Acceptance Criteria

1. THE system SHALL define the following canonical severity levels in ascending order of impact: info, warning, degraded, critical, canonical_break, deterministic_failure.
2. EVERY validator, orchestrator, provenance checker, semantic component, and report degradation path SHALL classify events using exclusively the canonical severity taxonomy defined in criterion 1.
3. THE severity taxonomy SHALL be defined in a single centralized location and referenced by all governance-aware components without local redefinition.
4. WHEN a component emits a governance event, THE event SHALL include the severity level, a human-readable description, the component identifier, and a timestamp.
5. THE severity taxonomy SHALL define for each level: the meaning, whether it blocks pipeline execution (in hard enforcement mode), whether it triggers audit logging, and whether it appears in the Daily_Report Data Availability summary.

### Requirement 18: Canonical Runtime State Model (Hardening: Missing Runtime State Contract)

**User Story:** As a system architect, I want a shared runtime state model used by all governance-aware components, so that state interpretation is consistent and state drift is prevented.

#### Acceptance Criteria

1. THE system SHALL define the following canonical runtime states: healthy, degraded, unavailable, invalid, inconsistent, collapsed, deterministic_failure, canonical_break.
2. ALL governance-aware components (Pipeline_Orchestrator, Chain_Validator, Registration_Validator, Semantic_Engine, Reasoning_Engines, Report_Engine, Semantic_State_Store) SHALL use exclusively the canonical runtime states defined in criterion 1.
3. THE runtime state definitions SHALL be globally defined in a single centralized location and SHALL NOT be redefined or reinterpreted locally by individual engines or components.
4. WHEN a component transitions between runtime states, THE component SHALL log the transition with the previous state, new state, reason for transition, and timestamp.
5. THE Pipeline_Orchestrator SHALL aggregate component runtime states into a pipeline-level runtime state using the highest-severity component state as the pipeline state.

### Requirement 19: Configurable Confidence Degradation Policy (Hardening: Formula Hardcode Risk)

**User Story:** As a system architect, I want the confidence degradation formula to be a configurable policy rather than hardcoded logic, so that governance rules can evolve without schema changes.

#### Acceptance Criteria

1. THE confidence degradation formula defined in Requirement 11 criterion 3 SHALL be implemented as a named confidence_degradation_policy with a version identifier, not as hardcoded arithmetic in engine logic.
2. THE confidence_degradation_policy SHALL define: the base confidence ceiling when degradation applies, the penalty per missing signal category, the minimum confidence floor, and the policy version.
3. THE default confidence_degradation_policy SHALL be: base_ceiling=50, penalty_per_missing_category=10, minimum_floor=0, version="1.0.0".
4. THE confidence_degradation_policy SHALL be configurable without modifying the Reasoning_Object schema structure or the Reasoning_Engine source code.
5. WHEN the confidence_degradation_policy is updated, THE system SHALL log the policy change with the previous version, new version, and effective timestamp.

### Requirement 20: Provenance Performance Optimization (Hardening: Quadratic Validation Growth)

**User Story:** As a system architect, I want provenance validation to use cached resolution and indexed lookups, so that chain validation does not degrade to quadratic complexity as the system scales.

#### Acceptance Criteria

1. THE Chain_Validator SHALL support cached provenance resolution, reusing previously validated chain segments within the same Run_Context without re-traversing the full object graph.
2. THE system SHALL maintain a deterministic identifier index enabling O(1) lookup of Reasoning Object identifiers, Semantic State identifiers, and Signal Engine identifiers during provenance validation.
3. THE Chain_Validator SHALL validate chain integrity for all 9 canonical sections without repeatedly traversing full object graphs, achieving worst-case O(n) complexity where n is the total number of unique identifiers across all sections.
4. WHEN the identifier index is populated during a pipeline run, THE Pipeline_Orchestrator SHALL make the index available to the Chain_Validator before validation begins.
5. THE provenance validation performance SHALL remain within the 2-second budget defined in Requirement 10 criterion 5 for reports containing up to 50 unique Reasoning Objects and 200 unique Semantic States.

### Requirement 21: Canonical Boundary Definition (Hardening: Canonical vs. Non-Canonical Truth)

**User Story:** As a governance maintainer, I want explicit rules defining what constitutes canonical truth, so that degraded placeholders and compatibility artifacts are never confused with authoritative system output.

#### Acceptance Criteria

1. THE following SHALL be considered canonical truth when valid: Semantic_States with runtime state "healthy", Reasoning_Objects conforming to schema with confidence_level above 0, Daily_Report outputs produced through complete chain validation, Deployment_Matrix outputs with at least one classified position, and Run_Context snapshots persisted after successful pipeline completion.
2. THE following SHALL NOT be considered canonical truth under any circumstances: degraded placeholder content in report sections, observability warnings and governance event logs, compatibility briefing files (legacy), transient orchestration artifacts, and intermediate draft reasoning objects that have not passed schema validation.
3. WHEN the Report_Engine renders degraded content, THE Report_Engine SHALL mark the degraded content with a visible non-canonical indicator so that consumers can distinguish it from canonical conclusions.
4. THE Chain_Validator SHALL verify that only canonical artifacts are referenced in provenance metadata, rejecting references to non-canonical artifacts.

### Requirement 22: Determinism Scope Clarification (Hardening: Overkill Prevention)

**User Story:** As a system architect, I want determinism requirements scoped precisely to canonical outputs, so that implementation does not waste effort enforcing byte-identity on internal transient structures.

#### Acceptance Criteria

1. Byte-identical determinism requirements (as defined in Requirement 15) SHALL apply exclusively to: persisted Daily_Report output, persisted Run_Context metadata, persisted Semantic_State snapshots, persisted Reasoning_Objects, persisted Deployment_Matrix outputs, and persisted provenance metadata.
2. Internal runtime memory layout, temporary orchestration ordering, in-memory collection iteration order, and non-persisted transient structures SHALL NOT require byte-level determinism unless explicitly persisted or externally exposed.
3. WHEN a transient structure is promoted to canonical status (per Requirement 16 criterion 5), THE Pipeline_Orchestrator SHALL apply deterministic serialization at the point of promotion, not retroactively to the transient processing history.

### Requirement 23: Schema Version Contracts (Hardening: Missing Version Governance)

**User Story:** As a system architect, I want every persisted canonical artifact to carry a schema version identifier, so that future schema evolution does not break compatibility silently.

#### Acceptance Criteria

1. THE following schemas SHALL carry a canonical version identifier: Semantic_State schema, Reasoning_Object schema, provenance schema, Run_Context schema, Deployment_Matrix schema.
2. EVERY persisted canonical artifact SHALL include its schema_version field as a required metadata attribute, using semantic versioning format (MAJOR.MINOR.PATCH).
3. WHEN a schema is modified, THE schema version SHALL be incremented according to semantic versioning rules: MAJOR for breaking changes, MINOR for backward-compatible additions, PATCH for clarifications without structural change.
4. THE Pipeline_Orchestrator SHALL validate that all artifacts consumed during a pipeline run use compatible schema versions (same MAJOR version) and log a warning if MINOR versions differ between producer and consumer.

### Requirement 24: Report Section Completeness States (Hardening: Section Atomicity)

**User Story:** As a system architect, I want explicit section completeness states, so that the Report_Engine determines rendering behavior from a formal state model rather than ad hoc local logic.

#### Acceptance Criteria

1. THE Report_Engine SHALL classify each report section into exactly one of the following completeness states before rendering: complete (all Reasoning Objects available and valid), partial (some Reasoning Objects available, others degraded), degraded (Reasoning Objects available but with low confidence), unavailable (no Reasoning Objects available for this section), invalid (Reasoning Objects present but failing schema validation).
2. THE Report_Engine SHALL determine section rendering behavior from the section completeness state: "complete" renders full content, "partial" renders available content with a partial-data notice, "degraded" renders content with a confidence warning, "unavailable" renders only a degradation notice, "invalid" renders an error notice with remediation guidance.
3. THE section completeness state SHALL be included in the provenance metadata block for each section.
4. THE Report_Engine SHALL NOT use ad hoc conditional logic to determine rendering behavior; all rendering decisions SHALL flow from the section completeness state classification.

### Requirement 25: Compatibility Sunset Governance (Hardening: Legacy Briefing Lifecycle)

**User Story:** As a governance maintainer, I want legacy compatibility briefing files to have explicit sunset dates and migration tracking, so that they cannot persist indefinitely.

#### Acceptance Criteria

1. EACH legacy Briefing_File that continues to be generated during Observability_Mode SHALL be annotated in the Artifact_Registry with: deprecation_start_date (the date chain-compliant replacement became available), sunset_target_date (the date after which the briefing file SHALL no longer be generated), and downstream_dependency_count (the number of components still consuming the legacy file).
2. THE observability reporting (health report) SHALL expose for each compatibility briefing file: the age since deprecation_start_date, the remaining days until sunset_target_date, and the current downstream_dependency_count.
3. WHEN a Briefing_File reaches its sunset_target_date and downstream_dependency_count is zero, THE Pipeline_Orchestrator SHALL stop generating that file and log a sunset completion event.
4. IF a Briefing_File reaches its sunset_target_date but downstream_dependency_count is greater than zero, THEN THE Pipeline_Orchestrator SHALL continue generating the file, log a sunset-blocked warning with the list of remaining consumers, and escalate the event to severity level "critical".
