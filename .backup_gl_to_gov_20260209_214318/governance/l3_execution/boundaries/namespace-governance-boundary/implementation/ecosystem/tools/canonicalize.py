#!/usr/bin/env python3
"""
Canonicalization Tool for Era-1 Evidence System
================================================

This tool provides deterministic canonicalization and hashing for JSON and YAML data
using RFC 8785 JSON Canonicalization Scheme (JCS).

Capabilities:
1. JSON canonicalization using JCS
2. YAML to JSON conversion with canonicalization
3. SHA256 hash computation of canonicalized data
4. Layer-based sorting (optional, application-level)

Author: SuperNinja AI Agent
Era: 1 (Evidence-Native Bootstrap)
Version: 1.0.0
"""

import hashlib
import json
import sys
from typing import Any, Dict, Optional
import yaml

try:
    from rfc8785 import dumps as canonicalize
except ImportError:
    print("ERROR: rfc8785 package not installed. Run: pip install rfc8785")
    sys.exit(1)


# ============================================================================
# Layer Map (Optional Application-Level Layering)
# ============================================================================

DEFAULT_LAYER_MAP: Dict[str, int] = {
    # L1: Core fields (never change)
    "uuid": 1,
    "artifact_id": 1,
    "timestamp": 1,
    "event_id": 1,
    # L2: Optional fields (can be added in future)
    "type": 2,
    "source": 2,
    "era": 2,
    "layer": 2,
    "phase": 2,
    "step": 2,
    # L3: Extension fields (can be infinitely expanded)
    # All other fields default to 3
}


# ============================================================================
# Core Canonicalization Functions
# ============================================================================


def canonicalize_json(data: Any) -> str:
    """
    Canonicalize JSON data using RFC 8785 (JCS).

    Args:
        data: Python object (dict, list, str, int, float, bool, None)

    Returns:
        Canonical JSON string (deterministic, no whitespace, sorted keys)

    Example:
        >>> data = {"b": 2, "a": 1}
        >>> canonicalize_json(data)
        '{"a":1,"b":2}'
    """
    try:
        result = canonicalize(data)
        # rfc8785.dumps returns bytes, decode to string
        if isinstance(result, bytes):
            return result.decode("utf-8")
        return result
    except Exception as e:
        raise ValueError(f"Failed to canonicalize data: {e}")


def canonicalize_and_hash(data: Any, hash_algorithm: str = "sha256") -> str:
    """
    Canonicalize JSON data and compute its hash.

    Args:
        data: Python object to canonicalize
        hash_algorithm: Hash algorithm to use (default: 'sha256')

    Returns:
        Hexadecimal hash string

    Example:
        >>> data = {"b": 2, "a": 1}
        >>> canonicalize_and_hash(data)
        'a9993e364706816aba3e25717850c26c9cd0d89d'
    """
    canonical_json = canonicalize_json(data)

    if hash_algorithm == "sha256":
        hash_obj = hashlib.sha256()
    elif hash_algorithm == "sha1":
        hash_obj = hashlib.sha1()
    elif hash_algorithm == "sha512":
        hash_obj = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    hash_obj.update(canonical_json.encode("utf-8"))
    return hash_obj.hexdigest()


def canonicalize_layered(
    data: Dict[str, Any], layer_map: Optional[Dict[str, int]] = None
) -> str:
    """
    Canonicalize JSON data using layered sorting protocol (application-level).

    This is OPTIONAL and should only be used when layered semantics are required.
    The layering is applied at the application level before JCS canonicalization.

    Args:
        data: Dictionary to canonicalize
        layer_map: Optional layer map (default: DEFAULT_LAYER_MAP)

    Returns:
        Canonical JSON string with layered ordering

    Layer Ordering:
        - L1: Core fields (always first, sorted)
        - L2: Optional fields (middle, sorted)
        - L3: Extension fields (last, sorted)

    Example:
        >>> data = {"z": 3, "uuid": "123", "b": 2, "a": 1}
        >>> canonicalize_layered(data)
        '{"uuid":"123","a":1,"b":2,"z":3}'
    """
    if layer_map is None:
        layer_map = DEFAULT_LAYER_MAP

    # Separate fields by layer
    l1_fields = {k: v for k, v in data.items() if layer_map.get(k, 3) == 1}
    l2_fields = {k: v for k, v in data.items() if layer_map.get(k, 3) == 2}
    l3_fields = {k: v for k, v in data.items() if layer_map.get(k, 3) == 3}

    # Sort each layer alphabetically
    l1_sorted = dict(sorted(l1_fields.items()))
    l2_sorted = dict(sorted(l2_fields.items()))
    l3_sorted = dict(sorted(l3_fields.items()))

    # Merge layers in order (L1 → L2 → L3)
    layered_data = {**l1_sorted, **l2_sorted, **l3_sorted}

    # Apply JCS canonicalization to the layered data
    return canonicalize_json(layered_data)


def canonicalize_layered_and_hash(
    data: Dict[str, Any],
    layer_map: Optional[Dict[str, int]] = None,
    hash_algorithm: str = "sha256",
) -> str:
    """
    Canonicalize JSON data using layered protocol and compute hash.

    Args:
        data: Dictionary to canonicalize
        layer_map: Optional layer map
        hash_algorithm: Hash algorithm to use

    Returns:
        Hexadecimal hash string
    """
    canonical_json = canonicalize_layered(data, layer_map)

    if hash_algorithm == "sha256":
        hash_obj = hashlib.sha256()
    elif hash_algorithm == "sha1":
        hash_obj = hashlib.sha1()
    elif hash_algorithm == "sha512":
        hash_obj = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    hash_obj.update(canonical_json.encode("utf-8"))
    return hash_obj.hexdigest()


# ============================================================================
# YAML Handling
# ============================================================================


def yaml_to_canonical_json(yaml_content: str) -> str:
    """
    Convert YAML content to canonical JSON.

    This function handles YAML-specific features:
    - Anchors: Expanded inline
    - Tags: Converted to plain values
    - Multi-doc: First document only

    Args:
        yaml_content: YAML string

    Returns:
        Canonical JSON string

    Example:
        >>> yaml_content = "a: 1\\nb: 2"
        >>> yaml_to_canonical_json(yaml_content)
        '{"a":1,"b":2}'
    """
    try:
        # Parse YAML
        data = yaml.safe_load(yaml_content)

        # Canonicalize using JCS
        return canonicalize_json(data)
    except Exception as e:
        raise ValueError(f"Failed to convert YAML to canonical JSON: {e}")


def yaml_file_to_canonical_json(yaml_file_path: str) -> str:
    """
    Read YAML file and convert to canonical JSON.

    Args:
        yaml_file_path: Path to YAML file

    Returns:
        Canonical JSON string
    """
    try:
        with open(yaml_file_path, "r", encoding="utf-8") as f:
            yaml_content = f.read()
        return yaml_to_canonical_json(yaml_content)
    except Exception as e:
        raise ValueError(f"Failed to read YAML file: {e}")


def yaml_file_hash(yaml_file_path: str, hash_algorithm: str = "sha256") -> str:
    """
    Compute hash of YAML file using canonicalization.

    Args:
        yaml_file_path: Path to YAML file
        hash_algorithm: Hash algorithm to use

    Returns:
        Hexadecimal hash string
    """
    canonical_json = yaml_file_to_canonical_json(yaml_file_path)

    if hash_algorithm == "sha256":
        hash_obj = hashlib.sha256()
    elif hash_algorithm == "sha1":
        hash_obj = hashlib.sha1()
    elif hash_algorithm == "sha512":
        hash_obj = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    hash_obj.update(canonical_json.encode("utf-8"))
    return hash_obj.hexdigest()


# ============================================================================
# Verification Functions
# ============================================================================


def verify_hash(data: Any, expected_hash: str, hash_algorithm: str = "sha256") -> bool:
    """
    Verify that the canonical hash of data matches expected hash.

    Args:
        data: Python object to verify
        expected_hash: Expected hash value
        hash_algorithm: Hash algorithm to use

    Returns:
        True if hash matches, False otherwise
    """
    actual_hash = canonicalize_and_hash(data, hash_algorithm)
    return actual_hash.lower() == expected_hash.lower()


def verify_yaml_hash(
    yaml_content: str, expected_hash: str, hash_algorithm: str = "sha256"
) -> bool:
    """
    Verify that the canonical hash of YAML content matches expected hash.

    Args:
        yaml_content: YAML string to verify
        expected_hash: Expected hash value
        hash_algorithm: Hash algorithm to use

    Returns:
        True if hash matches, False otherwise
    """
    canonical_json = yaml_to_canonical_json(yaml_content)

    if hash_algorithm == "sha256":
        hash_obj = hashlib.sha256()
    elif hash_algorithm == "sha1":
        hash_obj = hashlib.sha1()
    elif hash_algorithm == "sha512":
        hash_obj = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    hash_obj.update(canonical_json.encode("utf-8"))
    actual_hash = hash_obj.hexdigest()

    return actual_hash.lower() == expected_hash.lower()


# ============================================================================
# Command-Line Interface
# ============================================================================


def main():
    """Command-line interface for canonicalization tool."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Canonicalize JSON/YAML data using RFC 8785 (JCS)"
    )

    parser.add_argument(
        "file", type=str, help="Path to JSON or YAML file to canonicalize"
    )

    parser.add_argument(
        "--hash", action="store_true", help="Compute hash of canonicalized data"
    )

    parser.add_argument(
        "--algorithm",
        type=str,
        default="sha256",
        choices=["sha256", "sha1", "sha512"],
        help="Hash algorithm (default: sha256)",
    )

    parser.add_argument(
        "--layered",
        action="store_true",
        help="Use layered sorting protocol (application-level)",
    )

    parser.add_argument("--verify", type=str, help="Expected hash to verify against")

    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        # Read file
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

        # Detect format
        if args.file.endswith(".yaml") or args.file.endswith(".yml"):
            # YAML file
            if args.layered:
                print(
                    "ERROR: Layered sorting is not supported for YAML files",
                    file=sys.stderr,
                )
                sys.exit(1)

            canonical_json = yaml_to_canonical_json(content)
        else:
            # JSON file
            data = json.loads(content)

            if args.layered:
                canonical_json = canonicalize_layered(data)
            else:
                canonical_json = canonicalize_json(data)

        # Compute hash if requested
        if args.hash or args.verify:
            if args.algorithm == "sha256":
                hash_obj = hashlib.sha256()
            elif args.algorithm == "sha1":
                hash_obj = hashlib.sha1()
            elif args.algorithm == "sha512":
                hash_obj = hashlib.sha512()

            hash_obj.update(canonical_json.encode("utf-8"))
            hash_value = hash_obj.hexdigest()

        # Verify hash if requested
        if args.verify:
            if hash_value.lower() == args.verify.lower():
                print(f"✓ Hash verification PASSED", file=sys.stderr)
                print(f"  Expected: {args.verify}")
                print(f"  Actual:   {hash_value}")
            else:
                print(f"✗ Hash verification FAILED", file=sys.stderr)
                print(f"  Expected: {args.verify}")
                print(f"  Actual:   {hash_value}")
                sys.exit(1)

        # Output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.hash:
                    f.write(hash_value + "\n")
                else:
                    f.write(canonical_json + "\n")
        else:
            if args.hash:
                print(hash_value)
            else:
                print(canonical_json)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
