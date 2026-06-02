"""Property-based tests for Reasoning Object Schema Enforcement.

**Validates: Requirements 9.1, 9.4, 9.5**

Tests that invalid objects (missing fields, out-of-range values) are correctly
rejected by validate(), and that valid objects always pass validation.
Hypothesis generates random ReasoningObject fields; verify validate() catches
all constraint violations.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
    VALID_PRODUCING_ENGINES,
)


# --- Strategies for valid field generation ---

valid_reasoning_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=1,
    max_size=128,
)

valid_source_semantic_states_strategy = st.lists(
    st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P")),
        min_size=1,
        max_size=50,
    ),
    min_size=1,
    max_size=50,
)

valid_conclusion_strategy = st.builds(
    Conclusion,
    summary=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
        min_size=1,
        max_size=100,
    ),
    category=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=50,
    ),
)

valid_confidence_level_strategy = st.integers(min_value=0, max_value=100)

valid_confidence_explanation_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
    min_size=1,
    max_size=100,
)

valid_action_implication_strategy = st.builds(
    ActionImplication,
    action=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
        min_size=1,
        max_size=50,
    ),
    rationale=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
        min_size=1,
        max_size=50,
    ),
)

valid_action_implications_strategy = st.lists(
    valid_action_implication_strategy, min_size=0, max_size=20
)

valid_temporal_validity_strategy = st.builds(
    TemporalValidity,
    valid_from=st.just("2026-01-01T00:00:00+00:00"),
    valid_until=st.just("2026-12-31T23:59:59+00:00"),
    stale_after=st.just(None),
)

valid_producing_engine_strategy = st.sampled_from(sorted(VALID_PRODUCING_ENGINES))

valid_schema_version_strategy = st.just("1.0.0")


# --- Strategy for a fully valid ReasoningObject ---

valid_reasoning_object_strategy = st.builds(
    ReasoningObject,
    reasoning_id=valid_reasoning_id_strategy,
    source_semantic_states=valid_source_semantic_states_strategy,
    conclusion=valid_conclusion_strategy,
    confidence_level=valid_confidence_level_strategy,
    confidence_explanation=valid_confidence_explanation_strategy,
    action_implications=valid_action_implications_strategy,
    temporal_validity=valid_temporal_validity_strategy,
    producing_engine=valid_producing_engine_strategy,
    schema_version=valid_schema_version_strategy,
)


# --- Strategies for invalid field generation ---

invalid_reasoning_id_empty_strategy = st.just("")

invalid_reasoning_id_too_long_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L",)),
    min_size=129,
    max_size=200,
)

invalid_source_semantic_states_empty_strategy = st.just([])

invalid_source_semantic_states_too_many_strategy = st.lists(
    st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=10,
    ),
    min_size=51,
    max_size=60,
)

invalid_confidence_level_below_strategy = st.integers(
    min_value=-1000, max_value=-1
)

invalid_confidence_level_above_strategy = st.integers(
    min_value=101, max_value=1000
)

invalid_producing_engine_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=50,
).filter(lambda x: x not in VALID_PRODUCING_ENGINES)


class TestReasoningObjectSchemaEnforcement:
    """Property-based tests for ReasoningObject.validate() method."""

    @given(obj=valid_reasoning_object_strategy)
    @settings(max_examples=200)
    def test_valid_objects_always_pass_validation(self, obj: ReasoningObject) -> None:
        """Property 1: Valid objects always pass validation (empty error list).

        **Validates: Requirements 9.1**

        For any ReasoningObject with all fields within valid ranges,
        validate() returns an empty list.
        """
        errors = obj.validate()
        assert errors == [], (
            f"Valid object produced validation errors: {errors}\n"
            f"Object: reasoning_id={obj.reasoning_id!r}, "
            f"confidence_level={obj.confidence_level}, "
            f"producing_engine={obj.producing_engine!r}, "
            f"source_semantic_states count={len(obj.source_semantic_states)}"
        )

    @given(
        invalid_id=invalid_reasoning_id_empty_strategy
        | invalid_reasoning_id_too_long_strategy,
        source_states=valid_source_semantic_states_strategy,
        conclusion=valid_conclusion_strategy,
        confidence=valid_confidence_level_strategy,
        explanation=valid_confidence_explanation_strategy,
        implications=valid_action_implications_strategy,
        validity=valid_temporal_validity_strategy,
        engine=valid_producing_engine_strategy,
    )
    @settings(max_examples=200)
    def test_invalid_reasoning_id_produces_errors(
        self,
        invalid_id: str,
        source_states: list[str],
        conclusion: Conclusion,
        confidence: int,
        explanation: str,
        implications: list[ActionImplication],
        validity: TemporalValidity,
        engine: str,
    ) -> None:
        """Property 2: Invalid reasoning_id (empty or >128 chars) always produces errors.

        **Validates: Requirements 9.1**

        For any ReasoningObject with an empty or too-long reasoning_id,
        validate() returns a non-empty error list mentioning reasoning_id.
        """
        obj = ReasoningObject(
            reasoning_id=invalid_id,
            source_semantic_states=source_states,
            conclusion=conclusion,
            confidence_level=confidence,
            confidence_explanation=explanation,
            action_implications=implications,
            temporal_validity=validity,
            producing_engine=engine,
        )
        errors = obj.validate()
        assert len(errors) > 0, (
            f"Invalid reasoning_id={invalid_id!r} (len={len(invalid_id)}) "
            f"was not rejected by validate()"
        )
        assert any("reasoning_id" in e for e in errors), (
            f"Errors {errors} do not mention 'reasoning_id' for invalid id={invalid_id!r}"
        )

    @given(
        reasoning_id=valid_reasoning_id_strategy,
        invalid_states=invalid_source_semantic_states_empty_strategy
        | invalid_source_semantic_states_too_many_strategy,
        conclusion=valid_conclusion_strategy,
        confidence=valid_confidence_level_strategy,
        explanation=valid_confidence_explanation_strategy,
        implications=valid_action_implications_strategy,
        validity=valid_temporal_validity_strategy,
        engine=valid_producing_engine_strategy,
    )
    @settings(max_examples=200)
    def test_invalid_source_semantic_states_produces_errors(
        self,
        reasoning_id: str,
        invalid_states: list[str],
        conclusion: Conclusion,
        confidence: int,
        explanation: str,
        implications: list[ActionImplication],
        validity: TemporalValidity,
        engine: str,
    ) -> None:
        """Property 3: Invalid source_semantic_states (empty list or >50 entries) always produces errors.

        **Validates: Requirements 9.1, 9.5**

        For any ReasoningObject with an empty or oversized source_semantic_states,
        validate() returns a non-empty error list mentioning source_semantic_states.
        """
        obj = ReasoningObject(
            reasoning_id=reasoning_id,
            source_semantic_states=invalid_states,
            conclusion=conclusion,
            confidence_level=confidence,
            confidence_explanation=explanation,
            action_implications=implications,
            temporal_validity=validity,
            producing_engine=engine,
        )
        errors = obj.validate()
        assert len(errors) > 0, (
            f"Invalid source_semantic_states (len={len(invalid_states)}) "
            f"was not rejected by validate()"
        )
        assert any("source_semantic_states" in e for e in errors), (
            f"Errors {errors} do not mention 'source_semantic_states' "
            f"for invalid states (len={len(invalid_states)})"
        )

    @given(
        reasoning_id=valid_reasoning_id_strategy,
        source_states=valid_source_semantic_states_strategy,
        conclusion=valid_conclusion_strategy,
        invalid_confidence=invalid_confidence_level_below_strategy
        | invalid_confidence_level_above_strategy,
        explanation=valid_confidence_explanation_strategy,
        implications=valid_action_implications_strategy,
        validity=valid_temporal_validity_strategy,
        engine=valid_producing_engine_strategy,
    )
    @settings(max_examples=200)
    def test_invalid_confidence_level_produces_errors(
        self,
        reasoning_id: str,
        source_states: list[str],
        conclusion: Conclusion,
        invalid_confidence: int,
        explanation: str,
        implications: list[ActionImplication],
        validity: TemporalValidity,
        engine: str,
    ) -> None:
        """Property 4: Invalid confidence_level (<0 or >100) always produces errors.

        **Validates: Requirements 9.1, 9.4**

        For any ReasoningObject with confidence_level outside [0, 100],
        validate() returns a non-empty error list mentioning confidence_level.
        """
        obj = ReasoningObject(
            reasoning_id=reasoning_id,
            source_semantic_states=source_states,
            conclusion=conclusion,
            confidence_level=invalid_confidence,
            confidence_explanation=explanation,
            action_implications=implications,
            temporal_validity=validity,
            producing_engine=engine,
        )
        errors = obj.validate()
        assert len(errors) > 0, (
            f"Invalid confidence_level={invalid_confidence} "
            f"was not rejected by validate()"
        )
        assert any("confidence_level" in e for e in errors), (
            f"Errors {errors} do not mention 'confidence_level' "
            f"for invalid value={invalid_confidence}"
        )

    @given(
        reasoning_id=valid_reasoning_id_strategy,
        source_states=valid_source_semantic_states_strategy,
        conclusion=valid_conclusion_strategy,
        confidence=valid_confidence_level_strategy,
        explanation=valid_confidence_explanation_strategy,
        implications=valid_action_implications_strategy,
        validity=valid_temporal_validity_strategy,
        invalid_engine=invalid_producing_engine_strategy,
    )
    @settings(max_examples=200)
    def test_invalid_producing_engine_produces_errors(
        self,
        reasoning_id: str,
        source_states: list[str],
        conclusion: Conclusion,
        confidence: int,
        explanation: str,
        implications: list[ActionImplication],
        validity: TemporalValidity,
        invalid_engine: str,
    ) -> None:
        """Property 5: Invalid producing_engine (not in VALID_PRODUCING_ENGINES) always produces errors.

        **Validates: Requirements 9.1, 9.4**

        For any ReasoningObject with a producing_engine not in the valid set,
        validate() returns a non-empty error list mentioning producing_engine.
        """
        obj = ReasoningObject(
            reasoning_id=reasoning_id,
            source_semantic_states=source_states,
            conclusion=conclusion,
            confidence_level=confidence,
            confidence_explanation=explanation,
            action_implications=implications,
            temporal_validity=validity,
            producing_engine=invalid_engine,
        )
        errors = obj.validate()
        assert len(errors) > 0, (
            f"Invalid producing_engine={invalid_engine!r} "
            f"was not rejected by validate()"
        )
        assert any("producing_engine" in e for e in errors), (
            f"Errors {errors} do not mention 'producing_engine' "
            f"for invalid engine={invalid_engine!r}"
        )

    @given(
        invalid_id=invalid_reasoning_id_empty_strategy
        | invalid_reasoning_id_too_long_strategy,
        invalid_confidence=invalid_confidence_level_below_strategy
        | invalid_confidence_level_above_strategy,
        invalid_engine=invalid_producing_engine_strategy,
        conclusion=valid_conclusion_strategy,
        explanation=valid_confidence_explanation_strategy,
        implications=valid_action_implications_strategy,
        validity=valid_temporal_validity_strategy,
    )
    @settings(max_examples=200)
    def test_multiple_violations_produce_multiple_errors(
        self,
        invalid_id: str,
        invalid_confidence: int,
        invalid_engine: str,
        conclusion: Conclusion,
        explanation: str,
        implications: list[ActionImplication],
        validity: TemporalValidity,
    ) -> None:
        """Property 6: Multiple violations produce multiple errors.

        **Validates: Requirements 9.4**

        For any ReasoningObject with multiple invalid fields simultaneously,
        validate() returns multiple errors (at least one per violated field).
        """
        obj = ReasoningObject(
            reasoning_id=invalid_id,
            source_semantic_states=["valid_state_1"],
            conclusion=conclusion,
            confidence_level=invalid_confidence,
            confidence_explanation=explanation,
            action_implications=implications,
            temporal_validity=validity,
            producing_engine=invalid_engine,
        )
        errors = obj.validate()
        # At least 3 errors: reasoning_id, confidence_level, producing_engine
        assert len(errors) >= 3, (
            f"Expected at least 3 errors for 3 violations, got {len(errors)}: {errors}\n"
            f"Violations: reasoning_id={invalid_id!r}, "
            f"confidence_level={invalid_confidence}, "
            f"producing_engine={invalid_engine!r}"
        )
        # Each violated field should be mentioned
        assert any("reasoning_id" in e for e in errors), (
            f"Errors {errors} do not mention 'reasoning_id'"
        )
        assert any("confidence_level" in e for e in errors), (
            f"Errors {errors} do not mention 'confidence_level'"
        )
        assert any("producing_engine" in e for e in errors), (
            f"Errors {errors} do not mention 'producing_engine'"
        )
