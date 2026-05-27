"""
Observer 5: SSOT Consistency Validator

Detects SSOT conflicts and missing SSOT references (warnings only).
"""

import time
from pathlib import Path
from typing import List, Optional, Dict, Set
from artifact_registry import ArtifactRegistry
from validation_result import ValidationWarning, ValidationResult, WarningCodes


class SSOTConsistencyValidator:
    """Validates SSOT consistency and relationships"""
    
    def __init__(self, artifact_registry: ArtifactRegistry):
        """
        Initialize SSOT consistency validator
        
        Args:
            artifact_registry: Artifact registry instance
        """
        self.artifact_registry = artifact_registry
        self.observer_name = "SSOTConsistencyValidator"
    
    def validate(self, changed_files: Optional[List[Path]] = None) -> ValidationResult:
        """
        Validate SSOT consistency for all artifacts
        
        Args:
            changed_files: List of file paths that changed (relative to repo root)
                          If None, validates all registered artifacts
        
        Returns:
            ValidationResult with warnings
        """
        start_time = time.time()
        warnings = []
        
        # Ensure registry is loaded
        if not self.artifact_registry._loaded:
            self.artifact_registry.load()
        
        # Get all artifacts (SSOT validation needs global view)
        all_artifacts = self.artifact_registry.list_all_artifacts()
        
        # Check for multiple canonical SSOTs per topic
        canonical_warnings = self._check_multiple_canonical_ssots(all_artifacts)
        warnings.extend(canonical_warnings)
        
        # Get artifacts to validate for missing references
        if changed_files is None:
            artifacts_to_check = all_artifacts
        else:
            artifacts_to_check = []
            for file_path in changed_files:
                artifact = self._get_artifact_by_file_path(str(file_path))
                if artifact:
                    artifacts_to_check.append(artifact)
        
        # Check for missing SSOT references
        for artifact in artifacts_to_check:
            reference_warnings = self._check_missing_ssot_references(artifact, all_artifacts)
            warnings.extend(reference_warnings)
        
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
    
    def _check_multiple_canonical_ssots(self, artifacts: List) -> List[ValidationWarning]:
        """
        Check for multiple canonical SSOTs on the same topic
        
        Args:
            artifacts: List of all artifacts
        
        Returns:
            List of warnings for SSOT conflicts
        """
        warnings = []
        
        # Group canonical SSOTs by topic
        canonical_by_topic: Dict[str, List] = {}
        
        for artifact in artifacts:
            if artifact.ssot_relationship == 'canonical' and artifact.topic:
                if artifact.topic not in canonical_by_topic:
                    canonical_by_topic[artifact.topic] = []
                canonical_by_topic[artifact.topic].append(artifact)
        
        # Check for conflicts
        for topic, canonical_artifacts in canonical_by_topic.items():
            if len(canonical_artifacts) > 1:
                # Multiple canonical SSOTs for same topic
                for artifact in canonical_artifacts:
                    other_artifacts = [a.artifact_id for a in canonical_artifacts if a.artifact_id != artifact.artifact_id]
                    
                    warnings.append(ValidationWarning(
                        observer_name=self.observer_name,
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        warning_code=WarningCodes.W400_MULTIPLE_CANONICAL_SSOT,
                        warning_message=f"Multiple canonical SSOTs detected for topic '{topic}'",
                        suggestion=f"Mark one as canonical and others as derived. Conflicts with: {', '.join(other_artifacts)}",
                        severity="critical"
                    ))
        
        return warnings
    
    def _check_missing_ssot_references(self, artifact, all_artifacts: List) -> List[ValidationWarning]:
        """
        Check for missing SSOT references in derived and implementation artifacts
        
        Args:
            artifact: Artifact to check
            all_artifacts: List of all artifacts (for finding canonical SSOTs)
        
        Returns:
            List of warnings for missing references
        """
        warnings = []
        
        # Check derived documents
        if artifact.ssot_relationship == 'derived':
            if not artifact.dependencies:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W401_MISSING_SSOT_REFERENCE,
                    warning_message="Derived document must reference its canonical SSOT",
                    suggestion="Add canonical SSOT artifact_id to dependencies field",
                    severity="high"
                ))
            else:
                # Check if dependencies include a canonical SSOT
                has_canonical_ref = self._has_canonical_ssot_reference(artifact.dependencies, all_artifacts)
                if not has_canonical_ref:
                    warnings.append(ValidationWarning(
                        observer_name=self.observer_name,
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        warning_code=WarningCodes.W401_MISSING_SSOT_REFERENCE,
                        warning_message="Derived document dependencies do not include a canonical SSOT",
                        suggestion="Add canonical SSOT artifact_id to dependencies field",
                        severity="high"
                    ))
        
        # Check implementation artifacts
        if artifact.ssot_relationship == 'implementation':
            if not artifact.dependencies:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W401_MISSING_SSOT_REFERENCE,
                    warning_message="Implementation artifact must reference its SSOT specification",
                    suggestion="Add SSOT specification artifact_id to dependencies field",
                    severity="high"
                ))
            else:
                # Check if dependencies include an SSOT
                has_ssot_ref = self._has_ssot_reference(artifact.dependencies, all_artifacts)
                if not has_ssot_ref:
                    warnings.append(ValidationWarning(
                        observer_name=self.observer_name,
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        warning_code=WarningCodes.W401_MISSING_SSOT_REFERENCE,
                        warning_message="Implementation artifact dependencies do not include an SSOT specification",
                        suggestion="Add SSOT specification artifact_id to dependencies field",
                        severity="high"
                    ))
        
        # Check for invalid ssot_relationship values
        valid_relationships = ['canonical', 'derived', 'implementation', 'none']
        if artifact.ssot_relationship not in valid_relationships:
            warnings.append(ValidationWarning(
                observer_name=self.observer_name,
                artifact_id=artifact.artifact_id,
                file_path=artifact.file_path,
                warning_code=WarningCodes.W402_INVALID_SSOT_RELATIONSHIP,
                warning_message=f"Invalid ssot_relationship '{artifact.ssot_relationship}'",
                suggestion=f"Use one of: {', '.join(valid_relationships)}",
                severity="medium"
            ))
        
        return warnings
    
    def _has_canonical_ssot_reference(self, dependencies: List[str], all_artifacts: List) -> bool:
        """
        Check if dependencies include a canonical SSOT
        
        Args:
            dependencies: List of artifact IDs
            all_artifacts: List of all artifacts
        
        Returns:
            True if dependencies include a canonical SSOT
        """
        for dep_id in dependencies:
            for artifact in all_artifacts:
                if artifact.artifact_id == dep_id and artifact.ssot_relationship == 'canonical':
                    return True
        return False
    
    def _has_ssot_reference(self, dependencies: List[str], all_artifacts: List) -> bool:
        """
        Check if dependencies include any SSOT (canonical or derived)
        
        Args:
            dependencies: List of artifact IDs
            all_artifacts: List of all artifacts
        
        Returns:
            True if dependencies include an SSOT
        """
        for dep_id in dependencies:
            for artifact in all_artifacts:
                if artifact.artifact_id == dep_id and artifact.ssot_relationship in ['canonical', 'derived']:
                    return True
        return False
