"""
Domain registry operations
"""

import yaml
from pathlib import Path
from typing import List, Optional, Dict
from domain_schema import DomainDefinition, validate_domain_dict


class DomainRegistry:
    """Manages domain registry operations"""
    
    def __init__(self, registry_path: Optional[Path] = None):
        """
        Initialize domain registry
        
        Args:
            registry_path: Path to domain_registry.yaml file
                          If None, uses default path relative to this file
        """
        if registry_path is None:
            # Default to .domainization/domain_registry.yaml
            self.registry_path = Path(__file__).parent.parent / "domain_registry.yaml"
        else:
            self.registry_path = Path(registry_path)
        
        self._domains: Dict[str, DomainDefinition] = {}
        self._loaded = False
    
    def load(self) -> None:
        """Load domain registry from YAML file"""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")
        
        with open(self.registry_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data or 'domains' not in data:
            raise ValueError("Invalid registry format: missing 'domains' key")
        
        # Clear existing domains
        self._domains.clear()
        
        # Load domains
        for domain_dict in data['domains']:
            domain = self._dict_to_domain(domain_dict)
            
            # Validate domain
            is_valid, errors = domain.validate()
            if not is_valid:
                raise ValueError(f"Invalid domain '{domain.domain_id}': {', '.join(errors)}")
            
            self._domains[domain.domain_id] = domain
        
        self._loaded = True
    
    def get_domain(self, domain_id: str) -> Optional[DomainDefinition]:
        """
        Retrieve domain by ID
        
        Args:
            domain_id: Domain ID to retrieve
        
        Returns:
            DomainDefinition if found, None otherwise
        """
        if not self._loaded:
            self.load()
        
        return self._domains.get(domain_id)
    
    def list_domains(self) -> List[DomainDefinition]:
        """
        Get all domains
        
        Returns:
            List of all domain definitions
        """
        if not self._loaded:
            self.load()
        
        return list(self._domains.values())
    
    def list_core_domains(self) -> List[DomainDefinition]:
        """
        Get all core reasoning domains
        
        Returns:
            List of core domain definitions (priority='core')
        """
        if not self._loaded:
            self.load()
        
        return [
            domain for domain in self._domains.values()
            if domain.is_core_domain()
        ]
    
    def list_surface_domains(self) -> List[DomainDefinition]:
        """
        Get all surface domains
        
        Returns:
            List of surface domain definitions (priority='surface')
        """
        if not self._loaded:
            self.load()
        
        return [
            domain for domain in self._domains.values()
            if not domain.is_core_domain()
        ]
    
    def validate_domain_assignment(self, artifact_type: str, domain_id: str) -> tuple[bool, Optional[str]]:
        """
        Check if domain can own artifact type
        
        Args:
            artifact_type: The artifact type to check
            domain_id: The domain ID to check
        
        Returns:
            (is_valid, error_message)
            error_message is None if valid
        """
        if not self._loaded:
            self.load()
        
        # Check domain exists
        domain = self._domains.get(domain_id)
        if domain is None:
            return (False, f"Domain '{domain_id}' does not exist")
        
        # Check if domain can own this type
        if not domain.can_own_type(artifact_type):
            # Find valid domains for this type
            valid_domains = [
                d.domain_id for d in self._domains.values()
                if d.can_own_type(artifact_type)
            ]
            
            if valid_domains:
                return (False, f"Domain '{domain_id}' cannot own artifact type '{artifact_type}'. Valid domains: {', '.join(valid_domains)}")
            else:
                return (False, f"No domain can own artifact type '{artifact_type}'")
        
        return (True, None)
    
    def get_valid_domains_for_type(self, artifact_type: str) -> List[str]:
        """
        Get list of domain IDs that can own an artifact type
        
        Args:
            artifact_type: The artifact type to check
        
        Returns:
            List of domain IDs that can own this type
        """
        if not self._loaded:
            self.load()
        
        return [
            domain.domain_id for domain in self._domains.values()
            if domain.can_own_type(artifact_type)
        ]
    
    def get_core_reasoning_chain(self) -> List[DomainDefinition]:
        """
        Get core reasoning domains in authority order
        
        Returns:
            List of core domains sorted by authority level (1=highest)
        """
        if not self._loaded:
            self.load()
        
        core_domains = self.list_core_domains()
        # Sort by authority level (lower = higher authority)
        return sorted(core_domains, key=lambda d: d.get_authority_level())
    
    def _dict_to_domain(self, domain_dict: dict) -> DomainDefinition:
        """Convert dictionary to DomainDefinition object"""
        return DomainDefinition(
            domain_id=domain_dict['domain_id'],
            name=domain_dict['name'],
            responsibility_scope=domain_dict['responsibility_scope'],
            allowed_artifact_types=domain_dict['allowed_artifact_types'],
            cannot_own=domain_dict['cannot_own'],
            priority=domain_dict['priority'],
            authority_level=domain_dict.get('authority_level')
        )
