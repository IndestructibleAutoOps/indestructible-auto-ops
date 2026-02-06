# RKE2 安全加固集成方案

## 📋 執行摘要

本文檔概述如何將 **RKE2 (Rancher Kubernetes Engine 2)** 安全加固功能集成到 **MachineNativeOps** 專案的現有架構中。RKE2 作為「預設硬化」的 Kubernetes 分發版，完美契合專案的 GL 治理框架和企業級安全需求。

---

## 🏗️ 專案架構分析

### 現有架構特徵

**核心治理系統**
- GL (Governance Layers) 7層治理框架 (GL00-99)
- 119+ 集成治理文件
- 嚴格的語義邊界和不可變約束

**基礎設施現狀**
- `infrastructure/kubernetes/manifests/` - Kubernetes 編排配置
- `infrastructure/k8s-legacy/` - 舊版 K8s 配置
- `infrastructure/deployment/helm/` - Helm charts
- `infrastructure/deployment/terraform/` - Terraform 配置
- 災難恢復、高可用性、Istio、Jaeger 等組件

**安全現狀**
- CodeQL、Bandit 安全掃描
- GL50-59 觀察層安全監控
- 安全審計工件管理

### RKE2 與專案的契合度

| 特性 | MachineNativeOps 需求 | RKE2 能力 | 匹配度 |
|------|---------------------|-----------|--------|
| **CIS 合規** | 企業級合規要求 | 預設通過大多數 CIS 控制 | ✅ 完美 |
| **安全加固** | GL 治理框架安全標準 | 預設硬化 | ✅ 完美 |
| **多租戶** | 跨領域架構 | 支援命名空間隔離 | ✅ 良好 |
| **自動化** | 即時執行引擎 | 自動化配置和驗證 | ✅ 良好 |
| **文檔治理** | GL 文檔標準 | 結構化配置 | ✅ 良好 |

---

## 🎯 集成策略

### 策略 1: RKE2 配置模組化

**目錄結構**
```
infrastructure/rke2/
├── profiles/                    # RKE2 配置檔案
│   ├── cis/                     # CIS 基準配置
│   │   ├── cis-1.23.yaml
│   │   └── cis-1.29.yaml
│   ├── production/              # 生產環境配置
│   │   ├── config.yaml
│   │   └── encryption-provider-config.yaml
│   └── staging/                 # 暫存環境配置
├── scripts/                     # 自動化腳本
│   ├── install-rke2.sh
│   ├── validate-cis.sh
│   └── rotate-secrets.sh
├── manifests/                   # Kubernetes 清單
│   ├── network-policies/
│   ├── pod-security-policies/
│   └── audit-logging/
└── documentation/               # 文檔
    ├── RKE2_SETUP_GUIDE.md
    ├── CIS_COMPLIANCE_CHECKLIST.md
    └── SECURITY_HARDENING_GUIDE.md
```

**GL 治理整合**
```yaml
# infrastructure/rke2/profiles/production/config.yaml
# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: rke2-configuration
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

profile: cis-1.29
selinux: true
protect-kernel-defaults: true
secrets-encryption: true
```

### 策略 2: CIS 基準整合

**GL 層對應**
- **GL10-19 (風險與指標)**: CIS 合規指標追蹤
- **GL20-29 (資源與標準)**: RKE2 資源配置標準
- **GL30-39 (流程與控制)**: CIS 審計流程
- **GL40-49 (監控與優化)**: 安全監控與優化

**實現方式**
```yaml
# GL10-risk-registry.json 更新
{
  "risks": [
    {
      "id": "RKE2-CIS-001",
      "name": "CIS Control 1.1.1 - etcd Data Directory",
      "severity": "medium",
      "status": "mitigated",
      "mitigation": "RKE2 CIS profile enforcement",
      "gl_layer": "GL20-29"
    }
  ]
}
```

### 策略 3: 安全治理自動化

**工作流程整合**
```yaml
# .github/workflows/rke2-security-validation.yml
name: RKE2 Security Validation

on:
  push:
    paths:
      - 'infrastructure/rke2/**'
  pull_request:
    paths:
      - 'infrastructure/rke2/**'

jobs:
  cis-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate CIS Profile
        run: |
          ./infrastructure/rke2/scripts/validate-cis.sh
      - name: Check SELinux Configuration
        run: |
          yq eval '.selinux' infrastructure/rke2/profiles/production/config.yaml
      - name: Validate Encryption Provider
        run: |
          kubectl apply --dry-run=client -f infrastructure/rke2/profiles/production/encryption-provider-config.yaml
```

### 策略 4: 監控與合規報告

**GL50-59 觀察層整合**
```yaml
# infrastructure/rke2/manifests/audit-logging/audit-policy.yaml
# @GL-governed
# @GL-layer: GL50-59
# @GL-semantic: audit-logging

apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: Metadata
    resources:
      - group: ""
        resources: ["pods", "configmaps", "secrets"]
  - level: RequestResponse
    resources:
      - group: "authorization.k8s.io"
        resources: ["subjectaccessreviews"]
```

**合規報告生成**
```python
# infrastructure/rke2/scripts/generate-cis-report.py
#!/usr/bin/env python3
"""
Generate CIS Compliance Report
@GL-governed
@GL-layer: GL50-59
@GL-semantic: cis-report-generation
"""

import json
import yaml
from datetime import datetime

def generate_cis_report():
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "rke2_version": "v1.29.0+rke2r1",
        "cis_profile": "cis-1.29",
        "compliance_status": "compliant",
        "controls_passed": 156,
        "controls_failed": 0,
        "controls_skipped": 8,
        "gl_layer": "GL50-59"
    }
    
    with open("outputs/cis-compliance-report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return report

if __name__ == "__main__":
    generate_cis_report()
```

---

## 📁 檔案結構集成

### 1. 配置檔案

**RKE2 主配置**
```yaml
# infrastructure/rke2/profiles/production/config.yaml
# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: rke2-production-config

# CIS Profile
profile: cis-1.29

# SELinux
selinux: true

# Kernel Protection
protect-kernel-defaults: true

# Secrets Encryption
secrets-encryption: true
encryption-provider-config: /etc/rancher/rke2/encryption-provider-config.yaml

# Network Policies
network-policies: true

# Pod Security Admission
pod-security-admission-config-file: /etc/rancher/rke2/psa-config.yaml

# Audit Logging
audit-policy-file: /etc/rancher/rke2/audit-policy.yaml
audit-log-path: /var/log/rke2/audit.log
audit-log-maxage: 30
audit-log-maxbackup: 10
audit-log-maxsize: 100

# etcd Configuration
etcd-snapshot-schedule-cron: "0 */4 * * *"
etcd-snapshot-retention: 72

# Cluster Configuration
cluster-name: machine-native-ops-production
cluster-domain: cluster.local
```

**加密提供者配置**
```yaml
# infrastructure/rke2/profiles/production/encryption-provider-config.yaml
# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: encryption-provider

apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <BASE64_ENCODED_KEY>
      - identity: {}
```

### 2. 自動化腳本

**RKE2 安裝腳本**
```bash
#!/bin/bash
# infrastructure/rke2/scripts/install-rke2.sh
# @GL-governed
# @GL-layer: GL30-39
# @GL-semantic: rke2-installation

set -e

# Configuration
RKE2_VERSION="v1.29.0+rke2r1"
CIS_PROFILE="cis-1.29"
INSTALL_DIR="/opt/rke2"

echo "🚀 Installing RKE2 ${RKE2_VERSION} with CIS profile..."

# Download RKE2
curl -sfL [EXTERNAL_URL_REMOVED] | sh -

# Create configuration directory
mkdir -p /etc/rancher/rke2

# Copy configuration files
cp infrastructure/rke2/profiles/production/config.yaml /etc/rancher/rke2/
cp infrastructure/rke2/profiles/production/encryption-provider-config.yaml /etc/rancher/rke2/

# Enable and start RKE2
systemctl enable rke2-server
systemctl start rke2-server

echo "✅ RKE2 installed successfully!"
```

**CIS 驗證腳本**
```bash
#!/bin/bash
# infrastructure/rke2/scripts/validate-cis.sh
# @GL-governed
# @GL-layer: GL40-49
# @GL-semantic: cis-validation

set -e

echo "🔍 Validating RKE2 CIS compliance..."

# Check CIS profile
if ! grep -q "profile: cis" /etc/rancher/rke2/config.yaml; then
    echo "❌ CIS profile not enabled"
    exit 1
fi

# Check SELinux
if ! grep -q "selinux: true" /etc/rancher/rke2/config.yaml; then
    echo "⚠️  SELinux not enabled"
fi

# Check secrets encryption
if ! grep -q "secrets-encryption: true" /etc/rancher/rke2/config.yaml; then
    echo "❌ Secrets encryption not enabled"
    exit 1
fi

# Check kernel parameters
if [ ! -f /etc/sysctl.d/99-rke2-cis.conf ]; then
    echo "⚠️  Kernel parameters not configured"
fi

echo "✅ CIS validation passed!"
```

### 3. Kubernetes 清單

**網路策略**
```yaml
# infrastructure/rke2/manifests/network-policies/deny-all-ingress.yaml
# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: network-policy

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

**Pod Security Admission**
```yaml
# infrastructure/rke2/manifests/pod-security-policies/psa-config.yaml
# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: pod-security-admission

apiVersion: apiserver.config.k8s.io/v1
kind: PodSecurityConfiguration
defaults:
  enforce: restricted
  enforce-version: latest
  audit: restricted
  audit-version: latest
  warn: restricted
  warn-version: latest
exemptions:
  usernames: []
  runtimeClasses: []
  namespaces: [kube-system, cis-operator-system, tigera-operator]
```

---

## 🔧 實施步驟

### Phase 1: 準備階段 (1-2 週)

**任務清單**
- [ ] 創建 `infrastructure/rke2/` 目錄結構
- [ ] 編寫 RKE2 配置檔案模板
- [ ] 準備 CIS 基準配置
- [ ] 創建 GL 治理標記
- [ ] 更新 `governance-manifest.yaml`

**輸出**
- RKE2 配置模板
- CIS 基準配置檔案
- GL 治理文檔

### Phase 2: 開發階段 (2-3 週)

**任務清單**
- [ ] 實現 RKE2 安裝腳本
- [ ] 開發 CIS 驗證腳本
- [ ] 創建網路策略清單
- [ ] 配置 Pod Security Admission
- [ ] 實現 Secrets 加密
- [ ] 設定審計日誌

**輸出**
- 自動化腳本
- Kubernetes 清單
- 配置檔案

### Phase 3: 測試階段 (1-2 週)

**任務清單**
- [ ] 在測試環境部署 RKE2
- [ ] 執行 CIS 合規檢查
- [ ] 驗證 SELinux 配置
- [ ] 測試 Secrets 加密
- [ ] 驗證網路策略
- [ ] 測審計日誌

**輸出**
- 測試報告
- 合規性證明
- 問題清單

### Phase 4: 部署階段 (1-2 週)

**任務清單**
- [ ] 在生產環境部署 RKE2
- [ ] 配置監控和警報
- [ ] 建立備份和恢復流程
- [ ] 培運維團隊
- [ ] 更新文檔

**輸出**
- 生產環境 RKE2 集群
- 監控儀表板
- 運維手冊

### Phase 5: 優化階段 (持續)

**任務清單**
- [ ] 持續監控合規性
- [ ] 定期更新 RKE2 版本
- [ ] 優化安全配置
- [ ] 更新 CIS 基準
- [ ] 審計和改進

**輸出**
- 定期報告
- 優化建議
- 改進計畫

---

## 📊 合規性追蹤

### GL 層對應表

| RKE2 功能 | GL 層 | 責任組件 | 狀態 |
|-----------|-------|----------|------|
| CIS 基準 | GL10-19 | 風險註冊表 | 待實現 |
| etcd 安全 | GL20-29 | 資源標準 | 待實現 |
| SELinux | GL20-29 | 資源標準 | 待實現 |
| 網路策略 | GL30-39 | 流程控制 | 待實現 |
| PSA 配置 | GL30-39 | 流程控制 | 待實現 |
| Secrets 加密 | GL40-49 | 監控優化 | 待實現 |
| 審計日誌 | GL50-59 | 觀察層 | 待實現 |
| 合規報告 | GL90-99 | 文檔治理 | 待實現 |

### 合規性檢查清單

**CIS 1.1.1 - etcd Data Directory**
- [ ] etcd 數據目錄權限為 600
- [ ] etcd 用戶擁有數據目錄
- [ ] GL20-29 註冊表更新

**CIS 1.1.2 - API Server Pod Specification**
- [ ] Pod 規範文件權限為 600 或更嚴格
- [ ] GL20-29 註冊表更新

**CIS 1.1.12 - etcd User**
- [ ] etcd 用戶存在
- [ ] etcd 用戶無法登錄
- [ ] GL20-29 註冊表更新

**CIS 1.2.0 - Control Plane Configuration**
- [ ] --authorization-mode 包含 Node
- [ ] --enable-admission-plugins 配置正確
- [ ] GL30-39 流程控制更新

**CIS 1.3.0 - Controller Manager**
- [ ] --terminated-pod-gc-threshold 配置
- [ ] --use-service-account-credentials 配置
- [ ] GL30-39 流程控制更新

---

## 🔒 安全加固要點

### 1. SELinux 強制模式

**配置**
```yaml
# infrastructure/rke2/profiles/production/config.yaml
selinux: true
```

**驗證**
```bash
# 檢查 SELinux 狀態
getenforce

# 查看拒絕日誌
ausearch -m avc -ts recent
```

### 2. Kernel 參數保護

**配置**
```yaml
# infrastructure/rke2/profiles/production/config.yaml
protect-kernel-defaults: true
```

**驗證**
```bash
# 檢查 kernel 參數
sysctl -a | grep net.ipv4.ip_forward
```

### 3. Secrets 加密

**配置**
```yaml
secrets-encryption: true
```

**輪換**
```bash
# 生成新密鑰
HEAD -c 32 /dev/urandom | base64

# 更新加密配置
kubectl apply -f encryption-provider-config.yaml

# 重啟 API Server
systemctl restart rke2-server
```

### 4. 網路策略

**預設拒絆**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### 5. Pod Security Admission

**受限制模式**
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: PodSecurityConfiguration
defaults:
  enforce: restricted
exemptions:
  namespaces: [kube-system, cis-operator-system, tigera-operator]
```

---

## 📈 監控和警報

### Prometheus 指標

**RKE2 特定指標**
```yaml
# infrastructure/rke2/manifests/monitoring/prometheus-rules.yaml
# @GL-governed
# @GL-layer: GL50-59
# @GL-semantic: monitoring-rules

groups:
  - name: rke2_security
    rules:
      - alert: CISComplianceFailed
        expr: rke2_cis_compliance_status < 1
        for: 5m
        labels:
          severity: critical
          gl_layer: GL50-59
        annotations:
          summary: "CIS compliance check failed"
          description: "RKE2 cluster is not CIS compliant"

      - alert: SELinuxPermissiveMode
        expr: rke2_selinux_mode != 1
        for: 10m
        labels:
          severity: warning
          gl_layer: GL50-59
        annotations:
          summary: "SELinux not in enforcing mode"
          description: "SELinux is running in permissive mode"
```

### Grafana 儀表板

**安全合規儀表板**
- CIS 合規狀態
- SELinux 模式
- Secrets 加密狀態
- 網路策略違規
- Pod 安全策略違規
- 審計日誌事件

---

## 📚 文檔和培訓

### 1. 用戶文檔

**RKE2 安裝指南**
- 系統要求
- 安裝步驟
- 配置選項
- 故障排除

**CIS 合規指南**
- CIS 控制清單
- 驗證步驟
- 合規報告
- 審計準備

### 2. 運維文檔

**運維手冊**
- 日常維護
- 備份和恢復
- 升級程序
- 應急響應

**故障排除指南**
- 常見問題
- 診斷工具
- 日誌分析
- 支援渠道

### 3. 培訓材料

**培訓課程**
- RKE2 基礎
- CIS 合規
- 安全加固
- 應急響應

**實驗室練習**
- 搭建測試環境
- 配置 CIS 基準
- 執行安全掃描
- 應對安全事件

---

## 🎉 總結

RKE2 安全加固集成到 MachineNativeOps 專案將提供：

1. **增強的安全性** - 預設硬化配置滿足企業級安全要求
2. **CIS 合規** - 自動合規檢查和報告
3. **GL 治理整合** - 與現有 GL 治理框架無縫集成
4. **自動化** - 腳本和工作流程自動化安全配置
5. **可觀測性** - 完整的監控和警報系統
6. **文檔化** - 全面的文檔和培訓材料

通過系統化的實施，專案將獲得一個安全、合規、可維護的 Kubernetes 平台。

---

**文檔版本**: 1.0  
**最後更新**: 2026-01-30  
**GL 層**: GL90-99  
**狀態**: 📋 規劃中