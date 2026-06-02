"""
Observer 4: Boundary Awareness Validator

Detects authority chain violations, domain boundary violations,
forbidden cloud provider references, missing report value, and
runtime flow violations (warnings only).

Requirements: 5.5, 6.1-6.7, 11.1-11.4, 11.7, 12.1, 12.2, 12.8, 12.9, 12.10, 13.1-13.14, 14.1-14.10
"""

import logging
import time
from pathlib import Path
from typing import List, Optional, Dict, Set
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from cloud_provider_detector import CloudProviderDetector, ScanResult
from report_value_detector import ReportValueDetector, ReportValueAssessment, ReportValueHealthScore
from runtime_flow_detector import RuntimeFlowDetector, FlowStatus, FlowDetectionResult, RuntimeFlow
from validation_result import ValidationWarning, ValidationResult, WarningCodes

logger = logging.getLogger(__name__)


class BoundaryAwarenessValidator:
    """Validates domain boundaries and authority chain rules"""
    
    def __init__(self, artifact_registry: ArtifactRegistry, domain_registry: DomainRegistry):
        """
        Initialize boundary awareness validator
        
        Args:
            artifact_registry: Artifact registry instance
            domain_registry: Domain registry instance
        """
        self.artifact_registry = artifact_registry
        self.domain_registry = domain_registry
        self.observer_name = "BoundaryAwarenessValidator"
        self.cloud_provider_detector = CloudProviderDetector()
        self.report_value_detector = ReportValueDetector()
        self.runtime_flow_detector = RuntimeFlowDetector()
        
        # Define authority chain artifact types for each domain
        self.domain_artifact_types = {
            'SIGNALS': {'signal', 'signal_output', 'data_out'},
            'SEMANTICS': {'semantic_state', 'semantic_interpretation'},
            'REASONING': {'reasoning_object', 'reasoning_conclusion'},
            'REPORT': {'report_out', 'report_text'}
        }
    
    def validate(self, changed_files: Optional[List[Path]] = None,
                 modifier_domain: Optional[str] = None) -> ValidationResult:
        """
        Validate domain boundaries and authority chains for changed files
        
        Args:
            changed_files: List of file paths that changed (relative to repo root)
                          If None, validates all registered artifacts
            modifier_domain: Domain making the modification (for write permission checks)
        
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
            # Check authority chain violations
            authority_warnings = self._check_authority_chain_violations(artifact)
            warnings.extend(authority_warnings)
            
            # Check runtime flow violations via dependencies (Req 14.1-14.7)
            flow_warnings = self._check_runtime_flow_violations(artifact)
            warnings.extend(flow_warnings)
            
            # Check write permissions if modifier_domain provided
            if modifier_domain and changed_files and Path(artifact.file_path) in changed_files:
                if not artifact.can_write(modifier_domain):
                    warnings.append(self._create_cross_domain_write_warning(
                        artifact, modifier_domain
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
    
    def _check_authority_chain_violations(self, artifact) -> List[ValidationWarning]:
        """
        Check for authority chain violations
        
        Authority chain: SIGNALS (1) → SEMANTICS (2) → REASONING (3) → REPORT (4)
        Each domain should only create artifacts in its authority level
        """
        warnings = []
        
        # Get domain definition
        domain = self.domain_registry.get_domain(artifact.primary_domain)
        if not domain:
            return warnings  # Domain validation handled by Observer 2
        
        # Check if this is a core reasoning domain
        if not domain.is_core_domain():
            return warnings  # Surface domains don't participate in authority chain
        
        # Check for specific authority chain violations
        
        # SIGNALS should only write signal artifacts
        if artifact.primary_domain == 'SIGNALS':
            if artifact.artifact_type in ['SEMANTIC_STATE', 'REASONING_OBJECT', 'REPORT_OUT']:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W301_SIGNALS_WRITES_NON_SIGNAL,
                    warning_message="SIGNALS domain should only write signal artifacts, not semantic/reasoning/report artifacts",
                    suggestion="Move semantic interpretation to SEMANTICS domain, reasoning to REASONING domain, or report generation to REPORT domain",
                    severity="high"
                ))
        
        # SEMANTICS should only write semantic artifacts
        elif artifact.primary_domain == 'SEMANTICS':
            if artifact.artifact_type in ['SIGNAL', 'DATA_OUT']:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W302_SEMANTICS_WRITES_NON_SEMANTIC,
                    warning_message="SEMANTICS domain should not write raw signals, only semantic interpretations",
                    suggestion="Move signal generation to SIGNALS domain",
                    severity="high"
                ))
            elif artifact.artifact_type in ['REASONING_OBJECT', 'REPORT_OUT']:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W302_SEMANTICS_WRITES_NON_SEMANTIC,
                    warning_message="SEMANTICS domain should not write reasoning or report artifacts",
                    suggestion="Move reasoning to REASONING domain or report generation to REPORT domain",
                    severity="high"
                ))
        
        # REASONING should only write reasoning artifacts
        elif artifact.primary_domain == 'REASONING':
            if artifact.artifact_type in ['SIGNAL', 'DATA_OUT', 'SEMANTIC_STATE']:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W303_REASONING_WRITES_NON_REASONING,
                    warning_message="REASONING domain should not write signals or semantic states",
                    suggestion="Move signal generation to SIGNALS domain or semantic interpretation to SEMANTICS domain",
                    severity="high"
                ))
            elif artifact.artifact_type == 'REPORT_OUT':
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W303_REASONING_WRITES_NON_REASONING,
                    warning_message="REASONING domain should not write report artifacts",
                    suggestion="Move report generation to REPORT domain",
                    severity="high"
                ))
        
        # REPORT should only write report artifacts
        elif artifact.primary_domain == 'REPORT':
            if artifact.artifact_type in ['SIGNAL', 'DATA_OUT', 'SEMANTIC_STATE', 'REASONING_OBJECT']:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=artifact.artifact_id,
                    file_path=artifact.file_path,
                    warning_code=WarningCodes.W304_REPORT_WRITES_BUSINESS_LOGIC,
                    warning_message="REPORT domain should only write human-readable text, not business logic",
                    suggestion="Move signal generation to SIGNALS, semantic interpretation to SEMANTICS, or reasoning to REASONING domain",
                    severity="high"
                ))
            elif artifact.artifact_type == 'ENGINE':
                # Check if this is a report generation engine (allowed) or business logic engine (not allowed)
                if 'report' not in artifact.file_path.lower() and 'briefing' not in artifact.file_path.lower():
                    warnings.append(ValidationWarning(
                        observer_name=self.observer_name,
                        artifact_id=artifact.artifact_id,
                        file_path=artifact.file_path,
                        warning_code=WarningCodes.W304_REPORT_WRITES_BUSINESS_LOGIC,
                        warning_message="REPORT domain engines should only generate reports, not implement business logic",
                        suggestion="Move business logic engines to appropriate domain (SIGNALS, SEMANTICS, or REASONING)",
                        severity="medium"
                    ))
        
        return warnings
    
    def _create_cross_domain_write_warning(self, artifact, modifier_domain: str) -> ValidationWarning:
        """Create warning for cross-domain write attempt"""
        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=WarningCodes.W305_CROSS_DOMAIN_WRITE,
            warning_message=f"Domain '{modifier_domain}' attempted to modify artifact owned by '{artifact.primary_domain}'",
            suggestion=f"Request approval from {artifact.primary_domain} domain owner or add '{modifier_domain}' to allowed_writers",
            severity="high"
        )

    def _check_runtime_flow_violations(self, artifact) -> List[ValidationWarning]:
        """
        Check for runtime flow violations based on artifact dependencies.

        Uses RuntimeFlowDetector to analyze dependency flows and generates
        warnings for forbidden flows. Operates in OBSERVABILITY MODE (no blocking).

        Each dependency represents a flow from the dependency's domain to the
        artifact's domain (the artifact consumes from its dependencies).

        Args:
            artifact: Artifact metadata object with dependencies

        Returns:
            List of ValidationWarning objects for forbidden flows

        Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7
        """
        warnings = []

        # Skip if artifact has no dependencies
        if not artifact.dependencies:
            return warnings

        # Build dependency list with domain information
        dependencies = []
        for dep_id in artifact.dependencies:
            dep_artifact = self.artifact_registry.get_artifact(dep_id)
            if dep_artifact:
                dependencies.append({
                    "artifact_id": dep_id,
                    "domain": dep_artifact.primary_domain,
                })

        if not dependencies:
            return warnings

        # Detect flows from dependencies
        result = self.runtime_flow_detector.detect_flows_from_dependencies(
            artifact_id=artifact.artifact_id,
            artifact_domain=artifact.primary_domain,
            dependencies=dependencies,
        )

        # Generate warnings for forbidden flows (Req 14.6: log with details)
        for flow in result.get_forbidden_flows():
            warning = self._create_flow_violation_warning(artifact, flow)
            warnings.append(warning)

            # Log forbidden flow with details (Req 14.6)
            logger.warning(
                "Forbidden runtime flow detected: %s → %s | "
                "Artifact: %s | Reason: %s | Suggestion: %s",
                flow.source_domain,
                flow.target_domain,
                artifact.artifact_id,
                flow.reason,
                flow.suggestion,
            )

        return warnings

    def _create_flow_violation_warning(self, artifact, flow: RuntimeFlow) -> ValidationWarning:
        """
        Create a ValidationWarning for a forbidden runtime flow.

        Maps the flow violation to the appropriate warning code based on
        the type of violation detected.

        Args:
            artifact: The artifact with the forbidden dependency flow
            flow: The RuntimeFlow object describing the violation

        Returns:
            ValidationWarning with appropriate code and message
        """
        # Determine specific warning code based on flow characteristics
        warning_code = self._get_flow_warning_code(flow)

        return ValidationWarning(
            observer_name=self.observer_name,
            artifact_id=artifact.artifact_id,
            file_path=artifact.file_path,
            warning_code=warning_code,
            warning_message=(
                f"Forbidden runtime flow detected: {flow.source_domain} → {flow.target_domain}. "
                f"Authority chain violation: {flow.reason}"
            ),
            suggestion=flow.suggestion or (
                "Review artifact dependencies and ensure flows follow the authority chain: "
                "SIGNALS → SEMANTICS → REASONING → REPORT"
            ),
            severity="high"
        )

    def _get_flow_warning_code(self, flow: RuntimeFlow) -> str:
        """
        Determine the appropriate warning code for a flow violation.

        Args:
            flow: The RuntimeFlow describing the violation

        Returns:
            Warning code string
        """
        source = flow.source_domain
        target = flow.target_domain

        # Surface domain trying to create meaning in core domain
        if source in self.runtime_flow_detector.SURFACE_DOMAINS:
            return WarningCodes.W703_SURFACE_TO_CORE_FLOW

        # Backward authority flow
        source_level = self.runtime_flow_detector.AUTHORITY_LEVELS.get(source)
        target_level = self.runtime_flow_detector.AUTHORITY_LEVELS.get(target)
        if source_level and target_level and source_level > target_level:
            return WarningCodes.W702_BACKWARD_AUTHORITY_FLOW

        # Skipping authority levels
        if source_level and target_level and (target_level - source_level) > 1:
            return WarningCodes.W701_AUTHORITY_CHAIN_SKIP

        # Generic forbidden flow
        return WarningCodes.W700_FORBIDDEN_RUNTIME_FLOW

    def get_flow_traceability(self, artifact_id: str) -> Optional[Dict]:
        """
        Get complete flow traceability for an artifact showing the
        signal-to-report chain.

        Traces the dependency chain from the given artifact back through
        its dependencies to show the complete authority chain path.

        Args:
            artifact_id: ID of the artifact to trace

        Returns:
            Dictionary with traceability information, or None if artifact not found.
            Contains:
            - artifact_id: The traced artifact
            - domain: The artifact's domain
            - chain: List of steps in the flow chain
            - visualization: ASCII visualization of the authority chain
            - is_valid: Whether the chain follows valid authority flow
            - violations: List of any violations in the chain

        Requirements: 14.7
        """
        if not self.artifact_registry._loaded:
            self.artifact_registry.load()

        artifact = self.artifact_registry.get_artifact(artifact_id)
        if not artifact:
            return None

        # Build the flow chain by tracing dependencies
        chain = self._trace_dependency_chain(artifact_id, visited=set())

        # Extract domain path from chain
        domain_path = [step["domain"] for step in chain]

        # Visualize the authority chain
        visualization = self.runtime_flow_detector.visualize_authority_chain(domain_path)

        return {
            "artifact_id": artifact_id,
            "domain": artifact.primary_domain,
            "chain": chain,
            "domain_path": domain_path,
            "visualization": visualization.render_ascii(),
            "is_valid": visualization.is_valid,
            "violations": visualization.violations,
        }

    def _trace_dependency_chain(self, artifact_id: str, visited: set) -> List[Dict]:
        """
        Recursively trace the dependency chain for an artifact.

        Builds a list of steps from the deepest dependency (signal source)
        to the current artifact.

        Args:
            artifact_id: ID of the artifact to trace
            visited: Set of already-visited artifact IDs (cycle prevention)

        Returns:
            List of chain step dictionaries with artifact_id and domain
        """
        if artifact_id in visited:
            return []

        visited.add(artifact_id)

        artifact = self.artifact_registry.get_artifact(artifact_id)
        if not artifact:
            return []

        # Recursively trace dependencies first (depth-first)
        upstream_chain = []
        if artifact.dependencies:
            for dep_id in artifact.dependencies:
                dep_steps = self._trace_dependency_chain(dep_id, visited)
                upstream_chain.extend(dep_steps)

        # Add current artifact at the end
        upstream_chain.append({
            "artifact_id": artifact_id,
            "domain": artifact.primary_domain,
            "artifact_type": artifact.artifact_type,
            "file_path": artifact.file_path,
        })

        return upstream_chain

    def detect_all_runtime_flows(self) -> FlowDetectionResult:
        """
        Detect all runtime flows across all registered artifacts.

        Scans every artifact with dependencies and checks for forbidden flows.
        Used by health reporter for flow analysis section.

        Returns:
            FlowDetectionResult with all detected flows across the system

        Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6
        """
        start_time = time.time()
        all_flows = []

        if not self.artifact_registry._loaded:
            self.artifact_registry.load()

        artifacts = self.artifact_registry.list_all_artifacts()

        for artifact in artifacts:
            if not artifact.dependencies:
                continue

            # Build dependency list with domain info
            dependencies = []
            for dep_id in artifact.dependencies:
                dep_artifact = self.artifact_registry.get_artifact(dep_id)
                if dep_artifact:
                    dependencies.append({
                        "artifact_id": dep_id,
                        "domain": dep_artifact.primary_domain,
                    })

            if not dependencies:
                continue

            # Detect flows for this artifact
            result = self.runtime_flow_detector.detect_flows_from_dependencies(
                artifact_id=artifact.artifact_id,
                artifact_domain=artifact.primary_domain,
                dependencies=dependencies,
            )
            all_flows.extend(result.flows)

        allowed_count = sum(1 for f in all_flows if f.status == FlowStatus.ALLOWED)
        forbidden_count = sum(1 for f in all_flows if f.status == FlowStatus.FORBIDDEN)
        execution_time = (time.time() - start_time) * 1000

        return FlowDetectionResult(
            flows=all_flows,
            allowed_count=allowed_count,
            forbidden_count=forbidden_count,
            execution_time_ms=execution_time,
        )

    def scan_files_for_cloud_providers(self, file_paths: List[Path]) -> List[ValidationWarning]:
        """
        Scan files for forbidden cloud provider references.
        
        Uses CloudProviderDetector to scan each file and generates warning-level
        validation results for each forbidden match found. Never blocks — always
        returns warnings only (observability mode).
        
        Args:
            file_paths: List of file paths to scan for cloud provider references
            
        Returns:
            List of ValidationWarning objects for each forbidden provider match
            
        Requirements: 11.1, 11.2, 11.3, 11.4, 11.7
        """
        warnings = []
        
        # Map provider names to specific warning codes
        provider_warning_codes = {
            'aws': WarningCodes.W501_AWS_REFERENCE_DETECTED,
            'supabase': WarningCodes.W502_SUPABASE_REFERENCE_DETECTED,
            'azure': WarningCodes.W503_AZURE_REFERENCE_DETECTED,
        }
        
        for file_path in file_paths:
            path = Path(file_path)
            scan_result = self.cloud_provider_detector.scan_file(path)
            
            if scan_result.has_forbidden_references:
                for match in scan_result.forbidden_matches:
                    # Use provider-specific warning code or generic one
                    warning_code = provider_warning_codes.get(
                        match.provider, WarningCodes.W500_FORBIDDEN_CLOUD_PROVIDER
                    )
                    
                    warnings.append(ValidationWarning(
                        observer_name=self.observer_name,
                        artifact_id=None,
                        file_path=str(path),
                        warning_code=warning_code,
                        warning_message=(
                            f"Forbidden cloud provider reference detected: "
                            f"[{match.provider.upper()}] at line {match.line_number} "
                            f"in {path}"
                        ),
                        suggestion=(
                            f"Remove or replace {match.provider.upper()} reference. "
                            f"Portfolio OS uses Google Cloud Platform only. "
                            f"Line {match.line_number}: {match.line_content.strip()}"
                        ),
                        severity="medium"
                    ))
        
        return warnings

    def check_report_value(self, artifacts: Optional[List] = None) -> List[ValidationWarning]:
        """
        Check artifacts for report value justification.

        Uses ReportValueDetector to assess each artifact's report value and
        generates warnings for:
        - Missing report value (Requirement 12.1, 12.2)
        - Infrastructure-heavy artifacts without report justification (Requirement 12.8)
        - Governance-only features without report quality benefit (Requirement 12.9)
        - Features prioritizing architectural elegance over report value (Requirement 12.10)

        All detection operates in WARNING mode only (no blocking).

        Args:
            artifacts: List of artifact metadata dicts to check.
                      If None, loads all artifacts from registry.

        Returns:
            List of ValidationWarning objects for report value issues

        Requirements: 12.1, 12.2, 12.8, 12.9, 12.10
        """
        warnings = []

        # Load artifacts from registry if not provided
        if artifacts is None:
            if not self.artifact_registry._loaded:
                self.artifact_registry.load()
            registered_artifacts = self.artifact_registry.list_all_artifacts()
            artifacts = [self._artifact_to_dict(a) for a in registered_artifacts]

        for artifact_meta in artifacts:
            assessment = self.report_value_detector.assess_artifact(artifact_meta)

            # Warning for missing report value (Requirement 12.1, 12.2)
            if not assessment.has_report_value:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=assessment.artifact_id,
                    file_path=assessment.file_path,
                    warning_code=WarningCodes.W600_MISSING_REPORT_VALUE,
                    warning_message=(
                        f"Artifact '{assessment.artifact_id or assessment.file_path}' "
                        f"has no report value declared. "
                        f"How does this improve the report?"
                    ),
                    suggestion=(
                        "Add a 'report_value' field with 'category' and 'justification' "
                        "to artifact metadata. If no report value exists, consider deferring."
                    ),
                    severity="low"
                ))

            # Warning for infrastructure-heavy without report value (Requirement 12.8)
            if assessment.is_infrastructure_heavy and not assessment.is_valid:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=assessment.artifact_id,
                    file_path=assessment.file_path,
                    warning_code=WarningCodes.W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE,
                    warning_message=(
                        f"Infrastructure-heavy artifact '{assessment.artifact_id or assessment.file_path}' "
                        f"lacks valid report value justification. "
                        f"Infrastructure without report benefit should be deferred."
                    ),
                    suggestion=(
                        "Add report value justification or defer this artifact. "
                        "Report value takes precedence over architectural elegance (Req 12.10)."
                    ),
                    severity="medium"
                ))

            # Warning for speculative report value (Requirement 12.4 via 12.10)
            if assessment.is_speculative:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=assessment.artifact_id,
                    file_path=assessment.file_path,
                    warning_code=WarningCodes.W602_SPECULATIVE_REPORT_VALUE,
                    warning_message=(
                        f"Artifact '{assessment.artifact_id or assessment.file_path}' "
                        f"has speculative report value: '{assessment.justification}'. "
                        f"Report value must be measurable and direct."
                    ),
                    suggestion=(
                        "Replace speculative justification with direct, measurable report value. "
                        "Avoid words like 'might', 'could', 'potentially', 'in the future'."
                    ),
                    severity="medium"
                ))

            # Warning for invalid category
            if assessment.has_report_value and assessment.report_value_category and \
               assessment.report_value_category not in self.report_value_detector.allowed_categories:
                warnings.append(ValidationWarning(
                    observer_name=self.observer_name,
                    artifact_id=assessment.artifact_id,
                    file_path=assessment.file_path,
                    warning_code=WarningCodes.W601_INVALID_REPORT_VALUE_CATEGORY,
                    warning_message=(
                        f"Artifact '{assessment.artifact_id or assessment.file_path}' "
                        f"has invalid report value category: '{assessment.report_value_category}'"
                    ),
                    suggestion=(
                        f"Use one of the 10 allowed categories: "
                        f"{', '.join(self.report_value_detector.allowed_categories)}"
                    ),
                    severity="medium"
                ))

        return warnings

    def get_report_value_health_score(self, artifacts: Optional[List] = None) -> ReportValueHealthScore:
        """
        Generate report-value health score for artifacts.

        Calculates coverage percentage, valid percentage, and infrastructure
        drift percentage across all artifacts.

        Args:
            artifacts: List of artifact metadata dicts.
                      If None, loads all artifacts from registry.

        Returns:
            ReportValueHealthScore with aggregated metrics

        Requirements: 12.1, 12.2, 12.8, 12.9, 12.10
        """
        if artifacts is None:
            if not self.artifact_registry._loaded:
                self.artifact_registry.load()
            registered_artifacts = self.artifact_registry.list_all_artifacts()
            artifacts = [self._artifact_to_dict(a) for a in registered_artifacts]

        return self.report_value_detector.generate_health_score(artifacts)

    def _artifact_to_dict(self, artifact) -> dict:
        """
        Convert an artifact object to a metadata dictionary for ReportValueDetector.

        Args:
            artifact: Artifact object from registry

        Returns:
            Dictionary with artifact metadata
        """
        meta = {
            "artifact_id": artifact.artifact_id,
            "file_path": artifact.file_path,
            "primary_domain": artifact.primary_domain,
            "artifact_type": artifact.artifact_type,
            "lifecycle_status": artifact.lifecycle_status,
        }
        # Include report_value if present
        if hasattr(artifact, 'report_value'):
            meta["report_value"] = artifact.report_value
        # Include description if present
        if hasattr(artifact, 'description') and artifact.description:
            meta["description"] = artifact.description
        return meta
