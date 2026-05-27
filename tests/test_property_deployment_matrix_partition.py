"""Property-based tests for Deployment Matrix Partition Invariant.

**Validates: Requirements 14.2, 14.3**

Tests that each position is assigned to exactly one basket with confidence_level,
semantic_state_refs, and valid temporal_validity. Hypothesis generates random
position lists; verify partition is exhaustive and exclusive.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from runtime.deployment_matrix import (
    DeploymentMatrix,
    PositionAssignment,
    VALID_BASKETS,
)
from runtime.reasoning_object import TemporalValidity


# --- Strategies ---

# Generate valid ISO 8601 UTC timestamps for TemporalValidity
valid_from_strategy = st.just("2026-01-01T00:00:00Z")
valid_until_strategy = st.just("2026-12-31T23:59:59Z")
stale_after_strategy = st.one_of(st.none(), st.just("2026-06-01T00:00:00Z"))

temporal_validity_strategy = st.builds(
    TemporalValidity,
    valid_from=valid_from_strategy,
    valid_until=valid_until_strategy,
    stale_after=stale_after_strategy,
)

basket_strategy = st.sampled_from(sorted(VALID_BASKETS))

semantic_state_ref_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=30,
)

semantic_state_refs_strategy = st.lists(
    semantic_state_ref_strategy, min_size=1, max_size=5
)

confidence_level_strategy = st.integers(min_value=0, max_value=100)

rationale_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=1,
    max_size=100,
)


def position_assignment_strategy(position_id: str) -> st.SearchStrategy[PositionAssignment]:
    """Build a PositionAssignment with a fixed position_id."""
    return st.builds(
        PositionAssignment,
        position_id=st.just(position_id),
        basket=basket_strategy,
        rationale=rationale_strategy,
        semantic_state_refs=semantic_state_refs_strategy,
        confidence_level=confidence_level_strategy,
        temporal_validity=temporal_validity_strategy,
    )


@st.composite
def unique_position_list_strategy(draw: st.DrawFn) -> list[PositionAssignment]:
    """Generate a list of PositionAssignments with unique position_ids."""
    num_positions = draw(st.integers(min_value=1, max_value=20))
    positions: list[PositionAssignment] = []
    for i in range(num_positions):
        position_id = f"POS_{i:04d}"
        pos = draw(position_assignment_strategy(position_id))
        positions.append(pos)
    return positions


class TestDeploymentMatrixPartitionInvariant:
    """Property-based tests for Deployment Matrix Partition Invariant.

    **Validates: Requirements 14.2, 14.3**

    Property 17: Each position is assigned to exactly one basket with
    confidence_level, semantic_state_refs, and valid temporal_validity.
    The partition is exhaustive (all positions accounted for) and exclusive
    (no position in multiple baskets).
    """

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_partition_is_exhaustive(
        self, positions: list[PositionAssignment]
    ) -> None:
        """Every position in the matrix appears in exactly one basket via get_basket().

        **Validates: Requirements 14.2**

        For any list of positions with unique IDs and valid baskets, the union
        of all basket contents equals the full position list (exhaustive partition).
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        # Collect all positions across all baskets
        all_from_baskets: list[PositionAssignment] = []
        for basket_name in VALID_BASKETS:
            all_from_baskets.extend(dm.get_basket(basket_name))

        # Every position must appear in the basket union
        original_ids = {p.position_id for p in positions}
        basket_ids = {p.position_id for p in all_from_baskets}

        assert original_ids == basket_ids, (
            f"Partition is not exhaustive. "
            f"Missing from baskets: {original_ids - basket_ids}. "
            f"Extra in baskets: {basket_ids - original_ids}."
        )

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_partition_is_exclusive(
        self, positions: list[PositionAssignment]
    ) -> None:
        """No position appears in more than one basket (exclusive partition).

        **Validates: Requirements 14.2**

        For any list of positions with unique IDs and valid baskets, no
        position_id appears in more than one basket's get_basket() result.
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        seen_ids: dict[str, str] = {}
        for basket_name in VALID_BASKETS:
            basket_positions = dm.get_basket(basket_name)
            for pos in basket_positions:
                assert pos.position_id not in seen_ids, (
                    f"Position '{pos.position_id}' appears in both "
                    f"'{seen_ids[pos.position_id]}' and '{basket_name}' baskets."
                )
                seen_ids[pos.position_id] = basket_name

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_each_position_has_valid_confidence_level(
        self, positions: list[PositionAssignment]
    ) -> None:
        """Every position has a confidence_level in [0, 100].

        **Validates: Requirements 14.2, 14.3**

        For any generated position list, each position's confidence_level
        is an integer between 0 and 100 inclusive.
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        for pos in dm.positions:
            assert isinstance(pos.confidence_level, int), (
                f"Position '{pos.position_id}' confidence_level is not an integer: "
                f"{type(pos.confidence_level).__name__}"
            )
            assert 0 <= pos.confidence_level <= 100, (
                f"Position '{pos.position_id}' confidence_level={pos.confidence_level} "
                f"is outside [0, 100]."
            )

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_each_position_has_non_empty_semantic_state_refs(
        self, positions: list[PositionAssignment]
    ) -> None:
        """Every position has at least one semantic_state_ref.

        **Validates: Requirements 14.3**

        For any generated position list, each position's semantic_state_refs
        is a non-empty list of non-empty strings.
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        for pos in dm.positions:
            assert isinstance(pos.semantic_state_refs, list), (
                f"Position '{pos.position_id}' semantic_state_refs is not a list."
            )
            assert len(pos.semantic_state_refs) >= 1, (
                f"Position '{pos.position_id}' has empty semantic_state_refs."
            )
            for ref in pos.semantic_state_refs:
                assert isinstance(ref, str) and len(ref) > 0, (
                    f"Position '{pos.position_id}' has invalid semantic_state_ref: {ref!r}"
                )

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_each_position_has_valid_temporal_validity(
        self, positions: list[PositionAssignment]
    ) -> None:
        """Every position has a TemporalValidity with valid_from and valid_until.

        **Validates: Requirements 14.3**

        For any generated position list, each position's temporal_validity
        is a TemporalValidity instance with non-empty valid_from and valid_until.
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        for pos in dm.positions:
            assert isinstance(pos.temporal_validity, TemporalValidity), (
                f"Position '{pos.position_id}' temporal_validity is not a "
                f"TemporalValidity instance: {type(pos.temporal_validity).__name__}"
            )
            assert pos.temporal_validity.valid_from, (
                f"Position '{pos.position_id}' has empty valid_from."
            )
            assert pos.temporal_validity.valid_until, (
                f"Position '{pos.position_id}' has empty valid_until."
            )

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_validate_passes_for_well_formed_matrix(
        self, positions: list[PositionAssignment]
    ) -> None:
        """A well-formed matrix with unique IDs and valid baskets passes validate().

        **Validates: Requirements 14.2, 14.3**

        For any generated position list with unique position_ids and valid
        basket names, DeploymentMatrix.validate() returns an empty error list.
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        errors = dm.validate()
        assert errors == [], (
            f"validate() returned errors for a well-formed matrix: {errors}"
        )

    @given(positions=unique_position_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_basket_count_equals_total_positions(
        self, positions: list[PositionAssignment]
    ) -> None:
        """Sum of positions across all baskets equals total position count.

        **Validates: Requirements 14.2**

        For any generated position list, the total number of positions
        retrieved via get_basket() across all valid baskets equals the
        total number of positions in the matrix.
        """
        dm = DeploymentMatrix(
            positions=positions,
            run_context_id="test-run-001",
        )

        total_from_baskets = sum(
            len(dm.get_basket(basket_name)) for basket_name in VALID_BASKETS
        )

        assert total_from_baskets == len(positions), (
            f"Basket total ({total_from_baskets}) != position count ({len(positions)}). "
            f"Some positions are lost or duplicated in basket retrieval."
        )
