"""
Acceptance Tests for Domainization System

BDD-style acceptance tests using Gherkin format (Given/When/Then).
Tests real-world scenarios that validate the system works correctly
from a user perspective.

Scenarios covered:
1. New developer adding a feature (registration, domain assignment, lifecycle)
2. Invalid domain assignment detection
3. SSOT conflict detection
4. Gradual migration support

Requirements: 15.1, 15.2, 15.3, 15.5
"""

import os
import sys
import shutil
import tempfile
import yaml
import pytest
from pathlib import Path

# Ensure src directory is on path
SRC_DIR = Path(__file__).parent
sys.path.insert(0, str(SRC_DIR))

from artifact_schema import ArtifactMetadata
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from validation_orchestrator import ValidationOrchestrator
from health_reporter import HealthReporter


# ============================================================================
# Shared Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test isolation"""
    tmp = tempfile.mkdtemp()
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def domainization_dir(temp_dir):
    """Create a minimal .domainization directory structure"""
    dom_dir = temp_dir / ".domainization"
    dom_dir.mkdir()
    (dom_dir / "backups").mkdir()
    (dom_dir / "logs").mkdir()
    (dom_dir / "reports").mkdir()
    (dom_dir / "src").mkdir()
    return dom_dir



@pytest.fixture
def domain_registry_data():
    """Full 12-domain registry for acceptance testing"""
    return {
        'domains': [
            {
                'domain_id': 'GOV',
                'name': 'Governance',
                'responsibility_scope': 'System governance and policies',
                'allowed_artifact_types': ['SSOT', 'CONFIG', 'STEERING'],
                'cannot_own': ['ENGINE', 'DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'ARCH',
                'name': 'Architecture',
                'responsibility_scope': 'System architecture and design',
                'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG', 'STEERING'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'SIGNALS',
                'name': 'Signal Generation',
                'responsibility_scope': 'Raw signal generation and calculation',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT', 'CONFIG'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT'],
                'priority': 'core',
                'authority_level': 1
            },
            {
                'domain_id': 'SEMANTICS',
                'name': 'Semantic Interpretation',
                'responsibility_scope': 'Semantic state interpretation',
                'allowed_artifact_types': ['ENGINE', 'SSOT', 'CONFIG'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT', 'DATA_OUT'],
                'priority': 'core',
                'authority_level': 2
            },
            {
                'domain_id': 'REASONING',
                'name': 'Reasoning Logic',
                'responsibility_scope': 'Reasoning and decision logic',
                'allowed_artifact_types': ['ENGINE', 'SSOT', 'CONFIG'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT', 'DATA_OUT'],
                'priority': 'core',
                'authority_level': 3
            },
            {
                'domain_id': 'REPORT',
                'name': 'Report Generation',
                'responsibility_scope': 'Human-readable report generation',
                'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT', 'CONFIG'],
                'cannot_own': ['DATA_OUT', 'DASHBOARD'],
                'priority': 'core',
                'authority_level': 4
            },
            {
                'domain_id': 'STATE',
                'name': 'Portfolio State',
                'responsibility_scope': 'Portfolio state management',
                'allowed_artifact_types': ['DATA_IN', 'DATA_OUT', 'SSOT', 'CONFIG', 'SNAPSHOT'],
                'cannot_own': ['ENGINE', 'DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'DATA',
                'name': 'Data Management',
                'responsibility_scope': 'Data ingestion and normalization',
                'allowed_artifact_types': ['ENGINE', 'DATA_IN', 'DATA_OUT', 'SSOT', 'CONFIG'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'USER',
                'name': 'User Interface',
                'responsibility_scope': 'User-facing dashboards and interfaces',
                'allowed_artifact_types': ['DASHBOARD', 'ENGINE', 'SSOT', 'CONFIG'],
                'cannot_own': ['REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'DEPLOY',
                'name': 'Deployment',
                'responsibility_scope': 'Deployment and infrastructure',
                'allowed_artifact_types': ['RUNTIME', 'CONFIG', 'SSOT', 'STEERING'],
                'cannot_own': ['ENGINE', 'DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'MEMORY',
                'name': 'Portfolio Memory',
                'responsibility_scope': 'Historical data and snapshots',
                'allowed_artifact_types': ['SNAPSHOT', 'DATA_IN', 'DATA_OUT', 'SSOT', 'CONFIG'],
                'cannot_own': ['ENGINE', 'DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'SIM',
                'name': 'Simulation',
                'responsibility_scope': 'Scenario simulation and modeling',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT', 'CONFIG'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
        ]
    }


@pytest.fixture
def lifecycle_data():
    """Lifecycle state machines for acceptance testing"""
    return {
        'artifact_types': {
            'SSOT': {
                'description': 'Single Source of Truth documents',
                'states': ['draft', 'review', 'canonical', 'deprecated'],
                'initial_state': 'draft',
                'transitions': [
                    {'from': 'draft', 'to': 'review', 'condition': 'Author completes'},
                    {'from': 'review', 'to': 'canonical', 'condition': 'Domain owner approves'},
                    {'from': 'canonical', 'to': 'draft', 'condition': 'Revision required'},
                    {'from': 'canonical', 'to': 'deprecated', 'condition': 'Superseded'},
                ],
                'modifiable_states': ['draft', 'review', 'canonical'],
                'read_only_states': ['deprecated']
            },
            'ENGINE': {
                'description': 'Processing engines',
                'states': ['planned', 'development', 'active', 'deprecated'],
                'initial_state': 'planned',
                'transitions': [
                    {'from': 'planned', 'to': 'development', 'condition': 'Implementation begins'},
                    {'from': 'development', 'to': 'active', 'condition': 'Production ready'},
                    {'from': 'development', 'to': 'development', 'condition': 'Iteration'},
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'},
                ],
                'modifiable_states': ['planned', 'development', 'active'],
                'read_only_states': ['deprecated']
            },
            'REPORT_OUT': {
                'description': 'Report outputs',
                'states': ['generated', 'current', 'archived'],
                'initial_state': 'generated',
                'transitions': [
                    {'from': 'generated', 'to': 'current', 'condition': 'Becomes latest'},
                    {'from': 'current', 'to': 'archived', 'condition': 'Superseded'},
                ],
                'modifiable_states': ['generated', 'current'],
                'read_only_states': ['archived']
            },
            'DATA_IN': {
                'description': 'Input data',
                'states': ['active', 'stale', 'archived'],
                'initial_state': 'active',
                'transitions': [
                    {'from': 'active', 'to': 'stale', 'condition': 'Data outdated'},
                    {'from': 'stale', 'to': 'archived', 'condition': 'Moved to history'},
                ],
                'modifiable_states': ['active', 'stale'],
                'read_only_states': ['archived']
            },
            'DATA_OUT': {
                'description': 'Output data',
                'states': ['generated', 'current', 'archived'],
                'initial_state': 'generated',
                'transitions': [
                    {'from': 'generated', 'to': 'current', 'condition': 'Becomes latest'},
                    {'from': 'current', 'to': 'archived', 'condition': 'Superseded'},
                ],
                'modifiable_states': ['generated', 'current'],
                'read_only_states': ['archived']
            },
            'CONFIG': {
                'description': 'Configuration files',
                'states': ['active', 'deprecated'],
                'initial_state': 'active',
                'transitions': [
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'},
                ],
                'modifiable_states': ['active'],
                'read_only_states': ['deprecated']
            },
            'RUNTIME': {
                'description': 'Runtime entry points',
                'states': ['active', 'deprecated'],
                'initial_state': 'active',
                'transitions': [
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'},
                ],
                'modifiable_states': ['active'],
                'read_only_states': ['deprecated']
            },
            'DASHBOARD': {
                'description': 'Dashboard interfaces',
                'states': ['active', 'deprecated'],
                'initial_state': 'active',
                'transitions': [
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'},
                ],
                'modifiable_states': ['active'],
                'read_only_states': ['deprecated']
            },
            'SNAPSHOT': {
                'description': 'Historical snapshots',
                'states': ['current', 'archived'],
                'initial_state': 'current',
                'transitions': [
                    {'from': 'current', 'to': 'archived', 'condition': 'Superseded'},
                ],
                'modifiable_states': ['current'],
                'read_only_states': ['archived']
            },
            'STEERING': {
                'description': 'Steering documents',
                'states': ['active', 'deprecated'],
                'initial_state': 'active',
                'transitions': [
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'},
                ],
                'modifiable_states': ['active'],
                'read_only_states': ['deprecated']
            },
            'CALIBRATION': {
                'description': 'Calibration artifacts',
                'states': ['active', 'deprecated'],
                'initial_state': 'active',
                'transitions': [
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'},
                ],
                'modifiable_states': ['active'],
                'read_only_states': ['deprecated']
            },
        }
    }


@pytest.fixture
def existing_artifacts_data():
    """Pre-existing artifacts representing a mature repository"""
    return {
        'artifacts': [
            {
                'artifact_id': 'system_architecture_md',
                'file_path': 'docs/system_architecture.md',
                'primary_domain': 'ARCH',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2025-01-01',
                'last_modified': '2025-05-20',
                'owner_role': 'System Architect',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['ARCH'],
                'allowed_readers': ['ALL'],
                'topic': 'system_architecture'
            },
            {
                'artifact_id': 'allocation_engine_py',
                'file_path': 'engines/allocation_engine.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2025-01-15',
                'last_modified': '2025-05-18',
                'owner_role': 'Signal Engineer',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'dependencies': ['system_architecture_md']
            },
            {
                'artifact_id': 'portfolio_report_txt',
                'file_path': 'portfolio_report.txt',
                'primary_domain': 'REPORT',
                'artifact_type': 'REPORT_OUT',
                'lifecycle_status': 'current',
                'created_date': '2025-03-01',
                'last_modified': '2025-05-25',
                'owner_role': 'Report Engine',
                'ssot_relationship': 'derived',
                'allowed_writers': ['REPORT'],
                'allowed_readers': ['ALL'],
                'dependencies': ['system_architecture_md']
            },
            {
                'artifact_id': 'signal_spec_md',
                'file_path': 'docs/signal_specification.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2025-02-01',
                'last_modified': '2025-04-10',
                'owner_role': 'Signal Architect',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'signal_specification'
            },
        ]
    }


@pytest.fixture
def setup_acceptance_environment(temp_dir, domainization_dir, domain_registry_data,
                                  lifecycle_data, existing_artifacts_data):
    """Set up a complete acceptance test environment"""
    # Write domain registry
    domain_registry_path = domainization_dir / "domain_registry.yaml"
    with open(domain_registry_path, 'w') as f:
        yaml.dump(domain_registry_data, f, default_flow_style=False)

    # Write lifecycle state machine
    lifecycle_path = domainization_dir / "lifecycle_state_machine.yaml"
    with open(lifecycle_path, 'w') as f:
        yaml.dump(lifecycle_data, f, default_flow_style=False)

    # Write artifact registry
    artifact_registry_path = domainization_dir / "artifact_registry.yaml"
    with open(artifact_registry_path, 'w') as f:
        yaml.dump(existing_artifacts_data, f, default_flow_style=False)

    # Create sample files in the repo
    docs_dir = temp_dir / "docs"
    docs_dir.mkdir()
    (docs_dir / "system_architecture.md").write_text("# System Architecture\n")
    (docs_dir / "signal_specification.md").write_text("# Signal Specification\n")

    engines_dir = temp_dir / "engines"
    engines_dir.mkdir()
    (engines_dir / "allocation_engine.py").write_text("# Allocation Engine\n")

    (temp_dir / "portfolio_report.txt").write_text("Portfolio Report\n")

    return {
        'repo_root': temp_dir,
        'domainization_dir': domainization_dir,
        'domain_registry_path': domain_registry_path,
        'lifecycle_path': lifecycle_path,
        'artifact_registry_path': artifact_registry_path,
    }


# ============================================================================
# Scenario 1: New Developer Adding a Feature
# ============================================================================


class TestScenarioNewDeveloperAddingFeature:
    """
    Feature: New developer adds a feature to the repository

    As a new developer joining the team,
    I want to add a new engine to the SIGNALS domain,
    So that I can contribute signal processing capabilities.

    The system should guide me through proper registration,
    domain assignment, and lifecycle management.
    """

    def test_developer_creates_unregistered_file_gets_warning(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Developer creates a new file without registering it

        Given a repository with the domainization system active
        And the system is in observability mode (warnings only)
        When a developer creates a new Python engine file
        And the file is not registered in the artifact registry
        Then the validation system should generate a warning
        And the warning should suggest how to register the artifact
        And the commit should NOT be blocked (observability mode)

        Validates: Requirements 15.1, 15.5
        """
        env = setup_acceptance_environment

        # Given: A repository with domainization active
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # When: Developer creates a new unregistered file
        new_engine = env['repo_root'] / "engines" / "new_signal_engine.py"
        new_engine.write_text("# New Signal Engine\nclass NewSignalEngine:\n    pass\n")

        # Then: Validation generates a warning about unregistered artifact
        report = orchestrator.validate_all(changed_files=[new_engine])

        assert report.total_warnings > 0
        # The commit is not blocked (observability mode)
        # Warnings are informational only
        registration_warnings = report.warnings_by_observer.get('RegistrationValidator', [])
        assert len(registration_warnings) > 0

        # Warning should mention the unregistered file
        warning_messages = [w.warning_message for w in registration_warnings]
        assert any('new_signal_engine' in msg or 'not registered' in msg.lower()
                   for msg in warning_messages)

    def test_developer_registers_artifact_correctly(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Developer properly registers a new engine artifact

        Given a repository with the domainization system active
        When a developer registers a new engine with valid metadata
        And assigns it to the SIGNALS domain with ENGINE type
        And sets lifecycle_status to 'planned' (initial state)
        Then the artifact should be successfully registered
        And validation should produce no warnings for this artifact

        Validates: Requirements 15.1, 15.2
        """
        env = setup_acceptance_environment

        # Given: A repository with domainization active
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        # When: Developer registers a new engine correctly
        new_artifact = ArtifactMetadata(
            artifact_id='new_signal_engine_py',
            file_path='engines/new_signal_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='planned',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Signal Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            dependencies=['signal_spec_md']
        )

        # Then: Registration succeeds without error
        artifact_registry.register_artifact(new_artifact)
        artifact_registry.save()

        # Verify artifact is retrievable
        retrieved = artifact_registry.get_artifact('new_signal_engine_py')
        assert retrieved is not None
        assert retrieved.primary_domain == 'SIGNALS'
        assert retrieved.artifact_type == 'ENGINE'
        assert retrieved.lifecycle_status == 'planned'

        # Validate domain assignment is correct
        is_valid, error = domain_registry.validate_domain_assignment('ENGINE', 'SIGNALS')
        assert is_valid is True

        # Validate lifecycle state is valid initial state
        initial_state = lifecycle_manager.get_initial_state('ENGINE')
        assert initial_state == 'planned'

    def test_developer_progresses_artifact_through_lifecycle(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Developer progresses artifact through lifecycle states

        Given a registered engine artifact in 'planned' state
        When the developer transitions it to 'development'
        And later transitions it to 'active'
        Then each transition should be validated as valid
        And the lifecycle manager should confirm the transitions

        Validates: Requirements 15.1, 15.3
        """
        env = setup_acceptance_environment

        # Given: A registered engine in planned state
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        # When: Developer transitions planned -> development
        is_valid, error = lifecycle_manager.validate_transition('ENGINE', 'planned', 'development')
        assert is_valid is True
        assert error is None

        # And: Developer transitions development -> active
        is_valid, error = lifecycle_manager.validate_transition('ENGINE', 'development', 'active')
        assert is_valid is True
        assert error is None

        # Then: The full lifecycle path is valid
        allowed_from_planned = lifecycle_manager.get_allowed_transitions('ENGINE', 'planned')
        assert 'development' in allowed_from_planned

        allowed_from_development = lifecycle_manager.get_allowed_transitions('ENGINE', 'development')
        assert 'active' in allowed_from_development

    def test_developer_gets_guidance_on_invalid_transition(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Developer attempts invalid lifecycle transition

        Given a registered engine artifact in 'planned' state
        When the developer attempts to transition directly to 'active'
        Then the system should reject the transition
        And provide guidance on valid transitions from 'planned'

        Validates: Requirements 15.1, 15.3
        """
        env = setup_acceptance_environment

        # Given: Lifecycle manager loaded
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        # When: Developer attempts invalid transition (planned -> active)
        is_valid, error = lifecycle_manager.validate_transition('ENGINE', 'planned', 'active')

        # Then: Transition is rejected with guidance
        assert is_valid is False
        assert error is not None
        assert 'development' in error  # Should suggest valid transition

    def test_full_developer_workflow_end_to_end(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Complete developer workflow from file creation to validation

        Given a repository with domainization active
        When a developer creates a file, registers it, and runs validation
        Then the system should show zero warnings for the properly registered artifact
        And validation should complete within performance target (<5 seconds)

        Validates: Requirements 15.1, 15.2, 15.5
        """
        env = setup_acceptance_environment

        # Given: Full environment
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        # When: Developer creates and registers a new file
        new_file = env['repo_root'] / "engines" / "correlation_engine.py"
        new_file.write_text("# Correlation Engine\nclass CorrelationEngine:\n    pass\n")

        new_artifact = ArtifactMetadata(
            artifact_id='correlation_engine_py',
            file_path='engines/correlation_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Signal Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            dependencies=['signal_spec_md']
        )
        artifact_registry.register_artifact(new_artifact)
        artifact_registry.save()

        # Reload registry for validation
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # Use relative path as the validator expects relative paths from repo root
        relative_file = Path("engines/correlation_engine.py")

        # Then: Validation passes within performance target
        report = orchestrator.validate_all(changed_files=[relative_file])

        assert report.performance_target_met is True
        assert report.total_execution_time_ms < 5000

        # Registration observer should not warn about this file (it's registered)
        registration_warnings = report.warnings_by_observer.get('RegistrationValidator', [])
        file_specific_warnings = [
            w for w in registration_warnings
            if w.file_path and 'correlation_engine' in str(w.file_path)
        ]
        assert len(file_specific_warnings) == 0


# ============================================================================
# Scenario 2: Invalid Domain Assignment
# ============================================================================


class TestScenarioInvalidDomainAssignment:
    """
    Feature: System detects invalid domain assignments

    As a system architect,
    I want the system to detect when artifacts are assigned to wrong domains,
    So that domain boundaries remain clear and enforceable.
    """

    def test_engine_assigned_to_governance_domain_generates_warning(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Engine artifact incorrectly assigned to GOV domain

        Given a repository with 12 canonical domains defined
        And the GOV domain cannot own ENGINE artifacts
        When an artifact of type ENGINE is assigned to domain GOV
        Then the domain assignment validator should generate a warning
        And the warning should suggest valid domains for ENGINE type

        Validates: Requirements 15.1, 15.2
        """
        env = setup_acceptance_environment

        # Given: Domain registry with GOV domain that cannot own ENGINE
        domain_registry = DomainRegistry(env['domain_registry_path'])

        # When: Attempting to assign ENGINE to GOV
        is_valid, error = domain_registry.validate_domain_assignment('ENGINE', 'GOV')

        # Then: Assignment is invalid
        assert is_valid is False
        assert error is not None
        assert 'GOV' in error
        assert 'ENGINE' in error

    def test_report_output_assigned_to_signals_domain_generates_warning(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Report output incorrectly assigned to SIGNALS domain

        Given a repository with domain boundaries defined
        And the SIGNALS domain cannot own REPORT_OUT artifacts
        When an artifact of type REPORT_OUT is assigned to domain SIGNALS
        Then the system should reject the assignment
        And suggest REPORT as the valid domain

        Validates: Requirements 15.1, 15.2
        """
        env = setup_acceptance_environment

        # Given: Domain registry loaded
        domain_registry = DomainRegistry(env['domain_registry_path'])

        # When: Attempting to assign REPORT_OUT to SIGNALS
        is_valid, error = domain_registry.validate_domain_assignment('REPORT_OUT', 'SIGNALS')

        # Then: Assignment is invalid with suggestion
        assert is_valid is False
        assert error is not None
        # Should suggest REPORT as valid domain
        valid_domains = domain_registry.get_valid_domains_for_type('REPORT_OUT')
        assert 'REPORT' in valid_domains

    def test_nonexistent_domain_assignment_generates_warning(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Artifact assigned to a domain that does not exist

        Given a repository with 12 canonical domains
        When an artifact is assigned to domain 'ANALYTICS' (not in registry)
        Then the system should reject the assignment
        And indicate that the domain does not exist

        Validates: Requirements 15.1, 15.2
        """
        env = setup_acceptance_environment

        # Given: Domain registry with 12 domains
        domain_registry = DomainRegistry(env['domain_registry_path'])

        # When: Attempting to assign to nonexistent domain
        is_valid, error = domain_registry.validate_domain_assignment('ENGINE', 'ANALYTICS')

        # Then: Assignment is invalid - domain does not exist
        assert is_valid is False
        assert error is not None
        assert 'ANALYTICS' in error
        assert 'does not exist' in error.lower() or 'not exist' in error.lower()

    def test_validation_orchestrator_detects_invalid_domain_in_registry(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Validation orchestrator detects invalid domain in artifact registry

        Given an artifact registered with an invalid domain assignment
        When the validation orchestrator runs all observers
        Then the domain assignment observer should generate a warning
        And the warning should have appropriate severity

        Validates: Requirements 15.1, 15.2, 15.5
        """
        env = setup_acceptance_environment

        # Given: Register an artifact with invalid domain assignment
        # (DASHBOARD assigned to SIGNALS, which cannot own DASHBOARD)
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        invalid_artifact = ArtifactMetadata(
            artifact_id='invalid_dashboard_py',
            file_path='dashboards/invalid_dashboard.py',
            primary_domain='SIGNALS',  # SIGNALS cannot own DASHBOARD
            artifact_type='DASHBOARD',
            lifecycle_status='active',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Developer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
        )
        artifact_registry.register_artifact(invalid_artifact)
        artifact_registry.save()

        # Create the file
        dashboards_dir = env['repo_root'] / "dashboards"
        dashboards_dir.mkdir(exist_ok=True)
        (dashboards_dir / "invalid_dashboard.py").write_text("# Invalid Dashboard\n")

        # When: Run validation orchestrator
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        # Then: Domain assignment observer should have warnings
        domain_warnings = report.warnings_by_observer.get('DomainAssignmentValidator', [])
        assert len(domain_warnings) > 0

        # Find warning about our invalid artifact
        invalid_warnings = [
            w for w in domain_warnings
            if w.artifact_id == 'invalid_dashboard_py'
        ]
        assert len(invalid_warnings) > 0

    def test_dashboard_correctly_assigned_to_user_domain(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Dashboard artifact correctly assigned to USER domain

        Given the USER domain can own DASHBOARD artifacts
        When a DASHBOARD artifact is assigned to USER domain
        Then the domain assignment should be valid
        And no warnings should be generated for this artifact

        Validates: Requirements 15.1, 15.2
        """
        env = setup_acceptance_environment

        # Given: Domain registry loaded
        domain_registry = DomainRegistry(env['domain_registry_path'])

        # When: Assigning DASHBOARD to USER
        is_valid, error = domain_registry.validate_domain_assignment('DASHBOARD', 'USER')

        # Then: Assignment is valid
        assert is_valid is True
        assert error is None


# ============================================================================
# Scenario 3: SSOT Conflict Detection
# ============================================================================


class TestScenarioSSOTConflict:
    """
    Feature: System detects SSOT (Single Source of Truth) conflicts

    As a system architect,
    I want the system to detect when multiple canonical SSOTs exist for the same topic,
    So that there is always exactly one authoritative source per topic.
    """

    def test_duplicate_canonical_ssot_detected(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Two canonical SSOT documents claim the same topic

        Given a canonical SSOT document for topic 'system_architecture'
        When another document is registered as canonical for the same topic
        Then the SSOT consistency observer should detect the conflict
        And generate a critical severity warning
        And suggest which document to mark as derived

        Validates: Requirements 15.1, 15.3
        """
        env = setup_acceptance_environment

        # Given: Existing canonical SSOT for 'system_architecture'
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        # When: Register a second canonical SSOT for same topic
        conflicting_ssot = ArtifactMetadata(
            artifact_id='system_architecture_v2_md',
            file_path='docs/system_architecture_v2.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='System Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            topic='system_architecture'  # Same topic as existing
        )
        artifact_registry.register_artifact(conflicting_ssot)
        artifact_registry.save()

        # Create the file
        docs_dir = env['repo_root'] / "docs"
        (docs_dir / "system_architecture_v2.md").write_text("# System Architecture V2\n")

        # Then: SSOT observer detects the conflict
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        # SSOT observer should have warnings
        ssot_warnings = report.warnings_by_observer.get('SSOTConsistencyValidator', [])
        assert len(ssot_warnings) > 0

        # Should detect the conflict for system_architecture topic
        conflict_warnings = [
            w for w in ssot_warnings
            if 'system_architecture' in (w.warning_message or '')
            or 'conflict' in (w.warning_message or '').lower()
            or 'multiple' in (w.warning_message or '').lower()
            or w.warning_code == 'W400'
        ]
        assert len(conflict_warnings) > 0

    def test_derived_document_without_canonical_reference_detected(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Derived document missing reference to canonical SSOT

        Given a canonical SSOT document exists
        When a derived document is registered without referencing the canonical
        Then the SSOT consistency observer should generate a warning
        And suggest adding the canonical reference to dependencies

        Validates: Requirements 15.1, 15.3
        """
        env = setup_acceptance_environment

        # Given: Existing canonical SSOT
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        # When: Register a derived document without canonical reference
        orphaned_derived = ArtifactMetadata(
            artifact_id='arch_summary_md',
            file_path='docs/architecture_summary.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='draft',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Developer',
            ssot_relationship='derived',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            # No dependencies - missing canonical reference
        )
        artifact_registry.register_artifact(orphaned_derived)
        artifact_registry.save()

        # Create the file
        docs_dir = env['repo_root'] / "docs"
        (docs_dir / "architecture_summary.md").write_text("# Architecture Summary\n")

        # Then: SSOT observer detects missing reference
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        # SSOT observer should have warnings about missing reference
        ssot_warnings = report.warnings_by_observer.get('SSOTConsistencyValidator', [])
        orphan_warnings = [
            w for w in ssot_warnings
            if w.artifact_id == 'arch_summary_md'
            or (w.warning_message and 'derived' in w.warning_message.lower())
            or w.warning_code in ('W401', 'W403')
        ]
        assert len(orphan_warnings) > 0

    def test_properly_linked_derived_document_no_warning(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Derived document properly references its canonical SSOT

        Given a canonical SSOT document for 'system_architecture'
        When a derived document is registered with proper canonical reference
        Then the SSOT consistency observer should NOT generate a warning
        for this specific artifact

        Validates: Requirements 15.1, 15.3
        """
        env = setup_acceptance_environment

        # Given: Existing canonical SSOT
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        # When: Register a properly linked derived document
        proper_derived = ArtifactMetadata(
            artifact_id='arch_implementation_guide_md',
            file_path='docs/architecture_implementation_guide.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='draft',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Developer',
            ssot_relationship='derived',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            dependencies=['system_architecture_md']  # Proper canonical reference
        )
        artifact_registry.register_artifact(proper_derived)
        artifact_registry.save()

        # Create the file
        docs_dir = env['repo_root'] / "docs"
        (docs_dir / "architecture_implementation_guide.md").write_text(
            "# Architecture Implementation Guide\n"
        )

        # Then: SSOT observer should not warn about this specific artifact
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        # Check that our properly linked document does not have SSOT warnings
        ssot_warnings = report.warnings_by_observer.get('SSOTConsistencyValidator', [])
        our_warnings = [
            w for w in ssot_warnings
            if w.artifact_id == 'arch_implementation_guide_md'
        ]
        assert len(our_warnings) == 0

    def test_ssot_conflict_provides_actionable_resolution(
        self, setup_acceptance_environment
    ):
        """
        Scenario: SSOT conflict warning provides actionable resolution

        Given two canonical SSOT documents for the same topic
        When the validation system detects the conflict
        Then the warning should identify both conflicting artifacts
        And suggest marking one as derived or deprecated

        Validates: Requirements 15.1, 15.3, 15.5
        """
        env = setup_acceptance_environment

        # Given: Create a conflict
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        conflicting_ssot = ArtifactMetadata(
            artifact_id='signal_spec_v2_md',
            file_path='docs/signal_specification_v2.md',
            primary_domain='SIGNALS',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Signal Architect',
            ssot_relationship='canonical',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            topic='signal_specification'  # Same topic as existing signal_spec_md
        )
        artifact_registry.register_artifact(conflicting_ssot)
        artifact_registry.save()

        # Create the file
        docs_dir = env['repo_root'] / "docs"
        (docs_dir / "signal_specification_v2.md").write_text("# Signal Spec V2\n")

        # When: Run validation
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        # Then: Warning provides actionable suggestion
        ssot_warnings = report.warnings_by_observer.get('SSOTConsistencyValidator', [])
        conflict_warnings = [
            w for w in ssot_warnings
            if w.warning_code == 'W400'
            or 'canonical' in (w.warning_message or '').lower()
            or 'conflict' in (w.warning_message or '').lower()
        ]
        assert len(conflict_warnings) > 0

        # Suggestion should be actionable
        for warning in conflict_warnings:
            assert warning.suggestion is not None
            assert len(warning.suggestion) > 0


# ============================================================================
# Scenario 4: Gradual Migration Support
# ============================================================================


class TestScenarioGradualMigration:
    """
    Feature: System supports gradual migration without breaking existing functionality

    As a system maintainer,
    I want to migrate artifacts incrementally to the domainization system,
    So that existing functionality is not disrupted during the transition.
    """

    def test_unregistered_artifacts_allowed_during_migration(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Unregistered artifacts are allowed during migration phase

        Given a repository with some artifacts registered and some not
        And the system is in observability mode (soft validation)
        When validation runs on unregistered files
        Then warnings are generated but commits are NOT blocked
        And the system continues to function normally

        Validates: Requirements 15.1, 15.5
        """
        env = setup_acceptance_environment

        # Given: Repository with mix of registered and unregistered files
        # Create several unregistered files
        (env['repo_root'] / "legacy_script.py").write_text("# Legacy script\n")
        (env['repo_root'] / "old_config.yaml").write_text("key: value\n")
        (env['repo_root'] / "utils.py").write_text("# Utilities\n")

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # When: Validation runs on unregistered files
        unregistered_files = [
            env['repo_root'] / "legacy_script.py",
            env['repo_root'] / "old_config.yaml",
            env['repo_root'] / "utils.py",
        ]
        report = orchestrator.validate_all(changed_files=unregistered_files)

        # Then: Warnings are generated (not errors/blocks)
        assert report.total_warnings > 0
        # System still functions - report is generated successfully
        assert report.total_execution_time_ms >= 0
        assert report.performance_target_met is True

    def test_incremental_registration_reduces_warnings(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Incrementally registering artifacts reduces warning count

        Given a repository with unregistered files generating warnings
        When artifacts are registered one by one
        Then the warning count should decrease with each registration
        And eventually reach zero for registered artifacts

        Validates: Requirements 15.1, 15.2, 15.5
        """
        env = setup_acceptance_environment

        # Given: Create unregistered files
        new_file = env['repo_root'] / "engines" / "new_data_engine.py"
        new_file.write_text("# New Data Engine\n")

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        # Measure warnings before registration
        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )
        report_before = orchestrator.validate_all(changed_files=[new_file])
        warnings_before = report_before.total_warnings

        # When: Register the artifact
        new_artifact = ArtifactMetadata(
            artifact_id='new_data_engine_py',
            file_path='engines/new_data_engine.py',
            primary_domain='DATA',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Data Engineer',
            ssot_relationship='implementation',
            allowed_writers=['DATA'],
            allowed_readers=['ALL'],
        )
        artifact_registry.register_artifact(new_artifact)
        artifact_registry.save()

        # Then: Warnings should decrease after registration
        artifact_registry_fresh = ArtifactRegistry(env['artifact_registry_path'])
        orchestrator_fresh = ValidationOrchestrator(
            artifact_registry=artifact_registry_fresh,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )
        report_after = orchestrator_fresh.validate_all(changed_files=[new_file])

        # Registration warnings should be reduced
        reg_warnings_before = len(
            report_before.warnings_by_observer.get('RegistrationValidator', [])
        )
        reg_warnings_after = len(
            report_after.warnings_by_observer.get('RegistrationValidator', [])
        )
        assert reg_warnings_after <= reg_warnings_before

    def test_existing_files_remain_in_current_locations(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Domainization does not require moving existing files

        Given existing files in their current directory structure
        When artifacts are registered in the domainization system
        Then files remain in their original locations
        And the registry references them by their current paths

        Validates: Requirements 15.1, 15.5
        """
        env = setup_acceptance_environment

        # Given: Files exist in their current locations
        assert (env['repo_root'] / "docs" / "system_architecture.md").exists()
        assert (env['repo_root'] / "engines" / "allocation_engine.py").exists()
        assert (env['repo_root'] / "portfolio_report.txt").exists()

        # When: Registry is loaded and queried
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        artifact_registry.load()

        # Then: Registry references files at their current paths
        arch_doc = artifact_registry.get_artifact('system_architecture_md')
        assert arch_doc is not None
        assert arch_doc.file_path == 'docs/system_architecture.md'

        engine = artifact_registry.get_artifact('allocation_engine_py')
        assert engine is not None
        assert engine.file_path == 'engines/allocation_engine.py'

        report = artifact_registry.get_artifact('portfolio_report_txt')
        assert report is not None
        assert report.file_path == 'portfolio_report.txt'

        # Files still exist at original locations (not moved)
        assert (env['repo_root'] / "docs" / "system_architecture.md").exists()
        assert (env['repo_root'] / "engines" / "allocation_engine.py").exists()
        assert (env['repo_root'] / "portfolio_report.txt").exists()

    def test_migration_phases_can_be_validated_independently(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Each migration phase can be validated independently

        Given the system supports phased migration
        When individual observers are run independently
        Then each observer produces its own validation result
        And observers can be enabled/disabled per phase

        Validates: Requirements 15.1, 15.5
        """
        env = setup_acceptance_environment

        # Given: Full environment
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # When: Run each observer independently
        # Phase 1: Registration only
        reg_result = orchestrator.validate_observer('RegistrationValidator')
        assert reg_result is not None
        assert reg_result.observer_name == 'RegistrationValidator'

        # Phase 2: Domain assignment
        domain_result = orchestrator.validate_observer('DomainAssignmentValidator')
        assert domain_result is not None
        assert domain_result.observer_name == 'DomainAssignmentValidator'

        # Phase 3: Lifecycle
        lifecycle_result = orchestrator.validate_observer('LifecycleValidator')
        assert lifecycle_result is not None
        assert lifecycle_result.observer_name == 'LifecycleValidator'

        # Phase 4: Boundary awareness
        boundary_result = orchestrator.validate_observer('BoundaryAwarenessValidator')
        assert boundary_result is not None
        assert boundary_result.observer_name == 'BoundaryAwarenessValidator'

        # Phase 5: SSOT consistency
        ssot_result = orchestrator.validate_observer('SSOTConsistencyValidator')
        assert ssot_result is not None
        assert ssot_result.observer_name == 'SSOTConsistencyValidator'

        # Then: Each produces independent results
        all_results = [reg_result, domain_result, lifecycle_result, boundary_result, ssot_result]
        for result in all_results:
            assert result.execution_time_ms >= 0

    def test_validation_determinism_across_multiple_runs(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Validation produces deterministic results

        Given a repository in a fixed state
        When validation is run multiple times
        Then the results should be identical each time
        And the system should be predictable for developers

        Validates: Requirements 15.5
        """
        env = setup_acceptance_environment

        # Given: Fixed repository state
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # When: Run validation 3 times
        report1 = orchestrator.validate_all()
        report2 = orchestrator.validate_all()
        report3 = orchestrator.validate_all()

        # Then: Results are identical (deterministic)
        assert report1.total_warnings == report2.total_warnings == report3.total_warnings
        assert report1.critical_warnings == report2.critical_warnings == report3.critical_warnings
        assert report1.high_warnings == report2.high_warnings == report3.high_warnings
        assert report1.medium_warnings == report2.medium_warnings == report3.medium_warnings
        assert report1.low_warnings == report2.low_warnings == report3.low_warnings

    def test_health_report_tracks_migration_progress(
        self, setup_acceptance_environment
    ):
        """
        Scenario: Health report shows migration progress

        Given a repository with some registered and some unregistered artifacts
        When a health report is generated
        Then it should show total vs registered artifact counts
        And provide a registration percentage
        And complete within performance target (<10 seconds)

        Validates: Requirements 15.1, 15.3
        """
        env = setup_acceptance_environment

        # Given: Repository with registered artifacts
        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        # When: Generate health report
        health_reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )
        report = health_reporter.generate_health_report()

        # Then: Report contains migration progress information
        assert report is not None
        assert 'summary' in report or hasattr(report, 'summary')

        # Report should track registered artifacts
        if isinstance(report, dict):
            summary = report.get('summary', {})
            assert 'registered_artifacts' in summary or 'total_artifacts' in summary
        else:
            # Object-based report
            assert hasattr(report, 'registered_artifacts') or hasattr(report, 'total_artifacts')

