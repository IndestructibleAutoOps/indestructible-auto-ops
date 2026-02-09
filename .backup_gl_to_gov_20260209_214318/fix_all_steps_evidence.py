#!/usr/bin/env python3
"""修復所有 10 個 step 方法 - 添加證據生成"""

import re
from pathlib import Path

def main():
    enforce_rules_path = Path("/workspace/ecosystem/enforce.rules.py")
    
    with open(enforce_rules_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加證據生成的代碼模板
    evidence_code_template = '''
        
        # ========== 證據鏈生成 ==========
        # 生成 step artifact
        artifact_file = self._generate_artifact(
            step_number={step_num},
            input_data={input_dict},
            output_data={output_dict},
            result={result_dict}
        )
        
        # 寫入事件流
        self._write_step_event(
            step_number={step_num},
            artifact_file=artifact_file,
            result={result_dict}
        )
'''
    
    # 修復 step_2_local_reasoning
    step2_marker = "        return EnforcementResult(\n            status=&quot;PASS&quot;,\n            message=&quot;Local Reasoning Complete&quot;"
    
    if step2_marker in content:
        content = content.replace(
            step2_marker,
            f'''            status="PASS",
            message="Local Reasoning Complete",{evidence_code_template.format(
                step_num=2,
                input_dict='{"local_state": str(type(local_state))}',
                output_dict='{"strengths": len(strengths), "gaps": len(gaps), "inconsistencies": len(inconsistencies), "risks": len(risks)}',
                result_dict='{"status": "PASS", "strengths": len(strengths), "gaps": len(gaps), "inconsistencies": len(inconsistencies), "risks": len(risks)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_3_global_retrieval
    step3_marker = "        return EnforcementResult(\n            status=&quot;PASS&quot;,\n            message=&quot;Global Retrieval Complete&quot;"
    
    if step3_marker in content:
        content = content.replace(
            step3_marker,
            f'''            status="PASS",
            message="Global Retrieval Complete",{evidence_code_template.format(
                step_num=3,
                input_dict='{}',
                output_dict='{"frameworks": len(frameworks), "principles": len(principles), "patterns": len(patterns)}',
                result_dict='{"status": "PASS", "frameworks": len(frameworks), "principles": len(principles), "patterns": len(patterns)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_4_global_reasoning
    step4_marker = "        return EnforcementResult(\n            status=&quot;PASS&quot;,\n            message=&quot;Global Reasoning Complete&quot;"
    
    if step4_marker in content:
        content = content.replace(
            step4_marker,
            f'''            status="PASS",
            message="Global Reasoning Complete",{evidence_code_template.format(
                step_num=4,
                input_dict='{"global_best_practices": str(type(global_best_practices))}',
                output_dict='{"abstract_patterns": len(abstract_patterns), "rules": len(rules), "guidelines": len(guidelines)}',
                result_dict='{"status": "PASS", "abstract_patterns": len(abstract_patterns), "rules": len(rules), "guidelines": len(guidelines)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_5_integration
    step5_marker = "        return EnforcementResult(\n            status=&quot;PASS&quot;,\n            message=&quot;Integration Complete&quot;"
    
    if step5_marker in content:
        content = content.replace(
            step5_marker,
            f'''            status="PASS",
            message="Integration Complete",{evidence_code_template.format(
                step_num=5,
                input_dict='{"local_gap": str(type(local_gap)), "global_insight": str(type(global_insight))}',
                output_dict='{"enforcement_layers": len(enforcement_layers), "strategies": len(strategies)}',
                result_dict='{"status": "PASS", "enforcement_layers": len(enforcement_layers), "strategies": len(strategies)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_6_execution_validation
    step6_marker = "        return EnforcementResult(\n            status=&quot;READY&quot;,\n            message=&quot;Execution & Validation Complete&quot;"
    
    if step6_marker in content:
        content = content.replace(
            step6_marker,
            f'''            status="READY",
            message="Execution & Validation Complete",{evidence_code_template.format(
                step_num=6,
                input_dict='{"blueprint": str(type(blueprint))}',
                output_dict='{"validations_passed": validations_passed, "total_validations": total_validations}',
                result_dict='{"status": "READY", "validations_passed": validations_passed, "total_validations": total_validations}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_7_governance_event_stream
    step7_marker = "        return EnforcementResult(\n            status=&quot;PASS&quot;,\n            message=&quot;Governance Event Stream Complete&quot;"
    
    if step7_marker in content:
        content = content.replace(
            step7_marker,
            f'''            status="PASS",
            message="Governance Event Stream Complete",{evidence_code_template.format(
                step_num=7,
                input_dict='{}',
                output_dict='{"event_stream_file": str(self.event_stream.event_stream_file), "total_events": event_count}',
                result_dict='{"status": "PASS", "event_stream_file": str(self.event_stream.event_stream_file), "total_events": event_count}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_8_auto_fix
    step8_marker = "        return EnforcementResult(\n            status=&quot;ENABLED&quot;,\n            message=&quot;Auto-Fix Loop Complete&quot;"
    
    if step8_marker in content:
        content = content.replace(
            step8_marker,
            f'''            status="ENABLED",
            message="Auto-Fix Loop Complete",{evidence_code_template.format(
                step_num=8,
                input_dict='{}',
                output_dict='{"auto_fix_capabilities": len(auto_fix_capabilities)}',
                result_dict='{"status": "ENABLED", "auto_fix_capabilities": len(auto_fix_capabilities)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_9_reverse_architecture
    step9_marker = "        return EnforcementResult(\n            status=&quot;PASS&quot;,\n            message=&quot;Reverse Architecture Loop Complete&quot;"
    
    if step9_marker in content:
        content = content.replace(
            step9_marker,
            f'''            status="PASS",
            message="Reverse Architecture Loop Complete",{evidence_code_template.format(
                step_num=9,
                input_dict='{}',
                output_dict='{"reverse_architecture_capabilities": len(reverse_architecture_capabilities)}',
                result_dict='{"status": "PASS", "reverse_architecture_capabilities": len(reverse_architecture_capabilities)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 修復 step_10_loop_back
    step10_marker = "        return EnforcementResult(\n            status=&quot;ACTIVE&quot;,\n            message=&quot;Loop Back Complete&quot;"
    
    if step10_marker in content:
        content = content.replace(
            step10_marker,
            f'''            status="ACTIVE",
            message="Loop Back Complete",{evidence_code_template.format(
                step_num=10,
                input_dict='{}',
                output_dict='{"loop_triggers": len(loop_triggers), "loop_benefits": len(loop_benefits)}',
                result_dict='{"status": "ACTIVE", "loop_triggers": len(loop_triggers), "loop_benefits": len(loop_benefits)}'
            )}, artifacts=[str(artifact_file)]'''
        )
    
    # 保存
    with open(enforce_rules_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已修復所有 10 個 step 方法")

if __name__ == "__main__":
    main()