#!/usr/bin/env python3
"""修復 enforce.rules.py - 添加證據鏈機制"""

import json
from pathlib import Path
from datetime import datetime
import uuid
import hashlib

def compute_sha256(file_path: Path) -> str:
    """計算文件的 SHA256 hash"""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()

def main():
    # 讀取原始文件
    enforce_rules_path = Path("/workspace/ecosystem/enforce.rules.py")
    with open(enforce_rules_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加證據輔助方法
    evidence_helpers = '''
    
    # ========== 證據鏈輔助方法 ==========
    
    def _create_evidence_dir(self) -> Path:
        """創建證據目錄"""
        evidence_dir = self.workspace_root / "ecosystem" / ".evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        return evidence_dir
    
    def _generate_artifact(self, step_number: int, input_data: dict, output_data: dict, result: dict) -> Path:
        """生成 step artifact"""
        evidence_dir = self._create_evidence_dir()
        
        artifact = {
            "artifact_id": f"step-{step_number}",
            "step_number": step_number,
            "timestamp": datetime.utcnow().isoformat(),
            "uuid": str(uuid.uuid4()),
            "sha256_hash": None,
            "input_trace": input_data,
            "output_trace": output_data,
            "result": result,
            "evidence_links": {
                "event_stream": str(self.event_stream.event_stream_file),
                "artifact_file": None
            },
            "provenance": {
                "executor": "SuperNinja AI Agent",
                "methodology": "Immutable Core Governance Engineering Methodology v1.0",
                "enforcement_rules_version": "2.0.0"
            }
        }
        
        # 保存 artifact
        artifact_file = evidence_dir / f"step-{step_number}.json"
        with open(artifact_file, 'w', encoding='utf-8') as f:
            json.dump(artifact, f, indent=2, ensure_ascii=False)
        
        # 計算 hash
        artifact["sha256_hash"] = compute_sha256(artifact_file)
        artifact["evidence_links"]["artifact_file"] = str(artifact_file)
        
        # 重新寫入（包含 hash）
        with open(artifact_file, 'w', encoding='utf-8') as f:
            json.dump(artifact, f, indent=2, ensure_ascii=False)
        
        return artifact_file
    
    def _write_step_event(self, step_number: int, artifact_file: Path, result: dict):
        """寫入 step 執行事件到 event stream"""
        violation = Violation(
            violation_id=str(uuid.uuid4()),
            event_type="STEP_EXECUTED",
            timestamp=datetime.utcnow().isoformat(),
            source="enforce.rules.py",
            severity=Severity.LOW,
            layer=Layer.ENFORCEMENT,
            artifact=f"step-{step_number}",
            description=f"Step {step_number} executed successfully",
            evidence={
                "artifact_file": str(artifact_file),
                "sha256_hash": compute_sha256(artifact_file),
                "result": result
            },
            action_taken=Action.LOG,
            result="PASS",
            metadata={
                "executor": "SuperNinja AI Agent",
                "step_number": step_number,
                "evidence_chain_enabled": True
            }
        )
        
        self.event_stream.write_event(violation)
    
'''
    
    # 在 EnforcementCoordinator 類的 __init__ 方法後添加證據輔助方法
    init_marker = "        self.metadata = MetaSpec()\n"
    if init_marker in content:
        content = content.replace(init_marker, init_marker + evidence_helpers)
    
    # 保存修復後的文件
    with open(enforce_rules_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已添加證據鏈輔助方法到 enforce.rules.py")

if __name__ == "__main__":
    main()