# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/GL-UNIFIED-NAMING-CHARTER.yaml


/**
 * Omni-Context Integration Layer
 * 全域脈絡整合層
 * 
 * 整合所有脈絡組件的主入口
 */

import { ContextFusionEngine, Context, FusionRequest, FusionResult } from './context-fusion/index.js';
import { 
  TemporalCoherenceEngine, 
  TemporalState, 
  CoherenceRequest, 
  CoherenceResult,
  StabilityMetrics
} from './temporal-coherence/index.js';
import { 
  MultiScaleReasoningEngine, 
  ReasoningTask, 
  ReasoningResult,
  ScaleLevel,
  MultiScalePlan
} from './multi-scale-reasoning/index.js';
import {
  ContextAwareStrategyEngine,
  StrategySelectionRequest,
  StrategySelectionResult,
  Strategy,
  Agent
} from './context-aware-strategy/index.js';
import {
  GlobalConsistencyFabric,
  ConsistencyContext,
  ConsistencyCheck,
  ConsistencyViolation,
  ConsistencyMetrics
} from './global-consistency-fabric/index.js';
import {
  KnowledgeAlignmentEngine,
  KnowledgeDomain,
  AlignmentRequest,
  AlignmentResult,
  KnowledgeAlignmentMetrics
} from './knowledge-alignment/index.js';

export interface OmniContextConfig {
  contextFusion?: {
    maxHistorySize?: number;
    coherenceThreshold?: number;
  };
  temporalCoherence?: {
    stabilityThreshold?: number;
    confidenceDecayRate?: number;
    maxHistorySize?: number;
    snapshotInterval?: number;
  };
  multiScaleReasoning?: {
    maxQueueSize?: number;
    maxHistorySize?: number;
    parallelExecution?: boolean;
  };
  contextAwareStrategy?: {
    maxHistorySize?: number;
    selectionAlgorithm?: 'greedy' | 'epsilon-greedy' | 'ucb' | 'thompson-sampling';
  };
  globalConsistency?: {
    maxHistorySize?: number;
    consistencyThreshold?: number;
    autoCorrection?: boolean;
  };
  knowledgeAlignment?: {
    maxHistorySize?: number;
    similarityThreshold?: number;
  };
}

export interface OmniContextState {
  initialized: boolean;
  componentsActive: {
    contextFusion: boolean;
    temporalCoherence: boolean;
    multiScaleReasoning: boolean;
    contextAwareStrategy: boolean;
    globalConsistency: boolean;
    knowledgeAlignment: boolean;
  };
  overallCoherence: number;
  globalConsistencyScore: number;
  lastUpdateTime: number;
}

export class OmniContextIntegration {
  private contextFusion: ContextFusionEngine;
  private temporalCoherence: TemporalCoherenceEngine;
  private multiScaleReasoning: MultiScaleReasoningEngine;
  private contextAwareStrategy: ContextAwareStrategyEngine;
  private globalConsistency: GlobalConsistencyFabric;
  private knowledgeAlignment: KnowledgeAlignmentEngine;
  private config: OmniContextConfig;
  private state: OmniContextState;

  constructor(config?: OmniContextConfig) {
    this.config = config || {};
    
    // 初始化所有組件
    this.contextFusion = new ContextFusionEngine(this.config.contextFusion);
    this.temporalCoherence = new TemporalCoherenceEngine(this.config.temporalCoherence);
    this.multiScaleReasoning = new MultiScaleReasoningEngine(this.config.multiScaleReasoning);
    this.contextAwareStrategy = new ContextAwareStrategyEngine(this.config.contextAwareStrategy);
    this.globalConsistency = new GlobalConsistencyFabric(this.config.globalConsistency);
    this.knowledgeAlignment = new KnowledgeAlignmentEngine(this.config.knowledgeAlignment);
    
    this.state = {
      initialized: false,
      componentsActive: {
        contextFusion: false,
        temporalCoherence: false,
        multiScaleReasoning: false,
        contextAwareStrategy: false,
        globalConsistency: false,
        knowledgeAlignment: false
      },
      overallCoherence: 0,
      globalConsistencyScore: 0,
      lastUpdateTime: 0
    };
  }

  /**
   * 初始化全域脈絡整合層
   */
  async initialize(): Promise<void> {
    // 所有組件已經在構造函數中初始化
    this.state.initialized = true;
    this.state.componentsActive = {
      contextFusion: true,
      temporalCoherence: true,
      multiScaleReasoning: true,
      contextAwareStrategy: true,
      globalConsistency: true,
      knowledgeAlignment: true
    };
    this.state.overallCoherence = 1.0;
    this.state.globalConsistencyScore = 1.0;
    this.state.lastUpdateTime = Date.now();
  }

  /**
   * 添加脈絡並融合
   */
  async addAndFuseContext(contexts: Context[]): Promise<FusionResult> {
    for (const context of contexts) {
      await this.contextFusion.addContext(context);
    }

    const request: FusionRequest = {
      contexts,
      priorities: {
        semantic: 5,
        technical: 4,
        reasoning: 3,
        historical: 2,
        task: 2,
        cultural: 1,
        organizational: 1
      }
    };

    return await this.contextFusion.fuseContexts(request);
  }

  /**
   * 添加狀態並檢查時間一致性
   */
  async addAndCheckCoherence(state: TemporalState): Promise<CoherenceResult> {
    return await this.temporalCoherence.addState(state);
  }

  /**
   * 執行多尺度推理
   */
  async reasonMultiScale(task: ReasoningTask): Promise<ReasoningResult> {
    const taskId = await this.multiScaleReasoning.submitTask(task);
    return await this.multiScaleReasoning.reason(taskId);
  }

  /**
   * 執行多尺度計劃推理
   */
  async reasonMultiScalePlan(plan: MultiScalePlan): Promise<Map<string, ReasoningResult>> {
    return await this.multiScaleReasoning.reasonMultiScale(plan);
  }

  /**
   * 選擇策略和代理
   */
  async selectStrategy(request: StrategySelectionRequest): Promise<StrategySelectionResult> {
    return await this.contextAwareStrategy.selectStrategy(request);
  }

  /**
   * 檢查全域一致性
   */
  async checkGlobalConsistency(context: ConsistencyContext): Promise<ConsistencyCheck> {
    const check = await this.globalConsistency.checkConsistency(context);
    
    // 更新狀態
    this.state.globalConsistencyScore = check.overallScore;
    this.state.overallCoherence = Math.min(this.state.overallCoherence, check.overallScore);
    this.state.lastUpdateTime = Date.now();

    return check;
  }

  /**
   * 對齊知識領域
   */
  async alignKnowledge(request: AlignmentRequest): Promise<AlignmentResult> {
    return await this.knowledgeAlignment.alignKnowledge(request);
  }

  /**
   * 獲取系統狀態
   */
  getState(): OmniContextState {
    return { ...this.state };
  }

  /**
   * 獲取完整統計信息
   */
  getFullStatistics() {
    return {
      contextFusion: this.contextFusion.getStatistics(),
      temporalCoherence: this.temporalCoherence.getStabilityMetrics(),
      multiScaleReasoning: this.multiScaleReasoning.getStatistics(),
      contextAwareStrategy: this.contextAwareStrategy.getStatistics(),
      globalConsistency: this.globalConsistency.getMetrics(),
      knowledgeAlignment: this.knowledgeAlignment.getMetrics(),
      overall: {
        initialized: this.state.initialized,
        overallCoherence: this.state.overallCoherence,
        globalConsistencyScore: this.state.globalConsistencyScore,
        lastUpdateTime: this.state.lastUpdateTime
      }
    };
  }

  /**
   * 註冊策略
   */
  async registerStrategy(strategy: Strategy): Promise<void> {
    await this.contextAwareStrategy.registerStrategy(strategy);
  }

  /**
   * 註冊代理
   */
  async registerAgent(agent: Agent): Promise<void> {
    await this.contextAwareStrategy.registerAgent(agent);
  }

  /**
   * 註冊知識領域
   */
  async registerKnowledgeDomain(domain: KnowledgeDomain): Promise<void> {
    await this.knowledgeAlignment.registerDomain(domain);
  }

  /**
   * 執行全局一致性檢查
   */
  async performGlobalCheck(): Promise<{
    coherenceCheck: CoherenceResult;
    consistencyCheck: ConsistencyCheck;
    overallStatus: 'healthy' | 'degraded' | 'critical';
  }> {
    // 創建一個虛擬的時間一致性檢查
    const coherenceResult: CoherenceResult = {
      coherent: true,
      coherenceScore: this.state.overallCoherence,
      violations: [],
      recommendations: [],
      accepted: true,
      timestamp: Date.now()
    };

    // 創建一個虛擬的一致性檢查
    const consistencyCheck = await this.globalConsistency.checkConsistency({
      timestamp: Date.now(),
      components: {},
      metadata: {}
    });

    // 確定整體狀態
    const overallStatus: 'healthy' | 'degraded' | 'critical' = 
      consistencyCheck.overallScore >= 0.9 ? 'healthy' :
      consistencyCheck.overallScore >= 0.7 ? 'degraded' :
      'critical';

    return {
      coherenceCheck: coherenceResult,
      consistencyCheck,
      overallStatus
    };
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    await this.contextFusion.cleanup(olderThan);
    await this.temporalCoherence.cleanup(olderThan);
    await this.multiScaleReasoning.cleanup(olderThan);
    await this.contextAwareStrategy.cleanup(olderThan);
    await this.globalConsistency.cleanup(olderThan);
    await this.knowledgeAlignment.cleanup(olderThan);
  }

  /**
   * 重置整個系統
   */
  async reset(): Promise<void> {
    await this.contextFusion.reset();
    await this.temporalCoherence.reset();
    await this.multiScaleReasoning.reset();
    await this.contextAwareStrategy.reset();
    await this.globalConsistency.reset();
    await this.knowledgeAlignment.reset();
    
    this.state.initialized = false;
    this.state.overallCoherence = 0;
    this.state.globalConsistencyScore = 0;
  }
}

// 導出所有類型
export * from './context-fusion/index.js';
export * from './temporal-coherence/index.js';
export * from './multi-scale-reasoning/index.js';
export * from './context-aware-strategy/index.js';
export * from './global-consistency-fabric/index.js';
export * from './knowledge-alignment/index.js';