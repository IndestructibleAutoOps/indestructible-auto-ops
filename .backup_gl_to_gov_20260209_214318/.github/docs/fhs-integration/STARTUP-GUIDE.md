<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# GL Unified Charter Activated
# FHS Integration System - Startup and Operation Guide
# FHS 整合系統啟動與運作指南

## 快速啟動

### 第一次使用

```bash
# 1. 初始化系統
cd /home/runner/work/mno-repository-understanding-system/mno-repository-understanding-system
./scripts/fhs-integration/init_fhs_integration.sh

# 2. 運行健康檢查
./scripts/fhs-integration/health_check.sh

# 3. 運行功能測試
python3 scripts/fhs-integration/operational_test.py
```

## 啟動步驟詳解

### 步驟 1: 系統初始化

初始化腳本會執行以下檢查：

1. **環境檢查**
   - 驗證 Python 3 是否安裝
   - 檢查必要的 Python 模組

2. **目錄結構驗證**
   - 確保 FHS 目錄存在 (bin/, sbin/, lib/, etc/)
   - 如果缺少會自動創建

3. **工具驗證**
   - 檢查所有 FHS 整合工具是否存在
   - 驗證 Python 文件語法
   - 設置正確的執行權限

4. **文檔驗證**
   - 確認文檔目錄和文件存在

5. **功能測試**
   - 測試每個組件的基本功能
   - 確保 --help 選項正常工作

6. **快速評估**
   - 對所有 workspace 組件進行評估
   - 生成評估摘要

**運行命令**：
```bash
./scripts/fhs-integration/init_fhs_integration.sh

# 只驗證不運行評估
./scripts/fhs-integration/init_fhs_integration.sh --verify-only
```

**預期輸出**：
```
=================================
FHS Integration System Initialization
=================================

[1/6] Environment Checks
✓ Python 3 found: 3.x.x

[2/6] Directory Structure Validation
✓ bin/
✓ sbin/
✓ lib/
✓ etc/
...

[6/6] Running Quick Assessment
✓ Assessment completed successfully

=================================
✓ Initialization Complete
=================================
```

### 步驟 2: 健康檢查

健康檢查腳本驗證系統各組件狀態：

**運行命令**：
```bash
./scripts/fhs-integration/health_check.sh
```

**檢查項目**：
- Python 3 可用性
- FHS 目錄存在性
- 所有工具文件存在
- 工具功能正常
- Git 倉庫狀態

**預期輸出**：
```
=================================
FHS Integration System Health Check
=================================

✓ Python 3 available
✓ bin/ directory exists
✓ sbin/ directory exists
...
✓ Automation leader runs

=================================
Summary:
  Passed: 14
  Failed: 0
✓ System Health: GOOD
=================================
```

### 步驟 3: 功能測試

完整的功能測試確保所有組件正常運作：

**運行命令**：
```bash
python3 scripts/fhs-integration/operational_test.py
```

**測試內容**：
1. 模組導入測試
2. 實例化測試
3. 成熟度評估測試
4. 驗證功能測試
5. 批量評估測試

**預期輸出**：
```
============================================================
FHS Integration System Operational Test
============================================================

[1/5] Module Import Tests
✓ Import MaturityAssessor
✓ Import FHSIntegrator
✓ Import FHSIntegrationValidator
✓ Import FHSAutomationMaster

[2/5] Instantiation Tests
✓ Create MaturityAssessor instance
✓ Create FHSIntegrator instance
✓ Create FHSIntegrationValidator instance

[3/5] Maturity Assessment Tests
✓ Assess fhs-integration component
✓ Assessment result structure valid

[4/5] Validation Tests
✓ Validation execution successful

[5/5] Batch Assessment Test
✓ Batch assessment successful
  └─ Assessed 23 components

============================================================
Test Summary:
  Passed: 12
  Failed: 0
✓ All tests passed - System fully operational
============================================================
```

## 日常運作

### 評估組件成熟度

```bash
# 評估單個組件
python3 workspace/tools/fhs-integration/maturity_assessor.py repository-understanding

# 評估所有組件
python3 workspace/tools/fhs-integration/fhs_automation_leader.py --assess-all

# JSON 格式輸出
python3 workspace/tools/fhs-integration/maturity_assessor.py repository-understanding --json
```

### 執行 FHS 整合

```bash
# 乾運行（推薦先運行）
python3 workspace/tools/fhs-integration/fhs_integrator.py repository-understanding

# 實際執行整合
python3 workspace/tools/fhs-integration/fhs_integrator.py repository-understanding --execute

# 指定成熟度分數
python3 workspace/tools/fhs-integration/fhs_integrator.py repository-understanding --maturity-score 85 --execute
```

### 運行驗證

```bash
# 獨立運行驗證器
python3 workspace/tools/fhs-integration/fhs_validator.py component-name

# 保存驗證報告
python3 workspace/tools/fhs-integration/fhs_validator.py component-name --save-report
```

## 定期維護

### 每日檢查

```bash
# 運行健康檢查
./scripts/fhs-integration/health_check.sh

# 如果失敗，運行功能測試定位問題
python3 scripts/fhs-integration/operational_test.py
```

### 每週評估

```bash
# 評估所有組件並保存報告
python3 workspace/tools/fhs-integration/fhs_automation_leader.py --assess-all --save-report
```

### 每月整合

```bash
# 檢查是否有組件達到整合標準 (80+ 分)
python3 workspace/tools/fhs-integration/fhs_automation_leader.py --assess-all | grep "READY FOR FHS INTEGRATION"

# 對達標組件進行整合（乾運行）
python3 workspace/tools/fhs-integration/fhs_automation_leader.py --auto-integrate

# 確認無誤後實際執行
python3 workspace/tools/fhs-integration/fhs_automation_leader.py --auto-integrate --execute
```

## 故障排除

### 問題: 初始化失敗

**解決方案**：
```bash
# 檢查 Python 版本
python3 --version

# 安裝依賴
pip install PyYAML

# 重新運行初始化
./scripts/fhs-integration/init_fhs_integration.sh
```

### 問題: 健康檢查失敗

**解決方案**：
```bash
# 查看詳細錯誤
./scripts/fhs-integration/health_check.sh 2>&1 | tee health_check.log

# 檢查特定組件
python3 workspace/tools/fhs-integration/maturity_assessor.py --help
```

### 問題: 功能測試失敗

**解決方案**：
```bash
# 查看詳細錯誤
python3 scripts/fhs-integration/operational_test.py 2>&1 | tee operational_test.log

# 手動測試每個組件
cd workspace/tools/fhs-integration
python3 -m py_compile maturity_assessor.py
python3 -m py_compile fhs_integrator.py
python3 -m py_compile fhs_validator.py
```

## 自動化設置

### Cron Job 設置

```bash
# 編輯 crontab
crontab -e

# 添加以下行：

# 每日健康檢查
0 9 * * * cd /home/runner/work/mno-repository-understanding-system/mno-repository-understanding-system && ./scripts/fhs-integration/health_check.sh

# 每週評估報告
0 10 * * 1 cd /home/runner/work/mno-repository-understanding-system/mno-repository-understanding-system && python3 workspace/tools/fhs-integration/fhs_automation_leader.py --assess-all --save-report
```

### GitHub Actions 設置

在 `.github/workflows/fhs-integration-check.yml` 中添加：

```yaml
name: FHS Integration System Check

on:
  schedule:
    - cron: '0 9 * * *'  # 每日運行
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Health Check
        run: ./scripts/fhs-integration/health_check.sh
      
      - name: Run Operational Test
        run: python3 scripts/fhs-integration/operational_test.py
      
      - name: Run Assessment
        run: python3 workspace/tools/fhs-integration/fhs_automation_leader.py --assess-all
```

## 總結

FHS 整合系統現在已完全初始化並可運作。遵循以下最佳實踐：

1. ✅ 每次使用前運行健康檢查
2. ✅ 先用乾運行測試整合
3. ✅ 查看驗證報告確保安全
4. ✅ 保持定期評估和維護
5. ✅ 記錄所有整合操作

系統已就緒，可以安全地進行 workspace → FHS 遷移！
