"""Deployment Matrix schema for the three-basket capital allocation model.

Formalizes the Deployment Matrix as a data structure where each position is
assigned to exactly one basket with confidence, rationale, and temporal validity.

Baskets:
- momentum_core: High-conviction current positions
- diversification_candidates: Positions improving portfolio resilience
- risk_thresholds: Positions requiring monitoring or reduction
- unclassified: Positions that cannot be classified due to insufficient data

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5
"""

from dataclasses import dataclass, field

from runtime.reasoning_object import TemporalValidity


VALID_BASKETS = frozenset({
    "momentum_core",
    "diversification_candidates",
    "risk_thresholds",
    "unclassified",
})


@dataclass
class PositionAssignment:
    """A single position's basket assignment within the Deployment Matrix.

    Attributes:
        position_id: Unique identifier for the position.
        basket: One of the valid basket names.
        rationale: Explanation referencing at least one semantic state.
        semantic_state_refs: signal_ids supporting this assignment.
        confidence_level: Integer 0-100 for assignment confidence.
        temporal_validity: Explicit validity model with valid_from, valid_until, stale_after.
    """

    position_id: str
    basket: str
    rationale: str
    semantic_state_refs: list[str]
    confidence_level: int
    temporal_validity: TemporalValidity


@dataclass
class DeploymentMatrix:
    """Three-basket capital allocation model.

    Each position is assigned to exactly one basket. The matrix is produced
    per pipeline run and tied to a specific Run_Context.

    Attributes:
        positions: All position assignments in this matrix.
        run_context_id: The Run_Context identifier for this matrix.
        schema_version: Schema version string (semantic versioning).
    """

    positions: list[PositionAssignment] = field(default_factory=list)
    run_context_id: str = ""
    schema_version: str = "1.0.0"

    def get_basket(self, basket_name: str) -> list[PositionAssignment]:
        """Return all positions assigned to the given basket.

        Args:
            basket_name: One of momentum_core, diversification_candidates,
                         risk_thresholds, or unclassified.

        Returns:
            List of PositionAssignment objects in the specified basket.
        """
        return [p for p in self.positions if p.basket == basket_name]

    def validate(self) -> list[str]:
        """Return validation errors. Empty list = valid.

        Validates:
        - Each position has a valid basket name.
        - Each position_id appears exactly once (no duplicates).
        - confidence_level is within 0-100.
        - semantic_state_refs is non-empty.
        - run_context_id is non-empty.
        """
        errors: list[str] = []

        if not self.run_context_id:
            errors.append("run_context_id must be a non-empty string")

        if not self.schema_version:
            errors.append("schema_version must be a non-empty string")

        # Track position_ids for duplicate detection
        seen_position_ids: dict[str, int] = {}

        for i, pos in enumerate(self.positions):
            prefix = f"positions[{i}]"

            # position_id must be non-empty
            if not pos.position_id or not isinstance(pos.position_id, str):
                errors.append(f"{prefix}.position_id must be a non-empty string")
            else:
                if pos.position_id in seen_position_ids:
                    errors.append(
                        f"{prefix}.position_id '{pos.position_id}' is duplicated "
                        f"(first seen at index {seen_position_ids[pos.position_id]})"
                    )
                seen_position_ids[pos.position_id] = i

            # basket must be one of the valid baskets
            if pos.basket not in VALID_BASKETS:
                errors.append(
                    f"{prefix}.basket '{pos.basket}' is not valid. "
                    f"Must be one of: {', '.join(sorted(VALID_BASKETS))}"
                )

            # rationale must be non-empty
            if not pos.rationale or not isinstance(pos.rationale, str):
                errors.append(f"{prefix}.rationale must be a non-empty string")

            # semantic_state_refs must have at least one entry
            if not isinstance(pos.semantic_state_refs, list):
                errors.append(f"{prefix}.semantic_state_refs must be a list")
            elif len(pos.semantic_state_refs) < 1:
                errors.append(
                    f"{prefix}.semantic_state_refs must have at least 1 entry"
                )
            else:
                for j, ref in enumerate(pos.semantic_state_refs):
                    if not ref or not isinstance(ref, str):
                        errors.append(
                            f"{prefix}.semantic_state_refs[{j}] must be a non-empty string"
                        )

            # confidence_level must be 0-100
            if not isinstance(pos.confidence_level, int):
                errors.append(f"{prefix}.confidence_level must be an integer")
            elif pos.confidence_level < 0 or pos.confidence_level > 100:
                errors.append(
                    f"{prefix}.confidence_level must be between 0 and 100"
                )

        return errors
