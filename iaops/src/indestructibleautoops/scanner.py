from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class NarrativeSecretScanner:
    """Scanner for detecting narrative patterns and questions in file paths.
    
    Note: This scanner currently only checks file PATHS, not file contents.
    This is by design to provide fast, lightweight governance checks during
    the indexing phase. Content-based scanning could be added in future versions.
    """
    narrative_patterns: list[str]
    forbid_question_patterns: list[str]

    def scan_index(self, index: dict[str, Any]) -> dict[str, Any]:
        """Scan file paths in the index for narrative patterns and questions.
        
        Args:
            index: Index dictionary containing list of files with their paths.
            
        Returns:
            Dictionary with:
                - blocked: True if any patterns matched
                - reason: "narrative_detected" or "question_detected"
                - narrativeHits: List of path/pattern matches for narratives
                - questionHits: List of path/pattern matches for questions
        """
        files = index.get("files", [])
        narrative_hits: list[dict[str, Any]] = []
        question_hits: list[dict[str, Any]] = []
        for f in files:
            path = f.get("path", "")
            for pat in self.narrative_patterns:
                if re.search(pat, path):
                    narrative_hits.append({"path": path, "pattern": pat})
            for pat in self.forbid_question_patterns:
                if re.search(pat, path):
                    question_hits.append({"path": path, "pattern": pat})

        blocked = bool(narrative_hits or question_hits)
        reason = (
            "narrative_detected" if narrative_hits else "question_detected" if question_hits else ""
        )
        return {
            "blocked": blocked,
            "reason": reason,
            "narrativeHits": narrative_hits,
            "questionHits": question_hits,
        }
