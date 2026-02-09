# 外部依賴移除策略 - 全面自給自足平台

## 策略概述

將專案轉換為第一個完全自給自足的平台，移除所有外部依賴、映射和引用。

## 依賴分析結果

### 1. NPM 依賴（主要問題）

#### 受影響的文件：
- `package-lock.json` 文件（多個位置）
- 包含數百個NPM註冊表引用

#### 當前狀態：
- 每個 `package-lock.json` 包含306-1311個外部URL引用
- 所有引用指向 `https://registry.npmjs.org`
- 這些是構建時依賴，不是運行時依賴

### 2. GitHub Actions 依賴

#### 受影響的文件：
- `.github/workflows/*.yml` 文件（145個文件）
- 包含大量 `uses: actions/xxx@xxx` 引用

#### 當前狀態：
- 145個GitHub工作流文件包含外部動作引用
- 這些是CI/CD流程依賴

### 3. Python 依賴

#### 受影響的文件：
- `requirements.txt` 文件（多個位置）
- 包含PyPI包引用

#### 當前狀態：
- Python包管理器依賴（如numpy、scipy、qiskit）

## 移除策略

### 階段1：識別和分類依賴

#### 1.1 建構依賴 vs 運行時依賴

**建構依賴（可以移除）：**
- NPM packages用於開發環境
- GitHub Actions用於CI/CD流程
- Python包用於開發和測試

**運行時依賴（需要保留）：**
- 系統運行時必要的核心依賴
- 平台運行所需的核心庫

#### 1.2 分類依賴類型

1. **註冊表依賴**：NPM、PyPI、Docker Hub引用
2. **CI/CD依賴**：GitHub Actions、外部構建工具
3. **配置依賴**：外部配置服務、監控服務
4. **文檔依賴**：外部文檔鏈接、參考鏈接

### 階段2：移除策略

#### 2.1 NPM依賴移除

**策略A：本地化依賴（推薦）**
```yaml
動作：
1. 提取所有必需的NPM包源碼
2. 將其納入專案本地存儲
3. 更新package.json指向本地包
4. 禁用npm registry訪問

實施步驟：
- 創建本地NPM包存儲：gov-local-packages/
- 提取核心依賴源碼
- 修改package.json的依賴路徑
- 設置本地npm配置
```

**策略B：完全移除（激進）**
```yaml
動作：
1. 移除所有package.json和package-lock.json
2. 將核心功能重構為不依賴NPM的純Python/Go/Rust實現
3. 移除node_modules目錄

適用場景：
- 平台不使用任何JavaScript
- 所有JavaScript功能可以用其他語言實現
```

#### 2.2 GitHub Actions移除

**策略A：自託管CI/CD**
```yaml
動作：
1. 創建本地CI/CD基礎設施
2. 替換所有GitHub Actions為本地腳本
3. 使用本地Docker容器進行構建

實施步驟：
- 在gl-execution-runtime中創建本地CI/CD引擎
- 將GitHub Actions工作流轉換為本地腳本
- 使用本地Docker Registry
```

**策略B：簡化CI/CD**
```yaml
動作：
1. 保留最基本的GitHub Actions（checkout、upload）
2. 移除所有第三方Actions
3. 使用原生shell腳本替代

實施步驟：
- 只保留actions/checkout@v6
- 移除所有actions/setup-*動作
- 直接在workflow中執行命令
```

#### 2.3 Python依賴移除

**策略A：本地化Python包**
```yaml
動作：
1. 提取所有必需的Python包源碼
2. 創建本地Python包存儲
3. 更新requirements.txt指向本地包

實施步驟：
- 創建gl-local-python-packages/
- 下載核心包源碼
- 修改導入路徑
```

**策略B：重構為純標準庫**
```yaml
動作：
1. 用Python標準庫替換第三方包
2. 重寫依賴第三方包的代碼
3. 創建自定義實現

實施步驟：
- 移除numpy依賴，使用純Python實現
- 移除scipy依賴，創建自定義算法
- 移除PyYAML，使用標準庫json模塊
```

### 階段3：實施優先級

#### 3.1 高優先級（立即執行）

1. **移除NPM註冊表引用**
   - 替換所有 `https://registry.npmjs.org` 引用
   - 使用本地包或完全移除

2. **簡化GitHub Actions**
   - 移除所有第三方Actions
   - 只保留核心的checkout和upload功能

3. **本地化Python依賴**
   - 提取核心Python包源碼
   - 創建本地包存儲

#### 3.2 中優先級（下一階段）

1. **移除Docker Hub依賴**
   - 使用本地Docker Registry
   - 或使用無基礎鏡像構建

2. **移除監控服務依賴**
   - 替換Prometheus/Grafana為本地實現
   - 創建本地監控系統

3. **移除文檔外部鏈接**
   - 內文說明替代外部參考
   - 創建本地知識庫

#### 3.3 低優先級（可選）

1. **完全移除package.json**
   - 如果不使用JavaScript，完全移除Node.js依賴

2. **移除所有registry.npmjs.org引用**
   - 創建完整的本地包生態

## 實施計劃

### 第一步：創建本地基礎設施

```bash
# 創建本地包存儲結構
mkdir -p gov-local-packages/npm
mkdir -p gov-local-packages/python
mkdir -p gov-local-packages/docker
```

### 第二步：提取核心依賴

```bash
# 提取NPM核心包
# 提取Python核心包
# 提取Docker鏡像
```

### 第三步：更新配置

```yaml
# 更新package.json
# 更新requirements.txt
# 更新Dockerfile
# 更新GitHub Actions
```

### 第四步：驗證和測試

```bash
# 測試本地構建
# 測試本地CI/CD
# 測試運行時功能
```

## 預期結果

### 完全自給自足平台特性

1. **無外部網絡依賴**
   - 離線環境可運行
   - 完全本地化構建

2. **無外部服務依賴**
   - 不依賴任何外部API
   - 自託管所有服務

3. **無外部註冊表依賴**
   - 本地包管理
   - 本地Docker Registry

4. **無外部文檔依賴**
   - 完整本地文檔
   - 內建知識庫

## 風險評估

### 高風險

1. **維護負擔增加**
   - 需要維護本地包
   - 安全更新需要手動處理

2. **功能受限**
   - 無法使用最新的第三方庫
   - 需要自行開發功能

### 中風險

1. **構建時間增加**
   - 本地構建可能更慢
   - 需要更多存儲空間

2. **兼容性問題**
   - 本地包可能有兼容性問題

### 低風險

1. **學習曲線**
   - 需要學習本地包管理
   - 需要了解CI/CD替代方案

## 建議

### 推薦策略

**混合方法：**
1. 將運行時核心依賴本地化
2. 移除所有開發時外部依賴
3. 創建自託管的CI/CD基礎設施
4. 保留可選的外部依賴（用戶可選擇）

### 實施順序

1. **Week 1-2：** 依賴分析和分類
2. **Week 3-4：** 高優先級依賴移除
3. **Week 5-6：** 中優先級依賴移除
4. **Week 7-8：** 測試和驗證
5. **Week 9-10：** 文檔和完善

## 成功標準

1. ✅ 零外部註冊表依賴
2. ✅ 零外部服務依賴
3. ✅ 離線環境可運行
4. ✅ 完整本地文檔
5. ✅ 自託管CI/CD

## 結論

通過系統化地移除所有外部依賴，我們將創建一個完全自給自足的平台，這將是專案中第一個達到此標準的全面完成平台。這需要大量的重構工作，但將提供最大的自主性和控制力。