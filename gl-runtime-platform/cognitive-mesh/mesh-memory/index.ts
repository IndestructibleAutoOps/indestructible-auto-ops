/**
 * GL Cognitive Mesh Memory - Global Shared Memory
 * @GL-layer: GL11
 * @GL-semantic: mesh-shared-memory
 * @GL-audit-trail: ../../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Provides global shared memory across all agents in the mesh
 */

import { EventEmitter } from 'events';

export interface MemoryEntry {
  id: string;
  type: 'semantic' | 'resource' | 'strategy' | 'dag' | 'federation' | 'repair';
  data: any;
  metadata: {
    source: string;
    timestamp: Date;
    confidence: number;
    tags: string[];
  };
  semanticKey?: string;
}

export interface MemoryQuery {
  type?: string;
  tags?: string[];
  semanticKey?: string;
  source?: string;
  minConfidence?: number;
  limit?: number;
}

export class MeshMemory extends EventEmitter {
  private entries: Map<string, MemoryEntry> = new Map();
  private semanticIndex: Map<string, string[]> = new Map(); // semanticKey -> entry IDs
  private tagIndex: Map<string, string[]> = new Map(); // tag -> entry IDs
  private maxEntries: number = 100000;
  private retentionDays: number = 90;
  private initialized: boolean = false;

  constructor(maxEntries?: number, retentionDays?: number) {
    super();
    if (maxEntries) this.maxEntries = maxEntries;
    if (retentionDays) this.retentionDays = retentionDays;
  }

  async initialize(): Promise<void> {
    this.initialized = true;
    this.startCleanupTask();
    this.emit('initialized');
  }

  /**
   * Store data in shared memory
   */
  async store(entry: MemoryEntry): Promise<void> {
    if (!this.initialized) {
      throw new Error('MeshMemory not initialized');
    }

    // Check capacity
    if (this.entries.size >= this.maxEntries) {
      this.evictOldest();
    }

    // Index by semantic key
    if (entry.semanticKey) {
      if (!this.semanticIndex.has(entry.semanticKey)) {
        this.semanticIndex.set(entry.semanticKey, []);
      }
      this.semanticIndex.get(entry.semanticKey)!.push(entry.id);
    }

    // Index by tags
    for (const tag of entry.metadata.tags) {
      if (!this.tagIndex.has(tag)) {
        this.tagIndex.set(tag, []);
      }
      this.tagIndex.get(tag)!.push(entry.id);
    }

    this.entries.set(entry.id, entry);
    this.emit('stored', { id: entry.id, type: entry.type });
  }

  /**
   * Retrieve data by ID
   */
  async get(id: string): Promise<MemoryEntry | undefined> {
    return this.entries.get(id);
  }

  /**
   * Query memory with filters
   */
  async query(query: MemoryQuery): Promise<MemoryEntry[]> {
    let results: MemoryEntry[] = Array.from(this.entries.values());

    // Filter by type
    if (query.type) {
      results = results.filter(e => e.type === query.type);
    }

    // Filter by source
    if (query.source) {
      results = results.filter(e => e.metadata.source === query.source);
    }

    // Filter by confidence
    if (query.minConfidence !== undefined) {
      const minConf = query.minConfidence ?? 0;
      results = results.filter(e => e.metadata.confidence >= minConf);
    }

    // Filter by semantic key
    if (query.semanticKey) {
      const ids = this.semanticIndex.get(query.semanticKey) || [];
      results = results.filter(e => ids.includes(e.id));
    }

    // Filter by tags (all tags must match)
    if (query.tags && query.tags.length > 0) {
      results = results.filter(e => {
        return query.tags!.every(tag => e.metadata.tags.includes(tag));
      });
    }

    // Sort by confidence (descending)
    results.sort((a, b) => b.metadata.confidence - a.metadata.confidence);

    // Limit results
    if (query.limit && query.limit > 0) {
      results = results.slice(0, query.limit);
    }

    return results;
  }

  /**
   * Semantic search - find entries with similar semantic keys
   */
  async semanticSearch(semanticKey: string, limit: number = 10): Promise<MemoryEntry[]> {
    const relatedIds: string[] = [];
    
    // Find entries with matching semantic keys
    for (const [key, ids] of this.semanticIndex.entries()) {
      if (key.includes(semanticKey) || semanticKey.includes(key)) {
        relatedIds.push(...ids);
      }
    }

    // Remove duplicates and get entries
    const uniqueIds = [...new Set(relatedIds)];
    const entries = await Promise.all(
      uniqueIds.map(id => this.get(id))
    );
    
    const results = entries.filter((e): e is MemoryEntry => e !== undefined);
    return results.slice(0, limit);
  }

  /**
   * Update existing entry
   */
  async update(id: string, updates: Partial<MemoryEntry>): Promise<boolean> {
    const entry = this.entries.get(id);
    if (!entry) {
      return false;
    }

    Object.assign(entry, updates);
    this.emit('updated', { id });
    return true;
  }

  /**
   * Delete entry
   */
  async delete(id: string): Promise<boolean> {
    const entry = this.entries.get(id);
    if (!entry) {
      return false;
    }

    // Remove from semantic index
    if (entry.semanticKey) {
      const ids = this.semanticIndex.get(entry.semanticKey);
      if (ids) {
        const idx = ids.indexOf(id);
        if (idx !== -1) {
          ids.splice(idx, 1);
        }
      }
    }

    // Remove from tag indexes
    for (const tag of entry.metadata.tags) {
      const ids = this.tagIndex.get(tag);
      if (ids) {
        const idx = ids.indexOf(id);
        if (idx !== -1) {
          ids.splice(idx, 1);
        }
      }
    }

    this.entries.delete(id);
    this.emit('deleted', { id });
    return true;
  }

  getSize(): number {
    return this.entries.size;
  }

  private evictOldest(): void {
    const entries = Array.from(this.entries.values());
    entries.sort((a, b) => a.metadata.timestamp.getTime() - b.metadata.timestamp.getTime());
    
    const toRemove = entries.slice(0, Math.floor(entries.length * 0.1));
    for (const entry of toRemove) {
      this.delete(entry.id);
    }
  }

  private startCleanupTask(): void {
    setInterval(() => {
      this.cleanup();
    }, 3600000); // Every hour
  }

  private cleanup(): void {
    const now = new Date();
    const retentionCutoff = new Date(now.getTime() - (this.retentionDays * 24 * 60 * 60 * 1000));
    
    const entries = Array.from(this.entries.values());
    for (const entry of entries) {
      if (entry.metadata.timestamp < retentionCutoff) {
        this.delete(entry.id);
      }
    }
  }
}