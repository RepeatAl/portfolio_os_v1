from datetime import datetime


def run_report_engine(
    allocation_data,
    regime_data,
    decision_data,
    quality_data,
    scenario_data
):

    print("\n=== FINAL REPORT ===")

    date = datetime.today().strftime(
        "%Y-%m-%d"
    )

    # ---------------------------------------------------
    # REGIME
    # ---------------------------------------------------

    regime_comment = regime_data.get(
        "Regime Comment",
        "No regime data"
    )

    # ---------------------------------------------------
    # DECISIONS
    # ---------------------------------------------------

    decisions = decision_data.get(
        "decisions",
        []
    )

    primary = next(

        (
            d["message"]

            for d in decisions

            if d["type"] == "primary_action"
        ),

        "No primary decision"
    )

    risk_context = next(

        (
            d["message"]

            for d in decisions

            if d["type"] == "risk_adjustment"
        ),

        "No risk context"
    )

    # ---------------------------------------------------
    # QUALITY
    # ---------------------------------------------------

    confidence = quality_data.get(
        "confidence_score",
        0
    )

    quality_label = quality_data.get(
        "quality_label",
        "UNKNOWN"
    )

    # ---------------------------------------------------
    # TARGET VS ACTUAL
    # ---------------------------------------------------

    target_vs_actual = allocation_data.get(
        "target_vs_actual",
        []
    )

    allocation_summary = ""

    for row in target_vs_actual:

        allocation_summary += (

            f"- {row['Risk Level']} "
            f"allocation currently at "
            f"{row['Actual %']}% "
            f"(Target: {row['Target %']}%)\n"
        )

    # ---------------------------------------------------
    # SCENARIOS
    # ---------------------------------------------------

    scenarios = scenario_data.get(
        "scenarios",
        []
    )

    scenario_summary = ""

    for s in scenarios:

        scenario_summary += (
            f"- {s['scenario']}: "
            f"{s['impact']}\n"
        )

    # ---------------------------------------------------
    # REPORT
    # ---------------------------------------------------

    report = f"""
PORTFOLIO INTELLIGENCE REPORT — {date}
=====================================

MARKET REGIME
-------------
{regime_comment}

PRIMARY ACTION
--------------
{primary}

RISK CONTEXT
------------
{risk_context}

TARGET VS ACTUAL
----------------
{allocation_summary}

SCENARIO ANALYSIS
-----------------
{scenario_summary}

CONFIDENCE
----------
Confidence Score: {confidence}
Confidence Level: {quality_label}

PM SUMMARY
----------
Portfolio currently operates with elevated
HIGH-risk exposure and concentration pressure.

Current positioning remains functional
but should be monitored closely under
current market conditions.
"""

    print(report)

    return {

        "report": report,

        "date": date,

        "confidence": confidence
    }