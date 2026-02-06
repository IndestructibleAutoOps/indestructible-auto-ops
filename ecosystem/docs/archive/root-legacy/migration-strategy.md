# 結構重建遷移策略

## 當前狀態
- 已創建新的8層GL架構目錄
- 舊目錄：gl-platform, gl-runtime-platform, gl-semantic-core-platform
- 業務系統目錄：elasticsearch-search-system, file-organizer-system, esync-platform, quantum-platform

## 遷移策略

### 1. 治理文件遷移（gl-platform → gl-enterprise-architecture）
```bash
# 遷移治理內容到新架構
mv gl-platform/governance gl-enterprise-architecture/
mv gl-platform/governance gl-meta-specifications/
```

### 2. 平台遷移到 gl-platform-services
- gl-runtime-platform → gl-platform-services/runtime/
- gl-semantic-core-platform → gl-platform-services/semantic/

### 3. 業務系統分類
根據GL層分配業務系統：
- elasticsearch-search-system → gl-data-processing/
- file-organizer-system → gl-execution-runtime/
- observability → gl-observability/
- infrastructure → infrastructure/

### 4. 配置和文檔
- config/ → gl-enterprise-architecture/configs/
- docs/ → docs/
- scripts/ → scripts/
- deploy/ → gl-governance-compliance/deployments/

## 執行步驟
1. 備份當前結構
2. 遷移治理文件
3. 遷移平台服務
4. 遷移業務系統
5. 遷移配置文檔
6. 驗證結果
7. 提交變更