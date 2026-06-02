"""
Integration tests for runtime flow detection in Observer 4 (Boundary Awareness).

Tests the full flow: artifact with dependencies → observer detects forbidden flow
→ warning generated → flow shown in health report.

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from artifact_schema import ArtifactMetadata
from observer_boundary_awareness import BoundaryAwarenessValidator
from health_reporter import HealthReporter
from runtime_flow_detector import FlowStatus
from validation_result import WarningCodes


@pytest.fixture
def temp_repo():
    """Create temporary repository structure with domain registry"""
    temp_dir = tempfile.mkdtemp()
    repo_root = Path(temp_dir)

    # Create .domainization directory
    domainization_dir = repo_root / '.domainization'
    domainization_dir.mkdir()
    (domainization_dir / 'reports').mkdir()
    (domainization_dir / 'logs').mkdir()

    # Create empty artifact registry
    artifact_registry_file = domainization_dir / 'artifact_registry.yaml'
    artifact_registry_file.write_text('artifacts: []\n')

    # Create domain registry with all core reasoning domains
    domain_registry_file = domainization_dir / 'domain_registry.yaml'
    domains_data = {
        'domains': [
            {
                'domain_id': 'SIGNALS',
                'name': 'Signal Generation',
                'responsibility_scope': 'Generate structured signals',
                'allowed_artifact_types': ['ENGINE', 'SSOT', 'DATA_OUT'],
                'cannot_own': ['REPORT_OUT', 'SEMANTIC_STATE'],
                'priority': 'core',
                'authority_level': 1
            },
            {
                'domain_id': 'SEMANTICS',
                'name': 'Semantic Interpretation',
                'responsibility_scope': 'Interpret signals semantically',
                'allowed_artifact_types': ['ENGINE', 'SSOT', 'SEMANTIC_STATE'],
                'cannot_own': ['SIGNAL', 'REPORT_OUT'],
                'priority': 'core',
                'authority_level': 2
            },
            {
                'domain_id': 'REASONING',
                'name': 'Reasoning Logic',
                'responsibility_scope': 'Apply reasoning',
                'allowed_artifact_types': ['ENGINE', 'SSOT', 'REASONING_OBJECT'],
                'cannot_own': ['SIGNAL', 'SEMANTIC_STATE', 'REPORT_OUT'],
                'priority': 'core',
                'authority_level': 3
            },
            {
                'domain_id': 'REPORT',
                'name': 'Report Generation',
                'responsibility_scope': 'Generate reports',
                'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT'],
                'cannot_own': ['SIGNAL', 'SEMANTIC_STATE', 'REASONING_OBJECT'],
                'priority': 'core',
                'authority_level': 4
            },
            {
                'domain_id': 'USER',
                'name': 'User Interface',
                'responsibility_scope': 'Dashboard and user interaction',
                'allowed_artifact_types': ['DASHBOARD', 'CONFIG'],
                'cannot_own': ['SIGNAL', 'SEMANTIC_STATE'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'DATA',
                'name': 'Data Management',
                'responsibility_scope': 'Data normalization',
                'allowed_artifact_types': ['DATA_IN', 'DATA_OUT', 'ENGINE'],
                'cannot_own': [],
                'priority': 'surface',
                'authority_level': None
            },
        ]
    }
    with open(domain_registry_file, 'w') as f:
        yaml.dump(domains_data, f)

    # Create lifecycle state machine
    lifecycle_file = domainization_dir / 'lifecycle_state_machine.yaml'
    lifecycle_data = {
        'artifact_types': {
            'ENGINE': {
                'states': ['planned', 'development', 'active', 'deprecated'],
                'transitions': [
                    {'from': 'planned', 'to': 'development'},
                    {'from': 'development', 'to': 'active'},
                    {'from': 'active', 'to': 'deprecated'},
                ]
            },
            'REPORT_OUT': {
                'states': ['generated', 'current', 'archived'],
                'transitions': [
                    {'from': 'generated', 'to': 'current'},
                    {'from': 'current', 'to': 'archived'},
                ]
            },
            'DATA_OUT': {
                'states': ['generated', 'current', 'archived'],
                'transitions': [
                    {'from': 'generated', 'to': 'current'},
                    {'from': 'current', 'to': 'archived'},
                ]
            },
            'DASHBOARD': {
                'states': ['planned', 'development', 'active', 'deprecated'],
                'transitions': [
                    {'from': 'planned', 'to': 'development'},
                    {'from': 'development', 'to': 'active'},
                    {'from': 'active', 'to': 'deprecated'},
                ]
            },
        }
    }
    with open(lifecycle_file, 'w') as f:
        yaml.dump(lifecycle_data, f)

    yield repo_root

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def artifact_registry(temp_repo):
    """Create artifact registry"""
    registry_path = temp_repo / '.domainization' / 'artifact_registry.yaml'
    registry = ArtifactRegistry(registry_path)
    registry.load()
    return registry


@pytest.fixture
def domain_registry(temp_repo):
    """Create domain registry"""
    registry_path = temp_repo / '.domainization' / 'domain_registry.yaml'
    registry = DomainRegistry(registry_path)
    registry.load()
    return registry


@pytest.fixture
def validator(artifact_registry, domain_registry):
    """Create boundary awareness validator with flow detection"""
    return BoundaryAwarenessValidator(artifact_registry, domain_registry)


def _make_artifact(artifact_id, file_path, domain, artifact_type,
                   lifecycle_status="active", dependencies=None):
    """Helper to create ArtifactMetadata"""
    return ArtifactMetadata(
        artifact_id=artifact_id,
        file_path=file_path,
        primary_domain=domain,
        artifact_type=artifact_type,
        lifecycle_status=lifecycle_status,
        created_date='2026-01-01',
        last_modified='2026-01-01',
        owner_role='Engineer',
        ssot_relationship='none',
        allowed_writers=[domain],
        allowed_readers=['ALL'],
        dependencies=dependencies,
    )


# ============================================================
# Requirement 14.1: Allowed flow SIGNALS → SEMANTICS → REASONING → REPORT
# ============================================================

class TestAllowedFlowsIntegration:
    """Integration tests for allowed authority chain flows"""

    def test_valid_chain_no_warnings(self, validator, artifact_registry):
        """Full valid chain produces no flow warnings (Req 14.1)"""
        # Register chain: signal → semantic → reasoning → report
        signal = _make_artifact(
            "signal-engine", "signal_engine.py", "SIGNALS", "ENGINE"
        )
        semantic = _make_artifact(
            "semantic-engine", "semantic_engine.py", "SEMANTICS", "ENGINE",
            dependencies=["signal-engine"]
        )
        reasoning = _make_artifact(
            "reasoning-engine", "reasoning_engine.py", "REASONING", "ENGINE",
            dependencies=["semantic-engine"]
        )
        report = _make_artifact(
            "report-output", "report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["reasoning-engine"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(semantic)
        artifact_registry.register_artifact(reasoning)
        artifact_registry.register_artifact(report)

        # Validate - should have no flow warnings
        result = validator.validate()
        flow_warnings = [
            w for w in result.warnings
            if w.warning_code in (
                WarningCodes.W700_FORBIDDEN_RUNTIME_FLOW,
                WarningCodes.W701_AUTHORITY_CHAIN_SKIP,
                WarningCodes.W702_BACKWARD_AUTHORITY_FLOW,
                WarningCodes.W703_SURFACE_TO_CORE_FLOW,
            )
        ]
        assert len(flow_warnings) == 0

    def test_signals_to_semantics_allowed(self, validator, artifact_registry):
        """SIGNALS → SEMANTICS dependency is allowed (Req 14.1)"""
        signal = _make_artifact(
            "signal-1", "signal.py", "SIGNALS", "ENGINE"
        )
        semantic = _make_artifact(
            "semantic-1", "semantic.py", "SEMANTICS", "ENGINE",
            dependencies=["signal-1"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(semantic)

        result = validator.validate()
        flow_warnings = [
            w for w in result.warnings
            if w.warning_code.startswith("W7")
        ]
        assert len(flow_warnings) == 0


# ============================================================
# Requirement 14.2: Signal → Report is forbidden
# ============================================================

class TestSignalToReportForbiddenIntegration:
    """Integration tests for Signal → Report forbidden flow"""

    def test_signal_to_report_generates_warning(self, validator, artifact_registry):
        """Report depending directly on Signal generates warning (Req 14.2)"""
        signal = _make_artifact(
            "signal-output", "signal_output.py", "SIGNALS", "DATA_OUT"
        )
        report = _make_artifact(
            "report-direct", "report_direct.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["signal-output"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)

        result = validator.validate()
        flow_warnings = [
            w for w in result.warnings
            if w.warning_code.startswith("W7")
        ]
        assert len(flow_warnings) >= 1
        assert any("SIGNALS" in w.warning_message and "REPORT" in w.warning_message
                   for w in flow_warnings)

    def test_signal_to_report_warning_has_suggestion(self, validator, artifact_registry):
        """Forbidden flow warning includes actionable suggestion (Req 14.2)"""
        signal = _make_artifact(
            "sig-1", "sig.py", "SIGNALS", "ENGINE"
        )
        report = _make_artifact(
            "rpt-1", "rpt.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["sig-1"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 1
        assert flow_warnings[0].suggestion  # Has a suggestion


# ============================================================
# Requirement 14.3: Signal → Reasoning is forbidden
# ============================================================

class TestSignalToReasoningForbiddenIntegration:
    """Integration tests for Signal → Reasoning forbidden flow"""

    def test_signal_to_reasoning_generates_warning(self, validator, artifact_registry):
        """Reasoning depending directly on Signal generates warning (Req 14.3)"""
        signal = _make_artifact(
            "signal-raw", "signal_raw.py", "SIGNALS", "ENGINE"
        )
        reasoning = _make_artifact(
            "reasoning-direct", "reasoning_direct.py", "REASONING", "ENGINE",
            dependencies=["signal-raw"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(reasoning)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 1
        assert any("SIGNALS" in w.warning_message and "REASONING" in w.warning_message
                   for w in flow_warnings)


# ============================================================
# Requirement 14.4: Dashboard → Semantic Truth is forbidden
# ============================================================

class TestDashboardToSemanticForbiddenIntegration:
    """Integration tests for Dashboard → Semantic Truth forbidden flow"""

    def test_dashboard_to_semantics_generates_warning(self, validator, artifact_registry):
        """Semantic artifact depending on Dashboard generates warning (Req 14.4)"""
        dashboard = _make_artifact(
            "dashboard-app", "app.py", "USER", "DASHBOARD"
        )
        semantic = _make_artifact(
            "semantic-from-dash", "semantic_from_dash.py", "SEMANTICS", "ENGINE",
            dependencies=["dashboard-app"]
        )

        artifact_registry.register_artifact(dashboard)
        artifact_registry.register_artifact(semantic)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 1
        assert any(
            w.warning_code == WarningCodes.W703_SURFACE_TO_CORE_FLOW
            for w in flow_warnings
        )


# ============================================================
# Requirement 14.5: Dashboard → Signal Generation is forbidden
# ============================================================

class TestDashboardToSignalForbiddenIntegration:
    """Integration tests for Dashboard → Signal Generation forbidden flow"""

    def test_dashboard_to_signals_generates_warning(self, validator, artifact_registry):
        """Signal artifact depending on Dashboard generates warning (Req 14.5)"""
        dashboard = _make_artifact(
            "user-dashboard", "dashboard.py", "USER", "DASHBOARD"
        )
        signal = _make_artifact(
            "signal-from-dash", "signal_from_dash.py", "SIGNALS", "ENGINE",
            dependencies=["user-dashboard"]
        )

        artifact_registry.register_artifact(dashboard)
        artifact_registry.register_artifact(signal)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 1
        assert any(
            w.warning_code == WarningCodes.W703_SURFACE_TO_CORE_FLOW
            for w in flow_warnings
        )


# ============================================================
# Requirement 14.6: Forbidden flows logged with details
# ============================================================

class TestForbiddenFlowLogging:
    """Integration tests for forbidden flow logging"""

    def test_forbidden_flow_warning_has_details(self, validator, artifact_registry):
        """Forbidden flow warning includes full details (Req 14.6)"""
        signal = _make_artifact(
            "sig-detail", "sig_detail.py", "SIGNALS", "ENGINE"
        )
        report = _make_artifact(
            "rpt-detail", "rpt_detail.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["sig-detail"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 1

        warning = flow_warnings[0]
        # Warning must include: source domain, target domain, reason
        assert "SIGNALS" in warning.warning_message
        assert "REPORT" in warning.warning_message
        assert "authority chain violation" in warning.warning_message.lower() or \
               "forbidden" in warning.warning_message.lower()
        # Must have artifact reference
        assert warning.artifact_id == "rpt-detail"
        # Must have file path
        assert warning.file_path == "rpt_detail.txt"

    def test_forbidden_flow_severity_is_high(self, validator, artifact_registry):
        """Forbidden flow warnings have high severity (Req 14.6)"""
        signal = _make_artifact(
            "sig-sev", "sig_sev.py", "SIGNALS", "ENGINE"
        )
        reasoning = _make_artifact(
            "rsn-sev", "rsn_sev.py", "REASONING", "ENGINE",
            dependencies=["sig-sev"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(reasoning)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert all(w.severity == "high" for w in flow_warnings)

    def test_no_blocking_only_warnings(self, validator, artifact_registry):
        """System operates in observability mode - warnings only, no blocking (Req 14.6)"""
        signal = _make_artifact(
            "sig-obs", "sig_obs.py", "SIGNALS", "ENGINE"
        )
        report = _make_artifact(
            "rpt-obs", "rpt_obs.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["sig-obs"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)

        # Validate returns a result (not an exception/block)
        result = validator.validate()
        assert result is not None
        assert result.observer_name == "BoundaryAwarenessValidator"
        # Warnings exist but validation completes successfully
        assert result.has_warnings()


# ============================================================
# Requirement 14.7: Flow traceability
# ============================================================

class TestFlowTraceability:
    """Integration tests for flow traceability"""

    def test_trace_valid_chain(self, validator, artifact_registry):
        """Traceability shows complete signal-to-report chain (Req 14.7)"""
        signal = _make_artifact(
            "trace-signal", "trace_signal.py", "SIGNALS", "ENGINE"
        )
        semantic = _make_artifact(
            "trace-semantic", "trace_semantic.py", "SEMANTICS", "ENGINE",
            dependencies=["trace-signal"]
        )
        reasoning = _make_artifact(
            "trace-reasoning", "trace_reasoning.py", "REASONING", "ENGINE",
            dependencies=["trace-semantic"]
        )
        report = _make_artifact(
            "trace-report", "trace_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["trace-reasoning"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(semantic)
        artifact_registry.register_artifact(reasoning)
        artifact_registry.register_artifact(report)

        # Get traceability for the report artifact
        trace = validator.get_flow_traceability("trace-report")

        assert trace is not None
        assert trace["artifact_id"] == "trace-report"
        assert trace["domain"] == "REPORT"
        assert trace["is_valid"] is True
        assert len(trace["violations"]) == 0

        # Chain should show full path
        domain_path = trace["domain_path"]
        assert "SIGNALS" in domain_path
        assert "SEMANTICS" in domain_path
        assert "REASONING" in domain_path
        assert "REPORT" in domain_path

    def test_trace_invalid_chain(self, validator, artifact_registry):
        """Traceability shows violations in invalid chain (Req 14.7)"""
        signal = _make_artifact(
            "trace-sig-bad", "trace_sig_bad.py", "SIGNALS", "ENGINE"
        )
        report = _make_artifact(
            "trace-rpt-bad", "trace_rpt_bad.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["trace-sig-bad"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)

        trace = validator.get_flow_traceability("trace-rpt-bad")

        assert trace is not None
        assert trace["is_valid"] is False
        assert len(trace["violations"]) > 0

    def test_trace_nonexistent_artifact(self, validator, artifact_registry):
        """Traceability returns None for nonexistent artifact"""
        trace = validator.get_flow_traceability("nonexistent-artifact")
        assert trace is None

    def test_trace_visualization_ascii(self, validator, artifact_registry):
        """Traceability includes ASCII visualization (Req 14.7)"""
        signal = _make_artifact(
            "viz-signal", "viz_signal.py", "SIGNALS", "ENGINE"
        )
        semantic = _make_artifact(
            "viz-semantic", "viz_semantic.py", "SEMANTICS", "ENGINE",
            dependencies=["viz-signal"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(semantic)

        trace = validator.get_flow_traceability("viz-semantic")

        assert trace is not None
        assert "visualization" in trace
        assert "Authority Chain" in trace["visualization"]
        assert "SIGNALS" in trace["visualization"]
        assert "SEMANTICS" in trace["visualization"]

    def test_trace_no_dependencies(self, validator, artifact_registry):
        """Traceability for artifact with no dependencies shows single step"""
        signal = _make_artifact(
            "solo-signal", "solo_signal.py", "SIGNALS", "ENGINE"
        )
        artifact_registry.register_artifact(signal)

        trace = validator.get_flow_traceability("solo-signal")

        assert trace is not None
        assert len(trace["chain"]) == 1
        assert trace["chain"][0]["artifact_id"] == "solo-signal"


# ============================================================
# Health Report Flow Visualization Integration
# ============================================================

class TestHealthReportFlowVisualization:
    """Integration tests for flow visualization in health reports"""

    def test_health_report_includes_flow_analysis(self, temp_repo, artifact_registry, domain_registry):
        """Health report includes runtime flow analysis section"""
        # Register artifacts with a forbidden flow
        signal = _make_artifact(
            "hr-signal", "hr_signal.py", "SIGNALS", "ENGINE"
        )
        report = _make_artifact(
            "hr-report", "hr_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["hr-signal"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)
        artifact_registry.save()

        # Create health reporter
        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            repo_root=temp_repo,
        )

        health_report = reporter.generate_health_report(include_violations=False)

        # Report must include runtime flow analysis
        assert 'runtime_flow_analysis' in health_report
        rfa = health_report['runtime_flow_analysis']
        assert rfa['total_flows'] >= 1
        assert rfa['forbidden_flows'] >= 1
        assert rfa['authority_chain_status'] == 'violations_detected'

    def test_health_report_flow_analysis_healthy(self, temp_repo, artifact_registry, domain_registry):
        """Health report shows healthy status when no forbidden flows"""
        # Register artifacts with valid chain
        signal = _make_artifact(
            "healthy-signal", "healthy_signal.py", "SIGNALS", "ENGINE"
        )
        semantic = _make_artifact(
            "healthy-semantic", "healthy_semantic.py", "SEMANTICS", "ENGINE",
            dependencies=["healthy-signal"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(semantic)
        artifact_registry.save()

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            repo_root=temp_repo,
        )

        health_report = reporter.generate_health_report(include_violations=False)

        rfa = health_report['runtime_flow_analysis']
        assert rfa['forbidden_flows'] == 0
        assert rfa['allowed_flows'] >= 1
        assert rfa['authority_chain_status'] == 'healthy'
        assert rfa['flow_health_percentage'] == 100.0

    def test_health_report_summary_includes_flow_counts(self, temp_repo, artifact_registry, domain_registry):
        """Health report summary includes flow detection counts"""
        signal = _make_artifact(
            "sum-signal", "sum_signal.py", "SIGNALS", "ENGINE"
        )
        report = _make_artifact(
            "sum-report", "sum_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["sum-signal"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report)
        artifact_registry.save()

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            repo_root=temp_repo,
        )

        health_report = reporter.generate_health_report(include_violations=False)

        assert 'total_flows_detected' in health_report['summary']
        assert 'forbidden_flows_detected' in health_report['summary']
        assert health_report['summary']['forbidden_flows_detected'] >= 1

    def test_health_report_text_format_includes_flows(self, temp_repo, artifact_registry, domain_registry):
        """Formatted text report includes runtime flow analysis section"""
        signal = _make_artifact(
            "fmt-signal", "fmt_signal.py", "SIGNALS", "ENGINE"
        )
        report_artifact = _make_artifact(
            "fmt-report", "fmt_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["fmt-signal"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report_artifact)
        artifact_registry.save()

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            repo_root=temp_repo,
        )

        health_report = reporter.generate_health_report(include_violations=False)
        text_report = reporter.format_report_text(health_report)

        assert "RUNTIME FLOW ANALYSIS" in text_report
        assert "Forbidden Flows" in text_report or "Forbidden Flow" in text_report
        assert "Authority Chain Status" in text_report
        assert "SIGNALS" in text_report


# ============================================================
# Full Integration: End-to-End Flow
# ============================================================

class TestEndToEndFlowDetection:
    """End-to-end integration tests for the complete flow"""

    def test_full_flow_artifact_to_warning_to_report(
        self, temp_repo, artifact_registry, domain_registry
    ):
        """
        Full integration: artifact with forbidden dependency → observer detects
        → warning generated → flow shown in health report
        """
        # Step 1: Register artifacts with a forbidden flow (Signal → Report)
        signal = _make_artifact(
            "e2e-signal", "e2e_signal.py", "SIGNALS", "ENGINE"
        )
        report_artifact = _make_artifact(
            "e2e-report", "e2e_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["e2e-signal"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(report_artifact)
        artifact_registry.save()

        # Step 2: Observer detects forbidden flow
        validator = BoundaryAwarenessValidator(artifact_registry, domain_registry)
        result = validator.validate()

        # Step 3: Warning is generated
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 1
        assert flow_warnings[0].artifact_id == "e2e-report"
        assert "SIGNALS" in flow_warnings[0].warning_message
        assert "REPORT" in flow_warnings[0].warning_message

        # Step 4: Flow shown in health report
        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            repo_root=temp_repo,
        )
        health_report = reporter.generate_health_report(include_violations=False)

        rfa = health_report['runtime_flow_analysis']
        assert rfa['forbidden_flows'] >= 1
        assert len(rfa['forbidden_flow_details']) >= 1

        # Verify the forbidden flow detail
        detail = rfa['forbidden_flow_details'][0]
        assert detail['source_domain'] == 'SIGNALS'
        assert detail['target_domain'] == 'REPORT'
        assert detail['artifact_id'] == 'e2e-report'

    def test_detect_all_runtime_flows(self, validator, artifact_registry):
        """detect_all_runtime_flows scans all artifacts"""
        signal = _make_artifact(
            "all-signal", "all_signal.py", "SIGNALS", "ENGINE"
        )
        semantic = _make_artifact(
            "all-semantic", "all_semantic.py", "SEMANTICS", "ENGINE",
            dependencies=["all-signal"]
        )
        report = _make_artifact(
            "all-report", "all_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["all-signal"]  # Forbidden: SIGNALS → REPORT
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(semantic)
        artifact_registry.register_artifact(report)

        result = validator.detect_all_runtime_flows()

        assert result.allowed_count >= 1  # SIGNALS → SEMANTICS
        assert result.forbidden_count >= 1  # SIGNALS → REPORT
        assert result.execution_time_ms >= 0

    def test_no_dependencies_no_flows(self, validator, artifact_registry):
        """Artifacts without dependencies produce no flow detections"""
        signal = _make_artifact(
            "nodep-signal", "nodep_signal.py", "SIGNALS", "ENGINE"
        )
        artifact_registry.register_artifact(signal)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) == 0

    def test_multiple_forbidden_flows_all_detected(self, validator, artifact_registry):
        """Multiple forbidden flows are all detected"""
        signal = _make_artifact(
            "multi-signal", "multi_signal.py", "SIGNALS", "ENGINE"
        )
        dashboard = _make_artifact(
            "multi-dash", "multi_dash.py", "USER", "DASHBOARD"
        )
        # Report depends on signal (forbidden: SIGNALS → REPORT)
        report = _make_artifact(
            "multi-report", "multi_report.txt", "REPORT", "REPORT_OUT",
            lifecycle_status="current",
            dependencies=["multi-signal"]
        )
        # Semantic depends on dashboard (forbidden: USER → SEMANTICS)
        semantic = _make_artifact(
            "multi-semantic", "multi_semantic.py", "SEMANTICS", "ENGINE",
            dependencies=["multi-dash"]
        )

        artifact_registry.register_artifact(signal)
        artifact_registry.register_artifact(dashboard)
        artifact_registry.register_artifact(report)
        artifact_registry.register_artifact(semantic)

        result = validator.validate()
        flow_warnings = [w for w in result.warnings if w.warning_code.startswith("W7")]
        assert len(flow_warnings) >= 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
