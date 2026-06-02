"""
Unit tests for Observer 5: SSOT Consistency Validator
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata
from observer_ssot_consistency import SSOTConsistencyValidator
from validation_result import WarningCodes


class TestSSOTConsistencyValidator:
    """Test suite for SSOTConsistencyValidator"""
    
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
    def validator(self, artifact_registry):
        """Create SSOT consistency validator"""
        return SSOTConsistencyValidator(artifact_registry)
    
    def test_detect_multiple_canonical_ssots(self, validator, artifact_registry):
        """Test detection of multiple canonical SSOTs for same topic"""
        # Register two canonical SSOTs with same topic
        metadata1 = ArtifactMetadata(
            artifact_id='ssot1_md',
            file_path='ssot1.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            topic='system_architecture'  # Same topic
        )
        artifact_registry.register_artifact(metadata1)
        
        metadata2 = ArtifactMetadata(
            artifact_id='ssot2_md',
            file_path='ssot2.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            topic='system_architecture'  # Same topic
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate
        result = validator.validate()
        
        # Should have warnings for both artifacts
        assert result.has_warnings()
        assert len(result.warnings) == 2
        assert all(w.warning_code == WarningCodes.W400_MULTIPLE_CANONICAL_SSOT for w in result.warnings)
        assert all(w.severity == 'critical' for w in result.warnings)
    
    def test_allow_multiple_canonical_different_topics(self, validator, artifact_registry):
        """Test that multiple canonical SSOTs with different topics are allowed"""
        # Register two canonical SSOTs with different topics
        metadata1 = ArtifactMetadata(
            artifact_id='ssot1_md',
            file_path='ssot1.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            topic='system_architecture'
        )
        artifact_registry.register_artifact(metadata1)
        
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
            topic='signal_calculation'  # Different topic
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate
        result = validator.validate()
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_detect_derived_without_dependencies(self, validator, artifact_registry):
        """Test detection of derived document without dependencies"""
        # Register derived document without dependencies
        metadata = ArtifactMetadata(
            artifact_id='derived_md',
            file_path='derived.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='derived',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            dependencies=None  # Missing
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W401_MISSING_SSOT_REFERENCE
    
    def test_detect_derived_without_canonical_reference(self, validator, artifact_registry):
        """Test detection of derived document without canonical SSOT reference"""
        # Register non-canonical SSOT
        metadata1 = ArtifactMetadata(
            artifact_id='other_doc_md',
            file_path='other_doc.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='draft',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='none',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata1)
        
        # Register derived document referencing non-canonical
        metadata2 = ArtifactMetadata(
            artifact_id='derived_md',
            file_path='derived.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='derived',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            dependencies=['other_doc_md']  # Not canonical
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W401_MISSING_SSOT_REFERENCE
    
    def test_valid_derived_with_canonical_reference(self, validator, artifact_registry):
        """Test valid derived document with canonical SSOT reference"""
        # Register canonical SSOT
        metadata1 = ArtifactMetadata(
            artifact_id='canonical_md',
            file_path='canonical.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            topic='architecture'
        )
        artifact_registry.register_artifact(metadata1)
        
        # Register derived document referencing canonical
        metadata2 = ArtifactMetadata(
            artifact_id='derived_md',
            file_path='derived.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='derived',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            dependencies=['canonical_md']  # References canonical
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate
        result = validator.validate()
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_detect_implementation_without_dependencies(self, validator, artifact_registry):
        """Test detection of implementation without dependencies"""
        # Register implementation without dependencies
        metadata = ArtifactMetadata(
            artifact_id='engine_py',
            file_path='engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            dependencies=None  # Missing
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W401_MISSING_SSOT_REFERENCE
    
    def test_valid_implementation_with_ssot_reference(self, validator, artifact_registry):
        """Test valid implementation with SSOT reference"""
        # Register SSOT
        metadata1 = ArtifactMetadata(
            artifact_id='spec_md',
            file_path='spec.md',
            primary_domain='SIGNALS',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='canonical',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            topic='signal_spec'
        )
        artifact_registry.register_artifact(metadata1)
        
        # Register implementation referencing SSOT
        metadata2 = ArtifactMetadata(
            artifact_id='engine_py',
            file_path='engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL'],
            dependencies=['spec_md']  # References SSOT
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate
        result = validator.validate()
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_detect_invalid_ssot_relationship(self, validator, artifact_registry):
        """Test detection of invalid ssot_relationship value"""
        # Register artifact with valid relationship first
        metadata = ArtifactMetadata(
            artifact_id='doc_md',
            file_path='doc.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Manually corrupt to test validation
        artifact_registry._artifacts['doc_md'].ssot_relationship = 'invalid_value'
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W402_INVALID_SSOT_RELATIONSHIP
    
    def test_execution_time_tracking(self, validator, artifact_registry):
        """Test that execution time is tracked"""
        # Register artifact
        metadata = ArtifactMetadata(
            artifact_id='doc_md',
            file_path='doc.md',
            primary_domain='ARCH',
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL'],
            topic='test'
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have execution time
        assert result.execution_time_ms > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
