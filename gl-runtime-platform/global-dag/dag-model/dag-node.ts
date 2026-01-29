// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-node-model
// @GL-charter-version: 2.0.0

/**
 * Global DAG Node Model
 * Represents any entity in the global execution graph
 */

export interface DAGNode {
  // Unique identifier for the node
  id: string;
  
  // Node type classification
  type: 'repo' | 'pipeline' | 'agent' | 'file' | 'semantic-unit' | 
        'dependency' | 'cluster' | 'deployment' | 'organization' | 'project';
  
  // Source repository
  repository: string;
  
  // Organization owning this node
  organization: string;
  
  // GL governance layer
  glLayer: string;
  
  // Semantic anchor
  semanticAnchor?: string;
  
  // Path (for file-type nodes)
  path?: string;
  
  // Dependencies (IDs of nodes this node depends on)
  dependencies: string[];
  
  // Dependents (IDs of nodes that depend on this node)
  dependents: string[];
  
  // Execution priority
  priority: number;
  
  // Current status
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  
  // Execution metadata
  metadata: {
    createdAt: string;
    updatedAt: string;
    startedAt?: string;
    completedAt?: string;
    executionDuration?: number;
    retryCount: number;
    lastError?: string;
  };
  
  // Governance compliance
  governance: {
    isCompliant: boolean;
    complianceScore: number;
    violations: string[];
    lastAuditAt: string;
  };
}

export interface DAGEdge {
  // Unique identifier
  id: string;
  
  // Source node ID
  source: string;
  
  // Target node ID
  target: string;
  
  // Edge type
  type: 'dependency' | 'reference' | 'include' | 'import' | 
        'deploy-to' | 'managed-by' | 'part-of';
  
  // Edge strength (weight)
  strength: number;
  
  // Whether this edge is critical
  critical: boolean;
}

export interface DAGGraph {
  // Graph ID
  id: string;
  
  // All nodes
  nodes: Map<string, DAGNode>;
  
  // All edges
  edges: DAGEdge[];
  
  // Graph metadata
  metadata: {
    version: string;
    createdAt: string;
    updatedAt: string;
    totalNodes: number;
    totalEdges: number;
  };
  
  // Execution context
  executionContext: {
    maxConcurrency: number;
    currentExecution: string[];
    completedNodes: Set<string>;
    failedNodes: Set<string>;
  };
}