// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Continuum Memory
 * Version 20.0.0
 * Temporal memory storage and time-indexed retrieval
 */

import {
  TemporalMemoryNode,
  TemporalContext,
  MemoryIndex,
  MemoryCompression
} from './types';
import { v4 as uuidv4 } from 'uuid';

export class TemporalContinuumMemory {
  private memoryNodes: Map<string, TemporalMemoryNode>;
  private memoryIndex: MemoryIndex;
  private compressionInfo: MemoryCompression;
  private config: {
    retentionPeriod: number;
    compressionInterval: number;
    maxMemorySize: number;
  };
  private compressionInterval: NodeJS.Timeout | null = null;

  constructor(config?: Partial<TemporalContinuumMemory['config']>) {
    this.config = {
      retentionPeriod: 7 * 24 * 60 * 60 * 1000, // 7 days
      compressionInterval: 600000, // 10 minutes
      maxMemorySize: 10000, // max nodes
      ...config
    };

    this.memoryNodes = new Map();
    this.memoryIndex = {
      timeIndex: new Map(),
      semanticIndex: new Map(),
      eventIndex: new Map()
    };

    this.compressionInfo = {
      originalSize: 0,
      compressedSize: 0,
      compressionRatio: 1.0,
      lastCompression: Date.now()
    };
  }

  /**
   * Start continuum memory
   */
  public start(): void {
    if (this.compressionInterval) {
      return;
    }

    this.compressionInterval = setInterval(() => {
      this.performMaintenance();
    }, this.config.compressionInterval);
  }

  /**
   * Stop continuum memory
   */
  public stop(): void {
    if (this.compressionInterval) {
      clearInterval(this.compressionInterval);
      this.compressionInterval = null;
    }
  }

  /**
   * Store a memory node
   */
  public storeMemory(
    data: any,
    semanticTags: string[] = [],
    relatedEvents: string[] = []
  ): string {
    if (this.memoryNodes.size >= this.config.maxMemorySize) {
      this.pruneOldMemories();
    }

    const now = Date.now();
    const timeWindow: [number, number] = [now, now];

    const temporalContext: TemporalContext = {
      timeWindow,
      relatedEvents,
      semanticTags
    };

    const memoryNode: TemporalMemoryNode = {
      id: uuidv4(),
      data,
      timestamp: now,
      temporalContext,
      retrievalCount: 0
    };

    this.memoryNodes.set(memoryNode.id, memoryNode);
    this.indexMemory(memoryNode);
    this.updateCompressionInfo(true);

    return memoryNode.id;
  }

  /**
   * Index a memory node
   */
  private indexMemory(memoryNode: TemporalMemoryNode): void {
    const { timestamp, temporalContext } = memoryNode;

    // Time index (bucket by hour)
    const hourBucket = Math.floor(timestamp / (1000 * 60 * 60));
    if (!this.memoryIndex.timeIndex.has(hourBucket)) {
      this.memoryIndex.timeIndex.set(hourBucket, []);
    }
    this.memoryIndex.timeIndex.get(hourBucket)!.push(memoryNode.id);

    // Semantic index
    for (const tag of temporalContext.semanticTags) {
      if (!this.memoryIndex.semanticIndex.has(tag)) {
        this.memoryIndex.semanticIndex.set(tag, []);
      }
      this.memoryIndex.semanticIndex.get(tag)!.push(memoryNode.id);
    }

    // Event index
    for (const eventId of temporalContext.relatedEvents) {
      if (!this.memoryIndex.eventIndex.has(eventId)) {
        this.memoryIndex.eventIndex.set(eventId, []);
      }
      this.memoryIndex.eventIndex.get(eventId)!.push(memoryNode.id);
    }
  }

  /**
   * Retrieve memory by ID
   */
  public retrieveMemory(memoryId: string): TemporalMemoryNode | null {
    const memoryNode = this.memoryNodes.get(memoryId);
    
    if (memoryNode) {
      memoryNode.retrievalCount++;
    }

    return memoryNode || null;
  }

  /**
   * Retrieve memories by time range
   */
  public retrieveByTimeRange(startTime: number, endTime: number): TemporalMemoryNode[] {
    const results: TemporalMemoryNode[] = [];
    const startHour = Math.floor(startTime / (1000 * 60 * 60));
    const endHour = Math.floor(endTime / (1000 * 60 * 60));

    for (let hour = startHour; hour <= endHour; hour++) {
      const nodeIds = this.memoryIndex.timeIndex.get(hour);
      if (nodeIds) {
        for (const nodeId of nodeIds) {
          const node = this.memoryNodes.get(nodeId);
          if (node && node.timestamp >= startTime && node.timestamp <= endTime) {
            results.push(node);
          }
        }
      }
    }

    return results;
  }

  /**
   * Retrieve memories by semantic tags
   */
  public retrieveBySemantic(tags: string[]): TemporalMemoryNode[] {
    const results = new Map<string, TemporalMemoryNode>();

    for (const tag of tags) {
      const nodeIds = this.memoryIndex.semanticIndex.get(tag);
      if (nodeIds) {
        for (const nodeId of nodeIds) {
          const node = this.memoryNodes.get(nodeId);
          if (node) {
            results.set(nodeId, node);
          }
        }
      }
    }

    return Array.from(results.values());
  }

  /**
   * Retrieve memories by event
   */
  public retrieveByEvent(eventId: string): TemporalMemoryNode[] {
    const nodeIds = this.memoryIndex.eventIndex.get(eventId);
    if (!nodeIds) {
      return [];
    }

    return nodeIds
      .map(id => this.memoryNodes.get(id))
      .filter((node): node is TemporalMemoryNode => node !== undefined);
  }

  /**
   * Search memories by content
   */
  public searchByContent(query: string, limit: number = 10): TemporalMemoryNode[] {
    const results: Array<{ node: TemporalMemoryNode; score: number }> = [];
    const queryLower = query.toLowerCase();

    for (const node of this.memoryNodes.values()) {
      const contentStr = JSON.stringify(node.data).toLowerCase();
      
      // Simple text matching
      let score = 0;
      if (contentStr.includes(queryLower)) {
        score = 1;
        
        // Boost score for exact matches
        const exactMatches = (contentStr.match(new RegExp(queryLower, 'g')) || []).length;
        score += exactMatches * 0.5;

        // Boost score based on retrieval frequency
        score += Math.min(1, node.retrievalCount * 0.1);

        results.push({ node, score });
      }
    }

    // Sort by score and return top results
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit).map(r => r.node);
  }

  /**
   * Get recent memories
   */
  public getRecentMemories(limit: number = 10): TemporalMemoryNode[] {
    const allMemories = Array.from(this.memoryNodes.values());
    allMemories.sort((a, b) => b.timestamp - a.timestamp);
    return allMemories.slice(0, limit);
  }

  /**
   * Get frequently accessed memories
   */
  public getFrequentMemories(limit: number = 10): TemporalMemoryNode[] {
    const allMemories = Array.from(this.memoryNodes.values());
    allMemories.sort((a, b) => b.retrievalCount - a.retrievalCount);
    return allMemories.slice(0, limit);
  }

  /**
   * Perform memory maintenance
   */
  private performMaintenance(): void {
    // Prune old memories
    this.pruneOldMemories();

    // Compress memory
    this.compressMemory();

    // Update compression info
    this.updateCompressionInfo(false);
  }

  /**
   * Prune old memories
   */
  private pruneOldMemories(): void {
    const now = Date.now();
    const cutoffTime = now - this.config.retentionPeriod;
    const nodesToRemove: string[] = [];

    for (const [nodeId, node] of this.memoryNodes.entries()) {
      if (node.timestamp < cutoffTime) {
        nodesToRemove.push(nodeId);
      }
    }

    for (const nodeId of nodesToRemove) {
      this.removeMemory(nodeId);
    }
  }

  /**
   * Remove memory node
   */
  private removeMemory(nodeId: string): void {
    const node = this.memoryNodes.get(nodeId);
    if (!node) {
      return;
    }

    // Remove from indices
    const hourBucket = Math.floor(node.timestamp / (1000 * 60 * 60));
    const timeIndexNodes = this.memoryIndex.timeIndex.get(hourBucket);
    if (timeIndexNodes) {
      const index = timeIndexNodes.indexOf(nodeId);
      if (index > -1) {
        timeIndexNodes.splice(index, 1);
      }
      if (timeIndexNodes.length === 0) {
        this.memoryIndex.timeIndex.delete(hourBucket);
      }
    }

    for (const tag of node.temporalContext.semanticTags) {
      const semanticNodes = this.memoryIndex.semanticIndex.get(tag);
      if (semanticNodes) {
        const index = semanticNodes.indexOf(nodeId);
        if (index > -1) {
          semanticNodes.splice(index, 1);
        }
        if (semanticNodes.length === 0) {
          this.memoryIndex.semanticIndex.delete(tag);
        }
      }
    }

    for (const eventId of node.temporalContext.relatedEvents) {
      const eventNodes = this.memoryIndex.eventIndex.get(eventId);
      if (eventNodes) {
        const index = eventNodes.indexOf(nodeId);
        if (index > -1) {
          eventNodes.splice(index, 1);
        }
        if (eventNodes.length === 0) {
          this.memoryIndex.eventIndex.delete(eventId);
        }
      }
    }

    // Remove from main storage
    this.memoryNodes.delete(nodeId);
  }

  /**
   * Compress memory
   */
  private compressMemory(): void {
    // Simplified compression: merge similar memories
    const similarMemories = this.findSimilarMemories();

    for (const [id1, id2] of similarMemories) {
      const node1 = this.memoryNodes.get(id1);
      const node2 = this.memoryNodes.get(id2);

      if (node1 && node2) {
        // Merge memories
        const mergedData = {
          merged: true,
          originalIds: [id1, id2],
          data1: node1.data,
          data2: node2.data,
          timestamp: Math.max(node1.timestamp, node2.timestamp)
        };

        // Create merged memory
        const mergedId = this.storeMemory(
          mergedData,
          [...node1.temporalContext.semanticTags, ...node2.temporalContext.semanticTags],
          [...node1.temporalContext.relatedEvents, ...node2.temporalContext.relatedEvents]
        );

        // Remove original memories
        this.removeMemory(id1);
        this.removeMemory(id2);

        // Update index to point to merged memory
        this.memoryIndex.timeIndex.set(
          Math.floor(mergedData.timestamp / (1000 * 60 * 60)),
          [mergedId]
        );
      }
    }

    this.compressionInfo.lastCompression = Date.now();
  }

  /**
   * Find similar memories
   */
  private findSimilarMemories(): Array<[string, string]> {
    const similarPairs: Array<[string, string]> = [];
    const memoryArray = Array.from(this.memoryNodes.values());

    for (let i = 0; i < memoryArray.length; i++) {
      for (let j = i + 1; j < memoryArray.length; j++) {
        const node1 = memoryArray[i];
        const node2 = memoryArray[j];

        // Check time proximity (within 1 hour)
        const timeDiff = Math.abs(node1.timestamp - node2.timestamp);
        if (timeDiff > 3600000) {
          continue;
        }

        // Check semantic overlap
        const tags1 = new Set(node1.temporalContext.semanticTags);
        const tags2 = new Set(node2.temporalContext.semanticTags);
        const overlap = [...tags1].filter(tag => tags2.has(tag)).length;

        if (overlap >= 2) {
          similarPairs.push([node1.id, node2.id]);
        }
      }
    }

    return similarPairs.slice(0, 10); // Limit to 10 pairs
  }

  /**
   * Update compression info
   */
  private updateCompressionInfo(isAddition: boolean): void {
    const currentSize = this.memoryNodes.size;

    if (isAddition) {
      this.compressionInfo.originalSize = currentSize;
    } else {
      this.compressionInfo.compressedSize = currentSize;
      if (this.compressionInfo.originalSize > 0) {
        this.compressionInfo.compressionRatio = 
          this.compressionInfo.compressedSize / this.compressionInfo.originalSize;
      }
    }
  }

  /**
   * Get memory statistics
   */
  public getStatistics(): {
    totalMemories: number;
    indexedByTime: number;
    indexedBySemantic: number;
    indexedByEvent: number;
    averageRetrievalCount: number;
    compressionRatio: number;
    memoryUtilization: number;
  } {
    const totalMemories = this.memoryNodes.size;
    const totalRetrievals = Array.from(this.memoryNodes.values())
      .reduce((sum, node) => sum + node.retrievalCount, 0);

    return {
      totalMemories,
      indexedByTime: this.memoryIndex.timeIndex.size,
      indexedBySemantic: this.memoryIndex.semanticIndex.size,
      indexedByEvent: this.memoryIndex.eventIndex.size,
      averageRetrievalCount: totalMemories > 0 ? totalRetrievals / totalMemories : 0,
      compressionRatio: this.compressionInfo.compressionRatio,
      memoryUtilization: totalMemories / this.config.maxMemorySize
    };
  }

  /**
   * Get compression info
   */
  public getCompressionInfo(): MemoryCompression {
    return this.compressionInfo;
  }

  /**
   * Clear all memories
   */
  public clearAllMemories(): void {
    this.memoryNodes.clear();
    this.memoryIndex.timeIndex.clear();
    this.memoryIndex.semanticIndex.clear();
    this.memoryIndex.eventIndex.clear();

    this.compressionInfo = {
      originalSize: 0,
      compressedSize: 0,
      compressionRatio: 1.0,
      lastCompression: Date.now()
    };
  }

  /**
   * Export memory as JSON
   */
  public exportMemory(): string {
    const data = {
      memoryNodes: Array.from(this.memoryNodes.values()),
      compressionInfo: this.compressionInfo,
      exportTime: Date.now()
    };

    return JSON.stringify(data, null, 2);
  }

  /**
   * Import memory from JSON
   */
  public importMemory(json: string): void {
    try {
      const data = JSON.parse(json);

      // Clear existing memory
      this.clearAllMemories();

      // Import memory nodes
      for (const node of data.memoryNodes) {
        this.memoryNodes.set(node.id, node);
        this.indexMemory(node);
      }

      // Import compression info
      if (data.compressionInfo) {
        this.compressionInfo = data.compressionInfo;
      }
    } catch (error) {
      console.error('Failed to import memory:', error);
    }
  }

  /**
   * Get memory by time bucket
   */
  public getByTimeBucket(hour: number): TemporalMemoryNode[] {
    const nodeIds = this.memoryIndex.timeIndex.get(hour);
    if (!nodeIds) {
      return [];
    }

    return nodeIds
      .map(id => this.memoryNodes.get(id))
      .filter((node): node is TemporalMemoryNode => node !== undefined);
  }

  /**
   * Get semantic tags
   */
  public getSemanticTags(): string[] {
    return Array.from(this.memoryIndex.semanticIndex.keys());
  }

  /**
   * Get related events
   */
  public getRelatedEvents(): string[] {
    return Array.from(this.memoryIndex.eventIndex.keys());
  }
}