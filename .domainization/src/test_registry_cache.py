"""
Unit tests for registry cache
"""

import pytest
import tempfile
import time
import yaml
from pathlib import Path
from registry_cache import RegistryCache
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from artifact_schema import ArtifactMetadata


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_artifact_registry(temp_dir):
    """Create sample artifact registry file"""
    registry_path = temp_dir / "artifact_registry.yaml"
    
    data = {
        'artifacts': [
            {
                'artifact_id': 'test_artifact_1',
                'file_path': 'test1.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'test_topic_1'
            },
            {
                'artifact_id': 'test_artifact_2',
                'file_path': 'test2.py',
                'primary_domain': 'SEMANTICS',
                'secondary_domains': ['SIGNALS'],
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'development',
                'created_date': '2026-01-02',
                'last_modified': '2026-01-02',
                'owner_role': 'Test owner',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SEMANTICS'],
                'allowed_readers': ['ALL'],
                'topic': 'test_topic_1'
            },
            {
                'artifact_id': 'test_artifact_3',
                'file_path': 'test3.md',
                'primary_domain': 'ARCH',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-03',
                'last_modified': '2026-01-03',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['ARCH'],
                'allowed_readers': ['ALL'],
                'topic': 'test_topic_2'
            }
        ]
    }
    
    with open(registry_path, 'w') as f:
        yaml.dump(data, f)
    
    return registry_path


@pytest.fixture
def sample_domain_registry(temp_dir):
    """Create sample domain registry file"""
    registry_path = temp_dir / "domain_registry.yaml"
    
    data = {
        'domains': [
            {
                'domain_id': 'SIGNALS',
                'name': 'Signal Generation',
                'responsibility_scope': 'Generate raw signals',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT'],
                'cannot_own': ['SSOT', 'REPORT_OUT'],
                'priority': 'core',
                'authority_level': 1
            },
            {
                'domain_id': 'SEMANTICS',
                'name': 'Semantic Interpretation',
                'responsibility_scope': 'Interpret signals',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT'],
                'cannot_own': ['SSOT', 'REPORT_OUT'],
                'priority': 'core',
                'authority_level': 2
            },
            {
                'domain_id': 'ARCH',
                'name': 'Architecture',
                'responsibility_scope': 'System architecture',
                'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                'cannot_own': ['REPORT_OUT'],
                'priority': 'surface'
            }
        ]
    }
    
    with open(registry_path, 'w') as f:
        yaml.dump(data, f)
    
    return registry_path


@pytest.fixture
def sample_lifecycle_manager(temp_dir):
    """Create sample lifecycle state machine file"""
    sm_path = temp_dir / "lifecycle_state_machine.yaml"
    
    data = {
        'artifact_types': {
            'ENGINE': {
                'description': 'Executable code engines',
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
                'description': 'Single source of truth documents',
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
    
    with open(sm_path, 'w') as f:
        yaml.dump(data, f)
    
    return sm_path


@pytest.fixture
def cache_with_data(sample_artifact_registry, sample_domain_registry, sample_lifecycle_manager):
    """Create cache with sample data"""
    artifact_registry = ArtifactRegistry(sample_artifact_registry)
    domain_registry = DomainRegistry(sample_domain_registry)
    lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
    
    cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
    cache.load()
    
    return cache


class TestRegistryCacheBasics:
    """Test basic cache operations"""
    
    def test_cache_initialization(self):
        """Test cache can be initialized"""
        cache = RegistryCache()
        assert cache is not None
        assert not cache._loaded
    
    def test_cache_load(self, cache_with_data):
        """Test cache loads data correctly"""
        assert cache_with_data._loaded
        assert len(cache_with_data._artifacts) == 3
    
    def test_cache_statistics(self, cache_with_data):
        """Test cache statistics"""
        stats = cache_with_data.get_statistics()
        
        assert stats['total_artifacts'] == 3
        assert stats['domains'] == 3  # SIGNALS, SEMANTICS, ARCH
        assert stats['artifact_types'] == 2  # ENGINE, SSOT
        assert stats['lifecycle_states'] == 3  # active, development, canonical
        assert stats['topics'] == 2  # test_topic_1, test_topic_2
        assert stats['cache_loaded'] is True


class TestRegistryCacheQueries:
    """Test cache query operations"""
    
    def test_get_artifact_by_id(self, cache_with_data):
        """Test O(1) artifact lookup by ID"""
        artifact = cache_with_data.get_artifact('test_artifact_1')
        
        assert artifact is not None
        assert artifact.artifact_id == 'test_artifact_1'
        assert artifact.primary_domain == 'SIGNALS'
        assert artifact.artifact_type == 'ENGINE'
    
    def test_get_nonexistent_artifact(self, cache_with_data):
        """Test lookup of nonexistent artifact"""
        artifact = cache_with_data.get_artifact('nonexistent')
        assert artifact is None
    
    def test_list_artifacts_by_domain(self, cache_with_data):
        """Test indexed lookup by domain"""
        # Primary domain
        signals_artifacts = cache_with_data.list_artifacts_by_domain('SIGNALS')
        assert len(signals_artifacts) == 2  # test_artifact_1 (primary) and test_artifact_2 (secondary)
        
        semantics_artifacts = cache_with_data.list_artifacts_by_domain('SEMANTICS')
        assert len(semantics_artifacts) == 1
        
        arch_artifacts = cache_with_data.list_artifacts_by_domain('ARCH')
        assert len(arch_artifacts) == 1
    
    def test_list_artifacts_by_type(self, cache_with_data):
        """Test indexed lookup by artifact type"""
        engines = cache_with_data.list_artifacts_by_type('ENGINE')
        assert len(engines) == 2
        
        ssots = cache_with_data.list_artifacts_by_type('SSOT')
        assert len(ssots) == 1
    
    def test_list_artifacts_by_lifecycle(self, cache_with_data):
        """Test indexed lookup by lifecycle status"""
        active = cache_with_data.list_artifacts_by_lifecycle('active')
        assert len(active) == 1
        
        development = cache_with_data.list_artifacts_by_lifecycle('development')
        assert len(development) == 1
        
        canonical = cache_with_data.list_artifacts_by_lifecycle('canonical')
        assert len(canonical) == 1
    
    def test_list_artifacts_by_topic(self, cache_with_data):
        """Test indexed lookup by topic"""
        topic1_artifacts = cache_with_data.list_artifacts_by_topic('test_topic_1')
        assert len(topic1_artifacts) == 2
        
        topic2_artifacts = cache_with_data.list_artifacts_by_topic('test_topic_2')
        assert len(topic2_artifacts) == 1
    
    def test_list_all_artifacts(self, cache_with_data):
        """Test listing all artifacts"""
        all_artifacts = cache_with_data.list_all_artifacts()
        assert len(all_artifacts) == 3


class TestRegistryCacheInvalidation:
    """Test cache invalidation"""
    
    def test_manual_invalidation(self, cache_with_data):
        """Test manual cache invalidation"""
        assert cache_with_data._loaded
        
        cache_with_data.invalidate()
        
        assert not cache_with_data._loaded
        assert len(cache_with_data._artifacts) == 0
    
    def test_automatic_refresh_on_file_modification(
        self, sample_artifact_registry, sample_domain_registry, sample_lifecycle_manager
    ):
        """Test cache automatically refreshes when registry file is modified"""
        artifact_registry = ArtifactRegistry(sample_artifact_registry)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        cache.load()
        
        # Initial state
        assert len(cache._artifacts) == 3
        assert not cache._needs_refresh()
        
        # Modify registry file
        time.sleep(0.1)  # Ensure mtime changes
        with open(sample_artifact_registry, 'r') as f:
            data = yaml.safe_load(f)
        
        # Add new artifact
        data['artifacts'].append({
            'artifact_id': 'test_artifact_4',
            'file_path': 'test4.py',
            'primary_domain': 'SIGNALS',
            'artifact_type': 'ENGINE',
            'lifecycle_status': 'active',
            'created_date': '2026-01-04',
            'last_modified': '2026-01-04',
            'owner_role': 'Test owner',
            'ssot_relationship': 'implementation',
            'allowed_writers': ['SIGNALS'],
            'allowed_readers': ['ALL']
        })
        
        with open(sample_artifact_registry, 'w') as f:
            yaml.dump(data, f)
        
        # Cache should detect modification
        assert cache._needs_refresh()
        
        # Load should refresh cache
        cache.load()
        assert len(cache._artifacts) == 4
    
    def test_force_reload(self, cache_with_data):
        """Test force reload ignores cache validity"""
        initial_count = len(cache_with_data._artifacts)
        
        # Force reload even though cache is valid
        cache_with_data.load(force=True)
        
        # Should still have same data
        assert len(cache_with_data._artifacts) == initial_count


class TestRegistryCacheIndexing:
    """Test cache indexing"""
    
    def test_domain_index_includes_secondary_domains(self, cache_with_data):
        """Test domain index includes both primary and secondary domains"""
        # test_artifact_2 has SEMANTICS as primary and SIGNALS as secondary
        signals_artifacts = cache_with_data.list_artifacts_by_domain('SIGNALS')
        
        artifact_ids = [a.artifact_id for a in signals_artifacts]
        assert 'test_artifact_1' in artifact_ids  # Primary domain
        assert 'test_artifact_2' in artifact_ids  # Secondary domain
    
    def test_indexes_updated_on_load(self, cache_with_data):
        """Test all indexes are properly populated"""
        # Check domain index
        assert 'SIGNALS' in cache_with_data._by_domain
        assert 'SEMANTICS' in cache_with_data._by_domain
        assert 'ARCH' in cache_with_data._by_domain
        
        # Check type index
        assert 'ENGINE' in cache_with_data._by_type
        assert 'SSOT' in cache_with_data._by_type
        
        # Check lifecycle index
        assert 'active' in cache_with_data._by_lifecycle
        assert 'development' in cache_with_data._by_lifecycle
        assert 'canonical' in cache_with_data._by_lifecycle
        
        # Check topic index
        assert 'test_topic_1' in cache_with_data._by_topic
        assert 'test_topic_2' in cache_with_data._by_topic


class TestRegistryCacheDomainOperations:
    """Test domain-related cache operations"""
    
    def test_get_domain(self, cache_with_data):
        """Test domain retrieval through cache"""
        domain = cache_with_data.get_domain('SIGNALS')
        
        assert domain is not None
        assert domain.domain_id == 'SIGNALS'
        assert domain.name == 'Signal Generation'
    
    def test_list_domains(self, cache_with_data):
        """Test listing all domains through cache"""
        domains = cache_with_data.list_domains()
        
        assert len(domains) == 3
        domain_ids = [d.domain_id for d in domains]
        assert 'SIGNALS' in domain_ids
        assert 'SEMANTICS' in domain_ids
        assert 'ARCH' in domain_ids


class TestRegistryCacheLifecycleOperations:
    """Test lifecycle-related cache operations"""
    
    def test_get_state_machine(self, cache_with_data):
        """Test state machine retrieval through cache"""
        sm = cache_with_data.get_state_machine('ENGINE')
        
        assert sm is not None
        assert sm.artifact_type == 'ENGINE'
        assert 'active' in sm.states
    
    def test_validate_transition(self, cache_with_data):
        """Test transition validation through cache"""
        is_valid, error = cache_with_data.validate_transition('ENGINE', 'development', 'active')
        
        assert is_valid
        assert error is None
        
        # Invalid transition
        is_valid, error = cache_with_data.validate_transition('ENGINE', 'active', 'planned')
        assert not is_valid
        assert error is not None


class TestRegistryCachePerformance:
    """Test cache performance characteristics"""
    
    def test_query_performance_with_indexes(self, cache_with_data):
        """Test that indexed queries are fast"""
        import time
        
        # Warm up cache
        cache_with_data.load()
        
        # Test indexed lookup performance
        start = time.time()
        for _ in range(1000):
            cache_with_data.get_artifact('test_artifact_1')
        elapsed = time.time() - start
        
        # Should be very fast (< 1 second for 1000 lookups)
        assert elapsed < 1.0
    
    def test_domain_query_performance(self, cache_with_data):
        """Test domain query performance"""
        import time
        
        start = time.time()
        for _ in range(1000):
            cache_with_data.list_artifacts_by_domain('SIGNALS')
        elapsed = time.time() - start
        
        # Should be fast with index
        assert elapsed < 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
