"""
Unit tests for artifact registry and schema validation
"""

import pytest
import yaml
from pathlib import Path
from artifact_schema import ArtifactMetadata, validate_artifact_dict


def load_artifact_registry():
    """Load artifact registry from YAML file"""
    registry_path = Path(__file__).parent.parent / "artifact_registry.yaml"
    with open(registry_path, 'r') as f:
        return yaml.safe_load(f)


class TestArtifactRegistrySchema:
    """Test artifact registry structure"""
    
    def test_registry_loads_successfully(self):
        """Test that artifact registry YAML is valid and loads"""
        registry = load_artifact_registry()
        assert registry is not None
        assert 'artifacts' in registry
    
    def test_artifacts_is_list(self):
        """Test that artifacts is a list"""
        registry = load_artifact_registry()
        assert isinstance(registry['artifacts'], list)
    
    def test_example_artifacts_present(self):
        """Test that example artifacts are present"""
        registry = load_artifact_registry()
        assert len(registry['artifacts']) >= 11  # At least 11 examples
    
    def test_each_artifact_has_required_fields(self):
        """Test that each artifact has all required fields"""
        registry = load_artifact_registry()
        required_fields = [
            'artifact_id', 'file_path', 'primary_domain', 'artifact_type',
            'lifecycle_status', 'created_date', 'last_modified', 'owner_role',
            'ssot_relationship', 'allowed_writers', 'allowed_readers'
        ]
        
        for artifact in registry['artifacts']:
            for field in required_fields:
                assert field in artifact, \
                    f"Artifact {artifact.get('artifact_id')} missing field: {field}"
    
    def test_artifact_ids_are_unique(self):
        """Test that artifact IDs are unique"""
        registry = load_artifact_registry()
        artifact_ids = [a['artifact_id'] for a in registry['artifacts']]
        assert len(artifact_ids) == len(set(artifact_ids))


class TestArtifactExamples:
    """Test that example artifacts cover all artifact types"""
    
    def test_ssot_example_present(self):
        """Test that SSOT example is present"""
        registry = load_artifact_registry()
        ssot_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'SSOT']
        assert len(ssot_artifacts) > 0
    
    def test_engine_example_present(self):
        """Test that ENGINE example is present"""
        registry = load_artifact_registry()
        engine_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'ENGINE']
        assert len(engine_artifacts) > 0
    
    def test_report_out_example_present(self):
        """Test that REPORT_OUT example is present"""
        registry = load_artifact_registry()
        report_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'REPORT_OUT']
        assert len(report_artifacts) > 0
    
    def test_data_in_example_present(self):
        """Test that DATA_IN example is present"""
        registry = load_artifact_registry()
        data_in_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'DATA_IN']
        assert len(data_in_artifacts) > 0
    
    def test_data_out_example_present(self):
        """Test that DATA_OUT example is present"""
        registry = load_artifact_registry()
        data_out_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'DATA_OUT']
        assert len(data_out_artifacts) > 0
    
    def test_runtime_example_present(self):
        """Test that RUNTIME example is present"""
        registry = load_artifact_registry()
        runtime_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'RUNTIME']
        assert len(runtime_artifacts) > 0
    
    def test_dashboard_example_present(self):
        """Test that DASHBOARD example is present"""
        registry = load_artifact_registry()
        dashboard_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'DASHBOARD']
        assert len(dashboard_artifacts) > 0
    
    def test_snapshot_example_present(self):
        """Test that SNAPSHOT example is present"""
        registry = load_artifact_registry()
        snapshot_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'SNAPSHOT']
        assert len(snapshot_artifacts) > 0
    
    def test_config_example_present(self):
        """Test that CONFIG example is present"""
        registry = load_artifact_registry()
        config_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'CONFIG']
        assert len(config_artifacts) > 0
    
    def test_calibration_example_present(self):
        """Test that CALIBRATION example is present"""
        registry = load_artifact_registry()
        calibration_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'CALIBRATION']
        assert len(calibration_artifacts) > 0
    
    def test_steering_example_present(self):
        """Test that STEERING example is present"""
        registry = load_artifact_registry()
        steering_artifacts = [a for a in registry['artifacts'] if a['artifact_type'] == 'STEERING']
        assert len(steering_artifacts) > 0


class TestSchemaValidation:
    """Test schema validation function"""
    
    def test_valid_artifact_passes_validation(self):
        """Test that valid artifact passes validation"""
        artifact = {
            'artifact_id': 'test_artifact',
            'file_path': 'test/artifact.py',
            'primary_domain': 'SIGNALS',
            'artifact_type': 'ENGINE',
            'lifecycle_status': 'active',
            'created_date': '2026-05-24',
            'last_modified': '2026-05-24',
            'owner_role': 'Test engineer',
            'ssot_relationship': 'none',
            'allowed_writers': ['SIGNALS'],
            'allowed_readers': ['ALL']
        }
        
        is_valid, errors = validate_artifact_dict(artifact)
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_required_field_fails_validation(self):
        """Test that missing required field fails validation"""
        artifact = {
            'artifact_id': 'test_artifact',
            'file_path': 'test/artifact.py',
            # Missing primary_domain
            'artifact_type': 'ENGINE',
            'lifecycle_status': 'active',
            'created_date': '2026-05-24',
            'last_modified': '2026-05-24',
            'owner_role': 'Test engineer',
            'ssot_relationship': 'none',
            'allowed_writers': ['SIGNALS'],
            'allowed_readers': ['ALL']
        }
        
        is_valid, errors = validate_artifact_dict(artifact)
        assert not is_valid
        assert any('primary_domain' in error for error in errors)
    
    def test_invalid_date_format_fails_validation(self):
        """Test that invalid date format fails validation"""
        artifact = {
            'artifact_id': 'test_artifact',
            'file_path': 'test/artifact.py',
            'primary_domain': 'SIGNALS',
            'artifact_type': 'ENGINE',
            'lifecycle_status': 'active',
            'created_date': '05/24/2026',  # Invalid format
            'last_modified': '2026-05-24',
            'owner_role': 'Test engineer',
            'ssot_relationship': 'none',
            'allowed_writers': ['SIGNALS'],
            'allowed_readers': ['ALL']
        }
        
        is_valid, errors = validate_artifact_dict(artifact)
        assert not is_valid
        assert any('YYYY-MM-DD' in error for error in errors)
    
    def test_invalid_ssot_relationship_fails_validation(self):
        """Test that invalid ssot_relationship fails validation"""
        artifact = {
            'artifact_id': 'test_artifact',
            'file_path': 'test/artifact.py',
            'primary_domain': 'SIGNALS',
            'artifact_type': 'ENGINE',
            'lifecycle_status': 'active',
            'created_date': '2026-05-24',
            'last_modified': '2026-05-24',
            'owner_role': 'Test engineer',
            'ssot_relationship': 'invalid',  # Invalid value
            'allowed_writers': ['SIGNALS'],
            'allowed_readers': ['ALL']
        }
        
        is_valid, errors = validate_artifact_dict(artifact)
        assert not is_valid
        assert any('ssot_relationship' in error for error in errors)
    
    def test_all_registry_artifacts_pass_validation(self):
        """Test that all artifacts in registry pass validation"""
        registry = load_artifact_registry()
        
        for artifact in registry['artifacts']:
            is_valid, errors = validate_artifact_dict(artifact)
            assert is_valid, \
                f"Artifact {artifact['artifact_id']} failed validation: {errors}"


class TestArtifactMetadataClass:
    """Test ArtifactMetadata class methods"""
    
    def test_is_modifiable_for_active_artifact(self):
        """Test that active artifacts are modifiable"""
        metadata = ArtifactMetadata(
            artifact_id='test',
            file_path='test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-05-24',
            last_modified='2026-05-24',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        assert metadata.is_modifiable()
    
    def test_is_not_modifiable_for_deprecated_artifact(self):
        """Test that deprecated artifacts are not modifiable"""
        metadata = ArtifactMetadata(
            artifact_id='test',
            file_path='test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='deprecated',
            created_date='2026-05-24',
            last_modified='2026-05-24',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        assert not metadata.is_modifiable()
    
    def test_can_write_for_allowed_domain(self):
        """Test that allowed domain can write"""
        metadata = ArtifactMetadata(
            artifact_id='test',
            file_path='test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-05-24',
            last_modified='2026-05-24',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS', 'ARCH'],
            allowed_readers=['ALL']
        )
        
        assert metadata.can_write('SIGNALS')
        assert metadata.can_write('ARCH')
        assert not metadata.can_write('REPORT')
    
    def test_can_read_for_all(self):
        """Test that all domains can read when allowed_readers is ALL"""
        metadata = ArtifactMetadata(
            artifact_id='test',
            file_path='test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-05-24',
            last_modified='2026-05-24',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        assert metadata.can_read('SIGNALS')
        assert metadata.can_read('REPORT')
        assert metadata.can_read('USER')
    
    def test_can_read_for_specific_domains(self):
        """Test that only specific domains can read when restricted"""
        metadata = ArtifactMetadata(
            artifact_id='test',
            file_path='test.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-05-24',
            last_modified='2026-05-24',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['SIGNALS', 'ARCH']
        )
        
        assert metadata.can_read('SIGNALS')
        assert metadata.can_read('ARCH')
        assert not metadata.can_read('REPORT')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
