---
artifact_id: portfolio_os_domainization_steering_md
primary_domain: GOV
secondary_domains: [ARCH]
artifact_type: STEERING
lifecycle_status: canonical
created_date: 2026-05-24
last_modified: 2026-05-25
owner_role: Establishes canonical domain ownership and governance rules for all artifacts
ssot_relationship: canonical
topic: domainization_steering
allowed_writers: [GOV, ARCH]
allowed_readers: [ALL]
dependencies: [decision_governance_md, system_architecture_md, domainization_architecture_md]
---

# PORTFOLIO OS — DOMAINIZATION STEERING
Version: v1  
Status: Canonical Governance SSOT  
Date: 2026-05-24

---

# PURPOSE

This document establishes canonical domain ownership for all Portfolio OS artifacts.

Every artifact must have clear domain ownership.
Every domain must have clear responsibility boundaries.
Every future feature must add measurable report value.

No artifact may remain ownerless.
No domain may overlap responsibility.
No feature may bypass domain governance.

---

# CORE DOMAINIZATION PRINCIPLE

Portfolio OS artifacts are organized by responsibility domain, not file type or location.

Every artifact must specify:
1. primary_domain
2. optional secondary_domains  
3. artifact_type
4. ownership_role
5. allowed_to_write
6. allowed_to_read
7. SSOT relationship
8. lifecycle_status

---

# DOMAIN MODEL

Portfolio OS operates under 10 canonical domains.

---

## 1. GOVERNANCE DOMAIN

**Responsibility:**
System governance, decision authority, and compliance rules.

**Owns:**
- Decision governance frameworks
- Confidence model specifications
- Action-space generation rules
- No-command enforcement
- Signal authority hierarchy
- Human-control principles
- Risk and compliance logic
- Domain boundary enforcement

**Cannot Own:**
- Implementation engines
- Data processing logic
- Report rendering
- User interface elements

**SSOT Documents:**
- decision_governance.md
- confidence_model.md
- action_space_framework.md

---

## 2. ARCHITECTURE DOMAIN

**Responsibility:**
System design, structural principles, and architectural boundaries.

**Owns:**
- System architecture specifications
- Engine design principles
- Report pipeline architecture
- Semantic reasoning architecture
- Domainization rules (this document)
- Artifact boundary definitions
- Integration patterns
- Deployment architecture patterns

**Cannot Own:**
- Business logic implementation
- Data content
- User experience design
- Specific market signals

**SSOT Documents:**
- system_architecture.md
- engine_design_principles.md
- report_pipeline_architecture.md
- semantic_reasoning_rules.md
- portfolio_os_domainization_steering.md (this document)

---

## 3. LOGIC / INTELLIGENCE DOMAIN

**Responsibility:**
Core reasoning engines, signal processing, and portfolio intelligence.

**Owns:**
- Signal generation engines
- Semantic interpretation engine
- PM reasoning logic
- Scoring algorithms
- Portfolio health assessment
- Correlation/dependency analysis
- Scenario calculation logic
- Opportunity identification logic

**Cannot Own:**
- Report language rendering
- User interface components
- Data ingestion rules
- Deployment configuration

**SSOT Documents:**
- semantic_signal_registry.md
- signal_calculation_framework.md
- portfolio_health_framework.md
- correlation_dependency_framework.md
- scoring_methodology_framework.md
- opportunity_engine_design.md

**Implementation Artifacts:**
- engines/allocation_engine.py
- engines/semantic_engine.py
- engines/regime_engine.py
- engines/attribution_engine.py
- engines/priority_engine.py
- engines/scenario_engine.py
- engines/decision_engine.py
- engines/scoring_engine.py
- engines/quality_engine.py

---

## 4. REPORT DOMAIN

**Responsibility:**
Report generation, PM reasoning synthesis, and language rendering.

**Priority Rule:**
Every new feature must add measurable value to this domain.

**Owns:**
- Report reasoning system
- Report section specifications
- PM report engine implementation
- Briefing output generation
- Language rendering rules
- Report quality standards
- Multilingual framework
- Report traceability requirements

**Cannot Own:**
- Raw signal generation
- Semantic state creation
- Data ingestion logic
- User interface design

**SSOT Documents:**
- report_reasoning_system.md
- report_section_specification.md
- multilingual_rendering_framework.md

**Implementation Artifacts:**
- engines/report_engine.py
- engines/morning_briefing_engine.py
- engines/delta_engine.py
- reports/pm_report_engine.py

**Output Artifacts:**
- portfolio_report.txt
- morning_briefing.txt
- allocation_briefing.txt
- All .txt briefing files

---

## 5. PORTFOLIO STATE DOMAIN

**Responsibility:**
Portfolio state modeling, position tracking, and exposure analysis.

**Owns:**
- Portfolio state model specifications
- Watchlist vs portfolio separation rules
- Asset registry frameworks
- Category mapping logic
- Exposure state calculations
- Capital state tracking
- Structural state assessment
- Position-level data models

**Cannot Own:**
- Market data ingestion
- Report generation
- User interface elements
- Deployment configuration

**SSOT Documents:**
- portfolio_state_model.md
- watchlist_asset_registry_framework.md

**Data Artifacts:**
- watchlist.xlsx
- data.json
- Portfolio-related .xlsx outputs

---

## 6. DATA / INGESTION DOMAIN

**Responsibility:**
Data ingestion, normalization, and source management.

**Owns:**
- Data ingestion frameworks
- Normalization rules
- Source hierarchy definitions
- Google Sheets migration specifications
- Google Finance validation rules
- Data freshness requirements
- File I/O governance
- Data quality standards

**Cannot Own:**
- Portfolio reasoning logic
- Report generation
- User experience design
- Semantic interpretation

**SSOT Documents:**
- data_ingestion_normalization_framework.md
- trusted_signal_sources.md

**Implementation Artifacts:**
- Data loading functions in engines
- Excel I/O operations
- Data validation logic

---

## 7. USER DOMAIN

**Responsibility:**
User-facing experience, readability, and accessibility.

**Owns:**
- User experience specifications
- Dashboard philosophy
- Readability requirements
- German/English rendering expectations
- Non-professional user clarity standards
- PM workspace behavior rules
- Accessibility guidelines
- User interface principles

**Cannot Own:**
- Business logic engines
- Data processing rules
- Deployment infrastructure
- Signal generation logic

**SSOT Documents:**
- dashboard_philosophy.md

**Implementation Artifacts:**
- app.py (Streamlit interface)
- engines/visual_engine.py

---

## 8. DEPLOYMENT DOMAIN

**Responsibility:**
Runtime configuration, deployment patterns, and infrastructure.

**Mandatory Direction:**
Google-only future deployment.
AWS, Supabase, Azure forbidden unless explicitly approved.

**Owns:**
- Local runtime configuration
- Google Cloud deployment specifications
- Streamlit deployment patterns
- Configuration governance
- Environment variable handling
- Service account strategies
- Provider constraint enforcement
- Infrastructure patterns

**Cannot Own:**
- Business logic
- Report content
- User experience design
- Portfolio reasoning

**SSOT Documents:**
- deployment_intelligence_framework.md

**Implementation Artifacts:**
- main.py (CLI runtime)
- Configuration files (future)
- Environment setup (future)

---

## 9. MEMORY / HISTORY DOMAIN

**Responsibility:**
Historical data preservation, longitudinal analysis, and memory systems.

**Owns:**
- Portfolio memory architecture
- Historical snapshot management
- History folder governance
- Longitudinal reasoning frameworks
- Previous report preservation
- Semantic evolution tracking
- Time-series analysis patterns
- Memory persistence rules

**Cannot Own:**
- Current portfolio state
- Real-time signal generation
- Report rendering logic
- User interface components

**SSOT Documents:**
- portfolio_memory_architecture.md

**Data Artifacts:**
- history/ folder contents
- Historical .xlsx files
- Time-stamped briefings

---

## 10. SIMULATION / SCENARIO DOMAIN

**Responsibility:**
Simulation architecture, stress testing, and scenario analysis.

**Owns:**
- Simulation architecture specifications
- Stress scenario frameworks
- Before/after modeling logic
- Scenario consequence analysis
- Structural vulnerability assessment
- What-if analysis patterns
- Scenario validation rules
- Simulation output standards

**Cannot Own:**
- Current portfolio state
- Report language rendering
- User interface design
- Data ingestion rules

**SSOT Documents:**
- simulation_architecture.md

**Implementation Artifacts:**
- Scenario-related engine functions
- Simulation output files

---

# SSOT DOCUMENT MAPPING

| Document | Primary Domain | Secondary Domain | Artifact Type |
|----------|---------------|------------------|---------------|
| system_architecture.md | Architecture | - | canonical_ssot |
| engine_design_principles.md | Architecture | Logic | canonical_ssot |
| semantic_reasoning_rules.md | Architecture | Logic | canonical_ssot |
| semantic_signal_registry.md | Logic | - | canonical_ssot |
| report_reasoning_system.md | Report | - | canonical_ssot |
| report_pipeline_architecture.md | Architecture | Report | canonical_ssot |
| report_section_specification.md | Report | - | canonical_ssot |
| portfolio_state_model.md | Portfolio State | - | canonical_ssot |
| portfolio_health_framework.md | Logic | Portfolio State | canonical_ssot |
| correlation_dependency_framework.md | Logic | - | canonical_ssot |
| deployment_intelligence_framework.md | Deployment | - | canonical_ssot |
| decision_governance.md | Governance | - | canonical_ssot |
| action_space_framework.md | Governance | Report | canonical_ssot |
| confidence_model.md | Governance | Logic | canonical_ssot |
| market_regime_framework.md | Logic | - | canonical_ssot |
| opportunity_engine_design.md | Logic | - | canonical_ssot |
| simulation_architecture.md | Simulation | - | canonical_ssot |
| portfolio_memory_architecture.md | Memory | - | canonical_ssot |
| dashboard_philosophy.md | User | - | canonical_ssot |
| trusted_signal_sources.md | Data | - | canonical_ssot |
| data_ingestion_normalization_framework.md | Data | - | canonical_ssot |
| watchlist_asset_registry_framework.md | Portfolio State | Data | canonical_ssot |
| scoring_methodology_framework.md | Logic | - | canonical_ssot |
| multilingual_rendering_framework.md | Report | User | canonical_ssot |
| future_framework_backlog.md | Architecture | - | canonical_ssot |
| signal_calculation_framework.md | Logic | - | canonical_ssot |
| kiro_calibration_report.md | Architecture | - | calibration_report |
| portfolio_os_domainization_steering.md | Governance | Architecture | steering_document |

---

# ARTIFACT CLASSIFICATION RULES

## Artifact Classes

### canonical_ssot
- **Allowed Domains:** All domains (as primary owner)
- **Allowed Writers:** Domain owners only
- **Allowed Readers:** All domains
- **Business Logic:** May contain specifications, not implementation
- **Rendering Logic:** Forbidden
- **Output Generation:** Forbidden

### implementation_engine
- **Allowed Domains:** Logic, Report, Data, Portfolio State
- **Allowed Writers:** Domain owners only
- **Allowed Readers:** All domains
- **Business Logic:** Required (core responsibility)
- **Rendering Logic:** Only in Report domain engines
- **Output Generation:** Allowed for structured data only

### report_output
- **Allowed Domains:** Report (primary), Memory (secondary)
- **Allowed Writers:** Report domain only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden
- **Rendering Logic:** Required
- **Output Generation:** Required (human-readable text)

### data_input
- **Allowed Domains:** Data, Portfolio State
- **Allowed Writers:** Data domain only
- **Allowed Readers:** Logic, Portfolio State, Report domains
- **Business Logic:** Forbidden
- **Rendering Logic:** Forbidden
- **Output Generation:** Forbidden

### data_output
- **Allowed Domains:** Logic, Portfolio State, Memory
- **Allowed Writers:** Domain owners only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden (structured data only)
- **Rendering Logic:** Forbidden
- **Output Generation:** Required (structured formats)

### runtime_entrypoint
- **Allowed Domains:** Deployment
- **Allowed Writers:** Deployment domain only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden
- **Rendering Logic:** Forbidden
- **Output Generation:** Orchestration only

### dashboard_surface
- **Allowed Domains:** User
- **Allowed Writers:** User domain only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden
- **Rendering Logic:** Required (visualization only)
- **Output Generation:** User interface only

### historical_snapshot
- **Allowed Domains:** Memory
- **Allowed Writers:** Memory domain only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden
- **Rendering Logic:** Forbidden
- **Output Generation:** Preservation only

### deployment_config
- **Allowed Domains:** Deployment
- **Allowed Writers:** Deployment domain only
- **Allowed Readers:** Deployment domain only
- **Business Logic:** Forbidden
- **Rendering Logic:** Forbidden
- **Output Generation:** Configuration only

### calibration_report
- **Allowed Domains:** Architecture
- **Allowed Writers:** Architecture domain only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden
- **Rendering Logic:** Analysis only
- **Output Generation:** Documentation only

### steering_document
- **Allowed Domains:** Governance, Architecture
- **Allowed Writers:** Governance domain only
- **Allowed Readers:** All domains
- **Business Logic:** Forbidden (governance rules only)
- **Rendering Logic:** Forbidden
- **Output Generation:** Governance specifications only

---

# WRITER / READER GOVERNANCE

## Writer Principles

**Signal Engines:**
- May write structured signals only
- Must not write semantic interpretations
- Must not write PM conclusions
- Must not write human-readable narratives

**Semantic Layer:**
- May write semantic states only
- Must not write raw signals
- Must not write PM reasoning
- Must not write final reports

**PM Reasoning:**
- May write reasoning objects only
- Must not write raw signals
- Must not write semantic states
- Must not write final language rendering

**Report Rendering:**
- May write human-readable text only
- Must not write business logic
- Must not invent signals or semantics
- Must explain existing reasoning only

**Dashboard:**
- May read reasoning outputs only
- Must not become truth source
- Must not generate business logic
- Must visualize existing data only

**Data Ingestion:**
- May normalize data only
- Must not reason about data
- Must not generate signals
- Must not create semantic states

**Deployment:**
- May configure runtime only
- Must not change business logic
- Must not generate reports
- Must not process portfolio data

## Reader Principles

**All Domains:**
- May read canonical SSOT documents
- May read calibration reports
- May read steering documents

**Logic Domain:**
- May read data inputs
- May read portfolio state
- Must not read deployment secrets

**Report Domain:**
- May read all reasoning outputs
- May read semantic states
- Must not read raw configuration

**User Domain:**
- May read report outputs
- May read visualization data
- Must not read internal engine states

**Memory Domain:**
- May read all historical artifacts
- May read current state snapshots
- Must preserve read-only access

---

# TARGET FOLDER MODEL

**Proposed Future Structure:**
```
docs/
├── steering/
│   ├── domains/
│   └── governance/
├── ssot/
│   ├── architecture/
│   ├── logic/
│   ├── report/
│   └── domains/
└── calibration/

src/
├── engines/
│   ├── signals/
│   ├── semantics/
│   ├── reasoning/
│   └── rendering/
├── data/
│   ├── ingestion/
│   ├── normalization/
│   └── validation/
└── deployment/
    ├── local/
    └── google/

artifacts/
├── reports/
│   ├── briefings/
│   └── intelligence/
├── data/
│   ├── inputs/
│   ├── outputs/
│   └── snapshots/
└── config/
    ├── local/
    └── google/

history/
├── reports/
├── portfolio_snapshots/
└── semantic_snapshots/
```

**Migration Rules:**
- No immediate file moves required
- Target structure for future organization
- Preserve existing functionality during transition
- Maintain domain ownership during reorganization

---

# BOUNDARY RULES

## Hard Boundaries

1. **No report without semantic states**
   - Reports must trace to semantic interpretations
   - No direct raw-signal-to-language rendering

2. **No dashboard as SSOT**
   - Dashboard visualizes existing truth
   - Dashboard cannot create business logic

3. **No engine writes final PM narrative**
   - Engines generate structured outputs only
   - Report domain owns narrative generation

4. **No renderer creates business logic**
   - Rendering translates existing meaning
   - No business decisions in presentation layer

5. **No data source bypasses normalization**
   - All data must pass through Data domain
   - No direct engine-to-external-source coupling

6. **No deployment file controls PM logic**
   - Deployment configures runtime only
   - Business logic remains in Logic domain

7. **No feature accepted unless it improves report value**
   - All features must enhance report quality
   - Report domain has veto authority

8. **No artifact without primary_domain**
   - Every file must have domain ownership
   - No orphaned artifacts allowed

9. **No cloud provider except Google direction**
   - Google Cloud, Sheets, Drive, Finance only
   - AWS, Supabase, Azure forbidden

10. **No root-level artifact growth without domain assignment**
    - New root files must declare domain ownership
    - Domain owners must approve new artifacts

## Soft Boundaries

**Cross-Domain Collaboration:**
- Domains may share secondary ownership
- SSOT documents may reference multiple domains
- Implementation may require cross-domain coordination

**Evolution Boundaries:**
- Domain responsibilities may evolve
- New domains may be created with governance approval
- Boundary adjustments require steering document updates

---

# REPORT-FIRST PRIORITY RULE

## Binding Rule

**The first implementation priority after domainization is:**
**ENHANCE REPORT**

## Feature Acceptance Criteria

Every new future function must answer:
**"How does this improve the report?"**

## Allowed Report Value

**Stronger Semantic Interpretation:**
- Better signal-to-semantic translation
- More accurate semantic state detection
- Improved semantic relationship modeling

**Better PM Reasoning:**
- Clearer structural vs tactical separation
- Enhanced dependency explanation
- Improved tradeoff analysis

**Better Concentration Explanation:**
- Clearer concentration risk communication
- Better narrative dependency analysis
- Enhanced exposure fragility explanation

**Better Dependency Explanation:**
- Improved hidden exposure detection
- Better correlation analysis
- Enhanced structural vulnerability assessment

**Better Scenario Interpretation:**
- Clearer stress scenario communication
- Better what-if analysis
- Enhanced structural impact explanation

**Better Confidence Explanation:**
- Improved confidence model implementation
- Better signal alignment communication
- Enhanced uncertainty acknowledgment

**Better Action-Space Clarity:**
- Clearer option generation
- Better tradeoff explanation
- Enhanced decision support

**Better Multilingual Rendering:**
- Improved German/English consistency
- Better semantic preservation across languages
- Enhanced accessibility

**Better Traceability:**
- Improved signal-to-conclusion tracking
- Better reasoning chain visibility
- Enhanced explainability

**Better User Understanding:**
- Clearer non-professional communication
- Better institutional PM explanation
- Enhanced readability

## Feature Rejection Criteria

**If no report value exists:**
- Defer the feature
- Require report value justification
- Reject until report enhancement identified

---

# GOOGLE-ONLY DEPLOYMENT DIRECTION

## Mandatory Direction

**Allowed Google Services:**
- Google Cloud Platform
- Google Sheets API
- Google Drive API
- Google Finance API (validation only)
- Google service accounts
- Google Cloud deployment services

**Forbidden Providers:**
- AWS (all services)
- Supabase (all services)
- Azure (all services)
- Firebase (unless explicitly approved later)
- Random third-party infrastructure
- Non-Google cloud providers

## Migration Requirements

**Data Layer:**
- Replace Excel I/O with Google Sheets API
- Implement Google Drive for file persistence
- Add Google service account authentication

**Deployment Layer:**
- Prepare Google Cloud deployment configuration
- Implement Google-native environment handling
- Add Google Cloud service integration

**Validation Layer:**
- Integrate Google Finance for market data validation
- Implement Google-based data source hierarchy
- Add Google API rate limiting and error handling

## Compliance Enforcement

**Architecture Domain:**
- Must enforce Google-only direction in all specifications
- Must reject non-Google integration proposals
- Must maintain provider constraint documentation

**Deployment Domain:**
- Must implement only Google-compatible solutions
- Must refuse AWS/Supabase integration requests
- Must prepare Google Cloud migration path

---

# GOVERNANCE ENFORCEMENT

## Domain Ownership Enforcement

**Every artifact must declare:**
```yaml
primary_domain: [domain_name]
secondary_domains: [optional_list]
artifact_type: [classification]
ownership_role: [responsibility]
allowed_writers: [domain_list]
allowed_readers: [domain_list]
ssot_relationship: [canonical|derived|implementation]
lifecycle_status: [active|deprecated|planned]
```

## Violation Response

**Ownership Violations:**
- Reject artifacts without domain declaration
- Require domain assignment for all new files
- Enforce writer/reader permissions

**Boundary Violations:**
- Reject cross-domain business logic
- Enforce rendering/logic separation
- Maintain SSOT authority

**Priority Violations:**
- Reject features without report value
- Require report enhancement justification
- Enforce report-first development

## Governance Updates

**Steering Document Updates:**
- Require Governance domain approval
- Must maintain backward compatibility
- Must preserve existing domain ownership

**Domain Boundary Changes:**
- Require cross-domain consensus
- Must update all affected SSOT documents
- Must maintain artifact ownership clarity

---

# IMPLEMENTATION NOTES

## Current State Preservation

**No Immediate Changes Required:**
- Existing files remain in current locations
- Current functionality preserved
- Existing engine orchestration maintained

**Gradual Migration Path:**
- Domain ownership can be declared incrementally
- Target folder structure implemented over time
- Boundary enforcement added progressively

## Next Steps

1. **Declare domain ownership for existing artifacts**
2. **Implement report enhancement (first priority)**
3. **Add boundary enforcement mechanisms**
4. **Begin Google Cloud migration preparation**
5. **Implement target folder structure**

---

# DEFINITION OF DONE

✓ Domain model defined with 10 canonical domains  
✓ SSOT documents mapped to primary domains  
✓ Artifact classes defined with ownership rules  
✓ Writer/reader governance established  
✓ Target folder model proposed  
✓ Boundary rules explicitly defined  
✓ Google-only deployment direction encoded  
✓ Report-first priority rule established  
✓ Governance enforcement mechanisms defined  
✓ No code changes performed  
✓ Documentation-only governance task completed  

**Status:** Portfolio OS domainization steering established.  
**Next Phase:** Implement report enhancement while respecting domain boundaries.