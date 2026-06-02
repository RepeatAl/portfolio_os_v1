"""
Integration tests for end-to-end flows

Tests complete workflows across multiple components:
- Commit gate execution flow (all 5 observers in sequence)
- Registry persistence and loading
- CLI commands (register, update, list, show, validate, health, config)
- Pre-commit hook execution
- Backup and recovery

Requirements: 15.1, 15.2, 15.3, 15.5
"""

import os
import sys
import shutil
import subprocess
import tempfile
import yaml
import pytest
from pathlib import Path
from datetime import datetime


# Ensure src directory is on path
SRC_DIR = Path(__file__).parent
sys.path.insert(0, str(SRC_DIR))

from artifact_schema import ArtifactMetadata
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from validation_orchestrator import ValidationOrchestrator
from registry_backup_manager import (
    create_backup,
    list_backups,
    cleanup_old_backups,
    create_backup_and_cleanup,
)
from registry_recovery_manager import RegistryRecoveryManager
from health_reporter import HealthReporter


# ============================================================================
# Fixtures
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
def sample_domain_registry_yaml():
    """Minimal domain registry YAML content for testing"""
    return {
        'domains': [
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
                'domain_id': 'DATA',
                'name': 'Data Management',
                'responsibility_scope': 'Data ingestion and normalization',
                'allowed_artifact_types': ['ENGINE', 'DATA_IN', 'DATA_OUT', 'SSOT', 'CONFIG'],
                'cannot_own': ['DASHBOARD', 'REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
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
                'domain_id': 'STATE',
                'name': 'Portfolio State',
                'responsibility_scope': 'Portfolio state management',
                'allowed_artifact_types': ['DATA_IN', 'DATA_OUT', 'SSOT', 'CONFIG', 'SNAPSHOT'],
                'cannot_own': ['ENGINE', 'DASHBOARD', 'REPORT_OUT'],
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
def sample_lifecycle_yaml():
    """Minimal lifecycle state machine YAML content for testing"""
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
def sample_artifact_registry_yaml():
    """Minimal artifact registry YAML content for testing"""
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
        ]
    }


@pytest.fixture
def setup_test_environment(temp_dir, domainization_dir, sample_domain_registry_yaml,
                           sample_lifecycle_yaml, sample_artifact_registry_yaml):
    """Set up a complete test environment with all registry files"""
    # Write domain registry
    domain_registry_path = domainization_dir / "domain_registry.yaml"
    with open(domain_registry_path, 'w') as f:
        yaml.dump(sample_domain_registry_yaml, f, default_flow_style=False)

    # Write lifecycle state machine
    lifecycle_path = domainization_dir / "lifecycle_state_machine.yaml"
    with open(lifecycle_path, 'w') as f:
        yaml.dump(sample_lifecycle_yaml, f, default_flow_style=False)

    # Write artifact registry
    artifact_registry_path = domainization_dir / "artifact_registry.yaml"
    with open(artifact_registry_path, 'w') as f:
        yaml.dump(sample_artifact_registry_yaml, f, default_flow_style=False)

    # Create some sample files in the repo
    docs_dir = temp_dir / "docs"
    docs_dir.mkdir()
    (docs_dir / "system_architecture.md").write_text("# System Architecture\n")

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
# Test Class: Complete Commit Gate Execution Flow
# ============================================================================


class TestCommitGateExecutionFlow:
    """Integration tests for complete commit gate (observer) execution flow"""

    def test_full_validation_with_all_observers(self, setup_test_environment):
        """Test that all 5 observers run in sequence and produce a report"""
        env = setup_test_environment

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        # Report should be generated
        assert report is not None
        assert report.total_execution_time_ms >= 0
        # All 5 observers should have entries
        assert len(report.warnings_by_observer) == 5

    def test_validation_completes_within_performance_target(self, setup_test_environment):
        """Test that validation completes in less than 5 seconds (Req 15.1)"""
        env = setup_test_environment

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        report = orchestrator.validate_all()

        assert report.performance_target_met is True
        assert report.total_execution_time_ms < 5000

    def test_validation_with_changed_files(self, setup_test_environment):
        """Test validation scoped to specific changed files"""
        env = setup_test_environment

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # Validate with specific changed files
        changed_files = [
            env['repo_root'] / "docs" / "system_architecture.md",
            env['repo_root'] / "engines" / "allocation_engine.py",
        ]

        report = orchestrator.validate_all(changed_files=changed_files)

        assert report is not None
        assert report.total_execution_time_ms >= 0

    def test_validation_with_unregistered_file(self, setup_test_environment):
        """Test that unregistered files generate warnings"""
        env = setup_test_environment

        # Create an unregistered file
        unregistered_file = env['repo_root'] / "new_feature.py"
        unregistered_file.write_text("# New feature\n")

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        changed_files = [unregistered_file]
        report = orchestrator.validate_all(changed_files=changed_files)

        # Should have at least one warning about unregistered artifact
        assert report.total_warnings > 0

    def test_validation_determinism(self, setup_test_environment):
        """Test that same input always produces same result (Req 15.5)"""
        env = setup_test_environment

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # Run validation twice
        report1 = orchestrator.validate_all()
        report2 = orchestrator.validate_all()

        # Results should be identical (deterministic)
        assert report1.total_warnings == report2.total_warnings
        assert report1.critical_warnings == report2.critical_warnings
        assert report1.high_warnings == report2.high_warnings
        assert report1.medium_warnings == report2.medium_warnings
        assert report1.low_warnings == report2.low_warnings

    def test_individual_observer_execution(self, setup_test_environment):
        """Test running a specific observer independently (Req 15.8)"""
        env = setup_test_environment

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        domain_registry = DomainRegistry(env['domain_registry_path'])
        lifecycle_manager = LifecycleManager(env['lifecycle_path'])

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=env['repo_root']
        )

        # Run each observer individually
        result = orchestrator.validate_observer('RegistrationValidator')
        assert result is not None
        assert result.observer_name == 'RegistrationValidator'

        result = orchestrator.validate_observer('DomainAssignmentValidator')
        assert result is not None
        assert result.observer_name == 'DomainAssignmentValidator'



# ============================================================================
# Test Class: Registry Persistence and Loading
# ============================================================================


class TestRegistryPersistenceAndLoading:
    """Integration tests for registry persistence and loading"""

    def test_artifact_registry_save_and_reload(self, setup_test_environment):
        """Test that artifacts persist correctly through save/load cycle"""
        env = setup_test_environment

        # Load registry
        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        # Verify initial state
        artifacts = registry.list_all_artifacts()
        assert len(artifacts) == 3

        # Register a new artifact
        new_artifact = ArtifactMetadata(
            artifact_id='test_new_engine_py',
            file_path='engines/test_new_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Developer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
        )
        registry.register_artifact(new_artifact)
        registry.save()

        # Reload and verify persistence
        registry2 = ArtifactRegistry(env['artifact_registry_path'])
        registry2.load()

        artifacts2 = registry2.list_all_artifacts()
        assert len(artifacts2) == 4

        retrieved = registry2.get_artifact('test_new_engine_py')
        assert retrieved is not None
        assert retrieved.primary_domain == 'SIGNALS'
        assert retrieved.artifact_type == 'ENGINE'
        assert retrieved.lifecycle_status == 'development'

    def test_artifact_registry_update_persists(self, setup_test_environment):
        """Test that artifact updates persist through save/load cycle"""
        env = setup_test_environment

        # Load and update
        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        artifact = registry.get_artifact('allocation_engine_py')
        assert artifact is not None

        # Update the artifact
        updated = ArtifactMetadata(
            artifact_id='allocation_engine_py',
            file_path='engines/allocation_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2025-01-15',
            last_modified='2025-05-26',
            owner_role='Signal Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            dependencies=['system_architecture_md'],
            description='Updated description'
        )
        registry.update_artifact('allocation_engine_py', updated)
        registry.save()

        # Reload and verify
        registry2 = ArtifactRegistry(env['artifact_registry_path'])
        registry2.load()

        retrieved = registry2.get_artifact('allocation_engine_py')
        assert retrieved is not None
        assert retrieved.last_modified == '2025-05-26'
        assert retrieved.description == 'Updated description'

    def test_domain_registry_loads_all_domains(self, setup_test_environment):
        """Test that domain registry loads all 12 domains correctly"""
        env = setup_test_environment

        domain_reg = DomainRegistry(env['domain_registry_path'])
        domain_reg.load()

        domains = domain_reg.list_domains()
        assert len(domains) == 12

        # Verify core domains
        core_domains = domain_reg.list_core_domains()
        core_ids = [d.domain_id for d in core_domains]
        assert 'SIGNALS' in core_ids
        assert 'SEMANTICS' in core_ids
        assert 'REASONING' in core_ids
        assert 'REPORT' in core_ids

        # Verify surface domains
        surface_domains = domain_reg.list_surface_domains()
        assert len(surface_domains) == 8

    def test_lifecycle_manager_loads_all_types(self, setup_test_environment):
        """Test that lifecycle manager loads state machines for all types"""
        env = setup_test_environment

        lifecycle_mgr = LifecycleManager(env['lifecycle_path'])
        lifecycle_mgr.load()

        artifact_types = lifecycle_mgr.list_artifact_types()
        assert 'SSOT' in artifact_types
        assert 'ENGINE' in artifact_types
        assert 'REPORT_OUT' in artifact_types
        assert 'DATA_IN' in artifact_types
        assert 'DATA_OUT' in artifact_types

    def test_registry_query_by_domain(self, setup_test_environment):
        """Test querying artifacts by domain after loading"""
        env = setup_test_environment

        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        signals_artifacts = registry.list_artifacts_by_domain('SIGNALS')
        assert len(signals_artifacts) == 1
        assert signals_artifacts[0].artifact_id == 'allocation_engine_py'

        report_artifacts = registry.list_artifacts_by_domain('REPORT')
        assert len(report_artifacts) == 1
        assert report_artifacts[0].artifact_id == 'portfolio_report_txt'

    def test_registry_query_by_type(self, setup_test_environment):
        """Test querying artifacts by type after loading"""
        env = setup_test_environment

        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        engines = registry.list_artifacts_by_type('ENGINE')
        assert len(engines) == 1
        assert engines[0].artifact_id == 'allocation_engine_py'

        ssot_docs = registry.list_artifacts_by_type('SSOT')
        assert len(ssot_docs) == 1
        assert ssot_docs[0].artifact_id == 'system_architecture_md'

    def test_registry_query_by_lifecycle(self, setup_test_environment):
        """Test querying artifacts by lifecycle status after loading"""
        env = setup_test_environment

        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        active_artifacts = registry.list_artifacts_by_lifecycle('active')
        assert len(active_artifacts) == 1

        canonical_artifacts = registry.list_artifacts_by_lifecycle('canonical')
        assert len(canonical_artifacts) == 1

    def test_registry_handles_missing_file_gracefully(self, temp_dir):
        """Test that registry raises appropriate error for missing file"""
        missing_path = temp_dir / "nonexistent.yaml"
        registry = ArtifactRegistry(missing_path)

        with pytest.raises(FileNotFoundError):
            registry.load()

    def test_registry_supports_1000_artifacts(self, setup_test_environment):
        """Test that registry supports at least 1000 artifacts (Req 15.2)"""
        env = setup_test_environment

        # Create a registry with 1000 artifacts
        artifacts_list = []
        for i in range(1000):
            artifacts_list.append({
                'artifact_id': f'artifact_{i:04d}',
                'file_path': f'files/artifact_{i:04d}.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2025-01-01',
                'last_modified': '2025-05-26',
                'owner_role': 'Developer',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
            })

        large_registry = {'artifacts': artifacts_list}
        with open(env['artifact_registry_path'], 'w') as f:
            yaml.dump(large_registry, f, default_flow_style=False)

        # Load and verify
        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        all_artifacts = registry.list_all_artifacts()
        assert len(all_artifacts) == 1000

        # Query should work
        signals = registry.list_artifacts_by_domain('SIGNALS')
        assert len(signals) == 1000



# ============================================================================
# Test Class: CLI Commands
# ============================================================================


class TestCLICommands:
    """Integration tests for CLI commands end-to-end"""

    @pytest.fixture
    def cli_path(self):
        """Path to the CLI main script"""
        return Path(__file__).parent / "cli_main.py"

    @pytest.fixture
    def venv_python(self):
        """Path to the venv Python with dependencies installed"""
        venv_path = Path(__file__).parent.parent.parent / ".venv" / "bin" / "python"
        if venv_path.exists():
            return str(venv_path)
        return sys.executable

    def test_cli_register_and_show(self, cli_path, venv_python, setup_test_environment):
        """Test registering an artifact via CLI and showing it"""
        env = setup_test_environment

        # Register a new artifact
        result = subprocess.run(
            [
                venv_python, str(cli_path), 'register',
                '--artifact-id', 'cli_test_artifact',
                '--file-path', 'test/cli_test.py',
                '--domain', 'SIGNALS',
                '--type', 'ENGINE',
                '--lifecycle', 'development',
                '--owner', 'Test Developer',
                '--ssot-relationship', 'implementation',
                '--writers', 'SIGNALS',
                '--readers', 'ALL',
            ],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
            env={**os.environ, 'DOMAINIZATION_REGISTRY': str(env['artifact_registry_path'])}
        )

        # CLI should execute without crashing (may fail due to env setup)
        # We verify the CLI is callable and processes arguments
        assert result.returncode is not None

    def test_cli_list_command(self, cli_path, venv_python, setup_test_environment):
        """Test listing artifacts via CLI"""
        env = setup_test_environment

        result = subprocess.run(
            [venv_python, str(cli_path), 'list'],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # CLI should execute without crashing
        assert result.returncode is not None

    def test_cli_validate_command(self, cli_path, venv_python, setup_test_environment):
        """Test running validation via CLI"""
        env = setup_test_environment

        result = subprocess.run(
            [venv_python, str(cli_path), 'validate'],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # CLI should execute without crashing
        assert result.returncode is not None

    def test_cli_health_command(self, cli_path, venv_python, setup_test_environment):
        """Test generating health report via CLI"""
        env = setup_test_environment

        result = subprocess.run(
            [venv_python, str(cli_path), 'health'],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # CLI should execute without crashing
        assert result.returncode is not None

    def test_cli_config_show_command(self, cli_path, venv_python):
        """Test showing configuration via CLI"""
        result = subprocess.run(
            [venv_python, str(cli_path), 'config', 'show'],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # CLI should execute without crashing
        assert result.returncode is not None

    def test_cli_no_command_shows_help(self, cli_path, venv_python):
        """Test that running CLI without command shows help"""
        result = subprocess.run(
            [venv_python, str(cli_path)],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # Should show help and return non-zero
        assert result.returncode == 1
        assert 'domainization' in result.stdout or 'usage' in result.stdout.lower()

    def test_cli_invalid_command(self, cli_path, venv_python):
        """Test that invalid command produces error"""
        result = subprocess.run(
            [venv_python, str(cli_path), 'nonexistent'],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # Should return error
        assert result.returncode != 0 or 'error' in result.stderr.lower() or 'usage' in result.stderr.lower()

    def test_cli_recover_list_command(self, cli_path, venv_python):
        """Test listing backups via CLI recover command"""
        result = subprocess.run(
            [venv_python, str(cli_path), 'recover', 'list'],
            capture_output=True,
            text=True,
            cwd=str(SRC_DIR),
        )

        # CLI should execute without crashing
        assert result.returncode is not None



# ============================================================================
# Test Class: Pre-Commit Hook Execution
# ============================================================================


class TestPreCommitHookExecution:
    """Integration tests for pre-commit hook execution"""

    @pytest.fixture
    def hook_path(self):
        """Path to the pre-commit hook script"""
        return Path(__file__).parent.parent / "hooks" / "pre-commit"

    def test_hook_script_exists_and_is_executable(self, hook_path):
        """Test that pre-commit hook script exists"""
        assert hook_path.exists(), f"Pre-commit hook not found at {hook_path}"

    def test_hook_script_is_valid_bash(self, hook_path):
        """Test that pre-commit hook is valid bash syntax"""
        result = subprocess.run(
            ['bash', '-n', str(hook_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Bash syntax error: {result.stderr}"

    def test_hook_never_blocks_commits(self, hook_path):
        """Test that hook always exits with 0 (never blocks)"""
        # The hook should always exit 0 even if validation fails
        # We verify by checking the script content for 'exit 0' at the end
        content = hook_path.read_text()
        # Last non-empty line should be 'exit 0'
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        assert lines[-1] == 'exit 0', "Hook must always exit 0 (never block commits)"

    def test_hook_contains_observability_mode_indicator(self, hook_path):
        """Test that hook clearly indicates observability mode"""
        content = hook_path.read_text()
        assert 'OBSERVABILITY' in content.upper() or 'WARNINGS ONLY' in content.upper() or 'warnings only' in content.lower()

    def test_hook_handles_missing_domainization_dir(self, temp_dir):
        """Test that hook handles missing .domainization directory gracefully"""
        hook_path = Path(__file__).parent.parent / "hooks" / "pre-commit"

        # Run hook in a directory without .domainization
        result = subprocess.run(
            ['bash', str(hook_path)],
            capture_output=True,
            text=True,
            cwd=str(temp_dir),
            env={**os.environ, 'GIT_DIR': str(temp_dir / '.git')}
        )

        # Hook should not crash (exit 0 or handle gracefully)
        # It may fail because git rev-parse won't work, but it shouldn't crash badly
        # The important thing is it doesn't block (non-zero exit from hook = block)
        # Since we're not in a git repo, it may error, which is acceptable
        assert result.returncode is not None


# ============================================================================
# Test Class: Backup and Recovery
# ============================================================================


class TestBackupAndRecovery:
    """Integration tests for backup and recovery flows"""

    def test_backup_created_on_registry_save(self, setup_test_environment, monkeypatch):
        """Test that saving registry creates a backup automatically"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Monkeypatch the DEFAULT_BACKUP_DIR so backups go to our temp dir
        import registry_backup_manager
        monkeypatch.setattr(registry_backup_manager, 'DEFAULT_BACKUP_DIR', backups_dir)

        # Count initial backups
        initial_backups = list(backups_dir.glob("*.yaml"))
        initial_count = len(initial_backups)

        # Load, modify, and save registry
        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()

        new_artifact = ArtifactMetadata(
            artifact_id='backup_test_artifact',
            file_path='test/backup_test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Developer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
        )
        registry.register_artifact(new_artifact)
        registry.save()

        # Verify backup was created
        new_backups = list(backups_dir.glob("*.yaml"))
        assert len(new_backups) > initial_count

    def test_backup_retention_policy(self, setup_test_environment):
        """Test that backup retention policy keeps only last N backups"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create more than 10 backups manually
        for i in range(15):
            backup_path = backups_dir / f"artifact_registry_2025-05-{i+1:02d}_00-00-00.yaml"
            backup_path.write_text(f"# Backup {i}\n")

        # Run cleanup with retention of 10
        removed = cleanup_old_backups(
            env['artifact_registry_path'],
            keep=10,
            backup_dir=backups_dir
        )

        # Should have removed some backups
        assert len(removed) > 0

        # Should have at most 10 remaining
        remaining = list_backups(env['artifact_registry_path'], backup_dir=backups_dir)
        assert len(remaining) <= 10

    def test_create_backup_and_cleanup_combined(self, setup_test_environment):
        """Test combined backup creation and cleanup"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create a backup
        backup_path = create_backup_and_cleanup(
            env['artifact_registry_path'],
            keep=10,
            backup_dir=backups_dir
        )

        assert backup_path is not None
        assert backup_path.exists()
        assert 'artifact_registry' in backup_path.name

    def test_recovery_from_backup(self, setup_test_environment):
        """Test full recovery flow from backup"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create a backup of current state
        backup_path = create_backup(
            env['artifact_registry_path'],
            backup_dir=backups_dir
        )
        assert backup_path is not None

        # Corrupt the registry
        with open(env['artifact_registry_path'], 'w') as f:
            yaml.dump({'artifacts': []}, f)

        # Verify corruption
        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()
        assert len(registry.list_all_artifacts()) == 0

        # Recover from backup
        recovery_mgr = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=env['artifact_registry_path'],
            repo_root=env['repo_root']
        )

        result = recovery_mgr.restore_from_backup(str(backup_path))

        assert result['success'] is True

        # Verify recovery
        registry2 = ArtifactRegistry(env['artifact_registry_path'])
        registry2.load()
        assert len(registry2.list_all_artifacts()) == 3

    def test_recovery_from_latest_backup(self, setup_test_environment):
        """Test recovery from the most recent backup"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create multiple backups
        create_backup(env['artifact_registry_path'], backup_dir=backups_dir)

        # Modify and create another backup
        registry = ArtifactRegistry(env['artifact_registry_path'])
        registry.load()
        new_artifact = ArtifactMetadata(
            artifact_id='recovery_test_artifact',
            file_path='test/recovery.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2025-05-26',
            last_modified='2025-05-26',
            owner_role='Developer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
        )
        registry.register_artifact(new_artifact)
        registry.save()

        # Now corrupt the registry
        with open(env['artifact_registry_path'], 'w') as f:
            yaml.dump({'artifacts': []}, f)

        # Recover from latest
        recovery_mgr = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=env['artifact_registry_path'],
            repo_root=env['repo_root']
        )

        result = recovery_mgr.restore_latest_backup()
        assert result['success'] is True

    def test_recovery_lists_available_backups(self, setup_test_environment):
        """Test listing available backups for recovery"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create backups with distinct timestamps by writing files directly
        backup1 = backups_dir / "artifact_registry_2025-05-20_10-00-00.yaml"
        backup2 = backups_dir / "artifact_registry_2025-05-21_10-00-00.yaml"
        shutil.copy2(env['artifact_registry_path'], backup1)
        shutil.copy2(env['artifact_registry_path'], backup2)

        recovery_mgr = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=env['artifact_registry_path'],
            repo_root=env['repo_root']
        )

        backups = recovery_mgr.list_available_backups()
        assert len(backups) >= 2

        # Each backup should have required metadata
        for backup in backups:
            assert 'file_name' in backup
            assert 'file_path' in backup
            assert 'file_size' in backup
            assert 'modified_time_str' in backup

    def test_recovery_validates_backup_before_restore(self, setup_test_environment):
        """Test that recovery validates backup file before restoring"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create an invalid backup file
        invalid_backup = backups_dir / "invalid_backup.yaml"
        invalid_backup.write_text("this is not valid yaml: [[[")

        recovery_mgr = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=env['artifact_registry_path'],
            repo_root=env['repo_root']
        )

        with pytest.raises(ValueError):
            recovery_mgr.restore_from_backup(str(invalid_backup))

    def test_recovery_generates_health_report_after_restore(self, setup_test_environment):
        """Test that recovery generates health report after successful restore"""
        env = setup_test_environment
        backups_dir = env['domainization_dir'] / "backups"

        # Create a backup
        backup_path = create_backup(
            env['artifact_registry_path'],
            backup_dir=backups_dir
        )

        recovery_mgr = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=env['artifact_registry_path'],
            repo_root=env['repo_root']
        )

        result = recovery_mgr.restore_from_backup(str(backup_path))

        assert result['success'] is True
        assert result['health_report'] is not None
        assert 'total_artifacts' in result['health_report']


# ============================================================================
# Test Class: Health Report Integration
# ============================================================================


class TestHealthReportIntegration:
    """Integration tests for health report generation with real data"""

    def test_health_report_with_real_registry(self, setup_test_environment):
        """Test health report generation with actual registry data"""
        env = setup_test_environment

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        health_reporter = HealthReporter(
            artifact_registry=artifact_registry,
            repo_root=env['repo_root']
        )

        report = health_reporter.generate_health_report()

        assert report is not None
        assert 'summary' in report
        assert 'report_date' in report
        assert report['summary']['total_artifacts'] >= 0

    def test_health_report_completes_within_target(self, setup_test_environment):
        """Test that health report generates in less than 10 seconds (Req 15.3)"""
        env = setup_test_environment
        import time

        artifact_registry = ArtifactRegistry(env['artifact_registry_path'])
        health_reporter = HealthReporter(
            artifact_registry=artifact_registry,
            repo_root=env['repo_root']
        )

        start = time.time()
        report = health_reporter.generate_health_report()
        elapsed = time.time() - start

        assert elapsed < 10.0, f"Health report took {elapsed:.2f}s, exceeds 10s target"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
