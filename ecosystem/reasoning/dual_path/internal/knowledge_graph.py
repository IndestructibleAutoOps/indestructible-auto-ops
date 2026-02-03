"""
Code Knowledge Graph
Builds and queries a multi-layer graph representing code structure
"""
import os
import json
import hashlib
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timezone
from collections import defaultdict

# Import simple_yaml for zero-dependency YAML parsing
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.simple_yaml import safe_load


class KnowledgeGraph:
    """
    Multi-layer code knowledge graph
    L1: Symbol graph - definitions and references
    L2: Call graph - function call relationships
    L3: Semantic graph - high-level concepts
    """
    
    def __init__(self, codebase_path: str, graph_db_uri: Optional[str] = None):
        """Initialize knowledge graph"""
        self.codebase_path = codebase_path
        self.graph_db_uri = graph_db_uri
        
        # Graph storage (in-memory for prototype, would use Neo4j in production)
        self.layers = {
            "L1_symbol_graph": defaultdict(dict),
            "L2_call_graph": defaultdict(list),
            "L3_semantic_graph": defaultdict(set)
        }
        
    def build_graph(self, codebase_path: str):
        """
        Build the multi-layer knowledge graph
        
        Args:
            codebase_path: Path to the codebase root
        """
        print(f"Building knowledge graph from {codebase_path}...")
        
        # L1: Symbol graph - parse code files
        self._build_symbol_graph(codebase_path)
        
        # L2: Call graph - analyze function calls
        self._build_call_graph(codebase_path)
        
        # L3: Semantic graph - infer high-level concepts
        self._build_semantic_graph()
        
        print("Knowledge graph built successfully")
        print(f"  L1 (Symbol): {len(self.layers['L1_symbol_graph'])} symbols")
        print(f"  L2 (Call): {len(self.layers['L2_call_graph'])} call relationships")
        print(f"  L3 (Semantic): {len(self.layers['L3_semantic_graph'])} concepts")
    
    def _build_symbol_graph(self, codebase_path: str):
        """
        Build L1 symbol graph
        Extracts function, class, and variable definitions
        """
        # Mock implementation - would use tree-sitter or ast in production
        python_files = self._find_files(codebase_path, "*.py")
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple regex-based extraction (mock)
                self._extract_symbols(file_path, content)
                
            except Exception as e:
                print(f"Warning: Could not parse {file_path}: {e}")
    
    def _extract_symbols(self, file_path: str, content: str):
        """Extract symbols from file content (mock implementation)"""
        # Mock: Detect common Python patterns
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Function definitions
            if line.strip().startswith('def '):
                func_name = line.split('(')[0].replace('def ', '').strip()
                self.layers['L1_symbol_graph'][func_name] = {
                    'type': 'function',
                    'file': file_path,
                    'line': i,
                    'checksum': hashlib.md5(line.encode()).hexdigest()[:16]
                }
            
            # Class definitions
            elif line.strip().startswith('class '):
                class_name = line.split('(')[0].replace('class ', '').strip().rstrip(':')
                self.layers['L1_symbol_graph'][class_name] = {
                    'type': 'class',
                    'file': file_path,
                    'line': i,
                    'checksum': hashlib.md5(line.encode()).hexdigest()[:16]
                }
    
    def _build_call_graph(self, codebase_path: str):
        """
        Build L2 call graph
        Analyzes function call relationships
        """
        # Mock implementation - would analyze AST in production
        
        # Add mock call relationships
        mock_calls = [
            ('process_task', 'execute_task'),
            ('execute_task', 'asyncio.create_task'),
            ('main', 'process_task'),
            ('execute_task', 'task_queue.put')
        ]
        
        for caller, callee in mock_calls:
            if caller in self.layers['L1_symbol_graph']:
                self.layers['L2_call_graph'][caller].append(callee)
    
    def _build_semantic_graph(self):
        """
        Build L3 semantic graph
        Infers high-level concepts from symbols and calls
        """
        # Mock semantic concepts
        concepts = {
            'async_execution': ['process_task', 'execute_task', 'asyncio.create_task'],
            'task_management': ['task_queue', 'process_task', 'main'],
            'worker_runtime': ['gl-execution-runtime', 'worker', 'executor']
        }
        
        for concept, symbols in concepts.items():
            for symbol in symbols:
                if symbol in self.layers['L1_symbol_graph']:
                    self.layers['L3_semantic_graph'][concept].add(symbol)
    
    def query_context(self, symbol: str, depth: int = 3) -> Dict:
        """
        Query context for a symbol
        
        Args:
            symbol: Symbol name
            depth: Depth of context to retrieve
            
        Returns:
            Dictionary with context information
        """
        context = {
            "symbol": symbol,
            "definition": None,
            "callers": [],
            "callees": [],
            "related_concepts": [],
            "ancestors": [],
            "descendants": []
        }
        
        # Get symbol definition (L1)
        if symbol in self.layers['L1_symbol_graph']:
            context["definition"] = self.layers['L1_symbol_graph'][symbol]
        
        # Get callers (who calls this function) (L2)
        for caller, callees in self.layers['L2_call_graph'].items():
            if symbol in callees:
                if caller in self.layers['L1_symbol_graph']:
                    context["callers"].append({
                        "symbol": caller,
                        "location": self.layers['L1_symbol_graph'][caller]
                    })
        
        # Get callees (what this function calls) (L2)
        if symbol in self.layers['L2_call_graph']:
            for callee in self.layers['L2_call_graph'][symbol]:
                if callee in self.layers['L1_symbol_graph']:
                    context["callees"].append({
                        "symbol": callee,
                        "location": self.layers['L1_symbol_graph'][callee]
                    })
        
        # Get related concepts (L3)
        for concept, symbols in self.layers['L3_semantic_graph'].items():
            if symbol in symbols:
                context["related_concepts"].append({
                    "concept": concept,
                    "related_symbols": list(symbols - {symbol})
                })
        
        # Get ancestors (call chain upstream)
        context["ancestors"] = self._get_ancestors(symbol, depth)
        
        # Get descendants (call chain downstream)
        context["descendants"] = self._get_descendants(symbol, depth)
        
        return context
    
    def _get_ancestors(self, symbol: str, depth: int) -> List[Dict]:
        """Get ancestor symbols in call chain"""
        ancestors = []
        visited = set()
        current_level = [symbol]
        
        for _ in range(depth):
            next_level = []
            for s in current_level:
                for caller, callees in self.layers['L2_call_graph'].items():
                    if s in callees and caller not in visited:
                        ancestors.append({
                            "symbol": caller,
                            "level": len(ancestors) + 1
                        })
                        visited.add(caller)
                        next_level.append(caller)
            current_level = next_level
        
        return ancestors[:depth]
    
    def _get_descendants(self, symbol: str, depth: int) -> List[Dict]:
        """Get descendant symbols in call chain"""
        descendants = []
        visited = set()
        current_level = [symbol]
        
        for _ in range(depth):
            next_level = []
            for s in current_level:
                if s in self.layers['L2_call_graph']:
                    for callee in self.layers['L2_call_graph'][s]:
                        if callee not in visited:
                            descendants.append({
                                "symbol": callee,
                                "level": len(descendants) + 1
                            })
                            visited.add(callee)
                            next_level.append(callee)
            current_level = next_level
        
        return descendants[:depth]
    
    def find_related_symbols(self, symbol: str, 
                             relation_type: str = "all") -> List[Dict]:
        """
        Find symbols related to a given symbol
        
        Args:
            symbol: Base symbol
            relation_type: Type of relation (callers, callees, same_concept, all)
            
        Returns:
            List of related symbols with metadata
        """
        related = []
        
        context = self.query_context(symbol)
        
        if relation_type in ["callers", "all"]:
            for caller in context["callers"]:
                related.append({
                    "symbol": caller["symbol"],
                    "relation": "caller",
                    "location": caller["location"]
                })
        
        if relation_type in ["callees", "all"]:
            for callee in context["callees"]:
                related.append({
                    "symbol": callee["symbol"],
                    "relation": "callee",
                    "location": callee["location"]
                })
        
        if relation_type in ["same_concept", "all"]:
            for concept in context["related_concepts"]:
                for symbol in concept["related_symbols"]:
                    if symbol in self.layers['L1_symbol_graph']:
                        related.append({
                            "symbol": symbol,
                            "relation": "same_concept",
                            "concept": concept["concept"],
                            "location": self.layers['L1_symbol_graph'][symbol]
                        })
        
        return related
    
    def export_graph(self, output_path: str, format: str = "json"):
        """
        Export knowledge graph to file
        
        Args:
            output_path: Output file path
            format: Export format (json, yaml, graphml)
        """
        export_data = {
            "metadata": {
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "codebase_path": self.codebase_path,
                "graph_version": "1.0.0"
            },
            "layers": {
                "L1_symbol_graph": dict(self.layers['L1_symbol_graph']),
                "L2_call_graph": dict(self.layers['L2_call_graph']),
                "L3_semantic_graph": {
                    k: list(v) for k, v in self.layers['L3_semantic_graph'].items()
                }
            }
        }
        
        if format == "json":
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        elif format == "yaml":
            with open(output_path, 'w') as f:
                yaml.dump(export_data, f, default_flow_style=False)
        
        print(f"Knowledge graph exported to {output_path}")
    
    def _find_files(self, root: str, pattern: str) -> List[str]:
        """Find files matching pattern"""
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if filename.endswith(pattern.replace('*', '')):
                    files.append(os.path.join(dirpath, filename))
        return files


if __name__ == "__main__":
    # Test knowledge graph
    graph = KnowledgeGraph(codebase_path="/workspace/machine-native-ops")
    
    # Build graph
    graph.build_graph("/workspace/machine-native-ops")
    
    # Query context for a symbol
    context = graph.query_context("process_task", depth=2)
    
    print("\n\nContext for 'process_task':")
    print(json.dumps(context, indent=2))
    
    # Find related symbols
    related = graph.find_related_symbols("process_task", relation_type="all")
    
    print(f"\n\nRelated symbols (found {len(related)}):")
    for rel in related:
        print(f"  - {rel['symbol']} ({rel['relation']})")
    
    # Export graph
    graph.export_graph("/workspace/machine-native-ops/ecosystem/indexes/internal/knowledge_graph.json")