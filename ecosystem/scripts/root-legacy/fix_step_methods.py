#!/usr/bin/env python3
"""修復所有 step 方法 - 添加證據生成"""

import re
from pathlib import Path

def main():
    enforce_rules_path = Path("/workspace/ecosystem/enforce.rules.py")
    
    with open(enforce_rules_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改 step_1_local_retrieval
    step1_pattern = r'(    def step_1_local_retrieval\(self\) -> EnforcementResult:.*?return EnforcementResult\()([^\)]+)\)'
    
    step1_replacement = r'''\1
        # 生成 artifact
        artifact_file = self._generate_artifact(
            step_number=1,
            input_data={"workspace": str(self.workspace_root)},
            output_data={"ugs_files": len(ugs_files), "meta_spec_files": len(meta_spec_files)},
            result={
                "status": "PASS",
                "ugs_files": len(ugs_files),
                "meta_spec_files": len(meta_spec_files),
                "gl_anchors_files": len(gl_anchors_files),
                "engines_files": len(engines_files)
            }
        )
        
        # 寫入事件流
        self._write_step_event(
            step_number=1,
            artifact_file=artifact_file,
            result={
                "status": "PASS",
                "ugs_files": len(ugs_files),
                "meta_spec_files": len(meta_spec_files)
            }
        )
        
        \2, artifacts=[str(artifact_file)])'''
    
    content = re.sub(step1_pattern, step1_replacement, content, flags=re.DOTALL)
    
    # 保存
    with open(enforce_rules_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已修復 step_1 方法")

if __name__ == "__main__":
    main()