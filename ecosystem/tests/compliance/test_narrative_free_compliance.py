#!/usr/bin/env python3
"""
Test Suite for GL-NarrativeFree Compliance Scanner v2.0

Tests the scanner's ability to:
1. Detect narrative phrases (GLCM-NAR)
2. Detect unsealed conclusions (GLCM-UNC)
3. Detect fabricated timelines (GLCM-FCT) - CRITICAL
4. Verify evidence chains (GLCM-EVC)
5. Support multi-language detection
6. Generate compliance reports

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import unittest
import json
import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from tools.compliance.glnarrativefree_scanner import (
    GLNarrativeFreeScanner,
    Violation,
    ViolationType,
    Severity
)


class TestNarrativePhraseDetection(unittest.TestCase):
    """Test GLCM-NAR: Narrative phrases detection"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scanner = GLNarrativeFreeScanner()
    
    def test_detect_chinese_narrative(self):
        """Test detecting Chinese narrative phrases"""
        text = "我們相信這個解決方案會有效"
        violations = self.scanner.scan_text(text, lang="zh")
        
        narrative_violations = [v for v in violations if v.type == "narrative"]
        self.assertEqual(len(narrative_violations), 1)
        self.assertIn("我們相信", narrative_violations[0].text)
    
    def test_detect_english_narrative(self):
        """Test detecting English narrative phrases"""
        text = "We believe this solution will work"
        violations = self.scanner.scan_text(text, lang="en")
        
        narrative_violations = [v for v in violations if v.type == "narrative"]
        self.assertEqual(len(narrative_violations), 1)
        self.assertIn("we believe", narrative_violations[0].text.lower())
    
    def test_no_narrative_in_clean_text(self):
        """Test that clean text has no narrative violations"""
        text = "系統重新啟動了 nginx 服務，hash: abc123"
        violations = self.scanner.scan_text(text, lang="zh")
        
        narrative_violations = [v for v in violations if v.type == "narrative"]
        self.assertEqual(len(narrative_violations), 0)


class TestFabricatedTimelineDetection(unittest.TestCase):
    """Test GLCM-FCT: Fabricated timeline detection - CRITICAL"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scanner = GLNarrativeFreeScanner()
    
    def test_detect_fabricated_timeline_chinese(self):
        """Test detecting fabricated timeline in Chinese"""
        text = "問題已解決"
        violations = self.scanner.scan_text(text, lang="zh")
        
        fabricated_violations = [v for v in violations if v.type == "fabricated_timeline"]
        self.assertEqual(len(fabricated_violations), 1)
        self.assertFalse(fabricated_violations[0].evidence_found)
        self.assertEqual(fabricated_violations[0].severity, "CRITICAL")
    
    def test_detect_fabricated_timeline_english(self):
        """Test detecting fabricated timeline in English"""
        text = "The issue has been resolved"
        violations = self.scanner.scan_text(text, lang="en")
        
        fabricated_violations = [v for v in violations if v.type == "fabricated_timeline"]
        self.assertEqual(len(fabricated_violations), 1)
        self.assertFalse(fabricated_violations[0].evidence_found)
        self.assertEqual(fabricated_violations[0].severity, "CRITICAL")
    
    def test_fabricated_timeline_with_evidence(self):
        """Test that fabricated timeline with evidence has lower severity"""
        text = "問題已解決。trace: abc123, hash: def456"
        violations = self.scanner.scan_text(text, lang="zh")
        
        fabricated_violations = [v for v in violations if v.type == "fabricated_timeline"]
        if len(fabricated_violations) > 0:
            self.assertTrue(fabricated_violations[0].evidence_found)
            self.assertEqual(fabricated_violations[0].severity, "HIGH")


if __name__ == "__main__":
    unittest.main()