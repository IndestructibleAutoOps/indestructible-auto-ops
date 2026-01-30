/**
 * Global Consistency Fabric
 * 全域一致性織網
 * 
 * 功能：確保語意、推理、策略、演化、文明規則的一致性
 * 目標：實現「智慧的連續性」
 */

export interface ConsistencyRule {
  id: string;
  name: string;
  type: 'semantic' | 'reasoning' | 'strategy' | 'evolution' | 'civilization' | 'cross-domain';
  priority: number;
  description: string;
  validation: (context: ConsistencyContext) => boolean;
  recommendation?: (violation: ConsistencyViolation) => string[];
}

export interface ConsistencyContext {
  timestamp: number;
  components: {
    semantic?: any;
    reasoning?: any;
    strategy?: any;
    evolution?: any;
    civilization?: any;
  };
  metadata?: Record<string, any>;
}

export interface ConsistencyViolation {
  ruleId: string;
  ruleName: string;
  ruleType: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  affectedComponents: string[];
  recommendations: string[];
  timestamp: number;
}

export interface ConsistencyCheck {
  id: string;
  timestamp: number;
  context: ConsistencyContext;
  violations: ConsistencyViolation[];
  overallScore: number;
  status: 'consistent' | 'inconsistent' | 'degraded';
  recommendations: string[];
}

export interface ConsistencySnapshot {
  id: string;
  timestamp: number;
  check: ConsistencyCheck;
  previousSnapshotId?: string;
  delta: ConsistencyDelta;
}

export interface ConsistencyDelta {
  newViolations: ConsistencyViolation[];
  resolvedViolations: ConsistencyViolation[];
  scoreChange: number;
  statusChange?: 'improved' | 'degraded' | 'stable';
}

export interface ConsistencyMetrics {
  overallScore: number;
  ruleViolations: number;
  criticalViolations: number;
  componentScores: Record<string, number>;
  trend: number[];
  averageResolutionTime: number;
}

export class GlobalConsistencyFabric {
  private rules: Map<string, ConsistencyRule>;
  private checkHistory: ConsistencyCheck[];
  private snapshots: Map<string, ConsistencySnapshot>;
  private activeViolations: Map<string, ConsistencyViolation>;
  private maxHistorySize: number;
  private consistencyThreshold: number;
  private autoCorrection: boolean;

  constructor(options?: {
    maxHistorySize?: number;
    consistencyThreshold?: number;
    autoCorrection?: boolean;
  }) {
    this.rules = new Map();
    this.checkHistory = [];
    this.snapshots = new Map();
    this.activeViolations = new Map();
    this.maxHistorySize = options?.maxHistorySize || 1000;
    this.consistencyThreshold = options?.consistencyThreshold || 0.8;
    this.autoCorrection = options?.autoCorrection ?? false;

    // 初始化默認規則
    this.initializeDefaultRules();
  }

  /**
   * 註冊一致性規則
   */
  async registerRule(rule: ConsistencyRule): Promise<void> {
    this.rules.set(rule.id, rule);
  }

  /**
   * 執行一致性檢查
   */
  async checkConsistency(context: ConsistencyContext): Promise<ConsistencyCheck> {
    const violations: ConsistencyViolation[] = [];

    // 檢查所有規則
    for (const [ruleId, rule] of this.rules.entries()) {
      try {
        const isValid = rule.validation(context);

        if (!isValid) {
          const violation: ConsistencyViolation = {
            ruleId,
            ruleName: rule.name,
            ruleType: rule.type,
            severity: this.calculateSeverity(rule, context),
            description: rule.description,
            affectedComponents: this.getAffectedComponents(rule, context),
            recommendations: rule.recommendation ? rule.recommendation(this.createViolationContext(rule, context)) : [],
            timestamp: Date.now()
          };

          violations.push(violation);
          this.activeViolations.set(`${ruleId}-${Date.now()}`, violation);
        }
      } catch (error) {
        console.error(`Error validating rule ${ruleId}:`, error);
      }
    }

    // 計算整體分數
    const overallScore = this.calculateOverallScore(violations);

    // 確定狀態
    const status = this.determineStatus(overallScore);

    // 生成建議
    const recommendations = this.generateRecommendations(violations, status);

    // 創建檢查結果
    const check: ConsistencyCheck = {
      id: `check-${Date.now()}`,
      timestamp: Date.now(),
      context,
      violations,
      overallScore,
      status,
      recommendations
    };

    // 添加到歷史
    this.checkHistory.push(check);
    this.maintainHistorySize();

    // 創建快照
    await this.createSnapshot(check);

    // 自動修正（如果啟用）
    if (this.autoCorrection && status !== 'consistent') {
      await this.autoCorrect(violations);
    }

    return check;
  }

  /**
   * 獲取主動違規
   */
  async getActiveViolations(): Promise<ConsistencyViolation[]> {
    return Array.from(this.activeViolations.values());
  }

  /**
   * 解決違規
   */
  async resolveViolation(violationId: string): Promise<boolean> {
    return this.activeViolations.delete(violationId);
  }

  /**
   * 獲取一致性指標
   */
  getMetrics(): ConsistencyMetrics {
    const recentChecks = this.checkHistory.slice(-20);

    if (recentChecks.length === 0) {
      return {
        overallScore: 1.0,
        ruleViolations: 0,
        criticalViolations: 0,
        componentScores: {},
        trend: [],
        averageResolutionTime: 0
      };
    }

    const overallScore = recentChecks[recentChecks.length - 1].overallScore;
    const ruleViolations = this.activeViolations.size;
    const criticalViolations = Array.from(this.activeViolations.values())
      .filter(v => v.severity === 'critical').length;

    // 計算組件分數
    const componentScores: Record<string, number> = {};
    const lastCheck = recentChecks[recentChecks.length - 1];
    
    for (const [component, data] of Object.entries(lastCheck.context.components)) {
      componentScores[component] = this.calculateComponentScore(component, lastCheck);
    }

    // 計算趨勢
    const trend = recentChecks.map(check => check.overallScore);

    // 計算平均解決時間（簡化）
    const averageResolutionTime = 3600000; // 1 小時

    return {
      overallScore,
      ruleViolations,
      criticalViolations,
      componentScores,
      trend,
      averageResolutionTime
    };
  }

  /**
   * 獲取快照
   */
  async getSnapshot(snapshotId: string): Promise<ConsistencySnapshot | null> {
    return this.snapshots.get(snapshotId) || null;
  }

  /**
   * 恢復快照
   */
  async restoreSnapshot(snapshotId: string): Promise<boolean> {
    const snapshot = this.snapshots.get(snapshotId);
    
    if (!snapshot) {
      return false;
    }

    // 重新執行檢查以恢復狀態
    await this.checkConsistency(snapshot.context);

    return true;
  }

  /**
   * 初始化默認規則
   */
  private initializeDefaultRules(): void {
    const defaultRules: ConsistencyRule[] = [
      {
        id: 'semantic-consistency',
        name: 'Semantic Consistency Rule',
        type: 'semantic',
        priority: 1,
        description: 'Ensure semantic definitions are consistent across all components',
        validation: (context) => {
          if (!context.components.semantic) return true;
          const semantic = context.components.semantic;
          return !semantic.conflicts || semantic.conflicts.length === 0;
        },
        recommendation: (violation) => [
          'Review semantic definitions in all components',
          'Standardize terminology and concepts',
          'Use semantic validation before integration'
        ]
      },
      {
        id: 'reasoning-consistency',
        name: 'Reasoning Consistency Rule',
        type: 'reasoning',
        priority: 2,
        description: 'Ensure reasoning paths are logically consistent',
        validation: (context) => {
          if (!context.components.reasoning) return true;
          const reasoning = context.components.reasoning;
          return !reasoning.contradictions || reasoning.contradictions.length === 0;
        },
        recommendation: (violation) => [
          'Review reasoning chains for logical fallacies',
          'Validate assumptions and premises',
          'Ensure conclusion follows from premises'
        ]
      },
      {
        id: 'strategy-consistency',
        name: 'Strategy Consistency Rule',
        type: 'strategy',
        priority: 3,
        description: 'Ensure strategies are aligned with overall objectives',
        validation: (context) => {
          if (!context.components.strategy) return true;
          const strategy = context.components.strategy;
          return strategy.alignmentScore && strategy.alignmentScore >= 0.8;
        },
        recommendation: (violation) => [
          'Review strategy alignment with objectives',
          'Ensure strategic priorities are consistent',
          'Validate strategy execution plans'
        ]
      },
      {
        id: 'evolution-consistency',
        name: 'Evolution Consistency Rule',
        type: 'evolution',
        priority: 4,
        description: 'Ensure evolution follows coherent paths',
        validation: (context) => {
          if (!context.components.evolution) return true;
          const evolution = context.components.evolution;
          return evolution.coherenceScore && evolution.coherenceScore >= 0.75;
        },
        recommendation: (violation) => [
          'Review evolution trajectory',
          'Ensure changes are incremental and coherent',
          'Maintain backward compatibility'
        ]
      },
      {
        id: 'civilization-consistency',
        name: 'Civilization Consistency Rule',
        type: 'civilization',
        priority: 5,
        description: 'Ensure civilization rules are consistently applied',
        validation: (context) => {
          if (!context.components.civilization) return true;
          const civilization = context.components.civilization;
          return civilization.ruleCompliance && civilization.ruleCompliance >= 0.9;
        },
        recommendation: (violation) => [
          'Review civilization rule applications',
          'Ensure rules are consistently enforced',
          'Maintain cultural coherence'
        ]
      },
      {
        id: 'cross-domain-alignment',
        name: 'Cross-Domain Alignment Rule',
        type: 'cross-domain',
        priority: 6,
        description: 'Ensure cross-domain interactions are properly aligned',
        validation: (context) => {
          const components = Object.keys(context.components);
          if (components.length < 2) return true;

          // 檢查至少有一個跨域對齊
          let hasAlignment = false;
          for (let i = 0; i < components.length; i++) {
            for (let j = i + 1; j < components.length; j++) {
              const dataA = context.components[components[i]];
              const dataB = context.components[components[j]];
              if (dataA.alignment && dataA.alignment[components[j]]) {
                hasAlignment = true;
                break;
              }
            }
            if (hasAlignment) break;
          }

          return hasAlignment;
        },
        recommendation: (violation) => [
          'Establish cross-domain communication protocols',
          'Create shared semantic anchors',
          'Implement cross-domain validation checks'
        ]
      }
    ];

    for (const rule of defaultRules) {
      this.rules.set(rule.id, rule);
    }
  }

  /**
   * 計算嚴重程度
   */
  private calculateSeverity(rule: ConsistencyRule, context: ConsistencyContext): 'low' | 'medium' | 'high' | 'critical' {
    if (rule.priority <= 2) return 'critical';
    if (rule.priority <= 4) return 'high';
    if (rule.priority <= 6) return 'medium';
    return 'low';
  }

  /**
   * 獲取受影響的組件
   */
  private getAffectedComponents(rule: ConsistencyRule, context: ConsistencyContext): string[] {
    const affected: string[] = [];

    if (rule.type === 'semantic') affected.push('semantic');
    if (rule.type === 'reasoning') affected.push('reasoning');
    if (rule.type === 'strategy') affected.push('strategy');
    if (rule.type === 'evolution') affected.push('evolution');
    if (rule.type === 'civilization') affected.push('civilization');
    if (rule.type === 'cross-domain') {
      affected.push(...Object.keys(context.components));
    }

    return affected;
  }

  /**
   * 創建違規上下文
   */
  private createViolationContext(rule: ConsistencyRule, context: ConsistencyContext): ConsistencyViolation {
    return {
      ruleId: rule.id,
      ruleName: rule.name,
      ruleType: rule.type,
      severity: 'medium',
      description: rule.description,
      affectedComponents: this.getAffectedComponents(rule, context),
      recommendations: [],
      timestamp: Date.now()
    };
  }

  /**
   * 計算整體分數
   */
  private calculateOverallScore(violations: ConsistencyViolation[]): number {
    if (violations.length === 0) return 1.0;

    // 基於違規嚴重程度計算懲罰
    let penalty = 0;
    for (const violation of violations) {
      switch (violation.severity) {
        case 'critical':
          penalty += 0.2;
          break;
        case 'high':
          penalty += 0.1;
          break;
        case 'medium':
          penalty += 0.05;
          break;
        case 'low':
          penalty += 0.02;
          break;
      }
    }

    return Math.max(0, 1.0 - penalty);
  }

  /**
   * 確定狀態
   */
  private determineStatus(score: number): 'consistent' | 'inconsistent' | 'degraded' {
    if (score >= this.consistencyThreshold) return 'consistent';
    if (score >= this.consistencyThreshold - 0.2) return 'degraded';
    return 'inconsistent';
  }

  /**
   * 生成建議
   */
  private generateRecommendations(violations: ConsistencyViolation[], status: string): string[] {
    const recommendations: string[] = [];

    // 從違規中收集建議
    for (const violation of violations) {
      recommendations.push(...violation.recommendations);
    }

    // 根據狀態添加通用建議
    if (status === 'inconsistent') {
      recommendations.push('Immediate action required: Review and resolve all violations');
      recommendations.push('Consider pausing operations until consistency is restored');
    } else if (status === 'degraded') {
      recommendations.push('System performance may be affected: Review violations');
      recommendations.push('Schedule maintenance to address inconsistencies');
    }

    return recommendations;
  }

  /**
   * 計算組件分數
   */
  private calculateComponentScore(component: string, check: ConsistencyCheck): number {
    const componentViolations = check.violations.filter(v => 
      v.affectedComponents.includes(component)
    );

    if (componentViolations.length === 0) return 1.0;

    const criticalViolations = componentViolations.filter(v => v.severity === 'critical').length;
    const penalty = criticalViolations * 0.2 + (componentViolations.length - criticalViolations) * 0.05;

    return Math.max(0, 1.0 - penalty);
  }

  /**
   * 創建快照
   */
  private async createSnapshot(check: ConsistencyCheck): Promise<ConsistencySnapshot> {
    const snapshotId = `snapshot-${Date.now()}`;
    const previousSnapshot = this.snapshots.size > 0 
      ? Array.from(this.snapshots.values()).pop() 
      : null;

    // 計算 delta
    const delta = this.calculateDelta(previousSnapshot, check);

    const snapshot: ConsistencySnapshot = {
      id: snapshotId,
      timestamp: Date.now(),
      check,
      previousSnapshotId: previousSnapshot?.id,
      delta
    };

    this.snapshots.set(snapshotId, snapshot);

    // 清理舊快照
    this.cleanupOldSnapshots();

    return snapshot;
  }

  /**
   * 計算 delta
   */
  private calculateDelta(previous: ConsistencySnapshot | null, current: ConsistencyCheck): ConsistencyDelta {
    if (!previous) {
      return {
        newViolations: current.violations,
        resolvedViolations: [],
        scoreChange: current.overallScore - 1.0,
        statusChange: undefined
      };
    }

    const previousViolations = new Set(
      (previous.check?.violations || []).map(v => `${v.ruleId}-${v.timestamp}`)
    );
    const currentViolations = new Set(
      current.violations.map(v => `${v.ruleId}-${v.timestamp}`)
    );

    const newViolations = current.violations.filter(v => 
      !previousViolations.has(`${v.ruleId}-${v.timestamp}`)
    );
    const resolvedViolations = (previous.check?.violations || []).filter(v => 
      !currentViolations.has(`${v.ruleId}-${v.timestamp}`)
    );

    const scoreChange = current.overallScore - (previous.check?.overallScore || 1.0);

    let statusChange: 'improved' | 'degraded' | 'stable' | undefined;
    if (scoreChange > 0.05) statusChange = 'improved';
    else if (scoreChange < -0.05) statusChange = 'degraded';
    else statusChange = 'stable';

    return {
      newViolations,
      resolvedViolations,
      scoreChange,
      statusChange
    };
  }

  /**
   * 自動修正
   */
  private async autoCorrect(violations: ConsistencyViolation[]): Promise<void> {
    // 對低嚴重程度的違規進行自動修正
    for (const violation of violations) {
      if (violation.severity === 'low') {
        // 記錄修正意圖（實際修正需要組件協作）
        // console.log(`Auto-correcting low severity violation: ${violation.ruleId}`);
      }
    }
  }

  /**
   * 清理舊快照
   */
  private cleanupOldSnapshots(): void {
    const now = Date.now();
    const cutoff = now - (24 * 60 * 60 * 1000); // 保留 24 小時

    for (const [id, snapshot] of this.snapshots.entries()) {
      if (snapshot.timestamp < cutoff) {
        this.snapshots.delete(id);
      }
    }
  }

  /**
   * 維護歷史大小
   */
  private maintainHistorySize(): void {
    while (this.checkHistory.length > this.maxHistorySize) {
      this.checkHistory.shift();
    }
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    const now = Date.now();
    const cutoff = now - olderThan;

    this.checkHistory = this.checkHistory.filter(c => c.timestamp >= cutoff);
    
    for (const [id, violation] of this.activeViolations.entries()) {
      if (violation.timestamp < cutoff) {
        this.activeViolations.delete(id);
      }
    }
  }

  /**
   * 重置引擎
   */
  async reset(): Promise<void> {
    this.rules.clear();
    this.checkHistory = [];
    this.snapshots.clear();
    this.activeViolations.clear();
    
    // 重新初始化默認規則
    this.initializeDefaultRules();
  }
}