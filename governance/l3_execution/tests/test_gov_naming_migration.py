#!/usr/bin/env python3
"""
Unit tests for GovNamingMigration
"""

import tempfile
import unittest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "migration"))

from gov_naming_migration import GovNamingMigration


class TestGovNamingMigration(unittest.TestCase):
    """Test cases for GovNamingMigration"""

    def setUp(self):
        """Create a temporary directory for testing"""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)
        self.migrator = GovNamingMigration(str(self.test_path), dry_run=True)

    def tearDown(self):
        """Clean up temporary directory"""
        self.test_dir.cleanup()

    def test_ng_to_gov_naming_migration(self):
        """Test that ng_ prefix migrates to gov_naming_"""
        old_name = "ng_example.yaml"
        new_name = self.migrator.generate_new_name(old_name)
        
        self.assertEqual(new_name, "gov_naming_example.yaml")

    def test_gl_to_gov_migration(self):
        """Test that gl_ prefix migrates to gov_"""
        old_name = "gl_config.py"
        new_name = self.migrator.generate_new_name(old_name)
        
        self.assertEqual(new_name, "gov_config.py")

    def test_already_compliant_name_unchanged(self):
        """Test that names without deprecated prefixes remain unchanged"""
        old_name = "gov_test.yaml"
        new_name = self.migrator.generate_new_name(old_name)
        
        self.assertEqual(new_name, old_name)

    def test_no_prefix_name_unchanged(self):
        """Test that names without any special prefix remain unchanged"""
        old_name = "test_file.py"
        new_name = self.migrator.generate_new_name(old_name)
        
        self.assertEqual(new_name, old_name)

    def test_scan_deprecated_finds_ng_files(self):
        """Test that scan_deprecated finds files with ng_ prefix"""
        # Create test files
        ng_file = self.test_path / "ng_test.py"
        ng_file.write_text("# test")
        
        gov_file = self.test_path / "gov_test.py"
        gov_file.write_text("# test")
        
        deprecated = self.migrator.scan_deprecated()
        
        self.assertEqual(len(deprecated), 1)
        self.assertEqual(deprecated[0].name, "ng_test.py")

    def test_scan_deprecated_finds_gl_files(self):
        """Test that scan_deprecated finds files with gl_ prefix"""
        gl_file = self.test_path / "gl_legacy.yaml"
        gl_file.write_text("test: value")
        
        deprecated = self.migrator.scan_deprecated()
        
        self.assertEqual(len(deprecated), 1)
        self.assertEqual(deprecated[0].name, "gl_legacy.yaml")

    def test_scan_deprecated_finds_directories(self):
        """Test that scan_deprecated finds directories with deprecated prefixes"""
        ng_dir = self.test_path / "ng_directory"
        ng_dir.mkdir()
        
        gl_dir = self.test_path / "gl_directory"
        gl_dir.mkdir()
        
        deprecated = self.migrator.scan_deprecated()
        
        self.assertEqual(len(deprecated), 2)
        deprecated_names = [d.name for d in deprecated]
        self.assertIn("ng_directory", deprecated_names)
        self.assertIn("gl_directory", deprecated_names)

    def test_scan_deprecated_ignores_compliant_assets(self):
        """Test that scan_deprecated ignores assets without deprecated prefixes"""
        # Create compliant files
        (self.test_path / "gov_test.py").write_text("# test")
        (self.test_path / "gov_naming_test.yaml").write_text("test: value")
        (self.test_path / "other_file.txt").write_text("content")
        
        deprecated = self.migrator.scan_deprecated()
        
        self.assertEqual(len(deprecated), 0)

    def test_prefix_migrations_mapping(self):
        """Test that PREFIX_MIGRATIONS mapping is correct"""
        self.assertEqual(self.migrator.PREFIX_MIGRATIONS["ng_"], "gov_naming_")
        self.assertEqual(self.migrator.PREFIX_MIGRATIONS["gl_"], "gov_")

    def test_deprecated_prefixes_list(self):
        """Test that DEPRECATED_PREFIXES list contains both prefixes"""
        self.assertIn("ng_", self.migrator.DEPRECATED_PREFIXES)
        self.assertIn("gl_", self.migrator.DEPRECATED_PREFIXES)
        self.assertEqual(len(self.migrator.DEPRECATED_PREFIXES), 2)

    def test_complex_ng_filename(self):
        """Test migration of complex ng_ filename"""
        old_name = "ng_complex_test_file.py"
        new_name = self.migrator.generate_new_name(old_name)
        
        self.assertEqual(new_name, "gov_naming_complex_test_file.py")

    def test_complex_gl_filename(self):
        """Test migration of complex gl_ filename"""
        old_name = "gl_complex_test_file.yaml"
        new_name = self.migrator.generate_new_name(old_name)
        
        self.assertEqual(new_name, "gov_complex_test_file.yaml")

    def test_return_type_of_scan_deprecated(self):
        """Test that scan_deprecated returns a List[Path]"""
        result = self.migrator.scan_deprecated()
        
        self.assertIsInstance(result, list)
        # Create a file to ensure we get Path objects
        test_file = self.test_path / "ng_test.py"
        test_file.write_text("# test")
        
        result = self.migrator.scan_deprecated()
        if result:
            self.assertIsInstance(result[0], Path)


if __name__ == "__main__":
    unittest.main()
