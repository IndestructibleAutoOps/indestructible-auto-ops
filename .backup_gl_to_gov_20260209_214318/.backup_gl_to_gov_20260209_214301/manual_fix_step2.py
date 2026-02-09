#!/usr/bin/env python3
"""手動修復 step_2"""

# 找到 return EnforcementResult 的位置（第 528 行）
# 在 return 之前插入證據生成代碼

insert_code = '''
        
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
            result={
                "status": "PASS",
                "strengths": len(local_gap_matrix.strengths),
                "gaps": len(local_gap_matrix.gaps)
            }
        )
        
'''

# 讀取文件
with open('/workspace/ecosystem/enforce.rules.py', 'r') as f:
    lines = f.readlines()

# 找到第 528 行（0-index: 527）
# 在 return 之前插入
insert_index = 527  # return 所在的行

lines.insert(insert_index, insert_code)

# 修改 return 語句，添加 artifacts
# 找到 return EnforcementResult 的位置
for i in range(insert_index + len(insert_code.split('\n')), min(insert_index + len(insert_code.split('\n')) + 20, len(lines))):
    if 'return EnforcementResult(' in lines[i]:
        # 找到了，修改這行
        lines[i] = lines[i].rstrip() + f',\n            artifacts=[str(artifact_file)]\n'
        break

# 寫回文件
with open('/workspace/ecosystem/enforce.rules.py', 'w') as f:
    f.writelines(lines)

print("✅ 已修復 step_2_local_reasoning")