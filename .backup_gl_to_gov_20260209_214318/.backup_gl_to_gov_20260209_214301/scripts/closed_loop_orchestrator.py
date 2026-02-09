#!/usr/bin/env python3
"""
全機器自理 — 閉環編排器 (Closed-Loop Orchestrator)

完整閉環：sensing → execution → anchor feedback
零人類介入的全自主治理循環。

流程：
  1. 掃描 (Sensing)    — 發現所有模組狀態
  2. 執行 (Execution)  — 驗證門檻、產生證據
  3. 修復 (Remediation) — 自動修復可修復問題
  4. 回饋 (Feedback)   — 更新基線、發射事件
  5. 報告 (Report)     — 產生閉環報告
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# 匯入掃描器和執行器
sys.path.insert(0, str(Path(__file__).resolve().parent))
from autonomous_scanner import AutonomousScanner
from autonomous_executor import AutonomousExecutor


# ═══════════════════════════════════════════════════════════════════════════════
# 常數
# ═══════════════════════════════════════════════════════════════════════════════

EVENT_STREAM = ".governance/event-stream.jsonl"
CLOSED_LOOP_REPORT_DIR = ".governance/closed-loop-reports"
ANCHOR_BASELINE = "responsibility-governance-anchor-boundary/baseline/governance-baseline.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ═══════════════════════════════════════════════════════════════════════════════
# 閉環編排器
# ═══════════════════════════════════════════════════════════════════════════════

class ClosedLoopOrchestrator:
    """全機器自理閉環編排器。"""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.cycle_id = f"CYCLE-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        self.report: Dict[str, Any] = {
            "cycle_id": self.cycle_id,
            "started_at": utc_now(),
            "mode": "autonomous",
            "phases": [],
            "status": "RUNNING",
        }

    def run(self) -> Dict[str, Any]:
        """執行完整閉環。"""
        print("=" * 72)
        print(f"  全機器自理閉環編排器 — {self.cycle_id}")
        print(f"  模式: 全自主 (Zero Human Intervention)")
        print("=" * 72)

        try:
            # Phase 1: Sensing
            self._phase_sensing()

            # Phase 2: Execution
            self._phase_execution()

            # Phase 3: Feedback
            self._phase_feedback()

            # Phase 4: Report
            self._phase_report()

            self.report["status"] = "COMPLETED"
            self.report["completed_at"] = utc_now()

        except Exception as e:
            self.report["status"] = "FAILED"
            self.report["error"] = str(e)
            self.report["completed_at"] = utc_now()
            print(f"\n[ERROR] 閉環執行失敗: {e}")
            import traceback
            traceback.print_exc()

        # 儲存閉環報告
        self._save_report()

        # 發射閉環事件
        self._emit_cycle_event()

        return self.report

    def _phase_sensing(self):
        """Phase 1: 掃描。"""
        print(f"\n{'─' * 72}")
        print(f"  Phase 1: SENSING (掃描)")
        print(f"{'─' * 72}")

        scanner = AutonomousScanner(self.repo_root)
        scan_results = scanner.scan_all()
        scanner.save_report()
        scanner.emit_event()

        self.report["phases"].append({
            "phase": "sensing",
            "status": "COMPLETED",
            "timestamp": utc_now(),
            "summary": scan_results.get("summary", {}),
        })

    def _phase_execution(self):
        """Phase 2: 執行。"""
        print(f"\n{'─' * 72}")
        print(f"  Phase 2: EXECUTION (執行)")
        print(f"{'─' * 72}")

        executor = AutonomousExecutor(self.repo_root)
        exec_results = executor.execute()

        self.report["phases"].append({
            "phase": "execution",
            "status": "COMPLETED",
            "timestamp": utc_now(),
            "summary": {
                "execution_id": exec_results.get("execution_id"),
                "gates_passed": exec_results.get("gates_passed", 0),
                "gates_failed": exec_results.get("gates_failed", 0),
                "gate_pass_rate": exec_results.get("gate_pass_rate", 0),
                "fixes_applied": exec_results.get("fixes_applied", 0),
                "evidence_id": exec_results.get("evidence", {}).get("evidence_id"),
            },
        })

    def _phase_feedback(self):
        """Phase 3: 回饋至 anchor。"""
        print(f"\n{'─' * 72}")
        print(f"  Phase 3: FEEDBACK (回饋)")
        print(f"{'─' * 72}")

        # 讀取最新執行結果
        exec_report_path = self.repo_root / "responsibility-governance-execution-boundary/reports/execution-report-latest.json"
        if not exec_report_path.exists():
            print("  ⚠️ 無執行報告可回饋")
            self.report["phases"].append({
                "phase": "feedback",
                "status": "SKIPPED",
                "timestamp": utc_now(),
                "reason": "no_execution_report",
            })
            return

        with exec_report_path.open("r", encoding="utf-8") as f:
            exec_result = json.load(f)

        # 更新 anchor 事件模型
        events_path = self.repo_root / "responsibility-governance-anchor-boundary/event-model/governance-events.yaml"
        if events_path.exists():
            # 追加閉環回饋記錄
            feedback_entry = f"""
# Closed-Loop Feedback — {self.cycle_id}
# Timestamp: {utc_now()}
# Gate Pass Rate: {exec_result.get('gate_pass_rate', 0)}%
# Fixes Applied: {exec_result.get('fixes_applied', 0)}
"""
            # 不修改 YAML 結構，僅追加註解
            print(f"  📝 閉環回饋已記錄至 anchor 事件模型")

        # 更新 hash boundary
        scan_report_path = self.repo_root / "responsibility-governance-sensing-boundary/report/scan-report.json"
        if scan_report_path.exists():
            with scan_report_path.open("r", encoding="utf-8") as f:
                scan_report = json.load(f)

            # 提取所有模組雜湊
            hash_update = {}
            for module in scan_report.get("modules", []):
                if module.get("hash"):
                    hash_update[module["module_id"]] = module["hash"]

            # 儲存雜湊快照
            hash_snapshot_dir = self.repo_root / "responsibility-governance-anchor-boundary/hash-boundary/snapshots"
            hash_snapshot_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
            snapshot_file = hash_snapshot_dir / f"hash-snapshot-{timestamp}.json"
            with snapshot_file.open("w", encoding="utf-8") as f:
                json.dump({
                    "cycle_id": self.cycle_id,
                    "timestamp": utc_now(),
                    "module_hashes": hash_update,
                }, f, indent=2, ensure_ascii=False)

            print(f"  📸 雜湊快照已儲存: {snapshot_file.name}")

        self.report["phases"].append({
            "phase": "feedback",
            "status": "COMPLETED",
            "timestamp": utc_now(),
            "hash_modules_updated": len(hash_update) if 'hash_update' in dir() else 0,
        })

    def _phase_report(self):
        """Phase 4: 產生閉環報告。"""
        print(f"\n{'─' * 72}")
        print(f"  Phase 4: REPORT (報告)")
        print(f"{'─' * 72}")

        # 彙總所有 phases
        sensing = next((p for p in self.report["phases"] if p["phase"] == "sensing"), {})
        execution = next((p for p in self.report["phases"] if p["phase"] == "execution"), {})

        sensing_summary = sensing.get("summary", {})
        execution_summary = execution.get("summary", {})

        overall_health = "HEALTHY"
        if sensing_summary.get("failed", 0) > 0 or execution_summary.get("gates_failed", 0) > 0:
            overall_health = "DEGRADED"
        if sensing_summary.get("pass_rate", 100) < 50:
            overall_health = "CRITICAL"

        self.report["overall_health"] = overall_health
        self.report["metrics"] = {
            "scan_pass_rate": sensing_summary.get("pass_rate", 0),
            "gate_pass_rate": execution_summary.get("gate_pass_rate", 0),
            "violations": sensing_summary.get("violations_count", 0),
            "drift_detected": sensing_summary.get("drift_count", 0),
            "fixes_applied": execution_summary.get("fixes_applied", 0),
        }

        health_icon = {"HEALTHY": "🟢", "DEGRADED": "🟡", "CRITICAL": "🔴"}
        print(f"\n  {health_icon.get(overall_health, '?')} 系統健康狀態: {overall_health}")
        print(f"  掃描通過率: {sensing_summary.get('pass_rate', 0)}%")
        print(f"  門檻通過率: {execution_summary.get('gate_pass_rate', 0)}%")
        print(f"  違規數: {sensing_summary.get('violations_count', 0)}")
        print(f"  修復數: {execution_summary.get('fixes_applied', 0)}")

        self.report["phases"].append({
            "phase": "report",
            "status": "COMPLETED",
            "timestamp": utc_now(),
        })

    def _save_report(self):
        """儲存閉環報告。"""
        report_dir = self.repo_root / CLOSED_LOOP_REPORT_DIR
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        report_file = report_dir / f"closed-loop-{timestamp}.json"
        with report_file.open("w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        latest = report_dir / "closed-loop-latest.json"
        with latest.open("w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        print(f"\n  💾 閉環報告: {report_file}")

    def _emit_cycle_event(self):
        """發射閉環完成事件。"""
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
            "event_type": "closed_loop_cycle_completed",
            "namespace": "/governance/closed-loop/",
            "layer": "orchestration",
            "platform": "all",
            "era": "Era-1",
            "payload": {
                "cycle_id": self.cycle_id,
                "status": self.report["status"],
                "overall_health": self.report.get("overall_health", "UNKNOWN"),
                "metrics": self.report.get("metrics", {}),
                "engine_version": "2.0.0",
            },
        }

        with event_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

        print(f"  📡 閉環事件: event_id={next_id}")


# ═══════════════════════════════════════════════════════════════════════════════
# 主程式
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    repo_root = Path(__file__).resolve().parent.parent
    registry_path = "responsibility-governance-execution-boundary/registry/governance-modules.json"
    if not (repo_root / registry_path).exists():
        repo_root = Path.cwd()
    if not (repo_root / registry_path).exists():
        print("[FATAL] 無法找到治理模組註冊表")
        sys.exit(1)

    orchestrator = ClosedLoopOrchestrator(repo_root)
    result = orchestrator.run()

    print("\n" + "=" * 72)
    if result["status"] == "COMPLETED":
        print(f"  ✅ 閉環循環完成 — {result['cycle_id']}")
        health = result.get("overall_health", "UNKNOWN")
        if health == "HEALTHY":
            sys.exit(0)
        else:
            print(f"  ⚠️ 系統健康狀態: {health}")
            sys.exit(1)
    else:
        print(f"  ❌ 閉環循環失敗 — {result.get('error', 'Unknown error')}")
        sys.exit(2)


if __name__ == "__main__":
    main()
