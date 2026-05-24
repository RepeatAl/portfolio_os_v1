def run_decision_engine(priority_data, scenario_data):

    priorities = priority_data["priorities"]
    scenarios = scenario_data["scenarios"]

    decisions = []

    # =========================
    # PRIMARY ACTION
    # =========================

    if len(priorities) > 0:

        top_priority = priorities[0]["message"]

        decisions.append({
            "type": "primary_action",
            "message": f"Primary focus: {top_priority}"
        })

    # =========================
    # RISK FRAME
    # =========================

    if len(scenarios) > 0:

        decisions.append({
            "type": "risk_frame",
            "message": "Downside scenarios indicate concentration-driven vulnerability."
        })

    # =========================
    # STRATEGIC STANCE
    # =========================

    if any("uncertainty" in p["message"].lower() for p in priorities):

        decisions.append({
            "type": "strategy",
            "message": "Maintain cautious positioning until macro clarity improves."
        })
    else:

        decisions.append({
            "type": "strategy",
            "message": "Portfolio positioning can remain constructive."
        })

    # =========================
    # OUTPUT
    # =========================

    decision_result = {
        "decisions": decisions
    }

    print("\n=== DECISION ENGINE ===")
    for d in decisions:
        print(f"- {d['message']}")

    print("\nDecision Engine modularisiert.")

    return decision_result


if __name__ == "__main__":
    print("Run via main orchestrator.")