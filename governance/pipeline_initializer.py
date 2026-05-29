"""Pipeline initialization with cold-start detection and provenance tagging.

Wires the ColdStartHandler into the governance pipeline initialization flow.
At pipeline start:
1. Instantiate ColdStartHandler
2. Check is_cold_start() to detect missing governance state
3. If cold-start: initialize defaults, force observability, tag bootstrap_derived
4. If not cold-start: use configured enforcement mode, tag authoritative

This module is the entry point for governance pipeline initialization and
delegates to enforcement_config_loader.initialize_enforcers() for the actual
enforcer instantiation.

Validates: Requirements 31.1, 31.2
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from governance.actor_identity import ActorIdentity
from governance.cold_start_handler import ColdStartHandler, LedgerEntry
from governance.enforcement_config_loader import (
    initialize_enforcers,
    load_enforcement_mode,
)
from governance.state_provenance_tagger import (
    GovernanceProvenance,
    StateProvenanceTagger,
)


@dataclass
class PipelineInitResult:
    """Result of pipeline initialization including enforcement context.

    Attributes:
        enforcement_mode: The active enforcement mode for this pipeline run.
        is_cold_start: Whether cold-start was detected.
        provenance: The governance state provenance tag.
        bootstrap_entry: The bootstrap LedgerEntry if cold-start, else None.
        enforcers: Dictionary of initialized enforcer instances.
        provenance_tagger: The StateProvenanceTagger instance for this run.
    """

    enforcement_mode: str
    is_cold_start: bool
    provenance: GovernanceProvenance
    bootstrap_entry: LedgerEntry | None
    enforcers: dict[str, Any]
    provenance_tagger: StateProvenanceTagger


def initialize_pipeline(
    base_path: str | None = None,
    actor: ActorIdentity | None = None,
    config_path: str | None = None,
) -> PipelineInitResult:
    """Initialize the governance pipeline with cold-start detection.

    This is the primary entry point for governance pipeline initialization.
    It checks for cold-start conditions and configures the enforcement
    pipeline accordingly.

    Args:
        base_path: Project root directory. Defaults to current working directory.
        actor: The ActorIdentity performing the initialization. If None,
            detected from environment.
        config_path: Explicit path to config.yaml. If None, uses default.

    Returns:
        PipelineInitResult containing the enforcement mode, provenance,
        and initialized enforcers.
    """
    if base_path is None:
        base_path = os.getcwd()

    if actor is None:
        actor = ActorIdentity.from_environment()

    domainization_path = os.path.join(base_path, ".domainization")

    # Step 1: Instantiate ColdStartHandler
    cold_start_handler = ColdStartHandler(domainization_path)

    # Step 2: Check cold-start condition
    provenance_tagger = StateProvenanceTagger()

    if cold_start_handler.is_cold_start():
        # Cold-start path: initialize defaults, force observability, tag bootstrap_derived
        return _handle_cold_start(
            cold_start_handler=cold_start_handler,
            actor=actor,
            provenance_tagger=provenance_tagger,
            base_path=base_path,
            config_path=config_path,
        )
    else:
        # Normal path: use configured enforcement mode, tag authoritative
        return _handle_normal_start(
            provenance_tagger=provenance_tagger,
            base_path=base_path,
            config_path=config_path,
        )


def _handle_cold_start(
    cold_start_handler: ColdStartHandler,
    actor: ActorIdentity,
    provenance_tagger: StateProvenanceTagger,
    base_path: str,
    config_path: str | None,
) -> PipelineInitResult:
    """Handle cold-start initialization.

    Calls initialize(actor) to create minimal defaults, forces observability
    mode, and tags provenance as bootstrap_derived.

    Args:
        cold_start_handler: The ColdStartHandler instance.
        actor: The ActorIdentity performing initialization.
        provenance_tagger: The StateProvenanceTagger for this run.
        base_path: Project root directory.
        config_path: Explicit path to config.yaml.

    Returns:
        PipelineInitResult with cold-start configuration.
    """
    # Initialize minimal defaults and get bootstrap ledger entry
    bootstrap_entry = cold_start_handler.initialize(actor)

    # Force observability mode regardless of config
    enforcement_mode = "observability"

    # Tag provenance as bootstrap_derived
    provenance = provenance_tagger.tag(
        source="cold_start_initialization",
        is_validated=False,
        is_cached=False,
        is_cold_start=True,
    )

    # Initialize enforcers with cold_start_override=True
    enforcers = initialize_enforcers(
        config_path=config_path,
        base_path=base_path,
        cold_start_override=True,
    )

    return PipelineInitResult(
        enforcement_mode=enforcement_mode,
        is_cold_start=True,
        provenance=provenance,
        bootstrap_entry=bootstrap_entry,
        enforcers=enforcers,
        provenance_tagger=provenance_tagger,
    )


def _handle_normal_start(
    provenance_tagger: StateProvenanceTagger,
    base_path: str,
    config_path: str | None,
) -> PipelineInitResult:
    """Handle normal (non-cold-start) initialization.

    Reads enforcement mode from config and tags provenance as authoritative.

    Args:
        provenance_tagger: The StateProvenanceTagger for this run.
        base_path: Project root directory.
        config_path: Explicit path to config.yaml.

    Returns:
        PipelineInitResult with normal configuration.
    """
    # Read enforcement mode from config
    enforcement_mode = load_enforcement_mode(
        config_path=config_path,
        base_path=base_path,
    )

    # Tag provenance as authoritative (loaded from canonical source, validated)
    provenance = provenance_tagger.tag(
        source="config.yaml",
        is_validated=True,
        is_cached=False,
        is_cold_start=False,
    )

    # Initialize enforcers with configured mode
    enforcers = initialize_enforcers(
        config_path=config_path,
        base_path=base_path,
        cold_start_override=False,
    )

    return PipelineInitResult(
        enforcement_mode=enforcement_mode,
        is_cold_start=False,
        provenance=provenance,
        bootstrap_entry=None,
        enforcers=enforcers,
        provenance_tagger=provenance_tagger,
    )
