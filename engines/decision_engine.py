def run_decision_engine(allocation, scenario, priority):

    print("\n=== DECISION ENGINE ===")

    decisions = []

    # ---------------------------------------------------
    # LOAD PRIORITIES
    # ---------------------------------------------------

    priorities = priority.get(
        "priorities",
        []
    )

    # ---------------------------------------------------
    # LOAD SCENARIOS
    # ---------------------------------------------------

    action_scenarios = scenario.get(
        "action_scenarios",
        []
    )

    # ---------------------------------------------------
    # PRIMARY ACTION
    # ---------------------------------------------------

    if priorities:

        top_priority = priorities[0]

        decisions.append({

            "type": "primary_action",

            "message": top_priority.get(
                "message",
                "No action available."
            ),

            "priority_type": top_priority.get(
                "type",
                "general"
            )
        })

    else:

        decisions.append({

            "type": "primary_action",

            "message": (
                "Portfolio currently appears balanced."
            ),

            "priority_type": "balanced"
        })

    # ---------------------------------------------------
    # RISK INTERPRETATION
    # ---------------------------------------------------

    if action_scenarios:

        decisions.append({

            "type": "risk_adjustment",

            "message": (
                "Portfolio adjustments may improve "
                "overall resilience."
            )
        })

    else:

        decisions.append({

            "type": "hold",

            "message": (
                "Current positioning remains acceptable."
            )
        })

    # ---------------------------------------------------
    # FINAL DECISION STATE
    # ---------------------------------------------------

    result = {

        "decisions": decisions,

        "primary_action": decisions[0]["message"],

        "decision_count": len(decisions)
    }

    print("\n=== DECISION OUTPUT ===")

    for d in decisions:

        print(f"- {d['message']}")

    print("\nDecision Engine modularisiert.")

    return result