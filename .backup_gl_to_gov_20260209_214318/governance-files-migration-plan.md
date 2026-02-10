# GL 治理文件遷移計劃

## 問題分析

### 錯位文件清單

#### 1. 應該從根目錄移動的文件
- `governance-manifest.yaml` → `ecosystem/governance/`
- `governance-monitor-config.yaml` → `ecosystem/governance/`
- `init-governance.sh` → `ecosystem/governance/scripts/`
- `scripts/generate-governance-dashboard.py` → `ecosystem/tools/`

#### 2. 應該從 ecosystem/contracts/governance/ 移動的文件
- `GL_REVOLUTIONARY_AI_FRAMEWORK_ANALYSIS.md` → `ecosystem/docs/revolutionary-ai/`

#### 3. gov-evolution-data/ 目錄
- 應該從根目錄移至 `gov-governance-compliance/data/evolution/`

## 遷移策略

### 原則
1. **合約規範**：保留在 ecosystem/contracts/
2. **實現代碼**：保留在 gov-governance-compliance/
3. **文檔**：移至 ecosystem/docs/
4. **配置**：移至 ecosystem/governance/
5. **數據**：移至 gov-governance-compliance/data/

### 目標結構

```
ecosystem/
├── contracts/
│   ├── governance/           # 治理合約規範
│   ├── fact-verification/     # 事實驗證合約
│   └── verification/          # 驗證合約
├── docs/
│   └── revolutionary-ai/      # 革命性 AI 文檔
├── governance/               # 治理配置和腳本
│   ├── governance-manifest.yaml
│   ├── governance-monitor-config.yaml
│   └── scripts/
│       └── init-governance.sh
└── tools/
    └── generate-governance-dashboard.py

gov-governance-compliance/
├── data/                     # 數據目錄
│   └── evolution/            # 演化數據
├── contracts/                # 實現模塊
├── scripts/                  # 執行腳本
│   ├── naming/
│   └── evolution/
└── ... (其他標準目錄)
```

## 執行步驟

### Step 1: 創建目標目錄
```bash
mkdir -p ecosystem/docs/revolutionary-ai
mkdir -p ecosystem/governance/scripts
mkdir -p ecosystem/tools
mkdir -p gov-governance-compliance/data/evolution
```

### Step 2: 移動文檔
```bash
mv ecosystem/contracts/governance/GL_REVOLUTIONARY_AI_FRAMEWORK_ANALYSIS.md ecosystem/docs/revolutionary-ai/
```

### Step 3: 移動治理配置
```bash
mv governance-manifest.yaml ecosystem/governance/
mv governance-monitor-config.yaml ecosystem/governance/
mv init-governance.sh ecosystem/governance/scripts/
```

### Step 4: 移動工具
```bash
mv scripts/generate-governance-dashboard.py ecosystem/tools/
```

### Step 5: 移動演化數據
```bash
mv gov-evolution-data gov-governance-compliance/data/evolution
```

## 驗證檢查清單

- [ ] 所有合約文件仍在 ecosystem/contracts/
- [ ] 所有實現代碼仍在 gov-governance-compliance/
- [ ] 所有文檔在 ecosystem/docs/
- [ ] 所有配置在 ecosystem/governance/
- [ ] 所有數據在 gov-governance-compliance/data/
- [ ] 根目錄不再有治理相關文件
- [ ] Git 狀態正確