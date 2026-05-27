"""Unit tests for Run Context module.

Tests creation, validation, persistence, and loading of RunContext
and DataSourceReference dataclasses.
"""

import hashlib
import os
import tempfile
import uuid

import pytest
import yaml

from runtime.run_context import DataSourceReference, RunContext
from runtime.runtime_state_model import RuntimeState


class TestDataSourceReference:
    """Tests for DataSourceReference dataclass."""

    def test_create_available_source(self):
        ref = DataSourceReference(
            file_path="data/input.xlsx",
            content_hash="abc123",
            status="available",
        )
        assert ref.file_path == "data/input.xlsx"
        assert ref.content_hash == "abc123"
        assert ref.status == "available"

    def test_create_unavailable_source(self):
        ref = DataSourceReference(
            file_path="missing/file.csv",
            content_hash="",
            status="unavailable",
        )
        assert ref.status == "unavailable"
        assert ref.content_hash == ""


class TestRunContextCreate:
    """Tests for RunContext.create() class method."""

    def test_create_with_existing_files(self, tmp_path):
        file1 = tmp_path / "input1.txt"
        file1.write_text("hello world")
        file2 = tmp_path / "input2.txt"
        file2.write_text("test data")

        ctx = RunContext.create([str(file1), str(file2)])

        assert uuid.UUID(ctx.run_id, version=4)
        assert ctx.timestamp.endswith("Z")
        assert len(ctx.data_sources) == 2
        assert ctx.schema_version == "1.0.0"
        assert ctx.pipeline_state == RuntimeState.HEALTHY
        assert ctx.report_hash is None

    def test_create_computes_correct_hash(self, tmp_path):
        content = b"deterministic content"
        file1 = tmp_path / "data.bin"
        file1.write_bytes(content)

        expected_hash = hashlib.sha256(content).hexdigest()
        ctx = RunContext.create([str(file1)])

        assert ctx.data_sources[0].content_hash == expected_hash
        assert ctx.data_sources[0].status == "available"

    def test_create_marks_missing_files_unavailable(self):
        ctx = RunContext.create(["/nonexistent/path/file.txt"])

        assert len(ctx.data_sources) == 1
        assert ctx.data_sources[0].status == "unavailable"
        assert ctx.data_sources[0].content_hash == ""

    def test_create_handles_mixed_files(self, tmp_path):
        existing = tmp_path / "exists.txt"
        existing.write_text("data")

        ctx = RunContext.create([str(existing), "/no/such/file.csv"])

        assert ctx.data_sources[0].status == "available"
        assert ctx.data_sources[1].status == "unavailable"

    def test_create_generates_unique_run_ids(self, tmp_path):
        file1 = tmp_path / "f.txt"
        file1.write_text("x")

        ctx1 = RunContext.create([str(file1)])
        ctx2 = RunContext.create([str(file1)])

        assert ctx1.run_id != ctx2.run_id

    def test_create_timestamp_is_utc_iso8601(self, tmp_path):
        file1 = tmp_path / "f.txt"
        file1.write_text("x")

        ctx = RunContext.create([str(file1)])

        # ISO 8601 UTC format: YYYY-MM-DDTHH:MM:SSZ
        assert "T" in ctx.timestamp
        assert ctx.timestamp.endswith("Z")
        # Verify parseable
        from datetime import datetime
        dt = datetime.fromisoformat(ctx.timestamp.replace("Z", "+00:00"))
        assert dt.tzinfo is not None


class TestRunContextValidateSource:
    """Tests for RunContext.validate_source() method."""

    def test_validate_unchanged_file(self, tmp_path):
        file1 = tmp_path / "stable.txt"
        file1.write_text("unchanged content")

        ctx = RunContext.create([str(file1)])
        assert ctx.validate_source(str(file1)) is True

    def test_validate_modified_file(self, tmp_path):
        file1 = tmp_path / "mutable.txt"
        file1.write_text("original")

        ctx = RunContext.create([str(file1)])

        # Modify file after snapshot
        file1.write_text("modified")
        assert ctx.validate_source(str(file1)) is False

    def test_validate_deleted_file(self, tmp_path):
        file1 = tmp_path / "temp.txt"
        file1.write_text("temporary")

        ctx = RunContext.create([str(file1)])

        # Delete file after snapshot
        file1.unlink()
        assert ctx.validate_source(str(file1)) is False

    def test_validate_unknown_file(self, tmp_path):
        file1 = tmp_path / "known.txt"
        file1.write_text("known")

        ctx = RunContext.create([str(file1)])
        assert ctx.validate_source("/unknown/path.txt") is False

    def test_validate_unavailable_source(self):
        ctx = RunContext.create(["/nonexistent/file.txt"])
        assert ctx.validate_source("/nonexistent/file.txt") is False


class TestRunContextPersistAndLoad:
    """Tests for RunContext.persist() and RunContext.load() round-trip."""

    def test_persist_creates_yaml_file(self, tmp_path):
        file1 = tmp_path / "input.txt"
        file1.write_text("test")

        ctx = RunContext.create([str(file1)])
        output_dir = str(tmp_path / "output")
        result_path = ctx.persist(output_dir)

        assert os.path.exists(result_path)
        assert result_path.endswith("_run_context.yaml")
        assert ctx.run_id in result_path

    def test_persist_creates_output_directory(self, tmp_path):
        ctx = RunContext.create([])
        output_dir = str(tmp_path / "nested" / "output")
        ctx.persist(output_dir)

        assert os.path.isdir(output_dir)

    def test_persist_writes_valid_yaml(self, tmp_path):
        file1 = tmp_path / "data.txt"
        file1.write_text("content")

        ctx = RunContext.create([str(file1)])
        result_path = ctx.persist(str(tmp_path / "out"))

        with open(result_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["run_id"] == ctx.run_id
        assert data["timestamp"] == ctx.timestamp
        assert data["schema_version"] == "1.0.0"
        assert data["pipeline_state"] == RuntimeState.HEALTHY
        assert len(data["data_sources"]) == 1

    def test_load_reconstructs_context(self, tmp_path):
        file1 = tmp_path / "source.txt"
        file1.write_text("source data")

        original = RunContext.create([str(file1)])
        persisted_path = original.persist(str(tmp_path / "out"))

        loaded = RunContext.load(persisted_path)

        assert loaded.run_id == original.run_id
        assert loaded.timestamp == original.timestamp
        assert loaded.schema_version == original.schema_version
        assert loaded.pipeline_state == original.pipeline_state
        assert loaded.report_hash == original.report_hash
        assert len(loaded.data_sources) == len(original.data_sources)
        assert loaded.data_sources[0].file_path == original.data_sources[0].file_path
        assert loaded.data_sources[0].content_hash == original.data_sources[0].content_hash
        assert loaded.data_sources[0].status == original.data_sources[0].status

    def test_load_with_report_hash(self, tmp_path):
        ctx = RunContext.create([])
        ctx.report_hash = "abc123def456"
        persisted_path = ctx.persist(str(tmp_path / "out"))

        loaded = RunContext.load(persisted_path)
        assert loaded.report_hash == "abc123def456"

    def test_load_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            RunContext.load("/nonexistent/path.yaml")

    def test_round_trip_with_multiple_sources(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f1.write_text("aaa")
        f2 = tmp_path / "b.txt"
        f2.write_text("bbb")

        original = RunContext.create([str(f1), str(f2), "/missing.txt"])
        path = original.persist(str(tmp_path / "out"))
        loaded = RunContext.load(path)

        assert len(loaded.data_sources) == 3
        assert loaded.data_sources[0].status == "available"
        assert loaded.data_sources[1].status == "available"
        assert loaded.data_sources[2].status == "unavailable"
