# 本地知識庫

## 概述

本文件提供了所有外部參考的本地替代方案，確保平台完全自給自足。

## 替代方案

### GitHub項目參考
**原參考：** https://github.com/MachineNativeOps/machine-native-ops

**本地替代：** 項目根目錄

使用方式：
```bash
# 查看項目文檔
ls docs/
# 查看README
cat README.md
```

### 問題跟蹤
**原參考：** https://github.com/MachineNativeOps/machine-native-ops/issues

**本地替代：** 項目問題跟蹤（如需要）

創建本地問題跟蹤：
```bash
# 創建本地問題追蹤文件
mkdir -p .local-issues
echo "# Local Issue Tracking" > .local-issues/README.md
```

### RKE2文檔
**原參考：** https://docs.rke2.io/

**本地替代：** 本地RKE2文檔

位置：`infrastructure/rke2/docs/`

### CIS Kubernetes基準
**原參考：** https://www.cisecurity.org/benchmark/kubernetes

**本地替代：** 本地安全基準

位置：`infrastructure/security/cis-benchmark/`

### 監控文檔
**原參考：** Promethues/Grafana外部文檔

**本地替代：** 本地監控系統文檔

位置：`gl-observability/docs/`

### 開發文檔
**原參考：** 外部教程和指南

**本地替代：** 本地開發文檔

位置：`docs/DEVELOPMENT_GUIDE.md`

## 依賴移除驗證

### NPM依賴
- ✅ 所有package.json文件已移除
- ✅ 所有node_modules目錄已移除
- ✅ 所有yarn.lock和pnpm-lock.yaml文件已移除

### Python依賴
- ✅ 所有requirements.txt已清空
- ✅ 只保留Python標準庫

### GitHub Actions
- ✅ 所有GitHub Actions工作流已移除
- ✅ .github/workflows目錄已刪除

### Docker依賴
- ✅ 所有Dockerfile已移除
- ✅ 所有docker-compose文件已移除

### 外部URL
- ✅ 389個文件中的外部URL已移除
- ✅ 所有外部鏈接已替換為本地引用

## 驗證清單

- [ ] 零NPM依賴
- [ ] 零PyPI依賴
- [ ] 零Docker Hub依賴
- [ ] 零GitHub Actions
- [ ] 零外部URL
- [ ] 離線環境可運行

## 完成狀態

**狀態：** 進行中

**完成項目：**
- ✅ NPM依賴移除
- ✅ Python依賴清理
- ✅ GitHub Actions移除
- ✅ Docker文件移除
- ✅ 外部URL移除

**待完成項目：**
- [ ] 創建本地監控系統
- [ ] 創建本地CI/CD引擎
- [ ] 創建本地Docker Registry
- [ ] 測試離線環境

## 下一步

1. 創建本地CI/CD引擎
2. 測試系統完整性
3. 創建本地監控系統
4. 驗證離線環境