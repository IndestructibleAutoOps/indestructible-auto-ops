# 根目錄清理計劃

## 待清理的治理相關腳本

### 1. GL Marker 相關腳本
- `add-gl-markers.py` - 添加 GL markers 的腳本
- `add-gl-markers-batch.py` - 批量添加 GL markers 的腳本
- `add-gl-markers-json.py` - JSON 格式的 GL markers 腳本
- `add-gl-markers-yaml.py` - YAML 格式的 GL markers 腳本
- `fix-governance-markers.py` - 修復治理 markers 的腳本

### 2. 審計相關腳本
- `gl-audit-simple.py` - 簡單 GL 審計腳本

### 3. 其他平台腳本
- `start-gl-platform.sh` - 啟動 GL 平台的腳本

## 建議遷移位置

### GL Markers 工具
→ `ecosystem/tools/gl-markers/`
- `add-gl-markers.py`
- `add-gl-markers-batch.py`
- `add-gl-markers-json.py`
- `add-gl-markers-yaml.py`
- `fix-governance-markers.py`

### 審計工具
→ `ecosystem/tools/audit/`
- `gl-audit-simple.py`

### 平台工具
→ `ecosystem/tools/platform/`
- `start-gl-platform.sh`

### 其他清理
- `gl-simple-audit-report.json` → `gl-governance-compliance/outputs/`
- `gl-validation-output.txt` → `gl-governance-compliance/outputs/`
- `gl-runtime-platform.zip` → `archives/`

## 執行計劃

```bash
# 創建目標目錄
mkdir -p ecosystem/tools/gl-markers
mkdir -p ecosystem/tools/audit
mkdir -p ecosystem/tools/platform
mkdir -p gl-governance-compliance/outputs
mkdir -p archives

# 移動 GL Markers 工具
mv add-gl-markers*.py ecosystem/tools/gl-markers/
mv fix-governance-markers.py ecosystem/tools/gl-markers/

# 移動審計工具
mv gl-audit-simple.py ecosystem/tools/audit/

# 移動平台工具
mv start-gl-platform.sh ecosystem/tools/platform/

# 移動輸出文件
mv gl-simple-audit-report.json gl-governance-compliance/outputs/
mv gl-validation-output.txt gl-governance-compliance/outputs/

# 移動歸檔文件
mv gl-runtime-platform.zip archives/
```
