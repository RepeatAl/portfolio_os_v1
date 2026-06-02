"""Property test: Cooldown Enforcement (Property 7).

**Property 7: Cooldown Enforcement**
**Validates: Requirements 7.1, 7.2, 7.3, 7.5**

Tests that:
- No two successful non-emergency transitions occur within cooldown_duration.
- Emergency overrides always succeed with cooldown_bypassed=True.
- Cooldown duration is clamped to [1.0, 24.0] hours.
- Repeated transitions inside cooldown window are rejected.
- Transitions after cooldown window expires are accepted.
- Emergency override requires non-empty bypass_reason (ValueError if empty).
- Emergency override records an audit event to ledger.
- Transition history records both accepted and rejected attempts.
"""

from __future__ import annotations

import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import yaml
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from governance.actor_identity import ActorIdentity, ActorType
from governance.mutation_audit_ledger import MutationAuditLedger
from governance.transition_cooldown import (
    CooldownConfig,
    TransitionCooldown,
    TRANSITION_EVENT_TYPE,
)


# --- Strategies ---

enforcement_modes = st.sampled_from(["observability", "soft", "hard"])

# Cooldown hours strategy: below, inside, and above allowed range
cooldown_hours_strategy = st.one_of(
    st.floats(min_value=0.01, max_value=0.99),   # Below minimum (should clamp to 1.0)
    st.floats(min_value=1.0, max_value=24.0),    # Inside valid range
    st.floats(min_value=24.01, max_value=100.0), # Above maximum (should clamp to 24.0)
)

# Strategy for generating transition sequences
transition_sequence_strategy = st.lists(
    st.tuples(
        st.integers(min_value=0, max_value=100),  # offset in minutes from base time
        st.booleans(),                             # is_emergency
    ),
    min_size=1,
    max_size=10,
)

bypass_reason_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
    min_size=1,
    max_size=50,
)


# --- Helpers ---

def _create_test_actor() -> ActorIdentity:
    """Create a test actor identity."""
    return ActorIdentity(
        actor_type=ActorType.USER,
        actor_id="test_user",
        context={},
        is_fallback=False,
    )


def _create_temp_config(cooldown_hours: float) -> str:
    """Create a temporary config.yaml with the given cooldown_hours."""
    config_data = {
        "enforcement_mode": "observability",
        "transition_hysteresis": {
            "cooldown_hours": cooldown_hours,
        },
    }
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        yaml.dump(config_data, f)
    return path


def _create_temp_ledger() -> tuple[str, MutationAuditLedger]:
    """Create a temporary ledger file and return path + ledger instance."""
    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    os.unlink(path)  # Let MutationAuditLedger create it fresh
    ledger = MutationAuditLedger(path)
    return path, ledger


# --- Property Tests ---


@given(hours=cooldown_hours_strategy)
@settings(max_examples=200)
def test_cooldown_config_clamping(hours: float) -> None:
    """CooldownConfig clamps duration_hours to [1.0, 24.0].

    **Validates: Requirements 7.1, 7.2**

    For any float value:
    - Values below 1.0 are clamped to 1.0
    - Values above 24.0 are clamped to 24.0
    - Values within [1.0, 24.0] remain unchanged
    """
    config = CooldownConfig(duration_hours=hours)
    assert 1.0 <= config.duration_hours <= 24.0

    if hours < 1.0:
        assert config.duration_hours == 1.0
    elif hours > 24.0:
        assert config.duration_hours == 24.0
    else:
        assert config.duration_hours == hours


@given(hours=cooldown_hours_strategy)
@settings(max_examples=200)
def test_cooldown_config_loaded_from_yaml_is_clamped(hours: float) -> None:
    """TransitionCooldown.load_config() clamps values from YAML to [1.0, 24.0].

    **Validates: Requirements 7.1, 7.2**

    Regardless of what value is written to config.yaml, the loaded config
    always has duration_hours within [1.0, 24.0].
    """
    config_path = _create_temp_config(hours)
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=None)
        loaded_config = cooldown._config
        assert 1.0 <= loaded_config.duration_hours <= 24.0

        if hours < 1.0:
            assert loaded_config.duration_hours == 1.0
        elif hours > 24.0:
            assert loaded_config.duration_hours == 24.0
        else:
            assert loaded_config.duration_hours == hours
    finally:
        os.unlink(config_path)


@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
)
@settings(max_examples=200)
def test_transition_accepted_when_no_cooldown_active(
    from_mode: str, to_mode: str
) -> None:
    """Transitions are accepted when no prior transition exists (no cooldown).

    **Validates: Requirements 7.1, 7.3**

    With an empty ledger (no prior transitions), any transition attempt
    should be accepted.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(4.0)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        attempt = cooldown.attempt_transition(
            from_mode=from_mode,
            to_mode=to_mode,
            actor=actor,
        )
        assert attempt.result == "accepted"
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)


@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
)
@settings(max_examples=200)
def test_repeated_transition_inside_cooldown_rejected(
    from_mode: str, to_mode: str
) -> None:
    """Repeated transitions inside cooldown window are rejected.

    **Validates: Requirements 7.1, 7.2**

    After a successful transition, a second non-emergency transition
    attempted immediately (within the cooldown window) must be rejected.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(4.0)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        # First transition — should be accepted
        first = cooldown.attempt_transition(
            from_mode=from_mode,
            to_mode=to_mode,
            actor=actor,
        )
        assert first.result == "accepted"

        # Second transition immediately — should be rejected (within cooldown)
        second = cooldown.attempt_transition(
            from_mode=to_mode,
            to_mode=from_mode,
            actor=actor,
        )
        assert second.result == "rejected_cooldown"
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)


@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
    bypass_reason=bypass_reason_strategy,
)
@settings(max_examples=200)
def test_emergency_override_bypasses_cooldown(
    from_mode: str, to_mode: str, bypass_reason: str
) -> None:
    """Emergency overrides always succeed regardless of cooldown state.

    **Validates: Requirements 7.3, 7.5**

    Even when cooldown is active, an emergency override with a valid
    bypass_reason must succeed with result 'accepted_emergency'.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(4.0)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        # First transition to activate cooldown
        first = cooldown.attempt_transition(
            from_mode=from_mode,
            to_mode=to_mode,
            actor=actor,
        )
        assert first.result == "accepted"

        # Emergency override during cooldown — must succeed
        emergency = cooldown.attempt_transition(
            from_mode=to_mode,
            to_mode=from_mode,
            actor=actor,
            is_emergency=True,
            bypass_reason=bypass_reason,
        )
        assert emergency.result == "accepted_emergency"
        assert emergency.is_emergency is True
        assert emergency.bypass_reason == bypass_reason
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)



@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
)
@settings(max_examples=200)
def test_emergency_override_empty_reason_raises_valueerror(
    from_mode: str, to_mode: str
) -> None:
    """Emergency override with empty bypass_reason raises ValueError.

    **Validates: Requirements 7.5**

    Emergency overrides require a non-empty bypass_reason for mandatory
    audit logging. Passing None or empty string must raise ValueError.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(4.0)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        # Empty string bypass_reason
        import pytest

        with pytest.raises(ValueError):
            cooldown.attempt_transition(
                from_mode=from_mode,
                to_mode=to_mode,
                actor=actor,
                is_emergency=True,
                bypass_reason="",
            )

        # None bypass_reason
        with pytest.raises(ValueError):
            cooldown.attempt_transition(
                from_mode=from_mode,
                to_mode=to_mode,
                actor=actor,
                is_emergency=True,
                bypass_reason=None,
            )
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)


@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
    bypass_reason=bypass_reason_strategy,
)
@settings(max_examples=200)
def test_emergency_override_records_audit_event(
    from_mode: str, to_mode: str, bypass_reason: str
) -> None:
    """Emergency override records an audit event with cooldown_bypassed=True.

    **Validates: Requirements 7.5**

    When an emergency override is performed, the ledger must contain an
    entry with cooldown_bypassed=True and the bypass_reason recorded.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(4.0)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        # Perform emergency override
        cooldown.attempt_transition(
            from_mode=from_mode,
            to_mode=to_mode,
            actor=actor,
            is_emergency=True,
            bypass_reason=bypass_reason,
        )

        # Check ledger for the audit event
        entries = ledger.query_by_event_type(TRANSITION_EVENT_TYPE)
        assert len(entries) >= 1

        # Find the emergency entry
        emergency_entries = [
            e for e in entries
            if e.details.get("cooldown_bypassed") is True
        ]
        assert len(emergency_entries) >= 1

        last_emergency = emergency_entries[-1]
        assert last_emergency.details["bypass_reason"] == bypass_reason
        assert last_emergency.details["is_emergency"] is True
        assert last_emergency.details["result"] in ("accepted_emergency", "accepted")
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)


@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
)
@settings(max_examples=200)
def test_transition_history_records_both_accepted_and_rejected(
    from_mode: str, to_mode: str
) -> None:
    """Transition history records both accepted and rejected attempts.

    **Validates: Requirements 7.1, 7.2**

    After performing one accepted and one rejected transition, the
    query_transition_history() must return both attempts.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(4.0)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        # First transition — accepted
        cooldown.attempt_transition(
            from_mode=from_mode,
            to_mode=to_mode,
            actor=actor,
        )

        # Second transition — rejected (within cooldown)
        cooldown.attempt_transition(
            from_mode=to_mode,
            to_mode=from_mode,
            actor=actor,
        )

        # Query history
        history = cooldown.query_transition_history()
        assert len(history) == 2

        results = [h.result for h in history]
        assert "accepted" in results
        assert "rejected_cooldown" in results
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)


@given(
    sequence=transition_sequence_strategy,
    cooldown_hours=st.floats(min_value=1.0, max_value=4.0),
)
@settings(max_examples=200, deadline=None)
def test_no_two_successful_non_emergency_within_cooldown(
    sequence: list[tuple[int, bool]],
    cooldown_hours: float,
) -> None:
    """No two successful non-emergency transitions within cooldown_duration.

    **Validates: Requirements 7.1, 7.2, 7.3**

    For any generated sequence of (offset_minutes, is_emergency) pairs,
    after replaying through the cooldown system, no two successful
    non-emergency transitions have timestamps less than cooldown_duration apart.
    """
    config_path = _create_temp_config(cooldown_hours)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()
        modes = ["observability", "soft", "hard"]

        # Sort sequence by offset to ensure chronological order
        sorted_sequence = sorted(sequence, key=lambda x: x[0])

        base_time = datetime.now(timezone.utc)
        successful_non_emergency_times: list[datetime] = []

        for i, (offset_minutes, is_emergency) in enumerate(sorted_sequence):
            current_time = base_time + timedelta(minutes=offset_minutes)
            from_mode = modes[i % len(modes)]
            to_mode = modes[(i + 1) % len(modes)]

            # Mock datetime.now to control time
            with patch(
                "governance.transition_cooldown.datetime"
            ) as mock_dt:
                mock_dt.now.return_value = current_time
                mock_dt.fromisoformat = datetime.fromisoformat
                mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

                try:
                    if is_emergency:
                        attempt = cooldown.attempt_transition(
                            from_mode=from_mode,
                            to_mode=to_mode,
                            actor=actor,
                            is_emergency=True,
                            bypass_reason="test emergency bypass",
                        )
                    else:
                        attempt = cooldown.attempt_transition(
                            from_mode=from_mode,
                            to_mode=to_mode,
                            actor=actor,
                        )

                    # Track successful non-emergency transitions
                    if attempt.result == "accepted" and not is_emergency:
                        successful_non_emergency_times.append(current_time)
                except ValueError:
                    # Emergency with empty reason — skip
                    pass

        # Verify: no two successful non-emergency transitions within cooldown
        cooldown_delta = timedelta(hours=cooldown_hours)
        for i in range(len(successful_non_emergency_times)):
            for j in range(i + 1, len(successful_non_emergency_times)):
                time_diff = (
                    successful_non_emergency_times[j]
                    - successful_non_emergency_times[i]
                )
                assert time_diff >= cooldown_delta, (
                    f"Two successful non-emergency transitions within cooldown: "
                    f"{successful_non_emergency_times[i]} and "
                    f"{successful_non_emergency_times[j]} "
                    f"(diff={time_diff}, cooldown={cooldown_delta})"
                )
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)


@given(
    from_mode=enforcement_modes,
    to_mode=enforcement_modes,
    cooldown_hours=st.floats(min_value=1.0, max_value=2.0),
)
@settings(max_examples=200, deadline=None)
def test_transition_after_cooldown_expires_is_accepted(
    from_mode: str, to_mode: str, cooldown_hours: float
) -> None:
    """Transitions after cooldown window expires are accepted.

    **Validates: Requirements 7.1, 7.3**

    After the cooldown period has elapsed since the last successful
    transition, a new non-emergency transition must be accepted.
    """
    assume(from_mode != to_mode)

    config_path = _create_temp_config(cooldown_hours)
    ledger_path, ledger = _create_temp_ledger()
    try:
        cooldown = TransitionCooldown(config_path=config_path, ledger=ledger)
        actor = _create_test_actor()

        # First transition — accepted
        base_time = datetime.now(timezone.utc)
        with patch("governance.transition_cooldown.datetime") as mock_dt:
            mock_dt.now.return_value = base_time
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

            first = cooldown.attempt_transition(
                from_mode=from_mode,
                to_mode=to_mode,
                actor=actor,
            )
            assert first.result == "accepted"

        # Second transition after cooldown expires — should be accepted
        after_cooldown = base_time + timedelta(hours=cooldown_hours, seconds=1)
        with patch("governance.transition_cooldown.datetime") as mock_dt:
            mock_dt.now.return_value = after_cooldown
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

            second = cooldown.attempt_transition(
                from_mode=to_mode,
                to_mode=from_mode,
                actor=actor,
            )
            assert second.result == "accepted"
    finally:
        os.unlink(config_path)
        os.unlink(ledger_path)
