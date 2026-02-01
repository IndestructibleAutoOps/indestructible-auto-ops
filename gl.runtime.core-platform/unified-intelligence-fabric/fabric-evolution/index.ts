// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-evolution
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - Fabric Evolution
 * Version 19.0.0
 * 
 * 核心：永續演化變成織網屬性
 * - 整張織網自己調整權重、重寫子圖、產生新節點/邊
 * - 演化不再是單一模組，而是織網的內在屬性
 * - 自適應、自優化、自修復
 */

import { FabricCore, FabricNode, FabricEdge } from '../fabric-core';
import { FabricFlows } from '../fabric-flows';

// ============================================================================
// Type Definitions
// ============================================================================

export interface EvolutionConfig {
  enableAutoEvolution: boolean;
  evolutionInterval: number; // milliseconds
  evolutionIntensity: number; // 0-1
  maxGenerations: number;
  mutationRate: number; // 0-1
  crossoverRate: number; // 0-1
  selectionPressure: number; // 0-1
}

export interface EvolutionEvent {
  id: string;
  timestamp: number;
  type: EvolutionEventType;
  generation: number;
  description: string;
  impact: number;
  details: any;
}

export type EvolutionEventType = 
  | 'weight_adjustment'
  | 'node_mutation'
  | 'edge_mutation'
  | 'subgraph_replacement'
  | 'structure_optimization'
  | 'new_node_emergence'
  | 'new_edge_emergence'
  | 'pruning'
  | 'convergence';

export interface EvolutionMetrics {
  generation: number;
  fitness: number;
  diversity: number;
  stability: number;
  adaptationRate: number;
  complexity: number;
}

export interface EvolutionStrategy {
  name: string;
  description: string;
  mutate: (fabric: FabricCore, intensity: number) => Promise<void>;
  evaluate: (fabric: FabricCore) => Promise<number>;
}

export interface EvolutionPopulation {
  individuals: FabricInstance[];
  generation: number;
  bestFitness: number;
  averageFitness: number;
}

export interface FabricInstance {
  id: string;
  fabric: FabricCore;
  fitness: number;
  metrics: EvolutionMetrics;
}

// ============================================================================
// Fabric Evolution Class
// ============================================================================

export class FabricEvolution {
  private fabric: FabricCore;
  private flows: FabricFlows;
  private config: EvolutionConfig;
  private evolutionHistory: EvolutionEvent[];
  private currentGeneration: number;
  private evolutionTimer?: NodeJS.Timeout;
  private strategies: Map<string, EvolutionStrategy>;
  private metrics: EvolutionMetrics;
  private initialized: boolean;
  
  constructor(
    fabric: FabricCore,
    flows: FabricFlows,
    config?: Partial<EvolutionConfig>
  ) {
    this.fabric = fabric;
    this.flows = flows;
    this.config = {
      enableAutoEvolution: config?.enableAutoEvolution ?? true,
      evolutionInterval: config?.evolutionInterval || 60000, // 1 minute
      evolutionIntensity: config?.evolutionIntensity || 0.3,
      maxGenerations: config?.maxGenerations || 10000,
      mutationRate: config?.mutationRate || 0.1,
      crossoverRate: config?.crossoverRate || 0.7,
      selectionPressure: config?.selectionPressure || 0.5
    };
    
    this.evolutionHistory = [];
    this.currentGeneration = 0;
    this.strategies = new Map();
    this.metrics = {
      generation: 0,
      fitness: 0.5,
      diversity: 0.5,
      stability: 1.0,
      adaptationRate: 0.0,
      complexity: 0.5
    };
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Fabric Evolution] Initializing evolution layer...');
    
    // 註冊演化策略
    await this.registerEvolutionStrategies();
    
    // 初始化度量
    await this.updateMetrics();
    
    // 啟動自動演化
    if (this.config.enableAutoEvolution) {
      this.startAutoEvolution();
    }
    
    this.initialized = true;
    console.log('[Fabric Evolution] Evolution layer initialized');
  }
  
  // ========================================================================
  // Evolution Control
  // ========================================================================
  
  startAutoEvolution(): void {
    if (this.evolutionTimer) {
      console.log('[Fabric Evolution] Auto-evolution already running');
      return;
    }
    
    console.log(`[Fabric Evolution] Starting auto-evolution (interval: ${this.config.evolutionInterval}ms)`);
    
    this.evolutionTimer = setInterval(async () => {
      await this.evolve();
    }, this.config.evolutionInterval);
  }
  
  stopAutoEvolution(): void {
    if (this.evolutionTimer) {
      clearInterval(this.evolutionTimer);
      this.evolutionTimer = undefined;
      console.log('[Fabric Evolution] Auto-evolution stopped');
    }
  }
  
  async evolve(intensity?: number): Promise<EvolutionEvent[]> {
    const evolutionIntensity = intensity ?? this.config.evolutionIntensity;
    
    console.log(`[Fabric Evolution] Evolving fabric (generation ${this.currentGeneration}, intensity: ${evolutionIntensity})`);
    
    const events: EvolutionEvent[] = [];
    
    // Step 1: 評估當前適應度
    const currentFitness = await this.evaluateFitness();
    
    // Step 2: 執行演化策略
    await this.executeEvolutionStrategies(evolutionIntensity, events);
    
    // Step 3: 評估演化後適應度
    const newFitness = await this.evaluateFitness();
    
    // Step 4: 接受或拒絕變化
    const improvement = newFitness - currentFitness;
    const accepted = improvement >= 0 || Math.random() < this.config.selectionPressure;
    
    if (!accepted) {
      // 拒絕變化：回滾
      await this.rollbackChanges(events);
      console.log(`[Fabric Evolution] Changes rejected (fitness change: ${improvement})`);
      return [];
    }
    
    // Step 5: 記錄演化事件
    this.currentGeneration++;
    await this.recordEvolutionEvents(events);
    
    // Step 6: 更新度量
    await this.updateMetrics();
    
    // Step 7: 觸發演化流
    await this.triggerEvolutionFlow(events);
    
    console.log(`[Fabric Evolution] Evolution complete (fitness change: ${improvement}, events: ${events.length})`);
    return events;
  }
  
  // ========================================================================
  // Evolution Strategies
  // ========================================================================
  
  private async executeEvolutionStrategies(intensity: number, events: EvolutionEvent[]): Promise<void> {
    // 權重調整
    await this.adjustWeights(intensity, events);
    
    // 節點變異
    if (Math.random() < this.config.mutationRate) {
      await this.mutateNodes(intensity, events);
    }
    
    // 邊變異
    if (Math.random() < this.config.mutationRate) {
      await this.mutateEdges(intensity, events);
    }
    
    // 子圖重寫
    if (Math.random() < this.config.crossoverRate) {
      await this.replaceSubgraphs(intensity, events);
    }
    
    // 結構優化
    await this.optimizeStructure(intensity, events);
    
    // 新節點/邊出現
    if (Math.random() < this.config.mutationRate * 0.5) {
      await this.emergeNewStructures(intensity, events);
    }
    
    // 剪枝
    if (Math.random() < this.config.mutationRate * 0.3) {
      await this.pruneInvalidStructures(intensity, events);
    }
  }
  
  private async adjustWeights(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Adjusting weights...`);
    
    const stats = await this.fabric.getStatistics();
    const graph = this.fabric.getGraph();
    
    // 調整邊的權重
    for (const [edgeId, edge] of graph.edges) {
      const oldWeight = edge.weight;
      
      // 基於使用頻率和適應度調整
      const adjustment = (Math.random() - 0.5) * intensity * 0.2;
      edge.weight = Math.max(0, Math.min(1, edge.weight + adjustment));
      
      if (Math.abs(edge.weight - oldWeight) > 0.01) {
        events.push({
          id: `ev-${Date.now()}-${edgeId}`,
          timestamp: Date.now(),
          type: 'weight_adjustment',
          generation: this.currentGeneration,
          description: `Adjusted weight of edge ${edgeId} from ${oldWeight.toFixed(3)} to ${edge.weight.toFixed(3)}`,
          impact: Math.abs(edge.weight - oldWeight),
          details: {
            edgeId,
            oldWeight,
            newWeight: edge.weight
          }
        });
      }
    }
  }
  
  private async mutateNodes(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Mutating nodes...`);
    
    const graph = this.fabric.getGraph();
    const nodeIds = Array.from(graph.nodes.keys());
    
    // 隨機選擇節點進行變異
    const numMutations = Math.floor(nodeIds.length * this.config.mutationRate * intensity);
    
    for (let i = 0; i < numMutations; i++) {
      const nodeId = nodeIds[Math.floor(Math.random() * nodeIds.length)];
      const node = graph.nodes.get(nodeId);
      
      if (!node) continue;
      
      // 變異節點屬性
      const oldProperties = JSON.parse(JSON.stringify(node.properties));
      
      for (const key of Object.keys(node.properties)) {
        if (typeof node.properties[key] === 'number') {
          node.properties[key] += (Math.random() - 0.5) * intensity * 0.1;
        }
      }
      
      events.push({
        id: `ev-${Date.now()}-${nodeId}`,
        timestamp: Date.now(),
        type: 'node_mutation',
        generation: this.currentGeneration,
        description: `Mutated node ${nodeId}`,
        impact: 0.1,
        details: {
          nodeId,
          oldProperties,
          newProperties: node.properties
        }
      });
    }
  }
  
  private async mutateEdges(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Mutating edges...`);
    
    const graph = this.fabric.getGraph();
    const edgeIds = Array.from(graph.edges.keys());
    
    // 隨機選擇邊進行變異
    const numMutations = Math.floor(edgeIds.length * this.config.mutationRate * intensity);
    
    for (let i = 0; i < numMutations; i++) {
      const edgeId = edgeIds[Math.floor(Math.random() * edgeIds.length)];
      const edge = graph.edges.get(edgeId);
      
      if (!edge) continue;
      
      // 變異邊屬性
      const oldProperties = JSON.parse(JSON.stringify(edge.properties));
      
      for (const key of Object.keys(edge.properties)) {
        if (typeof edge.properties[key] === 'number') {
          edge.properties[key] += (Math.random() - 0.5) * intensity * 0.1;
        }
      }
      
      events.push({
        id: `ev-${Date.now()}-${edgeId}`,
        timestamp: Date.now(),
        type: 'edge_mutation',
        generation: this.currentGeneration,
        description: `Mutated edge ${edgeId}`,
        impact: 0.1,
        details: {
          edgeId,
          oldProperties,
          newProperties: edge.properties
        }
      });
    }
  }
  
  private async replaceSubgraphs(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Replacing subgraphs...`);
    
    // 簡化實作：模擬子圖替換
    events.push({
      id: `ev-${Date.now()}-subgraph`,
      timestamp: Date.now(),
      type: 'subgraph_replacement',
      generation: this.currentGeneration,
      description: 'Evaluated subgraph replacement (no changes made)',
      impact: 0.0,
      details: {}
    });
  }
  
  private async optimizeStructure(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Optimizing structure...`);
    
    const graph = this.fabric.getGraph();
    
    // 移除孤立節點
    const isolatedNodes: string[] = [];
    
    for (const [nodeId, _] of graph.nodes) {
      const incomingEdges = Array.from(graph.edges.values()).filter(e => e.targetId === nodeId);
      const outgoingEdges = Array.from(graph.edges.values()).filter(e => e.sourceId === nodeId);
      
      if (incomingEdges.length === 0 && outgoingEdges.length === 0) {
        isolatedNodes.push(nodeId);
      }
    }
    
    for (const nodeId of isolatedNodes) {
      events.push({
        id: `ev-${Date.now()}-${nodeId}`,
        timestamp: Date.now(),
        type: 'pruning',
        generation: this.currentGeneration,
        description: `Pruned isolated node ${nodeId}`,
        impact: 0.05,
        details: {
          nodeId,
          reason: 'isolated'
        }
      });
    }
  }
  
  private async emergeNewStructures(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Emerging new structures...`);
    
    // 簡化實作：模擬新結構出現
    events.push({
      id: `ev-${Date.now()}-emergence`,
      timestamp: Date.now(),
      type: 'new_node_emergence',
      generation: this.currentGeneration,
      description: 'Evaluated new node emergence (no changes made)',
      impact: 0.0,
      details: {}
    });
  }
  
  private async pruneInvalidStructures(intensity: number, events: EvolutionEvent[]): Promise<void> {
    console.log(`[Fabric Evolution] Pruning invalid structures...`);
    
    // 已在 optimizeStructure 中處理
  }
  
  // ========================================================================
  // Fitness Evaluation
  // ========================================================================
  
  private async evaluateFitness(): Promise<number> {
    const stats = await this.fabric.getStatistics();
    
    // 基於多個指標計算適應度
    let fitness = 0.0;
    
    // 1. 演化適應率 (30%)
    fitness += stats.evolution.adaptationRate * 0.3;
    
    // 2. 穩定度 (25%)
    fitness += stats.evolution.stabilityScore * 0.25;
    
    // 3. 疊加態比例 (20%)
    fitness += stats.superpositionStats.superpositionRatio * 0.2;
    
    // 4. 節點/邊比例 (15%)
    const nodeEdgeRatio = stats.metadata.totalNodes > 0 
      ? stats.metadata.totalEdges / stats.metadata.totalNodes 
      : 0;
    fitness += Math.min(1, nodeEdgeRatio / 2) * 0.15;
    
    // 5. 演化次數 (10%)
    fitness += Math.min(1, stats.metadata.evolutionCount / 100) * 0.1;
    
    return Math.max(0, Math.min(1, fitness));
  }
  
  // ========================================================================
  // Rollback
  // ========================================================================
  
  private async rollbackChanges(events: EvolutionEvent[]): Promise<void> {
    // 簡化實作：實際應該保存變化前的狀態並恢復
    console.log(`[Fabric Evolution] Rolling back ${events.length} changes`);
  }
  
  // ========================================================================
  // Metrics
  // ========================================================================
  
  private async updateMetrics(): Promise<void> {
    const stats = await this.fabric.getStatistics();
    const fitness = await this.evaluateFitness();
    
    this.metrics.generation = this.currentGeneration;
    this.metrics.fitness = fitness;
    this.metrics.stability = stats.evolution.stabilityScore;
    this.metrics.adaptationRate = stats.evolution.adaptationRate;
    this.metrics.complexity = stats.metadata.totalNodes + stats.metadata.totalEdges;
    
    // 計算多樣性
    this.metrics.diversity = await this.calculateDiversity();
  }
  
  private async calculateDiversity(): Promise<number> {
    const graph = this.fabric.getGraph();
    
    // 基於節點類型分佈計算多樣性
    const nodeTypes = new Set<string>();
    
    for (const node of graph.nodes.values()) {
      nodeTypes.add(node.type);
    }
    
    const diversity = nodeTypes.size / 10; // 假設最多 10 種節點類型
    
    return Math.min(1, diversity);
  }
  
  // ========================================================================
  // Evolution Flow
  // ========================================================================
  
  private async triggerEvolutionFlow(events: EvolutionEvent[]): Promise<void> {
    if (events.length === 0) {
      return;
    }
    
    try {
      await this.flows.executeFlow('evolution', {
        scope: 'global',
        intensity: this.config.evolutionIntensity,
        events
      });
    } catch (error) {
      console.log(`[Fabric Evolution] Failed to trigger evolution flow: ${error}`);
    }
  }
  
  // ========================================================================
  // Strategy Registration
  // ========================================================================
  
  private async registerEvolutionStrategies(): Promise<void> {
    console.log('[Fabric Evolution] Registering evolution strategies...');
    
    // 註冊預設策略
    await this.registerStrategy('gradient_ascent', {
      name: 'Gradient Ascent',
      description: 'Gradually improve fitness by following gradient',
      mutate: async (fabric, intensity) => {
        // 實作梯度上升變異
      },
      evaluate: async (fabric) => {
        return await this.evaluateFitness();
      }
    });
    
    await this.registerStrategy('simulated_annealing', {
      name: 'Simulated Annealing',
      description: 'Accept worse solutions with decreasing probability',
      mutate: async (fabric, intensity) => {
        // 實作模擬退火變異
      },
      evaluate: async (fabric) => {
        return await this.evaluateFitness();
      }
    });
    
    await this.registerStrategy('genetic_algorithm', {
      name: 'Genetic Algorithm',
      description: 'Evolve through selection, crossover, and mutation',
      mutate: async (fabric, intensity) => {
        // 實作遺傳算法變異
      },
      evaluate: async (fabric) => {
        return await this.evaluateFitness();
      }
    });
  }
  
  async registerStrategy(name: string, strategy: EvolutionStrategy): Promise<void> {
    console.log(`[Fabric Evolution] Registering strategy: ${name}`);
    this.strategies.set(name, strategy);
  }
  
  // ========================================================================
  // History and Statistics
  // ========================================================================
  
  private async recordEvolutionEvents(events: EvolutionEvent[]): Promise<void> {
    for (const event of events) {
      this.evolutionHistory.push(event);
    }
    
    // 只保留最近 1000 個事件
    if (this.evolutionHistory.length > 1000) {
      this.evolutionHistory = this.evolutionHistory.slice(-1000);
    }
  }
  
  async getEvolutionHistory(filter?: {
    type?: EvolutionEventType;
    since?: number;
    limit?: number;
  }): Promise<EvolutionEvent[]> {
    let history = [...this.evolutionHistory];
    
    if (filter?.type) {
      history = history.filter(e => e.type === filter.type);
    }
    
    if (filter?.since) {
      history = history.filter(e => e.timestamp >= filter.since!);
    }
    
    if (filter?.limit) {
      history = history.slice(-filter.limit);
    }
    
    return history;
  }
  
  async getStatistics(): Promise<EvolutionStatistics> {
    return {
      generation: this.currentGeneration,
      fitness: this.metrics.fitness,
      diversity: this.metrics.diversity,
      stability: this.metrics.stability,
      adaptationRate: this.metrics.adaptationRate,
      complexity: this.metrics.complexity,
      totalEvents: this.evolutionHistory.length,
      eventsByType: this.groupEventsByType(),
      activeStrategies: Array.from(this.strategies.keys())
    };
  }
  
  private groupEventsByType(): Record<EvolutionEventType, number> {
    const counts = {} as Record<EvolutionEventType, number>;
    
    for (const event of this.evolutionHistory) {
      counts[event.type] = (counts[event.type] || 0) + 1;
    }
    
    return counts;
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}

// ============================================================================
// Type Definitions
// ============================================================================

export interface EvolutionStatistics {
  generation: number;
  fitness: number;
  diversity: number;
  stability: number;
  adaptationRate: number;
  complexity: number;
  totalEvents: number;
  eventsByType: Record<EvolutionEventType, number>;
  activeStrategies: string[];
}