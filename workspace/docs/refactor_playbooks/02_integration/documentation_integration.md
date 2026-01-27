# Documentation Layer 集成劇本（Integration Playbook）

> **GL Layer**: GL90-99 Meta-Specification Layer  
> **Phase**: 02_integration (集成階段)  
> **Target**: Root documentation files (README.md, README-MACHINE.md, PROJECT_STATUS.md, QUICKSTART.md)  
> **Last Updated**: 2026-01-19

---

## 1. 模組邊界定義（Module Boundary Definition）

### 1.1 屬於文檔層的職責

**Root Layer Documentation** 負責：

- ✅ **項目概覽（Project Overview）**: README.md - 人類可讀的項目介紹
- ✅ **機器可讀規範（Machine-Readable Spec）**: README-MACHINE.md - AI 代理和自動化工具的入口
- ✅ **項目狀態（Project Status）**: PROJECT_STATUS.md - 實時狀態追蹤
- ✅ **快速開始（Quick Start）**: QUICKSTART.md - 3 步驟快速上手指南
- ✅ **安全政策（Security Policy）**: SECURITY.md - 安全報告與政策
- ✅ **任務追蹤（Task Tracking）**: todo.md - GL 層級更新狀態

### 1.2 不屬於文檔層的職責（由其他模組負責）

以下職責**不屬於** Root Layer Documentation：

- ❌ **詳細技術文檔**: 由 `workspace/docs/` 負責
- ❌ **API 文檔**: 由 `workspace/docs/api/` 負責
- ❌ **架構設計文檔**: 由 `workspace/docs/architecture/` 負責
- ❌ **治理詳細規範**: 由 `controlplane/documentation/` 負責
- ❌ **重構劇本**: 由 `workspace/docs/refactor_playbooks/` 負責
- ❌ **操作手冊**: 由 `workspace/docs/operations/` 負責

### 1.3 與其他模組的交界線

```yaml
boundary_definition:
  root_documentation:
    scope: "High-level overview, quick navigation, project status"
    depth: "1-2 levels deep, links to detailed docs"
    audience: ["New users", "Project managers", "AI agents"]
    
  workspace_docs:
    scope: "Detailed technical documentation"
    depth: "Unlimited, comprehensive coverage"
    audience: ["Developers", "Architects", "DevOps engineers"]
    
  controlplane_docs:
    scope: "Governance, policies, specifications"
    depth: "Detailed governance rules and schemas"
    audience: ["Governance team", "Compliance officers", "AI agents"]
```

---

## 2. 公開介面規格（Public Interface Specification）

### 2.1 文檔結構契約（Documentation Structure Contract）

#### README.md 結構標準

```yaml
readme_structure:
  required_sections:
    - name: "Project Header"
      content: ["Title", "GL Layer comment", "Quick Navigation"]
      
    - name: "Current Focus"
      content: ["Recent updates", "Active initiatives", "Key metrics"]
      
    - name: "Architecture Overview"
      content: ["Taxonomy Root Layer", "Directory structure", "Design principles"]
      
    - name: "Quick Start"
      content: ["Environment setup", "Validation steps", "First tasks"]
      
    - name: "CI/CD System"
      content: ["Pipeline overview", "Key features", "Integration points"]
      
    - name: "Directory Guide"
      content: ["FHS directories", "Controlplane", "Workspace"]
      
    - name: "Important Notes"
      content: ["Path updates", "Permissions", "Constraints"]
      
  optional_sections:
    - "Advanced Features"
    - "Troubleshooting"
    - "Related Resources"
    
  metadata:
    gl_layer: "GL90-99 Meta-Specification Layer"
    purpose_comment: "<!-- Purpose: Project overview and navigation -->"
    version: "Semantic version at bottom"
    last_updated: "Date in YYYY-MM-DD format"
```

#### README-MACHINE.md 結構標準

```yaml
readme_machine_structure:
  required_sections:
    - name: "Machine-Readable Header"
      content: ["YAML frontmatter", "GL Layer", "Purpose"]
      
    - name: "Quick Start for AI Agents"
      content: ["Manifest location", "CLI commands", "API endpoints"]
      
    - name: "AI Interfaces"
      content: ["Validation endpoint", "Generation endpoint", "Query endpoint"]
      
    - name: "Schemas and Contracts"
      content: ["Schema locations", "Contract definitions"]
      
  format:
    style: "Machine-first, human-readable"
    code_blocks: "Executable examples"
    data_format: "YAML for structured data"
```

### 2.2 文檔更新協議（Documentation Update Protocol）

```yaml
update_protocol:
  triggers:
    - event: "Architecture change"
      action: "Update README.md architecture section"
      validation: "Structure diagram matches filesystem"
      
    - event: "New feature added"
      action: "Add to Current Focus section"
      validation: "Link to detailed docs exists"
      
    - event: "Status change"
      action: "Update PROJECT_STATUS.md"
      validation: "Status reflects actual system state"
      
    - event: "GL layer update"
      action: "Update todo.md and README.md GL comments"
      validation: "GL compliance check passes"
      
  update_frequency:
    readme_md: "On major changes (monthly or on release)"
    readme_machine_md: "On governance/interface changes"
    project_status_md: "Weekly or on significant events"
    quickstart_md: "On onboarding flow changes"
    todo_md: "Daily (automated GL layer updates)"
```

### 2.3 交叉引用標準（Cross-Reference Standard）

```yaml
cross_reference_rules:
  internal_links:
    format: "Relative paths from repo root"
    examples:
      - "[PROJECT_STATUS.md](PROJECT_STATUS.md)"
      - "[workspace/docs/DOCUMENTATION_INDEX.md](workspace/docs/DOCUMENTATION_INDEX.md)"
    
  external_links:
    format: "Absolute URLs with context"
    examples:
      - "[FHS 標準](https://refspecs.linuxfoundation.org/FHS_3.0/)"
    
  deep_links:
    format: "Link to detailed docs for >2 levels of depth"
    rule: "Root docs stay shallow, link to workspace/docs for details"
```

---

## 3. 依賴關係（Dependency Strategy）

### 3.1 上游依賴（Upstream Dependencies）

Root Layer Documentation **依賴**：

```yaml
upstream_dependencies:
  filesystem_structure:
    source: "Actual repository layout"
    sync: "README.md structure diagram must match reality"
    validation: "tree command output comparison"
    
  governance_manifest:
    source: "governance-manifest.yaml"
    sync: "README-MACHINE.md references correct manifest"
    validation: "YAML parsing and schema validation"
    
  project_status:
    source: "CI/CD state, issue tracker, git history"
    sync: "PROJECT_STATUS.md reflects actual status"
    validation: "Automated status checker"
    
  gl_layers:
    source: "GL00-99 specifications"
    sync: "GL comments in all root docs"
    validation: "GL compliance checker"
```

### 3.2 下游使用者（Downstream Consumers）

以下模組/工具**依賴** Root Layer Documentation：

```yaml
downstream_consumers:
  human_readers:
    - role: "New developers"
      entry_point: "README.md"
      expectation: "Clear overview and quick start"
      
    - role: "Project managers"
      entry_point: "PROJECT_STATUS.md"
      expectation: "Current status and metrics"
      
  ai_agents:
    - agent: "GitHub Copilot"
      entry_point: "README-MACHINE.md"
      expectation: "Executable governance commands"
      
    - agent: "Automation bots"
      entry_point: "governance-manifest.yaml (referenced in README-MACHINE.md)"
      expectation: "Machine-readable interfaces"
      
  navigation_systems:
    - system: "DOCUMENTATION_INDEX.md"
      dependency: "Links to root docs"
      expectation: "All root docs listed and categorized"
      
    - system: "GitHub UI"
      dependency: "README.md as landing page"
      expectation: "Professional first impression"
```

### 3.3 依賴方向圖（Dependency Direction Graph）

```text
┌─────────────────────────────────────────────────────────┐
│                    External Users                        │
│  (Developers, PMs, AI Agents, GitHub UI)                │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               Root Layer Documentation                   │
│  README.md, README-MACHINE.md, PROJECT_STATUS.md, etc.  │
└────────────────────────┬────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ workspace/   │  │ controlplane/│  │ Filesystem   │
│ docs/        │  │ documentation│  │ Structure    │
└──────────────┘  └──────────────┘  └──────────────┘
```

**依賴原則**:
- ✅ Root docs **消費** workspace/controlplane docs（通過鏈接引用）
- ✅ Root docs **反映** filesystem structure（單向觀察）
- ❌ **禁止** workspace docs 依賴 root docs（避免循環）

---

## 4. 遷移策略（Migration Strategy）

### 4.1 從舊架構到新架構的路徑

#### Phase 1: 邊界清晰化（Boundary Clarification）

**目標**: 明確區分 Root 和 Workspace 文檔職責

```yaml
phase_1:
  duration: "1 week"
  tasks:
    - id: "P1.1"
      task: "審計 README.md 內容深度"
      action: "識別超過 2 層深度的內容"
      outcome: "移動詳細內容到 workspace/docs/"
      
    - id: "P1.2"
      task: "建立文檔邊界規則"
      action: "創建 documentation_integration.md (本文件)"
      outcome: "明確的職責分離"
      
    - id: "P1.3"
      task: "更新交叉引用"
      action: "確保所有深度內容有 workspace/docs/ 鏈接"
      outcome: "清晰的導航路徑"
      
  validation:
    - "README.md 不超過 400 行"
    - "所有詳細內容有對應 workspace/docs/ 文件"
    - "交叉引用 100% 可達"
```

#### Phase 2: 自動化同步機制（Automated Sync Mechanism）

**目標**: 建立自動化文檔更新流程

```yaml
phase_2:
  duration: "2 weeks"
  tasks:
    - id: "P2.1"
      task: "實現 PROJECT_STATUS.md 自動更新"
      action: "創建 CI job 從 git/issues/PRs 提取狀態"
      outcome: "每日自動更新狀態文檔"
      
    - id: "P2.2"
      task: "實現結構圖自動生成"
      action: "tree 命令輸出 → README.md 結構區塊"
      outcome: "結構圖永遠準確"
      
    - id: "P2.3"
      task: "實現 GL 合規檢查"
      action: "掃描所有 root docs 的 GL 註釋"
      outcome: "GL 合規自動驗證"
      
  validation:
    - "CI job 執行無錯誤"
    - "狀態文檔與實際狀態一致性 > 95%"
    - "GL 合規檢查通過"
```

#### Phase 3: 維護流程標準化（Maintenance Process Standardization）

**目標**: 建立長期維護標準

```yaml
phase_3:
  duration: "1 week"
  tasks:
    - id: "P3.1"
      task: "文檔化更新協議"
      action: "創建 DOCUMENTATION_MAINTENANCE.md"
      outcome: "清晰的維護責任與流程"
      
    - id: "P3.2"
      task: "設置文檔審查檢查點"
      action: "PR template 包含文檔更新檢查"
      outcome: "架構變更自動觸發文檔審查"
      
    - id: "P3.3"
      task: "建立文檔品質指標"
      action: "定義可測量的文檔品質標準"
      outcome: "持續監控文檔健康度"
      
  validation:
    - "維護文檔存在且完整"
    - "PR template 包含文檔檢查"
    - "品質指標基線建立"
```

### 4.2 向後相容性策略（Backward Compatibility Strategy）

```yaml
backward_compatibility:
  principles:
    - "保持現有 README.md 路徑不變"
    - "現有鏈接持續有效（通過 symlinks 或 redirects）"
    - "逐步廢棄，而非突然移除"
    
  deprecation_process:
    step_1:
      action: "在舊位置添加 deprecation notice"
      duration: "1 month"
      
    step_2:
      action: "重定向到新位置"
      duration: "2 months"
      
    step_3:
      action: "移除舊內容，保留重定向"
      duration: "Permanent redirect"
      
  example:
    old_path: "README.md (with excessive detail)"
    deprecation: "<!-- ⚠️ Detailed content moved to workspace/docs/ARCHITECTURE.md -->"
    new_structure: "README.md (overview) + link to workspace/docs/ARCHITECTURE.md"
```

---

## 5. 整合測試（Integration Testing）

### 5.1 測試場景（Test Scenarios）

```yaml
test_scenarios:
  scenario_1:
    name: "新用戶導航測試"
    steps:
      - "新用戶打開 README.md"
      - "閱讀快速開始章節"
      - "點擊鏈接到 QUICKSTART.md"
      - "執行 3 步驟快速開始"
    expected_outcome: "用戶成功完成初始化，無需外部幫助"
    validation: "用戶反饋 + 完成率統計"
    
  scenario_2:
    name: "AI 代理自動化測試"
    steps:
      - "AI 代理讀取 README-MACHINE.md"
      - "解析 governance-manifest.yaml 位置"
      - "執行 governance_agent.py validate 命令"
    expected_outcome: "AI 代理成功執行治理驗證"
    validation: "命令執行成功，輸出符合預期"
    
  scenario_3:
    name: "文檔一致性測試"
    steps:
      - "提取 README.md 中的目錄結構圖"
      - "執行 tree 命令獲取實際結構"
      - "比較兩者差異"
    expected_outcome: "結構圖與實際文件系統 100% 匹配"
    validation: "自動化比對腳本"
    
  scenario_4:
    name: "交叉引用完整性測試"
    steps:
      - "提取所有 root docs 中的內部鏈接"
      - "驗證每個鏈接目標存在"
      - "驗證鏈接路徑正確"
    expected_outcome: "0 個死鏈接，100% 可達"
    validation: "link-checker 工具"
```

### 5.2 驗收條件（Acceptance Criteria）

```yaml
acceptance_criteria:
  documentation_quality:
    - metric: "README.md 行數"
      target: "<= 400 lines"
      current: "400 lines"
      status: "✅ PASS"
      
    - metric: "交叉引用準確性"
      target: "100% valid links"
      validation: "link-checker scan"
      
    - metric: "結構圖準確性"
      target: "100% match with filesystem"
      validation: "tree diff = 0"
      
  maintainability:
    - metric: "自動化更新覆蓋率"
      target: ">= 80% of status updates automated"
      validation: "Manual vs automated update ratio"
      
    - metric: "GL 合規性"
      target: "100% of root docs have GL comments"
      validation: "GL compliance checker"
      
  usability:
    - metric: "新用戶完成率"
      target: ">= 90% complete quick start without help"
      validation: "User testing + analytics"
      
    - metric: "AI 代理成功率"
      target: "100% of governance commands executable"
      validation: "Automated command execution tests"
```

### 5.3 效能與可靠性指標（Performance & Reliability Metrics）

```yaml
performance_metrics:
  documentation_freshness:
    metric: "Time from change to doc update"
    target: "< 24 hours for automated updates"
    measurement: "Git commit timestamp delta"
    
  link_availability:
    metric: "Internal link uptime"
    target: "99.9% (allow for brief refactoring periods)"
    measurement: "Continuous link checking"
    
  search_efficiency:
    metric: "Time to find information"
    target: "< 3 clicks from README.md to any doc"
    measurement: "Navigation depth analysis"
```

---

## 6. 維護責任與流程（Maintenance Responsibility & Process）

### 6.1 維護責任矩陣（Maintenance Responsibility Matrix）

```yaml
maintenance_matrix:
  readme_md:
    owner: "Platform Team"
    reviewers: ["Architecture Team", "Documentation Team"]
    update_trigger: ["Architecture changes", "Major features", "Releases"]
    automation_level: "30% (structure diagram, version)"
    
  readme_machine_md:
    owner: "Governance Team"
    reviewers: ["AI/Automation Team"]
    update_trigger: ["Governance changes", "API changes"]
    automation_level: "50% (schema references, command examples)"
    
  project_status_md:
    owner: "DevOps Team"
    reviewers: ["Project Management"]
    update_trigger: ["Status changes", "Milestones", "Incidents"]
    automation_level: "80% (CI status, issue tracking, git history)"
    
  quickstart_md:
    owner: "Developer Experience Team"
    reviewers: ["New developer feedback"]
    update_trigger: ["Onboarding flow changes", "Tooling updates"]
    automation_level: "20% (mostly manual, user-driven)"
    
  todo_md:
    owner: "GL Compliance Bot"
    reviewers: ["Architecture Team"]
    update_trigger: ["GL layer updates"]
    automation_level: "100% (fully automated)"
```

### 6.2 更新流程（Update Workflow）

```yaml
update_workflow:
  manual_update:
    steps:
      - "Create branch: docs/update-readme-[topic]"
      - "Edit documentation files"
      - "Run documentation validation: make docs-validate"
      - "Create PR with documentation label"
      - "Request review from designated reviewers"
      - "Merge after approval"
      
  automated_update:
    triggers:
      - event: "CI pipeline completion"
        action: "Update PROJECT_STATUS.md CI status"
        
      - event: "Directory structure change"
        action: "Regenerate README.md structure diagram"
        
      - event: "GL layer spec update"
        action: "Update todo.md GL checklist"
        
    process:
      - "Bot creates commit on main branch"
      - "Notify maintainers in Slack/GitHub Discussion"
      - "Manual review within 24 hours"
      - "Rollback if issues detected"
```

### 6.3 品質保證（Quality Assurance）

```yaml
quality_assurance:
  pre_commit_checks:
    - "Markdown linting (markdownlint)"
    - "Link validation (markdown-link-check)"
    - "GL comment presence check"
    - "YAML frontmatter validation"
    
  ci_checks:
    - "Documentation build test"
    - "Cross-reference integrity"
    - "Structure diagram accuracy"
    - "Search index update"
    
  periodic_audits:
    frequency: "Monthly"
    checks:
      - "Documentation completeness"
      - "Outdated information detection"
      - "User feedback integration"
      - "Metrics review (freshness, availability)"
```

---

## 7. 實施計劃（Implementation Plan）

### 7.1 階段 1：邊界清晰化（Week 1）

```yaml
week_1:
  tasks:
    - task: "創建本集成劇本"
      assignee: "Documentation Team"
      deliverable: "documentation_integration.md"
      status: "✅ DONE"
      
    - task: "審計 README.md 內容深度"
      assignee: "Architecture Team"
      deliverable: "Content depth analysis report"
      status: "⏳ IN PROGRESS"
      
    - task: "識別需要移動的詳細內容"
      assignee: "Documentation Team"
      deliverable: "Content migration list"
      status: "📋 TODO"
      
    - task: "更新 workspace/docs/ 結構"
      assignee: "Platform Team"
      deliverable: "Updated workspace docs structure"
      status: "📋 TODO"
```

### 7.2 階段 2：自動化機制（Week 2-3）

```yaml
week_2_3:
  tasks:
    - task: "實現 PROJECT_STATUS.md 自動更新"
      assignee: "DevOps Team"
      deliverable: ".github/workflows/update-project-status.yml"
      status: "📋 TODO"
      
    - task: "實現結構圖自動生成"
      assignee: "Automation Team"
      deliverable: "scripts/generate-structure-diagram.sh"
      status: "📋 TODO"
      
    - task: "實現 GL 合規檢查"
      assignee: "Governance Team"
      deliverable: "tools/python/gl_compliance_checker.py"
      status: "📋 TODO"
      
    - task: "設置 CI 文檔驗證"
      assignee: "DevOps Team"
      deliverable: ".github/workflows/docs-validation.yml"
      status: "📋 TODO"
```

### 7.3 階段 3：標準化與優化（Week 4）

```yaml
week_4:
  tasks:
    - task: "創建維護指南"
      assignee: "Documentation Team"
      deliverable: "workspace/docs/DOCUMENTATION_MAINTENANCE.md"
      status: "📋 TODO"
      
    - task: "更新 PR template"
      assignee: "Platform Team"
      deliverable: ".github/pull_request_template.md"
      status: "📋 TODO"
      
    - task: "建立品質指標基線"
      assignee: "DevOps Team"
      deliverable: "Documentation quality dashboard"
      status: "📋 TODO"
      
    - task: "用戶測試與反饋收集"
      assignee: "Developer Experience Team"
      deliverable: "User testing report"
      status: "📋 TODO"
```

---

## 8. 成功指標（Success Metrics）

### 8.1 短期指標（1 個月內）

```yaml
short_term_metrics:
  - metric: "文檔邊界清晰度"
    measurement: "Team survey: 'Can you clearly distinguish root vs workspace docs?'"
    target: ">= 90% 'Yes'"
    
  - metric: "交叉引用完整性"
    measurement: "Automated link checker"
    target: "0 broken links"
    
  - metric: "GL 合規性"
    measurement: "GL compliance checker"
    target: "100% of root docs compliant"
```

### 8.2 中期指標（3 個月內）

```yaml
mid_term_metrics:
  - metric: "自動化覆蓋率"
    measurement: "% of updates that are automated"
    target: ">= 70%"
    
  - metric: "新用戶成功率"
    measurement: "% of new users completing quick start without help"
    target: ">= 85%"
    
  - metric: "文檔新鮮度"
    measurement: "Average time from change to doc update"
    target: "< 48 hours"
```

### 8.3 長期指標（6 個月內）

```yaml
long_term_metrics:
  - metric: "文檔滿意度"
    measurement: "Developer satisfaction survey"
    target: ">= 4.5/5.0"
    
  - metric: "維護成本"
    measurement: "Hours spent on manual doc updates per week"
    target: "< 2 hours/week"
    
  - metric: "AI 代理成功率"
    measurement: "% of governance commands successfully executed by AI"
    target: "100%"
```

---

## 9. 風險與緩解（Risks & Mitigation）

```yaml
risks:
  - risk: "文檔碎片化（Content fragmentation）"
    probability: "Medium"
    impact: "High"
    mitigation:
      - "明確邊界定義（本文件）"
      - "交叉引用標準強制執行"
      - "定期一致性審計"
      
  - risk: "自動化更新錯誤（Automated update errors）"
    probability: "Low"
    impact: "Medium"
    mitigation:
      - "自動化更新需要人工審查（24 小時窗口）"
      - "快速回滾機制"
      - "詳細的變更日誌"
      
  - risk: "過時信息（Outdated information）"
    probability: "Medium"
    impact: "Medium"
    mitigation:
      - "自動新鮮度檢查（CI job）"
      - "月度文檔審計"
      - "用戶反饋機制"
      
  - risk: "複雜度增長（Complexity growth）"
    probability: "High"
    impact: "Low"
    mitigation:
      - "嚴格的 '400 行 README' 限制"
      - "定期簡化審查"
      - "深度內容強制外移到 workspace/docs/"
```

---

## 10. 下一步行動（Next Actions）

### 立即行動（Immediate Actions）

```yaml
immediate_actions:
  - action: "審查並批准本集成劇本"
    owner: "Architecture Team + Documentation Team"
    deadline: "2026-01-20"
    
  - action: "創建對應的重構劇本（Phase 3）"
    owner: "Documentation Team"
    deliverable: "workspace/docs/refactor_playbooks/03_refactor/meta/documentation_refactor.md"
    deadline: "2026-01-21"
    
  - action: "啟動 Phase 1 實施"
    owner: "Documentation Team"
    deadline: "2026-01-27"
```

### 後續行動（Follow-up Actions）

```yaml
followup_actions:
  - action: "Phase 2 實施（自動化）"
    deadline: "2026-02-10"
    
  - action: "Phase 3 實施（標準化）"
    deadline: "2026-02-17"
    
  - action: "首次品質審計"
    deadline: "2026-02-24"
```

---

## 附錄 A：文檔模板（Documentation Templates）

### A.1 Root README.md Template

```markdown
# ProjectName

<!-- GL Layer: GL90-99 Meta-Specification Layer -->
<!-- Purpose: Project overview and navigation -->

> **📚 Quick Navigation**: 
> - **Project Status** → [PROJECT_STATUS.md](PROJECT_STATUS.md)
> - **Documentation Index** → [workspace/docs/DOCUMENTATION_INDEX.md](workspace/docs/DOCUMENTATION_INDEX.md)
> - **Quick Start** → [QUICKSTART.md](QUICKSTART.md)

[Brief project description - 2-3 sentences]

---

## 🎯 當前焦點

[Current initiatives, recent updates, key metrics - keep updated]

---

## 🏗️ 架構概述

[High-level architecture overview - max 2 levels deep, link to workspace/docs/ for details]

---

## 🚀 快速開始

[3-5 step quick start - executable commands, expected outcomes]

---

## 📁 目錄說明

[Directory structure with brief explanations - link to detailed docs]

---

## 📚 文檔

[Links to all major documentation areas]

---

**版本**: v1.0.0  
**最後更新**: YYYY-MM-DD  
**維護者**: TeamName
```

### A.2 PROJECT_STATUS.md Template

```markdown
# ProjectName - Project Status

<!-- GL Layer: GL90-99 Meta-Specification Layer -->
<!-- Purpose: Project status tracking and reporting -->

**Last Updated**: YYYY-MM-DD  
**Status**: ✅ OPERATIONAL / ⚠️ DEGRADED / ❌ DOWN  
**Compliance**: [List compliance standards]

## Current State

### Systems Operational

- ✅ System 1 - Status description
- ✅ System 2 - Status description

### Recent Updates (YYYY-MM-DD)

[List of recent significant changes]

## Quick Commands

[Frequently used commands for status checking]

---

**Automated Status Updates**: Every 24 hours via CI/CD
```

---

## 附錄 B：自動化腳本範例（Automation Script Examples）

### B.1 結構圖生成腳本

```bash
#!/bin/bash
# scripts/generate-structure-diagram.sh
# Generate directory structure diagram for README.md

tree -L 2 -I 'node_modules|.git|__pycache__|*.pyc' --charset ascii > /tmp/structure.txt

# Insert into README.md between markers (using a maintainable multi-step approach)
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
```

### B.2 交叉引用驗證腳本

```bash
#!/bin/bash
# scripts/validate-doc-links.sh
# Validate all internal links in root documentation

find . -maxdepth 1 -name "*.md" -exec markdown-link-check {} \;

if [ $? -eq 0 ]; then
  echo "✅ All links valid"
  exit 0
else
  echo "❌ Broken links detected"
  exit 1
fi
```

---

**文檔版本**: 1.0.0  
**創建日期**: 2026-01-19  
**創建者**: Documentation Integration Task Force  
**下次審查**: 2026-02-19
