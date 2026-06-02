"""
Integration tests for CLI registry commands
"""

import pytest
import argparse
from pathlib import Path
from datetime import datetime
import tempfile
import shutil
import yaml

from cli_registry_commands import RegistryCommands
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from artifact_schema import ArtifactMetadata


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


class TestRegisterCommand:
    """Tests for register command"""
    
    def test_register_new_artifact(self, test_registries):
        """Test registering a new artifact"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        # Create args
        args = argparse.Namespace(
            artifact_id='new_artifact',
            file_path='test/new_file.py',
            domain='SIGNALS',
            type='ENGINE',
            lifecycle=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description='Test artifact',
            tags=['test']
        )
        
        # Register artifact
        result = commands.register(args)
        
        assert result == 0
        
        # Verify artifact was registered
        artifact = test_registries['artifact_registry'].get_artifact('new_artifact')
        assert artifact is not None
        assert artifact.artifact_id == 'new_artifact'
        assert artifact.file_path == 'test/new_file.py'
        assert artifact.primary_domain == 'SIGNALS'
        assert artifact.artifact_type == 'ENGINE'
        assert artifact.lifecycle_status == 'planned'  # Initial state
        assert artifact.description == 'Test artifact'
        assert artifact.tags == ['test']
    
    def test_register_with_invalid_domain(self, test_registries):
        """Test registering with invalid domain"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='invalid_artifact',
            file_path='test/file.py',
            domain='INVALID',
            type='ENGINE',
            lifecycle=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.register(args)
        
        assert result == 1
    
    def test_register_with_invalid_domain_type_combination(self, test_registries):
        """Test registering with domain that cannot own type"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='invalid_artifact',
            file_path='test/file.py',
            domain='SIGNALS',
            type='REPORT_OUT',  # SIGNALS cannot own REPORT_OUT
            lifecycle=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.register(args)
        
        assert result == 1
    
    def test_register_duplicate_artifact_id(self, test_registries):
        """Test registering with duplicate artifact_id"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='test_artifact_1',  # Already exists
            file_path='test/file.py',
            domain='SIGNALS',
            type='ENGINE',
            lifecycle=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.register(args)
        
        assert result == 1


class TestUpdateCommand:
    """Tests for update command"""
    
    def test_update_artifact_lifecycle(self, test_registries):
        """Test updating artifact lifecycle status"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='test_artifact_1',
            domain=None,
            lifecycle='deprecated',
            file_path=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.update(args)
        
        assert result == 0
        
        # Verify update
        artifact = test_registries['artifact_registry'].get_artifact('test_artifact_1')
        assert artifact.lifecycle_status == 'deprecated'
    
    def test_update_artifact_domain(self, test_registries):
        """Test updating artifact domain"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='test_artifact_1',
            domain='REPORT',
            lifecycle=None,
            file_path=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.update(args)
        
        assert result == 0
        
        # Verify update
        artifact = test_registries['artifact_registry'].get_artifact('test_artifact_1')
        assert artifact.primary_domain == 'REPORT'
    
    def test_update_nonexistent_artifact(self, test_registries):
        """Test updating artifact that doesn't exist"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='nonexistent',
            domain='SIGNALS',
            lifecycle=None,
            file_path=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.update(args)
        
        assert result == 1
    
    def test_update_with_invalid_lifecycle_transition(self, test_registries):
        """Test updating with invalid lifecycle transition"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='test_artifact_1',
            domain=None,
            lifecycle='planned',  # Cannot go from active to planned
            file_path=None,
            owner_role=None,
            ssot_relationship=None,
            allowed_writers=None,
            allowed_readers=None,
            secondary_domains=None,
            dependencies=None,
            topic=None,
            description=None,
            tags=None
        )
        
        result = commands.update(args)
        
        assert result == 1


class TestListCommand:
    """Tests for list command"""
    
    def test_list_all_artifacts(self, test_registries):
        """Test listing all artifacts"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            domain=None,
            type=None,
            lifecycle=None,
            verbose=False
        )
        
        result = commands.list_artifacts(args)
        
        assert result == 0
    
    def test_list_by_domain(self, test_registries):
        """Test listing artifacts by domain"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            domain='SIGNALS',
            type=None,
            lifecycle=None,
            verbose=False
        )
        
        result = commands.list_artifacts(args)
        
        assert result == 0
    
    def test_list_by_type(self, test_registries):
        """Test listing artifacts by type"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            domain=None,
            type='ENGINE',
            lifecycle=None,
            verbose=False
        )
        
        result = commands.list_artifacts(args)
        
        assert result == 0
    
    def test_list_by_lifecycle(self, test_registries):
        """Test listing artifacts by lifecycle"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            domain=None,
            type=None,
            lifecycle='active',
            verbose=False
        )
        
        result = commands.list_artifacts(args)
        
        assert result == 0
    
    def test_list_with_multiple_filters(self, test_registries):
        """Test listing with multiple filters"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            domain='SIGNALS',
            type='ENGINE',
            lifecycle='active',
            verbose=True
        )
        
        result = commands.list_artifacts(args)
        
        assert result == 0


class TestShowCommand:
    """Tests for show command"""
    
    def test_show_artifact(self, test_registries):
        """Test showing artifact details"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='test_artifact_1'
        )
        
        result = commands.show(args)
        
        assert result == 0
    
    def test_show_nonexistent_artifact(self, test_registries):
        """Test showing artifact that doesn't exist"""
        commands = RegistryCommands(
            test_registries['artifact_registry'],
            test_registries['domain_registry'],
            test_registries['lifecycle_manager']
        )
        
        args = argparse.Namespace(
            artifact_id='nonexistent'
        )
        
        result = commands.show(args)
        
        assert result == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
