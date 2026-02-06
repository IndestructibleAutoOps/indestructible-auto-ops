"""
Test 1: Semantic Corruption Tests
Purpose: Ensure semantic declarations are not corrupted by narrative, wrapping, or fuzzy language
"""

import pytest
from typing import List, Dict, Any


class TestSemanticCorruption:
    """Test suite for semantic corruption detection"""
    
    # Fuzzy language patterns to detect
    FUZZY_PATTERNS = [
        r"大致[完成完成]",
        r"應該[沒問題可以]",
        r"差不多[好了完成]",
        r"基本上[完成可以]",
        r"大概[沒問題完成]",
    ]
    
    # Narrative wrapper patterns to detect
    NARRATIVE_PATTERNS = [
        r"我們.*認為",
        r"從.*角度來看",
        r"在.*背景下",
        r"基於.*考慮",
    ]
    
    def test_tc_1_1_fuzzy_language_detection(self, sample_report, violation_maker):
        """
        TC-1.1: Fuzzy Language Detection
        
        Input: Report containing "大致完成" (roughly complete)
        Expected: System detects semantic shift
        Action: Generate complement, block sealing
        Severity: HIGH
        """
        report = {
            **sample_report,
            "summary": "大致完成，應該沒問題"
        }
        
        # Detect fuzzy language
        detected_fuzzy = self._detect_fuzzy_language(report["summary"])
        
        assert detected_fuzzy, "Should detect fuzzy language '大致完成'"
        
        # Generate violation
        violation = violation_maker(
            test_case="TC-1.1",
            severity="HIGH",
            detected_issue="fuzzy_language_detected",
            evidence={
                "fuzzy_phrases": ["大致完成", "應該沒問題"],
                "location": "report.summary",
                "original_text": report["summary"]
            },
            remediation={
                "action": "replace_with_factual_language",
                "required": "明確聲明狀態 (COMPLETED/IN_PROGRESS/FAILED)",
                "suggestion": "COMPLETED"
            }
        )
        
        assert violation.severity == "HIGH"
        assert violation.detected_issue == "fuzzy_language_detected"
        assert "大致完成" in violation.evidence["fuzzy_phrases"]
    
    def test_tc_1_2_narrative_wrapper_detection(self, sample_report, violation_maker):
        """
        TC-1.2: Narrative Wrapper Detection
        
        Input: Tool output with narrative wrapping
        Expected: System rejects narrative language
        Action: Generate complement, require factual output
        Severity: HIGH
        """
        report = {
            **sample_report,
            "summary": "從治理角度來看，我們認為這個任務基本完成了"
        }
        
        # Detect narrative wrapper
        detected_narrative = self._detect_narrative_wrapper(report["summary"])
        
        assert detected_narrative, "Should detect narrative wrapper"
        
        # Generate violation
        violation = violation_maker(
            test_case="TC-1.2",
            severity="HIGH",
            detected_issue="narrative_wrapper_detected",
            evidence={
                "narrative_phrases": ["從治理角度來看", "我們認為"],
                "location": "report.summary",
                "original_text": report["summary"]
            },
            remediation={
                "action": "remove_narrative_wrapper",
                "required": "直接陳述事實，不使用敘事性語言",
                "suggestion": "任務狀態: COMPLETED"
            }
        )
        
        assert violation.severity == "HIGH"
        assert violation.detected_issue == "narrative_wrapper_detected"
    
    def test_tc_1_3_semantic_declaration_mismatch(self, sample_report, violation_maker):
        """
        TC-1.3: Semantic Declaration Mismatch
        
        Input: "status": "COMPLETED" but evidence incomplete
        Expected: System detects mismatch
        Action: Generate complement, block sealing
        Severity: CRITICAL
        """
        report = {
            **sample_report,
            "status": "COMPLETED",
            "evidence": [],  # Empty evidence despite COMPLETED status
            "complements": []
        }
        
        # Detect semantic mismatch
        mismatch = self._detect_semantic_mismatch(report)
        
        assert mismatch, "Should detect semantic mismatch: COMPLETED with no evidence"
        
        # Generate violation
        violation = violation_maker(
            test_case="TC-1.3",
            severity="CRITICAL",
            detected_issue="declaration_mismatch",
            evidence={
                "declared_status": "COMPLETED",
                "actual_state": "NO_EVIDENCE",
                "evidence_count": 0,
                "complement_count": 0
            },
            remediation={
                "action": "align_status_with_evidence",
                "required": "狀態必須與證據一致",
                "suggestion": "提供完整證據或將狀態改為 IN_PROGRESS"
            }
        )
        
        assert violation.severity == "CRITICAL"
        assert violation.detected_issue == "declaration_mismatch"
    
    def test_fuzzy_language_not_detected_in_factual_report(self, sample_report):
        """Test that factual language is not flagged as fuzzy"""
        report = {
            **sample_report,
            "summary": "任務已完成，所有測試通過"
        }
        
        detected_fuzzy = self._detect_fuzzy_language(report["summary"])
        
        assert not detected_fuzzy, "Should not flag factual language as fuzzy"
    
    def test_narrative_not_detected_in_factual_report(self, sample_report):
        """Test that factual report is not flagged as narrative"""
        report = {
            **sample_report,
            "summary": "任務狀態: COMPLETED，證據: 3 個文件"
        }
        
        detected_narrative = self._detect_narrative_wrapper(report["summary"])
        
        assert not detected_narrative, "Should not flag factual report as narrative"
    
    def test_semantic_consistency_when_evidence_present(self, sample_report):
        """Test that COMPLETED status with evidence is not flagged"""
        report = {
            **sample_report,
            "status": "COMPLETED",
            "evidence": ["evidence-1.json", "evidence-2.json"],
            "complements": ["complement-1.md"]
        }
        
        mismatch = self._detect_semantic_mismatch(report)
        
        assert not mismatch, "Should not flag COMPLETED with evidence as mismatch"
    
    # Helper methods
    
    def _detect_fuzzy_language(self, text: str) -> bool:
        """Detect fuzzy language patterns"""
        import re
        
        for pattern in self.FUZZY_PATTERNS:
            if re.search(pattern, text):
                return True
        
        # Check for common fuzzy phrases
        fuzzy_phrases = ["大致", "應該", "差不多", "基本上", "大概"]
        for phrase in fuzzy_phrases:
            if phrase in text:
                return True
        
        return False
    
    def _detect_narrative_wrapper(self, text: str) -> bool:
        """Detect narrative wrapper patterns"""
        import re
        
        for pattern in self.NARRATIVE_PATTERNS:
            if re.search(pattern, text):
                return True
        
        # Check for narrative indicators
        narrative_indicators = ["我們認為", "從...角度來看", "基於...考慮"]
        for indicator in narrative_indicators:
            if indicator in text or indicator.split("...")[0] in text:
                return True
        
        return False
    
    def _detect_semantic_mismatch(self, report: Dict[str, Any]) -> bool:
        """Detect semantic declaration mismatch"""
        status = report.get("status", "")
        evidence = report.get("evidence", [])
        complements = report.get("complements", [])
        
        # CRITICAL status checks
        if status == "COMPLETED" and len(evidence) == 0:
            return True
        
        if status == "INTEGRATED" and len(evidence) == 0:
            return True
        
        if status == "PASSED" and len(evidence) == 0:
            return True
        
        # Check for missing complements
        if status == "COMPLETED" and len(complements) == 0:
            return True
        
        return False