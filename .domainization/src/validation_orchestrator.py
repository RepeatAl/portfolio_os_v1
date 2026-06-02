"""
Validation Orchestrator

Runs all 5 validation observers and generates comprehensive observability report.
Operates in observability mode: warnings only, never blocks.

Extended with artifact registration enforcement policy (HARDENING 14):
- All new runtime/ and governance/ artifacts REQUIRE registration before merge
- Test files (tests/) use simplified registration class
- Transient artifacts explicitly marked with registry_mode: transient_exempt
- Emits CI-compatible warning if unregistered artifact count increases from baseline
"""

import time
from pathlib import Path
from typing import List, Optional, Dict, Set
from dataclasses import dataclass, field

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from observer_registration import RegistrationValidator
from observer_domain_assignment import DomainAssignmentValidator
from observer_lifecycle import LifecycleValidator
from observer_boundary_awareness import BoundaryAwarenessValidator
from observer_ssot_consistency import SSOTConsistencyValidator
from validation_result import ValidationWarning, ValidationResult, WarningCodes


# Registration enforcement warning codes (W800-W899)
W800_REGISTRATION_REQUIRED = "W800"
W801_UNREGISTERED_COUNT_INCREASE = "W801"
W802_SIMPLIFIED_REGISTRATION_MISSING = "W802"


@dataclass
class RegistrationEnforcementPolicy:
    """Artifact registration enforcement policy (HARDENING 14).
    
    Defines which artifacts require full registration, simplified registration,
    or are exempt from registration requirements.
    """
    
    # Directories requiring full registration before merge
    full_registration_dirs: List[str] = field(default_factory=lambda: [
        "runtime/",
        "governance/",
    ])
    
    # Directories using simplified registration (artifact_id, file_path, primary_domain, artifact_type only)
    simplified_registration_dirs: List[str] = field(default_factory=lambda: [
        "tests/",
    ])
    
    # File patterns explicitly exempt from registration
    transient_exempt_patterns: List[str] = field(default_factory=lambda: [
        "__pycache__/",
        ".pytest_cache/",
        "__init__.py",
        ".coverage",
        "*.pyc",
    ])
    
    # Baseline unregistered artifact count (from health report 2026-05-26)
    baseline_unregistered_count: int = 13
    
    def requires_full_registration(self, file_path: str) -> bool:
        """Check if a file requires full registration with all schema fields."""
        return any(file_path.startswith(d) for d in self.full_registration_dirs)
    
    def requires_simplified_registration(self, file_path: str) -> bool:
        """Check if a file requires simplified registration (test files)."""
        return any(file_path.startswith(d) for d in self.simplified_registration_dirs)
    
    def is_transient_exempt(self, file_path: str) -> bool:
        """Check if a file is explicitly exempt from registration."""
        for pattern in self.transient_exempt_patterns:
            if pattern.endswith("/"):
                if pattern.rstrip("/") in file_path:
                    return True
            elif pattern.startswith("*"):
                if file_path.endswith(pattern[1:]):
                    return True
            elif pattern in file_path:
                return True
        return False


@dataclass
class RegistrationEnforcementResult:
    """Result from registration enforcement validation."""
    
    warnings: List[ValidationWarning] = field(default_factory=list)
    unregistered_count: int = 0
    baseline_exceeded: bool = False
    full_registration_violations: List[str] = field(default_factory=list)
    simplified_registration_violations: List[str] = field(default_factory=list)
    
    @property
    def ci_warning_message(self) -> Optional[str]:
        """Generate CI-compatible warning message if baseline exceeded."""
        if self.baseline_exceeded:
            return (
                f"::warning::HARDENING 14 - Unregistered artifact count ({self.unregistered_count}) "
                f"exceeds baseline (13). Register new artifacts before merge."
            )
        return None


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

    def validate_registration_enforcement(
        self,
        changed_files: Optional[List[Path]] = None,
        policy: Optional[RegistrationEnforcementPolicy] = None
    ) -> RegistrationEnforcementResult:
        """
        Validate artifact registration enforcement policy (HARDENING 14).
        
        Checks that:
        - All new runtime/ and governance/ artifacts are registered with full schema
        - Test files (tests/) have at least simplified registration
        - Transient artifacts are explicitly marked as exempt
        - Unregistered artifact count does not exceed baseline
        
        Args:
            changed_files: List of file paths that changed (relative to repo root).
                          If None, validates all trackable files.
            policy: Registration enforcement policy. Uses default if None.
        
        Returns:
            RegistrationEnforcementResult with warnings and CI-compatible output
        """
        if policy is None:
            policy = RegistrationEnforcementPolicy()
        
        result = RegistrationEnforcementResult()
        
        # Ensure registry is loaded
        if not self.artifact_registry._loaded:
            self.artifact_registry.load()
        
        # Get registered file paths
        registered_files = self._get_registered_file_paths()
        
        # Get files to check
        if changed_files is None:
            files_to_check = self._get_trackable_files_for_enforcement()
        else:
            files_to_check = [str(f) for f in changed_files]
        
        # Track unregistered count
        unregistered_files = []
        
        for file_path in files_to_check:
            # Skip transient-exempt files
            if policy.is_transient_exempt(file_path):
                continue
            
            # Check if registered
            if file_path not in registered_files:
                unregistered_files.append(file_path)
                
                # Check enforcement level
                if policy.requires_full_registration(file_path):
                    result.full_registration_violations.append(file_path)
                    result.warnings.append(ValidationWarning(
                        observer_name="RegistrationEnforcement",
                        artifact_id=None,
                        file_path=file_path,
                        warning_code=W800_REGISTRATION_REQUIRED,
                        warning_message=(
                            f"Runtime/governance artifact requires full registration before merge"
                        ),
                        suggestion=(
                            f"Register {file_path} in .domainization/artifact_registry.yaml "
                            f"with all required schema fields"
                        ),
                        severity="high"
                    ))
                elif policy.requires_simplified_registration(file_path):
                    result.simplified_registration_violations.append(file_path)
                    result.warnings.append(ValidationWarning(
                        observer_name="RegistrationEnforcement",
                        artifact_id=None,
                        file_path=file_path,
                        warning_code=W802_SIMPLIFIED_REGISTRATION_MISSING,
                        warning_message=(
                            f"Test file requires simplified registration "
                            f"(artifact_id, file_path, primary_domain, artifact_type)"
                        ),
                        suggestion=(
                            f"Add simplified registration for {file_path} in "
                            f".domainization/artifact_registry.yaml"
                        ),
                        severity="medium"
                    ))
        
        # Check baseline count
        result.unregistered_count = len(unregistered_files)
        if result.unregistered_count > policy.baseline_unregistered_count:
            result.baseline_exceeded = True
            result.warnings.append(ValidationWarning(
                observer_name="RegistrationEnforcement",
                artifact_id=None,
                file_path=None,
                warning_code=W801_UNREGISTERED_COUNT_INCREASE,
                warning_message=(
                    f"Unregistered artifact count ({result.unregistered_count}) exceeds "
                    f"baseline ({policy.baseline_unregistered_count}). "
                    f"Growth must stop per HARDENING 14."
                ),
                suggestion=(
                    "Register all new artifacts before merge. "
                    "Use full registration for runtime/governance, "
                    "simplified for tests, transient_exempt for internal files."
                ),
                severity="high"
            ))
        
        return result

    def _get_registered_file_paths(self) -> Set[str]:
        """Get set of all registered file paths from the artifact registry."""
        artifacts = self.artifact_registry.list_all_artifacts()
        return {artifact.file_path for artifact in artifacts}

    def _get_trackable_files_for_enforcement(self) -> List[str]:
        """
        Get all files in runtime/, governance/, and tests/ directories
        that are subject to registration enforcement.
        """
        trackable_files = []
        
        enforcement_dirs = ["runtime/", "governance/", "tests/"]
        
        if self.repo_root is None:
            domainization_dir = Path(__file__).parent.parent
            repo_root = domainization_dir.parent
        else:
            repo_root = Path(self.repo_root)
        
        for enforcement_dir in enforcement_dirs:
            dir_path = repo_root / enforcement_dir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_dir():
                    continue
                
                rel_path = str(file_path.relative_to(repo_root))
                
                # Skip __pycache__ and .pytest_cache
                if "__pycache__" in rel_path or ".pytest_cache" in rel_path:
                    continue
                
                trackable_files.append(rel_path)
        
        return trackable_files
