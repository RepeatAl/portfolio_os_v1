import pandas as pd
import yfinance as yf


def run_allocation_engine(user_portfolio):

    results = []

    # =========================
    # PORTFOLIO ENGINE (USER DATA)
    # =========================

    for asset in user_portfolio:

        symbol = asset["ticker"]
        quantity = asset["quantity"]
        category = asset["category"]

        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")

        if data.empty:
            continue

        current_price = data["Close"].iloc[-1]

        market_value = current_price * quantity

        results.append({
            "Ticker": symbol,
            "Category": category,
            "Market Value €": round(market_value, 2)
        })

    portfolio_df = pd.DataFrame(results)

    if portfolio_df.empty:
        return {
            "allocation": [],
            "governance": [{"Governance Signals": "No data available."}]
        }

    # =========================
    # TOTAL VALUE
    # =========================

    total_value = portfolio_df["Market Value €"].sum()

    # =========================
    # CATEGORY ALLOCATION
    # =========================

    allocation_df = (
        portfolio_df
        .groupby("Category")["Market Value €"]
        .sum()
        .reset_index()
    )

    allocation_df["Allocation %"] = (
        allocation_df["Market Value €"] / total_value
    ) * 100

    allocation_df["Allocation %"] = allocation_df["Allocation %"].round(2)

    # =========================
    # GOVERNANCE FLAGS
    # =========================

    governance_flags = []

    for _, row in allocation_df.iterrows():

        category = row["Category"]
        allocation = row["Allocation %"]

        if allocation > 35:
            governance_flags.append(
                f"{category} exceeds healthy concentration limits."
            )
        elif allocation > 25:
            governance_flags.append(
                f"{category} currently overweight."
            )

    if len(governance_flags) == 0:
        governance_flags.append(
            "Portfolio allocation balanced."
        )

    governance_df = pd.DataFrame({
        "Governance Signals": governance_flags
    })

    print("\n=== ALLOCATION ENGINE ===")
    print(allocation_df)

    print("\n=== GOVERNANCE ENGINE ===")
    print(governance_df)

    print("\nAllocation Engine (User Portfolio aktiv).")

    return {
        "allocation": allocation_df.to_dict(orient="records"),
        "governance": governance_df.to_dict(orient="records")
    }


if __name__ == "__main__":
    print("Run via orchestrator.")