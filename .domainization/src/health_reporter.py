"""
Health reporter for domainization system

Generates comprehensive health reports showing:
- Registration coverage
- Domain distribution
- Lifecycle distribution
- Report-value health score
- Infrastructure drift percentage
- Violations and recommendations
- Governance events (severity, description, component, timestamp)
- Sunset governance status (deprecated artifacts, sunset phases, blocked sunsets)
- State transitions (previous state, new state, reason, timestamp)
- Integrity verification (zero forbidden flows, zero unregistered artifacts, 100% report_value)

Requirements: 1.5, 3.4, 4.6, 17.4, 18.4
"""

import sys
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone
from collections import defaultdict

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from violation_detector import ViolationDetector
from report_value_detector import ReportValueDetector, ReportValueHealthScore
from runtime_flow_detector import RuntimeFlowDetector, FlowStatus, FlowDetectionResult

# Add project root to path for runtime/governance imports
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from governance.sunset_governance import SunsetGovernance, SunsetPhase, SunsetReportEntry
from runtime.severity_taxonomy import Severity, SEVERITY_DEFINITIONS
from runtime.runtime_state_model import RuntimeState, IntegrityDimension, aggregate_pipeline_state


class HealthReporter:
    """Generates domainization health reports"""
    
    def __init__(
        self,
        artifact_registry: Optional[ArtifactRegistry] = None,
        domain_registry: Optional[DomainRegistry] = None,
        lifecycle_manager: Optional[LifecycleManager] = None,
        violation_detector: Optional[ViolationDetector] = None,
        repo_root: Optional[Path] = None
    ):
        """
        Initialize health reporter
        
        Args:
            artifact_registry: ArtifactRegistry instance (creates default if None)
            domain_registry: DomainRegistry instance (creates default if None)
            lifecycle_manager: LifecycleManager instance (creates default if None)
            violation_detector: ViolationDetector instance (creates default if None)
            repo_root: Repository root path (uses parent of .domainization if None)
        """
        self.artifact_registry = artifact_registry or ArtifactRegistry()
        self.domain_registry = domain_registry or DomainRegistry()
        self.lifecycle_manager = lifecycle_manager or LifecycleManager()
        self.report_value_detector = ReportValueDetector()
        self.runtime_flow_detector = RuntimeFlowDetector()
        
        if repo_root is None:
            # Default to parent of .domainization directory
            self.repo_root = Path(__file__).parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        # Create violation detector with same registries
        self.violation_detector = violation_detector or ViolationDetector(
            artifact_registry=self.artifact_registry,
            domain_registry=self.domain_registry,
            lifecycle_manager=self.lifecycle_manager,
            repo_root=self.repo_root
        )
        
        # Governance event log — structured events with severity, description,
        # component, and timestamp (Req 17.4, 18.4)
        self._governance_events: List[Dict] = []
        
        # State transition log — previous state, new state, reason, timestamp (Req 18.4)
        self._state_transitions: List[Dict] = []
        
        # Current runtime state for the health reporter component
        self._current_state: str = RuntimeState.HEALTHY
    
    def _emit_governance_event(
        self, severity: Severity, description: str, component: str
    ) -> Dict:
        """Emit a structured governance event.

        Every governance event includes severity, description, component identifier,
        and timestamp per Requirements 17.4, 18.4.

        Args:
            severity: Canonical severity level from the severity taxonomy.
            description: Human-readable description of the event.
            component: Identifier of the component emitting the event.

        Returns:
            The structured event dictionary that was recorded.
        """
        event = {
            "severity": severity.name,
            "severity_level": int(severity),
            "description": description,
            "component": component,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        self._governance_events.append(event)
        return event

    def _record_state_transition(
        self, previous_state: str, new_state: str, reason: str
    ) -> Dict:
        """Record a runtime state transition.

        State transitions include previous state, new state, reason, and timestamp
        per Requirement 18.4.

        Args:
            previous_state: The state before the transition.
            new_state: The state after the transition.
            reason: Human-readable reason for the transition.

        Returns:
            The structured transition dictionary that was recorded.
        """
        transition = {
            "previous_state": previous_state,
            "new_state": new_state,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        self._state_transitions.append(transition)
        self._current_state = new_state
        return transition

    def generate_health_report(self, include_violations: bool = True) -> Dict:
        """
        Generate comprehensive health report
        
        Args:
            include_violations: Whether to include violation detection (default: True)
        
        Returns:
            Dictionary containing health report data
        """
        # Load registries
        self.artifact_registry.load()
        self.domain_registry.load()
        self.lifecycle_manager.load()
        
        # Get all artifacts
        all_artifacts = self.artifact_registry.list_all_artifacts()
        
        # Calculate metrics
        total_artifacts = len(all_artifacts)
        registered_artifacts = total_artifacts  # All in registry are registered
        
        # Get domain coverage
        domain_coverage = self.get_domain_coverage()
        
        # Get lifecycle distribution
        lifecycle_distribution = self.get_lifecycle_distribution()
        
        # Build report
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'report_time': datetime.now().strftime('%H:%M:%S'),
            'report_version': '1.0',
            'enforcement_mode': 'observability',  # FAST LANE phase
            'summary': {
                'total_artifacts': total_artifacts,
                'registered_artifacts': registered_artifacts,
                'registration_percentage': 100.0 if total_artifacts > 0 else 0.0,
                'total_domains': len(self.domain_registry.list_domains()),
                'domains_with_artifacts': len([d for d in domain_coverage if d['artifact_count'] > 0])
            },
            'domain_coverage': domain_coverage,
            'lifecycle_distribution': lifecycle_distribution
        }
        
        # Add report-value health score
        report_value_health = self.get_report_value_health_score()
        report['report_value_health'] = report_value_health
        report['summary']['report_value_valid_percentage'] = report_value_health.get('valid_percentage', 0.0)
        report['summary']['infrastructure_drift_percentage'] = report_value_health.get('infrastructure_drift_percentage', 0.0)
        
        # Add runtime flow analysis (Req 14.1-14.7)
        flow_analysis = self.get_runtime_flow_analysis()
        report['runtime_flow_analysis'] = flow_analysis
        report['summary']['total_flows_detected'] = flow_analysis.get('total_flows', 0)
        report['summary']['forbidden_flows_detected'] = flow_analysis.get('forbidden_flows', 0)
        
        # Add sunset governance report (Req 25.1, 25.2)
        sunset_report = self.get_sunset_governance_report()
        report['sunset_governance'] = sunset_report
        report['summary']['deprecated_artifacts'] = sunset_report.get('total_deprecated', 0)
        report['summary']['sunset_blocked_count'] = sunset_report.get('sunset_blocked_count', 0)
        
        # Add integrity verification summary (Req 1.5, 3.4, 4.6)
        integrity = self.get_integrity_verification()
        report['integrity_verification'] = integrity
        
        # Add violations if requested
        if include_violations:
            violations = self.violation_detector.detect_all_violations()
            
            # Add violation summary to report
            report['summary']['total_violations'] = len(violations)
            
            # Group violations by severity
            by_severity = self.violation_detector.get_violations_by_severity(violations)
            report['summary']['violations_by_severity'] = {
                'critical': len(by_severity.get('critical', [])),
                'high': len(by_severity.get('high', [])),
                'medium': len(by_severity.get('medium', [])),
                'low': len(by_severity.get('low', []))
            }
            
            # Add violations to report
            report['violations'] = [v.to_dict() for v in violations]
            
            # Generate recommendations based on violations
            report['recommendations'] = self._generate_recommendations(violations)
        
        # Add governance events log (Req 17.4, 18.4)
        report['governance_events'] = list(self._governance_events)
        report['summary']['total_governance_events'] = len(self._governance_events)
        
        # Add state transitions log (Req 18.4)
        report['state_transitions'] = list(self._state_transitions)
        report['summary']['total_state_transitions'] = len(self._state_transitions)
        
        return report
    
    def get_domain_coverage(self) -> List[Dict]:
        """
        Calculate artifact distribution by domain
        
        Returns:
            List of domain coverage dictionaries with:
            - domain_id
            - domain_name
            - artifact_count
            - artifact_types (breakdown by type)
        """
        # Get all domains
        domains = self.domain_registry.list_domains()
        
        coverage = []
        for domain in domains:
            # Get artifacts for this domain
            artifacts = self.artifact_registry.list_artifacts_by_domain(domain.domain_id)
            
            # Count by artifact type
            type_counts = defaultdict(int)
            for artifact in artifacts:
                type_counts[artifact.artifact_type] += 1
            
            # Build artifact types list
            artifact_types = [
                {'type': artifact_type, 'count': count}
                for artifact_type, count in sorted(type_counts.items())
            ]
            
            coverage.append({
                'domain_id': domain.domain_id,
                'domain_name': domain.name,
                'priority': domain.priority,
                'artifact_count': len(artifacts),
                'artifact_types': artifact_types
            })
        
        # Sort by artifact count (descending)
        coverage.sort(key=lambda x: x['artifact_count'], reverse=True)
        
        return coverage

    
    def get_lifecycle_distribution(self) -> List[Dict]:
        """
        Calculate artifact distribution by lifecycle state
        
        Returns:
            List of lifecycle distribution dictionaries with:
            - artifact_type
            - states (breakdown by state)
        """
        # Get all artifacts
        all_artifacts = self.artifact_registry.list_all_artifacts()
        
        # Group by artifact type and lifecycle status
        type_lifecycle_counts = defaultdict(lambda: defaultdict(int))
        for artifact in all_artifacts:
            type_lifecycle_counts[artifact.artifact_type][artifact.lifecycle_status] += 1
        
        distribution = []
        for artifact_type in sorted(type_lifecycle_counts.keys()):
            states = [
                {'state': state, 'count': count}
                for state, count in sorted(type_lifecycle_counts[artifact_type].items())
            ]
            
            distribution.append({
                'artifact_type': artifact_type,
                'total_count': sum(s['count'] for s in states),
                'states': states
            })
        
        return distribution

    def get_report_value_health_score(self) -> Dict:
        """
        Calculate report-value health score across all artifacts.

        Uses ReportValueDetector to assess each artifact's report value and
        generates aggregated metrics including coverage percentage, valid
        percentage, infrastructure drift, and category distribution.

        Returns:
            Dictionary containing report-value health metrics:
            - total_artifacts: Total number of artifacts assessed
            - artifacts_with_report_value: Count with any report value declared
            - artifacts_with_valid_report_value: Count with valid (non-speculative, allowed category)
            - artifacts_speculative: Count with speculative justification
            - artifacts_infrastructure_heavy: Count of infra-heavy without valid report value
            - artifacts_missing_report_value: Count without report value
            - coverage_percentage: Percentage with any report value
            - valid_percentage: Percentage with valid report value
            - infrastructure_drift_percentage: Percentage of infra-heavy without report value
            - category_distribution: Breakdown by report value category

        Requirements: 12.1, 12.2, 12.8, 12.9, 12.10
        """
        # Get all artifacts and convert to metadata dicts
        all_artifacts = self.artifact_registry.list_all_artifacts()
        artifact_dicts = []
        for artifact in all_artifacts:
            meta = {
                "artifact_id": artifact.artifact_id,
                "file_path": artifact.file_path,
                "primary_domain": artifact.primary_domain,
                "artifact_type": artifact.artifact_type,
                "lifecycle_status": artifact.lifecycle_status,
            }
            if hasattr(artifact, 'report_value'):
                meta["report_value"] = artifact.report_value
            if hasattr(artifact, 'description') and artifact.description:
                meta["description"] = artifact.description
            artifact_dicts.append(meta)

        # Generate health score
        score = self.report_value_detector.generate_health_score(artifact_dicts)

        return {
            'total_artifacts': score.total_artifacts,
            'artifacts_with_report_value': score.artifacts_with_report_value,
            'artifacts_with_valid_report_value': score.artifacts_with_valid_report_value,
            'artifacts_speculative': score.artifacts_speculative,
            'artifacts_infrastructure_heavy': score.artifacts_infrastructure_heavy,
            'artifacts_missing_report_value': score.artifacts_missing_report_value,
            'coverage_percentage': score.coverage_percentage,
            'valid_percentage': score.valid_percentage,
            'infrastructure_drift_percentage': score.infrastructure_drift_percentage,
            'category_distribution': score.category_distribution,
        }

    def get_runtime_flow_analysis(self) -> Dict:
        """
        Analyze runtime flows across all registered artifacts.

        Scans artifact dependencies to detect allowed and forbidden flows,
        providing a summary for the health report.

        Returns:
            Dictionary containing runtime flow analysis:
            - total_flows: Total number of flows detected
            - allowed_flows: Count of allowed flows
            - forbidden_flows: Count of forbidden flows
            - flow_health_percentage: Percentage of flows that are valid
            - forbidden_flow_details: List of forbidden flow descriptions
            - authority_chain_status: Summary of authority chain compliance
            - execution_time_ms: Time taken for analysis

        Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7
        """
        import time as _time
        start_time = _time.time()

        all_artifacts = self.artifact_registry.list_all_artifacts()
        all_flows = []

        for artifact in all_artifacts:
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
        total_flows = len(all_flows)
        flow_health = (allowed_count / total_flows * 100.0) if total_flows > 0 else 100.0

        # Build forbidden flow details
        forbidden_details = []
        for flow in all_flows:
            if flow.status == FlowStatus.FORBIDDEN:
                forbidden_details.append({
                    "source_domain": flow.source_domain,
                    "target_domain": flow.target_domain,
                    "artifact_id": flow.artifact_id,
                    "reason": flow.reason,
                    "suggestion": flow.suggestion,
                })

        execution_time = (_time.time() - start_time) * 1000

        return {
            "total_flows": total_flows,
            "allowed_flows": allowed_count,
            "forbidden_flows": forbidden_count,
            "flow_health_percentage": round(flow_health, 1),
            "forbidden_flow_details": forbidden_details,
            "authority_chain_status": "healthy" if forbidden_count == 0 else "violations_detected",
            "execution_time_ms": round(execution_time, 2),
        }

    def get_sunset_governance_report(self) -> Dict:
        """
        Generate sunset governance report for deprecated artifacts.

        Integrates the SunsetGovernance module to provide visibility into:
        - All deprecated artifacts and their current sunset phase
        - Sunset-blocked artifacts (at sunset date but dependencies remain)
        - Age since deprecation and remaining days until sunset
        - Phase distribution across the deprecation pipeline

        Requirements: 25.1, 25.2

        Returns:
            Dictionary containing sunset governance metrics:
            - total_deprecated: Count of artifacts in deprecation pipeline
            - phase_distribution: Breakdown by sunset phase
            - sunset_blocked_count: Count of sunset-blocked artifacts
            - sunset_blocked_artifacts: List of blocked artifact details
            - deprecated_artifacts: List of all deprecated artifact details
        """
        registry_path = self.repo_root / ".domainization" / "artifact_registry.yaml"

        try:
            sunset_gov = SunsetGovernance(registry_path=str(registry_path))
            sunset_entries = sunset_gov.get_sunset_report()
        except Exception as e:
            self._emit_governance_event(
                Severity.WARNING,
                f"Failed to load sunset governance: {e}",
                "health_reporter.get_sunset_governance_report",
            )
            return {
                "total_deprecated": 0,
                "phase_distribution": {},
                "sunset_blocked_count": 0,
                "sunset_blocked_artifacts": [],
                "deprecated_artifacts": [],
                "error": str(e),
            }

        # Build phase distribution
        phase_distribution: Dict[str, int] = defaultdict(int)
        sunset_blocked_artifacts: List[Dict] = []
        deprecated_artifacts: List[Dict] = []

        for entry in sunset_entries:
            phase_distribution[entry.phase.value] += 1

            artifact_detail = {
                "artifact_id": entry.artifact_id,
                "phase": entry.phase.value,
                "deprecated_date": entry.deprecated_date,
                "sunset_date": entry.sunset_date,
                "replacement_artifact": entry.replacement_artifact,
                "deprecation_reason": entry.deprecation_reason,
                "compatibility_impact": entry.compatibility_impact,
                "age_days": entry.age_days,
                "remaining_days": entry.remaining_days,
                "downstream_dependency_count": entry.downstream_dependency_count,
                "sunset_blocked": entry.sunset_blocked,
            }
            deprecated_artifacts.append(artifact_detail)

            if entry.sunset_blocked:
                sunset_blocked_artifacts.append(artifact_detail)
                # Emit governance event for sunset-blocked artifacts
                self._emit_governance_event(
                    Severity.CRITICAL,
                    f"Artifact '{entry.artifact_id}' is sunset-blocked: "
                    f"{entry.downstream_dependency_count} downstream dependencies remain",
                    "health_reporter.get_sunset_governance_report",
                )

        total_deprecated = len(sunset_entries)

        # Emit informational event about sunset governance status
        if total_deprecated > 0:
            self._emit_governance_event(
                Severity.INFO,
                f"Sunset governance: {total_deprecated} artifacts in deprecation pipeline, "
                f"{len(sunset_blocked_artifacts)} sunset-blocked",
                "health_reporter.get_sunset_governance_report",
            )

        return {
            "total_deprecated": total_deprecated,
            "phase_distribution": dict(phase_distribution),
            "sunset_blocked_count": len(sunset_blocked_artifacts),
            "sunset_blocked_artifacts": sunset_blocked_artifacts,
            "deprecated_artifacts": deprecated_artifacts,
        }

    def get_integrity_verification(self) -> Dict:
        """
        Verify key integrity metrics for the health report.

        Checks three critical integrity conditions:
        1. Zero forbidden flows (Req 1.5)
        2. Zero unregistered artifacts (Req 3.4)
        3. 100% report_value coverage (Req 4.6)

        Emits governance events for any integrity failures and records
        state transitions when integrity degrades.

        Returns:
            Dictionary containing integrity verification results:
            - zero_forbidden_flows: Boolean indicating no forbidden flows
            - zero_unregistered_artifacts: Boolean indicating full registration
            - full_report_value_coverage: Boolean indicating 100% coverage
            - overall_integrity_state: RuntimeState string
            - details: Dict with specific metrics
        """
        previous_state = self._current_state

        # Check forbidden flows
        flow_analysis = self.get_runtime_flow_analysis()
        forbidden_flows = flow_analysis.get("forbidden_flows", 0)
        zero_forbidden_flows = forbidden_flows == 0

        # Check unregistered artifacts
        violations = self.violation_detector.detect_all_violations()
        unregistered_count = sum(
            1 for v in violations if v.violation_type == "unregistered"
        )
        zero_unregistered = unregistered_count == 0

        # Check report_value coverage
        report_value_health = self.get_report_value_health_score()
        valid_percentage = report_value_health.get("valid_percentage", 0.0)
        full_report_value_coverage = valid_percentage == 100.0

        # Determine overall integrity state
        if zero_forbidden_flows and zero_unregistered and full_report_value_coverage:
            overall_state = RuntimeState.HEALTHY
        elif forbidden_flows > 0:
            overall_state = RuntimeState.CANONICAL_BREAK
            self._emit_governance_event(
                Severity.CANONICAL_BREAK,
                f"{forbidden_flows} forbidden Signal-to-Report flows detected",
                "health_reporter.get_integrity_verification",
            )
        elif unregistered_count > 0:
            overall_state = RuntimeState.DEGRADED
            self._emit_governance_event(
                Severity.WARNING,
                f"{unregistered_count} unregistered artifacts detected",
                "health_reporter.get_integrity_verification",
            )
        else:
            overall_state = RuntimeState.DEGRADED
            self._emit_governance_event(
                Severity.WARNING,
                f"Report value coverage at {valid_percentage:.1f}% (target: 100%)",
                "health_reporter.get_integrity_verification",
            )

        # Record state transition if state changed
        if str(overall_state) != str(previous_state):
            reason_parts = []
            if not zero_forbidden_flows:
                reason_parts.append(f"{forbidden_flows} forbidden flows")
            if not zero_unregistered:
                reason_parts.append(f"{unregistered_count} unregistered artifacts")
            if not full_report_value_coverage:
                reason_parts.append(f"report_value coverage {valid_percentage:.1f}%")
            reason = "; ".join(reason_parts) if reason_parts else "All integrity checks passed"

            self._record_state_transition(
                previous_state=str(previous_state),
                new_state=str(overall_state),
                reason=reason,
            )

        return {
            "zero_forbidden_flows": zero_forbidden_flows,
            "zero_unregistered_artifacts": zero_unregistered,
            "full_report_value_coverage": full_report_value_coverage,
            "overall_integrity_state": str(overall_state),
            "details": {
                "forbidden_flow_count": forbidden_flows,
                "unregistered_artifact_count": unregistered_count,
                "report_value_valid_percentage": valid_percentage,
            },
        }

    def _generate_recommendations(self, violations: List) -> List[Dict]:
        """
        Generate recommendations based on violations
        
        Args:
            violations: List of violations
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Count violations by type
        by_type = defaultdict(int)
        for violation in violations:
            by_type[violation.violation_type] += 1
        
        # Generate recommendations based on violation patterns
        if by_type.get('unregistered', 0) > 0:
            recommendations.append({
                'priority': 'high',
                'action': f"Register {by_type['unregistered']} unregistered artifact(s)",
                'rationale': "Unregistered artifacts lack governance and lifecycle tracking"
            })
        
        if by_type.get('ssot_conflict', 0) > 0:
            recommendations.append({
                'priority': 'high',
                'action': f"Resolve {by_type['ssot_conflict']} SSOT conflict(s)",
                'rationale': "Multiple canonical SSOTs create ambiguity about authoritative source"
            })
        
        if by_type.get('missing_lifecycle', 0) > 0:
            recommendations.append({
                'priority': 'medium',
                'action': f"Add lifecycle status to {by_type['missing_lifecycle']} artifact(s)",
                'rationale': "Lifecycle status enables proper artifact maturity tracking"
            })
        
        if by_type.get('deprecated_modification', 0) > 0:
            recommendations.append({
                'priority': 'medium',
                'action': f"Review {by_type['deprecated_modification']} deprecated artifact modification(s)",
                'rationale': "Deprecated artifacts should not be modified except for metadata updates"
            })
        
        if by_type.get('missing_ssot_reference', 0) > 0:
            recommendations.append({
                'priority': 'medium',
                'action': f"Add SSOT references to {by_type['missing_ssot_reference']} artifact(s)",
                'rationale': "Derived and implementation artifacts must reference their canonical SSOT"
            })
        
        return recommendations
    
    def save_report(self, report: Dict, output_path: Optional[Path] = None) -> Path:
        """
        Save health report to YAML file
        
        Args:
            report: Health report dictionary
            output_path: Path to save report (uses default if None)
        
        Returns:
            Path where report was saved
        """
        if output_path is None:
            # Default to .domainization/reports/health_report_YYYY-MM-DD.yaml
            reports_dir = Path(__file__).parent.parent / "reports"
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_path = reports_dir / f"health_report_{timestamp}.yaml"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save report
        with open(output_path, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        return output_path
    
    def format_report_text(self, report: Dict) -> str:
        """
        Format health report as human-readable text
        
        Args:
            report: Health report dictionary
        
        Returns:
            Formatted text report
        """
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("DOMAINIZATION HEALTH REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {report['report_date']} {report['report_time']}")
        lines.append(f"Enforcement Mode: {report['enforcement_mode'].upper()}")
        lines.append("")
        
        # Summary
        summary = report['summary']
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Artifacts:        {summary['total_artifacts']}")
        lines.append(f"Registered Artifacts:   {summary['registered_artifacts']}")
        lines.append(f"Registration Coverage:  {summary['registration_percentage']:.1f}%")
        lines.append(f"Total Domains:          {summary['total_domains']}")
        lines.append(f"Domains with Artifacts: {summary['domains_with_artifacts']}")
        lines.append("")
        
        # Domain Coverage
        lines.append("DOMAIN COVERAGE")
        lines.append("-" * 80)
        for domain in report['domain_coverage']:
            if domain['artifact_count'] > 0:
                lines.append(f"\n{domain['domain_name']} ({domain['domain_id']}) - {domain['priority'].upper()}")
                lines.append(f"  Total: {domain['artifact_count']} artifacts")
                
                if domain['artifact_types']:
                    lines.append("  Breakdown:")
                    for atype in domain['artifact_types']:
                        lines.append(f"    - {atype['type']}: {atype['count']}")
        lines.append("")
        
        # Lifecycle Distribution
        lines.append("LIFECYCLE DISTRIBUTION")
        lines.append("-" * 80)
        for dist in report['lifecycle_distribution']:
            lines.append(f"\n{dist['artifact_type']} (Total: {dist['total_count']})")
            for state in dist['states']:
                lines.append(f"  - {state['state']}: {state['count']}")
        lines.append("")
        
        # Report-Value Health Score
        if 'report_value_health' in report:
            rvh = report['report_value_health']
            lines.append("REPORT-VALUE HEALTH SCORE")
            lines.append("-" * 80)
            lines.append(f"Total Artifacts Assessed:    {rvh.get('total_artifacts', 0)}")
            lines.append(f"With Report Value Declared:  {rvh.get('artifacts_with_report_value', 0)}")
            lines.append(f"With Valid Report Value:      {rvh.get('artifacts_with_valid_report_value', 0)}")
            lines.append(f"Speculative Claims:          {rvh.get('artifacts_speculative', 0)}")
            lines.append(f"Missing Report Value:        {rvh.get('artifacts_missing_report_value', 0)}")
            lines.append(f"Infrastructure-Heavy (drift): {rvh.get('artifacts_infrastructure_heavy', 0)}")
            lines.append("")
            lines.append(f"Coverage Percentage:         {rvh.get('coverage_percentage', 0.0):.1f}%")
            lines.append(f"Valid Percentage:             {rvh.get('valid_percentage', 0.0):.1f}%")
            lines.append(f"Infrastructure Drift:        {rvh.get('infrastructure_drift_percentage', 0.0):.1f}%")
            lines.append("")
            
            # Category distribution
            cat_dist = rvh.get('category_distribution', {})
            if cat_dist:
                lines.append("Category Distribution:")
                for category, count in sorted(cat_dist.items(), key=lambda x: x[1], reverse=True):
                    lines.append(f"  - {category}: {count}")
            lines.append("")
        
        # Runtime Flow Analysis (Req 14.1-14.7)
        if 'runtime_flow_analysis' in report:
            rfa = report['runtime_flow_analysis']
            lines.append("RUNTIME FLOW ANALYSIS")
            lines.append("-" * 80)
            lines.append(f"Total Flows Detected:        {rfa.get('total_flows', 0)}")
            lines.append(f"Allowed Flows:               {rfa.get('allowed_flows', 0)}")
            lines.append(f"Forbidden Flows:             {rfa.get('forbidden_flows', 0)}")
            lines.append(f"Flow Health:                 {rfa.get('flow_health_percentage', 100.0):.1f}%")
            lines.append(f"Authority Chain Status:      {rfa.get('authority_chain_status', 'unknown').upper()}")
            lines.append(f"Analysis Time:               {rfa.get('execution_time_ms', 0.0):.2f}ms")
            lines.append("")

            # Show forbidden flow details
            forbidden_details = rfa.get('forbidden_flow_details', [])
            if forbidden_details:
                lines.append("Forbidden Flow Details:")
                for detail in forbidden_details[:10]:  # Show first 10
                    lines.append(
                        f"  ⚠ {detail['source_domain']} → {detail['target_domain']} "
                        f"(artifact: {detail.get('artifact_id', 'unknown')})"
                    )
                    lines.append(f"    Reason: {detail['reason']}")
                    lines.append(f"    Fix: {detail.get('suggestion', 'Review authority chain')}")
                    lines.append("")

                if len(forbidden_details) > 10:
                    lines.append(f"... and {len(forbidden_details) - 10} more forbidden flows")
                    lines.append("")
            else:
                lines.append("No forbidden flows detected. Authority chain is healthy.")
                lines.append("")

            # Show allowed authority chain
            lines.append("Valid Authority Chain: SIGNALS (L1) → SEMANTICS (L2) → REASONING (L3) → REPORT (L4)")
            lines.append("")
        
        # Violations (if present)
        if 'violations' in report and report['violations']:
            lines.append("VIOLATIONS")
            lines.append("-" * 80)
            lines.append(f"Total Violations: {report['summary']['total_violations']}")
            
            by_severity = report['summary']['violations_by_severity']
            lines.append(f"  Critical: {by_severity['critical']}")
            lines.append(f"  High:     {by_severity['high']}")
            lines.append(f"  Medium:   {by_severity['medium']}")
            lines.append(f"  Low:      {by_severity['low']}")
            lines.append("")
            
            # Show top violations
            for violation in report['violations'][:10]:  # Show first 10
                severity_icon = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(violation['severity'], '⚪')
                
                lines.append(f"{severity_icon} [{violation['violation_type']}] {violation['file_path']}")
                lines.append(f"  {violation['description']}")
                lines.append(f"  → {violation['recommendation']}")
                lines.append("")
            
            if len(report['violations']) > 10:
                lines.append(f"... and {len(report['violations']) - 10} more violations")
                lines.append("")
        
        # Recommendations (if present)
        if 'recommendations' in report and report['recommendations']:
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 80)
            for rec in report['recommendations']:
                priority_icon = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(rec['priority'], '⚪')
                
                lines.append(f"{priority_icon} [{rec['priority'].upper()}] {rec['action']}")
                lines.append(f"  Rationale: {rec['rationale']}")
                lines.append("")
        
        # Sunset Governance (Req 25.1, 25.2)
        if 'sunset_governance' in report:
            sg = report['sunset_governance']
            lines.append("SUNSET GOVERNANCE")
            lines.append("-" * 80)
            lines.append(f"Total Deprecated Artifacts:  {sg.get('total_deprecated', 0)}")
            lines.append(f"Sunset-Blocked Artifacts:    {sg.get('sunset_blocked_count', 0)}")
            lines.append("")

            # Phase distribution
            phase_dist = sg.get('phase_distribution', {})
            if phase_dist:
                lines.append("Phase Distribution:")
                for phase, count in sorted(phase_dist.items()):
                    lines.append(f"  - {phase}: {count}")
                lines.append("")

            # Sunset-blocked details
            blocked = sg.get('sunset_blocked_artifacts', [])
            if blocked:
                lines.append("Sunset-Blocked Artifacts (CRITICAL):")
                for artifact in blocked[:10]:
                    lines.append(
                        f"  🔴 {artifact['artifact_id']} — "
                        f"{artifact['downstream_dependency_count']} deps remaining"
                    )
                    if artifact.get('deprecation_reason'):
                        lines.append(f"     Reason: {artifact['deprecation_reason']}")
                lines.append("")

            # Deprecated artifact summary
            deprecated = sg.get('deprecated_artifacts', [])
            if deprecated and not blocked:
                lines.append("Deprecated Artifacts:")
                for artifact in deprecated[:10]:
                    remaining = artifact.get('remaining_days')
                    remaining_str = f"{remaining} days remaining" if remaining is not None else "no sunset date"
                    lines.append(
                        f"  ⚠ {artifact['artifact_id']} [{artifact['phase']}] — "
                        f"age: {artifact['age_days']} days, {remaining_str}"
                    )
                if len(deprecated) > 10:
                    lines.append(f"  ... and {len(deprecated) - 10} more")
                lines.append("")

        # Integrity Verification (Req 1.5, 3.4, 4.6)
        if 'integrity_verification' in report:
            iv = report['integrity_verification']
            lines.append("INTEGRITY VERIFICATION")
            lines.append("-" * 80)
            lines.append(f"Overall Integrity State:     {iv.get('overall_integrity_state', 'unknown').upper()}")
            lines.append("")

            check_icon = lambda passed: "✓" if passed else "✗"
            lines.append(f"  {check_icon(iv.get('zero_forbidden_flows', False))} Zero Forbidden Flows")
            lines.append(f"  {check_icon(iv.get('zero_unregistered_artifacts', False))} Zero Unregistered Artifacts")
            lines.append(f"  {check_icon(iv.get('full_report_value_coverage', False))} 100% Report Value Coverage")
            lines.append("")

            details = iv.get('details', {})
            if details:
                lines.append("Details:")
                lines.append(f"  Forbidden Flows:           {details.get('forbidden_flow_count', 0)}")
                lines.append(f"  Unregistered Artifacts:    {details.get('unregistered_artifact_count', 0)}")
                lines.append(f"  Report Value Coverage:     {details.get('report_value_valid_percentage', 0.0):.1f}%")
            lines.append("")

        # Governance Events (Req 17.4, 18.4)
        if 'governance_events' in report and report['governance_events']:
            events = report['governance_events']
            lines.append("GOVERNANCE EVENTS")
            lines.append("-" * 80)
            lines.append(f"Total Events: {len(events)}")
            lines.append("")

            for event in events[:20]:
                severity_icon = {
                    'INFO': '🔵',
                    'WARNING': '🟡',
                    'DEGRADED': '🟠',
                    'CRITICAL': '🔴',
                    'CANONICAL_BREAK': '⛔',
                    'DETERMINISTIC_FAILURE': '💀',
                }.get(event.get('severity', ''), '⚪')

                lines.append(
                    f"  {severity_icon} [{event.get('severity', 'UNKNOWN')}] "
                    f"{event.get('description', '')}"
                )
                lines.append(
                    f"     Component: {event.get('component', 'unknown')} | "
                    f"Time: {event.get('timestamp', 'unknown')}"
                )
                lines.append("")

            if len(events) > 20:
                lines.append(f"  ... and {len(events) - 20} more events")
                lines.append("")

        # State Transitions (Req 18.4)
        if 'state_transitions' in report and report['state_transitions']:
            transitions = report['state_transitions']
            lines.append("STATE TRANSITIONS")
            lines.append("-" * 80)
            lines.append(f"Total Transitions: {len(transitions)}")
            lines.append("")

            for transition in transitions[:10]:
                lines.append(
                    f"  {transition.get('previous_state', '?')} → "
                    f"{transition.get('new_state', '?')}"
                )
                lines.append(f"     Reason: {transition.get('reason', 'unknown')}")
                lines.append(f"     Time: {transition.get('timestamp', 'unknown')}")
                lines.append("")

            if len(transitions) > 10:
                lines.append(f"  ... and {len(transitions) - 10} more transitions")
                lines.append("")

        lines.append("=" * 80)
        
        return '\n'.join(lines)
