def run_visual_engine(allocation, decision, scenario, quality):

    print("\n=== VISUAL ENGINE V3 ===")

    visuals = {}

    # ---------------------------------------------------
    # NEXT MOVE
    # ---------------------------------------------------

    decision_list = decision.get(
        "decisions",
        []
    )

    primary_action = "No action available"

    for d in decision_list:

        if d.get("type") == "primary_action":

            primary_action = d.get(
                "message",
                "No action available"
            )

            break

    visuals["next_move"] = {

        "title": "What you should do",

        "message": simplify_message(primary_action),

        "raw": primary_action
    }

    # ---------------------------------------------------
    # PORTFOLIO ALLOCATION
    # ---------------------------------------------------

    allocation_data = allocation.get(
        "allocation",
        []
    )

    visuals["portfolio_pie"] = [

        {
            "category": item["Category"],
            "value": item["Allocation %"]
        }

        for item in allocation_data
    ]

    # ---------------------------------------------------
    # TARGET VS ACTUAL
    # ---------------------------------------------------

    target_vs_actual = allocation.get(
        "target_vs_actual"
    )

    if target_vs_actual is None:
        target_vs_actual = []

    visuals["target_vs_actual"] = target_vs_actual

    # ---------------------------------------------------
    # RISK BAR
    # ---------------------------------------------------

    confidence = quality.get(
        "confidence_score",
        0
    )

    if confidence >= 80:

        level = "HIGH"
        color = "red"
        message = "High risk detected"

    elif confidence >= 50:

        level = "MEDIUM"
        color = "orange"
        message = "Moderate risk"

    else:

        level = "LOW"
        color = "green"
        message = "Well balanced"

    visuals["risk_bar"] = {

        "level": level,
        "color": color,
        "value": confidence,
        "message": message
    }

    # ---------------------------------------------------
    # MARKET SCENARIOS
    # ---------------------------------------------------

    visuals["scenarios"] = [

        {
            "title": s["scenario"],
            "message": s["impact"]
        }

        for s in scenario.get(
            "scenarios",
            []
        )
    ]

    # ---------------------------------------------------
    # ACTION SIMULATION
    # ---------------------------------------------------

    visuals["action_simulation"] = []

    action_scenarios = scenario.get(
        "action_scenarios",
        []
    )

    for sim in action_scenarios:

        visuals["action_simulation"].append({

            "title": "If you follow the recommendation",

            "before": sim["before"],

            "after": sim["after"],

            "impact": sim["impact"]
        })

    print("Visual Engine v3 (Simulation + Dashboard) aktiv.")

    return visuals


def simplify_message(message):

    if "Reduce concentration" in message:

        return (
            "You have too much exposure "
            "in one area. Reduce it."
        )

    if "Reassess portfolio" in message:

        return (
            "Market is unclear. "
            "Stay cautious and review your positions."
        )

    return message