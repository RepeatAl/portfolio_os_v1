"""
CLI commands for health reporting

Provides commands for:
- Generating health reports
- Filtering by domain
- Output to file
- Violations-only mode
- Human-readable format
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from health_reporter import HealthReporter


class HealthCommands:
    """Health reporting CLI commands"""
    
    def __init__(self,
                 artifact_registry: Optional[ArtifactRegistry] = None,
                 domain_registry: Optional[DomainRegistry] = None,
                 lifecycle_manager: Optional[LifecycleManager] = None,
                 repo_root: Optional[Path] = None):
        """
        Initialize health commands
        
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
        
        # Create health reporter
        self.health_reporter = HealthReporter(
            self.artifact_registry,
            self.domain_registry,
            self.lifecycle_manager,
            repo_root=self.repo_root
        )
    
    def health(self, args: argparse.Namespace) -> int:
        """
        Generate health report
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Generate health report
            include_violations = not args.no_violations
            report = self.health_reporter.generate_health_report(include_violations)
            
            # Filter by domain if requested
            if args.domain:
                report = self._filter_by_domain(report, args.domain)
            
            # Filter to violations only if requested
            if args.violations_only:
                if 'violations' not in report or not report['violations']:
                    print("No violations found")
                    return 0
                
                # Keep only violations section but preserve required summary fields
                filtered_report = {
                    'report_date': report['report_date'],
                    'report_time': report['report_time'],
                    'enforcement_mode': report['enforcement_mode'],
                    'summary': {
                        'total_artifacts': report['summary']['total_artifacts'],
                        'registered_artifacts': report['summary']['registered_artifacts'],
                        'registration_percentage': report['summary']['registration_percentage'],
                        'total_domains': report['summary']['total_domains'],
                        'domains_with_artifacts': report['summary']['domains_with_artifacts'],
                        'total_violations': report['summary']['total_violations'],
                        'violations_by_severity': report['summary']['violations_by_severity']
                    },
                    'domain_coverage': [],  # Empty for violations-only
                    'lifecycle_distribution': [],  # Empty for violations-only
                    'violations': report['violations'],
                    'recommendations': report.get('recommendations', [])
                }
                report = filtered_report
            
            # Output to file if requested
            if args.output:
                output_path = Path(args.output)
                saved_path = self.health_reporter.save_report(report, output_path)
                print(f"Health report saved to: {saved_path}")
                
                # Also display to stdout if not quiet
                if not args.quiet:
                    print()
                    text_report = self.health_reporter.format_report_text(report)
                    print(text_report)
            else:
                # Display to stdout
                text_report = self.health_reporter.format_report_text(report)
                print(text_report)
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _filter_by_domain(self, report: dict, domain_id: str) -> dict:
        """
        Filter health report to show only artifacts from specified domain
        
        Args:
            report: Full health report
            domain_id: Domain ID to filter by
        
        Returns:
            Filtered health report
        """
        # Filter domain coverage
        filtered_coverage = [
            d for d in report['domain_coverage']
            if d['domain_id'] == domain_id
        ]
        
        # Filter lifecycle distribution (only include types from this domain)
        domain_artifact_types = set()
        for domain in filtered_coverage:
            for atype in domain['artifact_types']:
                domain_artifact_types.add(atype['type'])
        
        filtered_lifecycle = [
            d for d in report['lifecycle_distribution']
            if d['artifact_type'] in domain_artifact_types
        ]
        
        # Filter violations (only include violations from this domain)
        filtered_violations = []
        if 'violations' in report:
            # Load registry to check artifact domains
            self.artifact_registry.load()
            
            for violation in report['violations']:
                artifact_id = violation.get('artifact_id')
                if artifact_id:
                    artifact = self.artifact_registry.get_artifact(artifact_id)
                    if artifact and artifact.primary_domain == domain_id:
                        filtered_violations.append(violation)
                elif violation.get('file_path'):
                    # For unregistered artifacts, we can't filter by domain
                    # Include them in the report
                    filtered_violations.append(violation)
        
        # Update summary
        filtered_summary = report['summary'].copy()
        
        # Count artifacts in filtered domain
        total_artifacts = sum(d['artifact_count'] for d in filtered_coverage)
        filtered_summary['total_artifacts'] = total_artifacts
        filtered_summary['registered_artifacts'] = total_artifacts
        
        if 'violations' in report:
            filtered_summary['total_violations'] = len(filtered_violations)
            
            # Recalculate violations by severity
            by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            for violation in filtered_violations:
                severity = violation.get('severity', 'low')
                by_severity[severity] = by_severity.get(severity, 0) + 1
            
            filtered_summary['violations_by_severity'] = by_severity
        
        # Build filtered report
        filtered_report = {
            'report_date': report['report_date'],
            'report_time': report['report_time'],
            'report_version': report['report_version'],
            'enforcement_mode': report['enforcement_mode'],
            'summary': filtered_summary,
            'domain_coverage': filtered_coverage,
            'lifecycle_distribution': filtered_lifecycle
        }
        
        if 'violations' in report:
            filtered_report['violations'] = filtered_violations
        
        if 'recommendations' in report:
            filtered_report['recommendations'] = report['recommendations']
        
        return filtered_report


def add_health_parser(subparsers):
    """Add 'health' command parser"""
    parser = subparsers.add_parser(
        'health',
        help='Generate health report',
        description='Generate domainization health report'
    )
    
    # Optional arguments
    parser.add_argument('--domain', help='Filter by domain ID')
    parser.add_argument('--output', '-o', help='Save report to file (YAML format)')
    parser.add_argument('--violations-only', action='store_true',
                       help='Show only violations section')
    parser.add_argument('--no-violations', action='store_true',
                       help='Exclude violations from report')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress stdout output when saving to file')
    
    return parser
