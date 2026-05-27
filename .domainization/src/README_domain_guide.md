# Domain Guide

## Overview

Portfolio OS uses 12 canonical domains to organize all artifacts by responsibility. Each domain has explicit ownership boundaries, defining what it can and cannot own. The core reasoning chain (SIGNALS → SEMANTICS → REASONING → REPORT) establishes authority over how meaning flows from raw data to human-readable output.

This guide documents all 12 domains, their responsibilities, ownership rules, and the authority chain that governs runtime flows.

## Authority Chain

The authority chain defines how meaning is created in Portfolio OS. It is not just a data flow — it represents who has the authority to create meaning at each stage.

```
SIGNALS (Level 1) → SEMANTICS (Level 2) → REASONING (Level 3) → REPORT (Level 4)
```

| Level | Domain     | Creates                  | Reads From        | Cannot Create              |
|-------|------------|--------------------------|-------------------|----------------------------|
| 1     | SIGNALS    | Structured signals       | Raw market data   | Semantic interpretations   |
| 2     | SEMANTICS  | Semantic states          | Signal outputs    | Raw signals, reasoning     |
| 3     | REASONING  | Reasoning conclusions    | Semantic states   | Signals, semantic states   |
| 4     | REPORT     | Human-readable text      | Reasoning objects | Business logic, signals    |

### Authority Rules

- Lower authority level = higher authority in the reasoning chain
- Core domains have architectural priority over surface domains
- If a surface domain (USER, DEPLOY) conflicts with a core reasoning domain, the core domain takes precedence
- No domain may skip levels in the chain (e.g., SIGNALS cannot write directly to REPORT)

### Forbidden Flows

| Flow                          | Why Forbidden                                              |
|-------------------------------|-------------------------------------------------------------|
| Signal → Report               | Skips semantic interpretation and reasoning                 |
| Signal → Reasoning            | Skips semantic interpretation                               |
| Dashboard → Semantic Truth    | Surface domain cannot create meaning in core chain          |
| Dashboard → Signal Generation | Surface domain cannot generate signals                      |

## Core Reasoning Domains

### 1. SIGNALS

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `SIGNALS`                                                             |
| **Name**              | Signal Generation                                                     |
| **Priority**          | Core                                                                  |
| **Authority Level**   | 1 (highest)                                                           |
| **Responsibility**    | Raw signal calculation, market data processing, quantitative metrics  |
| **Can Own**           | SSOT, ENGINE, DATA_OUT, CONFIG                                        |
| **Cannot Own**        | REPORT_OUT, DASHBOARD                                                 |

**What SIGNALS does:**
- Calculates raw quantitative signals from market data
- Produces structured signal outputs (allocation scores, regime indicators, attribution metrics)
- Owns signal calculation frameworks and methodologies

**What SIGNALS cannot do:**
- Interpret what signals mean (that's SEMANTICS)
- Draw conclusions from signals (that's REASONING)
- Write human-readable narratives (that's REPORT)
- Present data to users (that's USER)

**Example artifacts:**
- `engines/allocation_engine.py` — ENGINE, calculates allocation signals
- `engines/regime_engine.py` — ENGINE, detects market regime signals
- `docs/semantic_signal_registry.md` — SSOT, defines signal specifications
- `allocation_engine.xlsx` — DATA_OUT, structured signal output


---

### 2. SEMANTICS

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `SEMANTICS`                                                           |
| **Name**              | Semantic Interpretation                                               |
| **Priority**          | Core                                                                  |
| **Authority Level**   | 2                                                                     |
| **Responsibility**    | Semantic state creation, signal interpretation, meaning extraction     |
| **Can Own**           | SSOT, ENGINE, DATA_OUT, CONFIG                                        |
| **Cannot Own**        | REPORT_OUT, DASHBOARD                                                 |

**What SEMANTICS does:**
- Interprets structured signals into semantic states
- Extracts meaning from quantitative data
- Creates semantic objects that represent "what the signals mean"

**What SEMANTICS cannot do:**
- Generate raw signals (that's SIGNALS)
- Draw portfolio conclusions (that's REASONING)
- Write human-readable text (that's REPORT)
- Present data to users (that's USER)

**Example artifacts:**
- `engines/semantic_engine.py` — ENGINE, interprets signals into semantic states
- `docs/semantic_reasoning_rules.md` — SSOT, defines semantic interpretation rules

---

### 3. REASONING

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `REASONING`                                                           |
| **Name**              | Reasoning Logic                                                       |
| **Priority**          | Core                                                                  |
| **Authority Level**   | 3                                                                     |
| **Responsibility**    | Decision logic, reasoning objects, portfolio conclusions               |
| **Can Own**           | SSOT, ENGINE, DATA_OUT, CONFIG                                        |
| **Cannot Own**        | REPORT_OUT, DASHBOARD                                                 |

**What REASONING does:**
- Creates reasoning objects from semantic states
- Draws portfolio conclusions and strategic recommendations
- Implements decision logic and priority scoring

**What REASONING cannot do:**
- Generate raw signals (that's SIGNALS)
- Create semantic interpretations (that's SEMANTICS)
- Write human-readable narratives (that's REPORT)
- Present data to users (that's USER)

**Example artifacts:**
- `engines/decision_engine.py` — ENGINE, creates portfolio decisions
- `engines/quality_engine.py` — ENGINE, evaluates portfolio quality
- `engines/priority_engine.py` — ENGINE, scores action priorities

---

### 4. REPORT

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `REPORT`                                                              |
| **Name**              | Report Generation                                                     |
| **Priority**          | Core                                                                  |
| **Authority Level**   | 4 (lowest in chain)                                                   |
| **Responsibility**    | Human-readable report text, narrative generation, multilingual rendering |
| **Can Own**           | SSOT, ENGINE, REPORT_OUT, CONFIG                                      |
| **Cannot Own**        | DATA_OUT, DASHBOARD                                                   |

**What REPORT does:**
- Renders reasoning objects into human-readable text
- Generates PM-facing narratives and briefings
- Handles multilingual rendering
- Owns report pipeline architecture

**What REPORT cannot do:**
- Generate raw signals (that's SIGNALS)
- Create semantic interpretations (that's SEMANTICS)
- Implement business logic or reasoning (that's REASONING)
- Generate structured data outputs (that's SIGNALS/SEMANTICS/REASONING)

**Example artifacts:**
- `engines/report_engine.py` — ENGINE, generates portfolio reports
- `engines/morning_briefing_engine.py` — ENGINE, generates morning briefings
- `portfolio_report.txt` — REPORT_OUT, final human-readable report
- `docs/report_reasoning_system.md` — SSOT, report generation rules


## Surface Domains

Surface domains support the core reasoning chain. They do not participate in the authority chain and have no authority level. When a surface domain conflicts with a core domain, the core domain takes precedence.

---

### 5. GOV (Governance)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `GOV`                                                                 |
| **Name**              | Governance                                                            |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Decision frameworks, confidence models, action space definitions       |
| **Can Own**           | SSOT, CONFIG, STEERING                                                |
| **Cannot Own**        | ENGINE, REPORT_OUT, DATA_OUT                                          |

**What GOV does:**
- Defines governance rules and decision frameworks
- Owns confidence models and action space definitions
- Manages steering documents that guide system behavior

**What GOV cannot do:**
- Implement engines or processing logic
- Generate reports or data outputs
- Override core reasoning chain authority

**Example artifacts:**
- `docs/decision_governance.md` — SSOT, governance decision framework
- `docs/confidence_model.md` — SSOT, confidence scoring model
- `docs/action_space_framework.md` — SSOT, action space definitions

---

### 6. ARCH (Architecture)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `ARCH`                                                                |
| **Name**              | Architecture                                                          |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | System design, component architecture, integration patterns            |
| **Can Own**           | SSOT, ENGINE, CONFIG, CALIBRATION                                     |
| **Cannot Own**        | REPORT_OUT, DATA_OUT                                                  |

**What ARCH does:**
- Defines system architecture and design principles
- Owns infrastructure engines (engine registry, engine runner)
- Manages calibration artifacts and integration patterns

**What ARCH cannot do:**
- Generate reports or data outputs
- Override core reasoning chain decisions
- Own domain-specific business logic engines

**Example artifacts:**
- `docs/system_architecture.md` — SSOT, system architecture specification
- `docs/engine_design_principles.md` — SSOT, engine design guidelines
- `engines/engine_registry.py` — ENGINE, infrastructure engine registry
- `engines/engine_runner.py` — ENGINE, engine execution orchestrator
- `docs/kiro_calibration_report.md` — CALIBRATION, system calibration data

---

### 7. STATE (Portfolio State)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `STATE`                                                               |
| **Name**              | Portfolio State                                                       |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Portfolio holdings, watchlist management, asset registry, current state |
| **Can Own**           | SSOT, DATA_IN, DATA_OUT, SNAPSHOT, CONFIG                             |
| **Cannot Own**        | ENGINE, REPORT_OUT                                                    |

**What STATE does:**
- Tracks current portfolio holdings and positions
- Manages watchlist and asset registry
- Stores current state snapshots

**What STATE cannot do:**
- Implement processing engines
- Generate reports
- Reason about portfolio decisions (that's REASONING)

**Example artifacts:**
- `docs/portfolio_state_model.md` — SSOT, portfolio state specification
- `docs/watchlist_asset_registry_framework.md` — SSOT, watchlist framework
- `watchlist.xlsx` — DATA_IN, current watchlist data
- `data.json` — DATA_OUT, portfolio state output


---

### 8. DATA (Data Management)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `DATA`                                                                |
| **Name**              | Data Management                                                       |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Data ingestion, normalization, trusted sources, data quality, ETL      |
| **Can Own**           | SSOT, ENGINE, DATA_IN, DATA_OUT, CONFIG                               |
| **Cannot Own**        | REPORT_OUT, DASHBOARD                                                 |

**What DATA does:**
- Ingests and normalizes external data
- Defines trusted signal sources
- Manages data quality and ETL processes
- Normalizes data only — does not interpret or reason

**What DATA cannot do:**
- Reason about data (that's REASONING)
- Interpret data semantically (that's SEMANTICS)
- Generate reports or dashboards
- Create signals from data (that's SIGNALS)

**Example artifacts:**
- `docs/data_ingestion_normalization_framework.md` — SSOT, data ingestion rules
- `docs/trusted_signal_sources.md` — SSOT, trusted data source registry
- `data/market_snapshot_2026-05-23.xlsx` — DATA_IN, ingested market data

---

### 9. USER (User Interface)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `USER`                                                                |
| **Name**              | User Interface                                                        |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Dashboard, visualization, user interaction, frontend presentation      |
| **Can Own**           | SSOT, DASHBOARD, CONFIG                                               |
| **Cannot Own**        | ENGINE, DATA_OUT, REPORT_OUT                                          |

**What USER does:**
- Presents data and reports to users via dashboards
- Manages visualization and user interaction
- Owns frontend presentation logic

**What USER cannot do:**
- Implement processing engines
- Generate data outputs
- Generate reports (that's REPORT)
- Create semantic truth (that's SEMANTICS)
- Generate signals (that's SIGNALS)

**Example artifacts:**
- `docs/dashboard_philosophy.md` — SSOT, dashboard design principles
- `app.py` — DASHBOARD, Streamlit dashboard application
- `engines/visual_engine.py` — Note: owned by USER for visualization

---

### 10. DEPLOY (Deployment)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `DEPLOY`                                                              |
| **Name**              | Deployment                                                            |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Runtime orchestration, deployment scripts, infrastructure as code      |
| **Can Own**           | RUNTIME, CONFIG                                                       |
| **Cannot Own**        | SSOT, ENGINE, REPORT_OUT, DATA_OUT                                    |

**What DEPLOY does:**
- Manages runtime entry points and execution orchestration
- Owns deployment scripts and infrastructure configuration
- Handles Google Cloud Platform deployment (Google-only constraint)

**What DEPLOY cannot do:**
- Own specification documents (SSOT)
- Implement business logic engines
- Generate reports or data outputs
- Define domain boundaries or governance rules

**Example artifacts:**
- `main.py` — RUNTIME, main execution entry point

---

### 11. MEMORY (Portfolio Memory)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `MEMORY`                                                              |
| **Name**              | Portfolio Memory                                                      |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Historical snapshots, portfolio memory, time-series archival           |
| **Can Own**           | SSOT, ENGINE, SNAPSHOT, DATA_OUT, CONFIG                              |
| **Cannot Own**        | REPORT_OUT, DASHBOARD                                                 |

**What MEMORY does:**
- Archives historical portfolio snapshots
- Manages time-series data for historical analysis
- Provides portfolio memory for trend detection

**What MEMORY cannot do:**
- Generate reports or dashboards
- Present data to users
- Make real-time decisions (that's REASONING)

**Example artifacts:**
- `docs/portfolio_memory_architecture.md` — SSOT, memory system design
- `history/portfolio_history_*.xlsx` — SNAPSHOT, archived portfolio states
- `data/portfolio_history.xlsx` — SNAPSHOT, historical portfolio data

---

### 12. SIM (Simulation)

| Property              | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Domain ID**         | `SIM`                                                                 |
| **Name**              | Simulation                                                            |
| **Priority**          | Surface                                                               |
| **Authority Level**   | None                                                                  |
| **Responsibility**    | Scenario modeling, what-if analysis, portfolio simulation, stress testing |
| **Can Own**           | SSOT, ENGINE, DATA_OUT, CONFIG                                        |
| **Cannot Own**        | REPORT_OUT, DASHBOARD                                                 |

**What SIM does:**
- Runs scenario simulations and what-if analyses
- Performs stress testing on portfolio positions
- Models hypothetical market conditions

**What SIM cannot do:**
- Generate reports or dashboards
- Present results to users directly (results flow through REASONING → REPORT)
- Override real portfolio state (that's STATE)

**Example artifacts:**
- `docs/simulation_architecture.md` — SSOT, simulation system design
- `engines/scenario_engine.py` — ENGINE, scenario simulation engine


## Domain Priority and Conflict Resolution

### Core vs Surface Priority

When a conflict arises between a core reasoning domain and a surface domain, the core domain always wins:

```
Core Domain Priority (by authority level):
  1. SIGNALS    — highest authority, creates raw structured signals
  2. SEMANTICS  — interprets signals into meaning
  3. REASONING  — draws conclusions from meaning
  4. REPORT     — renders conclusions for humans

Surface Domains (no authority level, support core chain):
  GOV, ARCH, STATE, DATA, USER, DEPLOY, MEMORY, SIM
```

### Conflict Examples

| Conflict                                    | Resolution                                      |
|---------------------------------------------|--------------------------------------------------|
| USER wants to generate signals              | Denied — SIGNALS has authority over signal creation |
| DEPLOY wants to own an ENGINE               | Denied — DEPLOY can only own RUNTIME and CONFIG  |
| DATA wants to interpret signal meaning      | Denied — SEMANTICS has authority over interpretation |
| GOV wants to own a report output            | Denied — REPORT has authority over REPORT_OUT    |

## Usage

### Programmatic Domain Validation

```python
from domain_registry import DomainRegistry

# Load registry
registry = DomainRegistry()
registry.load()

# Check if a domain can own an artifact type
is_valid, error = registry.validate_domain_assignment("ENGINE", "DEPLOY")
# is_valid = False
# error = "Domain 'DEPLOY' cannot own artifact type 'ENGINE'. Valid domains: ..."

# Get the core reasoning chain in order
chain = registry.get_core_reasoning_chain()
for domain in chain:
    print(f"Level {domain.authority_level}: {domain.domain_id} - {domain.name}")
# Level 1: SIGNALS - Signal Generation
# Level 2: SEMANTICS - Semantic Interpretation
# Level 3: REASONING - Reasoning Logic
# Level 4: REPORT - Report Generation

# List all surface domains
surface = registry.list_surface_domains()
for domain in surface:
    print(f"{domain.domain_id}: {domain.responsibility_scope}")
```

### Checking Domain Ownership

```python
from domain_registry import DomainRegistry

registry = DomainRegistry()
registry.load()

# Get a domain and check what it can own
signals = registry.get_domain("SIGNALS")
print(signals.can_own_type("ENGINE"))      # True
print(signals.can_own_type("REPORT_OUT"))  # False
print(signals.is_core_domain())            # True
print(signals.get_authority_level())       # 1

# Get valid domains for an artifact type
valid = registry.get_valid_domains_for_type("REPORT_OUT")
print(valid)  # ['REPORT']
```

### CLI Domain Inspection

```bash
# List all domains
python -m cli_main list --domains

# Validate a domain assignment
python -m cli_main validate --artifact-type ENGINE --domain DEPLOY
# Warning: Domain 'DEPLOY' cannot own artifact type 'ENGINE'

# Show health report with domain coverage
python -m cli_main health
```

## Quick Reference Table

| Domain     | Priority | Level | Can Own                          | Cannot Own                    |
|------------|----------|-------|----------------------------------|-------------------------------|
| SIGNALS    | Core     | 1     | SSOT, ENGINE, DATA_OUT, CONFIG   | REPORT_OUT, DASHBOARD         |
| SEMANTICS  | Core     | 2     | SSOT, ENGINE, DATA_OUT, CONFIG   | REPORT_OUT, DASHBOARD         |
| REASONING  | Core     | 3     | SSOT, ENGINE, DATA_OUT, CONFIG   | REPORT_OUT, DASHBOARD         |
| REPORT     | Core     | 4     | SSOT, ENGINE, REPORT_OUT, CONFIG | DATA_OUT, DASHBOARD           |
| GOV        | Surface  | —     | SSOT, CONFIG, STEERING           | ENGINE, REPORT_OUT, DATA_OUT  |
| ARCH       | Surface  | —     | SSOT, ENGINE, CONFIG, CALIBRATION| REPORT_OUT, DATA_OUT          |
| STATE      | Surface  | —     | SSOT, DATA_IN, DATA_OUT, SNAPSHOT, CONFIG | ENGINE, REPORT_OUT |
| DATA       | Surface  | —     | SSOT, ENGINE, DATA_IN, DATA_OUT, CONFIG | REPORT_OUT, DASHBOARD |
| USER       | Surface  | —     | SSOT, DASHBOARD, CONFIG          | ENGINE, DATA_OUT, REPORT_OUT  |
| DEPLOY     | Surface  | —     | RUNTIME, CONFIG                  | SSOT, ENGINE, REPORT_OUT, DATA_OUT |
| MEMORY     | Surface  | —     | SSOT, ENGINE, SNAPSHOT, DATA_OUT, CONFIG | REPORT_OUT, DASHBOARD |
| SIM        | Surface  | —     | SSOT, ENGINE, DATA_OUT, CONFIG   | REPORT_OUT, DASHBOARD         |

## Testing

### Running Domain Validation Tests

```bash
# Run domain schema tests
python -m pytest test_domain_schema.py -v

# Run domain registry operation tests
python -m pytest test_domain_registry.py -v

# Run boundary awareness validator tests
python -m pytest test_boundary_awareness_validator.py -v
```

## Requirements Satisfied

This guide satisfies the following requirements:

- ✅ **Requirement 2.1**: Domain registry defines exactly 12 canonical domains
- ✅ **Requirement 2.2**: Each domain includes domain_id, name, responsibility_scope, and allowed_artifact_types
- ✅ **Requirement 2.5**: Each domain specifies what it can own and what it cannot own
- ✅ **Requirement 2.8**: Core reasoning domains have architectural priority over surface domains
- ✅ **Requirement 2.9**: Primary reasoning chain is SIGNALS → SEMANTICS → REASONING → REPORT
- ✅ **Requirement 14.8**: Runtime flows represent authority chains, not just data flows
- ✅ **Requirement 14.9**: Meaning follows the authority chain: raw signals → semantic interpretation → reasoning conclusions → report language

## Related Files

- `.domainization/domain_registry.yaml` — Domain registry data (source of truth)
- `.domainization/src/domain_schema.py` — Domain definition data model
- `.domainization/src/domain_registry.py` — Domain registry operations
- `.domainization/src/boundary_awareness_validator.py` — Boundary enforcement validator
- `.domainization/src/test_domain_schema.py` — Domain schema unit tests
- `.domainization/src/test_domain_registry.py` — Domain registry operation tests
