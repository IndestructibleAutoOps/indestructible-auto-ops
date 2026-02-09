"""
白名单管理系统
Whitelist Management System with Audit Trail

Provides:
- WhitelistRule: Single whitelist rule with expiry and audit log
- WhitelistManager: Rule loading, matching, suppression, and persistence

Key features:
- BLOCKER issues are NEVER suppressible (hard rule)
- Expired rules are automatically skipped
- All suppression events are recorded in audit log
- YAML-based rule persistence
"""

import re
import json
from datetime import datetime
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from .validator import Severity, ValidationIssue


@dataclass
class WhitelistRule:
    """
    白名单规则
    - rule_id: 规则唯一标识
    - description: 规则描述
    - pattern: 问题ID匹配正则表达式
    - max_severity: 可豁免的最高严重级别
    - file_pattern: 文件路径匹配正则 (可选)
    - category: 问题类别匹配 (可选)
    - expires_at: 过期时间 (可选, ISO格式)
    - approved_by: 审批人
    - created_at: 创建时间
    - audit_log: 抑制事件审计日志
    """
    rule_id: str
    description: str
    pattern: str
    max_severity: str = "ERROR"
    file_pattern: Optional[str] = None
    category: Optional[str] = None
    expires_at: Optional[str] = None
    approved_by: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    audit_log: List[Dict[str, Any]] = field(default_factory=list)

    def is_expired(self) -> bool:
        """检查规则是否已过期"""
        if not self.expires_at:
            return False
        try:
            expiry = datetime.fromisoformat(self.expires_at)
            return expiry < datetime.utcnow()
        except (ValueError, TypeError):
            return False

    def matches(self, issue: ValidationIssue) -> bool:
        """
        检查问题是否匹配此规则
        BLOCKER 级别问题永远不可豁免
        """
        # 硬性规则: BLOCKER 不可豁免
        if issue.severity == Severity.BLOCKER:
            return False

        # 过期规则不生效
        if self.is_expired():
            return False

        # ID 正则匹配
        try:
            if not re.search(self.pattern, issue.issue_id):
                return False
        except re.error:
            return False

        # 严重性检查: 问题严重性不能超过规则允许的最高级别
        severity_order = Severity.severity_order()
        try:
            max_sev = Severity(self.max_severity)
            max_idx = severity_order.index(max_sev)
            issue_idx = severity_order.index(issue.severity)
            # issue_idx 越小表示越严重，max_idx 越小表示允许越严重
            if issue_idx < max_idx:
                return False
        except (ValueError, KeyError):
            return False

        # 文件路径匹配
        if self.file_pattern and "file" in issue.details:
            try:
                if not re.search(self.file_pattern, issue.details["file"]):
                    return False
            except re.error:
                return False

        # 类别匹配
        if self.category and issue.category and issue.category != self.category:
            return False

        return True

    def log_suppression(self, issue_id: str, issue_description: str = ""):
        """记录抑制事件到审计日志"""
        self.audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "issue_id": issue_id,
            "description": issue_description,
            "action": "suppressed",
        })


class WhitelistManager:
    """
    白名单管理器
    负责规则加载、匹配、抑制和持久化
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else None
        self.rules: Dict[str, WhitelistRule] = {}
        self._suppression_count = 0
        if self.config_path:
            self.load_rules()

    def load_rules(self):
        """从 YAML 文件加载规则"""
        if not self.config_path or not self.config_path.exists():
            return

        if HAS_YAML:
            with self.config_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        else:
            # 回退到 JSON 格式
            json_path = self.config_path.with_suffix(".json")
            if json_path.exists():
                with json_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}

        for rule_data in data.get("rules", []):
            rule = WhitelistRule(**rule_data)
            self.rules[rule.rule_id] = rule

    def save_rules(self):
        """保存规则到文件（包含审计日志）"""
        if not self.config_path:
            return

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"rules": [asdict(rule) for rule in self.rules.values()]}

        if HAS_YAML:
            with self.config_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, indent=2, allow_unicode=True, default_flow_style=False)
        else:
            json_path = self.config_path.with_suffix(".json")
            with json_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def add_rule(self, rule: WhitelistRule):
        """添加新规则"""
        self.rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """移除规则"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False

    def apply_rules(self, issues: List[ValidationIssue]) -> List[ValidationIssue]:
        """
        应用白名单规则过滤问题列表
        - BLOCKER 问题不可豁免
        - 匹配的问题降级为 INFO 并标记 [SUPPRESSED]
        - 所有抑制事件记录到审计日志
        :return: 处理后的问题列表
        """
        processed_issues = []
        self._suppression_count = 0

        for issue in issues:
            # BLOCKER 问题直接保留，不可豁免
            if issue.severity == Severity.BLOCKER:
                processed_issues.append(issue)
                continue

            suppressed = False
            for rule in self.rules.values():
                if rule.is_expired():
                    continue

                if rule.matches(issue):
                    # 记录抑制事件
                    rule.log_suppression(issue.issue_id, issue.description)

                    # 降级为 INFO 并标记
                    issue.severity = Severity.INFO
                    issue.description = f"[SUPPRESSED] {issue.description}"
                    issue.details["suppression_rule"] = rule.rule_id
                    issue.details["suppressed_at"] = datetime.utcnow().isoformat()
                    suppressed = True
                    self._suppression_count += 1
                    break

            processed_issues.append(issue)

        # 保存更新后的规则（包含审计日志）
        self.save_rules()
        return processed_issues

    @property
    def suppression_count(self) -> int:
        """获取最近一次 apply_rules 的抑制数量"""
        return self._suppression_count

    def get_active_rules(self) -> List[WhitelistRule]:
        """获取所有未过期的活跃规则"""
        return [r for r in self.rules.values() if not r.is_expired()]

    def get_expired_rules(self) -> List[WhitelistRule]:
        """获取所有已过期的规则"""
        return [r for r in self.rules.values() if r.is_expired()]

    def get_audit_summary(self) -> Dict[str, int]:
        """获取审计日志摘要"""
        summary = {}
        for rule in self.rules.values():
            summary[rule.rule_id] = len(rule.audit_log)
        return summary