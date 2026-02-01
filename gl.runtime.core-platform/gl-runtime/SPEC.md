# GL Runtime Unified Structure Specification (URSS)
Version: 1.0.0

## 1. 架構原則
- **層級純淨性**: 每版本僅包含該層級能力
- **可演化性**: 目錄結構可自然演化至 V25
- **治理就緒**: 所有模組具備可審計性、可追蹤性
- **版本隔離**: 版本間完全隔離，僅共享 shared/

## 2. 統一目錄結構
```
<version>/
├── README.md
├── VERSION
├── manifest.json
├── docs/
│   ├── overview/
│   ├── specs/
│   ├── api/
│   └── adr/
├── src/
│   ├── core/
│   ├── adapters/
│   ├── interfaces/
│   └── utils/
├── tests/
├── examples/
├── ops/
├── scripts/
└── config/
```

## 3. 版本演化路徑
```
V1 → V2 → V3 → V4 → V5 → V6 → V7 → V8 → V9 → V10 → V11
      ↓
      V12 → V13 → V14 → V15 → V16 → V17 → V18 → V19 → V20
      
V21 → V22
       ↘
        V23 → V24 → V0 Pro → V25
```

## 4. 治理層級
| Level | 名稱 | 適用版本 |
|-------|------|----------|
| 0 | No Governance | V1-V2 |
| 1 | Basic Governance | V3 |
| 2 | Repair/Optimization | V4-V5 |
| 3 | Collaboration/DAG | V6-V7 |
| 4 | Semantic/Evolution | V8-V20 |
| 5 | Root/Meta Governance | V23-V24 |
