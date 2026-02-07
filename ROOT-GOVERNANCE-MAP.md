# Root Governance Responsibility Map

Governance directories are now named by responsibility boundary (`responsibility-*`). This map clarifies each boundary, separation of duties, allowed interfaces, and violation handling to keep the governance loop closed.

## Directory Responsibilities and Boundaries

| Directory | Role | Responsibility Boundary | Inputs | Outputs | Violation Handling | Interfaces |
|-----------|------|-------------------------|--------|---------|--------------------|------------|
| `responsibility-governance-anchor-boundary/` (formerly `governance-root-anchor/`) | Unified governance anchor | Maintains baseline, semantic tree, hash boundary, event model, and verification rules; no execution logic lives here | Governance specs, module bindings, semantic attachments | Authoritative specs (baseline, semantic tree, hash specs, event/event rules) | Rejects unsigned/unknown artifacts; any drift from baseline marks modules as non-compliant until reconciled | Read-only by engines/scanners; updated only via governed change control |
| `responsibility-governance-execution-boundary/` (formerly `governance-execution-engine/`) | Execution core | Runs pipelines, gates, evidence verification, and replay; does not mutate anchor specs | Module registry entries, anchor specs, scanner results | Execution events, evidence, gate outcomes, replay traces | Fails fast on gate violations; records failure event and halts module promotion | Consumes anchor specs and scanner outputs; emits events to monitoring/logging |
| `responsibility-governance-sensing-boundary/` (formerly `governance-scanner-sensing/`) | Sensing layer | Discovers modules, bindings, pipelines, gates, semantic attachments, and hash boundaries; no execution | Filesystem modules, bindings, hash specs | Scan report (modules, integrity hashes, semantic attachment status, pipeline inventory) | Flags missing bindings/specs/pipelines; marks modules as pending remediation | Provides reports to execution engine and governance anchor maintainers |

## Closed-Loop Governance Flow

```
responsibility-governance-sensing-boundary (discover + assess)
        │ scan-report.json
        ▼
responsibility-governance-execution-boundary (execute pipelines, gates, replay, evidence verification)
        │ events, evidence, traces
        ▼
responsibility-governance-anchor-boundary (baseline + semantic + hash + event + verification rules)
        │ rules/updates (governed change control)
        └────────────────────────────────────────────────────┐
                                                             │
                 ←──────── feedback on drift/violations ─────┘
```

## Separation of Duties

- **Specification stewardship:** confined to `governance-root-anchor/` (policy owners only).
- **Operational execution:** confined to `governance-execution-engine/` (runbooks, pipelines, gates).
- **Sensing and discovery:** confined to `governance-scanner-sensing/` (inventory, integrity, semantic attachment).

## Violation Handling

- Missing binding/semantic attachment/hash coverage → scanner flags, engine blocks execution, anchor remains unchanged.
- Gate or consistency failure → engine stops module advancement, records failure event, requires remediation before retry.
- Hash boundary drift → scanner reports, engine refuses execution until hashes align with anchor specs.

## Minimal Interfaces

- Scanner → Engine: `report/scan-report.json`
- Engine → Anchor: read anchor specs; emit events against anchor-defined model
- Anchor → Engine/Scanner: governed spec updates only through approved change control
