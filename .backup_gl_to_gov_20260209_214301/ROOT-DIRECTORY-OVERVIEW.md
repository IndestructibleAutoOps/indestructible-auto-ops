# Root Directory Overview (Responsibility-Centric)

This document explains the root layout with responsibility boundaries, roles, and interactions. Core components are marked `Core`; support/auxiliary pieces are marked `Aux`.

## Root Tree (top-level)

```text
.
├── README.md
├── makefile
├── ROOT-RESPONSIBILITY-BOUNDARIES.md
├── ROOT-GOVERNANCE-MAP.md
├── .agent_hooks/ (Aux)
├── .config/ (Aux)
├── .evidence/ (Aux)
├── .github/ (Core)
├── .governance/ (Core)
├── archives/ (Aux)
├── audit-automation/ (Aux)
├── config/ (Core)
├── deployment/ (Core)
├── deployment-scripts/ (Core)
├── docs/ (Core)
├── indestructibleautoops/ (Core)
├── machinenativeops/ (Core)
├── monitoring/ (Core)
├── platforms/ (Core)
├── responsibility-*/ (Core, governance boundaries)
├── scripts/ (Core)
├── tests/ (Core)
└── other root files (plans, status, reports)
```

## Functional Responsibilities (2–3 sentences each)

| Component | Core/Aux | Responsibility (scope) | Not responsible for | Key interactions/dependencies |
|-----------|----------|------------------------|---------------------|-------------------------------|
| README.md | Core | Entry overview for the project and quick links to docs; sets context for contributors. | Does not hold detailed specs or runbooks. | Points to `docs/`, responsibility boundaries, and scripts. |
| makefile | Core | Standard task runner entry for tests/builds/automation. | Does not define business logic. | Invokes tools in `scripts/`, `deployment-scripts/`, `tests/`. |
| ROOT-RESPONSIBILITY-BOUNDARIES.md | Core | Defines responsibility-boundary names and scopes. | Not a substitute for per-boundary specs. | Aligns with `responsibility-*` directories and `ROOT-GOVERNANCE-MAP.md`. |
| ROOT-GOVERNANCE-MAP.md | Core | Closed-loop governance map (sensing → execution → anchor). | Not hosting executable pipelines. | Interfaces among `responsibility-governance-*` boundaries. |
| .agent_hooks/ | Aux | Hook scripts for automated governance checks. | Not general CI workflows. | Called by repo automation; relates to `.governance/`. |
| .config/ | Aux | Local tool/config cache (non-governed). | Not source of truth for policies. | Used by tooling; secondary to `config/`. |
| .evidence/ | Aux | Stores generated evidence artifacts. | Not a working directory for code. | Consumed by auditors and reports in `docs/`/status files. |
| .github/ | Core | CI/CD workflows, issue templates, governance bots. | No product logic. | Drives pipeline runs that execute `scripts/`, `tests/`, `deployment-scripts/`. |
| .governance/ | Core | Governance kernel metadata and audit anchors. | Not runtime code. | Referenced by responsibility boundaries and CI checks. |
| archives/ | Aux | Historical artifacts and snapshots. | Not active specs or code. | Read-only reference for audits. |
| audit-automation/ | Aux | Automation helpers for audits and scans. | Not hosting primary policies. | Consumes configs from `config/`, outputs to `.evidence/`. |
| config/ | Core | Central configuration (shared parameters, policy inputs). | Not long-form documentation. | Consumed by `scripts/`, `deployment-scripts/`, `responsibility-*`. |
| deployment/ | Core | Deployment manifests and environment definitions. | Not CI logic or governance specs. | Used by `deployment-scripts/` and ops tooling. |
| deployment-scripts/ | Core | Executable deployment/runbook scripts. | Not policy source; follows configs. | Uses `config/`, targets defined in `deployment/`, reports to `.evidence/`. |
| docs/ | Core | Formal documentation, runbooks, architecture notes. | Not executable code. | References all boundaries and subsystems; linked from README. |
| indestructibleautoops/ | Core | Primary project code/workspace (runtime, tooling). | Not historical archive. | Depends on `config/`, tested via `tests/`, governed by responsibility boundaries. |
| machinenativeops/ | Core | Machine Native Ops consolidated workspace. | Not CI configs. | Shares governance with `responsibility-*`; may feed artifacts to `docs/`. |
| monitoring/ | Core | Monitoring stacks/configs outside Grafana boundary. | Not deployment scripts. | Feeds observability pipelines; may depend on `config/` and `responsibility-observability-grafana-boundary/`. |
| platforms/ | Core | Platform definitions and mappings. | Not governance policies. | Consumed by deployment and ops tools; aligns with `responsibility-gl-layers-boundary/`. |
| scripts/ | Core | Utility/maintenance scripts (non-deployment). | Not long-term docs. | Invoked by makefile and CI; uses `config/`. |
| tests/ | Core | Automated test suites. | Not runtime code or docs. | Validate `indestructibleautoops/` and related workspaces. |
| responsibility-governance-anchor-boundary/ | Core | Authoritative governance baselines (semantic tree, hashes, events). | No execution logic. | Read-only source for execution/sensing boundaries. |
| responsibility-governance-execution-boundary/ | Core | Runs pipelines/gates/evidence verification. | Does not change anchor specs. | Consumes anchor and sensing outputs; emits evidence to `.evidence/`. |
| responsibility-governance-sensing-boundary/ | Core | Scans modules, bindings, hash/semantic coverage. | No execution of pipelines. | Produces scan reports for execution/anchor. |
| responsibility-governance-specs-boundary/ | Core | Core governance specs and workflows. | No deployment scripts. | Provides policies read by anchor/execution; coordinates with global policy. |
| responsibility-global-policy-boundary/ | Core | Cross-cutting policies, naming rules, defaults. | No platform-specific configs. | Feeds other boundaries; aligns with namespace and gateway. |
| responsibility-gl-layers-boundary/ | Core | GL00-99 layer definitions and artifacts. | No runtime automation. | Supplies layer taxonomy to other boundaries and platforms. |
| responsibility-gates-boundary/ | Core | Operational gate definitions/approval matrices. | Not traffic routing. | Inputs to execution; constrained by guardrails. |
| responsibility-gap-boundary/ | Core | Gap analysis, remediation plans, tracking. | No code fixes. | Reports to execution/guardrails; references docs. |
| responsibility-gateway-boundary/ | Core | API/network gateway specs and controls. | Not CI gates or business logic. | Coordinates with global/guardrails; informs deployment/monitoring. |
| responsibility-guardrails-boundary/ | Core | Safety/compliance guardrails and detection policies. | Not execution scripts. | Constrains execution/gateway; aligned with anchor. |
| responsibility-gcp-boundary/ | Core | GCP-specific governance (IAM, labels, constraints). | No multi-cloud/global defaults. | Works with deployment and monitoring for GCP targets. |
| responsibility-generation-boundary/ | Core | Artifact generation policies and provenance rules. | Not storing binaries. | Applies to execution outputs; ties to guardrails for signing. |
| responsibility-quantum-stack-boundary/ | Core | Governance Quantum Stack layers/contracts. | Not traditional ops policies. | Coordinates with anchor and guardrails; informs observability. |
| responsibility-group-boundary/ | Core | Group/tenant rules and shared-resource policies. | Not individual app settings. | Interacts with namespace/global policies; monitored via observability. |
| responsibility-observability-grafana-boundary/ | Core | Grafana dashboards, data source standards, alert thresholds. | Not raw telemetry. | Consumes execution events/monitoring feeds; feedback to anchor. |
| responsibility-mnga-architecture-boundary/ | Core | Machine Native Governance Architecture strategy/charters. | Not operational runbooks. | Guides mno/exec/global boundaries. |
| responsibility-mno-operations-boundary/ | Core | Machine Native Ops operational governance and lifecycle. | Not strategic architecture. | Drives execution and deployment policies; follows mnga guidance. |
| responsibility-namespace-governance-boundary/ | Core | Namespace/domain/tenant naming and isolation controls. | Not routing rules. | Works with global/gateway/group policies. |

## Interaction & Dependency Notes

- Governance loop: sensing → execution → anchor → feedback (see `ROOT-GOVERNANCE-MAP.md`).
- Policy flow: mnga (strategy) → global/guardrails/gates → execution/deployment → monitoring/observability → reports in `.evidence/` and `docs/`.
- Data flow: code in `indestructibleautoops/` & `machinenativeops/` uses `config/` and is validated by `tests/`; deployment uses `deployment/` + `deployment-scripts/`; monitoring feeds `responsibility-observability-grafana-boundary/`.
