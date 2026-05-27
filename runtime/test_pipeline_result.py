"""Unit tests for pipeline_result.py.

Validates PipelineResult dataclass instantiation, field types, and contract
correctness for deterministic pipeline output.
"""

import pytest
from dataclasses import fields

from runtime.pipeline_result import PipelineResult


class TestPipelineResultInstantiation:
    """Tests for PipelineResult dataclass creation."""

    def test_instantiation_with_all_fields(self):
        result = PipelineResult(
            run_id="abc-123-def-456",
            runtime_state="healthy",
            generated_artifacts=["output/daily_report.md", "output/abc_provenance.yaml"],
            degraded_categories=[],
            severity_events=[],
            report_path="output/daily_report.md",
            provenance_path="output/abc_provenance.yaml",
            run_context_path="output/abc_run_context.yaml",
            deterministic_integrity_state="verified",
            semantic_snapshot_path="state/snapshots/abc_semantic_snapshot.yaml",
        )
        assert result.run_id == "abc-123-def-456"
        assert result.runtime_state == "healthy"
        assert result.generated_artifacts == ["output/daily_report.md", "output/abc_provenance.yaml"]
        assert result.degraded_categories == []
        assert result.severity_events == []
        assert result.report_path == "output/daily_report.md"
        assert result.provenance_path == "output/abc_provenance.yaml"
        assert result.run_context_path == "output/abc_run_context.yaml"
        assert result.deterministic_integrity_state == "verified"
        assert result.semantic_snapshot_path == "state/snapshots/abc_semantic_snapshot.yaml"

    def test_instantiation_with_none_optional_fields(self):
        result = PipelineResult(
            run_id="run-001",
            runtime_state="collapsed",
            generated_artifacts=[],
            degraded_categories=["allocation", "regime", "attribution"],
            severity_events=[{"severity": "critical", "message": "all engines failed", "source": "orchestrator"}],
            report_path=None,
            provenance_path=None,
            run_context_path="output/run-001_run_context.yaml",
            deterministic_integrity_state="failed",
            semantic_snapshot_path=None,
        )
        assert result.report_path is None
        assert result.provenance_path is None
        assert result.semantic_snapshot_path is None

    def test_degraded_pipeline_result(self):
        result = PipelineResult(
            run_id="run-degraded",
            runtime_state="degraded",
            generated_artifacts=["output/daily_report.md"],
            degraded_categories=["flow", "liquidity"],
            severity_events=[
                {"severity": "degraded", "message": "flow engine timeout", "source": "flow_engine"},
                {"severity": "degraded", "message": "liquidity engine unavailable", "source": "liquidity_engine"},
            ],
            report_path="output/daily_report.md",
            provenance_path="output/run-degraded_provenance.yaml",
            run_context_path="output/run-degraded_run_context.yaml",
            deterministic_integrity_state="unverified",
            semantic_snapshot_path="state/snapshots/run-degraded_semantic_snapshot.yaml",
        )
        assert result.runtime_state == "degraded"
        assert len(result.degraded_categories) == 2
        assert len(result.severity_events) == 2


class TestPipelineResultFieldTypes:
    """Tests verifying field type annotations on the dataclass."""

    def test_has_10_fields(self):
        assert len(fields(PipelineResult)) == 10

    def test_field_names(self):
        expected_names = {
            "run_id",
            "runtime_state",
            "generated_artifacts",
            "degraded_categories",
            "severity_events",
            "report_path",
            "provenance_path",
            "run_context_path",
            "deterministic_integrity_state",
            "semantic_snapshot_path",
        }
        actual_names = {f.name for f in fields(PipelineResult)}
        assert actual_names == expected_names

    def test_run_id_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "run_id")
        assert f.type is str

    def test_runtime_state_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "runtime_state")
        assert f.type is str

    def test_generated_artifacts_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "generated_artifacts")
        assert f.type == list[str]

    def test_degraded_categories_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "degraded_categories")
        assert f.type == list[str]

    def test_severity_events_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "severity_events")
        assert f.type == list[dict]

    def test_report_path_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "report_path")
        assert f.type == str | None

    def test_provenance_path_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "provenance_path")
        assert f.type == str | None

    def test_run_context_path_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "run_context_path")
        assert f.type is str

    def test_deterministic_integrity_state_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "deterministic_integrity_state")
        assert f.type is str

    def test_semantic_snapshot_path_type_annotation(self):
        f = next(f for f in fields(PipelineResult) if f.name == "semantic_snapshot_path")
        assert f.type == str | None


class TestPipelineResultEquality:
    """Tests for dataclass equality behavior."""

    def test_equal_instances(self):
        kwargs = dict(
            run_id="run-eq",
            runtime_state="healthy",
            generated_artifacts=["a.md"],
            degraded_categories=[],
            severity_events=[],
            report_path="a.md",
            provenance_path="p.yaml",
            run_context_path="rc.yaml",
            deterministic_integrity_state="verified",
            semantic_snapshot_path="s.yaml",
        )
        assert PipelineResult(**kwargs) == PipelineResult(**kwargs)

    def test_unequal_instances(self):
        base = dict(
            run_id="run-1",
            runtime_state="healthy",
            generated_artifacts=[],
            degraded_categories=[],
            severity_events=[],
            report_path=None,
            provenance_path=None,
            run_context_path="rc.yaml",
            deterministic_integrity_state="verified",
            semantic_snapshot_path=None,
        )
        modified = dict(base, run_id="run-2")
        assert PipelineResult(**base) != PipelineResult(**modified)


class TestPipelineResultImportability:
    """Tests verifying the module is importable and the class is a dataclass."""

    def test_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(PipelineResult)

    def test_module_docstring_exists(self):
        import runtime.pipeline_result as mod
        assert mod.__doc__ is not None
        assert "Pipeline Result" in mod.__doc__
