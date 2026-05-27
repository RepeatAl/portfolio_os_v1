"""Property-based tests for Semantic Delta Correctness.

**Validates: Requirements 12.3, 12.5**

Tests that deltas correctly identify additions, removals, and changes between
consecutive snapshots. Hypothesis generates pairs of state lists; verify delta
captures all differences. Also verifies that identical states produce no delta
entries and that the union of additions + removals + unchanged accounts for all
signal_ids.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from runtime.run_context import RunContext
from runtime.semantic_state_store import SemanticStateStore


# Strategy: generate a semantic state dict with a unique signal_id and a value
def _semantic_state_strategy(signal_id_strategy=None):
    """Generate a single semantic state dict."""
    if signal_id_strategy is None:
        signal_id_strategy = st.text(
            alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
            min_size=3,
            max_size=20,
        )
    return st.fixed_dictionaries({
        "signal_id": signal_id_strategy,
        "category": st.sampled_from([
            "allocation", "attribution", "correlation", "cross_asset",
            "divergence", "early_warning", "flow", "liquidity",
            "market_breadth", "narrative_dependency", "regime",
            "relative_strength", "scenario", "portfolio_memory",
        ]),
        "meaning": st.text(min_size=5, max_size=50),
        "confidence": st.integers(min_value=0, max_value=100),
    })



# Strategy: generate a pair of state lists with controlled overlap
@st.composite
def _overlapping_state_pairs(draw):
    """Generate two state lists with some overlapping and some non-overlapping signal_ids.

    Returns (old_states, new_states) where:
    - Some signal_ids appear only in old (removals)
    - Some signal_ids appear only in new (additions)
    - Some signal_ids appear in both with same values (unchanged)
    - Some signal_ids appear in both with different values (changes)
    """
    # Generate a pool of unique signal_ids
    num_ids = draw(st.integers(min_value=1, max_value=12))
    signal_ids = draw(
        st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
                min_size=3,
                max_size=20,
            ),
            min_size=num_ids,
            max_size=num_ids,
            unique=True,
        )
    )

    # Partition signal_ids into: only_old, only_new, shared
    old_ids = set()
    new_ids = set()
    for sid in signal_ids:
        choice = draw(st.sampled_from(["old_only", "new_only", "both"]))
        if choice == "old_only":
            old_ids.add(sid)
        elif choice == "new_only":
            new_ids.add(sid)
        else:
            old_ids.add(sid)
            new_ids.add(sid)

    # Ensure at least one state in either list
    if not old_ids and not new_ids:
        old_ids.add(signal_ids[0])

    # Generate states for old list
    old_states = []
    for sid in sorted(old_ids):
        state = draw(_semantic_state_strategy(st.just(sid)))
        old_states.append(state)

    # Generate states for new list
    new_states = []
    for sid in sorted(new_ids):
        if sid in old_ids:
            # Shared id: sometimes same value, sometimes different
            mutate = draw(st.booleans())
            if mutate:
                # Generate a different state for this signal_id
                state = draw(_semantic_state_strategy(st.just(sid)))
                new_states.append(state)
            else:
                # Copy the old state exactly (unchanged)
                old_state = next(s for s in old_states if s["signal_id"] == sid)
                new_states.append(dict(old_state))
        else:
            # New-only id
            state = draw(_semantic_state_strategy(st.just(sid)))
            new_states.append(state)

    return old_states, new_states


def _make_run_context(run_id: str) -> RunContext:
    """Create a minimal RunContext for testing."""
    return RunContext(
        run_id=run_id,
        timestamp="2026-01-01T00:00:00Z",
        data_sources=[],
        schema_version="1.0.0",
        pipeline_state="healthy",
        report_hash=None,
    )


class TestSemanticDeltaCorrectnessProperties:
    """Property-based tests for semantic delta correctness."""

    @given(data=_overlapping_state_pairs())
    @settings(max_examples=200, deadline=None)
    def test_additions_are_new_signal_ids(self, data: tuple[list[dict], list[dict]]) -> None:
        """Property 1: States present in new but not old are recorded as additions.

        **Validates: Requirements 12.3, 12.5**

        For any pair of state lists, signal_ids that appear in the new list
        but not in the old list must appear in the delta's additions.
        """
        old_states, new_states = data

        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=str(Path(tmp_dir) / "state"))

            # Save old snapshot first
            ctx_old = _make_run_context("run-old")
            store.save_snapshot(old_states, ctx_old)

            # Save new snapshot (triggers delta computation)
            ctx_new = _make_run_context("run-new")
            store.save_snapshot(new_states, ctx_new)

            # Retrieve delta for the new run
            delta = store.get_delta("run-new")

            old_ids = {s["signal_id"] for s in old_states if "signal_id" in s}
            new_ids = {s["signal_id"] for s in new_states if "signal_id" in s}
            expected_additions = new_ids - old_ids

            actual_addition_ids = {a["signal_id"] for a in delta["additions"]}

            assert expected_additions == actual_addition_ids, (
                f"Expected additions {expected_additions}, got {actual_addition_ids}. "
                f"Old IDs: {old_ids}, New IDs: {new_ids}"
            )

    @given(data=_overlapping_state_pairs())
    @settings(max_examples=200, deadline=None)
    def test_removals_are_old_signal_ids(self, data: tuple[list[dict], list[dict]]) -> None:
        """Property 2: States present in old but not new are recorded as removals.

        **Validates: Requirements 12.3, 12.5**

        For any pair of state lists, signal_ids that appear in the old list
        but not in the new list must appear in the delta's removals.
        """
        old_states, new_states = data

        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=str(Path(tmp_dir) / "state"))

            ctx_old = _make_run_context("run-old")
            store.save_snapshot(old_states, ctx_old)

            ctx_new = _make_run_context("run-new")
            store.save_snapshot(new_states, ctx_new)

            delta = store.get_delta("run-new")

            old_ids = {s["signal_id"] for s in old_states if "signal_id" in s}
            new_ids = {s["signal_id"] for s in new_states if "signal_id" in s}
            expected_removals = old_ids - new_ids

            actual_removal_ids = {r["signal_id"] for r in delta["removals"]}

            assert expected_removals == actual_removal_ids, (
                f"Expected removals {expected_removals}, got {actual_removal_ids}. "
                f"Old IDs: {old_ids}, New IDs: {new_ids}"
            )

    @given(data=_overlapping_state_pairs())
    @settings(max_examples=200, deadline=None)
    def test_changes_are_modified_shared_ids(self, data: tuple[list[dict], list[dict]]) -> None:
        """Property 3: States present in both but with different values are recorded as changes.

        **Validates: Requirements 12.3, 12.5**

        For any pair of state lists, signal_ids that appear in both lists
        but with different values must appear in the delta's changes.
        """
        old_states, new_states = data

        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=str(Path(tmp_dir) / "state"))

            ctx_old = _make_run_context("run-old")
            store.save_snapshot(old_states, ctx_old)

            ctx_new = _make_run_context("run-new")
            store.save_snapshot(new_states, ctx_new)

            delta = store.get_delta("run-new")

            old_by_id = {s["signal_id"]: s for s in old_states if "signal_id" in s}
            new_by_id = {s["signal_id"]: s for s in new_states if "signal_id" in s}
            shared_ids = set(old_by_id.keys()) & set(new_by_id.keys())

            expected_changes = {
                sid for sid in shared_ids if old_by_id[sid] != new_by_id[sid]
            }

            actual_change_ids = {c["signal_id"] for c in delta["changes"]}

            assert expected_changes == actual_change_ids, (
                f"Expected changes {expected_changes}, got {actual_change_ids}. "
                f"Shared IDs: {shared_ids}"
            )

    @given(data=_overlapping_state_pairs())
    @settings(max_examples=200, deadline=None)
    def test_identical_values_produce_no_delta(self, data: tuple[list[dict], list[dict]]) -> None:
        """Property 4: States present in both with identical values produce no delta entry.

        **Validates: Requirements 12.3, 12.5**

        For any pair of state lists, signal_ids that appear in both lists
        with identical values must NOT appear in additions, removals, or changes.
        """
        old_states, new_states = data

        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=str(Path(tmp_dir) / "state"))

            ctx_old = _make_run_context("run-old")
            store.save_snapshot(old_states, ctx_old)

            ctx_new = _make_run_context("run-new")
            store.save_snapshot(new_states, ctx_new)

            delta = store.get_delta("run-new")

            old_by_id = {s["signal_id"]: s for s in old_states if "signal_id" in s}
            new_by_id = {s["signal_id"]: s for s in new_states if "signal_id" in s}
            shared_ids = set(old_by_id.keys()) & set(new_by_id.keys())

            unchanged_ids = {
                sid for sid in shared_ids if old_by_id[sid] == new_by_id[sid]
            }

            all_delta_ids = (
                {a["signal_id"] for a in delta["additions"]}
                | {r["signal_id"] for r in delta["removals"]}
                | {c["signal_id"] for c in delta["changes"]}
            )

            overlap = unchanged_ids & all_delta_ids
            assert not overlap, (
                f"Unchanged signal_ids should not appear in delta, but found: {overlap}"
            )

    @given(data=_overlapping_state_pairs())
    @settings(max_examples=200, deadline=None)
    def test_delta_accounts_for_all_signal_ids(self, data: tuple[list[dict], list[dict]]) -> None:
        """Property 5: Union of additions + removals + unchanged accounts for all signal_ids.

        **Validates: Requirements 12.3, 12.5**

        For any pair of state lists, the union of all signal_ids in additions,
        removals, changes, and unchanged must equal the union of all signal_ids
        across both old and new state lists.
        """
        old_states, new_states = data

        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SemanticStateStore(state_dir=str(Path(tmp_dir) / "state"))

            ctx_old = _make_run_context("run-old")
            store.save_snapshot(old_states, ctx_old)

            ctx_new = _make_run_context("run-new")
            store.save_snapshot(new_states, ctx_new)

            delta = store.get_delta("run-new")

            old_ids = {s["signal_id"] for s in old_states if "signal_id" in s}
            new_ids = {s["signal_id"] for s in new_states if "signal_id" in s}
            all_ids = old_ids | new_ids

            # Compute unchanged: shared ids with identical values
            old_by_id = {s["signal_id"]: s for s in old_states if "signal_id" in s}
            new_by_id = {s["signal_id"]: s for s in new_states if "signal_id" in s}
            shared_ids = old_ids & new_ids
            unchanged_ids = {
                sid for sid in shared_ids if old_by_id[sid] == new_by_id[sid]
            }

            addition_ids = {a["signal_id"] for a in delta["additions"]}
            removal_ids = {r["signal_id"] for r in delta["removals"]}
            change_ids = {c["signal_id"] for c in delta["changes"]}

            accounted_ids = addition_ids | removal_ids | change_ids | unchanged_ids

            assert accounted_ids == all_ids, (
                f"Delta does not account for all signal_ids. "
                f"All IDs: {all_ids}, Accounted: {accounted_ids}, "
                f"Missing: {all_ids - accounted_ids}, Extra: {accounted_ids - all_ids}"
            )
