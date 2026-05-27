"""
Artifact metadata schema validation
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ArtifactMetadata:
    """Artifact metadata schema"""
    
    # Required fields
    artifact_id: str
    file_path: str
    primary_domain: str
    artifact_type: str
    lifecycle_status: str
    created_date: str
    last_modified: str
    owner_role: str
    ssot_relationship: str
    allowed_writers: List[str]
    allowed_readers: List[str]
    
    # Optional fields
    secondary_domains: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None
    topic: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate metadata completeness and correctness
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields are not empty
        if not self.artifact_id:
            errors.append("artifact_id is required")
        if not self.file_path:
            errors.append("file_path is required")
        if not self.primary_domain:
            errors.append("primary_domain is required")
        if not self.artifact_type:
            errors.append("artifact_type is required")
        if not self.lifecycle_status:
            errors.append("lifecycle_status is required")
        if not self.created_date:
            errors.append("created_date is required")
        if not self.last_modified:
            errors.append("last_modified is required")
        if not self.owner_role:
            errors.append("owner_role is required")
        if not self.ssot_relationship:
            errors.append("ssot_relationship is required")
        if not self.allowed_writers:
            errors.append("allowed_writers is required")
        if not self.allowed_readers:
            errors.append("allowed_readers is required")
        
        # Validate date formats
        if self.created_date:
            if not self._is_valid_date(self.created_date):
                errors.append(f"created_date must be in YYYY-MM-DD format: {self.created_date}")
        
        if self.last_modified:
            if not self._is_valid_date(self.last_modified):
                errors.append(f"last_modified must be in YYYY-MM-DD format: {self.last_modified}")
        
        # Validate ssot_relationship
        valid_relationships = ['canonical', 'derived', 'implementation', 'none']
        if self.ssot_relationship and self.ssot_relationship not in valid_relationships:
            errors.append(f"ssot_relationship must be one of {valid_relationships}")
        
        # Validate lists are actually lists
        if self.allowed_writers and not isinstance(self.allowed_writers, list):
            errors.append("allowed_writers must be a list")
        
        if self.allowed_readers and not isinstance(self.allowed_readers, list):
            errors.append("allowed_readers must be a list")
        
        if self.secondary_domains and not isinstance(self.secondary_domains, list):
            errors.append("secondary_domains must be a list")
        
        if self.dependencies and not isinstance(self.dependencies, list):
            errors.append("dependencies must be a list")
        
        if self.tags and not isinstance(self.tags, list):
            errors.append("tags must be a list")
        
        return (len(errors) == 0, errors)
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Check if date string is in YYYY-MM-DD format"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def is_modifiable(self) -> bool:
        """Check if artifact can be modified based on lifecycle status"""
        # Deprecated and archived artifacts are read-only
        readonly_states = ['deprecated', 'archived', 'superseded']
        return self.lifecycle_status not in readonly_states
    
    def can_write(self, domain_id: str) -> bool:
        """Check if domain has write permission"""
        return domain_id in self.allowed_writers
    
    def can_read(self, domain_id: str) -> bool:
        """Check if domain has read permission"""
        return "ALL" in self.allowed_readers or domain_id in self.allowed_readers


def validate_artifact_dict(artifact_dict: dict) -> tuple[bool, List[str]]:
    """
    Validate artifact dictionary against schema
    
    Args:
        artifact_dict: Dictionary containing artifact metadata
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields exist
    required_fields = [
        'artifact_id', 'file_path', 'primary_domain', 'artifact_type',
        'lifecycle_status', 'created_date', 'last_modified', 'owner_role',
        'ssot_relationship', 'allowed_writers', 'allowed_readers'
    ]
    
    for field in required_fields:
        if field not in artifact_dict:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return (False, errors)
    
    # Create metadata object and validate
    try:
        metadata = ArtifactMetadata(
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
        
        return metadata.validate()
    
    except Exception as e:
        return (False, [f"Error creating metadata object: {str(e)}"])
