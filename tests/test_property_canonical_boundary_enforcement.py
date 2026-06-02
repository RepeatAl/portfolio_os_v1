"""Property-based tests for Canonical Boundary Enforcement.

**Validates: Requirements 16.4, 16.5**

Tests that transient artifacts are promoted to canonical when persisted or
passed downstream. Verifies classification is deterministic, canonical artifacts
always remain canonical, and unknown artifacts raise ValueError.
"""

from hypothesis import given, settings
from hypothesis import strategies as st
import pytest

from governance.canonical_boundary import (
    CANONICAL_ARTIFACTS,
    TRANSIENT_ARTIFACTS,
    classify,
    enforce_boundary,
)


# Strategies: sample from the known artifact sets
canonical_strategy = st.sampled_from(sorted(CANONICAL_ARTIFACTS))
transient_strategy = st.sampled_from(sorted(TRANSIENT_ARTIFACTS))
all_known_strategy = st.sampled_from(sorted(CANONICAL_ARTIFACTS | TRANSIENT_ARTIFACTS))
boolean_strategy = st.booleans()


# Strategy for unknown artifact names (strings not in either set)
unknown_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_"),
    min_size=1,
    max_size=50,
).filter(lambda s: s not in CANONICAL_ARTIFACTS and s not in TRANSIENT_ARTIFACTS)


class TestCanonicalBoundaryEnforcementProperties:
    """Property-based tests for canonical boundary classification and enforcement."""

    @given(artifact=all_known_strategy)
    @settings(max_examples=200)
    def test_classification_is_deterministic(self, artifact: str) -> None:
        """Property 1: Classification is deterministic — same artifact name always returns same result.

        **Validates: Requirements 16.4, 16.5**

        For any known artifact name, calling classify() multiple times always
        produces the same result.
        """
        result_1 = classify(artifact)
        result_2 = classify(artifact)

        assert result_1 == result_2, (
            f"Determinism violated: classify('{artifact}') returned "
            f"'{result_1}' and '{result_2}'"
        )

    @given(artifact=canonical_strategy, is_persisted=boolean_strategy, is_passed=boolean_strategy)
    @settings(max_examples=200)
    def test_canonical_artifacts_always_canonical(
        self, artifact: str, is_persisted: bool, is_passed: bool
    ) -> None:
        """Property 2: All canonical artifacts always classify as 'canonical' regardless of flags.

        **Validates: Requirements 16.4, 16.5**

        Canonical artifacts remain canonical no matter what combination of
        is_persisted and is_passed_downstream flags are provided.
        """
        result = enforce_boundary(
            artifact, is_persisted=is_persisted, is_passed_downstream=is_passed
        )

        assert result == "canonical", (
            f"Canonical artifact '{artifact}' was not classified as 'canonical' "
            f"with is_persisted={is_persisted}, is_passed_downstream={is_passed}. "
            f"Got '{result}'"
        )

    @given(artifact=transient_strategy)
    @settings(max_examples=200)
    def test_transient_promoted_when_persisted(self, artifact: str) -> None:
        """Property 3: Transient artifacts with is_persisted=True are promoted to 'canonical'.

        **Validates: Requirements 16.5**

        When a transient artifact is persisted to disk, it crosses a runtime
        boundary and must be reclassified as canonical.
        """
        result = enforce_boundary(artifact, is_persisted=True, is_passed_downstream=False)

        assert result == "canonical", (
            f"Transient artifact '{artifact}' was not promoted to 'canonical' "
            f"when is_persisted=True. Got '{result}'"
        )

    @given(artifact=transient_strategy)
    @settings(max_examples=200)
    def test_transient_promoted_when_passed_downstream(self, artifact: str) -> None:
        """Property 4: Transient artifacts with is_passed_downstream=True are promoted to 'canonical'.

        **Validates: Requirements 16.5**

        When a transient artifact is passed to a downstream engine as input,
        it crosses a runtime boundary and must be reclassified as canonical.
        """
        result = enforce_boundary(artifact, is_persisted=False, is_passed_downstream=True)

        assert result == "canonical", (
            f"Transient artifact '{artifact}' was not promoted to 'canonical' "
            f"when is_passed_downstream=True. Got '{result}'"
        )

    @given(artifact=transient_strategy)
    @settings(max_examples=200)
    def test_transient_remains_transient_without_flags(self, artifact: str) -> None:
        """Property 5: Transient artifacts with both flags False remain 'transient'.

        **Validates: Requirements 16.4**

        Transient artifacts that are not persisted and not passed downstream
        remain transient and exempt from canonical governance.
        """
        result = enforce_boundary(artifact, is_persisted=False, is_passed_downstream=False)

        assert result == "transient", (
            f"Transient artifact '{artifact}' should remain 'transient' "
            f"when both flags are False. Got '{result}'"
        )

    @given(artifact=unknown_strategy)
    @settings(max_examples=200)
    def test_unknown_artifacts_raise_value_error(self, artifact: str) -> None:
        """Property 6: Unknown artifact names always raise ValueError.

        **Validates: Requirements 16.4, 16.5**

        Any artifact name not in CANONICAL_ARTIFACTS or TRANSIENT_ARTIFACTS
        must raise ValueError from both classify() and enforce_boundary().
        """
        with pytest.raises(ValueError):
            classify(artifact)

        with pytest.raises(ValueError):
            enforce_boundary(artifact)
