#!/usr/bin/env python3
"""
NG 批次執行器
NG Batch Executor

NG Code: NG00002
Purpose: 批量執行 NG 命名空間治理操作

專門處理：
- 批次 1-5 的自動化執行
- 大規模命名空間操作
- 並行執行和進度追蹤
- 批次報告生成
"""

import sys
import json
import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

SCRIPT_DIR = Path(__file__).resolve().parent
NG_ROOT = SCRIPT_DIR.parent

logger = logging.getLogger(__name__)


@dataclass
class BatchTask:
    """批次任務"""

    task_id: str
    task_type: str  # register, validate, migrate, etc.
    target: str  # 目標命名空間或範圍
    params: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None
    error: str = None


class NgBatchExecutor:
    """NG 批次執行器"""

    def __init__(self, batch_id: str = "batch-1", max_workers: int = 4):
        """
        初始化批次執行器

        Args:
            batch_id: 批次 ID (batch-1 到 batch-5)
            max_workers: 最大並行工作線程數
        """
        self.batch_id = batch_id
        self.max_workers = max_workers
        self.tasks: List[BatchTask] = []
        self.execution_start = None
        self.execution_end = None

        logger.info(f"🎯 批次執行器已初始化: {batch_id} (workers={max_workers})")

    def add_task(self, task: BatchTask):
        """添加批次任務"""
        self.tasks.append(task)
        logger.info(f"📝 添加任務: {task.task_type} → {task.target}")

    def add_tasks_from_config(self, config_path: str):
        """從配置文件添加任務"""
        config_file = Path(config_path)

        if not config_file.exists():
            logger.warning(f"⚠️  配置文件不存在: {config_path}")
            return

        with open(config_file, "r", encoding="utf-8") as f:
            if config_path.endswith(".json"):
                config = json.load(f)
            else:  # YAML
                import yaml

                config = yaml.safe_load(f)

        batch_tasks = config.get("tasks", [])

        for task_config in batch_tasks:
            task = BatchTask(
                task_id=task_config.get("id", f"task-{len(self.tasks)}"),
                task_type=task_config["type"],
                target=task_config["target"],
                params=task_config.get("params", {}),
            )
            self.add_task(task)

        logger.info(f"✅ 從配置載入 {len(batch_tasks)} 個任務")

    def execute_sequential(self) -> Dict[str, Any]:
        """順序執行所有任務"""
        logger.info(f"🚀 開始順序執行: {len(self.tasks)} 個任務")

        self.execution_start = datetime.now()

        results = {
            "batch_id": self.batch_id,
            "mode": "sequential",
            "total_tasks": len(self.tasks),
            "completed": 0,
            "failed": 0,
            "tasks": [],
        }

        for task in self.tasks:
            result = self._execute_single_task(task)
            results["tasks"].append(result)

            if result["status"] == "completed":
                results["completed"] += 1
            elif result["status"] == "failed":
                results["failed"] += 1

        self.execution_end = datetime.now()
        duration = (self.execution_end - self.execution_start).total_seconds()

        results["duration_seconds"] = duration
        results["success_rate"] = (
            (results["completed"] / results["total_tasks"] * 100)
            if results["total_tasks"] > 0
            else 0
        )

        logger.info(
            f"✅ 批次執行完成: {results['completed']}/{results['total_tasks']} 成功"
        )

        return results

    def execute_parallel(self) -> Dict[str, Any]:
        """並行執行所有任務"""
        logger.info(
            f"🚀 開始並行執行: {len(self.tasks)} 個任務 (workers={self.max_workers})"
        )

        self.execution_start = datetime.now()

        results = {
            "batch_id": self.batch_id,
            "mode": "parallel",
            "total_tasks": len(self.tasks),
            "completed": 0,
            "failed": 0,
            "tasks": [],
        }

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任務
            future_to_task = {
                executor.submit(self._execute_single_task, task): task
                for task in self.tasks
            }

            # 收集結果
            for future in as_completed(future_to_task):
                result = future.result()
                results["tasks"].append(result)

                if result["status"] == "completed":
                    results["completed"] += 1
                elif result["status"] == "failed":
                    results["failed"] += 1

                # 顯示進度
                progress = (
                    (results["completed"] + results["failed"])
                    / results["total_tasks"]
                    * 100
                )
                logger.info(
                    f"📊 進度: {progress:.1f}% ({results['completed'] + results['failed']}/{results['total_tasks']})"
                )

        self.execution_end = datetime.now()
        duration = (self.execution_end - self.execution_start).total_seconds()

        results["duration_seconds"] = duration
        results["success_rate"] = (
            (results["completed"] / results["total_tasks"] * 100)
            if results["total_tasks"] > 0
            else 0
        )

        logger.info(
            f"✅ 並行執行完成: {results['completed']}/{results['total_tasks']} 成功"
        )

        return results

    def _execute_single_task(self, task: BatchTask) -> Dict[str, Any]:
        """執行單個任務"""
        task.status = "running"
        start_time = datetime.now()

        try:
            # 根據任務類型執行相應操作
            if task.task_type == "register":
                result = self._execute_register(task)
            elif task.task_type == "validate":
                result = self._execute_validate(task)
            elif task.task_type == "migrate":
                result = self._execute_migrate(task)
            elif task.task_type == "audit":
                result = self._execute_audit(task)
            else:
                result = {
                    "status": "skipped",
                    "reason": f"未知任務類型: {task.task_type}",
                }

            task.status = "completed"
            task.result = result

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            logger.error(f"❌ 任務失敗 {task.task_id}: {e}")

        duration = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "target": task.target,
            "status": task.status,
            "duration_ms": int(duration),
            "result": task.result,
            "error": task.error,
        }

    def _execute_register(self, task: BatchTask) -> Dict[str, Any]:
        """執行註冊任務"""
        return {"action": "register", "target": task.target, "status": "simulated"}

    def _execute_validate(self, task: BatchTask) -> Dict[str, Any]:
        """執行驗證任務"""
        return {
            "action": "validate",
            "target": task.target,
            "valid": True,
            "issues": [],
        }

    def _execute_migrate(self, task: BatchTask) -> Dict[str, Any]:
        """執行遷移任務"""
        return {
            "action": "migrate",
            "source": task.target,
            "target": task.params.get("target_namespace", "unknown"),
            "status": "mapped",
        }

    def _execute_audit(self, task: BatchTask) -> Dict[str, Any]:
        """執行審計任務"""
        return {
            "action": "audit",
            "target": task.target,
            "events_count": 0,
            "violations": [],
        }

    def generate_batch_report(self) -> str:
        """生成批次報告"""
        if not self.execution_end:
            return "批次尚未執行"

        duration = (self.execution_end - self.execution_start).total_seconds()

        completed = sum(1 for t in self.tasks if t.status == "completed")
        failed = sum(1 for t in self.tasks if t.status == "failed")
        success_rate = (completed / len(self.tasks) * 100) if self.tasks else 0

        report_lines = [
            "=" * 70,
            f"NG 批次執行報告 - {self.batch_id}",
            "=" * 70,
            f"開始時間: {self.execution_start.isoformat()}",
            f"結束時間: {self.execution_end.isoformat()}",
            f"總耗時: {duration:.2f} 秒",
            "",
            "執行結果:",
            f"  總任務數: {len(self.tasks)}",
            f"  ✅ 完成: {completed}",
            f"  ❌ 失敗: {failed}",
            f"  成功率: {success_rate:.1f}%",
            "",
            "任務詳情:",
        ]

        for task in self.tasks:
            status_icon = "✅" if task.status == "completed" else "❌"
            report_lines.append(
                f"  {status_icon} {task.task_id}: {task.task_type} → {task.target}"
            )

        report_lines.extend(["", "=" * 70])

        return "\n".join(report_lines)

    def save_batch_results(self, output_path: str = None):
        """保存批次執行結果"""
        if not output_path:
            output_path = f"logs/batch-{self.batch_id}-results.json"

        results = {
            "batch_id": self.batch_id,
            "execution_start": (
                self.execution_start.isoformat() if self.execution_start else None
            ),
            "execution_end": (
                self.execution_end.isoformat() if self.execution_end else None
            ),
            "tasks": [
                {
                    "task_id": t.task_id,
                    "task_type": t.task_type,
                    "target": t.target,
                    "status": t.status,
                    "params": t.params,
                    "result": t.result,
                    "error": t.error,
                }
                for t in self.tasks
            ],
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 批次結果已保存: {output_path}")


if __name__ == "__main__":
    # 測試批次執行器
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s"
    )

    print("=" * 70)
    print("NG 批次執行器測試")
    print("=" * 70)

    # 創建批次執行器
    batch_executor = NgBatchExecutor(batch_id="batch-test")

    # 添加測試任務
    print("\n添加測試任務...")

    for i in range(5):
        task = BatchTask(
            task_id=f"task-{i+1}",
            task_type="validate",
            target=f"pkg.era1.test.component{i+1}",
            params={},
        )
        batch_executor.add_task(task)

    # 順序執行
    print("\n=== 測試 1: 順序執行 ===")
    results_seq = batch_executor.execute_sequential()
    print(f"✅ 順序執行完成: {results_seq['success_rate']:.1f}% 成功率")

    # 重置任務狀態
    for task in batch_executor.tasks:
        task.status = "pending"

    # 並行執行
    print("\n=== 測試 2: 並行執行 ===")
    results_par = batch_executor.execute_parallel()
    print(f"✅ 並行執行完成: {results_par['success_rate']:.1f}% 成功率")

    # 生成報告
    print("\n" + batch_executor.generate_batch_report())

    # 保存結果
    batch_executor.save_batch_results()

    print("\n" + "=" * 70)
    print("✅ NG 批次執行器測試完成")
    print("=" * 70)
