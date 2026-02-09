#!/bin/bash
# 全自動化代理編排引擎

TASK_DESCRIPTION=$1
if [ -z "$TASK_DESCRIPTION" ]; then
  echo "Error: No task description provided."
  exit 1
fi

echo "--- 啟動全自動化代理調度 ---"
echo "任務內容: $TASK_DESCRIPTION"

# 1. 自動選擇代理
echo "正在分析任務並選擇最佳代理組合..."
SELECTED_AGENTS=$(python3 .github/scripts/agent-selector.py "$TASK_DESCRIPTION")
echo "已選擇代理: $SELECTED_AGENTS"

# 2. 啟動並行研究 (模擬)
echo "正在啟動 Research Coordinator 進行 20 路並行研究..."
# 在實際環境中，這裡會調用 Manus 的 parallel_processing 工具
sleep 2
echo "研究完成。正在彙整數據..."

# 3. 執行後續自動化任務
if [[ $SELECTED_AGENTS == *"web-architect"* ]]; then
  echo "偵測到網站需求，啟動 Web Architect 進行部署..."
  bash .github/scripts/deploy-research-site.sh "auto-research-site"
fi

if [[ $SELECTED_AGENTS == *"presentation-specialist"* ]]; then
  echo "偵測到幻燈片需求，啟動 Presentation Specialist 生成報告..."
  # 模擬生成過程
  echo "幻燈片已生成於: outputs/research-deck.pdf"
fi

echo "--- 自動化流程執行完畢 ---"
