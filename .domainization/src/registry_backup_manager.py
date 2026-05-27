"""
Registry Backup Manager

Provides automatic backup functionality for registry YAML files.
Creates timestamped backups before every write operation and
implements a retention policy to keep only the last N backups.

Backup Strategy:
    .domainization/backups/
        artifact_registry_YYYY-MM-DD_HH-MM-SS.yaml
        domain_registry_YYYY-MM-DD_HH-MM-SS.yaml
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional


# Default backup directory relative to .domainization/
DEFAULT_BACKUP_DIR = Path(__file__).parent.parent / "backups"

# Default number of backups to retain per registry file
DEFAULT_RETENTION_COUNT = 10


def create_backup(
    registry_file_path: Path,
    backup_dir: Optional[Path] = None,
) -> Optional[Path]:
    """
    Create a timestamped backup of a registry file.

    Args:
        registry_file_path: Path to the registry YAML file to back up.
        backup_dir: Directory to store backups. Defaults to .domainization/backups/.

    Returns:
        Path to the created backup file, or None if the source file does not exist.
    """
    registry_file_path = Path(registry_file_path)

    if not registry_file_path.exists():
        return None

    if backup_dir is None:
        backup_dir = DEFAULT_BACKUP_DIR

    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp-based backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    stem = registry_file_path.stem  # e.g. "artifact_registry"
    suffix = registry_file_path.suffix  # e.g. ".yaml"
    backup_filename = f"{stem}_{timestamp}{suffix}"
    backup_path = backup_dir / backup_filename

    shutil.copy2(registry_file_path, backup_path)

    return backup_path


def list_backups(
    registry_file_path: Path,
    backup_dir: Optional[Path] = None,
) -> List[Path]:
    """
    List all backups for a given registry file, sorted by date (oldest first).

    Args:
        registry_file_path: Path to the original registry file.
        backup_dir: Directory where backups are stored. Defaults to .domainization/backups/.

    Returns:
        List of backup file paths sorted chronologically (oldest first).
    """
    registry_file_path = Path(registry_file_path)

    if backup_dir is None:
        backup_dir = DEFAULT_BACKUP_DIR

    backup_dir = Path(backup_dir)

    if not backup_dir.exists():
        return []

    stem = registry_file_path.stem  # e.g. "artifact_registry"
    suffix = registry_file_path.suffix  # e.g. ".yaml"

    # Match pattern: {stem}_YYYY-MM-DD_HH-MM-SS{suffix}
    pattern = f"{stem}_*{suffix}"
    backups = list(backup_dir.glob(pattern))

    # Sort by filename (which contains the timestamp) - oldest first
    backups.sort(key=lambda p: p.name)

    return backups


def cleanup_old_backups(
    registry_file_path: Path,
    keep: int = DEFAULT_RETENTION_COUNT,
    backup_dir: Optional[Path] = None,
) -> List[Path]:
    """
    Remove old backups, keeping only the most recent N backups.

    Args:
        registry_file_path: Path to the original registry file.
        keep: Number of most recent backups to retain. Defaults to 10.
        backup_dir: Directory where backups are stored. Defaults to .domainization/backups/.

    Returns:
        List of paths that were removed.
    """
    backups = list_backups(registry_file_path, backup_dir=backup_dir)

    if len(backups) <= keep:
        return []

    # Remove oldest backups (list is sorted oldest first)
    to_remove = backups[:-keep] if keep > 0 else backups
    removed = []

    for backup_path in to_remove:
        backup_path.unlink()
        removed.append(backup_path)

    return removed


def create_backup_and_cleanup(
    registry_file_path: Path,
    keep: int = DEFAULT_RETENTION_COUNT,
    backup_dir: Optional[Path] = None,
) -> Optional[Path]:
    """
    Create a backup and enforce the retention policy in one operation.

    This is the primary function to call before every registry write.
    It creates a new backup and then removes old backups exceeding the
    retention limit.

    Args:
        registry_file_path: Path to the registry YAML file to back up.
        keep: Number of most recent backups to retain. Defaults to 10.
        backup_dir: Directory to store backups. Defaults to .domainization/backups/.

    Returns:
        Path to the created backup file, or None if the source file does not exist.
    """
    backup_path = create_backup(registry_file_path, backup_dir=backup_dir)

    if backup_path is not None:
        cleanup_old_backups(registry_file_path, keep=keep, backup_dir=backup_dir)

    return backup_path
