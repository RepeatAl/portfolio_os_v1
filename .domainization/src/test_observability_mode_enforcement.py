"""
Test Suite: Observability Mode Enforcement

Verifies that ALL observers respect observability mode:
- Generate warnings only (never errors/blocking results)
- Never return blocking behavior
- Commits always proceed
- Violations are logged for visibility

Requirements Validated: 5.9, 5.10, 9.8, 9.9
"""

import pytest
import tempfile
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from observer_registration import RegistrationValidator
from observer_domain_assignment import DomainAssignmentValidator
from observer_lifecycle import LifecycleValidator
from observer_boundary_awareness import BoundaryAwarenessValidator
from observer_ssot_consistency import SSOTConsistencyValidator
from validation_orchestrator import ValidationOrchestrator
from validation_result import ValidationWarning, ValidationResult


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_repo():
    """Create temporary repository structure with registries"""
    temp_dir = tempfile.mkdtemp()
    repo_root = Path(temp_dir)

    # Create .domainization directory
    domainization_dir = repo_root / '.domainization'
    domainization_dir.mkdir()

    # Create minimal artifact registry
    registry_file = domainization_dir / 'artifact_registry.yaml'
    registry_file.write_text('artifacts: []\n')

    # Create minimal domain registry
    domain_registry_file = domainization_dir / 'domain_registry.yaml'
    domain_registry_file.write_text("""domains:
  - domain_id: SIGNALS
    name: Signal Generation
    responsibility_scope: Raw signal generation and data output
    allowed_artifact_types: [ENGINE, DATA_OUT, SSOT, CONFIG]
    cannot_own: [SEMANTIC_STATE, REASONING_OBJECT, REPORT_OUT]
    priority: core
    authority_level: 1
  - domain_id: SEMANTICS
    name: Semantic Interpretation
    responsibility_scope: Semantic interpretation of signals
    allowed_artifact_types: [ENGINE, SSOT, CONFIG]
    cannot_own: [SIGNAL, DATA_OUT, REASONING_OBJECT, REPORT_OUT]
    priority: core
    authority_level: 2
  - domain_id: REASONING
    name: Reasoning Logic
    responsibility_scope: Reasoning and decision logic
    allowed_artifact_types: [ENGINE, SSOT, CONFIG]
    cannot_own: [SIGNAL, DATA_OUT, SEMANTIC_STATE, REPORT_OUT]
    priority: core
    authority_level: 3
  - domain_id: REPORT
    name: Report Generation
    responsibility_scope: Human-readable report generation
    allowed_artifact_types: [ENGINE, REPORT_OUT, SSOT, CONFIG]
    cannot_own: [SIGNAL, DATA_OUT, SEMANTIC_STATE, REASONING_OBJECT]
    priority: core
    authority_level: 4
  - domain_id: ARCH
    name: Architecture
    responsibility_scope: System architecture and design
    allowed_artifact_types: [SSOT, ENGINE, CONFIG, STEERING]
    cannot_own: []
    priority: surface
  - domain_id: DATA
    name: Data Management
    responsibility_scope: Data ingestion and normalization
    allowed_artifact_types: [ENGINE, DATA_IN, DATA_OUT, SSOT, CONFIG]
    cannot_own: []
    priority: surface
  - domain_id: GOV
    name: Governance
    responsibility_scope: System governance and policies
    allowed_artifact_types: [SSOT, CONFIG, STEERING]
    cannot_own: []
    priority: surface
  - domain_id: STATE
    name: Portfolio State
    responsibility_scope: Portfolio state management
    allowed_artifact_types: [DATA_IN, DATA_OUT, SSOT, CONFIG]
    cannot_own: []
    priority: surface
  - domain_id: USER
    name: User Interface
    responsibility_scope: User-facing dashboards and interfaces
    allowed_artifact_types: [DASHBOARD, CONFIG, SSOT]
    cannot_own: []
    priority: surface
  - domain_id: DEPLOY
    name: Deployment
    responsibility_scope: Deployment and infrastructure
    allowed_artifact_types: [RUNTIME, CONFIG, SSOT]
    cannot_own: []
    priority: surface
  - domain_id: MEMORY
    name: Portfolio Memory
    responsibility_scope: Historical data and snapshots
    allowed_artifact_types: [SNAPSHOT, DATA_IN, SSOT, CONFIG]
    cannot_own: []
    priority: surface
  - domain_id: SIM
    name: Simulation
    responsibility_scope: Scenario simulation
    allowed_artifact_types: [ENGINE, SSOT, CONFIG]
    cannot_own: []
    priority: surface
""")

    # Create minimal lifecycle state machine
    lifecycle_file = domainization_dir / 'lifecycle_state_machine.yaml'
    lifecycle_file.write_text("""artifact_types:
  SSOT:
    description: Single Source of Truth documents
    states: [draft, review, canonical, deprecated]
    initial_state: draft
    modifiable_states: [draft, review, canonical]
    read_only_states: [deprecated]
    transitions:
      - from: draft
        to: review
        condition: Author completes initial version
      - from: review
        to: canonical
        condition: Domain owner approves
      - from: canonical
        to: draft
        condition: Revision required
      - from: canonical
        to: deprecated
        condition: Superseded by new version
  ENGINE:
    description: Processing engines
    states: [planned, development, active, deprecated]
    initial_state: planned
    modifiable_states: [planned, development, active]
    read_only_states: [deprecated]
    transitions:
      - from: planned
        to: development
        condition: Implementation begins
      - from: development
        to: active
        condition: Production ready
      - from: development
        to: development
        condition: Iteration allowed
      - from: active
        to: deprecated
        condition: Replaced by new engine
  REPORT_OUT:
    description: Report output files
    states: [generated, current, archived]
    initial_state: generated
    modifiable_states: [generated, current]
    read_only_states: [archived]
    transitions:
      - from: generated
        to: current
        condition: Becomes latest version
      - from: current
        to: archived
        condition: Superseded by newer report
  DATA_OUT:
    description: Data output files
    states: [generated, current, archived]
    initial_state: generated
    modifiable_states: [generated, current]
    read_only_states: [archived]
    transitions:
      - from: generated
        to: current
        condition: Becomes latest version
      - from: current
        to: archived
        condition: Superseded by newer data
  DATA_IN:
    description: Data input files
    states: [active, stale, archived]
    initial_state: active
    modifiable_states: [active, stale]
    read_only_states: [archived]
    transitions:
      - from: active
        to: stale
        condition: Data becomes outdated
      - from: stale
        to: archived
        condition: Moved to historical storage
""")

    yield repo_root

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def artifact_registry(temp_repo):
    """Create artifact registry"""
    registry_path = temp_repo / '.domainization' / 'artifact_registry.yaml'
    registry = ArtifactRegistry(registry_path)
    registry.load()
    return registry


@pytest.fixture
def domain_registry(temp_repo):
    """Create domain registry"""
    registry_path = temp_repo / '.domainization' / 'domain_registry.yaml'
    registry = DomainRegistry(registry_path)
    registry.load()
    return registry


@pytest.fixture
def lifecycle_manager(temp_repo):
    """Create lifecycle manager"""
    lifecycle_path = temp_repo / '.domainization' / 'lifecycle_state_machine.yaml'
    manager = LifecycleManager(lifecycle_path)
    manager.load()
    return manager


@pytest.fixture
def orchestrator(artifact_registry, domain_registry, lifecycle_manager, temp_repo):
    """Create validation orchestrator"""
    return ValidationOrchestrator(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=temp_repo
    )


def _register_test_artifact(registry, artifact_id='test_engine_py',
                            file_path='engines/test_engine.py',
                            primary_domain='SIGNALS',
                            artifact_type='ENGINE',
                            lifecycle_status='active',
                            ssot_relationship='implementation',
                            allowed_writers=None,
                            dependencies=None,
                            topic=None):
    """Helper to register a test artifact"""
    metadata = ArtifactMetadata(
        artifact_id=artifact_id,
        file_path=file_path,
        primary_domain=primary_domain,
        artifact_type=artifact_type,
        lifecycle_status=lifecycle_status,
        created_date='2026-01-01',
        last_modified='2026-01-01',
        owner_role='Test Engineer',
        ssot_relationship=ssot_relationship,
        allowed_writers=allowed_writers or [primary_domain],
        allowed_readers=['ALL'],
        dependencies=dependencies,
        topic=topic
    )
    registry.register_artifact(metadata)
    return metadata


# =============================================================================
# Test Class: Observer 1 - Registration Validator (Observability Mode)
# =============================================================================


class TestRegistrationValidatorObservabilityMode:
    """
    Verify RegistrationValidator generates warnings only, never blocks.
    
    Validates: Requirements 5.9, 5.10, 9.8
    """

    def test_unregistered_artifact_produces_warning_not_error(self, temp_repo, artifact_registry):
        """Unregistered artifacts produce warnings, not blocking errors"""
        validator = RegistrationValidator(artifact_registry, temp_repo)

        # Create unregistered file
        test_file = temp_repo / 'unregistered_file.py'
        test_file.write_text('# Unregistered file\n')

        result = validator.validate([Path('unregistered_file.py')])

        # Must produce warnings, not errors
        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        for warning in result.warnings:
            assert isinstance(warning, ValidationWarning)
            assert warning.severity in ('critical', 'high', 'medium', 'low')
            # Warnings are never "error" severity
            assert warning.severity != 'error'

    def test_missing_metadata_produces_warning_not_block(self, temp_repo, artifact_registry):
        """Missing metadata produces warning, commit is not blocked"""
        validator = RegistrationValidator(artifact_registry, temp_repo)

        # Create markdown without frontmatter
        test_file = temp_repo / 'no_metadata.md'
        test_file.write_text('# No Metadata\n\nContent.\n')

        result = validator.validate([Path('no_metadata.md')])

        # Result is always non-blocking (ValidationResult has no success=False)
        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        # No blocking mechanism exists
        assert not hasattr(result, 'success') or not hasattr(result, 'blocked')

    def test_invalid_metadata_produces_warning_not_block(self, temp_repo, artifact_registry):
        """Invalid metadata schema produces warning, not blocking"""
        validator = RegistrationValidator(artifact_registry, temp_repo)

        # Create markdown with incomplete frontmatter
        test_file = temp_repo / 'incomplete.md'
        test_file.write_text('---\nartifact_id: incomplete_md\n---\n# Incomplete\n')

        result = validator.validate([Path('incomplete.md')])

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        # Warnings have suggestion field for visibility
        for warning in result.warnings:
            assert warning.suggestion is not None
            assert len(warning.suggestion) > 0

    def test_violations_are_logged_for_visibility(self, temp_repo, artifact_registry):
        """All violations are captured in warnings list for visibility"""
        validator = RegistrationValidator(artifact_registry, temp_repo)

        # Create multiple unregistered files
        for i in range(3):
            test_file = temp_repo / f'unregistered_{i}.py'
            test_file.write_text(f'# File {i}\n')

        files = [Path(f'unregistered_{i}.py') for i in range(3)]
        result = validator.validate(files)

        # All violations are visible in warnings
        assert len(result.warnings) == 3
        for warning in result.warnings:
            assert warning.observer_name == 'RegistrationValidator'
            assert warning.warning_code is not None
            assert warning.warning_message is not None


# =============================================================================
# Test Class: Observer 2 - Domain Assignment Validator (Observability Mode)
# =============================================================================


class TestDomainAssignmentValidatorObservabilityMode:
    """
    Verify DomainAssignmentValidator generates warnings only, never blocks.
    
    Validates: Requirements 5.9, 5.10, 9.8
    """

    def test_invalid_domain_produces_warning_not_error(self, artifact_registry, domain_registry):
        """Invalid domain assignment produces warning, not blocking error"""
        validator = DomainAssignmentValidator(artifact_registry, domain_registry)

        # Register artifact with invalid domain
        _register_test_artifact(
            artifact_registry,
            artifact_id='bad_domain_artifact',
            file_path='bad_domain.py',
            primary_domain='NONEXISTENT_DOMAIN'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        for warning in result.warnings:
            assert isinstance(warning, ValidationWarning)
            assert warning.severity != 'error'

    def test_domain_cannot_own_type_produces_warning(self, artifact_registry, domain_registry):
        """Domain that cannot own artifact type produces warning, not block"""
        validator = DomainAssignmentValidator(artifact_registry, domain_registry)

        # Register artifact with wrong domain-type combination
        # USER domain cannot own ENGINE type
        _register_test_artifact(
            artifact_registry,
            artifact_id='wrong_type_artifact',
            file_path='wrong_type.py',
            primary_domain='USER',
            artifact_type='ENGINE'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        # Warning provides suggestion for valid domains
        assert any('suggestion' in dir(w) and w.suggestion for w in result.warnings)

    def test_valid_domain_assignment_no_warnings(self, artifact_registry, domain_registry):
        """Valid domain assignment produces no warnings"""
        validator = DomainAssignmentValidator(artifact_registry, domain_registry)

        # Register artifact with valid domain-type combination
        _register_test_artifact(
            artifact_registry,
            artifact_id='valid_artifact',
            file_path='valid_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert not result.has_warnings()


# =============================================================================
# Test Class: Observer 3 - Lifecycle Validator (Observability Mode)
# =============================================================================


class TestLifecycleValidatorObservabilityMode:
    """
    Verify LifecycleValidator generates warnings only, never blocks.
    
    Validates: Requirements 5.9, 5.10, 9.8
    """

    def test_invalid_transition_produces_warning_not_block(self, artifact_registry, lifecycle_manager):
        """Invalid lifecycle transition produces warning, not blocking"""
        validator = LifecycleValidator(artifact_registry, lifecycle_manager)

        # Register artifact
        _register_test_artifact(
            artifact_registry,
            artifact_id='lifecycle_test',
            file_path='lifecycle_test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active'
        )

        # Simulate invalid transition (active -> planned is not valid)
        previous_states = {'lifecycle_test': 'active'}
        # Update the artifact to have an invalid new state
        artifact_registry._artifacts['lifecycle_test'].lifecycle_status = 'planned'

        result = validator.validate(
            changed_files=[Path('lifecycle_test.py')],
            previous_states=previous_states
        )

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        for warning in result.warnings:
            assert isinstance(warning, ValidationWarning)
            assert warning.severity != 'error'

    def test_deprecated_modification_produces_warning_not_block(self, artifact_registry, lifecycle_manager, temp_repo):
        """Modifying deprecated artifact produces warning, not blocking"""
        validator = LifecycleValidator(artifact_registry, lifecycle_manager)

        # Register deprecated artifact
        _register_test_artifact(
            artifact_registry,
            artifact_id='deprecated_artifact',
            file_path='deprecated.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='deprecated'
        )

        # Create the file
        (temp_repo / 'deprecated.py').write_text('# deprecated\n')

        result = validator.validate(
            changed_files=[Path('deprecated.py')]
        )

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        # Warning about deprecated modification
        deprecated_warnings = [w for w in result.warnings if 'deprecated' in w.warning_message.lower() or w.warning_code == 'W201']
        assert len(deprecated_warnings) > 0

    def test_valid_transition_no_warnings(self, artifact_registry, lifecycle_manager):
        """Valid lifecycle transition produces no warnings"""
        validator = LifecycleValidator(artifact_registry, lifecycle_manager)

        # Register artifact
        _register_test_artifact(
            artifact_registry,
            artifact_id='valid_transition',
            file_path='valid_transition.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active'
        )

        # Simulate valid transition (development -> active)
        previous_states = {'valid_transition': 'development'}

        result = validator.validate(
            changed_files=[Path('valid_transition.py')],
            previous_states=previous_states
        )

        assert isinstance(result, ValidationResult)
        assert not result.has_warnings()


# =============================================================================
# Test Class: Observer 4 - Boundary Awareness Validator (Observability Mode)
# =============================================================================


class TestBoundaryAwarenessValidatorObservabilityMode:
    """
    Verify BoundaryAwarenessValidator generates warnings only, never blocks.
    
    Validates: Requirements 5.9, 5.10, 9.8, 9.9
    """

    def test_authority_chain_violation_produces_warning_not_block(self, artifact_registry, domain_registry):
        """Authority chain violation produces warning, not blocking"""
        validator = BoundaryAwarenessValidator(artifact_registry, domain_registry)

        # Register artifact that violates authority chain
        # SIGNALS domain writing a REPORT_OUT artifact
        _register_test_artifact(
            artifact_registry,
            artifact_id='signals_report_violation',
            file_path='signals_report.txt',
            primary_domain='SIGNALS',
            artifact_type='REPORT_OUT'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        for warning in result.warnings:
            assert isinstance(warning, ValidationWarning)
            assert warning.severity != 'error'

    def test_cross_domain_write_produces_warning_not_block(self, artifact_registry, domain_registry, temp_repo):
        """Cross-domain write attempt produces warning, not blocking"""
        validator = BoundaryAwarenessValidator(artifact_registry, domain_registry)

        # Register artifact owned by SIGNALS
        _register_test_artifact(
            artifact_registry,
            artifact_id='signals_owned',
            file_path='signals_owned.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            allowed_writers=['SIGNALS']
        )

        # Create the file
        (temp_repo / 'signals_owned.py').write_text('# signals\n')

        # Validate with REPORT domain as modifier (not in allowed_writers)
        result = validator.validate(
            changed_files=[Path('signals_owned.py')],
            modifier_domain='REPORT'
        )

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        cross_domain_warnings = [w for w in result.warnings if w.warning_code == 'W305']
        assert len(cross_domain_warnings) > 0

    def test_valid_boundary_no_warnings(self, artifact_registry, domain_registry):
        """Valid boundary usage produces no warnings"""
        validator = BoundaryAwarenessValidator(artifact_registry, domain_registry)

        # Register artifact with correct domain-type combination
        _register_test_artifact(
            artifact_registry,
            artifact_id='valid_boundary',
            file_path='valid_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert not result.has_warnings()


# =============================================================================
# Test Class: Observer 5 - SSOT Consistency Validator (Observability Mode)
# =============================================================================


class TestSSOTConsistencyValidatorObservabilityMode:
    """
    Verify SSOTConsistencyValidator generates warnings only, never blocks.
    
    Validates: Requirements 5.9, 5.10, 9.8
    """

    def test_multiple_canonical_ssot_produces_warning_not_block(self, artifact_registry):
        """Multiple canonical SSOTs for same topic produces warning, not blocking"""
        validator = SSOTConsistencyValidator(artifact_registry)

        # Register two canonical SSOTs for same topic
        _register_test_artifact(
            artifact_registry,
            artifact_id='ssot_1',
            file_path='docs/ssot_1.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            ssot_relationship='canonical',
            topic='system_architecture'
        )
        _register_test_artifact(
            artifact_registry,
            artifact_id='ssot_2',
            file_path='docs/ssot_2.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            ssot_relationship='canonical',
            topic='system_architecture'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        # Critical severity but still just a warning, not blocking
        critical_warnings = result.get_critical_warnings()
        assert len(critical_warnings) > 0
        for warning in critical_warnings:
            assert isinstance(warning, ValidationWarning)
            assert warning.severity == 'critical'
            # Still a warning, not an error that blocks

    def test_missing_ssot_reference_produces_warning_not_block(self, artifact_registry):
        """Missing SSOT reference produces warning, not blocking"""
        validator = SSOTConsistencyValidator(artifact_registry)

        # Register derived artifact without dependencies
        _register_test_artifact(
            artifact_registry,
            artifact_id='derived_no_ref',
            file_path='docs/derived.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            ssot_relationship='derived',
            dependencies=None
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert result.has_warnings()
        for warning in result.warnings:
            assert isinstance(warning, ValidationWarning)
            assert warning.severity != 'error'

    def test_valid_ssot_no_warnings(self, artifact_registry):
        """Valid SSOT relationships produce no warnings"""
        validator = SSOTConsistencyValidator(artifact_registry)

        # Register single canonical SSOT
        _register_test_artifact(
            artifact_registry,
            artifact_id='valid_ssot',
            file_path='docs/valid_ssot.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            ssot_relationship='canonical',
            topic='unique_topic'
        )

        result = validator.validate()

        assert isinstance(result, ValidationResult)
        assert not result.has_warnings()


# =============================================================================
# Test Class: Validation Orchestrator (Observability Mode)
# =============================================================================


class TestValidationOrchestratorObservabilityMode:
    """
    Verify ValidationOrchestrator never blocks in observability mode.
    
    Validates: Requirements 5.9, 5.10, 9.8, 9.9
    """

    def test_orchestrator_never_blocks_with_violations(self, orchestrator, artifact_registry, temp_repo):
        """Orchestrator never blocks even with multiple violations"""
        # Create violations: unregistered file
        test_file = temp_repo / 'unregistered.py'
        test_file.write_text('# unregistered\n')

        # Register artifact with invalid domain
        _register_test_artifact(
            artifact_registry,
            artifact_id='bad_domain',
            file_path='bad_domain.py',
            primary_domain='NONEXISTENT'
        )

        report = orchestrator.validate_all(
            changed_files=[Path('unregistered.py'), Path('bad_domain.py')]
        )

        # Report is generated (not an exception or blocking result)
        assert report is not None
        assert report.total_warnings > 0
        # No blocking mechanism in ObservabilityReport
        assert not hasattr(report, 'blocked')
        assert not hasattr(report, 'success')

    def test_orchestrator_returns_report_not_exception(self, orchestrator, temp_repo):
        """Orchestrator returns report, never raises blocking exceptions"""
        # Create file that triggers warnings
        test_file = temp_repo / 'trigger_warnings.py'
        test_file.write_text('# trigger\n')

        # Should not raise any exception
        report = orchestrator.validate_all(
            changed_files=[Path('trigger_warnings.py')]
        )

        assert report is not None
        assert hasattr(report, 'total_warnings')
        assert hasattr(report, 'warnings_by_observer')

    def test_orchestrator_all_observers_produce_warnings_only(self, orchestrator, artifact_registry, temp_repo):
        """All observers in orchestrator produce warnings, never errors"""
        # Create various violations
        test_file = temp_repo / 'multi_violation.py'
        test_file.write_text('# multi violation\n')

        # Register artifact with issues
        _register_test_artifact(
            artifact_registry,
            artifact_id='multi_issue',
            file_path='multi_issue.py',
            primary_domain='SIGNALS',
            artifact_type='REPORT_OUT',  # Wrong type for SIGNALS
            lifecycle_status='active',
            ssot_relationship='derived',
            dependencies=None  # Missing SSOT reference
        )

        report = orchestrator.validate_all()

        # All warnings from all observers are ValidationWarning instances
        for observer_name, warnings in report.warnings_by_observer.items():
            for warning in warnings:
                assert isinstance(warning, ValidationWarning), \
                    f"Observer {observer_name} produced non-warning result"
                assert warning.severity in ('critical', 'high', 'medium', 'low'), \
                    f"Observer {observer_name} produced invalid severity: {warning.severity}"

    def test_orchestrator_performance_target_tracked(self, orchestrator):
        """Orchestrator tracks performance target (< 5 seconds)"""
        report = orchestrator.validate_all()

        assert hasattr(report, 'performance_target_met')
        assert hasattr(report, 'total_execution_time_ms')
        # Should complete well under 5 seconds for empty registry
        assert report.performance_target_met is True

    def test_orchestrator_report_string_shows_observability_mode(self, orchestrator):
        """Orchestrator report string indicates observability mode"""
        report = orchestrator.validate_all()
        report_str = str(report)

        assert 'OBSERVABILITY' in report_str.upper()
        assert 'warnings only' in report_str.lower() or 'no blocking' in report_str.lower()


# =============================================================================
# Test Class: Pre-Commit Hook (Never Blocks)
# =============================================================================


class TestPreCommitHookObservabilityMode:
    """
    Verify pre-commit hook never blocks commits.
    
    Validates: Requirements 5.9, 5.10, 9.8, 9.9
    """

    def test_pre_commit_hook_always_exits_zero(self):
        """Pre-commit hook script always exits with code 0"""
        hook_path = Path(__file__).parent.parent / 'hooks' / 'pre-commit'

        # Read the hook script
        assert hook_path.exists(), f"Pre-commit hook not found at {hook_path}"
        hook_content = hook_path.read_text()

        # Verify the hook always exits 0
        # The last exit command should be 'exit 0'
        lines = hook_content.strip().split('\n')
        last_exit_line = None
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.startswith('exit'):
                last_exit_line = stripped
                break

        assert last_exit_line == 'exit 0', \
            f"Pre-commit hook does not end with 'exit 0'. Found: {last_exit_line}"

    def test_pre_commit_hook_contains_no_exit_one(self):
        """Pre-commit hook never exits with code 1 (blocking)"""
        hook_path = Path(__file__).parent.parent / 'hooks' / 'pre-commit'
        hook_content = hook_path.read_text()

        # Check that no 'exit 1' exists in the script
        lines = hook_content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Skip comments
            if stripped.startswith('#'):
                continue
            assert 'exit 1' not in stripped, \
                f"Pre-commit hook has blocking 'exit 1' at line {i}: {stripped}"

    def test_pre_commit_hook_documents_non_blocking_behavior(self):
        """Pre-commit hook documents that it never blocks"""
        hook_path = Path(__file__).parent.parent / 'hooks' / 'pre-commit'
        hook_content = hook_path.read_text()

        # Should document non-blocking behavior
        assert 'never block' in hook_content.lower() or 'NEVER blocks' in hook_content, \
            "Pre-commit hook should document non-blocking behavior"

    def test_pre_commit_hook_mentions_observability(self):
        """Pre-commit hook mentions observability mode"""
        hook_path = Path(__file__).parent.parent / 'hooks' / 'pre-commit'
        hook_content = hook_path.read_text()

        assert 'observability' in hook_content.lower() or 'OBSERVABILITY' in hook_content, \
            "Pre-commit hook should mention observability mode"

    def test_pre_commit_hook_python_script_exits_zero(self):
        """Embedded Python script in hook always exits 0"""
        hook_path = Path(__file__).parent.parent / 'hooks' / 'pre-commit'
        hook_content = hook_path.read_text()

        # The embedded Python script should exit 0
        assert 'sys.exit(0)' in hook_content, \
            "Embedded Python script should always sys.exit(0)"

        # Should NOT have sys.exit(1) in the Python section
        # Find the Python script section
        in_python = False
        for line in hook_content.split('\n'):
            if 'PYTHON_SCRIPT' in line and not in_python:
                in_python = True
                continue
            if 'PYTHON_SCRIPT' in line and in_python:
                break
            if in_python and 'sys.exit(1)' in line:
                pytest.fail("Embedded Python script has blocking sys.exit(1)")


# =============================================================================
# Test Class: Validation Result Schema (Observability Design)
# =============================================================================


class TestValidationResultSchemaObservability:
    """
    Verify the ValidationResult schema is designed for observability only.
    
    Validates: Requirements 5.9, 5.10, 9.8, 9.9
    """

    def test_validation_result_has_no_blocking_field(self):
        """ValidationResult has no 'success' or 'blocked' field that could block"""
        result = ValidationResult(
            observer_name='TestObserver',
            warnings=[],
            execution_time_ms=1.0
        )

        # ValidationResult should not have blocking semantics
        assert not hasattr(result, 'success')
        assert not hasattr(result, 'blocked')
        assert not hasattr(result, 'error')

    def test_validation_warning_is_always_non_blocking(self):
        """ValidationWarning is inherently non-blocking by design"""
        warning = ValidationWarning(
            observer_name='TestObserver',
            artifact_id='test_artifact',
            file_path='test.py',
            warning_code='W001',
            warning_message='Test warning',
            suggestion='Fix this',
            severity='critical'
        )

        # Even critical severity is still a warning, not a block
        assert warning.severity == 'critical'
        assert not hasattr(warning, 'blocking')
        assert not hasattr(warning, 'error')

    def test_warning_severity_levels_are_all_non_blocking(self):
        """All severity levels (critical, high, medium, low) are non-blocking"""
        valid_severities = ['critical', 'high', 'medium', 'low']

        for severity in valid_severities:
            warning = ValidationWarning(
                observer_name='TestObserver',
                artifact_id='test',
                file_path='test.py',
                warning_code='W001',
                warning_message='Test',
                suggestion='Fix',
                severity=severity
            )
            # All are warnings, none are errors
            assert 'error' not in type(warning).__name__.lower()
            assert isinstance(warning, ValidationWarning)


# =============================================================================
# Test Class: Config-Driven Enforcement Mode
# =============================================================================


class TestConfigDrivenEnforcementMode:
    """
    Verify config.yaml enforcement_mode is respected.
    
    Validates: Requirements 5.9, 5.10, 9.8, 9.9
    """

    def test_config_specifies_observability_mode(self):
        """Config file specifies enforcement_mode as observability"""
        import yaml

        config_path = Path(__file__).parent.parent / 'config.yaml'
        assert config_path.exists(), "Config file not found"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config['enforcement_mode'] == 'observability', \
            f"Expected enforcement_mode='observability', got '{config['enforcement_mode']}'"

    def test_config_specifies_fast_lane_phase(self):
        """Config file specifies current_phase as fast_lane_report_mvp"""
        import yaml

        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config['current_phase'] == 'fast_lane_report_mvp', \
            f"Expected current_phase='fast_lane_report_mvp', got '{config['current_phase']}'"

    def test_config_commit_gates_deferred(self):
        """Config documents that commit gates are deferred (Req 5.9)"""
        import yaml

        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config['fast_lane_rules']['commit_gates_deferred'] is True

    def test_config_report_development_unblocked(self):
        """Config documents that report development is unblocked (Req 5.10)"""
        import yaml

        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config['fast_lane_rules']['report_development_unblocked'] is True

    def test_config_registry_soft_validation_only(self):
        """Config documents registry is soft-validation only (Req 9.8)"""
        import yaml

        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config['fast_lane_rules']['registry_soft_validation_only'] is True

    def test_all_observers_enabled_in_config(self):
        """All 5 observers are enabled in config"""
        import yaml

        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        observers = config['observers']
        expected_observers = [
            'RegistrationValidator',
            'DomainAssignmentValidator',
            'LifecycleValidator',
            'BoundaryAwarenessValidator',
            'SSOTConsistencyValidator'
        ]

        for observer_name in expected_observers:
            assert observer_name in observers, f"Observer {observer_name} not in config"
            assert observers[observer_name]['enabled'] is True, \
                f"Observer {observer_name} is not enabled"


# =============================================================================
# Test Class: Observability Report Format
# =============================================================================


class TestObservabilityReportFormat:
    """
    Verify ObservabilityReport communicates warnings clearly.
    
    Validates: Requirements 5.9, 9.8
    """

    def test_report_shows_warning_counts_by_severity(self, orchestrator):
        """Report shows warning counts by severity level"""
        report = orchestrator.validate_all()

        assert hasattr(report, 'critical_warnings')
        assert hasattr(report, 'high_warnings')
        assert hasattr(report, 'medium_warnings')
        assert hasattr(report, 'low_warnings')
        assert hasattr(report, 'total_warnings')

    def test_report_groups_warnings_by_observer(self, orchestrator):
        """Report groups warnings by observer for visibility"""
        report = orchestrator.validate_all()

        assert hasattr(report, 'warnings_by_observer')
        assert isinstance(report.warnings_by_observer, dict)

        # Should have entries for all 5 observers
        expected_observers = [
            'RegistrationValidator',
            'DomainAssignmentValidator',
            'LifecycleValidator',
            'BoundaryAwarenessValidator',
            'SSOTConsistencyValidator'
        ]
        for observer_name in expected_observers:
            assert observer_name in report.warnings_by_observer

    def test_report_tracks_execution_time(self, orchestrator):
        """Report tracks execution time for performance monitoring"""
        report = orchestrator.validate_all()

        assert hasattr(report, 'total_execution_time_ms')
        assert report.total_execution_time_ms >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
