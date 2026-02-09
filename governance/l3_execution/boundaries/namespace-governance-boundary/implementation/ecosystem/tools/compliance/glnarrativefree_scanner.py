#!/usr/bin/env python3
"""
GL-NarrativeFree Compliance Scanner v2.0

A comprehensive narrative-free compliance system for IndestructibleAutoOps,
ensuring zero narrative language, sealed conclusions, and evidence-backed claims.

Version 2.0 Features:
- GLCM-FCT: Fabricated Completion Timeline Detection (CRITICAL)
- GLCM-NAR: Narrative Phrases Detection
- GLCM-UNC: Unsealed Conclusions Detection
- GLCM-EVC: Evidence Chain Verification
- Multi-language support (zh, en, ja, ko, de, fr)
- Adaptive mode (GLCM-Auto)

Author: IndestructibleAutoOps
Version: 2.0
Date: 2024-02-05
"""

import os
import re
import sys
import json
import yaml
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class Severity(Enum):
    """Violation severity levels"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ViolationType(Enum):
    """Violation types"""

    NARRATIVE = "narrative"
    UNSEALED_CLAIM = "unsealed_claim"
    FABRICATED_TIMELINE = "fabricated_timeline"
    EVIDENCE_MISSING = "evidence_missing"
    LANGUAGE_NEUTRALITY = "language_neutrality"


@dataclass
class Violation:
    """Violation data structure"""

    type: str
    text: str
    pos: int
    rule: str
    severity: str
    evidence_found: bool = False
    language: Optional[str] = None


class GLNarrativeFreeScanner:
    """
    Governance Language Compliance Scanner (GLCM)

    Scans all outputs, reports, and logs to ensure:
    - Zero narrative language
    - All conclusions sealed with evidence
    - No fabricated timelines
    - Language-neutral hashing
    """

    # Narrative phrases (GLCM-NAR)
    NARRATIVE_PATTERNS = [
        r"我們相信",
        r"應該",
        r"可能",
        r"預期",
        r"希望",
        r"也許",
        r"有望",
        r"我們認為",
        r"我們預估",
        r"我們樂觀地",
        r"令人擔憂",
        r"值得期待",
        r"預料之中",
        r"看起來",
        r"似乎",
        r"大概",
        r"或許",
        r"估計",
        r"we believe",
        r"should",
        r"could",
        r"might",
        r"would",
        r"expect",
        r"hope",
        r"maybe",
        r"likely",
        r"probably",
        r"optimistic",
        r"concerning",
        r"promising",
        r"anticipated",
        r"appears",
        r"seems",
        r"roughly",
        r"perhaps",
    ]

    # Unsealed conclusions (GLCM-UNC)
    UNSEALED_CLAIMS = [
        r"因此我們決定",
        r"我們已完成",
        r"我們已修復",
        r"我們採取了行動",
        r"我們已部署",
        r"問題已解決",
        r"系統已恢復",
        r"我們已執行",
        r"我們已實施",
        r"therefore we decided",
        r"we have completed",
        r"we have fixed",
        r"we have taken action",
        r"we have deployed",
        r"the issue was resolved",
        r"the system has been restored",
        r"we have executed",
        r"we have implemented",
    ]

    # Fabricated timeline patterns (GLCM-FCT) - CRITICAL
    FABRICATED_TIMELINE_PATTERNS = {
        "zh": [
            r"已完成",
            r"已修復",
            r"已部署",
            r"已恢復",
            r"已解決",
            r"已執行",
            r"已實施",
            r"已修正",
            r"已完成修復",
            r"問題已解決",
            r"系統已恢復",
        ],
        "en": [
            r"has been completed",
            r"has been resolved",
            r"was fixed",
            r"has been deployed",
            r"we have completed",
            r"the issue was addressed",
            r"was successfully repaired",
            r"has been restored",
            r"has been executed",
            r"has been implemented",
        ],
        "ja": [
            r"修正しました",
            r"完了しました",
            r"復旧しました",
            r"解決しました",
            r"実行しました",
            r"展開しました",
            r"実施しました",
            r"修正が完了しました",
        ],
        "ko": [
            r"수정했습니다",
            r"완료했습니다",
            r"복구했습니다",
            r"해결했습니다",
            r"실행했습니다",
            r"배포했습니다",
            r"실시했습니다",
            r"수정이 완료되었습니다",
        ],
        "de": [
            r"haben wir abgeschlossen",
            r"wurde behoben",
            r"wurde bereitgestellt",
            r"wurde wiederhergestellt",
            r"wurde gelöst",
            r"wurde ausgeführt",
            r"wurde implementiert",
        ],
        "fr": [
            r"a été résolu",
            r"a été corrigé",
            r"a été déployé",
            r"a été restauré",
            r"a été achevé",
            r"a été exécuté",
            r"a été mis en œuvre",
        ],
    }

    # Evidence hints (required within 300 characters)
    EVIDENCE_HINTS = [
        r"hash",
        r"trace",
        r"\.evidence",
        r"補件",
        r"封存",
        r"gl-events",
        r"replay",
        r"canonical",
        r"era-1-closure",
        r"hash_translation_table",
        r"hash_of_",
        r"trace_id",
        r"evidence_file",
        r"artifact_hash",
    ]

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the scanner.

        Args:
            config_path: Path to adaptive config file
        """
        self.violations: Dict[str, List[Violation]] = {}
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load adaptive configuration"""
        default_config = {
            "enabled": True,
            "modules": {
                "GLCM-NAR": True,
                "GLCM-UNC": True,
                "GLCM-EVC": True,
                "GLCM-FCT": True,
                "GLCM-EMO": False,
                "GLCM-SOFT": False,
                "GLCM-EXC": {"enabled": False, "whitelist": []},
            },
        }

        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)

        return default_config

    def detect_language(self, text: str) -> str:
        """
        Detect text language.
        Simple heuristic based on character sets.
        """
        if re.search(r"[\u4e00-\u9fff]", text):
            return "zh"
        elif re.search(r"[\u3040-\u309f\u30a0-\u30ff]", text):
            return "ja"
        elif re.search(r"[\uac00-\ud7af]", text):
            return "ko"
        elif re.search(r"[äöüß]", text):
            return "de"
        elif re.search(r"[éèêëàâôîïûùç]", text):
            return "fr"
        else:
            return "en"

    def check_evidence_nearby(
        self, text: str, position: int, window: int = 300
    ) -> bool:
        """
        Check if evidence hints exist within window characters.
        """
        window_text = text[position : position + window]
        return any(
            re.search(hint, window_text, re.IGNORECASE) for hint in self.EVIDENCE_HINTS
        )

    def scan_narrative_phrases(self, text: str, lang: str) -> List[Violation]:
        """
        Scan for narrative phrases (GLCM-NAR).
        """
        if not self.config["modules"].get("GLCM-NAR", True):
            return []

        violations = []
        for pattern in self.NARRATIVE_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                violations.append(
                    Violation(
                        type=ViolationType.NARRATIVE.value,
                        text=match.group(),
                        pos=match.start(),
                        rule="GLCM-NAR",
                        severity=Severity.MEDIUM.value,
                        language=lang,
                    )
                )

        return violations

    def scan_unsealed_conclusions(self, text: str, lang: str) -> List[Violation]:
        """
        Scan for unsealed conclusions (GLCM-UNC).
        """
        if not self.config["modules"].get("GLCM-UNC", True):
            return []

        violations = []
        for pattern in self.UNSEALED_CLAIMS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                evidence_found = self.check_evidence_nearby(text, match.start())

                # If GLCM-SOFT is enabled, narrative is allowed with evidence
                if self.config["modules"].get("GLCM-SOFT", False) and evidence_found:
                    continue

                violations.append(
                    Violation(
                        type=ViolationType.UNSEALED_CLAIM.value,
                        text=match.group(),
                        pos=match.start(),
                        rule="GLCM-UNC",
                        severity=(
                            Severity.HIGH.value
                            if not evidence_found
                            else Severity.LOW.value
                        ),
                        evidence_found=evidence_found,
                        language=lang,
                    )
                )

        return violations

    def scan_fabricated_timelines(self, text: str, lang: str) -> List[Violation]:
        """
        Scan for fabricated completion timelines (GLCM-FCT).

        CRITICAL: This is the MOST CRITICAL vulnerability detection.
        """
        if not self.config["modules"].get("GLCM-FCT", True):
            return []

        violations = []
        patterns = self.FABRICATED_TIMELINE_PATTERNS.get(lang, [])

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                evidence_found = self.check_evidence_nearby(text, match.start())

                # Fabricated timeline without evidence is CRITICAL
                violations.append(
                    Violation(
                        type=ViolationType.FABRICATED_TIMELINE.value,
                        text=match.group(),
                        pos=match.start(),
                        rule="GLCM-FCT",
                        severity=(
                            Severity.CRITICAL.value
                            if not evidence_found
                            else Severity.HIGH.value
                        ),
                        evidence_found=evidence_found,
                        language=lang,
                    )
                )

        return violations

    def scan_text(self, text: str, lang: Optional[str] = None) -> List[Violation]:
        """
        Scan text for all violations.

        Args:
            text: Text to scan
            lang: Language code (auto-detected if None)

        Returns:
            List of violations
        """
        if lang is None:
            lang = self.detect_language(text)

        violations = []

        # Scan for different violation types
        violations.extend(self.scan_narrative_phrases(text, lang))
        violations.extend(self.scan_unsealed_conclusions(text, lang))
        violations.extend(self.scan_fabricated_timelines(text, lang))

        # Remove duplicates and overlapping matches
        # Prioritize CRITICAL > HIGH > MEDIUM > LOW
        # Sort by severity (descending), then by length (descending)
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        violations.sort(
            key=lambda v: (severity_order.get(v.severity, 99), -len(v.text))
        )

        seen = set()
        unique_violations = []
        for v in violations:
            # Check if this violation overlaps with any seen violation
            overlaps = False
            for pos in range(v.pos, v.pos + len(v.text)):
                if pos in seen:
                    overlaps = True
                    break

            if not overlaps:
                # Mark all positions as seen
                for pos in range(v.pos, v.pos + len(v.text)):
                    seen.add(pos)
                unique_violations.append(v)

        # Sort by position
        unique_violations.sort(key=lambda v: v.pos)

        return unique_violations

    def scan_file(self, file_path: str) -> List[Violation]:
        """
        Scan a single file.

        Args:
            file_path: Path to file

        Returns:
            List of violations
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check whitelist
            if self.config["modules"].get("GLCM-EXC", {}).get("enabled", False):
                whitelist = self.config["modules"]["GLCM-EXC"].get("whitelist", [])
                for pattern in whitelist:
                    if re.search(pattern, file_path):
                        return []

            return self.scan_text(content)

        except Exception as e:
            return [
                Violation(
                    type="error",
                    text=str(e),
                    pos=0,
                    rule="FILE_READ_ERROR",
                    severity=Severity.MEDIUM.value,
                )
            ]

    def scan_directory(self, target_dir: str) -> Dict[str, List[Violation]]:
        """
        Scan directory recursively.

        Args:
            target_dir: Target directory path

        Returns:
            Dictionary mapping file paths to violations
        """
        violations = {}

        for root, _, files in os.walk(target_dir):
            for file in files:
                # Only scan text files
                if file.endswith((".json", ".log", ".txt", ".md", ".yaml", ".yml")):
                    full_path = os.path.join(root, file)
                    findings = self.scan_file(full_path)
                    if findings:
                        violations[full_path] = findings

        return violations

    def generate_report(self, violations: Dict[str, List[Violation]]) -> Dict:
        """
        Generate compliance report.

        Args:
            violations: Violations dictionary

        Returns:
            Report dictionary
        """
        narrative_count = sum(
            1 for vlist in violations.values() for v in vlist if v.type == "narrative"
        )
        unsealed_count = sum(
            1
            for vlist in violations.values()
            for v in vlist
            if v.type == "unsealed_claim"
        )
        fabricated_count = sum(
            1
            for vlist in violations.values()
            for v in vlist
            if v.type == "fabricated_timeline"
        )

        # Count unsealed claims without evidence
        unsealed_without_evidence = sum(
            1
            for vlist in violations.values()
            for v in vlist
            if v.type == "unsealed_claim" and not v.evidence_found
        )

        # Count fabricated timelines without evidence (CRITICAL)
        fabricated_without_evidence = sum(
            1
            for vlist in violations.values()
            for v in vlist
            if v.type == "fabricated_timeline" and not v.evidence_found
        )

        report = {
            "scan_timestamp": datetime.utcnow().isoformat() + "Z",
            "glcm_config": self.config,
            "files": {
                path: [asdict(v) for v in vlist] for path, vlist in violations.items()
            },
            "summary": {
                "total_violations": sum(len(vlist) for vlist in violations.values()),
                "narrative_violations": narrative_count,
                "unsealed_conclusions": unsealed_count,
                "unsealed_without_evidence": unsealed_without_evidence,
                "fabricated_timelines": fabricated_count,
                "fabricated_without_evidence": fabricated_without_evidence,
                "files_scanned": self.files_scanned,
                "files_with_violations": len(violations),
            },
            "compliance_status": self._determine_compliance_status(
                narrative_count, unsealed_without_evidence, fabricated_without_evidence
            ),
        }

        return report

    def _determine_compliance_status(
        self, narrative: int, unsealed: int, fabricated: int
    ) -> Dict:
        """
        Determine overall compliance status.
        """
        if fabricated > 0:
            return {
                "status": "NON_COMPLIANT",
                "reason": f"CRITICAL: {fabricated} fabricated timeline(s) without evidence",
                "blocker": True,
            }
        elif unsealed > 0:
            return {
                "status": "WARNING",
                "reason": f"{unsealed} unsealed conclusion(s) without evidence",
                "blocker": False,
            }
        elif narrative > 0:
            return {
                "status": "WARNING",
                "reason": f"{narrative} narrative phrase(s) found",
                "blocker": False,
            }
        else:
            return {
                "status": "COMPLIANT",
                "reason": "Zero violations - narrative-free compliance achieved",
                "blocker": False,
            }


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="GL-NarrativeFree Compliance Scanner v2.0"
    )
    parser.add_argument("target", help="Target file or directory to scan")
    parser.add_argument("--config", "-c", help="Path to adaptive config file")
    parser.add_argument(
        "--output",
        "-o",
        default="narrative_free_compliance_report.json",
        help="Output report file path",
    )
    parser.add_argument(
        "--context",
        choices=["governance_report", "human_dialogue", "documentation"],
        help="Context for adaptive mode",
    )

    args = parser.parse_args()

    # Create scanner
    scanner = GLNarrativeFreeScanner(config_path=args.config)

    # Scan
    if os.path.isfile(args.target):
        violations = {args.target: scanner.scan_file(args.target)}
    else:
        violations = scanner.scan_directory(args.target)

    # Generate report
    report = scanner.generate_report(violations)

    # Write report
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"✅ Narrative-Free Compliance Scan Complete", file=sys.stderr)
    print(f"   Status: {report['compliance_status']['status']}", file=sys.stderr)
    print(
        f"   Total Violations: {report['summary']['total_violations']}", file=sys.stderr
    )
    print(f"   Report: {args.output}", file=sys.stderr)

    # Exit with error if BLOCKER
    if report["compliance_status"]["blocker"]:
        print(f"\n❌ BLOCKER: {report['compliance_status']['reason']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
