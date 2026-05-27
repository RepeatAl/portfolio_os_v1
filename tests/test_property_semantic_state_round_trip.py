"""Property-based tests for Semantic State Persistence Round-Trip.

**Validates: Requirements 12.1, 12.2**

Tests that persisting and loading states returns structurally identical results.
Hypothesis generates random semantic state lists; verify save→load round-trip
preserves all fields. Also verifies run_id consistency, latest pointer correctness
after multiple saves, and historical snapshot accessibility.
"""

from __future__ import annotations

import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from runtime.run_context import RunContext
from runtime.semantic_state_store import SemanticStateStore


# --- Strategies ---

# Strategy: generate a valid signal_id (unique identifier string)
signal_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
    min_size=3,
    max_size=30,
).filter(lambda s: len(s.strip()) >= 3)

# Strategy: generate a category string
category_strategy = st.sampled_from([
    "allocation",
    "attribution",
    "correlation",
    "cross_asset",
    "divergence",
    "early_warning",
    "flow",
    "liquidity",
    "market_breadth",
    "narrative_dependency",
    "regime",
    "relative_strength",
    "scenario",
    "portfolio_memory",
])

# Strategy: generate a meaning string
meaning_strategy = st.text(min_size=5, max_size=100).filter(lambda s: len(s.strip()) >= 5)

# Strategy: generate a source string
source_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_"),
    min_size=3,
    max_size=30,
).filter(lambda s: len(s.strip()) >= 3)

# Strategy: generate a value (numeric or string)
value_strategy = st.one_of(
    st.integers(min_value=-1000, max_value=1000),
    st.floats(min_value=-1000.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
    st.text(min_size=1, max_size=50).filter(lambda s: len(s.strip()) >= 1),
)


def semantic_state_strategy():
    """Generate a single semantic state dict with required fields."""
    return st.fixed_dictionaries({
        "signal_id": signal_id_strategy,
        "category": category_strategy,
        "meaning": meaning_strategy,
        "source": source_strategy,
        "value": value_strategy,
    })


# Strategy: generate a list of semantic states with unique signal_ids
def unique_semantic_states_strategy(min_size=1, max_size=10):
    """Generate a list of semantic states with unique signal_ids."""
    return st.lists(
        semantic_state_strategy(),
        min_size=min_size,
        max_size=max_size,
    ).filter(
        lambda states: len({s["signal_id"] for s in states}) == len(states)
    )


def make_run_context(run_id: str | None = None) -> RunContext:
    """Create a minimal RunContext for testing."""
    return RunContext(
        run_id=run_id or str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        data_sources=[],
        schema_version="1.0.0",
        pipeline_state="healthy",
        report_hash=None,
    )



class TestSemanticStatePersistenceRoundTrip:
    """Property-based tests for Semantic State Store persistence round-trip."""

    @given(states=unique_semantic_states_strategy(min_size=1, max_size=10))
    @settings(max_examples=200, deadline=None)
    def test_save_load_round_trip_preserves_all_fields(self, states: list[dict]) -> None:
        """Property 1: save_snapshot → load_snapshot returns identical states.

        **Validates: Requirements 12.1, 12.2**

        For any list of semantic states (dicts with signal_id), persisting via
        save_snapshot and loading via load_snapshot returns structurally identical
        states with all fields preserved.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=tmp_dir)
            run_ctx = make_run_context()

            # Save states
            store.save_snapshot(states, run_ctx)

            # Load states back
            loaded_states, loaded_run_id = store.load_snapshot()

            # All states must be preserved identically
            assert len(loaded_states) == len(states), (
                f"State count mismatch: saved {len(states)}, loaded {len(loaded_states)}"
            )

            # Compare each state by signal_id
            saved_by_id = {s["signal_id"]: s for s in states}
            loaded_by_id = {s["signal_id"]: s for s in loaded_states}

            assert set(saved_by_id.keys()) == set(loaded_by_id.keys()), (
                f"Signal IDs mismatch: saved {set(saved_by_id.keys())}, "
                f"loaded {set(loaded_by_id.keys())}"
            )

            for signal_id in saved_by_id:
                assert saved_by_id[signal_id] == loaded_by_id[signal_id], (
                    f"State mismatch for signal_id '{signal_id}': "
                    f"saved {saved_by_id[signal_id]}, loaded {loaded_by_id[signal_id]}"
                )

    @given(states=unique_semantic_states_strategy(min_size=1, max_size=10))
    @settings(max_examples=200, deadline=None)
    def test_load_returns_matching_run_id(self, states: list[dict]) -> None:
        """Property 2: The run_id returned by load_snapshot matches the run_context used in save_snapshot.

        **Validates: Requirements 12.1, 12.2**

        For any list of semantic states, the run_id returned by load_snapshot
        must match the run_id of the RunContext used during save_snapshot.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=tmp_dir)
            run_ctx = make_run_context()

            # Save states
            store.save_snapshot(states, run_ctx)

            # Load and verify run_id
            _, loaded_run_id = store.load_snapshot()

            assert loaded_run_id == run_ctx.run_id, (
                f"Run ID mismatch: expected {run_ctx.run_id}, got {loaded_run_id}"
            )

    @given(
        states_first=unique_semantic_states_strategy(min_size=1, max_size=5),
        states_second=unique_semantic_states_strategy(min_size=1, max_size=5),
    )
    @settings(max_examples=100, deadline=None)
    def test_multiple_saves_preserve_latest(
        self, states_first: list[dict], states_second: list[dict]
    ) -> None:
        """Property 3: Multiple consecutive saves always preserve the latest states.

        **Validates: Requirements 12.1, 12.2**

        After two consecutive saves, load_snapshot returns the states from the
        second (most recent) save, not the first. The latest pointer is correct.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=tmp_dir)
            run_ctx_1 = make_run_context()
            run_ctx_2 = make_run_context()

            # Save first batch
            store.save_snapshot(states_first, run_ctx_1)

            # Save second batch (overwrites latest pointer)
            store.save_snapshot(states_second, run_ctx_2)

            # Load should return the second (latest) states
            loaded_states, loaded_run_id = store.load_snapshot()

            assert loaded_run_id == run_ctx_2.run_id, (
                f"Latest pointer incorrect: expected {run_ctx_2.run_id}, got {loaded_run_id}"
            )

            loaded_by_id = {s["signal_id"]: s for s in loaded_states}
            expected_by_id = {s["signal_id"]: s for s in states_second}

            assert set(loaded_by_id.keys()) == set(expected_by_id.keys()), (
                f"Latest states signal_ids mismatch: "
                f"expected {set(expected_by_id.keys())}, got {set(loaded_by_id.keys())}"
            )

            for signal_id in expected_by_id:
                assert loaded_by_id[signal_id] == expected_by_id[signal_id], (
                    f"Latest state mismatch for '{signal_id}'"
                )

    @given(
        states_first=unique_semantic_states_strategy(min_size=1, max_size=5),
        states_second=unique_semantic_states_strategy(min_size=1, max_size=5),
    )
    @settings(max_examples=100, deadline=None)
    def test_historical_snapshots_remain_accessible(
        self, states_first: list[dict], states_second: list[dict]
    ) -> None:
        """Property 4: Historical snapshots remain accessible after new saves.

        **Validates: Requirements 12.1, 12.2**

        After saving two snapshots, the first snapshot is still accessible
        via load_historical() using its original run_id.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=tmp_dir)
            run_ctx_1 = make_run_context()
            run_ctx_2 = make_run_context()

            # Save first batch
            store.save_snapshot(states_first, run_ctx_1)

            # Save second batch
            store.save_snapshot(states_second, run_ctx_2)

            # Historical snapshot for first run should still be accessible
            historical_states, historical_run_id = store.load_historical(run_ctx_1.run_id)

            assert historical_run_id == run_ctx_1.run_id, (
                f"Historical run_id mismatch: expected {run_ctx_1.run_id}, "
                f"got {historical_run_id}"
            )

            historical_by_id = {s["signal_id"]: s for s in historical_states}
            expected_by_id = {s["signal_id"]: s for s in states_first}

            assert set(historical_by_id.keys()) == set(expected_by_id.keys()), (
                f"Historical states signal_ids mismatch: "
                f"expected {set(expected_by_id.keys())}, got {set(historical_by_id.keys())}"
            )

            for signal_id in expected_by_id:
                assert historical_by_id[signal_id] == expected_by_id[signal_id], (
                    f"Historical state mismatch for '{signal_id}'"
                )
