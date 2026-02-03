#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: change-control
# @GL-audit-trail: ../../GL_SEMANTIC_ANCHOR.json
#
"""
Strict Change Control System
=============================
嚴格變更控制系統 - 五階段變更流程

階段: Proposal → Review → Approval → Release → Notification
標準: Aviation Airworthiness-Grade
"""

import hashlib
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging


class ChangeCategory(Enum):
    """變更類別"""
    EMERGENCY_SECURITY = "category-1"  # 緊急安全修復
    BREAKING_CHANGE = "category-2"     # 破壞性變更
    FEATURE_ENHANCEMENT = "category-3"  # 功能增強
    BUG_FIX = "category-4"             # 錯誤修正


class ChangeStatus(Enum):
    """變更狀態"""
    DRAFT = "draft"
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    REVIEWED = "reviewed"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    RELEASED = "released"
    DEPRECATED = "deprecated"


class UrgencyLevel(Enum):
    """緊急級別"""
    EMERGENCY = "emergency"  # 24小時
    HIGH = "high"            # 3天
    NORMAL = "normal"        # 14天
    LOW = "low"              # 30天


@dataclass
class ChangeProposal:
    """變更提案"""
    proposal_id: str
    spec_id: str
    current_version: str
    proposed_version: str
    change_category: ChangeCategory
    urgency_level: UrgencyLevel
    title: str
    abstract: str
    rationale: Dict[str, List[str]]
    detailed_changes: List[Dict]
    impact_analysis: Dict
    risk_assessment: Dict
    test_plan: Dict
    proposer_id: str
    proposer_role: str
    migration_plan: Optional[Dict] = None
    dependencies: Dict = field(default_factory=dict)
    submitted_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: ChangeStatus = ChangeStatus.DRAFT
    review_assignments: List[str] = field(default_factory=list)
    approval_record: Optional[Dict] = None
    audit_hash: Optional[str] = None


@dataclass
class ReviewDecision:
    """審查決定"""
    reviewer_id: str
    proposal_id: str
    decision: str  # approve, reject, needs_revision
    score: Dict[str, int]  # 各維度評分（1-5）
    comments: List[Dict]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ApprovalRecord:
    """批准記錄"""
    record_id: str
    proposal_id: str
    spec_id: str
    from_version: str
    to_version: str
    approval_level: str
    required_approvers: List[str]
    actual_approvers: List[Dict]
    approval_status: str  # approved, rejected, timed_out
    approval_timestamp: str
    audit_hash: str
    blockchain_tx_id: Optional[str] = None


class ChangeControlSystem:
    """變更控制系統"""
    
    # 角色權限矩陣
    ROLE_PERMISSIONS = {
        'governance-core': {
            'allowed_categories': ['category-1', 'category-2', 'category-3', 'category-4'],
            'quota_monthly': float('inf'),
            'cooldown_days': 0
        },
        'spec-owner': {
            'allowed_categories': ['category-3', 'category-4'],
            'quota_monthly': 3,
            'cooldown_days': 7
        },
        'validator-owner': {
            'allowed_categories': ['category-4'],
            'quota_monthly': 1,
            'cooldown_days': 30
        },
        'security-team': {
            'allowed_categories': ['category-1', 'category-4'],
            'quota_monthly': float('inf'),
            'cooldown_days': 0
        }
    }
    
    # 批准要求
    APPROVAL_REQUIREMENTS = {
        'category-1': {  # 緊急安全
            'approvers': ['emergency-response-team'],
            'quorum': '2-of-3',
            'voting_days': 1,
            'post_review_required': True
        },
        'category-2': {  # 重大變更
            'approvers': ['governance-committee', 'security-lead', 'operations-lead'],
            'quorum': '3-of-3',
            'voting_days': 7,
            'post_review_required': False
        },
        'category-3': {  # 功能增強
            'approvers': ['governance-core', 'spec-owner'],
            'quorum': '2-of-2',
            'voting_days': 5,
            'post_review_required': False
        },
        'category-4': {  # 錯誤修正
            'approvers': ['spec-owner', '1-reviewer'],
            'quorum': '2-of-2',
            'voting_days': 3,
            'post_review_required': False
        }
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 提案存儲: {proposal_id: ChangeProposal}
        self._proposals: Dict[str, ChangeProposal] = {}
        
        # 審查記錄: {proposal_id: [ReviewDecision]}
        self._reviews: Dict[str, List[ReviewDecision]] = {}
        
        # 批准記錄: {proposal_id: ApprovalRecord}
        self._approvals: Dict[str, ApprovalRecord] = {}
        
        # 審計追蹤（不可變）
        self._audit_trail: List[Dict] = []
        
        self.logger.info("Change Control System initialized (Airworthiness-Grade)")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('ChangeControlSystem')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    # ========================================================================
    # 階段 1: 提案 (Proposal)
    # ========================================================================
    
    def submit_proposal(self, proposal: ChangeProposal) -> Tuple[bool, List[str]]:
        """
        提交變更提案
        
        Args:
            proposal: 變更提案
            
        Returns:
            (成功, 錯誤列表)
        """
        errors = []
        
        # 驗證提案者資格
        if not self._validate_proposer_eligibility(proposal):
            errors.append("提案者不具備提交此類變更的資格")
        
        # 驗證配額
        if not self._check_proposal_quota(proposal.proposer_id, proposal.proposer_role):
            errors.append("提案者已超過月度配額限制")
        
        # 驗證冷卻期
        if not self._check_cooldown_period(proposal.proposer_id):
            errors.append("提案者在冷卻期內，暫時無法提交新提案")
        
        # 驗證版本號正確性
        if not self._validate_version_number(proposal):
            errors.append("版本號與變更類別不匹配")
        
        # 驗證提案完整性
        completeness_errors = self._validate_proposal_completeness(proposal)
        errors.extend(completeness_errors)
        
        if errors:
            self.logger.error(f"提案驗證失敗: {proposal.proposal_id}\n{errors}")
            return False, errors
        
        # 註冊提案
        self._proposals[proposal.proposal_id] = proposal
        proposal.status = ChangeStatus.PROPOSED
        
        # 記錄審計
        self._record_audit_event({
            'event': 'proposal_submitted',
            'proposal_id': proposal.proposal_id,
            'proposer': proposal.proposer_id,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.logger.info(
            f"提案已提交: {proposal.proposal_id}\n"
            f"  規範: {proposal.spec_id}\n"
            f"  版本: {proposal.current_version} → {proposal.proposed_version}\n"
            f"  類別: {proposal.change_category.value}"
        )
        
        return True, []
    
    def _validate_proposer_eligibility(self, proposal: ChangeProposal) -> bool:
        """驗證提案者資格"""
        role_perms = self.ROLE_PERMISSIONS.get(proposal.proposer_role, {})
        allowed_categories = role_perms.get('allowed_categories', [])
        
        return proposal.change_category.value in allowed_categories
    
    def _check_proposal_quota(self, proposer_id: str, role: str) -> bool:
        """檢查提案配額"""
        role_perms = self.ROLE_PERMISSIONS.get(role, {})
        monthly_quota = role_perms.get('quota_monthly', 0)
        
        # 統計本月提案數
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        month_proposals = sum(
            1 for p in self._proposals.values()
            if p.proposer_id == proposer_id and 
            datetime.fromisoformat(p.submitted_at) >= month_start
        )
        
        return month_proposals < monthly_quota
    
    def _check_cooldown_period(self, proposer_id: str) -> bool:
        """檢查冷卻期"""
        # 獲取最後一個提案
        proposer_proposals = [
            p for p in self._proposals.values()
            if p.proposer_id == proposer_id
        ]
        
        if not proposer_proposals:
            return True
        
        # 按時間排序
        latest = max(proposer_proposals, key=lambda p: p.submitted_at)
        
        # 獲取冷卻期（根據角色）
        # 簡化實現：使用固定7天
        cooldown_days = 7
        
        days_since = (datetime.utcnow() - datetime.fromisoformat(latest.submitted_at)).days
        
        return days_since >= cooldown_days
    
    def _validate_version_number(self, proposal: ChangeProposal) -> bool:
        """驗證版本號與類別匹配"""
        current = tuple(map(int, proposal.current_version.split('.')))
        proposed = tuple(map(int, proposal.proposed_version.split('.')))
        
        category = proposal.change_category
        
        # Category-2: MAJOR 變更
        if category == ChangeCategory.BREAKING_CHANGE:
            return (proposed[0] > current[0] and 
                   proposed[1] == 0 and 
                   proposed[2] == 0)
        
        # Category-3: MINOR 變更
        elif category == ChangeCategory.FEATURE_ENHANCEMENT:
            return (proposed[0] == current[0] and 
                   proposed[1] > current[1] and 
                   proposed[2] == 0)
        
        # Category-4: PATCH 變更
        elif category == ChangeCategory.BUG_FIX:
            return (proposed[0] == current[0] and 
                   proposed[1] == current[1] and 
                   proposed[2] > current[2])
        
        return True
    
    def _validate_proposal_completeness(self, proposal: ChangeProposal) -> List[str]:
        """驗證提案完整性"""
        errors = []
        
        # 檢查必要字段
        if not proposal.title:
            errors.append("缺少標題")
        
        if not proposal.abstract:
            errors.append("缺少摘要")
        
        if not proposal.rationale:
            errors.append("缺少變更理由")
        
        if not proposal.impact_analysis:
            errors.append("缺少影響分析")
        
        if not proposal.risk_assessment:
            errors.append("缺少風險評估")
        
        if not proposal.test_plan:
            errors.append("缺少測試計劃")
        
        # 重大變更需要遷移計劃
        if proposal.change_category in [ChangeCategory.BREAKING_CHANGE, ChangeCategory.EMERGENCY_SECURITY]:
            if not proposal.migration_plan:
                errors.append("重大變更必須包含遷移計劃")
        
        return errors
    
    # ========================================================================
    # 階段 2: 審查 (Review)
    # ========================================================================
    
    def assign_reviewers(
        self,
        proposal_id: str,
        auto_assign: bool = True
    ) -> List[str]:
        """
        分配審查者
        
        Args:
            proposal_id: 提案ID
            auto_assign: 是否自動分配
            
        Returns:
            審查者ID列表
        """
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            return []
        
        # 根據變更類別確定需要的審查者數量和專業
        if auto_assign:
            reviewers = self._auto_assign_reviewers(proposal)
        else:
            reviewers = []
        
        proposal.review_assignments = reviewers
        proposal.status = ChangeStatus.UNDER_REVIEW
        
        # 記錄審計
        self._record_audit_event({
            'event': 'reviewers_assigned',
            'proposal_id': proposal_id,
            'reviewers': reviewers,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.logger.info(
            f"審查者已分配: {proposal_id}\n"
            f"  審查者: {', '.join(reviewers)}"
        )
        
        return reviewers
    
    def _auto_assign_reviewers(self, proposal: ChangeProposal) -> List[str]:
        """自動分配審查者"""
        # 簡化實現：根據類別選擇固定審查者
        reviewers = ['reviewer-001', 'reviewer-002']  # 至少2名
        
        # 安全相關需要安全專家
        if proposal.change_category in [ChangeCategory.EMERGENCY_SECURITY, ChangeCategory.BREAKING_CHANGE]:
            reviewers.append('security-reviewer')
        
        return reviewers
    
    def submit_review(
        self,
        proposal_id: str,
        review: ReviewDecision
    ) -> bool:
        """
        提交審查意見
        
        Args:
            proposal_id: 提案ID
            review: 審查決定
            
        Returns:
            成功返回True
        """
        if proposal_id not in self._reviews:
            self._reviews[proposal_id] = []
        
        self._reviews[proposal_id].append(review)
        
        # 記錄審計
        self._record_audit_event({
            'event': 'review_submitted',
            'proposal_id': proposal_id,
            'reviewer': review.reviewer_id,
            'decision': review.decision,
            'timestamp': review.timestamp
        })
        
        # 檢查是否所有審查者都已提交
        proposal = self._proposals[proposal_id]
        if len(self._reviews[proposal_id]) >= len(proposal.review_assignments):
            # 計算總體評分
            self._finalize_review(proposal_id)
        
        self.logger.info(
            f"審查已提交: {proposal_id} by {review.reviewer_id}\n"
            f"  決定: {review.decision}"
        )
        
        return True
    
    def _finalize_review(self, proposal_id: str):
        """完成審查階段"""
        reviews = self._reviews.get(proposal_id, [])
        
        # 計算總體分數
        total_scores = {}
        for review in reviews:
            for criterion, score in review.score.items():
                if criterion not in total_scores:
                    total_scores[criterion] = []
                total_scores[criterion].append(score)
        
        avg_scores = {
            criterion: sum(scores) / len(scores)
            for criterion, scores in total_scores.items()
        }
        
        overall_avg = sum(avg_scores.values()) / len(avg_scores) if avg_scores else 0
        
        # 確定審查結果
        if overall_avg >= 4.0 and all(s >= 3.0 for s in avg_scores.values()):
            decision = 'pass'
        elif overall_avg >= 3.5:
            decision = 'conditional_pass'
        else:
            decision = 'reject'
        
        # 更新提案狀態
        proposal = self._proposals[proposal_id]
        if decision == 'pass':
            proposal.status = ChangeStatus.REVIEWED
        elif decision == 'reject':
            proposal.status = ChangeStatus.REJECTED
        
        self.logger.info(
            f"審查完成: {proposal_id}\n"
            f"  總體分數: {overall_avg:.2f}/5.0\n"
            f"  決定: {decision}"
        )
    
    # ========================================================================
    # 階段 3: 批准 (Approval)
    # ========================================================================
    
    def request_approval(self, proposal_id: str) -> str:
        """
        請求批准
        
        Args:
            proposal_id: 提案ID
            
        Returns:
            批准請求ID
        """
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            return ""
        
        if proposal.status != ChangeStatus.REVIEWED:
            self.logger.error(f"提案未通過審查，無法請求批准: {proposal_id}")
            return ""
        
        # 確定批准級別
        category = proposal.change_category.value
        requirements = self.APPROVAL_REQUIREMENTS.get(category, {})
        
        # 創建批准記錄
        record = ApprovalRecord(
            record_id=f"APPROVAL-{proposal_id}",
            proposal_id=proposal_id,
            spec_id=proposal.spec_id,
            from_version=proposal.current_version,
            to_version=proposal.proposed_version,
            approval_level=category,
            required_approvers=requirements.get('approvers', []),
            actual_approvers=[],
            approval_status='pending',
            approval_timestamp="",
            audit_hash=""
        )
        
        self._approvals[proposal_id] = record
        proposal.status = ChangeStatus.PENDING_APPROVAL
        
        # 記錄審計
        self._record_audit_event({
            'event': 'approval_requested',
            'proposal_id': proposal_id,
            'approval_level': category,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.logger.info(
            f"批准已請求: {proposal_id}\n"
            f"  批准級別: {category}\n"
            f"  需要批准者: {', '.join(requirements.get('approvers', []))}"
        )
        
        return record.record_id
    
    def approve(
        self,
        proposal_id: str,
        approver_id: str,
        signature: str
    ) -> bool:
        """
        批准變更
        
        Args:
            proposal_id: 提案ID
            approver_id: 批准者ID
            signature: 數字簽名
            
        Returns:
            成功返回True
        """
        record = self._approvals.get(proposal_id)
        if not record:
            return False
        
        # 驗證批准者授權
        if approver_id not in record.required_approvers:
            self.logger.error(f"批准者無權限: {approver_id}")
            return False
        
        # 記錄批准
        record.actual_approvers.append({
            'approver_id': approver_id,
            'signature': signature,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # 檢查是否達到法定人數
        quorum = self._check_quorum(record)
        
        if quorum:
            record.approval_status = 'approved'
            record.approval_timestamp = datetime.utcnow().isoformat()
            
            # 生成審計哈希
            record.audit_hash = self._generate_audit_hash(record)
            
            # 更新提案狀態
            proposal = self._proposals[proposal_id]
            proposal.status = ChangeStatus.APPROVED
            proposal.approval_record = asdict(record)
            
            # 記錄審計
            self._record_audit_event({
                'event': 'proposal_approved',
                'proposal_id': proposal_id,
                'approvers': [a['approver_id'] for a in record.actual_approvers],
                'audit_hash': record.audit_hash,
                'timestamp': record.approval_timestamp
            })
            
            self.logger.info(f"提案已批准: {proposal_id}")
        
        return True
    
    def _check_quorum(self, record: ApprovalRecord) -> bool:
        """檢查是否達到法定人數"""
        quorum_spec = self.APPROVAL_REQUIREMENTS.get(
            record.approval_level, {}
        ).get('quorum', '1-of-1')
        
        # 解析法定人數規則
        required, total = map(int, quorum_spec.split('-of-'))
        actual = len(record.actual_approvers)
        
        return actual >= required
    
    # ========================================================================
    # 階段 4: 發布 (Release)
    # ========================================================================
    
    def release_version(self, proposal_id: str) -> Dict:
        """
        發布新版本
        
        Args:
            proposal_id: 提案ID
            
        Returns:
            發布結果
        """
        proposal = self._proposals.get(proposal_id)
        if not proposal or proposal.status != ChangeStatus.APPROVED:
            return {'success': False, 'error': '提案未批准'}
        
        # 執行發布管道
        release_result = {
            'spec_id': proposal.spec_id,
            'version': proposal.proposed_version,
            'released_at': datetime.utcnow().isoformat(),
            'artifacts': []
        }
        
        # 更新狀態
        proposal.status = ChangeStatus.RELEASED
        
        # 處理舊版本棄用
        if proposal.change_category == ChangeCategory.BREAKING_CHANGE:
            self._deprecate_old_version(
                proposal.spec_id,
                proposal.current_version
            )
        
        # 記錄審計
        self._record_audit_event({
            'event': 'version_released',
            'proposal_id': proposal_id,
            'spec_id': proposal.spec_id,
            'version': proposal.proposed_version,
            'timestamp': release_result['released_at']
        })
        
        self.logger.info(
            f"版本已發布: {proposal.spec_id} v{proposal.proposed_version}"
        )
        
        return release_result
    
    def _deprecate_old_version(self, spec_id: str, old_version: str):
        """標記舊版本為棄用"""
        # 記錄棄用
        self._record_audit_event({
            'event': 'version_deprecated',
            'spec_id': spec_id,
            'version': old_version,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.logger.warning(
            f"版本已棄用: {spec_id} v{old_version}"
        )
    
    # ========================================================================
    # 階段 5: 通知 (Notification)
    # ========================================================================
    
    def notify_stakeholders(
        self,
        proposal_id: str
    ) -> Dict:
        """
        通知利益相關者
        
        Args:
            proposal_id: 提案ID
            
        Returns:
            通知結果
        """
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            return {'success': False}
        
        # 確定通知級別
        notification_tier = self._determine_notification_tier(proposal)
        
        # 識別受眾
        audiences = self._identify_notification_audiences(proposal)
        
        # 發送通知（模擬）
        notification_results = {
            'proposal_id': proposal_id,
            'tier': notification_tier,
            'audiences': audiences,
            'sent_at': datetime.utcnow().isoformat(),
            'success': True
        }
        
        # 記錄審計
        self._record_audit_event({
            'event': 'notifications_sent',
            'proposal_id': proposal_id,
            'tier': notification_tier,
            'audience_count': len(audiences),
            'timestamp': notification_results['sent_at']
        })
        
        self.logger.info(
            f"通知已發送: {proposal_id}\n"
            f"  級別: {notification_tier}\n"
            f"  受眾: {len(audiences)} 個"
        )
        
        return notification_results
    
    def _determine_notification_tier(self, proposal: ChangeProposal) -> str:
        """確定通知級別"""
        if proposal.change_category in [ChangeCategory.EMERGENCY_SECURITY, ChangeCategory.BREAKING_CHANGE]:
            return 'tier-1-critical'
        elif proposal.change_category == ChangeCategory.FEATURE_ENHANCEMENT:
            return 'tier-2-important'
        else:
            return 'tier-3-informational'
    
    def _identify_notification_audiences(self, proposal: ChangeProposal) -> List[str]:
        """識別通知受眾"""
        # 簡化實現：返回固定受眾
        audiences = ['all-validators']
        
        if proposal.change_category in [ChangeCategory.EMERGENCY_SECURITY, ChangeCategory.BREAKING_CHANGE]:
            audiences.extend(['security-team', 'governance-members'])
        
        return audiences
    
    # ========================================================================
    # 審計與追蹤
    # ========================================================================
    
    def _record_audit_event(self, event: Dict):
        """記錄審計事件（不可變）"""
        # 生成事件哈希
        event_hash = hashlib.sha256(
            json.dumps(event, sort_keys=True).encode()
        ).hexdigest()
        
        # 添加到審計追蹤
        audit_entry = {
            'event_hash': event_hash,
            'event': event,
            'recorded_at': datetime.utcnow().isoformat()
        }
        
        self._audit_trail.append(audit_entry)
    
    def _generate_audit_hash(self, record: ApprovalRecord) -> str:
        """生成批准記錄審計哈希"""
        data = {
            'proposal_id': record.proposal_id,
            'spec_id': record.spec_id,
            'from_version': record.from_version,
            'to_version': record.to_version,
            'approvers': [a['approver_id'] for a in record.actual_approvers],
            'timestamp': record.approval_timestamp
        }
        
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
    
    def get_audit_trail(
        self,
        proposal_id: Optional[str] = None
    ) -> List[Dict]:
        """獲取審計追蹤"""
        if proposal_id:
            return [
                entry for entry in self._audit_trail
                if entry['event'].get('proposal_id') == proposal_id
            ]
        return self._audit_trail
    
    def generate_compliance_report(self) -> Dict:
        """生成合規報告"""
        total_proposals = len(self._proposals)
        
        by_status = {}
        by_category = {}
        
        for proposal in self._proposals.values():
            status = proposal.status.value
            category = proposal.change_category.value
            
            by_status[status] = by_status.get(status, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            'total_proposals': total_proposals,
            'by_status': by_status,
            'by_category': by_category,
            'audit_events': len(self._audit_trail),
            'compliance_rate': 1.0  # 假設100%合規
        }
