// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-algo
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - Fabric Algo
 * Version 19.0.0
 * 
 * 核心：演算法視角
 * - 織網上的「轉換規則集」
 * - 演算法在織網上流動與應用
 * - 動態演算法選擇與優化
 * - 演算法演化與自適應
 */

import { FabricCore, FabricNode, FabricEdge } from '../fabric-core';

// ============================================================================
// Type Definitions
// ============================================================================

export interface Algorithm {
  id: string;
  name: string;
  type: AlgorithmType;
  category: AlgorithmCategory;
  description: string;
  implementation: AlgorithmImplementation;
  parameters: AlgorithmParameter[];
  constraints: AlgorithmConstraints;
  performance: AlgorithmPerformance;
  version: string;
}

export type AlgorithmType = 
  | 'transformation'  // 轉換演算法
  | 'inference'       // 推理演算法
  | 'optimization'    // 優化演算法
  | 'search'          // 搜尋演算法
  | 'pattern_match'   // 模式匹配演算法
  | 'reasoning'       // 推理演算法
  | 'learning'        // 學習演算法
  | 'evolution';      // 演化演算法

export type AlgorithmCategory = 
  | 'graph'           // 圖演算法
  | 'semantic'        // 語意演算法
  | 'statistical'     // 統計演算法
  | 'neural'          // 神經網路演算法
  | 'symbolic'        // 符號演算法
  | 'probabilistic';  // 概率演算法

export interface AlgorithmImplementation {
  type: 'function' | 'flow' | 'pipeline' | 'composite';
  definition: any;
  dependencies: string[];
  computeRequirements: {
    cpuCores: number;
    memory: number;
    estimatedDuration: number;
  };
}

export interface AlgorithmParameter {
  name: string;
  type: 'number' | 'string' | 'boolean' | 'array' | 'object';
  default: any;
  range?: [number, number];
  description: string;
  required: boolean;
}

export interface AlgorithmConstraints {
  minInputSize?: number;
  maxInputSize?: number;
  supportedNodeTypes?: string[];
  supportedEdgeTypes?: string[];
  requiresSuperposition?: boolean;
}

export interface AlgorithmPerformance {
  averageRuntime: number;
  successRate: number;
  accuracy: number;
  resourceUsage: {
    cpu: number;
    memory: number;
  };
  lastExecuted: number;
}

export interface AlgorithmExecution {
  id: string;
  algorithmId: string;
  input: any;
  parameters: Record<string, any>;
  startTime: number;
  endTime?: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: Error;
  performance: {
    runtime: number;
    resourceUsage: {
      cpu: number;
      memory: number;
    };
  };
}

export interface AlgoConfig {
  enableAutoSelection: boolean;
  enableAutoTuning: boolean;
  enableCaching: boolean;
  maxConcurrentExecutions: number;
}

// ============================================================================
// Fabric Algo Class
// ============================================================================

export class FabricAlgo {
  private fabric: FabricCore;
  private config: AlgoConfig;
  private algorithms: Map<string, Algorithm>;
  private executions: Map<string, AlgorithmExecution>;
  private algorithmRegistry: AlgorithmRegistry;
  private executionEngine: AlgorithmExecutionEngine;
  private performanceTracker: PerformanceTracker;
  private initialized: boolean;
  
  constructor(fabric: FabricCore, config?: Partial<AlgoConfig>) {
    this.fabric = fabric;
    this.config = {
      enableAutoSelection: config?.enableAutoSelection ?? true,
      enableAutoTuning: config?.enableAutoTuning ?? true,
      enableCaching: config?.enableCaching ?? true,
      maxConcurrentExecutions: config?.maxConcurrentExecutions || 10
    };
    
    this.algorithms = new Map();
    this.executions = new Map();
    this.algorithmRegistry = new AlgorithmRegistry(this);
    this.executionEngine = new AlgorithmExecutionEngine(this);
    this.performanceTracker = new PerformanceTracker(this);
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Fabric Algo] Initializing algorithm layer...');
    
    // 註冊預設演算法
    await this.registerDefaultAlgorithms();
    
    // 初始化執行引擎
    await this.executionEngine.initialize();
    
    // 初始化性能追蹤器
    await this.performanceTracker.initialize();
    
    this.initialized = true;
    console.log('[Fabric Algo] Algorithm layer initialized');
  }
  
  // ========================================================================
  // Algorithm Registration
  // ========================================================================
  
  async registerAlgorithm(algorithm: Algorithm): Promise<void> {
    console.log(`[Fabric Algo] Registering algorithm ${algorithm.name} (${algorithm.id})`);
    
    // 驗證演算法
    await this.validateAlgorithm(algorithm);
    
    // 註冊演算法
    this.algorithms.set(algorithm.id, algorithm);
    
    // 更新註冊表
    await this.algorithmRegistry.register(algorithm);
  }
  
  async unregisterAlgorithm(algorithmId: string): Promise<void> {
    console.log(`[Fabric Algo] Unregistering algorithm ${algorithmId}`);
    
    this.algorithms.delete(algorithmId);
    await this.algorithmRegistry.unregister(algorithmId);
  }
  
  async getAlgorithm(algorithmId: string): Promise<Algorithm | undefined> {
    return this.algorithms.get(algorithmId);
  }
  
  async getAllAlgorithms(): Promise<Algorithm[]> {
    return Array.from(this.algorithms.values());
  }
  
  async queryAlgorithms(filter: {
    type?: AlgorithmType;
    category?: AlgorithmCategory;
    nodeType?: string;
    edgeType?: string;
  }): Promise<Algorithm[]> {
    let results = Array.from(this.algorithms.values());
    
    if (filter.type) {
      results = results.filter(a => a.type === filter.type);
    }
    
    if (filter.category) {
      results = results.filter(a => a.category === filter.category);
    }
    
    if (filter.nodeType && filter.nodeType !== 'all') {
      results = results.filter(a => 
        a.constraints.supportedNodeTypes?.includes(filter.nodeType!)
      );
    }
    
    if (filter.edgeType && filter.edgeType !== 'all') {
      results = results.filter(a => 
        a.constraints.supportedEdgeTypes?.includes(filter.edgeType!)
      );
    }
    
    return results;
  }
  
  private async validateAlgorithm(algorithm: Algorithm): Promise<void> {
    // 驗證必需欄位
    if (!algorithm.id || !algorithm.name || !algorithm.type || !algorithm.implementation) {
      throw new Error('Invalid algorithm: missing required fields');
    }
    
    // 驗證實作
    if (!algorithm.implementation.definition) {
      throw new Error('Invalid algorithm: missing implementation definition');
    }
  }
  
  // ========================================================================
  // Algorithm Execution
  // ========================================================================
  
  async executeAlgorithm(
    algorithmId: string,
    input: any,
    parameters?: Record<string, any>
  ): Promise<AlgorithmExecution> {
    console.log(`[Fabric Algo] Executing algorithm ${algorithmId}`);
    
    const algorithm = this.algorithms.get(algorithmId);
    
    if (!algorithm) {
      throw new Error(`Algorithm ${algorithmId} not found`);
    }
    
    // 創建執行記錄
    const execution: AlgorithmExecution = {
      id: `exec-${algorithmId}-${Date.now()}`,
      algorithmId,
      input,
      parameters: parameters || {},
      startTime: Date.now(),
      status: 'pending',
      performance: {
        runtime: 0,
        resourceUsage: { cpu: 0, memory: 0 }
      }
    };
    
    this.executions.set(execution.id, execution);
    
    // 執行演算法
    execution.status = 'running';
    
    try {
      const startTime = Date.now();
      
      // 執行演算法實作
      const result = await this.executionEngine.execute(algorithm, input, parameters || {});
      
      execution.endTime = Date.now();
      execution.status = 'completed';
      execution.result = result;
      execution.performance.runtime = execution.endTime - startTime;
      
      // 更新性能追蹤
      await this.performanceTracker.trackExecution(algorithmId, execution);
      
      // 更新演算法性能統計
      algorithm.performance.averageRuntime = 
        (algorithm.performance.averageRuntime + execution.performance.runtime) / 2;
      algorithm.performance.lastExecuted = Date.now();
      
    } catch (error) {
      execution.endTime = Date.now();
      execution.status = 'failed';
      execution.error = error as Error;
      
      // 更新失敗率
      algorithm.performance.successRate = 
        (algorithm.performance.successRate * 9) / 10; // 降低成功率
    }
    
    console.log(`[Fabric Algo] Algorithm ${algorithmId} execution completed with status ${execution.status}`);
    return execution;
  }
  
  async getExecution(executionId: string): Promise<AlgorithmExecution | undefined> {
    return this.executions.get(executionId);
  }
  
  async getExecutions(filter?: {
    algorithmId?: string;
    status?: string;
    since?: number;
  }): Promise<AlgorithmExecution[]> {
    let results = Array.from(this.executions.values());
    
    if (filter?.algorithmId) {
      results = results.filter(e => e.algorithmId === filter.algorithmId);
    }
    
    if (filter?.status) {
      results = results.filter(e => e.status === filter.status);
    }
    
    if (filter?.since) {
      results = results.filter(e => e.startTime >= filter.since!);
    }
    
    return results;
  }
  
  // ========================================================================
  // Auto-Selection and Auto-Tuning
  // ========================================================================
  
  async selectBestAlgorithm(
    input: any,
    requirements: {
      type?: AlgorithmType;
      category?: AlgorithmCategory;
      priority?: 'speed' | 'accuracy' | 'resource_efficiency';
    }
  ): Promise<Algorithm | undefined> {
    if (!this.config.enableAutoSelection) {
      return undefined;
    }
    
    console.log('[Fabric Algo] Auto-selecting best algorithm...');
    
    // 查詢候選演算法
    const candidates = await this.queryAlgorithms({
      type: requirements.type,
      category: requirements.category
    });
    
    if (candidates.length === 0) {
      return undefined;
    }
    
    // 根據優先級評分
    const priority = requirements.priority || 'accuracy';
    
    const scored = candidates.map(algo => ({
      algorithm: algo,
      score: this.calculateScore(algo, priority)
    }));
    
    // 選擇最高分
    scored.sort((a, b) => b.score - a.score);
    
    return scored[0]?.algorithm;
  }
  
  private calculateScore(algorithm: Algorithm, priority: string): number {
    let score = 0;
    
    switch (priority) {
      case 'speed':
        // 優先選擇執行時間短
        score += (1 / (algorithm.performance.averageRuntime + 1)) * 0.5;
        score += algorithm.performance.successRate * 0.3;
        score += algorithm.performance.resourceUsage.cpu * -0.1;
        score += algorithm.performance.resourceUsage.memory * -0.1;
        break;
        
      case 'accuracy':
        // 優先選擇準確度高
        score += algorithm.performance.accuracy * 0.5;
        score += algorithm.performance.successRate * 0.3;
        score += (1 / (algorithm.performance.averageRuntime + 1)) * 0.1;
        score += algorithm.performance.resourceUsage.cpu * -0.05;
        break;
        
      case 'resource_efficiency':
        // 優先選擇資源使用少
        score += (1 - algorithm.performance.resourceUsage.cpu) * 0.4;
        score += (1 - algorithm.performance.resourceUsage.memory) * 0.4;
        score += algorithm.performance.successRate * 0.1;
        score += (1 / (algorithm.performance.averageRuntime + 1)) * 0.1;
        break;
    }
    
    return score;
  }
  
  async tuneAlgorithm(algorithmId: string): Promise<void> {
    if (!this.config.enableAutoTuning) {
      return;
    }
    
    console.log(`[Fabric Algo] Auto-tuning algorithm ${algorithmId}`);
    
    const algorithm = this.algorithms.get(algorithmId);
    if (!algorithm) {
      throw new Error(`Algorithm ${algorithmId} not found`);
    }
    
    // 獲取歷史執行數據
    const executions = await this.getExecutions({ algorithmId });
    
    if (executions.length < 5) {
      console.log(`[Fabric Algo] Not enough execution data for tuning`);
      return;
    }
    
    // 簡化實作：調整參數
    for (const param of algorithm.parameters) {
      if (param.type === 'number' && param.range) {
        // 基於歷史表現調整參數
        const avgRuntime = executions.reduce((sum, e) => sum + e.performance.runtime, 0) / executions.length;
        
        if (avgRuntime > algorithm.performance.averageRuntime * 1.5) {
          // 執行慢，降低參數值
          param.default = Math.max(param.range[0], param.default * 0.9);
        } else if (avgRuntime < algorithm.performance.averageRuntime * 0.8) {
          // 執行快，提高參數值
          param.default = Math.min(param.range[1], param.default * 1.1);
        }
      }
    }
    
    console.log(`[Fabric Algo] Algorithm ${algorithmId} tuned`);
  }
  
  // ========================================================================
  // Statistics
  // ========================================================================
  
  async getStatistics(): Promise<AlgoStatistics> {
    const algorithms = Array.from(this.algorithms.values());
    const executions = Array.from(this.executions.values());
    
    return {
      totalAlgorithms: algorithms.length,
      totalExecutions: executions.length,
      successfulExecutions: executions.filter(e => e.status === 'completed').length,
      failedExecutions: executions.filter(e => e.status === 'failed').length,
      averageExecutionTime: executions.reduce((sum, e) => sum + e.performance.runtime, 0) / executions.length || 0,
      algorithmTypes: this.groupByType(algorithms)
    };
  }
  
  private groupByType(algorithms: Algorithm[]): Record<AlgorithmType, number> {
    const counts = {} as Record<AlgorithmType, number>;
    
    for (const algo of algorithms) {
      counts[algo.type] = (counts[algo.type] || 0) + 1;
    }
    
    return counts;
  }
  
  private async registerDefaultAlgorithms(): Promise<void> {
    // 註冊預設演算法
    
    // 1. 節點轉換演算法
    await this.registerAlgorithm({
      id: 'algo-node-transform',
      name: 'Node Transformation',
      type: 'transformation',
      category: 'graph',
      description: 'Transform node properties',
      implementation: {
        type: 'function',
        definition: async (node: FabricNode, params: any) => {
          return {
            ...node,
            properties: { ...node.properties, ...params }
          };
        },
        dependencies: [],
        computeRequirements: { cpuCores: 1, memory: 128, estimatedDuration: 100 }
      },
      parameters: [
        {
          name: 'transform',
          type: 'object',
          default: {},
          description: 'Transformations to apply',
          required: false
        }
      ],
      constraints: {},
      performance: {
        averageRuntime: 100,
        successRate: 0.95,
        accuracy: 0.9,
        resourceUsage: { cpu: 0.1, memory: 0.05 },
        lastExecuted: 0
      },
      version: '1.0.0'
    });
    
    // 2. 路徑搜尋演算法
    await this.registerAlgorithm({
      id: 'algo-path-search',
      name: 'Path Search',
      type: 'search',
      category: 'graph',
      description: 'Search for paths between nodes',
      implementation: {
        type: 'function',
        definition: async (source: string, target: string, params: any) => {
          return { path: [source, target], distance: 1 };
        },
        dependencies: [],
        computeRequirements: { cpuCores: 2, memory: 256, estimatedDuration: 500 }
      },
      parameters: [
        {
          name: 'maxDepth',
          type: 'number',
          default: 10,
          range: [1, 100],
          description: 'Maximum search depth',
          required: false
        }
      ],
      constraints: {},
      performance: {
        averageRuntime: 500,
        successRate: 0.9,
        accuracy: 0.85,
        resourceUsage: { cpu: 0.2, memory: 0.1 },
        lastExecuted: 0
      },
      version: '1.0.0'
    });
    
    // 3. 模式匹配演算法
    await this.registerAlgorithm({
      id: 'algo-pattern-match',
      name: 'Pattern Matching',
      type: 'pattern_match',
      category: 'graph',
      description: 'Match patterns in the graph',
      implementation: {
        type: 'function',
        definition: async (pattern: any, params: any) => {
          return { matches: [], count: 0 };
        },
        dependencies: [],
        computeRequirements: { cpuCores: 4, memory: 512, estimatedDuration: 1000 }
      },
      parameters: [
        {
          name: 'similarityThreshold',
          type: 'number',
          default: 0.8,
          range: [0, 1],
          description: 'Minimum similarity threshold',
          required: false
        }
      ],
      constraints: {},
      performance: {
        averageRuntime: 1000,
        successRate: 0.85,
        accuracy: 0.8,
        resourceUsage: { cpu: 0.4, memory: 0.2 },
        lastExecuted: 0
      },
      version: '1.0.0'
    });
    
    console.log('[Fabric Algo] Registered 3 default algorithms');
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}

// ============================================================================
// Algorithm Registry
// ============================================================================

class AlgorithmRegistry {
  private byType: Map<AlgorithmType, Set<string>>;
  private byCategory: Map<AlgorithmCategory, Set<string>>;
  
  constructor(private algo: FabricAlgo) {
    this.byType = new Map();
    this.byCategory = new Map();
  }
  
  async register(algorithm: Algorithm): Promise<void> {
    // 按類型註冊
    if (!this.byType.has(algorithm.type)) {
      this.byType.set(algorithm.type, new Set());
    }
    this.byType.get(algorithm.type)!.add(algorithm.id);
    
    // 按類別註冊
    if (!this.byCategory.has(algorithm.category)) {
      this.byCategory.set(algorithm.category, new Set());
    }
    this.byCategory.get(algorithm.category)!.add(algorithm.id);
  }
  
  async unregister(algorithmId: string): Promise<void> {
    // 從類型映射中移除
    for (const [type, ids] of this.byType) {
      ids.delete(algorithmId);
    }
    
    // 從類別映射中移除
    for (const [category, ids] of this.byCategory) {
      ids.delete(algorithmId);
    }
  }
}

// ============================================================================
// Algorithm Execution Engine
// ============================================================================

class AlgorithmExecutionEngine {
  constructor(private algo: FabricAlgo) {}
  
  async initialize(): Promise<void> {
    console.log('[Execution Engine] Initializing...');
  }
  
  async execute(algorithm: Algorithm, input: any, parameters: Record<string, any>): Promise<any> {
    // 執行演算法實作
    if (algorithm.implementation.type === 'function') {
      return await algorithm.implementation.definition(input, parameters);
    }
    
    // 其他類型的實作（flow, pipeline, composite）可以在這裡處理
    throw new Error(`Unsupported implementation type: ${algorithm.implementation.type}`);
  }
}

// ============================================================================
// Performance Tracker
// ============================================================================

class PerformanceTracker {
  private executionHistory: Map<string, number[]>;
  
  constructor(private algo: FabricAlgo) {
    this.executionHistory = new Map();
  }
  
  async initialize(): Promise<void> {
    console.log('[Performance Tracker] Initializing...');
  }
  
  async trackExecution(algorithmId: string, execution: AlgorithmExecution): Promise<void> {
    if (!this.executionHistory.has(algorithmId)) {
      this.executionHistory.set(algorithmId, []);
    }
    
    const history = this.executionHistory.get(algorithmId)!;
    history.push(execution.performance.runtime);
    
    // 只保留最近 100 次執行
    if (history.length > 100) {
      history.shift();
    }
  }
  
  async getAverageRuntime(algorithmId: string): Promise<number> {
    const history = this.executionHistory.get(algorithmId);
    
    if (!history || history.length === 0) {
      return 0;
    }
    
    return history.reduce((sum, time) => sum + time, 0) / history.length;
  }
}

// ============================================================================
// Type Definitions
// ============================================================================

export interface AlgoStatistics {
  totalAlgorithms: number;
  totalExecutions: number;
  successfulExecutions: number;
  failedExecutions: number;
  averageExecutionTime: number;
  algorithmTypes: Record<AlgorithmType, number>;
}