#!/usr/bin/env python3
"""
Test Tool Registry
==================

Tests the tool registry and tool registration.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "/workspace/ecosystem")
sys.path.insert(0, "/workspace")


def test_tool_registry_exists():
    """Test that tool registry exists"""
    print("Testing tool registry exists...")

    registry_file = Path("/workspace/ecosystem/tools/registry.json")

    if not registry_file.exists():
        print("  ❌ FAILED: Tool registry does not exist")
        return False

    print("  ✅ PASSED: Tool registry exists")
    return True


def test_tool_registry_structure():
    """Test that tool registry has correct structure"""
    print("Testing tool registry structure...")

    registry_file = Path("/workspace/ecosystem/tools/registry.json")

    with open(registry_file, "r") as f:
        registry = json.load(f)

    required_fields = ["version", "era", "tools", "verification_status"]

    missing_fields = [f for f in required_fields if f not in registry]

    if len(missing_fields) > 0:
        print(f"  ❌ FAILED: Missing registry fields: {missing_fields}")
        return False

    print(f"  ✅ PASSED: Tool registry has correct structure")
    return True


def test_tools_registered():
    """Test that all required tools are registered"""
    print("Testing tools registered...")

    registry_file = Path("/workspace/ecosystem/tools/registry.json")

    with open(registry_file, "r") as f:
        registry = json.load(f)

    tools = registry.get("tools", {})
    required_tools = [
        "evidence_chain_diagnostic",
        "migrate_event_stream",
        "test_hash_consistency",
        "governance_closure_engine",
        "canonicalize",
        "enforce_rules",
    ]

    missing_tools = [t for t in required_tools if t not in tools]

    if len(missing_tools) > 0:
        print(f"  ❌ FAILED: Missing tools: {missing_tools}")
        return False

    print(f"  ✅ PASSED: All {len(required_tools)} tools registered")
    return True


def test_tool_verification_status():
    """Test that tools have verification status"""
    print("Testing tool verification status...")

    registry_file = Path("/workspace/ecosystem/tools/registry.json")

    with open(registry_file, "r") as f:
        registry = json.load(f)

    verification_status = registry.get("verification_status", {})

    if "verified_tools" not in verification_status:
        print("  ❌ FAILED: Verification status missing verified_tools count")
        return False

    if verification_status["verified_tools"] == 0:
        print("  ❌ FAILED: No verified tools")
        return False

    print(f"  ✅ PASSED: {verification_status['verified_tools']} tools verified")
    return True


def generate_test_result(test_name: str, passed: bool):
    """Generate test result JSON"""
    import hashlib
    from datetime import datetime, timezone

    result = {
        "test": test_name,
        "status": "passed" if passed else "failed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_file": "tests/governance/test_tool_registry.py",
    }

    # Generate hash
    result_str = json.dumps(result, sort_keys=True)
    result["hash"] = f"sha256:{hashlib.sha256(result_str.encode()).hexdigest()}"

    return result


def save_test_results(results: list):
    """Save test results to file"""
    evidence_dir = Path("/workspace/ecosystem/.evidence/tests")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    result_file = evidence_dir / "test-tool-registry.json"

    with open(result_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Test results saved to: {result_file}")


def main():
    """Main entry point"""
    print("=" * 70)
    print("🧪 Tool Registry Tests")
    print("=" * 70)
    print()

    results = []

    # Run tests
    results.append(
        generate_test_result("test_tool_registry_exists", test_tool_registry_exists())
    )
    results.append(
        generate_test_result(
            "test_tool_registry_structure", test_tool_registry_structure()
        )
    )
    results.append(
        generate_test_result("test_tools_registered", test_tools_registered())
    )
    results.append(
        generate_test_result(
            "test_tool_verification_status", test_tool_verification_status()
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
