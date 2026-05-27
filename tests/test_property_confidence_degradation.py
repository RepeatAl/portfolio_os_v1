"""Property-based tests for Confidence Degradation Computation.

**Validates: Requirements 11.3, 19.3**

Tests that for any N missing categories (0-14), confidence = max(floor, ceiling - penalty × N).
Hypothesis generates random N values and custom policy parameters; verifies formula holds
and result is within [0, 50] for default policy.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from runtime.confidence_policy import ConfidenceDegradationPolicy


# Strategy: generate missing category count in valid range [0, 14]
missing_category_count_strategy = st.integers(min_value=0, max_value=14)

# Strategy: generate custom policy parameters
custom_ceiling_strategy = st.integers(min_value=1, max_value=100)
custom_penalty_strategy = st.integers(min_value=1, max_value=50)
custom_floor_strategy = st.integers(min_value=0, max_value=50)


class TestConfidenceDegradationProperties:
    """Property-based tests for ConfidenceDegradationPolicy.compute()."""

    @given(n=missing_category_count_strategy)
    @settings(max_examples=200)
    def test_default_policy_formula(self, n: int) -> None:
        """Property 1: For default policy, compute(N) == max(0, 50 - 10*N) for any N in [0, 14].

        **Validates: Requirements 11.3, 19.3**

        The default policy uses base_ceiling=50, penalty_per_missing_category=10,
        minimum_floor=0. The formula must hold exactly.
        """
        policy = ConfidenceDegradationPolicy()
        result = policy.compute(n)
        expected = max(0, 50 - 10 * n)

        assert result == expected, (
            f"Default policy formula violated: compute({n}) = {result}, "
            f"expected max(0, 50 - 10*{n}) = {expected}"
        )

    @given(n=missing_category_count_strategy)
    @settings(max_examples=200)
    def test_result_always_gte_minimum_floor(self, n: int) -> None:
        """Property 2: Result is always >= minimum_floor.

        **Validates: Requirements 11.3, 19.3**

        For any number of missing categories, the computed confidence
        never drops below the policy's minimum_floor.
        """
        policy = ConfidenceDegradationPolicy()
        result = policy.compute(n)

        assert result >= policy.minimum_floor, (
            f"Floor violation: compute({n}) = {result}, "
            f"but minimum_floor = {policy.minimum_floor}"
        )

    @given(n=missing_category_count_strategy)
    @settings(max_examples=200)
    def test_result_always_lte_base_ceiling(self, n: int) -> None:
        """Property 3: Result is always <= base_ceiling.

        **Validates: Requirements 11.3, 19.3**

        For any number of missing categories, the computed confidence
        never exceeds the policy's base_ceiling.
        """
        policy = ConfidenceDegradationPolicy()
        result = policy.compute(n)

        assert result <= policy.base_ceiling, (
            f"Ceiling violation: compute({n}) = {result}, "
            f"but base_ceiling = {policy.base_ceiling}"
        )

    @given(data=st.data())
    @settings(max_examples=300)
    def test_monotonically_non_increasing(self, data: st.DataObject) -> None:
        """Property 4: Result is monotonically non-increasing as N increases.

        **Validates: Requirements 11.3, 19.3**

        For any two values n1 <= n2, compute(n1) >= compute(n2).
        More missing categories never increases confidence.
        """
        n1 = data.draw(st.integers(min_value=0, max_value=13), label="n1")
        n2 = data.draw(st.integers(min_value=n1, max_value=14), label="n2")

        policy = ConfidenceDegradationPolicy()
        result_n1 = policy.compute(n1)
        result_n2 = policy.compute(n2)

        assert result_n1 >= result_n2, (
            f"Monotonicity violated: compute({n1}) = {result_n1} < "
            f"compute({n2}) = {result_n2}, but n1 <= n2"
        )

    @given(ceiling=custom_ceiling_strategy, penalty=custom_penalty_strategy, floor=custom_floor_strategy)
    @settings(max_examples=200)
    def test_compute_zero_always_equals_base_ceiling(
        self, ceiling: int, penalty: int, floor: int
    ) -> None:
        """Property 5: compute(0) always equals base_ceiling.

        **Validates: Requirements 11.3, 19.3**

        With zero missing categories, no penalty is applied, so the result
        equals the base_ceiling (assuming floor <= ceiling).
        """
        # Ensure floor <= ceiling for a valid policy
        actual_floor = min(floor, ceiling)
        policy = ConfidenceDegradationPolicy(
            base_ceiling=ceiling,
            penalty_per_missing_category=penalty,
            minimum_floor=actual_floor,
        )
        result = policy.compute(0)

        assert result == ceiling, (
            f"compute(0) should equal base_ceiling={ceiling}, got {result}"
        )

    @given(
        ceiling=custom_ceiling_strategy,
        penalty=custom_penalty_strategy,
        floor=custom_floor_strategy,
        n=st.integers(min_value=0, max_value=14),
    )
    @settings(max_examples=500)
    def test_custom_policy_formula_holds(
        self, ceiling: int, penalty: int, floor: int, n: int
    ) -> None:
        """Property 6: For custom policies, formula max(floor, ceiling - penalty*N) always holds.

        **Validates: Requirements 11.3, 19.3**

        For any valid policy parameters and any N, the compute function
        returns exactly max(minimum_floor, base_ceiling - penalty_per_missing_category * N).
        """
        # Ensure floor <= ceiling for a valid policy
        actual_floor = min(floor, ceiling)
        policy = ConfidenceDegradationPolicy(
            base_ceiling=ceiling,
            penalty_per_missing_category=penalty,
            minimum_floor=actual_floor,
        )
        result = policy.compute(n)
        expected = max(actual_floor, ceiling - penalty * n)

        assert result == expected, (
            f"Custom policy formula violated: compute({n}) = {result}, "
            f"expected max({actual_floor}, {ceiling} - {penalty}*{n}) = {expected}"
        )
