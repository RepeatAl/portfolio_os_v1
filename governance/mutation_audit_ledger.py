"""Mutation Audit Ledger — append-only structured log of governance mutations.

Provides the canonical LedgerEntry dataclass and MutationAuditLedger class
for persisting, querying, and recovering governance-relevant mutation records.

Event Types:
- REGISTRY_ADD: Artifact added to the Artifact_Registry
- REGISTRY_MODIFY: Artifact field modified in the Artifact_Registry
- REGISTRY_REMOVE: Artifact removed from the Artifact_Registry
- GOVERNANCE_EVENT: Mode change, policy reload, gate result, sunset evaluation
- POLICY_CHANGE: Confidence policy reload, enforcement mode change
- SUNSET_TRANSITION: Sunset phase changes

Persistence: Append-only YAML in .domainization/mutation_audit_ledger.yaml
Corruption Recovery: Create new ledger, log corruption event (Req 13.5)

Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 13.1, 13.2, 13.3, 13.4, 13.5,
              14.1, 14.2, 14.3, 15.1, 15.2, 15.3
"""

from __future__ import annotations

import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Final

import yaml

logger = logging.getLogger(__name__)

# Supported event types for the mutation audit ledger
EVENT_TYPES: Final[frozenset[str]] = frozenset(
    {
        "REGISTRY_ADD",
        "REGISTRY_MODIFY",
        "REGISTRY_REMOVE",
        "GOVERNANCE_EVENT",
        "POLICY_CHANGE",
        "SUNSET_TRANSITION",
    }
)

# Schema version for the ledger file format
LEDGER_SCHEMA_VERSION: Final[str] = "1.0.0"


@dataclass
class LedgerEntry:
    """A single entry in the mutation audit ledger.

    This is the CANONICAL implementation. The minimal forward-compatible
    version in governance/cold_start_handler.py shares the same interface.

    Attributes:
        entry_id: Unique identifier for this entry (UUID v4).
        event_type: One of the supported EVENT_TYPES.
        timestamp: ISO 8601 timestamp of when the event occurred.
        actor: Serialized ActorIdentity dict (from ActorIdentity.to_dict()).
        governance_policy_version: Content hash identifying active policy.
        severity: Severity level (INFO, WARNING, CRITICAL, etc.).
        details: Event-specific structured details.
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
        """Deserialize from a dictionary (e.g., loaded from YAML).

        Args:
            data: Dictionary with keys matching LedgerEntry fields.

        Returns:
            A LedgerEntry instance.

        Raises:
            KeyError: If required keys are missing.
        """
        return cls(
            entry_id=data["entry_id"],
            event_type=data["event_type"],
            timestamp=data["timestamp"],
            actor=dict(data["actor"]),
            governance_policy_version=data["governance_policy_version"],
            severity=data["severity"],
            details=dict(data.get("details", {})),
        )



class MutationAuditLedger:
    """Append-only structured log of all governance-relevant mutations.

    Persists LedgerEntry records to a YAML file with append-only semantics.
    Supports querying by time range and event type, corruption recovery,
    and cold-start detection.

    Usage:
        ledger = MutationAuditLedger(".domainization/mutation_audit_ledger.yaml")
        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="REGISTRY_ADD",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor=actor.to_dict(),
            governance_policy_version="sha256:abc123",
            severity="INFO",
            details={"artifact_id": "my_artifact"},
        )
        ledger.append(entry)
    """

    def __init__(self, ledger_path: str) -> None:
        """Initialize the mutation audit ledger.

        Creates the ledger file if it does not exist, initializing it with
        the schema version and an empty entries list.

        Args:
            ledger_path: Path to the YAML ledger file.
        """
        self._ledger_path = ledger_path
        self._ensure_ledger_exists()

    @property
    def ledger_path(self) -> str:
        """Return the path to the ledger file."""
        return self._ledger_path

    def append(self, entry: LedgerEntry) -> None:
        """Append a single entry to the ledger (append-only).

        Reads the current ledger, appends the new entry, and writes back.
        Never overwrites or removes existing entries.

        Args:
            entry: The LedgerEntry to append.
        """
        ledger_data = self._read_ledger()
        ledger_data["entries"].append(entry.to_dict())
        self._write_ledger(ledger_data)
        logger.debug(
            "Appended ledger entry: %s [%s]", entry.entry_id, entry.event_type
        )

    def query_by_time_range(self, start: str, end: str) -> list[LedgerEntry]:
        """Query ledger entries within a time range (inclusive).

        Uses lexicographic comparison on ISO 8601 timestamps, which works
        correctly for ISO format strings.

        Args:
            start: ISO 8601 start timestamp (inclusive).
            end: ISO 8601 end timestamp (inclusive).

        Returns:
            List of LedgerEntry objects within the time range, ordered
            chronologically.
        """
        ledger_data = self._read_ledger()
        results = []
        for entry_dict in ledger_data.get("entries", []):
            ts = entry_dict.get("timestamp", "")
            if start <= ts <= end:
                results.append(LedgerEntry.from_dict(entry_dict))
        return results

    def query_by_event_type(self, event_type: str) -> list[LedgerEntry]:
        """Query ledger entries by event type.

        Args:
            event_type: The event type to filter by (e.g., "REGISTRY_ADD").

        Returns:
            List of LedgerEntry objects matching the event type, ordered
            chronologically.
        """
        ledger_data = self._read_ledger()
        results = []
        for entry_dict in ledger_data.get("entries", []):
            if entry_dict.get("event_type") == event_type:
                results.append(LedgerEntry.from_dict(entry_dict))
        return results

    def recover_from_corruption(self) -> None:
        """Recover from a corrupted ledger file.

        Creates a new empty ledger and logs a corruption recovery event
        as the first entry. This ensures the system can continue operating
        even when the ledger file is damaged (Req 13.5).
        """
        logger.warning(
            "Ledger corruption detected at %s. Creating new ledger.",
            self._ledger_path,
        )

        # Create a fresh ledger with a corruption recovery event
        recovery_entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="GOVERNANCE_EVENT",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "mutation_audit_ledger",
                "context": {"action": "corruption_recovery"},
                "is_fallback": False,
            },
            governance_policy_version="unknown",
            severity="WARNING",
            details={
                "action": "corruption_recovery",
                "reason": "Previous ledger file was corrupted or unreadable",
                "previous_path": self._ledger_path,
            },
        )

        ledger_data = {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "entries": [recovery_entry.to_dict()],
        }
        self._write_ledger(ledger_data)
        logger.info("New ledger created after corruption recovery.")

    def is_cold_start(self) -> bool:
        """Check whether the ledger file exists.

        Returns True if the ledger file does not exist, indicating the
        governance system has never been initialized.

        Returns:
            True if the ledger file does not exist.
        """
        return not os.path.isfile(self._ledger_path)

    def _ensure_ledger_exists(self) -> None:
        """Create the ledger file if it does not exist."""
        if not os.path.isfile(self._ledger_path):
            # Ensure parent directory exists
            parent_dir = os.path.dirname(self._ledger_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

            # Initialize empty ledger
            ledger_data = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "entries": [],
            }
            self._write_ledger(ledger_data)
            logger.info("Created new ledger file at %s", self._ledger_path)

    def _read_ledger(self) -> dict:
        """Read and parse the ledger YAML file.

        If the file is corrupted or unreadable, triggers corruption
        recovery and returns the fresh ledger data.

        Returns:
            Parsed ledger data dictionary with 'schema_version' and 'entries'.
        """
        try:
            with open(self._ledger_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            # Validate basic structure
            if not isinstance(data, dict):
                raise ValueError("Ledger file does not contain a YAML mapping")
            if "entries" not in data:
                raise ValueError("Ledger file missing 'entries' key")
            if not isinstance(data["entries"], list):
                raise ValueError("Ledger 'entries' is not a list")

            return data

        except (yaml.YAMLError, ValueError, OSError) as exc:
            logger.error("Failed to read ledger: %s", exc)
            self.recover_from_corruption()
            # Re-read the fresh ledger
            with open(self._ledger_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)

    def _write_ledger(self, data: dict) -> None:
        """Write ledger data to the YAML file.

        Args:
            data: The complete ledger data dictionary to persist.
        """
        with open(self._ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(
                data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
