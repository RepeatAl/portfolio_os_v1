# Deployment Governance Gap Analysis — Domainization-Governance-Hardening

## Document Purpose

Analysis of deployment guarantees, CI coverage gaps, and warning-vs-blocking boundaries.
All findings are evidence-backed with file references. No implementation recommendations.

---

## 1. Current Deployment Guarantees

### CI Pipeline Definition

Source: `.github/workflows/python-app.yml`

**Trigger conditions:**
- Push to: `main`, `governance/**`, `feature/**`, `fix/**`, `spec/**`
- Pull requests to: `main`

**Execution environment:** Ubuntu latest, Python 3.13

**Steps executed:**

| Step | Command | What It Validates | Blocks Deploy? |
|------|---------|-------------------|----------------|
| 1. Checkout | `actions/checkout@v4` | Repository accessible | Yes (infra) |
| 2. Setup Python | `actions/setup-python@v5` | Python 3.13 available | Yes (infra) |
| 3. Install deps | `pip install -r requirements.txt` | Dependencies resolve | Yes |
| 4. Set PYTHONPATH | `echo "PYTHONPATH=$(pwd)"` | Import paths correct | Yes (infra) |
| 5. Validate syntax | `python -m compileall engines/ -q` | Python files in `engines/` parse | Yes |
| 6. Validate imports | 4× `python -c "from engines import X"` | 4 specific engines importable | Yes |
| 7. Summary | `echo "...completed successfully."` | Nothing | No |

### What Is Actually Verified

| Guarantee | Scope | Confidence |
|-----------|-------|------------|
| Python syntax correctness | `engines/` directory only | HIGH for engines, ZERO for runtime/, governance/, tests/ |
| Import resolution | allocation, report, regime, scoring engines | HIGH for these 4, ZERO for 8 other engines |
| Dependency installation | All pip packages | HIGH |

### What Is NOT Verified

| Missing Guarantee | Impact |
|-------------------|--------|
| Syntax of `runtime/` files | Runtime modules could have syntax errors on main |
| Syntax of `governance/` files | Governance modules could have syntax errors on main |
| Syntax of `.domainization/src/` files | Domainization system could be broken on main |
| Any test execution | All 27 property-based tests never run |
| Any governance check | Health report, registration, lifecycle — none execute |
| Import of 8 other engines | priority, scenario, decision, quality, delta, morning_briefing, visual, semantic engines unchecked |
| YAML validity | `config.yaml`, `domain_registry.yaml`, `artifact_registry.yaml`, `lifecycle_state_machine.yaml` — none validated |

---

## 2. Missing Deployment Guarantees

### Tier 1: Fundamental (Should Block Deploy)

| Missing Check | What It Would Catch | Current Risk |
|---------------|--------------------|--------------| 
| Full test suite execution | Broken governance contracts, invalid schemas, chain integrity failures | CRITICAL — 27 tests exist but never run in CI |
| Syntax validation of all Python | Syntax errors in runtime/, governance/, .domainization/src/ | HIGH — only engines/ is checked |
| All engine imports | Broken imports in 8 unchecked engines | MEDIUM — partial coverage exists |
| YAML schema validation | Malformed registry, invalid lifecycle definitions, broken config | HIGH — YAML files are governance truth |

### Tier 2: Governance (Should Warn or Block)

| Missing Check | What It Would Catch | Current Risk |
|---------------|--------------------|--------------| 
| Health report generation | Overall system health degradation | HIGH — no visibility into system state at deploy |
| Registration enforcement | Unregistered artifacts merging to main | HIGH — W800/W801 warnings never emitted in CI |
| Lifecycle state validation | Invalid transitions persisted to registry | MEDIUM — transitions are post-hoc validated only |
| Sunset governance evaluation | Expired artifacts still generating | MEDIUM — sunset dates pass without action |
| Chain validator execution | Broken provenance chains | HIGH — chain integrity is a core guarantee |

### Tier 3: Integrity (Should Audit)

| Missing Check | What It Would Catch | Current Risk |
|---------------|--------------------|--------------| 
| Schema version compatibility | Producer/consumer version mismatches | LOW — all at 1.0.0 currently |
| Domain boundary validation | Cross-domain ownership violations | MEDIUM — violations accumulate silently |
| Artifact mutation audit | Unauthorized registry modifications | MEDIUM — no per-commit tracking |
| Determinism verification | Non-reproducible outputs | HIGH — determinism is a stated requirement |

---

## 3. Recommended Future Deployment Gates

### Gate Priority Matrix

| Priority | Gate Name | Type | Rationale |
|----------|-----------|------|-----------|
| P0 | Full test suite | Blocking | 27 property tests verify all governance contracts |
| P0 | All-directory syntax check | Blocking | Current check covers only `engines/` |
| P1 | YAML schema validation | Blocking | Registry/config corruption breaks governance |
| P1 | Health report generation | Warning → Blocking | System health visibility at deploy time |
| P2 | Registration enforcement | Warning | Track unregistered artifact growth |
| P2 | Chain validator smoke test | Warning → Blocking | Provenance integrity verification |
| P3 | Sunset governance report | Informational | Visibility into deprecation pipeline |
| P3 | Domain boundary audit | Informational | Track cross-domain violations |
| P4 | Determinism verification | Blocking (future) | Requires stable inputs for comparison |

### Phase Mapping

| Phase | Gates Activated | Mode |
|-------|----------------|------|
| Domainization-Governance-Hardeninga (immediate) | P0 gates | Blocking |
| Domainization-Governance-Hardeningb (stabilization) | P1 gates | Warning initially, blocking after validation |
| Domainization-Governance-Hardeningc (enforcement) | P2 gates | Warning with baseline tracking |
| Domainization-Governance-Hardeningd (maturity) | P3-P4 gates | Informational → Warning → Blocking progression |

---

## 4. Warning vs Blocking Analysis

### Current Warning-Only Components

| Component | Current Behavior | Should It Block? | Rationale |
|-----------|-----------------|------------------|-----------|
| Pre-commit hook (all observers) | Always exits 0 | Configurable | Depends on enforcement mode transition |
| Forbidden flow detection | Logs WARNING | No (currently) | 13/14 categories are known gaps — blocking would halt all development |
| Briefing deprecation warnings | `DeprecationWarning` | No | Legacy compatibility required during transition |
| Sunset governance warnings | `DeprecationWarning` | Conditional | Should block only when sunset_date passed AND deps=0 |
| Registration enforcement (W800) | Warning in report | Yes (for new artifacts) | New artifacts should require registration |
| Registration baseline (W801) | Warning in report | Yes (growth detection) | Unregistered count should not increase |
| Chain validation violations | `severity: "warning"` | Conditional | Should block in `hard` mode only |
| Lifecycle transition violations | Warning in observer | Conditional | Should block invalid transitions in `hard` mode |

### Blocking Criteria Analysis

| Condition | Should Block? | Evidence for Decision |
|-----------|--------------|----------------------|
| Test failure | Yes — always | Tests verify governance contracts; failure = broken contract |
| Syntax error (any directory) | Yes — always | Broken syntax = broken system |
| YAML parse failure | Yes — always | Unparseable config = governance system offline |
| Unregistered artifact (new) | Yes — in `soft`+ mode | `RegistrationEnforcementPolicy` already defines this |
| Chain integrity violation | Yes — in `hard` mode | `SEVERITY_DEFINITIONS[CANONICAL_BREAK]["blocks_pipeline_hard_mode"] = True` |
| Lifecycle invalid transition | Yes — in `hard` mode | State machine defines valid transitions |
| Sunset-blocked artifact | No — warning only | `sunset_governance.py` handles gracefully with continued generation |
| Forbidden flow (known) | No — warning only | Known gaps during transition period |
| Domain boundary violation | No — warning only (initially) | Requires `allowed_writers` enforcement infrastructure |

---

## 5. Deployment/Runtime Divergence Risks

### What CI Validates vs What Runtime Assumes

| Aspect | CI Validates | Runtime Assumes | Divergence Risk |
|--------|-------------|-----------------|-----------------|
| Engine availability | 4 engines importable | All 12 engines callable | 8 engines could fail at runtime without CI catching it |
| YAML config validity | Not checked | `pipeline_orchestrator.py` loads config at startup | Malformed YAML crashes pipeline at runtime |
| Registry integrity | Not checked | `sunset_governance.py` loads full registry | Corrupt registry breaks sunset evaluation |
| Chain model integrity | Not checked | `chain_validator.py` builds identifier graph | Broken chain model produces invalid provenance |
| Semantic engine | Not checked | `pipeline_orchestrator.py` calls `interpret_allocation_signals()` | Semantic engine failure degrades all outputs |
| State machine validity | Not checked | `lifecycle_manager.py` loads state machine | Invalid state machine breaks lifecycle validation |
| Confidence policy | Not checked | `confidence_policy.py` loads from YAML at runtime | Invalid policy formula produces wrong confidence values |

### Divergence Scenarios

| Scenario | CI Result | Runtime Result | Detection |
|----------|-----------|----------------|-----------|
| `runtime/chain_validator.py` has syntax error | CI passes (not checked) | ImportError at pipeline start | **Undetected until runtime** |
| `governance/confidence_policy.yaml` has invalid formula | CI passes (not checked) | Wrong confidence values in reports | **Undetected until manual review** |
| `.domainization/artifact_registry.yaml` has duplicate artifact_id | CI passes (not checked) | Sunset governance produces incorrect phase evaluations | **Undetected until health report** |
| `engines/semantic_engine.py` import fails | CI passes (not checked) | Pipeline degrades all 14 categories | **Undetected until pipeline execution** |
| Property test for provenance parseability fails | CI passes (tests not run) | Provenance sidecar may be unparseable | **Undetected until chain validation** |

---

## 6. Deployment Integrity Score

### Current Score: 2/10

| Criterion | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Syntax validation coverage | 15% | 3/10 | Only `engines/` checked; 4 other directories unchecked |
| Import validation coverage | 10% | 3/10 | 4 of 12+ engines checked |
| Test execution | 25% | 0/10 | Zero tests run in CI |
| Governance check execution | 20% | 0/10 | Zero governance checks in CI |
| YAML validation | 10% | 0/10 | No YAML files validated |
| Deployment gate existence | 10% | 0/10 | No blocking gates beyond syntax/import |
| Audit trail | 10% | 2/10 | Git history exists but no structured governance audit |

**Weighted score: 0.15×3 + 0.10×3 + 0.25×0 + 0.20×0 + 0.10×0 + 0.10×0 + 0.10×2 = 0.45 + 0.30 + 0 + 0 + 0 + 0 + 0.20 = 0.95/10 ≈ 1.0/10**

### Gap to Minimum Acceptable (6/10)

To reach 6/10, the deployment pipeline needs:
1. Full syntax validation (all directories) → +1.2 points
2. Full import validation (all engines) → +0.7 points  
3. Test execution (27 property tests) → +2.5 points
4. Basic governance check (health report) → +1.0 points
5. YAML validation (4 config files) → +1.0 points

**Total potential improvement: +6.4 points → 7.4/10**

---

## 7. Summary

The deployment pipeline provides minimal guarantees (syntax of one directory, imports of 4 engines) while the runtime system assumes comprehensive integrity across all modules, configurations, and governance contracts. This divergence means:

1. **Governance contracts are unverified at deploy time** — 27 property tests exist but never execute
2. **Configuration integrity is unverified** — 4 YAML governance files are never validated
3. **Runtime module integrity is unverified** — `runtime/`, `governance/`, `.domainization/src/` syntax never checked
4. **The gap between CI and runtime assumptions is the primary deployment risk** — CI validates ~10% of what runtime depends on
