import hashlib
from pathlib import Path
from typing import Any, Dict


class EvidenceVerificationEngine:
    """Verify evidence integrity using hash specifications."""

    def __init__(self, hash_spec: Dict[str, Any]) -> None:
        self.hash_spec = hash_spec

    def compute_hash(self, path: str | Path) -> str:
        """Compute a SHA-256 hash for the given file."""
        file_path = Path(path)
        digest = hashlib.sha256()
        with file_path.open("rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def verify(self, evidence_path: str | Path, expected_hash: str) -> bool:
        """Compare an evidence file hash with the expected hash."""
        actual_hash = self.compute_hash(evidence_path)
        return actual_hash == expected_hash
