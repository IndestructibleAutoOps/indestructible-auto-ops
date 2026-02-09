#!/usr/bin/env python3
"""
Test Suite for Kubernetes Naming Policy System

GL Layer: GL60-80 Governance Compliance
Purpose: Comprehensive tests for naming policy validation
Version: 1.0.0
Last Updated: 2026-02-07
"""

import pytest
import json
from pathlib import Path

# Import modules to test
import sys
sys.path.insert(0, str(Path(__file__).parent))

from core import (
    Rule, Normalizer, Truncator, NamingValidator,
    CollisionTracker, build_standard_validator,
    ValidationResult, NormalizationStep
)


# ==============================================================================
# Test Normalizer
# ==============================================================================

class TestNormalizer:
    """Test the 6-step normalization pipeline."""

    def test_unicode_nfkc_compatibility(self):
        """Test Unicode NFKC normalization."""
        normalizer = Normalizer()

        # Test combining characters
        result, audit = normalizer.normalize("café")  # e + combining acute
        assert "cafe" in result.lower()
        assert audit[0].operation == "unicode_nfkc"

    def test_lowercase_conversion(self):
        """Test lowercase conversion."""
        normalizer = Normalizer()
        result, audit = normalizer.normalize("UPPERCASE")
        assert result == "uppercase"
        assert any(step.operation == "lowercase" for step in audit)

    def test_illegal_char_replacement(self):
        """Test illegal character replacement."""
        normalizer = Normalizer()

        test_cases = [
            ("hello@world", "hello-world"),
            ("test/path", "test-path"),
            ("under_score", "under-score"),
        ]

        for input_val, expected in test_cases:
            result, _ = normalizer.normalize(input_val)
            assert result == expected, f"Failed for {input_val}"

    def test_dash_collapse(self):
        """Test collapsing multiple dashes."""
        normalizer = Normalizer()

        test_cases = [
            ("hello---world", "hello-world"),
            ("a----b", "a-b"),
            ("multiple---dashes---here", "multiple-dashes-here"),
        ]

        for input_val, expected in test_cases:
            result, _ = normalizer.normalize(input_val)
            assert result == expected, f"Failed for {input_val}"

    def test_dash_trimming(self):
        """Test trimming leading/trailing dashes."""
        normalizer = Normalizer()

        test_cases = [
            ("---hello---", "hello"),
            ("-test-", "test"),
            ("--leading", "leading"),
            ("trailing--", "trailing"),
        ]

        for input_val, expected in test_cases:
            result, _ = normalizer.normalize(input_val)
            assert result == expected, f"Failed for {input_val}"

    def test_complete_normalization(self):
        """Test complete normalization pipeline."""
        normalizer = Normalizer()

        test_cases = [
            ("Prod/Payment@SVC", "prod-payment-svc"),
            ("---a---", "a"),
            ("Test___123", "test-123"),
            ("HELLO___WORLD___", "hello-world"),
        ]

        for input_val, expected in test_cases:
            result, _ = normalizer.normalize(input_val)
            assert result == expected, f"Failed for {input_val}"

    def test_audit_trail_completeness(self):
        """Test that audit trail records all steps."""
        normalizer = Normalizer()
        result, audit = normalizer.normalize("Test@Value")

        assert len(audit) == 6  # All 6 steps should be recorded
        assert audit[0].step == 1
        assert audit[5].step == 6

        # Check operation names
        operations = [step.operation for step in audit]
        assert "unicode_nfkc" in operations
        assert "lowercase" in operations
        assert "replace_illegal_chars" in operations
        assert "collapse_dashes" in operations
        assert "trim_dashes" in operations
        assert "empty_check" in operations


# ==============================================================================
# Test Rule
# ==============================================================================

class TestRule:
    """Test Rule validation."""

    def test_dns1123_label_valid(self):
        """Test valid DNS 1123 labels."""
        rule = Rule(
            name="test",
            maxLength=63,
            allowEmpty=False,
            charset=r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$"
        )

        valid_cases = [
            "a",
            "test",
            "test-123",
            "my-service",
            "prod-payment-svc",
        ]

        for case in valid_cases:
            is_valid, error = rule.validate(case)
            assert is_valid, f"Should be valid: {case}, error: {error}"
            assert error is None

    def test_dns1123_label_invalid(self):
        """Test invalid DNS 1123 labels."""
        rule = Rule(
            name="test",
            maxLength=63,
            allowEmpty=False,
            charset=r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$"
        )

        invalid_cases = [
            "UPPERCASE",  # Uppercase not allowed
            "test-",  # Trailing dash
            "-test",  # Leading dash
            "test_underscore",  # Underscore not allowed
        ]

        for case in invalid_cases:
            is_valid, error = rule.validate(case)
            assert not is_valid, f"Should be invalid: {case}"
            assert error is not None

    def test_port_name_validation(self):
        """Test port name validation (max 15 chars, must start with letter)."""
        rule = Rule(
            name="portName",
            maxLength=15,
            allowEmpty=False,
            charset=r"^[a-z]([a-z0-9-]{0,13}[a-z0-9])?$"
        )

        # Valid cases
        assert rule.validate("http")[0] is True
        assert rule.validate("https")[0] is True
        assert rule.validate("h2c")[0] is True

        # Invalid cases
        assert rule.validate("8080")[0] is False  # Starts with number
        assert rule.validate("HTTP")[0] is False  # Uppercase
        assert rule.validate("very-long-port-name")[0] is False  # Too long

    def test_length_validation(self):
        """Test length validation."""
        rule = Rule(
            name="test",
            maxLength=10,
            allowEmpty=False,
            charset=r"^[a-z0-9-]+$"
        )

        assert rule.validate("short")[0] is True
        assert rule.validate("exactly10c")[0] is True
        assert rule.validate("too-long-value")[0] is False

    def test_empty_handling(self):
        """Test empty value handling."""
        # Rule that allows empty
        rule_allow_empty = Rule(
            name="test",
            maxLength=10,
            allowEmpty=True,
            charset=r"^$|^[a-z0-9-]+$"
        )
        assert rule_allow_empty.validate("")[0] is True

        # Rule that doesn't allow empty
        rule_no_empty = Rule(
            name="test",
            maxLength=10,
            allowEmpty=False,
            charset=r"^[a-z0-9-]+$"
        )
        assert rule_no_empty.validate("")[0] is False


# ==============================================================================
# Test Truncator
# ==============================================================================

class TestTruncator:
    """Test truncate-and-hash functionality."""

    def test_no_truncation_needed(self):
        """Test that short names are not truncated."""
        truncator = Truncator()
        result = truncator.truncate_and_hash("short", max_length=63)
        assert result == "short"

    def test_truncation_determinism(self):
        """Test that truncation is deterministic."""
        truncator = Truncator()
        long_name = "this-is-a-very-long-service-name-that-exceeds-maximum-length"

        result1 = truncator.truncate_and_hash(long_name, max_length=20)
        result2 = truncator.truncate_and_hash(long_name, max_length=20)

        assert result1 == result2
        assert len(result1) <= 20

    def test_truncation_format(self):
        """Test that truncated names have correct format."""
        truncator = Truncator(hash_length=6, joiner="-")
        long_name = "very-long-service-name"

        result = truncator.truncate_and_hash(long_name, max_length=15)

        # Should be: prefix + "-" + hash(6 chars)
        assert len(result) == 15
        assert "-" in result
        parts = result.split("-")
        # Last part should be the hash
        assert len(parts[-1]) == 6

    def test_prefix_preservation(self):
        """Test that prefix is preserved where possible."""
        truncator = Truncator(hash_length=6, joiner="-")

        result = truncator.truncate_and_hash("production-service", max_length=20)

        # Should start with prefix
        assert result.startswith("production")

    def test_collision_tracking(self):
        """Test collision tracker."""
        tracker = CollisionTracker()

        # Record multiple unique values
        tracker.record("value1", "val-abc123")
        tracker.record("value2", "val-def456")
        tracker.record("value3", "val-ghi789")

        assert tracker.total_count == 3
        assert tracker.collision_count == 0
        assert tracker.is_healthy()


# ==============================================================================
# Test NamingValidator
# ==============================================================================

class TestNamingValidator:
    """Test complete validation pipeline."""

    def test_permissive_mode_normalization(self):
        """Test permissive mode with normalization."""
        validator = build_standard_validator()

        result = validator.process(
            "Prod/Payment@SVC",
            "dns1123Label63",
            normalize=True,
            auto_truncate=False
        )

        assert result.normalized == "prod-payment-svc"
        assert result.final == "prod-payment-svc"
        assert result.passed is True
        assert len(result.errors) == 0

    def test_strict_mode_no_normalization(self):
        """Test strict mode without normalization."""
        validator = build_standard_validator()

        result = validator.process(
            "Prod/Payment@SVC",
            "dns1123Label63",
            normalize=False,
            auto_truncate=False
        )

        assert result.normalized is None
        assert result.passed is False
        assert len(result.errors) > 0

    def test_auto_truncate(self):
        """Test auto-truncation for long names."""
        validator = build_standard_validator()

        long_name = "a" * 100  # Exceeds 63 char limit

        result = validator.process(
            long_name,
            "dns1123Label63",
            normalize=False,
            auto_truncate=True
        )

        assert len(result.final) <= 63
        assert result.passed is True

    def test_validation_result_structure(self):
        """Test that ValidationResult has all required fields."""
        validator = build_standard_validator()

        result = validator.process(
            "test-value",
            "dns1123Label63",
            normalize=False,
            auto_truncate=False
        )

        assert hasattr(result, 'original')
        assert hasattr(result, 'normalized')
        assert hasattr(result, 'final')
        assert hasattr(result, 'passed')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'audit_trail')
        assert hasattr(result, 'timestamp')

    def test_batch_processing(self):
        """Test batch validation."""
        validator = build_standard_validator()

        values = [
            ("test1", "dns1123Label63"),
            ("test2", "dns1123Label63"),
            ("test3", "dns1123Label63"),
        ]

        results = validator.process_batch(values, normalize=False, auto_truncate=False)

        assert len(results) == 3
        assert all(r.passed for r in results)

    def test_unknown_rule_handling(self):
        """Test handling of unknown rule names."""
        validator = build_standard_validator()

        result = validator.process(
            "test",
            "nonexistent_rule",
            normalize=False,
            auto_truncate=False
        )

        assert result.passed is False
        assert any("Unknown rule" in err for err in result.errors)


# ==============================================================================
# Cross-Language Compatibility Vectors
# ==============================================================================

class TestCrossLanguageCompatibility:
    """Test vectors for cross-language implementation compatibility."""

    def get_test_vectors(self):
        """Get standard test vectors for cross-language validation."""
        return [
            # (input, rule, expected_normalized, should_pass_strict)
            ("test", "dns1123Label63", "test", True),
            ("Prod/Payment@SVC", "dns1123Label63", "prod-payment-svc", False),
            ("---a---", "dns1123Label63", "a", False),
            ("UPPERCASE", "dns1123Label63", "uppercase", False),
            ("test-123", "dns1123Label63", "test-123", True),
            ("http", "portName15", "http", True),
            ("8080-http", "portName15", "8080-http", False),
            ("", "k8sLabelValue63", "", True),
            ("valid-label", "k8sLabelValue63", "valid-label", True),
        ]

    def test_normalization_vectors(self):
        """Test normalization produces expected results."""
        validator = build_standard_validator()

        for input_val, rule_name, expected_norm, _ in self.get_test_vectors():
            result = validator.process(
                input_val,
                rule_name,
                normalize=True,
                auto_truncate=False
            )

            assert result.normalized == expected_norm, \
                f"Normalization failed for {input_val}: expected {expected_norm}, got {result.normalized}"

    def test_strict_validation_vectors(self):
        """Test strict validation produces expected results."""
        validator = build_standard_validator()

        for input_val, rule_name, _, should_pass in self.get_test_vectors():
            result = validator.process(
                input_val,
                rule_name,
                normalize=False,
                auto_truncate=False
            )

            assert result.passed == should_pass, \
                f"Strict validation failed for {input_val}: expected {should_pass}, got {result.passed}"


# ==============================================================================
# Performance Tests
# ==============================================================================

class TestPerformance:
    """Basic performance benchmarks."""

    def test_normalization_performance(self):
        """Test normalization performance."""
        normalizer = Normalizer()

        # Should process 10K normalizations quickly
        for i in range(10000):
            normalizer.normalize(f"test-value-{i}")

    def test_validation_performance(self):
        """Test validation performance."""
        validator = build_standard_validator()

        # Should process 1K validations quickly
        for i in range(1000):
            validator.process(
                f"test-value-{i}",
                "dns1123Label63",
                normalize=True,
                auto_truncate=False
            )


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
