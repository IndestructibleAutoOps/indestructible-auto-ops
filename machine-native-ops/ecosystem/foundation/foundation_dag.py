#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: foundation-dag
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Foundation Layer DAG (Directed Acyclic Graph)
=============================================
GL Layer: GL00-09 Strategic Layer (Foundation)

Defines and manages the foundational layer hierarchy:

    Language Layer (L0)
         ↓ defines
    Format Layer (L1)
         ↓ carries
    Semantic Layer (L2)

The DAG ensures:
- Language determines if format can exist
- Format determines if semantics can be carried
- Semantics determines if governance can be executed

This is the "Layer 0" that supports all other governance layers.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum


class FoundationLayer(Enum):
    """Foundation layer hierarchy"""
    LANGUAGE = 0  # L0 - Base layer
    FORMAT = 1    # L1 - Schema layer
    SEMANTIC = 2  # L2 - Meaning layer


@dataclass
class DAGNode:
    """Represents a node in the Foundation DAG"""
    id: str
    layer: FoundationLayer
    name: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DAGEdge:
    """Represents an edge in the Foundation DAG"""
    source: str
    target: str
    relation: str  # "defines", "carries", "validates"
    weight: float = 1.0


class FoundationDAG:
    """
    Manages the Foundation Layer DAG.
    
    The DAG defines relationships between:
    - Language Layer (parsers, validators)
    - Format Layer (schemas, structures)
    - Semantic Layer (meaning, governance rules)
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize the Foundation DAG"""
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent.parent.parent
        
        self.nodes: Dict[str, DAGNode] = {}
        self.edges: List[DAGEdge] = []
        
        self._initialize_core_nodes()
        self._initialize_core_edges()
    
    def _initialize_core_nodes(self):
        """Initialize core DAG nodes"""
        # Language Layer nodes (L0)
        language_nodes = [
            DAGNode(
                id="lang-yaml",
                layer=FoundationLayer.LANGUAGE,
                name="YAML Language",
                description="YAML parser and validator (restricted)",
                outputs=["fmt-gl-rule", "fmt-evidence", "fmt-contract", "fmt-adapter"]
            ),
            DAGNode(
                id="lang-json",
                layer=FoundationLayer.LANGUAGE,
                name="JSON Language",
                description="JSON parser and validator",
                outputs=["fmt-gl-meta", "fmt-semantic-index"]
            ),
            DAGNode(
                id="lang-markdown",
                layer=FoundationLayer.LANGUAGE,
                name="Markdown Language",
                description="Markdown parser (HTML-free)",
                outputs=["fmt-spec-doc"]
            ),
            DAGNode(
                id="lang-python",
                layer=FoundationLayer.LANGUAGE,
                name="Python Language",
                description="Python AST parser (restricted)",
                outputs=["fmt-enforcer"]
            ),
            DAGNode(
                id="lang-gldsl",
                layer=FoundationLayer.LANGUAGE,
                name="GL-DSL Language",
                description="Governance DSL parser",
                outputs=["fmt-gl-rule"],
                status="planned"
            )
        ]
        
        # Format Layer nodes (L1)
        format_nodes = [
            DAGNode(
                id="fmt-gl-meta",
                layer=FoundationLayer.FORMAT,
                name="GL Meta Format",
                description="Module metadata format (gl.meta.json)",
                dependencies=["lang-json"],
                outputs=["sem-module-identity"]
            ),
            DAGNode(
                id="fmt-gl-rule",
                layer=FoundationLayer.FORMAT,
                name="GL Rule Format",
                description="Governance rule format (GL*.yaml)",
                dependencies=["lang-yaml"],
                outputs=["sem-governance-rule"]
            ),
            DAGNode(
                id="fmt-semantic-index",
                layer=FoundationLayer.FORMAT,
                name="Semantic Index Format",
                description="Semantic index format (semantic-index.json)",
                dependencies=["lang-json"],
                outputs=["sem-anchor-relation"]
            ),
            DAGNode(
                id="fmt-evidence",
                layer=FoundationLayer.FORMAT,
                name="Evidence Format",
                description="Evidence record format (evidence.yaml)",
                dependencies=["lang-yaml"],
                outputs=["sem-proof"]
            ),
            DAGNode(
                id="fmt-contract",
                layer=FoundationLayer.FORMAT,
                name="Contract Format",
                description="Contract format (contract.yaml)",
                dependencies=["lang-yaml"],
                outputs=["sem-agreement"]
            ),
            DAGNode(
                id="fmt-adapter",
                layer=FoundationLayer.FORMAT,
                name="Adapter Format",
                description="Cloud adapter format (adapter.yaml)",
                dependencies=["lang-yaml"],
                outputs=["sem-integration"]
            ),
            DAGNode(
                id="fmt-spec-doc",
                layer=FoundationLayer.FORMAT,
                name="Spec Document Format",
                description="Specification document format (*.md)",
                dependencies=["lang-markdown"],
                outputs=["sem-documentation"]
            ),
            DAGNode(
                id="fmt-enforcer",
                layer=FoundationLayer.FORMAT,
                name="Enforcer Format",
                description="Governance enforcer format (*.py)",
                dependencies=["lang-python"],
                outputs=["sem-executor"]
            )
        ]
        
        # Semantic Layer nodes (L2)
        semantic_nodes = [
            DAGNode(
                id="sem-module-identity",
                layer=FoundationLayer.SEMANTIC,
                name="Module Identity",
                description="Module identification and versioning",
                dependencies=["fmt-gl-meta"]
            ),
            DAGNode(
                id="sem-governance-rule",
                layer=FoundationLayer.SEMANTIC,
                name="Governance Rule",
                description="Governance rule definition and enforcement",
                dependencies=["fmt-gl-rule"]
            ),
            DAGNode(
                id="sem-anchor-relation",
                layer=FoundationLayer.SEMANTIC,
                name="Anchor Relation",
                description="Semantic anchor and relation graph",
                dependencies=["fmt-semantic-index"]
            ),
            DAGNode(
                id="sem-proof",
                layer=FoundationLayer.SEMANTIC,
                name="Proof/Evidence",
                description="Governance compliance evidence",
                dependencies=["fmt-evidence"]
            ),
            DAGNode(
                id="sem-agreement",
                layer=FoundationLayer.SEMANTIC,
                name="Agreement/Contract",
                description="Governance contracts and SLAs",
                dependencies=["fmt-contract"]
            ),
            DAGNode(
                id="sem-integration",
                layer=FoundationLayer.SEMANTIC,
                name="Integration",
                description="External system integration",
                dependencies=["fmt-adapter"]
            ),
            DAGNode(
                id="sem-documentation",
                layer=FoundationLayer.SEMANTIC,
                name="Documentation",
                description="Specification and documentation",
                dependencies=["fmt-spec-doc"]
            ),
            DAGNode(
                id="sem-executor",
                layer=FoundationLayer.SEMANTIC,
                name="Executor",
                description="Governance execution logic",
                dependencies=["fmt-enforcer"]
            )
        ]
        
        # Add all nodes
        for node in language_nodes + format_nodes + semantic_nodes:
            self.nodes[node.id] = node
    
    def _initialize_core_edges(self):
        """Initialize core DAG edges"""
        # Language → Format edges (defines)
        self.edges.extend([
            DAGEdge("lang-yaml", "fmt-gl-rule", "defines"),
            DAGEdge("lang-yaml", "fmt-evidence", "defines"),
            DAGEdge("lang-yaml", "fmt-contract", "defines"),
            DAGEdge("lang-yaml", "fmt-adapter", "defines"),
            DAGEdge("lang-json", "fmt-gl-meta", "defines"),
            DAGEdge("lang-json", "fmt-semantic-index", "defines"),
            DAGEdge("lang-markdown", "fmt-spec-doc", "defines"),
            DAGEdge("lang-python", "fmt-enforcer", "defines"),
        ])
        
        # Format → Semantic edges (carries)
        self.edges.extend([
            DAGEdge("fmt-gl-meta", "sem-module-identity", "carries"),
            DAGEdge("fmt-gl-rule", "sem-governance-rule", "carries"),
            DAGEdge("fmt-semantic-index", "sem-anchor-relation", "carries"),
            DAGEdge("fmt-evidence", "sem-proof", "carries"),
            DAGEdge("fmt-contract", "sem-agreement", "carries"),
            DAGEdge("fmt-adapter", "sem-integration", "carries"),
            DAGEdge("fmt-spec-doc", "sem-documentation", "carries"),
            DAGEdge("fmt-enforcer", "sem-executor", "carries"),
        ])
        
        # Semantic → Semantic edges (validates/uses)
        self.edges.extend([
            DAGEdge("sem-governance-rule", "sem-proof", "validates"),
            DAGEdge("sem-executor", "sem-governance-rule", "executes"),
            DAGEdge("sem-agreement", "sem-executor", "constrains"),
        ])
    
    def get_node(self, node_id: str) -> Optional[DAGNode]:
        """Get node by ID"""
        return self.nodes.get(node_id)
    
    def get_nodes_by_layer(self, layer: FoundationLayer) -> List[DAGNode]:
        """Get all nodes in a layer"""
        return [n for n in self.nodes.values() if n.layer == layer]
    
    def get_dependencies(self, node_id: str) -> List[DAGNode]:
        """Get all dependencies of a node"""
        node = self.nodes.get(node_id)
        if not node:
            return []
        return [self.nodes[dep] for dep in node.dependencies if dep in self.nodes]
    
    def get_dependents(self, node_id: str) -> List[DAGNode]:
        """Get all nodes that depend on this node"""
        return [n for n in self.nodes.values() if node_id in n.dependencies]
    
    def validate_dag(self) -> Tuple[bool, List[str]]:
        """Validate the DAG is acyclic and well-formed"""
        errors = []
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            
            node = self.nodes.get(node_id)
            if node:
                for dep in node.dependencies:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True
            
            rec_stack.remove(node_id)
            return False
        
        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle(node_id):
                    errors.append(f"Cycle detected involving node: {node_id}")
        
        # Check all dependencies exist
        for node in self.nodes.values():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    errors.append(f"Node {node.id} has missing dependency: {dep}")
        
        # Check layer hierarchy
        for edge in self.edges:
            source = self.nodes.get(edge.source)
            target = self.nodes.get(edge.target)
            
            if source and target:
                if edge.relation == "defines" and source.layer.value >= target.layer.value:
                    errors.append(f"Invalid 'defines' edge: {edge.source} → {edge.target}")
                if edge.relation == "carries" and source.layer.value >= target.layer.value:
                    errors.append(f"Invalid 'carries' edge: {edge.source} → {edge.target}")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Export DAG as dictionary"""
        return {
            "version": self.VERSION,
            "metadata": {
                "created": datetime.now(timezone.utc).isoformat(),
                "layer": "foundation",
                "semantic": "foundation-dag"
            },
            "layers": {
                "L0_language": [n.id for n in self.get_nodes_by_layer(FoundationLayer.LANGUAGE)],
                "L1_format": [n.id for n in self.get_nodes_by_layer(FoundationLayer.FORMAT)],
                "L2_semantic": [n.id for n in self.get_nodes_by_layer(FoundationLayer.SEMANTIC)]
            },
            "nodes": {
                node_id: {
                    "layer": node.layer.name,
                    "name": node.name,
                    "description": node.description,
                    "dependencies": node.dependencies,
                    "outputs": node.outputs,
                    "status": node.status
                }
                for node_id, node in self.nodes.items()
            },
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "relation": edge.relation,
                    "weight": edge.weight
                }
                for edge in self.edges
            ]
        }
    
    def to_mermaid(self) -> str:
        """Generate Mermaid diagram of the DAG"""
        lines = [
            "graph TD",
            "    %% Foundation Layer DAG",
            "    %% Language → Format → Semantic",
            ""
        ]
        
        # Add subgraphs for each layer
        lines.append("    subgraph L0[\"Language Layer (L0)\"]")
        for node in self.get_nodes_by_layer(FoundationLayer.LANGUAGE):
            status_icon = "🟢" if node.status == "active" else "🟡"
            lines.append(f"        {node.id}[\"{status_icon} {node.name}\"]")
        lines.append("    end")
        lines.append("")
        
        lines.append("    subgraph L1[\"Format Layer (L1)\"]")
        for node in self.get_nodes_by_layer(FoundationLayer.FORMAT):
            lines.append(f"        {node.id}[\"{node.name}\"]")
        lines.append("    end")
        lines.append("")
        
        lines.append("    subgraph L2[\"Semantic Layer (L2)\"]")
        for node in self.get_nodes_by_layer(FoundationLayer.SEMANTIC):
            lines.append(f"        {node.id}[\"{node.name}\"]")
        lines.append("    end")
        lines.append("")
        
        # Add edges
        lines.append("    %% Edges")
        relation_styles = {
            "defines": "-->|defines|",
            "carries": "-->|carries|",
            "validates": "-.->|validates|",
            "executes": "-.->|executes|",
            "constrains": "-.->|constrains|"
        }
        
        for edge in self.edges:
            style = relation_styles.get(edge.relation, "-->")
            lines.append(f"    {edge.source} {style} {edge.target}")
        
        return "\n".join(lines)
    
    def generate_ascii_diagram(self) -> str:
        """Generate ASCII diagram of the layer hierarchy"""
        diagram = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        FOUNDATION LAYER HIERARCHY                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                    LANGUAGE LAYER (L0)                                  │ ║
║  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │ ║
║  │  │  YAML   │  │  JSON   │  │Markdown │  │ Python  │  │ GL-DSL  │       │ ║
║  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │ ║
║  └───────┼───────────┼───────────┼───────────┼───────────┼────────────────┘ ║
║          │ defines   │ defines   │ defines   │ defines   │ defines          ║
║          ▼           ▼           ▼           ▼           ▼                  ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                     FORMAT LAYER (L1)                                   │ ║
║  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │ ║
║  │  │GL-Rule  │  │GL-Meta  │  │Sem-Index│  │Evidence │  │Contract │       │ ║
║  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │ ║
║  └───────┼───────────┼───────────┼───────────┼───────────┼────────────────┘ ║
║          │ carries   │ carries   │ carries   │ carries   │ carries          ║
║          ▼           ▼           ▼           ▼           ▼                  ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                    SEMANTIC LAYER (L2)                                  │ ║
║  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │ ║
║  │  │Gov-Rule │  │Identity │  │Anchor   │  │ Proof   │  │Agreement│       │ ║
║  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  Language determines if Format can exist                                     ║
║  Format determines if Semantics can be carried                               ║
║  Semantics determines if Governance can be executed                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        return diagram


class UnifiedFoundationEnforcer:
    """
    Unified Foundation Layer Enforcer.
    
    Orchestrates validation across all foundation layers:
    1. Language Layer validation
    2. Format Layer validation
    3. Semantic Layer validation (via DAG)
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize unified enforcer"""
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent.parent.parent
        
        self.dag = FoundationDAG(str(self.project_root))
        
        # Import layer enforcers
        from .language import LanguageEnforcer
        from .format import FormatEnforcer
        
        self.language_enforcer = LanguageEnforcer(str(self.project_root))
        self.format_enforcer = FormatEnforcer(str(self.project_root))
    
    def validate(self, directory: Optional[Path] = None) -> Dict[str, Any]:
        """
        Run unified validation across all foundation layers.
        
        Returns:
            Comprehensive validation report
        """
        if directory is None:
            directory = self.project_root / "ecosystem"
        
        # Validate DAG structure
        dag_valid, dag_errors = self.dag.validate_dag()
        
        # Validate Language Layer
        language_results = self.language_enforcer.validate_directory(directory)
        
        # Validate Format Layer
        format_results = self.format_enforcer.validate_directory(directory)
        
        # Compute overall status
        overall_valid = (
            dag_valid and
            language_results["summary"]["invalid_files"] == 0 and
            format_results["summary"]["invalid_files"] == 0
        )
        
        return {
            "version": self.VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_valid": overall_valid,
            "layers": {
                "dag": {
                    "valid": dag_valid,
                    "errors": dag_errors,
                    "node_count": len(self.dag.nodes),
                    "edge_count": len(self.dag.edges)
                },
                "language": {
                    "valid": language_results["summary"]["invalid_files"] == 0,
                    "summary": language_results["summary"],
                    "violations": [
                        r for r in language_results["results"] if not r["valid"]
                    ][:10]  # Limit to 10
                },
                "format": {
                    "valid": format_results["summary"]["invalid_files"] == 0,
                    "summary": format_results["summary"],
                    "violations": [
                        r for r in format_results["results"] if not r["valid"]
                    ][:10]  # Limit to 10
                }
            },
            "dag_topology": self.dag.to_dict()
        }


def main():
    """Main entry point for Foundation DAG"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Foundation Layer DAG")
    parser.add_argument("--validate", action="store_true", help="Validate DAG structure")
    parser.add_argument("--diagram", action="store_true", help="Generate Mermaid diagram")
    parser.add_argument("--ascii", action="store_true", help="Generate ASCII diagram")
    parser.add_argument("--json", action="store_true", help="Export as JSON")
    parser.add_argument("--full", action="store_true", help="Run full validation")
    
    args = parser.parse_args()
    
    dag = FoundationDAG()
    
    if args.validate:
        valid, errors = dag.validate_dag()
        if valid:
            print("✅ DAG is valid")
        else:
            print("❌ DAG validation failed:")
            for error in errors:
                print(f"  - {error}")
    
    elif args.diagram:
        print(dag.to_mermaid())
    
    elif args.ascii:
        print(dag.generate_ascii_diagram())
    
    elif args.json:
        print(json.dumps(dag.to_dict(), indent=2))
    
    elif args.full:
        enforcer = UnifiedFoundationEnforcer()
        results = enforcer.validate()
        print(json.dumps(results, indent=2, default=str))
    
    else:
        # Default: show ASCII diagram and validation
        print(dag.generate_ascii_diagram())
        print("\nDAG Validation:")
        valid, errors = dag.validate_dag()
        if valid:
            print("  ✅ DAG structure is valid")
            print(f"  - Nodes: {len(dag.nodes)}")
            print(f"  - Edges: {len(dag.edges)}")
            print(f"  - Language Layer: {len(dag.get_nodes_by_layer(FoundationLayer.LANGUAGE))} nodes")
            print(f"  - Format Layer: {len(dag.get_nodes_by_layer(FoundationLayer.FORMAT))} nodes")
            print(f"  - Semantic Layer: {len(dag.get_nodes_by_layer(FoundationLayer.SEMANTIC))} nodes")
        else:
            print("  ❌ DAG validation failed:")
            for error in errors:
                print(f"    - {error}")


if __name__ == "__main__":
    main()
