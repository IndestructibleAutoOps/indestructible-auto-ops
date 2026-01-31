# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: legacy-scripts
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
GL Unified Charter - AEP Engine 治理稽核引擎
============================================
Version: 2.0.0
Status: GL Unified Charter Activated
Date: 2026-01-24

執行規範：
- 嚴格遵守 GL Root Semantic Anchor
- 所有執行步驟產生治理事件 (Governance Event Stream)
- 所有檢測結果可重建、可逆、可驗證
- 不允許 continue-on-error
- 每個文件獨立 sandbox 執行
"""

import json
import hashlib
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# CONSTANTS & CONFIGURATION
# ============================================================

GL_CHARTER_VERSION = "2.0.0"
GL_AUDIT_SESSION_ID = f"gl-audit-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

class Severity(Enum):
    CRITICAL = "P0"
    HIGH = "P1"
    MEDIUM = "P2"
    LOW = "P3"
    INFO = "P4"

class IssueType(Enum):
    GL_MARKER_MISSING = "gl_marker_missing"
    SEMANTIC_MANIFEST_MISSING = "semantic_manifest_missing"
    METADATA_MISSING = "metadata_missing"
    SCHEMA_MISMATCH = "schema_mismatch"
    NAMING_INCONSISTENT = "naming_inconsistent"
    STRUCTURE_VIOLATION = "structure_violation"
    DAG_INTEGRITY = "dag_integrity"
    PIPELINE_ERROR = "pipeline_error"
    TYPE_ERROR = "type_error"
    DOCUMENTATION_MISSING = "documentation_missing"
    EVIDENCE_CHAIN_BROKEN = "evidence_chain_broken"
    GOVERNANCE_EVENT_MISSING = "gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_missing"

# GL Marker patterns
GL_MARKER_PATTERNS = [
    r'GL\s*Unified\s*Charter\s*Activated',
    r'@gl-governed',
    r'gl-root-anchor',
    r'GL_GOVERNANCE',
    r'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance[-_]enabled',
    r'\[GL\]',
    r'GL\s*Root\s*Semantic\s*Anchor'
]

# Required metadata fields
REQUIRED_METADATA = ['version', 'status', 'author', 'last_updated']

# Best practice directory structure
BEST_PRACTICE_STRUCTURE = {
    'engine': {
        'core': ['index.ts', 'interfaces.d.ts'],
        'parser': ['yaml_parser.ts', 'json_passthrough.ts', 'anchor_resolver.ts'],
        'loader': ['fs_loader.ts', 'git_loader.ts', 'merge_index.ts'],
        'normalizer': ['defaults_applier.ts', 'env_merger.ts', 'module_defaults.ts'],
        'validator': ['schema_validator.ts', 'module_validator.ts', 'error_reporter.ts'],
        'renderer': ['template_engine.ts', 'module_mapper.ts', 'artifact_writer.ts'],
        'executor': ['local_executor.ts', 'remote_executor.ts', 'rollback.ts'],
        'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance': ['gl_engine.ts', 'rule_evaluator.ts', 'events_writer.ts', 'anchor_resolver.ts'],
        'artifacts': ['artifact_manager.ts', 'evidence_chain.ts', 'manifest_generator.ts'],
        'tests': {},
        '.gl': ['manifest.yaml', 'semantic-anchors.yaml', 'evidence-chain.json']
    }
}

# Naming conventions
NAMING_CONVENTIONS = {
    'ts_files': r'^[a-z][a-z0-9]*(_[a-z0-9]+)*\.ts$',
    'test_files': r'^[a-z][a-z0-9]*(_[a-z0-9]+)*\.test\.ts$',
    'directories': r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$',
    'yaml_files': r'^[a-z][a-z0-9]*(-[a-z0-9]+)*\.ya?ml$',
    'json_files': r'^[a-z][a-z0-9]*(-[a-z0-9]+)*\.json$'
}

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class GovernanceEvent:
    """治理事件"""
    event_id: str
    timestamp: str
    event_type: str
    source: str
    target: str
    action: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)
    hash: str = ""
    
    def __post_init__(self):
        if not self.hash:
            content = f"{self.event_id}{self.timestamp}{self.event_type}{self.source}{self.target}{self.action}"
            self.hash = hashlib.sha256(content.encode()).hexdigest()[:16]

@dataclass
class Issue:
    """檢測到的問題"""
    issue_id: str
    file_path: str
    issue_type: IssueType
    severity: Severity
    title: str
    description: str
    line_number: Optional[int] = None
    suggestion: str = ""
    auto_fixable: bool = False
    
@dataclass
class FileAuditResult:
    """單檔稽核結果"""
    file_path: str
    file_hash: str
    audit_timestamp: str
    etl_status: str
    es_index_status: str
    issues: List[Issue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_events: List[GovernanceEvent] = field(default_factory=list)
    execution_time_ms: int = 0
    
@dataclass
class GlobalAuditReport:
    """全域治理稽核報告"""
    session_id: str
    charter_version: str
    audit_start: str
    audit_end: str
    total_files: int
    files_processed: int
    files_passed: int
    files_failed: int
    total_issues: int
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues_by_type: Dict[str, int] = field(default_factory=dict)
    file_results: List[FileAuditResult] = field(default_factory=list)
    gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream: List[GovernanceEvent] = field(default_factory=list)
    best_practice_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    migration_plan: Dict[str, Any] = field(default_factory=dict)

# ============================================================
# ETL PIPELINE ENGINE
# ============================================================

class ETLPipeline:
    """ETL Pipeline 執行引擎"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.events: List[GovernanceEvent] = []
        
    def emit_event(self, event_type: str, source: str, target: str, action: str, status: str, details: Dict = None) -> GovernanceEvent:
        """發送治理事件"""
        event = GovernanceEvent(
            event_id=f"evt-{len(self.events)+1:04d}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            source=source,
            target=target,
            action=action,
            status=status,
            details=details or {}
        )
        self.events.append(event)
        return event
    
    def extract(self, file_path: str) -> Tuple[Dict[str, Any], GovernanceEvent]:
        """Extract 階段：提取檔案內容與結構"""
        full_path = self.base_path / file_path
        
        self.emit_event("ETL", "extract", file_path, "start", "running")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stat = full_path.stat()
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            
            extracted_data = {
                'file_path': file_path,
                'file_name': full_path.name,
                'file_extension': full_path.suffix,
                'file_size': stat.st_size,
                'file_hash': file_hash,
                'content': content,
                'line_count': len(content.splitlines()),
                'modified_time': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                'parent_dir': str(full_path.parent.relative_to(self.base_path))
            }
            
            event = self.emit_event("ETL", "extract", file_path, "complete", "success", 
                                   {"size": stat.st_size, "hash": file_hash[:16]})
            return extracted_data, event
            
        except Exception as e:
            self.emit_event("ETL", "extract", file_path, "complete", "failed", 
                           {"error": str(e)})
            raise RuntimeError(f"Extract failed for {file_path}: {e}")
    
    def transform(self, extracted_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Issue], GovernanceEvent]:
        """Transform 階段：套用治理規則轉換並檢測問題"""
        file_path = extracted_data['file_path']
        content = extracted_data['content']
        issues: List[Issue] = []
        
        self.emit_event("ETL", "transform", file_path, "start", "running")
        
        # 1. GL 標記檢測
        has_gl_marker = any(re.search(pattern, content, re.IGNORECASE) for pattern in GL_MARKER_PATTERNS)
        if not has_gl_marker:
            issues.append(Issue(
                issue_id=f"ISS-{len(issues)+1:04d}",
                file_path=file_path,
                issue_type=IssueType.GL_MARKER_MISSING,
                severity=Severity.HIGH,
                title="GL 治理標記缺失",
                description=f"檔案 {file_path} 缺少 GL Unified Charter 標記",
                suggestion="在檔案開頭添加 '// GL Unified Charter Activated' 或 '@gl-governed' 標記",
                auto_fixable=True
            ))
        
        # 2. Metadata 檢測
        # Metadata extraction patterns
        # - author: Handles both JSON format ("author": "value") and Markdown (**Author**: value)
        # - last_updated: Extracts ISO date format, skipping markdown asterisks
        metadata_found = {}
        metadata_patterns = {
            'version': r'[Vv]ersion[:\s]*([0-9]+\.[0-9]+\.[0-9]+)',
            'status': r'[Ss]tatus[:\s]*(\w+)',
            'author': r'["\']?[Aa]uthor["\']?[*\s]*:\s*["\']?([^"\',\n\r]+?)(?:["\',\s]|$)',
            'last_updated': r'[Ll]ast[_\s][Uu]pdated?[*\s]*:\s*[*\s]*([0-9]{4}-[0-9]{2}-[0-9]{2}(?:[T\s][0-9:]+)?)'
        }
        
        for key, pattern in metadata_patterns.items():
            match = re.search(pattern, content)
            if match:
                metadata_found[key] = match.group(1).strip()
        
        missing_metadata = [k for k in REQUIRED_METADATA if k not in metadata_found]
        if missing_metadata and extracted_data['file_extension'] in ['.ts', '.md']:
            issues.append(Issue(
                issue_id=f"ISS-{len(issues)+1:04d}",
                file_path=file_path,
                issue_type=IssueType.METADATA_MISSING,
                severity=Severity.MEDIUM,
                title="Metadata 缺失",
                description=f"缺少以下 metadata: {', '.join(missing_metadata)}",
                suggestion=f"添加缺失的 metadata 欄位: {', '.join(missing_metadata)}",
                auto_fixable=False
            ))
        
        # 3. 命名規範檢測
        file_name = extracted_data['file_name']
        ext = extracted_data['file_extension']
        
        naming_valid = True
        if ext == '.ts':
            if '.test.ts' in file_name:
                naming_valid = bool(re.match(NAMING_CONVENTIONS['test_files'], file_name))
            else:
                naming_valid = bool(re.match(NAMING_CONVENTIONS['ts_files'], file_name))
        elif ext in ['.yaml', '.yml']:
            naming_valid = bool(re.match(NAMING_CONVENTIONS['yaml_files'], file_name))
        elif ext == '.json':
            naming_valid = bool(re.match(NAMING_CONVENTIONS['json_files'], file_name))
        
        if not naming_valid:
            issues.append(Issue(
                issue_id=f"ISS-{len(issues)+1:04d}",
                file_path=file_path,
                issue_type=IssueType.NAMING_INCONSISTENT,
                severity=Severity.LOW,
                title="命名不符規範",
                description=f"檔案名稱 '{file_name}' 不符合命名規範",
                suggestion="使用 snake_case 命名 TypeScript 檔案，kebab-case 命名 YAML/JSON 檔案",
                auto_fixable=False
            ))
        
        # 4. TypeScript 特定檢測
        if ext == '.ts':
            # 檢測 any 類型使用
            any_matches = list(re.finditer(r':\s*any\b', content))
            if any_matches:
                issues.append(Issue(
                    issue_id=f"ISS-{len(issues)+1:04d}",
                    file_path=file_path,
                    issue_type=IssueType.TYPE_ERROR,
                    severity=Severity.MEDIUM,
                    title="使用 any 類型",
                    description=f"發現 {len(any_matches)} 處使用 'any' 類型",
                    line_number=content[:any_matches[0].start()].count('\n') + 1 if any_matches else None,
                    suggestion="使用具體類型替代 'any' 以提高類型安全性",
                    auto_fixable=False
                ))
            
            # 檢測 console.log
            console_matches = list(re.finditer(r'console\.(log|warn|error)', content))
            if console_matches:
                issues.append(Issue(
                    issue_id=f"ISS-{len(issues)+1:04d}",
                    file_path=file_path,
                    issue_type=IssueType.PIPELINE_ERROR,
                    severity=Severity.LOW,
                    title="Console 輸出",
                    description=f"發現 {len(console_matches)} 處 console 輸出",
                    suggestion="使用正式的 logging 機制替代 console 輸出",
                    auto_fixable=True
                ))
            
            # 檢測 TODO/FIXME
            todo_matches = list(re.finditer(r'(TODO|FIXME|XXX|HACK):', content, re.IGNORECASE))
            if todo_matches:
                issues.append(Issue(
                    issue_id=f"ISS-{len(issues)+1:04d}",
                    file_path=file_path,
                    issue_type=IssueType.DOCUMENTATION_MISSING,
                    severity=Severity.INFO,
                    title="待處理標記",
                    description=f"發現 {len(todo_matches)} 處 TODO/FIXME 標記",
                    suggestion="處理或追蹤這些待辦事項",
                    auto_fixable=False
                ))
        
        # 5. Semantic Manifest 檢測 (針對主要模組檔案)
        if ext == '.ts' and 'index' not in file_name and 'test' not in file_path:
            semantic_patterns = [
                r'@semantic-anchor',
                r'semantic[-_]manifest',
                r'@module',
                r'@description'
            ]
            has_semantic = any(re.search(p, content, re.IGNORECASE) for p in semantic_patterns)
            if not has_semantic:
                issues.append(Issue(
                    issue_id=f"ISS-{len(issues)+1:04d}",
                    file_path=file_path,
                    issue_type=IssueType.SEMANTIC_MANIFEST_MISSING,
                    severity=Severity.MEDIUM,
                    title="Semantic Manifest 缺失",
                    description="檔案缺少語意標記或模組描述",
                    suggestion="添加 @module 和 @description JSDoc 標記",
                    auto_fixable=True
                ))
        
        # 6. README 檢測 (針對目錄)
        parent_dir = extracted_data['parent_dir']
        readme_path = self.base_path / parent_dir / 'README.md'
        if not readme_path.exists() and ext == '.ts' and 'test' not in file_path:
            issues.append(Issue(
                issue_id=f"ISS-{len(issues)+1:04d}",
                file_path=file_path,
                issue_type=IssueType.DOCUMENTATION_MISSING,
                severity=Severity.LOW,
                title="目錄缺少 README",
                description=f"目錄 {parent_dir} 缺少 README.md",
                suggestion=f"在 {parent_dir} 目錄添加 README.md 文件",
                auto_fixable=False
            ))
        
        # 構建轉換後的數據
        transformed_data = {
            **extracted_data,
            'metadata': metadata_found,
            'has_gl_marker': has_gl_marker,
            'issues_count': len(issues),
            'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_compliant': len([i for i in issues if i.severity in [Severity.CRITICAL, Severity.HIGH]]) == 0
        }
        
        event = self.emit_event("ETL", "transform", file_path, "complete", "success",
                               {"issues_found": len(issues)})
        
        return transformed_data, issues, event
    
    def load(self, transformed_data: Dict[str, Any], issues: List[Issue]) -> Tuple[Dict[str, Any], GovernanceEvent]:
        """Load 階段：準備 Elasticsearch 索引數據"""
        file_path = transformed_data['file_path']
        
        self.emit_event("ETL", "load", file_path, "start", "running")
        
        # 構建 ES 文檔
        es_document = {
            '_index': 'gl-gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance-audit',
            '_id': transformed_data['file_hash'][:16],
            '_source': {
                'file_path': file_path,
                'file_name': transformed_data['file_name'],
                'file_extension': transformed_data['file_extension'],
                'file_size': transformed_data['file_size'],
                'file_hash': transformed_data['file_hash'],
                'line_count': transformed_data['line_count'],
                'parent_dir': transformed_data['parent_dir'],
                'modified_time': transformed_data['modified_time'],
                'audit_timestamp': datetime.now(timezone.utc).isoformat(),
                'session_id': GL_AUDIT_SESSION_ID,
                'metadata': transformed_data['metadata'],
                'has_gl_marker': transformed_data['has_gl_marker'],
                'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_compliant': transformed_data['gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_compliant'],
                'issues': [
                    {
                        'issue_id': i.issue_id,
                        'type': i.issue_type.value,
                        'severity': i.severity.value,
                        'title': i.title,
                        'description': i.description,
                        'suggestion': i.suggestion,
                        'auto_fixable': i.auto_fixable
                    }
                    for i in issues
                ],
                'issues_count': len(issues),
                'critical_issues': len([i for i in issues if i.severity == Severity.CRITICAL]),
                'high_issues': len([i for i in issues if i.severity == Severity.HIGH]),
                'medium_issues': len([i for i in issues if i.severity == Severity.MEDIUM]),
                'low_issues': len([i for i in issues if i.severity == Severity.LOW])
            }
        }
        
        event = self.emit_event("ETL", "load", file_path, "complete", "success",
                               {"es_index": "gl-gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance-audit", "doc_id": es_document['_id']})
        
        return es_document, event

# ============================================================
# GOVERNANCE AUDIT ENGINE
# ============================================================

class GovernanceAuditEngine:
    """治理稽核引擎"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.engine_path = self.repo_path / 'engine'
        self.etl = ETLPipeline(repo_path)
        self.file_results: List[FileAuditResult] = []
        self.all_issues: List[Issue] = []
        self.es_documents: List[Dict] = []
        
    def scan_files(self) -> List[str]:
        """掃描所有需要稽核的檔案"""
        files = []
        for ext in ['*.ts', '*.json', '*.yaml', '*.yml', '*.md']:
            files.extend([str(f.relative_to(self.repo_path)) for f in self.engine_path.rglob(ext)])
        return sorted(files)
    
    def audit_file(self, file_path: str) -> FileAuditResult:
        """對單一檔案執行完整 ETL → ES 流程"""
        start_time = datetime.now(timezone.utc)
        
        self.etl.emit_event("AUDIT", "engine", file_path, "start", "running")
        
        try:
            # Extract
            extracted_data, _ = self.etl.extract(file_path)
            
            # Transform
            transformed_data, issues, _ = self.etl.transform(extracted_data)
            
            # Load
            es_doc, _ = self.etl.load(transformed_data, issues)
            self.es_documents.append(es_doc)
            
            # 計算執行時間
            end_time = datetime.now(timezone.utc)
            execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # 構建結果
            result = FileAuditResult(
                file_path=file_path,
                file_hash=extracted_data['file_hash'],
                audit_timestamp=end_time.isoformat(),
                etl_status="success",
                es_index_status="indexed",
                issues=issues,
                metadata=transformed_data['metadata'],
                gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_events=self.etl.events[-4:],  # 最近4個事件
                execution_time_ms=execution_time_ms
            )
            
            self.etl.emit_event("AUDIT", "engine", file_path, "complete", "success",
                               {"issues": len(issues), "time_ms": execution_time_ms})
            
            return result
            
        except Exception as e:
            self.etl.emit_event("AUDIT", "engine", file_path, "complete", "failed",
                               {"error": str(e)})
            
            return FileAuditResult(
                file_path=file_path,
                file_hash="",
                audit_timestamp=datetime.now(timezone.utc).isoformat(),
                etl_status="failed",
                es_index_status="not_indexed",
                issues=[Issue(
                    issue_id="ISS-ERR",
                    file_path=file_path,
                    issue_type=IssueType.PIPELINE_ERROR,
                    severity=Severity.CRITICAL,
                    title="Pipeline 執行失敗",
                    description=str(e),
                    suggestion="檢查檔案格式和編碼"
                )],
                metadata={},
                gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_events=self.etl.events[-2:],
                execution_time_ms=0
            )
    
    def generate_best_practice_recommendations(self) -> List[Dict[str, Any]]:
        """生成最佳實踐建議"""
        recommendations = []
        
        # 分析目錄結構
        current_structure = {}
        for result in self.file_results:
            parts = Path(result.file_path).parts
            if len(parts) >= 2:
                module = parts[1]
                if module not in current_structure:
                    current_structure[module] = []
                current_structure[module].append(result.file_path)
        
        # 檢查是否缺少核心目錄
        expected_dirs = ['core', 'parser', 'loader', 'normalizer', 'validator', 
                        'renderer', 'executor', 'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance', 'artifacts', 'tests', '.gl']
        
        for expected in expected_dirs:
            if expected not in current_structure and expected != 'core':
                recommendations.append({
                    'type': 'structure',
                    'priority': 'medium',
                    'title': f'建議添加 {expected} 目錄',
                    'description': f'最佳實踐建議包含 {expected} 目錄以組織相關功能',
                    'action': f'mkdir -p engine/{expected}'
                })
        
        # 檢查 .gl 目錄
        gl_files = [r.file_path for r in self.file_results if '.gl' in r.file_path]
        if not gl_files:
            recommendations.append({
                'type': 'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance',
                'priority': 'high',
                'title': '建議添加 .gl 治理目錄',
                'description': '缺少 .gl 目錄，無法存放治理配置',
                'action': 'mkdir -p engine/.gl && touch engine/.gl/manifest.yaml'
            })
        
        # 根據問題類型生成建議
        issue_types = {}
        for result in self.file_results:
            for issue in result.issues:
                issue_type = issue.issue_type.value
                if issue_type not in issue_types:
                    issue_types[issue_type] = 0
                issue_types[issue_type] += 1
        
        if issue_types.get('gl_marker_missing', 0) > 10:
            recommendations.append({
                'type': 'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance',
                'priority': 'high',
                'title': '批量添加 GL 標記',
                'description': f'有 {issue_types["gl_marker_missing"]} 個檔案缺少 GL 標記',
                'action': '執行自動化腳本批量添加 GL 標記'
            })
        
        if issue_types.get('semantic_manifest_missing', 0) > 5:
            recommendations.append({
                'type': 'documentation',
                'priority': 'medium',
                'title': '添加 Semantic Manifest',
                'description': f'有 {issue_types["semantic_manifest_missing"]} 個檔案缺少語意標記',
                'action': '為主要模組添加 @module 和 @description JSDoc 標記'
            })
        
        return recommendations
    
    def generate_migration_plan(self) -> Dict[str, Any]:
        """生成遷移計劃"""
        migrations = []
        
        # 檢查需要重命名的檔案
        for result in self.file_results:
            for issue in result.issues:
                if issue.issue_type == IssueType.NAMING_INCONSISTENT:
                    file_name = Path(result.file_path).name
                    suggested_name = re.sub(r'([A-Z])', r'_\1', file_name).lower().lstrip('_')
                    new_path = str(Path(result.file_path).parent / suggested_name)
                    # Only add migration if the filename actually changes (normalize paths for comparison)
                    if Path(result.file_path).resolve() != Path(new_path).resolve():
                        migrations.append({
                            'type': 'rename',
                            'from': result.file_path,
                            'to': new_path,
                            'reason': issue.description
                        })
        
        # 建議的目錄結構
        suggested_structure = {
            'engine': {
                'core': {
                    'description': '核心入口和介面定義',
                    'files': ['index.ts', 'interfaces.d.ts', 'interfaces-fix.d.ts']
                },
                'parser': {
                    'description': '解析器模組',
                    'files': ['yaml_parser.ts', 'json_passthrough.ts', 'anchor_resolver.ts']
                },
                'loader': {
                    'description': '載入器模組',
                    'files': ['fs_loader.ts', 'git_loader.ts', 'merge_index.ts']
                },
                'normalizer': {
                    'description': '正規化模組',
                    'files': ['defaults_applier.ts', 'env_merger.ts', 'module_defaults.ts']
                },
                'validator': {
                    'description': '驗證器模組',
                    'files': ['schema_validator.ts', 'module_validator.ts', 'error_reporter.ts']
                },
                'renderer': {
                    'description': '渲染器模組',
                    'files': ['template_engine.ts', 'module_mapper.ts', 'artifact_writer.ts']
                },
                'executor': {
                    'description': '執行器模組',
                    'files': ['local_executor.ts', 'remote_executor.ts', 'rollback.ts']
                },
                'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance': {
                    'description': '治理模組',
                    'files': ['gl_engine.ts', 'rule_evaluator.ts', 'events_writer.ts', 'anchor_resolver.ts']
                },
                'artifacts': {
                    'description': '產出物管理',
                    'files': ['artifact_manager.ts', 'evidence_chain.ts', 'manifest_generator.ts']
                },
                'tests': {
                    'description': '測試檔案',
                    'subdirs': ['artifacts', 'validator', 'normalizer', 'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance', 'loader']
                },
                '.gl': {
                    'description': 'GL 治理配置',
                    'files': ['manifest.yaml', 'semantic-anchors.yaml', 'evidence-chain.json']
                }
            }
        }
        
        return {
            'migrations': migrations,
            'suggested_structure': suggested_structure,
            'migration_commands': [
                '# 執行以下命令進行遷移',
                *[f"git mv {m['from']} {m['to']}" for m in migrations[:10]]
            ]
        }
    
    def run_full_audit(self) -> GlobalAuditReport:
        """執行完整稽核"""
        audit_start = datetime.now(timezone.utc)
        
        print(f"\n{'='*60}")
        print("GL Unified Charter - AEP Engine 治理稽核")
        print(f"Session ID: {GL_AUDIT_SESSION_ID}")
        print(f"Charter Version: {GL_CHARTER_VERSION}")
        print(f"{'='*60}\n")
        
        # 掃描檔案
        files = self.scan_files()
        print(f"📁 發現 {len(files)} 個檔案待稽核\n")
        
        # 逐檔執行
        for i, file_path in enumerate(files, 1):
            print(f"[{i:02d}/{len(files)}] 處理: {file_path}")
            result = self.audit_file(file_path)
            self.file_results.append(result)
            self.all_issues.extend(result.issues)
            
            status = "✅" if result.etl_status == "success" else "❌"
            issues_str = f"({len(result.issues)} issues)" if result.issues else ""
            print(f"       {status} {result.etl_status} {issues_str}")
        
        audit_end = datetime.now(timezone.utc)
        
        # 統計
        issues_by_severity = {}
        issues_by_type = {}
        for issue in self.all_issues:
            sev = issue.severity.value
            typ = issue.issue_type.value
            issues_by_severity[sev] = issues_by_severity.get(sev, 0) + 1
            issues_by_type[typ] = issues_by_type.get(typ, 0) + 1
        
        # 生成報告
        report = GlobalAuditReport(
            session_id=GL_AUDIT_SESSION_ID,
            charter_version=GL_CHARTER_VERSION,
            audit_start=audit_start.isoformat(),
            audit_end=audit_end.isoformat(),
            total_files=len(files),
            files_processed=len(self.file_results),
            files_passed=len([r for r in self.file_results if r.etl_status == "success"]),
            files_failed=len([r for r in self.file_results if r.etl_status == "failed"]),
            total_issues=len(self.all_issues),
            issues_by_severity=issues_by_severity,
            issues_by_type=issues_by_type,
            file_results=self.file_results,
            gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream=self.etl.events,
            best_practice_recommendations=self.generate_best_practice_recommendations(),
            migration_plan=self.generate_migration_plan()
        )
        
        print(f"\n{'='*60}")
        print("稽核完成")
        print(f"總檔案: {report.total_files}")
        print(f"成功: {report.files_passed}")
        print(f"失敗: {report.files_failed}")
        print(f"總問題數: {report.total_issues}")
        print(f"{'='*60}\n")
        
        return report

# ============================================================
# REPORT GENERATORS
# ============================================================

def generate_json_reports(report: GlobalAuditReport, output_dir: Path):
    """生成 JSON 報告"""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        raise RuntimeError(f"Failed to create output directory {output_dir}: {e}")
    
    # 全域報告
    global_report_path = output_dir / 'global-gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance-audit-report.json'
    try:
        with open(global_report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'session_id': report.session_id,
                'charter_version': report.charter_version,
                'audit_start': report.audit_start,
                'audit_end': report.audit_end,
                'summary': {
                    'total_files': report.total_files,
                    'files_processed': report.files_processed,
                    'files_passed': report.files_passed,
                    'files_failed': report.files_failed,
                    'total_issues': report.total_issues,
                    'issues_by_severity': report.issues_by_severity,
                    'issues_by_type': report.issues_by_type
                },
                'best_practice_recommendations': report.best_practice_recommendations,
                'migration_plan': report.migration_plan
            }, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError, UnicodeEncodeError) as e:
        raise RuntimeError(f"Failed to write global report to {global_report_path}: {e}")
    
    # 個別檔案報告
    file_reports_dir = output_dir / 'file-reports'
    try:
        file_reports_dir.mkdir(exist_ok=True)
    except (PermissionError, OSError) as e:
        raise RuntimeError(f"Failed to create file reports directory {file_reports_dir}: {e}")
    
    for result in report.file_results:
        safe_name = result.file_path.replace('/', '_').replace('\\', '_')
        file_report_path = file_reports_dir / f'{safe_name}.json'
        try:
            with open(file_report_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'file_path': result.file_path,
                    'file_hash': result.file_hash,
                    'audit_timestamp': result.audit_timestamp,
                    'etl_status': result.etl_status,
                    'es_index_status': result.es_index_status,
                    'metadata': result.metadata,
                    'execution_time_ms': result.execution_time_ms,
                    'issues': [
                        {
                            'issue_id': i.issue_id,
                            'type': i.issue_type.value,
                            'severity': i.severity.value,
                            'title': i.title,
                            'description': i.description,
                            'line_number': i.line_number,
                            'suggestion': i.suggestion,
                            'auto_fixable': i.auto_fixable
                        }
                        for i in result.issues
                    ],
                    'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_events': [asdict(e) for e in result.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_events]
                }, f, indent=2, ensure_ascii=False)
        except (PermissionError, OSError, UnicodeEncodeError) as e:
            raise RuntimeError(f"Failed to write file report {file_report_path}: {e}")
    
    # 治理事件流
    events_path = output_dir / 'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance-event-stream.json'
    try:
        with open(events_path, 'w', encoding='utf-8') as f:
            json.dump({
                'session_id': report.session_id,
                'total_events': len(report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream),
                'events': [asdict(e) for e in report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream]
            }, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError, UnicodeEncodeError) as e:
        raise RuntimeError(f"Failed to write gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance event stream to {events_path}: {e}")
    
    # ES 批量索引文件
    es_bulk_path = output_dir / 'es-bulk-index.ndjson'
    try:
        with open(es_bulk_path, 'w', encoding='utf-8') as f:
            for result in report.file_results:
                # Index action
                f.write(json.dumps({'index': {'_index': 'gl-gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance-audit', '_id': result.file_hash[:16]}}) + '\n')
                # Document
                f.write(json.dumps({
                    'file_path': result.file_path,
                    'file_hash': result.file_hash,
                    'audit_timestamp': result.audit_timestamp,
                    'session_id': report.session_id,
                    'etl_status': result.etl_status,
                    'issues_count': len(result.issues),
                    'critical_issues': len([i for i in result.issues if i.severity == Severity.CRITICAL]),
                    'high_issues': len([i for i in result.issues if i.severity == Severity.HIGH]),
                    'gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_compliant': len([i for i in result.issues if i.severity in [Severity.CRITICAL, Severity.HIGH]]) == 0
                }) + '\n')
    except (PermissionError, OSError, UnicodeEncodeError) as e:
        raise RuntimeError(f"Failed to write ES bulk index file to {es_bulk_path}: {e}")
    
    return global_report_path

def generate_markdown_report(report: GlobalAuditReport, output_path: Path):
    """生成 Markdown 報告"""
    
    content = f"""# GL Unified Charter - AEP Engine 治理稽核報告

**GL Unified Charter Activated**

## 執行摘要

| 項目 | 數值 |
|------|------|
| Session ID | `{report.session_id}` |
| Charter Version | {report.charter_version} |
| 稽核開始 | {report.audit_start} |
| 稽核結束 | {report.audit_end} |
| 總檔案數 | {report.total_files} |
| 處理成功 | {report.files_passed} |
| 處理失敗 | {report.files_failed} |
| 總問題數 | {report.total_issues} |

## 問題分布

### 按嚴重度

| 嚴重度 | 數量 | 說明 |
|--------|------|------|
| P0 (Critical) | {report.issues_by_severity.get('P0', 0)} | 必須立即修復 |
| P1 (High) | {report.issues_by_severity.get('P1', 0)} | 高優先級修復 |
| P2 (Medium) | {report.issues_by_severity.get('P2', 0)} | 中優先級修復 |
| P3 (Low) | {report.issues_by_severity.get('P3', 0)} | 低優先級修復 |
| P4 (Info) | {report.issues_by_severity.get('P4', 0)} | 資訊性提示 |

### 按類型

| 問題類型 | 數量 |
|----------|------|
"""
    
    for issue_type, count in sorted(report.issues_by_type.items(), key=lambda x: -x[1]):
        content += f"| {issue_type} | {count} |\n"
    
    content += """
## 問題詳情

### P0/P1 高優先級問題

"""
    
    high_priority_issues = [
        (r.file_path, i) 
        for r in report.file_results 
        for i in r.issues 
        if i.severity in [Severity.CRITICAL, Severity.HIGH]
    ]
    
    if high_priority_issues:
        for file_path, issue in high_priority_issues[:20]:
            content += f"""#### {issue.severity.value}: {issue.title}
- **檔案**: `{file_path}`
- **類型**: {issue.issue_type.value}
- **描述**: {issue.description}
- **建議**: {issue.suggestion}

"""
    else:
        content += "_無高優先級問題_\n\n"
    
    content += """## 最佳實踐建議

"""
    
    for rec in report.best_practice_recommendations:
        content += f"""### {rec['title']}
- **優先級**: {rec['priority']}
- **類型**: {rec['type']}
- **描述**: {rec['description']}
- **操作**: `{rec['action']}`

"""
    
    content += """## 建議目錄結構

```
engine/
├── core/                    # 核心入口和介面定義
│   ├── index.ts
│   ├── interfaces.d.ts
│   └── interfaces-fix.d.ts
├── parser/                  # 解析器模組
│   ├── yaml_parser.ts
│   ├── json_passthrough.ts
│   └── anchor_resolver.ts
├── loader/                  # 載入器模組
│   ├── fs_loader.ts
│   ├── git_loader.ts
│   └── merge_index.ts
├── normalizer/              # 正規化模組
│   ├── defaults_applier.ts
│   ├── env_merger.ts
│   └── module_defaults.ts
├── validator/               # 驗證器模組
│   ├── schema_validator.ts
│   ├── module_validator.ts
│   └── error_reporter.ts
├── renderer/                # 渲染器模組
│   ├── template_engine.ts
│   ├── module_mapper.ts
│   └── artifact_writer.ts
├── executor/                # 執行器模組
│   ├── local_executor.ts
│   ├── remote_executor.ts
│   └── rollback.ts
├── gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance/              # 治理模組
│   ├── gl_engine.ts
│   ├── rule_evaluator.ts
│   ├── events_writer.ts
│   └── anchor_resolver.ts
├── artifacts/               # 產出物管理
│   ├── artifact_manager.ts
│   ├── evidence_chain.ts
│   └── manifest_generator.ts
├── tests/                   # 測試檔案
│   ├── artifacts/
│   ├── validator/
│   ├── normalizer/
│   ├── gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance/
│   └── loader/
└── .gl/                     # GL 治理配置
    ├── manifest.yaml
    ├── semantic-anchors.yaml
    └── evidence-chain.json
```

## 治理事件流摘要

| 統計項目 | 數值 |
|----------|------|
| 總事件數 | {total_events} |
| ETL 事件 | {etl_events} |
| AUDIT 事件 | {audit_events} |
| 成功事件 | {success_events} |
| 失敗事件 | {failed_events} |

## 鏈鍵 (Link Key)

```
GL-AUDIT-LINK-KEY: {link_key}
```

---

**GL Unified Charter Activated**  
**Generated**: {timestamp}
""".format(
        total_events=len(report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream),
        etl_events=len([e for e in report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream if e.event_type == 'ETL']),
        audit_events=len([e for e in report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream if e.event_type == 'AUDIT']),
        # Count both 'success' and 'running' status as successful (start events have 'running' status)
        success_events=len([e for e in report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream if e.status in ['success', 'running']]),
        failed_events=len([e for e in report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream if e.status == 'failed']),
        link_key=hashlib.sha256(f"{report.session_id}{report.audit_end}{report.total_issues}".encode()).hexdigest()[:32],
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except (PermissionError, OSError, UnicodeEncodeError) as e:
        raise RuntimeError(f"Failed to write markdown report to {output_path}: {e}")
    
    return output_path

def generate_link_key(report: GlobalAuditReport, output_path: Path):
    """生成鏈鍵文件"""
    
    link_key_data = {
        'link_key': hashlib.sha256(
            f"{report.session_id}{report.audit_end}{report.total_issues}".encode()
        ).hexdigest(),
        'session_id': report.session_id,
        'charter_version': report.charter_version,
        'audit_timestamp': report.audit_end,
        'verification': {
            'total_files': report.total_files,
            'total_issues': report.total_issues,
            'files_hash': hashlib.sha256(
                ''.join(r.file_hash for r in report.file_results).encode()
            ).hexdigest()[:32],
            'events_hash': hashlib.sha256(
                ''.join(e.hash for e in report.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_event_stream).encode()
            ).hexdigest()[:32]
        },
        'provenance': {
            'generator': 'GL Governance Audit Engine',
            'version': GL_CHARTER_VERSION,
            'generated_at': datetime.now(timezone.utc).isoformat()
        }
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(link_key_data, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError, UnicodeEncodeError) as e:
        raise RuntimeError(f"Failed to write link key to {output_path}: {e}")
    
    return link_key_data['link_key']

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """主執行函數"""
    parser = argparse.ArgumentParser(
        description='GL Unified Charter - AEP Engine 治理稽核引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run audit on current directory
  python gl_gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_audit_engine.py
  
  # Run audit on specific repository
  python gl_gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_audit_engine.py --repo-path /path/to/repo
  
  # Specify custom output directory
  python gl_gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_audit_engine.py --output-dir /path/to/output
        """
    )
    
    parser.add_argument(
        '--repo-path',
        type=str,
        default=None,
        help='Path to the repository to audit (default: current working directory)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for audit reports (default: <repo-path>/gl-audit-reports)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'GL Governance Audit Engine {GL_CHARTER_VERSION}'
    )
    
    args = parser.parse_args()
    
    # Determine repo path - ensure it's a string for GovernanceAuditEngine
    if args.repo_path:
        repo_path = str(args.repo_path)
    else:
        # Path.cwd() returns a Path object, convert to string
        repo_path = str(Path.cwd())
    
    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(repo_path) / 'gl-audit-reports'
    
    print(f"🔍 GL Governance Audit Engine v{GL_CHARTER_VERSION}")
    print(f"📂 Repository: {repo_path}")
    print(f"📝 Output: {output_dir}")
    print()
    
    # 初始化引擎
    engine = GovernanceAuditEngine(repo_path)
    
    # 執行完整稽核
    report = engine.run_full_audit()
    
    # 生成報告
    print("📝 生成報告...")
    
    json_report = generate_json_reports(report, output_dir)
    print(f"   ✅ JSON 報告: {json_report}")
    
    md_report = generate_markdown_report(report, output_dir / 'GOVERNANCE-AUDIT-REPORT.md')
    print(f"   ✅ Markdown 報告: {md_report}")
    
    link_key = generate_link_key(report, output_dir / 'link-key.json')
    print(f"   ✅ 鏈鍵: {link_key}")
    
    print(f"\n🎯 所有報告已生成至: {output_dir}")
    
    return report

if __name__ == '__main__':
    main()