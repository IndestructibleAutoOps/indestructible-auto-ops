# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/GL-UNIFIED-NAMING-CHARTER.yaml


/**
 * Omni-Domain Knowledge Alignment Engine
 * 跨領域知識對齊引擎
 * 
 * 功能：將不同領域、文明、推理模型、策略框架的知識對齊
 * 目標：實現「智慧的整合性」
 */

export interface KnowledgeDomain {
  id: string;
  name: string;
  type: 'software-engineering' | 'data-science' | 'systems-thinking' | 'philosophy' | 'other';
  concepts: Map<string, Concept>;
  relationships: Map<string, Relationship>;
  axioms: Map<string, Axiom>;
  metadata?: Record<string, any>;
}

export interface Concept {
  id: string;
  name: string;
  definition: string;
  aliases: string[];
  domain: string;
  properties: Record<string, any>;
  confidence: number;
}

export interface Relationship {
  id: string;
  source: string;
  target: string;
  type: 'is-a' | 'part-of' | 'depends-on' | 'similar-to' | 'opposite-of' | 'causes' | 'enables';
  strength: number;
  confidence: number;
}

export interface Axiom {
  id: string;
  statement: string;
  domain: string;
  validity: number;
  confidence: number;
  proof?: string;
}

export interface AlignmentMapping {
  id: string;
  sourceDomain: string;
  targetDomain: string;
  conceptMappings: Map<string, string>; // source concept -> target concept
  relationshipMappings: Map<string, string>;
  axiomMappings: Map<string, string>;
  confidence: number;
  metadata?: Record<string, any>;
}

export interface AlignmentRequest {
  domains: string[];
  alignmentType: 'concept' | 'relationship' | 'axiom' | 'full';
  strictness?: 'lenient' | 'moderate' | 'strict';
}

export interface AlignmentResult {
  success: boolean;
  mappings: AlignmentMapping[];
  statistics: {
    totalConceptsAligned: number;
    totalRelationshipsAligned: number;
    totalAxiomsAligned: number;
    averageConfidence: number;
  };
  conflicts: AlignmentConflict[];
  recommendations: string[];
}

export interface AlignmentConflict {
  type: 'concept' | 'relationship' | 'axiom';
  sourceDomain: string;
  targetDomain: string;
  sourceItem: string;
  targetItem: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
  resolution?: string;
}

export interface KnowledgeAlignmentMetrics {
  totalDomains: number;
  totalAlignments: number;
  averageAlignmentConfidence: number;
  domainConnectivity: Map<string, number>;
  conflictsResolved: number;
  conflictsPending: number;
}

export class KnowledgeAlignmentEngine {
  private domains: Map<string, KnowledgeDomain>;
  private mappings: Map<string, AlignmentMapping>;
  private conflicts: AlignmentConflict[];
  private alignmentHistory: AlignmentResult[];
  private maxHistorySize: number;
  private similarityThreshold: number;

  constructor(options?: {
    maxHistorySize?: number;
    similarityThreshold?: number;
  }) {
    this.domains = new Map();
    this.mappings = new Map();
    this.conflicts = [];
    this.alignmentHistory = [];
    this.maxHistorySize = options?.maxHistorySize || 1000;
    this.similarityThreshold = options?.similarityThreshold || 0.7;

    // 初始化默認領域
    this.initializeDefaultDomains();
  }

  /**
   * 註冊知識領域
   */
  async registerDomain(domain: KnowledgeDomain): Promise<void> {
    this.domains.set(domain.id, domain);
  }

  /**
   * 對齊知識領域
   */
  async alignKnowledge(request: AlignmentRequest): Promise<AlignmentResult> {
    const mappings: AlignmentMapping[] = [];
    const conflicts: AlignmentConflict[] = [];
    const recommendations: string[] = [];

    // 獲取要對齊的領域
    const domainsToAlign = request.domains
      .map(id => this.domains.get(id))
      .filter((d): d is KnowledgeDomain => d !== undefined);

    if (domainsToAlign.length < 2) {
      throw new Error('At least two domains are required for alignment');
    }

    // 兩兩對齊
    for (let i = 0; i < domainsToAlign.length; i++) {
      for (let j = i + 1; j < domainsToAlign.length; j++) {
        const domainA = domainsToAlign[i];
        const domainB = domainsToAlign[j];

        const alignment = await this.alignDomains(domainA, domainB, request);
        mappings.push(alignment);

        // 檢查衝突
        const domainConflicts = this.detectConflicts(domainA, domainB, alignment);
        conflicts.push(...domainConflicts);
      }
    }

    // 生成統計
    const statistics = this.calculateAlignmentStatistics(mappings);

    // 生成建議
    this.generateAlignmentRecommendations(conflicts, recommendations);

    // 保存到歷史
    const result: AlignmentResult = {
      success: mappings.length > 0,
      mappings,
      statistics,
      conflicts,
      recommendations
    };

    this.alignmentHistory.push(result);
    this.maintainHistorySize();

    return result;
  }

  /**
   * 獲取對齊映射
   */
  async getMapping(mappingId: string): Promise<AlignmentMapping | null> {
    return this.mappings.get(mappingId) || null;
  }

  /**
   * 查詢跨領域概念
   */
  async queryConcept(conceptId: string, domains?: string[]): Promise<Map<string, Concept>> {
    const results = new Map<string, Concept>();

    const domainsToSearch = domains || Array.from(this.domains.keys());

    for (const domainId of domainsToSearch) {
      const domain = this.domains.get(domainId);
      if (domain) {
        const concept = domain.concepts.get(conceptId);
        if (concept) {
          results.set(domainId, concept);
        }
      }
    }

    return results;
  }

  /**
   * 查詢跨領域關係
   */
  async queryRelationship(relationshipId: string, domains?: string[]): Promise<Map<string, Relationship>> {
    const results = new Map<string, Relationship>();

    const domainsToSearch = domains || Array.from(this.domains.keys());

    for (const domainId of domainsToSearch) {
      const domain = this.domains.get(domainId);
      if (domain) {
        const relationship = domain.relationships.get(relationshipId);
        if (relationship) {
          results.set(domainId, relationship);
        }
      }
    }

    return results;
  }

  /**
   * 獲取指標
   */
  getMetrics(): KnowledgeAlignmentMetrics {
    const domainConnectivity = new Map<string, number>();

    // 計算每個領域的連接度
    for (const [mappingId, mapping] of this.mappings.entries()) {
      const sourceCount = domainConnectivity.get(mapping.sourceDomain) || 0;
      const targetCount = domainConnectivity.get(mapping.targetDomain) || 0;

      domainConnectivity.set(mapping.sourceDomain, sourceCount + 1);
      domainConnectivity.set(mapping.targetDomain, targetCount + 1);
    }

    const averageConfidence = this.mappings.size > 0
      ? Array.from(this.mappings.values()).reduce((sum, m) => sum + m.confidence, 0) / this.mappings.size
      : 0;

    return {
      totalDomains: this.domains.size,
      totalAlignments: this.mappings.size,
      averageAlignmentConfidence: averageConfidence,
      domainConnectivity,
      conflictsResolved: this.conflicts.filter(c => c.resolution).length,
      conflictsPending: this.conflicts.filter(c => !c.resolution).length
    };
  }

  /**
   * 初始化默認領域
   */
  private initializeDefaultDomains(): void {
    // 軟體工程領域
    const softwareEngineeringDomain: KnowledgeDomain = {
      id: 'software-engineering',
      name: 'Software Engineering',
      type: 'software-engineering',
      concepts: new Map([
        ['component', { id: 'component', name: 'Component', definition: 'A reusable software unit', aliases: ['module', 'unit'], domain: 'software-engineering', properties: { complexity: 'variable' }, confidence: 0.95 }],
        ['dependency', { id: 'dependency', name: 'Dependency', definition: 'A relationship where one component requires another', aliases: ['requires'], domain: 'software-engineering', properties: { direction: 'unidirectional' }, confidence: 0.95 }],
        ['architecture', { id: 'architecture', name: 'Architecture', definition: 'The high-level structure of a system', aliases: ['structure', 'design'], domain: 'software-engineering', properties: { abstraction: 'high' }, confidence: 0.95 }]
      ]),
      relationships: new Map([
        ['component-part-of-architecture', { id: 'component-part-of-architecture', source: 'component', target: 'architecture', type: 'part-of', strength: 0.9, confidence: 0.95 }],
        ['component-depends-on-component', { id: 'component-depends-on-component', source: 'component', target: 'dependency', type: 'depends-on', strength: 0.85, confidence: 0.95 }]
      ]),
      axioms: new Map([
        ['modularity', { id: 'modularity', statement: 'Systems should be composed of independent, reusable components', domain: 'software-engineering', validity: 0.95, confidence: 0.95 }]
      ])
    };

    // 數據科學領域
    const dataScienceDomain: KnowledgeDomain = {
      id: 'data-science',
      name: 'Data Science',
      type: 'data-science',
      concepts: new Map([
        ['model', { id: 'model', name: 'Model', definition: 'A mathematical representation of a system', aliases: ['representation'], domain: 'data-science', properties: { accuracy: 'measurable' }, confidence: 0.95 }],
        ['feature', { id: 'feature', name: 'Feature', definition: 'An input variable used for prediction', aliases: ['attribute', 'variable'], domain: 'data-science', properties: { type: 'various' }, confidence: 0.95 }],
        ['pattern', { id: 'pattern', name: 'Pattern', definition: 'A regularity in data', aliases: ['regularity'], domain: 'data-science', properties: { complexity: 'variable' }, confidence: 0.95 }]
      ]),
      relationships: new Map([
        ['feature-part-of-model', { id: 'feature-part-of-model', source: 'feature', target: 'model', type: 'part-of', strength: 0.9, confidence: 0.95 }],
        ['pattern-revealed-by-model', { id: 'pattern-revealed-by-model', source: 'pattern', target: 'model', type: 'causes', strength: 0.85, confidence: 0.95 }]
      ]),
      axioms: new Map([
        ['no-free-lunch', { id: 'no-free-lunch', statement: 'No single model works best for all problems', domain: 'data-science', validity: 0.95, confidence: 0.95 }]
      ])
    };

    // 系統思維領域
    const systemsThinkingDomain: KnowledgeDomain = {
      id: 'systems-thinking',
      name: 'Systems Thinking',
      type: 'systems-thinking',
      concepts: new Map([
        ['system', { id: 'system', name: 'System', definition: 'A set of interconnected components', aliases: ['whole'], domain: 'systems-thinking', properties: { complexity: 'emergent' }, confidence: 0.95 }],
        ['emergence', { id: 'emergence', name: 'Emergence', definition: 'Properties that arise from system interactions', aliases: ['emergent-property'], domain: 'systems-thinking', properties: { unpredictability: 'high' }, confidence: 0.95 }],
        ['feedback', { id: 'feedback', name: 'Feedback', definition: 'Information about system output used to regulate behavior', aliases: ['feedback-loop'], domain: 'systems-thinking', properties: { type: 'circular' }, confidence: 0.95 }]
      ]),
      relationships: new Map([
        ['emergence-part-of-system', { id: 'emergence-part-of-system', source: 'emergence', target: 'system', type: 'part-of', strength: 0.95, confidence: 0.95 }],
        ['feedback-regulates-system', { id: 'feedback-regulates-system', source: 'feedback', target: 'system', type: 'enables', strength: 0.9, confidence: 0.95 }]
      ]),
      axioms: new Map([
        ['wholeness', { id: 'wholeness', statement: 'The whole is greater than the sum of its parts', domain: 'systems-thinking', validity: 0.95, confidence: 0.95 }]
      ])
    };

    // 哲學領域
    const philosophyDomain: KnowledgeDomain = {
      id: 'philosophy',
      name: 'Philosophy',
      type: 'philosophy',
      concepts: new Map([
        ['concept', { id: 'concept', name: 'Concept', definition: 'An abstract idea representing a category', aliases: ['notion', 'idea'], domain: 'philosophy', properties: { abstraction: 'high' }, confidence: 0.95 }],
        ['logic', { id: 'logic', name: 'Logic', definition: 'The study of valid reasoning', aliases: ['reasoning'], domain: 'philosophy', properties: { structure: 'formal' }, confidence: 0.95 }],
        ['truth', { id: 'truth', name: 'Truth', definition: 'Conformity with reality or fact', aliases: ['verity'], domain: 'philosophy', properties: { universality: 'aspired' }, confidence: 0.95 }]
      ]),
      relationships: new Map([
        ['logic-enables-concept', { id: 'logic-enables-concept', source: 'logic', target: 'concept', type: 'enables', strength: 0.9, confidence: 0.95 }],
        ['truth-aim-of-logic', { id: 'truth-aim-of-logic', source: 'truth', target: 'logic', type: 'causes', strength: 0.85, confidence: 0.95 }]
      ]),
      axioms: new Map([
        ['identity', { id: 'identity', statement: 'A thing is what it is', domain: 'philosophy', validity: 0.95, confidence: 0.95 }]
      ])
    };

    this.domains.set('software-engineering', softwareEngineeringDomain);
    this.domains.set('data-science', dataScienceDomain);
    this.domains.set('systems-thinking', systemsThinkingDomain);
    this.domains.set('philosophy', philosophyDomain);
  }

  /**
   * 對齊兩個領域
   */
  private async alignDomains(
    domainA: KnowledgeDomain,
    domainB: KnowledgeDomain,
    request: AlignmentRequest
  ): Promise<AlignmentMapping> {
    const mappingId = `mapping-${domainA.id}-${domainB.id}-${Date.now()}`;
    const conceptMappings = new Map<string, string>();
    const relationshipMappings = new Map<string, string>();
    const axiomMappings = new Map<string, string>();

    // 對齊概念
    if (request.alignmentType === 'concept' || request.alignmentType === 'full') {
      for (const [conceptIdA, conceptA] of domainA.concepts.entries()) {
        const bestMatch = this.findBestConceptMatch(conceptA, domainB.concepts);
        if (bestMatch && bestMatch.similarity >= this.similarityThreshold) {
          conceptMappings.set(conceptIdA, bestMatch.concept.id);
        }
      }
    }

    // 對齊關係
    if (request.alignmentType === 'relationship' || request.alignmentType === 'full') {
      for (const [relIdA, relA] of domainA.relationships.entries()) {
        const bestMatch = this.findBestRelationshipMatch(relA, domainB.relationships);
        if (bestMatch && bestMatch.similarity >= this.similarityThreshold) {
          relationshipMappings.set(relIdA, bestMatch.relationship.id);
        }
      }
    }

    // 對齊公理
    if (request.alignmentType === 'axiom' || request.alignmentType === 'full') {
      for (const [axiomIdA, axiomA] of domainA.axioms.entries()) {
        const bestMatch = this.findBestAxiomMatch(axiomA, domainB.axioms);
        if (bestMatch && bestMatch.similarity >= this.similarityThreshold) {
          axiomMappings.set(axiomIdA, bestMatch.axiom.id);
        }
      }
    }

    // 計算信心度
    const confidence = this.calculateAlignmentConfidence(
      conceptMappings,
      relationshipMappings,
      axiomMappings,
      domainA,
      domainB
    );

    const mapping: AlignmentMapping = {
      id: mappingId,
      sourceDomain: domainA.id,
      targetDomain: domainB.id,
      conceptMappings,
      relationshipMappings,
      axiomMappings,
      confidence
    };

    this.mappings.set(mappingId, mapping);

    return mapping;
  }

  /**
   * 尋找最佳概念匹配
   */
  private findBestConceptMatch(
    concept: Concept,
    targetConcepts: Map<string, Concept>
  ): { concept: Concept; similarity: number } | null {
    let bestMatch: { concept: Concept; similarity: number } | null = null;

    for (const [id, targetConcept] of targetConcepts.entries()) {
      const similarity = this.calculateConceptSimilarity(concept, targetConcept);
      
      if (similarity >= this.similarityThreshold) {
        if (!bestMatch || similarity > bestMatch.similarity) {
          bestMatch = { concept: targetConcept, similarity };
        }
      }
    }

    return bestMatch;
  }

  /**
   * 尋找最佳關係匹配
   */
  private findBestRelationshipMatch(
    relationship: Relationship,
    targetRelationships: Map<string, Relationship>
  ): { relationship: Relationship; similarity: number } | null {
    let bestMatch: { relationship: Relationship; similarity: number } | null = null;

    for (const [id, targetRelationship] of targetRelationships.entries()) {
      const similarity = this.calculateRelationshipSimilarity(relationship, targetRelationship);
      
      if (similarity >= this.similarityThreshold) {
        if (!bestMatch || similarity > bestMatch.similarity) {
          bestMatch = { relationship: targetRelationship, similarity };
        }
      }
    }

    return bestMatch;
  }

  /**
   * 尋找最佳公理匹配
   */
  private findBestAxiomMatch(
    axiom: Axiom,
    targetAxioms: Map<string, Axiom>
  ): { axiom: Axiom; similarity: number } | null {
    let bestMatch: { axiom: Axiom; similarity: number } | null = null;

    for (const [id, targetAxiom] of targetAxioms.entries()) {
      const similarity = this.calculateAxiomSimilarity(axiom, targetAxiom);
      
      if (similarity >= this.similarityThreshold) {
        if (!bestMatch || similarity > bestMatch.similarity) {
          bestMatch = { axiom: targetAxiom, similarity };
        }
      }
    }

    return bestMatch;
  }

  /**
   * 計算概念相似度
   */
  private calculateConceptSimilarity(a: Concept, b: Concept): number {
    // 名稱相似度
    const nameSimilarity = this.stringSimilarity(a.name.toLowerCase(), b.name.toLowerCase());

    // 別名相似度
    let aliasSimilarity = 0;
    for (const aliasA of a.aliases) {
      for (const aliasB of b.aliases) {
        const sim = this.stringSimilarity(aliasA.toLowerCase(), aliasB.toLowerCase());
        if (sim > aliasSimilarity) {
          aliasSimilarity = sim;
        }
      }
    }

    // 定義相似度
    const definitionSimilarity = this.stringSimilarity(a.definition.toLowerCase(), b.definition.toLowerCase());

    // 加權平均
    return nameSimilarity * 0.3 + aliasSimilarity * 0.3 + definitionSimilarity * 0.4;
  }

  /**
   * 計算關係相似度
   */
  private calculateRelationshipSimilarity(a: Relationship, b: Relationship): number {
    // 類型匹配
    const typeMatch = a.type === b.type ? 1.0 : 0.0;

    // 強度相似度
    const strengthSimilarity = 1 - Math.abs(a.strength - b.strength);

    // 信心度相似度
    const confidenceSimilarity = 1 - Math.abs(a.confidence - b.confidence);

    return typeMatch * 0.5 + strengthSimilarity * 0.25 + confidenceSimilarity * 0.25;
  }

  /**
   * 計算公理相似度
   */
  private calculateAxiomSimilarity(a: Axiom, b: Axiom): number {
    // 語句相似度
    const statementSimilarity = this.stringSimilarity(a.statement.toLowerCase(), b.statement.toLowerCase());

    // 有效性相似度
    const validitySimilarity = 1 - Math.abs(a.validity - b.validity);

    // 信心度相似度
    const confidenceSimilarity = 1 - Math.abs(a.confidence - b.confidence);

    return statementSimilarity * 0.5 + validitySimilarity * 0.25 + confidenceSimilarity * 0.25;
  }

  /**
   * 字符串相似度（簡單的 Jaccard 相似度）
   */
  private stringSimilarity(a: string, b: string): number {
    const setA = new Set(a.split(/\s+/));
    const setB = new Set(b.split(/\s+/));

    const intersection = new Set([...setA].filter(x => setB.has(x)));
    const union = new Set([...setA, ...setB]);

    if (union.size === 0) return 0;

    return intersection.size / union.size;
  }

  /**
   * 計算對齊信心度
   */
  private calculateAlignmentConfidence(
    conceptMappings: Map<string, string>,
    relationshipMappings: Map<string, string>,
    axiomMappings: Map<string, string>,
    domainA: KnowledgeDomain,
    domainB: KnowledgeDomain
  ): number {
    const conceptCoverage = conceptMappings.size / Math.max(1, domainA.concepts.size);
    const relationshipCoverage = relationshipMappings.size / Math.max(1, domainA.relationships.size);
    const axiomCoverage = axiomMappings.size / Math.max(1, domainA.axioms.size);

    return (conceptCoverage + relationshipCoverage + axiomCoverage) / 3;
  }

  /**
   * 檢測衝突
   */
  private detectConflicts(
    domainA: KnowledgeDomain,
    domainB: KnowledgeDomain,
    mapping: AlignmentMapping
  ): AlignmentConflict[] {
    const conflicts: AlignmentConflict[] = [];

    // 檢查概念衝突（矛盾的定義）
    for (const [sourceId, targetId] of mapping.conceptMappings.entries()) {
      const sourceConcept = domainA.concepts.get(sourceId);
      const targetConcept = domainB.concepts.get(targetId);

      if (sourceConcept && targetConcept) {
        const definitionSimilarity = this.stringSimilarity(
          sourceConcept.definition.toLowerCase(),
          targetConcept.definition.toLowerCase()
        );

        if (definitionSimilarity < 0.3) {
          conflicts.push({
            type: 'concept',
            sourceDomain: domainA.id,
            targetDomain: domainB.id,
            sourceItem: sourceId,
            targetItem: targetId,
            description: `Conflicting definitions: "${sourceConcept.definition}" vs "${targetConcept.definition}"`,
            severity: 'high'
          });
        }
      }
    }

    // 檢查公理衝突（矛盾的陳述）
    for (const [sourceId, targetId] of mapping.axiomMappings.entries()) {
      const sourceAxiom = domainA.axioms.get(sourceId);
      const targetAxiom = domainB.axioms.get(targetId);

      if (sourceAxiom && targetAxiom) {
        const statementSimilarity = this.stringSimilarity(
          sourceAxiom.statement.toLowerCase(),
          targetAxiom.statement.toLowerCase()
        );

        if (statementSimilarity < 0.3 && sourceAxiom.validity > 0.7 && targetAxiom.validity > 0.7) {
          conflicts.push({
            type: 'axiom',
            sourceDomain: domainA.id,
            targetDomain: domainB.id,
            sourceItem: sourceId,
            targetItem: targetId,
            description: `Potentially contradictory axioms: "${sourceAxiom.statement}" vs "${targetAxiom.statement}"`,
            severity: 'high'
          });
        }
      }
    }

    return conflicts;
  }

  /**
   * 計算對齊統計
   */
  private calculateAlignmentStatistics(mappings: AlignmentMapping[]) {
    let totalConceptsAligned = 0;
    let totalRelationshipsAligned = 0;
    let totalAxiomsAligned = 0;
    let totalConfidence = 0;

    for (const mapping of mappings) {
      totalConceptsAligned += mapping.conceptMappings.size;
      totalRelationshipsAligned += mapping.relationshipMappings.size;
      totalAxiomsAligned += mapping.axiomMappings.size;
      totalConfidence += mapping.confidence;
    }

    return {
      totalConceptsAligned,
      totalRelationshipsAligned,
      totalAxiomsAligned,
      averageConfidence: mappings.length > 0 ? totalConfidence / mappings.length : 0
    };
  }

  /**
   * 生成對齊建議
   */
  private generateAlignmentRecommendations(conflicts: AlignmentConflict[], recommendations: string[]): void {
    const criticalConflicts = conflicts.filter(c => c.severity === 'critical');
    const highConflicts = conflicts.filter(c => c.severity === 'high');

    if (highConflicts.length > 0) {
      recommendations.push('High-severity conflicts detected: Review concept definitions for consistency');
    }

    if (highConflicts.length > 0) {
      recommendations.push('High-severity conflicts detected: Review concept definitions for consistency');
    }

    if (conflicts.length > 0) {
      recommendations.push('Establish cross-domain semantic anchors to resolve conflicts');
      recommendations.push('Create hybrid concepts that bridge conflicting definitions');
    }
  }

  /**
   * 維護歷史大小
   */
  private maintainHistorySize(): void {
    while (this.alignmentHistory.length > this.maxHistorySize) {
      this.alignmentHistory.shift();
    }
  }

  /**
   * 清理舊數據
   */
  async cleanup(olderThan: number): Promise<void> {
    const now = Date.now();
    const cutoff = now - olderThan;

    this.alignmentHistory = this.alignmentHistory.filter(r => 
      // 簡化：移除非常舊的記錄
      true
    );
  }

  /**
   * 重置引擎
   */
  async reset(): Promise<void> {
    this.domains.clear();
    this.mappings.clear();
    this.conflicts = [];
    this.alignmentHistory = [];
    
    // 重新初始化默認領域
    this.initializeDefaultDomains();
  }
}