"""
Integration tests for report-first detection in observers and health reports.

Tests the integration of ReportValueDetector with:
- Observer 4 (BoundaryAwarenessValidator) check_report_value() method
- Health Reporter report-value health score section
- Infrastructure drift detection
- Warning generation (no blocking)

Requirements: 12.1, 12.2, 12.8, 12.9, 12.10
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path

from observer_boundary_awareness import BoundaryAwarenessValidator
from health_reporter import HealthReporter
from report_value_detector import (
    ReportValueDetector,
    ReportValueAssessment,
    ReportValueHealthScore,
    ALLOWED_REPORT_VALUE_CATEGORIES,
)
from validation_result import ValidationWarning, WarningCodes


# --- Fixtures ---


class MockArtifact:
    """Mock artifact object for testing"""

    def __init__(self, artifact_id, file_path, primary_domain, artifact_type,
                 lifecycle_status="active", report_value=None, description=None):
        self.artifact_id = artifact_id
        self.file_path = file_path
        self.primary_domain = primary_domain
        self.artifact_type = artifact_type
        self.lifecycle_status = lifecycle_status
        self.report_value = report_value
        self.description = description

    def can_write(self, domain_id):
        return True


@pytest.fixture
def mock_artifact_registry():
    """Create a mock artifact registry"""
    registry = MagicMock()
    registry._loaded = True
    return registry


@pytest.fixture
def mock_domain_registry():
    """Create a mock domain registry"""
    registry = MagicMock()
    registry._loaded = True
    return registry


@pytest.fixture
def boundary_validator(mock_artifact_registry, mock_domain_registry):
    """Create a BoundaryAwarenessValidator instance with mocked registries"""
    return BoundaryAwarenessValidator(mock_artifact_registry, mock_domain_registry)


@pytest.fixture
def artifacts_with_report_value():
    """Artifacts that have valid report value"""
    return [
        MockArtifact(
            artifact_id="report_engine_py",
            file_path="engines/report_engine.py",
            primary_domain="REPORT",
            artifact_type="ENGINE",
            report_value={"category": "pm_reasoning", "justification": "Generates PM reasoning section"},
        ),
        MockArtifact(
            artifact_id="semantic_engine_py",
            file_path="engines/semantic_engine.py",
            primary_domain="SEMANTICS",
            artifact_type="ENGINE",
            report_value={"category": "semantic_interpretation", "justification": "Produces semantic state for report"},
        ),
    ]


@pytest.fixture
def artifacts_without_report_value():
    """Artifacts that lack report value"""
    return [
        MockArtifact(
            artifact_id="deploy_config_yaml",
            file_path="deploy/config.yaml",
            primary_domain="DEPLOY",
            artifact_type="CONFIG",
        ),
        MockArtifact(
            artifact_id="ci_pipeline_yaml",
            file_path="ci/pipeline.yaml",
            primary_domain="DEPLOY",
            artifact_type="CONFIG",
            description="CI/CD pipeline configuration",
        ),
    ]


@pytest.fixture
def artifacts_mixed():
    """Mix of artifacts with and without report value"""
    return [
        # Valid report value
        MockArtifact(
            artifact_id="report_engine_py",
            file_path="engines/report_engine.py",
            primary_domain="REPORT",
            artifact_type="ENGINE",
            report_value={"category": "pm_reasoning", "justification": "Generates PM reasoning"},
        ),
        # Missing report value (infrastructure)
        MockArtifact(
            artifact_id="deploy_script_sh",
            file_path="deploy/run.sh",
            primary_domain="DEPLOY",
            artifact_type="RUNTIME",
        ),
        # Speculative report value
        MockArtifact(
            artifact_id="cache_layer_py",
            file_path="src/cache_layer.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            report_value={"category": "traceability", "justification": "Might improve report speed in the future"},
        ),
        # Valid report value (non-infrastructure)
        MockArtifact(
            artifact_id="signal_engine_py",
            file_path="engines/signal_engine.py",
            primary_domain="SIGNALS",
            artifact_type="ENGINE",
            report_value={"category": "confidence_explanation", "justification": "Generates confidence signals for report"},
        ),
        # Missing report value (non-infrastructure)
        MockArtifact(
            artifact_id="data_loader_py",
            file_path="src/data_loader.py",
            primary_domain="DATA",
            artifact_type="ENGINE",
        ),
    ]


# --- Observer 4 Integration Tests: check_report_value ---


class TestBoundaryValidatorReportValueIntegration:
    """Test report value detection integrated into Observer 4"""

    def test_check_report_value_with_valid_artifacts(self, boundary_validator, artifacts_with_report_value):
        """
        Requirement 12.1: Artifacts with valid report value generate no warnings.
        """
        # Convert mock artifacts to dicts for the detector
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts_with_report_value]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # No missing report value warnings for valid artifacts
        missing_warnings = [w for w in warnings if w.warning_code == WarningCodes.W600_MISSING_REPORT_VALUE]
        assert len(missing_warnings) == 0

    def test_check_report_value_missing_generates_warning(self, boundary_validator, artifacts_without_report_value):
        """
        Requirement 12.2: Artifacts without report value generate warnings.
        """
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts_without_report_value]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # Should have missing report value warnings
        missing_warnings = [w for w in warnings if w.warning_code == WarningCodes.W600_MISSING_REPORT_VALUE]
        assert len(missing_warnings) == 2

        # Warnings should be severity "low" (not blocking)
        for w in missing_warnings:
            assert w.severity == "low"

    def test_check_report_value_infrastructure_drift_warning(self, boundary_validator, artifacts_without_report_value):
        """
        Requirement 12.8: Infrastructure-heavy artifacts without report value
        generate infrastructure drift warnings.
        """
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts_without_report_value]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # Should have infrastructure drift warnings
        infra_warnings = [w for w in warnings if w.warning_code == WarningCodes.W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE]
        assert len(infra_warnings) == 2  # Both are DEPLOY/CONFIG (infrastructure)

        # Warnings should be severity "medium"
        for w in infra_warnings:
            assert w.severity == "medium"

    def test_check_report_value_speculative_warning(self, boundary_validator):
        """
        Requirement 12.10: Speculative report value generates warning.
        Report value must be direct and measurable.
        """
        speculative_artifact = MockArtifact(
            artifact_id="cache_py",
            file_path="src/cache.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            report_value={"category": "traceability", "justification": "Could help with report speed eventually"},
        )
        artifact_dicts = [boundary_validator._artifact_to_dict(speculative_artifact)]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        speculative_warnings = [w for w in warnings if w.warning_code == WarningCodes.W602_SPECULATIVE_REPORT_VALUE]
        assert len(speculative_warnings) == 1
        assert speculative_warnings[0].severity == "medium"

    def test_check_report_value_invalid_category_warning(self, boundary_validator):
        """
        Requirement 12.10: Invalid report value category generates warning.
        """
        invalid_artifact = MockArtifact(
            artifact_id="monitoring_py",
            file_path="src/monitoring.py",
            primary_domain="DEPLOY",
            artifact_type="RUNTIME",
            report_value={"category": "performance_optimization", "justification": "Improves speed"},
        )
        artifact_dicts = [boundary_validator._artifact_to_dict(invalid_artifact)]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        category_warnings = [w for w in warnings if w.warning_code == WarningCodes.W601_INVALID_REPORT_VALUE_CATEGORY]
        assert len(category_warnings) == 1
        assert "performance_optimization" in category_warnings[0].warning_message

    def test_check_report_value_never_blocks(self, boundary_validator, artifacts_mixed):
        """
        All report value detection operates in WARNING mode only (no blocking).
        Warnings are informational, never prevent commits.
        """
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts_mixed]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # All warnings should have severity "low" or "medium" (never "critical" or blocking)
        for w in warnings:
            assert w.severity in ("low", "medium")
            assert w.observer_name == "BoundaryAwarenessValidator"

    def test_check_report_value_loads_from_registry_when_none(self, boundary_validator, mock_artifact_registry):
        """
        When artifacts=None, check_report_value loads from registry.
        """
        mock_artifact_registry.list_all_artifacts.return_value = [
            MockArtifact(
                artifact_id="test_artifact",
                file_path="test.py",
                primary_domain="DATA",
                artifact_type="ENGINE",
            )
        ]
        warnings = boundary_validator.check_report_value(artifacts=None)

        # Should have loaded from registry
        mock_artifact_registry.list_all_artifacts.assert_called_once()
        # Should have at least a missing report value warning
        assert len(warnings) >= 1

    def test_check_report_value_governance_without_report_quality(self, boundary_validator):
        """
        Requirement 12.9: Governance features without report quality benefit
        should be flagged as infrastructure-heavy.
        """
        gov_artifact = MockArtifact(
            artifact_id="governance_validator_py",
            file_path="src/governance/validator.py",
            primary_domain="ARCH",
            artifact_type="STEERING",
            description="Governance validation framework",
        )
        artifact_dicts = [boundary_validator._artifact_to_dict(gov_artifact)]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # ARCH domain + STEERING type = infrastructure-heavy
        infra_warnings = [w for w in warnings if w.warning_code == WarningCodes.W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE]
        assert len(infra_warnings) == 1


# --- Health Reporter Integration Tests ---


class TestHealthReporterReportValueIntegration:
    """Test report-value health score in health reports"""

    def test_get_report_value_health_score_returns_dict(self, mock_artifact_registry, mock_domain_registry):
        """
        Health reporter returns report-value health score as dictionary.
        """
        mock_artifact_registry.list_all_artifacts.return_value = [
            MockArtifact(
                artifact_id="report_engine",
                file_path="engines/report_engine.py",
                primary_domain="REPORT",
                artifact_type="ENGINE",
                report_value={"category": "pm_reasoning", "justification": "Generates PM reasoning"},
            ),
            MockArtifact(
                artifact_id="deploy_config",
                file_path="deploy/config.yaml",
                primary_domain="DEPLOY",
                artifact_type="CONFIG",
            ),
        ]

        reporter = HealthReporter(
            artifact_registry=mock_artifact_registry,
            domain_registry=mock_domain_registry,
        )
        score = reporter.get_report_value_health_score()

        assert isinstance(score, dict)
        assert score['total_artifacts'] == 2
        assert score['artifacts_with_report_value'] == 1
        assert score['artifacts_with_valid_report_value'] == 1
        assert score['artifacts_missing_report_value'] == 1
        assert score['coverage_percentage'] == 50.0
        assert score['valid_percentage'] == 50.0

    def test_health_score_infrastructure_drift_tracked(self, mock_artifact_registry, mock_domain_registry):
        """
        Requirement 12.8: Infrastructure drift percentage is tracked in health reports.
        """
        mock_artifact_registry.list_all_artifacts.return_value = [
            MockArtifact(
                artifact_id="deploy_1",
                file_path="deploy/run.sh",
                primary_domain="DEPLOY",
                artifact_type="RUNTIME",
            ),
            MockArtifact(
                artifact_id="deploy_2",
                file_path="deploy/config.yaml",
                primary_domain="DEPLOY",
                artifact_type="CONFIG",
            ),
            MockArtifact(
                artifact_id="report_1",
                file_path="engines/report.py",
                primary_domain="REPORT",
                artifact_type="ENGINE",
                report_value={"category": "pm_reasoning", "justification": "Direct report generation"},
            ),
        ]

        reporter = HealthReporter(
            artifact_registry=mock_artifact_registry,
            domain_registry=mock_domain_registry,
        )
        score = reporter.get_report_value_health_score()

        # 2 out of 3 are infrastructure-heavy without report value
        assert score['artifacts_infrastructure_heavy'] == 2
        assert abs(score['infrastructure_drift_percentage'] - 66.7) < 0.1

    def test_health_score_category_distribution(self, mock_artifact_registry, mock_domain_registry):
        """
        Health score tracks category distribution across artifacts.
        """
        mock_artifact_registry.list_all_artifacts.return_value = [
            MockArtifact(
                artifact_id="a1",
                file_path="a1.py",
                primary_domain="REPORT",
                artifact_type="ENGINE",
                report_value={"category": "pm_reasoning", "justification": "Direct"},
            ),
            MockArtifact(
                artifact_id="a2",
                file_path="a2.py",
                primary_domain="REPORT",
                artifact_type="ENGINE",
                report_value={"category": "pm_reasoning", "justification": "Direct"},
            ),
            MockArtifact(
                artifact_id="a3",
                file_path="a3.py",
                primary_domain="SIGNALS",
                artifact_type="ENGINE",
                report_value={"category": "confidence_explanation", "justification": "Direct"},
            ),
        ]

        reporter = HealthReporter(
            artifact_registry=mock_artifact_registry,
            domain_registry=mock_domain_registry,
        )
        score = reporter.get_report_value_health_score()

        assert score['category_distribution']['pm_reasoning'] == 2
        assert score['category_distribution']['confidence_explanation'] == 1

    def test_health_score_empty_registry(self, mock_artifact_registry, mock_domain_registry):
        """
        Health score handles empty registry gracefully.
        """
        mock_artifact_registry.list_all_artifacts.return_value = []

        reporter = HealthReporter(
            artifact_registry=mock_artifact_registry,
            domain_registry=mock_domain_registry,
        )
        score = reporter.get_report_value_health_score()

        assert score['total_artifacts'] == 0
        assert score['coverage_percentage'] == 0.0
        assert score['valid_percentage'] == 0.0
        assert score['infrastructure_drift_percentage'] == 0.0


# --- Report Text Formatting Integration Tests ---


class TestHealthReportTextFormatting:
    """Test that report-value health score appears in formatted text reports"""

    def test_format_report_includes_report_value_section(self, mock_artifact_registry, mock_domain_registry):
        """
        Formatted text report includes REPORT-VALUE HEALTH SCORE section.
        """
        reporter = HealthReporter(
            artifact_registry=mock_artifact_registry,
            domain_registry=mock_domain_registry,
        )

        # Build a minimal report dict with report_value_health
        report = {
            'report_date': '2025-01-15',
            'report_time': '10:00:00',
            'report_version': '1.0',
            'enforcement_mode': 'observability',
            'summary': {
                'total_artifacts': 5,
                'registered_artifacts': 5,
                'registration_percentage': 100.0,
                'total_domains': 12,
                'domains_with_artifacts': 4,
                'report_value_valid_percentage': 60.0,
                'infrastructure_drift_percentage': 20.0,
            },
            'domain_coverage': [],
            'lifecycle_distribution': [],
            'report_value_health': {
                'total_artifacts': 5,
                'artifacts_with_report_value': 3,
                'artifacts_with_valid_report_value': 3,
                'artifacts_speculative': 0,
                'artifacts_infrastructure_heavy': 1,
                'artifacts_missing_report_value': 2,
                'coverage_percentage': 60.0,
                'valid_percentage': 60.0,
                'infrastructure_drift_percentage': 20.0,
                'category_distribution': {'pm_reasoning': 2, 'traceability': 1},
            },
        }

        text = reporter.format_report_text(report)

        assert "REPORT-VALUE HEALTH SCORE" in text
        assert "Coverage Percentage:" in text
        assert "Valid Percentage:" in text
        assert "Infrastructure Drift:" in text
        assert "60.0%" in text
        assert "20.0%" in text
        assert "pm_reasoning: 2" in text
        assert "traceability: 1" in text

    def test_format_report_without_report_value_section(self, mock_artifact_registry, mock_domain_registry):
        """
        Formatted text report handles missing report_value_health gracefully.
        """
        reporter = HealthReporter(
            artifact_registry=mock_artifact_registry,
            domain_registry=mock_domain_registry,
        )

        # Report without report_value_health key
        report = {
            'report_date': '2025-01-15',
            'report_time': '10:00:00',
            'report_version': '1.0',
            'enforcement_mode': 'observability',
            'summary': {
                'total_artifacts': 0,
                'registered_artifacts': 0,
                'registration_percentage': 0.0,
                'total_domains': 12,
                'domains_with_artifacts': 0,
            },
            'domain_coverage': [],
            'lifecycle_distribution': [],
        }

        text = reporter.format_report_text(report)

        # Should not crash, just skip the section
        assert "REPORT-VALUE HEALTH SCORE" not in text
        assert "DOMAINIZATION HEALTH REPORT" in text


# --- End-to-End Integration Tests ---


class TestReportFirstDetectionEndToEnd:
    """End-to-end integration tests for report-first detection flow"""

    def test_full_flow_mixed_artifacts(self, boundary_validator, artifacts_mixed):
        """
        End-to-end: Mixed artifacts produce correct warnings and health score.
        """
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts_mixed]

        # Get warnings
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # Get health score
        health_score = boundary_validator.get_report_value_health_score(artifact_dicts)

        # Verify health score metrics
        assert health_score.total_artifacts == 5
        assert health_score.artifacts_with_report_value == 3  # report_engine, cache_layer, signal_engine
        assert health_score.artifacts_with_valid_report_value == 2  # report_engine, signal_engine
        assert health_score.artifacts_speculative == 1  # cache_layer
        assert health_score.artifacts_missing_report_value == 2  # deploy_script, data_loader

        # Verify warnings generated
        missing_warnings = [w for w in warnings if w.warning_code == WarningCodes.W600_MISSING_REPORT_VALUE]
        assert len(missing_warnings) == 2

        infra_warnings = [w for w in warnings if w.warning_code == WarningCodes.W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE]
        # deploy_script (DEPLOY/RUNTIME) and cache_layer (ARCH/ENGINE with speculative value)
        assert len(infra_warnings) >= 1

        speculative_warnings = [w for w in warnings if w.warning_code == WarningCodes.W602_SPECULATIVE_REPORT_VALUE]
        assert len(speculative_warnings) == 1

    def test_report_value_precedence_over_architecture(self, boundary_validator):
        """
        Requirement 12.10: Report value takes precedence over architectural elegance.
        Architecture-focused artifacts without report value get flagged.
        """
        arch_artifacts = [
            MockArtifact(
                artifact_id="arch_refactor",
                file_path="src/architecture/refactor.py",
                primary_domain="ARCH",
                artifact_type="ENGINE",
                description="Architectural refactoring for elegance",
            ),
            MockArtifact(
                artifact_id="report_improvement",
                file_path="engines/report_improvement.py",
                primary_domain="REPORT",
                artifact_type="ENGINE",
                report_value={"category": "user_understanding", "justification": "Improves report clarity for PM"},
            ),
        ]
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in arch_artifacts]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # Architecture artifact without report value should be flagged
        infra_warnings = [w for w in warnings if w.warning_code == WarningCodes.W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE]
        assert len(infra_warnings) == 1
        assert infra_warnings[0].artifact_id == "arch_refactor"

        # Report improvement should NOT be flagged
        assert all(w.artifact_id != "report_improvement" for w in warnings
                   if w.warning_code == WarningCodes.W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE)

    def test_infrastructure_drift_percentage_calculation(self, boundary_validator):
        """
        Requirement 12.8: Infrastructure drift percentage correctly calculated.
        """
        artifacts = [
            MockArtifact("a1", "deploy/a.sh", "DEPLOY", "RUNTIME"),
            MockArtifact("a2", "deploy/b.sh", "DEPLOY", "RUNTIME"),
            MockArtifact("a3", "engines/report.py", "REPORT", "ENGINE",
                         report_value={"category": "pm_reasoning", "justification": "Direct"}),
            MockArtifact("a4", "engines/signal.py", "SIGNALS", "ENGINE",
                         report_value={"category": "confidence_explanation", "justification": "Direct"}),
            MockArtifact("a5", "src/data.py", "DATA", "ENGINE"),
        ]
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts]
        health_score = boundary_validator.get_report_value_health_score(artifact_dicts)

        # 2 infrastructure-heavy without report value out of 5 total = 40%
        assert health_score.infrastructure_drift_percentage == 40.0

    def test_all_warnings_are_non_blocking(self, boundary_validator, artifacts_mixed):
        """
        All report-first detection operates in WARNING mode only.
        No warnings should have severity that would block commits.
        """
        artifact_dicts = [boundary_validator._artifact_to_dict(a) for a in artifacts_mixed]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        # No critical or blocking warnings
        for w in warnings:
            assert w.severity in ("low", "medium"), (
                f"Warning {w.warning_code} has severity '{w.severity}' which may block. "
                f"Report-first detection must be WARNING mode only."
            )

    def test_warning_messages_are_actionable(self, boundary_validator):
        """
        Requirement 15.4: All warnings provide actionable suggestions.
        """
        artifact = MockArtifact(
            artifact_id="test_artifact",
            file_path="test.py",
            primary_domain="DEPLOY",
            artifact_type="CONFIG",
        )
        artifact_dicts = [boundary_validator._artifact_to_dict(artifact)]
        warnings = boundary_validator.check_report_value(artifact_dicts)

        for w in warnings:
            assert w.suggestion, f"Warning {w.warning_code} has no suggestion"
            assert len(w.suggestion) > 10, f"Warning {w.warning_code} suggestion too short"
            assert w.warning_message, f"Warning {w.warning_code} has no message"
