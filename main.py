import pandas as pd
import yfinance as yf
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

watchlist = pd.read_excel(
    "watchlist.xlsx"
)

results = []

# =========================
# PORTFOLIO ENGINE
# =========================

for _, row in watchlist.iterrows():

    symbol = row["Ticker"]

    quantity = row["Quantity"]

    entry_price = row["Entry Price"]

    category = row["Category"]

    trigger = row["Trigger"]

    ticker = yf.Ticker(symbol)

    data = ticker.history(period="1mo")

    current_price = (
        data["Close"].iloc[-1]
    )

    market_value = (
        current_price * quantity
    )

    results.append({
        "Ticker": symbol,
        "Category": category,
        "Trigger": trigger,
        "Market Value €": round(
            market_value,
            2
        )
    })

portfolio_df = pd.DataFrame(results)

# =========================
# TOTAL VALUE
# =========================

total_value = (
    portfolio_df["Market Value €"]
    .sum()
)

# =========================
# CATEGORY ALLOCATION
# =========================

allocation_df = (
    portfolio_df
    .groupby("Category")
    ["Market Value €"]
    .sum()
    .reset_index()
)

allocation_df[
    "Allocation %"
] = (
    allocation_df["Market Value €"]
    / total_value
) * 100

allocation_df[
    "Allocation %"
] = allocation_df[
    "Allocation %"
].round(2)

# =========================
# GOVERNANCE RULES
# =========================

governance_flags = []

for _, row in allocation_df.iterrows():

    category = row["Category"]

    allocation = row["Allocation %"]

    # ---------------------

    if allocation > 35:

        governance_flags.append(
            f"{category} exceeds "
            f"healthy concentration limits."
        )

    elif allocation > 25:

        governance_flags.append(
            f"{category} currently overweight."
        )

# =========================
# REGIME CONTEXT
# =========================

dax = yf.Ticker("^GDAXI")

dax_data = dax.history(period="10d")

dax_return = (
    (
        dax_data["Close"].iloc[-1]
        - dax_data["Close"].iloc[0]
    )
    / dax_data["Close"].iloc[0]
) * 100

bunds = yf.Ticker("^TNX")

bund_data = bunds.history(period="10d")

bund_return = (
    (
        bund_data["Close"].iloc[-1]
        - bund_data["Close"].iloc[0]
    )
    / bund_data["Close"].iloc[0]
) * 100

regime_comment = (
    "Neutral allocation environment."
)

if (
    dax_return > 2
    and bund_return < 0
):

    regime_comment = (
        "Current liquidity regime supports "
        "moderate AI/Growth overweighting."
    )

# =========================
# HEALTH SCORE
# =========================

health_score = 100

health_score -= (
    len(governance_flags) * 10
)

if health_score < 50:

    health_score = 50

# =========================
# GOVERNANCE SUMMARY
# =========================

if len(governance_flags) == 0:

    governance_flags.append(
        "Portfolio allocation currently balanced."
    )

governance_df = pd.DataFrame({
    "Governance Signals": governance_flags
})

# =========================
# BRIEFING
# =========================

briefing = f"""
ALLOCATION GOVERNANCE ENGINE — {today}

Portfolio Health Score:
{health_score}/100

Allocation Regime:
{regime_comment}

Governance Signals:

{' '.join(governance_flags)}

Observation:
Portfolio governance now evaluates
allocation quality, concentration,
and regime-adjusted positioning.
"""

# =========================
# EXPORTS
# =========================

allocation_df.to_excel(
    "allocation_engine.xlsx",
    index=False
)

governance_df.to_excel(
    "allocation_governance.xlsx",
    index=False
)

with open(
    "allocation_briefing.txt",
    "w"
) as file:

    file.write(briefing)

# =========================
# TERMINAL
# =========================

print("\n=== ALLOCATION ENGINE ===")
print(allocation_df)

print("\n=== GOVERNANCE ENGINE ===")
print(governance_df)

print("\n=== ALLOCATION BRIEFING ===")
print(briefing)

print("\nAllocation Governance Intelligence aktualisiert.")