"""
CLI commands for configuration management

Provides commands for:
- Displaying current configuration
- Modifying configuration
- Setting enforcement mode (soft/hard)
- Enabling/disabling specific gates
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import yaml


class ConfigCommands:
    """Configuration CLI commands"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize config commands
        
        Args:
            config_path: Path to config.yaml file (uses default if None)
        """
        if config_path is None:
            # Default to .domainization/config.yaml
            self.config_path = Path(__file__).parent.parent / "config.yaml"
        else:
            self.config_path = Path(config_path)
    
    def show(self, args: argparse.Namespace) -> int:
        """
        Display current configuration
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Load configuration
            config = self._load_config()
            
            # Display configuration
            print("=" * 80)
            print("DOMAINIZATION CONFIGURATION")
            print("=" * 80)
            print()
            
            print(f"Configuration File: {self.config_path}")
            print()
            
            print("Enforcement Mode:")
            print(f"  {config.get('enforcement_mode', 'observability')}")
            print()
            
            print("Observer Status:")
            observers = config.get('observers', {})
            for observer_name in [
                'RegistrationValidator',
                'DomainAssignmentValidator',
                'LifecycleValidator',
                'BoundaryAwarenessValidator',
                'SSOTConsistencyValidator'
            ]:
                enabled = observers.get(observer_name, {}).get('enabled', True)
                status = "✓ Enabled" if enabled else "✗ Disabled"
                print(f"  {observer_name}: {status}")
            
            print()
            
            # Show additional settings
            if 'performance' in config:
                print("Performance Settings:")
                perf = config['performance']
                print(f"  Validation Timeout: {perf.get('validation_timeout_ms', 5000)}ms")
                print(f"  Health Report Timeout: {perf.get('health_report_timeout_ms', 10000)}ms")
                print()
            
            if 'logging' in config:
                print("Logging Settings:")
                logging = config['logging']
                print(f"  Level: {logging.get('level', 'INFO')}")
                print(f"  Audit Enabled: {logging.get('audit_enabled', True)}")
                print()
            
            print("=" * 80)
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def set_config(self, args: argparse.Namespace) -> int:
        """
        Modify configuration
        
        Args:
            args: Parsed command-line arguments
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Load existing configuration
            config = self._load_config()
            
            # Update enforcement mode if provided
            if args.enforcement_mode:
                if args.enforcement_mode not in ['observability', 'soft', 'hard']:
                    print(f"Error: Invalid enforcement mode '{args.enforcement_mode}'", file=sys.stderr)
                    print("Valid modes: observability, soft, hard")
                    return 1
                
                config['enforcement_mode'] = args.enforcement_mode
                print(f"✓ Set enforcement_mode to '{args.enforcement_mode}'")
            
            # Enable/disable observers
            if args.enable_observer:
                if 'observers' not in config:
                    config['observers'] = {}
                
                for observer_name in args.enable_observer:
                    if observer_name not in config['observers']:
                        config['observers'][observer_name] = {}
                    
                    config['observers'][observer_name]['enabled'] = True
                    print(f"✓ Enabled observer: {observer_name}")
            
            if args.disable_observer:
                if 'observers' not in config:
                    config['observers'] = {}
                
                for observer_name in args.disable_observer:
                    if observer_name not in config['observers']:
                        config['observers'][observer_name] = {}
                    
                    config['observers'][observer_name]['enabled'] = False
                    print(f"✓ Disabled observer: {observer_name}")
            
            # Update performance settings
            if args.validation_timeout:
                if 'performance' not in config:
                    config['performance'] = {}
                
                config['performance']['validation_timeout_ms'] = args.validation_timeout
                print(f"✓ Set validation_timeout_ms to {args.validation_timeout}")
            
            if args.health_report_timeout:
                if 'performance' not in config:
                    config['performance'] = {}
                
                config['performance']['health_report_timeout_ms'] = args.health_report_timeout
                print(f"✓ Set health_report_timeout_ms to {args.health_report_timeout}")
            
            # Update logging settings
            if args.log_level:
                if 'logging' not in config:
                    config['logging'] = {}
                
                config['logging']['level'] = args.log_level
                print(f"✓ Set log level to {args.log_level}")
            
            if args.audit_enabled is not None:
                if 'logging' not in config:
                    config['logging'] = {}
                
                config['logging']['audit_enabled'] = args.audit_enabled
                status = "enabled" if args.audit_enabled else "disabled"
                print(f"✓ Audit logging {status}")
            
            # Save configuration
            self._save_config(config)
            print()
            print(f"Configuration saved to: {self.config_path}")
            
            return 0
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _load_config(self) -> dict:
        """Load configuration from file"""
        if not self.config_path.exists():
            # Return default configuration
            return self._get_default_config()
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config if config else self._get_default_config()
    
    def _save_config(self, config: dict) -> None:
        """Save configuration to file"""
        # Create parent directory if needed
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save configuration
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            'enforcement_mode': 'observability',
            'observers': {
                'RegistrationValidator': {'enabled': True},
                'DomainAssignmentValidator': {'enabled': True},
                'LifecycleValidator': {'enabled': True},
                'BoundaryAwarenessValidator': {'enabled': True},
                'SSOTConsistencyValidator': {'enabled': True}
            },
            'performance': {
                'validation_timeout_ms': 5000,
                'health_report_timeout_ms': 10000
            },
            'logging': {
                'level': 'INFO',
                'audit_enabled': True
            }
        }


def add_config_show_parser(subparsers):
    """Add 'config show' command parser"""
    parser = subparsers.add_parser(
        'show',
        help='Display current configuration',
        description='Display current domainization configuration'
    )
    
    return parser


def add_config_set_parser(subparsers):
    """Add 'config set' command parser"""
    parser = subparsers.add_parser(
        'set',
        help='Modify configuration',
        description='Modify domainization configuration'
    )
    
    # Enforcement mode
    parser.add_argument('--enforcement-mode',
                       choices=['observability', 'soft', 'hard'],
                       help='Set enforcement mode')
    
    # Observer control
    parser.add_argument('--enable-observer', nargs='+',
                       choices=[
                           'RegistrationValidator',
                           'DomainAssignmentValidator',
                           'LifecycleValidator',
                           'BoundaryAwarenessValidator',
                           'SSOTConsistencyValidator'
                       ],
                       help='Enable specific observers')
    
    parser.add_argument('--disable-observer', nargs='+',
                       choices=[
                           'RegistrationValidator',
                           'DomainAssignmentValidator',
                           'LifecycleValidator',
                           'BoundaryAwarenessValidator',
                           'SSOTConsistencyValidator'
                       ],
                       help='Disable specific observers')
    
    # Performance settings
    parser.add_argument('--validation-timeout', type=int,
                       help='Validation timeout in milliseconds')
    
    parser.add_argument('--health-report-timeout', type=int,
                       help='Health report timeout in milliseconds')
    
    # Logging settings
    parser.add_argument('--log-level',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Set logging level')
    
    parser.add_argument('--audit-enabled', type=lambda x: x.lower() == 'true',
                       help='Enable/disable audit logging (true/false)')
    
    return parser
