#!/usr/bin/env python3
"""
Test Governance Closure
========================

Tests the governance closure specification and validation.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, '/workspace/ecosystem')
sys.path.insert(0, '/workspace')


def test_governance_closure_spec_exists():
    """Test that governance closure specification exists"""
    print("Testing governance closure spec exists...")
    
    spec_file = Path("/workspace/ecosystem/governance/closure/governance_closure_spec.yaml")
    
    if not spec_file.exists():
        print("  ❌ FAILED: Governance closure spec does not exist")
        return False
    
    print("  ✅ PASSED: Governance closure spec exists")
    return True


def test_governance_owner_defined():
    """Test that governance owner is defined"""
    print("Testing governance owner defined...")
    
    import yaml
    
    spec_file = Path("/workspace/ecosystem/governance/closure/governance_closure_spec.yaml")
    
    with open(spec_file, 'r') as f:
        spec = yaml.safe_load(f)
    
    if 'governance_owner' not in spec:
        print("  ❌ FAILED: Governance owner not defined in spec")
        return False
    
    owner = spec['governance_owner']
    if owner != 'IndestructibleAutoOps':
        print(f"  ⚠️  WARNING: Governance owner is '{owner}' (expected 'IndestructibleAutoOps')")
        return False
    
    print(f"  ✅ PASSED: Governance owner defined as '{owner}'")
    return True


def test_closure_conditions_defined():
    """Test that closure conditions are defined"""
    print("Testing closure conditions defined...")
    
    import yaml
    
    spec_file = Path("/workspace/ecosystem/governance/closure/governance_closure_spec.yaml")
    
    with open(spec_file, 'r') as f:
        spec = yaml.safe_load(f)
    
    if 'closure_conditions' not in spec:
        print("  ❌ FAILED: Closure conditions not defined")
        return False
    
    conditions = spec['closure_conditions']
    
    required_conditions = [
        'all_artifacts_have_canonical_hash',
        'all_hashes_are_reproducible',
        'all_complements_exist',
        'all_events_have_hash',
        'all_tools_registered',
        'all_tests_passed',
        'all_semantics_consistent',
        'all_evidence_canonicalized_and_sealed'
    ]
    
    missing_conditions = [c for c in required_conditions if c not in conditions]
    
    if len(missing_conditions) > 0:
        print(f"  ❌ FAILED: Missing closure conditions: {missing_conditions}")
        return False
    
    print(f"  ✅ PASSED: All {len(required_conditions)} closure conditions defined")
    return True


def test_closure_thresholds_defined():
    """Test that closure thresholds are defined"""
    print("Testing closure thresholds defined...")
    
    import yaml
    
    spec_file = Path("/workspace/ecosystem/governance/closure/governance_closure_spec.yaml")
    
    with open(spec_file, 'r') as f:
        spec = yaml.safe_load(f)
    
    if 'thresholds' not in spec:
        print("  ❌ FAILED: Closure thresholds not defined")
        return False
    
    thresholds = spec['thresholds']
    
    required_thresholds = ['diagnostic_score_min', 'artifact_hash_consistency', 'event_hash_coverage', 'test_pass_rate']
    
    missing_thresholds = [t for t in required_thresholds if t not in thresholds]
    
    if len(missing_thresholds) > 0:
        print(f"  ❌ FAILED: Missing thresholds: {missing_thresholds}")
        return False
    
    print(f"  ✅ PASSED: All {len(required_thresholds)} thresholds defined")
    return True


def generate_test_result(test_name: str, passed: bool):
    """Generate test result JSON"""
    import hashlib
    from datetime import datetime, timezone
    
    result = {
        "test": test_name,
        "status": "passed" if passed else "failed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_file": "tests/governance/test_governance_closure.py"
    }
    
    # Generate hash
    result_str = json.dumps(result, sort_keys=True)
    result["hash"] = f"sha256:{hashlib.sha256(result_str.encode()).hexdigest()}"
    
    return result


def save_test_results(results: list):
    """Save test results to file"""
    evidence_dir = Path("/workspace/ecosystem/.evidence/tests")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    result_file = evidence_dir / "test-governance-closure.json"
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Test results saved to: {result_file}")


def main():
    """Main entry point"""
    print("=" * 70)
    print("🧪 Governance Closure Tests")
    print("=" * 70)
    print()
    
    results = []
    
    # Run tests
    results.append(generate_test_result("test_governance_closure_spec_exists", test_governance_closure_spec_exists()))
    results.append(generate_test_result("test_governance_owner_defined", test_governance_owner_defined()))
    results.append(generate_test_result("test_closure_conditions_defined", test_closure_conditions_defined()))
    results.append(generate_test_result("test_closure_thresholds_defined", test_closure_thresholds_defined()))
    
    # Save results
    save_test_results(results)
    
    # Summary
    passed = sum(1 for r in results if r['status'] == 'passed')
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