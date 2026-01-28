/**
 * GL Evolutionary Memory
 * @GL-layer: GL12
 * @GL-semantic: evolutionary-memory
 * @GL-audit-trail: ../../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Remembers successful strategies, effective repairs, optimal DAG orderings,
 * stable mesh structures, and effective federation patterns across versions.
 */

import { EventEmitter } from 'events';

export interface MemoryEntry {
  id: string;
  type: 'strategy' | 'repair' | 'dag-ordering' | 'mesh-structure' | 'federation-pattern';
  data: any;
  metrics: {
    successRate: number;
    effectiveness: number;
    usageCount: number;
    lastUsed: Date;
  };
  context: {
    version: string;
    scenario: string;
    timestamp: Date;
  };
  tags: string[];
}

export interface MemoryQuery {
  type?: string;
  minSuccessRate?: number;
  minEffectiveness?: number;
  tags?: string[];
  limit?: number;
}

export class EvolutionaryMemory extends EventEmitter {
  private memory: Map<string, MemoryEntry> = new Map();
  private tagIndex: Map<string, string[]> = new Map();
  private maxSize: number = 10000;
  private retentionDays: number = 365;

  constructor(maxSize?: number, retentionDays?: number) {
    super();
    if (maxSize) this.maxSize = maxSize;
    if (retentionDays) this.retentionDays = retentionDays;
  }

  /**
   * Store a memory entry
   */
  async store(entry: MemoryEntry): Promise<void> {
    // Check capacity
    if (this.memory.size >= this.maxSize) {
      this.evictLeastUsed();
    }

    // Index by tags
    for (const tag of entry.tags) {
      if (!this.tagIndex.has(tag)) {
        this.tagIndex.set(tag, []);
      }
      this.tagIndex.get(tag)!.push(entry.id);
    }

    this.memory.set(entry.id, entry);
    this.emit('memory-stored', { id: entry.id, type: entry.type });
  }

  /**
   * Retrieve memory entry by ID
   */
  async get(id: string): Promise<MemoryEntry | undefined> {
    const entry = this.memory.get(id);
    if (entry) {
      entry.metrics.usageCount++;
      entry.metrics.lastUsed = new Date();
    }
    return entry;
  }

  /**
   * Query memory with filters
   */
  async query(query: MemoryQuery): Promise<MemoryEntry[]> {
    let results = Array.from(this.memory.values());

    // Filter by type
    if (query.type) {
      results = results.filter(e => e.type === query.type);
    }

    // Filter by success rate
    if (query.minSuccessRate !== undefined) {
      results = results.filter(e => e.metrics.successRate >= query.minSuccessRate!);
    }

    // Filter by effectiveness
    if (query.minEffectiveness !== undefined) {
      results = results.filter(e => e.metrics.effectiveness >= query.minEffectiveness!);
    }

    // Filter by tags
    if (query.tags && query.tags.length > 0) {
      results = results.filter(e => 
        query.tags!.some(tag => e.tags.includes(tag))
      );
    }

    // Sort by effectiveness (descending)
    results.sort((a, b) => b.metrics.effectiveness - a.metrics.effectiveness);

    // Limit results
    if (query.limit && query.limit > 0) {
      results = results.slice(0, query.limit);
    }

    return results;
  }

  /**
   * Find best strategy for scenario
   */
  async findBestStrategy(scenario: string): Promise<MemoryEntry | undefined> {
    const strategies = await this.query({
      type: 'strategy',
      tags: [scenario],
      limit: 1
    });

    return strategies.length > 0 ? strategies[0] : undefined;
  }

  /**
   * Find best repair for issue type
   */
  async findBestRepair(issueType: string): Promise<MemoryEntry | undefined> {
    const repairs = await this.query({
      type: 'repair',
      tags: [issueType],
      limit: 1
    });

    return repairs.length > 0 ? repairs[0] : undefined;
  }

  /**
   * Find optimal DAG ordering
   */
  async findOptimalDAGOrdering(dagId: string): Promise<MemoryEntry | undefined> {
    const orderings = await this.query({
      type: 'dag-ordering',
      tags: [dagId],
      limit: 1
    });

    return orderings.length > 0 ? orderings[0] : undefined;
  }

  /**
   * Find stable mesh structure
   */
  async findStableMeshStructure(meshId: string): Promise<MemoryEntry | undefined> {
    const structures = await this.query({
      type: 'mesh-structure',
      tags: [meshId],
      limit: 1
    });

    return structures.length > 0 ? structures[0] : undefined;
  }

  /**
   * Find effective federation pattern
   */
  async findEffectiveFederationPattern(scenario: string): Promise<MemoryEntry | undefined> {
    const patterns = await this.query({
      type: 'federation-pattern',
      tags: [scenario],
      limit: 1
    });

    return patterns.length > 0 ? patterns[0] : undefined;
  }

  /**
   * Update memory entry metrics
   */
  async updateMetrics(id: string, updates: Partial<MemoryEntry['metrics']>): Promise<boolean> {
    const entry = this.memory.get(id);
    if (!entry) {
      return false;
    }

    Object.assign(entry.metrics, updates);
    this.emit('memory-updated', { id });
    return true;
  }

  /**
   * Delete memory entry
   */
  async delete(id: string): Promise<boolean> {
    const entry = this.memory.get(id);
    if (!entry) {
      return false;
    }

    // Remove from tag index
    for (const tag of entry.tags) {
      const ids = this.tagIndex.get(tag);
      if (ids) {
        const idx = ids.indexOf(id);
        if (idx !== -1) {
          ids.splice(idx, 1);
        }
      }
    }

    this.memory.delete(id);
    this.emit('memory-deleted', { id });
    return true;
  }

  /**
   * Evict least used entries
   */
  private evictLeastUsed(): void {
    const entries = Array.from(this.memory.values());
    entries.sort((a, b) => a.metrics.usageCount - b.metrics.usageCount);
    
    const toRemove = entries.slice(0, Math.floor(entries.length * 0.1));
    for (const entry of toRemove) {
      this.delete(entry.id);
    }
  }

  /**
   * Get memory statistics
   */
  getStatistics() {
    const entries = Array.from(this.memory.values());
    
    return {
      totalEntries: entries.length,
      byType: this.groupByType(entries),
      averageSuccessRate: this.average(entries.map(e => e.metrics.successRate)),
      averageEffectiveness: this.average(entries.map(e => e.metrics.effectiveness)),
      totalUsageCount: entries.reduce((sum, e) => sum + e.metrics.usageCount, 0)
    };
  }

  private groupByType(entries: MemoryEntry[]): Record<string, number> {
    const groups: Record<string, number> = {};
    for (const entry of entries) {
      groups[entry.type] = (groups[entry.type] || 0) + 1;
    }
    return groups;
  }

  private average(values: number[]): number {
    if (values.length === 0) return 0;
    return values.reduce((sum, v) => sum + v, 0) / values.length;
  }

  /**
   * Get all memory entries
   */
  getAll(): MemoryEntry[] {
    return Array.from(this.memory.values());
  }

  /**
   * Clear all memory
   */
  clear(): void {
    this.memory.clear();
    this.tagIndex.clear();
    this.emit('memory-cleared');
  }
}