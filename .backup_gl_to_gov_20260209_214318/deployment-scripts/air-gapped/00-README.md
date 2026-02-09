# 實體隔離環境部署腳本 (Air-gapped/Offline)

## 目錄結構

```
air-gapped/
├── 00_README.md                           # 本文件
├── 01_export_resources.sh                 # 在線環境資源導出腳本
├── 02_import_resources.sh                 # 離線環境資源導入腳本
├── 03_setup_registry.sh                   # 本地 Registry 設置腳本
├── 04_install_k3s.sh                      # k3s 離線安裝腳本
├── 05_deploy_gl_backend.sh                # GL-Native Backend 部署
├── 06_dependency_check.sh                 # 依賴檢查清單腳本
└── bundles/                               # 離線安裝包
    ├── k3s-v1.28.3+k3s2.tar.gz
    ├── images/
    ├── charts/
    └── packages/
```

## 實體隔離環境特徵

### 環境特徵
- **完全無互聯網**：所有資源預下載到本地
- **內部網路**：僅內部 LAN，無外部 DNS
- **本地資源**：鏡像從本地 registry 拉取
- **依賴管理**：所有依賴必須預先準備

### 核心差異

| 特性 | 在線環境 | 離線環境 |
|------|----------|----------|
| **鏡像拉取** | Docker Hub / 公共 Registry | 本地 Registry |
| **依賴解決** | 自動（apt/yum） | 手動下載 |
| **更新機制** | 在線更新 | 離線更新包 |
| **故障排查** | 在線文檔/社區 | 本地文檔/日誌 |
| **安全性** | 依賴外部信任 | 完全隔離，自證 |

## 使用方式

### 階段 1：在線環境準備

在連接互聯網的機器上執行：

```bash
# 1. 導出所有需要的資源
./01_export_resources.sh \
  --k3s-version v1.28.3+k3s2 \
  --export-dir /tmp/offline-bundle \
  --registry localhost:5000

# 2. 創建離線安裝包
cd /tmp/offline-bundle
tar -czf offline-bundle.tar.gz .

# 3. 驗證安裝包完整性
sha256sum offline-bundle.tar.gz > offline-bundle.sha256
```

### 階段 2：傳輸到離線環境

使用安全的方式（USB、安全文件傳輸等）將 `offline-bundle.tar.gz` 傳輸到離線環境。

### 階段 3：離線環境部署

在離線環境機器上執行：

```bash
# 1. 解壓安裝包
tar -xzf offline-bundle.tar.gz -C /tmp/offline

# 2. 檢查依賴
./06_dependency_check.sh --bundle-dir /tmp/offline

# 3. 設置本地 Registry
./03_setup_registry.sh --bundle-dir /tmp/offline

# 4. 安裝 k3s
./04_install_k3s.sh \
  --bundle-dir /tmp/offline \
  --registry-url [EXTERNAL_URL_REMOVED]

# 5. 部署 GL-Native Backend
./05_deploy_gl_backend.sh --registry-url [EXTERNAL_URL_REMOVED]

# 6. 健康檢查
./health_check.sh
```

## 資源清單

### 必需資源

**Docker Images:**
- `rancher/k3s:v1.28.3+k3s2`
- `flannel/flannel:v0.22.0` 或 `calico/*:v3.26.1`
- `coredns/coredns:1.9.3`
- `traefik:2.10`
- `gov-native/backend:v1.1`

**Helm Charts:**
- `nginx-ingress:1.0.0`
- `prometheus:15.0.0`
- `grafana:6.50.0`

**二進制文件:**
- `k3s: v1.28.3+k3s2`
- `kubectl: v1.28.3`
- `helm: v3.12.0`

**OS 套件（Ubuntu/Debian）:**
- `containerd.io`
- `docker-ce`
- `docker-ce-cli`
- `ca-certificates`
- `curl`

### 可選資源

**監控工具:**
- `prometheus:2.45.0`
- `grafana:9.5.0`
- `node-exporter:1.6.0`

**日誌工具:**
- `elasticsearch:8.8.0`
- `fluentd:1.16.0`
- `kibana:8.8.0`

## 系統要求

### 硬體要求

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 200+ GB SSD（考慮鏡像大小）
- **Network**: 內部 LAN（1 Gbps+）

### 軟體要求

- **OS**: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+
- **Kernel**: >= 4.15（支持 cgroup v2）
- **Docker**: >= 20.10.0
- **時間同步**: chrony 或 ntpd

### 網路配置

- **DNS**: 本地 DNS 或 hosts 文件
- **NTP**: 內部 NTP 服務器
- **防火牆**: 允許內部通信
- **端口**: 6443（API）、5000（Registry）、8472（CNI）

## 離線套件管理策略

### 在線環境預下載

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

### 打包策略

- **鏡像打包**: `docker save` + `tar.gz`
- **Charts 打包**: Helm chart archive
- **二進制打包**: 單獨打包或包含在 tar.gz
- **完整性驗證**: SHA256 checksum

### 本地 Registry

**Registry 選擇**:
- **Harbor**: 企業級功能、安全掃描、Helm chart repository
- **Docker Registry v2**: 輕量級、簡單部署

**Registry 配置**:
- HTTP Basic Auth 認證
- TLS 證書（內部 CA）
- 存儲後端（本地文件系統、NFS）

## 依賴處理

### DNS 配置

**CoreDNS**:
- Kubernetes 內置 DNS
- 自動服務發現
- 自定義 DNS 配置

**本地 DNS**:
- Bind / dnsmasq
- 節點名稱解析
- 自定義域名

**Hosts 文件**:
- 簡單場景使用
- 手動維護
- 快速部署

### 時間同步

**內部 NTP 服務器**:
```bash
# 安裝 chrony
apt install chrony

# 配置 chrony.conf
server 192.168.1.10 iburst
allow 192.168.0.0/16
```

**節點時間同步**:
```bash
# 配置 ntp.conf
server ntp.internal iburst
restrict 192.168.0.0 mask 255.255.0.0 nomodify notrap
```

**時間檢查**:
```bash
# 檢查時間同步狀態
timedatectl status

# 檢查 NTP 服務
systemctl status chronyd
```

### 憑證管理

**內部 CA 生成**:
```bash
# 生成 CA 私鑰和證書
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ca.key \
  -out ca.crt

# 生成服務器證書
openssl req -new -nodes \
  -keyout server.key \
  -out server.csr

openssl x509 -req -in server.csr \
  -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt \
  -days 365
```

**證書分發**:
- 手動複製到所有節點
- 使用 Secret 管理證書
- 配置證書自動輪換

### Registry 認證

**HTTP Basic Auth**:
```bash
# 創建用戶名密碼
htpasswd -Bn registry_user > htpasswd

# 配置 Docker Registry
docker run -d -p 5000:5000 \
  --name registry \
  -v /auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  registry:2
```

**Docker Login**:
```bash
# 登錄到本地 Registry
docker login localhost:5000

# 輸入用戶名和密碼
```

**Kubernetes Secret**:
```bash
# 創建 Registry 認證 Secret
kubectl create secret docker-registry regcred \
  --docker-server=localhost:5000 \
  --docker-username=registry_user \
  --docker-password=password \
  --docker-email=user@example.com
```

## 依賴檢查清單

### 安裝前檢查

- [ ] 所有 images 已下載並導入
- [ ] 所有 Helm charts 已打包
- [ ] OS 套件依賴已收集
- [ ] 本地 Registry 運行正常
- [ ] NTP 服務器可達
- [ ] 內部 DNS 配置完成
- [ ] 憑證已生成並分發
- [ ] 磁碟空間充足（考慮 images 大小）
- [ ] 網路開通（節點間通信）

### 驗證命令

```bash
# 驗證 images
docker images | grep -E "k3s|flannel|coredns"

# 驗證二進制文件
ls -lh /tmp/offline/k3s
ls -lh /tmp/offline/helm

# 驗證 OS 套件
dpkg -l | grep -E "docker|containerd"

# 驗證 Helm charts
ls -lh /tmp/offline/charts/

# 驗證 Registry
curl [EXTERNAL_URL_REMOVED]

# 驗證 CA 證書
openssl verify ca.crt

# 驗證時間同步
timedatectl status | grep synchronized
```

## 版本與一致性

### 版本鎖定策略

**固定版本號**:
- 使用具體的版本號（如 v1.28.3+k3s2）
- 不使用 `latest` 標籤
- 維護版本清單文件

**版本清單**:
```bash
# versions.txt
k3s=v1.28.3+k3s2
flannel=v0.22.0
calico=v3.26.1
coredns=1.9.3
traefik=2.10
gov-native-backend=v1.1
```

**簽名驗證**:
- SHA256 校驗
- GPG 簽名驗證
- 完整性檢查

### 線上離線一致性

**環境對齊**:
- 確保線上離線環境配置一致
- 相同的 OS 版本
- 相同的內核版本
- 相同的依賴版本

**依賴完整**:
- 不遺漏任何依賴
- 遞歸檢查依賴
- 測試環境驗證

**版本匹配**:
- 所有組件版本完全一致
- 配置文件版本一致
- 環境變數一致

### 離線環境升級流程

**1. 在線環境準備**:
```bash
# 下載新版本組件
./01_export_resources.sh \
  --k3s-version v1.29.0+k3s1 \
  --export-dir /tmp/upgrade-bundle

# 測試新版本功能
# 在測試環境驗證

# 打包離線安裝包
cd /tmp/upgrade-bundle
tar -czf upgrade-bundle.tar.gz .
```

**2. 驗證完整性**:
```bash
# SHA256 校驗
sha256sum upgrade-bundle.tar.gz > upgrade-bundle.sha256

# 依賴檢查
./06_dependency_check.sh --bundle-dir /tmp/upgrade-bundle
```

**3. 傳輸到離線環境**:
```bash
# 安全傳輸（加密）
scp -C upgrade-bundle.tar.gz user@offline-host:/tmp/

# 完整性驗證
sha256sum -c upgrade-bundle.sha256
```

**4. 測試環境驗證**:
```bash
# 在測試環境部署
./04_install_k3s.sh --upgrade

# 功能驗證
./health_check.sh --verbose

# 性能測試
./performance_test.sh
```

**5. 生產環境部署**:
```bash
# 備份當前環境
./backup.sh --full

# 滾動升級
./04_install_k3s.sh --upgrade --rolling

# 監控升級過程
./monitor_upgrade.sh

# 驗證升級結果
./health_check.sh --full
```

## 常見問題

### 依賴缺失

**症狀**:
- 部署時發現缺少某個 image 或套件
- `ImagePullBackOff` 錯誤
- `ErrImagePull` 錯誤

**原因**:
- 依賴清單不完整
- 版本不匹配
- 打包時遺漏

**解決**:
```bash
# 建立完整的依賴清單
./01_export_resources.sh --verify

# 在線環境驗證所有依賴
docker images
ls -lh packages/

# 打包前進行完整性檢查
./06_dependency_check.sh --bundle-dir /tmp/offline
```

### 版本不匹配

**症狀**:
- 線上離線版本不一致
- API 不兼容
- 配置錯誤

**原因**:
- 版本管理不嚴格
- 不同步更新
- 標籤混淆

**解決**:
```bash
# 使用版本鎖定
export K3S_VERSION="v1.28.3+k3s2"

# 維護版本清單
cat versions.txt

# 簽名驗證
sha256sum -c *.sha256
```

### 時間同步失效

**症狀**:
- 憑證驗證失敗
- API 通信錯誤
- 時間戳不一致

**原因**:
- NTP 服務器不可達
- 配置錯誤
- 網路問題

**解決**:
```bash
# 配置內部 NTP 服務器
vim /etc/chrony.conf
systemctl restart chronyd

# 驗證時間同步狀態
timedatectl status

# 檢查 NTP 服務
chronyc sources
```

### Registry 不可達

**症狀**:
- 節點無法拉取 images
- `ErrImagePull` 錯誤
- 連接超時

**原因**:
- Registry 服務故障
- 網路問題
- 認證失敗

**解決**:
```bash
# 監控 Registry 健康狀態
docker ps | grep registry

# 檢查 Registry 日誌
docker logs registry

# 測試 Registry 連接
curl [EXTERNAL_URL_REMOVED]

# 配置 Registry 高可用
./03_setup_registry.sh --ha
```

### DNS 配置錯誤

**症狀**:
- 節點無法解析域名
- 服務發現失敗
- 連接超時

**原因**:
- DNS 配置錯誤
- 服務故障
- 網路問題

**解決**:
```bash
# 配置本地 DNS
vim /etc/resolv.conf

# 使用 hosts 文件作為備用
echo "192.168.1.100 registry.local" >> /etc/hosts

# 測試 DNS 解析
nslookup registry.local
dig registry.local
```

## 最佳實踐

### 安全性

1. **內部 CA**:
   - 使用自簽名 CA
   - 輪換證書
   - 分發證書

2. **Registry 認證**:
   - 使用 HTTP Basic Auth
   - TLS 加密通信
   - 定期更換密碼

3. **網路隔離**:
   - 配置防火牆規則
   - 限制外部訪問
   - 監控網路流量

### 可維護性

1. **版本管理**:
   - 使用 Git 管理配置
   - 維護版本清單
   - 記錄變更日誌

2. **備份策略**:
   - 定期備份 etcd
   - 備份配置文件
   - 備份 Registry

3. **監控告警**:
   - 監控資源使用
   - 監控服務健康
   - 配置告警規則

### 擴展性

1. **水平擴展**:
   - 添加工作節點
   - 配置負載均衡
   - 使用 Cluster Autoscaler

2. **垂直擴展**:
   - 增加節點資源
   - 優化性能
   - 調整配置

## 故障排除

### 通用步驟

1. **檢查日誌**:
   ```bash
   # k3s 日誌
   journalctl -u k3s -f
   
   # Pod 日誌
   kubectl logs <pod-name>
   
   # Registry 日誌
   docker logs registry
   ```

2. **檢查狀態**:
   ```bash
   # 節點狀態
   kubectl get nodes
   
   # Pod 狀態
   kubectl get pods -A
   
   # 服務狀態
   kubectl get svc -A
   ```

3. **檢查網路**:
   ```bash
   # 網路連接
   ping <node-ip>
   
   # 端口開放
   telnet <node-ip> 6443
   
   # DNS 解析
   nslookup <service-name>
   ```

### 特定問題

參見 `05_TROUBLESHOOTING.md` 詳細故障排除指南。