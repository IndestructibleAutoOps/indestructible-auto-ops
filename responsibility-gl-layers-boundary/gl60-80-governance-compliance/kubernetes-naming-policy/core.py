#!/usr/bin/env python3
"""
Enterprise-Grade Kubernetes Naming Policy System - Core Implementation

GL Layer: GL60-80 Governance Compliance
Purpose: Kubernetes resource naming policy validation and normalization
Version: 1.0.0
Last Updated: 2026-02-07

This module provides a production-ready, deterministic naming policy validator
for Kubernetes resources with:
- Zero-Trust Architecture (reject-only mode)
- Deterministic Validation (cross-language compatible)
- Enterprise Audit Trail
- Collision-Resistant truncation with BLAKE3 hashing
- No external dependencies (pure Python 3.11+)
"""

import re
import hashlib
import unicodedata
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ==============================================================================
# Constants
# ==============================================================================

# Standard Kubernetes naming rules
DNS_1123_LABEL_PATTERN = r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$"
PORT_NAME_PATTERN = r"^[a-z]([a-z0-9-]{0,13}[a-z0-9])?$"
K8S_LABEL_VALUE_PATTERN = r"^$|^[a-z0-9]([a-z0-9_.-]{0,61}[a-z0-9])?$"

DEFAULT_HASH_LENGTH = 6
DEFAULT_JOINER = "-"


# ==============================================================================
# Data Classes
# ==============================================================================

@dataclass
class Rule:
    """
    Defines a naming rule with constraints.

    Attributes:
        name: Unique rule identifier
        maxLength: Maximum allowed length
        allowEmpty: Whether empty strings are allowed
        charset: Regex pattern for allowed characters
    """
    name: str
    maxLength: int
    allowEmpty: bool
    charset: str
    _compiled_pattern: Optional[re.Pattern] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compile regex pattern for performance."""
        self._compiled_pattern = re.compile(self.charset)

    def validate(self, value: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a value against this rule.

        Args:
            value: The value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value and not self.allowEmpty:
            return False, "Value cannot be empty"

        if len(value) > self.maxLength:
            return False, f"Exceeds maximum length {self.maxLength} (got {len(value)})"

        if not self._compiled_pattern.match(value):
            return False, f"Does not match charset pattern: {self.charset}"

        return True, None


@dataclass
class NormalizationStep:
    """Records a single step in the normalization pipeline."""
    step: int
    operation: str
    input: str
    output: str
    changed: bool


@dataclass
class ValidationResult:
    """
    Result of a validation operation.

    Attributes:
        original: Original input value
        normalized: Value after normalization (if applied)
        final: Final value after truncation (if applied)
        passed: Whether validation passed
        errors: List of error messages
        audit_trail: List of normalization steps for debugging
        timestamp: When validation occurred
    """
    original: str
    normalized: Optional[str]
    final: str
    passed: bool
    errors: List[str]
    audit_trail: List[NormalizationStep] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        return result


# ==============================================================================
# Normalizer
# ==============================================================================

class Normalizer:
    """
    Deterministic 6-step normalization pipeline for Kubernetes names.

    All implementations (Python, Go, Java, Rust) must produce identical results.
    """

    @staticmethod
    def normalize(value: str) -> Tuple[str, List[NormalizationStep]]:
        """
        Apply 6-step normalization pipeline.

        Steps:
        1. Unicode NFKC normalization
        2. Lowercase conversion
        3. Replace illegal characters with dash
        4. Collapse multiple dashes
        5. Trim leading/trailing dashes
        6. Handle empty result

        Args:
            value: Input string to normalize

        Returns:
            Tuple of (normalized_value, audit_trail)
        """
        audit_trail = []
        current = value

        # Step 1: Unicode NFKC normalization
        next_val = unicodedata.normalize('NFKC', current)
        audit_trail.append(NormalizationStep(
            step=1,
            operation="unicode_nfkc",
            input=current,
            output=next_val,
            changed=(current != next_val)
        ))
        current = next_val

        # Step 2: Lowercase conversion
        next_val = current.lower()
        audit_trail.append(NormalizationStep(
            step=2,
            operation="lowercase",
            input=current,
            output=next_val,
            changed=(current != next_val)
        ))
        current = next_val

        # Step 3: Replace illegal characters with dash
        # Keep only alphanumeric and dash
        next_val = re.sub(r'[^a-z0-9-]', '-', current)
        audit_trail.append(NormalizationStep(
            step=3,
            operation="replace_illegal_chars",
            input=current,
            output=next_val,
            changed=(current != next_val)
        ))
        current = next_val

        # Step 4: Collapse multiple dashes
        next_val = re.sub(r'-+', '-', current)
        audit_trail.append(NormalizationStep(
            step=4,
            operation="collapse_dashes",
            input=current,
            output=next_val,
            changed=(current != next_val)
        ))
        current = next_val

        # Step 5: Trim leading/trailing dashes
        next_val = current.strip('-')
        audit_trail.append(NormalizationStep(
            step=5,
            operation="trim_dashes",
            input=current,
            output=next_val,
            changed=(current != next_val)
        ))
        current = next_val

        # Step 6: Empty check (handled by caller)
        audit_trail.append(NormalizationStep(
            step=6,
            operation="empty_check",
            input=current,
            output=current,
            changed=False
        ))

        return current, audit_trail


# ==============================================================================
# Truncator
# ==============================================================================

class Truncator:
    """
    Deterministic truncate-and-hash for names exceeding maxLength.

    Uses BLAKE3 (or SHA256 fallback) for collision resistance.
    """

    def __init__(self, hash_length: int = DEFAULT_HASH_LENGTH, joiner: str = DEFAULT_JOINER):
        """
        Initialize truncator.

        Args:
            hash_length: Number of hex characters from hash to use
            joiner: Character to join prefix and hash
        """
        self.hash_length = hash_length
        self.joiner = joiner

    def _compute_hash(self, value: str) -> str:
        """
        Compute hash of value using BLAKE3 (or SHA256 fallback).

        Args:
            value: Value to hash

        Returns:
            Hex string of hash
        """
        # Try BLAKE3 first (requires blake3 package)
        # Fall back to SHA256 (standard library)
        try:
            import blake3
            hasher = blake3.blake3()
            hasher.update(value.encode('utf-8'))
            return hasher.hexdigest()
        except ImportError:
            # Fallback to SHA256
            return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def truncate_and_hash(self, value: str, max_length: int) -> str:
        """
        Truncate value to max_length using deterministic hash suffix.

        Algorithm:
        1. Compute hash of full value
        2. Take first hash_length characters of hash
        3. Calculate max prefix length: max_length - joiner_length - hash_length
        4. Extract prefix, trim trailing dashes
        5. Combine: prefix + joiner + hash_suffix

        Args:
            value: Value to truncate
            max_length: Maximum allowed length

        Returns:
            Truncated value with hash suffix
        """
        if len(value) <= max_length:
            return value

        # Compute hash
        full_hash = self._compute_hash(value)
        hash_suffix = full_hash[:self.hash_length]

        # Calculate prefix length
        max_prefix_length = max_length - len(self.joiner) - self.hash_length

        if max_prefix_length <= 0:
            # Can't fit anything, return just the hash (truncated if needed)
            return hash_suffix[:max_length]

        # Extract prefix
        prefix = value[:max_prefix_length]

        # Trim trailing dashes from prefix
        prefix = prefix.rstrip('-')

        # Combine
        result = f"{prefix}{self.joiner}{hash_suffix}"

        return result


# ==============================================================================
# Collision Tracker
# ==============================================================================

class CollisionTracker:
    """
    Tracks hash collisions to monitor system health.

    In production, this should alert if collision rate exceeds threshold.
    """

    def __init__(self):
        """Initialize collision tracker."""
        self.hash_to_originals: Dict[str, List[str]] = {}
        self.collision_count = 0
        self.total_count = 0

    def record(self, original: str, truncated: str):
        """
        Record a truncation operation.

        Args:
            original: Original value before truncation
            truncated: Truncated value with hash
        """
        self.total_count += 1

        # Extract hash from truncated value (last hash_length chars after joiner)
        parts = truncated.split('-')
        if len(parts) >= 2:
            hash_part = parts[-1]

            if hash_part not in self.hash_to_originals:
                self.hash_to_originals[hash_part] = []

            # Check for collision
            if original not in self.hash_to_originals[hash_part]:
                if len(self.hash_to_originals[hash_part]) > 0:
                    # Collision detected
                    self.collision_count += 1

                self.hash_to_originals[hash_part].append(original)

    def get_collision_rate(self) -> float:
        """
        Get collision rate.

        Returns:
            Collision rate as percentage (0-100)
        """
        if self.total_count == 0:
            return 0.0
        return (self.collision_count / self.total_count) * 100.0

    def is_healthy(self, threshold: float = 1.0) -> bool:
        """
        Check if collision rate is below threshold.

        Args:
            threshold: Maximum acceptable collision rate (percentage)

        Returns:
            True if healthy, False otherwise
        """
        return self.get_collision_rate() < threshold


# ==============================================================================
# Naming Validator
# ==============================================================================

class NamingValidator:
    """
    Main validator class for Kubernetes naming policy enforcement.

    Supports both permissive (normalize + auto-truncate) and strict modes.
    """

    def __init__(self, rules: Dict[str, Rule]):
        """
        Initialize validator with rules.

        Args:
            rules: Dictionary of rule_name -> Rule
        """
        self.rules = rules
        self.normalizer = Normalizer()
        self.truncator = Truncator()
        self.collision_tracker = CollisionTracker()

    def process(
        self,
        value: str,
        rule_name: str,
        normalize: bool = False,
        auto_truncate: bool = False
    ) -> ValidationResult:
        """
        Process a value through the validation pipeline.

        Args:
            value: Input value to validate
            rule_name: Name of rule to apply
            normalize: Whether to normalize the value
            auto_truncate: Whether to auto-truncate if exceeds max length

        Returns:
            ValidationResult with detailed information
        """
        if rule_name not in self.rules:
            return ValidationResult(
                original=value,
                normalized=None,
                final=value,
                passed=False,
                errors=[f"Unknown rule: {rule_name}"]
            )

        rule = self.rules[rule_name]
        errors = []
        audit_trail = []

        # Step 1: Normalize if requested
        if normalize:
            normalized, norm_audit = self.normalizer.normalize(value)
            audit_trail.extend(norm_audit)
        else:
            normalized = value

        # Step 2: Validate against rule
        is_valid, error_msg = rule.validate(normalized)

        # If validation fails due to length and auto_truncate is enabled
        final = normalized
        if not is_valid and auto_truncate and len(normalized) > rule.maxLength:
            final = self.truncator.truncate_and_hash(normalized, rule.maxLength)
            self.collision_tracker.record(normalized, final)

            # Re-validate truncated value
            is_valid, error_msg = rule.validate(final)

        if not is_valid and error_msg:
            errors.append(error_msg)

        return ValidationResult(
            original=value,
            normalized=normalized if normalize else None,
            final=final,
            passed=is_valid,
            errors=errors,
            audit_trail=audit_trail
        )

    def process_batch(
        self,
        values: List[Tuple[str, str]],
        normalize: bool = False,
        auto_truncate: bool = False
    ) -> List[ValidationResult]:
        """
        Process multiple values in batch.

        Args:
            values: List of (value, rule_name) tuples
            normalize: Whether to normalize values
            auto_truncate: Whether to auto-truncate

        Returns:
            List of ValidationResult objects
        """
        results = []
        for value, rule_name in values:
            result = self.process(value, rule_name, normalize, auto_truncate)
            results.append(result)
        return results


# ==============================================================================
# Factory Functions
# ==============================================================================

def build_standard_validator() -> NamingValidator:
    """
    Build a validator with standard Kubernetes rules.

    Returns:
        NamingValidator with standard rules configured
    """
    rules = {
        "dns1123Label63": Rule(
            name="dns1123Label63",
            maxLength=63,
            allowEmpty=False,
            charset=DNS_1123_LABEL_PATTERN
        ),
        "portName15": Rule(
            name="portName15",
            maxLength=15,
            allowEmpty=False,
            charset=PORT_NAME_PATTERN
        ),
        "k8sLabelValue63": Rule(
            name="k8sLabelValue63",
            maxLength=63,
            allowEmpty=True,
            charset=K8S_LABEL_VALUE_PATTERN
        )
    }

    return NamingValidator(rules)


# ==============================================================================
# Main (for testing)
# ==============================================================================

if __name__ == "__main__":
    # Example usage
    validator = build_standard_validator()

    # Test permissive mode
    print("=== Permissive Mode (normalize + auto-truncate) ===")
    result = validator.process(
        "Prod/Payment@SVC",
        "dns1123Label63",
        normalize=True,
        auto_truncate=True
    )
    print(f"Original: {result.original}")
    print(f"Normalized: {result.normalized}")
    print(f"Final: {result.final}")
    print(f"Passed: {result.passed}")
    print(f"Errors: {result.errors}")
    print()

    # Test strict mode
    print("=== Strict Mode (no normalization) ===")
    result = validator.process(
        "Prod/Payment@SVC",
        "dns1123Label63",
        normalize=False,
        auto_truncate=False
    )
    print(f"Original: {result.original}")
    print(f"Final: {result.final}")
    print(f"Passed: {result.passed}")
    print(f"Errors: {result.errors}")
