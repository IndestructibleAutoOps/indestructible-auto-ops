// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-graph-model
// @GL-charter-version: 2.0.0

import { DAGNode, DAGEdge, DAGGraph } from './dag-node';

/**
 * Global DAG Graph Model
 * Manages the complete directed acyclic graph
 */

export class GlobalDAGGraph {
  private graph: DAGGraph;
  
  constructor() {
    this.graph = {
      id: 'global-dag-v9',
      nodes: new Map(),
      edges: [],
      metadata: {
        version: '9.0.0',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        totalNodes: 0,
        totalEdges: 0
      },
      executionContext: {
        maxConcurrency: 100,
        currentExecution: [],
        completedNodes: new Set(),
        failedNodes: new Set()
      }
    };
  }
  
  /**
   * Add a node to the graph
   */
  addNode(node: DAGNode): void {
    this.graph.nodes.set(node.id, node);
    this.graph.metadata.totalNodes = this.graph.nodes.size;
    this.graph.metadata.updatedAt = new Date().toISOString();
  }
  
  /**
   * Get a node by ID
   */
  getNode(id: string): DAGNode | undefined {
    return this.graph.nodes.get(id);
  }
  
  /**
   * Add an edge to the graph
   */
  addEdge(edge: DAGEdge): void {
    this.graph.edges.push(edge);
    this.graph.metadata.totalEdges = this.graph.edges.length;
    this.graph.metadata.updatedAt = new Date().toISOString();
    
    // Update node dependencies
    const sourceNode = this.graph.nodes.get(edge.source);
    const targetNode = this.graph.nodes.get(edge.target);
    
    if (sourceNode && !sourceNode.dependents.includes(edge.target)) {
      sourceNode.dependents.push(edge.target);
    }
    
    if (targetNode && !targetNode.dependencies.includes(edge.source)) {
      targetNode.dependencies.push(edge.source);
    }
  }
  
  /**
   * Get all nodes by type
   */
  getNodesByType(type: DAGNode['type']): DAGNode[] {
    return Array.from(this.graph.nodes.values()).filter(node => node.type === type);
  }
  
  /**
   * Get all nodes by repository
   */
  getNodesByRepository(repository: string): DAGNode[] {
    return Array.from(this.graph.nodes.values()).filter(
      node => node.repository === repository
    );
  }
  
  /**
   * Get all nodes by organization
   */
  getNodesByOrganization(organization: string): DAGNode[] {
    return Array.from(this.graph.nodes.values()).filter(
      node => node.organization === organization
    );
  }
  
  /**
   * Get all nodes by GL layer
   */
  getNodesByGLLayer(glLayer: string): DAGNode[] {
    return Array.from(this.graph.nodes.values()).filter(
      node => node.glLayer === glLayer
    );
  }
  
  /**
   * Get nodes ready for execution (no pending dependencies)
   */
  getReadyNodes(): DAGNode[] {
    return Array.from(this.graph.nodes.values()).filter(node => {
      if (node.status !== 'pending') return false;
      
      // Check if all dependencies are completed
      return node.dependencies.every(depId => 
        this.graph.executionContext.completedNodes.has(depId)
      );
    }).sort((a, b) => b.priority - a.priority);
  }
  
  /**
   * Mark node as completed
   */
  markNodeCompleted(nodeId: string): void {
    const node = this.graph.nodes.get(nodeId);
    if (node) {
      node.status = 'completed';
      node.metadata.completedAt = new Date().toISOString();
      node.metadata.executionDuration = node.metadata.startedAt 
        ? Date.now() - new Date(node.metadata.startedAt).getTime()
        : 0;
      this.graph.executionContext.completedNodes.add(nodeId);
      this.graph.executionContext.currentExecution = 
        this.graph.executionContext.currentExecution.filter(id => id !== nodeId);
      this.graph.metadata.updatedAt = new Date().toISOString();
    }
  }
  
  /**
   * Mark node as failed
   */
  markNodeFailed(nodeId: string, error: string): void {
    const node = this.graph.nodes.get(nodeId);
    if (node) {
      node.status = 'failed';
      node.metadata.lastError = error;
      this.graph.executionContext.failedNodes.add(nodeId);
      this.graph.executionContext.currentExecution = 
        this.graph.executionContext.currentExecution.filter(id => id !== nodeId);
      this.graph.metadata.updatedAt = new Date().toISOString();
    }
  }
  
  /**
   * Check for circular dependencies
   */
  detectCycles(): string[][] {
    const visited = new Set<string>();
    const recursionStack = new Set<string>();
    const cycles: string[][] = [];
    
    const detect = (nodeId: string, path: string[]): void => {
      const node = this.graph.nodes.get(nodeId);
      if (!node) return;
      
      visited.add(nodeId);
      recursionStack.add(nodeId);
      
      for (const depId of node.dependencies) {
        if (!visited.has(depId)) {
          detect(depId, [...path, nodeId]);
        } else if (recursionStack.has(depId)) {
          const cycleStart = path.indexOf(depId);
          if (cycleStart !== -1) {
            cycles.push([...path.slice(cycleStart), nodeId]);
          }
        }
      }
      
      recursionStack.delete(nodeId);
    };
    
    for (const nodeId of this.graph.nodes.keys()) {
      if (!visited.has(nodeId)) {
        detect(nodeId, []);
      }
    }
    
    return cycles;
  }
  
  /**
   * Get graph statistics
   */
  getStatistics() {
    const nodesByType = Array.from(this.graph.nodes.values()).reduce((acc, node) => {
      acc[node.type] = (acc[node.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    const nodesByOrg = Array.from(this.graph.nodes.values()).reduce((acc, node) => {
      acc[node.organization] = (acc[node.organization] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    const complianceScores = Array.from(this.graph.nodes.values())
      .map(node => node.governance.complianceScore);
    
    const avgCompliance = complianceScores.length > 0
      ? complianceScores.reduce((a, b) => a + b, 0) / complianceScores.length
      : 0;
    
    return {
      totalNodes: this.graph.nodes.size,
      totalEdges: this.graph.edges.length,
      nodesByType,
      nodesByOrg,
      avgCompliance,
      completedNodes: this.graph.executionContext.completedNodes.size,
      failedNodes: this.graph.executionContext.failedNodes.size,
      currentlyExecuting: this.graph.executionContext.currentExecution.length
    };
  }
  
  /**
   * Export graph to JSON
   */
  toJSON(): any {
    return {
      id: this.graph.id,
      nodes: Array.from(this.graph.nodes.entries()),
      edges: this.graph.edges,
      metadata: this.graph.metadata,
      statistics: this.getStatistics()
    };
  }
}