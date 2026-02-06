#!/usr/bin/env python3
"""
Semantic Defense System Test Runner
Era-1 Test Framework
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def run_pytest(test_path: str = None, verbose: bool = True, html_report: bool = False) -> int:
    """Run pytest and return exit code"""
    cmd = ["python", "-m", "pytest"]
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("ecosystem/tests/semantic-defense")
    
    if verbose:
        cmd.append("-v")
    
    if html_report:
        cmd.extend(["--html", "test-report.html", "--self-contained-html"])
    
    cmd.extend(["--tb=short", "--color=yes"])
    
    print("=" * 70)
    print("🛡️  Era-1 Semantic Defense System Test Suite")
    print("=" * 70)
    print(f"\nRunning: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_specific_test(test_case: str) -> int:
    """Run a specific test case"""
    return run_pytest(test_path=test_case)


def generate_test_summary() -> Dict[str, Any]:
    """Generate test summary report"""
    # This would parse test results and generate summary
    # For now, return placeholder
    return {
        "test_run": datetime.utcnow().isoformat() + "Z",
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "violations_detected": 0,
        "complements_generated": 0
    }


def print_summary():
    """Print test summary"""
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    
    summary = generate_test_summary()
    
    print(f"\nTotal Tests: {summary['total_tests']}")
    print(f"✅ Passed: {summary['passed']}")
    print(f"❌ Failed: {summary['failed']}")
    print(f"⏭️  Skipped: {summary['skipped']}")
    print(f"⚠️  Violations Detected: {summary['violations_detected']}")
    print(f"📦 Complements Generated: {summary['complements_generated']}")
    print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Era-1 Semantic Defense System Test Runner"
    )
    parser.add_argument(
        "--test",
        help="Run specific test case (e.g., test-semantic-corruption/test_semantic_corruption.py::TestSemanticCorruption::test_tc_1_1)"
    )
    parser.add_argument(
        "--category",
        help="Run specific test category (e.g., test_semantic_corruption)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Run tests quietly (minimal output)"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report"
    )
    
    args = parser.parse_args()
    
    # Change to workspace directory
    import os
    os.chdir("/workspace")
    
    # Run tests
    if args.test:
        exit_code = run_specific_test(args.test)
    elif args.category:
        exit_code = run_pytest(
            test_path=f"ecosystem/tests/semantic-defense/{args.category}",
            verbose=not args.quiet,
            html_report=args.html
        )
    else:
        exit_code = run_pytest(verbose=not args.quiet, html_report=args.html)
    
    # Print summary
    if not args.quiet:
        print_summary()
    
    # Exit with appropriate code
    if exit_code == 0:
        print("\n✅ All semantic defense tests passed!")
        print("   Era-1 is secure and ready for sealing.")
    else:
        print("\n❌ Semantic defense tests failed!")
        print("   Please review violations and generate complements.")
        print("   Era-1 sealing is blocked until all critical tests pass.")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()