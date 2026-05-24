def run_quality_engine(allocation_data, priority_data, scoring_data):

    priorities = priority_data["priorities"]
    scores = scoring_data["scores"]

    quality_flags = []

    confidence = 0

    # =========================
    # SIGNAL STRENGTH
    # =========================

    high_scores = [s for s in scores if s["score"] >= 70]

    if len(high_scores) >= 2:
        confidence += 40
        quality_flags.append("Multiple high-impact signals detected.")

    # =========================
    # CONSISTENCY CHECK
    # =========================

    if len(priorities) > 0:
        confidence += 30
        quality_flags.append("Priority signals are present and actionable.")

    # =========================
    # CONCENTRATION CONFIRMATION
    # =========================

    allocation = allocation_data["allocation"]

    concentration = any(item["Allocation %"] > 25 for item in allocation)

    if concentration:
        confidence += 30
        quality_flags.append("Concentration risk confirmed by allocation data.")

    # =========================
    # FINAL CONFIDENCE
    # =========================

    if confidence >= 80:
        level = "HIGH"
    elif confidence >= 50:
        level = "MEDIUM"
    else:
        level = "LOW"

    # =========================
    # OUTPUT
    # =========================

    quality_result = {
        "confidence_score": confidence,
        "confidence_level": level,
        "flags": quality_flags
    }

    print("\n=== QUALITY ENGINE ===")
    print(f"Confidence: {confidence} ({level})")

    for f in quality_flags:
        print(f"- {f}")

    print("\nQuality Engine modularisiert.")

    return quality_result


if __name__ == "__main__":
    print("Run via main orchestrator.")