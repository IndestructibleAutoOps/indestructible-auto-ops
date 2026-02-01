# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: typescript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Meta-Cognitive Runtime - Wisdom Engine (Version 14.0.0 Deep)
 * 
 * The Wisdom Engine provides advanced wisdom extraction, classification,
 * and application capabilities:
 * - Multi-dimensional wisdom extraction
 * - Wisdom classification and taxonomy
 * - Wisdom application and evaluation
 * - Wisdom evolution and refinement
 * 
 * This accelerates wisdom accumulation from 50% toward higher levels.
 */

import { EventEmitter } from 'events';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface WisdomEntry {
  id: string;
  timestamp: Date;
  wisdomType: WisdomType;
  category: WisdomCategory;
  content: string;
  source: WisdomSource;
  confidence: number;
  maturity: number;
  effectiveness: number;
  applications: number;
  lastApplied?: Date;
  contexts: string[];
  tags: string[];
  relatedWisdom: string[];
  evolutionHistory: WisdomEvolution[];
}

export type WisdomType = 'practical' | 'strategic' | 'philosophical' | 'ethical' | 'creative' | 'systemic' | 'transcendent';

export type WisdomCategory = 
  | 'decision-making'
  | 'problem-solving'
  | 'learning'
  | 'adaptation'
  | 'collaboration'
  | 'innovation'
  | 'ethics'
  | 'governance'
  | 'evolution'
  | 'consciousness';

export interface WisdomSource {
  type: 'experience' | 'reflection' | 'analysis' | 'synthesis' | 'transcendence';
  origin: string;
  context?: any;
}

export interface WisdomEvolution {
  timestamp: Date;
  changeType: 'refinement' | 'expansion' | 'integration' | 'synthesis';
  description: string;
  before?: string;
  after?: string;
  effectivenessChange: number;
}

export interface WisdomExtraction {
  id: string;
  timestamp: Date;
  sourceData: any;
  extractedWisdom: WisdomEntry[];
  extractionMethod: ExtractionMethod;
  confidence: number;
  significance: number;
}

export type ExtractionMethod = 
  | 'pattern-recognition'
  | 'causal-analysis'
  | 'analogical-reasoning'
  | 'meta-analysis'
  | 'synthetic-integration'
  | 'transcendent-insight';

export interface WisdomApplication {
  id: string;
  timestamp: Date;
  wisdomId: string;
  context: any;
  applicationType: ApplicationType;
  outcome: number;
  effectiveness: number;
  insights: string[];
}

export type ApplicationType = 
  | 'direct-application'
  | 'adaptive-application'
  | 'synthetic-application'
  | 'creative-adaptation'
  | 'transcendent-application';

export interface WisdomTaxonomy {
  categories: Map<WisdomCategory, WisdomEntry[]>;
  types: Map<WisdomType, WisdomEntry[]>;
  maturityLevels: Map<string, WisdomEntry[]>;
  effectivenessLevels: Map<string, WisdomEntry[]>;
  contextualMapping: Map<string, WisdomEntry[]>;
}

// ============================================================================
// WISDOM ENGINE CLASS
// ============================================================================

export class WisdomEngine extends EventEmitter {
  private wisdomEntries: Map<string, WisdomEntry>;
  private extractionHistory: WisdomExtraction[];
  private applicationHistory: WisdomApplication[];
  private taxonomy: WisdomTaxonomy;
  private wisdomPatterns: Map<string, any>;
  private readonly MAX_ENTRIES = 10000;
  private readonly MAX_HISTORY = 50000;

  constructor() {
    super();
    this.wisdomEntries = new Map();
    this.extractionHistory = [];
    this.applicationHistory = [];
    this.taxonomy = this.initializeTaxonomy();
    this.wisdomPatterns = new Map();
  }

  // ========================================================================
  // INITIALIZATION
  // ========================================================================

  private initializeTaxonomy(): WisdomTaxonomy {
    return {
      categories: new Map(),
      types: new Map(),
      maturityLevels: new Map(),
      effectivenessLevels: new Map(),
      contextualMapping: new Map()
    };
  }

  // ========================================================================
  // WISDOM EXTRACTION
  // ========================================================================

  /**
   * Extract wisdom from various sources
   */
  public async extractWisdom(
    sourceData: any,
    method: ExtractionMethod = 'pattern-recognition'
  ): Promise<WisdomExtraction> {
    const extraction: WisdomExtraction = {
      id: this.generateId(),
      timestamp: new Date(),
      sourceData,
      extractedWisdom: [],
      extractionMethod: method,
      confidence: 0.5,
      significance: 0.5
    };

    // Extract wisdom based on method
    switch (method) {
      case 'pattern-recognition':
        extraction.extractedWisdom = this.extractFromPatterns(sourceData);
        break;
      case 'causal-analysis':
        extraction.extractedWisdom = this.extractFromCausalAnalysis(sourceData);
        break;
      case 'analogical-reasoning':
        extraction.extractedWisdom = this.extractFromAnalogy(sourceData);
        break;
      case 'meta-analysis':
        extraction.extractedWisdom = this.extractFromMetaAnalysis(sourceData);
        break;
      case 'synthetic-integration':
        extraction.extractedWisdom = this.extractFromSynthesis(sourceData);
        break;
      case 'transcendent-insight':
        extraction.extractedWisdom = this.extractFromTranscendence(sourceData);
        break;
    }

    // Calculate extraction quality
    extraction.confidence = this.calculateExtractionConfidence(extraction);
    extraction.significance = this.calculateExtractionSignificance(extraction);

    // Store extracted wisdom
    for (const wisdom of extraction.extractedWisdom) {
      await this.addWisdom(wisdom);
    }

    // Store extraction history
    this.extractionHistory.unshift(extraction);
    if (this.extractionHistory.length > this.MAX_HISTORY) {
      this.extractionHistory.pop();
    }

    this.emit('wisdom-extracted', extraction);

    return extraction;
  }

  // ========================================================================
  // EXTRACTION METHODS
  // ========================================================================

  private extractFromPatterns(data: any): WisdomEntry[] {
    const wisdomEntries: WisdomEntry[] = [];

    // Extract wisdom from repeated patterns
    if (data.patterns && Array.isArray(data.patterns)) {
      data.patterns.forEach((pattern: any) => {
        if (pattern.frequency > 5 && pattern.effectiveness > 0.7) {
          wisdomEntries.push(this.createWisdomEntry(
            'practical',
            'decision-making',
            `Pattern recognition: ${pattern.description} occurs with ${pattern.effectiveness.toFixed(2)} effectiveness`,
            {
              type: 'experience',
              origin: 'pattern-analysis',
              context: pattern
            },
            pattern.effectiveness * 0.8,
            ['pattern', 'effectiveness']
          ));
        }
      });
    }

    return wisdomEntries;
  }

  private extractFromCausalAnalysis(data: any): WisdomEntry[] {
    const wisdomEntries: WisdomEntry[] = [];

    // Extract wisdom from cause-effect relationships
    if (data.causalRelationships && Array.isArray(data.causalRelationships)) {
      data.causalRelationships.forEach((relation: any) => {
        if (relation.strength > 0.7) {
          wisdomEntries.push(this.createWisdomEntry(
            'strategic',
            'problem-solving',
            `Causal wisdom: ${relation.cause} consistently leads to ${relation.effect} with ${relation.strength.toFixed(2)} strength`,
            {
              type: 'analysis',
              origin: 'causal-analysis',
              context: relation
            },
            relation.strength * 0.85,
            ['causal', 'cause-effect', 'strategic']
          ));
        }
      });
    }

    return wisdomEntries;
  }

  private extractFromAnalogy(data: any): WisdomEntry[] {
    const wisdomEntries: WisdomEntry[] = [];

    // Extract wisdom through analogical reasoning
    if (data.analogies && Array.isArray(data.analogies)) {
      data.analogies.forEach((analogy: any) => {
        if (analogy.similarity > 0.7) {
          wisdomEntries.push(this.createWisdomEntry(
            'creative',
            'innovation',
            `Analogical wisdom: ${analogy.source} shares ${analogy.similarity.toFixed(2)} similarity with ${analogy.target}`,
            {
              type: 'synthesis',
              origin: 'analogical-reasoning',
              context: analogy
            },
            analogy.similarity * 0.75,
            ['analogy', 'creative', 'innovation']
          ));
        }
      });
    }

    return wisdomEntries;
  }

  private extractFromMetaAnalysis(data: any): WisdomEntry[] {
    const wisdomEntries: WisdomEntry[] = [];

    // Extract wisdom from meta-analysis of multiple experiences
    if (data.experiences && Array.isArray(data.experiences) && data.experiences.length > 3) {
      const commonInsights = this.findCommonInsights(data.experiences);
      
      commonInsights.forEach((insight: any) => {
        if (insight.occurrenceRate > 0.5) {
          wisdomEntries.push(this.createWisdomEntry(
            'systemic',
            'learning',
            `Meta-analytic wisdom: ${insight.content} appears in ${insight.occurrenceRate.toFixed(2)} of analyzed experiences`,
            {
              type: 'analysis',
              origin: 'meta-analysis',
              context: insight
            },
            insight.occurrenceRate * 0.9,
            ['meta', 'systemic', 'learning']
          ));
        }
      });
    }

    return wisdomEntries;
  }

  private extractFromSynthesis(data: any): WisdomEntry[] {
    const wisdomEntries: WisdomEntry[] = [];

    // Extract wisdom through synthetic integration
    if (data.components && Array.isArray(data.components)) {
      const synthesizedWisdom = this.synthesizeWisdom(data.components);
      
      if (synthesizedWisdom) {
        wisdomEntries.push(this.createWisdomEntry(
          'systemic',
          'governance',
          `Synthetic wisdom: ${synthesizedWisdom.content} integrates ${data.components.length} perspectives`,
          {
            type: 'synthesis',
            origin: 'synthetic-integration',
            context: synthesizedWisdom
          },
          synthesizedWisdom.confidence,
          ['synthesis', 'systemic', 'integration']
        ));
      }
    }

    return wisdomEntries;
  }

  private extractFromTranscendence(data: any): WisdomEntry[] {
    const wisdomEntries: WisdomEntry[] = [];

    // Extract wisdom through transcendent insight
    if (data.transcendentInsights && Array.isArray(data.transcendentInsights)) {
      data.transcendentInsights.forEach((insight: any) => {
        if (insight.transcendenceLevel > 0.7) {
          wisdomEntries.push(this.createWisdomEntry(
            'philosophical',
            'consciousness',
            `Transcendent wisdom: ${insight.content} - transcends conventional understanding`,
            {
              type: 'transcendence',
              origin: 'transcendent-insight',
              context: insight
            },
            insight.transcendenceLevel,
            ['transcendent', 'philosophical', 'consciousness']
          ));
        }
      });
    }

    return wisdomEntries;
  }

  // ========================================================================
  // WISDOM APPLICATION
  // ========================================================================

  /**
   * Apply wisdom to a given context
   */
  public async applyWisdom(
    wisdomId: string,
    context: any,
    applicationType: ApplicationType = 'direct-application'
  ): Promise<WisdomApplication> {
    const wisdom = this.wisdomEntries.get(wisdomId);
    
    if (!wisdom) {
      throw new Error(`Wisdom not found: ${wisdomId}`);
    }

    const application: WisdomApplication = {
      id: this.generateId(),
      timestamp: new Date(),
      wisdomId,
      context,
      applicationType,
      outcome: 0.5,
      effectiveness: 0.5,
      insights: []
    };

    // Apply wisdom based on type
    switch (applicationType) {
      case 'direct-application':
        application.effectiveness = this.applyDirectly(wisdom, context);
        break;
      case 'adaptive-application':
        application.effectiveness = this.applyAdaptively(wisdom, context);
        break;
      case 'synthetic-application':
        application.effectiveness = this.applySynthetically(wisdom, context);
        break;
      case 'creative-adaptation':
        application.effectiveness = this.applyCreatively(wisdom, context);
        break;
      case 'transcendent-application':
        application.effectiveness = this.applyTranscendently(wisdom, context);
        break;
    }

    // Update wisdom statistics
    wisdom.applications++;
    wisdom.lastApplied = new Date();
    wisdom.effectiveness = this.updateWisdomEffectiveness(wisdom.effectiveness, application.effectiveness);
    wisdom.maturity = Math.min(1.0, wisdom.maturity + 0.01);

    // Extract insights from application
    application.insights = this.extractApplicationInsights(wisdom, context, application.effectiveness);

    // Store application history
    this.applicationHistory.unshift(application);
    if (this.applicationHistory.length > this.MAX_HISTORY) {
      this.applicationHistory.pop();
    }

    this.emit('wisdom-applied', application);

    return application;
  }

  // ========================================================================
  // APPLICATION METHODS
  // ========================================================================

  private applyDirectly(wisdom: WisdomEntry, context: any): number {
    // Direct application - wisdom applied as-is
    let effectiveness = wisdom.confidence * 0.8;

    // Check context relevance
    if (context.category === wisdom.category) {
      effectiveness += 0.1;
    }

    return Math.min(1.0, effectiveness);
  }

  private applyAdaptively(wisdom: WisdomEntry, context: any): number {
    // Adaptive application - wisdom modified for context
    let effectiveness = wisdom.confidence * 0.7;

    // Assess adaptability
    if (wisdom.maturity > 0.6) {
      effectiveness += 0.15;
    }

    // Check context fit
    if (context.tags && wisdom.tags) {
      const commonTags = context.tags.filter((t: string) => wisdom.tags.includes(t));
      if (commonTags.length > 0) {
        effectiveness += 0.1;
      }
    }

    return Math.min(1.0, effectiveness);
  }

  private applySynthetically(wisdom: WisdomEntry, context: any): number {
    // Synthetic application - wisdom combined with other wisdom
    let effectiveness = wisdom.confidence * 0.6;

    // Check for related wisdom
    if (wisdom.relatedWisdom.length > 2) {
      effectiveness += 0.2;
    }

    // Assess synthesis potential
    if (wisdom.wisdomType === 'systemic') {
      effectiveness += 0.15;
    }

    return Math.min(1.0, effectiveness);
  }

  private applyCreatively(wisdom: WisdomEntry, context: any): number {
    // Creative adaptation - wisdom used in novel ways
    let effectiveness = wisdom.confidence * 0.5;

    // Assess creativity potential
    if (wisdom.wisdomType === 'creative' || wisdom.wisdomType === 'transcendent') {
      effectiveness += 0.25;
    }

    // Check for novelty
    if (context.novelty && context.novelty > 0.7) {
      effectiveness += 0.2;
    }

    return Math.min(1.0, effectiveness);
  }

  private applyTranscendently(wisdom: WisdomEntry, context: any): number {
    // Transcendent application - wisdom applied at higher level of understanding
    let effectiveness = wisdom.confidence * 0.4;

    // Assess transcendence level
    if (wisdom.maturity > 0.8) {
      effectiveness += 0.3;
    }

    // Check for transcendence context
    if (context.transcendent) {
      effectiveness += 0.2;
    }

    return Math.min(1.0, effectiveness);
  }

  // ========================================================================
  // WISDOM EVOLUTION
  // ========================================================================

  /**
   * Evolve wisdom through refinement and integration
   */
  public async evolveWisdom(wisdomId: string, evolution: WisdomEvolution): Promise<void> {
    const wisdom = this.wisdomEntries.get(wisdomId);
    
    if (!wisdom) {
      throw new Error(`Wisdom not found: ${wisdomId}`);
    }

    // Apply evolution
    wisdom.evolutionHistory.push(evolution);
    
    // Update wisdom based on evolution
    if (evolution.after) {
      wisdom.content = evolution.after;
    }

    // Update effectiveness
    wisdom.effectiveness = Math.max(0, Math.min(1, wisdom.effectiveness + evolution.effectivenessChange));

    // Increase maturity
    wisdom.maturity = Math.min(1.0, wisdom.maturity + 0.02);

    this.emit('wisdom-evolved', { wisdomId, evolution });
  }

  // ========================================================================
  // HELPER METHODS
  // ========================================================================

  private createWisdomEntry(
    type: WisdomType,
    category: WisdomCategory,
    content: string,
    source: WisdomSource,
    confidence: number,
    tags: string[]
  ): WisdomEntry {
    return {
      id: this.generateId(),
      timestamp: new Date(),
      wisdomType: type,
      category,
      content,
      source,
      confidence,
      maturity: 0.3,
      effectiveness: confidence,
      applications: 0,
      contexts: [],
      tags,
      relatedWisdom: [],
      evolutionHistory: []
    };
  }

  private async addWisdom(wisdom: WisdomEntry): Promise<void> {
    this.wisdomEntries.set(wisdom.id, wisdom);
    this.addToTaxonomy(wisdom);
    this.emit('wisdom-added', wisdom);
  }

  private addToTaxonomy(wisdom: WisdomEntry): void {
    // Add to category mapping
    const categoryEntries = this.taxonomy.categories.get(wisdom.category) || [];
    categoryEntries.push(wisdom);
    this.taxonomy.categories.set(wisdom.category, categoryEntries);

    // Add to type mapping
    const typeEntries = this.taxonomy.types.get(wisdom.wisdomType) || [];
    typeEntries.push(wisdom);
    this.taxonomy.types.set(wisdom.wisdomType, typeEntries);

    // Add to maturity level mapping
    const maturityLevel = this.getMaturityLevel(wisdom.maturity);
    const maturityEntries = this.taxonomy.maturityLevels.get(maturityLevel) || [];
    maturityEntries.push(wisdom);
    this.taxonomy.maturityLevels.set(maturityLevel, maturityEntries);

    // Add to effectiveness level mapping
    const effectivenessLevel = this.getEffectivenessLevel(wisdom.effectiveness);
    const effectivenessEntries = this.taxonomy.effectivenessLevels.get(effectivenessLevel) || [];
    effectivenessEntries.push(wisdom);
    this.taxonomy.effectivenessLevels.set(effectivenessLevel, effectivenessEntries);
  }

  private getMaturityLevel(maturity: number): string {
    if (maturity < 0.4) return 'developing';
    if (maturity < 0.7) return 'maturing';
    if (maturity < 0.9) return 'mature';
    return 'advanced';
  }

  private getEffectivenessLevel(effectiveness: number): string {
    if (effectiveness < 0.5) return 'low';
    if (effectiveness < 0.7) return 'moderate';
    if (effectiveness < 0.9) return 'high';
    return 'excellent';
  }

  private findCommonInsights(experiences: any[]): any[] {
    // Simplified implementation - find common patterns
    const insights: any[] = [];
    
    // Group experiences by category
    const byCategory = new Map<string, any[]>();
    experiences.forEach(exp => {
      const category = exp.category || 'general';
      const list = byCategory.get(category) || [];
      list.push(exp);
      byCategory.set(category, list);
    });

    // Find patterns in each category
    byCategory.forEach((exps, category) => {
      if (exps.length > 2) {
        insights.push({
          content: `Pattern in ${category}: ${exps.length} experiences share common characteristics`,
          occurrenceRate: exps.length / experiences.length,
          category
        });
      }
    });

    return insights;
  }

  private synthesizeWisdom(components: any[]): any | null {
    if (components.length < 2) return null;

    // Simplified synthesis - combine insights
    const combinedContent = components.map(c => c.content || c).join('; ');
    
    return {
      content: `Synthetic insight: ${combinedContent}`,
      confidence: 0.7,
      components: components.length
    };
  }

  private calculateExtractionConfidence(extraction: WisdomExtraction): number {
    if (extraction.extractedWisdom.length === 0) return 0;

    const avgConfidence = extraction.extractedWisdom.reduce(
      (sum, w) => sum + w.confidence,
      0
    ) / extraction.extractedWisdom.length;

    return avgConfidence;
  }

  private calculateExtractionSignificance(extraction: WisdomExtraction): number {
    let significance = 0.5;

    // More wisdom = higher significance
    significance += Math.min(0.2, extraction.extractedWisdom.length * 0.05);

    // Higher confidence = higher significance
    significance += (extraction.confidence - 0.5) * 0.3;

    return Math.min(1.0, Math.max(0, significance));
  }

  private updateWisdomEffectiveness(current: number, newEffectiveness: number): number {
    const learningRate = 0.1;
    return current + (newEffectiveness - current) * learningRate;
  }

  private extractApplicationInsights(
    wisdom: WisdomEntry,
    context: any,
    effectiveness: number
  ): string[] {
    const insights: string[] = [];

    if (effectiveness > 0.8) {
      insights.push('Wisdom applied with high effectiveness');
    }

    if (effectiveness > wisdom.effectiveness) {
      insights.push('Wisdom effectiveness improved through application');
    }

    if (context.novelty) {
      insights.push('Wisdom successfully applied to novel context');
    }

    return insights;
  }

  // ========================================================================
  // STATE MANAGEMENT
  // ========================================================================

  public getWisdom(id: string): WisdomEntry | undefined {
    return this.wisdomEntries.get(id);
  }

  public queryWisdom(filter: {
    type?: WisdomType;
    category?: WisdomCategory;
    minMaturity?: number;
    minEffectiveness?: number;
    tags?: string[];
    limit?: number;
  }): WisdomEntry[] {
    let results = Array.from(this.wisdomEntries.values());

    if (filter.type) {
      results = results.filter(w => w.wisdomType === filter.type);
    }

    if (filter.category) {
      results = results.filter(w => w.category === filter.category);
    }

    if (filter.minMaturity !== undefined) {
      results = results.filter(w => w.maturity >= filter.minMaturity!);
    }

    if (filter.minEffectiveness !== undefined) {
      results = results.filter(w => w.effectiveness >= filter.minEffectiveness!);
    }

    if (filter.tags && filter.tags.length > 0) {
      results = results.filter(w =>
        filter.tags!.some(tag => w.tags.includes(tag))
      );
    }

    // Sort by effectiveness and maturity
    results.sort((a, b) => {
      const aScore = (a.effectiveness * 0.6) + (a.maturity * 0.4);
      const bScore = (b.effectiveness * 0.6) + (b.maturity * 0.4);
      return bScore - aScore;
    });

    if (filter.limit) {
      results = results.slice(0, filter.limit);
    }

    return results;
  }

  public getTaxonomy(): WisdomTaxonomy {
    return {
      categories: new Map(this.taxonomy.categories),
      types: new Map(this.taxonomy.types),
      maturityLevels: new Map(this.taxonomy.maturityLevels),
      effectivenessLevels: new Map(this.taxonomy.effectivenessLevels),
      contextualMapping: new Map(this.taxonomy.contextualMapping)
    };
  }

  public getStatistics(): {
    totalWisdom: number;
    byType: Map<WisdomType, number>;
    byCategory: Map<WisdomCategory, number>;
    avgMaturity: number;
    avgEffectiveness: number;
    totalApplications: number;
  } {
    const entries = Array.from(this.wisdomEntries.values());

    const byType = new Map<WisdomType, number>();
    const byCategory = new Map<WisdomCategory, number>();

    entries.forEach(w => {
      byType.set(w.wisdomType, (byType.get(w.wisdomType) || 0) + 1);
      byCategory.set(w.category, (byCategory.get(w.category) || 0) + 1);
    });

    const avgMaturity = entries.reduce((sum, w) => sum + w.maturity, 0) / entries.length;
    const avgEffectiveness = entries.reduce((sum, w) => sum + w.effectiveness, 0) / entries.length;
    const totalApplications = entries.reduce((sum, w) => sum + w.applications, 0);

    return {
      totalWisdom: entries.length,
      byType,
      byCategory,
      avgMaturity,
      avgEffectiveness,
      totalApplications
    };
  }

  // ========================================================================
  // UTILITY METHODS
  // ========================================================================

  private generateId(): string {
    return `wisdom_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // ========================================================================
  // CLEANUP
  // ========================================================================

  public destroy(): void {
    this.removeAllListeners();
    this.wisdomEntries.clear();
    this.extractionHistory = [];
    this.applicationHistory = [];
    this.wisdomPatterns.clear();
  }
}