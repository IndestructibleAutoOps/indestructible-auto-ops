# Governance Engine Migration Guide
# v1 → v2: From Governance Illusion to Real Governance

---

## Executive Summary

This guide documents the critical migration from **Governance Engine v1** (which exhibited "Governance Illusion" - claiming all checks passed without actual verification) to **Governance Engine v2** (which performs real checks with full evidence chain).

### Key Improvement

**Before (v1):**
```bash
$ python ecosystem/enforce.py
real    0m1.373s
✅ 所有檢查通過 (18/18)
# Evidence: 0 files generated
```

**After (v2):**
```bash
$ python ecosystem/enforce.rules.v2.py
real    0m0.088s
❌ 治理檢查失敗: 4 個檢查未通過
# Evidence: .governance/reports/GLCM-REPORT-*.json
# Evidence: .governance/event-stream.jsonl
```

---

## Why Migrate?

### The Problem: Governance Illusion

v1 exhibited a **meta-level governance failure**:
- ✅ Displayed "all checks passed"
- ✅ Executed in 1.373 seconds (too fast for real checks)
- ❌ Generated NO evidence
- ❌ Generated NO trace
- ❌ Generated NO hash
- ❌ NO replayability

### The Solution: Real Governance v2

v2 implements:
- ✅ **Actual file scanning** and content validation
- ✅ **Complete evidence chain** generation
- ✅ **Replayable verification** with trace hash
- ✅ **Event stream integration**
- ✅ **Self-governance mechanism**

---

## Migration Steps

### Step 1: Seal the Governance Illusion (Archival)

The governance illusion has been sealed as a negative example:

```bash
# Evidence of the problem
evidence/violations/governance-illusion-2025-02-05.json
```

This includes:
- Violation documentation
- Evidence of fake execution
- Corrective actions taken
- Lessons learned

### Step 2: Deploy v2 Engine

```bash
# The new real governance engine
ecosystem/enforce.rules.v2.py

# Key features:
# - RealGovernanceEngine class
# - 7 actual checks (GLCM-NAR, GLCM-FCT, GLCM-UNC, GLCM-EVC, DIR, HASH, EVENT)
# - Full evidence sealing
# - Event stream integration
```

### Step 3: Update CI/CD Pipeline

```yaml
# .github/workflows/governance-check.yml

- name: Run Governance Check
  run: |
    python ecosystem/enforce.rules.v2.py
  env:
    GOVERNANCE_ENGINE_VERSION: "v2.0.0"
```

### Step 4: Initialize Evidence Chain

```bash
# Create necessary directories
mkdir -p .governance/evidence/violations
mkdir -p .governance/evidence/requirements
mkdir -p .governance/evidence/implementation
mkdir -p .governance/reports
mkdir -p .governance/self-checks
```

### Step 5: Run Self-Governance Check

```bash
# Check the governance engine itself
python governance/kernel/self_governance.py
```

---

## Verification

### Test the New Engine

```bash
# Run v2 engine
python ecosystem/enforce.rules.v2.py

# Expected output:
# - 8 checks executed
# - Real violations found (GLCM-NAR, GLCM-FCT, etc.)
# - Report generated: .governance/reports/GLCM-REPORT-*.json
# - Event stream updated: .governance/event-stream.jsonl
```

### Verify Evidence Generation

```bash
# Check report file
ls -la .governance/reports/GLCM-REPORT-*.json

# Check event stream
tail -5 .governance/event-stream.jsonl

# Verify trace hash
jq '.trace_hash' .governance/reports/GLCM-REPORT-*.json
```

---

## Comparison: v1 vs v2

### Architecture

```yaml
v1_architecture:
  execution: fake
  evidence: none
  traceability: none
  replayability: none
  execution_time: 1.373s
  status: GOVERNANCE_ILLUSION

v2_architecture:
  execution: real
  evidence: complete
  traceability: full
  replayability: yes
  execution_time: ~100ms
  status: REAL_GOVERNANCE
```

### Checks Performed

| Check ID | v1 Status | v2 Status | Description |
|----------|-----------|-----------|-------------|
| GLCM-NAR | ❌ Not checked | ✅ Implemented | No narrative language |
| GLCM-FCT | ❌ Not checked | ✅ Implemented | No false timeline |
| GLCM-UNC | ❌ Not checked | ✅ Implemented | No unsealed conclusions |
| GLCM-EVC | ❌ Not checked | ✅ Implemented | Evidence chain |
| DIR | ❌ Not checked | ✅ Implemented | Directory structure |
| HASH | ❌ Not checked | ✅ Implemented | Hash integrity |
| EVENT | ❌ Not checked | ✅ Implemented | Event stream |

### Evidence Generated

```yaml
v1_evidence:
  reports: 0
  traces: 0
  hashes: 0
  total_files: 0

v2_evidence:
  reports: 1 (GLCM-REPORT-*.json)
  traces: 1 (trace hash)
  hashes: 1 (trace hash + file hashes)
  total_files: 2
```

---

## Rollback Plan

If issues occur with v2:

```bash
# Rollback to v1 (not recommended)
cp ecosystem/enforce.rules.py ecosystem/enforce.rules.v1.backup
cp ecosystem/enforce.py ecosystem/enforce.v1.backup

# Restore
python ecosystem/enforce.py
```

**Note:** Rolling back to v1 is **STRONGLY DISCOURAGED** as it reintroduces the governance illusion.

---

## Best Practices

### 1. Always Run v2

```bash
# Never use v1 again
# python ecosystem/enforce.py  # ❌ DO NOT USE

# Always use v2
python ecosystem/enforce.rules.v2.py  # ✅ CORRECT
```

### 2. Verify Evidence

```bash
# After each run, verify evidence was generated
if [ ! -f .governance/reports/GLCM-REPORT-*.json ]; then
  echo "❌ Governance check failed to generate evidence"
  exit 1
fi
```

### 3. Monitor Event Stream

```bash
# Check event stream is growing
tail -10 .governance/event-stream.jsonl
```

### 4. Self-Governance

```bash
# Regularly check the governance engine itself
python governance/kernel/self_governance.py
```

---

## Troubleshooting

### Issue: Import Error

```bash
ModuleNotFoundError: No module named 'yaml'

# Solution:
pip install pyyaml
```

### Issue: Permission Denied

```bash
PermissionError: [Errno 13] Permission denied: '.governance/reports'

# Solution:
chmod -R 755 .governance
```

### Issue: Event Stream Corrupted

```bash
json.JSONDecodeError: Expecting value

# Solution:
# Backup and recreate
cp .governance/event-stream.jsonl .governance/event-stream.jsonl.backup
echo "" > .governance/event-stream.jsonl
```

---

## Future Enhancements

### Era-2 Planned Features

1. **Blockchain-anchored audit trails**
   - Anchor evidence hashes to blockchain
   - Immutable verification

2. **Zero-knowledge proofs**
   - Verify compliance without revealing sensitive data

3. **Automated remediation**
   - Auto-fix simple governance violations
   - Request human review for complex issues

4. **Multi-language support**
   - Expand beyond zh/en
   - Support ja, ko, de, fr

---

## References

1. [Governance Illusion Evidence](../../evidence/violations/governance-illusion-2025-02-05.json)
2. [Real Governance Engine v2](../../ecosystem/enforce.rules.v2.py)
3. [Self-Governance Mechanism](../../governance/kernel/self_governance.py)
4. [Global Best Practices - Audit Trails](https://www.linkedin.com/pulse/autonomous-system-audit-trails-immutable-tracking)
5. [Zero-Trust Architecture](https://www.cisa.gov/sites/default/files/2023-04/CISA_Zero_Trust_Maturity_Model_Version_2_508c.pdf)

---

## Appendix: Test Cases

### Test Case 1: Verify Real Execution

```bash
# Should NOT execute in < 1 second
time python ecosystem/enforce.rules.v2.py

# Expected: > 0.05 seconds (real execution)
```

### Test Case 2: Verify Evidence Generation

```bash
# Run engine
python ecosystem/enforce.rules.v2.py

# Verify evidence exists
ls -la .governance/reports/GLCM-REPORT-*.json

# Verify event stream exists
ls -la .governance/event-stream.jsonl
```

### Test Case 3: Verify Trace Hash

```bash
# Extract trace hash
jq '.trace_hash' .governance/reports/GLCM-REPORT-*.json

# Should be 64-character SHA256 hash
# Example: c3315266e3222d02c8af4d6c04a279f252702661c45dc862fb0cd6c67448d6b8
```

### Test Case 4: Verify Replayability

```bash
# Run twice, should produce same trace hash for same state
python ecosystem/enforce.rules.v2.py
HASH1=$(jq '.trace_hash' .governance/reports/GLCM-REPORT-*.json)

python ecosystem/enforce.rules.v2.py
HASH2=$(jq '.trace_hash' .governance/reports/GLCM-REPORT-*.json)

# Should be equal
[ "$HASH1" = "$HASH2" ] && echo "✅ Replayable" || echo "❌ Not replayable"
```

---

**Document Version:** 1.0.0
**Created:** 2025-02-05
**Status:** CANONICAL
**GL Level:** GL50
**Era:** Era-1 (Evidence-Native Bootstrap)