"""
Unit tests for Report Value Detection Framework

Tests report value category validation, speculative claim detection,
infrastructure-heavy artifact detection, and health score generation.

Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7
"""

import pytest
from report_value_detector import (
    ReportValueDetector,
    ReportValueAssessment,
    ReportValueHealthScore,
    ALLOWED_REPORT_VALUE_CATEGORIES,
    SPECULATIVE_KEYWORDS,
    INFRASTRUCTURE_KEYWORDS,
)


class TestAllowedCategories:
    """Test the 10 allowed report value categories (Requirement 12.5)"""

    def test_exactly_10_categories_defined(self):
        """Requirement 12.5: There shall be exactly 10 allowed categories"""
        assert len(ALLOWED_REPORT_VALUE_CATEGORIES) == 10

    def test_semantic_interpretation_in_categories(self):
        """Requirement 12.5: semantic_interpretation is an allowed category"""
        assert "semantic_interpretation" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_pm_reasoning_in_categories(self):
        """Requirement 12.5: pm_reasoning is an allowed category"""
        assert "pm_reasoning" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_concentration_explanation_in_categories(self):
        """Requirement 12.5: concentration_explanation is an allowed category"""
        assert "concentration_explanation" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_dependency_explanation_in_categories(self):
        """Requirement 12.5: dependency_explanation is an allowed category"""
        assert "dependency_explanation" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_scenario_interpretation_in_categories(self):
        """Requirement 12.5: scenario_interpretation is an allowed category"""
        assert "scenario_interpretation" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_confidence_explanation_in_categories(self):
        """Requirement 12.5: confidence_explanation is an allowed category"""
        assert "confidence_explanation" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_action_space_clarity_in_categories(self):
        """Requirement 12.5: action_space_clarity is an allowed category"""
        assert "action_space_clarity" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_multilingual_rendering_in_categories(self):
        """Requirement 12.5: multilingual_rendering is an allowed category"""
        assert "multilingual_rendering" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_traceability_in_categories(self):
        """Requirement 12.5: traceability is an allowed category"""
        assert "traceability" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_user_understanding_in_categories(self):
        """Requirement 12.5: user_understanding is an allowed category"""
        assert "user_understanding" in ALLOWED_REPORT_VALUE_CATEGORIES

    def test_get_allowed_categories_returns_all(self):
        """Test that detector returns all 10 categories"""
        detector = ReportValueDetector()
        categories = detector.get_allowed_categories()
        assert len(categories) == 10
        assert set(categories) == set(ALLOWED_REPORT_VALUE_CATEGORIES)


class TestReportValueDetector:
    """Test suite for ReportValueDetector class"""

    @pytest.fixture
    def detector(self):
        """Create a ReportValueDetector instance"""
        return ReportValueDetector()

    @pytest.fixture
    def valid_artifact(self):
        """Artifact with valid report value"""
        return {
            "artifact_id": "report_engine_py",
            "file_path": "engines/report_engine.py",
            "primary_domain": "REPORT",
            "artifact_type": "ENGINE",
            "report_value": {
                "category": "pm_reasoning",
                "justification": "Generates PM reasoning section in the portfolio report",
            },
        }

    @pytest.fixture
    def artifact_no_report_value(self):
        """Artifact without report value field"""
        return {
            "artifact_id": "deploy_config_yaml",
            "file_path": "deploy/config.yaml",
            "primary_domain": "DEPLOY",
            "artifact_type": "CONFIG",
        }

    @pytest.fixture
    def artifact_speculative(self):
        """Artifact with speculative report value"""
        return {
            "artifact_id": "cache_layer_py",
            "file_path": "src/cache_layer.py",
            "primary_domain": "ARCH",
            "artifact_type": "ENGINE",
            "report_value": {
                "category": "traceability",
                "justification": "This might improve report generation speed in the future",
            },
        }

    @pytest.fixture
    def artifact_invalid_category(self):
        """Artifact with invalid report value category"""
        return {
            "artifact_id": "monitoring_py",
            "file_path": "src/monitoring.py",
            "primary_domain": "DEPLOY",
            "artifact_type": "RUNTIME",
            "report_value": {
                "category": "performance_optimization",
                "justification": "Improves system performance",
            },
        }

    # --- assess_artifact Tests ---

    def test_assess_valid_report_value(self, detector, valid_artifact):
        """Requirement 12.1: Feature answers 'How does this improve the report?'"""
        assessment = detector.assess_artifact(valid_artifact)
        assert assessment.has_report_value is True
        assert assessment.is_valid is True
        assert assessment.report_value_category == "pm_reasoning"
        assert assessment.is_speculative is False
        assert len(assessment.issues) == 0

    def test_assess_missing_report_value(self, detector, artifact_no_report_value):
        """Requirement 12.2: No report value identified"""
        assessment = detector.assess_artifact(artifact_no_report_value)
        assert assessment.has_report_value is False
        assert assessment.is_valid is False
        assert "No report_value field" in assessment.issues[0]

    def test_assess_speculative_report_value(self, detector, artifact_speculative):
        """Requirement 12.4: Speculative report value detected"""
        assessment = detector.assess_artifact(artifact_speculative)
        assert assessment.has_report_value is True
        assert assessment.is_speculative is True
        assert assessment.is_valid is False

    def test_assess_invalid_category(self, detector, artifact_invalid_category):
        """Requirement 12.5: Invalid category not in allowed list"""
        assessment = detector.assess_artifact(artifact_invalid_category)
        assert assessment.has_report_value is True
        assert assessment.is_valid is False
        assert any("not in allowed" in issue for issue in assessment.issues)

    def test_assess_string_report_value(self, detector):
        """Test report_value as simple string (treated as category)"""
        artifact = {
            "artifact_id": "test_artifact",
            "file_path": "test.py",
            "primary_domain": "REPORT",
            "artifact_type": "ENGINE",
            "report_value": "semantic_interpretation",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.has_report_value is True
        assert assessment.report_value_category == "semantic_interpretation"
        assert assessment.is_valid is True

    def test_assess_invalid_report_value_format(self, detector):
        """Test report_value with invalid format (not dict or string)"""
        artifact = {
            "artifact_id": "test_artifact",
            "file_path": "test.py",
            "primary_domain": "REPORT",
            "artifact_type": "ENGINE",
            "report_value": 42,
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.has_report_value is False
        assert any("invalid format" in issue for issue in assessment.issues)

    def test_assess_empty_report_value_dict(self, detector):
        """Test report_value with empty dict"""
        artifact = {
            "artifact_id": "test_artifact",
            "file_path": "test.py",
            "primary_domain": "REPORT",
            "artifact_type": "ENGINE",
            "report_value": {},
        }
        # Empty dict has no category, so it won't match allowed categories
        assessment = detector.assess_artifact(artifact)
        assert assessment.has_report_value is True
        assert assessment.is_valid is False

    def test_assess_all_valid_categories(self, detector):
        """Test that all 10 allowed categories pass validation"""
        for category in ALLOWED_REPORT_VALUE_CATEGORIES:
            artifact = {
                "artifact_id": f"test_{category}",
                "file_path": "test.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {
                    "category": category,
                    "justification": "Directly improves report quality",
                },
            }
            assessment = detector.assess_artifact(artifact)
            assert assessment.is_valid is True, f"Category '{category}' should be valid"


class TestSpeculativeDetection:
    """Test speculative/indirect report value detection (Requirement 12.4)"""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    def test_detect_might_improve(self, detector):
        """Detect 'might improve' as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "traceability",
                "justification": "This might improve report clarity",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True

    def test_detect_could_help(self, detector):
        """Detect 'could help' as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "traceability",
                "justification": "This could help with report generation",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True

    def test_detect_potentially(self, detector):
        """Detect 'potentially' as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "user_understanding",
                "justification": "Potentially enhances user understanding",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True

    def test_detect_in_the_future(self, detector):
        """Detect 'in the future' as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "pm_reasoning",
                "justification": "Will improve PM reasoning in the future",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True

    def test_detect_indirectly(self, detector):
        """Detect 'indirectly' as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "confidence_explanation",
                "justification": "Indirectly supports confidence explanation",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True

    def test_direct_justification_not_speculative(self, detector):
        """Direct justification should not be flagged as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "pm_reasoning",
                "justification": "Generates the PM reasoning paragraph in the daily report",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is False

    def test_empty_justification_not_speculative(self, detector):
        """Empty justification should not be flagged as speculative"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "pm_reasoning",
                "justification": "",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is False

    def test_case_insensitive_speculative_detection(self, detector):
        """Speculative keywords should be detected case-insensitively"""
        artifact = {
            "artifact_id": "test",
            "file_path": "test.py",
            "report_value": {
                "category": "traceability",
                "justification": "MIGHT IMPROVE report quality",
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True


class TestInfrastructureDetection:
    """Test infrastructure-heavy artifact detection (Requirement 12.7)"""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    def test_deploy_domain_is_infrastructure(self, detector):
        """DEPLOY domain artifacts are infrastructure-heavy"""
        artifact = {
            "artifact_id": "deploy_script",
            "file_path": "deploy/run.sh",
            "primary_domain": "DEPLOY",
            "artifact_type": "RUNTIME",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is True

    def test_arch_domain_is_infrastructure(self, detector):
        """ARCH domain artifacts are infrastructure-heavy"""
        artifact = {
            "artifact_id": "arch_doc",
            "file_path": "docs/architecture.md",
            "primary_domain": "ARCH",
            "artifact_type": "SSOT",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is True

    def test_config_type_is_infrastructure(self, detector):
        """CONFIG artifact type is infrastructure-heavy"""
        artifact = {
            "artifact_id": "app_config",
            "file_path": "config/app.yaml",
            "primary_domain": "DATA",
            "artifact_type": "CONFIG",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is True

    def test_runtime_type_is_infrastructure(self, detector):
        """RUNTIME artifact type is infrastructure-heavy"""
        artifact = {
            "artifact_id": "main_runtime",
            "file_path": "main.py",
            "primary_domain": "DATA",
            "artifact_type": "RUNTIME",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is True

    def test_infrastructure_in_file_path(self, detector):
        """File path containing infrastructure keywords is detected"""
        artifact = {
            "artifact_id": "infra_module",
            "file_path": "src/infrastructure/cache.py",
            "primary_domain": "DATA",
            "artifact_type": "ENGINE",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is True

    def test_infrastructure_in_description(self, detector):
        """Description containing infrastructure keywords is detected"""
        artifact = {
            "artifact_id": "scaling_module",
            "file_path": "src/scaler.py",
            "primary_domain": "DATA",
            "artifact_type": "ENGINE",
            "description": "Handles load balancing across services",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is True

    def test_report_domain_not_infrastructure(self, detector):
        """REPORT domain artifacts are not infrastructure-heavy"""
        artifact = {
            "artifact_id": "report_engine",
            "file_path": "engines/report_engine.py",
            "primary_domain": "REPORT",
            "artifact_type": "ENGINE",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is False

    def test_signals_domain_not_infrastructure(self, detector):
        """SIGNALS domain artifacts are not infrastructure-heavy"""
        artifact = {
            "artifact_id": "signal_engine",
            "file_path": "engines/signal_engine.py",
            "primary_domain": "SIGNALS",
            "artifact_type": "ENGINE",
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_infrastructure_heavy is False


class TestHealthScore:
    """Test report-value health score generation"""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    def test_health_score_all_valid(self, detector):
        """Health score with all artifacts having valid report value"""
        artifacts = [
            {
                "artifact_id": f"artifact_{i}",
                "file_path": f"src/artifact_{i}.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {
                    "category": "pm_reasoning",
                    "justification": "Directly generates PM reasoning",
                },
            }
            for i in range(5)
        ]
        score = detector.generate_health_score(artifacts)
        assert score.total_artifacts == 5
        assert score.artifacts_with_report_value == 5
        assert score.artifacts_with_valid_report_value == 5
        assert score.coverage_percentage == 100.0
        assert score.valid_percentage == 100.0
        assert score.artifacts_missing_report_value == 0

    def test_health_score_none_valid(self, detector):
        """Health score with no artifacts having report value"""
        artifacts = [
            {
                "artifact_id": f"artifact_{i}",
                "file_path": f"src/artifact_{i}.py",
                "primary_domain": "DATA",
                "artifact_type": "ENGINE",
            }
            for i in range(3)
        ]
        score = detector.generate_health_score(artifacts)
        assert score.total_artifacts == 3
        assert score.artifacts_with_report_value == 0
        assert score.artifacts_with_valid_report_value == 0
        assert score.coverage_percentage == 0.0
        assert score.valid_percentage == 0.0
        assert score.artifacts_missing_report_value == 3

    def test_health_score_mixed(self, detector):
        """Health score with mixed valid, speculative, and missing"""
        artifacts = [
            # Valid
            {
                "artifact_id": "valid_1",
                "file_path": "src/valid.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {
                    "category": "pm_reasoning",
                    "justification": "Generates PM reasoning",
                },
            },
            # Speculative
            {
                "artifact_id": "speculative_1",
                "file_path": "src/speculative.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {
                    "category": "traceability",
                    "justification": "Might improve traceability in the future",
                },
            },
            # Missing
            {
                "artifact_id": "missing_1",
                "file_path": "src/missing.py",
                "primary_domain": "DATA",
                "artifact_type": "ENGINE",
            },
            # Invalid category
            {
                "artifact_id": "invalid_1",
                "file_path": "src/invalid.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {
                    "category": "not_a_real_category",
                    "justification": "Direct improvement",
                },
            },
        ]
        score = detector.generate_health_score(artifacts)
        assert score.total_artifacts == 4
        assert score.artifacts_with_report_value == 3  # valid + speculative + invalid category
        assert score.artifacts_with_valid_report_value == 1  # only the valid one
        assert score.artifacts_speculative == 1
        assert score.artifacts_missing_report_value == 1
        assert score.valid_percentage == 25.0  # 1/4

    def test_health_score_empty_artifacts(self, detector):
        """Health score with empty artifact list"""
        score = detector.generate_health_score([])
        assert score.total_artifacts == 0
        assert score.coverage_percentage == 0.0
        assert score.valid_percentage == 0.0
        assert score.infrastructure_drift_percentage == 0.0

    def test_health_score_category_distribution(self, detector):
        """Health score tracks category distribution"""
        artifacts = [
            {
                "artifact_id": "a1",
                "file_path": "a1.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {"category": "pm_reasoning", "justification": "Direct"},
            },
            {
                "artifact_id": "a2",
                "file_path": "a2.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {"category": "pm_reasoning", "justification": "Direct"},
            },
            {
                "artifact_id": "a3",
                "file_path": "a3.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {"category": "traceability", "justification": "Direct"},
            },
        ]
        score = detector.generate_health_score(artifacts)
        assert score.category_distribution["pm_reasoning"] == 2
        assert score.category_distribution["traceability"] == 1

    def test_health_score_infrastructure_drift(self, detector):
        """Health score detects infrastructure drift"""
        artifacts = [
            # Infrastructure without report value
            {
                "artifact_id": "deploy_1",
                "file_path": "deploy/script.sh",
                "primary_domain": "DEPLOY",
                "artifact_type": "RUNTIME",
            },
            # Infrastructure with valid report value (not counted as drift)
            {
                "artifact_id": "deploy_2",
                "file_path": "deploy/report_deploy.sh",
                "primary_domain": "DEPLOY",
                "artifact_type": "RUNTIME",
                "report_value": {
                    "category": "multilingual_rendering",
                    "justification": "Deploys multilingual rendering service",
                },
            },
            # Non-infrastructure without report value (not counted as infra drift)
            {
                "artifact_id": "signal_1",
                "file_path": "engines/signal.py",
                "primary_domain": "SIGNALS",
                "artifact_type": "ENGINE",
            },
        ]
        score = detector.generate_health_score(artifacts)
        assert score.artifacts_infrastructure_heavy == 1  # only deploy_1


class TestDetectMissingReportValue:
    """Test detection of artifacts missing report value"""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    def test_detect_missing(self, detector):
        """Requirement 12.2: Identify artifacts without report value"""
        artifacts = [
            {"artifact_id": "a1", "file_path": "a1.py", "report_value": {"category": "pm_reasoning", "justification": "Direct"}},
            {"artifact_id": "a2", "file_path": "a2.py"},
            {"artifact_id": "a3", "file_path": "a3.py", "report_value": None},
        ]
        missing = detector.detect_missing_report_value(artifacts)
        assert len(missing) == 2
        assert missing[0]["artifact_id"] == "a2"
        assert missing[1]["artifact_id"] == "a3"

    def test_detect_none_missing(self, detector):
        """All artifacts have report value"""
        artifacts = [
            {"artifact_id": "a1", "file_path": "a1.py", "report_value": {"category": "pm_reasoning", "justification": "Direct"}},
            {"artifact_id": "a2", "file_path": "a2.py", "report_value": "traceability"},
        ]
        missing = detector.detect_missing_report_value(artifacts)
        assert len(missing) == 0


class TestDetectInfrastructureWithoutReportValue:
    """Test detection of infrastructure-heavy artifacts without report value"""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    def test_detect_infra_without_value(self, detector):
        """Requirement 12.7: Identify infrastructure without report benefit"""
        artifacts = [
            {
                "artifact_id": "deploy_1",
                "file_path": "deploy/config.yaml",
                "primary_domain": "DEPLOY",
                "artifact_type": "CONFIG",
            },
            {
                "artifact_id": "report_1",
                "file_path": "engines/report.py",
                "primary_domain": "REPORT",
                "artifact_type": "ENGINE",
                "report_value": {"category": "pm_reasoning", "justification": "Direct"},
            },
        ]
        infra = detector.detect_infrastructure_without_report_value(artifacts)
        assert len(infra) == 1
        assert infra[0]["artifact_id"] == "deploy_1"

    def test_infra_with_valid_report_value_not_flagged(self, detector):
        """Infrastructure with valid report value should not be flagged"""
        artifacts = [
            {
                "artifact_id": "deploy_1",
                "file_path": "deploy/config.yaml",
                "primary_domain": "DEPLOY",
                "artifact_type": "CONFIG",
                "report_value": {
                    "category": "multilingual_rendering",
                    "justification": "Configures multilingual rendering deployment",
                },
            },
        ]
        infra = detector.detect_infrastructure_without_report_value(artifacts)
        assert len(infra) == 0


class TestIsValidCategory:
    """Test category validation helper"""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    def test_valid_categories(self, detector):
        """All allowed categories should be valid"""
        for category in ALLOWED_REPORT_VALUE_CATEGORIES:
            assert detector.is_valid_category(category) is True

    def test_invalid_category(self, detector):
        """Unknown categories should be invalid"""
        assert detector.is_valid_category("performance_optimization") is False
        assert detector.is_valid_category("code_quality") is False
        assert detector.is_valid_category("") is False

    def test_category_case_insensitive(self, detector):
        """Category validation should be case-insensitive"""
        assert detector.is_valid_category("PM_REASONING") is True
        assert detector.is_valid_category("Pm_Reasoning") is True

    def test_category_whitespace_trimmed(self, detector):
        """Category validation should trim whitespace"""
        assert detector.is_valid_category("  pm_reasoning  ") is True


class TestReportValueAssessment:
    """Test ReportValueAssessment dataclass"""

    def test_is_valid_true(self):
        """Assessment is valid when all conditions met"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=True,
            report_value_category="pm_reasoning",
            is_speculative=False,
        )
        assert assessment.is_valid is True

    def test_is_valid_false_no_report_value(self):
        """Assessment is invalid when no report value"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=False,
        )
        assert assessment.is_valid is False

    def test_is_valid_false_speculative(self):
        """Assessment is invalid when speculative"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=True,
            report_value_category="pm_reasoning",
            is_speculative=True,
        )
        assert assessment.is_valid is False

    def test_is_valid_false_invalid_category(self):
        """Assessment is invalid when category not in allowed list"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=True,
            report_value_category="not_allowed",
            is_speculative=False,
        )
        assert assessment.is_valid is False

    def test_summary_valid(self):
        """Summary for valid assessment"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=True,
            report_value_category="pm_reasoning",
            is_speculative=False,
        )
        assert "Valid report value" in assessment.summary()
        assert "pm_reasoning" in assessment.summary()

    def test_summary_missing(self):
        """Summary for missing report value"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=False,
        )
        assert "No report value" in assessment.summary()

    def test_summary_speculative(self):
        """Summary for speculative report value"""
        assessment = ReportValueAssessment(
            artifact_id="test",
            file_path="test.py",
            has_report_value=True,
            report_value_category="pm_reasoning",
            is_speculative=True,
            justification="Might improve things",
        )
        assert "Speculative" in assessment.summary()


class TestReportValueHealthScore:
    """Test ReportValueHealthScore dataclass"""

    def test_coverage_percentage_calculation(self):
        """Test coverage percentage calculation"""
        score = ReportValueHealthScore(
            total_artifacts=10,
            artifacts_with_report_value=7,
        )
        assert score.coverage_percentage == 70.0

    def test_valid_percentage_calculation(self):
        """Test valid percentage calculation"""
        score = ReportValueHealthScore(
            total_artifacts=10,
            artifacts_with_valid_report_value=5,
        )
        assert score.valid_percentage == 50.0

    def test_infrastructure_drift_percentage(self):
        """Test infrastructure drift percentage calculation"""
        score = ReportValueHealthScore(
            total_artifacts=10,
            artifacts_infrastructure_heavy=3,
        )
        assert score.infrastructure_drift_percentage == 30.0

    def test_zero_artifacts_no_division_error(self):
        """Test that zero artifacts doesn't cause division by zero"""
        score = ReportValueHealthScore(total_artifacts=0)
        assert score.coverage_percentage == 0.0
        assert score.valid_percentage == 0.0
        assert score.infrastructure_drift_percentage == 0.0

    def test_summary_format(self):
        """Test summary string format"""
        score = ReportValueHealthScore(
            total_artifacts=10,
            artifacts_with_report_value=8,
            artifacts_with_valid_report_value=6,
            artifacts_infrastructure_heavy=2,
        )
        summary = score.summary()
        assert "60.0%" in summary
        assert "6/10" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
