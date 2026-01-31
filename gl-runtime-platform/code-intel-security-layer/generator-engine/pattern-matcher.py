# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

# @GL-governed
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GL Code Intelligence & Security Layer - Pattern Matcher
Version 21.0.0

This module matches code patterns against known security, performance, and architecture patterns.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class PatternMatch:
    """Represents a pattern match"""
    pattern_name: str
    severity: str
    line_number: int
    code_snippet: str
    description: str
    mitigation: List[str]

class PatternMatcher:
    """Matches code against known patterns"""
    
    def __init__(self):
        self.patterns = {}
        self._load_security_patterns()
        self._load_performance_patterns()
        self._load_architecture_patterns()
    
    def _load_security_patterns(self):
        """Load security patterns"""
        self.patterns["sql-injection"] = {
            "name": "SQL Injection",
            "severity": "high",
            "patterns": [
                r".*\b(SELECT|INSERT|UPDATE|DELETE)\b.*\+.*['&quot;].*['&quot;]",
                r".*\`.*\$\{.*\}.*\`.*"
            ],
            "description": "Potential SQL injection vulnerability",
            "mitigation": [
                "Use parameterized queries",
                "Use ORM frameworks",
                "Validate and sanitize inputs"
            ]
        }
        
        self.patterns["xss"] = {
            "name": "Cross-Site Scripting",
            "severity": "high",
            "patterns": [
                r".*innerHTML\s*=.*\+.*",
                r".*outerHTML\s*=.*\+.*",
                r".*document\.write\s*\(.*\+.*"
            ],
            "description": "Potential XSS vulnerability",
            "mitigation": [
                "Use output encoding",
                "Implement Content Security Policy",
                "Use textContent instead of innerHTML"
            ]
        }
    
    def _load_performance_patterns(self):
        """Load performance patterns"""
        self.patterns["n-plus-one-query"] = {
            "name": "N+1 Query Problem",
            "severity": "medium",
            "patterns": [
                r".*for\s*\(.*\).*\{[\s\S]*?query\s*\(.*\).*\}"
            ],
            "description": "Potential N+1 query problem",
            "mitigation": [
                "Use eager loading",
                "Implement query batching",
                "Use caching"
            ]
        }
    
    def _load_architecture_patterns(self):
        """Load architecture patterns"""
        self.patterns["large-class"] = {
            "name": "Large Class",
            "severity": "medium",
            "patterns": [
                r"class\s+\w+\s*{[\s\S]{500,}}"
            ],
            "description": "Class with too many responsibilities",
            "mitigation": [
                "Apply Single Responsibility Principle",
                "Extract smaller classes",
                "Use composition over inheritance"
            ]
        }
    
    def match_code(self, code: str) -> List[PatternMatch]:
        """Match code against all patterns"""
        matches = []
        lines = code.split('\n')
        
        for pattern_name, pattern_info in self.patterns.items():
            for pattern_regex in pattern_info["patterns"]:
                try:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern_regex, line, re.IGNORECASE):
                            match = PatternMatch(
                                pattern_name=pattern_name,
                                severity=pattern_info["severity"],
                                line_number=line_num,
                                code_snippet=line.strip(),
                                description=pattern_info["description"],
                                mitigation=pattern_info["mitigation"]
                            )
                            matches.append(match)
                except re.error:
                    continue
        
        return matches
    
    def get_pattern_info(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific pattern"""
        return self.patterns.get(pattern_name)


if __name__ == "__main__":
    # Example usage
    matcher = PatternMatcher()
    
    code = """
    const query = "SELECT * FROM users WHERE id = '" + userId + "'";
    const result = db.execute(query);
    """
    
    matches = matcher.match_code(code)
    for match in matches:
        print(f"Found {match.pattern_name} at line {match.line_number}")