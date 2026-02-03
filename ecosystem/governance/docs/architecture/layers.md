# Architecture Layers

Generated: 2026-02-03T14:25:40.850614Z

## meta-spec

Components: 6

- governance.meta-spec.format.meta-format.schema
- governance.meta-spec.language.meta-language.spec
- governance.meta-spec.meta-spec.meta
- governance.meta-spec.registry.specs.registry
- governance.meta-spec.semantics.meta-semantics
- governance.meta-spec.topology.meta-topology

## ugs

Components: 10

- governance.ugs.l00-language.grammar.ast
- governance.ugs.l00-language.grammar.tokens
- governance.ugs.l00-language.ldl.spec
- governance.ugs.l02-semantics.layer-semantics
- governance.ugs.l03-index.index-spec
- governance.ugs.l04-topology.topology-spec
- governance.ugs.l50-format.governance.schema
- governance.ugs.l50-format.layer.schema
- governance.ugs.l50-format.naming.schema
- governance.ugs.ugs.meta

## governance

Components: 49

- contracts.governance.ROLE_LANGUAGE_SPECIFICATION
- contracts.governance.ROLE_RUNTIME_FLOW
- contracts.governance.ROLE_SYSTEM_IMPLEMENTATION_COMPLETE
- contracts.governance.role.schema
- contracts.governance.roles.ecosystem.analyst
- contracts.governance.roles.ecosystem.architect
- contracts.governance.roles.ecosystem.runner
- contracts.governance.roles.ecosystem.semantic-checker
- contracts.governance.roles.ecosystem.validator
- contracts.governance.roles.registry
- contracts.naming-governance.gl-build-layer-specification
- contracts.naming-governance.gl-ci-cd-layer-specification
- contracts.naming-governance.gl-dependency-layer-specification
- contracts.naming-governance.gl-deployment-layer-specification
- contracts.naming-governance.gl-documentation-layer-specification
- contracts.naming-governance.gl-extensibility-layer-specification
- contracts.naming-governance.gl-generator-layer-specification
- contracts.naming-governance.gl-governance-layer-specification
- contracts.naming-governance.gl-indexing-layer-specification
- contracts.naming-governance.gl-interface-layer-specification
- contracts.naming-governance.gl-metadata-layer-specification
- contracts.naming-governance.gl-observability-layer-specification
- contracts.naming-governance.gl-packaging-layer-specification
- contracts.naming-governance.gl-permission-layer-specification
- contracts.naming-governance.gl-reasoning-layer-specification
- contracts.naming-governance.gl-security-layer-specification
- contracts.naming-governance.gl-supply-chain-layer-specification
- contracts.naming-governance.gl-testing-layer-specification
- contracts.naming-governance.gl-user-facing-layer-specification
- contracts.naming-governance.gl-validation-layer-specification
- contracts.naming-governance.gl-versioning-layer-specification
- ecosystem.governance.docs.architecture.architecture_summary
- ecosystem.governance.docs.architecture.components
- ecosystem.governance.docs.architecture.layers
- ecosystem.governance.docs.architecture.metrics
- enforcers.governance_enforcer
- governance.docs.architecture.architecture_summary
- governance.docs.architecture.components
- governance.docs.architecture.layers
- governance.docs.architecture.metrics
- governance.engines.refresh.__init__
- governance.engines.refresh.refresh_engine
- governance.engines.reverse-architecture.__init__
- governance.engines.reverse-architecture.reverse_architecture_engine
- governance.engines.validation.__init__
- governance.engines.validation.validation_engine
- governance.format-layer.schemas.contract.schema
- governance.format-layer.schemas.evidence.schema
- governance.format-layer.schemas.platform-instance.schema

## reasoning

Components: 15

- contracts.reasoning.dual_path_spec
- reasoning.agents.planning_agent
- reasoning.agents.tools_registry
- reasoning.auto_reasoner
- reasoning.contracts.dual_path_spec
- reasoning.dual_path.arbitration.arbitrator
- reasoning.dual_path.arbitration.rule_engine
- reasoning.dual_path.arbitration.rules.api
- reasoning.dual_path.arbitration.rules.dependency
- reasoning.dual_path.arbitration.rules.security
- reasoning.dual_path.external.retrieval
- reasoning.dual_path.internal.knowledge_graph
- reasoning.dual_path.internal.retrieval
- reasoning.traceability.feedback
- reasoning.traceability.traceability

## gates

Components: 2

- gates.operation-gate
- gates.self-auditor-config

## platform-cloud

Components: 4

- platform-cloud.README
- platform-cloud.dev.deployment
- platform-cloud.dev.environment
- platform-cloud.dev.platform

## ecosystem-cloud

Components: 7

- ecosystem-cloud.adapters.aws.aws_adapter
- ecosystem-cloud.contracts.compute.v1.compute_contract
- ecosystem-cloud.contracts.logging.v1.logging_contract
- ecosystem-cloud.contracts.queue.v1.queue_contract
- ecosystem-cloud.contracts.secrets.v1.secrets_contract
- ecosystem-cloud.contracts.storage.v1.storage_contract
- ecosystem-cloud.registry.cloud_adapters

## contracts

Components: 0


## engines

Components: 0


