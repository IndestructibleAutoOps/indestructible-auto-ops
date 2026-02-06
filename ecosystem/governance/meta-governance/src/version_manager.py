#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: governance
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Version Manager
==================
版本管理器 - 語義化版本控制

GL Governance Layer: GL90-99 (Meta-Specification Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging


class VersionType(Enum):
    """版本類型"""

    MAJOR = "major"  # 破壞性變更
    MINOR = "minor"  # 向後兼容的功能新增
    PATCH = "patch"  # 向後兼容的缺陷修復


class ReleaseType(Enum):
    """發布類型"""

    STABLE = "stable"  # 穩定版本
    BETA = "beta"  # 測試版本
    ALPHA = "alpha"  # 早期版本
    RC = "rc"  # 候選版本
    LTS = "lts"  # 長期支持版本


@dataclass
class SemanticVersion:
    """語義化版本"""

    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None  # alpha, beta, rc
    build: Optional[str] = None

    def __str__(self) -> str:
        """字符串表示"""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    def __lt__(self, other: "SemanticVersion") -> bool:
        """比較版本"""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        return False

    @classmethod
    def parse(cls, version_str: str) -> "SemanticVersion":
        """解析版本字符串"""
        # 匹配 SemVer 格式: major.minor.patch[-prerelease][+build]
        pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?$"
        match = re.match(pattern, version_str)

        if not match:
            raise ValueError(f"Invalid version format: {version_str}")

        return cls(
            major=int(match.group(1)),
            minor=int(match.group(2)),
            patch=int(match.group(3)),
            prerelease=match.group(4),
            build=match.group(5),
        )


@dataclass
class VersionMetadata:
    """版本元數據"""

    version: SemanticVersion
    component: str
    release_type: ReleaseType
    release_date: str
    changes: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    deprecations: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    contributors: List[str] = field(default_factory=list)
    reviewed_by: List[str] = field(default_factory=list)
    approved_by: Optional[str] = None


class VersionManager:
    """版本管理器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化版本管理器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()

        # 版本歷史: {component: [VersionMetadata]}
        self._versions: Dict[str, List[VersionMetadata]] = {}

        # LTS 版本: {component: version_string}
        self._lts_versions: Dict[str, str] = {}

        self.logger.info("Version Manager initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("VersionManager")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def create_version(
        self,
        component: str,
        version_type: str,
        changes: List[str],
        breaking_changes: Optional[List[str]] = None,
        release_type: str = "stable",
    ) -> VersionMetadata:
        """
        創建新版本

        Args:
            component: 組件名稱
            version_type: 版本類型（major, minor, patch）
            changes: 變更列表
            breaking_changes: 破壞性變更列表
            release_type: 發布類型

        Returns:
            版本元數據
        """
        # 獲取當前版本
        current = self.get_latest_version(component)

        if current is None:
            # 首次發布
            new_version = SemanticVersion(1, 0, 0)
        else:
            # 計算新版本
            new_version = self._calculate_next_version(
                current.version, VersionType(version_type)
            )

        # 創建版本元數據
        metadata = VersionMetadata(
            version=new_version,
            component=component,
            release_type=ReleaseType(release_type),
            release_date=datetime.utcnow().isoformat(),
            changes=changes,
            breaking_changes=breaking_changes or [],
        )

        # 保存版本
        if component not in self._versions:
            self._versions[component] = []

        self._versions[component].append(metadata)

        self.logger.info(
            f"Version created: {component} v{new_version} "
            f"({len(changes)} changes, {len(metadata.breaking_changes)} breaking)"
        )

        return metadata

    def _calculate_next_version(
        self, current: SemanticVersion, version_type: VersionType
    ) -> SemanticVersion:
        """
        計算下一個版本號

        Args:
            current: 當前版本
            version_type: 版本類型

        Returns:
            新版本
        """
        if version_type == VersionType.MAJOR:
            return SemanticVersion(current.major + 1, 0, 0)
        elif version_type == VersionType.MINOR:
            return SemanticVersion(current.major, current.minor + 1, 0)
        else:  # PATCH
            return SemanticVersion(current.major, current.minor, current.patch + 1)

    def get_latest_version(self, component: str) -> Optional[VersionMetadata]:
        """
        獲取最新版本

        Args:
            component: 組件名稱

        Returns:
            最新版本元數據或None
        """
        versions = self._versions.get(component, [])
        if not versions:
            return None

        # 返回版本號最大的
        return max(versions, key=lambda v: v.version)

    def get_version(self, component: str, version: str) -> Optional[VersionMetadata]:
        """
        獲取特定版本

        Args:
            component: 組件名稱
            version: 版本字符串

        Returns:
            版本元數據或None
        """
        try:
            target_version = SemanticVersion.parse(version)
        except ValueError:
            return None

        versions = self._versions.get(component, [])
        for v in versions:
            if str(v.version) == str(target_version):
                return v

        return None

    def list_versions(
        self, component: str, release_type: Optional[str] = None
    ) -> List[VersionMetadata]:
        """
        列出版本

        Args:
            component: 組件名稱
            release_type: 發布類型過濾

        Returns:
            版本列表
        """
        versions = self._versions.get(component, [])

        if release_type:
            rt = ReleaseType(release_type)
            versions = [v for v in versions if v.release_type == rt]

        return sorted(versions, key=lambda v: v.version, reverse=True)

    def set_lts_version(self, component: str, version: str) -> bool:
        """
        設置 LTS 版本

        Args:
            component: 組件名稱
            version: 版本字符串

        Returns:
            成功返回True
        """
        # 驗證版本存在
        if not self.get_version(component, version):
            self.logger.error(f"Version not found: {component} {version}")
            return False

        self._lts_versions[component] = version
        self.logger.info(f"LTS version set: {component} -> {version}")

        return True

    def get_lts_version(self, component: str) -> Optional[str]:
        """獲取 LTS 版本"""
        return self._lts_versions.get(component)

    def validate_version(self, metadata: VersionMetadata) -> Dict[str, Any]:
        """
        驗證版本

        Args:
            metadata: 版本元數據

        Returns:
            驗證結果
        """
        errors = []
        warnings = []

        # 檢查破壞性變更
        if metadata.breaking_changes:
            if metadata.version.major == 0:
                warnings.append("Major version is 0, but has breaking changes")

        # 檢查版本號合理性
        if metadata.version.major == 0 and metadata.version.minor == 0:
            warnings.append("Version 0.0.x should only be used for initial development")

        # 檢查變更記錄
        if not metadata.changes and metadata.version.patch > 0:
            warnings.append("No changes listed for patch version")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def generate_changelog(
        self,
        component: str,
        from_version: Optional[str] = None,
        to_version: Optional[str] = None,
    ) -> str:
        """
        生成變更日誌

        Args:
            component: 組件名稱
            from_version: 起始版本
            to_version: 結束版本

        Returns:
            變更日誌文本
        """
        versions = self.list_versions(component)

        # 過濾版本範圍
        if from_version:
            from_ver = SemanticVersion.parse(from_version)
            versions = [v for v in versions if v.version > from_ver]

        if to_version:
            to_ver = SemanticVersion.parse(to_version)
            versions = [v for v in versions if v.version <= to_ver]

        # 生成日誌
        changelog = []
        changelog.append(f"# Changelog - {component}")
        changelog.append("")

        for metadata in versions:
            changelog.append(f"## [{metadata.version}] - {metadata.release_date[:10]}")
            changelog.append("")

            if metadata.breaking_changes:
                changelog.append("### ⚠️ Breaking Changes")
                for change in metadata.breaking_changes:
                    changelog.append(f"- {change}")
                changelog.append("")

            if metadata.changes:
                changelog.append("### Changes")
                for change in metadata.changes:
                    changelog.append(f"- {change}")
                changelog.append("")

            if metadata.deprecations:
                changelog.append("### Deprecations")
                for dep in metadata.deprecations:
                    changelog.append(f"- {dep}")
                changelog.append("")

        return "\n".join(changelog)

    def check_compatibility(
        self, component: str, current_version: str, target_version: str
    ) -> Dict[str, Any]:
        """
        檢查版本兼容性

        Args:
            component: 組件名稱
            current_version: 當前版本
            target_version: 目標版本

        Returns:
            兼容性分析結果
        """
        try:
            current = SemanticVersion.parse(current_version)
            target = SemanticVersion.parse(target_version)
        except ValueError as e:
            return {"compatible": False, "error": str(e)}

        # 檢查主版本
        if target.major > current.major:
            return {
                "compatible": False,
                "reason": "Major version upgrade - may contain breaking changes",
                "recommendation": "Review migration guide and test thoroughly",
            }

        # 檢查次版本
        if target.major == current.major and target.minor > current.minor:
            return {
                "compatible": True,
                "reason": "Minor version upgrade - backward compatible",
                "recommendation": "Safe to upgrade, but test new features",
            }

        # 檢查修訂版本
        if target.major == current.major and target.minor == current.minor:
            return {
                "compatible": True,
                "reason": "Patch version upgrade - bug fixes only",
                "recommendation": "Safe to upgrade immediately",
            }

        # 降級
        if target < current:
            return {
                "compatible": False,
                "reason": "Version downgrade detected",
                "recommendation": "Downgrade not recommended",
            }

        return {"compatible": True}

    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        total_versions = sum(len(versions) for versions in self._versions.values())

        return {
            "total_components": len(self._versions),
            "total_versions": total_versions,
            "lts_versions": len(self._lts_versions),
            "components": list(self._versions.keys()),
        }
