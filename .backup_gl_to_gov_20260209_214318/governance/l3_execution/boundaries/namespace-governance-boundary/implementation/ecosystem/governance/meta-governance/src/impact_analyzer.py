#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: impact-analysis
# @GL-audit-trail: ../../GL_SEMANTIC_ANCHOR.json
#
"""
Impact Analyzer
===============
影響分析器 - 版本變更影響評估

智能分析版本變更對下游的影響鏈路
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging


@dataclass
class ImpactChain:
    """影響鏈"""

    spec_id: str
    from_version: str
    to_version: str
    change_type: str  # MAJOR, MINOR, PATCH
    affected_validators: List[str] = field(default_factory=list)
    downstream_impacts: List["ImpactChain"] = field(default_factory=list)
    migration_cost: float = 0.0  # 0-100
    risk_score: float = 0.0  # 0-100


@dataclass
class MigrationPlan:
    """遷移計劃"""

    target_version: str
    upgrade_sequence: List[str]
    estimated_effort_days: int
    risk_level: str
    critical_path: List[str]
    rollback_plan: str
    testing_requirements: List[str]


class ImpactAnalyzer:
    """影響分析器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = self._setup_logger()

        # 依賴圖: {validator_id: [spec_ids]}
        self.dependency_graph: Dict[str, List[str]] = {}

        # 驗證器註冊: {validator_id: {spec_dependencies}}
        self._validators: Dict[str, Dict] = {}

        self.logger.info("Impact Analyzer initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("ImpactAnalyzer")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def register_validator(self, validator_id: str, spec_dependencies: List[Dict]):
        """
        註冊驗證器及其依賴

        Args:
            validator_id: 驗證器ID
            spec_dependencies: 規範依賴列表
        """
        self._validators[validator_id] = {"dependencies": spec_dependencies}

        # 更新依賴圖（簡化實現）
        self.dependency_graph[validator_id] = [
            dep["spec_id"] for dep in spec_dependencies
        ]

    def analyze_version_change_impact(
        self, spec_id: str, from_version: str, to_version: str
    ) -> ImpactChain:
        """
        分析版本變更影響

        Args:
            spec_id: 規範ID
            from_version: 當前版本
            to_version: 目標版本

        Returns:
            影響鏈分析結果
        """
        # 確定變更類型
        change_type = self._determine_change_type(from_version, to_version)

        # 找到所有受影響的驗證器
        affected_validators = self._find_affected_validators(spec_id)

        # 分析下游影響
        downstream_impacts = []
        for validator_id in affected_validators:
            downstream = self._analyze_downstream_impact(
                validator_id, spec_id, to_version, depth=1
            )
            if downstream:
                downstream_impacts.extend(downstream)

        # 計算遷移成本
        migration_cost = self._calculate_migration_cost(
            change_type, len(affected_validators), len(downstream_impacts)
        )

        # 計算風險分數
        risk_score = self._calculate_risk_score(
            change_type, affected_validators, downstream_impacts
        )

        impact_chain = ImpactChain(
            spec_id=spec_id,
            from_version=from_version,
            to_version=to_version,
            change_type=change_type,
            affected_validators=affected_validators,
            downstream_impacts=downstream_impacts,
            migration_cost=migration_cost,
            risk_score=risk_score,
        )

        self.logger.info(
            f"影響分析完成: {spec_id} {from_version}→{to_version}\n"
            f"  變更類型: {change_type}\n"
            f"  直接影響: {len(affected_validators)} 驗證器\n"
            f"  下游影響: {len(downstream_impacts)} 組件\n"
            f"  遷移成本: {migration_cost:.1f}/100\n"
            f"  風險分數: {risk_score:.1f}/100"
        )

        return impact_chain

    def generate_migration_plan(
        self, spec_id: str, current_version: str, target_version: str
    ) -> MigrationPlan:
        """
        生成遷移計劃

        Args:
            spec_id: 規範ID
            current_version: 當前版本
            target_version: 目標版本

        Returns:
            遷移計劃
        """
        # 計算升級序列
        upgrade_sequence = self._calculate_upgrade_sequence(
            current_version, target_version
        )

        # 分析影響鏈
        impact = self.analyze_version_change_impact(
            spec_id, current_version, target_version
        )

        # 估算工作量
        effort_days = self._estimate_migration_effort(impact)

        # 確定風險級別
        risk_level = self._determine_risk_level(impact.risk_score)

        # 找出關鍵路徑
        critical_path = self._find_critical_path(impact)

        # 生成回滾計劃
        rollback_plan = self._generate_rollback_plan(
            spec_id, current_version, target_version
        )

        # 確定測試需求
        testing_requirements = self._determine_testing_requirements(impact.change_type)

        plan = MigrationPlan(
            target_version=target_version,
            upgrade_sequence=upgrade_sequence,
            estimated_effort_days=effort_days,
            risk_level=risk_level,
            critical_path=critical_path,
            rollback_plan=rollback_plan,
            testing_requirements=testing_requirements,
        )

        self.logger.info(
            f"遷移計劃已生成: {spec_id} → v{target_version}\n"
            f"  升級序列: {' → '.join(upgrade_sequence)}\n"
            f"  預估工作量: {effort_days} 天\n"
            f"  風險級別: {risk_level}"
        )

        return plan

    def _determine_change_type(self, from_version: str, to_version: str) -> str:
        """確定變更類型"""
        from_tuple = self._version_to_tuple(from_version)
        to_tuple = self._version_to_tuple(to_version)

        if to_tuple[0] > from_tuple[0]:
            return "MAJOR"
        elif to_tuple[1] > from_tuple[1]:
            return "MINOR"
        else:
            return "PATCH"

    def _find_affected_validators(self, spec_id: str) -> List[str]:
        """找到所有依賴此規範的驗證器"""
        affected = []

        for validator_id, validator_data in self._validators.items():
            for dep in validator_data["dependencies"]:
                if dep["spec_id"] == spec_id:
                    affected.append(validator_id)
                    break

        return affected

    def _analyze_downstream_impact(
        self,
        validator_id: str,
        spec_id: str,
        new_version: str,
        depth: int,
        max_depth: int = 3,
    ) -> List[ImpactChain]:
        """遞歸分析下游影響"""
        if depth > max_depth:
            return []

        impacts = []

        # 檢查此驗證器是否有下游依賴
        # （簡化實現：實際需要查詢驗證器間的依賴關係）

        return impacts

    def _calculate_migration_cost(
        self, change_type: str, direct_affected: int, downstream_affected: int
    ) -> float:
        """計算遷移成本（0-100）"""
        base_cost = {"MAJOR": 60, "MINOR": 20, "PATCH": 5}.get(change_type, 0)

        # 基於影響範圍調整
        impact_cost = direct_affected * 5 + downstream_affected * 2

        return min(100.0, base_cost + impact_cost)

    def _calculate_risk_score(
        self, change_type: str, affected_validators: List[str], downstream_impacts: List
    ) -> float:
        """計算風險分數（0-100）"""
        base_risk = {"MAJOR": 80, "MINOR": 30, "PATCH": 10}.get(change_type, 0)

        # 基於影響範圍調整
        scope_risk = len(affected_validators) * 3
        downstream_risk = len(downstream_impacts) * 2

        return min(100.0, base_risk + scope_risk + downstream_risk)

    def _calculate_upgrade_sequence(self, current: str, target: str) -> List[str]:
        """計算升級序列（無跳躍）"""
        current_tuple = self._version_to_tuple(current)
        target_tuple = self._version_to_tuple(target)

        sequence = [current]

        # 主版本升級
        for major in range(current_tuple[0], target_tuple[0]):
            # 遞進到下一個主版本的 X.0.0
            next_major = f"{major + 1}.0.0"
            if next_major not in sequence:
                sequence.append(next_major)

        # 次版本升級
        start_minor = 0 if target_tuple[0] > current_tuple[0] else current_tuple[1]
        for minor in range(start_minor, target_tuple[1]):
            next_minor = f"{target_tuple[0]}.{minor + 1}.0"
            if next_minor not in sequence:
                sequence.append(next_minor)

        # 修訂版本升級
        if str(target_tuple[0]) + "." + str(target_tuple[1]) in sequence[-1]:
            start_patch = int(sequence[-1].split(".")[-1])
        else:
            start_patch = 0

        for patch in range(start_patch, target_tuple[2]):
            next_patch = f"{target_tuple[0]}.{target_tuple[1]}.{patch + 1}"
            if next_patch not in sequence:
                sequence.append(next_patch)

        # 確保目標版本在序列中
        if target not in sequence:
            sequence.append(target)

        return sequence[1:]  # 移除當前版本

    def _estimate_migration_effort(self, impact: ImpactChain) -> int:
        """估算遷移工作量（天數）"""
        base_effort = {"MAJOR": 30, "MINOR": 7, "PATCH": 1}.get(impact.change_type, 1)

        # 基於影響範圍調整
        scope_factor = len(impact.affected_validators) * 0.5
        downstream_factor = len(impact.downstream_impacts) * 0.3

        return int(base_effort + scope_factor + downstream_factor)

    def _determine_risk_level(self, risk_score: float) -> str:
        """確定風險級別"""
        if risk_score >= 75:
            return "CRITICAL"
        elif risk_score >= 50:
            return "HIGH"
        elif risk_score >= 25:
            return "MEDIUM"
        else:
            return "LOW"

    def _find_critical_path(self, impact: ImpactChain) -> List[str]:
        """找出關鍵路徑"""
        # 簡化實現：返回主要受影響組件
        return impact.affected_validators[:5]

    def _generate_rollback_plan(
        self, spec_id: str, current_version: str, target_version: str
    ) -> str:
        """生成回滾計劃"""
        return f"""
回滾計劃 - {spec_id}

當前版本: {current_version}
目標版本: {target_version}

回滾步驟:
1. 停止所有使用 v{target_version} 的驗證器
2. 恢復配置到 v{current_version}
3. 重啟服務並驗證健康狀態
4. 執行煙霧測試
5. 監控24小時確保穩定

預計回滾時間: 2小時
需要審批: 技術負責人
"""

    def _determine_testing_requirements(self, change_type: str) -> List[str]:
        """確定測試需求"""
        requirements = {
            "MAJOR": [
                "完整回歸測試套件",
                "兼容性矩陣測試",
                "性能基準測試",
                "安全掃描",
                "遷移路徑測試",
                "回滾流程測試",
            ],
            "MINOR": ["功能測試", "集成測試", "兼容性測試", "性能影響測試"],
            "PATCH": ["單元測試", "回歸測試", "語意驗證"],
        }

        return requirements.get(change_type, ["基礎測試"])

    def _version_to_tuple(self, version: str) -> Tuple[int, int, int]:
        """版本轉元組"""
        parts = version.split("-")[0].split(".")
        return (int(parts[0]), int(parts[1]), int(parts[2]))
