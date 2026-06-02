---
artifact_id: language_rendering_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines language-neutrality as an architectural principle for all canonical primitives
ssot_relationship: canonical
topic: multilingual_rendering
allowed_writers: [ARCH, GOV]
allowed_readers: [ALL]
dependencies: [market_organism_framework, narrative_framework_md, user_intelligence_journey_framework_md]
---

# LANGUAGE RENDERING FRAMEWORK

Version: v1
Status: Canonical Architecture Principle
Position: Foundational constraint — applies to ALL canonical primitives before implementation

---

## WHY THIS DOCUMENT EXISTS

MoneyHorst is defining canonical primitives:
- State_Change
- Narrative
- System
- Asset
- Signal
- Semantic State
- Reasoning Object
- Intelligence Object

If these primitives are modeled with display text as identity,
every future language addition requires rebuilding the knowledge layer.

This is the single most expensive architectural mistake in internationalization.
It must be prevented NOW, before the first taxonomy entry is written.

---

## CORE PRINCIPLE

> **Language is a rendering layer, not a knowledge layer.**
> **Time is a rendering layer, not a knowledge layer.**

The organism is language-neutral AND timezone-neutral.
Languages are views. Local times are views.
There is exactly one truth.
There are many renderings of that truth.

---

## THE FIVE RULES

### Rule 1: Knowledge is Language-Neutral

Every canonical object in MoneyHorst exists as a stable, language-independent identity.
No canonical object uses display text as its primary identifier.

**Correct:**
```
state_change_id: hyperscaler_capex_increase
```

**Incorrect:**
```
state_change_id: "Hyperscaler erhöhen Capex"
state_change_id: "Hyperscalers increase capex"
```

The truth is `hyperscaler_capex_increase`.
"Hyperscaler erhöhen Capex" is a German rendering.
"Hyperscalers increase capex" is an English rendering.

---

### Rule 2: Every Canonical Object Requires a Stable ID

All primitives must carry a machine-readable, language-independent identifier:

| Primitive | ID Format | Example |
|-----------|-----------|---------|
| State_Change | `sc.[category].[subcategory].[instance]` | `sc.corporate.capex.hyperscaler_increase` |
| Narrative | `narrative.[name]` | `narrative.ai_infrastructure` |
| System | `system.[name]` | `system.datacenter_networking` |
| Dependency_Type | `dep.[type]` | `dep.supply_chain` |
| Expansion_Order | `order.[n]` | `order.2nd` |
| Temporal_Property | `temporal.[property]` | `temporal.latency` |
| Principle | `principle.[name]` | `principle.taxonomy_before_assets` |
| Signal | `signal.[category].[name]` | `signal.risk.concentration_score` |
| Semantic_State | `sem.[signal_id]` | `sem.ai_dependency_high` |

These IDs are:
- Immutable (never change once assigned)
- Language-independent (no natural language in the ID)
- Machine-readable (valid identifiers, no spaces, no special characters)
- Hierarchical (dot-separated namespace)

---

### Rule 3: Language is Rendering

Display text is produced by a rendering layer that maps stable IDs to localized strings:

```
Canonical Layer (language-neutral):
  narrative.ai_infrastructure
       |
       v
Rendering Layer (language-specific):
  DE: "KI-Infrastruktur"
  EN: "AI Infrastructure"
  FR: "Infrastructure IA"
  AR: "البنية التحتية للذكاء الاصطناعي"
```

The rendering layer is:
- Separate from the knowledge layer
- Additive (new languages don't change the canonical layer)
- Overridable (user preferences determine which rendering is shown)
- Fallback-capable (if a rendering is missing, show the canonical ID)

---

### Rule 4: Display Text is Never Identity

No system component may use display text to:
- Look up a canonical object
- Compare two objects for equality
- Store relationships between objects
- Reference an object in cross-references

**Correct:**
```yaml
narrative_id: narrative.ai_infrastructure
parent: narrative.ai_transformation
```

**Incorrect:**
```yaml
narrative_name: "AI Infrastructure"
parent: "AI Transformation"
```

If "AI Infrastructure" is renamed to "AI Compute Infrastructure" in English,
the canonical identity `narrative.ai_infrastructure` remains unchanged.
Only the rendering changes.

---

### Rule 5: Altitude and Language are Independent Dimensions

The Learning Journey defines altitude switching (beginner / intermediate / expert).
Language is a separate, orthogonal dimension.

The rendering matrix is:

```
Canonical Object: narrative.ai_infrastructure
  |
  |-- Language: DE
  |     |-- Altitude: Beginner -> "KI-Infrastruktur: Rechenzentren und Chips fuer kuenstliche Intelligenz"
  |     |-- Altitude: Intermediate -> "KI-Infrastruktur: Hyperscaler-Capex treibt Nachfrage nach GPU, Netzwerk, Kuehlung"
  |     +-- Altitude: Expert -> "KI-Infrastruktur: Capex-Zyklen der Hyperscaler als primaerer Nachfragetreiber..."
  |
  +-- Language: EN
        |-- Altitude: Beginner -> "AI Infrastructure: Data centers and chips for artificial intelligence"
        |-- Altitude: Intermediate -> "AI Infrastructure: Hyperscaler capex driving demand for GPU, networking, cooling"
        +-- Altitude: Expert -> "AI Infrastructure: Hyperscaler capex cycles as primary demand driver..."
```

Language and Altitude are:
- Independent (changing language does not change altitude)
- Combinatorial (every language x altitude combination is a valid rendering)
- Separately cacheable (language packs and altitude packs are independent)

---

## TEMPORAL RENDERING RULES

### Rule 6: Time is a Rendering Layer, Not a Knowledge Layer

All canonical temporal objects store UTC as truth.
Local time is rendered per user timezone.
No canonical object may use rendered local time as identity or truth.

**Correct:**
```yaml
occurred_at_utc: 2026-08-15T21:00:00Z
source_timezone: America/New_York
```

**Incorrect:**
```yaml
occurred_at: "Aug 15, 2026 5:00 PM ET"
occurred_at: "15.08.2026 23:00 Uhr"
```

The truth is `2026-08-15T21:00:00Z`.
"5:00 PM ET" is a New York rendering.
"23:00 Uhr" is a Munich rendering.

---

### Rule 7: Three Temporal Contexts

MoneyHorst operates with three distinct time contexts:

| Context | Definition | Example |
|---------|-----------|---------|
| Market Time | The timezone of the exchange where an event occurs | Xetra: Europe/Berlin, NYSE: America/New_York |
| Event Time | The UTC timestamp when a State_Change occurred | `2026-08-15T21:00:00Z` |
| User Time | The timezone where the user views the rendering | Europe/Berlin, Asia/Dubai, America/Toronto |

**Rules:**
- Event Time is always stored as UTC (canonical truth)
- Market Time is stored as IANA timezone identifier alongside the UTC timestamp (source context)
- User Time is never stored — it is applied at rendering time from user preferences

---

### Rule 8: Every Temporal Object Requires UTC + Source Timezone

All canonical objects with temporal properties must store:

```yaml
utc_timestamp: "2026-08-15T21:00:00Z"       # canonical truth
source_timezone: "America/New_York"           # IANA zone where event originated
temporal_context: "market" | "event" | "system"  # what kind of time this represents
```

**Examples:**

State_Change:
```yaml
state_change_id: sc.corporate.earnings.nvidia_raise
occurred_at_utc: 2026-08-15T21:00:00Z
source_timezone: America/New_York
temporal_context: market
```

Narrative birth:
```yaml
narrative_id: narrative.ai_infrastructure
birth_timestamp_utc: 2023-03-14T00:00:00Z
source_timezone: America/New_York
temporal_context: event
```

Signal generation:
```yaml
signal_id: signal.risk.concentration_score
generated_at_utc: 2026-05-31T06:00:00Z
source_timezone: UTC
temporal_context: system
```

---

### Rule 9: Propagation Latency References Market Time

When the Temporal_Taxonomy defines Latency (Day, Week, Month, Quarter, Year),
the reference frame is:

- For Macro State_Changes: calendar days from event UTC timestamp
- For Corporate State_Changes: trading days in the source market timezone
- For Narrative State_Changes: calendar days from event UTC timestamp
- For Event State_Changes: calendar days from event UTC timestamp

This distinction matters because "2 days after Nvidia earnings" means
2 NYSE trading days, not 2 calendar days.

The Temporal_Taxonomy must specify which reference frame applies per State_Change category.

---

### Rule 10: Rendering Pipeline Includes Timezone

The complete rendering pipeline is:

```
Canonical Intelligence Object
  (language-neutral, timezone-neutral, stable ID, single truth)
       |
       v
Language Renderer
  (maps ID to localized display text)
       |
       v
Altitude Renderer
  (selects explanation depth)
       |
       v
Temporal Renderer
  (converts UTC to user's local timezone + locale formatting)
       |
       v
Output Target
  (UI, Report, Dashboard, Briefing, API)
```

The four rendering dimensions are:
1. **Language** — which language to display
2. **Altitude** — which explanation depth
3. **Timezone** — which local time to show
4. **Locale** — which date/number formatting (DD.MM.YYYY vs. MM/DD/YYYY, comma vs. period for decimals)

---

## AFFECTED PRIMITIVES

Every canonical primitive in MoneyHorst must comply with these rules:

| Primitive | Current Risk | Required Action |
|-----------|-------------|-----------------|
| State_Change | Sub-category names are English text | Assign stable IDs, treat names as EN rendering |
| Narrative | Names like "AI Infrastructure" used as identity | Assign `narrative.*` IDs |
| System | Names like "Datacenter Networking" used as identity | Assign `system.*` IDs |
| Dependency_Type | Names like "Supply_Chain" already ID-like | Formalize as `dep.*` namespace |
| Temporal_Property | Enum values (Day, Week, etc.) are language-neutral | Already compliant |
| Amplification/Dampening | Enum values (None, Low, etc.) are English | Assign language-neutral codes or accept EN as canonical |
| Signal | `signal_id` field already exists | Already compliant |
| Semantic_State | `signal_id` field already exists | Already compliant |
| Principle | Named in English prose | Assign `principle.*` IDs |

---

## IMPLICATIONS FOR CURRENT SPEC

### State_Change_Taxonomy

When writing taxonomy entries, every sub-category must have:
```
id: sc.macro.rates
name_en: "Rates"
name_de: "Zinsen"
description_en: "..."
description_de: "..."
```

For the current phase (definition documents), English is the working language.
But the STRUCTURE must support future languages by using stable IDs as primary keys.

### Narrative Framework

The Narrative Registry (conceptual schema) must use:
```
narrative_id: narrative.ai_infrastructure  (stable, language-neutral)
display_name: {"en": "AI Infrastructure", "de": "KI-Infrastruktur"}  (rendering)
```

NOT:
```
name: "AI Infrastructure"  (display text as identity — VIOLATION)
```

### Expansion_Taxonomy Worked Examples

Worked examples may use English display text for readability.
But every entity referenced must have a stable ID noted:

```
1st Order: Nvidia (asset.nvidia), AMD (asset.amd)
  via: dep.supply_chain
  from: sc.corporate.capex.hyperscaler_increase
```

### Market_Organism_Principles

Principles are written in English (working language).
Each principle carries a stable ID for cross-referencing:

```
principle.taxonomy_before_assets
principle.all_propagation_temporal
principle.feedback_structural
```

---

## RENDERING ARCHITECTURE (Conceptual)

```
Canonical Intelligence Object
  (language-neutral, timezone-neutral, stable ID, single truth)
       |
       v
Language Renderer
  (maps ID to localized display text)
       |
       v
Altitude Renderer
  (selects explanation depth)
       |
       v
Temporal Renderer
  (converts UTC to user local timezone + locale formatting)
       |
       v
Output Target
  (UI, Report, Dashboard, Briefing, API)
```

The rendering pipeline applies four independent dimensions:
1. Resolve canonical object by stable ID
2. Select language (user preference or system default)
3. Select altitude (user profile or context)
4. Apply timezone (user timezone preference)
5. Apply locale formatting (date format, number format)
6. Produce display output for the target

---

## WHAT THIS DOES NOT REQUIRE (NOW)

- Translation files or language packs (future)
- Multi-language UI implementation (future)
- Localization tooling (future)
- Right-to-left layout support (future)
- Currency/date/number formatting implementation (future)
- Timezone conversion libraries (future)
- User timezone preference storage (future)

What it DOES require NOW:
- Stable IDs on every canonical primitive
- No display text as identity in any schema or registry
- All timestamps stored as UTC with IANA source timezone
- No local time used as canonical truth
- Structure that SUPPORTS future language and timezone rendering without knowledge-layer changes

---

## RELATIONSHIP TO EXISTING ARCHITECTURE

| Component | Impact |
|-----------|--------|
| Signal Bubble | `signal_id` already language-neutral — compliant |
| Semantic_State | `signal_id` already language-neutral — compliant |
| Signal_Lifecycle_Definition | `signal_id` field compliant; `category` field needs ID formalization |
| Narrative Framework | Narrative names need `narrative.*` IDs (currently English text) |
| State_Change_Taxonomy | Sub-categories need `sc.*` IDs (currently English text) |
| Expansion_Taxonomy | Order names (1st, 2nd, etc.) are language-neutral — compliant |
| Dependency_Types | Type names need `dep.*` IDs (currently English text, already ID-like) |
| Temporal_Taxonomy | Enum values are English but function as codes — acceptable |
| Market_Organism_Principles | Need `principle.*` IDs for cross-referencing |
| User Journey | Journey names are architectural labels, not user-facing — acceptable |
| Reports | Already defined as "rendering layer" in system_architecture.md — compliant |

---

## KEY INSIGHT

The existing Portfolio OS architecture already states:

> "Language is rendering. Semantics are truth."
> — system_architecture.md, Core Principle

This document formalizes that principle into an enforceable architectural constraint
that applies to every canonical primitive being defined in the Market Organism Framework.

The unified rendering principle:

> **Language and Time are rendering dimensions.**
> **Canonical objects must remain language-neutral AND timezone-neutral.**
> **All timestamps stored in UTC. All identifiers are language-independent.**
> **The rendering layer determines: language, altitude, timezone, locale formatting.**
> **No rendered language or local time may be treated as canonical truth.**

The cost of compliance NOW: assign stable IDs + store UTC timestamps.
The cost of non-compliance LATER: rebuild every registry, every cross-reference,
every report template, every dashboard component, every temporal query
when a second language or timezone is needed.

This is not about building translations or timezone conversion today.
This is about ensuring the architecture NEVER prevents them tomorrow.
