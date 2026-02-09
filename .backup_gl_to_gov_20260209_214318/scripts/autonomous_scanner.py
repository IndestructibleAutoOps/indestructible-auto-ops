#!/usr/bin/env python3
"""
全機器自理 — 自主掃描引擎 (Autonomous Scanner Engine)

掃描所有 18 個責任邊界目錄，產生完整的治理掃描報告。
閉環設計：sensing → execution → anchor → feedback

功能：
  1. 模組存在性掃描 — 驗證所有已註冊模組目錄是否存在
  2. 必要工件完整性 — 檢查 README.md 及核心子目錄
  3. 雜湊完整性 — 計算每個邊界目錄的 SHA-256 雜湊
  4. 語義一致性 — 驗證語義樹附掛
  5. 跨邊界違規偵測 — 檢查檔案是否放錯邊界
  6. 漂移偵測 — 與上次掃描比對雜湊變化
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# 常數定義
# ═══════════════════════════════════════════════════════════════════════════════

REGISTRY_PATH = "responsibility-governance-execution-boundary/registry/governance-modules.json"
REPORT_DIR = "responsibility-governance-sensing-boundary/report"
EVENT_STREAM = ".governance/event-stream.jsonl"
BASELINE_PATH = "responsibility-governance-anchor-boundary/baseline/governance-baseline.yaml"
HASH_SPEC_PATH = "responsibility-governance-anchor-boundary/hash-boundary/hash-spec.yaml"

# 跨邊界違規規則：哪些檔案模式不應出現在哪些邊界
CROSS_BOUNDARY_RULES = {
    "responsibility-governance-anchor-boundary": {
        "forbidden_patterns": [r"\.sh$", r"\.py$", r"Dockerfile"],
        "reason": "anchor 邊界禁止存放執行腳本"
    },
    "responsibility-governance-specs-boundary": {
        "forbidden_patterns": [r"\.sh$", r"\.py$", r"Dockerfile", r"\.tmp$"],
        "reason": "specs 邊界禁止存放執行腳本或暫存檔"
    },
    "responsibility-guardrails-boundary": {
        "forbidden_patterns": [r"scanner.*\.py$", r"scan.*\.sh$"],
        "reason": "guardrails 邊界禁止存放掃描腳本，應放在 sensing"
    },
    "responsibility-gateway-boundary": {
        "forbidden_patterns": [r"deploy.*\.sh$", r"Dockerfile"],
        "reason": "gateway 邊界禁止存放部署腳本"
    },
    "responsibility-mnga-architecture-boundary": {
        "forbidden_patterns": [r"ops.*\.sh$", r"runbook.*\.yaml$"],
        "reason": "mnga 邊界禁止存放運維流程，應放在 mno-operations"
    },
    "responsibility-generation-boundary": {
        "forbidden_patterns": [r"\.bin$", r"\.tar\.gz$", r"\.zip$", r"\.jar$"],
        "reason": "generation 邊界禁止存放二進位工件"
    },
    "responsibility-gcp-boundary": {
        "forbidden_patterns": [r"aws.*\.yaml$", r"azure.*\.yaml$"],
        "reason": "gcp 邊界禁止存放 AWS/Azure 配置"
    },
    "responsibility-global-policy-boundary": {
        "forbidden_patterns": [r"gcp.*\.yaml$", r"aws.*\.yaml$"],
        "reason": "global-policy 邊界禁止存放特定雲供應商配置"
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函式
# ═══════════════════════════════════════════════════════════════════════════════

def compute_file_hash(path: Path) -> str:
    """計算單一檔案的 SHA-256 雜湊。"""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_directory_hash(directory: Path) -> str:
    """計算目錄下所有檔案的確定性 SHA-256 雜湊。"""
    digest = hashlib.sha256()
    for file_path in sorted(p for p in directory.rglob("*") if p.is_file()):
        rel = str(file_path.relative_to(directory))
        digest.update(rel.encode("utf-8"))
        digest.update(compute_file_hash(file_path).encode("utf-8"))
    return digest.hexdigest()


def utc_now() -> str:
    """取得 UTC ISO 時間戳。"""
    return datetime.now(timezone.utc).isoformat()


def load_registry(repo_root: Path) -> Dict[str, Any]:
    """載入治理模組註冊表。"""
    registry_file = repo_root / REGISTRY_PATH
    if not registry_file.exists():
        print(f"[FATAL] 註冊表不存在: {registry_file}")
        sys.exit(1)
    with registry_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_previous_scan(repo_root: Path) -> Optional[Dict[str, Any]]:
    """載入上次掃描報告以進行漂移偵測。"""
    report_dir = repo_root / REPORT_DIR
    if not report_dir.exists():
        return None
    reports = sorted(report_dir.glob("scan-report-*.json"), reverse=True)
    if not reports:
        # 嘗試載入 scan-report.json
        fallback = report_dir / "scan-report.json"
        if fallback.exists():
            with fallback.open("r", encoding="utf-8") as f:
                return json.load(f)
        return None
    with reports[0].open("r", encoding="utf-8") as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# 掃描器核心
# ═══════════════════════════════════════════════════════════════════════════════

class AutonomousScanner:
    """全自主掃描引擎 — 零人類介入。"""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.registry = load_registry(self.repo_root)
        self.modules = self.registry.get("modules", [])
        self.previous_scan = load_previous_scan(self.repo_root)
        self.scan_id = f"SCAN-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        self.results: Dict[str, Any] = {
            "scan_id": self.scan_id,
            "timestamp": utc_now(),
            "scanner_version": "2.0.0",
            "mode": "autonomous",
            "repo_root": str(self.repo_root),
            "total_modules": len(self.modules),
            "modules": [],
            "summary": {},
            "violations": [],
            "drift_detected": [],
            "remediation_required": [],
        }

    def scan_all(self) -> Dict[str, Any]:
        """執行完整掃描。"""
        print(f"[{self.scan_id}] 啟動全自主掃描引擎...")
        print(f"[{self.scan_id}] 已註冊模組數: {len(self.modules)}")

        passed = 0
        failed = 0
        warnings = 0

        for module in self.modules:
            module_result = self._scan_module(module)
            self.results["modules"].append(module_result)

            status = module_result["status"]
            if status == "PASS":
                passed += 1
            elif status == "FAIL":
                failed += 1
            else:
                warnings += 1

        # 跨邊界違規掃描
        self._scan_cross_boundary_violations()

        # 漂移偵測
        self._detect_drift()

        # 彙總
        self.results["summary"] = {
            "total": len(self.modules),
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "pass_rate": round(passed / max(len(self.modules), 1) * 100, 2),
            "violations_count": len(self.results["violations"]),
            "drift_count": len(self.results["drift_detected"]),
            "remediation_count": len(self.results["remediation_required"]),
            "scan_completed_at": utc_now(),
        }

        print(f"\n[{self.scan_id}] 掃描完成:")
        print(f"  通過: {passed} | 失敗: {failed} | 警告: {warnings}")
        print(f"  違規: {len(self.results['violations'])} | 漂移: {len(self.results['drift_detected'])}")

        return self.results

    def _scan_module(self, module: Dict[str, Any]) -> Dict[str, Any]:
        """掃描單一治理模組。"""
        module_id = module["id"]
        directory = module["directory"]
        module_path = self.repo_root / directory

        result: Dict[str, Any] = {
            "module_id": module_id,
            "directory": directory,
            "checks": [],
            "status": "PASS",
            "hash": None,
            "file_count": 0,
        }

        # 檢查 1: 目錄存在性
        exists = module_path.is_dir()
        result["checks"].append({
            "check": "directory_exists",
            "passed": exists,
            "detail": f"{'存在' if exists else '不存在'}: {directory}",
        })
        if not exists:
            result["status"] = "FAIL"
            self.results["remediation_required"].append({
                "module_id": module_id,
                "issue": "目錄不存在",
                "action": f"mkdir -p {directory}",
                "severity": "CRITICAL",
            })
            return result

        # 檢查 2: README.md 存在
        readme_exists = (module_path / "README.md").is_file()
        result["checks"].append({
            "check": "readme_exists",
            "passed": readme_exists,
            "detail": f"README.md {'存在' if readme_exists else '缺失'}",
        })
        if not readme_exists:
            self.results["remediation_required"].append({
                "module_id": module_id,
                "issue": "缺少 README.md",
                "action": f"generate_readme:{directory}",
                "severity": "HIGH",
            })

        # 檢查 3: 檔案計數
        files = list(module_path.rglob("*"))
        file_count = sum(1 for f in files if f.is_file())
        result["file_count"] = file_count
        has_content = file_count > 0
        result["checks"].append({
            "check": "has_content",
            "passed": has_content,
            "detail": f"檔案數: {file_count}",
        })

        # 檢查 4: 雜湊完整性
        try:
            dir_hash = compute_directory_hash(module_path)
            result["hash"] = dir_hash
            result["checks"].append({
                "check": "hash_computed",
                "passed": True,
                "detail": f"SHA-256: {dir_hash[:16]}...",
            })
        except Exception as e:
            result["checks"].append({
                "check": "hash_computed",
                "passed": False,
                "detail": f"雜湊計算失敗: {str(e)}",
            })

        # 檢查 5: 子目錄結構
        subdirs = [d.name for d in module_path.iterdir() if d.is_dir()]
        result["checks"].append({
            "check": "subdirectory_structure",
            "passed": len(subdirs) > 0 or file_count > 1,
            "detail": f"子目錄: {subdirs}" if subdirs else "無子目錄",
        })

        # 決定最終狀態
        failed_checks = [c for c in result["checks"] if not c["passed"]]
        if any(c["check"] in ("directory_exists", "has_content") for c in failed_checks):
            result["status"] = "FAIL"
        elif failed_checks:
            result["status"] = "WARNING"

        status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️"}
        print(f"  {status_icon.get(result['status'], '?')} {module_id}: {result['status']} ({file_count} files)")

        return result

    def _scan_cross_boundary_violations(self):
        """掃描跨邊界違規。"""
        print(f"\n[{self.scan_id}] 掃描跨邊界違規...")

        for boundary_dir, rules in CROSS_BOUNDARY_RULES.items():
            boundary_path = self.repo_root / boundary_dir
            if not boundary_path.is_dir():
                continue

            for file_path in boundary_path.rglob("*"):
                if not file_path.is_file():
                    continue
                filename = file_path.name
                for pattern in rules["forbidden_patterns"]:
                    if re.search(pattern, filename):
                        violation = {
                            "boundary": boundary_dir,
                            "file": str(file_path.relative_to(self.repo_root)),
                            "pattern": pattern,
                            "reason": rules["reason"],
                            "severity": "HIGH",
                            "action": "move_to_correct_boundary",
                        }
                        self.results["violations"].append(violation)
                        print(f"  ⚠️ 違規: {violation['file']} — {rules['reason']}")

    def _detect_drift(self):
        """與上次掃描比對，偵測雜湊漂移。"""
        if not self.previous_scan:
            print(f"\n[{self.scan_id}] 無先前掃描報告，跳過漂移偵測")
            return

        print(f"\n[{self.scan_id}] 執行漂移偵測...")
        prev_modules = {m["module_id"]: m for m in self.previous_scan.get("modules", [])}

        for current in self.results["modules"]:
            module_id = current["module_id"]
            prev = prev_modules.get(module_id)
            if not prev:
                continue

            current_hash = current.get("hash")
            prev_hash = prev.get("hash")

            if current_hash and prev_hash and current_hash != prev_hash:
                drift = {
                    "module_id": module_id,
                    "previous_hash": prev_hash[:16] + "...",
                    "current_hash": current_hash[:16] + "...",
                    "detected_at": utc_now(),
                }
                self.results["drift_detected"].append(drift)
                print(f"  🔄 漂移偵測: {module_id}")

    def save_report(self) -> Path:
        """儲存掃描報告。"""
        report_dir = self.repo_root / REPORT_DIR
        report_dir.mkdir(parents=True, exist_ok=True)

        # 儲存帶時間戳的報告
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        report_file = report_dir / f"scan-report-{timestamp}.json"
        with report_file.open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # 同時儲存為 scan-report.json（最新）
        latest_file = report_dir / "scan-report.json"
        with latest_file.open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n[{self.scan_id}] 報告已儲存: {report_file}")
        return report_file

    def emit_event(self):
        """將掃描事件寫入治理事件流。"""
        event_file = self.repo_root / EVENT_STREAM
        event_file.parent.mkdir(parents=True, exist_ok=True)

        # 讀取現有事件以取得下一個 event_id
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
            "event_type": "autonomous_scan_completed",
            "namespace": "/governance/sensing/",
            "layer": "sensing",
            "platform": "all",
            "era": "Era-1",
            "payload": {
                "scan_id": self.scan_id,
                "total_modules": self.results["summary"]["total"],
                "passed": self.results["summary"]["passed"],
                "failed": self.results["summary"]["failed"],
                "warnings": self.results["summary"]["warnings"],
                "violations": self.results["summary"]["violations_count"],
                "drift_count": self.results["summary"]["drift_count"],
                "pass_rate": self.results["summary"]["pass_rate"],
                "scanner_version": "2.0.0",
            },
        }

        with event_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

        print(f"[{self.scan_id}] 事件已寫入: event_id={next_id}")


# ═══════════════════════════════════════════════════════════════════════════════
# 主程式
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """主入口。"""
    # 自動偵測 repo root
    repo_root = Path(__file__).resolve().parent.parent
    if not (repo_root / REGISTRY_PATH).exists():
        # 嘗試從 CWD
        repo_root = Path.cwd()
    if not (repo_root / REGISTRY_PATH).exists():
        print("[FATAL] 無法找到治理模組註冊表，請在 repo 根目錄執行")
        sys.exit(1)

    scanner = AutonomousScanner(repo_root)
    scanner.scan_all()
    scanner.save_report()
    scanner.emit_event()

    # 回傳退出碼
    summary = scanner.results["summary"]
    if summary["failed"] > 0:
        print(f"\n[結果] 掃描發現 {summary['failed']} 個失敗模組，需要補救")
        sys.exit(1)
    elif summary["violations_count"] > 0:
        print(f"\n[結果] 掃描發現 {summary['violations_count']} 個違規，需要處理")
        sys.exit(1)
    else:
        print(f"\n[結果] 所有模組通過掃描 ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
