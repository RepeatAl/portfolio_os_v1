"""Property-based tests for Section Completeness State Classification.

**Validates: Requirements 24.1, 24.2**

Tests that each section is classified into exactly one state and rendering
behavior follows from that state. The SectionCompletenessClassifier must
always return one of the 5 valid completeness states, and classification
must be deterministic.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from engines.report_engine import (
    SectionCompletenessClassifier,
    COMPLETENESS_STATES,
    CANONICAL_SECTIONS,
)
from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
    VALID_PRODUCING_ENGINES,
)


# --- Strategies ---

section_name_strategy = st.sampled_from(CANONICAL_SECTIONS)

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

# Strategy for a fully valid ReasoningObject with high confidence (>= 50)
valid_high_confidence_object_strategy = st.builds(
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
        category=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=30,
        ),
    ),
    confidence_level=st.integers(min_value=50, max_value=100),
    confidence_explanation=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=100,
    ),
    action_implications=st.lists(valid_action_implication_strategy, min_size=0, max_size=3),
    temporal_validity=valid_temporal_validity_strategy,
    producing_engine=st.sampled_from(sorted(VALID_PRODUCING_ENGINES)),
    schema_version=st.just("1.0.0"),
)

# Strategy for a valid ReasoningObject with low confidence (< 50)
valid_low_confidence_object_strategy = st.builds(
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
        category=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=30,
        ),
    ),
    confidence_level=st.integers(min_value=0, max_value=49),
    confidence_explanation=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=100,
    ),
    action_implications=st.lists(valid_action_implication_strategy, min_size=0, max_size=3),
    temporal_validity=valid_temporal_validity_strategy,
    producing_engine=st.sampled_from(sorted(VALID_PRODUCING_ENGINES)),
    schema_version=st.just("1.0.0"),
)

# Strategy for an invalid ReasoningObject (fails validate())
invalid_object_strategy = st.builds(
    ReasoningObject,
    reasoning_id=st.just(""),  # Empty reasoning_id triggers validation failure
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
        category=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=30,
        ),
    ),
    confidence_level=st.integers(min_value=50, max_value=100),
    confidence_explanation=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=100,
    ),
    action_implications=st.lists(valid_action_implication_strategy, min_size=0, max_size=3),
    temporal_validity=valid_temporal_validity_strategy,
    producing_engine=st.sampled_from(sorted(VALID_PRODUCING_ENGINES)),
    schema_version=st.just("1.0.0"),
)

# Mixed list strategy: some valid high-confidence, some valid low-confidence
mixed_objects_strategy = st.lists(
    st.one_of(
        valid_high_confidence_object_strategy,
        valid_low_confidence_object_strategy,
        invalid_object_strategy,
    ),
    min_size=0,
    max_size=10,
)


class TestSectionCompletenessStateClassification:
    """Property-based tests for SectionCompletenessClassifier.classify()."""

    @given(
        section_name=section_name_strategy,
        objects=mixed_objects_strategy,
    )
    @settings(max_examples=300)
    def test_classify_always_returns_valid_completeness_state(
        self, section_name: str, objects: list[ReasoningObject]
    ) -> None:
        """Property 1: classify() always returns one of the 5 valid completeness states.

        **Validates: Requirements 24.1**

        For any section name and any list of ReasoningObjects (valid, invalid,
        or mixed), classify() must return exactly one of: complete, partial,
        degraded, unavailable, invalid.
        """
        classifier = SectionCompletenessClassifier()
        result = classifier.classify(section_name, objects)

        assert result in COMPLETENESS_STATES, (
            f"classify() returned '{result}' which is not in COMPLETENESS_STATES "
            f"{COMPLETENESS_STATES}. Section: {section_name}, "
            f"object count: {len(objects)}"
        )

    @given(section_name=section_name_strategy)
    @settings(max_examples=100)
    def test_empty_object_list_always_returns_unavailable(
        self, section_name: str
    ) -> None:
        """Property 2: Empty object list always returns "unavailable".

        **Validates: Requirements 24.1**

        When no ReasoningObjects are available for a section, the classifier
        must return "unavailable" regardless of section name.
        """
        classifier = SectionCompletenessClassifier()
        result = classifier.classify(section_name, [])

        assert result == "unavailable", (
            f"Empty object list should return 'unavailable', got '{result}' "
            f"for section '{section_name}'"
        )

    @given(
        section_name=section_name_strategy,
        objects=st.lists(valid_high_confidence_object_strategy, min_size=1, max_size=5),
    )
    @settings(max_examples=200)
    def test_all_valid_high_confidence_objects_return_complete(
        self, section_name: str, objects: list[ReasoningObject]
    ) -> None:
        """Property 3: All-valid high-confidence objects always return "complete".

        **Validates: Requirements 24.1, 24.2**

        When all ReasoningObjects pass validation and have confidence >= 50,
        the section must be classified as "complete".
        """
        classifier = SectionCompletenessClassifier()

        # Confirm all objects are actually valid and high-confidence
        for obj in objects:
            assume(obj.validate() == [])
            assume(obj.confidence_level >= 50)

        result = classifier.classify(section_name, objects)

        assert result == "complete", (
            f"All-valid high-confidence objects should return 'complete', "
            f"got '{result}' for section '{section_name}'. "
            f"Object count: {len(objects)}, "
            f"confidence levels: {[o.confidence_level for o in objects]}"
        )

    @given(
        section_name=section_name_strategy,
        objects=st.lists(invalid_object_strategy, min_size=1, max_size=5),
    )
    @settings(max_examples=200)
    def test_all_invalid_objects_return_invalid(
        self, section_name: str, objects: list[ReasoningObject]
    ) -> None:
        """Property 4: All-invalid objects always return "invalid".

        **Validates: Requirements 24.1, 24.2**

        When all ReasoningObjects fail validation, the section must be
        classified as "invalid".
        """
        classifier = SectionCompletenessClassifier()

        # Confirm all objects actually fail validation
        for obj in objects:
            assume(obj.validate() != [])

        result = classifier.classify(section_name, objects)

        assert result == "invalid", (
            f"All-invalid objects should return 'invalid', got '{result}' "
            f"for section '{section_name}'. Object count: {len(objects)}"
        )

    @given(
        section_name=section_name_strategy,
        objects=mixed_objects_strategy,
    )
    @settings(max_examples=300)
    def test_classification_is_deterministic(
        self, section_name: str, objects: list[ReasoningObject]
    ) -> None:
        """Property 5: Classification is deterministic (same inputs → same state).

        **Validates: Requirements 24.1**

        For any given section name and list of ReasoningObjects, calling
        classify() multiple times must always return the same result.
        """
        classifier = SectionCompletenessClassifier()

        result_1 = classifier.classify(section_name, objects)
        result_2 = classifier.classify(section_name, objects)
        result_3 = classifier.classify(section_name, objects)

        assert result_1 == result_2 == result_3, (
            f"Classification is non-deterministic! "
            f"Got '{result_1}', '{result_2}', '{result_3}' for same inputs. "
            f"Section: {section_name}, object count: {len(objects)}"
        )
