# Research Loop Boot Sequence (Isolation Import)

This workflow turns the "retrieve -> reason -> validate" loop into a mandatory
pre-work SOP while preserving the zero-external-dependencies constraint.
All external knowledge is imported via a controlled isolation zone and stored
as offline snapshots (refpacks).

## Core Principles
- **No direct egress from the closed zone**.
- **Isolation import only** for any external/global research.
- **Every run is auditable** with frozen evidence and run artifacts.
- **Naming/spec/rule alignment** is enforced through mapping and registry IDs.

## Entry Points
- Workflow: `governance/workflows/research-loop/workflow.yaml`
- Gates: `governance/workflows/research-loop/gates.yaml`
- Import Pipeline: `governance/workflows/research-loop/import-pipelines.yaml`
- Name Map: `governance/workflows/research-loop/mappings/naming-map.yaml`
- Registry: `governance/workflows/research-loop/references/registry.yaml`

## Run Artifacts (Default)
`reports/research-runs/{run_id}/`
- `intake.md`
- `gap-list.md`
- `evidence/*.jsonl`
- `provenance/*-audit.json`
- `synthesis.md`
- `outputs/architecture-plan.md`
- `outputs/naming-map.json`
- `outputs/pr-plan.yaml`

## Gate Behavior
External/global stages are only allowed through isolation import:
- `EGRESS-EXTERNAL-ISOLATION`
- `EGRESS-GLOBAL-ISOLATION`

## Mapping Policy
Any external naming or draft terminology must be mapped to internal IDs.
See `mappings/naming-map.yaml` for normalized IDs.
