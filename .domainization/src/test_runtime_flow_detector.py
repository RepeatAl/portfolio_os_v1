"""
Unit tests for Runtime Flow Detector

Tests flow detection, authority chain validation, forbidden flow detection,
and authority chain visualization.

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.8, 14.9, 14.10
"""

import pytest
from runtime_flow_detector import (
    RuntimeFlowDetector,
    FlowStatus,
    FlowStep,
    RuntimeFlow,
    AuthorityChainVisualization,
    FlowDetectionResult,
)


@pytest.fixture
def detector():
    """Create a RuntimeFlowDetector instance"""
    return RuntimeFlowDetector()


# ============================================================
# Requirement 14.1: Allowed flow SIGNALS → SEMANTICS → REASONING → REPORT
# ============================================================

class TestAllowedFlows:
    """Test that the full authority chain is allowed"""

    def test_signals_to_semantics_allowed(self, detector):
        """SIGNALS → SEMANTICS is a valid authority chain step"""
        flow = detector.detect_flow("SIGNALS", "SEMANTICS")
        assert flow.status == FlowStatus.ALLOWED
        assert flow.source_domain == "SIGNALS"
        assert flow.target_domain == "SEMANTICS"

    def test_semantics_to_reasoning_allowed(self, detector):
        """SEMANTICS → REASONING is a valid authority chain step"""
        flow = detector.detect_flow("SEMANTICS", "REASONING")
        assert flow.status == FlowStatus.ALLOWED

    def test_reasoning_to_report_allowed(self, detector):
        """REASONING → REPORT is a valid authority chain step"""
        flow = detector.detect_flow("REASONING", "REPORT")
        assert flow.status == FlowStatus.ALLOWED

    def test_full_chain_path_allowed(self, detector):
        """Full chain SIGNALS → SEMANTICS → REASONING → REPORT is valid"""
        result = detector.validate_flow_path(
            ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]
        )
        assert result.forbidden_count == 0
        assert result.allowed_count == 3  # 3 steps in a 4-domain path
        assert not result.has_violations()

    def test_same_domain_flow_allowed(self, detector):
        """Same-domain flow is always allowed (internal)"""
        flow = detector.detect_flow("SIGNALS", "SIGNALS")
        assert flow.status == FlowStatus.ALLOWED

    def test_surface_to_surface_allowed(self, detector):
        """Surface-to-surface flows are allowed"""
        flow = detector.detect_flow("DATA", "STATE")
        assert flow.status == FlowStatus.ALLOWED


# ============================================================
# Requirement 14.2: Signal → Report is forbidden
# ============================================================

class TestSignalToReportForbidden:
    """Test that Signal → Report flow is forbidden"""

    def test_signal_to_report_forbidden(self, detector):
        """SIGNALS → REPORT is explicitly forbidden"""
        flow = detector.detect_flow("SIGNALS", "REPORT")
        assert flow.status == FlowStatus.FORBIDDEN
        assert "14.2" in flow.reason

    def test_signal_to_report_has_suggestion(self, detector):
        """Forbidden flow provides actionable suggestion"""
        flow = detector.detect_flow("SIGNALS", "REPORT")
        assert "SEMANTICS" in flow.suggestion
        assert "REASONING" in flow.suggestion

    def test_signal_to_report_with_artifact(self, detector):
        """Forbidden flow tracks artifact ID"""
        flow = detector.detect_flow("SIGNALS", "REPORT", artifact_id="test-artifact")
        assert flow.artifact_id == "test-artifact"
        assert flow.status == FlowStatus.FORBIDDEN


# ============================================================
# Requirement 14.3: Signal → Reasoning is forbidden
# ============================================================

class TestSignalToReasoningForbidden:
    """Test that Signal → Reasoning flow is forbidden"""

    def test_signal_to_reasoning_forbidden(self, detector):
        """SIGNALS → REASONING is explicitly forbidden"""
        flow = detector.detect_flow("SIGNALS", "REASONING")
        assert flow.status == FlowStatus.FORBIDDEN
        assert "14.3" in flow.reason

    def test_signal_to_reasoning_has_suggestion(self, detector):
        """Forbidden flow provides suggestion to route through SEMANTICS"""
        flow = detector.detect_flow("SIGNALS", "REASONING")
        assert "SEMANTICS" in flow.suggestion


# ============================================================
# Requirement 14.4: Dashboard → Semantic Truth is forbidden
# ============================================================

class TestDashboardToSemanticForbidden:
    """Test that Dashboard → Semantic Truth flow is forbidden"""

    def test_dashboard_to_semantics_forbidden(self, detector):
        """USER (Dashboard) → SEMANTICS is forbidden"""
        flow = detector.detect_flow("USER", "SEMANTICS")
        assert flow.status == FlowStatus.FORBIDDEN
        assert "14.4" in flow.reason

    def test_dashboard_to_semantics_suggestion(self, detector):
        """Provides guidance that dashboard should read, not create"""
        flow = detector.detect_flow("USER", "SEMANTICS")
        assert "read" in flow.suggestion.lower() or "SIGNALS" in flow.suggestion


# ============================================================
# Requirement 14.5: Dashboard → Signal Generation is forbidden
# ============================================================

class TestDashboardToSignalForbidden:
    """Test that Dashboard → Signal Generation flow is forbidden"""

    def test_dashboard_to_signals_forbidden(self, detector):
        """USER (Dashboard) → SIGNALS is forbidden"""
        flow = detector.detect_flow("USER", "SIGNALS")
        assert flow.status == FlowStatus.FORBIDDEN
        assert "14.5" in flow.reason

    def test_dashboard_to_signals_suggestion(self, detector):
        """Provides guidance that dashboard cannot generate signals"""
        flow = detector.detect_flow("USER", "SIGNALS")
        assert "SIGNALS" in flow.suggestion


# ============================================================
# Requirement 14.8: Flows represent authority chains
# ============================================================

class TestAuthorityChains:
    """Test that flows represent authority chains, not just data flows"""

    def test_backward_flow_forbidden(self, detector):
        """Backward authority flow is forbidden (higher level → lower level)"""
        flow = detector.detect_flow("REPORT", "SIGNALS")
        assert flow.status == FlowStatus.FORBIDDEN
        assert "authority" in flow.reason.lower() or "forward" in flow.reason.lower()

    def test_reasoning_to_signals_forbidden(self, detector):
        """REASONING → SIGNALS is a backward authority flow"""
        flow = detector.detect_flow("REASONING", "SIGNALS")
        assert flow.status == FlowStatus.FORBIDDEN

    def test_reasoning_to_semantics_forbidden(self, detector):
        """REASONING → SEMANTICS is a backward authority flow"""
        flow = detector.detect_flow("REASONING", "SEMANTICS")
        assert flow.status == FlowStatus.FORBIDDEN

    def test_semantics_to_signals_forbidden(self, detector):
        """SEMANTICS → SIGNALS is a backward authority flow"""
        flow = detector.detect_flow("SEMANTICS", "SIGNALS")
        assert flow.status == FlowStatus.FORBIDDEN

    def test_report_to_reasoning_forbidden(self, detector):
        """REPORT → REASONING is a backward authority flow"""
        flow = detector.detect_flow("REPORT", "REASONING")
        assert flow.status == FlowStatus.FORBIDDEN

    def test_report_to_semantics_forbidden(self, detector):
        """REPORT → SEMANTICS is a backward authority flow"""
        flow = detector.detect_flow("REPORT", "SEMANTICS")
        assert flow.status == FlowStatus.FORBIDDEN


# ============================================================
# Requirement 14.9: Meaning follows authority chain
# ============================================================

class TestMeaningCreationChain:
    """Test that meaning creation follows the authority chain"""

    def test_valid_meaning_chain(self, detector):
        """Valid meaning chain: raw signals → semantic → reasoning → report"""
        result = detector.validate_flow_path(
            ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]
        )
        assert not result.has_violations()
        assert result.allowed_count == 3

    def test_partial_valid_chain(self, detector):
        """Partial chain SIGNALS → SEMANTICS is valid"""
        result = detector.validate_flow_path(["SIGNALS", "SEMANTICS"])
        assert not result.has_violations()
        assert result.allowed_count == 1

    def test_skipping_semantics_forbidden(self, detector):
        """Skipping SEMANTICS in the chain is forbidden"""
        result = detector.validate_flow_path(["SIGNALS", "REASONING", "REPORT"])
        assert result.has_violations()
        assert result.forbidden_count >= 1


# ============================================================
# Requirement 14.10: Domain cannot create meaning outside authority
# ============================================================

class TestMeaningOutsideAuthority:
    """Test that domains cannot create meaning outside their authority"""

    def test_surface_domain_to_core_forbidden(self, detector):
        """Surface domain cannot create meaning in core domain"""
        # DATA trying to create semantic meaning
        flow = detector.detect_flow("DATA", "SEMANTICS")
        assert flow.status == FlowStatus.FORBIDDEN
        assert "14.10" in flow.reason or "meaning" in flow.reason.lower()

    def test_deploy_to_reasoning_forbidden(self, detector):
        """DEPLOY cannot create reasoning objects"""
        flow = detector.detect_flow("DEPLOY", "REASONING")
        assert flow.status == FlowStatus.FORBIDDEN

    def test_memory_to_signals_forbidden(self, detector):
        """MEMORY cannot create signals"""
        flow = detector.detect_flow("MEMORY", "SIGNALS")
        assert flow.status == FlowStatus.FORBIDDEN

    def test_state_to_report_forbidden(self, detector):
        """STATE cannot create report content"""
        flow = detector.detect_flow("STATE", "REPORT")
        assert flow.status == FlowStatus.FORBIDDEN



# ============================================================
# Flow Detection from Dependencies
# ============================================================

class TestFlowDetectionFromDependencies:
    """Test flow detection based on artifact dependencies"""

    def test_valid_dependencies(self, detector):
        """Artifact with valid dependency chain produces no violations"""
        dependencies = [
            {"artifact_id": "signal-output-1", "domain": "SIGNALS"},
        ]
        result = detector.detect_flows_from_dependencies(
            artifact_id="semantic-state-1",
            artifact_domain="SEMANTICS",
            dependencies=dependencies,
        )
        assert not result.has_violations()
        assert result.allowed_count == 1

    def test_forbidden_dependency(self, detector):
        """Artifact depending on wrong domain produces violation"""
        dependencies = [
            {"artifact_id": "signal-output-1", "domain": "SIGNALS"},
        ]
        result = detector.detect_flows_from_dependencies(
            artifact_id="report-1",
            artifact_domain="REPORT",
            dependencies=dependencies,
        )
        assert result.has_violations()
        assert result.forbidden_count == 1

    def test_multiple_dependencies_mixed(self, detector):
        """Multiple dependencies with mixed validity"""
        dependencies = [
            {"artifact_id": "reasoning-1", "domain": "REASONING"},  # Valid for REPORT
            {"artifact_id": "signal-1", "domain": "SIGNALS"},  # Invalid for REPORT
        ]
        result = detector.detect_flows_from_dependencies(
            artifact_id="report-1",
            artifact_domain="REPORT",
            dependencies=dependencies,
        )
        assert result.allowed_count == 1
        assert result.forbidden_count == 1

    def test_empty_dependencies(self, detector):
        """Empty dependencies produce no flows"""
        result = detector.detect_flows_from_dependencies(
            artifact_id="test-1",
            artifact_domain="REPORT",
            dependencies=[],
        )
        assert result.allowed_count == 0
        assert result.forbidden_count == 0
        assert not result.has_violations()

    def test_missing_domain_in_dependency(self, detector):
        """Dependencies without domain field are skipped"""
        dependencies = [
            {"artifact_id": "unknown-1"},  # No domain field
        ]
        result = detector.detect_flows_from_dependencies(
            artifact_id="test-1",
            artifact_domain="REPORT",
            dependencies=dependencies,
        )
        assert len(result.flows) == 0


# ============================================================
# Authority Chain Visualization
# ============================================================

class TestAuthorityChainVisualization:
    """Test authority chain visualization"""

    def test_valid_chain_visualization(self, detector):
        """Valid chain shows all steps with correct levels"""
        viz = detector.visualize_authority_chain(
            ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]
        )
        assert viz.is_valid
        assert len(viz.chain) == 4
        assert viz.chain[0].authority_level == 1
        assert viz.chain[1].authority_level == 2
        assert viz.chain[2].authority_level == 3
        assert viz.chain[3].authority_level == 4
        assert len(viz.violations) == 0

    def test_invalid_chain_visualization(self, detector):
        """Invalid chain shows violations"""
        viz = detector.visualize_authority_chain(
            ["SIGNALS", "REPORT"]  # Skips SEMANTICS and REASONING
        )
        assert not viz.is_valid
        assert len(viz.violations) > 0
        assert "Skipped" in viz.violations[0]

    def test_backward_chain_visualization(self, detector):
        """Backward chain shows backward flow violation"""
        viz = detector.visualize_authority_chain(
            ["REPORT", "SIGNALS"]
        )
        assert not viz.is_valid
        assert "Backward" in viz.violations[0]

    def test_surface_to_core_visualization(self, detector):
        """Surface domain in chain shows violation"""
        viz = detector.visualize_authority_chain(
            ["USER", "SEMANTICS"]
        )
        assert not viz.is_valid
        assert "Surface" in viz.violations[0] or "meaning" in viz.violations[0].lower()

    def test_ascii_render_valid(self, detector):
        """ASCII render shows valid chain"""
        viz = detector.visualize_authority_chain(
            ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]
        )
        rendered = viz.render_ascii()
        assert "SIGNALS" in rendered
        assert "REPORT" in rendered
        assert "VALID" in rendered
        assert "→" in rendered

    def test_ascii_render_invalid(self, detector):
        """ASCII render shows invalid chain with violations"""
        viz = detector.visualize_authority_chain(
            ["SIGNALS", "REPORT"]
        )
        rendered = viz.render_ascii()
        assert "INVALID" in rendered
        assert "Violations" in rendered

    def test_empty_chain_visualization(self, detector):
        """Empty chain renders gracefully"""
        viz = detector.visualize_authority_chain([])
        assert viz.is_valid  # No violations possible in empty chain
        rendered = viz.render_ascii()
        assert "empty" in rendered.lower()


# ============================================================
# Flow Definition Queries
# ============================================================

class TestFlowDefinitions:
    """Test querying allowed and forbidden flow definitions"""

    def test_get_allowed_flows(self, detector):
        """Returns all defined allowed flows"""
        allowed = detector.get_allowed_flow_definitions()
        assert len(allowed) == 3  # 3 steps in the chain
        sources = [f["source"] for f in allowed]
        assert "SIGNALS" in sources
        assert "SEMANTICS" in sources
        assert "REASONING" in sources

    def test_get_forbidden_flows(self, detector):
        """Returns all defined forbidden flows"""
        forbidden = detector.get_forbidden_flow_definitions()
        assert len(forbidden) > 0
        # Check Signal → Report is in forbidden list
        signal_report = [
            f for f in forbidden
            if f["source"] == "SIGNALS" and f["target"] == "REPORT"
        ]
        assert len(signal_report) == 1

    def test_forbidden_flows_have_reasons(self, detector):
        """All forbidden flows have reasons"""
        forbidden = detector.get_forbidden_flow_definitions()
        for f in forbidden:
            assert f["reason"], f"Missing reason for {f['source']} → {f['target']}"


# ============================================================
# Flow Path Validation
# ============================================================

class TestFlowPathValidation:
    """Test multi-step flow path validation"""

    def test_single_domain_path(self, detector):
        """Single domain path produces no flows"""
        result = detector.validate_flow_path(["SIGNALS"])
        assert result.allowed_count == 0
        assert result.forbidden_count == 0

    def test_two_step_valid_path(self, detector):
        """Two-step valid path"""
        result = detector.validate_flow_path(["SIGNALS", "SEMANTICS"])
        assert result.allowed_count == 1
        assert result.forbidden_count == 0

    def test_invalid_path_with_skip(self, detector):
        """Path that skips a level is invalid"""
        result = detector.validate_flow_path(["SIGNALS", "REASONING"])
        assert result.has_violations()

    def test_execution_time_tracked(self, detector):
        """Execution time is tracked"""
        result = detector.validate_flow_path(
            ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]
        )
        assert result.execution_time_ms >= 0


# ============================================================
# FlowDetectionResult Methods
# ============================================================

class TestFlowDetectionResult:
    """Test FlowDetectionResult helper methods"""

    def test_get_forbidden_flows(self, detector):
        """get_forbidden_flows returns only forbidden flows"""
        result = detector.validate_flow_path(
            ["SIGNALS", "REASONING", "REPORT"]  # First step forbidden
        )
        forbidden = result.get_forbidden_flows()
        assert all(f.status == FlowStatus.FORBIDDEN for f in forbidden)

    def test_get_allowed_flows(self, detector):
        """get_allowed_flows returns only allowed flows"""
        result = detector.validate_flow_path(
            ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]
        )
        allowed = result.get_allowed_flows()
        assert all(f.status == FlowStatus.ALLOWED for f in allowed)
        assert len(allowed) == 3
