#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 離線環境資源導入腳本
#
# 用途：在離線環境中導入並安裝所有部署所需的資源
# 使用方式：./02_import_resources.sh --bundle-dir DIR
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BUNDLE_DIR=${BUNDLE_DIR:-""}
REGISTRY_URL=${REGISTRY_URL:-"http://localhost:5000"}
VERIFY=${VERIFY:-true}
START_REGISTRY=${START_REGISTRY:-true}

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
    print_header "GL-Native 離線環境資源導入腳本"
    echo ""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --bundle-dir=*)
                BUNDLE_DIR="${1#*=}"
                shift
                ;;
            --registry-url=*)
                REGISTRY_URL="${1#*=}"
                shift
                ;;
            --skip-registry)
                START_REGISTRY=false
                shift
                ;;
            --skip-verify)
                VERIFY=false
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                exit 0
                ;;
        esac
    done
    
    if [ -z "$BUNDLE_DIR" ]; then
        print_error "必須指定 bundle 目錄: --bundle-dir"
        exit 1
    fi
    
    # 驗證 bundle
    if [ "$VERIFY" = true ]; then
        print_step "1/4" "驗證 bundle 完整性"
        cd "$BUNDLE_DIR"
        sha256sum -c sha256sum.txt || exit 1
        cd - > /dev/null
        print_success "Bundle 驗證通過"
    fi
    
    # 啟動 registry
    if [ "$START_REGISTRY" = true ]; then
        print_step "2/4" "啟動本地 Registry"
        docker run -d -p 5000:5000 --restart=always --name registry registry:2
        sleep 5
        print_success "Registry 啟動成功"
    fi
    
    # 導入 images
    print_step "3/4" "導入 Docker Images"
    for tar in "$BUNDLE_DIR"/images/*.tar; do
        print_info "導入: $(basename "$tar")"
        docker load -i "$tar"
    done
    print_success "Docker Images 導入完成"
    
    # 安裝二進制文件
    print_step "4/4" "安裝二進制文件"
    cp "$BUNDLE_DIR/binaries/k3s" /usr/local/bin/k3s
    chmod +x /usr/local/bin/k3s
    cp "$BUNDLE_DIR/binaries/kubectl" /usr/local/bin/kubectl
    chmod +x /usr/local/bin/kubectl
    print_success "二進制文件安裝完成"
    
    print_header "資源導入完成"
    echo -e "${GREEN}✓ 所有資源導入成功！${NC}"
    exit 0
}

main "$@"