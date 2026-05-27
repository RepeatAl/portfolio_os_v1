"""
Integration tests for health reporter with violation detection
"""

import pytest
import yaml
from pathlib import Path
from health_reporter import HealthReporter
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from violation_detector import ViolationDetector


@pytest.fixture
def test_system_with_violations(tmp_path):
    """Create test system with known violations"""
    # Create artifact registry with violations
    artifact_registry_path = tmp_path / "artifact_registry.yaml"
    artifact_data = {
        'artifacts': [
            {
                'artifact_id': 'good_ssot',
                'file_path': 'docs/good.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'good_topic'
            },
            {
                'artifact_id': 'conflict_ssot_1',
                'file_path': 'docs/conflict1.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'conflict_topic'
            },
            {
                'artifact_id': 'conflict_ssot_2',
                'file_path': 'docs/conflict2.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'canonical',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'topic': 'conflict_topic'  # Same topic - conflict!
            },
            {
                'artifact_id': 'no_lifecycle',
                'file_path': 'docs/no_lifecycle.md',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'SSOT',
                'lifecycle_status': '',  # Missing!
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
            },
            {
                'domain_id': 'SEMANTICS',
                'name': 'Semantic Interpretation',
                'responsibility_scope': 'Interpret signals',
                'allowed_artifact_types': ['SSOT', 'ENGINE'],
                'cannot_own': [],
                'priority': 'core',
                'authority_level': 2
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
                    {'from': 'draft', 'to': 'review', 'condition': 'Ready'},
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
    violation_detector = ViolationDetector(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        repo_root=tmp_path
    )
    
    return artifact_registry, domain_registry, lifecycle_manager, violation_detector, tmp_path


def test_health_report_includes_violations(test_system_with_violations):
    """Test that health report includes violation detection"""
    artifact_registry, domain_registry, lifecycle_manager, violation_detector, tmp_path = test_system_with_violations
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        violation_detector=violation_detector,
        repo_root=tmp_path
    )
    
    report = reporter.generate_health_report(include_violations=True)
    
    # Check that violations are included
    assert 'violations' in report
    assert 'recommendations' in report
    assert 'total_violations' in report['summary']
    assert 'violations_by_severity' in report['summary']
    
    # Should have violations
    assert report['summary']['total_violations'] > 0
    
    # Should have SSOT conflicts (2 artifacts with same topic)
    ssot_conflicts = [v for v in report['violations'] if v['violation_type'] == 'ssot_conflict']
    assert len(ssot_conflicts) == 2
    
    # Should have missing lifecycle
    missing_lifecycle = [v for v in report['violations'] if v['violation_type'] == 'missing_lifecycle']
    assert len(missing_lifecycle) == 1


def test_health_report_without_violations(test_system_with_violations):
    """Test that health report can exclude violations"""
    artifact_registry, domain_registry, lifecycle_manager, violation_detector, tmp_path = test_system_with_violations
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        violation_detector=violation_detector,
        repo_root=tmp_path
    )
    
    report = reporter.generate_health_report(include_violations=False)
    
    # Check that violations are not included
    assert 'violations' not in report
    assert 'recommendations' not in report
    assert 'total_violations' not in report['summary']


def test_health_report_recommendations(test_system_with_violations):
    """Test that recommendations are generated based on violations"""
    artifact_registry, domain_registry, lifecycle_manager, violation_detector, tmp_path = test_system_with_violations
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        violation_detector=violation_detector,
        repo_root=tmp_path
    )
    
    report = reporter.generate_health_report(include_violations=True)
    
    # Should have recommendations
    assert len(report['recommendations']) > 0
    
    # Should recommend resolving SSOT conflicts
    ssot_rec = [r for r in report['recommendations'] if 'SSOT conflict' in r['action']]
    assert len(ssot_rec) > 0
    assert ssot_rec[0]['priority'] == 'high'
    
    # Should recommend adding lifecycle status
    lifecycle_rec = [r for r in report['recommendations'] if 'lifecycle status' in r['action']]
    assert len(lifecycle_rec) > 0
    assert lifecycle_rec[0]['priority'] == 'medium'


def test_health_report_text_format_with_violations(test_system_with_violations):
    """Test text formatting includes violations"""
    artifact_registry, domain_registry, lifecycle_manager, violation_detector, tmp_path = test_system_with_violations
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        violation_detector=violation_detector,
        repo_root=tmp_path
    )
    
    report = reporter.generate_health_report(include_violations=True)
    text = reporter.format_report_text(report)
    
    # Check that violations section is present
    assert "VIOLATIONS" in text
    assert "Total Violations:" in text
    assert "Critical:" in text
    assert "High:" in text
    
    # Check that recommendations section is present
    assert "RECOMMENDATIONS" in text


def test_health_report_save_with_violations(test_system_with_violations, tmp_path):
    """Test saving health report with violations"""
    artifact_registry, domain_registry, lifecycle_manager, violation_detector, test_root = test_system_with_violations
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        violation_detector=violation_detector,
        repo_root=test_root
    )
    
    report = reporter.generate_health_report(include_violations=True)
    
    # Save report
    output_path = tmp_path / "health_with_violations.yaml"
    saved_path = reporter.save_report(report, output_path)
    
    assert saved_path.exists()
    
    # Load and verify
    with open(saved_path, 'r') as f:
        loaded_report = yaml.safe_load(f)
    
    assert 'violations' in loaded_report
    assert 'recommendations' in loaded_report
    assert loaded_report['summary']['total_violations'] > 0


def test_violations_by_severity_in_report(test_system_with_violations):
    """Test that violations are properly categorized by severity"""
    artifact_registry, domain_registry, lifecycle_manager, violation_detector, tmp_path = test_system_with_violations
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager,
        violation_detector=violation_detector,
        repo_root=tmp_path
    )
    
    report = reporter.generate_health_report(include_violations=True)
    
    by_severity = report['summary']['violations_by_severity']
    
    # Should have critical violations (SSOT conflicts)
    assert by_severity['critical'] >= 2
    
    # Should have medium violations (missing lifecycle)
    assert by_severity['medium'] >= 1
    
    # Total should match
    total = sum(by_severity.values())
    assert total == report['summary']['total_violations']
