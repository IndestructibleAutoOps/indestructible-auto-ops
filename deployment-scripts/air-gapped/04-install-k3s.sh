#!/bin/bash
#
# GL-Native Execution Backend - k3s 離線安裝腳本
#
# 用途：在離線環境中安裝 k3s
# 使用方式：./04_install_k3s.sh [選項]
#

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

K3S_VERSION=${K3S_VERSION:-"v1.28.3+k3s2"}
BUNDLE_DIR=${BUNDLE_DIR:-"/tmp/offline"}
REGISTRY_URL=${REGISTRY_URL:-"http://localhost:5000"}
UPGRADE=${UPGRADE:-false}

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

main() {
    print_header "GL-Native k3s 離線安裝腳本"
    echo ""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --version=*)
                K3S_VERSION="${1#*=}"
                shift
                ;;
            --bundle-dir=*)
                BUNDLE_DIR="${1#*=}"
                shift
                ;;
            --registry-url=*)
                REGISTRY_URL="${1#*=}"
                shift
                ;;
            --upgrade)
                UPGRADE=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                exit 0
                ;;
        esac
    done
    
    # 檢查 k3s 二進制文件
    if [ ! -f "$BUNDLE_DIR/binaries/k3s" ]; then
        print_error "k3s 二進制文件不存在: $BUNDLE_DIR/binaries/k3s"
        exit 1
    fi
    
    # 檢查現有 k3s
    if command -v k3s > /dev/null 2>&amp;1; then
        local existing_version=$(k3s --version 2>/dev/null | head -1)
        print_warning "檢測到 k3s 已安裝: $existing_version"
        
        if [ "$UPGRADE" = false ]; then
            print_error "如果要重新安裝，請使用 --upgrade"
            exit 1
        fi
    fi
    
    # 複製 k3s 二進制文件
    print_info "安裝 k3s ${K3S_VERSION}..."
    cp "$BUNDLE_DIR/binaries/k3s" /usr/local/bin/k3s
    chmod +x /usr/local/bin/k3s
    
    # 創建符號連結
    ln -sf /usr/local/bin/k3s /usr/local/bin/crictl
    ln -sf /usr/local/bin/k3s /usr/local/bin/kubectl
    
    # 配置 k3s
    mkdir -p /etc/rancher/k3s
    cat > /etc/rancher/k3s/config.yaml <<EOF
# GL-Native k3s 配置
# 版本: ${K3S_VERSION}
# 離線模式: 是

# Registry 配置
EOF
    
    # 配置使用本地 registry
    if [ -n "$REGISTRY_URL" ]; then
        cat >> /etc/rancher/k3s/config.yaml <<EOF
mirrors:
  "docker.io":
    endpoint:
      - "${REGISTRY_URL}"
  "registry.k8s.io":
    endpoint:
      - "${REGISTRY_URL}"
EOF
    fi
    
    # 啟動 k3s
    print_info "啟動 k3s 服務..."
    INSTALL_K3S_SKIP_DOWNLOAD=true \
    INSTALL_K3S_EXEC="--config /etc/rancher/k3s/config.yaml" \
    INSTALL_K3S_VERSION="${K3S_VERSION}" \
    bash "$BUNDLE_DIR/scripts/install.sh"
    
    # 等待 k3s 啟動
    print_info "等待 k3s 啟動..."
    sleep 10
    
    # 驗證安裝
    if kubectl get nodes > /dev/null 2>&amp;1; then
        print_success "k3s 安裝成功"
        kubectl get nodes
    else
        print_error "k3s 安裝失敗"
        print_info "查看日誌: journalctl -u k3s -n 50"
        exit 1
    fi
    
    print_header "k3s 安裝完成"
    echo -e "${GREEN}✓ k3s ${K3S_VERSION} 安裝成功！${NC}"
    echo ""
    echo "下一步:"
    echo "  ./05_deploy_gl_backend.sh"
    echo ""
    
    exit 0
}

main "$@"