"""
验证结果数据结构与严重等级定义
Enterprise Validation Data Structures & Severity Definitions

Provides:
- Severity: 5-level severity enum (BLOCKER > CRITICAL > ERROR > WARNING > INFO)
- ValidationConfig: System configuration dataclass
- ValidationIssue: Single validation issue record
- ValidatorResult: Per-validator result container
- ValidationResult: Aggregated validation report
"""

import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class Severity(str, Enum):
    """
    五级严重性定义，对应不同处理策略:
    - BLOCKER: 阻塞性问题，不可豁免，必须立即修复
    - CRITICAL: 关键问题，可在白名单内豁免，需优先处理
    - ERROR: 错误，阻止部署但可通过审批豁免
    - WARNING: 警告，不阻止部署但需关注
    - INFO: 信息，仅供参考
    """
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

    @classmethod
    def severity_order(cls) -> list:
        """返回严重性从高到低的排序列表"""
        return [cls.BLOCKER, cls.CRITICAL, cls.ERROR, cls.WARNING, cls.INFO]

    @classmethod
    def is_blocking(cls, severity: "Severity") -> bool:
        """判断是否为阻塞性严重级别"""
        return severity in [cls.BLOCKER, cls.CRITICAL]

    def __lt__(self, other):
        if not isinstance(other, Severity):
            return NotImplemented
        order = self.severity_order()
        return order.index(self) > order.index(other)

    def __le__(self, other):
        if not isinstance(other, Severity):
            return NotImplemented
        order = self.severity_order()
        return order.index(self) >= order.index(other)


@dataclass
class ValidationConfig:
    """
    验证系统配置
    - project_root: 项目根目录
    - baseline_dir: 基线数据存储目录
    - output_dir: 验证报告输出目录
    - whitelist_path: 白名单配置文件路径
    - strict_mode: 是否启用严格模式
    - performance_threshold: 性能偏差阈值 (默认20%)
    - metric_threshold: 通用指标偏差阈值 (默认10%)
    """
    project_root: str
    baseline_dir: str = ".baselines"
    output_dir: str = ".validation"
    whitelist_path: Optional[str] = None
    strict_mode: bool = True
    performance_threshold: float = 0.2
    metric_threshold: float = 0.1

    def ensure_dirs(self):
        """确保所有必要目录存在"""
        Path(self.baseline_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)


@dataclass
class ValidationIssue:
    """
    单个验证问题记录
    - issue_id: 问题唯一标识
    - description: 问题描述
    - severity: 严重级别
    - details: 详细数据字典
    - category: 问题类别 (performance/structural/functional)
    - source: 问题来源 (文件路径/模块名)
    """
    issue_id: str
    description: str
    severity: Severity
    details: Dict[str, Any]
    category: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        """转换为可序列化字典"""
        d = asdict(self)
        d["severity"] = self.severity.value
        return d

    def is_blocking(self) -> bool:
        """判断此问题是否为阻塞性"""
        return Severity.is_blocking(self.severity)

    def __repr__(self):
        return f"[{self.severity.value}] {self.issue_id}: {self.description}"


@dataclass
class ValidatorResult:
    """
    单个验证器的执行结果
    - validator_name: 验证器名称
    - passed: 是否通过
    - issues: 发现的问题列表
    - execution_time: 执行耗时(秒)
    """
    validator_name: str
    passed: bool
    issues: List[ValidationIssue]
    execution_time: float = 0.0

    @property
    def blocking_issues(self) -> List[ValidationIssue]:
        """获取所有阻塞性问题"""
        return [issue for issue in self.issues if issue.is_blocking()]

    @property
    def issue_count(self) -> int:
        """问题总数"""
        return len(self.issues)

    @property
    def blocking_count(self) -> int:
        """阻塞性问题数量"""
        return len(self.blocking_issues)

    def to_dict(self) -> dict:
        """转换为可序列化字典"""
        return {
            "validator_name": self.validator_name,
            "passed": self.passed,
            "issues": [issue.to_dict() for issue in self.issues],
            "execution_time": self.execution_time,
            "blocking_count": self.blocking_count,
            "total_count": self.issue_count,
        }


@dataclass
class ValidationResult:
    """
    验证结果汇总报告
    - timestamp: 验证时间戳
    - config: 验证配置
    - validators: 各验证器结果
    - overall_passed: 整体是否通过
    - suppressed_issues: 被白名单抑制的问题数
    """
    timestamp: float
    config: dict
    validators: Dict[str, ValidatorResult]
    overall_passed: bool
    suppressed_issues: int = 0

    def save(self, output_dir: str) -> Path:
        """保存验证结果到JSON文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        report_file = output_path / f"report_{int(self.timestamp)}.json"
        with report_file.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        return report_file

    def to_dict(self) -> dict:
        """转换为可序列化字典"""
        return {
            "timestamp": self.timestamp,
            "config": self.config,
            "validators": {
                k: v.to_dict() for k, v in self.validators.items()
            },
            "overall_passed": self.overall_passed,
            "suppressed_issues": self.suppressed_issues,
            "summary": self.get_summary(),
        }

    def get_summary(self) -> dict:
        """生成问题摘要统计"""
        summary = {sev.value: 0 for sev in Severity}
        for v in self.validators.values():
            for issue in v.issues:
                summary[issue.severity.value] += 1
        summary["total"] = sum(summary.values())
        summary["blocking"] = summary.get("BLOCKER", 0) + summary.get("CRITICAL", 0)
        return summary

    def print_report(self):
        """打印验证报告到控制台"""
        if self.overall_passed:
            print("✅ 所有验证通过 - 可安全部署")
        else:
            print("❌ 发现阻塞性问题 - 部署被阻止")

        print(f"\n📊 问题摘要:")
        summary = self.get_summary()
        for sev in Severity.severity_order():
            count = summary.get(sev.value, 0)
            if count > 0:
                print(f"  {sev.value}: {count}")
        print(f"  总计: {summary['total']}")
        print(f"  已抑制: {self.suppressed_issues}")

        print(f"\n📋 验证器详情:")
        for name, result in self.validators.items():
            status = "✅" if result.passed else "❌"
            print(f"  {status} {name} ({result.execution_time:.3f}s) - "
                  f"{result.issue_count} 问题, {result.blocking_count} 阻塞")
            for issue in result.blocking_issues:
                print(f"    🛑 [{issue.severity.value}] {issue.issue_id}: {issue.description}")