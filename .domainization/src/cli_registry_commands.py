"""
CLI commands for registry management

Provides commands for:
- Registering new artifacts
- Updating artifact metadata
- Listing artifacts with filters
- Showing artifact details
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from artifact_schema import ArtifactMetadata


class RegistryCommands:
    """Registry management CLI commands"""
    
    AUDIT_LOG_PATH = Path(__file__).parent.parent / "audit_trail.jsonl"
    
    def __init__(self, 
                 artifact_registry: Optional[ArtifactRegistry] = None,
                 domain_registry: Optional[DomainRegistry] = None,
                 lifecycle_manager: Optional[LifecycleManager] = None):
        """
        Initialize registry commands
        
        Args:
            artifact_registry: ArtifactRegistry instance (creates default if None)
            domain_registry: DomainRegistry instance (creates default if None)
            lifecycle_manager: LifecycleManager instance (creates default if None)
        """
        self.artifact_registry = artifact_registry or ArtifactRegistry()
        self.domain_registry = domain_registry or DomainRegistry()
        self.lifecycle_manager = lifecycle_manager or LifecycleManager()
    
    def _log_force_override(self, command: str, artifact_id: str, override_reason: str, details: dict) -> None:
        """
        Log a --force override to the audit trail.
        
        Every --force call MUST be logged with:
        - timestamp
        - command
        - override_reason
        - affected_artifact
        - details of what was overridden
        """
        import getpass
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": getpass.getuser(),
            "command": command,
            "artifact_id": artifact_id,
            "override_reason": override_reason,
            "details": details
        }
        
        # Append to audit trail (JSONL format)
        with open(self.AUDIT_LOG_PATH, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        print(f"  ⚠️  Force override logged to audit trail")
    
    def register(self, args: argparse.Namespace) -> int:
        """
        Register a new artifact
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Load registries
            self.artifact_registry.load()
            self.domain_registry.load()
            self.lifecycle_manager.load()
            
            # Validate domain
            domain = self.domain_registry.get_domain(args.domain)
            if domain is None:
                print(f"Error: Invalid domain '{args.domain}'", file=sys.stderr)
                print(f"Valid domains: {', '.join([d.domain_id for d in self.domain_registry.list_domains()])}")
                return 1
            
            # Validate artifact type
            if not domain.can_own_type(args.type):
                print(f"Error: Domain '{args.domain}' cannot own artifact type '{args.type}'", file=sys.stderr)
                valid_domains = self.domain_registry.get_valid_domains_for_type(args.type)
                if valid_domains:
                    print(f"Valid domains for {args.type}: {', '.join(valid_domains)}")
                return 1
            
            # Get initial lifecycle state
            initial_state = self.lifecycle_manager.get_initial_state(args.type)
            if initial_state is None:
                print(f"Error: No state machine defined for artifact type '{args.type}'", file=sys.stderr)
                return 1
            
            # Validate allowed_writers domains (Governance Hardening)
            writers = args.allowed_writers or [args.domain]
            for writer_domain_id in writers:
                writer_domain = self.domain_registry.get_domain(writer_domain_id)
                if writer_domain is None:
                    print(f"Error: Invalid writer domain '{writer_domain_id}'", file=sys.stderr)
                    return 1
                if not writer_domain.can_own_type(args.type):
                    if not getattr(args, 'force', False):
                        print(f"Error: Writer domain '{writer_domain_id}' cannot own type '{args.type}'", file=sys.stderr)
                        print(f"Use --force with --force-reason to override this check")
                        return 1
                    else:
                        reason = getattr(args, 'force_reason', None) or 'No reason provided'
                        self._log_force_override(
                            command=f"register {args.artifact_id}",
                            artifact_id=args.artifact_id,
                            override_reason=reason,
                            details={
                                "violation": "cross_domain_writer",
                                "writer_domain": writer_domain_id,
                                "artifact_type": args.type,
                                "primary_domain": args.domain
                            }
                        )
                        print(f"  Warning: Forcing cross-domain writer '{writer_domain_id}' for type '{args.type}'")
            
            # Create metadata
            metadata = ArtifactMetadata(
                artifact_id=args.artifact_id,
                file_path=args.file_path,
                primary_domain=args.domain,
                artifact_type=args.type,
                lifecycle_status=args.lifecycle or initial_state,
                created_date=datetime.now().strftime('%Y-%m-%d'),
                last_modified=datetime.now().strftime('%Y-%m-%d'),
                owner_role=args.owner_role or f"{args.domain} domain owner",
                ssot_relationship=args.ssot_relationship or 'none',
                allowed_writers=args.allowed_writers or [args.domain],
                allowed_readers=args.allowed_readers or ['ALL'],
                secondary_domains=args.secondary_domains,
                dependencies=args.dependencies,
                topic=args.topic,
                description=args.description,
                tags=args.tags
            )
            
            # Register artifact
            self.artifact_registry.register_artifact(metadata)
            self.artifact_registry.save()
            
            print(f"✓ Successfully registered artifact '{args.artifact_id}'")
            print(f"  File: {args.file_path}")
            print(f"  Domain: {args.domain}")
            print(f"  Type: {args.type}")
            print(f"  Lifecycle: {metadata.lifecycle_status}")
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def update(self, args: argparse.Namespace) -> int:
        """
        Update artifact metadata
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Load registries
            self.artifact_registry.load()
            self.domain_registry.load()
            self.lifecycle_manager.load()
            
            # Get existing artifact
            existing = self.artifact_registry.get_artifact(args.artifact_id)
            if existing is None:
                print(f"Error: Artifact '{args.artifact_id}' not found", file=sys.stderr)
                return 1
            
            # Update fields if provided
            if args.domain:
                # Validate domain
                domain = self.domain_registry.get_domain(args.domain)
                if domain is None:
                    print(f"Error: Invalid domain '{args.domain}'", file=sys.stderr)
                    return 1
                
                # Validate domain can own type
                if not domain.can_own_type(existing.artifact_type):
                    print(f"Error: Domain '{args.domain}' cannot own artifact type '{existing.artifact_type}'", file=sys.stderr)
                    return 1
                
                existing.primary_domain = args.domain
            
            if args.lifecycle:
                # Validate lifecycle transition
                is_valid, error = self.lifecycle_manager.validate_transition(
                    existing.artifact_type,
                    existing.lifecycle_status,
                    args.lifecycle
                )
                if not is_valid:
                    print(f"Error: {error}", file=sys.stderr)
                    return 1
                
                existing.lifecycle_status = args.lifecycle
            
            if args.file_path:
                existing.file_path = args.file_path
            
            if args.owner_role:
                existing.owner_role = args.owner_role
            
            if args.ssot_relationship:
                existing.ssot_relationship = args.ssot_relationship
            
            if args.allowed_writers:
                # Validate writer domains (Governance Hardening)
                for writer_domain_id in args.allowed_writers:
                    writer_domain = self.domain_registry.get_domain(writer_domain_id)
                    if writer_domain is None:
                        print(f"Error: Invalid writer domain '{writer_domain_id}'", file=sys.stderr)
                        return 1
                    if not writer_domain.can_own_type(existing.artifact_type):
                        if not getattr(args, 'force', False):
                            print(f"Error: Writer domain '{writer_domain_id}' cannot own type '{existing.artifact_type}'", file=sys.stderr)
                            print(f"Use --force with --force-reason to override this check")
                            return 1
                        else:
                            reason = getattr(args, 'force_reason', None) or 'No reason provided'
                            self._log_force_override(
                                command=f"update {args.artifact_id}",
                                artifact_id=args.artifact_id,
                                override_reason=reason,
                                details={
                                    "violation": "cross_domain_writer",
                                    "writer_domain": writer_domain_id,
                                    "artifact_type": existing.artifact_type,
                                    "primary_domain": existing.primary_domain
                                }
                            )
                            print(f"  Warning: Forcing cross-domain writer '{writer_domain_id}' for type '{existing.artifact_type}'")
                existing.allowed_writers = args.allowed_writers
            
            if args.allowed_readers:
                existing.allowed_readers = args.allowed_readers
            
            if args.secondary_domains:
                existing.secondary_domains = args.secondary_domains
            
            if args.dependencies:
                existing.dependencies = args.dependencies
            
            if args.topic:
                existing.topic = args.topic
            
            if args.description:
                existing.description = args.description
            
            if args.tags:
                existing.tags = args.tags
            
            # Update last_modified
            existing.last_modified = datetime.now().strftime('%Y-%m-%d')
            
            # Save changes
            self.artifact_registry.update_artifact(args.artifact_id, existing)
            self.artifact_registry.save()
            
            print(f"✓ Successfully updated artifact '{args.artifact_id}'")
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def list_artifacts(self, args: argparse.Namespace) -> int:
        """
        List artifacts with optional filters
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Load registry
            self.artifact_registry.load()
            
            # Get artifacts based on filters
            artifacts = []
            
            if args.domain:
                artifacts = self.artifact_registry.list_artifacts_by_domain(args.domain)
            elif args.type:
                artifacts = self.artifact_registry.list_artifacts_by_type(args.type)
            elif args.lifecycle:
                artifacts = self.artifact_registry.list_artifacts_by_lifecycle(args.lifecycle)
            else:
                artifacts = self.artifact_registry.list_all_artifacts()
            
            # Apply additional filters
            if args.domain and args.type:
                artifacts = [a for a in artifacts if a.artifact_type == args.type]
            
            if args.domain and args.lifecycle:
                artifacts = [a for a in artifacts if a.lifecycle_status == args.lifecycle]
            
            if args.type and args.lifecycle:
                artifacts = [a for a in artifacts if a.lifecycle_status == args.lifecycle]
            
            # Sort artifacts
            artifacts.sort(key=lambda a: a.artifact_id)
            
            # Display results
            if not artifacts:
                print("No artifacts found matching the criteria")
                return 0
            
            print(f"Found {len(artifacts)} artifact(s):")
            print()
            
            for artifact in artifacts:
                print(f"  {artifact.artifact_id}")
                print(f"    File: {artifact.file_path}")
                print(f"    Domain: {artifact.primary_domain}")
                print(f"    Type: {artifact.artifact_type}")
                print(f"    Lifecycle: {artifact.lifecycle_status}")
                
                if args.verbose:
                    print(f"    Owner: {artifact.owner_role}")
                    print(f"    SSOT: {artifact.ssot_relationship}")
                    print(f"    Created: {artifact.created_date}")
                    print(f"    Modified: {artifact.last_modified}")
                    
                    if artifact.secondary_domains:
                        print(f"    Secondary Domains: {', '.join(artifact.secondary_domains)}")
                    
                    if artifact.dependencies:
                        print(f"    Dependencies: {', '.join(artifact.dependencies)}")
                    
                    if artifact.topic:
                        print(f"    Topic: {artifact.topic}")
                    
                    if artifact.description:
                        print(f"    Description: {artifact.description}")
                    
                    if artifact.tags:
                        print(f"    Tags: {', '.join(artifact.tags)}")
                
                print()
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def show(self, args: argparse.Namespace) -> int:
        """
        Show detailed information about an artifact
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Load registries
            self.artifact_registry.load()
            self.domain_registry.load()
            self.lifecycle_manager.load()
            
            # Get artifact
            artifact = self.artifact_registry.get_artifact(args.artifact_id)
            if artifact is None:
                print(f"Error: Artifact '{args.artifact_id}' not found", file=sys.stderr)
                return 1
            
            # Display artifact details
            print("=" * 80)
            print(f"ARTIFACT: {artifact.artifact_id}")
            print("=" * 80)
            print()
            
            print("Basic Information:")
            print(f"  File Path:        {artifact.file_path}")
            print(f"  Primary Domain:   {artifact.primary_domain}")
            print(f"  Artifact Type:    {artifact.artifact_type}")
            print(f"  Lifecycle Status: {artifact.lifecycle_status}")
            print(f"  Owner Role:       {artifact.owner_role}")
            print(f"  SSOT Relationship: {artifact.ssot_relationship}")
            print()
            
            print("Dates:")
            print(f"  Created:      {artifact.created_date}")
            print(f"  Last Modified: {artifact.last_modified}")
            print()
            
            print("Permissions:")
            print(f"  Allowed Writers: {', '.join(artifact.allowed_writers)}")
            print(f"  Allowed Readers: {', '.join(artifact.allowed_readers)}")
            print()
            
            if artifact.secondary_domains:
                print("Secondary Domains:")
                for domain_id in artifact.secondary_domains:
                    domain = self.domain_registry.get_domain(domain_id)
                    if domain:
                        print(f"  - {domain_id}: {domain.name}")
                    else:
                        print(f"  - {domain_id}")
                print()
            
            if artifact.dependencies:
                print("Dependencies:")
                for dep_id in artifact.dependencies:
                    dep = self.artifact_registry.get_artifact(dep_id)
                    if dep:
                        print(f"  - {dep_id} ({dep.artifact_type})")
                    else:
                        print(f"  - {dep_id} (not found)")
                print()
            
            if artifact.topic:
                print(f"Topic: {artifact.topic}")
                print()
            
            if artifact.description:
                print(f"Description: {artifact.description}")
                print()
            
            if artifact.tags:
                print(f"Tags: {', '.join(artifact.tags)}")
                print()
            
            # Show lifecycle information
            state_machine = self.lifecycle_manager.get_state_machine(artifact.artifact_type)
            if state_machine:
                allowed_transitions = state_machine.get_allowed_transitions(artifact.lifecycle_status)
                if allowed_transitions:
                    print("Allowed Lifecycle Transitions:")
                    for next_state in allowed_transitions:
                        print(f"  - {artifact.lifecycle_status} → {next_state}")
                    print()
            
            # Show domain information
            domain = self.domain_registry.get_domain(artifact.primary_domain)
            if domain:
                print("Domain Information:")
                print(f"  Name: {domain.name}")
                print(f"  Priority: {domain.priority}")
                print(f"  Responsibility: {domain.responsibility_scope}")
                print()
            
            print("=" * 80)
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1


def add_register_parser(subparsers):
    """Add 'register' command parser"""
    parser = subparsers.add_parser(
        'register',
        help='Register a new artifact',
        description='Register a new artifact in the domainization system'
    )
    
    # Required arguments
    parser.add_argument('artifact_id', help='Unique artifact identifier')
    parser.add_argument('file_path', help='Path to artifact file (relative to repo root)')
    parser.add_argument('domain', help='Primary domain ID')
    parser.add_argument('type', help='Artifact type')
    
    # Optional arguments
    parser.add_argument('--lifecycle', help='Lifecycle status (uses initial state if not provided)')
    parser.add_argument('--owner-role', help='Owner role description')
    parser.add_argument('--ssot-relationship', choices=['canonical', 'derived', 'implementation', 'none'],
                       help='SSOT relationship')
    parser.add_argument('--allowed-writers', nargs='+', help='List of domain IDs with write permission')
    parser.add_argument('--allowed-readers', nargs='+', help='List of domain IDs with read permission')
    parser.add_argument('--secondary-domains', nargs='+', help='Secondary domain IDs')
    parser.add_argument('--dependencies', nargs='+', help='Artifact IDs this depends on')
    parser.add_argument('--topic', help='Topic for SSOT conflict detection')
    parser.add_argument('--description', help='Artifact description')
    parser.add_argument('--tags', nargs='+', help='Tags for categorization')
    parser.add_argument('--force', action='store_true', 
                       help='Force operation, bypassing governance checks (logged to audit trail)')
    parser.add_argument('--force-reason', help='Required reason when using --force (logged to audit trail)')
    
    return parser


def add_update_parser(subparsers):
    """Add 'update' command parser"""
    parser = subparsers.add_parser(
        'update',
        help='Update artifact metadata',
        description='Update metadata for an existing artifact'
    )
    
    # Required arguments
    parser.add_argument('artifact_id', help='Artifact identifier to update')
    
    # Optional arguments (all fields that can be updated)
    parser.add_argument('--domain', help='New primary domain ID')
    parser.add_argument('--lifecycle', help='New lifecycle status')
    parser.add_argument('--file-path', help='New file path')
    parser.add_argument('--owner-role', help='New owner role description')
    parser.add_argument('--ssot-relationship', choices=['canonical', 'derived', 'implementation', 'none'],
                       help='New SSOT relationship')
    parser.add_argument('--allowed-writers', nargs='+', help='New list of domain IDs with write permission')
    parser.add_argument('--allowed-readers', nargs='+', help='New list of domain IDs with read permission')
    parser.add_argument('--secondary-domains', nargs='+', help='New secondary domain IDs')
    parser.add_argument('--dependencies', nargs='+', help='New artifact IDs this depends on')
    parser.add_argument('--topic', help='New topic')
    parser.add_argument('--description', help='New description')
    parser.add_argument('--tags', nargs='+', help='New tags')
    parser.add_argument('--force', action='store_true',
                       help='Force operation, bypassing governance checks (logged to audit trail)')
    parser.add_argument('--force-reason', help='Required reason when using --force (logged to audit trail)')
    
    return parser


def add_list_parser(subparsers):
    """Add 'list' command parser"""
    parser = subparsers.add_parser(
        'list',
        help='List artifacts',
        description='List artifacts with optional filters'
    )
    
    # Filter arguments
    parser.add_argument('--domain', help='Filter by domain ID')
    parser.add_argument('--type', help='Filter by artifact type')
    parser.add_argument('--lifecycle', help='Filter by lifecycle status')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed information')
    
    return parser


def add_show_parser(subparsers):
    """Add 'show' command parser"""
    parser = subparsers.add_parser(
        'show',
        help='Show artifact details',
        description='Display detailed information about an artifact'
    )
    
    # Required arguments
    parser.add_argument('artifact_id', help='Artifact identifier to show')
    
    return parser
