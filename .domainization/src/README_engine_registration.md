# Engine Registration

## Overview

This document describes the engine registration process implemented in Task 9. All Python engine files in the `engines/` and `reports/` directories have been registered in the artifact registry with complete metadata, enabling proper artifact tracking and governance within the domainization system.

## Purpose

The registration of engine artifacts serves multiple purposes:

1. **Domain Ownership** - Establishes clear ownership boundaries for each engine
2. **Artifact Tracking** - Enables the domainization system to track and validate engines
3. **Dependency Management** - Documents dependencies between engines and SSOT specifications
4. **Lifecycle Management** - Tracks the lifecycle status of each engine
5. **Access Control** - Defines which domains can write to and read from each engine
6. **Implementation Traceability** - Links engines to their SSOT specifications

## Registry Schema

Each registered engine contains metadata in the artifact registry with the following fields:

```yaml
- artifact_id: <unique_identifier>
  file_path: <relative_path>
  primary_domain: <DOMAIN_ID>
  artifact_type: ENGINE
  lifecycle_status: <STATUS>
  created_date: <YYYY-MM-DD>
  last_modified: <YYYY-MM-DD>
  owner_role: <description>
  ssot_relationship: implementation
  allowed_writers: [<DOMAIN_ID>]
  allowed_readers: [ALL]
  dependencies: [<artifact_id>, ...]
  description: <human_readable_description>
  tags: [<tag1>, <tag2>, ...]
```

### Field Descriptions

- **artifact_id**: Unique identifier derived from filename (e.g., `allocation_engine_py`)
- **file_path**: Relative path from repo root (e.g., `engines/allocation_engine.py`)
- **primary_domain**: Primary owning domain (SIGNALS, SEMANTICS, REASONING, REPORT, etc.)
- **artifact_type**: Always `ENGINE` for engine artifacts
- **lifecycle_status**: Current lifecycle state (planned, development, active, deprecated)
- **created_date**: Original creation date
- **last_modified**: Last modification date
- **owner_role**: Description of the engine's responsibility
- **ssot_relationship**: Always `implementation` (engines implement SSOT specifications)
- **allowed_writers**: List of domains permitted to modify the engine (typically only primary domain)
- **allowed_readers**: List of domains permitted to read the engine (typically `[ALL]`)
- **dependencies**: List of SSOT specification artifact IDs this engine implements
- **description**: Human-readable description of engine functionality
- **tags**: Categorization tags for filtering and organization

## Registered Engines by Domain

### Signals Domain (SIGNALS)

Engines that generate raw signals from data analysis:

- **allocation_engine.py** - Generates allocation structure signals for portfolio composition analysis
  - Dependencies: `portfolio_health_framework_md`, `signal_calculation_framework_md`
  - Tags: signals, allocation

- **regime_engine.py** - Generates market regime classification signals based on liquidity conditions
  - Dependencies: `market_regime_framework_md`, `signal_calculation_framework_md`
  - Tags: signals, regime

- **attribution_engine.py** - Generates attribution signals identifying portfolio performance drivers
  - Dependencies: `correlation_dependency_framework_md`, `signal_calculation_framework_md`
  - Tags: signals, attribution

- **scoring_engine.py** - Generates portfolio scoring signals for action prioritization
  - Dependencies: `scoring_methodology_framework_md`, `signal_calculation_framework_md`
  - Tags: signals, scoring

### Semantics Domain (SEMANTICS)

Engines that interpret raw signals into semantic states:

- **semantic_engine.py** - Interprets raw signals into semantic states with meaning and context
  - Dependencies: `semantic_signal_registry_md`, `semantic_reasoning_rules_md`
  - Tags: semantics, interpretation

### Reasoning Domain (REASONING)

Engines that generate reasoning conclusions from semantic states:

- **decision_engine.py** - Generates actionable decisions based on semantic states and priorities
  - Dependencies: `decision_governance_md`, `semantic_reasoning_rules_md`
  - Tags: reasoning, decisions

- **quality_engine.py** - Evaluates reasoning quality and confidence levels for decision validation
  - Dependencies: `decision_governance_md`, `semantic_reasoning_rules_md`
  - Tags: reasoning, quality

- **priority_engine.py** - Prioritizes actions and risks based on semantic interpretation
  - Dependencies: `decision_governance_md`, `semantic_reasoning_rules_md`
  - Tags: reasoning, priority

### Report Domain (REPORT)

Engines that generate human-readable reports from reasoning outputs:

- **report_engine.py** - Generates comprehensive portfolio manager reports from reasoning outputs
  - Dependencies: `report_reasoning_system_md`, `report_section_specification_md`
  - Tags: report, generation

- **morning_briefing_engine.py** - Generates daily morning briefing summaries for portfolio managers
  - Dependencies: `report_reasoning_system_md`, `report_section_specification_md`
  - Tags: report, briefing

- **delta_engine.py** - Detects and reports changes between consecutive portfolio reports
  - Dependencies: `report_reasoning_system_md`
  - Tags: report, delta

- **pm_report_engine.py** - Portfolio manager report generation engine (in development)
  - Location: `reports/pm_report_engine.py`
  - Dependencies: `report_reasoning_system_md`, `report_section_specification_md`
  - Lifecycle: development
  - Tags: report, pm

### Simulation Domain (SIM)

Engines that generate scenario analysis and stress testing:

- **scenario_engine.py** - Generates scenario analysis and stress testing simulations
  - Dependencies: `simulation_architecture_md`
  - Tags: simulation, scenarios

### User Domain (USER)

Engines that generate visualization data for user interfaces:

- **visual_engine.py** - Generates visualization data structures for dashboard rendering
  - Dependencies: `dashboard_philosophy_md`
  - Tags: visualization, dashboard

### Architecture Domain (ARCH)

Engines that orchestrate system execution and manage engine dependencies:

- **engine_registry.py** - Central registry defining engine dependencies and execution order
  - Dependencies: `engine_design_principles_md`, `system_architecture_md`
  - Tags: architecture, orchestration

- **engine_runner.py** - Orchestrates engine execution flow and dependency resolution
  - Dependencies: `engine_design_principles_md`, `system_architecture_md`, `engine_registry_py`
  - Tags: architecture, orchestration

## Registration Process

### Task 9 Implementation

Task 9 was divided into 4 subtasks, each handling engines for specific domains:

#### Subtask 9.1 - Signal Generation Engines
Registered all signal generation engines with SIGNALS domain ownership:
- allocation_engine.py
- regime_engine.py
- attribution_engine.py
- scoring_engine.py

#### Subtask 9.2 - Semantic and Reasoning Engines
Registered semantic interpretation and reasoning engines:
- semantic_engine.py (SEMANTICS domain)
- decision_engine.py (REASONING domain)
- quality_engine.py (REASONING domain)
- priority_engine.py (REASONING domain)

#### Subtask 9.3 - Report Engines
Registered report generation engines with REPORT domain ownership:
- report_engine.py
- morning_briefing_engine.py
- delta_engine.py
- pm_report_engine.py

#### Subtask 9.4 - Remaining Engines
Registered engines for SIM, USER, and ARCH domains:
- scenario_engine.py (SIM domain)
- visual_engine.py (USER domain)
- engine_registry.py (ARCH domain)
- engine_runner.py (ARCH domain)

### Validation

After registration, all engines were validated to ensure:

1. **Schema Compliance** - All required metadata fields are present
2. **Domain Validity** - Primary domain is a valid domain ID
3. **Artifact Type** - Artifact type is ENGINE
4. **Lifecycle Validity** - Lifecycle status is valid for ENGINE type
5. **Dependency Validity** - Referenced SSOT specifications exist
6. **Implementation Relationship** - ssot_relationship is set to "implementation"

## Usage

### Querying Registered Engines

Use the domainization CLI to query registered engines:

```bash
# List all engines
domainization list --type ENGINE

# List engines by domain
domainization list --domain SIGNALS
domainization list --domain REASONING
domainization list --domain REPORT

# Show details for a specific engine
domainization show allocation_engine_py
domainization show semantic_engine_py

# List with verbose output
domainization list --type ENGINE --verbose
```

### Updating Engine Metadata

Update metadata for registered engines:

```bash
# Update lifecycle status
domainization update allocation_engine_py --lifecycle active

# Update last modified date
domainization update semantic_engine_py --last-modified 2026-05-26

# Add dependencies
domainization update report_engine_py \
  --dependencies report_reasoning_system_md report_section_specification_md
```

### Validating Engines

Run validation observers on registered engines:

```bash
# Validate all engines
domainization validate --type ENGINE

# Validate specific engine
domainization validate --files engines/allocation_engine.py

# Run domain assignment validation
domainization validate --observer DomainAssignmentValidator

# Dry-run mode
domainization validate --dry-run
```

### Health Reporting

Generate health reports for registered engines:

```bash
# Full health report
domainization health

# Domain-specific health report
domainization health --domain SIGNALS

# Save health report to file
domainization health --output reports/engine_health.yaml

# Show only violations
domainization health --violations-only
```

## Engine Lifecycle States

### Lifecycle States for ENGINE Artifacts

- **planned**: Engine is planned but not yet implemented
- **development**: Engine is under active development
- **active**: Engine is production-ready and actively used
- **deprecated**: Engine is no longer recommended, maintained for compatibility

### Lifecycle Transitions

Valid transitions for ENGINE artifacts:

```
planned → development → active → deprecated
         ↓            ↑
         └────────────┘
         (iteration allowed)
```

### Current Status

All registered engines are in **active** lifecycle status except:
- **pm_report_engine.py**: development (actively being developed)

## Authority Chain and Domain Boundaries

### Core Reasoning Chain

Engines follow the authority chain: **SIGNALS → SEMANTICS → REASONING → REPORT**

1. **SIGNALS engines** generate raw signals from data
2. **SEMANTICS engines** interpret signals into semantic states
3. **REASONING engines** generate conclusions from semantic states
4. **REPORT engines** render reasoning into human-readable text

### Domain Boundary Rules

- **SIGNALS engines** can only write signal outputs (DATA_OUT)
- **SEMANTICS engines** can only write semantic states
- **REASONING engines** can only write reasoning objects
- **REPORT engines** can only write report text (REPORT_OUT)
- **Cross-domain reading** is allowed (engines can read outputs from previous chain stages)

### Surface Domains

Surface domains support the core reasoning chain:

- **SIM engines** (Simulation) - Generate scenario analysis
- **USER engines** (User Interface) - Generate visualization data
- **ARCH engines** (Architecture) - Orchestrate execution flow

## Dependencies and SSOT Traceability

### Dependency Patterns

All engines declare dependencies on their SSOT specifications:

```yaml
dependencies:
  - <ssot_specification_md>
  - <framework_md>
  - <other_engine_py>  # For orchestration engines
```

### Common Dependency Patterns

- **Signal Engines** → Signal calculation frameworks + domain-specific frameworks
- **Semantic Engine** → Semantic signal registry + reasoning rules
- **Reasoning Engines** → Decision governance + reasoning rules
- **Report Engines** → Report reasoning system + section specifications
- **Orchestration Engines** → System architecture + engine design principles

### Traceability

Each engine can be traced to its authoritative specifications:

```bash
# Show engine dependencies
domainization show allocation_engine_py

# Find all engines implementing a specification
domainization list --dependencies portfolio_health_framework_md
```

## Access Control

### Allowed Writers

Each engine is writable only by its primary domain:

```yaml
allowed_writers: [SIGNALS]  # Only SIGNALS domain can modify
```

### Allowed Readers

All engines are publicly readable:

```yaml
allowed_readers: [ALL]  # All domains can read
```

### Access Control Rationale

- **Single Writer**: Prevents cross-domain modifications and maintains clear ownership
- **Public Reader**: Enables downstream domains to read outputs (e.g., SEMANTICS reads SIGNALS outputs)
- **Authority Chain**: Enforces proper data flow through the reasoning chain

## Integration with Domainization System

### Registry Integration

All registered engines are tracked in the artifact registry:

- **Location**: `.domainization/artifact_registry.yaml`
- **Format**: YAML with full metadata
- **Validation**: Automatic validation on registration and updates

### Validation Observers

Multiple observers validate registered engines:

1. **RegistrationValidator**: Ensures all engines are registered
2. **DomainAssignmentValidator**: Validates domain ownership
3. **LifecycleValidator**: Validates lifecycle transitions
4. **BoundaryAwarenessValidator**: Checks domain boundaries and authority chain
5. **SSOTConsistencyValidator**: Validates SSOT dependencies

### Health Reporting

Health reports include engine metrics:

- **Domain Coverage**: Engines per domain
- **Lifecycle Distribution**: Engines by lifecycle state
- **Dependency Health**: Broken or missing dependencies
- **Authority Chain**: Proper flow through reasoning chain
- **Violations**: Any governance violations

## Best Practices

### When Creating New Engines

1. **Choose the Right Domain**: Assign to the domain matching the engine's output type
2. **Declare Dependencies**: Reference all SSOT specifications the engine implements
3. **Set Implementation Relationship**: Always use `ssot_relationship: implementation`
4. **Use Development Status**: Start with `lifecycle_status: development`
5. **Add Descriptive Tags**: Use tags for categorization and filtering
6. **Write Clear Description**: Explain what the engine does and what it produces

### When Updating Engines

1. **Update last_modified**: Always update the modification date
2. **Maintain Dependencies**: Keep dependency list current
3. **Respect Lifecycle**: Follow valid lifecycle transitions
4. **Validate Changes**: Run validation after updates
5. **Update Description**: Keep description accurate

### When Deprecating Engines

1. **Transition Lifecycle**: Move to `deprecated` state
2. **Document Replacement**: Reference the replacement engine
3. **Update Dependencies**: Update engines that depend on it
4. **Maintain Temporarily**: Keep available during transition period
5. **Remove Eventually**: Remove when no longer needed

## Troubleshooting

### Engine Not Registered

If an engine is not showing up in queries:

```bash
# Check if file exists
ls -la engines/your_engine.py

# Check registry
grep "your_engine" .domainization/artifact_registry.yaml

# Manually register if needed
domainization register your_engine_py engines/your_engine.py DOMAIN ENGINE
```

### Invalid Domain Assignment

If validation reports invalid domain:

```bash
# Check valid domains for ENGINE type
domainization config show

# Update to valid domain
domainization update your_engine_py --domain VALID_DOMAIN
```

### Broken Dependencies

If health report shows broken dependencies:

```bash
# Check dependencies
domainization show your_engine_py

# Update dependencies to valid artifact IDs
domainization update your_engine_py --dependencies valid_ssot_md
```

### Authority Chain Violation

If validation reports authority chain violation:

```bash
# Check engine domain and output type
domainization show your_engine_py

# Ensure engine domain matches output type:
# SIGNALS → signal outputs
# SEMANTICS → semantic states
# REASONING → reasoning objects
# REPORT → report text
```

## Requirements Satisfied

This implementation satisfies the following requirements:

- **1.2** - Register artifacts with metadata (engine files)
- **1.5** - Artifact metadata includes domain, type, lifecycle, dependencies
- **2.3** - Domain assignment validation
- **2.8** - SEMANTICS domain support
- **2.9** - REASONING domain support
- **7.3** - SSOT dependency tracking
- **9.1** - Signal generation engines registered
- **9.2** - Semantic and reasoning engines registered
- **9.3** - Report engines registered

## File Structure

```
engines/
├── allocation_engine.py           # SIGNALS domain
├── regime_engine.py               # SIGNALS domain
├── attribution_engine.py          # SIGNALS domain
├── scoring_engine.py              # SIGNALS domain
├── semantic_engine.py             # SEMANTICS domain
├── decision_engine.py             # REASONING domain
├── quality_engine.py              # REASONING domain
├── priority_engine.py             # REASONING domain
├── report_engine.py               # REPORT domain
├── morning_briefing_engine.py     # REPORT domain
├── delta_engine.py                # REPORT domain
├── scenario_engine.py             # SIM domain
├── visual_engine.py               # USER domain
├── engine_registry.py             # ARCH domain
└── engine_runner.py               # ARCH domain

reports/
└── pm_report_engine.py            # REPORT domain (development)

.domainization/
├── artifact_registry.yaml         # Registry with all metadata
└── src/
    └── README_engine_registration.md  # This file
```

## See Also

- [SSOT Document Registration](README_ssot_document_registration.md) - SSOT registration guide
- [Command-Line Interface](README_command_line_interface.md) - CLI documentation
- [CLI Usage Guide](README_cli_usage.md) - Detailed usage examples
- [Registry Layer Python API](README_registry_layer_python_api.md) - Registry API
- [Validation Observers](README_validation_observers.md) - Validation system
- [Reporting Layer](README_reporting_layer.md) - Health reporting
- [Design Document](../../.kiro/specs/domainization/design.md) - System design
- [Requirements Document](../../.kiro/specs/domainization/requirements.md) - Requirements

## Summary

Task 9 successfully registered all engine files in the `engines/` and `reports/` directories with complete metadata in the artifact registry. This enables:

- **Clear Domain Ownership** - Every engine has a primary domain owner
- **Artifact Tracking** - All engines are tracked in the registry
- **Dependency Management** - Engine dependencies on SSOT specifications are explicit
- **Lifecycle Management** - Engine lifecycle is tracked and validated
- **Access Control** - Read/write permissions are defined
- **Implementation Traceability** - Engines are linked to their SSOT specifications
- **Authority Chain Enforcement** - Proper data flow through reasoning chain
- **Validation** - Automated validation ensures compliance
- **Health Reporting** - Comprehensive health metrics for engines

All 15 engines across 7 domains are now properly registered and validated.

## Author

Implemented as part of Task 9 of the domainization system for Portfolio OS.

## License

Internal use only.
