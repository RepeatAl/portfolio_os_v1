def run_scoring_engine(priority_data, scenario_data):

    priorities = priority_data["priorities"]
    scenarios = scenario_data["scenarios"]

    scores = []

    # =========================
    # PRIORITY SCORING
    # =========================

    for p in priorities:

        score = 0

        if p["type"] == "risk":
            score += 70

        if "Reduce concentration" in p["message"]:
            score += 20

        if p["type"] == "context":
            score += 40

        scores.append({
            "item": p["message"],
            "score": score
        })

    # =========================
    # SCENARIO SCORING
    # =========================

    for s in scenarios:

        score = 0

        if "disproportionate drawdown" in s["impact"]:
            score += 60

        if "macro" in s["scenario"].lower():
            score += 50

        scores.append({
            "item": s["scenario"],
            "score": score
        })

    # =========================
    # SORTING
    # =========================

    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    # =========================
    # OUTPUT
    # =========================

    scoring_result = {
        "scores": scores
    }

    print("\n=== SCORING ENGINE ===")
    for s in scores:
        print(f"- {s['item']} → Score: {s['score']}")

    print("\nScoring Engine modularisiert.")

    return scoring_result


if __name__ == "__main__":
    print("Run via main orchestrator.")