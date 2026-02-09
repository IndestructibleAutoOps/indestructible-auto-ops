import hashlib
from pathlib import Path
from typing import Any, Dict

import yaml


class IntegrityScanner:
    """Scan hash boundaries defined in the hash specification."""

    def __init__(self, hash_spec_path: str | Path) -> None:
        self.hash_spec_path = Path(hash_spec_path)
        with self.hash_spec_path.open("r", encoding="utf-8") as file:
            self.hash_spec: Dict[str, Any] = yaml.safe_load(file) or {}

    def compute_hash(self, path: Path) -> str:
        """Compute a SHA-256 hash for a file."""
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def compute_directory_hash(self, directory: Path) -> str:
        """Compute a deterministic hash for all files under a directory."""
        digest = hashlib.sha256()
        for file_path in sorted(p for p in directory.rglob("*") if p.is_file()):
            digest.update(str(file_path.relative_to(directory)).encode("utf-8"))
            digest.update(self.compute_hash(file_path).encode("utf-8"))
        return digest.hexdigest()

    def scan(self) -> Dict[str, str]:
        """Return hashes for all included paths in the hash specification."""
        spec = self.hash_spec.get("hash_spec", {})
        include = spec.get("include", [])
        results: Dict[str, str] = {}

        for pattern in include:
            target = Path(pattern)
            if target.is_file():
                results[str(target)] = self.compute_hash(target)
            elif target.is_dir():
                results[str(target)] = self.compute_directory_hash(target)

        return results
