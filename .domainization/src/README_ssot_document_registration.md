# SSOT Document Registration

## Overview

This document describes the SSOT (Single Source of Truth) document registration process implemented in Task 8. All markdown documents in the `docs/` directory have been registered with YAML frontmatter containing domain metadata, enabling proper artifact tracking and governance within the domainization system.

## Purpose

The registration of SSOT documents serves multiple purposes:

1. **Domain Ownership** - Establishes clear ownership boundaries for each document
2. **Artifact Tracking** - Enables the domainization system to track and validate documents
3. **Dependency Management** - Documents dependencies between SSOT documents
4. **Lifecycle Management** - Tracks the lifecycle status of each document
5. **Access Control** - Defines which domains can write to and read from each document
6. **SSOT Governance** - Prevents conflicts and ensures canonical truth sources

## Frontmatter Schema

Each registered SSOT document contains YAML frontmatter with the following fields:

```yaml
---
artifact_id: <unique_identifier>
primary_domain: <DOMAIN_ID>
secondary_domains: [<DOMAIN_ID>, ...]  # Optional
artifact_type: <TYPE>
lifecycle_status: <STATUS>
created_date: <YYYY-MM-DD>
last_modified: <YYYY-MM-DD>
owner_role: <description>
ssot_relationship: <RELATIONSHIP>
topic: <topic_name>
allowed_writers: [<DOMAIN_ID>, ...]
allowed_readers: [<DOMAIN_ID>, ...]
dependencies: [<artifact_id>, ...]  # Optional
---
```

### Field Descriptions

- **artifact_id**: Unique identifier derived from filename (e.g., `decision_governance_md`)
- **primary_domain**: Primary owning domain (GOV, ARCH, SIGNALS, REPORT, etc.)
- **secondary_domains**: Optional list of secondary domains with shared responsibility
- **artifact_type**: Type of artifact (SSOT, CALIBRATION, STEERING)
- **lifecycle_status**: Current lifecycle state (canonical, published, active, etc.)
- **created_date**: Original creation date
- **last_modified**: Last modification date
- **owner_role**: Description of the document's responsibility
- **ssot_relationship**: Relationship to truth (canonical, derived, implementation, none)
- **topic**: Topic identifier for SSOT conflict detection
- **allowed_writers**: List of domains permitted to modify the document
- **allowed_readers**: List of domains permitted to read the document (typically [ALL])
- **dependencies**: Optional list of artifact IDs this document depends on

## Registered Documents by Domain

### Governance Domain (GOV)

Documents defining system governance, decision authority, and compliance rules:


- **decision_governance.md** - Decision-making principles and AI role boundaries
- **confidence_model.md** - Confidence calculation methodology and interpretation rules
- **action_space_framework.md** - Action space generation principles and option structuring
- **portfolio_os_domainization_steering.md** - Canonical domain ownership and governance rules (STEERING artifact)

### Architecture Domain (ARCH)

Documents defining system design, structural principles, and architectural boundaries:

- **system_architecture.md** - System architecture layers and component responsibilities
- **engine_design_principles.md** - Engine design patterns and modularity principles
- **report_pipeline_architecture.md** - Report generation pipeline and stage orchestration
- **semantic_reasoning_rules.md** - Semantic interpretation and reasoning transformation rules
- **domainization_architecture.md** - Domainization system architecture and governance framework
- **kiro_calibration_report.md** - Initial system analysis and calibration findings (CALIBRATION artifact)
- **future_framework_backlog.md** - Planned future frameworks and expansion roadmap

### Signals Domain (SIGNALS)

Documents defining signal generation, semantic interpretation, and portfolio intelligence:

- **semantic_signal_registry.md** - Canonical semantic states and signal vocabulary
- **signal_calculation_framework.md** - Signal calculation rules and threshold governance
- **portfolio_health_framework.md** - Portfolio health evaluation methodology
- **correlation_dependency_framework.md** - Correlation analysis and dependency detection methodology
- **scoring_methodology_framework.md** - Scoring calculation and normalization methodology
- **opportunity_engine_design.md** - Opportunity identification and evaluation methodology
- **market_regime_framework.md** - Market regime classification and interpretation methodology

### Reasoning Domain (REASONING)

Documents defining reasoning logic and interpretation systems:

- **deployment_intelligence_framework.md** - Deployment reasoning and capital positioning interpretation

### Report Domain (REPORT)

Documents defining report generation, PM reasoning synthesis, and language rendering:

- **report_reasoning_system.md** - Report reasoning orchestration and PM interpretation rules
- **report_section_specification.md** - Canonical report structure and section specifications
- **multilingual_rendering_framework.md** - Multilingual rendering rules and translation governance

### Portfolio State Domain (STATE)

Documents defining portfolio state modeling, position tracking, and exposure analysis:

- **portfolio_state_model.md** - Canonical portfolio state structure and hierarchy
- **watchlist_asset_registry_framework.md** - Watchlist management and asset registry framework

### Data Domain (DATA)

Documents defining data ingestion, normalization, and source management:

- **data_ingestion_normalization_framework.md** - Data ingestion, normalization, and validation rules
- **trusted_signal_sources.md** - Trusted data sources and signal governance rules

### User Domain (USER)

Documents defining user-facing experience, readability, and accessibility:

- **dashboard_philosophy.md** - Dashboard design philosophy and visualization principles

### Memory Domain (MEMORY)

Documents defining historical data preservation and longitudinal analysis:

- **portfolio_memory_architecture.md** - Portfolio memory persistence and longitudinal reasoning architecture

### Simulation Domain (SIM)

Documents defining simulation architecture, stress testing, and scenario analysis:

- **simulation_architecture.md** - Simulation framework and scenario analysis architecture

## Registration Process

### Task 8 Implementation

Task 8 was divided into 6 subtasks, each handling a specific domain or group of domains:

#### Subtask 8.1 - Governance Domain
Registered governance SSOT documents with GOV domain ownership.

#### Subtask 8.2 - Architecture Domain
Registered architecture SSOT documents with ARCH domain ownership, including the calibration report.

#### Subtask 8.3 - Signals Domain
Registered all signal-related SSOT documents with SIGNALS domain ownership.

#### Subtask 8.4 - Semantics and Reasoning Domains
Reviewed and registered documents belonging to SEMANTICS or REASONING domains.

#### Subtask 8.5 - Report Domain
Registered report generation and rendering SSOT documents with REPORT domain ownership.

#### Subtask 8.6 - Remaining Domains
Registered documents for STATE, DATA, USER, MEMORY, and SIM domains.

### Validation

After registration, all documents were validated to ensure:

1. **Schema Compliance** - All required frontmatter fields are present
2. **Domain Validity** - Primary and secondary domains are valid domain IDs
3. **Artifact Type Validity** - Artifact types match allowed types for the domain
4. **Lifecycle Validity** - Lifecycle status is valid for the artifact type
5. **Dependency Validity** - Referenced dependencies exist in the registry
6. **SSOT Consistency** - No topic conflicts between canonical SSOT documents

## Usage

### Querying Registered Documents

Use the domainization CLI to query registered SSOT documents:

```bash
# List all SSOT documents
domainization list --type SSOT

# List documents by domain
domainization list --domain GOV
domainization list --domain ARCH
domainization list --domain SIGNALS

# Show details for a specific document
domainization show decision_governance_md
domainization show system_architecture_md

# List with verbose output
domainization list --type SSOT --verbose
```

### Updating Document Metadata

Update metadata for registered documents:

```bash
# Update lifecycle status
domainization update decision_governance_md --lifecycle active

# Update last modified date
domainization update system_architecture_md --last-modified 2026-05-26

# Add dependencies
domainization update report_reasoning_system_md \
  --dependencies semantic_reasoning_rules_md report_pipeline_architecture_md
```

### Validating Documents

Run validation observers on registered documents:

```bash
# Validate all documents
domainization validate

# Validate specific document
domainization validate --files docs/decision_governance.md

# Run SSOT consistency validation
domainization validate --observer SSOTConsistencyValidator

# Dry-run mode
domainization validate --dry-run
```

### Health Reporting

Generate health reports for registered documents:

```bash
# Full health report
domainization health

# Domain-specific health report
domainization health --domain GOV

# Save health report to file
domainization health --output reports/ssot_health.yaml

# Show only violations
domainization health --violations-only
```

## Artifact Types

### SSOT (Single Source of Truth)

Canonical documents that define authoritative specifications:

- **Characteristics**: Authoritative, versioned, domain-owned
- **Examples**: decision_governance.md, system_architecture.md
- **SSOT Relationship**: canonical
- **Lifecycle**: canonical, active, deprecated

### CALIBRATION

Analysis and calibration reports:

- **Characteristics**: Derived from system analysis, time-stamped
- **Examples**: kiro_calibration_report.md
- **SSOT Relationship**: derived
- **Lifecycle**: published, archived

### STEERING

Governance and steering documents:

- **Characteristics**: Cross-domain governance rules, high authority
- **Examples**: portfolio_os_domainization_steering.md
- **SSOT Relationship**: canonical
- **Lifecycle**: canonical, active

## SSOT Relationships

### Canonical

The document is the authoritative source of truth for its topic:

- Only one canonical SSOT per topic allowed
- Highest authority level
- Changes require governance approval
- Examples: All domain SSOT documents

### Derived

The document is derived from canonical sources:

- Must reference source documents in dependencies
- Lower authority than canonical
- Can be regenerated from sources
- Examples: Calibration reports, analysis documents

### Implementation

The document implements specifications from canonical sources:

- Contains executable code or configurations
- Must trace to canonical SSOT documents
- Examples: Engine implementations (not in docs/)

### None

The document is not part of the SSOT hierarchy:

- Informational or temporary documents
- No governance requirements
- Examples: Meeting notes, drafts

## Dependencies

Documents can declare dependencies on other artifacts:

```yaml
dependencies: [system_architecture_md, decision_governance_md]
```

### Dependency Rules

1. **Canonical SSOT** documents should minimize dependencies
2. **Derived documents** must declare all source dependencies
3. **Implementation artifacts** must reference their SSOT specifications
4. **Circular dependencies** are not allowed
5. **Cross-domain dependencies** are permitted and encouraged

### Common Dependency Patterns

- **Architecture → Governance**: Architecture documents depend on governance rules
- **Report → Architecture**: Report documents depend on architecture specifications
- **Signals → Architecture**: Signal documents depend on system architecture
- **Domain-Specific → System**: Domain documents depend on system architecture

## Access Control

### Allowed Writers

Defines which domains can modify the document:

```yaml
allowed_writers: [GOV]  # Only Governance domain can write
allowed_writers: [ARCH, GOV]  # Architecture and Governance can write
```

### Allowed Readers

Defines which domains can read the document:

```yaml
allowed_readers: [ALL]  # All domains can read (most common)
allowed_readers: [ARCH, GOV, SIGNALS]  # Restricted access
```

### Access Control Patterns

- **Public SSOT**: `allowed_readers: [ALL]` - Most SSOT documents
- **Restricted SSOT**: `allowed_readers: [specific domains]` - Sensitive documents
- **Single Writer**: `allowed_writers: [DOMAIN]` - Domain-owned documents
- **Shared Writers**: `allowed_writers: [DOMAIN1, DOMAIN2]` - Cross-domain documents

## Lifecycle Management

### Lifecycle States

- **canonical**: Authoritative SSOT document (permanent)
- **active**: Currently in use and maintained
- **published**: Published report or analysis
- **development**: Under active development
- **deprecated**: No longer recommended, maintained for compatibility
- **archived**: Historical record, no longer maintained

### Lifecycle Transitions

Valid transitions for SSOT documents:

- `canonical` → (permanent state, no transitions)
- `active` → `deprecated` → `archived`
- `published` → `archived`
- `development` → `active` → `deprecated` → `archived`

## Topic-Based SSOT Conflict Detection

Each SSOT document declares a topic:

```yaml
topic: decision_governance
```

### Topic Rules

1. **One Canonical per Topic**: Only one document can be canonical for a given topic
2. **Topic Uniqueness**: Topics should be descriptive and unique
3. **Topic Hierarchy**: Related topics can share prefixes (e.g., `report_reasoning`, `report_sections`)
4. **Cross-Domain Topics**: Topics can span multiple domains

### Conflict Detection

The domainization system validates:

- No two canonical SSOT documents share the same topic
- Derived documents can share topics with canonical sources
- Implementation artifacts can share topics with SSOT specifications

## Integration with Domainization System

### Registry Integration

All registered documents are tracked in the artifact registry:

- **Location**: `.domainization/artifact_registry.yaml`
- **Format**: YAML with full metadata
- **Validation**: Automatic validation on registration and updates

### Validation Observers

Multiple observers validate registered documents:

1. **RegistrationValidator**: Ensures all documents are registered
2. **DomainAssignmentValidator**: Validates domain ownership
3. **LifecycleValidator**: Validates lifecycle transitions
4. **BoundaryAwarenessValidator**: Checks domain boundaries
5. **SSOTConsistencyValidator**: Prevents SSOT conflicts

### Health Reporting

Health reports include SSOT document metrics:

- **Domain Coverage**: Documents per domain
- **Lifecycle Distribution**: Documents by lifecycle state
- **SSOT Conflicts**: Any topic conflicts detected
- **Dependency Health**: Broken or circular dependencies
- **Violations**: Any governance violations

## Best Practices

### When Creating New SSOT Documents

1. **Choose the Right Domain**: Assign to the domain with primary responsibility
2. **Define Clear Topic**: Use descriptive, unique topic names
3. **Declare Dependencies**: Reference all source documents
4. **Set Appropriate Access**: Use `[ALL]` for readers unless restricted
5. **Use Canonical Relationship**: For authoritative specifications
6. **Add Owner Role**: Clearly describe the document's responsibility

### When Updating SSOT Documents

1. **Update last_modified**: Always update the modification date
2. **Maintain Dependencies**: Keep dependency list current
3. **Respect Lifecycle**: Follow valid lifecycle transitions
4. **Validate Changes**: Run validation after updates
5. **Document Changes**: Update version or changelog if applicable

### When Deprecating SSOT Documents

1. **Transition Lifecycle**: Move to `deprecated` state
2. **Document Replacement**: Reference the replacement document
3. **Update Dependencies**: Update documents that depend on it
4. **Maintain Temporarily**: Keep available during transition period
5. **Archive Eventually**: Move to `archived` when no longer needed

## Troubleshooting

### Document Not Registered

If a document is not showing up in queries:

```bash
# Check if file exists
ls -la docs/your_document.md

# Verify frontmatter is present
head -20 docs/your_document.md

# Manually register if needed
domainization register your_document_md docs/your_document.md DOMAIN SSOT
```

### SSOT Conflict Detected

If validation reports a topic conflict:

```bash
# Find conflicting documents
domainization list --type SSOT --verbose | grep "topic:"

# Update one document to use a different topic
# Edit the frontmatter manually or use update command
```

### Invalid Domain or Type

If validation reports invalid domain or type:

```bash
# Check valid domains
domainization config show

# Update to valid domain
domainization update artifact_id --domain VALID_DOMAIN
```

### Broken Dependencies

If health report shows broken dependencies:

```bash
# Check dependencies
domainization show artifact_id

# Update dependencies to valid artifact IDs
domainization update artifact_id --dependencies valid_id1 valid_id2
```

## Requirements Satisfied

This implementation satisfies the following requirements:

- **1.2** - Register artifacts with metadata (SSOT documents)
- **1.5** - Artifact metadata includes domain, type, lifecycle, dependencies
- **2.3** - Domain assignment validation
- **2.8** - SEMANTICS domain support
- **2.9** - REASONING domain support
- **9.1** - SSOT documents have YAML frontmatter
- **9.2** - Frontmatter includes all required fields
- **9.3** - SSOT relationship and topic fields present

## File Structure

```
docs/
├── decision_governance.md              # GOV domain
├── confidence_model.md                 # GOV domain
├── action_space_framework.md           # GOV domain
├── portfolio_os_domainization_steering.md  # GOV/ARCH steering
├── system_architecture.md              # ARCH domain
├── engine_design_principles.md         # ARCH domain
├── report_pipeline_architecture.md     # ARCH domain
├── semantic_reasoning_rules.md         # ARCH domain
├── future_framework_backlog.md         # ARCH domain
├── semantic_signal_registry.md         # SIGNALS domain
├── signal_calculation_framework.md     # SIGNALS domain
├── portfolio_health_framework.md       # SIGNALS domain
├── correlation_dependency_framework.md # SIGNALS domain
├── scoring_methodology_framework.md    # SIGNALS domain
├── opportunity_engine_design.md        # SIGNALS domain
├── market_regime_framework.md          # SIGNALS domain
├── deployment_intelligence_framework.md # REASONING domain
├── report_reasoning_system.md          # REPORT domain
├── report_section_specification.md     # REPORT domain
├── multilingual_rendering_framework.md # REPORT domain
├── portfolio_state_model.md            # STATE domain
├── watchlist_asset_registry_framework.md # STATE domain
├── data_ingestion_normalization_framework.md # DATA domain
├── trusted_signal_sources.md           # DATA domain
├── dashboard_philosophy.md             # USER domain
├── portfolio_memory_architecture.md    # MEMORY domain
└── simulation_architecture.md          # SIM domain

reports/
└── kiro_calibration_report.md          # ARCH domain (CALIBRATION)

.kiro/specs/domainization/
└── domainization_architecture.md       # ARCH domain

.domainization/
├── artifact_registry.yaml              # Registry with all metadata
└── src/
    └── README_ssot_document_registration.md  # This file
```

## See Also

- [Command-Line Interface](README_command_line_interface.md) - CLI documentation
- [CLI Usage Guide](README_cli_usage.md) - Detailed usage examples
- [Registry Layer Python API](README_registry_layer_python_api.md) - Registry API
- [Validation Observers](README_validation_observers.md) - Validation system
- [Reporting Layer](README_reporting_layer.md) - Health reporting
- [Design Document](../../.kiro/specs/domainization/design.md) - System design
- [Requirements Document](../../.kiro/specs/domainization/requirements.md) - Requirements
- [Domainization Architecture](../../.kiro/specs/domainization/domainization_architecture.md) - Architecture spec

## Summary

Task 8 successfully registered all SSOT documents in the `docs/` directory with proper YAML frontmatter. This enables:

- **Clear Domain Ownership** - Every document has a primary domain owner
- **Artifact Tracking** - All documents are tracked in the registry
- **Dependency Management** - Document dependencies are explicit
- **Lifecycle Management** - Document lifecycle is tracked and validated
- **Access Control** - Read/write permissions are defined
- **SSOT Governance** - Topic-based conflict detection prevents duplicates
- **Validation** - Automated validation ensures compliance
- **Health Reporting** - Comprehensive health metrics for documentation

All 27 SSOT documents across 10 domains are now properly registered and validated.

## Author

Implemented as part of Task 8 of the domainization system for Portfolio OS.

## License

Internal use only.
