"""Deployment Authority Model — OWNER/CI/RUNTIME authority partitioning.

Defines the minimal deployment authority model with three roles, topology
constraint enforcement, and deploy provenance recording. Ensures no single
actor can both deploy and mutate governance.

Loaded from .domainization/deployment_authority_model.yaml.
Validated at governance initialization.

Requirements: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum

import yaml

from governance.mutation_audit_ledger import LedgerEntry, MutationAuditLedger

logger = logging.getLogger(__name__)


class AuthorityRole(StrEnum):
    """Classification of deployment actor roles.

    Exactly three roles with no inheritance or dynamic creation:
    - OWNER: Human operator with full governance mutation rights
    - CI: Automated pipeline with deploy and validation rights
    - RUNTIME: Execution process with override and fail-mode rights
    """

    OWNER = "OWNER"
    CI = "CI"
    RUNTIME = "RUNTIME"


class Authority(StrEnum):
    """Enumeration of all deployment authorities.

    Each authority is assigned to exactly one role in the model.
    """

    MUTATE_GOVERNANCE = "mutate_governance"
    CHANGE_ENFORCEMENT_MODE = "change_enforcement_mode"
    DEPLOY = "deploy"
    ACCEPT_RUNTIME_HASH = "accept_runtime_hash"
    EXECUTE_OVERRIDE = "execute_override"
    CHANGE_FAIL_MODE = "change_fail_mode"


@dataclass(frozen=True)
class AuthorityAssignment:
    """Immutable assignment of authorities to a role.

    Attributes:
        role: The authority role (OWNER, CI, or RUNTIME).
        authorities: Frozenset of authorities held by this role.
    """

    role: AuthorityRole
    authorities: frozenset[Authority]

    def to_dict(self) -> dict:
        """Serialize to a dictionary for YAML persistence."""
        return {
            "role": str(self.role),
            "authorities": sorted(str(a) for a in self.authorities),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AuthorityAssignment":
        """Deserialize from a dictionary (e.g., loaded from YAML).

        Args:
            data: Dictionary with 'role' and 'authorities' keys.
                  Supports both 'role' and 'role_id' key names for
                  compatibility with the YAML data file format.

        Returns:
            An AuthorityAssignment instance.

        Raises:
            ValueError: If role or authority values are invalid.
            KeyError: If required keys are missing.
        """
        role_key = "role" if "role" in data else "role_id"
        role = AuthorityRole(data[role_key])
        authorities = frozenset(Authority(a) for a in data["authorities"])
        return cls(role=role, authorities=authorities)


@dataclass
class DeployProvenance:
    """Structured record of a deployment event.

    Links a deployment to the actor, authority, validation status,
    and runtime hash at deployment time.

    Attributes:
        deploy_id: Unique identifier for this deployment event.
        timestamp: ISO 8601 timestamp of the deployment.
        actor_role: The authority role that performed the deployment.
        authority_used: The specific authority exercised.
        is_validated: False if manual deployment without CI validation run.
        runtime_hash: Runtime integrity hash validated at deployment time.
        details: Additional event-specific structured details.
    """

    deploy_id: str
    timestamp: str
    actor_role: AuthorityRole
    authority_used: Authority
    is_validated: bool
    runtime_hash: str
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to a dictionary for YAML persistence."""
        return {
            "deploy_id": self.deploy_id,
            "timestamp": self.timestamp,
            "actor_role": str(self.actor_role),
            "authority_used": str(self.authority_used),
            "is_validated": self.is_validated,
            "runtime_hash": self.runtime_hash,
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DeployProvenance":
        """Deserialize from a dictionary.

        Args:
            data: Dictionary with DeployProvenance field keys.

        Returns:
            A DeployProvenance instance.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If enum values are invalid.
        """
        return cls(
            deploy_id=data["deploy_id"],
            timestamp=data["timestamp"],
            actor_role=AuthorityRole(data["actor_role"]),
            authority_used=Authority(data["authority_used"]),
            is_validated=data["is_validated"],
            runtime_hash=data["runtime_hash"],
            details=dict(data.get("details", {})),
        )


# Topology constraints — these pairs MUST NOT coexist on any single role.
# CTO Decision (2026-05-31): Final set is ADDITIVE and stricter.
# All three pairs are enforced simultaneously.
FORBIDDEN_AUTHORITY_PAIRS: list[tuple[Authority, Authority]] = [
    (Authority.MUTATE_GOVERNANCE, Authority.DEPLOY),
    (Authority.DEPLOY, Authority.CHANGE_ENFORCEMENT_MODE),
    (Authority.CHANGE_ENFORCEMENT_MODE, Authority.EXECUTE_OVERRIDE),
]


class DeploymentAuthorityModel:
    """Minimal authority model: OWNER/CI/RUNTIME with topology constraints.

    Loaded from .domainization/deployment_authority_model.yaml.
    Validated at governance initialization. Emits CRITICAL events on
    topology violations and WARNING events on unvalidated deployments.

    The ledger parameter is optional for backward compatibility.
    """

    def __init__(
        self,
        model_path: str,
        ledger: MutationAuditLedger | None = None,
    ) -> None:
        """Initialize the deployment authority model.

        Args:
            model_path: Path to the deployment_authority_model.yaml file.
            ledger: Optional MutationAuditLedger for recording events.
        """
        self._model_path = model_path
        self._ledger = ledger
        self._assignments: list[AuthorityAssignment] = []

    @property
    def model_path(self) -> str:
        """Return the path to the authority model YAML file."""
        return self._model_path

    @property
    def assignments(self) -> list[AuthorityAssignment]:
        """Return the current authority assignments."""
        return list(self._assignments)

    def load_model(self) -> list[AuthorityAssignment]:
        """Load authority assignments from the YAML model file.

        Reads .domainization/deployment_authority_model.yaml and parses
        role definitions into AuthorityAssignment objects.

        Returns:
            List of AuthorityAssignment objects loaded from the file.

        Raises:
            FileNotFoundError: If the model file does not exist.
            yaml.YAMLError: If the file contains invalid YAML.
            ValueError: If role or authority values are invalid.
        """
        with open(self._model_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "roles" not in data:
            raise ValueError(
                f"Invalid deployment authority model: missing 'roles' key in {self._model_path}"
            )

        assignments = []
        for role_data in data["roles"]:
            assignment = AuthorityAssignment.from_dict(role_data)
            assignments.append(assignment)

        self._assignments = assignments
        return assignments

    def validate_topology(self) -> tuple[bool, list[str]]:
        """Check that no role holds forbidden authority pairs.

        Validates the currently loaded assignments against
        FORBIDDEN_AUTHORITY_PAIRS. Each pair defines two authorities
        that must not coexist on any single role.

        Returns:
            Tuple of (is_valid, list_of_violation_messages).
            is_valid is True if no violations found.
        """
        violations: list[str] = []

        for assignment in self._assignments:
            for auth_a, auth_b in FORBIDDEN_AUTHORITY_PAIRS:
                if auth_a in assignment.authorities and auth_b in assignment.authorities:
                    violations.append(
                        f"Role {assignment.role} holds forbidden pair: "
                        f"({auth_a}, {auth_b})"
                    )

        is_valid = len(violations) == 0
        return is_valid, violations

    def validate_at_init(self) -> tuple[bool, list[str]]:
        """Run full validation: load model, validate topology.

        Called once at governance initialization. Emits CRITICAL events
        to the ledger on topology violations.

        Returns:
            Tuple of (is_valid, list_of_error_messages).
        """
        errors: list[str] = []

        # Load the model
        try:
            self.load_model()
        except (FileNotFoundError, yaml.YAMLError, ValueError, KeyError) as exc:
            error_msg = f"Failed to load deployment authority model: {exc}"
            errors.append(error_msg)
            logger.critical(error_msg)
            self._emit_critical_event(error_msg)
            return False, errors

        # Validate topology constraints
        is_valid, violations = self.validate_topology()
        if not is_valid:
            for violation in violations:
                logger.critical("Topology violation: %s", violation)
                self._emit_critical_event(violation)
            errors.extend(violations)

        return is_valid, errors

    def check_authority(self, role: AuthorityRole, authority: Authority) -> bool:
        """Check if a role holds a specific authority.

        Args:
            role: The authority role to check.
            authority: The authority to look for.

        Returns:
            True if the role holds the specified authority.
        """
        for assignment in self._assignments:
            if assignment.role == role:
                return authority in assignment.authorities
        return False

    def record_deploy_provenance(self, provenance: DeployProvenance) -> None:
        """Persist deploy provenance to Mutation_Audit_Ledger.

        Records the deployment event with event_type 'deployment_authorized'.
        Emits WARNING severity if provenance.is_validated is False
        (manual deployment without CI validation run).

        Args:
            provenance: The DeployProvenance record to persist.
        """
        if self._ledger is None:
            logger.warning(
                "No ledger available for deploy provenance recording. "
                "Deploy ID: %s",
                provenance.deploy_id,
            )
            return

        severity = "INFO" if provenance.is_validated else "WARNING"

        if not provenance.is_validated:
            logger.warning(
                "Unvalidated deployment detected (no CI validation run). "
                "Deploy ID: %s",
                provenance.deploy_id,
            )

        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="deployment_authorized",
            timestamp=provenance.timestamp
            or datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": str(provenance.actor_role),
                "actor_id": provenance.deploy_id,
                "context": provenance.details,
                "is_fallback": False,
            },
            governance_policy_version=provenance.details.get(
                "governance_policy_version", "unknown"
            ),
            severity=severity,
            details=provenance.to_dict(),
        )

        try:
            self._ledger.append(entry)
            logger.debug(
                "Recorded deploy provenance: %s [validated=%s]",
                provenance.deploy_id,
                provenance.is_validated,
            )
        except OSError as exc:
            logger.warning(
                "Failed to record deploy provenance to ledger: %s. "
                "Failing soft — continuing pipeline.",
                exc,
            )

    def _emit_critical_event(self, message: str) -> None:
        """Emit a CRITICAL severity event to the ledger.

        Args:
            message: Description of the critical event.
        """
        if self._ledger is None:
            return

        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="deployment_authorized",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "deployment_authority_model",
                "context": {"action": "topology_validation"},
                "is_fallback": False,
            },
            governance_policy_version="unknown",
            severity="CRITICAL",
            details={
                "violation": message,
                "action": "topology_validation_failed",
            },
        )

        try:
            self._ledger.append(entry)
        except OSError as exc:
            logger.error(
                "Failed to emit CRITICAL event to ledger: %s", exc
            )
