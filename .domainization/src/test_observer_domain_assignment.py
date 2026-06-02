"""
Unit tests for Observer 2: Domain Assignment Validator
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from artifact_schema import ArtifactMetadata
from observer_domain_assignment import DomainAssignmentValidator
from validation_result import WarningCodes


class TestDomainAssignmentValidator:
    """Test suite for DomainAssignmentValidator"""
    
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
        
        # Create domain registry with test domains
        domain_registry_file = domainization_dir / 'domain_registry.yaml'
        domains_data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Generate structured signals',
                    'allowed_artifact_types': ['ENGINE', 'SSOT', 'DATA_OUT'],
                    'cannot_own': ['REPORT_OUT', 'DASHBOARD'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'ARCH',
                    'name': 'Architecture',
                    'responsibility_scope': 'System architecture',
                    'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                    'cannot_own': ['REPORT_OUT'],
                    'priority': 'surface',
                    'authority_level': None
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
    def domain_registry(self, temp_repo):
        """Create domain registry"""
        registry_path = temp_repo / '.domainization' / 'domain_registry.yaml'
        registry = DomainRegistry(registry_path)
        registry.load()
        return registry
    
    @pytest.fixture
    def validator(self, artifact_registry, domain_registry):
        """Create domain assignment validator"""
        return DomainAssignmentValidator(artifact_registry, domain_registry)
    
    def test_detect_invalid_domain(self, validator, artifact_registry):
        """Test detection of invalid domain"""
        # Register artifact with invalid domain
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='INVALID_DOMAIN',  # Invalid
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
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W100_INVALID_DOMAIN
        assert 'INVALID_DOMAIN' in result.warnings[0].warning_message
    
    def test_detect_domain_cannot_own_type(self, validator, artifact_registry):
        """Test detection of domain that cannot own artifact type"""
        # Register artifact with domain that cannot own this type
        metadata = ArtifactMetadata(
            artifact_id='test_report_py',
            file_path='test_report.py',
            primary_domain='SIGNALS',  # SIGNALS cannot own REPORT_OUT
            artifact_type='REPORT_OUT',
            lifecycle_status='current',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W101_DOMAIN_CANNOT_OWN_TYPE
        assert 'cannot own' in result.warnings[0].warning_message.lower()
    
    def test_valid_domain_assignment(self, validator, artifact_registry):
        """Test valid domain assignment"""
        # Register artifact with valid domain
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',  # SIGNALS can own ENGINE
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
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_suggest_valid_domains(self, validator, artifact_registry):
        """Test that suggestions include valid domains"""
        # Register artifact with domain that cannot own this type
        metadata = ArtifactMetadata(
            artifact_id='test_report_py',
            file_path='test_report.py',
            primary_domain='SIGNALS',  # SIGNALS cannot own REPORT_OUT
            artifact_type='REPORT_OUT',
            lifecycle_status='current',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should suggest REPORT domain
        assert result.has_warnings()
        assert 'REPORT' in result.warnings[0].suggestion
    
    def test_detect_invalid_secondary_domain(self, validator, artifact_registry):
        """Test detection of invalid secondary domain"""
        # Register artifact with invalid secondary domain
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
            allowed_readers=['ALL'],
            secondary_domains=['INVALID_DOMAIN']  # Invalid
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W100_INVALID_DOMAIN
        assert 'INVALID_DOMAIN' in result.warnings[0].warning_message
        assert result.warnings[0].severity == 'medium'  # Secondary domain is medium severity
    
    def test_validate_specific_files(self, validator, artifact_registry):
        """Test validation of specific files only"""
        # Register two artifacts
        metadata1 = ArtifactMetadata(
            artifact_id='test1_py',
            file_path='test1.py',
            primary_domain='INVALID',  # Invalid
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata1)
        
        metadata2 = ArtifactMetadata(
            artifact_id='test2_py',
            file_path='test2.py',
            primary_domain='SIGNALS',  # Valid
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate only test2.py
        result = validator.validate([Path('test2.py')])
        
        # Should have no warnings (test1.py not validated)
        assert not result.has_warnings()
    
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
