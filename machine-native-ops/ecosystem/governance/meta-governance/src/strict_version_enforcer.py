#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: version-enforcement
# @GL-audit-trail: ../../GL_SEMANTIC_ANCHOR.json
#
"""
Strict Version Enforcer
=======================
嚴格版本執行器 - 航空適航級版本管理

Standards: DO-178C, ISO 9001, CCAR-21/R3
Enforcement Level: STRICT
"""

import re
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging


@dataclass
class VersionValidation:
    """版本驗證結果"""
    valid: bool
    version: str
    errors: List[str]
    warnings: List[str]
    compliance_level: str  # COMPLIANT, NON_COMPLIANT, REQUIRES_REVIEW


class StrictVersionEnforcer:
    """嚴格版本執行器"""
    
    # SemVer 正則表達式（完整版）
    SEMVER_PATTERN = re.compile(
        r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
        r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    )
    
    PRERELEASE_PATTERN = re.compile(r'^(alpha|beta|rc)\.(0|[1-9]\d*)$')
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 版本註冊表: {spec_id: [versions]}
        self._registry: Dict[str, List[str]] = {}
        
        # 版本哈希: {spec_id: {version: hash}}
        self._hashes: Dict[str, Dict[str, str]] = {}
        
        # 版本簽名: {spec_id: {version: signature}}
        self._signatures: Dict[str, Dict[str, str]] = {}
        
        self.logger.info("Strict Version Enforcer initialized (Airworthiness-Grade)")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('StrictVersionEnforcer')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def validate_version_format(self, version: str) -> VersionValidation:
        """
        驗證版本格式（嚴格）
        
        Args:
            version: 版本字符串
            
        Returns:
            驗證結果
        """
        errors = []
        warnings = []
        
        # 格式驗證
        if not self.SEMVER_PATTERN.match(version):
            errors.append(f"版本格式不符合 SemVer 規範: {version}")
            return VersionValidation(
                valid=False,
                version=version,
                errors=errors,
                warnings=warnings,
                compliance_level="NON_COMPLIANT"
            )
        
        # 解析版本
        match = self.SEMVER_PATTERN.match(version)
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        prerelease = match.group(4)
        build = match.group(5)
        
        # 檢查前導零
        if version.startswith('0') and major != 0:
            errors.append("主版本號不允許前導零")
        
        # 檢查預發布標識
        if prerelease:
            if not self.PRERELEASE_PATTERN.match(prerelease):
                errors.append(
                    f"預發布標識必須為 alpha.N, beta.N 或 rc.N 格式: {prerelease}"
                )
        
        # 開發版本警告
        if major == 0:
            warnings.append("版本 0.x.x 僅應用於初始開發")
        
        return VersionValidation(
            valid=len(errors) == 0,
            version=version,
            errors=errors,
            warnings=warnings,
            compliance_level="COMPLIANT" if not errors else "NON_COMPLIANT"
        )
    
    def validate_version_sequence(
        self,
        spec_id: str,
        new_version: str
    ) -> VersionValidation:
        """
        驗證版本序列連續性（禁止跳過）
        
        Args:
            spec_id: 規範ID
            new_version: 新版本
            
        Returns:
            驗證結果
        """
        errors = []
        warnings = []
        
        # 獲取已有版本
        existing_versions = sorted(
            self._registry.get(spec_id, []),
            key=lambda v: self._version_to_tuple(v)
        )
        
        if not existing_versions:
            # 首次發布，必須是 1.0.0
            if new_version != "1.0.0":
                warnings.append(
                    f"首次發布建議使用 1.0.0，當前: {new_version}"
                )
            
            return VersionValidation(
                valid=True,
                version=new_version,
                errors=errors,
                warnings=warnings,
                compliance_level="COMPLIANT"
            )
        
        latest = existing_versions[-1]
        latest_tuple = self._version_to_tuple(latest)
        new_tuple = self._version_to_tuple(new_version)
        
        # 檢查連續性
        major_diff = new_tuple[0] - latest_tuple[0]
        minor_diff = new_tuple[1] - latest_tuple[1]
        patch_diff = new_tuple[2] - latest_tuple[2]
        
        if major_diff > 1:
            errors.append(
                f"主版本跳躍: {latest} → {new_version} "
                f"(跳過 {major_diff - 1} 個主版本)"
            )
        
        elif major_diff == 1:
            if new_tuple[1] != 0 or new_tuple[2] != 0:
                errors.append(
                    f"主版本升級必須重置為 X.0.0: {new_version}"
                )
        
        elif major_diff == 0:
            if minor_diff > 1:
                errors.append(
                    f"次版本跳躍: {latest} → {new_version} "
                    f"(跳過 {minor_diff - 1} 個次版本)"
                )
            
            elif minor_diff == 1:
                if new_tuple[2] != 0:
                    errors.append(
                        f"次版本升級必須重置修訂號為 0: {new_version}"
                    )
            
            elif minor_diff == 0:
                if patch_diff > 1:
                    errors.append(
                        f"修訂版本跳躍: {latest} → {new_version} "
                        f"(跳過 {patch_diff - 1} 個修訂)"
                    )
                
                elif patch_diff <= 0:
                    errors.append(
                        f"版本號必須遞增: {latest} → {new_version}"
                    )
        
        return VersionValidation(
            valid=len(errors) == 0,
            version=new_version,
            errors=errors,
            warnings=warnings,
            compliance_level="COMPLIANT" if not errors else "NON_COMPLIANT"
        )
    
    def register_version(
        self,
        spec_id: str,
        version: str,
        content_hash: str,
        signature: str
    ) -> bool:
        """
        註冊版本（帶簽名和哈希驗證）
        
        Args:
            spec_id: 規範ID
            version: 版本號
            content_hash: 內容哈希
            signature: 數字簽名
            
        Returns:
            註冊成功返回True
        """
        # 1. 格式驗證
        format_val = self.validate_version_format(version)
        if not format_val.valid:
            self.logger.error(
                f"版本格式驗證失敗: {spec_id} {version}\n"
                f"錯誤: {format_val.errors}"
            )
            return False
        
        # 2. 序列驗證
        sequence_val = self.validate_version_sequence(spec_id, version)
        if not sequence_val.valid:
            self.logger.error(
                f"版本序列驗證失敗: {spec_id} {version}\n"
                f"錯誤: {sequence_val.errors}"
            )
            return False
        
        # 3. 註冊版本
        if spec_id not in self._registry:
            self._registry[spec_id] = []
        
        if version in self._registry[spec_id]:
            self.logger.error(
                f"版本已存在（禁止重用）: {spec_id} {version}"
            )
            return False
        
        self._registry[spec_id].append(version)
        
        # 4. 保存哈希和簽名
        if spec_id not in self._hashes:
            self._hashes[spec_id] = {}
        self._hashes[spec_id][version] = content_hash
        
        if spec_id not in self._signatures:
            self._signatures[spec_id] = {}
        self._signatures[spec_id][version] = signature
        
        self.logger.info(
            f"版本已註冊: {spec_id} v{version} "
            f"(hash: {content_hash[:16]}...)"
        )
        
        return True
    
    def verify_version_integrity(
        self,
        spec_id: str,
        version: str,
        content: str
    ) -> bool:
        """
        驗證版本完整性（哈希驗證）
        
        Args:
            spec_id: 規範ID
            version: 版本號
            content: 內容
            
        Returns:
            驗證通過返回True
        """
        # 計算內容哈希
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # 獲取註冊的哈希
        registered_hash = self._hashes.get(spec_id, {}).get(version)
        
        if not registered_hash:
            self.logger.warning(
                f"版本未註冊: {spec_id} {version}"
            )
            return False
        
        if content_hash != registered_hash:
            self.logger.error(
                f"哈希驗證失敗: {spec_id} {version}\n"
                f"預期: {registered_hash}\n"
                f"實際: {content_hash}"
            )
            return False
        
        return True
    
    def check_compatibility(
        self,
        spec_id: str,
        current_version: str,
        target_version: str
    ) -> Dict[str, any]:
        """
        檢查版本兼容性
        
        Args:
            spec_id: 規範ID
            current_version: 當前版本
            target_version: 目標版本
            
        Returns:
            兼容性分析結果
        """
        current = self._version_to_tuple(current_version)
        target = self._version_to_tuple(target_version)
        
        # MAJOR版本變更
        if target[0] > current[0]:
            return {
                'compatible': False,
                'change_type': 'MAJOR',
                'breaking': True,
                'action_required': 'migration',
                'timeline_days': 90,
                'requirements': [
                    '完成下游驗證器重新審查',
                    '發布遷移指南',
                    '進行影響評估',
                    '建立遷移支援通道'
                ]
            }
        
        # MINOR版本變更
        elif target[1] > current[1]:
            return {
                'compatible': True,
                'change_type': 'MINOR',
                'breaking': False,
                'action_required': 'TESTING',
                'timeline_days': 30,
                'requirements': [
                    '執行兼容性測試',
                    '驗證新功能',
                    '確認回退機制'
                ]
            }
        
        # PATCH版本變更
        elif target[2] > current[2]:
            return {
                'compatible': True,
                'change_type': 'PATCH',
                'breaking': False,
                'action_required': 'REVIEW',
                'timeline_days': 7,
                'requirements': [
                    '審查變更內容',
                    '驗證無功能變更',
                    '立即可升級'
                ]
            }
        
        # 降級或無變更
        else:
            return {
                'compatible': False,
                'change_type': 'DOWNGRADE' if target < current else 'NO_CHANGE',
                'breaking': target < current,
                'action_required': 'REJECT',
                'requirements': ['不支持版本降級']
            }
    
    def _version_to_tuple(self, version: str) -> Tuple[int, int, int]:
        """將版本字符串轉換為元組"""
        match = self.SEMVER_PATTERN.match(version)
        if not match:
            return (0, 0, 0)
        
        return (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3))
        )
    
    def generate_version_hash(self, content: str) -> str:
        """生成版本內容哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def validate_production_deployment(
        self,
        version: str,
        environment: str
    ) -> bool:
        """
        驗證生產部署（禁止開發版本）
        
        Args:
            version: 版本號
            environment: 環境名稱
            
        Returns:
            允許部署返回True
        """
        if environment != 'production':
            return True
        
        # 生產環境檢查
        if '-' in version:
            self.logger.error(
                f"生產環境禁止使用預發布版本: {version}"
            )
            return False
        
        if any(prefix in version for prefix in ['dev-', 'feat-', 'ci-', 'nightly-']):
            self.logger.error(
                f"生產環境禁止使用開發版本: {version}"
            )
            return False
        
        return True
    
    def enforce_version_immutability(
        self,
        spec_id: str,
        version: str,
        new_content: str
    ) -> bool:
        """
        強制版本不可變性
        
        Args:
            spec_id: 規範ID
            version: 版本號
            new_content: 新內容
            
        Returns:
            允許修改返回True
        """
        # 檢查版本是否已註冊
        if version in self._registry.get(spec_id, []):
            self.logger.error(
                f"已發布版本禁止修改: {spec_id} {version}\n"
                f"請創建新版本"
            )
            return False
        
        return True
    
    def calculate_version_health_score(
        self,
        spec_id: str,
        version: str,
        usage_data: Optional[Dict] = None
    ) -> float:
        """
        計算版本健康度（0-100）
        
        Args:
            spec_id: 規範ID
            version: 版本號
            usage_data: 使用數據
            
        Returns:
            健康度分數
        """
        score = 100.0
        
        usage_data = usage_data or {}
        
        # 版本年齡懲罰
        if 'published_date' in usage_data:
            days_old = (datetime.utcnow() - usage_data['published_date']).days
            if days_old > 365:
                score -= 20  # 超過1年 -20分
            elif days_old > 180:
                score -= 10  # 超過半年 -10分
        
        # 已知問題懲罰
        if 'known_issues' in usage_data:
            critical = usage_data['known_issues'].get('critical', 0)
            high = usage_data['known_issues'].get('high', 0)
            
            score -= critical * 15  # 每個嚴重問題 -15分
            score -= high * 5       # 每個高級問題 -5分
        
        # 採用率加分
        if 'adoption_rate' in usage_data:
            if usage_data['adoption_rate'] > 0.8:
                score += 10  # 高採用率 +10分
            elif usage_data['adoption_rate'] < 0.2:
                score -= 10  # 低採用率 -10分
        
        return max(0.0, min(100.0, score))
