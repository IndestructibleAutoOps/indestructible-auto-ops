# 叢集環境部署腳本

## 目錄結構

```
cluster/
├── 00_README.md                           # 本文件
├── 01_pre_install_check.sh                # 前置檢查腳本
├── 02_init_control_plane.sh               # 控制平面初始化腳本
├── 03_join_worker_node.sh                 # Worker 節點加入腳本
├── 04_install_cni.sh                      # CNI 安裝腳本
├── 05_deploy_gl_backend.sh                # GL-Native Backend 部署
├── 06_health_check.sh                     # 健康檢查腳本
├── 07_remove_node.sh                      # 移除節點腳本
├── configs/                               # 配置檔案
│   ├── k3s-server.yaml                   # 控制平面配置
│   ├── k3s-agent.yaml                    # Worker 節點配置
│   └── cluster-config.yaml               # 叢集配置
└── manifests/                             # K8s manifests
    ├── loadbalancer.yaml
    ├── namespace.yaml
    ├── deployment.yaml
    └── service.yaml
```

## 叢集架構

```
                    Load Balancer (HAProxy + Keepalived)
                            VIP: 192.168.1.100
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │ Control-1 │    │ Control-2 │    │ Control-3 │
    │ 192.168.1.11│   │ 192.168.1.12│   │ 192.168.1.13│
    │ (Server)  │    │ (Server)  │    │ (Server)  │
    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │  Worker-1 │    │  Worker-2 │    │  Worker-3 │
    │ 192.168.1.21│   │ 192.168.1.22│   │ 192.168.1.23│
    │  (Agent)  │    │  (Agent)  │    │  (Agent)  │
    └───────────┘    └───────────┘    └───────────┘
```

## 使用方式

### 初始化控制平面

```bash
# 在第一個控制平面節點上執行
sudo ./01_pre_install_check.sh
sudo ./02_init_control_plane.sh --role first-server
```

### 添加額外控制平面節點

```bash
# 在第二和第三個控制平面節點上執行
sudo ./01_pre_install_check.sh
sudo ./02_init_control_plane.sh --role additional-server --server-url https://192.168.1.11:6443 --token <token>
```

### 添加 Worker 節點

```bash
# 在 Worker 節點上執行
sudo ./01_pre_install_check.sh
sudo ./03_join_worker_node.sh --server-url https://192.168.1.11:6443 --token <token>
```

### 安裝 CNI

```bash
# 在任意控制平面節點上執行一次
./04_install_cni.sh --plugin calico
```

### 部署 GL-Native Backend

```bash
# 在任意控制平面節點上執行
./05_deploy_gl_backend.sh
```

### 健康檢查

```bash
# 在任意控制平面節點上執行
./06_health_check.sh
```

## 系統要求

### 控制平面節點 (3 個)
- OS: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+
- CPU: 4 cores
- RAM: 8 GB
- Storage: 100 GB SSD
- Network: 低延遲網路連接

### Worker 節點 (2-N 個)
- OS: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+
- CPU: 8+ cores
- RAM: 16+ GB
- Storage: 200+ GB SSD
- Network: 低延遲網路連接

## 網路配置

### 必須開放的端口

**控制平面節點:**
- 6443: Kubernetes API Server
- 10250: Kubelet API
- 8472: Flannel VXLAN (如使用 Flannel)
- 179: Calico BGP (如使用 Calico)

**Worker 節點:**
- 10250: Kubelet API
- 8472: Flannel VXLAN (如使用 Flannel)
- 179: Calico BGP (如使用 Calico)

**Load Balancer:**
- 6443: 轉發到控制平面節點

### 網路配置要求

- 節點間網路延遲: < 5ms
- 節點間網路帶寬: ≥ 1 Gbps
- Pod CIDR: 10.42.0.0/16 (可配置)
- Service CIDR: 10.43.0.0/16 (可配置)

## 負載均衡配置

### HAProxy 配置

參見 `configs/haproxy.cfg`

### Keepalived 配置

參見 `configs/keepalived.conf`

## 變數配置

所有腳本使用環境變數配置：

```bash
# k3s 配置
export K3S_VERSION="v1.28.3+k3s2"
export CLUSTER_CIDR="10.42.0.0/16"
export SERVICE_CIDR="10.43.0.0/16"

# 節點配置
export CONTROL_PLANE_IPS="192.168.1.11,192.168.1.12,192.168.1.13"
export WORKER_IPS="192.168.1.21,192.168.1.22,192.168.1.23"

# GL-Native 配置
export NAMESPACE="gl-native"
export BACKEND_VERSION="v1.1"
```

## 高可用性配置

### 控制平面 HA
- 3 個控制平面節點
- 負載均衡器 + VIP
- etcd quorum (可容忍 1 個節點故障)

### Worker 節點 HA
- 多個 Worker 節點
- Pod 反親和性配置
- 自動重新調度

## 故障排除

### 節點無法加入叢集

```bash
# 檢查節點連接
ping <server-ip>

# 檢查端口
telnet <server-ip> 6443

# 查看 k3s 日誌
sudo journalctl -u k3s -f

# 查看節點狀態
kubectl get nodes
kubectl describe node <node-name>
```

### Pod 無法啟動

```bash
# 查看 Pod 狀態
kubectl get pods -A

# 查看 Pod 日誌
kubectl logs <pod-name> -n <namespace>

# 查看 Pod 事件
kubectl describe pod <pod-name> -n <namespace>
```

### CNI 問題

```bash
# 檢查 CNI Pods
kubectl get pods -n kube-system | grep -E "calico|flannel|cilium"

# 檢查網路策略
kubectl get networkpolicies -A

# 重啟 CNI Pods
kubectl delete pods -n kube-system -l k8s-app=calico-node
```

## 升級策略

### 控制平面滾動升級

```bash
# 升級第一個控制平面節點
export K3S_VERSION="v1.29.0+k3s1"
sudo ./02_init_control_plane.sh --role first-server --upgrade

# 升級額外控制平面節點
sudo ./02_init_control_plane.sh --role additional-server --upgrade
```

### Worker 節點滾動升級

```bash
# 驅逐 Worker 節點
kubectl cordon <node-name>
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# 升級 Worker 節點
export K3S_VERSION="v1.29.0+k3s1"
sudo ./03_join_worker_node.sh --upgrade

# 恢復 Worker 節點
kubectl uncordon <node-name>
```

## 備份與恢復

### 備份 etcd 數據

```bash
# 備份 k3s 數據
sudo k3s etcd-snapshot save --name snapshot-$(date +%Y%m%d)

# 列出快照
sudo k3s etcd-snapshot ls

# 刪除舊快照
sudo k3s etcd-snapshot delete snapshot-20240101
```

### 恢復 etcd 數據

```bash
# 停止 k3s
sudo systemctl stop k3s

# 恢復快照
sudo k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/snapshot-<name>

# 啟動 k3s
sudo systemctl start k3s
```