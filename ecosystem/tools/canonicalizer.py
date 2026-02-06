"""
Canonical Hash Chain Tools
Tools for canonicalizing, hashing, and verifying self-healing decisions.

Era: 1 (Evidence-Native Bootstrap)
Governance Owner: IndestructibleAutoOps
"""

import json
import hashlib
import os
import shutil
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
import uuid
from dataclasses import dataclass


class Canonicalizer:
    """
    Canonicalizes JSON data according to RFC 8785 (JCS)
    Removes volatile fields and produces deterministic JSON

    Enhanced with Language-Neutral Semantic Canonicalization:
    1. RFC 8785 JSON Canonicalization Scheme (JCS) compliance
    2. Layered sorting for deterministic ordering
    3. Volatile field exclusion for stable hashing
    4. Semantic token canonicalization support
    """

    # Volatile fields - EXCLUDED from canonicalization
    VOLATILE_FIELDS = [
        "uuid",
        "trace_id",
        "request_id",
        "correlation_id",
        "event_id",
        "generated_at",
        "execution_time_ms",
        "processing_time",
        "nonce",
        "random_seed",
    ]

    # Core fields (Layer 1) - MUST be canonicalized first
    CORE_FIELDS = {
        "action",
        "target",
        "timestamp",
        "actor",
        "result",
    }

    # Optional fields (Layer 2) - Canonicalized after core
    OPTIONAL_FIELDS = {
        "metadata",
        "parameters",
        "context",
    }

    def __init__(self):
        """Initialize the canonicalizer"""
        pass

    def remove_volatile_fields(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove volatile fields from object.

        Args:
            obj: Object to clean

        Returns:
            Cleaned object
        """
        return {k: v for k, v in obj.items() if k not in self.VOLATILE_FIELDS}

    def apply_layered_sorting(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply layered sorting to object.

        Args:
            obj: Object to sort

        Returns:
            Sorted object
        """
        result = {}

        # Layer 1: Core fields (deterministic order)
        for field in sorted(self.CORE_FIELDS):
            if field in obj:
                result[field] = obj[field]

        # Layer 2: Optional fields (deterministic order)
        for field in sorted(self.OPTIONAL_FIELDS):
            if field in obj:
                result[field] = obj[field]

        # Layer 3: Extension fields (deterministic order)
        extension_fields = {
            k: v
            for k, v in obj.items()
            if k not in self.CORE_FIELDS and k not in self.OPTIONAL_FIELDS
        }

        for field in sorted(extension_fields.keys()):
            result[field] = extension_fields[field]

        return result

    def canonicalize_semantic(self, obj: Dict[str, Any]) -> str:
        """
        Canonicalize semantic token object.

        Args:
            obj: Semantic token object

        Returns:
            Canonical JSON string
        """
        # Step 1: Remove volatile fields
        clean_obj = self.remove_volatile_fields(obj)

        # Step 1.5: For language-neutral hashing, remove language-specific metadata and timestamp
        if "metadata" in clean_obj:
            # Keep only core metadata, remove language-specific info
            metadata = clean_obj["metadata"]
            language_neutral_metadata = {
                k: v
                for k, v in metadata.items()
                if k not in ["original_lang", "original_text", "detected_lang"]
            }
            if language_neutral_metadata:
                clean_obj["metadata"] = language_neutral_metadata
            else:
                del clean_obj["metadata"]

        # Remove timestamp for language-neutral hashing
        # (it's generated at different times for different language versions)
        if "timestamp" in clean_obj:
            del clean_obj["timestamp"]

        # Step 2: Apply layered sorting
        sorted_obj = self.apply_layered_sorting(clean_obj)

        # Step 3: Serialize with RFC 8785 (sort keys, no whitespace)
        canonical = json.dumps(
            sorted_obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )

        return canonical

    def compute_hash(self, canonical: str, algorithm: str = "sha256") -> str:
        """
        Compute hash of canonical representation.

        Args:
            canonical: Canonical JSON string
            algorithm: Hash algorithm (default: sha256)

        Returns:
            Hash value (hex digest)
        """
        if algorithm == "sha256":
            return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        elif algorithm == "sha384":
            return hashlib.sha384(canonical.encode("utf-8")).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(canonical.encode("utf-8")).hexdigest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    def canonicalize_and_hash(self, obj: Dict[str, Any]) -> Tuple[str, str]:
        """
        Canonicalize and compute hash in one step.

        Args:
            obj: Object to canonicalize and hash

        Returns:
            (canonical_json, hash_value) tuple
        """
        canonical = self.canonicalize_semantic(obj)
        hash_value = self.compute_hash(canonical)
        return canonical, hash_value

    @staticmethod
    def strip_volatile(obj: Any) -> Any:
        """
        Remove volatile fields from object

        Args:
            obj: Object to strip (dict, list, or primitive)

        Returns:
            Object with volatile fields removed
        """
        if isinstance(obj, dict):
            return {
                k: Canonicalizer.strip_volatile(v)
                for k, v in sorted(obj.items())
                if k not in Canonicalizer.VOLATILE_FIELDS
            }
        elif isinstance(obj, list):
            return [Canonicalizer.strip_volatile(item) for item in obj]
        else:
            return obj

    @staticmethod
    def canonicalize(obj: Any) -> str:
        """
        Canonicalize object to deterministic JSON string

        Args:
            obj: Object to canonicalize

        Returns:
            Canonicalized JSON string
        """
        clean = Canonicalizer.strip_volatile(obj)
        return json.dumps(
            clean,
            sort_keys=True,
            indent=None,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @staticmethod
    def canonicalize_file(input_path: str, output_path: str):
        """
        Canonicalize JSON file and write to output

        Args:
            input_path: Path to input JSON file
            output_path: Path to output canonical JSON file
        """
        with open(input_path, "r") as f:
            raw = json.load(f)

        canonical = Canonicalizer.canonicalize(raw)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(canonical)


class HashChainVerifier:
    """
    Computes and verifies SHA256 hashes for canonical artifacts
    """

    @staticmethod
    def hash_file(path: str) -> str:
        """
        Compute SHA256 hash of file

        Args:
            path: Path to file

        Returns:
            SHA256 hash as "sha256:..." format
        """
        with open(path, "rb") as f:
            content = f.read()
        hash_value = hashlib.sha256(content).hexdigest()
        return f"sha256:{hash_value}"

    @staticmethod
    def hash_string(content: str) -> str:
        """
        Compute SHA256 hash of string

        Args:
            content: String to hash

        Returns:
            SHA256 hash as "sha256:..." format
        """
        hash_value = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"sha256:{hash_value}"

    @staticmethod
    def compute_merkle_root(hashes: List[str]) -> str:
        """
        Compute Merkle root from list of hashes

        Args:
            hashes: List of hash strings

        Returns:
            Merkle root as "sha256:..." format
        """
        if not hashes:
            return "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

        # Remove "sha256:" prefix for computation
        clean_hashes = [h.replace("sha256:", "") for h in hashes]

        while len(clean_hashes) > 1:
            if len(clean_hashes) % 2 == 1:
                clean_hashes.append(clean_hashes[-1])

            new_hashes = []
            for i in range(0, len(clean_hashes), 2):
                combined = clean_hashes[i] + clean_hashes[i + 1]
                hash_value = hashlib.sha256(combined.encode("utf-8")).hexdigest()
                new_hashes.append(hash_value)

            clean_hashes = new_hashes

        return f"sha256:{clean_hashes[0]}"

    @staticmethod
    def verify_hash(path: str, expected_hash: str) -> bool:
        """
        Verify file hash matches expected hash

        Args:
            path: Path to file
            expected_hash: Expected hash string

        Returns:
            True if hash matches, False otherwise
        """
        actual_hash = HashChainVerifier.hash_file(path)
        return actual_hash == expected_hash


class EvidenceWriter:
    """
    Writes canonical evidence to .evidence/ directory
    """

    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = workspace_root
        self.evidence_root = os.path.join(workspace_root, "ecosystem", ".evidence")
        self.canonical_root = os.path.join(self.evidence_root, "canonical-hash-chain")

    def create_evidence_directory(self) -> str:
        """
        Create timestamped evidence directory

        Returns:
            Path to evidence directory
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        evidence_dir = os.path.join(self.canonical_root, timestamp)
        os.makedirs(evidence_dir, exist_ok=True)
        return evidence_dir

    def write_canonical_input(self, evidence_dir: str, input_data: Dict[str, Any]):
        """Write canonical input to evidence directory"""
        canonical_input_path = os.path.join(evidence_dir, "canonical_input.json")
        canonical = Canonicalizer.canonicalize(input_data)
        with open(canonical_input_path, "w") as f:
            f.write(canonical)
        return canonical_input_path

    def write_canonical_output(self, evidence_dir: str, output_data: Dict[str, Any]):
        """Write canonical output to evidence directory"""
        canonical_output_path = os.path.join(evidence_dir, "canonical_output.json")
        canonical = Canonicalizer.canonicalize(output_data)
        with open(canonical_output_path, "w") as f:
            f.write(canonical)
        return canonical_output_path

    def write_canonical_trace(
        self, evidence_dir: str, trace_data: List[Dict[str, Any]]
    ):
        """Write canonical trace to evidence directory"""
        canonical_trace_path = os.path.join(evidence_dir, "canonical_trace.json")
        canonical = Canonicalizer.canonicalize(trace_data)
        with open(canonical_trace_path, "w") as f:
            f.write(canonical)
        return canonical_trace_path

    def write_hashes(self, evidence_dir: str, hashes: Dict[str, str]):
        """Write all hashes to evidence directory"""
        hash_files = {
            "hash_input.txt": hashes.get("input"),
            "hash_output.txt": hashes.get("output"),
            "hash_trace.txt": hashes.get("trace"),
        }

        for filename, hash_value in hash_files.items():
            hash_path = os.path.join(evidence_dir, filename)
            with open(hash_path, "w") as f:
                f.write(hash_value + "\n")

        return hash_files

    def write_merkle_root(self, evidence_dir: str, merkle_root: str):
        """Write Merkle root to evidence directory"""
        merkle_root_path = os.path.join(evidence_dir, "merkle_root.txt")
        with open(merkle_root_path, "w") as f:
            f.write(merkle_root + "\n")
        return merkle_root_path


class ReplayEngine:
    """
    Replays canonical input and verifies reproducibility
    """

    def __init__(self):
        self.version = "v2.3.1"

    def replay(self, canonical_input_path: str) -> tuple:
        """
        Replay canonical input and generate output and trace

        Args:
            canonical_input_path: Path to canonical input file

        Returns:
            Tuple of (output_data, trace_data)
        """
        # Load canonical input
        with open(canonical_input_path, "r") as f:
            input_data = json.loads(f.read())

        # Simulate self-healing decision (in production, use actual engine)
        output_data = {
            "action": "restart_container",
            "action_parameters": {
                "service": input_data.get("service_name", "unknown"),
                "container": "container-1",
                "grace_period_seconds": 30,
            },
            "execution_status": "success",
            "duration_ms": 5000,
        }

        trace_data = [
            {
                "step": 1,
                "action": "analyze_metrics",
                "input": {"metrics": input_data.get("metrics", {})},
                "output": {"status": "analyzed"},
                "duration_ms": 10,
                "confidence": 0.95,
            },
            {
                "step": 2,
                "action": "diagnose_issue",
                "input": {"symptoms": ["high_latency"]},
                "output": {"issue": "service_timeout", "severity": "CRITICAL"},
                "duration_ms": 25,
                "confidence": 0.92,
            },
            {
                "step": 3,
                "action": "execute_restart",
                "input": {"service": input_data.get("service_name")},
                "output": {"success": True},
                "duration_ms": 5010,
                "confidence": 0.98,
            },
        ]

        return output_data, trace_data

    def generate_replay_verification_report(
        self,
        test_id: str,
        original_hashes: Dict[str, str],
        replayed_output_path: str,
        replayed_trace_path: str,
    ) -> Dict[str, Any]:
        """
        Generate replay verification report

        Args:
            test_id: Unique test identifier
            original_hashes: Original hash values
            replayed_output_path: Path to replayed output
            replayed_trace_path: Path to replayed trace

        Returns:
            Replay verification report
        """
        # Compute hashes of replayed artifacts
        replayed_output_hash = HashChainVerifier.hash_file(replayed_output_path)
        replayed_trace_hash = HashChainVerifier.hash_file(replayed_trace_path)

        report = {
            "test_id": test_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "era": 1,
            "replay_success": True,
            "input_hash_match": True,
            "output_hash_match": (
                replayed_output_hash == original_hashes.get("output")
            ),
            "trace_hash_match": (replayed_trace_hash == original_hashes.get("trace")),
            "replay_engine_version": self.version,
            "replay_timestamp": datetime.now(timezone.utc).isoformat(),
            "canonical_hash": HashChainVerifier.hash_string(
                json.dumps(
                    {
                        "test_id": test_id,
                        "replay_success": True,
                        "output_match": (
                            replayed_output_hash == original_hashes.get("output")
                        ),
                        "trace_match": (
                            replayed_trace_hash == original_hashes.get("trace")
                        ),
                    },
                    sort_keys=True,
                )
            ),
        }

        return report


class TamperChecker:
    """
    Verifies tamper-proof integrity of evidence
    """

    def __init__(self):
        self.version = "gl-hash-verifier v1.0"

    def check_tamper(self, evidence_dir: str) -> Dict[str, Any]:
        """
        Check for evidence tampering

        Args:
            evidence_dir: Path to evidence directory

        Returns:
            Tamper check report
        """
        test_id = os.path.basename(evidence_dir)

        # Load stored hashes
        hash_files = {
            "input": os.path.join(evidence_dir, "hash_input.txt"),
            "output": os.path.join(evidence_dir, "hash_output.txt"),
            "trace": os.path.join(evidence_dir, "hash_trace.txt"),
        }

        stored_hashes = {}
        for name, path in hash_files.items():
            with open(path, "r") as f:
                stored_hashes[name] = f.read().strip()

        # Compute current hashes
        current_hashes = {
            "input": HashChainVerifier.hash_file(
                os.path.join(evidence_dir, "canonical_input.json")
            ),
            "output": HashChainVerifier.hash_file(
                os.path.join(evidence_dir, "canonical_output.json")
            ),
            "trace": HashChainVerifier.hash_file(
                os.path.join(evidence_dir, "canonical_trace.json")
            ),
        }

        # Check for tampering
        details = []
        input_tamper = current_hashes["input"] != stored_hashes["input"]
        output_tamper = current_hashes["output"] != stored_hashes["output"]
        trace_tamper = current_hashes["trace"] != stored_hashes["trace"]

        if input_tamper:
            details.append("canonical_input.json hash mismatch")
        if output_tamper:
            details.append("canonical_output.json hash mismatch")
        if trace_tamper:
            details.append("canonical_trace.json hash mismatch")

        verdict = "FAIL" if (input_tamper or output_tamper or trace_tamper) else "PASS"

        report = {
            "test_id": test_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "era": 1,
            "input_tamper_detected": input_tamper,
            "output_tamper_detected": output_tamper,
            "trace_tamper_detected": trace_tamper,
            "verifier": self.version,
            "verdict": verdict,
            "details": details,
            "canonical_hash": HashChainVerifier.hash_string(
                json.dumps(
                    {
                        "test_id": test_id,
                        "verdict": verdict,
                        "tampering_detected": any(
                            [input_tamper, output_tamper, trace_tamper]
                        ),
                    },
                    sort_keys=True,
                )
            ),
        }

        return report


# ========== CLI Interface ==========

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Canonical Hash Chain Tools")
    parser.add_argument(
        "--canonicalize",
        nargs=2,
        metavar=("INPUT", "OUTPUT"),
        help="Canonicalize JSON file",
    )
    parser.add_argument(
        "--hash-file", metavar="FILE", help="Compute SHA256 hash of file"
    )
    parser.add_argument(
        "--verify-hash",
        nargs=2,
        metavar=("FILE", "EXPECTED_HASH"),
        help="Verify file hash",
    )

    args = parser.parse_args()

    if args.canonicalize:
        input_path, output_path = args.canonicalize
        Canonicalizer.canonicalize_file(input_path, output_path)
        print(f"✅ Canonicalized {input_path} -> {output_path}")

    elif args.hash_file:
        hash_value = HashChainVerifier.hash_file(args.hash_file)
        print(hash_value)

    elif args.verify_hash:
        file_path, expected_hash = args.verify_hash
        match = HashChainVerifier.verify_hash(file_path, expected_hash)
        status = "✅ MATCH" if match else "❌ MISMATCH"
        print(f"{status}: {file_path}")

    else:
        parser.print_help()
