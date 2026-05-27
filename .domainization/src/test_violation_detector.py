"""
Unit tests for violation detector
"""

import pytest
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from violation_detector import ViolationDetector, Violation
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager


@pytest.fixture
def test_registries(tmp_path):
    """Create test registries"""
    # Create artifact registry
    artifact_registry_path = tmp_path / "artifact_registry.yaml"
    artifact_data = {
        'artifacts': [
            {
                'artifact_id': 'test_ssot_1',
                'file_path': 'docs/test1.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'test_topic'
            },
            {
                'artifact_id': 'test_ssot_2',
                'file_path': 'docs/test2.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'test_topic'  # Same topic - conflict!
            },
            {
                'artifact_id': 'test_derived',
                'file_path': 'docs/derived.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'derived',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL']
                # Missing dependencies - violation!
            },
            {
                'artifact_id': 'test_no_lifecycle',
                'file_path': 'docs/no_lifecycle.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': '',  # Missing lifecycle - violation!
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL']
            },
            {
                'artifact_id': 'test_deprecated',
                'file_path': 'docs/deprecated.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'deprecated',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL']
            }
        ]
    }
    with open(artifact_registry_path, 'w') as f:
        yaml.dump(artifact_data, f)
    
    # Create domain registry
    domain_registry_path = tmp_path / "domain_registry.yaml"
    domain_data = {
        'domains': [
            {
                'domain_id': 'SIGNALS',
                'name': 'Signal Generation',
                'responsibility_scope': 'Generate raw signals',
                'allowed_artifact_types': ['SSOT', 'ENGINE'],
                'cannot_own': [],
                'priority': 'core',
                'authority_level': 1
            }
        ]
    }
    with open(domain_registry_path, 'w') as f:
        yaml.dump(domain_data, f)
    
    # Create lifecycle state machine
    lifecycle_path = tmp_path / "lifecycle_state_machine.yaml"
    lifecycle_data = {
        'artifact_types': {
            'SSOT': {
                'description': 'Single Source of Truth documents',
                'states': ['draft', 'review', 'canonical', 'deprecated'],
                'initial_state': 'draft',
                'transitions': [
                    {'from': 'draft', 'to': 'review', 'condition': 'Ready for review'},
                    {'from': 'review', 'to': 'canonical', 'condition': 'Approved'}
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
    
    return artifact_registry, domain_registry, lifecycle_manager, tmp_path


def test_violation_initialization():
    """Test violation object initialization"""
    violation = Violation(
        artifact_id='test_id',
        file_path='test/path.md',
        violation_type='test_violation',
        severity='high',
        description='Test description',
        recommendation='Test recommendation'
    )
    
    assert violation.artifact_id == 'test_id'
    assert violation.file_path == 'test/path.md'
    assert violation.violation_type == 'test_violation'
    assert violation.severity == 'high'
    assert violation.description == 'Test description'
    assert violation.recommendation == 'Test recommendation'


def test_violation_to_dict():
    """Test violation to dictionary conversion"""
    violation = Violation(
        artifact_id='test_id',
        file_path='test/path.md',
        violation_type='test_violation',
        severity='high',
        description='Test description',
        recommendation='Test recommendation'
    )
    
    vdict = violation.to_dict()
    
    assert vdict['artifact_id'] == 'test_id'
    assert vdict['file_path'] == 'test/path.md'
    assert vdict['violation_type'] == 'test_violation'
    assert vdict['severity'] == 'high'


def test_violation_detector_initialization(test_registries):
    """Test violation detector initialization"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    assert detector.artifact_registry is artifact_registry
    assert detector.domain_registry is domain_registry
    assert detector.lifecycle_manager is lifecycle_manager


def test_detect_missing_lifecycle_status(test_registries):
    """Test detection of missing lifecycle status"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    violations = detector.detect_missing_lifecycle_status()
    
    # Should find 1 violation (test_no_lifecycle)
    assert len(violations) == 1
    assert violations[0].artifact_id == 'test_no_lifecycle'
    assert violations[0].violation_type == 'missing_lifecycle'
    assert violations[0].severity == 'medium'


def test_detect_ssot_conflicts(test_registries):
    """Test detection of SSOT conflicts"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    violations = detector.detect_ssot_conflicts()
    
    # Should find violations:
    # - 2 for SSOT conflict (test_ssot_1 and test_ssot_2 have same topic)
    # - 1 for missing SSOT reference (test_derived has no dependencies)
    assert len(violations) >= 2
    
    # Check for SSOT conflict violations
    conflict_violations = [v for v in violations if v.violation_type == 'ssot_conflict']
    assert len(conflict_violations) == 2
    
    # Check for missing SSOT reference
    missing_ref_violations = [v for v in violations if v.violation_type == 'missing_ssot_reference']
    assert len(missing_ref_violations) >= 1


def test_detect_deprecated_modifications(test_registries):
    """Test detection of deprecated artifact modifications"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    # Create the deprecated file and touch it recently
    deprecated_file = tmp_path / 'docs' / 'deprecated.md'
    deprecated_file.parent.mkdir(parents=True, exist_ok=True)
    deprecated_file.write_text('test content')
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    violations = detector.detect_deprecated_modifications()
    
    # Should find 1 violation (test_deprecated was recently modified)
    assert len(violations) == 1
    assert violations[0].artifact_id == 'test_deprecated'
    assert violations[0].violation_type == 'deprecated_modification'
    assert violations[0].severity == 'high'


def test_detect_all_violations(test_registries):
    """Test detection of all violations"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    # Create the deprecated file
    deprecated_file = tmp_path / 'docs' / 'deprecated.md'
    deprecated_file.parent.mkdir(parents=True, exist_ok=True)
    deprecated_file.write_text('test content')
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    violations = detector.detect_all_violations()
    
    # Should find multiple violations
    assert len(violations) > 0
    
    # Check that different violation types are present
    violation_types = set(v.violation_type for v in violations)
    assert 'missing_lifecycle' in violation_types
    assert 'ssot_conflict' in violation_types


def test_get_violations_by_severity(test_registries):
    """Test grouping violations by severity"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    # Create test violations
    violations = [
        Violation('id1', 'path1', 'type1', 'critical', 'desc1', 'rec1'),
        Violation('id2', 'path2', 'type2', 'high', 'desc2', 'rec2'),
        Violation('id3', 'path3', 'type3', 'critical', 'desc3', 'rec3'),
    ]
    
    by_severity = detector.get_violations_by_severity(violations)
    
    assert len(by_severity['critical']) == 2
    assert len(by_severity['high']) == 1


def test_get_violations_by_type(test_registries):
    """Test grouping violations by type"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    # Create test violations
    violations = [
        Violation('id1', 'path1', 'ssot_conflict', 'critical', 'desc1', 'rec1'),
        Violation('id2', 'path2', 'missing_lifecycle', 'high', 'desc2', 'rec2'),
        Violation('id3', 'path3', 'ssot_conflict', 'critical', 'desc3', 'rec3'),
    ]
    
    by_type = detector.get_violations_by_type(violations)
    
    assert len(by_type['ssot_conflict']) == 2
    assert len(by_type['missing_lifecycle']) == 1


def test_format_violations_text(test_registries):
    """Test formatting violations as text"""
    artifact_registry, domain_registry, lifecycle_manager, tmp_path = test_registries
    
    detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    # Test with no violations
    text = detector.format_violations_text([])
    assert "No violations detected" in text
    
    # Test with violations
    violations = [
        Violation('id1', 'path1', 'type1', 'critical', 'desc1', 'rec1'),
        Violation('id2', 'path2', 'type2', 'high', 'desc2', 'rec2'),
    ]
    
    text = detector.format_violations_text(violations)
    assert "Found 2 violation(s)" in text
    assert "CRITICAL" in text
    assert "HIGH" in text
