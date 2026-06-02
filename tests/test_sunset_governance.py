"""Unit tests for governance/sunset_governance.py.

Tests the 4-phase sunset model, phase evaluation, sunset report generation,
and deprecation governance field validation.

Validates: Requirements 2.5, 25.1, 25.2, 25.3, 25.4
"""

import tempfile
from datetime import date
from pathlib import Path

import pytest
import yaml

from governance.sunset_governance import (
    CompatibilityImpact,
    DeprecationGovernance,
    SunsetGovernance,
    SunsetPhase,
    SunsetReportEntry,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _create_registry(artifacts: list[dict], tmp_path: Path) -> str:
    """Create a temporary artifact registry YAML file."""
    registry_path = tmp_path / "artifact_registry.yaml"
    registry_path.write_text(yaml.dump({"artifacts": artifacts}, sort_keys=False))
    return str(registry_path)


@pytest.fixture
def basic_registry(tmp_path):
    """Registry with a single deprecated artifact."""
    artifacts = [
        {
            "artifact_id": "test_briefing_txt",
            "file_path": "test_briefing.txt",
            "primary_domain": "REPORT",
            "artifact_type": "REPORT_OUT",
            "lifecycle_status": "deprecated",
            "deprecated_date": "2026-05-27",
            "sunset_date": "2026-08-27",
            "replacement_artifact": "daily_report_md",
            "deprecation_reason": "Replaced by chain-compliant output",
            "compatibility_impact": "minor",
            "dependencies": [],
        },
        {
            "artifact_id": "daily_report_md",
            "file_path": "output/daily_report.md",
            "primary_domain": "REPORT",
            "artifact_type": "REPORT_OUT",
            "lifecycle_status": "current",
            "dependencies": ["test_briefing_txt"],
        },
    ]
    return _create_registry(artifacts, tmp_path)


@pytest.fixture
def multi_phase_registry(tmp_path):
    """Registry with artifacts in different sunset phases."""
    artifacts = [
        {
            "artifact_id": "not_deprecated_artifact",
            "file_path": "active.txt",
            "lifecycle_status": "current",
        },
        {
            "artifact_id": "warning_only_artifact",
            "file_path": "warning.txt",
            "lifecycle_status": "deprecated",
            "deprecated_date": "2026-05-27",
            # No replacement_artifact → WARNING_ONLY
        },
        {
            "artifact_id": "replacement_path_artifact",
            "file_path": "replacement.txt",
            "lifecycle_status": "deprecated",
            "deprecated_date": "2026-05-27",
            "sunset_date": "2026-08-27",
            "replacement_artifact": "new_artifact",
        },
        {
            "artifact_id": "runtime_disabled_artifact",
            "file_path": "disabled.txt",
            "lifecycle_status": "deprecated",
            "deprecated_date": "2026-01-01",
            "sunset_date": "2026-06-01",
            "replacement_artifact": "new_artifact",
        },
        {
            "artifact_id": "archived_artifact",
            "file_path": "archived.txt",
            "lifecycle_status": "archived",
            "deprecated_date": "2025-01-01",
            "sunset_date": "2025-06-01",
        },
        {
            # This artifact depends on runtime_disabled_artifact
            "artifact_id": "consumer_artifact",
            "file_path": "consumer.txt",
            "lifecycle_status": "current",
            "dependencies": ["runtime_disabled_artifact"],
        },
    ]
    return _create_registry(artifacts, tmp_path)


# ---------------------------------------------------------------------------
# DeprecationGovernance Validation Tests
# ---------------------------------------------------------------------------


class TestDeprecationGovernance:
    """Tests for DeprecationGovernance dataclass validation."""

    def test_valid_fields(self):
        gov = DeprecationGovernance(
            deprecated_date="2026-05-27",
            sunset_date="2026-08-27",
            replacement_artifact="daily_report_md",
            deprecation_reason="Replaced by chain-compliant output",
            compatibility_impact="minor",
        )
        assert gov.validate() == []

    def test_invalid_deprecated_date(self):
        gov = DeprecationGovernance(deprecated_date="not-a-date")
        errors = gov.validate()
        assert len(errors) == 1
        assert "deprecated_date" in errors[0]

    def test_invalid_sunset_date(self):
        gov = DeprecationGovernance(sunset_date="2026-13-45")
        errors = gov.validate()
        assert len(errors) == 1
        assert "sunset_date" in errors[0]

    def test_reason_too_long(self):
        gov = DeprecationGovernance(deprecation_reason="x" * 201)
        errors = gov.validate()
        assert len(errors) == 1
        assert "200 chars" in errors[0]

    def test_invalid_compatibility_impact(self):
        gov = DeprecationGovernance(compatibility_impact="catastrophic")
        errors = gov.validate()
        assert len(errors) == 1
        assert "compatibility_impact" in errors[0]

    def test_sunset_before_deprecated(self):
        gov = DeprecationGovernance(
            deprecated_date="2026-08-27",
            sunset_date="2026-05-27",
        )
        errors = gov.validate()
        assert len(errors) == 1
        assert "sunset_date must be on or after" in errors[0]

    def test_all_none_is_valid(self):
        gov = DeprecationGovernance()
        assert gov.validate() == []


# ---------------------------------------------------------------------------
# SunsetPhase Evaluation Tests
# ---------------------------------------------------------------------------


class TestEvaluateSunsetPhase:
    """Tests for SunsetGovernance.evaluate_sunset_phase()."""

    def test_not_deprecated(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        assert sg.evaluate_sunset_phase("not_deprecated_artifact") == SunsetPhase.NOT_DEPRECATED

    def test_warning_only(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        assert sg.evaluate_sunset_phase("warning_only_artifact") == SunsetPhase.WARNING_ONLY

    def test_replacement_path(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        assert sg.evaluate_sunset_phase("replacement_path_artifact") == SunsetPhase.REPLACEMENT_PATH

    def test_runtime_disabled(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 7, 1),
        )
        assert sg.evaluate_sunset_phase("runtime_disabled_artifact") == SunsetPhase.RUNTIME_DISABLED

    def test_archived(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 7, 1),
        )
        assert sg.evaluate_sunset_phase("archived_artifact") == SunsetPhase.ARCHIVED

    def test_unknown_artifact_raises(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        with pytest.raises(ValueError, match="not found"):
            sg.evaluate_sunset_phase("nonexistent_artifact")


# ---------------------------------------------------------------------------
# Sunset Blocked Tests
# ---------------------------------------------------------------------------


class TestSunsetBlocked:
    """Tests for sunset-blocked behavior (deps > 0 at RUNTIME_DISABLED)."""

    def test_sunset_blocked_with_dependencies(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 7, 1),
        )
        # runtime_disabled_artifact has consumer_artifact depending on it
        assert sg.is_sunset_blocked("runtime_disabled_artifact") is True

    def test_not_sunset_blocked_without_dependencies(self, tmp_path):
        artifacts = [
            {
                "artifact_id": "lonely_artifact",
                "file_path": "lonely.txt",
                "lifecycle_status": "deprecated",
                "deprecated_date": "2026-01-01",
                "sunset_date": "2026-06-01",
                "replacement_artifact": "new_thing",
            },
        ]
        registry_path = _create_registry(artifacts, tmp_path)
        sg = SunsetGovernance(
            registry_path=registry_path,
            reference_date=date(2026, 7, 1),
        )
        assert sg.is_sunset_blocked("lonely_artifact") is False

    def test_should_generate_sunset_blocked(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 7, 1),
        )
        # Sunset-blocked: still generates because deps > 0
        assert sg.should_generate("runtime_disabled_artifact") is True

    def test_should_not_generate_sunset_no_deps(self, tmp_path):
        artifacts = [
            {
                "artifact_id": "lonely_artifact",
                "file_path": "lonely.txt",
                "lifecycle_status": "deprecated",
                "deprecated_date": "2026-01-01",
                "sunset_date": "2026-06-01",
                "replacement_artifact": "new_thing",
            },
        ]
        registry_path = _create_registry(artifacts, tmp_path)
        sg = SunsetGovernance(
            registry_path=registry_path,
            reference_date=date(2026, 7, 1),
        )
        assert sg.should_generate("lonely_artifact") is False


# ---------------------------------------------------------------------------
# Sunset Report Tests
# ---------------------------------------------------------------------------


class TestGetSunsetReport:
    """Tests for SunsetGovernance.get_sunset_report()."""

    def test_report_contains_all_deprecated(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        report = sg.get_sunset_report()
        # 4 artifacts have deprecated_date set
        assert len(report) == 4

    def test_report_entry_fields(self, basic_registry):
        sg = SunsetGovernance(
            registry_path=basic_registry,
            reference_date=date(2026, 6, 15),
        )
        report = sg.get_sunset_report()
        assert len(report) == 1
        entry = report[0]
        assert entry.artifact_id == "test_briefing_txt"
        assert entry.phase == SunsetPhase.REPLACEMENT_PATH
        assert entry.deprecated_date == "2026-05-27"
        assert entry.sunset_date == "2026-08-27"
        assert entry.replacement_artifact == "daily_report_md"
        assert entry.deprecation_reason == "Replaced by chain-compliant output"
        assert entry.compatibility_impact == "minor"
        assert entry.age_days == 19  # 2026-05-27 to 2026-06-15
        assert entry.remaining_days == 73  # 2026-06-15 to 2026-08-27
        # daily_report_md depends on test_briefing_txt in this fixture
        assert entry.downstream_dependency_count == 1
        assert entry.sunset_blocked is False

    def test_report_with_sunset_blocked(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 7, 1),
        )
        report = sg.get_sunset_report()
        blocked_entries = [e for e in report if e.sunset_blocked]
        assert len(blocked_entries) == 1
        assert blocked_entries[0].artifact_id == "runtime_disabled_artifact"


# ---------------------------------------------------------------------------
# Deprecation Warning Tests
# ---------------------------------------------------------------------------


class TestDeprecationWarnings:
    """Tests for deprecation warning messages."""

    def test_warning_only_message(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        msg = sg.get_deprecation_warning("warning_only_artifact")
        assert "[DEPRECATION WARNING]" in msg
        assert "warning_only_artifact" in msg

    def test_replacement_path_message(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        msg = sg.get_deprecation_warning("replacement_path_artifact")
        assert "[DEPRECATION WARNING]" in msg
        assert "Replacement:" in msg
        assert "new_artifact" in msg

    def test_sunset_blocked_critical_message(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 7, 1),
        )
        msg = sg.get_deprecation_warning("runtime_disabled_artifact")
        assert "[CRITICAL]" in msg
        assert "sunset date" in msg.lower() or "Sunset-blocked" in msg

    def test_no_warning_for_active(self, multi_phase_registry):
        sg = SunsetGovernance(
            registry_path=multi_phase_registry,
            reference_date=date(2026, 6, 15),
        )
        msg = sg.get_deprecation_warning("not_deprecated_artifact")
        assert msg is None


# ---------------------------------------------------------------------------
# Real Registry Integration Test
# ---------------------------------------------------------------------------


class TestRealRegistry:
    """Integration test against the actual artifact registry."""

    def test_real_registry_loads(self):
        sg = SunsetGovernance(reference_date=date(2026, 6, 15))
        report = sg.get_sunset_report()
        # Should find 15 deprecated briefing files
        assert len(report) == 15

    def test_all_briefings_in_replacement_path(self):
        sg = SunsetGovernance(reference_date=date(2026, 6, 15))
        report = sg.get_sunset_report()
        for entry in report:
            assert entry.phase == SunsetPhase.REPLACEMENT_PATH
            assert entry.replacement_artifact == "daily_report_md"
            assert entry.compatibility_impact == "minor"

    def test_all_briefings_runtime_disabled_after_sunset(self):
        sg = SunsetGovernance(reference_date=date(2026, 9, 1))
        report = sg.get_sunset_report()
        for entry in report:
            assert entry.phase == SunsetPhase.RUNTIME_DISABLED
