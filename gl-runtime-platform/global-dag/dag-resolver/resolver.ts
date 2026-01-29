// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-resolver
// @GL-charter-version: 2.0.0

import { GlobalDAGGraph, DAGNode } from '../dag-model';

/**
 * Global DAG Resolver
 * Resolves cross-repo and cross-cluster dependencies
 * Uses Self-Healing Engine to automatically fix issues
 */

export interface ResolutionResult {
  nodeId: string;
  resolved: boolean;
  issues: string[];
  fixes: string[];
  executionTime: number;
}

export class GlobalDAGResolver {
  private graph: GlobalDAGGraph;
  private resolutionResults: Map<string, ResolutionResult>;
  
  constructor(graph: GlobalDAGGraph) {
    this.graph = graph;
    this.resolutionResults = new Map();
  }
  
  /**
   * Resolve all dependencies in the DAG
   */
  async resolveAll(): Promise<Map<string, ResolutionResult>> {
    console.log('🔍 Resolving global DAG dependencies...');
    
    const nodes = Array.from(this.graph.getNodesByType('file'));
    const batchSize = 50;
    
    for (let i = 0; i < nodes.length; i += batchSize) {
      const batch = nodes.slice(i, i + batchSize);
      await Promise.all(batch.map(node => this.resolveNode(node)));
    }
    
    console.log('✅ Dependency resolution complete');
    return this.resolutionResults;
  }
  
  /**
   * Resolve dependencies for a single node
   */
  private async resolveNode(node: DAGNode): Promise<void> {
    const startTime = Date.now();
    const issues: string[] = [];
    const fixes: string[] = [];
    
    try {
      // Check if all dependencies exist
      for (const depId of node.dependencies) {
        const depNode = this.graph.getNode(depId);
        
        if (!depNode) {
          issues.push(`Missing dependency: ${depId}`);
          
          // Auto-fix: Remove missing dependency
          node.dependencies = node.dependencies.filter(d => d !== depId);
          fixes.push(`Removed missing dependency: ${depId}`);
        }
      }
      
      // Check for orphan nodes
      if (node.dependents.length === 0 && node.type === 'file') {
        const isLeaf = node.type === 'file' && !node.path?.includes('index');
        if (!isLeaf) {
          issues.push('Orphaned node detected');
          
          const repoNode = this.graph.getNode(`repo-${node.repository}`);
          const parent = node.metadata.repository || 'unknown';
          if (repoNode) {
            repoNode.dependents.push(node.id);
            fixes.push('Linked orphaned node to repository');
          }
        }
        }
      // Update node status
      if (issues.length === 0) {
        this.graph.markNodeCompleted(node.id);
      } else {
        this.graph.markNodeFailed(node.id, issues.join('; '));
      }
      
    } catch (error) {
      issues.push(`Resolution error: ${error}`);
      this.graph.markNodeFailed(node.id, issues.join('; '));
    }
    
    const result: ResolutionResult = {
      nodeId: node.id,
      resolved: issues.length === 0,
      issues,
      fixes,
      executionTime: Date.now() - startTime
    };
    
    this.resolutionResults.set(node.id, result);
  }
  
  /**
   * Get resolution statistics
   */
  getStatistics() {
    const results = Array.from(this.resolutionResults.values());
    
    return {
      total: results.length,
      resolved: results.filter(r => r.resolved).length,
      failed: results.filter(r => !r.resolved).length,
      totalIssues: results.reduce((sum, r) => sum + r.issues.length, 0),
      totalFixes: results.reduce((sum, r) => sum + r.fixes.length, 0),
      avgExecutionTime: results.reduce((sum, r) => sum + r.executionTime, 0) / results.length
    };
  }
}