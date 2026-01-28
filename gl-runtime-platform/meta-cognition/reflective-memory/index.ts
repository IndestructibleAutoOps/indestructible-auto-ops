/**
 * GL Meta-Cognitive Runtime - Reflective Memory (Version 14.0.0)
 * 
 * The Reflective Memory provides the GL Runtime with the ability to:
 * - Remember its own mistakes
 * - Remember corrected strategies
 * - Remember improved behaviors
 * - Remember evolved directions
 * 
 * This is the "I remember what I learned" capability.
 */

import { EventEmitter } from 'events';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface ReflectiveMemoryState {
  totalMemories: number;
  memoryCategories: Map<string, number>;
  learningRate: number;
  wisdomAccumulation: number;
  lastMemoryUpdate?: Date;
}

export interface MemoryEntry {
  id: string;
  timestamp: Date;
  category: 'mistake' | 'correction' | 'improvement' | 'evolution' | 'insight' | 'wisdom';
  memoryType: string;
  content: any;
  context: any;
  lessons: string[];
  effectiveness: number;
  confidence: number;
  tags: string[];
  accessCount: number;
  lastAccessed?: Date;
}

export interface MemoryQuery {
  category?: string;
  memoryType?: string;
  tags?: string[];
  since?: Date;
  limit?: number;
  minConfidence?: number;
  minEffectiveness?: number;
}

export interface MemoryPattern {
  id: string;
  patternType: string;
  frequency: number;
  effectiveness: number;
  lastObserved: Date;
  recommendations: string[];
}

export interface WisdomEntry {
  id: string;
  timestamp: Date;
  wisdomType: 'practical' | 'strategic' | 'philosophical' | 'cultural';
  wisdom: string;
  source: string;
  applications: number;
  effectiveness: number;
  maturity: number;
}

// ============================================================================
// REFLECTIVE MEMORY CLASS
// ============================================================================

export class ReflectiveMemory extends EventEmitter {
  private state: ReflectiveMemoryState;
  private memories: Map<string, MemoryEntry>;
  private wisdom: Map<string, WisdomEntry>;
  private patterns: Map<string, MemoryPattern>;
  private semanticIndex: Map<string, string[]>; // keyword -> memory IDs
  private readonly MAX_MEMORIES = 100000;
  private readonly MAX_WISDOM = 10000;
  private readonly RETENTION_DAYS = 365;

  constructor() {
    super();
    this.state = this.initializeState();
    this.memories = new Map();
    this.wisdom = new Map();
    this.patterns = new Map();
    this.semanticIndex = new Map();
  }

  // ========================================================================
  // INITIALIZATION
  // ========================================================================

  private initializeState(): ReflectiveMemoryState {
    return {
      totalMemories: 0,
      memoryCategories: new Map(),
      learningRate: 0.5,
      wisdomAccumulation: 0.5,
    };
  }

  // ========================================================================
  // CORE MEMORY OPERATIONS
  // ========================================================================

  /**
   * Store a memory
   */
  public async storeMemory(
    category: 'mistake' | 'correction' | 'improvement' | 'evolution' | 'insight' | 'wisdom',
    memoryType: string,
    content: any,
    context: any,
    lessons: string[],
    confidence: number = 0.7,
    tags: string[] = []
  ): Promise<MemoryEntry> {
    const memory: MemoryEntry = {
      id: this.generateId(),
      timestamp: new Date(),
      category,
      memoryType,
      content,
      context,
      lessons,
      effectiveness: 0.5, // Will be updated as we learn
      confidence,
      tags,
      accessCount: 0
    };

    // Store memory
    this.memories.set(memory.id, memory);

    // Update state
    this.state.totalMemories++;
    this.updateCategoryCount(category);
    this.state.lastMemoryUpdate = new Date();

    // Update semantic index
    this.updateSemanticIndex(memory);

    // Emit event
    this.emit('memory-stored', memory);

    return memory;
  }

  /**
   * Retrieve memories
   */
  public async retrieveMemories(query: MemoryQuery): Promise<MemoryEntry[]> {
    let results = Array.from(this.memories.values());

    // Filter by category
    if (query.category) {
      results = results.filter(m => m.category === query.category);
    }

    // Filter by memory type
    if (query.memoryType) {
      results = results.filter(m => m.memoryType === query.memoryType);
    }

    // Filter by tags
    if (query.tags && query.tags.length > 0) {
      results = results.filter(m =>
        query.tags!.some(tag => m.tags.includes(tag))
      );
    }

    // Filter by date
    if (query.since) {
      results = results.filter(m => m.timestamp >= query.since!);
    }

    // Filter by confidence
    if (query.minConfidence !== undefined) {
      results = results.filter(m => m.confidence >= query.minConfidence!);
    }

    // Filter by effectiveness
    if (query.minEffectiveness !== undefined) {
      results = results.filter(m => m.effectiveness >= query.minEffectiveness!);
    }

    // Sort by effectiveness and recency
    results.sort((a, b) => {
      if (b.effectiveness !== a.effectiveness) {
        return b.effectiveness - a.effectiveness;
      }
      return b.timestamp.getTime() - a.timestamp.getTime();
    });

    // Update access counts
    results.forEach(m => {
      m.accessCount++;
      m.lastAccessed = new Date();
    });

    // Apply limit
    if (query.limit) {
      results = results.slice(0, query.limit);
    }

    return results;
  }

  /**
   * Semantic search
   */
  public async semanticSearch(keywords: string[], limit: number = 20): Promise<MemoryEntry[]> {
    const memoryIds = new Set<string>();

    // Find memories matching keywords
    keywords.forEach(keyword => {
      const ids = this.semanticIndex.get(keyword.toLowerCase()) || [];
      ids.forEach(id => memoryIds.add(id));
    });

    // Retrieve memories
    const results = Array.from(memoryIds)
      .map(id => this.memories.get(id))
      .filter((m): m is MemoryEntry => m !== undefined);

    // Sort by relevance and effectiveness
    results.sort((a, b) => {
      const aMatchScore = this.calculateMatchScore(a, keywords);
      const bMatchScore = this.calculateMatchScore(b, keywords);

      if (Math.abs(bMatchScore - aMatchScore) > 0.1) {
        return bMatchScore - aMatchScore;
      }

      return b.effectiveness - a.effectiveness;
    });

    // Update access counts
    results.forEach(m => {
      m.accessCount++;
      m.lastAccessed = new Date();
    });

    return results.slice(0, limit);
  }

  /**
   * Update memory effectiveness
   */
  public async updateMemoryEffectiveness(
    memoryId: string,
    effectiveness: number
  ): Promise<void> {
    const memory = this.memories.get(memoryId);
    if (memory) {
      memory.effectiveness = effectiveness;
      this.emit('memory-updated', memory);
    }
  }

  /**
   * Extract wisdom from memories
   */
  public async extractWisdom(
    wisdomType: 'practical' | 'strategic' | 'philosophical' | 'cultural',
    source: string,
    wisdom: string
  ): Promise<WisdomEntry> {
    const entry: WisdomEntry = {
      id: this.generateId(),
      timestamp: new Date(),
      wisdomType,
      wisdom,
      source,
      applications: 0,
      effectiveness: 0.7,
      maturity: 0.5
    };

    this.wisdom.set(entry.id, entry);
    this.state.wisdomAccumulation = this.updateWisdomAccumulation();

    this.emit('wisdom-extracted', entry);

    return entry;
  }

  /**
   * Apply wisdom
   */
  public async applyWisdom(wisdomId: string, effectiveness: number): Promise<void> {
    const wisdomEntry = this.wisdom.get(wisdomId);
    if (wisdomEntry) {
      wisdomEntry.applications++;
      wisdomEntry.effectiveness = this.updateMetric(wisdomEntry.effectiveness, effectiveness);
      wisdomEntry.maturity = Math.min(1, wisdomEntry.maturity + 0.05);
      
      this.state.wisdomAccumulation = this.updateWisdomAccumulation();
      
      this.emit('wisdom-applied', wisdomEntry);
    }
  }

  /**
   * Find similar memories
   */
  public async findSimilarMemories(memory: MemoryEntry, limit: number = 10): Promise<MemoryEntry[]> {
    const results: { memory: MemoryEntry; similarity: number }[] = [];

    for (const [id, candidate] of this.memories) {
      if (id === memory.id) continue;

      const similarity = this.calculateSimilarity(memory, candidate);
      if (similarity > 0.5) {
        results.push({ memory: candidate, similarity });
      }
    }

    // Sort by similarity
    results.sort((a, b) => b.similarity - a.similarity);

    return results.slice(0, limit).map(r => r.memory);
  }

  /**
   * Identify patterns in memories
   */
  public async identifyPatterns(): Promise<MemoryPattern[]> {
    const patternMap = new Map<string, MemoryPattern>();

    // Analyze memories for patterns
    for (const memory of this.memories.values()) {
      const patternKey = `${memory.category}:${memory.memoryType}`;
      
      let pattern = patternMap.get(patternKey);
      if (!pattern) {
        pattern = {
          id: this.generateId(),
          patternType: patternKey,
          frequency: 0,
          effectiveness: 0,
          lastObserved: new Date(),
          recommendations: []
        };
        patternMap.set(patternKey, pattern);
      }

      pattern.frequency++;
      pattern.effectiveness = this.updateMetric(pattern.effectiveness, memory.effectiveness);
      pattern.lastObserved = memory.timestamp;
    }

    // Generate recommendations for patterns
    const patterns = Array.from(patternMap.values());
    patterns.forEach(pattern => {
      pattern.recommendations = this.generatePatternRecommendations(pattern);
    });

    // Update patterns cache
    this.patterns.clear();
    patterns.forEach(p => this.patterns.set(p.id, p));

    return patterns;
  }

  // ========================================================================
  // MEMORY MAINTENANCE
  // ========================================================================

  /**
   * Clean up old memories
   */
  public async cleanupOldMemories(): Promise<number> {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.RETENTION_DAYS);

    let cleaned = 0;

    for (const [id, memory] of this.memories) {
      if (memory.timestamp < cutoffDate && memory.effectiveness < 0.5) {
        this.memories.delete(id);
        this.removeFromSemanticIndex(memory);
        cleaned++;
      }
    }

    this.state.totalMemories = this.memories.size;

    this.emit('memories-cleaned', { cleaned });

    return cleaned;
  }

  /**
   * Optimize memory storage
   */
  public async optimizeMemory(): Promise<void> {
    // Remove duplicates
    const seen = new Set<string>();
    for (const [id, memory] of this.memories) {
      const signature = this.createSignature(memory);
      if (seen.has(signature)) {
        this.memories.delete(id);
        this.removeFromSemanticIndex(memory);
      } else {
        seen.add(signature);
      }
    }

    // Update state
    this.state.totalMemories = this.memories.size;
    this.state.lastMemoryUpdate = new Date();

    this.emit('memory-optimized');
  }

  // ========================================================================
  // STATE MANAGEMENT
  // ========================================================================

  public getState(): ReflectiveMemoryState {
    return {
      ...this.state,
      memoryCategories: new Map(this.state.memoryCategories)
    };
  }

  public getWisdom(filter?: {
    type?: string;
    minMaturity?: number;
    limit?: number;
  }): WisdomEntry[] {
    let results = Array.from(this.wisdom.values());

    if (filter?.type) {
      results = results.filter(w => w.wisdomType === filter.type);
    }

    if (filter?.minMaturity !== undefined) {
      results = results.filter(w => w.maturity >= filter.minMaturity!);
    }

    // Sort by effectiveness and maturity
    results.sort((a, b) => {
      const aScore = (a.effectiveness * 0.6) + (a.maturity * 0.4);
      const bScore = (b.effectiveness * 0.6) + (b.maturity * 0.4);
      return bScore - aScore;
    });

    if (filter?.limit) {
      results = results.slice(0, filter.limit);
    }

    return results;
  }

  // ========================================================================
  // HELPER METHODS
  // ========================================================================

  private updateCategoryCount(category: string): void {
    const count = this.state.memoryCategories.get(category) || 0;
    this.state.memoryCategories.set(category, count + 1);
  }

  private updateSemanticIndex(memory: MemoryEntry): void {
    // Extract keywords from tags and content
    const keywords = [
      ...memory.tags,
      memory.category,
      memory.memoryType,
      ...Object.keys(memory.context || {})
    ];

    keywords.forEach(keyword => {
      const key = keyword.toLowerCase();
      const ids = this.semanticIndex.get(key) || [];
      if (!ids.includes(memory.id)) {
        ids.push(memory.id);
      }
      this.semanticIndex.set(key, ids);
    });
  }

  private removeFromSemanticIndex(memory: MemoryEntry): void {
    const keywords = [
      ...memory.tags,
      memory.category,
      memory.memoryType,
      ...Object.keys(memory.context || {})
    ];

    keywords.forEach(keyword => {
      const key = keyword.toLowerCase();
      const ids = this.semanticIndex.get(key) || [];
      const filtered = ids.filter(id => id !== memory.id);
      
      if (filtered.length > 0) {
        this.semanticIndex.set(key, filtered);
      } else {
        this.semanticIndex.delete(key);
      }
    });
  }

  private calculateMatchScore(memory: MemoryEntry, keywords: string[]): number {
    let matches = 0;
    keywords.forEach(keyword => {
      if (memory.tags.includes(keyword) ||
          memory.memoryType.includes(keyword) ||
          memory.category.includes(keyword)) {
        matches++;
      }
    });

    return matches / keywords.length;
  }

  private calculateSimilarity(memory1: MemoryEntry, memory2: MemoryEntry): number {
    let similarity = 0;

    // Category match
    if (memory1.category === memory2.category) similarity += 0.3;

    // Memory type match
    if (memory1.memoryType === memory2.memoryType) similarity += 0.2;

    // Tag overlap
    const commonTags = memory1.tags.filter(tag => memory2.tags.includes(tag));
    if (memory1.tags.length > 0 || memory2.tags.length > 0) {
      similarity += (commonTags.length / Math.max(memory1.tags.length, memory2.tags.length)) * 0.3;
    }

    // Context similarity
    const contextKeys1 = Object.keys(memory1.context || {});
    const contextKeys2 = Object.keys(memory2.context || {});
    const commonContext = contextKeys1.filter(key => contextKeys2.includes(key));
    if (contextKeys1.length > 0 || contextKeys2.length > 0) {
      similarity += (commonContext.length / Math.max(contextKeys1.length, contextKeys2.length)) * 0.2;
    }

    return similarity;
  }

  private createSignature(memory: MemoryEntry): string {
    return `${memory.category}:${memory.memoryType}:${JSON.stringify(memory.content)}`;
  }

  private generatePatternRecommendations(pattern: MemoryPattern): string[] {
    const recommendations: string[] = [];

    if (pattern.frequency > 10 && pattern.effectiveness > 0.7) {
      recommendations.push('This pattern is highly effective - consider making it a standard practice');
    }

    if (pattern.frequency > 10 && pattern.effectiveness < 0.5) {
      recommendations.push('This pattern occurs frequently but is ineffective - review and improve');
    }

    if (pattern.effectiveness > 0.8) {
      recommendations.push('Highly effective pattern - document as best practice');
    }

    return recommendations;
  }

  private updateMetric(current: number, newValue: number): number {
    const learningRate = 0.1;
    return current + (newValue - current) * learningRate;
  }

  private updateWisdomAccumulation(): number {
    if (this.wisdom.size === 0) return 0.5;

    const totalEffectiveness = Array.from(this.wisdom.values())
      .reduce((sum, w) => sum + w.effectiveness, 0);

    const totalMaturity = Array.from(this.wisdom.values())
      .reduce((sum, w) => sum + w.maturity, 0);

    return ((totalEffectiveness / this.wisdom.size) * 0.6) +
           ((totalMaturity / this.wisdom.size) * 0.4);
  }

  private generateId(): string {
    return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // ========================================================================
  // CLEANUP
  // ========================================================================

  public destroy(): void {
    this.removeAllListeners();
    this.memories.clear();
    this.wisdom.clear();
    this.patterns.clear();
    this.semanticIndex.clear();
  }
}