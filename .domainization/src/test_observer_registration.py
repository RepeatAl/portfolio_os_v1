"""
Unit tests for Observer 1: Registration Validator
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata
from observer_registration import RegistrationValidator
from validation_result import WarningCodes


class TestRegistrationValidator:
    """Test suite for RegistrationValidator"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary repository structure"""
        temp_dir = tempfile.mkdtemp()
        repo_root = Path(temp_dir)
        
        # Create .domainization directory
        domainization_dir = repo_root / '.domainization'
        domainization_dir.mkdir()
        
        # Create empty registry file
        registry_file = domainization_dir / 'artifact_registry.yaml'
        registry_file.write_text('artifacts: []\n')
        
        yield repo_root
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def registry(self, temp_repo):
        """Create artifact registry"""
        registry_path = temp_repo / '.domainization' / 'artifact_registry.yaml'
        registry = ArtifactRegistry(registry_path)
        registry.load()
        return registry
    
    @pytest.fixture
    def validator(self, registry, temp_repo):
        """Create registration validator"""
        return RegistrationValidator(registry, temp_repo)
    
    def test_detect_unregistered_file(self, validator, temp_repo):
        """Test detection of unregistered file"""
        # Create unregistered file
        test_file = temp_repo / 'test_file.py'
        test_file.write_text('# Test file\n')
        
        # Validate
        result = validator.validate([Path('test_file.py')])
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W001_UNREGISTERED_ARTIFACT
        assert 'test_file.py' in result.warnings[0].file_path
    
    def test_detect_unregistered_markdown_without_frontmatter(self, validator, temp_repo):
        """Test detection of markdown file without frontmatter"""
        # Create markdown file without frontmatter
        test_file = temp_repo / 'test_doc.md'
        test_file.write_text('# Test Document\n\nContent here.\n')
        
        # Validate
        result = validator.validate([Path('test_doc.md')])
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W001_UNREGISTERED_ARTIFACT
    
    def test_validate_markdown_with_incomplete_frontmatter(self, validator, temp_repo):
        """Test validation of markdown with incomplete frontmatter"""
        # Create markdown file with incomplete frontmatter
        test_file = temp_repo / 'test_doc.md'
        frontmatter = """---
artifact_id: test_doc_md
primary_domain: ARCH
---

# Test Document

Content here.
"""
        test_file.write_text(frontmatter)
        
        # Validate
        result = validator.validate([Path('test_doc.md')])
        
        # Should have warning about missing fields
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W004_INCOMPLETE_METADATA
        assert 'missing required fields' in result.warnings[0].warning_message.lower()
    
    def test_validate_markdown_with_complete_frontmatter(self, validator, temp_repo):
        """Test validation of markdown with complete frontmatter"""
        # Create markdown file with complete frontmatter
        test_file = temp_repo / 'test_doc.md'
        frontmatter = """---
artifact_id: test_doc_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
owner_role: System Architect
ssot_relationship: canonical
allowed_writers: [ARCH]
allowed_readers: [ALL]
---

# Test Document

Content here.
"""
        test_file.write_text(frontmatter)
        
        # Validate
        result = validator.validate([Path('test_doc.md')])
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_validate_registered_artifact_with_valid_metadata(self, validator, registry, temp_repo):
        """Test validation of registered artifact with valid metadata"""
        # Create file
        test_file = temp_repo / 'test_engine.py'
        test_file.write_text('# Test engine\n')
        
        # Register artifact
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Signal Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate([Path('test_engine.py')])
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_validate_registered_artifact_with_invalid_metadata(self, validator, registry, temp_repo):
        """Test validation of registered artifact with invalid metadata"""
        # Create file
        test_file = temp_repo / 'test_engine.py'
        test_file.write_text('# Test engine\n')
        
        # Register artifact with valid metadata first
        metadata = ArtifactMetadata(
            artifact_id='test_engine_py',
            file_path='test_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Signal Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        registry.register_artifact(metadata)
        
        # Manually corrupt the metadata to test validation
        registry._artifacts['test_engine_py'].created_date = 'invalid-date'
        
        # Validate
        result = validator.validate([Path('test_engine.py')])
        
        # Should have warning about invalid metadata
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W003_INVALID_METADATA_SCHEMA
    
    def test_skip_excluded_directories(self, validator, temp_repo):
        """Test that excluded directories are skipped"""
        # Create files in excluded directories
        git_dir = temp_repo / '.git'
        git_dir.mkdir()
        (git_dir / 'config').write_text('git config\n')
        
        pycache_dir = temp_repo / '__pycache__'
        pycache_dir.mkdir()
        (pycache_dir / 'test.pyc').write_text('bytecode\n')
        
        # Validate all files
        result = validator.validate(None)
        
        # Should not warn about excluded files
        for warning in result.warnings:
            assert '.git' not in warning.file_path
            assert '__pycache__' not in warning.file_path
    
    def test_execution_time_tracking(self, validator, temp_repo):
        """Test that execution time is tracked"""
        # Create test file
        test_file = temp_repo / 'test.py'
        test_file.write_text('# Test\n')
        
        # Validate
        result = validator.validate([Path('test.py')])
        
        # Should have execution time
        assert result.execution_time_ms > 0
    
    def test_severity_levels(self, validator, temp_repo):
        """Test that warnings have appropriate severity levels"""
        # Create unregistered file
        test_file = temp_repo / 'test.py'
        test_file.write_text('# Test\n')
        
        # Validate
        result = validator.validate([Path('test.py')])
        
        # Unregistered artifact should be high severity
        assert result.warnings[0].severity == 'high'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
