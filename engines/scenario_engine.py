def run_scenario_engine(allocation, regime, attribution):

    print("\n=== SCENARIO ENGINE ===")

    scenarios = []

    action_scenarios = []

    regime_comment = regime.get(
        "Regime Comment",
        "Neutral environment."
    )

    # ---------------------------------------------------
    # BASE MARKET SCENARIOS
    # ---------------------------------------------------

    if "neutral" in regime_comment.lower():

        scenarios.append({

            "scenario": "Neutral Market Regime",

            "impact": (
                "Markets remain range-bound. "
                "Selective positioning remains important."
            )
        })

    else:

        scenarios.append({

            "scenario": "Macro Stress Regime",

            "impact": (
                "Higher volatility and defensive positioning expected."
            )
        })

    # ---------------------------------------------------
    # TARGET VS ACTUAL
    # ---------------------------------------------------

    target_vs_actual = allocation.get(
        "target_vs_actual"
    )

    if target_vs_actual is None:
        target_vs_actual = []

    # ---------------------------------------------------
    # ACTION SIMULATION
    # ---------------------------------------------------

    for row in target_vs_actual:

        difference = row.get(
            "Difference %",
            0
        )

        if difference > 10:

            action_scenarios.append({

                "before": (
                    f"{row['Risk Level']} exposure "
                    f"is currently {row['Actual %']}%"
                ),

                "after": (
                    f"Reducing exposure closer to "
                    f"{row['Target %']}%"
                ),

                "impact": (
                    "Portfolio concentration risk improves "
                    "and resilience increases."
                )
            })

    # ---------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------

    result = {

        "scenarios": scenarios,

        "action_scenarios": action_scenarios
    }

    print("Scenario Engine modularisiert.")

    return result