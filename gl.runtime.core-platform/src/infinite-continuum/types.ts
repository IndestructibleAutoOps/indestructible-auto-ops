// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Type Definitions
 * Version 20.0.0
 */

import { FabricNode, FabricEdge, FabricGraph } from '../../unified-intelligence-fabric/fabric-core';

// ============================================================================
// Knowledge Accretion Types
// ============================================================================

export interface KnowledgeNode {
  id: string;
  content: any;
  type: 'fact' | 'concept' | 'relation' | 'pattern' | 'insight';
  confidence: number;
  source: string;
  timestamp: number;
  accessCount: number;
  reinforcement: number;
}

export interface KnowledgeEdge {
  id: string;
  sourceId: string;
  targetId: string;
  type: 'causal' | 'temporal' | 'semantic' | 'structural';
  strength: number;
  timestamp: number;
  accessCount: number;
}

export interface KnowledgeGraph {
  nodes: Map<string, KnowledgeNode>;
  edges: Map<string, KnowledgeEdge>;
  metrics: KnowledgeMetrics;
}

export interface KnowledgeMetrics {
  totalNodes: number;
  totalEdges: number;
  averageConfidence: number;
  connectivity: number;
  coherenceScore: number;
  growthRate: number;
}

// ============================================================================
// Semantic Reformation Types
// ============================================================================

export interface SemanticCluster {
  id: string;
  nodeIds: string[];
  centroid: number[];
  semanticCoherence: number;
  stability: number;
  lastReformation: number;
}

export interface ConceptBoundary {
  conceptId: string;
  boundary: number[];
  flexibility: number;
  adaptationRate: number;
}

export interface SemanticReformationEvent {
  id: string;
  type: 'cluster_split' | 'cluster_merge' | 'boundary_shift' | 'concept_emergence';
  timestamp: number;
  affectedNodes: string[];
  impact: number;
}

// ============================================================================
// Algorithmic Evolution Types
// ============================================================================

export interface AlgorithmGenome {
  id: string;
  algorithmType: string;
  parameters: Map<string, any>;
  performance: AlgorithmPerformance;
  lineage: string[];
  generation: number;
}

export interface AlgorithmPerformance {
  accuracy: number;
  efficiency: number;
  adaptability: number;
  generalization: number;
  lastUpdated: number;
}

export interface EvolutionEvent {
  id: string;
  type: 'mutation' | 'crossover' | 'selection' | 'extinction';
  timestamp: number;
  parentId: string;
  childId: string;
  fitnessDelta: number;
}

// ============================================================================
// Infinite Composition Types
// ============================================================================

export interface CompositionTemplate {
  id: string;
  structure: CompositionNode[];
  constraints: CompositionConstraints;
  performance: CompositionPerformance;
  usage: number;
}

export interface CompositionNode {
  id: string;
  type: 'algorithm' | 'data' | 'control' | 'transformation';
  config: any;
  dependencies: string[];
}

export interface CompositionConstraints {
  maxComplexity: number;
  allowedTypes: string[];
  resourceLimits: ResourceLimits;
}

export interface ResourceLimits {
  maxMemory: number;
  maxCpu: number;
  maxTime: number;
}

export interface CompositionPerformance {
  quality: number;
  efficiency: number;
  reliability: number;
  lastExecuted: number;
}

// ============================================================================
// Fabric Expansion Types
// ============================================================================

export interface ExpansionPolicy {
  trigger: 'usage' | 'demand' | 'prediction' | 'manual';
  threshold: number;
  strategy: 'incremental' | 'exponential' | 'adaptive';
  constraints: ExpansionConstraints;
}

export interface ExpansionConstraints {
  maxNodes: number;
  maxEdges: number;
  maxMemory: number;
  growthRate: number;
}

export interface ExpansionEvent {
  id: string;
  type: 'node_addition' | 'edge_addition' | 'subgraph_creation';
  timestamp: number;
  impact: number;
  justification: string;
}

// ============================================================================
// Continuum Memory Types
// ============================================================================

export interface TemporalMemoryNode {
  id: string;
  data: any;
  timestamp: number;
  temporalContext: TemporalContext;
  retrievalCount: number;
}

export interface TemporalContext {
  timeWindow: [number, number];
  relatedEvents: string[];
  semanticTags: string[];
}

export interface MemoryIndex {
  timeIndex: Map<number, string[]>;
  semanticIndex: Map<string, string[]>;
  eventIndex: Map<string, string[]>;
}

export interface MemoryCompression {
  originalSize: number;
  compressedSize: number;
  compressionRatio: number;
  lastCompression: number;
}

// ============================================================================
// Configuration Types
// ============================================================================

export interface InfiniteContinuumConfig {
  knowledgeAccretion: {
    interval: number;
    maxNodes: number;
    confidenceThreshold: number;
  };
  semanticReformation: {
    interval: number;
    coherenceThreshold: number;
    adaptationRate: number;
  };
  algorithmicEvolution: {
    interval: number;
    populationSize: number;
    mutationRate: number;
    elitismRate: number;
  };
  infiniteComposition: {
    maxCompositions: number;
    searchDepth: number;
    diversityThreshold: number;
  };
  fabricExpansion: {
    interval: number;
    maxNodes: number;
    growthRate: number;
    strategy: 'incremental' | 'exponential' | 'adaptive';
  };
  continuumMemory: {
    retentionPeriod: number;
    compressionInterval: number;
    maxMemorySize: number;
  };
}

export interface ContinuumMetrics {
  knowledgeSize: number;
  semanticCoherence: number;
  algorithmFitness: number;
  compositionDiversity: number;
  fabricUtilization: number;
  memoryEfficiency: number;
  evolutionRate: number;
}