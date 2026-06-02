"""
Integration tests for CLI configuration commands
"""

import pytest
import argparse
from pathlib import Path
import tempfile
import shutil
import yaml

from cli_config_commands import ConfigCommands


@pytest.fixture
def temp_config_dir():
    """Create temporary directory for test config"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_config_path(temp_config_dir):
    """Create test config file"""
    config_path = temp_config_dir / "config.yaml"
    
    # Create initial config
    config_data = {
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
    
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    
    return config_path


class TestConfigShowCommand:
    """Tests for config show command"""
    
    def test_show_existing_config(self, test_config_path):
        """Test showing existing configuration"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace()
        
        result = commands.show(args)
        
        assert result == 0
    
    def test_show_nonexistent_config(self, temp_config_dir):
        """Test showing config when file doesn't exist (should show defaults)"""
        config_path = temp_config_dir / "nonexistent_config.yaml"
        commands = ConfigCommands(config_path)
        
        args = argparse.Namespace()
        
        result = commands.show(args)
        
        assert result == 0


class TestConfigSetCommand:
    """Tests for config set command"""
    
    def test_set_enforcement_mode(self, test_config_path):
        """Test setting enforcement mode"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode='hard',
            enable_observer=None,
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['enforcement_mode'] == 'hard'
    
    def test_set_invalid_enforcement_mode(self, test_config_path):
        """Test setting invalid enforcement mode"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode='invalid',
            enable_observer=None,
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 1
    
    def test_enable_observer(self, test_config_path):
        """Test enabling an observer"""
        commands = ConfigCommands(test_config_path)
        
        # First disable it
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=None,
            disable_observer=['RegistrationValidator'],
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        commands.set_config(args)
        
        # Then enable it
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=['RegistrationValidator'],
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['observers']['RegistrationValidator']['enabled'] is True
    
    def test_disable_observer(self, test_config_path):
        """Test disabling an observer"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=None,
            disable_observer=['DomainAssignmentValidator'],
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['observers']['DomainAssignmentValidator']['enabled'] is False
    
    def test_set_validation_timeout(self, test_config_path):
        """Test setting validation timeout"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=None,
            disable_observer=None,
            validation_timeout=3000,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['performance']['validation_timeout_ms'] == 3000
    
    def test_set_health_report_timeout(self, test_config_path):
        """Test setting health report timeout"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=None,
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=15000,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['performance']['health_report_timeout_ms'] == 15000
    
    def test_set_log_level(self, test_config_path):
        """Test setting log level"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=None,
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=None,
            log_level='DEBUG',
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['logging']['level'] == 'DEBUG'
    
    def test_set_audit_enabled(self, test_config_path):
        """Test enabling/disabling audit logging"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode=None,
            enable_observer=None,
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=False
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify config was updated
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['logging']['audit_enabled'] is False
    
    def test_set_multiple_options(self, test_config_path):
        """Test setting multiple configuration options at once"""
        commands = ConfigCommands(test_config_path)
        
        args = argparse.Namespace(
            enforcement_mode='soft',
            enable_observer=['RegistrationValidator'],
            disable_observer=['LifecycleValidator'],
            validation_timeout=4000,
            health_report_timeout=12000,
            log_level='WARNING',
            audit_enabled=True
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        
        # Verify all config changes
        with open(test_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert config['enforcement_mode'] == 'soft'
        assert config['observers']['RegistrationValidator']['enabled'] is True
        assert config['observers']['LifecycleValidator']['enabled'] is False
        assert config['performance']['validation_timeout_ms'] == 4000
        assert config['performance']['health_report_timeout_ms'] == 12000
        assert config['logging']['level'] == 'WARNING'
        assert config['logging']['audit_enabled'] is True
    
    def test_create_config_if_not_exists(self, temp_config_dir):
        """Test creating config file if it doesn't exist"""
        config_path = temp_config_dir / "new_config.yaml"
        commands = ConfigCommands(config_path)
        
        args = argparse.Namespace(
            enforcement_mode='observability',
            enable_observer=None,
            disable_observer=None,
            validation_timeout=None,
            health_report_timeout=None,
            log_level=None,
            audit_enabled=None
        )
        
        result = commands.set_config(args)
        
        assert result == 0
        assert config_path.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
