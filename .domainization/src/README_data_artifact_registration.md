# Data Artifact Registration Guide

## Overview

This document describes the data artifacts registered in the Portfolio OS domainization system. Data artifacts include signal outputs, portfolio state files, and historical snapshots.

## Registration Summary

**Total Data Artifacts Registered**: 39

### By Domain
- **SIGNALS**: 24 DATA_OUT files
- **STATE**: 7 files (1 DATA_IN, 2 CONFIG, 4 DATA_OUT)
- **MEMORY**: 8 SNAPSHOT files
- **DATA**: 1 DATA_IN file

### By Type
- **DATA_OUT**: 28 files
- **SNAPSHOT**: 8 files
- **DATA_IN**: 2 files
- **CONFIG**: 2 files

## SIGNALS Domain Data Outputs (24 files)

Signal generation engines produce structured data outputs that are consumed by semantic interpretation and reasoning layers.

### Core Signal Outputs
1. `allocation_engine.xlsx` - Allocation structure signals
2. `attribution_engine.xlsx` - Performance attribution signals
3. `regime_engine.xlsx` - Market regime classification signals
4. `scenario_engine.xlsx` - Scenario analysis signals
5. `risk_engine.xlsx` - Risk assessment signals

### Correlation & Dependency Signals
6. `correlation_matrix.xlsx` - Asset correlation matrix
7. `high_correlation_pairs.xlsx` - High correlation asset pairs
8. `trigger_dependency.xlsx` - Trigger dependency signals
9. `narrative_risk_engine.xlsx` - Narrative risk signals
10. `narrative_summary.xlsx` - Narrative summary signals

### Market Analysis Signals
11. `divergence_engine.xlsx` - Market divergence signals
12. `divergence_market_data.xlsx` - Divergence market data
13. `early_warning_engine.xlsx` - Early warning signals
14. `flow_engine.xlsx` - Market flow signals
15. `liquidity_engine.xlsx` - Liquidity conditions signals
16. `liquidity_signals.xlsx` - Liquidity signals
17. `market_breadth_engine.xlsx` - Market breadth signals
18. `relative_strength_engine.xlsx` - Relative strength signals

### Cross-Asset & Category Signals
19. `cross_asset_engine.xlsx` - Cross-asset relationship signals
20. `cross_asset_data.xlsx` - Cross-asset data signals
21. `breadth_category_strength.xlsx` - Category strength breadth signals
22. `category_attribution.xlsx` - Category attribution signals
23. `category_relative_strength.xlsx` - Category relative strength signals

### Macro Signals
24. `macro_output.xlsx` - Macro signals

## STATE Domain Files (7 files)

Portfolio state management files track current portfolio composition and configuration.

### Input Files
1. `watchlist.xlsx` (DATA_IN) - Portfolio watchlist with tracked assets

### Configuration Files
2. `data.json` (CONFIG) - Portfolio state configuration

### Output Files
3. `portfolio_output.xlsx` (DATA_OUT) - Portfolio state output data
4. `category_exposure.xlsx` (DATA_OUT) - Portfolio category exposure
5. `category_flow.xlsx` (DATA_OUT) - Portfolio category flow
6. `allocation_governance.xlsx` (DATA_OUT) - Portfolio allocation governance

## MEMORY Domain Snapshots (8 files)

Historical snapshots preserve portfolio state and analysis over time.

### Continuous History Files
1. `data/portfolio_history.xlsx` (SNAPSHOT, captured) - Historical portfolio positions and performance
2. `history/portfolio_memory.xlsx` (SNAPSHOT, captured) - Consolidated portfolio memory
3. `history/regime_history.xlsx` (SNAPSHOT, captured) - Historical market regime classifications

### Archived Daily Snapshots (2026-05-23)
4. `history/briefing_2026-05-23.txt` (SNAPSHOT, archived) - Archived briefing
5. `history/macro_2026-05-23.xlsx` (SNAPSHOT, archived) - Archived macro data
6. `history/narrative_2026-05-23.xlsx` (SNAPSHOT, archived) - Archived narrative data
7. `history/portfolio_2026-05-23.xlsx` (SNAPSHOT, archived) - Archived portfolio

### Archived Daily Snapshots (2026-05-24)
8. `history/report_2026-05-24.txt` (SNAPSHOT, archived) - Archived report

## DATA Domain Input Files (1 file)

External market data inputs for signal generation.

1. `data/market_snapshot_2026-05-23.xlsx` (DATA_IN) - Daily market data snapshot

## Metadata Schema

All data artifacts are registered with the following metadata:

### Required Fields
- `artifact_id`: Unique identifier (e.g., `allocation_engine_xlsx`)
- `file_path`: Relative path from repo root
- `primary_domain`: Domain ID (SIGNALS, STATE, MEMORY, DATA)
- `artifact_type`: Type ID (DATA_OUT, DATA_IN, SNAPSHOT, CONFIG)
- `lifecycle_status`: Current state (current, active, captured, archived)
- `created_date`: Creation date (YYYY-MM-DD)
- `last_modified`: Last modification date (YYYY-MM-DD)
- `owner_role`: Responsibility description
- `ssot_relationship`: Always "none" for data artifacts
- `allowed_writers`: Domain IDs with write permission
- `allowed_readers`: Domain IDs with read permission (typically "ALL")

### Optional Fields
- `dependencies`: Artifact IDs this depends on (e.g., generating engine)
- `description`: Human-readable description
- `tags`: Categorization tags

## Lifecycle States

### DATA_OUT Files
- **current**: Latest version of generated data
- **archived**: Superseded by newer data

### DATA_IN Files
- **active**: Currently used input data
- **stale**: Outdated input data
- **archived**: Moved to historical storage

### SNAPSHOT Files
- **captured**: Ongoing historical record
- **archived**: Point-in-time snapshot

### CONFIG Files
- **active**: Currently used configuration
- **deprecated**: Superseded configuration

## Dependencies

### Signal Outputs
Signal output files depend on:
- Generating engine (e.g., `allocation_engine_py`)
- SSOT framework documents (e.g., `signal_calculation_framework_md`)

### State Files
State files depend on:
- SSOT framework documents (e.g., `portfolio_state_model_md`)
- Governance documents (e.g., `decision_governance_md`)

### Memory Snapshots
Memory snapshots depend on:
- `portfolio_memory_architecture_md`
- Relevant framework documents

## Validation

All registered data artifacts have been validated:
- YAML schema is valid
- All required metadata fields are present
- Domain assignments are valid
- Artifact types match lifecycle state machines
- Dependencies reference valid artifact IDs

## Usage

### Query by Domain
```python
from artifact_registry import ArtifactRegistry

registry = ArtifactRegistry()
signals_data = registry.list_artifacts_by_domain("SIGNALS")
```

### Query by Type
```python
data_outputs = registry.list_artifacts_by_type("DATA_OUT")
```

### Query by Lifecycle
```python
current_data = registry.list_artifacts_by_lifecycle("current")
```

## Maintenance

### Adding New Data Files
1. Generate or create the data file
2. Add registry entry to `.domainization/artifact_registry.yaml`
3. Include all required metadata fields
4. Reference generating engine in dependencies
5. Validate registry with `python -c "import yaml; yaml.safe_load(open('.domainization/artifact_registry.yaml'))"`

### Archiving Old Data
1. Update `lifecycle_status` to "archived"
2. Update `last_modified` date
3. Move file to `history/` directory if appropriate

### Updating Data Files
1. Modify the data file
2. Update `last_modified` date in registry
3. Ensure lifecycle_status is still appropriate

## References

- **Artifact Registry**: `.domainization/artifact_registry.yaml`
- **Domain Registry**: `.domainization/domain_registry.yaml`
- **Lifecycle State Machines**: `.domainization/lifecycle_state_machine.yaml`
- **SSOT Documents**: `docs/*.md`
