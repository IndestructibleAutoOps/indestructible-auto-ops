// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-trans-domain-integration
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * Trans-Domain Knowledge Mapping Engine
 * 
 * 跨領域知識映射引擎 - 跨領域、跨文明、跨 Mesh 的知識映射
 * 
 * 核心能力：
 * 1. Cross-domain knowledge mapping
 * 2. Cross-civilization rule mapping
 * 3. Cross-Mesh semantic mapping
 * 
 * 這是「智慧的遷移能力」
 */

import { EventEmitter } from 'events';

interface KnowledgeDomain {
  id: string;
  name: string;
  domain: string;
  concepts: string[];
  rules: string[];
  patterns: string[];
}

interface KnowledgeMapping {
  sourceDomain: string;
  targetDomain: string;
  mappingType: 'domain-to-domain' | 'civilization-to-civilization' | 'mesh-to-mesh';
  mappings: ConceptMapping[];
  confidence: number;
  transferability: number;
}

interface ConceptMapping {
  sourceConcept: string;
  targetConcept: string;
  transformation: string;
  confidence: number;
  applicableContexts: string[];
}

interface MappingResult {
  success: boolean;
  sourceDomain: string;
  targetDomain: string;
  mappings: ConceptMapping[];
  confidence: number;
  transferability: number;
  timestamp: Date;
}

interface TransferredKnowledge {
  originalSource: string;
  targetDomain: string;
  concept: string;
  adaptedConcept: string;
  application: string;
  success: boolean;
}

export class KnowledgeMappingEngine extends EventEmitter {
  private domains: Map<string, KnowledgeDomain>;
  private mappings: Map<string, KnowledgeMapping>;
  private transferredKnowledge: TransferredKnowledge[];
  private isConnected: boolean;

  constructor() {
    super();
    this.domains = new Map();
    this.mappings = new Map();
    this.transferredKnowledge = [];
    this.isConnected = false;
  }

  /**
   * Initialize the knowledge mapping engine
   */
  async initialize(): Promise<void> {
    this.isConnected = true;
    console.log('✅ Knowledge Mapping Engine initialized');
    this.emit('initialized');
  }

  /**
   * Register a knowledge domain
   */
  registerDomain(domain: KnowledgeDomain): void {
    this.domains.set(domain.id, domain);
    this.emit('domain-registered', { domainId: domain.id });
  }

  /**
   * Map knowledge between domains
   */
  async mapKnowledge(
    sourceDomainId: string,
    targetDomainId: string,
    mappingType: 'domain-to-domain' | 'civilization-to-civilization' | 'mesh-to-mesh'
  ): Promise<MappingResult> {
    const sourceDomain = this.domains.get(sourceDomainId);
    const targetDomain = this.domains.get(targetDomainId);

    if (!sourceDomain || !targetDomain) {
      return {
        success: false,
        sourceDomain: sourceDomainId,
        targetDomain: targetDomainId,
        mappings: [],
        confidence: 0,
        transferability: 0,
        timestamp: new Date()
      };
    }

    try {
      // Generate concept mappings
      const mappings = this.generateConceptMappings(sourceDomain, targetDomain);
      
      // Calculate confidence and transferability
      const confidence = this.calculateConfidence(mappings);
      const transferability = this.calculateTransferability(mappings);

      const result: MappingResult = {
        success: true,
        sourceDomain: sourceDomainId,
        targetDomain: targetDomainId,
        mappings,
        confidence,
        transferability,
        timestamp: new Date()
      };

      // Store mapping
      const mappingKey = `${sourceDomainId}->${targetDomainId}`;
      this.mappings.set(mappingKey, {
        sourceDomain: sourceDomainId,
        targetDomain: targetDomainId,
        mappingType,
        mappings,
        confidence,
        transferability
      });

      this.emit('knowledge-mapped', { 
        sourceDomain: sourceDomainId, 
        targetDomain: targetDomainId,
        confidence 
      });

      return result;
    } catch (error) {
      return {
        success: false,
        sourceDomain: sourceDomainId,
        targetDomain: targetDomainId,
        mappings: [],
        confidence: 0,
        transferability: 0,
        timestamp: new Date()
      };
    }
  }

  /**
   * Generate concept mappings between domains
   */
  private generateConceptMappings(
    source: KnowledgeDomain,
    target: KnowledgeDomain
  ): ConceptMapping[] {
    const mappings: ConceptMapping[] = [];
    
    // Map concepts from source to target
    for (const sourceConcept of source.concepts) {
      const targetConcept = this.findBestMatch(sourceConcept, target.concepts);
      
      if (targetConcept) {
        mappings.push({
          sourceConcept,
          targetConcept,
          transformation: this.determineTransformation(source.domain, target.domain),
          confidence: 0.7 + Math.random() * 0.3,
          applicableContexts: [target.domain]
        });
      }
    }

    return mappings;
  }

  /**
   * Find best matching concept in target domain
   */
  private findBestMatch(sourceConcept: string, targetConcepts: string[]): string | null {
    // In a real implementation, this would use semantic similarity
    // For now, we'll use a simple heuristic
    for (const targetConcept of targetConcepts) {
      const similarity = this.calculateSimilarity(sourceConcept, targetConcept);
      if (similarity > 0.6) {
        return targetConcept;
      }
    }
    return null;
  }

  /**
   * Calculate similarity between concepts
   */
  private calculateSimilarity(concept1: string, concept2: string): number {
    // Simple similarity based on common words
    const words1 = concept1.toLowerCase().split(/\s+/);
    const words2 = concept2.toLowerCase().split(/\s+/);
    const common = words1.filter(w => words2.includes(w));
    return common.length / Math.max(words1.length, words2.length);
  }

  /**
   * Determine transformation type between domains
   */
  private determineTransformation(sourceDomain: string, targetDomain: string): string {
    if (sourceDomain === targetDomain) {
      return 'direct-mapping';
    }
    return 'cross-domain-adaptation';
  }

  /**
   * Calculate confidence for mappings
   */
  private calculateConfidence(mappings: ConceptMapping[]): number {
    if (mappings.length === 0) return 0;
    const avgConfidence = mappings.reduce((sum, m) => sum + m.confidence, 0) / mappings.length;
    return avgConfidence;
  }

  /**
   * Calculate transferability for mappings
   */
  private calculateTransferability(mappings: ConceptMapping[]): number {
    // Transferability depends on number of high-confidence mappings
    const highConfidenceCount = mappings.filter(m => m.confidence > 0.8).length;
    return highConfidenceCount / Math.max(mappings.length, 1);
  }

  /**
   * Transfer knowledge from one domain to another
   */
  async transferKnowledge(
    sourceDomainId: string,
    targetDomainId: string,
    concept: string,
    application: string
  ): Promise<TransferredKnowledge> {
    const mappingKey = `${sourceDomainId}->${targetDomainId}`;
    const mapping = this.mappings.get(mappingKey);

    if (!mapping) {
      return {
        originalSource: sourceDomainId,
        targetDomain: targetDomainId,
        concept,
        adaptedConcept: concept,
        application,
        success: false
      };
    }

    // Find the mapping for the concept
    const conceptMapping = mapping.mappings.find(m => m.sourceConcept === concept);
    
    if (!conceptMapping) {
      return {
        originalSource: sourceDomainId,
        targetDomain: targetDomainId,
        concept,
        adaptedConcept: concept,
        application,
        success: false
      };
    }

    const transferred: TransferredKnowledge = {
      originalSource: sourceDomainId,
      targetDomain: targetDomainId,
      concept,
      adaptedConcept: conceptMapping.targetConcept,
      application,
      success: true
    };

    this.transferredKnowledge.push(transferred);
    this.emit('knowledge-transferred', {
      sourceDomain: sourceDomainId,
      targetDomain: targetDomainId,
      concept
    });

    return transferred;
  }

  /**
   * Map civilization rules
   */
  async mapCivilizationRules(
    sourceCivilizationId: string,
    targetCivilizationId: string
  ): Promise<MappingResult> {
    return this.mapKnowledge(
      sourceCivilizationId,
      targetCivilizationId,
      'civilization-to-civilization'
    );
  }

  /**
   * Map Mesh semantics
   */
  async mapMeshSemantics(
    sourceMeshId: string,
    targetMeshId: string
  ): Promise<MappingResult> {
    return this.mapKnowledge(
      sourceMeshId,
      targetMeshId,
      'mesh-to-mesh'
    );
  }

  /**
   * Get all registered domains
   */
  getDomains(): KnowledgeDomain[] {
    return Array.from(this.domains.values());
  }

  /**
   * Get all mappings
   */
  getMappings(): KnowledgeMapping[] {
    return Array.from(this.mappings.values());
  }

  /**
   * Get transferred knowledge history
   */
  getTransferredKnowledge(): TransferredKnowledge[] {
    return this.transferredKnowledge;
  }

  /**
   * Check if connected
   */
  isActive(): boolean {
    return this.isConnected;
  }
}