# GL 平台整合計劃

**日期**: 2026-02-06  
**狀態**: 提案階段  
**目標**: 將 26 個分散的 GL 平台整合到統一的架構結構中

## 問題分析

### 當前狀況
- **平台數量**: 26 個 GL-* 平台文件夾
- **位置**: 全部在根目錄，造成混亂
- **重複**: 多個平台有重複功能和內容
- **維護困難**: 分散式結構不易管理

### 發現的平台列表

#### GL00-09 層（企業架構）
1. `gl-enterprise-architecture/` (100K)
2. `gl-governance-architecture-platform/` (2.9M)

#### GL10-29 層（平台服務）
3. `gl-platform-services/` (12K)
4. `gl-platform-core-platform/` (292K)

#### GL20-29 層（數據處理）
5. `gl-data-processing/` (12K)
6. `gl-data-processing-platform/` (284K)
7. `gl-search-elasticsearch-platform/` (?)

#### GL30-49 層（執行運行時）
8. `gl-execution-runtime/` (12K)
9. `gl-runtime-execution-platform/` (80K)
10. `gl-runtime-engine-platform/` (7.6M - 最大)
11. `gl-runtime-services-platform/` (1.8M)

#### GL50-59 層（監控可觀測性）
12. `gl-monitoring-observability-platform/` (52K)
13. `gl-monitoring-system-platform/` (200K)
14. `gl-observability/` (12K)

#### GL60-80 層（治理合規）
15. `gl-governance-compliance/` (488K)
16. `gl-governance-compliance-platform/` (504K)

#### GL81-83 層（擴展服務）
17. `gl-extension-services/` (12K)
18. `gl-extension-services-platform/` (12K)
19. `gl-integration-hub-platform/` (36K)

#### GL90-99 層（元規範）
20. `gl-meta-specifications/` (12K)
21. `gl-meta-specifications-platform/` (12K)
22. `gl-semantic-core-platform/` (76K)

#### 專項平台
23. `gl-automation-instant-platform/` (724K)
24. `gl-automation-organizer-platform/` (136K)
25. `gl-quantum-computing-platform/` (328K)
26. `gl-infrastructure-foundation-platform/` (1.2M)

**總大小**: 約 16+ MB

---

## 整合策略

### 方案 A：按 GL 層級整合（推薦）✅

將所有平台按照 GL 架構層級整合到對應的標準目錄：

```
workspace/
├── gl00-09-enterprise-architecture/
│   ├── governance/          # 合併 gl-governance-architecture-platform
│   └── specifications/      # 合併 gl-enterprise-architecture
│
├── gl10-19-platform-services/
│   ├── core/                # 合併 gl-platform-core-platform
│   └── services/            # 合併 gl-platform-services
│
├── gl20-29-data-processing/
│   ├── processing/          # 合併 gl-data-processing*
│   └── search/              # 合併 gl-search-elasticsearch-platform
│
├── gl30-49-runtime-execution/
│   ├── engine/              # 合併 gl-runtime-engine-platform
│   ├── execution/           # 合併 gl-runtime-execution-platform
│   └── services/            # 合併 gl-runtime-services-platform
│
├── gl50-59-monitoring-observability/
│   ├── monitoring/          # 合併 gl-monitoring-*
│   └── observability/       # 合併 gl-observability
│
├── gl60-80-governance-compliance/
│   └── compliance/          # 合併所有 gl-governance-compliance*
│
├── gl81-83-extension-services/
│   ├── extensions/          # 合併 gl-extension-services*
│   └── integrations/        # 合併 gl-integration-hub-platform
│
├── gl90-99-meta-specifications/
│   ├── specifications/      # 合併 gl-meta-specifications*
│   └── semantic-core/       # 合併 gl-semantic-core-platform
│
└── platforms/               # 專項平台（保留現有）
    ├── automation/          # 合併 gl-automation-*
    ├── quantum/             # 合併 gl-quantum-computing-platform
    └── infrastructure/      # 合併 gl-infrastructure-foundation-platform
```

### 方案 B：單一 platforms 目錄

```
workspace/
└── platforms/
    ├── gl00-enterprise/
    ├── gl10-services/
    ├── gl20-data/
    ├── gl30-runtime/
    ├── gl50-monitoring/
    ├── gl60-governance/
    ├── gl81-extensions/
    └── gl90-meta/
```

### 方案 C：保留關鍵，歸檔其他

保留 5-8 個核心平台，將其他歸檔到 `archives/legacy-platforms/`

---

## 推薦執行計劃（方案 A）

### Phase 1: 準備階段（1 小時）

1. **備份當前狀態**
   ```bash
   git add -A
   git commit -m "backup: before platform consolidation"
   git tag platform-consolidation-backup
   ```

2. **創建新的目錄結構**
   ```bash
   mkdir -p gl{00-09,10-19,20-29,30-49,50-59,60-80,81-83,90-99}-*/
   ```

3. **生成遷移映射表**
   - 記錄每個文件的原位置和目標位置
   - 生成自動化腳本

### Phase 2: 遷移執行（2-3 小時）

#### 步驟 1: 治理層（GL00-09, GL60-80）
```bash
# 合併治理相關平台
rsync -av gl-governance-architecture-platform/ gl00-09-enterprise-architecture/governance/
rsync -av gl-governance-compliance*/ gl60-80-governance-compliance/compliance/
```

#### 步驟 2: 運行時層（GL30-49）
```bash
# 合併運行時平台（最大的平台）
rsync -av gl-runtime-engine-platform/ gl30-49-runtime-execution/engine/
rsync -av gl-runtime-execution-platform/ gl30-49-runtime-execution/execution/
rsync -av gl-runtime-services-platform/ gl30-49-runtime-execution/services/
```

#### 步驟 3: 其他層級
```bash
# 數據處理層
rsync -av gl-data-processing*/ gl20-29-data-processing/

# 監控層
rsync -av gl-monitoring-*/ gl50-59-monitoring-observability/
rsync -av gl-observability/ gl50-59-monitoring-observability/

# 擴展服務層
rsync -av gl-extension-services*/ gl81-83-extension-services/
rsync -av gl-integration-hub-platform/ gl81-83-extension-services/integrations/

# 元規範層
rsync -av gl-meta-specifications*/ gl90-99-meta-specifications/
rsync -av gl-semantic-core-platform/ gl90-99-meta-specifications/semantic-core/
```

#### 步驟 4: 專項平台
```bash
# 移動到 platforms/ 目錄
mv gl-automation-* platforms/automation/
mv gl-quantum-computing-platform platforms/quantum/
mv gl-infrastructure-foundation-platform platforms/infrastructure/
```

### Phase 3: 清理階段（1 小時）

1. **驗證遷移完整性**
   ```bash
   # 比對文件數量和大小
   python3 tools/verify-migration.py
   ```

2. **更新所有路徑引用**
   ```bash
   # 更新 imports, configs, 文檔
   python3 tools/update-references.py
   ```

3. **刪除舊目錄**
   ```bash
   # 只在驗證通過後執行
   rm -rf gl-*-platform/ gl-*-services/
   ```

4. **測試系統功能**
   ```bash
   pytest tests/ -v
   npm run validate:gl
   ```

### Phase 4: 文檔更新（30分鐘）

1. 更新 README.md 中的目錄結構
2. 更新 ARCHITECTURE.md
3. 生成遷移報告
4. 更新開發文檔

---

## 預期效果

### 優勢
✅ **清晰的層級結構** - 符合 GL 架構設計  
✅ **易於維護** - 相關功能集中管理  
✅ **減少重複** - 消除冗餘平台  
✅ **提升開發體驗** - 容易找到對應代碼  
✅ **符合規範** - 遵循 GL 命名約定  

### 風險評估

| 風險 | 等級 | 緩解措施 |
|------|------|----------|
| 路徑引用破壞 | 中 | 自動化更新工具 + 全面測試 |
| 文件遺失 | 低 | Git 備份 + 驗證腳本 |
| 開發中斷 | 中 | 分階段執行 + 回滾計劃 |
| CI/CD 失敗 | 中 | 更新 workflow 配置 |

---

## 實施時間表

| 階段 | 時間 | 輸出 |
|------|------|------|
| Phase 1: 準備 | 1 小時 | 備份 + 目錄結構 |
| Phase 2: 遷移 | 2-3 小時 | 完成文件移動 |
| Phase 3: 清理 | 1 小時 | 驗證 + 測試 |
| Phase 4: 文檔 | 30 分鐘 | 更新文檔 |
| **總計** | **4.5-5.5 小時** | **完整整合** |

---

## 自動化腳本示例

### 遷移腳本 (`tools/consolidate-platforms.sh`)

```bash
#!/bin/bash
set -e

echo "🚀 Starting Platform Consolidation..."

# Phase 1: Backup
git add -A
git commit -m "backup: before platform consolidation" || true
git tag platform-consolidation-backup-$(date +%Y%m%d-%H%M%S)

# Phase 2: Create new structure
echo "📁 Creating new directory structure..."
for layer in "00-09-enterprise-architecture" \
             "10-19-platform-services" \
             "20-29-data-processing" \
             "30-49-runtime-execution" \
             "50-59-monitoring-observability" \
             "60-80-governance-compliance" \
             "81-83-extension-services" \
             "90-99-meta-specifications"; do
    mkdir -p "gl${layer}"
done

# Phase 3: Migrate platforms
echo "🔄 Migrating platforms..."
source tools/migration-mapping.sh

# Phase 4: Verify
echo "✅ Verifying migration..."
python3 tools/verify-migration.py

echo "✨ Platform consolidation complete!"
```

---

## 回滾計劃

如果整合出現問題：

```bash
# 方案 1: Git 回滾
git reset --hard platform-consolidation-backup

# 方案 2: 恢復特定文件
git checkout platform-consolidation-backup -- gl-*-platform/

# 方案 3: Cherry-pick 好的更改
git cherry-pick <good-commits>
```

---

## 下一步行動

### 立即執行（推薦）
1. ✅ 審查此計劃
2. 建議修改點
3. 開始 Phase 1（備份）
4. 執行自動化遷移

### 延後執行
1. 標記為 TODO
2. 創建 GitHub Issue
3. 計劃下次重構時間

---

## 決策點

**請選擇執行方案**：

- [ ] **方案 A**: 按 GL 層級整合（推薦，4-5 小時）
- [ ] **方案 B**: 單一 platforms 目錄（簡單，2-3 小時）
- [ ] **方案 C**: 保留關鍵平台（最快，1 小時）
- [ ] **延後**: 創建 Issue，稍後處理

**是否立即開始**：
- [ ] 是，立即執行 Phase 1（備份）
- [ ] 否，需要進一步討論

---

**創建者**: Cursor Cloud Agent  
**日期**: 2026-02-06  
**相關文檔**: ARCHITECTURE.md, README.md
