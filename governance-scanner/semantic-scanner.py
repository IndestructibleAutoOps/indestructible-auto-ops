from pathlib import Path

import yaml


class SemanticScanner:
    """Validate whether modules are attached to the semantic tree."""

    def __init__(self, semantic_tree_path: str | Path) -> None:
        with Path(semantic_tree_path).open("r", encoding="utf-8") as file:
            tree = yaml.safe_load(file) or {}
        self.nodes = tree.get("semantic_tree", {}).get("nodes", [])

    def scan_attachment(self, module_id: str) -> bool:
        """Return True if the module id exists in the semantic tree."""
        return any(node.get("id") == module_id for node in self.nodes)
