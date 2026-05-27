"""
Performance tests for registry cache

Verifies that cache meets performance requirements:
- < 5 second validation time for 1000 artifacts
- Efficient indexed queries
- Fast cache loading
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


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def create_large_artifact_registry(registry_path: Path, num_artifacts: int):
    """
    Create artifact registry with specified number of artifacts
    
    Args:
        registry_path: Path to registry file
        num_artifacts: Number of artifacts to create
    """
    domains = ['SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT', 'ARCH', 'STATE', 'DATA']
    types = ['ENGINE', 'SSOT', 'DATA_OUT', 'REPORT_OUT', 'CONFIG']
    lifecycles = ['active', 'development', 'canonical', 'deprecated']
    
    artifacts = []
    for i in range(num_artifacts):
        artifact = {
            'artifact_id': f'artifact_{i:05d}',
            'file_path': f'test/artifact_{i:05d}.py',
            'primary_domain': domains[i % len(domains)],
            'artifact_type': types[i % len(types)],
            'lifecycle_status': lifecycles[i % len(lifecycles)],
            'created_date': '2026-01-01',
            'last_modified': '2026-01-01',
            'owner_role': f'Owner {i}',
            'ssot_relationship': 'implementation',
            'allowed_writers': [domains[i % len(domains)]],
            'allowed_readers': ['ALL'],
            'topic': f'topic_{i % 100}'  # 100 different topics
        }
        
        # Add secondary domains to some artifacts
        if i % 3 == 0:
            artifact['secondary_domains'] = [domains[(i + 1) % len(domains)]]
        
        artifacts.append(artifact)
    
    data = {'artifacts': artifacts}
    
    with open(registry_path, 'w') as f:
        yaml.dump(data, f)


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
                'domain_id': 'REASONING',
                'name': 'Reasoning',
                'responsibility_scope': 'Reasoning logic',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT'],
                'cannot_own': ['SSOT', 'REPORT_OUT'],
                'priority': 'core',
                'authority_level': 3
            },
            {
                'domain_id': 'REPORT',
                'name': 'Report Generation',
                'responsibility_scope': 'Generate reports',
                'allowed_artifact_types': ['ENGINE', 'REPORT_OUT'],
                'cannot_own': ['SSOT'],
                'priority': 'core',
                'authority_level': 4
            },
            {
                'domain_id': 'ARCH',
                'name': 'Architecture',
                'responsibility_scope': 'System architecture',
                'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                'cannot_own': ['REPORT_OUT'],
                'priority': 'surface'
            },
            {
                'domain_id': 'STATE',
                'name': 'State Management',
                'responsibility_scope': 'Portfolio state',
                'allowed_artifact_types': ['DATA_OUT', 'CONFIG'],
                'cannot_own': ['SSOT', 'ENGINE'],
                'priority': 'surface'
            },
            {
                'domain_id': 'DATA',
                'name': 'Data Management',
                'responsibility_scope': 'Data processing',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT'],
                'cannot_own': ['SSOT', 'REPORT_OUT'],
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
            },
            'DATA_OUT': {
                'description': 'Data output files',
                'states': ['generated', 'current', 'archived'],
                'initial_state': 'generated',
                'transitions': [
                    {'from': 'generated', 'to': 'current', 'condition': 'Becomes latest'},
                    {'from': 'current', 'to': 'archived', 'condition': 'Superseded'}
                ],
                'modifiable_states': ['generated', 'current'],
                'read_only_states': ['archived']
            },
            'REPORT_OUT': {
                'description': 'Report output files',
                'states': ['generated', 'current', 'archived'],
                'initial_state': 'generated',
                'transitions': [
                    {'from': 'generated', 'to': 'current', 'condition': 'Becomes latest'},
                    {'from': 'current', 'to': 'archived', 'condition': 'Superseded'}
                ],
                'modifiable_states': ['generated', 'current'],
                'read_only_states': ['archived']
            },
            'CONFIG': {
                'description': 'Configuration files',
                'states': ['draft', 'active', 'deprecated'],
                'initial_state': 'draft',
                'transitions': [
                    {'from': 'draft', 'to': 'active', 'condition': 'Activated'},
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                ],
                'modifiable_states': ['draft', 'active'],
                'read_only_states': ['deprecated']
            }
        }
    }
    
    with open(sm_path, 'w') as f:
        yaml.dump(data, f)
    
    return sm_path


class TestCacheLoadingPerformance:
    """Test cache loading performance"""
    
    def test_load_100_artifacts(self, temp_dir, sample_domain_registry, sample_lifecycle_manager):
        """Test loading cache with 100 artifacts"""
        registry_path = temp_dir / "artifact_registry.yaml"
        create_large_artifact_registry(registry_path, 100)
        
        artifact_registry = ArtifactRegistry(registry_path)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        
        start = time.time()
        cache.load()
        elapsed = time.time() - start
        
        print(f"\nLoad time for 100 artifacts: {elapsed:.3f}s")
        assert elapsed < 1.0  # Should load in < 1 second
        assert len(cache._artifacts) == 100
    
    def test_load_1000_artifacts(self, temp_dir, sample_domain_registry, sample_lifecycle_manager):
        """Test loading cache with 1000 artifacts"""
        registry_path = temp_dir / "artifact_registry.yaml"
        create_large_artifact_registry(registry_path, 1000)
        
        artifact_registry = ArtifactRegistry(registry_path)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        
        start = time.time()
        cache.load()
        elapsed = time.time() - start
        
        print(f"\nLoad time for 1000 artifacts: {elapsed:.3f}s")
        assert elapsed < 5.0  # REQUIREMENT: < 5 seconds for 1000 artifacts
        assert len(cache._artifacts) == 1000


class TestQueryPerformance:
    """Test query performance with large datasets"""
    
    @pytest.fixture
    def cache_1000_artifacts(self, temp_dir, sample_domain_registry, sample_lifecycle_manager):
        """Create cache with 1000 artifacts"""
        registry_path = temp_dir / "artifact_registry.yaml"
        create_large_artifact_registry(registry_path, 1000)
        
        artifact_registry = ArtifactRegistry(registry_path)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        cache.load()
        
        return cache
    
    def test_get_artifact_performance(self, cache_1000_artifacts):
        """Test artifact lookup performance"""
        # Warm up
        cache_1000_artifacts.get_artifact('artifact_00000')
        
        # Test 1000 lookups
        start = time.time()
        for i in range(1000):
            cache_1000_artifacts.get_artifact(f'artifact_{i:05d}')
        elapsed = time.time() - start
        
        print(f"\n1000 artifact lookups: {elapsed:.3f}s ({elapsed/1000*1000:.3f}ms per lookup)")
        assert elapsed < 0.5  # Should be very fast with O(1) lookup
    
    def test_domain_query_performance(self, cache_1000_artifacts):
        """Test domain query performance"""
        # Warm up
        cache_1000_artifacts.list_artifacts_by_domain('SIGNALS')
        
        # Test 100 domain queries
        start = time.time()
        for _ in range(100):
            cache_1000_artifacts.list_artifacts_by_domain('SIGNALS')
        elapsed = time.time() - start
        
        print(f"\n100 domain queries: {elapsed:.3f}s ({elapsed/100*1000:.3f}ms per query)")
        assert elapsed < 0.5  # Should be fast with indexed lookup
    
    def test_type_query_performance(self, cache_1000_artifacts):
        """Test artifact type query performance"""
        # Test 100 type queries
        start = time.time()
        for _ in range(100):
            cache_1000_artifacts.list_artifacts_by_type('ENGINE')
        elapsed = time.time() - start
        
        print(f"\n100 type queries: {elapsed:.3f}s ({elapsed/100*1000:.3f}ms per query)")
        assert elapsed < 0.5
    
    def test_lifecycle_query_performance(self, cache_1000_artifacts):
        """Test lifecycle query performance"""
        # Test 100 lifecycle queries
        start = time.time()
        for _ in range(100):
            cache_1000_artifacts.list_artifacts_by_lifecycle('active')
        elapsed = time.time() - start
        
        print(f"\n100 lifecycle queries: {elapsed:.3f}s ({elapsed/100*1000:.3f}ms per query)")
        assert elapsed < 0.5
    
    def test_topic_query_performance(self, cache_1000_artifacts):
        """Test topic query performance"""
        # Test 100 topic queries
        start = time.time()
        for _ in range(100):
            cache_1000_artifacts.list_artifacts_by_topic('topic_0')
        elapsed = time.time() - start
        
        print(f"\n100 topic queries: {elapsed:.3f}s ({elapsed/100*1000:.3f}ms per query)")
        assert elapsed < 0.5


class TestValidationPerformance:
    """Test validation performance with cache"""
    
    @pytest.fixture
    def cache_1000_artifacts(self, temp_dir, sample_domain_registry, sample_lifecycle_manager):
        """Create cache with 1000 artifacts"""
        registry_path = temp_dir / "artifact_registry.yaml"
        create_large_artifact_registry(registry_path, 1000)
        
        artifact_registry = ArtifactRegistry(registry_path)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        cache.load()
        
        return cache
    
    def test_simulated_validation_performance(self, cache_1000_artifacts):
        """
        Simulate validation of all artifacts
        
        This simulates what would happen during commit gate validation:
        - Check each artifact exists
        - Validate domain assignment
        - Check lifecycle state
        """
        start = time.time()
        
        # Simulate validation of all 1000 artifacts
        for i in range(1000):
            artifact_id = f'artifact_{i:05d}'
            
            # Get artifact (O(1))
            artifact = cache_1000_artifacts.get_artifact(artifact_id)
            
            if artifact:
                # Get domain (O(1))
                domain = cache_1000_artifacts.get_domain(artifact.primary_domain)
                
                # Get state machine (O(1))
                sm = cache_1000_artifacts.get_state_machine(artifact.artifact_type)
        
        elapsed = time.time() - start
        
        print(f"\nValidation simulation for 1000 artifacts: {elapsed:.3f}s")
        print(f"Average per artifact: {elapsed/1000*1000:.3f}ms")
        
        # REQUIREMENT: < 5 seconds for 1000 artifacts
        assert elapsed < 5.0
    
    def test_complex_query_performance(self, cache_1000_artifacts):
        """Test performance of complex multi-index queries"""
        start = time.time()
        
        # Simulate complex validation queries
        for _ in range(10):
            # Get all artifacts by domain
            signals = cache_1000_artifacts.list_artifacts_by_domain('SIGNALS')
            
            # Filter by lifecycle
            active_signals = [a for a in signals if a.lifecycle_status == 'active']
            
            # Filter by type
            signal_engines = [a for a in active_signals if a.artifact_type == 'ENGINE']
        
        elapsed = time.time() - start
        
        print(f"\n10 complex queries: {elapsed:.3f}s ({elapsed/10*1000:.3f}ms per query)")
        assert elapsed < 1.0


class TestCacheInvalidationPerformance:
    """Test cache invalidation performance"""
    
    def test_invalidation_speed(self, temp_dir, sample_domain_registry, sample_lifecycle_manager):
        """Test cache invalidation is fast"""
        registry_path = temp_dir / "artifact_registry.yaml"
        create_large_artifact_registry(registry_path, 1000)
        
        artifact_registry = ArtifactRegistry(registry_path)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        cache.load()
        
        # Test invalidation speed
        start = time.time()
        cache.invalidate()
        elapsed = time.time() - start
        
        print(f"\nCache invalidation: {elapsed*1000:.3f}ms")
        assert elapsed < 0.1  # Should be very fast
    
    def test_reload_after_modification(self, temp_dir, sample_domain_registry, sample_lifecycle_manager):
        """Test reload performance after file modification"""
        registry_path = temp_dir / "artifact_registry.yaml"
        create_large_artifact_registry(registry_path, 1000)
        
        artifact_registry = ArtifactRegistry(registry_path)
        domain_registry = DomainRegistry(sample_domain_registry)
        lifecycle_manager = LifecycleManager(sample_lifecycle_manager)
        
        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        cache.load()
        
        # Modify file
        time.sleep(0.1)
        with open(registry_path, 'a') as f:
            f.write('\n# Modified\n')
        
        # Test reload performance
        start = time.time()
        cache.load()
        elapsed = time.time() - start
        
        print(f"\nCache reload after modification: {elapsed:.3f}s")
        assert elapsed < 5.0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
