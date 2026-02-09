# GL-Native Execution Backend 部署架構分析

## 技術選擇與理由

### 為什麼選擇 k3s？

**k3s 作為統一執行引擎的核心理由：**

1. **單二進制部署** - 單一可執行檔案，簡化安裝與維護
2. **資源占用極低** - 最小 512MB RAM 運行，適合邊緣環境
3. **完全相容 K8s API** - 所有標準 K8s 工具均可使用
4. **內建 SQL 儲存** - 不需要外部 etcd 叢集
5. **優化網路性能** - 內置 Traefik Ingress + ServiceLB
6. **離線友好** - 支持完整的離線部署模式

**環境適配性：**
- 單節點：k3s 原生單節點模式
- 叢集：k3s multi-server 模式（1-3 控制平面）
- 實體隔離：k3s air-gapped 安裝模式

---

## 1. 單節點環境 (Single Node)

### 1.1 架構概念說明

**節點角色與網路拓樸：**
- **節點角色**：單一節點兼控制平面（API Server、Scheduler、Controller Manager）和數據平面（Kubelet、Pods）
- **網路拓樸**：本地回環（localhost）或簡單橋接網路，無需跨主機通信
- **控制平面與數據平面關係**：在同一進程空間運行（k3s single mode）
- **存儲設計**：所有 Kubernetes 組件打包在單一 VM/主機中，使用本地存儲

**適用場景：**
- 開發/測試環境
- 邊緣計算（Edge Computing）
- 小型應用部署
- 快速原型驗證

### 1.2 核心差異分析

**單節點 vs 叢集 vs 實體隔離：**

| 特性 | 單節點 | 叢集 | 實體隔離 |
|------|--------|------|----------|
| **高可用性** | ❌ 無冗餘（單點故障） | ✅ 多節點高可用 | 取決於配置 |
| **網路依賴** | 本地通信 | 跨主機扁平網路 | 內部 LAN，無外部 DNS |
| **資源需求** | 最小（2C/4G/50G） | 較高（4C/8G/100G+） | 較高（預下載資源） |
| **部署複雜度** | ⭐ 低 | ⭐⭐ 中 | ⭐⭐⭐ 高 |
| **安全要求** | 基本安全 | RBAC + NetworkPolicy | 內部 CA + 手動密鑰分發 |
| **升級策略** | 版本切換腳本 | Rolling Update | 預下載 + 重裝 |
| **故障恢復** | 慢（需重裝） | 快（自動調度） | 取決於備份策略 |

### 1.3 部署關鍵考量點

#### 高可用性、擴展性、資源配置

**高可用性：**
- 單點故障風險：節點故障 = 服務中斷
- 緩解策略：
  - 定期備份 etcd (SQLite) 數據
  - 使用 k3s 的備份恢復機制
  - 準備快速重裝腳本
  - 監控系統資源使用率

**擴展性：**
- 水平擴展限制：單節點無法水平擴展
- 垂直擴展：增加 CPU/RAM/Storage
- 適用場景：小於 50 Pods，流量 < 1000 QPS
- 擴展建議：
  - CPU: 2-4 cores（開發），4-8 cores（生產）
  - RAM: 4-8 GB（開發），8-16 GB（生產）
  - Storage: 50-100 GB SSD

#### 安全性（憑證、密鑰管理、RBAC、網路隔離）

**憑證管理：**
- 默認使用 k3s 自動生成的憑證
- kubeconfig 文件位於 `/etc/rancher/k3s/k3s.yaml`
- 憑證有效期：1 年（可配置）
- 建議：定期輪換憑證

**密鑰管理：**
- Kubernetes Secrets：存儲敏感數據
- 憑證加密：啟用 Encryption at Rest
- 環境變數：通過 Pod env 注入
- 最佳實踐：避免硬編碼密鑰

**RBAC（基於角色的訪問控制）：**
- 默認啟用 RBAC
- 角色：ClusterRole（集群級）、Role（命名空間級）
- 綁定：ClusterRoleBinding、RoleBinding
- 最小權限原則：僅授予必要的權限

**網路隔離：**
- Pod 網路隔離：`hostNetwork: false`
- Service 隔離：ClusterIP（默認）、NodePort、LoadBalancer
- Network Policy：可選的 Pod 級網路策略

#### 可維護性（升級策略、版本管理、日誌與監控）

**升級策略：**
- k3s 版本切換腳本：`k3s-install.sh --version <new-version>`
- 最小停機：k3s 支持滾動升級
- 回滾機制：保留舊版本二進制文件
- 升級檢查清單：
  - 驗證新版本兼容性
  - 備份當前配置
  - 測試升級流程
  - 監控升級後的服務

**版本管理：**
- 使用 Git tag 標記配置版本
- 配置文件版本化：`configs/k3s-config-v1.28.3.yaml`
- 變更日誌記錄：`CHANGELOG.md`
- 版本鎖定：固定 k3s 版本號

**日誌管理：**
- 系統日誌：`journalctl -u k3s`
- 應用日誌：`kubectl logs <pod>`
- 日誌聚合：可選的 ELK stack
- 日誌保留：默認 24 小時，可配置

**監控：**
- 系統監控：`top`、`htop`、`vmstat`
- Kubernetes 監控：
  - Metrics Server：資源使用監控
  - Prometheus operator：單節點版
  - Grafana：可視化儀表板
- 健康檢查：`./04_health_check.sh`

#### 容易出問題點

**1. 資源爭用**
- 症狀：Pod 被 evicted
- 原因：CPU/記憶體不足
- 解決：
  - 配置 Resource limits
  - 監控資源使用
  - 增加節點資源
  - 使用 PriorityClass

**2. 端口衝突**
- 症狀：k3s 無法啟動
- 原因：端口被佔用（e.g., 6443 API 端口）
- 解決：
  - 檢查端口：`ss -tuln | grep 6443`
  - 停止佔用進程
  - 修改 k3s 配置使用其他端口

**3. 鏡像拉取失敗**
- 症狀：ImagePullBackOff
- 原因：網路不穩、registry 不可達
- 解決：
  - 檢查網路連接
  - 配置 image pull policy
  - 預先拉取鏡像
  - 使用本地 registry

**4. 時間同步問題**
- 症狀：憑證驗證失敗
- 原因：系統時間不準確
- 解決：
  - 安裝 NTP：`apt install ntp`
  - 同步時間：`timedatectl set-ntp true`
  - 檢查同步：`timedatectl status`

---

## 2. 叢集環境 (Cluster)

### 2.1 架構概念說明

**節點角色定義：**
- **控制平面節點**（Control Plane Nodes）：
  - 至少 1 個（生產建議 3 個）
  - 角色：etcd、API Server、Scheduler、Controller Manager
  - 職責：集群管理、調度決策、狀態維護
  
- **工作節點**（Worker Nodes）：
  - 2-N 個（根據工作負載）
  - 角色：Kubelet、CNI、Pods
  - 職責：運行工作負載、資源管理

**網路拓樸：**
- **跨主機扁平網路**：CNI 提供跨主機 Pod-to-Pod 通信
- **Service 網路**：ClusterIP、NodePort、LoadBalancer
- **Ingress 網路**：Traefik/NGINX Ingress Controller
- **CNI 選擇**：Flannel（簡單）、Calico（強大）、Cilium（高性能）

**控制平面與數據平面關係：**
- **分離原則**：控制節點不調度 Pods（除非 taint 移除）
- **etcd 集群化**：多個控制節點組成 etcd 集群，確保一致性
- **通信方式**：API Server 與 Kubelet 通過 HTTPS 通信
- **數據一致性**：etcd 作為單一事實來源

**存儲設計：**
- **本地存儲**：每個節點本地 SSD
- **共享存儲**：NFS / Ceph（跨節點共享）
- **備份策略**：定期快照 + etcd 備份
- **持久化存儲**：PVC + StorageClass

### 2.2 核心差異分析

**叢集環境優勢：**
- **高可用性**：多節點冗餘，單點故障不影響整體服務
- **負載均衡**：流量分發到多個節點
- **彈性擴展**：動態添加/移除節點
- **資源利用率**：多節點共享資源池
- **故障隔離**：單個節點故障不影響其他節點

**與單節點的關鍵區別：**
1. **架構複雜度**：多節點協調、網路配置
2. **運維成本**：需要更多的運維工作
3. **資源需求**：總體資源需求更高
4. **故障處理**：需要處理節點間故障
5. **性能優勢**：更好的並行處理能力

**與實體隔離的關鍵區別：**
- **網路依賴**：依賴外部網路拉取鏡像
- **更新機制**：可以直接從在線更新
- **依賴管理**：自動解決依賴
- **部署速度**：部署速度更快

### 2.3 部署關鍵考量點

#### 高可用性、擴展性、資源配置

**高可用性配置：**
- **控制平面 HA**：
  - 3 個控制平面節點（奇數個，確保 etcd quorum）
  - 負載均衡器：HAProxy + Keepalived VIP
  - etcd quorum：可容忍 1 個節點故障
  - 自動故障轉移：< 30 秒恢復
  
- **工作節點 HA**：
  - 多個 Worker 節點（2-N 個）
  - Pod 反親和性配置
  - 自動重新調度
  - PodDisruptionBudget 配置

**擴展性策略：**
- **水平擴展**：
  - 動態添加 Worker 節點
  - 使用 Cluster Autoscaler
  - 支持雲原生自動擴展
  
- **垂直擴展**：
  - 每個節點可升級 CPU/RAM
  - 在線升級（部分雲平台支持）
  
- **資源配置建議**：
  ```
  控制平面節點：
  - CPU: 4 cores
  - RAM: 8 GB
  - Storage: 100 GB SSD
  
  工作節點：
  - CPU: 8+ cores
  - RAM: 16+ GB
  - Storage: 200+ GB SSD
  ```

**負載均衡配置：**
- **HAProxy 配置**：負載均衡 API Server 流量
- **Keepalived 配置**：提供虛擬 IP（VIP）
- **Session Affinity**：基於客戶端 IP 的會話保持
- **健康檢查**：定期檢查 API Server 健康狀態

#### 安全性（憑證、密鑰管理、RBAC、網路隔離）

**憑證管理：**
- **自動生成**：k3s 自動生成集群憑證
- **TLS SAN 配置**：添加所有控制平面節點 IP
- **憑證輪換**：定期更新憑證
- **cert-manager**：自動管理 TLS 憑證

**密鑰管理：**
- **Sealed Secrets**：加密 Kubernetes Secrets
- **Vault**：企業級密鑰管理
- **External Secrets**：從外部系統同步密鑰
- **密鑰加密**：啟用 etcd 加密

**RBAC 配置：**
- **細粒度控制**：基於角色的訪問控制
- **命名空間隔離**：不同環境使用不同命名空間
- **最小權限原則**：僅授予必要的權限
- **審計日誌**：記錄所有 RBAC 操作

**網路隔離：**
- **Network Policy**：Pod 級網路策略
- **VLAN 隔離**：網路層隔離
- **Service Mesh**：Istio/Linkerd 提供更細粒度的網路控制
- **防火牆規則**：限制不必要的網路訪問

#### 可維護性（升級策略、版本管理、日誌與監控）

**升級策略：**
- **滾動升級**：逐個節點升級，最小化停機
- **金絲雀發布**：分批部署新版本
- **版本鎖定**：使用 Helm values.yaml 固定版本
- **回滾機制**：保留舊版本配置

**版本管理：**
- **Helm**：統一管理應用版本
- **GitOps**：ArgoCD/Flux 自動化部署
- **配置版本化**：所有配置文件納入版本控制
- **變更日誌**：記錄所有版本變更

**日誌聚合：**
- **EFK Stack**：Elasticsearch + Fluentd + Kibana
- **Loki Stack**：Loki + Promtail + Grafana
- **集中化日誌**：所有節點日誌集中存儲
- **日誌查詢**：強大的日誌搜索和分析能力

**監控系統：**
- **Kubernetes Dashboard**：集群可視化
- **Metrics Server**：資源使用監控
- **Prometheus**：指標收集和存儲
- **Grafana**：可視化儀表板
- **AlertManager**：告警通知

#### 容易出問題點

**1. 節點間網路延遲**
- **症狀**：Pods 無法通信
- **原因**：CNI 配置錯誤、網路延遲過高
- **解決**：
  - 檢查 CNI 配置
  - 測試節點間連通性
  - 調整 CNI 后端模式
  - 檢查防火牆規則

**2. etcd quorum 丟失**
- **症狀**：集群不可用
- **原因**：多個控制平面節點故障
- **解決**：
  - 維護奇數個控制節點
  - 定期備份 etcd
  - 監控 etcd 健康狀態
  - 快速恢復故障節點

**3. 憑證過期**
- **症狀**：API 通信失敗
- **原因**：憑證有效期過期
- **解決**：
  - 設置憑證自動輪換
  - 監控憑證有效期
  - 定期更新憑證
  - 配置告警通知

**4. 資源耗盡**
- **症狀**：Pod 無法調度、系統變慢
- **原因**：無限制的 Pod 導致 OOM
- **解決**：
  - 配置 Resource limits
  - 使用 PriorityClass
  - 監控資源使用
  - 自動擴展節點

---

## 3. 實體隔離環境 (Air-gapped/Offline)

### 3.1 架構概念說明

**環境特徵：**
- **完全無互聯網**：所有資源預下載到本地
- **內部網路**：僅內部 LAN，無外部 DNS
- **本地資源**：鏡像從本地 registry 拉取
- **依賴管理**：所有依賴必須預先準備

**節點角色：**
- 同集群環境：控制節點、工作節點
- 但所有組件都依賴本地資源

**網路拓樸：**
- **內部 LAN**：節點間通信
- **無外部 DNS**：使用本地 DNS 或 hosts 文件
- **內部 NTP**：時間同步服務器
- **內部 CA**：自簽名證書

**控制平面與數據平面：**
- 同集群環境架構
- 但依賴本地 NTP/CA

### 3.2 核心差異分析

**實體隔離環境挑戰：**
- **資源準備**：需要預下載所有依賴
- **版本管理**：確保線上離線版本一致
- **升級複雜**：需要預下載新版本
- **故障恢復**：缺少在線支持

**與在線環境的關鍵區別：**
1. **鏡像拉取**：從本地 registry 而非公共 registry
2. **依賴解決**：手動管理所有依賴
3. **更新機制**：離線更新包傳輸
4. **故障排查**：缺少在線文檔和社區支持

**優勢：**
- **安全性**：完全隔離，減少攻擊面
- **合規性**：滿足嚴格的安全合規要求
- **穩定性**：不依賴外部網路
- **可控性**：完全控制所有組件

### 3.3 部署關鍵考量點

#### 離線套件管理策略

**在線環境預下載：**
```bash
# Docker images
docker pull rancher/k3s:v1.28.3+k3s2
docker pull flannel/flannel:v0.22.0

# Helm charts
helm pull stable/nginx-ingress --version 1.0.0

# k3s 二進制文件
curl -LO [EXTERNAL_URL_REMOVED]

# OS 套件
apt-get download docker-ce docker-ce-cli containerd.io
```

**打包策略：**
- **鏡像打包**：`docker save` + `tar.gz`
- **Charts 打包**：Helm chart archive
- **二進制打包**：單獨打包或包含在 tar.gz
- **完整性驗證**：SHA256 checksum

**本地 Registry 配置：**
- **Registry 選擇**：Harbor / Docker Registry v2
- **Registry 部署**：內部網路部署
- **鏡像導入**：`docker load` + `docker tag` + `docker push`
- **Registry 認證**：HTTP Basic Auth

#### 依賴處理

**DNS 配置：**
- **CoreDNS**：Kubernetes 內置 DNS
- **本地 DNS**：Bind / dnsmasq
- **Hosts 文件**：簡單場景使用

**時間同步：**
- **內部 NTP 服務器**：chrony / ntpd
- **節點時間同步**：配置 ntp.conf
- **時間檢查**：`timedatectl status`
- **時區配置**：統一 UTC 或本地時區

**憑證管理：**
- **內部 CA**：openssl 生成自簽名 CA
- **證書分發**：手動分發到所有節點
- **證書有效期**：設置合理的有效期
- **證書輪換**：定期更新證書

**Registry 認證：**
- **HTTP Basic Auth**：簡單認證
- **TLS 證書**：加密通信
- **Docker Login**：`docker login localhost:5000`
- **Kubernetes Secret**：配置 registry 認證

**依賴檢查清單：**
- [ ] 所有 images 已下載並導入
- [ ] 所有 Helm charts 已打包
- [ ] OS 套件依賴已收集
- [ ] 本地 Registry 運行正常
- [ ] NTP 服務器可達
- [ ] 內部 DNS 配置完成
- [ ] 憑證已生成並分發
- [ ] 磁碟空間充足（考慮 images 大小）
- [ ] 網路開通（節點間通信）

#### 版本與一致性

**版本鎖定策略：**
- **固定版本號**：使用具體的版本號（如 v1.28.3+k3s2）
- **版本清單**：維護所有組件的版本清單
- **簽名驗證**：驗證下載文件的完整性
- **測試驗證**：在線環境測試通過後再打包

**線上離線一致性：**
- **環境對齊**：確保線上離線環境配置一致
- **依賴完整**：不遺漏任何依賴
- **版本匹配**：所有組件版本完全一致
- **測試覆蓋**：在線環境測試所有功能

**離線環境升級流程：**
1. **在線環境準備**：
   - 下載新版本組件
   - 測試新版本功能
   - 打包離線安裝包
   
2. **驗證完整性**：
   - SHA256 校驗
   - 依賴檢查
   - 功能測試
   
3. **傳輸到離線環境**：
   - 安全傳輸（加密）
   - 完整性驗證
   - 備份舊版本
   
4. **測試環境驗證**：
   - 在測試環境部署
   - 功能驗證
   - 性能測試
   
5. **生產環境部署**：
   - 滾動升級
   - 監控升級過程
   - 驗證升級結果

#### 容易出問題點

**1. 依賴缺失**
- **症狀**：部署時發現缺少某個 image 或套件
- **原因**：依賴清單不完整
- **解決**：
  - 建立完整的依賴清單
  - 在線環境驗證所有依賴
  - 打包前進行完整性檢查

**2. 版本不匹配**
- **症狀**：線上離線版本不一致
- **原因**：版本管理不嚴格
- **解決**：
  - 使用版本鎖定
  - 維護版本清單
  - 簽名驗證

**3. 時間同步失效**
- **症狀**：憑證驗證失敗
- **原因**：NTP 服務器不可達或配置錯誤
- **解決**：
  - 配置內部 NTP 服務器
  - 驗證時間同步狀態
  - 設置告警

**4. Registry 不可達**
- **症狀**：節點無法拉取 images
- **原因**：Registry 服務故障或網路問題
- **解決**：
  - 監控 Registry 健康狀態
  - 配置 Registry 高可用
  - 預先拉取 images 到節點

**5. DNS 配置錯誤**
- **症狀**：節點無法解析域名
- **原因**：DNS 配置錯誤或服務故障
- **解決**：
  - 配置本地 DNS
  - 使用 hosts 文件作為備用
  - 測試 DNS 解析

---

## 4. 技術棧選擇理由

### 4.1 單節點環境
**選擇：k3s (Single Server)**
- 原因：
  1. 原生支持單節點模式
  2. 最小資源占用（512MB RAM）
  3. 內置 Ingress + ServiceLB
  4. 完整 K8s API 相容
  5. 簡單升級和維護

### 4.2 叢集環境
**選擇：k3s Multi-Server**
- 原因：
  1. 簡化叢集搭建（相比 kubeadm）
  2. 內置 HA 支持
  3. 統一管理控制平面和工作節點
  4. 內置 SQL 儲存（不需要外部 etcd）
  5. 滾動升級簡化

### 4.3 實體隔離環境
**選擇：k3s Air-gapped Mode + Harbor Registry**
- 原因：
  1. k3s 支持離線安裝模式
  2. Harbor 提供完整離線 Registry
  3. 支持本地 Helm chart repository
  4. 安全掃描功能
  5. 複製功能支持

---

## 5. 部署風險評估

### 5.1 單節點風險
- **單點故障**：節點宕機 = 服務中斷
  - 緩解：定期備份 + 快速重裝腳本
- **資源競爭**：多個 Pod 競爭有限資源
  - 緩解：Resource limits + Priority
- **擴展限制**：無法水平擴展
  - 緩解：規劃時預留容量

### 5.2 叢集風險
- **etcd quorum 失效**：多個控制平面故障
  - 緩解：3 個控制平面 + 定期備份
- **網路分區**：節點無法通信
  - 緩解：多路網路 + 預警機制
- **配置漂移**：節點配置不一致
  - 緩解：GitOps (ArgoCD) + IaC

### 5.3 實體隔離風險
- **依賴缺失**：部署時發現缺少組件
  - 緩解：完整依賴清單 + 驗證腳本
- **版本不匹配**：線上離線版本不一致
  - 緩解：版本鎖定 + 完整性驗證
- **升級困難**：離線環境升級複雜
  - 緩解：測試環境驗證 + 滾動升級

---

## 6. 部署腳本可重用性設計

### 6.1 變數化設計

所有腳本支持環境變數配置：

```bash
# k3s 配置
export K3S_VERSION="v1.28.3+k3s2"
export CLUSTER_CIDR="10.42.0.0/16"
export SERVICE_CIDR="10.43.0.0/16"

# 節點配置
export CONTROL_PLANE_IPS="192.168.1.11,192.168.1.12,192.168.1.13"
export WORKER_IPS="192.168.1.21,192.168.1.22,192.168.1.23"

# GL-Native 配置
export NAMESPACE="gov-native"
export BACKEND_VERSION="v1.1"
```

### 6.2 模組化設計

每個腳本獨立運行，可組合使用：

```bash
# 單節點部署
./01_pre_install_check.sh
./02_install_k3s.sh
./03_deploy_gl_backend.sh
./04_health_check.sh

# 叢集部署
./01_pre_install_check.sh --role first-server
./02_init_control_plane.sh --role first-server
./03_join_worker_node.sh --server-url <url> --token <token>
./04_install_cni.sh --plugin calico
./05_deploy_gl_backend.sh
./06_health_check.sh
```

### 6.3 錯誤處理

所有腳本包含完整的錯誤處理：

```bash
set -e  # 遇到錯誤立即退出
set -u  # 使用未定義的變數時報錯
set -o pipefail  # 管道中任何命令失敗都退出

# 檢查命令是否存在
if ! command -v kubectl > /dev/null 2>&1; then
    print_error "kubectl 未安裝"
    exit 1
fi

# 檢查服務狀態
if systemctl is-active --quiet k3s; then
    print_success "k3s 服務正在運行"
else
    print_error "k3s 服務未運行"
    exit 1
fi
```

---

## 7. 下一步

下一階段將實施：
- Phase 4: 實體隔離環境部署腳本
- Phase 5: 部署流程與檢查清單
- Phase 6: 故障排除與最佳實踐
- Phase 7: 完整文檔整合

所有腳本將遵循：
- ✅ 可執行性（完整腳本，非片段）
- ✅ 可維護性（註解清晰，模組化）
- ✅ 可擴展性（參數化配置）
- ✅ 安全性（最小權限，審計日誌）