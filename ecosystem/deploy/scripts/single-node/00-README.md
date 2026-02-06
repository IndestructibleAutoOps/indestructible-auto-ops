# 單節點環境部署腳本

## 目錄結構

```
single-node/
├── 00_README.md                    # 本文件
├── 01_pre_install_check.sh         # 安裝前置檢查
├── 02_install_k3s.sh              # k3s 安裝腳本
├── 03_deploy_gl_backend.sh        # GL-Native Backend 部署
├── 04_health_check.sh             # 健康檢查腳本
├── 05_uninstall.sh                # 卸載腳本
├── configs/                       # 配置檔案
│   ├── k3s-config.yaml           # k3s 配置
│   └── gl-backend-config.yaml    # GL Backend 配置
└── manifests/                     # K8s manifests
    ├── namespace.yaml
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

## 使用方式

### 完整部署流程

```bash
# 1. 前置檢查
./01_pre_install_check.sh

# 2. 安裝 k3s
./02_install_k3s.sh

# 3. 部署 GL-Native Backend
./03_deploy_gl_backend.sh

# 4. 健康檢查
./04_health_check.sh
```

### 單獨執行

每個腳本都可以單獨執行，但建議按順序執行。

## 系統要求

- OS: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+
- CPU: 最少 2 cores
- RAM: 最少 4 GB (推薦 8 GB)
- Storage: 最少 50 GB (推薦 100 GB)
- Network: 標準以太網連接

## 變數配置

所有腳本使用環境變數配置，可在執行前設置：

```bash
export K3S_VERSION="v1.28.3+k3s2"
export GL_BACKEND_VERSION="v1.1"
export NAMESPACE="gl-native"
export STORAGE_PATH="/opt/gl-native/data"
```

## 故障排除

如果部署失敗，請查看日誌：

```bash
# k3s 日誌
sudo journalctl -u k3s -f

# GL Backend 日誌
kubectl logs -n gl-native -l app=gl-backend

# 健康檢查
./04_health_check.sh --verbose
```