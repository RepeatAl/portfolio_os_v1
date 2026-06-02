# Implementation Plan

## Overview

Domainization system implementation for Portfolio OS. Establishes governed repository cognition through artifact registry, domain boundaries, lifecycle state machines, validation observers, CLI tooling, and health reporting.

**Governance Mode**: FOUNDATION + OBSERVABILITY  
**Core Principle**: A visible unhealthy system is preferable to an invisible blocked system during FAST LANE phase.

### Active Capabilities
- ✅ Artifact indexing and registry
- ✅ Lifecycle tracking and visibility
- ✅ Dependency mapping
- ✅ SSOT visibility
- ✅ Deployment harmonization (Google-only)
- ✅ Runtime observability
- ✅ Health reporting
- ✅ Validation observers (warnings only)

### Deferred Capabilities
- ⏸️ Hard commit blocking
- ⏸️ Workflow interruption
- ⏸️ Mandatory metadata enforcement
- ⏸️ Runtime flow blocking
- ⏸️ Governance-first friction

### Implementation Strategy

**All validation gates operate in OBSERVABILITY MODE**:
- Generate warnings, not errors
- Report violations, don't block commits
- Build visibility, not enforcement
- Help reasoning, not punish contributors

**Pre-commit hooks are OPTIONAL HELPERS**:
- Optional installation
- Warnings only
- Dependency visibility
- Lifecycle hints

**Registry is DISCOVERY LAYER**:
- Artifacts may exist unregistered during FAST LANE
- Health reports expose gaps
- No mandatory bureaucracy

**Deployment harmonization is ACTIVE**:
- Google-only scanning (warnings)
- Provider detection (reports)
- Deployment topology mapping

---

## Post-Task Completion Rule

**After completing each task**, create a README file in `.domainization/src/` documenting what was implemented. Follow the existing pattern (see `README_registry_cache.md` or `README_backup_and_recovery.md` for reference).

- Naming: `README_<descriptive_topic>.md`
- Sections: Overview, Features, Usage (with code examples), Testing (with run commands), Requirements Satisfied, Related Files
- Language: English
- Scope: All modules, classes, and CLI commands created in the task

---

## Tasks

### Tasks Overview

- [x] 1. Create foundation infrastructure
  - Create `.domainization/` directory structure with subdirectories for backups, logs, reports, hooks, and src
  - Create empty registry files as templates
  - _Requirements: 1.1, 1.2_

- [x] 1.1 Create domain registry with 12 canonical domains
  - Write `domain_registry.yaml` with all 12 domains (GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM)
  - Define responsibility_scope, allowed_artifact_types, priority (core/surface), and authority_level for each domain
  - Add core reasoning chain priority: SIGNALS (1) → SEMANTICS (2) → REASONING (3) → REPORT (4)
  - Write unit tests to validate domain registry schema and domain definitions
  - _Requirements: 2.1, 2.2, 2.3, 2.8, 2.9, 2.10_

- [x] 1.2 Create lifecycle state machines for all artifact types
  - Write `lifecycle_state_machine.yaml` with state machines for SSOT, ENGINE, REPORT_OUT, DATA_IN, DATA_OUT, RUNTIME, DASHBOARD, SNAPSHOT, CONFIG, CALIBRATION, STEERING
  - Define states and valid transitions for each artifact type
  - Document transition conditions
  - Write unit tests to validate state machine definitions and transition logic
  - _Requirements: 3.1, 3.2, 3.3, 3.7, 4.1, 4.2, 4.3_

- [x] 1.3 Create artifact registry template
  - Write `artifact_registry.yaml` template with metadata schema documentation
  - Include example entries for each artifact type
  - Document required and optional fields
  - Write schema validation function
  - _Requirements: 1.2, 1.5, 8.1, 8.2, 8.3_

- [x] 2. Implement registry layer Python modules
  - Create Python package structure in `.domainization/src/`
  - Implement core data models and registry operations
  - _Requirements: 1.1, 1.2, 1.6_

- [x] 2.1 Implement artifact metadata data model
  - Create `ArtifactMetadata` dataclass with all required and optional fields
  - Implement `validate()` method to check metadata completeness
  - Implement `is_modifiable()` method to check if artifact can be modified
  - Implement `can_write()` and `can_read()` methods for permission checking
  - Write unit tests for metadata validation and permission checks
  - _Requirements: 8.1, 8.2, 8.4, 8.5, 8.6_

- [x] 2.2 Implement domain definition data model
  - Create `DomainDefinition` dataclass with domain properties
  - Implement `can_own_type()` method to validate artifact type ownership
  - Implement `is_core_domain()` and `get_authority_level()` methods
  - Write unit tests for domain validation logic
  - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.8_

- [x] 2.3 Implement lifecycle state machine data model
  - Create `StateTransition` and `StateMachine` dataclasses
  - Implement `is_valid_transition()` method to validate state transitions
  - Implement `get_allowed_transitions()` method to get valid next states
  - Implement `get_initial_state()` method for new artifacts
  - Write unit tests for state machine logic
  - _Requirements: 4.1, 4.2, 4.3, 4.7_



- [x] 2.4 Implement artifact registry operations
  - Create `ArtifactRegistry` class with YAML loading and saving
  - Implement `register_artifact()` method to add new artifacts
  - Implement `update_artifact()` method to modify existing artifacts
  - Implement `get_artifact()` method to retrieve artifact by ID
  - Implement `list_artifacts_by_domain()`, `list_artifacts_by_type()`, and `list_artifacts_by_lifecycle()` query methods
  - Implement frontmatter parsing for markdown files
  - Write unit tests for all registry operations
  - _Requirements: 1.2, 1.3, 1.4, 1.5, 1.6, 8.3, 8.4_

- [x] 2.5 Implement domain registry operations
  - Create `DomainRegistry` class with YAML loading
  - Implement `get_domain()` method to retrieve domain by ID
  - Implement `list_domains()`, `list_core_domains()`, and `list_surface_domains()` methods
  - Implement `validate_domain_assignment()` method to check if domain can own artifact type
  - Write unit tests for domain registry operations
  - _Requirements: 2.1, 2.2, 2.3, 2.6, 2.7_

- [x] 2.6 Implement lifecycle state machine operations
  - Create `LifecycleManager` class with state machine loading
  - Implement `get_state_machine()` method to retrieve state machine for artifact type
  - Implement `validate_transition()` method to check if transition is valid
  - Implement `get_allowed_transitions()` method to get valid next states
  - Implement `is_modifiable()` method to check if artifact can be modified based on lifecycle
  - Write unit tests for lifecycle operations
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.7_

- [x] 3. Implement validation observers (warnings only, no blocking)
  - Create validator modules for observability and health reporting
  - All validators operate in soft mode: warnings only, no commit blocking
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10_

- [x] 3.1 Implement Observer 1: Artifact Registration Validator
  - Create `RegistrationValidator` class
  - Detect unregistered artifacts and generate warnings
  - Implement metadata schema validation (warnings only)
  - Generate actionable suggestions for registration
  - Write unit tests for registration detection
  - _Requirements: 5.2, 8.5, 8.6, 8.7_

- [x] 3.2 Implement Observer 2: Domain Assignment Validator
  - Create `DomainAssignmentValidator` class
  - Detect invalid domain assignments and generate warnings
  - Suggest valid domains for artifact types
  - Write unit tests for domain assignment detection
  - _Requirements: 5.3, 2.6, 2.7_

- [x] 3.3 Implement Observer 3: Lifecycle Validator
  - Create `LifecycleValidator` class
  - Detect invalid lifecycle transitions and generate warnings
  - Detect deprecated artifact modifications and generate warnings
  - Suggest valid transitions
  - Write unit tests for lifecycle detection
  - _Requirements: 5.4, 4.3, 4.4, 4.5, 4.6, 4.7_

- [x] 3.4 Implement Observer 4: Boundary Awareness Validator
  - Create `BoundaryAwarenessValidator` class
  - Detect authority chain violations and generate warnings
  - Report when SIGNALS writes non-signal artifacts
  - Report when SEMANTICS writes non-semantic artifacts
  - Report when REASONING writes non-reasoning artifacts
  - Report when REPORT writes business logic
  - Generate explanatory warnings about authority chains
  - Write unit tests for boundary detection
  - _Requirements: 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 6.7, 13.1-13.14, 14.8, 14.9, 14.10_

- [x] 3.5 Implement Observer 5: SSOT Consistency Validator
  - Create `SSOTConsistencyValidator` class
  - Detect multiple canonical SSOTs and generate warnings
  - Detect missing SSOT references and generate warnings
  - Suggest SSOT relationship corrections
  - Write unit tests for SSOT detection
  - _Requirements: 5.6, 7.1, 7.2, 7.3, 7.4, 7.5, 7.7_

- [x] 3.6 Implement validation orchestrator (observability mode)
  - Create `ValidationOrchestrator` class to run all 5 observers
  - Collect warnings from all observers (never block)
  - Generate comprehensive observability report
  - Implement performance monitoring (target < 5 seconds)
  - Write integration tests for full observer execution
  - _Requirements: 5.1, 5.7, 5.8, 15.1, 15.5_

- [x] 4. Implement reporting layer
  - Create health reporting and violation detection modules
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [x] 4.1 Implement health reporter
  - Create `HealthReporter` class
  - Implement `generate_health_report()` method to create comprehensive health report
  - Implement `get_domain_coverage()` method to calculate artifact distribution by domain
  - Implement `get_lifecycle_distribution()` method to calculate artifact distribution by lifecycle state
  - Generate report in YAML format with summary, domain coverage, lifecycle distribution, violations, and recommendations
  - Implement performance optimization (target < 10 seconds for 1000 artifacts)
  - Write unit tests for health reporting
  - _Requirements: 10.1, 10.2, 10.3, 10.6, 15.3_

- [x] 4.2 Implement violation detector
  - Create `ViolationDetector` class
  - Implement detection logic for unregistered artifacts
  - Implement detection logic for missing lifecycle status
  - Implement detection logic for SSOT conflicts
  - Implement detection logic for deprecated artifact modifications
  - Generate violations with severity levels (critical, high, medium, low)
  - Generate actionable recommendations for each violation
  - Write unit tests for violation detection
  - _Requirements: 10.4, 10.5_

- [x] 5. Implement registry caching for performance
  - Create caching layer to optimize registry queries
  - _Requirements: 15.1, 15.2, 15.5_

- [x] 5.1 Implement registry cache
  - Create `RegistryCache` class with in-memory caching
  - Implement cache invalidation on registry modification
  - Implement cache loading with file modification time checking
  - Create indexes for artifact_id, domain_id, artifact_type, lifecycle_status, and topic
  - Implement optimized query methods using indexes
  - Write unit tests for cache operations and invalidation
  - Write performance tests to verify < 5 second validation time for 1000 artifacts
  - _Requirements: 15.1, 15.2, 15.9_



- [x] 6. Implement optional pre-commit hook (observability helper)
  - Create optional pre-commit hook for developer observability
  - Hook provides warnings and hints, never blocks commits
  - _Requirements: 5.1, 5.7, 5.8_

- [x] 6.1 Create optional pre-commit hook script
  - Write `.domainization/hooks/pre-commit` bash script
  - Detect changed files in git staging area
  - Call Python validation orchestrator
  - Display warnings and suggestions (never block)
  - Support --no-verify bypass (no audit needed, since it never blocks)
  - Write integration tests for hook execution
  - _Requirements: 5.1, 5.7, 5.8_

- [x] 6.2 Create optional hook installation script
  - Write script to optionally install pre-commit hook
  - Clearly document that hook is optional and non-blocking
  - Create backup of existing pre-commit hook if present
  - Make hook executable
  - Provide uninstall option
  - Write documentation emphasizing optional nature
  - _Requirements: 5.1_

- [x] 7. Implement command-line interface
  - Create CLI for registry management and validation
  - _Requirements: 1.1, 1.2, 1.3, 1.6, 5.1, 10.1_

- [x] 7.1 Implement registry management commands
  - Create `domainization register` command to register new artifacts
  - Create `domainization update` command to update artifact metadata
  - Create `domainization list` command with filters for domain, type, and lifecycle
  - Create `domainization show` command to display artifact details
  - Implement argument parsing and validation
  - Write integration tests for CLI commands
  - _Requirements: 1.2, 1.3, 1.6_

- [x] 7.2 Implement validation commands
  - Create `domainization validate` command to run commit gates on current repository state
  - Support validation of specific files
  - Support running specific gates
  - Implement dry-run mode
  - Display validation results with color-coded output
  - Write integration tests for validation commands
  - _Requirements: 5.1, 5.7, 5.8_

- [x] 7.3 Implement health reporting commands
  - Create `domainization health` command to generate health report
  - Support filtering by domain
  - Support output to file
  - Support violations-only mode
  - Display health report in human-readable format
  - Write integration tests for health commands
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [x] 7.4 Implement configuration commands
  - Create `domainization config show` command to display current configuration
  - Create `domainization config set` command to modify configuration
  - Support setting enforcement_mode (soft/hard)
  - Support enabling/disabling specific gates
  - Write configuration to `.domainization/config.yaml`
  - Write integration tests for config commands
  - _Requirements: 5.9, 5.10, 9.8, 9.9_



- [x] 8. Register existing SSOT documents
  - Add YAML frontmatter to all markdown files in `docs/` directory
  - _Requirements: 1.2, 1.5, 9.1, 9.2, 9.3_

- [x] 8.1 Register governance domain SSOT documents
  - Add frontmatter to `docs/decision_governance.md` with primary_domain="GOV", artifact_type="SSOT", lifecycle_status="canonical"
  - Add frontmatter to `docs/confidence_model.md`
  - Add frontmatter to `docs/action_space_framework.md`
  - Validate frontmatter schema
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 8.2 Register architecture domain SSOT documents
  - Add frontmatter to `docs/system_architecture.md` with primary_domain="ARCH", artifact_type="SSOT", lifecycle_status="canonical"
  - Add frontmatter to `docs/engine_design_principles.md`
  - Add frontmatter to `docs/report_pipeline_architecture.md`
  - Add frontmatter to `docs/semantic_reasoning_rules.md`
  - Add frontmatter to `docs/domainization_architecture.md`
  - Add frontmatter to `docs/kiro_calibration_report.md` with artifact_type="CALIBRATION"
  - Validate frontmatter schema
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 8.3 Register signals domain SSOT documents
  - Add frontmatter to `docs/semantic_signal_registry.md` with primary_domain="SIGNALS", artifact_type="SSOT", lifecycle_status="canonical"
  - Add frontmatter to `docs/signal_calculation_framework.md`
  - Add frontmatter to `docs/portfolio_health_framework.md`
  - Add frontmatter to `docs/correlation_dependency_framework.md`
  - Add frontmatter to `docs/scoring_methodology_framework.md`
  - Add frontmatter to `docs/opportunity_engine_design.md`
  - Add frontmatter to `docs/market_regime_framework.md`
  - Validate frontmatter schema
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 8.4 Register semantics and reasoning domain SSOT documents
  - Review existing SSOT documents to determine if they belong to SEMANTICS or REASONING domain
  - Add appropriate frontmatter with primary_domain="SEMANTICS" or "REASONING"
  - Validate frontmatter schema
  - _Requirements: 1.2, 1.5, 2.3, 2.8, 2.9_

- [x] 8.5 Register report domain SSOT documents
  - Add frontmatter to `docs/report_reasoning_system.md` with primary_domain="REPORT", artifact_type="SSOT", lifecycle_status="canonical"
  - Add frontmatter to `docs/report_section_specification.md`
  - Add frontmatter to `docs/multilingual_rendering_framework.md`
  - Validate frontmatter schema
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 8.6 Register remaining domain SSOT documents
  - Add frontmatter to STATE domain documents (`docs/portfolio_state_model.md`, `docs/watchlist_asset_registry_framework.md`)
  - Add frontmatter to DATA domain documents (`docs/data_ingestion_normalization_framework.md`, `docs/trusted_signal_sources.md`)
  - Add frontmatter to USER domain documents (`docs/dashboard_philosophy.md`)
  - Add frontmatter to MEMORY domain documents (`docs/portfolio_memory_architecture.md`)
  - Add frontmatter to SIM domain documents (`docs/simulation_architecture.md`)
  - Validate frontmatter schema
  - _Requirements: 1.2, 1.5, 2.3_



- [x] 9. Register implementation engines
  - Add registry entries for all Python engine files
  - _Requirements: 1.2, 1.5, 9.1, 9.2, 9.3_

- [x] 9.1 Register signal generation engines
  - Add registry entries for `engines/allocation_engine.py`, `engines/regime_engine.py`, `engines/attribution_engine.py` with primary_domain="SIGNALS", artifact_type="ENGINE", lifecycle_status="active"
  - Add registry entries for other signal engines
  - Reference SSOT specifications in dependencies field
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3, 7.3_

- [x] 9.2 Register semantic and reasoning engines
  - Add registry entry for `engines/semantic_engine.py` with primary_domain="SEMANTICS", artifact_type="ENGINE", lifecycle_status="active"
  - Add registry entries for reasoning engines (`engines/decision_engine.py`, `engines/quality_engine.py`, `engines/priority_engine.py`) with primary_domain="REASONING"
  - Reference SSOT specifications in dependencies field
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3, 2.8, 2.9, 7.3_

- [x] 9.3 Register report engines
  - Add registry entries for `engines/report_engine.py`, `engines/morning_briefing_engine.py`, `engines/delta_engine.py`, `reports/pm_report_engine.py` with primary_domain="REPORT", artifact_type="ENGINE", lifecycle_status="active"
  - Reference SSOT specifications in dependencies field
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3, 7.3_

- [x] 9.4 Register remaining engines
  - Add registry entries for `engines/scenario_engine.py` with primary_domain="SIM"
  - Add registry entries for `engines/visual_engine.py` with primary_domain="USER"
  - Add registry entries for `engines/engine_registry.py` and `engines/engine_runner.py` with primary_domain="ARCH"
  - Reference SSOT specifications in dependencies field
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3, 7.3_

- [x] 10. Register report outputs
  - Add registry entries for all report text files
  - _Requirements: 1.2, 1.5, 9.1, 9.2, 9.3_

- [x] 10.1 Register main report outputs
  - Add registry entries for `portfolio_report.txt` and `morning_briefing.txt` with primary_domain="REPORT", artifact_type="REPORT_OUT", lifecycle_status="current"
  - Reference report engine dependencies
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 10.2 Register briefing outputs
  - Add registry entries for all `*_briefing.txt` files with primary_domain="REPORT", artifact_type="REPORT_OUT", lifecycle_status="current"
  - Reference corresponding engine dependencies
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3_



- [x] 11. Register data artifacts
  - Add registry entries for all data files (Excel and JSON)
  - _Requirements: 1.2, 1.5, 9.1, 9.2, 9.3_

- [x] 11.1 Register signal output data files
  - Add registry entries for `allocation_engine.xlsx`, `attribution_engine.xlsx`, `regime_engine.xlsx`, etc. with primary_domain="SIGNALS", artifact_type="DATA_OUT", lifecycle_status="current"
  - Reference generating engine dependencies
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 11.2 Register portfolio state data files
  - Add registry entries for `watchlist.xlsx`, `data.json`, `portfolio_output.xlsx` with primary_domain="STATE", artifact_type="DATA_IN" or "DATA_OUT"
  - Reference SSOT specifications in dependencies field
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 11.3 Register historical data files
  - Add registry entries for files in `history/` directory with primary_domain="MEMORY", artifact_type="SNAPSHOT", lifecycle_status="archived"
  - Add registry entries for files in `data/` directory
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 12. Register runtime and configuration artifacts
  - Add registry entries for runtime entry points and configuration files
  - _Requirements: 1.2, 1.5, 9.1, 9.2, 9.3_

- [x] 12.1 Register runtime entry points
  - Add registry entry for `main.py` with primary_domain="DEPLOY", artifact_type="RUNTIME", lifecycle_status="active"
  - Add registry entry for `app.py` with primary_domain="USER", artifact_type="DASHBOARD", lifecycle_status="active"
  - Validate registry entries
  - _Requirements: 1.2, 1.5, 2.3_

- [x] 13. Implement error handling and logging
  - Create error handling infrastructure for validation failures
  - _Requirements: 5.7, 15.4, 15.11, 15.12_

- [x] 13.1 Implement validation error classes
  - Create `ValidationError` dataclass with gate_name, artifact_id, error_code, error_message, suggestion, severity, enforcement_mode
  - Define error codes (E001-E010) for common validation failures
  - Implement error message formatting with actionable suggestions
  - Write unit tests for error handling
  - _Requirements: 5.7, 15.4_

- [x] 13.2 Implement audit logging
  - Create audit log system to track artifact registration, metadata changes, lifecycle transitions, validation failures, and bypass usage
  - Write logs to `.domainization/logs/audit_*.log`
  - Implement log rotation
  - Write unit tests for logging
  - _Requirements: 15.11, 15.12, 15.13_



- [x] 14. Implement backup and recovery
  - Create backup system for registry files
  - _Requirements: 9.6, 15.11_

- [x] 14.1 Implement automatic registry backup
  - Create backup before every registry write operation
  - Save backups to `.domainization/backups/` with timestamp
  - Implement backup retention policy (keep last 10 backups)
  - Write unit tests for backup operations
  - _Requirements: 9.6_

- [x] 14.2 Implement registry recovery
  - Create recovery command to restore from backup
  - Implement registry validation after recovery
  - Generate health report after recovery
  - Write integration tests for recovery
  - _Requirements: 9.6_

- [x] 15. Write comprehensive documentation
  - Create developer and architecture documentation
  - _Requirements: 15.10_

- [x] 15.1 Write getting started guide
  - Document what domainization is and why it exists
  - Explain how it affects developer workflow
  - Provide quick start tutorial
  - Include examples of adding metadata
  - _Requirements: 15.10_

- [x] 15.2 Write domain guide
  - Document all 12 domains with responsibilities
  - Explain what each domain can and cannot own
  - Document authority chain (SIGNALS → SEMANTICS → REASONING → REPORT)
  - Provide examples for each domain
  - _Requirements: 2.1, 2.2, 2.5, 2.8, 2.9, 14.8, 14.9_

- [x] 15.3 Write artifact type guide
  - Document all 11 artifact types
  - Explain lifecycle states for each type
  - Provide guidance on when to use each type
  - Include examples
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2_

- [x] 15.4 Write metadata guide
  - Document required and optional metadata fields
  - Explain how to add YAML frontmatter
  - Explain how to register in artifact_registry.yaml
  - Provide templates and examples
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 15.5 Write troubleshooting guide
  - Document common validation errors and resolutions
  - Explain when to use emergency bypass
  - Provide contact information for help
  - Include FAQ section
  - _Requirements: 5.7, 15.4_

- [x] 15.6 Write architecture documentation
  - Document system architecture with component diagrams
  - Explain design decisions and rationale
  - Document extension points for adding domains, artifact types, and gates
  - _Requirements: 15.10_



- [x] 16. Implement Google-only deployment observability
  - Add detection for forbidden cloud provider references (warnings only)
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

- [x] 16.1 Implement cloud provider pattern detection
  - Create pattern matching logic to detect AWS, Supabase, Azure references
  - Define forbidden patterns (aws., supabase., azure., .amazonaws.com, supabase.co)
  - Define allowed patterns (google., googleapis.com, gcp.)
  - Implement file scanning for provider references
  - Write unit tests for pattern detection
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

- [x] 16.2 Integrate cloud provider detection into observers
  - Add cloud provider detection to Observer 4 (Boundary Awareness)
  - Generate warnings for forbidden provider references (no blocking)
  - Report which provider and where it was found
  - Write integration tests for cloud provider detection
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.7_

- [x] 17. Implement report-first observability
  - Add detection for features without report value justification (warnings only)
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 12.10_

- [x] 17.1 Create report value detection framework
  - Define allowed report value categories
  - Create detection logic to check for report value justification
  - Generate report-value health scores
  - Write unit tests for report value detection
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_

- [x] 17.2 Integrate report-first detection into observers
  - Add report value detection to Observer 4 (Boundary Awareness)
  - Generate warnings for missing report value (no blocking)
  - Show report-value health score in health reports
  - Identify infrastructure-heavy drift
  - Write integration tests for report-first detection
  - _Requirements: 12.1, 12.2, 12.8, 12.9, 12.10_

- [x] 18. Implement runtime flow observability
  - Add detection for forbidden runtime flows (warnings and visualization only)
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 14.10_

- [x] 18.1 Create runtime flow detector
  - Define allowed flows (Signal → Semantic → Reasoning → Report)
  - Define forbidden flows (Signal → Report, Dashboard → Semantic Truth, etc.)
  - Implement flow detection based on artifact dependencies
  - Implement authority chain visualization
  - Write unit tests for flow detection
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.8, 14.9, 14.10_

- [x] 18.2 Integrate runtime flow detection into observers
  - Add flow detection to Observer 4 (Boundary Awareness)
  - Check artifact dependencies for forbidden flows
  - Generate warnings explaining authority chain violations (no blocking)
  - Visualize detected flows in health reports
  - Write integration tests for runtime flow detection
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7_



- [x] 19. Write comprehensive test suite
  - Create unit, integration, and acceptance tests
  - _Requirements: 15.1, 15.2, 15.3, 15.5, 15.6, 15.7, 15.8, 15.9_

- [x] 19.1 Write unit tests for all components
  - Write tests for artifact metadata validation
  - Write tests for domain definition validation
  - Write tests for lifecycle state machine logic
  - Write tests for all 5 commit gates
  - Write tests for health reporter and violation detector
  - Write tests for registry cache
  - Achieve > 90% code coverage
  - _Requirements: 15.1, 15.2, 15.3, 15.5, 15.6, 15.7, 15.8_

- [x] 19.2 Write integration tests for end-to-end flows
  - Write tests for complete commit gate execution flow
  - Write tests for registry persistence and loading
  - Write tests for CLI commands
  - Write tests for pre-commit hook execution
  - Write tests for backup and recovery
  - _Requirements: 15.1, 15.2, 15.3, 15.5_

- [x] 19.3 Write performance tests
  - Write tests for commit gate execution time with 100, 1000 artifacts
  - Write tests for health report generation time
  - Write tests for registry query performance
  - Verify < 5 second validation time target
  - Verify < 10 second health report generation target
  - _Requirements: 15.1, 15.2, 15.3, 15.9_

- [x] 19.4 Write acceptance tests
  - Write scenario tests for new developer adding feature
  - Write scenario tests for invalid domain assignment
  - Write scenario tests for SSOT conflict
  - Write scenario tests for gradual migration
  - Use Gherkin format for test scenarios
  - _Requirements: 15.1, 15.2, 15.3, 15.5_

- [x] 20. Configure observability mode for FAST LANE phase
  - Set system to observability-only mode (warnings, no blocking)
  - _Requirements: 5.9, 5.10, 9.8, 9.9, 12.8, 12.9_

- [x] 20.1 Create configuration file for observability mode
  - Create `.domainization/config.yaml` with enforcement_mode="observability"
  - Document that system operates in warning-only mode during FAST LANE
  - Document configuration options
  - _Requirements: 5.9, 5.10, 9.8_

- [x] 20.2 Ensure all observers respect observability mode
  - Verify all observers generate warnings only
  - Verify no blocking behavior exists
  - Verify commits always proceed
  - Log all violations for visibility
  - Write tests for observability-only behavior
  - _Requirements: 5.9, 5.10, 9.8, 9.9_

- [x] 21. Generate initial health report
  - Run health report to establish baseline
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [x] 21.1 Generate and review baseline health report
  - Run `domainization health` command
  - Review registration coverage (should be 100% after registration tasks)
  - Review domain coverage distribution
  - Review lifecycle distribution
  - Identify any violations
  - Document baseline metrics
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [x] 22. Install optional pre-commit hook
  - Optionally install hook for developer observability
  - _Requirements: 5.1_

- [x] 22.1 Document and optionally install pre-commit hook
  - Document that hook is optional and provides observability only
  - Run hook installation script if developer chooses
  - Test hook with sample commit (verify warnings displayed, commit proceeds)
  - Document hook usage for team
  - _Requirements: 5.1, 5.9, 5.10_

## Task Dependency Graph

```json
{
  "waves": [
    { "wave": 1, "tasks": ["1", "1.1", "1.2", "1.3"] },
    { "wave": 2, "tasks": ["2", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6"] },
    { "wave": 3, "tasks": ["3", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6"] },
    { "wave": 4, "tasks": ["4", "4.1", "4.2"] },
    { "wave": 5, "tasks": ["5", "5.1", "5.2", "5.3", "5.4"] },
    { "wave": 6, "tasks": ["6", "7"] },
    { "wave": 7, "tasks": ["8", "8.1", "8.2", "8.3", "9", "9.1", "9.2", "9.3", "9.4", "9.5", "10", "10.1", "10.2", "11", "11.1", "11.2", "11.3"] },
    { "wave": 8, "tasks": ["12", "12.1", "12.2", "13", "13.1", "14", "14.1", "15", "15.1", "16", "16.1", "17", "17.1", "18", "18.1", "19", "19.1", "20", "20.1"] },
    { "wave": 9, "tasks": ["21", "21.1", "22", "22.1"] }
  ]
}
```

## Notes

- All validation operates in OBSERVABILITY MODE (warnings only, no blocking)
- Pre-commit hooks are optional helpers, not mandatory gates
- Registry is a discovery layer — artifacts may exist unregistered during FAST LANE phase
- Governance stabilization audit completed 2026-05-25 (see `reports/governance_stabilization_verification_2026-05-25.md`)
- Three hardenings applied: `regenerable_states`, `mirror_only` registry mode, `--force` audit trail
