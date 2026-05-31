"""Unit tests for governance/transition_cooldown.py.

Covers deterministic edge cases: config clamping (below min, above max,
missing section), cooldown rejection message, and emergency bypass semantics.

Does NOT duplicate property tests (cooldown enforcement across generated
transition sequences).

Validates: Requirements 7.4
"""

from __future__ import annotations

import os
import tempfile

import pytest
import yaml

from governance.actor_identity import ActorIdentity, ActorType
from governance.mutation_audit_ledger import MutationAuditLedger
from governance.transition_cooldown import (
    CooldownConfig,
    CooldownState,
    TransitionAttempt,
    TransitionCooldown,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_dir():
    """Provide a temporary directory for test YAML files."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def ledger(tmp_dir: str) -> MutationAuditLedger:
    """Create a temporary ledger for testing."""
    ledger_path = os.path.join(tmp_dir, "ledger.yaml")
    return MutationAuditLedger(ledger_path)


@pytest.fixture
def test_actor() -> ActorIdentity:
    """Create a test actor identity."""
    return ActorIdentity(
        actor_type=ActorType.USER,
        actor_id="test_user",
        context={},
        is_fallback=False,
    )


def _write_config(tmp_dir: str, config_data: dict) -> str:
    """Write a config.yaml file and return its path."""
    path = os.path.join(tmp_dir, "config.yaml")
    with open(path, "w") as f:
        yaml.dump(config_data, f)
    return path


# ---------------------------------------------------------------------------
# Test: CooldownConfig Clamping
# ---------------------------------------------------------------------------


class TestCooldownConfigClamping:
    """Tests for config duration clamping to [1.0, 24.0] range."""

    def test_clamp_below_minimum(self):
        """Duration below 1.0 is clamped to 1.0."""
        config = CooldownConfig(duration_hours=0.5)
        assert config.duration_hours == 1.0

    def test_clamp_above_maximum(self):
        """Duration above 24.0 is clamped to 24.0."""
        config = CooldownConfig(duration_hours=30.0)
        assert config.duration_hours == 24.0

    def test_valid_duration_unchanged(self):
        """Duration within [1.0, 24.0] is not modified."""
        config = CooldownConfig(duration_hours=4.0)
        assert config.duration_hours == 4.0

    def test_minimum_boundary(self):
        """Duration exactly 1.0 is accepted."""
        config = CooldownConfig(duration_hours=1.0)
        assert config.duration_hours == 1.0

    def test_maximum_boundary(self):
        """Duration exactly 24.0 is accepted."""
        config = CooldownConfig(duration_hours=24.0)
        assert config.duration_hours == 24.0

    def test_negative_duration_clamped(self):
        """Negative duration is clamped to 1.0."""
        config = CooldownConfig(duration_hours=-5.0)
        assert config.duration_hours == 1.0


# ---------------------------------------------------------------------------
# Test: Config Loading from YAML
# ---------------------------------------------------------------------------


class TestConfigLoading:
    """Tests for loading cooldown config from config.yaml."""

    def test_load_valid_config(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Valid transition_hysteresis section loads correctly."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 6}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)
        assert cooldown._config.duration_hours == 6.0

    def test_missing_transition_hysteresis_section(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Missing transition_hysteresis section defaults to 4.0 hours."""
        path = _write_config(tmp_dir, {"enforcement_mode": "observability"})
        cooldown = TransitionCooldown(path, ledger=ledger)
        assert cooldown._config.duration_hours == 4.0

    def test_config_below_min_clamped(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Config value below 1.0 is clamped to 1.0."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 0.3}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)
        assert cooldown._config.duration_hours == 1.0

    def test_config_above_max_clamped(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Config value above 24.0 is clamped to 24.0."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 48}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)
        assert cooldown._config.duration_hours == 24.0

    def test_missing_config_file_defaults(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Non-existent config file defaults to 4.0 hours (fail_soft)."""
        path = os.path.join(tmp_dir, "nonexistent_config.yaml")
        cooldown = TransitionCooldown(path, ledger=ledger)
        assert cooldown._config.duration_hours == 4.0

    def test_invalid_cooldown_hours_value(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Non-numeric cooldown_hours value defaults to 4.0 hours."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": "not_a_number"}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)
        assert cooldown._config.duration_hours == 4.0


# ---------------------------------------------------------------------------
# Test: Cooldown Rejection Message
# ---------------------------------------------------------------------------


class TestCooldownRejection:
    """Tests for cooldown rejection behavior and messaging."""

    def test_first_transition_accepted(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """First transition (no prior transitions) is always accepted."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        attempt = cooldown.attempt_transition(
            from_mode="observability",
            to_mode="soft",
            actor=test_actor,
        )

        assert attempt.result == "accepted"

    def test_second_transition_within_cooldown_rejected(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Second transition within cooldown window is rejected."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        # First transition — accepted
        attempt1 = cooldown.attempt_transition(
            from_mode="observability",
            to_mode="soft",
            actor=test_actor,
        )
        assert attempt1.result == "accepted"

        # Second transition immediately after — rejected
        attempt2 = cooldown.attempt_transition(
            from_mode="soft",
            to_mode="hard",
            actor=test_actor,
        )
        assert attempt2.result == "rejected_cooldown"
        assert attempt2.cooldown_remaining_seconds > 0

    def test_emergency_override_bypasses_cooldown(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Emergency override bypasses active cooldown."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        # First transition — accepted
        cooldown.attempt_transition(
            from_mode="observability",
            to_mode="soft",
            actor=test_actor,
        )

        # Emergency override during cooldown — accepted
        attempt = cooldown.attempt_transition(
            from_mode="soft",
            to_mode="observability",
            actor=test_actor,
            is_emergency=True,
            bypass_reason="Critical production issue requires rollback",
        )

        assert attempt.result == "accepted_emergency"
        assert attempt.bypass_reason == "Critical production issue requires rollback"

    def test_emergency_without_bypass_reason_raises(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Emergency override without bypass_reason raises ValueError."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        with pytest.raises(ValueError, match="bypass_reason"):
            cooldown.attempt_transition(
                from_mode="observability",
                to_mode="soft",
                actor=test_actor,
                is_emergency=True,
                bypass_reason=None,
            )

    def test_emergency_with_empty_bypass_reason_raises(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Emergency override with empty bypass_reason raises ValueError."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        with pytest.raises(ValueError, match="bypass_reason"):
            cooldown.attempt_transition(
                from_mode="observability",
                to_mode="soft",
                actor=test_actor,
                is_emergency=True,
                bypass_reason="",
            )


# ---------------------------------------------------------------------------
# Test: Transition History
# ---------------------------------------------------------------------------


class TestTransitionHistory:
    """Tests for transition history recording."""

    def test_accepted_transition_recorded_in_history(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Accepted transitions appear in query_transition_history."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        cooldown.attempt_transition(
            from_mode="observability",
            to_mode="soft",
            actor=test_actor,
        )

        history = cooldown.query_transition_history()
        assert len(history) == 1
        assert history[0].from_mode == "observability"
        assert history[0].to_mode == "soft"
        assert history[0].result == "accepted"

    def test_rejected_transition_recorded_in_history(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Rejected transitions also appear in query_transition_history."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=ledger)

        # First — accepted
        cooldown.attempt_transition(
            from_mode="observability", to_mode="soft", actor=test_actor
        )
        # Second — rejected
        cooldown.attempt_transition(
            from_mode="soft", to_mode="hard", actor=test_actor
        )

        history = cooldown.query_transition_history()
        assert len(history) == 2
        assert history[0].result == "accepted"
        assert history[1].result == "rejected_cooldown"

    def test_no_ledger_returns_empty_history(self, tmp_dir: str):
        """query_transition_history returns empty list when no ledger."""
        path = _write_config(tmp_dir, {
            "transition_hysteresis": {"cooldown_hours": 4}
        })
        cooldown = TransitionCooldown(path, ledger=None)

        history = cooldown.query_transition_history()
        assert history == []
