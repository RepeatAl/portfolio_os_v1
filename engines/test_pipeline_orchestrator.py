"""Tests for Pipeline Orchestrator.

Validates the PipelineOrchestrator class implements the 10-step pipeline,
forbidden flow detection, and engine failure handling correctly.

Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 8.1, 8.2, 11.1, 15.5, 15.6
"""

import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from engines.pipeline_orchestrator import (
    ALL_SIGNAL_CATEGORIES,
    CANONICAL_SECTIONS,
    CATEGORY_TO_SECTION,
    ENGINE_TIMEOUT_SECONDS,
    EngineTimeoutError,
    PipelineOrchestrator,
    _run_with_timeout,
)
from runtime.pipeline_result import PipelineResult
from runtime.runtime_state_model import RuntimeState
from runtime.severity_taxonomy import Severity


class TestPipelineOrchestratorInit:
    """Test PipelineOrchestrator initialization and config loading."""

    def test_loads_config_from_default_path(self):
        po = PipelineOrchestrator()
        assert po.enforcement_mode == "observability"
        assert po.config is not None

    def test_loads_config_from_custom_path(self, tmp_path):
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("enforcement_mode: hard\ncurrent_phase: test\n")
        po = PipelineOrchestrator(config_path=str(config_file))
        assert po.enforcement_mode == "hard"

    def test_handles_missing_config_gracefully(self, tmp_path):
        po = PipelineOrchestrator(config_path=str(tmp_path / "nonexistent.yaml"))
        assert po.enforcement_mode == "observability"


class TestDetectForbiddenFlows:
    """Test forbidden flow detection (Requirement 1.2, 1.3)."""

    def test_detects_uncovered_categories_as_forbidden(self):
        po = PipelineOrchestrator()
        flows = po.detect_forbidden_flows({})
        # All categories except allocation (which has semantic coverage) are forbidden
        assert len(flows) == 13
        # Each flow has required fields
        for flow in flows:
            assert "source_engine" in flow
            assert "target_section" in flow
            assert "skipped_layers" in flow
            assert "SEMANTICS" in flow["skipped_layers"]
            assert "REASONING" in flow["skipped_layers"]

    def test_detects_report_engine_shortcut(self):
        po = PipelineOrchestrator()
        flows = po.detect_forbidden_flows({"report": {"text": "test"}})
        # 13 category flows + 1 report engine shortcut
        assert len(flows) == 14
        report_flow = [f for f in flows if "run_report_engine" in f["source_engine"]]
        assert len(report_flow) == 1
        assert "SEMANTICS" in report_flow[0]["skipped_layers"]

    def test_flow_contains_source_engine_identifier(self):
        po = PipelineOrchestrator()
        flows = po.detect_forbidden_flows({})
        sources = [f["source_engine"] for f in flows]
        assert "regime_engine" in sources
        assert "attribution_engine" in sources

    def test_flow_contains_target_section(self):
        po = PipelineOrchestrator()
        flows = po.detect_forbidden_flows({})
        sections = [f["target_section"] for f in flows]
        assert "Market Regime" in sections
        assert "Portfolio Structure" in sections


class TestHandleEngineFailure:
    """Test engine failure handling (Requirement 11.1)."""

    def test_marks_categories_as_degraded(self):
        po = PipelineOrchestrator()
        po.handle_engine_failure("allocation_engine", RuntimeError("test"))
        assert "allocation" in po._degraded_categories

    def test_emits_severity_event(self):
        po = PipelineOrchestrator()
        po.handle_engine_failure("regime_engine", RuntimeError("test"))
        assert len(po._severity_events) == 1
        event = po._severity_events[0]
        assert event["severity"] == "DEGRADED"
        assert "regime_engine" in event["message"]

    def test_timeout_error_is_critical(self):
        po = PipelineOrchestrator()
        po.handle_engine_failure(
            "allocation_engine",
            EngineTimeoutError("allocation_engine"),
        )
        assert len(po._severity_events) == 1
        event = po._severity_events[0]
        assert event["severity"] == "CRITICAL"

    def test_multiple_failures_accumulate(self):
        po = PipelineOrchestrator()
        po.handle_engine_failure("allocation_engine", RuntimeError("err1"))
        po.handle_engine_failure("regime_engine", RuntimeError("err2"))
        assert "allocation" in po._degraded_categories
        assert "regime" in po._degraded_categories
        assert "liquidity" in po._degraded_categories
        assert len(po._severity_events) == 2

    def test_does_not_duplicate_categories(self):
        po = PipelineOrchestrator()
        po.handle_engine_failure("allocation_engine", RuntimeError("err1"))
        po.handle_engine_failure("allocation_engine", RuntimeError("err2"))
        assert po._degraded_categories.count("allocation") == 1


class TestEngineTimeout:
    """Test engine timeout mechanism (Requirement 11.1)."""

    def test_timeout_constant_is_60_seconds(self):
        assert ENGINE_TIMEOUT_SECONDS == 60

    def test_run_with_timeout_returns_result(self):
        result = _run_with_timeout(lambda: 42, (), timeout=5)
        assert result == 42

    def test_run_with_timeout_raises_on_timeout(self):
        import time

        def slow_func():
            time.sleep(10)

        with pytest.raises(EngineTimeoutError):
            _run_with_timeout(slow_func, (), timeout=1)

    def test_run_with_timeout_propagates_exceptions(self):
        def failing_func():
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            _run_with_timeout(failing_func, (), timeout=5)


class TestExecutePipeline:
    """Test the full execute() pipeline (Requirements 8.1, 8.2, 15.5, 15.6)."""

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_returns_pipeline_result(self, mock_run_all):
        mock_run_all.return_value = {
            "allocation": {"allocation_df": None},
            "regime": {},
        }
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        result = po.execute(input_files=[])

        assert isinstance(result, PipelineResult)
        assert result.run_id is not None
        assert result.runtime_state in [s.value for s in RuntimeState]
        assert isinstance(result.generated_artifacts, list)
        assert isinstance(result.degraded_categories, list)
        assert isinstance(result.severity_events, list)
        assert result.run_context_path is not None
        assert result.deterministic_integrity_state in [
            "verified", "unverified", "failed"
        ]

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_creates_run_context(self, mock_run_all):
        mock_run_all.return_value = {}
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        result = po.execute(input_files=[])

        assert result.run_id is not None
        assert os.path.exists(result.run_context_path)

    @patch("engines.pipeline_orchestrator.run_all_engines")
    def test_handles_engine_runner_failure(self, mock_run_all):
        mock_run_all.side_effect = RuntimeError("Engine runner crashed")
        po = PipelineOrchestrator()
        po.output_dir = tempfile.mkdtemp()
        po.state_dir = tempfile.mkdtemp()

        result = po.execute(input_files=[])

        assert isinstance(result, PipelineResult)
        assert len(result.degraded_categories) > 0
        assert len(result.severity_events) > 0


class TestConstants:
    """Test module-level constants are correctly defined."""

    def test_all_signal_categories_has_14_entries(self):
        assert len(ALL_SIGNAL_CATEGORIES) == 14

    def test_canonical_sections_has_9_entries(self):
        assert len(CANONICAL_SECTIONS) == 9

    def test_category_to_section_maps_all_categories(self):
        for category in ALL_SIGNAL_CATEGORIES:
            assert category in CATEGORY_TO_SECTION

    def test_all_sections_in_canonical_list(self):
        for section in CATEGORY_TO_SECTION.values():
            assert section in CANONICAL_SECTIONS
