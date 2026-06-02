"""Unit tests for governance/provenance_schema.py.

Tests SectionProvenance and ReportProvenance dataclasses including
serialization (YAML/JSON), persistence, and markdown embedding.
"""

import json
import os
import tempfile

import yaml
import pytest

from governance.provenance_schema import SectionProvenance, ReportProvenance


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_section_provenance() -> SectionProvenance:
    """Create a sample SectionProvenance for testing."""
    return SectionProvenance(
        section_name="Executive Summary",
        reasoning_object_ids=["ro_decision_001", "ro_quality_001"],
        semantic_state_ids=["ai_dependency_high", "concentration_risk_elevated"],
        signal_engine_ids=["allocation_engine", "regime_engine"],
        completeness_state="complete",
        unavailable_layers=[],
        schema_version="1.0.0",
    )


@pytest.fixture
def degraded_section_provenance() -> SectionProvenance:
    """Create a degraded SectionProvenance with unavailable layers."""
    return SectionProvenance(
        section_name="Scenario Analysis",
        reasoning_object_ids=[],
        semantic_state_ids=["ai_dependency_high"],
        signal_engine_ids=["scenario_engine"],
        completeness_state="degraded",
        unavailable_layers=[
            {"layer": "REASONING", "reason": "decision_engine timeout"}
        ],
        schema_version="1.0.0",
    )


@pytest.fixture
def sample_report_provenance(
    sample_section_provenance: SectionProvenance,
    degraded_section_provenance: SectionProvenance,
) -> ReportProvenance:
    """Create a sample ReportProvenance with multiple sections."""
    return ReportProvenance(
        run_context_id="run_abc123",
        timestamp="2026-05-26T08:00:00Z",
        sections=[sample_section_provenance, degraded_section_provenance],
        schema_version="1.0.0",
    )


# ---------------------------------------------------------------------------
# SectionProvenance Tests
# ---------------------------------------------------------------------------


class TestSectionProvenance:
    """Tests for SectionProvenance dataclass."""

    def test_creation_with_all_fields(self, sample_section_provenance: SectionProvenance):
        """Verify all fields are set correctly on creation."""
        sp = sample_section_provenance
        assert sp.section_name == "Executive Summary"
        assert sp.reasoning_object_ids == ["ro_decision_001", "ro_quality_001"]
        assert sp.semantic_state_ids == ["ai_dependency_high", "concentration_risk_elevated"]
        assert sp.signal_engine_ids == ["allocation_engine", "regime_engine"]
        assert sp.completeness_state == "complete"
        assert sp.unavailable_layers == []
        assert sp.schema_version == "1.0.0"

    def test_default_unavailable_layers(self):
        """Verify unavailable_layers defaults to empty list."""
        sp = SectionProvenance(
            section_name="Market Regime",
            reasoning_object_ids=["ro_001"],
            semantic_state_ids=["state_001"],
            signal_engine_ids=["engine_001"],
            completeness_state="complete",
        )
        assert sp.unavailable_layers == []
        assert sp.schema_version == "1.0.0"

    def test_to_yaml_produces_valid_yaml(self, sample_section_provenance: SectionProvenance):
        """Verify to_yaml() produces parseable YAML with correct content."""
        yaml_str = sample_section_provenance.to_yaml()
        parsed = yaml.safe_load(yaml_str)
        assert parsed["section_name"] == "Executive Summary"
        assert parsed["reasoning_object_ids"] == ["ro_decision_001", "ro_quality_001"]
        assert parsed["completeness_state"] == "complete"
        assert parsed["schema_version"] == "1.0.0"

    def test_to_json_produces_valid_json(self, sample_section_provenance: SectionProvenance):
        """Verify to_json() produces parseable JSON with correct content."""
        json_str = sample_section_provenance.to_json()
        parsed = json.loads(json_str)
        assert parsed["section_name"] == "Executive Summary"
        assert parsed["signal_engine_ids"] == ["allocation_engine", "regime_engine"]
        assert parsed["completeness_state"] == "complete"

    def test_to_yaml_includes_unavailable_layers(
        self, degraded_section_provenance: SectionProvenance
    ):
        """Verify unavailable_layers are serialized in YAML output."""
        yaml_str = degraded_section_provenance.to_yaml()
        parsed = yaml.safe_load(yaml_str)
        assert len(parsed["unavailable_layers"]) == 1
        assert parsed["unavailable_layers"][0]["layer"] == "REASONING"
        assert parsed["unavailable_layers"][0]["reason"] == "decision_engine timeout"

    def test_to_json_includes_unavailable_layers(
        self, degraded_section_provenance: SectionProvenance
    ):
        """Verify unavailable_layers are serialized in JSON output."""
        json_str = degraded_section_provenance.to_json()
        parsed = json.loads(json_str)
        assert parsed["unavailable_layers"][0]["layer"] == "REASONING"


# ---------------------------------------------------------------------------
# ReportProvenance Tests
# ---------------------------------------------------------------------------


class TestReportProvenance:
    """Tests for ReportProvenance dataclass."""

    def test_creation_with_sections(self, sample_report_provenance: ReportProvenance):
        """Verify ReportProvenance is created with correct fields."""
        rp = sample_report_provenance
        assert rp.run_context_id == "run_abc123"
        assert rp.timestamp == "2026-05-26T08:00:00Z"
        assert len(rp.sections) == 2
        assert rp.schema_version == "1.0.0"

    def test_persist_creates_sidecar_file(self, sample_report_provenance: ReportProvenance):
        """Verify persist() writes a YAML sidecar file with correct name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = sample_report_provenance.persist(tmpdir)
            assert os.path.exists(file_path)
            assert file_path.endswith("run_abc123_provenance.yaml")

    def test_persist_file_content_is_valid_yaml(
        self, sample_report_provenance: ReportProvenance
    ):
        """Verify the persisted sidecar file contains valid, correct YAML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = sample_report_provenance.persist(tmpdir)
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            assert data["run_context_id"] == "run_abc123"
            assert data["timestamp"] == "2026-05-26T08:00:00Z"
            assert data["schema_version"] == "1.0.0"
            assert len(data["sections"]) == 2
            assert data["sections"][0]["section_name"] == "Executive Summary"
            assert data["sections"][1]["section_name"] == "Scenario Analysis"

    def test_persist_creates_output_directory(
        self, sample_report_provenance: ReportProvenance
    ):
        """Verify persist() creates the output directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_dir = os.path.join(tmpdir, "nested", "output")
            file_path = sample_report_provenance.persist(nested_dir)
            assert os.path.exists(file_path)

    def test_embed_in_markdown_returns_fenced_yaml(
        self, sample_report_provenance: ReportProvenance
    ):
        """Verify embed_in_markdown() returns a fenced YAML code block."""
        result = sample_report_provenance.embed_in_markdown("Executive Summary")
        assert result.startswith("```yaml\n")
        assert result.endswith("```")
        # Extract YAML content between fences
        yaml_content = result[len("```yaml\n"):-len("```")]
        parsed = yaml.safe_load(yaml_content)
        assert parsed["section_name"] == "Executive Summary"

    def test_embed_in_markdown_returns_empty_for_unknown_section(
        self, sample_report_provenance: ReportProvenance
    ):
        """Verify embed_in_markdown() returns empty string for non-existent section."""
        result = sample_report_provenance.embed_in_markdown("Nonexistent Section")
        assert result == ""

    def test_embed_in_markdown_degraded_section(
        self, sample_report_provenance: ReportProvenance
    ):
        """Verify embed_in_markdown() works for degraded sections with unavailable layers."""
        result = sample_report_provenance.embed_in_markdown("Scenario Analysis")
        assert result.startswith("```yaml\n")
        yaml_content = result[len("```yaml\n"):-len("```")]
        parsed = yaml.safe_load(yaml_content)
        assert parsed["completeness_state"] == "degraded"
        assert parsed["unavailable_layers"][0]["layer"] == "REASONING"
