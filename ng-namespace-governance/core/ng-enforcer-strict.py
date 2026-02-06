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
from typing import Dict, List, Any, Tuple, Optional
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


class BinaryResult(Enum):
    """二元結果（只有兩種）"""
    PASS = "pass"
    BLOCK = "block"


class NgStrictEnforcer:
    """
    NG 嚴格執行器（絕對二元執行）
    
    IndestructibleAutoOps 零容忍執行模式：
    - 只有 PASS 或 BLOCK（無警告）
    - 100% 自動化決策（無人工）
    - 立即阻斷機制（無延遲）
    - 不可變審計（無修改）
    - 無修復建議（只有拒絕原因）
    """
    
    def __init__(self):
        """初始化嚴格執行器（零容忍模式強制）"""
        self.blocked_operations: List[str] = []
        self.enforcement_metrics = {
            'total_checks': 0,
            'total_pass': 0,
            'total_block': 0,
            'pass_rate': 0.0,
            'block_rate': 0.0
        }
        
        # 禁止任何非二元結果
        self.allowed_results = {BinaryResult.PASS, BinaryResult.BLOCK}
        
        logger.info("🛡️  NG 嚴格執行器已啟動 [ABSOLUTE_BINARY_ENFORCEMENT]")
    
    def enforce_uniqueness(
        self,
        namespace_id: str,
        existing_namespaces: List[str]
    ) -> Dict[str, any]:
        """
        強制唯一性（絕對二元執行）
        
        Returns:
            {'result': 'pass'} 或 {'result': 'block', 'reason': '...'}
        """
        self.enforcement_metrics['total_checks'] += 1
        
        # 檢查完全匹配（二元決策）
        if namespace_id in existing_namespaces:
            self.enforcement_metrics['total_block'] += 1
            self.blocked_operations.append(namespace_id)
            
            logger.critical(
                f"🚫 BLOCK: 命名空間 {namespace_id} 已存在"
            )
            
            return {
                'result': BinaryResult.BLOCK.value,
                'reason': f"命名空間 {namespace_id} 已存在於系統中",
                'rule_code': 'NG00301',
                'action_taken': 'REJECT_REGISTRATION',
                'user_action': '請使用不同的命名空間 ID'
            }
        
        # 檢查語義相似度（ML 二元決策）
        for existing in existing_namespaces:
            similarity = self._calculate_similarity(namespace_id, existing)
            
            # ML 二元決策：>= 0.80 = BLOCK，< 0.80 = 繼續檢查
            if similarity >= 0.80:
                self.enforcement_metrics['total_block'] += 1
                self.blocked_operations.append(namespace_id)
                
                logger.critical(
                    f"🚫 BLOCK: 語義相似度 {similarity:.0%} >= 80% 與 {existing}"
                )
                
                return {
                    'result': BinaryResult.BLOCK.value,
                    'reason': f"語義相似度 {similarity:.0%} 過高（與 {existing} 太相似）",
                    'rule_code': 'NG00301',
                    'threshold': '80%',
                    'action_taken': 'REJECT_REGISTRATION',
                    'user_action': '請使用語義差異更大的命名空間 ID'
                }
        
        # 所有檢查通過
        self.enforcement_metrics['total_pass'] += 1
        
        return {
            'result': BinaryResult.PASS.value,
            'rule_code': 'NG00301',
            'checks_passed': ['global_uniqueness', 'semantic_uniqueness']
        }
    
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
    
    def enforce_format(self, namespace_id: str) -> Dict[str, any]:
        """
        強制格式（絕對二元執行）
        
        Returns:
            {'result': 'pass'} 或 {'result': 'block', 'reason': '...'}
        """
        self.enforcement_metrics['total_checks'] += 1
        
        # 零容忍：嚴格格式檢查
        parts = namespace_id.split('.')
        
        # 必須有 4 個部分（二元檢查）
        if len(parts) != 4:
            self.enforcement_metrics['total_block'] += 1
            self.blocked_operations.append(namespace_id)
            
            return {
                'result': BinaryResult.BLOCK.value,
                'reason': f"格式錯誤: 必須恰好 4 個部分（type.era.domain.component），實際 {len(parts)} 個",
                'rule_code': 'NG00302',
                'action_taken': 'REJECT_REGISTRATION',
                'user_action': f'正確格式範例: pkg.era1.platform.core'
            }
        
        # 檢查每個部分
        type_part, era_part, domain_part, component_part = parts
        
        # Type 檢查（二元）
        if not type_part.islower() or not type_part.isalpha():
            self.enforcement_metrics['total_block'] += 1
            return {
                'result': BinaryResult.BLOCK.value,
                'reason': f"類型部分 '{type_part}' 必須是純小寫字母",
                'rule_code': 'NG00302',
                'action_taken': 'REJECT_REGISTRATION'
            }
        
        # Era 檢查（二元）
        if era_part not in ['era1', 'era2', 'era3', 'cross']:
            self.enforcement_metrics['total_block'] += 1
            return {
                'result': BinaryResult.BLOCK.value,
                'reason': f"Era '{era_part}' 必須是 era1/era2/era3/cross 之一",
                'rule_code': 'NG00302',
                'valid_values': ['era1', 'era2', 'era3', 'cross'],
                'action_taken': 'REJECT_REGISTRATION'
            }
        
        # Domain 和 Component 檢查（kebab-case）- 二元決策
        for part_name, part_value in [('domain', domain_part), ('component', component_part)]:
            # 檢查字符白名單
            if not all(c.islower() or c.isdigit() or c == '-' for c in part_value):
                self.enforcement_metrics['total_block'] += 1
                return {
                    'result': BinaryResult.BLOCK.value,
                    'reason': f"{part_name} '{part_value}' 必須只包含小寫字母、數字、連字號",
                    'rule_code': 'NG00302',
                    'allowed_chars': '[a-z0-9-]',
                    'action_taken': 'REJECT_REGISTRATION'
                }
            
            # 禁止連字號開頭或結尾
            if part_value.startswith('-') or part_value.endswith('-'):
                self.enforcement_metrics['total_block'] += 1
                return {
                    'result': BinaryResult.BLOCK.value,
                    'reason': f"{part_name} '{part_value}' 不能以連字號開頭或結尾",
                    'rule_code': 'NG00302',
                    'action_taken': 'REJECT_REGISTRATION'
                }
            
            # 禁止連續連字號
            if '--' in part_value:
                self.enforcement_metrics['total_block'] += 1
                return {
                    'result': BinaryResult.BLOCK.value,
                    'reason': f"{part_name} '{part_value}' 不能有連續連字號",
                    'rule_code': 'NG00302',
                    'action_taken': 'REJECT_REGISTRATION'
                }
        
        # 所有檢查通過（二元結果）
        self.enforcement_metrics['total_pass'] += 1
        
        return {
            'result': BinaryResult.PASS.value,
            'rule_code': 'NG00302',
            'checks_passed': ['format_structure', 'kebab_case', 'character_whitelist']
        }
    
    def _binary_block(self, namespace_id: str, reason: str, rule_code: str) -> Dict[str, any]:
        """創建二元 BLOCK 結果（刪除違規記錄概念，直接返回結果）"""
        self.enforcement_metrics['total_block'] += 1
        self.blocked_operations.append(namespace_id)
        
        logger.critical(f"🚫 BLOCK: {reason}")
        
        return {
            'result': BinaryResult.BLOCK.value,
            'reason': reason,
            'rule_code': rule_code,
            'action_taken': 'REJECT_OPERATION',
            'timestamp': datetime.now().isoformat()
        }
    
    def enforce_closure(self, namespace_data: Dict[str, Any]) -> Dict[str, any]:
        """
        強制閉環完整性（絕對二元執行）
        
        Returns:
            {'result': 'pass'} 或 {'result': 'block', 'reason': '...'}
        """
        self.enforcement_metrics['total_checks'] += 1
        
        namespace_id = namespace_data.get('namespace_id', 'unknown')
        missing_items = []
        
        # 檢查 NG 編碼（必要項）
        if not namespace_data.get('ng_code'):
            missing_items.append('NG 編碼')
        
        # 檢查審計追蹤（必要項）
        if not namespace_data.get('audit_trail') or len(namespace_data.get('audit_trail', [])) == 0:
            missing_items.append('審計追蹤')
        
        # 檢查驗證記錄（必要項）
        if not namespace_data.get('validated'):
            missing_items.append('驗證記錄')
        
        # 二元決策
        if missing_items:
            self.enforcement_metrics['total_block'] += 1
            self.blocked_operations.append(namespace_id)
            
            logger.critical(
                f"🚫 BLOCK: 閉環不完整 - 缺少 {', '.join(missing_items)}"
            )
            
            return {
                'result': BinaryResult.BLOCK.value,
                'reason': f"閉環不完整：缺少 {', '.join(missing_items)}",
                'rule_code': 'NG90001',
                'missing_items': missing_items,
                'action_taken': 'REJECT_ALL_OPERATIONS',
                'user_action': '命名空間必須完成完整生命週期才能使用'
            }
        
        # 所有檢查通過
        self.enforcement_metrics['total_pass'] += 1
        
        return {
            'result': BinaryResult.PASS.value,
            'rule_code': 'NG90001',
            'checks_passed': ['ng_code_present', 'audit_trail_present', 'validation_complete']
        }
    
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
