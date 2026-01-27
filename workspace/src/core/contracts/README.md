# External API Contracts

# 外部 API 合約定義

<!-- GL Layer: GL30-49 Execution Layer -->
<!-- Purpose: Contract specifications and schema definitions -->

> 外部 API 合約規格定義，包含 OpenAPI specs 和 JSON Schema。
> External API contract specifications, including OpenAPI specs and JSON Schema.

## 📋 Overview 概述

本目錄包含 MachineNativeOps 平台的外部 API 合約定義。這些是純資料/規格文件，不包含任何實作代碼。

**⚠️ 重要區分 Important Distinction:**

| 目錄 Directory | 內容 Content | 說明 Description |
|----------------|--------------|------------------|
| `contracts/` (本目錄) | 合約定義資料 | 外部 API 合約**規格定義** (純 Schema/Spec) |
| `core/contract_service/` | 微服務程式碼 | 合約管理服務的**實作代碼** (L1 Service) |

This directory contains external API contract definitions for the MachineNativeOps platform. These are pure data/specification files without any implementation code.

## 📁 Directory Structure 目錄結構

```
contracts/
├── external/            # 外部整合合約
└── external-api.json    # 外部 API 合約定義
```

## 🎯 What This Directory Does 本目錄負責什麼

### ✅ Responsibilities 職責 (GL30-49: Schema Definition)

1. **API Contract Definitions API 合約定義**
   - 外部系統 API 規格
   - OpenAPI/Swagger 文件
   - JSON Schema 定義

2. **Interface Specifications 介面規格**
   - 請求/回應格式定義
   - 驗證規則
   - 資料結構定義

### ❌ What This Directory Does NOT Do 本目錄不負責什麼

- **不包含任何實作代碼** - 實作在 `core/contract_service/` (GL30-49: Automation Script)
- **不包含合約管理服務** - 使用 `core/contract_service/`
- **不包含 L1 服務代碼** - L1 實作已整合到 `core/contract_service/contracts-L1/`
- **不包含運行時邏輯** - 這是純資料/規格

## 📦 Contents 內容

### external-api.json

外部 API 合約定義，用於：

- 與外部系統整合時的介面規格
- API 驗證和測試
- 文檔生成

## 🔗 Dependencies 依賴關係

### ✅ Who Should Depend on This 誰應該依賴本目錄

| Consumer 使用者 | Purpose 用途 |
|----------------|--------------|
| `bridges/` | 跨語言整合時參考合約 |
| `core/unified_integration/` | 整合外部系統時使用 |
| `tests/` | API 測試驗證 |

### ❌ This Directory Should NOT Depend on 本目錄不應依賴

| 不應依賴 | Reason 原因 |
|---------|-------------|
| 任何實作代碼 | 合約定義應獨立於實作 |
| `core/contract_service/` | 規格不應依賴服務實作 |

## 🚀 Usage 使用方式

### Validating Against Contract 根據合約驗證

```javascript
import Ajv from 'ajv';
import contractSchema from './contracts/external-api.json';

const ajv = new Ajv();
const validate = ajv.compile(contractSchema);

const isValid = validate(apiResponse);
if (!isValid) {
  console.error('Contract validation failed:', validate.errors);
}
```

### Generating Documentation 生成文檔

```bash
# 使用 OpenAPI Generator
npx openapi-generator-cli generate \
  -i contracts/external-api.json \
  -g markdown \
  -o docs/api
```

## 🔄 Consolidation Note 整合說明

**日期**: 2026-01-19  
**變更**: 移除重複的 contracts-L1 實作代碼

原先 `contracts/contracts-L1/` 目錄包含完整的服務實作代碼（2.3MB），與 `contract_service/contracts-L1/` 重複。
根據 machine-native 原則（單一來源、minimal diff），已移除重複實作，保留唯一規範來源：

- **保留**: `core/contract_service/contracts-L1/` (canonical implementation)
- **移除**: `core/contracts/contracts-L1/` (duplicate removed)
- **保留**: `core/contracts/external-api.json` and `external/` (contract specs)

## 📖 Related Documentation 相關文檔

- [Architecture Layers](./docs/architecture/layers.md) - 架構分層視圖
- [Repository Map](./docs/architecture/repo-map.md) - 倉庫語義邊界
- [Contract Service](./core/contract_service/README.md) - 合約管理服務
- [Integration Guide](./docs/INTEGRATION_GUIDE.md) - 整合指南

## 📝 Document History 文檔歷史

| Date 日期 | Version 版本 | Changes 變更 |
|-----------|-------------|--------------|
| 2025-11-30 | 1.0.0 | Initial README with boundary definitions |

---

**Owner 負責人**: Integration Team  
**Last Updated 最後更新**: 2025-11-30
