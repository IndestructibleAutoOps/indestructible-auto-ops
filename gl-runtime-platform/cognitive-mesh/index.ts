/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Cognitive Mesh - Main Export
 * @GL-layer: GL11
 * @GL-semantic: cognitive-mesh
 * @GL-audit-trail: ../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Version 11: Global Cognitive Mesh
 * Transforms the GL Runtime from autonomous swarm to shared cognitive network
 */

export { MeshCore, MeshConfig, MeshState } from './mesh-core';
export { MeshMemory, MemoryEntry, MemoryQuery } from './mesh-memory';
export { MeshNodes, CognitiveNode, NodeCapability } from './mesh-nodes';
export { MeshRouting, RoutingDecision, RoutingRequest, RoutingConfig } from './mesh-routing';
export { MeshSynchronization, SyncState, SyncStatus } from './mesh-synchronization';
export { MeshOptimizer, OptimizationMetrics, OptimizationAction } from './mesh-optimizer';
export { MeshEmergence, EmergencePattern, EmergenceMetrics } from './mesh-emergence';