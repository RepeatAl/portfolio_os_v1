# Performance Benchmarks

## Overview

Comprehensive performance benchmark tests for the domainization system. These tests validate that the system meets non-functional performance requirements under realistic load conditions with 100 and 1000 artifacts.

## Features

- **Commit gate validation benchmarks**: Verifies all 5 observers complete within the 5-second target
- **Health report generation benchmarks**: Verifies full report generation (with violations) completes within 10 seconds
- **Registry query performance**: Validates indexed lookups, domain/type/lifecycle filtering at scale
- **Scalability verification**: Confirms support for 20+ domains and 10 lifecycle states per artifact type
- **End-to-end workflow simulation**: Tests cold-start and warm-cache scenarios

## Performance Targets

| Operation | Target | Measured (1000 artifacts) |
|-----------|--------|--------------------------|
| Commit gate validation | < 5 seconds | ~1.7s |
| Health report generation | < 10 seconds | ~3.2s |
| Individual artifact lookup | < 1ms | ~0.001ms |
| Domain query (cached) | < 1ms | ~0.06ms |
| Cache warm validation | < 1 second | ~0.07s |

## Usage

### Run all performance tests

```bash
cd .domainization/src
python -m pytest test_performance_benchmarks.py -v -s
```

### Run specific test class

```bash
# Commit gate performance only
python -m pytest test_performance_benchmarks.py::TestCommitGateValidationPerformance -v -s

# Health report performance only
python -m pytest test_performance_benchmarks.py::TestHealthReportGenerationPerformance -v -s

# Registry query performance only
python -m pytest test_performance_benchmarks.py::TestRegistryQueryPerformance -v -s

# Scalability tests only
python -m pytest test_performance_benchmarks.py::TestScalability -v -s
```

## Test Classes

### TestCommitGateValidationPerformance
- Validates 100 and 1000 artifact scenarios
- Tests subset validation (changed files only)
- Measures individual observer execution time

### TestHealthReportGenerationPerformance
- Full report generation with and without violations
- Domain coverage calculation performance
- Lifecycle distribution calculation performance

### TestRegistryQueryPerformance
- Registry load time at scale
- Artifact lookup by ID (O(1) with dict)
- Domain, type, and lifecycle filter queries
- Cached vs uncached query comparison

### TestScalability
- 20+ domain support verification
- 10 lifecycle states per artifact type
- Combined scalability under load

### TestEndToEndPerformanceScenario
- Full cold-start commit gate workflow
- Repeated validation (warm cache) speedup measurement

## Requirements Satisfied

- **15.1**: Commit gates complete in less than 5 seconds
- **15.2**: Registry supports at least 1000 artifacts
- **15.3**: Health reports complete in less than 10 seconds
- **15.9**: System supports at least 20 domains and 10 lifecycle states per artifact type

## Related Files

- `validation_orchestrator.py` - Orchestrates all 5 validation observers
- `health_reporter.py` - Generates health reports
- `registry_cache.py` - In-memory cache with indexed queries
- `artifact_registry.py` - Core artifact registry operations
- `test_registry_cache_performance.py` - Cache-specific performance tests
