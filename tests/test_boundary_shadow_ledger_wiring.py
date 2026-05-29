"""Tests for boundary enforcer and shadow authority detector ledger wiring.

Verifies:
- BoundaryEnforcer emits ledger entries for cross-domain interactions when ledger is connected
- ShadowAuthorityDetector emits ledger entries for shadow events when ledger is connected
- Both modules work without a ledger (backward compatible)

Requirements: 19.1, 40.1, 40.3
"""

import os
import tempfile
import uuid

import yaml

from governance.boundary_enforcer import BoundaryEnforcer
from governance.mutation_audit_ledger import LedgerEntry, MutationAuditLedger
from governance.shadow_authority_detector import ShadowAuthorityDetector


def _create_artifact_registry(tmpdir: str, artifacts: list[dict]) -> str:
    """Create a temporary artifact registry YAML file."""
    registry_path = os.path.join(tmpdir, "artifact_registry.yaml")
    with open(registry_path, "w", encoding="utf-8") as f:
        yaml.dump({"artifacts": artifacts}, f)
    return registry_path


def _create_domain_registry(tmpdir: str, domains: list[dict]) -> str:
    """Create a temporary domain registry YAML file."""
    registry_path = os.path.join(tmpdir, "domain_registry.yaml")
    with open(registry_path, "w", encoding="utf-8") as f:
        yaml.dump({"domains": domains}, f)
    return registry_path


class TestBoundaryEnforcerLedgerWiring:
    """Tests for BoundaryEnforcer -> MutationAuditLedger wiring."""

    def test_cross_domain_interaction_emits_ledger_entry(self):
        """BoundaryEnforcer emits GOVERNANCE_EVENT for cross-domain interactions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "report_daily",
                    "artifact_type": "REPORT_OUT",
                    "allowed_writers": ["reporting_domain"],
                    "domain": "reporting_domain",
                }
            ]
            domains = [
                {"domain_id": "analytics_domain"},
                {"domain_id": "reporting_domain"},
            ]
            artifact_path = _create_artifact_registry(tmpdir, artifacts)
            domain_path = _create_domain_registry(tmpdir, domains)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            enforcer = BoundaryEnforcer(
                artifact_registry_path=artifact_path,
                domain_registry_path=domain_path,
                enforcement_mode="observability",
                ledger=ledger,
            )

            # Trigger cross-domain interaction
            enforcer.detect_cross_domain_interaction(
                source_domain="analytics_domain",
                target_domain="reporting_domain",
                artifact_id="report_daily",
                interaction_type="read",
            )

            # Verify ledger entry was emitted
            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 1
            entry = entries[0]
            assert entry.event_type == "GOVERNANCE_EVENT"
            assert entry.details["source_domain"] == "analytics_domain"
            assert entry.details["target_domain"] == "reporting_domain"
            assert entry.details["artifact_id"] == "report_daily"
            assert entry.details["interaction_type"] == "read"
            assert entry.severity == "INFO"

    def test_cross_domain_write_violation_hard_mode_emits_warning(self):
        """Hard mode violations emit WARNING severity ledger entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "config_main",
                    "artifact_type": "CONFIG",
                    "allowed_writers": ["governance_domain"],
                    "domain": "governance_domain",
                }
            ]
            domains = [
                {"domain_id": "analytics_domain"},
                {"domain_id": "governance_domain"},
            ]
            artifact_path = _create_artifact_registry(tmpdir, artifacts)
            domain_path = _create_domain_registry(tmpdir, domains)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            enforcer = BoundaryEnforcer(
                artifact_registry_path=artifact_path,
                domain_registry_path=domain_path,
                enforcement_mode="hard",
                ledger=ledger,
            )

            # Trigger cross-domain write violation
            result = enforcer.detect_cross_domain_interaction(
                source_domain="analytics_domain",
                target_domain="governance_domain",
                artifact_id="config_main",
                interaction_type="write",
            )

            assert result["permitted"] is False
            assert result["enforcement_action"] == "block"

            # Verify ledger entry has WARNING severity
            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 1
            assert entries[0].severity == "WARNING"

    def test_same_domain_interaction_does_not_emit_ledger_entry(self):
        """Same-domain interactions do not emit ledger entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "report_daily",
                    "artifact_type": "REPORT_OUT",
                    "allowed_writers": ["reporting_domain"],
                    "domain": "reporting_domain",
                }
            ]
            domains = [{"domain_id": "reporting_domain"}]
            artifact_path = _create_artifact_registry(tmpdir, artifacts)
            domain_path = _create_domain_registry(tmpdir, domains)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            enforcer = BoundaryEnforcer(
                artifact_registry_path=artifact_path,
                domain_registry_path=domain_path,
                enforcement_mode="observability",
                ledger=ledger,
            )

            # Same-domain interaction
            enforcer.detect_cross_domain_interaction(
                source_domain="reporting_domain",
                target_domain="reporting_domain",
                artifact_id="report_daily",
                interaction_type="write",
            )

            # No ledger entry should be emitted for same-domain
            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 0

    def test_boundary_enforcer_works_without_ledger(self):
        """BoundaryEnforcer works without a ledger (backward compatible)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "report_daily",
                    "artifact_type": "REPORT_OUT",
                    "allowed_writers": ["reporting_domain"],
                    "domain": "reporting_domain",
                }
            ]
            domains = [
                {"domain_id": "analytics_domain"},
                {"domain_id": "reporting_domain"},
            ]
            artifact_path = _create_artifact_registry(tmpdir, artifacts)
            domain_path = _create_domain_registry(tmpdir, domains)

            # No ledger provided
            enforcer = BoundaryEnforcer(
                artifact_registry_path=artifact_path,
                domain_registry_path=domain_path,
                enforcement_mode="observability",
            )

            # Should work without error
            result = enforcer.detect_cross_domain_interaction(
                source_domain="analytics_domain",
                target_domain="reporting_domain",
                artifact_id="report_daily",
                interaction_type="read",
            )

            assert result["is_cross_domain"] is True
            assert result["permitted"] is True

    def test_soft_mode_cross_domain_write_violation_emits_info(self):
        """Soft mode write violations emit INFO severity (not blocked)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "config_main",
                    "artifact_type": "CONFIG",
                    "allowed_writers": ["governance_domain"],
                    "domain": "governance_domain",
                }
            ]
            domains = [
                {"domain_id": "analytics_domain"},
                {"domain_id": "governance_domain"},
            ]
            artifact_path = _create_artifact_registry(tmpdir, artifacts)
            domain_path = _create_domain_registry(tmpdir, domains)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            enforcer = BoundaryEnforcer(
                artifact_registry_path=artifact_path,
                domain_registry_path=domain_path,
                enforcement_mode="soft",
                ledger=ledger,
            )

            # Soft mode: write violation is warned but not blocked
            result = enforcer.detect_cross_domain_interaction(
                source_domain="analytics_domain",
                target_domain="governance_domain",
                artifact_id="config_main",
                interaction_type="write",
            )

            assert result["permitted"] is True
            assert result["enforcement_action"] == "warn"

            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 1
            # Soft mode violation is not a block, so severity is INFO
            assert entries[0].severity == "INFO"


class TestShadowAuthorityDetectorLedgerWiring:
    """Tests for ShadowAuthorityDetector -> MutationAuditLedger wiring."""

    def test_shadow_event_emits_ledger_entry(self):
        """ShadowAuthorityDetector emits GOVERNANCE_EVENT for shadow events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "report_daily",
                    "artifact_type": "REPORT_OUT",
                    "allowed_writers": ["report_engine"],
                }
            ]
            registry_path = _create_artifact_registry(tmpdir, artifacts)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            detector = ShadowAuthorityDetector(
                artifact_registry_path=registry_path,
                ledger=ledger,
            )

            # Record a shadow event (unregistered module writing)
            detector.record_shadow_event(
                writing_module="random_script.py",
                target_artifact_id="report_daily",
                declared_writers=["report_engine"],
            )

            # Verify ledger entry was emitted
            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 1
            entry = entries[0]
            assert entry.event_type == "GOVERNANCE_EVENT"
            assert entry.details["writing_module"] == "random_script.py"
            assert entry.details["target_artifact_id"] == "report_daily"
            assert entry.details["declared_writers"] == ["report_engine"]
            assert entry.details["is_shadow"] is True

    def test_unregistered_module_shadow_emits_warning_severity(self):
        """Unregistered module shadow events emit WARNING severity."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "config_main",
                    "artifact_type": "CONFIG",
                    "allowed_writers": ["governance_domain"],
                }
            ]
            registry_path = _create_artifact_registry(tmpdir, artifacts)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            detector = ShadowAuthorityDetector(
                artifact_registry_path=registry_path,
                ledger=ledger,
            )

            # Unregistered module shadow event
            detector.record_shadow_event(
                writing_module="unknown_module.py",
                target_artifact_id="config_main",
                declared_writers=["governance_domain"],
            )

            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 1
            assert entries[0].severity == "WARNING"

    def test_shadow_detector_works_without_ledger(self):
        """ShadowAuthorityDetector works without a ledger (backward compatible)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "report_daily",
                    "artifact_type": "REPORT_OUT",
                    "allowed_writers": ["report_engine"],
                }
            ]
            registry_path = _create_artifact_registry(tmpdir, artifacts)

            # No ledger provided
            detector = ShadowAuthorityDetector(
                artifact_registry_path=registry_path,
            )

            # Should work without error
            event = detector.record_shadow_event(
                writing_module="random_script.py",
                target_artifact_id="report_daily",
                declared_writers=["report_engine"],
            )

            assert event["writing_module"] == "random_script.py"
            assert event["target_artifact_id"] == "report_daily"

            # Observation report should still work
            report = detector.get_observation_report()
            assert report["unique_paths"] == 1

    def test_multiple_shadow_events_emit_multiple_ledger_entries(self):
        """Multiple shadow events produce multiple ledger entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts = [
                {
                    "artifact_id": "artifact_a",
                    "artifact_type": "CONFIG",
                    "allowed_writers": ["domain_a"],
                },
                {
                    "artifact_id": "artifact_b",
                    "artifact_type": "REPORT_OUT",
                    "allowed_writers": ["domain_b"],
                },
            ]
            registry_path = _create_artifact_registry(tmpdir, artifacts)
            ledger_path = os.path.join(tmpdir, "ledger.yaml")
            ledger = MutationAuditLedger(ledger_path)

            detector = ShadowAuthorityDetector(
                artifact_registry_path=registry_path,
                ledger=ledger,
            )

            # Record multiple shadow events
            detector.record_shadow_event(
                writing_module="module_x.py",
                target_artifact_id="artifact_a",
                declared_writers=["domain_a"],
            )
            detector.record_shadow_event(
                writing_module="module_y.py",
                target_artifact_id="artifact_b",
                declared_writers=["domain_b"],
            )

            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            assert len(entries) == 2
            assert entries[0].details["writing_module"] == "module_x.py"
            assert entries[1].details["writing_module"] == "module_y.py"
