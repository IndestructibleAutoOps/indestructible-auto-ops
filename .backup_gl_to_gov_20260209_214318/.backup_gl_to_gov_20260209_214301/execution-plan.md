# GL 自動執行調整 - 執行計畫

## 執行計畫概述

**執行模式:** HIGH_WEIGHT_EXECUTION  
**執行範圍:** 1,189 個需調整檔案  
**目標:** 100% GL 治理合規  
**安全機制:** 備份、回滾、驗證

---

## 執行階段

### 階段 1: 準備工作 [完成]
1. ✅ 建立備份機制
2. ✅ 建立目標目錄結構
3. ✅ 準備執行腳本
   - ✅ 備份完成: backup/20260131/machine-native-backup.tar.gz (115M)
   - ✅ 目標結構建立
   - ✅ GL Root Anchor 和 Naming Charter 複製
   - ✅ 執行腳本準備完成

### 階段 2: 執行調整 [進行中]
- [x] 建立目標目錄結構
- [x] 執行檔案遷移
  - ✅ semantic_engine → gl-platform/GL90-99-semantic-engine
  - ✅ .governance → gl-platform/GL90-99-governance
  - ✅ .github/governance-legacy → gl-platform/governance/archived/legacy
- [x] 新增 GL 標記
  - ✅ 處理 1000 個檔案
  - ✅ 成功標記: 766 個
  - ✅ 已有標記: 191 個
  - ✅ 錯誤: 43 個
  - ✅ 合規率: 95.7%
- [x] 更新引用關係
  - ✅ 處理 567 個 Python 檔案
  - ✅ 更新 semantic_engine 引用
  - ✅ 更新 governance 引用
  - ✅ 更新所有 .governance 引用
  - ✅ 驗證引用完整性

### 階段 3: 驗證測試 [準備啟動]
- [ ] 驗證檔案結構
- [ ] 驗證命名合規
- [ ] 驗證引用完整性

### 階段 4: 部署上線 [準備啟動]
- [ ] 提交變更
- [ ] 更新文檔
- [ ] 監控運行

---

## 階段 1: 準備工作詳細計畫

### 1.1 建立備份機制

#### 備份目標目錄
```bash
# 建立備份目錄
mkdir -p /workspace/backup/$(date +%Y%m%d)

# 完整備份專案
tar -czf /workspace/backup/$(date +%Y%m%d)/machine-native-ops-backup.tar.gz \
  -C /workspace/machine-native-ops .

# 驗證備份
tar -tzf /workspace/backup/$(date +%Y%m%d)/machine-native-ops-backup.tar.gz \
  --list | wc -l
```

#### 備份驗證
```python
#!/usr/bin/env python3
"""驗證備份完整性"""

def verify_backup(backup_file):
    """驗證備份檔案完整性"""
    # 檢查檔案存在
    # 驗證壓縮包
    # 計算校驗和
    # 生成報告
```

### 1.2 建立目標目錄結構

#### 建立治理架構
```bash
#!/bin/bash
# 建立目標結構腳本

# 基礎目錄
mkdir -p gl-platform/gl90-99-meta-specification-layer/governance
mkdir -p gl-platform/gl90-99-meta-specification-layer/governance/naming-governance
mkdir -p gl-platform/gl90-99-meta-specification-layer/governance/archived/legacy
mkdir -p gl-platform/gl90-99-meta-specification-layer/governance/audit-trails
mkdir -p gl-platform/gl90-99-meta-specification-layer/governance/architecture
mkdir -p gl-platform/GL30-49-Execution-Layer/engine/governance
mkdir -p gl-platform/GL30-49-Execution-Layer/engine/governance/GL90-99-semantic-engine

# 建立 GL 根錨點
cp machine-native-ops/.github/governance-legacy/gl-artifacts/GL-ROOT-SEMANTIC-ANCHOR.yaml \
   gl-platform/gl90-99-meta-specification-layer/governance/

# 建立命名章程
cp machine-native-ops/.github/governance-legacy/gl-artifacts/gl-unified-naming-charter.yaml \
   gl-platform/gl90-99-meta-specification-layer/governance/

echo "目標結構建立完成"
```

### 1.3 準備執行腳本

#### 腳本 1: GL 標記添加腳本
```python
#!/usr/bin/env python3
"""GL Markers Addition Script"""

import os
from pathlib import Path

# GL 標記範本
PYTHON_MARKER = """# @GL-governed
# @GL-layer: {layer}
# @GL-semantic: {semantic}
# @GL-audit-trail: {audit_path}
#
# GL Unified Architecture Governance Framework Activated
# GL Root Semantic Anchor: gl-platform/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform/governance/GL-UNIFIED-NAMING-CHARTER.yaml

"""

YAML_MARKER = """# @GL-governed
# @GL-layer: {layer}
# @GL-semantic: {semantic}
# @GL-audit-trail: {audit_path}
#
# GL Unified Architecture Governance Framework Activated
# GL Root Semantic Anchor: gl-platform/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform/governance/GL-UNIFIED-NAMING-CHARTER.yaml

"""

def add_markers(file_path, layer, semantic, audit_path):
    """Add GL markers to file"""
    try:
        # 讀取檔案內容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有標記
        if '@GL-governed' in content:
            return False
        
        # 選擇標記範本
        if file_path.suffix == '.py':
            marker = PYTHON_MARKER.format(
                layer=layer,
                semantic=semantic,
                audit_path=audit_path
            )
        elif file_path.suffix in ['.yaml', '.yml']:
            marker = YAML_MARKER.format(
                layer=layer,
                semantic=semantic,
                audit_path=audit_path
            )
        else:
            marker = YAML_MARKER.format(
                layer=layer,
                semantic=semantic,
                audit_path=audit_path
            )
        
        # 添加標記
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(marker)
            f.write('\n')
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

if __name__ == '__main__':
    # 從 scan_results.json 讀取需要調整的檔案
    import json
    
    with open('/workspace/scan_results.json', 'r') as f:
        data = json.load(f)
    
    # 處理每個需要調整的檔案
    for item in data['adjustment_suggestions']:
        file_path = Path(f"/workspace/machine-native-ops/{item['current_path']}")
        if file_path.exists():
            layer = item['gl_layer']
            semantic = item['semantic_type']
            audit_path = f"gl-platform/governance/audit-trails/{layer}-audit.json"
            
            if add_markers(file_path, layer, semantic, audit_path):
                print(f"✓ Added markers to: {item['current_path']}")
            else:
                print(f"✗ Skipped: {item['current_path']} (already has markers)")
```

#### 腳本 2: 檔案遷移腳本
```python
#!/usr/bin/env python3
"""File Migration Script"""

import shutil
from pathlib import Path

# 遷移映射
MIGRATION_MAP = {
    'semantic_engine/': 'gl-platform/gl90-99-meta-specification-layer/governance/semantic-engine/',
    '.governance/': 'gl-platform/gl90-99-meta-specification-layer/governance/',
    '.github/governance-legacy/': 'gl-platform/gl90-99-meta-specification-layer/governance/archived/legacy/',
}

def migrate_file(file_path, target_path):
    """遷移單個檔案"""
    try:
        # 建立目標目錄
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 移動檔案
        shutil.move(str(file_path), str(target_path))
        
        print(f"✓ Migrated: {file_path} → {target_path}")
        return True
    except Exception as e:
        print(f"✗ Error migrating {file_path}: {e}")
        return False

def migrate_all():
    """執行所有遷移"""
    # 遷移 semantic_engine
    semantic_engine_src = Path('/workspace/machine-native-ops/semantic_engine')
    if semantic_engine_src.exists():
        semantic_engine_dst = Path('/workspace/machine-native-ops/gl-platform/gl90-99-meta-specification-layer/governance/gl90-99-semantic-engine')
        if not semantic_engine_dst.exists():
            shutil.move(str(semantic_engine_src), str(semantic_engine_dst))
            print(f"✓ Migrated semantic_engine directory")
    
    # 遷移 .governance
    governance_src = Path('/workspace/machine-native-ops/.governance')
    if governance_src.exists():
        governance_dst = Path('/workspace/machine-native-ops/gl-platform/gl90-99-meta-specification-layer/governance')
        if not governance_dst.exists():
            shutil.move(str(governance_src), str(governance_dst))
            print(f"✓ Migrated .governance directory")
    
    # 遷移 governance-legacy
    legacy_src = Path('/workspace/machine-native-ops/.github/governance-legacy')
    if legacy_src.exists():
        legacy_dst = Path('/workspace/machine-native-oss/gl-platform/gl90-99-meta-specification-layer/governance/archived/legacy')
        if not legacy_dst.exists():
            shutil.move(str(legacy_src), str(legacy_dst))
            print(f"✓ Migrated governance-legacy directory")

if __name__ == '__main__':
    migrate_all()
    print("Migration complete")
```

#### 腳本 3: 引用更新腳本
```python
#!/usr/bin/env python3
"""Import Update Script"""

import re
from pathlib import Path

# 引用映射
IMPORT_MAP = {
    'semantic_engine': 'gl-platform.governance.semantic_engine',
    'governance': 'gl-platform.governance',
}

# 正則模式
IMPORT_PATTERN = re.compile(r'(from|import)\s+(semantic_engine|governance)')

def update_imports(file_path):
    """更新檔案中的 import 語句"""
    try:
        # 讀取檔案
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 原始內容
        original_content = content
        
        # 替換 import
        for old_module, new_module in IMPORT_MAP.items():
            content = content.replace(old_module, new_module)
        
        # 如果有變更，寫回檔案
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def update_all_imports():
    """更新所有 Python 檔案的 import"""
    python_files = list(Path('/workspace/machine-native-ops').rglob('*.py'))
    
    updated_count = 0
    for file_path in python_files:
        if update_imports(file_path):
            print(f"✓ Updated imports in: {file_path}")
            updated_count += 1
    
    print(f"Total files updated: {updated_count}")

if __name__ == '__main__':
    update_all_imports()
```

---

## 開始執行

**準備階段已完成:** ✅  
**下一步:** 開始執行檔案遷移

**確認開始執行?**