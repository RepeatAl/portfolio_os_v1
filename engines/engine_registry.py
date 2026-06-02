ENGINE_REGISTRY = {

    "allocation": {
        "function": "run_allocation_engine",
        "dependencies": []
    },

    "regime": {
        "function": "run_regime_engine",
        "dependencies": []
    },

    "attribution": {
        "function": "run_attribution_engine",
        "dependencies": ["allocation", "regime"]
    },

    "priority": {
        "function": "run_priority_engine",
        "dependencies": ["allocation", "attribution"]
    },

    "scenario": {
        "function": "run_scenario_engine",
        "dependencies": ["allocation", "regime"]
    },

    "decision": {
        "function": "run_decision_engine",
        "dependencies": ["priority", "scenario"]
    },

    "scoring": {
        "function": "run_scoring_engine",
        "dependencies": ["priority", "scenario"]
    },

    "quality": {
        "function": "run_quality_engine",
        "dependencies": ["allocation", "priority", "scoring"]
    },

    "report": {
        "function": "run_report_engine",
        "dependencies": ["allocation", "regime", "decision", "quality"]
    },

    "delta": {
        "function": "run_delta_engine",
        "dependencies": ["report"]
    },

    "morning_briefing": {
        "function": "run_morning_briefing_engine",
        "dependencies": ["report", "scoring", "delta"]
    },

    "visual": {
        "function": "run_visual_engine",
        "dependencies": ["allocation", "decision", "scenario"]
    }

}