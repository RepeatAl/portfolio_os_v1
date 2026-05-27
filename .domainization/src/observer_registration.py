"""
Observer 1: Artifact Registration Validator

Detects unregistered artifacts and validates metadata schema (warnings only).
"""

import time
from pathlib import Path
from typing import List, Optional, Set
from artifact_registry import ArtifactRegistry
from artifact_schema import ArtifactMetadata, validate_artifact_dict
from validation_result import ValidationWarning, ValidationResult, WarningCodes


class RegistrationValidator:
    """Validates artifact registration and metadata completeness"""
    
    def __init__(self, registry: ArtifactRegistry, repo_root: Optional[Path] = None):
        """
        Initialize registration validator
        
        Args:
            registry: Artifact registry instance
            repo_root: Root directory of repository (defaults to parent of .domainization)
        """
        self.registry = registry
        
        if repo_root is None:
            # Default to parent of .domainization directory
            domainization_dir = Path(__file__).parent.parent
            self.repo_root = domainization_dir.parent
        else:
            self.repo_root = Path(repo_root)
        
        self.observer_name = "RegistrationValidator"
    
    def validate(self, changed_files: Optional[List[Path]] = None) -> ValidationResult:
        """
        Validate artifact registration for changed files
        
        Args:
            changed_files: List of file paths that changed (relative to repo root)
                          If None, validates all files in repository
        
        Returns:
            ValidationResult with warnings
        """
        start_time = time.time()
        warnings = []
        
        # Ensure registry is loaded
        if not self.registry._loaded:
            self.registry.load()
        
        # Get list of files to validate
        if changed_files is None:
            files_to_check = self._get_all_trackable_files()
        else:
            files_to_check = [Path(f) for f in changed_files]
        
        # Get registered artifact file paths
        registered_files = self._get_registered_file_paths()
        
        # Check each file
        for file_path in files_to_check:
            # Skip if file doesn't exist
            full_path = self.repo_root / file_path
            if not full_path.exists():
                continue
            
            # Check if file is registered
            if str(file_path) not in registered_files:
                # Check for frontmatter in markdown files
                if file_path.suffix == '.md':
                    frontmatter = self.registry.parse_frontmatter(full_path)
                    if frontmatter:
                        # Has frontmatter, validate it
                        validation_warnings = self._validate_frontmatter(file_path, frontmatter)
                        warnings.extend(validation_warnings)
                    else:
                        # No frontmatter, warn about unregistered
                        warnings.append(self._create_unregistered_warning(file_path))
                else:
                    # Non-markdown file, must be in registry
                    warnings.append(self._create_unregistered_warning(file_path))
            else:
                # File is registered, validate metadata
                artifact = self._get_artifact_by_file_path(str(file_path))
                if artifact:
                    validation_warnings = self._validate_metadata(artifact)
                    warnings.extend(validation_warnings)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return ValidationResult(
            observer_name=self.observer_name,
            warnings=warnings,
            execution_time_ms=execution_time
        )
    
    def _get_all_trackable_files(self) -> List[Path]:
        """
        Get all files in repository that should be tracked
        
        Returns:
            List of file paths relative to repo root
        """
        trackable_files = []
        
        # Directories to skip
        skip_dirs = {
            '.git', '.kiro', '__pycache__', '.pytest_cache',
            'node_modules', '.venv', 'venv', '.idea', '.vscode',
            '.domainization/backups', '.domainization/logs'
        }
        
        # File patterns to skip
        skip_patterns = {
            '.DS_Store', '.gitignore', '.pyc', '.pyo', '.pyd',
            '.so', '.dylib', '.dll', '.egg-info'
        }
        
        for file_path in self.repo_root.rglob('*'):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Get relative path
            rel_path = file_path.relative_to(self.repo_root)
            
            # Skip if in excluded directory
            if any(skip_dir in rel_path.parts for skip_dir in skip_dirs):
                continue
            
            # Skip if matches excluded pattern
            if any(pattern in file_path.name for pattern in skip_patterns):
                continue
            
            trackable_files.append(rel_path)
        
        return trackable_files
    
    def _get_registered_file_paths(self) -> Set[str]:
        """
        Get set of all registered file paths
        
        Returns:
            Set of file paths (as strings)
        """
        artifacts = self.registry.list_all_artifacts()
        return {artifact.file_path for artifact in artifacts}
    
    def _get_artifact_by_file_path(self, file_path: str) -> Optional[ArtifactMetadata]:
        """
        Get artifact by file path
        
        Args:
            file_path: File path to search for
        
        Returns:
            ArtifactMetadata if found, None otherwise
        """
        artifacts = self.registry.list_all_artifacts()
        for artifact in artifacts:
            if artifact.file_path == file_path:
                return artifact
        return None
    
    def _create_unregistered_warning(self, file_path: Path) -> ValidationWarning:
        """Create warning for unregistered artifact"""
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=None,
            file_path=str(file_path),
            warning_code=WarningCodes.W001_UNREGISTERED_ARTIFACT,
            warning_message=f"Artifact not registered in domainization system",
            suggestion=(
                f"Add YAML frontmatter to {file_path} (if markdown) or "
                f"register in .domainization/artifact_registry.yaml"
            ),
            severity="high"
        )
    
    def _validate_frontmatter(self, file_path: Path, frontmatter: dict) -> List[ValidationWarning]:
        """
        Validate frontmatter metadata
        
        Args:
            file_path: Path to file
            frontmatter: Parsed frontmatter dictionary
        
        Returns:
            List of validation warnings
        """
        warnings = []
        
        # Check if frontmatter has required fields
        required_fields = [
            'artifact_id', 'primary_domain', 'artifact_type',
            'lifecycle_status', 'owner_role', 'ssot_relationship',
            'allowed_writers', 'allowed_readers'
        ]
        
        missing_fields = [f for f in required_fields if f not in frontmatter]
        
        if missing_fields:
            warnings.append(ValidationWarning(
                observer_name=self.observer_name,
                artifact_id=frontmatter.get('artifact_id'),
                file_path=str(file_path),
                warning_code=WarningCodes.W004_INCOMPLETE_METADATA,
                warning_message=f"Frontmatter missing required fields: {', '.join(missing_fields)}",
                suggestion=f"Add missing fields to YAML frontmatter: {', '.join(missing_fields)}",
                severity="high"
            ))
        
        # Validate metadata schema if all required fields present
        if not missing_fields:
            # Add file_path and dates if not present
            metadata_dict = frontmatter.copy()
            if 'file_path' not in metadata_dict:
                metadata_dict['file_path'] = str(file_path)
            if 'created_date' not in metadata_dict:
                metadata_dict['created_date'] = '2026-01-01'  # Placeholder
            if 'last_modified' not in metadata_dict:
                metadata_dict['last_modified'] = '2026-01-01'  # Placeholder
            
            is_valid, errors = validate_artifact_dict(metadata_dict)
            if not is_valid:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=frontmatter.get('artifact_id'),
                    file_path=str(file_path),
                    warning_code=WarningCodes.W003_INVALID_METADATA_SCHEMA,
                    warning_message=f"Invalid metadata schema: {'; '.join(errors)}",
                    suggestion="Fix metadata validation errors in frontmatter",
                    severity="high"
                ))
        
        return warnings
    
    def _validate_metadata(self, artifact: ArtifactMetadata) -> List[ValidationWarning]:
        """
        Validate artifact metadata completeness
        
        Args:
            artifact: Artifact metadata to validate
        
        Returns:
            List of validation warnings
        """
        warnings = []
        
        # Validate metadata
        is_valid, errors = artifact.validate()
        
        if not is_valid:
            warnings.append(ValidationWarning(
                observer_name=self.observer_name,
                artifact_id=artifact.artifact_id,
                file_path=artifact.file_path,
                warning_code=WarningCodes.W003_INVALID_METADATA_SCHEMA,
                warning_message=f"Invalid metadata: {'; '.join(errors)}",
                suggestion="Fix metadata validation errors in artifact_registry.yaml",
                severity="high"
            ))
        
        return warnings
