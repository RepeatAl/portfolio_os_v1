# Requirements Document

## Introduction

This document specifies the requirements for transitioning the Portfolio OS governance system from Level 1 (Observability Only) to Level 2+ (Auditable/Enforceable). The system currently detects 15+ categories of violations across 5 observers but cannot prevent any of them. CI validates approximately 10% of what the runtime depends on. All governance is advisory — the pre-commit hook always exits 0, enforcement mode is permanently "observability", and no transition mechanism exists.

This spec covers six areas: CI Runtime Hardening, Deployment Gate Enforcement, Lifecycle Runtime Enforcement, Mutation Audit Ledger, Boundary Enforcement Runtime, and Warning Governance. The goal is to raise the deployment integrity score from 1.0/10 to ≥6.0/10 and advance governance maturity from Level 1 to Level 2 minimum, while preserving all existing invariants and never blocking pipeline execution in observability mode.

## Glossary

- **Governance_Runtime**: The collection of modules in `.domainization/src/`, `governance/`, and `runtime/` that detect, report, and (after this spec) enforce governance rules
- **Enforcement_Mode**: A configuration value in `.domainization/config.yaml` controlling governance behavior; one of `observability`, `soft`, or `hard`
- **CI_Pipeline**: The GitHub Actions workflow defined in `.github/workflows/python-app.yml` that validates code on push and PR
- **Deployment_Gate**: A named, independently configurable check within the CI_Pipeline that produces a structured pass/fail result
- **Lifecycle_State_Machine**: The YAML-defined set of valid states and transitions per artifact type in `.domainization/lifecycle_state_machine.yaml`
- **Artifact_Registry**: The YAML file `.domainization/artifact_registry.yaml` containing metadata for all 132 registered artifacts
- **Domain_Registry**: The YAML file `.domainization/domain_registry.yaml` defining 12 canonical domains with authority boundaries
- **Mutation_Audit_Ledger**: A structured, append-only log of governance-relevant changes to the Artifact_Registry and related governance state
- **Canonical_Boundary**: The classification system in `governance/canonical_boundary.py` that distinguishes canonical from transient artifacts
- **Chain_Model**: The 4-layer authority chain SIGNALS(L1)->SEMANTICS(L2)->REASONING(L3)->REPORT(L4)
- **Property_Test**: A Hypothesis-based test that verifies a governance contract holds for all generated inputs
- **Observer**: A validation module within the Governance_Runtime that detects a specific category of violations
- **Warning_Baseline**: A persisted set of known, accepted warnings that are expected on each run
- **Gate_Result**: A structured output object from a Deployment_Gate containing pass/fail status, severity, duration, and details
- **Read_Only_State**: A lifecycle state (e.g., `archived`, `superseded`, `deprecated`) where artifact content is frozen and only metadata changes are permitted
- **Regenerable_State**: A lifecycle state where automated engine runs may overwrite artifact content but human edits are not permitted
- **Severity_Taxonomy**: The strictly ordered IntEnum in `runtime/severity_taxonomy.py` (INFO < WARNING < DEGRADED < CRITICAL < CANONICAL_BREAK < DETERMINISTIC_FAILURE)
- **Runtime_State_Model**: The StrEnum-based state model in `runtime/runtime_state_model.py` with orthogonal integrity dimensions
- **Time_Budget**: A maximum execution duration allocated to a Deployment_Gate, after which the gate reports timeout rather than blocking indefinitely
- **Fail_Mode**: The behavior classification of a governance component when it cannot operate normally; one of `fail_open` (skip governance, continue), `fail_soft` (log degradation, continue), or `fail_closed` (block until resolved)
- **Governance_Recursion**: A condition where governance enforcement triggers additional governance enforcement on the same artifact, creating potential infinite loops
- **Cold_Start**: The initial state of the governance system when no prior history, ledger, or baseline exists (fresh clone, first run)
- **Governance_Meta**: Internal governance artifacts (ledger entries, gate results, baselines) that are exempt from full governance enforcement but subject to integrity checks
- **Actor_Type**: A formal classification of the entity performing a mutation; one of SYSTEM, CI, USER, ENGINE, MIGRATION, RUNTIME, HOT_RELOAD
- **Governance_Policy_Version**: A content hash of combined governance configuration files that identifies which rules were active at a given point in time
- **Enforcement_Deadlock**: A state where governance blocks a mutation that is required to resolve the governance violation causing the block
- **Emergency_Override**: A governed escape mechanism that permits a blocked mutation with mandatory audit logging, limited to USER and MIGRATION actors
- **Runtime_Integrity_Hash**: A SHA-256 fingerprint computed from governance and runtime files, used to detect drift between CI validation and runtime execution
- **Governance_Overhead_Budget**: The maximum percentage of pipeline execution time (15%) that governance operations may consume
- **Shadow_Authority**: An undeclared mutation path where a module writes to an artifact without being listed in that artifact's `allowed_writers` field
- **Governance_State_Provenance**: A tag indicating the source and reliability of the current governance state; one of `authoritative`, `cached`, `fallback_derived`, `bootstrap_derived`, `partially_degraded`, `indeterminate`
- **Bounded_Degradation**: The principle that fail-soft governance degradation must be time-limited and escalate to alerts if not resolved within defined thresholds

## Requirements

### Requirement 1: CI Full Test Suite Execution

**User Story:** As a governance maintainer, I want CI to execute all property-based tests on every push and PR, so that governance contracts are continuously verified and regressions are detected before merge.

#### Acceptance Criteria

1. WHEN a push or pull request event occurs, THE CI_Pipeline SHALL execute the full pytest suite including all Property_Test files in the `tests/` directory
2. WHEN any Property_Test fails during CI execution, THE CI_Pipeline SHALL report the failure and block the merge
3. THE CI_Pipeline SHALL execute a minimum of 27 Property_Test files on every run
4. WHEN the pytest suite completes, THE CI_Pipeline SHALL produce a structured summary containing total tests, passed count, failed count, and execution duration

### Requirement 2: CI All-Directory Syntax Validation

**User Story:** As a developer, I want CI to validate Python syntax across all source directories, so that syntax errors in runtime, governance, or domainization modules are caught before merge.

#### Acceptance Criteria

1. WHEN a push or pull request event occurs, THE CI_Pipeline SHALL validate Python syntax for the `engines/`, `runtime/`, `governance/`, `.domainization/src/`, and `tests/` directories
2. WHEN any Python file fails syntax validation, THE CI_Pipeline SHALL report the failing file path and block the merge
3. THE CI_Pipeline SHALL use `python -m compileall` with quiet mode for each validated directory

### Requirement 3: CI Governance YAML Validation

**User Story:** As a governance maintainer, I want CI to validate all governance YAML files parse correctly, so that malformed configuration does not reach the main branch.

#### Acceptance Criteria

1. WHEN a push or pull request event occurs, THE CI_Pipeline SHALL validate that `config.yaml`, `domain_registry.yaml`, `artifact_registry.yaml`, and `lifecycle_state_machine.yaml` in `.domainization/` parse without errors
2. WHEN any governance YAML file fails to parse, THE CI_Pipeline SHALL report the file name and parse error, and block the merge
3. THE CI_Pipeline SHALL validate YAML structure beyond parse success by checking that required top-level keys exist in each file

### Requirement 4: CI All-Engine Import Validation

**User Story:** As a developer, I want CI to validate that all engine modules are importable, so that broken imports in any engine are caught before merge.

#### Acceptance Criteria

1. WHEN a push or pull request event occurs, THE CI_Pipeline SHALL validate the importability of all Python modules in the `engines/` directory
2. WHEN any engine module fails to import, THE CI_Pipeline SHALL report the module name and import error, and block the merge
3. THE CI_Pipeline SHALL validate imports for all engines including allocation, report, regime, scoring, priority, scenario, decision, quality, delta, morning_briefing, visual, and semantic engines

### Requirement 5: Deployment Gate Framework

**User Story:** As a governance maintainer, I want deployment gates to be independently configurable with blocking or warning behavior per enforcement mode, so that governance checks can be gradually activated without all-or-nothing risk.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL support independently configurable Deployment_Gate instances, each with its own blocking behavior per Enforcement_Mode
2. WHILE Enforcement_Mode is `observability`, THE Governance_Runtime SHALL execute all Deployment_Gate checks but report results as warnings without blocking
3. WHILE Enforcement_Mode is `soft`, THE Governance_Runtime SHALL block on gates configured as `blocking_in_soft` and warn on all others
4. WHILE Enforcement_Mode is `hard`, THE Governance_Runtime SHALL block on all gates configured as `blocking_in_hard` or `blocking_in_soft`
5. WHEN a Deployment_Gate completes, THE Governance_Runtime SHALL produce a Gate_Result containing gate name, pass/fail status, enforcement action taken, execution duration, and structured details
6. FOR ALL valid Deployment_Gate configurations, serializing then deserializing a Gate_Result SHALL produce an equivalent object (round-trip property)

### Requirement 6: Deployment Gate Time Budgets

**User Story:** As a developer, I want each deployment gate to complete within a defined time budget, so that governance checks do not cause unbounded CI execution times.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL assign a Time_Budget to each Deployment_Gate
2. WHEN a Deployment_Gate exceeds its Time_Budget, THE Governance_Runtime SHALL terminate the gate execution and report a timeout result
3. IF a Deployment_Gate times out, THEN THE Governance_Runtime SHALL record the timeout in the Gate_Result with the allocated and elapsed durations
4. THE CI_Pipeline SHALL complete all Deployment_Gate executions within a total budget of 120 seconds

### Requirement 7: Enforcement Mode Configuration and Transition

**User Story:** As a governance maintainer, I want enforcement mode transitions to be config-driven and auditable, so that the system can progress from observability to soft to hard enforcement without code changes.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL read Enforcement_Mode from `.domainization/config.yaml` at startup and respect it for all governance decisions
2. THE Governance_Runtime SHALL support three Enforcement_Mode values: `observability`, `soft`, and `hard`
3. WHEN Enforcement_Mode is changed in configuration, THE Governance_Runtime SHALL record the transition in the Mutation_Audit_Ledger with timestamp, previous mode, new mode, and actor
4. THE Governance_Runtime SHALL define explicit, documented criteria for each mode transition (observability to soft, soft to hard)
5. WHILE Enforcement_Mode is `observability`, THE Governance_Runtime SHALL execute all governance checks but produce warnings only, never blocking commits or pipeline execution
6. FOR ALL Enforcement_Mode values, parsing then serializing the mode SHALL produce the original string value (round-trip property)

### Requirement 8: Lifecycle Transition Enforcement

**User Story:** As a governance maintainer, I want invalid lifecycle transitions to be prevented in soft and hard enforcement modes, so that artifacts cannot move to states not permitted by the Lifecycle_State_Machine.

#### Acceptance Criteria

1. WHEN a lifecycle state transition is requested, THE Governance_Runtime SHALL validate the transition against the Lifecycle_State_Machine before persisting the change
2. WHILE Enforcement_Mode is `soft`, IF an invalid lifecycle transition is attempted, THEN THE Governance_Runtime SHALL reject the transition and log a structured warning with the artifact identifier, attempted from-state, attempted to-state, and valid transitions from the current state
3. WHILE Enforcement_Mode is `hard`, IF an invalid lifecycle transition is attempted, THEN THE Governance_Runtime SHALL reject the transition and raise an enforcement error
4. WHILE Enforcement_Mode is `observability`, IF an invalid lifecycle transition is attempted, THEN THE Governance_Runtime SHALL log a warning but permit the transition
5. FOR ALL artifact types defined in the Lifecycle_State_Machine, THE Governance_Runtime SHALL enforce that only transitions explicitly listed in the `transitions` array are valid

### Requirement 9: Read-Only State Protection

**User Story:** As a governance maintainer, I want artifacts in read-only lifecycle states to be protected from content modification, so that archived and superseded artifacts remain immutable.

#### Acceptance Criteria

1. WHILE an artifact is in a Read_Only_State AND Enforcement_Mode is `soft` or `hard`, THE Governance_Runtime SHALL reject content modifications to that artifact
2. WHILE an artifact is in a Read_Only_State AND Enforcement_Mode is `observability`, THE Governance_Runtime SHALL log a warning when content modification is attempted but permit the modification
3. THE Governance_Runtime SHALL treat the following states as Read_Only_State: `archived`, `superseded`, and `deprecated` (as defined per artifact type in the Lifecycle_State_Machine)
4. WHILE an artifact is in a Read_Only_State, THE Governance_Runtime SHALL permit metadata-only changes (e.g., `last_modified`, `governance_notes`)

### Requirement 10: Regenerable State Gate

**User Story:** As a governance maintainer, I want regenerable state checks before engine overwrites, so that engines do not overwrite artifacts that are not in a regenerable state.

#### Acceptance Criteria

1. WHEN an engine attempts to overwrite an artifact, THE Governance_Runtime SHALL verify the artifact is in a Regenerable_State before permitting the write
2. IF an engine attempts to overwrite an artifact NOT in a Regenerable_State AND Enforcement_Mode is `soft` or `hard`, THEN THE Governance_Runtime SHALL reject the overwrite and log the violation
3. IF an engine attempts to overwrite an artifact NOT in a Regenerable_State AND Enforcement_Mode is `observability`, THEN THE Governance_Runtime SHALL log a warning but permit the overwrite
4. THE Governance_Runtime SHALL recognize `regenerable_states` as defined per artifact type in the Lifecycle_State_Machine (currently defined for REPORT_OUT, DATA_OUT, and SNAPSHOT types)

### Requirement 11: Lifecycle Transition Audit Logging

**User Story:** As a governance auditor, I want all lifecycle state transitions to be logged with structured metadata, so that the history of artifact state changes is traceable.

#### Acceptance Criteria

1. WHEN a lifecycle state transition occurs (valid or invalid), THE Governance_Runtime SHALL record a structured log entry containing artifact identifier, artifact type, from-state, to-state, timestamp, actor, and validity status
2. THE Governance_Runtime SHALL persist transition audit logs to the Mutation_Audit_Ledger
3. THE Governance_Runtime SHALL retain transition audit logs across multiple executions (logs are not ephemeral)
4. FOR ALL transition audit log entries, serializing then deserializing the entry SHALL produce an equivalent object (round-trip property)

### Requirement 12: Mutation Audit Ledger — Registry Change Records

**User Story:** As a governance auditor, I want structured change records for every artifact registry modification, so that registry changes are traceable beyond git diff.

#### Acceptance Criteria

1. WHEN an artifact is added to the Artifact_Registry, THE Mutation_Audit_Ledger SHALL record a structured entry containing artifact identifier, artifact type, initial state, primary domain, timestamp, and actor
2. WHEN an artifact field is modified in the Artifact_Registry, THE Mutation_Audit_Ledger SHALL record a structured entry containing artifact identifier, field name, previous value, new value, timestamp, and actor
3. WHEN an artifact is removed from the Artifact_Registry, THE Mutation_Audit_Ledger SHALL record a structured entry containing artifact identifier, final state, removal reason, timestamp, and actor
4. THE Mutation_Audit_Ledger SHALL persist all records to a structured file format (YAML or JSON) in the `.domainization/` directory
5. FOR ALL Mutation_Audit_Ledger entries, serializing then deserializing the entry SHALL produce an equivalent object (round-trip property)

### Requirement 13: Mutation Audit Ledger — Governance Event Persistence

**User Story:** As a governance auditor, I want governance events to persist beyond a single pipeline execution, so that historical governance decisions are available for audit.

#### Acceptance Criteria

1. WHEN a governance event occurs (enforcement mode change, policy reload, gate result, sunset evaluation), THE Mutation_Audit_Ledger SHALL persist a structured record
2. THE Mutation_Audit_Ledger SHALL store governance events in an append-only format that preserves chronological ordering
3. THE Mutation_Audit_Ledger SHALL include event type, timestamp, severity, source component, and event-specific details in each record
4. THE Mutation_Audit_Ledger SHALL support querying events by time range and event type
5. IF the Mutation_Audit_Ledger file becomes corrupted, THEN THE Governance_Runtime SHALL create a new ledger file and log the corruption event without blocking pipeline execution

### Requirement 14: Mutation Audit Ledger — Policy Change Auditing

**User Story:** As a governance auditor, I want policy changes (confidence policy reloads, enforcement mode changes) to be audited, so that runtime behavior changes are traceable.

#### Acceptance Criteria

1. WHEN the confidence policy is reloaded during pipeline execution, THE Mutation_Audit_Ledger SHALL record the reload event with timestamp, previous policy hash, new policy hash, and triggering context
2. WHEN Enforcement_Mode is changed, THE Mutation_Audit_Ledger SHALL record the change with timestamp, previous mode, new mode, and justification field
3. THE Mutation_Audit_Ledger SHALL distinguish between automated policy changes (hot-reload) and manual policy changes (config edit)

### Requirement 15: Mutation Audit Ledger — Sunset Transition Recording

**User Story:** As a governance auditor, I want sunset phase transitions to be recorded, so that the deprecation lifecycle of artifacts is traceable.

#### Acceptance Criteria

1. WHEN an artifact transitions between sunset phases (active, deprecated, sunset_pending, archived), THE Mutation_Audit_Ledger SHALL record the phase change with artifact identifier, previous phase, new phase, downstream dependency count, and timestamp
2. WHEN a sunset date is reached for an artifact, THE Mutation_Audit_Ledger SHALL record the event with artifact identifier, sunset date, current dependency count, and action taken (continued generation or halted)
3. THE Mutation_Audit_Ledger SHALL record whether sunset transitions were evaluated automatically or triggered manually

### Requirement 16: Boundary Enforcement — Allowed Writers

**User Story:** As a governance maintainer, I want `allowed_writers` to be enforced at write time in soft and hard modes, so that only authorized domains can modify artifacts they have permission to write.

#### Acceptance Criteria

1. WHEN a write operation targets an artifact AND Enforcement_Mode is `soft` or `hard`, THE Governance_Runtime SHALL check the writing domain against the artifact's `allowed_writers` field in the Artifact_Registry
2. IF the writing domain is not in the artifact's `allowed_writers` list AND Enforcement_Mode is `soft`, THEN THE Governance_Runtime SHALL reject the write and log a structured boundary violation
3. IF the writing domain is not in the artifact's `allowed_writers` list AND Enforcement_Mode is `hard`, THEN THE Governance_Runtime SHALL reject the write and raise a boundary enforcement error
4. WHILE Enforcement_Mode is `observability`, THE Governance_Runtime SHALL log boundary violations as warnings but permit all writes
5. WHEN `allowed_writers` contains the value `ALL`, THE Governance_Runtime SHALL permit writes from any domain

### Requirement 17: Boundary Enforcement — Cannot Own

**User Story:** As a governance maintainer, I want `cannot_own` constraints to be enforced at domain assignment time, so that domains cannot own artifact types they are forbidden from owning.

#### Acceptance Criteria

1. WHEN a domain assignment is requested for an artifact AND Enforcement_Mode is `soft` or `hard`, THE Governance_Runtime SHALL check the artifact type against the target domain's `cannot_own` list in the Domain_Registry
2. IF the artifact type is in the target domain's `cannot_own` list AND Enforcement_Mode is `soft` or `hard`, THEN THE Governance_Runtime SHALL reject the assignment and log a structured boundary violation
3. WHILE Enforcement_Mode is `observability`, THE Governance_Runtime SHALL log `cannot_own` violations as warnings but permit the assignment
4. FOR ALL domains in the Domain_Registry, THE Governance_Runtime SHALL enforce that `cannot_own` and `allowed_artifact_types` constraints are consistent (an artifact type cannot appear in both lists for the same domain)

### Requirement 18: Canonical Boundary Runtime Discovery

**User Story:** As a governance maintainer, I want the canonical boundary classification to support runtime discovery from the Artifact_Registry, so that new artifacts are automatically classified without requiring hardcoded set updates.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL derive canonical/transient classification from Artifact_Registry metadata rather than relying solely on hardcoded frozensets
2. WHEN a new artifact is registered that is not in the hardcoded canonical or transient sets, THE Governance_Runtime SHALL classify it based on its artifact type and lifecycle state
3. THE Governance_Runtime SHALL maintain backward compatibility with the existing `CANONICAL_ARTIFACTS` and `TRANSIENT_ARTIFACTS` frozensets as a fallback
4. THE Governance_Runtime SHALL log a warning when an artifact requires fallback classification (indicating the registry-based classification could not determine status)

### Requirement 19: Cross-Domain Interaction Detection

**User Story:** As a governance maintainer, I want cross-domain interactions to be detected and logged, so that unauthorized cross-domain data flows are visible.

#### Acceptance Criteria

1. WHEN a module in one domain reads or writes an artifact owned by a different domain, THE Governance_Runtime SHALL detect and log the cross-domain interaction
2. THE Governance_Runtime SHALL record cross-domain interactions with source domain, target domain, artifact identifier, interaction type (read/write), and timestamp
3. WHILE Enforcement_Mode is `observability` or `soft`, THE Governance_Runtime SHALL log cross-domain interactions as informational events without blocking
4. WHILE Enforcement_Mode is `hard`, IF a cross-domain write violates `allowed_writers`, THEN THE Governance_Runtime SHALL block the interaction

### Requirement 20: Warning Suppression for Known Warnings

**User Story:** As a developer, I want known and accepted warnings to be suppressible via a baseline file, so that repeated expected warnings do not create noise.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL support a Warning_Baseline file that lists known, accepted warnings by warning code and artifact identifier
2. WHEN a warning matches an entry in the Warning_Baseline, THE Governance_Runtime SHALL suppress the warning from standard output
3. THE Governance_Runtime SHALL count suppressed warnings separately and report the suppression count in the governance summary
4. WHEN a warning in the Warning_Baseline is no longer emitted by the system, THE Governance_Runtime SHALL flag the stale baseline entry for removal

### Requirement 21: New Warning Escalation

**User Story:** As a governance maintainer, I want new or unexpected warnings to be escalated with higher visibility, so that novel governance violations are not lost in noise.

#### Acceptance Criteria

1. WHEN a warning is emitted that does NOT match any entry in the Warning_Baseline, THE Governance_Runtime SHALL classify it as a new warning and escalate its visibility
2. THE Governance_Runtime SHALL present new warnings with distinct formatting (prefix, severity marker, or section header) separate from suppressed known warnings
3. WHILE Enforcement_Mode is `hard`, IF a new warning has severity CRITICAL or above in the Severity_Taxonomy, THEN THE Governance_Runtime SHALL treat the new warning as a blocking violation
4. THE Governance_Runtime SHALL report the count of new warnings separately from known warnings in the governance summary

### Requirement 22: Warning Deduplication

**User Story:** As a developer, I want duplicate warnings within a single execution to be deduplicated, so that warning volume is bounded and each unique violation is reported once.

#### Acceptance Criteria

1. WHEN the same warning (identical code, artifact, and message) is emitted multiple times within a single pipeline execution, THE Governance_Runtime SHALL report it once with an occurrence count
2. THE Governance_Runtime SHALL deduplicate warnings based on warning code and artifact identifier combination
3. WHEN the governance summary is produced, THE Governance_Runtime SHALL report total unique warnings and total occurrences as separate counts
4. THE Governance_Runtime SHALL bound warning output to a maximum of 50 unique warnings per execution, with overflow reported as a count

### Requirement 23: Warning Trend Tracking

**User Story:** As a governance maintainer, I want warning trends tracked over time, so that I can identify whether governance health is improving or degrading.

#### Acceptance Criteria

1. WHEN a pipeline execution completes, THE Governance_Runtime SHALL persist a warning summary record containing execution timestamp, total unique warnings, warnings by category, and new warning count
2. THE Governance_Runtime SHALL store warning trend data in the Mutation_Audit_Ledger
3. THE Governance_Runtime SHALL support comparison between current execution warning counts and the previous execution to detect increases
4. WHEN warning count increases by more than 20% compared to the previous execution, THE Governance_Runtime SHALL emit a trend alert in the governance summary

### Requirement 24: Severity-to-Enforcement-Mode Mapping

**User Story:** As a governance maintainer, I want warning severity levels to map to enforcement mode behavior, so that the existing `blocks_pipeline_hard_mode` field in the Severity_Taxonomy is actually consumed at runtime.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL read the `blocks_pipeline_hard_mode` attribute from each severity level in the Severity_Taxonomy
2. WHILE Enforcement_Mode is `hard`, WHEN a governance event has a severity where `blocks_pipeline_hard_mode` is true, THE Governance_Runtime SHALL treat the event as a blocking violation
3. WHILE Enforcement_Mode is `soft`, THE Governance_Runtime SHALL treat severity levels CRITICAL and above as blocking violations
4. WHILE Enforcement_Mode is `observability`, THE Governance_Runtime SHALL treat all severity levels as non-blocking regardless of the `blocks_pipeline_hard_mode` attribute
5. FOR ALL severity levels in the Severity_Taxonomy, THE Governance_Runtime SHALL preserve the strict ordering (INFO < WARNING < DEGRADED < CRITICAL < CANONICAL_BREAK < DETERMINISTIC_FAILURE)

### Requirement 25: Invariant Preservation

**User Story:** As a system architect, I want all existing governance invariants to be preserved by the enforcement system, so that hardening does not break foundational guarantees.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL preserve INV-1: every registered artifact has exactly one primary_domain
2. THE Governance_Runtime SHALL preserve INV-2: every artifact type has a defined lifecycle state machine
3. THE Governance_Runtime SHALL preserve INV-3: the Chain_Model is SIGNALS(L1)->SEMANTICS(L2)->REASONING(L3)->REPORT(L4)
4. THE Governance_Runtime SHALL preserve INV-4: severity levels are strictly ordered (INFO < WARNING < DEGRADED < CRITICAL < CANONICAL_BREAK < DETERMINISTIC_FAILURE)
5. THE Governance_Runtime SHALL preserve INV-5: runtime states belong to orthogonal integrity dimensions
6. THE Governance_Runtime SHALL preserve INV-6: provenance truth lives in sidecar YAML, not markdown
7. THE Governance_Runtime SHALL preserve INV-7: pipeline execution completes (degraded output preferred over no output)
8. THE Governance_Runtime SHALL preserve INV-8: observability mode never blocks commits or pipeline execution
9. THE Governance_Runtime SHALL preserve INV-9: schema versions use semantic versioning (MAJOR.MINOR.PATCH)
10. THE Governance_Runtime SHALL preserve INV-10: canonical artifacts are subject to full governance; transient artifacts are exempt

### Requirement 26: Structured Gate Output Format

**User Story:** As a CI consumer, I want deployment gate results in a structured, machine-readable format, so that downstream tools can parse and act on gate outcomes.

#### Acceptance Criteria

1. WHEN a Deployment_Gate produces a Gate_Result, THE Governance_Runtime SHALL format the result as a structured object containing: gate_name, status (pass/fail/timeout/skip), enforcement_action (block/warn/info), duration_ms, details (list of findings), and timestamp
2. THE Governance_Runtime SHALL produce a combined gate summary after all gates execute, containing total gates, passed count, failed count, blocked count, and total duration
3. THE Governance_Runtime SHALL output Gate_Result objects in both human-readable (terminal) and machine-readable (JSON) formats
4. FOR ALL Gate_Result objects, THE Gate_Result_Serializer SHALL produce valid JSON that round-trips through parse and serialize without data loss

### Requirement 27: Deployment Gate Structured Output Persistence

**User Story:** As a governance auditor, I want gate results persisted for historical comparison, so that deployment integrity trends are visible over time.

#### Acceptance Criteria

1. WHEN all Deployment_Gate checks complete in a CI run, THE CI_Pipeline SHALL persist the combined gate summary to the Mutation_Audit_Ledger
2. THE Mutation_Audit_Ledger SHALL store gate results with the git commit SHA, branch name, execution timestamp, and combined gate summary
3. THE Governance_Runtime SHALL support querying historical gate results to compute deployment integrity score trends

### Requirement 28: Property-Based Test Coverage for Governance Contracts

**User Story:** As a governance maintainer, I want property-based tests (Hypothesis) for all new governance enforcement contracts, so that enforcement logic is verified across generated input spaces.

#### Acceptance Criteria

1. THE test suite SHALL include Property_Test coverage for Enforcement_Mode parsing and serialization (round-trip)
2. THE test suite SHALL include Property_Test coverage for Gate_Result serialization and deserialization (round-trip)
3. THE test suite SHALL include Property_Test coverage for Mutation_Audit_Ledger entry serialization (round-trip)
4. THE test suite SHALL include Property_Test coverage for lifecycle transition validation (valid transitions accepted, invalid transitions rejected for all artifact types)
5. THE test suite SHALL include Property_Test coverage for boundary enforcement (allowed_writers check produces correct accept/reject for generated domain and artifact combinations)
6. THE test suite SHALL include Property_Test coverage for warning deduplication (deduplicated output contains same unique warnings as input, occurrence counts are correct)
7. THE test suite SHALL include Property_Test coverage for severity ordering preservation (enforcement decisions respect strict severity ordering)
8. THE test suite SHALL include Property_Test coverage for Warning_Baseline matching (suppression is idempotent — applying baseline twice produces same result as applying once)

### Requirement 29: Governance Fail-Mode Classification

**User Story:** As a system architect, I want every governance enforcement component explicitly classified as fail-open, fail-soft, or fail-closed, so that runtime behavior under governance degradation is deterministic and never ambiguous.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL classify every enforcement component into exactly one of three fail-modes: `fail_open` (pipeline continues, governance skipped), `fail_soft` (pipeline continues, degradation logged), or `fail_closed` (pipeline blocks until governance recovers)
2. WHEN the Mutation_Audit_Ledger is corrupt or unavailable, THE Governance_Runtime SHALL operate in `fail_soft` mode: pipeline continues, a governance degradation event is emitted, and the corruption is recorded upon recovery
3. WHEN a governance YAML file (config, registry, lifecycle, domain) fails to parse AND Enforcement_Mode is `soft` or `hard`, THE Governance_Runtime SHALL operate in `fail_closed` mode: the pipeline SHALL NOT proceed with unparseable governance truth. WHEN Enforcement_Mode is `observability`, THE Governance_Runtime SHALL operate in `fail_soft` mode using the last successfully parsed state (if cached) or skip governance entirely with a CRITICAL severity event.
4. WHEN the Boundary Enforcement system is unavailable, THE Governance_Runtime SHALL operate in `fail_soft` mode: pipeline continues with boundary checks skipped and a DEGRADED severity event emitted
5. WHEN the Warning Governance system is unavailable, THE Governance_Runtime SHALL operate in `fail_open` mode: pipeline continues without warning processing and an alert is emitted to stdout
6. WHEN a lifecycle paradox is detected (artifact in a state not defined by its type's state machine), THE Governance_Runtime SHALL operate in `fail_closed` mode in `hard` Enforcement_Mode and `fail_soft` mode in `soft` or `observability` Enforcement_Mode
7. THE Governance_Runtime SHALL persist the fail-mode classification for each component in a structured configuration file, not in source code comments

### Requirement 30: Governance Recursion Protection

**User Story:** As a system architect, I want explicit governance recursion boundaries, so that governance systems do not infinitely govern their own governance artifacts and create recursive explosion.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL define a maximum governance recursion depth of 1: governance artifacts (ledger entries, gate results, warning baselines) are subject to integrity validation but NOT to lifecycle enforcement, mutation auditing, or boundary enforcement
2. THE Governance_Runtime SHALL classify governance-internal artifacts (Mutation_Audit_Ledger entries, Gate_Result records, Warning_Baseline file, governance event logs) as `governance_meta` — exempt from full governance enforcement but subject to structural integrity checks
3. WHEN a governance operation would trigger another governance operation on the same artifact, THE Governance_Runtime SHALL detect the recursion and terminate the chain with a structured log entry
4. THE Governance_Runtime SHALL NOT apply lifecycle state machines to governance-internal artifacts (ledger files, baseline files, gate result files)
5. THE Governance_Runtime SHALL NOT require registration enforcement for governance-internal artifacts that are auto-generated during pipeline execution
6. FOR ALL governance operations, THE Governance_Runtime SHALL complete without triggering more than one level of nested governance evaluation (recursion depth property)

### Requirement 31: Governance Cold-Start Mode

**User Story:** As a developer, I want the governance system to support cold-start initialization, so that fresh clones, empty registries, and first-time setups do not fail or block pipeline execution.

#### Acceptance Criteria

1. WHEN the Mutation_Audit_Ledger does not exist, THE Governance_Runtime SHALL create an empty ledger file with a bootstrap entry recording the initialization timestamp and actor
2. WHEN the Warning_Baseline file does not exist, THE Governance_Runtime SHALL operate with an empty baseline (all warnings are treated as new) without blocking
3. WHEN the Artifact_Registry is empty or missing, THE Governance_Runtime SHALL emit a CRITICAL governance event and operate in `observability` mode regardless of configured Enforcement_Mode
4. WHEN no historical gate results exist, THE Governance_Runtime SHALL skip trend comparison and report "no baseline available" in the governance summary
5. THE Governance_Runtime SHALL NOT require any pre-existing governance history to execute successfully on first run
6. WHEN cold-start mode is active, THE Governance_Runtime SHALL emit a structured `COLD_START` event containing initialization timestamp, missing components list, and fallback behavior applied
7. WHEN cold-start mode is detected (no Mutation_Audit_Ledger AND no Warning_Baseline AND no historical gate results), THE Governance_Runtime SHALL apply cold-start rules with precedence over fail-mode classifications defined in Requirement 29. Cold-start mode forces `observability` behavior regardless of configured Enforcement_Mode or component fail-mode classification.
8. Cold-start mode SHALL be temporary and explicitly bounded. THE Governance_Runtime SHALL track cold-start duration and require transition into normal governance mode after baseline initialization completes (first successful pipeline run that produces a ledger entry, warning baseline, and gate result).
9. IF cold-start mode persists beyond 3 consecutive pipeline executions without transitioning to normal mode, THE Governance_Runtime SHALL emit a CRITICAL severity event indicating governance bootstrap failure requiring manual intervention.

### Requirement 32: Partial Governance Tolerance

**User Story:** As a system architect, I want the governance system to support partial degradation states, so that individual gate timeouts or module unavailability do not invalidate the entire governance evaluation.

#### Acceptance Criteria

1. WHEN one or more Deployment_Gates timeout or fail while others pass, THE Governance_Runtime SHALL produce a partial governance result containing the individual gate outcomes and an aggregate state of `partial`
2. THE Governance_Runtime SHALL define aggregate governance states: `healthy` (all gates pass), `partial` (at least one gate timeout or unavailable but more than 50% of gates pass), `degraded` (50% or fewer gates pass), `collapsed` (zero gates pass or governance system itself is unavailable)
3. WHEN aggregate governance state is `partial`, THE Governance_Runtime SHALL report which specific gates are unavailable and continue pipeline execution with available governance results
4. THE Governance_Runtime SHALL NOT treat a single gate timeout as equivalent to total governance failure
5. WHEN aggregate governance state is `collapsed`, THE Governance_Runtime SHALL emit a CRITICAL severity event and fall back to the fail-mode classification of each component (Requirement 29)
6. FOR ALL combinations of gate pass/fail/timeout states, THE aggregate governance state SHALL be deterministically computable from the individual gate outcomes (aggregation property)

### Requirement 33: Mutation Actor Identity Model

**User Story:** As a governance auditor, I want mutation actors to be formally typed, so that audit ledger entries clearly identify who or what performed each change.

#### Acceptance Criteria

1. THE Mutation_Audit_Ledger SHALL record actor identity using a typed actor model with the following actor types: `SYSTEM`, `CI`, `USER`, `ENGINE`, `MIGRATION`, `RUNTIME`, `HOT_RELOAD`
2. WHEN a pipeline engine produces an artifact, THE Mutation_Audit_Ledger SHALL record the actor as type `ENGINE` with the engine identifier
3. WHEN CI executes a governance check, THE Mutation_Audit_Ledger SHALL record the actor as type `CI` with the workflow run identifier
4. WHEN a confidence policy is hot-reloaded during execution, THE Mutation_Audit_Ledger SHALL record the actor as type `HOT_RELOAD` with the triggering context
5. WHEN a human modifies the Artifact_Registry directly, THE Mutation_Audit_Ledger SHALL record the actor as type `USER` with identity resolved in the following priority order: (1) git author from commit context if available, (2) `$USER` environment variable if available, (3) `unknown_user` as explicit fallback. The fallback indicator SHALL be flagged in the actor record to enable later identity resolution.
6. FOR ALL actor types, THE actor identity SHALL be serializable to a structured format containing actor_type, actor_id, and optional context fields

### Requirement 34: Governance Policy Versioning

**User Story:** As a governance auditor, I want all governance decisions to include the governance policy version under which they were made, so that historical decisions can be evaluated against the rules that were active at the time.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL maintain a `governance_policy_version` identifier that changes whenever governance rules, severity mappings, gate configurations, or enforcement mode definitions change
2. WHEN a Gate_Result is produced, THE Gate_Result SHALL include the `governance_policy_version` that was active during evaluation
3. WHEN a Mutation_Audit_Ledger entry is recorded, THE entry SHALL include the `governance_policy_version` active at the time of the event
4. WHEN a lifecycle enforcement decision is made (accept or reject), THE decision record SHALL include the `governance_policy_version`
5. THE Governance_Runtime SHALL compute `governance_policy_version` as a content hash of the combined governance configuration files (config.yaml, lifecycle_state_machine.yaml, domain_registry.yaml, confidence_policy.yaml)
6. WHEN `governance_policy_version` changes between consecutive pipeline runs, THE Governance_Runtime SHALL emit a structured `POLICY_VERSION_CHANGE` event with previous and new version hashes

### Requirement 35: Enforcement Deadlock Prevention and Recovery

**User Story:** As a system architect, I want governance deadlock prevention, so that the system cannot enter a state where governance blocks a mutation that is required to fix a governance violation.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL detect enforcement deadlock conditions using the following heuristic: a deadlock exists when (a) a governance enforcement action rejects a mutation targeting artifact A, AND (b) the rejection reason references a violation on the same artifact A that can only be resolved by the rejected mutation. Detection SHALL be based on artifact identifier matching between the rejection target and the violation source within the same enforcement cycle.
2. The initial heuristic SHALL use same-artifact matching as the minimum deterministic baseline. THE Governance_Runtime MAY later extend deadlock detection to declared dependency chains, lifecycle-linked artifacts, and canonical-boundary relationships without changing baseline same-artifact behavior.
2. WHEN an enforcement deadlock is detected, THE Governance_Runtime SHALL provide an emergency override mechanism that permits the blocked mutation with mandatory audit logging
3. WHEN an emergency override is used, THE Mutation_Audit_Ledger SHALL record the override with: artifact identifier, blocked violation, override justification, actor, timestamp, and `EMERGENCY_OVERRIDE` flag
4. THE Governance_Runtime SHALL limit emergency overrides to actors of type `USER` or `MIGRATION` — automated actors (`ENGINE`, `RUNTIME`, `HOT_RELOAD`) SHALL NOT invoke emergency overrides
5. WHEN an emergency override is used, THE Governance_Runtime SHALL emit a CRITICAL severity governance event visible in the next health report
6. THE Governance_Runtime SHALL track emergency override frequency and emit a trend alert if overrides exceed 3 within a 7-day window

### Requirement 36: Runtime/CI Consistency Hashing

**User Story:** As a deployment engineer, I want a runtime-integrity fingerprint that CI can produce and runtime can verify, so that deployment drift between CI validation and runtime execution is detectable.

#### Acceptance Criteria

1. WHEN CI completes all Deployment_Gate checks, THE CI_Pipeline SHALL compute a `runtime_integrity_hash` from the combined content of: all governance YAML files, all runtime Python modules, all governance Python modules, and the confidence policy YAML
2. THE CI_Pipeline SHALL persist the `runtime_integrity_hash` in the Gate_Result summary alongside the git commit SHA
3. WHEN the Pipeline_Orchestrator starts execution, THE Pipeline_Orchestrator SHALL compute the same `runtime_integrity_hash` from the local file system
4. IF the runtime-computed hash differs from the last CI-computed hash (indicating files changed after CI validation), THE Pipeline_Orchestrator SHALL emit a DEGRADED severity event with the mismatched hash values
5. THE `runtime_integrity_hash` SHALL be computed using SHA-256 over deterministically sorted file contents
6. FOR ALL identical file system states, THE `runtime_integrity_hash` computation SHALL produce identical results (determinism property)

### Requirement 37: Transient Artifact Promotion Governance

**User Story:** As a governance maintainer, I want transient artifacts to require explicit promotion before canonical persistence, so that governance boundaries are not silently crossed.

#### Acceptance Criteria

1. WHEN a transient artifact is persisted to disk or passed to a downstream engine, THE Governance_Runtime SHALL detect the boundary crossing and require explicit promotion
2. WHILE Enforcement_Mode is `soft` or `hard`, IF a transient artifact crosses the canonical boundary without explicit promotion, THEN THE Governance_Runtime SHALL reject the persistence and log a boundary violation
3. WHILE Enforcement_Mode is `observability`, IF a transient artifact crosses the canonical boundary without explicit promotion, THEN THE Governance_Runtime SHALL log a warning and permit the crossing
4. THE Governance_Runtime SHALL provide an explicit `promote_to_canonical()` function that records the promotion in the Mutation_Audit_Ledger with artifact name, promotion reason, and actor
5. WHEN a transient artifact is promoted to canonical, THE Governance_Runtime SHALL verify the artifact meets canonical requirements (schema validation, provenance metadata presence) before completing promotion

### Requirement 38: Governance Performance Budget

**User Story:** As a system architect, I want bounded governance overhead relative to pipeline runtime, so that governance does not become the dominant cost of pipeline execution.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL enforce a total governance overhead budget of 15% of pipeline execution time during local pipeline execution (Pipeline_Orchestrator.execute()). This budget is independent of the CI_Pipeline gate time budget defined in Requirement 6, which applies to CI-specific Deployment_Gate execution.
2. WHEN total governance overhead exceeds the budget, THE Governance_Runtime SHALL emit a DEGRADED severity event and skip non-critical governance checks (warning deduplication, trend tracking) to stay within budget
3. THE Governance_Runtime SHALL measure and report governance overhead as a percentage of total pipeline execution time in the Gate_Result summary
4. THE Governance_Runtime SHALL prioritize governance checks in the following order when budget is constrained: (1) fail-closed checks, (2) fail-soft checks, (3) fail-open checks, (4) informational checks
5. THE CI_Pipeline SHALL report governance overhead percentage in the combined gate summary
6. FOR ALL pipeline executions, THE governance overhead SHALL be measurable and reproducible (overhead measurement property)

### Requirement 39: Anti-Ontology Proliferation Constraint

**User Story:** As a system architect, I want explicit constraints against unnecessary governance ontology expansion, so that the governance system remains minimal and does not become the product itself.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL NOT introduce new artifact types beyond the 10 defined in the Lifecycle_State_Machine without explicit CTO approval documented in the Mutation_Audit_Ledger
2. THE Governance_Runtime SHALL NOT introduce new governance dimensions (beyond the 5 integrity dimensions in the Runtime_State_Model) without explicit justification recorded in the Mutation_Audit_Ledger
3. THE Governance_Runtime SHALL NOT introduce new severity levels beyond the 6 defined in the Severity_Taxonomy
4. WHEN a new governance concept is proposed, THE Governance_Runtime SHALL require a justification entry in the Mutation_Audit_Ledger containing: concept name, necessity rationale, alternatives considered, and approval actor
5. THE Governance_Runtime SHALL track total governance concept count (artifact types + severity levels + integrity dimensions + enforcement modes + actor types) and emit a warning if the count exceeds 50

### Requirement 40: Shadow Authority Detection

**User Story:** As a governance maintainer, I want undeclared mutation authority paths to be detected at runtime, so that implicit cross-domain writes are visible and governable.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL detect when a module writes to an artifact without being listed in that artifact's `allowed_writers` field, and classify this as a shadow authority event
2. THE Governance_Runtime SHALL record shadow authority events in the Mutation_Audit_Ledger with: writing module path, target artifact identifier, declared allowed_writers, and timestamp
3. WHEN shadow authority events exceed 5 unique paths within a single pipeline execution, THE Governance_Runtime SHALL emit a CRITICAL severity event indicating systemic boundary violation
4. THE Governance_Runtime SHALL distinguish between shadow authority from registered engines (potentially legitimate but undeclared) and shadow authority from unregistered modules (likely violation)
5. WHILE Enforcement_Mode is `hard`, THE Governance_Runtime SHALL block shadow authority writes that originate from unregistered modules

### Requirement 41: Governance State Provenance Tagging

**User Story:** As a governance auditor, I want every governance state to carry explicit provenance indicating its source, so that the system always knows whether a governance state is authoritative, cached, fallback-derived, or degraded.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL explicitly tag every governance state with a provenance indicator from the following set: `authoritative` (loaded from canonical source, validated), `cached` (loaded from last-known-good cache, source unavailable), `fallback_derived` (computed from fallback logic due to component failure), `bootstrap_derived` (generated during cold-start initialization), `partially_degraded` (some components authoritative, some unavailable), `indeterminate` (provenance cannot be determined)
2. WHEN the Governance_Runtime produces a Gate_Result, THE Gate_Result SHALL include the governance state provenance tag indicating under what conditions the gate was evaluated
3. WHEN the Governance_Runtime falls back to cached registry state (per Requirement 29.3 observability mode), THE governance state provenance SHALL be tagged as `cached` with the cache timestamp
4. WHEN cold-start mode is active, THE governance state provenance SHALL be tagged as `bootstrap_derived` until normal mode is established
5. THE Governance_Runtime SHALL make governance state provenance observable in the health report and governance summary
6. WHEN governance state provenance is `indeterminate`, THE Governance_Runtime SHALL emit a DEGRADED severity event and treat all enforcement decisions as non-blocking regardless of Enforcement_Mode

### Requirement 42: Bounded Fail-Soft Degradation

**User Story:** As a system architect, I want fail-soft degradation to be time-bounded, so that the system does not remain in a degraded governance state indefinitely without alerting.

#### Acceptance Criteria

1. WHEN a governance component enters `fail_soft` mode, THE Governance_Runtime SHALL record the degradation start timestamp
2. IF a governance component remains in `fail_soft` mode for more than 5 consecutive pipeline executions, THE Governance_Runtime SHALL escalate the degradation to a CRITICAL severity event
3. IF a governance component remains in `fail_soft` mode for more than 10 consecutive pipeline executions, THE Governance_Runtime SHALL emit a `GOVERNANCE_DEGRADATION_PERSISTENT` event recommending manual intervention
4. THE Governance_Runtime SHALL track degradation duration per component and include it in the health report
5. WHEN a degraded component recovers (returns to normal operation), THE Governance_Runtime SHALL record the recovery event with degradation duration and recovery reason in the Mutation_Audit_Ledger

### Requirement 43: Governance Layer Complexity Budget

**User Story:** As a system architect, I want a bounded governance-layer complexity budget, so that the governance system does not grow into an unmanageable meta-system that nobody can understand or debug.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL maintain a governance complexity budget tracking: total governance modules (max 25), total governance configuration files (max 10), total governance state categories (max 60 combined concepts), and total governance enforcement paths (max 15)
2. WHEN the governance layer exceeds any complexity threshold, THE Governance_Runtime SHALL emit a CRITICAL severity event and require explicit CTO justification before any new governance concept is added
3. THE Governance_Runtime SHALL report current complexity metrics in the health report under a "Governance Complexity" section
4. THE Governance_Runtime SHALL reject additions of new governance modules, states, or enforcement categories that would exceed the budget without a recorded justification entry in the Mutation_Audit_Ledger
5. THE complexity budget SHALL be defined in `.domainization/config.yaml` under a `governance_complexity_budget` section, not hardcoded in source

### Requirement 44: Mutation Audit Ledger Rotation

**User Story:** As a system architect, I want the Mutation Audit Ledger to support deterministic archival rotation, so that the ledger does not grow unbounded into a single monolithic file that degrades performance.

#### Acceptance Criteria

1. THE Mutation_Audit_Ledger SHALL support deterministic archival rotation when the active ledger file exceeds 1000 entries or 500KB file size
2. WHEN rotation occurs, THE Governance_Runtime SHALL archive the current ledger file with a timestamp suffix (e.g., `mutation_audit_ledger_2026-06-01.yaml`) and create a new empty active ledger
3. THE rotation process SHALL preserve chronological integrity: archived entries remain in original order, new entries append to the new active file
4. THE rotation process SHALL preserve hash continuity: the archived file's content hash is recorded as the first entry in the new active ledger, creating a verifiable chain
5. THE Governance_Runtime SHALL support querying across archived and active ledger files transparently (query API does not expose rotation boundaries to callers)
6. THE rotation process SHALL preserve replayability: the complete governance history can be reconstructed by reading archived files in chronological order followed by the active file

### Requirement 45: Warning Baseline Decay and Revalidation

**User Story:** As a governance maintainer, I want warning baseline entries to require periodic revalidation, so that the baseline does not become a permanent warning graveyard that hides real issues.

#### Acceptance Criteria

1. THE Warning_Baseline SHALL include an `added_date` and `expires_after_days` field for each suppression entry, defaulting to 90 days if not specified
2. WHEN a baseline entry exceeds its `expires_after_days` threshold without revalidation, THE Governance_Runtime SHALL escalate the suppressed warning to visible status and emit a `BASELINE_ENTRY_EXPIRED` event
3. THE Governance_Runtime SHALL support explicit revalidation of baseline entries by updating the `added_date` to the current date with a `revalidation_reason` field
4. WHEN more than 30% of baseline entries are expired, THE Governance_Runtime SHALL emit a CRITICAL severity event indicating baseline maintenance is overdue
5. THE health report SHALL include a "Warning Baseline Health" section showing total entries, expired entries, entries expiring within 14 days, and average entry age

### Requirement 46: Scoped Policy Version Domains

**User Story:** As a governance maintainer, I want policy versioning scoped to individual governance domains, so that a minor change to one policy area does not invalidate all governance decisions system-wide.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL support scoped policy version domains: `lifecycle_policy_version`, `boundary_policy_version`, `severity_policy_version`, `warning_policy_version`, and `gate_policy_version`, each computed from the relevant subset of configuration files
2. THE global `governance_policy_version` (Requirement 34) SHALL remain as the combined hash of all scoped versions for backward compatibility
3. WHEN a Gate_Result or Ledger_Entry is produced, THE record SHALL include both the global `governance_policy_version` and the relevant scoped version(s) that influenced the decision
4. WHEN only one scoped policy version changes between runs, THE Governance_Runtime SHALL emit a `SCOPED_POLICY_CHANGE` event identifying which domain changed, without triggering a full global policy invalidation alert
5. THE scoped version computation SHALL use the same SHA-256 canonicalization as the global version (Requirement 34.5)

### Requirement 47: Temporary Authority Declarations

**User Story:** As a governance maintainer, I want explicitly scoped temporary authority declarations, so that legitimate temporary operations (migrations, hotfixes) do not trigger false shadow authority events.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL support temporary authority declarations with: target artifact pattern (glob or exact), granted domain, duration (ISO 8601 duration or explicit end timestamp), reason, and declaring actor
2. WHEN a write matches an active temporary authority declaration, THE Shadow_Authority_Detector SHALL classify the write as `authorized_temporary` rather than `shadow_authority`
3. WHEN a temporary authority declaration expires, THE Governance_Runtime SHALL automatically revoke the authority and record the expiration in the Mutation_Audit_Ledger
4. THE Governance_Runtime SHALL limit temporary authority duration to a maximum of 7 days; declarations exceeding this limit SHALL be rejected
5. THE Governance_Runtime SHALL emit a WARNING severity event when a temporary authority is declared, and a separate event when it expires or is revoked
6. ONLY actors of type `USER` or `MIGRATION` SHALL be permitted to create temporary authority declarations

### Requirement 48: Runtime Integrity Hash Canonicalization

**User Story:** As a deployment engineer, I want runtime integrity hashing to use canonicalized content, so that platform differences (line endings, encoding, whitespace) do not produce false integrity drift alerts.

#### Acceptance Criteria

1. THE `runtime_integrity_hash` computation SHALL canonicalize all file content before hashing by: normalizing line endings to LF (Unix), normalizing encoding to UTF-8, stripping trailing whitespace from each line, and ensuring files end with exactly one newline
2. FOR YAML files included in the hash, THE computation SHALL parse and re-serialize using deterministic YAML output (sorted keys, consistent formatting) before hashing, rather than hashing raw file bytes
3. FOR Python files included in the hash, THE computation SHALL hash the raw canonicalized text (LF line endings, UTF-8, stripped trailing whitespace) without parsing
4. THE canonicalization process SHALL produce identical hash results on macOS, Linux, and CI environments (Ubuntu) for the same logical file content
5. THE Governance_Runtime SHALL document the canonicalization algorithm in the `runtime_integrity_hash` module docstring

### Requirement 49: Governance Self-Disable Protection

**User Story:** As a system architect, I want governance components prohibited from weakening their own enforcement classification during active execution, so that self-weakening governance paths cannot emerge.

#### Acceptance Criteria

1. THE Governance_Runtime SHALL prohibit any governance component from modifying its own fail-mode classification, enforcement mode, or blocking behavior during active pipeline execution
2. WHEN a governance component attempts to modify its own enforcement classification during execution, THE Governance_Runtime SHALL reject the modification and emit a CRITICAL severity event with the component name and attempted change
3. Enforcement mode changes SHALL only be permitted between pipeline executions (at startup from config) or via explicit USER actor intervention recorded in the Mutation_Audit_Ledger
4. THE fail_mode_config.yaml SHALL be loaded once at governance initialization and treated as immutable for the duration of the pipeline execution
5. THE Governance_Runtime SHALL detect and reject circular self-modification patterns where component A weakens component B which weakens component A
