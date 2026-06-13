# Owner-Verified P1 Decision Record — Peer Group Registry Preflight

> **Scope**: Owner-verified P1 decision record
> **production_authority**: NONE
> **registry_creation_authority**: NONE
> **candidate_approval_authority**: NONE
> **decision_authority**: OWNER_VERIFIED_REVIEW_DECISION
> **Status**: P1_OWNER_VERIFIED_DECISION_RECORD_READY

---

## Purpose

This document records owner-verified P1 decisions for the three highest-priority peer group family assignment conflicts identified during the completed Peer Group Registry Creation Preflight.

These are owner-verified review decisions for future spec input. They:

- Do **not** create production registry authority
- Do **not** approve candidates
- Do **not** create final production peer assignments
- Do **not** mint canonical peer_group_id values
- Do **not** mutate SAI
- Do **not** start Production Registry Creation Spec

---

## Decision Basis

Decisions are based on:

1. **MoneyHorst scope alignment** — classifying peer-group fit for portfolio intelligence and decision governance
2. **Institutional peer-group comparability** — which assets are genuinely comparable for investment analysis
3. **Avoidance of narrative-driven misclassification** — not forcing assets into families based on marketing narratives
4. **Production-readiness discipline** — ensuring decisions are structurally sound before production use
5. **Separation of primary peer family from adjacent/dependency context** — one primary family, with context references preserved
6. **MoneyHorst taxonomy distinction** between system layer, strategy, method, style, factor, and instrument

MoneyHorst is not deciding based on whether an asset is "Growth", "Value", "Quant", or simply a "stock". MoneyHorst is classifying peer-group fit for future portfolio intelligence and decision governance.

**Reference**: `docs/moneyhorst/investment_style_method_taxonomy_ssot.md`

---

## P1 Decision Summary Table

| Gap ID | Asset | Owner-Verified Decision | Status | Production Spec Effect |
|--------|-------|------------------------|--------|------------------------|
| CTX-GAP-004 | SMCI | Primary family = PGF-01 AI Infrastructure; PGF-07 may be retained as dependency/adjacent context | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model SMCI under PGF-01 with PGF-07 context |
| CTX-GAP-005 | NET | Primary family = PGF-02 Cybersecurity / Security Platform; PGF-01 may be retained as adjacent AI infrastructure context | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model NET under PGF-02 with PGF-01 context |
| CTX-GAP-015 | PLTR | Do not force final PGF-06 core classification; prepare separate PGF-10 AI Software / Decision Intelligence Platform scope or keep PLTR as context/benchmark until PGF-10 exists | DEFER_WITH_ARCHITECTURE_REQUIREMENT | Future production spec must not finalize PLTR as PGF-06 core without explicit PGF-10 decision or context-only treatment |

---

## Individual Decision Records

### CTX-GAP-004 — SMCI

**Decision**: Primary family assignment: **PGF-01 AI Infrastructure**.

**Peer handling**:
- Future production spec may treat SMCI as PGF-01 production input.
- PGF-07 may be retained as dependency_context or adjacent_context because power, cooling, and infrastructure dependency remain relevant.
- Do not dual-classify SMCI as two primary families.

**Rationale**: SMCI is most useful to MoneyHorst as an AI infrastructure exposure and AI server/infrastructure comparability case. Cooling/power relevance is real but should be modeled as dependency context, not as the primary peer family.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve PGF-07 dependency/adjacent context.
- Future production spec must avoid silent duplicate primary-family assignment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-005 — NET

**Decision**: Primary family assignment: **PGF-02 Cybersecurity / Security Platform**.

**Peer handling**:
- Future production spec may treat NET as PGF-02 production input.
- PGF-01 may be retained as adjacent_context because edge compute, network infrastructure, and AI inference relevance exist.
- Do not classify NET primarily as AI infrastructure unless future evidence shows AI infrastructure becomes the dominant comparison basis.

**Rationale**: Cloudflare's cleanest institutional peer frame is security/network/SaaS platform comparability. AI infrastructure relevance is important but currently better handled as adjacent context rather than primary family.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve PGF-01 adjacent context.
- Future production spec must not confuse security platform exposure with pure AI infrastructure exposure.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-015 — PLTR

**Decision**: Do not force PLTR into final PGF-06 core classification as the only production treatment.

**Preferred architecture**: Prepare a future PGF-10 AI Software / Decision Intelligence Platform family, or keep PLTR as context/benchmark until PGF-10 is explicitly scoped.

**Peer handling**:
- PLTR may remain related to PGF-06 because of government, defense, and security relevance.
- PLTR should not be finalized as a PGF-06 core peer without explicit human/CTO architecture approval.
- PLTR requires a separate software/AI platform comparability frame.

**Rationale**: Palantir is not cleanly comparable to traditional defense/security peers only. Its stronger MoneyHorst classification is AI/data/decision-intelligence software. Forcing PLTR into PGF-06 would create peer-group distortion and may hide the need for a separate software/AI platform family.

**Decision status**: DEFER_WITH_ARCHITECTURE_REQUIREMENT

**Conditions**:
- Future Production Registry Creation Spec must either:
  - introduce a PGF-10 AI Software / Decision Intelligence Platform scope, or
  - keep PLTR as context/benchmark rather than final PGF-06 core peer.
- PLTR must not be silently promoted to PGF-06 core peer.
- Final production registry still requires separate spec and gate.

---

## Production Registry Readiness Effect

| Item | Readiness Effect |
|------|-----------------|
| SMCI | P1 resolved for future production-spec input, with PGF-07 context condition |
| NET | P1 resolved for future production-spec input, with PGF-01 context condition |
| PLTR | P1 not production-final; architecture requirement created for PGF-10 or context-only handling |

---

## Remaining Review After P1

After this P1 record, **P2 Peer Role Decisions** remain:

- ARM
- DDOG
- TENB
- BKNG
- AXON
- GEV

P3 and P4 remain lower-priority review inputs.

This artifact does not execute P2/P3/P4 decisions.

---

## Explicit Non-Authorization

This document does **not** authorize:

- Production registry creation
- Canonical peer_group_id creation
- peer_group_registry.yaml creation
- Final peer assignments
- Candidate approval
- Candidate_Status mutation
- SAI usage
- Market data integration
- Trading or execution usage
- Production Registry Creation Spec start
- Automated candidate promotion

---

## Boundary Confirmations

- ✓ No production registry created
- ✓ No peer_group_registry.yaml created
- ✓ No canonical peer_group_id values minted
- ✓ No candidate records modified
- ✓ No Candidate_Status values changed
- ✓ No SAI mutation
- ✓ No runtime code created
- ✓ No validation code created
- ✓ No market data integration
- ✓ No trading or execution scope
- ✓ No production registry creation spec started
- ✓ Documentation-only guidance

---

```
P1_OWNER_VERIFIED_DECISION_RECORD_READY
```

---

*End of Owner-Verified P1 Decision Record.*
