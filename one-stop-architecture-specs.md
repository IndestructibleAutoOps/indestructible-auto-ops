# One-Stop Architecture and Specification Hub

Last Updated: 2026-02-05

This document is the consolidated entry point for the repository's architecture
and specification sources. Use it to locate canonical docs, understand where
each layer lives, and close the loop from specs to implementation, validation,
and evidence.

## Quick Start (by role)

- Executive / Program: [readme.md](readme.md),
  [executive_summary.md](executive_summary.md),
  [workspace-status.md](workspace-status.md)
- Architect / Tech Lead: [gl-enterprise-architecture/readme.md](gl-enterprise-architecture/readme.md),
  [directory-boundary-specification.md](gl-enterprise-architecture/governance/directory-boundary-specification.md),
  [boundary-reference-matrix.md](gl-enterprise-architecture/governance/boundary-reference-matrix.md),
  [designs/multi-agent-architecture.md](designs/multi-agent-architecture.md),
  [gl-runtime-engine-platform/SPEC.md](gl-runtime-engine-platform/SPEC.md)
- Developer: [Layer READMEs](#canonical-architecture-map-gl-layers),
  [ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md](governance/specs/ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md),
  [scripts/](scripts/)
- Compliance / QA: [boundary_checker.py](gl-governance-compliance-platform/scripts/boundary_checker.py),
  [policies](.github/governance/policies/),
  [evidence/](evidence/),
  [reports/](reports/)

## Canonical Architecture Map (GL Layers)

| GL Layer | Purpose | Canonical Docs | Implementation Roots |
| --- | --- | --- | --- |
| GL00-09 | Enterprise governance and architecture | [gl-enterprise-architecture/readme.md](gl-enterprise-architecture/readme.md)<br>[directory-boundary-specification.md](gl-enterprise-architecture/governance/directory-boundary-specification.md)<br>[boundary-reference-matrix.md](gl-enterprise-architecture/governance/boundary-reference-matrix.md)<br>[boundary-enforcement-rules.md](gl-enterprise-architecture/governance/boundary-enforcement-rules.md) | `gl-enterprise-architecture/` (canonical)<br>`gl-governance-architecture-platform/` (mirror) |
| GL10-29 | Platform services | [gl-platform-services/readme.md](gl-platform-services/readme.md) | `gl-platform-services/`<br>`gl-automation-*`<br>`gl-platform-core-platform/` |
| GL20-29 | Data processing | [gl-data-processing/readme.md](gl-data-processing/readme.md)<br>[gl-data-processing-platform/readme.md](gl-data-processing-platform/readme.md) | `gl-data-processing/`<br>`gl-data-processing-platform/`<br>`gl-search-elasticsearch-platform/` |
| GL30-49 | Execution runtime | [gl-execution-runtime/readme.md](gl-execution-runtime/readme.md) | `gl-execution-runtime/`<br>`gl-runtime-engine-platform/`<br>`gl-runtime-execution-platform/` |
| GL50-59 | Observability | [gl-observability/readme.md](gl-observability/readme.md)<br>[gl-monitoring-observability-platform/readme.md](gl-monitoring-observability-platform/readme.md) | `gl-observability/`<br>`gl-monitoring-observability-platform/`<br>`gl-monitoring-system-platform/` |
| GL60-80 | Governance compliance | [gl-governance-compliance-platform/readme.md](gl-governance-compliance-platform/readme.md) | `gl-governance-compliance/`<br>`gl-governance-compliance-platform/` |
| GL81-83 | Extension services | [gl-extension-services/readme.md](gl-extension-services/readme.md)<br>[gl-extension-services-platform/readme.md](gl-extension-services-platform/readme.md) | `gl-extension-services/`<br>`gl-extension-services-platform/` |
| GL90-99 | Meta specifications | [gl-meta-specifications/readme.md](gl-meta-specifications/readme.md)<br>[.github/governance/GL-readme.md](.github/governance/GL-readme.md) | `gl-meta-specifications/`<br>`.github/governance/`<br>`gl-governance-architecture-platform/GL90-99-Meta-Specification-Layer/` |

## Core Specifications and Protocols

### Governance (Canonical)

- [ARCHITECTURE-TO-CODE-PROTOCOL.md](governance/specs/ARCHITECTURE-TO-CODE-PROTOCOL.md)
- [ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md](governance/specs/ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md)
- [ARCHITECTURE-TO-CODE-PROTOCOL-DELIVERABLES.md](governance/specs/ARCHITECTURE-TO-CODE-PROTOCOL-DELIVERABLES.md)
- [AUTONOMY-BOUNDARY-TEST-SPEC.md](governance/specs/AUTONOMY-BOUNDARY-TEST-SPEC.md)
- [AUTONOMY-BOUNDARY-TEST-INTEGRATION.md](governance/specs/AUTONOMY-BOUNDARY-TEST-INTEGRATION.md)
- [GOVERNANCE-ENGINE-MIGRATION-GUIDE.md](governance/specs/GOVERNANCE-ENGINE-MIGRATION-GUIDE.md)

### Ecosystem Governance Specs

- [materialization-complement-spec-v2.md](ecosystem/governance/materialization-complement-spec-v2.md)
- [canonical-hash-chain-spec.md](ecosystem/governance/canonical-hash-chain-spec.md)
- [hash-storage-specification.md](ecosystem/governance/hash-storage-specification.md)
- [governance-closure-engine-spec-v1.md](ecosystem/governance/governance-closure-engine-spec-v1.md)
- [reporting-governance-spec.md](ecosystem/governance/reporting-governance-spec.md)
- [tool-definition-protocol.md](ecosystem/governance/tool-definition-protocol.md)
- [evidence-verification-engine-spec-v1.md](ecosystem/governance/evidence-verification-engine-spec-v1.md)
- [semantic-defense-specification.md](ecosystem/governance/semantic-defense-specification.md)

### Architecture References (Ecosystem)

- [components.md](ecosystem/governance/docs/architecture/components.md)
- [layers.md](ecosystem/governance/docs/architecture/layers.md)
- [metrics.md](ecosystem/governance/docs/architecture/metrics.md)

## Runtime and Platform Architecture

- [AEP Engine Overview](gl-runtime-engine-platform/readme.md)
- [AEP Engine Spec](gl-runtime-engine-platform/SPEC.md)
- [ETL Pipeline System Architecture](gl-runtime-engine-platform/etl-pipeline/docs/architecture/system-architecture.md)
- [ETL Pipeline GL Layer Mapping](gl-runtime-engine-platform/etl-pipeline/docs/guides/gl-layer-mapping.md)
- [Runtime Execution Platform Overview](gl-runtime-execution-platform/readme.md)
- [Runtime Execution AEP Spec](gl-runtime-execution-platform/engine/SPEC.md)
- [Data Processing Platform Overview](gl-data-processing-platform/readme.md)

## Agent System Architecture

- [AGENTS.md](AGENTS.md)
- [Multi-Agent Architecture Design](designs/multi-agent-architecture.md)
- [MONICA AI Agent Engineering Specification](monica-ai-agent-engineering-specification.md)
- [Agent Configuration README](.github/config/agents/readme.md)

## Governance and Policy Sources

- [GL Governance README](.github/governance/GL-readme.md)
- [Governance Architecture Overview](.github/governance/GOVERNANCE-ARCHITECTURE-OVERVIEW.md)
- [GL Architecture Quick Reference](.github/governance/architecture/gl-quickref.md)
- [GL Architecture Readme](.github/governance/architecture/gl-architecture-readme.md)
- [Security Policy](.github/governance/policies/security-policy.md)
- [Repository Policies](policies/)

## Compliance, Validation, and Evidence

- [Boundary Checker](gl-governance-compliance-platform/scripts/boundary_checker.py)
- [Naming Validator](gl-governance-compliance/scripts/naming/gl_naming_validator.py)
- [Evolution Engine](gl-governance-compliance/scripts/evolution/gl_evolution_engine.py)
- [Validation Scripts](scripts/)
- [Tests](tests/)
- [Evidence](evidence/)
- [Audit Reports](audit-reports/)
- [Reports](reports/)

## Integration and Migration Guides

- [execution-plan.md](execution-plan.md)
- [migration-strategy.md](migration-strategy.md)
- [structure-migration-plan.md](structure-migration-plan.md)
- [architecture-to-code-implementation-plan.md](architecture-to-code-implementation-plan.md)
- [Integration Docs Index](.github/docs/INTEGRATION-DOCS-INDEX.md)
- [Documentation Portal](.github/docs/DOCUMENTATION-PORTAL.md)

## Mirrors, Archives, and Legacy Sources

Some documents are mirrored or archived for historical reference. Prefer the
canonical sources listed above unless you are explicitly validating legacy
work.

- `machine-native-ops/` contains historical mirrors of runtime docs.
- `gl-governance-architecture-platform/GL90-99-Meta-Specification-Layer/governance/archived/legacy/`
  contains archived governance artifacts.

## Closed-Loop Update Workflow

When adding or updating a spec or architecture document, close the loop:

1. Add/update the spec in `governance/specs/` or `ecosystem/governance/`.
2. Link the implementation in the relevant GL layer or `gl-*-platform/`.
3. Add or update validation in `gl-governance-compliance*/` or `scripts/`.
4. Attach evidence in `evidence/` or `reports/`.
5. Update this hub so the entry point stays current.
