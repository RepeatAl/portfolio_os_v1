"""
Registry cache for performance optimization

Provides in-memory caching with indexes for fast artifact queries.
Automatically invalidates cache when registry files are modified.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Set
from collections import defaultdict
from artifact_schema import ArtifactMetadata
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager


class RegistryCache:
    """
    In-memory cache for registry data with automatic invalidation
    
    Provides indexed access to artifacts for fast queries:
    - By artifact_id (O(1) lookup)
    - By domain_id (O(1) lookup)
    - By artifact_type (O(1) lookup)
    - By lifecycle_status (O(1) lookup)
    - By topic (O(1) lookup)
    """
    
    def __init__(
        self,
        artifact_registry: Optional[ArtifactRegistry] = None,
        domain_registry: Optional[DomainRegistry] = None,
        lifecycle_manager: Optional[LifecycleManager] = None
    ):
        """
        Initialize registry cache
        
        Args:
            artifact_registry: ArtifactRegistry instance (creates default if None)
            domain_registry: DomainRegistry instance (creates default if None)
            lifecycle_manager: LifecycleManager instance (creates default if None)
        """
        self.artifact_registry = artifact_registry or ArtifactRegistry()
        self.domain_registry = domain_registry or DomainRegistry()
        self.lifecycle_manager = lifecycle_manager or LifecycleManager()
        
        # Cache storage
        self._artifacts: Dict[str, ArtifactMetadata] = {}
        
        # Indexes for fast lookups
        self._by_domain: Dict[str, Set[str]] = defaultdict(set)
        self._by_type: Dict[str, Set[str]] = defaultdict(set)
        self._by_lifecycle: Dict[str, Set[str]] = defaultdict(set)
        self._by_topic: Dict[str, Set[str]] = defaultdict(set)
        
        # File modification times for cache invalidation
        self._artifact_registry_mtime: Optional[float] = None
        self._domain_registry_mtime: Optional[float] = None
        self._lifecycle_manager_mtime: Optional[float] = None
        
        # Cache state
        self._loaded = False
    
    def load(self, force: bool = False) -> None:
        """
        Load registries into cache
        
        Args:
            force: If True, reload even if cache is valid
        """
        # Check if cache needs refresh
        if not force and self._loaded and not self._needs_refresh():
            return
        
        # Load registries
        self.artifact_registry.load()
        self.domain_registry.load()
        self.lifecycle_manager.load()
        
        # Clear existing cache
        self._clear_cache()
        
        # Build cache from artifact registry
        for artifact in self.artifact_registry.list_all_artifacts():
            self._add_to_cache(artifact)
        
        # Update modification times
        self._update_mtimes()
        
        self._loaded = True
    
    def invalidate(self) -> None:
        """Force cache invalidation on next access"""
        self._loaded = False
        self._clear_cache()

    
    def get_artifact(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        """
        Get artifact by ID (O(1) lookup)
        
        Args:
            artifact_id: Artifact ID to retrieve
        
        Returns:
            ArtifactMetadata if found, None otherwise
        """
        self.load()
        return self._artifacts.get(artifact_id)
    
    def list_artifacts_by_domain(self, domain_id: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts for a domain (O(1) index lookup)
        
        Args:
            domain_id: Domain ID to filter by
        
        Returns:
            List of artifacts in the domain
        """
        self.load()
        artifact_ids = self._by_domain.get(domain_id, set())
        return [self._artifacts[aid] for aid in artifact_ids if aid in self._artifacts]
    
    def list_artifacts_by_type(self, artifact_type: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts of a specific type (O(1) index lookup)
        
        Args:
            artifact_type: Artifact type to filter by
        
        Returns:
            List of artifacts of the specified type
        """
        self.load()
        artifact_ids = self._by_type.get(artifact_type, set())
        return [self._artifacts[aid] for aid in artifact_ids if aid in self._artifacts]
    
    def list_artifacts_by_lifecycle(self, lifecycle_status: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts in a specific lifecycle state (O(1) index lookup)
        
        Args:
            lifecycle_status: Lifecycle status to filter by
        
        Returns:
            List of artifacts in the specified lifecycle state
        """
        self.load()
        artifact_ids = self._by_lifecycle.get(lifecycle_status, set())
        return [self._artifacts[aid] for aid in artifact_ids if aid in self._artifacts]
    
    def list_artifacts_by_topic(self, topic: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts for a topic (O(1) index lookup)
        
        Args:
            topic: Topic to filter by
        
        Returns:
            List of artifacts with the specified topic
        """
        self.load()
        artifact_ids = self._by_topic.get(topic, set())
        return [self._artifacts[aid] for aid in artifact_ids if aid in self._artifacts]
    
    def list_all_artifacts(self) -> List[ArtifactMetadata]:
        """
        Get all artifacts
        
        Returns:
            List of all artifacts
        """
        self.load()
        return list(self._artifacts.values())
    
    def get_domain(self, domain_id: str):
        """
        Get domain definition
        
        Args:
            domain_id: Domain ID to retrieve
        
        Returns:
            DomainDefinition if found, None otherwise
        """
        self.load()
        return self.domain_registry.get_domain(domain_id)
    
    def list_domains(self):
        """Get all domains"""
        self.load()
        return self.domain_registry.list_domains()
    
    def get_state_machine(self, artifact_type: str):
        """
        Get state machine for artifact type
        
        Args:
            artifact_type: Artifact type
        
        Returns:
            StateMachine if found, None otherwise
        """
        self.load()
        return self.lifecycle_manager.get_state_machine(artifact_type)
    
    def validate_transition(self, artifact_type: str, from_state: str, to_state: str):
        """
        Validate lifecycle transition
        
        Args:
            artifact_type: Artifact type
            from_state: Current state
            to_state: Target state
        
        Returns:
            (is_valid, error_message)
        """
        self.load()
        return self.lifecycle_manager.validate_transition(artifact_type, from_state, to_state)
    
    def get_statistics(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        self.load()
        
        return {
            'total_artifacts': len(self._artifacts),
            'domains': len(self._by_domain),
            'artifact_types': len(self._by_type),
            'lifecycle_states': len(self._by_lifecycle),
            'topics': len(self._by_topic),
            'cache_loaded': self._loaded,
            'needs_refresh': self._needs_refresh()
        }
    
    def _add_to_cache(self, artifact: ArtifactMetadata) -> None:
        """
        Add artifact to cache and update indexes
        
        Args:
            artifact: Artifact to add
        """
        artifact_id = artifact.artifact_id
        
        # Add to main cache
        self._artifacts[artifact_id] = artifact
        
        # Update domain index (primary and secondary)
        self._by_domain[artifact.primary_domain].add(artifact_id)
        if artifact.secondary_domains:
            for domain in artifact.secondary_domains:
                self._by_domain[domain].add(artifact_id)
        
        # Update type index
        self._by_type[artifact.artifact_type].add(artifact_id)
        
        # Update lifecycle index
        self._by_lifecycle[artifact.lifecycle_status].add(artifact_id)
        
        # Update topic index
        if artifact.topic:
            self._by_topic[artifact.topic].add(artifact_id)
    
    def _clear_cache(self) -> None:
        """Clear all cache data and indexes"""
        self._artifacts.clear()
        self._by_domain.clear()
        self._by_type.clear()
        self._by_lifecycle.clear()
        self._by_topic.clear()
    
    def _needs_refresh(self) -> bool:
        """
        Check if cache needs refresh based on file modification times
        
        Returns:
            True if any registry file has been modified
        """
        # Check artifact registry
        if self._file_modified(
            self.artifact_registry.registry_path,
            self._artifact_registry_mtime
        ):
            return True
        
        # Check domain registry
        if self._file_modified(
            self.domain_registry.registry_path,
            self._domain_registry_mtime
        ):
            return True
        
        # Check lifecycle manager
        if self._file_modified(
            self.lifecycle_manager.state_machine_path,
            self._lifecycle_manager_mtime
        ):
            return True
        
        return False
    
    def _file_modified(self, file_path: Path, cached_mtime: Optional[float]) -> bool:
        """
        Check if file has been modified since cached time
        
        Args:
            file_path: Path to file
            cached_mtime: Cached modification time
        
        Returns:
            True if file has been modified or doesn't exist
        """
        if not file_path.exists():
            return True
        
        if cached_mtime is None:
            return True
        
        current_mtime = os.path.getmtime(file_path)
        return current_mtime > cached_mtime
    
    def _update_mtimes(self) -> None:
        """Update cached modification times for all registry files"""
        if self.artifact_registry.registry_path.exists():
            self._artifact_registry_mtime = os.path.getmtime(
                self.artifact_registry.registry_path
            )
        
        if self.domain_registry.registry_path.exists():
            self._domain_registry_mtime = os.path.getmtime(
                self.domain_registry.registry_path
            )
        
        if self.lifecycle_manager.state_machine_path.exists():
            self._lifecycle_manager_mtime = os.path.getmtime(
                self.lifecycle_manager.state_machine_path
            )
