"""
Self-Healing Replayability Demo
Demonstrates the complete replayability workflow with sample decisions.
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Add ecosystem to path
sys.path.insert(0, "/workspace")

from ecosystem.engines.selfhealing.replay_engine import ReplayEngine


def create_sample_decision_artifacts(engine: ReplayEngine, decision_id: str):
    """Create sample decision artifacts for testing"""

    # Import test helper
    sys.path.insert(0, "/workspace/ecosystem/tests/selfhealing")
    from test_replayability import SelfHealingTestHelper

    # Create decision
    decision = SelfHealingTestHelper.create_sample_decision(decision_id)

    # Save decision artifact
    decision_path = os.path.join(engine.decisions_root, f"{decision_id}.json")
    with open(decision_path, "w") as f:
        json.dump(decision, f, indent=2)

    # Create and save input snapshots
    inputs = SelfHealingTestHelper.create_sample_input_snapshot(decision_id)

    metrics_path = os.path.join(engine.snapshots_root, "metrics", f"{decision_id}.json")
    with open(metrics_path, "w") as f:
        json.dump(inputs["metrics"], f, indent=2)

    logs_path = os.path.join(engine.snapshots_root, "logs", f"{decision_id}.json")
    with open(logs_path, "w") as f:
        json.dump(inputs["logs"], f, indent=2)

    topology_path = os.path.join(
        engine.snapshots_root, "topology", f"{decision_id}.json"
    )
    with open(topology_path, "w") as f:
        json.dump(inputs["topology"], f, indent=2)

    alerts_path = os.path.join(engine.snapshots_root, "alerts", f"{decision_id}.json")
    with open(alerts_path, "w") as f:
        json.dump(inputs["alerts"], f, indent=2)

    # Create and save execution trace
    trace = SelfHealingTestHelper.create_sample_execution_trace(decision_id)
    trace_path = os.path.join(engine.traces_root, f"{decision_id}.json")
    with open(trace_path, "w") as f:
        json.dump(trace, f, indent=2)

    return decision


def main():
    print("=" * 80)
    print("🧪 Self-Healing Replayability Demonstration")
    print("=" * 80)
    print()

    # Initialize replay engine
    engine = ReplayEngine(workspace_root="/workspace")

    # Create sample decision ID
    import uuid

    decision_id = str(uuid.uuid4())

    print(f"📝 Creating sample decision artifacts for {decision_id}...")
    decision = create_sample_decision_artifacts(engine, decision_id)
    print(f"✅ Decision artifacts created")
    print(f"   - Decision: {engine.decisions_root}/{decision_id}.json")
    print(f"   - Input snapshots: {engine.snapshots_root}/*/{decision_id}.json")
    print(f"   - Execution trace: {engine.traces_root}/{decision_id}.json")
    print()

    # Replay decision
    print(f"🔄 Replaying decision {decision_id}...")
    replay_result = engine.replay_decision(decision_id)
    print(f"✅ Replay completed")
    print(f"   - Output action: {replay_result.output_action}")
    print(f"   - Duration: {replay_result.duration_ms:.2f}ms")
    print(f"   - Canonical hash: {replay_result.canonical_hash}")
    print()

    # Verify replay
    print(f"🔍 Verifying replay matches original...")
    verification = engine.verify_replay(decision_id)
    print(f"✅ Verification completed")
    print(f"   - Output match: {verification.output_match}")
    print(f"   - Trace match: {verification.trace_match}")
    print(f"   - Parameters match: {verification.parameters_match}")
    print(f"   - Duration: {verification.duration_ms:.2f}ms")
    print()

    # Run complete test suite
    print(f"🧪 Running complete test suite...")
    test_result = engine.generate_test_result(decision_id)
    print(f"✅ Test suite completed")
    print(f"   - Overall status: {test_result['summary']['overall_status']}")
    print(
        f"   - Tests passed: {test_result['summary']['passed']}/{test_result['summary']['total_tests']}"
    )
    print(f"   - Total duration: {test_result['summary']['total_duration_ms']:.2f}ms")
    print(
        f"   - Test result saved: {engine.tests_root}/testreplayability_{decision_id}.json"
    )
    print()

    # Display individual test results
    print("📊 Individual Test Results:")
    print("-" * 80)
    for test_name, test_data in test_result["tests"].items():
        status_emoji = "✅" if test_data["status"] == "passed" else "❌"
        print(f"{status_emoji} {test_name}:")
        print(f"   Status: {test_data['status']}")
        print(f"   Duration: {test_data['duration_ms']:.2f}ms")
        if "output_match" in test_data:
            print(f"   Output match: {test_data['output_match']}")
        if "trace_match" in test_data:
            print(f"   Trace match: {test_data['trace_match']}")
        if "semantic_drift" in test_data:
            print(f"   Semantic drift: {test_data['semantic_drift']}")
        if "order_independence" in test_data:
            print(f"   Order independence: {test_data['order_independence']}")
        if "determinism" in test_data:
            print(f"   Determinism: {test_data['determinism']}%")
    print()

    print("=" * 80)
    print("✅ Self-Healing Replayability Demonstration Complete")
    print("=" * 80)
    print()
    print("📁 Generated Artifacts:")
    print(f"   - Decision: {engine.decisions_root}/{decision_id}.json")
    print(f"   - Input snapshots: {engine.snapshots_root}/*/{decision_id}.json")
    print(f"   - Execution trace: {engine.traces_root}/{decision_id}.json")
    print(f"   - Test result: {engine.tests_root}/testreplayability_{decision_id}.json")
    print()
    print("🔐 Hash Verification:")
    print(f"   - Decision hash: {decision['canonical_hash']}")
    print(f"   - Replay hash: {replay_result.canonical_hash}")
    print(f"   - Test result hash: {test_result['canonical_hash']}")
    print()


if __name__ == "__main__":
    main()
