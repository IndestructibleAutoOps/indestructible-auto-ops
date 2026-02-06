#!/usr/bin/env python3
"""
NG 嚴格執行器（零容忍）
NG Strict Enforcer - Zero Tolerance Mode

NG Code: NG00004
Purpose: IndestructibleAutoOps 零容忍執行器

絕對規則：
- 任何違規 = 立即阻斷
- 無警告，只有阻斷
- 無建議，只有強制
- 無例外，無寬容
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ViolationSeverity(Enum):
    """違規嚴重性（零容忍分級）"""
    IMMUTABLE = "IMMUTABLE"          # 憲法級 - 永久阻斷
    ABSOLUTE = "ABSOLUTE"            # 絕對級 - 立即阻斷
    STRICT = "STRICT"                # 嚴格級 - 阻斷並警報
    MANDATORY = "MANDATORY"          # 強制級 - 阻斷直到修復


class EnforcementAction(Enum):
    """執行動作（零容忍）"""
    PERMANENT_BLOCK = "permanent_block"                    # 永久阻斷
    IMMEDIATE_BLOCK = "immediate_block"                    # 立即阻斷
    BLOCK_AND_ROLLBACK = "block_and_rollback"             # 阻斷並回滾
    BLOCK_AND_ALERT = "block_and_alert"                   # 阻斷並警報
    BLOCK_UNTIL_FIXED = "block_until_fixed"               # 阻斷直到修復
    FREEZE_SYSTEM = "freeze_system"                       # 凍結系統
    TRIGGER_EMERGENCY = "trigger_emergency"               # 觸發緊急狀態


@dataclass
class StrictViolation:
    """嚴格違規記錄"""
    violation_id: str
    namespace_id: str
    rule_code: str
    severity: ViolationSeverity
    action: EnforcementAction
    description: str
    detected_at: str
    blocked: bool = True
    immutable: bool = True


class NgStrictEnforcer:
    """
    NG 嚴格執行器
    
    IndestructibleAutoOps 零容忍執行模式：
    - 100% 驗證通過率要求
    - 0% 違規容忍
    - 立即阻斷機制
    - 不可變審計
    """
    
    def __init__(self, zero_tolerance_mode: bool = True):
        """
        初始化嚴格執行器
        
        Args:
            zero_tolerance_mode: 零容忍模式（只能是 True）
        """
        if not zero_tolerance_mode:
            raise ValueError("FORBIDDEN: IndestructibleAutoOps 必須使用零容忍模式")
        
        self.zero_tolerance_mode = True
        self.violations: List[StrictViolation] = []
        self.blocked_operations: List[str] = []
        self.enforcement_metrics = {
            'total_checks': 0,
            'total_blocks': 0,
            'block_rate': 0.0
        }
        
        logger.info("🛡️  NG 嚴格執行器已啟動 [ZERO_TOLERANCE_MODE]")
    
    def enforce_uniqueness(
        self,
        namespace_id: str,
        existing_namespaces: List[str]
    ) -> Tuple[bool, Optional[StrictViolation]]:
        """
        強制唯一性（零容忍）
        
        Returns:
            (通過, 違規記錄或None)
        """
        self.enforcement_metrics['total_checks'] += 1
        
        # 檢查完全匹配
        if namespace_id in existing_namespaces:
            violation = StrictViolation(
                violation_id=f"uniq-{len(self.violations)}",
                namespace_id=namespace_id,
                rule_code="NG00301",
                severity=ViolationSeverity.IMMUTABLE,
                action=EnforcementAction.PERMANENT_BLOCK,
                description=f"命名空間已存在: {namespace_id}",
                detected_at=datetime.now().isoformat(),
                blocked=True,
                immutable=True
            )
            
            self.violations.append(violation)
            self.blocked_operations.append(namespace_id)
            self.enforcement_metrics['total_blocks'] += 1
            
            logger.critical(
                f"🚨 PERMANENT_BLOCK: 命名空間重複 {namespace_id}"
            )
            
            return (False, violation)
        
        # 零容忍：檢查語義相似度（防止混淆）
        for existing in existing_namespaces:
            similarity = self._calculate_similarity(namespace_id, existing)
            
            if similarity >= 0.80:  # 80% 以上視為太相似
                violation = StrictViolation(
                    violation_id=f"sim-{len(self.violations)}",
                    namespace_id=namespace_id,
                    rule_code="NG00301",
                    severity=ViolationSeverity.ABSOLUTE,
                    action=EnforcementAction.IMMEDIATE_BLOCK,
                    description=f"語義相似度過高 {similarity:.0%} 與 {existing}",
                    detected_at=datetime.now().isoformat()
                )
                
                self.violations.append(violation)
                self.blocked_operations.append(namespace_id)
                self.enforcement_metrics['total_blocks'] += 1
                
                logger.error(
                    f"🚨 IMMEDIATE_BLOCK: 語義相似 {namespace_id} ≈ {existing} ({similarity:.0%})"
                )
                
                return (False, violation)
        
        return (True, None)
    
    def _calculate_similarity(self, ns1: str, ns2: str) -> float:
        """計算語義相似度（簡化版）"""
        # 簡單的 Levenshtein 距離
        ns1_parts = set(ns1.split('.'))
        ns2_parts = set(ns2.split('.'))
        
        intersection = ns1_parts & ns2_parts
        union = ns1_parts | ns2_parts
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def enforce_format(self, namespace_id: str) -> Tuple[bool, Optional[StrictViolation]]:
        """
        強制格式（零容忍）
        
        Returns:
            (通過, 違規記錄或None)
        """
        self.enforcement_metrics['total_checks'] += 1
        
        # 零容忍：嚴格格式檢查
        parts = namespace_id.split('.')
        
        # 必須有 4 個部分
        if len(parts) != 4:
            return self._create_format_violation(
                namespace_id,
                f"格式錯誤: 必須恰好 4 個部分，實際 {len(parts)} 個"
            )
        
        # 檢查每個部分
        type_part, era_part, domain_part, component_part = parts
        
        # Type 檢查
        if not type_part.islower() or not type_part.isalpha():
            return self._create_format_violation(
                namespace_id,
                f"類型部分錯誤: '{type_part}' 必須是小寫字母"
            )
        
        # Era 檢查
        if era_part not in ['era1', 'era2', 'era3', 'cross']:
            return self._create_format_violation(
                namespace_id,
                f"Era 錯誤: '{era_part}' 必須是 era1/era2/era3/cross"
            )
        
        # Domain 和 Component 檢查（kebab-case）
        for part_name, part_value in [('domain', domain_part), ('component', component_part)]:
            if not all(c.islower() or c.isdigit() or c == '-' for c in part_value):
                return self._create_format_violation(
                    namespace_id,
                    f"{part_name} 錯誤: '{part_value}' 必須是 kebab-case（小寫+連字號+數字）"
                )
            
            # 禁止開頭或結尾是連字號
            if part_value.startswith('-') or part_value.endswith('-'):
                return self._create_format_violation(
                    namespace_id,
                    f"{part_name} 錯誤: '{part_value}' 不能以連字號開頭或結尾"
                )
            
            # 禁止連續連字號
            if '--' in part_value:
                return self._create_format_violation(
                    namespace_id,
                    f"{part_name} 錯誤: '{part_value}' 不能有連續連字號"
                )
        
        return (True, None)
    
    def _create_format_violation(
        self,
        namespace_id: str,
        description: str
    ) -> Tuple[bool, StrictViolation]:
        """創建格式違規"""
        violation = StrictViolation(
            violation_id=f"fmt-{len(self.violations)}",
            namespace_id=namespace_id,
            rule_code="NG00302",
            severity=ViolationSeverity.IMMUTABLE,
            action=EnforcementAction.IMMEDIATE_BLOCK,
            description=description,
            detected_at=datetime.now().isoformat()
        )
        
        self.violations.append(violation)
        self.blocked_operations.append(namespace_id)
        self.enforcement_metrics['total_blocks'] += 1
        
        logger.critical(f"🚨 IMMEDIATE_BLOCK: {description}")
        
        return (False, violation)
    
    def enforce_closure(
        self,
        namespace_data: Dict[str, Any]
    ) -> Tuple[bool, List[StrictViolation]]:
        """
        強制閉環完整性（零容忍）
        
        Returns:
            (通過, 違規列表)
        """
        self.enforcement_metrics['total_checks'] += 1
        
        violations = []
        namespace_id = namespace_data.get('namespace_id', 'unknown')
        
        # 零容忍：必須有 NG 編碼
        if not namespace_data.get('ng_code'):
            violations.append(StrictViolation(
                violation_id=f"cls-{len(self.violations)}",
                namespace_id=namespace_id,
                rule_code="NG90001",
                severity=ViolationSeverity.IMMUTABLE,
                action=EnforcementAction.BLOCK_UNTIL_FIXED,
                description="缺少 NG 編碼（閉環必要項）",
                detected_at=datetime.now().isoformat()
            ))
        
        # 零容忍：必須有審計追蹤
        audit_trail = namespace_data.get('audit_trail', [])
        if not audit_trail:
            violations.append(StrictViolation(
                violation_id=f"aud-{len(self.violations)}",
                namespace_id=namespace_id,
                rule_code="NG00701",
                severity=ViolationSeverity.ABSOLUTE,
                action=EnforcementAction.BLOCK_UNTIL_FIXED,
                description="缺少審計追蹤（閉環必要項）",
                detected_at=datetime.now().isoformat()
            ))
        
        # 零容忍：必須有驗證記錄
        if not namespace_data.get('validated'):
            violations.append(StrictViolation(
                violation_id=f"val-{len(self.violations)}",
                namespace_id=namespace_id,
                rule_code="NG00301",
                severity=ViolationSeverity.ABSOLUTE,
                action=EnforcementAction.BLOCK_UNTIL_FIXED,
                description="缺少驗證記錄（閉環必要項）",
                detected_at=datetime.now().isoformat()
            ))
        
        if violations:
            self.violations.extend(violations)
            self.blocked_operations.append(namespace_id)
            self.enforcement_metrics['total_blocks'] += len(violations)
            
            logger.critical(
                f"🚨 CLOSURE INCOMPLETE: {namespace_id} - "
                f"{len(violations)} 個閉環缺口 [BLOCK_ALL_OPERATIONS]"
            )
            
            return (False, violations)
        
        return (True, [])
    
    def get_enforcement_report(self) -> str:
        """生成執行報告"""
        total = self.enforcement_metrics['total_checks']
        blocks = self.enforcement_metrics['total_blocks']
        pass_rate = ((total - blocks) / total * 100) if total > 0 else 100.0
        
        report_lines = [
            "=" * 70,
            "NG 嚴格執行器報告（零容忍）",
            "=" * 70,
            f"模式: ZERO_TOLERANCE",
            f"NG Code: NG00004",
            "",
            "執行統計:",
            f"  總檢查數: {total}",
            f"  總阻斷數: {blocks}",
            f"  通過率: {pass_rate:.1f}%",
            f"  阻斷率: {blocks / total * 100 if total > 0 else 0:.1f}%",
            "",
            "違規分布:"
        ]
        
        by_severity = {}
        for v in self.violations:
            by_severity[v.severity.value] = by_severity.get(v.severity.value, 0) + 1
        
        for severity, count in by_severity.items():
            report_lines.append(f"  {severity}: {count}")
        
        report_lines.extend([
            "",
            "零容忍合規:",
            f"  容忍度: 0%",
            f"  警告允許: ❌",
            f"  手動繞過: ❌",
            f"  寬限期: 0 seconds",
            "",
            "阻斷命名空間:"
        ])
        
        for ns_id in self.blocked_operations[:10]:
            report_lines.append(f"  🚫 {ns_id}")
        
        if len(self.blocked_operations) > 10:
            report_lines.append(f"  ... 及 {len(self.blocked_operations) - 10} 個其他")
        
        report_lines.extend([
            "",
            "=" * 70
        ])
        
        return "\n".join(report_lines)


if __name__ == "__main__":
    # 測試嚴格執行器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s'
    )
    
    print("\n" + "=" * 70)
    print("NG 嚴格執行器測試（零容忍模式）")
    print("=" * 70)
    
    enforcer = NgStrictEnforcer()
    
    # 測試 1: 唯一性執行
    print("\n測試 1: 唯一性執行（零容忍）")
    print("-" * 70)
    
    existing = ["pkg.era1.platform.core", "svc.era2.runtime.api"]
    
    # 測試重複命名空間
    passed, violation = enforcer.enforce_uniqueness(
        "pkg.era1.platform.core",
        existing
    )
    print(f"測試重複: {'✅ 通過' if passed else '🚫 阻斷'}")
    
    # 測試新命名空間
    passed, violation = enforcer.enforce_uniqueness(
        "pkg.era1.data.processor",
        existing
    )
    print(f"測試新建: {'✅ 通過' if passed else '🚫 阻斷'}")
    
    # 測試 2: 格式執行
    print("\n測試 2: 格式執行（零容忍）")
    print("-" * 70)
    
    test_cases = [
        "pkg.era1.platform.core",           # ✅ 正確
        "PKG.era1.platform.core",           # ❌ 大寫
        "pkg.era1.platform_core",           # ❌ 下劃線
        "pkg.era1.platform",                # ❌ 不完整
        "pkg.era1.platform.core.extra",     # ❌ 太多部分
    ]
    
    for test_ns in test_cases:
        passed, violation = enforcer.enforce_format(test_ns)
        status = "✅ 通過" if passed else "🚫 阻斷"
        print(f"  {status}: {test_ns}")
    
    # 測試 3: 閉環執行
    print("\n測試 3: 閉環執行（零容忍）")
    print("-" * 70)
    
    complete_ns = {
        'namespace_id': 'pkg.era1.test.complete',
        'ng_code': 'NG10001',
        'validated': True,
        'audit_trail': [{'action': 'registered'}]
    }
    
    incomplete_ns = {
        'namespace_id': 'pkg.era1.test.incomplete',
        'ng_code': None,  # 缺少
        'audit_trail': []  # 缺少
    }
    
    passed_1, violations_1 = enforcer.enforce_closure(complete_ns)
    print(f"完整命名空間: {'✅ 通過' if passed_1 else f'🚫 阻斷 ({len(violations_1)} 缺口)'}")
    
    passed_2, violations_2 = enforcer.enforce_closure(incomplete_ns)
    print(f"不完整命名空間: {'✅ 通過' if passed_2 else f'🚫 阻斷 ({len(violations_2)} 缺口)'}")
    
    # 生成報告
    print("\n" + enforcer.get_enforcement_report())
    
    print("\n" + "=" * 70)
    print("✅ NG 嚴格執行器測試完成")
    print("=" * 70)
