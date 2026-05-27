"""
Integration tests for complete CLI workflow

Tests the full CLI workflow using the actual CLI in place.
"""

import pytest
import subprocess
from pathlib import Path


class TestCLIIntegration:
    """Integration tests for complete CLI workflow"""
    
    def test_cli_help(self):
        """Test CLI help output"""
        cli_path = Path(__file__).parent / "cli_main.py"
        
        result = subprocess.run(
            ['python3', str(cli_path), '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'domainization' in result.stdout
        assert 'register' in result.stdout
        assert 'validate' in result.stdout
        assert 'health' in result.stdout
    
    def test_cli_version(self):
        """Test CLI version output"""
        cli_path = Path(__file__).parent / "cli_main.py"
        
        result = subprocess.run(
            ['python3', str(cli_path), '--version'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'domainization' in result.stdout
    
    def test_register_help(self):
        """Test register command help"""
        cli_path = Path(__file__).parent / "cli_main.py"
        
        result = subprocess.run(
            ['python3', str(cli_path), 'register', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'Register a new artifact' in result.stdout
    
    def test_validate_help(self):
        """Test validate command help"""
        cli_path = Path(__file__).parent / "cli_main.py"
        
        result = subprocess.run(
            ['python3', str(cli_path), 'validate', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'validation' in result.stdout.lower()
    
    def test_health_help(self):
        """Test health command help"""
        cli_path = Path(__file__).parent / "cli_main.py"
        
        result = subprocess.run(
            ['python3', str(cli_path), 'health', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'health report' in result.stdout.lower()
    
    def test_config_help(self):
        """Test config command help"""
        cli_path = Path(__file__).parent / "cli_main.py"
        
        result = subprocess.run(
            ['python3', str(cli_path), 'config', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'configuration' in result.stdout.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
