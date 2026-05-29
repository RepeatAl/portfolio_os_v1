# CI Pipeline Hardening — Governance Runtime Enforcement

## Purpose

This document describes the CI pipeline hardening implemented as part of the Governance Runtime Enforcement spec (Task 3). The pipeline validates governance contracts, syntax integrity, YAML schemas, engine imports, and runtime integrity on every push and PR.

## CI Workflow

**File**: `.github/workflows/python-app.yml`
**Trigger**: Push to `main`, `governance/**`, `feature/**`, `fix/**`, `spec/**` branches; all PRs to `main`
**Runner**: `ubuntu-latest` with Python 3.13

## Pipeline Steps

| # | Step | Blocking | Time Budget | Requirements |
|---|------|----------|-------------|--------------|
| 1 | Full Test Suite | Yes | 60s | Req 1.1–1.4 |
| 2 | All-Directory Syntax Validation | Yes | — | Req 2.1–2.3 |
| 3 | Governance YAML Validation | Yes | — | Req 3.1–3.3 |
| 4 | ENGINE_REGISTRY Import Validation | Yes | — | Req 4.1–4.3 |
| 5 | Runtime Integrity Hash | No (informational) | 5s | Req 36.1–36.2 |

### Step 1: Full Test Suite

Executes all property-based and unit tests in `tests/` with verbose output and short tracebacks.

```bash
python -m pytest tests/ -v --tb=short
```

- Blocks merge on any test failure
- 60-second timeout prevents runaway tests

### Step 2: All-Directory Syntax Validation

Validates Python syntax across all source directories using `compileall`.

```bash
python -m compileall -q engines/ runtime/ governance/ .domainization/src/ tests/
```

- Quiet mode (only reports errors)
- Blocks merge on syntax errors in any directory

### Step 3: Governance YAML Validation

Inline Python script that loads and validates required top-level keys in governance YAML files.

**Validated files and required keys**:

| File | Required Keys |
|------|---------------|
| `.domainization/config.yaml` | `enforcement_mode`, `current_phase`, `observers` |
| `.domainization/domain_registry.yaml` | `domains` |
| `.domainization/artifact_registry.yaml` | `artifacts` |
| `.domainization/lifecycle_state_machine.yaml` | `artifact_types` |

- Reports file name and specific error on failure
- Blocks merge on parse failure or missing keys

### Step 4: ENGINE_REGISTRY Import Validation

Dynamically reads `ENGINE_REGISTRY` from `engines/engine_registry.py` and imports each registered engine.

- No hardcoded engine list — reads from registry at runtime
- Future engines are validated automatically when added to the registry
- Reports module name and import error on failure
- Blocks merge on import failure

### Step 5: Runtime Integrity Hash (Informational)

Computes a SHA-256 fingerprint over behavior-defining files for drift detection.

- Uses `RuntimeIntegrityHash` + `HashCanonicalizer` from `governance/`
- Persists hash to `runtime_integrity_hash.txt` as CI artifact
- `continue-on-error: true` — does NOT block merge
- Detects drift between CI-validated state and runtime execution

## Supporting Modules

### `governance/hash_canonicalizer.py`

Platform-independent file content canonicalization for deterministic hashing.

**Methods**:
- `normalize_line_endings()` — CRLF/CR → LF
- `normalize_encoding()` — bytes → UTF-8 (latin-1 fallback)
- `strip_trailing_whitespace()` — per-line trailing whitespace removal
- `ensure_final_newline()` — exactly one trailing newline
- `canonicalize_yaml()` — parse → re-serialize with sorted keys
- `canonicalize_python()` — LF + strip trailing whitespace + final newline
- `canonicalize_file()` — auto-detect by extension, apply appropriate canonicalization
- `compute_hash()` — SHA-256 over sorted canonicalized content

### `governance/runtime_integrity_hash.py`

SHA-256 fingerprint for detecting deployment drift.

**TARGET_PATHS** (behavior-defining files):
- `.domainization/config.yaml`
- `.domainization/lifecycle_state_machine.yaml`
- `.domainization/domain_registry.yaml`
- `.domainization/artifact_registry.yaml`
- `.domainization/fail_mode_config.yaml`
- `governance/confidence_policy.yaml`
- `governance/*.py` (all governance modules)
- `runtime/*.py` (all runtime modules)
- `engines/engine_registry.py` (dependency graph only)

**Excluded**: Individual engine implementations (`*_engine.py`)

**Methods**:
- `compute()` — resolve paths, canonicalize, SHA-256
- `verify_against(expected_hash)` — compare current vs expected, return (match, details)

## Design Principles

1. **Dynamic over hardcoded** — Engine validation reads from registry, not a static list
2. **Informational before blocking** — Integrity hash is non-blocking until enforcement mode advances
3. **Platform independence** — Canonicalization ensures identical hashes across macOS/Linux/CI
4. **Scope principle** — Hash files that define system behavior, not files that implement business logic
