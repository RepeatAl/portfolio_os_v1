"""Unit tests for governance/ontology_growth_observer.py.

Tests the OntologyGrowthObserver observation engine for governance
concept tracking. Validates measure(), report(), and trend() methods.

Requirements: 39.1, 39.2, 39.3, 39.4
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from governance.ontology_growth_observer import OntologyGrowthObserver


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure with registry files."""
    # Create .domainization directory
    domainization_dir = tmp_path / ".domainization"
    domainization_dir.mkdir()

    # Create artifact_registry.yaml with known artifact types
    artifact_registry = [
        {"artifact_id": "art1", "artifact_type": "SSOT", "primary_domain": "GOV"},
        {"artifact_id": "art2", "artifact_type": "ENGINE", "primary_domain": "SIGNALS"},
        {"artifact_id": "art3", "artifact_type": "REPORT_OUT", "primary_domain": "REPORT"},
        {"artifact_id": "art4", "artifact_type": "CONFIG", "primary_domain": "ARCH"},
        {"artifact_id": "art5", "artifact_type": "SSOT", "primary_domain": "DATA"},
    ]
    with open(domainization_dir / "artifact_registry.yaml", "w") as f:
        yaml.dump(artifact_registry, f)

    # Create domain_registry.yaml with known domains
    domain_registry = {
        "domains": [
            {"domain_id": "GOV", "name": "Governance"},
            {"domain_id": "ARCH", "name": "Architecture"},
            {"domain_id": "SIGNALS", "name": "Signal Generation"},
            {"domain_id": "REPORT", "name": "Report"},
        ]
    }
    with open(domainization_dir / "domain_registry.yaml", "w") as f:
        yaml.dump(domain_registry, f)

    # Create runtime/severity_taxonomy.py with known severity levels
    runtime_dir = tmp_path / "runtime"
    runtime_dir.mkdir()
    severity_content = '''"""Severity Taxonomy."""
from enum import IntEnum

class Severity(IntEnum):
    INFO = 0
    WARNING = 1
    DEGRADED = 2
    CRITICAL = 3
    CANONICAL_BREAK = 4
'''
    (runtime_dir / "severity_taxonomy.py").write_text(severity_content)
    (runtime_dir / "__init__.py").write_text("")

    return tmp_path


class TestOntologyGrowthObserverMeasure:
    """Tests for the measure() method."""

    def test_measure_returns_expected_keys(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.measure()

        assert "artifact_type_count" in result
        assert "governance_dimension_count" in result
        assert "severity_level_count" in result
        assert "total_concepts" in result
        assert "timestamp" in result

    def test_measure_counts_unique_artifact_types(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.measure()

        # 4 unique types: SSOT, ENGINE, REPORT_OUT, CONFIG
        assert result["artifact_type_count"] == 4

    def test_measure_counts_governance_dimensions(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.measure()

        # 4 domains defined
        assert result["governance_dimension_count"] == 4

    def test_measure_total_concepts_is_sum(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.measure()

        expected_total = (
            result["artifact_type_count"]
            + result["governance_dimension_count"]
            + result["severity_level_count"]
        )
        assert result["total_concepts"] == expected_total

    def test_measure_with_missing_artifact_registry(self, tmp_path):
        """Missing artifact registry returns 0 for artifact types."""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        # Only create domain registry, not artifact registry
        domain_registry = {"domains": [{"domain_id": "GOV", "name": "Governance"}]}
        with open(domainization_dir / "domain_registry.yaml", "w") as f:
            yaml.dump(domain_registry, f)

        observer = OntologyGrowthObserver(str(tmp_path))
        result = observer.measure()

        assert result["artifact_type_count"] == 0
        assert result["governance_dimension_count"] == 1

    def test_measure_with_missing_domain_registry(self, tmp_path):
        """Missing domain registry returns 0 for dimensions."""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        # Only create artifact registry, not domain registry
        artifacts = [{"artifact_id": "a1", "artifact_type": "SSOT"}]
        with open(domainization_dir / "artifact_registry.yaml", "w") as f:
            yaml.dump(artifacts, f)

        observer = OntologyGrowthObserver(str(tmp_path))
        result = observer.measure()

        assert result["artifact_type_count"] == 1
        assert result["governance_dimension_count"] == 0

    def test_measure_with_empty_registries(self, tmp_path):
        """Empty registries return 0 counts."""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        (domainization_dir / "artifact_registry.yaml").write_text("")
        (domainization_dir / "domain_registry.yaml").write_text("")

        observer = OntologyGrowthObserver(str(tmp_path))
        result = observer.measure()

        assert result["artifact_type_count"] == 0
        assert result["governance_dimension_count"] == 0


class TestOntologyGrowthObserverReport:
    """Tests for the report() method."""

    def test_report_returns_expected_keys(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.report()

        assert "counts" in result
        assert "growth_rate" in result
        assert "recommendation" in result

    def test_report_growth_rate_is_none_without_previous(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.report()

        assert result["growth_rate"] is None

    def test_report_recommendation_is_string(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        result = observer.report()

        assert isinstance(result["recommendation"], str)
        assert result["recommendation"] in ("stable", "growing", "rapid growth - review needed")


class TestOntologyGrowthObserverTrend:
    """Tests for the trend() method."""

    def test_trend_returns_expected_keys(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        previous = {
            "counts": {
                "artifact_type_count": 3,
                "governance_dimension_count": 3,
                "severity_level_count": 4,
                "total_concepts": 10,
            }
        }
        result = observer.trend(previous)

        assert "current" in result
        assert "previous" in result
        assert "growth_rate" in result
        assert "recommendation" in result
        assert "deltas" in result

    def test_trend_computes_positive_growth_rate(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        previous = {
            "artifact_type_count": 2,
            "governance_dimension_count": 2,
            "severity_level_count": 2,
            "total_concepts": 6,
        }
        result = observer.trend(previous)

        # Current total > 6, so growth rate should be positive
        assert result["growth_rate"] > 0.0

    def test_trend_computes_zero_growth_when_same(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        # First measure to get current values
        current = observer.measure()
        # Use current as previous — should yield 0% growth
        result = observer.trend(current)

        assert result["growth_rate"] == 0.0
        assert result["recommendation"] == "stable"

    def test_trend_handles_zero_previous_total(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        previous = {"total_concepts": 0}
        result = observer.trend(previous)

        # With zero previous and non-zero current, growth_rate = 100%
        assert result["growth_rate"] == 100.0

    def test_trend_deltas_are_correct(self, temp_project):
        observer = OntologyGrowthObserver(str(temp_project))
        previous = {
            "artifact_type_count": 2,
            "governance_dimension_count": 3,
            "severity_level_count": 4,
            "total_concepts": 9,
        }
        result = observer.trend(previous)

        # artifact_type_count is 4, previous was 2 → delta = 2
        assert result["deltas"]["artifact_type_delta"] == 2
        # governance_dimension_count is 4, previous was 3 → delta = 1
        assert result["deltas"]["governance_dimension_delta"] == 1

    def test_trend_accepts_nested_report_format(self, temp_project):
        """trend() should accept output from report() as previous."""
        observer = OntologyGrowthObserver(str(temp_project))
        report = observer.report()
        # Use the report as previous — should yield 0% growth
        result = observer.trend(report)

        assert result["growth_rate"] == 0.0


class TestOntologyGrowthObserverRecommendations:
    """Tests for recommendation logic."""

    def test_stable_recommendation_for_low_count(self, tmp_path):
        """Total concepts <= 30 should yield 'stable'."""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        # Create minimal registries: 1 type + 1 domain = 2 concepts + severity
        artifacts = [{"artifact_id": "a1", "artifact_type": "SSOT"}]
        with open(domainization_dir / "artifact_registry.yaml", "w") as f:
            yaml.dump(artifacts, f)
        domain_registry = {"domains": [{"domain_id": "GOV", "name": "Governance"}]}
        with open(domainization_dir / "domain_registry.yaml", "w") as f:
            yaml.dump(domain_registry, f)

        observer = OntologyGrowthObserver(str(tmp_path))
        result = observer.report()

        # 1 type + 1 domain + 0 severity (no import available) = 2 total
        assert result["recommendation"] == "stable"

    def test_rapid_growth_recommendation_for_high_growth(self, temp_project):
        """Growth rate > 25% should yield 'rapid growth - review needed'."""
        observer = OntologyGrowthObserver(str(temp_project))
        previous = {"total_concepts": 5}
        result = observer.trend(previous)

        # Current is ~13 concepts, previous was 5 → growth > 100%
        assert result["recommendation"] == "rapid growth - review needed"


class TestOntologyGrowthObserverNoEnforcement:
    """Tests confirming the observer does NOT enforce anything."""

    def test_no_blocking_methods(self):
        """Observer should not have any blocking/enforcement methods."""
        observer_methods = dir(OntologyGrowthObserver)
        forbidden_patterns = ["block", "reject", "enforce", "deny", "prevent"]
        for method in observer_methods:
            for pattern in forbidden_patterns:
                assert pattern not in method.lower(), (
                    f"Method '{method}' contains forbidden pattern '{pattern}'. "
                    f"OntologyGrowthObserver MUST NOT contain enforcement logic."
                )

    def test_measure_never_raises(self, tmp_path):
        """measure() should never raise — graceful degradation only."""
        # Point to completely empty directory
        observer = OntologyGrowthObserver(str(tmp_path))
        result = observer.measure()

        # Should return zeros for file-based counts, not raise
        assert result["artifact_type_count"] == 0
        assert result["governance_dimension_count"] == 0
        # severity_level_count may be non-zero if runtime.severity_taxonomy
        # is importable from the project's sys.path — that's expected behavior
        assert isinstance(result["total_concepts"], int)
        assert result["total_concepts"] >= 0


class TestOntologyGrowthObserverRealProject:
    """Integration test against the real project structure."""

    def test_measure_against_real_project(self):
        """Verify observer works against the actual project root."""
        project_root = str(Path(__file__).parent.parent)
        observer = OntologyGrowthObserver(project_root)
        result = observer.measure()

        # Real project has 13 artifact types, 12 domains, 6 severity levels
        assert result["artifact_type_count"] >= 10
        assert result["governance_dimension_count"] >= 10
        assert result["severity_level_count"] == 6
        assert result["total_concepts"] >= 26
