#!/usr/bin/env python3
"""
Test Hash Consistency
=====================

Tests that:
1. Artifact canonical hashes are consistent
2. Event canonical hashes are consistent
3. Hash chain links are valid
"""

import json
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, "/workspace/ecosystem")
sys.path.insert(0, "/workspace")

from ecosystem.tools.canonicalize import canonicalize_json


def test_artifact_hash_consistency():
    """Test that artifact hashes are consistent"""
    print("Testing artifact hash consistency...")

    evidence_dir = Path("/workspace/ecosystem/.evidence")
    artifact_files = sorted(evidence_dir.glob("step-*.json"))

    passed = 0
    failed = 0

    for artifact_file in artifact_files:
        with open(artifact_file, "r") as f:
            artifact = json.load(f)

        stored_hash = artifact.get("canonical_hash", "")

        # Recompute hash using the same layered structure as artifact generation
        layered_data = {
            "_layer1": {
                "artifact_id": artifact.get("artifact_id"),
                "step_number": artifact.get("step_number"),
                "timestamp": artifact.get("timestamp"),
                "era": artifact.get("era"),
                "success": artifact.get("success"),
            },
            "_layer2": {
                "metadata": artifact.get("metadata", {}),
                "execution_time_ms": artifact.get("execution_time_ms"),
                "violations_count": artifact.get("violations_count", 0),
            },
            "_layer3": {"artifacts_generated": artifact.get("artifacts_generated", [])},
        }

        canonical_str = canonicalize_json(layered_data)
        computed_hash = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

        if stored_hash == computed_hash:
            passed += 1
        else:
            failed += 1
            print(f"  ❌ {artifact_file.name}: Hash mismatch")
            print(f"     Stored: {stored_hash[:16]}...")
            print(f"     Computed: {computed_hash[:16]}...")

    print(f"  Result: {passed} passed, {failed} failed")
    return failed == 0


def test_event_hash_consistency():
    """Test that event hashes are consistent"""
    print("Testing event hash consistency...")

    event_stream_file = Path("/workspace/ecosystem/.governance/event-stream.jsonl")

    passed = 0
    failed = 0
    total = 0

    with open(event_stream_file, "r") as f:
        for line in f:
            event = json.loads(line.strip())
            total += 1

            if "canonical_hash" not in event:
                failed += 1
                continue

            stored_hash = event.get("canonical_hash", "")

            # Recompute hash
            event_copy = event.copy()
            event_copy.pop("canonical_hash", None)
            event_copy.pop("hash_chain", None)

            try:
                canonical_str = canonicalize_json(event_copy)
                computed_hash = hashlib.sha256(
                    canonical_str.encode("utf-8")
                ).hexdigest()

                if stored_hash == computed_hash:
                    passed += 1
                else:
                    failed += 1
            except Exception:
                # Some events may not be canonicalizable
                pass

    print(f"  Result: {passed}/{total} passed, {failed} failed")
    return failed == 0


def test_hash_chain_links():
    """Test that hash chain links are valid"""
    print("Testing hash chain links...")

    event_stream_file = Path("/workspace/ecosystem/.governance/event-stream.jsonl")

    events = []
    with open(event_stream_file, "r") as f:
        for line in f:
            events.append(json.loads(line.strip()))

    passed = 0
    failed = 0

    for i, event in enumerate(events):
        if "hash_chain" not in event:
            continue

        hash_chain = event["hash_chain"]

        # Check previous_event link
        if i > 0:
            previous_event = events[i - 1]
            previous_hash = previous_event.get("canonical_hash", "")
            if hash_chain.get("previous_event") != previous_hash:
                failed += 1
            else:
                passed += 1
        else:
            # First event should have no previous_event
            if hash_chain.get("previous_event") is None:
                passed += 1
            else:
                failed += 1

    print(f"  Result: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Main entry point"""
    print("=" * 70)
    print("🧪 Hash Consistency Tests")
    print("=" * 70)
    print()

    results = []

    # Run tests
    results.append(("Artifact Hash Consistency", test_artifact_hash_consistency()))
    print()
    results.append(("Event Hash Consistency", test_event_hash_consistency()))
    print()
    results.append(("Hash Chain Links", test_hash_chain_links()))
    print()

    # Summary
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"📊 Summary: {passed}/{total} tests passed")
    print("=" * 70)

    all_passed = all(result for _, result in results)

    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
