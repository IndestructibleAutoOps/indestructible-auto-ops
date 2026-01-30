#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 叢集環境前置檢查腳本
#
# 用途：在安裝 k3s 叢集之前檢查系統環境是否符合要求
# 使用方式：./01_pre_install_check.sh [--role ROLE] [--verbose]
###############################################################################

set -e  # 遇到錯誤立即退出
set -u  # 使用未定義的變數時報錯

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 全局變數
VERBOSE=${VERBOSE:-false}
NODE_ROLE=${NODE_ROLE:-'unknown'}
CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

# 叢集配置
CLUSTER_ENABLED=${CLUSTER_ENABLED:-true}
HA_MODE=${HA_MODE:-false}

# 最小系統要求
MIN_CPU_CORES_CONTROL=4
MIN_CPU_CORES_WORKER=8
MIN_RAM_GB_CONTROL=8
MIN_RAM_GB_WORKER=16
MIN_DISK_GB=100

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
    ((CHECKS_PASSED++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

print_info() {
    echo -e "${NC}→${NC} $1"
}

verbose_info() {
    if [ "$VERBOSE" = true ]; then
        echo "  [VERBOSE] $1"
    fi
}

###############################################################################
# 檢查函數
###############################################################################

check_root() {
    print_header "檢查 1: Root 權限"
    
    if [ "$EUID" -ne 0 ]; then 
        print_error "請使用 root 權限執行此腳本"
        print_info "使用方式: sudo $0"
        return 1
    fi
    
    print_success "具有 root 權限"
    return 0
}

check_os() {
    print_header "檢查 2: 作業系統"
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
        
        print_info "檢測到 OS: $NAME $VERSION"
        
        case "$OS" in
            ubuntu|debian)
                if [ "$OS" = "ubuntu" ] && [ "$(echo "$VERSION < 20.04" | bc 2>/dev/null || echo "0")" = "1" ]; then
                    print_error "Ubuntu 版本過低，需要 20.04 或更高版本"
                    return 1
                fi
                if [ "$OS" = "debian" ] && [ "$(echo "$VERSION < 11" | bc 2>/dev/null || echo "0")" = "1" ]; then
                    print_error "Debian 版本過低，需要 11 或更高版本"
                    return 1
                fi
                ;;
            rhel|rocky|centos)
                if [ "$(echo "$VERSION < 8" | bc 2>/dev/null || echo "0")" = "1" ]; then
                    print_error "RHEL 系列版本過低，需要 8 或更高版本"
                    return 1
                fi
                ;;
            *)
                print_error "不支援的作業系統: $OS"
                print_info "支援的系統: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+"
                return 1
                ;;
        esac
        
        print_success "OS 版本符合要求"
        return 0
    else
        print_error "無法檢測作業系統版本"
        return 1
    fi
}

check_hostname() {
    print_header "檢查 3: 主機名"
    
    local hostname=$(hostname)
    local hostname_fqdn=$(hostname -f 2>/dev/null || echo "")
    
    print_info "主機名: $hostname"
    print_info "FQDN: ${hostname_fqdn}"
    
    if [ -z "$hostname" ] || [ "$hostname" = "localhost" ]; then
        print_error "主機名無效，請設置唯一的主機名"
        print_info "設置主機名: hostnamectl set-hostname <node-name>"
        return 1
    fi
    
    # 檢查 /etc/hosts
    if ! grep -q "^127.0.0.1.*${hostname}" /etc/hosts; then
        print_warning "/etc/hosts 中未找到主機名映射"
        print_info "建議添加: echo '127.0.0.1 ${hostname}' >> /etc/hosts"
    fi
    
    print_success "主機名配置正確"
    return 0
}

check_cpu() {
    print_header "檢查 4: CPU 核心"
    
    local cpu_cores=$(nproc)
    print_info "檢測到 CPU 核心: $cpu_cores"
    
    local min_cores
    if [ "$NODE_ROLE" = "control" ] || [ "$NODE_ROLE" = "first-server" ] || [ "$NODE_ROLE" = "additional-server" ]; then
        min_cores=$MIN_CPU_CORES_CONTROL
    else
        min_cores=$MIN_CPU_CORES_WORKER
    fi
    
    if [ "$cpu_cores" -ge "$min_cores" ]; then
        print_success "CPU 核心數符合要求 (≥ $min_cores cores)"
        return 0
    elif [ "$cpu_cores" -ge "$((min_cores / 2))" ]; then
        print_warning "CPU 核心數較低，建議至少 $min_cores cores"
        return 0
    else
        print_error "CPU 核心數不足 (需要 ≥ $min_cores cores，實際: $cpu_cores)"
        return 1
    fi
}

check_memory() {
    print_header "檢查 5: 記憶體"
    
    local ram_gb=$(free -g | awk '/^Mem:/{print $2}')
    local ram_mb=$(free -m | awk '/^Mem:/{print $2}')
    
    print_info "檢測到記憶體: ${ram_mb} MB (${ram_gb} GB)"
    
    local min_ram
    if [ "$NODE_ROLE" = "control" ] || [ "$NODE_ROLE" = "first-server" ] || [ "$NODE_ROLE" = "additional-server" ]; then
        min_ram=$MIN_RAM_GB_CONTROL
    else
        min_ram=$MIN_RAM_GB_WORKER
    fi
    
    if [ "$ram_gb" -ge "$min_ram" ]; then
        print_success "記憶體符合要求 (≥ ${min_ram} GB)"
        return 0
    elif [ "$ram_mb" -ge "$((min_ram * 1024 - 1024))" ]; then
        print_warning "記憶體較低，建議至少 ${min_ram} GB"
        return 0
    else
        print_error "記憶體不足 (需要 ≥ ${min_ram} GB，實際: ${ram_gb} GB)"
        return 1
    fi
}

check_disk() {
    print_header "檢查 6: 磁碟空間"
    
    local disk_gb=$(df -BG / | awk 'NR==2 {print $4}' | tr -d 'G')
    
    print_info "檢測到可用磁碟空間: ${disk_gb} GB"
    
    if [ "$disk_gb" -ge "$MIN_DISK_GB" ]; then
        print_success "磁碟空間符合要求 (≥ ${MIN_DISK_GB} GB)"
        return 0
    elif [ "$disk_gb" -ge "$((MIN_DISK_GB / 2))" ]; then
        print_warning "磁碟空間較低，建議至少 ${MIN_DISK_GB} GB"
        return 0
    else
        print_error "磁碟空間不足 (需要 ≥ ${MIN_DISK_GB} GB，實際: ${disk_gb} GB)"
        return 1
    fi
}

check_network() {
    print_header "檢查 7: 網路連接"
    
    # 檢查是否有活動網路介面
    local active_interfaces=$(ip -o link show up | grep -v lo | awk '{print $2}' | cut -d: -f1)
    
    if [ -z "$active_interfaces" ]; then
        print_error "未檢測到活動網路介面"
        return 1
    fi
    
    print_info "檢測到活動網路介面:"
    echo "$active_interfaces" | while read iface; do
        local ip=$(ip -4 addr show "$iface" 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -1)
        print_info "  - $iface: ${ip:-N/A}"
    done
    
    # 檢查節點間連通性 (叢集模式)
    if [ "$CLUSTER_ENABLED" = true ]; then
        print_info "叢集模式：檢查節點間連通性"
        
        if [ -n "${CONTROL_PLANE_IPS:-}" ]; then
            IFS=',' read -ra IPS <<< "$CONTROL_PLANE_IPS"
            for ip in "${IPS[@]}"; do
                if [ "$ip" != "$(hostname -I | awk '{print $1}')" ]; then
                    if ping -c 1 -W 2 "$ip" > /dev/null 2>&1; then
                        print_success "可以連接到控制平面節點 $ip"
                    else
                        print_error "無法連接到控制平面節點 $ip"
                        return 1
                    fi
                fi
            done
        fi
    fi
    
    # 檢查外部網路連接
    if ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
        print_success "外部網路連接正常"
        return 0
    else
        print_warning "無法連接到外部網路 (8.8.8.8)"
        print_info "如果部署在離線環境，這是預期的"
        return 0
    fi
}

check_ports() {
    print_header "檢查 8: 端口可用性"
    
    local ports_to_check=("6443" "10250")
    local all_ports_available=true
    
    if [ "$NODE_ROLE" = "control" ] || [ "$NODE_ROLE" = "first-server" ] || [ "$NODE_ROLE" = "additional-server" ]; then
        ports_to_check+=("8472")  # Flannel VXLAN
    fi
    
    for port in "${ports_to_check[@]}"; do
        if ss -tuln | grep -q ":${port} "; then
            print_error "端口 ${port} 已被佔用"
            verbose_info "進程: $(ss -tulnp | grep ":${port} " || echo 'unknown')"
            all_ports_available=false
        else
            print_success "端口 ${port} 可用"
        fi
    done
    
    if [ "$all_ports_available" = true ]; then
        return 0
    else
        print_error "部分端口被佔用，請停止佔用進程或使用其他端口"
        return 1
    fi
}

check_firewall() {
    print_header "檢查 9: 防火牆設定"
    
    local firewalld_running=false
    local ufw_running=false
    local iptables_rules=false
    
    # 檢查 firewalld
    if systemctl is-active --quiet firewalld 2>/dev/null; then
        firewalld_running=true
        print_info "檢測到 firewalld 正在運行"
    fi
    
    # 檢查 ufw
    if command -v ufw > /dev/null 2>&1; then
        if ufw status | grep -q "Status: active"; then
            ufw_running=true
            print_info "檢測到 ufw 正在運行"
        fi
    fi
    
    # 檢查 iptables 規則
    if iptables -L -n 2>/dev/null | grep -q "Chain"; then
        iptables_rules=true
        print_info "檢測到 iptables 規則"
    fi
    
    if [ "$firewalld_running" = true ] || [ "$ufw_running" = true ] || [ "$iptables_rules" = true ]; then
        print_warning "檢測到防火牆正在運行"
        
        local required_ports="6443 (API), 10250 (Kubelet)"
        if [ "$NODE_ROLE" = "control" ] || [ "$NODE_ROLE" = "first-server" ] || [ "$NODE_ROLE" = "additional-server" ]; then
            required_ports+=", 8472 (Flannel)"
        fi
        
        print_info "k3s 需要以下端口: ${required_ports}"
        print_info "請確保這些端口已開放"
        return 0
    else
        print_success "未檢測到活動防火牆"
        return 0
    fi
}

check_swap() {
    print_header "檢查 10: Swap 空間"
    
    local swap_total=$(free -g | awk '/^Swap:/{print $2}')
    
    print_info "檢測到 Swap: ${swap_total} GB"
    
    if [ "$swap_total" -gt 0 ]; then
        print_warning "檢測到 Swap 空間已啟用"
        print_info "Kubernetes 建議關閉 Swap 以獲得最佳性能"
        print_info "關閉 Swap: sudo swapoff -a"
        print_info "永久關閉: 註釋 /etc/fstab 中的 swap 行"
        return 0
    else
        print_success "Swap 已關閉 (符合 Kubernetes 最佳實踐)"
        return 0
    fi
}

check_time_sync() {
    print_header "檢查 11: 時間同步"
    
    local ntp_running=false
    local chrony_running=false
    local systemd_timesyncd=false
    
    if systemctl is-active --quiet ntpd 2>/dev/null || systemctl is-active --quiet ntp 2>/dev/null; then
        ntp_running=true
        print_info "檢測到 NTP 服務正在運行"
    fi
    
    if systemctl is-active --quiet chronyd 2>/dev/null; then
        chrony_running=true
        print_info "檢測到 Chrony 服務正在運行"
    fi
    
    if systemctl is-active --quiet systemd-timesyncd 2>/dev/null; then
        systemd_timesyncd=true
        print_info "檢測到 systemd-timesyncd 正在運行"
    fi
    
    if [ "$ntp_running" = true ] || [ "$chrony_running" = true ] || [ "$systemd_timesyncd" = true ]; then
        print_success "時間同步服務正在運行"
        
        # 檢查時間偏差
        if command -v chronyc > /dev/null 2>&1; then
            local offset=$(chronyc tracking | grep "Last offset" | awk '{print $4}')
            print_info "時間偏差: ${offset}"
        fi
        
        return 0
    else
        print_warning "未檢測到時間同步服務"
        print_info "Kubernetes 叢集需要所有節點時間同步"
        print_info "建議安裝: sudo apt install ntp (Ubuntu/Debian)"
        print_info "         sudo yum install chrony (RHEL/CentOS)"
        return 0
    fi
}

check_kernel_modules() {
    print_header "檢查 12: Kernel 模組"
    
    local modules_needed=("br_netfilter" "overlay")
    local all_loaded=true
    
    for module in "${modules_needed[@]}"; do
        if lsmod | grep -q "^${module} "; then
            print_info "模組 ${module} 已加載"
        else
            print_info "模組 ${module} 未加載"
            all_loaded=false
        fi
    done
    
    if [ "$all_loaded" = true ]; then
        print_success "所需的 Kernel 模組已加載"
        return 0
    else
        print_warning "部分 Kernel 模組未加載"
        print_info "加載模組: sudo modprobe br_netfilter overlay"
        print_info "永久加載: echo 'br_netfilter' > /etc/modules-load.d/k3s.conf"
        print_info "            echo 'overlay' >> /etc/modules-load.d/k3s.conf"
        return 0
    fi
}

check_existing_k3s() {
    print_header "檢查 13: 現有 k3s 安裝"
    
    if command -v k3s > /dev/null 2>&1; then
        local k3s_version=$(k3s --version 2>/dev/null | head -1)
        print_warning "檢測到 k3s 已安裝: $k3s_version"
        print_info "如果要重新安裝，請先卸載現有 k3s"
        return 0
    else
        print_success "未檢測到現有 k3s 安裝"
        return 0
    fi
}

check_docker() {
    print_header "檢查 14: Docker 安裝"
    
    if command -v docker > /dev/null 2>&1; then
        local docker_version=$(docker --version)
        print_warning "檢測到 Docker 已安裝: $docker_version"
        print_info "k3s 使用 containerd 作為容器運行時，Docker 不是必需的"
        print_info "但可以與 Docker 共存"
        return 0
    else
        print_success "未檢測到 Docker (k3s 不需要 Docker)"
        return 0
    fi
}

check_cluster_requirements() {
    print_header "檢查 15: 叢集專屬要求"
    
    if [ "$CLUSTER_ENABLED" != true ]; then
        print_info "非叢集模式，跳過叢集專屬檢查"
        return 0
    fi
    
    local cluster_checks_passed=true
    
    # 檢查 DNS 配置
    print_info "檢查 DNS 配置..."
    if grep -q "^search" /etc/resolv.conf; then
        print_success "DNS 配置正常"
    else
        print_warning "未配置 DNS search domains"
    fi
    
    # 檢查 SSH 訪問
    print_info "檢查 SSH 服務..."
    if systemctl is-active --quiet ssh 2>/dev/null || systemctl is-active --quiet sshd 2>/dev/null; then
        print_success "SSH 服務正在運行"
    else
        print_warning "SSH 服務未運行"
    fi
    
    # 控制平面節點額外檢查
    if [ "$NODE_ROLE" = "control" ] || [ "$NODE_ROLE" = "first-server" ] || [ "$NODE_ROLE" = "additional-server" ]; then
        print_info "控制平面節點檢查..."
        
        # 檢查 Load Balancer (如果是第一個節點)
        if [ "$NODE_ROLE" = "first-server" ] && [ "$HA_MODE" = true ]; then
            if [ -n "${VIP_ADDRESS:-}" ]; then
                print_info "VIP 地址: ${VIP_ADDRESS}"
            else
                print_warning "未配置 VIP 地址"
            fi
        fi
    fi
    
    return 0
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native 叢集環境前置檢查"
    echo ""
    
    # 解析參數
    for arg in "$@"; do
        case $arg in
            --role=*)
                NODE_ROLE="${arg#*=}"
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --role=ROLE           指定節點角色 (first-server/additional-server/agent)"
                echo "  --verbose, -v         顯示詳細輸出"
                echo "  --help, -h            顯示此幫助信息"
                echo ""
                echo "環境變數:"
                echo "  CLUSTER_ENABLED       啟用叢集模式 (默認: true)"
                echo "  HA_MODE               高可用模式 (默認: false)"
                echo "  CONTROL_PLANE_IPS     控制平面節點 IP 列表"
                echo "  VIP_ADDRESS           虛擬 IP 地址"
                exit 0
                ;;
        esac
    done
    
    # 執行所有檢查
    check_root || true
    check_os || true
    check_hostname || true
    check_cpu || true
    check_memory || true
    check_disk || true
    check_network || true
    check_ports || true
    check_firewall || true
    check_swap || true
    check_time_sync || true
    check_kernel_modules || true
    check_existing_k3s || true
    check_docker || true
    check_cluster_requirements || true
    
    # 總結
    print_header "檢查結果總結"
    echo -e "${GREEN}通過:${NC} $CHECKS_PASSED"
    echo -e "${YELLOW}警告:${NC} $WARNINGS"
    echo -e "${RED}失敗:${NC} $CHECKS_FAILED"
    echo ""
    
    if [ "$CHECKS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ 所有關鍵檢查通過，可以繼續安裝${NC}"
        echo ""
        
        if [ "$NODE_ROLE" = "first-server" ]; then
            echo "下一步: sudo ./02_init_control_plane.sh --role first-server"
        elif [ "$NODE_ROLE" = "additional-server" ]; then
            echo "下一步: sudo ./02_init_control_plane.sh --role additional-server --server-url <url> --token <token>"
        elif [ "$NODE_ROLE" = "agent" ]; then
            echo "下一步: sudo ./03_join_worker_node.sh --server-url <url> --token <token>"
        else
            echo "請指定節點角色: --role first-server|additional-server|agent"
        fi
        echo ""
        return 0
    else
        echo -e "${RED}✗ 檢查失敗，請解決上述問題後重試${NC}"
        return 1
    fi
}

# 執行主函數
main "$@"