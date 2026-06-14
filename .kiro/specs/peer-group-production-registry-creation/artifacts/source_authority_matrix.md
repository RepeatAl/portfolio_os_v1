# Source Authority Matrix

> **Spec**: peer-group-production-registry-creation | **Task**: 1
> **Date**: 2026-06-14 | **Authority**: CTO / Architecture
> **Status**: DOCUMENTATION_ONLY

---

## Purpose

This artifact classifies every governing document referenced by the peer-group-production-registry-creation spec according to its authority type. It defines what each source may govern and how authority flows from controlling sources through methodology to field-level rules.

**Critical Statement**: This artifact classifies sources only. It does not create registry content, mint canonical IDs, approve candidate records, or mutate any production artifact.

---

## Authority Type Definitions

| Authority Type | Definition | Governance Power |
|---------------|-----------|-----------------|
| **Controlling** | Direct governing source whose decisions are binding and non-negotiable | May mandate field values, block production activation, require explicit approval |
| **Methodology authority** | Sole authority for peer group methodology, field rules, family definitions, and subcluster logic | Defines HOW peer groups are structured; no other source may override methodology decisions |
| **Terminology authority** | Defines canonical vocabulary for asset classes, instruments, styles, factors, methods, allocation, strategy, and system layers | Governs naming and classification; registry must use terminology from this source |
| **Governance authority** | Defines decision-making processes, research behavior, evidence quality, and architectural principles | Constrains HOW decisions are made but does not define registry content directly |
| **Boundary authority** | Defines what the registry must NOT do, what belongs to other layers, and scope limitations | Constrains registry scope; violation = boundary breach |
| **Downstream compatibility authority** | Defines systems that consume registry data and their interface requirements | Registry must remain compatible; does not grant these systems authority over registry content |
| **Context only** | Provides background information; does not govern, constrain, or authorize any registry decision | Zero governance power; informational reference only |

---

## Complete Source Classification (31 Sources)

### Controlling Sources (2 logical entries, 5 files)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 1 | Production Registry Readiness Review | `docs/moneyhorst/reviews/peer_group_production_registry_readiness_review.md` | Direct governing source for P1–P4 decisions, readiness conditions, and production activation prerequisites |
| 2 | P1–P4 Decision Records | `docs/moneyhorst/reviews/peer_group_p{1,2,3,4}_owner_verified_decision_record.md` | Owner-verified decisions binding on registry content (19 decisions across P1–P4) |


### Methodology Authority (1)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 3 | PGMF (Peer Group Methodology Framework) | `.kiro/specs/peer-group-registry-methodology-framework/` | Sole methodology authority for field rules, family definitions, subcluster logic, peer role assignment, and comparability criteria |

### Terminology Authority (1)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 4 | Investment Taxonomy SSOT | `docs/moneyhorst/investment_style_method_taxonomy_ssot.md` | Layer separation vocabulary: asset class, instrument, style, factor, method, allocation, strategy, system |

### Governance Authority (4)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 5 | Research Mechanism SSOT | `docs/moneyhorst/research_mechanism_ssot.md` | Research behavior, evidence quality, signal governance |
| 6 | System Architecture | `docs/system_architecture.md` | Portfolio OS system architecture and identity |
| 7 | Decision Governance | `docs/decision_governance.md` | Human governance, no-autonomous-decision constraints |
| 8 | Engine Design Principles | `docs/engine_design_principles.md` | Engine architecture principles and design constraints |

### Boundary Authority (11)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 9 | Asset Type and Sentiment Guidance | `docs/README_asset_type_and_sentiment_guidance.md` | ETF/fund and analyst sentiment boundaries |
| 10 | Semantic Reasoning Rules | `docs/semantic_reasoning_rules.md` | Semantic interpretation constraints; registry must not perform reasoning |
| 11 | Action Space Framework | `docs/action_space_framework.md` | Action-space generation boundaries; registry does not generate actions |
| 12 | Watchlist/Asset Registry | `docs/watchlist_asset_registry_framework.md` | Asset identity ownership; registry references but does not own asset identity |
| 13 | Confidence Model | `docs/confidence_model.md` | Confidence = evidence alignment, not prediction; registry confidence fields follow this model |
| 14 | Data Ingestion Framework | `docs/data_ingestion_normalization_framework.md` | Ingestion boundary — no data ingestion implementation within registry scope |
| 15 | Scoring Methodology | `docs/scoring_methodology_framework.md` | No scoring/ranking from registry; scoring belongs to downstream layers |
| 16 | Market Regime Framework | `docs/market_regime_framework.md` | No regime conclusions from registry; regime analysis belongs elsewhere |
| 17 | Multilingual Rendering | `docs/multilingual_rendering_framework.md` | Language-independent structural states; rendering belongs downstream |
| 18 | Dashboard Philosophy | `docs/dashboard_philosophy.md` | Rendering belongs downstream; registry provides data, not presentation |
| 19 | Deployment Intelligence Framework | `docs/deployment_intelligence_framework.md` | Deployment boundary; registry does not deploy or manage deployment |


### Downstream Compatibility Authority (9)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 20 | Portfolio State Model | `docs/portfolio_state_model.md` | Portfolio state ownership; registry must be compatible with state model consumption |
| 21 | Semantic Signal Registry | `docs/semantic_signal_registry.md` | Signal authority model; registry provides context consumed by signal layer |
| 22 | Report Reasoning System | `docs/report_reasoning_system.md` | Report rendering boundaries; registry provides data for report reasoning |
| 23 | Report Pipeline Architecture | `docs/report_pipeline_architecture.md` | Report pipeline consumption interface |
| 24 | Portfolio Health Framework | `docs/portfolio_health_framework.md` | Health/dependency analysis boundaries; health calculations owned by this framework, not registry |
| 25 | Opportunity Engine Design | `docs/opportunity_engine_design.md` | Opportunity screening boundaries; registry provides context, engine owns screening logic |
| 26 | Correlation/Dependency Framework | `docs/correlation_dependency_framework.md` | Dependency interpretation boundaries; correlation calculations owned by this framework |
| 27 | Portfolio Memory Architecture | `docs/portfolio_memory_architecture.md` | Memory layer boundaries; registry provides structural context to memory layer |
| 28 | Signal Calculation Framework | `docs/signal_calculation_framework.md` | Signal hierarchy; registry does not calculate signals |
| 29 | Trusted Signal Sources | `docs/trusted_signal_sources.md` | Signal hierarchy; registry does not define or validate signal sources |

### Context Only (2)

| # | Source | Path | Authority Scope |
|---|--------|------|----------------|
| 30 | Preflight Spec | `.kiro/specs/peer-group-registry-creation-preflight/` | Background context from completed preflight phase; no governance power |
| 31 | Future Framework Backlog | `docs/future_framework_backlog.md` | Context only; planned future capabilities with zero current authority |

---

## Source Count Summary

| Authority Type | Count |
|---------------|-------|
| Controlling | 2 (5 files) |
| Methodology authority | 1 |
| Terminology authority | 1 |
| Governance authority | 4 |
| Boundary authority | 11 |
| Downstream compatibility authority | 9 |
| Context only | 2 |
| **Total** | **31 classified entries** |

---

## Authority Chain

The authority chain defines how decisions flow from controlling sources through methodology to field-level rules. No intermediate layer may override a higher-authority source.

```
Level 1: CONTROLLING
┌─────────────────────────────────────────────────────────────────────┐
│ Production Registry Readiness Review                                │
│ P1–P4 Decision Records                                             │
│                                                                     │
│ → These sources MANDATE what the registry must contain              │
│ → Their decisions are final and non-negotiable                      │
│ → They define WHAT gets produced                                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ governs
                               ▼
Level 2: METHODOLOGY AUTHORITY
┌─────────────────────────────────────────────────────────────────────┐
│ PGMF (Peer Group Methodology Framework)                            │
│                                                                     │
│ → Sole authority for HOW peer groups are structured                 │
│ → Defines families, subclusters, roles, comparability rules         │
│ → Translates controlling decisions into structural methodology      │
│ → No other source may override PGMF methodology decisions           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ constrains
                               ▼
Level 3: TERMINOLOGY + GOVERNANCE + BOUNDARY
┌─────────────────────────────────────────────────────────────────────┐
│ Terminology: Investment Taxonomy SSOT                               │
│ Governance: Research SSOT, System Arch, Decision Gov, Engine Design │
│ Boundary: Asset Type, Semantic Rules, Action Space, Watchlist,      │
│           Confidence, Data Ingestion, Scoring, Market Regime,       │
│           Multilingual, Dashboard, Deployment Intelligence          │
│                                                                     │
│ → Terminology defines WHAT WORDS MEAN                               │
│ → Governance defines HOW DECISIONS ARE MADE                         │
│ → Boundary defines WHAT THE REGISTRY MUST NOT DO                    │
│ → Together they constrain the solution space                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ informs
                               ▼
Level 4: DOWNSTREAM COMPATIBILITY
┌─────────────────────────────────────────────────────────────────────┐
│ Portfolio State, Semantic Signal Registry, Report Reasoning,        │
│ Report Pipeline, Portfolio Health, Opportunity Engine,              │
│ Correlation/Dependency, Portfolio Memory, Signal Calculation,       │
│ Trusted Signal Sources                                             │
│                                                                     │
│ → Registry must remain COMPATIBLE with these consumers              │
│ → These systems do NOT govern registry content                      │
│ → They define interface expectations the registry must satisfy      │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ references
                               ▼
Level 5: CONTEXT ONLY
┌─────────────────────────────────────────────────────────────────────┐
│ Preflight Spec, Future Framework Backlog                           │
│                                                                     │
│ → Zero governance power                                             │
│ → Informational background only                                     │
│ → May not be cited as authority for any decision                    │
└─────────────────────────────────────────────────────────────────────┘
```


### Decision Flow Example

```
Controlling Decision: "SMCI assigned to PGF-01 Semiconductor" (P1 Decision Record)
       │
       ▼
Methodology Translation: PGMF defines PGF-01 field rules, subcluster options,
                         comparability criteria for semiconductors
       │
       ▼
Terminology Constraint: Investment Taxonomy SSOT confirms "Semiconductor"
                        is a valid asset class category
       │
       ▼
Boundary Constraint: Scoring Methodology confirms registry must NOT score SMCI;
                     Confidence Model confirms evidence_status field semantics
       │
       ▼
Downstream Compatibility: Portfolio State Model, Semantic Signal Registry,
                          Report Reasoning all define how they will consume
                          the SMCI peer group record (read-only)
       │
       ▼
Context Reference: Preflight Spec shows historical context for SMCI assignment
                   (no governance power)
```

---

## Extension Governance

### Adding New Sources

New sources may only be added to this authority matrix under the following conditions:

1. **CTO Approval Required**: No source may be added without explicit CTO approval recorded with approver identity and date.
2. **Authority Type Required**: Every new source must be classified into exactly one authority type before addition.
3. **Non-Escalation Rule**: A new source cannot be added at a higher authority level than existing sources without formal governance review.
4. **Documentation Required**: The addition must include:
   - Source name and path
   - Authority type classification
   - Justification for addition
   - CTO approval artifact reference
5. **No Silent Addition**: Adding a source without documented CTO approval is a governance violation.

### Removing Sources

Sources may not be removed from the matrix. They may only be reclassified to "Context only" with CTO approval if their governance power is revoked.

### Reclassifying Sources

Authority type reclassification requires:
- CTO approval with recorded identity and date
- Justification document
- Impact analysis on downstream tasks

---

## Boundary Confirmations

- [ ] This artifact classifies sources only
- [ ] No registry content created
- [ ] No canonical peer_group_id values minted
- [ ] No candidate records approved
- [ ] No SAI artifacts mutated
- [ ] No runtime code produced
- [ ] Extension governance requires CTO approval

---

## Traceability

| Requirement | Coverage |
|------------|----------|
| R12 (Source Authority) | All 31 sources classified with authority types, chain documented, extension governance defined |

---

```
TASK_1_SOURCE_AUTHORITY_MATRIX_COMPLETE
```

---

*End of source authority matrix.*
