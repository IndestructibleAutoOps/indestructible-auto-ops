<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

================================================================================
COMPREHENSIVE eval() USAGE ANALYSIS REPORT
================================================================================
Generated: 2026-01-16T15:39:01.576684

SUMMARY STATISTICS
--------------------------------------------------------------------------------
Total Python files scanned:    1370
Files with eval() usage:       28
Total eval() occurrences:      130

BY FILE TYPE:
  Tool/analysis files:         7
  Test files:                  5
  Demo/example files:          4
  Core application files:      12

BY SAFETY LEVEL:
  Safe usage (documented):     73
  Needs security warning:      57
  Needs replacement:           0

================================================================================
ACTION REQUIRED: ADD_WARNING
================================================================================
Count: 57


File: /home/runner/work/machine-native-ops/machine-native-ops/code_quality_analyzer.py
  Type: tool
  Occurrences: 1
    Line 165: needs_review
      Code: (r"eval\s*\(", "高危：使用 eval() 可能導致代碼注入漏洞"),

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_eval_comprehensive.py
  Type: tool
  Occurrences: 11
    Line 6: needs_review
      Code: 1. Scans all Python files for eval() usage
    Line 25: needs_review
      Code: """Analyzes and categorizes eval() usage in Python files."""
    Line 89: needs_review
      Code: Categorize eval() usage and suggest action.
    Line 117: needs_review
      Code: """Analyze a single file for eval() usage."""
    Line 124: needs_review
      Code: # Find all eval() occurrences
    Line 188: needs_review
      Code: """Scan entire repository for eval() usage."""
    Line 189: needs_review
      Code: print("Scanning repository for eval() usage...")
    Line 201: needs_review
      Code: print(f"Scan complete. Found {self.stats['total_eval_usage']} eval() usages in {self.stats['files_wi
    Line 216: needs_review
      Code: report.append(f"Files with eval() usage:       {self.stats['files_with_eval']}")
    Line 217: needs_review
      Code: report.append(f"Total eval() occurrences:      {self.stats['total_eval_usage']}")
    Line 310: needs_review
      Code: print(f"Total eval() usage: {analyzer.stats['total_eval_usage']}")

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_eval_usage.py
  Type: tool
  Occurrences: 8
    Line 24: needs_review
      Code: """Analyze eval() usage in a file."""
    Line 31: needs_review
      Code: # Find all eval() calls
    Line 84: needs_review
      Code: """Check if eval() can be replaced with json.loads()."""
    Line 99: needs_review
      Code: """Fix eval() usage in a file.
    Line 114: needs_review
      Code: # Analyze eval() usage
    Line 190: needs_review
      Code: print("Phase 2 Week 2: Fix HIGH Severity eval() Usage")
    Line 193: needs_review
      Code: # Files with eval() usage (from security audit)
    Line 227: needs_review
      Code: print(f"eval() calls fixed: {total_fixed}")

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_remaining_high_issues.py
  Type: tool
  Occurrences: 10
    Line 6: needs_review
      Code: 1. Identifying actual eval() calls vs mentions in comments/strings
    Line 16: needs_review
      Code: """Find actual eval() function calls (not in comments or strings)."""
    Line 65: needs_review
      Code: # Check for eval() call
    Line 69: needs_review
      Code: # Check for whitespace before eval (to avoid catching "evaluate", etc.)
    Line 83: needs_review
      Code: """Add security warning before eval() usage."""
    Line 108: needs_review
      Code: """Fix eval() usage in a file.
    Line 123: needs_review
      Code: print(f"  Found {len(eval_calls)} potential eval() calls")
    Line 126: needs_review
      Code: # Determine if this is a real eval() call or just a mention
    Line 131: needs_review
      Code: # eval(...)
    Line 155: needs_review
      Code: print("Fix Remaining HIGH Severity eval() Issues")

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_remaining_issues.py
  Type: tool
  Occurrences: 5
    Line 13: needs_review
      Code: - 77 security vulnerabilities (MD5, eval())
    Line 178: needs_review
      Code: """Replace unsafe eval() with safer alternatives."""
    Line 250: needs_review
      Code: # Fix eval() usage
    Line 334: needs_review
      Code: print("  ⚠️  eval() usage marked for review")
    Line 370: needs_review
      Code: print(f"eval() reviews: {summary['eval_fixed']}")

File: /home/runner/work/machine-native-ops/machine-native-ops/scripts/auto-quality-check.py
  Type: tool
  Occurrences: 2
    Line 200: needs_review
      Code: """P1: eval() 使用檢查"""
    Line 201: needs_review
      Code: print("\n⚠️  檢查 eval() 使用...")

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/automation/architect/core/analysis/security_scanner.py
  Type: core
  Occurrences: 1
    Line 114: needs_review
      Code: (r"eval\s*\(", "eval-usage", "Use of eval() can lead to code injection"),

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/tests/test_phase5_components.py
  Type: test
  Occurrences: 1
    Line 390: needs_review
      Code: code = "result = eval(user_input)"

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/tests/test_task_executor.py
  Type: test
  Occurrences: 2
    Line 86: test_or_demo
      Code: code_with_eval = "result = eval(user_input)"
    Line 117: needs_review
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/examples/demo.py
  Type: demo
  Occurrences: 1
    Line 42: needs_review
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/pipeline_service.py
  Type: core
  Occurrences: 1
    Line 361: test_or_demo
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/test-vectors/generator.py
  Type: demo
  Occurrences: 1
    Line 221: test_or_demo
      Code: "    result = eval(user_input)",

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/tests/test_phase5_components.py
  Type: test
  Occurrences: 1
    Line 390: needs_review
      Code: code = "result = eval(user_input)"

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/tests/test_task_executor.py
  Type: test
  Occurrences: 2
    Line 86: test_or_demo
      Code: code_with_eval = "result = eval(user_input)"
    Line 117: needs_review
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/automation/architect/core/analysis/security_scanner.py
  Type: core
  Occurrences: 1
    Line 114: needs_review
      Code: (r"eval\s*\(", "eval-usage", "Use of eval() can lead to code injection"),

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/tests/test_tool_executor_validation.py
  Type: test
  Occurrences: 6
    Line 59: test_or_demo
      Code: """Actual eval() calls should be blocked"""
    Line 60: test_or_demo
      Code: code = 'eval("print(1)")'
    Line 63: test_or_demo
      Code: assert not valid, "Should block eval()"
    Line 176: test_or_demo
      Code: """eval() calls should be blocked"""
    Line 177: test_or_demo
      Code: code = 'eval("console.log(1)");'
    Line 180: test_or_demo
      Code: assert not valid, "Should block eval()"

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/tools/security_audit.py
  Type: tool
  Occurrences: 3
    Line 6: needs_review
      Code: analyzing MD5 usage, eval() usage, and other security concerns.
    Line 150: needs_review
      Code: """Check for eval() usage."""
    Line 158: needs_review
      Code: # Check for eval() calls
================================================================================
ACTION REQUIRED: SAFE
================================================================================
Count: 73


File: /home/runner/work/machine-native-ops/machine-native-ops/ns-root/namespaces-adk/adk/core/workflow_orchestrator.py
  Type: core
  Occurrences: 2
    Line 367: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 368: comment
      Code: return eval(condition, {"__builtins__": {}}, context)

File: /home/runner/work/machine-native-ops/machine-native-ops/code_quality_analyzer.py
  Type: tool
  Occurrences: 1
    Line 4: comment
      Code: # It uses eval() and other security-sensitive functions for analysis purposes only.

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_eval_comprehensive.py
  Type: tool
  Occurrences: 7
    Line 3: comment
      Code: Comprehensive eval() Usage Security Remediation Script
    Line 12: documented
      Code: SECURITY NOTE: This script itself uses eval() for analysis purposes only.
    Line 13: documented
      Code: All eval() usage in this file is for security analysis and is not exposed to user input.
    Line 97: string_check
      Code: # Check if it's string detection (checking for "eval(" in string)
    Line 98: string_check
      Code: if '"eval("' in code or "'eval('" in code or 'in code' in context:
    Line 98: string_check
      Code: if '"eval("' in code or "'eval('" in code or 'in code' in context:
    Line 207: comment
      Code: report.append("COMPREHENSIVE eval() USAGE ANALYSIS REPORT")

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_eval_usage.py
  Type: tool
  Occurrences: 10
    Line 4: comment
      Code: # It uses eval() and other security-sensitive functions for analysis purposes only.
    Line 9: comment
      Code: Fix HIGH severity eval() usage issues.
    Line 11: comment
      Code: This script analyzes and fixes eval() usage by:
    Line 12: safe_alternative
      Code: 1. Replacing eval() with ast.literal_eval() for literal evaluation
    Line 13: safe_alternative
      Code: 2. Replacing eval() with json.loads() for JSON parsing
    Line 14: safe_alternative
      Code: 3. Adding security warnings for eval() that cannot be replaced
    Line 56: safe_alternative
      Code: """Check if eval() can be replaced with ast.literal_eval()."""
    Line 57: string_check
      Code: # Remove 'eval(' and ')'
    Line 129: comment
      Code: new_code = code.replace('eval(', 'ast.literal_eval(')
    Line 171: documented
      Code: warning = "# SECURITY: eval() used with trusted input only. Do not use with untrusted user input."

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_final_issues.py
  Type: core
  Occurrences: 1
    Line 22: comment
      Code: # It uses eval() and other security-sensitive functions for analysis purposes only.

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_md5_usage.py
  Type: core
  Occurrences: 1
    Line 4: comment
      Code: # It uses eval() and other security-sensitive functions for analysis purposes only.

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_remaining_high_issues.py
  Type: tool
  Occurrences: 4
    Line 3: comment
      Code: Fix remaining HIGH severity eval() issues.
    Line 5: comment
      Code: This script intelligently handles eval() usage by:
    Line 95: documented
      Code: if idx > 0 and '# SECURITY: eval()' in lines[idx-1]:
    Line 99: documented
      Code: warning = "# SECURITY: eval() used with trusted input only. Do not use with untrusted user input.\n"

File: /home/runner/work/machine-native-ops/machine-native-ops/fix_remaining_issues.py
  Type: tool
  Occurrences: 10
    Line 4: comment
      Code: # It uses eval() and other security-sensitive functions for analysis purposes only.
    Line 183: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 184: string_check
      Code: if "eval(" not in content:
    Line 187: documented
      Code: # Note: eval() replacement is complex and context-dependent
    Line 190: comment
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 192: comment
      Code: if "eval(" in content:
    Line 194: safe_alternative
      Code: warning = "# TODO: Security - Consider replacing eval() with safer alternatives like ast.literal_eva
    Line 197: documented
      Code: # Find eval() lines and add warning
    Line 198: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 201: comment
      Code: if "eval(" in line and "# TODO: Security" not in line:

File: /home/runner/work/machine-native-ops/machine-native-ops/scripts/auto-quality-check.py
  Type: tool
  Occurrences: 1
    Line 208: string_check
      Code: if "eval(" in content:

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/agents/task_executor.py
  Type: core
  Occurrences: 10
    Line 135: string_check
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 136: comment
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 137: comment
      Code: if "eval(" in code or "exec(" in code:
    Line 235: comment
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 236: string_check
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 238: comment
      Code: if "eval(" in code or "exec(" in code:
    Line 240: string_check
      Code: fixed_code = code.replace("eval(", "# REMOVED_eval(")
    Line 295: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 296: comment
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 299: comment
      Code: result = eval(user_input)  # Security issue!

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/examples/demo.py
  Type: demo
  Occurrences: 2
    Line 42: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 43: documented
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/pipeline_service.py
  Type: core
  Occurrences: 2
    Line 361: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 362: documented
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/test-vectors/generator.py
  Type: demo
  Occurrences: 2
    Line 221: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 222: documented
      Code: "    result = eval(user_input)",

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/tests/test_phase5_components.py
  Type: test
  Occurrences: 3
    Line 376: string_check
      Code: if "eval(" in code:
    Line 381: documented
      Code: description="Dangerous eval() usage",
    Line 382: documented
      Code: location="Code contains eval()",

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/autonomous/agents/tests/test_task_executor.py
  Type: test
  Occurrences: 1
    Line 50: comment
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/core/plugins/virtual_experts/domain_experts.py
  Type: core
  Occurrences: 2
    Line 500: string_check
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 501: string_check
      Code: if "eval(" in code_lower or "exec(" in code_lower:

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/core/run-debug/cli.py
  Type: core
  Occurrences: 2
    Line 387: documented
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 388: documented
      Code: def eval(expression):

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/src/core/virtual_experts/domain_experts.py
  Type: core
  Occurrences: 2
    Line 505: string_check
      Code: # SECURITY: eval() used with trusted input only. Do not use with untrusted user input.
    Line 506: string_check
      Code: if "eval(" in code_lower or "exec(" in code_lower:

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/agents/task_executor.py
  Type: core
  Occurrences: 4
    Line 135: string_check
      Code: if "eval(" in code or "exec(" in code:
    Line 234: string_check
      Code: if "eval(" in code or "exec(" in code:
    Line 236: string_check
      Code: fixed_code = code.replace("eval(", "# REMOVED_eval(")
    Line 293: comment
      Code: result = eval(user_input)  # Security issue!

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/tests/test_phase5_components.py
  Type: test
  Occurrences: 3
    Line 376: string_check
      Code: if "eval(" in code:
    Line 381: documented
      Code: description="Dangerous eval() usage",
    Line 382: documented
      Code: location="Code contains eval()",

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/teams/holy-grail/agents/autonomous/tests/test_task_executor.py
  Type: test
  Occurrences: 1
    Line 50: comment
      Code: result = eval(user_input)

File: /home/runner/work/machine-native-ops/machine-native-ops/workspace/tools/security_audit.py
  Type: tool
  Occurrences: 2
    Line 190: safe_alternative
      Code: issue="eval() function usage detected",
    Line 192: safe_alternative
      Code: recommendation="Avoid eval() as it can execute arbitrary code. "