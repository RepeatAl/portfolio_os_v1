"""Unit tests for engines/report_engine.py.

Tests the 4 sub-components (SectionCompletenessClassifier, ProvenanceAssembler,
SectionRenderer, DegradationRenderer) and the ReportEngine orchestrator.

Validates: Requirements 24.1, 24.2, 24.4
"""

import warnings
from datetime import datetime, timezone, timedelta

import pytest

from engines.report_engine import (
    CANONICAL_SECTIONS,
    CATEGORY_TO_SECTION,
    COMPLETENESS_STATES,
    DegradationRenderer,
    ProvenanceAssembler,
    ReportEngine,
    SectionCompletenessClassifier,
    SectionRenderer,
    run_report_engine,
)
from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
)
from runtime.run_context import RunContext
from governance.provenance_schema import SectionProvenance


# --- Helpers ---


def _make_temporal_validity() -> TemporalValidity:
    """Create a TemporalValidity that is currently valid."""
    now = datetime.now(timezone.utc)
    return TemporalValidity(
        valid_from=(now - timedelta(hours=1)).isoformat(),
        valid_until=(now + timedelta(hours=24)).isoformat(),
        stale_after=None,
    )


def _make_valid_object(
    reasoning_id: str = "ro-001",
    category: str = "allocation",
    confidence_level: int = 75,
    producing_engine: str = "decision_engine",
    source_states: list[str] | None = None,
) -> ReasoningObject:
    """Create a valid ReasoningObject with configurable fields."""
    return ReasoningObject(
        reasoning_id=reasoning_id,
        source_semantic_states=source_states or ["state_1", "state_2"],
        conclusion=Conclusion(
            summary=f"Test conclusion for {category}",
            category=category,
        ),
        confidence_level=confidence_level,
        confidence_explanation="Based on available data",
        action_implications=[
            ActionImplication(action="Monitor", rationale="Ongoing signal"),
        ],
        temporal_validity=_make_temporal_validity(),
        producing_engine=producing_engine,
        schema_version="1.0.0",
    )


def _make_invalid_object(reasoning_id: str = "ro-invalid") -> ReasoningObject:
    """Create a ReasoningObject that fails validation."""
    return ReasoningObject(
        reasoning_id="",  # Invalid: empty
        source_semantic_states=[],  # Invalid: empty list
        conclusion=Conclusion(summary="", category=""),  # Invalid: empty
        confidence_level=200,  # Invalid: > 100
        confidence_explanation="",  # Invalid: empty
        action_implications=[],
        temporal_validity=_make_temporal_validity(),
        producing_engine="invalid_engine",  # Invalid
        schema_version="1.0.0",
    )


def _make_low_confidence_object(
    reasoning_id: str = "ro-low",
    category: str = "allocation",
    confidence_level: int = 30,
) -> ReasoningObject:
    """Create a valid ReasoningObject with low confidence."""
    return _make_valid_object(
        reasoning_id=reasoning_id,
        category=category,
        confidence_level=confidence_level,
    )


# --- SectionCompletenessClassifier Tests ---


class TestSectionCompletenessClassifier:
    """Tests for SectionCompletenessClassifier.classify()."""

    def setup_method(self):
        self.classifier = SectionCompletenessClassifier()

    def test_unavailable_when_no_objects(self):
        result = self.classifier.classify("Executive Summary", [])
        assert result == "unavailable"

    def test_complete_when_all_valid_high_confidence(self):
        objects = [
            _make_valid_object("ro-1", confidence_level=80),
            _make_valid_object("ro-2", confidence_level=90),
        ]
        result = self.classifier.classify("Market Regime", objects)
        assert result == "complete"

    def test_invalid_when_all_objects_fail_validation(self):
        objects = [_make_invalid_object(), _make_invalid_object()]
        result = self.classifier.classify("Portfolio Structure", objects)
        assert result == "invalid"

    def test_degraded_when_all_valid_objects_low_confidence(self):
        objects = [
            _make_low_confidence_object("ro-1", confidence_level=20),
            _make_low_confidence_object("ro-2", confidence_level=40),
        ]
        result = self.classifier.classify("Action Space", objects)
        assert result == "degraded"

    def test_partial_when_some_invalid_some_valid(self):
        objects = [
            _make_valid_object("ro-1", confidence_level=80),
            _make_invalid_object(),
        ]
        result = self.classifier.classify("Deployment Analysis", objects)
        assert result == "partial"

    def test_partial_when_some_low_confidence(self):
        objects = [
            _make_valid_object("ro-1", confidence_level=80),
            _make_low_confidence_object("ro-2", confidence_level=30),
        ]
        result = self.classifier.classify("Scenario Analysis", objects)
        assert result == "partial"

    def test_all_completeness_states_are_valid(self):
        """Verify all returned states are in the canonical set."""
        test_cases = [
            ([], "unavailable"),
            ([_make_valid_object()], "complete"),
            ([_make_invalid_object()], "invalid"),
            ([_make_low_confidence_object()], "degraded"),
            ([_make_valid_object(), _make_invalid_object()], "partial"),
        ]
        for objects, expected in test_cases:
            result = self.classifier.classify("Test Section", objects)
            assert result in COMPLETENESS_STATES, f"Got '{result}' not in valid states"
            assert result == expected


# --- ProvenanceAssembler Tests ---


class TestProvenanceAssembler:
    """Tests for ProvenanceAssembler.assemble()."""

    def setup_method(self):
        self.assembler = ProvenanceAssembler()

    def test_assembles_provenance_from_valid_objects(self):
        objects = [
            _make_valid_object("ro-1", source_states=["sem_1", "sem_2"]),
            _make_valid_object("ro-2", source_states=["sem_2", "sem_3"]),
        ]
        prov = self.assembler.assemble("Market Regime", objects, "complete")

        assert isinstance(prov, SectionProvenance)
        assert prov.section_name == "Market Regime"
        assert "ro-1" in prov.reasoning_object_ids
        assert "ro-2" in prov.reasoning_object_ids
        assert "sem_1" in prov.semantic_state_ids
        assert "sem_2" in prov.semantic_state_ids
        assert "sem_3" in prov.semantic_state_ids
        assert prov.completeness_state == "complete"
        assert prov.unavailable_layers == []

    def test_deduplicates_semantic_state_ids(self):
        objects = [
            _make_valid_object("ro-1", source_states=["sem_1", "sem_2"]),
            _make_valid_object("ro-2", source_states=["sem_1", "sem_2"]),
        ]
        prov = self.assembler.assemble("Test", objects, "complete")
        # Should be deduplicated
        assert prov.semantic_state_ids.count("sem_1") == 1
        assert prov.semantic_state_ids.count("sem_2") == 1

    def test_marks_unavailable_layers_when_no_valid_objects(self):
        objects = [_make_invalid_object()]
        prov = self.assembler.assemble("Test Section", objects, "invalid")

        assert len(prov.unavailable_layers) > 0
        layer_names = [layer["layer"] for layer in prov.unavailable_layers]
        assert "REASONING" in layer_names

    def test_empty_objects_marks_all_layers_unavailable(self):
        prov = self.assembler.assemble("Test Section", [], "unavailable")

        layer_names = [layer["layer"] for layer in prov.unavailable_layers]
        assert "REASONING" in layer_names
        assert "SEMANTICS" in layer_names
        assert "SIGNALS" in layer_names

    def test_provenance_includes_producing_engine_as_signal_id(self):
        objects = [
            _make_valid_object("ro-1", producing_engine="decision_engine"),
            _make_valid_object("ro-2", producing_engine="quality_engine"),
        ]
        prov = self.assembler.assemble("Test", objects, "complete")
        assert "decision_engine" in prov.signal_engine_ids
        assert "quality_engine" in prov.signal_engine_ids


# --- SectionRenderer Tests ---


class TestSectionRenderer:
    """Tests for SectionRenderer.render()."""

    def setup_method(self):
        self.renderer = SectionRenderer()

    def test_complete_renders_full_content(self):
        objects = [_make_valid_object("ro-1", category="allocation")]
        result = self.renderer.render("Portfolio Structure", objects, "complete")

        assert "Test conclusion for allocation" in result
        assert "Monitor" in result
        assert "Ongoing signal" in result

    def test_unavailable_renders_degradation_notice_only(self):
        result = self.renderer.render("Executive Summary", [], "unavailable")

        assert "Section Unavailable" in result
        assert "Executive Summary" in result
        assert "No analytical content" in result

    def test_invalid_renders_error_notice(self):
        objects = [_make_invalid_object()]
        result = self.renderer.render("Market Regime", objects, "invalid")

        assert "Validation Error" in result
        assert "Market Regime" in result
        assert "Remediation" in result

    def test_degraded_renders_content_with_confidence_warning(self):
        objects = [_make_low_confidence_object("ro-1", confidence_level=25)]
        result = self.renderer.render("Action Space", objects, "degraded")

        assert "Low Confidence Warning" in result
        assert "25/100" in result
        assert "Test conclusion for allocation" in result

    def test_partial_renders_content_with_partial_notice(self):
        objects = [_make_valid_object("ro-1")]
        result = self.renderer.render("Deployment Analysis", objects, "partial")

        assert "Partial Data Notice" in result
        assert "Test conclusion for allocation" in result

    def test_no_synthetic_content_for_unavailable(self):
        """HARDENING 7: unavailable sections must NOT contain synthetic content."""
        result = self.renderer.render("PM Summary", [], "unavailable")

        # Should not contain any analytical language
        assert "conclusion" not in result.lower() or "No" in result
        assert "Section Unavailable" in result


# --- DegradationRenderer Tests ---


class TestDegradationRenderer:
    """Tests for DegradationRenderer."""

    def setup_method(self):
        self.renderer = DegradationRenderer()

    def test_degradation_notice_includes_section_name(self):
        result = self.renderer.render_degradation_notice(
            "Executive Summary", ["Engine timeout"]
        )
        assert "Executive Summary" in result
        assert "Engine timeout" in result

    def test_degradation_notice_includes_all_reasons(self):
        reasons = ["Engine A failed", "Engine B timeout", "Data unavailable"]
        result = self.renderer.render_degradation_notice("Test", reasons)
        for reason in reasons:
            assert reason in result

    def test_confidence_warning_includes_level(self):
        result = self.renderer.render_confidence_warning("Market Regime", 35)
        assert "35/100" in result
        assert "Market Regime" in result
        assert "Low Confidence Warning" in result

    def test_error_notice_includes_validation_errors(self):
        errors = ["reasoning_id must be non-empty", "confidence_level out of range"]
        result = self.renderer.render_error_notice("Portfolio Structure", errors)
        assert "Validation Error" in result
        assert "Portfolio Structure" in result
        for error in errors:
            assert error in result
        assert "Remediation" in result


# --- ReportEngine Orchestrator Tests ---


class TestReportEngine:
    """Tests for the ReportEngine orchestrating class."""

    def setup_method(self):
        self.engine = ReportEngine()

    def test_canonical_sections_list(self):
        assert len(ReportEngine.CANONICAL_SECTIONS) == 9
        assert "Executive Summary" in ReportEngine.CANONICAL_SECTIONS
        assert "PM Summary" in ReportEngine.CANONICAL_SECTIONS

    def test_render_section_returns_tuple(self):
        objects = [_make_valid_object("ro-1")]
        content, provenance = self.engine.render_section("Market Regime", objects)

        assert isinstance(content, str)
        assert isinstance(provenance, SectionProvenance)

    def test_render_section_complete(self):
        objects = [_make_valid_object("ro-1", confidence_level=80)]
        content, provenance = self.engine.render_section("Market Regime", objects)

        assert "Test conclusion" in content
        assert provenance.completeness_state == "complete"
        assert "ro-1" in provenance.reasoning_object_ids

    def test_render_section_unavailable(self):
        content, provenance = self.engine.render_section("Executive Summary", [])

        assert "Section Unavailable" in content
        assert provenance.completeness_state == "unavailable"
        assert len(provenance.unavailable_layers) > 0

    def test_render_section_invalid(self):
        objects = [_make_invalid_object()]
        content, provenance = self.engine.render_section("Portfolio Structure", objects)

        assert "Validation Error" in content
        assert provenance.completeness_state == "invalid"

    def test_render_section_degraded(self):
        objects = [_make_low_confidence_object("ro-1", confidence_level=20)]
        content, provenance = self.engine.render_section("Action Space", objects)

        assert "Low Confidence Warning" in content
        assert provenance.completeness_state == "degraded"

    def test_sub_components_initialized(self):
        assert isinstance(self.engine.classifier, SectionCompletenessClassifier)
        assert isinstance(self.engine.provenance_assembler, ProvenanceAssembler)
        assert isinstance(self.engine.section_renderer, SectionRenderer)
        assert isinstance(self.engine.degradation_renderer, DegradationRenderer)

    def test_hardening_7_no_inference_on_unavailable(self):
        """HARDENING 7: ReportEngine must NOT create semantics or reasoning."""
        content, _ = self.engine.render_section("Scenario Analysis", [])
        # Must not contain any synthesized analytical content
        assert "Section Unavailable" in content
        # No conclusions should be fabricated
        lines = content.split("\n")
        for line in lines:
            # Lines should only be notice/warning text, not analytical content
            if line.strip() and not line.startswith(">") and not line.startswith("-"):
                # Allow empty lines and notice formatting
                assert "No analytical content" in content


# --- ReportEngine.render() Full Report Tests ---


def _make_run_context() -> RunContext:
    """Create a minimal RunContext for testing."""
    return RunContext(
        run_id="test-run-001",
        timestamp="2026-06-01T08:00:00Z",
        data_sources=[],
        schema_version="1.0.0",
        pipeline_state="healthy",
        report_hash=None,
    )


class TestReportEngineRender:
    """Tests for ReportEngine.render() — full daily report generation.

    Validates: Requirements 6.1, 6.2, 6.4, 6.6, 6.7, 13.1, 13.2
    """

    def setup_method(self):
        self.engine = ReportEngine()
        self.run_context = _make_run_context()

    def test_render_produces_all_9_sections_in_order(self):
        """Requirement 6.1: All 9 canonical sections in fixed order."""
        objects = [
            _make_valid_object("ro-regime", category="regime", confidence_level=80),
            _make_valid_object("ro-alloc", category="allocation", confidence_level=85),
        ]
        result = self.engine.render(
            reasoning_objects=objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # All 9 sections must appear as ## headers
        for section in CANONICAL_SECTIONS:
            assert f"## {section}" in result, f"Missing section: {section}"

        # Verify order: find positions of each section header
        positions = [result.index(f"## {s}") for s in CANONICAL_SECTIONS]
        assert positions == sorted(positions), "Sections are not in canonical order"

    def test_render_includes_report_header_with_timestamp(self):
        """Report starts with a header containing the run timestamp."""
        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )
        assert "# Daily Portfolio Report" in result
        assert "2026-06-01T08:00:00Z" in result

    def test_render_maps_reasoning_objects_to_correct_sections(self):
        """Requirement 13.2: Objects mapped to correct sections via category."""
        regime_obj = _make_valid_object("ro-regime", category="regime", confidence_level=80)
        alloc_obj = _make_valid_object("ro-alloc", category="allocation", confidence_level=85)

        result = self.engine.render(
            reasoning_objects=[regime_obj, alloc_obj],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # regime maps to "Market Regime" section
        market_regime_idx = result.index("## Market Regime")
        portfolio_structure_idx = result.index("## Portfolio Structure")

        # regime content should appear between Market Regime and Portfolio Structure
        regime_content_area = result[market_regime_idx:portfolio_structure_idx]
        assert "Test conclusion for regime" in regime_content_area

        # allocation maps to "Portfolio Structure" section
        concentration_idx = result.index("## Concentration and Dependency")
        portfolio_area = result[portfolio_structure_idx:concentration_idx]
        assert "Test conclusion for allocation" in portfolio_area

    def test_render_includes_provenance_blocks_per_section(self):
        """Requirement 13.1: Provenance block for each section."""
        objects = [
            _make_valid_object("ro-regime", category="regime", confidence_level=80),
        ]
        result = self.engine.render(
            reasoning_objects=objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # Each section should have a provenance YAML block
        yaml_blocks = result.count("```yaml")
        # At least 9 provenance blocks (one per section)
        assert yaml_blocks >= 9

    def test_render_includes_data_availability_summary(self):
        """Requirement 11.5: Data Availability summary with all 14 categories."""
        objects = [
            _make_valid_object("ro-regime", category="regime", confidence_level=80),
        ]
        result = self.engine.render(
            reasoning_objects=objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        assert "## Data Availability" in result
        assert "| Signal Category | Status |" in result

        # All 14 categories should be listed
        for category in CATEGORY_TO_SECTION.keys():
            assert category in result

        # regime should be available, others unavailable
        assert "| regime | available |" in result
        assert "| allocation | unavailable_no_output |" in result

    def test_render_with_no_reasoning_objects_shows_all_unavailable(self):
        """Requirement 6.4: Missing objects produce degradation notices."""
        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # All sections should show unavailable notice
        for section in CANONICAL_SECTIONS:
            assert f"## {section}" in result

        # Data availability should show all unavailable
        assert "unavailable_no_output" in result
        assert "available |" not in result or "unavailable" in result

    def test_render_with_multiple_objects_per_section(self):
        """Multiple categories mapping to same section are grouped."""
        # Both 'regime' and 'flow' map to "Market Regime"
        objects = [
            _make_valid_object("ro-regime", category="regime", confidence_level=80),
            _make_valid_object("ro-flow", category="flow", confidence_level=75),
        ]
        result = self.engine.render(
            reasoning_objects=objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # Both conclusions should appear in Market Regime section
        market_regime_idx = result.index("## Market Regime")
        portfolio_structure_idx = result.index("## Portfolio Structure")
        market_area = result[market_regime_idx:portfolio_structure_idx]

        assert "Test conclusion for regime" in market_area
        assert "Test conclusion for flow" in market_area

    def test_render_with_invalid_objects_shows_error_notice(self):
        """Invalid objects produce error notices in their section."""
        # Create an invalid object with allocation category
        invalid_obj = ReasoningObject(
            reasoning_id="",
            source_semantic_states=[],
            conclusion=Conclusion(summary="", category="allocation"),
            confidence_level=200,
            confidence_explanation="",
            action_implications=[],
            temporal_validity=_make_temporal_validity(),
            producing_engine="invalid_engine",
            schema_version="1.0.0",
        )
        result = self.engine.render(
            reasoning_objects=[invalid_obj],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # Portfolio Structure section should have validation error
        portfolio_idx = result.index("## Portfolio Structure")
        concentration_idx = result.index("## Concentration and Dependency")
        portfolio_area = result[portfolio_idx:concentration_idx]
        assert "Validation Error" in portfolio_area

    def test_render_with_degraded_objects_shows_confidence_warning(self):
        """Degraded objects produce confidence warnings."""
        low_obj = _make_valid_object(
            "ro-low", category="scenario", confidence_level=30
        )
        result = self.engine.render(
            reasoning_objects=[low_obj],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # Scenario Analysis section should have confidence warning
        scenario_idx = result.index("## Scenario Analysis")
        action_idx = result.index("## Action Space")
        scenario_area = result[scenario_idx:action_idx]
        assert "Low Confidence Warning" in scenario_area

    def test_render_returns_string(self):
        """render() returns a string."""
        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_handles_unknown_category_gracefully(self):
        """Objects with unknown categories are not mapped to any section."""
        unknown_obj = _make_valid_object(
            "ro-unknown", category="nonexistent_category", confidence_level=80
        )
        result = self.engine.render(
            reasoning_objects=[unknown_obj],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # Report should still render all 9 sections (all unavailable)
        for section in CANONICAL_SECTIONS:
            assert f"## {section}" in result

    def test_render_data_availability_counts_valid_objects_only(self):
        """Data Availability only counts valid objects as available."""
        invalid_obj = ReasoningObject(
            reasoning_id="",
            source_semantic_states=[],
            conclusion=Conclusion(summary="", category="regime"),
            confidence_level=200,
            confidence_explanation="",
            action_implications=[],
            temporal_validity=_make_temporal_validity(),
            producing_engine="invalid_engine",
            schema_version="1.0.0",
        )
        result = self.engine.render(
            reasoning_objects=[invalid_obj],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        # regime should be unavailable since the object is invalid
        assert "| regime | unavailable_no_output |" in result


# --- Legacy Function Tests ---


class TestRunReportEngineLegacy:
    """Tests for the deprecated run_report_engine() function."""

    def test_emits_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            run_report_engine(
                allocation_data={"target_vs_actual": []},
                regime_data={"Regime Comment": "Test"},
                decision_data={"decisions": []},
                quality_data={"confidence_score": 50, "quality_label": "MEDIUM"},
                scenario_data={"scenarios": []},
            )
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()

    def test_returns_expected_keys(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = run_report_engine(
                allocation_data={"target_vs_actual": []},
                regime_data={"Regime Comment": "Test regime"},
                decision_data={"decisions": []},
                quality_data={"confidence_score": 75, "quality_label": "HIGH"},
                scenario_data={"scenarios": []},
            )
        assert "report" in result
        assert "date" in result
        assert "confidence" in result
        assert result["confidence"] == 75


# --- Constants Tests ---


class TestConstants:
    """Tests for module-level constants."""

    def test_canonical_sections_count(self):
        assert len(CANONICAL_SECTIONS) == 9

    def test_category_to_section_maps_to_valid_sections(self):
        for category, section in CATEGORY_TO_SECTION.items():
            assert section in CANONICAL_SECTIONS, (
                f"Category '{category}' maps to '{section}' which is not canonical"
            )

    def test_completeness_states_are_five(self):
        assert len(COMPLETENESS_STATES) == 5
        assert "complete" in COMPLETENESS_STATES
        assert "partial" in COMPLETENESS_STATES
        assert "degraded" in COMPLETENESS_STATES
        assert "unavailable" in COMPLETENESS_STATES
        assert "invalid" in COMPLETENESS_STATES
