"""
Validation Orchestrator

Runs all 5 validation observers and generates comprehensive observability report.
Operates in observability mode: warnings only, never blocks.
"""

import time
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from observer_registration import RegistrationValidator
from observer_domain_assignment import DomainAssignmentValidator
from observer_lifecycle import LifecycleValidator
from observer_boundary_awareness import BoundaryAwarenessValidator
from observer_ssot_consistency import SSOTConsistencyValidator
from validation_result import ValidationWarning, ValidationResult


@dataclass
class ObservabilityReport:
    """Comprehensive observability report from all observers"""
    
    total_warnings: int
    critical_warnings: int
    high_warnings: int
    medium_warnings: int
    low_warnings: int
    warnings_by_observer: Dict[str, List[ValidationWarning]]
    total_execution_time_ms: float
    performance_target_met: bool  # < 5 seconds
    
    def __str__(self) -> str:
        """Format report for display"""
        lines = []
        lines.append("=" * 80)
        lines.append("DOMAINIZATION OBSERVABILITY REPORT")
        lines.append("=" * 80)
        lines.append(f"Mode: OBSERVABILITY (warnings only, no blocking)")
        lines.append(f"Execution Time: {self.total_execution_time_ms:.2f}ms")
        lines.append(f"Performance Target (<5000ms): {'✓ MET' if self.performance_target_met else '✗ EXCEEDED'}")
        lines.append("")
        lines.append(f"Total Warnings: {self.total_warnings}")
        lines.append(f"  Critical: {self.critical_warnings}")
        lines.append(f"  High: {self.high_warnings}")
        lines.append(f"  Medium: {self.medium_warnings}")
        lines.append(f"  Low: {self.low_warnings}")
        lines.append("")
        
        if self.total_warnings == 0:
            lines.append("✓ No warnings detected. System is healthy.")
        else:
            lines.append("Warnings by Observer:")
            lines.append("-" * 80)
            for observer_name, warnings in self.warnings_by_observer.items():
                if warnings:
                    lines.append(f"\n{observer_name}: {len(warnings)} warning(s)")
                    for warning in warnings:
                        lines.append(f"  {warning}")
        
        lines.append("=" * 80)
        return "\n".join(lines)


class ValidationOrchestrator:
    """Orchestrates all validation observers in observability mode"""
    
    def __init__(self, 
                 artifact_registry: ArtifactRegistry,
                 domain_registry: DomainRegistry,
                 lifecycle_manager: LifecycleManager,
                 repo_root: Optional[Path] = None):
        """
        Initialize validation orchestrator
        
        Args:
            artifact_registry: Artifact registry instance
            domain_registry: Domain registry instance
            lifecycle_manager: Lifecycle manager instance
            repo_root: Root directory of repository
        """
        self.artifact_registry = artifact_registry
        self.domain_registry = domain_registry
        self.lifecycle_manager = lifecycle_manager
        self.repo_root = repo_root
        
        # Initialize all observers
        self.observer_registration = RegistrationValidator(artifact_registry, repo_root)
        self.observer_domain = DomainAssignmentValidator(artifact_registry, domain_registry)
        self.observer_lifecycle = LifecycleValidator(artifact_registry, lifecycle_manager)
        self.observer_boundary = BoundaryAwarenessValidator(artifact_registry, domain_registry)
        self.observer_ssot = SSOTConsistencyValidator(artifact_registry)
        
        # Performance target: < 5 seconds
        self.performance_target_ms = 5000
    
    def validate_all(self, 
                    changed_files: Optional[List[Path]] = None,
                    previous_states: Optional[Dict[str, str]] = None,
                    modifier_domain: Optional[str] = None) -> ObservabilityReport:
        """
        Run all validation observers and generate observability report
        
        Args:
            changed_files: List of file paths that changed (relative to repo root)
                          If None, validates all artifacts
            previous_states: Dictionary mapping artifact_id to previous lifecycle_status
                           Used by lifecycle validator to detect transitions
            modifier_domain: Domain making the modification (for boundary checks)
        
        Returns:
            ObservabilityReport with all warnings
        """
        start_time = time.time()
        
        # Run all observers
        results = []
        
        # Observer 1: Registration
        result1 = self.observer_registration.validate(changed_files)
        results.append(result1)
        
        # Observer 2: Domain Assignment
        result2 = self.observer_domain.validate(changed_files)
        results.append(result2)
        
        # Observer 3: Lifecycle
        result3 = self.observer_lifecycle.validate(changed_files, previous_states)
        results.append(result3)
        
        # Observer 4: Boundary Awareness
        result4 = self.observer_boundary.validate(changed_files, modifier_domain)
        results.append(result4)
        
        # Observer 5: SSOT Consistency
        result5 = self.observer_ssot.validate(changed_files)
        results.append(result5)
        
        total_execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Aggregate warnings
        all_warnings = []
        warnings_by_observer = {}
        
        for result in results:
            all_warnings.extend(result.warnings)
            warnings_by_observer[result.observer_name] = result.warnings
        
        # Count by severity
        critical_count = sum(1 for w in all_warnings if w.severity == 'critical')
        high_count = sum(1 for w in all_warnings if w.severity == 'high')
        medium_count = sum(1 for w in all_warnings if w.severity == 'medium')
        low_count = sum(1 for w in all_warnings if w.severity == 'low')
        
        # Check performance target
        performance_target_met = total_execution_time < self.performance_target_ms
        
        return ObservabilityReport(
            total_warnings=len(all_warnings),
            critical_warnings=critical_count,
            high_warnings=high_count,
            medium_warnings=medium_count,
            low_warnings=low_count,
            warnings_by_observer=warnings_by_observer,
            total_execution_time_ms=total_execution_time,
            performance_target_met=performance_target_met
        )
    
    def validate_observer(self, observer_name: str, 
                         changed_files: Optional[List[Path]] = None) -> ValidationResult:
        """
        Run a specific observer
        
        Args:
            observer_name: Name of observer to run
            changed_files: List of file paths that changed
        
        Returns:
            ValidationResult from the observer
        
        Raises:
            ValueError: If observer_name is invalid
        """
        observers = {
            'RegistrationValidator': self.observer_registration,
            'DomainAssignmentValidator': self.observer_domain,
            'LifecycleValidator': self.observer_lifecycle,
            'BoundaryAwarenessValidator': self.observer_boundary,
            'SSOTConsistencyValidator': self.observer_ssot
        }
        
        if observer_name not in observers:
            raise ValueError(f"Invalid observer name: {observer_name}. Valid names: {list(observers.keys())}")
        
        observer = observers[observer_name]
        return observer.validate(changed_files)
