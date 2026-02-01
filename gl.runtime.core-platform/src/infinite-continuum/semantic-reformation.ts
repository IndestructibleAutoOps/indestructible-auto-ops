// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Semantic Reformation
 * Version 20.0.0
 * Dynamic semantic evolution and concept boundary adaptation
 */

import {
  SemanticCluster,
  ConceptBoundary,
  SemanticReformationEvent,
  KnowledgeNode,
  KnowledgeGraph
} from './types';
import { v4 as uuidv4 } from 'uuid';

export class ContinuousSemanticReformation {
  private clusters: Map<string, SemanticCluster>;
  private conceptBoundaries: Map<string, ConceptBoundary>;
  private reformationHistory: SemanticReformationEvent[];
  private config: {
    interval: number;
    coherenceThreshold: number;
    adaptationRate: number;
    maxClusters: number;
  };
  private reformationInterval: NodeJS.Timeout | null = null;

  constructor(config?: Partial<ContinuousSemanticReformation['config']>) {
    this.config = {
      interval: 120000, // 2 minutes
      coherenceThreshold: 0.7,
      adaptationRate: 0.1,
      maxClusters: 100,
      ...config
    };

    this.clusters = new Map();
    this.conceptBoundaries = new Map();
    this.reformationHistory = [];
  }

  /**
   * Start continuous semantic reformation
   */
  public start(): void {
    if (this.reformationInterval) {
      return;
    }

    this.reformationInterval = setInterval(() => {
      this.performReformation();
    }, this.config.interval);
  }

  /**
   * Stop semantic reformation
   */
  public stop(): void {
    if (this.reformationInterval) {
      clearInterval(this.reformationInterval);
      this.reformationInterval = null;
    }
  }

  /**
   * Perform semantic reformation
   */
  private performReformation(): void {
    // Update cluster coherence
    this.updateClusterCoherence();

    // Identify clusters needing reformation
    const unstableClusters = this.identifyUnstableClusters();

    // Perform cluster operations
    for (const cluster of unstableClusters) {
      if (cluster.semanticCoherence < this.config.coherenceThreshold * 0.5) {
        this.splitCluster(cluster.id);
      } else if (cluster.semanticCoherence > this.config.coherenceThreshold * 1.5) {
        this.mergeSimilarClusters(cluster.id);
      } else {
        this.shiftClusterBoundary(cluster.id);
      }
    }

    // Adapt concept boundaries
    this.adaptConceptBoundaries();

    // Prune empty clusters
    this.pruneEmptyClusters();
  }

  /**
   * Initialize clusters from knowledge graph
   */
  public initializeClusters(knowledgeGraph: KnowledgeGraph): void {
    const nodes = Array.from(knowledgeGraph.nodes.values());
    const initialClusters = this.groupBySemanticType(nodes);

    for (const [type, nodeIds] of Object.entries(initialClusters)) {
      if (nodeIds.length > 0) {
        this.createCluster(nodeIds, type);
      }
    }

    // Initialize concept boundaries for each cluster
    for (const cluster of this.clusters.values()) {
      this.initializeConceptBoundary(cluster.id, cluster);
    }
  }

  /**
   * Group nodes by semantic type
   */
  private groupBySemanticType(nodes: KnowledgeNode[]): Record<string, string[]> {
    const groups: Record<string, string[]> = {};

    for (const node of nodes) {
      if (!groups[node.type]) {
        groups[node.type] = [];
      }
      groups[node.type].push(node.id);
    }

    return groups;
  }

  /**
   * Create a new cluster
   */
  private createCluster(nodeIds: string[], type: string): SemanticCluster {
    const cluster: SemanticCluster = {
      id: uuidv4(),
      nodeIds: [...nodeIds],
      centroid: this.calculateCentroid(nodeIds, type),
      semanticCoherence: this.calculateCoherence(nodeIds, type),
      stability: 1.0,
      lastReformation: Date.now()
    };

    this.clusters.set(cluster.id, cluster);
    return cluster;
  }

  /**
   * Calculate cluster centroid (simplified)
   */
  private calculateCentroid(nodeIds: string[], type: string): number[] {
    // Simplified centroid calculation
    // In production, this would use actual vector embeddings
    return [nodeIds.length, type.length, Date.now() % 100];
  }

  /**
   * Calculate cluster coherence
   */
  private calculateCoherence(nodeIds: string[], type: string): number {
    if (nodeIds.length === 0) {
      return 0;
    }

    // Simplified coherence calculation
    // In production, this would measure actual semantic similarity
    const baseCoherence = 0.8;
    const sizePenalty = Math.min(0.2, nodeIds.length * 0.01);
    return Math.max(0, baseCoherence - sizePenalty);
  }

  /**
   * Initialize concept boundary
   */
  private initializeConceptBoundary(clusterId: string, cluster: SemanticCluster): ConceptBoundary {
    const boundary: ConceptBoundary = {
      conceptId: clusterId,
      boundary: cluster.centroid.map(c => c * 1.2), // Initial boundary
      flexibility: 0.3,
      adaptationRate: this.config.adaptationRate
    };

    this.conceptBoundaries.set(clusterId, boundary);
    return boundary;
  }

  /**
   * Update cluster coherence
   */
  private updateClusterCoherence(): void {
    for (const cluster of this.clusters.values()) {
      cluster.semanticCoherence = this.calculateCoherence(cluster.nodeIds, 'mixed');
      cluster.stability = this.calculateStability(cluster);
      cluster.lastReformation = Date.now();
    }
  }

  /**
   * Calculate cluster stability
   */
  private calculateStability(cluster: SemanticCluster): number {
    // Stability decreases with frequent reformation
    const timeSinceReformation = Date.now() - cluster.lastReformation;
    const stabilityFactor = Math.min(1.0, timeSinceReformation / 10000);
    return cluster.stability * 0.7 + stabilityFactor * 0.3;
  }

  /**
   * Identify unstable clusters
   */
  private identifyUnstableClusters(): SemanticCluster[] {
    return Array.from(this.clusters.values()).filter(
      cluster => 
        cluster.semanticCoherence < this.config.coherenceThreshold ||
        cluster.stability < 0.5
    );
  }

  /**
   * Split cluster into multiple clusters
   */
  private splitCluster(clusterId: string): void {
    const cluster = this.clusters.get(clusterId);
    if (!cluster || cluster.nodeIds.length < 2) {
      return;
    }

    // Split nodes into two groups
    const midPoint = Math.floor(cluster.nodeIds.length / 2);
    const groupA = cluster.nodeIds.slice(0, midPoint);
    const groupB = cluster.nodeIds.slice(midPoint);

    // Create new clusters
    const clusterA = this.createCluster(groupA, 'split_A');
    const clusterB = this.createCluster(groupB, 'split_B');

    // Initialize boundaries
    this.initializeConceptBoundary(clusterA.id, clusterA);
    this.initializeConceptBoundary(clusterB.id, clusterB);

    // Remove original cluster
    this.clusters.delete(clusterId);
    this.conceptBoundaries.delete(clusterId);

    // Record event
    this.recordReformationEvent({
      id: uuidv4(),
      type: 'cluster_split',
      timestamp: Date.now(),
      affectedNodes: [...groupA, ...groupB],
      impact: 0.8
    });
  }

  /**
   * Merge similar clusters
   */
  private mergeSimilarClusters(clusterId: string): void {
    const cluster = this.clusters.get(clusterId);
    if (!cluster) {
      return;
    }

    // Find similar cluster
    let mostSimilarCluster: SemanticCluster | null = null;
    let highestSimilarity = 0;

    for (const [otherId, otherCluster] of this.clusters.entries()) {
      if (otherId === clusterId) {
        continue;
      }

      const similarity = this.calculateClusterSimilarity(cluster, otherCluster);
      if (similarity > highestSimilarity && similarity > 0.8) {
        highestSimilarity = similarity;
        mostSimilarCluster = otherCluster;
      }
    }

    if (mostSimilarCluster) {
      // Merge node IDs
      const mergedNodeIds = [...cluster.nodeIds, ...mostSimilarCluster.nodeIds];

      // Create merged cluster
      const mergedCluster = this.createCluster(mergedNodeIds, 'merged');
      this.initializeConceptBoundary(mergedCluster.id, mergedCluster);

      // Remove original clusters
      this.clusters.delete(clusterId);
      this.clusters.delete(mostSimilarCluster.id);
      this.conceptBoundaries.delete(clusterId);
      this.conceptBoundaries.delete(mostSimilarCluster.id);

      // Record event
      this.recordReformationEvent({
        id: uuidv4(),
        type: 'cluster_merge',
        timestamp: Date.now(),
        affectedNodes: mergedNodeIds,
        impact: 0.9
      });
    }
  }

  /**
   * Calculate cluster similarity
   */
  private calculateClusterSimilarity(
    clusterA: SemanticCluster,
    clusterB: SemanticCluster
  ): number {
    // Simplified similarity calculation
    const centroidDistance = this.calculateCentroidDistance(
      clusterA.centroid,
      clusterB.centroid
    );
    return Math.max(0, 1 - centroidDistance);
  }

  /**
   * Calculate centroid distance
   */
  private calculateCentroidDistance(centroidA: number[], centroidB: number[]): number {
    if (centroidA.length !== centroidB.length) {
      return 1;
    }

    let sumSquared = 0;
    for (let i = 0; i < centroidA.length; i++) {
      sumSquared += Math.pow(centroidA[i] - centroidB[i], 2);
    }

    return Math.sqrt(sumSquared) / centroidA.length;
  }

  /**
   * Shift cluster boundary
   */
  private shiftClusterBoundary(clusterId: string): void {
    const boundary = this.conceptBoundaries.get(clusterId);
    const cluster = this.clusters.get(clusterId);

    if (!boundary || !cluster) {
      return;
    }

    // Adapt boundary based on current centroid
    const adaptationRate = boundary.adaptationRate;
    for (let i = 0; i < boundary.boundary.length; i++) {
      boundary.boundary[i] = boundary.boundary[i] * (1 - adaptationRate) + 
                           cluster.centroid[i] * adaptationRate * 1.2;
    }

    // Record event
    this.recordReformationEvent({
      id: uuidv4(),
      type: 'boundary_shift',
      timestamp: Date.now(),
      affectedNodes: cluster.nodeIds,
      impact: 0.3
    });
  }

  /**
   * Adapt concept boundaries
   */
  private adaptConceptBoundaries(): void {
    for (const [clusterId, boundary] of this.conceptBoundaries.entries()) {
      const cluster = this.clusters.get(clusterId);
      if (!cluster) {
        continue;
      }

      // Update flexibility based on stability
      boundary.flexibility = Math.min(1.0, cluster.stability * 2);
    }
  }

  /**
   * Prune empty clusters
   */
  private pruneEmptyClusters(): void {
    const emptyClusters: string[] = [];

    for (const [clusterId, cluster] of this.clusters.entries()) {
      if (cluster.nodeIds.length === 0) {
        emptyClusters.push(clusterId);
      }
    }

    for (const clusterId of emptyClusters) {
      this.clusters.delete(clusterId);
      this.conceptBoundaries.delete(clusterId);
    }
  }

  /**
   * Record reformation event
   */
  private recordReformationEvent(event: SemanticReformationEvent): void {
    this.reformationHistory.push(event);

    // Keep only last 1000 events
    if (this.reformationHistory.length > 1000) {
      this.reformationHistory = this.reformationHistory.slice(-1000);
    }
  }

  /**
   * Get clusters
   */
  public getClusters(): SemanticCluster[] {
    return Array.from(this.clusters.values());
  }

  /**
   * Get concept boundaries
   */
  public getConceptBoundaries(): ConceptBoundary[] {
    return Array.from(this.conceptBoundaries.values());
  }

  /**
   * Get reformation history
   */
  public getReformationHistory(limit?: number): SemanticReformationEvent[] {
    if (limit) {
      return this.reformationHistory.slice(-limit);
    }
    return this.reformationHistory;
  }

  /**
   * Find cluster for node
   */
  public findClusterForNode(nodeId: string): SemanticCluster | null {
    for (const cluster of this.clusters.values()) {
      if (cluster.nodeIds.includes(nodeId)) {
        return cluster;
      }
    }
    return null;
  }

  /**
   * Add node to appropriate cluster
   */
  public addNodeToCluster(nodeId: string, type: string): void {
    // Find best matching cluster
    let bestCluster: SemanticCluster | null = null;
    let bestScore = 0;

    for (const cluster of this.clusters.values()) {
      const score = this.calculateNodeClusterFit(nodeId, type, cluster);
      if (score > bestScore && score > 0.6) {
        bestScore = score;
        bestCluster = cluster;
      }
    }

    if (bestCluster) {
      bestCluster.nodeIds.push(nodeId);
    } else if (this.clusters.size < this.config.maxClusters) {
      // Create new cluster
      this.createCluster([nodeId], type);
      const newCluster = this.clusters.values().next().value;
      if (newCluster) {
        this.initializeConceptBoundary(newCluster.id, newCluster);
      }
    }
  }

  /**
   * Calculate node-cluster fit
   */
  private calculateNodeClusterFit(
    nodeId: string,
    type: string,
    cluster: SemanticCluster
  ): number {
    // Simplified fit calculation
    let fit = 0.5;

    if (cluster.nodeIds.length > 0) {
      // Check if cluster has similar type nodes
      fit += 0.3;
    }

    // Consider cluster stability
    fit += cluster.stability * 0.2;

    return Math.min(1.0, fit);
  }
}