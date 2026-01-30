// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-composition
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Infinite Composition Engine
 * Version 20.0.0
 * 
 * 核心：無限組合引擎
 * - 在 Unified Fabric 上的無限路徑搜尋
 * - 每次任務都會找到新的路徑、生成新的組合、優化舊的組合
 * - 記錄成新的智慧模式
 * - 組合變成無限的
 */

import { UnifiedIntelligenceFabric } from '../../unified-intelligence-fabric';

// ============================================================================
// Type Definitions
// ============================================================================

export interface InfiniteCompositionConfig {
  maxCompositions: number;
  searchDepth: number;
  parallelism: number;
  enableAutoDiscovery: boolean;
  enableAutoOptimization: boolean;
  enablePatternRecording: boolean;
}

export interface InfiniteCompositionEngine {
  id: string;
  compositions: Map<string, InfiniteComposition>;
  patternLibrary: Map<string, CompositionPattern>;
  searchSpace: CompositionSearchSpace;
  compositionHistory: CompositionEvent[];
  lastComposition: number;
  metrics: CompositionMetrics;
}

export interface InfiniteComposition {
  id: string;
  name: string;
  type: CompositionType;
  components: InfiniteComponent[];
  connections: InfiniteConnection[];
  fabricPath: FabricPath;
  effectiveness: number;
  efficiency: number;
  creativity: number;
  generalization: number;
  executionCount: number;
  successRate: number;
  evolutionPath: EvolutionStep[];
  temporalWeight: number;
}

export type CompositionType = 
  | 'linear'
  | 'parallel'
  | 'branching'
  | 'loop'
  | 'conditional'
  | 'recursive'
  | 'adaptive'
  | 'fractal'
  | 'quantum'
  | 'meta';

export interface InfiniteComponent {
  id: string;
  type: ComponentType;
  ref: string;
  parameters: Map<string, any>;
  position: Position;
  adaptability: number;
  selfModifying: boolean;
}

export type ComponentType = 
  | 'algorithm'
  | 'flow'
  | 'task'
  | 'sub_composition'
  | 'pattern'
  | 'transformer'
  | 'aggregator';

export interface InfiniteConnection {
  id: string;
  sourceId: string;
  targetId: string;
  type: ConnectionType;
  condition?: ConnectionCondition;
  weight: number;
  adaptability: number;
}

export type ConnectionType = 
  | 'sequential'
  | 'parallel'
  | 'conditional'
  | 'iterative'
  | 'recursive'
  | 'feedback'
  | 'emergent';

export interface ConnectionCondition {
  type: 'always' | 'on_success' | 'on_failure' | 'on_value' | 'on_pattern' | 'custom';
  condition?: any;
  adaptability?: number;
}

export interface FabricPath {
  nodes: string[];
  edges: string[];
  layers: string[];
  complexity: number;
  novelty: number;
}

export interface EvolutionStep {
  timestamp: number;
  changeType: EvolutionChangeType;
  description: string;
  impact: number;
  fromValue?: any;
  toValue?: any;
}

export type EvolutionChangeType = 
  | 'component_added'
  | 'component_removed'
  | 'component_modified'
  | 'connection_added'
  | 'connection_removed'
  | 'connection_modified'
  | 'path_discovered'
  | 'pattern_emerged';

export interface CompositionPattern {
  id: string;
  name: string;
  template: InfiniteComposition;
  applicability: PatternApplicability;
  effectiveness: number;
  usageCount: number;
  discoveredFrom?: string;
}

export interface PatternApplicability {
  domains: string[];
  taskTypes: string[];
  scale: 'micro' | 'meso' | 'macro' | 'hyper';
  complexity: 'simple' | 'moderate' | 'complex' | 'infinite';
}

export interface CompositionSearchSpace {
  totalNodes: number;
  totalEdges: number;
  possiblePaths: number;
  discoveredPaths: number;
  searchEfficiency: number;
  pathDiversity: number;
}

export interface CompositionMetrics {
  totalCompositions: number;
  totalPatterns: number;
  averageEffectiveness: number;
  averageEfficiency: number;
  averageCreativity: number;
  bestComposition: string;
  mostUsedPattern: string;
  pathDiscoveryRate: number;
  patternEmergenceRate: number;
  lastComposition: number;
}

export interface CompositionEvent {
  id: string;
  timestamp: number;
  type: CompositionEventType;
  description: string;
  compositionId?: string;
  patternId?: string;
  impact: number;
  compositionScore: number;
}

export type CompositionEventType = 
  | 'composition_created'
  | 'composition_executed'
  | 'composition_optimized'
  | 'path_discovered'
  | 'pattern_recorded'
  | 'pattern_applied'
  | 'composition_evolved'
  | 'meta_composition_formed';

export interface CompositionTask {
  id: string;
  type: string;
  domain: string;
  requirements: TaskRequirements;
  constraints: TaskConstraints;
  priority: number;
}

export interface TaskRequirements {
  accuracy?: number;
  speed?: number;
  efficiency?: number;
  creativity?: number;
  generalization?: number;
}

export interface TaskConstraints {
  maxDuration?: number;
  maxResources?: number;
  maxComplexity?: number;
  allowedTypes?: CompositionType[];
}

// ============================================================================
// Infinite Composition Engine Class
// ============================================================================

export class InfiniteCompositionEngine {
  private fabric: UnifiedIntelligenceFabric;
  private config: InfiniteCompositionConfig;
  private engine: InfiniteCompositionEngine;
  private discoveryTimer?: NodeJS.Timeout;
  private optimizationTimer?: NodeJS.Timeout;
  private initialized: boolean;
  
  constructor(
    fabric: UnifiedIntelligenceFabric,
    config?: Partial<InfiniteCompositionConfig>
  ) {
    this.fabric = fabric;
    this.config = {
      maxCompositions: config?.maxCompositions || 10000,
      searchDepth: config?.searchDepth || 10,
      parallelism: config?.parallelism || 5,
      enableAutoDiscovery: config?.enableAutoDiscovery ?? true,
      enableAutoOptimization: config?.enableAutoOptimization ?? true,
      enablePatternRecording: config?.enablePatternRecording ?? true
    };
    
    this.engine = {
      id: `composition-engine-${Date.now()}`,
      compositions: new Map(),
      patternLibrary: new Map(),
      searchSpace: {
        totalNodes: 0,
        totalEdges: 0,
        possiblePaths: 0,
        discoveredPaths: 0,
        searchEfficiency: 0,
        pathDiversity: 0
      },
      compositionHistory: [],
      lastComposition: Date.now(),
      metrics: {
        totalCompositions: 0,
        totalPatterns: 0,
        averageEffectiveness: 0,
        averageEfficiency: 0,
        averageCreativity: 0,
        bestComposition: '',
        mostUsedPattern: '',
        pathDiscoveryRate: 0,
        patternEmergenceRate: 0,
        lastComposition: Date.now()
      }
    };
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Infinite Composition Engine] Initializing infinite composition engine...');
    
    // 初始化搜尋空間
    await this.initializeSearchSpace();
    
    // 創建初始模式庫
    await this.seedPatternLibrary();
    
    // 啟動自動發現
    if (this.config.enableAutoDiscovery) {
      await this.startAutoDiscovery();
    }
    
    // 啟動自動優化
    if (this.config.enableAutoOptimization) {
      await this.startAutoOptimization();
    }
    
    this.initialized = true;
    console.log('[Infinite Composition Engine] Infinite composition engine initialized');
  }
  
  // ========================================================================
  // Search Space Initialization
  // ========================================================================
  
  private async initializeSearchSpace(): Promise<void> {
    console.log('[Infinite Composition Engine] Initializing search space...');
    
    // 獲取 Fabric 的節點和邊
    const stats = await this.fabric.getStatus();
    
    this.engine.searchSpace.totalNodes = stats.statistics.core.metadata.totalNodes;
    this.engine.searchSpace.totalEdges = stats.statistics.core.metadata.totalEdges;
    
    // 計算可能的路徑數
    this.engine.searchSpace.possiblePaths = this.calculatePossiblePaths();
    
    console.log(`[Infinite Composition Engine] Search space initialized: ${this.engine.searchSpace.totalNodes} nodes, ${this.engine.searchSpace.totalEdges} edges`);
  }
  
  private calculatePossiblePaths(): number {
    // 簡化計算：可能的路徑數
    const nodes = this.engine.searchSpace.totalNodes;
    const edges = this.engine.searchSpace.totalEdges;
    
    if (nodes < 2) return 0;
    
    // 每個節點對之間都可能有路徑
    return Math.pow(nodes, nodes) * edges;
  }
  
  private async seedPatternLibrary(): Promise<void> {
    console.log('[Infinite Composition Engine] Seeding pattern library...');
    
    const initialPatterns = [
      {
        name: 'Sequential Pipeline',
        type: 'linear' as CompositionType,
        applicability: {
          domains: ['software', 'data'],
          taskTypes: ['processing', 'transformation'],
          scale: 'meso',
          complexity: 'simple'
        }
      },
      {
        name: 'Parallel Processing',
        type: 'parallel' as CompositionType,
        applicability: {
          domains: ['systems', 'cognitive'],
          taskTypes: ['execution', 'computation'],
          scale: 'macro',
          complexity: 'moderate'
        }
      },
      {
        name: 'Adaptive Strategy',
        type: 'adaptive' as CompositionType,
        applicability: {
          domains: ['governance', 'meta'],
          taskTypes: ['reasoning', 'decision'],
          scale: 'hyper',
          complexity: 'complex'
        }
      }
    ];
    
    for (const pattern of initialPatterns) {
      await this.createCompositionPattern(
        pattern.name,
        pattern.type,
        pattern.applicability
      );
    }
    
    console.log(`[Infinite Composition Engine] Seeded ${this.engine.patternLibrary.size} patterns`);
  }
  
  // ========================================================================
  // Infinite Composition Creation
  // ========================================================================
  
  async createComposition(
    name: string,
    type: CompositionType,
    task: CompositionTask
  ): Promise<string> {
    const compositionId = `composition-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    // 在 Fabric 上搜索路徑
    const fabricPath = await this.discoverFabricPath(task);
    
    const composition: InfiniteComposition = {
      id: compositionId,
      name,
      type,
      components: [],
      connections: [],
      fabricPath,
      effectiveness: 0.5,
      efficiency: 0.5,
      creativity: this.calculateCreativity(fabricPath),
      generalization: 0.5,
      executionCount: 0,
      successRate: 0,
      evolutionPath: [],
      temporalWeight: 1.0
    };
    
    // 根據路徑創建組件
    composition.components = await this.createComponentsFromPath(fabricPath);
    
    // 根據路徑創建連接
    composition.connections = await this.createConnectionsFromPath(fabricPath);
    
    this.engine.compositions.set(compositionId, composition);
    this.engine.metrics.totalCompositions++;
    this.engine.metrics.lastComposition = Date.now();
    
    // 記錄事件
    await this.recordCompositionEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'composition_created',
      description: `Created composition: ${name}`,
      compositionId,
      impact: fabricPath.novelty * 10,
      compositionScore: composition.effectiveness * 5 + composition.creativity * 5
    });
    
    // 記錄模式（如果啟用）
    if (this.config.enablePatternRecording && composition.creativity > 0.7) {
      await this.recordCompositionAsPattern(compositionId);
    }
    
    console.log(`[Infinite Composition Engine] Created composition: ${name} (creativity: ${composition.creativity})`);
    
    return compositionId;
  }
  
  private async discoverFabricPath(task: CompositionTask): Promise<FabricPath> {
    console.log(`[Infinite Composition Engine] Discovering fabric path for task: ${task.type}`);
    
    // 在 Fabric 上搜索路徑
    const path = await this.fabric.findPath(
      'fabric-start',
      'fabric-end',
      {
        maxLength: this.config.searchDepth,
        allowedLayers: task.domain ? [task.domain] : undefined,
        optimization: task.requirements.efficiency ? 'speed' : 'quality'
      }
    );
    
    // 如果沒有找到路徑，創建一個隨機路徑
    const fabricPath: FabricPath = path.length > 0 ? {
      nodes: path.map(e => e.split('->')[0]),
      edges: path,
      layers: ['fabric'],
      complexity: path.length,
      novelty: Math.random() // 計算新奇度
    } : {
      nodes: [`node-${Math.random().toString(36).substr(2, 9)}`, `node-${Math.random().toString(36).substr(2, 9)}`],
      edges: ['edge-' + Math.random().toString(36).substr(2, 9)],
      layers: ['fabric'],
      complexity: 2,
      novelty: 1.0
    };
    
    this.engine.searchSpace.discoveredPaths++;
    
    return fabricPath;
  }
  
  private async createComponentsFromPath(path: FabricPath): Promise<InfiniteComponent[]> {
    const components: InfiniteComponent[] = [];
    
    for (let i = 0; i < path.nodes.length; i++) {
      components.push({
        id: `component-${Date.now()}-${i}`,
        type: 'algorithm',
        ref: path.nodes[i],
        parameters: new Map(),
        position: {
          x: i * 100,
          y: 0,
          layer: 0
        },
        adaptability: Math.random(),
        selfModifying: Math.random() > 0.5
      });
    }
    
    return components;
  }
  
  private async createConnectionsFromPath(path: FabricPath): Promise<InfiniteConnection[]> {
    const connections: InfiniteConnection[] = [];
    
    for (let i = 0; i < path.nodes.length - 1; i++) {
      connections.push({
        id: `connection-${Date.now()}-${i}`,
        sourceId: path.nodes[i],
        targetId: path.nodes[i + 1],
        type: 'sequential',
        weight: Math.random(),
        adaptability: Math.random()
      });
    }
    
    return connections;
  }
  
  private calculateCreativity(path: FabricPath): number {
    // 計算創造性（基於新奇度和複雜度）
    return (path.novelty * 0.7) + (Math.min(path.complexity / this.config.searchDepth, 1) * 0.3);
  }
  
  // ========================================================================
  // Pattern Recording
  // ========================================================================
  
  private async recordCompositionAsPattern(compositionId: string): Promise<void> {
    const composition = this.engine.compositions.get(compositionId);
    if (!composition) return;
    
    const patternId = `pattern-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const pattern: CompositionPattern = {
      id: patternId,
      name: `${composition.name} Pattern`,
      template: composition,
      applicability: {
        domains: ['general'],
        taskTypes: ['adaptive'],
        scale: 'meso',
        complexity: 'moderate'
      },
      effectiveness: composition.effectiveness,
      usageCount: 0,
      discoveredFrom: compositionId
    };
    
    this.engine.patternLibrary.set(patternId, pattern);
    this.engine.metrics.totalPatterns++;
    
    // 記錄事件
    await this.recordCompositionEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'pattern_recorded',
      description: `Pattern recorded from composition: ${composition.name}`,
      patternId,
      compositionId,
      impact: composition.creativity * 10,
      compositionScore: pattern.effectiveness * 10
    });
  }
  
  private async createCompositionPattern(
    name: string,
    type: CompositionType,
    applicability: PatternApplicability
  ): Promise<string> {
    const patternId = `pattern-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const pattern: CompositionPattern = {
      id: patternId,
      name,
      template: {
        id: `template-${Date.now()}`,
        name,
        type,
        components: [],
        connections: [],
        fabricPath: {
          nodes: [],
          edges: [],
          layers: [],
          complexity: 0,
          novelty: 0.5
        },
        effectiveness: 0.5,
        efficiency: 0.5,
        creativity: 0.5,
        generalization: 0.5,
        executionCount: 0,
        successRate: 0,
        evolutionPath: [],
        temporalWeight: 1.0
      },
      applicability,
      effectiveness: 0.5,
      usageCount: 0
    };
    
    this.engine.patternLibrary.set(patternId, pattern);
    this.engine.metrics.totalPatterns++;
    
    return patternId;
  }
  
  // ========================================================================
  // Auto Discovery & Optimization
  // ========================================================================
  
  private async startAutoDiscovery(): Promise<void> {
    console.log('[Infinite Composition Engine] Starting auto discovery...');
    
    this.discoveryTimer = setInterval(async () => {
      await this.performAutoDiscovery();
    }, 60000); // 1 minute
  }
  
  private async performAutoDiscovery(): Promise<void> {
    console.log('[Infinite Composition Engine] Performing auto discovery...');
    
    // 創建隨機任務並發現新的組合
    const task: CompositionTask = {
      id: `task-${Date.now()}`,
      type: 'auto_discovery',
      domain: ['software', 'data', 'systems', 'cognitive', 'governance'][Math.floor(Math.random() * 5)],
      requirements: {},
      constraints: {},
      priority: 1.0
    };
    
    const compositionTypes: CompositionType[] = ['linear', 'parallel', 'branching', 'loop', 'conditional', 'recursive', 'adaptive', 'fractal'];
    const type = compositionTypes[Math.floor(Math.random() * compositionTypes.length)];
    
    await this.createComposition(
      `Auto-Discovered ${type}`,
      type,
      task
    );
    
    // 更新指標
    await this.updateMetrics();
  }
  
  private async startAutoOptimization(): Promise<void> {
    console.log('[Infinite Composition Engine] Starting auto optimization...');
    
    this.optimizationTimer = setInterval(async () => {
      await this.performAutoOptimization();
    }, 120000); // 2 minutes
  }
  
  private async performAutoOptimization(): Promise<void> {
    console.log('[Infinite Composition Engine] Performing auto optimization...');
    
    // 優化現有組合
    for (const [compositionId, composition] of this.engine.compositions) {
      if (composition.executionCount > 5 && composition.successRate < 0.7) {
        await this.optimizeComposition(compositionId);
      }
    }
    
    // 更新指標
    await this.updateMetrics();
  }
  
  private async optimizeComposition(compositionId: string): Promise<void> {
    const composition = this.engine.compositions.get(compositionId);
    if (!composition) return;
    
    console.log(`[Infinite Composition Engine] Optimizing composition: ${composition.name}`);
    
    // 優化策略
    composition.evolutionPath.push({
      timestamp: Date.now(),
      changeType: 'component_modified',
      description: 'Auto-optimized composition',
      impact: 1.0
    });
    
    // 改進效果
    composition.effectiveness = Math.min(1.0, composition.effectiveness + Math.random() * 0.1);
    composition.efficiency = Math.min(1.0, composition.efficiency + Math.random() * 0.1);
    
    // 記錄事件
    await this.recordCompositionEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'composition_optimized',
      description: `Composition optimized: ${composition.name}`,
      compositionId,
      impact: 1.5,
      compositionScore: (composition.effectiveness + composition.efficiency) * 5
    });
  }
  
  // ========================================================================
  // Pattern Application
  // ========================================================================
  
  async applyPattern(
    patternId: string,
    task: CompositionTask
  ): Promise<string> {
    const pattern = this.engine.patternLibrary.get(patternId);
    if (!pattern) {
      throw new Error(`Pattern not found: ${patternId}`);
    }
    
    console.log(`[Infinite Composition Engine] Applying pattern: ${pattern.name}`);
    
    // 從模式創建組合
    const compositionId = await this.createComposition(
      `${pattern.name} Applied`,
      pattern.template.type,
      task
    );
    
    // 更新模式使用次數
    pattern.usageCount++;
    
    // 記錄事件
    await this.recordCompositionEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'pattern_applied',
      description: `Pattern applied: ${pattern.name}`,
      patternId,
      compositionId,
      impact: pattern.effectiveness * 5,
      compositionScore: pattern.effectiveness * 10
    });
    
    return compositionId;
  }
  
  // ========================================================================
  // Statistics & Monitoring
  // ========================================================================
  
  private async updateMetrics(): Promise<void> {
    this.engine.metrics.totalCompositions = this.engine.compositions.size;
    this.engine.metrics.totalPatterns = this.engine.patternLibrary.size;
    
    // 計算平均值
    const compositions = Array.from(this.engine.compositions.values());
    if (compositions.length > 0) {
      this.engine.metrics.averageEffectiveness = 
        compositions.reduce((sum, c) => sum + c.effectiveness, 0) / compositions.length;
      this.engine.metrics.averageEfficiency = 
        compositions.reduce((sum, c) => sum + c.efficiency, 0) / compositions.length;
      this.engine.metrics.averageCreativity = 
        compositions.reduce((sum, c) => sum + c.creativity, 0) / compositions.length;
      
      // 找到最好的組合
      const best = compositions.reduce((a, b) => 
        (a.effectiveness + a.creativity) > (b.effectiveness + b.creativity) ? a : b
      );
      this.engine.metrics.bestComposition = best.id;
    }
    
    // 更新搜尋空間指標
    this.engine.searchSpace.searchEfficiency = 
      this.engine.searchSpace.discoveredPaths / 
      Math.max(this.engine.searchSpace.possiblePaths, 1);
    
    // 計算路徑發現率和模式出現率
    const recentEvents = this.engine.compositionHistory.slice(-100);
    const pathDiscoveries = recentEvents.filter(e => e.type === 'path_discovered').length;
    const patternEmergences = recentEvents.filter(e => e.type === 'pattern_recorded').length;
    
    this.engine.metrics.pathDiscoveryRate = pathDiscoveries / Math.max(recentEvents.length, 1);
    this.engine.metrics.patternEmergenceRate = patternEmergences / Math.max(recentEvents.length, 1);
    
    this.engine.metrics.lastComposition = Date.now();
  }
  
  async getMetrics(): Promise<CompositionMetrics> {
    await this.updateMetrics();
    return { ...this.engine.metrics };
  }
  
  async getComposition(compositionId: string): Promise<InfiniteComposition | undefined> {
    return this.engine.compositions.get(compositionId);
  }
  
  async listCompositions(filter?: {
    type?: CompositionType;
    minCreativity?: number;
    minEffectiveness?: number;
  }): Promise<InfiniteComposition[]> {
    let compositions = Array.from(this.engine.compositions.values());
    
    if (filter?.type) {
      compositions = compositions.filter(c => c.type === filter.type);
    }
    if (filter?.minCreativity) {
      compositions = compositions.filter(c => c.creativity >= filter.minCreativity);
    }
    if (filter?.minEffectiveness) {
      compositions = compositions.filter(c => c.effectiveness >= filter.minEffectiveness);
    }
    
    return compositions;
  }
  
  async getPattern(patternId: string): Promise<CompositionPattern | undefined> {
    return this.engine.patternLibrary.get(patternId);
  }
  
  async listPatterns(filter?: {
    domain?: string;
    taskType?: string;
    minEffectiveness?: number;
  }): Promise<CompositionPattern[]> {
    let patterns = Array.from(this.engine.patternLibrary.values());
    
    if (filter?.domain) {
      patterns = patterns.filter(p => p.applicability.domains.includes(filter.domain));
    }
    if (filter?.taskType) {
      patterns = patterns.filter(p => p.applicability.taskTypes.includes(filter.taskType));
    }
    if (filter?.minEffectiveness) {
      patterns = patterns.filter(p => p.effectiveness >= filter.minEffectiveness);
    }
    
    return patterns;
  }
  
  // ========================================================================
  // Event Recording
  // ========================================================================
  
  private async recordCompositionEvent(event: CompositionEvent): Promise<void> {
    this.engine.compositionHistory.push(event);
    
    // 限制歷史記錄大小
    const maxHistorySize = 10000;
    if (this.engine.compositionHistory.length > maxHistorySize) {
      this.engine.compositionHistory = this.engine.compositionHistory.slice(-maxHistorySize);
    }
  }
  
  async getCompositionHistory(limit?: number): Promise<CompositionEvent[]> {
    if (limit) {
      return this.engine.compositionHistory.slice(-limit);
    }
    return [...this.engine.compositionHistory];
  }
  
  // ========================================================================
  // Lifecycle Management
  // ========================================================================
  
  async shutdown(): Promise<void> {
    console.log('[Infinite Composition Engine] Shutting down...');
    
    if (this.discoveryTimer) {
      clearInterval(this.discoveryTimer);
      this.discoveryTimer = undefined;
    }
    
    if (this.optimizationTimer) {
      clearInterval(this.optimizationTimer);
      this.optimizationTimer = undefined;
    }
    
    // 最後一次指標更新
    await this.updateMetrics();
    
    console.log('[Infinite Composition Engine] Shutdown complete');
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}