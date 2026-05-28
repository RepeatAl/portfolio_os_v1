"""
Unit tests for health reporter observability polish (task 11.8).

Tests governance event integration, sunset governance report integration,
structured event emission, state transitions, and integrity verification.

Requirements: 1.5, 3.4, 4.6, 17.4, 18.4
"""

import pytest
import yaml
from pathlib import Path
from datetime import datetime, date, timezone
from unittest.mock import patch, MagicMock

from health_reporter import HealthReporter
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from lifecycle_manager import LifecycleManager


@pytest.fixture
def test_registries_with_deprecation(tmp_path):
    """Create test registries with deprecated artifacts for sunset governance testing."""
    # Create artifact registry with deprecated artifacts
    artifact_registry_path = tmp_path / "artifact_registry.yaml"
    artifact_data = {
        'artifacts': [
            {
                'artifact_id': 'active_artifact_1',
                'file_path': 'engines/active_engine.py',
                'primary_domain': 'SIGNALS',
                'artifact_type': 'ENGINE',
                'lifecycle_status': 'active',
                'created_date': '2026-01-01',
                'last_modified': '2026-05-01',
                'owner_role': 'CTO',
                'ssot_relationship': 'implementation',
                'allowed_writers': ['SIGNALS'],
                'allowed_readers': ['ALL'],
                'report_value': {
                    'category': 'semantic_interpretation',
                    'justification': 'Produces allocation signals for daily report'
                },
            },
            {
                'artifact_id': 'deprecated_briefing_1',
                'file_path': 'output/allocation_briefing.txt',
                'primary_domain': 'REPORT',
                'artifact_type': 'REPORT_OUT',
                'lifecycle_status': 'deprecated',
                'created_date': '2025-01-01',
                'last_modified': '2026-03-01',
                'owner_role': 'CTO',
                'ssot_relationship': 'derived',
                'allowed_writers': ['REPORT'],
                'allowed_readers': ['ALL'],
                'deprecated_date': '2026-04-01',
                'sunset_date': '2026-07-01',
                'replacement_artifact': 'daily_report_allocation_section',
                'deprecation_reason': 'Replaced by chain-compliant daily report section',
                'compatibility_impact': 'minor',
                'report_value': {
                    'category': 'pm_reasoning',
                    'justification': 'Legacy allocation briefing for PM consumption'
                },
                'dependencies': ['active_artifact_1'],
            },
            {
                'artifact_id': 'deprecated_briefing_2',
                'file_path': 'output/regime_briefing.txt',
                'primary_domain': 'REPORT',
                'artifact_type': 'REPORT_OUT',
                'lifecycle_status': 'deprecated',
                'created_date': '2025-01-01',
                'last_modified': '2026-03-01',
                'owner_role': 'CTO',
                'ssot_relationship': 'derived',
                'allowed_writers': ['REPORT'],
                'allowed_readers': ['ALL'],
                'deprecated_date': '2026-04-01',
                'sunset_date': '2026-05-01',
                'replacement_artifact': 'daily_report_regime_section',
                'deprecation_reason': 'Replaced by chain-compliant daily report section',
                'compatibility_impact': 'minor',
                'report_value': {
                    'category': 'pm_reasoning',
                    'justification': 'Legacy regime briefing for PM consumption'
                },
                'dependencies': [],
            },
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
                'domain_id': 'REPORT',
                'name': 'Report Output',
                'responsibility_scope': 'Generate reports',
                'allowed_artifact_types': ['REPORT_OUT'],
                'cannot_own': ['SIGNAL'],
                'priority': 'core',
                'authority_level': 4
            },
        ]
    }
    with open(domain_registry_path, 'w') as f:
        yaml.dump(domain_data, f)

    # Create lifecycle state machine
    lifecycle_path = tmp_path / "lifecycle_state_machine.yaml"
    lifecycle_data = {
        'artifact_types': {
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
            },
            'REPORT_OUT': {
                'description': 'Report output files',
                'states': ['generated', 'current', 'deprecated', 'sunset_pending', 'archived', 'superseded'],
                'initial_state': 'generated',
                'transitions': [
                    {'from': 'generated', 'to': 'current', 'condition': 'Validated'},
                    {'from': 'current', 'to': 'deprecated', 'condition': 'Replaced by chain-compliant output'},
                    {'from': 'deprecated', 'to': 'sunset_pending', 'condition': 'Sunset target date reached'},
                    {'from': 'sunset_pending', 'to': 'archived', 'condition': 'Zero downstream dependencies'},
                    {'from': 'current', 'to': 'superseded', 'condition': 'Replaced by different artifact type'},
                ],
                'modifiable_states': ['generated', 'current', 'deprecated', 'sunset_pending'],
                'read_only_states': ['archived', 'superseded']
            }
        }
    }
    with open(lifecycle_path, 'w') as f:
        yaml.dump(lifecycle_data, f)

    # Create .domainization directory structure for sunset governance
    domainization_dir = tmp_path / ".domainization"
    domainization_dir.mkdir(exist_ok=True)
    # Copy artifact registry to .domainization path for SunsetGovernance
    import shutil
    shutil.copy(artifact_registry_path, domainization_dir / "artifact_registry.yaml")

    artifact_registry = ArtifactRegistry(artifact_registry_path)
    domain_registry = DomainRegistry(domain_registry_path)
    lifecycle_manager = LifecycleManager(lifecycle_path)

    return artifact_registry, domain_registry, lifecycle_manager, tmp_path


class TestGovernanceEventEmission:
    """Tests that validators emit structured events with severity, description,
    component, and timestamp (Req 17.4, 18.4)."""

    def test_emit_governance_event_structure(self, test_registries_with_deprecation):
        """Test that governance events have all required fields."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        from runtime.severity_taxonomy import Severity

        event = reporter._emit_governance_event(
            Severity.WARNING,
            "Test governance event description",
            "test_component.test_method",
        )

        # Verify all required fields present
        assert "severity" in event
        assert "description" in event
        assert "component" in event
        assert "timestamp" in event

        # Verify field values
        assert event["severity"] == "WARNING"
        assert event["severity_level"] == 1
        assert event["description"] == "Test governance event description"
        assert event["component"] == "test_component.test_method"
        assert event["timestamp"].endswith("Z")

    def test_governance_events_accumulated_in_report(
        self, test_registries_with_deprecation
    ):
        """Test that governance events are included in the health report."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()

        # Report should contain governance_events key
        assert "governance_events" in report
        assert isinstance(report["governance_events"], list)
        assert "total_governance_events" in report["summary"]

    def test_governance_event_timestamp_is_utc_iso8601(
        self, test_registries_with_deprecation
    ):
        """Test that governance event timestamps are valid ISO 8601 UTC."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        from runtime.severity_taxonomy import Severity

        event = reporter._emit_governance_event(
            Severity.INFO, "Test event", "test_component"
        )

        timestamp = event["timestamp"]
        assert timestamp.endswith("Z")
        # Should parse without error
        parsed = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        assert parsed is not None


class TestStateTransitions:
    """Tests that state transitions include previous state, new state, reason,
    and timestamp (Req 18.4)."""

    def test_record_state_transition_structure(
        self, test_registries_with_deprecation
    ):
        """Test that state transitions have all required fields."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        transition = reporter._record_state_transition(
            previous_state="healthy",
            new_state="degraded",
            reason="2 unregistered artifacts detected",
        )

        # Verify all required fields
        assert "previous_state" in transition
        assert "new_state" in transition
        assert "reason" in transition
        assert "timestamp" in transition

        # Verify values
        assert transition["previous_state"] == "healthy"
        assert transition["new_state"] == "degraded"
        assert transition["reason"] == "2 unregistered artifacts detected"
        assert transition["timestamp"].endswith("Z")

    def test_state_transitions_in_report(self, test_registries_with_deprecation):
        """Test that state transitions are included in the health report."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()

        assert "state_transitions" in report
        assert isinstance(report["state_transitions"], list)
        assert "total_state_transitions" in report["summary"]

    def test_state_transition_updates_current_state(
        self, test_registries_with_deprecation
    ):
        """Test that recording a transition updates the current state."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        assert reporter._current_state == "healthy"

        reporter._record_state_transition("healthy", "degraded", "test reason")
        assert reporter._current_state == "degraded"


class TestSunsetGovernanceIntegration:
    """Tests sunset governance report integration into health report."""

    def test_sunset_governance_in_report(self, test_registries_with_deprecation):
        """Test that sunset governance data is included in health report."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()

        assert "sunset_governance" in report
        sg = report["sunset_governance"]
        assert "total_deprecated" in sg
        assert "phase_distribution" in sg
        assert "sunset_blocked_count" in sg
        assert "sunset_blocked_artifacts" in sg
        assert "deprecated_artifacts" in sg

    def test_sunset_governance_detects_deprecated_artifacts(
        self, test_registries_with_deprecation
    ):
        """Test that deprecated artifacts are detected in sunset report."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        sg = report["sunset_governance"]

        # We have 2 deprecated artifacts in the fixture
        assert sg["total_deprecated"] == 2
        assert len(sg["deprecated_artifacts"]) == 2

    def test_sunset_governance_detects_blocked_sunsets(
        self, test_registries_with_deprecation
    ):
        """Test that sunset-blocked artifacts are detected.

        deprecated_briefing_1 has sunset_date 2026-07-01 (future) so not blocked.
        deprecated_briefing_2 has sunset_date 2026-05-01 (past) and no deps, so
        it should be at RUNTIME_DISABLED phase but NOT blocked (zero deps).
        """
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        sg = report["sunset_governance"]

        # deprecated_briefing_2 has sunset_date in the past and zero deps
        # so it's RUNTIME_DISABLED but NOT sunset-blocked
        assert sg["sunset_blocked_count"] == 0

    def test_sunset_governance_summary_in_report_summary(
        self, test_registries_with_deprecation
    ):
        """Test that sunset governance metrics appear in report summary."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        summary = report["summary"]

        assert "deprecated_artifacts" in summary
        assert "sunset_blocked_count" in summary
        assert summary["deprecated_artifacts"] == 2


class TestIntegrityVerification:
    """Tests integrity verification (zero forbidden flows, zero unregistered,
    100% report_value coverage)."""

    def test_integrity_verification_in_report(
        self, test_registries_with_deprecation
    ):
        """Test that integrity verification is included in health report."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()

        assert "integrity_verification" in report
        iv = report["integrity_verification"]
        assert "zero_forbidden_flows" in iv
        assert "zero_unregistered_artifacts" in iv
        assert "full_report_value_coverage" in iv
        assert "overall_integrity_state" in iv
        assert "details" in iv

    def test_integrity_verification_details(
        self, test_registries_with_deprecation
    ):
        """Test that integrity verification details contain specific metrics."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        details = report["integrity_verification"]["details"]

        assert "forbidden_flow_count" in details
        assert "unregistered_artifact_count" in details
        assert "report_value_valid_percentage" in details

    def test_integrity_emits_governance_events_on_failure(
        self, test_registries_with_deprecation
    ):
        """Test that integrity failures emit governance events."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        # Generate report — this will trigger integrity verification
        report = reporter.generate_health_report()

        # There should be governance events emitted
        events = report["governance_events"]
        assert len(events) > 0

        # All events should have required fields
        for event in events:
            assert "severity" in event
            assert "description" in event
            assert "component" in event
            assert "timestamp" in event


class TestFormatReportText:
    """Tests that the formatted text report includes new sections."""

    def test_format_includes_sunset_governance(
        self, test_registries_with_deprecation
    ):
        """Test that formatted text includes sunset governance section."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        text = reporter.format_report_text(report)

        assert "SUNSET GOVERNANCE" in text
        assert "Total Deprecated Artifacts:" in text

    def test_format_includes_integrity_verification(
        self, test_registries_with_deprecation
    ):
        """Test that formatted text includes integrity verification section."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        text = reporter.format_report_text(report)

        assert "INTEGRITY VERIFICATION" in text
        assert "Overall Integrity State:" in text
        assert "Zero Forbidden Flows" in text
        assert "Zero Unregistered Artifacts" in text
        assert "100% Report Value Coverage" in text

    def test_format_includes_governance_events(
        self, test_registries_with_deprecation
    ):
        """Test that formatted text includes governance events section."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        text = reporter.format_report_text(report)

        assert "GOVERNANCE EVENTS" in text

    def test_format_includes_state_transitions(
        self, test_registries_with_deprecation
    ):
        """Test that formatted text includes state transitions when present."""
        artifact_registry, domain_registry, lifecycle_manager, tmp_path = (
            test_registries_with_deprecation
        )

        reporter = HealthReporter(
            artifact_registry=artifact_registry,
            domain_registry=domain_registry,
            lifecycle_manager=lifecycle_manager,
            repo_root=tmp_path,
        )

        report = reporter.generate_health_report()
        text = reporter.format_report_text(report)

        # State transitions should be present if integrity state changed
        if report["state_transitions"]:
            assert "STATE TRANSITIONS" in text
