def run_visual_engine(allocation_data, decision_data, scenario_data):

    visuals = []

    # =========================
    # NEXT MOVE VISUAL
    # =========================

    for decision in decision_data["decisions"]:

        if decision["type"] == "primary_action":

            visuals.append({
                "type": "next_move",
                "title": "Next Move",
                "message": decision["message"]
            })

    # =========================
    # RISK VISUAL
    # =========================

    for scenario in scenario_data["scenarios"]:

        visuals.append({
            "type": "risk_scenario",
            "scenario": scenario["scenario"],
            "impact": scenario["impact"]
        })

    print("\n=== VISUAL ENGINE ===")
    for v in visuals:
        print("-", v)

    print("\nVisual Engine modularisiert.")

    return {
        "visuals": visuals
    }


if __name__ == "__main__":
    print("Run via orchestrator.")