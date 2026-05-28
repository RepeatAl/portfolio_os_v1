from engines.allocation_engine import run_allocation_engine
from engines.regime_engine import run_regime_engine
from engines.attribution_engine import run_attribution_engine
from engines.priority_engine import run_priority_engine
from engines.scenario_engine import run_scenario_engine
from engines.decision_engine import run_decision_engine
from engines.scoring_engine import run_scoring_engine
from engines.quality_engine import run_quality_engine
from engines.report_engine import run_report_engine
from engines.delta_engine import run_delta_engine
from engines.morning_briefing_engine import run_morning_briefing_engine
from engines.visual_engine import run_visual_engine

import warnings

# HARDENING 6 — ENGINE_RUNNER COMPATIBILITY:
# engine_runner.py remains functional but emits deprecation warnings
# for direct briefing outputs. Use pipeline_orchestrator.py for
# chain-compliant execution.
_DEPRECATION_MSG = (
    "engine_runner.run_all_engines() produces direct briefing outputs that "
    "bypass the canonical chain (SIGNALS → SEMANTICS → REASONING → REPORT). "
    "Use engines.pipeline_orchestrator.PipelineOrchestrator.execute() instead."
)


def run_all_engines(portfolio_data=None, risk_profile=None):
    warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    print("\n=== PORTFOLIO OS START ===")

    # --- ALLOCATION ---
    allocation = run_allocation_engine(portfolio_data, risk_profile)

    # --- REGIME ---
    regime = run_regime_engine()

    # --- ATTRIBUTION ---
    attribution = run_attribution_engine(allocation, regime)

    # --- PRIORITY ---
    priority = run_priority_engine(allocation, attribution)

    # --- SCENARIO ---
    scenario = run_scenario_engine(allocation)

    # --- DECISION ---
    decision = run_decision_engine(priority, scenario)

    # --- SCORING ---
    scoring = run_scoring_engine(priority, scenario)

    # --- QUALITY (FIXED HERE) ---
    quality = run_quality_engine(allocation, priority, scoring)

    # --- REPORT ---
    report = run_report_engine(regime, decision, quality)

    # --- DELTA ---
    delta = run_delta_engine(report)

    # --- MORNING BRIEFING ---
    briefing = run_morning_briefing_engine(priority, scoring, delta, report)

    # --- VISUAL ---
    visuals = run_visual_engine(allocation, decision, scenario, quality)

    print("\n=== DASHBOARD DATA ===")
    print(visuals)

    return {
        "allocation": allocation,
        "regime": regime,
        "attribution": attribution,
        "priority": priority,
        "scenario": scenario,
        "decision": decision,
        "scoring": scoring,
        "quality": quality,
        "report": report,
        "delta": delta,
        "morning_briefing": briefing,
        "visual": visuals
    }