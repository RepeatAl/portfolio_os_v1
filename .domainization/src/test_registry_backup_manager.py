"""
Tests for Registry Backup Manager

Validates backup functionality including:
- Backup creation with correct timestamp naming
- Backup retention policy (keeps only last 10)
- Listing backups in chronological order
- Backup content matches original file
- Handling of missing backup directory (auto-creation)
"""

import time
import yaml
import pytest
from pathlib import Path

from registry_backup_manager import (
    create_backup,
    list_backups,
    cleanup_old_backups,
    create_backup_and_cleanup,
    DEFAULT_RETENTION_COUNT,
)


@pytest.fixture
def temp_registry(tmp_path):
    """Create a temporary registry YAML file for testing"""
    registry_file = tmp_path / "artifact_registry.yaml"
    data = {
        "artifacts": [
            {
                "artifact_id": "test_artifact_1",
                "file_path": "docs/test.md",
                "primary_domain": "ARCH",
                "artifact_type": "SSOT",
                "lifecycle_status": "canonical",
            }
        ]
    }
    with open(registry_file, "w") as f:
        yaml.dump(data, f)
    return registry_file


@pytest.fixture
def backup_dir(tmp_path):
    """Create a temporary backup directory"""
    bdir = tmp_path / "backups"
    bdir.mkdir()
    return bdir


class TestCreateBackup:
    """Tests for backup creation"""

    def test_creates_backup_file(self, temp_registry, backup_dir):
        """Backup creates a file in the backup directory"""
        result = create_backup(temp_registry, backup_dir=backup_dir)

        assert result is not None
        assert result.exists()
        assert result.parent == backup_dir

    def test_backup_filename_contains_timestamp(self, temp_registry, backup_dir):
        """Backup filename includes YYYY-MM-DD_HH-MM-SS timestamp"""
        result = create_backup(temp_registry, backup_dir=backup_dir)

        # Filename format: artifact_registry_YYYY-MM-DD_HH-MM-SS.yaml
        name = result.name
        assert name.startswith("artifact_registry_")
        assert name.endswith(".yaml")

        # Extract timestamp portion
        timestamp_part = name.replace("artifact_registry_", "").replace(".yaml", "")
        # Verify timestamp format (YYYY-MM-DD_HH-MM-SS)
        parts = timestamp_part.split("_")
        assert len(parts) == 2
        date_part = parts[0]
        time_part = parts[1]
        assert len(date_part.split("-")) == 3  # YYYY-MM-DD
        assert len(time_part.split("-")) == 3  # HH-MM-SS

    def test_backup_content_matches_original(self, temp_registry, backup_dir):
        """Backup file content is identical to the original"""
        result = create_backup(temp_registry, backup_dir=backup_dir)

        original_content = temp_registry.read_text()
        backup_content = result.read_text()
        assert original_content == backup_content

    def test_returns_none_for_missing_source(self, tmp_path, backup_dir):
        """Returns None when source file does not exist"""
        missing_file = tmp_path / "nonexistent.yaml"
        result = create_backup(missing_file, backup_dir=backup_dir)

        assert result is None

    def test_auto_creates_backup_directory(self, temp_registry, tmp_path):
        """Automatically creates backup directory if it does not exist"""
        new_backup_dir = tmp_path / "new_backups"
        assert not new_backup_dir.exists()

        result = create_backup(temp_registry, backup_dir=new_backup_dir)

        assert new_backup_dir.exists()
        assert result is not None
        assert result.exists()

    def test_multiple_backups_have_unique_names(self, temp_registry, backup_dir):
        """Multiple backups created in sequence have different timestamps"""
        backup1 = create_backup(temp_registry, backup_dir=backup_dir)
        time.sleep(1.1)  # Ensure different second
        backup2 = create_backup(temp_registry, backup_dir=backup_dir)

        assert backup1.name != backup2.name
        assert backup1.exists()
        assert backup2.exists()

    def test_preserves_file_extension(self, tmp_path, backup_dir):
        """Backup preserves the original file extension"""
        yml_file = tmp_path / "domain_registry.yml"
        yml_file.write_text("domains: []")

        result = create_backup(yml_file, backup_dir=backup_dir)

        assert result.suffix == ".yml"
        assert result.name.startswith("domain_registry_")


class TestListBackups:
    """Tests for listing backups in chronological order"""

    def test_lists_backups_sorted_oldest_first(self, temp_registry, backup_dir):
        """Backups are listed in chronological order (oldest first)"""
        # Create backups with different timestamps
        backup1 = create_backup(temp_registry, backup_dir=backup_dir)
        time.sleep(1.1)
        backup2 = create_backup(temp_registry, backup_dir=backup_dir)
        time.sleep(1.1)
        backup3 = create_backup(temp_registry, backup_dir=backup_dir)

        backups = list_backups(temp_registry, backup_dir=backup_dir)

        assert len(backups) == 3
        assert backups[0] == backup1
        assert backups[1] == backup2
        assert backups[2] == backup3

    def test_returns_empty_list_when_no_backups(self, temp_registry, backup_dir):
        """Returns empty list when no backups exist"""
        backups = list_backups(temp_registry, backup_dir=backup_dir)
        assert backups == []

    def test_returns_empty_list_when_backup_dir_missing(self, temp_registry, tmp_path):
        """Returns empty list when backup directory does not exist"""
        missing_dir = tmp_path / "nonexistent_backups"
        backups = list_backups(temp_registry, backup_dir=missing_dir)
        assert backups == []

    def test_only_lists_backups_for_specific_registry(self, tmp_path, backup_dir):
        """Only lists backups matching the given registry file"""
        # Create two different registry files
        artifact_reg = tmp_path / "artifact_registry.yaml"
        artifact_reg.write_text("artifacts: []")

        domain_reg = tmp_path / "domain_registry.yaml"
        domain_reg.write_text("domains: []")

        # Create backups for both
        create_backup(artifact_reg, backup_dir=backup_dir)
        create_backup(domain_reg, backup_dir=backup_dir)

        # List should only return backups for the specified file
        artifact_backups = list_backups(artifact_reg, backup_dir=backup_dir)
        domain_backups = list_backups(domain_reg, backup_dir=backup_dir)

        assert len(artifact_backups) == 1
        assert len(domain_backups) == 1
        assert "artifact_registry" in artifact_backups[0].name
        assert "domain_registry" in domain_backups[0].name


class TestCleanupOldBackups:
    """Tests for backup retention policy"""

    def test_keeps_only_last_n_backups(self, temp_registry, backup_dir):
        """Cleanup removes oldest backups, keeping only the specified count"""
        # Create 12 backups
        for i in range(12):
            # Write unique content to distinguish backups
            backup_file = backup_dir / f"artifact_registry_2024-01-{i+1:02d}_10-00-00.yaml"
            backup_file.write_text(f"backup_{i}")

        removed = cleanup_old_backups(temp_registry, keep=10, backup_dir=backup_dir)

        assert len(removed) == 2
        remaining = list_backups(temp_registry, backup_dir=backup_dir)
        assert len(remaining) == 10

    def test_removes_oldest_backups_first(self, temp_registry, backup_dir):
        """Oldest backups are removed first"""
        # Create backups with known timestamps
        old_backup = backup_dir / "artifact_registry_2024-01-01_10-00-00.yaml"
        old_backup.write_text("old")

        mid_backup = backup_dir / "artifact_registry_2024-06-15_10-00-00.yaml"
        mid_backup.write_text("mid")

        new_backup = backup_dir / "artifact_registry_2024-12-31_10-00-00.yaml"
        new_backup.write_text("new")

        removed = cleanup_old_backups(temp_registry, keep=2, backup_dir=backup_dir)

        assert len(removed) == 1
        assert old_backup in removed
        assert not old_backup.exists()
        assert mid_backup.exists()
        assert new_backup.exists()

    def test_no_removal_when_under_limit(self, temp_registry, backup_dir):
        """No backups removed when count is at or below the limit"""
        # Create 5 backups (under default limit of 10)
        for i in range(5):
            backup_file = backup_dir / f"artifact_registry_2024-01-{i+1:02d}_10-00-00.yaml"
            backup_file.write_text(f"backup_{i}")

        removed = cleanup_old_backups(temp_registry, keep=10, backup_dir=backup_dir)

        assert len(removed) == 0
        remaining = list_backups(temp_registry, backup_dir=backup_dir)
        assert len(remaining) == 5

    def test_custom_retention_count(self, temp_registry, backup_dir):
        """Custom retention count is respected"""
        for i in range(8):
            backup_file = backup_dir / f"artifact_registry_2024-01-{i+1:02d}_10-00-00.yaml"
            backup_file.write_text(f"backup_{i}")

        removed = cleanup_old_backups(temp_registry, keep=3, backup_dir=backup_dir)

        assert len(removed) == 5
        remaining = list_backups(temp_registry, backup_dir=backup_dir)
        assert len(remaining) == 3

    def test_returns_removed_paths(self, temp_registry, backup_dir):
        """Returns list of paths that were removed"""
        for i in range(5):
            backup_file = backup_dir / f"artifact_registry_2024-01-{i+1:02d}_10-00-00.yaml"
            backup_file.write_text(f"backup_{i}")

        removed = cleanup_old_backups(temp_registry, keep=2, backup_dir=backup_dir)

        assert len(removed) == 3
        for path in removed:
            assert not path.exists()

    def test_default_retention_is_ten(self):
        """Default retention count is 10"""
        assert DEFAULT_RETENTION_COUNT == 10


class TestCreateBackupAndCleanup:
    """Tests for the combined backup + cleanup operation"""

    def test_creates_backup_and_enforces_retention(self, temp_registry, backup_dir):
        """Combined operation creates backup and removes old ones"""
        # Pre-create 10 backups
        for i in range(10):
            backup_file = backup_dir / f"artifact_registry_2024-01-{i+1:02d}_10-00-00.yaml"
            backup_file.write_text(f"backup_{i}")

        result = create_backup_and_cleanup(
            temp_registry, keep=10, backup_dir=backup_dir
        )

        assert result is not None
        assert result.exists()

        # Should have 10 total (removed 1 old, added 1 new)
        remaining = list_backups(temp_registry, backup_dir=backup_dir)
        assert len(remaining) == 10

    def test_returns_none_for_missing_source(self, tmp_path, backup_dir):
        """Returns None when source file does not exist"""
        missing_file = tmp_path / "nonexistent.yaml"
        result = create_backup_and_cleanup(missing_file, backup_dir=backup_dir)

        assert result is None

    def test_skips_cleanup_when_backup_fails(self, tmp_path, backup_dir):
        """Does not run cleanup when backup creation returns None"""
        missing_file = tmp_path / "nonexistent.yaml"

        # Pre-create some backups
        for i in range(3):
            backup_file = backup_dir / f"nonexistent_{2024+i}-01-01_10-00-00.yaml"
            backup_file.write_text(f"backup_{i}")

        result = create_backup_and_cleanup(
            missing_file, keep=1, backup_dir=backup_dir
        )

        assert result is None
        # Existing backups should not be touched
        existing = list(backup_dir.glob("nonexistent_*.yaml"))
        assert len(existing) == 3


class TestBackupDirectoryAutoCreation:
    """Tests for automatic backup directory creation"""

    def test_creates_nested_backup_directory(self, temp_registry, tmp_path):
        """Creates deeply nested backup directory if needed"""
        nested_dir = tmp_path / "level1" / "level2" / "backups"
        assert not nested_dir.exists()

        result = create_backup(temp_registry, backup_dir=nested_dir)

        assert nested_dir.exists()
        assert result is not None
        assert result.exists()

    def test_works_with_existing_directory(self, temp_registry, backup_dir):
        """Works correctly when backup directory already exists"""
        result = create_backup(temp_registry, backup_dir=backup_dir)

        assert result is not None
        assert result.exists()
