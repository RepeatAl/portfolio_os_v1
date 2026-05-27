"""Unit tests for runtime/deployment_matrix.py.

Tests the DeploymentMatrix and PositionAssignment dataclasses,
including get_basket() filtering and validate() constraint enforcement.

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5
"""

import pytest

from runtime.deployment_matrix import (
    DeploymentMatrix,
    PositionAssignment,
    VALID_BASKETS,
)
from runtime.reasoning_object import TemporalValidity


@pytest.fixture
def sample_temporal_validity() -> TemporalValidity:
    """Provide a valid TemporalValidity for tests."""
    return TemporalValidity(
        valid_from="2026-01-01T00:00:00Z",
        valid_until="2026-12-31T23:59:59Z",
    )


@pytest.fixture
def sample_positions(sample_temporal_validity: TemporalValidity) -> list[PositionAssignment]:
    """Provide a set of valid positions across all baskets."""
    return [
        PositionAssignment(
            position_id="AAPL",
            basket="momentum_core",
            rationale="Strong momentum from AI narrative",
            semantic_state_refs=["ai_dependency_high"],
            confidence_level=85,
            temporal_validity=sample_temporal_validity,
        ),
        PositionAssignment(
            position_id="MSFT",
            basket="momentum_core",
            rationale="Tech leadership position",
            semantic_state_refs=["semiconductor_dependency_high"],
            confidence_level=75,
            temporal_validity=sample_temporal_validity,
        ),
        PositionAssignment(
            position_id="GLD",
            basket="diversification_candidates",
            rationale="Portfolio hedge exposure",
            semantic_state_refs=["portfolio_health_fragile"],
            confidence_level=60,
            temporal_validity=sample_temporal_validity,
        ),
        PositionAssignment(
            position_id="TLT",
            basket="risk_thresholds",
            rationale="Duration risk elevated",
            semantic_state_refs=["concentration_risk_elevated"],
            confidence_level=40,
            temporal_validity=sample_temporal_validity,
        ),
        PositionAssignment(
            position_id="XYZ",
            basket="unclassified",
            rationale="Insufficient semantic data",
            semantic_state_refs=["defense_dependency_elevated"],
            confidence_level=0,
            temporal_validity=sample_temporal_validity,
        ),
    ]


class TestPositionAssignment:
    """Tests for PositionAssignment dataclass."""

    def test_creation(self, sample_temporal_validity: TemporalValidity) -> None:
        """PositionAssignment stores all fields correctly."""
        pa = PositionAssignment(
            position_id="NVDA",
            basket="momentum_core",
            rationale="Semiconductor leadership",
            semantic_state_refs=["semiconductor_dependency_high", "ai_dependency_high"],
            confidence_level=90,
            temporal_validity=sample_temporal_validity,
        )
        assert pa.position_id == "NVDA"
        assert pa.basket == "momentum_core"
        assert pa.rationale == "Semiconductor leadership"
        assert pa.semantic_state_refs == ["semiconductor_dependency_high", "ai_dependency_high"]
        assert pa.confidence_level == 90
        assert pa.temporal_validity is sample_temporal_validity


class TestDeploymentMatrix:
    """Tests for DeploymentMatrix dataclass."""

    def test_default_construction(self) -> None:
        """DeploymentMatrix can be created with defaults."""
        dm = DeploymentMatrix(run_context_id="run-001")
        assert dm.positions == []
        assert dm.run_context_id == "run-001"
        assert dm.schema_version == "1.0.0"

    def test_get_basket_returns_correct_positions(
        self, sample_positions: list[PositionAssignment]
    ) -> None:
        """get_basket() returns only positions matching the basket name."""
        dm = DeploymentMatrix(positions=sample_positions, run_context_id="run-001")

        momentum = dm.get_basket("momentum_core")
        assert len(momentum) == 2
        assert all(p.basket == "momentum_core" for p in momentum)
        assert {p.position_id for p in momentum} == {"AAPL", "MSFT"}

    def test_get_basket_diversification(
        self, sample_positions: list[PositionAssignment]
    ) -> None:
        """get_basket() returns diversification_candidates correctly."""
        dm = DeploymentMatrix(positions=sample_positions, run_context_id="run-001")
        div = dm.get_basket("diversification_candidates")
        assert len(div) == 1
        assert div[0].position_id == "GLD"

    def test_get_basket_risk_thresholds(
        self, sample_positions: list[PositionAssignment]
    ) -> None:
        """get_basket() returns risk_thresholds correctly."""
        dm = DeploymentMatrix(positions=sample_positions, run_context_id="run-001")
        risk = dm.get_basket("risk_thresholds")
        assert len(risk) == 1
        assert risk[0].position_id == "TLT"

    def test_get_basket_unclassified(
        self, sample_positions: list[PositionAssignment]
    ) -> None:
        """get_basket() returns unclassified positions correctly."""
        dm = DeploymentMatrix(positions=sample_positions, run_context_id="run-001")
        unc = dm.get_basket("unclassified")
        assert len(unc) == 1
        assert unc[0].position_id == "XYZ"

    def test_get_basket_empty_result(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """get_basket() returns empty list when no positions match."""
        pos = PositionAssignment(
            position_id="A",
            basket="momentum_core",
            rationale="Test",
            semantic_state_refs=["x"],
            confidence_level=50,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos], run_context_id="run-001")
        assert dm.get_basket("risk_thresholds") == []

    def test_validate_valid_matrix(
        self, sample_positions: list[PositionAssignment]
    ) -> None:
        """validate() returns empty list for a valid matrix."""
        dm = DeploymentMatrix(positions=sample_positions, run_context_id="run-001")
        assert dm.validate() == []

    def test_validate_empty_run_context_id(
        self, sample_positions: list[PositionAssignment]
    ) -> None:
        """validate() catches empty run_context_id."""
        dm = DeploymentMatrix(positions=sample_positions, run_context_id="")
        errors = dm.validate()
        assert any("run_context_id" in e for e in errors)

    def test_validate_duplicate_position_id(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """validate() catches duplicate position_ids."""
        pos1 = PositionAssignment(
            position_id="AAPL",
            basket="momentum_core",
            rationale="First",
            semantic_state_refs=["x"],
            confidence_level=80,
            temporal_validity=sample_temporal_validity,
        )
        pos2 = PositionAssignment(
            position_id="AAPL",
            basket="risk_thresholds",
            rationale="Duplicate",
            semantic_state_refs=["y"],
            confidence_level=30,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos1, pos2], run_context_id="run-001")
        errors = dm.validate()
        assert any("duplicated" in e for e in errors)

    def test_validate_invalid_basket(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """validate() catches invalid basket names."""
        pos = PositionAssignment(
            position_id="BAD",
            basket="nonexistent_basket",
            rationale="Invalid",
            semantic_state_refs=["x"],
            confidence_level=50,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos], run_context_id="run-001")
        errors = dm.validate()
        assert any("not valid" in e for e in errors)

    def test_validate_confidence_out_of_range(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """validate() catches confidence_level outside 0-100."""
        pos = PositionAssignment(
            position_id="OOR",
            basket="momentum_core",
            rationale="Out of range",
            semantic_state_refs=["x"],
            confidence_level=150,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos], run_context_id="run-001")
        errors = dm.validate()
        assert any("confidence_level" in e for e in errors)

    def test_validate_negative_confidence(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """validate() catches negative confidence_level."""
        pos = PositionAssignment(
            position_id="NEG",
            basket="momentum_core",
            rationale="Negative",
            semantic_state_refs=["x"],
            confidence_level=-5,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos], run_context_id="run-001")
        errors = dm.validate()
        assert any("confidence_level" in e for e in errors)

    def test_validate_empty_semantic_state_refs(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """validate() catches empty semantic_state_refs."""
        pos = PositionAssignment(
            position_id="EMPTY",
            basket="momentum_core",
            rationale="No refs",
            semantic_state_refs=[],
            confidence_level=50,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos], run_context_id="run-001")
        errors = dm.validate()
        assert any("semantic_state_refs" in e for e in errors)

    def test_validate_empty_rationale(
        self, sample_temporal_validity: TemporalValidity
    ) -> None:
        """validate() catches empty rationale."""
        pos = PositionAssignment(
            position_id="NORAT",
            basket="momentum_core",
            rationale="",
            semantic_state_refs=["x"],
            confidence_level=50,
            temporal_validity=sample_temporal_validity,
        )
        dm = DeploymentMatrix(positions=[pos], run_context_id="run-001")
        errors = dm.validate()
        assert any("rationale" in e for e in errors)


class TestValidBaskets:
    """Tests for the VALID_BASKETS constant."""

    def test_contains_all_required_baskets(self) -> None:
        """VALID_BASKETS contains exactly the 4 required baskets."""
        expected = {"momentum_core", "diversification_candidates", "risk_thresholds", "unclassified"}
        assert VALID_BASKETS == expected

    def test_is_frozenset(self) -> None:
        """VALID_BASKETS is immutable."""
        assert isinstance(VALID_BASKETS, frozenset)
