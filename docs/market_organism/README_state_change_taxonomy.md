# State Change Taxonomy

---
artifact_id: state_change_taxonomy_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines the formal taxonomy of all state change types in the Market Organism
ssot_relationship: canonical
topic: state_change_taxonomy
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_principles_md, shared_glossary_reference_md]
---

## Scope Statement

This document defines the formal taxonomy of all State_Change types in the Market Organism Framework. It classifies every market impulse by its nature and originating causal mechanism before any asset association occurs. The taxonomy establishes exactly four top-level categories (Macro, Corporate, Narrative, Events), their sub-categories, and the mandatory classification hierarchy that all downstream systems must follow. This document does NOT contain engines, code, scores, weights, probabilities, asset lists, correlation matrices, dashboards, or any executable logic.

---

## Glossary Reference

All terms used in this document are defined in the canonical glossary:
→ `.kiro/specs/market-organism-framework/requirements.md`, Section: Glossary

This document does not define terms. It consumes them.

---

## Classification Hierarchy

Every State_Change classification follows this mandatory hierarchy. The ordering is inviolable — no step may be skipped, and no step may be reordered.

```
State_Change type → Expansion type → Affected systems → Affected narratives → Affected assets
```

**Interpretation:**

1. **State_Change type** — Classify the impulse by its originating causal mechanism (which top-level category and sub-category)
2. **Expansion type** — Determine how the impulse propagates (See: README_expansion_taxonomy, Section: Expansion Definition)
3. **Affected systems** — Identify which functional domains are affected at each Expansion_Order
4. **Affected narratives** — Identify which narrative containers carry the propagation
5. **Affected assets** — Only at the final step, identify which leaf-node assets are observable endpoints

Assets are always the LAST element in this hierarchy. They are never the starting point of classification.

(See: README_market_organism_principles, Section: Principle 2 — Taxonomy Precedes Assets)

---

## Top-Level Categories

The State_Change taxonomy contains exactly four top-level categories. Each represents a fundamentally distinct class of originating causal mechanism.

| # | Category | Canonical ID | Causal Domain |
|---|----------|-------------|---------------|
| 1 | Macro | `sc.macro` | Macroeconomic policy, conditions, and structural forces |
| 2 | Corporate | `sc.corporate` | Individual company actions, disclosures, and decisions |
| 3 | Narrative | `sc.narrative` | Thematic shifts in market belief systems and investment themes |
| 4 | Events | `sc.events` | Discrete external occurrences that alter market context |

---

## Category 1: Macro

**Canonical ID**: `sc.macro`

**Definition**: State_Changes originating from macroeconomic policy decisions, structural economic conditions, or systemic forces that affect broad market segments simultaneously. The causal mechanism operates at the level of economic systems rather than individual entities.

---

### Rates

**Canonical ID**: `sc.macro.rates`

**Scope**: State_Changes driven by shifts in interest rate policy, yield curve dynamics, or the cost of capital across the economy.

**Example**: Fed announces a 50bp emergency rate hike citing persistent inflation
  - Root_Node Type: Regime_Shift
  - Why it belongs: The causal mechanism is a central bank policy action that directly alters the cost of capital for all borrowers — this is a macroeconomic force operating at the system level, not a corporate or narrative event.

**Boundary (Does NOT Belong)**: A bank raises its mortgage rates by 25bp to protect margins
  - Why it doesn't belong: This is a corporate pricing decision (`sc.corporate`) driven by the bank's business strategy, not a macroeconomic policy shift. The bank is responding to macro conditions, but the impulse originates from a corporate decision.

---

### Inflation

**Canonical ID**: `sc.macro.inflation`

**Scope**: State_Changes driven by shifts in price level dynamics, purchasing power erosion, or inflation expectations that alter economic behavior across sectors.

**Example**: CPI prints at 9.1% year-over-year, the highest reading in 40 years
  - Root_Node Type: State_Change
  - Why it belongs: The causal mechanism is a measurable shift in economy-wide price dynamics that forces behavioral changes across all economic actors — consumers, corporations, and policymakers simultaneously.

**Boundary (Does NOT Belong)**: A semiconductor company raises chip prices by 15% due to supply constraints
  - Why it doesn't belong: This is a corporate pricing action (`sc.corporate`) or potentially a supply chain event. The price increase is localized to one company's products, not a systemic shift in economy-wide price levels.

---

### Oil

**Canonical ID**: `sc.macro.oil`

**Scope**: State_Changes driven by shifts in global energy supply, demand, or pricing that propagate through the economy as an input cost or geopolitical force.

**Example**: OPEC announces a 2 million barrel per day production cut effective immediately
  - Root_Node Type: Event
  - Why it belongs: The causal mechanism is a supply-side shock to a foundational economic input that propagates through transportation costs, manufacturing costs, and consumer prices across the entire economy.

**Boundary (Does NOT Belong)**: An oil company announces a new offshore drilling project
  - Why it doesn't belong: This is a corporate capital expenditure decision (`sc.corporate.capex`). While it relates to oil, the impulse originates from a single company's investment decision, not from a shift in global energy market dynamics.

---

### Liquidity

**Canonical ID**: `sc.macro.liquidity`

**Scope**: State_Changes driven by shifts in the availability of capital, credit conditions, or monetary base that alter the funding environment for all market participants.

**Example**: The Fed begins quantitative tightening, reducing its balance sheet by $95 billion per month
  - Root_Node Type: Regime_Shift
  - Why it belongs: The causal mechanism is a structural reduction in system-wide liquidity that affects all asset classes simultaneously by reducing the total pool of available capital in the financial system.

**Boundary (Does NOT Belong)**: A venture capital firm closes its latest fund at $2 billion
  - Why it doesn't belong: This is a corporate fundraising event. While it represents capital availability in one market segment, it does not alter system-wide liquidity conditions or the monetary base.

---

### FX

**Canonical ID**: `sc.macro.fx`

**Scope**: State_Changes driven by shifts in currency valuations, exchange rate regimes, or cross-border capital flow dynamics that alter relative economic competitiveness.

**Example**: The Bank of Japan abandons yield curve control, allowing the yen to strengthen rapidly
  - Root_Node Type: Regime_Shift
  - Why it belongs: The causal mechanism is a central bank policy shift that fundamentally alters the exchange rate regime, affecting all entities with cross-border exposure — exporters, importers, carry traders, and multinational corporations simultaneously.

**Boundary (Does NOT Belong)**: A US company reports a $200M FX translation loss in quarterly earnings
  - Why it doesn't belong: This is a corporate earnings impact (`sc.corporate.earnings`). The company is reporting the downstream effect of an FX shift on its financials — the impulse is the corporate disclosure, not the currency movement itself.

---

## Category 2: Corporate

**Canonical ID**: `sc.corporate`

**Definition**: State_Changes originating from individual company actions, disclosures, or strategic decisions that alter the market's understanding of that entity and propagate outward through Dependency_Paths to connected systems, narratives, and assets.

---

### Earnings

**Canonical ID**: `sc.corporate.earnings`

**Scope**: State_Changes driven by the disclosure of financial results that reveal a material shift in a company's operating performance relative to market expectations.

**Example**: Nvidia reports quarterly revenue of $26 billion, beating consensus estimates by 20%
  - Root_Node Type: State_Change
  - Why it belongs: The causal mechanism is a corporate disclosure that reveals a material gap between expected and actual performance, forcing the market to reprice not just the company but all entities connected through Dependency_Paths (suppliers, competitors, narrative members).

**Boundary (Does NOT Belong)**: An analyst upgrades a stock based on sector momentum
  - Why it doesn't belong: This is a narrative-driven opinion shift (`sc.narrative`), not a corporate disclosure. No new corporate information has been revealed — the analyst is interpreting existing conditions through a thematic lens.

---

### Guidance

**Canonical ID**: `sc.corporate.guidance`

**Scope**: State_Changes driven by forward-looking statements from corporate management that alter market expectations about future performance trajectories.

**Example**: Nvidia raises full-year revenue guidance by 40% citing unprecedented AI infrastructure demand
  - Root_Node Type: State_Change
  - Why it belongs: The causal mechanism is a corporate forward-looking disclosure that shifts the market's expectation of future earnings power — this propagates through the organism differently than a backward-looking earnings report because it resets the trajectory, not just the current state.

**Boundary (Does NOT Belong)**: A sell-side analyst raises their price target based on a new valuation model
  - Why it doesn't belong: This is an external opinion, not a corporate action. The company has not disclosed new information — an external party has reinterpreted existing information. The causal mechanism originates outside the corporation.

---

### Capex

**Canonical ID**: `sc.corporate.capex`

**Scope**: State_Changes driven by material shifts in corporate capital expenditure plans that signal strategic direction changes and propagate through supply chains and competitive dynamics.

**Example**: Microsoft announces $50 billion in AI data center capital expenditure for the fiscal year
  - Root_Node Type: State_Change
  - Why it belongs: The causal mechanism is a corporate capital allocation decision that signals strategic commitment and directly creates demand through supply chains — affecting semiconductor suppliers, construction firms, power utilities, and cooling system manufacturers through identifiable Dependency_Paths.

**Boundary (Does NOT Belong)**: A government announces a $100 billion infrastructure spending bill
  - Why it doesn't belong: This is a macroeconomic fiscal policy action (`sc.macro`) or an event (`sc.events.elections` if tied to political outcomes). The causal mechanism is governmental, not corporate — even though the downstream effects on construction companies may appear similar.

---

### M&A

**Canonical ID**: `sc.corporate.ma`

**Scope**: State_Changes driven by mergers, acquisitions, divestitures, or corporate restructuring actions that alter competitive landscapes and ownership structures.

**Example**: Broadcom announces a $69 billion acquisition of VMware
  - Root_Node Type: State_Change
  - Why it belongs: The causal mechanism is a corporate strategic action that immediately alters the competitive landscape, forces repricing of the target and acquirer, and propagates through the organism to competitors, customers, and suppliers of both entities.

**Boundary (Does NOT Belong)**: Rumors circulate on social media that a company might be acquired
  - Why it doesn't belong: This is a narrative shift (`sc.narrative`) driven by speculation, not a corporate action. No corporate decision has been made or disclosed — the impulse originates from market narrative dynamics, not from a corporate boardroom.

---

### Buybacks

**Canonical ID**: `sc.corporate.buybacks`

**Scope**: State_Changes driven by material share repurchase programs that signal management's capital allocation priorities and alter supply-demand dynamics for the company's equity.

**Example**: Apple announces a $110 billion share buyback authorization, the largest in corporate history
  - Root_Node Type: State_Change
  - Why it belongs: The causal mechanism is a corporate capital return decision that directly reduces share supply, signals management confidence in intrinsic value, and propagates through the organism by setting expectations for peer behavior and sector-wide capital return policies.

**Boundary (Does NOT Belong)**: A company's share price rises because passive index funds must buy more shares after a market cap increase
  - Why it doesn't belong: This is a flow-driven mechanical effect (a Dependency_Type of Flow), not a corporate decision. The company has not taken an action — the buying pressure originates from index rebalancing mechanics, not from corporate capital allocation strategy.

---

## Category 3: Narrative

**Canonical ID**: `sc.narrative`

**Definition**: State_Changes originating from thematic shifts in market belief systems, investment themes, or collective interpretive frameworks that alter how the market categorizes and values groups of assets. The causal mechanism operates at the level of shared market understanding rather than individual corporate actions or macroeconomic forces.

---

### AI

**Canonical ID**: `sc.narrative.ai`

**Scope**: State_Changes driven by shifts in the market's collective belief about the pace, scope, or economic impact of artificial intelligence adoption and infrastructure buildout.

**Example**: The release of a breakthrough AI model demonstrates capabilities previously thought to be years away, triggering a reassessment of AI infrastructure demand timelines
  - Root_Node Type: Impulse
  - Why it belongs: The causal mechanism is a shift in collective market belief about AI's trajectory — not a single company's earnings or a macroeconomic force, but a thematic reassessment that simultaneously affects all entities the market associates with the AI narrative.

**Boundary (Does NOT Belong)**: Nvidia reports record data center revenue driven by AI chip demand
  - Why it doesn't belong: This is a corporate earnings disclosure (`sc.corporate.earnings`). While it relates to AI, the impulse originates from a specific company's financial results, not from a shift in the broader market narrative about AI's trajectory.

---

### Security

**Canonical ID**: `sc.narrative.security`

**Scope**: State_Changes driven by shifts in the market's collective belief about cybersecurity threats, defense requirements, or the economic value of security infrastructure.

**Example**: A major nation-state cyberattack on critical infrastructure triggers a market-wide reassessment of cybersecurity spending requirements
  - Root_Node Type: Impulse
  - Why it belongs: The causal mechanism is a shift in collective market belief about the necessity and urgency of security spending — the attack itself is the trigger, but the State_Change is the narrative shift that reprices all entities associated with the security theme.

**Boundary (Does NOT Belong)**: A cybersecurity company reports a 40% increase in annual recurring revenue
  - Why it doesn't belong: This is a corporate earnings disclosure (`sc.corporate.earnings`). The company is reporting its own financial performance, not triggering a market-wide reassessment of the security narrative.

---

### Defense

**Canonical ID**: `sc.narrative.defense`

**Scope**: State_Changes driven by shifts in the market's collective belief about geopolitical threat levels, defense spending trajectories, or the strategic importance of military-industrial capabilities.

**Example**: NATO members collectively commit to raising defense spending to 3% of GDP following a geopolitical escalation
  - Root_Node Type: Regime_Shift
  - Why it belongs: The causal mechanism is a structural shift in the market's belief about long-term defense spending trajectories — this reprices all entities associated with the defense narrative simultaneously, not through individual corporate actions but through a thematic reassessment.

**Boundary (Does NOT Belong)**: A defense contractor wins a $10 billion government contract
  - Why it doesn't belong: This is a corporate event that affects one company's revenue outlook (`sc.corporate.earnings` or `sc.corporate.guidance`). While it relates to defense, the impulse is a specific contract award, not a shift in the broader market narrative about defense spending.

---

### Robotics

**Canonical ID**: `sc.narrative.robotics`

**Scope**: State_Changes driven by shifts in the market's collective belief about the timeline, feasibility, or economic impact of physical automation and robotic systems deployment.

**Example**: Multiple companies simultaneously demonstrate humanoid robots performing complex manufacturing tasks, triggering a reassessment of automation timelines
  - Root_Node Type: Impulse
  - Why it belongs: The causal mechanism is a shift in collective market belief about when robotics will achieve economic viability at scale — this reprices all entities associated with the robotics narrative (component suppliers, integrators, labor-intensive industries) through a thematic reassessment.

**Boundary (Does NOT Belong)**: A robotics company announces a $500 million factory to manufacture its robots
  - Why it doesn't belong: This is a corporate capital expenditure decision (`sc.corporate.capex`). The company is making a specific investment decision, not triggering a market-wide reassessment of the robotics narrative.

---

### Energy

**Canonical ID**: `sc.narrative.energy`

**Scope**: State_Changes driven by shifts in the market's collective belief about energy transition timelines, clean energy economics, or the structural transformation of energy systems.

**Example**: A major economy announces that renewable energy has achieved grid parity without subsidies, triggering a reassessment of fossil fuel demand trajectories
  - Root_Node Type: Impulse
  - Why it belongs: The causal mechanism is a shift in collective market belief about the pace of energy transition — this reprices all entities associated with both legacy energy and clean energy narratives simultaneously through a thematic reassessment of long-term energy economics.

**Boundary (Does NOT Belong)**: An oil shock caused by OPEC production cuts
  - Why it doesn't belong: This is a macroeconomic supply-side event (`sc.macro.oil`). The causal mechanism is a physical supply constraint, not a shift in market belief about energy transition. Oil prices can spike without any change in the energy transition narrative.

---

## Category 4: Events

**Canonical ID**: `sc.events`

**Definition**: State_Changes originating from discrete external occurrences — political, geopolitical, natural, or social — that alter the market context abruptly. The causal mechanism is an identifiable occurrence in the world that forces market participants to reassess conditions, distinct from ongoing macroeconomic forces, corporate actions, or gradual narrative shifts.

---

### Elections

**Canonical ID**: `sc.events.elections`

**Scope**: State_Changes driven by political elections, referendums, or transfers of power that alter the policy environment, regulatory outlook, or fiscal trajectory for market participants.

**Example**: A presidential election produces a surprise result with a candidate whose platform includes significant tariff increases on major trading partners
  - Root_Node Type: Event
  - Why it belongs: The causal mechanism is a discrete political occurrence that immediately alters the expected policy environment — trade policy, fiscal policy, regulatory approach — forcing all market participants to reassess their operating context simultaneously.

**Boundary (Does NOT Belong)**: A government passes a new regulation requiring higher capital reserves for banks
  - Why it doesn't belong: This is a regulatory action that belongs under `sc.macro` (if it alters system-wide conditions) or may be a Dependency_Type of Regulatory in the propagation model. The impulse is a policy implementation, not an election event.

---

### Wars

**Canonical ID**: `sc.events.wars`

**Scope**: State_Changes driven by the outbreak, escalation, or resolution of armed conflicts that disrupt supply chains, alter geopolitical alignments, or force structural reallocation of capital.

**Example**: A major military conflict erupts between two nations that control critical shipping lanes, disrupting 30% of global container traffic
  - Root_Node Type: Event
  - Why it belongs: The causal mechanism is a discrete geopolitical occurrence that immediately disrupts physical supply chains, forces capital reallocation toward defense and away from affected trade routes, and alters risk premiums across all entities with exposure to the affected region.

**Boundary (Does NOT Belong)**: Defense spending increases gradually over three years in response to rising geopolitical tensions
  - Why it doesn't belong: This is a narrative shift (`sc.narrative.defense`) driven by evolving market beliefs about threat levels. The gradual spending increase reflects a changing narrative, not a discrete event. There is no single identifiable occurrence that triggered the change.

---

### Pandemics

**Canonical ID**: `sc.events.pandemics`

**Scope**: State_Changes driven by the emergence, escalation, or resolution of widespread health crises that force behavioral changes, supply chain disruptions, or policy responses across the global economy.

**Example**: The World Health Organization declares a novel respiratory virus a global pandemic, triggering simultaneous lockdown announcements across major economies
  - Root_Node Type: Event
  - Why it belongs: The causal mechanism is a discrete health crisis occurrence that forces immediate behavioral and policy changes across the entire global economy — travel cessation, supply chain disruption, fiscal stimulus, and demand destruction happen simultaneously through identifiable causal channels.

**Boundary (Does NOT Belong)**: A pharmaceutical company announces positive Phase 3 trial results for a new vaccine
  - Why it doesn't belong: This is a corporate disclosure (`sc.corporate.guidance` or `sc.corporate.earnings` depending on context). The impulse originates from a single company's clinical development program, not from the pandemic event itself.

---

### Sporting_Events

**Canonical ID**: `sc.events.sporting_events`

**Scope**: State_Changes driven by major international sporting events that create concentrated economic activity, infrastructure investment, and temporary demand shifts in host regions and associated industries.

**Example**: The FIFA World Cup begins in a host nation, triggering a concentrated surge in tourism, media spending, and consumer discretionary activity across the host economy
  - Root_Node Type: Event
  - Why it belongs: The causal mechanism is a discrete, time-bounded occurrence that creates concentrated economic activity — media rights spending, tourism flows, infrastructure utilization, and consumer behavior shifts — all traceable to the event's occurrence rather than to any corporate decision or macroeconomic force.

**Boundary (Does NOT Belong)**: A sports media company reports record subscriber growth driven by exclusive content deals
  - Why it doesn't belong: This is a corporate earnings disclosure (`sc.corporate.earnings`). The company is reporting its own financial performance, which may have been influenced by sporting events but originates as a corporate disclosure, not as the sporting event itself.

---

## Satisfies (Task 2.1)

This section of the document satisfies the following requirements:

| Requirement | How Satisfied |
|-------------|---------------|
| 1.1 | Top-Level Categories section defines exactly four categories: Macro, Corporate, Narrative, Events |
| 1.2 | Category 1: Macro defines sub-categories: Rates, Inflation, Oil, Liquidity, FX |
| 1.3 | Category 2: Corporate defines sub-categories: Earnings, Guidance, Capex, M&A, Buybacks |
| 1.4 | Category 3: Narrative defines sub-categories: AI, Security, Defense, Robotics, Energy |
| 1.5 | Category 4: Events defines sub-categories: Elections, Wars, Pandemics, Sporting_Events |
| 1.6 | Every sub-category includes: (a) one-sentence scope, (b) concrete example with Root_Node type, (c) boundary counter-example with explanation |
| 1.7 | Classification Hierarchy section defines the mandatory ordering: State_Change type → Expansion type → Affected systems → Affected narratives → Affected assets |

---

## Primary Classification Rule

**Canonical ID**: `sc.rule.primary_classification`

When a State_Change could plausibly be classified under more than one top-level category, the following rule applies:

> **Assign the State_Change to the category whose originating causal mechanism produced the impulse.**

The classification question is always: "Where did this impulse originate?" — not "What systems does it affect?" or "Which assets moved?"

### Application Procedure

1. Identify the **originating causal mechanism** — the specific force, decision, or occurrence that initiated the state change
2. Determine which top-level category owns that causal mechanism
3. Assign the State_Change to that category regardless of downstream effects

### Disambiguation Examples

| State_Change | Appears to Span | Originating Causal Mechanism | Correct Classification |
|-------------|-----------------|------------------------------|----------------------|
| OPEC cuts production, triggering inflation fears | Macro (Oil) + Macro (Inflation) | Supply-side decision by oil cartel | `sc.macro.oil` |
| AI narrative shift causes Nvidia earnings beat expectations | Narrative (AI) + Corporate (Earnings) | Corporate financial disclosure | `sc.corporate.earnings` |
| Election result triggers defense spending narrative | Events (Elections) + Narrative (Defense) | Discrete political occurrence | `sc.events.elections` |
| Fed rate hike strengthens dollar | Macro (Rates) + Macro (FX) | Central bank policy action on rates | `sc.macro.rates` |

### Rule Rationale

A single State_Change may propagate across multiple categories through Expansion_Orders and Dependency_Paths. The classification captures the **origin**, not the **destination**. Downstream effects are modeled through the Expansion_Taxonomy, not through multiple category assignments.

(See: README_expansion_taxonomy, Section: Expansion Definition)

---

## Extension Criteria

**Canonical ID**: `sc.rule.extension_criteria`

The State_Change_Taxonomy supports controlled growth through criteria-gated addition. New sub-categories may be added to any top-level category provided ALL of the following criteria are satisfied:

### Mandatory Requirements for a New Sub-Category

| # | Criterion | Purpose |
|---|-----------|---------|
| 1 | **Distinct Causal Mechanism** | The proposed sub-category must represent a causal mechanism that is fundamentally different from all existing sub-categories within the same top-level category. If the impulse could be classified under an existing sub-category, it does not warrant a new one. |
| 2 | **Scope Definition** | A one-sentence definition that precisely delineates what State_Changes belong to this sub-category and what does not. The scope must be narrow enough to be testable — given any candidate State_Change, the scope definition must produce a clear yes/no answer. |
| 3 | **Concrete Example** | At least one real-world State_Change that belongs to the proposed sub-category, annotated with its Root_Node type and an explanation of why the causal mechanism places it here rather than in an existing sub-category. |
| 4 | **Boundary Counter-Example** | At least one State_Change that appears similar but belongs to a different sub-category, annotated with an explanation of the distinguishing causal mechanism. This proves the boundary is meaningful and non-arbitrary. |

### Extension Process

1. Propose the new sub-category with all four mandatory elements
2. Verify the causal mechanism is not already covered by an existing sub-category
3. Verify the boundary counter-example demonstrates a real distinction (not a trivial relabeling)
4. Assign a stable canonical ID following the namespace convention: `sc.<category>.<sub_category>`
5. Add the entry to the taxonomy in the same format as existing sub-categories

### Extension Prohibitions

- A new sub-category MUST NOT be created solely because a new asset class emerged (assets are leaf nodes, not classification anchors)
- A new sub-category MUST NOT duplicate the causal mechanism of an existing sub-category with different terminology
- A new sub-category MUST NOT be created to accommodate a single historical event that will not recur as a category

### Top-Level Category Extension

Adding a fifth top-level category requires extraordinary justification:
- Evidence that the proposed category represents a causal domain fundamentally distinct from Macro, Corporate, Narrative, and Events
- Demonstration that no combination of existing categories can accommodate the impulses in question
- Complete sub-category structure with at minimum two sub-categories, each satisfying all four criteria above

---

## Root Node Invariant

**Canonical ID**: `sc.invariant.root_node`

The Root Node Invariant is the foundational constraint that ensures the Market Organism always reasons from causes to effects — never from tickers to interpretations. This invariant is inviolable across all deliverables.

### Definition

A Root_Node is the origin point of a Cascade in the Organism_Graph. Root_Nodes are exclusively one of:

| Valid Root_Node Type | Definition |
|---------------------|-----------|
| State_Change | A discrete shift in market conditions that initiates propagation |
| Event | A discrete external occurrence that alters market context |
| Impulse | The initial force that triggers a State_Change |
| Regime_Shift | A fundamental change in the prevailing market structure or policy environment that redefines the operating context for multiple systems simultaneously |

Individual assets, tickers, securities, or asset class names are **permanently prohibited** from serving as Root_Nodes.

### Valid Root Nodes

| Example | Root_Node Type | Classification Question |
|---------|---------------|------------------------|
| Fed Hawkish Shift | Regime_Shift | "What kind of state change occurred?" |
| Nvidia Guidance Raise | State_Change | "What kind of state change occurred?" |
| Oil Shock | Event | "What kind of state change occurred?" |
| World Cup Start | Event | "What kind of state change occurred?" |

### Invalid Root Nodes (Invariant Violations)

| Example | Why Invalid | Required Reformulation |
|---------|-------------|----------------------|
| "NVDA" | Names a financial instrument without specifying what changed | "Nvidia Guidance Raise" |
| "Gold" | Names an asset class without specifying what changed | "Gold Safe Haven Demand Spike" |
| "SPY" | Names an ETF ticker without specifying what changed | "S&P 500 Regime Break Below Support" |
| "US Treasuries" | Names an asset class without specifying what changed | "Treasury Yield Curve Inversion" |

### Disambiguation Rule

A candidate Root_Node is valid **ONLY IF** it describes an observable shift in conditions or context.

A candidate Root_Node is **INVALID IF** it names a financial instrument without specifying what changed.

**Test**: Can you answer "What kind of state change occurred?" using only the Root_Node label? If yes, it is valid. If the answer requires knowing which asset moved, it is invalid and must be reformulated.

### Classification Question

**CORRECT**: "What kind of state change occurred?"

**PROHIBITED**: "How do I classify this asset?"

The correct question forces the analyst to identify the causal mechanism first. The prohibited question starts from the asset and works backward — this inverts the primitive chain and violates the taxonomy-before-assets principle.

(See: README_market_organism_principles, Section: Principle 2 — Taxonomy Precedes Assets)

### Reformulation Requirement

If a candidate Root_Node names a specific asset without describing a state change, it constitutes an invariant violation. The resolution is mandatory reformulation:

1. Identify what actually changed about the conditions surrounding that asset
2. Express the Root_Node as the underlying State_Change, Event, Impulse, or Regime_Shift
3. The asset becomes a downstream affected entity in the Expansion sequence — never the origin

**Example Reformulation**:
- INVALID: "Tesla" → VALID: "Tesla Autonomous Driving Regulatory Approval" (Event)
- INVALID: "Bitcoin" → VALID: "Bitcoin Spot ETF Approval" (Event)
- INVALID: "Oil" → VALID: "OPEC Emergency Production Cut" (Event)

---

## Exclusion Constraints

**Canonical ID**: `sc.constraints.exclusions`

This section consolidates all prohibitions that apply to this document. These constraints are non-negotiable and apply to all content within the State_Change_Taxonomy.

### Consolidated Prohibitions

| # | Prohibition | Rationale |
|---|-------------|-----------|
| 1 | **No engine implementations, Python code, or executable logic** | This is a definition document. Engines belong to future implementation phases. |
| 2 | **No scoring algorithms, numeric weights, probabilities, ranking systems, or quantitative models** | Weights on an incomplete model produce false confidence. Qualitative classification precedes quantification. |
| 3 | **No dashboard designs, report templates, or visualization specifications** | Presentation belongs to the REPORT domain, not to taxonomy definition. |
| 4 | **No asset lists, ticker symbols, or position sizing as root-level entities** | Assets are leaf nodes in the primitive chain. They appear only as illustrative examples within worked propagation scenarios, never as classification anchors or organizational structures. |
| 5 | **No correlation matrices or statistical co-movement measures** | Correlations are not causal mechanisms. This taxonomy defines causal classification, not statistical patterns. |

### Unified Rationale

All exclusions serve a single purpose: **weights on an incomplete model produce false confidence**. The definition layer must remain pure so that future implementation phases can build on a stable, uncontaminated conceptual foundation. Premature quantification creates the illusion of precision where only structural understanding exists.

### Permitted Content

For clarity, the following ARE permitted in this document:
- Qualitative descriptions of causal mechanisms
- Concrete examples using real company names, events, and market scenarios (as illustrations, not as root entities)
- Canonical IDs for machine identity
- Cross-references to other deliverables
- Extension criteria and invariant definitions

---

## Cross-References

This document references and is referenced by the following deliverables in the Market Organism Framework:

### Outbound References (This Document → Other Deliverables)

| Reference | Target Deliverable | Target Section | Relationship |
|-----------|--------------------|----------------|-------------|
| Expansion propagation model | README_expansion_taxonomy | Expansion Definition | State_Changes classified here propagate through Expansion_Orders defined there |
| Expansion_Order assignment | README_expansion_taxonomy | 1st Order through 4th Order | Each classified State_Change enters the expansion sequence at 1st Order |
| Dependency mechanisms | README_dependency_types_v2 | Type Enumeration | Propagation from classified State_Changes uses Dependency_Types defined there |
| Temporal properties | README_temporal_taxonomy | Latency Definition | Each propagation hop from a classified State_Change carries temporal properties defined there |
| Governing principles | README_market_organism_principles | Principle 2 — Taxonomy Precedes Assets | The classification hierarchy in this document implements Principle 2 |
| Organism constraints | README_market_organism_principles | Principle 1 — Organism over Collection | The Root Node Invariant enforces Principle 1 |

### Inbound References (Other Deliverables → This Document)

| Source Deliverable | Source Section | Relationship |
|--------------------|----------------|-------------|
| README_expansion_taxonomy | Worked Examples | Uses State_Change classifications from this document as Root_Nodes |
| README_dependency_types_v2 | Per-Type Examples | References State_Change categories as source/target entities |
| README_temporal_taxonomy | Complete Temporal Example | Uses classified State_Changes as the originating Impulse |
| README_market_organism_principles | All Principles | Constrains the classification rules defined here |

### Cross-Reference Convention

All cross-references in this document follow the canonical format:

```
(See: [Deliverable_Name], Section: [Section_Title])
```

(See: README_shared_glossary_reference, Section: Cross-Reference Convention)

---

## Explanation Readiness

**Canonical ID**: `sc.meta.explanation_readiness`

Every entry in this taxonomy supports traversal through explanation levels with no dead ends. The explanation chain for any State_Change classification is:

```
Level 0 (Headline): "A [Root_Node_Type] occurred in [Category]"
Level 1 (Summary): "The [Sub-Category] state change was: [Example description]"
Level 2 (Mechanism): "This belongs to [Sub-Category] because the originating causal mechanism is [explanation]"
Level 3 (Boundary): "This does NOT belong to [Alternative] because [boundary explanation]"
Level 4 (Classification): "The Primary Classification Rule assigns it here because [originating mechanism rationale]"
Level 5 (Root): "The Root Node is valid because it describes [observable shift], not an asset name"
```

### Traversal Guarantees

- **No dead ends**: Every sub-category has both a positive example (why it belongs) and a boundary counter-example (why alternatives don't apply), ensuring explanation can always proceed to the next level
- **Bidirectional navigation**: From any sub-category, the analyst can traverse UP to the top-level category (via causal domain) or DOWN to specific examples (via concrete instances)
- **Cross-deliverable continuity**: From the classification level, explanation continues into the Expansion_Taxonomy (how it propagates) and Dependency_Types_v2 (through what mechanisms)

(See: README_expansion_taxonomy, Section: Expansion Definition)
(See: README_dependency_types_v2, Section: Type Enumeration)

---

## Satisfies (Task 2.2)

This section of the document satisfies the following requirements:

| Requirement | How Satisfied |
|-------------|---------------|
| 1.8 | Primary Classification Rule assigns exactly one primary category based on originating causal mechanism |
| 1.9 | Extension Criteria defines the four mandatory requirements for new sub-category inclusion |
| 2.1 | Root Node Invariant defines Root_Nodes as exclusively State_Changes, Events, Impulses, or Regime_Shifts |
| 2.2 | Root Node Invariant explicitly prohibits individual assets, tickers, or securities as Root_Nodes |
| 2.3 | Valid Root Nodes table provides 4 examples: Fed Hawkish Shift, Nvidia Guidance Raise, Oil Shock, World Cup Start |
| 2.4 | Invalid Root Nodes table provides examples of ticker symbols and asset names with explanations |
| 2.5 | Classification Question defines correct ("What kind of state change occurred?") and prohibited ("How do I classify this asset?") |
| 2.6 | Disambiguation Rule states validity requires describing an observable shift, invalidity means naming an instrument without specifying what changed |
| 2.7 | Reformulation Requirement mandates that invalid Root_Nodes be reformulated as the underlying State_Change |
| 8.7 | Exclusion Constraints section consolidates all prohibitions in one reviewable location |
| 10.8 | Cross-References section provides explicit references to Expansion_Taxonomy and Dependency_Types_v2 using canonical convention |
