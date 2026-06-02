def run_morning_briefing_engine(priority_data, scoring_data, delta_data, report_data):
    print("\n=== MORNING BRIEFING ===")

    priorities = priority_data.get("priorities", [])
    scores = scoring_data.get("scores", [])
    changes = delta_data.get("changes", ["No previous data available."])
    report_text = report_data.get("report", "")

    # --- TOP PRIORITY ---
    if scores:
        top = max(scores, key=lambda x: x["score"])
        top_priority = f"{top['item']} (Score: {top['score']})"
    else:
        top_priority = "No priority available"

    # --- BUILD BRIEFING ---
    briefing = f"""
MORNING BRIEFING — TODAY
==========================

TOP PRIORITY
------------
{top_priority}

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
{report_text}
"""

    print(briefing)

    return {
        "briefing": briefing
    }