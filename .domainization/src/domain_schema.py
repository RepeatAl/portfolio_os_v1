"""
Domain definition schema and validation
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DomainDefinition:
    """Domain definition schema"""
    
    # Required fields
    domain_id: str
    name: str
    responsibility_scope: str
    allowed_artifact_types: List[str]
    cannot_own: List[str]
    priority: str  # "core" or "surface"
    
    # Optional fields
    authority_level: Optional[int] = None  # 1-4 for core reasoning chain, None for surface domains
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate domain definition completeness and correctness
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields are not empty
        if not self.domain_id:
            errors.append("domain_id is required")
        if not self.name:
            errors.append("name is required")
        if not self.responsibility_scope:
            errors.append("responsibility_scope is required")
        if not self.allowed_artifact_types:
            errors.append("allowed_artifact_types is required")
        if self.cannot_own is None:
            errors.append("cannot_own is required (can be empty list)")
        if not self.priority:
            errors.append("priority is required")
        
        # Validate priority
        valid_priorities = ['core', 'surface']
        if self.priority and self.priority not in valid_priorities:
            errors.append(f"priority must be one of {valid_priorities}")
        
        # Validate authority_level
        if self.authority_level is not None:
            if not isinstance(self.authority_level, int):
                errors.append("authority_level must be an integer or null")
            elif self.authority_level < 1 or self.authority_level > 4:
                errors.append("authority_level must be between 1 and 4 for core domains")
            elif self.priority == 'surface':
                errors.append("surface domains should not have authority_level (should be null)")
        
        # Core domains should have authority_level
        if self.priority == 'core' and self.authority_level is None:
            errors.append("core domains must have authority_level (1-4)")
        
        # Validate lists are actually lists
        if self.allowed_artifact_types and not isinstance(self.allowed_artifact_types, list):
            errors.append("allowed_artifact_types must be a list")
        
        if self.cannot_own and not isinstance(self.cannot_own, list):
            errors.append("cannot_own must be a list")
        
        # Check for conflicts between allowed and cannot_own
        if self.allowed_artifact_types and self.cannot_own:
            conflicts = set(self.allowed_artifact_types) & set(self.cannot_own)
            if conflicts:
                errors.append(f"Artifact types cannot be both allowed and forbidden: {conflicts}")
        
        return (len(errors) == 0, errors)
    
    def can_own_type(self, artifact_type: str) -> bool:
        """
        Check if domain can own artifact type
        
        Args:
            artifact_type: The artifact type to check
        
        Returns:
            True if domain can own this type, False otherwise
        """
        if artifact_type in self.cannot_own:
            return False
        return artifact_type in self.allowed_artifact_types
    
    def is_core_domain(self) -> bool:
        """
        Check if this is a core reasoning domain
        
        Returns:
            True if core domain, False if surface domain
        """
        return self.priority == "core"
    
    def get_authority_level(self) -> int:
        """
        Get authority level in reasoning chain
        
        Returns:
            Authority level (1=highest for SIGNALS, 4=lowest for REPORT)
            Returns 999 for surface domains (no authority in reasoning chain)
        """
        return self.authority_level if self.authority_level is not None else 999


def validate_domain_dict(domain_dict: dict) -> tuple[bool, List[str]]:
    """
    Validate domain dictionary against schema
    
    Args:
        domain_dict: Dictionary containing domain definition
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields exist
    required_fields = [
        'domain_id', 'name', 'responsibility_scope',
        'allowed_artifact_types', 'cannot_own', 'priority'
    ]
    
    for field in required_fields:
        if field not in domain_dict:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return (False, errors)
    
    # Create domain object and validate
    try:
        domain = DomainDefinition(
            domain_id=domain_dict['domain_id'],
            name=domain_dict['name'],
            responsibility_scope=domain_dict['responsibility_scope'],
            allowed_artifact_types=domain_dict['allowed_artifact_types'],
            cannot_own=domain_dict['cannot_own'],
            priority=domain_dict['priority'],
            authority_level=domain_dict.get('authority_level')
        )
        
        return domain.validate()
    
    except Exception as e:
        return (False, [f"Error creating domain object: {str(e)}"])
