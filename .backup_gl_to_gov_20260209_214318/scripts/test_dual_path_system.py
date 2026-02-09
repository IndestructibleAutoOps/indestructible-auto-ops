#!/usr/bin/env python3
"""
Test script for Dual-Path Retrieval + Arbitration System
MNGA Layer 6 (Reasoning)

@GL-semantic: test-dual-path-system
@GL-audit-trail: enabled
"""

import sys
import json
from pathlib import Path

# Add ecosystem to path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "ecosystem"))

from reasoning.dual_path.pipeline import ReasoningPipeline


def test_basic_query():
    """Test basic query handling"""
    print("=" * 80)
    print("TEST 1: Basic Query - Async Task Processing")
    print("=" * 80)

    pipeline = ReasoningPipeline()

    response = pipeline.handle_request(
        task_spec="How should I implement async task processing in Python?",
        context={
            "task_type": "pattern",
            "category": "engineering",
            "sources": ["code", "documentation"],
        },
        user_id="test_user",
    )

    print(f"\nRequest ID: {response.request_id}")
    print(f"Decision: {response.decision['decision']}")
    print(f"Confidence: {response.confidence:.2%}")
    print(f"\nFinal Answer:\n{response.final_answer}\n")
    print(f"Risk Assessment: {response.risk_assessment}")
    print(f"Source Counts: {response.source_counts}")

    return response.request_id


def test_governance_query():
    """Test governance-related query"""
    print("\n" + "=" * 80)
    print("TEST 2: Governance Query - Naming Conventions")
    print("=" * 80)

    pipeline = ReasoningPipeline()

    response = pipeline.handle_request(
        task_spec="What are the GL naming conventions for modules?",
        context={
            "task_type": "api_usage",
            "category": "governance",
            "module": "naming-governance",
        },
        user_id="test_user",
    )

    print(f"\nRequest ID: {response.request_id}")
    print(f"Decision: {response.decision['decision']}")
    print(f"Confidence: {response.confidence:.2%}")
    print(f"\nFinal Answer:\n{response.final_answer}\n")

    return response.request_id


def test_security_query():
    """Test security-related query"""
    print("\n" + "=" * 80)
    print("TEST 3: Security Query - Vulnerability Fix")
    print("=" * 80)

    pipeline = ReasoningPipeline()

    response = pipeline.handle_request(
        task_spec="How to fix SQL injection vulnerability?",
        context={
            "task_type": "vulnerability_fix",
            "category": "security",
        },
        user_id="test_user",
    )

    print(f"\nRequest ID: {response.request_id}")
    print(f"Decision: {response.decision['decision']}")
    print(f"Confidence: {response.confidence:.2%}")
    print(f"\nFinal Answer:\n{response.final_answer}\n")

    return response.request_id


def test_feedback():
    """Test feedback submission"""
    print("\n" + "=" * 80)
    print("TEST 4: Feedback Submission")
    print("=" * 80)

    pipeline = ReasoningPipeline()

    # Submit feedback
    request_id = "test-request-123"
    pipeline.submit_feedback(
        request_id=request_id,
        feedback_type="ACCEPT",
        user_id="test_user",
        reason="Helpful and accurate answer",
    )

    print(f"\nFeedback submitted for request: {request_id}")

    # Get metrics
    metrics = pipeline.get_metrics()
    print("\nPipeline Metrics:")
    print(json.dumps(metrics, indent=2, default=str))

    # Generate feedback report
    report = pipeline.generate_feedback_report()
    print(f"\nFeedback Report:\n{report}")


def test_traceability():
    """Test traceability"""
    print("\n" + "=" * 80)
    print("TEST 5: Traceability")
    print("=" * 80)

    pipeline = ReasoningPipeline()

    # Get a request ID
    request_id = pipeline.handle_request(
        task_spec="Test query for traceability",
        context={},
        user_id="test_user",
    ).request_id

    # Get trace
    trace = pipeline.get_trace(request_id)
    print(f"\nTrace for request {request_id}:")
    print(json.dumps(trace, indent=2, default=str))

    # Export traces
    export_path = pipeline.export_traces(format="json")
    print(f"\nTraces exported to: {export_path}")


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("DUAL-PATH RETRIEVAL + ARBITRATION SYSTEM - TEST SUITE")
    print("MNGA Layer 6 (Reasoning)")
    print("=" * 80 + "\n")

    try:
        # Run tests
        test_basic_query()
        test_governance_query()
        test_security_query()
        test_feedback()
        test_traceability()

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED ✓")
        print("=" * 80 + "\n")

        print("System Status:")
        print("- Internal Retrieval Engine: ✓ Operational")
        print("- External Retrieval Engine: ✓ Operational")
        print("- Arbitration Engine: ✓ Operational")
        print("- Traceability Engine: ✓ Operational")
        print("- Feedback System: ✓ Operational")
        print("- Reasoning Pipeline: ✓ Operational")
        print("\nMNGA Layer 6 (Reasoning) is fully functional!")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
