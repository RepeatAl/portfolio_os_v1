"""
Artifact registry operations
"""

import yaml
from pathlib import Path
from typing import List, Optional, Dict
from artifact_schema import ArtifactMetadata, validate_artifact_dict


class ArtifactRegistry:
    """Manages artifact registry operations"""
    
    def __init__(self, registry_path: Optional[Path] = None):
        """
        Initialize artifact registry
        
        Args:
            registry_path: Path to artifact_registry.yaml file
                          If None, uses default path relative to this file
        """
        if registry_path is None:
            # Default to .domainization/artifact_registry.yaml
            self.registry_path = Path(__file__).parent.parent / "artifact_registry.yaml"
        else:
            self.registry_path = Path(registry_path)
        
        self._artifacts: Dict[str, ArtifactMetadata] = {}
        self._loaded = False
    
    def load(self) -> None:
        """Load artifact registry from YAML file"""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")
        
        with open(self.registry_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data or 'artifacts' not in data:
            raise ValueError("Invalid registry format: missing 'artifacts' key")
        
        # Clear existing artifacts
        self._artifacts.clear()
        
        # Load artifacts
        for artifact_dict in data['artifacts']:
            metadata = self._dict_to_metadata(artifact_dict)
            self._artifacts[metadata.artifact_id] = metadata
        
        self._loaded = True
    
    def save(self) -> None:
        """Save artifact registry to YAML file"""
        if not self._loaded:
            raise RuntimeError("Registry not loaded. Call load() first.")
        
        # Convert artifacts to dict format
        artifacts_list = []
        for metadata in self._artifacts.values():
            artifact_dict = self._metadata_to_dict(metadata)
            artifacts_list.append(artifact_dict)
        
        # Sort by artifact_id for consistent output
        artifacts_list.sort(key=lambda x: x['artifact_id'])
        
        data = {'artifacts': artifacts_list}
        
        # Create timestamped backup before saving (with retention policy)
        if self.registry_path.exists():
            from registry_backup_manager import create_backup_and_cleanup
            create_backup_and_cleanup(self.registry_path)
        
        # Save to file
        with open(self.registry_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    def register_artifact(self, metadata: ArtifactMetadata) -> None:
        """
        Register a new artifact
        
        Args:
            metadata: Artifact metadata
        
        Raises:
            ValueError: If artifact_id already exists or metadata is invalid
        """
        if not self._loaded:
            self.load()
        
        # Validate metadata
        is_valid, errors = metadata.validate()
        if not is_valid:
            raise ValueError(f"Invalid metadata: {', '.join(errors)}")
        
        # Check for duplicate artifact_id
        if metadata.artifact_id in self._artifacts:
            raise ValueError(f"Artifact with ID '{metadata.artifact_id}' already exists")
        
        # Add to registry
        self._artifacts[metadata.artifact_id] = metadata
    
    def update_artifact(self, artifact_id: str, metadata: ArtifactMetadata) -> None:
        """
        Update existing artifact metadata
        
        Args:
            artifact_id: ID of artifact to update
            metadata: New metadata
        
        Raises:
            ValueError: If artifact not found or metadata is invalid
        """
        if not self._loaded:
            self.load()
        
        # Check artifact exists
        if artifact_id not in self._artifacts:
            raise ValueError(f"Artifact with ID '{artifact_id}' not found")
        
        # Validate metadata
        is_valid, errors = metadata.validate()
        if not is_valid:
            raise ValueError(f"Invalid metadata: {', '.join(errors)}")
        
        # Ensure artifact_id matches
        if metadata.artifact_id != artifact_id:
            raise ValueError(f"Metadata artifact_id '{metadata.artifact_id}' does not match '{artifact_id}'")
        
        # Update registry
        self._artifacts[artifact_id] = metadata
    
    def get_artifact(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        """
        Retrieve artifact by ID
        
        Args:
            artifact_id: ID of artifact to retrieve
        
        Returns:
            ArtifactMetadata if found, None otherwise
        """
        if not self._loaded:
            self.load()
        
        return self._artifacts.get(artifact_id)
    
    def list_artifacts_by_domain(self, domain_id: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts for a domain
        
        Args:
            domain_id: Domain ID to filter by
        
        Returns:
            List of artifacts in the domain
        """
        if not self._loaded:
            self.load()
        
        return [
            artifact for artifact in self._artifacts.values()
            if artifact.primary_domain == domain_id or
               (artifact.secondary_domains and domain_id in artifact.secondary_domains)
        ]
    
    def list_artifacts_by_type(self, artifact_type: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts of a specific type
        
        Args:
            artifact_type: Artifact type to filter by
        
        Returns:
            List of artifacts of the specified type
        """
        if not self._loaded:
            self.load()
        
        return [
            artifact for artifact in self._artifacts.values()
            if artifact.artifact_type == artifact_type
        ]
    
    def list_artifacts_by_lifecycle(self, lifecycle_status: str) -> List[ArtifactMetadata]:
        """
        Get all artifacts in a specific lifecycle state
        
        Args:
            lifecycle_status: Lifecycle status to filter by
        
        Returns:
            List of artifacts in the specified lifecycle state
        """
        if not self._loaded:
            self.load()
        
        return [
            artifact for artifact in self._artifacts.values()
            if artifact.lifecycle_status == lifecycle_status
        ]
    
    def list_all_artifacts(self) -> List[ArtifactMetadata]:
        """
        Get all artifacts in registry
        
        Returns:
            List of all artifacts
        """
        if not self._loaded:
            self.load()
        
        return list(self._artifacts.values())
    
    @staticmethod
    def parse_frontmatter(file_path: Path) -> Optional[Dict]:
        """
        Parse YAML frontmatter from markdown file
        
        Args:
            file_path: Path to markdown file
        
        Returns:
            Dictionary of frontmatter metadata, or None if no frontmatter
        """
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML frontmatter (starts with ---)
        if not content.startswith('---'):
            return None
        
        # Find end of frontmatter
        lines = content.split('\n')
        end_index = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_index = i
                break
        
        if end_index is None:
            return None
        
        # Extract and parse frontmatter
        frontmatter_text = '\n'.join(lines[1:end_index])
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter if frontmatter else None
        except yaml.YAMLError:
            return None
    
    def _dict_to_metadata(self, artifact_dict: dict) -> ArtifactMetadata:
        """Convert dictionary to ArtifactMetadata object"""
        return ArtifactMetadata(
            artifact_id=artifact_dict['artifact_id'],
            file_path=artifact_dict['file_path'],
            primary_domain=artifact_dict['primary_domain'],
            artifact_type=artifact_dict['artifact_type'],
            lifecycle_status=artifact_dict['lifecycle_status'],
            created_date=artifact_dict['created_date'],
            last_modified=artifact_dict['last_modified'],
            owner_role=artifact_dict['owner_role'],
            ssot_relationship=artifact_dict['ssot_relationship'],
            allowed_writers=artifact_dict['allowed_writers'],
            allowed_readers=artifact_dict['allowed_readers'],
            secondary_domains=artifact_dict.get('secondary_domains'),
            dependencies=artifact_dict.get('dependencies'),
            topic=artifact_dict.get('topic'),
            description=artifact_dict.get('description'),
            tags=artifact_dict.get('tags')
        )
    
    def _metadata_to_dict(self, metadata: ArtifactMetadata) -> dict:
        """Convert ArtifactMetadata object to dictionary"""
        artifact_dict = {
            'artifact_id': metadata.artifact_id,
            'file_path': metadata.file_path,
            'primary_domain': metadata.primary_domain,
            'artifact_type': metadata.artifact_type,
            'lifecycle_status': metadata.lifecycle_status,
            'created_date': metadata.created_date,
            'last_modified': metadata.last_modified,
            'owner_role': metadata.owner_role,
            'ssot_relationship': metadata.ssot_relationship,
            'allowed_writers': metadata.allowed_writers,
            'allowed_readers': metadata.allowed_readers
        }
        
        # Add optional fields if present
        if metadata.secondary_domains:
            artifact_dict['secondary_domains'] = metadata.secondary_domains
        if metadata.dependencies:
            artifact_dict['dependencies'] = metadata.dependencies
        if metadata.topic:
            artifact_dict['topic'] = metadata.topic
        if metadata.description:
            artifact_dict['description'] = metadata.description
        if metadata.tags:
            artifact_dict['tags'] = metadata.tags
        
        return artifact_dict
