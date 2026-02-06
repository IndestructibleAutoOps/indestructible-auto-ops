#!/bin/bash

echo "開始監控 governance event stream 更新..."
echo "每 60 秒檢查一次是否有新的更新"

while true; do
  git status --porcelain | grep -q "modified.*\.governance.*event-stream"
  if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 發現 governance event stream 更新，正在提交和推送..."
    
    # 添加所有 governance event stream 文件
    git add engine/.governance/event-stream.jsonl 2>/dev/null
    git add engine/.governance/governance-event-stream.jsonl 2>/dev/null
    git add file-organizer-system/.governance/event-stream.jsonl 2>/dev/null
    
    # 提交更改
    git commit -m "chore: periodic governance event stream update - $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null
    
    # 推送到遠端
    if [ $? -eq 0 ]; then
      git push origin main
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 提交和推送完成"
    else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  沒有需要提交的更改"
    fi
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 沒有新的更新，等待 60 秒..."
  fi
  
  sleep 60
done
