#!/usr/bin/env python3
"""
GL Change Manager
=================
變更管理器 - 標準化變更流程

GL Governance Layer: GL90-99 (Meta-Specification Layer)
"""

import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging


class ImpactLevel(Enum):
    """影響級別"""
    LOW = "low"              # 低風險
    MEDIUM = "medium"        # 中風險
    HIGH = "high"            # 高風險
    CRITICAL = "critical"    # 關鍵風險


class ChangeStatus(Enum):
    """變更狀態"""
    PROPOSED = "proposed"              # 提案
    ASSESSING = "assessing"            # 評估中
    PENDING_REVIEW = "pending_review"  # 待審查
    APPROVED = "approved"              # 已批准
    IN_PROGRESS = "in_progress"        # 執行中
    TESTING = "testing"                # 測試中
    COMPLETED = "completed"            # 已完成
    REJECTED = "rejected"              # 已拒絕
    ROLLED_BACK = "rolled_back"        # 已回滾


@dataclass
class ChangeRequest:
    """變更請求"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    impact_level: ImpactLevel = ImpactLevel.MEDIUM
    affected_components: List[str] = field(default_factory=list)
    status: ChangeStatus = ChangeStatus.PROPOSED
    submitter: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # 評估
    risk_assessment: Optional[Dict[str, Any]] = None
    rollback_plan: Optional[str] = None
    performance_impact: Optional[str] = None
    
    # 審查
    reviewers: List[str] = field(default_factory=list)
    approvers: List[str] = field(default_factory=list)
    
    # 執行
    implementation_start: Optional[str] = None
    implementation_end: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None


class ChangeManager:
    """變更管理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化變更管理器"""
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 變更請求: {change_id: ChangeRequest}
        self._changes: Dict[str, ChangeRequest] = {}
        
        # 審批規則
        self._approval_rules = {
            ImpactLevel.LOW: ['team_lead'],
            ImpactLevel.MEDIUM: ['team_lead', 'tech_lead'],
            ImpactLevel.HIGH: ['team_lead', 'tech_lead', 'architect'],
            ImpactLevel.CRITICAL: ['team_lead', 'tech_lead', 'architect', 'cto']
        }
        
        self.logger.info("Change Manager initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('ChangeManager')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def submit_change(
        self,
        title: str,
        description: str,
        impact_level: str,
        affected_components: List[str],
        submitter: str = "unknown"
    ) -> str:
        """
        提交變更請求
        
        Args:
            title: 標題
            description: 描述
            impact_level: 影響級別
            affected_components: 受影響組件
            submitter: 提交者
            
        Returns:
            變更ID
        """
        change = ChangeRequest(
            title=title,
            description=description,
            impact_level=ImpactLevel(impact_level),
            affected_components=affected_components,
            submitter=submitter
        )
        
        # 根據影響級別設置審查者
        change.reviewers = self._approval_rules.get(
            change.impact_level,
            ['team_lead']
        )
        
        self._changes[change.id] = change
        
        self.logger.info(
            f"Change request submitted: {change.id} - {title} "
            f"(impact: {impact_level})"
        )
        
        return change.id
    
    def assess_change(self, change_id: str) -> Dict[str, Any]:
        """
        評估變更
        
        Args:
            change_id: 變更ID
            
        Returns:
            評估結果
        """
        change = self._changes.get(change_id)
        if not change:
            return {'error': 'Change not found'}
        
        # 更新狀態
        change.status = ChangeStatus.ASSESSING
        
        # 自動風險評估
        risk_score = self._calculate_risk_score(change)
        
        assessment = {
            'change_id': change_id,
            'impact_level': change.impact_level.value,
            'affected_components': change.affected_components,
            'risk_score': risk_score,
            'required_approvers': change.reviewers,
            'recommendations': self._generate_recommendations(change)
        }
        
        change.risk_assessment = assessment
        change.status = ChangeStatus.PENDING_REVIEW
        change.updated_at = datetime.utcnow().isoformat()
        
        self.logger.info(f"Change assessed: {change_id} (risk: {risk_score})")
        
        return assessment
    
    def _calculate_risk_score(self, change: ChangeRequest) -> float:
        """
        計算風險分數（0-100）
        
        Args:
            change: 變更請求
            
        Returns:
            風險分數
        """
        score = 0.0
        
        # 基於影響級別
        impact_scores = {
            ImpactLevel.LOW: 10,
            ImpactLevel.MEDIUM: 30,
            ImpactLevel.HIGH: 60,
            ImpactLevel.CRITICAL: 90
        }
        score += impact_scores.get(change.impact_level, 0)
        
        # 基於受影響組件數量
        score += min(len(change.affected_components) * 5, 10)
        
        return min(score, 100)
    
    def _generate_recommendations(self, change: ChangeRequest) -> List[str]:
        """生成建議"""
        recommendations = []
        
        if change.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]:
            recommendations.append("需要提供詳細的回滾方案")
            recommendations.append("需要進行性能基準測試")
            recommendations.append("建議通過影子發布（Shadow Deployment）驗證")
        
        if len(change.affected_components) > 3:
            recommendations.append("變更影響多個組件，建議分階段實施")
        
        if not change.rollback_plan:
            recommendations.append("請添加回滾方案")
        
        return recommendations
    
    def approve_change(
        self,
        change_id: str,
        approver: str,
        comments: Optional[str] = None
    ) -> bool:
        """
        批准變更
        
        Args:
            change_id: 變更ID
            approver: 批准者
            comments: 評論
            
        Returns:
            成功返回True
        """
        change = self._changes.get(change_id)
        if not change:
            return False
        
        # 記錄批准
        if approver not in change.approvers:
            change.approvers.append(approver)
        
        # 檢查是否所有必需的批准者都已批准
        required = set(change.reviewers)
        approved = set(change.approvers)
        
        if required.issubset(approved):
            change.status = ChangeStatus.APPROVED
            self.logger.info(f"Change fully approved: {change_id}")
        
        change.updated_at = datetime.utcnow().isoformat()
        
        return True
    
    def execute_change(self, change_id: str) -> bool:
        """
        執行變更
        
        Args:
            change_id: 變更ID
            
        Returns:
            成功返回True
        """
        change = self._changes.get(change_id)
        if not change:
            return False
        
        if change.status != ChangeStatus.APPROVED:
            self.logger.error(f"Change not approved: {change_id}")
            return False
        
        change.status = ChangeStatus.IN_PROGRESS
        change.implementation_start = datetime.utcnow().isoformat()
        change.updated_at = datetime.utcnow().isoformat()
        
        self.logger.info(f"Change execution started: {change_id}")
        
        return True
    
    def complete_change(
        self,
        change_id: str,
        test_results: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        完成變更
        
        Args:
            change_id: 變更ID
            test_results: 測試結果
            
        Returns:
            成功返回True
        """
        change = self._changes.get(change_id)
        if not change:
            return False
        
        change.status = ChangeStatus.COMPLETED
        change.implementation_end = datetime.utcnow().isoformat()
        change.test_results = test_results
        change.updated_at = datetime.utcnow().isoformat()
        
        self.logger.info(f"Change completed: {change_id}")
        
        return True
    
    def get_change(self, change_id: str) -> Optional[ChangeRequest]:
        """獲取變更請求"""
        return self._changes.get(change_id)
    
    def list_changes(
        self,
        status: Optional[str] = None,
        impact_level: Optional[str] = None
    ) -> List[ChangeRequest]:
        """列出變更請求"""
        changes = list(self._changes.values())
        
        if status:
            changes = [c for c in changes if c.status == ChangeStatus(status)]
        
        if impact_level:
            changes = [c for c in changes if c.impact_level == ImpactLevel(impact_level)]
        
        return sorted(changes, key=lambda c: c.created_at, reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        by_status = {}
        by_impact = {}
        
        for change in self._changes.values():
            status = change.status.value
            impact = change.impact_level.value
            
            by_status[status] = by_status.get(status, 0) + 1
            by_impact[impact] = by_impact.get(impact, 0) + 1
        
        return {
            'total_changes': len(self._changes),
            'by_status': by_status,
            'by_impact': by_impact
        }
