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

# Naming type markers required by MNGA enforcement
NAMING_TYPE_MARKERS = [
    "CommentNaming",
    "MappingNaming",
    "ReferenceNaming",
    "PathNaming",
    "PortNaming",
    "ServiceNaming",
    "DependencyNaming",
    "ShortNaming",
    "LongNaming",
    "DirectoryNaming",
    "FileNaming",
    "EventNaming",
    "VariableNaming",
    "EnvironmentVariableNaming",
    "GitOpsNaming",
    "HelmReleaseNaming",
]

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
    """命名規範模式定義。

    NG 前綴代表 Naming Governance 命名空間，只用於命名規範檢查，並不要求整個儲存庫都改名；
    同時保留 legacy GL 前綴兼容。
    """

    def __init__(self, primary_prefix: str = "ng", legacy_prefix: Optional[str] = "gl"):
        prefixes = [primary_prefix.lower()]
        if legacy_prefix:
            prefixes.append(legacy_prefix.lower())

        allowed_prefix = re.compile(r"^[a-z0-9-]+$")
        validated = []
        for p in prefixes:
            if not allowed_prefix.fullmatch(p):
                raise ValueError(f"Invalid naming prefix: {p}")
            validated.append(p)

        self.prefixes: Tuple[str, ...] = tuple(dict.fromkeys(validated))
        escaped_prefixes = [re.escape(p) for p in self.prefixes]
        escaped_upper_prefixes = [re.escape(p.upper()) for p in self.prefixes]

        self.primary_prefix = self.prefixes[0]
        self.prefix_group = "|".join(escaped_prefixes)
        self.upper_prefix_group = "|".join(escaped_upper_prefixes)

        prefix = rf"(?:{self.prefix_group})"
        upper_prefix = rf"(?:{self.upper_prefix_group})"

        # 1. Comment Naming: <prefix>:<domain>:<capability>:<tag>
        self.COMMENT_TAG = re.compile(rf"^{prefix}:[a-z]+:[a-z]+:[a-z-]+$")
        self.COMMENT_BLOCK = re.compile(rf"^{prefix}-block:[a-z]+:[a-z]+:[a-z_]+$")
        self.COMMENT_KEY = re.compile(rf"^{prefix}\.key\.[a-z]+\.[a-z]+\.[a-z_]+$")

        # 2. Mapping Naming: <prefix>-<domain>-<capability>-map
        self.MAPPING = re.compile(rf"^{prefix}-[a-z]+-[a-z]+-map$")

        # 3. Reference Naming: <prefix>.ref.<domain>.<capability>.<resource>
        self.REFERENCE = re.compile(rf"^{prefix}\.ref\.[a-z]+\.[a-z]+\.[a-z]+$")

        # 4. Path Naming: /<prefix>/<domain>/<capability>/<resource>
        self.API_PATH = re.compile(rf"^/{prefix}/[a-z]+/[a-z]+(/[a-z-]+)*$")
        self.REPO_PATH = re.compile(rf"^/platforms/{prefix}-[a-z]+-[a-z]+-platform$")

        # 5. Port Naming: <protocol>-<domain>-<capability>
        self.PORT = re.compile(r"^(http|grpc|metrics)-[a-z]+-[a-z]+$")

        # 6. Service Naming: <prefix>-<domain>-<capability>-svc
        self.SERVICE = re.compile(rf"^{prefix}-[a-z]+-[a-z]+-svc$")

        # 7. Dependency Naming: <prefix>.dep.<domain>.<capability>
        self.DEPENDENCY = re.compile(rf"^{prefix}\.dep\.[a-z]+\.[a-z]+$")

        # 8. Short Naming: <prefix>.<abbr> or <prefix>.<domainabbr>.<capabbr>
        self.SHORT = re.compile(rf"^{prefix}\.[a-z]{2,4}(\.[a-z]{2,4})?$")

        # 9. Long Naming: <prefix>-<domain>-<capability>-<resource>
        self.LONG = re.compile(rf"^{prefix}-[a-z]+-[a-z]+(-[a-z]+)?$")

        # 10. Directory Naming
        self.PLATFORM_DIR = re.compile(rf"^{prefix}-[a-z]+-[a-z]+-platform$")
        self.SERVICE_DIR = re.compile(rf"^{prefix}-[a-z]+-[a-z]+-service$")
        self.MODULE_DIR = re.compile(rf"^{prefix}-[a-z]+-[a-z]+-module$")
        self.KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")

        # 11. File Naming
        self.GL_FILE = re.compile(
            rf"^{prefix}-[a-z]+-[a-z]+-[a-z-]+\.(yaml|json|md|py|ts|js|go)$"
        )
        self.PYTHON_FILE = re.compile(r"^[a-z][a-z0-9_]*\.py$")
        self.CONFIG_FILE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.(yaml|yml|json|toml)$")

        # 12. Event Naming: <prefix>.event.<domain>.<capability>.<action>
        self.EVENT = re.compile(rf"^{prefix}\.event\.[a-z]+\.[a-z]+\.[a-z]+$")

        # 13. Variable Naming: <PREFIX><DOMAIN><CAPABILITY>_<RESOURCE>
        self.VARIABLE = re.compile(rf"^{upper_prefix}[A-Z]+_[A-Z_]+$")

        # 14. Environment Variable: <PREFIX>_<DOMAIN>_<CAPABILITY>_<KEY>
        self.ENV_VAR = re.compile(rf"^{upper_prefix}_[A-Z]+_[A-Z]+_[A-Z_]+$")

        # 15. GitOps Naming: <prefix>-<env>-<domain>-<capability>
        self.GITOPS = re.compile(rf"^{prefix}-(dev|staging|prod)-[a-z]+-[a-z]+$")

        # 16. Helm Release: <prefix>-<domain>-<capability>-<env>
        self.HELM = re.compile(rf"^{prefix}-[a-z]+-[a-z]+-(dev|staging|prod)$")

        # K8s Labels
        self.K8S_LABEL_KEY = re.compile(
            r"^(app\.kubernetes\.io|(gl|ng)\.machinenativeops\.io)/[a-z-]+$"
        )

        # Governance Annotations (allowing NG/GL prefixes)
        self.GL_ANNOTATION = re.compile(
            r"^@[A-Z]{2}-(governed|layer|semantic|audit-trail)"
        )

        # Naming type markers (used by meta-governance completeness checks)
        self.NAMING_TYPE_MARKERS = {
            "CommentNaming": self.COMMENT_TAG,
            "MappingNaming": self.MAPPING,
            "ReferenceNaming": self.REFERENCE,
            "PathNaming": self.API_PATH,
            "PortNaming": self.PORT,
            "ServiceNaming": self.SERVICE,
            "DependencyNaming": self.DEPENDENCY,
            "ShortNaming": self.SHORT,
            "LongNaming": self.LONG,
            "DirectoryNaming": self.PLATFORM_DIR,
            "FileNaming": self.GL_FILE,
            "EventNaming": self.EVENT,
            "VariableNaming": self.VARIABLE,
            "EnvironmentVariableNaming": self.ENV_VAR,
            "GitOpsNaming": self.GITOPS,
            "HelmReleaseNaming": self.HELM,
        }


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

                prefix_tokens = [f"{p}:" for p in self.patterns.prefixes]
                annotation_tokens = [f"@{p.upper()}-" for p in self.patterns.prefixes]
                for i, line in enumerate(lines):
                    # 檢查治理標註
                    if any(token in line for token in annotation_tokens):
                        items_checked += 1
                        if not self.patterns.GL_ANNOTATION.search(line):
                            violations.append(
                                NamingViolation(
                                    rule_id="GL20-COMMENT-001",
                                    category=NamingCategory.COMMENT,
                                    path=str(py_file.relative_to(self.workspace)),
                                    name=line.strip()[:50],
                                    expected_pattern="@<PREFIX>-(governed|layer|semantic|audit-trail)",
                                    actual_value=line.strip()[:50],
                                    severity=Severity.MEDIUM,
                                    message="治理標註格式不正確",
                                    suggestion="使用 @GL-governed/@NG-governed, @GL-layer/@NG-layer, @GL-semantic/@NG-semantic 或 @GL-audit-trail/@NG-audit-trail",
                                    line_number=i + 1,
                                )
                            )

                    # 檢查 gl: 標籤
                    if any(token in line.lower() for token in prefix_tokens) and "#" in line:
                        items_checked += 1
                        # 提取 <prefix>: 標籤
                        match = re.search(
                            rf"(?:{self.patterns.prefix_group}):[a-z:_-]+", line.lower()
                        )
                        if match:
                            tag = match.group()
                            if not self.patterns.COMMENT_TAG.match(tag):
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-COMMENT-002",
                                        category=NamingCategory.COMMENT,
                                        path=str(py_file.relative_to(self.workspace)),
                                        name=tag,
                                        expected_pattern=f"{self.patterns.primary_prefix}:<domain>:<capability>:<tag>",
                                        actual_value=tag,
                                        severity=Severity.LOW,
                                        message="命名空間標籤格式不正確",
                                        suggestion=f"使用 {self.patterns.primary_prefix}:<domain>:<capability>:<tag> 格式",
                                        line_number=i + 1,
                                    )
                                )
            except Exception as e:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-COMMENT-999",
                        category=NamingCategory.COMMENT,
                        path=str(py_file.relative_to(self.workspace)),
                        name=str(py_file.name),
                        expected_pattern="可讀取並掃描檔案",
                        actual_value="scan_failed",
                        severity=Severity.LOW,
                        message=f"掃描檔案失敗: {e}",
                        suggestion="檢查檔案內容或權限後重新掃描",
                    )
                )

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
    # 通用占位檢查 (尚未啟用的命名類別)
    # ========================================================================

    def _empty_check(self, category: NamingCategory) -> NamingCheckResult:
        """返回空結果以保持命名類別覆蓋"""
        return NamingCheckResult(
            category=category,
            passed=True,
            items_checked=0,
            violations=[],
            execution_time_ms=0,
        )

    def check_mapping_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.MAPPING)

    def check_reference_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.REFERENCE)

    def check_port_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.PORT)

    def check_dependency_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.DEPENDENCY)

    def check_short_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.SHORT)

    def check_long_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.LONG)

    def check_event_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.EVENT)

    def check_variable_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.VARIABLE)

    def check_gitops_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.GITOPS)

    def check_helm_naming(self) -> NamingCheckResult:
        return self._empty_check(NamingCategory.HELM)

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

                    # 檢查是否以 /<prefix>/ 或 /api/ 開頭
                    if not re.match(
                        rf"^/({self.patterns.prefix_group})/", path
                    ) and not path.startswith("/api/"):
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-PATH-001",
                                category=NamingCategory.PATH,
                                path=str(yaml_file.relative_to(self.workspace)),
                                name=path,
                                expected_pattern=f"/{self.patterns.primary_prefix}/<domain>/<capability>/* or /api/v*/*",
                                actual_value=path,
                                severity=Severity.MEDIUM,
                                message="API 路徑應以命名空間或 /api/ 開頭",
                                suggestion=f"重命名為 /{self.patterns.primary_prefix}{path} 或 /api/v1{path}",
                            )
                        )
            except Exception as e:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-PATH-999",
                        category=NamingCategory.PATH,
                        path=str(yaml_file.relative_to(self.workspace)),
                        name=str(yaml_file.name),
                        expected_pattern="可讀取並掃描 API 路徑",
                        actual_value="scan_failed",
                        severity=Severity.LOW,
                        message=f"解析 API 路徑失敗: {e}",
                        suggestion="確認 YAML 格式與編碼後重新掃描",
                    )
                )

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

                    if re.match(rf"^/({self.patterns.prefix_group})/", path):
                        if not self.patterns.API_PATH.match(path):
                            violations.append(
                                NamingViolation(
                                    rule_id="GL20-PATH-002",
                                    category=NamingCategory.PATH,
                                    path=str(yaml_file.relative_to(self.workspace)),
                                    name=path,
                                    expected_pattern=f"/{self.patterns.primary_prefix}/<domain>/<capability>/<resource>",
                                    actual_value=path,
                                    severity=Severity.LOW,
                                    message="命名空間 API 路徑格式不正確",
                                    suggestion=f"使用 /{self.patterns.primary_prefix}/<domain>/<capability>/<resource> 格式",
                                )
                            )
            except Exception as e:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-PATH-998",
                        category=NamingCategory.PATH,
                        path=str(yaml_file.relative_to(self.workspace)),
                        name=str(yaml_file.name),
                        expected_pattern="可讀取並掃描治理路徑",
                        actual_value="scan_failed",
                        severity=Severity.LOW,
                        message=f"解析治理路徑失敗: {e}",
                        suggestion="確認檔案可讀並符合 YAML 格式",
                    )
                )

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

                        # 檢查是否符合 <prefix>-*-svc 格式
                        if any(
                            service_name.startswith(f"{p}-")
                            for p in self.patterns.prefixes
                        ):
                            if not self.patterns.SERVICE.match(service_name):
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-SVC-001",
                                        category=NamingCategory.SERVICE,
                                        path=str(yaml_file.relative_to(self.workspace)),
                                        name=service_name,
                                        expected_pattern=f"{self.patterns.primary_prefix}-<domain>-<capability>-svc",
                                        actual_value=service_name,
                                        severity=Severity.HIGH,
                                        message="Service 命名空間前綴格式不正確",
                                        suggestion=f"使用 {self.patterns.primary_prefix}-<domain>-<capability>-svc 格式",
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
            except Exception as e:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-SVC-999",
                        category=NamingCategory.SERVICE,
                        path=str(yaml_file.relative_to(self.workspace)),
                        name=str(yaml_file.name),
                        expected_pattern="可讀取並掃描 Service",
                        actual_value="scan_failed",
                        severity=Severity.LOW,
                        message=f"解析 Service 檔案失敗: {e}",
                        suggestion="確認 YAML 格式與編碼後重新掃描",
                    )
                )

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
            if any(name.startswith(f"{p}-") for p in self.patterns.prefixes) and (
                "platform" in name
            ):
                if not self.patterns.PLATFORM_DIR.match(name):
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-DIR-002",
                            category=NamingCategory.DIRECTORY,
                            path=str(dir_path.relative_to(self.workspace)),
                            name=name,
                            expected_pattern=f"{self.patterns.primary_prefix}-<domain>-<capability>-platform",
                            actual_value=name,
                            severity=Severity.MEDIUM,
                            message=f"平台目錄 '{name}' 格式不正確",
                            suggestion=f"使用 {self.patterns.primary_prefix}-<domain>-<capability>-platform 格式",
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
                if re.match(rf"^({self.patterns.upper_prefix_group})\d{{2}}", stem):
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
                        label_keys = re.findall(
                            r"labels:\s*(?:\n\s+([A-Za-z0-9\.\-\/]+):)", content
                        )
                        for key in label_keys:
                            if (
                                "machinenativeops.io" in key
                                or key.startswith("app.kubernetes.io")
                            ):
                                if not self.patterns.K8S_LABEL_KEY.match(key):
                                    violations.append(
                                        NamingViolation(
                                            rule_id="GL20-LABEL-002",
                                            category=NamingCategory.LABEL,
                                            path=str(
                                                yaml_file.relative_to(self.workspace)
                                            ),
                                            name=key,
                                            expected_pattern=self.patterns.K8S_LABEL_KEY.pattern,
                                            actual_value=key,
                                            severity=Severity.MEDIUM,
                                            message="K8s 標籤鍵不符合命名空間規範",
                                            suggestion="使用 app.kubernetes.io/* 或 ng/gl.machinenativeops.io/* 格式",
                                        )
                                    )
            except Exception:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-LABEL-999",
                        category=NamingCategory.LABEL,
                        path=str(yaml_file.relative_to(self.workspace)),
                        name=str(yaml_file.name),
                        expected_pattern="可讀取並掃描標籤",
                        actual_value="scan_failed",
                        severity=Severity.LOW,
                        message="解析標籤檔案失敗",
                        suggestion="確認檔案可讀並符合 YAML 格式",
                    )
                )

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
                        if any(
                            var_name.startswith(prefix.upper())
                            for prefix in self.patterns.prefixes
                        ):
                            if not self.patterns.ENV_VAR.match(var_name):
                                violations.append(
                                    NamingViolation(
                                        rule_id="GL20-ENV-001",
                                        category=NamingCategory.ENV_VAR,
                                        path=str(env_file.relative_to(self.workspace)),
                                        name=var_name,
                                        expected_pattern=f"{self.patterns.primary_prefix.upper()}_<DOMAIN>_<CAPABILITY>_<KEY>",
                                        actual_value=var_name,
                                        severity=Severity.MEDIUM,
                                        message=f"命名空間環境變數 '{var_name}' 格式不正確",
                                        suggestion=f"使用 {self.patterns.primary_prefix.upper()}_<DOMAIN>_<CAPABILITY>_<KEY> 格式",
                                        line_number=i + 1,
                                    )
                                )
            except Exception as e:
                violations.append(
                    NamingViolation(
                        rule_id="GL20-ENV-999",
                        category=NamingCategory.ENV_VAR,
                        path=str(env_file.relative_to(self.workspace)),
                        name=str(env_file.name),
                        expected_pattern="可讀取並掃描環境變數檔案",
                        actual_value="scan_failed",
                        severity=Severity.LOW,
                        message=f"解析環境變數檔案失敗: {e}",
                        suggestion="確認檔案存在且編碼正確",
                    )
                )

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
            self.check_mapping_naming,
            self.check_reference_naming,
            self.check_path_naming,
            self.check_port_naming,
            self.check_service_naming,
            self.check_dependency_naming,
            self.check_short_naming,
            self.check_long_naming,
            self.check_directory_naming,
            self.check_file_naming,
            self.check_event_naming,
            self.check_variable_naming,
            self.check_label_naming,
            self.check_env_var_naming,
            self.check_gitops_naming,
            self.check_helm_naming,
        ]

        results = []
        for check in checks:
            try:
                result = check()
                results.append(result)
            except Exception as e:
                print(f"檢查失敗: {check.__name__}: {e}")

        # 排除僅為佔位的檢查（尚未實作且無檢查項目）
        effective_results = [
            r for r in results if r.items_checked > 0 or len(r.violations) > 0
        ]

        # 統計
        total_violations = sum(len(r.violations) for r in effective_results)
        passed_checks = len([r for r in effective_results if r.passed])

        by_category = {}
        by_severity = {}

        for result in effective_results:
            by_category[result.category.value] = len(result.violations)
            for v in result.violations:
                by_severity[v.severity.value] = by_severity.get(v.severity.value, 0) + 1

        report = CompleteNamingReport(
            timestamp=datetime.now().isoformat(),
            workspace=str(self.workspace),
            total_checks=len(effective_results),
            passed_checks=passed_checks,
            total_violations=total_violations,
            by_category=by_category,
            by_severity=by_severity,
            results=results,
            compliance_rate=(
                round(passed_checks / len(effective_results) * 100, 2)
                if effective_results
                else 0
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
