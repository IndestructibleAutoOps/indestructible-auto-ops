#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 本地 Registry 設置腳本
#
# 用途：設置和配置本地 Docker Registry 用於離線環境
# 使用方式：./03_setup_registry.sh [選項]
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REGISTRY_PORT=${REGISTRY_PORT:-5000}
REGISTRY_DATA_DIR=${REGISTRY_DATA_DIR:-"/var/lib/registry"}
REGISTRY_IMAGE=${REGISTRY_IMAGE:-"registry:2"}
AUTH_ENABLE=${AUTH_ENABLE:-false}
AUTH_FILE=${AUTH_FILE:-"/etc/docker/registry/htpasswd"}
USERNAME=${USERNAME:-"admin"}
PASSWORD=${PASSWORD:-"admin123"}

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

create_auth() {
    if [ "$AUTH_ENABLE" = false ]; then
        return 0
    fi
    
    print_info "創建 Registry 認證..."
    
    if ! command -v htpasswd > /dev/null 2>&1; then
        print_warning "htpasswd 未安裝，嘗試安裝..."
        apt-get update && apt-get install -y apache2-utils || \
        yum install -y httpd-tools
    fi
    
    mkdir -p "$(dirname "$AUTH_FILE")"
    htpasswd -Bbn "$USERNAME" "$PASSWORD" > "$AUTH_FILE"
    
    print_success "認證創建完成"
    print_info "用戶名: $USERNAME"
}

main() {
    print_header "GL-Native 本地 Registry 設置"
    echo ""
    
    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            --port=*)
                REGISTRY_PORT="${1#*=}"
                shift
                ;;
            --data-dir=*)
                REGISTRY_DATA_DIR="${1#*=}"
                shift
                ;;
            --auth)
                AUTH_ENABLE=true
                shift
                ;;
            --username=*)
                USERNAME="${1#*=}"
                shift
                ;;
            --password=*)
                PASSWORD="${1#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                exit 0
                ;;
        esac
    done
    
    # 停止現有 registry
    if docker ps -a | grep -q "registry"; then
        print_warning "Registry 已存在，停止並刪除..."
        docker stop registry || true
        docker rm registry || true
    fi
    
    # 創建數據目錄
    mkdir -p "$REGISTRY_DATA_DIR"
    
    # 創建認證
    create_auth
    
    # 啟動 registry
    print_info "啟動 Docker Registry..."
    
    if [ "$AUTH_ENABLE" = true ]; then
        docker run -d \
            -p "${REGISTRY_PORT}:5000" \
            --restart=always \
            --name registry \
            -v "$REGISTRY_DATA_DIR":/var/lib/registry \
            -v "$AUTH_FILE":/auth/htpasswd \
            -e "REGISTRY_AUTH=htpasswd" \
            -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
            -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
            "$REGISTRY_IMAGE"
    else
        docker run -d \
            -p "${REGISTRY_PORT}:5000" \
            --restart=always \
            --name registry \
            -v "$REGISTRY_DATA_DIR":/var/lib/registry \
            "$REGISTRY_IMAGE"
    fi
    
    sleep 5
    
    # 驗證 registry
    if curl -s "http://localhost:${REGISTRY_PORT}/v2/_catalog" > /dev/null; then
        print_success "Registry 啟動成功"
        print_info "Registry URL: http://localhost:${REGISTRY_PORT}"
    else
        print_error "Registry 啟動失敗"
        exit 1
    fi
    
    # 配置 k3s 使用本地 registry
    print_info "配置 k3s 使用本地 registry..."
    mkdir -p /etc/rancher/k3s
    cat > /etc/rancher/k3s/registries.yaml <<EOF
mirrors:
  "docker.io":
    endpoint:
      - "http://localhost:${REGISTRY_PORT}"
  "registry.k8s.io":
    endpoint:
      - "http://localhost:${REGISTRY_PORT}"
EOF
    
    print_success "k3s registry 配置完成"
    
    # 登錄到 registry
    if [ "$AUTH_ENABLE" = true ]; then
        print_info "登錄到 registry..."
        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin "localhost:${REGISTRY_PORT}"
        print_success "登錄成功"
    fi
    
    print_header "Registry 設置完成"
    echo -e "${GREEN}✓ 本地 Registry 設置成功！${NC}"
    echo ""
    echo "Registry 信息:"
    echo "  URL: http://localhost:${REGISTRY_PORT}"
    echo "  Data: $REGISTRY_DATA_DIR"
    echo "  Auth: $AUTH_ENABLE"
    echo ""
    
    exit 0
}

main "$@"