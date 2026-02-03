# 全面維修計劃 - MNGA 治理系統

## 1. 診斷階段 [x]
- [x] 檢查 Git 狀態 (7 個本地提交待推送)
- [x] 運行 enforce.py --audit (7/7 通過，但有警告)

## 2. 修復命名問題 [ ]
- [ ] 重命名 summarized_conversations → summarized-conversations
- [ ] 修復審計報告文件命名格式

## 3. 修復治理合約問題 [ ]
- [ ] 檢查 ecosystem/contracts/ 目錄結構
- [ ] 創建缺失的治理合約文件
- [ ] 驗證 governance_enforcer.py 的 before_operation 功能

## 4. 完整性檢查 [ ]
- [ ] 檢查 complete_naming_enforcer.py 整合狀態
- [ ] 驗證所有 16 種命名類型的實現
- [ ] 運行完整的命名治理掃描

## 5. 推送到 GitHub [ ]
- [ ] 提交所有修復
- [ ] 推送到遠端倉庫
- [ ] 驗證推送成功

## 6. 最終驗證 [ ]
- [ ] 運行 enforce.py --audit 確認所有問題已修復
- [ ] 生成最終報告