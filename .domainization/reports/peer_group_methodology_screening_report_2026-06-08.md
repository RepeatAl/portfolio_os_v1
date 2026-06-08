# Peer Group Methodology Source Screening Report

**Artifact**: peer_group_methodology_screening_report_2026-06-08.md
**Date**: 2026-06-08
**Branch**: spec/peer-group-methodology-source-screening
**Authority**: Research / Source Screening
**Status**: screening complete
**Purpose**: Human-readable screening report explaining what was read, why it matters, what was extracted, what remains unresolved, and whether the system is ready for a methodology framework spec.

---

## 1. Scope

This report documents the completion of the Peer Group Methodology Source Screening task. The task followed the merge of PR #41 (peer group registry scope preflight) and is the first step toward building a Goldman-Sachs-level Peer Group Registry Methodology Framework for MoneyHorst.

The task did not create a Peer Group Registry. It did not finalize peer groups. It did not answer Q1–Q10 canonically. It collected and structured the institutional evidence needed to answer those questions with documented authority.

Three artifacts were produced:
1. `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` — 22 sources documented with authority tier, Q-mapping, extracted principles, registry fields impacted, and rule type.
2. `.domainization/reports/peer_group_methodology_evidence_matrix_2026-06-08.md` — Q1–Q10 evidence matrix with readiness status per question.
3. This screening report.

---

## 2. Sources Inspected

Eight source families were screened. 22 individual sources were registered.

| Category | Sources | Tier 1 | Institutions |
|----------|---------|--------|-------------|
| A — GIPS / CFA Governance | 3 | 3 | CFA Institute |
| B — GICS Taxonomy | 3 | 3 | MSCI, S&P Global |
| C — ICB Taxonomy | 2 | 1 | FTSE Russell / LSEG |
| D — Porter's Five Forces | 1 | 1 | Harvard Business Review / Porter |
| E — Comparable Company Analysis | 3 | 2 | NYU Stern / Damodaran |
| F — ETF / Fund Methodology | 4 | 1 | Morningstar, Columbia Law, etf.com |
| G — Security Identification / ADR | 3 | 1 | OpenFIGI, Intrinio, OpenSanctions |
| H — Accounting Comparability | 3 | 3 | IFRS Foundation, KPMG, PwC |
| **Total** | **22** | **15** | |

All 22 sources are recorded in the source registry with full provenance. No source relied on blogs or SEO content without explicit Tier 3 marking. Tier 3 sources are marked context-only and are not used as standalone authority for any rule.

---

## 3. Why Each Source Family Matters

### A — GIPS / CFA (Governance Analogy)

GIPS does not govern peer classification directly. Its value for MoneyHorst is as a governance framework analogy. The two core GIPS principles — fair representation and full disclosure — establish institutional standards for how methodology must be documented, versioned, and audited. Without these governance principles applied to peer group management, the registry will produce outputs that cannot be independently verified or reproduced. GIPS also establishes the institutional precedent for annual review cycles and version management, which directly inform Q9 and Q10.

### B — GICS (Primary Taxonomy Discipline)

GICS is the dominant global industry classification system used by asset managers, index providers, and portfolio management platforms worldwide. Its principles — one primary classification per company, revenue-first determination, annual review — represent the global institutional consensus on how company classification should work. MoneyHorst must either adopt these principles or explicitly document where and why it departs from them. Undocumented departure from GICS would undermine the credibility of the registry.

### C — ICB (European Taxonomy Reference)

ICB is the standard used by European exchanges. Multiple MoneyHorst peer group families (PGF-06 Defense, PGF-07 Industrials, PGF-08 Banks) include European-listed companies classified under ICB, not GICS. A peer group methodology that only references GICS will not correctly handle Rheinmetall, Siemens, ADYEN, or SAN. ICB also provides the most developed institutional model for challenge/appeal governance of classification decisions, which directly informs Q9 subcluster governance design.

### D — Porter's Five Forces (Strategic Peer Logic)

The Five Forces framework establishes the conceptual architecture for why direct rivals are not the only competitive comparison context. Without this foundation, the peer group methodology would default to naive GICS sub-industry peers and miss substitute peers, ecosystem adjacency, and cross-industry competitive dynamics. UBER competing with LYFT (direct rival) vs. UBER competing with DASH (delivery substitute) cannot be captured without a framework that distinguishes peer roles. Porter provides that framework. It is the strategic authority behind the core/adjacent tier structure in Q3.

### E — Comparable Company Analysis (Damodaran)

Damodaran's comparable company analysis framework is the most authoritative source for financial comparability gates. It establishes that peer comparison validity depends on business model similarity, size comparability, growth profile, margin structure, capital intensity, leverage, and accounting standards. Without these gates, the registry would assign peers that look similar on the surface but are financially non-comparable — a direct path to misleading SAI-BLK-21 diagnostic outputs.

### F — ETF / Fund Methodology (Morningstar, Columbia Law, etf.com)

PGF-09 requires a distinct comparison framework. Morningstar's tracking difference / tracking error framework is the institutional standard. Columbia Law's research confirms that name/theme similarity is insufficient for ETF peer comparison — multi-dimensional comparison is required. Together these sources define the specific fields (TER, tracking difference, tracking error, AUM, domicile, replication method, distribution policy, look-through) that must be in the ETF peer group registry record.

### G — Security Identification / ADR Normalization (OpenFIGI, Intrinio)

Cross-listed securities are a systematic challenge for any global peer group registry. OpenFIGI is the open institutional standard for instrument identification. Intrinio's security master architecture describes the canonical data model for separating economic entities from their listing vehicles. Without a canonical entity ID approach, the registry will double-count ASML, misidentify ADRs, and break on relisting events.

### H — Accounting Comparability (IFRS Foundation, KPMG, PwC)

R&D capitalization, lease accounting, inventory methods, and financial instrument classification differ between IFRS and US GAAP in ways that materially affect P&L and balance sheet comparisons. Without these sources, the registry would have no evidence base for the comparability_adjustment_required field or the accounting_standard field, and cross-region peer comparisons would silently produce misleading outputs.

---

## 4. What Each Source Contributes to MoneyHorst

| Source Category | Primary Contribution | Becomes in Registry |
|-----------------|---------------------|---------------------|
| GIPS / CFA | Governance and disclosure principles | Hard governance rules for versioning, review cycle, methodology disclosure |
| GICS | One-primary-classification + revenue basis + annual review | primary_family field design + Q1 answer direction + versioning pattern |
| ICB | Cross-region taxonomy + challenge/appeal governance | taxonomy_reference field + Q9 governance model for European peers |
| Porter Five Forces | Peer role taxonomy: direct vs. substitute vs. ecosystem | peer_role field (core / adjacent / benchmark_context) + Q2/Q3 answer direction |
| Damodaran Comps | Financial comparability gates | financial_comparability_gate field + Q6/Q8 comparability flag design |
| ETF Methodology | ETF-specific comparison field set | PGF-09 fields: TER, tracking_difference, tracking_error, domicile, AUM, etc. |
| OpenFIGI / Security Master | Entity vs. listing distinction + identifier architecture | canonical_entity_id field + Q4 architecture decision |
| IFRS/GAAP Sources | Accounting standard comparability gaps | accounting_standard, comparability_adjustment_required, restatement_flag fields |

---

## 5. What Should Become Hard Rule vs. Soft Context

### Hard rules (non-negotiable in the methodology framework):

1. **One primary family per asset** — GICS precedent. Deviations require documented rationale.
2. **Revenue as primary classification basis** — GICS and ICB convergence.
3. **Peer_role taxonomy required** — Porter. Every peer must be labeled core, adjacent, or benchmark_context.
4. **Financial comparability gates** — Damodaran. Size, growth, margin, capital structure, accounting standard must be assessed before peer assignment.
5. **ETF peer comparison is multi-dimensional** — Morningstar / Columbia Law. TER, tracking difference, and tracking error are mandatory.
6. **Canonical entity ID required** — OpenFIGI / Intrinio. Ticker alone is insufficient.
7. **Accounting standard must be documented per peer** — KPMG / PwC. Cross-standard comparison requires comparability_adjustment_required flag.
8. **Versioning required** — GICS/GIPS. Effective_date versioning is minimum standard.
9. **Annual review minimum** — GICS/GIPS. At least annual review of all subcluster assignments.
10. **ETFs and indices are never company peers** — Architectural rule, not a soft guideline.

### Soft context (governed by judgment, not algorithm):

1. **Multi-family membership** — Analytically correct for UBER/AMZN/VRT but no institutional standard prescribes this. Q2 requires human/CTO decision.
2. **Specific market-cap threshold values** — The principle is hard; the specific numbers are judgment calls requiring additional sourcing.
3. **Challenge/appeal governance** — ICB models this; whether MoneyHorst needs it is a governance design choice.
4. **Private comparable handling** — No authoritative methodology exists. Must remain soft or be explicitly deferred.

---

## 6. What Is Still Unresolved

### Q6 — Liquidity / Market-Cap Thresholds (EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED)

The principle that size comparability matters is well-evidenced. The specific numeric thresholds (e.g., must a core peer be within 5x market cap of the subject company?) are not prescribed by any source in the current registry. Additional sourcing from index construction methodology (Russell index methodology, MSCI index construction rules) is needed before a numeric threshold can be proposed.

**Recommended action**: Source Russell/MSCI index construction methodology before the methodology framework spec is written. Alternatively, adopt a soft threshold approach with human-defined ranges at the time of registry creation.

### Q7 — Private Comparables (EVIDENCE_INSUFFICIENT)

No source in the current registry addresses private comparable methodology at the required depth. The gap is real: SpaceX (PGF-06), Stripe (PGF-03), and ByteDance (PGF-05) are competitive peers with no public listing.

**Recommended action**: Either (a) defer private comparable handling to a future registry extension and mark it scope_deferred in the methodology framework, or (b) source M&A advisory / private equity valuation methodology from a CFA or investment banking reference before the framework spec is written.

---

## 7. How This Evidence Supports the Future Peer Group Registry Methodology Framework

The Peer Group Registry Methodology Framework spec will need to answer these foundational questions. Evidence readiness per question:

| Question | Evidence Ready? |
|----------|----------------|
| What is the organization principle? | Yes — asset-level with primary + secondary families |
| What are the membership rules? | Yes — core + adjacent tier structure |
| How are entities identified? | Yes — canonical entity ID architecture defined |
| How are ETFs/indices stored? | Yes — role-separated storage with ETF-specific field set |
| What comparability gates govern peer assignment? | Partially — principles defined; threshold values need sourcing |
| How are cross-region peers handled? | Yes — accounting standard field + comparability_adjustment_required flag |
| How is the registry governed? | Yes — annual + event-triggered review with documented rationale |
| How does the registry version? | Yes — effective_date versioning as minimum standard |

This evidence base enables writing a methodology framework spec at institutional quality. The framework spec is the correct next step after human review.

---

## 8. Why Registry Creation Is Still Prohibited After This Task

This task produced evidence documentation only. No canonical peer groups have been created. No peer group IDs have been assigned. No registry YAML has been written. No Q1–Q10 decisions have been made canonically.

The Peer Group Registry cannot be created until:
1. Q1–Q10 are answered canonically by human/CTO decision.
2. A Peer Group Registry Methodology Framework spec has been written and approved.
3. The registry structure (fields, data model, governance rules) has been designed.
4. The registry creation task has been formally scoped and approved.

This evidence screening is Step 1 of that process. It is complete. Steps 2–4 remain.

---

## 9. Proposed Next Step After Human Review

**Recommended next step**: Human review of the evidence matrix, followed by CTO decisions on Q1–Q10, followed by creation of a Peer Group Registry Methodology Framework spec.

**The next step is NOT registry creation.**
**The next step is NOT peer group assignment.**
**The next step is a methodology framework specification informed by CTO decisions on Q1–Q10.**

Proposed branch for next step: `spec/peer-group-registry-methodology-framework`
Proposed spec location: `.kiro/specs/peer-group-registry-methodology-framework/`

---

## 10. Boundary Confirmations

| Item | Confirmed |
|------|-----------|
| No Peer Group Registry created | CONFIRMED |
| No canonical peer group IDs assigned | CONFIRMED |
| No peer group YAML created | CONFIRMED |
| No SAI artifacts modified | CONFIRMED |
| No registry / SSOT mutation | CONFIRMED |
| No implementation code | CONFIRMED |
| No scoring / ranking / recommendation / allocation / trading logic | CONFIRMED |
| No Q1–Q10 answered canonically | CONFIRMED |
| All sources recorded with provenance | CONFIRMED |
| All Q1–Q10 have at least one evidence mapping | CONFIRMED |
| Q6 marked EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED | CONFIRMED |
| Q7 marked EVIDENCE_INSUFFICIENT | CONFIRMED |
| No Tier 3 sources used as standalone authority | CONFIRMED |
| All copyrighted source content summarized and cited | CONFIRMED |

---

## 11. Final Screening Status

```
PEER_GROUP_METHODOLOGY_SOURCE_SCREENING_COMPLETE
```

**Evidence summary**:
- 22 sources inspected across 8 source families
- 15 Tier 1 institutional sources
- 8 of 10 Q1–Q10 questions: EVIDENCE_SUFFICIENT_FOR_METHOD_DECISION
- 1 of 10 questions: EVIDENCE_PARTIAL_MORE_RESEARCH_REQUIRED (Q6 — threshold values)
- 1 of 10 questions: EVIDENCE_INSUFFICIENT (Q7 — private comparables)
- No blocking gaps for methodology framework creation
- Registry creation remains prohibited until methodology framework spec is approved

---

*End of screening report. Content was rephrased for compliance with licensing restrictions.*
