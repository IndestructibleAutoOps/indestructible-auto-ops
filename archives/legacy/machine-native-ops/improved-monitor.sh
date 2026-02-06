#!/bin/bash

# GL-ROOT Governance Event Stream Monitor - Enhanced Version
# 定期提交和推送 governance event stream 更新

CONFIG_FILE="governance-monitor-config.yaml"
LOG_FILE="governance-monitor.log"
PID_FILE="governance-monitor.pid"

# 初始化日誌
init_log() {
    echo "=== Governance Monitor Started at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
}

# 寫入日誌
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# 檢查 governance event stream 文件是否有變更
check_for_changes() {
    git status --porcelain | grep -q "\.governance.*event-stream"
    return $?
}

# 提交並推送變更
commit_and_push() {
    log "INFO" "發現 governance event stream 更新，正在處理..."
    
    # 添加所有 governance event stream 文件
    local added_files=0
    for file in engine/.governance/event-stream.jsonl \
                 engine/.governance/governance-event-stream.jsonl \
                 file-organizer-system/.governance/event-stream.jsonl; do
        if [ -f "$file" ]; then
            git add "$file" 2>/dev/null
            if [ $? -eq 0 ]; then
                ((added_files++))
                log "DEBUG" "已添加文件: $file"
            fi
        fi
    done
    
    if [ $added_files -eq 0 ]; then
        log "WARN" "沒有需要提交的文件"
        return 1
    fi
    
    # 提交更改
    local commit_msg="chore: periodic governance event stream update - $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$commit_msg" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        log "WARN" "提交失敗或沒有變更需要提交"
        return 1
    fi
    
    log "INFO" "提交成功: $commit_msg"
    
    # 推送到遠端
    git push origin main 2>&1 | tee -a "$LOG_FILE"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        log "INFO" "✅ 推送成功"
        return 0
    else
        log "ERROR" "❌ 推送失敗"
        return 1
    fi
}

# 清理函數
cleanup() {
    log "INFO" "接收到停止信號，正在清理..."
    if [ -f "$PID_FILE" ]; then
        rm -f "$PID_FILE"
    fi
    log "INFO" "Governance Monitor 已停止"
    exit 0
}

# 設置信號處理
trap cleanup SIGINT SIGTERM

# 檢查是否已經在運行
if [ -f "$PID_FILE" ]; then
    old_pid=$(cat "$PID_FILE")
    if ps -p "$old_pid" > /dev/null 2>&1; then
        echo "Governance Monitor 已經在運行 (PID: $old_pid)"
        exit 1
    else
        rm -f "$PID_FILE"
    fi
fi

# 創建 PID 文件
echo $$ > "$PID_FILE"

# 初始化
init_log
log "INFO" "Governance Event Stream Monitor 已啟動"
log "INFO" "配置文件: $CONFIG_FILE"
log "INFO" "日誌文件: $LOG_FILE"
log "INFO" "監控間隔: 60 秒"

# 主監控循環
check_count=0
commit_count=0
push_success_count=0
push_fail_count=0

while true; do
    ((check_count++))
    log "DEBUG" "監控檢查 #$check_count"
    
    if check_for_changes; then
        log "INFO" "檢測到 governance event stream 變更"
        
        if commit_and_push; then
            ((commit_count++))
            ((push_success_count++))
            log "INFO" "統計: 檢查=$check_count, 提交=$commit_count, 推送成功=$push_success_count, 推送失敗=$push_fail_count"
        else
            ((push_fail_count++))
            log "INFO" "統計: 檢查=$check_count, 提交=$commit_count, 推送成功=$push_success_count, 推送失敗=$push_fail_count"
        fi
    else
        log "DEBUG" "沒有新的更新"
    fi
    
    # 每小時輸出一次統計信息
    if [ $((check_count % 60)) -eq 0 ]; then
        log "INFO" "每小時統計: 檢查=$check_count, 提交=$commit_count, 推送成功=$push_success_count, 推送失敗=$push_fail_count"
    fi
    
    sleep 60
done
