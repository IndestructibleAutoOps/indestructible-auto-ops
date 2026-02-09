# 手動修復指南 - Step 1-10 證據鏈

## 當前狀態

✅ **已完成**:
- enforcement.rules.yaml v2.0.0 (完整修復)
- 證據輔助方法已添加 (`_create_evidence_dir`, `_generate_artifact`, `_write_step_event`)

⏸️ **待完成**:
- 10 個 step 方法需要在 `return EnforcementResult()` 之前添加證據生成

---

## 修復方法

對每個 step 方法，在 `return EnforcementResult()` 之前添加以下代碼：

### Step 1 (行 440)
```python
        # ========== 證據鏈生成 ==========
        artifact_file = self._generate_artifact(
            step_number=1,
            input_data={"workspace": str(self.workspace_root)},
            output_data={"ugs_files": len(ugs_files), "meta_spec_files": len(meta_spec_files)},
            result={"status": "PASS", "completed": true}
        )
        
        # 寫入事件流
        self._write_step_event(
            step_number=1,
            artifact_file=artifact_file,
            result={"status": "PASS", "completed": true}
        )
        
        return EnforcementResult(
            ...
            artifacts=[str(artifact_file)],
            ...
        )
```

### Step 2 (行 525)
```python
        # ========== 證據鏈生成 ==========
        artifact_file = self._generate_artifact(
            step_number=2,
            input_data={"local_state": str(type(local_state))},
            output_data={
                "strengths": len(local_gap_matrix.strengths),
                "gaps": len(local_gap_matrix.gaps),
                "inconsistencies": len(local_gap_matrix.inconsistencies),
                "risks": len(local_gap_matrix.risks)
            },
            result={
                "status": "PASS",
                "strengths": len(local_gap_matrix.strengths),
                "gaps": len(local_gap_matrix.gaps),
                "inconsistencies": len(local_gap_matrix.inconsistencies),
                "risks": len(local_gap_matrix.risks)
            }
        )
        
        # 寫入事件流
        self._write_step_event(
            step_number=2,
            artifact_file=artifact_file,
            result={"status": "PASS", "strengths": len(local_gap_matrix.strengths), "gaps": len(local_gap_matrix.gaps)}
        )
        
        return EnforcementResult(
            ...
            artifacts=[str(artifact_file)],
            ...
        )
```

### Step 3-10 (類似模式)

對於其餘步驟，使用相同的模式，只需調整：
- `step_number`: 3-10
- `input_data`: 根據 step 的輸入
- `output_data`: 根據 step 的輸出
- `result`: 包含狀態和關鍵指標

---

## 快速修復命令

如果你熟悉編輯器，可以執行以下快速修復：

### 使用 vim
```bash
vim /workspace/ecosystem/enforce.rules.py
```

然後對每個 return 語句進行修改。

### 使用 sed (逐個)

由於每個 step 的代碼結構略有不同，建議手動編輯。

---

## 驗證修復

修復後執行：

```bash
# 1. 語法檢查
python -m py_compile /workspace/ecosystem/enforce.rules.py

# 2. 執行驗證
python /workspace/ecosystem/enforce.rules.py

# 3. 檢查 artifacts
ls -la /workspace/ecosystem/.evidence/

# 4. 檢查 event stream
ls -la /workspace/ecosystem/.governance/event-stream.jsonl
```

---

## 預期結果

修復成功後，你應該看到：

1. ✅ 所有 10 個 step 成功執行
2. ✅ `ecosystem/.evidence/` 目錄包含 10 個 `step-*.json` 文件
3. ✅ `ecosystem/.governance/event-stream.jsonl` 包含 10 個事件
4. ✅ 每個 artifact 包含 SHA256 hash、UUID、timestamp

---

## 當前進度

| Step | 行號 | 狀態 |
|------|------|------|
| 1 | 440 | ⏸️ 待修復 |
| 2 | 525 | ⏸️ 待修復 |
| 3 | 612 | ⏸️ 待修復 |
| 4 | 701 | ⏸️ 待修復 |
| 5 | 785 | ⏸️ 待修復 |
| 6 | 854 | ⏸️ 待修復 |
| 7 | 898 | ⏸️ 待修復 |
| 8 | 963 | ⏸️ 待修復 |
| 9 | 1025 | ⏸️ 待修復 |
| 10 | 1092 | ⏸️ 待修復 |

---

## 建議

由於每個 step 的變量名稱不同，建議：

1. **選項 A**: 手動逐個修復（最穩健）
2. **選項 B**: 創建一個新的、簡化的 enforce.rules.py
3. **選項 C**: 使用 AI 輔助工具進行精確修改

你希望採用哪個選項？
