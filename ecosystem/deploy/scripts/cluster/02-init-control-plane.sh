#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 控制平面初始化腳本 (叢集環境)
#
# 用途：初始化 k3s 控制平面節點（第一個節點或額外節點）
# 使用方式：./02_init_control_plane.sh --role first-server|additional-server [選項]
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

# 叢集配置
CLUSTER_CIDR=${CLUSTER_CIDR:-"10.42.0.0/16"}
SERVICE_CIDR=${SERVICE_CIDR:-"10.43.0.0/16"}
CLUSTER_DNS=${CLUSTER_DNS:-"10.43.0.10"}

# TLS SAN 配置
TLS_SAN=${TLS_SAN:-""}
NODE_NAME=${NODE_NAME:-$(hostname)}

# 伺服器配置
SERVER_URL=${SERVER_URL:-""}
TOKEN=${TOKEN:-""}

# 運行模式
ROLE=${ROLE:-""}
UPGRADE=${UPGRADE:-false}

# 網路配置
BIND_ADDRESS=${BIND_ADDRESS:-"0.0.0.0"}
ADVERTISE_ADDRESS=${ADVERTISE_ADDRESS:-$(hostname -I | awk '{print $1}')}

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

confirm_action() {
    local message="$1"
    read -p "$message [y/N]: " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

###############################################################################
# 前置檢查
###############################################################################

pre_init_check() {
    print_header "初始化前置檢查"
    
    # 檢查 root 權限
    if [ "$EUID" -ne 0 ]; then 
        print_error "請使用 root 權限執行此腳本"
        exit 1
    fi
    
    # 檢查角色
    if [ -z "$ROLE" ]; then
        print_error "必須指定角色: --role first-server|additional-server"
        exit 1
    fi
    
    # 檢查現有 k3s
    if command -v k3s > /dev/null 2>&1; then
        local existing_version=$(k3s --version 2>/dev/null | head -1)
        print_warning "檢測到 k3s 已安裝: $existing_version"
        
        if [ "$UPGRADE" = false ]; then
            print_error "如果重新安裝，請使用 --upgrade 或先卸載"
            exit 1
        fi
    fi
    
    # 如果是額外控制平面節點，檢查必要參數
    if [ "$ROLE" = "additional-server" ]; then
        if [ -z "$SERVER_URL" ]; then
            print_error "額外控制平面節點需要 --server-url"
            exit 1
        fi
        
        if [ -z "$TOKEN" ]; then
            print_error "額外控制平面節點需要 --token"
            print_info "從第一個控制平面節點獲取 token: cat /var/lib/rancher/k3s/server/node-token"
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
            apt-get update -qq
            apt-get install -y -qq curl wget ca-certificates iptables arptables ebtables
            update-alternatives --set iptables /usr/sbin/iptables-legacy 2>/dev/null || true
            update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy 2>/dev/null || true
            ;;
        rhel|rocky|centos)
            yum install -y -q curl wget ca-certificates iptables arptables ebtables
            ;;
    esac
    
    # 加載 kernel 模組
    modprobe br_netfilter 2>/dev/null || true
    modprobe overlay 2>/dev/null || true
    
    cat > /etc/modules-load.d/k3s.conf <<EOF
br_netfilter
overlay
EOF
    
    # 配置 sysctl
    cat > /etc/sysctl.d/99-k3s.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
    sysctl --system > /dev/null
    
    # 關閉 swap
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
    wget -q --show-progress --progress=bar:force -O "${K3S_INSTALL_DIR}/k3s" "${K3S_BIN_URL}"
    
    chmod +x "${K3S_INSTALL_DIR}/k3s"
    ln -sf "${K3S_INSTALL_DIR}/k3s" /usr/local/bin/crictl
    ln -sf "${K3S_INSTALL_DIR}/k3s" /usr/local/bin/kubectl
    
    print_success "k3s 下載完成"
}

###############################################################################
# 創建控制平面配置
###############################################################################

create_control_plane_config() {
    print_step "3/7" "創建控制平面配置"
    
    mkdir -p "${K3S_CONFIG_DIR}"
    
    # 創建 TLS SAN 列表
    local tls_san_list="$NODE_NAME"
    tls_san_list+=",$(hostname -f)"
    tls_san_list+=",$ADVERTISE_ADDRESS"
    tls_san_list+=",127.0.0.1"
    tls_san_list+=",localhost"
    
    if [ -n "$TLS_SAN" ]; then
        tls_san_list+=",$TLS_SAN"
    fi
    
    cat > "${K3S_CONFIG_DIR}/config.yaml" <<EOF
# GL-Native k3s 控制平面配置
# 節點角色: ${ROLE}
# 版本: ${K3S_VERSION}

# 網路配置
cluster-cidr: ${CLUSTER_CIDR}
service-cidr: ${SERVICE_CIDR}
cluster-dns: ${CLUSTER_DNS}
bind-address: ${BIND_ADDRESS}
advertise-address: ${ADVERTISE_ADDRESS}
node-name: ${NODE_NAME}

# TLS SAN
tls-san:
EOF
    
    # 添加 TLS SAN 列表
    IFS=',' read -ra SAN_LIST <<< "$tls_san_list"
    for san in "${SAN_LIST[@]}"; do
        echo "  - $san" >> "${K3S_CONFIG_DIR}/config.yaml"
    done
    
    cat >> "${K3S_CONFIG_DIR}/config.yaml" <<EOF

# 禁用組件
disable:
  - local-storage
  - metrics-server  # 如果需要 metrics，請註釋此行

# 啟用組件
enable-features:
  - EphemeralContainers

# 日誌配置
log: /var/log/k3s.log

# 數據存儲
data-dir: ${K3S_DATA_DIR}

# 寫入 kubeconfig 權限
write-kubeconfig-mode: "0644"

# 標籤和污點
node-label:
  - "node-role.kubernetes.io/master=true"
  - "node.kubernetes.io/role=control-plane"
EOF
    
    print_success "控制平面配置創建完成"
}

###############################################################################
# 初始化第一個控制平面節點
###############################################################################

init_first_server() {
    print_step "4/7" "初始化第一個控制平面節點"
    
    # 下載 k3s 安裝腳本
    curl -sfL https://get.k3s.io -o /tmp/k3s-install.sh
    chmod +x /tmp/k3s-install.sh
    
    # 創建環境變數檔案
    cat > /etc/systemd/system/k3s.service.env <<EOF
# GL-Native k3s 環境變數
INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml --cluster-init"
K3S_VERSION=${K3S_VERSION}
EOF
    
    print_info "安裝第一個控制平面節點..."
    INSTALL_K3S_SKIP_DOWNLOAD=true \
    INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml --cluster-init" \
    INSTALL_K3S_VERSION="${K3S_VERSION}" \
    bash /tmp/k3s-install.sh
    
    print_success "第一個控制平面節點初始化完成"
    
    # 獲取並顯示 token
    local token=$(cat /var/lib/rancher/k3s/server/node-token)
    print_header "節點 Token"
    print_info "Token: $token"
    print_info "請保存此 token，其他節點加入叢集時需要使用"
    print_info "保存到檔案: /tmp/k3s-node-token.txt"
    echo "$token" > /tmp/k3s-node-token.txt
    chmod 600 /tmp/k3s-node-token.txt
}

###############################################################################
# 加入額外控制平面節點
###############################################################################

join_additional_server() {
    print_step "4/7" "加入額外控制平面節點"
    
    print_info "連接到: $SERVER_URL"
    print_info "Token: ${TOKEN:0:20}..."
    
    # 下載 k3s 安裝腳本
    curl -sfL https://get.k3s.io -o /tmp/k3s-install.sh
    chmod +x /tmp/k3s-install.sh
    
    # 創建環境變數檔案
    cat > /etc/systemd/system/k3s.service.env <<EOF
# GL-Native k3s 環境變數
INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml --server ${SERVER_URL} --token ${TOKEN}"
K3S_VERSION=${K3S_VERSION}
K3S_TOKEN=${TOKEN}
K3S_URL=${SERVER_URL}
EOF
    
    print_info "加入叢集..."
    INSTALL_K3S_SKIP_DOWNLOAD=true \
    INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml --server ${SERVER_URL} --token ${TOKEN}" \
    INSTALL_K3S_VERSION="${K3S_VERSION}" \
    K3S_TOKEN="${TOKEN}" \
    K3S_URL="${SERVER_URL}" \
    bash /tmp/k3s-install.sh
    
    print_success "額外控制平面節點加入完成"
}

###############################################################################
# 啟動 k3s
###############################################################################

start_k3s() {
    print_step "5/7" "啟動 k3s 服務"
    
    systemctl enable k3s
    systemctl start k3s
    
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
        if kubectl get nodes > /dev/null 2>&1; then
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
# 驗證控制平面
###############################################################################

verify_control_plane() {
    print_step "6/7" "驗證控制平面"
    
    print_info "檢查 k3s 版本..."
    k3s --version
    
    print_info "檢查節點狀態..."
    kubectl get nodes -o wide
    
    print_info "檢查系統 Pods..."
    kubectl get pods -n kube-system
    
    print_info "檢查服務狀態..."
    systemctl status k3s --no-pager -l
    
    # 檢查 etcd 成員（如果是第一個節點）
    if [ "$ROLE" = "first-server" ]; then
        print_info "檢查 etcd 成員..."
        kubectl get endpoints -n kube-system kube-etcd || echo "etcd endpoints not ready yet"
    fi
    
    print_success "控制平面驗證通過"
}

###############################################################################
# 配置 kubectl
###############################################################################

configure_kubectl() {
    print_step "7/7" "配置 kubectl"
    
    if [ ! -f /etc/rancher/k3s/k3s.yaml ]; then
        print_error "kubeconfig 不存在"
        exit 1
    fi
    
    mkdir -p /root/.kube
    cp /etc/rancher/k3s/k3s.yaml /root/.kube/config
    chmod 600 /root/.kube/config
    
    if [ -n "${SUDO_USER:-}" ]; then
        mkdir -p "/home/${SUDO_USER}/.kube"
        cp /etc/rancher/k3s/k3s.yaml "/home/${SUDO_USER}/.kube/config"
        chown -R "${SUDO_USER}:${SUDO_USER}" "/home/${SUDO_USER}/.kube"
    fi
    
    print_success "kubectl 配置完成"
    kubectl get nodes
}

###############################################################################
# 初始化完成總結
###############################################################################

print_summary() {
    print_header "控制平面初始化完成"
    
    echo -e "${GREEN}✓ 控制平面節點初始化成功！${NC}"
    echo ""
    echo "節點信息:"
    echo "  角色: ${ROLE}"
    echo "  主機名: ${NODE_NAME}"
    echo "  IP 地址: ${ADVERTISE_ADDRESS}"
    echo "  k3s 版本: ${K3S_VERSION}"
    echo ""
    echo "叢集配置:"
    echo "  Pod CIDR: ${CLUSTER_CIDR}"
    echo "  Service CIDR: ${SERVICE_CIDR}"
    echo "  Cluster DNS: ${CLUSTER_DNS}"
    echo ""
    
    if [ "$ROLE" = "first-server" ]; then
        echo "節點 Token: $(cat /tmp/k3s-node-token.txt 2>/dev/null || echo 'N/A')"
        echo ""
        echo "添加額外控制平面節點:"
        echo "  sudo ./02_init_control_plane.sh --role additional-server \&quot;
        echo "    --server-url https://${ADVERTISE_ADDRESS}:6443 \&quot;
        echo "    --token \$(cat /tmp/k3s-node-token.txt)"
        echo ""
        echo "添加 Worker 節點:"
        echo "  sudo ./03_join_worker_node.sh \&quot;
        echo "    --server-url https://${ADVERTISE_ADDRESS}:6443 \&quot;
        echo "    --token \$(cat /tmp/k3s-node-token.txt)"
        echo ""
    fi
    
    echo "下一步:"
    echo "  ./04_install_cni.sh --plugin calico        # 安裝 CNI"
    echo "  ./05_deploy_gl_backend.sh                  # 部署 GL-Native Backend"
    echo "  ./06_health_check.sh                       # 健康檢查"
    echo ""
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native 控制平面初始化腳本 (叢集環境)"
    echo ""
    
    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            --role=*)
                ROLE="${1#*=}"
                shift
                ;;
            --server-url=*)
                SERVER_URL="${1#*=}"
                shift
                ;;
            --token=*)
                TOKEN="${1#*=}"
                shift
                ;;
            --tls-san=*)
                TLS_SAN="${1#*=}"
                shift
                ;;
            --node-name=*)
                NODE_NAME="${1#*=}"
                shift
                ;;
            --upgrade)
                UPGRADE=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --role=ROLE            節點角色 (first-server|additional-server) [必需]"
                echo "  --server-url=URL       伺服器 URL (額外節點需要)"
                echo "  --token=TOKEN          節點 Token (額外節點需要)"
                echo "  --tls-san=SAN          額外 TLS SAN"
                echo "  --node-name=NAME       節點名稱"
                echo "  --upgrade              升級模式"
                echo "  --help, -h             顯示此幫助信息"
                echo ""
                echo "環境變數:"
                echo "  K3S_VERSION            k3s 版本 (默認: v1.28.3+k3s2)"
                echo "  CLUSTER_CIDR           Pod CIDR (默認: 10.42.0.0/16)"
                echo "  SERVICE_CIDR           Service CIDR (默認: 10.43.0.0/16)"
                exit 0
                ;;
            *)
                print_error "未知選項: $1"
                exit 1
                ;;
        esac
    done
    
    # 執行初始化步驟
    pre_init_check
    install_dependencies
    download_k3s
    create_control_plane_config
    
    if [ "$ROLE" = "first-server" ]; then
        init_first_server
    elif [ "$ROLE" = "additional-server" ]; then
        join_additional_server
    else
        print_error "無效的角色: $ROLE"
        exit 1
    fi
    
    start_k3s
    verify_control_plane
    configure_kubectl
    print_summary
    
    exit 0
}

# 執行主函數
main "$@"