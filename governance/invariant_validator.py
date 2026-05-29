"""Runtime Invariant Preservation Validator.

Validates runtime-owned invariants (INV-3, INV-4, INV-5, INV-7, INV-8) to ensure
the governance enforcement system preserves foundational guarantees. This module
validates ONLY runtime-owned invariants. Domainization-owned invariants (INV-1,
INV-2, INV-6, INV-9, INV-10) are validated elsewhere.

Wires into the gate framework as a validation gate via `as_gate_check_fn()`.

Requirements: 25.3, 25.4, 25.5, 25.7, 25.8
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from governance.gate_framework import GateResult


# Expected chain model ordering: SIGNALS(L1) -> SEMANTICS(L2) -> REASONING(L3) -> REPORT(L4)
EXPECTED_CHAIN_MODEL = [
    ("SIGNALS", 1),
    ("SEMANTICS", 2),
    ("REASONING", 3),
    ("REPORT", 4),
]

# Expected severity ordering (strictly increasing IntEnum values)
EXPECTED_SEVERITY_ORDER = [
    "INFO",
    "WARNING",
    "DEGRADED",
    "CRITICAL",
    "CANONICAL_BREAK",
    "DETERMINISTIC_FAILURE",
]


@dataclass
class InvariantCheckResult:
    """Result of a single invariant check.

    Attributes:
        invariant_id: Identifier (e.g., "INV-3").
        passed: Whether the invariant holds.
        details: Human-readable description of the check outcome.
    """

    invariant_id: str
    passed: bool
    details: str


@dataclass
class InvariantValidationSummary:
    """Summary of all invariant checks.

    Attributes:
        results: List of individual invariant check results.
        all_passed: True if every invariant check passed.
        timestamp: ISO 8601 timestamp of validation.
    """

    results: list[InvariantCheckResult] = field(default_factory=list)
    all_passed: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add(self, result: InvariantCheckResult) -> None:
        """Add a check result and update all_passed."""
        self.results.append(result)
        if not result.passed:
            self.all_passed = False


class RuntimeInvariantValidator:
    """Validates runtime-owned invariants for preservation.

    Runtime-owned invariants:
        INV-3: Chain_Model is SIGNALS(L1)->SEMANTICS(L2)->REASONING(L3)->REPORT(L4)
        INV-4: Severity levels strictly ordered
        INV-5: Runtime states belong to orthogonal integrity dimensions
        INV-7: Pipeline execution completes (degraded output preferred over no output)
        INV-8: Observability mode never blocks commits or pipeline execution

    Domainization-owned invariants NOT validated here:
        INV-1, INV-2, INV-6, INV-9, INV-10

    Usage as a gate:
        validator = RuntimeInvariantValidator(enforcement_mode="observability")
        gate_result = validator.validate_all()

    Usage with GateFramework:
        config = {
            "gates": {
                "runtime_invariant_preservation": {
                    "blocking_in_soft": True,
                    "blocking_in_hard": True,
                    "time_budget_ms": 5000,
                    "check_fn": validator.as_gate_check_fn(),
                }
            }
        }
    """

    GATE_NAME = "runtime_invariant_preservation"

    def __init__(self, enforcement_mode: str = "observability") -> None:
        """Initialize the invariant validator.

        Args:
            enforcement_mode: One of "observability", "soft", or "hard".
        """
        self._enforcement_mode = enforcement_mode

    @property
    def enforcement_mode(self) -> str:
        """Current enforcement mode."""
        return self._enforcement_mode

    def _check_chain_model(self) -> InvariantCheckResult:
        """INV-3: Verify Chain_Model is SIGNALS(L1)->SEMANTICS(L2)->REASONING(L3)->REPORT(L4).

        Imports the domain registry YAML and verifies that core reasoning chain
        domains have the correct authority levels in the correct order.
        """
        try:
            import yaml
            import os

            # Find domain_registry.yaml relative to project root
            base_paths = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             ".domainization", "domain_registry.yaml"),
            ]

            registry_path = None
            for path in base_paths:
                if os.path.exists(path):
                    registry_path = path
                    break

            if registry_path is None:
                return InvariantCheckResult(
                    invariant_id="INV-3",
                    passed=False,
                    details="Cannot locate domain_registry.yaml to verify chain model",
                )

            with open(registry_path, "r") as f:
                registry = yaml.safe_load(f)

            domains = registry.get("domains", [])

            # Extract core reasoning chain domains with authority levels
            chain_domains: list[tuple[str, int]] = []
            for domain in domains:
                authority_level = domain.get("authority_level")
                if authority_level is not None:
                    chain_domains.append((domain["domain_id"], int(authority_level)))

            # Sort by authority level
            chain_domains.sort(key=lambda x: x[1])

            if chain_domains == EXPECTED_CHAIN_MODEL:
                return InvariantCheckResult(
                    invariant_id="INV-3",
                    passed=True,
                    details="Chain model preserved: SIGNALS(L1)->SEMANTICS(L2)->REASONING(L3)->REPORT(L4)",
                )
            else:
                return InvariantCheckResult(
                    invariant_id="INV-3",
                    passed=False,
                    details=(
                        f"Chain model violated. Expected {EXPECTED_CHAIN_MODEL}, "
                        f"got {chain_domains}"
                    ),
                )

        except Exception as exc:
            return InvariantCheckResult(
                invariant_id="INV-3",
                passed=False,
                details=f"Chain model check failed with exception: {type(exc).__name__}: {exc}",
            )

    def _check_severity_ordering(self) -> InvariantCheckResult:
        """INV-4: Verify severity levels are strictly ordered.

        Expected: INFO < WARNING < DEGRADED < CRITICAL < CANONICAL_BREAK < DETERMINISTIC_FAILURE
        """
        try:
            from runtime.severity_taxonomy import Severity

            # Verify all expected levels exist
            for level_name in EXPECTED_SEVERITY_ORDER:
                if not hasattr(Severity, level_name):
                    return InvariantCheckResult(
                        invariant_id="INV-4",
                        passed=False,
                        details=f"Missing severity level: {level_name}",
                    )

            # Verify strict ordering
            levels = [Severity[name] for name in EXPECTED_SEVERITY_ORDER]
            for i in range(len(levels) - 1):
                if not (levels[i] < levels[i + 1]):
                    return InvariantCheckResult(
                        invariant_id="INV-4",
                        passed=False,
                        details=(
                            f"Severity ordering violated: {levels[i].name} "
                            f"(value={levels[i].value}) is not less than "
                            f"{levels[i + 1].name} (value={levels[i + 1].value})"
                        ),
                    )

            return InvariantCheckResult(
                invariant_id="INV-4",
                passed=True,
                details="Severity levels strictly ordered: INFO < WARNING < DEGRADED < CRITICAL < CANONICAL_BREAK < DETERMINISTIC_FAILURE",
            )

        except Exception as exc:
            return InvariantCheckResult(
                invariant_id="INV-4",
                passed=False,
                details=f"Severity ordering check failed with exception: {type(exc).__name__}: {exc}",
            )

    def _check_orthogonal_dimensions(self) -> InvariantCheckResult:
        """INV-5: Verify runtime states belong to orthogonal integrity dimensions.

        Each state must map to at most one integrity dimension (except HEALTHY
        which maps to none). Dimensions must be independent axes.
        """
        try:
            from runtime.runtime_state_model import (
                IntegrityDimension,
                RuntimeState,
                STATE_DIMENSIONS,
            )

            # Verify all RuntimeState values have a dimension mapping
            for state in RuntimeState:
                if state not in STATE_DIMENSIONS:
                    return InvariantCheckResult(
                        invariant_id="INV-5",
                        passed=False,
                        details=f"RuntimeState.{state.name} has no dimension mapping in STATE_DIMENSIONS",
                    )

            # Verify HEALTHY maps to no dimensions (it's the baseline)
            if STATE_DIMENSIONS.get(RuntimeState.HEALTHY, None) != []:
                return InvariantCheckResult(
                    invariant_id="INV-5",
                    passed=False,
                    details="HEALTHY state should map to no integrity dimensions (empty list)",
                )

            # Verify orthogonality: each non-HEALTHY state maps to exactly one dimension
            for state, dimensions in STATE_DIMENSIONS.items():
                if state == RuntimeState.HEALTHY:
                    continue
                if len(dimensions) != 1:
                    return InvariantCheckResult(
                        invariant_id="INV-5",
                        passed=False,
                        details=(
                            f"RuntimeState.{state.name} maps to {len(dimensions)} dimensions "
                            f"(expected exactly 1 for orthogonality): {dimensions}"
                        ),
                    )

            # Verify all IntegrityDimension values are used
            used_dimensions = set()
            for state, dimensions in STATE_DIMENSIONS.items():
                for dim in dimensions:
                    used_dimensions.add(dim)

            all_dimensions = set(IntegrityDimension)
            unused = all_dimensions - used_dimensions
            if unused:
                return InvariantCheckResult(
                    invariant_id="INV-5",
                    passed=False,
                    details=f"Unused integrity dimensions (orphaned): {[d.value for d in unused]}",
                )

            return InvariantCheckResult(
                invariant_id="INV-5",
                passed=True,
                details=(
                    f"Runtime states belong to orthogonal integrity dimensions. "
                    f"{len(IntegrityDimension)} dimensions, "
                    f"{len(RuntimeState)} states, all mapped correctly."
                ),
            )

        except Exception as exc:
            return InvariantCheckResult(
                invariant_id="INV-5",
                passed=False,
                details=f"Orthogonal dimensions check failed with exception: {type(exc).__name__}: {exc}",
            )

    def _check_pipeline_completion(self) -> InvariantCheckResult:
        """INV-7: Pipeline execution completes (degraded output preferred over no output).

        This is a design invariant. We validate that the gate framework never raises
        exceptions that would halt pipeline execution — it always produces a GateResult
        (even on failure/timeout) rather than propagating exceptions.
        """
        try:
            from governance.gate_framework import GateFramework

            # Verify that executing a gate that raises an exception still produces
            # a GateResult (fail) rather than propagating the exception
            test_config = {
                "gates": {
                    "_invariant_test_gate": {
                        "blocking_in_soft": False,
                        "blocking_in_hard": False,
                        "time_budget_ms": 1000,
                    }
                }
            }

            framework = GateFramework(config=test_config, enforcement_mode="observability")

            # Test 1: A gate that raises should produce a fail result, not propagate
            def raising_check() -> bool:
                raise RuntimeError("Simulated gate failure")

            result = framework.execute_gate("_invariant_test_gate", raising_check, 1000)

            if result.status != "fail":
                return InvariantCheckResult(
                    invariant_id="INV-7",
                    passed=False,
                    details=(
                        f"Gate framework propagated exception instead of producing fail result. "
                        f"Got status: {result.status}"
                    ),
                )

            # Test 2: A gate that returns False should produce a fail result
            def failing_check() -> bool:
                return False

            result2 = framework.execute_gate("_invariant_test_gate", failing_check, 1000)
            if result2.status != "fail":
                return InvariantCheckResult(
                    invariant_id="INV-7",
                    passed=False,
                    details="Gate framework did not produce fail result for falsy check return",
                )

            return InvariantCheckResult(
                invariant_id="INV-7",
                passed=True,
                details=(
                    "Pipeline completion invariant preserved: gate framework catches exceptions "
                    "and produces GateResult (degraded output) rather than halting pipeline"
                ),
            )

        except Exception as exc:
            return InvariantCheckResult(
                invariant_id="INV-7",
                passed=False,
                details=f"Pipeline completion check failed with exception: {type(exc).__name__}: {exc}",
            )

    def _check_observability_non_blocking(self) -> InvariantCheckResult:
        """INV-8: Observability mode never blocks commits or pipeline execution.

        Validates that when enforcement_mode is "observability", the gate framework
        enforcement_action is always "warn" or "info", never "block".
        """
        try:
            from governance.gate_framework import GateFramework

            # Create a framework in observability mode with a blocking gate config
            test_config = {
                "gates": {
                    "_inv8_test_gate": {
                        "blocking_in_soft": True,
                        "blocking_in_hard": True,
                        "time_budget_ms": 1000,
                    }
                }
            }

            framework = GateFramework(config=test_config, enforcement_mode="observability")

            # A failing gate in observability mode must NOT produce "block"
            def failing_check() -> bool:
                return False

            result = framework.execute_gate("_inv8_test_gate", failing_check, 1000)

            if result.enforcement_action == "block":
                return InvariantCheckResult(
                    invariant_id="INV-8",
                    passed=False,
                    details=(
                        "Observability mode produced 'block' enforcement action. "
                        "This violates INV-8: observability mode must never block."
                    ),
                )

            if result.enforcement_action not in ("warn", "info"):
                return InvariantCheckResult(
                    invariant_id="INV-8",
                    passed=False,
                    details=(
                        f"Observability mode produced unexpected enforcement action: "
                        f"'{result.enforcement_action}'. Expected 'warn' or 'info'."
                    ),
                )

            # Also verify a raising gate doesn't block in observability
            def raising_check() -> bool:
                raise RuntimeError("Simulated failure")

            result2 = framework.execute_gate("_inv8_test_gate", raising_check, 1000)

            if result2.enforcement_action == "block":
                return InvariantCheckResult(
                    invariant_id="INV-8",
                    passed=False,
                    details=(
                        "Observability mode produced 'block' on exception. "
                        "This violates INV-8."
                    ),
                )

            return InvariantCheckResult(
                invariant_id="INV-8",
                passed=True,
                details=(
                    "Observability mode non-blocking invariant preserved: "
                    "enforcement_action is always 'warn' or 'info', never 'block'"
                ),
            )

        except Exception as exc:
            return InvariantCheckResult(
                invariant_id="INV-8",
                passed=False,
                details=f"Observability non-blocking check failed with exception: {type(exc).__name__}: {exc}",
            )

    def validate_all(self) -> GateResult:
        """Run all runtime invariant checks and produce a GateResult.

        Returns:
            A GateResult summarizing the invariant validation outcome.
            Status is "pass" if all invariants hold, "fail" otherwise.
            Enforcement action respects the configured enforcement mode.
        """
        start_time = time.monotonic()

        summary = InvariantValidationSummary()
        summary.add(self._check_chain_model())
        summary.add(self._check_severity_ordering())
        summary.add(self._check_orthogonal_dimensions())
        summary.add(self._check_pipeline_completion())
        summary.add(self._check_observability_non_blocking())

        elapsed_ms = (time.monotonic() - start_time) * 1000.0

        # Build details list from individual check results
        details: list[str] = []
        for result in summary.results:
            prefix = "PASS" if result.passed else "FAIL"
            details.append(f"[{prefix}] {result.invariant_id}: {result.details}")

        status = "pass" if summary.all_passed else "fail"

        # Determine enforcement action based on mode
        if status == "pass":
            enforcement_action = "info"
        elif self._enforcement_mode == "observability":
            enforcement_action = "warn"
        else:
            # soft and hard mode: invariant violations are always blocking
            enforcement_action = "block"

        return GateResult(
            gate_name=self.GATE_NAME,
            status=status,
            enforcement_action=enforcement_action,
            duration_ms=round(elapsed_ms, 2),
            details=details,
            timestamp=datetime.now(timezone.utc).isoformat(),
            governance_policy_version="",
            governance_state_provenance="authoritative",
        )

    def as_gate_check_fn(self) -> callable:
        """Return a callable suitable for use as a gate check_fn in GateFramework.

        The returned callable produces a dict with "status", "passed", and "details"
        keys that the GateFramework executor interprets.

        Returns:
            A zero-argument callable for use in GateFramework config.
        """

        def _check() -> dict[str, Any]:
            summary = InvariantValidationSummary()
            summary.add(self._check_chain_model())
            summary.add(self._check_severity_ordering())
            summary.add(self._check_orthogonal_dimensions())
            summary.add(self._check_pipeline_completion())
            summary.add(self._check_observability_non_blocking())

            details: list[str] = []
            for result in summary.results:
                prefix = "PASS" if result.passed else "FAIL"
                details.append(f"[{prefix}] {result.invariant_id}: {result.details}")

            return {
                "status": "pass" if summary.all_passed else "fail",
                "passed": summary.all_passed,
                "details": details,
            }

        return _check
