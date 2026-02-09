#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 在線環境資源導出腳本
#
# 用途：在連接互聯網的機器上導出所有部署所需的資源
# 使用方式：./01_export_resources.sh [選項]
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
EXPORT_DIR=${EXPORT_DIR:-"/tmp/offline-bundle"}
REGISTRY=${REGISTRY:-"localhost:5000"}
VERIFY=${VERIFY:-false}
CREATE_REGISTRY=${CREATE_REGISTRY:-false}

# Docker images 列表
IMAGES=(
    "rancher/k3s:${K3S_VERSION}"
    "flannel/flannel:v0.22.0"
    "calico/node:v3.26.1"
    "calico/cni:v3.26.1"
    "calico/kube-controllers:v3.26.1"
    "coredns/coredns:1.9.3"
    "traefik:2.10"
    "gov-native/backend:v1.1"
)

# Helm charts 列表
HELM_CHARTS=(
    "https://prometheus-community.github.io/helm-charts/prometheus-15.0.0.tgz"
    "https://grafana.github.io/helm-charts/grafana-6.50.0.tgz"
)

# 二進制文件列表
BINARIES=(
    "https://github.com/k3s-io/k3s/releases/download/${K3S_VERSION}/k3s"
    "https://dl.k8s.io/release/v1.28.3/bin/linux/amd64/kubectl"
    "https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz"
)

# OS 套件列表 (Ubuntu/Debian)
PACKAGES=(
    "containerd.io"
    "docker-ce"
    "docker-ce-cli"
    "docker-compose-plugin"
)

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
# 創建目錄結構
###############################################################################

create_directory_structure() {
    print_step "1/7" "創建目錄結構"
    
    mkdir -p "${EXPORT_DIR}/images"
    mkdir -p "${EXPORT_DIR}/charts"
    mkdir -p "${EXPORT_DIR}/binaries"
    mkdir -p "${EXPORT_DIR}/packages"
    mkdir -p "${EXPORT_DIR}/scripts"
    
    print_success "目錄結構創建完成"
    print_info "導出目錄: ${EXPORT_DIR}"
}

###############################################################################
# 啟動本地 Registry
###############################################################################

start_local_registry() {
    if [ "$CREATE_REGISTRY" = false ]; then
        return 0
    fi
    
    print_step "2/7" "啟動本地 Registry"
    
    # 檢查 Registry 是否已運行
    if docker ps | grep -q "registry:2"; then
        print_info "Registry 已在運行"
        return 0
    fi
    
    print_info "啟動本地 Registry..."
    docker run -d \
        -p 5000:5000 \
        --restart=always \
        --name registry \
        -v "${EXPORT_DIR}/registry-data":/var/lib/registry \
        registry:2
    
    # 等待 Registry 啟動
    sleep 5
    
    # 驗證 Registry
    if curl -s http://localhost:5000/v2/_catalog > /dev/null; then
        print_success "Registry 啟動成功"
    else
        print_error "Registry 啟動失敗"
        exit 1
    fi
}

###############################################################################
# 導出 Docker Images
###############################################################################

export_docker_images() {
    print_step "3/7" "導出 Docker Images"
    
    local total_images=${#IMAGES[@]}
    local current=0
    
    for img in "${IMAGES[@]}"; do
        ((current++))
        print_info "[${current}/${total_images}] 處理: ${img}"
        
        # 拉取鏡像
        print_info "  拉取鏡像..."
        if ! docker pull "$img"; then
            print_warning "  無法拉取 ${img}，跳過"
            continue
        fi
        
        # 標記鏡像到本地 registry
        if [ "$CREATE_REGISTRY" = true ]; then
            local local_img="${REGISTRY}/${img}"
            print_info "  標記鏡像: ${local_img}"
            docker tag "$img" "$local_img"
            
            # 推送到本地 registry
            print_info "  推送到本地 registry..."
            docker push "$local_img"
        fi
        
        # 保存鏡像到 tar 文件
        local safe_name=$(echo "$img" | tr '/' '-' | tr ':' '-')
        local tar_file="${EXPORT_DIR}/images/${safe_name}.tar"
        
        print_info "  保存鏡像: ${tar_file}"
        docker save "$img" -o "$tar_file"
        
        # 計算文件大小
        local file_size=$(du -h "$tar_file" | cut -f1)
        print_success "  完成 (${file_size})"
    done
    
    # 創建鏡像清單
    cat > "${EXPORT_DIR}/images/manifest.txt" <<EOF
# GL-Native Docker Images Manifest
# Generated: $(date)
# k3s Version: ${K3S_VERSION}

EOF
    
    for img in "${IMAGES[@]}"; do
        echo "$img" >> "${EXPORT_DIR}/images/manifest.txt"
    done
    
    print_success "Docker Images 導出完成"
    print_info "鏡像清單: ${EXPORT_DIR}/images/manifest.txt"
}

###############################################################################
# 導出 Helm Charts
###############################################################################

export_helm_charts() {
    print_step "4/7" "導出 Helm Charts"
    
    # 下載 Helm
    if ! command -v helm > /dev/null 2>&1; then
        print_info "安裝 Helm..."
        curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    fi
    
    local total_charts=${#HELM_CHARTS[@]}
    local current=0
    
    for chart_url in "${HELM_CHARTS[@]}"; do
        ((current++))
        local chart_name=$(basename "$chart_url")
        print_info "[${current}/${total_charts}] 下載: ${chart_name}"
        
        cd "${EXPORT_DIR}/charts"
        if curl -fsSL -O "$chart_url"; then
            print_success "  下載完成"
        else
            print_error "  下載失敗: ${chart_url}"
        fi
        cd - > /dev/null
    done
    
    # 創建 Helm charts 清單
    cat > "${EXPORT_DIR}/charts/manifest.txt" <<EOF
# GL-Native Helm Charts Manifest
# Generated: $(date)

EOF
    
    for chart_url in "${HELM_CHARTS[@]}"; do
        echo "$chart_url" >> "${EXPORT_DIR}/charts/manifest.txt"
    done
    
    print_success "Helm Charts 導出完成"
}

###############################################################################
# 導出二進制文件
###############################################################################

export_binaries() {
    print_step "5/7" "導出二進制文件"
    
    local total_binaries=${#BINARIES[@]}
    local current=0
    
    for binary_url in "${BINARIES[@]}"; do
        ((current++))
        local binary_name=$(basename "$binary_url")
        print_info "[${current}/${total_binaries}] 下載: ${binary_name}"
        
        if curl -fsSL -o "${EXPORT_DIR}/binaries/${binary_name}" "$binary_url"; then
            chmod +x "${EXPORT_DIR}/binaries/${binary_name}"
            print_success "  下載完成"
        else
            print_error "  下載失敗: ${binary_url}"
        fi
    done
    
    # 下載 k3s 安裝腳本
    print_info "下載 k3s 安裝腳本..."
    curl -fsSL -o "${EXPORT_DIR}/scripts/install.sh" https://get.k3s.io
    chmod +x "${EXPORT_DIR}/scripts/install.sh"
    
    # 創建二進制文件清單
    cat > "${EXPORT_DIR}/binaries/manifest.txt" <<EOF
# GL-Native Binaries Manifest
# Generated: $(date)

EOF
    
    for binary_url in "${BINARIES[@]}"; do
        echo "$binary_url" >> "${EXPORT_DIR}/binaries/manifest.txt"
    done
    
    print_success "二進制文件導出完成"
}

###############################################################################
# 導出 OS 套件
###############################################################################

export_packages() {
    print_step "6/7" "導出 OS 套件"
    
    if [ ! -f /etc/os-release ]; then
        print_warning "無法檢測作業系統，跳過 OS 套件導出"
        return 0
    fi
    
    . /etc/os-release
    
    case "$ID" in
        ubuntu|debian)
            print_info "檢測到 Ubuntu/Debian，導出 .deb 套件"
            
            for pkg in "${PACKAGES[@]}"; do
                print_info "下載: ${pkg}"
                cd "${EXPORT_DIR}/packages"
                if apt-get download "$pkg" 2>&1 | grep -q "E:"; then
                    print_warning "  下載失敗: ${pkg}"
                else
                    print_success "  下載完成"
                fi
                cd - > /dev/null
            done
            ;;
        rhel|rocky|centos)
            print_info "檢測到 RHEL/CentOS，導出 .rpm 套件"
            
            for pkg in "${PACKAGES[@]}"; do
                print_info "下載: ${pkg}"
                cd "${EXPORT_DIR}/packages"
                if yumdownloader --resolve "$pkg" 2>&1 | grep -q "Error:"; then
                    print_warning "  下載失敗: ${pkg}"
                else
                    print_success "  下載完成"
                fi
                cd - > /dev/null
            done
            ;;
        *)
            print_warning "不支援的作業系統: $ID"
            ;;
    esac
    
    # 創建套件清單
    cat > "${EXPORT_DIR}/packages/manifest.txt" <<EOF
# GL-Native OS Packages Manifest
# Generated: $(date)
# OS: ${NAME} ${VERSION_ID}

EOF
    
    for pkg in "${PACKAGES[@]}"; do
        echo "$pkg" >> "${EXPORT_DIR}/packages/manifest.txt"
    done
    
    print_success "OS 套件導出完成"
}

###############################################################################
# 創建元數據和校驗
###############################################################################

create_metadata() {
    print_step "7/7" "創建元數據和校驗"
    
    # 創建版本清單
    cat > "${EXPORT_DIR}/versions.txt" <<EOF
# GL-Native Offline Bundle Version Manifest
# Generated: $(date)
# Bundle Version: 1.0.0

# k3s
K3S_VERSION=${K3S_VERSION}

# Docker Images
EOF
    
    for img in "${IMAGES[@]}"; do
        echo "IMAGE=${img}" >> "${EXPORT_DIR}/versions.txt"
    done
    
    echo "" >> "${EXPORT_DIR}/versions.txt"
    echo "# Helm Charts" >> "${EXPORT_DIR}/versions.txt"
    for chart_url in "${HELM_CHARTS[@]}"; do
        echo "CHART=$(basename "$chart_url")" >> "${EXPORT_DIR}/versions.txt"
    done
    
    # 創建 SHA256 校驗和
    print_info "創建 SHA256 校驗和..."
    cd "${EXPORT_DIR}"
    find . -type f -not -name "sha256sum.txt" -exec sha256sum {} \; > sha256sum.txt
    cd - > /dev/null
    
    # 驗證校驗和
    if [ "$VERIFY" = true ]; then
        print_info "驗證校驗和..."
        cd "${EXPORT_DIR}"
        sha256sum -c sha256sum.txt
        cd - > /dev/null
    fi
    
    # 創建 README
    cat > "${EXPORT_DIR}/README.txt" <<EOF
GL-Native Offline Installation Bundle
======================================

Generated: $(date)
k3s Version: ${K3S_VERSION}

Contents:
- images/     : Docker images
- charts/     : Helm charts
- binaries/   : Binary files (k3s, kubectl, helm)
- packages/   : OS packages
- scripts/    : Installation scripts

Installation:
1. Transfer this bundle to the air-gapped machine
2. Extract: tar -xzf offline-bundle.tar.gz
3. Run: ./02_import_resources.sh --bundle-dir .

Verification:
sha256sum -c sha256sum.txt

For detailed instructions, see the deployment guide.
EOF
    
    print_success "元數據和校驗創建完成"
}

###############################################################################
# 創建壓縮包
###############################################################################

create_bundle() {
    print_header "創建壓縮包"
    
    local bundle_name="offline-bundle-${K3S_VERSION}.tar.gz"
    local bundle_path="${EXPORT_DIR}/../${bundle_name}"
    
    print_info "創建壓縮包: ${bundle_path}"
    cd "${EXPORT_DIR}/.."
    tar -czf "${bundle_name}" -C "$(basename "${EXPORT_DIR}")" .
    
    local bundle_size=$(du -h "${bundle_path}" | cut -f1)
    print_success "壓縮包創建完成"
    print_info "文件大小: ${bundle_size}"
    print_info "文件路徑: ${bundle_path}"
    
    # 創建壓縮包的 SHA256
    sha256sum "${bundle_path}" > "${bundle_path}.sha256"
    
    print_info ""
    print_info "SHA256: $(cat "${bundle_path}.sha256" | cut -d' ' -f1)"
}

###############################################################################
# 導出完成總結
###############################################################################

print_summary() {
    print_header "資源導出完成"
    
    echo -e "${GREEN}✓ 所有資源導出成功！${NC}"
    echo ""
    echo "導出摘要:"
    echo "  k3s 版本: ${K3S_VERSION}"
    echo "  導出目錄: ${EXPORT_DIR}"
    echo "  Docker Images: ${#IMAGES[@]}"
    echo "  Helm Charts: ${#HELM_CHARTS[@]}"
    echo "  Binaries: ${#BINARIES[@]}"
    echo "  OS Packages: ${#PACKAGES[@]}"
    echo ""
    
    if [ -f "${EXPORT_DIR}/../offline-bundle-${K3S_VERSION}.tar.gz" ]; then
        echo "離線安裝包:"
        echo "  ${EXPORT_DIR}/../offline-bundle-${K3S_VERSION}.tar.gz"
        echo ""
        echo "下一步:"
        echo "  1. 傳輸離線安裝包到離線環境"
        echo "  2. 在離線環境執行: ./02_import_resources.sh"
        echo "  3. 安裝 k3s: ./04_install_k3s.sh"
        echo ""
    else
        echo "資源已導出到: ${EXPORT_DIR}"
        echo ""
        echo "下一步:"
        echo "  1. 手動打包: cd ${EXPORT_DIR}/.. && tar -czf offline-bundle.tar.gz offline-bundle/"
        echo "  2. 傳輸到離線環境"
        echo ""
    fi
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native 在線環境資源導出腳本"
    echo ""
    
    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            --k3s-version=*)
                K3S_VERSION="${1#*=}"
                shift
                ;;
            --export-dir=*)
                EXPORT_DIR="${1#*=}"
                shift
                ;;
            --registry=*)
                REGISTRY="${1#*=}"
                shift
                ;;
            --create-registry)
                CREATE_REGISTRY=true
                shift
                ;;
            --verify)
                VERIFY=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --k3s-version=VERSION   k3s 版本 (默認: v1.28.3+k3s2)"
                echo "  --export-dir=DIR        導出目錄 (默認: /tmp/offline-bundle)"
                echo "  --registry=URL          本地 registry URL"
                echo "  --create-registry       創建本地 registry"
                echo "  --verify                驗證導出的文件"
                echo "  --help, -h              顯示此幫助信息"
                exit 0
                ;;
            *)
                print_error "未知選項: $1"
                exit 1
                ;;
        esac
    done
    
    # 執行導出步驟
    create_directory_structure
    start_local_registry
    export_docker_images
    export_helm_charts
    export_binaries
    export_packages
    create_metadata
    create_bundle
    print_summary
    
    exit 0
}

# 執行主函數
main "$@"