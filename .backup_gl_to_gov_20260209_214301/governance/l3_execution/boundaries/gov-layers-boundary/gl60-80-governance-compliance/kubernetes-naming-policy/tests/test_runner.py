#!/usr/bin/env python3
"""
Simple test runner for naming policy system (no pytest required)
GL Layer: GL60-80 Governance Compliance
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import build_standard_validator, Normalizer, Truncator, Rule

def test_normalizer():
    """Test normalizer functionality."""
    print("Testing Normalizer...")
    normalizer = Normalizer()

    test_cases = [
        ("Prod/Payment@SVC", "prod-payment-svc"),
        ("---a---", "a"),
        ("UPPERCASE", "uppercase"),
        ("test-123", "test-123"),
        ("hello---world", "hello-world"),
    ]

    passed = 0
    failed = 0

    for input_val, expected in test_cases:
        result = normalizer.normalize(input_val)
        if result == expected:
            print(f"  ✓ {input_val} -> {result}")
            passed += 1
        else:
            print(f"  ✗ {input_val} -> {result} (expected {expected})")
            failed += 1

    return passed, failed

def test_validator():
    """Test validator functionality."""
    print("\nTesting NamingValidator...")
    validator = build_standard_validator()

    test_cases = [
        ("test", "dns1123Label63", True, True),
        ("test-123", "dns1123Label63", True, True),
        ("UPPERCASE", "dns1123Label63", False, True),  # Strict fails, normalized passes
        ("http", "portName15", True, True),
        ("8080", "portName15", False, False),  # Starts with number - always fails
    ]

    passed = 0
    failed = 0

    for input_val, rule, should_pass_strict, should_pass_norm in test_cases:
        # Test strict mode
        result_strict = validator.process(input_val, rule, normalize=False, auto_truncate=False)
        strict_ok = (result_strict.passed == should_pass_strict)

        # Test normalized mode
        result_norm = validator.process(input_val, rule, normalize=True, auto_truncate=False)
        norm_ok = (result_norm.passed == should_pass_norm)

        if strict_ok and norm_ok:
            print(f"  ✓ {input_val} ({rule})")
            passed += 1
        else:
            print(f"  ✗ {input_val} ({rule}) - strict:{result_strict.passed}/{should_pass_strict}, norm:{result_norm.passed}/{should_pass_norm}")
            failed += 1

    return passed, failed

def test_truncator():
    """Test truncator functionality."""
    print("\nTesting Truncator...")
    truncator = Truncator()

    # Test short name (no truncation)
    short = "short"
    result = truncator.truncate_and_hash(short, 63)

    if result == short:
        print(f"  ✓ Short name not truncated")
        passed = 1
        failed = 0
    else:
        print(f"  ✗ Short name changed: {result}")
        passed = 0
        failed = 1

    # Test long name (truncation)
    long_name = "a" * 100
    result = truncator.truncate_and_hash(long_name, 63)

    if len(result) <= 63:
        print(f"  ✓ Long name truncated to {len(result)} chars")
        passed += 1
    else:
        print(f"  ✗ Long name not properly truncated: {len(result)} chars")
        failed += 1

    # Test determinism
    result1 = truncator.truncate_and_hash(long_name, 63)
    result2 = truncator.truncate_and_hash(long_name, 63)

    if result1 == result2:
        print(f"  ✓ Truncation is deterministic")
        passed += 1
    else:
        print(f"  ✗ Truncation is not deterministic")
        failed += 1

    return passed, failed

def test_rules():
    """Test rule validation."""
    print("\nTesting Rules...")

    rule = Rule(
        name="test",
        maxLength=63,
        allowEmpty=False,
        charset=r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$"
    )

    valid_cases = ["test", "test-123", "my-service"]
    invalid_cases = ["UPPERCASE", "test-", "-test"]

    passed = 0
    failed = 0

    for case in valid_cases:
        is_valid = rule.matches(case)
        if is_valid:
            print(f"  ✓ {case} is valid")
            passed += 1
        else:
            print(f"  ✗ {case} should be valid")
            failed += 1

    for case in invalid_cases:
        is_valid = rule.matches(case)
        if not is_valid:
            print(f"  ✓ {case} is invalid (as expected)")
            passed += 1
        else:
            print(f"  ✗ {case} should be invalid")
            failed += 1

    return passed, failed

def main():
    """Run all tests."""
    print("=" * 60)
    print("Kubernetes Naming Policy System - Test Runner")
    print("=" * 60)

    total_passed = 0
    total_failed = 0

    # Run all test suites
    passed, failed = test_normalizer()
    total_passed += passed
    total_failed += failed

    passed, failed = test_validator()
    total_passed += passed
    total_failed += failed

    passed, failed = test_truncator()
    total_passed += passed
    total_failed += failed

    passed, failed = test_rules()
    total_passed += passed
    total_failed += failed

    # Summary
    print("\n" + "=" * 60)
    print(f"Test Results: {total_passed} passed, {total_failed} failed")
    print("=" * 60)

    if total_failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total_failed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
