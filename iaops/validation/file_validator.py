"""
文件检查器
File Integrity Validator

Validates:
- Source file count against baseline (detects unexpected file removal)
- Required files existence check
- File size anomaly detection
- Empty file detection
"""

import time
from pathlib import Path

from .regression_detector import RegressionDetector
from .validator import Severity, ValidationConfig, ValidationIssue, ValidatorResult


class FileCheckValidator:
    """
    文件完整性验证器
    检查源文件数量、必需文件存在性、文件大小异常和空文件
    """

    REQUIRED_FILES = [
        "README.md",
        "pyproject.toml",
    ]

    def __init__(self, config: ValidationConfig, baseline: dict | None = None):
        self.config = config
        self.name = "file_validator"
        self.baseline = baseline or {}
        self.detector = RegressionDetector(config)

    def execute(self) -> ValidatorResult:
        """执行文件完整性验证"""
        start_time = time.time()
        issues: list[ValidationIssue] = []

        project_root = Path(self.config.project_root)

        # 1. 源文件数量检查
        issues.extend(self._check_source_file_count(project_root))

        # 2. 必需文件存在性检查
        issues.extend(self._check_required_files(project_root))

        # 3. 空文件检测
        issues.extend(self._check_empty_files(project_root))

        # 4. 文件大小异常检测
        issues.extend(self._check_file_size_anomalies(project_root))

        passed = not any(issue.is_blocking() for issue in issues)
        execution_time = time.time() - start_time

        return ValidatorResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            execution_time=execution_time,
        )

    def _check_source_file_count(self, project_root: Path) -> list[ValidationIssue]:
        """检查源文件数量是否与基线一致"""
        issues = []

        # 统计 Python 源文件
        py_files = list(project_root.rglob("*.py"))
        py_files = [f for f in py_files if f.is_file() and ".git" not in str(f)]
        current_count = len(py_files)

        baseline_count = self.baseline.get("source_file_count")
        if baseline_count is not None:
            delta = current_count - baseline_count
            if delta < 0:
                severity = Severity.CRITICAL if abs(delta) > 5 else Severity.WARNING
                issues.append(
                    ValidationIssue(
                        issue_id="source_file_count_decrease",
                        description=f"源文件减少: {abs(delta)} 个文件 "
                        f"(基线: {baseline_count}, 当前: {current_count})",
                        severity=severity,
                        details={
                            "baseline": baseline_count,
                            "current": current_count,
                            "delta": delta,
                        },
                        category="file_integrity",
                        source="project_root",
                    )
                )

        # 更新基线
        self.baseline["source_file_count"] = current_count
        return issues

    def _check_required_files(self, project_root: Path) -> list[ValidationIssue]:
        """检查必需文件是否存在"""
        issues = []
        for required_file in self.REQUIRED_FILES:
            file_path = project_root / required_file
            if not file_path.exists():
                issues.append(
                    ValidationIssue(
                        issue_id=f"missing_required_file_{required_file}",
                        description=f"缺失必需文件: {required_file}",
                        severity=Severity.ERROR,
                        details={
                            "file": required_file,
                            "expected_path": str(file_path),
                        },
                        category="file_integrity",
                        source=required_file,
                    )
                )
        return issues

    def _check_empty_files(self, project_root: Path) -> list[ValidationIssue]:
        """检测空的 Python 源文件（排除 __init__.py）"""
        issues = []
        py_files = list(project_root.rglob("*.py"))
        for f in py_files:
            if not f.is_file() or ".git" in str(f):
                continue
            if f.name == "__init__.py":
                continue
            if f.stat().st_size == 0:
                issues.append(
                    ValidationIssue(
                        issue_id=f"empty_file_{f.name}",
                        description=f"空文件: {f.relative_to(project_root)}",
                        severity=Severity.WARNING,
                        details={
                            "file": str(f.relative_to(project_root)),
                            "size": 0,
                        },
                        category="file_integrity",
                        source=str(f.relative_to(project_root)),
                    )
                )
        return issues

    def _check_file_size_anomalies(self, project_root: Path) -> list[ValidationIssue]:
        """检测文件大小异常（与基线对比）"""
        issues = []

        # 确保基线数据字典存在
        if "file_sizes" not in self.baseline:
            self.baseline["file_sizes"] = {}

        baseline_sizes = self.baseline["file_sizes"]

        py_files = list(project_root.rglob("*.py"))
        for f in py_files:
            if not f.is_file() or ".git" in str(f):
                continue
            rel_path = str(f.relative_to(project_root))
            current_size = f.stat().st_size
            baseline_size = baseline_sizes.get(rel_path)

            if baseline_size and baseline_size > 100:
                # 文件缩小超过 50% 视为异常
                if current_size < baseline_size * 0.5:
                    shrink_pct = ((baseline_size - current_size) / baseline_size) * 100
                    issues.append(
                        ValidationIssue(
                            issue_id=f"file_size_anomaly_{f.name}",
                            description=f"文件大小异常缩小: {rel_path} 缩小 {shrink_pct:.1f}%",
                            severity=Severity.WARNING,
                            details={
                                "file": rel_path,
                                "baseline_size": baseline_size,
                                "current_size": current_size,
                                "shrink_pct": round(shrink_pct, 1),
                            },
                            category="file_integrity",
                            source=rel_path,
                        )
                    )

            # 无论是否有异常，都更新当前文件大小到基线
            baseline_sizes[rel_path] = current_size

        return issues

    def get_updated_baseline(self) -> dict:
        """获取更新后的基线数据"""
        return self.baseline
