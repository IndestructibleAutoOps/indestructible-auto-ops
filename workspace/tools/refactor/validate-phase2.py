#!/usr/bin/env python3
"""
Phase 2 Deliverables Validator

Validates that all Phase 2 (Integration) deliverables are present and correctly formatted.

Usage:
    python3 tools/refactor/validate-phase2.py --deliverables-path <path>
"""

import argparse
import json
import sys
import logging

logger = logging.getLogger(__name__)
from pathlib import Path

try:
    import yaml
except ImportError:
    logger.info("❌ PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)


class Phase2Validator:
    """Validator for Phase 2 deliverables."""

    REQUIRED_DELIVERABLES = {
        "module_boundaries.md": {
            "type": "markdown",
            "description": "Module boundary specifications",
            "min_size": 500,
            "required_sections": ["Responsibilities", "Boundaries"],
        },
        "interface_contracts.yaml": {
            "type": "yaml",
            "description": "API contract definitions",
            "required_keys": ["contracts", "version"],
        },
        "integration_strategy.md": {
            "type": "markdown",
            "description": "Integration strategy plan",
            "min_size": 1000,
            "required_sections": ["Strategy", "Patterns"],
        },
        "migration_roadmap.yaml": {
            "type": "yaml",
            "description": "Migration roadmap",
            "required_keys": ["phases", "timeline"],
        },
    }

    def __init__(self, deliverables_path: str):
        self.deliverables_path = Path(deliverables_path)
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed: list[str] = []

    def validate(self) -> tuple[bool, dict]:
        """Run all validations."""
        logger.info(f"🔍 Validating Phase 2 deliverables at: {self.deliverables_path}")
        logger.info("")

        # Check directory exists
        if not self.deliverables_path.exists():
            self.errors.append(
                f"Deliverables directory not found: {self.deliverables_path}"
            )
            return False, self._get_report()

        # Validate each deliverable
        for filename, spec in self.REQUIRED_DELIVERABLES.items():
            self._validate_deliverable(filename, spec)

        # Check for integration tests
        self._check_integration_tests()

        # Print summary
        self._print_summary()

        # Return results
        success = len(self.errors) == 0
        return success, self._get_report()

    def _validate_deliverable(self, filename: str, spec: dict):
        """Validate a single deliverable."""
        filepath = self.deliverables_path / filename

        # Check existence
        if not filepath.exists():
            self.errors.append(f"Missing deliverable: {filename}")
            logger.info(f"❌ {filename} - Not found")
            return

        # Check file size
        file_size = filepath.stat().st_size
        min_size = spec.get("min_size", 0)
        if file_size < min_size:
            self.warnings.append(
                f"{filename} is smaller than expected ({file_size} < {min_size} bytes)"
            )

        # Validate content based on type
        file_type = spec.get("type")

        try:
            if file_type == "yaml":
                self._validate_yaml(filepath, spec)
            elif file_type == "markdown":
                self._validate_markdown(filepath, spec)

            self.passed.append(filename)
            logger.info(f"✓ {filename} - Valid")

        except Exception as e:
            self.errors.append(f"{filename}: {str(e)}")
            logger.info(f"❌ {filename} - {str(e)

    def _validate_yaml(self, filepath: Path, spec: dict):
        """Validate YAML file."""
        with open(filepath) as f:
            data = yaml.safe_load(f)

        if data is None:
            raise ValueError("Empty YAML file")

        # Check required keys
        required_keys = spec.get("required_keys", [])
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")

    def _validate_markdown(self, filepath: Path, spec: dict):
        """Validate Markdown file."""
        with open(filepath) as f:
            content = f.read()

        if len(content.strip()) == 0:
            raise ValueError("Empty Markdown file")

        # Check for required sections
        required_sections = spec.get("required_sections", [])
        for section in required_sections:
            if section.lower() not in content.lower():
                self.warnings.append(
                    f"{filepath.name}: Missing recommended section: {section}"
                )

    def _check_integration_tests(self):
        """Check for integration test suites."""
        # Look for tests directory in workspace
        repo_root = self.deliverables_path.parent.parent.parent
        tests_dir = repo_root / "workspace" / "tests" / "integration"

        if not tests_dir.exists():
            self.warnings.append(
                "Integration tests directory not found: workspace/tests/integration/"
            )
        else:
            # Count test files
            test_files = list(tests_dir.glob("**/*test*.{py,js,ts}"))
            if len(test_files) == 0:
                self.warnings.append("No integration test files found")
            else:
                logger.info(f"ℹ Found {len(test_files)

    def _print_summary(self):
        """Print validation summary."""
        logger.info("")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info("📊 Validation Summary")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info(f"✓ Passed: {len(self.passed)
        logger.warning(f"⚠ Warnings: {len(self.warnings)
        logger.error(f"❌ Errors: {len(self.errors)
        logger.info("")

        if self.warnings:
            logger.warning("Warnings:")
            for warning in self.warnings:
                logger.warning(f"  ⚠ {warning}")
            logger.info("")

        if self.errors:
            logger.error("Errors:")
            for error in self.errors:
                logger.error(f"  ❌ {error}")
            logger.info("")

    def _get_report(self) -> dict:
        """Get validation report."""
        return {
            "phase": 2,
            "deliverables_path": str(self.deliverables_path),
            "passed": self.passed,
            "warnings": self.warnings,
            "errors": self.errors,
            "success": len(self.errors) == 0,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate Phase 2 (Integration) deliverables"
    )
    parser.add_argument(
        "--deliverables-path",
        required=True,
        help="Path to Phase 2 deliverables directory",
    )
    parser.add_argument(
        "--output", help="Output validation report to file (JSON format)"
    )

    args = parser.parse_args()

    # Run validation
    validator = Phase2Validator(args.deliverables_path)
    success, report = validator.validate()

    # Save report if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        logger.info(f"📄 Report saved to: {args.output}")

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
