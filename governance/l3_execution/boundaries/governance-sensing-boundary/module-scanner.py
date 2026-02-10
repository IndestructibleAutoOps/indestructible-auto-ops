from pathlib import Path
from typing import Any, Dict, List

import yaml


class ModuleScanner:
    """Scan governance modules and their bindings."""

    def __init__(self, root_path: str | Path) -> None:
        self.root_path = Path(root_path)

    def find_modules(self) -> List[Path]:
        """Locate governance-binding.yaml files under the root path."""
        return list(self.root_path.rglob("governance-binding.yaml"))

    def load_binding(self, path: Path) -> Dict[str, Any]:
        """Load a governance binding file."""
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def scan(self) -> List[Dict[str, Any]]:
        """Return a summary of discovered governance modules."""
        results: List[Dict[str, Any]] = []
        for binding_path in self.find_modules():
            binding = self.load_binding(binding_path)
            results.append(
                {
                    "moduleid": binding.get("moduleid"),
                    "bindingpath": str(binding_path),
                    "valid": bool(binding),
                }
            )
        return results
