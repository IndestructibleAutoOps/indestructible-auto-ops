#!/usr/bin/env python3
"""
Simple YAML Parser - Zero Dependency Implementation
====================================================
A minimal YAML parser for basic YAML files without external dependencies.

Supported Features:
- Basic key-value pairs
- Nested dictionaries
- Lists
- Comments (#)
- String values (quoted and unquoted)
- Numbers (integers and floats)
- Booleans (true/false)
- None/null values

Limitations:
- No multi-line strings
- No anchors/aliases
- No complex types
- No custom tags
"""

import re
from typing import Any, Dict, List, Union


def parse_yaml(content: str) -> Dict[str, Any]:
    """
    Parse YAML content into a Python dictionary.

    Args:
        content: YAML string content

    Returns:
        Parsed dictionary
    """
    lines = content.split("\n")
    result = {}
    stack = [(result, 0)]  # (current_dict, indent_level)

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and comments
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        # Calculate indentation
        indent = len(line) - len(stripped)

        # Find the appropriate parent level
        while stack and stack[-1][1] > indent:
            stack.pop()

        if not stack:
            continue

        current_dict, _ = stack[-1]

        # Parse key-value pair
        if ":" in stripped:
            key_part, value_part = stripped.split(":", 1)
            key = key_part.strip()
            value = value_part.strip()

            # Check if this is a nested structure
            if not value:
                # Empty value means nested structure
                new_dict = {}
                current_dict[key] = new_dict
                stack.append((new_dict, indent))
            else:
                # Parse the value
                current_dict[key] = _parse_value(value)
        elif stripped.startswith("- "):
            # List item
            list_value = stripped[2:].strip()
            if not isinstance(current_dict, list):
                # Convert to list if needed
                if current_dict:
                    # This shouldn't happen in valid YAML
                    pass

            parsed_value = _parse_value(list_value)
            if isinstance(current_dict, list):
                current_dict.append(parsed_value)

    return result


def _parse_value(value: str) -> Any:
    """
    Parse a YAML value string into appropriate Python type.

    Args:
        value: String value to parse

    Returns:
        Parsed value (str, int, float, bool, None, list, dict)
    """
    value = value.strip()

    # Handle quoted strings
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    # Handle null/none
    if value.lower() in ("null", "none", "~"):
        return None

    # Handle booleans
    if value.lower() in ("true", "yes", "on"):
        return True
    if value.lower() in ("false", "no", "off"):
        return False

    # Handle numbers
    try:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        pass

    # Handle lists (inline)
    if value.startswith("[") and value.endswith("]"):
        return _parse_inline_list(value[1:-1])

    # Handle dictionaries (inline)
    if value.startswith("{") and value.endswith("}"):
        return _parse_inline_dict(value[1:-1])

    # Default to string
    return value


def _parse_inline_list(content: str) -> List[Any]:
    """Parse an inline YAML list."""
    if not content.strip():
        return []

    items = []
    current = ""
    in_quotes = False
    quote_char = None
    depth = 0

    for char in content:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
            current += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            current += char
        elif char == "[" and not in_quotes:
            depth += 1
            current += char
        elif char == "]" and not in_quotes:
            depth -= 1
            current += char
        elif char == "," and not in_quotes and depth == 0:
            items.append(_parse_value(current.strip()))
            current = ""
        else:
            current += char

    if current.strip():
        items.append(_parse_value(current.strip()))

    return items


def _parse_inline_dict(content: str) -> Dict[str, Any]:
    """Parse an inline YAML dictionary."""
    result = {}
    if not content.strip():
        return result

    pairs = content.split(",")
    for pair in pairs:
        if ":" in pair:
            key, value = pair.split(":", 1)
            result[key.strip()] = _parse_value(value.strip())

    return result


def safe_load(file_obj) -> Dict[str, Any]:
    """
    Load YAML from a file object (mimics yaml.safe_load).

    Args:
        file_obj: File object to read from

    Returns:
        Parsed dictionary
    """
    content = file_obj.read()
    return parse_yaml(content)


def load(filepath: str) -> Dict[str, Any]:
    """
    Load YAML from a file path.

    Args:
        filepath: Path to YAML file

    Returns:
        Parsed dictionary
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return parse_yaml(f.read())
