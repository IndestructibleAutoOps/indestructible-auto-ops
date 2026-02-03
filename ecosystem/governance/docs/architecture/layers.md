# Architecture Layers

Generated: 2026-02-03T15:13:41.663509Z

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

Components: 97

- contracts.fact-verification.gl.internal-vs-external-governance
- contracts.governance.ROLE_LANGUAGE_SPECIFICATION
- contracts.governance.ROLE_RUNTIME_FLOW
- contracts.governance.ROLE_SYSTEM_IMPLEMENTATION_COMPLETE
- contracts.governance.gl-governance-layers
- contracts.governance.gl-semantic-violation-classifier
- contracts.governance.gl.causal-reasoning-spec
- contracts.governance.gl.cognitive-modes-spec
- contracts.governance.gl.evolution-metrics
- contracts.governance.gl.execution.finalization-spec
- contracts.governance.gqs-layers
- contracts.governance.role.schema
- contracts.governance.roles.ecosystem.analyst
- contracts.governance.roles.ecosystem.architect
- contracts.governance.roles.ecosystem.runner
- contracts.governance.roles.ecosystem.semantic-checker
- contracts.governance.roles.ecosystem.validator
- contracts.governance.roles.registry
- contracts.governance.templates.gl.execution.analysis-report
- contracts.governance.templates.gl.execution.delta-report
- contracts.governance.templates.gl.flow.upgrade-log
- contracts.naming-governance.gl-build-layer-specification
- contracts.naming-governance.gl-ci-cd-layer-specification
- contracts.naming-governance.gl-contract-layer-specification
- contracts.naming-governance.gl-dependency-layer-specification
- contracts.naming-governance.gl-deployment-layer-specification
- contracts.naming-governance.gl-documentation-layer-specification
- contracts.naming-governance.gl-extensibility-layer-specification
- contracts.naming-governance.gl-format-layer-specification
- contracts.naming-governance.gl-generator-layer-specification
- contracts.naming-governance.gl-governance-layer-specification
- contracts.naming-governance.gl-indexing-layer-specification
- contracts.naming-governance.gl-interface-layer-specification
- contracts.naming-governance.gl-language-layer-specification
- contracts.naming-governance.gl-metadata-layer-specification
- contracts.naming-governance.gl-naming-ontology
- contracts.naming-governance.gl-naming-ontology-expanded
- contracts.naming-governance.gl-observability-layer-specification
- contracts.naming-governance.gl-packaging-layer-specification
- contracts.naming-governance.gl-permission-layer-specification
- contracts.naming-governance.gl-platform-layer-specification
- contracts.naming-governance.gl-prefix-principles-engineering
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
- enforcers.closed_loop_governance
- enforcers.governance_enforcer
- governance.GL_SEMANTIC_ANCHOR
- governance.audit_logger
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
- governance.governance-manifest
- governance.governance-monitor-config
- governance.meta-governance.DRIFT_ANALYSIS_REPORT
- governance.meta-governance.FULL_INTEGRATION_REPORT
- governance.meta-governance.META_GOVERNANCE_APPLICATION_REPORT
- governance.meta-governance.README
- governance.meta-governance.configs.governance-config
- governance.meta-governance.schemas.version-specification
- governance.meta-governance.src.__init__
- governance.meta-governance.src.change_control_system
- governance.meta-governance.src.change_manager
- governance.meta-governance.src.dependency_manager
- governance.meta-governance.src.governance_framework
- governance.meta-governance.src.impact_analyzer
- governance.meta-governance.src.review_manager
- governance.meta-governance.src.sha_integrity_system
- governance.meta-governance.src.strict_version_enforcer
- governance.meta-governance.src.version_manager
- governance.meta-governance.tests.test_change_control
- governance.meta-governance.tests.test_meta_governance
- governance.meta-governance.tests.test_sha_integrity
- governance.meta-governance.tests.test_strict_version_management
- governance.meta-governance.tools.apply_governance
- governance.meta-governance.tools.apply_strict_versioning
- governance.meta-governance.tools.full_governance_integration
- tools.generate-governance-dashboard
- tools.gl-markers.fix-governance-markers

## reasoning

Components: 16

- contracts.reasoning.dual_path_spec
- contracts.reasoning.gl-reasoning-rules
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

Components: 16

- contracts.extensions.gl-extension-points
- contracts.fact-verification.README
- contracts.fact-verification.gl.fact-pipeline-spec
- contracts.fact-verification.gl.verifiable-report-spec
- contracts.generator.gl-generator-spec
- contracts.platforms.gl-platforms
- contracts.policies.conftest
- contracts.validation.gl-validation-rules
- contracts.verification.gl-audit-report-template
- contracts.verification.gl-proof-model
- contracts.verification.gl-proof-model-executable
- contracts.verification.gl-verifiable-report-standard
- contracts.verification.gl-verifiable-report-standard-executable
- contracts.verification.gl-verification-engine-spec
- contracts.verification.gl-verification-engine-spec-executable
- registry.naming.gl-naming-contracts-registry

## engines

Components: 0


