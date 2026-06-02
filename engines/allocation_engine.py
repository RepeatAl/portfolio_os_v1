import pandas as pd

from engines.semantic_engine import interpret_allocation_signals


WATCHLIST_PATH = "watchlist.xlsx"


def load_watchlist(path=WATCHLIST_PATH):
    return pd.read_excel(path)


def build_allocation_table(watchlist_df):
    required_columns = ["Category", "Market Value €"]

    for column in required_columns:
        if column not in watchlist_df.columns:
            raise ValueError(f"Missing required column: {column}")

    allocation_df = (
        watchlist_df
        .groupby("Category", as_index=False)["Market Value €"]
        .sum()
    )

    total_value = allocation_df["Market Value €"].sum()

    if total_value == 0:
        allocation_df["Allocation %"] = 0.0
    else:
        allocation_df["Allocation %"] = (
            allocation_df["Market Value €"] / total_value * 100
        ).round(2)

    return allocation_df


def build_governance_signals(allocation_df):
    signals = []

    for _, row in allocation_df.iterrows():
        category = row["Category"]
        allocation = float(row["Allocation %"])

        if allocation > 25:
            signals.append({
                "Governance Signals": f"{category} currently overweight."
            })

    return pd.DataFrame(signals)


def run_allocation_engine():
    watchlist_df = load_watchlist()
    allocation_df = build_allocation_table(watchlist_df)
    governance_df = build_governance_signals(allocation_df)
    semantic_states = interpret_allocation_signals(allocation_df)

    print("\n=== ALLOCATION ENGINE ===")
    print(allocation_df)

    print("\n=== GOVERNANCE ENGINE ===")
    print(governance_df)

    print("\n=== SEMANTIC STATES ===")
    for state in semantic_states:
        print(state)

    allocation_df.to_excel("allocation_engine.xlsx", index=False)
    governance_df.to_excel("allocation_governance.xlsx", index=False)

    print("\nAllocation Engine modularisiert.")


if __name__ == "__main__":
    run_allocation_engine()