// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-main-orchestrator
// @GL-charter-version: 2.0.0

import { GlobalDAGGraph } from './dag-model';
import { GlobalDAGBuilder, DAGBuilderConfig } from './dag-builder';
import { GlobalDAGExecutor, ExecutionConfig } from './dag-executor';
import { GlobalDAGResolver } from './dag-resolver';
import { GlobalDAGRepair } from './dag-repair';
import { GlobalDAGOptimizer } from './dag-optimizer';
import { GlobalDAGVisualizer } from './dag-visualizer';

/**
 * Global DAG Orchestrator
 * Main entry point for Global DAG-based Multi-Repo Execution
 */

export interface GlobalDAGConfig {
  repositories: Array<{
    id: string;
    organization: string;
    path: string;
    glLayer: string;
  }>;
  pipelines: Array<{
    id: string;
    repository: string;
    organization: string;
    dependencies?: string[];
  }>;
  agents: Array<{
    id: string;
    repository: string;
    organization: string;
    priority: number;
  }>;
  clusters: Array<{
    id: string;
    region: string;
  }>;
  execution: Partial<ExecutionConfig>;
}

export class GlobalDAGOrchestrator {
  private graph: GlobalDAGGraph;
  private builder: GlobalDAGBuilder;
  private executor: GlobalDAGExecutor;
  private resolver: GlobalDAGResolver;
  private repair: GlobalDAGRepair;
  private optimizer: GlobalDAGOptimizer;
  private visualizer: GlobalDAGVisualizer;
  private config: GlobalDAGConfig;
  
  constructor(config: GlobalDAGConfig) {
    this.config = config;
    
    const builderConfig: DAGBuilderConfig = {
      repositories: config.repositories,
      pipelines: config.pipelines,
      agents: config.agents,
      clusters: config.clusters
    };
    
    this.graph = new GlobalDAGGraph();
    this.builder = new GlobalDAGBuilder(builderConfig);
    this.executor = new GlobalDAGExecutor(this.graph, config.execution);
    this.resolver = new GlobalDAGResolver(this.graph);
    this.repair = new GlobalDAGRepair(this.graph);
    this.optimizer = new GlobalDAGOptimizer(this.graph);
    this.visualizer = new GlobalDAGVisualizer(this.graph);
  }
  
  /**
   * Execute complete Global DAG workflow
   */
  async execute(): Promise<{
    graph: GlobalDAGGraph;
    executionResults: any[];
    statistics: any;
    visualization: any;
  }> {
    console.log('🌐 Starting Global DAG-Based Multi-Repo Execution...');
    
    // Phase 1: Build the DAG
    console.log('\n=== Phase 1: Building Global DAG ===');
    await this.builder.build();
    
    // Phase 2: Resolve dependencies
    console.log('\n=== Phase 2: Resolving Dependencies ===');
    await this.resolver.resolveAll();
    
    // Phase 3: Optimize execution
    console.log('\n=== Phase 3: Optimizing Execution ===');
    await this.optimizer.optimize();
    
    // Phase 4: Execute DAG
    console.log('\n=== Phase 4: Executing DAG ===');
    const executionResults = await this.executor.execute();
    
    // Phase 5: Generate visualization
    console.log('\n=== Phase 5: Generating Visualization ===');
    const visualization = await this.visualizer.generateVisualization();
    
    // Phase 6: Generate statistics
    const statistics = {
      graph: this.graph.getStatistics(),
      resolver: this.resolver.getStatistics(),
      executor: this.executor.getStatistics(),
      repair: this.repair.getStatistics(),
      optimizer: await this.optimizer.optimize()
    };
    
    console.log('\n✅ Global DAG execution complete!');
    console.log('\n=== Execution Statistics ===');
    console.log(JSON.stringify(statistics, null, 2));
    
    return {
      graph: this.graph,
      executionResults,
      statistics,
      visualization
    };
  }
  
  /**
   * Get the current graph
   */
  getGraph(): GlobalDAGGraph {
    return this.graph;
  }
  
  /**
   * Get the executor
   */
  getExecutor(): GlobalDAGExecutor {
    return this.executor;
  }
  
  /**
   * Get the visualizer
   */
  getVisualizer(): GlobalDAGVisualizer {
    return this.visualizer;
  }
}

// Export all modules
export { GlobalDAGGraph } from './dag-model';
export { GlobalDAGBuilder, DAGBuilderConfig } from './dag-builder';
export { GlobalDAGExecutor, ExecutionConfig } from './dag-executor';
export { GlobalDAGResolver } from './dag-resolver';
export { GlobalDAGRepair } from './dag-repair';
export { GlobalDAGOptimizer } from './dag-optimizer';
export { GlobalDAGVisualizer } from './dag-visualizer';