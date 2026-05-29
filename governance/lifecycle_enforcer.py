"""Lifecycle enforcement for artifact state transitions.

Validates lifecycle transitions against the state machine, enforces read-only
state protection, and gates regenerable state overwrites. Produces structured
GateResult objects respecting the configured enforcement mode.

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.1, 9.2, 9.3, 9.4, 10.1, 10.2, 10.3, 10.4
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

from governance.gate_framework import GateResult

logger = logging.getLogger(__name__)

# Valid enforcement modes
VALID_ENFORCEMENT_MODES = frozenset({"observability", "soft", "hard"})


class LifecycleEnforcer:
    """Enforces lifecycle state machine rules for artifact transitions.

    Validates transitions against the lifecycle state machine YAML,
    protects read-only states from content modification, and gates
    regenerable state overwrites by non-engine actors.

    Attributes:
        state_machine: Parsed lifecycle state machine configuration.
        enforcement_mode: Current enforcement mode (observability/soft/hard).
    """

    def __init__(self, state_machine_path: str, enforcement_mode: str) -> None:
        """Initialize the lifecycle enforcer.

        Args:
            state_machine_path: Path to the lifecycle_state_machine.yaml file.
            enforcement_mode: One of 'observability', 'soft', or 'hard'.

        Raises:
            ValueError: If enforcement_mode is not valid.
            FileNotFoundError: If state_machine_path does not exist.
            yaml.YAMLError: If the YAML file is malformed.
        """
        if enforcement_mode not in VALID_ENFORCEMENT_MODES:
            raise ValueError(
                f"Invalid enforcement_mode '{enforcement_mode}'. "
                f"Must be one of: {sorted(VALID_ENFORCEMENT_MODES)}"
            )

        self.enforcement_mode = enforcement_mode
        self.state_machine_path = Path(state_machine_path)
        self.state_machine: dict = self._load_state_machine()

    def _load_state_machine(self) -> dict:
        """Load and validate the lifecycle state machine YAML.

        Returns:
            Parsed state machine dictionary keyed by artifact type.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            yaml.YAMLError: If the YAML is malformed.
            ValueError: If the YAML structure is invalid.
        """
        if not self.state_machine_path.exists():
            raise FileNotFoundError(
                f"Lifecycle state machine not found: {self.state_machine_path}"
            )

        try:
            with open(self.state_machine_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(
                f"Failed to parse lifecycle state machine: {e}"
            ) from e

        if not isinstance(data, dict) or "artifact_types" not in data:
            raise ValueError(
                "Lifecycle state machine YAML must contain 'artifact_types' key"
            )

        return data["artifact_types"]

    def _get_valid_transitions(self, artifact_type: str) -> list[tuple[str, str]]:
        """Get valid (from_state, to_state) pairs for an artifact type.

        Args:
            artifact_type: The artifact type to look up.

        Returns:
            List of (from_state, to_state) tuples representing valid transitions.
        """
        type_config = self.state_machine.get(artifact_type, {})
        transitions = type_config.get("transitions", [])
        return [(t["from"], t["to"]) for t in transitions]

    def _get_read_only_states(self, artifact_type: str) -> list[str]:
        """Get read-only states for an artifact type.

        Args:
            artifact_type: The artifact type to look up.

        Returns:
            List of state names that are read-only.
        """
        type_config = self.state_machine.get(artifact_type, {})
        return type_config.get("read_only_states", [])

    def _get_regenerable_states(self, artifact_type: str) -> list[str]:
        """Get regenerable states for an artifact type.

        Args:
            artifact_type: The artifact type to look up.

        Returns:
            List of state names that are regenerable.
        """
        type_config = self.state_machine.get(artifact_type, {})
        return type_config.get("regenerable_states", [])

    def _make_timestamp(self) -> str:
        """Generate an ISO 8601 UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    def _get_enforcement_action(self, is_valid: bool) -> str:
        """Determine enforcement action based on mode and validity.

        Args:
            is_valid: Whether the check passed.

        Returns:
            Enforcement action string: 'info', 'warn', or 'block'.
        """
        if is_valid:
            return "info"

        if self.enforcement_mode == "observability":
            return "warn"
        else:
            # Both soft and hard modes block invalid operations
            return "block"

    def validate_transition(
        self, artifact_id: str, artifact_type: str, from_state: str, to_state: str
    ) -> GateResult:
        """Validate a lifecycle transition against the state machine.

        Checks whether the requested transition is valid according to the
        lifecycle state machine definition for the given artifact type.

        Args:
            artifact_id: Identifier of the artifact being transitioned.
            artifact_type: The artifact's type (e.g., SSOT, ENGINE, REPORT_OUT).
            from_state: Current lifecycle state.
            to_state: Requested target lifecycle state.

        Returns:
            GateResult with status 'pass' if transition is valid,
            'fail' if invalid.
        """
        start_time = time.perf_counter()

        # Check if artifact type exists in state machine
        if artifact_type not in self.state_machine:
            duration_ms = (time.perf_counter() - start_time) * 1000
            return GateResult(
                gate_name="lifecycle_transition_validation",
                status="fail",
                enforcement_action=self._get_enforcement_action(is_valid=False),
                duration_ms=duration_ms,
                details=[
                    f"Unknown artifact type '{artifact_type}' for artifact '{artifact_id}'"
                ],
                timestamp=self._make_timestamp(),
            )

        valid_transitions = self._get_valid_transitions(artifact_type)
        is_valid = (from_state, to_state) in valid_transitions

        duration_ms = (time.perf_counter() - start_time) * 1000

        if is_valid:
            return GateResult(
                gate_name="lifecycle_transition_validation",
                status="pass",
                enforcement_action="info",
                duration_ms=duration_ms,
                details=[
                    f"Transition '{from_state}' -> '{to_state}' is valid "
                    f"for artifact '{artifact_id}' (type: {artifact_type})"
                ],
                timestamp=self._make_timestamp(),
            )
        else:
            valid_from_current = [
                t[1] for t in valid_transitions if t[0] == from_state
            ]
            return GateResult(
                gate_name="lifecycle_transition_validation",
                status="fail",
                enforcement_action=self._get_enforcement_action(is_valid=False),
                duration_ms=duration_ms,
                details=[
                    f"Invalid transition '{from_state}' -> '{to_state}' "
                    f"for artifact '{artifact_id}' (type: {artifact_type}). "
                    f"Valid transitions from '{from_state}': {valid_from_current}"
                ],
                timestamp=self._make_timestamp(),
            )

    def is_read_only(self, artifact_type: str, current_state: str) -> bool:
        """Check if an artifact type in a given state is read-only.

        Args:
            artifact_type: The artifact's type.
            current_state: The artifact's current lifecycle state.

        Returns:
            True if the state is read-only for this artifact type.
        """
        read_only_states = self._get_read_only_states(artifact_type)
        return current_state in read_only_states

    def is_regenerable(self, artifact_type: str, current_state: str) -> bool:
        """Check if an artifact type in a given state is regenerable.

        Args:
            artifact_type: The artifact's type.
            current_state: The artifact's current lifecycle state.

        Returns:
            True if the state is regenerable for this artifact type.
        """
        regenerable_states = self._get_regenerable_states(artifact_type)
        return current_state in regenerable_states


    def enforce_transition(
        self, artifact_id: str, artifact_type: str, from_state: str, to_state: str
    ) -> GateResult:
        """Enforce a lifecycle transition respecting the enforcement mode.

        In observability mode, invalid transitions produce a warning but are
        permitted (status=pass, enforcement_action=warn).
        In soft mode, invalid transitions are rejected with a structured warning
        (status=fail, enforcement_action=block).
        In hard mode, invalid transitions are rejected with an enforcement error
        (status=fail, enforcement_action=block).

        Args:
            artifact_id: Identifier of the artifact being transitioned.
            artifact_type: The artifact's type.
            from_state: Current lifecycle state.
            to_state: Requested target lifecycle state.

        Returns:
            GateResult indicating whether the transition is permitted.
        """
        start_time = time.perf_counter()

        # Check if artifact type exists in state machine
        if artifact_type not in self.state_machine:
            duration_ms = (time.perf_counter() - start_time) * 1000
            detail_msg = (
                f"Unknown artifact type '{artifact_type}' for artifact '{artifact_id}'"
            )
            if self.enforcement_mode == "observability":
                logger.warning(detail_msg)
                return GateResult(
                    gate_name="lifecycle_transition_enforcement",
                    status="pass",
                    enforcement_action="warn",
                    duration_ms=duration_ms,
                    details=[detail_msg],
                    timestamp=self._make_timestamp(),
                )
            else:
                return GateResult(
                    gate_name="lifecycle_transition_enforcement",
                    status="fail",
                    enforcement_action="block",
                    duration_ms=duration_ms,
                    details=[detail_msg],
                    timestamp=self._make_timestamp(),
                )

        valid_transitions = self._get_valid_transitions(artifact_type)
        is_valid = (from_state, to_state) in valid_transitions

        duration_ms = (time.perf_counter() - start_time) * 1000

        if is_valid:
            return GateResult(
                gate_name="lifecycle_transition_enforcement",
                status="pass",
                enforcement_action="info",
                duration_ms=duration_ms,
                details=[
                    f"Transition '{from_state}' -> '{to_state}' permitted "
                    f"for artifact '{artifact_id}' (type: {artifact_type})"
                ],
                timestamp=self._make_timestamp(),
            )

        # Invalid transition — behavior depends on enforcement mode
        valid_from_current = [
            t[1] for t in valid_transitions if t[0] == from_state
        ]
        detail_msg = (
            f"Invalid transition '{from_state}' -> '{to_state}' "
            f"for artifact '{artifact_id}' (type: {artifact_type}). "
            f"Valid transitions from '{from_state}': {valid_from_current}"
        )

        if self.enforcement_mode == "observability":
            logger.warning(detail_msg)
            return GateResult(
                gate_name="lifecycle_transition_enforcement",
                status="pass",
                enforcement_action="warn",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
        elif self.enforcement_mode == "soft":
            logger.warning(f"[SOFT BLOCK] {detail_msg}")
            return GateResult(
                gate_name="lifecycle_transition_enforcement",
                status="fail",
                enforcement_action="block",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
        else:
            # hard mode
            logger.error(f"[HARD BLOCK] {detail_msg}")
            return GateResult(
                gate_name="lifecycle_transition_enforcement",
                status="fail",
                enforcement_action="block",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )

    def enforce_read_only(
        self, artifact_id: str, artifact_type: str, current_state: str
    ) -> GateResult:
        """Enforce read-only state protection for an artifact.

        Checks whether the artifact is in a read-only state and produces
        a GateResult based on the enforcement mode.

        In observability mode, modifications to read-only artifacts produce
        a warning but are permitted (status=pass, enforcement_action=warn).
        In soft/hard modes, modifications are rejected
        (status=fail, enforcement_action=block).

        Args:
            artifact_id: Identifier of the artifact.
            artifact_type: The artifact's type.
            current_state: The artifact's current lifecycle state.

        Returns:
            GateResult indicating whether modification is permitted.
        """
        start_time = time.perf_counter()

        is_readonly = self.is_read_only(artifact_type, current_state)

        duration_ms = (time.perf_counter() - start_time) * 1000

        if not is_readonly:
            return GateResult(
                gate_name="lifecycle_read_only_enforcement",
                status="pass",
                enforcement_action="info",
                duration_ms=duration_ms,
                details=[
                    f"Artifact '{artifact_id}' (type: {artifact_type}) in state "
                    f"'{current_state}' is not read-only. Modification permitted."
                ],
                timestamp=self._make_timestamp(),
            )

        # Artifact is in a read-only state
        detail_msg = (
            f"Artifact '{artifact_id}' (type: {artifact_type}) is in read-only "
            f"state '{current_state}'. Content modification is not permitted."
        )

        if self.enforcement_mode == "observability":
            logger.warning(detail_msg)
            return GateResult(
                gate_name="lifecycle_read_only_enforcement",
                status="pass",
                enforcement_action="warn",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
        elif self.enforcement_mode == "soft":
            logger.warning(f"[SOFT BLOCK] {detail_msg}")
            return GateResult(
                gate_name="lifecycle_read_only_enforcement",
                status="fail",
                enforcement_action="block",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
        else:
            # hard mode
            logger.error(f"[HARD BLOCK] {detail_msg}")
            return GateResult(
                gate_name="lifecycle_read_only_enforcement",
                status="fail",
                enforcement_action="block",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )

    def enforce_regenerable(
        self, artifact_id: str, artifact_type: str, current_state: str, actor_type: str
    ) -> GateResult:
        """Enforce regenerable state gate for engine overwrites.

        Checks whether an artifact is in a regenerable state before permitting
        an engine overwrite. Only artifacts in regenerable states can be
        overwritten by automated engine runs.

        In observability mode, overwrites of non-regenerable artifacts produce
        a warning but are permitted (status=pass, enforcement_action=warn).
        In soft/hard modes, overwrites are rejected
        (status=fail, enforcement_action=block).

        Args:
            artifact_id: Identifier of the artifact.
            artifact_type: The artifact's type.
            current_state: The artifact's current lifecycle state.
            actor_type: The type of actor attempting the overwrite
                       (e.g., 'ENGINE', 'USER').

        Returns:
            GateResult indicating whether the overwrite is permitted.
        """
        start_time = time.perf_counter()

        is_regen = self.is_regenerable(artifact_type, current_state)

        duration_ms = (time.perf_counter() - start_time) * 1000

        if is_regen:
            return GateResult(
                gate_name="lifecycle_regenerable_enforcement",
                status="pass",
                enforcement_action="info",
                duration_ms=duration_ms,
                details=[
                    f"Artifact '{artifact_id}' (type: {artifact_type}) in state "
                    f"'{current_state}' is regenerable. Overwrite by "
                    f"actor '{actor_type}' permitted."
                ],
                timestamp=self._make_timestamp(),
            )

        # Artifact is NOT in a regenerable state
        regenerable_states = self._get_regenerable_states(artifact_type)
        detail_msg = (
            f"Artifact '{artifact_id}' (type: {artifact_type}) in state "
            f"'{current_state}' is NOT regenerable. Overwrite by actor "
            f"'{actor_type}' is not permitted. "
            f"Regenerable states for {artifact_type}: {regenerable_states}"
        )

        if self.enforcement_mode == "observability":
            logger.warning(detail_msg)
            return GateResult(
                gate_name="lifecycle_regenerable_enforcement",
                status="pass",
                enforcement_action="warn",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
        elif self.enforcement_mode == "soft":
            logger.warning(f"[SOFT BLOCK] {detail_msg}")
            return GateResult(
                gate_name="lifecycle_regenerable_enforcement",
                status="fail",
                enforcement_action="block",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
        else:
            # hard mode
            logger.error(f"[HARD BLOCK] {detail_msg}")
            return GateResult(
                gate_name="lifecycle_regenerable_enforcement",
                status="fail",
                enforcement_action="block",
                duration_ms=duration_ms,
                details=[detail_msg],
                timestamp=self._make_timestamp(),
            )
