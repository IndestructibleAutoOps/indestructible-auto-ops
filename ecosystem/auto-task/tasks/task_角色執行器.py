"""角色執行器任務

整合自: ecosystem/enforcers/role_executor.py
用途: MNGA 角色執行層 - 角色調用和執行生命週期管理
"""

import logging
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class RoleExecutor:
    """角色執行器"""

    def __init__(self):
        """初始化執行器"""
        self.roles_registry = {}
        self.execution_history = []

    def register_role(self, role_id: str, role_handler: callable) -> bool:
        """註冊角色處理器"""
        if role_id in self.roles_registry:
            logger.warning(f"⚠️  角色已存在，將覆蓋: {role_id}")

        self.roles_registry[role_id] = {
            "handler": role_handler,
            "registered_at": datetime.now().isoformat(),
            "invocation_count": 0,
        }

        logger.info(f"✅ 註冊角色: {role_id}")
        return True

    def invoke_role(
        self,
        role_id: str,
        input_data: Any,
        parameters: Dict[str, Any] = None,
        actor: str = "system",
    ) -> Dict[str, Any]:
        """調用角色"""
        invocation_id = str(uuid.uuid4())
        start_time = datetime.now()

        result = {
            "invocation_id": invocation_id,
            "role_id": role_id,
            "status": "unknown",
            "timestamp": start_time.isoformat(),
            "actor": actor,
            "result": None,
            "error": None,
        }

        if role_id not in self.roles_registry:
            result["status"] = "failed"
            result["error"] = f"角色未註冊: {role_id}"
            logger.error(f"❌ {result['error']}")
            return result

        try:
            # 執行角色處理器
            role_info = self.roles_registry[role_id]
            handler = role_info["handler"]

            logger.info(f"▶️  調用角色: {role_id} [invocation={invocation_id[:8]}]")

            handler_result = handler(input_data, parameters or {})

            # 更新統計
            role_info["invocation_count"] += 1
            role_info["last_invocation"] = datetime.now().isoformat()

            # 記錄結果
            result["status"] = "success"
            result["result"] = handler_result

            duration = (datetime.now() - start_time).total_seconds() * 1000
            result["duration_ms"] = int(duration)

            logger.info(f"✅ 角色執行完成: {role_id} ({duration:.0f}ms)")

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logger.error(f"❌ 角色執行失敗 {role_id}: {e}")

        # 記錄歷史
        self.execution_history.append(result)

        return result

    def get_role_statistics(self) -> Dict[str, Any]:
        """取得角色統計"""
        stats = {
            "total_roles": len(self.roles_registry),
            "total_invocations": len(self.execution_history),
            "roles": {},
        }

        for role_id, role_info in self.roles_registry.items():
            stats["roles"][role_id] = {
                "invocation_count": role_info.get("invocation_count", 0),
                "last_invocation": role_info.get("last_invocation", "never"),
            }

        return stats

    def list_roles(self) -> List[str]:
        """列出所有已註冊角色"""
        return list(self.roles_registry.keys())


class RoleExecutorTask(Task):
    """角色執行器任務"""

    name = "角色執行器"
    priority = 4

    def __init__(self):
        super().__init__()
        self.executor_engine = RoleExecutor()
        self._register_default_roles()

    def _register_default_roles(self):
        """註冊預設角色"""

        # 監控角色
        def monitor_role(input_data, params):
            return {"status": "monitoring", "data": input_data}

        # 驗證角色
        def validator_role(input_data, params):
            return {"status": "validated", "valid": True}

        # 審計角色
        def auditor_role(input_data, params):
            return {"status": "audited", "findings": []}

        self.executor_engine.register_role("monitor", monitor_role)
        self.executor_engine.register_role("validator", validator_role)
        self.executor_engine.register_role("auditor", auditor_role)

    def execute(self):
        """執行角色管理"""
        logger.info("🎭 檢查角色執行器...")

        # 列出所有角色
        roles = self.executor_engine.list_roles()
        logger.info(f"📋 已註冊角色數: {len(roles)}")
        for role_id in roles:
            logger.info(f"  - {role_id}")

        # 測試角色調用
        test_result = self.executor_engine.invoke_role(
            "monitor", {"test": "data"}, {"mode": "test"}
        )

        if test_result["status"] == "success":
            logger.info("✅ 角色調用測試通過")

        # 顯示統計
        stats = self.executor_engine.get_role_statistics()
        logger.info(f"📊 執行統計:")
        logger.info(f"  總角色數: {stats['total_roles']}")
        logger.info(f"  總調用數: {stats['total_invocations']}")


# 註冊任務：每 2 小時檢查一次
executor.register(RoleExecutorTask, interval=7200, priority=4)
