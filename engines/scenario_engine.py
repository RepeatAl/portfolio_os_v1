def run_scenario_engine(allocation_data, regime_data):

    allocation = allocation_data["allocation"]
    regime_comment = regime_data["Regime Comment"]

    scenarios = []

    # =========================
    # SCENARIO 1: CONCENTRATION RISK
    # =========================

    for item in allocation:

        category = item["Category"]
        weight = item["Allocation %"]

        if weight > 25:
            scenarios.append({
                "scenario": f"If {category} declines 10%",
                "impact": f"Portfolio may experience disproportionate drawdown due to {weight}% exposure."
            })

    # =========================
    # SCENARIO 2: MACRO SHIFT
    # =========================

    if "neutral" in regime_comment.lower():

        scenarios.append({
            "scenario": "If macro environment turns risk-off",
            "impact": "Growth and cyclical exposures may underperform simultaneously."
        })

    # =========================
    # OUTPUT
    # =========================

    scenario_result = {
        "scenarios": scenarios
    }

    print("\n=== SCENARIO ENGINE ===")
    for s in scenarios:
        print(f"- {s['scenario']}: {s['impact']}")

    print("\nScenario Engine modularisiert.")

    return scenario_result


if __name__ == "__main__":
    print("Run via main orchestrator.")