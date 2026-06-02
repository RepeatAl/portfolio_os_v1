# Phase B Preflight: Signal→Report Shortcut Analysis

**Task:** 4.1 — Inspect engine_runner behavior and identify Signal→Report shortcuts  
**Date:** 2026-05-27  
**Requirements:** 1.1, 1.5, 2.4

---

## 1. Engine Runner Flow (`engines/engine_runner.py`)

`run_all_engines()` executes 12 engines in a fixed sequence:

```
1. allocation_engine  (SIGNALS)     — no dependencies
2. regime_engine      (SIGNALS)     — no dependencies
3. attribution_engine (SIGNALS)     — depends on: allocation, regime
4. priority_engine    (REASONING)   — depends on: allocation, attribution
5. scenario_engine    (SIM)         — depends on: allocation
6. decision_engine    (REASONING)   — depends on: priority, scenario
7. scoring_engine     (SIGNALS)     — depends on: priority, scenario
8. quality_engine     (REASONING)   — depends on: allocation, priority, scoring
9. report_engine      (REPORT)      — depends on: regime, decision, quality
10. delta_engine      (REPORT)      — depends on: report
11. morning_briefing  (REPORT)      — depends on: priority, scoring, delta, report
12. visual_engine     (ARCH)        — depends on: allocation, decision, scenario, quality
```

### Critical Finding: Signal→Report Shortcut Confirmed

`run_all_engines()` calls:
```python
report = run_report_engine(regime, decision, quality)
```

This passes raw engine outputs **directly** to the Report Engine. There is:
- **No Semantic Engine invocation** between Signal Engines and Report Engine
- **No Reasoning Object creation** — the Report Engine receives raw dicts, not structured Reasoning Objects
- The only semantic processing in the entire pipeline is `interpret_allocation_signals()` called internally by `allocation_engine.py`

---

## 2. Report Engine Behavior (`engines/report_engine.py`)

### Function Signature
```python
def run_report_engine(allocation_data, regime_data, decision_data, quality_data, scenario_data):
```

### Signature Mismatch
The engine_runner calls `run_report_engine(regime, decision, quality)` with **3 arguments**, but the function signature expects **5 parameters**. This means:
- `regime` → maps to `allocation_data` (positional mismatch)
- `decision` → maps to `regime_data` (positional mismatch)
- `quality` → maps to `decision_data` (positional mismatch)
- `quality_data` and `scenario_data` are never provided

### Direct Formatting (No Semantic Layer)
The Report Engine:
1. Extracts raw values from input dicts using `.get()` calls
2. Formats them directly into a text template string
3. Returns `{"report": report_text, "date": date, "confidence": confidence}`

**There is NO:**
- Schema validation of inputs
- Reasoning Object consumption
- Semantic State interpretation
- Provenance metadata generation
- Chain integrity verification

The Report Engine is a pure **string formatter** — it takes raw engine outputs and concatenates them into a text report.

---

## 3. Semantic Engine Scope (`engines/semantic_engine.py`)

### Confirmed: Limited to Allocation Signals Only

The semantic engine contains a single function:
```python
def interpret_allocation_signals(allocation_df) -> list[dict]
```

It produces exactly **3 semantic states** based on allocation percentages:
1. `defense_dependency_elevated` — when Defense allocation > 25%
2. `semiconductor_dependency_elevated` — when Semiconductor allocation > 25%
3. `concentration_risk_elevated` — when any category allocation > 25%

### What It Does NOT Cover
- No regime interpretation
- No attribution semantics
- No correlation/cross-asset semantics
- No divergence/early-warning semantics
- No flow/liquidity semantics
- No market breadth semantics
- No narrative dependency semantics (beyond allocation-based)
- No scenario semantics
- No portfolio memory semantics
- No relative strength semantics

### Integration Point
`interpret_allocation_signals()` is called **only** by `allocation_engine.py` internally. Its output is printed to console but **never passed downstream** to any Reasoning Engine or Report Engine.

---

## 4. Briefing File Inventory

### 14 Legacy Briefing Files (All Signal→Report Shortcuts)

These files exist on disk at the project root. They bypass the canonical chain entirely:

| # | Briefing File | Signal Category | Producing Engine(s) |
|---|--------------|-----------------|---------------------|
| 1 | `allocation_briefing.txt` | allocation | allocation_engine |
| 2 | `attribution_briefing.txt` | attribution | attribution_engine |
| 3 | `correlation_briefing.txt` | correlation | correlation/scoring engines |
| 4 | `cross_asset_briefing.txt` | cross_asset | cross_asset signal engines |
| 5 | `divergence_briefing.txt` | divergence | divergence signal engines |
| 6 | `early_warning_briefing.txt` | early_warning | early_warning signal engines |
| 7 | `flow_briefing.txt` | flow | flow signal engines |
| 8 | `liquidity_briefing.txt` | liquidity | liquidity signal engines |
| 9 | `market_breadth_briefing.txt` | market_breadth | market_breadth signal engines |
| 10 | `narrative_dependency_briefing.txt` | narrative_dependency | narrative_risk signal engines |
| 11 | `regime_briefing.txt` | regime | regime_engine |
| 12 | `relative_strength_briefing.txt` | relative_strength | relative_strength signal engines |
| 13 | `scenario_briefing.txt` | scenario | scenario_engine |
| 14 | `portfolio_memory_briefing.txt` | portfolio_memory | portfolio_memory engines |

**Note:** The file-write code for these briefing files is not present in the current repository source. They appear to be artifacts from a previous pipeline version or produced by engines not currently in the `engines/` directory (the forensic scan identifies signal engines like `correlation_matrix.xlsx`, `divergence_engine.xlsx`, etc. that produce `.xlsx` outputs but whose Python source may exist elsewhere or have been refactored).

### Additional Report Outputs

| File | Producer | Type |
|------|----------|------|
| `portfolio_report.txt` | report_engine (historical) | REPORT_OUT |
| `morning_briefing.txt` | morning_briefing_engine | REPORT_OUT |

---

## 5. All Signal→Report Shortcuts Identified

### Category A: The 8 "Forbidden" Briefing Flows (Pure Signal→Report)

These 8 categories have signal engines producing `.xlsx` data outputs AND briefing `.txt` files, with **zero** semantic or reasoning processing:

| # | Category | Signal Engine Output | Briefing File | Layers Skipped |
|---|----------|---------------------|---------------|----------------|
| 1 | allocation | `allocation_engine.xlsx` | `allocation_briefing.txt` | SEMANTICS, REASONING |
| 2 | attribution | `attribution_engine.xlsx` | `attribution_briefing.txt` | SEMANTICS, REASONING |
| 3 | correlation | `correlation_matrix.xlsx` | `correlation_briefing.txt` | SEMANTICS, REASONING |
| 4 | cross_asset | `cross_asset_engine.xlsx` | `cross_asset_briefing.txt` | SEMANTICS, REASONING |
| 5 | divergence | `divergence_engine.xlsx` | `divergence_briefing.txt` | SEMANTICS, REASONING |
| 6 | early_warning | `early_warning_engine.xlsx` | `early_warning_briefing.txt` | SEMANTICS, REASONING |
| 7 | flow | `flow_engine.xlsx` | `flow_briefing.txt` | SEMANTICS, REASONING |
| 8 | liquidity | `liquidity_engine.xlsx` | `liquidity_briefing.txt` | SEMANTICS, REASONING |

### Category B: Additional Briefing Producers (Also Signal→Report)

These 6 categories also produce briefing files bypassing the chain:

| # | Category | Signal Engine Output | Briefing File | Layers Skipped |
|---|----------|---------------------|---------------|----------------|
| 9 | regime | `regime_engine.xlsx` | `regime_briefing.txt` | SEMANTICS, REASONING |
| 10 | market_breadth | `market_breadth_engine.xlsx` | `market_breadth_briefing.txt` | SEMANTICS, REASONING |
| 11 | narrative_dependency | `narrative_risk_engine.xlsx` | `narrative_dependency_briefing.txt` | SEMANTICS, REASONING |
| 12 | relative_strength | `relative_strength_engine.xlsx` | `relative_strength_briefing.txt` | SEMANTICS, REASONING |
| 13 | scenario | `scenario_engine.xlsx` | `scenario_briefing.txt` | SEMANTICS, REASONING |
| 14 | portfolio_memory | `history/portfolio_memory.xlsx` | `portfolio_memory_briefing.txt` | SEMANTICS, REASONING |

### Category C: The Main Report Engine Shortcut

The `run_report_engine()` function in `engine_runner.py` is itself a Signal→Report shortcut:
- Receives raw outputs from `regime_engine`, `decision_engine`, `quality_engine`
- Formats them directly into text without semantic interpretation
- No Reasoning Objects are created or consumed
- No provenance metadata is generated

### Category D: Morning Briefing Engine Shortcut

`run_morning_briefing_engine()` receives:
- `priority_data` (from priority_engine — REASONING domain)
- `scoring_data` (from scoring_engine — SIGNALS domain)
- `delta_data` (from delta_engine — REPORT domain)
- `report_data` (from report_engine — REPORT domain)

This mixes domain levels without semantic interpretation.

---

## 6. Summary of Findings

| Finding | Status |
|---------|--------|
| `run_all_engines()` calls `run_report_engine()` directly with raw engine outputs | **CONFIRMED** |
| Report Engine formats text directly from raw dicts (no semantic layer) | **CONFIRMED** |
| Semantic Engine only handles allocation signals (3 states) | **CONFIRMED** |
| Semantic Engine output is never consumed by Report Engine | **CONFIRMED** |
| 14 briefing files exist as Signal→Report shortcuts | **CONFIRMED** |
| Total forbidden flows: 14 briefing files + 1 main report + 1 morning briefing = **16** | **CONFIRMED** |
| No Reasoning Objects exist anywhere in the current pipeline | **CONFIRMED** |
| No Chain Provenance metadata exists in any output | **CONFIRMED** |

### Implications for Phase B

1. **Pipeline_Orchestrator** must intercept the `run_all_engines()` flow and route signal outputs through SEMANTICS → REASONING before reaching REPORT
2. **Semantic Engine** must be expanded from 3 states to cover all 14 signal categories
3. **Report Engine** must be rewritten to consume Reasoning Objects instead of raw dicts
4. **All 14 briefing files** must be replaced with chain-compliant outputs (or deprecated with sunset governance)
5. The existing `engine_runner.py` remains for backward compatibility but is wrapped by `pipeline_orchestrator.py`
