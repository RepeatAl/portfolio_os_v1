"""
Unit tests for Observer 3: Lifecycle Validator
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from lifecycle_manager import LifecycleManager
from artifact_schema import ArtifactMetadata
from observer_lifecycle import LifecycleValidator
from validation_result import WarningCodes


class TestLifecycleValidator:
    """Test suite for LifecycleValidator"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary repository structure"""
        temp_dir = tempfile.mkdtemp()
        repo_root = Path(temp_dir)
        
        # Create .domainization directory
        domainization_dir = repo_root / '.domainization'
        domainization_dir.mkdir()
        
        # Create empty artifact registry
        artifact_registry_file = domainization_dir / 'artifact_registry.yaml'
        artifact_registry_file.write_text('artifacts: []\n')
        
        # Create lifecycle state machine registry
        lifecycle_file = domainization_dir / 'lifecycle_state_machine.yaml'
        lifecycle_data = {
            'artifact_types': {
                'ENGINE': {
                    'description': 'Engine lifecycle',
                    'states': ['planned', 'development', 'active', 'deprecated'],
                    'initial_state': 'planned',
                    'transitions': [
                        {'from': 'planned', 'to': 'development', 'condition': 'Implementation begins'},
                        {'from': 'development', 'to': 'active', 'condition': 'Production ready'},
                        {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                    ],
                    'modifiable_states': ['planned', 'development', 'active'],
                    'read_only_states': ['deprecated']
                },
                'SSOT': {
                    'description': 'SSOT lifecycle',
                    'states': ['draft', 'review', 'canonical', 'deprecated'],
                    'initial_state': 'draft',
                    'transitions': [
                        {'from': 'draft', 'to': 'review', 'condition': 'Ready for review'},
                        {'from': 'review', 'to': 'canonical', 'condition': 'Approved'},
                        {'from': 'canonical', 'to': 'deprecated', 'condition': 'Superseded'}
                    ],
                    'modifiable_states': ['draft', 'review', 'canonical'],
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
    def artifact_registry(self, temp_repo):
        """Create artifact registry"""
        registry_path = temp_repo / '.domainization' / 'artifact_registry.yaml'
        registry = ArtifactRegistry(registry_path)
        registry.load()
        return registry
    
    @pytest.fixture
    def lifecycle_manager(self, temp_repo):
        """Create lifecycle manager"""
        lifecycle_path = temp_repo / '.domainization' / 'lifecycle_state_machine.yaml'
        manager = LifecycleManager(lifecycle_path)
        manager.load()
        return manager
    
    @pytest.fixture
    def validator(self, artifact_registry, lifecycle_manager):
        """Create lifecycle validator"""
        return LifecycleValidator(artifact_registry, lifecycle_manager)
    
    def test_detect_missing_lifecycle_status(self, validator, artifact_registry):
        """Test detection of missing lifecycle status"""
        # Register artifact with valid lifecycle_status first
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
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
        artifact_registry.register_artifact(metadata)
        
        # Manually corrupt to test validation
        artifact_registry._artifacts['test_engine_py'].lifecycle_status = ''
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W202_MISSING_LIFECYCLE_STATUS
    
    def test_detect_invalid_lifecycle_state(self, validator, artifact_registry):
        """Test detection of invalid lifecycle state"""
        # Register artifact with invalid state
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='invalid_state',  # Not in state machine
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W203_INVALID_LIFECYCLE_STATE
        assert 'invalid_state' in result.warnings[0].warning_message
    
    def test_detect_invalid_transition(self, validator, artifact_registry):
        """Test detection of invalid lifecycle transition"""
        # Register artifact
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
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
        artifact_registry.register_artifact(metadata)
        
        # Set previous state
        previous_states = {'test_engine_py': 'planned'}  # Invalid: planned -> active (should go through development)
        
        # Validate
        result = validator.validate(previous_states=previous_states)
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W200_INVALID_LIFECYCLE_TRANSITION
        assert 'planned' in result.warnings[0].warning_message
        assert 'active' in result.warnings[0].warning_message
    
    def test_valid_transition(self, validator, artifact_registry):
        """Test valid lifecycle transition"""
        # Register artifact
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Set previous state
        previous_states = {'test_engine_py': 'planned'}  # Valid: planned -> development
        
        # Validate
        result = validator.validate(previous_states=previous_states)
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_detect_deprecated_modification(self, validator, artifact_registry, temp_repo):
        """Test detection of modification to deprecated artifact"""
        # Create file
        test_file = temp_repo / 'test_engine.py'
        test_file.write_text('# Test engine\n')
        
        # Register deprecated artifact
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='deprecated',  # Read-only
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate with file in changed_files
        result = validator.validate(changed_files=[Path('test_engine.py')])
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W201_DEPRECATED_MODIFICATION
    
    def test_no_warning_for_deprecated_not_modified(self, validator, artifact_registry):
        """Test no warning for deprecated artifact that wasn't modified"""
        # Register deprecated artifact
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='deprecated',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate without file in changed_files
        result = validator.validate(changed_files=[])
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_suggest_valid_transitions(self, validator, artifact_registry):
        """Test that suggestions include valid transitions"""
        # Register artifact
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
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
        artifact_registry.register_artifact(metadata)
        
        # Set previous state
        previous_states = {'test_engine_py': 'planned'}  # Invalid transition
        
        # Validate
        result = validator.validate(previous_states=previous_states)
        
        # Should suggest development
        assert result.has_warnings()
        assert 'development' in result.warnings[0].suggestion
    
    def test_execution_time_tracking(self, validator, artifact_registry):
        """Test that execution time is tracked"""
        # Register artifact
        metadata = ArtifactMetadata(
            artifact_id='test_py',
            file_path='test.py',
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
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have execution time
        assert result.execution_time_ms > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
