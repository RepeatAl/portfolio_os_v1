"""
Tests for Audit Logger

Validates audit logging functionality including:
- Event logging for all event types
- Date-based log file creation
- Log rotation and retention
- Thread-safety for concurrent writes
- Log entry parsing and filtering
"""

import json
import os
import tempfile
import threading
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from audit_logger import AuditEventType, AuditLogger


@pytest.fixture
def temp_logs_dir(tmp_path):
    """Create a temporary logs directory for testing"""
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    return str(logs_dir)


@pytest.fixture
def logger(temp_logs_dir):
    """Create an AuditLogger instance with a temporary logs directory"""
    return AuditLogger(logs_dir=temp_logs_dir)


class TestAuditLoggerInitialization:
    """Tests for AuditLogger initialization and configuration"""

    def test_creates_logs_directory_if_missing(self, tmp_path):
        """Logger creates logs directory if it does not exist"""
        logs_dir = str(tmp_path / "new_logs")
        logger = AuditLogger(logs_dir=logs_dir)
        assert Path(logs_dir).exists()

    def test_default_retention_days(self, logger):
        """Default retention period is 30 days"""
        assert logger.retention_days == 30

    def test_custom_retention_days(self, temp_logs_dir):
        """Custom retention period is respected"""
        logger = AuditLogger(logs_dir=temp_logs_dir, retention_days=7)
        assert logger.retention_days == 7

    def test_enabled_by_default(self, logger):
        """Audit logging is enabled by default"""
        assert logger.enabled is True

    def test_can_disable_logging(self, temp_logs_dir):
        """Audit logging can be disabled"""
        logger = AuditLogger(logs_dir=temp_logs_dir, enabled=False)
        assert logger.enabled is False

    def test_enable_disable_toggle(self, logger):
        """Logging can be toggled on and off"""
        logger.enabled = False
        assert logger.enabled is False
        logger.enabled = True
        assert logger.enabled is True


class TestLogRegistration:
    """Tests for artifact registration logging"""

    def test_log_registration_creates_entry(self, logger, temp_logs_dir):
        """Registration event creates a log entry"""
        logger.log_registration(
            artifact_id="my_doc_md",
            domain="ARCH",
            artifact_type="SSOT",
        )

        entries = logger.read_log_entries()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "artifact_registered"
        assert entries[0]["artifact_id"] == "my_doc_md"
        assert entries[0]["domain"] == "ARCH"
        assert entries[0]["details"]["artifact_type"] == "SSOT"

    def test_log_registration_with_file_path(self, logger):
        """Registration event includes file path when provided"""
        logger.log_registration(
            artifact_id="engine_py",
            domain="SIGNALS",
            artifact_type="ENGINE",
            file_path="engines/allocation_engine.py",
        )

        entries = logger.read_log_entries()
        assert entries[0]["details"]["file_path"] == "engines/allocation_engine.py"

    def test_log_registration_includes_timestamp(self, logger):
        """Registration event includes ISO timestamp"""
        logger.log_registration(
            artifact_id="test_artifact",
            domain="GOV",
            artifact_type="STEERING",
        )

        entries = logger.read_log_entries()
        assert "timestamp" in entries[0]
        # Verify timestamp is parseable ISO format
        datetime.fromisoformat(entries[0]["timestamp"])


class TestLogMetadataChange:
    """Tests for metadata change logging"""

    def test_log_metadata_change(self, logger):
        """Metadata change event is logged correctly"""
        logger.log_metadata_change(
            artifact_id="my_doc_md",
            field_name="lifecycle_status",
            old_value="draft",
            new_value="canonical",
            domain="ARCH",
        )

        entries = logger.read_log_entries()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "metadata_changed"
        assert entries[0]["artifact_id"] == "my_doc_md"
        assert entries[0]["details"]["field"] == "lifecycle_status"
        assert entries[0]["details"]["old_value"] == "draft"
        assert entries[0]["details"]["new_value"] == "canonical"

    def test_log_metadata_change_without_old_value(self, logger):
        """Metadata change works without old_value (new field added)"""
        logger.log_metadata_change(
            artifact_id="new_artifact",
            field_name="secondary_domains",
            new_value="DEPLOY",
        )

        entries = logger.read_log_entries()
        assert "old_value" not in entries[0]["details"]
        assert entries[0]["details"]["new_value"] == "DEPLOY"


class TestLogLifecycleTransition:
    """Tests for lifecycle transition logging"""

    def test_log_lifecycle_transition(self, logger):
        """Lifecycle transition event is logged correctly"""
        logger.log_lifecycle_transition(
            artifact_id="engine_py",
            from_state="development",
            to_state="active",
            domain="SIGNALS",
        )

        entries = logger.read_log_entries()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "lifecycle_transition"
        assert entries[0]["artifact_id"] == "engine_py"
        assert entries[0]["details"]["from_state"] == "development"
        assert entries[0]["details"]["to_state"] == "active"
        assert entries[0]["domain"] == "SIGNALS"

    def test_log_lifecycle_transition_without_domain(self, logger):
        """Lifecycle transition works without domain context"""
        logger.log_lifecycle_transition(
            artifact_id="report_txt",
            from_state="current",
            to_state="archived",
        )

        entries = logger.read_log_entries()
        assert "domain" not in entries[0]


class TestLogValidationFailure:
    """Tests for validation failure logging"""

    def test_log_validation_failure(self, logger):
        """Validation failure event is logged correctly"""
        logger.log_validation_failure(
            error_code="E001",
            artifact_id="unregistered_file",
            gate_name="Gate 1: Artifact Registration",
            error_message="Artifact not registered",
        )

        entries = logger.read_log_entries()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "validation_failure"
        assert entries[0]["artifact_id"] == "unregistered_file"
        assert entries[0]["details"]["error_code"] == "E001"
        assert entries[0]["details"]["gate_name"] == "Gate 1: Artifact Registration"

    def test_log_validation_failure_minimal(self, logger):
        """Validation failure works with minimal parameters"""
        logger.log_validation_failure(error_code="E005")

        entries = logger.read_log_entries()
        assert entries[0]["details"]["error_code"] == "E005"
        assert "artifact_id" not in entries[0]


class TestLogBypass:
    """Tests for bypass usage logging"""

    def test_log_bypass(self, logger):
        """Bypass event is logged correctly"""
        logger.log_bypass(
            reason="Developer override",
            context="pre-commit hook",
        )

        entries = logger.read_log_entries()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "bypass_used"
        assert entries[0]["details"]["reason"] == "Developer override"
        assert entries[0]["details"]["context"] == "pre-commit hook"

    def test_log_bypass_without_context(self, logger):
        """Bypass event works without context"""
        logger.log_bypass(reason="Emergency fix")

        entries = logger.read_log_entries()
        assert "context" not in entries[0]["details"]

    def test_log_bypass_with_domain(self, logger):
        """Bypass event includes domain when provided"""
        logger.log_bypass(
            reason="Testing",
            context="CI pipeline",
            domain="DEPLOY",
        )

        entries = logger.read_log_entries()
        assert entries[0]["domain"] == "DEPLOY"


class TestLogRegistryModification:
    """Tests for registry modification logging"""

    def test_log_registry_modification(self, logger):
        """Registry modification event is logged correctly"""
        logger.log_registry_modification(
            artifact_id="new_engine",
            action="added",
            domain="REASONING",
        )

        entries = logger.read_log_entries()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "registry_modified"
        assert entries[0]["artifact_id"] == "new_engine"
        assert entries[0]["details"]["action"] == "added"


class TestLogFileNaming:
    """Tests for date-based log file naming"""

    def test_log_file_uses_date_format(self, logger, temp_logs_dir):
        """Log file uses audit_YYYY-MM-DD.log format"""
        logger.log_bypass(reason="test")

        today = datetime.now().strftime("%Y-%m-%d")
        expected_file = Path(temp_logs_dir) / f"audit_{today}.log"
        assert expected_file.exists()

    def test_multiple_entries_same_day_same_file(self, logger, temp_logs_dir):
        """Multiple entries on the same day go to the same file"""
        logger.log_bypass(reason="first")
        logger.log_bypass(reason="second")
        logger.log_bypass(reason="third")

        log_files = list(Path(temp_logs_dir).glob("audit_*.log"))
        assert len(log_files) == 1

        entries = logger.read_log_entries()
        assert len(entries) == 3


class TestLogRotation:
    """Tests for log rotation and retention"""

    def test_rotate_removes_old_files(self, temp_logs_dir):
        """Rotation removes files older than retention period"""
        logger = AuditLogger(logs_dir=temp_logs_dir, retention_days=7)

        # Create old log files
        old_date = datetime.now() - timedelta(days=10)
        old_file = Path(temp_logs_dir) / f"audit_{old_date.strftime('%Y-%m-%d')}.log"
        old_file.write_text('{"event": "old"}\n')

        # Create recent log file
        recent_date = datetime.now() - timedelta(days=3)
        recent_file = Path(temp_logs_dir) / f"audit_{recent_date.strftime('%Y-%m-%d')}.log"
        recent_file.write_text('{"event": "recent"}\n')

        removed = logger.rotate_logs()

        assert removed == 1
        assert not old_file.exists()
        assert recent_file.exists()

    def test_rotate_keeps_files_within_retention(self, temp_logs_dir):
        """Rotation keeps files within the retention period"""
        logger = AuditLogger(logs_dir=temp_logs_dir, retention_days=30)

        # Create files within retention
        for days_ago in range(5):
            date = datetime.now() - timedelta(days=days_ago)
            file_path = Path(temp_logs_dir) / f"audit_{date.strftime('%Y-%m-%d')}.log"
            file_path.write_text('{"event": "test"}\n')

        removed = logger.rotate_logs()
        assert removed == 0

    def test_rotate_handles_malformed_filenames(self, temp_logs_dir):
        """Rotation skips files with unexpected naming"""
        logger = AuditLogger(logs_dir=temp_logs_dir, retention_days=1)

        # Create a file with bad naming
        bad_file = Path(temp_logs_dir) / "audit_not-a-date.log"
        bad_file.write_text("bad\n")

        # Should not crash
        removed = logger.rotate_logs()
        assert removed == 0
        assert bad_file.exists()

    def test_rotate_returns_count(self, temp_logs_dir):
        """Rotation returns the number of removed files"""
        logger = AuditLogger(logs_dir=temp_logs_dir, retention_days=5)

        # Create 3 old files
        for days_ago in [10, 15, 20]:
            date = datetime.now() - timedelta(days=days_ago)
            file_path = Path(temp_logs_dir) / f"audit_{date.strftime('%Y-%m-%d')}.log"
            file_path.write_text('{"event": "old"}\n')

        removed = logger.rotate_logs()
        assert removed == 3


class TestDisabledLogging:
    """Tests for disabled audit logging"""

    def test_disabled_logger_does_not_write(self, temp_logs_dir):
        """Disabled logger does not create log files"""
        logger = AuditLogger(logs_dir=temp_logs_dir, enabled=False)
        logger.log_bypass(reason="should not appear")

        log_files = list(Path(temp_logs_dir).glob("audit_*.log"))
        assert len(log_files) == 0

    def test_disabled_logger_all_methods_silent(self, temp_logs_dir):
        """All logging methods are silent when disabled"""
        logger = AuditLogger(logs_dir=temp_logs_dir, enabled=False)

        logger.log_registration("id", "ARCH", "SSOT")
        logger.log_metadata_change("id", "field")
        logger.log_lifecycle_transition("id", "draft", "active")
        logger.log_validation_failure("E001")
        logger.log_bypass("reason")
        logger.log_registry_modification("id", "added")

        log_files = list(Path(temp_logs_dir).glob("audit_*.log"))
        assert len(log_files) == 0


class TestThreadSafety:
    """Tests for thread-safe concurrent writes"""

    def test_concurrent_writes_no_data_loss(self, logger):
        """Concurrent writes from multiple threads produce all entries"""
        num_threads = 10
        entries_per_thread = 20
        total_expected = num_threads * entries_per_thread

        def write_entries(thread_id):
            for i in range(entries_per_thread):
                logger.log_bypass(reason=f"thread_{thread_id}_entry_{i}")

        threads = []
        for t_id in range(num_threads):
            t = threading.Thread(target=write_entries, args=(t_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        entries = logger.read_log_entries()
        assert len(entries) == total_expected

    def test_concurrent_writes_valid_json(self, logger):
        """All entries from concurrent writes are valid JSON"""
        num_threads = 5
        entries_per_thread = 10

        def write_entries(thread_id):
            for i in range(entries_per_thread):
                logger.log_registration(
                    artifact_id=f"artifact_{thread_id}_{i}",
                    domain="ARCH",
                    artifact_type="SSOT",
                )

        threads = []
        for t_id in range(num_threads):
            t = threading.Thread(target=write_entries, args=(t_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # All entries should be parseable JSON
        entries = logger.read_log_entries()
        assert len(entries) == num_threads * entries_per_thread
        for entry in entries:
            assert "timestamp" in entry
            assert "event_type" in entry


class TestReadLogEntries:
    """Tests for reading and filtering log entries"""

    def test_read_entries_from_today(self, logger):
        """Read entries returns today's entries"""
        logger.log_bypass(reason="test1")
        logger.log_bypass(reason="test2")

        entries = logger.read_log_entries()
        assert len(entries) == 2

    def test_read_entries_filter_by_event_type(self, logger):
        """Read entries can filter by event type"""
        logger.log_bypass(reason="bypass1")
        logger.log_registration("id1", "ARCH", "SSOT")
        logger.log_bypass(reason="bypass2")

        bypass_entries = logger.read_log_entries(
            event_type=AuditEventType.BYPASS_USED
        )
        assert len(bypass_entries) == 2

        reg_entries = logger.read_log_entries(
            event_type=AuditEventType.ARTIFACT_REGISTERED
        )
        assert len(reg_entries) == 1

    def test_read_entries_empty_for_missing_date(self, logger):
        """Read entries returns empty list for dates with no log file"""
        old_date = datetime(2020, 1, 1)
        entries = logger.read_log_entries(date=old_date)
        assert entries == []

    def test_read_entries_specific_date(self, temp_logs_dir):
        """Read entries can target a specific date"""
        logger = AuditLogger(logs_dir=temp_logs_dir)

        # Manually create a log file for a specific date
        target_date = datetime(2024, 6, 15)
        log_path = Path(temp_logs_dir) / "audit_2024-06-15.log"
        entry = json.dumps({
            "timestamp": "2024-06-15T10:00:00",
            "event_type": "bypass_used",
            "details": {"reason": "historical"},
        })
        log_path.write_text(entry + "\n")

        entries = logger.read_log_entries(date=target_date)
        assert len(entries) == 1
        assert entries[0]["details"]["reason"] == "historical"


class TestGetLogFiles:
    """Tests for listing log files"""

    def test_get_log_files_sorted_newest_first(self, temp_logs_dir):
        """Log files are returned sorted newest first"""
        logger = AuditLogger(logs_dir=temp_logs_dir)

        # Create files for different dates
        for days_ago in [5, 1, 3]:
            date = datetime.now() - timedelta(days=days_ago)
            file_path = Path(temp_logs_dir) / f"audit_{date.strftime('%Y-%m-%d')}.log"
            file_path.write_text('{"event": "test"}\n')

        files = logger.get_log_files()
        assert len(files) == 3
        # Verify sorted newest first
        names = [f.name for f in files]
        assert names == sorted(names, reverse=True)

    def test_get_log_files_empty_directory(self, logger):
        """Returns empty list when no log files exist"""
        files = logger.get_log_files()
        assert files == []
