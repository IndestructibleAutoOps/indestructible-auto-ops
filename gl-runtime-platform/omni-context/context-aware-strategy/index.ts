/**
 * Context-Aware Strategy Selection Engine
 * 脈絡感知策略選擇引擎
 * 
 * 功能：根據脈絡自動決定代理、策略、推理路徑、演化方向
 * 目標：實現「智慧的穩定性」
 */

export interface ContextSnapshot {
  id: string;
  timestamp: number;
  contextType: string;
  metadata: Record<string, any>;
  features: Record<string, number>;
}

export interface Strategy {
  id: string;
  name: string;
  type: 'collaborative' | 'competitive' | 'adaptive' | 'evolutionary' | 'conservative' | 'aggressive';
  capabilities: string[];
  performanceMetrics: {
    successRate: number;
    averageEfficiency: number;
    averageConfidence: number;
    totalExecutions: number;
  };
  suitabilityFactors: Record<string, number>;
  metadata?: Record<string, any>;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  currentLoad: number;
  performanceMetrics: {
    tasksCompleted: number;
    successRate: number;
    averageTaskTime: number;
  };
  metadata?: Record<string, any>;
}

export interface StrategySelectionRequest {
  taskId: string;
  taskType: string;
  context: ContextSnapshot;
  requirements?: {
    capabilities?: string[];
    constraints?: Record<string, any>;
    preferences?: Record<string, any>;
  };
  timeConstraints?: {
    deadline?: number;
    maxExecutionTime?: number;
  };
}

export interface StrategySelectionResult {
  taskId: string;
  selectedStrategy: Strategy;
  selectedAgents: Agent[];
  reasoningPath: string;
  confidence: number;
  alternatives: Strategy[];
  timestamp: number;
}

export interface StrategyPerformance {
  strategyId: string;
  contextType: string;
  success: boolean;
  efficiency: number;
  confidence: number;
  timestamp: number;
}

export class ContextAwareStrategyEngine {
  private strategies: Map<string, Strategy>;
  private agents: Map<string, Agent>;
  private performanceHistory: StrategyPerformance[];
  private contextHistory: ContextSnapshot[];
  private maxHistorySize: number;
  private selectionAlgorithm: 'greedy' | 'epsilon-greedy' | 'ucb' | 'thompson-sampling';

  constructor(options?: {
    maxHistorySize?: number;
    selectionAlgorithm?: 'greedy' | 'epsilon-greedy' | 'ucb' | 'thompson-sampling';
  }) {
    this.strategies = new Map();
    this.agents = new Map();
    this.performanceHistory = [];
    this.contextHistory = [];
    this.maxHistorySize = options?.maxHistorySize || 10000;
    this.selectionAlgorithm = options?.selectionAlgorithm || 'ucb';

    // 初始化默認策略
    this.initializeDefaultStrategies();
    this.initializeDefaultAgents();
  }

  /**
   * 註冊策略
   */
  async registerStrategy(strategy: Strategy): Promise<void> {
    this.strategies.set(strategy.id, strategy);
  }

  /**
   * 註冊代理
   */
  async registerAgent(agent: Agent): Promise<void> {
    this.agents.set(agent.id, agent);
  }

  /**
   * 選擇策略和代理
   */
  async selectStrategy(request: StrategySelectionRequest): Promise<StrategySelectionResult> {
    // 記錄上下文
    this.contextHistory.push(request.context);
    this.maintainHistorySize();

    // 1. 過濾合適的策略
    const suitableStrategies = this.filterSuitableStrategies(request);

    if (suitableStrategies.length === 0) {
      throw new Error('No suitable strategies found for the given context');
    }

    // 2. 根據選擇算法選擇策略
    const selectedStrategy = this.applySelectionAlgorithm(suitableStrategies, request);

    // 3. 選擇合適的代理
    const selectedAgents = await this.selectAgents(selectedStrategy, request);

    // 4. 推導推理路徑
    const reasoningPath = this.deriveReasoningPath(selectedStrategy, selectedAgents, request);

    // 5. 計算信心度
    const confidence = this.calculateSelectionConfidence(selectedStrategy, selectedAgents, request);

    // 6. 提供替代方案
    const alternatives = this.getAlternativeStrategies(suitableStrategies, selectedStrategy, 3);

    return {
      taskId: request.taskId,
      selectedStrategy,
      selectedAgents,
      reasoningPath,
      confidence,
      alternatives,
      timestamp: Date.now()
    };
  }

  /**
   * 記錄策略執行結果
   */
  async recordPerformance(performance: StrategyPerformance): Promise<void> {
    this.performanceHistory.push(performance);
    
    // 更新策略性能指標
    const strategy = this.strategies.get(performance.strategyId);
    if (strategy) {
      strategy.performanceMetrics.totalExecutions++;
      strategy.performanceMetrics.successRate = 
        (strategy.performanceMetrics.successRate * (strategy.performanceMetrics.totalExecutions - 1) + 
         (performance.success ? 1 : 0)) / 
        strategy.performanceMetrics.totalExecutions;
      strategy.performanceMetrics.averageEfficiency = 
        (strategy.performanceMetrics.averageEfficiency * (strategy.performanceMetrics.totalExecutions - 1) + 
         performance.efficiency) / 
        strategy.performanceMetrics.totalExecutions;
      strategy.performanceMetrics.averageConfidence = 
        (strategy.performanceMetrics.averageConfidence * (strategy.performanceMetrics.totalExecutions - 1) + 
         performance.confidence) / 
        strategy.performanceMetrics.totalExecutions;
    }

    this.maintainHistorySize();
  }

  /**
   * 獲取策略
   */
  async getStrategy(id: string): Promise<Strategy | null> {
    return this.strategies.get(id) || null;
  }

  /**
   * 獲取代理
   */
  async getAgent(id: string): Promise<Agent | null> {
    return this.agents.get(id) || null;
  }

  /**
   * 查詢策略
   */
  async queryStrategies(filter: {
    type?: string;
    minSuccessRate?: number;
    capabilities?: string[];
  }): Promise<Strategy[]> {
    let strategies = Array.from(this.strategies.values());

    if (filter.type) {
      strategies = strategies.filter(s => s.type === filter.type);
    }

    if (filter.minSuccessRate !== undefined) {
      strategies = strategies.filter(s => s.performanceMetrics.successRate >= filter.minSuccessRate);
    }

    if (filter.capabilities) {
      strategies = strategies.filter(s => 
        filter.capabilities!.every(cap => s.capabilities.includes(cap))
      );
    }

    return strategies;
  }

  /**
   * 獲取統計信息
   */
  getStatistics() {
    const allStrategies = Array.from(this.strategies.values());
    const allAgents = Array.from(this.agents.values());

    return {
      totalStrategies: this.strategies.size,
      totalAgents: this.agents.size,
      averageStrategySuccessRate: allStrategies.length > 0
        ? allStrategies.reduce((sum, s) => sum + s.performanceMetrics.successRate, 0) / allStrategies.length
        : 0,
      averageAgentSuccessRate: allAgents.length > 0
        ? allAgents.reduce((sum, a) => sum + a.performanceMetrics.successRate, 0) / allAgents.length
        : 0,
      performanceHistorySize: this.performanceHistory.length,
      contextHistorySize: this.contextHistory.length
    };
  }

  /**
   * 初始化默認策略
   */
  private initializeDefaultStrategies(): void {
    const defaultStrategies: Strategy[] = [
      {
        id: 'collaborative-consensus',
        name: 'Collaborative Consensus',
        type: 'collaborative',
        capabilities: ['multi-agent', 'consensus', 'communication'],
        performanceMetrics: {
          successRate: 0.88,
          averageEfficiency: 0.75,
          averageConfidence: 0.82,
          totalExecutions: 45
        },
        suitabilityFactors: {
          teamSize: 0.9,
          complexity: 0.7,
          timeConstraint: 0.6,
          qualityRequirement: 0.9
        }
      },
      {
        id: 'data-driven-analysis',
        name: 'Data-Driven Analysis',
        type: 'adaptive',
        capabilities: ['analytics', 'pattern-recognition', 'data-processing'],
        performanceMetrics: {
          successRate: 0.92,
          averageEfficiency: 0.85,
          averageConfidence: 0.88,
          totalExecutions: 128
        },
        suitabilityFactors: {
          dataAvailability: 0.95,
          complexity: 0.8,
          timeConstraint: 0.7,
          qualityRequirement: 0.85
        }
      },
      {
        id: 'value-aligned-selection',
        name: 'Value-Aligned Selection',
        type: 'conservative',
        capabilities: ['value-alignment', 'governance', 'semantic-validation'],
        performanceMetrics: {
          successRate: 0.90,
          averageEfficiency: 0.78,
          averageConfidence: 0.86,
          totalExecutions: 89
        },
        suitabilityFactors: {
          governanceRequirement: 0.95,
          complexity: 0.6,
          timeConstraint: 0.5,
          qualityRequirement: 0.9
        }
      },
      {
        id: 'adaptive-iteration',
        name: 'Adaptive Iteration',
        type: 'adaptive',
        capabilities: ['iteration', 'optimization', 'feedback'],
        performanceMetrics: {
          successRate: 0.85,
          averageEfficiency: 0.70,
          averageConfidence: 0.80,
          totalExecutions: 67
        },
        suitabilityFactors: {
          uncertainty: 0.9,
          complexity: 0.8,
          timeConstraint: 0.4,
          qualityRequirement: 0.8
        }
      },
      {
        id: 'evolutionary-exploration',
        name: 'Evolutionary Exploration',
        type: 'evolutionary',
        capabilities: ['evolution', 'mutation', 'optimization'],
        performanceMetrics: {
          successRate: 0.82,
          averageEfficiency: 0.65,
          averageConfidence: 0.75,
          totalExecutions: 34
        },
        suitabilityFactors: {
          innovation: 0.95,
          complexity: 0.9,
          timeConstraint: 0.3,
          qualityRequirement: 0.7
        }
      }
    ];

    for (const strategy of defaultStrategies) {
      this.strategies.set(strategy.id, strategy);
    }
  }

  /**
   * 初始化默認代理
   */
  private initializeDefaultAgents(): void {
    const defaultAgents: Agent[] = [
      {
        id: 'agent-alpha',
        name: 'Pipeline Specialist Alpha',
        role: 'Pipeline Specialist',
        capabilities: ['pipeline-execution', 'workflow-management', 'task-orchestration'],
        currentLoad: 0.3,
        performanceMetrics: {
          tasksCompleted: 45,
          successRate: 0.94,
          averageTaskTime: 3200
        }
      },
      {
        id: 'agent-beta',
        name: 'Schema Validator Beta',
        role: 'Schema Validator',
        capabilities: ['schema-validation', 'semantic-checking', 'format-verification'],
        currentLoad: 0.5,
        performanceMetrics: {
          tasksCompleted: 128,
          successRate: 0.95,
          averageTaskTime: 1500
        }
      },
      {
        id: 'agent-gamma',
        name: 'Semantic Analyst Gamma',
        role: 'Semantic Analyst',
        capabilities: ['semantic-analysis', 'context-understanding', 'meaning-extraction'],
        currentLoad: 0.4,
        performanceMetrics: {
          tasksCompleted: 89,
          successRate: 0.94,
          averageTaskTime: 2800
        }
      },
      {
        id: 'agent-delta',
        name: 'Federation Coordinator Delta',
        role: 'Federation Coordinator',
        capabilities: ['federation-management', 'cross-repo-orchestration', 'distributed-execution'],
        currentLoad: 0.2,
        performanceMetrics: {
          tasksCompleted: 67,
          successRate: 0.94,
          averageTaskTime: 4500
        }
      },
      {
        id: 'agent-epsilon',
        name: 'DAG Optimizer Epsilon',
        role: 'DAG Optimizer',
        capabilities: ['dag-optimization', 'dependency-analysis', 'parallel-execution'],
        currentLoad: 0.6,
        performanceMetrics: {
          tasksCompleted: 34,
          successRate: 0.94,
          averageTaskTime: 3800
        }
      }
    ];

    for (const agent of defaultAgents) {
      this.agents.set(agent.id, agent);
    }
  }

  /**
   * 過濾合適的策略
   */
  private filterSuitableStrategies(request: StrategySelectionRequest): Strategy[] {
    let strategies = Array.from(this.strategies.values());

    // 過濾能力要求
    if (request.requirements?.capabilities) {
      strategies = strategies.filter(s =>
        request.requirements!.capabilities!.every(cap => s.capabilities.includes(cap))
      );
    }

    // 過濾約束條件
    if (request.requirements?.constraints) {
      // 可以添加更具體的約束檢查邏輯
    }

    return strategies;
  }

  /**
   * 應用選擇算法
   */
  private applySelectionAlgorithm(strategies: Strategy[], request: StrategySelectionRequest): Strategy {
    switch (this.selectionAlgorithm) {
      case 'greedy':
        return this.greedySelection(strategies, request);
      case 'epsilon-greedy':
        return this.epsilonGreedySelection(strategies, request);
      case 'ucb':
        return this.ucbSelection(strategies, request);
      case 'thompson-sampling':
        return this.thompsonSamplingSelection(strategies, request);
      default:
        return this.greedySelection(strategies, request);
    }
  }

  /**
   * 貪心選擇
   */
  private greedySelection(strategies: Strategy[], request: StrategySelectionRequest): Strategy {
    // 基於成功率、效率、適應性的綜合評分
    return strategies.reduce((best, current) => {
      const bestScore = this.calculateStrategyScore(best, request);
      const currentScore = this.calculateStrategyScore(current, request);
      return currentScore > bestScore ? current : best;
    });
  }

  /**
   * Epsilon-Greedy 選擇
   */
  private epsilonGreedySelection(strategies: Strategy[], request: StrategySelectionRequest): Strategy {
    const epsilon = 0.1;

    if (Math.random() < epsilon) {
      // 隨機探索
      return strategies[Math.floor(Math.random() * strategies.length)];
    } else {
      return this.greedySelection(strategies, request);
    }
  }

  /**
   * UCB (Upper Confidence Bound) 選擇
   */
  private ucbSelection(strategies: Strategy[], request: StrategySelectionRequest): Strategy {
    return strategies.reduce((best, current) => {
      const bestScore = this.calculateUCBScore(best);
      const currentScore = this.calculateUCBScore(current);
      return currentScore > bestScore ? current : best;
    });
  }

  /**
   * Thompson Sampling 選擇
   */
  private thompsonSamplingSelection(strategies: Strategy[], request: StrategySelectionRequest): Strategy {
    let bestStrategy = strategies[0];
    let bestSample = 0;

    for (const strategy of strategies) {
      // 使用 Beta 分佈採樣
      const alpha = strategy.performanceMetrics.totalExecutions * strategy.performanceMetrics.successRate + 1;
      const beta = strategy.performanceMetrics.totalExecutions * (1 - strategy.performanceMetrics.successRate) + 1;
      const sample = this.sampleBeta(alpha, beta);

      if (sample > bestSample) {
        bestSample = sample;
        bestStrategy = strategy;
      }
    }

    return bestStrategy;
  }

  /**
   * 選擇代理
   */
  private async selectAgents(strategy: Strategy, request: StrategySelectionRequest): Promise<Agent[]> {
    const selectedAgents: Agent[] = [];
    const requiredCapabilities = strategy.capabilities;

    // 按性能排序代理
    const sortedAgents = Array.from(this.agents.values()).sort((a, b) => {
      const scoreA = a.performanceMetrics.successRate - a.currentLoad;
      const scoreB = b.performanceMetrics.successRate - b.currentLoad;
      return scoreB - scoreA;
    });

    // 為每個所需能力選擇最佳代理
    for (const capability of requiredCapabilities) {
      const bestAgent = sortedAgents.find(a => 
        a.capabilities.includes(capability) && 
        a.currentLoad < 0.8 &&
        !selectedAgents.includes(a)
      );

      if (bestAgent) {
        selectedAgents.push(bestAgent);
      }
    }

    return selectedAgents;
  }

  /**
   * 推導推理路徑
   */
  private deriveReasoningPath(
    strategy: Strategy,
    agents: Agent[],
    request: StrategySelectionRequest
  ): string {
    const path = [
      `Context: ${request.context.contextType}`,
      `Strategy: ${strategy.name} (${strategy.type})`,
      `Agents: ${agents.map(a => a.name).join(', ')}`,
      `Reasoning: Apply ${strategy.capabilities.join(' → ')}`
    ];

    return path.join('\n');
  }

  /**
   * 計算選擇信心度
   */
  private calculateSelectionConfidence(
    strategy: Strategy,
    agents: Agent[],
    request: StrategySelectionRequest
  ): number {
    // 基於策略性能和代理性能
    const strategyConfidence = strategy.performanceMetrics.successRate * 0.6;
    const agentConfidence = agents.length > 0
      ? agents.reduce((sum, a) => sum + a.performanceMetrics.successRate, 0) / agents.length * 0.4
      : 0;

    return Math.min(1, strategyConfidence + agentConfidence);
  }

  /**
   * 獲取替代策略
   */
  private getAlternativeStrategies(
    strategies: Strategy[],
    selected: Strategy,
    count: number
  ): Strategy[] {
    return strategies
      .filter(s => s.id !== selected.id)
      .sort((a, b) => b.performanceMetrics.successRate - a.performanceMetrics.successRate)
      .slice(0, count);
  }

  /**
   * 計算策略分數
   */
  private calculateStrategyScore(strategy: Strategy, request: StrategySelectionRequest): number {
    // 基於成功率、效率、適應性的加權分數
    const successRate = strategy.performanceMetrics.successRate;
    const efficiency = strategy.performanceMetrics.averageEfficiency;
    const confidence = strategy.performanceMetrics.averageConfidence;

    // 檢查適應性因素
    let suitabilityScore = 0;
    for (const [factor, weight] of Object.entries(strategy.suitabilityFactors)) {
      if (request.context.features[factor] !== undefined) {
        suitabilityScore += request.context.features[factor] * weight;
      }
    }

    return successRate * 0.4 + efficiency * 0.3 + confidence * 0.2 + suitabilityScore * 0.1;
  }

  /**
   * 計算 UCB 分數
   */
  private calculateUCBScore(strategy: Strategy): number {
    const n = strategy.performanceMetrics.totalExecutions;
    if (n === 0) return Infinity;

    const mean = strategy.performanceMetrics.successRate;
    const c = 1.0; // 探索常數
    const totalPulls = Array.from(this.strategies.values())
      .reduce((sum, s) => sum + s.performanceMetrics.totalExecutions, 0);

    return mean + c * Math.sqrt(Math.log(totalPulls) / n);
  }

  /**
   * Beta 分佈採樣
   */
  private sampleBeta(alpha: number, beta: number): number {
    // 使用 Gamma 分佈的簡單近似
    const sampleGamma = (shape: number): number => {
      if (shape > 1) {
        const d = shape - 1 / 3;
        const c = 1 / Math.sqrt(9 * d);
        while (true) {
          let x, v;
          do {
            x = this.normalRandom();
            v = 1 + c * x;
          } while (v <= 0);
          v = v * v * v;
          const u = Math.random();
          if (u < 1 - 0.0331 * (x * x) * (x * x)) {
            return d * v;
          }
          if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) {
            return d * v;
          }
        }
      } else {
        const u = Math.random();
        return Math.pow(u, 1 / shape);
      }
    };

    const x = sampleGamma(alpha);
    const y = sampleGamma(beta);
    return x / (x + y);
  }

  /**
   * 標準正態分佈隨機數
   */
  private normalRandom(): number {
    let u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  }

  /**
   * 維護歷史大小
   */
  private maintainHistorySize(): void {
    while (this.contextHistory.length > this.maxHistorySize) {
      this.contextHistory.shift();
    }
    while (this.performanceHistory.length > this.maxHistorySize) {
      this.performanceHistory.shift();
    }
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    const now = Date.now();
    const cutoff = now - olderThan;

    this.contextHistory = this.contextHistory.filter(c => c.timestamp >= cutoff);
    this.performanceHistory = this.performanceHistory.filter(p => p.timestamp >= cutoff);
  }

  /**
   * 重置引擎
   */
  async reset(): Promise<void> {
    this.strategies.clear();
    this.agents.clear();
    this.performanceHistory = [];
    this.contextHistory = [];
    
    // 重新初始化默認策略和代理
    this.initializeDefaultStrategies();
    this.initializeDefaultAgents();
  }
}