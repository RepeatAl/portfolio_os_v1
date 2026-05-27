---
artifact_id: trusted_signal_sources_md
primary_domain: DATA
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2024-06-08
last_modified: 2026-05-25
owner_role: Defines trusted data sources and signal governance rules
ssot_relationship: canonical
topic: trusted_sources
allowed_writers: [DATA]
allowed_readers: [ALL]
dependencies: [data_ingestion_normalization_framework_md]
---

# PORTFOLIO OS — TRUSTED SIGNAL SOURCES
Version: v1
Status: Active Signal Governance SSOT

---

# PURPOSE

Portfolio OS is a signal-driven reasoning system.

The quality of reasoning depends on the quality of signal sources.

This document defines:

- trusted market data sources
- trusted macro sources
- trusted institutional sources
- trusted financial media
- trusted research providers
- signal governance rules

Portfolio OS must prioritize:

- reliability
- institutional relevance
- consistency
- signal quality

over:

- speed
- hype
- social sentiment
- retail noise

---

# CORE PRINCIPLE

Not all financial information has equal value.

Portfolio OS prioritizes:

- institutional-grade information
- economically relevant signals
- historically reliable data providers
- broad macro context
- cross-confirmed market information

The system must avoid:

- social media hype
- emotional narratives
- influencer-driven signals
- meme-style market commentary
- low-trust speculation

---

# MARKET DATA SOURCES

These sources provide raw market and pricing data.

---

## PRIMARY MARKET DATA PROVIDERS

### Yahoo Finance

Purpose:
General market pricing and historical data.

Used For:
- equities
- ETFs
- indices
- currencies
- historical pricing

Strengths:
- broad coverage
- accessible
- fast integration

Limitations:
- not institutional-grade latency
- occasional symbol inconsistencies

Status:
Approved.

---

### Google Finance

Purpose:
Supplementary pricing validation.

Used For:
- broad market confirmation
- company information
- quick validation

Strengths:
- simple verification layer
- broad retail accessibility

Limitations:
- limited API structure
- less detailed institutional data

Status:
Approved as secondary validation source.

---

### Stooq

Purpose:
Historical macro and index validation.

Used For:
- indices
- macro proxies
- historical comparisons

Strengths:
- reliable long-term datasets
- lightweight access

Limitations:
- narrower coverage

Status:
Approved.

---

# INSTITUTIONAL MACRO SOURCES

These sources define macroeconomic reality.

---

## CENTRAL BANKS

### Federal Reserve (FED)

Used For:
- rates
- liquidity conditions
- macro policy

Status:
Primary macro authority.

---

### European Central Bank (ECB)

Used For:
- European rates
- liquidity
- inflation policy

Status:
Primary European macro authority.

---

### Bank of Japan (BOJ)

Used For:
- global liquidity context
- yield curve monitoring

Status:
Approved.

---

# ECONOMIC INSTITUTIONS

---

### IMF

Used For:
- global macro conditions
- sovereign risk
- structural economic trends

Status:
Approved.

---

### OECD

Used For:
- economic cycle analysis
- growth projections
- structural indicators

Status:
Approved.

---

### World Bank

Used For:
- global development context
- macro structural analysis

Status:
Approved.

---

# FINANCIAL NEWS SOURCES

Portfolio OS uses news as contextual signal support.

News must NEVER directly define portfolio truth.

---

# PRIMARY FINANCIAL NEWS SOURCES

### Reuters

Purpose:
Primary factual financial news source.

Strengths:
- high factual consistency
- low sensationalism
- institutional relevance

Status:
Tier 1 Trusted Source.

---

### Bloomberg

Purpose:
Institutional market context and macro interpretation.

Strengths:
- broad institutional coverage
- macro relevance
- policy interpretation

Limitations:
- occasional narrative framing bias

Status:
Tier 1 Trusted Source.

---

### Financial Times (FT)

Purpose:
Global macro and institutional interpretation.

Strengths:
- macro depth
- international relevance

Status:
Tier 1 Trusted Source.

---

### Wall Street Journal (WSJ)

Purpose:
Corporate and macroeconomic context.

Strengths:
- business coverage
- institutional relevance

Status:
Tier 1 Trusted Source.

---

### CNBC

Purpose:
Short-term market context monitoring.

Strengths:
- fast reporting
- market reaction visibility

Limitations:
- higher noise level
- TV-driven narrative bias

Status:
Tier 2 Context Source.

---

# RESEARCH PROVIDERS

Research providers are supportive context only.

Portfolio OS must NEVER blindly follow analyst opinions.

---

## APPROVED RESEARCH SOURCES

### Goldman Sachs Research
### JPMorgan Research
### Morgan Stanley Research
### Bank of America Research
### UBS Research
### Deutsche Bank Research
### Barclays Research
### Citi Research
### BlackRock Research
### Bridgewater Research

Purpose:
- institutional positioning insight
- macro framing
- sentiment monitoring

Limitations:
- opinion-based
- not canonical truth

Status:
Contextual signal support only.

---

# FORBIDDEN SIGNAL SOURCES

Portfolio OS must avoid:

- TikTok finance
- Reddit hype threads
- meme stock influencers
- Twitter/X trading hype
- pump-and-dump channels
- anonymous Telegram groups
- emotional trading commentary
- AI-generated market spam

These sources may distort reasoning quality.

---

# SIGNAL PRIORITY HIERARCHY

Priority order:

1. Market structure
2. Macro conditions
3. Liquidity conditions
4. Breadth confirmation
5. Cross-asset confirmation
6. Portfolio structure
7. Institutional research
8. Financial news
9. Retail sentiment

Retail sentiment is lowest priority.

---

# NEWS GOVERNANCE RULE

News is contextual.

News does NOT equal truth.

Portfolio OS must prioritize:

- measurable signals
- market structure
- portfolio structure

over headlines.

---

# CROSS-CONFIRMATION RULE

Important conclusions should ideally be confirmed by:

- multiple engines
- multiple signal types
- multiple source categories

Example:

Risk-off environment may require confirmation from:

- volatility
- yields
- breadth
- liquidity
- cross-asset behavior

No single headline may dominate PM reasoning.

---

# LONG-TERM SOURCE EXPANSION

Future approved sources may include:

- BIS
- Eurostat
- FRED
- SEC filings
- earnings transcripts
- fund flow databases
- options flow datasets
- bond spread datasets

All future sources must satisfy:

- reliability
- explainability
- institutional relevance
- low noise
- historical usefulness

---

# SOURCE GOVERNANCE PRINCIPLE

Portfolio OS is not designed to maximize information volume.

Portfolio OS is designed to maximize signal quality.

Reliable reasoning requires disciplined inputs.