def run_priority_engine(allocation_data, attribution_data):

    allocation = allocation_data["allocation"]
    insights = attribution_data["insights"]

    priorities = []

    # =========================
    # PRIORITY: CONCENTRATION RISK
    # =========================

    for item in allocation:

        category = item["Category"]
        weight = item["Allocation %"]

        if weight > 25:
            priorities.append({
                "type": "risk",
                "message": f"Reduce concentration in {category} ({weight}%)."
            })

    # =========================
    # PRIORITY: REGIME MISMATCH
    # =========================

    for insight in insights:

        if "uncertain macro regime" in insight:
            priorities.append({
                "type": "context",
                "message": "Reassess portfolio positioning under current macro uncertainty."
            })

    # =========================
    # OUTPUT
    # =========================

    priority_result = {
        "priorities": priorities
    }

    print("\n=== PRIORITY ENGINE ===")
    for p in priorities:
        print(f"- {p['message']}")

    print("\nPriority Engine modularisiert.")

    return priority_result


if __name__ == "__main__":
    print("Run via main orchestrator.")