# Python Environment Configuration

## inclusion: always

**Status**: MANDATORY | **Owner**: CTO | **Scope**: all-python-execution

## Python Interpreter

This project uses Python 3.13.7 via a local virtual environment.

**ALWAYS use this command to run Python:**

```
.venv/bin/python
```

**NEVER run:**
- `python` (does not exist on this system)
- `python3` (system Python, missing project dependencies)
- `which python` (wastes time, answer is always `.venv/bin/python`)

## Package Management

- Use `.venv/bin/pip` for installing packages
- Use `.venv/bin/python -m pytest` for running tests

## Working Directory for Domainization Tests

When running domainization tests:

```bash
.venv/bin/python -m pytest .domainization/src/<test_file>.py -v
```

Or from within the src directory:

```bash
cd .domainization/src && ../../.venv/bin/python -m pytest <test_file>.py -v
```

## Key Facts

- Python version: 3.13.7
- Virtual environment: `.venv/` (project root)
- Interpreter path: `.venv/bin/python`
- Pip path: `.venv/bin/pip`
- OS: macOS (darwin)
