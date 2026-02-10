#!/bin/bash
# 文件名：.git/hooks/pre-commit

# 依赖检查器 (使用renovate)
MAX_DEPTH=3
DEPTH=$(npm ls --json | jq '.dependencies[].dependencies | length' | sort -nr | head -1)
if [ "$DEPTH" -gt "$MAX_DEPTH" ]; then
  echo "ERROR: Dependency depth $DEPTH exceeds maximum allowed ($MAX_DEPTH)"
  exit 1
fi

# 安全漏洞扫描
snyk test --severity-threshold=high | grep "✓" || {
  echo "Critical vulnerabilities found!"
  exit 1
}

# 架构规范检查
arch_linter check --ruleset .arch-rules.yml || exit 1
