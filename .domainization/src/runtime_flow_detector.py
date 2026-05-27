"""
Runtime Flow Detector

Detects and validates runtime flows between domains based on artifact dependencies.
Enforces authority chains: SIGNALS (1) → SEMANTICS (2) → REASONING (3) → REPORT (4).
Forbidden flows (e.g., Signal → Report, Dashboard → Semantic Truth) generate warnings.

Operates in OBSERVABILITY MODE: generates warnings, never blocks.

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.8, 14.9, 14.10
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Set
from enum import Enum


class FlowStatus(Enum):
    """Status of a detected runtime flow"""
    ALLOWED = "allowed"
    FORBIDDEN = "forbidden"
    WARNING = "warning"


@dataclass
class FlowStep:
    """A single step in a runtime flow"""
    domain_id: str
    authority_level: Optional[int]
    artifact_id: Optional[str] = None
    description: str = ""


@dataclass
class RuntimeFlow:
    """Represents a detected runtime flow between domains"""
    source_domain: str
    target_domain: str
    flow_path: List[str]  # Full path of domain IDs in the flow
    status: FlowStatus
    reason: str
    artifact_id: Optional[str] = None
    suggestion: str = ""


@dataclass
class AuthorityChainVisualization:
    """Visualization of the authority chain for a flow"""
    chain: List[FlowStep]
    is_valid: bool
    violations: List[str] = field(default_factory=list)

    def render_ascii(self) -> str:
        """Render the authority chain as ASCII art"""
        if not self.chain:
            return "(empty chain)"

        parts = []
        for i, step in enumerate(self.chain):
            level_str = f"L{step.authority_level}" if step.authority_level else "N/A"
            parts.append(f"{step.domain_id} ({level_str})")
            if i < len(self.chain) - 1:
                parts.append(" → ")

        chain_str = "".join(parts)
        status = "✓ VALID" if self.is_valid else "✗ INVALID"
        result = f"Authority Chain: {chain_str}\nStatus: {status}"

        if self.violations:
            result += "\nViolations:"
            for v in self.violations:
                result += f"\n  - {v}"

        return result


@dataclass
class FlowDetectionResult:
    """Result of runtime flow detection"""
    flows: List[RuntimeFlow]
    allowed_count: int = 0
    forbidden_count: int = 0
    execution_time_ms: float = 0.0

    def has_violations(self) -> bool:
        """Check if any forbidden flows were detected"""
        return self.forbidden_count > 0

    def get_forbidden_flows(self) -> List[RuntimeFlow]:
        """Get only forbidden flows"""
        return [f for f in self.flows if f.status == FlowStatus.FORBIDDEN]

    def get_allowed_flows(self) -> List[RuntimeFlow]:
        """Get only allowed flows"""
        return [f for f in self.flows if f.status == FlowStatus.ALLOWED]



class RuntimeFlowDetector:
    """
    Detects and validates runtime flows between domains.

    The core reasoning chain defines the allowed authority flow:
    SIGNALS (authority level 1) → SEMANTICS (level 2) → REASONING (level 3) → REPORT (level 4)

    Forbidden flows include:
    - Signal → Report (skips Semantics and Reasoning)
    - Signal → Reasoning (skips Semantics)
    - Dashboard → Semantic Truth (surface domain creating core meaning)
    - Dashboard → Signal Generation (surface domain creating signals)
    - Any domain creating meaning outside its authority level

    Operates in OBSERVABILITY MODE: warnings only, no blocking.
    """

    # Core reasoning chain in authority order
    AUTHORITY_CHAIN = ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]

    # Authority levels for core domains
    AUTHORITY_LEVELS: Dict[str, int] = {
        "SIGNALS": 1,
        "SEMANTICS": 2,
        "REASONING": 3,
        "REPORT": 4,
    }

    # Surface domains (no authority in reasoning chain)
    SURFACE_DOMAINS = {"GOV", "ARCH", "STATE", "DATA", "USER", "DEPLOY", "MEMORY", "SIM"}

    # Allowed direct flows (source → target)
    ALLOWED_FLOWS: Set[Tuple[str, str]] = {
        ("SIGNALS", "SEMANTICS"),
        ("SEMANTICS", "REASONING"),
        ("REASONING", "REPORT"),
    }

    # Explicitly forbidden flows with reasons
    FORBIDDEN_FLOWS: Dict[Tuple[str, str], str] = {
        ("SIGNALS", "REPORT"): "Signal → Report skips semantic interpretation and reasoning (Req 14.2)",
        ("SIGNALS", "REASONING"): "Signal → Reasoning skips semantic interpretation (Req 14.3)",
        ("USER", "SEMANTICS"): "Dashboard cannot create semantic truth (Req 14.4)",
        ("USER", "SIGNALS"): "Dashboard cannot generate signals (Req 14.5)",
        ("REPORT", "SIGNALS"): "Report domain cannot create signals (authority flows forward only)",
        ("REPORT", "SEMANTICS"): "Report domain cannot create semantic states (authority flows forward only)",
        ("REPORT", "REASONING"): "Report domain cannot create reasoning objects (authority flows forward only)",
        ("REASONING", "SIGNALS"): "Reasoning cannot create signals (authority flows forward only)",
        ("REASONING", "SEMANTICS"): "Reasoning cannot create semantic states (authority flows forward only)",
        ("SEMANTICS", "SIGNALS"): "Semantics cannot create signals (authority flows forward only)",
    }

    def __init__(self):
        """Initialize the runtime flow detector"""
        self.observer_name = "RuntimeFlowDetector"

    def detect_flow(self, source_domain: str, target_domain: str,
                    artifact_id: Optional[str] = None) -> RuntimeFlow:
        """
        Detect and validate a single flow between two domains.

        Args:
            source_domain: Domain initiating the flow
            target_domain: Domain receiving the flow
            artifact_id: Optional artifact ID involved in the flow

        Returns:
            RuntimeFlow with status and reason
        """
        flow_pair = (source_domain, target_domain)

        # Check explicitly forbidden flows
        if flow_pair in self.FORBIDDEN_FLOWS:
            return RuntimeFlow(
                source_domain=source_domain,
                target_domain=target_domain,
                flow_path=[source_domain, target_domain],
                status=FlowStatus.FORBIDDEN,
                reason=self.FORBIDDEN_FLOWS[flow_pair],
                artifact_id=artifact_id,
                suggestion=self._get_suggestion_for_forbidden_flow(source_domain, target_domain),
            )

        # Check allowed flows
        if flow_pair in self.ALLOWED_FLOWS:
            return RuntimeFlow(
                source_domain=source_domain,
                target_domain=target_domain,
                flow_path=[source_domain, target_domain],
                status=FlowStatus.ALLOWED,
                reason=f"Valid authority chain step: {source_domain} → {target_domain}",
                artifact_id=artifact_id,
            )

        # Check if it's a surface domain trying to create meaning in core domain
        if source_domain in self.SURFACE_DOMAINS and target_domain in self.AUTHORITY_LEVELS:
            return RuntimeFlow(
                source_domain=source_domain,
                target_domain=target_domain,
                flow_path=[source_domain, target_domain],
                status=FlowStatus.FORBIDDEN,
                reason=f"Surface domain '{source_domain}' cannot create meaning in core domain '{target_domain}' (Req 14.10)",
                artifact_id=artifact_id,
                suggestion=f"Only core reasoning domains can create meaning. {source_domain} should consume outputs from {target_domain}, not produce them.",
            )

        # Check if it's a backward flow in the authority chain
        if source_domain in self.AUTHORITY_LEVELS and target_domain in self.AUTHORITY_LEVELS:
            source_level = self.AUTHORITY_LEVELS[source_domain]
            target_level = self.AUTHORITY_LEVELS[target_domain]
            if source_level > target_level:
                return RuntimeFlow(
                    source_domain=source_domain,
                    target_domain=target_domain,
                    flow_path=[source_domain, target_domain],
                    status=FlowStatus.FORBIDDEN,
                    reason=f"Authority flows forward only: {source_domain} (L{source_level}) cannot create meaning in {target_domain} (L{target_level})",
                    artifact_id=artifact_id,
                    suggestion=f"Authority chain flows: SIGNALS → SEMANTICS → REASONING → REPORT. Reverse flows are forbidden.",
                )
            # Non-adjacent forward flow (skipping levels)
            if target_level - source_level > 1:
                skipped = [d for d, l in self.AUTHORITY_LEVELS.items()
                           if source_level < l < target_level]
                return RuntimeFlow(
                    source_domain=source_domain,
                    target_domain=target_domain,
                    flow_path=[source_domain, target_domain],
                    status=FlowStatus.FORBIDDEN,
                    reason=f"Flow skips required authority levels: {', '.join(skipped)}",
                    artifact_id=artifact_id,
                    suggestion=f"Route through the full chain: {' → '.join(self.AUTHORITY_CHAIN[source_level-1:target_level])}",
                )

        # Same domain flow or surface-to-surface: allowed
        if source_domain == target_domain:
            return RuntimeFlow(
                source_domain=source_domain,
                target_domain=target_domain,
                flow_path=[source_domain],
                status=FlowStatus.ALLOWED,
                reason="Same-domain flow (internal)",
                artifact_id=artifact_id,
            )

        # Surface-to-surface flows are generally allowed
        if source_domain in self.SURFACE_DOMAINS and target_domain in self.SURFACE_DOMAINS:
            return RuntimeFlow(
                source_domain=source_domain,
                target_domain=target_domain,
                flow_path=[source_domain, target_domain],
                status=FlowStatus.ALLOWED,
                reason=f"Surface-to-surface flow: {source_domain} → {target_domain}",
                artifact_id=artifact_id,
            )

        # Core domain reading from surface domain (allowed - surface supports core)
        if source_domain in self.SURFACE_DOMAINS and target_domain not in self.AUTHORITY_LEVELS:
            return RuntimeFlow(
                source_domain=source_domain,
                target_domain=target_domain,
                flow_path=[source_domain, target_domain],
                status=FlowStatus.ALLOWED,
                reason=f"Surface domain flow: {source_domain} → {target_domain}",
                artifact_id=artifact_id,
            )

        # Default: allowed with note
        return RuntimeFlow(
            source_domain=source_domain,
            target_domain=target_domain,
            flow_path=[source_domain, target_domain],
            status=FlowStatus.ALLOWED,
            reason=f"Flow {source_domain} → {target_domain} (no specific rule)",
            artifact_id=artifact_id,
        )

    def detect_flows_from_dependencies(
        self, artifact_id: str, artifact_domain: str,
        dependencies: List[Dict[str, str]]
    ) -> FlowDetectionResult:
        """
        Detect flows based on artifact dependencies.

        Each dependency represents a flow from the dependency's domain
        to the artifact's domain (the artifact consumes from its dependencies).

        Args:
            artifact_id: ID of the artifact being checked
            artifact_domain: Domain of the artifact
            dependencies: List of dicts with 'artifact_id' and 'domain' keys

        Returns:
            FlowDetectionResult with all detected flows
        """
        start_time = time.time()
        flows = []

        for dep in dependencies:
            dep_domain = dep.get("domain", "")
            dep_artifact_id = dep.get("artifact_id", "")

            if not dep_domain:
                continue

            # Flow goes from dependency domain → artifact domain
            flow = self.detect_flow(
                source_domain=dep_domain,
                target_domain=artifact_domain,
                artifact_id=artifact_id,
            )
            flows.append(flow)

        allowed_count = sum(1 for f in flows if f.status == FlowStatus.ALLOWED)
        forbidden_count = sum(1 for f in flows if f.status == FlowStatus.FORBIDDEN)
        execution_time = (time.time() - start_time) * 1000

        return FlowDetectionResult(
            flows=flows,
            allowed_count=allowed_count,
            forbidden_count=forbidden_count,
            execution_time_ms=execution_time,
        )

    def validate_flow_path(self, flow_path: List[str]) -> FlowDetectionResult:
        """
        Validate a complete flow path (multi-step).

        Checks each adjacent pair in the path for validity.

        Args:
            flow_path: List of domain IDs representing the flow path
                      e.g., ["SIGNALS", "SEMANTICS", "REASONING", "REPORT"]

        Returns:
            FlowDetectionResult with flows for each step
        """
        start_time = time.time()
        flows = []

        if len(flow_path) < 2:
            execution_time = (time.time() - start_time) * 1000
            return FlowDetectionResult(
                flows=[],
                allowed_count=0,
                forbidden_count=0,
                execution_time_ms=execution_time,
            )

        for i in range(len(flow_path) - 1):
            source = flow_path[i]
            target = flow_path[i + 1]
            flow = self.detect_flow(source, target)
            flow.flow_path = flow_path  # Set full path context
            flows.append(flow)

        allowed_count = sum(1 for f in flows if f.status == FlowStatus.ALLOWED)
        forbidden_count = sum(1 for f in flows if f.status == FlowStatus.FORBIDDEN)
        execution_time = (time.time() - start_time) * 1000

        return FlowDetectionResult(
            flows=flows,
            allowed_count=allowed_count,
            forbidden_count=forbidden_count,
            execution_time_ms=execution_time,
        )

    def visualize_authority_chain(self, flow_path: List[str]) -> AuthorityChainVisualization:
        """
        Visualize the authority chain for a given flow path.

        Shows each domain's authority level and whether the chain is valid.

        Args:
            flow_path: List of domain IDs in the flow

        Returns:
            AuthorityChainVisualization with chain details and validity
        """
        chain = []
        violations = []

        for domain_id in flow_path:
            level = self.AUTHORITY_LEVELS.get(domain_id)
            step = FlowStep(
                domain_id=domain_id,
                authority_level=level,
                description=self._get_domain_description(domain_id),
            )
            chain.append(step)

        # Check for violations in the chain
        for i in range(len(chain) - 1):
            current = chain[i]
            next_step = chain[i + 1]

            # Both must be core domains for authority chain validation
            if current.authority_level is not None and next_step.authority_level is not None:
                # Authority must flow forward (increasing level numbers)
                if next_step.authority_level <= current.authority_level:
                    violations.append(
                        f"Backward flow: {current.domain_id} (L{current.authority_level}) "
                        f"→ {next_step.domain_id} (L{next_step.authority_level})"
                    )
                # Must not skip levels
                elif next_step.authority_level - current.authority_level > 1:
                    violations.append(
                        f"Skipped level: {current.domain_id} (L{current.authority_level}) "
                        f"→ {next_step.domain_id} (L{next_step.authority_level})"
                    )
            elif current.authority_level is None and next_step.authority_level is not None:
                # Surface domain trying to feed into core domain
                violations.append(
                    f"Surface domain '{current.domain_id}' cannot create meaning "
                    f"in core domain '{next_step.domain_id}' (L{next_step.authority_level})"
                )

        is_valid = len(violations) == 0
        return AuthorityChainVisualization(
            chain=chain,
            is_valid=is_valid,
            violations=violations,
        )

    def get_allowed_flow_definitions(self) -> List[Dict[str, str]]:
        """
        Get all defined allowed flows.

        Returns:
            List of dicts with 'source', 'target', and 'description' keys
        """
        return [
            {
                "source": source,
                "target": target,
                "description": f"Authority chain step: {source} (L{self.AUTHORITY_LEVELS[source]}) → {target} (L{self.AUTHORITY_LEVELS[target]})",
            }
            for source, target in self.ALLOWED_FLOWS
        ]

    def get_forbidden_flow_definitions(self) -> List[Dict[str, str]]:
        """
        Get all defined forbidden flows.

        Returns:
            List of dicts with 'source', 'target', and 'reason' keys
        """
        return [
            {"source": source, "target": target, "reason": reason}
            for (source, target), reason in self.FORBIDDEN_FLOWS.items()
        ]

    def _get_suggestion_for_forbidden_flow(self, source: str, target: str) -> str:
        """Generate actionable suggestion for a forbidden flow"""
        if source == "SIGNALS" and target == "REPORT":
            return "Route through full chain: SIGNALS → SEMANTICS → REASONING → REPORT"
        elif source == "SIGNALS" and target == "REASONING":
            return "Route through SEMANTICS first: SIGNALS → SEMANTICS → REASONING"
        elif source == "USER" and target == "SEMANTICS":
            return "Dashboard should read semantic outputs, not create them. Use SIGNALS → SEMANTICS flow instead."
        elif source == "USER" and target == "SIGNALS":
            return "Dashboard should read signal outputs, not generate them. Signal generation belongs to SIGNALS domain."
        elif source in self.AUTHORITY_LEVELS and target in self.AUTHORITY_LEVELS:
            source_level = self.AUTHORITY_LEVELS[source]
            target_level = self.AUTHORITY_LEVELS[target]
            if source_level > target_level:
                return f"Authority flows forward only (SIGNALS → SEMANTICS → REASONING → REPORT). {source} cannot create meaning in {target}."
        return f"Review the authority chain and ensure flows follow: SIGNALS → SEMANTICS → REASONING → REPORT"

    def _get_domain_description(self, domain_id: str) -> str:
        """Get human-readable description for a domain"""
        descriptions = {
            "SIGNALS": "Raw signal calculation and structured signal output",
            "SEMANTICS": "Semantic interpretation of signals into meaning",
            "REASONING": "Reasoning conclusions from semantic states",
            "REPORT": "Human-readable report language from reasoning",
            "USER": "Dashboard and user interface",
            "DATA": "Data normalization and management",
            "STATE": "Portfolio state tracking",
            "DEPLOY": "Deployment and runtime orchestration",
            "MEMORY": "Historical snapshots and portfolio memory",
            "SIM": "Scenario modeling and simulation",
            "GOV": "Governance and decision frameworks",
            "ARCH": "Architecture and system design",
        }
        return descriptions.get(domain_id, f"Domain: {domain_id}")
