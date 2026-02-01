"""
Pipeline Integration - GL治理執行層與事實驗證管道的集成

負責將 gl-fact-pipeline.py 集成到治理執行層，提供：
1. 標準化的管道執行接口
2. 與 GovernanceEnforcer 的無縫集成
3. 證據收集和驗證的自動化
4. 報告生成和驗證
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import yaml
from datetime import datetime
import hashlib
import re

# 添加事實驗證工具的路徑
fact_verification_path = Path(__file__).parent.parent / "tools" / "fact-verification"
sys.path.insert(0, str(fact_verification_path))

try:
    from gl_fact_pipeline import GLFactPipeline
except ImportError:
    GLFactPipeline = None


class PipelineIntegration:
    """GL事實驗證管道集成器"""
    
    def __init__(self, 
                 config_path: Optional[str] = None,
                 workspace_path: str = "."):
        """
        初始化管道集成器
        
        Args:
            config_path: 管道配置文件路徑
            workspace_path: 工作區路徑
        """
        # 默認配置路徑
        if config_path is None:
            config_path = "ecosystem/contracts/naming-governance/gl.fact-pipeline-spec.yaml"
        
        self.config_path = Path(config_path)
        self.workspace_path = Path(workspace_path)
        
        # 初始化事實驗證管道
        try:
            if GLFactPipeline and self.config_path.exists():
                self.pipeline = GLFactPipeline(
                    config_path=str(self.config_path),
                    workspace_path=str(self.workspace_path)
                )
                self.pipeline_available = True
            else:
                self.pipeline = None
                self.pipeline_available = False
        except Exception as e:
            print(f"無法初始化 GLFactPipeline: {e}")
            self.pipeline = None
            self.pipeline_available = False
        
        # 輸出目錄
        self.output_dir = self.workspace_path / "ecosystem" / "outputs" / "fact-verification"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_verification(self, 
                        topics: List[str],
                        operation_context: Optional[Dict] = None) -> Dict:
        """
        執行事實驗證
        
        Args:
            topics: 驗證主題列表（如 ['semver', 'cncf']）
            operation_context: 操作上下文信息
            
        Returns:
            驗證報告
        """
        if not self.pipeline_available:
            return self._generate_mock_report(topics, operation_context)
        
        try:
            # 執行管道
            report = self.pipeline.run_pipeline(topics)
            
            # 添加操作上下文
            if operation_context:
                report['operation_context'] = operation_context
            
            # 保存報告
            report_path = self._save_report(report, operation_context)
            
            return {
                'status': 'SUCCESS',
                'report': report,
                'report_path': report_path
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e),
                'report': None
            }
    
    def collect_evidence(self, 
                         sources: List[Dict],
                         operation_id: str) -> List[Dict]:
        """
        收集證據
        
        Args:
            sources: 證據源列表 [{'type': 'contract', 'path': 'path/to/contract.yaml'}]
            operation_id: 操作ID
            
        Returns:
            證據鏈列表
        """
        evidence_chain = []
        
        for source in sources:
            try:
                source_type = source.get('type')
                source_path = source.get('path')
                
                # 計算文件哈希
                full_path = self.workspace_path / source_path
                if full_path.exists():
                    with open(full_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    evidence = {
                        'type': source_type,
                        'path': source_path,
                        'hash': file_hash,
                        'size': full_path.stat().st_size,
                        'timestamp': datetime.now().isoformat(),
                        'operation_id': operation_id
                    }
                    
                    evidence_chain.append(evidence)
            except Exception as e:
                print(f"收集證據失敗 {source_path}: {e}")
        
        return evidence_chain
    
    def validate_report(self, 
                        report: Dict,
                        min_evidence_coverage: float = 0.90) -> Dict:
        """
        驗證報告質量
        
        Args:
            report: 要驗證的報告
            min_evidence_coverage: 最小證據覆蓋率閾值
            
        Returns:
            驗證結果
        """
        validation = {
            'has_unverified_claims': False,
            'evidence_coverage': 0.0,
            'forbidden_phrase_violations': [],
            'passed': True,
            'errors': [],
            'warnings': []
        }
        
        # 檢查證據覆蓋率
        report_text = json.dumps(report, ensure_ascii=False)
        
        # 計算證據鏈接
        evidence_pattern = r'\[證據:\s*[^\]]+\]'
        evidence_links = re.findall(evidence_pattern, report_text)
        
        # 計算聲明句數
        statement_pattern = r'[^.!?。？！]+[.!?。？！]'
        statements = re.findall(statement_pattern, report_text)
        total_statements = len(statements)
        
        if total_statements > 0:
            validation['evidence_coverage'] = len(evidence_links) / total_statements
        
        # 檢查覆蓋率閾值
        if validation['evidence_coverage'] < min_evidence_coverage:
            validation['passed'] = False
            validation['errors'].append(
                f"證據覆蓋率不足: {validation['evidence_coverage']:.1%} < {min_evidence_coverage:.1%}"
            )
        
        # 檢查禁止短語
        forbidden_phrases = [
            ("100% 完成", "基於已實現的功能集"),
            ("完全符合", "在[方面]與標準對齊"),
            ("已全部實現", "已實現[具體功能列表]"),
        ]
        
        for phrase, replacement in forbidden_phrases:
            if phrase in report_text:
                validation['forbidden_phrase_violations'].append({
                    'phrase': phrase,
                    'replacement': replacement
                })
                validation['passed'] = False
                validation['warnings'].append(
                    f"發現禁止短語: '{phrase}'，建議替換為 '{replacement}'"
                )
        
        if validation['forbidden_phrase_violations']:
            validation['has_unverified_claims'] = True
        
        return validation
    
    def _save_report(self, 
                     report: Dict, 
                     operation_context: Optional[Dict] = None) -> str:
        """
        保存報告
        
        Args:
            report: 報告內容
            operation_context: 操作上下文
            
        Returns:
            保存的路徑
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if operation_context and 'operation_id' in operation_context:
            filename = f"verification_{operation_context['operation_id']}_{timestamp}.json"
        else:
            filename = f"verification_{timestamp}.json"
        
        report_path = self.output_dir / filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(report_path)
    
    def _generate_mock_report(self, 
                              topics: List[str],
                              operation_context: Optional[Dict] = None) -> Dict:
        """生成模擬報告（當管道不可用時）"""
        return {
            'status': 'MOCK',
            'mock': True,
            'message': '管道不可用，使用模擬報告',
            'topics': topics,
            'operation_context': operation_context,
            'internal_facts': {
                'status': 'collected',
                'count': len(topics)
            },
            'external_context': {
                'status': 'skipped',
                'reason': 'pipeline_not_available'
            }
        }


def main():
    """測試PipelineIntegration"""
    print("=== Pipeline Integration 測試 ===\n")
    
    # 創建集成器
    integration = PipelineIntegration(workspace_path="/workspace/machine-native-ops")
    
    print(f"1. 管道可用性: {'✅ 可用' if integration.pipeline_available else '⚠️ 不可用'}")
    print()
    
    # 測試證據收集
    print("2. 測試證據收集")
    sources = [
        {'type': 'contract', 'path': 'ecosystem/contracts/platforms/gl-platforms.yaml'},
        {'type': 'governance', 'path': 'ecosystem/contracts/naming-governance/gl-naming-ontology.yaml'}
    ]
    evidence = integration.collect_evidence(sources, 'test-op-001')
    print(f"   收集到 {len(evidence)} 個證據:")
    for e in evidence:
        print(f"   - {e['type']}: {e['path']} (hash: {e['hash'][:16]}...)")
    print()
    
    # 測試報告驗證
    print("3. 測試報告驗證")
    test_report = {
        'summary': '根據治理合約[證據: ecosystem/contracts/platforms/gl-platforms.yaml]，平台符合標準。',
        'details': [
            '所有平台都遵循GL命名規範[證據: gl-naming-ontology.yaml]。',
            '驗證結果顯示100%完成。'  # 包含禁止短語
        ]
    }
    validation = integration.validate_report(test_report, min_evidence_coverage=0.90)
    print(f"   驗證通過: {'✅' if validation['passed'] else '❌'}")
    print(f"   證據覆蓋率: {validation['evidence_coverage']:.1%}")
    print(f"   禁止短語違規: {len(validation['forbidden_phrase_violations'])} 個")
    for v in validation['forbidden_phrase_violations']:
        print(f"   - '{v['phrase']}' -> '{v['replacement']}'")
    print()
    
    # 測試執行驗證
    print("4. 測試執行驗證")
    result = integration.run_verification(
        topics=['platform-naming'],
        operation_context={'operation_id': 'test-001', 'operation_type': 'validation'}
    )
    print(f"   狀態: {result['status']}")
    if result.get('report'):
        print(f"   報告已生成: {result.get('report_path', 'N/A')}")
    print()
    
    print("=== Pipeline Integration 測試完成 ===")


if __name__ == "__main__":
    main()
