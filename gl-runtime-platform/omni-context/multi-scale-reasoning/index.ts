/**
 * Multi-Scale Reasoning Engine
 * 多尺度推理引擎
 * 
 * 功能：同時在微觀、中觀、宏觀、超宏觀四個尺度進行推理
 * 目標：整合版本 9-15 的所有推理能力
 */

export type ScaleLevel = 'micro' | 'meso' | 'macro' | 'hyper';

export interface ReasoningContext {
  id: string;
  scope: string;
  scale: ScaleLevel;
  data: Record<string, any>;
  dependencies?: string[];
  timestamp: number;
}

export interface ReasoningTask {
  id: string;
  type: string;
  priority: number;
  scale: ScaleLevel;
  context: ReasoningContext;
  deadline?: number;
}

export interface ReasoningResult {
  taskId: string;
  scale: ScaleLevel;
  success: boolean;
  result: Record<string, any>;
  confidence: number;
  reasoning: string;
  dependencies: string[];
  crossScaleInsights?: CrossScaleInsight[];
  timestamp: number;
}

export interface CrossScaleInsight {
  sourceScale: ScaleLevel;
  targetScale: ScaleLevel;
  insight: string;
  confidence: number;
  relevance: number;
}

export interface ScaleCapabilities {
  micro: {
    fileLevelReasoning: boolean;
    codeAnalysis: boolean;
    localPatternDetection: boolean;
  };
  meso: {
    projectLevelReasoning: boolean;
    componentIntegration: boolean;
    crossFileConsistency: boolean;
  };
  macro: {
    crossProjectReasoning: boolean;
    federationAnalysis: boolean;
    globalOptimization: boolean;
  };
  hyper: {
    civilizationLevelReasoning: boolean;
    longTermStrategy: boolean;
    emergentBehavior: boolean;
  };
}

export interface MultiScalePlan {
  id: string;
  tasks: ReasoningTask[];
  executionOrder: string[];
  crossScaleDependencies: Map<string, string[]>;
  estimatedCompletion: number;
}

export class MultiScaleReasoningEngine {
  private reasoningQueue: Map<string, ReasoningTask>;
  private results: Map<string, ReasoningResult>;
  private scaleCapabilities: ScaleCapabilities;
  private activeReasonings: Map<string, ReasoningResult>;
  private maxQueueSize: number;
  private maxHistorySize: number;
  private parallelExecution: boolean;

  constructor(options?: {
    maxQueueSize?: number;
    maxHistorySize?: number;
    parallelExecution?: boolean;
  }) {
    this.reasoningQueue = new Map();
    this.results = new Map();
    this.activeReasonings = new Map();
    this.maxQueueSize = options?.maxQueueSize || 100;
    this.maxHistorySize = options?.maxHistorySize || 1000;
    this.parallelExecution = options?.parallelExecution ?? true;
    
    this.scaleCapabilities = {
      micro: {
        fileLevelReasoning: true,
        codeAnalysis: true,
        localPatternDetection: true
      },
      meso: {
        projectLevelReasoning: true,
        componentIntegration: true,
        crossFileConsistency: true
      },
      macro: {
        crossProjectReasoning: true,
        federationAnalysis: true,
        globalOptimization: true
      },
      hyper: {
        civilizationLevelReasoning: true,
        longTermStrategy: true,
        emergentBehavior: true
      }
    };
  }

  /**
   * 提交推理任務
   */
  async submitTask(task: ReasoningTask): Promise<string> {
    const taskId = task.id;
    
    // 檢查隊列大小
    if (this.reasoningQueue.size >= this.maxQueueSize) {
      throw new Error('Reasoning queue is full');
    }

    this.reasoningQueue.set(taskId, task);
    return taskId;
  }

  /**
   * 執行推理（多尺度）
   */
  async reason(taskId: string): Promise<ReasoningResult> {
    const task = this.reasoningQueue.get(taskId);
    
    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }

    // 移動到活躍推理
    this.activeReasonings.set(taskId, {
      taskId,
      scale: task.scale,
      success: false,
      result: {},
      confidence: 0,
      reasoning: '',
      dependencies: task.context.dependencies || [],
      timestamp: Date.now()
    });

    try {
      // 執行指定尺度的推理
      const result = await this.executeScaleReasoning(task);
      
      // 執行跨尺度推理
      const crossScaleInsights = await this.executeCrossScaleReasoning(task, result);
      
      // 合併跨尺度見解
      result.crossScaleInsights = crossScaleInsights;
      
      // 調整信心度
      if (crossScaleInsights.length > 0) {
        result.confidence = Math.min(1, result.confidence + 0.1);
      }

      // 保存結果
      this.results.set(taskId, result);
      
      // 從隊列中移除
      this.reasoningQueue.delete(taskId);
      this.activeReasonings.delete(taskId);
      
      // 維護歷史大小
      this.maintainHistorySize();
      
      return result;
    } catch (error) {
      const errorResult: ReasoningResult = {
        taskId,
        scale: task.scale,
        success: false,
        result: {},
        confidence: 0,
        reasoning: `Error: ${error}`,
        dependencies: task.context.dependencies || [],
        timestamp: Date.now()
      };
      
      this.results.set(taskId, errorResult);
      this.reasoningQueue.delete(taskId);
      this.activeReasonings.delete(taskId);
      
      throw error;
    }
  }

  /**
   * 執行批量推理（多尺度計劃）
   */
  async reasonMultiScale(plan: MultiScalePlan): Promise<Map<string, ReasoningResult>> {
    const results = new Map<string, ReasoningResult>();

    // 按執行順序處理任務
    for (const taskId of plan.executionOrder) {
      try {
        const result = await this.reason(taskId);
        results.set(taskId, result);
      } catch (error) {
        console.error(`Task ${taskId} failed:`, error);
      }
    }

    return results;
  }

  /**
   * 獲取推理結果
   */
  async getResult(taskId: string): Promise<ReasoningResult | null> {
    return this.results.get(taskId) || null;
  }

  /**
   * 查詢結果
   */
  async queryResults(filter: {
    scale?: ScaleLevel;
    type?: string;
    success?: boolean;
    minConfidence?: number;
    timeWindow?: { start: number; end: number };
  }): Promise<ReasoningResult[]> {
    let results = Array.from(this.results.values());

    if (filter.scale) {
      results = results.filter(r => r.scale === filter.scale);
    }

    if (filter.type) {
      results = results.filter(r => r.result.type === filter.type);
    }

    if (filter.success !== undefined) {
      results = results.filter(r => r.success === filter.success);
    }

    if (filter.minConfidence !== undefined) {
      results = results.filter(r => r.confidence >= filter.minConfidence);
    }

    if (filter.timeWindow) {
      results = results.filter(r => 
        r.timestamp >= filter.timeWindow!.start && r.timestamp <= filter.timeWindow!.end
      );
    }

    return results;
  }

  /**
   * 創建多尺度計劃
   */
  async createMultiScalePlan(contexts: ReasoningContext[]): Promise<MultiScalePlan> {
    const planId = `plan-${Date.now()}`;
    const tasks: ReasoningTask[] = [];
    const executionOrder: string[] = [];
    const crossScaleDependencies = new Map<string, string[]>();

    // 按尺度分組
    const groupedByScale = new Map<ScaleLevel, ReasoningContext[]>();
    for (const context of contexts) {
      if (!groupedByScale.has(context.scale)) {
        groupedByScale.set(context.scale, []);
      }
      groupedByScale.get(context.scale)!.push(context);
    }

    // 為每個尺度創建任務
    for (const [scale, scaleContexts] of groupedByScale.entries()) {
      for (let i = 0; i < scaleContexts.length; i++) {
        const context = scaleContexts[i];
        const taskId = `${scale}-${i}-${Date.now()}`;
        
        const task: ReasoningTask = {
          id: taskId,
          type: 'multi-scale-reasoning',
          priority: this.calculatePriority(scale),
          scale,
          context
        };

        tasks.push(task);
        
        // 執行順序：micro -> meso -> macro -> hyper
        if (scale === 'micro') {
          executionOrder.push(taskId);
        } else if (scale === 'meso') {
          executionOrder.push(taskId);
        } else if (scale === 'macro') {
          executionOrder.push(taskId);
        } else if (scale === 'hyper') {
          executionOrder.push(taskId);
        }
      }
    }

    // 建立跨尺度依賴
    this.establishCrossScaleDependencies(tasks, crossScaleDependencies);

    return {
      id: planId,
      tasks,
      executionOrder,
      crossScaleDependencies,
      estimatedCompletion: Date.now() + tasks.length * 5000 // 估算
    };
  }

  /**
   * 獲取尺度能力
   */
  getScaleCapabilities(): ScaleCapabilities {
    return this.scaleCapabilities;
  }

  /**
   * 獲取統計信息
   */
  getStatistics() {
    const allResults = Array.from(this.results.values());
    
    return {
      queueSize: this.reasoningQueue.size,
      activeReasonings: this.activeReasonings.size,
      completedReasonings: allResults.length,
      successRate: allResults.length > 0 
        ? allResults.filter(r => r.success).length / allResults.length 
        : 1.0,
      averageConfidence: allResults.length > 0
        ? allResults.reduce((sum, r) => sum + r.confidence, 0) / allResults.length
        : 0,
      scaleDistribution: this.getScaleDistribution(allResults)
    };
  }

  /**
   * 執行指定尺度的推理
   */
  private async executeScaleReasoning(task: ReasoningTask): Promise<ReasoningResult> {
    const scale = task.scale;
    const context = task.context;

    switch (scale) {
      case 'micro':
        return await this.executeMicroReasoning(task);
      case 'meso':
        return await this.executeMesoReasoning(task);
      case 'macro':
        return await this.executeMacroReasoning(task);
      case 'hyper':
        return await this.executeHyperReasoning(task);
      default:
        throw new Error(`Unknown scale: ${scale}`);
    }
  }

  /**
   * 執行微觀推理（單一檔案）
   */
  private async executeMicroReasoning(task: ReasoningTask): Promise<ReasoningResult> {
    const context = task.context;
    
    // 模擬微觀推理
    const result: ReasoningResult = {
      taskId: task.id,
      scale: 'micro',
      success: true,
      result: {
        scope: context.scope,
        insights: [
          'Identified local code patterns',
          'Detected file-level dependencies',
          'Analyzed function complexity'
        ],
        recommendations: [
          'Optimize function X for better performance',
          'Refactor duplicate code blocks'
        ]
      },
      confidence: 0.85,
      reasoning: 'Micro-scale reasoning completed with file-level analysis',
      dependencies: context.dependencies || [],
      timestamp: Date.now()
    };

    return result;
  }

  /**
   * 執行中觀推理（單一專案）
   */
  private async executeMesoReasoning(task: ReasoningTask): Promise<ReasoningResult> {
    const context = task.context;
    
    // 模擬中觀推理
    const result: ReasoningResult = {
      taskId: task.id,
      scale: 'meso',
      success: true,
      result: {
        scope: context.scope,
        insights: [
          'Analyzed project architecture',
          'Identified component interactions',
          'Detected cross-file consistency issues'
        ],
        recommendations: [
          'Improve module separation',
          'Standardize API interfaces',
          'Enhance error handling across components'
        ]
      },
      confidence: 0.82,
      reasoning: 'Meso-scale reasoning completed with project-level analysis',
      dependencies: context.dependencies || [],
      timestamp: Date.now()
    };

    return result;
  }

  /**
   * 執行宏觀推理（跨專案）
   */
  private async executeMacroReasoning(task: ReasoningTask): Promise<ReasoningResult> {
    const context = task.context;
    
    // 模擬宏觀推理
    const result: ReasoningResult = {
      taskId: task.id,
      scale: 'macro',
      success: true,
      result: {
        scope: context.scope,
        insights: [
          'Analyzed federation architecture',
          'Identified cross-project dependencies',
          'Detected global optimization opportunities'
        ],
        recommendations: [
          'Standardize governance across projects',
          'Implement shared component library',
          'Optimize resource allocation'
        ]
      },
      confidence: 0.78,
      reasoning: 'Macro-scale reasoning completed with cross-project analysis',
      dependencies: context.dependencies || [],
      timestamp: Date.now()
    };

    return result;
  }

  /**
   * 執行超宏觀推理（整個文明層）
   */
  private async executeHyperReasoning(task: ReasoningTask): Promise<ReasoningResult> {
    const context = task.context;
    
    // 模擬超宏觀推理
    const result: ReasoningResult = {
      taskId: task.id,
      scale: 'hyper',
      success: true,
      result: {
        scope: context.scope,
        insights: [
          'Analyzed civilization structure',
          'Identified emergent behaviors',
          'Detected long-term trends'
        ],
        recommendations: [
          'Strengthen civilization governance',
          'Promote knowledge sharing',
          'Plan for sustainable evolution'
        ]
      },
      confidence: 0.75,
      reasoning: 'Hyper-scale reasoning completed with civilization-level analysis',
      dependencies: context.dependencies || [],
      timestamp: Date.now()
    };

    return result;
  }

  /**
   * 執行跨尺度推理
   */
  private async executeCrossScaleReasoning(
    task: ReasoningTask,
    currentResult: ReasoningResult
  ): Promise<CrossScaleInsight[]> {
    const insights: CrossScaleInsight[] = [];
    const currentScale = task.scale;

    // 根據當前尺度查找其他尺度的相關見解
    const otherScales: ScaleLevel[] = ['micro', 'meso', 'macro', 'hyper'].filter(s => s !== currentScale);
    
    for (const otherScale of otherScales) {
      const otherResults = await this.queryResults({
        scale: otherScale,
        success: true,
        minConfidence: 0.7
      });

      // 從其他尺度的結果中提取相關見解
      for (const otherResult of otherResults) {
        const relevance = this.calculateCrossScaleRelevance(currentResult, otherResult);
        
        if (relevance > 0.5) {
          const insight: CrossScaleInsight = {
            sourceScale: otherScale,
            targetScale: currentScale,
            insight: `From ${otherScale}: ${otherResult.reasoning}`,
            confidence: otherResult.confidence,
            relevance
          };

          insights.push(insight);
        }
      }
    }

    // 排序並限制數量
    insights.sort((a, b) => b.relevance - a.relevance);
    return insights.slice(0, 5);
  }

  /**
   * 計算跨尺度相關性
   */
  private calculateCrossScaleRelevance(a: ReasoningResult, b: ReasoningResult): number {
    // 基於依賴關係和主題相關性
    let relevance = 0;

    // 檢查依賴關係
    if (a.dependencies.some(dep => b.dependencies.includes(dep))) {
      relevance += 0.3;
    }

    // 檢查主題相關性（基於推理文本）
    const aKeywords = this.extractKeywords(a.reasoning);
    const bKeywords = this.extractKeywords(b.reasoning);
    const commonKeywords = aKeywords.filter(k => bKeywords.includes(k));
    
    relevance += commonKeywords.length * 0.1;

    return Math.min(1, relevance);
  }

  /**
   * 提取關鍵詞
   */
  private extractKeywords(text: string): string[] {
    const commonWords = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'a', 'an'];
    const words = text.toLowerCase().split(/\W+/);
    return words.filter(w => w.length > 3 && !commonWords.includes(w));
  }

  /**
   * 計算優先級
   */
  private calculatePriority(scale: ScaleLevel): number {
    const priorities: Record<ScaleLevel, number> = {
      micro: 4,
      meso: 3,
      macro: 2,
      hyper: 1
    };
    return priorities[scale];
  }

  /**
   * 建立跨尺度依賴
   */
  private establishCrossScaleDependencies(
    tasks: ReasoningTask[],
    dependencies: Map<string, string[]>
  ): void {
    // micro -> meso -> macro -> hyper
    const scaleOrder: ScaleLevel[] = ['micro', 'meso', 'macro', 'hyper'];

    for (let i = 0; i < tasks.length; i++) {
      const taskA = tasks[i];
      const scaleIndexA = scaleOrder.indexOf(taskA.scale);

      for (let j = 0; j < tasks.length; j++) {
        const taskB = tasks[j];
        const scaleIndexB = scaleOrder.indexOf(taskB.scale);

        // 如果 taskB 的尺度更高，則 taskA 依賴於 taskB
        if (scaleIndexB > scaleIndexA) {
          if (!dependencies.has(taskA.id)) {
            dependencies.set(taskA.id, []);
          }
          dependencies.get(taskA.id)!.push(taskB.id);
        }
      }
    }
  }

  /**
   * 獲取尺度分布
   */
  private getScaleDistribution(results: ReasoningResult[]): Record<string, number> {
    const distribution: Record<string, number> = {
      micro: 0,
      meso: 0,
      macro: 0,
      hyper: 0
    };

    for (const result of results) {
      distribution[result.scale]++;
    }

    return distribution;
  }

  /**
   * 維護歷史大小
   */
  private maintainHistorySize(): void {
    while (this.results.size > this.maxHistorySize) {
      // 刪除最舊的結果
      const oldestKey = Array.from(this.results.keys())[0];
      this.results.delete(oldestKey);
    }
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    const now = Date.now();
    const cutoff = now - olderThan;

    for (const [id, result] of this.results.entries()) {
      if (result.timestamp < cutoff) {
        this.results.delete(id);
      }
    }
  }

  /**
   * 重置引擎
   */
  async reset(): Promise<void> {
    this.reasoningQueue.clear();
    this.results.clear();
    this.activeReasonings.clear();
  }
}