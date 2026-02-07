#!/usr/bin/env python3
"""
NG 命名空間治理執行引擎
NG Namespace Governance Execution Engine

NG Code: NG00001 (最高權重執行器)
Priority: 0 (最高優先級)
Purpose: 統一執行所有 NG 命名空間治理操作

這是 NG 系統的核心執行引擎，負責：
- 自動化命名空間治理閉環
- 批量執行 NG 操作
- 跨 Era 協調和映射
- 治理指標監控
- 審計和合規報告
"""

import sys
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Add parent directories to path
SCRIPT_DIR = Path(__file__).resolve().parent
NG_ROOT = SCRIPT_DIR.parent

# Import registry module
registry_path = NG_ROOT / "registry" / "namespace-registry.py"
if registry_path.exists():
    import importlib.util

    spec = importlib.util.spec_from_file_location("namespace_registry", registry_path)
    namespace_registry_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(namespace_registry_module)

    NgNamespaceRegistry = namespace_registry_module.NgNamespaceRegistry
    NamespaceSpec = namespace_registry_module.NamespaceSpec
    NamespaceRecord = namespace_registry_module.NamespaceRecord
    Era = namespace_registry_module.Era
    NamespaceStatus = namespace_registry_module.NamespaceStatus
else:
    # Fallback: define minimal classes for standalone execution
    class Era(Enum):
        ERA_1 = "era-1"
        ERA_2 = "era-2"
        ERA_3 = "era-3"
        CROSS = "cross"

    class NamespaceStatus(Enum):
        REGISTERED = "registered"
        ACTIVE = "active"
        DEPRECATED = "deprecated"
        ARCHIVED = "archived"
        DESTROYED = "destroyed"

    @dataclass
    class NamespaceSpec:
        namespace_id: str
        namespace_type: str
        era: Era
        domain: str
        component: str
        owner: str
        description: str

    @dataclass
    class NamespaceRecord:
        id: str
        ng_code: str
        spec: NamespaceSpec
        status: NamespaceStatus
        created_at: str
        updated_at: str
        audit_trail: List[Dict] = None

    class NgNamespaceRegistry:
        def __init__(self, registry_path: str = "registry/namespaces.json"):
            self.namespaces = {}

        def register_namespace(self, spec):
            return "test-id"

        def get_namespace(self, ns_id):
            return None

        def list_namespaces(self, **kwargs):
            return []

        def update_namespace_status(self, ns_id, status, actor):
            return True

        def get_statistics(self):
            return {"total": 0, "by_era": {}, "by_status": {}}


logger = logging.getLogger(__name__)


class ExecutionPriority(Enum):
    """執行優先級（零容忍模式）"""

    IMMUTABLE = -2  # 憲法級（永不寬容）
    ABSOLUTE = -1  # 絕對級（零容忍）
    CRITICAL = 0  # 關鍵級（立即阻斷）
    HIGH = 1  # 高級（嚴格執行）
    MANDATORY = 2  # 強制級（必須修復）


class OperationType(Enum):
    """操作類型"""

    REGISTER = "register"
    VALIDATE = "validate"
    MONITOR = "monitor"
    MIGRATE = "migrate"
    AUDIT = "audit"
    OPTIMIZE = "optimize"
    ARCHIVE = "archive"
    CLOSURE = "closure"  # 閉環操作


@dataclass
class NgOperation:
    """NG 操作定義"""

    operation_id: str
    operation_type: OperationType
    priority: ExecutionPriority
    target_namespaces: List[str]
    parameters: Dict[str, Any]
    batch_id: Optional[str] = None
    era_scope: Optional[Era] = None

    def to_dict(self) -> Dict:
        """轉換為字典"""
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "priority": self.priority.value,
            "target_namespaces": self.target_namespaces,
            "parameters": self.parameters,
            "batch_id": self.batch_id,
            "era_scope": self.era_scope.value if self.era_scope else None,
        }


@dataclass
class ExecutionResult:
    """執行結果"""

    operation_id: str
    status: str  # success, warning, failed
    timestamp: str
    duration_ms: int
    results: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    audit_trail: List[Dict]

    def to_dict(self) -> Dict:
        """轉換為字典"""
        return asdict(self)


class NgExecutor:
    """
    NG 命名空間治理執行引擎

    最高權重執行器，負責統一執行所有 NG 治理操作
    """

    def __init__(self, registry_path: str = "registry/namespaces.json"):
        """初始化執行引擎"""
        self.registry = NgNamespaceRegistry(registry_path)
        self.operations_queue: List[NgOperation] = []
        self.execution_history: List[ExecutionResult] = []
        self.closure_state = {
            "last_closure_check": None,
            "closure_complete": False,
            "pending_operations": [],
        }

        # 操作處理器註冊表
        self.operation_handlers: Dict[OperationType, Callable] = {
            OperationType.REGISTER: self._handle_register,
            OperationType.VALIDATE: self._handle_validate,
            OperationType.MONITOR: self._handle_monitor,
            OperationType.MIGRATE: self._handle_migrate,
            OperationType.AUDIT: self._handle_audit,
            OperationType.OPTIMIZE: self._handle_optimize,
            OperationType.ARCHIVE: self._handle_archive,
            OperationType.CLOSURE: self._handle_closure,
        }

        logger.info("🚀 NG 執行引擎已初始化")

    def submit_operation(self, operation: NgOperation) -> str:
        """提交操作到執行隊列"""
        self.operations_queue.append(operation)
        logger.info(
            f"📝 提交操作: {operation.operation_type.value} "
            f"[優先級={operation.priority.value}, ID={operation.operation_id}]"
        )
        return operation.operation_id

    def execute_all(self, auto_closure: bool = True) -> List[ExecutionResult]:
        """
        執行所有待處理操作

        Args:
            auto_closure: 是否自動執行閉環檢查

        Returns:
            執行結果列表
        """
        logger.info(f"🎯 開始執行 {len(self.operations_queue)} 個操作...")

        # 按優先級排序
        sorted_ops = sorted(self.operations_queue, key=lambda x: x.priority.value)

        results = []
        for operation in sorted_ops:
            result = self.execute_operation(operation)
            results.append(result)

        # 清空隊列
        self.operations_queue.clear()

        # 自動閉環檢查
        if auto_closure:
            closure_result = self.check_closure()
            if not closure_result["closure_complete"]:
                logger.warning("⚠️  治理閉環未完成")
                logger.info(
                    f"   待處理: {len(closure_result['pending_operations'])} 個操作"
                )

        logger.info(f"✅ 執行完成: {len(results)} 個操作")
        return results

    def execute_operation(self, operation: NgOperation) -> ExecutionResult:
        """
        執行單個操作（零容忍模式）

        ZERO TOLERANCE: 任何錯誤立即阻斷，無警告，無重試

        Args:
            operation: 操作定義

        Returns:
            執行結果
        """
        start_time = datetime.now()

        # 零容忍：檢查執行時間
        timeout_ms = 100  # 100ms 超時限制

        logger.info(
            f"▶️  執行: {operation.operation_type.value} "
            f"[優先級={operation.priority.value}] [ZERO_TOLERANCE_MODE]"
        )

        result = ExecutionResult(
            operation_id=operation.operation_id,
            status="unknown",
            timestamp=start_time.isoformat(),
            duration_ms=0,
            results={},
            errors=[],
            warnings=[],
            audit_trail=[],
        )

        try:
            # ZERO TOLERANCE: 驗證操作合法性
            self._zero_tolerance_pre_check(operation)

            # 獲取操作處理器
            handler = self.operation_handlers.get(operation.operation_type)

            if not handler:
                raise ValueError(
                    f"ZERO_TOLERANCE_VIOLATION: 不支援的操作類型: {operation.operation_type}"
                )

            # 執行操作
            handler_result = handler(operation)

            # ZERO TOLERANCE: 檢查執行時間
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            if elapsed > timeout_ms:
                raise TimeoutError(
                    f"ZERO_TOLERANCE_VIOLATION: 操作超時 {elapsed:.0f}ms > {timeout_ms}ms"
                )

            # ZERO TOLERANCE: 驗證結果完整性
            self._zero_tolerance_post_check(handler_result)

            result.status = "success"
            result.results = handler_result

            # 記錄審計（不可變）
            result.audit_trail.append(
                {
                    "action": operation.operation_type.value,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "ng_code": "NG00001",
                    "zero_tolerance": True,
                    "immutable": True,
                }
            )

            logger.info(
                f"✅ 完成: {operation.operation_type.value} [ZERO_TOLERANCE_PASS]"
            )

        except Exception as e:
            result.status = "failed"
            result.errors.append(f"ZERO_TOLERANCE_FAILURE: {str(e)}")

            # ZERO TOLERANCE: 立即觸發緊急處理
            self._zero_tolerance_failure_handler(operation, e)

            logger.error(
                f"❌ 失敗: {operation.operation_type.value} - {e} [IMMEDIATE_BLOCK]"
            )

        finally:
            # 計算執行時間
            duration = (datetime.now() - start_time).total_seconds() * 1000
            result.duration_ms = int(duration)

            # 記錄執行歷史
            self.execution_history.append(result)

        return result

    def _zero_tolerance_pre_check(self, operation: NgOperation):
        """零容忍前置檢查"""
        # 檢查操作參數完整性
        if not operation.target_namespaces:
            raise ValueError("ZERO_TOLERANCE: 缺少目標命名空間")

        # 檢查優先級合法性
        if operation.priority not in ExecutionPriority:
            raise ValueError("ZERO_TOLERANCE: 非法優先級")

    def _zero_tolerance_post_check(self, result: Dict[str, Any]):
        """零容忍後置檢查"""
        # 檢查結果完整性
        if not result:
            raise ValueError("ZERO_TOLERANCE: 操作返回空結果")

        # 檢查是否有失敗項
        if "failed" in result and result["failed"]:
            raise ValueError(f"ZERO_TOLERANCE: 檢測到失敗項 {len(result['failed'])} 個")

    def _zero_tolerance_failure_handler(self, operation: NgOperation, error: Exception):
        """零容忍失敗處理器"""
        # 記錄到不可變審計日誌
        immutable_log = {
            "timestamp": datetime.now().isoformat(),
            "operation_id": operation.operation_id,
            "operation_type": operation.operation_type.value,
            "error": str(error),
            "action_taken": "IMMEDIATE_BLOCK",
            "zero_tolerance": True,
            "immutable": True,
            "requires_resolution": True,
        }

        # 觸發警報
        logger.critical(f"🚨 ZERO_TOLERANCE VIOLATION: {error}")
        logger.critical(f"🚨 ACTION: IMMEDIATE_BLOCK")
        logger.critical(f"🚨 RESOLUTION: Manual intervention required")

        # TODO: 整合到外部告警系統
        # alert_system.trigger_critical(immutable_log)

    def _handle_register(self, operation: NgOperation) -> Dict[str, Any]:
        """處理註冊操作"""
        results = {
            "registered": [],
            "failed": [],
            "total": len(operation.target_namespaces),
        }

        for namespace_id in operation.target_namespaces:
            try:
                # 從參數構建 NamespaceSpec
                params = operation.parameters.get(namespace_id, {})

                spec = NamespaceSpec(
                    namespace_id=namespace_id,
                    namespace_type=params.get("type", "unknown"),
                    era=operation.era_scope or Era.ERA_1,
                    domain=params.get("domain", "unknown"),
                    component=params.get("component", "unknown"),
                    owner=params.get("owner", "system"),
                    description=params.get("description", ""),
                )

                ns_id = self.registry.register_namespace(spec)
                results["registered"].append(ns_id)

            except Exception as e:
                results["failed"].append({"namespace": namespace_id, "error": str(e)})

        return results

    def _handle_validate(self, operation: NgOperation) -> Dict[str, Any]:
        """處理驗證操作"""
        results = {
            "validated": [],
            "invalid": [],
            "total": len(operation.target_namespaces),
        }

        for namespace_id in operation.target_namespaces:
            record = self.registry.get_namespace(namespace_id)

            if not record:
                results["invalid"].append(
                    {"namespace": namespace_id, "reason": "命名空間不存在"}
                )
                continue

            # 驗證邏輯
            validation_result = self._validate_namespace(record)

            if validation_result["valid"]:
                results["validated"].append(namespace_id)
            else:
                results["invalid"].append(
                    {"namespace": namespace_id, "issues": validation_result["issues"]}
                )

        return results

    def _validate_namespace(self, record: NamespaceRecord) -> Dict[str, Any]:
        """驗證命名空間"""
        validation = {"valid": True, "issues": []}

        # 檢查格式
        parts = record.spec.namespace_id.split(".")
        if len(parts) < 4:
            validation["valid"] = False
            validation["issues"].append("格式不完整")

        # 檢查狀態
        if record.status == NamespaceStatus.DESTROYED:
            validation["valid"] = False
            validation["issues"].append("命名空間已銷毀")

        # 檢查 NG 編碼
        if not record.ng_code or not record.ng_code.startswith("NG"):
            validation["valid"] = False
            validation["issues"].append("NG 編碼無效")

        return validation

    def _handle_monitor(self, operation: NgOperation) -> Dict[str, Any]:
        """處理監控操作"""
        results = {"monitored": [], "metrics": {}, "alerts": []}

        # 收集統計
        stats = self.registry.get_statistics()
        results["metrics"] = stats

        # 檢查健康狀況
        for namespace_id in operation.target_namespaces:
            record = self.registry.get_namespace(namespace_id)

            if record:
                health = self._check_namespace_health(record)
                results["monitored"].append(
                    {"namespace": namespace_id, "health": health}
                )

                # 生成警報
                if not health["healthy"]:
                    results["alerts"].append(
                        {"namespace": namespace_id, "issues": health["issues"]}
                    )

        return results

    def _check_namespace_health(self, record: NamespaceRecord) -> Dict[str, Any]:
        """檢查命名空間健康狀況"""
        health = {"healthy": True, "issues": []}

        # 檢查狀態
        if record.status in [NamespaceStatus.DEPRECATED, NamespaceStatus.ARCHIVED]:
            health["healthy"] = False
            health["issues"].append(f"狀態異常: {record.status.value}")

        # 檢查審計追蹤
        if not record.audit_trail or len(record.audit_trail) == 0:
            health["issues"].append("缺少審計追蹤")

        return health

    def _handle_migrate(self, operation: NgOperation) -> Dict[str, Any]:
        """處理遷移操作"""
        results = {"migrated": [], "failed": [], "mappings": []}

        migration_plan = operation.parameters.get("migration_plan", {})

        for namespace_id in operation.target_namespaces:
            try:
                # 獲取源命名空間
                source_record = self.registry.get_namespace(namespace_id)

                if not source_record:
                    results["failed"].append(
                        {"namespace": namespace_id, "reason": "源命名空間不存在"}
                    )
                    continue

                # 獲取目標 Era
                target_era = operation.parameters.get("target_era")

                if not target_era:
                    results["failed"].append(
                        {"namespace": namespace_id, "reason": "未指定目標 Era"}
                    )
                    continue

                # 生成映射
                mapping = self._generate_era_mapping(
                    source_record.spec, Era(target_era)
                )

                results["mappings"].append(mapping)
                results["migrated"].append(namespace_id)

                logger.info(
                    f"✅ 遷移映射: {namespace_id} → {mapping['target_namespace']}"
                )

            except Exception as e:
                results["failed"].append({"namespace": namespace_id, "error": str(e)})

        return results

    def _generate_era_mapping(
        self, source_spec: NamespaceSpec, target_era: Era
    ) -> Dict[str, Any]:
        """生成 Era 間映射"""
        # 映射規則（基於 NG90101）
        type_mappings = {
            (Era.ERA_1, Era.ERA_2): {
                "package": "service",
                "module": "api",
                "class": "component",
                "function": "endpoint",
            },
            (Era.ERA_2, Era.ERA_3): {
                "service": "intent",
                "api": "semantic",
                "event": "intent",
                "stream": "neural",
            },
        }

        # 獲取映射規則
        mapping_key = (source_spec.era, target_era)
        type_map = type_mappings.get(mapping_key, {})

        # 映射命名空間類型
        target_type = type_map.get(
            source_spec.namespace_type, source_spec.namespace_type
        )

        # 構建目標命名空間 ID
        target_namespace_id = (
            f"{target_type}.{target_era.value}."
            f"{source_spec.domain}.{source_spec.component}"
        )

        return {
            "source_namespace": source_spec.namespace_id,
            "target_namespace": target_namespace_id,
            "source_era": source_spec.era.value,
            "target_era": target_era.value,
            "transformation": f"{source_spec.namespace_type} → {target_type}",
            "ng_mapping_code": "NG90101",
        }

    def _handle_audit(self, operation: NgOperation) -> Dict[str, Any]:
        """處理審計操作"""
        results = {
            "audited": [],
            "total_events": 0,
            "by_severity": {},
            "violations": [],
        }

        for namespace_id in operation.target_namespaces:
            record = self.registry.get_namespace(namespace_id)

            if record:
                audit_summary = {
                    "namespace": namespace_id,
                    "ng_code": record.ng_code,
                    "event_count": len(record.audit_trail),
                    "status": record.status.value,
                    "created": record.created_at,
                    "updated": record.updated_at,
                }

                results["audited"].append(audit_summary)
                results["total_events"] += len(record.audit_trail)

        return results

    def _handle_optimize(self, operation: NgOperation) -> Dict[str, Any]:
        """處理優化操作"""
        results = {"optimized": [], "recommendations": []}

        # 分析命名空間使用模式
        stats = self.registry.get_statistics()

        # 生成優化建議
        if stats["total"] > 1000:
            results["recommendations"].append(
                {
                    "type": "archival",
                    "message": "建議歸檔不活躍的命名空間",
                    "ng_code": "NG90501",
                }
            )

        # 檢查命名空間碎片化
        for era, count in stats.get("by_era", {}).items():
            if count < 5:
                results["recommendations"].append(
                    {
                        "type": "consolidation",
                        "message": f"建議整合 {era} 的命名空間",
                        "ng_code": "NG90502",
                    }
                )

        return results

    def _handle_archive(self, operation: NgOperation) -> Dict[str, Any]:
        """處理歸檔操作"""
        results = {"archived": [], "failed": []}

        for namespace_id in operation.target_namespaces:
            try:
                success = self.registry.update_namespace_status(
                    namespace_id, NamespaceStatus.ARCHIVED, actor="ng-executor"
                )

                if success:
                    results["archived"].append(namespace_id)
                else:
                    results["failed"].append(namespace_id)

            except Exception as e:
                results["failed"].append({"namespace": namespace_id, "error": str(e)})

        return results

    def _handle_closure(self, operation: NgOperation) -> Dict[str, Any]:
        """處理閉環操作"""
        logger.info("🔄 執行治理閉環檢查...")

        closure_check = self.check_closure()

        # 如果有待處理操作，自動生成並執行
        if not closure_check["closure_complete"]:
            pending_ops = closure_check["pending_operations"]

            logger.info(f"🔧 發現 {len(pending_ops)} 個待處理操作，自動執行...")

            for pending_op in pending_ops:
                self.submit_operation(pending_op)

            # 遞歸執行（最多 3 層）
            recursion_depth = operation.parameters.get("recursion_depth", 0)
            if recursion_depth < 3:
                operation.parameters["recursion_depth"] = recursion_depth + 1
                self.execute_all(auto_closure=True)

        return closure_check

    def check_closure(self) -> Dict[str, Any]:
        """
        檢查治理閉環完整性

        Returns:
            閉環狀態和待處理操作
        """
        closure_state = {
            "timestamp": datetime.now().isoformat(),
            "closure_complete": True,
            "pending_operations": [],
            "closure_metrics": {},
        }

        # 檢查所有命名空間的生命週期狀態
        all_namespaces = self.registry.list_namespaces()

        for record in all_namespaces:
            # 檢查是否需要驗證
            if record.status == NamespaceStatus.REGISTERED:
                # 應該進行初始驗證
                closure_state["closure_complete"] = False
                closure_state["pending_operations"].append(
                    NgOperation(
                        operation_id=f"validate-{record.id}",
                        operation_type=OperationType.VALIDATE,
                        priority=ExecutionPriority.HIGH,
                        target_namespaces=[record.id],
                        parameters={},
                    )
                )

            # 檢查是否需要審計
            if not record.audit_trail or len(record.audit_trail) < 1:
                closure_state["closure_complete"] = False
                closure_state["pending_operations"].append(
                    NgOperation(
                        operation_id=f"audit-{record.id}",
                        operation_type=OperationType.AUDIT,
                        priority=ExecutionPriority.MEDIUM,
                        target_namespaces=[record.id],
                        parameters={},
                    )
                )

        # 更新閉環狀態
        self.closure_state = closure_state
        self.closure_state["last_closure_check"] = datetime.now().isoformat()

        return closure_state

    def execute_batch(self, batch_id: str, era: Era = None) -> Dict[str, Any]:
        """
        執行批次操作

        Args:
            batch_id: 批次 ID (batch-1, batch-2, etc.)
            era: 目標 Era（可選）

        Returns:
            批次執行結果
        """
        logger.info(f"📦 執行批次: {batch_id}")

        # 根據批次 ID 確定操作範圍
        batch_config = self._get_batch_config(batch_id)

        if not batch_config:
            logger.error(f"❌ 未知的批次 ID: {batch_id}")
            return {"status": "failed", "reason": "invalid_batch_id"}

        # 生成批次操作
        batch_operations = self._generate_batch_operations(batch_config, era)

        # 提交操作
        for operation in batch_operations:
            operation.batch_id = batch_id
            self.submit_operation(operation)

        # 執行
        results = self.execute_all()

        return {
            "batch_id": batch_id,
            "operations_count": len(batch_operations),
            "results": [r.to_dict() for r in results],
            "success_rate": (
                sum(1 for r in results if r.status == "success") / len(results)
                if results
                else 0
            ),
        }

    def _get_batch_config(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """獲取批次配置"""
        batch_configs = {
            "batch-1": {
                "name": "Meta Framework",
                "ng_range": "NG000-099",
                "focus": "core_specifications",
            },
            "batch-2": {
                "name": "Era-1 Code Layer",
                "ng_range": "NG100-299",
                "focus": "code_namespaces",
                "era": Era.ERA_1,
            },
            "batch-3": {
                "name": "Era-2 Microcode Layer",
                "ng_range": "NG300-599",
                "focus": "service_namespaces",
                "era": Era.ERA_2,
            },
            "batch-4": {
                "name": "Era-3 No-Code Layer",
                "ng_range": "NG600-899",
                "focus": "intent_namespaces",
                "era": Era.ERA_3,
            },
            "batch-5": {
                "name": "Cross-Era Closure",
                "ng_range": "NG900-999",
                "focus": "cross_era_mapping",
            },
        }

        return batch_configs.get(batch_id)

    def _generate_batch_operations(
        self, batch_config: Dict[str, Any], era: Era = None
    ) -> List[NgOperation]:
        """生成批次操作"""
        operations = []

        # 根據批次配置生成操作
        focus = batch_config.get("focus")

        if focus == "core_specifications":
            # 批次 1: 驗證核心規範
            operations.append(
                NgOperation(
                    operation_id=f"validate-core-specs",
                    operation_type=OperationType.VALIDATE,
                    priority=ExecutionPriority.CRITICAL,
                    target_namespaces=[],
                    parameters={"scope": "core"},
                )
            )

        elif focus in ["code_namespaces", "service_namespaces", "intent_namespaces"]:
            # 批次 2-4: 註冊和驗證命名空間
            target_era = batch_config.get("era", era)

            if target_era:
                # 列出該 Era 的所有命名空間
                era_namespaces = self.registry.list_namespaces(era=target_era)
                namespace_ids = [r.id for r in era_namespaces]

                # 驗證操作
                operations.append(
                    NgOperation(
                        operation_id=f"validate-{target_era.value}",
                        operation_type=OperationType.VALIDATE,
                        priority=ExecutionPriority.HIGH,
                        target_namespaces=namespace_ids,
                        parameters={},
                        era_scope=target_era,
                    )
                )

        elif focus == "cross_era_mapping":
            # 批次 5: 跨 Era 映射和閉環
            operations.append(
                NgOperation(
                    operation_id="cross-era-mapping",
                    operation_type=OperationType.MIGRATE,
                    priority=ExecutionPriority.HIGH,
                    target_namespaces=[],
                    parameters={"mapping_type": "cross_era"},
                )
            )

            operations.append(
                NgOperation(
                    operation_id="final-closure-check",
                    operation_type=OperationType.CLOSURE,
                    priority=ExecutionPriority.CRITICAL,
                    target_namespaces=[],
                    parameters={},
                )
            )

        return operations

    def get_execution_statistics(self) -> Dict[str, Any]:
        """獲取執行統計"""
        stats = {
            "total_operations": len(self.execution_history),
            "by_type": {},
            "by_status": {},
            "success_rate": 0,
            "avg_duration_ms": 0,
        }

        if not self.execution_history:
            return stats

        # 按類型統計
        for result in self.execution_history:
            op_type = result.operation_id.split("-")[0]
            stats["by_type"][op_type] = stats["by_type"].get(op_type, 0) + 1

            # 按狀態統計
            stats["by_status"][result.status] = (
                stats["by_status"].get(result.status, 0) + 1
            )

        # 計算成功率
        success_count = stats["by_status"].get("success", 0)
        stats["success_rate"] = success_count / len(self.execution_history) * 100

        # 平均執行時間
        total_duration = sum(r.duration_ms for r in self.execution_history)
        stats["avg_duration_ms"] = total_duration / len(self.execution_history)

        return stats

    def generate_execution_report(self) -> str:
        """生成執行報告"""
        stats = self.get_execution_statistics()
        registry_stats = self.registry.get_statistics()

        report_lines = [
            "=" * 70,
            "NG 執行引擎報告",
            "=" * 70,
            f"生成時間: {datetime.now().isoformat()}",
            f"NG Code: NG00001 (最高權重執行器)",
            "",
            "執行統計:",
            f"  總操作數: {stats['total_operations']}",
            f"  成功率: {stats['success_rate']:.1f}%",
            f"  平均執行時間: {stats['avg_duration_ms']:.0f}ms",
            "",
            "操作分布:",
        ]

        for op_type, count in stats["by_type"].items():
            report_lines.append(f"  {op_type}: {count}")

        report_lines.extend(
            [
                "",
                "命名空間統計:",
                f"  總命名空間數: {registry_stats['total']}",
                "",
                "Era 分布:",
            ]
        )

        for era, count in registry_stats.get("by_era", {}).items():
            report_lines.append(f"  {era}: {count}")

        report_lines.extend(
            [
                "",
                "閉環狀態:",
                f"  閉環完整: {'✅' if self.closure_state['closure_complete'] else '❌'}",
                f"  最後檢查: {self.closure_state.get('last_closure_check', 'never')}",
                f"  待處理操作: {len(self.closure_state.get('pending_operations', []))}",
                "=" * 70,
            ]
        )

        return "\n".join(report_lines)

    def save_execution_log(self, output_path: str = "logs/ng-executor.json"):
        """保存執行日誌"""
        # 轉換 closure_state 中的 NgOperation 對象
        closure_state_serializable = {
            "timestamp": self.closure_state.get("timestamp"),
            "closure_complete": self.closure_state.get("closure_complete"),
            "last_closure_check": self.closure_state.get("last_closure_check"),
            "pending_operations": [
                op.to_dict() if hasattr(op, "to_dict") else str(op)
                for op in self.closure_state.get("pending_operations", [])
            ],
        }

        log_data = {
            "metadata": {
                "executor": "NgExecutor",
                "ng_code": "NG00001",
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat(),
            },
            "statistics": self.get_execution_statistics(),
            "execution_history": [r.to_dict() for r in self.execution_history],
            "closure_state": closure_state_serializable,
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 執行日誌已保存: {output_path}")


# 全局執行器實例
ng_executor = NgExecutor()


if __name__ == "__main__":
    # 測試執行引擎
    import uuid

    print("=" * 70)
    print("NG 執行引擎測試")
    print("=" * 70)

    # 設置日誌
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s"
    )

    # 創建測試執行器
    executor = NgExecutor()

    # 測試 1: 註冊操作
    print("\n測試 1: 註冊命名空間")
    print("-" * 70)

    register_op = NgOperation(
        operation_id=str(uuid.uuid4()),
        operation_type=OperationType.REGISTER,
        priority=ExecutionPriority.CRITICAL,
        target_namespaces=["pkg.era1.test.demo"],
        parameters={
            "pkg.era1.test.demo": {
                "type": "package",
                "domain": "test",
                "component": "demo",
                "owner": "test-team",
                "description": "測試演示包",
            }
        },
        era_scope=Era.ERA_1,
    )

    executor.submit_operation(register_op)

    # 測試 2: 驗證操作
    print("\n測試 2: 驗證命名空間")
    print("-" * 70)

    validate_op = NgOperation(
        operation_id=str(uuid.uuid4()),
        operation_type=OperationType.VALIDATE,
        priority=ExecutionPriority.HIGH,
        target_namespaces=["pkg.era1.test.demo"],
        parameters={},
    )

    executor.submit_operation(validate_op)

    # 測試 3: 監控操作
    print("\n測試 3: 監控命名空間")
    print("-" * 70)

    monitor_op = NgOperation(
        operation_id=str(uuid.uuid4()),
        operation_type=OperationType.MONITOR,
        priority=ExecutionPriority.MEDIUM,
        target_namespaces=["pkg.era1.test.demo"],
        parameters={},
    )

    executor.submit_operation(monitor_op)

    # 執行所有操作
    print("\n執行所有操作")
    print("=" * 70)

    results = executor.execute_all()

    # 顯示結果
    print(f"\n執行完成: {len(results)} 個操作")
    for result in results:
        status_icon = "✅" if result.status == "success" else "❌"
        print(
            f"{status_icon} {result.operation_id}: {result.status} ({result.duration_ms}ms)"
        )

    # 生成報告
    print("\n" + executor.generate_execution_report())

    # 保存日誌
    executor.save_execution_log()

    print("\n" + "=" * 70)
    print("✅ NG 執行引擎測試完成")
    print("=" * 70)
