"""
Test Report Value Registry Compliance

Validates that the actual artifact_registry.yaml achieves 100% report_value
field population with valid categories and no speculative language.

This test exercises the Report_Value_Detector against the real registry file,
confirming the wiring between the detector and the registry is operational.

Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6
"""

import sys
from pathlib import Path

import pytest
import yaml

# Ensure the src directory is importable
sys.path.insert(0, str(Path(__file__).parent))

from report_value_detector import (
    ReportValueDetector,
    ALLOWED_REPORT_VALUE_CATEGORIES,
    SPECULATIVE_KEYWORDS,
)


REGISTRY_PATH = Path(__file__).parent.parent / "artifact_registry.yaml"


class TestRegistryReportValueCompliance:
    """Validate the actual artifact registry for 100% report_value compliance."""

    @pytest.fixture
    def detector(self):
        return ReportValueDetector()

    @pytest.fixture
    def registry_artifacts(self):
        """Load artifacts from the actual registry file."""
        with open(REGISTRY_PATH, "r") as f:
            data = yaml.safe_load(f)
        return data.get("artifacts", [])

    def test_registry_file_exists(self):
        """Requirement 4.6: Registry must exist and be loadable."""
        assert REGISTRY_PATH.exists(), f"Registry not found at {REGISTRY_PATH}"

    def test_registry_has_artifacts(self, registry_artifacts):
        """Registry must contain at least one artifact."""
        assert len(registry_artifacts) > 0, "Registry contains no artifacts"

    def test_100_percent_report_value_population(self, detector, registry_artifacts):
        """
        Requirement 4.6: 100% report_value field population across all registered artifacts.
        """
        missing = detector.detect_missing_report_value(registry_artifacts)
        missing_ids = [a.get("artifact_id", "UNKNOWN") for a in missing]
        assert len(missing) == 0, (
            f"Artifacts missing report_value ({len(missing)}): {missing_ids}"
        )

    def test_all_categories_are_valid(self, detector, registry_artifacts):
        """
        Requirement 4.2: Every report_value category must be one of the 10 accepted categories.
        """
        invalid = []
        for artifact in registry_artifacts:
            rv = artifact.get("report_value")
            if rv and isinstance(rv, dict):
                category = rv.get("category", "").strip().lower()
                if category and category not in ALLOWED_REPORT_VALUE_CATEGORIES:
                    invalid.append((artifact.get("artifact_id"), category))
        assert len(invalid) == 0, (
            f"Artifacts with invalid categories ({len(invalid)}): {invalid}"
        )

    def test_no_speculative_justifications(self, detector, registry_artifacts):
        """
        Requirement 4.4: No report_value justification contains speculative language.
        """
        speculative = []
        for artifact in registry_artifacts:
            rv = artifact.get("report_value")
            if rv and isinstance(rv, dict):
                justification = rv.get("justification", "")
                if detector._is_speculative_claim(justification):
                    for kw in SPECULATIVE_KEYWORDS:
                        if kw in justification.lower():
                            speculative.append((artifact.get("artifact_id"), kw))
                            break
        assert len(speculative) == 0, (
            f"Artifacts with speculative justifications ({len(speculative)}): {speculative}"
        )

    def test_no_empty_report_value_fields(self, registry_artifacts):
        """
        Requirement 4.5: No report_value field has empty category or justification.
        """
        empty = []
        for artifact in registry_artifacts:
            rv = artifact.get("report_value")
            if rv and isinstance(rv, dict):
                category = rv.get("category", "").strip()
                justification = rv.get("justification", "").strip()
                if not category or not justification:
                    empty.append(artifact.get("artifact_id"))
        assert len(empty) == 0, (
            f"Artifacts with empty report_value fields ({len(empty)}): {empty}"
        )

    def test_validate_registry_file_method(self, detector):
        """
        Test the validate_registry_file() method returns compliant results.
        """
        result = detector.validate_registry_file(str(REGISTRY_PATH))
        assert result["is_compliant"] is True, (
            f"Registry not compliant: "
            f"missing={result['missing_report_value']}, "
            f"invalid_categories={result['invalid_categories']}, "
            f"speculative={result['speculative_justifications']}, "
            f"empty={result['empty_fields']}"
        )
        assert result["total_artifacts"] > 0
        assert result["coverage_percentage"] == 100.0
        assert result["valid_count"] == result["total_artifacts"]

    def test_health_score_100_percent_valid(self, detector, registry_artifacts):
        """
        Requirement 4.6: Health score shows 100% valid coverage.
        """
        score = detector.generate_health_score(registry_artifacts)
        assert score.valid_percentage == 100.0, (
            f"Expected 100% valid, got {score.valid_percentage:.1f}%"
        )
        assert score.coverage_percentage == 100.0, (
            f"Expected 100% coverage, got {score.coverage_percentage:.1f}%"
        )
        assert score.artifacts_missing_report_value == 0
        assert score.artifacts_speculative == 0

    def test_all_10_categories_represented(self, detector, registry_artifacts):
        """
        Verify that the registry uses a healthy distribution of categories.
        At least 5 of the 10 categories should be represented.
        """
        score = detector.generate_health_score(registry_artifacts)
        categories_used = set(score.category_distribution.keys())
        assert len(categories_used) >= 5, (
            f"Only {len(categories_used)} categories used: {categories_used}. "
            f"Expected at least 5 of 10."
        )

    def test_boundary_validator_produces_zero_warnings(self, registry_artifacts):
        """
        Requirement 4.6: BoundaryAwarenessValidator produces zero report_value warnings.
        """
        from artifact_registry import ArtifactRegistry
        from domain_registry import DomainRegistry
        from observer_boundary_awareness import BoundaryAwarenessValidator

        ar = ArtifactRegistry()
        dr = DomainRegistry()
        validator = BoundaryAwarenessValidator(ar, dr)
        warnings = validator.check_report_value(registry_artifacts)
        assert len(warnings) == 0, (
            f"Expected zero warnings, got {len(warnings)}: "
            f"{[w.warning_message for w in warnings]}"
        )
