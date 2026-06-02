"""Semantic State Store — immutable archive persistence layer.

Persists semantic states between pipeline runs, maintaining a canonical
snapshot with immutable archives and append-only delta logging. Implements
Hardening 6 (destructive snapshot overwrite prevention) and Hardening 8
(semantic state protection).

Each pipeline run produces an immutable snapshot file. A stable 'latest'
pointer references the current canonical snapshot. Historical snapshots
remain available for replay, rollback, and forensic diff reconstruction.

Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import yaml

from runtime.run_context import RunContext

logger = logging.getLogger(__name__)


class SemanticStateStore:
    """Persist semantic states between pipeline runs with immutable archives.

    Storage layout:
        state/snapshots/<run_id>_semantic_snapshot.yaml  — immutable per-run archive
        state/latest_snapshot.yaml                       — pointer to current canonical
        state/semantic_delta_log.yaml                    — append-only delta log
    """

    def __init__(self, state_dir: str = "state/") -> None:
        """Initialize with directory for snapshot and delta files.

        Args:
            state_dir: Root directory for all state persistence files.
        """
        self.state_dir = Path(state_dir)
        self.snapshots_dir = self.state_dir / "snapshots"
        self.latest_pointer_path = self.state_dir / "latest_snapshot.yaml"
        self.delta_log_path = self.state_dir / "semantic_delta_log.yaml"

    def save_snapshot(self, states: list[dict], run_context: RunContext) -> None:
        """Persist current semantic states as immutable archived snapshot.

        Archives previous snapshot (never overwrites destructively).
        Computes delta from previous snapshot and logs changes.
        Updates 'latest' pointer to new snapshot.

        On write failure, the previous snapshot remains unchanged and
        the failure is logged and propagated.

        Args:
            states: List of semantic state dicts, each containing a 'signal_id' field.
            run_context: The RunContext for this pipeline execution.

        Raises:
            OSError: If directory creation or file writing fails critically.
        """
        run_id = run_context.run_id
        timestamp = run_context.timestamp

        # Ensure directories exist
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # Step 1: Load previous snapshot for delta computation
        previous_states: list[dict] = []
        previous_run_id: str | None = None
        try:
            previous_states, previous_run_id = self.load_snapshot()
        except (FileNotFoundError, KeyError, yaml.YAMLError):
            # No previous snapshot exists — first run
            pass

        # Step 2: Write new immutable snapshot
        snapshot_path = self.snapshots_dir / f"{run_id}_semantic_snapshot.yaml"
        snapshot_data = {
            "run_id": run_id,
            "timestamp": timestamp,
            "states": states,
        }

        try:
            with open(snapshot_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(snapshot_data, f, default_flow_style=False, sort_keys=True)
        except OSError as e:
            logger.error(
                "Failed to write semantic snapshot for run %s: %s",
                run_id,
                e,
            )
            raise

        # Step 3: Compute delta between old and new states
        delta = self._compute_delta(previous_states, states, run_id, timestamp)

        # Step 4: Append delta entry to delta log
        try:
            self._append_delta(delta)
        except OSError as e:
            logger.warning(
                "Failed to append delta log for run %s: %s. Snapshot saved successfully.",
                run_id,
                e,
            )

        # Step 5: Update latest pointer
        try:
            pointer_data = {"current_run_id": run_id, "timestamp": timestamp}
            with open(self.latest_pointer_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(pointer_data, f, default_flow_style=False, sort_keys=True)
        except OSError as e:
            logger.error(
                "Failed to update latest pointer for run %s: %s",
                run_id,
                e,
            )
            raise

    def load_snapshot(self) -> tuple[list[dict], str]:
        """Return (current canonical states, run_id that produced them).

        Reads from 'latest' pointer, then loads the referenced snapshot file.
        Must complete within 5 seconds.

        Returns:
            Tuple of (list of semantic state dicts, run_id string).

        Raises:
            FileNotFoundError: If no latest pointer or snapshot file exists.
            KeyError: If required fields are missing from YAML.
            yaml.YAMLError: If YAML parsing fails.
        """
        if not self.latest_pointer_path.exists():
            raise FileNotFoundError(
                f"No latest snapshot pointer found at {self.latest_pointer_path}"
            )

        with open(self.latest_pointer_path, "r", encoding="utf-8") as f:
            pointer = yaml.safe_load(f)

        current_run_id = pointer["current_run_id"]
        snapshot_path = self.snapshots_dir / f"{current_run_id}_semantic_snapshot.yaml"

        if not snapshot_path.exists():
            raise FileNotFoundError(
                f"Snapshot file not found for run_id {current_run_id}: {snapshot_path}"
            )

        with open(snapshot_path, "r", encoding="utf-8") as f:
            snapshot_data = yaml.safe_load(f)

        return snapshot_data["states"], snapshot_data["run_id"]

    def load_historical(self, run_id: str) -> tuple[list[dict], str]:
        """Return historical snapshot for a specific run_id.

        Enables forensic replay and diff reconstruction.

        Args:
            run_id: The run identifier to load.

        Returns:
            Tuple of (list of semantic state dicts, run_id string).

        Raises:
            FileNotFoundError: If no snapshot exists for the given run_id.
            yaml.YAMLError: If YAML parsing fails.
        """
        snapshot_path = self.snapshots_dir / f"{run_id}_semantic_snapshot.yaml"

        if not snapshot_path.exists():
            raise FileNotFoundError(
                f"No historical snapshot found for run_id {run_id}: {snapshot_path}"
            )

        with open(snapshot_path, "r", encoding="utf-8") as f:
            snapshot_data = yaml.safe_load(f)

        return snapshot_data["states"], snapshot_data["run_id"]

    def get_delta(self, run_id: str) -> dict:
        """Return delta entry for a specific run: additions, removals, changes.

        Searches the append-only delta log for the entry matching the run_id.

        Args:
            run_id: The run identifier to look up.

        Returns:
            Dict with keys: run_id, timestamp, additions, removals, changes.
            Returns empty delta structure if run_id not found in log.
        """
        if not self.delta_log_path.exists():
            return self._empty_delta(run_id)

        with open(self.delta_log_path, "r", encoding="utf-8") as f:
            delta_log = yaml.safe_load(f)

        if not delta_log or "deltas" not in delta_log:
            return self._empty_delta(run_id)

        for entry in delta_log["deltas"]:
            if entry.get("run_id") == run_id:
                return entry

        return self._empty_delta(run_id)

    def _compute_delta(
        self,
        old_states: list[dict],
        new_states: list[dict],
        run_id: str,
        timestamp: str,
    ) -> dict:
        """Compute delta between old and new state lists by signal_id.

        Args:
            old_states: Previous canonical states.
            new_states: Current states to persist.
            run_id: Current run identifier.
            timestamp: Current run timestamp.

        Returns:
            Delta dict with additions, removals, and changes.
        """
        old_by_id = {s["signal_id"]: s for s in old_states if "signal_id" in s}
        new_by_id = {s["signal_id"]: s for s in new_states if "signal_id" in s}

        old_ids = set(old_by_id.keys())
        new_ids = set(new_by_id.keys())

        additions = [
            {"signal_id": sid, "new_value": new_by_id[sid]}
            for sid in sorted(new_ids - old_ids)
        ]

        removals = [
            {"signal_id": sid, "last_value": old_by_id[sid]}
            for sid in sorted(old_ids - new_ids)
        ]

        changes = []
        for sid in sorted(old_ids & new_ids):
            if old_by_id[sid] != new_by_id[sid]:
                changes.append({
                    "signal_id": sid,
                    "previous_value": old_by_id[sid],
                    "current_value": new_by_id[sid],
                })

        return {
            "run_id": run_id,
            "timestamp": timestamp,
            "additions": additions,
            "removals": removals,
            "changes": changes,
        }

    def _append_delta(self, delta: dict) -> None:
        """Append a delta entry to the append-only delta log.

        Creates the log file if it does not exist.

        Args:
            delta: Delta dict to append.
        """
        if self.delta_log_path.exists():
            with open(self.delta_log_path, "r", encoding="utf-8") as f:
                delta_log = yaml.safe_load(f) or {}
        else:
            delta_log = {}

        if "deltas" not in delta_log:
            delta_log["deltas"] = []

        delta_log["deltas"].append(delta)

        with open(self.delta_log_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(delta_log, f, default_flow_style=False, sort_keys=True)

    @staticmethod
    def _empty_delta(run_id: str) -> dict:
        """Return an empty delta structure for a given run_id.

        Args:
            run_id: The run identifier.

        Returns:
            Dict with empty additions, removals, and changes lists.
        """
        return {
            "run_id": run_id,
            "timestamp": "",
            "additions": [],
            "removals": [],
            "changes": [],
        }
