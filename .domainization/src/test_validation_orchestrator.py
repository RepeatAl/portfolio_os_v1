"""
Integration tests for Validation Orchestrator
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from artifact_schema import ArtifactMetadata
from validation_orchestrator import ValidationOrchestrator


class TestValidationOrchestrator:
    """Test suite for ValidationOrchestrator"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary repository structure with all registries"""
        temp_dir = tempfile.mkdtemp()
        repo_root = Path(temp_dir)
        
        # Create .domainization directory
        domainization_dir = repo_root / '.domainization'
        domainization_dir.mkdir()
        
        # Create artifact registry
        artifact_registry_file = domainization_dir / 'artifact_registry.yaml'
        artifact_registry_file.write_text('artifacts: []\n')
        
        # Create domain registry
        domain_registry_file = domainization_dir / 'domain_registry.yaml'
        domains_data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Generate signals',
                    'allowed_artifact_types': ['ENGINE', 'SSOT', 'DATA_OUT'],
                    'cannot_own': ['REPORT_OUT'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'REPORT',
                    'name': 'Report Generation',
                    'responsibility_scope': 'Generate reports',
                    'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT'],
                    'cannot_own': ['DATA_OUT'],
                    'priority': 'core',
                    'authority_level': 4
                }
            ]
        }
        with open(domain_registry_file, 'w') as f:
            yaml.dump(domains_data, f)
        
        # Create lifecycle state machine
        lifecycle_file = domainization_dir / 'lifecycle_state_machine.yaml'
        lifecycle_data = {
            'artifact_types': {
                'ENGINE': {
                    'description': 'Engine lifecycle',
                    'states': ['planned', 'development', 'active', 'deprecated'],
                    'initial_state': 'planned',
                    'transitions': [
                        {'from': 'planned', 'to': 'development', 'condition': 'Start'},
                        {'from': 'development', 'to': 'active', 'condition': 'Ready'}
                    ],
                    'modifiable_states': ['planned', 'development', 'active'],
                    'read_only_states': ['deprecated']
                }
            }
        }
        with open(lifecycle_file, 'w') as f:
            yaml.dump(lifecycle_data, f)
        
        yield repo_root
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def orchestrator(self, temp_repo):
        """Create validation orchestrator with all registries"""
        artifact_registry = ArtifactRegistry(temp_repo / '.domainization' / 'artifact_registry.yaml')
        artifact_registry.load()
        
        domain_registry = DomainRegistry(temp_repo / '.domainization' / 'domain_registry.yaml')
        domain_registry.load()
        
        lifecycle_manager = LifecycleManager(temp_repo / '.domainization' / 'lifecycle_state_machine.yaml')
        lifecycle_manager.load()
        
        return ValidationOrchestrator(artifact_registry, domain_registry, lifecycle_manager, temp_repo)
    
    def test_run_all_observers(self, orchestrator, temp_repo):
        """Test running all observers together"""
        # Create unregistered file
        test_file = temp_repo / 'test.py'
        test_file.write_text('# Test\n')
        
        # Run validation
        report = orchestrator.validate_all([Path('test.py')])
        
        # Should have warnings from registration observer
        assert report.total_warnings > 0
        assert 'RegistrationValidator' in report.warnings_by_observer
    
    def test_no_warnings_for_valid_artifact(self, orchestrator):
        """Test that valid artifacts produce no warnings"""
        # Register valid artifact with dependencies to avoid SSOT warning
        metadata = ArtifactMetadata(
            artifact_id='signal_engine_py',
            file_path='signal_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',  # Not an implementation, so no SSOT reference needed
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        orchestrator.artifact_registry.register_artifact(metadata)
        
        # Run validation
        report = orchestrator.validate_all([Path('signal_engine.py')])
        
        # Should have no warnings
        assert report.total_warnings == 0
    
    def test_multiple_violations_detected(self, orchestrator):
        """Test detection of multiple violations across observers"""
        # Register artifact with multiple issues
        metadata = ArtifactMetadata(
            artifact_id='bad_artifact_py',
            file_path='bad_artifact.py',
            primary_domain='SIGNALS',
            artifact_type='REPORT_OUT',  # Wrong: SIGNALS can't own REPORT_OUT
            lifecycle_status='invalid_state',  # Invalid lifecycle state
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        orchestrator.artifact_registry.register_artifact(metadata)
        
        # Run validation
        report = orchestrator.validate_all([Path('bad_artifact.py')])
        
        # Should have warnings from multiple observers
        assert report.total_warnings >= 2
        # Domain assignment should fail
        assert len(report.warnings_by_observer['DomainAssignmentValidator']) > 0
        # Boundary awareness should fail (SIGNALS writing REPORT_OUT)
        assert len(report.warnings_by_observer['BoundaryAwarenessValidator']) > 0
    
    def test_severity_counting(self, orchestrator):
        """Test that warnings are counted by severity"""
        # Register artifact with critical SSOT conflict
        metadata1 = ArtifactMetadata(
            artifact_id='ssot1_md',
            file_path='ssot1.md',
            primary_domain='SIGNALS',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='canonical',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            topic='test_topic'
        )
        orchestrator.artifact_registry.register_artifact(metadata1)
        
        metadata2 = ArtifactMetadata(
            artifact_id='ssot2_md',
            file_path='ssot2.md',
            primary_domain='SIGNALS',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='canonical',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            topic='test_topic'  # Same topic - conflict
        )
        orchestrator.artifact_registry.register_artifact(metadata2)
        
        # Run validation
        report = orchestrator.validate_all()
        
        # Should have critical warnings
        assert report.critical_warnings > 0
    
    def test_performance_tracking(self, orchestrator):
        """Test that execution time is tracked"""
        # Run validation
        report = orchestrator.validate_all()
        
        # Should have execution time
        assert report.total_execution_time_ms > 0
        # Should check performance target
        assert isinstance(report.performance_target_met, bool)
    
    def test_performance_target_met(self, orchestrator):
        """Test that performance target is met for small datasets"""
        # Register a few artifacts
        for i in range(10):
            metadata = ArtifactMetadata(
                artifact_id=f'artifact_{i}_py',
                file_path=f'artifact_{i}.py',
                primary_domain='SIGNALS',
                artifact_type='ENGINE',
                lifecycle_status='active',
                created_date='2026-01-01',
                last_modified='2026-01-01',
                owner_role='Engineer',
                ssot_relationship='implementation',
                allowed_writers=['SIGNALS'],
                allowed_readers=['ALL']
            )
            orchestrator.artifact_registry.register_artifact(metadata)
        
        # Run validation
        report = orchestrator.validate_all()
        
        # Should meet performance target (< 5 seconds)
        assert report.performance_target_met
        assert report.total_execution_time_ms < 5000
    
    def test_report_formatting(self, orchestrator):
        """Test that report can be formatted as string"""
        # Run validation
        report = orchestrator.validate_all()
        
        # Should be able to convert to string
        report_str = str(report)
        assert 'DOMAINIZATION OBSERVABILITY REPORT' in report_str
        assert 'OBSERVABILITY' in report_str
        assert 'Execution Time' in report_str
    
    def test_run_specific_observer(self, orchestrator, temp_repo):
        """Test running a specific observer"""
        # Create unregistered file
        test_file = temp_repo / 'test.py'
        test_file.write_text('# Test\n')
        
        # Run only registration validator
        result = orchestrator.validate_observer('RegistrationValidator', [Path('test.py')])
        
        # Should have result from registration validator
        assert result.observer_name == 'RegistrationValidator'
        assert result.has_warnings()
    
    def test_invalid_observer_name(self, orchestrator):
        """Test error handling for invalid observer name"""
        with pytest.raises(ValueError) as exc_info:
            orchestrator.validate_observer('InvalidObserver')
        
        assert 'Invalid observer name' in str(exc_info.value)
    
    def test_observability_mode_never_blocks(self, orchestrator):
        """Test that observability mode never blocks (always returns report)"""
        # Register artifact with valid metadata first
        metadata = ArtifactMetadata(
            artifact_id='bad_py',
            file_path='bad.py',
            primary_domain='SIGNALS',
            artifact_type='REPORT_OUT',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        orchestrator.artifact_registry.register_artifact(metadata)
        
        # Manually corrupt to create violations
        orchestrator.artifact_registry._artifacts['bad_py'].primary_domain = 'INVALID_DOMAIN'
        orchestrator.artifact_registry._artifacts['bad_py'].lifecycle_status = 'invalid'
        orchestrator.artifact_registry._artifacts['bad_py'].ssot_relationship = 'invalid'
        
        # Run validation - should not raise exception
        report = orchestrator.validate_all([Path('bad.py')])
        
        # Should return report with warnings, not block
        assert report is not None
        assert report.total_warnings > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
