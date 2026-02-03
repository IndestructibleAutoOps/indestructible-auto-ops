#!/usr/bin/env python3
"""
Apply Meta-Governance to Ecosystem
===================================
工程工具：將 Meta-Governance 應用到整個 ecosystem

執行：語意分析 → 飄移檢測 → 標記注入 → 驗證
"""

# MNGA-002: Import organization needs review
import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FileAnalysis:
    """文件分析結果"""
    path: str
    file_type: str  # python, yaml, shell, markdown
    has_gl_markers: bool
    current_gl_layer: str
    suggested_gl_layer: str
    semantic_category: str
    drift_type: List[str]  # naming, path, semantic, module
    drift_reasons: List[str]
    needs_relocation: bool
    suggested_path: str


@dataclass
class DriftReport:
    """飄移報告"""
    total_files: int
    files_with_drift: int
    drift_by_type: Dict[str, int]
    files_analysis: List[FileAnalysis]
    

class GovernanceApplicator:
    """治理應用器"""
    
    # GL 層級映射：功能 -> GL Layer
    FUNCTION_TO_LAYER = {
        # GL10-29: Operational Layer（運營層）
        'coordination': 'GL10-29',  # 協調組件
        'service-discovery': 'GL10-29',
        'api-gateway': 'GL10-29',
        'communication': 'GL10-29',
        'data-synchronization': 'GL10-29',
        'registry': 'GL10-29',
        'platform-templates': 'GL10-29',
        
        # GL30-49: Execution Layer（執行層）
        'examples': 'GL30-49',
        'hooks': 'GL30-49',
        'enforcers': 'GL30-49',
        
        # GL50-59: Observability Layer（觀測層）
        'monitoring': 'GL50-59',
        
        # GL90-99: Meta Layer（元規範層）
        'meta-governance': 'GL90-99',
        'governance': 'GL90-99',
        'contracts': 'GL90-99',
    }
    
    def __init__(self, root_dir: str = '/workspace/ecosystem'):
        self.root = Path(root_dir)
        self.files_analyzed: List[FileAnalysis] = []
        
    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """分析單個文件"""
        rel_path = str(file_path.relative_to(self.root))
        
        # 確定文件類型
        suffix = file_path.suffix
        file_type = {
            '.py': 'python',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'shell',
            '.md': 'markdown'
        }.get(suffix, 'other')
        
        # 檢查是否有 GL 標記
        has_markers = False
        current_layer = None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(500)  # 只讀前500字符
                has_markers = '@GL-governed' in content
                
                # 提取當前層級
                match = re.search(r'@GL-layer:\s*(\S+)', content)
                if match:
                    current_layer = match.group(1)
        except:
            pass
        
        # 推斷應該的 GL 層級
        suggested_layer = self._infer_gl_layer(rel_path)
        semantic_category = self._infer_semantic_category(rel_path)
        
        # 檢測飄移
        drift_types = []
        drift_reasons = []
        
        if not has_markers:
            drift_types.append('missing_markers')
            drift_reasons.append('缺少 GL 治理標記')
        
        if current_layer and current_layer != suggested_layer:
            drift_types.append('incorrect_layer')
            drift_reasons.append(f'GL 層級不正確：{current_layer} vs {suggested_layer}')
        
        # 檢查路徑是否符合規範
        if not self._is_path_compliant(rel_path):
            drift_types.append('path_non_compliant')
            drift_reasons.append('路徑不符合 GL 命名規範')
        
        return FileAnalysis(
            path=rel_path,
            file_type=file_type,
            has_gl_markers=has_markers,
            current_gl_layer=current_layer or 'none',
            suggested_gl_layer=suggested_layer,
            semantic_category=semantic_category,
            drift_type=drift_types,
            drift_reasons=drift_reasons,
            needs_relocation=False,  # 暫不重定位
            suggested_path=rel_path
        )
    
    def _infer_gl_layer(self, path: str) -> str:
        """推斷 GL 層級"""
        path_lower = path.lower()
        
        # 根據路徑組件推斷
        for keyword, layer in self.FUNCTION_TO_LAYER.items():
            if keyword in path_lower:
                return layer
        
        # 默認運營層
        return 'GL10-29'
    
    def _infer_semantic_category(self, path: str) -> str:
        """推斷語意類別"""
        if 'coordination' in path:
            return 'coordination'
        elif 'governance' in path or 'meta-governance' in path:
            return 'governance'
        elif 'registry' in path:
            return 'registry'
        elif 'platform-templates' in path:
            return 'platform-templates'
        elif 'tools' in path:
            return 'tools'
        elif 'tests' in path:
            return 'testing'
        else:
            return 'general'
    
    def _is_path_compliant(self, path: str) -> bool:
        """檢查路徑是否符合規範"""
        # 簡化檢查：kebab-case 目錄名
        parts = Path(path).parts
        for part in parts[:-1]:  # 排除文件名
            if part.startswith('.'):
                continue
            # 檢查是否為 kebab-case 或已知例外
            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', part):
                if part not in ['tests', 'src', 'configs', 'scripts', 'examples', 'connectors']:
                    return False
        return True
    
    def scan_ecosystem(self) -> DriftReport:
        """掃描整個 ecosystem"""
        print("掃描 ecosystem 目錄...")
        
        # 掃描所有相關文件
        patterns = ['**/*.py', '**/*.yaml', '**/*.yml', '**/*.sh']
        all_files = set()
        
        for pattern in patterns:
            all_files.update(self.root.glob(pattern))
        
        # 排除某些目錄
        exclude_patterns = ['.git', '__pycache__', '*.pyc', 'node_modules']
        
        for file_path in all_files:
            if any(excl in str(file_path) for excl in exclude_patterns):
                continue
            
            if file_path.is_file():
                analysis = self.analyze_file(file_path)
                self.files_analyzed.append(analysis)
        
        # 統計飄移
        files_with_drift = [f for f in self.files_analyzed if f.drift_type]
        
        drift_by_type = {}
        for f in files_with_drift:
            for dtype in f.drift_type:
                drift_by_type[dtype] = drift_by_type.get(dtype, 0) + 1
        
        return DriftReport(
            total_files=len(self.files_analyzed),
            files_with_drift=len(files_with_drift),
            drift_by_type=drift_by_type,
            files_analysis=self.files_analyzed
        )
    
    def generate_markers(self, file_path: str, gl_layer: str, semantic: str) -> str:
        """生成 GL 標記"""
        markers = f"""#
# @GL-governed
# @GL-layer: {gl_layer}
# @GL-semantic: {semantic}
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#"""
        return markers
    
    def apply_markers_to_file(self, file_path: Path, gl_layer: str, semantic: str) -> bool:
        """應用 GL 標記到文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢查是否已有標記
            if '@GL-governed' in content:
                return True  # 已有標記，跳過
            
            # 生成標記
            markers = self.generate_markers(str(file_path), gl_layer, semantic)
            
            # 插入標記
            if file_path.suffix == '.py':
                # Python：在 shebang 後插入
                if content.startswith('#!'):
                    lines = content.split('\n', 1)
                    new_content = lines[0] + '\n' + markers + '\n' + (lines[1] if len(lines) > 1 else '')
                else:
                    new_content = markers + '\n' + content
            
            elif file_path.suffix in ['.yaml', '.yml']:
                # YAML：在文件開頭插入
                new_content = markers + '\n' + content
            
            elif file_path.suffix == '.sh':
                # Shell：在 shebang 後插入
                if content.startswith('#!'):
                    lines = content.split('\n', 1)
                    new_content = lines[0] + '\n' + markers + '\n' + (lines[1] if len(lines) > 1 else '')
                else:
                    new_content = markers + '\n' + content
            
            else:
                return False
            
            # 寫回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
            
        except Exception as e:
            print(f"錯誤處理文件 {file_path}: {e}")
            return False


def main():
    """主函數"""
    print("\n" + "="*80)
    print("Meta-Governance Application - Engineering Mode")
    print("="*80 + "\n")
    
    applicator = GovernanceApplicator()
    
    # 1. 掃描和分析
    print("階段 1: 掃描和分析...")
    report = applicator.scan_ecosystem()
    
    print(f"\n掃描完成：")
    print(f"  總文件數: {report.total_files}")
    print(f"  飄移文件數: {report.files_with_drift}")
    print(f"  飄移率: {report.files_with_drift/report.total_files*100:.1f}%")
    
    print(f"\n飄移類型分佈：")
    for dtype, count in sorted(report.drift_by_type.items(), key=lambda x: -x[1]):
        print(f"  - {dtype}: {count}")
    
    # 2. 生成報告
    print("\n階段 2: 生成飄移報告...")
    
    # 保存詳細報告
    report_path = Path('/workspace/ecosystem/governance/meta-governance/DRIFT_ANALYSIS_REPORT.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump({
            'generated_at': datetime.utcnow().isoformat(),
            'summary': {
                'total_files': report.total_files,
                'files_with_drift': report.files_with_drift,
                'drift_by_type': report.drift_by_type
            },
            'files': [asdict(f) for f in report.files_analysis]
        }, f, indent=2)
    
    print(f"✓ 報告已保存: {report_path}")
    
    # 3. 應用標記
    print("\n階段 3: 應用 GL 標記...")
    
    applied = 0
    skipped = 0
    
    for file_analysis in report.files_analysis:
        if 'missing_markers' in file_analysis.drift_type:
            file_path = applicator.root / file_analysis.path
            
            # 跳過測試文件和文檔
            if '/tests/' in file_analysis.path or file_analysis.file_type == 'markdown':
                skipped += 1
                continue
            
            success = applicator.apply_markers_to_file(
                file_path,
                file_analysis.suggested_gl_layer,
                file_analysis.semantic_category
            )
            
            if success:
                applied += 1
    
    print(f"\n✓ GL 標記應用完成:")
    print(f"  已添加標記: {applied}")
    print(f"  已跳過: {skipped}")
    
    print("\n" + "="*80)
    print("✅ Meta-Governance 應用完成")
    print("="*80 + "\n")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
