"""Domain Lifecycle — Three-state lifecycle model with deprecation reassignment.

Manages domain lifecycle states (active/deprecated/archived) and handles
deprecation-triggered artifact reassignment planning and execution.

State Machine:
    active → deprecated (with reassignment_target)
    deprecated → archived (all artifacts reassigned)
    deprecated → active (reactivation)
    archived → (terminal, no transitions out)

Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from governance.actor_identity import ActorIdentity
    from governance.mutation_audit_ledger import MutationAuditLedger

logger = logging.getLogger(__name__)


class DomainLifecycleState(StrEnum):
    """Lifecycle states for domains in the domain registry."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


# Valid transitions between domain lifecycle states (Req 9.2)
VALID_DOMAIN_TRANSITIONS: dict[DomainLifecycleState, list[DomainLifecycleState]] = {
    DomainLifecycleState.ACTIVE: [DomainLifecycleState.DEPRECATED],
    DomainLifecycleState.DEPRECATED: [
        DomainLifecycleState.ARCHIVED,
        DomainLifecycleState.ACTIVE,
    ],
    DomainLifecycleState.ARCHIVED: [],  # Terminal state — no transitions out
}


@dataclass
class DeprecationRequest:
    """Request to deprecate a domain with artifact reassignment.

    Attributes:
        domain_id: The domain to deprecate.
        reassignment_target: Target domain_id for artifact reassignment (Req 10.2).
        reason: Human-readable reason for deprecation.
        requested_by: Actor ID of the requester.
        timestamp: ISO 8601 timestamp of the request.
    """

    domain_id: str
    reassignment_target: str  # Target domain_id for artifact reassignment
    reason: str
    requested_by: str  # actor_id
    timestamp: str


@dataclass
class ReassignmentPlanEntry:
    """A single artifact reassignment within a deprecation plan.

    Attributes:
        artifact_id: Identifier of the artifact to reassign.
        artifact_type: Type of the artifact (e.g., ENGINE, SSOT).
        previous_domain: Current owning domain.
        new_domain: Target domain for reassignment.
    """

    artifact_id: str
    artifact_type: str
    previous_domain: str
    new_domain: str


@dataclass
class ReassignmentPlan:
    """Complete reassignment plan for a domain deprecation.

    Attributes:
        deprecated_domain: The domain being deprecated.
        target_domain: The domain receiving reassigned artifacts.
        entries: List of artifact reassignment entries.
        blocked_types: Artifact types that cannot_own blocks from reassignment.
        is_valid: False if blocked_types is non-empty.
        generated_at: ISO 8601 timestamp when the plan was generated.
    """

    deprecated_domain: str
    target_domain: str
    entries: list[ReassignmentPlanEntry] = field(default_factory=list)
    blocked_types: list[str] = field(default_factory=list)
    is_valid: bool = True
    generated_at: str = ""


class DomainLifecycleManager:
    """Domain lifecycle state management with deprecation reassignment.

    Extends domain_registry.yaml with a lifecycle_state field per domain.
    Defaults to 'active' for all existing domains (Req 9.5).

    Fail mode: fail_soft — if domain registry is unreadable, skip lifecycle
    checks with WARNING.
    """

    def __init__(
        self,
        domain_registry_path: str,
        artifact_registry_path: str,
        ledger: MutationAuditLedger | None = None,
    ) -> None:
        """Initialize DomainLifecycleManager.

        Args:
            domain_registry_path: Path to domain_registry.yaml.
            artifact_registry_path: Path to artifact_registry.yaml.
            ledger: Optional MutationAuditLedger for recording transitions.
                    If None, transitions are not recorded (backward compatible).
        """
        self._domain_registry_path = domain_registry_path
        self._artifact_registry_path = artifact_registry_path
        self._ledger = ledger

        # Load registries
        self._domain_registry: list[dict] = self._load_domain_registry()
        self._artifact_registry: list[dict] = self._load_artifact_registry()

        # Build lookup indexes
        self._domain_index: dict[str, dict] = {
            d["domain_id"]: d
            for d in self._domain_registry
            if "domain_id" in d
        }

    def _load_domain_registry(self) -> list[dict]:
        """Load and parse the domain registry YAML file.

        Returns:
            List of domain dictionaries. Empty list on failure (fail_soft).
        """
        path = Path(self._domain_registry_path)
        if not path.exists():
            logger.warning(
                "Domain registry not found at %s. Defaulting to empty.",
                self._domain_registry_path,
            )
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data is None:
                return []
            if isinstance(data, dict) and "domains" in data:
                domains = data["domains"]
                return domains if isinstance(domains, list) else []
            if isinstance(data, list):
                return data
            return []
        except (yaml.YAMLError, OSError) as exc:
            logger.warning("Failed to load domain registry: %s", exc)
            return []

    def _load_artifact_registry(self) -> list[dict]:
        """Load and parse the artifact registry YAML file.

        Returns:
            List of artifact dictionaries. Empty list on failure (fail_soft).
        """
        path = Path(self._artifact_registry_path)
        if not path.exists():
            logger.warning(
                "Artifact registry not found at %s. Defaulting to empty.",
                self._artifact_registry_path,
            )
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data is None:
                return []
            if isinstance(data, dict) and "artifacts" in data:
                artifacts = data["artifacts"]
                return artifacts if isinstance(artifacts, list) else []
            if isinstance(data, list):
                return data
            return []
        except (yaml.YAMLError, OSError) as exc:
            logger.warning("Failed to load artifact registry: %s", exc)
            return []

    def get_domain_state(self, domain_id: str) -> DomainLifecycleState:
        """Get current lifecycle state for a domain.

        Reads the lifecycle_state field from domain_registry.yaml.
        Defaults to ACTIVE if the field is missing or domain is not found (Req 9.5).

        Args:
            domain_id: The domain identifier to look up.

        Returns:
            The current DomainLifecycleState for the domain.
        """
        domain = self._domain_index.get(domain_id)
        if domain is None:
            # Domain not found — default to ACTIVE (Req 9.5)
            return DomainLifecycleState.ACTIVE

        state_str = domain.get("lifecycle_state", "active")
        try:
            return DomainLifecycleState(state_str)
        except ValueError:
            logger.warning(
                "Invalid lifecycle_state '%s' for domain '%s'. Defaulting to ACTIVE.",
                state_str,
                domain_id,
            )
            return DomainLifecycleState.ACTIVE

    def validate_transition(
        self, domain_id: str, to_state: DomainLifecycleState
    ) -> tuple[bool, str]:
        """Validate a domain lifecycle transition against VALID_DOMAIN_TRANSITIONS.

        Args:
            domain_id: The domain to transition.
            to_state: The target lifecycle state.

        Returns:
            Tuple of (is_valid, reason). If valid, reason is empty string.
            If invalid, reason describes why the transition is rejected.
        """
        from_state = self.get_domain_state(domain_id)

        # Check if transition is valid
        valid_targets = VALID_DOMAIN_TRANSITIONS.get(from_state, [])
        if to_state in valid_targets:
            return (True, "")

        # Invalid transition — build rejection reason (Req 9.4)
        if not valid_targets:
            reason = (
                f"Domain '{domain_id}' is in terminal state '{from_state}'. "
                f"No transitions are permitted."
            )
        else:
            valid_str = ", ".join(str(s) for s in valid_targets)
            reason = (
                f"Invalid transition for domain '{domain_id}': "
                f"'{from_state}' → '{to_state}' is not permitted. "
                f"Valid transitions from '{from_state}': [{valid_str}]"
            )

        return (False, reason)


    def request_deprecation(
        self, request: DeprecationRequest
    ) -> tuple[bool, ReassignmentPlan | str]:
        """Process a deprecation request for a domain.

        Steps:
        1. Validate transition (active → deprecated) (Req 9.3)
        2. Identify all artifacts with this domain as primary_domain (Req 10.1)
        3. Check reassignment_target can own all artifact types (cannot_own check) (Req 10.3)
        4. If valid: produce ReassignmentPlan for OWNER approval (Req 10.4)
        5. If invalid: return error string listing blocked artifact types

        Args:
            request: The DeprecationRequest with domain_id, reassignment_target, reason, etc.

        Returns:
            Tuple of (success, result). On success, result is a ReassignmentPlan.
            On failure, result is an error string.
        """
        # Step 1: Validate transition
        is_valid, reason = self.validate_transition(
            request.domain_id, DomainLifecycleState.DEPRECATED
        )
        if not is_valid:
            return (False, reason)

        # Step 2: Find all artifacts owned by this domain (Req 10.1)
        owned_artifacts = [
            a
            for a in self._artifact_registry
            if a.get("primary_domain") == request.domain_id
        ]

        # Step 3: Check cannot_own constraints for reassignment target (Req 10.3)
        target_domain = self._domain_index.get(request.reassignment_target)
        if target_domain is None:
            return (
                False,
                f"Reassignment target domain '{request.reassignment_target}' not found.",
            )

        cannot_own = target_domain.get("cannot_own", [])
        if not isinstance(cannot_own, list):
            cannot_own = []

        blocked_types: list[str] = []
        entries: list[ReassignmentPlanEntry] = []

        for artifact in owned_artifacts:
            artifact_id = artifact.get("artifact_id", "unknown")
            artifact_type = artifact.get("artifact_type", "unknown")

            if artifact_type in cannot_own:
                if artifact_type not in blocked_types:
                    blocked_types.append(artifact_type)
            else:
                entry = ReassignmentPlanEntry(
                    artifact_id=artifact_id,
                    artifact_type=artifact_type,
                    previous_domain=request.domain_id,
                    new_domain=request.reassignment_target,
                )
                entries.append(entry)

        # If any artifact types are blocked, reject the deprecation (Req 10.3)
        if blocked_types:
            sorted_blocked = sorted(blocked_types)
            plan = ReassignmentPlan(
                deprecated_domain=request.domain_id,
                target_domain=request.reassignment_target,
                entries=entries,
                blocked_types=sorted_blocked,
                is_valid=False,
                generated_at=datetime.now(timezone.utc).isoformat(),
            )
            return (
                False,
                f"Deprecation rejected: target domain '{request.reassignment_target}' "
                f"cannot own artifact types: {sorted_blocked}. "
                f"These artifacts cannot be reassigned.",
            )

        # Step 4: Produce reassignment plan (Req 10.4)
        plan = ReassignmentPlan(
            deprecated_domain=request.domain_id,
            target_domain=request.reassignment_target,
            entries=entries,
            blocked_types=[],
            is_valid=True,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

        return (True, plan)

    def execute_reassignment(
        self, plan: ReassignmentPlan, actor: ActorIdentity
    ) -> bool:
        """Execute an approved reassignment plan.

        Records each reassignment in the Mutation_Audit_Ledger (Req 10.5).

        Args:
            plan: The approved ReassignmentPlan to execute.
            actor: The ActorIdentity performing the reassignment.

        Returns:
            True if all reassignments were recorded successfully.
            False if ledger is unavailable or plan is invalid.
        """
        from governance.mutation_audit_ledger import LedgerEntry

        if not plan.entries:
            logger.info(
                "No artifacts to reassign for domain '%s'.", plan.deprecated_domain
            )
            return True

        if self._ledger is None:
            logger.warning(
                "Ledger unavailable — cannot record reassignment for domain '%s'. "
                "Failing soft.",
                plan.deprecated_domain,
            )
            return False

        for entry in plan.entries:
            ledger_entry = LedgerEntry(
                entry_id=str(uuid.uuid4()),
                event_type="domain_lifecycle_transition",
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor=actor.to_dict(),
                governance_policy_version="unknown",
                severity="INFO",
                details={
                    "action": "artifact_reassignment",
                    "artifact_id": entry.artifact_id,
                    "artifact_type": entry.artifact_type,
                    "previous_domain": entry.previous_domain,
                    "new_domain": entry.new_domain,
                    "deprecated_domain": plan.deprecated_domain,
                },
            )

            try:
                self._ledger.append(ledger_entry)
                logger.debug(
                    "Recorded reassignment: %s from '%s' to '%s'",
                    entry.artifact_id,
                    entry.previous_domain,
                    entry.new_domain,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to record reassignment for artifact '%s': %s",
                    entry.artifact_id,
                    exc,
                )
                return False

        logger.info(
            "Executed reassignment plan for domain '%s': %d artifacts reassigned.",
            plan.deprecated_domain,
            len(plan.entries),
        )
        return True

    def transition_domain(
        self,
        domain_id: str,
        to_state: DomainLifecycleState,
        actor: ActorIdentity,
    ) -> tuple[bool, str]:
        """Perform a domain lifecycle transition (non-deprecation transitions).

        Validates the transition, persists the state change, and records
        to the Mutation_Audit_Ledger with event_type 'domain_lifecycle_transition'.

        For deprecation transitions, use request_deprecation() instead.

        Args:
            domain_id: The domain to transition.
            to_state: The target lifecycle state.
            actor: The ActorIdentity performing the transition.

        Returns:
            Tuple of (success, message). On success, message confirms the transition.
            On failure, message describes why the transition was rejected.
        """
        from governance.mutation_audit_ledger import LedgerEntry

        # Validate transition (Req 9.3)
        is_valid, reason = self.validate_transition(domain_id, to_state)
        if not is_valid:
            # Emit CRITICAL event for invalid transition (Req 9.4)
            self._emit_invalid_transition_event(domain_id, to_state, reason, actor)
            return (False, reason)

        from_state = self.get_domain_state(domain_id)

        # Record transition to ledger (Req 9.6)
        if self._ledger is not None:
            ledger_entry = LedgerEntry(
                entry_id=str(uuid.uuid4()),
                event_type="domain_lifecycle_transition",
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor=actor.to_dict(),
                governance_policy_version="unknown",
                severity="INFO",
                details={
                    "action": "domain_state_transition",
                    "domain_id": domain_id,
                    "from_state": str(from_state),
                    "to_state": str(to_state),
                },
            )

            try:
                self._ledger.append(ledger_entry)
                logger.debug(
                    "Recorded domain transition: '%s' %s → %s",
                    domain_id,
                    from_state,
                    to_state,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to record domain transition to ledger: %s. "
                    "Failing soft — transition proceeds.",
                    exc,
                )

        # Update in-memory state
        if domain_id in self._domain_index:
            self._domain_index[domain_id]["lifecycle_state"] = str(to_state)

        message = (
            f"Domain '{domain_id}' transitioned: {from_state} → {to_state}"
        )
        logger.info(message)
        return (True, message)

    def _emit_invalid_transition_event(
        self,
        domain_id: str,
        to_state: DomainLifecycleState,
        reason: str,
        actor: ActorIdentity,
    ) -> None:
        """Emit a CRITICAL event for an invalid domain lifecycle transition.

        Args:
            domain_id: The domain that attempted the transition.
            to_state: The rejected target state.
            reason: The rejection reason.
            actor: The actor who attempted the transition.
        """
        if self._ledger is None:
            return

        from governance.mutation_audit_ledger import LedgerEntry

        from_state = self.get_domain_state(domain_id)
        valid_targets = VALID_DOMAIN_TRANSITIONS.get(from_state, [])

        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="domain_lifecycle_transition",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor=actor.to_dict(),
            governance_policy_version="unknown",
            severity="CRITICAL",
            details={
                "action": "invalid_transition_rejected",
                "domain_id": domain_id,
                "from_state": str(from_state),
                "attempted_to_state": str(to_state),
                "valid_transitions": [str(s) for s in valid_targets],
                "rejection_reason": reason,
            },
        )

        try:
            self._ledger.append(entry)
        except Exception as exc:
            logger.warning(
                "Failed to emit invalid transition event: %s", exc
            )
