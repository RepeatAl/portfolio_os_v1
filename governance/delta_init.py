"""Delta layer initialization sequence — linear, minimal, no framework.

Loads the 4 delta governance components in strict order:
    1. InfluenceGraph (CRITICAL — halts on cycles or missing declarations)
    2. DeploymentAuthority (CRITICAL — halts on topology violations)
    3. TransitionCooldown (fail_soft — degrades gracefully)
    4. DomainLifecycleManager (fail_soft — degrades gracefully)

Design constraints:
- No framework escalation
- No plugin system
- No event bus
- No runtime kernel
- Simple linear function, not an architecture

Requirements: 2.4, 4.4, 5.4, 11.5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from governance.deployment_authority import DeploymentAuthorityModel
    from governance.domain_lifecycle import DomainLifecycleManager
    from governance.influence_graph import GovernanceInfluenceGraph
    from governance.mutation_audit_ledger import MutationAuditLedger
    from governance.transition_cooldown import TransitionCooldown

logger = logging.getLogger(__name__)


@dataclass
class DeltaInitResult:
    """Result of the delta layer initialization sequence.

    Attributes:
        success: True if all CRITICAL components initialized without error.
        influence_graph: The initialized InfluenceGraph, or None on failure.
        deployment_authority: The initialized DeploymentAuthorityModel, or None on failure.
        transition_cooldown: The initialized TransitionCooldown, or None if degraded.
        domain_lifecycle: The initialized DomainLifecycleManager, or None if degraded.
        errors: List of error messages from CRITICAL failures (halting).
        warnings: List of warning messages from fail_soft degradations.
    """

    success: bool
    influence_graph: GovernanceInfluenceGraph | None = None
    deployment_authority: DeploymentAuthorityModel | None = None
    transition_cooldown: TransitionCooldown | None = None
    domain_lifecycle: DomainLifecycleManager | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def initialize_delta_layer(
    declarations_path: str,
    authority_model_path: str,
    config_path: str,
    domain_registry_path: str,
    artifact_registry_path: str,
    ledger: MutationAuditLedger | None = None,
) -> DeltaInitResult:
    """Initialize the governance delta layer in strict component order.

    Loads components sequentially:
        1. InfluenceGraph — CRITICAL: halts init on cycles or directionality violations
        2. DeploymentAuthority — CRITICAL: halts init on topology violations
        3. TransitionCooldown — fail_soft: degrades gracefully on config errors
        4. DomainLifecycleManager — fail_soft: degrades gracefully on registry errors

    If a CRITICAL component fails, initialization halts immediately and
    subsequent components are NOT loaded. fail_soft components that encounter
    errors log warnings and return None in the result, but do not halt init.

    Args:
        declarations_path: Path to governance_influence_declarations.yaml.
        authority_model_path: Path to deployment_authority_model.yaml.
        config_path: Path to .domainization/config.yaml.
        domain_registry_path: Path to domain_registry.yaml.
        artifact_registry_path: Path to artifact_registry.yaml.
        ledger: Optional MutationAuditLedger for event recording.

    Returns:
        DeltaInitResult with initialized components and any errors/warnings.
    """
    errors: list[str] = []
    warnings: list[str] = []

    # --- Step 1: InfluenceGraph (CRITICAL — halt on failure) ---
    logger.info("Delta init [1/4]: Loading InfluenceGraph...")
    influence_graph = _init_influence_graph(declarations_path, ledger, errors)
    if influence_graph is None:
        logger.critical(
            "Delta init HALTED: InfluenceGraph validation failed. "
            "Errors: %s",
            errors,
        )
        return DeltaInitResult(success=False, errors=errors, warnings=warnings)

    # --- Step 2: DeploymentAuthority (CRITICAL — halt on failure) ---
    logger.info("Delta init [2/4]: Loading DeploymentAuthority...")
    deployment_authority = _init_deployment_authority(
        authority_model_path, ledger, errors
    )
    if deployment_authority is None:
        logger.critical(
            "Delta init HALTED: DeploymentAuthority validation failed. "
            "Errors: %s",
            errors,
        )
        return DeltaInitResult(
            success=False,
            influence_graph=influence_graph,
            errors=errors,
            warnings=warnings,
        )

    # --- Step 3: TransitionCooldown (fail_soft — degrade gracefully) ---
    logger.info("Delta init [3/4]: Loading TransitionCooldown...")
    transition_cooldown = _init_transition_cooldown(config_path, ledger, warnings)

    # --- Step 4: DomainLifecycleManager (fail_soft — degrade gracefully) ---
    logger.info("Delta init [4/4]: Loading DomainLifecycleManager...")
    domain_lifecycle = _init_domain_lifecycle(
        domain_registry_path, artifact_registry_path, ledger, warnings
    )

    logger.info(
        "Delta init complete. Components: InfluenceGraph=OK, "
        "DeploymentAuthority=OK, TransitionCooldown=%s, DomainLifecycle=%s",
        "OK" if transition_cooldown else "DEGRADED",
        "OK" if domain_lifecycle else "DEGRADED",
    )

    return DeltaInitResult(
        success=True,
        influence_graph=influence_graph,
        deployment_authority=deployment_authority,
        transition_cooldown=transition_cooldown,
        domain_lifecycle=domain_lifecycle,
        errors=errors,
        warnings=warnings,
    )


def _init_influence_graph(
    declarations_path: str,
    ledger: MutationAuditLedger | None,
    errors: list[str],
) -> GovernanceInfluenceGraph | None:
    """Initialize the InfluenceGraph component.

    Returns the initialized graph on success, None on CRITICAL failure.
    Appends error messages to the errors list on failure.
    """
    from governance.influence_graph import GovernanceInfluenceGraph

    try:
        graph = GovernanceInfluenceGraph(
            declarations_path=declarations_path,
            ledger=ledger,
        )
        is_valid, validation_errors = graph.validate_at_init()
        if not is_valid:
            errors.extend(validation_errors)
            return None
        return graph
    except Exception as exc:
        errors.append(f"InfluenceGraph init exception: {exc}")
        logger.critical("InfluenceGraph init exception: %s", exc)
        return None


def _init_deployment_authority(
    model_path: str,
    ledger: MutationAuditLedger | None,
    errors: list[str],
) -> DeploymentAuthorityModel | None:
    """Initialize the DeploymentAuthority component.

    Returns the initialized model on success, None on CRITICAL failure.
    Appends error messages to the errors list on failure.
    """
    from governance.deployment_authority import DeploymentAuthorityModel

    try:
        model = DeploymentAuthorityModel(
            model_path=model_path,
            ledger=ledger,
        )
        is_valid, validation_errors = model.validate_at_init()
        if not is_valid:
            errors.extend(validation_errors)
            return None
        return model
    except Exception as exc:
        errors.append(f"DeploymentAuthority init exception: {exc}")
        logger.critical("DeploymentAuthority init exception: %s", exc)
        return None


def _init_transition_cooldown(
    config_path: str,
    ledger: MutationAuditLedger | None,
    warnings: list[str],
) -> TransitionCooldown | None:
    """Initialize the TransitionCooldown component (fail_soft).

    Returns the initialized cooldown on success, None on degradation.
    Appends warning messages to the warnings list on degradation.
    """
    from governance.transition_cooldown import TransitionCooldown

    try:
        cooldown = TransitionCooldown(
            config_path=config_path,
            ledger=ledger,
        )
        return cooldown
    except Exception as exc:
        warning_msg = (
            f"TransitionCooldown degraded: {exc}. "
            f"Cooldown enforcement unavailable."
        )
        warnings.append(warning_msg)
        logger.warning(warning_msg)
        return None


def _init_domain_lifecycle(
    domain_registry_path: str,
    artifact_registry_path: str,
    ledger: MutationAuditLedger | None,
    warnings: list[str],
) -> DomainLifecycleManager | None:
    """Initialize the DomainLifecycleManager component (fail_soft).

    Returns the initialized manager on success, None on degradation.
    Appends warning messages to the warnings list on degradation.
    """
    from governance.domain_lifecycle import DomainLifecycleManager

    try:
        manager = DomainLifecycleManager(
            domain_registry_path=domain_registry_path,
            artifact_registry_path=artifact_registry_path,
            ledger=ledger,
        )
        return manager
    except Exception as exc:
        warning_msg = (
            f"DomainLifecycleManager degraded: {exc}. "
            f"Domain lifecycle checks unavailable."
        )
        warnings.append(warning_msg)
        logger.warning(warning_msg)
        return None
