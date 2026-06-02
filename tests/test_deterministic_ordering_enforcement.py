"""Unit tests for deterministic ordering enforcement.

Verifies that all YAML serializations (Run_Context, provenance sidecar,
Semantic State snapshots) produce byte-identical output for same inputs.
Also verifies SHA-256 report hash computation and recording.

Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 22.1, 22.2, 22.3
"""

import hashlib
import os
from pathlib import Path

import pytest
import yaml

from runtime.run_context import RunContext
from runtime.semantic_state_store import SemanticStateStore
from governance.provenance_schema import SectionProvenance, ReportProvenance


class TestRunContextDeterministicYAML:
    """Verify RunContext.persist() produces byte-identical YAML for same inputs."""

    def test_persist_byte_identical_for_same_inputs(self, tmp_path):
        """Two persists of the same RunContext produce byte-identical YAML."""
        ctx = RunContext(
            run_id="fixed-run-id-001",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        dir1 = str(tmp_path / "out1")
        dir2 = str(tmp_path / "out2")
        path1 = ctx.persist(dir1)
        path2 = ctx.persist(dir2)

        content1 = Path(path1).read_bytes()
        content2 = Path(path2).read_bytes()
        assert content1 == content2, "RunContext YAML output is not byte-identical"

    def test_persist_sorted_keys(self, tmp_path):
        """Persisted YAML has keys in sorted order."""
        ctx = RunContext(
            run_id="test-sorted-keys",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash="abc123",
        )

        path = ctx.persist(str(tmp_path / "out"))
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        # Verify keys are in sorted order by re-dumping with sort_keys=True
        reserialized = yaml.safe_dump(data, default_flow_style=False, sort_keys=True)
        with open(path, "r") as f:
            original = f.read()
        assert original == reserialized

    def test_persist_with_data_sources_byte_identical(self, tmp_path):
        """RunContext with data sources produces byte-identical output."""
        from runtime.run_context import DataSourceReference

        sources = [
            DataSourceReference(file_path="z_file.xlsx", content_hash="hash_z", status="available"),
            DataSourceReference(file_path="a_file.xlsx", content_hash="hash_a", status="available"),
            DataSourceReference(file_path="m_file.xlsx", content_hash="hash_m", status="unavailable"),
        ]

        ctx = RunContext(
            run_id="deterministic-test-002",
            timestamp="2026-05-26T09:00:00Z",
            data_sources=sources,
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        dir1 = str(tmp_path / "out1")
        dir2 = str(tmp_path / "out2")
        path1 = ctx.persist(dir1)
        path2 = ctx.persist(dir2)

        assert Path(path1).read_bytes() == Path(path2).read_bytes()


class TestProvenanceDeterministicYAML:
    """Verify ReportProvenance.persist() produces byte-identical YAML for same inputs."""

    def _make_provenance(self) -> ReportProvenance:
        """Create a ReportProvenance with unordered identifier lists."""
        sections = [
            SectionProvenance(
                section_name="Executive Summary",
                reasoning_object_ids=["ro_quality_001", "ro_decision_001"],
                semantic_state_ids=["concentration_risk_elevated", "ai_dependency_high"],
                signal_engine_ids=["regime_engine", "allocation_engine"],
                completeness_state="complete",
                unavailable_layers=[],
            ),
            SectionProvenance(
                section_name="Market Regime",
                reasoning_object_ids=["ro_decision_002"],
                semantic_state_ids=["regime_state_bullish"],
                signal_engine_ids=["regime_engine"],
                completeness_state="complete",
                unavailable_layers=[],
            ),
        ]
        return ReportProvenance(
            run_context_id="run_deterministic_001",
            timestamp="2026-05-26T08:00:00Z",
            sections=sections,
            schema_version="1.0.0",
        )

    def test_persist_byte_identical_for_same_inputs(self, tmp_path):
        """Two persists of the same ReportProvenance produce byte-identical YAML."""
        prov = self._make_provenance()

        dir1 = str(tmp_path / "out1")
        dir2 = str(tmp_path / "out2")
        path1 = prov.persist(dir1)
        path2 = prov.persist(dir2)

        content1 = Path(path1).read_bytes()
        content2 = Path(path2).read_bytes()
        assert content1 == content2, "Provenance YAML output is not byte-identical"

    def test_persist_sorts_identifier_lists(self, tmp_path):
        """Identifier lists in provenance are sorted for determinism."""
        prov = self._make_provenance()
        path = prov.persist(str(tmp_path / "out"))

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        exec_summary = data["sections"][0]
        assert exec_summary["reasoning_object_ids"] == ["ro_decision_001", "ro_quality_001"]
        assert exec_summary["semantic_state_ids"] == ["ai_dependency_high", "concentration_risk_elevated"]
        assert exec_summary["signal_engine_ids"] == ["allocation_engine", "regime_engine"]

    def test_persist_sorted_keys(self, tmp_path):
        """Persisted provenance YAML has keys in sorted order."""
        prov = self._make_provenance()
        path = prov.persist(str(tmp_path / "out"))

        with open(path, "r") as f:
            content = f.read()

        # Re-parse and re-dump with sort_keys=True should be identical
        data = yaml.safe_load(content)
        reserialized = yaml.safe_dump(data, default_flow_style=False, sort_keys=True)
        assert content == reserialized

    def test_section_provenance_to_yaml_sorts_lists(self):
        """SectionProvenance.to_yaml() sorts identifier lists."""
        sp = SectionProvenance(
            section_name="Test Section",
            reasoning_object_ids=["z_ro", "a_ro", "m_ro"],
            semantic_state_ids=["z_state", "a_state"],
            signal_engine_ids=["z_engine", "a_engine"],
            completeness_state="complete",
        )
        yaml_str = sp.to_yaml()
        parsed = yaml.safe_load(yaml_str)

        assert parsed["reasoning_object_ids"] == ["a_ro", "m_ro", "z_ro"]
        assert parsed["semantic_state_ids"] == ["a_state", "z_state"]
        assert parsed["signal_engine_ids"] == ["a_engine", "z_engine"]


class TestSemanticStateStoreDeterministicYAML:
    """Verify SemanticStateStore produces byte-identical YAML for same inputs."""

    @pytest.fixture
    def store(self, tmp_path):
        """Provide a SemanticStateStore with a temporary directory."""
        state_dir = str(tmp_path / "state") + "/"
        return SemanticStateStore(state_dir=state_dir)

    @pytest.fixture
    def sample_states(self):
        """Provide sample semantic states with deterministic content."""
        return [
            {
                "signal_id": "ai_dependency_high",
                "category": "narrative_dependency",
                "meaning": "AI exposure is elevated.",
                "source": "allocation_engine",
                "value": 42.0,
            },
            {
                "signal_id": "concentration_risk_elevated",
                "category": "concentration",
                "meaning": "Concentration risk is high.",
                "source": "scoring_engine",
                "value": 30.0,
            },
        ]

    def test_snapshot_byte_identical_for_same_inputs(self, tmp_path, sample_states):
        """Two saves with same states and run_context produce byte-identical snapshots."""
        # Use two separate stores with identical inputs
        store1 = SemanticStateStore(state_dir=str(tmp_path / "state1") + "/")
        store2 = SemanticStateStore(state_dir=str(tmp_path / "state2") + "/")

        # Create identical RunContexts (fixed run_id and timestamp)
        ctx1 = RunContext(
            run_id="fixed-run-id",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )
        ctx2 = RunContext(
            run_id="fixed-run-id",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        store1.save_snapshot(sample_states, ctx1)
        store2.save_snapshot(sample_states, ctx2)

        snap1_path = store1.snapshots_dir / "fixed-run-id_semantic_snapshot.yaml"
        snap2_path = store2.snapshots_dir / "fixed-run-id_semantic_snapshot.yaml"

        content1 = snap1_path.read_bytes()
        content2 = snap2_path.read_bytes()
        assert content1 == content2, "Semantic snapshot YAML is not byte-identical"

    def test_snapshot_sorted_keys(self, store, sample_states):
        """Snapshot YAML has keys in sorted order."""
        ctx = RunContext(
            run_id="sorted-keys-test",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )
        store.save_snapshot(sample_states, ctx)

        snap_path = store.snapshots_dir / "sorted-keys-test_semantic_snapshot.yaml"
        with open(snap_path, "r") as f:
            content = f.read()

        data = yaml.safe_load(content)
        reserialized = yaml.safe_dump(data, default_flow_style=False, sort_keys=True)
        assert content == reserialized

    def test_latest_pointer_sorted_keys(self, store, sample_states):
        """Latest pointer YAML has keys in sorted order."""
        ctx = RunContext(
            run_id="pointer-test",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )
        store.save_snapshot(sample_states, ctx)

        with open(store.latest_pointer_path, "r") as f:
            content = f.read()

        data = yaml.safe_load(content)
        reserialized = yaml.safe_dump(data, default_flow_style=False, sort_keys=True)
        assert content == reserialized


class TestReportHashComputation:
    """Verify SHA-256 report hash computation and recording in RunContext."""

    def test_compute_and_record_report_hash(self, tmp_path):
        """compute_and_record_report_hash computes correct SHA-256 and stores it."""
        report_content = b"# Daily Portfolio Report\n## Executive Summary\nContent here.\n"
        report_path = tmp_path / "daily_report.md"
        report_path.write_bytes(report_content)

        ctx = RunContext(
            run_id="hash-test-001",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        result = ctx.compute_and_record_report_hash(str(report_path))

        expected_hash = hashlib.sha256(report_content).hexdigest()
        assert result == expected_hash
        assert ctx.report_hash == expected_hash
        assert len(ctx.report_hash) == 64

    def test_report_hash_persisted_in_yaml(self, tmp_path):
        """Report hash is included in persisted RunContext YAML."""
        report_content = b"Test report content"
        report_path = tmp_path / "daily_report.md"
        report_path.write_bytes(report_content)

        ctx = RunContext(
            run_id="hash-persist-test",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )
        ctx.compute_and_record_report_hash(str(report_path))

        yaml_path = ctx.persist(str(tmp_path / "output"))
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["report_hash"] == hashlib.sha256(report_content).hexdigest()

    def test_report_hash_raises_for_missing_file(self):
        """compute_and_record_report_hash raises FileNotFoundError for missing file."""
        ctx = RunContext(
            run_id="missing-file-test",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        with pytest.raises(FileNotFoundError):
            ctx.compute_and_record_report_hash("/nonexistent/daily_report.md")

    def test_report_hash_deterministic_for_same_content(self, tmp_path):
        """Same report content always produces the same hash."""
        content = b"Deterministic content for hash test"
        report1 = tmp_path / "report1.md"
        report2 = tmp_path / "report2.md"
        report1.write_bytes(content)
        report2.write_bytes(content)

        ctx1 = RunContext(
            run_id="det-hash-1",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )
        ctx2 = RunContext(
            run_id="det-hash-2",
            timestamp="2026-05-26T08:00:00Z",
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        hash1 = ctx1.compute_and_record_report_hash(str(report1))
        hash2 = ctx2.compute_and_record_report_hash(str(report2))

        assert hash1 == hash2
