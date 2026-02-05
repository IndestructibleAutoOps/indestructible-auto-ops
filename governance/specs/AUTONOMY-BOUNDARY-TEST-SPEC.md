# Autonomy Boundary Test Generation Specification
# Version: 1.0.0
# GL Level: GL50 (Indestructible Kernel)
# Namespace: /governance/kernel/specs/autonomy-boundary-test
# Alignment: MNGA v2.0 - Era-1 Evidence-Native Bootstrap

## Definition

**自治性邊界測試 (Autonomy Boundary Test)** 不是功能測試，而是治理驗證：

```
功能測試問：這個功能正常嗎？
治理測試問：失效時系統是否仍可治理？
```

## Governance Alignment

### MNGA Compliance
- **Layer:** Governance Layer → Validation Layer
- **Engine:** Autonomy Boundary Validation Engine
- **Event Stream:** All test operations logged to `.governance/event-stream.jsonl`
- **Evidence Chain:** Complete traceability from test generation to verification
- **Closure Mode:** Test generation itself must be closed-loop

### Namespace Structure
```
/governance/kernel/specs/autonomy-boundary-test/
├── test-generation-protocol.md
├── evidence-requirements.md
├── closure-verification.md
└── era-boundary-sealing.md
```

## Test Generation Closure Mode

### Trigger Format

```yaml
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
    - gl_event_file: ".governance/gl-events/{timestamp}_external_api_unavailable.json"
    - fallback_trace: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/fallback_decision_trace.json"
    - schema_hash: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/hash_of_last_verified_schema.txt"
    - replayability_report: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/replayability_report.json"
    - seal: "tests/gl/autonomy-boundary/external_api_unavailable/evidence/era_boundary_seal.json"
  
  era: "current-era"
  layer: "production-backend"
  platform: "test"
  gl_level: "GL50"
```

### AI Response Format (Boundary Confirmation Phase)

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
    - "Evidence Chain: 完整證據鏈從生成到驗證"
    - "Hash Registry: 所有產物註冊到 .governance/hash-registry.json"
    - "Closure Verification: 驗證器使用 ecosystem/validators/"

warning: |
  此為自治性邊界測試生成模式。
  所有產出都必須符合治理閉環要求。
  請確認所有邊界問題後，我將進入 LOCKED 狀態。
```

## Test Directory Structure

### Standard Structure

```
tests/gl/autonomy-boundary/
├── {scenario_name}/
│   ├── meta.yaml                          # 測試元數據
│   ├── inject_failure.sh                  # 故障注入腳本
│   ├── verify_closure.py                  # 閉環驗證腳本
│   ├── expected_artifacts/                # 期望產物
│   │   ├── gl-events/
│   │   │   └── external_api_unavailable.json.template
│   │   ├── fallback_decision_trace.json.schema
│   │   └── hash_boundary.yaml.schema
│   ├── evidence/                          # 測試本身的證據
│   │   ├── test_generation_trace.json
│   │   ├── test_seal.json
│   │   ├── injection/
│   │   │   └── injection_trace.json
│   │   └── closure_verification_report.json
│   └── README.md                          # 測試說明
```

## Meta.yaml Format

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
  - "系統必須切換到本地快取"
  - "系統必須產生 GL Event"
  - "系統不得嘗試修復 API"
  - "所有決策必須可重播"
  - "所有產物必須符合 MNGA 治理規格"
  - "證據鏈必須完整可追溯"

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
    schema: "expected_artifacts/gl-events/external_api_unavailable.json.template"
  
  - path: "evidence/fallback_decision_trace.json"
    type: "decision_trace"
    required: true
    schema: "expected_artifacts/fallback_decision_trace.json.schema"

verification_steps:
  - "驗證 GL Event 存在且格式正確"
  - "驗證 fallback 決策可追溯"
  - "驗證系統未嘗試自動修復"
  - "驗證所有決策可重播"
  - "驗證證據已封存"
  - "驗證符合 MNGA 治理規格"

seal_requirements:
  - "所有產物必須有 SHA256 hash"
  - "必須產生 era_boundary_seal.json"
  - "必須記錄到 event-stream.jsonl"
  - "必須註冊到 hash-registry.json"

mnga_integration:
  event_stream_logging: true
  hash_registry_registration: true
  validator_integration: true
  closure_verification_required: true
```

## Evidence Requirements

### Complete Evidence Chain

1. **Test Generation Evidence** (`test_generation_trace.json`)
   - AI prompt and responses
   - Decision-making process
   - Boundary clarifications
   - Generated artifact hashes

2. **Injection Evidence** (`injection/injection_trace.json`)
   - Failure injection commands
   - Verification of injection success
   - System state before/after injection

3. **Runtime Evidence** (`runtime_trace.json`)
   - System behavior during failure
   - GL events generated
   - Decision trace
   - Fallback actions

4. **Verification Evidence** (`closure_verification_report.json`)
   - All verification checks
   - Pass/fail status
   - Violations found
   - Final closure status

5. **Seal Evidence** (`era_boundary_seal.json`)
   - Complete evidence hash
   - Artifacts list with hashes
   - Era boundary confirmation
   - MNGA compliance verification