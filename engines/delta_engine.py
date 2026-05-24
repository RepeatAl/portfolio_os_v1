from pathlib import Path


def run_delta_engine(report_data):

    root_path = Path(__file__).resolve().parent.parent
    history_path = root_path / "history"

    files = sorted(history_path.glob("report_*.txt"))

    # =========================
    # NO HISTORY CASE (FIX)
    # =========================

    if len(files) < 2:
        print("\n=== DELTA ENGINE ===")
        print("No previous report available for comparison.")

        return {
            "changes": ["No previous data available."]
        }

    latest = files[-1]
    previous = files[-2]

    with open(latest, "r") as f:
        current_report = f.read()

    with open(previous, "r") as f:
        previous_report = f.read()

    # =========================
    # DELTA CHECK
    # =========================

    changes = []

    if current_report != previous_report:
        changes.append("Portfolio state has changed since last report.")
    else:
        changes.append("No significant change detected.")

    print("\n=== DELTA ENGINE ===")
    for c in changes:
        print(f"- {c}")

    return {
        "changes": changes
    }


if __name__ == "__main__":
    print("Run via main orchestrator.")