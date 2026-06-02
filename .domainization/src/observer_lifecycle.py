"""
Observer 3: Lifecycle Validator

Detects invalid lifecycle transitions and deprecated artifact modifications (warnings only).
"""

import time
from pathlib import Path
from typing import List, Optional, Dict
from artifact_registry import ArtifactRegistry
from lifecycle_manager import LifecycleManager
from validation_result import ValidationWarning, ValidationResult, WarningCodes


class LifecycleValidator:
    """Validates lifecycle state transitions and modification rules"""
    
    def __init__(self, artifact_registry: ArtifactRegistry, lifecycle_manager: LifecycleManager):
        """
        Initialize lifecycle validator
        
        Args:
            artifact_registry: Artifact registry instance
            lifecycle_manager: Lifecycle manager instance
        """
        self.artifact_registry = artifact_registry
        self.lifecycle_manager = lifecycle_manager
        self.observer_name = "LifecycleValidator"
        
        # Track previous states for transition validation
        self._previous_states: Dict[str, str] = {}
    
    def validate(self, changed_files: Optional[List[Path]] = None, 
                 previous_states: Optional[Dict[str, str]] = None) -> ValidationResult:
        """
        Validate lifecycle states and transitions for changed files
        
        Args:
            changed_files: List of file paths that changed (relative to repo root)
                          If None, validates all registered artifacts
            previous_states: Dictionary mapping artifact_id to previous lifecycle_status
                           Used to detect transitions
        
        Returns:
            ValidationResult with warnings
        """
        start_time = time.time()
        warnings = []
        
        # Ensure registries are loaded
        if not self.artifact_registry._loaded:
            self.artifact_registry.load()
        if not self.lifecycle_manager._loaded:
            self.lifecycle_manager.load()
        
        # Update previous states if provided
        if previous_states:
            self._previous_states.update(previous_states)
        
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
            # Check if lifecycle_status is missing
            if not artifact.lifecycle_status:
                warnings.append(self._create_missing_lifecycle_warning(artifact))
                continue
            
            # Check if lifecycle state is valid for artifact type
            state_machine = self.lifecycle_manager.get_state_machine(artifact.artifact_type)
            if state_machine:
                if artifact.lifecycle_status not in state_machine.states:
                    warnings.append(self._create_invalid_lifecycle_state_warning(
                        artifact, state_machine.states
                    ))
                    continue
            
            # Check for invalid transitions if we have previous state
            if artifact.artifact_id in self._previous_states:
                previous_state = self._previous_states[artifact.artifact_id]
                current_state = artifact.lifecycle_status
                
                if previous_state != current_state:
                    # State changed, validate transition
                    is_valid, error_message = self.lifecycle_manager.validate_transition(
                        artifact.artifact_type,
                        previous_state,
                        current_state
                    )
                    
                    if not is_valid:
                        warnings.append(self._create_invalid_transition_warning(
                            artifact, previous_state, current_state, error_message
                        ))
            
            # Check if artifact is deprecated/read-only and was modified
            if not artifact.is_modifiable():
                # Check if file was actually modified (in changed_files)
                if changed_files and Path(artifact.file_path) in changed_files:
                    warnings.append(self._create_deprecated_modification_warning(artifact))
        
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return ValidationResult(
            observer_name=self.observer_name,
            warnings=warnings,
            execution_time_ms=execution_time
        )
    
    def update_previous_state(self, artifact_id: str, lifecycle_status: str) -> None:
        """
        Update tracked previous state for an artifact
        
        Args:
            artifact_id: Artifact ID
            lifecycle_status: Previous lifecycle status
        """
        self._previous_states[artifact_id] = lifecycle_status
    
    def _get_artifact_by_file_path(self, file_path: str) -> Optional:
        """Get artifact by file path"""
        artifacts = self.artifact_registry.list_all_artifacts()
        for artifact in artifacts:
            if artifact.file_path == file_path:
                return artifact
        return None
    
    def _create_missing_lifecycle_warning(self, artifact) -> ValidationWarning:
        """Create warning for missing lifecycle status"""
        state_machine = self.lifecycle_manager.get_state_machine(artifact.artifact_type)
        initial_state = state_machine.get_initial_state() if state_machine else 'unknown'
        
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W202_MISSING_LIFECYCLE_STATUS,
            warning_message="Artifact missing lifecycle_status",
            suggestion=f"Add lifecycle_status field (suggested initial state: '{initial_state}')",
            severity="high"
        )
    
    def _create_invalid_lifecycle_state_warning(self, artifact, valid_states: List[str]) -> ValidationWarning:
        """Create warning for invalid lifecycle state"""
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W203_INVALID_LIFECYCLE_STATE,
            warning_message=f"Invalid lifecycle_status '{artifact.lifecycle_status}' for artifact type '{artifact.artifact_type}'",
            suggestion=f"Use one of the valid states: {', '.join(valid_states)}",
            severity="high"
        )
    
    def _create_invalid_transition_warning(self, artifact, from_state: str, 
                                          to_state: str, error_message: str) -> ValidationWarning:
        """Create warning for invalid lifecycle transition"""
        allowed_transitions = self.lifecycle_manager.get_allowed_transitions(
            artifact.artifact_type, from_state
        )
        
        suggestion = f"Valid transitions from '{from_state}': {', '.join(allowed_transitions)}" if allowed_transitions else \
                    f"No valid transitions from state '{from_state}'"
        
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W200_INVALID_LIFECYCLE_TRANSITION,
            warning_message=f"Invalid transition from '{from_state}' to '{to_state}': {error_message}",
            suggestion=suggestion,
            severity="high"
        )
    
    def _create_deprecated_modification_warning(self, artifact) -> ValidationWarning:
        """Create warning for modification of deprecated/read-only artifact"""
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W201_DEPRECATED_MODIFICATION,
            warning_message=f"Artifact in '{artifact.lifecycle_status}' state should not be modified",
            suggestion="Only metadata updates allowed for deprecated/archived artifacts. Consider creating a new version instead.",
            severity="high"
        )
