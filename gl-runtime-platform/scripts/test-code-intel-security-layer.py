# @GL-governed
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Intelligence & Security Layer Test Suite
Version 21.0.0

This script performs comprehensive testing of the Code Intelligence & Security Layer
including all components: Capability Schema, Pattern Library, Generator Engine,
Evaluation Engine, Deployment Weaver, Evolution Engine, and integrations.
"""

import os
import sys
import json
import datetime
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

# ============================================================================
# Test Configuration
# ============================================================================

TEST_CONFIG = {
    "version": "21.0.0",
    "test_date": datetime.datetime.now().isoformat(),
    "workspace_root": "/workspace/gl-runtime-platform",
    "code_intel_layer": "code-intel-security-layer",
    "test_output_dir": "./test-reports",
    "test_scenarios": [
        "capability_schema",
        "pattern_library",
        "generator_engine",
        "evaluation_engine",
        "deployment_weaver",
        "evolution_engine",
        "v19_fabric_integration",
        "v20_continuum_integration"
    ]
}

# ============================================================================
# Test Result Classes
# ============================================================================

class TestCase:
    """Individual test case"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "pending"  # pending, running, passed, failed, skipped
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.duration_ms: float = 0.0
        self.error_message: Optional[str] = None
        self.assertions: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
    
    def start(self):
        """Start test execution"""
        self.status = "running"
        self.start_time = time.time()
    
    def pass_test(self, metrics: Optional[Dict[str, Any]] = None):
        """Mark test as passed"""
        self.status = "passed"
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        if metrics:
            self.metrics.update(metrics)
    
    def fail_test(self, error_message: str):
        """Mark test as failed"""
        self.status = "failed"
        self.error_message = error_message
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
    
    def skip_test(self, reason: str):
        """Skip test"""
        self.status = "skipped"
        self.error_message = reason
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "assertions": self.assertions,
            "metrics": self.metrics
        }

class TestSuite:
    """Test suite for a component"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.test_cases: List[TestCase] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.total_duration_ms: float = 0.0
    
    def add_test(self, test_case: TestCase):
        """Add test case to suite"""
        self.test_cases.append(test_case)
    
    def start(self):
        """Start test suite"""
        self.start_time = time.time()
    
    def finish(self):
        """Finish test suite"""
        self.end_time = time.time()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000
    
    def get_statistics(self) -> Dict[str, int]:
        """Get test statistics"""
        return {
            "total": len(self.test_cases),
            "passed": sum(1 for t in self.test_cases if t.status == "passed"),
            "failed": sum(1 for t in self.test_cases if t.status == "failed"),
            "skipped": sum(1 for t in self.test_cases if t.status == "skipped")
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "statistics": self.get_statistics(),
            "duration_ms": self.total_duration_ms,
            "test_cases": [t.to_dict() for t in self.test_cases]
        }

# ============================================================================
# Code Intelligence & Security Layer Tester
# ============================================================================

class CodeIntelTester:
    """Main tester for Code Intelligence & Security Layer"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.test_suites: List[TestSuite] = []
        self.output_dir = Path(config["test_output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🧪 Code Intelligence & Security Layer Tester v{config['version']}")
        print(f"📁 Workspace: {config['workspace_root']}")
        print(f"📊 Output: {self.output_dir}")
        print()
    
    # ========================================================================
    # Test Methods
    # ========================================================================
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites"""
        print("🚀 Starting comprehensive testing...")
        print()
        
        # Run each test suite
        for scenario in self.config["test_scenarios"]:
            test_method = getattr(self, f"test_{scenario}", None)
            if test_method:
                test_method()
        
        # Generate report
        report = self.generate_test_report()
        self.save_test_report(report)
        
        # Print summary
        self.print_summary(report)
        
        return report
    
    def test_capability_schema(self):
        """Test Capability Schema component"""
        suite = TestSuite(
            "Capability Schema",
            "Test capability description language and generation"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing Capability Schema")
        print("=" * 80)
        
        # Test 1: Check capability-schema directory exists
        test1 = TestCase(
            "Directory Exists",
            "Verify capability-schema directory exists"
        )
        test1.start()
        
        schema_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "capability-schema"
        
        if schema_dir.exists():
            test1.pass_test({
                "directory_path": str(schema_dir),
                "directory_exists": True
            })
            print("✅ Test 1: Directory exists")
        else:
            test1.fail_test(f"Directory not found: {schema_dir}")
            print("❌ Test 1: Directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check capability schema files
        test2 = TestCase(
            "Schema Files",
            "Verify required schema files exist"
        )
        test2.start()
        
        required_files = [
            "capability-definition-language.md",
            "capability-templates.yaml",
            "capability-examples.json"
        ]
        
        found_files = []
        for file in required_files:
            file_path = schema_dir / file
            if file_path.exists():
                found_files.append(file)
        
        if len(found_files) == len(required_files):
            test2.pass_test({
                "required_files": required_files,
                "found_files": found_files,
                "all_present": True
            })
            print("✅ Test 2: All schema files present")
        else:
            test2.fail_test(f"Missing files: {set(required_files) - set(found_files)}")
            print("❌ Test 2: Some schema files missing")
        
        suite.add_test(test2)
        
        # Test 3: Validate schema structure
        test3 = TestCase(
            "Schema Structure",
            "Validate schema structure and content"
        )
        test3.start()
        
        try:
            examples_file = schema_dir / "capability-examples.json"
            if examples_file.exists():
                with open(examples_file, 'r') as f:
                    examples = json.load(f)
                
                if isinstance(examples, list) and len(examples) > 0:
                    test3.pass_test({
                        "total_examples": len(examples),
                        "first_example_id": examples[0].get("id", "N/A"),
                        "structure_valid": True
                    })
                    print(f"✅ Test 3: Schema structure valid ({len(examples)} examples)")
                else:
                    test3.fail_test("Invalid examples structure")
                    print("❌ Test 3: Invalid schema structure")
            else:
                test3.skip_test("Examples file not found")
                print("⚠️  Test 3: Skipped (file not found)")
        except Exception as e:
            test3.fail_test(str(e))
            print(f"❌ Test 3: Error - {e}")
        
        suite.add_test(test3)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_pattern_library(self):
        """Test Pattern Library component"""
        suite = TestSuite(
            "Pattern Library",
            "Test security, performance, and architecture patterns"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing Pattern Library")
        print("=" * 80)
        
        # Test 1: Check pattern-library directory
        test1 = TestCase(
            "Directory Exists",
            "Verify pattern-library directory exists"
        )
        test1.start()
        
        pattern_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "pattern-library"
        
        if pattern_dir.exists():
            test1.pass_test({"directory_path": str(pattern_dir)})
            print("✅ Test 1: Pattern library directory exists")
        else:
            test1.fail_test(f"Directory not found: {pattern_dir}")
            print("❌ Test 1: Pattern library directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check pattern categories
        test2 = TestCase(
            "Pattern Categories",
            "Verify all pattern categories exist"
        )
        test2.start()
        
        required_categories = [
            "security-patterns",
            "performance-patterns",
            "architecture-patterns"
        ]
        
        found_categories = []
        for category in required_categories:
            cat_path = pattern_dir / category
            if cat_path.exists():
                found_categories.append(category)
        
        if len(found_categories) == len(required_categories):
            test2.pass_test({
                "required_categories": required_categories,
                "found_categories": found_categories,
                "all_present": True
            })
            print("✅ Test 2: All pattern categories present")
        else:
            test2.fail_test(f"Missing categories: {set(required_categories) - set(found_categories)}")
            print("❌ Test 2: Some pattern categories missing")
        
        suite.add_test(test2)
        
        # Test 3: Count patterns
        test3 = TestCase(
            "Pattern Count",
            "Count and validate patterns"
        )
        test3.start()
        
        total_patterns = 0
        pattern_details = {}
        
        for category in required_categories:
            cat_path = pattern_dir / category
            if cat_path.exists():
                patterns = list(cat_path.glob("*.md")) + list(cat_path.glob("*.yaml"))
                pattern_details[category] = len(patterns)
                total_patterns += len(patterns)
        
        if total_patterns > 0:
            test3.pass_test({
                "total_patterns": total_patterns,
                "pattern_details": pattern_details
            })
            print(f"✅ Test 3: Found {total_patterns} patterns")
            for cat, count in pattern_details.items():
                print(f"   - {cat}: {count} patterns")
        else:
            test3.fail_test("No patterns found")
            print("❌ Test 3: No patterns found")
        
        suite.add_test(test3)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_generator_engine(self):
        """Test Generator Engine component"""
        suite = TestSuite(
            "Generator Engine",
            "Test capability generation engine"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing Generator Engine")
        print("=" * 80)
        
        # Test 1: Check generator-engine directory
        test1 = TestCase(
            "Directory Exists",
            "Verify generator-engine directory exists"
        )
        test1.start()
        
        generator_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "generator-engine"
        
        if generator_dir.exists():
            test1.pass_test({"directory_path": str(generator_dir)})
            print("✅ Test 1: Generator engine directory exists")
        else:
            test1.fail_test(f"Directory not found: {generator_dir}")
            print("❌ Test 1: Generator engine directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check generator components
        test2 = TestCase(
            "Generator Components",
            "Verify generator engine components"
        )
        test2.start()
        
        required_components = [
            "capability-generator.py",
            "pattern-matcher.py",
            "template-engine.py"
        ]
        
        found_components = []
        for component in required_components:
            comp_path = generator_dir / component
            if comp_path.exists():
                found_components.append(component)
        
        if len(found_components) == len(required_components):
            test2.pass_test({
                "required_components": required_components,
                "found_components": found_components,
                "all_present": True
            })
            print("✅ Test 2: All generator components present")
        else:
            test2.fail_test(f"Missing components: {set(required_components) - set(found_components)}")
            print("❌ Test 2: Some generator components missing")
        
        suite.add_test(test2)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_evaluation_engine(self):
        """Test Evaluation Engine component"""
        suite = TestSuite(
            "Evaluation Engine",
            "Test verification and evaluation layer"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing Evaluation Engine")
        print("=" * 80)
        
        # Test 1: Check evaluation-engine directory
        test1 = TestCase(
            "Directory Exists",
            "Verify evaluation-engine directory exists"
        )
        test1.start()
        
        eval_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "evaluation-engine"
        
        if eval_dir.exists():
            test1.pass_test({"directory_path": str(eval_dir)})
            print("✅ Test 1: Evaluation engine directory exists")
        else:
            test1.fail_test(f"Directory not found: {eval_dir}")
            print("❌ Test 1: Evaluation engine directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check evaluation criteria
        test2 = TestCase(
            "Evaluation Criteria",
            "Verify evaluation criteria definitions"
        )
        test2.start()
        
        criteria_file = eval_dir / "evaluation-criteria.yaml"
        
        if criteria_file.exists():
            test2.pass_test({
                "criteria_file": str(criteria_file),
                "exists": True
            })
            print("✅ Test 2: Evaluation criteria file exists")
        else:
            test2.fail_test("Evaluation criteria file not found")
            print("❌ Test 2: Evaluation criteria file not found")
        
        suite.add_test(test2)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_deployment_weaver(self):
        """Test Deployment Weaver component"""
        suite = TestSuite(
            "Deployment Weaver",
            "Test CLI/IDE/Web/CI/CD integration"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing Deployment Weaver")
        print("=" * 80)
        
        # Test 1: Check deployment-weaver directory
        test1 = TestCase(
            "Directory Exists",
            "Verify deployment-weaver directory exists"
        )
        test1.start()
        
        deploy_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "deployment-weaver"
        
        if deploy_dir.exists():
            test1.pass_test({"directory_path": str(deploy_dir)})
            print("✅ Test 1: Deployment weaver directory exists")
        else:
            test1.fail_test(f"Directory not found: {deploy_dir}")
            print("❌ Test 1: Deployment weaver directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check deployment platforms
        test2 = TestCase(
            "Deployment Platforms",
            "Verify all deployment platforms are configured"
        )
        test2.start()
        
        required_platforms = [
            "cli-generator",
            "ide-extension",
            "web-console",
            "ci-cd-integration"
        ]
        
        found_platforms = []
        for platform in required_platforms:
            platform_path = deploy_dir / platform
            if platform_path.exists():
                found_platforms.append(platform)
        
        if len(found_platforms) == len(required_platforms):
            test2.pass_test({
                "required_platforms": required_platforms,
                "found_platforms": found_platforms,
                "all_present": True
            })
            print("✅ Test 2: All deployment platforms configured")
        else:
            test2.fail_test(f"Missing platforms: {set(required_platforms) - set(found_platforms)}")
            print("❌ Test 2: Some deployment platforms missing")
        
        suite.add_test(test2)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_evolution_engine(self):
        """Test Evolution Engine component"""
        suite = TestSuite(
            "Evolution Engine",
            "Test self-evolving system"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing Evolution Engine")
        print("=" * 80)
        
        # Test 1: Check evolution-engine directory
        test1 = TestCase(
            "Directory Exists",
            "Verify evolution-engine directory exists"
        )
        test1.start()
        
        evolution_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "evolution-engine"
        
        if evolution_dir.exists():
            test1.pass_test({"directory_path": str(evolution_dir)})
            print("✅ Test 1: Evolution engine directory exists")
        else:
            test1.fail_test(f"Directory not found: {evolution_dir}")
            print("❌ Test 1: Evolution engine directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check evolution mechanisms
        test2 = TestCase(
            "Evolution Mechanisms",
            "Verify evolution mechanisms are defined"
        )
        test2.start()
        
        evolution_files = [
            "usage-tracker.py",
            "adaptation-engine.py",
            "self-optimizer.py"
        ]
        
        found_files = []
        for file in evolution_files:
            file_path = evolution_dir / file
            if file_path.exists():
                found_files.append(file)
        
        if len(found_files) >= 2:  # At least 2 of 3
            test2.pass_test({
                "required_files": evolution_files,
                "found_files": found_files,
                "minimum_met": True
            })
            print(f"✅ Test 2: Evolution mechanisms defined ({len(found_files)}/3)")
        else:
            test2.fail_test(f"Insufficient evolution mechanisms: {len(found_files)}/3")
            print(f"❌ Test 2: Insufficient evolution mechanisms ({len(found_files)}/3)")
        
        suite.add_test(test2)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_v19_fabric_integration(self):
        """Test V19 Fabric integration"""
        suite = TestSuite(
            "V19 Fabric Integration",
            "Test integration with Unified Intelligence Fabric"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing V19 Fabric Integration")
        print("=" * 80)
        
        # Test 1: Check integration directory
        test1 = TestCase(
            "Integration Directory",
            "Verify V19 fabric integration directory exists"
        )
        test1.start()
        
        integration_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "integrations" / "v19-fabric"
        
        if integration_dir.exists():
            test1.pass_test({"directory_path": str(integration_dir)})
            print("✅ Test 1: V19 fabric integration directory exists")
        else:
            test1.fail_test(f"Directory not found: {integration_dir}")
            print("❌ Test 1: V19 fabric integration directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check integration files
        test2 = TestCase(
            "Integration Files",
            "Verify integration files are present"
        )
        test2.start()
        
        integration_files = [
            "fabric-connector.py",
            "fabric-adapter.py"
        ]
        
        found_files = []
        for file in integration_files:
            file_path = integration_dir / file
            if file_path.exists():
                found_files.append(file)
        
        if len(found_files) >= 1:
            test2.pass_test({
                "required_files": integration_files,
                "found_files": found_files,
                "minimum_met": True
            })
            print(f"✅ Test 2: Integration files present ({len(found_files)}/2)")
        else:
            test2.fail_test("No integration files found")
            print("❌ Test 2: No integration files found")
        
        suite.add_test(test2)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    def test_v20_continuum_integration(self):
        """Test V20 Continuum integration"""
        suite = TestSuite(
            "V20 Continuum Integration",
            "Test integration with Infinite Learning Continuum"
        )
        suite.start()
        
        print("=" * 80)
        print("Testing V20 Continuum Integration")
        print("=" * 80)
        
        # Test 1: Check integration directory
        test1 = TestCase(
            "Integration Directory",
            "Verify V20 continuum integration directory exists"
        )
        test1.start()
        
        integration_dir = Path(self.config["workspace_root"]) / self.config["code_intel_layer"] / "integrations" / "v20-continuum"
        
        if integration_dir.exists():
            test1.pass_test({"directory_path": str(integration_dir)})
            print("✅ Test 1: V20 continuum integration directory exists")
        else:
            test1.fail_test(f"Directory not found: {integration_dir}")
            print("❌ Test 1: V20 continuum integration directory not found")
        
        suite.add_test(test1)
        
        # Test 2: Check integration files
        test2 = TestCase(
            "Integration Files",
            "Verify continuum integration files"
        )
        test2.start()
        
        integration_files = [
            "continuum-connector.py",
            "learning-adapter.py"
        ]
        
        found_files = []
        for file in integration_files:
            file_path = integration_dir / file
            if file_path.exists():
                found_files.append(file)
        
        if len(found_files) >= 1:
            test2.pass_test({
                "required_files": integration_files,
                "found_files": found_files,
                "minimum_met": True
            })
            print(f"✅ Test 2: Integration files present ({len(found_files)}/2)")
        else:
            test2.fail_test("No integration files found")
            print("❌ Test 2: No integration files found")
        
        suite.add_test(test2)
        
        suite.finish()
        self.test_suites.append(suite)
        print()
    
    # ========================================================================
    # Report Generation
    # ========================================================================
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = sum(suite.get_statistics()["total"] for suite in self.test_suites)
        total_passed = sum(suite.get_statistics()["passed"] for suite in self.test_suites)
        total_failed = sum(suite.get_statistics()["failed"] for suite in self.test_suites)
        total_skipped = sum(suite.get_statistics()["skipped"] for suite in self.test_suites)
        
        total_duration = sum(suite.total_duration_ms for suite in self.test_suites)
        
        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "test_metadata": {
                "version": self.config["version"],
                "test_date": self.config["test_date"],
                "tester": "CodeIntelTester v21.0.0",
                "workspace_root": self.config["workspace_root"]
            },
            "summary": {
                "total_tests": total_tests,
                "total_passed": total_passed,
                "total_failed": total_failed,
                "total_skipped": total_skipped,
                "pass_rate": round(pass_rate, 2),
                "total_duration_ms": round(total_duration, 2),
                "total_duration_seconds": round(total_duration / 1000, 2)
            },
            "test_suites": [suite.to_dict() for suite in self.test_suites],
            "overall_status": "PASSED" if total_failed == 0 else "FAILED"
        }
    
    def save_test_report(self, report: Dict[str, Any]):
        """Save test report to file"""
        report_path = self.output_dir / "code-intel-test-report.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Test report saved to: {report_path}")
        
        # Also save markdown summary
        self.save_markdown_summary(report)
    
    def save_markdown_summary(self, report: Dict[str, Any]):
        """Save markdown summary"""
        summary_path = self.output_dir / "test-summary.md"
        
        md_content = f"""# Code Intelligence & Security Layer Test Report

**Version:** {report['test_metadata']['version']}  
**Date:** {report['test_metadata']['test_date']}  
**Tester:** {report['test_metadata']['tester']}

## Executive Summary

- **Overall Status:** {'✅ PASSED' if report['overall_status'] == 'PASSED' else '❌ FAILED'}
- **Total Tests:** {report['summary']['total_tests']}
- **Passed:** {report['summary']['total_passed']}
- **Failed:** {report['summary']['total_failed']}
- **Skipped:** {report['summary']['total_skipped']}
- **Pass Rate:** {report['summary']['pass_rate']}%
- **Total Duration:** {report['summary']['total_duration_seconds']}s

## Test Suite Results

"""
        
        for suite in report['test_suites']:
            status_icon = "✅" if suite['statistics']['failed'] == 0 else "❌"
            md_content += f"""
### {status_icon} {suite['name']}

**Description:** {suite['description']}  
**Duration:** {suite['duration_ms'] / 1000:.2f}s  
**Tests:** {suite['statistics']['passed']}/{suite['statistics']['total']} passed

"""
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📝 Summary saved to: {summary_path}")
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary"""
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print()
        print(f"Overall Status: {'✅ PASSED' if report['overall_status'] == 'PASSED' else '❌ FAILED'}")
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['total_passed']}")
        print(f"Failed: {report['summary']['total_failed']}")
        print(f"Skipped: {report['summary']['total_skipped']}")
        print(f"Pass Rate: {report['summary']['pass_rate']}%")
        print(f"Total Duration: {report['summary']['total_duration_seconds']}s")
        print()
        
        for suite in report['test_suites']:
            stats = suite['statistics']
            status = "✅ PASS" if stats['failed'] == 0 else "❌ FAIL"
            print(f"{status} {suite['name']}: {stats['passed']}/{stats['total']} tests passed")
        
        print()
        print("=" * 80)

# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    tester = CodeIntelTester(TEST_CONFIG)
    report = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if report['overall_status'] == 'PASSED' else 1)