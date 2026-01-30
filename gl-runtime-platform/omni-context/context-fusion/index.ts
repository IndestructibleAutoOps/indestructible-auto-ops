/**
 * Omni-Context Fusion Engine
 * 全域脈絡融合引擎
 * 
 * 功能：整合所有類型的脈絡（技術、語意、歷史、任務、文化、組織、推理）
 * 目標：讓所有代理、策略、推理在同一個脈絡空間中協作
 */

export interface Context {
  id: string;
  type: 'technical' | 'semantic' | 'historical' | 'task' | 'cultural' | 'organizational' | 'reasoning';
  data: Record<string, any>;
  timestamp: number;
  confidence: number;
  source: string;
  metadata?: Record<string, any>;
}

export interface FusedContext {
  id: string;
  primaryContext: Context;
  relatedContexts: Context[];
  fusionScore: number;
  coherence: number;
  completeness: number;
  confidence: number;
  timestamp: number;
  metadata?: Record<string, any>;
}

export interface FusionRequest {
  contexts: Context[];
  priorities?: Record<string, number>;
  filters?: {
    types?: string[];
    confidenceThreshold?: number;
    timeWindow?: { start: number; end: number };
  };
}

export interface FusionResult {
  success: boolean;
  fusedContexts: FusedContext[];
  fusionStatistics: {
    totalContexts: number;
    fusedCount: number;
    averageConfidence: number;
    averageCoherence: number;
    averageCompleteness: number;
  };
  errors?: string[];
}

export class ContextFusionEngine {
  private contexts: Map<string, Context>;
  private fusedContexts: Map<string, FusedContext>;
  private fusionHistory: FusedContext[];
  private maxHistorySize: number;
  private coherenceThreshold: number;

  constructor(options?: {
    maxHistorySize?: number;
    coherenceThreshold?: number;
  }) {
    this.contexts = new Map();
    this.fusedContexts = new Map();
    this.fusionHistory = [];
    this.maxHistorySize = options?.maxHistorySize || 1000;
    this.coherenceThreshold = options?.coherenceThreshold || 0.7;
  }

  /**
   * 添加新脈絡
   */
  async addContext(context: Context): Promise<void> {
    this.contexts.set(context.id, context);
  }

  /**
   * 批量添加脈絡
   */
  async addContexts(contexts: Context[]): Promise<void> {
    for (const context of contexts) {
      await this.addContext(context);
    }
  }

  /**
   * 脈絡融合
   */
  async fuseContexts(request: FusionRequest): Promise<FusionResult> {
    const contexts = this.filterAndPrioritizeContexts(request);
    const fusedContexts: FusedContext[] = [];

    // 按類型分組
    const groupedContexts = this.groupContextsByType(contexts);

    // 對每個組進行融合
    for (const [type, contextsOfType] of groupedContexts.entries()) {
      if (contextsOfType.length === 0) continue;

      // 選擇主脈絡（優先級最高的）
      const primaryContext = this.selectPrimaryContext(contextsOfType, request.priorities);
      
      // 查找相關脈絡
      const relatedContexts = this.findRelatedContexts(primaryContext, contexts);

      // 計算融合分數
      const fusionScore = this.calculateFusionScore(primaryContext, relatedContexts);
      
      // 計算一致性
      const coherence = this.calculateCoherence(primaryContext, relatedContexts);
      
      // 計算完整性
      const completeness = this.calculateCompleteness(primaryContext, relatedContexts);
      
      // 計算信心度
      const confidence = this.calculateConfidence(primaryContext, relatedContexts);

      // 只有在一致性達到閾值時才創建融合脈絡
      if (coherence >= this.coherenceThreshold) {
        const fusedContext: FusedContext = {
          id: this.generateFusionId(primaryContext.id),
          primaryContext,
          relatedContexts,
          fusionScore,
          coherence,
          completeness,
          confidence,
          timestamp: Date.now(),
          metadata: {
            fusionMethod: 'multi-type',
            contextTypes: [primaryContext.type, ...relatedContexts.map(c => c.type)],
          }
        };

        fusedContexts.push(fusedContext);
        this.fusedContexts.set(fusedContext.id, fusedContext);
        this.addToHistory(fusedContext);
      }
    }

    const result: FusionResult = {
      success: fusedContexts.length > 0,
      fusedContexts,
      fusionStatistics: {
        totalContexts: contexts.length,
        fusedCount: fusedContexts.length,
        averageConfidence: fusedContexts.reduce((sum, c) => sum + c.confidence, 0) / fusedContexts.length || 0,
        averageCoherence: fusedContexts.reduce((sum, c) => sum + c.coherence, 0) / fusedContexts.length || 0,
        averageCompleteness: fusedContexts.reduce((sum, c) => sum + c.completeness, 0) / fusedContexts.length || 0,
      }
    };

    return result;
  }

  /**
   * 獲取融合脈絡
   */
  async getFusedContext(id: string): Promise<FusedContext | null> {
    return this.fusedContexts.get(id) || null;
  }

  /**
   * 查詢相關融合脈絡
   */
  async queryFusedContexts(query: {
    type?: string;
    timeWindow?: { start: number; end: number };
    minConfidence?: number;
    minCoherence?: number;
  }): Promise<FusedContext[]> {
    let results = Array.from(this.fusedContexts.values());

    if (query.type) {
      results = results.filter(c => c.primaryContext.type === query.type);
    }

    if (query.timeWindow) {
      results = results.filter(c => 
        c.timestamp >= query.timeWindow!.start && c.timestamp <= query.timeWindow!.end
      );
    }

    if (query.minConfidence !== undefined) {
      results = results.filter(c => c.confidence >= query.minConfidence);
    }

    if (query.minCoherence !== undefined) {
      results = results.filter(c => c.coherence >= query.minCoherence);
    }

    return results;
  }

  /**
   * 過濾和優先級排序脈絡
   */
  private filterAndPrioritizeContexts(request: FusionRequest): Context[] {
    let contexts = Array.from(this.contexts.values());

    // 過濾
    if (request.filters?.types) {
      contexts = contexts.filter(c => request.filters!.types!.includes(c.type));
    }

    if (request.filters?.confidenceThreshold) {
      contexts = contexts.filter(c => c.confidence >= request.filters!.confidenceThreshold!);
    }

    if (request.filters?.timeWindow) {
      contexts = contexts.filter(c => 
        c.timestamp >= request.filters!.timeWindow!.start && 
        c.timestamp <= request.filters!.timeWindow!.end
      );
    }

    // 優先級排序
    if (request.priorities) {
      contexts.sort((a, b) => {
        const priorityA = request.priorities![a.type] || 0;
        const priorityB = request.priorities![b.type] || 0;
        return priorityB - priorityA;
      });
    }

    return contexts;
  }

  /**
   * 按類型分組脈絡
   */
  private groupContextsByType(contexts: Context[]): Map<string, Context[]> {
    const grouped = new Map<string, Context[]>();

    for (const context of contexts) {
      if (!grouped.has(context.type)) {
        grouped.set(context.type, []);
      }
      grouped.get(context.type)!.push(context);
    }

    return grouped;
  }

  /**
   * 選擇主脈絡
   */
  private selectPrimaryContext(contexts: Context[], priorities?: Record<string, number>): Context {
    if (contexts.length === 0) {
      throw new Error('No contexts to select from');
    }

    if (!priorities) {
      return contexts[0];
    }

    // 根據優先級排序
    const sorted = [...contexts].sort((a, b) => {
      const priorityA = priorities[a.type] || 0;
      const priorityB = priorities[b.type] || 0;
      if (priorityA !== priorityB) return priorityB - priorityA;
      return b.confidence - a.confidence;
    });

    return sorted[0];
  }

  /**
   * 查找相關脈絡
   */
  private findRelatedContexts(primary: Context, allContexts: Context[]): Context[] {
    const related: Context[] = [];

    for (const context of allContexts) {
      if (context.id === primary.id) continue;

      // 檢查相似度（基於數據的交集）
      const similarity = this.calculateSimilarity(primary, context);
      
      if (similarity > 0.3) {
        related.push(context);
      }
    }

    return related;
  }

  /**
   * 計算融合分數
   */
  private calculateFusionScore(primary: Context, related: Context[]): number {
    if (related.length === 0) return primary.confidence;

    // 基於信心度、相似度、數量的綜合分數
    const avgConfidence = related.reduce((sum, c) => sum + c.confidence, 0) / related.length;
    const avgSimilarity = related.reduce((sum, c) => sum + this.calculateSimilarity(primary, c), 0) / related.length;
    const diversity = related.length / 10; // 假設最多 10 個相關脈絡

    return (primary.confidence * 0.4 + avgConfidence * 0.3 + avgSimilarity * 0.2 + diversity * 0.1);
  }

  /**
   * 計算一致性
   */
  private calculateCoherence(primary: Context, related: Context[]): number {
    if (related.length === 0) return 1.0;

    // 基於脈絡之間的一致性檢查
    let coherenceSum = 0;
    let comparisons = 0;

    for (const relatedContext of related) {
      const coherence = this.calculateContextCoherence(primary, relatedContext);
      coherenceSum += coherence;
      comparisons++;
    }

    return comparisons > 0 ? coherenceSum / comparisons : 0;
  }

  /**
   * 計算完整性
   */
  private calculateCompleteness(primary: Context, related: Context[]): number {
    // 基於覆蓋的脈絡類型
    const typesCovered = new Set([primary.type, ...related.map(c => c.type)]);
    const allTypes = ['technical', 'semantic', 'historical', 'task', 'cultural', 'organizational', 'reasoning'];
    
    return typesCovered.size / allTypes.length;
  }

  /**
   * 計算信心度
   */
  private calculateConfidence(primary: Context, related: Context[]): number {
    if (related.length === 0) return primary.confidence;

    const allConfidences = [primary.confidence, ...related.map(c => c.confidence)];
    return Math.min(...allConfidences);
  }

  /**
   * 計算兩個脈絡的相似度
   */
  private calculateSimilarity(a: Context, b: Context): number {
    // 基於數據鍵的交集
    const keysA = Object.keys(a.data);
    const keysB = Object.keys(b.data);
    const intersection = keysA.filter(key => keysB.includes(key));

    if (keysA.length === 0 || keysB.length === 0) return 0;

    return (2 * intersection.length) / (keysA.length + keysB.length);
  }

  /**
   * 計算兩個脈絡的一致性
   */
  private calculateContextCoherence(a: Context, b: Context): number {
    // 檢查共同鍵的值是否一致
    const keysA = Object.keys(a.data);
    const keysB = Object.keys(b.data);
    const commonKeys = keysA.filter(key => keysB.includes(key));

    if (commonKeys.length === 0) return 0.5; // 無法判斷，給中性分數

    let coherentCount = 0;
    for (const key of commonKeys) {
      if (a.data[key] === b.data[key]) {
        coherentCount++;
      }
    }

    return coherentCount / commonKeys.length;
  }

  /**
   * 生成融合 ID
   */
  private generateFusionId(primaryId: string): string {
    return `fused-${primaryId}-${Date.now()}`;
  }

  /**
   * 添加到歷史
   */
  private addToHistory(fusedContext: FusedContext): void {
    this.fusionHistory.push(fusedContext);
    
    // 維護歷史大小
    if (this.fusionHistory.length > this.maxHistorySize) {
      this.fusionHistory.shift();
    }
  }

  /**
   * 獲取統計信息
   */
  getStatistics() {
    return {
      totalContexts: this.contexts.size,
      totalFusedContexts: this.fusedContexts.size,
      historySize: this.fusionHistory.length,
      coherenceThreshold: this.coherenceThreshold,
    };
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    const now = Date.now();
    const cutoff = now - olderThan;

    // 清理舊脈絡
    for (const [id, context] of this.contexts.entries()) {
      if (context.timestamp < cutoff) {
        this.contexts.delete(id);
      }
    }

    // 清理舊融合脈絡
    for (const [id, fused] of this.fusedContexts.entries()) {
      if (fused.timestamp < cutoff) {
        this.fusedContexts.delete(id);
      }
    }

    // 清理歷史
    this.fusionHistory = this.fusionHistory.filter(f => f.timestamp >= cutoff);
  }

  /**
   * 重置引擎
   */
  async reset(): Promise<void> {
    this.contexts.clear();
    this.fusedContexts.clear();
    this.fusionHistory = [];
  }
}