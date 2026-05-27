"""Unit tests for governance/canonical_boundary.py.

Tests classification and boundary enforcement logic for canonical
vs. transient artifacts.
"""

import pytest

from governance.canonical_boundary import (
    CANONICAL_ARTIFACTS,
    TRANSIENT_ARTIFACTS,
    classify,
    enforce_boundary,
)


# ---------------------------------------------------------------------------
# Tests for CANONICAL_ARTIFACTS and TRANSIENT_ARTIFACTS sets
# ---------------------------------------------------------------------------


class TestArtifactSets:
    """Verify the artifact sets are correctly defined and disjoint."""

    def test_canonical_artifacts_is_frozenset(self):
        assert isinstance(CANONICAL_ARTIFACTS, frozenset)

    def test_transient_artifacts_is_frozenset(self):
        assert isinstance(TRANSIENT_ARTIFACTS, frozenset)

    def test_canonical_contains_expected_members(self):
        expected = {
            "semantic_state_snapshot",
            "reasoning_object",
            "daily_report",
            "deployment_matrix",
            "run_context",
            "provenance_metadata",
        }
        assert CANONICAL_ARTIFACTS == expected

    def test_transient_contains_expected_members(self):
        expected = {
            "orchestration_buffer",
            "in_memory_transform",
            "pre_validation_staging",
            "intermediate_draft_reasoning",
        }
        assert TRANSIENT_ARTIFACTS == expected

    def test_sets_are_disjoint(self):
        assert CANONICAL_ARTIFACTS.isdisjoint(TRANSIENT_ARTIFACTS)


# ---------------------------------------------------------------------------
# Tests for classify()
# ---------------------------------------------------------------------------


class TestClassify:
    """Verify classify() returns correct category or raises ValueError."""

    @pytest.mark.parametrize("artifact", sorted(CANONICAL_ARTIFACTS))
    def test_canonical_artifacts_classified_correctly(self, artifact):
        assert classify(artifact) == "canonical"

    @pytest.mark.parametrize("artifact", sorted(TRANSIENT_ARTIFACTS))
    def test_transient_artifacts_classified_correctly(self, artifact):
        assert classify(artifact) == "transient"

    def test_unknown_artifact_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown artifact"):
            classify("nonexistent_artifact")

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown artifact"):
            classify("")


# ---------------------------------------------------------------------------
# Tests for enforce_boundary()
# ---------------------------------------------------------------------------


class TestEnforceBoundary:
    """Verify boundary enforcement and promotion logic."""

    def test_canonical_artifact_stays_canonical_no_flags(self):
        assert enforce_boundary("daily_report") == "canonical"

    def test_canonical_artifact_stays_canonical_with_persisted(self):
        assert enforce_boundary("daily_report", is_persisted=True) == "canonical"

    def test_canonical_artifact_stays_canonical_with_downstream(self):
        assert enforce_boundary("reasoning_object", is_passed_downstream=True) == "canonical"

    def test_transient_artifact_stays_transient_no_flags(self):
        assert enforce_boundary("orchestration_buffer") == "transient"

    def test_transient_promoted_when_persisted(self):
        assert enforce_boundary("orchestration_buffer", is_persisted=True) == "canonical"

    def test_transient_promoted_when_passed_downstream(self):
        assert enforce_boundary("in_memory_transform", is_passed_downstream=True) == "canonical"

    def test_transient_promoted_when_both_flags_set(self):
        assert enforce_boundary(
            "pre_validation_staging", is_persisted=True, is_passed_downstream=True
        ) == "canonical"

    def test_transient_not_promoted_when_both_flags_false(self):
        assert enforce_boundary(
            "intermediate_draft_reasoning", is_persisted=False, is_passed_downstream=False
        ) == "transient"

    def test_unknown_artifact_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown artifact"):
            enforce_boundary("unknown_thing", is_persisted=True)
