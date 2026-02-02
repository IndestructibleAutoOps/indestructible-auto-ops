#!/usr/bin/env python3
"""
GL Review Manager
=================
審查管理器 - 三層審查機制

GL Governance Layer: GL90-99 (Meta-Specification Layer)
"""

import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging


class ReviewLayer(Enum):
    """審查層級"""
    TECHNICAL = "technical"      # 技術合規
    ARCHITECTURE = "architecture"  # 架構設計
    BUSINESS = "business"          # 業務驗證


class ReviewDecision(Enum):
    """審查決定"""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CHANGES = "needs_changes"
    PENDING = "pending"


@dataclass
class ReviewComment:
    """審查意見"""
    reviewer: str
    layer: ReviewLayer
    decision: ReviewDecision
    comments: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    suggestions: List[str] = field(default_factory=list)


@dataclass
class Review:
    """審查"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    change_id: str = ""
    required_layers: List[ReviewLayer] = field(default_factory=list)
    reviewers: Dict[ReviewLayer, List[str]] = field(default_factory=dict)
    comments: List[ReviewComment] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed: bool = False


class ReviewManager:
    """審查管理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化審查管理器"""
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 審查: {review_id: Review}
        self._reviews: Dict[str, Review] = {}
        
        # 審查者配置
        self._reviewers_config = {
            ReviewLayer.TECHNICAL: ['dev-team', 'qa-team'],
            ReviewLayer.ARCHITECTURE: ['architect', 'tech-lead'],
            ReviewLayer.BUSINESS: ['product-owner', 'domain-expert']
        }
        
        self.logger.info("Review Manager initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('ReviewManager')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def create_review(
        self,
        change_id: str,
        reviewers: Optional[List[str]] = None,
        required_layers: Optional[List[str]] = None
    ) -> str:
        """
        創建審查
        
        Args:
            change_id: 變更ID
            reviewers: 審查者列表
            required_layers: 必需的審查層級
            
        Returns:
            審查ID
        """
        # 確定審查層級
        layers = []
        if required_layers:
            layers = [ReviewLayer(layer) for layer in required_layers]
        else:
            # 默認所有層級
            layers = list(ReviewLayer)
        
        # 創建審查
        review = Review(
            change_id=change_id,
            required_layers=layers
        )
        
        # 設置審查者
        for layer in layers:
            review.reviewers[layer] = self._reviewers_config.get(layer, [])
        
        self._reviews[review.id] = review
        
        self.logger.info(
            f"Review created: {review.id} for change {change_id} "
            f"({len(layers)} layers)"
        )
        
        return review.id
    
    def submit_review(
        self,
        review_id: str,
        reviewer: str,
        layer: str,
        decision: str,
        comments: str = "",
        suggestions: Optional[List[str]] = None
    ) -> bool:
        """
        提交審查意見
        
        Args:
            review_id: 審查ID
            reviewer: 審查者
            layer: 審查層級
            decision: 決定
            comments: 評論
            suggestions: 建議
            
        Returns:
            成功返回True
        """
        review = self._reviews.get(review_id)
        if not review:
            return False
        
        # 創建審查意見
        comment = ReviewComment(
            reviewer=reviewer,
            layer=ReviewLayer(layer),
            decision=ReviewDecision(decision),
            comments=comments,
            suggestions=suggestions or []
        )
        
        review.comments.append(comment)
        
        # 檢查是否所有層級都已審查
        self._check_review_completion(review)
        
        self.logger.info(
            f"Review submitted: {review_id} by {reviewer} "
            f"({layer}: {decision})"
        )
        
        return True
    
    def _check_review_completion(self, review: Review):
        """檢查審查是否完成"""
        # 統計每層的審查決定
        layer_decisions = {layer: [] for layer in review.required_layers}
        
        for comment in review.comments:
            if comment.layer in layer_decisions:
                layer_decisions[comment.layer].append(comment.decision)
        
        # 檢查每層是否有批准
        all_approved = True
        for layer, decisions in layer_decisions.items():
            if not decisions or ReviewDecision.REJECTED in decisions:
                all_approved = False
                break
            if ReviewDecision.APPROVED not in decisions:
                all_approved = False
                break
        
        review.completed = all_approved
    
    def get_review_status(self, review_id: str) -> Optional[Dict[str, Any]]:
        """
        獲取審查狀態
        
        Args:
            review_id: 審查ID
            
        Returns:
            審查狀態或None
        """
        review = self._reviews.get(review_id)
        if not review:
            return None
        
        # 統計每層的狀態
        layer_status = {}
        for layer in review.required_layers:
            layer_comments = [c for c in review.comments if c.layer == layer]
            
            if not layer_comments:
                layer_status[layer.value] = 'pending'
            else:
                decisions = [c.decision for c in layer_comments]
                if ReviewDecision.APPROVED in decisions:
                    layer_status[layer.value] = 'approved'
                elif ReviewDecision.REJECTED in decisions:
                    layer_status[layer.value] = 'rejected'
                else:
                    layer_status[layer.value] = 'needs_changes'
        
        return {
            'review_id': review.id,
            'change_id': review.change_id,
            'completed': review.completed,
            'layer_status': layer_status,
            'total_comments': len(review.comments),
            'required_layers': [layer.value for layer in review.required_layers]
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        total = len(self._reviews)
        completed = sum(1 for r in self._reviews.values() if r.completed)
        
        return {
            'total_reviews': total,
            'completed': completed,
            'pending': total - completed
        }
