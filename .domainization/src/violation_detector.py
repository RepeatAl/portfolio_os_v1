"""
Violation detector for domainization system

Detects governance violations:
- Unregistered artifacts
- Missing lifecycle status
- SSOT conflicts
- Deprecated artifact modifications
"""

from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from artifact_schema import ArtifactMetadata


class Violation:
    """Represents a governance violation"""
    
    def __init__(
        self,
        artifact_id: Optional[str],
        file_path: str,
        violation_type: str,
        severity: str,
        description: str,
        recommendation: str
    ):
        """
        Initialize violation
        
        Args:
            artifact_id: Artifact ID (None if unregistered)
            file_path: File path that has violation
            violation_type: Type of violation
            severity: "critical" | "high" | "medium" | "low"
            description: Human-readable description
            recommendation: Actionable resolution guidance
        """
        self.artifact_id = artifact_id
        self.file_path = file_path
        self.violation_type = violation_type
        self.severity = severity
        self.description = description
        self.recommendation = recommendation
    
    def to_dict(self) -> Dict:
        """Convert violation to dictionary"""
        return {
            'artifact_id': self.artifact_id,
            'file_path': self.file_path,
            'violation_type': self.violation_type,
            'severity': self.severity,
            'description': self.description,
            'recommendation': self.recommendation
        }
    
    def __str__(self) -> str:
        """Format violation for display"""
        severity_icon = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }.get(self.severity, '⚪')
        
        location = self.artifact_id or self.file_path
        return f"{severity_icon} [{self.violation_type}] {location}: {self.description}\n   → {self.recommendation}"


class ViolationDetector:
    """Detects domainization governance violations"""
    
    def __init__(
        self,
        artifact_registry: Optional[ArtifactRegistry] = None,
        domain_registry: Optional[DomainRegistry] = None,
        lifecycle_manager: Optional[LifecycleManager] = None,
        repo_root: Optional[Path] = None
    ):
        """
        Initialize violation detector
        
        Args:
            artifact_registry: ArtifactRegistry instance (creates default if None)
            domain_registry: DomainRegistry instance (creates default if None)
            lifecycle_manager: LifecycleManager instance (creates default if None)
            repo_root: Repository root path (uses parent of .domainization if None)
        """
        self.artifact_registry = artifact_registry or ArtifactRegistry()
        self.domain_registry = domain_registry or DomainRegistry()
        self.lifecycle_manager = lifecycle_manager or LifecycleManager()
        
        if repo_root is None:
            # Default to parent of .domainization directory
            self.repo_root = Path(__file__).parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
    
    def detect_all_violations(self) -> List[Violation]:
        """
        Detect all governance violations
        
        Returns:
            List of violations found
        """
        # Load registries
        self.artifact_registry.load()
        self.domain_registry.load()
        self.lifecycle_manager.load()
        
        violations = []
        
        # Detect unregistered artifacts
        violations.extend(self.detect_unregistered_artifacts())
        
        # Detect missing lifecycle status
        violations.extend(self.detect_missing_lifecycle_status())
        
        # Detect SSOT conflicts
        violations.extend(self.detect_ssot_conflicts())
        
        # Detect deprecated artifact modifications
        violations.extend(self.detect_deprecated_modifications())
        
        return violations
    
    def detect_unregistered_artifacts(self) -> List[Violation]:
        """
        Detect artifacts that are not registered
        
        Returns:
            List of violations for unregistered artifacts
        """
        violations = []
        
        # Get all registered file paths
        registered_paths = set()
        for artifact in self.artifact_registry.list_all_artifacts():
            registered_paths.add(artifact.file_path)
        
        # Scan repository for files that should be registered
        # For now, we'll check specific directories
        scan_dirs = ['docs', 'engines', 'reports', 'data']
        scan_extensions = ['.md', '.py', '.yaml', '.yml', '.json', '.xlsx', '.txt']
        
        for scan_dir in scan_dirs:
            dir_path = self.repo_root / scan_dir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.rglob('*'):
                if not file_path.is_file():
                    continue
                
                # Check if file should be registered
                if file_path.suffix not in scan_extensions:
                    continue
                
                # Skip test files and cache
                if '__pycache__' in str(file_path) or 'test_' in file_path.name:
                    continue
                
                # Get relative path
                try:
                    rel_path = str(file_path.relative_to(self.repo_root))
                except ValueError:
                    continue
                
                # Check if registered
                if rel_path not in registered_paths:
                    violations.append(Violation(
                        artifact_id=None,
                        file_path=rel_path,
                        violation_type='unregistered',
                        severity='high',
                        description=f"Artifact not registered in domainization system",
                        recommendation="Add YAML frontmatter metadata or register in artifact_registry.yaml"
                    ))
        
        return violations

    
    def detect_missing_lifecycle_status(self) -> List[Violation]:
        """
        Detect artifacts with missing or invalid lifecycle status
        
        Returns:
            List of violations for missing lifecycle status
        """
        violations = []
        
        for artifact in self.artifact_registry.list_all_artifacts():
            # Check if lifecycle_status is missing or empty
            if not artifact.lifecycle_status or artifact.lifecycle_status.strip() == '':
                violations.append(Violation(
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    violation_type='missing_lifecycle',
                    severity='medium',
                    description="Artifact missing lifecycle status",
                    recommendation=f"Add lifecycle_status field with valid state for {artifact.artifact_type}"
                ))
                continue
            
            # Check if lifecycle status is valid for artifact type
            state_machine = self.lifecycle_manager.get_state_machine(artifact.artifact_type)
            if state_machine:
                valid_states = state_machine.states
                if artifact.lifecycle_status not in valid_states:
                    violations.append(Violation(
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        violation_type='invalid_lifecycle',
                        severity='medium',
                        description=f"Invalid lifecycle status '{artifact.lifecycle_status}' for {artifact.artifact_type}",
                        recommendation=f"Use one of: {', '.join(valid_states)}"
                    ))
        
        return violations
    
    def detect_ssot_conflicts(self) -> List[Violation]:
        """
        Detect SSOT conflicts (multiple canonical SSOTs for same topic)
        
        Returns:
            List of violations for SSOT conflicts
        """
        violations = []
        
        # Group canonical SSOTs by topic
        canonical_by_topic = defaultdict(list)
        
        for artifact in self.artifact_registry.list_all_artifacts():
            # Only check SSOT artifacts with canonical relationship
            if artifact.artifact_type == 'SSOT' and artifact.ssot_relationship == 'canonical':
                # Use topic if available, otherwise use file_path as topic
                topic = artifact.topic if artifact.topic else artifact.file_path
                canonical_by_topic[topic].append(artifact)
        
        # Check for conflicts
        for topic, artifacts in canonical_by_topic.items():
            if len(artifacts) > 1:
                # Multiple canonical SSOTs for same topic
                artifact_ids = [a.artifact_id for a in artifacts]
                
                for artifact in artifacts:
                    violations.append(Violation(
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        violation_type='ssot_conflict',
                        severity='critical',
                        description=f"Multiple canonical SSOTs for topic '{topic}'",
                        recommendation=f"Mark one as canonical, others as derived. Conflicts with: {', '.join([aid for aid in artifact_ids if aid != artifact.artifact_id])}"
                    ))
        
        # Check for derived documents without canonical reference
        for artifact in self.artifact_registry.list_all_artifacts():
            if artifact.ssot_relationship == 'derived':
                # Check if it has dependencies
                if not artifact.dependencies or len(artifact.dependencies) == 0:
                    violations.append(Violation(
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        violation_type='missing_ssot_reference',
                        severity='high',
                        description="Derived document must reference canonical SSOT",
                        recommendation="Add canonical SSOT artifact_id to dependencies field"
                    ))
                else:
                    # Check if any dependency is a canonical SSOT
                    has_canonical_ref = False
                    for dep_id in artifact.dependencies:
                        dep = self.artifact_registry.get_artifact(dep_id)
                        if dep and dep.ssot_relationship == 'canonical':
                            has_canonical_ref = True
                            break
                    
                    if not has_canonical_ref:
                        violations.append(Violation(
                            artifact_id=artifact.artifact_id,
                            file_path=artifact.file_path,
                            violation_type='missing_ssot_reference',
                            severity='high',
                            description="Derived document dependencies do not include canonical SSOT",
                            recommendation="Add canonical SSOT artifact_id to dependencies field"
                        ))
        
        # Check for implementation artifacts without SSOT reference
        for artifact in self.artifact_registry.list_all_artifacts():
            if artifact.ssot_relationship == 'implementation':
                # Check if it has dependencies
                if not artifact.dependencies or len(artifact.dependencies) == 0:
                    violations.append(Violation(
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        violation_type='missing_ssot_reference',
                        severity='high',
                        description="Implementation artifact must reference SSOT specification",
                        recommendation="Add SSOT specification artifact_id to dependencies field"
                    ))
                else:
                    # Check if any dependency is an SSOT
                    has_ssot_ref = False
                    for dep_id in artifact.dependencies:
                        dep = self.artifact_registry.get_artifact(dep_id)
                        if dep and dep.artifact_type == 'SSOT':
                            has_ssot_ref = True
                            break
                    
                    if not has_ssot_ref:
                        violations.append(Violation(
                            artifact_id=artifact.artifact_id,
                            file_path=artifact.file_path,
                            violation_type='missing_ssot_reference',
                            severity='high',
                            description="Implementation artifact dependencies do not include SSOT",
                            recommendation="Add SSOT specification artifact_id to dependencies field"
                        ))
        
        return violations
    
    def detect_deprecated_modifications(self) -> List[Violation]:
        """
        Detect modifications to deprecated artifacts
        
        Returns:
            List of violations for deprecated modifications
        """
        violations = []
        
        # Get all deprecated artifacts
        for artifact in self.artifact_registry.list_all_artifacts():
            if artifact.lifecycle_status == 'deprecated':
                # Check if file was recently modified
                file_path = self.repo_root / artifact.file_path
                
                if file_path.exists():
                    # Get file modification time
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    # Check if modified in last 7 days (configurable threshold)
                    if datetime.now() - mtime < timedelta(days=7):
                        violations.append(Violation(
                            artifact_id=artifact.artifact_id,
                            file_path=artifact.file_path,
                            violation_type='deprecated_modification',
                            severity='high',
                            description="Deprecated artifact was recently modified",
                            recommendation="Only metadata updates allowed for deprecated artifacts. Consider updating lifecycle status if artifact is active again."
                        ))
        
        return violations
    
    def get_violations_by_severity(self, violations: List[Violation]) -> Dict[str, List[Violation]]:
        """
        Group violations by severity
        
        Args:
            violations: List of violations
        
        Returns:
            Dictionary mapping severity to list of violations
        """
        by_severity = defaultdict(list)
        for violation in violations:
            by_severity[violation.severity].append(violation)
        
        return dict(by_severity)
    
    def get_violations_by_type(self, violations: List[Violation]) -> Dict[str, List[Violation]]:
        """
        Group violations by type
        
        Args:
            violations: List of violations
        
        Returns:
            Dictionary mapping violation type to list of violations
        """
        by_type = defaultdict(list)
        for violation in violations:
            by_type[violation.violation_type].append(violation)
        
        return dict(by_type)
    
    def format_violations_text(self, violations: List[Violation]) -> str:
        """
        Format violations as human-readable text
        
        Args:
            violations: List of violations
        
        Returns:
            Formatted text
        """
        if not violations:
            return "✅ No violations detected"
        
        lines = []
        lines.append(f"Found {len(violations)} violation(s):\n")
        
        # Group by severity
        by_severity = self.get_violations_by_severity(violations)
        
        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in by_severity:
                lines.append(f"\n{severity.upper()} ({len(by_severity[severity])})")
                lines.append("-" * 80)
                for violation in by_severity[severity]:
                    lines.append(str(violation))
                    lines.append("")
        
        return '\n'.join(lines)
