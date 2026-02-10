#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 依賴檢查清單腳本
#
# 用途：檢查離線環境是否具備所有必需的依賴
# 使用方式：./06_dependency_check.sh --bundle-dir DIR
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BUNDLE_DIR=${BUNDLE_DIR:-""}
VERBOSE=${VERBOSE:-false}
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((CHECKS_WARNING++))
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

check_docker_images() {
    print_header "檢查 1: Docker Images"
    
    if [ ! -d "$BUNDLE_DIR/images" ]; then
        print_error "Images 目錄不存在: $BUNDLE_DIR/images"
        return 1
    fi
    
    local manifest_file="$BUNDLE_DIR/images/manifest.txt"
    if [ ! -f "$manifest_file" ]; then
        print_error "Images manifest 不存在"
        return 1
    fi
    
    local total_images=$(grep -c "^IMAGE=" "$manifest_file" 2>/dev/null || echo "0")
    print_info "期望的 images: $total_images"
    
    local found_images=$(find "$BUNDLE_DIR/images" -name "*.tar" | wc -l)
    print_info "找到的 images: $found_images"
    
    if [ "$found_images" -lt "$total_images" ]; then
        print_error "缺少 Docker images"
        return 1
    fi
    
    # 檢查關鍵 images
    local required_images=("k3s" "flannel" "coredns")
    for img in "${required_images[@]}"; do
        if find "$BUNDLE_DIR/images" -name "*${img}*" | grep -q .; then
            print_success "找到 ${img} image"
        else
            print_error "缺少 ${img} image"
            return 1
        fi
    done
    
    print_success "Docker Images 檢查通過"
    return 0
}

check_binaries() {
    print_header "檢查 2: 二進制文件"
    
    if [ ! -d "$BUNDLE_DIR/binaries" ]; then
        print_error "Binaries 目錄不存在: $BUNDLE_DIR/binaries"
        return 1
    fi
    
    local required_binaries=("k3s")
    for bin in "${required_binaries[@]}"; do
        if [ -f "$BUNDLE_DIR/binaries/$bin" ]; then
            if [ -x "$BUNDLE_DIR/binaries/$bin" ]; then
                print_success "$bin 存在且可執行"
            else
                print_error "$bin 存在但不可執行"
                return 1
            fi
        else
            print_error "缺少 $bin"
            return 1
        fi
    done
    
    # 檢查可選二進制文件
    local optional_binaries=("kubectl" "helm")
    for bin in "${optional_binaries[@]}"; do
        if [ -f "$BUNDLE_DIR/binaries/$bin" ]; then
            print_success "$bin 存在"
        else
            print_warning "$bin 不存在（可選）"
        fi
    done
    
    print_success "二進制文件檢查通過"
    return 0
}

check_packages() {
    print_header "檢查 3: OS 套件"
    
    if [ ! -d "$BUNDLE_DIR/packages" ]; then
        print_warning "Packages 目錄不存在（可選）"
        return 0
    fi
    
    local package_count=$(find "$BUNDLE_DIR/packages" -type f \( -name "*.deb" -o -name "*.rpm" \) | wc -l)
    print_info "找到的 OS 套件: $package_count"
    
    if [ "$package_count" -eq 0 ]; then
        print_warning "沒有找到 OS 套件"
    else
        print_success "找到 $package_count 個 OS 套件"
    fi
    
    return 0
}

check_charts() {
    print_header "檢查 4: Helm Charts"
    
    if [ ! -d "$BUNDLE_DIR/charts" ]; then
        print_warning "Charts 目錄不存在（可選）"
        return 0
    fi
    
    local chart_count=$(find "$BUNDLE_DIR/charts" -name "*.tgz" | wc -l)
    print_info "找到的 Helm Charts: $chart_count"
    
    if [ "$chart_count" -eq 0 ]; then
        print_warning "沒有找到 Helm Charts"
    else
        print_success "找到 $chart_count 個 Helm Charts"
    fi
    
    return 0
}

check_registry() {
    print_header "檢查 5: Docker Registry"
    
    if command -v docker > /dev/null 2>&1; then
        print_info "Docker 已安裝"
        
        if docker ps | grep -q "registry:2"; then
            print_success "Registry 容器正在運行"
        else
            print_warning "Registry 容器未運行"
        fi
        
        if curl -s http://localhost:5000/v2/_catalog > /dev/null 2>&1; then
            print_success "Registry API 可訪問"
        else
            print_warning "Registry API 不可訪問"
        fi
    else
        print_warning "Docker 未安裝"
    fi
    
    return 0
}

check_disk_space() {
    print_header "檢查 6: 磁碟空間"
    
    local available_gb=$(df -BG "$BUNDLE_DIR" | awk 'NR==2 {print $4}' | tr -d 'G')
    print_info "可用磁碟空間: ${available_gb} GB"
    
    if [ "$available_gb" -lt 10 ]; then
        print_warning "磁碟空間較低，建議至少 10 GB"
    else
        print_success "磁碟空間充足"
    fi
    
    return 0
}

check_network() {
    print_header "檢查 7: 網路配置"
    
    # 檢查內部網路
    local active_interfaces=$(ip -o link show up | grep -v lo | awk '{print $2}' | cut -d: -f1)
    print_info "活動網路介面: $active_interfaces"
    
    if [ -z "$active_interfaces" ]; then
        print_error "沒有活動網路介面"
        return 1
    else
        print_success "網路配置正常"
    fi
    
    return 0
}

check_time_sync() {
    print_header "檢查 8: 時間同步"
    
    if systemctl is-active --quiet chronyd 2>/dev/null || \
       systemctl is-active --quiet ntp 2>/dev/null || \
       systemctl is-active --quiet systemd-timesyncd 2>/dev/null; then
        print_success "時間同步服務正在運行"
    else
        print_warning "時間同步服務未運行"
    fi
    
    # 檢查時間同步狀態
    local synced=$(timedatectl 2>/dev/null | grep -c "System clock synchronized: yes" || echo "0")
    if [ "$synced" -eq 1 ]; then
        print_success "時間已同步"
    else
        print_warning "時間未同步"
    fi
    
    return 0
}

check_integrity() {
    print_header "檢查 9: 完整性驗證"
    
    local sha256_file="$BUNDLE_DIR/sha256sum.txt"
    if [ ! -f "$sha256_file" ]; then
        print_warning "SHA256 校驗文件不存在"
        return 0
    fi
    
    print_info "驗證文件完整性..."
    cd "$BUNDLE_DIR"
    if sha256sum -c sha256sum.txt > /dev/null 2>&1; then
        print_success "所有文件完整性驗證通過"
        cd - > /dev/null
        return 0
    else
        print_error "部分文件完整性驗證失敗"
        cd - > /dev/null
        return 1
    fi
}

check_metadata() {
    print_header "檢查 10: 元數據"
    
    local required_files=("versions.txt" "README.txt")
    for file in "${required_files[@]}"; do
        if [ -f "$BUNDLE_DIR/$file" ]; then
            print_success "$file 存在"
        else
            print_warning "$file 不存在"
        fi
    done
    
    return 0
}

main() {
    print_header "GL-Native 依賴檢查腳本"
    echo ""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --bundle-dir=*)
                BUNDLE_DIR="${1#*=}"
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
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
    
    # 執行所有檢查
    check_docker_images || true
    check_binaries || true
    check_packages || true
    check_charts || true
    check_registry || true
    check_disk_space || true
    check_network || true
    check_time_sync || true
    check_integrity || true
    check_metadata || true
    
    # 總結
    print_header "檢查結果總結"
    echo -e "${GREEN}通過:${NC} $CHECKS_PASSED"
    echo -e "${YELLOW}警告:${NC} $CHECKS_WARNING"
    echo -e "${RED}失敗:${NC} $CHECKS_FAILED"
    echo ""
    
    if [ "$CHECKS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ 所有关鍵檢查通過，可以開始安裝${NC}"
        echo ""
        echo "下一步:"
        echo "  ./03_setup_registry.sh"
        echo "  ./04_install_k3s.sh"
        exit 0
    else
        echo -e "${RED}✗ 檢查失敗，請解決上述問題後重試${NC}"
        exit 1
    fi
}

main "$@"