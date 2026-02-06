#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 卸載腳本 (單節點環境)
#
# 用途：卸載 k3s 和 GL-Native Execution Backend
# 使用方式：./05_uninstall.sh [--purge] [--namespace NAMESPACE]
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
NAMESPACE=${NAMESPACE:-"gl-native"}
PURGE=${PURGE:-false}
K3S_DATA_DIR=${K3S_DATA_DIR:-"/var/lib/rancher/k3s"}
K3S_CONFIG_DIR=${K3S_CONFIG_DIR:-"/etc/rancher/k3s"}
STORAGE_PATH=${STORAGE_PATH:-"/opt/gl-native/data"}

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

confirm_action() {
    local message="$1"
    local default="${2:-n}"
    
    if [ "$default" = "y" ]; then
        read -p "$message [Y/n]: " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Nn]$ ]]
    else
        read -p "$message [y/N]: " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]]
    fi
}

###############################################################################
# 卸載 GL-Native Backend
###############################################################################

uninstall_gl_backend() {
    print_header "卸載 GL-Native Execution Backend"
    
    # 檢查 Namespace 是否存在
    if ! kubectl get namespace "${NAMESPACE}" > /dev/null 2>&1; then
        print_info "Namespace ${NAMESPACE} 不存在，跳過"
        return 0
    fi
    
    print_warning "即將刪除 Namespace ${NAMESPACE} 及其所有資源"
    print_info "這將刪除:"
    echo "  - 所有 Pods"
    echo "  - 所有 Services"
    echo "  - 所有 ConfigMaps"
    echo "  - 所有 Secrets"
    echo "  - 所有 PVCs"
    echo ""
    
    if ! confirm_action "確定要刪除 GL-Native Backend嗎?"; then
        print_info "取消卸載 GL-Native Backend"
        return 0
    fi
    
    # 刪除 Namespace (級聯刪除所有資源)
    print_info "刪除 Namespace ${NAMESPACE}..."
    kubectl delete namespace "${NAMESPACE}" --timeout=60s
    
    # 等待刪除完成
    print_info "等待刪除完成..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if ! kubectl get namespace "${NAMESPACE}" > /dev/null 2>&1; then
            print_success "GL-Native Backend 已卸載"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done
    echo ""
    
    print_error "Namespace 刪除超時"
    print_info "請手動檢查: kubectl get namespace ${NAMESPACE}"
}

###############################################################################
# 卸載 k3s
###############################################################################

uninstall_k3s() {
    print_header "卸載 k3s"
    
    # 檢查 k3s 是否安裝
    if ! command -v k3s > /dev/null 2>&1; then
        print_info "k3s 未安裝，跳過"
        return 0
    fi
    
    print_warning "即將卸載 k3s"
    print_info "這將:"
    echo "  - 停止 k3s 服務"
    echo "  - 刪除 k3s 二進制文件"
    echo "  - 刪除 k3s 數據 (如果使用 --purge)"
    echo ""
    
    if ! confirm_action "確定要卸載 k3s嗎?"; then
        print_info "取消卸載 k3s"
        return 0
    fi
    
    # 如果使用 --purge，再次確認
    if [ "$PURGE" = true ]; then
        print_warning "這將永久刪除所有 k3s 數據和配置"
        if ! confirm_action "確定要完全清除 k3s嗎?"; then
            PURGE=false
        fi
    fi
    
    # 停止 k3s 服務
    print_info "停止 k3s 服務..."
    systemctl stop k3s 2>/dev/null || true
    systemctl disable k3s 2>/dev/null || true
    
    # 使用 k3s 卸載腳本
    if [ -f /usr/local/bin/k3s-uninstall.sh ]; then
        print_info "執行 k3s 卸載腳本..."
        if [ "$PURGE" = true ]; then
            K3S_DATA_DIR="${K3S_DATA_DIR}" /usr/local/bin/k3s-uninstall.sh 2>/dev/null || true
        else
            /usr/local/bin/k3s-uninstall.sh 2>/dev/null || true
        fi
    fi
    
    # 手動清理
    print_info "清理 k3s 文件..."
    
    # 刪除二進制文件
    rm -f /usr/local/bin/k3s 2>/dev/null || true
    rm -f /usr/local/bin/kubectl 2>/dev/null || true
    rm -f /usr/local/bin/crictl 2>/dev/null || true
    
    # 刪除符號連結
    rm -f /usr/local/bin/kubectl 2>/dev/null || true
    
    # 刪除服務文件
    rm -f /etc/systemd/system/k3s.service 2>/dev/null || true
    rm -f /etc/systemd/system/k3s.service.env 2>/dev/null || true
    
    # 重新載入 systemd
    systemctl daemon-reload
    
    # 如果使用 --purge，刪除數據和配置
    if [ "$PURGE" = true ]; then
        print_warning "刪除 k3s 數據和配置..."
        
        # 刪除數據目錄
        rm -rf "${K3S_DATA_DIR}" 2>/dev/null || true
        
        # 刪除配置目錄
        rm -rf "${K3S_CONFIG_DIR}" 2>/dev/null || true
        
        # 刪除 cgroup
        rm -rf /sys/fs/cgroup/kubepods 2>/dev/null || true
        
        # 刪除網路介面 (flannel)
        ip link delete flannel.1 2>/dev/null || true
        ip link delete cni0 2>/dev/null || true
        
        print_success "k3s 數據和配置已清除"
    else
        print_info "k3s 數據和配置保留在 ${K3S_DATA_DIR}"
    fi
    
    print_success "k3s 已卸載"
}

###############################################################################
# 清理存儲數據
###############################################################################

cleanup_storage() {
    print_header "清理存儲數據"
    
    if [ -d "${STORAGE_PATH}" ]; then
        print_info "存儲路徑: ${STORAGE_PATH}"
        local storage_size=$(du -sh "${STORAGE_PATH}" 2>/dev/null | cut -f1)
        print_info "存儲大小: ${storage_size}"
        
        if [ "$PURGE" = true ]; then
            print_warning "即將刪除存儲數據"
            if confirm_action "確定要刪除存儲數據嗎?"; then
                print_info "刪除存儲數據..."
                rm -rf "${STORAGE_PATH}"
                print_success "存儲數據已刪除"
            else
                print_info "保留存儲數據"
            fi
        else
            print_info "存儲數據保留在 ${STORAGE_PATH}"
        fi
    else
        print_info "存儲路徑不存在"
    fi
    
    # 清理日誌
    if [ -d "/var/log/gl-native" ]; then
        print_info "日誌路徑: /var/log/gl-native"
        
        if [ "$PURGE" = true ]; then
            print_info "刪除日誌..."
            rm -rf "/var/log/gl-native"
            print_success "日誌已刪除"
        fi
    fi
}

###############################################################################
# 清理網路配置
###############################################################################

cleanup_network() {
    print_header "清理網路配置"
    
    # 檢查 iptables 規則
    print_info "檢查 iptables 規則..."
    
    local k3s_chains=$(iptables -L -n 2>/dev/null | grep -i "Chain KUBE" | wc -l)
    
    if [ "$k3s_chains" -gt 0 ]; then
        print_warning "發現 $k3s_chains 個 k3s iptables chains"
        
        if [ "$PURGE" = true ]; then
            print_warning "清理 iptables 規則需要手動操作"
            print_info "請運行以下命令清理 iptables:"
            echo "  iptables -F"
            echo "  iptables -t nat -F"
            echo "  iptables -t mangle -F"
            echo "  iptables -X"
            echo "  iptables -t nat -X"
            echo "  iptables -t mangle -X"
            print_info "或重啟系統以自動清理"
        else
            print_info "保留 iptables 規則"
        fi
    else
        print_success "沒有發現 k3s iptables 規則"
    fi
}

###############################################################################
# 驗證卸載
###############################################################################

verify_uninstall() {
    print_header "驗證卸載"
    
    local all_clean=true
    
    # 檢查 k3s
    if command -v k3s > /dev/null 2>&1; then
        print_error "k3s 仍然存在"
        all_clean=false
    else
        print_success "k3s 已刪除"
    fi
    
    # 檢查 k3s 服務
    if systemctl list-unit-files | grep -q k3s.service; then
        print_error "k3s 服務仍然存在"
        all_clean=false
    else
        print_success "k3s 服務已刪除"
    fi
    
    # 檢查 Namespace
    if kubectl get namespace "${NAMESPACE}" > /dev/null 2>&1; then
        print_error "Namespace ${NAMESPACE} 仍然存在"
        all_clean=false
    else
        print_success "Namespace ${NAMESPACE} 已刪除"
    fi
    
    # 檢查數據目錄
    if [ "$PURGE" = true ]; then
        if [ -d "${K3S_DATA_DIR}" ]; then
            print_warning "k3s 數據目錄仍然存在: ${K3S_DATA_DIR}"
        else
            print_success "k3s 數據目錄已刪除"
        fi
        
        if [ -d "${STORAGE_PATH}" ]; then
            print_warning "存儲數據仍然存在: ${STORAGE_PATH}"
        else
            print_success "存儲數據已刪除"
        fi
    fi
    
    if [ "$all_clean" = true ]; then
        print_success "卸載驗證通過"
    else
        print_warning "部分組件仍然存在，請手動清理"
    fi
}

###############################################################################
# 卸載完成總結
###############################################################################

print_summary() {
    print_header "卸載完成"
    
    echo -e "${GREEN}✓ 卸載完成${NC}"
    echo ""
    echo "卸載摘要:"
    echo "  GL-Native Backend: 已卸載"
    echo "  k3s: 已卸載"
    echo "  Purge 模式: $PURGE"
    echo ""
    
    if [ "$PURGE" = false ]; then
        echo "保留的數據:"
        echo "  k3s 數據: ${K3S_DATA_DIR}"
        echo "  k3s 配置: ${K3S_CONFIG_DIR}"
        echo "  存儲數據: ${STORAGE_PATH}"
        echo "  日誌: /var/log/gl-native"
        echo ""
        echo "如果要完全清除所有數據，請重新運行:"
        echo "  $0 --purge"
    else
        echo "所有數據已清除"
    fi
    echo ""
    
    echo "如果需要重新安裝，請運行:"
    echo "  ./01_pre_install_check.sh"
    echo "  ./02_install_k3s.sh"
    echo "  ./03_deploy_gl_backend.sh"
    echo ""
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native 卸載腳本 (單節點環境)"
    echo ""
    
    # 解析參數
    for arg in "$@"; do
        case $arg in
            --purge)
                PURGE=true
                shift
                ;;
            --namespace=*)
                NAMESPACE="${arg#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --purge              完全清除所有數據和配置"
                echo "  --namespace=NS       指定 Namespace (默認: gl-native)"
                echo "  --help, -h           顯示此幫助信息"
                echo ""
                echo "說明:"
                echo "  默認情況下，卸載腳本會保留數據和配置"
                echo "  使用 --purge 選項會完全刪除所有數據"
                exit 0
                ;;
        esac
    done
    
    # 執行卸載步驟
    uninstall_gl_backend
    uninstall_k3s
    cleanup_storage
    cleanup_network
    verify_uninstall
    print_summary
    
    exit 0
}

# 執行主函數
main "$@"