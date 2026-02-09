# 根目錄清理計劃

## 待清理的治理相關腳本

### 1. GL Marker 相關腳本
- `add-gov-markers.py` - 添加 GL markers 的腳本
- `add-gov-markers-batch.py` - 批量添加 GL markers 的腳本
- `add-gov-markers-json.py` - JSON 格式的 GL markers 腳本
- `add-gov-markers-yaml.py` - YAML 格式的 GL markers 腳本
- `fix-governance-markers.py` - 修復治理 markers 的腳本

### 2. 審計相關腳本
- `gov-audit-simple.py` - 簡單 GL 審計腳本

### 3. 其他平台腳本
- `start-gov-platform.sh` - 啟動 GL 平台的腳本

## 建議遷移位置

### GL Markers 工具
→ `ecosystem/tools/gov-markers/`
- `add-gov-markers.py`
- `add-gov-markers-batch.py`
- `add-gov-markers-json.py`
- `add-gov-markers-yaml.py`
- `fix-governance-markers.py`

### 審計工具
→ `ecosystem/tools/audit/`
- `gov-audit-simple.py`

### 平台工具
→ `ecosystem/tools/platform/`
- `start-gov-platform.sh`

### 其他清理
- `gov-simple-audit-report.json` → `gov-governance-compliance/outputs/`
- `gov-validation-output.txt` → `gov-governance-compliance/outputs/`
- `gov-runtime-platform.zip` → `archives/`

## 執行計劃

```bash
# 創建目標目錄
mkdir -p ecosystem/tools/gov-markers
mkdir -p ecosystem/tools/audit
mkdir -p ecosystem/tools/platform
mkdir -p gov-governance-compliance/outputs
mkdir -p archives

# 移動 GL Markers 工具
mv add-gov-markers*.py ecosystem/tools/gov-markers/
mv fix-governance-markers.py ecosystem/tools/gov-markers/

# 移動審計工具
mv gov-audit-simple.py ecosystem/tools/audit/

# 移動平台工具
mv start-gov-platform.sh ecosystem/tools/platform/

# 移動輸出文件
mv gov-simple-audit-report.json gov-governance-compliance/outputs/
mv gov-validation-output.txt gov-governance-compliance/outputs/

# 移動歸檔文件
mv gov-runtime-platform.zip archives/
```
