def run_quality_engine(allocation, scenario, decision):

    print("\n=== QUALITY ENGINE ===")

    confidence_score = 50

    # ---------------------------------------------------
    # DECISION ANALYSIS
    # ---------------------------------------------------

    decisions = decision.get(
        "decisions",
        []
    )

    for d in decisions:

        message = d.get(
            "message",
            ""
        ).lower()

        if "reduce" in message:
            confidence_score += 15

        if "risk" in message:
            confidence_score += 10

        if "acceptable" in message:
            confidence_score -= 5

    # ---------------------------------------------------
    # SCENARIO DEPTH
    # ---------------------------------------------------

    scenarios = scenario.get(
        "scenarios",
        []
    )

    if len(scenarios) > 0:
        confidence_score += 10

    # ---------------------------------------------------
    # ALLOCATION COMPLEXITY
    # ---------------------------------------------------

    allocation_data = allocation.get(
        "allocation",
        []
    )

    if len(allocation_data) >= 5:
        confidence_score += 5

    # ---------------------------------------------------
    # NORMALIZE
    # ---------------------------------------------------

    confidence_score = max(
        0,
        min(confidence_score, 100)
    )

    result = {

        "confidence_score": confidence_score,

        "quality_label": (
            "HIGH"
            if confidence_score >= 80
            else "MEDIUM"
            if confidence_score >= 50
            else "LOW"
        )
    }

    print(f"Confidence Score: {confidence_score}")

    print("Quality Engine modularisiert.")

    return result