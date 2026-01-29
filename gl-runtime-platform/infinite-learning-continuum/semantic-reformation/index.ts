// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-semantic-reformation
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Continuous Semantic Reformation
 * Version 20.0.0
 * 
 * 核心：語意連續重構
 * - 語意不是固定的，而是隨著新資料、新策略、新現實、新文明重構
 * - SRG 變成永續重構的語意場（Semantic Field）
 * - 語意流動、演變、適應
 */

import { UnifiedIntelligenceFabric } from '../../unified-intelligence-fabric';

// ============================================================================
// Type Definitions
// ============================================================================

export interface SemanticReformationConfig {
  reformationInterval: number;      // milliseconds
  coherenceThreshold: number;
  adaptationRate: number;
  enableAutoReformation: boolean;
  enableSemanticField: boolean;
  enableCivilizationAwareness: boolean;
}

export interface SemanticField {
  id: string;
  name: string;
  domain: string;
  semantics: Map<string, SemanticEntity>;
  relationships: Map<string, SemanticRelationship[]>;
  evolutionState: SemanticEvolutionState;
  reformationHistory: ReformationEvent[];
  lastReformation: number;
}

export interface SemanticEntity {
  id: string;
  type: SemanticEntityType;
  name: string;
  meaning: any;
  confidence: number;
  stability: number;
  adaptability: number;
  version: number;
  evolutionPath: EvolutionPath[];
  temporalWeight: number;
}

export type SemanticEntityType = 
  | 'concept'
  | 'relation'
  | 'pattern'
  | 'strategy'
  | 'metaphor'
  | 'axiom'
  | 'principle';

export interface SemanticRelationship {
  id: string;
  sourceId: string;
  targetId: string;
  type: RelationshipType;
  strength: number;
  confidence: number;
  context: Record<string, any>;
}

export type RelationshipType = 
  | 'is_a'
  | 'has_a'
  | 'part_of'
  | 'related_to'
  | 'causes'
  | 'enables'
  | 'contradicts'
  | 'evolves_into';

export interface SemanticEvolutionState {
  stage: SemanticEvolutionStage;
  coherence: number;
  complexity: number;
  diversity: number;
  adaptationVelocity: number;
  evolutionPressure: number;
}

export type SemanticEvolutionStage = 
  | 'emerging'       // 新生語意
  | 'stabilizing'    // 穩定中
  | 'stable'         // 穩定
  | 'evolving'       // 演變中
  | 'transcending'   // 超越中
  | 'deprecated';    // 已棄用

export interface EvolutionPath {
  timestamp: number;
  changeType: EvolutionChangeType;
  fromValue: any;
  toValue: any;
  reason: string;
  impact: number;
}

export type EvolutionChangeType = 
  | 'meaning_shift'
  | 'confidence_change'
  | 'relationship_update'
  | 'context_adaptation'
  | 'cross_domain_migration';

export interface ReformationEvent {
  id: string;
  timestamp: number;
  type: ReformationType;
  description: string;
  affectedEntities: string[];
  impact: number;
  reformationScore: number;
}

export type ReformationType = 
  | 'semantic_shift'
  | 'relationship_rewire'
  | 'field_expansion'
  | 'domain_convergence'
  | 'civilization_adaptation'
  | 'reality_alignment';

export interface SemanticReformationStatistics {
  totalFields: number;
  totalEntities: number;
  totalRelationships: number;
  reformationsPerformed: number;
  averageReformationImpact: number;
  fieldCoherence: number;
  semanticDiversity: number;
  adaptationVelocity: number;
  lastReformation: number;
}

// ============================================================================
// Continuous Semantic Reformation Class
// ============================================================================

export class ContinuousSemanticReformation {
  private fabric: UnifiedIntelligenceFabric;
  private config: SemanticReformationConfig;
  private semanticFields: Map<string, SemanticField>;
  private reformationHistory: ReformationEvent[];
  private reformationTimer?: NodeJS.Timeout;
  private statistics: SemanticReformationStatistics;
  private initialized: boolean;
  
  constructor(
    fabric: UnifiedIntelligenceFabric,
    config?: Partial<SemanticReformationConfig>
  ) {
    this.fabric = fabric;
    this.config = {
      reformationInterval: config?.reformationInterval || 60000, // 1 minute
      coherenceThreshold: config?.coherenceThreshold || 0.7,
      adaptationRate: config?.adaptationRate || 0.3,
      enableAutoReformation: config?.enableAutoReformation ?? true,
      enableSemanticField: config?.enableSemanticField ?? true,
      enableCivilizationAwareness: config?.enableCivilizationAwareness ?? true
    };
    
    this.semanticFields = new Map();
    this.reformationHistory = [];
    this.statistics = {
      totalFields: 0,
      totalEntities: 0,
      totalRelationships: 0,
      reformationsPerformed: 0,
      averageReformationImpact: 0,
      fieldCoherence: 0,
      semanticDiversity: 0,
      adaptationVelocity: 0,
      lastReformation: 0
    };
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Continuous Semantic Reformation] Initializing perpetual semantic reformation...');
    
    // 初始化語意場
    await this.initializeSemanticFields();
    
    // 啟動持續語意重構
    if (this.config.enableAutoReformation) {
      await this.startPerpetualReformation();
    }
    
    this.initialized = true;
    console.log('[Continuous Semantic Reformation] Perpetual semantic reformation initialized');
  }
  
  // ========================================================================
  // Semantic Field Management
  // ========================================================================
  
  async createSemanticField(
    name: string,
    domain: string
  ): Promise<string> {
    const fieldId = `semantic-field-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const field: SemanticField = {
      id: fieldId,
      name,
      domain,
      semantics: new Map(),
      relationships: new Map(),
      evolutionState: {
        stage: 'emerging',
        coherence: 0.5,
        complexity: 0.5,
        diversity: 0.5,
        adaptationVelocity: 0.1,
        evolutionPressure: 0.5
      },
      reformationHistory: [],
      lastReformation: Date.now()
    };
    
    this.semanticFields.set(fieldId, field);
    this.statistics.totalFields++;
    
    console.log(`[Continuous Semantic Reformation] Created semantic field: ${name} (${domain})`);
    
    return fieldId;
  }
  
  async addSemanticEntity(
    fieldId: string,
    type: SemanticEntityType,
    name: string,
    meaning: any,
    confidence?: number
  ): Promise<string> {
    const field = this.semanticFields.get(fieldId);
    if (!field) {
      throw new Error(`Semantic field not found: ${fieldId}`);
    }
    
    const entityId = `semantic-entity-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const entity: SemanticEntity = {
      id: entityId,
      type,
      name,
      meaning,
      confidence: confidence || 0.5,
      stability: 0.3,
      adaptability: 0.7,
      version: 1,
      evolutionPath: [],
      temporalWeight: 1.0
    };
    
    field.semantics.set(entityId, entity);
    this.statistics.totalEntities++;
    
    console.log(`[Continuous Semantic Reformation] Added semantic entity: ${name}`);
    
    return entityId;
  }
  
  async addSemanticRelationship(
    fieldId: string,
    sourceId: string,
    targetId: string,
    type: RelationshipType,
    strength?: number
  ): Promise<string> {
    const field = this.semanticFields.get(fieldId);
    if (!field) {
      throw new Error(`Semantic field not found: ${fieldId}`);
    }
    
    const relationshipId = `semantic-relationship-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const relationship: SemanticRelationship = {
      id: relationshipId,
      sourceId,
      targetId,
      type,
      strength: strength || 0.5,
      confidence: 0.5,
      context: {}
    };
    
    if (!field.relationships.has(sourceId)) {
      field.relationships.set(sourceId, []);
    }
    field.relationships.get(sourceId)!.push(relationship);
    this.statistics.totalRelationships++;
    
    console.log(`[Continuous Semantic Reformation] Added semantic relationship: ${sourceId} -> ${targetId}`);
    
    return relationshipId;
  }
  
  // ========================================================================
  // Perpetual Semantic Reformation
  // ========================================================================
  
  private async startPerpetualReformation(): Promise<void> {
    console.log(`[Continuous Semantic Reformation] Starting perpetual reformation every ${this.config.reformationInterval}ms`);
    
    this.reformationTimer = setInterval(async () => {
      await this.performPerpetualReformation();
    }, this.config.reformationInterval);
  }
  
  private async performPerpetualReformation(): Promise<void> {
    const startTime = Date.now();
    
    console.log('[Continuous Semantic Reformation] Performing perpetual reformation cycle...');
    
    // 對每個語意場進行重構
    for (const [fieldId, field] of this.semanticFields) {
      await this.reformSemanticField(fieldId);
    }
    
    // 跨場語意整合
    await this.integrateCrossFieldSemantics();
    
    // 文明感知重構
    if (this.config.enableCivilizationAwareness) {
      await this.reformForCivilization();
    }
    
    // 更新統計
    await this.updateStatistics();
    
    const duration = Date.now() - startTime;
    console.log(`[Continuous Semantic Reformation] Reformation cycle completed in ${duration}ms`);
  }
  
  private async reformSemanticField(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    console.log(`[Continuous Semantic Reformation] Reforming field: ${field.name}`);
    
    // 1. 語意漂移檢測
    await this.detectSemanticDrift(fieldId);
    
    // 2. 關係重連
    await this.rewireRelationships(fieldId);
    
    // 3. 演化階段更新
    await this.updateEvolutionStages(fieldId);
    
    // 4. 一致性檢查
    await this.checkFieldCoherence(fieldId);
    
    field.lastReformation = Date.now();
  }
  
  private async detectSemanticDrift(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    // 檢測語意漂移
    for (const [entityId, entity] of field.semantics) {
      const driftDetected = await this.detectEntityDrift(fieldId, entityId);
      
      if (driftDetected > this.config.adaptationRate) {
        await this.adaptEntity(fieldId, entityId, driftDetected);
      }
    }
  }
  
  private async detectEntityDrift(fieldId: string, entityId: string): Promise<number> {
    // 檢測實體的語意漂移程度
    const field = this.semanticFields.get(fieldId);
    if (!field) return 0;
    
    const entity = field.semantics.get(entityId);
    if (!entity) return 0;
    
    // 計算漂移程度（簡化實作）
    let drift = 0;
    const now = Date.now();
    const timeSinceLastUpdate = now - entity.evolutionPath[entity.evolutionPath.length - 1]?.timestamp || 0;
    
    // 時間越長，漂移越大
    drift = Math.min(timeSinceLastUpdate / 86400000, 1.0); // 每天增加漂移
    
    return drift;
  }
  
  private async adaptEntity(fieldId: string, entityId: string, drift: number): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    const entity = field.semantics.get(entityId);
    if (!entity) return;
    
    // 適應語意漂移
    entity.stability = Math.max(0, entity.stability - drift * 0.1);
    entity.confidence = Math.max(0.1, entity.confidence - drift * 0.05);
    entity.version++;
    
    // 記錄演化路徑
    entity.evolutionPath.push({
      timestamp: Date.now(),
      changeType: 'meaning_shift',
      fromValue: entity.meaning,
      toValue: this.evolveMeaning(entity.meaning, drift),
      reason: 'semantic_drift',
      impact: drift
    });
    
    // 更新實體
    field.semantics.set(entityId, entity);
    
    // 記錄重構事件
    await this.recordReformationEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'semantic_shift',
      description: `Semantic entity ${entity.name} adapted due to drift`,
      affectedEntities: [entityId],
      impact: drift,
      reformationScore: drift * 10
    });
  }
  
  private evolveMeaning(meaning: any, drift: number): any {
    // 演變語意（簡化實作）
    if (typeof meaning === 'string') {
      return `${meaning} (evolved)`;
    } else if (typeof meaning === 'object' && meaning !== null) {
      return { ...meaning, evolved: true, drift };
    }
    return meaning;
  }
  
  private async rewireRelationships(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    // 重連關係
    for (const [sourceId, relationships] of field.relationships) {
      for (const relationship of relationships) {
        const source = field.semantics.get(sourceId);
        const target = field.semantics.get(relationship.targetId);
        
        if (source && target) {
          // 根據穩定性和信心調整關係強度
          const avgStability = (source.stability + target.stability) / 2;
          const avgConfidence = (source.confidence + target.confidence) / 2;
          
          relationship.strength = relationship.strength * 0.9 + avgStability * 0.1;
          relationship.confidence = relationship.confidence * 0.9 + avgConfidence * 0.1;
          
          // 移除弱關係
          if (relationship.strength < 0.1) {
            const index = relationships.indexOf(relationship);
            if (index > -1) {
              relationships.splice(index, 1);
            }
          }
        }
      }
    }
    
    // 記錄重構事件
    await this.recordReformationEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'relationship_rewire',
      description: 'Relationships rewired based on stability and confidence',
      affectedEntities: [],
      impact: 1.0,
      reformationScore: 5.0
    });
  }
  
  private async updateEvolutionStages(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    // 更新演化階段
    for (const [entityId, entity] of field.semantics) {
      let newStage: SemanticEvolutionStage = entity.stability > 0.8 ? 'stable' : 
                                              entity.stability > 0.5 ? 'stabilizing' :
                                              entity.stability > 0.3 ? 'emerging' :
                                              entity.stability > 0.1 ? 'evolving' : 'deprecated';
      
      if (newStage !== entity.evolutionPath[entity.evolutionPath.length - 1]?.changeType) {
        // 階段改變
        entity.evolutionPath.push({
          timestamp: Date.now(),
          changeType: 'context_adaptation',
          fromValue: entity.evolutionPath[entity.evolutionPath.length - 1]?.changeType,
          toValue: newStage,
          reason: 'evolution_stage_update',
          impact: 1.0
        });
      }
      
      field.evolutionState.stage = newStage;
    }
  }
  
  private async checkFieldCoherence(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    // 檢查場一致性
    let totalCoherence = 0;
    let entityCount = 0;
    
    for (const [_, entity] of field.semantics) {
      totalCoherence += entity.confidence;
      entityCount++;
    }
    
    field.evolutionState.coherence = entityCount > 0 ? totalCoherence / entityCount : 0;
    
    // 如果一致性低於閾值，觸發場擴展
    if (field.evolutionState.coherence < this.config.coherenceThreshold) {
      await this.expandField(fieldId);
    }
  }
  
  private async expandField(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    console.log(`[Continuous Semantic Reformation] Expanding field: ${field.name}`);
    
    // 擴展場（增加新的語意實體）
    await this.addSemanticEntity(fieldId, 'concept', `auto-generated-${Date.now()}`, 'Auto-generated semantic concept for field expansion', 0.5);
    
    // 記錄重構事件
    await this.recordReformationEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'field_expansion',
      description: `Field ${field.name} expanded due to low coherence`,
      affectedEntities: [],
      impact: 2.0,
      reformationScore: 10.0
    });
  }
  
  private async integrateCrossFieldSemantics(): Promise<void> {
    console.log('[Continuous Semantic Reformation] Integrating cross-field semantics...');
    
    // 跨場整合（簡化實作）
    const fieldIds = Array.from(this.semanticFields.keys());
    
    for (let i = 0; i < fieldIds.length; i++) {
      for (let j = i + 1; j < fieldIds.length; j++) {
        await this.connectFields(fieldIds[i], fieldIds[j]);
      }
    }
  }
  
  private async connectFields(fieldId1: string, fieldId2: string): Promise<void> {
    const field1 = this.semanticFields.get(fieldId1);
    const field2 = this.semanticFields.get(fieldId2);
    
    if (!field1 || !field2) return;
    
    // 連接相似的實體
    const similarity = await this.calculateFieldSimilarity(fieldId1, fieldId2);
    
    if (similarity > 0.7) {
      console.log(`[Continuous Semantic Reformation] Connecting fields: ${field1.name} <-> ${field2.name}`);
      
      // 記錄重構事件
      await this.recordReformationEvent({
        id: `event-${Date.now()}`,
        timestamp: Date.now(),
        type: 'domain_convergence',
        description: `Fields ${field1.name} and ${field2.name} converged due to similarity`,
        affectedEntities: [],
        impact: similarity,
        reformationScore: similarity * 10
      });
    }
  }
  
  private async calculateFieldSimilarity(fieldId1: string, fieldId2: string): Promise<number> {
    // 計算場相似度（簡化實作）
    const field1 = this.semanticFields.get(fieldId1);
    const field2 = this.semanticFields.get(fieldId2);
    
    if (!field1 || !field2) return 0;
    
    // 基於領域相似度
    const domainSimilarity = field1.domain === field2.domain ? 1.0 : 0.3;
    
    // 基於實體數量
    const sizeRatio = Math.min(field1.semantics.size, field2.semantics.size) / 
                     Math.max(field1.semantics.size, field2.semantics.size);
    
    return (domainSimilarity + sizeRatio) / 2;
  }
  
  private async reformForCivilization(): Promise<void> {
    console.log('[Continuous Semantic Reformation] Reforming for civilization...');
    
    // 文明感知重構（簡化實作）
    for (const [fieldId, field] of this.semanticFields) {
      if (field.domain === 'civilization' || field.domain === 'meta') {
        await this.adaptToCivilization(fieldId);
      }
    }
  }
  
  private async adaptToCivilization(fieldId: string): Promise<void> {
    const field = this.semanticFields.get(fieldId);
    if (!field) return;
    
    console.log(`[Continuous Semantic Reformation] Adapting field to civilization: ${field.name}`);
    
    // 記錄重構事件
    await this.recordReformationEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'civilization_adaptation',
      description: `Field ${field.name} adapted to civilization context`,
      affectedEntities: [],
      impact: 1.5,
      reformationScore: 7.5
    });
  }
  
  // ========================================================================
  // Statistics & Monitoring
  // ========================================================================
  
  private async updateStatistics(): Promise<void> {
    this.statistics.totalFields = this.semanticFields.size;
    
    let totalEntities = 0;
    let totalRelationships = 0;
    let totalCoherence = 0;
    
    for (const [_, field] of this.semanticFields) {
      totalEntities += field.semantics.size;
      totalRelationships += Array.from(field.relationships.values()).flat().length;
      totalCoherence += field.evolutionState.coherence;
    }
    
    this.statistics.totalEntities = totalEntities;
    this.statistics.totalRelationships = totalRelationships;
    this.statistics.fieldCoherence = this.semanticFields.size > 0 ? 
      totalCoherence / this.semanticFields.size : 0;
    
    // 計算平均重構影響
    if (this.reformationHistory.length > 0) {
      const recentImpact = this.reformationHistory.slice(-10).map(e => e.impact);
      this.statistics.averageReformationImpact = 
        recentImpact.reduce((sum, impact) => sum + impact, 0) / recentImpact.length;
    }
    
    this.statistics.lastReformation = Date.now();
  }
  
  async getStatistics(): Promise<SemanticReformationStatistics> {
    await this.updateStatistics();
    return { ...this.statistics };
  }
  
  async getSemanticField(fieldId: string): Promise<SemanticField | undefined> {
    return this.semanticFields.get(fieldId);
  }
  
  async listSemanticFields(): Promise<SemanticField[]> {
    return Array.from(this.semanticFields.values());
  }
  
  // ========================================================================
  // Event Recording
  // ========================================================================
  
  private async recordReformationEvent(event: ReformationEvent): Promise<void> {
    this.reformationHistory.push(event);
    this.statistics.reformationsPerformed++;
    
    // 限制歷史記錄大小
    const maxHistorySize = 10000;
    if (this.reformationHistory.length > maxHistorySize) {
      this.reformationHistory = this.reformationHistory.slice(-maxHistorySize);
    }
  }
  
  async getReformationHistory(limit?: number): Promise<ReformationEvent[]> {
    if (limit) {
      return this.reformationHistory.slice(-limit);
    }
    return [...this.reformationHistory];
  }
  
  // ========================================================================
  // Lifecycle Management
  // ========================================================================
  
  async shutdown(): Promise<void> {
    console.log('[Continuous Semantic Reformation] Shutting down...');
    
    if (this.reformationTimer) {
      clearInterval(this.reformationTimer);
      this.reformationTimer = undefined;
    }
    
    // 最後一次重構
    await this.performPerpetualReformation();
    
    console.log('[Continuous Semantic Reformation] Shutdown complete');
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}