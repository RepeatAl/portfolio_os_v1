# README: Layer Separation and Boundary Specification

> **Artifact**: `layer_separation_boundary_specification.md`
> **Spec**: peer-group-production-registry-creation | **Task**: 3
> **Purpose**: Prevent drift on registry scope for humans and future AI agents

---

## What This Artifact Defines

The Layer Separation and Boundary Specification defines:

1. The 10 architectural layers in Portfolio OS and their ownership boundaries
2. What the Peer Group Production Registry owns vs. what belongs to other layers
3. Prohibited cross-layer behaviors (24 explicit prohibitions)
4. Registry schema boundaries (what it contains vs. excludes)
5. Correlation Calculation Prohibition Table (12 prohibited calculations)
6. Dependency Boundary Table (allowed vs. prohibited dependency behaviors)
7. No-Authority-Simulation rules

---

## What This Artifact Does NOT Do

- Does NOT create registry content or peer_group_registry.yaml
- Does NOT implement any calculations, algorithms, or runtime logic
- Does NOT execute verification gates or approval gates
- Does NOT activate any downstream system
- Does NOT modify SAI, portfolio state, or any other Portfolio OS layer

---

## Why the Registry Must NOT Calculate Correlations, Scores, or Portfolio Health

The Peer Group Production Registry is a **structural intelligence layer**. Its purpose is to document peer comparability relationships, family membership, and structural context. It answers the question: "What structural relationships exist between assets and peer groups?"

It does NOT answer: "How correlated are these assets?" or "Is this portfolio healthy?" or "Which asset is the best opportunity?"

### The distinction:

| Registry provides (structural context) | Downstream calculates (quantitative output) |
|----------------------------------------|---------------------------------------------|
| "AVGO has a supply_chain_dependency on AI accelerator demand" | "AVGO-NVDA rolling correlation = 0.68" |
| "MELI carries a LatAm regional_context caveat" | "MELI beta to EM index = 1.4" |
| "GEV has a structural_break_caveat (spin-off from GE)" | "GEV portfolio concentration contribution = 3.2%" |
| "UBER is in PGF-04 Mobility primary subcluster" | "UBER opportunity score = 7.2/10" |

The registry provides the **facts about structure**. Downstream systems provide the **quantitative meaning** of that structure.

### Why this matters:

1. **Ownership clarity**: If the registry calculates correlations, it becomes unclear whether the Correlation/Dependency Engine or the registry owns that calculation. Ownership confusion leads to conflicting outputs.

2. **Governance isolation**: Each downstream system has its own governance rules. The Scoring Methodology has rules about how scores are produced. The Portfolio Health Framework has rules about concentration thresholds. The registry must not bypass those governance boundaries.

3. **No authority simulation**: If the registry produces scores or health metrics, it could be misinterpreted as making investment recommendations. A registry that says "concentration_risk_elevated" is simulating authority that belongs to the Portfolio Health Framework.

4. **Principle preservation**: "Signals decide, AI interprets, Human decides." The registry provides structure. Signals and engines decide what that structure means quantitatively. Humans decide what to do about it.

---

## The Difference Between Providing Structural Context and Performing Reasoning

### Structural context (what the registry does):
- Documents that a relationship of type X exists between entities A and B
- Records the source authority for that relationship claim
- Preserves evidence status (VERIFIED, INFERRED, CONTEXT_ONLY)
- Provides graph-readable structure that downstream systems can traverse

### Reasoning (what the registry must NEVER do):
- Deriving quantitative conclusions from structural relationships
- Activating semantic states (dependency_elevated, concentration_risk_elevated)
- Producing scores, rankings, or opportunity prioritization
- Generating narrative explanations or PM interpretations
- Inferring trading signals from structural patterns
- Concluding portfolio health status from dependency density

The boundary is: **documentation vs. derivation**. The registry documents. It never derives.

---

## Each Downstream System Owns Its Own Calculations

| System | Owns These Calculations | Registry Provides |
|--------|------------------------|-------------------|
| Correlation/Dependency Engine | Statistical correlations, beta, factor exposure | Structural relationship context |
| Signal Engines | Rolling correlations, momentum, regime detection | Does not consume registry directly |
| Portfolio Health | Concentration, health metrics, dependency density impact | Dependency structure, peer density context |
| Semantic Reasoning | Semantic conclusions, meaning derivation, state activation | Structural fields, dependency types |
| Scoring Methodology | Asset scores, opportunity rankings | Peer context, family membership |
| PM Reasoning | Investment interpretation, thesis evaluation | Peer context for explanation framing |
| Action Space | Action generation, buy/sell/size framing | Structural boundaries, comparability context |
| Report Rendering | Localized text, dashboard output, visualizations | Canonical structural tokens |

No downstream system may attribute its calculations to the registry. Each system is responsible for its own governance, its own accuracy, and its own outputs.

---

## Preventing Agent Drift on Registry Scope

### For AI agents consuming or extending this spec:

1. **Never add calculations to the registry**. If you find yourself computing a statistical measure, you are in the wrong layer.

2. **Never activate semantic states from registry data**. States like `dependency_elevated` or `ai_dependency_high` belong to the Semantic Reasoning layer.

3. **Never produce scores or rankings**. If output looks like "Asset X ranks #3 in PGF-01", you are violating the boundary.

4. **Never generate recommendations**. The registry is not an investment advisor. It provides structure for systems that humans use to make decisions.

5. **Never write back from downstream**. If a downstream system wants to update registry content, that requires separate governance and approval.

6. **Check the Verification Gate**. Checks M, N, O, and P validate that no prohibited output has leaked into registry artifacts.

### Decision tree for boundary questions:

```
Is this a structural fact about a relationship?
  YES → Belongs in registry
  NO  → Does it require market data or time-series?
          YES → Belongs to Signal/Correlation engines
          NO  → Does it produce a score, rank, or recommendation?
                  YES → Belongs to Scoring/Opportunity/Action layers
                  NO  → Does it interpret meaning or activate state?
                          YES → Belongs to Semantic layer
                          NO  → Ask CTO for guidance
```

---

## Controlling Sources

- design.md Section 5 (Layer Separation Diagram)
- design.md Section 6 (Registry Schema Boundaries)
- design.md Section 15 (Dependency Boundary Table)
- design.md Section 16 (Correlation Calculation Prohibition Table)
- design.md Section 25 (No-Authority-Simulation)
- requirements.md R13 (Output Restrictions)
- requirements.md R17 (Trading and Market Data Boundary)
- requirements.md R27 (Portfolio OS Scope Preservation)
- requirements.md R28 (Registry Layer Separation)
- requirements.md R29 (No Authority Simulation)

---

## Boundary Confirmations

- ✓ This README explains why the registry must not calculate correlations, scores, or portfolio health
- ✓ This README explains the difference between providing structural context and performing reasoning
- ✓ This README states that each downstream system owns its own calculations
- ✓ This README prevents agent drift on registry scope
- ✓ No calculations implemented
- ✓ No registry content created
- ✓ Documentation only

---

*End of README.*
