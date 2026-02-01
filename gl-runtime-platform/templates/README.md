# GL Runtime Platform Kubernetes Templates

本目錄包含 GL Runtime Platform 的 Kubernetes 模板，遵循 GL 全域命名治理規範 v2.1.0。

## 目錄結構

```
templates/
├── README.md                           # 本文件
├── base/                               # 基礎模板
│   ├── namespace/                      # 命名空間模板
│   ├── deployments/                    # 部署模板
│   ├── services/                       # 服務模板
│   ├── configmaps/                     # 配置映射模板
│   ├── secrets/                        # 密鑰模板
│   ├── ingress/                        # 入口模板
│   └── rbac/                           # RBAC 模板
├── environments/                       # 環境特定模板
│   ├── dev/                            # 開發環境
│   ├── test/                           # 測試環境
│   ├── staging/                        # 預發布環境
│   └── prod/                           # 生產環境
├── policies/                           # 治理政策
│   ├── opa/                            # OPA 政策
│   └── kustomize/                      # Kustomize 配置
└── tools/                              # 工具腳本
    ├── validate-naming.sh              # 命名驗證腳本
    └── migrate-names.sh                # 名稱遷移腳本
```

## 命名規範

### 命名空間模式

- **開發環境**: `team-gl-runtime-dev-{region}`
- **測試環境**: `team-gl-runtime-test-{region}`
- **預發布環境**: `team-gl-runtime-staging-{region}`
- **生產環境**: `team-gl-runtime-prod-{region}`

### 資源命名模式

```
{service-name}-{component-type}-{version}
```

範例：
- 部署: `gl-execution-runtime-api-deploy-v1`
- 服務: `gl-execution-runtime-api-svc`
- 配置映射: `gl-execution-runtime-api-config`
- 入口: `gl-execution-runtime-ingress`

### 標籤標準

所有資源必須包含以下標籤：

```yaml
labels:
  # Kubernetes 標準標籤
  app.kubernetes.io/name: "{service-name}"
  app.kubernetes.io/component: "{component}"
  app.kubernetes.io/part-of: "gl-execution-runtime"
  app.kubernetes.io/version: "{version}"
  app.kubernetes.io/managed-by: "{tool}"
  
  # 企業治理標籤
  tenant: "gl-runtime-team"
  environment: "{environment}"
  cost-center: "platform-engineering"
  business-unit: "infrastructure"
  
  # 操作標籤（依需求）
  monitoring.tier: "{tier}"
  backup.tier: "{tier}"
```

## 使用方式

### 1. 基礎模板使用

```bash
# 應用基礎模板
kubectl apply -f base/namespace/
kubectl apply -f base/deployments/
kubectl apply -f base/services/
```

### 2. 環境特定部署

```bash
# 部署到開發環境
kubectl apply -k environments/dev/

# 部署到生產環境
kubectl apply -k environments/prod/
```

### 3. 命名驗證

```bash
# 驗證所有模板的命名規範
./tools/validate-naming.sh templates/
```

## 組件清單

### 核心服務

1. **GL Runtime Platform API** - 主要 API 服務
2. **REST API Service** - RESTful API 網關
3. **NLP Control Plane** - 自然語言控制平面
4. **Governance Service** - 治理服務
5. **Audit Service** - 審計服務

### 基礎設施

1. **PostgreSQL** - 關聯式數據庫
2. **Redis** - 緩存和事件流
3. **Prometheus** - 監控系統
4. **MinIO** - 對象存儲

## 治理政策

所有模板必須通過以下政策驗證：

- OPA Gatekeeper 政策
- 命名規範政策
- 標籤完整性政策
- 資源限制政策

## 版本控制

- 當前版本: v1.0.0
- 命名規範版本: v2.1.0
- GL Platform Universe: v1.0.0

## 聯繫方式

- **平台團隊**: platform-team@gl-runtime.io
- **DevOps 團隊**: devops@gl-runtime.io
- **文檔**: [EXTERNAL_URL_REMOVED]

## 變更日誌

### v1.0.0 (2024-01-31)
- 初始版本發布
- 對齊 GL 全域命名治理規範 v2.1.0
- 實施多環境模板架構
- 整合 OPA 政策驗證
- 添加 Kustomize 支持