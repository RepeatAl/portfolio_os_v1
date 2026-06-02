"""
CLI commands for registry recovery

Provides commands for:
- Listing available backups
- Restoring from a specific backup
- Restoring from the most recent backup
- Displaying validation results after recovery
- Displaying health report summary after recovery
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from registry_recovery_manager import RegistryRecoveryManager


class RecoveryCommands:
    """Registry recovery CLI commands"""

    def __init__(
        self,
        backups_dir: Optional[Path] = None,
        registry_path: Optional[Path] = None,
        repo_root: Optional[Path] = None
    ):
        """
        Initialize recovery commands

        Args:
            backups_dir: Path to backups directory
            registry_path: Path to artifact_registry.yaml
            repo_root: Repository root path
        """
        self.recovery_manager = RegistryRecoveryManager(
            backups_dir=backups_dir,
            registry_path=registry_path,
            repo_root=repo_root
        )

    def list_backups(self, args: argparse.Namespace) -> int:
        """
        List available backups

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            backups = self.recovery_manager.list_available_backups()

            if not backups:
                print("No backups available")
                return 0

            print(f"Available backups ({len(backups)} found):")
            print("-" * 70)
            print(f"{'#':<4} {'File Name':<40} {'Date':<20} {'Size':<10}")
            print("-" * 70)

            for i, backup in enumerate(backups, 1):
                size_str = self._format_size(backup['file_size'])
                print(f"{i:<4} {backup['file_name']:<40} {backup['modified_time_str']:<20} {size_str:<10}")

            print("-" * 70)
            print(f"\nUse 'domainization recover restore <file_name>' to restore a backup")

            return 0

        except Exception as e:
            print(f"Error listing backups: {e}", file=sys.stderr)
            return 1

    def restore_backup(self, args: argparse.Namespace) -> int:
        """
        Restore from a specific backup

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            backup_file = args.backup_file

            # If just a filename, look in backups directory
            backup_path = Path(backup_file)
            if not backup_path.is_absolute() and not backup_path.exists():
                # Try in backups directory
                potential_path = self.recovery_manager.backups_dir / backup_file
                if potential_path.exists():
                    backup_path = potential_path

            print(f"Restoring registry from: {backup_path.name}")
            print()

            result = self.recovery_manager.restore_from_backup(str(backup_path))

            # Display result
            self._display_recovery_result(result)

            return 0 if result['success'] else 1

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except ValueError as e:
            print(f"Validation error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error restoring backup: {e}", file=sys.stderr)
            return 1

    def restore_latest(self, args: argparse.Namespace) -> int:
        """
        Restore from the most recent backup

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            print("Restoring registry from most recent backup...")
            print()

            result = self.recovery_manager.restore_latest_backup()

            # Display result
            self._display_recovery_result(result)

            return 0 if result['success'] else 1

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error restoring latest backup: {e}", file=sys.stderr)
            return 1

    def _display_recovery_result(self, result: dict) -> None:
        """Display recovery result to stdout"""
        # Status
        status_icon = "✅" if result['success'] else "❌"
        print(f"{status_icon} {result['message']}")
        print()

        # Validation results
        validation = result['validation_result']
        print("VALIDATION RESULTS")
        print("-" * 50)
        print(f"  Valid:          {'Yes' if validation['is_valid'] else 'No'}")
        print(f"  Artifact count: {validation['artifact_count']}")

        if validation['errors']:
            print(f"  Errors ({len(validation['errors'])}):")
            for error in validation['errors'][:5]:
                print(f"    - {error}")
            if len(validation['errors']) > 5:
                print(f"    ... and {len(validation['errors']) - 5} more")
        print()

        # Health report summary
        if result.get('health_report'):
            health = result['health_report']
            if 'error' in health:
                print(f"Health report: {health['error']}")
            else:
                print("HEALTH REPORT SUMMARY")
                print("-" * 50)
                print(f"  Total artifacts:        {health['total_artifacts']}")
                print(f"  Registered artifacts:   {health['registered_artifacts']}")
                print(f"  Registration coverage:  {health['registration_percentage']:.1f}%")
                print(f"  Domains with artifacts: {health['domains_with_artifacts']}")
                print(f"  Report generated:       {health['report_date']} {health['report_time']}")
            print()

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"


def add_recover_parser(subparsers):
    """Add 'recover' command parser with subcommands"""
    recover_parser = subparsers.add_parser(
        'recover',
        help='Registry recovery operations',
        description='Recover artifact registry from backups'
    )

    recover_subparsers = recover_parser.add_subparsers(
        dest='recover_command',
        help='Recovery commands'
    )

    # List backups
    recover_subparsers.add_parser(
        'list',
        help='List available backups',
        description='Show all available registry backups'
    )

    # Restore from specific backup
    restore_parser = recover_subparsers.add_parser(
        'restore',
        help='Restore from specific backup',
        description='Restore registry from a specific backup file'
    )
    restore_parser.add_argument(
        'backup_file',
        help='Backup file name or path to restore from'
    )

    # Restore latest
    recover_subparsers.add_parser(
        'latest',
        help='Restore from most recent backup',
        description='Restore registry from the most recent backup'
    )

    return recover_parser
