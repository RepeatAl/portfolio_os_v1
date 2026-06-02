"""
Integration tests for CLI health commands
"""

import pytest
import argparse
from pathlib import Path
import tempfile
import shutil
import yaml

from cli_health_commands import HealthCommands
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager


@pytest.fixture
def temp_registry_dir():
    """Create temporary directory for test registries"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_registries(temp_registry_dir):
    """Create test registries with sample data"""
    # Create artifact registry
    artifact_registry_path = temp_registry_dir / "artifact_registry.yaml"
    artifact_data = {
        'artifacts': [
            {
                'artifact_id': 'test_artifact_1',
                'file_path': 'test/file1.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'SIGNALS domain owner',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL']
            },
            {
                'artifact_id': 'test_artifact_2',
                'file_path': 'test/file2.py',
                'primary_domain': 'REPORT',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'development',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'REPORT domain owner',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['REPORT'],
                'allowed_readers': ['ALL']
            },
            {
                'artifact_id': 'test_ssot_1',
                'file_path': 'docs/test_doc.md',
                'primary_domain': 'ARCH',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'ARCH domain owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['ARCH'],
                'allowed_readers': ['ALL'],
                'topic': 'test_topic'
            }
        ]
    }
    
    with open(artifact_registry_path, 'w') as f:
        yaml.dump(artifact_data, f)
    
    # Create domain registry
    domain_registry_path = temp_registry_dir / "domain_registry.yaml"
    domain_data = {
        'domains': [
            {
                'domain_id': 'SIGNALS',
                'name': 'Signal Generation',
                'responsibility_scope': 'Generate structured signals',
                'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT'],
                'cannot_own': ['REPORT_OUT'],
                'priority': 'core',
                'authority_level': 1
            },
            {
                'domain_id': 'ARCH',
                'name': 'Architecture',
                'responsibility_scope': 'System architecture',
                'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                'cannot_own': ['REPORT_OUT'],
                'priority': 'surface',
                'authority_level': None
            },
            {
                'domain_id': 'REPORT',
                'name': 'Report Generation',
                'responsibility_scope': 'Generate reports',
                'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT'],
                'cannot_own': ['DATA_OUT'],
                'priority': 'core',
                'authority_level': 4
            }
        ]
    }
    
    with open(domain_registry_path, 'w') as f:
        yaml.dump(domain_data, f)
    
    # Create lifecycle state machine
    lifecycle_path = temp_registry_dir / "lifecycle_state_machine.yaml"
    lifecycle_data = {
        'artifact_types': {
            'ENGINE': {
                'description': 'Engine lifecycle',
                'states': ['planned', 'development', 'active', 'deprecated'],
                'initial_state': 'planned',
                'transitions': [
                    {'from': 'planned', 'to': 'development', 'condition': 'Implementation begins'},
                    {'from': 'development', 'to': 'active', 'condition': 'Production ready'},
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                ],
                'modifiable_states': ['planned', 'development', 'active'],
                'read_only_states': ['deprecated']
            },
            'SSOT': {
                'description': 'SSOT lifecycle',
                'states': ['draft', 'review', 'canonical', 'deprecated'],
                'initial_state': 'draft',
                'transitions': [
                    {'from': 'draft', 'to': 'review', 'condition': 'Ready for review'},
                    {'from': 'review', 'to': 'canonical', 'condition': 'Approved'},
                    {'from': 'canonical', 'to': 'deprecated', 'condition': 'Superseded'}
                ],
                'modifiable_states': ['draft', 'review', 'canonical'],
                'read_only_states': ['deprecated']
            }
        }
    }
    
    with open(lifecycle_path, 'w') as f:
        yaml.dump(lifecycle_data, f)
    
    # Create registry instances
    artifact_registry = ArtifactRegistry(artifact_registry_path)
    domain_registry = DomainRegistry(domain_registry_path)
    lifecycle_manager = LifecycleManager(lifecycle_path)
    
    return {
        'artifact_registry': artifact_registry,
        'domain_registry': domain_registry,
        'lifecycle_manager': lifecycle_manager,
        'temp_dir': temp_registry_dir
    }


class TestHealthCommand:
    """Tests for health command"""
    
    def test_generate_health_report(self, test_registries):
        """Test generating basic health report"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        args = argparse.Namespace(
            domain=None,
            output=None,
            violations_only=False,
            no_violations=False,
            quiet=False
        )
        
        result = commands.health(args)
        
        assert result == 0
    
    def test_health_report_filter_by_domain(self, test_registries):
        """Test filtering health report by domain"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        args = argparse.Namespace(
            domain='SIGNALS',
            output=None,
            violations_only=False,
            no_violations=False,
            quiet=False
        )
        
        result = commands.health(args)
        
        assert result == 0
    
    def test_health_report_save_to_file(self, test_registries, temp_registry_dir):
        """Test saving health report to file"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        output_path = temp_registry_dir / "health_report.yaml"
        
        args = argparse.Namespace(
            domain=None,
            output=str(output_path),
            violations_only=False,
            no_violations=False,
            quiet=False
        )
        
        result = commands.health(args)
        
        assert result == 0
        assert output_path.exists()
        
        # Verify file content
        with open(output_path, 'r') as f:
            report_data = yaml.safe_load(f)
        
        assert 'summary' in report_data
        assert 'domain_coverage' in report_data
        assert 'lifecycle_distribution' in report_data
    
    def test_health_report_violations_only(self, test_registries):
        """Test violations-only mode"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        args = argparse.Namespace(
            domain=None,
            output=None,
            violations_only=True,
            no_violations=False,
            quiet=False
        )
        
        result = commands.health(args)
        
        assert result == 0
    
    def test_health_report_no_violations(self, test_registries):
        """Test excluding violations from report"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        args = argparse.Namespace(
            domain=None,
            output=None,
            violations_only=False,
            no_violations=True,
            quiet=False
        )
        
        result = commands.health(args)
        
        assert result == 0
    
    def test_health_report_quiet_mode(self, test_registries, temp_registry_dir):
        """Test quiet mode (no stdout when saving to file)"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        output_path = temp_registry_dir / "health_report_quiet.yaml"
        
        args = argparse.Namespace(
            domain=None,
            output=str(output_path),
            violations_only=False,
            no_violations=False,
            quiet=True
        )
        
        result = commands.health(args)
        
        assert result == 0
        assert output_path.exists()
    
    def test_health_report_combined_filters(self, test_registries, temp_registry_dir):
        """Test combining multiple filters"""
        commands = HealthCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager'],
            test_registries['temp_dir']
        )
        
        output_path = temp_registry_dir / "health_report_filtered.yaml"
        
        args = argparse.Namespace(
            domain='REPORT',
            output=str(output_path),
            violations_only=False,
            no_violations=False,
            quiet=True
        )
        
        result = commands.health(args)
        
        assert result == 0
        assert output_path.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
