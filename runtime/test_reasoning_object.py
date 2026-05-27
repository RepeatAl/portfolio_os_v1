"""Unit tests for runtime/reasoning_object.py.

Tests TemporalValidity, ActionImplication, Conclusion, and ReasoningObject
dataclasses including the validate() method and validity_state property.
"""

from datetime import datetime, timezone, timedelta

import pytest

from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
    VALID_PRODUCING_ENGINES,
)


# --- Helpers ---

def _make_valid_temporal_validity() -> TemporalValidity:
    """Create a TemporalValidity that is currently valid."""
    now = datetime.now(timezone.utc)
    return TemporalValidity(
        valid_from=(now - timedelta(hours=1)).isoformat(),
        valid_until=(now + timedelta(hours=24)).isoformat(),
        stale_after=None,
    )


def _make_valid_reasoning_object(**overrides) -> ReasoningObject:
    """Create a valid ReasoningObject with optional field overrides."""
    defaults = {
        "reasoning_id": "ro-test-001",
        "source_semantic_states": ["state_1", "state_2"],
        "conclusion": Conclusion(summary="Test conclusion summary", category="allocation"),
        "confidence_level": 75,
        "confidence_explanation": "High confidence based on complete input data",
        "action_implications": [
            ActionImplication(action="Hold position", rationale="Strong momentum signal"),
        ],
        "temporal_validity": _make_valid_temporal_validity(),
        "producing_engine": "decision_engine",
        "schema_version": "1.0.0",
    }
    defaults.update(overrides)
    return ReasoningObject(**defaults)


# --- TemporalValidity Tests ---

class TestTemporalValidity:
    def test_valid_state_when_within_bounds(self):
        now = datetime.now(timezone.utc)
        tv = TemporalValidity(
            valid_from=(now - timedelta(hours=1)).isoformat(),
            valid_until=(now + timedelta(hours=24)).isoformat(),
            stale_after=None,
        )
        assert tv.validity_state == "valid"

    def test_expired_state_when_past_valid_until(self):
        now = datetime.now(timezone.utc)
        tv = TemporalValidity(
            valid_from=(now - timedelta(hours=48)).isoformat(),
            valid_until=(now - timedelta(hours=1)).isoformat(),
            stale_after=None,
        )
        assert tv.validity_state == "expired"

    def test_stale_state_when_past_stale_after(self):
        now = datetime.now(timezone.utc)
        tv = TemporalValidity(
            valid_from=(now - timedelta(hours=48)).isoformat(),
            valid_until=(now + timedelta(hours=24)).isoformat(),
            stale_after=(now - timedelta(hours=1)).isoformat(),
        )
        assert tv.validity_state == "stale"

    def test_valid_state_when_stale_after_is_future(self):
        now = datetime.now(timezone.utc)
        tv = TemporalValidity(
            valid_from=(now - timedelta(hours=1)).isoformat(),
            valid_until=(now + timedelta(hours=48)).isoformat(),
            stale_after=(now + timedelta(hours=24)).isoformat(),
        )
        assert tv.validity_state == "valid"

    def test_expired_with_invalid_valid_until(self):
        tv = TemporalValidity(
            valid_from="2026-01-01T00:00:00+00:00",
            valid_until="not-a-date",
            stale_after=None,
        )
        assert tv.validity_state == "expired"

    def test_stale_after_none_means_no_stale_state(self):
        now = datetime.now(timezone.utc)
        tv = TemporalValidity(
            valid_from=(now - timedelta(hours=1)).isoformat(),
            valid_until=(now + timedelta(hours=24)).isoformat(),
            stale_after=None,
        )
        assert tv.validity_state == "valid"


# --- ReasoningObject.validate() Tests ---

class TestReasoningObjectValidation:
    def test_valid_object_has_no_errors(self):
        ro = _make_valid_reasoning_object()
        assert ro.validate() == []

    def test_empty_reasoning_id(self):
        ro = _make_valid_reasoning_object(reasoning_id="")
        errors = ro.validate()
        assert any("reasoning_id" in e for e in errors)

    def test_reasoning_id_too_long(self):
        ro = _make_valid_reasoning_object(reasoning_id="x" * 129)
        errors = ro.validate()
        assert any("reasoning_id" in e and "128" in e for e in errors)

    def test_reasoning_id_at_max_length(self):
        ro = _make_valid_reasoning_object(reasoning_id="x" * 128)
        assert ro.validate() == []

    def test_empty_source_semantic_states(self):
        ro = _make_valid_reasoning_object(source_semantic_states=[])
        errors = ro.validate()
        assert any("source_semantic_states" in e and "at least 1" in e for e in errors)

    def test_too_many_source_semantic_states(self):
        ro = _make_valid_reasoning_object(
            source_semantic_states=[f"state_{i}" for i in range(51)]
        )
        errors = ro.validate()
        assert any("source_semantic_states" in e and "50" in e for e in errors)

    def test_source_semantic_states_with_empty_entry(self):
        ro = _make_valid_reasoning_object(source_semantic_states=["valid", ""])
        errors = ro.validate()
        assert any("source_semantic_states[1]" in e for e in errors)

    def test_empty_conclusion_summary(self):
        ro = _make_valid_reasoning_object(
            conclusion=Conclusion(summary="", category="allocation")
        )
        errors = ro.validate()
        assert any("conclusion.summary" in e for e in errors)

    def test_conclusion_summary_too_long(self):
        ro = _make_valid_reasoning_object(
            conclusion=Conclusion(summary="x" * 1001, category="allocation")
        )
        errors = ro.validate()
        assert any("conclusion.summary" in e and "1000" in e for e in errors)

    def test_empty_conclusion_category(self):
        ro = _make_valid_reasoning_object(
            conclusion=Conclusion(summary="Valid summary", category="")
        )
        errors = ro.validate()
        assert any("conclusion.category" in e for e in errors)

    def test_confidence_level_below_zero(self):
        ro = _make_valid_reasoning_object(confidence_level=-1)
        errors = ro.validate()
        assert any("confidence_level" in e for e in errors)

    def test_confidence_level_above_100(self):
        ro = _make_valid_reasoning_object(confidence_level=101)
        errors = ro.validate()
        assert any("confidence_level" in e for e in errors)

    def test_confidence_level_at_boundaries(self):
        ro_zero = _make_valid_reasoning_object(confidence_level=0)
        assert ro_zero.validate() == []
        ro_hundred = _make_valid_reasoning_object(confidence_level=100)
        assert ro_hundred.validate() == []

    def test_empty_confidence_explanation(self):
        ro = _make_valid_reasoning_object(confidence_explanation="")
        errors = ro.validate()
        assert any("confidence_explanation" in e for e in errors)

    def test_confidence_explanation_too_long(self):
        ro = _make_valid_reasoning_object(confidence_explanation="x" * 501)
        errors = ro.validate()
        assert any("confidence_explanation" in e and "500" in e for e in errors)

    def test_too_many_action_implications(self):
        ro = _make_valid_reasoning_object(
            action_implications=[
                ActionImplication(action=f"action_{i}", rationale=f"reason_{i}")
                for i in range(21)
            ]
        )
        errors = ro.validate()
        assert any("action_implications" in e and "20" in e for e in errors)

    def test_action_implication_empty_action(self):
        ro = _make_valid_reasoning_object(
            action_implications=[ActionImplication(action="", rationale="valid")]
        )
        errors = ro.validate()
        assert any("action_implications[0].action" in e for e in errors)

    def test_action_implication_empty_rationale(self):
        ro = _make_valid_reasoning_object(
            action_implications=[ActionImplication(action="valid", rationale="")]
        )
        errors = ro.validate()
        assert any("action_implications[0].rationale" in e for e in errors)

    def test_zero_action_implications_is_valid(self):
        ro = _make_valid_reasoning_object(action_implications=[])
        assert ro.validate() == []

    def test_invalid_producing_engine(self):
        ro = _make_valid_reasoning_object(producing_engine="invalid_engine")
        errors = ro.validate()
        assert any("producing_engine" in e for e in errors)

    def test_all_valid_producing_engines(self):
        for engine in VALID_PRODUCING_ENGINES:
            ro = _make_valid_reasoning_object(producing_engine=engine)
            assert ro.validate() == [], f"Failed for engine: {engine}"

    def test_empty_schema_version(self):
        ro = _make_valid_reasoning_object(schema_version="")
        errors = ro.validate()
        assert any("schema_version" in e for e in errors)

    def test_multiple_errors_reported(self):
        ro = _make_valid_reasoning_object(
            reasoning_id="",
            source_semantic_states=[],
            confidence_level=200,
            producing_engine="bad",
        )
        errors = ro.validate()
        assert len(errors) >= 4
