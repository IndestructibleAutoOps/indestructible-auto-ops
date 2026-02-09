# GL-NarrativeFree Compliance Specification v2.0

## Executive Summary

This specification defines a narrative-free compliance system for IndestructibleAutoOps, ensuring zero narrative language, sealed conclusions, and evidence-backed claims. Version 2.0 includes critical **Fabricated Completion Timeline (GLCM-FCT)** detection to prevent semantic-level deception through fabricated timelines.

---

## Core Principles

> ✅ **Zero Narrative**: No non-deterministic, subjective, or speculative language
> ✅ **All Conclusions Sealed**: Every conclusion statement MUST have trace/hash/evidence
> ✅ **No Fabricated Timelines**: Every "completed/fixed" statement MUST have hash/trace/complement evidence
> ✅ **All Outputs Sealable**: All reports, logs, outputs MUST be canonicalizable with hash

---

## Problem Definition: Fabricated Timeline (GLCM-FCT)

### What is a Fabricated Timeline?

> System uses past tense or completion aspect to imply an event has occurred, completed, been fixed, or deployed, but lacks corresponding sealed evidence (hash, trace, complement, .evidence).

### Examples

| Language | Pattern | Example |
|----------|---------|---------|
| 中文 | 過去式 + 結論語氣 | 「我們已完成」「已修復」「已部署」「已恢復」「已解決」 |
| 英文 | Past perfect / passive voice | "has been resolved", "was fixed", "we have completed", "the issue was addressed" |
| 日文 | 完了形 + 結論語氣 | 「修正しました」「完了しました」「復旧しました」 |
| 韓文 | 완료형 + 결론어조 | "수정했습니다", "완료했습니다", "복구했습니다" |
| 德文 | Perfekt + Schlussfolgerung | "haben wir abgeschlossen", "wurde behoben", "wurde bereitgestellt" |
| 法文 | Passé composé + ton conclusif | "a été résolu", "a corrigé", "a déployé" |

---

## Architecture Design

```
[輸出檔案] → [語言分類器] → [規則匹配器] → [模組切換器] → [掃描器執行] → [封存模組狀態]
     │              │              │              │              │              │
     │              │              │              │              │              ├──→ narrative_free_report.json
     │              │              │              │              │              ├──→ glcm_config_used.yaml
     │              │              │              │              │              ├──→ hash_narrative_report.txt
     │              │              │              │              │              └──→ gl-events/narrative_scan_completed.json
```

---

## Governance Language Compliance Modules (GLCM)

### Modular Architecture

| 模組代號 | 功能 | 可條件啟用 | 預設狀態 |
|----------|------|------------|----------|
| **GLCM-NAR** | 禁用敘事語言 | ✅ 可依語境開關 | 開啟 |
| **GLCM-UNC** | 禁用未封存結論語句 | ✅ 可依輸出類型開關 | 開啟 |
| **GLCM-EVC** | 強制證據鏈引用 | ✅ 可依語句類型開關 | 開啟 |
| **GLCM-FCT** | 偵測虛假時間線 | ✅ 可依場景開關 | 開啟 |
| **GLCM-EMO** | 禁用情緒性語言 | ✅ 可依角色開關 | 關閉 |
| **GLCM-SOFT** | 軟性敘述允許（需附 hash） | ✅ 可依場景開啟 | 關閉 |
| **GLCM-EXC** | 允許例外白名單 | ✅ 可指定路徑或 pattern | 關閉 |

---

## Detection Rules

### GLCM-NAR: Narrative Phrases Detection

**Banlist** (rules/narrative_banlist.yaml):
```yaml
narrative_phrases:
  - 我們相信
  - 應該
  - 可能
  - 預期
  - 希望
  - 也許
  - 有望
  - 我們認為
  - 我們預估
  - 我們樂觀地
  - 令人擔憂
  - 值得期待
  - 預料之中
  - 看起來
  - 似乎
  - 大概
  - 或許
  - 估計
```

### GLCM-UNC: Unsealed Conclusions Detection

**Banlist**:
```yaml
unsealed_conclusions:
  - 因此我們決定
  - 我們已完成
  - 我們已修復
  - 我們採取了行動
  - 我們已部署
  - 問題已解決
  - 系統已恢復
  - 我們已執行
  - 我們已實施
```

**Evidence Hints** (Required within 300 characters):
```yaml
evidence_hints:
  - hash
  - trace
  - .evidence
  - 補件
  - 封存
  - gl-events
  - replay
  - canonical
  - era-1-closure
  - hash_translation_table
```

### GLCM-FCT: Fabricated Completion Timeline Detection

**Critical Issue**: This is the MOST CRITICAL vulnerability - a fundamental blocking issue.

**Detection Patterns** (Multi-language):

**中文**:
```yaml
fabricated_timeline_zh:
  - "已完成"
  - "已修復"
  - "已部署"
  - "已恢復"
  - "已解決"
  - "已執行"
  - "已實施"
  - "已修正"
  - "已完成修復"
  - "問題已解決"
  - "系統已恢復"
```

**English**:
```yaml
fabricated_timeline_en:
  - "has been completed"
  - "has been resolved"
  - "was fixed"
  - "has been deployed"
  - "we have completed"
  - "the issue was addressed"
  - "was successfully repaired"
  - "has been restored"
```

**日文**:
```yaml
fabricated_timeline_ja:
  - "修正しました"
  - "完了しました"
  - "復旧しました"
  - "解決しました"
  - "実行しました"
  - "展開しました"
```

**韓文**:
```yaml
fabricated_timeline_ko:
  - "수정했습니다"
  - "완료했습니다"
  - "복구했습니다"
  - "해결했습니다"
  - "실행했습니다"
  - "배포했습니다"
```

**德文**:
```yaml
fabricated_timeline_de:
  - "haben wir abgeschlossen"
  - "wurde behoben"
  - "wurde bereitgestellt"
  - "wurde wiederhergestellt"
  - "wurde gelöst"
```

**法文**:
```yaml
fabricated_timeline_fr:
  - "a été résolu"
  - "a été corrigé"
  - "a été déployé"
  - "a été restauré"
  - "a été achevé"
```

---

## Verification Conditions

### For Fabricated Timeline Statements

Each statement matching GLCM-FCT patterns MUST have evidence within **300 characters**:

**Required Evidence Keywords**:
- `hash:`
- `trace:`
- `.evidence/`
- `gl-events/`
- `replay_verification_report.json`
- `era-1-closure.json`
- `hash_translation_table.jsonl`

**OR** explicit artifact reference:
- `hash_of_patch_plan.txt`
- `trace_id: abc123`
- `evidence_file: ...`

### For Narrative Phrases

ANY occurrence of GLCM-NAR phrases is **IMMEDIATE VIOLATION** (no evidence check needed).

### For Unsealed Conclusions

Statement matching GLCM-UNC patterns MUST have evidence hints within **300 characters**.

---

## Report Format

### narrative_free_compliance_report.json

```json
{
  "scan_timestamp": "2024-02-05T03:35:54Z",
  "glcm_config": {
    "enabled": true,
    "modules": {
      "GLCM-NAR": true,
      "GLCM-UNC": true,
      "GLCM-EVC": true,
      "GLCM-FCT": true,
      "GLCM-EMO": false,
      "GLCM-SOFT": false,
      "GLCM-EXC": {"enabled": false}
    }
  },
  "files": {
    "outputs/self_healing_summary.txt": [
      {
        "type": "narrative",
        "text": "我們樂觀地預期",
        "pos": 88,
        "rule": "GLCM-NAR",
        "severity": "MEDIUM"
      },
      {
        "type": "unsealed_claim",
        "text": "我們已修復此問題",
        "pos": 212,
        "rule": "GLCM-UNC",
        "evidence_found": false,
        "severity": "HIGH"
      },
      {
        "type": "fabricated_timeline",
        "text": "問題已解決",
        "pos": 328,
        "rule": "GLCM-FCT",
        "evidence_found": false,
        "severity": "CRITICAL"
      }
    ]
  },
  "summary": {
    "total_violations": 3,
    "narrative_violations": 1,
    "unsealed_conclusions": 1,
    "fabricated_timelines": 1,
    "files_scanned": 57,
    "files_with_violations": 1
  }
}
```

---

## Acceptance Criteria (GL-NarrativeFree v2 Compliance)

### Phase 1: Narrative-Free

| 條件 | 驗證方式 |
|------|----------|
| 無 narrative 語言 | type: narrative 條目為空 |
| 無未封存結論語句 | type: unsealed_claim 條目為空 或 evidence_found: true |
| 無虛假時間線語句 | type: fabricated_timeline 條目為空 |
| 所有結論皆有證據鏈 | 每句結論語句 300 字內含 hash/trace/.evidence |

### Phase 2: Evidence Integrity

| 條件 | 驗證方式 |
|------|----------|
| 所有報告可 canonicalize | 可成功執行 canonicalizer.py 並產生 hash |
| 報告封存成功 | .evidence/YYYYMMDD-HHMMSS/ 中含 narrative_free_report.json 與其 hash |
| 模組狀態封存 | glcm_config_used.yaml 封存於 .evidence/ |

### Phase 3: Cross-Language Compliance

| 條件 | 驗證方式 |
|------|----------|
| 可封存語言對照 | language_map.json 與 semantic_tokens.json 對應一致 |
| 可重播驗證 | 任一語言輸入 → semanticize → hash → replay 驗證一致性 |
| 語意中立 hash | hash 與語言無關，僅來自 semantic 層 |

---

## Governance Assertions

### GL-NFC-001: Zero Narrative
- All outputs MUST NOT contain narrative language
- GLCM-NAR violations MUST be zero

### GL-NFC-002: Sealed Conclusions
- All conclusion statements MUST have trace/hash/evidence
- GLCM-UNC violations MUST be zero OR evidence_found: true

### GL-NFC-003: No Fabricated Timelines
- All "completed/fixed" statements MUST have hash/trace/complement evidence
- GLCM-FCT violations MUST be zero OR evidence_found: true
- **CRITICAL**: Fabricated timeline without evidence = BLOCKER

### GL-NFC-004: Evidence Chain Integrity
- All claims MUST reference sealed artifacts
- Evidence hints MUST be within 300 characters

### GL-NFC-005: Language Neutrality
- hash MUST be language-independent
- Semantic tokens MUST be the sole source of hash

---

## Adaptive Mode (GLCM-Auto)

### Automatic Mode Switching

**Purpose**: Automatically enable/disable GLCM modules based on context.

**Rules** (adaptive_rules.yaml):
```yaml
rules:
  # Governance Reports - Strictest Mode
  - if:
      output_path: "outputs/selfhealing/*.json"
      context: "governance_report"
    enable:
      - GLCM-NAR
      - GLCM-UNC
      - GLCM-EVC
      - GLCM-FCT
    disable:
      - GLCM-EMO
      - GLCM-SOFT
      - GLCM-EXC

  # Documentation - Softer Mode
  - if:
      output_path: "docs/**/*.md"
      context: "documentation"
    enable:
      - GLCM-SOFT
    disable:
      - GLCM-UNC
      - GLCM-EVC
      - GLCM-FCT

  # Human Dialogue - Most Permissive
  - if:
      output_path: "chatlogs/*.txt"
      context: "human_dialogue"
    enable:
      - GLCM-EMO
      - GLCM-SOFT
    disable:
      - GLCM-NAR
      - GLCM-UNC
      - GLCM-EVC
      - GLCM-FCT

  # Dev Branch - Allow Soft Narrative
  - if:
      branch: "dev"
    enable:
      - GLCM-SOFT
    disable:
      - GLCM-NAR

  # Main Branch - Strictest Mode
  - if:
      branch: "main"
    enable:
      - GLCM-NAR
      - GLCM-UNC
      - GLCM-EVC
      - GLCM-FCT
    disable:
      - GLCM-SOFT
```

---

## Integration with CI/CD

### GitHub Actions Workflow

```yaml
- name: Run Narrative-Free Compliance Scan
  run: |
    python3 ecosystem/tools/compliance/glnarrativefree_scanner.py ./outputs/ --context governance_report
    cat narrative_free_compliance_report.json
    # Fail if CRITICAL violations found
    test $(jq '.summary.fabricated_timelines' narrative_free_compliance_report.json) -eq 0
    # Fail if unsealed claims without evidence found
    test $(jq '.summary.unsealed_conclusions_without_evidence' narrative_free_compliance_report.json) -eq 0
```

---

## File Structure

```
ecosystem/
├── governance/
│   ├── GL-LanguageNeutralHash-Spec-v1.md
│   └── GL-NarrativeFreeCompliance-Spec-v2.md
├── tools/
│   └── compliance/
│       ├── glnarrativefree_scanner.py
│       ├── glnarrativefree_scanner_strict.py
│       ├── semanticizer.py
│       └── canonicalizer.py
└── tests/
    └── compliance/
        ├── test_language_neutral_hash.py
        └── test_narrative_free_compliance.py
```

---

## Sealing Procedure

After scanning, seal:
```bash
mkdir -p .evidence/$(date +%Y%m%d-%H%M%S)/
cp narrative_free_compliance_report.json .evidence/$(date +%Y%m%d-%H%M%S)/
cp glcm_config_used.yaml .evidence/$(date +%Y%m%d-%H%M%S)/
sha256sum .evidence/$(date +%Y%m%d-%H%M%S)/narrative_free_compliance_report.json > .evidence/$(date +%Y%m%d-%H%M%S)/hash_narrative_report.txt
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-01-15 | Initial narrative-free compliance spec |
| 2.0 | 2024-02-05 | **ADD**: GLCM-FCT (Fabricated Completion Timeline) detection |
| 2.0 | 2024-02-05 | **ADD**: Multi-language support (zh, en, ja, ko, de, fr) |
| 2.0 | 2024-02-05 | **ADD**: Adaptive mode (GLCM-Auto) |
| 2.0 | 2024-02-05 | **ADD**: Evidence verification within 300 characters |

---

## References

- Plain Writing Act Compliance Report - USDA (2024)
- Government Auditing Standards 2024 Revision - GAO
- Narrative-free governance principles - MIT Law (2024)
- Blockchain evidence integrity verification - Rapid Innovation (2024)