"""Unit tests for SemanticStateStore.

Tests immutable snapshot persistence, delta computation, historical replay,
and graceful failure handling.

Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from runtime.run_context import RunContext
from runtime.semantic_state_store import SemanticStateStore


@pytest.fixture
def tmp_state_dir(tmp_path):
    """Provide a temporary state directory."""
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    return str(state_dir) + "/"


@pytest.fixture
def store(tmp_state_dir):
    """Provide a SemanticStateStore with a temporary directory."""
    return SemanticStateStore(state_dir=tmp_state_dir)


@pytest.fixture
def sample_states():
    """Provide sample semantic states."""
    return [
        {
            "signal_id": "defense_dependency_elevated",
            "category": "narrative_dependency",
            "meaning": "Portfolio depends on defense sector strength.",
            "source": "allocation_engine",
            "value": 30.0,
        },
        {
            "signal_id": "concentration_risk_elevated",
            "category": "concentration",
            "meaning": "Defense exposure is structurally elevated.",
            "source": "allocation_engine",
            "value": 30.0,
        },
    ]


@pytest.fixture
def run_context():
    """Provide a RunContext for testing."""
    return RunContext.create(input_files=[])


class TestSaveAndLoadSnapshot:
    """Tests for save_snapshot and load_snapshot."""

    def test_save_creates_immutable_snapshot_file(self, store, sample_states, run_context):
        """Req 12.1: Persist states with run_id and timestamp."""
        store.save_snapshot(sample_states, run_context)

        snapshot_path = Path(store.snapshots_dir) / f"{run_context.run_id}_semantic_snapshot.yaml"
        assert snapshot_path.exists()

        with open(snapshot_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["run_id"] == run_context.run_id
        assert data["timestamp"] == run_context.timestamp
        assert data["states"] == sample_states

    def test_save_updates_latest_pointer(self, store, sample_states, run_context):
        """Req 12.2: Maintain most recent canonical snapshot pointer."""
        store.save_snapshot(sample_states, run_context)

        assert store.latest_pointer_path.exists()
        with open(store.latest_pointer_path, "r") as f:
            pointer = yaml.safe_load(f)

        assert pointer["current_run_id"] == run_context.run_id

    def test_load_snapshot_returns_states_and_run_id(self, store, sample_states, run_context):
        """Req 12.4: Retrieve canonical snapshot without re-running engine."""
        store.save_snapshot(sample_states, run_context)

        loaded_states, loaded_run_id = store.load_snapshot()

        assert loaded_states == sample_states
        assert loaded_run_id == run_context.run_id

    def test_save_does_not_overwrite_previous_snapshot(self, store, sample_states):
        """Hardening 6: Previous snapshots are never destructively overwritten."""
        ctx1 = RunContext.create(input_files=[])
        ctx2 = RunContext.create(input_files=[])

        store.save_snapshot(sample_states, ctx1)
        store.save_snapshot(sample_states, ctx2)

        # Both snapshot files exist
        path1 = Path(store.snapshots_dir) / f"{ctx1.run_id}_semantic_snapshot.yaml"
        path2 = Path(store.snapshots_dir) / f"{ctx2.run_id}_semantic_snapshot.yaml"
        assert path1.exists()
        assert path2.exists()

    def test_latest_pointer_updates_to_newest_run(self, store, sample_states):
        """Req 12.2: Latest pointer supersedes prior snapshot."""
        ctx1 = RunContext.create(input_files=[])
        ctx2 = RunContext.create(input_files=[])

        store.save_snapshot(sample_states, ctx1)
        store.save_snapshot(sample_states, ctx2)

        _, loaded_run_id = store.load_snapshot()
        assert loaded_run_id == ctx2.run_id

    def test_load_snapshot_raises_when_no_pointer(self, store):
        """Req 12.4: FileNotFoundError when no snapshot exists."""
        with pytest.raises(FileNotFoundError):
            store.load_snapshot()


class TestLoadHistorical:
    """Tests for load_historical."""

    def test_load_historical_returns_specific_run(self, store, sample_states):
        """Forensic replay of specific run_id snapshots."""
        ctx1 = RunContext.create(input_files=[])
        ctx2 = RunContext.create(input_files=[])

        states_v1 = sample_states
        states_v2 = [sample_states[0]]  # Only first state

        store.save_snapshot(states_v1, ctx1)
        store.save_snapshot(states_v2, ctx2)

        # Load historical first run
        loaded_states, loaded_run_id = store.load_historical(ctx1.run_id)
        assert loaded_states == states_v1
        assert loaded_run_id == ctx1.run_id

    def test_load_historical_raises_for_unknown_run_id(self, store):
        """FileNotFoundError for non-existent run_id."""
        with pytest.raises(FileNotFoundError):
            store.load_historical("nonexistent-run-id")


class TestDeltaComputation:
    """Tests for delta computation and get_delta."""

    def test_first_run_delta_all_additions(self, store, sample_states, run_context):
        """Req 12.3, 12.5: First run records all states as additions."""
        store.save_snapshot(sample_states, run_context)

        delta = store.get_delta(run_context.run_id)

        assert delta["run_id"] == run_context.run_id
        assert len(delta["additions"]) == 2
        assert len(delta["removals"]) == 0
        assert len(delta["changes"]) == 0

    def test_delta_detects_removals(self, store, sample_states):
        """Req 12.5: Removed states logged with last known value."""
        ctx1 = RunContext.create(input_files=[])
        ctx2 = RunContext.create(input_files=[])

        store.save_snapshot(sample_states, ctx1)
        store.save_snapshot([sample_states[0]], ctx2)  # Remove second state

        delta = store.get_delta(ctx2.run_id)

        assert len(delta["removals"]) == 1
        assert delta["removals"][0]["signal_id"] == "concentration_risk_elevated"
        assert delta["removals"][0]["last_value"] == sample_states[1]

    def test_delta_detects_changes(self, store, sample_states):
        """Req 12.5: Changed states logged with previous and current values."""
        ctx1 = RunContext.create(input_files=[])
        ctx2 = RunContext.create(input_files=[])

        store.save_snapshot(sample_states, ctx1)

        # Modify value of first state
        modified_states = [
            {**sample_states[0], "value": 45.0},
            sample_states[1],
        ]
        store.save_snapshot(modified_states, ctx2)

        delta = store.get_delta(ctx2.run_id)

        assert len(delta["changes"]) == 1
        assert delta["changes"][0]["signal_id"] == "defense_dependency_elevated"
        assert delta["changes"][0]["previous_value"]["value"] == 30.0
        assert delta["changes"][0]["current_value"]["value"] == 45.0

    def test_delta_detects_additions(self, store, sample_states):
        """Req 12.5: Added states logged with new value."""
        ctx1 = RunContext.create(input_files=[])
        ctx2 = RunContext.create(input_files=[])

        store.save_snapshot([sample_states[0]], ctx1)
        store.save_snapshot(sample_states, ctx2)  # Add second state

        delta = store.get_delta(ctx2.run_id)

        assert len(delta["additions"]) == 1
        assert delta["additions"][0]["signal_id"] == "concentration_risk_elevated"

    def test_get_delta_returns_empty_for_unknown_run_id(self, store, sample_states, run_context):
        """get_delta returns empty structure for unknown run_id."""
        store.save_snapshot(sample_states, run_context)

        delta = store.get_delta("unknown-run-id")

        assert delta["run_id"] == "unknown-run-id"
        assert delta["additions"] == []
        assert delta["removals"] == []
        assert delta["changes"] == []

    def test_get_delta_returns_empty_when_no_log_exists(self, store):
        """get_delta returns empty structure when delta log does not exist."""
        delta = store.get_delta("any-run-id")

        assert delta["additions"] == []
        assert delta["removals"] == []
        assert delta["changes"] == []


class TestWriteFailureHandling:
    """Tests for graceful failure handling (Req 12.6)."""

    def test_save_preserves_previous_on_snapshot_write_failure(self, store, sample_states):
        """Req 12.6: Write failure preserves previous snapshot unchanged."""
        ctx1 = RunContext.create(input_files=[])
        store.save_snapshot(sample_states, ctx1)

        # Make snapshots dir read-only to force write failure
        os.chmod(store.snapshots_dir, 0o444)

        ctx2 = RunContext.create(input_files=[])
        try:
            with pytest.raises(OSError):
                store.save_snapshot(sample_states, ctx2)
        finally:
            os.chmod(store.snapshots_dir, 0o755)

        # Previous snapshot still accessible
        loaded_states, loaded_run_id = store.load_snapshot()
        assert loaded_run_id == ctx1.run_id
        assert loaded_states == sample_states
