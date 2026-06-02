import streamlit as st
import pandas as pd

# ---------------------------------------------------
# ENGINE IMPORTS
# ---------------------------------------------------

from engines.allocation_engine import run_allocation_engine
from engines.regime_engine import run_regime_engine
from engines.attribution_engine import run_attribution_engine
from engines.priority_engine import run_priority_engine
from engines.scenario_engine import run_scenario_engine
from engines.decision_engine import run_decision_engine
from engines.scoring_engine import run_scoring_engine
from engines.quality_engine import run_quality_engine
from engines.visual_engine import run_visual_engine
from engines.report_engine import run_report_engine

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(

    page_title="Portfolio OS",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📊 Portfolio Operating System")

# ---------------------------------------------------
# PIPELINE EXECUTION
# ---------------------------------------------------

allocation = run_allocation_engine()

regime = run_regime_engine(
    allocation
)

attribution = run_attribution_engine(
    allocation,
    regime
)

priority = run_priority_engine(
    allocation,
    attribution
)

scenario = run_scenario_engine(
    allocation,
    regime,
    attribution
)

decision = run_decision_engine(
    allocation,
    scenario,
    priority
)

scoring = run_scoring_engine(
    allocation,
    decision
)

quality = run_quality_engine(
    allocation,
    scenario,
    decision
)

visuals = run_visual_engine(
    allocation,
    decision,
    scenario,
    quality
)

report = run_report_engine(
    allocation,
    regime,
    decision,
    quality,
    scenario
)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Risk Level",
        visuals["risk_bar"]["level"]
    )

with col2:

    st.metric(
        "Confidence Score",
        visuals["risk_bar"]["value"]
    )

with col3:

    st.metric(
        "Primary Action",
        visuals["next_move"]["message"]
    )

# ---------------------------------------------------
# NEXT MOVE
# ---------------------------------------------------

st.subheader("🎯 Next Move")

st.info(
    visuals["next_move"]["message"]
)

# ---------------------------------------------------
# PORTFOLIO ALLOCATION
# ---------------------------------------------------

st.subheader("📈 Portfolio Allocation")

allocation_df = pd.DataFrame(
    visuals["portfolio_pie"]
)

st.bar_chart(
    allocation_df.set_index("category")
)

st.dataframe(
    allocation_df,
    width="stretch"
)

# ---------------------------------------------------
# TARGET VS ACTUAL
# ---------------------------------------------------

st.subheader("⚖️ Target vs Actual Allocation")

target_vs_actual_df = pd.DataFrame(
    visuals["target_vs_actual"]
)

if not target_vs_actual_df.empty:

    st.dataframe(
        target_vs_actual_df,
        width="stretch"
    )

else:

    st.write(
        "No target allocation data available."
    )

# ---------------------------------------------------
# RISK ASSESSMENT
# ---------------------------------------------------

st.subheader("⚠️ Risk Assessment")

risk_value = visuals["risk_bar"]["value"]

st.progress(
    min(risk_value / 100, 1.0)
)

st.write(
    visuals["risk_bar"]["message"]
)

# ---------------------------------------------------
# MARKET SCENARIOS
# ---------------------------------------------------

st.subheader("🧠 Market Scenarios")

for scenario_item in visuals["scenarios"]:

    st.markdown(
        f"### {scenario_item['title']}"
    )

    st.write(
        scenario_item["message"]
    )

# ---------------------------------------------------
# ACTION SIMULATION
# ---------------------------------------------------

st.subheader("🔮 Action Simulation")

if visuals["action_simulation"]:

    for sim in visuals["action_simulation"]:

        st.markdown(
            "### If you follow the recommendation"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Before")

            st.write(
                sim["before"]
            )

        with col2:

            st.markdown("#### After")

            st.write(
                sim["after"]
            )

        st.success(
            sim["impact"]
        )

else:

    st.write(
        "No simulation available."
    )

# ---------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------

st.subheader("🧾 Portfolio Intelligence Report")

st.code(
    report["report"]
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Portfolio OS v1"
)