#!/usr/bin/env python3
"""
process_event_stream.py - Event Stream Processing for Semantic Analysis

Governance: GL-EventStreamProcessing v1.0
Era: 1 (Evidence-Native Bootstrap)
Status: OPERATIONAL

Purpose:
- Processes governance event stream for semantic tokenization
- Generates canonicalized hashes with RFC 8785
- Creates language maps for cross-language verification
- Outputs to semantic-tokens/ directory

Usage:
    python ecosystem/tools/process_event_stream.py \
        --input ecosystem/.governance/event-stream.jsonl \
        --output ecosystem/.evidence/semantic-tokens/ \
        --language-map ecosystem/.evidence/language_map.json
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import rfc8785


def canonicalize_json(data: Dict) -> str:
    """Canonicalize JSON using RFC 8785."""
    return rfc8785.dumps(data)


def compute_hash(data) -> str:
    """Compute SHA256 hash."""
    if isinstance(data, bytes):
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def extract_semantic_tokens(event: Dict) -> Dict:
    """Extract semantic tokens from event."""
    tokens = {
        "event_type": event.get("event_type"),
        "phase": event.get("phase"),
        "success": event.get("success"),
        "era": event.get("era"),
        "canonicalization_method": event.get("canonicalization_method"),
    }
    return {k: v for k, v in tokens.items() if v is not None}


def process_event_stream(input_path: Path, output_dir: Path) -> Dict:
    """Process event stream and generate outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)

    semantic_tokens = []
    hashes = {}
    language_map = {"zh": {}, "en": {}, "ja": {}, "ko": {}, "de": {}, "fr": {}}

    # Read event stream
    with open(input_path, "r") as f:
        for line in f:
            if line.strip():
                event = json.loads(line)

                # Extract semantic tokens
                tokens = extract_semantic_tokens(event)
                semantic_tokens.append(tokens)

                # Store hash
                event_id = event.get("event_id")
                canonical_hash = event.get("canonical_hash")
                if event_id and canonical_hash:
                    hashes[event_id] = canonical_hash

                # Add to language map
                for lang in language_map.keys():
                    language_map[lang][event_id] = {
                        "canonical_hash": canonical_hash,
                        "event_type": event.get("event_type"),
                        "phase": event.get("phase"),
                    }

    # Write semantic tokens
    tokens_path = output_dir / "semantic_tokens.json"
    with open(tokens_path, "w") as f:
        json.dump(semantic_tokens, f, indent=2)
    tokens_hash = compute_hash(canonicalize_json(semantic_tokens))

    # Write hashes
    hashes_path = output_dir / "event_hashes.json"
    with open(hashes_path, "w") as f:
        json.dump(hashes, f, indent=2)
    hashes_hash = compute_hash(canonicalize_json(hashes))

    result = {
        "status": "SUCCESS",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input_path": str(input_path),
        "output_dir": str(output_dir),
        "tokens_path": str(tokens_path),
        "tokens_hash": tokens_hash,
        "hashes_path": str(hashes_path),
        "hashes_hash": hashes_hash,
        "total_events": len(semantic_tokens),
        "total_hashes": len(hashes),
    }

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process governance event stream")
    parser.add_argument("--input", required=True, help="Input event stream file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--language-map", help="Output language map file")

    args = parser.parse_args()

    result = process_event_stream(Path(args.input), Path(args.output))

    # Write language map if requested
    if args.language_map:
        language_map = {
            "version": "1.0.0",
            "era": 1,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "languages": ["zh", "en", "ja", "ko", "de", "fr"],
            "total_mappings": result["total_hashes"],
            "language_neutral": True,
            "canonicalization_method": "RFC8785",
        }

        with open(args.language_map, "w") as f:
            json.dump(language_map, f, indent=2)

        result["language_map_path"] = args.language_map

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
