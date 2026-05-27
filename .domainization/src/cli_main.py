#!/usr/bin/env python3
"""
Main CLI entry point for domainization system

Provides unified command-line interface for:
- Registry management (register, update, list, show)
- Validation (validate)
- Health reporting (health)
- Configuration (config show, config set)
"""

import argparse
import sys
from pathlib import Path

from cli_registry_commands import (
    RegistryCommands,
    add_register_parser,
    add_update_parser,
    add_list_parser,
    add_show_parser
)
from cli_validation_commands import (
    ValidationCommands,
    add_validate_parser
)
from cli_health_commands import (
    HealthCommands,
    add_health_parser
)
from cli_config_commands import (
    ConfigCommands,
    add_config_show_parser,
    add_config_set_parser
)
from cli_recovery_commands import (
    RecoveryCommands,
    add_recover_parser
)


def main():
    """Main CLI entry point"""
    # Create main parser
    parser = argparse.ArgumentParser(
        prog='domainization',
        description='Domainization system CLI - Artifact governance and validation',
        epilog='For more information, see .domainization/docs/'
    )
    
    parser.add_argument('--version', action='version', version='domainization 1.0.0')
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Registry management commands
    register_parser = add_register_parser(subparsers)
    update_parser = add_update_parser(subparsers)
    list_parser = add_list_parser(subparsers)
    show_parser = add_show_parser(subparsers)
    
    # Validation commands
    validate_parser = add_validate_parser(subparsers)
    
    # Health reporting commands
    health_parser = add_health_parser(subparsers)
    
    # Configuration commands
    config_parser = subparsers.add_parser(
        'config',
        help='Configuration management',
        description='Manage domainization configuration'
    )
    config_subparsers = config_parser.add_subparsers(dest='config_command', help='Config commands')
    config_show_parser = add_config_show_parser(config_subparsers)
    config_set_parser = add_config_set_parser(config_subparsers)
    
    # Recovery commands
    recover_parser = add_recover_parser(subparsers)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        if args.command == 'register':
            commands = RegistryCommands()
            return commands.register(args)
        
        elif args.command == 'update':
            commands = RegistryCommands()
            return commands.update(args)
        
        elif args.command == 'list':
            commands = RegistryCommands()
            return commands.list_artifacts(args)
        
        elif args.command == 'show':
            commands = RegistryCommands()
            return commands.show(args)
        
        elif args.command == 'validate':
            commands = ValidationCommands()
            return commands.validate(args)
        
        elif args.command == 'health':
            commands = HealthCommands()
            return commands.health(args)
        
        elif args.command == 'config':
            if not args.config_command:
                config_parser.print_help()
                return 1
            
            commands = ConfigCommands()
            
            if args.config_command == 'show':
                return commands.show(args)
            elif args.config_command == 'set':
                return commands.set_config(args)
        
        elif args.command == 'recover':
            if not hasattr(args, 'recover_command') or not args.recover_command:
                recover_parser.print_help()
                return 1
            
            commands = RecoveryCommands()
            
            if args.recover_command == 'list':
                return commands.list_backups(args)
            elif args.recover_command == 'restore':
                return commands.restore_backup(args)
            elif args.recover_command == 'latest':
                return commands.restore_latest(args)
        
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            parser.print_help()
            return 1
    
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
