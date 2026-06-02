"""Verification script for ledger append-only behavior and corruption recovery."""

import tempfile
import os
import uuid
import yaml
from datetime import datetime, timezone
from governance.mutation_audit_ledger import MutationAuditLedger, LedgerEntry


def test_append_only_behavior():
    """Verify entries only grow, never shrink."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger_path = os.path.join(tmpdir, "test_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        # Append 3 entries
        for i in range(3):
            entry = LedgerEntry(
                entry_id=str(uuid.uuid4()),
                event_type="REGISTRY_ADD",
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor={"actor_type": "SYSTEM", "actor_id": "test", "context": {}, "is_fallback": False},
                governance_policy_version="sha256:test",
                severity="INFO",
                details={"artifact_id": f"artifact_{i}"},
            )
            ledger.append(entry)

        with open(ledger_path, "r") as f:
            data = yaml.safe_load(f)
        assert len(data["entries"]) == 3, f"Expected 3 entries, got {len(data['entries'])}"

        # Append one more
        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="GOVERNANCE_EVENT",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={"actor_type": "CI", "actor_id": "test_ci", "context": {}, "is_fallback": False},
            governance_policy_version="sha256:test2",
            severity="WARNING",
            details={"action": "mode_change"},
        )
        ledger.append(entry)

        with open(ledger_path, "r") as f:
            data = yaml.safe_load(f)
        assert len(data["entries"]) == 4, f"Expected 4 entries, got {len(data['entries'])}"
        print("PASS: Append-only behavior verified (entries only grow, never shrink)")


def test_corruption_recovery():
    """Verify corruption recovery creates new ledger with recovery event."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger_path = os.path.join(tmpdir, "corrupt_ledger.yaml")

        # Write corrupt data
        with open(ledger_path, "w") as f:
            f.write("{{{{invalid yaml content not parseable")

        # Create ledger - should trigger corruption recovery
        ledger = MutationAuditLedger(ledger_path)

        # Verify recovery happened - ledger should be usable
        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="REGISTRY_ADD",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={"actor_type": "SYSTEM", "actor_id": "recovery_test", "context": {}, "is_fallback": False},
            governance_policy_version="sha256:recovered",
            severity="INFO",
            details={"test": "post_recovery"},
        )
        ledger.append(entry)

        with open(ledger_path, "r") as f:
            data = yaml.safe_load(f)
        # Should have recovery entry + our new entry
        assert len(data["entries"]) >= 2, f"Expected >= 2 entries after recovery, got {len(data['entries'])}"
        # First entry should be the corruption recovery event
        recovery = data["entries"][0]
        assert recovery["event_type"] == "GOVERNANCE_EVENT"
        assert recovery["details"]["action"] == "corruption_recovery"
        print("PASS: Corruption recovery verified (new ledger created with recovery event)")


def test_query_by_event_type():
    """Verify querying by event type works correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger_path = os.path.join(tmpdir, "query_ledger.yaml")
        ledger = MutationAuditLedger(ledger_path)

        for etype in ["REGISTRY_ADD", "GOVERNANCE_EVENT", "REGISTRY_ADD", "POLICY_CHANGE"]:
            entry = LedgerEntry(
                entry_id=str(uuid.uuid4()),
                event_type=etype,
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor={"actor_type": "SYSTEM", "actor_id": "test", "context": {}, "is_fallback": False},
                governance_policy_version="sha256:test",
                severity="INFO",
                details={},
            )
            ledger.append(entry)

        adds = ledger.query_by_event_type("REGISTRY_ADD")
        assert len(adds) == 2, f"Expected 2 REGISTRY_ADD entries, got {len(adds)}"
        print("PASS: Query by event type verified")


def test_cross_module_integration():
    """Verify policy_versioner and shadow_authority_detector import and integrate."""
    from governance.policy_versioner import PolicyVersioner
    from governance.shadow_authority_detector import ShadowAuthorityDetector

    # PolicyVersioner basic check
    pv = PolicyVersioner("/tmp")
    version = pv.compute_version()
    assert isinstance(version, str), "PolicyVersioner.compute_version() must return str"
    print(f"PASS: PolicyVersioner integration OK (version={version[:20]}...)")

    # ShadowAuthorityDetector basic check
    with tempfile.TemporaryDirectory() as tmpdir2:
        # Create a minimal artifact registry for the detector
        registry_path = os.path.join(tmpdir2, "artifact_registry.yaml")
        with open(registry_path, "w") as f:
            yaml.dump({"artifacts": {}}, f)
        sad = ShadowAuthorityDetector(registry_path)
        report = sad.get_observation_report()
        assert isinstance(report, dict), "ShadowAuthorityDetector.get_observation_report() must return dict"
        assert "unique_paths" in report, "Report must contain 'unique_paths'"
        print(f"PASS: ShadowAuthorityDetector integration OK (report={report})")


if __name__ == "__main__":
    test_append_only_behavior()
    test_corruption_recovery()
    test_query_by_event_type()
    test_cross_module_integration()
    print()
    print("ALL LEDGER INTEGRATION CHECKS PASSED")
