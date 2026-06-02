"""Tests for degradation propagation through the pipeline chain.

Validates that unavailability markers propagate from Pipeline_Orchestrator
through Semantic_Engine to Reasoning_Engines to Report_Engine, that
confidence capping uses ConfidenceDegradationPolicy, and that the
all-engines-fail scenario produces only a Data Availability summary.

Requirements: 11.2, 11.3, 11.4, 11.5, 11.6
"""

import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from engines.pipeline_orchestrator import (
    ALL_SIGNAL_CATEGORIES,
    CANONICAL_SECTIONS,
    CATEGORY_TO_SECTION,
    PipelineOrchestrator,
    EngineTimeoutError,
)
from runtime.confidence_policy import ConfidenceDegradationPolicy
from runtime.pipeline_result import PipelineResult
from runtime.reasoning_object import ReasoningObject
from runtime.runtime_state_model import RuntimeState


class TestConfidenceCappingWithPolicy:
    """Test that confidence capping uses ConfidenceDegradationPolicy (Req 11.3)."""

    def test_orchestrator_loads_confidence_policy(self):
        """PipelineOrchestrator loads ConfidenceDegradationPolicy on init."""
        po = PipelineOrchestrator()
        assert hasattr(po, "_confidence_policy")
        assert isinstance(po._confidence_policy, ConfidenceDegradationPolicy)

    def test_policy_defaults_match_design(self):
        """Default policy: base_ceiling=50, penalty=10, floor=0."""
        po = PipelineOrchestrator()
        policy = po._confidence_policy
        assert policy.base_ceiling == 50
        assert policy.penalty_per_missing_category == 10
        assert policy.minimum_floor == 0

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_confidence_capped_when_categories_degraded(self, mock_run_all):
        """When categories are degraded, confidence uses policy.compute()."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # Simulate 2 degraded categories
        po._degraded_categories = ["allocation", "regime"]

        # Execute reasoning engines with some semantic states
        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = [
            {
                "signal_id": "flow_baseline",
                "category": "flow",
                "meaning": "Test flow state",
                "source": "semantic_engine_placeholder",
                "value": None,
                "completeness": "placeholder",
            }
        ]

        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        # With 2 missing categories, policy.compute(2) = max(0, 50 - 20) = 30
        expected_confidence = po._confidence_policy.compute(2)
        assert expected_confidence == 30

        # All produced reasoning objects should have capped confidence
        for ro in reasoning_objects:
            assert ro.confidence_level == expected_confidence

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_confidence_not_capped_when_no_degradation(self, mock_run_all):
        """When no categories are degraded, confidence is not capped by policy."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # No degraded categories
        po._degraded_categories = []

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = [
            {
                "signal_id": "flow_baseline",
                "category": "flow",
                "meaning": "Test flow state",
                "source": "semantic_engine_placeholder",
                "value": None,
                "completeness": "placeholder",
            }
        ]

        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        # With no degradation, placeholder states get confidence=30 (not policy-capped)
        for ro in reasoning_objects:
            assert ro.confidence_level == 30  # placeholder confidence

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_confidence_floors_at_zero_with_many_failures(self, mock_run_all):
        """With many degraded categories, confidence floors at minimum_floor (0)."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # Simulate 6 degraded categories (50 - 60 = -10, floored to 0)
        po._degraded_categories = [
            "allocation", "regime", "attribution",
            "correlation", "scenario", "flow",
        ]

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = [
            {
                "signal_id": "liquidity_baseline",
                "category": "liquidity",
                "meaning": "Test liquidity state",
                "source": "semantic_engine_placeholder",
                "value": None,
                "completeness": "placeholder",
            }
        ]

        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        expected_confidence = po._confidence_policy.compute(6)
        assert expected_confidence == 0

        for ro in reasoning_objects:
            assert ro.confidence_level == 0


class TestDegradationPropagation:
    """Test that unavailability markers propagate through the chain (Req 11.2)."""

    def test_engine_failure_marks_categories_unavailable(self):
        """handle_engine_failure marks affected categories as degraded."""
        po = PipelineOrchestrator()
        po.handle_engine_failure("allocation_engine", RuntimeError("test"))
        assert "allocation" in po._degraded_categories

    def test_degraded_categories_skip_semantic_state_generation(self):
        """Degraded categories do not get placeholder semantic states."""
        po = PipelineOrchestrator()
        po._degraded_categories = ["allocation", "regime", "liquidity"]

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = po._execute_semantic_engine({}, run_context)

        # Degraded categories should NOT have placeholder states
        categories_in_states = [s.get("category") for s in semantic_states]
        assert "allocation" not in categories_in_states
        assert "regime" not in categories_in_states
        assert "liquidity" not in categories_in_states

    def test_degraded_categories_skip_reasoning_object_generation(self):
        """Degraded categories are skipped in reasoning engine execution."""
        po = PipelineOrchestrator()
        po._degraded_categories = ["allocation"]

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = [
            {
                "signal_id": "allocation_baseline",
                "category": "allocation",
                "meaning": "Test",
                "source": "test",
                "value": None,
                "completeness": "placeholder",
            },
            {
                "signal_id": "flow_baseline",
                "category": "flow",
                "meaning": "Test flow",
                "source": "test",
                "value": None,
                "completeness": "placeholder",
            },
        ]

        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        # allocation should be skipped, flow should be produced
        categories = [ro.conclusion.category for ro in reasoning_objects]
        assert "allocation" not in categories
        assert "flow" in categories

    def test_confidence_explanation_lists_missing_categories(self):
        """Reasoning Objects include explanation about degraded categories."""
        po = PipelineOrchestrator()
        po._degraded_categories = ["allocation", "regime"]

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = [
            {
                "signal_id": "flow_baseline",
                "category": "flow",
                "meaning": "Test flow",
                "source": "test",
                "value": None,
                "completeness": "placeholder",
            },
        ]

        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        for ro in reasoning_objects:
            assert "2 categories degraded" in ro.confidence_explanation


class TestDegradationNoticeRendering:
    """Test that sections with confidence < 50 get degradation notices (Req 11.4)."""

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_low_confidence_sections_get_degradation_notice(self, mock_run_all):
        """Report renders degradation notice for confidence < 50."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # Simulate 3 degraded categories to get confidence = 20
        po._degraded_categories = ["allocation", "regime", "attribution"]

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = [
            {
                "signal_id": "flow_baseline",
                "category": "flow",
                "meaning": "Test flow",
                "source": "test",
                "value": None,
                "completeness": "placeholder",
            },
        ]

        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        # Verify confidence is below 50
        for ro in reasoning_objects:
            assert ro.confidence_level < 50

        # Now render the report
        report_path = po._execute_report_engine(
            reasoning_objects, semantic_states, run_context
        )

        assert report_path is not None
        with open(report_path, "r") as f:
            report_content = f.read()

        # Should contain degradation notice
        assert "Degradation Notice" in report_content


class TestDataAvailabilitySummary:
    """Test Data Availability summary in daily_report.md (Req 11.5)."""

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_data_availability_lists_all_14_categories(self, mock_run_all):
        """Data Availability summary lists all 14 signal categories."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        report_path = po._execute_report_engine([], [], run_context)

        assert report_path is not None
        with open(report_path, "r") as f:
            report_content = f.read()

        assert "## Data Availability" in report_content
        for category in ALL_SIGNAL_CATEGORIES:
            assert category in report_content

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_data_availability_shows_correct_statuses(self, mock_run_all):
        """Available categories show 'available', degraded show 'unavailable_engine_failure'."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()
        po._degraded_categories = ["allocation", "regime"]

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        report_path = po._execute_report_engine([], [], run_context)

        with open(report_path, "r") as f:
            report_content = f.read()

        assert "| allocation | unavailable_engine_failure |" in report_content
        assert "| regime | unavailable_engine_failure |" in report_content
        # Non-degraded categories should be available
        assert "| flow | available |" in report_content


class TestAllEnginesFailScenario:
    """Test all-engines-fail scenario (Requirement 11.6).

    When all Signal Engines fail, the report should contain ONLY the
    Data Availability summary with all categories marked unavailable,
    and no fabricated section content.
    """

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_all_engines_fail_produces_only_data_availability(self, mock_run_all):
        """When all 14 categories are degraded, only Data Availability is rendered."""
        mock_run_all.side_effect = RuntimeError("All engines crashed")
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # Mark all categories as degraded
        po._degraded_categories = list(ALL_SIGNAL_CATEGORIES)

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        report_path = po._execute_report_engine([], [], run_context)

        assert report_path is not None
        with open(report_path, "r") as f:
            report_content = f.read()

        # Should have Data Availability section
        assert "## Data Availability" in report_content

        # Should NOT have any of the 9 canonical sections
        for section in CANONICAL_SECTIONS:
            assert f"## {section}" not in report_content

        # All categories should be marked unavailable
        for category in ALL_SIGNAL_CATEGORIES:
            assert f"| {category} | unavailable_engine_failure |" in report_content

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_all_engines_fail_no_fabricated_content(self, mock_run_all):
        """All-engines-fail report has no fabricated analytical content."""
        mock_run_all.side_effect = RuntimeError("All engines crashed")
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        po._degraded_categories = list(ALL_SIGNAL_CATEGORIES)

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        report_path = po._execute_report_engine([], [], run_context)

        with open(report_path, "r") as f:
            report_content = f.read()

        # Should not contain any reasoning object content
        assert "confidence:" not in report_content.lower() or "confidence" not in report_content.split("## Data Availability")[1]
        # Should not contain degradation notices for sections (no sections rendered)
        assert "No Reasoning Objects available" not in report_content

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_all_engines_fail_end_to_end(self, mock_run_all):
        """Full pipeline execution with all engines failing produces correct result."""
        mock_run_all.side_effect = RuntimeError("All engines crashed")
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        result = po.execute(input_files=[])

        assert isinstance(result, PipelineResult)
        # All categories should be degraded (engine_runner failure marks all)
        # engine_runner failure maps to all categories via "engine_runner" key
        # which falls back to [engine_id] = ["engine_runner"]
        assert len(result.severity_events) > 0

        # Report should still be generated
        assert result.report_path is not None
        with open(result.report_path, "r") as f:
            report_content = f.read()

        assert "## Data Availability" in report_content


class TestDegradationPropagationEndToEnd:
    """Integration tests for the full degradation propagation path."""

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_partial_failure_propagates_through_chain(self, mock_run_all):
        """Partial engine failure propagates correctly through all layers."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # Simulate allocation_engine failure
        po.handle_engine_failure("allocation_engine", RuntimeError("timeout"))

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        # Step 1: Semantic engine should skip allocation
        semantic_states = po._execute_semantic_engine({}, run_context)
        categories_in_states = [s.get("category") for s in semantic_states]
        assert "allocation" not in categories_in_states

        # Step 2: Reasoning engine should skip allocation
        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)
        ro_categories = [ro.conclusion.category for ro in reasoning_objects]
        assert "allocation" not in ro_categories

        # Step 3: Remaining categories should have capped confidence
        expected_confidence = po._confidence_policy.compute(1)  # 1 missing
        assert expected_confidence == 40
        for ro in reasoning_objects:
            assert ro.confidence_level == expected_confidence

        # Step 4: Report should show allocation as unavailable
        report_path = po._execute_report_engine(
            reasoning_objects, semantic_states, run_context
        )
        with open(report_path, "r") as f:
            report_content = f.read()

        assert "| allocation | unavailable_engine_failure |" in report_content
        # Other categories should be available
        assert "| flow | available |" in report_content

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_multiple_failures_compound_degradation(self, mock_run_all):
        """Multiple engine failures compound confidence degradation."""
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        # Simulate multiple engine failures
        po.handle_engine_failure("allocation_engine", RuntimeError("err"))
        po.handle_engine_failure("regime_engine", RuntimeError("err"))
        po.handle_engine_failure("scoring_engine", RuntimeError("err"))

        # allocation, regime, liquidity, correlation, relative_strength = 5 categories
        assert len(po._degraded_categories) == 5

        from runtime.run_context import RunContext
        run_context = RunContext.create([])

        semantic_states = po._execute_semantic_engine({}, run_context)
        reasoning_objects = po._execute_reasoning_engines(semantic_states, run_context)

        # With 5 missing categories: max(0, 50 - 50) = 0
        expected_confidence = po._confidence_policy.compute(5)
        assert expected_confidence == 0

        for ro in reasoning_objects:
            assert ro.confidence_level == 0
            assert "5 categories degraded" in ro.confidence_explanation
