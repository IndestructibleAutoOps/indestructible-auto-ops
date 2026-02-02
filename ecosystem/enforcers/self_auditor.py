#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: general
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
SelfAuditor - GL治理執行層的自我審計組件

負責對AI助理的操作歷史進行持續審計，檢查：
1. 操作是否遵守治理合約
2. 報告是否包含足夠的證據
3. 是否有違禁短語
4. 治理違規趨勢分析

功能：
- 定期掃描操作日誌
- 識別治理違規
- 生成審計報告
- 觸發自動修復
- 違規趨勢分析
"""

import os
import json
import yaml
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict, Counter


class SelfAuditor:
    """GL治理執行層的自我審計器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化自我審計器
        
        Args:
            config_path: 配置文件路徑，默認為 ecosystem/gates/self-auditor-config.yaml
        """
        if config_path is None:
            config_path = "ecosystem/gates/self-auditor-config.yaml"
        
        self.config_path = config_path
        self.config = self._load_config()
        
        # 設置日誌目錄
        self.audit_logs_dir = Path("ecosystem/logs/audit-logs")
        self.audit_logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 禁止短語列表（從gl-fact-pipeline規範）
        self.forbidden_phrases = self.config.get('forbidden_phrases', [
            # CRITICAL級別 - 絕對禁止
            ("100% 完成", "CRITICAL", "基於已實現的功能集"),
            ("完全符合", "CRITICAL", "在[方面]與標準對齊"),
            ("已全部實現", "CRITICAL", "已實現[具體功能列表]"),
            ("一定", "CRITICAL", "建議/可能/根據分析"),
            ("必須", "CRITICAL", "應該/建議/推薦"),
            
            # HIGH級別 - 需要避免
            ("應該是", "HIGH", "根據[證據]，建議"),
            ("可能是", "HIGH", "基於[證據]，推測"),
            ("我認為", "HIGH", "基於[證據]，分析表明"),
            ("顯然", "HIGH", "根據[證據]"),
            ("毫無疑問", "HIGH", "根據證據分析"),
            
            # MEDIUM級別 - 需要改進
            ("應該", "MEDIUM", "建議"),
            ("可能", "MEDIUM", "可能存在"),
            ("或許", "MEDIUM", "可能"),
            ("大概", "MEDIUM", "大約"),
            
            # LOW級別 - 語言風格
            ("似乎", "LOW", "看起來"),
            ("看起來", "LOW", "從分析來看"),
            ("感覺", "LOW", "分析顯示"),
        ])
        
        # 證據覆蓋率閾值
        self.evidence_coverage_threshold = self.config.get('evidence_coverage_threshold', 0.90)
        
        # 審計歷史
        self.audit_history: List[Dict] = []
        
    def _load_config(self) -> Dict:
        """加載配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {
            'audit_interval_hours': 24,
            'max_audit_days': 7,
            'forbidden_phrases': [],
            'evidence_coverage_threshold': 0.90,
            'trend_analysis_window_days': 30,
            'critical_violation_threshold': 5,
        }
    
    def scan_audit_logs(self, days: int = 7) -> List[Dict]:
        """
        掃描審計日誌
        
        Args:
            days: 掃描最近幾天的日誌
            
        Returns:
            審計日誌列表
        """
        audit_logs = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for log_file in self.audit_logs_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log = json.load(f)
                    
                    # 檢查日誌日期
                    log_date = datetime.fromisoformat(log.get('timestamp', ''))
                    if log_date >= cutoff_date:
                        audit_logs.append(log)
            except Exception as e:
                print(f"讀取日誌文件失敗 {log_file}: {e}")
        
        return audit_logs
    
    def check_forbidden_phrases(self, text: str) -> List[Dict]:
        """
        檢查文本中的禁止短語
        
        Args:
            text: 要檢查的文本
            
        Returns:
            違規列表
        """
        violations = []
        
        for phrase, severity, replacement in self.forbidden_phrases:
            if phrase in text:
                # 找到所有出現位置
                matches = list(re.finditer(re.escape(phrase), text))
                for match in matches:
                    violations.append({
                        'phrase': phrase,
                        'severity': severity,
                        'replacement': replacement,
                        'position': match.start(),
                        'context': text[max(0, match.start()-20):match.end()+20]
                    })
        
        return violations
    
    def calculate_evidence_coverage(self, report_text: str) -> float:
        """
        計算證據覆蓋率
        
        Args:
            report_text: 報告文本
            
        Returns:
            覆蓋率（0.0-1.0）
        """
        # 證據鏈接格式：[證據: path/to/file.yaml#L10-L15]
        evidence_pattern = r'\[證據:\s*[^\]]+\]'
        evidence_links = re.findall(evidence_pattern, report_text)
        
        # 計算聲明句數（以句號、問號、感歎號結尾）
        statement_pattern = r'[^.!?。？！]+[.!?。？！]'
        statements = re.findall(statement_pattern, report_text)
        total_statements = len(statements)
        
        if total_statements == 0:
            return 0.0
        
        coverage = len(evidence_links) / total_statements
        return min(coverage, 1.0)
    
    def analyze_governance_compliance(self, audit_log: Dict) -> Dict:
        """
        分析治理合規性
        
        Args:
            audit_log: 審計日誌
            
        Returns:
            合規性分析結果
        """
        analysis = {
            'audit_id': audit_log.get('audit_id'),
            'timestamp': audit_log.get('timestamp'),
            'operation_type': audit_log.get('operation_type'),
            'compliance': {
                'status': 'COMPLIANT',
                'violations': []
            }
        }
        
        # 檢查證據鏈
        if 'evidence_chain' in audit_log:
            evidence_chain = audit_log['evidence_chain']
            if not evidence_chain or len(evidence_chain) == 0:
                analysis['compliance']['violations'].append({
                    'rule': 'GA-003',
                    'description': '缺少證據鏈',
                    'severity': 'CRITICAL'
                })
                analysis['compliance']['status'] = 'NON_COMPLIANT'
        
        # 檢查報告驗證
        if 'report_validation' in audit_log:
            validation = audit_log['report_validation']
            if validation.get('has_unverified_claims', False):
                analysis['compliance']['violations'].append({
                    'rule': 'GA-004',
                    'description': '報告包含未驗證的聲明',
                    'severity': 'CRITICAL'
                })
                analysis['compliance']['status'] = 'NON_COMPLIANT'
            
            evidence_coverage = validation.get('evidence_coverage', 0.0)
            if evidence_coverage < self.evidence_coverage_threshold:
                analysis['compliance']['violations'].append({
                    'rule': 'GA-003',
                    'description': f'證據覆蓋率不足: {evidence_coverage:.1%} < {self.evidence_coverage_threshold:.1%}',
                    'severity': 'HIGH'
                })
                if analysis['compliance']['status'] == 'COMPLIANT':
                    analysis['compliance']['status'] = 'WARNING'
            
            if validation.get('forbidden_phrase_violations'):
                analysis['compliance']['violations'].append({
                    'rule': 'GA-004',
                    'description': f'報告包含禁止短語: {len(validation["forbidden_phrase_violations"])}個',
                    'severity': 'HIGH'
                })
                if analysis['compliance']['status'] == 'COMPLIANT':
                    analysis['compliance']['status'] = 'WARNING'
        
        return analysis
    
    def audit_operation(self, operation_data: Dict) -> Dict:
        """
        審計單個操作
        
        Args:
            operation_data: 操作數據
            
        Returns:
            審計結果
        """
        audit_result = {
            'audit_id': f"audit-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'operation_type': operation_data.get('operation_type'),
            'operation_id': operation_data.get('operation_id'),
            'status': 'PASSED',
            'findings': [],
            'recommendations': []
        }
        
        # 檢查治理合約引用
        if 'governance_contracts' not in operation_data or not operation_data['governance_contracts']:
            audit_result['findings'].append({
                'type': 'MISSING_CONTRACTS',
                'severity': 'CRITICAL',
                'description': '操作未引用相關治理合約',
                'rule': 'GA-001'
            })
            audit_result['status'] = 'FAILED'
            audit_result['recommendations'].append(
                '請在操作前查詢並引用相關的治理合約'
            )
        
        # 檢查證據鏈
        if 'evidence_chain' not in operation_data or not operation_data['evidence_chain']:
            audit_result['findings'].append({
                'type': 'MISSING_EVIDENCE',
                'severity': 'CRITICAL',
                'description': '操作缺少證據鏈',
                'rule': 'GA-003'
            })
            audit_result['status'] = 'FAILED'
            audit_result['recommendations'].append(
                '請提供完整的證據鏈，包括源文件、合約引用、驗證輸出等'
            )
        
        # 檢查報告驗證
        if 'report' in operation_data:
            report_text = operation_data['report']
            
            # 檢查禁止短語
            forbidden_violations = self.check_forbidden_phrases(report_text)
            if forbidden_violations:
                audit_result['findings'].append({
                    'type': 'FORBIDDEN_PHRASES',
                    'severity': 'HIGH',
                    'description': f'報告包含 {len(forbidden_violations)} 個禁止短語',
                    'details': forbidden_violations,
                    'rule': 'GA-004'
                })
                if audit_result['status'] == 'PASSED':
                    audit_result['status'] = 'WARNING'
                audit_result['recommendations'].append(
                    f'替換禁止短語為更精確的表述，參見詳細違規列表'
                )
            
            # 檢查證據覆蓋率
            evidence_coverage = self.calculate_evidence_coverage(report_text)
            if evidence_coverage < self.evidence_coverage_threshold:
                audit_result['findings'].append({
                    'type': 'LOW_EVIDENCE_COVERAGE',
                    'severity': 'HIGH',
                    'description': f'證據覆蓋率不足: {evidence_coverage:.1%} < {self.evidence_coverage_threshold:.1%}',
                    'rule': 'GA-003'
                })
                if audit_result['status'] == 'PASSED':
                    audit_result['status'] = 'WARNING'
                audit_result['recommendations'].append(
                    '增加證據鏈接，確保至少90%的聲明有證據支持'
                )
        
        # 保存審計結果
        self.audit_history.append(audit_result)
        
        return audit_result
    
    def analyze_violation_trends(self, days: int = 30) -> Dict:
        """
        分析違規趨勢
        
        Args:
            days: 分析最近幾天的數據
            
        Returns:
            趨勢分析結果
        """
        audit_logs = self.scan_audit_logs(days)
        
        # 統計違規類型
        violation_by_type = Counter()
        violation_by_severity = Counter()
        violation_by_operation = Counter()
        daily_violations = defaultdict(int)
        
        for log in audit_logs:
            # 檢查合規性分析
            compliance = log.get('compliance', {})
            violations = compliance.get('violations', [])
            
            for violation in violations:
                rule = violation.get('rule')
                severity = violation.get('severity')
                operation = log.get('operation_type')
                date = log.get('timestamp', '')[:10]
                
                violation_by_type[rule] += 1
                violation_by_severity[severity] += 1
                violation_by_operation[operation] += 1
                daily_violations[date] += 1
        
        # 計算趨勢
        trend = {
            'total_violations': sum(violation_by_type.values()),
            'by_type': dict(violation_by_type),
            'by_severity': dict(violation_by_severity),
            'by_operation': dict(violation_by_operation),
            'daily': dict(daily_violations),
            'trend_direction': 'UNKNOWN',
            'critical_findings': []
        }
        
        # 分析趨勢方向
        if len(daily_violations) >= 2:
            recent_week = list(daily_violations.values())[-7:]
            previous_week = list(daily_violations.values())[-14:-7] if len(daily_violations) >= 14 else recent_week
            
            if len(recent_week) > 0 and len(previous_week) > 0:
                avg_recent = sum(recent_week) / len(recent_week)
                avg_previous = sum(previous_week) / len(previous_week)
                
                if avg_recent > avg_previous * 1.2:
                    trend['trend_direction'] = 'INCREASING'
                elif avg_recent < avg_previous * 0.8:
                    trend['trend_direction'] = 'DECREASING'
                else:
                    trend['trend_direction'] = 'STABLE'
        
        # 識別關鍵問題
        critical_threshold = self.config.get('critical_violation_threshold', 5)
        for rule, count in violation_by_type.items():
            if count >= critical_threshold:
                trend['critical_findings'].append({
                    'rule': rule,
                    'count': count,
                    'description': f'規則 {rule} 違規次數超過閾值 {critical_threshold}'
                })
        
        return trend
    
    def generate_audit_report(self, days: int = 7) -> Dict:
        """
        生成審計報告
        
        Args:
            days: 報告覆蓋的天數
            
        Returns:
            審計報告
        """
        audit_logs = self.scan_audit_logs(days)
        
        # 統計指標
        total_operations = len(audit_logs)
        compliant_operations = 0
        non_compliant_operations = 0
        warning_operations = 0
        
        violations_by_type = Counter()
        violations_by_severity = Counter()
        
        # 分析每個操作
        for log in audit_logs:
            compliance = log.get('compliance', {})
            status = compliance.get('status', 'UNKNOWN')
            
            if status == 'COMPLIANT':
                compliant_operations += 1
            elif status == 'NON_COMPLIANT':
                non_compliant_operations += 1
            elif status == 'WARNING':
                warning_operations += 1
            
            # 統計違規
            for violation in compliance.get('violations', []):
                rule = violation.get('rule')
                severity = violation.get('severity')
                violations_by_type[rule] += 1
                violations_by_severity[severity] += 1
        
        # 趨勢分析
        trend = self.analyze_violation_trends(days)
        
        report = {
            'report_id': f"audit-report-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'report_period_days': days,
            'summary': {
                'total_operations': total_operations,
                'compliant_operations': compliant_operations,
                'non_compliant_operations': non_compliant_operations,
                'warning_operations': warning_operations,
                'compliance_rate': compliant_operations / total_operations if total_operations > 0 else 0.0,
                'violation_count': sum(violations_by_type.values())
            },
            'violations': {
                'by_type': dict(violations_by_type),
                'by_severity': dict(violations_by_severity)
            },
            'trends': trend,
            'recommendations': self._generate_recommendations(trend, violations_by_type, violations_by_severity)
        }
        
        return report
    
    def _generate_recommendations(self, trend: Dict, by_type: Counter, by_severity: Counter) -> List[str]:
        """生成改進建議"""
        recommendations = []
        
        # 基於趨勢的建議
        if trend['trend_direction'] == 'INCREASING':
            recommendations.append(
                '⚠️ 違規趨勢上升，建議加強治理培訓和審查流程'
            )
        
        # 基於關鍵問題的建議
        for finding in trend.get('critical_findings', []):
            recommendations.append(
                f"🚨 關鍵問題：{finding['description']}"
            )
        
        # 基於違規類型的建議
        if 'GA-001' in by_type:
            recommendations.append(
                '建議：在執行操作前，確保查詢並引用相關治理合約'
            )
        if 'GA-002' in by_type:
            recommendations.append(
                '建議：使用標準化驗證工具，確保治理合約符合性'
            )
        if 'GA-003' in by_type:
            recommendations.append(
                '建議：提供完整的證據鏈，包括源文件、合約引用、驗證輸出'
            )
        if 'GA-004' in by_type:
            recommendations.append(
                '建議：避免使用禁止短語，提供基於證據的準確報告'
            )
        
        # 基於嚴重程度的建議
        if by_severity.get('CRITICAL', 0) > 0:
            recommendations.append(
                '🚨 發現CRITICAL級別違規，需要立即處理'
            )
        if by_severity.get('HIGH', 0) > 5:
            recommendations.append(
                '⚠️ HIGH級別違規較多，建議優先處理'
            )
        
        return recommendations
    
    def save_audit_report(self, report: Dict, filename: Optional[str] = None) -> str:
        """
        保存審計報告
        
        Args:
            report: 審計報告
            filename: 文件名，默認使用報告ID
            
        Returns:
            保存的文件路徑
        """
        if filename is None:
            filename = f"{report['report_id']}.json"
        
        filepath = self.audit_logs_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def trigger_auto_remediation(self, violations: List[Dict]) -> List[Dict]:
        """
        觸發自動修復（可選功能）
        
        Args:
            violations: 違規列表
            
        Returns:
            修復結果列表
        """
        remediation_results = []
        
        # 這裡可以實現自動修復邏輯
        # 例如：自動添加證據鏈接、替換禁止短語等
        
        return remediation_results


def main():
    """測試SelfAuditor"""
    print("=== SelfAuditor 測試 ===\n")
    
    # 創建審計器
    auditor = SelfAuditor()
    
    # 測試禁止短語檢查
    print("1. 測試禁止短語檢查")
    test_text = "這個項目已經100%完成了，完全符合標準，必須成功。"
    violations = auditor.check_forbidden_phrases(test_text)
    print(f"   發現 {len(violations)} 個違規:")
    for v in violations[:3]:
        print(f"   - '{v['phrase']}' ({v['severity']}) -> '{v['replacement']}'")
    print()
    
    # 測試證據覆蓋率計算
    print("2. 測試證據覆蓋率計算")
    report_text = """
    根據GL治理合約[證據: ecosystem/contracts/platforms/gl-platforms.yaml]，
    該平台符合標準。
    另外，文件[證據: gl-platforms.yaml#L10-L20]也確認了這一點。
    第三個點是基於驗證結果[證據: validation/output.json]。
    """
    coverage = auditor.calculate_evidence_coverage(report_text)
    print(f"   證據覆蓋率: {coverage:.1%}")
    print(f"   閾值: {auditor.evidence_coverage_threshold:.1%}")
    print(f"   狀態: {'✅ 通過' if coverage >= auditor.evidence_coverage_threshold else '❌ 未通過'}")
    print()
    
    # 測試操作審計
    print("3. 測試操作審計")
    test_operation = {
        'operation_type': 'file_migration',
        'operation_id': 'test-001',
        'governance_contracts': ['file-naming-content-contract.yaml'],
        'evidence_chain': [
            {'type': 'source_file', 'path': 'ecosystem/contracts/governance/file-naming-content-contract.yaml'}
        ],
        'report': '根據治理合約[證據: file-naming-content-contract.yaml]，該操作符合規範。'
    }
    audit_result = auditor.audit_operation(test_operation)
    print(f"   審計ID: {audit_result['audit_id']}")
    print(f"   狀態: {audit_result['status']}")
    print(f"   發現: {len(audit_result['findings'])} 個")
    for finding in audit_result['findings']:
        print(f"   - {finding['type']}: {finding['description']}")
    print()
    
    # 測試生成審計報告
    print("4. 測試生成審計報告")
    report = auditor.generate_audit_report(days=7)
    print(f"   報告ID: {report['report_id']}")
    print(f"   總操作數: {report['summary']['total_operations']}")
    print(f"   合規率: {report['summary']['compliance_rate']:.1%}")
    print(f"   違規數: {report['summary']['violation_count']}")
    print(f"   趨勢: {report['trends']['trend_direction']}")
    print()
    
    # 保存報告
    report_path = auditor.save_audit_report(report)
    print(f"   報告已保存: {report_path}")
    print()
    
    print("=== SelfAuditor 測試完成 ===")


if __name__ == "__main__":
    main()