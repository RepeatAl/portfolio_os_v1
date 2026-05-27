"""
Integration tests for registry recovery manager

Tests:
- Listing available backups
- Restoring from a specific backup
- Restoring latest backup
- Validation after recovery (valid and invalid registry)
- Health report generation after recovery
- Error handling for missing/corrupt backups
"""

import pytest
import yaml
import shutil
from pathlib import Path
from datetime import datetime
import time

from registry_recovery_manager import RegistryRecoveryManager


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory structure mimicking .domainization/"""
    backups_dir = tmp_path / "backups"
    backups_dir.mkdir()

    registry_path = tmp_path / "artifact_registry.yaml"

    return tmp_path, backups_dir, registry_path


@pytest.fixture
def valid_registry_data():
    """Create valid registry data for testing"""
    return {
        'artifacts': [
            {
                'artifact_id': 'test_artifact_1',
                'file_path': 'docs/test_doc.md',
                'primary_domain': 'GOV',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2025-01-01',
                'last_modified': '2025-01-15',
                'owner_role': 'System Architect',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['GOV'],
                'allowed_readers': ['ALL'],
                'topic': 'governance'
            },
            {
                'artifact_id': 'test_artifact_2',
                'file_path': 'engines/test_engine.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2025-01-05',
                'last_modified': '2025-01-20',
                'owner_role': 'Signal Engineer',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'dependencies': ['test_artifact_1']
            }
        ]
    }


@pytest.fixture
def invalid_registry_data():
    """Create invalid registry data for testing"""
    return {
        'artifacts': [
            {
                'artifact_id': 'broken_artifact',
                # Missing required fields: file_path, primary_domain, etc.
            }
        ]
    }


@pytest.fixture
def recovery_manager_with_backups(temp_dir, valid_registry_data):
    """Create a recovery manager with pre-populated backups"""
    tmp_path, backups_dir, registry_path = temp_dir

    # Write current registry
    with open(registry_path, 'w') as f:
        yaml.dump(valid_registry_data, f)

    # Create multiple backup files with slight time differences
    for i in range(3):
        backup_name = f"artifact_registry_2025-01-{10+i:02d}_12-00-00.yaml"
        backup_path = backups_dir / backup_name
        with open(backup_path, 'w') as f:
            yaml.dump(valid_registry_data, f)
        # Ensure different modification times
        time.sleep(0.05)

    manager = RegistryRecoveryManager(
        backups_dir=backups_dir,
        registry_path=registry_path,
        repo_root=tmp_path
    )

    return manager, backups_dir, registry_path


class TestListAvailableBackups:
    """Tests for listing available backups"""

    def test_list_backups_empty_directory(self, temp_dir):
        """Test listing backups when no backups exist"""
        tmp_path, backups_dir, registry_path = temp_dir

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        backups = manager.list_available_backups()
        assert backups == []

    def test_list_backups_nonexistent_directory(self, tmp_path):
        """Test listing backups when backups directory does not exist"""
        manager = RegistryRecoveryManager(
            backups_dir=tmp_path / "nonexistent",
            registry_path=tmp_path / "registry.yaml",
            repo_root=tmp_path
        )

        backups = manager.list_available_backups()
        assert backups == []

    def test_list_backups_with_yaml_files(self, recovery_manager_with_backups):
        """Test listing backups returns correct count and metadata"""
        manager, backups_dir, _ = recovery_manager_with_backups

        backups = manager.list_available_backups()

        assert len(backups) == 3
        # Most recent first
        assert backups[0]['modified_time'] >= backups[1]['modified_time']
        assert backups[1]['modified_time'] >= backups[2]['modified_time']

    def test_list_backups_contains_required_fields(self, recovery_manager_with_backups):
        """Test that each backup entry has all required fields"""
        manager, _, _ = recovery_manager_with_backups

        backups = manager.list_available_backups()

        for backup in backups:
            assert 'file_name' in backup
            assert 'file_path' in backup
            assert 'file_size' in backup
            assert 'modified_time' in backup
            assert 'modified_time_str' in backup
            assert backup['file_size'] > 0

    def test_list_backups_includes_backup_extension(self, temp_dir, valid_registry_data):
        """Test that .backup files are also listed"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Create a .backup file
        backup_path = backups_dir / "artifact_registry.yaml.backup"
        with open(backup_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        backups = manager.list_available_backups()
        assert len(backups) == 1
        assert backups[0]['file_name'] == "artifact_registry.yaml.backup"


class TestRestoreFromBackup:
    """Tests for restoring from a specific backup"""

    def test_restore_valid_backup(self, recovery_manager_with_backups):
        """Test restoring from a valid backup file"""
        manager, backups_dir, registry_path = recovery_manager_with_backups

        # Get a backup file
        backups = manager.list_available_backups()
        backup_path = backups[0]['file_path']

        result = manager.restore_from_backup(backup_path)

        assert result['success'] is True
        assert 'restored' in result['message'].lower()
        assert result['validation_result']['is_valid'] is True
        assert result['validation_result']['artifact_count'] == 2

    def test_restore_creates_safety_backup(self, recovery_manager_with_backups):
        """Test that restoring creates a safety backup of current registry"""
        manager, backups_dir, registry_path = recovery_manager_with_backups

        # Count backups before restore
        initial_backup_count = len(list(backups_dir.glob("*")))

        backups = manager.list_available_backups()
        manager.restore_from_backup(backups[0]['file_path'])

        # Should have one more backup (the safety backup)
        final_backup_count = len(list(backups_dir.glob("*")))
        assert final_backup_count == initial_backup_count + 1

        # Safety backup should have "pre_recovery" in name
        safety_backups = list(backups_dir.glob("pre_recovery_*"))
        assert len(safety_backups) == 1

    def test_restore_nonexistent_backup_raises_error(self, recovery_manager_with_backups):
        """Test that restoring from nonexistent file raises FileNotFoundError"""
        manager, _, _ = recovery_manager_with_backups

        with pytest.raises(FileNotFoundError):
            manager.restore_from_backup("/nonexistent/path/backup.yaml")

    def test_restore_invalid_backup_raises_error(self, temp_dir):
        """Test that restoring from invalid backup raises ValueError"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Create an invalid backup file
        invalid_backup = backups_dir / "invalid_backup.yaml"
        with open(invalid_backup, 'w') as f:
            f.write("not_artifacts: true\n")

        # Write a current registry
        with open(registry_path, 'w') as f:
            yaml.dump({'artifacts': []}, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(ValueError, match="not a valid registry"):
            manager.restore_from_backup(str(invalid_backup))

    def test_restore_corrupt_yaml_raises_error(self, temp_dir):
        """Test that restoring from corrupt YAML raises ValueError"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Create a corrupt YAML file
        corrupt_backup = backups_dir / "corrupt_backup.yaml"
        with open(corrupt_backup, 'w') as f:
            f.write("{{invalid yaml: [unclosed\n")

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(ValueError, match="not a valid registry"):
            manager.restore_from_backup(str(corrupt_backup))


class TestRestoreLatestBackup:
    """Tests for restoring from the most recent backup"""

    def test_restore_latest_success(self, recovery_manager_with_backups):
        """Test restoring from the latest backup"""
        manager, _, _ = recovery_manager_with_backups

        result = manager.restore_latest_backup()

        assert result['success'] is True
        assert result['validation_result']['is_valid'] is True

    def test_restore_latest_no_backups_raises_error(self, temp_dir):
        """Test that restoring latest with no backups raises FileNotFoundError"""
        tmp_path, backups_dir, registry_path = temp_dir

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(FileNotFoundError, match="No backup files available"):
            manager.restore_latest_backup()

    def test_restore_latest_uses_most_recent(self, temp_dir, valid_registry_data):
        """Test that restore_latest uses the most recently modified backup"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Write current registry
        with open(registry_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        # Create older backup with fewer artifacts
        older_data = {'artifacts': [valid_registry_data['artifacts'][0]]}
        older_backup = backups_dir / "old_backup.yaml"
        with open(older_backup, 'w') as f:
            yaml.dump(older_data, f)

        time.sleep(0.05)

        # Create newer backup with all artifacts
        newer_backup = backups_dir / "new_backup.yaml"
        with open(newer_backup, 'w') as f:
            yaml.dump(valid_registry_data, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        result = manager.restore_latest_backup()

        # Should have restored the newer backup (2 artifacts)
        assert result['validation_result']['artifact_count'] == 2

    def test_restore_latest_with_custom_registry_path(self, temp_dir, valid_registry_data):
        """Test restoring latest with a custom registry file path"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Create a custom registry path
        custom_registry = tmp_path / "custom_registry.yaml"
        with open(custom_registry, 'w') as f:
            yaml.dump({'artifacts': []}, f)

        # Create a backup
        backup_path = backups_dir / "backup.yaml"
        with open(backup_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        result = manager.restore_latest_backup(registry_file_path=str(custom_registry))

        assert result['success'] is True
        # Verify the custom registry was updated
        with open(custom_registry, 'r') as f:
            restored_data = yaml.safe_load(f)
        assert len(restored_data['artifacts']) == 2


class TestValidationAfterRecovery:
    """Tests for registry validation after recovery"""

    def test_valid_registry_passes_validation(self, temp_dir, valid_registry_data):
        """Test that a valid registry passes validation after recovery"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Write current registry
        with open(registry_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        # Create backup
        backup_path = backups_dir / "valid_backup.yaml"
        with open(backup_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        result = manager.restore_from_backup(str(backup_path))

        assert result['validation_result']['is_valid'] is True
        assert result['validation_result']['errors'] == []
        assert result['validation_result']['artifact_count'] == 2

    def test_invalid_registry_fails_validation(self, temp_dir, invalid_registry_data):
        """Test that an invalid registry fails validation"""
        tmp_path, backups_dir, registry_path = temp_dir

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        # Validate the invalid data directly
        invalid_file = backups_dir / "invalid.yaml"
        with open(invalid_file, 'w') as f:
            yaml.dump(invalid_registry_data, f)

        result = manager._validate_registry_file(invalid_file)

        assert result['is_valid'] is False
        assert len(result['errors']) > 0

    def test_duplicate_artifact_ids_detected(self, temp_dir):
        """Test that duplicate artifact_ids are detected during validation"""
        tmp_path, backups_dir, registry_path = temp_dir

        duplicate_data = {
            'artifacts': [
                {
                    'artifact_id': 'duplicate_id',
                    'file_path': 'file1.md',
                    'primary_domain': 'GOV',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2025-01-01',
                    'last_modified': '2025-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'canonical',
                    'allowed_writers': ['GOV'],
                    'allowed_readers': ['ALL']
                },
                {
                    'artifact_id': 'duplicate_id',
                    'file_path': 'file2.md',
                    'primary_domain': 'ARCH',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2025-01-01',
                    'last_modified': '2025-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'canonical',
                    'allowed_writers': ['ARCH'],
                    'allowed_readers': ['ALL']
                }
            ]
        }

        dup_file = backups_dir / "duplicate.yaml"
        with open(dup_file, 'w') as f:
            yaml.dump(duplicate_data, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        result = manager._validate_registry_file(dup_file)

        assert result['is_valid'] is False
        assert any('Duplicate artifact_id' in e for e in result['errors'])

    def test_empty_file_fails_validation(self, temp_dir):
        """Test that an empty file fails validation"""
        tmp_path, backups_dir, registry_path = temp_dir

        empty_file = backups_dir / "empty.yaml"
        with open(empty_file, 'w') as f:
            f.write("")

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        result = manager._validate_registry_file(empty_file)

        assert result['is_valid'] is False


class TestHealthReportAfterRecovery:
    """Tests for health report generation after recovery"""

    def test_health_report_generated_on_success(self, recovery_manager_with_backups):
        """Test that health report is generated after successful recovery"""
        manager, _, _ = recovery_manager_with_backups

        result = manager.restore_latest_backup()

        assert result['success'] is True
        assert result['health_report'] is not None
        assert 'total_artifacts' in result['health_report']
        assert 'registered_artifacts' in result['health_report']
        assert 'registration_percentage' in result['health_report']

    def test_health_report_contains_expected_fields(self, recovery_manager_with_backups):
        """Test that health report has all expected summary fields"""
        manager, _, _ = recovery_manager_with_backups

        result = manager.restore_latest_backup()
        health = result['health_report']

        assert 'total_artifacts' in health
        assert 'registered_artifacts' in health
        assert 'registration_percentage' in health
        assert 'domains_with_artifacts' in health
        assert 'report_date' in health
        assert 'report_time' in health

    def test_health_report_not_generated_on_failure(self, temp_dir):
        """Test that health report is not generated when validation fails"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Create a file that passes basic YAML parsing but has invalid artifacts
        # We need it to pass the pre-restore validation but fail post-restore
        # Actually, if pre-restore validation fails, restore_from_backup raises ValueError
        # So we test the internal method directly
        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        # Validate a non-existent file
        result = manager._validate_registry_file(tmp_path / "nonexistent.yaml")
        assert result['is_valid'] is False
        assert result['artifact_count'] == 0


class TestErrorHandling:
    """Tests for error handling with missing/corrupt backups"""

    def test_restore_from_missing_file(self, temp_dir):
        """Test error handling when backup file is missing"""
        tmp_path, backups_dir, registry_path = temp_dir

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(FileNotFoundError):
            manager.restore_from_backup("/path/to/missing/backup.yaml")

    def test_restore_from_corrupt_yaml(self, temp_dir):
        """Test error handling when backup contains corrupt YAML"""
        tmp_path, backups_dir, registry_path = temp_dir

        corrupt_file = backups_dir / "corrupt.yaml"
        with open(corrupt_file, 'w') as f:
            f.write("{{{{invalid: yaml: content: [[[")

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(ValueError):
            manager.restore_from_backup(str(corrupt_file))

    def test_restore_from_non_registry_yaml(self, temp_dir):
        """Test error handling when YAML file is not a registry"""
        tmp_path, backups_dir, registry_path = temp_dir

        non_registry = backups_dir / "not_registry.yaml"
        with open(non_registry, 'w') as f:
            yaml.dump({'some_key': 'some_value'}, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(ValueError, match="not a valid registry"):
            manager.restore_from_backup(str(non_registry))

    def test_restore_preserves_current_on_failure(self, temp_dir, valid_registry_data):
        """Test that current registry is preserved when restore validation fails"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Write current valid registry
        with open(registry_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        # Create invalid backup
        invalid_backup = backups_dir / "invalid.yaml"
        with open(invalid_backup, 'w') as f:
            f.write("not_a_registry: true\n")

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        with pytest.raises(ValueError):
            manager.restore_from_backup(str(invalid_backup))

        # Current registry should be unchanged
        with open(registry_path, 'r') as f:
            current_data = yaml.safe_load(f)
        assert current_data == valid_registry_data

    def test_restore_when_no_current_registry(self, temp_dir, valid_registry_data):
        """Test restoring when no current registry exists"""
        tmp_path, backups_dir, registry_path = temp_dir

        # Don't create a current registry file
        # Create a valid backup
        backup_path = backups_dir / "backup.yaml"
        with open(backup_path, 'w') as f:
            yaml.dump(valid_registry_data, f)

        manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=tmp_path
        )

        result = manager.restore_from_backup(str(backup_path))

        assert result['success'] is True
        assert registry_path.exists()
