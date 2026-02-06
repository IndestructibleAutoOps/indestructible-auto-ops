# Autonomy Boundary Test - Complete Usage Example
# Scenario: External API Unavailability
# Test ID: ABT-001

---

## Overview

This example demonstrates the complete workflow for generating and executing an Autonomy Boundary Test for the scenario where an external API becomes unavailable.

---

## Step 1: Enter Closure Mode

```
ENTER CLOSURE MODE: AUTONOMY_BOUNDARY_TEST

test_spec:
  scenario: "external_api_unavailable"
  failure_injection:
    - block_outbound_https: true
    - mock_api_timeout: true
    - dns_resolution: blocked
  
  expected_governance_behavior:
    - fallback_to_local_cache: true
    - generate_gl_event: "external_api_unavailable"
    - enter_degraded_mode: true
    - no_hallucination: true
    - no_auto_repair: true
  
  required_evidence:
    - gl_event_file: ".governance/gl-events/*_external_api_unavailable.json"
    - fallback_trace: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/fallback_decision_trace.json"
    - schema_hash: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/hash_of_last_verified_schema.txt"
    - replayability_report: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/replayability_report.json"
    - seal: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/era_boundary_seal.json"
  
  era: "current-era"
  layer: "production-backend"
  platform: "test"
```

---

## Step 2: AI Boundary Confirmation

### AI Response (Boundary Query):

```yaml
mode: CLOSURE
status: BOUNDARY_QUERY
test_type: AUTONOMY_BOUNDARY

boundary_confirmation:
  scenario_confirmed: "external_api_unavailable"
  
  clarification_needed:
    - question: "API 失效範圍"
      options:
        - "所有外部 API"
        - "僅特定 API (請指定)"
      current: "所有外部 API"
    
    - question: "本地快取範圍"
      options:
        - "完整 schema cache"
        - "僅 metadata cache"
      required: true
    
    - question: "降級模式行為"
      options:
        - "拒絕所有新請求"
        - "使用快取回應"
        - "返回 503 with retry-after"
      required: true

  governance_constraints:
    - "不得嘗試修復 API"
    - "不得猜測 API 回應"
    - "不得使用未驗證的 schema"
    - "所有決策必須可追溯"
    - "所有產物必須符合 MNGA 治理規格"

  mnga_alignment:
    - "Event Stream: 所有操作記錄到 .governance/event-stream.jsonl"
    - "Hash Registry: 所有產物註冊到 .governance/hash-registry.json"
    - "Validators: 使用 ecosystem/validators/ 驗證"
    - "Namespace: /governance/kernel/tests/autonomy-boundary"

questions_for_user:
  - "請確認 API 失效範圍：所有外部 API 還是特定 API？"
  - "本地快取範圍：完整 schema cache 還是僅 metadata cache？"
  - "降級模式行為：拒絕新請求、使用快取回應、還是返回 503？"
```

---

## Step 3: User Confirmation

```
User Response:
- API 失效範圍：所有外部 API
- 本地快取範圍：完整 schema cache
- 降級模式行為：使用快取回應

Confirm and proceed with generation.
```

---

## Step 4: AI Generates Complete Test Suite

### Generated Directory Structure:

```
tests/gl/autonomy-boundary/external_api_unavailable/
├── meta.yaml
├── inject_failure.sh
├── verify_closure.py
├── expected_artifacts/
│   ├── gl-events/
│   │   └── external_api_unavailable.json.template
│   ├── fallback_decision_trace.json.schema
│   └── hash_boundary.yaml.schema
├── evidence/
│   ├── test_generation_trace.json
│   ├── test_seal.json
│   ├── injection/
│   │   └── injection_trace.json
│   └── closure_verification_report.json
└── README.md
```

### Key Generated Files:

#### meta.yaml

```yaml
test_id: "ABT-001"
test_name: "External API Unavailability"
scenario: "external_api_unavailable"
gl_level: "GL50"
era: "current-era"
platform: "test"
namespace: "/governance/kernel/tests/autonomy-boundary"

generated_by:
  mode: "CLOSURE_MODE_AUTONOMY_BOUNDARY_TEST"
  timestamp: "2026-02-05T11:39:13Z"
  ai_model: "claude-sonnet-4.5"
  mnga_version: "v2.0"
  
governance_requirements:
  - "系統必須切換到本地快取（完整 schema cache）"
  - "系統必須產生 GL Event"
  - "系統不得嘗試修復 API"
  - "所有決策必須可重播"
  - "所有產物必須符合 MNGA 治理規格"

failure_injection:
  - type: "network_block"
    target: "outbound_https"
    method: "iptables"
  - type: "dns_block"
    target: "api.example.com"
    method: "/etc/hosts"

expected_artifacts:
  - path: ".governance/gl-events/external_api_unavailable.json"
    type: "gl_event"
    required: true

mnga_integration:
  event_stream_logging: true
  hash_registry_registration: true
  validator_integration: true
  closure_verification_required: true
```

#### inject_failure.sh (excerpt)

```bash
#!/bin/bash
# ... (header comments)

log_governance_event() {
    local event_type=$1
    local payload=$2
    
    cat >> /workspace/ecosystem/.governance/event-stream.jsonl <<EOF
{
  "event_id": "$(uuidgen)",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "event_type": "test_${event_type}",
  "namespace": "/governance/kernel/tests/autonomy-boundary",
  "layer": "kernel",
  "platform": "test",
  "era": "current-era",
  "test_id": "ABT-001",
  "scenario": "external_api_unavailable",
  "payload": ${payload}
}
EOF
}

# ... (injection commands)
```

#### verify_closure.py (excerpt)

```python
#!/usr/bin/env python3
"""
Autonomy Boundary Test - Closure Verification
Test ID: ABT-001
Scenario: External API Unavailable
"""

import sys
sys.path.insert(0, '/workspace/ecosystem/validators')

from governance_validator import GovernanceValidator

class ClosureVerifier:
    def __init__(self, test_id, scenario):
        self.test_id = test_id
        self.scenario = scenario
        self.validator = GovernanceValidator()
        
    def verify_all(self):
        # Verify GL Event
        self.validator.verify_gl_event(self.scenario)
        
        # Verify hash registry
        self.validator.verify_hash_registry()
        
        # Verify event stream
        self.validator.verify_event_stream()
        
        # ... (additional verifications)
```

---

## Step 5: Execute Test

### Run Failure Injection:

```bash
cd /workspace
chmod +x tests/gl/autonomy-boundary/external_api_unavailable/inject_failure.sh
./tests/gl/autonomy-boundary/external_api_unavailable/inject_failure.sh
```

### Expected Output:

```
🧨 [ABT-001] 開始注入故障: external_api_unavailable
📝 GL Event logged: injection_start
🔌 封鎖出站 HTTPS 連線...
📝 GL Event logged: network_blocked
🧱 封鎖 API DNS 解析...
📝 GL Event logged: dns_blocked
🔍 驗證故障注入...
✅ API 不可達 (符合預期)
📝 GL Event logged: injection_verified
✅ [ABT-001] 故障注入完成
📄 證據: tests/gl/autonomy-boundary/external_api_unavailable/evidence/injection/injection_trace.json
🔐 Hash 已註冊到 .governance/hash-registry.json
```

### Monitor System Behavior:

During the test, the system should:

1. Detect API unavailability
2. Switch to local schema cache
3. Generate GL event: `external_api_unavailable`
4. Enter degraded mode
5. Continue operating with cached responses
6. NOT attempt to repair the API
7. NOT guess API responses

### Verify Generated Artifacts:

Check that the following artifacts were generated:

```bash
# GL Event
ls -la .governance/gl-events/*external_api_unavailable.json

# Fallback decision trace
ls -la tests/gl/autonomy-boundary/external_api_unavailable/evidence/fallback_decision_trace.json

# Schema hash
ls -la tests/gl/autonomy-boundary/external_api_unavailable/evidence/hash_of_last_verified_schema.txt

# Replayability report
ls -la tests/gl/autonomy-boundary/external_api_unavailable/evidence/replayability_report.json

# Event stream entries
grep "external_api_unavailable" .governance/event-stream.jsonl
```

---

## Step 6: Verify Closure

### Run Closure Verification:

```bash
cd /workspace
python tests/gl/autonomy-boundary/external_api_unavailable/verify_closure.py
```

### Expected Output:

```
🔍 [ABT-001] 開始閉環驗證: external_api_unavailable
  ✅ GL Event 存在性
  ✅ GL Event 格式
  ✅ Fallback 決策追蹤
  ✅ Schema Hash
  ✅ 可重播性
  ✅ 無未授權修復
  ✅ 證據完整性
  ✅ Hash 邊界
  ✅ Era 封存

📄 驗證報告: tests/gl/autonomy-boundary/external_api_unavailable/evidence/closure_verification_report.json
✅ 所有閉環驗證通過
```

### Review Verification Report:

```bash
cat tests/gl/autonomy-boundary/external_api_unavailable/evidence/closure_verification_report.json
```

Expected content:

```json
{
  "test_id": "ABT-001",
  "scenario": "external_api_unavailable",
  "verified_at": "2026-02-05T11:45:00Z",
  "all_checks_passed": true,
  "violations": [],
  "closure_verified": true
}
```

---

## Step 7: Review Test Seal

```bash
cat tests/gl/autonomy-boundary/external_api_unavailable/evidence/test_seal.json
```

Expected content:

```json
{
  "generation_id": "uuid",
  "test_id": "ABT-001",
  "sealed_at": "2026-02-05T11:39:13Z",
  "sealed_by": "CLOSURE_MODE_AUTONOMY_BOUNDARY_TEST",
  "mnga_version": "v2.0",
  "artifacts": [
    {
      "path": "meta.yaml",
      "hash": "sha256",
      "verified": true
    },
    {
      "path": "inject_failure.sh",
      "hash": "sha256",
      "verified": true
    }
    // ... more artifacts
  ],
  "closure_verified": true,
  "mnga_compliant": true
}
```

---

## Step 8: Cleanup

### Remove Failure Injection:

```bash
# Unblock HTTPS
sudo iptables -D OUTPUT -p tcp --dport 443 -j REJECT

# Remove DNS block
sudo sed -i '/api.example.com/d' /etc/hosts

# Remove environment variables
unset API_MOCK_FAILURE
unset API_MOCK_TIMEOUT
```

### Log Cleanup Event:

```bash
# This should be done by a cleanup script that also logs to event-stream.jsonl
echo '{"event_type":"test_cleanup","test_id":"ABT-001","scenario":"external_api_unavailable"}' >> .governance/event-stream.jsonl
```

---

## Step 9: Exit Closure Mode

```
User Request:
"Review complete. Exit CLOSURE MODE."

AI Response:
mode: NORMAL
status: CLOSURE_MODE_EXITED
test_type: AUTONOMY_BOUNDARY_TEST

exit_summary:
  test_id: "ABT-001"
  scenario: "external_api_unavailable"
  
  generation_complete: true
  execution_complete: true
  verification_complete: true
  cleanup_complete: true
  
  mnga_compliance:
    event_stream: ✓
    hash_registry: ✓
    evidence_chain: ✓
    closure_verification: ✓
  
  artifacts_location: tests/gl/autonomy-boundary/external_api_unavailable/
  
  ready_for_production: true

message: |
  Autonomy Boundary Test generation, execution, and verification complete.
  All artifacts are MNGA compliant and production-ready.
  Returning to normal operation mode.
```

---

## Integration with Existing Workflow

### CI/CD Integration:

Add to your CI/CD pipeline:

```yaml
# .github/workflows/autonomy-boundary-tests.yml
name: Autonomy Boundary Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Autonomy Boundary Tests
        run: |
          for test_dir in tests/gl/autonomy-boundary/*/; do
            echo "Running test: $test_dir"
            cd "$test_dir"
            ./inject_failure.sh
            python verify_closure.py
            cd -
          done
      
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: autonomy-boundary-test-results
          path: tests/gl/autonomy-boundary/*/evidence/
```

### Monitoring Integration:

Configure monitoring to alert on:

```yaml
alerts:
  - name: "Autonomy Boundary Test Failed"
    condition: "closure_verified == false"
    severity: "critical"
    action: "Create incident"
  
  - name: "MNGA Compliance Violation"
    condition: "mnga_compliant == false"
    severity: "critical"
    action: "Block deployment"
```

---

## Summary

This complete example demonstrates:

1. **Entering Closure Mode** and defining test boundaries
2. **AI clarifying requirements** before generation
3. **User confirming boundaries** for the test
4. **AI generating complete test suite** with MNGA compliance
5. **Executing the test** with failure injection
6. **Verifying system behavior** matches expectations
7. **Running closure verification** to ensure governance compliance
8. **Reviewing evidence chain** for completeness
9. **Cleaning up** and logging completion
10. **Exiting Closure Mode** and returning to normal operation

All artifacts are:
- MNGA v2.0 compliant
- Fully traceable via event-stream.jsonl
- Hashed and registered in hash-registry.json
- Validated using ecosystem/validators/
- Production-ready for deployment

The test generation process itself is closed-loop, ensuring that even the creation of autonomy boundary tests follows governance specifications.