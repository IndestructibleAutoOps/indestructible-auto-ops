// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-composition
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - Fabric Composition
 * Version 19.0.0
 * 
 * 核心：組合視角
 * - 織網上的「路徑搜尋與組合」
 * - 動態組合演算法、計算、流程
 * - 自動發現最佳執行路徑
 * - 智能組合優化
 */

import { FabricCore, FabricNode, FabricEdge } from '../fabric-core';
import { FabricAlgo, Algorithm } from '../fabric-algo';
import { FabricCompute, ComputeTask } from '../fabric-compute';

// ============================================================================
// Type Definitions
// ============================================================================

export interface Composition {
  id: string;
  name: string;
  type: CompositionType;
  description: string;
  components: Component[];
  connections: Connection[];
  properties: CompositionProperties;
  performance: CompositionPerformance;
  version: string;
}

export type CompositionType = 
  | 'linear'         // 線性組合
  | 'parallel'       // 並行組合
  | 'branching'      // 分支組合
  | 'loop'           // 循環組合
  | 'conditional'    // 條件組合
  | 'recursive'      // 遞迴組合
  | 'adaptive';      // 自適應組合

export interface Component {
  id: string;
  type: ComponentType;
  ref: string; // Reference to algorithm, flow, or task
  parameters: Record<string, any>;
  position: Position;
}

export type ComponentType = 
  | 'algorithm'
  | 'flow'
  | 'task'
  | 'sub_composition';

export interface Position {
  x: number;
  y: number;
  layer: number;
}

export interface Connection {
  id: string;
  sourceComponentId: string;
  targetComponentId: string;
  condition?: ConnectionCondition;
  weight: number;
}

export interface ConnectionCondition {
  type: 'always' | 'on_success' | 'on_failure' | 'on_value' | 'custom';
  condition?: any;
}

export interface CompositionProperties {
  deterministic: boolean;
  retryPolicy: RetryPolicy;
  timeout: number;
  maxParallelism: number;
  enableCaching: boolean;
}

export interface RetryPolicy {
  maxAttempts: number;
  backoffStrategy: 'fixed' | 'exponential' | 'linear';
  initialDelay: number;
}

export interface CompositionPerformance {
  averageExecutionTime: number;
  successRate: number;
  throughput: number;
  resourceEfficiency: number;
  lastExecuted: number;
}

export interface CompositionExecution {
  id: string;
  compositionId: string;
  input: any;
  startTime: number;
  endTime?: number;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  componentExecutions: Map<string, ComponentExecution>;
  result?: any;
  error?: Error;
  performance: {
    executionTime: number;
    componentsExecuted: number;
    cacheHits: number;
  };
}

export interface ComponentExecution {
  componentId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  input: any;
  output?: any;
  startTime: number;
  endTime?: number;
  error?: Error;
}

export interface CompositionConfig {
  enableAutoOptimization: boolean;
  enablePathSearch: boolean;
  maxExecutionDepth: number;
  enableMemoization: boolean;
}

// ============================================================================
// Fabric Composition Class
// ============================================================================

export class FabricComposition {
  private fabric: FabricCore;
  private algo: FabricAlgo;
  private compute: FabricCompute;
  private config: CompositionConfig;
  private compositions: Map<string, Composition>;
  private executions: Map<string, CompositionExecution>;
  private pathFinder: PathFinder;
  private optimizer: CompositionOptimizer;
  private executor: CompositionExecutor;
  private initialized: boolean;
  
  constructor(
    fabric: FabricCore,
    algo: FabricAlgo,
    compute: FabricCompute,
    config?: Partial<CompositionConfig>
  ) {
    this.fabric = fabric;
    this.algo = algo;
    this.compute = compute;
    this.config = {
      enableAutoOptimization: config?.enableAutoOptimization ?? true,
      enablePathSearch: config?.enablePathSearch ?? true,
      maxExecutionDepth: config?.maxExecutionDepth || 10,
      enableMemoization: config?.enableMemoization ?? true
    };
    
    this.compositions = new Map();
    this.executions = new Map();
    this.pathFinder = new PathFinder(this);
    this.optimizer = new CompositionOptimizer(this);
    this.executor = new CompositionExecutor(this);
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Fabric Composition] Initializing composition layer...');
    
    // 註冊預設組合
    await this.registerDefaultCompositions();
    
    // 初始化路徑搜尋器
    await this.pathFinder.initialize();
    
    // 初始化優化器
    await this.optimizer.initialize();
    
    // 初始化執行器
    await this.executor.initialize();
    
    this.initialized = true;
    console.log('[Fabric Composition] Composition layer initialized');
  }
  
  // ========================================================================
  // Composition Management
  // ========================================================================
  
  async registerComposition(composition: Composition): Promise<void> {
    console.log(`[Fabric Composition] Registering composition ${composition.name} (${composition.id})`);
    
    // 驗證組合
    await this.validateComposition(composition);
    
    // 註冊組合
    this.compositions.set(composition.id, composition);
  }
  
  async unregisterComposition(compositionId: string): Promise<void> {
    console.log(`[Fabric Composition] Unregistering composition ${compositionId}`);
    
    this.compositions.delete(compositionId);
  }
  
  async getComposition(compositionId: string): Promise<Composition | undefined> {
    return this.compositions.get(compositionId);
  }
  
  async getAllCompositions(): Promise<Composition[]> {
    return Array.from(this.compositions.values());
  }
  
  private async validateComposition(composition: Composition): Promise<void> {
    // 驗證組件
    const componentIds = new Set<string>();
    
    for (const component of composition.components) {
      if (componentIds.has(component.id)) {
        throw new Error(`Duplicate component ID: ${component.id}`);
      }
      componentIds.add(component.id);
    }
    
    // 驗證連接
    for (const connection of composition.connections) {
      if (!componentIds.has(connection.sourceComponentId)) {
        throw new Error(`Connection source component not found: ${connection.sourceComponentId}`);
      }
      if (!componentIds.has(connection.targetComponentId)) {
        throw new Error(`Connection target component not found: ${connection.targetComponentId}`);
      }
    }
  }
  
  // ========================================================================
  // Composition Execution
  // ========================================================================
  
  async executeComposition(
    compositionId: string,
    input: any,
    options?: {
      optimize?: boolean;
      searchPath?: boolean;
    }
  ): Promise<CompositionExecution> {
    console.log(`[Fabric Composition] Executing composition ${compositionId}`);
    
    const composition = this.compositions.get(compositionId);
    
    if (!composition) {
      throw new Error(`Composition ${compositionId} not found`);
    }
    
    // 創建執行記錄
    const execution: CompositionExecution = {
      id: `exec-${compositionId}-${Date.now()}`,
      compositionId,
      input,
      startTime: Date.now(),
      status: 'pending',
      componentExecutions: new Map(),
      performance: {
        executionTime: 0,
        componentsExecuted: 0,
        cacheHits: 0
      }
    };
    
    this.executions.set(execution.id, execution);
    
    // 優化（可選）
    if (options?.optimize !== false && this.config.enableAutoOptimization) {
      await this.optimizer.optimize(compositionId);
    }
    
    // 搜尋路徑（可選）
    let executionPath: string[] = [];
    if (options?.searchPath !== false && this.config.enablePathSearch) {
      executionPath = await this.pathFinder.findBestPath(compositionId, input);
    }
    
    // 執行組合
    execution.status = 'running';
    
    try {
      const result = await this.executor.execute(composition, input, executionPath);
      
      execution.endTime = Date.now();
      execution.status = 'completed';
      execution.result = result;
      execution.performance.executionTime = execution.endTime - execution.startTime;
      
      // 更新性能統計
      composition.performance.averageExecutionTime = 
        (composition.performance.averageExecutionTime + execution.performance.executionTime) / 2;
      composition.performance.lastExecuted = Date.now();
      
    } catch (error) {
      execution.endTime = Date.now();
      execution.status = 'failed';
      execution.error = error as Error;
      
      // 更新失敗率
      composition.performance.successRate = 
        (composition.performance.successRate * 9) / 10;
    }
    
    console.log(`[Fabric Composition] Composition ${compositionId} execution completed with status ${execution.status}`);
    return execution;
  }
  
  async getExecution(executionId: string): Promise<CompositionExecution | undefined> {
    return this.executions.get(executionId);
  }
  
  // ========================================================================
  // Path Finding
  // ========================================================================
  
  async findExecutionPath(
    compositionId: string,
    input: any,
    criteria?: {
      minimizeTime?: boolean;
      maximizeSuccessRate?: boolean;
      minimizeResourceUsage?: boolean;
    }
  ): Promise<string[]> {
    if (!this.config.enablePathSearch) {
      return [];
    }
    
    console.log(`[Fabric Composition] Finding execution path for composition ${compositionId}`);
    
    return await this.pathFinder.findBestPath(
      compositionId,
      input,
      criteria
    );
  }
  
  // ========================================================================
  // Composition Building
  // ========================================================================
  
  async buildComposition(
    name: string,
    type: CompositionType,
    components: Omit<Component, 'id' | 'position'>[],
    connections: Omit<Connection, 'id'>[],
    options?: Partial<CompositionProperties>
  ): Promise<Composition> {
    console.log(`[Fabric Composition] Building composition ${name}`);
    
    // 生成組件 ID 和位置
    const compositionComponents: Component[] = [];
    
    for (let i = 0; i < components.length; i++) {
      const component: Component = {
        id: `comp-${Date.now()}-${i}`,
        ...components[i],
        position: {
          x: i * 100,
          y: 0,
          layer: 0
        }
      };
      compositionComponents.push(component);
    }
    
    // 生成連接 ID
    const compositionConnections: Connection[] = connections.map((conn, i) => ({
      id: `conn-${Date.now()}-${i}`,
      ...conn
    }));
    
    // 建構組合
    const composition: Composition = {
      id: `composition-${Date.now()}`,
      name,
      type,
      description: `Auto-generated ${type} composition`,
      components: compositionComponents,
      connections: compositionConnections,
      properties: {
        deterministic: true,
        retryPolicy: {
          maxAttempts: 3,
          backoffStrategy: 'exponential',
          initialDelay: 1000
        },
        timeout: 60000,
        maxParallelism: 5,
        enableCaching: true,
        ...options
      },
      performance: {
        averageExecutionTime: 0,
        successRate: 1.0,
        throughput: 0,
        resourceEfficiency: 1.0,
        lastExecuted: 0
      },
      version: '1.0.0'
    };
    
    // 註冊組合
    await this.registerComposition(composition);
    
    return composition;
  }
  
  // ========================================================================
  // Statistics
  // ========================================================================
  
  async getStatistics(): Promise<CompositionStatistics> {
    const compositions = Array.from(this.compositions.values());
    const executions = Array.from(this.executions.values());
    
    return {
      totalCompositions: compositions.length,
      totalExecutions: executions.length,
      successfulExecutions: executions.filter(e => e.status === 'completed').length,
      failedExecutions: executions.filter(e => e.status === 'failed').length,
      averageExecutionTime: executions.reduce((sum, e) => sum + e.performance.executionTime, 0) / executions.length || 0,
      compositionTypes: this.groupByType(compositions)
    };
  }
  
  private groupByType(compositions: Composition[]): Record<CompositionType, number> {
    const counts = {} as Record<CompositionType, number>;
    
    for (const comp of compositions) {
      counts[comp.type] = (counts[comp.type] || 0) + 1;
    }
    
    return counts;
  }
  
  private async registerDefaultCompositions(): Promise<void> {
    console.log('[Fabric Composition] Registering default compositions...');
    
    // 註冊預設組合：線性推理流程
    const linearComposition: Composition = {
      id: 'comp-linear-reasoning',
      name: 'Linear Reasoning Flow',
      type: 'linear',
      description: 'Linear composition for reasoning tasks',
      components: [
        {
          id: 'comp-input',
          type: 'task',
          ref: 'input-processing',
          parameters: {},
          position: { x: 0, y: 0, layer: 0 }
        },
        {
          id: 'comp-reason',
          type: 'algorithm',
          ref: 'algo-path-search',
          parameters: { maxDepth: 10 },
          position: { x: 100, y: 0, layer: 0 }
        },
        {
          id: 'comp-output',
          type: 'task',
          ref: 'output-generation',
          parameters: {},
          position: { x: 200, y: 0, layer: 0 }
        }
      ],
      connections: [
        {
          id: 'conn-1',
          sourceComponentId: 'comp-input',
          targetComponentId: 'comp-reason',
          condition: { type: 'always' },
          weight: 1.0
        },
        {
          id: 'conn-2',
          sourceComponentId: 'comp-reason',
          targetComponentId: 'comp-output',
          condition: { type: 'always' },
          weight: 1.0
        }
      ],
      properties: {
        deterministic: true,
        retryPolicy: {
          maxAttempts: 3,
          backoffStrategy: 'exponential',
          initialDelay: 1000
        },
        timeout: 60000,
        maxParallelism: 1,
        enableCaching: true
      },
      performance: {
        averageExecutionTime: 0,
        successRate: 1.0,
        throughput: 0,
        resourceEfficiency: 1.0,
        lastExecuted: 0
      },
      version: '1.0.0'
    };
    
    await this.registerComposition(linearComposition);
    
    console.log('[Fabric Composition] Registered 1 default composition');
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
  
  // ========================================================================
  // Getters for internal components
  // ========================================================================
  
  getAlgo(): FabricAlgo {
    return this.algo;
  }
  
  getCompute(): FabricCompute {
    return this.compute;
  }
}

// ============================================================================
// Path Finder
// ============================================================================

class PathFinder {
  private pathCache: Map<string, string[]>;
  
  constructor(private composition: FabricComposition) {
    this.pathCache = new Map();
  }
  
  async initialize(): Promise<void> {
    console.log('[Path Finder] Initializing...');
  }
  
  async findBestPath(
    compositionId: string,
    input: any,
    criteria?: {
      minimizeTime?: boolean;
      maximizeSuccessRate?: boolean;
      minimizeResourceUsage?: boolean;
    }
  ): Promise<string[]> {
    const composition = this.composition['compositions'].get(compositionId);
    
    if (!composition) {
      throw new Error(`Composition ${compositionId} not found`);
    }
    
    // 檢查緩存
    const cacheKey = `${compositionId}-${JSON.stringify(criteria)}`;
    if (this.pathCache.has(cacheKey)) {
      return this.pathCache.get(cacheKey)!;
    }
    
    // 根據組合類型搜尋路徑
    let path: string[];
    
    switch (composition.type) {
      case 'linear':
        path = this.findLinearPath(composition);
        break;
      case 'parallel':
        path = this.findParallelPath(composition);
        break;
      case 'branching':
        path = this.findBranchingPath(composition, input);
        break;
      case 'loop':
        path = this.findLoopPath(composition, input);
        break;
      case 'conditional':
        path = this.findConditionalPath(composition, input);
        break;
      default:
        path = this.findLinearPath(composition);
    }
    
    // 緩存路徑
    this.pathCache.set(cacheKey, path);
    
    return path;
  }
  
  private findLinearPath(composition: Composition): string[] {
    // 線性路徑：按連接順序
    const path: string[] = [];
    const visited = new Set<string>();
    
    // 找到起始節點
    const startComponents = composition.components.filter(c => 
      !composition.connections.some(conn => conn.targetComponentId === c.id)
    );
    
    if (startComponents.length === 0) {
      return composition.components.map(c => c.id);
    }
    
    // 深度優先搜尋
    const dfs = (componentId: string): void => {
      if (visited.has(componentId)) {
        return;
      }
      
      visited.add(componentId);
      path.push(componentId);
      
      const outgoingConnections = composition.connections.filter(
        conn => conn.sourceComponentId === componentId
      );
      
      for (const conn of outgoingConnections) {
        dfs(conn.targetComponentId);
      }
    };
    
    for (const start of startComponents) {
      dfs(start.id);
    }
    
    return path;
  }
  
  private findParallelPath(composition: Composition): string[] {
    // 並行路徑：所有並行分支
    const path: string[] = [];
    
    for (const component of composition.components) {
      path.push(component.id);
    }
    
    return path;
  }
  
  private findBranchingPath(composition: Composition, input: any): string[] {
    // 分支路徑：根據條件選擇
    const path: string[] = [];
    
    // 簡化實作：選擇第一個分支
    const startComponents = composition.components.filter(c => 
      !composition.connections.some(conn => conn.targetComponentId === c.id)
    );
    
    if (startComponents.length > 0) {
      path.push(startComponents[0].id);
      
      const outgoingConnections = composition.connections.filter(
        conn => conn.sourceComponentId === startComponents[0].id
      );
      
      if (outgoingConnections.length > 0) {
        // 選擇權重最高的連接
        outgoingConnections.sort((a, b) => b.weight - a.weight);
        path.push(outgoingConnections[0].targetComponentId);
      }
    }
    
    return path;
  }
  
  private findLoopPath(composition: Composition, input: any): string[] {
    // 循環路徑：簡化實作
    return this.findLinearPath(composition);
  }
  
  private findConditionalPath(composition: Composition, input: any): string[] {
    // 條件路徑：簡化實作
    return this.findBranchingPath(composition, input);
  }
}

// ============================================================================
// Composition Optimizer
// ============================================================================

class CompositionOptimizer {
  constructor(private composition: FabricComposition) {}
  
  async initialize(): Promise<void> {
    console.log('[Composition Optimizer] Initializing...');
  }
  
  async optimize(compositionId: string): Promise<void> {
    console.log(`[Composition Optimizer] Optimizing composition ${compositionId}`);
    
    const composition = this.composition['compositions'].get(compositionId);
    
    if (!composition) {
      throw new Error(`Composition ${compositionId} not found`);
    }
    
    // 優化步驟：
    // 1. 移除冗餘組件
    await this.removeRedundantComponents(composition);
    
    // 2. 合併相似組件
    await this.mergeSimilarComponents(composition);
    
    // 3. 優化連接權重
    await this.optimizeConnectionWeights(composition);
    
    console.log(`[Composition Optimizer] Composition ${compositionId} optimized`);
  }
  
  private async removeRedundantComponents(composition: Composition): Promise<void> {
    // 簡化實作：無操作
  }
  
  private async mergeSimilarComponents(composition: Composition): Promise<void> {
    // 簡化實作：無操作
  }
  
  private async optimizeConnectionWeights(composition: Composition): Promise<void> {
    // 基於歷史執行數據優化權重
    for (const conn of composition.connections) {
      // 簡化實作：使用固定權重
      conn.weight = 1.0;
    }
  }
}

// ============================================================================
// Composition Executor
// ============================================================================

class CompositionExecutor {
  constructor(private composition: FabricComposition) {}
  
  async initialize(): Promise<void> {
    console.log('[Composition Executor] Initializing...');
  }
  
  async execute(
    composition: Composition,
    input: any,
    path: string[]
  ): Promise<any> {
    console.log(`[Composition Executor] Executing composition ${composition.id}`);
    
    const executionMap = new Map<string, ComponentExecution>();
    let currentInput = input;
    let result: any = input;
    
    // 按路徑執行組件
    for (const componentId of path) {
      const component = composition.components.find(c => c.id === componentId);
      
      if (!component) {
        throw new Error(`Component ${componentId} not found`);
      }
      
      // 創建組件執行記錄
      const componentExec: ComponentExecution = {
        componentId,
        status: 'running',
        input: currentInput,
        startTime: Date.now()
      };
      
      executionMap.set(componentId, componentExec);
      
      try {
        // 執行組件
        currentInput = await this.executeComponent(component, currentInput);
        
        componentExec.status = 'completed';
        componentExec.output = currentInput;
        componentExec.endTime = Date.now();
        
        result = currentInput;
        
      } catch (error) {
        componentExec.status = 'failed';
        componentExec.error = error as Error;
        componentExec.endTime = Date.now();
        
        throw error;
      }
    }
    
    return result;
  }
  
  private async executeComponent(component: Component, input: any): Promise<any> {
    const algo = this.composition.getAlgo();
    
    switch (component.type) {
      case 'algorithm':
        // 執行演算法
        const algorithm = await algo.getAlgorithm(component.ref);
        if (!algorithm) {
          throw new Error(`Algorithm ${component.ref} not found`);
        }
        const execution = await algo.executeAlgorithm(
          component.ref,
          input,
          component.parameters
        );
        return execution.result;
        
      case 'flow':
        // 執行流程
        return await this.executeFlow(component.ref, input, component.parameters);
        
      case 'task':
        // 執行任務
        return await this.executeTask(component.ref, input, component.parameters);
        
      case 'sub_composition':
        // 執行子組合
        return await this.composition.executeComposition(
          component.ref,
          input,
          component.parameters
        );
        
      default:
        throw new Error(`Unknown component type: ${component.type}`);
    }
  }
  
  private async executeFlow(flowRef: string, input: any, parameters: any): Promise<any> {
    // 簡化實作：返回輸入
    return { flow: flowRef, input, result: input };
  }
  
  private async executeTask(taskRef: string, input: any, parameters: any): Promise<any> {
    // 簡化實作：返回輸入
    return { task: taskRef, input, result: input };
  }
}

// ============================================================================
// Type Definitions
// ============================================================================

export interface CompositionStatistics {
  totalCompositions: number;
  totalExecutions: number;
  successfulExecutions: number;
  failedExecutions: number;
  averageExecutionTime: number;
  compositionTypes: Record<CompositionType, number>;
}