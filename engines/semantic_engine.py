def interpret_allocation_signals(allocation_df):
    semantic_states = []

    for _, row in allocation_df.iterrows():
        category = row["Category"]
        allocation = float(row["Allocation %"])

        if category == "Defense" and allocation > 25:
            semantic_states.append({
                "signal_id": "defense_dependency_elevated",
                "category": "narrative_dependency",
                "meaning": "Portfolio performance increasingly depends on continued defense-sector strength.",
                "source": "allocation_engine",
                "value": allocation,
            })

        if category == "Semiconductor" and allocation > 25:
            semantic_states.append({
                "signal_id": "semiconductor_dependency_elevated",
                "category": "narrative_dependency",
                "meaning": "Portfolio performance increasingly depends on semiconductor and AI infrastructure leadership.",
                "source": "allocation_engine",
                "value": allocation,
            })

        if allocation > 25:
            semantic_states.append({
                "signal_id": "concentration_risk_elevated",
                "category": "concentration",
                "meaning": f"{category} exposure is structurally elevated.",
                "source": "allocation_engine",
                "value": allocation,
            })

    return semantic_states