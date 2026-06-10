# Peer Group Registry Methodology Framework

**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-10
**Authority**: CTO / Architecture

---

## Framework Status

| Dimension | Status |
|-----------|--------|
| Framework status | COMPLETE_PENDING_FINAL_HUMAN_REVIEW |
| Implementation status | METHODOLOGY_ONLY |
| Registry status | NOT_CREATED |
| Runtime status | NOT_IMPLEMENTED |
| SAI status | COMPATIBILITY_VERIFIED_NOT_MUTATED |
| Verification gate | VG-PGMF-1 PASS |
| Completion scope | Tasks 1–12 |

---

## 1. What This Framework Is

The Peer Group Registry Methodology Framework defines the rules, field taxonomy, governance model, and architectural constraints that any future Peer Group Registry must satisfy. It answers ten foundational design questions (Q1–Q10) using evidence from 35 institutional sources. Every decision traces to at least one Tier 1 source within the correct authority domain.

The framework operates at the methodology layer only. No registry data exists. No peer groups are assigned. No runtime code is implemented. No market data is integrated. No trading functionality is created.

---

## 2. Completed Artifact Inventory

| Task | Artifact | Purpose | Status |
|------|----------|---------|--------|
| 1 | decision_intake_review_2026-06-08.md | Q1–Q10 canonical decisions with evidence citations | Complete |
| 2 | source_authority_verification_2026-06-08.md | Traceability: all decisions cite Tier 1 in correct domain | Complete |
| 3 | field_taxonomy_reference_2026-06-08.md | Complete field catalog by scope (4 categories, ~90 fields) | Complete |
| 4 | etf_fund_peer_rule_specification_2026-06-08.md | PGF-09: etf_peer, benchmark_context, 11 comparison fields | Complete |
| 5 | cross_region_comparability_specification_2026-06-08.md | GAAP/IFRS normalization, currency, taxonomy reconciliation | Complete |
| 6 | governance_versioning_specification_2026-06-08.md | Non-overlap, review cycles, event triggers, as-of-date lookup | Complete |
| 7 | market_data_readiness_specification_2026-06-08.md | 8 CURRENT_MODEL_NULLABLE + 9 FUTURE_VENDOR_INTEGRATION | Complete |
| 8 | trading_governance_boundary_2026-06-08.md | 17 FUTURE_COMPLIANCE_REFERENCE fields, three-gate model | Complete |
| 9 | unsupported_asset_class_handling_2026-06-08.md | 30+ categories, 10 handling statuses, derivative/private/crypto | Complete |
| 10 | sai_compatibility_verification_2026-06-08.md | 10 blocking states, 12 scenarios, compatibility matrix | Complete |
| 11 | gate_vg_pgmf_1.md | Verification gate: 16 checks PASS, 10 drift categories NONE | Complete |

---

## 3. Methodology Chain (Completed)

```
Decision Intake (Q1–Q10) → Source Authority → Field Taxonomy
→ ETF/Fund Handling → Cross-Region Comparability
→ Governance/Versioning → Market Data Readiness
→ Trading Governance Boundary → Unsupported Asset Handling
→ SAI Compatibility → Verification Gate VG-PGMF-1 (PASS)
→ README Finalization (this document)
```

---

## 4. Verified Boundary Summary

The completed framework does NOT create:

- peer_group_registry.yaml
- Final peer group assignments
- Canonical peer_group_id values
- SAI mutations
- Runtime code or validation code
- Market-data integration
- Broker, exchange, ATS, or trading venue connectivity
- Order routing or execution logic
- Market-access controls, kill-switch, or surveillance runtime
- Compliance certification or claims

---

## 5. SAI Compatibility Summary

**SAI may**: Read methodology as context; explain blocked states; preserve useful context; surface methodology status.

**SAI may NOT**: Create registry entries, peer_group_id values, final peer assignments, runtime behavior, trading implications, or execution eligibility.

**Key blocking states**: BLOCK_FINAL_PEER_ASSIGNMENT, BLOCK_UNSUPPORTED_ASSET_CLASS, BLOCK_SOURCE_INSUFFICIENT, BLOCK_IDENTITY_UNRESOLVED, BLOCK_GOVERNANCE_CONFLICT, BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED, BLOCK_ETF_COMPANY_FALLBACK, BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY, BLOCK_TRADING_ELIGIBILITY_INFERENCE.

---

## 6. Unsupported Asset Class Summary

Unsupported, deferred, context-only, or reference-only: private companies, derivatives, options, warrants, certificates, leveraged products, structured products, crypto/tokenized assets, commodities, FX pairs, bonds, money-market instruments, indices/baskets, synthetic exposures, unresolved identities.

No unsupported asset class receives peer assignment unless a future methodology extension is explicitly created, sourced, reviewed, and approved through the six-step extension pathway.

---

## 7. Market Data and Trading Boundary

| Concern | Status |
|---------|--------|
| Market data readiness | 8 fields reserved (CURRENT_MODEL_NULLABLE, null in v1) |
| Market data integration | NOT active — FUTURE_VENDOR_INTEGRATION |
| Peer group eligibility | Based on methodology, NOT on market data availability |
| Tradability | Requires regulated-entity status — FUTURE_COMPLIANCE_REFERENCE |
| Trading governance | 17 fields reserved as vocabulary only — NOT operational |
| Broker connectivity | NOT modeled — outside this framework |

**Key rule**: Market data availability NEVER implies peer methodology eligibility or trading readiness.

---

## 8. Future Extension Pathway

Any move from methodology to operational use requires a separate future spec:
1. Productive schema (peer_group_registry.yaml)
2. Canonical peer_group_id governance
3. Validation logic
4. Source authority enforcement (runtime)
5. SAI integration contracts
6. Audit behavior
7. Test coverage
8. Human approval

---

## 9. Downstream Usage Guidance

**May reference PGMF as**: methodology foundation, governance reference, source authority reference, SAI compatibility reference, peer classification design input.

**May NOT treat PGMF as**: active registry, runtime module, completed peer assignment database, trading eligibility system, market data entitlement system, broker or execution system.

---

## 10. Verification Status

| Item | Result |
|------|--------|
| VG-PGMF-1 gate | PASS |
| Gate checks (A–P) | 16/16 PASS |
| Drift risk | 10/10 NONE |
| Human review checklist | 15/15 YES |
| Tasks completed | 12/12 |

---

## 11. Final Human Review Checklist

| # | Check | Status |
|---|-------|--------|
| 1 | README updated | YES |
| 2 | Artifact inventory complete | YES |
| 3 | Tasks 1–12 complete | YES |
| 4 | VG-PGMF-1 PASS referenced | YES |
| 5 | Methodology-only boundary preserved | YES |
| 6 | No registry created | YES |
| 7 | No peer assignments | YES |
| 8 | No peer_group_id values | YES |
| 9 | No SAI mutation | YES |
| 10 | No runtime code | YES |
| 11 | No market-data integration | YES |
| 12 | No trading/execution logic | YES |
| 13 | Ready for final human review | YES |

---

## 12. Final Framework Status

```
PGMF_FRAMEWORK_README_UPDATED_READY_FOR_FINAL_HUMAN_REVIEW
```

---

*End of README.*
