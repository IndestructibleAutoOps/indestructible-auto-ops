# @GL-semantic: org.mnga.engines.reverse-architecture@1.0.0
# @GL-audit-trail: enabled
"""
Reverse Architecture Engine - Analyze and document existing architecture
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ArchitectureComponent:
    """Represents a component in the architecture"""

    name: str
    type: str
    path: str
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchitectureAnalysis:
    """Result of architecture analysis"""

    components: List[ArchitectureComponent] = field(default_factory=list)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    layers: Dict[str, List[str]] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


class ReverseArchitectureEngine:
    """
    Reverse Architecture Engine for analyzing and documenting existing architecture.

    This engine scans the codebase, identifies components, analyzes dependencies,
    and generates comprehensive architecture documentation.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize Reverse Architecture Engine

        Args:
            workspace_root: Root directory of the workspace
        """
        if workspace_root is None:
            # .../ecosystem/governance/engines/reverse-architecture/* -> repo root
            workspace_root = str(Path(__file__).resolve().parents[4])

        self.workspace_root = workspace_root
        self.ecosystem_root = os.path.join(workspace_root, "ecosystem")
        self.output_dir = os.path.join(
            workspace_root, "ecosystem", "governance", "docs", "architecture"
        )

    def analyze(self) -> ArchitectureAnalysis:
        """
        Perform comprehensive architecture analysis

        Returns:
            ArchitectureAnalysis with complete analysis results
        """
        print("=== Reverse Architecture Engine: Starting Analysis ===")
        print(f"Workspace: {self.workspace_root}")
        print(f"Ecosystem Root: {self.ecosystem_root}")
        print()

        analysis = ArchitectureAnalysis()

        # Step 1: Identify all components
        print("Step 1: Identifying components...")
        components = self._identify_components()
        analysis.components = components
        print(f"Found {len(components)} components")
        print()

        # Step 2: Analyze dependencies
        print("Step 2: Analyzing dependencies...")
        dependency_graph = self._analyze_dependencies(components)
        analysis.dependency_graph = dependency_graph
        print(f"Analyzed {len(dependency_graph)} dependency relationships")
        print()

        # Step 3: Identify layers
        print("Step 3: Identifying layers...")
        layers = self._identify_layers(components)
        analysis.layers = layers
        print(f"Identified {len(layers)} layers")
        for layer_name, layer_components in layers.items():
            print(f"  {layer_name}: {len(layer_components)} components")
        print()

        # Step 4: Calculate metrics
        print("Step 4: Calculating metrics...")
        metrics = self._calculate_metrics(components, dependency_graph, layers)
        analysis.metrics = metrics
        print("Metrics calculated:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        print()

        # Step 5: Generate documentation
        print("Step 5: Generating documentation...")
        self._generate_documentation(analysis)
        print("Documentation generated")
        print()

        print("=== Analysis Complete ===")
        return analysis

    def _identify_components(self) -> List[ArchitectureComponent]:
        """
        Identify all components in the architecture

        Returns:
            List of ArchitectureComponent objects
        """
        components = []

        # Scan ecosystem directory
        for root, dirs, files in os.walk(self.ecosystem_root):
            # Skip hidden directories and common non-code directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["__pycache__", "node_modules", ".git"]
            ]

            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.workspace_root)

                # Identify component type
                component_type = self._identify_component_type(file)

                if component_type:
                    component_name = self._get_component_name(rel_path)

                    component = ArchitectureComponent(
                        name=component_name,
                        type=component_type,
                        path=rel_path,
                        metadata={
                            "size": os.path.getsize(file_path),
                            "modified": datetime.fromtimestamp(
                                os.path.getmtime(file_path)
                            ).isoformat()
                            + "Z",
                        },
                    )
                    components.append(component)

        return sorted(components, key=lambda c: c.name)

    def _identify_component_type(self, filename: str) -> Optional[str]:
        """
        Identify component type from filename

        Args:
            filename: Name of the file

        Returns:
            Component type or None
        """
        extensions = {
            ".py": "python_module",
            ".yaml": "yaml_spec",
            ".yml": "yaml_spec",
            ".json": "json_schema",
            ".md": "documentation",
            ".txt": "text_file",
        }

        for ext, comp_type in extensions.items():
            if filename.endswith(ext):
                return comp_type

        return None

    def _get_component_name(self, file_path: str) -> str:
        """
        Extract component name from file path

        Args:
            file_path: Path to the file

        Returns:
            Component name
        """
        # Remove extension
        name = os.path.splitext(file_path)[0]
        # Replace path separators with dots
        name = name.replace("/", ".").replace("\\", ".")
        # Remove ecosystem prefix
        if name.startswith("ecosystem."):
            name = name[10:]

        return name

    def _analyze_dependencies(
        self, components: List[ArchitectureComponent]
    ) -> Dict[str, List[str]]:
        """
        Analyze dependencies between components

        Args:
            components: List of components

        Returns:
            Dependency graph as dict mapping component to its dependencies
        """
        dependency_graph = {}

        for component in components:
            dependencies = []

            # For Python modules, analyze imports
            if component.type == "python_module":
                dependencies = self._analyze_python_dependencies(component.path)

            # For YAML specs, analyze references
            elif component.type == "yaml_spec":
                dependencies = self._analyze_yaml_dependencies(component.path)

            # For JSON schemas, analyze $ref
            elif component.type == "json_schema":
                dependencies = self._analyze_json_dependencies(component.path)

            dependency_graph[component.name] = dependencies

            # Update component's dependencies
            component.dependencies = dependencies

        # Build dependents list
        for component in components:
            component.dependents = []
            for other_component in components:
                if component.name in other_component.dependencies:
                    component.dependents.append(other_component.name)

        return dependency_graph

    def _analyze_python_dependencies(self, file_path: str) -> List[str]:
        """
        Analyze Python module dependencies

        Args:
            file_path: Path to Python file (relative to workspace)

        Returns:
            List of dependency names
        """
        full_path = os.path.join(self.workspace_root, file_path)
        dependencies = []

        try:
            with open(full_path, "r") as f:
                content = f.read()

                # Find import statements
                import_keywords = ["import ", "from "]
                for line in content.split("\n"):
                    line = line.strip()
                    for keyword in import_keywords:
                        if line.startswith(keyword):
                            # Extract module name
                            module_part = line[len(keyword) :].split()[0]
                            # Clean up
                            module_name = module_part.split(".")[0]
                            if module_name and not module_name.startswith("."):
                                dependencies.append(module_name)
        except Exception as e:
            print(f"  Warning: Could not analyze {file_path}: {str(e)}")

        return list(set(dependencies))

    def _analyze_yaml_dependencies(self, file_path: str) -> List[str]:
        """
        Analyze YAML specification dependencies

        Args:
            file_path: Path to YAML file (relative to workspace)

        Returns:
            List of dependency names
        """
        full_path = os.path.join(self.workspace_root, file_path)
        dependencies = []

        try:
            with open(full_path, "r") as f:
                content = f.read()

                # Look for spec_id references
                if "spec_id:" in content:
                    for line in content.split("\n"):
                        if "spec_id:" in line and "org.mnga" in line:
                            # Extract spec_id value
                            spec_id = line.split("spec_id:")[1].strip()
                            dependencies.append(spec_id)
        except Exception as e:
            print(f"  Warning: Could not analyze {file_path}: {str(e)}")

        return list(set(dependencies))

    def _analyze_json_dependencies(self, file_path: str) -> List[str]:
        """
        Analyze JSON schema dependencies

        Args:
            file_path: Path to JSON file (relative to workspace)

        Returns:
            List of dependency names
        """
        full_path = os.path.join(self.workspace_root, file_path)
        dependencies = []

        try:
            with open(full_path, "r") as f:
                data = json.load(f)

                # Look for $ref references
                json_str = json.dumps(data)
                if "$ref" in json_str:
                    # Simple extraction of references
                    import re

                    refs = re.findall(r'\$ref["\s:]+([^"\s]+)', json_str)
                    dependencies.extend(refs)
        except Exception as e:
            print(f"  Warning: Could not analyze {file_path}: {str(e)}")

        return list(set(dependencies))

    def _identify_layers(
        self, components: List[ArchitectureComponent]
    ) -> Dict[str, List[str]]:
        """
        Identify architectural layers

        Args:
            components: List of components

        Returns:
            Dict mapping layer names to component names
        """
        layers = {
            "meta-spec": [],
            "ugs": [],
            "governance": [],
            "reasoning": [],
            "gates": [],
            "platform-cloud": [],
            "ecosystem-cloud": [],
            "contracts": [],
            "engines": [],
        }

        for component in components:
            # Determine layer based on path
            if "meta-spec" in component.path:
                layers["meta-spec"].append(component.name)
            elif "ugs" in component.path:
                layers["ugs"].append(component.name)
            elif "governance" in component.path and "ugs" not in component.path:
                layers["governance"].append(component.name)
            elif "reasoning" in component.path:
                layers["reasoning"].append(component.name)
            elif "gates" in component.path:
                layers["gates"].append(component.name)
            elif "platform-cloud" in component.path:
                layers["platform-cloud"].append(component.name)
            elif "ecosystem-cloud" in component.path:
                layers["ecosystem-cloud"].append(component.name)
            elif "contracts" in component.path:
                layers["contracts"].append(component.name)
            elif "engines" in component.path:
                layers["engines"].append(component.name)

        return layers

    def _calculate_metrics(
        self,
        components: List[ArchitectureComponent],
        dependency_graph: Dict[str, List[str]],
        layers: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        """
        Calculate architecture metrics

        Args:
            components: List of components
            dependency_graph: Dependency graph
            layers: Layer mapping

        Returns:
            Dict of metrics
        """
        metrics = {}

        # Component counts
        metrics["total_components"] = len(components)
        metrics["by_type"] = {}
        for component in components:
            comp_type = component.type
            metrics["by_type"][comp_type] = metrics["by_type"].get(comp_type, 0) + 1

        # Layer counts
        metrics["by_layer"] = {}
        for layer_name, layer_components in layers.items():
            metrics["by_layer"][layer_name] = len(layer_components)

        # Dependency metrics
        total_dependencies = sum(len(deps) for deps in dependency_graph.values())
        metrics["total_dependencies"] = total_dependencies
        metrics["avg_dependencies_per_component"] = (
            total_dependencies / len(components) if components else 0
        )

        # Find components with most dependencies
        dependency_counts = [
            (name, len(deps)) for name, deps in dependency_graph.items()
        ]
        dependency_counts.sort(key=lambda x: x[1], reverse=True)
        metrics["most_dependent"] = dependency_counts[:5]

        # Find components with most dependents
        dependent_counts = [(c.name, len(c.dependents)) for c in components]
        dependent_counts.sort(key=lambda x: x[1], reverse=True)
        metrics["most_coupled"] = dependent_counts[:5]

        return metrics

    def _generate_documentation(self, analysis: ArchitectureAnalysis) -> None:
        """
        Generate architecture documentation

        Args:
            analysis: Architecture analysis results
        """
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Generate components documentation
        components_file = os.path.join(self.output_dir, "components.md")
        with open(components_file, "w") as f:
            f.write("# Architecture Components\n\n")
            f.write(f"Generated: {analysis.timestamp}\n\n")
            f.write(f"Total Components: {len(analysis.components)}\n\n")

            for component in analysis.components:
                f.write(f"## {component.name}\n\n")
                f.write(f"- **Type**: {component.type}\n")
                f.write(f"- **Path**: {component.path}\n")
                f.write(f"- **Dependencies**: {len(component.dependencies)}\n")
                if component.dependencies:
                    f.write(f"  - {', '.join(component.dependencies)}\n")
                f.write(f"- **Dependents**: {len(component.dependents)}\n")
                if component.dependents:
                    f.write(f"  - {', '.join(component.dependents)}\n")
                f.write("\n")

        # Generate layers documentation
        layers_file = os.path.join(self.output_dir, "layers.md")
        with open(layers_file, "w") as f:
            f.write("# Architecture Layers\n\n")
            f.write(f"Generated: {analysis.timestamp}\n\n")

            for layer_name, layer_components in analysis.layers.items():
                f.write(f"## {layer_name}\n\n")
                f.write(f"Components: {len(layer_components)}\n\n")
                for component_name in layer_components:
                    f.write(f"- {component_name}\n")
                f.write("\n")

        # Generate metrics documentation
        metrics_file = os.path.join(self.output_dir, "metrics.md")
        with open(metrics_file, "w") as f:
            f.write("# Architecture Metrics\n\n")
            f.write(f"Generated: {analysis.timestamp}\n\n")

            f.write("## Overview\n\n")
            f.write(f"- **Total Components**: {analysis.metrics['total_components']}\n")
            f.write(
                f"- **Total Dependencies**: {analysis.metrics['total_dependencies']}\n"
            )
            f.write(
                f"- **Avg Dependencies/Component**: {analysis.metrics['avg_dependencies_per_component']:.2f}\n\n"
            )

            f.write("## By Type\n\n")
            for comp_type, count in analysis.metrics["by_type"].items():
                f.write(f"- **{comp_type}**: {count}\n")
            f.write("\n")

            f.write("## By Layer\n\n")
            for layer_name, count in analysis.metrics["by_layer"].items():
                f.write(f"- **{layer_name}**: {count}\n")
            f.write("\n")

            f.write("## Most Dependent Components\n\n")
            for idx, (name, count) in enumerate(analysis.metrics["most_dependent"], 1):
                f.write(f"{idx}. {name} ({count} dependencies)\n")
            f.write("\n")

            f.write("## Most Coupled Components\n\n")
            for idx, (name, count) in enumerate(analysis.metrics["most_coupled"], 1):
                f.write(f"{idx}. {name} ({count} dependents)\n")
            f.write("\n")

        # Generate JSON summary
        summary_file = os.path.join(self.output_dir, "architecture-summary.json")
        summary = {
            "timestamp": analysis.timestamp,
            "metrics": analysis.metrics,
            "layers": analysis.layers,
            "components": [
                {
                    "name": c.name,
                    "type": c.type,
                    "path": c.path,
                    "dependencies": c.dependencies,
                    "dependents": c.dependents,
                }
                for c in analysis.components
            ],
        }
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)


def main():
    """Main entry point for reverse architecture engine"""
    engine = ReverseArchitectureEngine()
    analysis = engine.analyze()

    print("✓ Architecture analysis completed successfully")
    return 0


if __name__ == "__main__":
    exit(main())
