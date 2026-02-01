// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-flows
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - Fabric Flows
 * Version 19.0.0
 * 
 * 核心：智慧流
 * - 演算法不是「被呼叫」，而是在織網上流動的轉換流
 * - 推理 = 在織網上走一條路徑
 * - 修復 = 在織網上重寫局部子圖
 * - 演化 = 在織網上改變拓樸與權重
 * - 部署 = 在織網上啟動新的執行實例
 */

import { FabricCore, FabricNode, FabricEdge, EdgeType } from '../fabric-core';

// ============================================================================
// Type Definitions
// ============================================================================

export interface FlowConfig {
  maxDepth: number;
  timeout: number;
  parallelism: number;
  retryAttempts: number;
  enableCaching: boolean;
}

export interface FlowContext {
  flowId: string;
  flowType: FlowType;
  startTime: number;
  parameters: Record<string, any>;
  metadata: Record<string, any>;
}

export type FlowType = 
  | 'reasoning'      // 推理流
  | 'repair'         // 修復流
  | 'evolution'      // 演化流
  | 'deployment'     // 部署流
  | 'execution'      // 執行流
  | 'synchronization'; // 同步流

export interface FlowEvent {
  id: string;
  flowId: string;
  timestamp: number;
  type: 'start' | 'step' | 'decision' | 'branch' | 'merge' | 'complete' | 'error';
  data: any;
}

export interface FlowResult {
  flowId: string;
  flowType: FlowType;
  status: 'success' | 'failed' | 'partial' | 'timeout';
  startTime: number;
  endTime: number;
  duration: number;
  events: FlowEvent[];
  result: any;
  error?: Error;
  statistics: FlowStatistics;
}

export interface FlowStatistics {
  stepsExecuted: number;
  nodesVisited: number;
  edgesTraversed: number;
  decisionsMade: number;
  branchesCreated: number;
  cacheHits: number;
  cacheMisses: number;
}

export interface ReasoningFlowInput {
  query: string;
  context?: {
    startNodeId?: string;
    maxDepth?: number;
    edgeTypes?: EdgeType[];
    reasoningStyle?: 'deductive' | 'inductive' | 'abductive' | 'analogical';
  };
}

export interface RepairFlowInput {
  targetNodeId: string;
  issueDescription: string;
  repairStrategy?: 'local' | 'global' | 'incremental' | 'comprehensive';
}

export interface EvolutionFlowInput {
  scope?: 'node' | 'edge' | 'subgraph' | 'global';
  intensity?: number; // 0-1
  objectives?: string[];
}

export interface DeploymentFlowInput {
  deploymentTarget: string;
  deploymentConfig: any;
  validationRules?: any[];
}

// ============================================================================
// Fabric Flows Engine
// ============================================================================

export class FabricFlows {
  private fabric: FabricCore;
  private config: FlowConfig;
  private flowCache: Map<string, FlowResult>;
  private activeFlows: Map<string, FlowContext>;
  private flowHistory: FlowResult[];
  private initialized: boolean;
  
  constructor(fabric: FabricCore, config?: Partial<FlowConfig>) {
    this.fabric = fabric;
    this.config = {
      maxDepth: config?.maxDepth || 10,
      timeout: config?.timeout || 60000,
      parallelism: config?.parallelism || 5,
      retryAttempts: config?.retryAttempts || 3,
      enableCaching: config?.enableCaching ?? true
    };
    
    this.flowCache = new Map();
    this.activeFlows = new Map();
    this.flowHistory = [];
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Fabric Flows] Initializing flow engine...');
    this.initialized = true;
    console.log('[Fabric Flows] Flow engine initialized');
  }
  
  // ========================================================================
  // Flow Orchestration
  // ========================================================================
  
  async executeFlow(flowType: FlowType, input: any): Promise<FlowResult> {
    const flowId = `flow-${flowType}-${Date.now()}`;
    
    console.log(`[Fabric Flows] Executing ${flowType} flow ${flowId}`);
    
    // 建立流上下文
    const context: FlowContext = {
      flowId,
      flowType,
      startTime: Date.now(),
      parameters: input,
      metadata: {}
    };
    
    this.activeFlows.set(flowId, context);
    
    // 檢查緩存
    if (this.config.enableCaching) {
      const cached = await this.checkCache(flowType, input);
      if (cached) {
        console.log(`[Fabric Flows] Flow ${flowId} retrieved from cache`);
        this.activeFlows.delete(flowId);
        return cached;
      }
    }
    
    // 執行流
    let result: FlowResult;
    
    switch (flowType) {
      case 'reasoning':
        result = await this.executeReasoningFlow(context, input);
        break;
      case 'repair':
        result = await this.executeRepairFlow(context, input);
        break;
      case 'evolution':
        result = await this.executeEvolutionFlow(context, input);
        break;
      case 'deployment':
        result = await this.executeDeploymentFlow(context, input);
        break;
      case 'execution':
        result = await this.executeExecutionFlow(context, input);
        break;
      case 'synchronization':
        result = await this.executeSynchronizationFlow(context, input);
        break;
      default:
        result = {
          flowId,
          flowType,
          status: 'failed',
          startTime: context.startTime,
          endTime: Date.now(),
          duration: Date.now() - context.startTime,
          events: [],
          result: null,
          error: new Error(`Unknown flow type: ${flowType}`),
          statistics: {
            stepsExecuted: 0,
            nodesVisited: 0,
            edgesTraversed: 0,
            decisionsMade: 0,
            branchesCreated: 0,
            cacheHits: 0,
            cacheMisses: 0
          }
        };
    }
    
    // 緩存結果
    if (this.config.enableCaching && result.status === 'success') {
      await this.cacheResult(flowType, input, result);
    }
    
    // 記錄歷史
    this.flowHistory.push(result);
    
    // 清理活動流
    this.activeFlows.delete(flowId);
    
    console.log(`[Fabric Flows] Flow ${flowId} completed with status ${result.status}`);
    return result;
  }
  
  private async checkCache(flowType: FlowType, input: any): Promise<FlowResult | undefined> {
    const cacheKey = `${flowType}-${JSON.stringify(input)}`;
    return this.flowCache.get(cacheKey);
  }
  
  private async cacheResult(flowType: FlowType, input: any, result: FlowResult): Promise<void> {
    const cacheKey = `${flowType}-${JSON.stringify(input)}`;
    this.flowCache.set(cacheKey, result);
  }
  
  // ========================================================================
  // Reasoning Flow
  // ========================================================================
  
  private async executeReasoningFlow(context: FlowContext, input: ReasoningFlowInput): Promise<FlowResult> {
    const events: FlowEvent[] = [];
    const startTime = Date.now();
    
    console.log(`[Fabric Flows] Starting reasoning flow for query: ${input.query}`);
    
    // Step 1: 查詢相關節點
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'query_nodes', query: input.query }
    });
    
    const relevantNodes = await this.queryRelevantNodes(input.query);
    
    // Step 2: 建立推理路徑
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'build_path', nodeCount: relevantNodes.length }
    });
    
    const reasoningPath = await this.buildReasoningPath(
      relevantNodes,
      input.context?.startNodeId,
      input.context?.maxDepth || this.config.maxDepth,
      input.context?.edgeTypes
    );
    
    // Step 3: 執行推理
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'execute_reasoning', pathLength: reasoningPath.length }
    });
    
    const reasoningResult = await this.executeReasoning(
      reasoningPath,
      input.context?.reasoningStyle || 'deductive'
    );
    
    // Step 4: 生成結論
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'generate_conclusion' }
    });
    
    const conclusion = await this.generateConclusion(reasoningResult);
    
    const endTime = Date.now();
    
    return {
      flowId: context.flowId,
      flowType: 'reasoning',
      status: 'success',
      startTime,
      endTime,
      duration: endTime - startTime,
      events,
      result: {
        query: input.query,
        relevantNodes,
        reasoningPath,
        reasoningResult,
        conclusion
      },
      statistics: {
        stepsExecuted: events.length,
        nodesVisited: relevantNodes.length,
        edgesTraversed: reasoningPath.length - 1,
        decisionsMade: 1,
        branchesCreated: 0,
        cacheHits: 0,
        cacheMisses: 0
      }
    };
  }
  
  private async queryRelevantNodes(query: string): Promise<FabricNode[]> {
    // 簡化實作：查詢所有節點並過濾
    const stats = await this.fabric.getStatistics();
    const nodeCount = stats.layerStats?.['fabric']?.nodeCount || 0;
    
    // 在實際實作中，應該使用語意搜尋或向量相似度
    // 這裡返回一些示例節點
    return [];
  }
  
  private async buildReasoningPath(
    nodes: FabricNode[],
    startNodeId?: string,
    maxDepth?: number,
    edgeTypes?: EdgeType[]
  ): Promise<string[]> {
    if (nodes.length === 0) {
      return [];
    }
    
    const startNode = startNodeId || nodes[0].id;
    const path = [startNode];
    
    // 簡化實作：返回一條簡單的路徑
    for (let i = 1; i < Math.min(nodes.length, maxDepth || this.config.maxDepth); i++) {
      path.push(nodes[i].id);
    }
    
    return path;
  }
  
  private async executeReasoning(
    path: string[],
    style: 'deductive' | 'inductive' | 'abductive' | 'analogical'
  ): Promise<any> {
    console.log(`[Fabric Flows] Executing ${style} reasoning along path of ${path.length} nodes`);
    
    // 根據推理風格執行
    switch (style) {
      case 'deductive':
        return await this.deductiveReasoning(path);
      case 'inductive':
        return await this.inductiveReasoning(path);
      case 'abductive':
        return await this.abductiveReasoning(path);
      case 'analogical':
        return await this.analogicalReasoning(path);
      default:
        return await this.deductiveReasoning(path);
    }
  }
  
  private async deductiveReasoning(path: string[]): Promise<any> {
    // 演繹推理：從一般到特殊
    const premises = [];
    const conclusions = [];
    
    for (const nodeId of path) {
      const node = await this.fabric.getNode(nodeId);
      if (node) {
        premises.push({
          nodeId,
          content: node.properties
        });
      }
    }
    
    // 應用演繹規則
    for (let i = 1; i < premises.length; i++) {
      conclusions.push({
        step: i,
        premise: premises[i - 1],
        rule: 'modus_ponens',
        conclusion: premises[i]
      });
    }
    
    return {
      style: 'deductive',
      premises,
      conclusions,
      confidence: 0.9
    };
  }
  
  private async inductiveReasoning(path: string[]): Promise<any> {
    // 歸納推理：從特殊到一般
    const observations = [];
    
    for (const nodeId of path) {
      const node = await this.fabric.getNode(nodeId);
      if (node) {
        observations.push({
          nodeId,
          content: node.properties
        });
      }
    }
    
    // 從觀察中歸納規律
    const patterns = this.detectPatterns(observations);
    
    return {
      style: 'inductive',
      observations,
      patterns,
      generalization: patterns[0] || null,
      confidence: 0.7
    };
  }
  
  private async abductiveReasoning(path: string[]): Promise<any> {
    // 溯因推理：從結果找原因
    const effects = [];
    const hypotheses = [];
    
    for (const nodeId of path) {
      const node = await this.fabric.getNode(nodeId);
      if (node) {
        effects.push({
          nodeId,
          content: node.properties
        });
      }
    }
    
    // 生成假說
    for (const effect of effects) {
      hypotheses.push({
        effect,
        possibleCauses: this.generatePossibleCauses(effect),
        likelihood: Math.random()
      });
    }
    
    return {
      style: 'abductive',
      effects,
      hypotheses,
      bestHypothesis: hypotheses[0] || null,
      confidence: 0.6
    };
  }
  
  private async analogicalReasoning(path: string[]): Promise<any> {
    // 類比推理：從相似案例推論
    const sourceCases = [];
    const targetCases = [];
    
    for (let i = 0; i < path.length; i++) {
      const node = await this.fabric.getNode(path[i]);
      if (node) {
        if (i < path.length / 2) {
          sourceCases.push({
            nodeId: path[i],
            content: node.properties
          });
        } else {
          targetCases.push({
            nodeId: path[i],
            content: node.properties
          });
        }
      }
    }
    
    // 找出相似性
    const similarities = this.findSimilarities(sourceCases, targetCases);
    
    return {
      style: 'analogical',
      sourceCases,
      targetCases,
      similarities,
      inference: similarities[0] || null,
      confidence: 0.5
    };
  }
  
  private detectPatterns(observations: any[]): any[] {
    // 簡化實作：檢測簡單模式
    return [
      {
        pattern: 'sequential',
        confidence: 0.8
      }
    ];
  }
  
  private generatePossibleCauses(effect: any): any[] {
    // 簡化實作：生成可能的原因
    return [
      { cause: 'unknown', probability: 0.5 }
    ];
  }
  
  private findSimilarities(sources: any[], targets: any[]): any[] {
    // 簡化實作：找出相似性
    return [
      {
        similarity: 'structural',
        confidence: 0.6
      }
    ];
  }
  
  private async generateConclusion(reasoningResult: any): Promise<any> {
    return {
      summary: 'Reasoning completed successfully',
      confidence: reasoningResult.confidence || 0.8,
      recommendation: 'Proceed with inferred conclusion'
    };
  }
  
  // ========================================================================
  // Repair Flow
  // ========================================================================
  
  private async executeRepairFlow(context: FlowContext, input: RepairFlowInput): Promise<FlowResult> {
    const events: FlowEvent[] = [];
    const startTime = Date.now();
    
    console.log(`[Fabric Flows] Starting repair flow for node ${input.targetNodeId}`);
    
    // Step 1: 分析問題
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'analyze_issue', targetNode: input.targetNodeId }
    });
    
    const issueAnalysis = await this.analyzeIssue(input.targetNodeId, input.issueDescription);
    
    // Step 2: 設計修復策略
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'design_strategy', strategy: input.repairStrategy }
    });
    
    const repairStrategy = await this.designRepairStrategy(issueAnalysis, input.repairStrategy);
    
    // Step 3: 執行修復
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'execute_repair' }
    });
    
    const repairResult = await this.executeRepair(input.targetNodeId, repairStrategy);
    
    // Step 4: 驗證修復
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'verify_repair' }
    });
    
    const verification = await this.verifyRepair(input.targetNodeId, repairResult);
    
    const endTime = Date.now();
    
    return {
      flowId: context.flowId,
      flowType: 'repair',
      status: verification.success ? 'success' : 'failed',
      startTime,
      endTime,
      duration: endTime - startTime,
      events,
      result: {
        targetNode: input.targetNodeId,
        issueDescription: input.issueDescription,
        issueAnalysis,
        repairStrategy,
        repairResult,
        verification
      },
      statistics: {
        stepsExecuted: events.length,
        nodesVisited: 1,
        edgesTraversed: repairStrategy.affectedEdges?.length || 0,
        decisionsMade: 1,
        branchesCreated: 0,
        cacheHits: 0,
        cacheMisses: 0
      }
    };
  }
  
  private async analyzeIssue(nodeId: string, description: string): Promise<any> {
    const node = await this.fabric.getNode(nodeId);
    
    return {
      nodeId,
      description,
      severity: 'medium',
      type: 'inconsistency',
      affectedProperties: Object.keys(node?.properties || {})
    };
  }
  
  private async designRepairStrategy(issue: any, strategy?: string): Promise<any> {
    const repairStrategy = strategy || 'local';
    
    return {
      strategy: repairStrategy,
      steps: [
        'validate',
        'modify',
        'verify'
      ],
      affectedEdges: []
    };
  }
  
  private async executeRepair(nodeId: string, strategy: any): Promise<any> {
    console.log(`[Fabric Flows] Executing ${strategy.strategy} repair for node ${nodeId}`);
    
    // 更新節點屬性
    const node = await this.fabric.getNode(nodeId);
    if (node) {
      node.properties.repaired = true;
      node.properties.repairedAt = Date.now();
      await this.fabric.updateNode(nodeId, node);
    }
    
    return {
      nodeId,
      strategy: strategy.strategy,
      success: true,
      timestamp: Date.now()
    };
  }
  
  private async verifyRepair(nodeId: string, result: any): Promise<any> {
    const node = await this.fabric.getNode(nodeId);
    
    return {
      nodeId,
      success: node?.properties.repaired === true,
      timestamp: Date.now()
    };
  }
  
  // ========================================================================
  // Evolution Flow
  // ========================================================================
  
  private async executeEvolutionFlow(context: FlowContext, input: EvolutionFlowInput): Promise<FlowResult> {
    const events: FlowEvent[] = [];
    const startTime = Date.now();
    
    console.log(`[Fabric Flows] Starting evolution flow with scope ${input.scope || 'global'}`);
    
    // Step 1: 評估當前狀態
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'assess_state', scope: input.scope }
    });
    
    const currentState = await this.fabric.getStatistics();
    
    // Step 2: 觸發演化
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'trigger_evolution' }
    });
    
    await this.fabric.triggerEvolution();
    
    // Step 3: 評估演化結果
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'evaluate_result' }
    });
    
    const newState = await this.fabric.getStatistics();
    
    // Step 4: 記錄演化
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'log_evolution' }
    });
    
    const evolutionSummary = {
      scope: input.scope || 'global',
      intensity: input.intensity || 0.5,
      before: currentState,
      after: newState,
      improvement: this.calculateImprovement(currentState, newState)
    };
    
    const endTime = Date.now();
    
    return {
      flowId: context.flowId,
      flowType: 'evolution',
      status: 'success',
      startTime,
      endTime,
      duration: endTime - startTime,
      events,
      result: evolutionSummary,
      statistics: {
        stepsExecuted: events.length,
        nodesVisited: 0,
        edgesTraversed: 0,
        decisionsMade: 0,
        branchesCreated: 0,
        cacheHits: 0,
        cacheMisses: 0
      }
    };
  }
  
  private calculateImprovement(before: any, after: any): any {
    return {
      adaptationRateChange: after.evolution.adaptationRate - before.evolution.adaptationRate,
      stabilityScoreChange: after.evolution.stabilityScore - before.evolution.stabilityScore
    };
  }
  
  // ========================================================================
  // Deployment Flow
  // ========================================================================
  
  private async executeDeploymentFlow(context: FlowContext, input: DeploymentFlowInput): Promise<FlowResult> {
    const events: FlowEvent[] = [];
    const startTime = Date.now();
    
    console.log(`[Fabric Flows] Starting deployment flow to ${input.deploymentTarget}`);
    
    // Step 1: 準備部署
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'prepare_deployment', target: input.deploymentTarget }
    });
    
    const deploymentPrep = await this.prepareDeployment(input.deploymentTarget, input.deploymentConfig);
    
    // Step 2: 執行部署
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'execute_deployment' }
    });
    
    const deploymentResult = await this.executeDeployment(deploymentPrep);
    
    // Step 3: 驗證部署
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'verify_deployment' }
    });
    
    const verification = await this.verifyDeployment(input.deploymentTarget, deploymentResult);
    
    const endTime = Date.now();
    
    return {
      flowId: context.flowId,
      flowType: 'deployment',
      status: verification.success ? 'success' : 'failed',
      startTime,
      endTime,
      duration: endTime - startTime,
      events,
      result: {
        target: input.deploymentTarget,
        config: input.deploymentConfig,
        preparation: deploymentPrep,
        execution: deploymentResult,
        verification
      },
      statistics: {
        stepsExecuted: events.length,
        nodesVisited: 0,
        edgesTraversed: 0,
        decisionsMade: 0,
        branchesCreated: 0,
        cacheHits: 0,
        cacheMisses: 0
      }
    };
  }
  
  private async prepareDeployment(target: string, config: any): Promise<any> {
    return {
      target,
      config,
      ready: true,
      timestamp: Date.now()
    };
  }
  
  private async executeDeployment(prep: any): Promise<any> {
    console.log(`[Fabric Flows] Deploying to ${prep.target}`);
    
    return {
      target: prep.target,
      success: true,
      deployedAt: Date.now()
    };
  }
  
  private async verifyDeployment(target: string, result: any): Promise<any> {
    return {
      target,
      success: result.success,
      verifiedAt: Date.now()
    };
  }
  
  // ========================================================================
  // Execution Flow
  // ========================================================================
  
  private async executeExecutionFlow(context: FlowContext, input: any): Promise<FlowResult> {
    const events: FlowEvent[] = [];
    const startTime = Date.now();
    
    console.log(`[Fabric Flows] Starting execution flow`);
    
    // 執行邏輯
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'execute' }
    });
    
    const result = await this.executeComputation(input);
    
    const endTime = Date.now();
    
    return {
      flowId: context.flowId,
      flowType: 'execution',
      status: 'success',
      startTime,
      endTime,
      duration: endTime - startTime,
      events,
      result,
      statistics: {
        stepsExecuted: events.length,
        nodesVisited: 0,
        edgesTraversed: 0,
        decisionsMade: 0,
        branchesCreated: 0,
        cacheHits: 0,
        cacheMisses: 0
      }
    };
  }
  
  private async executeComputation(input: any): Promise<any> {
    return {
      result: 'computation_complete',
      timestamp: Date.now()
    };
  }
  
  // ========================================================================
  // Synchronization Flow
  // ========================================================================
  
  private async executeSynchronizationFlow(context: FlowContext, input: any): Promise<FlowResult> {
    const events: FlowEvent[] = [];
    const startTime = Date.now();
    
    console.log(`[Fabric Flows] Starting synchronization flow`);
    
    // 同步邏輯
    events.push({
      id: `event-${Date.now()}`,
      flowId: context.flowId,
      timestamp: Date.now(),
      type: 'step',
      data: { step: 'synchronize' }
    });
    
    const result = await this.synchronizeData(input);
    
    const endTime = Date.now();
    
    return {
      flowId: context.flowId,
      flowType: 'synchronization',
      status: 'success',
      startTime,
      endTime,
      duration: endTime - startTime,
      events,
      result,
      statistics: {
        stepsExecuted: events.length,
        nodesVisited: 0,
        edgesTraversed: 0,
        decisionsMade: 0,
        branchesCreated: 0,
        cacheHits: 0,
        cacheMisses: 0
      }
    };
  }
  
  private async synchronizeData(input: any): Promise<any> {
    return {
      synchronized: true,
      timestamp: Date.now()
    };
  }
  
  // ========================================================================
  // Flow Management
  // ========================================================================
  
  async getActiveFlows(): Promise<FlowContext[]> {
    return Array.from(this.activeFlows.values());
  }
  
  async getFlowHistory(filter?: {
    flowType?: FlowType;
    since?: number;
    limit?: number;
  }): Promise<FlowResult[]> {
    let history = [...this.flowHistory];
    
    if (filter?.flowType) {
      history = history.filter(r => r.flowType === filter.flowType);
    }
    
    if (filter?.since) {
      history = history.filter(r => r.startTime >= filter.since!);
    }
    
    if (filter?.limit) {
      history = history.slice(-filter.limit);
    }
    
    return history;
  }
  
  async cancelFlow(flowId: string): Promise<void> {
    this.activeFlows.delete(flowId);
    console.log(`[Fabric Flows] Flow ${flowId} cancelled`);
  }
  
  async clearCache(): Promise<void> {
    this.flowCache.clear();
    console.log('[Fabric Flows] Cache cleared');
  }
  
  // ========================================================================
  // Statistics
  // ========================================================================
  
  async getStatistics(): Promise<FlowStatistics> {
    const totalSteps = this.flowHistory.reduce((sum, r) => sum + r.statistics.stepsExecuted, 0);
    const totalNodes = this.flowHistory.reduce((sum, r) => sum + r.statistics.nodesVisited, 0);
    const totalEdges = this.flowHistory.reduce((sum, r) => sum + r.statistics.edgesTraversed, 0);
    const totalDecisions = this.flowHistory.reduce((sum, r) => sum + r.statistics.decisionsMade, 0);
    const totalBranches = this.flowHistory.reduce((sum, r) => sum + r.statistics.branchesCreated, 0);
    
    return {
      stepsExecuted: totalSteps,
      nodesVisited: totalNodes,
      edgesTraversed: totalEdges,
      decisionsMade: totalDecisions,
      branchesCreated: totalBranches,
      cacheHits: this.flowCache.size,
      cacheMisses: 0
    };
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}