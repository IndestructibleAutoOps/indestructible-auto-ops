# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

# @GL-governed
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GL Code Intelligence & Security Layer - Capability Generator
Version 21.0.0

This module generates capabilities based on defined schemas and patterns.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

class CapabilityGenerator:
    """Generates capabilities from schemas and patterns"""
    
    def __init__(self, schema_path: str, pattern_path: str):
        self.schema_path = schema_path
        self.pattern_path = pattern_path
        self.capabilities: List[Dict[str, Any]] = []
    
    def generate_from_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate capability from schema definition"""
        capability = {
            "id": str(uuid.uuid4()),
            "name": schema.get("name", "Unnamed Capability"),
            "version": schema.get("version", "1.0.0"),
            "category": schema.get("category", "deep-code-understanding"),
            "description": schema.get("description", ""),
            "inputs": schema.get("inputs", []),
            "outputs": schema.get("outputs", []),
            "dimensions": schema.get("dimensions", {}),
            "guarantees": schema.get("guarantees", []),
            "metadata": {
                "author": schema.get("author", "GL Auto-Generator"),
                "created-at": datetime.now().isoformat(),
                "updated-at": datetime.now().isoformat(),
                "tags": schema.get("tags", [])
            },
            "evolution": {
                "generation": 1,
                "usage-count": 0,
                "success-rate": 1.0,
                "average-performance": 0.0
            }
        }
        
        self.capabilities.append(capability)
        return capability
    
    def generate_from_pattern(self, pattern: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate capabilities from pattern definitions"""
        capabilities = []
        
        # Create capability for each pattern type
        pattern_type = pattern.get("type", "security")
        severity = pattern.get("severity", "high")
        
        # Generate base capability
        capability = {
            "id": str(uuid.uuid4()),
            "name": f"{pattern_type}-{severity}-detector",
            "version": "1.0.0",
            "category": self._map_pattern_to_category(pattern_type),
            "description": f"Detects {pattern_type} issues with {severity} severity",
            "inputs": [
                {
                    "id": "source-code",
                    "type": "sourcecode",
                    "description": "Source code to analyze",
                    "required": True
                }
            ],
            "outputs": [
                {
                    "id": "issues",
                    "type": "risk-profile",
                    "description": f"Detected {pattern_type} issues",
                    "format": "sarif"
                }
            ],
            "dimensions": pattern.get("metrics", {}),
            "guarantees": [
                {
                    "type": "accuracy",
                    "description": "High accuracy in detecting issues"
                }
            ],
            "metadata": {
                "author": "GL Pattern Generator",
                "created-at": datetime.now().isoformat(),
                "updated-at": datetime.now().isoformat(),
                "tags": [pattern_type, severity, "auto-generated"]
            },
            "evolution": {
                "generation": 1,
                "usage-count": 0,
                "success-rate": 1.0,
                "average-performance": 0.0
            }
        }
        
        capabilities.append(capability)
        self.capabilities.extend(capabilities)
        
        return capabilities
    
    def _map_pattern_to_category(self, pattern_type: str) -> str:
        """Map pattern type to capability category"""
        mapping = {
            "security": "security-hardening",
            "performance": "performance-optimization",
            "architecture": "architecture-refactoring"
        }
        return mapping.get(pattern_type, "deep-code-understanding")
    
    def get_capabilities(self) -> List[Dict[str, Any]]:
        """Get all generated capabilities"""
        return self.capabilities
    
    def save_capabilities(self, output_path: str):
        """Save capabilities to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.capabilities, f, indent=2)


if __name__ == "__main__":
    # Example usage
    generator = CapabilityGenerator(
        schema_path="./capability-schema",
        pattern_path="./pattern-library"
    )
    
    # Generate from schema
    schema = {
        "name": "Example Detector",
        "category": "security-hardening",
        "description": "Example capability"
    }
    capability = generator.generate_from_schema(schema)
    print(f"Generated capability: {capability['name']}")