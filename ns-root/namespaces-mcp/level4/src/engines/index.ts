// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/engines
 * @gl-semantic-anchor GL-00-SRC_ENGINES_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4 - Engines Index
 * 
 * Central export point for all Level 4 engines
 */

// Phase 2: Core Engines
export { ObservationEngine } from './observation-engine';
export { EvolutionEngine } from './evolution-engine';
export { ReflexEngine } from './reflex-engine';
export { AuditEngine } from './audit-engine';

// Phase 3: Advanced Engines
export { PromotionEngine } from './promotion-engine';
export { VersioningEngine } from './versioning-engine';
export { CompressionEngine } from './compression-engine';
export { MigrationEngine } from './migration-engine';
export { EncapsulationEngine } from './encapsulation-engine';
export { ReplicationEngine } from './replication-engine';
export { ClosureEngine } from './closure-engine';
export { GovernanceEngine } from './governance-engine';