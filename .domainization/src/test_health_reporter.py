"""
Unit tests for health reporter
"""

import pytest
import yaml
from pathlib import Path
from datetime import datetime
from health_reporter import HealthReporter
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
                'allowed_readers': ['ALL']
            },
            {
                'artifact_id': 'test_engine_1',
                'file_path': 'engines/test_engine.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL']
            },
            {
                'artifact_id': 'test_ssot_2',
                'file_path': 'docs/test2.md',
                'primary_domain': 'SEMANTICS',
                'artifact_type': 'SSOT',
                'lifecycle_status': 'draft',
                'created_date': '2026-01-01',
                'last_modified': '2026-01-01',
                'owner_role': 'Test owner',
                'ssot_relationship': 'canonical',
                'allowed_writers': ['SEMANTICS'],
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
                'allowed_artifact_types': ['SSOT', 'ENGINE', 'DATA_OUT'],
                'cannot_own': ['SEMANTIC_STATE', 'REASONING_OBJECT'],
                'priority': 'core',
                'authority_level': 1
            },
            {
                'domain_id': 'SEMANTICS',
                'name': 'Semantic Interpretation',
                'responsibility_scope': 'Interpret signals',
                'allowed_artifact_types': ['SSOT', 'ENGINE'],
                'cannot_own': ['SIGNAL'],
                'priority': 'core',
                'authority_level': 2
            },
            {
                'domain_id': 'REASONING',
                'name': 'Reasoning Logic',
                'responsibility_scope': 'Apply reasoning',
                'allowed_artifact_types': ['SSOT', 'ENGINE'],
                'cannot_own': ['SIGNAL', 'SEMANTIC_STATE'],
                'priority': 'core',
                'authority_level': 3
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
                    {'from': 'review', 'to': 'canonical', 'condition': 'Approved'},
                    {'from': 'canonical', 'to': 'deprecated', 'condition': 'Superseded'}
                ],
                'modifiable_states': ['draft', 'review', 'canonical'],
                'read_only_states': ['deprecated']
            },
            'ENGINE': {
                'description': 'Implementation engines',
                'states': ['planned', 'development', 'active', 'deprecated'],
                'initial_state': 'planned',
                'transitions': [
                    {'from': 'planned', 'to': 'development', 'condition': 'Started'},
                    {'from': 'development', 'to': 'active', 'condition': 'Ready'},
                    {'from': 'active', 'to': 'deprecated', 'condition': 'Replaced'}
                ],
                'modifiable_states': ['planned', 'development', 'active'],
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
    
    return artifact_registry, domain_registry, lifecycle_manager


def test_health_reporter_initialization(test_registries):
    """Test health reporter initialization"""
    artifact_registry, domain_registry, lifecycle_manager = test_registries
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    assert reporter.artifact_registry is artifact_registry
    assert reporter.domain_registry is domain_registry
    assert reporter.lifecycle_manager is lifecycle_manager


def test_generate_health_report(test_registries):
    """Test health report generation"""
    artifact_registry, domain_registry, lifecycle_manager = test_registries
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    report = reporter.generate_health_report()
    
    # Check report structure
    assert 'report_date' in report
    assert 'report_time' in report
    assert 'report_version' in report
    assert 'enforcement_mode' in report
    assert 'summary' in report
    assert 'domain_coverage' in report
    assert 'lifecycle_distribution' in report
    
    # Check summary
    summary = report['summary']
    assert summary['total_artifacts'] == 3
    assert summary['registered_artifacts'] == 3
    assert summary['registration_percentage'] == 100.0
    assert summary['total_domains'] == 3


def test_get_domain_coverage(test_registries):
    """Test domain coverage calculation"""
    artifact_registry, domain_registry, lifecycle_manager = test_registries
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    # Load registries
    artifact_registry.load()
    domain_registry.load()
    
    coverage = reporter.get_domain_coverage()
    
    # Should have 3 domains
    assert len(coverage) == 3
    
    # Find SIGNALS domain
    signals_domain = next(d for d in coverage if d['domain_id'] == 'SIGNALS')
    assert signals_domain['artifact_count'] == 2  # 1 SSOT + 1 ENGINE
    assert len(signals_domain['artifact_types']) == 2
    
    # Find SEMANTICS domain
    semantics_domain = next(d for d in coverage if d['domain_id'] == 'SEMANTICS')
    assert semantics_domain['artifact_count'] == 1  # 1 SSOT
    assert len(semantics_domain['artifact_types']) == 1
    
    # Find REASONING domain
    reasoning_domain = next(d for d in coverage if d['domain_id'] == 'REASONING')
    assert reasoning_domain['artifact_count'] == 0  # No artifacts


def test_get_lifecycle_distribution(test_registries):
    """Test lifecycle distribution calculation"""
    artifact_registry, domain_registry, lifecycle_manager = test_registries
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    # Load registries
    artifact_registry.load()
    
    distribution = reporter.get_lifecycle_distribution()
    
    # Should have 2 artifact types (SSOT and ENGINE)
    assert len(distribution) == 2
    
    # Find SSOT distribution
    ssot_dist = next(d for d in distribution if d['artifact_type'] == 'SSOT')
    assert ssot_dist['total_count'] == 2
    
    # Check states
    states_dict = {s['state']: s['count'] for s in ssot_dist['states']}
    assert states_dict.get('canonical', 0) == 1
    assert states_dict.get('draft', 0) == 1
    
    # Find ENGINE distribution
    engine_dist = next(d for d in distribution if d['artifact_type'] == 'ENGINE')
    assert engine_dist['total_count'] == 1
    
    states_dict = {s['state']: s['count'] for s in engine_dist['states']}
    assert states_dict.get('active', 0) == 1


def test_save_report(test_registries, tmp_path):
    """Test saving health report"""
    artifact_registry, domain_registry, lifecycle_manager = test_registries
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    report = reporter.generate_health_report()
    
    # Save to custom path
    output_path = tmp_path / "test_report.yaml"
    saved_path = reporter.save_report(report, output_path)
    
    assert saved_path == output_path
    assert output_path.exists()
    
    # Load and verify
    with open(output_path, 'r') as f:
        loaded_report = yaml.safe_load(f)
    
    assert loaded_report['summary']['total_artifacts'] == 3


def test_format_report_text(test_registries):
    """Test formatting health report as text"""
    artifact_registry, domain_registry, lifecycle_manager = test_registries
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    report = reporter.generate_health_report()
    text = reporter.format_report_text(report)
    
    # Check key sections are present
    assert "DOMAINIZATION HEALTH REPORT" in text
    assert "SUMMARY" in text
    assert "DOMAIN COVERAGE" in text
    assert "LIFECYCLE DISTRIBUTION" in text
    assert "Total Artifacts:" in text
    assert "Signal Generation" in text


def test_empty_registry(tmp_path):
    """Test health report with empty registry"""
    # Create empty artifact registry
    artifact_registry_path = tmp_path / "artifact_registry.yaml"
    with open(artifact_registry_path, 'w') as f:
        yaml.dump({'artifacts': []}, f)
    
    # Create minimal domain registry
    domain_registry_path = tmp_path / "domain_registry.yaml"
    domain_data = {
        'domains': [
            {
                'domain_id': 'SIGNALS',
                'name': 'Signal Generation',
                'responsibility_scope': 'Generate raw signals',
                'allowed_artifact_types': ['SSOT'],
                'cannot_own': [],
                'priority': 'core',
                'authority_level': 1
            }
        ]
    }
    with open(domain_registry_path, 'w') as f:
        yaml.dump(domain_data, f)
    
    # Create minimal lifecycle
    lifecycle_path = tmp_path / "lifecycle_state_machine.yaml"
    with open(lifecycle_path, 'w') as f:
        yaml.dump({'artifact_types': {}}, f)
    
    artifact_registry = ArtifactRegistry(artifact_registry_path)
    domain_registry = DomainRegistry(domain_registry_path)
    lifecycle_manager = LifecycleManager(lifecycle_path)
    
    reporter = HealthReporter(
        artifact_registry=artifact_registry,
        domain_registry=domain_registry,
        lifecycle_manager=lifecycle_manager
    )
    
    report = reporter.generate_health_report()
    
    # Check empty report
    assert report['summary']['total_artifacts'] == 0
    assert report['summary']['registration_percentage'] == 0.0
    assert len(report['domain_coverage']) == 1
    assert len(report['lifecycle_distribution']) == 0
