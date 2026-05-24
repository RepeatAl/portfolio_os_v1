from datetime import datetime


def run_morning_briefing_engine(report_data, scoring_data, delta_data):

    report = report_data["report"]
    scores = scoring_data["scores"]
    changes = delta_data["changes"]

    today = datetime.now().strftime("%Y-%m-%d")

    top_item = scores[0]["item"]
    top_score = scores[0]["score"]

    briefing = f"""
MORNING BRIEFING — {today}
==========================

TOP PRIORITY
------------
{top_item} (Score: {top_score})

CHANGE VS YESTERDAY
-------------------
"""

    for c in changes:
        briefing += f"- {c}\n"

    briefing += f"""

TODAY'S FOCUS
-------------
Act on highest concentration risks first.

SYSTEM SUMMARY
--------------
{report}
"""

    print("\n=== MORNING BRIEFING ===")
    print(briefing)

    return {
        "briefing": briefing
    }


if __name__ == "__main__":
    print("Run via main orchestrator.")