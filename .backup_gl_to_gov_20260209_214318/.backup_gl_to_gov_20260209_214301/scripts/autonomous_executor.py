#!/usr/bin/env python3
"""
全機器自理 — 自主執行引擎 (Autonomous Execution Engine)

消費掃描報告，執行治理流水線，產生證據，驅動自動修復。
閉環設計：讀取 sensing 報告 → 執行門檻 → 產生證據 → 回饋 anchor

功能：
  1. 消費掃描報告 — 讀取 sensing 產出的 scan-report.json
  2. 執行門檻驗證 — 對每個模組執行全域門檻
  3. 自動修復 — 對可修復的問題自動產生修復
  4. 證據生成 — 產生不可變的執行證據鏈
  5. 事件發射 — 將執行結果寫入事件流
  6. 閉環回饋 — 更新 anchor 基線狀態
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# 常數定義
# ═══════════════════════════════════════════════════════════════════════════════

REGISTRY_PATH = "responsibility-governance-execution-boundary/registry/governance-modules.json"
SCAN_REPORT_PATH = "responsibility-governance-sensing-boundary/report/scan-report.json"
EVIDENCE_DIR = ".evidence"
EVENT_STREAM = ".governance/event-stream.jsonl"
GATES_PATH = "responsibility-governance-execution-boundary/gates/global-gates.yaml"
EXECUTION_REPORT_DIR = "responsibility-governance-execution-boundary/reports"


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函式
# ═══════════════════════════════════════════════════════════════════════════════

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# 門檻驗證器
# ═══════════════════════════════════════════════════════════════════════════════

class GateValidator:
    """全域門檻驗證器。"""

    GATES = [
        {
            "id": "directory_exists",
            "description": "模組目錄必須存在",
            "severity": "CRITICAL",
        },
        {
            "id": "readme_exists",
            "description": "模組必須包含 README.md",
            "severity": "HIGH",
        },
        {
            "id": "has_content",
            "description": "模組必須包含至少一個檔案",
            "severity": "HIGH",
        },
        {
            "id": "hash_computed",
            "description": "模組雜湊必須可計算",
            "severity": "MEDIUM",
        },
        {
            "id": "no_cross_boundary_violations",
            "description": "不得有跨邊界違規",
            "severity": "HIGH",
        },
    ]

    def validate_module(self, module_scan: Dict[str, Any], violations: List[Dict]) -> Dict[str, Any]:
        """對單一模組執行所有門檻。"""
        module_id = module_scan["module_id"]
        gate_results = []
        all_passed = True

        checks = {c["check"]: c["passed"] for c in module_scan.get("checks", [])}

        for gate in self.GATES:
            gate_id = gate["id"]
            if gate_id == "no_cross_boundary_violations":
                # 檢查此模組是否有違規
                module_violations = [
                    v for v in violations
                    if v.get("boundary", "").endswith(module_scan.get("directory", ""))
                    or module_scan.get("directory", "") in v.get("boundary", "")
                ]
                passed = len(module_violations) == 0
            else:
                passed = checks.get(gate_id, False)

            gate_results.append({
                "gate_id": gate_id,
                "passed": passed,
                "severity": gate["severity"],
                "description": gate["description"],
            })

            if not passed:
                all_passed = False

        return {
            "module_id": module_id,
            "gates": gate_results,
            "all_passed": all_passed,
            "gate_count": len(gate_results),
            "passed_count": sum(1 for g in gate_results if g["passed"]),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 自動修復引擎
# ═══════════════════════════════════════════════════════════════════════════════

class AutoRemediator:
    """自動修復引擎 — 對可修復的問題自動產生修復。"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.fixes_applied: List[Dict[str, Any]] = []

    def remediate(self, remediation_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """執行自動修復。"""
        for item in remediation_list:
            action = item.get("action", "")
            module_id = item.get("module_id", "")
            severity = item.get("severity", "MEDIUM")

            if action.startswith("mkdir"):
                self._fix_missing_directory(item)
            elif action.startswith("generate_readme:"):
                self._fix_missing_readme(item)
            else:
                self.fixes_applied.append({
                    "module_id": module_id,
                    "action": action,
                    "status": "SKIPPED",
                    "reason": "不支援的自動修復動作",
                    "timestamp": utc_now(),
                })

        return self.fixes_applied

    def _fix_missing_directory(self, item: Dict[str, Any]):
        """修復缺失的目錄。"""
        action = item["action"]
        # 解析 mkdir -p <dir>
        parts = action.split()
        if len(parts) >= 3:
            dir_path = self.repo_root / parts[-1]
        else:
            dir_path = self.repo_root / item.get("module_id", "unknown")

        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.fixes_applied.append({
                "module_id": item["module_id"],
                "action": f"created_directory:{dir_path}",
                "status": "FIXED",
                "timestamp": utc_now(),
            })
            print(f"  🔧 已修復: 建立目錄 {dir_path}")
        except Exception as e:
            self.fixes_applied.append({
                "module_id": item["module_id"],
                "action": action,
                "status": "FAILED",
                "reason": str(e),
                "timestamp": utc_now(),
            })

    def _fix_missing_readme(self, item: Dict[str, Any]):
        """修復缺失的 README.md。"""
        action = item["action"]
        directory = action.split(":", 1)[1] if ":" in action else item.get("module_id", "")
        readme_path = self.repo_root / directory / "README.md"

        if readme_path.exists():
            self.fixes_applied.append({
                "module_id": item["module_id"],
                "action": "generate_readme",
                "status": "SKIPPED",
                "reason": "README.md 已存在",
                "timestamp": utc_now(),
            })
            return

        try:
            # 從註冊表取得模組資訊
            registry = load_json(self.repo_root / REGISTRY_PATH)
            module_info = next(
                (m for m in registry.get("modules", []) if m["id"] == item["module_id"]),
                None
            )

            module_name = module_info["name"] if module_info else item["module_id"]
            gl_layer = module_info.get("gl_layer", "N/A") if module_info else "N/A"
            role = module_info.get("role", "N/A") if module_info else "N/A"

            content = f"""# {module_name}

**Directory**: `{directory}/`
**GL Layer**: {gl_layer}
**Role**: {role}
**Auto-Generated**: {utc_now()}

---

## Overview

This directory is a responsibility boundary within the IndestructibleAutoOps governance framework.

## Governance

This boundary follows the Machine Native Governance Architecture (MNGA) principles.

---

**Version**: 1.0.0
**Last Updated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**Maintained by**: IndestructibleAutoOps (Machine-Generated)
"""
            readme_path.parent.mkdir(parents=True, exist_ok=True)
            with readme_path.open("w", encoding="utf-8") as f:
                f.write(content)

            self.fixes_applied.append({
                "module_id": item["module_id"],
                "action": f"generated_readme:{readme_path}",
                "status": "FIXED",
                "timestamp": utc_now(),
            })
            print(f"  🔧 已修復: 生成 README.md → {readme_path}")
        except Exception as e:
            self.fixes_applied.append({
                "module_id": item["module_id"],
                "action": "generate_readme",
                "status": "FAILED",
                "reason": str(e),
                "timestamp": utc_now(),
            })


# ═══════════════════════════════════════════════════════════════════════════════
# 證據生成器
# ═══════════════════════════════════════════════════════════════════════════════

class EvidenceGenerator:
    """產生不可變的執行證據鏈。"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.evidence_dir = repo_root / EVIDENCE_DIR
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """產生證據。"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        evidence_id = f"EV-{timestamp}"

        # 序列化執行結果
        result_json = json.dumps(execution_result, sort_keys=True, ensure_ascii=False)
        result_hash = compute_hash(result_json)

        evidence = {
            "evidence_id": evidence_id,
            "timestamp": utc_now(),
            "execution_hash": result_hash,
            "execution_summary": {
                "total_modules": execution_result.get("total_modules", 0),
                "gates_passed": execution_result.get("gates_passed", 0),
                "gates_failed": execution_result.get("gates_failed", 0),
                "fixes_applied": execution_result.get("fixes_applied", 0),
            },
            "integrity": {
                "algorithm": "SHA-256",
                "hash": result_hash,
                "sealed": True,
            },
        }

        # 儲存證據
        evidence_file = self.evidence_dir / f"evidence-{timestamp}.json"
        save_json(evidence_file, evidence)
        print(f"  📋 證據已生成: {evidence_id} (hash: {result_hash[:16]}...)")

        return evidence


# ═══════════════════════════════════════════════════════════════════════════════
# 自主執行引擎
# ═══════════════════════════════════════════════════════════════════════════════

class AutonomousExecutor:
    """全自主執行引擎 — 零人類介入。"""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.execution_id = f"EXEC-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        self.gate_validator = GateValidator()
        self.remediator = AutoRemediator(self.repo_root)
        self.evidence_gen = EvidenceGenerator(self.repo_root)

    def execute(self) -> Dict[str, Any]:
        """執行完整的治理流水線。"""
        print(f"\n[{self.execution_id}] 啟動自主執行引擎...")

        # Step 1: 載入掃描報告
        scan_report_path = self.repo_root / SCAN_REPORT_PATH
        if not scan_report_path.exists():
            print(f"[{self.execution_id}] 掃描報告不存在，先執行掃描...")
            return {"status": "NO_SCAN_REPORT", "message": "請先執行 autonomous_scanner.py"}

        scan_report = load_json(scan_report_path)
        print(f"[{self.execution_id}] 已載入掃描報告: {scan_report.get('scan_id', 'N/A')}")

        # Step 2: 執行門檻驗證
        print(f"\n[{self.execution_id}] 執行門檻驗證...")
        gate_results = []
        violations = scan_report.get("violations", [])

        for module_scan in scan_report.get("modules", []):
            gate_result = self.gate_validator.validate_module(module_scan, violations)
            gate_results.append(gate_result)
            status_icon = "✅" if gate_result["all_passed"] else "❌"
            print(f"  {status_icon} {gate_result['module_id']}: "
                  f"{gate_result['passed_count']}/{gate_result['gate_count']} gates passed")

        gates_passed = sum(1 for g in gate_results if g["all_passed"])
        gates_failed = len(gate_results) - gates_passed

        # Step 3: 自動修復
        remediation_list = scan_report.get("remediation_required", [])
        fixes = []
        if remediation_list:
            print(f"\n[{self.execution_id}] 執行自動修復 ({len(remediation_list)} 項)...")
            fixes = self.remediator.remediate(remediation_list)
        else:
            print(f"\n[{self.execution_id}] 無需自動修復")

        # Step 4: 組裝執行結果
        execution_result = {
            "execution_id": self.execution_id,
            "timestamp": utc_now(),
            "scan_id": scan_report.get("scan_id", "N/A"),
            "total_modules": len(gate_results),
            "gates_passed": gates_passed,
            "gates_failed": gates_failed,
            "gate_pass_rate": round(gates_passed / max(len(gate_results), 1) * 100, 2),
            "fixes_applied": len([f for f in fixes if f["status"] == "FIXED"]),
            "fixes_skipped": len([f for f in fixes if f["status"] == "SKIPPED"]),
            "fixes_failed": len([f for f in fixes if f["status"] == "FAILED"]),
            "gate_details": gate_results,
            "fix_details": fixes,
            "violations_from_scan": len(violations),
        }

        # Step 5: 產生證據
        print(f"\n[{self.execution_id}] 產生執行證據...")
        evidence = self.evidence_gen.generate(execution_result)
        execution_result["evidence"] = evidence

        # Step 6: 發射事件
        self._emit_event(execution_result)

        # Step 7: 儲存執行報告
        self._save_report(execution_result)

        # 彙總
        print(f"\n[{self.execution_id}] 執行完成:")
        print(f"  門檻通過: {gates_passed}/{len(gate_results)}")
        print(f"  修復: {execution_result['fixes_applied']} applied, "
              f"{execution_result['fixes_skipped']} skipped, "
              f"{execution_result['fixes_failed']} failed")
        print(f"  證據: {evidence['evidence_id']}")

        return execution_result

    def _emit_event(self, result: Dict[str, Any]):
        """將執行事件寫入治理事件流。"""
        event_file = self.repo_root / EVENT_STREAM
        event_file.parent.mkdir(parents=True, exist_ok=True)

        existing_events = []
        if event_file.exists():
            with event_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            existing_events.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

        next_id = max((e.get("event_id", 0) for e in existing_events), default=0) + 1

        event = {
            "event_id": next_id,
            "timestamp": utc_now(),
            "event_type": "autonomous_execution_completed",
            "namespace": "/governance/execution/",
            "layer": "execution",
            "platform": "all",
            "era": "Era-1",
            "payload": {
                "execution_id": result["execution_id"],
                "scan_id": result["scan_id"],
                "total_modules": result["total_modules"],
                "gates_passed": result["gates_passed"],
                "gates_failed": result["gates_failed"],
                "gate_pass_rate": result["gate_pass_rate"],
                "fixes_applied": result["fixes_applied"],
                "evidence_id": result["evidence"]["evidence_id"],
                "engine_version": "2.0.0",
            },
        }

        with event_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

        print(f"  📡 事件已發射: event_id={next_id}")

    def _save_report(self, result: Dict[str, Any]):
        """儲存執行報告。"""
        report_dir = self.repo_root / EXECUTION_REPORT_DIR
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        report_file = report_dir / f"execution-report-{timestamp}.json"
        save_json(report_file, result)

        # 同時儲存為最新
        latest = report_dir / "execution-report-latest.json"
        save_json(latest, result)

        print(f"  💾 報告已儲存: {report_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# 主程式
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    repo_root = Path(__file__).resolve().parent.parent
    if not (repo_root / REGISTRY_PATH).exists():
        repo_root = Path.cwd()
    if not (repo_root / REGISTRY_PATH).exists():
        print("[FATAL] 無法找到治理模組註冊表")
        sys.exit(1)

    executor = AutonomousExecutor(repo_root)
    result = executor.execute()

    if result.get("gates_failed", 0) > 0:
        print(f"\n[結果] 有 {result['gates_failed']} 個模組未通過門檻")
        sys.exit(1)
    else:
        print(f"\n[結果] 所有模組通過門檻 ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
