# Owner-Verified P2 Decision Record — Peer Group Registry Preflight

> **Scope**: Owner-verified P2 peer role decision record
> **production_authority**: NONE
> **registry_creation_authority**: NONE
> **candidate_approval_authority**: NONE
> **decision_authority**: OWNER_VERIFIED_REVIEW_DECISION
> **Status**: P2_OWNER_VERIFIED_DECISION_RECORD_READY

---

## Purpose

This document records owner-verified P2 peer role decisions for six unresolved peer-role context observations identified during the completed Peer Group Registry Creation Preflight.

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

1. **MoneyHorst scope alignment** — classifying peer-role fit for portfolio intelligence and decision governance
2. **Institutional peer-group comparability** — which assets are genuinely comparable for investment analysis
3. **Peer-role discipline** — correct use of core_peer, adjacent_peer, benchmark_context, and dependency_context
4. **Avoidance of narrative-driven misclassification** — not forcing peer roles based on headlines or market narratives
5. **Separation of core_peer, adjacent_peer, benchmark_context, and dependency_context** — each role has distinct analytical meaning
6. **Production-readiness discipline** — ensuring decisions are structurally sound before production use
7. **MoneyHorst taxonomy distinction** between asset class, instrument, investment style, factor, method, asset allocation, strategy, and system layer

MoneyHorst is not deciding based on whether an asset is "Growth", "Value", "Quant", or simply a "stock". MoneyHorst is classifying peer-role fit for future portfolio intelligence and decision governance.

**Reference**: `docs/moneyhorst/investment_style_method_taxonomy_ssot.md`

---

## P2 Decision Summary Table

| Gap ID | Asset | Owner-Verified Decision | Status | Production Spec Effect |
|--------|-------|------------------------|--------|------------------------|
| CTX-GAP-003 | ARM | Role = adjacent_peer in PGF-01; not core_peer because IP licensing model differs from semiconductor manufacturers | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model ARM as PGF-01 adjacent_peer with explicit business-model caveat |
| CTX-GAP-006 | DDOG | Role = adjacent_peer in PGF-02; observability platform with security overlay, not pure cybersecurity core peer | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model DDOG as PGF-02 adjacent_peer |
| CTX-GAP-007 | TENB | Role = benchmark_context in PGF-02; vulnerability-management specialist, not broad platform peer | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may use TENB as benchmark/context, not core peer |
| CTX-GAP-013 | BKNG | Role = benchmark_context in PGF-04; travel marketplace benchmark, not mobility/delivery peer | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may use BKNG as platform/marketplace benchmark context |
| CTX-GAP-016 | AXON | Role = adjacent_peer in PGF-06; public safety AI / law-enforcement technology, defense-adjacent but not traditional defense core | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model AXON as PGF-06 adjacent_peer with public-safety caveat |
| CTX-GAP-017 | GEV | Role = core_peer in PGF-07 with spin-off history condition | APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION | Future production spec may model GEV as PGF-07 core_peer but must preserve limited standalone-history caveat |

---

## Individual Decision Records

### CTX-GAP-003 — ARM

**Decision**: Role assignment: **adjacent_peer** in PGF-01.

**Peer handling**:
- ARM may remain in PGF-01 because it is structurally relevant to AI compute architecture.
- ARM should not be treated as a PGF-01 core peer to semiconductor manufacturers such as chip designers or producers.
- Its IP licensing model must be preserved as a comparability caveat.

**Rationale**: ARM is strategically relevant to AI infrastructure, but its licensing/IP model differs materially from semiconductor manufacturing, fabless chip design, and AI accelerator economics. For MoneyHorst, ARM is best treated as adjacent_peer rather than core_peer.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve business-model caveat.
- Future production spec must not compare ARM mechanically against chip manufacturers without peer-role adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-006 — DDOG

**Decision**: Role assignment: **adjacent_peer** in PGF-02.

**Peer handling**:
- DDOG may remain in PGF-02 because observability, cloud monitoring, and security monitoring overlap.
- DDOG should not be treated as a pure cybersecurity core peer.
- DDOG should be handled as observability platform with security overlay.

**Rationale**: Datadog has relevant security and cloud-monitoring exposure, but its core institutional comparability is observability/platform monitoring rather than pure cybersecurity. It belongs as adjacent_peer, not core_peer.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve observability-vs-security caveat.
- Future production spec must not treat DDOG as equivalent to CRWD, PANW, or ZS without role adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-007 — TENB

**Decision**: Role assignment: **benchmark_context** in PGF-02.

**Peer handling**:
- TENB may be used as a cybersecurity benchmark/context reference.
- TENB should not be promoted to core_peer.
- TENB should not be treated as broad cybersecurity platform peer unless future evidence supports broader platform comparability.

**Rationale**: Tenable is relevant to cybersecurity, but its vulnerability-management specialization makes it narrower than broad platform cybersecurity peers. For MoneyHorst, it is better as benchmark_context than adjacent_peer or core_peer.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve narrow-specialist caveat.
- TENB must not distort broader cybersecurity peer-group comparability.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-013 — BKNG

**Decision**: Role assignment: **benchmark_context** in PGF-04.

**Peer handling**:
- BKNG may be retained as marketplace/platform benchmark context.
- BKNG should not be treated as a mobility or delivery peer.
- BKNG may help compare marketplace economics, travel demand, consumer platform monetization, and cyclicality.

**Rationale**: Booking Holdings is a travel marketplace/platform business, not a ride-hailing, delivery, or mobility-logistics platform. It can be useful as benchmark_context but should not dilute the mobility peer group.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve travel-marketplace distinction.
- BKNG must not be classified as mobility core or adjacent peer unless a separate travel/platform family is scoped.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-016 — AXON

**Decision**: Role assignment: **adjacent_peer** in PGF-06.

**Peer handling**:
- AXON may remain related to PGF-06 because public safety, law enforcement, security technology, and AI-enabled evidence systems are defense-adjacent.
- AXON should not be treated as a traditional defense contractor core_peer.
- AXON should be modeled as public safety AI / security technology adjacent_peer.

**Rationale**: Axon is not a conventional defense prime, but it is strategically relevant to security, law enforcement, public safety, and AI-enabled evidence workflows. For MoneyHorst, it belongs as PGF-06 adjacent_peer with a public-safety caveat.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve law-enforcement/public-safety caveat.
- AXON must not be mechanically compared to defense primes without role adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-017 — GEV

**Decision**: Role assignment: **core_peer** in PGF-07 with spin-off history condition.

**Peer handling**:
- GEV may be treated as PGF-07 core_peer because power, grid, electrification, and energy-transition infrastructure are central to PGF-07.
- GEV's recent spin-off status must remain a comparability caveat.
- Standalone financial-history limits must be preserved in future production spec.

**Rationale**: GE Vernova is structurally central to power/grid/electrification infrastructure and therefore fits PGF-07 core_peer better than adjacent_peer. However, its limited standalone history after spin-off requires explicit caution.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION

**Conditions**:
- Future production spec must preserve spin-off history caveat.
- Future production spec must not overstate standalone historical comparability.
- Future production spec should track standalone data maturity over time.
- Final production registry still requires separate spec and gate.


---

## Production Registry Readiness Effect

| Item | Readiness Effect |
|------|-----------------|
| ARM | P2 resolved for future production-spec input as PGF-01 adjacent_peer |
| DDOG | P2 resolved for future production-spec input as PGF-02 adjacent_peer |
| TENB | P2 resolved for future production-spec input as PGF-02 benchmark_context |
| BKNG | P2 resolved for future production-spec input as PGF-04 benchmark_context |
| AXON | P2 resolved for future production-spec input as PGF-06 adjacent_peer |
| GEV | P2 resolved for future production-spec input as PGF-07 core_peer with spin-off-history condition |

---

## Remaining Review After P2

After this P2 record, the following review layers remain:

**P3 Subcluster Assignment Decisions**:
- AVGO
- MU
- AXP
- UBER
- AMZN

**P4 Regional / Structural Observations**:
- MELI
- STNE
- GRAB
- UBS
- PGF-09 ETF membership population

This artifact does not execute P3/P4 decisions.

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
- ✓ No new spec started
- ✓ Documentation-only guidance

---

```
P2_OWNER_VERIFIED_DECISION_RECORD_READY
```

---

*End of Owner-Verified P2 Decision Record.*
