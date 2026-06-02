def run_scoring_engine(allocation, decision):

    print("\n=== SCORING ENGINE ===")

    decisions = decision.get(
        "decisions",
        []
    )

    score = 50

    for d in decisions:

        message = d.get(
            "message",
            ""
        ).lower()

        if "reduce" in message:
            score += 20

        if "risk" in message:
            score += 10

        if "acceptable" in message:
            score -= 10

    score = min(score, 100)

    result = {

        "portfolio_score": score,

        "score_label": (
            "Strong Action Needed"
            if score >= 70
            else "Moderate Review"
        )
    }

    print(f"Portfolio Score: {score}")

    print("Scoring Engine modularisiert.")

    return result