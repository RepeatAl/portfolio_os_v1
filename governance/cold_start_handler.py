"""Simplified Cold-Start Handler for governance initialization.

Detects when governance state is missing (no ledger file) and initializes
minimal defaults. Forces observability mode regardless of configured
enforcement mode during cold-start. Tags provenance as bootstrap_derived.

CTO Directive: Simplified to minimal version. No stuck-cold-start detection,
no 3-run threshold, no complex bootstrap.

Validates: Requirements 31.1, 31.2
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from governance.actor_identity import ActorIdentity
from governance.state_provenance_tagger import GovernanceProvenance


# Minimal LedgerEntry dataclass compatible with the future
# governance/mutation_audit_ledger.py (Task 7.1).
@dataclass
class LedgerEntry:
    """A single entry in the mutation audit ledger.

    This is a minimal forward-compatible definition. The full implementation
    will be in governance/mutation_audit_ledger.py.
    """

    entry_id: str
    event_type: str
    timestamp: str
    actor: dict
    governance_policy_version: str
    severity: str
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to a dictionary for YAML persistence."""
        return {
            "entry_id": self.entry_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "actor": dict(self.actor),
            "governance_policy_version": self.governance_policy_version,
            "severity": self.severity,
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, data: dict) -> LedgerEntry:
        """Deserialize from a dictionary."""
        return cls(
            entry_id=data["entry_id"],
            event_type=data["event_type"],
            timestamp=data["timestamp"],
            actor=dict(data["actor"]),
            governance_policy_version=data["governance_policy_version"],
            severity=data["severity"],
            details=dict(data.get("details", {})),
        )


# Default ledger file path relative to domainization directory
LEDGER_FILENAME = "mutation_audit_ledger.yaml"


class ColdStartHandler:
    """Minimal cold-start handler for governance initialization.

    Detects missing governance state and initializes minimal defaults.
    Forces observability mode and tags provenance as bootstrap_derived.

    Usage:
        handler = ColdStartHandler("/path/to/.domainization")
        if handler.is_cold_start():
            actor = ActorIdentity.from_environment()
            entry = handler.initialize(actor)
            # System now in observability mode with bootstrap_derived provenance
    """

    def __init__(self, domainization_path: str) -> None:
        """Initialize the cold-start handler.

        Args:
            domainization_path: Absolute or relative path to the
                .domainization directory.
        """
        self._domainization_path = domainization_path
        self._ledger_path = os.path.join(domainization_path, LEDGER_FILENAME)
        self._provenance = GovernanceProvenance.BOOTSTRAP_DERIVED

    @property
    def ledger_path(self) -> str:
        """Return the expected ledger file path."""
        return self._ledger_path

    @property
    def provenance(self) -> GovernanceProvenance:
        """Return the current provenance tag for cold-start state."""
        return self._provenance

    def is_cold_start(self) -> bool:
        """Check whether governance state is missing.

        Returns True if the mutation audit ledger file does not exist,
        indicating the system has never been initialized.

        Returns:
            True if governance state is missing (no ledger file exists).
        """
        return not os.path.isfile(self._ledger_path)

    def initialize(self, actor: ActorIdentity) -> LedgerEntry:
        """Initialize minimal governance defaults and return bootstrap entry.

        Creates an empty ledger file with a bootstrap entry recording the
        initialization timestamp and actor. Forces observability mode and
        tags provenance as bootstrap_derived.

        Args:
            actor: The ActorIdentity performing the initialization.

        Returns:
            A LedgerEntry representing the bootstrap initialization event.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Create the bootstrap ledger entry
        bootstrap_entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="GOVERNANCE_EVENT",
            timestamp=timestamp,
            actor=actor.to_dict(),
            governance_policy_version="bootstrap",
            severity="INFO",
            details={
                "action": "cold_start_initialization",
                "enforcement_mode": "observability",
                "provenance": GovernanceProvenance.BOOTSTRAP_DERIVED.value,
                "reason": "Governance state missing, initializing minimal defaults",
            },
        )

        # Ensure the domainization directory exists
        os.makedirs(self._domainization_path, exist_ok=True)

        # Write the bootstrap entry to the ledger file
        self._write_bootstrap_ledger(bootstrap_entry)

        return bootstrap_entry

    def get_forced_enforcement_mode(self) -> str:
        """Return the enforcement mode forced during cold-start.

        Cold-start always forces observability mode regardless of
        configured enforcement mode.

        Returns:
            The string "observability".
        """
        return "observability"

    def _write_bootstrap_ledger(self, entry: LedgerEntry) -> None:
        """Write the bootstrap entry to the ledger file as YAML.

        Args:
            entry: The bootstrap LedgerEntry to persist.
        """
        import yaml

        ledger_data = {
            "schema_version": "1.0.0",
            "entries": [entry.to_dict()],
        }

        with open(self._ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(
                ledger_data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
