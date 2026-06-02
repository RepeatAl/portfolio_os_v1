"""
Comprehensive Unit Test Suite for Domainization System

Covers all core components with targeted tests to achieve >90% code coverage:
- Artifact metadata validation
- Domain definition validation
- Lifecycle state machine logic
- All 5 commit gates (observers/validators)
- Health reporter and violation detector
- Registry cache

Requirements: 15.1, 15.2, 15.3, 15.5, 15.6, 15.7, 15.8
"""

import pytest
import tempfile
import shutil
import yaml
import time
from pathlib import Path
from datetime import datetime, timedelta

from artifact_schema import ArtifactMetadata, validate_artifact_dict
from domain_schema import DomainDefinition, validate_domain_dict
from lifecycle_schema import StateMachine, StateTransition, validate_state_machine_dict
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from registry_cache import RegistryCache
from health_reporter import HealthReporter
from violation_detector import Violation, ViolationDetector
from validation_result import ValidationWarning, ValidationResult, WarningCodes


# =============================================================================
# SECTION 1: Artifact Metadata Validation Tests
# =============================================================================

class TestArtifactMetadataValidation:
    """Tests for artifact metadata validation covering all required field checks"""

    def test_empty_artifact_id_fails(self):
        """Validate that empty artifact_id is caught"""
        metadata = ArtifactMetadata(
            artifact_id="",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "artifact_id is required" in errors

    def test_empty_file_path_fails(self):
        """Validate that empty file_path is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "file_path is required" in errors

    def test_empty_primary_domain_fails(self):
        """Validate that empty primary_domain is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "primary_domain is required" in errors

    def test_empty_artifact_type_fails(self):
        """Validate that empty artifact_type is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "artifact_type is required" in errors

    def test_empty_lifecycle_status_fails(self):
        """Validate that empty lifecycle_status is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "lifecycle_status is required" in errors

    def test_empty_created_date_fails(self):
        """Validate that empty created_date is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "created_date is required" in errors

    def test_empty_last_modified_fails(self):
        """Validate that empty last_modified is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "last_modified is required" in errors

    def test_empty_owner_role_fails(self):
        """Validate that empty owner_role is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "owner_role is required" in errors

    def test_empty_ssot_relationship_fails(self):
        """Validate that empty ssot_relationship is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "ssot_relationship is required" in errors

    def test_empty_allowed_writers_fails(self):
        """Validate that empty allowed_writers is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=[],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "allowed_writers is required" in errors

    def test_empty_allowed_readers_fails(self):
        """Validate that empty allowed_readers is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=[]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert "allowed_readers is required" in errors

    def test_invalid_created_date_format(self):
        """Validate that invalid date format is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="01-01-2026",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert any("created_date must be in YYYY-MM-DD format" in e for e in errors)

    def test_invalid_last_modified_format(self):
        """Validate that invalid last_modified date format is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="January 1, 2026",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert any("last_modified must be in YYYY-MM-DD format" in e for e in errors)

    def test_invalid_ssot_relationship_value(self):
        """Validate that invalid ssot_relationship value is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="invalid_value",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert any("ssot_relationship must be one of" in e for e in errors)

    def test_non_list_secondary_domains_fails(self):
        """Validate that non-list secondary_domains is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"],
            secondary_domains="SIGNALS"  # Should be a list
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert any("secondary_domains must be a list" in e for e in errors)

    def test_non_list_dependencies_fails(self):
        """Validate that non-list dependencies is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"],
            dependencies="some_dep"  # Should be a list
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert any("dependencies must be a list" in e for e in errors)

    def test_non_list_tags_fails(self):
        """Validate that non-list tags is caught"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"],
            tags="tag1"  # Should be a list
        )
        is_valid, errors = metadata.validate()
        assert not is_valid
        assert any("tags must be a list" in e for e in errors)

    def test_validate_artifact_dict_with_exception(self):
        """Validate that exception during dict validation is caught"""
        # Pass a dict that will cause an exception during object creation
        bad_dict = {
            'artifact_id': 'test',
            'file_path': 'test.py',
            'primary_domain': 'ARCH',
            'artifact_type': 'ENGINE',
            'lifecycle_status': 'active',
            'created_date': '2026-01-01',
            'last_modified': '2026-01-01',
            'owner_role': 'Engineer',
            'ssot_relationship': 'implementation',
            'allowed_writers': None,  # This will cause issues
            'allowed_readers': None   # This will cause issues
        }
        is_valid, errors = validate_artifact_dict(bad_dict)
        # Should either fail validation or catch exception
        assert not is_valid or len(errors) > 0

    def test_is_modifiable_for_archived_artifact(self):
        """Validate that archived artifacts are not modifiable"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="REPORT_OUT",
            lifecycle_status="archived",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="none",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        assert not metadata.is_modifiable()

    def test_is_modifiable_for_superseded_artifact(self):
        """Validate that superseded artifacts are not modifiable"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="superseded",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="none",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        assert not metadata.is_modifiable()

    def test_can_read_for_specific_domain_not_in_list(self):
        """Validate that domain not in allowed_readers cannot read"""
        metadata = ArtifactMetadata(
            artifact_id="test_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ARCH", "SIGNALS"]
        )
        assert metadata.can_read("ARCH")
        assert metadata.can_read("SIGNALS")
        assert not metadata.can_read("REPORT")


# =============================================================================
# SECTION 2: Domain Definition Validation Tests
# =============================================================================

class TestDomainDefinitionValidationComprehensive:
    """Tests for domain definition validation covering all edge cases"""

    def test_empty_domain_id_fails(self):
        """Validate that empty domain_id is caught"""
        domain = DomainDefinition(
            domain_id="",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority="surface"
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert "domain_id is required" in errors

    def test_empty_name_fails(self):
        """Validate that empty name is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority="surface"
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert "name is required" in errors

    def test_empty_responsibility_scope_fails(self):
        """Validate that empty responsibility_scope is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority="surface"
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert "responsibility_scope is required" in errors

    def test_empty_allowed_artifact_types_fails(self):
        """Validate that empty allowed_artifact_types is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=[],
            cannot_own=[],
            priority="surface"
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert "allowed_artifact_types is required" in errors

    def test_none_cannot_own_fails(self):
        """Validate that None cannot_own is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=None,
            priority="surface"
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert "cannot_own is required (can be empty list)" in errors

    def test_empty_priority_fails(self):
        """Validate that empty priority is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority=""
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert "priority is required" in errors

    def test_non_integer_authority_level_fails(self):
        """Validate that non-integer authority_level is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority="core",
            authority_level="high"  # Should be int
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any("authority_level must be an integer" in e for e in errors)

    def test_authority_level_below_range_fails(self):
        """Validate that authority_level below 1 is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority="core",
            authority_level=0
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any("authority_level must be between 1 and 4" in e for e in errors)

    def test_authority_level_above_range_fails(self):
        """Validate that authority_level above 4 is caught"""
        domain = DomainDefinition(
            domain_id="TEST",
            name="Test Domain",
            responsibility_scope="Testing",
            allowed_artifact_types=["ENGINE"],
            cannot_own=[],
            priority="core",
            authority_level=5
        )
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any("authority_level must be between 1 and 4" in e for e in errors)

    def test_validate_domain_dict_with_exception(self):
        """Validate that exception during dict validation is caught"""
        bad_dict = {
            'domain_id': 'TEST',
            'name': 'Test',
            'responsibility_scope': 'Testing',
            'allowed_artifact_types': None,  # Will cause issues
            'cannot_own': [],
            'priority': 'surface'
        }
        is_valid, errors = validate_domain_dict(bad_dict)
        # Should fail validation
        assert not is_valid


# =============================================================================
# SECTION 3: Lifecycle State Machine Logic Tests
# =============================================================================

class TestLifecycleStateMachineComprehensive:
    """Tests for lifecycle state machine logic covering all edge cases"""

    def test_state_machine_missing_description_fails(self):
        """Validate that missing description is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="",
            states=["draft", "active"],
            initial_state="draft",
            transitions=[StateTransition("draft", "active", "Activate")],
            modifiable_states=["draft", "active"],
            read_only_states=[]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert "description is required" in errors

    def test_state_machine_empty_states_fails(self):
        """Validate that empty states list is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=[],
            initial_state="draft",
            transitions=[],
            modifiable_states=[],
            read_only_states=[]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert "states is required and must not be empty" in errors

    def test_state_machine_missing_initial_state_fails(self):
        """Validate that missing initial_state is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=["draft", "active"],
            initial_state="",
            transitions=[],
            modifiable_states=["draft", "active"],
            read_only_states=[]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert "initial_state is required" in errors

    def test_state_machine_none_modifiable_states_fails(self):
        """Validate that None modifiable_states is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=["draft", "active"],
            initial_state="draft",
            transitions=[],
            modifiable_states=None,
            read_only_states=[]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert "modifiable_states is required (can be empty list)" in errors

    def test_state_machine_none_read_only_states_fails(self):
        """Validate that None read_only_states is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=["draft", "active"],
            initial_state="draft",
            transitions=[],
            modifiable_states=["draft", "active"],
            read_only_states=None
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert "read_only_states is required (can be empty list)" in errors

    def test_state_machine_invalid_regenerable_states(self):
        """Validate that invalid regenerable_states are caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=["draft", "active", "deprecated"],
            initial_state="draft",
            transitions=[StateTransition("draft", "active", "Activate")],
            modifiable_states=["draft", "active"],
            read_only_states=["deprecated"],
            regenerable_states=["nonexistent"]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert any("regenerable_states contains invalid states" in e for e in errors)

    def test_state_machine_transition_invalid_from_state(self):
        """Validate that transition with invalid from_state is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=["draft", "active"],
            initial_state="draft",
            transitions=[StateTransition("nonexistent", "active", "Bad transition")],
            modifiable_states=["draft", "active"],
            read_only_states=[]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert any("from_state 'nonexistent' not in states list" in e for e in errors)

    def test_state_machine_transition_invalid_to_state(self):
        """Validate that transition with invalid to_state is caught"""
        sm = StateMachine(
            artifact_type="TEST",
            description="Test machine",
            states=["draft", "active"],
            initial_state="draft",
            transitions=[StateTransition("draft", "nonexistent", "Bad transition")],
            modifiable_states=["draft", "active"],
            read_only_states=[]
        )
        is_valid, errors = sm.validate()
        assert not is_valid
        assert any("to_state 'nonexistent' not in states list" in e for e in errors)

    def test_validate_state_machine_dict_with_exception(self):
        """Validate that exception during dict validation is caught"""
        bad_dict = {
            'description': 'Test',
            'states': ['draft'],
            'initial_state': 'draft',
            'transitions': [{'from': None, 'to': None}],  # Will cause issues
            'modifiable_states': ['draft'],
            'read_only_states': []
        }
        is_valid, errors = validate_state_machine_dict(bad_dict)
        # Should fail validation due to None states in transitions
        assert not is_valid


# =============================================================================
# SECTION 4: Artifact Registry Operations Tests
# =============================================================================

class TestArtifactRegistryOperations:
    """Tests for artifact registry operations covering uncovered paths"""

    @pytest.fixture
    def temp_registry(self, tmp_path):
        """Create a temporary registry with sample data"""
        registry_file = tmp_path / "artifact_registry.yaml"
        data = {
            'artifacts': [
                {
                    'artifact_id': 'test_engine_py',
                    'file_path': 'engines/test_engine.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'active',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-15',
                    'owner_role': 'Signal Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'secondary_domains': ['DATA'],
                    'dependencies': ['signal_framework_md'],
                    'topic': 'signal_generation',
                    'description': 'Test engine',
                    'tags': ['signal', 'engine']
                },
                {
                    'artifact_id': 'arch_doc_md',
                    'file_path': 'docs/architecture.md',
                    'primary_domain': 'ARCH',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-10',
                    'owner_role': 'System Architect',
                    'ssot_relationship': 'canonical',
                    'allowed_writers': ['ARCH'],
                    'allowed_readers': ['ALL'],
                    'topic': 'system_architecture'
                }
            ]
        }
        with open(registry_file, 'w') as f:
            yaml.dump(data, f)
        return ArtifactRegistry(registry_file)

    def test_load_nonexistent_file_raises(self, tmp_path):
        """Test that loading nonexistent file raises FileNotFoundError"""
        registry = ArtifactRegistry(tmp_path / "nonexistent.yaml")
        with pytest.raises(FileNotFoundError):
            registry.load()

    def test_load_invalid_format_raises(self, tmp_path):
        """Test that loading invalid format raises ValueError"""
        registry_file = tmp_path / "bad_registry.yaml"
        registry_file.write_text("invalid: data\n")
        registry = ArtifactRegistry(registry_file)
        with pytest.raises(ValueError, match="missing 'artifacts' key"):
            registry.load()

    def test_save_without_load_raises(self, tmp_path):
        """Test that saving without loading raises RuntimeError"""
        registry_file = tmp_path / "registry.yaml"
        registry_file.write_text("artifacts: []\n")
        registry = ArtifactRegistry(registry_file)
        with pytest.raises(RuntimeError, match="Registry not loaded"):
            registry.save()

    def test_register_duplicate_artifact_raises(self, temp_registry):
        """Test that registering duplicate artifact_id raises ValueError"""
        temp_registry.load()
        metadata = ArtifactMetadata(
            artifact_id="test_engine_py",  # Already exists
            file_path="engines/another.py",
            primary_domain="SIGNALS",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["SIGNALS"],
            allowed_readers=["ALL"]
        )
        with pytest.raises(ValueError, match="already exists"):
            temp_registry.register_artifact(metadata)

    def test_update_nonexistent_artifact_raises(self, temp_registry):
        """Test that updating nonexistent artifact raises ValueError"""
        temp_registry.load()
        metadata = ArtifactMetadata(
            artifact_id="nonexistent_id",
            file_path="test.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        with pytest.raises(ValueError, match="not found"):
            temp_registry.update_artifact("nonexistent_id", metadata)

    def test_update_mismatched_artifact_id_raises(self, temp_registry):
        """Test that updating with mismatched artifact_id raises ValueError"""
        temp_registry.load()
        metadata = ArtifactMetadata(
            artifact_id="different_id",
            file_path="engines/test_engine.py",
            primary_domain="SIGNALS",
            artifact_type="ENGINE",
            lifecycle_status="active",
            created_date="2026-01-01",
            last_modified="2026-01-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["SIGNALS"],
            allowed_readers=["ALL"]
        )
        with pytest.raises(ValueError, match="does not match"):
            temp_registry.update_artifact("test_engine_py", metadata)

    def test_list_artifacts_by_domain_with_secondary(self, temp_registry):
        """Test listing artifacts includes secondary domain matches"""
        temp_registry.load()
        # test_engine_py has secondary_domains=['DATA']
        results = temp_registry.list_artifacts_by_domain("DATA")
        assert len(results) == 1
        assert results[0].artifact_id == "test_engine_py"

    def test_list_artifacts_by_type(self, temp_registry):
        """Test listing artifacts by type"""
        temp_registry.load()
        results = temp_registry.list_artifacts_by_type("SSOT")
        assert len(results) == 1
        assert results[0].artifact_id == "arch_doc_md"

    def test_list_artifacts_by_lifecycle(self, temp_registry):
        """Test listing artifacts by lifecycle status"""
        temp_registry.load()
        results = temp_registry.list_artifacts_by_lifecycle("canonical")
        assert len(results) == 1
        assert results[0].artifact_id == "arch_doc_md"

    def test_parse_frontmatter_valid(self, tmp_path):
        """Test parsing valid YAML frontmatter"""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
artifact_id: test_md
primary_domain: ARCH
---

# Content
""")
        result = ArtifactRegistry.parse_frontmatter(md_file)
        assert result is not None
        assert result['artifact_id'] == 'test_md'
        assert result['primary_domain'] == 'ARCH'

    def test_parse_frontmatter_no_frontmatter(self, tmp_path):
        """Test parsing file without frontmatter"""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Just a heading\n\nContent here.\n")
        result = ArtifactRegistry.parse_frontmatter(md_file)
        assert result is None

    def test_parse_frontmatter_nonexistent_file(self, tmp_path):
        """Test parsing nonexistent file"""
        result = ArtifactRegistry.parse_frontmatter(tmp_path / "nonexistent.md")
        assert result is None

    def test_parse_frontmatter_unclosed(self, tmp_path):
        """Test parsing file with unclosed frontmatter"""
        md_file = tmp_path / "test.md"
        md_file.write_text("---\nartifact_id: test\nno closing delimiter\n")
        result = ArtifactRegistry.parse_frontmatter(md_file)
        assert result is None

    def test_parse_frontmatter_invalid_yaml(self, tmp_path):
        """Test parsing file with invalid YAML in frontmatter"""
        md_file = tmp_path / "test.md"
        md_file.write_text("---\n: invalid: yaml: [unclosed\n---\n")
        result = ArtifactRegistry.parse_frontmatter(md_file)
        assert result is None

    def test_save_and_reload(self, temp_registry, tmp_path):
        """Test saving and reloading preserves data"""
        temp_registry.load()
        
        # Register new artifact
        metadata = ArtifactMetadata(
            artifact_id="new_artifact",
            file_path="new_file.py",
            primary_domain="ARCH",
            artifact_type="ENGINE",
            lifecycle_status="planned",
            created_date="2026-02-01",
            last_modified="2026-02-01",
            owner_role="Engineer",
            ssot_relationship="implementation",
            allowed_writers=["ARCH"],
            allowed_readers=["ALL"]
        )
        temp_registry.register_artifact(metadata)
        temp_registry.save()
        
        # Reload and verify
        temp_registry._loaded = False
        temp_registry.load()
        artifact = temp_registry.get_artifact("new_artifact")
        assert artifact is not None
        assert artifact.file_path == "new_file.py"

    def test_get_artifact_auto_loads(self, temp_registry):
        """Test that get_artifact auto-loads if not loaded"""
        # Don't call load() explicitly
        artifact = temp_registry.get_artifact("test_engine_py")
        assert artifact is not None
        assert artifact.primary_domain == "SIGNALS"


# =============================================================================
# SECTION 5: Domain Registry Operations Tests
# =============================================================================

class TestDomainRegistryOperations:
    """Tests for domain registry operations covering uncovered paths"""

    @pytest.fixture
    def temp_domain_registry(self, tmp_path):
        """Create a temporary domain registry"""
        registry_file = tmp_path / "domain_registry.yaml"
        data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Raw signal generation',
                    'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT'],
                    'cannot_own': ['DASHBOARD', 'REPORT_OUT'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'SEMANTICS',
                    'name': 'Semantic Interpretation',
                    'responsibility_scope': 'Semantic state creation',
                    'allowed_artifact_types': ['ENGINE', 'SSOT'],
                    'cannot_own': ['DASHBOARD', 'DATA_IN'],
                    'priority': 'core',
                    'authority_level': 2
                },
                {
                    'domain_id': 'REASONING',
                    'name': 'Reasoning Logic',
                    'responsibility_scope': 'Reasoning conclusions',
                    'allowed_artifact_types': ['ENGINE', 'SSOT'],
                    'cannot_own': ['DASHBOARD', 'DATA_IN'],
                    'priority': 'core',
                    'authority_level': 3
                },
                {
                    'domain_id': 'REPORT',
                    'name': 'Report Generation',
                    'responsibility_scope': 'Human-readable reports',
                    'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT'],
                    'cannot_own': ['DATA_IN'],
                    'priority': 'core',
                    'authority_level': 4
                },
                {
                    'domain_id': 'USER',
                    'name': 'User Interface',
                    'responsibility_scope': 'Dashboard and UI',
                    'allowed_artifact_types': ['DASHBOARD', 'CONFIG', 'SSOT'],
                    'cannot_own': ['ENGINE'],
                    'priority': 'surface'
                },
                {
                    'domain_id': 'DATA',
                    'name': 'Data Management',
                    'responsibility_scope': 'Data normalization',
                    'allowed_artifact_types': ['ENGINE', 'DATA_IN', 'DATA_OUT', 'SSOT'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'surface'
                }
            ]
        }
        with open(registry_file, 'w') as f:
            yaml.dump(data, f)
        return DomainRegistry(registry_file)

    def test_load_nonexistent_file_raises(self, tmp_path):
        """Test that loading nonexistent file raises FileNotFoundError"""
        registry = DomainRegistry(tmp_path / "nonexistent.yaml")
        with pytest.raises(FileNotFoundError):
            registry.load()

    def test_load_invalid_format_raises(self, tmp_path):
        """Test that loading invalid format raises ValueError"""
        registry_file = tmp_path / "bad_registry.yaml"
        registry_file.write_text("invalid: data\n")
        registry = DomainRegistry(registry_file)
        with pytest.raises(ValueError, match="missing 'domains' key"):
            registry.load()

    def test_load_invalid_domain_raises(self, tmp_path):
        """Test that loading invalid domain definition raises ValueError"""
        registry_file = tmp_path / "bad_domain.yaml"
        data = {
            'domains': [
                {
                    'domain_id': 'BAD',
                    'name': 'Bad Domain',
                    'responsibility_scope': 'Testing',
                    'allowed_artifact_types': ['ENGINE'],
                    'cannot_own': [],
                    'priority': 'invalid_priority'  # Invalid
                }
            ]
        }
        with open(registry_file, 'w') as f:
            yaml.dump(data, f)
        registry = DomainRegistry(registry_file)
        with pytest.raises(ValueError, match="Invalid domain"):
            registry.load()

    def test_get_domain_auto_loads(self, temp_domain_registry):
        """Test that get_domain auto-loads if not loaded"""
        domain = temp_domain_registry.get_domain("SIGNALS")
        assert domain is not None
        assert domain.name == "Signal Generation"

    def test_get_nonexistent_domain(self, temp_domain_registry):
        """Test getting nonexistent domain returns None"""
        temp_domain_registry.load()
        domain = temp_domain_registry.get_domain("NONEXISTENT")
        assert domain is None

    def test_list_domains(self, temp_domain_registry):
        """Test listing all domains"""
        temp_domain_registry.load()
        domains = temp_domain_registry.list_domains()
        assert len(domains) == 6

    def test_list_core_domains(self, temp_domain_registry):
        """Test listing core domains"""
        temp_domain_registry.load()
        core = temp_domain_registry.list_core_domains()
        assert len(core) == 4
        domain_ids = [d.domain_id for d in core]
        assert "SIGNALS" in domain_ids
        assert "SEMANTICS" in domain_ids
        assert "REASONING" in domain_ids
        assert "REPORT" in domain_ids

    def test_list_surface_domains(self, temp_domain_registry):
        """Test listing surface domains"""
        temp_domain_registry.load()
        surface = temp_domain_registry.list_surface_domains()
        assert len(surface) == 2
        domain_ids = [d.domain_id for d in surface]
        assert "USER" in domain_ids
        assert "DATA" in domain_ids

    def test_validate_domain_assignment_valid(self, temp_domain_registry):
        """Test valid domain assignment"""
        temp_domain_registry.load()
        is_valid, error = temp_domain_registry.validate_domain_assignment("ENGINE", "SIGNALS")
        assert is_valid
        assert error is None

    def test_validate_domain_assignment_invalid_domain(self, temp_domain_registry):
        """Test domain assignment with nonexistent domain"""
        temp_domain_registry.load()
        is_valid, error = temp_domain_registry.validate_domain_assignment("ENGINE", "NONEXISTENT")
        assert not is_valid
        assert "does not exist" in error

    def test_validate_domain_assignment_cannot_own(self, temp_domain_registry):
        """Test domain assignment where domain cannot own type"""
        temp_domain_registry.load()
        is_valid, error = temp_domain_registry.validate_domain_assignment("DASHBOARD", "SIGNALS")
        assert not is_valid
        assert "cannot own artifact type" in error

    def test_get_valid_domains_for_type(self, temp_domain_registry):
        """Test getting valid domains for an artifact type"""
        temp_domain_registry.load()
        valid = temp_domain_registry.get_valid_domains_for_type("DASHBOARD")
        assert "USER" in valid
        assert "SIGNALS" not in valid

    def test_get_core_reasoning_chain(self, temp_domain_registry):
        """Test getting core reasoning chain in authority order"""
        temp_domain_registry.load()
        chain = temp_domain_registry.get_core_reasoning_chain()
        assert len(chain) == 4
        assert chain[0].domain_id == "SIGNALS"
        assert chain[1].domain_id == "SEMANTICS"
        assert chain[2].domain_id == "REASONING"
        assert chain[3].domain_id == "REPORT"


# =============================================================================
# SECTION 6: Lifecycle Manager Operations Tests
# =============================================================================

class TestLifecycleManagerOperations:
    """Tests for lifecycle manager operations covering uncovered paths"""

    @pytest.fixture
    def temp_lifecycle_manager(self, tmp_path):
        """Create a temporary lifecycle manager"""
        sm_file = tmp_path / "lifecycle_state_machine.yaml"
        data = {
            'artifact_types': {
                'SSOT': {
                    'description': 'Single Source of Truth documents',
                    'states': ['draft', 'review', 'canonical', 'deprecated'],
                    'initial_state': 'draft',
                    'transitions': [
                        {'from': 'draft', 'to': 'review', 'condition': 'Author completes'},
                        {'from': 'review', 'to': 'canonical', 'condition': 'Owner approves'},
                        {'from': 'canonical', 'to': 'draft', 'condition': 'Revision required'},
                        {'from': 'canonical', 'to': 'deprecated', 'condition': 'Superseded'}
                    ],
                    'modifiable_states': ['draft', 'review', 'canonical'],
                    'read_only_states': ['deprecated']
                },
                'ENGINE': {
                    'description': 'Processing engines',
                    'states': ['planned', 'development', 'active', 'deprecated'],
                    'initial_state': 'planned',
                    'transitions': [
                        {'from': 'planned', 'to': 'development', 'condition': 'Implementation begins'},
                        {'from': 'development', 'to': 'active', 'condition': 'Production ready'},
                        {'from': 'development', 'to': 'development', 'condition': 'Iteration'},
                        {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                    ],
                    'modifiable_states': ['planned', 'development', 'active'],
                    'read_only_states': ['deprecated']
                }
            }
        }
        with open(sm_file, 'w') as f:
            yaml.dump(data, f)
        return LifecycleManager(sm_file)

    def test_load_nonexistent_file_raises(self, tmp_path):
        """Test that loading nonexistent file raises FileNotFoundError"""
        manager = LifecycleManager(tmp_path / "nonexistent.yaml")
        with pytest.raises(FileNotFoundError):
            manager.load()

    def test_load_invalid_format_raises(self, tmp_path):
        """Test that loading invalid format raises ValueError"""
        sm_file = tmp_path / "bad_sm.yaml"
        sm_file.write_text("invalid: data\n")
        manager = LifecycleManager(sm_file)
        with pytest.raises(ValueError, match="missing 'artifact_types' key"):
            manager.load()

    def test_get_state_machine_auto_loads(self, temp_lifecycle_manager):
        """Test that get_state_machine auto-loads if not loaded"""
        sm = temp_lifecycle_manager.get_state_machine("SSOT")
        assert sm is not None
        assert sm.artifact_type == "SSOT"

    def test_get_nonexistent_state_machine(self, temp_lifecycle_manager):
        """Test getting nonexistent state machine returns None"""
        temp_lifecycle_manager.load()
        sm = temp_lifecycle_manager.get_state_machine("NONEXISTENT")
        assert sm is None

    def test_validate_transition_valid(self, temp_lifecycle_manager):
        """Test valid transition"""
        temp_lifecycle_manager.load()
        is_valid, error = temp_lifecycle_manager.validate_transition("SSOT", "draft", "review")
        assert is_valid
        assert error is None

    def test_validate_transition_invalid(self, temp_lifecycle_manager):
        """Test invalid transition"""
        temp_lifecycle_manager.load()
        is_valid, error = temp_lifecycle_manager.validate_transition("SSOT", "draft", "deprecated")
        assert not is_valid
        assert "Invalid transition" in error

    def test_validate_transition_no_state_machine(self, temp_lifecycle_manager):
        """Test transition validation for nonexistent artifact type"""
        temp_lifecycle_manager.load()
        is_valid, error = temp_lifecycle_manager.validate_transition("NONEXISTENT", "draft", "active")
        assert not is_valid
        assert "No state machine defined" in error

    def test_validate_transition_no_valid_transitions_from_state(self, temp_lifecycle_manager):
        """Test transition from state with no outgoing transitions"""
        temp_lifecycle_manager.load()
        is_valid, error = temp_lifecycle_manager.validate_transition("SSOT", "deprecated", "draft")
        assert not is_valid
        assert "No valid transitions" in error

    def test_get_allowed_transitions(self, temp_lifecycle_manager):
        """Test getting allowed transitions"""
        temp_lifecycle_manager.load()
        transitions = temp_lifecycle_manager.get_allowed_transitions("SSOT", "canonical")
        assert "draft" in transitions
        assert "deprecated" in transitions

    def test_get_allowed_transitions_no_state_machine(self, temp_lifecycle_manager):
        """Test getting transitions for nonexistent type returns empty"""
        temp_lifecycle_manager.load()
        transitions = temp_lifecycle_manager.get_allowed_transitions("NONEXISTENT", "draft")
        assert transitions == []

    def test_is_modifiable_active(self, temp_lifecycle_manager):
        """Test modifiable check for active state"""
        temp_lifecycle_manager.load()
        assert temp_lifecycle_manager.is_modifiable("ENGINE", "active")

    def test_is_modifiable_deprecated(self, temp_lifecycle_manager):
        """Test modifiable check for deprecated state"""
        temp_lifecycle_manager.load()
        assert not temp_lifecycle_manager.is_modifiable("ENGINE", "deprecated")

    def test_is_modifiable_no_state_machine(self, temp_lifecycle_manager):
        """Test modifiable check for nonexistent type returns True"""
        temp_lifecycle_manager.load()
        assert temp_lifecycle_manager.is_modifiable("NONEXISTENT", "any_state")

    def test_get_initial_state(self, temp_lifecycle_manager):
        """Test getting initial state"""
        temp_lifecycle_manager.load()
        assert temp_lifecycle_manager.get_initial_state("SSOT") == "draft"
        assert temp_lifecycle_manager.get_initial_state("ENGINE") == "planned"

    def test_get_initial_state_no_state_machine(self, temp_lifecycle_manager):
        """Test getting initial state for nonexistent type returns None"""
        temp_lifecycle_manager.load()
        assert temp_lifecycle_manager.get_initial_state("NONEXISTENT") is None

    def test_list_artifact_types(self, temp_lifecycle_manager):
        """Test listing all artifact types"""
        temp_lifecycle_manager.load()
        types = temp_lifecycle_manager.list_artifact_types()
        assert "SSOT" in types
        assert "ENGINE" in types

    def test_list_states(self, temp_lifecycle_manager):
        """Test listing states for artifact type"""
        temp_lifecycle_manager.load()
        states = temp_lifecycle_manager.list_states("SSOT")
        assert states == ['draft', 'review', 'canonical', 'deprecated']

    def test_list_states_no_state_machine(self, temp_lifecycle_manager):
        """Test listing states for nonexistent type returns empty"""
        temp_lifecycle_manager.load()
        states = temp_lifecycle_manager.list_states("NONEXISTENT")
        assert states == []


# =============================================================================
# SECTION 7: Violation Detector Tests (covering uncovered paths)
# =============================================================================

class TestViolationDetectorComprehensive:
    """Tests for violation detector covering uncovered code paths"""

    @pytest.fixture
    def temp_repo_with_registries(self, tmp_path):
        """Create a temporary repo with registries for violation detection"""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        
        # Create .domainization directory
        domainization_dir = repo_root / ".domainization"
        domainization_dir.mkdir()
        
        # Create artifact registry
        artifact_data = {
            'artifacts': [
                {
                    'artifact_id': 'active_engine',
                    'file_path': 'engines/active_engine.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'active',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-15',
                    'owner_role': 'Signal Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'dependencies': ['signal_spec_md']
                },
                {
                    'artifact_id': 'signal_spec_md',
                    'file_path': 'docs/signal_spec.md',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'canonical',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'topic': 'signal_generation'
                },
                {
                    'artifact_id': 'derived_doc',
                    'file_path': 'docs/derived.md',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'derived',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'dependencies': ['signal_spec_md']
                },
                {
                    'artifact_id': 'orphan_derived',
                    'file_path': 'docs/orphan.md',
                    'primary_domain': 'ARCH',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'draft',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'derived',
                    'allowed_writers': ['ARCH'],
                    'allowed_readers': ['ALL'],
                    'dependencies': []
                },
                {
                    'artifact_id': 'derived_no_canonical_ref',
                    'file_path': 'docs/derived_bad.md',
                    'primary_domain': 'ARCH',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'draft',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'derived',
                    'allowed_writers': ['ARCH'],
                    'allowed_readers': ['ALL'],
                    'dependencies': ['active_engine']  # Not a canonical SSOT
                },
                {
                    'artifact_id': 'impl_no_deps',
                    'file_path': 'engines/impl.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'active',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'dependencies': []
                },
                {
                    'artifact_id': 'impl_no_ssot_ref',
                    'file_path': 'engines/impl2.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'active',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'dependencies': ['active_engine']  # Not an SSOT
                },
                {
                    'artifact_id': 'deprecated_engine',
                    'file_path': 'engines/deprecated.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'deprecated',
                    'created_date': '2025-01-01',
                    'last_modified': '2025-06-01',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL']
                },
                {
                    'artifact_id': 'missing_lifecycle',
                    'file_path': 'engines/no_lifecycle.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': '',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL']
                },
                {
                    'artifact_id': 'invalid_lifecycle',
                    'file_path': 'engines/bad_lifecycle.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'nonexistent_state',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL']
                }
            ]
        }
        artifact_file = domainization_dir / "artifact_registry.yaml"
        with open(artifact_file, 'w') as f:
            yaml.dump(artifact_data, f)
        
        # Create domain registry
        domain_data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Raw signals',
                    'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'ARCH',
                    'name': 'Architecture',
                    'responsibility_scope': 'System architecture',
                    'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'surface'
                }
            ]
        }
        domain_file = domainization_dir / "domain_registry.yaml"
        with open(domain_file, 'w') as f:
            yaml.dump(domain_data, f)
        
        # Create lifecycle state machine
        lifecycle_data = {
            'artifact_types': {
                'ENGINE': {
                    'description': 'Processing engines',
                    'states': ['planned', 'development', 'active', 'deprecated'],
                    'initial_state': 'planned',
                    'transitions': [
                        {'from': 'planned', 'to': 'development', 'condition': 'Start'},
                        {'from': 'development', 'to': 'active', 'condition': 'Ready'},
                        {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                    ],
                    'modifiable_states': ['planned', 'development', 'active'],
                    'read_only_states': ['deprecated']
                },
                'SSOT': {
                    'description': 'Source of truth',
                    'states': ['draft', 'review', 'canonical', 'deprecated'],
                    'initial_state': 'draft',
                    'transitions': [
                        {'from': 'draft', 'to': 'review', 'condition': 'Complete'},
                        {'from': 'review', 'to': 'canonical', 'condition': 'Approved'},
                        {'from': 'canonical', 'to': 'deprecated', 'condition': 'Superseded'}
                    ],
                    'modifiable_states': ['draft', 'review', 'canonical'],
                    'read_only_states': ['deprecated']
                }
            }
        }
        lifecycle_file = domainization_dir / "lifecycle_state_machine.yaml"
        with open(lifecycle_file, 'w') as f:
            yaml.dump(lifecycle_data, f)
        
        # Create actual files for deprecated modification detection
        engines_dir = repo_root / "engines"
        engines_dir.mkdir()
        deprecated_file = engines_dir / "deprecated.py"
        deprecated_file.write_text("# Deprecated engine\n")
        
        # Create docs directory with unregistered file
        docs_dir = repo_root / "docs"
        docs_dir.mkdir()
        (docs_dir / "unregistered.md").write_text("# Unregistered\n")
        
        return repo_root

    def test_detect_ssot_conflicts_derived_without_deps(self, temp_repo_with_registries):
        """Test detection of derived documents without dependencies"""
        repo_root = temp_repo_with_registries
        domainization_dir = repo_root / ".domainization"
        
        artifact_registry = ArtifactRegistry(domainization_dir / "artifact_registry.yaml")
        domain_registry = DomainRegistry(domainization_dir / "domain_registry.yaml")
        lifecycle_manager = LifecycleManager(domainization_dir / "lifecycle_state_machine.yaml")
        
        detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=repo_root
        )
        
        artifact_registry.load()
        violations = detector.detect_ssot_conflicts()
        
        # Should detect orphan_derived (empty deps) and derived_no_canonical_ref
        ssot_ref_violations = [v for v in violations if v.violation_type == 'missing_ssot_reference']
        assert len(ssot_ref_violations) >= 2

    def test_detect_ssot_conflicts_implementation_without_ssot_ref(self, temp_repo_with_registries):
        """Test detection of implementation artifacts without SSOT reference"""
        repo_root = temp_repo_with_registries
        domainization_dir = repo_root / ".domainization"
        
        artifact_registry = ArtifactRegistry(domainization_dir / "artifact_registry.yaml")
        domain_registry = DomainRegistry(domainization_dir / "domain_registry.yaml")
        lifecycle_manager = LifecycleManager(domainization_dir / "lifecycle_state_machine.yaml")
        
        detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=repo_root
        )
        
        artifact_registry.load()
        violations = detector.detect_ssot_conflicts()
        
        # Should detect impl_no_deps and impl_no_ssot_ref
        impl_violations = [v for v in violations 
                          if v.violation_type == 'missing_ssot_reference' 
                          and v.artifact_id in ('impl_no_deps', 'impl_no_ssot_ref')]
        assert len(impl_violations) >= 2

    def test_detect_missing_lifecycle_status(self, temp_repo_with_registries):
        """Test detection of missing lifecycle status"""
        repo_root = temp_repo_with_registries
        domainization_dir = repo_root / ".domainization"
        
        artifact_registry = ArtifactRegistry(domainization_dir / "artifact_registry.yaml")
        domain_registry = DomainRegistry(domainization_dir / "domain_registry.yaml")
        lifecycle_manager = LifecycleManager(domainization_dir / "lifecycle_state_machine.yaml")
        
        detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=repo_root
        )
        
        artifact_registry.load()
        lifecycle_manager.load()
        violations = detector.detect_missing_lifecycle_status()
        
        # Should detect missing_lifecycle and invalid_lifecycle
        assert len(violations) >= 2
        violation_ids = [v.artifact_id for v in violations]
        assert 'missing_lifecycle' in violation_ids

    def test_detect_invalid_lifecycle_status(self, temp_repo_with_registries):
        """Test detection of invalid lifecycle status"""
        repo_root = temp_repo_with_registries
        domainization_dir = repo_root / ".domainization"
        
        artifact_registry = ArtifactRegistry(domainization_dir / "artifact_registry.yaml")
        domain_registry = DomainRegistry(domainization_dir / "domain_registry.yaml")
        lifecycle_manager = LifecycleManager(domainization_dir / "lifecycle_state_machine.yaml")
        
        detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=repo_root
        )
        
        artifact_registry.load()
        lifecycle_manager.load()
        violations = detector.detect_missing_lifecycle_status()
        
        # Should detect invalid_lifecycle
        invalid_violations = [v for v in violations if v.violation_type == 'invalid_lifecycle']
        assert len(invalid_violations) >= 1

    def test_detect_deprecated_modifications(self, temp_repo_with_registries):
        """Test detection of deprecated artifact modifications"""
        repo_root = temp_repo_with_registries
        domainization_dir = repo_root / ".domainization"
        
        # Touch the deprecated file to make it recently modified
        deprecated_file = repo_root / "engines" / "deprecated.py"
        deprecated_file.write_text("# Modified deprecated engine\n")
        
        artifact_registry = ArtifactRegistry(domainization_dir / "artifact_registry.yaml")
        domain_registry = DomainRegistry(domainization_dir / "domain_registry.yaml")
        lifecycle_manager = LifecycleManager(domainization_dir / "lifecycle_state_machine.yaml")
        
        detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=repo_root
        )
        
        artifact_registry.load()
        violations = detector.detect_deprecated_modifications()
        
        # Should detect the recently modified deprecated file
        assert len(violations) >= 1
        assert violations[0].violation_type == 'deprecated_modification'

    def test_detect_unregistered_artifacts(self, temp_repo_with_registries):
        """Test detection of unregistered artifacts"""
        repo_root = temp_repo_with_registries
        domainization_dir = repo_root / ".domainization"
        
        artifact_registry = ArtifactRegistry(domainization_dir / "artifact_registry.yaml")
        domain_registry = DomainRegistry(domainization_dir / "domain_registry.yaml")
        lifecycle_manager = LifecycleManager(domainization_dir / "lifecycle_state_machine.yaml")
        
        detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=repo_root
        )
        
        artifact_registry.load()
        violations = detector.detect_unregistered_artifacts()
        
        # Should detect docs/unregistered.md
        unregistered = [v for v in violations if 'unregistered' in v.file_path]
        assert len(unregistered) >= 1

    def test_violation_str_representation(self):
        """Test Violation string representation"""
        violation = Violation(
            artifact_id="test_id",
            file_path="test.py",
            violation_type="test_violation",
            severity="high",
            description="Test violation description",
            recommendation="Fix it"
        )
        text = str(violation)
        assert "test_id" in text
        assert "Test violation description" in text
        assert "Fix it" in text

    def test_violation_to_dict(self):
        """Test Violation to_dict conversion"""
        violation = Violation(
            artifact_id="test_id",
            file_path="test.py",
            violation_type="test_violation",
            severity="critical",
            description="Critical issue",
            recommendation="Fix immediately"
        )
        d = violation.to_dict()
        assert d['artifact_id'] == "test_id"
        assert d['severity'] == "critical"
        assert d['violation_type'] == "test_violation"


# =============================================================================
# SECTION 8: Health Reporter Tests (covering additional paths)
# =============================================================================

class TestHealthReporterComprehensive:
    """Tests for health reporter covering additional code paths"""

    @pytest.fixture
    def health_reporter_setup(self, tmp_path):
        """Create health reporter with test data"""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        reports_dir = domainization_dir / "reports"
        reports_dir.mkdir()
        
        # Create artifact registry
        artifact_data = {
            'artifacts': [
                {
                    'artifact_id': 'engine_1',
                    'file_path': 'engines/engine1.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'active',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-15',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'dependencies': ['spec_1']
                },
                {
                    'artifact_id': 'spec_1',
                    'file_path': 'docs/spec.md',
                    'primary_domain': 'ARCH',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'canonical',
                    'allowed_writers': ['ARCH'],
                    'allowed_readers': ['ALL'],
                    'topic': 'architecture'
                },
                {
                    'artifact_id': 'report_1',
                    'file_path': 'reports/report.txt',
                    'primary_domain': 'REPORT',
                    'artifact_type': 'REPORT_OUT',
                    'lifecycle_status': 'current',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-20',
                    'owner_role': 'Report Engine',
                    'ssot_relationship': 'none',
                    'allowed_writers': ['REPORT'],
                    'allowed_readers': ['ALL']
                }
            ]
        }
        artifact_file = domainization_dir / "artifact_registry.yaml"
        with open(artifact_file, 'w') as f:
            yaml.dump(artifact_data, f)
        
        # Create domain registry
        domain_data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Raw signals',
                    'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'ARCH',
                    'name': 'Architecture',
                    'responsibility_scope': 'System architecture',
                    'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'surface'
                },
                {
                    'domain_id': 'REPORT',
                    'name': 'Report Generation',
                    'responsibility_scope': 'Reports',
                    'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT'],
                    'cannot_own': ['DATA_IN'],
                    'priority': 'core',
                    'authority_level': 4
                }
            ]
        }
        domain_file = domainization_dir / "domain_registry.yaml"
        with open(domain_file, 'w') as f:
            yaml.dump(domain_data, f)
        
        # Create lifecycle state machine
        lifecycle_data = {
            'artifact_types': {
                'ENGINE': {
                    'description': 'Processing engines',
                    'states': ['planned', 'development', 'active', 'deprecated'],
                    'initial_state': 'planned',
                    'transitions': [
                        {'from': 'planned', 'to': 'development', 'condition': 'Start'},
                        {'from': 'development', 'to': 'active', 'condition': 'Ready'},
                        {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                    ],
                    'modifiable_states': ['planned', 'development', 'active'],
                    'read_only_states': ['deprecated']
                },
                'SSOT': {
                    'description': 'Source of truth',
                    'states': ['draft', 'review', 'canonical', 'deprecated'],
                    'initial_state': 'draft',
                    'transitions': [
                        {'from': 'draft', 'to': 'review', 'condition': 'Complete'},
                        {'from': 'review', 'to': 'canonical', 'condition': 'Approved'}
                    ],
                    'modifiable_states': ['draft', 'review', 'canonical'],
                    'read_only_states': ['deprecated']
                },
                'REPORT_OUT': {
                    'description': 'Report outputs',
                    'states': ['generated', 'current', 'archived'],
                    'initial_state': 'generated',
                    'transitions': [
                        {'from': 'generated', 'to': 'current', 'condition': 'Latest'},
                        {'from': 'current', 'to': 'archived', 'condition': 'Superseded'}
                    ],
                    'modifiable_states': ['generated', 'current'],
                    'read_only_states': ['archived']
                }
            }
        }
        lifecycle_file = domainization_dir / "lifecycle_state_machine.yaml"
        with open(lifecycle_file, 'w') as f:
            yaml.dump(lifecycle_data, f)
        
        artifact_registry = ArtifactRegistry(artifact_file)
        domain_registry = DomainRegistry(domain_file)
        lifecycle_manager = LifecycleManager(lifecycle_file)
        
        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path
        )
        
        return reporter, reports_dir

    def test_generate_health_report_structure(self, health_reporter_setup):
        """Test that health report has correct structure"""
        reporter, _ = health_reporter_setup
        report = reporter.generate_health_report(include_violations=False)
        
        assert 'report_date' in report
        assert 'summary' in report
        assert 'domain_coverage' in report
        assert 'lifecycle_distribution' in report
        assert report['summary']['total_artifacts'] == 3

    def test_get_domain_coverage(self, health_reporter_setup):
        """Test domain coverage calculation"""
        reporter, _ = health_reporter_setup
        coverage = reporter.get_domain_coverage()
        
        # Should have entries for SIGNALS, ARCH, REPORT
        domain_ids = [c['domain_id'] for c in coverage]
        assert 'SIGNALS' in domain_ids
        assert 'ARCH' in domain_ids
        assert 'REPORT' in domain_ids

    def test_get_lifecycle_distribution(self, health_reporter_setup):
        """Test lifecycle distribution calculation"""
        reporter, _ = health_reporter_setup
        distribution = reporter.get_lifecycle_distribution()
        
        # Should have entries for ENGINE, SSOT, REPORT_OUT
        types = [d['artifact_type'] for d in distribution]
        assert 'ENGINE' in types

    def test_save_report(self, health_reporter_setup):
        """Test saving report to file"""
        reporter, reports_dir = health_reporter_setup
        report = reporter.generate_health_report(include_violations=False)
        
        output_path = reports_dir / "test_health_report.yaml"
        saved_path = reporter.save_report(report, output_path=output_path)
        assert saved_path.exists()
        
        # Verify content
        with open(saved_path, 'r') as f:
            saved_data = yaml.safe_load(f)
        assert saved_data['summary']['total_artifacts'] == 3

    def test_format_report_text(self, health_reporter_setup):
        """Test formatting report as text"""
        reporter, _ = health_reporter_setup
        report = reporter.generate_health_report(include_violations=False)
        text = reporter.format_report_text(report)
        
        assert "Health Report" in text or "health" in text.lower()
        assert "3" in text  # total artifacts


# =============================================================================
# SECTION 9: Registry Cache Tests (covering additional paths)
# =============================================================================

class TestRegistryCacheComprehensive:
    """Tests for registry cache covering additional code paths"""

    @pytest.fixture
    def cache_setup(self, tmp_path):
        """Create registry cache with test data"""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        
        # Create artifact registry
        artifact_data = {
            'artifacts': [
                {
                    'artifact_id': 'cached_engine',
                    'file_path': 'engines/cached.py',
                    'primary_domain': 'SIGNALS',
                    'artifact_type': 'ENGINE',
                    'lifecycle_status': 'active',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-15',
                    'owner_role': 'Engineer',
                    'ssot_relationship': 'implementation',
                    'allowed_writers': ['SIGNALS'],
                    'allowed_readers': ['ALL'],
                    'topic': 'caching'
                },
                {
                    'artifact_id': 'cached_doc',
                    'file_path': 'docs/cached.md',
                    'primary_domain': 'ARCH',
                    'artifact_type': 'SSOT',
                    'lifecycle_status': 'canonical',
                    'created_date': '2026-01-01',
                    'last_modified': '2026-01-01',
                    'owner_role': 'Architect',
                    'ssot_relationship': 'canonical',
                    'allowed_writers': ['ARCH'],
                    'allowed_readers': ['ALL'],
                    'topic': 'architecture'
                }
            ]
        }
        artifact_file = domainization_dir / "artifact_registry.yaml"
        with open(artifact_file, 'w') as f:
            yaml.dump(artifact_data, f)
        
        # Create domain registry
        domain_data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Raw signals',
                    'allowed_artifact_types': ['ENGINE', 'DATA_OUT', 'SSOT'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'ARCH',
                    'name': 'Architecture',
                    'responsibility_scope': 'System architecture',
                    'allowed_artifact_types': ['SSOT', 'ENGINE'],
                    'cannot_own': ['DASHBOARD'],
                    'priority': 'surface'
                }
            ]
        }
        domain_file = domainization_dir / "domain_registry.yaml"
        with open(domain_file, 'w') as f:
            yaml.dump(domain_data, f)
        
        # Create lifecycle state machine
        lifecycle_data = {
            'artifact_types': {
                'ENGINE': {
                    'description': 'Processing engines',
                    'states': ['planned', 'development', 'active', 'deprecated'],
                    'initial_state': 'planned',
                    'transitions': [
                        {'from': 'planned', 'to': 'development', 'condition': 'Start'},
                        {'from': 'development', 'to': 'active', 'condition': 'Ready'}
                    ],
                    'modifiable_states': ['planned', 'development', 'active'],
                    'read_only_states': ['deprecated']
                },
                'SSOT': {
                    'description': 'Source of truth',
                    'states': ['draft', 'review', 'canonical', 'deprecated'],
                    'initial_state': 'draft',
                    'transitions': [
                        {'from': 'draft', 'to': 'review', 'condition': 'Complete'}
                    ],
                    'modifiable_states': ['draft', 'review', 'canonical'],
                    'read_only_states': ['deprecated']
                }
            }
        }
        lifecycle_file = domainization_dir / "lifecycle_state_machine.yaml"
        with open(lifecycle_file, 'w') as f:
            yaml.dump(lifecycle_data, f)
        
        artifact_registry = ArtifactRegistry(artifact_file)
        domain_registry = DomainRegistry(domain_file)
        lifecycle_manager = LifecycleManager(lifecycle_file)
        
        cache = RegistryCache(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager
        )
        cache.load()
        
        return cache, artifact_file

    def test_cache_get_artifact(self, cache_setup):
        """Test getting artifact from cache"""
        cache, _ = cache_setup
        artifact = cache.get_artifact("cached_engine")
        assert artifact is not None
        assert artifact.primary_domain == "SIGNALS"

    def test_cache_get_nonexistent_artifact(self, cache_setup):
        """Test getting nonexistent artifact from cache"""
        cache, _ = cache_setup
        artifact = cache.get_artifact("nonexistent")
        assert artifact is None

    def test_cache_list_by_domain(self, cache_setup):
        """Test listing artifacts by domain from cache"""
        cache, _ = cache_setup
        results = cache.list_artifacts_by_domain("SIGNALS")
        assert len(results) == 1
        assert results[0].artifact_id == "cached_engine"

    def test_cache_list_by_type(self, cache_setup):
        """Test listing artifacts by type from cache"""
        cache, _ = cache_setup
        results = cache.list_artifacts_by_type("SSOT")
        assert len(results) == 1
        assert results[0].artifact_id == "cached_doc"

    def test_cache_list_by_lifecycle(self, cache_setup):
        """Test listing artifacts by lifecycle from cache"""
        cache, _ = cache_setup
        results = cache.list_artifacts_by_lifecycle("active")
        assert len(results) == 1

    def test_cache_list_by_topic(self, cache_setup):
        """Test listing artifacts by topic from cache"""
        cache, _ = cache_setup
        results = cache.list_artifacts_by_topic("caching")
        assert len(results) == 1
        assert results[0].artifact_id == "cached_engine"

    def test_cache_invalidation(self, cache_setup):
        """Test cache invalidation"""
        cache, _ = cache_setup
        cache.invalidate()
        # After invalidation, cache should reload on next access
        stats = cache.get_statistics()
        assert stats['total_artifacts'] == 2

    def test_cache_get_domain(self, cache_setup):
        """Test getting domain from cache"""
        cache, _ = cache_setup
        domain = cache.get_domain("SIGNALS")
        assert domain is not None
        assert domain.name == "Signal Generation"

    def test_cache_list_domains(self, cache_setup):
        """Test listing domains from cache"""
        cache, _ = cache_setup
        domains = cache.list_domains()
        assert len(domains) == 2

    def test_cache_get_state_machine(self, cache_setup):
        """Test getting state machine from cache"""
        cache, _ = cache_setup
        sm = cache.get_state_machine("ENGINE")
        assert sm is not None
        assert "active" in sm.states

    def test_cache_validate_transition(self, cache_setup):
        """Test validating transition through cache"""
        cache, _ = cache_setup
        result = cache.validate_transition("ENGINE", "planned", "development")
        # validate_transition returns (is_valid, error_message) tuple
        is_valid, error_msg = result
        assert is_valid
        assert error_msg is None

    def test_cache_validate_invalid_transition(self, cache_setup):
        """Test validating invalid transition through cache"""
        cache, _ = cache_setup
        result = cache.validate_transition("ENGINE", "planned", "deprecated")
        # validate_transition returns (is_valid, error_message) tuple
        is_valid, error_msg = result
        assert not is_valid
        assert error_msg is not None

    def test_cache_statistics(self, cache_setup):
        """Test cache statistics"""
        cache, _ = cache_setup
        stats = cache.get_statistics()
        assert stats['total_artifacts'] == 2
        assert 'domains' in stats
        assert stats['domains'] >= 2


# =============================================================================
# SECTION 10: Validation Result and Warning Tests
# =============================================================================

class TestValidationResultAndWarnings:
    """Tests for validation result and warning classes"""

    def test_validation_warning_str(self):
        """Test ValidationWarning string representation"""
        warning = ValidationWarning(
            observer_name="TestObserver",
            artifact_id="test_artifact",
            file_path="test.py",
            warning_code="W001",
            warning_message="Test warning message",
            suggestion="Fix it",
            severity="high"
        )
        text = str(warning)
        assert "TestObserver" in text
        assert "test_artifact" in text
        assert "Test warning message" in text
        assert "Fix it" in text

    def test_validation_warning_str_without_artifact_id(self):
        """Test ValidationWarning string when artifact_id is None"""
        warning = ValidationWarning(
            observer_name="TestObserver",
            artifact_id=None,
            file_path="test.py",
            warning_code="W001",
            warning_message="Unregistered file",
            suggestion="Register it",
            severity="medium"
        )
        text = str(warning)
        assert "test.py" in text

    def test_validation_result_has_warnings(self):
        """Test ValidationResult has_warnings method"""
        result = ValidationResult(
            observer_name="TestObserver",
            warnings=[],
            execution_time_ms=10.0
        )
        assert not result.has_warnings()
        
        result_with_warnings = ValidationResult(
            observer_name="TestObserver",
            warnings=[ValidationWarning(
                observer_name="TestObserver",
                artifact_id="test",
                file_path="test.py",
                warning_code="W001",
                warning_message="Warning",
                suggestion="Fix",
                severity="high"
            )],
            execution_time_ms=10.0
        )
        assert result_with_warnings.has_warnings()

    def test_validation_result_severity_filters(self):
        """Test ValidationResult severity filter methods"""
        warnings = [
            ValidationWarning("Obs", "a1", "f1.py", "W001", "Critical", "Fix", "critical"),
            ValidationWarning("Obs", "a2", "f2.py", "W002", "High", "Fix", "high"),
            ValidationWarning("Obs", "a3", "f3.py", "W003", "Medium", "Fix", "medium"),
            ValidationWarning("Obs", "a4", "f4.py", "W004", "Low", "Fix", "low"),
        ]
        result = ValidationResult(
            observer_name="TestObserver",
            warnings=warnings,
            execution_time_ms=5.0
        )
        
        assert len(result.get_critical_warnings()) == 1
        assert len(result.get_high_warnings()) == 1
        assert len(result.get_medium_warnings()) == 1
        assert len(result.get_low_warnings()) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
