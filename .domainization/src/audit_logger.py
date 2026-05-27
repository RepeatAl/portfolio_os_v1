"""
Audit Logger

Provides structured audit logging for the domainization system.
Tracks artifact registration, metadata changes, lifecycle transitions,
validation failures, and bypass usage.

Writes date-based log files to `.domainization/logs/audit_YYYY-MM-DD.log`
with automatic daily rotation and configurable retention.

Thread-safe for concurrent writes.
"""

import json
import os
import threading
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional


class AuditEventType(str, Enum):
    """Types of auditable events in the domainization system"""
    ARTIFACT_REGISTERED = "artifact_registered"
    METADATA_CHANGED = "metadata_changed"
    LIFECYCLE_TRANSITION = "lifecycle_transition"
    VALIDATION_FAILURE = "validation_failure"
    BYPASS_USED = "bypass_used"
    REGISTRY_MODIFIED = "registry_modified"


class AuditLogger:
    """
    Audit logger for domainization system events.

    Writes structured JSON log entries to date-based files in the logs directory.
    Supports daily rotation and configurable retention period.

    Usage:
        logger = AuditLogger()
        logger.log_registration(artifact_id="my_doc_md", domain="ARCH", artifact_type="SSOT")
        logger.log_lifecycle_transition(artifact_id="engine_py", from_state="development", to_state="active")
        logger.log_validation_failure(error_code="E001", artifact_id="unregistered_file", gate_name="Gate 1")
        logger.log_bypass(reason="Developer override", context="pre-commit hook")
    """

    DEFAULT_RETENTION_DAYS = 30

    def __init__(
        self,
        logs_dir: Optional[str] = None,
        retention_days: int = DEFAULT_RETENTION_DAYS,
        enabled: bool = True,
    ):
        """
        Initialize the audit logger.

        Args:
            logs_dir: Path to the logs directory. Defaults to `.domainization/logs/`.
            retention_days: Number of days to retain log files. Default: 30.
            enabled: Whether audit logging is active. Default: True.
        """
        if logs_dir is None:
            logs_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "logs",
            )
        self._logs_dir = Path(logs_dir)
        self._retention_days = retention_days
        self._enabled = enabled
        self._lock = threading.Lock()

        # Ensure logs directory exists
        self._logs_dir.mkdir(parents=True, exist_ok=True)

    @property
    def logs_dir(self) -> Path:
        """Return the logs directory path"""
        return self._logs_dir

    @property
    def retention_days(self) -> int:
        """Return the configured retention period in days"""
        return self._retention_days

    @property
    def enabled(self) -> bool:
        """Return whether audit logging is enabled"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable audit logging"""
        self._enabled = value

    def _get_log_file_path(self, date: Optional[datetime] = None) -> Path:
        """
        Get the log file path for a given date.

        Args:
            date: The date for the log file. Defaults to today.

        Returns:
            Path to the audit log file for the given date.
        """
        if date is None:
            date = datetime.now()
        filename = f"audit_{date.strftime('%Y-%m-%d')}.log"
        return self._logs_dir / filename

    def _format_entry(
        self,
        event_type: AuditEventType,
        artifact_id: Optional[str] = None,
        details: Optional[dict] = None,
        domain: Optional[str] = None,
    ) -> str:
        """
        Format a log entry as a JSON string.

        Args:
            event_type: The type of audit event.
            artifact_id: The affected artifact identifier (if applicable).
            details: Additional event details.
            domain: The domain context for the event.

        Returns:
            JSON-formatted log entry string.
        """
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_type": event_type.value,
        }
        if artifact_id is not None:
            entry["artifact_id"] = artifact_id
        if domain is not None:
            entry["domain"] = domain
        if details is not None:
            entry["details"] = details

        return json.dumps(entry, ensure_ascii=False)

    def _write_entry(self, entry: str) -> None:
        """
        Write a log entry to the current day's log file (thread-safe).

        Args:
            entry: The formatted log entry string.
        """
        if not self._enabled:
            return

        log_path = self._get_log_file_path()

        with self._lock:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(entry + "\n")

    def log_registration(
        self,
        artifact_id: str,
        domain: str,
        artifact_type: str,
        file_path: Optional[str] = None,
    ) -> None:
        """
        Log an artifact registration event.

        Args:
            artifact_id: The registered artifact identifier.
            domain: The primary domain assigned.
            artifact_type: The artifact type (e.g., SSOT, ENGINE).
            file_path: The file path of the artifact (optional).
        """
        details = {
            "artifact_type": artifact_type,
            "action": "registered",
        }
        if file_path:
            details["file_path"] = file_path

        entry = self._format_entry(
            event_type=AuditEventType.ARTIFACT_REGISTERED,
            artifact_id=artifact_id,
            details=details,
            domain=domain,
        )
        self._write_entry(entry)

    def log_metadata_change(
        self,
        artifact_id: str,
        field_name: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> None:
        """
        Log a metadata change event.

        Args:
            artifact_id: The affected artifact identifier.
            field_name: The metadata field that changed.
            old_value: The previous value (optional).
            new_value: The new value (optional).
            domain: The domain context (optional).
        """
        details = {"field": field_name}
        if old_value is not None:
            details["old_value"] = old_value
        if new_value is not None:
            details["new_value"] = new_value

        entry = self._format_entry(
            event_type=AuditEventType.METADATA_CHANGED,
            artifact_id=artifact_id,
            details=details,
            domain=domain,
        )
        self._write_entry(entry)

    def log_lifecycle_transition(
        self,
        artifact_id: str,
        from_state: str,
        to_state: str,
        domain: Optional[str] = None,
    ) -> None:
        """
        Log a lifecycle state transition event.

        Args:
            artifact_id: The affected artifact identifier.
            from_state: The previous lifecycle state.
            to_state: The new lifecycle state.
            domain: The domain context (optional).
        """
        details = {
            "from_state": from_state,
            "to_state": to_state,
        }

        entry = self._format_entry(
            event_type=AuditEventType.LIFECYCLE_TRANSITION,
            artifact_id=artifact_id,
            details=details,
            domain=domain,
        )
        self._write_entry(entry)

    def log_validation_failure(
        self,
        error_code: str,
        artifact_id: Optional[str] = None,
        gate_name: Optional[str] = None,
        error_message: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> None:
        """
        Log a validation failure event.

        Args:
            error_code: The validation error code (e.g., E001).
            artifact_id: The affected artifact identifier (optional).
            gate_name: The validation gate that failed (optional).
            error_message: Human-readable error description (optional).
            domain: The domain context (optional).
        """
        details = {"error_code": error_code}
        if gate_name:
            details["gate_name"] = gate_name
        if error_message:
            details["error_message"] = error_message

        entry = self._format_entry(
            event_type=AuditEventType.VALIDATION_FAILURE,
            artifact_id=artifact_id,
            details=details,
            domain=domain,
        )
        self._write_entry(entry)

    def log_bypass(
        self,
        reason: str,
        context: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> None:
        """
        Log a bypass usage event (e.g., --no-verify).

        Args:
            reason: Why the bypass was used.
            context: Where the bypass occurred (e.g., pre-commit hook).
            domain: The domain context (optional).
        """
        details = {"reason": reason}
        if context:
            details["context"] = context

        entry = self._format_entry(
            event_type=AuditEventType.BYPASS_USED,
            details=details,
            domain=domain,
        )
        self._write_entry(entry)

    def log_registry_modification(
        self,
        artifact_id: str,
        action: str,
        domain: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> None:
        """
        Log a registry modification event.

        Args:
            artifact_id: The affected artifact identifier.
            action: The modification action (e.g., "added", "updated", "removed").
            domain: The domain context (optional).
            details: Additional modification details (optional).
        """
        entry_details = {"action": action}
        if details:
            entry_details.update(details)

        entry = self._format_entry(
            event_type=AuditEventType.REGISTRY_MODIFIED,
            artifact_id=artifact_id,
            details=entry_details,
            domain=domain,
        )
        self._write_entry(entry)

    def rotate_logs(self) -> int:
        """
        Remove log files older than the retention period.

        Returns:
            Number of log files removed.
        """
        cutoff_date = datetime.now() - timedelta(days=self._retention_days)
        removed_count = 0

        for log_file in self._logs_dir.glob("audit_*.log"):
            # Extract date from filename: audit_YYYY-MM-DD.log
            try:
                date_str = log_file.stem.replace("audit_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if file_date < cutoff_date:
                    log_file.unlink()
                    removed_count += 1
            except (ValueError, OSError):
                # Skip files with unexpected naming or permission issues
                continue

        return removed_count

    def get_log_files(self) -> list:
        """
        List all audit log files sorted by date (newest first).

        Returns:
            List of Path objects for existing audit log files.
        """
        files = sorted(
            self._logs_dir.glob("audit_*.log"),
            key=lambda p: p.name,
            reverse=True,
        )
        return files

    def read_log_entries(
        self,
        date: Optional[datetime] = None,
        event_type: Optional[AuditEventType] = None,
    ) -> list:
        """
        Read and parse log entries from a specific date.

        Args:
            date: The date to read entries from. Defaults to today.
            event_type: Filter by event type (optional).

        Returns:
            List of parsed log entry dictionaries.
        """
        log_path = self._get_log_file_path(date)
        if not log_path.exists():
            return []

        entries = []
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if event_type is None or entry.get("event_type") == event_type.value:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue

        return entries
