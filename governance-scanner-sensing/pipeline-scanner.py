from pathlib import Path
from typing import Dict, List


class PipelineScanner:
    """Scan pipeline and gate directories for governance modules."""

    def __init__(self, root_path: str | Path) -> None:
        self.root_path = Path(root_path)

    def scan(self) -> List[Dict[str, List[str]]]:
        """Return discovered pipeline directories and their files."""
        results: List[Dict[str, List[str]]] = []
        for pipeline_dir in self.root_path.rglob("pipelines"):
            if pipeline_dir.is_dir():
                files = sorted(
                    [entry.name for entry in pipeline_dir.iterdir() if entry.is_file()]
                )
                results.append({"path": str(pipeline_dir), "pipelines": files})
        return results
