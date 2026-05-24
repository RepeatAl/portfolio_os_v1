from pathlib import Path
from datetime import datetime


def run_report_engine(allocation_data, regime_data, decision_data, quality_data):

    today = datetime.now().strftime("%Y-%m-%d")

    report = f"""
PORTFOLIO INTELLIGENCE REPORT — {today}
=====================================

REGIME
------
{regime_data['Regime Comment']}

KEY DECISION
------------
{decision_data['decisions'][0]['message']}

RISK CONTEXT
------------
{decision_data['decisions'][1]['message']}

STRATEGIC STANCE
----------------
{decision_data['decisions'][2]['message']}

CONFIDENCE
----------
Score: {quality_data['confidence_score']}
Level: {quality_data['confidence_level']}

DETAIL FLAGS
------------
"""

    for f in quality_data["flags"]:
        report += f"- {f}\n"

    # =========================
    # FILE STORAGE (NEU)
    # =========================

    root_path = Path(__file__).resolve().parent.parent

    history_path = root_path / "history"
    history_path.mkdir(exist_ok=True)

    file_name = f"report_{today}.txt"
    full_path = history_path / file_name

    with open(full_path, "w") as file:
        file.write(report)

    print("\n=== FINAL REPORT ===")
    print(report)

    print(f"\nReport saved to: {full_path}")

    return {
        "report": report,
        "path": str(full_path),
        "date": today
    }


if __name__ == "__main__":
    print("Run via main orchestrator.")