"""
CLI commands for validation

Provides commands for:
- Running validation observers on repository state
- Validating specific files
- Running specific observers
- Dry-run mode
- Color-coded output
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from validation_orchestrator import ValidationOrchestrator


# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Severity colors
    CRITICAL = '\033[91m'  # Bright red
    HIGH = '\033[93m'      # Bright yellow
    MEDIUM = '\033[33m'    # Yellow
    LOW = '\033[92m'       # Bright green
    
    # Status colors
    SUCCESS = '\033[92m'   # Bright green
    ERROR = '\033[91m'     # Bright red
    INFO = '\033[94m'      # Bright blue
    WARNING = '\033[93m'   # Bright yellow
    
    @staticmethod
    def disable():
        """Disable colors (for non-TTY output)"""
        Colors.RESET = ''
        Colors.BOLD = ''
        Colors.CRITICAL = ''
        Colors.HIGH = ''
        Colors.MEDIUM = ''
        Colors.LOW = ''
        Colors.SUCCESS = ''
        Colors.ERROR = ''
        Colors.INFO = ''
        Colors.WARNING = ''


class ValidationCommands:
    """Validation CLI commands"""
    
    def __init__(self,
                 artifact_registry: Optional[ArtifactRegistry] = None,
                 domain_registry: Optional[DomainRegistry] = None,
                 lifecycle_manager: Optional[LifecycleManager] = None,
                 repo_root: Optional[Path] = None):
        """
        Initialize validation commands
        
        Args:
            artifact_registry: ArtifactRegistry instance (creates default if None)
            domain_registry: DomainRegistry instance (creates default if None)
            lifecycle_manager: LifecycleManager instance (creates default if None)
            repo_root: Repository root path
        """
        self.artifact_registry = artifact_registry or ArtifactRegistry()
        self.domain_registry = domain_registry or DomainRegistry()
        self.lifecycle_manager = lifecycle_manager or LifecycleManager()
        
        if repo_root is None:
            # Default to parent of .domainization directory
            self.repo_root = Path(__file__).parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        # Create validation orchestrator
        self.orchestrator = ValidationOrchestrator(
            self.artifact_registry,
            self.domain_registry,
            self.lifecycle_manager,
            self.repo_root
        )
    
    def validate(self, args: argparse.Namespace) -> int:
        """
        Run validation observers
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Check if colors should be disabled
            if args.no_color or not sys.stdout.isatty():
                Colors.disable()
            
            # Load registries
            self.artifact_registry.load()
            self.domain_registry.load()
            self.lifecycle_manager.load()
            
            # Parse file paths if provided
            changed_files = None
            if args.files:
                changed_files = [Path(f) for f in args.files]
            
            # Dry-run mode
            if args.dry_run:
                print(f"{Colors.INFO}[DRY RUN MODE]{Colors.RESET}")
                print("Validation will be performed but no changes will be made")
                print()
            
            # Run validation
            if args.observer:
                # Run specific observer
                print(f"{Colors.INFO}Running observer: {args.observer}{Colors.RESET}")
                print()
                
                result = self.orchestrator.validate_observer(args.observer, changed_files)
                
                # Display results
                self._display_observer_result(result)
                
                # Return exit code based on warnings (dry-run always returns 0)
                if args.dry_run:
                    return 0
                return 1 if result.warnings else 0
            else:
                # Run all observers
                print(f"{Colors.INFO}Running all validation observers...{Colors.RESET}")
                print()
                
                report = self.orchestrator.validate_all(changed_files)
                
                # Display results
                self._display_observability_report(report)
                
                # Return exit code based on warnings (dry-run always returns 0)
                if args.dry_run:
                    return 0
                return 1 if report.total_warnings > 0 else 0
            
        except Exception as e:
            print(f"{Colors.ERROR}Error: {e}{Colors.RESET}", file=sys.stderr)
            return 1
    
    def _display_observer_result(self, result):
        """Display results from a single observer"""
        print("=" * 80)
        print(f"{Colors.BOLD}{result.observer_name}{Colors.RESET}")
        print("=" * 80)
        print()
        
        if not result.warnings:
            print(f"{Colors.SUCCESS}✓ No warnings detected{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}Found {len(result.warnings)} warning(s):{Colors.RESET}")
            print()
            
            for warning in result.warnings:
                self._display_warning(warning)
        
        print("=" * 80)
    
    def _display_observability_report(self, report):
        """Display observability report"""
        print("=" * 80)
        print(f"{Colors.BOLD}DOMAINIZATION OBSERVABILITY REPORT{Colors.RESET}")
        print("=" * 80)
        print(f"Mode: {Colors.INFO}OBSERVABILITY{Colors.RESET} (warnings only, no blocking)")
        print(f"Execution Time: {report.total_execution_time_ms:.2f}ms")
        
        if report.performance_target_met:
            print(f"Performance Target (<5000ms): {Colors.SUCCESS}✓ MET{Colors.RESET}")
        else:
            print(f"Performance Target (<5000ms): {Colors.ERROR}✗ EXCEEDED{Colors.RESET}")
        
        print()
        print(f"Total Warnings: {report.total_warnings}")
        
        if report.critical_warnings > 0:
            print(f"  {Colors.CRITICAL}Critical: {report.critical_warnings}{Colors.RESET}")
        if report.high_warnings > 0:
            print(f"  {Colors.HIGH}High: {report.high_warnings}{Colors.RESET}")
        if report.medium_warnings > 0:
            print(f"  {Colors.MEDIUM}Medium: {report.medium_warnings}{Colors.RESET}")
        if report.low_warnings > 0:
            print(f"  {Colors.LOW}Low: {report.low_warnings}{Colors.RESET}")
        
        print()
        
        if report.total_warnings == 0:
            print(f"{Colors.SUCCESS}✓ No warnings detected. System is healthy.{Colors.RESET}")
        else:
            print("Warnings by Observer:")
            print("-" * 80)
            
            for observer_name, warnings in report.warnings_by_observer.items():
                if warnings:
                    print()
                    print(f"{Colors.BOLD}{observer_name}: {len(warnings)} warning(s){Colors.RESET}")
                    
                    for warning in warnings:
                        self._display_warning(warning)
        
        print("=" * 80)
    
    def _display_warning(self, warning):
        """Display a single warning with color coding"""
        # Get severity color
        severity_color = {
            'critical': Colors.CRITICAL,
            'high': Colors.HIGH,
            'medium': Colors.MEDIUM,
            'low': Colors.LOW
        }.get(warning.severity, Colors.RESET)
        
        # Get severity icon
        severity_icon = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }.get(warning.severity, '⚪')
        
        print(f"  {severity_icon} {severity_color}[{warning.severity.upper()}]{Colors.RESET} {warning.artifact_id or 'N/A'}")
        
        if warning.file_path:
            print(f"    File: {warning.file_path}")
        
        print(f"    {warning.warning_message}")
        
        if warning.suggestion:
            print(f"    {Colors.INFO}→ {warning.suggestion}{Colors.RESET}")
        
        print()


def add_validate_parser(subparsers):
    """Add 'validate' command parser"""
    parser = subparsers.add_parser(
        'validate',
        help='Run validation observers',
        description='Run validation observers on current repository state'
    )
    
    # Optional arguments
    parser.add_argument('--files', nargs='+', help='Validate specific files only')
    parser.add_argument('--observer', 
                       choices=[
                           'RegistrationValidator',
                           'DomainAssignmentValidator',
                           'LifecycleValidator',
                           'BoundaryAwarenessValidator',
                           'SSOTConsistencyValidator'
                       ],
                       help='Run specific observer only')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Perform validation without affecting exit code')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')
    
    return parser
