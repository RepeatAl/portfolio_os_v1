"""
Registry recovery manager for domainization system

Provides recovery operations for the artifact registry:
- List available backups with timestamps
- Restore registry from a specific backup
- Restore from the most recent backup
- Validate restored registry integrity
- Generate health report after recovery
"""

import shutil
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from artifact_schema import validate_artifact_dict
from artifact_registry import ArtifactRegistry
from health_reporter import HealthReporter


class RegistryRecoveryManager:
    """Manages registry backup listing and recovery operations"""

    def __init__(
        self,
        backups_dir: Optional[Path] = None,
        registry_path: Optional[Path] = None,
        repo_root: Optional[Path] = None
    ):
        """
        Initialize recovery manager

        Args:
            backups_dir: Path to backups directory (defaults to .domainization/backups/)
            registry_path: Path to artifact_registry.yaml (defaults to .domainization/artifact_registry.yaml)
            repo_root: Repository root path (defaults to parent of .domainization)
        """
        domainization_dir = Path(__file__).parent.parent

        if backups_dir is None:
            self.backups_dir = domainization_dir / "backups"
        else:
            self.backups_dir = Path(backups_dir)

        if registry_path is None:
            self.registry_path = domainization_dir / "artifact_registry.yaml"
        else:
            self.registry_path = Path(registry_path)

        if repo_root is None:
            self.repo_root = domainization_dir.parent
        else:
            self.repo_root = Path(repo_root)

    def list_available_backups(self) -> List[Dict]:
        """
        List available backup files with metadata

        Returns:
            List of dictionaries with backup info:
            - file_name: Name of the backup file
            - file_path: Full path to the backup file
            - file_size: Size in bytes
            - modified_time: Last modification timestamp
            - modified_time_str: Human-readable timestamp string
        """
        if not self.backups_dir.exists():
            return []

        backups = []
        for backup_file in sorted(self.backups_dir.glob("*.yaml"), reverse=True):
            stat = backup_file.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)

            backups.append({
                'file_name': backup_file.name,
                'file_path': str(backup_file),
                'file_size': stat.st_size,
                'modified_time': modified_time,
                'modified_time_str': modified_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Also include .backup files (from the simple backup mechanism)
        for backup_file in sorted(self.backups_dir.glob("*.backup"), reverse=True):
            stat = backup_file.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)

            backups.append({
                'file_name': backup_file.name,
                'file_path': str(backup_file),
                'file_size': stat.st_size,
                'modified_time': modified_time,
                'modified_time_str': modified_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Sort by modification time (most recent first)
        backups.sort(key=lambda x: x['modified_time'], reverse=True)

        return backups

    def restore_from_backup(self, backup_path: str) -> Dict:
        """
        Restore registry from a specific backup file

        Args:
            backup_path: Path to the backup file to restore from

        Returns:
            Dictionary with recovery result:
            - success: Whether recovery succeeded
            - message: Description of what happened
            - validation_result: Registry validation result after recovery
            - health_report: Health report summary after recovery (if successful)

        Raises:
            FileNotFoundError: If backup file does not exist
            ValueError: If backup file is not a valid registry
        """
        backup_file = Path(backup_path)

        # Verify backup file exists
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        # Validate backup file content before restoring
        validation_result = self._validate_registry_file(backup_file)
        if not validation_result['is_valid']:
            raise ValueError(
                f"Backup file is not a valid registry: {', '.join(validation_result['errors'])}"
            )

        # Create a safety backup of current registry before overwriting
        if self.registry_path.exists():
            safety_backup_name = f"pre_recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            safety_backup_path = self.backups_dir / safety_backup_name
            self.backups_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.registry_path, safety_backup_path)

        # Restore the backup
        shutil.copy2(backup_file, self.registry_path)

        # Validate restored registry
        post_validation = self._validate_registry_file(self.registry_path)

        # Generate health report after recovery
        health_summary = None
        if post_validation['is_valid']:
            health_summary = self._generate_recovery_health_report()

        return {
            'success': post_validation['is_valid'],
            'message': f"Registry restored from {backup_file.name}",
            'backup_used': str(backup_file),
            'validation_result': post_validation,
            'health_report': health_summary
        }

    def restore_latest_backup(self, registry_file_path: Optional[str] = None) -> Dict:
        """
        Restore registry from the most recent backup

        Args:
            registry_file_path: Optional path to the registry file to restore
                              (uses default registry_path if None)

        Returns:
            Dictionary with recovery result (same as restore_from_backup)

        Raises:
            FileNotFoundError: If no backups are available
        """
        if registry_file_path:
            self.registry_path = Path(registry_file_path)

        backups = self.list_available_backups()
        if not backups:
            raise FileNotFoundError("No backup files available for recovery")

        # Use the most recent backup
        latest_backup = backups[0]
        return self.restore_from_backup(latest_backup['file_path'])

    def _validate_registry_file(self, file_path: Path) -> Dict:
        """
        Validate a registry file for schema correctness

        Args:
            file_path: Path to the registry YAML file

        Returns:
            Dictionary with:
            - is_valid: Whether the file is a valid registry
            - errors: List of validation errors (empty if valid)
            - artifact_count: Number of artifacts in the file
        """
        errors = []

        # Check file exists and is readable
        if not file_path.exists():
            return {'is_valid': False, 'errors': ['File does not exist'], 'artifact_count': 0}

        # Try to parse YAML
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return {'is_valid': False, 'errors': [f'Invalid YAML: {str(e)}'], 'artifact_count': 0}

        # Check basic structure
        if not data:
            return {'is_valid': False, 'errors': ['File is empty'], 'artifact_count': 0}

        if 'artifacts' not in data:
            return {'is_valid': False, 'errors': ["Missing 'artifacts' key"], 'artifact_count': 0}

        if not isinstance(data['artifacts'], list):
            return {'is_valid': False, 'errors': ["'artifacts' must be a list"], 'artifact_count': 0}

        # Validate each artifact entry
        artifact_ids = set()
        for i, artifact_dict in enumerate(data['artifacts']):
            if not isinstance(artifact_dict, dict):
                errors.append(f"Artifact at index {i} is not a dictionary")
                continue

            # Check for duplicate artifact_ids
            artifact_id = artifact_dict.get('artifact_id', '')
            if artifact_id in artifact_ids:
                errors.append(f"Duplicate artifact_id: {artifact_id}")
            artifact_ids.add(artifact_id)

            # Validate artifact schema
            is_valid, artifact_errors = validate_artifact_dict(artifact_dict)
            if not is_valid:
                errors.extend([f"Artifact '{artifact_id}': {e}" for e in artifact_errors])

        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'artifact_count': len(data['artifacts'])
        }

    def _generate_recovery_health_report(self) -> Dict:
        """
        Generate a health report summary after recovery

        Returns:
            Dictionary with health report summary
        """
        try:
            artifact_registry = ArtifactRegistry(registry_path=self.registry_path)
            health_reporter = HealthReporter(
                artifact_registry=artifact_registry,
                repo_root=self.repo_root
            )
            report = health_reporter.generate_health_report(include_violations=False)

            # Return summary only
            return {
                'total_artifacts': report['summary']['total_artifacts'],
                'registered_artifacts': report['summary']['registered_artifacts'],
                'registration_percentage': report['summary']['registration_percentage'],
                'domains_with_artifacts': report['summary']['domains_with_artifacts'],
                'report_date': report['report_date'],
                'report_time': report['report_time']
            }
        except Exception as e:
            return {
                'error': f"Could not generate health report: {str(e)}",
                'total_artifacts': 0,
                'registered_artifacts': 0,
                'registration_percentage': 0.0,
                'domains_with_artifacts': 0
            }
