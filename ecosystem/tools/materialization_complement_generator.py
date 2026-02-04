#!/usr/bin/env python3
"""
實體化補件生成器
Materialization Complement Generator

為語義聲明生成具體實現補件，不降階而是提供實體化證據。

核心原則：
1. 不降階：保留所有語義聲明
2. 實體化：為聲明提供可驗證的實體
3. 可追溯：語義 → 實體 → 驗證
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class DeclarationType(Enum):
    """語義聲明類型"""
    ARCHITECTURE = "architecture"  # 架構層級聲明
    PHASE = "phase"  # 階段聲明
    COMPLIANCE = "compliance"  # 合規性聲明
    COMPLETENESS = "completeness"  # 完整性聲明
    ERA_LAYER = "era_layer"  # Era/Layer/Semantic Closure 聲明
    PLATFORM = "platform"  # 平台化聲明
    SEALING = "sealing"  # 封存相關聲明


class EntityType(Enum):
    """實體類型"""
    DOCUMENT = "document"  # 文檔
    CODE = "code"  # 代碼
    DATA = "data"  # 數據
    EVIDENCE = "evidence"  # 證據
    CONFIG = "config"  # 配置


class Priority(Enum):
    """優先級"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ComplementStatus(Enum):
    """補件狀態"""
    MISSING = "MISSING"  # 缺失
    EXISTS = "EXISTS"  # 存在
    INCOMPLETE = "INCOMPLETE"  # 不完整
    GENERATED = "GENERATED"  # 已生成模板


@dataclass
class SemanticDeclaration:
    """語義聲明"""
    declaration_type: DeclarationType
    declaration_text: str
    source_file: str
    line_number: int
    context: str = ""


@dataclass
class ComplementEntity:
    """補件實體"""
    entity_type: EntityType
    name: str
    location: str
    template: Optional[str] = None
    status: ComplementStatus = ComplementStatus.MISSING
    priority: Priority = Priority.MEDIUM
    verification_methods: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class ComplementItem:
    """補件項目"""
    declaration: SemanticDeclaration
    entities: List[ComplementEntity] = field(default_factory=list)
    completion_rate: float = 0.0


@dataclass
class ComplementReport:
    """補件報告"""
    scan_time: str
    total_declarations: int
    total_entities: int
    missing_entities: int
    exists_entities: int
    generated_entities: int
    incomplete_entities: int
    completion_rate: float
    compliance_score: float
    items: List[ComplementItem] = field(default_factory=list)


class MaterializationComplementGenerator:
    """實體化補件生成器"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.reports_dir = self.workspace_root / "reports"
        self.complements_dir = self.workspace_root / "complements"
        self.templates_dir = self.complements_dir / "templates"
        
        # 確保目錄存在
        self.complements_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # 聲明檢測模式
        self.declaration_patterns = {
            DeclarationType.ARCHITECTURE: [
                r'治理平台|統一治理|完整閉環|完整架構|完全一致',
            ],
            DeclarationType.PHASE: [
                r'Phase\s+\d+[：:]\s*\w+|第\s*\d+\s*階段',
            ],
            DeclarationType.COMPLIANCE: [
                r'100%\s*合規|完全符合規範|所有檢查通過|合規性\s*:\s*\d+/\d+',
            ],
            DeclarationType.COMPLETENESS: [
                r'完整性保證|無缺點|完整覆蓋|完整性\s*:\s*\d+%',
            ],
            DeclarationType.ERA_LAYER: [
                r'Era\s*:\s*\d+|Layer\s*:\s*\w+|Semantic Closure\s*:\s*\w+',
            ],
            DeclarationType.PLATFORM: [
                r'平台|Platform|組件化|模塊化',
            ],
            DeclarationType.SEALING: [
                r'封存|密封|鎖定|Sealed|LOCKED',
            ],
        }
        
        # 補件模板映射
        self.entity_templates = {
            DeclarationType.ARCHITECTURE: [
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="平台架構圖",
                    location="docs/architecture/platform-architecture.md",
                    template="architecture-diagram-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["檢查文件是否存在", "驗證架構圖一致性"],
                    description="展示整體平台架構和組件關係"
                ),
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="API 文檔",
                    location="docs/api/platform-api.md",
                    template="api-doc-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["檢查接口定義完整性", "驗證 API 文檔格式"],
                    description="所有公開接口的詳細定義"
                ),
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="組件清單",
                    location="docs/architecture/component-list.md",
                    template="component-list-template.md",
                    priority=Priority.MEDIUM,
                    verification_methods=["驗證組件列表完整性", "檢查依賴關係"],
                    description="所有組件的名稱、職責、依賴"
                ),
            ],
            DeclarationType.PHASE: [
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="階段定義",
                    location="phases/{phase}/definition.md",
                    template="phase-definition-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["檢查定義完整性", "驗證範圍和目標"],
                    description="階段的目標、範圍、交付物"
                ),
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="階段檢查清單",
                    location="phases/{phase}/checklist.md",
                    template="phase-checklist-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["驗證檢查項覆蓋", "檢查完成標準"],
                    description="完成標準、驗收條件"
                ),
                ComplementEntity(
                    entity_type=EntityType.DATA,
                    name="階段狀態",
                    location="phases/{phase}/status.json",
                    template="phase-status-template.json",
                    priority=Priority.MEDIUM,
                    verification_methods=["驗證狀態文件格式", "檢查數據完整性"],
                    description="當前進度、完成度"
                ),
            ],
            DeclarationType.COMPLIANCE: [
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="合規性報告",
                    location="reports/compliance-report.md",
                    template="compliance-report-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["檢查報告完整性", "驗證得分計算"],
                    description="詳細檢查結果、得分、違規項"
                ),
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="證據清單",
                    location="reports/evidence-list.md",
                    template="evidence-list-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["驗證證據清單完整性", "檢查證據鏈"],
                    description="所有支持合規聲明的證據"
                ),
                ComplementEntity(
                    entity_type=EntityType.CODE,
                    name="驗證腳本",
                    location="tools/verify_compliance.py",
                    template="verify_compliance_template.py",
                    priority=Priority.HIGH,
                    verification_methods=["執行驗證腳本", "檢查測試覆蓋"],
                    description="可重複執行的驗證腳本"
                ),
            ],
            DeclarationType.COMPLETENESS: [
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="覆蓋率報告",
                    location="reports/coverage-report.md",
                    template="coverage-report-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["驗證覆蓋率數據", "檢查趨勢一致性"],
                    description="代碼覆蓋、測試覆蓋、需求覆蓋"
                ),
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="完整性檢查清單",
                    location="reports/completeness-checklist.md",
                    template="completeness-checklist-template.md",
                    priority=Priority.MEDIUM,
                    verification_methods=["驗證檢查項完整性", "檢查標準定義"],
                    description="所有完整性指標"
                ),
            ],
            DeclarationType.ERA_LAYER: [
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="Era 定義文檔",
                    location="docs/governance/era-definition.md",
                    template="era-definition-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["檢查 Era 定義完整性", "驗證限制條件"],
                    description="當前 Era 的定義、目標、限制"
                ),
                ComplementEntity(
                    entity_type=EntityType.DOCUMENT,
                    name="Layer 定義文檔",
                    location="docs/governance/layer-definition.md",
                    template="layer-definition-template.md",
                    priority=Priority.HIGH,
                    verification_methods=["檢查 Layer 定義完整性", "驗證職責範圍"],
                    description="當前 Layer 的職責、範圍"
                ),
            ],
        }
    
    def scan_reports(self) -> List[SemanticDeclaration]:
        """掃描報告文件，提取語義聲明"""
        declarations = []
        
        if not self.reports_dir.exists():
            print(f"⚠️  報告目錄不存在: {self.reports_dir}")
            return declarations
        
        # 掃描所有 markdown 報告
        for report_file in self.reports_dir.glob("*.md"):
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # 檢測每種類型的聲明
                for decl_type, patterns in self.declaration_patterns.items():
                    for pattern in patterns:
                        for line_num, line in enumerate(lines, 1):
                            if re.search(pattern, line, re.IGNORECASE):
                                declaration = SemanticDeclaration(
                                    declaration_type=decl_type,
                                    declaration_text=line.strip(),
                                    source_file=str(report_file.relative_to(self.workspace_root)),
                                    line_number=line_num,
                                    context=self._get_context(lines, line_num, 2)
                                )
                                declarations.append(declaration)
            
            except Exception as e:
                print(f"⚠️  讀取報告失敗 {report_file}: {e}")
        
        return declarations
    
    def _get_context(self, lines: List[str], line_num: int, context_lines: int) -> str:
        """獲取上下文"""
        start = max(0, line_num - context_lines - 1)
        end = min(len(lines), line_num + context_lines)
        return '\n'.join(lines[start:end])
    
    def detect_missing_entities(self, declaration: SemanticDeclaration) -> List[ComplementEntity]:
        """檢測缺失的實體"""
        entities = []
        
        # 獲取該類型的模板實體
        template_entities = self.entity_templates.get(declaration.declaration_type, [])
        
        for template_entity in template_entities:
            # 處理路徑中的變量（如 {phase}）
            location = self._resolve_location(template_entity.location, declaration)
            
            # 檢查實體是否存在
            entity_path = self.workspace_root / location
            status = self._check_entity_status(entity_path, template_entity.entity_type)
            
            entity = ComplementEntity(
                entity_type=template_entity.entity_type,
                name=template_entity.name,
                location=location,
                template=template_entity.template,
                status=status,
                priority=template_entity.priority,
                verification_methods=template_entity.verification_methods,
                description=template_entity.description
            )
            
            entities.append(entity)
        
        return entities
    
    def _resolve_location(self, location: str, declaration: SemanticDeclaration) -> str:
        """解析路徑中的變量"""
        # 提取 phase 號
        phase_match = re.search(r'Phase\s+(\d+)', declaration.declaration_text, re.IGNORECASE)
        if phase_match:
            phase_num = phase_match.group(1)
            location = location.replace("{phase}", f"phase-{phase_num}")
        
        return location
    
    def _check_entity_status(self, entity_path: Path, entity_type: EntityType) -> ComplementStatus:
        """檢查實體狀態"""
        if not entity_path.exists():
            return ComplementStatus.MISSING
        
        # 檢查實體是否完整
        if entity_type == EntityType.DOCUMENT:
            try:
                content = entity_path.read_text(encoding='utf-8')
                if len(content.strip()) < 50:  # 太短，視為不完整
                    return ComplementStatus.INCOMPLETE
                return ComplementStatus.EXISTS
            except Exception:
                return ComplementStatus.INCOMPLETE
        
        elif entity_type == EntityType.CODE:
            try:
                content = entity_path.read_text(encoding='utf-8')
                if len(content.strip()) < 20:
                    return ComplementStatus.INCOMPLETE
                return ComplementStatus.EXISTS
            except Exception:
                return ComplementStatus.INCOMPLETE
        
        elif entity_type == EntityType.DATA:
            try:
                with open(entity_path, 'r', encoding='utf-8') as f:
                    data = json.load(f) if entity_path.suffix == '.json' else f.read()
                return ComplementStatus.EXISTS
            except Exception:
                return ComplementStatus.INCOMPLETE
        
        return ComplementStatus.EXISTS
    
    def generate_complements(self, declarations: List[SemanticDeclaration]) -> ComplementReport:
        """生成補件報告"""
        items = []
        
        # 去重：相同類型和文本的聲明只處理一次
        unique_declarations = {}
        for decl in declarations:
            key = (decl.declaration_type, decl.declaration_text)
            if key not in unique_declarations:
                unique_declarations[key] = decl
        
        for declaration in unique_declarations.values():
            entities = self.detect_missing_entities(declaration)
            
            # 計算完成率
            completed = sum(1 for e in entities if e.status == ComplementStatus.EXISTS)
            completion_rate = (completed / len(entities)) * 100 if entities else 100.0
            
            item = ComplementItem(
                declaration=declaration,
                entities=entities,
                completion_rate=completion_rate
            )
            items.append(item)
        
        # 統計
        all_entities = [e for item in items for e in item.entities]
        total_entities = len(all_entities)
        missing_entities = sum(1 for e in all_entities if e.status == ComplementStatus.MISSING)
        exists_entities = sum(1 for e in all_entities if e.status == ComplementStatus.EXISTS)
        incomplete_entities = sum(1 for e in all_entities if e.status == ComplementStatus.INCOMPLETE)
        generated_entities = sum(1 for e in all_entities if e.status == ComplementStatus.GENERATED)
        
        # 計算完成率
        completion_rate = (exists_entities / total_entities) * 100 if total_entities > 0 else 100.0
        
        # 計算合規性評分（存在實體得分更高）
        compliance_score = completion_rate  # 簡化計算，可以根據優先級加權
        
        report = ComplementReport(
            scan_time=datetime.now().isoformat(),
            total_declarations=len(unique_declarations),
            total_entities=total_entities,
            missing_entities=missing_entities,
            exists_entities=exists_entities,
            generated_entities=generated_entities,
            incomplete_entities=incomplete_entities,
            completion_rate=completion_rate,
            compliance_score=compliance_score,
            items=items
        )
        
        return report
    
    def generate_complement_templates(self, report: ComplementReport) -> None:
        """生成補件模板"""
        for item in report.items:
            for entity in item.entities:
                if entity.status == ComplementStatus.MISSING and entity.template:
                    self._generate_template(entity)
    
    def _generate_template(self, entity: ComplementEntity) -> None:
        """生成單個實體模板"""
        template_path = self.templates_dir / entity.template
        
        # 檢查模板是否已存在
        if template_path.exists():
            return
        
        # 生成模板內容
        content = self._get_template_content(entity)
        
        # 創建模板目錄
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 寫入模板
        template_path.write_text(content, encoding='utf-8')
        
        # 更新實體狀態
        entity.status = ComplementStatus.GENERATED
        
        print(f"✅ 生成模板: {template_path}")
    
    def _get_template_content(self, entity: ComplementEntity) -> str:
        """獲取模板內容"""
        if entity.entity_type == EntityType.DOCUMENT:
            return f"""# {entity.name}

> **生成時間**: {datetime.now().isoformat()}
> **目的**: {entity.description}
> **位置**: {entity.location}

## 概述

[在此處描述 {entity.name} 的概述]

## 內容

[在此處填充 {entity.name} 的具體內容]

## 驗證方法

{chr(10).join(f"- {method}" for method in entity.verification_methods)}

---
**狀態**: ⏸️ 待填充  
**優先級**: {entity.priority.value}
"""
        elif entity.entity_type == EntityType.CODE:
            return f"""#!/usr/bin/env python3
&quot;&quot;&quot;
{entity.name}

{entity.description}

生成時間: {datetime.now().isoformat()}
位置: {entity.location}
&quot;&quot;&quot;

import os
import sys
from pathlib import Path

# TODO: 實現 {entity.name} 的功能

def main():
    &quot;&quot;&quot;主函數&quot;&quot;&quot;
    print(f&quot;{entity.name}&quot;)
    # TODO: 添加實現

if __name__ == &quot;__main__&quot;:
    main()

---
**狀態**: ⏸️ 待實現  
**優先級**: {entity.priority.value}
"""
        elif entity.entity_type == EntityType.DATA:
            return """{{
  &quot;name&quot;: &quot;{entity.name}&quot;,
  &quot;description&quot;: &quot;{entity.description}&quot;,
  &quot;created_at&quot;: &quot;{datetime.now().isoformat()}&quot;,
  &quot;location&quot;: &quot;{entity.location}&quot;,
  &quot;status&quot;: &quot;pending&quot;,
  &quot;data&quot;: {{
    &quot;TODO&quot;: &quot;填充實際數據&quot;
  }}
}}
""".replace('{entity.name}', entity.name).replace('{entity.description}', entity.description)
        
        return f"# {entity.name}\n\nTODO: 生成模板內容\n"
    
    def generate_markdown_report(self, report: ComplementReport, output_file: str) -> None:
        """生成 Markdown 補件報告"""
        content = f"""# 實體化補件報告

> **掃描時間**: {report.scan_time}
> **Era**: 1 (Evidence-Native Bootstrap)
> **不降階原則**: ✅ 保留所有語義聲明，提供實體化補件

---

## 執行摘要

| 指標 | 數值 |
|------|------|
| 總語義聲明數 | {report.total_declarations} |
| 總實體數 | {report.total_entities} |
| 缺失實體 | 🔴 {report.missing_entities} |
| 已存在實體 | ✅ {report.exists_entities} |
| 不完整實體 | 🟡 {report.incomplete_entities} |
| 已生成模板 | 📝 {report.generated_entities} |
| 補件完成率 | {report.completion_rate:.1f}% |
| 合規性評分 | {report.compliance_score:.1f}/100 |

---

## 語義聲明分析
"""
        
        # 按類型統計
        type_stats = {}
        for item in report.items:
            decl_type = item.declaration.declaration_type.value
            if decl_type not in type_stats:
                type_stats[decl_type] = {'total': 0, 'entities': 0, 'exists': 0}
            type_stats[decl_type]['total'] += 1
            type_stats[decl_type]['entities'] += len(item.entities)
            type_stats[decl_type]['exists'] += sum(1 for e in item.entities if e.status == ComplementStatus.EXISTS)
        
        for decl_type, stats in type_stats.items():
            completion = (stats['exists'] / stats['entities'] * 100) if stats['entities'] > 0 else 0
            content += f"""
### {decl_type.replace('_', ' ').title()}

| 指標 | 數值 |
|------|------|
| 聲明數 | {stats['total']} |
| 實體數 | {stats['entities']} |
| 已存在 | ✅ {stats['exists']} |
| 缺失 | 🔴 {stats['entities'] - stats['exists']} |
| 完成率 | {completion:.1f}% |

"""
        
        # 補件清單
        content += "---\n\n## 補件清單\n\n"
        for idx, item in enumerate(report.items, 1):
            content += f"""
### 補件 #{idx}: {item.declaration.declaration_text[:50]}...

> **類型**: {item.declaration.declaration_type.value}
> **來源**: {item.declaration.source_file}:{item.declaration.line_number}
> **完成率**: {item.completion_rate:.1f}%

"""
            for entity in item.entities:
                status_emoji = {
                    ComplementStatus.MISSING: "🔴 缺失",
                    ComplementStatus.EXISTS: "✅ 已存在",
                    ComplementStatus.INCOMPLETE: "🟡 不完整",
                    ComplementStatus.GENERATED: "📝 已生成模板",
                }
                
                content += f"""
#### {entity.name}

| 屬性 | 值 |
|------|-----|
| 類型 | {entity.entity_type.value} |
| 位置 | `{entity.location}` |
| 狀態 | {status_emoji.get(entity.status, entity.status.value)} |
| 優先級 | {entity.priority.value} |
| 描述 | {entity.description} |

**驗證方法**:
{chr(10).join(f"- {method}" for method in entity.verification_methods)}

**上下文**:
```markdown
{item.declaration.context}
```

"""
        
        # 驗證結果
        content += "---\n\n## 驗證結果\n\n"
        content += f"""
| 類別 | 數量 |
|------|------|
| ✅ 驗證通過的實體 | {report.exists_entities} |
| 🔴 缺失實體 | {report.missing_entities} |
| 🟡 不完整實體 | {report.incomplete_entities} |
| 📝 已生成模板 | {report.generated_entities} |

"""
        
        # 下一步行動
        content += "---\n\n## 下一步行動\n\n"
        content += """
### 立即行動（高優先級）
- [ ] 生成缺失實體的模板（已自動生成）
- [ ] 填充高優先級實體內容
- [ ] 執行驗證腳本

### 短期行動（1-2 週）
- [ ] 完成所有缺失實體的填充
- [ ] 修復不完整實體
- [ ] 執行完整驗證

### 中期行動（1-2 個月）
- [ ] 自動化補件生成
- [ ] 持續監控補件狀態
- [ ] 優化模板和驗證方法

---

## 附錄

### 補件原則

1. **不降階原則**: 保留所有語義聲明，不移除或降級
2. **實體化原則**: 為聲明提供可驗證的具體實體
3. **可追溯原則**: 語義 → 實體 → 驗證，形成完整鏈條

### Era-1 合規標準

- 語義聲明必須有意義（不虛構）
- 存在的實體必須可驗證
- 缺失的實體必須有計劃
- 補件進度必須可追蹤

---

**報告生成時間**: {datetime.now().isoformat()}  
**工具版本**: v1.0.0  
**Era**: 1 (Evidence-Native Bootstrap)
"""
        
        # 寫入文件
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        
        print(f"✅ 報告已生成: {output_path}")
    
    def generate_json_report(self, report: ComplementReport, output_file: str) -> None:
        """生成 JSON 格式報告"""
        data = {
            "scan_time": report.scan_time,
            "era": "1",
            "summary": {
                "total_declarations": report.total_declarations,
                "total_entities": report.total_entities,
                "missing_entities": report.missing_entities,
                "exists_entities": report.exists_entities,
                "incomplete_entities": report.incomplete_entities,
                "generated_entities": report.generated_entities,
                "completion_rate": report.completion_rate,
                "compliance_score": report.compliance_score,
            },
            "items": []
        }
        
        for item in report.items:
            item_data = {
                "declaration": {
                    "type": item.declaration.declaration_type.value,
                    "text": item.declaration.declaration_text,
                    "source": item.declaration.source_file,
                    "line": item.declaration.line_number,
                    "context": item.declaration.context,
                },
                "completion_rate": item.completion_rate,
                "entities": []
            }
            
            for entity in item.entities:
                entity_data = {
                    "type": entity.entity_type.value,
                    "name": entity.name,
                    "location": entity.location,
                    "template": entity.template,
                    "status": entity.status.value,
                    "priority": entity.priority.value,
                    "verification_methods": entity.verification_methods,
                    "description": entity.description,
                }
                item_data["entities"].append(entity_data)
            
            data["items"].append(item_data)
        
        # 寫入文件
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON 報告已生成: {output_path}")


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="實體化補件生成器 - 為語義聲明生成具體實現補件"
    )
    parser.add_argument(
        "--workspace",
        default="/workspace",
        help="工作區根目錄"
    )
    parser.add_argument(
        "--scan-reports",
        action="store_true",
        help="掃描報告並生成補件清單"
    )
    parser.add_argument(
        "--generate-templates",
        action="store_true",
        help="生成補件模板"
    )
    parser.add_argument(
        "--output-dir",
        default="/workspace/reports",
        help="輸出目錄"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="詳細輸出"
    )
    
    args = parser.parse_args()
    
    # 創建生成器
    generator = MaterializationComplementGenerator(args.workspace)
    
    # 掃描報告
    print("🔍 掃描報告文件...")
    declarations = generator.scan_reports()
    print(f"✅ 發現 {len(declarations)} 個語義聲明")
    
    if args.verbose:
        for decl in declarations:
            print(f"  - [{decl.declaration_type.value}] {decl.declaration_text}")
    
    # 生成補件
    print("\n📊 生成補件報告...")
    report = generator.generate_complements(declarations)
    
    # 生成模板
    if args.generate_templates:
        print("\n📝 生成補件模板...")
        generator.generate_complement_templates(report)
    
    # 生成報告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    markdown_report = f"{args.output_dir}/materialization-complement-report-{timestamp}.md"
    json_report = f"{args.output_dir}/materialization-complement-report-{timestamp}.json"
    
    generator.generate_markdown_report(report, markdown_report)
    generator.generate_json_report(report, json_report)
    
    # 打印摘要
    print("\n" + "=" * 80)
    print("📊 實體化補件摘要")
    print("=" * 80)
    print(f"總語義聲明數: {report.total_declarations}")
    print(f"總實體數: {report.total_entities}")
    print(f"缺失實體: 🔴 {report.missing_entities}")
    print(f"已存在實體: ✅ {report.exists_entities}")
    print(f"不完整實體: 🟡 {report.incomplete_entities}")
    print(f"已生成模板: 📝 {report.generated_entities}")
    print(f"補件完成率: {report.completion_rate:.1f}%")
    print(f"合規性評分: {report.compliance_score:.1f}/100")
    print("\n✅ 不降階原則：保留所有語義聲明，提供實體化補件")
    print("=" * 80)


if __name__ == "__main__":
    main()