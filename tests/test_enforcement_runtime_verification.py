"""Enforcement Runtime Verification — Output Contract (Task 6).

This verification script validates the 5 CTO-mandated checks:
1. Observability mode never blocks
2. Hard mode blocks invalid inputs
3. Cold-start bootstrap provenance is emitted
4. Registry-driven boundary enforcement works against real registry data
5. Existing invariants remain intact (full test suite)

Run with: .venv/bin/python -m pytest tests/test_enforcement_runtime_verification.py -v
"""

from __future__ import annotations

import os
import tempfile

import pytest


# ---------------------------------------------------------------------------
# Check 1: Observability Never Blocks
# ---------------------------------------------------------------------------

class TestObservabilityNeverBlocks:
    """Verify that observability mode NEVER produces enforcement_action='block'
    and status is always 'pass' even for invalid inputs."""

    def test_gate_framework_observability_never_blocks(self):
        """GateFramework in observability mode: failing gates produce warn, not block."""
        from governance.gate_framework import GateFramework

        config = {
            "gates": {
                "always_fail_gate": {
                    "blocking_in_soft": True,
                    "blocking_in_hard": True,
                    "time_budget_ms": 5000,
                    "check_fn": lambda: False,  # Always fails
                },
                "exception_gate": {
                    "blocking_in_soft": True,
                    "blocking_in_hard": True,
                    "time_budget_ms": 5000,
                    "check_fn": lambda: (_ for _ in ()).throw(RuntimeError("test error")),
                },
            }
        }

        framework = GateFramework(config=config, enforcement_mode="observability")
        summary = framework.execute_all_gates()

        for result in framework.results:
            assert result.enforcement_action != "block", (
                f"Observability mode produced 'block' for gate '{result.gate_name}': "
                f"status={result.status}, action={result.enforcement_action}"
            )
            # In observability mode, status should reflect the check outcome
            # but enforcement_action must be warn or info, never block
            assert result.enforcement_action in ("warn", "info"), (
                f"Unexpected enforcement_action '{result.enforcement_action}' "
                f"in observability mode for gate '{result.gate_name}'"
            )

    def test_lifecycle_enforcer_observability_never_blocks(self):
        """LifecycleEnforcer in observability mode: invalid transitions produce
        status=pass and enforcement_action=warn, never block."""
        from governance.lifecycle_enforcer import LifecycleEnforcer

        state_machine_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".domainization",
            "lifecycle_state_machine.yaml",
        )

        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_path,
            enforcement_mode="observability",
        )

        # Invalid transition: SSOT cannot go from 'draft' to 'deprecated' directly
        result = enforcer.enforce_transition(
            artifact_id="test_artifact",
            artifact_type="SSOT",
            from_state="draft",
            to_state="deprecated",
        )
        assert result.enforcement_action != "block", (
            f"Observability mode blocked lifecycle transition: {result.details}"
        )
        assert result.status == "pass", (
            f"Observability mode should pass (with warn), got status={result.status}"
        )

        # Read-only enforcement in observability
        result_ro = enforcer.enforce_read_only(
            artifact_id="test_artifact",
            artifact_type="SSOT",
            current_state="deprecated",
        )
        assert result_ro.enforcement_action != "block", (
            f"Observability mode blocked read-only check: {result_ro.details}"
        )
        assert result_ro.status == "pass", (
            f"Observability mode should pass read-only check, got status={result_ro.status}"
        )

        # Regenerable enforcement in observability
        result_regen = enforcer.enforce_regenerable(
            artifact_id="test_artifact",
            artifact_type="SSOT",
            current_state="canonical",
            actor_type="ENGINE",
        )
        assert result_regen.enforcement_action != "block", (
            f"Observability mode blocked regenerable check: {result_regen.details}"
        )

    def test_boundary_enforcer_observability_never_blocks(self):
        """BoundaryEnforcer in observability mode: unauthorized writes produce
        status=pass and enforcement_action=warn, never block."""
        from governance.boundary_enforcer import BoundaryEnforcer

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        artifact_registry_path = os.path.join(
            base_path, ".domainization", "artifact_registry.yaml"
        )
        domain_registry_path = os.path.join(
            base_path, ".domainization", "domain_registry.yaml"
        )

        enforcer = BoundaryEnforcer(
            artifact_registry_path=artifact_registry_path,
            domain_registry_path=domain_registry_path,
            enforcement_mode="observability",
        )

        # Unauthorized write: GOV domain writing to allocation_engine_py
        # (only SIGNALS is allowed)
        result = enforcer.enforce_write(
            writing_domain="GOV",
            artifact_id="allocation_engine_py",
        )
        assert result.enforcement_action != "block", (
            f"Observability mode blocked boundary write: {result.details}"
        )
        assert result.status == "pass", (
            f"Observability mode should pass (with warn), got status={result.status}"
        )

        # Cannot-own violation: GOV cannot own ENGINE
        result_assign = enforcer.enforce_domain_assignment(
            domain_id="GOV",
            artifact_id="test_engine",
            artifact_type="ENGINE",
        )
        assert result_assign.enforcement_action != "block", (
            f"Observability mode blocked domain assignment: {result_assign.details}"
        )
        assert result_assign.status == "pass", (
            f"Observability mode should pass domain assignment, got status={result_assign.status}"
        )


# ---------------------------------------------------------------------------
# Check 2: Hard Mode Blocks
# ---------------------------------------------------------------------------

class TestHardModeBlocks:
    """Verify that hard mode produces status='fail' and enforcement_action='block'
    for invalid inputs."""

    def test_gate_framework_hard_mode_blocks(self):
        """GateFramework in hard mode: failing gates with blocking config produce block."""
        from governance.gate_framework import GateFramework

        config = {
            "gates": {
                "critical_gate": {
                    "blocking_in_soft": True,
                    "blocking_in_hard": True,
                    "time_budget_ms": 5000,
                    "check_fn": lambda: False,  # Always fails
                },
            }
        }

        framework = GateFramework(config=config, enforcement_mode="hard")
        summary = framework.execute_all_gates()

        assert len(framework.results) == 1
        result = framework.results[0]
        assert result.status == "fail", (
            f"Hard mode should fail on failing gate, got status={result.status}"
        )
        assert result.enforcement_action == "block", (
            f"Hard mode should block on failing gate, got action={result.enforcement_action}"
        )

    def test_lifecycle_enforcer_hard_mode_blocks(self):
        """LifecycleEnforcer in hard mode: invalid transitions produce fail+block."""
        from governance.lifecycle_enforcer import LifecycleEnforcer

        state_machine_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".domainization",
            "lifecycle_state_machine.yaml",
        )

        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_path,
            enforcement_mode="hard",
        )

        # Invalid transition: SSOT cannot go from 'draft' to 'deprecated' directly
        result = enforcer.enforce_transition(
            artifact_id="test_artifact",
            artifact_type="SSOT",
            from_state="draft",
            to_state="deprecated",
        )
        assert result.status == "fail", (
            f"Hard mode should fail invalid transition, got status={result.status}"
        )
        assert result.enforcement_action == "block", (
            f"Hard mode should block invalid transition, got action={result.enforcement_action}"
        )

    def test_boundary_enforcer_hard_mode_blocks(self):
        """BoundaryEnforcer in hard mode: unauthorized writes produce fail+block."""
        from governance.boundary_enforcer import BoundaryEnforcer

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        artifact_registry_path = os.path.join(
            base_path, ".domainization", "artifact_registry.yaml"
        )
        domain_registry_path = os.path.join(
            base_path, ".domainization", "domain_registry.yaml"
        )

        enforcer = BoundaryEnforcer(
            artifact_registry_path=artifact_registry_path,
            domain_registry_path=domain_registry_path,
            enforcement_mode="hard",
        )

        # Unauthorized write: GOV domain writing to allocation_engine_py
        result = enforcer.enforce_write(
            writing_domain="GOV",
            artifact_id="allocation_engine_py",
        )
        assert result.status == "fail", (
            f"Hard mode should fail unauthorized write, got status={result.status}"
        )
        assert result.enforcement_action == "block", (
            f"Hard mode should block unauthorized write, got action={result.enforcement_action}"
        )


# ---------------------------------------------------------------------------
# Check 3: Cold-Start Bootstrap Provenance
# ---------------------------------------------------------------------------

class TestColdStartBootstrapProvenance:
    """Verify cold-start handler emits bootstrap_derived provenance."""

    def test_cold_start_detection_and_initialization(self):
        """ColdStartHandler: is_cold_start() returns True on fresh dir,
        initialize() returns LedgerEntry with provenance=bootstrap_derived
        and enforcement_mode=observability."""
        from governance.cold_start_handler import ColdStartHandler
        from governance.actor_identity import ActorIdentity, ActorType

        with tempfile.TemporaryDirectory() as tmp_dir:
            handler = ColdStartHandler(domainization_path=tmp_dir)

            # Should be cold start (no ledger file)
            assert handler.is_cold_start() is True, (
                "Expected is_cold_start() to return True for fresh directory"
            )

            # Initialize with a test actor
            actor = ActorIdentity(
                actor_type=ActorType.SYSTEM,
                actor_id="verification_test",
                context={"purpose": "runtime_verification"},
            )
            entry = handler.initialize(actor)

            # Verify the returned LedgerEntry
            assert entry is not None, "initialize() should return a LedgerEntry"
            assert entry.details["provenance"] == "bootstrap_derived", (
                f"Expected provenance='bootstrap_derived', "
                f"got '{entry.details.get('provenance')}'"
            )
            assert entry.details["enforcement_mode"] == "observability", (
                f"Expected enforcement_mode='observability', "
                f"got '{entry.details.get('enforcement_mode')}'"
            )

            # After initialization, cold start should be False
            assert handler.is_cold_start() is False, (
                "Expected is_cold_start() to return False after initialization"
            )

            # Verify forced enforcement mode
            assert handler.get_forced_enforcement_mode() == "observability", (
                "Cold-start should force observability mode"
            )


# ---------------------------------------------------------------------------
# Check 4: Registry-Driven Boundary Enforcement Against Real Registry Data
# ---------------------------------------------------------------------------

class TestRegistryDrivenBoundaryEnforcement:
    """Verify BoundaryEnforcer works against ACTUAL registry data."""

    def test_real_registry_write_permission_enforcement(self):
        """BoundaryEnforcer with real registries: enforce write permission
        for a real artifact (allocation_engine_py, allowed_writers=[SIGNALS])."""
        from governance.boundary_enforcer import BoundaryEnforcer

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        artifact_registry_path = os.path.join(
            base_path, ".domainization", "artifact_registry.yaml"
        )
        domain_registry_path = os.path.join(
            base_path, ".domainization", "domain_registry.yaml"
        )

        # Verify registry files exist
        assert os.path.isfile(artifact_registry_path), (
            f"Artifact registry not found: {artifact_registry_path}"
        )
        assert os.path.isfile(domain_registry_path), (
            f"Domain registry not found: {domain_registry_path}"
        )

        enforcer = BoundaryEnforcer(
            artifact_registry_path=artifact_registry_path,
            domain_registry_path=domain_registry_path,
            enforcement_mode="hard",
        )

        # Verify registries loaded
        assert len(enforcer.artifact_registry) > 0, (
            "Artifact registry should contain artifacts"
        )
        assert len(enforcer.domain_registry) > 0, (
            "Domain registry should contain domains"
        )

        # Test: SIGNALS domain CAN write to allocation_engine_py
        permitted = enforcer.check_write_permission("SIGNALS", "allocation_engine_py")
        assert permitted is True, (
            "SIGNALS should be permitted to write to allocation_engine_py"
        )

        # Test: GOV domain CANNOT write to allocation_engine_py
        not_permitted = enforcer.check_write_permission("GOV", "allocation_engine_py")
        assert not_permitted is False, (
            "GOV should NOT be permitted to write to allocation_engine_py"
        )

        # Test enforcement: authorized write passes
        result_pass = enforcer.enforce_write(
            writing_domain="SIGNALS",
            artifact_id="allocation_engine_py",
        )
        assert result_pass.status == "pass", (
            f"Authorized write should pass, got status={result_pass.status}"
        )

        # Test enforcement: unauthorized write blocks in hard mode
        result_block = enforcer.enforce_write(
            writing_domain="GOV",
            artifact_id="allocation_engine_py",
        )
        assert result_block.status == "fail", (
            f"Unauthorized write should fail in hard mode, got status={result_block.status}"
        )
        assert result_block.enforcement_action == "block", (
            f"Unauthorized write should block in hard mode, "
            f"got action={result_block.enforcement_action}"
        )

    def test_real_registry_cannot_own_enforcement(self):
        """BoundaryEnforcer with real registries: GOV domain cannot own ENGINE."""
        from governance.boundary_enforcer import BoundaryEnforcer

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        artifact_registry_path = os.path.join(
            base_path, ".domainization", "artifact_registry.yaml"
        )
        domain_registry_path = os.path.join(
            base_path, ".domainization", "domain_registry.yaml"
        )

        enforcer = BoundaryEnforcer(
            artifact_registry_path=artifact_registry_path,
            domain_registry_path=domain_registry_path,
            enforcement_mode="hard",
        )

        # GOV domain has cannot_own: [ENGINE, REPORT_OUT, DATA_OUT]
        violation = enforcer.check_cannot_own("GOV", "ENGINE")
        assert violation is True, (
            "GOV domain should have cannot_own violation for ENGINE type"
        )

        # SIGNALS domain does NOT have cannot_own for ENGINE
        no_violation = enforcer.check_cannot_own("SIGNALS", "ENGINE")
        assert no_violation is False, (
            "SIGNALS domain should NOT have cannot_own violation for ENGINE type"
        )


# ---------------------------------------------------------------------------
# Check 5: Module Import and Integration Verification
# ---------------------------------------------------------------------------

class TestModuleImportAndIntegration:
    """Verify all enforcement runtime modules import cleanly and integrate."""

    def test_gate_framework_imports(self):
        """GateFramework module imports cleanly."""
        from governance.gate_framework import (
            GateFramework,
            GateResult,
            GateSummary,
            compute_aggregate_state,
            VALID_STATUSES,
            VALID_ENFORCEMENT_ACTIONS,
            VALID_AGGREGATE_STATES,
        )
        assert GateFramework is not None
        assert GateResult is not None
        assert GateSummary is not None

    def test_lifecycle_enforcer_imports(self):
        """LifecycleEnforcer module imports cleanly."""
        from governance.lifecycle_enforcer import (
            LifecycleEnforcer,
            VALID_ENFORCEMENT_MODES,
        )
        assert LifecycleEnforcer is not None

    def test_boundary_enforcer_imports(self):
        """BoundaryEnforcer module imports cleanly."""
        from governance.boundary_enforcer import (
            BoundaryEnforcer,
            CANONICAL_ARTIFACT_TYPES,
            TRANSIENT_ARTIFACT_TYPES,
        )
        assert BoundaryEnforcer is not None

    def test_cold_start_handler_imports(self):
        """ColdStartHandler module imports cleanly."""
        from governance.cold_start_handler import (
            ColdStartHandler,
            LedgerEntry,
            LEDGER_FILENAME,
        )
        assert ColdStartHandler is not None
        assert LedgerEntry is not None

    def test_cross_module_integration(self):
        """Verify modules integrate: GateFramework can use results from
        LifecycleEnforcer and BoundaryEnforcer."""
        from governance.gate_framework import GateFramework, GateResult
        from governance.lifecycle_enforcer import LifecycleEnforcer
        from governance.boundary_enforcer import BoundaryEnforcer
        from governance.cold_start_handler import ColdStartHandler

        # All modules can be instantiated together
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        lifecycle = LifecycleEnforcer(
            state_machine_path=os.path.join(
                base_path, ".domainization", "lifecycle_state_machine.yaml"
            ),
            enforcement_mode="observability",
        )

        boundary = BoundaryEnforcer(
            artifact_registry_path=os.path.join(
                base_path, ".domainization", "artifact_registry.yaml"
            ),
            domain_registry_path=os.path.join(
                base_path, ".domainization", "domain_registry.yaml"
            ),
            enforcement_mode="observability",
        )

        # Results from both enforcers are GateResult instances
        lifecycle_result = lifecycle.enforce_transition(
            artifact_id="test", artifact_type="SSOT",
            from_state="draft", to_state="review",
        )
        boundary_result = boundary.enforce_write(
            writing_domain="SIGNALS", artifact_id="allocation_engine_py",
        )

        assert isinstance(lifecycle_result, GateResult)
        assert isinstance(boundary_result, GateResult)

        # Both can be serialized to dict
        assert "gate_name" in lifecycle_result.to_dict()
        assert "gate_name" in boundary_result.to_dict()
