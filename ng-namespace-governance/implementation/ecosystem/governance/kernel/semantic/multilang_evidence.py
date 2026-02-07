#!/usr/bin/env python3
"""
Multi-Language Evidence Sealing - Cross-Language Evidence Management

Seals semantic evidence across multiple languages, enabling cross-language
audit and verification.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from .tokenizer import SemanticTokenizer
from .ast_builder import SemanticAST


@dataclass
class MultiLanguageEvidence:
    """Multi-language evidence"""

    semantic_hash: str
    canonical_ast: Dict
    expressions: Dict[str, str]  # {"zh": "...", "en": "...", ...}
    sealed_at: str
    evidence_id: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class MultiLanguageEvidenceSealer:
    """Multi-language evidence sealer"""

    def __init__(self, evidence_dir: str = ".governance/semantic-evidence"):
        self.evidence_dir = evidence_dir
        self.tokenizer = SemanticTokenizer()
        self.ast_builder = SemanticAST()

        # Ensure evidence directory exists
        os.makedirs(evidence_dir, exist_ok=True)

    def seal_multilang(
        self,
        semantic_hash: str,
        expressions: Dict[str, str],
        canonical_ast: Optional[Dict] = None,
    ) -> str:
        """
        Seal multi-language expressions

        Args:
            semantic_hash: Semantic hash
            expressions: {"zh": "創建用戶", "en": "create user", ...}
            canonical_ast: Optional canonical AST (will build from first expression if not provided)

        Returns:
            Evidence file path
        """
        # Build AST if not provided
        if canonical_ast is None:
            first_lang = list(expressions.keys())[0]
            tokens = self.tokenizer.tokenize(
                expressions[first_lang], language=first_lang
            )
            self.ast_builder.build(tokens)
            canonical_ast = json.loads(self.ast_builder.to_canonical_json())

        # Generate evidence ID
        import uuid

        evidence_id = str(uuid.uuid4())

        # Create evidence
        evidence = MultiLanguageEvidence(
            semantic_hash=semantic_hash,
            canonical_ast=canonical_ast,
            expressions=expressions,
            sealed_at=datetime.utcnow().isoformat() + "Z",
            evidence_id=evidence_id,
        )

        # Store evidence
        file_path = os.path.join(
            self.evidence_dir, f"{semantic_hash.replace(':', '_')}.json"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(evidence.to_json())

        # Log to event stream
        self._log_to_event_stream(evidence)

        return file_path

    def seal_from_texts(
        self, texts: Dict[str, str]  # {"zh": "...", "en": "..."}
    ) -> Dict[str, str]:
        """
        Seal multi-language texts

        Args:
            texts: Dictionary of language → text

        Returns:
            {"semantic_hash": "...", "evidence_file": "..."}
        """
        # Build semantic hash from first text
        first_lang = list(texts.keys())[0]
        tokens = self.tokenizer.tokenize(texts[first_lang], language=first_lang)
        self.ast_builder.build(tokens)
        semantic_hash = self.ast_builder.hash()

        # Seal
        evidence_file = self.seal_multilang(semantic_hash, texts)

        return {"semantic_hash": semantic_hash, "evidence_file": evidence_file}

    def verify_multilang(
        self, semantic_hash: str, expression: str, language: str
    ) -> bool:
        """
        Verify if expression matches sealed semantic hash

        Args:
            semantic_hash: Semantic hash to verify
            expression: Expression to verify
            language: Language of expression

        Returns:
            True if expression matches semantic hash
        """
        # Tokenize expression
        tokens = self.tokenizer.tokenize(expression, language=language)
        self.ast_builder.build(tokens)
        current_hash = self.ast_builder.hash()

        # Compare hashes
        return current_hash == semantic_hash

    def load_evidence(self, semantic_hash: str) -> Optional[MultiLanguageEvidence]:
        """
        Load evidence by semantic hash

        Args:
            semantic_hash: Semantic hash

        Returns:
            MultiLanguageEvidence or None if not found
        """
        file_path = os.path.join(
            self.evidence_dir, f"{semantic_hash.replace(':', '_')}.json"
        )

        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return MultiLanguageEvidence(**data)

    def _log_to_event_stream(self, evidence: MultiLanguageEvidence):
        """Log evidence sealing to event stream"""
        event = {
            "event_type": "semantic_evidence_sealed",
            "evidence_id": evidence.evidence_id,
            "semantic_hash": evidence.semantic_hash,
            "languages": list(evidence.expressions.keys()),
            "sealed_at": evidence.sealed_at,
        }

        event_stream_path = ".governance/event-stream.jsonl"
        with open(event_stream_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
