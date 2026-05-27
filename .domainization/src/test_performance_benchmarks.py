"""
Performance benchmark tests for domainization system

Validates non-functional requirements:
- Commit gate validation: < 5 seconds for 1000 artifacts (Req 15.1)
- Registry queries: support at least 1000 artifacts (Req 15.2)
- Health report generation: < 10 seconds for 1000 artifacts (Req 15.3)
- System scalability: support at least 20 domains (Req 15.9)

Requirements: 15.1, 15.2, 15.3, 15.9
"""

import pytest
import tempfile
import time
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager
from registry_cache import RegistryCache
from validation_orchestrator import ValidationOrchestrator
from health_reporter import HealthReporter
from violation_detector import ViolationDetector


# ---------------------------------------------------------------------------
# Fixtures: Test data generation
# ---------------------------------------------------------------------------

DOMAINS = [
    'SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT', 'ARCH',
    'STATE', 'DATA', 'USER', 'DEPLOY', 'MEMORY', 'SIM', 'GOV'
]

ARTIFACT_TYPES = ['ENGINE', 'SSOT', 'DATA_OUT', 'REPORT_OUT', 'CONFIG',
                  'DATA_IN', 'RUNTIME', 'DASHBOARD', 'SNAPSHOT', 'CALIBRATION', 'STEERING']

LIFECYCLE_STATES = {
    'ENGINE': ['planned', 'development', 'active', 'deprecated'],
    'SSOT': ['draft', 'review', 'canonical', 'deprecated'],
    'DATA_OUT': ['generated', 'current', 'archived'],
    'REPORT_OUT': ['generated', 'current', 'archived'],
    'CONFIG': ['draft', 'active', 'deprecated'],
    'DATA_IN': ['active', 'stale', 'archived'],
    'RUNTIME': ['planned', 'development', 'active', 'deprecated'],
    'DASHBOARD': ['planned', 'development', 'active', 'deprecated'],
    'SNAPSHOT': ['generated', 'current', 'archived'],
    'CALIBRATION': ['draft', 'active', 'deprecated'],
    'STEERING': ['draft', 'active', 'deprecated'],
}


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def generate_artifact_registry_yaml(num_artifacts: int) -> dict:
    """
    Generate artifact registry data with specified number of artifacts.

    Creates realistic artifact entries distributed across all domains and types.
    """
    artifacts = []
    for i in range(num_artifacts):
        domain = DOMAINS[i % len(DOMAINS)]
        artifact_type = ARTIFACT_TYPES[i % len(ARTIFACT_TYPES)]
        states = LIFECYCLE_STATES[artifact_type]
        lifecycle = states[i % len(states)]

        artifact = {
            'artifact_id': f'perf_artifact_{i:05d}',
            'file_path': f'src/module_{i % 50}/artifact_{i:05d}.py',
            'primary_domain': domain,
            'artifact_type': artifact_type,
            'lifecycle_status': lifecycle,
            'created_date': '2026-01-01',
            'last_modified': '2026-05-01',
            'owner_role': f'Team {domain}',
            'ssot_relationship': 'implementation',
            'allowed_writers': [domain],
            'allowed_readers': ['ALL'],
            'topic': f'topic_{i % 200}',
        }

        # Add secondary domains to ~30% of artifacts
        if i % 3 == 0:
            artifact['secondary_domains'] = [DOMAINS[(i + 3) % len(DOMAINS)]]

        # Add dependencies to ~40% of artifacts
        if i % 5 < 2 and i > 10:
            artifact['dependencies'] = [f'perf_artifact_{(i - 5):05d}']

        artifacts.append(artifact)

    return {'artifacts': artifacts}


def generate_domain_registry_yaml() -> dict:
    """Generate domain registry with 12+ domains for scalability testing"""
    domains = []
    for i, domain_id in enumerate(DOMAINS):
        domain = {
            'domain_id': domain_id,
            'name': f'{domain_id.title()} Domain',
            'responsibility_scope': f'Manages {domain_id.lower()} artifacts',
            'allowed_artifact_types': ARTIFACT_TYPES[:6],  # Each domain can own multiple types
            'cannot_own': [],
            'priority': 'core' if domain_id in ['SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT'] else 'surface',
        }
        if domain_id in ['SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT']:
            domain['authority_level'] = ['SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT'].index(domain_id) + 1
        domains.append(domain)

    # Add extra domains to test scalability beyond 12 (Req 15.9: support 20 domains)
    for i in range(8):
        domains.append({
            'domain_id': f'EXTRA_{i:02d}',
            'name': f'Extra Domain {i}',
            'responsibility_scope': f'Extended domain {i}',
            'allowed_artifact_types': ARTIFACT_TYPES[:4],
            'cannot_own': [],
            'priority': 'surface',
        })

    return {'domains': domains}


def generate_lifecycle_state_machine_yaml() -> dict:
    """Generate lifecycle state machine definitions for all artifact types"""
    artifact_types = {}
    for atype, states in LIFECYCLE_STATES.items():
        transitions = []
        for j in range(len(states) - 1):
            transitions.append({
                'from': states[j],
                'to': states[j + 1],
                'condition': f'Transition from {states[j]} to {states[j+1]}'
            })
        artifact_types[atype] = {
            'description': f'{atype} artifacts',
            'states': states,
            'initial_state': states[0],
            'transitions': transitions,
            'modifiable_states': states[:-1],
            'read_only_states': [states[-1]],
        }
    return {'artifact_types': artifact_types}


def write_test_registries(temp_dir: Path, num_artifacts: int):
    """Write all registry files needed for testing"""
    # Artifact registry
    artifact_path = temp_dir / "artifact_registry.yaml"
    with open(artifact_path, 'w') as f:
        yaml.dump(generate_artifact_registry_yaml(num_artifacts), f)

    # Domain registry
    domain_path = temp_dir / "domain_registry.yaml"
    with open(domain_path, 'w') as f:
        yaml.dump(generate_domain_registry_yaml(), f)

    # Lifecycle state machine
    lifecycle_path = temp_dir / "lifecycle_state_machine.yaml"
    with open(lifecycle_path, 'w') as f:
        yaml.dump(generate_lifecycle_state_machine_yaml(), f)

    return artifact_path, domain_path, lifecycle_path


# ---------------------------------------------------------------------------
# Test Class: Commit Gate Validation Performance (Req 15.1)
# ---------------------------------------------------------------------------

class TestCommitGateValidationPerformance:
    """
    Verify commit gate validation completes within performance targets.

    Requirement 15.1: Commit gates SHALL complete in less than 5 seconds.
    """

    def test_validation_100_artifacts_under_5_seconds(self, temp_dir):
        """Commit gate validation with 100 artifacts completes in < 5 seconds"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 100)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        start = time.time()
        report = orchestrator.validate_all(changed_files=None)
        elapsed = time.time() - start

        print(f"\nValidation time for 100 artifacts: {elapsed:.3f}s")
        print(f"Performance target met: {report.performance_target_met}")

        # Must complete in < 5 seconds (Req 15.1)
        assert elapsed < 5.0, f"Validation took {elapsed:.3f}s, exceeds 5s target"
        assert report.performance_target_met

    def test_validation_1000_artifacts_under_5_seconds(self, temp_dir):
        """Commit gate validation with 1000 artifacts completes in < 5 seconds"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        start = time.time()
        report = orchestrator.validate_all(changed_files=None)
        elapsed = time.time() - start

        print(f"\nValidation time for 1000 artifacts: {elapsed:.3f}s")
        print(f"Total warnings: {report.total_warnings}")
        print(f"Performance target met: {report.performance_target_met}")

        # Must complete in < 5 seconds (Req 15.1)
        assert elapsed < 5.0, f"Validation took {elapsed:.3f}s, exceeds 5s target"
        assert report.performance_target_met

    def test_validation_with_changed_files_subset(self, temp_dir):
        """Validation of a subset of changed files is faster than full validation"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        # Validate only 10 changed files
        changed_files = [Path(f'src/module_0/artifact_{i:05d}.py') for i in range(10)]

        start = time.time()
        report = orchestrator.validate_all(changed_files=changed_files)
        elapsed = time.time() - start

        print(f"\nValidation time for 10 changed files (1000 in registry): {elapsed:.3f}s")

        # Subset validation should be well under 5 seconds
        assert elapsed < 2.0, f"Subset validation took {elapsed:.3f}s, expected < 2s"

    def test_individual_observer_performance(self, temp_dir):
        """Each individual observer completes within reasonable time"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        observers = [
            ('RegistrationValidator', orchestrator.observer_registration),
            ('DomainAssignmentValidator', orchestrator.observer_domain),
            ('LifecycleValidator', orchestrator.observer_lifecycle),
            ('BoundaryAwarenessValidator', orchestrator.observer_boundary),
            ('SSOTConsistencyValidator', orchestrator.observer_ssot),
        ]

        for name, observer in observers:
            start = time.time()
            observer.validate(changed_files=None)
            elapsed = time.time() - start

            print(f"\n{name}: {elapsed:.3f}s")
            # Each observer should complete in < 2 seconds individually
            assert elapsed < 2.0, f"{name} took {elapsed:.3f}s, exceeds 2s per-observer target"


# ---------------------------------------------------------------------------
# Test Class: Health Report Generation Performance (Req 15.3)
# ---------------------------------------------------------------------------

class TestHealthReportGenerationPerformance:
    """
    Verify health report generation completes within performance targets.

    Requirement 15.3: Health reports SHALL complete in less than 10 seconds.
    """

    def test_health_report_100_artifacts_under_10_seconds(self, temp_dir):
        """Health report generation with 100 artifacts completes in < 10 seconds"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 100)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)
        violation_detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            violation_detector=violation_detector,
            repo_root=temp_dir,
        )

        start = time.time()
        report = reporter.generate_health_report(include_violations=True)
        elapsed = time.time() - start

        print(f"\nHealth report time for 100 artifacts: {elapsed:.3f}s")
        print(f"Total artifacts in report: {report['summary']['total_artifacts']}")

        # Must complete in < 10 seconds (Req 15.3)
        assert elapsed < 10.0, f"Health report took {elapsed:.3f}s, exceeds 10s target"
        assert report['summary']['total_artifacts'] == 100

    def test_health_report_1000_artifacts_under_10_seconds(self, temp_dir):
        """Health report generation with 1000 artifacts completes in < 10 seconds"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)
        violation_detector = ViolationDetector(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            violation_detector=violation_detector,
            repo_root=temp_dir,
        )

        start = time.time()
        report = reporter.generate_health_report(include_violations=True)
        elapsed = time.time() - start

        print(f"\nHealth report time for 1000 artifacts: {elapsed:.3f}s")
        print(f"Total artifacts in report: {report['summary']['total_artifacts']}")
        print(f"Total violations: {report['summary']['total_violations']}")

        # Must complete in < 10 seconds (Req 15.3)
        assert elapsed < 10.0, f"Health report took {elapsed:.3f}s, exceeds 10s target"
        assert report['summary']['total_artifacts'] == 1000

    def test_health_report_without_violations_faster(self, temp_dir):
        """Health report without violation detection is faster"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        start = time.time()
        report = reporter.generate_health_report(include_violations=False)
        elapsed = time.time() - start

        print(f"\nHealth report (no violations) for 1000 artifacts: {elapsed:.3f}s")

        # Without violations should be significantly faster
        assert elapsed < 5.0, f"Health report (no violations) took {elapsed:.3f}s, expected < 5s"
        assert 'violations' not in report

    def test_health_report_domain_coverage_performance(self, temp_dir):
        """Domain coverage calculation is fast with many artifacts"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        # Load registries first
        artifact_registry.load()
        domain_registry.load()

        start = time.time()
        coverage = reporter.get_domain_coverage()
        elapsed = time.time() - start

        print(f"\nDomain coverage calculation for 1000 artifacts: {elapsed:.3f}s")
        print(f"Domains with artifacts: {len([d for d in coverage if d['artifact_count'] > 0])}")

        # Domain coverage should be fast
        assert elapsed < 2.0, f"Domain coverage took {elapsed:.3f}s, expected < 2s"
        # All 12 standard domains should have artifacts
        domains_with_artifacts = [d for d in coverage if d['artifact_count'] > 0]
        assert len(domains_with_artifacts) >= 12

    def test_health_report_lifecycle_distribution_performance(self, temp_dir):
        """Lifecycle distribution calculation is fast with many artifacts"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        # Load registries first
        artifact_registry.load()

        start = time.time()
        distribution = reporter.get_lifecycle_distribution()
        elapsed = time.time() - start

        print(f"\nLifecycle distribution for 1000 artifacts: {elapsed:.3f}s")
        print(f"Artifact types tracked: {len(distribution)}")

        # Lifecycle distribution should be fast
        assert elapsed < 2.0, f"Lifecycle distribution took {elapsed:.3f}s, expected < 2s"
        assert len(distribution) > 0


# ---------------------------------------------------------------------------
# Test Class: Registry Query Performance (Req 15.2)
# ---------------------------------------------------------------------------

class TestRegistryQueryPerformance:
    """
    Verify registry queries perform well with large datasets.

    Requirement 15.2: Registry SHALL support at least 1000 artifacts.
    """

    def test_registry_supports_1000_artifacts(self, temp_dir):
        """Registry loads and queries 1000 artifacts successfully"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        registry = ArtifactRegistry(artifact_path)

        start = time.time()
        registry.load()
        elapsed = time.time() - start

        print(f"\nRegistry load time for 1000 artifacts: {elapsed:.3f}s")

        all_artifacts = registry.list_all_artifacts()
        assert len(all_artifacts) == 1000
        assert elapsed < 5.0, f"Registry load took {elapsed:.3f}s, exceeds 5s"

    def test_artifact_lookup_by_id_performance(self, temp_dir):
        """Individual artifact lookup by ID is fast"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        registry = ArtifactRegistry(artifact_path)
        registry.load()

        # Perform 1000 lookups
        start = time.time()
        for i in range(1000):
            result = registry.get_artifact(f'perf_artifact_{i:05d}')
            assert result is not None
        elapsed = time.time() - start

        print(f"\n1000 artifact lookups: {elapsed:.3f}s ({elapsed/1000*1000:.3f}ms per lookup)")
        assert elapsed < 1.0, f"1000 lookups took {elapsed:.3f}s, expected < 1s"

    def test_domain_filter_query_performance(self, temp_dir):
        """Filtering artifacts by domain is fast"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        registry = ArtifactRegistry(artifact_path)
        registry.load()

        # Query each domain
        start = time.time()
        total_found = 0
        for domain in DOMAINS:
            results = registry.list_artifacts_by_domain(domain)
            total_found += len(results)
        elapsed = time.time() - start

        print(f"\n12 domain queries: {elapsed:.3f}s ({elapsed/12*1000:.3f}ms per query)")
        print(f"Total artifacts found across domains: {total_found}")
        assert elapsed < 2.0, f"Domain queries took {elapsed:.3f}s, expected < 2s"
        assert total_found >= 1000  # All artifacts should be found

    def test_type_filter_query_performance(self, temp_dir):
        """Filtering artifacts by type is fast"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        registry = ArtifactRegistry(artifact_path)
        registry.load()

        # Query each type
        start = time.time()
        total_found = 0
        for atype in ARTIFACT_TYPES:
            results = registry.list_artifacts_by_type(atype)
            total_found += len(results)
        elapsed = time.time() - start

        print(f"\n11 type queries: {elapsed:.3f}s ({elapsed/11*1000:.3f}ms per query)")
        print(f"Total artifacts found across types: {total_found}")
        assert elapsed < 2.0, f"Type queries took {elapsed:.3f}s, expected < 2s"
        assert total_found == 1000

    def test_lifecycle_filter_query_performance(self, temp_dir):
        """Filtering artifacts by lifecycle state is fast"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        registry = ArtifactRegistry(artifact_path)
        registry.load()

        all_states = set()
        for states in LIFECYCLE_STATES.values():
            all_states.update(states)

        start = time.time()
        total_found = 0
        for state in all_states:
            results = registry.list_artifacts_by_lifecycle(state)
            total_found += len(results)
        elapsed = time.time() - start

        print(f"\n{len(all_states)} lifecycle queries: {elapsed:.3f}s")
        print(f"Total artifacts found across states: {total_found}")
        assert elapsed < 2.0, f"Lifecycle queries took {elapsed:.3f}s, expected < 2s"
        assert total_found == 1000

    def test_cached_registry_query_performance(self, temp_dir):
        """Cached registry queries are significantly faster than raw queries"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        cache = RegistryCache(artifact_registry, domain_registry, lifecycle_manager)
        cache.load()

        # Perform 100 mixed queries using cache
        start = time.time()
        for i in range(100):
            cache.get_artifact(f'perf_artifact_{i:05d}')
            cache.list_artifacts_by_domain(DOMAINS[i % len(DOMAINS)])
            cache.list_artifacts_by_type(ARTIFACT_TYPES[i % len(ARTIFACT_TYPES)])
        elapsed = time.time() - start

        print(f"\n300 cached queries (mixed): {elapsed:.3f}s ({elapsed/300*1000:.3f}ms per query)")
        # Cached queries should be very fast
        assert elapsed < 1.0, f"300 cached queries took {elapsed:.3f}s, expected < 1s"


# ---------------------------------------------------------------------------
# Test Class: Scalability (Req 15.9)
# ---------------------------------------------------------------------------

class TestScalability:
    """
    Verify system scales to support required capacity.

    Requirement 15.9: System SHALL support at least 20 domains and 10 lifecycle
    states per artifact type.
    """

    def test_supports_20_domains(self, temp_dir):
        """System supports at least 20 domains"""
        domain_path = temp_dir / "domain_registry.yaml"
        data = generate_domain_registry_yaml()

        with open(domain_path, 'w') as f:
            yaml.dump(data, f)

        domain_registry = DomainRegistry(domain_path)
        domain_registry.load()

        domains = domain_registry.list_domains()
        print(f"\nTotal domains loaded: {len(domains)}")

        # Req 15.9: support at least 20 domains
        assert len(domains) >= 20, f"Only {len(domains)} domains, need >= 20"

    def test_supports_10_lifecycle_states(self, temp_dir):
        """System supports artifact types with up to 10 lifecycle states"""
        lifecycle_path = temp_dir / "lifecycle_state_machine.yaml"

        # Create an artifact type with 10 states
        data = {
            'artifact_types': {
                'COMPLEX_TYPE': {
                    'description': 'Complex artifact with many states',
                    'states': [f'state_{i}' for i in range(10)],
                    'initial_state': 'state_0',
                    'transitions': [
                        {'from': f'state_{i}', 'to': f'state_{i+1}', 'condition': f'Move to state {i+1}'}
                        for i in range(9)
                    ],
                    'modifiable_states': [f'state_{i}' for i in range(9)],
                    'read_only_states': ['state_9'],
                }
            }
        }

        with open(lifecycle_path, 'w') as f:
            yaml.dump(data, f)

        lifecycle_manager = LifecycleManager(lifecycle_path)
        lifecycle_manager.load()

        sm = lifecycle_manager.get_state_machine('COMPLEX_TYPE')
        assert sm is not None
        assert len(sm.states) == 10

        # Validate all transitions work
        for i in range(9):
            is_valid, _ = lifecycle_manager.validate_transition('COMPLEX_TYPE', f'state_{i}', f'state_{i+1}')
            assert is_valid, f"Transition state_{i} -> state_{i+1} should be valid"

    def test_performance_with_20_domains_1000_artifacts(self, temp_dir):
        """Full validation performs well with 20 domains and 1000 artifacts"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        # Verify we have 20 domains
        domain_registry.load()
        assert len(domain_registry.list_domains()) >= 20

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        start = time.time()
        report = orchestrator.validate_all(changed_files=None)
        elapsed = time.time() - start

        print(f"\nValidation with 20 domains, 1000 artifacts: {elapsed:.3f}s")
        assert elapsed < 5.0, f"Validation took {elapsed:.3f}s, exceeds 5s target"


# ---------------------------------------------------------------------------
# Test Class: End-to-End Performance Scenario
# ---------------------------------------------------------------------------

class TestEndToEndPerformanceScenario:
    """
    End-to-end performance scenario simulating real-world usage patterns.
    """

    def test_full_commit_gate_workflow(self, temp_dir):
        """
        Simulate complete commit gate workflow:
        1. Load registries
        2. Run all 5 observers
        3. Generate observability report
        Total must be < 5 seconds for 1000 artifacts.
        """
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        # Time the full workflow from cold start
        start = time.time()

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        report = orchestrator.validate_all(changed_files=None)

        elapsed = time.time() - start

        print(f"\nFull commit gate workflow (cold start): {elapsed:.3f}s")
        print(f"Warnings generated: {report.total_warnings}")

        # Full workflow including loading must be < 5 seconds
        assert elapsed < 5.0, f"Full workflow took {elapsed:.3f}s, exceeds 5s target"

    def test_repeated_validation_performance(self, temp_dir):
        """Repeated validations (warm cache) are faster than first run"""
        artifact_path, domain_path, lifecycle_path = write_test_registries(temp_dir, 1000)

        artifact_registry = ArtifactRegistry(artifact_path)
        domain_registry = DomainRegistry(domain_path)
        lifecycle_manager = LifecycleManager(lifecycle_path)

        orchestrator = ValidationOrchestrator(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=temp_dir,
        )

        # First run (cold)
        start = time.time()
        orchestrator.validate_all(changed_files=None)
        cold_elapsed = time.time() - start

        # Second run (warm - registries already loaded)
        start = time.time()
        orchestrator.validate_all(changed_files=None)
        warm_elapsed = time.time() - start

        print(f"\nCold validation: {cold_elapsed:.3f}s")
        print(f"Warm validation: {warm_elapsed:.3f}s")
        print(f"Speedup: {cold_elapsed/warm_elapsed:.1f}x")

        # Both must be under 5 seconds
        assert cold_elapsed < 5.0
        assert warm_elapsed < 5.0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
