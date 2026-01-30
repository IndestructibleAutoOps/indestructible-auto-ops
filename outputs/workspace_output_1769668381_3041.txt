// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-executor
// @GL-charter-version: 2.0.0

import { GlobalDAGGraph, DAGNode } from '../dag-model';
import { GlobalDAGResolver } from '../dag-resolver';
import { GlobalDAGRepair } from '../dag-repair';
import { GlobalDAGOptimizer } from '../dag-optimizer';

/**
 * Global DAG Executor
 * Executes the global DAG with parallel execution and self-healing
 */

export interface ExecutionConfig {
  maxConcurrency: number;
  enableSelfHealing: boolean;
  enableOptimization: boolean;
  timeoutMs: number;
}

export interface ExecutionResult {
  nodeId: string;
  status: 'success' | 'failed' | 'skipped';
  executionTime: number;
  retryCount: number;
  error?: string;
}

export class GlobalDAGExecutor {
  private graph: GlobalDAGGraph;
  private resolver: GlobalDAGResolver;
  private repair: GlobalDAGRepair;
  private optimizer: GlobalDAGOptimizer;
  private config: ExecutionConfig;
  private executionResults: Map<string, ExecutionResult>;
  
  constructor(
    graph: GlobalDAGGraph,
    config: Partial<ExecutionConfig> = {}
  ) {
    this.graph = graph;
    this.config = {
      maxConcurrency: config.maxConcurrency || 100,
      enableSelfHealing: config.enableSelfHealing !== false,
      enableOptimization: config.enableOptimization !== false,
      timeoutMs: config.timeoutMs || 300000
    };
    
    this.resolver = new GlobalDAGResolver(graph);
    this.repair = new GlobalDAGRepair(graph);
    this.optimizer = new GlobalDAGOptimizer(graph);
    this.executionResults = new Map();
  }
  
  /**
   * Execute the complete global DAG
   */
  async execute(): Promise<ExecutionResult[]> {
    console.log('🚀 Executing Global DAG...');
    const startTime = Date.now();
    
    // Step 1: Resolve dependencies
    await this.resolver.resolveAll();
    
    // Step 2: Optimize execution path
    if (this.config.enableOptimization) {
      console.log('⚡ Optimizing execution path...');
      await this.optimizer.optimize();
    }
    
    // Step 3: Execute nodes in parallel
    await this.executeGraph();
    
    // Step 4: Generate execution report
    const executionTime = Date.now() - startTime;
    console.log(`✅ Global DAG execution completed in ${executionTime}ms`);
    
    return Array.from(this.executionResults.values());
  }
  
  /**
   * Execute the graph with parallel execution
   */
  private async executeGraph(): Promise<void> {
    let completedCount = 0;
    const totalNodes = this.graph.getNodesByType('file').length;
    
    while (completedCount < totalNodes) {
      const readyNodes = this.graph.getReadyNodes();
      
      if (readyNodes.length === 0) {
        // Check if there are still pending nodes
        const pendingNodes = this.graph.getNodesByType('file').filter(
          n => n.status === 'pending'
        );
        
        if (pendingNodes.length === 0) {
          break; // All done or stuck
        }
        
        console.warn('⚠️  No ready nodes detected, checking for cycles...');
        const cycles = this.graph.detectCycles();
        if (cycles.length > 0) {
          console.warn('⚠️  Cycles detected, applying auto-repair...');
          await this.repair.repairCycles(cycles);
        }
        
        // Force continue with highest priority nodes
        readyNodes.push(...pendingNodes.sort((a, b) => b.priority - a.priority));
      }
      
      // Execute batch of nodes
      const batchSize = Math.min(
        this.config.maxConcurrency,
        readyNodes.length
      );
      
      const batch = readyNodes.slice(0, batchSize);
      await Promise.all(batch.map(node => this.executeNode(node)));
      
      completedCount = this.graph.getNodesByType('file').filter(
        n => n.status === 'completed'
      ).length;
      
      console.log(`📊 Progress: ${completedCount}/${totalNodes} nodes completed`);
    }
  }
  
  /**
   * Execute a single node with self-healing
   */
  private async executeNode(node: DAGNode): Promise<void> {
    const startTime = Date.now();
    let retryCount = 0;
    let status: 'success' | 'failed' | 'skipped' = 'success';
    let error: string | undefined;
    
    const execute = async (): Promise<boolean> => {
      try {
        node.status = 'running';
        node.metadata.startedAt = new Date().toISOString();
        
        // Simulate execution (in real scenario, this would execute the actual pipeline)
        await this.simulateExecution(node);
        
        node.status = 'completed';
        this.graph.markNodeCompleted(node.id);
        return true;
        
      } catch (err) {
        error = String(err);
        retryCount++;
        
        if (this.config.enableSelfHealing && retryCount < 3) {
          console.log(`🔧 Auto-repairing node ${node.id} (attempt ${retryCount})...`);
          const repaired = await this.repair.repairNode(node, error);
          
          if (repaired) {
            return execute(); // Retry after repair
          }
        }
        
        node.status = 'failed';
        this.graph.markNodeFailed(node.id, error);
        return false;
      }
    };
    
    const success = await execute();
    status = success ? 'success' : 'failed';
    
    const result: ExecutionResult = {
      nodeId: node.id,
      status,
      executionTime: Date.now() - startTime,
      retryCount,
      error
    };
    
    this.executionResults.set(node.id, result);
  }
  
  /**
   * Simulate execution for testing
   */
  private async simulateExecution(node: DAGNode): Promise<void> {
    // In production, this would execute actual pipelines
    // For now, simulate with a small delay
    await new Promise(resolve => setTimeout(resolve, Math.random() * 100));
    
    // Simulate occasional failures
    if (Math.random() < 0.05) {
      throw new Error('Simulated execution failure');
    }
  }
  
  /**
   * Get execution statistics
   */
  getStatistics() {
    const results = Array.from(this.executionResults.values());
    
    return {
      total: results.length,
      success: results.filter(r => r.status === 'success').length,
      failed: results.filter(r => r.status === 'failed').length,
      skipped: results.filter(r => r.status === 'skipped').length,
      totalRetries: results.reduce((sum, r) => sum + r.retryCount, 0),
      avgExecutionTime: results.reduce((sum, r) => sum + r.executionTime, 0) / results.length
    };
  }
}