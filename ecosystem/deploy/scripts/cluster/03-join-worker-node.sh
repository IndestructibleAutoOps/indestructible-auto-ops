#!/bin/bash

###############################################################################
# GL-Native Execution Backend - Worker 節點加入腳本 (叢集環境)
#
# 用途：將 Worker 節點加入 k3s 叢集
# 使用方式：./03_join_worker_node.sh --server-url URL --token TOKEN [選項]
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

# 連接配置
SERVER_URL=${SERVER_URL:-""}
TOKEN=${TOKEN:-""}

# 節點配置
NODE_NAME=${NODE_NAME:-$(hostname)}
NODE_LABELS=${NODE_LABELS:-""}
NODE_TAINTS=${NODE_TAINTS:-""}

# 運行模式
UPGRADE=${UPGRADE:-false}

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

pre_join_check() {
    print_header "加入前置檢查"
    
    # 檢查 root 權限
    if [ "$EUID" -ne 0 ]; then 
        print_error "請使用 root 權限執行此腳本"
        exit 1
    fi
    
    # 檢查必要參數
    if [ -z "$SERVER_URL" ]; then
        print_error "必須指定伺服器 URL: --server-url"
        exit 1
    fi
    
    if [ -z "$TOKEN" ]; then
        print_error "必須指定 token: --token"
        print_info "從控制平面節點獲取 token: cat /var/lib/rancher/k3s/server/node-token"
        exit 1
    fi
    
    # 檢查現有 k3s
    if command -v k3s > /dev/null 2>&1; then
        local existing_version=$(k3s --version 2>/dev/null | head -1)
        print_warning "檢測到 k3s 已安裝: $existing_version"
        
        if [ "$UPGRADE" = false ]; then
            print_error "如果重新加入，請使用 --upgrade 或先卸載"
            exit 1
        fi
    fi
    
    # 測試伺服器連接
    print_info "測試伺服器連接..."
    local server_host=$(echo "$SERVER_URL" | sed -e 's|^[^/]*//||' -e 's|/.*$||' -e 's|:.*$||')
    if ! ping -c 1 -W 3 "$server_host" > /dev/null 2>&1; then
        print_error "無法連接到伺服器: $server_host"
        print_info "請檢查網路連接和防火牆設置"
        exit 1
    fi
    
    print_success "前置檢查通過"
}

###############################################################################
# 安裝依賴
###############################################################################

install_dependencies() {
    print_step "1/6" "安裝依賴套件"
    
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
    print_step "2/6" "下載 k3s"
    
    K3S_BIN_URL="https://github.com/k3s-io/k3s/releases/download/${K3S_VERSION}/k3s"
    
    print_info "下載 k3s ${K3S_VERSION}..."
    wget -q --show-progress --progress=bar:force -O "${K3S_INSTALL_DIR}/k3s" "${K3S_BIN_URL}"
    
    chmod +x "${K3S_INSTALL_DIR}/k3s"
    ln -sf "${K3S_INSTALL_DIR}/k3s" /usr/local/bin/crictl
    ln -sf "${K3S_INSTALL_DIR}/k3s" /usr/local/bin/kubectl
    
    print_success "k3s 下載完成"
}

###############################################################################
# 創建 Worker 節點配置
###############################################################################

create_worker_config() {
    print_step "3/6" "創建 Worker 節點配置"
    
    mkdir -p "${K3S_CONFIG_DIR}"
    
    cat > "${K3S_CONFIG_DIR}/config.yaml" <<EOF
# GL-Native k3s Worker 節點配置
# 節點名稱: ${NODE_NAME}
# 版本: ${K3S_VERSION}

# 節點配置
node-name: ${NODE_NAME}

# 日誌配置
log: /var/log/k3s.log

# 數據存儲
data-dir: ${K3S_DATA_DIR}

# 寫入 kubeconfig 權限
write-kubeconfig-mode: "0640"
EOF
    
    # 添加節點標籤
    if [ -n "$NODE_LABELS" ]; then
        print_info "添加節點標籤: $NODE_LABELS"
        echo "" >> "${K3S_CONFIG_DIR}/config.yaml"
        echo "# 節點標籤" >> "${K3S_CONFIG_DIR}/config.yaml"
        echo "node-label:" >> "${K3S_CONFIG_DIR}/config.yaml"
        IFS=',' read -ra LABELS <<< "$NODE_LABELS"
        for label in "${LABELS[@]}"; do
            echo "  - &quot;$label&quot;" >> "${K3S_CONFIG_DIR}/config.yaml"
        done
    fi
    
    # 添加節點污點
    if [ -n "$NODE_TAINTS" ]; then
        print_info "添加節點污點: $NODE_TAINTS"
        echo "" >> "${K3S_CONFIG_DIR}/config.yaml"
        echo "# 節點污點" >> "${K3S_CONFIG_DIR}/config.yaml"
        echo "node-taint:" >> "${K3S_CONFIG_DIR}/config.yaml"
        IFS=',' read -ra TAINTS <<< "$NODE_TAINTS"
        for taint in "${TAINTS[@]}"; do
            echo "  - &quot;$taint&quot;" >> "${K3S_CONFIG_DIR}/config.yaml"
        done
    fi
    
    print_success "Worker 節點配置創建完成"
}

###############################################################################
# 加入叢集
###############################################################################

join_cluster() {
    print_step "4/6" "加入叢集"
    
    print_info "連接到: $SERVER_URL"
    print_info "節點名稱: $NODE_NAME"
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
K3S_NODE_NAME=${NODE_NAME}
EOF
    
    print_info "加入叢集..."
    INSTALL_K3S_SKIP_DOWNLOAD=true \
    INSTALL_K3S_EXEC="--config ${K3S_CONFIG_DIR}/config.yaml --server ${SERVER_URL} --token ${TOKEN}" \
    INSTALL_K3S_VERSION="${K3S_VERSION}" \
    K3S_TOKEN="${TOKEN}" \
    K3S_URL="${SERVER_URL}" \
    K3S_NODE_NAME="${NODE_NAME}" \
    bash /tmp/k3s-install.sh
    
    print_success "Worker 節點加入完成"
}

###############################################################################
# 啟動 k3s Agent
###############################################################################

start_k3s_agent() {
    print_step "5/6" "啟動 k3s Agent 服務"
    
    systemctl enable k3s-agent
    systemctl start k3s-agent
    
    print_info "等待 k3s Agent 啟動..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if systemctl is-active --quiet k3s-agent; then
            print_success "k3s Agent 服務已啟動"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done
    echo ""
    
    if [ $attempt -eq $max_attempts ]; then
        print_error "k3s Agent 服務啟動失敗"
        print_info "查看日誌: journalctl -u k3s-agent -n 50 --no-pager"
        exit 1
    fi
    
    # 等待節點註冊
    print_info "等待節點註冊..."
    max_attempts=60
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if systemctl is-active --quiet k3s-agent; then
            # 檢查日誌中是否有節點就緒信息
            if journalctl -u k3s-agent -n 20 --no-pager | grep -q "Node is ready"; then
                print_success "節點已註冊並就緒"
                break
            fi
        fi
        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done
    echo ""
}

###############################################################################
# 驗證節點加入
###############################################################################

verify_node_join() {
    print_step "6/6" "驗證節點加入"
    
    print_info "檢查 k3s Agent 版本..."
    k3s-agent --version 2>/dev/null || k3s --version
    
    print_info "檢查服務狀態..."
    systemctl status k3s-agent --no-pager -l
    
    print_info "檢查節點連接狀態..."
    local node_status=$(journalctl -u k3s-agent -n 30 --no-pager | grep -i "node" | tail -5)
    echo "$node_status"
    
    print_info "檢查最近的日誌..."
    journalctl -u k3s-agent -n 20 --no-pager
    
    print_success "Worker 節點驗證完成"
    print_info "請在控制平面節點上運行 'kubectl get nodes' 查看節點狀態"
}

###############################################################################
# 加入完成總結
###############################################################################

print_summary() {
    print_header "Worker 節點加入完成"
    
    echo -e "${GREEN}✓ Worker 節點加入成功！${NC}"
    echo ""
    echo "節點信息:"
    echo "  節點名稱: ${NODE_NAME}"
    echo "  連接到: ${SERVER_URL}"
    echo "  k3s 版本: ${K3S_VERSION}"
    echo ""
    echo "驗證節點狀態:"
    echo "  在控制平面節點上運行:"
    echo "    kubectl get nodes"
    echo "    kubectl describe node ${NODE_NAME}"
    echo ""
    echo "查看日誌:"
    echo "  journalctl -u k3s-agent -f"
    echo "  tail -f /var/log/k3s.log"
    echo ""
    echo "節點服務:"
    echo "  systemctl status k3s-agent"
    echo "  systemctl restart k3s-agent"
    echo ""
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native Worker 節點加入腳本 (叢集環境)"
    echo ""
    
    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            --server-url=*)
                SERVER_URL="${1#*=}"
                shift
                ;;
            --token=*)
                TOKEN="${1#*=}"
                shift
                ;;
            --node-name=*)
                NODE_NAME="${1#*=}"
                shift
                ;;
            --node-labels=*)
                NODE_LABELS="${1#*=}"
                shift
                ;;
            --node-taints=*)
                NODE_TAINTS="${1#*=}"
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
                echo "  --server-url=URL        伺服器 URL [必需]"
                echo "  --token=TOKEN           節點 Token [必需]"
                echo "  --node-name=NAME        節點名稱"
                echo "  --node-labels=LABELS    節點標籤 (逗號分隔)"
                echo "  --node-taints=TAINTS    節點污點 (逗號分隔)"
                echo "  --upgrade               升級模式"
                echo "  --help, -h              顯示此幫助信息"
                echo ""
                echo "環境變數:"
                echo "  K3S_VERSION             k3s 版本 (默認: v1.28.3+k3s2)"
                echo ""
                echo "範例:"
                echo "  ./03_join_worker_node.sh \&quot;
                echo "    --server-url https://192.168.1.11:6443 \&quot;
                echo "    --token K10b7c... \&quot;
                echo "    --node-name worker-1 \&quot;
                echo "    --node-labels 'node-type=worker,zone=prod'"
                exit 0
                ;;
            *)
                print_error "未知選項: $1"
                exit 1
                ;;
        esac
    done
    
    # 執行加入步驟
    pre_join_check
    install_dependencies
    download_k3s
    create_worker_config
    join_cluster
    start_k3s_agent
    verify_node_join
    print_summary
    
    exit 0
}

# 執行主函數
main "$@"