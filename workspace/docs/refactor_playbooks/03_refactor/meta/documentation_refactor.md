# Documentation Layer 重構劇本（Refactor Playbook）

> **GL Layer**: GL90-99 Meta-Specification Layer  
> **Phase**: 03_refactor (重構階段)  
> **Target**: Root documentation files (README.md, README-MACHINE.md, PROJECT_STATUS.md, QUICKSTART.md)  
> **Dependencies**: [documentation_integration.md](../../02_integration/documentation_integration.md)  
> **Last Updated**: 2026-01-19

---

## 執行摘要（Executive Summary）

本重構劇本基於 [Phase 2 Integration Playbook](../../02_integration/documentation_integration.md) 的設計，提供可執行的 P0/P1/P2 行動計劃，用於優化 Root Layer Documentation 的結構、一致性和可維護性。

**當前狀態**:
- ✅ README.md 結構良好，內容豐富（400 行）
- ✅ GL Layer 註釋已存在
- ✅ 快速導航鏈接已建立
- ⚠️ 缺乏自動化更新機制
- ⚠️ 交叉引用未完全驗證
- ⚠️ 文檔邊界不夠明確

**目標**:
- 🎯 建立清晰的文檔邊界（Root vs Workspace）
- 🎯 實現 70% 自動化更新覆蓋率
- 🎯 確保 100% 交叉引用有效性
- 🎯 建立長期維護標準

---

## P0: 關鍵優先（Critical Priority）

**執行時限**: 即刻 - 1 週內完成  
**失敗影響**: 阻塞項目理解，影響新用戶入職

### P0.1 ✅ 創建集成劇本（Integration Playbook Creation）

**狀態**: ✅ COMPLETED (2026-01-19)

```yaml
task: "創建 Phase 2 集成劇本"
deliverable: "workspace/docs/refactor_playbooks/02_integration/documentation_integration.md"
outcome: "文檔邊界、介面規格、依賴策略已明確定義"
verification: "集成劇本文件存在且完整"
```

**結果**:
- ✅ 集成劇本已創建（documentation_integration.md）
- ✅ 邊界定義清晰（Root vs Workspace vs Controlplane）
- ✅ 更新協議已建立
- ✅ 遷移策略已規劃

---

### P0.2 🔄 驗證交叉引用完整性（Cross-Reference Validation）

**狀態**: ⏳ IN PROGRESS

**目標**: 確保所有內部鏈接有效，無死鏈接

```yaml
action_items:
  - id: "P0.2.1"
    task: "掃描所有 root docs 的內部鏈接"
    tool: "markdown-link-check"
    expected_output: "鏈接清單 + 驗證狀態"
    
  - id: "P0.2.2"
    task: "修復所有死鏈接"
    priority: "HIGH"
    auto_fix: false  # 需要人工判斷正確目標
    
  - id: "P0.2.3"
    task: "建立 CI 鏈接驗證"
    deliverable: ".github/workflows/validate-docs-links.yml"
    automation: true
```

**執行計劃**:

```bash
# Step 1: 安裝工具
npm install -g markdown-link-check

# Step 2: 掃描 root docs
for file in README.md README-MACHINE.md PROJECT_STATUS.md QUICKSTART.md SECURITY.md todo.md; do
  echo "Checking $file..."
  markdown-link-check "$file"
done > /tmp/link-check-report.txt

# Step 3: 分析報告並修復
cat /tmp/link-check-report.txt | grep "✖" | while read line; do
  echo "BROKEN: $line"
done

# Step 4: 創建 CI workflow
cat > .github/workflows/validate-docs-links.yml << 'EOF'
name: Validate Documentation Links

on:
  push:
    paths:
      - '*.md'
      - 'workspace/docs/**/*.md'
  pull_request:
    paths:
      - '*.md'
      - 'workspace/docs/**/*.md'

jobs:
  validate-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install markdown-link-check
        run: npm install -g markdown-link-check
        
      - name: Check root documentation links
        run: |
          for file in README.md README-MACHINE.md PROJECT_STATUS.md QUICKSTART.md; do
            markdown-link-check "$file" --config .markdown-link-check.json
          done
EOF
```

**驗收條件**:
- [ ] 所有 root docs 無死鏈接（100% pass）
- [ ] CI workflow 已設置並通過
- [ ] `.markdown-link-check.json` 配置文件已創建

---

### P0.3 📋 審計 README.md 內容深度（Content Depth Audit）

**狀態**: 📋 TODO

**目標**: 識別超過 2 層深度的內容，準備移動到 workspace/docs/

```yaml
audit_criteria:
  max_depth: 2  # README.md 最多 2 層導航深度
  max_lines: 400  # 當前已達上限
  detail_threshold: "超過 50 行的單一主題區塊應移到 workspace/docs/"
```

**執行步驟**:

1. **手動審計當前內容**:
   ```bash
   # 分析 README.md 各章節行數
   awk '/^## / {if (section) print section, lines; section=$0; lines=0; next} {lines++} END {print section, lines}' README.md
   ```

2. **識別候選移動內容**:
   - 🔍 "量子增強驗證系統" 區塊（約 30 行）→ 檢查是否過於詳細
   - 🔍 "CI/CD System" 區塊（約 15 行）→ 檢查是否可精簡
   - 🔍 "目錄說明" 區塊（約 50 行）→ 考慮移到 ARCHITECTURE.md

3. **創建遷移清單**:
   ```yaml
   # /tmp/content-migration-list.yaml
   migrations:
     - source: "README.md ## 量子增強驗證系統"
       target: "workspace/docs/quantum/QUANTUM_VALIDATION_GUIDE.md"
       reason: "詳細技術內容，超過 README 深度"
       priority: "P1"
       
     - source: "README.md ## 目錄說明"
       target: "workspace/docs/ARCHITECTURE.md"
       reason: "架構細節應集中到架構文檔"
       priority: "P1"
   ```

**驗收條件**:
- [ ] 內容深度審計報告已生成
- [ ] 遷移清單已創建（content-migration-list.yaml）
- [ ] 無內容區塊超過 50 行（除非必要）

---

## P1: 高優先（High Priority）

**執行時限**: 1-2 週內完成  
**失敗影響**: 降低文檔可維護性，增加手動維護成本

### P1.1 🔧 實現自動化更新機制（Automated Update Mechanism）

**狀態**: 📋 TODO

**目標**: 實現 PROJECT_STATUS.md 和結構圖的自動更新

#### P1.1.1 PROJECT_STATUS.md 自動更新

```yaml
automation_target:
  file: "PROJECT_STATUS.md"
  update_frequency: "Daily (automated via CI)"
  data_sources:
    - "GitHub Issues (open/closed count)"
    - "GitHub PRs (recent merges)"
    - "CI/CD status (latest runs)"
    - "Git commit history (recent activity)"
```

**實現方案**:

```python
#!/usr/bin/env python3
# scripts/update-project-status.py
"""
Automated PROJECT_STATUS.md updater
"""

import os
import sys
from datetime import datetime
from github import Github
import yaml

def get_github_client():
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN not set")
    return Github(token)

def get_project_status(repo):
    """Fetch current project status from GitHub API"""
    status = {
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'open_issues': repo.open_issues_count,
        'recent_prs': [],
        'ci_status': 'OPERATIONAL',  # From latest workflow runs
    }
    
    # Get recent merged PRs (last 5)
    pulls = repo.get_pulls(state='closed', sort='updated')
    for pr in pulls[:5]:
        if pr.merged:
            status['recent_prs'].append({
                'number': pr.number,
                'title': pr.title,
                'merged_at': pr.merged_at.strftime('%Y-%m-%d')
            })
    
    return status

def update_status_file(status):
    """Update PROJECT_STATUS.md with new status"""
    template = f"""# Machine Native Ops - Project Status

<!-- GL Layer: GL90-99 Meta-Specification Layer -->
<!-- Purpose: Project status tracking and reporting -->

**Last Updated**: {status['last_updated']}  
**Status**: ✅ OPERATIONAL  
**Open Issues**: {status['open_issues']}

## Recent Updates

"""
    
    for pr in status['recent_prs']:
        template += f"- **PR #{pr['number']}**: {pr['title']} (merged {pr['merged_at']})\n"
    
    # Read existing content after "Recent Updates" section
    # and preserve it...
    
    with open('PROJECT_STATUS.md', 'w') as f:
        f.write(template)

if __name__ == '__main__':
    client = get_github_client()
    repo = client.get_repo('MachineNativeOps/machine-native-ops')
    status = get_project_status(repo)
    update_status_file(status)
    print("✅ PROJECT_STATUS.md updated")
```

**CI Workflow**:

```yaml
# .github/workflows/update-project-status.yml
name: Update Project Status

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  update-status:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install PyGithub PyYAML
          
      - name: Update PROJECT_STATUS.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/update-project-status.py
          
      - name: Commit changes
        run: |
          git config user.name "Status Update Bot"
          git config user.email "bot@machinenativeops.dev"
          git add PROJECT_STATUS.md
          git diff --cached --quiet || git commit -m "🤖 Auto-update PROJECT_STATUS.md"
          git push
```

**驗收條件**:
- [ ] Python 腳本已創建（scripts/update-project-status.py）
- [ ] CI workflow 已設置（.github/workflows/update-project-status.yml）
- [ ] 首次自動更新成功執行
- [ ] 手動驗證更新內容準確性

---

#### P1.1.2 README.md 結構圖自動生成

```yaml
automation_target:
  file: "README.md"
  section: "根層結構（極簡化）"
  update_trigger: "Directory structure change"
  markers:
    start: "<!-- STRUCTURE_START -->"
    end: "<!-- STRUCTURE_END -->"
```

**實現方案**:

```bash
#!/bin/bash
# scripts/update-readme-structure.sh
# Auto-generate directory structure diagram for README.md

set -e

echo "📊 Generating directory structure..."

# Generate structure (exclude common ignored dirs)
tree -L 2 -I 'node_modules|.git|__pycache__|*.pyc|.next|dist|build|coverage' \
  --charset ascii \
  --dirsfirst \
  -F \
  > /tmp/structure.txt

# Check if markers exist in README.md
if ! grep -q "<!-- STRUCTURE_START -->" README.md; then
  echo "❌ Structure markers not found in README.md"
  echo "Please add <!-- STRUCTURE_START --> and <!-- STRUCTURE_END --> markers"
  exit 1
fi

# Update README.md between markers (using a more maintainable approach)
# Step 1: Extract content before marker
sed -n '1,/<!-- STRUCTURE_START -->/p' README.md > /tmp/readme-before.txt

# Step 2: Extract content after marker
sed -n '/<!-- STRUCTURE_END -->/,$p' README.md > /tmp/readme-after.txt

# Step 3: Combine with new structure
cat /tmp/readme-before.txt > README.md.new
echo '```' >> README.md.new
cat /tmp/structure.txt >> README.md.new
echo '```' >> README.md.new
cat /tmp/readme-after.txt >> README.md.new

# Step 4: Replace original (keep backup)
mv README.md README.md.bak
mv README.md.new README.md

echo "✅ Structure diagram updated in README.md"

# Verify the change
if git diff --quiet README.md; then
  echo "ℹ️ No changes detected (structure unchanged)"
else
  echo "📝 Changes detected:"
  git diff README.md | head -20
fi
```

**CI Workflow**:

```yaml
# .github/workflows/update-readme-structure.yml
name: Update README Structure

on:
  push:
    paths:
      - '**/package.json'
      - '**/Cargo.toml'
      - 'controlplane/**'
      - 'workspace/**'
  workflow_dispatch:

jobs:
  update-structure:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Install tree command
        run: sudo apt-get install -y tree
        
      - name: Update structure diagram
        run: |
          bash scripts/update-readme-structure.sh
          
      - name: Commit changes
        run: |
          git config user.name "Structure Update Bot"
          git config user.email "bot@machinenativeops.dev"
          git add README.md
          git diff --cached --quiet || git commit -m "🤖 Auto-update README.md structure diagram"
          git push
```

**驗收條件**:
- [ ] Bash 腳本已創建（scripts/update-readme-structure.sh）
- [ ] README.md 已添加結構標記
- [ ] CI workflow 已設置
- [ ] 首次自動更新成功執行

---

### P1.2 📝 精簡並重組 README.md 內容（Content Simplification & Reorganization）

**狀態**: 📋 TODO

**目標**: 根據 P0.3 審計結果，移動詳細內容到 workspace/docs/

**執行步驟**:

1. **移動量子驗證詳細內容**:
   ```bash
   # 創建專門的量子驗證指南
   mkdir -p workspace/docs/quantum
   
   # 移動詳細內容（保留 README 中的簡要介紹）
   cat > workspace/docs/quantum/QUANTUM_VALIDATION_GUIDE.md << 'EOF'
   # 量子增強驗證系統完整指南
   
   ## 立即可用的驗證工具
   [從 README.md 移動的詳細內容...]
   EOF
   
   # 更新 README.md，保留簡要介紹 + 鏈接
   # 將詳細命令和配置移到 workspace/docs/quantum/
   ```

2. **移動架構詳細內容**:
   ```bash
   # 更新或創建 ARCHITECTURE.md
   cat > workspace/docs/ARCHITECTURE.md << 'EOF'
   # 系統架構詳細說明
   
   ## 目錄結構詳解
   [從 README.md 移動的詳細目錄說明...]
   EOF
   ```

3. **更新 README.md 引用**:
   ```markdown
   ## 🔬 量子增強驗證系統
   
   **快速概覽**: 8 維度驗證矩陣，99.3% 準確率，< 100ms 延遲
   
   **詳細文檔**: 
   - 完整指南: [workspace/docs/quantum/QUANTUM_VALIDATION_GUIDE.md](workspace/docs/quantum/QUANTUM_VALIDATION_GUIDE.md)
   - 整合報告: [workspace/docs/QUANTUM_VALIDATION_INTEGRATION_REPORT.md](workspace/docs/QUANTUM_VALIDATION_INTEGRATION_REPORT.md)
   
   **快速開始**:
   ```bash
   # 運行量子驗證
   python3 tools/validation/quantum_feature_extractor.py --input workspace/docs/
   ```
   [詳細命令選項請參考完整指南]
   ```

**驗收條件**:
- [ ] README.md 行數 <= 350 行（留 50 行緩衝）
- [ ] 所有詳細內容已移動到 workspace/docs/
- [ ] README.md 保留簡要介紹 + 鏈接
- [ ] 所有鏈接已驗證有效

---

### P1.3 🔍 實現 GL 合規檢查自動化（GL Compliance Automation）

**狀態**: 📋 TODO

**目標**: 自動檢查所有 root docs 的 GL Layer 註釋

```python
#!/usr/bin/env python3
# tools/python/gl_compliance_checker.py
"""
GL (Governance Layer) Compliance Checker for Documentation
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

GL_COMMENT_PATTERN = r'<!--\s*GL Layer:\s*GL\d{2}-\d{2}\s+.*?-->'
PURPOSE_COMMENT_PATTERN = r'<!--\s*Purpose:\s*.+?-->'

def check_file(filepath: Path) -> Dict[str, any]:
    """Check a single markdown file for GL compliance"""
    result = {
        'file': str(filepath),
        'has_gl_comment': False,
        'has_purpose_comment': False,
        'gl_layer': None,
        'purpose': None,
        'compliant': False,
        'issues': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for GL Layer comment
        gl_match = re.search(GL_COMMENT_PATTERN, content)
        if gl_match:
            result['has_gl_comment'] = True
            result['gl_layer'] = gl_match.group(0)
        else:
            result['issues'].append("Missing GL Layer comment")
            
        # Check for Purpose comment
        purpose_match = re.search(PURPOSE_COMMENT_PATTERN, content)
        if purpose_match:
            result['has_purpose_comment'] = True
            result['purpose'] = purpose_match.group(0)
        else:
            result['issues'].append("Missing Purpose comment")
            
        # Check if GL comment is in first 10 lines
        lines = content.split('\n')[:10]
        if not any(re.search(GL_COMMENT_PATTERN, line) for line in lines):
            result['issues'].append("GL Layer comment not in first 10 lines")
            
        result['compliant'] = len(result['issues']) == 0
        
    except Exception as e:
        result['issues'].append(f"Error reading file: {e}")
        
    return result

def check_root_docs() -> List[Dict]:
    """Check all root documentation files"""
    root_docs = [
        'README.md',
        'README-MACHINE.md',
        'PROJECT_STATUS.md',
        'QUICKSTART.md',
        'SECURITY.md',
        'todo.md'
    ]
    
    results = []
    for doc in root_docs:
        if os.path.exists(doc):
            results.append(check_file(Path(doc)))
        else:
            results.append({
                'file': doc,
                'compliant': False,
                'issues': ['File not found']
            })
            
    return results

def print_report(results: List[Dict]):
    """Print compliance report"""
    print("=" * 80)
    print("GL COMPLIANCE REPORT")
    print("=" * 80)
    
    compliant_count = sum(1 for r in results if r['compliant'])
    total_count = len(results)
    
    print(f"\nOverall: {compliant_count}/{total_count} files compliant")
    print(f"Compliance Rate: {compliant_count/total_count*100:.1f}%\n")
    
    for result in results:
        status = "✅ PASS" if result['compliant'] else "❌ FAIL"
        print(f"{status} {result['file']}")
        
        if result['has_gl_comment']:
            print(f"  GL Layer: {result['gl_layer']}")
        if result['has_purpose_comment']:
            print(f"  Purpose: {result['purpose']}")
            
        if result['issues']:
            print(f"  Issues:")
            for issue in result['issues']:
                print(f"    - {issue}")
        print()
        
    return compliant_count == total_count

if __name__ == '__main__':
    results = check_root_docs()
    all_compliant = print_report(results)
    sys.exit(0 if all_compliant else 1)
```

**CI Integration**:

```yaml
# .github/workflows/gl-compliance-check.yml
name: GL Compliance Check

on:
  push:
    paths:
      - '*.md'
  pull_request:
    paths:
      - '*.md'

jobs:
  check-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Run GL compliance checker
        run: python tools/python/gl_compliance_checker.py
```

**驗收條件**:
- [ ] GL compliance checker 已創建
- [ ] CI workflow 已設置
- [ ] 所有 root docs 100% GL 合規

---

## P2: 優化改進（Optimization Priority）

**執行時限**: 2-4 週內完成  
**失敗影響**: 不影響核心功能，但降低長期維護效率

### P2.1 📖 創建維護指南（Maintenance Guide）

**狀態**: 📋 TODO

**目標**: 文檔化文檔維護流程和責任

```markdown
# workspace/docs/DOCUMENTATION_MAINTENANCE.md

## 文檔維護指南

### 維護責任

| 文件 | 所有者 | 更新頻率 | 自動化程度 |
|------|--------|---------|-----------|
| README.md | Platform Team | 按需 | 30% |
| README-MACHINE.md | Governance Team | 按需 | 50% |
| PROJECT_STATUS.md | DevOps Team | 每日 | 80% |
| QUICKSTART.md | DX Team | 按需 | 20% |

### 更新流程

1. **識別需要更新的文檔**
2. **創建分支**: `docs/update-[file]-[topic]`
3. **進行編輯**
4. **運行驗證**: `make docs-validate`
5. **提交 PR**
6. **審查與合併**

### 自動化工具

- `scripts/update-project-status.py` - 自動更新 PROJECT_STATUS.md
- `scripts/update-readme-structure.sh` - 自動更新 README.md 結構圖
- `tools/python/gl_compliance_checker.py` - GL 合規檢查

### 品質標準

- 所有內部鏈接必須有效（100%）
- GL Layer 註釋必須存在（100%）
- README.md 不超過 400 行
- 代碼範例必須可執行
```

**驗收條件**:
- [ ] DOCUMENTATION_MAINTENANCE.md 已創建
- [ ] 包含維護責任矩陣
- [ ] 包含更新流程
- [ ] 包含品質標準

---

### P2.2 🎯 建立文檔品質指標（Documentation Quality Metrics）

**狀態**: 📋 TODO

**目標**: 建立可測量的文檔品質基線

```yaml
# workspace/docs/documentation-quality-metrics.yaml
metrics:
  freshness:
    description: "Time from change to doc update"
    target: "< 48 hours"
    measurement: "Git commit timestamp delta"
    current_baseline: "TBD"
    
  completeness:
    description: "Percentage of features documented"
    target: ">= 90%"
    measurement: "Feature inventory vs documented features"
    current_baseline: "TBD"
    
  accuracy:
    description: "Link validity and content accuracy"
    target: "100% valid links, <= 5% outdated content"
    measurement: "Automated link checker + manual review"
    current_baseline: "TBD"
    
  usability:
    description: "New user success rate"
    target: ">= 85%"
    measurement: "User testing completion rate"
    current_baseline: "TBD"
    
  automation_coverage:
    description: "Percentage of automated updates"
    target: ">= 70%"
    measurement: "Automated vs manual updates ratio"
    current_baseline: "30%"
```

**Dashboard** (可選，使用 GitHub Actions + Pages):

```python
# scripts/generate-docs-quality-dashboard.py
"""Generate documentation quality dashboard"""

import json
from datetime import datetime

def generate_dashboard():
    metrics = {
        'last_updated': datetime.now().isoformat(),
        'freshness': calculate_freshness(),
        'completeness': calculate_completeness(),
        'accuracy': calculate_accuracy(),
        'automation_coverage': calculate_automation_coverage()
    }
    
    with open('docs-quality-dashboard.json', 'w') as f:
        json.dump(metrics, f, indent=2)
        
    # Generate HTML dashboard
    html = f"""
    <html>
    <head><title>Documentation Quality Dashboard</title></head>
    <body>
      <h1>Documentation Quality Metrics</h1>
      <p>Last Updated: {metrics['last_updated']}</p>
      <ul>
        <li>Freshness: {metrics['freshness']}</li>
        <li>Completeness: {metrics['completeness']}</li>
        <li>Accuracy: {metrics['accuracy']}</li>
        <li>Automation Coverage: {metrics['automation_coverage']}</li>
      </ul>
    </body>
    </html>
    """
    
    with open('docs-quality-dashboard.html', 'w') as f:
        f.write(html)
```

**驗收條件**:
- [ ] Metrics YAML 已定義
- [ ] 基線數據已收集
- [ ] Dashboard 生成腳本已創建（可選）

---

### P2.3 🔄 更新 PR Template（PR Template Update）

**狀態**: 📋 TODO

**目標**: PR template 包含文檔更新檢查

```markdown
# .github/pull_request_template.md

## 變更說明
<!-- 描述你的變更 -->

## 變更類型
- [ ] Bug 修復
- [ ] 新功能
- [ ] 架構變更
- [ ] 文檔更新
- [ ] 其他

## 文檔檢查 ✅
<!-- 如果你的變更影響以下方面，請確保更新相應文檔 -->

- [ ] 我已檢查是否需要更新文檔
- [ ] 如果需要，我已更新以下文檔：
  - [ ] README.md（架構或功能變更）
  - [ ] PROJECT_STATUS.md（狀態或里程碑變更）
  - [ ] workspace/docs/（詳細技術文檔）
  - [ ] API 文檔（API 變更）
  - [ ] 其他：___________

## 驗證
- [ ] 所有測試通過
- [ ] 代碼審查完成
- [ ] 文檔鏈接已驗證（如有更新）
- [ ] GL 合規檢查通過（如涉及 root docs）

## 額外說明
<!-- 其他需要說明的內容 -->
```

**驗收條件**:
- [ ] PR template 已更新
- [ ] 包含文檔檢查清單
- [ ] 團隊已知悉新流程

---

## 結構交付視圖（Delivery Structure View）

### 新增文件

```
workspace/docs/refactor_playbooks/
├── 02_integration/
│   └── documentation_integration.md  ✅ CREATED (Phase 2)
└── 03_refactor/
    └── meta/
        └── documentation_refactor.md  ✅ CREATED (Phase 3, this file)

workspace/docs/
├── DOCUMENTATION_MAINTENANCE.md      📋 TODO (P2.1)
├── documentation-quality-metrics.yaml 📋 TODO (P2.2)
├── quantum/
│   └── QUANTUM_VALIDATION_GUIDE.md   📋 TODO (P1.2)
└── ARCHITECTURE.md                   📋 TODO (P1.2, may already exist)

scripts/
├── update-project-status.py          📋 TODO (P1.1.1)
└── update-readme-structure.sh        📋 TODO (P1.1.2)

tools/python/
└── gl_compliance_checker.py          📋 TODO (P1.3)

.github/workflows/
├── validate-docs-links.yml           📋 TODO (P0.2)
├── update-project-status.yml         📋 TODO (P1.1.1)
├── update-readme-structure.yml       📋 TODO (P1.1.2)
└── gl-compliance-check.yml           📋 TODO (P1.3)

.github/
└── pull_request_template.md          📋 TODO (P2.3, may need update)

.markdown-link-check.json             📋 TODO (P0.2)
```

### 修改文件

```
README.md                             📋 TODO (P1.2)
  - 添加結構標記 <!-- STRUCTURE_START/END -->
  - 精簡詳細內容
  - 添加鏈接到 workspace/docs/

PROJECT_STATUS.md                     📋 TODO (P1.1.1)
  - 添加自動更新標記
  - 結構化狀態區塊

workspace/docs/DOCUMENTATION_INDEX.md 📋 TODO (P1.2)
  - 更新文檔鏈接
  - 添加新創建的文檔
```

---

## 執行時間線（Execution Timeline）

```yaml
week_1:
  focus: "P0 關鍵任務"
  tasks:
    - P0.1: ✅ DONE
    - P0.2: ⏳ IN PROGRESS
    - P0.3: 📋 TODO
  target_completion: "100% P0"
  
week_2:
  focus: "P1 高優先任務（自動化）"
  tasks:
    - P1.1.1: PROJECT_STATUS.md 自動更新
    - P1.1.2: README.md 結構圖自動更新
    - P1.3: GL 合規檢查
  target_completion: "80% P1"
  
week_3:
  focus: "P1 高優先任務（內容重組）"
  tasks:
    - P1.2: 精簡 README.md
  target_completion: "100% P1"
  
week_4:
  focus: "P2 優化任務"
  tasks:
    - P2.1: 維護指南
    - P2.2: 品質指標
    - P2.3: PR template
  target_completion: "100% P2"
```

---

## 驗收測試（Acceptance Testing）

### 自動化測試

```bash
# tests/documentation/test_root_docs.py
import pytest
import os
from pathlib import Path

def test_all_root_docs_exist():
    """Verify all root documentation files exist"""
    required_docs = [
        'README.md',
        'README-MACHINE.md',
        'PROJECT_STATUS.md',
        'QUICKSTART.md',
        'SECURITY.md',
        'todo.md'
    ]
    
    for doc in required_docs:
        assert os.path.exists(doc), f"{doc} is missing"

def test_readme_line_count():
    """Verify README.md does not exceed line limit"""
    with open('README.md', 'r') as f:
        lines = f.readlines()
    
    assert len(lines) <= 400, f"README.md has {len(lines)} lines (max 400)"

def test_gl_comments_present():
    """Verify GL Layer comments are present"""
    from tools.python.gl_compliance_checker import check_root_docs
    
    results = check_root_docs()
    compliant = all(r['compliant'] for r in results)
    
    assert compliant, "Not all root docs are GL compliant"

def test_no_broken_links():
    """Verify no broken internal links"""
    # This would integrate with markdown-link-check
    # For now, placeholder
    pass
```

### 手動測試清單

```yaml
manual_testing:
  - test: "新用戶導航測試"
    steps:
      - "清除所有知識，模擬新用戶"
      - "閱讀 README.md"
      - "跟隨 QUICKSTART.md 完成設置"
    success_criteria: "無需外部幫助完成初始化"
    
  - test: "文檔一致性測試"
    steps:
      - "比對 README.md 結構圖與實際目錄"
      - "驗證所有交叉引用有效"
    success_criteria: "100% 匹配"
    
  - test: "自動化功能測試"
    steps:
      - "觸發 CI workflow"
      - "驗證 PROJECT_STATUS.md 自動更新"
      - "驗證 README.md 結構圖自動更新"
    success_criteria: "所有自動化正常運作"
```

---

## 回滾策略（Rollback Strategy）

```yaml
rollback_procedures:
  automated_updates:
    trigger: "自動更新導致錯誤內容"
    action:
      - "立即停用相關 CI workflow"
      - "Git revert 最後一次自動提交"
      - "人工審查並修正"
      - "更新自動化腳本"
      - "測試後重新啟用"
    
  content_migration:
    trigger: "內容移動導致鏈接失效或信息丟失"
    action:
      - "Git revert 內容遷移 commit"
      - "修正鏈接或恢復內容"
      - "重新執行遷移"
      
  structure_changes:
    trigger: "結構變更導致用戶困惑"
    action:
      - "收集用戶反饋"
      - "評估影響範圍"
      - "決定是 revert 或漸進調整"
```

---

## 成功指標（Success Metrics）

```yaml
success_metrics:
  immediate:
    - metric: "P0 任務完成率"
      target: "100%"
      deadline: "Week 1"
      
    - metric: "交叉引用有效性"
      target: "100%"
      deadline: "Week 1"
      
  short_term:
    - metric: "自動化覆蓋率"
      target: ">= 70%"
      deadline: "Week 3"
      
    - metric: "README.md 行數"
      target: "<= 350 lines"
      deadline: "Week 3"
      
  long_term:
    - metric: "文檔維護成本"
      target: "< 2 hours/week"
      measurement: "人工更新時間"
      deadline: "Month 2"
      
    - metric: "新用戶成功率"
      target: ">= 85%"
      measurement: "Quick start 完成率"
      deadline: "Month 3"
```

---

## 相關資源（Related Resources）

- **Phase 2 Integration Playbook**: [documentation_integration.md](../../02_integration/documentation_integration.md)
- **Documentation Index**: [workspace/docs/DOCUMENTATION_INDEX.md](../../../DOCUMENTATION_INDEX.md)
- **Three-Phase Refactoring Plan**: [THREE_PHASE_REFACTORING_EXECUTION_PLAN.md](../../../THREE_PHASE_REFACTORING_EXECUTION_PLAN.md)
- **Refactor Playbooks README**: [workspace/docs/refactor_playbooks/README.md](../../README.md)

---

**劇本版本**: 1.0.0  
**創建日期**: 2026-01-19  
**創建者**: Documentation Integration Task Force  
**下次審查**: 2026-02-19  
**狀態**: ⏳ IN PROGRESS
