"""Audit Ledger Verification — Output Contract (Task 8).

Verification checks:
1. Ledger append-only behavior
2. Ledger corruption recovery
3. Policy Versioner determinism
4. Shadow Authority Detector observation-only
5. Cross-module integration

This is a VERIFICATION GATE — explicit evidence required.
"""

import os
import tempfile
import uuid
from datetime import datetime, timezone

import pytest
import yaml

from governance.mutation_audit_ledger import (
    LedgerEntry,
    MutationAuditLedger,
)
from governance.policy_versioner import PolicyVersioner
from governance.shadow_authority_detector import ShadowAuthorityDetector


# ---------------------------------------------------------------------------
# Verification Check 1: Ledger Append-Only Behavior
# ---------------------------------------------------------------------------


class TestLedgerAppendOnlyBehavior:
    """Verify ledger append-only behavior: entries are never overwritten."""

    def test_append_three_entries_all_exist(self, tmp_path):
        """Create a temp ledger, append 3 entries, verify all 3 exist."""
        ledger_path = str(tmp_path / "test_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        entries = []
        for i in range(3):
            entry = LedgerEntry(
                entry_id=str(uuid.uuid4()),
                event_type="REGISTRY_ADD",
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor={
                    "actor_type": "SYSTEM",
                    "actor_id": f"test_actor_{i}",
                    "context": {"test_index": i},
                    "is_fallback": False,
                },
                governance_policy_version=f"sha256:test_hash_{i}",
                severity="INFO",
                details={"artifact_id": f"artifact_{i}", "index": i},
            )
            entries.append(entry)
            ledger.append(entry)

        # Read back and verify all 3 exist
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert len(data["entries"]) == 3
        for i, stored in enumerate(data["entries"]):
            assert stored["entry_id"] == entries[i].entry_id
            assert stored["event_type"] == "REGISTRY_ADD"
            assert stored["details"]["index"] == i

    def test_entry_order_preserved(self, tmp_path):
        """Verify entry order is preserved (chronological append)."""
        ledger_path = str(tmp_path / "order_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        entry_ids = []
        for i in range(5):
            eid = f"entry-{i}-{uuid.uuid4()}"
            entry = LedgerEntry(
                entry_id=eid,
                event_type="GOVERNANCE_EVENT",
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor={
                    "actor_type": "SYSTEM",
                    "actor_id": "order_test",
                    "context": {},
                    "is_fallback": False,
                },
                governance_policy_version="sha256:order_test",
                severity="INFO",
                details={"sequence": i},
            )
            entry_ids.append(eid)
            ledger.append(entry)

        # Read back and verify order
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        stored_ids = [e["entry_id"] for e in data["entries"]]
        assert stored_ids == entry_ids

    def test_no_entries_overwritten(self, tmp_path):
        """Verify that appending new entries does not overwrite existing ones."""
        ledger_path = str(tmp_path / "overwrite_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        # Append first entry
        first_entry = LedgerEntry(
            entry_id="first-entry",
            event_type="REGISTRY_ADD",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "USER",
                "actor_id": "user1",
                "context": {},
                "is_fallback": False,
            },
            governance_policy_version="sha256:v1",
            severity="INFO",
            details={"msg": "first"},
        )
        ledger.append(first_entry)

        # Read and verify first entry
        with open(ledger_path, "r", encoding="utf-8") as f:
            data_after_first = yaml.safe_load(f)
        assert len(data_after_first["entries"]) == 1
        assert data_after_first["entries"][0]["entry_id"] == "first-entry"

        # Append second entry
        second_entry = LedgerEntry(
            entry_id="second-entry",
            event_type="REGISTRY_MODIFY",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "ENGINE",
                "actor_id": "engine1",
                "context": {},
                "is_fallback": False,
            },
            governance_policy_version="sha256:v2",
            severity="WARNING",
            details={"msg": "second"},
        )
        ledger.append(second_entry)

        # Verify first entry still intact, second appended
        with open(ledger_path, "r", encoding="utf-8") as f:
            data_after_second = yaml.safe_load(f)
        assert len(data_after_second["entries"]) == 2
        assert data_after_second["entries"][0]["entry_id"] == "first-entry"
        assert data_after_second["entries"][0]["details"]["msg"] == "first"
        assert data_after_second["entries"][1]["entry_id"] == "second-entry"


# ---------------------------------------------------------------------------
# Verification Check 2: Ledger Corruption Recovery
# ---------------------------------------------------------------------------


class TestLedgerCorruptionRecovery:
    """Verify ledger auto-recovers from corruption."""

    def test_corrupt_yaml_triggers_recovery(self, tmp_path):
        """Corrupt the ledger file, call read, verify auto-recovery."""
        ledger_path = str(tmp_path / "corrupt_ledger.yaml")

        # Create a valid ledger first
        ledger = MutationAuditLedger(ledger_path)
        entry = LedgerEntry(
            entry_id="pre-corruption-entry",
            event_type="REGISTRY_ADD",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "test",
                "context": {},
                "is_fallback": False,
            },
            governance_policy_version="sha256:pre",
            severity="INFO",
            details={"msg": "before corruption"},
        )
        ledger.append(entry)

        # Corrupt the file with invalid YAML
        with open(ledger_path, "w", encoding="utf-8") as f:
            f.write("{{{{invalid yaml content: [[[not parseable\n\x00\x01\x02")

        # Create a new ledger instance and trigger a read operation
        recovered_ledger = MutationAuditLedger(ledger_path)

        # The read should trigger recovery — query to force read
        events = recovered_ledger.query_by_event_type("GOVERNANCE_EVENT")

        # Verify recovery: new ledger created with recovery event
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "entries" in data
        assert len(data["entries"]) >= 1

        # Find the recovery event
        recovery_entries = [
            e
            for e in data["entries"]
            if e.get("details", {}).get("action") == "corruption_recovery"
        ]
        assert len(recovery_entries) >= 1, "Recovery event not found in ledger"

        recovery = recovery_entries[0]
        assert recovery["event_type"] == "GOVERNANCE_EVENT"
        assert recovery["severity"] == "WARNING"
        assert "corrupt" in recovery["details"].get("reason", "").lower()

    def test_recovery_creates_functional_ledger(self, tmp_path):
        """After recovery, the ledger is functional for new appends."""
        ledger_path = str(tmp_path / "recover_functional.yaml")

        # Create and corrupt
        ledger = MutationAuditLedger(ledger_path)
        with open(ledger_path, "w", encoding="utf-8") as f:
            f.write("not: [valid: yaml: {{broken")

        # Re-create (triggers recovery on read)
        recovered = MutationAuditLedger(ledger_path)

        # Append a new entry after recovery
        new_entry = LedgerEntry(
            entry_id="post-recovery-entry",
            event_type="REGISTRY_ADD",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "recovery_test",
                "context": {},
                "is_fallback": False,
            },
            governance_policy_version="sha256:recovered",
            severity="INFO",
            details={"msg": "after recovery"},
        )
        recovered.append(new_entry)

        # Verify the new entry exists
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        entry_ids = [e["entry_id"] for e in data["entries"]]
        assert "post-recovery-entry" in entry_ids


# ---------------------------------------------------------------------------
# Verification Check 3: Policy Versioner Determinism
# ---------------------------------------------------------------------------


class TestPolicyVersionerDeterminism:
    """Verify policy versioner produces deterministic, change-sensitive output."""

    def test_compute_version_twice_identical(self, tmp_path):
        """Compute version twice, verify identical."""
        # Create governance files
        dom_dir = tmp_path / ".domainization"
        dom_dir.mkdir()
        gov_dir = tmp_path / "governance"
        gov_dir.mkdir()

        (dom_dir / "config.yaml").write_text("mode: observability\n")
        (dom_dir / "lifecycle_state_machine.yaml").write_text("states: {}\n")
        (dom_dir / "domain_registry.yaml").write_text("domains: []\n")
        (gov_dir / "confidence_policy.yaml").write_text("policy: default\n")

        pv = PolicyVersioner(str(tmp_path))
        v1 = pv.compute_version()
        v2 = pv.compute_version()
        assert v1 == v2, f"Non-deterministic: {v1} != {v2}"

    def test_modify_file_changes_version(self, tmp_path):
        """Modify a governance file, verify version changes."""
        dom_dir = tmp_path / ".domainization"
        dom_dir.mkdir()
        gov_dir = tmp_path / "governance"
        gov_dir.mkdir()

        config_path = dom_dir / "config.yaml"
        config_path.write_text("mode: observability\n")
        (dom_dir / "lifecycle_state_machine.yaml").write_text("states: {}\n")
        (dom_dir / "domain_registry.yaml").write_text("domains: []\n")
        (gov_dir / "confidence_policy.yaml").write_text("policy: default\n")

        pv = PolicyVersioner(str(tmp_path))
        v_before = pv.compute_version()

        # Modify a governance file
        config_path.write_text("mode: hard\nenforcement: strict\n")

        v_after = pv.compute_version()
        assert v_before != v_after, "Version did not change after file modification"

    def test_restore_file_restores_version(self, tmp_path):
        """Restore file content, verify version returns to original."""
        dom_dir = tmp_path / ".domainization"
        dom_dir.mkdir()
        gov_dir = tmp_path / "governance"
        gov_dir.mkdir()

        config_path = dom_dir / "config.yaml"
        original_content = "mode: observability\n"
        config_path.write_text(original_content)
        (dom_dir / "lifecycle_state_machine.yaml").write_text("states: {}\n")
        (dom_dir / "domain_registry.yaml").write_text("domains: []\n")
        (gov_dir / "confidence_policy.yaml").write_text("policy: default\n")

        pv = PolicyVersioner(str(tmp_path))
        v_original = pv.compute_version()

        # Modify
        config_path.write_text("mode: hard\n")
        v_modified = pv.compute_version()
        assert v_original != v_modified

        # Restore
        config_path.write_text(original_content)
        v_restored = pv.compute_version()
        assert v_restored == v_original, (
            f"Version did not return to original after restore: "
            f"{v_restored} != {v_original}"
        )


# ---------------------------------------------------------------------------
# Verification Check 4: Shadow Authority Detector Observation-Only
# ---------------------------------------------------------------------------


class TestShadowAuthorityDetectorObservationOnly:
    """Verify the detector is observation-only per CTO directive."""

    def test_no_check_threshold_method(self):
        """Verify the detector has NO check_threshold() method."""
        assert not hasattr(ShadowAuthorityDetector, "check_threshold"), (
            "CTO DIRECTIVE VIOLATION: ShadowAuthorityDetector must NOT have "
            "check_threshold() method"
        )

    def test_get_observation_report_returns_structured_data(self, tmp_path):
        """Verify get_observation_report() returns structured data."""
        # Create a minimal artifact registry
        registry_path = tmp_path / "artifact_registry.yaml"
        registry_path.write_text(
            yaml.dump(
                {
                    "artifacts": [
                        {
                            "artifact_id": "test_artifact",
                            "allowed_writers": ["authorized_module"],
                        }
                    ]
                }
            )
        )

        detector = ShadowAuthorityDetector(str(registry_path))
        report = detector.get_observation_report()

        # Verify structured data
        assert isinstance(report, dict)
        assert "unique_paths" in report
        assert "undeclared_writers" in report
        assert "severity_recommendation" in report
        assert isinstance(report["unique_paths"], int)
        assert isinstance(report["undeclared_writers"], list)
        assert isinstance(report["severity_recommendation"], str)

    def test_severity_recommendation_is_advisory_string(self, tmp_path):
        """Verify severity_recommendation is an advisory string, not a decision."""
        registry_path = tmp_path / "artifact_registry.yaml"
        registry_path.write_text(
            yaml.dump(
                {
                    "artifacts": [
                        {
                            "artifact_id": "art1",
                            "allowed_writers": ["module_a"],
                        }
                    ]
                }
            )
        )

        detector = ShadowAuthorityDetector(str(registry_path))

        # Record some shadow events
        detector.record_shadow_event("rogue_module", "art1", ["module_a"])

        report = detector.get_observation_report()
        severity = report["severity_recommendation"]

        # Must be a string
        assert isinstance(severity, str)
        # Must be one of the advisory levels (not CRITICAL)
        assert severity in ("info", "warning", "elevated"), (
            f"severity_recommendation '{severity}' is not a valid advisory level"
        )
        # Must NOT be CRITICAL (CTO directive)
        assert severity.upper() != "CRITICAL", (
            "CTO DIRECTIVE VIOLATION: severity_recommendation must NOT be CRITICAL"
        )

    def test_detector_does_not_block_on_any_input(self, tmp_path):
        """Verify the detector does NOT block or raise on any input."""
        registry_path = tmp_path / "artifact_registry.yaml"
        registry_path.write_text(
            yaml.dump(
                {
                    "artifacts": [
                        {
                            "artifact_id": "protected_artifact",
                            "allowed_writers": ["only_this_module"],
                        }
                    ]
                }
            )
        )

        detector = ShadowAuthorityDetector(str(registry_path))

        # Try many unauthorized writes — none should raise or block
        for i in range(20):
            # check_write_authority should return a boolean, never raise
            result = detector.check_write_authority(
                f"unauthorized_module_{i}", "protected_artifact"
            )
            assert isinstance(result, bool)

            # record_shadow_event should return a dict, never raise
            event = detector.record_shadow_event(
                f"unauthorized_module_{i}",
                "protected_artifact",
                ["only_this_module"],
            )
            assert isinstance(event, dict)

        # get_observation_report should still work without blocking
        report = detector.get_observation_report()
        assert isinstance(report, dict)
        assert report["unique_paths"] == 20

    def test_no_critical_classification(self, tmp_path):
        """Verify detector never classifies anything as CRITICAL."""
        registry_path = tmp_path / "artifact_registry.yaml"
        registry_path.write_text(
            yaml.dump(
                {
                    "artifacts": [
                        {
                            "artifact_id": f"art_{i}",
                            "allowed_writers": ["legit"],
                        }
                        for i in range(10)
                    ]
                }
            )
        )

        detector = ShadowAuthorityDetector(str(registry_path))

        # Record many shadow events (exceeding any threshold)
        for i in range(10):
            detector.record_shadow_event(
                f"rogue_{i}", f"art_{i}", ["legit"]
            )

        report = detector.get_observation_report()
        assert report["severity_recommendation"] != "critical"
        assert report["severity_recommendation"].upper() != "CRITICAL"


# ---------------------------------------------------------------------------
# Verification Check 5: Cross-Module Integration
# ---------------------------------------------------------------------------


class TestCrossModuleIntegration:
    """Verify MutationAuditLedger integrates with PolicyVersioner and ShadowAuthorityDetector."""

    def test_ledger_stores_policy_version_entries(self, tmp_path):
        """Verify ledger can store entries with embedded policy version."""
        ledger_path = str(tmp_path / "integration_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        # Create a policy versioner
        dom_dir = tmp_path / ".domainization"
        dom_dir.mkdir()
        gov_dir = tmp_path / "governance"
        gov_dir.mkdir()
        (dom_dir / "config.yaml").write_text("mode: observability\n")
        (dom_dir / "lifecycle_state_machine.yaml").write_text("states: {}\n")
        (dom_dir / "domain_registry.yaml").write_text("domains: []\n")
        (gov_dir / "confidence_policy.yaml").write_text("policy: default\n")

        pv = PolicyVersioner(str(tmp_path))
        policy_version = pv.compute_version()

        # Create a ledger entry with the policy version embedded
        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="POLICY_CHANGE",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "policy_versioner",
                "context": {"action": "version_check"},
                "is_fallback": False,
            },
            governance_policy_version=policy_version,
            severity="INFO",
            details={
                "action": "policy_version_computed",
                "version": policy_version,
            },
        )
        ledger.append(entry)

        # Verify the entry is stored with correct policy version
        results = ledger.query_by_event_type("POLICY_CHANGE")
        assert len(results) == 1
        assert results[0].governance_policy_version == policy_version
        assert results[0].governance_policy_version.startswith("sha256:")

    def test_ledger_stores_shadow_events(self, tmp_path):
        """Verify ledger can store shadow authority events."""
        ledger_path = str(tmp_path / "shadow_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        # Create shadow authority detector
        registry_path = tmp_path / "artifact_registry.yaml"
        registry_path.write_text(
            yaml.dump(
                {
                    "artifacts": [
                        {
                            "artifact_id": "protected_art",
                            "allowed_writers": ["authorized_only"],
                        }
                    ]
                }
            )
        )

        detector = ShadowAuthorityDetector(str(registry_path))

        # Record a shadow event
        shadow_event = detector.record_shadow_event(
            "rogue_module", "protected_art", ["authorized_only"]
        )

        # Store the shadow event in the ledger
        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="GOVERNANCE_EVENT",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "RUNTIME",
                "actor_id": "shadow_authority_detector",
                "context": {"action": "shadow_detection"},
                "is_fallback": False,
            },
            governance_policy_version="sha256:integration_test",
            severity="WARNING",
            details={
                "shadow_event": shadow_event,
                "writing_module": shadow_event["writing_module"],
                "target_artifact_id": shadow_event["target_artifact_id"],
                "authority_type": shadow_event["authority_type"],
            },
        )
        ledger.append(entry)

        # Verify the shadow event is stored in the ledger
        results = ledger.query_by_event_type("GOVERNANCE_EVENT")
        assert len(results) >= 1

        shadow_entries = [
            e
            for e in results
            if e.details.get("writing_module") == "rogue_module"
        ]
        assert len(shadow_entries) == 1
        assert shadow_entries[0].details["target_artifact_id"] == "protected_art"
        assert shadow_entries[0].details["authority_type"] == "unregistered_module_shadow"

    def test_all_modules_import_cleanly(self):
        """Verify all three modules import without errors."""
        # These imports should not raise
        from governance.mutation_audit_ledger import (
            MutationAuditLedger,
            LedgerEntry,
            EVENT_TYPES,
            LEDGER_SCHEMA_VERSION,
        )
        from governance.policy_versioner import PolicyVersioner
        from governance.shadow_authority_detector import ShadowAuthorityDetector

        # Verify key attributes exist
        assert hasattr(MutationAuditLedger, "append")
        assert hasattr(MutationAuditLedger, "query_by_time_range")
        assert hasattr(MutationAuditLedger, "query_by_event_type")
        assert hasattr(MutationAuditLedger, "recover_from_corruption")
        assert hasattr(PolicyVersioner, "compute_version")
        assert hasattr(PolicyVersioner, "detect_change")
        assert hasattr(PolicyVersioner, "get_current_version")
        assert hasattr(ShadowAuthorityDetector, "check_write_authority")
        assert hasattr(ShadowAuthorityDetector, "record_shadow_event")
        assert hasattr(ShadowAuthorityDetector, "get_observation_report")


# ---------------------------------------------------------------------------
# Verification Check 6: Cross-Module LedgerEntry Compatibility
# ---------------------------------------------------------------------------


class TestCrossModuleLedgerEntryCompatibility:
    """Verify LedgerEntry from mutation_audit_ledger.py is compatible with cold_start_handler.py."""

    def test_same_fields(self):
        """Verify both LedgerEntry classes have the same fields."""
        from governance.mutation_audit_ledger import LedgerEntry as CanonicalLedgerEntry
        from governance.cold_start_handler import LedgerEntry as ColdStartLedgerEntry

        import dataclasses

        canonical_fields = {f.name for f in dataclasses.fields(CanonicalLedgerEntry)}
        cold_start_fields = {f.name for f in dataclasses.fields(ColdStartLedgerEntry)}

        assert canonical_fields == cold_start_fields, (
            f"Field mismatch between LedgerEntry implementations:\n"
            f"  Canonical: {sorted(canonical_fields)}\n"
            f"  ColdStart: {sorted(cold_start_fields)}\n"
            f"  Missing in ColdStart: {canonical_fields - cold_start_fields}\n"
            f"  Extra in ColdStart: {cold_start_fields - canonical_fields}"
        )

    def test_to_dict_interface_compatible(self):
        """Verify both LedgerEntry classes produce identical to_dict() output."""
        from governance.mutation_audit_ledger import LedgerEntry as CanonicalLedgerEntry
        from governance.cold_start_handler import LedgerEntry as ColdStartLedgerEntry

        test_data = {
            "entry_id": "test-compat-id",
            "event_type": "GOVERNANCE_EVENT",
            "timestamp": "2026-05-29T10:00:00+00:00",
            "actor": {
                "actor_type": "SYSTEM",
                "actor_id": "test",
                "context": {"key": "value"},
                "is_fallback": False,
            },
            "governance_policy_version": "sha256:abc123",
            "severity": "INFO",
            "details": {"action": "test_action", "result": "success"},
        }

        canonical = CanonicalLedgerEntry(**test_data)
        cold_start = ColdStartLedgerEntry(**test_data)

        assert canonical.to_dict() == cold_start.to_dict(), (
            "to_dict() output differs between LedgerEntry implementations"
        )

    def test_from_dict_interface_compatible(self):
        """Verify both LedgerEntry classes can deserialize from the same dict."""
        from governance.mutation_audit_ledger import LedgerEntry as CanonicalLedgerEntry
        from governance.cold_start_handler import LedgerEntry as ColdStartLedgerEntry

        test_dict = {
            "entry_id": "test-from-dict-id",
            "event_type": "POLICY_CHANGE",
            "timestamp": "2026-05-29T11:00:00+00:00",
            "actor": {
                "actor_type": "CI",
                "actor_id": "workflow-123",
                "context": {"run_id": "abc"},
                "is_fallback": False,
            },
            "governance_policy_version": "sha256:def456",
            "severity": "WARNING",
            "details": {"previous_mode": "observability", "new_mode": "soft"},
        }

        canonical = CanonicalLedgerEntry.from_dict(test_dict)
        cold_start = ColdStartLedgerEntry.from_dict(test_dict)

        # Both should produce the same to_dict output
        assert canonical.to_dict() == cold_start.to_dict(), (
            "from_dict() produces different results between implementations"
        )

    def test_cross_serialization_roundtrip(self):
        """Verify an entry created by one can be deserialized by the other."""
        from governance.mutation_audit_ledger import LedgerEntry as CanonicalLedgerEntry
        from governance.cold_start_handler import LedgerEntry as ColdStartLedgerEntry

        # Create with ColdStart, deserialize with Canonical
        cold_start_entry = ColdStartLedgerEntry(
            entry_id="cross-compat-test",
            event_type="GOVERNANCE_EVENT",
            timestamp="2026-05-29T12:00:00+00:00",
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "cold_start_handler",
                "context": {"action": "cold_start_initialization"},
                "is_fallback": False,
            },
            governance_policy_version="bootstrap",
            severity="INFO",
            details={"action": "cold_start_initialization"},
        )

        serialized = cold_start_entry.to_dict()
        canonical_deserialized = CanonicalLedgerEntry.from_dict(serialized)

        assert canonical_deserialized.entry_id == cold_start_entry.entry_id
        assert canonical_deserialized.event_type == cold_start_entry.event_type
        assert canonical_deserialized.timestamp == cold_start_entry.timestamp
        assert canonical_deserialized.actor == cold_start_entry.actor
        assert canonical_deserialized.governance_policy_version == cold_start_entry.governance_policy_version
        assert canonical_deserialized.severity == cold_start_entry.severity
        assert canonical_deserialized.details == cold_start_entry.details
