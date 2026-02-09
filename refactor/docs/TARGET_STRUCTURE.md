# 目標專案結構文檔

## 設計時間
2026-02-09 13:16:31

## 設計原則

1. **統一命名規範** - 使用 `gov-` 前綴（kebab-case）
2. **清晰層級結構** - L0-L4 治理層級
3. **最小根層目錄** - < 15 個根層目錄
4. **職責分離** - 明確的功能和責任邊界
5. **可擴展性** - 支持未來增長

## 目標根層目錄結構

```
indestructibleautoops/
├── governance/                    # 統一治理系統（整合所有 governance 相關）
├── iaops/                         # IAOPS 治理引擎
├── indestructibleautoops/         # Python 包
├── machinenativeops/              # 機器原生操作
├── platforms/                     # 平台系統
├── deployment/                    # 部署配置
├── docs/                          # 文檔
├── tests/                         # 測試
├── scripts/                       # 腳本
├── config/                        # 配置
├── refactor/                      # 重構工具和文檔
├── audit-automation/              # 審計自動化
├── archives/                      # 歸檔
└── ecosystem/                     # 生態系統
```

**總計**: 14 個根層目錄（從 35 減少到 14）

---

## governance/ 統一治理系統結構

### L0 Semantic Root（語義根層）
```
governance/
├── l0_semantic_root/
│   ├── README.md                  # 治理憲章
│   ├── ANCHOR.md                  # 治理錨點
│   └── CHARTER.yaml               # 治理契約
```

### L1 Governance Core（治理核心）
```
governance/
├── l1_governance_core/
│   ├── charter/                   # 治理憲章
│   │   ├── governance-charter.yaml
│   │   └── contracts.yaml
│   ├── ontology/                  # 本體模型
│   │   ├── naming_models.py       # 命名模型
│   │   ├── naming_patterns.py     # 命名模式
│   │   ├── naming_enforcer.py     # 命名強制執行器
│   │   └── semantic_tree.yaml     # 語義樹
│   └── registry/                  # 註冊表
│       ├── naming_registry.yaml   # 命名註冊表
│       ├── policies_registry.yaml # 策略註冊表
│       └── roles_registry.yaml    # 角色註冊表
```

### L2 Governance Domains（治理領域）
```
governance/
├── l2_domains/
│   ├── naming/                    # 命名治理
│   │   ├── semantic_rules/        # 語義規則
│   │   │   ├── gov-comment-naming.yaml
│   │   │   ├── gov-mapping-naming.yaml
│   │   │   ├── gov-reference-naming.yaml
│   │   │   ├── gov-path-naming.yaml
│   │   │   ├── gov-port-naming.yaml
│   │   │   ├── gov-service-naming.yaml
│   │   │   ├── gov-dependency-naming.yaml
│   │   │   ├── gov-short-naming.yaml
│   │   │   ├── gov-long-naming.yaml
│   │   │   ├── gov-directory-naming.yaml
│   │   │   ├── gov-file-naming.yaml
│   │   │   ├── gov-event-naming.yaml
│   │   │   ├── gov-variable-naming.yaml
│   │   │   ├── gov-env-var-naming.yaml
│   │   │   ├── gov-gitops-naming.yaml
│   │   │   └── gov-helm-naming.yaml
│   │   ├── enforcement/           # 強制執行
│   │   │   ├── gov_naming_check.py
│   │   │   ├── gov_auto_fix.py
│   │   │   └── gov_enforcer.py
│   │   ├── validation/            # 驗證
│   │   │   ├── test_naming_models.py
│   │   │   ├── test_naming_patterns.py
│   │   │   └── test_integration.py
│   │   └── reports/               # 報告
│   │       ├── naming_violations.json
│   │       ├── naming_metrics.json
│   │       └── audit_reports.json
│   ├── access_control/            # 訪問控制
│   │   ├── policies.yaml
│   │   ├── roles.yaml
│   │   └── permissions.yaml
│   ├── security/                  # 安全
│   │   ├── policies.yaml
│   │   ├── compliance.yaml
│   │   └── audits.yaml
│   └── lifecycle/                 # 生命週期
│       ├── creation.yaml
│       ├── update.yaml
│       └── deprecation.yaml
```

### L3 Governance Execution（治理執行）
```
governance/
├── l3_execution/
│   ├── boundaries/                # 邊界（整合 18 個 responsibility-* 目錄）
│   │   ├── gap-boundary/
│   │   ├── gates-boundary/
│   │   ├── gateway-boundary/
│   │   ├── gcp-boundary/
│   │   ├── generation-boundary/
│   │   ├── gl-layers-boundary/
│   │   ├── global-policy-boundary/
│   │   ├── governance-anchor-boundary/
│   │   ├── governance-execution-boundary/
│   │   ├── governance-sensing-boundary/
│   │   ├── governance-specs-boundary/
│   │   ├── group-boundary/
│   │   ├── guardrails-boundary/
│   │   ├── mnga-architecture-boundary/
│   │   ├── mno-operations-boundary/
│   │   ├── namespace-governance-boundary/
│   │   ├── observability-grafana-boundary/
│   │   └── quantum-stack-boundary/
│   ├── enforcement/               # 強制執行
│   │   ├── gov_enforce.py
│   │   ├── gov_validate.py
│   │   └── gov_audit.py
│   ├── migration/                 # 遷移
│   │   ├── gov_migrate.py
│   │   ├── gov_transform.py
│   │   └── migration_logs.yaml
│   └── audit/                     # 審計
│       ├── gov_audit_logger.py
│       ├── audit_trail.yaml
│       └── audit_reports.yaml
```

### L4 Governance Evidence（治理證據）
```
governance/
├── l4_evidence/
│   ├── reports/                   # 報告
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   ├── audits/                    # 審計
│   │   ├── compliance/
│   │   ├── security/
│   │   └── performance/
│   ├── metrics/                   # 指標
│   │   ├── naming_violations.json
│   │   ├── compliance_score.json
│   │   └── performance_metrics.json
│   └── archives/                  # 歸檔
│       ├── historical_reports/
│       └── retired_components/
```

---

## 命名規範遷移映射

### gl-* → gov-*
```
gl-evolution-data → gov-evolution-data
gl-gate → gov-gate
gl-artifacts → gov-artifacts
gl-hooks → gov-hooks
gl-restructure → gov-restructure
gl-engine → gov-engine
gl-core → gov-core
gl-governance → gov-governance
```

### gl.* → gov.*
```
gl.platform-assistant → gov.platform-assistant
gl.platform-ide → gov.platform-ide
gl.causal-reasoning-spec → gov.causal-reasoning-spec
gl.execution.finalization-spec → gov.execution.finalization-spec
```

### gl_* → gov_*
```
gl_governance_audit_engine → gov_governance_audit_engine
```

### GL_* → GOV_*
```
GL_EVENT_TEMPLATE → GOV_EVENT_TEMPLATE
```

### governance-* → gov-*
```
governance-audit → gov-audit
governance-legacy → gov-legacy
governance-enforcement-implementation-complete → gov-enforcement-implementation-complete
governance-enforcement-progress → gov-enforcement-progress
governance-enforcement-layer-todo → gov-enforcement-layer-todo
```

### gov_* → gov-*（統一為 kebab-case）
```
gov_policy → gov-policy
gov_contract → gov-contract
gov_evolution_engine → gov-evolution-engine
gov_pre_commit → gov-pre-commit
gov_naming_check → gov-naming-check
```

---

## 遷移路徑

### 第 1 步：整合 responsibility-* 目錄
```bash
# 移動所有 responsibility-* 目錄到 governance/l3_execution/boundaries/
for dir in responsibility-*-boundary/; do
    name=${dir#responsibility-}
    mv "$dir" "governance/l3_execution/boundaries/${name}"
done
```

### 第 2 步：整合 governance 相關目錄
```bash
# 整合 enterprise-governance
mv enterprise-governance governance/l2_domains/enterprise

# 整合 .governance
mv .governance governance/l1_governance_core/.internal
```

### 第 3 步：統一命名前綴
```bash
# 使用自動重命名工具
python3 refactor/tools/rename_prefixes.py
```

---

## 驗證標準

### 結構驗證
- [ ] 根層目錄數 = 14
- [ ] governance/ 目錄結構完整
- [ ] 所有 L0-L4 層級存在
- [ ] 18 個 responsibility-* 目錄已整合

### 命名驗證
- [ ] 所有 gl-* → gov-*
- [ ] 所有 gl.* → gov.*
- [ ] 所有 gl_* → gov_*
- [ ] 所有 GL_* → GOV_*
- [ ] 所有 governance-* → gov-*
- [ ] 所有 gov_* → gov-*

### 功能驗證
- [ ] 所有導入路徑正確
- [ ] 所有配置文件有效
- [ ] 所有測試通過
- [ ] CI/CD 管道正常

---

## 回滾計畫

如果需要回滾，執行以下步驟：

1. **恢復備份**
```bash
cd /workspace
tar -xzf indestructibleautoops_backup_20260209_131441.tar.gz
```

2. **恢復 Git 狀態**
```bash
cd indestructibleautoops
git checkout main
git branch -D refactor/governance-standardization
```

3. **驗證回滾**
```bash
# 檢查根層目錄數
ls -1 | wc -l  # 應該返回 35

# 檢查 responsibility-* 目錄
ls -1d responsibility-*-boundary | wc -l  # 應該返回 18
```

---

## 風險緩解

### 高風險緩解
1. **破壞性變更**
   - 提供兼容性層
   - 更新所有導入路徑
   - 提供遷移指南

2. **數據丟失**
   - 完整備份
   - 操作日誌
   - 回滾機制

### 中風險緩解
1. **命名衝突**
   - 使用命名空間
   - 前綴區分
   - 版本控制

2. **性能影響**
   - 增量檢查
   - 緩存機制
   - 異步處理

---

**文檔版本**: 1.0  
**最後更新**: 2026-02-09 13:16:31