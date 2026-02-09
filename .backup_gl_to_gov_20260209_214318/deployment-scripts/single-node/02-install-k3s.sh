#!/bin/bash

###############################################################################
# GL-Native Execution Backend - k3s 安裝腳本 (單節點環境)
#
# 用途：安裝並配置 k3s Kubernetes 叢集
# 使用方式：./02_install_k3s.sh [--version VERSION] [--air-gapped]
###############################################################################

set -e  # 遇到錯誤立即退出
set -u  # 使用未定義的變數時報錯

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 全局變數
K3S_VERSION=${K3S_VERSION:-"v1.28.3+k3s2"}
K3S_INSTALL_DIR=${K3S_INSTALL_DIR:-"/usr/local/bin"}
K3S_CONFIG_DIR=${K3S_CONFIG_DIR:-"/etc/rancher/k3s"}
K3S_DATA_DIR=${K3S_DATA_DIR:-"/var/lib/rancher/k3s"}
AIR_GAPPED=${AIR_GAPPED:-false}
INSTALL_MODE="single-node"

# k3s 配置選項
K3S_CLUSTER_CIDR=${K3S_CLUSTER_CIDR:-"10.42.0.0/16"}
K3S_SERVICE_CIDR=${K3S_SERVICE_CIDR:-"10.43.0.0/16"}
K3S_CLUSTER_DNS=${K3S_CLUSTER_DNS:-"10.43.0.10"}
K3S_DISABLE_TRAEFIK=${K3S_DISABLE_TRAEFIK:-"false"}
K3S_DISABLE_SERVICE_LB=${K3S_DISABLE_SERVICE_LB:-"false"}

###############################################################################
# 工具函數
###############################################################################

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

print_step() {
    echo ""
    echo "[$1] $2"
}

###############################################################################
# 前置檢查
###############################################################################

pre_install_check() {
    print_header "前置檢查"
    
    # 檢查 root 權限
    if [ "$EUID" -ne 0 ]; then 
        print_error "請使用 root 權限執行此腳本"
        exit 1
    fi
    
    # 檢查 OS
    if [ ! -f /etc/os-release ]; then
        print_error "無法檢測作業系統"
        exit 1
    fi
    
    . /etc/os-release
    print_info "OS: $NAME $VERSION_ID"
    
    # 檢查現有 k3s
    if command -v k3s > /dev/null 2>&1; then
        local existing_version=$(k3s --version 2>/dev/null | head -1)
        print_warning "檢測到 k3s 已安裝: $existing_version"
        read -p "是否要卸載並重新安裝? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "卸載現有 k3s..."
            /usr/local/bin/k3s-uninstall.sh || true
        else
            print_error "取消安裝"
            exit 1
        fi
    fi
    
    print_success "前置檢查通過"
}

###############################################################################
# 安裝依賴
###############################################################################

install_dependencies() {
    print_step "1/7" "安裝依賴套件"
    
    . /etc/os-release
    
    case "$ID" in
        ubuntu|debian)
            print_info "更新套件索引..."
            apt-get update -qq
            
            print_info "安裝依賴套件..."
            apt-get install -y -qq curl wget ca-certificates
            
            print_info "安裝並配置 iptables..."
            apt-get install -y -qq iptables arptables ebtables
            update-alternatives --set iptables /usr/sbin/iptables-legacy 2>/dev/null || true
            update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy 2>/dev/null || true
            ;;
        rhel|rocky|centos)
            print_info "安裝依賴套件..."
            yum install -y -q curl wget ca-certificates
            
            print_info "安裝並配置 iptables..."
            yum install -y -q iptables arptables ebtables
            ;;
        *)
            print_error "不支援的作業系統: $ID"
            exit 1
            ;;
    esac
    
    # 加載 kernel 模組
    print_info "加載 Kernel 模組..."
    modprobe br_netfilter 2>/dev/null || true
    modprobe overlay 2>/dev/null || true
    
    # 持久化 kernel 模組
    mkdir -p /etc/modules-load.d
    cat > /etc/modules-load.d/k3s.conf <<EOF
br_netfilter
overlay
EOF
    
    # 配置 sysctl
    print_info "配置 sysctl 參數..."
    cat > /etc/sysctl.d/99-k3s.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
    sysctl --system > /dev/null
    
    # 關閉 swap
    print_info "關閉 Swap..."
    swapoff -a 2>/dev/null || true
    sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
    
    print_success "依賴套件安裝完成"
}

###############################################################################
# 下載 k3s
###############################################################################

download_k3s() {
    print_step "2/7" "下載 k3s"
    
    K3S_BIN_URL="https://github.com/k3s-io/k3s/releases/download/${K3S_VERSION}/k3s"
    
    print_info "下載 k3s ${K3S_VERSION}..."
    if ! wget -q --show-progress --progress=bar:force -O "${K3S_INSTALL_DIR}/k3s" "${K3S_BIN_URL}"; then
        print_error "下載 k3s 失敗"
        exit 1
    fi
    
    print_info "設置執行權限..."
    chmod +x "${K3S_INSTALL_DIR}/k3s"
    
    print_info "創建符號連結..."
    ln -sf "${K3S_INSTALL_DIR}/k3s" /usr/local/bin/crictl
    ln -sf "${K3S_INSTALL_DIR}/k3s" /usr/local/bin/kubectl
    
    print_success "k3s 下載完成"
}

###############################################################################
# 配置 k3s
###############################################################################

configure_k3s() {
    print_step "3/7" "配置 k3s"
    
    # 創建配置目錄
    mkdir -p "${K3S_CONFIG_DIR}"
    
    # 創建配置檔案
    print_info "創建 k3s 配置檔案..."
    cat > "${K3S_CONFIG_DIR}/config.yaml" <<EOF
# GL-Native k3s 配置
# 安裝模式: ${INSTALL_MODE}
# 版本: ${K3S_VERSION}

# 網路配置
cluster-cidr: ${K3S_CLUSTER_CIDR}
service-cidr: ${K3S_SERVICE_CIDR}
cluster-dns: ${K3S_CLUSTER_DNS}

# 禁用組件
disable:
  - local-storage
  - metrics-server  # 如果需要 metrics，請註釋此行

# 禁用 Traefik (如果使用其他 Ingress Controller)
EOF

    if [ "$K3S_DISABLE_TRAEFIK" = "true" ]; then
        echo "  - traefik" >> "${K3S_CONFIG_DIR}/config.yaml"
    fi

    if [ "$K3S_DISABLE_SERVICE_LB" = "true" ]; then
        echo "  - servicelb" >> "${K3S_CONFIG_DIR}/config.yaml"
    fi

    cat >> "${K3S_CONFIG_DIR}/config.yaml" <<EOF

# 啟用組件
enable-features:
  - EphemeralContainers

# 容器運行時配置
docker: false
container-runtime-endpoint: ""

# 日誌配置
log: /var/log/k3s.log

# 數據存儲
data-dir: ${K3S_DATA_DIR}

# 安全配置
tls-san:
  - $(hostname)
  - $(hostname -f)
  - 127.0.0.1
  - localhost

# 其他選項
write-kubeconfig-mode: "0644"
node-name: $(hostname)
EOF
    
    print_info "配置檔案已創建: ${K3S_CONFIG_DIR}/config.yaml"
    print_success "k3s 配置完成"
}

###############################################################################
# 安裝 k3s 服務
###############################################################################

install_k3s_service() {
    print_step "4/7" "安裝 k3s 服務"
    
    # 下載安裝腳本
    print_info "下載 k3s 安裝腳本..."
    curl -sfL https://get.k3s.io -o /tmp/k3s-install.sh
    chmod +x /tmp/k3s-install.sh
    
    # 創建環境變數檔案
    cat > /etc/systemd/system/k3s.service.env <<EOF
# GL-Native k3s 環境變數
INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml"
K3S_VERSION=${K3S_VERSION}
EOF
    
    print_info "安裝 k3s 服務..."
    INSTALL_K3S_SKIP_DOWNLOAD=true \
    INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml" \
    INSTALL_K3S_VERSION="${K3S_VERSION}" \
    bash /tmp/k3s-install.sh
    
    print_success "k3s 服務安裝完成"
}

###############################################################################
# 啟動 k3s
###############################################################################

start_k3s() {
    print_step "5/7" "啟動 k3s 服務"
    
    print_info "啟用並啟動 k3s 服務..."
    systemctl enable k3s
    systemctl start k3s
    
    # 等待 k3s 啟動
    print_info "等待 k3s 啟動..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if systemctl is-active --quiet k3s; then
            print_success "k3s 服務已啟動"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done
    echo ""
    
    if [ $attempt -eq $max_attempts ]; then
        print_error "k3s 服務啟動失敗"
        print_info "查看日誌: journalctl -u k3s -n 50 --no-pager"
        exit 1
    fi
    
    # 等待 k3s ready
    print_info "等待 k3s 就緒..."
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if kubectl get node >/dev/null 2>&1; then
            print_success "k3s 已就緒"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done
    echo ""
}

###############################################################################
# 驗證安裝
###############################################################################

verify_installation() {
    print_step "6/7" "驗證安裝"
    
    # 檢查版本
    print_info "檢查 k3s 版本..."
    k3s --version
    
    # 檢查節點狀態
    print_info "檢查節點狀態..."
    kubectl get node -o wide
    
    # 檢查系統 Pod
    print_info "檢查系統 Pod..."
    kubectl get pods -n kube-system
    
    # 檢查服務狀態
    print_info "檢查服務狀態..."
    systemctl status k3s --no-pager -l
    
    print_success "k3s 安裝驗證通過"
}

###############################################################################
# 配置 kubectl
###############################################################################

configure_kubectl() {
    print_step "7/7" "配置 kubectl"
    
    # 確保 kubeconfig 存在
    if [ ! -f /etc/rancher/k3s/k3s.yaml ]; then
        print_error "kubeconfig 不存在"
        exit 1
    fi
    
    # 創建目錄
    mkdir -p /root/.kube
    
    # 複製 kubeconfig
    cp /etc/rancher/k3s/k3s.yaml /root/.kube/config
    chmod 600 /root/.kube/config
    
    # 為非 root 用戶配置
    if [ -n "${SUDO_USER:-}" ]; then
        mkdir -p "/home/${SUDO_USER}/.kube"
        cp /etc/rancher/k3s/k3s.yaml "/home/${SUDO_USER}/.kube/config"
        chown -R "${SUDO_USER}:${SUDO_USER}" "/home/${SUDO_USER}/.kube"
    fi
    
    print_success "kubectl 配置完成"
    print_info "測試 kubectl: kubectl get nodes"
    kubectl get nodes
}

###############################################################################
# 安裝完成總結
###############################################################################

print_summary() {
    print_header "安裝完成"
    
    echo -e "${GREEN}✓ k3s 安裝成功！${NC}"
    echo ""
    echo "安裝信息:"
    echo "  k3s 版本: ${K3S_VERSION}"
    echo "  安裝目錄: ${K3S_INSTALL_DIR}"
    echo "  配置目錄: ${K3S_CONFIG_DIR}"
    echo "  數據目錄: ${K3S_DATA_DIR}"
    echo ""
    echo "網路配置:"
    echo "  Pod CIDR: ${K3S_CLUSTER_CIDR}"
    echo "  Service CIDR: ${K3S_SERVICE_CIDR}"
    echo "  Cluster DNS: ${K3S_CLUSTER_DNS}"
    echo ""
    echo "常用命令:"
    echo "  kubectl get nodes                    # 查看節點"
    echo "  kubectl get pods -A                  # 查看所有 Pods"
    echo "  kubectl get svc -A                   # 查看所有 Services"
    echo "  systemctl status k3s                 # 查看服務狀態"
    echo "  journalctl -u k3s -f                 # 查看 k3s 日誌"
    echo ""
    echo "下一步:"
    echo "  ./03_deploy_gl_backend.sh            # 部署 GL-Native Backend"
    echo ""
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native k3s 安裝腳本 (單節點環境)"
    echo ""
    
    # 解析參數
    for arg in "$@"; do
        case $arg in
            --version=*)
                K3S_VERSION="${arg#*=}"
                shift
                ;;
            --air-gapped)
                AIR_GAPPED=true
                INSTALL_MODE="air-gapped"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --version=VERSION    指定 k3s 版本 (默認: v1.28.3+k3s2)"
                echo "  --air-gapped         離線安裝模式"
                echo "  --help, -h           顯示此幫助信息"
                echo ""
                echo "環境變數:"
                echo "  K3S_VERSION          k3s 版本"
                echo "  K3S_INSTALL_DIR      安裝目錄 (默認: /usr/local/bin)"
                echo "  K3S_CONFIG_DIR       配置目錄 (默認: /etc/rancher/k3s)"
                echo "  K3S_DATA_DIR         數據目錄 (默認: /var/lib/rancher/k3s)"
                exit 0
                ;;
        esac
    done
    
    # 執行安裝步驟
    pre_install_check
    install_dependencies
    download_k3s
    configure_k3s
    install_k3s_service
    start_k3s
    verify_installation
    configure_kubectl
    print_summary
    
    exit 0
}

# 執行主函數
main "$@"