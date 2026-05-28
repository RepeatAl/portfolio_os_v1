"""
Script to add report_value metadata to all artifacts missing it in artifact_registry.yaml.
Achieves 100% report_value field population per Requirement 4.6.

Categories are assigned based on artifact domain, type, and purpose:
- semantic_interpretation: Artifacts that transform raw signals into semantic meaning
- pm_reasoning: Artifacts that produce portfolio manager-facing reasoning/conclusions
- concentration_explanation: Artifacts explaining portfolio concentration and correlation
- dependency_explanation: Artifacts explaining narrative/trigger dependencies
- scenario_interpretation: Artifacts related to scenario analysis and stress testing
- confidence_explanation: Artifacts related to confidence scoring and degradation
- action_space_clarity: Artifacts defining or enabling action/deployment decisions
- multilingual_rendering: Artifacts related to report rendering and localization
- traceability: Artifacts enabling governance, provenance, or audit trail
- user_understanding: Artifacts enabling user-facing visualization or comprehension
"""

import yaml
import sys
from pathlib import Path

REGISTRY_PATH = Path(".domainization/artifact_registry.yaml")

# Mapping of artifact_id to report_value metadata
REPORT_VALUE_MAP = {
    # SSOT DOCUMENT
    "system_architecture_md": {
        "category": "traceability",
        "justification": "Defines system component relationships enabling architectural provenance for all pipeline artifacts",
    },
    # SIGNAL ENGINES
    "allocation_engine_py": {
        "category": "semantic_interpretation",
        "justification": "Produces allocation structure signals consumed by semantic engine for portfolio composition interpretation",
    },
    "regime_engine_py": {
        "category": "semantic_interpretation",
        "justification": "Produces market regime classification signals consumed by semantic engine for regime state interpretation",
    },
    "attribution_engine_py": {
        "category": "pm_reasoning",
        "justification": "Produces attribution signals identifying performance drivers rendered in Portfolio Structure section",
    },
    "scoring_engine_py": {
        "category": "action_space_clarity",
        "justification": "Produces scoring signals enabling action prioritization in the Action Space report section",
    },
    # REASONING ENGINES
    "decision_engine_py": {
        "category": "pm_reasoning",
        "justification": "Produces Reasoning Objects with actionable portfolio decisions rendered in daily report sections",
    },
    "quality_engine_py": {
        "category": "confidence_explanation",
        "justification": "Evaluates reasoning quality and confidence levels rendered in Confidence Interpretation section",
    },
    "priority_engine_py": {
        "category": "action_space_clarity",
        "justification": "Prioritizes actions and risks rendered in Action Space and Executive Summary sections",
    },
    # REPORT ENGINES
    "morning_briefing_engine_py": {
        "category": "pm_reasoning",
        "justification": "Generates morning briefing summaries providing portfolio manager daily context",
    },
    "delta_engine_py": {
        "category": "pm_reasoning",
        "justification": "Detects changes between consecutive reports enabling portfolio manager awareness of shifts",
    },
    "pm_report_engine_py": {
        "category": "pm_reasoning",
        "justification": "Generates portfolio manager report with structured reasoning conclusions",
    },
    # SIMULATION ENGINE
    "scenario_engine_py": {
        "category": "scenario_interpretation",
        "justification": "Generates scenario analysis and stress testing rendered in Scenario Analysis report section",
    },
    # UI ENGINE
    "visual_engine_py": {
        "category": "user_understanding",
        "justification": "Generates visualization data structures enabling dashboard comprehension of portfolio state",
    },
    # ARCHITECTURE ENGINES
    "engine_registry_py": {
        "category": "traceability",
        "justification": "Defines engine dependencies and execution order enabling pipeline provenance validation",
    },
    "engine_runner_py": {
        "category": "traceability",
        "justification": "Orchestrates engine execution flow providing execution audit trail for pipeline runs",
    },
    # REPORT OUTPUTS
    "portfolio_report_txt": {
        "category": "pm_reasoning",
        "justification": "Daily portfolio report output delivering structured reasoning conclusions to portfolio manager",
    },
    "morning_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Morning briefing output delivering daily portfolio context to portfolio manager",
    },
    "allocation_briefing_txt": {
        "category": "concentration_explanation",
        "justification": "Allocation briefing explaining portfolio composition structure to portfolio manager",
    },
    "attribution_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Attribution briefing explaining performance drivers to portfolio manager",
    },
    "correlation_briefing_txt": {
        "category": "concentration_explanation",
        "justification": "Correlation briefing explaining asset dependency relationships to portfolio manager",
    },
    "cross_asset_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Cross-asset briefing explaining inter-market relationships to portfolio manager",
    },
    "divergence_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Divergence briefing explaining market divergence patterns to portfolio manager",
    },
    "early_warning_briefing_txt": {
        "category": "confidence_explanation",
        "justification": "Early warning briefing explaining risk signals and confidence degradation to portfolio manager",
    },
    "flow_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Flow briefing explaining market flow dynamics to portfolio manager",
    },
    "liquidity_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Liquidity briefing explaining market liquidity conditions to portfolio manager",
    },
    "market_breadth_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Market breadth briefing explaining participation breadth to portfolio manager",
    },
    "narrative_dependency_briefing_txt": {
        "category": "dependency_explanation",
        "justification": "Narrative dependency briefing explaining thematic risk dependencies to portfolio manager",
    },
    "portfolio_memory_briefing_txt": {
        "category": "pm_reasoning",
        "justification": "Portfolio memory briefing providing historical context for current portfolio decisions",
    },
    "regime_briefing_txt": {
        "category": "semantic_interpretation",
        "justification": "Regime briefing explaining current market regime classification to portfolio manager",
    },
    "relative_strength_briefing_txt": {
        "category": "action_space_clarity",
        "justification": "Relative strength briefing explaining deployment candidate rankings to portfolio manager",
    },
    "scenario_briefing_txt": {
        "category": "scenario_interpretation",
        "justification": "Scenario briefing explaining stress test results and scenario outcomes to portfolio manager",
    },
    # SIGNAL DATA OUTPUTS (.xlsx)
    "allocation_engine_xlsx": {
        "category": "semantic_interpretation",
        "justification": "Allocation signal data consumed by semantic engine for portfolio structure interpretation",
    },
    "attribution_engine_xlsx": {
        "category": "pm_reasoning",
        "justification": "Attribution signal data enabling performance driver identification in daily report",
    },
    "regime_engine_xlsx": {
        "category": "semantic_interpretation",
        "justification": "Regime signal data consumed by semantic engine for market regime state interpretation",
    },
    "scenario_engine_xlsx": {
        "category": "scenario_interpretation",
        "justification": "Scenario signal data enabling stress test analysis in Scenario Analysis section",
    },
    "risk_engine_xlsx": {
        "category": "confidence_explanation",
        "justification": "Risk signal data enabling confidence assessment and degradation detection in report",
    },
    "correlation_matrix_xlsx": {
        "category": "concentration_explanation",
        "justification": "Correlation matrix data enabling concentration risk detection in report",
    },
    "high_correlation_pairs_xlsx": {
        "category": "concentration_explanation",
        "justification": "High correlation pairs data enabling dependency risk explanation in report",
    },
    "divergence_engine_xlsx": {
        "category": "pm_reasoning",
        "justification": "Divergence signal data enabling market divergence interpretation in Market Regime section",
    },
    "early_warning_engine_xlsx": {
        "category": "confidence_explanation",
        "justification": "Early warning signal data enabling confidence degradation detection in report",
    },
    "flow_engine_xlsx": {
        "category": "pm_reasoning",
        "justification": "Flow signal data enabling market flow interpretation in Market Regime section",
    },
    "liquidity_engine_xlsx": {
        "category": "pm_reasoning",
        "justification": "Liquidity signal data enabling liquidity condition interpretation in Market Regime section",
    },
    "market_breadth_engine_xlsx": {
        "category": "pm_reasoning",
        "justification": "Market breadth signal data enabling participation analysis in Market Regime section",
    },
    "narrative_risk_engine_xlsx": {
        "category": "dependency_explanation",
        "justification": "Narrative risk signal data enabling thematic dependency explanation in report",
    },
    "relative_strength_engine_xlsx": {
        "category": "action_space_clarity",
        "justification": "Relative strength signal data enabling deployment candidate ranking in report",
    },
    "cross_asset_engine_xlsx": {
        "category": "pm_reasoning",
        "justification": "Cross-asset signal data enabling inter-market relationship interpretation in report",
    },
    "divergence_market_data_xlsx": {
        "category": "pm_reasoning",
        "justification": "Divergence market data enabling divergence pattern detection in Market Regime section",
    },
    "liquidity_signals_xlsx": {
        "category": "pm_reasoning",
        "justification": "Liquidity signal data enabling regime liquidity assessment in Market Regime section",
    },
    "macro_output_xlsx": {
        "category": "pm_reasoning",
        "justification": "Macro signal data enabling macroeconomic context interpretation in Executive Summary",
    },
    "narrative_summary_xlsx": {
        "category": "dependency_explanation",
        "justification": "Narrative summary data enabling thematic dependency explanation in report",
    },
    "trigger_dependency_xlsx": {
        "category": "dependency_explanation",
        "justification": "Trigger dependency data enabling causal chain explanation in Concentration section",
    },
    "breadth_category_strength_xlsx": {
        "category": "pm_reasoning",
        "justification": "Category strength data enabling sector breadth analysis in Market Regime section",
    },
    "category_attribution_xlsx": {
        "category": "pm_reasoning",
        "justification": "Category attribution data enabling sector performance explanation in Portfolio Structure",
    },
    "category_relative_strength_xlsx": {
        "category": "action_space_clarity",
        "justification": "Category relative strength data enabling sector deployment ranking in report",
    },
    "cross_asset_data_xlsx": {
        "category": "pm_reasoning",
        "justification": "Cross-asset data enabling inter-market correlation analysis in Market Regime section",
    },
    # PORTFOLIO STATE DATA
    "watchlist_xlsx": {
        "category": "action_space_clarity",
        "justification": "Watchlist data enabling deployment candidate tracking in Watchlist report block",
    },
    "data_json": {
        "category": "traceability",
        "justification": "Portfolio state configuration enabling consistent data access across pipeline components",
    },
    "portfolio_output_xlsx": {
        "category": "pm_reasoning",
        "justification": "Portfolio state output enabling Current Portfolio Reality block in daily report",
    },
    "category_exposure_xlsx": {
        "category": "concentration_explanation",
        "justification": "Category exposure data enabling concentration risk explanation in report",
    },
    "category_flow_xlsx": {
        "category": "pm_reasoning",
        "justification": "Category flow data enabling sector rotation analysis in Portfolio Structure section",
    },
    "allocation_governance_xlsx": {
        "category": "action_space_clarity",
        "justification": "Allocation governance data enabling deployment constraint explanation in report",
    },
    # DATA INPUT
    "market_snapshot_xlsx": {
        "category": "semantic_interpretation",
        "justification": "Daily market data snapshot providing raw input for signal engine interpretation chain",
    },
    # RUNTIME ENTRY POINTS
    "main_py": {
        "category": "traceability",
        "justification": "Main execution entry point enabling pipeline run initiation and audit trail",
    },
    "app_py": {
        "category": "user_understanding",
        "justification": "Dashboard entry point enabling portfolio visualization and user comprehension",
    },
    # HISTORICAL SNAPSHOTS
    "portfolio_history_xlsx": {
        "category": "pm_reasoning",
        "justification": "Historical portfolio data enabling temporal comparison in PM Summary section",
    },
    "briefing_2026_05_23_txt": {
        "category": "traceability",
        "justification": "Archived briefing snapshot enabling historical provenance and delta comparison",
    },
    "macro_2026_05_23_xlsx": {
        "category": "traceability",
        "justification": "Archived macro data snapshot enabling historical replay and forensic analysis",
    },
    "narrative_2026_05_23_xlsx": {
        "category": "traceability",
        "justification": "Archived narrative data snapshot enabling historical replay and forensic analysis",
    },
    "portfolio_2026_05_23_xlsx": {
        "category": "traceability",
        "justification": "Archived portfolio snapshot enabling historical state comparison and replay",
    },
    "portfolio_memory_xlsx": {
        "category": "pm_reasoning",
        "justification": "Consolidated portfolio memory enabling historical context in PM Summary section",
    },
    "regime_history_xlsx": {
        "category": "semantic_interpretation",
        "justification": "Historical regime data enabling regime transition detection and semantic state comparison",
    },
    "report_2026_05_24_txt": {
        "category": "traceability",
        "justification": "Archived report snapshot enabling historical comparison and delta detection",
    },
    # CALIBRATION AND STEERING
    "kiro_calibration_report_md": {
        "category": "confidence_explanation",
        "justification": "Calibration decisions enabling transparent confidence parameter tuning in report pipeline",
    },
    "execution_governance_baseline_md": {
        "category": "traceability",
        "justification": "Commit governance rules enabling audit trail integrity for all pipeline changes",
    },
    # SSOT FRAMEWORK DOCUMENTS (mirror_only)
    "signal_calculation_framework_md": {
        "category": "semantic_interpretation",
        "justification": "Signal calculation methodology enabling deterministic signal production for semantic interpretation",
    },
    "portfolio_health_framework_md": {
        "category": "confidence_explanation",
        "justification": "Portfolio health framework enabling health state detection and confidence assessment in report",
    },
    "market_regime_framework_md": {
        "category": "semantic_interpretation",
        "justification": "Market regime framework enabling regime classification rendered in Market Regime section",
    },
    "correlation_dependency_framework_md": {
        "category": "concentration_explanation",
        "justification": "Correlation framework enabling dependency detection rendered in Concentration section",
    },
    "scoring_methodology_framework_md": {
        "category": "action_space_clarity",
        "justification": "Scoring methodology enabling action prioritization rendered in Action Space section",
    },
    "semantic_signal_registry_md": {
        "category": "semantic_interpretation",
        "justification": "Semantic signal registry defining all semantic states interpreted from raw signals",
    },
    "semantic_reasoning_rules_md": {
        "category": "semantic_interpretation",
        "justification": "Semantic reasoning rules enabling deterministic state interpretation from signal inputs",
    },
    "decision_governance_md": {
        "category": "pm_reasoning",
        "justification": "Decision governance framework enabling structured reasoning in Reasoning Objects",
    },
    "report_reasoning_system_md": {
        "category": "pm_reasoning",
        "justification": "Report reasoning system defining how Reasoning Objects map to report sections",
    },
    "report_section_specification_md": {
        "category": "multilingual_rendering",
        "justification": "Report section specification defining content structure and rendering rules for daily report",
    },
    "simulation_architecture_md": {
        "category": "scenario_interpretation",
        "justification": "Simulation architecture enabling scenario analysis rendered in Scenario Analysis section",
    },
    "dashboard_philosophy_md": {
        "category": "user_understanding",
        "justification": "Dashboard philosophy defining visualization principles for portfolio comprehension",
    },
    "engine_design_principles_md": {
        "category": "traceability",
        "justification": "Engine design principles enabling consistent engine implementation across pipeline layers",
    },
    "portfolio_memory_architecture_md": {
        "category": "pm_reasoning",
        "justification": "Memory architecture enabling historical context integration in PM Summary section",
    },
    "portfolio_state_model_md": {
        "category": "pm_reasoning",
        "justification": "Portfolio state model defining data structures rendered in Current Portfolio Reality block",
    },
    "watchlist_asset_registry_framework_md": {
        "category": "action_space_clarity",
        "justification": "Watchlist framework defining deployment candidate tracking rendered in Watchlist block",
    },
    "data_ingestion_normalization_framework_md": {
        "category": "traceability",
        "justification": "Data ingestion framework enabling consistent data normalization for signal engine inputs",
    },
}


def main():
    with open(REGISTRY_PATH, "r") as f:
        content = f.read()

    data = yaml.safe_load(content)
    artifacts = data.get("artifacts", [])

    updated_count = 0
    for artifact in artifacts:
        aid = artifact.get("artifact_id")
        if aid in REPORT_VALUE_MAP and "report_value" not in artifact:
            artifact["report_value"] = REPORT_VALUE_MAP[aid]
            updated_count += 1

    # Verify 100% coverage
    missing_after = [a["artifact_id"] for a in artifacts if "report_value" not in a]

    print(f"Updated {updated_count} artifacts with report_value metadata")
    print(f"Remaining without report_value: {len(missing_after)}")
    if missing_after:
        print("Still missing:")
        for m in missing_after:
            print(f"  - {m}")
        return 1

    # Write back
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)

    print("Successfully wrote updated artifact_registry.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
