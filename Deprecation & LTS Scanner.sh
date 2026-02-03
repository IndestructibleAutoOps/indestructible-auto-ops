# 依赖生命周期扫描脚本
#!/bin/bash

# 检查弃用依赖
DEPRECATED_DEPS=$(npm ls --json | jq '.dependencies | to_entries[] | select(.value.deprecated)')
if [ -n "$DEPRECATED_DEPS" ]; then
  echo "WARNING: Deprecated dependencies detected:"
  echo $DEPRECATED_DEPS
  # 自动创建迁移工单
  curl -X POST -H "Content-Type: application/json" \
       -d '{"type":"dependency-migration","dependencies":$DEPRECATED_DEPS}' \
       http://task-system/api/v1/tickets
fi

# LTS到期检查
for DEP in $(npm ls --parseable); do
  SUPPORT_END=$(npm view $DEP supportEnd --json)
  TODAY=$(date +%s)
  if [ "$SUPPORT_END" -lt "$TODAY" ]; then
    echo "CRITICAL: $DEP has ended LTS support on $(date -d @$SUPPORT_END)"
    exit 1
  fi
done
