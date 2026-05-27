"""Property-based tests for Reasoning Object to Report Section Mapping.

**Validates: Requirements 2.3, 13.2**

Tests that each Reasoning Object's category maps to the correct Report Section
with provenance reference. Hypothesis generates random valid ReasoningObjects
with various categories; verify mapping is correct and deterministic.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from engines.report_engine import (
    CATEGORY_TO_SECTION,
    CANONICAL_SECTIONS,
    ReportEngine,
)
from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
    VALID_PRODUCING_ENGINES,
)


# --- Strategies ---

valid_category_strategy = st.sampled_from(sorted(CATEGORY_TO_SECTION.keys()))

valid_temporal_validity_strategy = st.builds(
    TemporalValidity,
    valid_from=st.just("2026-01-01T00:00:00+00:00"),
    valid_until=st.just("2026-12-31T23:59:59+00:00"),
    stale_after=st.just(None),
)

valid_action_implication_strategy = st.builds(
    ActionImplication,
    action=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=30,
    ),
    rationale=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=30,
    ),
)


def reasoning_object_with_category(category: str) -> st.SearchStrategy[ReasoningObject]:
    """Build a strategy for a valid ReasoningObject with a specific category."""
    return st.builds(
        ReasoningObject,
        reasoning_id=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=64,
        ),
        source_semantic_states=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N")),
                min_size=1,
                max_size=30,
            ),
            min_size=1,
            max_size=5,
        ),
        conclusion=st.builds(
            Conclusion,
            summary=st.text(
                alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
                min_size=1,
                max_size=100,
            ),
            category=st.just(category),
        ),
        confidence_level=st.integers(min_value=50, max_value=100),
        confidence_explanation=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
            min_size=1,
            max_size=100,
        ),
        action_implications=st.lists(
            valid_action_implication_strategy, min_size=0, max_size=3
        ),
        temporal_validity=valid_temporal_validity_strategy,
        producing_engine=st.sampled_from(sorted(VALID_PRODUCING_ENGINES)),
        schema_version=st.just("1.0.0"),
    )


# Strategy for a valid ReasoningObject with a random valid category
valid_reasoning_object_with_known_category_strategy = valid_category_strategy.flatmap(
    reasoning_object_with_category
)


class TestReasoningObjectToReportSectionMapping:
    """Property-based tests for CATEGORY_TO_SECTION mapping and ReportEngine provenance."""

    @given(category=valid_category_strategy)
    @settings(max_examples=200)
    def test_every_category_maps_to_valid_canonical_section(
        self, category: str
    ) -> None:
        """Property 1: Every category in CATEGORY_TO_SECTION maps to a valid canonical section.

        **Validates: Requirements 2.3**

        For any category key in CATEGORY_TO_SECTION, the mapped section name
        must be one of the 9 CANONICAL_SECTIONS.
        """
        section = CATEGORY_TO_SECTION[category]

        assert section in CANONICAL_SECTIONS, (
            f"Category '{category}' maps to section '{section}' which is not "
            f"in CANONICAL_SECTIONS: {CANONICAL_SECTIONS}"
        )

    @given(
        category=valid_category_strategy,
        reasoning_id=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=64,
        ),
        source_states=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N")),
                min_size=1,
                max_size=30,
            ),
            min_size=1,
            max_size=5,
        ),
        confidence=st.integers(min_value=50, max_value=100),
        explanation=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
            min_size=1,
            max_size=100,
        ),
    )
    @settings(max_examples=200)
    def test_reasoning_object_appears_in_correct_section_provenance(
        self,
        category: str,
        reasoning_id: str,
        source_states: list[str],
        confidence: int,
        explanation: str,
    ) -> None:
        """Property 2: ReasoningObjects with a given category appear in the correct section's provenance.

        **Validates: Requirements 2.3, 13.2**

        For any valid ReasoningObject with a known category, when rendered
        through ReportEngine.render_section(), the provenance must contain
        the object's reasoning_id in the expected section.
        """
        obj = ReasoningObject(
            reasoning_id=reasoning_id,
            source_semantic_states=source_states,
            conclusion=Conclusion(summary="Test conclusion", category=category),
            confidence_level=confidence,
            confidence_explanation=explanation,
            action_implications=[],
            temporal_validity=TemporalValidity(
                valid_from="2026-01-01T00:00:00+00:00",
                valid_until="2026-12-31T23:59:59+00:00",
                stale_after=None,
            ),
            producing_engine="decision_engine",
            schema_version="1.0.0",
        )

        # Ensure the object is valid
        assume(obj.validate() == [])

        expected_section = CATEGORY_TO_SECTION[category]
        engine = ReportEngine()

        # Render the section that this category maps to
        _content, provenance = engine.render_section(expected_section, [obj])

        assert obj.reasoning_id in provenance.reasoning_object_ids, (
            f"ReasoningObject with reasoning_id='{reasoning_id}' and "
            f"category='{category}' was not found in provenance for "
            f"section '{expected_section}'. "
            f"Provenance reasoning_object_ids: {provenance.reasoning_object_ids}"
        )

    @given(
        category=valid_category_strategy,
        reasoning_id=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=64,
        ),
        source_states=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N")),
                min_size=1,
                max_size=30,
            ),
            min_size=1,
            max_size=5,
        ),
        confidence=st.integers(min_value=50, max_value=100),
        explanation=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
            min_size=1,
            max_size=100,
        ),
    )
    @settings(max_examples=200)
    def test_mapping_is_deterministic(
        self,
        category: str,
        reasoning_id: str,
        source_states: list[str],
        confidence: int,
        explanation: str,
    ) -> None:
        """Property 3: Mapping is deterministic — same inputs always produce same section assignment.

        **Validates: Requirements 2.3, 13.2**

        For any valid ReasoningObject, the category-to-section mapping and
        provenance assembly must produce identical results across multiple
        invocations.
        """
        obj = ReasoningObject(
            reasoning_id=reasoning_id,
            source_semantic_states=source_states,
            conclusion=Conclusion(summary="Test conclusion", category=category),
            confidence_level=confidence,
            confidence_explanation=explanation,
            action_implications=[],
            temporal_validity=TemporalValidity(
                valid_from="2026-01-01T00:00:00+00:00",
                valid_until="2026-12-31T23:59:59+00:00",
                stale_after=None,
            ),
            producing_engine="decision_engine",
            schema_version="1.0.0",
        )

        # Ensure the object is valid
        assume(obj.validate() == [])

        expected_section = CATEGORY_TO_SECTION[category]
        engine = ReportEngine()

        # Render the section multiple times
        _content_1, provenance_1 = engine.render_section(expected_section, [obj])
        _content_2, provenance_2 = engine.render_section(expected_section, [obj])
        _content_3, provenance_3 = engine.render_section(expected_section, [obj])

        # All provenance results must be identical
        assert provenance_1.reasoning_object_ids == provenance_2.reasoning_object_ids, (
            f"Non-deterministic provenance! First call: {provenance_1.reasoning_object_ids}, "
            f"second call: {provenance_2.reasoning_object_ids}"
        )
        assert provenance_2.reasoning_object_ids == provenance_3.reasoning_object_ids, (
            f"Non-deterministic provenance! Second call: {provenance_2.reasoning_object_ids}, "
            f"third call: {provenance_3.reasoning_object_ids}"
        )

        # Section name in provenance must match expected section
        assert provenance_1.section_name == expected_section, (
            f"Provenance section_name '{provenance_1.section_name}' does not match "
            f"expected section '{expected_section}' for category '{category}'"
        )
        assert provenance_1.section_name == provenance_2.section_name == provenance_3.section_name, (
            f"Non-deterministic section_name in provenance across calls"
        )
