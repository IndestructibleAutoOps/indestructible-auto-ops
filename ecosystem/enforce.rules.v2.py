#!/usr/bin/env python3
"""
IndestructibleAutoOps - Real Governance Engine v2.0.0
GL Level: GL50 (Indestructible Kernel)

此版本修正 v1 的「治理假象」問題：
- 實際執行所有檢查
- 生成完整證據鏈
- 可重播驗證
- 自我治理

Changes from v1:
- Removed fake output that claimed "all checks passed" without verification
- Implemented actual file scanning and content validation
- Added evidence generation and sealing
- Added execution time tracking
- Added trace hash for verification
- Added event stream integration
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class GovernanceCheckResult:
    """治理檢查結果"""

    check_id: str
    rule: str
    description: str
    status: str  # PASS, FAIL, WARN
    evidence: Dict[str, Any]
    execution_time_ms: float
    checked_at: str


@dataclass
class GovernanceReport:
    """治理報告"""

    report_id: str
    started_at: str
    completed_at: str
    total_checks: int
    passed: int
    failed: int
    warnings: int
    checks: List[Dict[str, Any]]  # List of check dicts
    config_used: Dict[str, Any]
    trace_hash: str

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "report_id": self.report_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_checks": self.total_checks,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "checks": self.checks,
            "config_used": self.config_used,
            "trace_hash": self.trace_hash,
        }


class RealGovernanceEngine:
    """真正的治理引擎"""

    def __init__(self, config_path: str = ".governance/glcm-config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.checks: List[GovernanceCheckResult] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def _load_config(self) -> Dict[str, Any]:
        """載入治理配置"""
        if self.config_path.exists():
            try:
                import yaml

                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"⚠️  無法載入配置文件 {self.config_path}: {e}")

        # 預設配置
        return {
            "glcm_rules": [
                "GLCM-NAR",  # 無敘事語言
                "GLCM-FCT",  # 虛假時間線
                "GLCM-UNC",  # 未封存結論
                "GLCM-EVC",  # 證據鏈
            ],
            "evidence_dir": ".governance/evidence",
            "minimum_execution_time_ms": 5000,
            "scan_directories": ["governance", "ecosystem", ".governance"],
        }

    def run_all_checks(self) -> GovernanceReport:
        """執行所有治理檢查"""

        print("\n" + "=" * 70)
        print("🔍 Real Governance Engine v2.0.0 - 開始執行")
        print("=" * 70 + "\n")

        self.start_time = datetime.utcnow()
        print(f"開始時間: {self.start_time.isoformat()}Z\n")

        # 1. GLCM-NAR 檢查
        print("執行 GLCM-NAR: 檢查無敘事語言...")
        self._check_no_narrative_language()

        # 2. GLCM-FCT 檢查
        print("執行 GLCM-FCT: 檢查虛假時間線...")
        self._check_no_false_timeline()

        # 3. GLCM-UNC 檢查
        print("執行 GLCM-UNC: 檢查未封存結論...")
        self._check_no_unsealed_conclusions()

        # 4. GLCM-EVC 檢查
        print("執行 GLCM-EVC: 檢查證據鏈...")
        self._check_evidence_chain()

        # 5. 目錄結構檢查
        print("執行 DIR: 檢查目錄結構...")
        self._check_directory_structure()

        # 6. Hash 完整性檢查
        print("執行 HASH: 檢查 hash 完整性...")
        self._check_hash_integrity()

        # 7. Event stream 檢查
        print("執行 EVENT: 檢查 event stream...")
        self._check_event_stream()

        # 8. 文件完整性檢查
        print("執行 FILE: 檢查文件完整性...")
        self._check_file_integrity()

        self.end_time = datetime.utcnow()

        # 生成報告
        report = self._generate_report()

        # 封存報告
        self._seal_report(report)

        # 輸出摘要
        self._print_summary(report)

        return report

    def _check_no_narrative_language(self):
        """GLCM-NAR: 檢查無敘事語言"""

        start = time.time()

        # 掃描所有 Python 檔案
        violations = []
        narrative_keywords = [
            "應該",
            "可能",
            "大概",
            "也許",
            "或許",
            "可能會",
            "should",
            "maybe",
            "probably",
            "perhaps",
            "might",
            "could",
        ]

        scanned_files = 0
        scan_dirs = self.config.get("scan_directories", ["governance"])

        for scan_dir in scan_dirs:
            dir_path = Path(scan_dir)
            if not dir_path.exists():
                continue

            for py_file in dir_path.rglob("*.py"):
                scanned_files += 1
                try:
                    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                        for keyword in narrative_keywords:
                            if keyword in content:
                                line_num = self._find_line_number(content, keyword)
                                violations.append(
                                    {
                                        "file": str(py_file),
                                        "keyword": keyword,
                                        "line": line_num,
                                    }
                                )
                except Exception as e:
                    # 記錄但繼續
                    pass

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="GLCM-NAR-001",
                rule="GLCM-NAR",
                description="檢查程式碼中是否存在敘事語言",
                status="PASS" if len(violations) == 0 else "FAIL",
                evidence={
                    "files_scanned": scanned_files,
                    "violations_found": len(violations),
                    "violations": violations[:10],  # 只記錄前 10 個
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if len(violations) == 0:
            print(f"  ✅ 通過 - 掃描 {scanned_files} 個文件，未發現敘事語言")
        else:
            print(f"  ❌ 失敗 - 發現 {len(violations)} 個敘述語言")

    def _check_no_false_timeline(self):
        """GLCM-FCT: 檢查虛假時間線"""

        start = time.time()

        # 檢查是否有「已完成」但無證據的陳述
        violations = []
        scanned_files = 0

        # 掃描 Python 檔案中的輸出語句
        for scan_dir in self.config.get("scan_directories", ["ecosystem"]):
            dir_path = Path(scan_dir)
            if not dir_path.exists():
                continue

            for py_file in dir_path.rglob("*.py"):
                scanned_files += 1
                try:
                    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()

                        for i, line in enumerate(lines, 1):
                            if "print(" in line or "logger." in line:
                                # 檢查是否包含完成性語句
                                completion_keywords = [
                                    "完成",
                                    "成功",
                                    "通過",
                                    "100%",
                                    "complete",
                                    "success",
                                    "passed",
                                    "done",
                                    "finished",
                                ]

                                for keyword in completion_keywords:
                                    if keyword in line.lower():
                                        # 檢查是否有對應的證據生成
                                        has_evidence = (
                                            self._check_evidence_generation_nearby(
                                                lines, i
                                            )
                                        )

                                        if not has_evidence:
                                            violations.append(
                                                {
                                                    "file": str(py_file),
                                                    "line": i,
                                                    "statement": line.strip()[
                                                        :100
                                                    ],  # 限制長度
                                                    "keyword": keyword,
                                                }
                                            )
                except Exception as e:
                    pass

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="GLCM-FCT-001",
                rule="GLCM-FCT",
                description="檢查是否有虛假的完成宣告（無證據支持）",
                status="PASS" if len(violations) == 0 else "FAIL",
                evidence={
                    "files_scanned": scanned_files,
                    "violations_found": len(violations),
                    "violations": violations[:10],
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if len(violations) == 0:
            print(f"  ✅ 通過 - 掃描 {scanned_files} 個文件，未發現虛假時間線")
        else:
            print(f"  ❌ 失敗 - 發現 {len(violations)} 個潛在虛假宣告")

    def _check_no_unsealed_conclusions(self):
        """GLCM-UNC: 檢查未封存結論"""

        start = time.time()

        # 檢查所有結論性陳述是否有對應封存
        violations = []
        scanned_files = 0

        # 查找所有 return 語句中的結論
        for scan_dir in self.config.get("scan_directories", ["governance"]):
            dir_path = Path(scan_dir)
            if not dir_path.exists():
                continue

            for py_file in dir_path.rglob("*.py"):
                scanned_files += 1
                try:
                    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        lines = content.split("\n")

                        for i, line in enumerate(lines, 1):
                            if (
                                "return {" in line
                                or "return True" in line
                                or "return False" in line
                            ):
                                # 檢查函式內是否有封存邏輯
                                function_body = self._extract_function_body(lines, i)
                                has_sealing = any(
                                    "seal" in l.lower()
                                    or "hash" in l.lower()
                                    or "evidence" in l.lower()
                                    or "json.dump" in l
                                    or "yaml.dump" in l
                                    for l in function_body
                                )

                                if not has_sealing:
                                    violations.append(
                                        {
                                            "file": str(py_file),
                                            "line": i,
                                            "statement": line.strip()[:100],
                                        }
                                    )
                except Exception as e:
                    pass

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="GLCM-UNC-001",
                rule="GLCM-UNC",
                description="檢查結論是否有封存證據",
                status="WARN" if len(violations) > 0 else "PASS",
                evidence={
                    "files_scanned": scanned_files,
                    "potential_violations": len(violations),
                    "violations": violations[:10],
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if len(violations) == 0:
            print(f"  ✅ 通過 - 掃描 {scanned_files} 個文件，所有結論都有封存")
        else:
            print(f"  ⚠️  警告 - 發現 {len(violations)} 個潛在未封存結論")

    def _check_evidence_chain(self):
        """GLCM-EVC: 檢查證據鏈"""

        start = time.time()

        evidence_dir = Path(self.config.get("evidence_dir", ".governance/evidence"))

        # 檢查必要的證據目錄
        required_subdirs = ["violations", "requirements", "implementation"]
        missing_subdirs = []
        existing_subdirs = []

        for subdir in required_subdirs:
            subdir_path = evidence_dir / subdir
            if subdir_path.exists():
                existing_subdirs.append(subdir)
            else:
                missing_subdirs.append(subdir)

        # 檢查 event stream
        event_stream = Path(".governance/event-stream.jsonl")
        event_stream_exists = event_stream.exists()

        # 統計證據文件
        evidence_files = list(evidence_dir.rglob("*")) if evidence_dir.exists() else []
        evidence_count = sum(1 for f in evidence_files if f.is_file())

        elapsed = (time.time() - start) * 1000

        status = "PASS"
        if not event_stream_exists or evidence_count == 0:
            status = "FAIL"
        elif len(missing_subdirs) > 0:
            status = "WARN"

        self.checks.append(
            GovernanceCheckResult(
                check_id="GLCM-EVC-001",
                rule="GLCM-EVC",
                description="檢查證據鏈目錄結構",
                status=status,
                evidence={
                    "evidence_dir": str(evidence_dir),
                    "required_subdirs": required_subdirs,
                    "existing_subdirs": existing_subdirs,
                    "missing_subdirs": missing_subdirs,
                    "event_stream_exists": event_stream_exists,
                    "evidence_files_count": evidence_count,
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if status == "PASS":
            print(f"  ✅ 通過 - 證據鏈完整，{evidence_count} 個證據文件")
        elif status == "WARN":
            print(f"  ⚠️  警告 - 缺少部分證據目錄: {missing_subdirs}")
        else:
            print(f"  ❌ 失敗 - 證據鏈不完整，缺少 event stream")

    def _check_directory_structure(self):
        """檢查目錄結構"""

        start = time.time()

        required_dirs = [
            "governance/kernel",
            "governance/specs",
            "ecosystem",
            ".governance",
        ]

        existing_dirs = []
        missing_dirs = []

        for dir_path in required_dirs:
            if Path(dir_path).exists():
                existing_dirs.append(dir_path)
            else:
                missing_dirs.append(dir_path)

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="DIR-001",
                rule="DIRECTORY_STRUCTURE",
                description="檢查必要目錄結構",
                status="PASS" if len(missing_dirs) == 0 else "FAIL",
                evidence={
                    "required_dirs": required_dirs,
                    "existing_dirs": existing_dirs,
                    "missing_dirs": missing_dirs,
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if len(missing_dirs) == 0:
            print(f"  ✅ 通過 - 所有必要目錄存在")
        else:
            print(f"  ❌ 失敗 - 缺少目錄: {missing_dirs}")

    def _check_hash_integrity(self):
        """檢查 Hash 完整性"""

        start = time.time()

        hash_boundary = Path(".governance/hash-registry.json")

        if hash_boundary.exists():
            try:
                with open(hash_boundary, "r", encoding="utf-8") as f:
                    boundary = json.load(f)

                # 驗證 hash 格式
                total_hashes = boundary.get("total_hashes", 0)

                # 檢查是否有有效的 hash 條目
                has_valid_hashes = total_hashes > 0

                status = "PASS" if has_valid_hashes else "WARN"
            except Exception as e:
                status = "FAIL"
                boundary = {}
                has_valid_hashes = False
        else:
            status = "FAIL"
            boundary = {}
            has_valid_hashes = False

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="HASH-001",
                rule="HASH_INTEGRITY",
                description="檢查 hash registry 存在且有效",
                status=status,
                evidence={
                    "file_exists": hash_boundary.exists(),
                    "total_hashes": boundary.get("total_hashes", 0),
                    "has_valid_hashes": has_valid_hashes,
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if status == "PASS":
            print(f"  ✅ 通過 - Hash registry 包含 {total_hashes} 個 hashes")
        elif status == "WARN":
            print(f"  ⚠️  警告 - Hash registry 存在但沒有 hashes")
        else:
            print(f"  ❌ 失敗 - Hash registry 不存在或無效")

    def _check_event_stream(self):
        """檢查 Event Stream"""

        start = time.time()

        event_stream = Path(".governance/event-stream.jsonl")

        if event_stream.exists():
            try:
                # 驗證格式
                with open(event_stream, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                valid_events = 0
                invalid_events = 0

                for line in lines:
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                        if "event_id" in event and "timestamp" in event:
                            valid_events += 1
                        else:
                            invalid_events += 1
                    except json.JSONDecodeError:
                        invalid_events += 1

                status = "PASS" if invalid_events == 0 else "WARN"
            except Exception as e:
                status = "FAIL"
                valid_events = 0
                invalid_events = 0
        else:
            status = "FAIL"
            valid_events = 0
            invalid_events = 0

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="EVENT-001",
                rule="EVENT_STREAM",
                description="檢查 event-stream.jsonl 存在且格式正確",
                status=status,
                evidence={
                    "file_exists": event_stream.exists(),
                    "valid_events": valid_events,
                    "invalid_events": invalid_events,
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if status == "PASS":
            print(f"  ✅ 通過 - Event stream 包含 {valid_events} 個有效事件")
        elif status == "WARN":
            print(f"  ⚠️  警告 - Event stream 存在但有 {invalid_events} 個無效事件")
        else:
            print(f"  ❌ 失敗 - Event stream 不存在")

    def _check_file_integrity(self):
        """檢查文件完整性"""

        start = time.time()

        # 檢查關鍵文件是否存在
        key_files = [
            "ecosystem/enforce.py",
            "ecosystem/enforce.rules.py",
            "governance/specs/BACKEND-GOVERNANCE-RESPONSIBILITY.md",
        ]

        existing_files = []
        missing_files = []

        for file_path in key_files:
            if Path(file_path).exists():
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)

        elapsed = (time.time() - start) * 1000

        self.checks.append(
            GovernanceCheckResult(
                check_id="FILE-001",
                rule="FILE_INTEGRITY",
                description="檢查關鍵文件完整性",
                status="PASS" if len(missing_files) == 0 else "WARN",
                evidence={
                    "key_files": key_files,
                    "existing_files": existing_files,
                    "missing_files": missing_files,
                },
                execution_time_ms=elapsed,
                checked_at=datetime.utcnow().isoformat() + "Z",
            )
        )

        if len(missing_files) == 0:
            print(f"  ✅ 通過 - 所有關鍵文件存在")
        else:
            print(f"  ⚠️  警告 - 缺少文件: {missing_files}")

    def _generate_report(self) -> GovernanceReport:
        """生成治理報告"""

        total_checks = len(self.checks)
        passed = sum(1 for c in self.checks if c.status == "PASS")
        failed = sum(1 for c in self.checks if c.status == "FAIL")
        warnings = sum(1 for c in self.checks if c.status == "WARN")

        # 計算 trace hash
        checks_data = [
            {
                "check_id": c.check_id,
                "rule": c.rule,
                "description": c.description,
                "status": c.status,
                "evidence": c.evidence,
            }
            for c in self.checks
        ]
        trace_content = json.dumps(checks_data, sort_keys=True)
        trace_hash = hashlib.sha256(trace_content.encode()).hexdigest()

        return GovernanceReport(
            report_id=f"GLCM-REPORT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            started_at=self.start_time.isoformat() + "Z",
            completed_at=self.end_time.isoformat() + "Z",
            total_checks=total_checks,
            passed=passed,
            failed=failed,
            warnings=warnings,
            checks=checks_data,
            config_used=self.config,
            trace_hash=trace_hash,
        )

    def _seal_report(self, report: GovernanceReport):
        """封存治理報告"""

        # 建立報告目錄
        report_dir = Path(".governance/reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        # 儲存報告
        report_file = report_dir / f"{report.report_id}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        # 記錄到 event stream
        self._append_event_stream(report, str(report_file))

    def _append_event_stream(self, report: GovernanceReport, report_file: str):
        """附加到 event stream"""

        event_stream = Path(".governance/event-stream.jsonl")
        event_stream.parent.mkdir(parents=True, exist_ok=True)

        # 獲取下一個 event ID
        next_event_id = self._get_next_event_id()

        event = {
            "event_id": next_event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "governance_check_completed",
            "namespace": "/governance/kernel/",
            "layer": "kernel",
            "platform": "all",
            "era": "Era-1",
            "payload": {
                "report_id": report.report_id,
                "total_checks": report.total_checks,
                "passed": report.passed,
                "failed": report.failed,
                "warnings": report.warnings,
                "trace_hash": report.trace_hash,
                "report_file": report_file,
                "engine_version": "2.0.0",
            },
        }

        with open(event_stream, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _print_summary(self, report: GovernanceReport):
        """輸出摘要"""

        print(f"\n{'='*70}")
        print(f"治理檢查報告 - {report.report_id}")
        print(f"{'='*70}")
        print(f"開始時間: {report.started_at}")
        print(f"結束時間: {report.completed_at}")
        print(f"總檢查數: {report.total_checks}")
        print(f"通過: {report.passed} ✅")
        print(f"失敗: {report.failed} ❌")
        print(f"警告: {report.warnings} ⚠️")
        print(f"Trace Hash: {report.trace_hash}")
        print(f"{'='*70}\n")

        # 顯示失敗的檢查
        if report.failed > 0:
            print("失敗的檢查:")
            for check in report.checks:
                if check["status"] == "FAIL":
                    print(f"  ❌ {check['check_id']}: {check['description']}")
                    print(f"     證據: {check['evidence']}")

        # 顯示警告
        if report.warnings > 0:
            print("\n警告:")
            for check in report.checks:
                if check["status"] == "WARN":
                    print(f"  ⚠️  {check['check_id']}: {check['description']}")

    def _find_line_number(self, content: str, keyword: str) -> int:
        """找到關鍵字所在行號"""
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if keyword in line:
                return i
        return -1

    def _check_evidence_generation_nearby(
        self, lines: List[str], target_line: int, window: int = 10
    ) -> bool:
        """檢查目標行附近是否有證據生成"""
        start = max(0, target_line - window - 1)
        end = min(len(lines), target_line + window)

        nearby_code = "\n".join(lines[start:end])

        evidence_keywords = [
            "json.dump",
            "yaml.dump",
            "with open",
            ".json",
            ".yaml",
            "evidence",
            "seal",
            "hash",
            "write(",
            "append(",
            "event_stream",
        ]

        return any(kw in nearby_code for kw in evidence_keywords)

    def _extract_function_body(self, lines: List[str], return_line: int) -> List[str]:
        """提取函式主體"""
        # 簡化版：向上找到 def，向下到 return
        start = return_line - 1
        while start > 0 and not lines[start].strip().startswith("def "):
            start -= 1

        return lines[start:return_line]

    def _get_next_event_id(self) -> int:
        """取得下一個 event ID"""
        event_stream = Path(".governance/event-stream.jsonl")

        if not event_stream.exists():
            return 1

        try:
            with open(event_stream, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                return 1

            last_event = json.loads(lines[-1])
            return last_event.get("event_id", 0) + 1
        except:
            return 1


def main():
    """主程式"""
    engine = RealGovernanceEngine()
    report = engine.run_all_checks()

    # 根據結果決定退出碼
    if report.failed > 0:
        print(f"\n❌ 治理檢查失敗: {report.failed} 個檢查未通過")
        exit(1)
    elif report.warnings > 0:
        print(f"\n⚠️  治理檢查完成但有 {report.warnings} 個警告")
        exit(2)
    else:
        print(f"\n✅ 治理檢查全部通過")
        exit(0)


if __name__ == "__main__":
    main()
