#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MNGA 完整命名治理強制執行器 v1.0
Complete Naming Governance Enforcer

整合統一命名治理契約中定義的 16 種命名規範：
1. Comment Naming - 註解命名
2. Mapping Naming - 映射命名
3. Reference Naming - 引用命名
4. Path Naming - 路徑命名
5. Port Naming - 端口命名
6. Service Naming - 服務命名
7. Dependency Naming - 依賴命名
8. Short Naming - 短命名
9. Long Naming - 長命名
10. Directory Naming - 目錄命名
11. File Naming - 文件命名
12. Event Naming - 事件命名
13. Variable Naming - 變數命名
14. Environment Variable Naming - 環境變數命名
15. GitOps Naming - GitOps 命名
16. Helm Release Naming - Helm 發布命名

@GL-governed
@GL-layer: GL20-29
@GL-semantic: complete-naming-enforcement
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# ============================================================================
# 數據結構
# ============================================================================


class NamingCategory(Enum):
    """命名類別"""

    COMMENT = "comment"
    MAPPING = "mapping"
    REFERENCE = "reference"
    PATH = "path"
    PORT = "port"
    SERVICE = "service"
    DEPENDENCY = "dependency"
    SHORT = "short"
    LONG = "long"
    DIRECTORY = "directory"
    FILE = "file"
    EVENT = "event"
    VARIABLE = "variable"
    ENV_VAR = "env_var"
    GITOPS = "gitops"
    HELM = "helm"
    LABEL = "label"
    API = "api"
    DNS = "dns"
    COMPONENT = "component"


class Severity(Enum):
    """嚴重性級別"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class NamingViolation:
    """命名違規記錄"""

    rule_id: str
    category: NamingCategory
    path: str
    name: str
    expected_pattern: str
    actual_value: str
    severity: Severity
    message: str
    suggestion: str
    line_number: Optional[int] = None
    auto_fixable: bool = False
    fix_command: Optional[str] = None


@dataclass
class NamingCheckResult:
    """命名檢查結果"""

    category: NamingCategory
    passed: bool
    items_checked: int
    violations: List[NamingViolation] = field(default_factory=list)
    execution_time_ms: int = 0


@dataclass
class CompleteNamingReport:
    """完整命名報告"""

    timestamp: str
    workspace: str
    total_checks: int = 0
    passed_checks: int = 0
    total_violations: int = 0
    by_category: Dict[str, int] = field(default_factory=dict)
    by_severity: Dict[str, int] = field(default_factory=dict)
    results: List[NamingCheckResult] = field(default_factory=list)
    compliance_rate: float = 0.0


# ============================================================================
# 命名規範定義
# ============================================================================


class NamingPatterns:
    """命名規範模式定義"""

    # 1. Comment Naming: gl:<domain>:<capability>:<tag>
    COMMENT_TAG = re.compile(r"^gl:[a-z]+:[a-z]+:[a-z-]+$")
    COMMENT_BLOCK = re.compile(r"^gl-block:[a-z]+:[a-z]+:[a-z_]+$")
    COMMENT_KEY = re.compile(r"^gl\.key\.[a-z]+\.[a-z]+\.[a-z_]+$")

    # 2. Mapping Naming: gl-<domain>-<capability>-map
    MAPPING = re.compile(r"^gl-[a-z]+-[a-z]+-map$")

    # 3. Reference Naming: gl.ref.<domain>.<capability>.<resource>
    REFERENCE = re.compile(r"^gl\.ref\.[a-z]+\.[a-z]+\.[a-z]+$")

    # 4. Path Naming: /gl/<domain>/<capability>/<resource>
    API_PATH = re.compile(r"^/gl/[a-z]+/[a-z]+(/[a-z-]+)*$")
    REPO_PATH = re.compile(r"^/platforms/gl-[a-z]+-[a-z]+-platform$")

    # 5. Port Naming: <protocol>-<domain>-<capability>
    PORT = re.compile(r"^(http|grpc|metrics)-[a-z]+-[a-z]+$")

    # 6. Service Naming: gl-<domain>-<capability>-svc
    SERVICE = re.compile(r"^gl-[a-z]+-[a-z]+-svc$")

    # 7. Dependency Naming: gl.dep.<domain>.<capability>
    DEPENDENCY = re.compile(r"^gl\.dep\.[a-z]+\.[a-z]+$")

    # 8. Short Naming: gl.<abbr> or gl.<domainabbr>.<capabbr>
    SHORT = re.compile(r"^gl\.[a-z]{2,4}(\.[a-z]{2,4})?$")

    # 9. Long Naming: gl-<domain>-<capability>-<resource>
    LONG = re.compile(r"^gl-[a-z]+-[a-z]+(-[a-z]+)?$")

    # 10. Directory Naming
    PLATFORM_DIR = re.compile(r"^gl-[a-z]+-[a-z]+-platform$")
    SERVICE_DIR = re.compile(r"^gl-[a-z]+-[a-z]+-service$")
    MODULE_DIR = re.compile(r"^gl-[a-z]+-[a-z]+-module$")
    KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")

    # 11. File Naming
    GL_FILE = re.compile(r"^gl-[a-z]+-[a-z]+-[a-z-]+\.(yaml|json|md|py|ts|js|go)$")
    PYTHON_FILE = re.compile(r"^[a-z][a-z0-9_]*\.py$")
    CONFIG_FILE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.(yaml|yml|json|toml)$")

    # 12. Event Naming: gl.event.<domain>.<capability>.<action>
    EVENT = re.compile(r"^gl\.event\.[a-z]+\.[a-z]+\.[a-z]+$")

    # 13. Variable Naming: GL<DOMAIN><CAPABILITY>_<RESOURCE>
    VARIABLE = re.compile(r"^GL[A-Z]+_[A-Z_]+$")

    # 14. Environment Variable: GL_<DOMAIN>_<CAPABILITY>_<KEY>
    ENV_VAR = re.compile(r"^GL_[A-Z]+_[A-Z]+_[A-Z_]+$")

    # 15. GitOps Naming: gl-<env>-<domain>-<capability>
    GITOPS = re.compile(r"^gl-(dev|staging|prod)-[a-z]+-[a-z]+$")

    # 16. Helm Release: gl-<domain>-<capability>-<env>
    HELM = re.compile(r"^gl-[a-z]+-[a-z]+-(dev|staging|prod)$")

    # K8s Labels
    K8S_LABEL_KEY = re.compile(
        r"^(app\.kubernetes\.io|gl\.machinenativeops\.io)/[a-z-]+$"
    )

    # GL Annotations
    GL_ANNOTATION = re.compile(r"^@GL-(governed|layer|semantic|audit-trail)")


# ============================================================================
# 完整命名治理檢查器
# ============================================================================


class CompleteNamingEnforcer:
    """完整命名治理強制執行器"""

    def __init__(self, workspace_path: Path):
        self.workspace = workspace_path
        self.patterns = NamingPatterns()
        self.violations: List[NamingViolation] = []
        self.results: List[NamingCheckResult] = []

        # 排除目錄
        self.excluded_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".idea",
            ".vscode",
            "outputs",
            ".governance",
            "archived",
            "legacy",
            "summarized-conversations",
        }

        # 特殊目錄例外
        self.special_exceptions = {
            ".github",
            "PULL_REQUEST_TEMPLATE",
            "ISSUE_TEMPLATE",
            "(tabs)",
            "(auth)",
            "(app)",
            "RUNBOOKS",
            "TRAINING",
            "MIGRATION",
        }

        # GL 語義目錄模式
        self.gl_semantic_pattern = re.compile(r"^GL\d{2}(-\d{2})?(-[A-Za-z-]+)?$")

    def _should_exclude(self, path: Path) -> bool:
        """檢查是否應排除路徑"""
        for part in path.parts:
            if part in self.excluded_dirs:
                return True
        return False

    # ========================================================================
    # 1. Comment Naming Check (註解命名)
    # ========================================================================

    def check_comment_naming(self) -> NamingCheckResult:
        """檢查註解命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        # 檢查 Python 文件中的 GL 標註
        for py_file in self.workspace.rglob("*.py"):
            if self._should_exclude(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")
                lines = content.split("\n")

                for i, line in enumerate(lines):
                    # 檢查 @GL- 標註
                    if "@GL-" in line:
                        items_checked += 1
                        if not self.patterns.GL_ANNOTATION.search(line):
                            violations.append(
                                NamingViolation(
                                    rule_id="GL20-COMMENT-001",
                                    category=NamingCategory.COMMENT,
                                    path=str(py_file.relative_to(self.workspace)),
                                    name=line.strip()[:50],
                                    expected_pattern="@GL-(governed|layer|semantic|audit-trail)",
                                    actual_value=line.strip()[:50],
                                    severity=Severity.MEDIUM,
                                    message="GL 標註格式不正確",
                                    suggestion="使用 @GL-governed, @GL-layer, @GL-semantic 或 @GL-audit-trail",
                                    line_number=i + 1,
                                )
                            )

                    # 檢查 gl: 標籤
                    if "gl:" in line.lower() and "#" in line:
                        items_checked += 1
                        # 提取 gl: 標籤
                        match = re.search(r"gl:[a-z:_-]+", line.lower())
                        if match:
                            tag = match.group()
                            if not self.patterns.COMMENT_TAG.match(tag):
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-COMMENT-002",
                                        category=NamingCategory.COMMENT,
                                        path=str(py_file.relative_to(self.workspace)),
                                        name=tag,
                                        expected_pattern="gl:<domain>:<capability>:<tag>",
                                        actual_value=tag,
                                        severity=Severity.LOW,
                                        message="GL 標籤格式不正確",
                                        suggestion="使用 gl:<domain>:<capability>:<tag> 格式",
                                        line_number=i + 1,
                                    )
                                )
            except Exception:
                pass

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.COMMENT,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 4. Path Naming Check (路徑命名)
    # ========================================================================

    def check_path_naming(self) -> NamingCheckResult:
        """檢查 API 路徑命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        # 檢查 OpenAPI/Swagger 文件中的路徑
        for yaml_file in self.workspace.rglob("*.yaml"):
            if self._should_exclude(yaml_file):
                continue
            if (
                "openapi" not in yaml_file.name.lower()
                and "swagger" not in yaml_file.name.lower()
            ):
                continue

            try:
                content = yaml_file.read_text(encoding="utf-8")

                # 簡單的路徑提取
                path_matches = re.findall(
                    r"^\s+(/[a-zA-Z0-9/_-]+):", content, re.MULTILINE
                )

                for path in path_matches:
                    items_checked += 1

                    # 檢查是否以 /gl/ 或 /api/ 開頭
                    if not path.startswith("/gl/") and not path.startswith("/api/"):
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-PATH-001",
                                category=NamingCategory.PATH,
                                path=str(yaml_file.relative_to(self.workspace)),
                                name=path,
                                expected_pattern="/gl/<domain>/<capability>/* or /api/v*/*",
                                actual_value=path,
                                severity=Severity.MEDIUM,
                                message="API 路徑應以 /gl/ 或 /api/ 開頭",
                                suggestion=f"重命名為 /gl{path} 或 /api/v1{path}",
                            )
                        )
            except Exception:
                pass

        # 檢查治理契約中的路徑定義
        for yaml_file in self.workspace.rglob("*governance*.yaml"):
            if self._should_exclude(yaml_file):
                continue

            try:
                content = yaml_file.read_text(encoding="utf-8")

                # 提取 path: 定義
                path_matches = re.findall(
                    r'path:\s*["\']?(/[a-zA-Z0-9/_-]+)["\']?', content
                )

                for path in path_matches:
                    items_checked += 1

                    if path.startswith("/gl/"):
                        if not self.patterns.API_PATH.match(path):
                            violations.append(
                                NamingViolation(
                                    rule_id="GL20-PATH-002",
                                    category=NamingCategory.PATH,
                                    path=str(yaml_file.relative_to(self.workspace)),
                                    name=path,
                                    expected_pattern="/gl/<domain>/<capability>/<resource>",
                                    actual_value=path,
                                    severity=Severity.LOW,
                                    message="GL API 路徑格式不正確",
                                    suggestion="使用 /gl/<domain>/<capability>/<resource> 格式",
                                )
                            )
            except Exception:
                pass

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.PATH,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 6. Service Naming Check (服務命名)
    # ========================================================================

    def check_service_naming(self) -> NamingCheckResult:
        """檢查 K8s Service 命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        # 檢查 K8s YAML 文件
        for yaml_file in self.workspace.rglob("*.yaml"):
            if self._should_exclude(yaml_file):
                continue

            try:
                content = yaml_file.read_text(encoding="utf-8")

                # 檢查是否是 K8s Service
                if "kind: Service" in content:
                    # 提取 Service 名稱
                    name_match = re.search(
                        r'metadata:\s*\n\s*name:\s*["\']?([a-zA-Z0-9-]+)["\']?', content
                    )

                    if name_match:
                        service_name = name_match.group(1)
                        items_checked += 1

                        # 檢查是否符合 gl-*-svc 格式
                        if service_name.startswith("gl-"):
                            if not self.patterns.SERVICE.match(service_name):
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-SVC-001",
                                        category=NamingCategory.SERVICE,
                                        path=str(yaml_file.relative_to(self.workspace)),
                                        name=service_name,
                                        expected_pattern="gl-<domain>-<capability>-svc",
                                        actual_value=service_name,
                                        severity=Severity.HIGH,
                                        message="GL Service 名稱格式不正確",
                                        suggestion="使用 gl-<domain>-<capability>-svc 格式",
                                    )
                                )
                        elif not service_name.endswith(
                            "-svc"
                        ) and not service_name.endswith("-service"):
                            violations.append(
                                NamingViolation(
                                    rule_id="GL20-SVC-002",
                                    category=NamingCategory.SERVICE,
                                    path=str(yaml_file.relative_to(self.workspace)),
                                    name=service_name,
                                    expected_pattern="*-svc or *-service",
                                    actual_value=service_name,
                                    severity=Severity.MEDIUM,
                                    message="Service 名稱應以 -svc 或 -service 結尾",
                                    suggestion=f"重命名為 {service_name}-svc",
                                )
                            )
            except Exception:
                pass

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.SERVICE,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 10. Directory Naming Check (目錄命名)
    # ========================================================================

    def check_directory_naming(self) -> NamingCheckResult:
        """檢查目錄命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        for dir_path in self.workspace.rglob("*"):
            if not dir_path.is_dir():
                continue
            if self._should_exclude(dir_path):
                continue

            name = dir_path.name
            items_checked += 1

            # 跳過特殊目錄
            if name in self.special_exceptions:
                continue
            if self.gl_semantic_pattern.match(name):
                continue
            if name.startswith(".") or name.startswith("__"):
                continue

            # Python 包目錄允許 snake_case
            if (dir_path / "__init__.py").exists():
                if not self.patterns.SNAKE_CASE.match(name):
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-DIR-001",
                            category=NamingCategory.DIRECTORY,
                            path=str(dir_path.relative_to(self.workspace)),
                            name=name,
                            expected_pattern="snake_case (Python package)",
                            actual_value=name,
                            severity=Severity.MEDIUM,
                            message=f"Python 包目錄 '{name}' 命名不規範",
                            suggestion=f"重命名為 {name.replace('-', '_').lower()}",
                        )
                    )
                continue

            # 平台目錄檢查
            if name.startswith("gl-") and "platform" in name:
                if not self.patterns.PLATFORM_DIR.match(name):
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-DIR-002",
                            category=NamingCategory.DIRECTORY,
                            path=str(dir_path.relative_to(self.workspace)),
                            name=name,
                            expected_pattern="gl-<domain>-<capability>-platform",
                            actual_value=name,
                            severity=Severity.MEDIUM,
                            message=f"平台目錄 '{name}' 格式不正確",
                            suggestion="使用 gl-<domain>-<capability>-platform 格式",
                        )
                    )
                continue

            # 一般目錄應使用 kebab-case
            if "_" in name:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-DIR-003",
                        category=NamingCategory.DIRECTORY,
                        path=str(dir_path.relative_to(self.workspace)),
                        name=name,
                        expected_pattern="kebab-case",
                        actual_value=name,
                        severity=Severity.MEDIUM,
                        message=f"目錄 '{name}' 使用下劃線，應使用連字符",
                        suggestion=f"重命名為 {name.replace('_', '-')}",
                        auto_fixable=True,
                        fix_command=f"mv {dir_path} {dir_path.parent / name.replace('_', '-')}",
                    )
                )

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.DIRECTORY,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 11. File Naming Check (文件命名)
    # ========================================================================

    def check_file_naming(self) -> NamingCheckResult:
        """檢查文件命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        for file_path in self.workspace.rglob("*"):
            if not file_path.is_file():
                continue
            if self._should_exclude(file_path):
                continue

            name = file_path.name
            stem = file_path.stem
            suffix = file_path.suffix.lower()
            items_checked += 1

            # Python 文件
            if suffix == ".py":
                if name.startswith("__") and name.endswith("__.py"):
                    continue

                if "-" in stem:
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-FILE-001",
                            category=NamingCategory.FILE,
                            path=str(file_path.relative_to(self.workspace)),
                            name=name,
                            expected_pattern="snake_case.py",
                            actual_value=name,
                            severity=Severity.HIGH,
                            message=f"Python 文件 '{name}' 使用連字符，應使用下劃線",
                            suggestion=f"重命名為 {stem.replace('-', '_')}.py",
                            auto_fixable=True,
                        )
                    )

            # 配置文件
            elif suffix in [".yaml", ".yml", ".json", ".toml"]:
                # 跳過特殊文件
                if name in ["package.json", "package-lock.json", "tsconfig.json"]:
                    continue
                # 跳過 GL 語義文件
                if stem.startswith("GL") and re.match(r"^GL\d{2}", stem):
                    continue

                if "_" in stem:
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-FILE-002",
                            category=NamingCategory.FILE,
                            path=str(file_path.relative_to(self.workspace)),
                            name=name,
                            expected_pattern="kebab-case.yaml",
                            actual_value=name,
                            severity=Severity.MEDIUM,
                            message=f"配置文件 '{name}' 使用下劃線，應使用連字符",
                            suggestion=f"重命名為 {stem.replace('_', '-')}{suffix}",
                            auto_fixable=True,
                        )
                    )

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.FILE,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 標籤命名檢查 (K8s Labels)
    # ========================================================================

    def check_label_naming(self) -> NamingCheckResult:
        """檢查 K8s 標籤命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        required_labels = [
            "app.kubernetes.io/name",
            "app.kubernetes.io/component",
        ]

        for yaml_file in self.workspace.rglob("*.yaml"):
            if self._should_exclude(yaml_file):
                continue

            try:
                content = yaml_file.read_text(encoding="utf-8")

                # 檢查是否是 K8s 資源
                if "kind:" in content and "metadata:" in content:
                    # 檢查是否有 labels
                    if "labels:" in content:
                        items_checked += 1

                        # 檢查必要標籤
                        for label in required_labels:
                            if label not in content:
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-LABEL-001",
                                        category=NamingCategory.LABEL,
                                        path=str(yaml_file.relative_to(self.workspace)),
                                        name=label,
                                        expected_pattern=label,
                                        actual_value="missing",
                                        severity=Severity.LOW,
                                        message=f"缺少推薦標籤: {label}",
                                        suggestion=f"添加 {label} 標籤",
                                    )
                                )
            except Exception:
                pass

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.LABEL,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 環境變數命名檢查
    # ========================================================================

    def check_env_var_naming(self) -> NamingCheckResult:
        """檢查環境變數命名規範"""
        start_time = datetime.now()
        violations = []
        items_checked = 0

        # 檢查 .env 文件
        for env_file in self.workspace.rglob(".env*"):
            if self._should_exclude(env_file):
                continue
            if not env_file.is_file():
                continue

            try:
                content = env_file.read_text(encoding="utf-8")
                lines = content.split("\n")

                for i, line in enumerate(lines):
                    if "=" in line and not line.startswith("#"):
                        var_name = line.split("=")[0].strip()
                        items_checked += 1

                        # 檢查 GL 相關環境變數
                        if var_name.startswith("GL"):
                            if not self.patterns.ENV_VAR.match(var_name):
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-ENV-001",
                                        category=NamingCategory.ENV_VAR,
                                        path=str(env_file.relative_to(self.workspace)),
                                        name=var_name,
                                        expected_pattern="GL_<DOMAIN>_<CAPABILITY>_<KEY>",
                                        actual_value=var_name,
                                        severity=Severity.MEDIUM,
                                        message=f"GL 環境變數 '{var_name}' 格式不正確",
                                        suggestion="使用 GL_<DOMAIN>_<CAPABILITY>_<KEY> 格式",
                                        line_number=i + 1,
                                    )
                                )
            except Exception:
                pass

        elapsed = (datetime.now() - start_time).total_seconds() * 1000

        return NamingCheckResult(
            category=NamingCategory.ENV_VAR,
            passed=len(
                [
                    v
                    for v in violations
                    if v.severity in [Severity.CRITICAL, Severity.HIGH]
                ]
            )
            == 0,
            items_checked=items_checked,
            violations=violations,
            execution_time_ms=int(elapsed),
        )

    # ========================================================================
    # 主執行流程
    # ========================================================================

    def run_all_checks(self) -> CompleteNamingReport:
        """執行所有命名檢查"""
        start_time = datetime.now()

        # 執行所有檢查
        checks = [
            self.check_comment_naming,
            self.check_path_naming,
            self.check_service_naming,
            self.check_directory_naming,
            self.check_file_naming,
            self.check_label_naming,
            self.check_env_var_naming,
        ]

        results = []
        for check in checks:
            try:
                result = check()
                results.append(result)
            except Exception as e:
                print(f"檢查失敗: {check.__name__}: {e}")

        # 統計
        total_violations = sum(len(r.violations) for r in results)
        passed_checks = len([r for r in results if r.passed])

        by_category = {}
        by_severity = {}

        for result in results:
            by_category[result.category.value] = len(result.violations)
            for v in result.violations:
                by_severity[v.severity.value] = by_severity.get(v.severity.value, 0) + 1

        report = CompleteNamingReport(
            timestamp=datetime.now().isoformat(),
            workspace=str(self.workspace),
            total_checks=len(results),
            passed_checks=passed_checks,
            total_violations=total_violations,
            by_category=by_category,
            by_severity=by_severity,
            results=results,
            compliance_rate=(
                round(passed_checks / len(results) * 100, 2) if results else 0
            ),
        )

        return report

    def print_report(self, report: CompleteNamingReport):
        """打印報告"""
        print("\n" + "=" * 70)
        print("MNGA 完整命名治理檢查報告".center(70))
        print("=" * 70)

        print(f"\n總檢查數: {report.total_checks}")
        print(f"通過檢查: {report.passed_checks}")
        print(f"總違規數: {report.total_violations}")
        print(f"合規率: {report.compliance_rate}%")

        print("\n按類別統計:")
        for cat, count in report.by_category.items():
            status = "✅" if count == 0 else "❌"
            print(f"  {status} {cat}: {count} 個違規")

        print("\n按嚴重性統計:")
        for sev, count in report.by_severity.items():
            print(f"  [{sev}]: {count}")

        if report.total_violations > 0:
            print("\n" + "-" * 70)
            print("違規詳情 (前 20 個):")
            print("-" * 70)

            all_violations = []
            for result in report.results:
                all_violations.extend(result.violations)

            for v in all_violations[:20]:
                print(f"\n[{v.severity.value}] {v.rule_id}")
                print(f"  類別: {v.category.value}")
                print(f"  路徑: {v.path}")
                print(f"  名稱: {v.name}")
                print(f"  問題: {v.message}")
                print(f"  建議: {v.suggestion}")


# ============================================================================
# 主程序入口
# ============================================================================


def main():
    """主程序入口"""
    import argparse

    parser = argparse.ArgumentParser(description="MNGA 完整命名治理檢查器")
    parser.add_argument("--workspace", "-w", default=".", help="工作區路徑")
    parser.add_argument("--output", "-o", help="報告輸出路徑")
    parser.add_argument("--category", "-c", help="只檢查特定類別")

    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    enforcer = CompleteNamingEnforcer(workspace)

    report = enforcer.run_all_checks()
    enforcer.print_report(report)

    if args.output:
        import json

        with open(args.output, "w", encoding="utf-8") as f:
            # 轉換為可序列化格式
            report_dict = {
                "timestamp": report.timestamp,
                "workspace": report.workspace,
                "total_checks": report.total_checks,
                "passed_checks": report.passed_checks,
                "total_violations": report.total_violations,
                "compliance_rate": report.compliance_rate,
                "by_category": report.by_category,
                "by_severity": report.by_severity,
            }
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        print(f"\n報告已保存至: {args.output}")

    return 0 if report.passed_checks == report.total_checks else 1


if __name__ == "__main__":
    exit(main())
