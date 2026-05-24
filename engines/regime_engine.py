import yfinance as yf


def run_regime_engine():

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

    regime_comment = "Neutral allocation environment."

    if dax_return > 2 and bund_return < 0:
        regime_comment = (
            "Current liquidity regime supports "
            "moderate AI/Growth overweighting."
        )

    # =========================
    # NORMALIZED OUTPUT (WICHTIG)
    # =========================

    regime_result = {
        "DAX 10D Return %": float(round(dax_return, 2)),
        "Rate Proxy 10D Return %": float(round(bund_return, 2)),
        "Regime Comment": regime_comment
    }

    # =========================
    # OUTPUT
    # =========================

    print("\n=== REGIME ENGINE ===")
    print(regime_result)

    print("\nRegime Engine modularisiert.")

    return regime_result


if __name__ == "__main__":
    run_regime_engine()