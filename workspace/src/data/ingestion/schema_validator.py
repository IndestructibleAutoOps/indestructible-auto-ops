"""
GL20-29: Data Science / Data Access Layer
GL20: Data Ingestion Module - Schema Validator
"""

import re
from typing import Any


class SchemaValidator:
    """Validate data against schema definitions"""

    def __init__(self, schema: dict[str, Any]):
        self.schema = schema
        self.validation_errors = []

    def validate_record(self, record: dict[str, Any]) -> bool:
        """Validate a single record against schema"""

        self.validation_errors = []

        # Check required fields
        required_fields = self.schema.get('required_fields', [])
        for field in required_fields:
            if field not in record:
                self.validation_errors.append(f"Missing required field: {field}")

        # Check field types
        field_types = self.schema.get('field_types', {})
        for field, expected_type in field_types.items():
            if field in record:
                if not self._check_type(record[field], expected_type):
                    self.validation_errors.append(
                        f"Field '{field}' has wrong type. Expected {expected_type}, got {type(record[field])}"
                    )

        # Check field patterns
        field_patterns = self.schema.get('field_patterns', {})
        for field, pattern in field_patterns.items():
            if field in record and isinstance(record[field], str):
                if not re.match(pattern, record[field]):
                    self.validation_errors.append(
                        f"Field '{field}' does not match pattern: {pattern}"
                    )

        # Check field ranges
        field_ranges = self.schema.get('field_ranges', {})
        for field, range_spec in field_ranges.items():
            if field in record:
                value = record[field]
                if 'min' in range_spec and value < range_spec['min']:
                    self.validation_errors.append(
                        f"Field '{field}' value {value} is below minimum {range_spec['min']}"
                    )
                if 'max' in range_spec and value > range_spec['max']:
                    self.validation_errors.append(
                        f"Field '{field}' value {value} exceeds maximum {range_spec['max']}"
                    )

        return len(self.validation_errors) == 0

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type"""
        type_mapping = {
            'string': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict
        }

        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type is None:
            return True

        return isinstance(value, expected_python_type)

    def get_errors(self) -> list[str]:
        """Get validation errors"""
        return self.validation_errors
