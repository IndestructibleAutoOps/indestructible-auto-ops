# 結構重建遷移策略

## 當前狀態
- 已創建新的8層GL架構目錄
- 舊目錄：gov-platform, gov-runtime-platform, gov-semantic-core-platform
- 業務系統目錄：elasticsearch-search-system, file-organizer-system, esync-platform, quantum-platform

## 遷移策略

### 1. 治理文件遷移（gov-platform → gov-enterprise-architecture）
```bash
# 遷移治理內容到新架構
mv gov-platform/governance gov-enterprise-architecture/
mv gov-platform/governance gov-meta-specifications/
```

### 2. 平台遷移到 gov-platform-services
- gov-runtime-platform → gov-platform-services/runtime/
- gov-semantic-core-platform → gov-platform-services/semantic/

### 3. 業務系統分類
根據GL層分配業務系統：
- elasticsearch-search-system → gov-data-processing/
- file-organizer-system → gov-execution-runtime/
- observability → gov-observability/
- infrastructure → infrastructure/

### 4. 配置和文檔
- config/ → gov-enterprise-architecture/configs/
- docs/ → docs/
- scripts/ → scripts/
- deploy/ → gov-governance-compliance/deployments/

## 執行步驟
1. 備份當前結構
2. 遷移治理文件
3. 遷移平台服務
4. 遷移業務系統
5. 遷移配置文檔
6. 驗證結果
7. 提交變更