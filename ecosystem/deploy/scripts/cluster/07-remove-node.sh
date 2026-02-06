#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 節點移除腳本 (叢集環境)
#
# 用途：從叢集中安全移除節點
# 使用方式：./07_remove_node.sh --node-name NAME [--force]
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NODE_NAME=${NODE_NAME:-""}
FORCE=${FORCE:-false}
KUBECTL_CMD=${KUBECTL_CMD:-"kubectl"}

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

confirm_action() {
    local message="$1"
    read -p "$message [y/N]: " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

main() {
    print_header "GL-Native Node Removal Script"
    echo ""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --node-name=*)
                NODE_NAME="${1#*=}"
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo "  --node-name=NAME    節點名稱 [必需]"
                echo "  --force            強制移除"
                exit 0
                ;;
        esac
    done
    
    if [ -z "$NODE_NAME" ]; then
        print_error "必須指定節點名稱: --node-name"
        exit 1
    fi
    
    # Check if node exists
    if ! kubectl get node "$NODE_NAME" > /dev/null 2>&1; then
        print_error "節點不存在: $NODE_NAME"
        exit 1
    fi
    
    print_warning "即將從叢集中移除節點: $NODE_NAME"
    print_info "這將:"
    echo "  1. 驅逐節點上的所有 Pods"
    echo "  2. 標記節點為不可調度"
    echo "  3. 從叢集中移除節點"
    echo ""
    
    if [ "$FORCE" = false ]; then
        if ! confirm_action "確定要移除節點嗎?"; then
            print_info "取消移除"
            exit 0
        fi
    fi
    
    # Cordon node
    print_info "標記節點為不可調度..."
    kubectl cordon "$NODE_NAME"
    print_success "節點已標記為不可調度"
    
    # Drain node
    print_info "驅逐節點上的 Pods..."
    kubectl drain "$NODE_NAME" --ignore-daemonsets --delete-emptydir-data --force --grace-period=30
    print_success "Pods 已驅逐"
    
    # Delete node
    print_info "從叢集中移除節點..."
    kubectl delete node "$NODE_NAME"
    print_success "節點已移除"
    
    print_header "Node Removal Complete"
    echo -e "${GREEN}✓ 節點 $NODE_NAME 已成功移除！${NC}"
    echo ""
    echo "後續步驟:"
    echo "  1. 在節點上執行: sudo systemctl stop k3s-agent"
    echo "  2. 在節點上執行: sudo /usr/local/bin/k3s-agent-uninstall.sh"
    echo "  3. 或重新加入叢集: ./03_join_worker_node.sh"
    echo ""
    
    exit 0
}

main "$@"