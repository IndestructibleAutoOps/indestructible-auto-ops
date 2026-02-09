#!/usr/bin/env python3
"""
企业级严格工程验证系统 - 完整测试套件
Enterprise Strict Validation System - Complete Test Suite

Tests:
1. Severity ordering and comparison
2. ValidationIssue creation and blocking detection
3. ValidatorResult aggregation
4. RegressionDetector numeric/structural/trend detection
5. WhitelistManager rule matching, suppression, expiry, audit
6. FileCheckValidator file integrity checks
7. PerformanceValidator benchmark execution
8. StrictValidator full pipeline integration
9. ValidationEngine high-level API

注意：本测试套件同时支持直接运行和 pytest 运行
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

# pytest compatibility
import pytest

# 确保可以导入 validation 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from validation.file_validator import FileCheckValidator
from validation.performance_validator import PerformanceValidator
from validation.regression_detector import RegressionDetector
from validation.strict_validator import StrictValidator, ValidationEngine
from validation.validator import (
    Severity,
    ValidationConfig,
    ValidationIssue,
    ValidationResult,
    ValidatorResult,
)
from validation.whitelist_manager import WhitelistManager, WhitelistRule

# ── 测试辅助 ──────────────────────────────────────────────


class TestContext:
    """测试上下文管理器，自动创建和清理临时目录"""

    def __init__(self):
        self.temp_dir = None
        self.passed = 0
        self.failed = 0
        self.errors = []

    def setup(self):
        self.temp_dir = tempfile.mkdtemp(prefix="validation_test_")
        # 创建基本项目结构
        src_dir = Path(self.temp_dir) / "src"
        src_dir.mkdir(parents=True)
        (src_dir / "__init__.py").write_text("")
        (src_dir / "main.py").write_text("# main module\ndef main():\n    pass\n")
        (src_dir / "utils.py").write_text("# utils module\ndef helper():\n    pass\n")
        # 创建 README 和 pyproject.toml
        (Path(self.temp_dir) / "README.md").write_text("# Test Project\n")
        (Path(self.temp_dir) / "pyproject.toml").write_text('[project]\nname = "test"\n')
        return self

    def teardown(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def get_config(self, **overrides) -> ValidationConfig:
        defaults = {
            "project_root": self.temp_dir,
            "baseline_dir": os.path.join(self.temp_dir, ".baselines"),
            "output_dir": os.path.join(self.temp_dir, ".validation"),
            "strict_mode": True,
            "performance_threshold": 0.2,
            "metric_threshold": 0.1,
        }
        defaults.update(overrides)
        return ValidationConfig(**defaults)

    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"  ✅ {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  ❌ {message}")

    def assert_equal(self, actual, expected, message):
        self.assert_true(actual == expected, f"{message} (expected={expected}, actual={actual})")

    def assert_not_none(self, value, message):
        self.assert_true(value is not None, message)

    def assert_none(self, value, message):
        self.assert_true(value is None, message)

    def print_summary(self):
        total = self.passed + self.failed
        print(f"\n{'=' * 60}")
        print(f"  测试结果: {self.passed}/{total} 通过")
        if self.failed > 0:
            print(f"  ❌ 失败: {self.failed}")
            for err in self.errors:
                print(f"    - {err}")
        else:
            print("  ✅ 全部通过!")
        print(f"{'=' * 60}")
        return self.failed == 0


# ── Pytest 兼容性 ──────────────────────────────────────────


@pytest.fixture
def ctx():
    """Pytest fixture for test context"""
    test_ctx = TestContext()
    test_ctx.setup()
    yield test_ctx
    test_ctx.teardown()


# ── 测试用例 ──────────────────────────────────────────────


def test_severity(ctx: TestContext):
    """测试严重级别定义和排序"""
    print("\n📋 测试 1: Severity 严重级别")

    order = Severity.severity_order()
    ctx.assert_equal(len(order), 5, "严重级别共5个")
    ctx.assert_equal(order[0], Severity.BLOCKER, "最高级别为 BLOCKER")
    ctx.assert_equal(order[-1], Severity.INFO, "最低级别为 INFO")

    ctx.assert_true(Severity.is_blocking(Severity.BLOCKER), "BLOCKER 是阻塞性的")
    ctx.assert_true(Severity.is_blocking(Severity.CRITICAL), "CRITICAL 是阻塞性的")
    ctx.assert_true(Severity.is_blocking(Severity.ERROR), "ERROR 是阻塞性的")
    ctx.assert_true(not Severity.is_blocking(Severity.WARNING), "WARNING 不是阻塞性的")
    ctx.assert_true(not Severity.is_blocking(Severity.INFO), "INFO 不是阻塞性的")


def test_validation_issue(ctx: TestContext):
    """测试 ValidationIssue 数据结构"""
    print("\n📋 测试 2: ValidationIssue 数据结构")

    issue = ValidationIssue(
        issue_id="test_001",
        description="测试问题",
        severity=Severity.CRITICAL,
        details={"key": "value"},
        category="test",
        source="test_module",
    )

    ctx.assert_equal(issue.issue_id, "test_001", "issue_id 正确")
    ctx.assert_true(issue.is_blocking(), "CRITICAL 问题是阻塞性的")

    d = issue.to_dict()
    ctx.assert_equal(d["severity"], "CRITICAL", "to_dict 序列化正确")

    info_issue = ValidationIssue(
        issue_id="test_002",
        description="信息",
        severity=Severity.INFO,
        details={},
    )
    ctx.assert_true(not info_issue.is_blocking(), "INFO 问题不是阻塞性的")


def test_validator_result(ctx: TestContext):
    """测试 ValidatorResult 聚合"""
    print("\n📋 测试 3: ValidatorResult 聚合")

    issues = [
        ValidationIssue("i1", "blocker", Severity.BLOCKER, {}),
        ValidationIssue("i2", "critical", Severity.CRITICAL, {}),
        ValidationIssue("i3", "warning", Severity.WARNING, {}),
    ]

    result = ValidatorResult(
        validator_name="test_validator",
        passed=False,
        issues=issues,
    )

    ctx.assert_equal(result.issue_count, 3, "问题总数为 3")
    ctx.assert_equal(result.blocking_count, 2, "阻塞性问题为 2")
    ctx.assert_equal(len(result.blocking_issues), 2, "blocking_issues 列表长度为 2")

    d = result.to_dict()
    ctx.assert_equal(d["total_count"], 3, "to_dict total_count 正确")


def test_regression_numeric(ctx: TestContext):
    """测试数值型回归检测"""
    print("\n📋 测试 4: RegressionDetector 数值检测")

    config = ctx.get_config()
    detector = RegressionDetector(config)

    # 性能退化: 当前值超过基线 20%
    issue = detector.detect_numeric(1.3, 1.0, "performance", "api_latency")
    ctx.assert_not_none(issue, "检测到性能退化 (30% > 20%)")
    ctx.assert_equal(issue.severity, Severity.CRITICAL, "性能退化为 CRITICAL")

    # 性能正常: 当前值在阈值内
    issue = detector.detect_numeric(1.1, 1.0, "performance", "api_latency")
    ctx.assert_none(issue, "性能正常 (10% < 20%)")

    # 通用指标退化: 当前值低于基线 10%
    issue = detector.detect_numeric(0.85, 1.0, "general", "coverage")
    ctx.assert_not_none(issue, "检测到指标下降 (15% > 10%)")

    # 通用指标正常
    issue = detector.detect_numeric(0.95, 1.0, "general", "coverage")
    ctx.assert_none(issue, "指标正常 (5% < 10%)")

    # None 值处理
    issue = detector.detect_numeric(None, 1.0, "general", "test")
    ctx.assert_none(issue, "None 当前值返回 None")

    issue = detector.detect_numeric(1.0, None, "general", "test")
    ctx.assert_none(issue, "None 基线值返回 None")


def test_regression_structural(ctx: TestContext):
    """测试结构变化检测"""
    print("\n📋 测试 5: RegressionDetector 结构检测")

    config = ctx.get_config()
    detector = RegressionDetector(config)

    # 键差异
    issue = detector.detect_structural({"a": 1, "c": 3}, {"a": 1, "b": 2}, "test_api")
    ctx.assert_not_none(issue, "检测到键差异")
    ctx.assert_equal(issue.severity, Severity.BLOCKER, "结构变化为 BLOCKER")

    # 类型变化
    issue = detector.detect_structural({"a": "string"}, {"a": 123}, "test_api")
    ctx.assert_not_none(issue, "检测到类型变化")

    # 结构一致
    issue = detector.detect_structural({"a": 1, "b": 2}, {"a": 1, "b": 2}, "test_api")
    ctx.assert_none(issue, "结构一致无问题")

    # 空基线
    issue = detector.detect_structural({"a": 1}, {}, "test_api")
    ctx.assert_none(issue, "空基线返回 None")


def test_regression_trend(ctx: TestContext):
    """测试趋势退化检测"""
    print("\n📋 测试 6: RegressionDetector 趋势检测")

    config = ctx.get_config()
    detector = RegressionDetector(config)

    # 持续下降趋势
    declining = [100, 90, 80, 70, 60]
    issue = detector.detect_trend(declining, "test_metric", window=5)
    ctx.assert_not_none(issue, "检测到持续下降趋势")

    # 稳定趋势
    stable = [100, 101, 99, 100, 101]
    issue = detector.detect_trend(stable, "test_metric", window=5)
    ctx.assert_none(issue, "稳定趋势无问题")

    # 数据不足
    short = [100, 90]
    issue = detector.detect_trend(short, "test_metric", window=5)
    ctx.assert_none(issue, "数据不足返回 None")


def test_regression_batch(ctx: TestContext):
    """测试批量回归检测"""
    print("\n📋 测试 7: RegressionDetector 批量检测")

    config = ctx.get_config()
    detector = RegressionDetector(config)

    current = {"latency": 1.5, "coverage": 0.7, "throughput": 900}
    baseline = {"latency": 1.0, "coverage": 0.9, "throughput": 1000}
    types = {"latency": "performance", "coverage": "general", "throughput": "general"}

    issues = detector.detect_all(current, baseline, types)
    ctx.assert_true(len(issues) >= 2, f"批量检测发现 {len(issues)} 个问题 (>=2)")


def test_whitelist_basic(ctx: TestContext):
    """测试白名单基本功能"""
    print("\n📋 测试 8: WhitelistManager 基本功能")

    manager = WhitelistManager()

    rule = WhitelistRule(
        rule_id="WL-TEST-001",
        description="测试规则",
        pattern="performance_.*",
        max_severity="CRITICAL",
        approved_by="tester",
    )
    manager.add_rule(rule)

    ctx.assert_equal(len(manager.rules), 1, "添加规则成功")
    ctx.assert_equal(len(manager.get_active_rules()), 1, "活跃规则为 1")

    # 匹配测试
    issue = ValidationIssue(
        issue_id="performance_regression_api",
        description="性能退化",
        severity=Severity.CRITICAL,
        details={},
        category="performance",
    )
    ctx.assert_true(rule.matches(issue), "规则匹配 CRITICAL 性能问题")

    # BLOCKER 不可豁免
    blocker = ValidationIssue(
        issue_id="performance_regression_api",
        description="阻塞性问题",
        severity=Severity.BLOCKER,
        details={},
    )
    ctx.assert_true(not rule.matches(blocker), "BLOCKER 不可豁免")


def test_whitelist_suppression(ctx: TestContext):
    """测试白名单抑制功能"""
    print("\n📋 测试 9: WhitelistManager 抑制功能")

    manager = WhitelistManager()
    manager.add_rule(
        WhitelistRule(
            rule_id="WL-SUPP-001",
            description="抑制性能问题",
            pattern="performance_.*",
            max_severity="CRITICAL",
            approved_by="tester",
        )
    )

    issues = [
        ValidationIssue("performance_regression_api", "性能退化", Severity.CRITICAL, {}),
        ValidationIssue("structural_change_api", "结构变化", Severity.BLOCKER, {}),
        ValidationIssue("metric_regression_cov", "覆盖率下降", Severity.WARNING, {}),
    ]

    processed = manager.apply_rules(issues)
    ctx.assert_equal(len(processed), 3, "处理后问题数不变")

    # 性能问题被抑制为 INFO
    ctx.assert_equal(processed[0].severity, Severity.INFO, "性能问题被抑制为 INFO")
    ctx.assert_true("[SUPPRESSED]" in processed[0].description, "描述包含 [SUPPRESSED]")

    # BLOCKER 不受影响
    ctx.assert_equal(processed[1].severity, Severity.BLOCKER, "BLOCKER 不受影响")

    # 不匹配的问题不受影响
    ctx.assert_equal(processed[2].severity, Severity.WARNING, "不匹配的问题不受影响")

    ctx.assert_equal(manager.suppression_count, 1, "抑制计数为 1")


def test_whitelist_expiry(ctx: TestContext):
    """测试白名单过期功能"""
    print("\n📋 测试 10: WhitelistManager 过期规则")

    manager = WhitelistManager()

    # 已过期规则
    expired_rule = WhitelistRule(
        rule_id="WL-EXP-001",
        description="已过期规则",
        pattern="performance_.*",
        max_severity="CRITICAL",
        expires_at="2020-01-01T00:00:00",
        approved_by="tester",
    )
    manager.add_rule(expired_rule)

    ctx.assert_true(expired_rule.is_expired(), "规则已过期")
    ctx.assert_equal(len(manager.get_expired_rules()), 1, "过期规则列表为 1")
    ctx.assert_equal(len(manager.get_active_rules()), 0, "活跃规则列表为 0")

    # 过期规则不应抑制问题
    issues = [
        ValidationIssue("performance_regression_api", "性能退化", Severity.CRITICAL, {}),
    ]
    processed = manager.apply_rules(issues)
    ctx.assert_equal(processed[0].severity, Severity.CRITICAL, "过期规则不抑制问题")


def test_file_validator(ctx: TestContext):
    """测试文件检查器"""
    print("\n📋 测试 11: FileCheckValidator 文件检查")

    config = ctx.get_config()

    # 首次运行（无基线）
    validator = FileCheckValidator(config)
    result = validator.execute()
    ctx.assert_true(result.passed, "首次运行通过（无基线）")

    # 模拟文件减少
    baseline = {"source_file_count": 10}
    validator2 = FileCheckValidator(config, baseline=baseline)
    result2 = validator2.execute()
    # 当前只有 3 个 py 文件，基线是 10，应该检测到减少
    has_count_issue = any("source_file_count" in i.issue_id for i in result2.issues)
    ctx.assert_true(has_count_issue, "检测到源文件数量减少")


def test_file_validator_required(ctx: TestContext):
    """测试必需文件检查"""
    print("\n📋 测试 12: FileCheckValidator 必需文件")

    # 创建缺少 README 的项目
    temp_dir = tempfile.mkdtemp(prefix="validation_test_noreq_")
    try:
        Path(temp_dir).joinpath("src").mkdir()
        Path(temp_dir).joinpath("src", "main.py").write_text("pass")
        # 不创建 README.md

        config = ValidationConfig(
            project_root=temp_dir,
            baseline_dir=os.path.join(temp_dir, ".baselines"),
            output_dir=os.path.join(temp_dir, ".validation"),
        )
        validator = FileCheckValidator(config)
        result = validator.execute()

        has_missing = any("missing_required_file" in i.issue_id for i in result.issues)
        ctx.assert_true(has_missing, "检测到缺失必需文件")
    finally:
        shutil.rmtree(temp_dir)


def test_performance_validator(ctx: TestContext):
    """测试性能验证器"""
    print("\n📋 测试 13: PerformanceValidator 性能验证")

    config = ctx.get_config()
    validator = PerformanceValidator(config)

    # 注册一个简单的基准测试
    validator.register_benchmark("simple_sort", lambda: sorted(range(1000, 0, -1)))
    result = validator.execute()
    ctx.assert_true(isinstance(result, ValidatorResult), "返回 ValidatorResult")
    ctx.assert_equal(result.validator_name, "performance_validator", "验证器名称正确")


def test_performance_with_regression(ctx: TestContext):
    """测试性能退化检测"""
    print("\n📋 测试 14: PerformanceValidator 退化检测")

    config = ctx.get_config()

    # 手动设置基线使其触发退化
    baseline = {
        "performance_metrics": {
            "api_latency": {
                "current": 0.5,
                "baseline": 0.2,
                "type": "performance",
            }
        }
    }
    validator = PerformanceValidator(config, baseline=baseline)
    result = validator.execute()

    has_regression = any("regression" in i.issue_id for i in result.issues)
    ctx.assert_true(has_regression, "检测到性能退化")


def test_strict_validator_pipeline(ctx: TestContext):
    """测试完整验证管道"""
    print("\n📋 测试 15: StrictValidator 完整管道")

    config = ctx.get_config()
    validator = StrictValidator(config)
    result = validator.validate()

    ctx.assert_true(isinstance(result, ValidationResult), "返回 ValidationResult")
    ctx.assert_true(result.timestamp > 0, "时间戳有效")
    ctx.assert_true("file_validator" in result.validators, "包含 file_validator")

    # 检查报告保存
    report_dir = Path(config.output_dir)
    reports = list(report_dir.glob("report_*.json"))
    ctx.assert_true(len(reports) > 0, "报告文件已保存")


def test_validation_engine(ctx: TestContext):
    """测试高层验证引擎"""
    print("\n📋 测试 16: ValidationEngine 高层 API")

    config = ctx.get_config()
    engine = ValidationEngine(config)
    result = engine.run()

    ctx.assert_true(isinstance(result, ValidationResult), "返回 ValidationResult")
    summary = result.get_summary()
    ctx.assert_true("total" in summary, "摘要包含 total")
    ctx.assert_true("blocking" in summary, "摘要包含 blocking")


def test_validation_result_serialization(ctx: TestContext):
    """测试验证结果序列化"""
    print("\n📋 测试 17: ValidationResult 序列化")

    config = ctx.get_config()
    engine = ValidationEngine(config)
    result = engine.run()

    # 测试 to_dict
    d = result.to_dict()
    ctx.assert_true(isinstance(d, dict), "to_dict 返回字典")
    ctx.assert_true("validators" in d, "包含 validators")
    ctx.assert_true("summary" in d, "包含 summary")

    # 测试 JSON 序列化
    json_str = json.dumps(d, ensure_ascii=False)
    ctx.assert_true(len(json_str) > 0, "JSON 序列化成功")

    # 反序列化验证
    parsed = json.loads(json_str)
    ctx.assert_equal(parsed["overall_passed"], d["overall_passed"], "反序列化一致")


def test_whitelist_persistence(ctx: TestContext):
    """测试白名单持久化"""
    print("\n📋 测试 18: WhitelistManager 持久化")

    wl_path = os.path.join(ctx.temp_dir, "test_whitelist.json")

    # 创建并保存
    manager = WhitelistManager(wl_path)
    manager.add_rule(
        WhitelistRule(
            rule_id="WL-PERSIST-001",
            description="持久化测试",
            pattern="test_.*",
            max_severity="ERROR",
            approved_by="tester",
        )
    )
    manager.save_rules()

    # 重新加载
    manager2 = WhitelistManager(wl_path)
    ctx.assert_equal(len(manager2.rules), 1, "重新加载规则数量正确")
    ctx.assert_equal(
        list(manager2.rules.values())[0].rule_id,
        "WL-PERSIST-001",
        "规则 ID 正确",
    )


# ── 主执行 ──────────────────────────────────────────────


def main():
    print("=" * 60)
    print("  企业级严格工程验证系统 - 测试套件")
    print("  Enterprise Strict Validation - Test Suite")
    print("=" * 60)

    ctx = TestContext()
    ctx.setup()

    try:
        test_severity(ctx)
        test_validation_issue(ctx)
        test_validator_result(ctx)
        test_regression_numeric(ctx)
        test_regression_structural(ctx)
        test_regression_trend(ctx)
        test_regression_batch(ctx)
        test_whitelist_basic(ctx)
        test_whitelist_suppression(ctx)
        test_whitelist_expiry(ctx)
        test_file_validator(ctx)
        test_file_validator_required(ctx)
        test_performance_validator(ctx)
        test_performance_with_regression(ctx)
        test_strict_validator_pipeline(ctx)
        test_validation_engine(ctx)
        test_validation_result_serialization(ctx)
        test_whitelist_persistence(ctx)
    finally:
        ctx.teardown()

    all_passed = ctx.print_summary()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
