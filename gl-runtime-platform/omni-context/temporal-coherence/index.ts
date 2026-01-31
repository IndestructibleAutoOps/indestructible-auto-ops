# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/GL-UNIFIED-NAMING-CHARTER.yaml


/**
 * Temporal Coherence Engine
 * 時間一致性引擎
 * 
 * 功能：保持長期記憶一致性、推理方向穩定性、文明規則延續性、演化軌跡可解釋性
 * 目標：讓系統不會「跳來跳去」，而是有穩定的智慧軌跡
 */

export interface TemporalState {
  id: string;
  type: 'memory' | 'reasoning' | 'rule' | 'evolution' | 'strategy';
  data: Record<string, any>;
  timestamp: number;
  version: number;
  previousVersion?: string;
  confidence: number;
  stability: number;
  metadata?: Record<string, any>;
}

export interface CoherenceCheck {
  stateId: string;
  previousStateId: string;
  coherenceScore: number;
  violations: string[];
  recommendations: string[];
  timestamp: number;
}

export interface TemporalSnapshot {
  id: string;
  timestamp: number;
  states: Map<string, TemporalState>;
  globalCoherence: number;
  metadata?: Record<string, any>;
}

export interface CoherenceRequest {
  state: TemporalState;
  checkDepth?: number;
  strictness?: 'lenient' | 'moderate' | 'strict';
}

export interface CoherenceResult {
  coherent: boolean;
  coherenceScore: number;
  violations: string[];
  recommendations: string[];
  accepted: boolean;
  timestamp: number;
}

export interface StabilityMetrics {
  overallStability: number;
  typeStability: Record<string, number>;
  averageConfidence: number;
  stateVersionDrift: number;
  coherenceTrend: number[];
}

export class TemporalCoherenceEngine {
  private states: Map<string, TemporalState>;
  private snapshots: Map<string, TemporalSnapshot>;
  private coherenceHistory: CoherenceCheck[];
  private stabilityThreshold: number;
  private confidenceDecayRate: number;
  private maxHistorySize: number;
  private snapshotInterval: number;
  private nextSnapshotId: number;
  private versionCounter: Map<string, number>;

  constructor(options?: {
    stabilityThreshold?: number;
    confidenceDecayRate?: number;
    maxHistorySize?: number;
    snapshotInterval?: number;
  }) {
    this.states = new Map();
    this.snapshots = new Map();
    this.coherenceHistory = [];
    this.stabilityThreshold = options?.stabilityThreshold || 0.75;
    this.confidenceDecayRate = options?.confidenceDecayRate || 0.95;
    this.maxHistorySize = options?.maxHistorySize || 5000;
    this.snapshotInterval = options?.snapshotInterval || 300000; // 5 minutes
    this.nextSnapshotId = 1;
    this.versionCounter = new Map();
  }

  /**
   * 添加狀態
   */
  async addState(state: TemporalState): Promise<CoherenceResult> {
    // 檢查時間一致性
    const coherenceResult = await this.checkCoherence({ state, checkDepth: 1, strictness: 'moderate' });
    
    if (!coherenceResult.coherent) {
      // 不一致的狀態不會被接受
      return {
        ...coherenceResult,
        accepted: false
      };
    }

    // 設置版本號
    state.version = this.getNextVersion(state.id);
    
    // 更新穩定性
    state.stability = this.calculateStability(state);

    // 添加狀態
    this.states.set(state.id, state);
    
    // 衰減舊狀態的信心度
    await this.decayConfidence();

    // 記錄一致性檢查
    if (state.previousVersion) {
      const check: CoherenceCheck = {
        stateId: state.id,
        previousStateId: state.previousVersion,
        coherenceScore: coherenceResult.coherenceScore,
        violations: coherenceResult.violations,
        recommendations: coherenceResult.recommendations,
        timestamp: Date.now()
      };
      this.addToCoherenceHistory(check);
    }

    // 檢查是否需要創建快照
    await this.checkAndCreateSnapshot();

    return {
      ...coherenceResult,
      accepted: true
    };
  }

  /**
   * 檢查時間一致性
   */
  async checkCoherence(request: CoherenceRequest): Promise<CoherenceResult> {
    const state = request.state;
    const depth = request.checkDepth || 1;
    const strictness = request.strictness || 'moderate';

    const violations: string[] = [];
    const recommendations: string[] = [];
    let coherenceScore = 1.0;

    // 1. 檢查與前一狀態的一致性
    if (state.previousVersion) {
      const previousState = this.states.get(state.previousVersion);
      
      if (previousState) {
        const previousCoherence = this.checkStateCoherence(previousState, state, strictness);
        coherenceScore = previousCoherence.score;
        
        if (previousCoherence.violations.length > 0) {
          violations.push(...previousCoherence.violations);
          recommendations.push(...previousCoherence.recommendations);
        }
      } else {
        violations.push(`Previous version ${state.previousVersion} not found`);
        coherenceScore -= 0.2;
      }
    }

    // 2. 深度檢查（檢查更早的狀態）
    if (depth > 1 && state.previousVersion) {
      const deepCoherence = await this.checkDeepCoherence(state, depth);
      if (deepCoherence.score < coherenceScore) {
        coherenceScore = deepCoherence.score;
        violations.push(...deepCoherence.violations);
      }
    }

    // 3. 檢查與全局一致性
    const globalCoherence = await this.checkGlobalCoherence(state);
    if (globalCoherence.score < 1.0) {
      coherenceScore = Math.min(coherenceScore, globalCoherence.score);
      violations.push(...globalCoherence.violations);
    }

    // 判斷是否一致
    const coherent = coherenceScore >= this.stabilityThreshold;

    // 生成建議
    if (!coherent) {
      recommendations.push('Review state changes and ensure logical consistency');
      recommendations.push('Consider incremental changes instead of large jumps');
      recommendations.push('Validate changes against historical patterns');
    }

    return {
      coherent,
      coherenceScore: Math.max(0, coherenceScore),
      violations,
      recommendations,
      accepted: false, // 由調用者決定是否接受
      timestamp: Date.now()
    };
  }

  /**
   * 獲取狀態
   */
  async getState(id: string): Promise<TemporalState | null> {
    return this.states.get(id) || null;
  }

  /**
   * 獲取狀態歷史
   */
  async getStateHistory(id: string, depth?: number): Promise<TemporalState[]> {
    const history: TemporalState[] = [];
    let currentState = await this.getState(id);
    
    const maxDepth = depth || 10;
    let count = 0;

    while (currentState && count < maxDepth) {
      history.push(currentState);
      count++;
      
      if (currentState.previousVersion) {
        currentState = await this.getState(currentState.previousVersion);
      } else {
        break;
      }
    }

    return history;
  }

  /**
   * 創建快照
   */
  async createSnapshot(): Promise<TemporalSnapshot> {
    const snapshot: TemporalSnapshot = {
      id: `snapshot-${this.nextSnapshotId++}`,
      timestamp: Date.now(),
      states: new Map(this.states),
      globalCoherence: await this.calculateGlobalCoherence(),
      metadata: {
        stateCount: this.states.size
      }
    };

    this.snapshots.set(snapshot.id, snapshot);
    
    // 清理舊快照
    await this.cleanupOldSnapshots();

    return snapshot;
  }

  /**
   * 恢復快照
   */
  async restoreSnapshot(snapshotId: string): Promise<boolean> {
    const snapshot = this.snapshots.get(snapshotId);
    
    if (!snapshot) {
      return false;
    }

    this.states = new Map(snapshot.states);
    
    // 重新計算穩定性
    for (const [id, state] of this.states.entries()) {
      state.stability = this.calculateStability(state);
    }

    return true;
  }

  /**
   * 獲取穩定性指標
   */
  getStabilityMetrics(): StabilityMetrics {
    const states = Array.from(this.states.values());
    
    if (states.length === 0) {
      return {
        overallStability: 1.0,
        typeStability: {},
        averageConfidence: 1.0,
        stateVersionDrift: 0,
        coherenceTrend: []
      };
    }

    // 計算整體穩定性
    const overallStability = states.reduce((sum, s) => sum + s.stability, 0) / states.length;
    
    // 計算各類型穩定性
    const typeStability: Record<string, number> = {};
    const typeGroups: Record<string, TemporalState[]> = {};
    
    for (const state of states) {
      if (!typeGroups[state.type]) {
        typeGroups[state.type] = [];
      }
      typeGroups[state.type].push(state);
    }
    
    for (const [type, typeStates] of Object.entries(typeGroups)) {
      typeStability[type] = typeStates.reduce((sum, s) => sum + s.stability, 0) / typeStates.length;
    }
    
    // 計算平均信心度
    const averageConfidence = states.reduce((sum, s) => sum + s.confidence, 0) / states.length;
    
    // 計算版本漂移
    const stateVersionDrift = states.reduce((sum, s) => sum + s.version, 0) / states.length;
    
    // 獲取一致性趨勢
    const recentChecks = this.coherenceHistory.slice(-20);
    const coherenceTrend = recentChecks.map(check => check.coherenceScore);

    return {
      overallStability,
      typeStability,
      averageConfidence,
      versionDrift: stateVersionDrift,
      coherenceTrend
    };
  }

  /**
   * 檢查兩個狀態的一致性
   */
  private checkStateCoherence(
    previous: TemporalState,
    current: TemporalState,
    strictness: 'lenient' | 'moderate' | 'strict'
  ): { score: number; violations: string[]; recommendations: string[] } {
    const violations: string[] = [];
    const recommendations: string[] = [];
    let score = 1.0;

    // 1. 類型一致性
    if (previous.type !== current.type) {
      violations.push(`Type change: ${previous.type} -> ${current.type}`);
      score -= strictness === 'strict' ? 0.3 : 0.1;
      recommendations.push('Ensure type changes are intentional and well-documented');
    }

    // 2. 數據一致性檢查
    const dataCoherence = this.checkDataCoherence(previous.data, current.data, strictness);
    score -= dataCoherence.penalty;
    violations.push(...dataCoherence.violations);
    recommendations.push(...dataCoherence.recommendations);

    // 3. 信心度變化檢查
    if (current.confidence > previous.confidence + 0.2) {
      violations.push('Confidence increased too rapidly');
      score -= 0.1;
      recommendations.push('Verify confidence justification');
    }

    return {
      score: Math.max(0, score),
      violations,
      recommendations
    };
  }

  /**
   * 深度一致性檢查
   */
  private async checkDeepCoherence(state: TemporalState, depth: number): Promise<{ score: number; violations: string[] }> {
    const violations: string[] = [];
    let score = 1.0;

    let currentState = state;
    const statesToCheck: TemporalState[] = [state];

    // 收集要檢查的狀態
    for (let i = 1; i < depth; i++) {
      if (currentState.previousVersion) {
        const previous = await this.getState(currentState.previousVersion);
        if (previous) {
          statesToCheck.push(previous);
          currentState = previous;
        } else {
          break;
        }
      } else {
        break;
      }
    }

    // 檢查狀態序列的一致性
    for (let i = 1; i < statesToCheck.length; i++) {
      const previous = statesToCheck[i];
      const current = statesToCheck[i - 1];
      
      const coherence = this.checkStateCoherence(previous, current, 'moderate');
      score = Math.min(score, coherence.score);
      
      if (coherence.violations.length > 0) {
        violations.push(...coherence.violations.map(v => `Deep check (${i}): ${v}`));
      }
    }

    return { score, violations };
  }

  /**
   * 檢查全局一致性
   */
  private async checkGlobalCoherence(state: TemporalState): Promise<{ score: number; violations: string[] }> {
    const violations: string[] = [];
    let score = 1.0;

    const allStates = Array.from(this.states.values());

    // 檢查與同類型狀態的一致性
    const sameTypeStates = allStates.filter(s => s.type === state.type && s.id !== state.id);
    
    if (sameTypeStates.length > 0) {
      const avgConfidence = sameTypeStates.reduce((sum, s) => sum + s.confidence, 0) / sameTypeStates.length;
      
      if (Math.abs(state.confidence - avgConfidence) > 0.3) {
        violations.push(`Confidence deviates significantly from ${state.type} average`);
        score -= 0.1;
      }
    }

    return { score, violations };
  }

  /**
   * 計算全局一致性
   */
  private async calculateGlobalCoherence(): Promise<number> {
    const recentChecks = this.coherenceHistory.slice(-10);
    
    if (recentChecks.length === 0) {
      return 1.0;
    }

    return recentChecks.reduce((sum, check) => sum + check.coherenceScore, 0) / recentChecks.length;
  }

  /**
   * 檢查數據一致性
   */
  private checkDataCoherence(
    previous: Record<string, any>,
    current: Record<string, any>,
    strictness: 'lenient' | 'moderate' | 'strict'
  ): { penalty: number; violations: string[]; recommendations: string[] } {
    const violations: string[] = [];
    const recommendations: string[] = [];
    let penalty = 0;

    const prevKeys = Object.keys(previous);
    const currKeys = Object.keys(current);

    // 檢查刪除的鍵
    const removedKeys = prevKeys.filter(k => !currKeys.includes(k));
    if (removedKeys.length > 0 && strictness !== 'lenient') {
      violations.push(`Removed keys: ${removedKeys.join(', ')}`);
      penalty += strictness === 'strict' ? removedKeys.length * 0.05 : removedKeys.length * 0.02;
      recommendations.push('Document reasons for removing keys');
    }

    // 檢查新增的鍵
    const addedKeys = currKeys.filter(k => !prevKeys.includes(k));
    if (addedKeys.length > 0) {
      // 新增鍵是正常的，但記錄一下
    }

    // 檢查值變化
    const commonKeys = prevKeys.filter(k => currKeys.includes(k));
    for (const key of commonKeys) {
      const prevValue = previous[key];
      const currValue = current[key];
      
      // 檢查類型變化
      if (typeof prevValue !== typeof currValue) {
        violations.push(`Type change for ${key}: ${typeof prevValue} -> ${typeof currValue}`);
        penalty += 0.1;
      }
    }

    return { penalty, violations, recommendations };
  }

  /**
   * 計算穩定性
   */
  private calculateStability(state: TemporalState): number {
    // 基於信心度和版本穩定性
    const stability = state.confidence * 0.7 + (1 - Math.min(1, state.version / 100)) * 0.3;
    return stability;
  }

  /**
   * 獲取下一個版本號
   */
  private getNextVersion(id: string): number {
    const current = this.versionCounter.get(id) || 0;
    this.versionCounter.set(id, current + 1);
    return current + 1;
  }

  /**
   * 衰減信心度
   */
  private async decayConfidence(): Promise<void> {
    const now = Date.now();
    
    for (const [id, state] of this.states.entries()) {
      const age = now - state.timestamp;
      const decayPeriods = Math.floor(age / 3600000); // 每小時衰減一次
      
      if (decayPeriods > 0) {
        const newConfidence = state.confidence * Math.pow(this.confidenceDecayRate, decayPeriods);
        state.confidence = Math.max(0.1, newConfidence);
        state.stability = this.calculateStability(state);
      }
    }
  }

  /**
   * 添加到一致性歷史
   */
  private addToCoherenceHistory(check: CoherenceCheck): void {
    this.coherenceHistory.push(check);
    
    // 維護歷史大小
    if (this.coherenceHistory.length > this.maxHistorySize) {
      this.coherenceHistory.shift();
    }
  }

  /**
   * 檢查並創建快照
   */
  private async checkAndCreateSnapshot(): Promise<void> {
    const now = Date.now();
    
    if (this.snapshots.size === 0) {
      await this.createSnapshot();
      return;
    }

    const lastSnapshot = Array.from(this.snapshots.values()).pop();
    if (lastSnapshot && (now - lastSnapshot.timestamp) >= this.snapshotInterval) {
      await this.createSnapshot();
    }
  }

  /**
   * 清理舊快照
   */
  private async cleanupOldSnapshots(): Promise<void> {
    const now = Date.now();
    const cutoff = now - (24 * 60 * 60 * 1000); // 保留 24 小時

    for (const [id, snapshot] of this.snapshots.entries()) {
      if (snapshot.timestamp < cutoff) {
        this.snapshots.delete(id);
      }
    }
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    const now = Date.now();
    const cutoff = now - olderThan;

    // 清理舊狀態
    for (const [id, state] of this.states.entries()) {
      if (state.timestamp < cutoff) {
        this.states.delete(id);
      }
    }

    // 清理舊一致性檢查
    this.coherenceHistory = this.coherenceHistory.filter(c => c.timestamp >= cutoff);
  }

  /**
   * 重置引擎
   */
  async reset(): Promise<void> {
    this.states.clear();
    this.snapshots.clear();
    this.coherenceHistory = [];
    this.versionCounter.clear();
    this.nextSnapshotId = 1;
  }
}