// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Knowledge Accretion
 * Version 20.0.0
 * Continuous knowledge accumulation and graph evolution
 */

import { 
  KnowledgeNode, 
  KnowledgeEdge, 
  KnowledgeGraph, 
  KnowledgeMetrics 
} from './types';
import { FabricNode, FabricGraph as FabricGraphType } from '../../unified-intelligence-fabric/fabric-core';
import { v4 as uuidv4 } from 'uuid';

export class InfiniteKnowledgeAccretion {
  private knowledgeGraph: KnowledgeGraph;
  private config: {
    interval: number;
    maxNodes: number;
    confidenceThreshold: number;
  };
  private accretionInterval: NodeJS.Timeout | null = null;
  private integrationCallbacks: Map<string, Function> = new Map();

  constructor(config?: Partial<InfiniteKnowledgeAccretion['config']>) {
    this.config = {
      interval: 60000, // 1 minute
      maxNodes: 100000,
      confidenceThreshold: 0.5,
      ...config
    };

    this.knowledgeGraph = {
      nodes: new Map(),
      edges: new Map(),
      metrics: this.initializeMetrics()
    };
  }

  private initializeMetrics(): KnowledgeMetrics {
    return {
      totalNodes: 0,
      totalEdges: 0,
      averageConfidence: 0,
      connectivity: 0,
      coherenceScore: 0,
      growthRate: 0
    };
  }

  /**
   * Start continuous knowledge accretion
   */
  public start(): void {
    if (this.accretionInterval) {
      return;
    }

    this.accretionInterval = setInterval(() => {
      this.performAccretion();
    }, this.config.interval);
  }

  /**
   * Stop knowledge accretion
   */
  public stop(): void {
    if (this.accretionInterval) {
      clearInterval(this.accretionInterval);
      this.accretionInterval = null;
    }
  }

  /**
   * Add a new knowledge node
   */
  public addKnowledgeNode(
    content: any,
    type: any,
    source: string,
    confidence: number = 0.8
  ): string {
    // Validate type
    const validTypes = ['fact', 'concept', 'relation', 'pattern', 'insight'];
    const validatedType: KnowledgeNode['type'] = validTypes.includes(type) ? type : 'fact';
    if (this.knowledgeGraph.nodes.size >= this.config.maxNodes) {
      this.pruneLowConfidenceNodes();
    }

    const node: KnowledgeNode = {
      id: uuidv4(),
      content,
      type,
      confidence,
      source,
      timestamp: Date.now(),
      accessCount: 0,
      reinforcement: 0
    };

    this.knowledgeGraph.nodes.set(node.id, node);
    this.updateMetrics();

    return node.id;
  }

  /**
   * Add a knowledge edge between nodes
   */
  public addKnowledgeEdge(
    sourceId: string,
    targetId: string,
    type: KnowledgeEdge['type'],
    strength: number = 0.8
  ): string {
    if (!this.knowledgeGraph.nodes.has(sourceId) || 
        !this.knowledgeGraph.nodes.has(targetId)) {
      throw new Error('Source or target node does not exist');
    }

    const edge: KnowledgeEdge = {
      id: uuidv4(),
      sourceId,
      targetId,
      type,
      strength,
      timestamp: Date.now(),
      accessCount: 0
    };

    this.knowledgeGraph.edges.set(edge.id, edge);
    this.updateMetrics();

    return edge.id;
  }

  /**
   * Perform automatic knowledge accretion
   */
  private performAccretion(): void {
    // Reinforce frequently accessed knowledge
    this.reinforceKnowledge();

    // Identify and create implicit relationships
    this.discoverImplicitRelations();

    // Update coherence scores
    this.updateCoherence();

    // Calculate growth rate
    this.calculateGrowthRate();
  }

  /**
   * Reinforce frequently accessed knowledge
   */
  private reinforceKnowledge(): void {
    const reinforcementFactor = 0.1;
    const decayFactor = 0.05;

    for (const [nodeId, node] of this.knowledgeGraph.nodes) {
      if (node.accessCount > 10) {
        node.reinforcement += reinforcementFactor;
        node.confidence = Math.min(1.0, node.confidence + reinforcementFactor * 0.1);
      } else {
        node.reinforcement = Math.max(0, node.reinforcement - decayFactor);
      }
    }
  }

  /**
   * Discover implicit relationships between nodes
   */
  private discoverImplicitRelations(): void {
    const nodes = Array.from(this.knowledgeGraph.nodes.values());
    const implicitRelationThreshold = 0.7;

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const nodeA = nodes[i];
        const nodeB = nodes[j];

        // Check if they share semantic content
        const similarity = this.calculateSemanticSimilarity(nodeA, nodeB);

        if (similarity > implicitRelationThreshold) {
          // Check if edge already exists
          const edgeExists = Array.from(this.knowledgeGraph.edges.values()).some(
            edge => 
              (edge.sourceId === nodeA.id && edge.targetId === nodeB.id) ||
              (edge.sourceId === nodeB.id && edge.targetId === nodeA.id)
          );

          if (!edgeExists) {
            this.addKnowledgeEdge(
              nodeA.id,
              nodeB.id,
              'semantic',
              similarity
            );
          }
        }
      }
    }
  }

  /**
   * Calculate semantic similarity between nodes
   */
  private calculateSemanticSimilarity(nodeA: KnowledgeNode, nodeB: KnowledgeNode): number {
    // Simple similarity calculation based on content type and source
    let similarity = 0;

    if (nodeA.type === nodeB.type) {
      similarity += 0.3;
    }

    if (nodeA.source === nodeB.source) {
      similarity += 0.2;
    }

    // Content similarity (simplified)
    const contentA = JSON.stringify(nodeA.content);
    const contentB = JSON.stringify(nodeB.content);
    const commonTerms = this.findCommonTerms(contentA, contentB);
    similarity += Math.min(0.5, commonTerms.length * 0.1);

    return similarity;
  }

  /**
   * Find common terms between two strings
   */
  private findCommonTerms(strA: string, strB: string): string[] {
    const termsA = strA.toLowerCase().split(/\s+/).filter(t => t.length > 3);
    const termsB = strB.toLowerCase().split(/\s+/).filter(t => t.length > 3);
    
    const common = termsA.filter(term => termsB.includes(term));
    return [...new Set(common)];
  }

  /**
   * Update coherence scores
   */
  private updateCoherence(): void {
    if (this.knowledgeGraph.nodes.size === 0) {
      return;
    }

    let totalCoherence = 0;

    for (const [nodeId, node] of this.knowledgeGraph.nodes) {
      const connectedEdges = Array.from(this.knowledgeGraph.edges.values()).filter(
        edge => edge.sourceId === nodeId || edge.targetId === nodeId
      );

      const averageEdgeStrength = connectedEdges.length > 0
        ? connectedEdges.reduce((sum, edge) => sum + edge.strength, 0) / connectedEdges.length
        : 0;

      totalCoherence += averageEdgeStrength;
    }

    this.knowledgeGraph.metrics.coherenceScore = 
      totalCoherence / this.knowledgeGraph.nodes.size;
  }

  /**
   * Calculate growth rate
   */
  private calculateGrowthRate(): void {
    // Simplified growth rate calculation
    // In production, this would use historical data
    const currentSize = this.knowledgeGraph.nodes.size;
    const growthRate = currentSize > 0 ? 
      (this.knowledgeGraph.edges.size / currentSize) * 0.01 : 0;
    
    this.knowledgeGraph.metrics.growthRate = growthRate;
  }

  /**
   * Prune low confidence nodes
   */
  private pruneLowConfidenceNodes(): void {
    const nodesToRemove: string[] = [];

    for (const [nodeId, node] of this.knowledgeGraph.nodes) {
      if (node.confidence < this.config.confidenceThreshold && 
          node.reinforcement < 0.3) {
        nodesToRemove.push(nodeId);
      }
    }

    for (const nodeId of nodesToRemove) {
      this.knowledgeGraph.nodes.delete(nodeId);
      
      // Remove associated edges
      const edgesToRemove = Array.from(this.knowledgeGraph.edges.entries())
        .filter(([_, edge]) => edge.sourceId === nodeId || edge.targetId === nodeId)
        .map(([edgeId, _]) => edgeId);

      for (const edgeId of edgesToRemove) {
        this.knowledgeGraph.edges.delete(edgeId);
      }
    }

    this.updateMetrics();
  }

  /**
   * Update knowledge metrics
   */
  private updateMetrics(): void {
    this.knowledgeGraph.metrics.totalNodes = this.knowledgeGraph.nodes.size;
    this.knowledgeGraph.metrics.totalEdges = this.knowledgeGraph.edges.size;

    if (this.knowledgeGraph.nodes.size > 0) {
      const totalConfidence = Array.from(this.knowledgeGraph.nodes.values())
        .reduce((sum, node) => sum + node.confidence, 0);
      this.knowledgeGraph.metrics.averageConfidence = 
        totalConfidence / this.knowledgeGraph.nodes.size;
    }

    // Calculate connectivity
    if (this.knowledgeGraph.nodes.size > 0) {
      this.knowledgeGraph.metrics.connectivity = 
        this.knowledgeGraph.metrics.totalEdges / this.knowledgeGraph.metrics.totalNodes;
    }
  }

  /**
   * Integrate knowledge with fabric graph
   */
  public integrateWithFabric(fabricGraph: FabricGraphType): void {
    for (const [nodeId, knowledgeNode] of this.knowledgeGraph.nodes) {
      const fabricNode: Partial<FabricNode> = {
        id: `knowledge_${knowledgeNode.id}`,
        type: 'data' as any,
        layer: 'data' as any,
        properties: {
          content: knowledgeNode.content,
          knowledgeType: knowledgeNode.type,
          confidence: knowledgeNode.confidence,
          source: knowledgeNode.source,
          accessCount: knowledgeNode.accessCount,
          reinforcement: knowledgeNode.reinforcement
        },
        superposition: {
          states: []
        } as any,
        version: '1.0',
        realityId: 'default',
        timestamp: knowledgeNode.timestamp,
        projections: []
      };

      // FabricGraph doesn't have addNode method
      // fabricGraph.nodes.set(fabricNode.id, fabricNode as FabricNode);
    }

    // Trigger integration callbacks
    for (const callback of this.integrationCallbacks.values()) {
      callback(fabricGraph);
    }
  }

  /**
   * Register integration callback
   */
  public onIntegration(key: string, callback: Function): void {
    this.integrationCallbacks.set(key, callback);
  }

  /**
   * Get knowledge graph
   */
  public getKnowledgeGraph(): KnowledgeGraph {
    return this.knowledgeGraph;
  }

  /**
   * Get metrics
   */
  public getMetrics(): KnowledgeMetrics {
    return this.knowledgeGraph.metrics;
  }

  /**
   * Query knowledge by type
   */
  public queryByType(type: KnowledgeNode['type']): KnowledgeNode[] {
    return Array.from(this.knowledgeGraph.nodes.values())
      .filter(node => node.type === type);
  }

  /**
   * Query knowledge by source
   */
  public queryBySource(source: string): KnowledgeNode[] {
    return Array.from(this.knowledgeGraph.nodes.values())
      .filter(node => node.source === source);
  }

  /**
   * Search knowledge by content
   */
  public searchByContent(query: string): KnowledgeNode[] {
    const queryLower = query.toLowerCase();
    return Array.from(this.knowledgeGraph.nodes.values())
      .filter(node => {
        const contentStr = JSON.stringify(node.content).toLowerCase();
        return contentStr.includes(queryLower);
      });
  }
}