"""Unit tests for runtime_state_model.py.

Validates RuntimeState enum, IntegrityDimension enum, STATE_DIMENSIONS mapping,
and aggregate_pipeline_state() function behavior.
"""

import pytest

from runtime.runtime_state_model import (
    IntegrityDimension,
    RuntimeState,
    STATE_DIMENSIONS,
    aggregate_pipeline_state,
)


class TestRuntimeStateEnum:
    """Tests for RuntimeState StrEnum."""

    def test_has_8_members(self):
        assert len(RuntimeState) == 8

    def test_all_values_are_strings(self):
        for state in RuntimeState:
            assert isinstance(state, str)
            assert isinstance(state.value, str)

    def test_expected_members_exist(self):
        expected = {
            "healthy",
            "degraded",
            "unavailable",
            "invalid",
            "inconsistent",
            "collapsed",
            "deterministic_failure",
            "canonical_break",
        }
        actual = {s.value for s in RuntimeState}
        assert actual == expected

    def test_string_comparison(self):
        assert RuntimeState.HEALTHY == "healthy"
        assert RuntimeState.CANONICAL_BREAK == "canonical_break"


class TestIntegrityDimensionEnum:
    """Tests for IntegrityDimension StrEnum."""

    def test_has_5_members(self):
        assert len(IntegrityDimension) == 5

    def test_expected_dimensions_exist(self):
        expected = {
            "data_availability",
            "structural_validity",
            "runtime_consistency",
            "replay_integrity",
            "chain_integrity",
        }
        actual = {d.value for d in IntegrityDimension}
        assert actual == expected


class TestStateDimensions:
    """Tests for STATE_DIMENSIONS mapping."""

    def test_all_states_have_mapping(self):
        for state in RuntimeState:
            assert state in STATE_DIMENSIONS

    def test_healthy_has_no_dimensions(self):
        assert STATE_DIMENSIONS[RuntimeState.HEALTHY] == []

    def test_degraded_affects_data_availability(self):
        assert STATE_DIMENSIONS[RuntimeState.DEGRADED] == [IntegrityDimension.DATA_AVAILABILITY]

    def test_unavailable_affects_data_availability(self):
        assert STATE_DIMENSIONS[RuntimeState.UNAVAILABLE] == [IntegrityDimension.DATA_AVAILABILITY]

    def test_collapsed_affects_data_availability(self):
        assert STATE_DIMENSIONS[RuntimeState.COLLAPSED] == [IntegrityDimension.DATA_AVAILABILITY]

    def test_invalid_affects_structural_validity(self):
        assert STATE_DIMENSIONS[RuntimeState.INVALID] == [IntegrityDimension.STRUCTURAL_VALIDITY]

    def test_inconsistent_affects_runtime_consistency(self):
        assert STATE_DIMENSIONS[RuntimeState.INCONSISTENT] == [IntegrityDimension.RUNTIME_CONSISTENCY]

    def test_deterministic_failure_affects_replay_integrity(self):
        assert STATE_DIMENSIONS[RuntimeState.DETERMINISTIC_FAILURE] == [IntegrityDimension.REPLAY_INTEGRITY]

    def test_canonical_break_affects_chain_integrity(self):
        assert STATE_DIMENSIONS[RuntimeState.CANONICAL_BREAK] == [IntegrityDimension.CHAIN_INTEGRITY]


class TestAggregatePipelineState:
    """Tests for aggregate_pipeline_state() function."""

    def test_empty_list_returns_healthy(self):
        assert aggregate_pipeline_state([]) == RuntimeState.HEALTHY

    def test_all_healthy_returns_healthy(self):
        states = [RuntimeState.HEALTHY, RuntimeState.HEALTHY, RuntimeState.HEALTHY]
        assert aggregate_pipeline_state(states) == RuntimeState.HEALTHY

    def test_single_degraded_returns_degraded(self):
        states = [RuntimeState.HEALTHY, RuntimeState.DEGRADED]
        assert aggregate_pipeline_state(states) == RuntimeState.DEGRADED

    def test_canonical_break_takes_priority(self):
        states = [RuntimeState.COLLAPSED, RuntimeState.CANONICAL_BREAK, RuntimeState.INVALID]
        assert aggregate_pipeline_state(states) == RuntimeState.CANONICAL_BREAK

    def test_deterministic_failure_takes_priority_over_collapsed(self):
        states = [RuntimeState.COLLAPSED, RuntimeState.DETERMINISTIC_FAILURE]
        assert aggregate_pipeline_state(states) == RuntimeState.DETERMINISTIC_FAILURE

    def test_canonical_break_wins_over_deterministic_failure(self):
        states = [RuntimeState.DETERMINISTIC_FAILURE, RuntimeState.CANONICAL_BREAK]
        assert aggregate_pipeline_state(states) == RuntimeState.CANONICAL_BREAK

    def test_collapsed_over_inconsistent(self):
        states = [RuntimeState.INCONSISTENT, RuntimeState.COLLAPSED]
        assert aggregate_pipeline_state(states) == RuntimeState.COLLAPSED

    def test_inconsistent_over_invalid(self):
        states = [RuntimeState.INVALID, RuntimeState.INCONSISTENT]
        assert aggregate_pipeline_state(states) == RuntimeState.INCONSISTENT

    def test_invalid_over_unavailable(self):
        states = [RuntimeState.UNAVAILABLE, RuntimeState.INVALID]
        assert aggregate_pipeline_state(states) == RuntimeState.INVALID

    def test_unavailable_over_degraded(self):
        states = [RuntimeState.DEGRADED, RuntimeState.UNAVAILABLE]
        assert aggregate_pipeline_state(states) == RuntimeState.UNAVAILABLE

    def test_idempotent_single_state(self):
        for state in RuntimeState:
            assert aggregate_pipeline_state([state]) == state

    def test_idempotent_duplicate_states(self):
        for state in RuntimeState:
            assert aggregate_pipeline_state([state, state, state]) == state
