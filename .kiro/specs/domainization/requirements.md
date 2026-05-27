# Requirements Document

## Introduction

Portfolio OS requires a systematic artifact governance framework to prevent structural chaos and enforce domain boundaries. The domainization feature will implement an indexing and validation system that assigns every artifact to a primary domain, tracks lifecycle states, and enforces boundaries through automated commit gates.

Currently, Portfolio OS has 50+ root-level files without clear ownership, no documented lifecycle tracking, and no enforcement mechanisms for domain boundaries. This creates maintenance risks, unclear responsibilities, and potential for orphaned artifacts.

The domainization system will provide:
- Artifact indexing by domain responsibility
- Lifecycle state tracking for all artifacts
- Automated governance enforcement through commit gates
- Clear ownership and maintenance responsibility
- Prevention of orphaned or ungoverned artifacts

## Requirements

### Requirement 1: Artifact Registry Foundation

**User Story:** As a system architect, I want a central artifact registry, so that every file in the repository has documented ownership and lifecycle status.

#### Acceptance Criteria

1. WHEN the system initializes THEN it SHALL create a `.domainization/` directory structure
2. WHEN an artifact is created THEN it SHALL be registered with metadata including artifact_id, primary_domain, artifact_type, and lifecycle_status
3. WHEN an artifact is modified THEN its last_modified timestamp SHALL be updated in the registry
4. IF an artifact is a markdown file THEN it SHALL support YAML frontmatter for metadata
5. IF an artifact is not a markdown file THEN it SHALL be registered in `artifact_registry.yaml`
6. WHEN the registry is queried THEN it SHALL return all artifacts grouped by domain
7. WHEN an artifact is deleted THEN its registry entry SHALL be updated to reflect the deletion

### Requirement 2: Domain Model Definition

**User Story:** As a system architect, I want clearly defined domains with explicit responsibilities, so that artifact ownership is unambiguous and boundaries are enforceable.

#### Acceptance Criteria

1. WHEN the domain registry is created THEN it SHALL define exactly 12 canonical domains
2. WHEN a domain is defined THEN it SHALL include domain_id, name, responsibility_scope, and allowed_artifact_types
3. WHEN domains are queried THEN the system SHALL return GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, and SIM
4. IF an artifact type is assigned to a domain THEN the domain SHALL have explicit authority over that type
5. WHEN domain boundaries are defined THEN each domain SHALL specify what it can own and what it cannot own
6. WHEN a domain is referenced THEN it SHALL exist in the domain registry
7. IF a domain assignment is invalid THEN the system SHALL reject it with an error message
8. WHEN domain priorities are defined THEN core reasoning domains SHALL have architectural priority over surface domains
9. WHEN the primary reasoning chain is defined THEN it SHALL be SIGNALS → SEMANTICS → REASONING → REPORT
10. IF surface domains (USER, DEPLOY) conflict with core reasoning domains THEN core reasoning domains SHALL take precedence



### Requirement 3: Artifact Classification System

**User Story:** As a developer, I want artifacts classified by type with defined lifecycle states, so that I understand the maturity and purpose of each file.

#### Acceptance Criteria

1. WHEN an artifact is registered THEN it SHALL be assigned one of 11 defined artifact types
2. WHEN artifact types are defined THEN they SHALL include SSOT, ENGINE, REPORT_OUT, DATA_IN, DATA_OUT, RUNTIME, DASHBOARD, SNAPSHOT, CONFIG, CALIBRATION, and STEERING
3. WHEN an artifact type is assigned THEN it SHALL have a defined lifecycle state machine
4. IF an artifact is type SSOT THEN its lifecycle SHALL follow draft → review → canonical → deprecated
5. IF an artifact is type ENGINE THEN its lifecycle SHALL follow planned → development → active → deprecated
6. IF an artifact is type REPORT_OUT THEN its lifecycle SHALL follow generated → current → archived
7. WHEN an artifact's lifecycle status changes THEN the transition SHALL be validated against the state machine

### Requirement 4: Lifecycle State Management

**User Story:** As a system maintainer, I want lifecycle states tracked for all artifacts, so that I can identify deprecated, active, and draft artifacts.

#### Acceptance Criteria

1. WHEN an artifact is created THEN it SHALL be assigned an initial lifecycle_status
2. WHEN a lifecycle transition is requested THEN the system SHALL validate it against the state machine rules
3. IF a transition is invalid THEN the system SHALL block it and provide an error message
4. WHEN an artifact is marked as deprecated THEN it SHALL not be modifiable except for metadata updates
5. WHEN an artifact is marked as canonical THEN it SHALL be the authoritative source for its topic
6. IF multiple artifacts claim canonical status for the same topic THEN the system SHALL detect and report the conflict
7. WHEN lifecycle states are queried THEN the system SHALL return counts by state and artifact type

### Requirement 5: Commit Gate Validation

**User Story:** As a developer, I want automated validation at commit time, so that I cannot accidentally violate domain boundaries or create ungoverned artifacts.

#### Acceptance Criteria

1. WHEN a commit is attempted THEN the system SHALL execute 5 validation gates in sequence
2. WHEN Gate 1 executes THEN it SHALL verify all new or modified files have metadata
3. WHEN Gate 2 executes THEN it SHALL validate domain assignments against the domain registry
4. WHEN Gate 3 executes THEN it SHALL validate lifecycle state transitions
5. WHEN Gate 4 executes THEN it SHALL enforce domain boundary rules and writer permissions
6. WHEN Gate 5 executes THEN it SHALL validate SSOT consistency and prevent conflicts
7. IF any gate fails THEN the commit SHALL be blocked with an actionable error message
8. WHEN all gates pass THEN the commit SHALL be allowed to proceed
9. WHEN the system is in FAST LANE REPORT MVP phase THEN commit gates SHALL be deferred until MVP stabilizes
10. IF commit gates are implemented before report value is established THEN governance SHALL not block report development



### Requirement 6: Domain Boundary Enforcement

**User Story:** As a domain owner, I want domain boundaries enforced automatically, so that other domains cannot modify my artifacts without permission.

#### Acceptance Criteria

1. WHEN an artifact is registered THEN it SHALL specify allowed_writers as a list of domain IDs
2. WHEN a file is modified THEN the system SHALL verify the modifier is in the allowed_writers list
3. IF a cross-domain modification is attempted THEN it SHALL require explicit approval
4. WHEN SSOT documents are modified THEN only the primary domain owner SHALL have write authority
5. IF a domain boundary violation is detected THEN the commit SHALL be blocked
6. WHEN boundary rules are defined THEN they SHALL specify what each domain can and cannot own
7. WHEN a violation occurs THEN the error message SHALL explain which rule was violated and suggest resolution

### Requirement 7: SSOT Consistency Validation

**User Story:** As a system architect, I want single source of truth principles enforced, so that there is only one canonical document per topic.

#### Acceptance Criteria

1. WHEN an artifact is marked as canonical SSOT THEN the system SHALL verify no other canonical SSOT exists for the same topic
2. WHEN a derived document is created THEN it SHALL reference its canonical SSOT in metadata
3. WHEN an implementation artifact is created THEN it SHALL reference the SSOT specification it implements
4. IF multiple canonical SSOTs are detected for the same topic THEN the commit SHALL be blocked
5. WHEN SSOT relationships are queried THEN the system SHALL return canonical, derived, and implementation artifacts
6. WHEN a canonical SSOT is deprecated THEN it SHALL reference its replacement
7. IF an SSOT conflict is detected THEN the error message SHALL identify the conflicting artifacts

### Requirement 8: Metadata Schema Validation

**User Story:** As a developer, I want consistent metadata schemas, so that all artifacts have the same required fields.

#### Acceptance Criteria

1. WHEN metadata is defined THEN it SHALL include artifact_id, primary_domain, artifact_type, lifecycle_status, created_date, and last_modified
2. WHEN metadata is defined THEN it SHALL optionally include secondary_domains, owner_role, ssot_relationship, allowed_writers, allowed_readers, and dependencies
3. IF metadata is in YAML frontmatter THEN it SHALL be validated against the schema
4. IF metadata is in the artifact registry THEN it SHALL be validated against the schema
5. WHEN invalid metadata is detected THEN the system SHALL provide specific validation errors
6. WHEN metadata is queried THEN the system SHALL return all fields for the artifact
7. IF required fields are missing THEN the commit SHALL be blocked



### Requirement 9: Gradual Migration Support

**User Story:** As a system maintainer, I want gradual migration without breaking existing functionality, so that domainization can be implemented incrementally.

#### Acceptance Criteria

1. WHEN domainization is implemented THEN existing files SHALL remain in their current locations
2. WHEN the artifact registry is created THEN it SHALL work with the current directory structure
3. IF an artifact is not yet registered THEN the system SHALL allow it during the migration phase
4. WHEN migration phases are defined THEN they SHALL be: foundation, registration, commit gates, lifecycle enforcement, boundary enforcement, and monitoring
5. WHEN a migration phase completes THEN the system SHALL validate that phase's requirements
6. IF existing functionality breaks THEN the migration SHALL be rolled back
7. WHEN migration is complete THEN all artifacts SHALL be registered and validated
8. WHEN the system is in FAST LANE REPORT MVP phase THEN registry enforcement SHALL remain soft-validation only
9. IF registry enforcement blocks report development THEN enforcement SHALL be relaxed until report value is established
10. WHEN artifacts are registered THEN the process SHALL not require excessive metadata updates for small changes

### Requirement 10: Health Reporting and Monitoring

**User Story:** As a system architect, I want health reports showing domainization status, so that I can track progress and identify violations.

#### Acceptance Criteria

1. WHEN a health report is requested THEN it SHALL show total artifacts, registered artifacts, and unregistered artifacts
2. WHEN a health report is generated THEN it SHALL show domain coverage with artifact counts per domain
3. WHEN a health report is generated THEN it SHALL show lifecycle distribution across all artifact types
4. IF violations exist THEN the health report SHALL list them with severity levels
5. WHEN violations are detected THEN the report SHALL provide actionable recommendations
6. WHEN the report is generated THEN it SHALL include a timestamp and version number
7. IF the system is healthy THEN the report SHALL indicate 100% artifact registration and zero violations

### Requirement 11: Google-Only Deployment Constraint

**User Story:** As a deployment engineer, I want Google-only infrastructure enforced, so that no AWS, Supabase, or Azure dependencies are introduced.

#### Acceptance Criteria

1. WHEN commit gates execute THEN they SHALL scan for forbidden cloud provider references
2. IF AWS service references are detected THEN the commit SHALL be blocked
3. IF Supabase API calls are detected THEN the commit SHALL be blocked
4. IF Azure infrastructure references are detected THEN the commit SHALL be blocked
5. WHEN Google Cloud Platform references are detected THEN they SHALL be allowed
6. WHEN Google Sheets API references are detected THEN they SHALL be allowed
7. IF a forbidden provider is detected THEN the error message SHALL specify which provider and where it was found



### Requirement 12: Report-First Priority Enforcement

**User Story:** As a product owner, I want report value validated for new features, so that development focuses on improving report quality.

#### Acceptance Criteria

1. WHEN a new feature is proposed THEN it SHALL answer "How does this improve the report?"
2. IF no report value is identified THEN the feature SHALL be deferred
3. WHEN report value is claimed THEN it SHALL be measurable and direct
4. IF report value is speculative or indirect THEN the feature SHALL be rejected
5. WHEN allowed report value categories are defined THEN they SHALL include semantic interpretation, PM reasoning, concentration explanation, dependency explanation, scenario interpretation, confidence explanation, action-space clarity, multilingual rendering, traceability, and user understanding
6. WHEN the report domain reviews a feature THEN it SHALL have veto authority
7. IF a feature adds complexity without report benefit THEN it SHALL be rejected
8. WHEN features primarily improve infrastructure, deployment sophistication, or architectural elegance without immediate report value THEN they SHALL be deferred
9. IF a feature improves governance but not report quality THEN it SHALL be deferred until report MVP is stable
10. WHEN feature priority is evaluated THEN report value SHALL take precedence over architectural elegance

### Requirement 13: Domain-Specific Writer/Reader Rules

**User Story:** As a domain owner, I want explicit writer and reader rules, so that domain responsibilities are clear and enforceable.

#### Acceptance Criteria

1. WHEN SIGNALS domain writes THEN it SHALL write structured signals only
2. WHEN SIGNALS domain writes THEN it SHALL NOT write semantic interpretations
3. WHEN SEMANTICS domain writes THEN it SHALL write semantic states only
4. WHEN SEMANTICS domain writes THEN it SHALL NOT write raw signals
5. WHEN REASONING domain writes THEN it SHALL write reasoning objects only
6. WHEN REASONING domain writes THEN it SHALL NOT write semantic states
7. WHEN REPORT domain writes THEN it SHALL write human-readable text only
8. WHEN REPORT domain writes THEN it SHALL NOT write business logic
9. WHEN DATA domain writes THEN it SHALL normalize data only
10. WHEN DATA domain writes THEN it SHALL NOT reason about data
11. WHEN all domains read THEN they SHALL be able to read canonical SSOT documents
12. WHEN SEMANTICS domain reads THEN it SHALL be able to read signal outputs
13. WHEN REASONING domain reads THEN it SHALL be able to read semantic states
14. WHEN REPORT domain reads THEN it SHALL be able to read reasoning objects

### Requirement 14: Runtime Flow Validation

**User Story:** As a system architect, I want runtime flows validated, so that forbidden data flows are prevented and authority chains are preserved.

#### Acceptance Criteria

1. WHEN Signal → Semantic → Reasoning → Report flow is executed THEN it SHALL be allowed
2. WHEN Signal → Report flow is attempted THEN it SHALL be forbidden and blocked
3. WHEN Signal → Reasoning flow is attempted THEN it SHALL be forbidden and blocked
4. WHEN Dashboard → Semantic Truth flow is attempted THEN it SHALL be forbidden and blocked
5. WHEN Dashboard → Signal Generation flow is attempted THEN it SHALL be forbidden and blocked
6. WHEN a forbidden flow is detected THEN it SHALL be logged with details
7. WHEN flow traceability is requested THEN the system SHALL show the complete signal-to-report chain
8. WHEN runtime flows are defined THEN they SHALL represent authority chains, not just data flows
9. WHEN meaning is created THEN it SHALL follow the authority chain: raw signals → semantic interpretation → reasoning conclusions → report language
10. IF a domain attempts to create meaning outside its authority THEN the flow SHALL be blocked



### Requirement 15: Non-Functional Requirements

**User Story:** As a system user, I want the domainization system to be performant, explainable, and maintainable, so that it supports rather than hinders development.

#### Acceptance Criteria

1. WHEN commit gates execute THEN they SHALL complete in less than 5 seconds
2. WHEN the artifact registry is queried THEN it SHALL support at least 1000 artifacts
3. WHEN health reports are generated THEN they SHALL complete in less than 10 seconds
4. WHEN a validation fails THEN the error message SHALL explain why and suggest resolution
5. WHEN the same input is validated THEN it SHALL always produce the same result (determinism)
6. WHEN lifecycle changes occur THEN they SHALL be logged for traceability
7. WHEN domain definitions change THEN they SHALL require governance approval
8. WHEN commit gates are tested THEN they SHALL be independently executable
9. WHEN the system scales THEN it SHALL support at least 20 domains and 10 lifecycle states per artifact type
10. WHEN documentation is provided THEN validation rules SHALL be clearly documented
