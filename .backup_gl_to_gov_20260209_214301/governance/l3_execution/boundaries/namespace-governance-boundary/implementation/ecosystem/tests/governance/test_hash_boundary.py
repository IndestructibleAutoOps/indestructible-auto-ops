#!/usr/bin/env python3
"""
Test Hash Boundary
==================

Tests the hash boundary specification.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "/workspace/ecosystem")
sys.path.insert(0, "/workspace")


def test_hash_boundary_spec_exists():
    """Test that hash boundary specification exists"""
    print("Testing hash boundary spec exists...")

    spec_file = Path("/workspace/ecosystem/governance/hash_boundary.yaml")

    if not spec_file.exists():
        print("  ❌ FAILED: Hash boundary spec does not exist")
        return False

    print("  ✅ PASSED: Hash boundary spec exists")
    return True


def test_hash_boundary_include_patterns():
    """Test that hash boundary include patterns are defined"""
    print("Testing hash boundary include patterns...")

    import yaml

    spec_file = Path("/workspace/ecosystem/governance/hash_boundary.yaml")

    with open(spec_file, "r") as f:
        spec = yaml.safe_load(f)

    if "include" not in spec:
        print("  ❌ FAILED: Include patterns not defined")
        return False

    include = spec["include"]

    required_patterns = ["artifacts", "events", "governance", "tools"]

    missing_patterns = [p for p in required_patterns if p not in include]

    if len(missing_patterns) > 0:
        print(f"  ❌ FAILED: Missing include patterns: {missing_patterns}")
        return False

    print(f"  ✅ PASSED: All {len(required_patterns)} include patterns defined")
    return True


def test_hash_boundary_exclude_patterns():
    """Test that hash boundary exclude patterns are defined"""
    print("Testing hash boundary exclude patterns...")

    import yaml

    spec_file = Path("/workspace/ecosystem/governance/hash_boundary.yaml")

    with open(spec_file, "r") as f:
        spec = yaml.safe_load(f)

    if "exclude" not in spec:
        print("  ❌ FAILED: Exclude patterns not defined")
        return False

    exclude = spec["exclude"]

    if len(exclude) == 0:
        print("  ⚠️  WARNING: No exclude patterns defined")
        return True

    print(f"  ✅ PASSED: Exclude patterns defined ({len(exclude)} patterns)")
    return True


def test_hash_boundary_canonicalization():
    """Test that hash boundary canonicalization is defined"""
    print("Testing hash boundary canonicalization...")

    import yaml

    spec_file = Path("/workspace/ecosystem/governance/hash_boundary.yaml")

    with open(spec_file, "r") as f:
        spec = yaml.safe_load(f)

    if "canonicalization" not in spec:
        print("  ❌ FAILED: Canonicalization not defined")
        return False

    canonicalization = spec["canonicalization"]

    required_fields = ["method", "standard", "version", "hash_algorithm"]

    missing_fields = [f for f in required_fields if f not in canonicalization]

    if len(missing_fields) > 0:
        print(f"  ❌ FAILED: Missing canonicalization fields: {missing_fields}")
        return False

    if canonicalization["method"] != "JCS+LayeredSorting":
        print(
            f"  ⚠️  WARNING: Canonicalization method is '{canonicalization['method']}' (expected 'JCS+LayeredSorting')"
        )

    if canonicalization["standard"] != "RFC 8785":
        print(
            f"  ⚠️  WARNING: Canonicalization standard is '{canonicalization['standard']}' (expected 'RFC 8785')"
        )

    print(f"  ✅ PASSED: Canonicalization defined")
    return True


def generate_test_result(test_name: str, passed: bool):
    """Generate test result JSON"""
    import hashlib
    from datetime import datetime, timezone

    result = {
        "test": test_name,
        "status": "passed" if passed else "failed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_file": "tests/governance/test_hash_boundary.py",
    }

    # Generate hash
    result_str = json.dumps(result, sort_keys=True)
    result["hash"] = f"sha256:{hashlib.sha256(result_str.encode()).hexdigest()}"

    return result


def save_test_results(results: list):
    """Save test results to file"""
    evidence_dir = Path("/workspace/ecosystem/.evidence/tests")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    result_file = evidence_dir / "test-hash-boundary.json"

    with open(result_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Test results saved to: {result_file}")


def main():
    """Main entry point"""
    print("=" * 70)
    print("🧪 Hash Boundary Tests")
    print("=" * 70)
    print()

    results = []

    # Run tests
    results.append(
        generate_test_result(
            "test_hash_boundary_spec_exists", test_hash_boundary_spec_exists()
        )
    )
    results.append(
        generate_test_result(
            "test_hash_boundary_include_patterns", test_hash_boundary_include_patterns()
        )
    )
    results.append(
        generate_test_result(
            "test_hash_boundary_exclude_patterns", test_hash_boundary_exclude_patterns()
        )
    )
    results.append(
        generate_test_result(
            "test_hash_boundary_canonicalization", test_hash_boundary_canonicalization()
        )
    )

    # Save results
    save_test_results(results)

    # Summary
    passed = sum(1 for r in results if r["status"] == "passed")
    total = len(results)

    print()
    print("=" * 70)
    print(f"📊 Summary: {passed}/{total} tests passed")
    print("=" * 70)

    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
