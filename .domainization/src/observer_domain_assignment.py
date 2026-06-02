"""
Observer 2: Domain Assignment Validator

Detects invalid domain assignments and suggests valid domains (warnings only).
"""

import time
from pathlib import Path
from typing import List, Optional
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from validation_result import ValidationWarning, ValidationResult, WarningCodes


class DomainAssignmentValidator:
    """Validates domain assignments against domain registry"""
    
    def __init__(self, artifact_registry: ArtifactRegistry, domain_registry: DomainRegistry):
        """
        Initialize domain assignment validator
        
        Args:
            artifact_registry: Artifact registry instance
            domain_registry: Domain registry instance
        """
        self.artifact_registry = artifact_registry
        self.domain_registry = domain_registry
        self.observer_name = "DomainAssignmentValidator"
    
    def validate(self, changed_files: Optional[List[Path]] = None) -> ValidationResult:
        """
        Validate domain assignments for changed files
        
        Args:
            changed_files: List of file paths that changed (relative to repo root)
                          If None, validates all registered artifacts
        
        Returns:
            ValidationResult with warnings
        """
        start_time = time.time()
        warnings = []
        
        # Ensure registries are loaded
        if not self.artifact_registry._loaded:
            self.artifact_registry.load()
        if not self.domain_registry._loaded:
            self.domain_registry.load()
        
        # Get artifacts to validate
        if changed_files is None:
            artifacts = self.artifact_registry.list_all_artifacts()
        else:
            artifacts = []
            for file_path in changed_files:
                artifact = self._get_artifact_by_file_path(str(file_path))
                if artifact:
                    artifacts.append(artifact)
        
        # Validate each artifact
        for artifact in artifacts:
            # Check if primary domain exists
            domain = self.domain_registry.get_domain(artifact.primary_domain)
            if domain is None:
                warnings.append(self._create_invalid_domain_warning(artifact))
                continue
            
            # Check if domain can own this artifact type
            is_valid, error_message = self.domain_registry.validate_domain_assignment(
                artifact.artifact_type,
                artifact.primary_domain
            )
            
            if not is_valid:
                warnings.append(self._create_domain_cannot_own_type_warning(artifact, error_message))
            
            # Validate secondary domains if present
            if artifact.secondary_domains:
                for secondary_domain in artifact.secondary_domains:
                    domain = self.domain_registry.get_domain(secondary_domain)
                    if domain is None:
                        warnings.append(self._create_invalid_secondary_domain_warning(
                            artifact, secondary_domain
                        ))
        
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return ValidationResult(
            observer_name=self.observer_name,
            warnings=warnings,
            execution_time_ms=execution_time
        )
    
    def _get_artifact_by_file_path(self, file_path: str) -> Optional:
        """Get artifact by file path"""
        artifacts = self.artifact_registry.list_all_artifacts()
        for artifact in artifacts:
            if artifact.file_path == file_path:
                return artifact
        return None
    
    def _create_invalid_domain_warning(self, artifact) -> ValidationWarning:
        """Create warning for invalid domain"""
        valid_domains = [d.domain_id for d in self.domain_registry.list_domains()]
        
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W100_INVALID_DOMAIN,
            warning_message=f"Invalid primary_domain '{artifact.primary_domain}' does not exist",
            suggestion=f"Use one of the valid domains: {', '.join(valid_domains)}",
            severity="high"
        )
    
    def _create_domain_cannot_own_type_warning(self, artifact, error_message: str) -> ValidationWarning:
        """Create warning for domain that cannot own artifact type"""
        valid_domains = self.domain_registry.get_valid_domains_for_type(artifact.artifact_type)
        
        suggestion = f"Change primary_domain to one of: {', '.join(valid_domains)}" if valid_domains else \
                    f"No domain can own artifact type '{artifact.artifact_type}'"
        
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W101_DOMAIN_CANNOT_OWN_TYPE,
            warning_message=error_message,
            suggestion=suggestion,
            severity="high"
        )
    
    def _create_invalid_secondary_domain_warning(self, artifact, secondary_domain: str) -> ValidationWarning:
        """Create warning for invalid secondary domain"""
        valid_domains = [d.domain_id for d in self.domain_registry.list_domains()]
        
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W100_INVALID_DOMAIN,
            warning_message=f"Invalid secondary_domain '{secondary_domain}' does not exist",
            suggestion=f"Use one of the valid domains: {', '.join(valid_domains)}",
            severity="medium"
        )
