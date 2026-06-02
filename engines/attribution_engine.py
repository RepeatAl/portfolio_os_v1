def run_attribution_engine(allocation_data, regime_data):

    allocation = allocation_data["allocation"]
    governance = allocation_data["governance"]

    regime_comment = regime_data["Regime Comment"]

    insights = []

    # =========================
    # CONCENTRATION ANALYSIS
    # =========================

    for item in allocation:

        category = item["Category"]
        weight = item["Allocation %"]

        if weight > 25:
            insights.append(
                f"{category} is a dominant allocation driver ({weight}%)."
            )

    # =========================
    # REGIME ALIGNMENT
    # =========================

    if "Growth overweighting" in regime_comment:

        insights.append(
            "Portfolio positioning aligns with growth-supportive liquidity regime."
        )
    else:

        insights.append(
            "Portfolio positioning operates in a neutral or uncertain macro regime."
        )

    # =========================
    # GOVERNANCE CROSS-CHECK
    # =========================

    if len(governance) > 0:
        insights.append(
            "Governance flags indicate concentration risks that may impact resilience."
        )

    # =========================
    # OUTPUT
    # =========================

    attribution_result = {
        "insights": insights
    }

    print("\n=== ATTRIBUTION ENGINE ===")
    for insight in insights:
        print(f"- {insight}")

    print("\nAttribution Engine modularisiert.")

    return attribution_result


if __name__ == "__main__":
    print("Run via main orchestrator.")