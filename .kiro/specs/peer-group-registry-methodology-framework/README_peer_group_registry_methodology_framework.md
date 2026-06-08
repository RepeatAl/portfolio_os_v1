# Peer Group Registry Methodology Framework

**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: draft — ready for human review

---

## 1. What This Framework Is

The Peer Group Registry Methodology Framework defines the rules, field taxonomy, governance model, and architectural constraints that any future Peer Group Registry must satisfy. It answers ten foundational design questions (Q1–Q10) using evidence from 35 institutional sources screened during the Peer Group Methodology Source Screening task. Every decision traces to at least one Tier 1 institutional source.

The framework operates at the methodology layer. It specifies how economic entities are identified, how assets are classified into peer families, what roles peers may have, what financial comparability gates must pass before a peer assignment is valid, how cross-region peers are handled, how ETFs and indices are kept separate from company peers, how peer groups are versioned and reviewed, and what fields are reserved for future market data and trading governance.

This framework is not a Peer Group Registry. It does not assign peer groups to assets. It does not create canonical peer group IDs. It is the rulebook that governs the registry when it is eventually created.

---

## 2. Why This Framework Exists

MoneyHorst needs peer groups that are not ad-hoc, narrative-driven, or AI-invented. SAI-BLK-21 (Peer Comparison) is currently blocked because no canonical peer group definitions exist. To unblock SAI-BLK-21, a Peer Group Registry must be created — but the registry must be built on a sound, institutionally grounded methodology.

The evidence screening identified that 8 of 10 foundational design questions have sufficient evidence for a decision. This framework converts those evidence-backed decisions into enforceable methodology rules. Without this framework, any registry created would risk drift, ambiguity, and silent false peer comparisons.

---

## 3. What This Framework Enables

When this framework is approved and a Peer Group Registry is subsequently created under its rules:

- SAI-BLK-21 will produce peer-relative financial metric observations, competitive position interpretation, and peer-relative red flag assessments
- SAI-BLK-19 gains peer-relative strength observations in addition to benchmark and sector dimensions
- SAI-BLK-20 gains peer correlation observations in addition to benchmark and sector correlation
- Cross-family candidates (UBER, AMZN, VRT) will have correctly modeled primary and secondary peer families
- European-listed peers (Rheinmetall, ASML, ADYEN, SAN, Siemens) will be correctly handled with accounting standard flags
- ETFs and indices will be formally stored as benchmark_context without contaminating company peer groups
- Peer groups will version correctly over time

---

## 4. What This Framework Does Not Enable

This framework does NOT enable:

- **Peer group assignment**: Which specific companies belong to which families is a registry data decision. Registry creation is a separate future task.
- **Real-time market data**: The framework reserves data model fields but does not integrate any data feed.
- **Broker or exchange connectivity**: No trading venue connections are created or implied.
- **Order routing or trading logic**: All trading governance fields are future compliance references only. MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue.
- **SAI modification**: SAI is architecturally complete. The interface contract in `deferred_interfaces.md` Section 2.3 is already correct.

---

## 5. How This Framework Relates to SAI

SAI-BLK-21 depends on the Peer Group Registry for canonical peer definitions. The interface contract was declared in:

- `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` — Section 2.3
- `.kiro/specs/single-asset-intelligence-framework/artifacts/peer_benchmark.md` — Section 6

This methodology framework defines exactly the elements SAI expects to consume. When the registry is eventually created under this framework's rules, it will satisfy the SAI interface contract. No SAI artifact is modified.

---

## 6. How This Framework Relates to Future Peer Group Registry

```
This Framework (methodology rules)
    → Registry Creation Preflight (map 9 families to methodology fields)
    → Human/CTO approval of candidate records
    → Peer Group Registry (canonical data)
    → SAI-BLK-21 consumption
```

The registry may only be created after: (1) this methodology framework is approved, (2) a registry creation preflight is completed, (3) candidate records are approved by human/CTO.

---

## 7. How This Framework Relates to Market Data and Trading Readiness

The framework reserves market data fields (exchange_mic, exchange_timezone, trading_calendar_id, market_data_source, data_vendor, data_latency_class, derived_data_policy) in the registry data model now, so that adding quote data later does not require a structural registry rewrite.

All trading governance fields (pre-trade controls, best execution, kill switch, audit log, surveillance, market abuse monitoring) are reserved as future compliance references only. They are not implemented. They are not current obligations.

Evidence source: `.domainization/reports/market_data_exchange_and_trading_readiness_evidence_2026-06-08.md`

---

## 8. Which Future Specs Depend on This Framework

| Future Spec | Dependency |
|-------------|-----------|
| Peer Group Registry Creation | Registry must be built under these methodology rules |
| Market Data / Quote Integration | Depends on data model readiness fields (Section 8 of requirements.md) |
| SAI-BLK-21 Full Activation | Depends on Peer Group Registry with canonical definitions |
| Trading Readiness Framework | Depends on trading governance boundary (Section 9 of requirements.md) |
| Private Comparable Methodology | Q7 future extension — requires separate evidence sourcing |
| Liquidity Threshold Calibration | Q6 numeric thresholds — requires index construction methodology sourcing |

---

## 9. Canonical Artifact Map

| Artifact | Description |
|----------|-------------|
| `requirements.md` | Q1–Q10 decisions, source authority hierarchy, field classifications, SAI compatibility, governance rules |
| `design.md` | Methodology chain, three-layer architecture, full field taxonomy, decision rationale, prohibitions |
| `tasks.md` | 12 documentation and verification tasks — no implementation tasks |
| `artifacts/decision_intake_review_*` | Q1–Q10 formal CTO decision intake |
| `artifacts/source_authority_verification_*` | Evidence citation traceability |
| `artifacts/field_taxonomy_reference_*` | Complete field catalog by scope |
| `artifacts/etf_fund_peer_rule_specification_*` | PGF-09 specification |
| `artifacts/cross_region_comparability_specification_*` | GAAP/IFRS/taxonomy/currency rules |
| `artifacts/governance_versioning_specification_*` | Review cycle and versioning mechanics |
| `artifacts/market_data_readiness_specification_*` | Current vs. future market data fields |
| `artifacts/trading_governance_boundary_*` | FUTURE_COMPLIANCE_REFERENCE vocabulary |
| `artifacts/unsupported_asset_class_handling_*` | Rules for assets outside v0 scope |
| `artifacts/sai_compatibility_verification_*` | SAI interface contract satisfaction |
| `artifacts/gate_vg_pgmf_1.md` | Verification gate |

---

## 10. Final Status

```
PEER_GROUP_REGISTRY_METHODOLOGY_FRAMEWORK_SPEC_READY_FOR_HUMAN_REVIEW
```

Recommended next step: Human review of Q1–Q10 decisions in `artifacts/decision_intake_review_2026-06-08.md`, CTO confirmation or override, then Peer Group Registry creation preflight.

---

*End of README.*
