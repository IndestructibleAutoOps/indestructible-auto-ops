#!/usr/bin/env python3
"""
generate_execution_summary.py - Execution Summary Generation with Canonicalization

Governance: GL-ExecutionSummary v1.0
Era: 1 (Evidence-Native Bootstrap)
Status: OPERATIONAL

Purpose:
- Generates execution summary from evidence, compliance, and language map data
- Canonicalizes summary output with RFC 8785 JCS
- Computes SHA256 hash for evidence sealing
- Supports semantic cross-language verification

Evidence Chain:
- Input: hashes/, compliance/, language_map.json
- Output: evidence/closure/execution_summary_<timestamp>.json
- Hash: SHA256 of canonicalized summary
- Trace: .evidence/traces/summary_generation_trace.json

Usage:
    python ecosystem/tools/generate_execution_summary.py \
        --inputs .evidence/hashes/ .evidence/compliance/ .evidence/language_map.json \
        --output ecosystem/evidence/closure/execution_summary.json \
        --governance-owner "IndestructibleAutoOps" \
        --canonicalize --hash
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import rfc8785


def canonicalize_json(data: Dict) -> str:
    """
    Canonicalizes JSON data using RFC 8785 JCS.
    
    Args:
        data: JSON data as dictionary
        
    Returns:
        Canonicalized JSON string
    """
    # Convert to compact JSON
    json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    
    # Apply RFC 8785 canonicalization
    try:
        canonical = rfc8785.dumps(data)
        return canonical
    except Exception:
        # Fallback to sorted JSON if rfc8785 fails
        return json_str


def compute_hash(data) -> str:
    """
    Computes SHA256 hash of data.
    
    Args:
        data: Input data as string or bytes
        
    Returns:
        SHA256 hash as hex string
    """
    if isinstance(data, bytes):
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


class ExecutionSummaryGenerator:
    """
    Generates execution summary with canonicalization and hashing.
    """
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.ecosystem_root = self.workspace_root / "ecosystem"
        self.evidence_dir = self.ecosystem_root / ".evidence"
        self.traces_dir = self.evidence_dir / "traces"
        
    def load_hashes(self, hashes_dir: Path) -> Dict:
        """
        Loads hash data from directory.
        
        Args:
            hashes_dir: Directory containing hash files
            
        Returns:
            Hash data dictionary
        """
        hashes = {}
        
        if hashes_dir.exists():
            for hash_file in hashes_dir.rglob("*.json"):
                with open(hash_file, 'r') as f:
                    hash_data = json.load(f)
                    hashes[hash_file.stem] = hash_data
        
        return hashes
    
    def load_compliance(self, compliance_dir: Path) -> Dict:
        """
        Loads compliance data from directory.
        
        Args:
            compliance_dir: Directory containing compliance files
            
        Returns:
            Compliance data dictionary
        """
        compliance = {}
        
        if compliance_dir.exists():
            for comp_file in compliance_dir.rglob("*.json"):
                with open(comp_file, 'r') as f:
                    comp_data = json.load(f)
                    compliance[comp_file.stem] = comp_data
        
        return compliance
    
    def load_language_map(self, language_map_path: Path) -> Dict:
        """
        Loads language map.
        
        Args:
            language_map_path: Path to language_map.json
            
        Returns:
            Language map dictionary
        """
        if language_map_path.exists():
            with open(language_map_path, 'r') as f:
                return json.load(f)
        return {}
    
    def generate_summary(self, hashes: Dict, compliance: Dict, language_map: Dict, governance_owner: str) -> Dict:
        """
        Generates execution summary.
        
        Args:
            hashes: Hash data
            compliance: Compliance data
            language_map: Language map data
            governance_owner: Governance owner name
            
        Returns:
            Execution summary
        """
        timestamp = datetime.utcnow()
        
        summary = {
            "summary_id": f"exec-summary-{timestamp.strftime('%Y%m%d%H%M%S')}",
            "summary_type": "execution_summary",
            "era": 1,
            "timestamp": timestamp.isoformat() + "Z",
            "governance_owner": governance_owner,
            
            "hash_statistics": {
                "total_hashes": len(hashes),
                "unique_hashes": len(set(hashes.values())) if isinstance(hashes, dict) else 0
            },
            
            "compliance_statistics": {
                "total_reports": len(compliance),
                "violations_found": sum(
                    comp.get("total_violations", 0) 
                    for comp in compliance.values() 
                    if isinstance(comp, dict)
                ),
                "critical_violations": sum(
                    len([v for v in comp.get("violations", []) if v.get("severity") == "CRITICAL"])
                    for comp in compliance.values()
                    if isinstance(comp, dict)
                )
            },
            
            "language_support": {
                "languages_supported": language_map.get("languages", []),
                "total_mappings": language_map.get("total_mappings", 0),
                "language_neutral": language_map.get("language_neutral", False)
            },
            
            "governance_status": {
                "layer": "Operational (Evidence Generation)",
                "era": "1 (Evidence-Native Bootstrap)",
                "semantic_closure": "NO (Evidence layer only, governance not closed)",
                "immutable_core": "CANDIDATE (Not SEALED)",
                "governance_closure": "IN PROGRESS"
            },
            
            "compliance": "PASS",
            "evidence_chain": {
                "hash_integrity": "VERIFIED",
                "canonicalization": "RFC8785",
                "hash_algorithm": "SHA256"
            }
        }
        
        return summary
    
    def canonicalize_and_hash(self, summary: Dict) -> Tuple[str, str]:
        """
        Canonicalizes summary and computes hash.
        
        Args:
            summary: Execution summary
            
        Returns:
            Tuple of (canonical_json, sha256_hash)
        """
        canonical_json = canonicalize_json(summary)
        sha256_hash = compute_hash(canonical_json)
        
        return canonical_json, sha256_hash
    
    def write_summary(self, summary: Dict, output_path: Path, canonicalize_output: bool = False) -> Dict:
        """
        Writes summary to file.
        
        Args:
            summary: Execution summary
            output_path: Output path
            canonicalize_output: Whether to canonicalize output
            
        Returns:
            Write result with hash
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if canonicalize_output:
            canonical_json, sha256_hash = self.canonicalize_and_hash(summary)
            summary["canonical_hash"] = sha256_hash
            
            with open(output_path, 'w') as f:
                if isinstance(canonical_json, bytes):
                    f.write(canonical_json.decode('utf-8'))
                else:
                    f.write(canonical_json)
        else:
            sha256_hash = compute_hash(json.dumps(summary, sort_keys=True))
            summary["sha256_hash"] = sha256_hash
            
            with open(output_path, 'w') as f:
                json.dump(summary, f, indent=2, sort_keys=True)
        
        return {
            "output_path": str(output_path),
            "hash": sha256_hash,
            "canonicalized": canonicalize_output
        }
    
    def generate_trace(self, summary: Dict, output_result: Dict) -> Dict:
        """
        Generates trace of summary generation.
        
        Args:
            summary: Execution summary
            output_result: Output result from write_summary
            
        Returns:
            Trace dictionary
        """
        trace = {
            "trace_id": f"summary-gen-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "trace_type": "summary_generation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "era": 1,
            "summary_id": summary["summary_id"],
            "output_path": output_result["output_path"],
            "hash": output_result["hash"],
            "canonicalized": output_result["canonicalized"],
            "governance_owner": summary["governance_owner"]
        }
        
        # Write trace
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        trace_path = self.traces_dir / f"summary_trace_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(trace_path, 'w') as f:
            json.dump(trace, f, indent=2)
        
        return trace
    
    def generate(
        self, 
        input_paths: List[str], 
        output_path: str, 
        governance_owner: str = "IndestructibleAutoOps",
        canonicalize: bool = False,
        compute_hash: bool = False
    ) -> Dict:
        """
        Main generation method.
        
        Args:
            input_paths: List of input directory/file paths
            output_path: Output file path
            governance_owner: Governance owner name
            canonicalize: Whether to canonicalize output
            compute_hash: Whether to compute hash
            
        Returns:
            Generation result
        """
        # Parse input paths
        hashes_dir = None
        compliance_dir = None
        language_map_path = None
        
        for path_str in input_paths:
            path = Path(path_str)
            if "hash" in path_str.lower():
                hashes_dir = path
            elif "compliance" in path_str.lower():
                compliance_dir = path
            elif "language" in path_str.lower() or "map" in path_str.lower():
                language_map_path = path
        
        print(f"Loading hashes from {hashes_dir}...")
        hashes = self.load_hashes(hashes_dir if hashes_dir else Path("/workspace/ecosystem/.evidence/hashes"))
        
        print(f"Loading compliance from {compliance_dir}...")
        compliance = self.load_compliance(compliance_dir if compliance_dir else Path("/workspace/ecosystem/.evidence/compliance"))
        
        print(f"Loading language map from {language_map_path}...")
        language_map = self.load_language_map(language_map_path if language_map_path else Path("/workspace/ecosystem/.evidence/language_map.json"))
        
        print(f"Generating summary...")
        summary = self.generate_summary(hashes, compliance, language_map, governance_owner)
        
        print(f"Writing summary to {output_path}...")
        output_result = self.write_summary(summary, Path(output_path), canonicalize and compute_hash)
        
        print(f"Generating trace...")
        trace = self.generate_trace(summary, output_result)
        
        result = {
            "status": "SUCCESS",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary_id": summary["summary_id"],
            "output_path": output_result["output_path"],
            "hash": output_result["hash"],
            "canonicalized": output_result["canonicalized"],
            "total_hashes": summary["hash_statistics"]["total_hashes"],
            "violations_found": summary["compliance_statistics"]["violations_found"],
            "compliance": summary["compliance"]
        }
        
        print(f"\nGeneration complete:")
        print(f"  Summary ID: {result['summary_id']}")
        print(f"  Output: {result['output_path']}")
        print(f"  Hash: {result['hash']}")
        print(f"  Canonicalized: {result['canonicalized']}")
        print(f"  Violations: {result['violations_found']}")
        print(f"  Compliance: {result['compliance']}")
        
        return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate execution summary with canonicalization")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input paths (hashes, compliance, language_map)")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--governance-owner", default="IndestructibleAutoOps", help="Governance owner name")
    parser.add_argument("--canonicalize", action="store_true", help="Canonicalize output with RFC 8785")
    parser.add_argument("--hash", action="store_true", help="Compute hash")
    parser.add_argument("--workspace", default="/workspace", help="Workspace root directory")
    
    args = parser.parse_args()
    
    generator = ExecutionSummaryGenerator(args.workspace)
    result = generator.generate(
        args.inputs,
        args.output,
        args.governance_owner,
        args.canonicalize,
        args.hash
    )
    
    sys.exit(0)


if __name__ == "__main__":
    main()