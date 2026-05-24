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
from engines.engine_registry import ENGINE_REGISTRY


FUNCTION_MAP = {
    "run_allocation_engine": run_allocation_engine,
    "run_regime_engine": run_regime_engine,
    "run_attribution_engine": run_attribution_engine,
    "run_priority_engine": run_priority_engine,
    "run_scenario_engine": run_scenario_engine,
    "run_decision_engine": run_decision_engine,
    "run_scoring_engine": run_scoring_engine,
    "run_quality_engine": run_quality_engine,
    "run_report_engine": run_report_engine,
    "run_delta_engine": run_delta_engine,
    "run_morning_briefing_engine": run_morning_briefing_engine,
    "run_visual_engine": run_visual_engine
}


def run_all_engines(user_portfolio):

    results = {}

    for engine_name, config in ENGINE_REGISTRY.items():

        function_name = config["function"]
        dependencies = config["dependencies"]

        func = FUNCTION_MAP[function_name]

        # =========================
        # SPECIAL CASE: ALLOCATION
        # =========================

        if engine_name == "allocation":
            result = func(user_portfolio)

        elif not dependencies:
            result = func()

        else:
            dep_results = [results[d] for d in dependencies]
            result = func(*dep_results)

        results[engine_name] = result

    return results