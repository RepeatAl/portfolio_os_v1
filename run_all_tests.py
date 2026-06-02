"""Run all tests individually and collect results."""
import subprocess
import time
import re
import os

os.chdir("/Users/macbookpro/PycharmProjects/portfolio_os_v1")

test_files = [
    "tests/test_deterministic_ordering_enforcement.py",
    "tests/test_property_canonical_boundary_enforcement.py",
    "tests/test_property_chain_provenance_integrity.py",
    "tests/test_property_confidence_degradation.py",
    "tests/test_property_data_availability_summary.py",
    "tests/test_property_deployment_matrix_partition.py",
    "tests/test_property_forbidden_flow_detection.py",
    "tests/test_property_governance_event_completeness.py",
    "tests/test_property_graceful_degradation.py",
    "tests/test_property_non_determinism_injection.py",
    "tests/test_property_pipeline_determinism.py",
    "tests/test_property_pipeline_state_aggregation.py",
    "tests/test_property_portfolio_watchlist_separation.py",
    "tests/test_property_position_transition_rendering.py",
    "tests/test_property_provenance_parseability.py",
    "tests/test_property_reasoning_object_schema.py",
    "tests/test_property_reasoning_object_section_mapping.py",
    "tests/test_property_report_structure_invariant.py",
    "tests/test_property_report_value_validation.py",
    "tests/test_property_run_context_temporal_consistency.py",
    "tests/test_property_schema_version_compatibility.py",
    "tests/test_property_section_completeness.py",
    "tests/test_property_semantic_coverage_invariant.py",
    "tests/test_property_semantic_delta_correctness.py",
    "tests/test_property_semantic_state_round_trip.py",
    "tests/test_property_sunset_governance_behavior.py",
    "tests/test_sunset_governance.py",
]

total_passed = 0
total_failed = 0
total_errors = 0
total_skipped = 0
total_warnings = 0
failed_tests = []
start_time = time.time()

for tf in test_files:
    try:
        result = subprocess.run(
            [".venv/bin/python", "-m", "pytest", tf, "--tb=line", "-q"],
            capture_output=True, text=True, timeout=45
        )
        output = result.stdout + result.stderr
        # Parse summary line
        for line in output.split("\n"):
            if "passed" in line or "failed" in line or "error" in line:
                if ("passed" in line or "failed" in line) and "in" in line:
                    passed_m = re.search(r"(\d+) passed", line)
                    failed_m = re.search(r"(\d+) failed", line)
                    error_m = re.search(r"(\d+) error", line)
                    skipped_m = re.search(r"(\d+) skipped", line)
                    warning_m = re.search(r"(\d+) warning", line)
                    if passed_m:
                        total_passed += int(passed_m.group(1))
                    if failed_m:
                        total_failed += int(failed_m.group(1))
                        failed_tests.append(tf)
                    if error_m:
                        total_errors += int(error_m.group(1))
                    if skipped_m:
                        total_skipped += int(skipped_m.group(1))
                    if warning_m:
                        total_warnings += int(warning_m.group(1))
                    break
        print(f"  {tf}: done ({result.returncode})")
    except subprocess.TimeoutExpired:
        print(f"  {tf}: TIMEOUT")
        failed_tests.append(f"{tf} (TIMEOUT)")

elapsed = time.time() - start_time

print(f"\n{'='*60}")
print(f"FULL TEST SUITE RESULTS")
print(f"{'='*60}")
print(f"Total tests:    {total_passed + total_failed + total_errors}")
print(f"Passed:         {total_passed}")
print(f"Failed:         {total_failed}")
print(f"Errors:         {total_errors}")
print(f"Skipped:        {total_skipped}")
print(f"Warnings:       {total_warnings}")
print(f"Runtime:        {elapsed:.2f}s")
print(f"{'='*60}")
if failed_tests:
    print(f"\nFailed test files:")
    for ft in failed_tests:
        print(f"  - {ft}")
else:
    print("\nAll tests PASSED!")
