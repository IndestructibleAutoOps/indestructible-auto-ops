#!/usr/bin/env python3
"""
Unit tests for GovNamingEnforcer
"""

import tempfile
import unittest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "enforcement"))

from gov_naming_enforcer import GovNamingEnforcer


class TestGovNamingEnforcer(unittest.TestCase):
    """Test cases for GovNamingEnforcer"""

    def setUp(self):
        """Create a temporary directory for testing"""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)
        self.enforcer = GovNamingEnforcer(str(self.test_path))

    def tearDown(self):
        """Clean up temporary directory"""
        self.test_dir.cleanup()

    def test_deprecated_prefix_ng_detection(self):
        """Test detection of deprecated ng_ prefix"""
        test_file = self.test_path / "ng_test.py"
        test_file.write_text("# test file")
        
        violation = self.enforcer.check_file_naming(test_file)
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation["violation_id"], "NAMING-DEPRECATED-001")
        self.assertEqual(violation["severity"], "BLOCKER")
        self.assertIn("ng_", violation["description"])

    def test_deprecated_prefix_gl_detection(self):
        """Test detection of deprecated gl_ prefix"""
        test_file = self.test_path / "gl_test.yaml"
        test_file.write_text("test: value")
        
        violation = self.enforcer.check_file_naming(test_file)
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation["violation_id"], "NAMING-DEPRECATED-001")
        self.assertEqual(violation["severity"], "BLOCKER")
        self.assertIn("gl_", violation["description"])

    def test_valid_gov_prefix_file(self):
        """Test that files with gov_ prefix pass validation"""
        test_file = self.test_path / "gov_test.py"
        test_file.write_text("# test file")
        
        violation = self.enforcer.check_file_naming(test_file)
        
        self.assertIsNone(violation)

    def test_valid_gov_naming_prefix_file(self):
        """Test that files with gov_naming_ prefix pass validation"""
        test_file = self.test_path / "gov_naming_test.yaml"
        test_file.write_text("test: value")
        
        violation = self.enforcer.check_file_naming(test_file)
        
        self.assertIsNone(violation)

    def test_invalid_file_pattern(self):
        """Test detection of invalid file naming patterns"""
        test_file = self.test_path / "TestFile.py"
        test_file.write_text("# test file")
        
        violation = self.enforcer.check_file_naming(test_file)
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation["violation_id"], "NAMING-001")
        self.assertEqual(violation["severity"], "CRITICAL")

    def test_directory_deprecated_prefix(self):
        """Test detection of deprecated prefix in directories"""
        test_dir = self.test_path / "ng_directory"
        test_dir.mkdir()
        
        violation = self.enforcer.check_directory_naming(test_dir)
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation["violation_id"], "NAMING-DEPRECATED-002")
        self.assertEqual(violation["severity"], "BLOCKER")

    def test_valid_directory_name(self):
        """Test that valid directory names pass"""
        test_dir = self.test_path / "gov_directory"
        test_dir.mkdir()
        
        violation = self.enforcer.check_directory_naming(test_dir)
        
        self.assertIsNone(violation)

    def test_invalid_directory_pattern(self):
        """Test detection of invalid directory naming patterns"""
        test_dir = self.test_path / "Invalid_Dir"
        test_dir.mkdir()
        
        violation = self.enforcer.check_directory_naming(test_dir)
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation["violation_id"], "NAMING-002")

    def test_scan_project_finds_violations(self):
        """Test that scan_project finds multiple violations"""
        # Create files with violations
        (self.test_path / "ng_old.py").write_text("# old")
        (self.test_path / "gl_legacy.yaml").write_text("test: value")
        (self.test_path / "InvalidName.py").write_text("# invalid")
        
        # Create valid file
        (self.test_path / "gov_valid.py").write_text("# valid")
        
        violations = self.enforcer.scan_project()
        
        self.assertGreaterEqual(len(violations), 3)
        violation_ids = [v["violation_id"] for v in violations]
        self.assertIn("NAMING-DEPRECATED-001", violation_ids)

    def test_governance_file_prefix_enforcement(self):
        """Test that governance files require gov_ prefix"""
        # Create governance directory structure
        gov_dir = self.test_path / "governance"
        gov_dir.mkdir()
        
        # File without gov_ prefix in governance directory
        test_file = gov_dir / "test.yaml"
        test_file.write_text("test: value")
        
        violation = self.enforcer.check_file_naming(test_file)
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation["violation_id"], "NAMING-PREFIX-001")

    def test_readme_exemption_in_governance(self):
        """Test that README.md is exempted from prefix requirement"""
        gov_dir = self.test_path / "governance"
        gov_dir.mkdir()
        
        readme = gov_dir / "README.md"
        readme.write_text("# Documentation")
        
        violation = self.enforcer.check_file_naming(readme)
        
        self.assertIsNone(violation)

    def test_l0_l9_directory_prefixes_allowed(self):
        """Test that l0_ through l9_ prefixes are allowed for directories"""
        gov_dir = self.test_path / "governance"
        gov_dir.mkdir()
        
        for i in range(10):
            test_dir = gov_dir / f"l{i}_test"
            test_dir.mkdir()
            
            violation = self.enforcer.check_directory_naming(test_dir)
            self.assertIsNone(violation, f"l{i}_ prefix should be allowed")


if __name__ == "__main__":
    unittest.main()
