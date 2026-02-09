#!/usr/bin/env python3
"""
@GL-governed
@GL-layer: GL30-49
@GL-semantic: governance-mapping
@GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json

NG Era Mapping Engine
Handles cross-era namespace mapping (Era-1 ↔ Era-2 ↔ Era-3)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class Era(Enum):
    ERA1 = "Era-1"
    ERA2 = "Era-2"
    ERA3 = "Era-3"

@dataclass
class NGMapping:
    """NG Namespace Mapping"""
    source_era: Era
    target_era: Era
    source_ng_code: str
    target_ng_code: str
    transformation_rule: str
    bidirectional: bool = True

@dataclass
class MappingResult:
    """Namespace Mapping Result"""
    source_namespace: str
    target_namespace: str
    mapping_confidence: float
    transformation_applied: str
    warnings: List[str] = field(default_factory=list)

class NGEraMappingEngine:
    """NG Era Mapping Engine"""
    
    def __init__(self):
        # NG90100: Cross-Era Namespace Mapping rules
        self.mapping_rules = self._load_mapping_rules()
        
    def _load_mapping_rules(self) -> Dict[str, NGMapping]:
        """Load NG90100 mapping rules"""
        return {
            # Era-1 → Era-2 mappings
            "NG10100_NG30100": NGMapping(
                source_era=Era.ERA1,
                target_era=Era.ERA2,
                source_ng_code="NG10100",
                target_ng_code="NG30100",
                transformation_rule="code_package → microservice_boundary",
                bidirectional=True
            ),
            "NG10200_NG30200": NGMapping(
                source_era=Era.ERA1,
                target_era=Era.ERA2,
                source_ng_code="NG10200",
                target_ng_code="NG30200",
                transformation_rule="class → service_mesh_component",
                bidirectional=True
            ),
            "NG10300_NG30300": NGMapping(
                source_era=Era.ERA1,
                target_era=Era.ERA2,
                source_ng_code="NG10300",
                target_ng_code="NG30300",
                transformation_rule="method → event_stream",
                bidirectional=True
            ),
            "NG20600_NG40300": NGMapping(
                source_era=Era.ERA1,
                target_era=Era.ERA2,
                source_ng_code="NG20600",
                target_ng_code="NG40300",
                transformation_rule="database_table → data_shard",
                bidirectional=True
            ),
            
            # Era-2 → Era-3 mappings
            "NG30100_NG60100": NGMapping(
                source_era=Era.ERA2,
                target_era=Era.ERA3,
                source_ng_code="NG30100",
                target_ng_code="NG60100",
                transformation_rule="microservice_boundary → business_intent",
                bidirectional=False
            ),
            "NG30300_NG60400": NGMapping(
                source_era=Era.ERA2,
                target_era=Era.ERA3,
                source_ng_code="NG30300",
                target_ng_code="NG60400",
                transformation_rule="event_stream → semantic_intent",
                bidirectional=False
            ),
            "NG30400_NG60500": NGMapping(
                source_era=Era.ERA2,
                target_era=Era.ERA3,
                source_ng_code="NG30400",
                target_ng_code="NG60500",
                transformation_rule="data_pipeline → neural_network_intent",
                bidirectional=False
            ),
            "NG30800_NG60800": NGMapping(
                source_era=Era.ERA2,
                target_era=Era.ERA3,
                source_ng_code="NG30800",
                target_ng_code="NG60800",
                transformation_rule="configuration_center → automation_policy",
                bidirectional=False
            ),
            "NG31000_NG80400": NGMapping(
                source_era=Era.ERA2,
                target_era=Era.ERA3,
                source_ng_code="NG31000",
                target_ng_code="NG80400",
                transformation_rule="circuit_breaker → self_protecting_system",
                bidirectional=False
            ),
            
            # Cross-Era direct mappings
            "NG50000_UNIVERSAL": NGMapping(
                source_era=Era.ERA1,
                target_era=Era.ERA3,
                source_ng_code="NG50000",
                target_ng_code="NG50000",
                transformation_rule="security → universal (all eras)",
                bidirectional=False
            ),
            "NG10700_UNIVERSAL": NGMapping(
                source_era=Era.ERA1,
                target_era=Era.ERA3,
                source_ng_code="NG10700",
                target_ng_code="NG10700",
                transformation_rule="configuration → universal (all eras)",
                bidirectional=False
            ),
        }
    
    def map_namespace(
        self,
        namespace: str,
        source_era: Era,
        target_era: Era
    ) -> Optional[MappingResult]:
        """Map namespace from source era to target era"""
        
        # Find applicable mapping rule
        mapping_key = self._find_mapping_key(source_era, target_era, namespace)
        
        if not mapping_key:
            return None
        
        mapping = self.mapping_rules.get(mapping_key)
        if not mapping:
            return None
        
        # Apply transformation
        target_namespace = self._apply_transformation(
            namespace,
            mapping.transformation_rule
        )
        
        return MappingResult(
            source_namespace=namespace,
            target_namespace=target_namespace,
            mapping_confidence=0.95,  # High confidence for defined mappings
            transformation_applied=mapping.transformation_rule,
            warnings=[]
        )
    
    def _find_mapping_key(
        self,
        source_era: Era,
        target_era: Era,
        namespace: str
    ) -> Optional[str]:
        """Find the appropriate mapping key"""
        
        # Direct era-to-era mappings
        for key, mapping in self.mapping_rules.items():
            if mapping.source_era == source_era and mapping.target_era == target_era:
                return key
        
        return None
    
    def _apply_transformation(
        self,
        namespace: str,
        rule: str
    ) -> str:
        """Apply transformation rule to namespace"""
        
        transformations = {
            "code_package → microservice_boundary": lambda x: x.replace("com.", "").replace(".", "-"),
            "class → service_mesh_component": lambda x: x.replace("_", "-").lower(),
            "method → event_stream": lambda x: f"{x}-event",
            "database_table → data_shard": lambda x: f"{x}-shard",
            "microservice_boundary → business_intent": lambda x: f"intent-{x}",
            "event_stream → semantic_intent": lambda x: f"semantic-{x}",
            "data_pipeline → neural_network_intent": lambda x: f"nn-{x}",
            "configuration_center → automation_policy": lambda x: f"policy-{x}",
            "circuit_breaker → self_protecting_system": lambda x: f"protect-{x}",
        }
        
        transformer = transformations.get(rule, lambda x: x)
        return transformer(namespace)
    
    def validate_bidirectional_mapping(
        self,
        ns1: str,
        era1: Era,
        ns2: str,
        era2: Era
    ) -> Tuple[bool, str]:
        """Validate bidirectional mapping consistency"""
        
        # Map era1 → era2
        result1 = self.map_namespace(ns1, era1, era2)
        if not result1 or result1.target_namespace != ns2:
            return False, f"Era1→Era2 mapping failed: {ns1} → {result1.target_namespace if result1 else 'None'} (expected {ns2})"
        
        # Map era2 → era1 (if bidirectional)
        mapping_key = self._find_mapping_key(era1, era2, ns1)
        if mapping_key and self.mapping_rules[mapping_key].bidirectional:
            result2 = self.map_namespace(ns2, era2, era1)
            if not result2 or result2.target_namespace != ns1:
                return False, f"Era2→Era1 mapping failed: {ns2} → {result2.target_namespace if result2 else 'None'} (expected {ns1})"
        
        return True, "Bidirectional mapping validated"
    
    def generate_mapping_matrix(self) -> Dict:
        """Generate complete NG cross-era mapping matrix"""
        
        matrix = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ng_code": "NG90100",
            "era1_to_era2": {},
            "era2_to_era3": {},
            "direct_mappings": []
        }
        
        # Era-1 → Era-2 mappings
        for key, mapping in self.mapping_rules.items():
            if mapping.source_era == Era.ERA1 and mapping.target_era == Era.ERA2:
                matrix["era1_to_era2"][mapping.source_ng_code] = {
                    "target_ng_code": mapping.target_ng_code,
                    "transformation": mapping.transformation_rule,
                    "bidirectional": mapping.bidirectional
                }
        
        # Era-2 → Era-3 mappings
        for key, mapping in self.mapping_rules.items():
            if mapping.source_era == Era.ERA2 and mapping.target_era == Era.ERA3:
                matrix["era2_to_era3"][mapping.source_ng_code] = {
                    "target_ng_code": mapping.target_ng_code,
                    "transformation": mapping.transformation_rule,
                    "bidirectional": mapping.bidirectional
                }
        
        # Direct/universal mappings
        for key, mapping in self.mapping_rules.items():
            if "UNIVERSAL" in key:
                matrix["direct_mappings"].append({
                    "ng_code": mapping.source_ng_code,
                    "description": mapping.transformation_rule
                })
        
        return matrix
    
    def export_mapping_matrix(self, output_path: Path):
        """Export mapping matrix to JSON"""
        matrix = self.generate_mapping_matrix()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matrix, f, indent=2, ensure_ascii=False)

def main():
    """Main entry point for testing"""
    engine = NGEraMappingEngine()
    
    # Test mapping
    result = engine.map_namespace(
        "com.example.service",
        Era.ERA1,
        Era.ERA2
    )
    
    print(f"Mapping result: {result}")
    
    # Generate and export matrix
    output_path = Path("/workspace/ng-namespace-governance/analysis/ng-cross-era-matrix.json")
    engine.export_mapping_matrix(output_path)
    print(f"Mapping matrix exported to: {output_path}")

if __name__ == "__main__":
    main()