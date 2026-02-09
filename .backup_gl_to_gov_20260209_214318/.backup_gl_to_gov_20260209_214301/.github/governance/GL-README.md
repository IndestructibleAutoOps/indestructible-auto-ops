# GL (Governance Layers) 架構 - Migrated

GL 是 MachineNativeOps 的核心治理架構，定義了從戰略到執行的完整治理層級。

## Migration Status

**✅ GL Migration Complete** - All GL artifacts have been migrated to their proper locations:
- Artifacts: `engine/governance/gl-artifacts/`
- Architecture: `.github/governance/architecture/`
- Sealed: `.github/governance/sealed/`

## Current Directory Structure

```
engine/governance/gl-artifacts/
├── strategic/          # GL00-09 戰略層
├── operational/        # GL10-29 運營層
├── data/               # GL20-29 資料層
├── execution/          # GL30-49 執行層
├── observability/      # GL50-59 觀測層
├── feedback/           # GL60-80 回饋層
├── extended/           # GL81-83 擴展層
└── meta/               # GL90-99 元規範層

.github/governance/
├── architecture/       # GL 核心架構定義
├── sealed/            # 已封存的治理決策
└── GL-README.md       # 本文件
```

## GL 層級速查

| 層級 | 名稱 | 職責 |
|------|------|------|
| GL00-09 | Strategic | 願景、架構、決策、風險、合規 |
| GL10-29 | Operational | 政策、流程、工具、品質管理 |
| GL30-49 | Execution | 模板、Schema、自動化、配置 |
| GL50-59 | Observability | 監控、指標、告警、洞察 |
| GL60-80 | Feedback | AI優化、回饋機制、審計 |
| GL81-83 | Extended | 外部整合、自動評論 |
| GL90-99 | Meta | 命名規範、語意定義 |

## 快速使用

```bash
# 查詢檔案的 GL 層級
npx ts-node engine/governance/gl_engine.ts validate --strict

# 驗證 GL 結構
npx ts-node engine/governance/gl_engine.ts validate --workspace engine
```

## 在程式碼中標註 GL 層級

```typescript
// @GL-governed
// @GL-layer: GL-L1-CORE
// @GL-semantic: governance-layer-core
// @GL-revision: 1.0.0
// @GL-status: active
```

```yaml
# GL-Layer: GL10-29
metadata:
  layer: "GL10-29"
```

## GL Integration Status

- ✅ Engine Module: Integrated
- ✅ File Organizer System: Integrated
- ✅ Agent Orchestration: Active
- ✅ CI/CD Pipelines: Configured
- ✅ Git Hooks: Configured
- ✅ GL Markers: Applied to all files (4057 files)

**GL Unified Charter**: ✅ **ACTIVATED**