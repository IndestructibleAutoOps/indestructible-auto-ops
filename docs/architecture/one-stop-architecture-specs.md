# One-Stop Architecture and Specification Hub

Last Updated: 2026-02-05

This document is the consolidated entry point for the repository's architecture
and specification sources. Use it to locate canonical docs, understand where
each layer lives, and close the loop from specs to implementation, validation,
and evidence.

## Quick Start (by role)

- Executive / Program: [README.md](README.md),
  [executive_summary.md](executive_summary.md),
  [WORKSPACE_STATUS.md](WORKSPACE_STATUS.md)
- Architect / Tech Lead: [gov-enterprise-architecture/README.md](gov-enterprise-architecture/README.md),
  [directory-boundary-specification.md](gov-enterprise-architecture/governance/directory-boundary-specification.md),
  [boundary-reference-matrix.md](gov-enterprise-architecture/governance/boundary-reference-matrix.md),
  [designs/multi-agent-architecture.md](designs/multi-agent-architecture.md),
  [gov-runtime-engine-platform/SPEC.md](gov-runtime-engine-platform/SPEC.md)
- Developer: [Layer READMEs](#canonical-architecture-map-gov-layers),
  [ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md](governance/specs/ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md),
  [scripts/](scripts/)
- Compliance / QA: [boundary_checker.py](gov-governance-compliance-platform/scripts/boundary_checker.py),
  [policies](.github/governance/policies/),
  [evidence/](evidence/),
  [reports/](reports/)

## Canonical Architecture Map (GL Layers)

| GL Layer | Purpose | Canonical Docs | Implementation Roots |
| --- | --- | --- | --- |
| GL00-09 | Enterprise governance and architecture | [gov-enterprise-architecture/README.md](gov-enterprise-architecture/README.md)<br>[directory-boundary-specification.md](gov-enterprise-architecture/governance/directory-boundary-specification.md)<br>[boundary-reference-matrix.md](gov-enterprise-architecture/governance/boundary-reference-matrix.md)<br>[boundary-enforcement-rules.md](gov-enterprise-architecture/governance/boundary-enforcement-rules.md) | `gov-enterprise-architecture/` (canonical)<br>`gov-governance-architecture-platform/` (mirror) |
| GL10-29 | Platform services | [gov-platform-services/README.md](gov-platform-services/README.md) | `gov-platform-services/`<br>`gov-automation-*`<br>`gov-platform-core-platform/` |
| GL20-29 | Data processing | [gov-data-processing/README.md](gov-data-processing/README.md)<br>[gov-data-processing-platform/README.md](gov-data-processing-platform/README.md) | `gov-data-processing/`<br>`gov-data-processing-platform/`<br>`gov-search-elasticsearch-platform/` |
| GL30-49 | Execution runtime | [gov-execution-runtime/README.md](gov-execution-runtime/README.md) | `gov-execution-runtime/`<br>`gov-runtime-engine-platform/`<br>`gov-runtime-execution-platform/` |
| GL50-59 | Observability | [gov-observability/README.md](gov-observability/README.md)<br>[gov-monitoring-observability-platform/README.md](gov-monitoring-observability-platform/README.md) | `gov-observability/`<br>`gov-monitoring-observability-platform/`<br>`gov-monitoring-system-platform/` |
| GL60-80 | Governance compliance | [gov-governance-compliance-platform/README.md](gov-governance-compliance-platform/README.md) | `gov-governance-compliance/`<br>`gov-governance-compliance-platform/` |
| GL81-83 | Extension services | [gov-extension-services/README.md](gov-extension-services/README.md)<br>[gov-extension-services-platform/README.md](gov-extension-services-platform/README.md) | `gov-extension-services/`<br>`gov-extension-services-platform/` |
| GL90-99 | Meta specifications | [gov-meta-specifications/README.md](gov-meta-specifications/README.md)<br>[.github/governance/GL-README.md](.github/governance/GL-README.md) | `gov-meta-specifications/`<br>`.github/governance/`<br>`gov-governance-architecture-platform/GL90-99-Meta-Specification-Layer/` |

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

- [AEP Engine Overview](gov-runtime-engine-platform/README.md)
- [AEP Engine Spec](gov-runtime-engine-platform/SPEC.md)
- [ETL Pipeline System Architecture](gov-runtime-engine-platform/etl-pipeline/docs/architecture/system-architecture.md)
- [ETL Pipeline GL Layer Mapping](gov-runtime-engine-platform/etl-pipeline/docs/guides/gov-layer-mapping.md)
- [Runtime Execution Platform Overview](gov-runtime-execution-platform/README.md)
- [Runtime Execution AEP Spec](gov-runtime-execution-platform/engine/SPEC.md)
- [Data Processing Platform Overview](gov-data-processing-platform/README.md)

## Agent System Architecture

- [AGENTS.md](AGENTS.md)
- [Multi-Agent Architecture Design](designs/multi-agent-architecture.md)
- [MONICA AI Agent Engineering Specification](MONICA_AI_AGENT_ENGINEERING_SPECIFICATION.md)
- [Agent Configuration README](.github/config/agents/README.md)

## Governance and Policy Sources

- [GL Governance README](.github/governance/GL-README.md)
- [Governance Architecture Overview](.github/governance/GOVERNANCE-ARCHITECTURE-OVERVIEW.md)
- [GL Architecture Quick Reference](.github/governance/architecture/gov-quickref.md)
- [GL Architecture Readme](.github/governance/architecture/gov-architecture-readme.md)
- [Security Policy](.github/governance/policies/security-policy.md)
- [Repository Policies](policies/)

## Compliance, Validation, and Evidence

- [Boundary Checker](gov-governance-compliance-platform/scripts/boundary_checker.py)
- [Naming Validator](gov-governance-compliance/scripts/naming/gl_naming_validator.py)
- [Evolution Engine](gov-governance-compliance/scripts/evolution/gov_evolution_engine.py)
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
- `gov-governance-architecture-platform/GL90-99-Meta-Specification-Layer/governance/archived/legacy/`
  contains archived governance artifacts.

## Closed-Loop Update Workflow

When adding or updating a spec or architecture document, close the loop:

1. Add/update the spec in `governance/specs/` or `ecosystem/governance/`.
2. Link the implementation in the relevant GL layer or `gl-*-platform/`.
3. Add or update validation in `gov-governance-compliance*/` or `scripts/`.
4. Attach evidence in `evidence/` or `reports/`.
5. Update this hub so the entry point stays current.
