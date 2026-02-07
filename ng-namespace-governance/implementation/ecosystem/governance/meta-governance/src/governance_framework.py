#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: governance
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Governance Framework
=======================
元治理框架 - 統一治理接口

GL Governance Layer: GL90-99 (Meta-Specification Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from typing import Dict, Optional, Any
import logging

from version_manager import VersionManager, VersionType
from change_manager import ChangeManager, ImpactLevel
from review_manager import ReviewManager, ReviewLayer
from dependency_manager import DependencyManager


class GovernanceFramework:
    """元治理框架"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化治理框架

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()

        # 初始化管理器
        self.version_manager = VersionManager(config)
        self.change_manager = ChangeManager(config)
        self.review_manager = ReviewManager(config)
        self.dependency_manager = DependencyManager(config)

        self.logger.info("Governance Framework initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("GovernanceFramework")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def propose_change(
        self,
        title: str,
        description: str,
        component: str,
        impact_level: str,
        submitter: str = "unknown",
    ) -> Dict[str, str]:
        """
        提出變更

        Args:
            title: 標題
            description: 描述
            component: 組件
            impact_level: 影響級別
            submitter: 提交者

        Returns:
            變更和審查ID
        """
        # 1. 提交變更請求
        change_id = self.change_manager.submit_change(
            title=title,
            description=description,
            impact_level=impact_level,
            affected_components=[component],
            submitter=submitter,
        )

        # 2. 評估變更
        assessment = self.change_manager.assess_change(change_id)

        # 3. 創建審查
        review_id = self.review_manager.create_review(change_id)

        self.logger.info(f"Change proposed: {change_id} (review: {review_id})")

        return {
            "change_id": change_id,
            "review_id": review_id,
            "risk_score": str(assessment.get("risk_score", 0)),
        }

    def release_version(
        self,
        component: str,
        version_type: str,
        changes: list,
        breaking_changes: Optional[list] = None,
    ) -> str:
        """
        發布版本

        Args:
            component: 組件名稱
            version_type: 版本類型
            changes: 變更列表
            breaking_changes: 破壞性變更列表

        Returns:
            版本字符串
        """
        # 創建版本
        metadata = self.version_manager.create_version(
            component=component,
            version_type=version_type,
            changes=changes,
            breaking_changes=breaking_changes,
        )

        # 驗證版本
        validation = self.version_manager.validate_version(metadata)

        if not validation["valid"]:
            self.logger.error(f"Version validation failed: {validation['errors']}")
            return ""

        version_str = str(metadata.version)

        self.logger.info(f"Version released: {component} v{version_str}")

        return version_str

    def get_governance_report(self) -> Dict[str, Any]:
        """
        生成治理報告

        Returns:
            治理報告
        """
        return {
            "version_management": self.version_manager.get_stats(),
            "change_management": self.change_manager.get_stats(),
            "review_management": self.review_manager.get_stats(),
            "dependency_management": self.dependency_manager.get_stats(),
        }
