"""
Unit tests for artifact registry operations
"""

import pytest
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata


class TestArtifactRegistryLoad:
    """Test artifact registry loading"""
    
    def test_load_registry_successfully(self):
        """Test that registry loads successfully"""
        registry = ArtifactRegistry()
        registry.load()
        
        artifacts = registry.list_all_artifacts()
        assert len(artifacts) > 0
    
    def test_load_nonexistent_registry_raises_error(self):
        """Test that loading nonexistent registry raises error"""
        registry = ArtifactRegistry(Path("/nonexistent/path.yaml"))
        
        with pytest.raises(FileNotFoundError):
            registry.load()
    
    def test_artifacts_indexed_by_id(self):
        """Test that artifacts are indexed by artifact_id"""
        registry = ArtifactRegistry()
        registry.load()
        
        # Get a known artifact
        artifacts = registry.list_all_artifacts()
        if artifacts:
            artifact = artifacts[0]
            retrieved = registry.get_artifact(artifact.artifact_id)
            assert retrieved is not None
            assert retrieved.artifact_id == artifact.artifact_id


class TestArtifactRegistryRegister:
    """Test artifact registration"""
    
    def test_register_new_artifact(self):
        """Test registering a new artifact"""
        registry = ArtifactRegistry()
        registry.load()
        
        initial_count = len(registry.list_all_artifacts())
        
        new_artifact = ArtifactMetadata(
            artifact_id='test_new_artifact',
            file_path='test/new_artifact.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2026-05-25',
            last_modified='2026-05-25',
            owner_role='Test engineer',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        registry.register_artifact(new_artifact)
        
        # Verify artifact was added
        assert len(registry.list_all_artifacts()) == initial_count + 1
        retrieved = registry.get_artifact('test_new_artifact')
        assert retrieved is not None
        assert retrieved.file_path == 'test/new_artifact.py'
    
    def test_register_duplicate_artifact_raises_error(self):
        """Test that registering duplicate artifact_id raises error"""
        registry = ArtifactRegistry()
        registry.load()
        
        # Get existing artifact ID
        existing = registry.list_all_artifacts()[0]
        
        duplicate = ArtifactMetadata(
            artifact_id=existing.artifact_id,  # Duplicate ID
            file_path='test/duplicate.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2026-05-25',
            last_modified='2026-05-25',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        with pytest.raises(ValueError, match="already exists"):
            registry.register_artifact(duplicate)
    
    def test_register_invalid_artifact_raises_error(self):
        """Test that registering invalid artifact raises error"""
        registry = ArtifactRegistry()
        registry.load()
        
        invalid_artifact = ArtifactMetadata(
            artifact_id='',  # Invalid: empty
            file_path='test/invalid.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2026-05-25',
            last_modified='2026-05-25',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        with pytest.raises(ValueError, match="Invalid metadata"):
            registry.register_artifact(invalid_artifact)


class TestArtifactRegistryUpdate:
    """Test artifact update"""
    
    def test_update_existing_artifact(self):
        """Test updating an existing artifact"""
        registry = ArtifactRegistry()
        registry.load()
        
        # Get existing artifact
        existing = registry.list_all_artifacts()[0]
        artifact_id = existing.artifact_id
        
        # Create updated metadata
        updated = ArtifactMetadata(
            artifact_id=artifact_id,
            file_path=existing.file_path,
            primary_domain=existing.primary_domain,
            artifact_type=existing.artifact_type,
            lifecycle_status='active',  # Changed
            created_date=existing.created_date,
            last_modified='2026-05-25',  # Changed
            owner_role='Updated owner',  # Changed
            ssot_relationship=existing.ssot_relationship,
            allowed_writers=existing.allowed_writers,
            allowed_readers=existing.allowed_readers
        )
        
        registry.update_artifact(artifact_id, updated)
        
        # Verify update
        retrieved = registry.get_artifact(artifact_id)
        assert retrieved.lifecycle_status == 'active'
        assert retrieved.last_modified == '2026-05-25'
        assert retrieved.owner_role == 'Updated owner'
    
    def test_update_nonexistent_artifact_raises_error(self):
        """Test that updating nonexistent artifact raises error"""
        registry = ArtifactRegistry()
        registry.load()
        
        nonexistent = ArtifactMetadata(
            artifact_id='nonexistent_id',
            file_path='test/nonexistent.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='development',
            created_date='2026-05-25',
            last_modified='2026-05-25',
            owner_role='Test',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        
        with pytest.raises(ValueError, match="not found"):
            registry.update_artifact('nonexistent_id', nonexistent)
    
    def test_update_with_mismatched_id_raises_error(self):
        """Test that updating with mismatched artifact_id raises error"""
        registry = ArtifactRegistry()
        registry.load()
        
        existing = registry.list_all_artifacts()[0]
        
        mismatched = ArtifactMetadata(
            artifact_id='different_id',  # Doesn't match
            file_path=existing.file_path,
            primary_domain=existing.primary_domain,
            artifact_type=existing.artifact_type,
            lifecycle_status=existing.lifecycle_status,
            created_date=existing.created_date,
            last_modified=existing.last_modified,
            owner_role=existing.owner_role,
            ssot_relationship=existing.ssot_relationship,
            allowed_writers=existing.allowed_writers,
            allowed_readers=existing.allowed_readers
        )
        
        with pytest.raises(ValueError, match="does not match"):
            registry.update_artifact(existing.artifact_id, mismatched)


class TestArtifactRegistryQuery:
    """Test artifact query methods"""
    
    def test_get_artifact_by_id(self):
        """Test retrieving artifact by ID"""
        registry = ArtifactRegistry()
        registry.load()
        
        artifacts = registry.list_all_artifacts()
        if artifacts:
            artifact = artifacts[0]
            retrieved = registry.get_artifact(artifact.artifact_id)
            assert retrieved is not None
            assert retrieved.artifact_id == artifact.artifact_id
    
    def test_get_nonexistent_artifact_returns_none(self):
        """Test that getting nonexistent artifact returns None"""
        registry = ArtifactRegistry()
        registry.load()
        
        retrieved = registry.get_artifact('nonexistent_id')
        assert retrieved is None
    
    def test_list_artifacts_by_domain(self):
        """Test listing artifacts by domain"""
        registry = ArtifactRegistry()
        registry.load()
        
        # Get artifacts for a known domain
        signals_artifacts = registry.list_artifacts_by_domain('SIGNALS')
        
        # Verify all returned artifacts belong to SIGNALS domain
        for artifact in signals_artifacts:
            assert artifact.primary_domain == 'SIGNALS' or \
                   (artifact.secondary_domains and 'SIGNALS' in artifact.secondary_domains)
    
    def test_list_artifacts_by_type(self):
        """Test listing artifacts by type"""
        registry = ArtifactRegistry()
        registry.load()
        
        # Get artifacts of a known type
        ssot_artifacts = registry.list_artifacts_by_type('SSOT')
        
        # Verify all returned artifacts are SSOT type
        for artifact in ssot_artifacts:
            assert artifact.artifact_type == 'SSOT'
    
    def test_list_artifacts_by_lifecycle(self):
        """Test listing artifacts by lifecycle status"""
        registry = ArtifactRegistry()
        registry.load()
        
        # Get artifacts in a known lifecycle state
        canonical_artifacts = registry.list_artifacts_by_lifecycle('canonical')
        
        # Verify all returned artifacts are in canonical state
        for artifact in canonical_artifacts:
            assert artifact.lifecycle_status == 'canonical'
    
    def test_list_all_artifacts(self):
        """Test listing all artifacts"""
        registry = ArtifactRegistry()
        registry.load()
        
        all_artifacts = registry.list_all_artifacts()
        assert len(all_artifacts) > 0
        assert isinstance(all_artifacts, list)


class TestArtifactRegistryFrontmatter:
    """Test frontmatter parsing"""
    
    def test_parse_frontmatter_from_markdown(self, tmp_path):
        """Test parsing YAML frontmatter from markdown file"""
        # Create test markdown file with frontmatter
        test_file = tmp_path / "test.md"
        content = """---
artifact_id: test_doc
primary_domain: ARCH
artifact_type: SSOT
---

# Test Document

This is test content.
"""
        test_file.write_text(content)
        
        frontmatter = ArtifactRegistry.parse_frontmatter(test_file)
        
        assert frontmatter is not None
        assert frontmatter['artifact_id'] == 'test_doc'
        assert frontmatter['primary_domain'] == 'ARCH'
        assert frontmatter['artifact_type'] == 'SSOT'
    
    def test_parse_frontmatter_no_frontmatter_returns_none(self, tmp_path):
        """Test that file without frontmatter returns None"""
        test_file = tmp_path / "test.md"
        content = """# Test Document

This file has no frontmatter.
"""
        test_file.write_text(content)
        
        frontmatter = ArtifactRegistry.parse_frontmatter(test_file)
        assert frontmatter is None
    
    def test_parse_frontmatter_nonexistent_file_returns_none(self):
        """Test that nonexistent file returns None"""
        frontmatter = ArtifactRegistry.parse_frontmatter(Path("/nonexistent/file.md"))
        assert frontmatter is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
