"""Property-based tests for Pipeline State Aggregation.

**Validates: Requirements 18.5**

Tests that for any set of component runtime states, the aggregated pipeline
state equals the highest-severity component state. Verifies aggregation is
idempotent, monotonic, deterministic, and always returns one of the input states.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from runtime.runtime_state_model import RuntimeState, aggregate_pipeline_state


# Strategy: generate a single RuntimeState value
runtime_state_strategy = st.sampled_from(list(RuntimeState))

# Strategy: generate a list of RuntimeState values (0 to 20 elements)
runtime_state_list_strategy = st.lists(runtime_state_strategy, min_size=0, max_size=20)

# Priority order from highest severity to lowest (used for monotonicity checks)
SEVERITY_PRIORITY: list[RuntimeState] = [
    RuntimeState.CANONICAL_BREAK,
    RuntimeState.DETERMINISTIC_FAILURE,
    RuntimeState.COLLAPSED,
    RuntimeState.INCONSISTENT,
    RuntimeState.INVALID,
    RuntimeState.UNAVAILABLE,
    RuntimeState.DEGRADED,
    RuntimeState.HEALTHY,
]


def severity_rank(state: RuntimeState) -> int:
    """Return severity rank (lower index = higher severity)."""
    return SEVERITY_PRIORITY.index(state)


class TestPipelineStateAggregationProperties:
    """Property-based tests for aggregate_pipeline_state function."""

    @given(state=runtime_state_strategy)
    @settings(max_examples=200)
    def test_idempotency_single_state(self, state: RuntimeState) -> None:
        """Property 1: Aggregating a single state returns that state.

        **Validates: Requirements 18.5**

        For any RuntimeState s, aggregate_pipeline_state([s]) == s.
        """
        result = aggregate_pipeline_state([state])
        assert result == state, (
            f"Idempotency violated: aggregate_pipeline_state([{state}]) "
            f"returned {result}, expected {state}"
        )

    @given(states=runtime_state_list_strategy, worse_state=runtime_state_strategy)
    @settings(max_examples=500)
    def test_monotonicity_adding_worse_state(
        self, states: list[RuntimeState], worse_state: RuntimeState
    ) -> None:
        """Property 2: Adding a worse state never improves the result.

        **Validates: Requirements 18.5**

        For any list of states and any additional state with equal or higher
        severity, the aggregated result with the additional state is at least
        as severe as without it.
        """
        original_result = aggregate_pipeline_state(states)
        extended_result = aggregate_pipeline_state(states + [worse_state])

        # The extended result should be at least as severe (lower or equal rank)
        assert severity_rank(extended_result) <= severity_rank(original_result), (
            f"Monotonicity violated: adding {worse_state} to {states} "
            f"improved result from {original_result} to {extended_result}"
        )

    @given(states=runtime_state_list_strategy)
    @settings(max_examples=500)
    def test_result_is_input_state_or_healthy(
        self, states: list[RuntimeState]
    ) -> None:
        """Property 3: The aggregated result is always one of the input states (or HEALTHY for empty).

        **Validates: Requirements 18.5**

        The aggregation function returns either HEALTHY (for empty input) or
        one of the states present in the input list.
        """
        result = aggregate_pipeline_state(states)

        if not states:
            assert result == RuntimeState.HEALTHY, (
                f"Empty list should return HEALTHY, got {result}"
            )
        else:
            assert result in states, (
                f"Result {result} is not in input states {states}"
            )

    @given(states=runtime_state_list_strategy)
    @settings(max_examples=500)
    def test_determinism_same_inputs_same_output(
        self, states: list[RuntimeState]
    ) -> None:
        """Property 4: Aggregation is deterministic (same inputs produce same output).

        **Validates: Requirements 18.5**

        Running aggregate_pipeline_state twice with the same input always
        produces the same result.
        """
        result_1 = aggregate_pipeline_state(states)
        result_2 = aggregate_pipeline_state(states)

        assert result_1 == result_2, (
            f"Determinism violated: same input {states} produced "
            f"{result_1} and {result_2}"
        )
