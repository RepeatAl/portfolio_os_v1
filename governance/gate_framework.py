"""Deployment gate framework data contracts, aggregate state computation, and executor.

Provides GateResult and GateSummary dataclasses for structured gate output,
round-trip serialization to/from dict for JSON/YAML persistence,
deterministic aggregate governance state computation, and the GateFramework
executor class for running gates with enforcement mode logic and time budgets.

Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.2, 6.3, 6.4, 26.1, 26.2, 26.3, 26.4, 32.1, 32.2, 32.6
"""

from __future__ import annotations

import concurrent.futures
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


# Valid values for GateResult.status
VALID_STATUSES = frozenset({"pass", "fail", "timeout", "skip"})

# Valid values for GateResult.enforcement_action
VALID_ENFORCEMENT_ACTIONS = frozenset({"block", "warn", "info"})

# Valid values for GateSummary.aggregate_state
VALID_AGGREGATE_STATES = frozenset({"healthy", "partial", "degraded", "collapsed"})


@dataclass
class GateResult:
    """Structured output from a single deployment gate execution.

    Attributes:
        gate_name: Identifier for the gate that was executed.
        status: Outcome of the gate check. One of "pass", "fail",
                "timeout", or "skip".
        enforcement_action: Action taken based on enforcement mode.
                           One of "block", "warn", or "info".
        duration_ms: Execution duration in milliseconds.
        details: List of human-readable findings or violation descriptions.
        timestamp: ISO 8601 timestamp of when the gate was evaluated.
        governance_policy_version: Content hash identifying the active
                                   governance policy at evaluation time.
        governance_state_provenance: Provenance tag indicating the source
                                     and reliability of governance state.
    """

    gate_name: str
    status: str
    enforcement_action: str
    duration_ms: float
    details: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    governance_policy_version: str = ""
    governance_state_provenance: str = "authoritative"

    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{self.status}'. Must be one of: {sorted(VALID_STATUSES)}"
            )
        if self.enforcement_action not in VALID_ENFORCEMENT_ACTIONS:
            raise ValueError(
                f"Invalid enforcement_action '{self.enforcement_action}'. "
                f"Must be one of: {sorted(VALID_ENFORCEMENT_ACTIONS)}"
            )

    def to_dict(self) -> dict:
        """Serialize to a dict suitable for JSON/YAML persistence.

        Returns:
            A dictionary with all GateResult fields, suitable for
            round-trip serialization.
        """
        return {
            "gate_name": self.gate_name,
            "status": self.status,
            "enforcement_action": self.enforcement_action,
            "duration_ms": self.duration_ms,
            "details": list(self.details),
            "timestamp": self.timestamp,
            "governance_policy_version": self.governance_policy_version,
            "governance_state_provenance": self.governance_state_provenance,
        }

    @classmethod
    def from_dict(cls, data: dict) -> GateResult:
        """Deserialize from a dict (e.g., loaded from JSON/YAML).

        Args:
            data: Dictionary with GateResult field keys.

        Returns:
            A GateResult instance.

        Raises:
            ValueError: If status or enforcement_action is invalid.
            KeyError: If required keys are missing.
        """
        return cls(
            gate_name=data["gate_name"],
            status=data["status"],
            enforcement_action=data["enforcement_action"],
            duration_ms=float(data["duration_ms"]),
            details=list(data.get("details", [])),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            governance_policy_version=data.get("governance_policy_version", ""),
            governance_state_provenance=data.get("governance_state_provenance", "authoritative"),
        )


@dataclass
class GateSummary:
    """Combined summary of all deployment gate executions.

    Attributes:
        total_gates: Total number of gates executed.
        passed: Number of gates with status "pass".
        failed: Number of gates with status "fail".
        blocked: Number of gates with enforcement_action "block" and
                 status "fail".
        timed_out: Number of gates with status "timeout".
        total_duration_ms: Sum of all gate execution durations.
        aggregate_state: Deterministic aggregate governance state.
                        One of "healthy", "partial", "degraded", "collapsed".
        git_sha: Git commit SHA for the evaluated code.
        branch: Git branch name.
        runtime_integrity_hash: SHA-256 fingerprint of governance/runtime files.
        governance_overhead_percent: Governance time as percentage of
                                     total pipeline time.
    """

    total_gates: int
    passed: int
    failed: int
    blocked: int
    timed_out: int
    total_duration_ms: float
    aggregate_state: str
    git_sha: str = ""
    branch: str = ""
    runtime_integrity_hash: str = ""
    governance_overhead_percent: float = 0.0

    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if self.aggregate_state not in VALID_AGGREGATE_STATES:
            raise ValueError(
                f"Invalid aggregate_state '{self.aggregate_state}'. "
                f"Must be one of: {sorted(VALID_AGGREGATE_STATES)}"
            )

    def to_dict(self) -> dict:
        """Serialize to a dict suitable for JSON/YAML persistence.

        Returns:
            A dictionary with all GateSummary fields.
        """
        return {
            "total_gates": self.total_gates,
            "passed": self.passed,
            "failed": self.failed,
            "blocked": self.blocked,
            "timed_out": self.timed_out,
            "total_duration_ms": self.total_duration_ms,
            "aggregate_state": self.aggregate_state,
            "git_sha": self.git_sha,
            "branch": self.branch,
            "runtime_integrity_hash": self.runtime_integrity_hash,
            "governance_overhead_percent": self.governance_overhead_percent,
        }

    @classmethod
    def from_dict(cls, data: dict) -> GateSummary:
        """Deserialize from a dict (e.g., loaded from JSON/YAML).

        Args:
            data: Dictionary with GateSummary field keys.

        Returns:
            A GateSummary instance.

        Raises:
            ValueError: If aggregate_state is invalid.
            KeyError: If required keys are missing.
        """
        return cls(
            total_gates=int(data["total_gates"]),
            passed=int(data["passed"]),
            failed=int(data["failed"]),
            blocked=int(data["blocked"]),
            timed_out=int(data["timed_out"]),
            total_duration_ms=float(data["total_duration_ms"]),
            aggregate_state=data["aggregate_state"],
            git_sha=data.get("git_sha", ""),
            branch=data.get("branch", ""),
            runtime_integrity_hash=data.get("runtime_integrity_hash", ""),
            governance_overhead_percent=float(data.get("governance_overhead_percent", 0.0)),
        )


def compute_aggregate_state(results: list[GateResult]) -> str:
    """Compute deterministic aggregate governance state from gate results.

    Aggregate state logic:
    - "healthy": all gates pass
    - "partial": some gates fail or timeout but no gate has enforcement_action
                 "block" with status "fail", and more than 50% pass
    - "degraded": at least one gate blocked (enforcement_action "block" with
                  status "fail"), or 50% or fewer gates pass
    - "collapsed": majority of gates fail or timeout, or zero gates pass,
                   or no gates were executed

    The computation is deterministic: for any given set of gate results,
    the same aggregate state is always produced.

    Args:
        results: List of GateResult objects from gate execution.

    Returns:
        One of "healthy", "partial", "degraded", or "collapsed".
    """
    if not results:
        return "collapsed"

    total = len(results)
    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    timed_out = sum(1 for r in results if r.status == "timeout")
    blocked = sum(
        1 for r in results
        if r.status == "fail" and r.enforcement_action == "block"
    )

    # All gates pass -> healthy
    if passed == total:
        return "healthy"

    # Zero gates pass -> collapsed
    if passed == 0:
        return "collapsed"

    # Majority fail or timeout -> collapsed
    if (failed + timed_out) > (total / 2):
        return "collapsed"

    # At least one gate blocked -> degraded
    if blocked > 0:
        return "degraded"

    # 50% or fewer pass -> degraded
    if passed <= (total / 2):
        return "degraded"

    # Some gates fail/timeout but none blocked and more than 50% pass -> partial
    return "partial"


# Valid enforcement modes for GateFramework
VALID_ENFORCEMENT_MODES = frozenset({"observability", "soft", "hard"})

# Total CI gate budget in seconds (Req 6.4)
TOTAL_CI_GATE_BUDGET_SECONDS = 120


class GateFramework:
    """Deployment gate executor with enforcement mode logic and time budgets.

    Executes independently configurable gates, applies enforcement mode
    logic to determine blocking vs. warning behavior, and enforces per-gate
    time budgets. Produces structured GateResult and GateSummary output.

    Enforcement Mode Logic:
        - observability: execute all gates, report as warnings, never block
        - soft: block on gates configured as blocking_in_soft, warn on others
        - hard: block on all gates configured as blocking_in_soft or blocking_in_hard

    Config format:
        {
            "gates": {
                "gate_name": {
                    "blocking_in_soft": True/False,
                    "blocking_in_hard": True/False,
                    "time_budget_ms": 5000,
                    "check_fn": callable  # optional, can be passed to execute_gate
                }
            }
        }

    Requirements: 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4
    """

    def __init__(self, config: dict, enforcement_mode: str) -> None:
        """Initialize the gate framework with configuration and enforcement mode.

        Args:
            config: Dictionary containing gate configurations under a "gates" key.
                    Each gate entry may have blocking_in_soft, blocking_in_hard,
                    time_budget_ms, and optionally check_fn.
            enforcement_mode: One of "observability", "soft", or "hard".

        Raises:
            ValueError: If enforcement_mode is not a valid mode.
        """
        if enforcement_mode not in VALID_ENFORCEMENT_MODES:
            raise ValueError(
                f"Invalid enforcement_mode '{enforcement_mode}'. "
                f"Must be one of: {sorted(VALID_ENFORCEMENT_MODES)}"
            )
        self._config = config
        self._enforcement_mode = enforcement_mode
        self._gates: dict[str, dict] = config.get("gates", {})
        self._results: list[GateResult] = []
        self._policy_version: str = config.get("governance_policy_version", "")
        self._state_provenance: str = config.get("governance_state_provenance", "authoritative")

    @property
    def enforcement_mode(self) -> str:
        """Current enforcement mode."""
        return self._enforcement_mode

    @property
    def gates(self) -> dict[str, dict]:
        """Configured gates."""
        return dict(self._gates)

    @property
    def results(self) -> list[GateResult]:
        """Results from executed gates."""
        return list(self._results)

    def _determine_enforcement_action(self, gate_name: str, status: str) -> str:
        """Determine the enforcement action based on mode and gate config.

        Args:
            gate_name: Name of the gate being evaluated.
            status: The gate's execution status ("pass", "fail", "timeout", "skip").

        Returns:
            One of "block", "warn", or "info".
        """
        # Passing gates are always informational
        if status == "pass":
            return "info"

        # Skipped gates are always informational
        if status == "skip":
            return "info"

        gate_config = self._gates.get(gate_name, {})
        blocking_in_soft = gate_config.get("blocking_in_soft", False)
        blocking_in_hard = gate_config.get("blocking_in_hard", False)

        if self._enforcement_mode == "observability":
            # Observability mode: never block, always warn on non-pass
            return "warn"

        elif self._enforcement_mode == "soft":
            # Soft mode: block only if gate is configured as blocking_in_soft
            if blocking_in_soft:
                return "block"
            return "warn"

        elif self._enforcement_mode == "hard":
            # Hard mode: block if blocking_in_soft OR blocking_in_hard
            if blocking_in_soft or blocking_in_hard:
                return "block"
            return "warn"

        # Fallback (should not reach here due to __init__ validation)
        return "warn"

    def execute_gate(
        self, gate_name: str, check_fn: Callable[[], Any], time_budget_ms: int
    ) -> GateResult:
        """Execute a single gate with timeout handling.

        Runs the check function within the specified time budget. If the
        function exceeds the budget, a TIMEOUT result is produced. If the
        function raises an exception, a FAIL result is produced.

        Args:
            gate_name: Identifier for the gate being executed.
            check_fn: Callable that performs the gate check. Should return
                      a truthy value for pass, falsy for fail. May also
                      return a dict with "status" and optional "details" keys.
            time_budget_ms: Maximum execution time in milliseconds.

        Returns:
            A GateResult with the gate's outcome, enforcement action, and timing.
        """
        time_budget_seconds = time_budget_ms / 1000.0
        start_time = time.monotonic()
        status = "fail"
        details: list[str] = []

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(check_fn)
                try:
                    result = future.result(timeout=time_budget_seconds)

                    # Interpret the check function result
                    if isinstance(result, dict):
                        status = result.get("status", "pass" if result.get("passed", True) else "fail")
                        if status not in VALID_STATUSES:
                            status = "pass" if result.get("passed", True) else "fail"
                        details = result.get("details", [])
                        if isinstance(details, str):
                            details = [details]
                    elif result:
                        status = "pass"
                    else:
                        status = "fail"
                        details = [f"Gate '{gate_name}' check returned falsy value"]

                except concurrent.futures.TimeoutError:
                    status = "timeout"
                    details = [
                        f"Gate '{gate_name}' exceeded time budget of {time_budget_ms}ms",
                        f"Allocated: {time_budget_ms}ms",
                    ]
                    # Cancel the future if still running
                    future.cancel()

        except Exception as exc:
            status = "fail"
            details = [f"Gate '{gate_name}' raised exception: {type(exc).__name__}: {exc}"]

        elapsed_ms = (time.monotonic() - start_time) * 1000.0
        enforcement_action = self._determine_enforcement_action(gate_name, status)

        gate_result = GateResult(
            gate_name=gate_name,
            status=status,
            enforcement_action=enforcement_action,
            duration_ms=round(elapsed_ms, 2),
            details=details,
            timestamp=datetime.now(timezone.utc).isoformat(),
            governance_policy_version=self._policy_version,
            governance_state_provenance=self._state_provenance,
        )

        self._results.append(gate_result)
        return gate_result

    def execute_all_gates(self) -> GateSummary:
        """Execute all configured gates and produce a GateSummary.

        Iterates through all gates defined in the config, executing each
        with its configured check_fn and time_budget_ms. Gates without
        a check_fn are skipped. Produces a GateSummary with aggregate
        state computation.

        Returns:
            A GateSummary containing counts, timing, and aggregate state.
        """
        for gate_name, gate_config in self._gates.items():
            check_fn = gate_config.get("check_fn")
            if check_fn is None:
                # Skip gates without a check function
                skip_result = GateResult(
                    gate_name=gate_name,
                    status="skip",
                    enforcement_action="info",
                    duration_ms=0.0,
                    details=[f"Gate '{gate_name}' has no check_fn configured"],
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    governance_policy_version=self._policy_version,
                    governance_state_provenance=self._state_provenance,
                )
                self._results.append(skip_result)
                continue

            time_budget_ms = gate_config.get("time_budget_ms", 5000)
            self.execute_gate(gate_name, check_fn, time_budget_ms)

        # Compute summary from results
        aggregate_state = compute_aggregate_state(self._results)

        passed = sum(1 for r in self._results if r.status == "pass")
        failed = sum(1 for r in self._results if r.status == "fail")
        blocked = sum(
            1 for r in self._results
            if r.enforcement_action == "block" and r.status in ("fail", "timeout")
        )
        timed_out = sum(1 for r in self._results if r.status == "timeout")
        total_duration_ms = sum(r.duration_ms for r in self._results)

        return GateSummary(
            total_gates=len(self._results),
            passed=passed,
            failed=failed,
            blocked=blocked,
            timed_out=timed_out,
            total_duration_ms=round(total_duration_ms, 2),
            aggregate_state=aggregate_state,
        )
