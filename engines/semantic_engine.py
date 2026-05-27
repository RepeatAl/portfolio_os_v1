"""Semantic Engine — Interprets raw signals into semantic states.

This engine is part of the SEMANTICS domain (Level 2) in the canonical chain:
SIGNALS → SEMANTICS → REASONING → REPORT.

It interprets Signal Engine outputs into deterministic, language-independent
Semantic States that represent canonical system truth.

The Semantic Signal Registry defines the complete signal structure for each state.
"""

# =============================================================================
# SEMANTIC SIGNAL REGISTRY
# =============================================================================
# Each entry defines a complete semantic state with:
#   signal_id, category, meaning, signal_origin, reasoning_impact, confidence_behavior
#
# HARDENING 8 — SEMANTIC STATE PROTECTION:
# The following 5 states are PROTECTED and must NOT be modified:
#   - ai_dependency_high
#   - deployment_fully_extended
#   - concentration_risk_elevated
#   - portfolio_health_fragile
#   - defense_dependency_elevated
# =============================================================================

SEMANTIC_SIGNAL_REGISTRY = {
    # --- PROTECTED STATES (DO NOT MODIFY) ---

    "ai_dependency_high": {
        "signal_id": "ai_dependency_high",
        "category": "narrative_dependency",
        "meaning": "Portfolio performance strongly depends on continued AI-related market leadership.",
        "signal_origin": ["allocation_engine", "attribution_engine", "correlation_engine"],
        "reasoning_impact": "Portfolio upside remains strong if AI leadership continues, but dependency risk rises if AI expectations weaken.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "AI exposure concentrated",
                "semiconductors dominate",
                "growth correlation rises",
            ]
        },
    },
    "deployment_fully_extended": {
        "signal_id": "deployment_fully_extended",
        "category": "deployment",
        "meaning": "Portfolio currently maintains very high invested exposure.",
        "signal_origin": ["allocation_engine", "capital_engine"],
        "reasoning_impact": "Future flexibility decreases while exposure sensitivity rises.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "cash low",
                "concentration elevated",
            ]
        },
    },
    "concentration_risk_elevated": {
        "signal_id": "concentration_risk_elevated",
        "category": "concentration",
        "meaning": "Portfolio exposure depends heavily on a limited number of positions, sectors, or narratives.",
        "signal_origin": ["allocation_engine", "correlation_engine", "scenario_engine"],
        "reasoning_impact": "Portfolio drawdown sensitivity increases.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "top holdings dominate allocation",
                "correlations rise",
                "narrative overlap increases",
            ]
        },
    },
    "portfolio_health_fragile": {
        "signal_id": "portfolio_health_fragile",
        "category": "portfolio_health",
        "meaning": "Portfolio structure may become vulnerable under stress scenarios.",
        "signal_origin": ["scenario_engine", "correlation_engine", "concentration_engine"],
        "reasoning_impact": "Risk management and exposure discipline become increasingly important.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "concentration elevated",
                "scenarios weak",
                "diversification poor",
            ]
        },
    },
    "defense_dependency_elevated": {
        "signal_id": "defense_dependency_elevated",
        "category": "narrative_dependency",
        "meaning": "Portfolio performance increasingly depends on continued defense-sector strength.",
        "signal_origin": ["allocation_engine", "attribution_engine"],
        "reasoning_impact": "Portfolio becomes more sensitive to geopolitical and macro-defense narratives.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "defense allocation dominant",
                "defense momentum persistent",
            ]
        },
    },

    # --- NEW STATES (Phase C — Semantic Expansion) ---

    "semiconductor_dependency_high": {
        "signal_id": "semiconductor_dependency_high",
        "category": "narrative_dependency",
        "meaning": "Portfolio performance strongly depends on semiconductor infrastructure leadership.",
        "signal_origin": ["allocation_engine", "attribution_engine"],
        "reasoning_impact": "Portfolio remains exposed to semiconductor cycle risk; supply chain disruptions or demand shifts in chip infrastructure may disproportionately impact returns.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "semiconductor allocation concentrated",
                "AI infrastructure correlation rises",
                "chip supply chain dependency elevated",
            ]
        },
    },
    "energy_grid_dependency": {
        "signal_id": "energy_grid_dependency",
        "category": "narrative_dependency",
        "meaning": "Portfolio performance depends on energy grid expansion and power infrastructure buildout narratives.",
        "signal_origin": ["allocation_engine", "attribution_engine", "scenario_engine"],
        "reasoning_impact": "Portfolio becomes sensitive to energy policy changes, grid capacity constraints, and power infrastructure investment cycles.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "energy infrastructure allocation rising",
                "power demand growth narrative strengthening",
                "grid buildout capital expenditure increasing",
            ]
        },
    },
    "datacenter_infrastructure_exposure": {
        "signal_id": "datacenter_infrastructure_exposure",
        "category": "narrative_dependency",
        "meaning": "Portfolio carries significant exposure to datacenter infrastructure buildout and hyperscaler capital expenditure cycles.",
        "signal_origin": ["allocation_engine", "attribution_engine", "correlation_engine"],
        "reasoning_impact": "Portfolio returns become sensitive to hyperscaler capex decisions, datacenter demand cycles, and compute infrastructure investment trends.",
        "confidence_behavior": {
            "confidence_increases_when": [
                "datacenter-related allocation concentrated",
                "hyperscaler capex correlation elevated",
                "compute infrastructure demand persistent",
            ]
        },
    },
}


def interpret_allocation_signals(allocation_df):
    """Interpret allocation signals into semantic states.

    Processes allocation data to detect narrative dependencies and concentration risks.
    Produces deterministic semantic states given the same input signals.

    Args:
        allocation_df: DataFrame with columns 'Category' and 'Allocation %'.

    Returns:
        List of semantic state dicts with signal_id, category, meaning, source, value.
    """
    semantic_states = []

    for _, row in allocation_df.iterrows():
        category = row["Category"]
        allocation = float(row["Allocation %"])

        if category == "Defense" and allocation > 25:
            semantic_states.append({
                "signal_id": "defense_dependency_elevated",
                "category": "narrative_dependency",
                "meaning": "Portfolio performance increasingly depends on continued defense-sector strength.",
                "source": "allocation_engine",
                "value": allocation,
            })

        if category == "Semiconductor" and allocation > 25:
            semantic_states.append({
                "signal_id": "semiconductor_dependency_elevated",
                "category": "narrative_dependency",
                "meaning": "Portfolio performance increasingly depends on semiconductor and AI infrastructure leadership.",
                "source": "allocation_engine",
                "value": allocation,
            })

        if allocation > 25:
            semantic_states.append({
                "signal_id": "concentration_risk_elevated",
                "category": "concentration",
                "meaning": f"{category} exposure is structurally elevated.",
                "source": "allocation_engine",
                "value": allocation,
            })

    return semantic_states


def interpret_narrative_dependency_signals(allocation_df, attribution_df=None, correlation_df=None):
    """Interpret signals for narrative dependency semantic states (Phase C expansion).

    Detects semiconductor_dependency_high, energy_grid_dependency, and
    datacenter_infrastructure_exposure based on allocation thresholds and
    attribution/correlation signals.

    Args:
        allocation_df: DataFrame with columns 'Category' and 'Allocation %'.
        attribution_df: Optional DataFrame with attribution signals.
        correlation_df: Optional DataFrame with correlation signals.

    Returns:
        List of semantic state dicts for narrative dependency states.
    """
    semantic_states = []

    # Track relevant allocations
    semiconductor_allocation = 0.0
    energy_allocation = 0.0
    datacenter_allocation = 0.0

    for _, row in allocation_df.iterrows():
        category = row["Category"]
        allocation = float(row["Allocation %"])

        if category in ("Semiconductor", "Semiconductors", "Chips", "AI Infrastructure"):
            semiconductor_allocation += allocation
        if category in ("Energy", "Energy Infrastructure", "Power", "Grid", "Utilities"):
            energy_allocation += allocation
        if category in ("Datacenter", "Data Center", "Cloud Infrastructure", "Hyperscaler"):
            datacenter_allocation += allocation

    # semiconductor_dependency_high: emitted when semiconductor allocation is concentrated
    if semiconductor_allocation > 20:
        registry_entry = SEMANTIC_SIGNAL_REGISTRY["semiconductor_dependency_high"]
        semantic_states.append({
            "signal_id": registry_entry["signal_id"],
            "category": registry_entry["category"],
            "meaning": registry_entry["meaning"],
            "source": "allocation_engine",
            "value": semiconductor_allocation,
        })

    # energy_grid_dependency: emitted when energy infrastructure allocation is significant
    if energy_allocation > 15:
        registry_entry = SEMANTIC_SIGNAL_REGISTRY["energy_grid_dependency"]
        semantic_states.append({
            "signal_id": registry_entry["signal_id"],
            "category": registry_entry["category"],
            "meaning": registry_entry["meaning"],
            "source": "allocation_engine",
            "value": energy_allocation,
        })

    # datacenter_infrastructure_exposure: emitted when datacenter allocation is concentrated
    if datacenter_allocation > 15:
        registry_entry = SEMANTIC_SIGNAL_REGISTRY["datacenter_infrastructure_exposure"]
        semantic_states.append({
            "signal_id": registry_entry["signal_id"],
            "category": registry_entry["category"],
            "meaning": registry_entry["meaning"],
            "source": "allocation_engine",
            "value": datacenter_allocation,
        })

    return semantic_states


def get_registry_entry(signal_id: str) -> dict | None:
    """Retrieve a semantic state definition from the registry.

    Args:
        signal_id: The signal_id to look up.

    Returns:
        The registry entry dict, or None if not found.
    """
    return SEMANTIC_SIGNAL_REGISTRY.get(signal_id)


def get_all_registry_entries() -> dict:
    """Return the complete Semantic Signal Registry.

    Returns:
        Dict mapping signal_id to complete signal structure.
    """
    return SEMANTIC_SIGNAL_REGISTRY.copy()


def get_protected_state_ids() -> list[str]:
    """Return the list of protected state signal_ids (Hardening 8).

    These states must NOT be modified during any expansion phase.

    Returns:
        List of protected signal_id strings.
    """
    return [
        "ai_dependency_high",
        "deployment_fully_extended",
        "concentration_risk_elevated",
        "portfolio_health_fragile",
        "defense_dependency_elevated",
    ]


def get_new_state_ids() -> list[str]:
    """Return the list of new state signal_ids added in Phase C.

    Returns:
        List of new signal_id strings.
    """
    return [
        "semiconductor_dependency_high",
        "energy_grid_dependency",
        "datacenter_infrastructure_exposure",
    ]
