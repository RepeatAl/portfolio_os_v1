"""Enforcement mode transition cooldown (anti-flapping guard).

Prevents rapid enforcement mode oscillation by enforcing a configurable
cooldown period between transitions. All transition attempts (successful,
rejected, and emergency-bypassed) are recorded to the Mutation Audit Ledger.

Reads configuration from .domainization/config.yaml under the
'transition_hysteresis' section. Cooldown duration is clamped to [1.0, 24.0]
hours with a default of 4.0 hours.

Emergency overrides (is_emergency=True) bypass the cooldown entirely but
require a mandatory bypass_reason for audit logging.

Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import yaml

from governance.actor_identity import ActorIdentity
from governance.mutation_audit_ledger import LedgerEntry, MutationAuditLedger

logger = logging.getLogger(__name__)

# Event type used for all enforcement mode transition records
TRANSITION_EVENT_TYPE = "enforcement_mode_rollback"


@dataclass
class CooldownConfig:
    """Configuration for the transition cooldown period.

    Attributes:
        duration_hours: Cooldown duration in hours, clamped to [1.0, 24.0].
    """

    duration_hours: float = 4.0

    def __post_init__(self) -> None:
        """Clamp duration_hours to the valid range [1.0, 24.0]."""
        self.duration_hours = max(1.0, min(24.0, self.duration_hours))


@dataclass
class CooldownState:
    """Current state of the transition cooldown.

    Attributes:
        is_active: True if cooldown is currently in effect.
        last_transition_time: ISO 8601 timestamp of last successful transition,
            or None if no transition has ever occurred.
        cooldown_expires_at: ISO 8601 timestamp when cooldown expires,
            or None if not active.
        remaining_seconds: Seconds remaining in cooldown, 0.0 if not active.
    """

    is_active: bool
    last_transition_time: str | None
    cooldown_expires_at: str | None
    remaining_seconds: float

    @property
    def remaining(self) -> float:
        """Return remaining cooldown seconds, clamped to non-negative."""
        return max(0.0, self.remaining_seconds)


@dataclass
class TransitionAttempt:
    """Record of a single enforcement mode transition attempt.

    Attributes:
        attempt_id: Unique identifier for this attempt (UUID v4).
        timestamp: ISO 8601 timestamp of the attempt.
        from_mode: Source enforcement mode.
        to_mode: Target enforcement mode.
        is_emergency: Whether this was an emergency override.
        bypass_reason: Reason for emergency bypass, or None.
        result: One of "accepted", "rejected_cooldown", "accepted_emergency".
        cooldown_remaining_seconds: Seconds remaining at time of attempt.
    """

    attempt_id: str
    timestamp: str
    from_mode: str
    to_mode: str
    is_emergency: bool
    bypass_reason: str | None
    result: str  # "accepted", "rejected_cooldown", "accepted_emergency"
    cooldown_remaining_seconds: float


class TransitionCooldown:
    """Enforcement mode transition cooldown (anti-flapping).

    Reads config from .domainization/config.yaml under 'transition_hysteresis'.
    Persists all attempts (success + rejection) to Mutation_Audit_Ledger.

    Usage:
        cooldown = TransitionCooldown(
            config_path=".domainization/config.yaml",
            ledger=MutationAuditLedger(".domainization/mutation_audit_ledger.yaml"),
        )
        attempt = cooldown.attempt_transition(
            from_mode="observability",
            to_mode="soft",
            actor=ActorIdentity.from_environment(),
        )
        if attempt.result == "accepted":
            # Transition allowed
            ...
    """

    def __init__(
        self,
        config_path: str,
        ledger: MutationAuditLedger | None = None,
    ) -> None:
        """Initialize the transition cooldown.

        Args:
            config_path: Path to .domainization/config.yaml.
            ledger: Optional MutationAuditLedger instance. If None, ledger
                operations are skipped (backward compatible).
        """
        self._config_path = config_path
        self._ledger = ledger
        self._config = self.load_config()

    def load_config(self) -> CooldownConfig:
        """Load cooldown duration from config.yaml.

        Reads the 'transition_hysteresis.cooldown_hours' value.
        Clamps to [1.0, 24.0] range. Defaults to 4.0 if missing or unreadable.

        Returns:
            CooldownConfig with the configured (and clamped) duration.
        """
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            if not isinstance(config_data, dict):
                logger.warning(
                    "Config file %s is not a valid YAML mapping. "
                    "Using default cooldown of 4.0 hours.",
                    self._config_path,
                )
                return CooldownConfig()

            hysteresis = config_data.get("transition_hysteresis", {})
            if not isinstance(hysteresis, dict):
                logger.warning(
                    "transition_hysteresis section is not a mapping. "
                    "Using default cooldown of 4.0 hours.",
                )
                return CooldownConfig()

            raw_hours = hysteresis.get("cooldown_hours", 4.0)
            try:
                duration = float(raw_hours)
            except (TypeError, ValueError):
                logger.warning(
                    "Invalid cooldown_hours value '%s'. "
                    "Using default cooldown of 4.0 hours.",
                    raw_hours,
                )
                return CooldownConfig()

            config = CooldownConfig(duration_hours=duration)

            # Warn if clamping occurred
            if duration < 1.0 or duration > 24.0:
                logger.warning(
                    "cooldown_hours=%s clamped to %s (valid range: [1.0, 24.0]).",
                    duration,
                    config.duration_hours,
                )

            return config

        except (OSError, yaml.YAMLError) as exc:
            logger.warning(
                "Failed to read config from %s: %s. "
                "Using default cooldown of 4.0 hours.",
                self._config_path,
                exc,
            )
            return CooldownConfig()

    def get_cooldown_state(self) -> CooldownState:
        """Query ledger for last successful transition to determine cooldown state.

        Searches the ledger for the most recent successful transition event
        (event_type='enforcement_mode_rollback' with details.success=True or
        details.result in ['accepted', 'accepted_emergency']).

        Returns:
            CooldownState indicating whether cooldown is active and remaining time.
        """
        if self._ledger is None:
            return CooldownState(
                is_active=False,
                last_transition_time=None,
                cooldown_expires_at=None,
                remaining_seconds=0.0,
            )

        # Query all transition events from the ledger
        entries = self._ledger.query_by_event_type(TRANSITION_EVENT_TYPE)

        # Find the last successful transition
        last_successful: LedgerEntry | None = None
        for entry in reversed(entries):
            details = entry.details
            result = details.get("result", details.get("success"))
            if result in ("accepted", "accepted_emergency", True):
                last_successful = entry
                break

        if last_successful is None:
            return CooldownState(
                is_active=False,
                last_transition_time=None,
                cooldown_expires_at=None,
                remaining_seconds=0.0,
            )

        # Calculate cooldown expiry
        last_ts = last_successful.timestamp
        try:
            last_dt = datetime.fromisoformat(last_ts)
            # Ensure timezone-aware
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            logger.warning(
                "Invalid timestamp in last transition entry: %s. "
                "Treating as no active cooldown.",
                last_ts,
            )
            return CooldownState(
                is_active=False,
                last_transition_time=last_ts,
                cooldown_expires_at=None,
                remaining_seconds=0.0,
            )

        cooldown_duration = timedelta(hours=self._config.duration_hours)
        expires_at = last_dt + cooldown_duration
        now = datetime.now(timezone.utc)

        remaining = (expires_at - now).total_seconds()
        is_active = remaining > 0.0

        return CooldownState(
            is_active=is_active,
            last_transition_time=last_ts,
            cooldown_expires_at=expires_at.isoformat() if is_active else None,
            remaining_seconds=remaining if is_active else 0.0,
        )

    def attempt_transition(
        self,
        from_mode: str,
        to_mode: str,
        actor: ActorIdentity,
        is_emergency: bool = False,
        bypass_reason: str | None = None,
    ) -> TransitionAttempt:
        """Attempt an enforcement mode transition.

        Checks cooldown state and either accepts or rejects the transition.
        Emergency overrides bypass cooldown with mandatory bypass_reason audit.
        All attempts (success, rejection, emergency) are recorded to the ledger.

        Args:
            from_mode: Current enforcement mode (e.g., "observability").
            to_mode: Target enforcement mode (e.g., "soft").
            actor: The ActorIdentity requesting the transition.
            is_emergency: If True, bypass cooldown (requires bypass_reason).
            bypass_reason: Mandatory reason string for emergency overrides.

        Returns:
            TransitionAttempt with the result of the attempt.

        Raises:
            ValueError: If is_emergency=True but bypass_reason is None or empty.
        """
        now = datetime.now(timezone.utc)
        attempt_id = str(uuid.uuid4())
        timestamp = now.isoformat()

        cooldown_state = self.get_cooldown_state()
        remaining = cooldown_state.remaining

        # Validate emergency override requirements
        if is_emergency and not bypass_reason:
            raise ValueError(
                "Emergency overrides require a non-empty bypass_reason "
                "for mandatory audit logging."
            )

        # Determine result
        if not cooldown_state.is_active:
            # No cooldown active — accept transition
            result = "accepted"
        elif is_emergency:
            # Emergency override — bypass cooldown
            result = "accepted_emergency"
        else:
            # Cooldown active, not emergency — reject
            result = "rejected_cooldown"

        attempt = TransitionAttempt(
            attempt_id=attempt_id,
            timestamp=timestamp,
            from_mode=from_mode,
            to_mode=to_mode,
            is_emergency=is_emergency,
            bypass_reason=bypass_reason if is_emergency else None,
            result=result,
            cooldown_remaining_seconds=remaining,
        )

        # Record to ledger
        self._record_attempt_to_ledger(attempt, actor)

        # Log the outcome
        if result == "rejected_cooldown":
            hours_remaining = remaining / 3600.0
            logger.warning(
                "Transition %s→%s rejected: cooldown active, %.1fh remaining.",
                from_mode,
                to_mode,
                hours_remaining,
            )
        elif result == "accepted_emergency":
            logger.info(
                "Transition %s→%s accepted via emergency override. "
                "Bypass reason: %s",
                from_mode,
                to_mode,
                bypass_reason,
            )
        else:
            logger.info(
                "Transition %s→%s accepted.",
                from_mode,
                to_mode,
            )

        return attempt

    def query_transition_history(self) -> list[TransitionAttempt]:
        """Return all transition attempts (success + rejected) from ledger.

        Returns:
            List of TransitionAttempt objects in chronological order.
            Returns empty list if no ledger is configured.
        """
        if self._ledger is None:
            return []

        entries = self._ledger.query_by_event_type(TRANSITION_EVENT_TYPE)
        attempts: list[TransitionAttempt] = []

        for entry in entries:
            details = entry.details
            attempt = TransitionAttempt(
                attempt_id=details.get("attempt_id", entry.entry_id),
                timestamp=entry.timestamp,
                from_mode=details.get("from_mode", "unknown"),
                to_mode=details.get("to_mode", "unknown"),
                is_emergency=details.get("is_emergency", False),
                bypass_reason=details.get("bypass_reason"),
                result=details.get("result", "unknown"),
                cooldown_remaining_seconds=details.get(
                    "cooldown_remaining_seconds", 0.0
                ),
            )
            attempts.append(attempt)

        return attempts

    def _record_attempt_to_ledger(
        self,
        attempt: TransitionAttempt,
        actor: ActorIdentity,
    ) -> None:
        """Record a transition attempt to the Mutation Audit Ledger.

        Args:
            attempt: The TransitionAttempt to record.
            actor: The actor who initiated the transition.
        """
        if self._ledger is None:
            logger.debug(
                "No ledger configured; skipping audit record for attempt %s.",
                attempt.attempt_id,
            )
            return

        # Determine severity based on result
        if attempt.result == "rejected_cooldown":
            severity = "WARNING"
        elif attempt.result == "accepted_emergency":
            severity = "WARNING"
        else:
            severity = "INFO"

        details: dict = {
            "attempt_id": attempt.attempt_id,
            "from_mode": attempt.from_mode,
            "to_mode": attempt.to_mode,
            "result": attempt.result,
            "is_emergency": attempt.is_emergency,
            "cooldown_remaining_seconds": attempt.cooldown_remaining_seconds,
        }

        if attempt.result == "rejected_cooldown":
            hours_remaining = attempt.cooldown_remaining_seconds / 3600.0
            details["rejection_reason"] = (
                f"cooldown active, {hours_remaining:.1f}h remaining"
            )

        if attempt.is_emergency and attempt.bypass_reason:
            details["bypass_reason"] = attempt.bypass_reason
            details["cooldown_bypassed"] = True
        else:
            details["cooldown_bypassed"] = False

        # Include success flag for backward compatibility with design doc format
        details["success"] = attempt.result in ("accepted", "accepted_emergency")

        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type=TRANSITION_EVENT_TYPE,
            timestamp=attempt.timestamp,
            actor=actor.to_dict(),
            governance_policy_version="unknown",
            severity=severity,
            details=details,
        )

        try:
            self._ledger.append(entry)
        except OSError as exc:
            # Fail soft — log to stderr, continue (per error handling spec)
            logger.error(
                "Failed to write transition attempt to ledger: %s. "
                "Continuing without audit record.",
                exc,
            )
