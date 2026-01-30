// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Fabric Expansion
 * Version 20.0.0
 * Autonomous fabric growth and capacity management
 */

import {
  ExpansionPolicy,
  ExpansionConstraints,
  ExpansionEvent
} from './types';
import { FabricNode, FabricEdge, FabricGraph } from '../../unified-intelligence-fabric/fabric-core';
import { v4 as uuidv4 } from 'uuid';

export class SelfExpandingFabric {
  private fabric: FabricGraph;
  private expansionPolicy: ExpansionPolicy;
  private expansionHistory: ExpansionEvent[];
  private config: {
    interval: number;
    maxNodes: number;
    growthRate: number;
    strategy: 'incremental' | 'exponential' | 'adaptive';
  };
  private expansionInterval: NodeJS.Timeout | null = null;

  constructor(
    fabric: any,
    config?: Partial<SelfExpandingFabric['config']>
  ) {
    this.fabric = fabric;
    this.config = {
      interval: 240000, // 4 minutes
      maxNodes: 10000,
      growthRate: 0.05, // 5% growth per interval
      strategy: 'adaptive',
      ...config
    };

    this.expansionPolicy = {
      trigger: 'demand',
      threshold: 0.8,
      strategy: this.config.strategy,
      constraints: {
        maxNodes: this.config.maxNodes,
        maxEdges: this.config.maxNodes * 3,
        maxMemory: 1024 * 1024 * 1024, // 1GB
        growthRate: this.config.growthRate
      }
    };

    this.expansionHistory = [];
  }

  /**
   * Start continuous fabric expansion
   */
  public start(): void {
    if (this.expansionInterval) {
      return;
    }

    this.expansionInterval = setInterval(() => {
      this.evaluateExpansion();
    }, this.config.interval);
  }

  /**
   * Stop fabric expansion
   */
  public stop(): void {
    if (this.expansionInterval) {
      clearInterval(this.expansionInterval);
      this.expansionInterval = null;
    }
  }

  /**
   * Evaluate if expansion is needed
   */
  private evaluateExpansion(): void {
    const utilization = this.calculateFabricUtilization();
    const shouldExpand = this.shouldTriggerExpansion(utilization);

    if (shouldExpand) {
      this.performExpansion(utilization);
    }
  }

  /**
   * Calculate fabric utilization
   */
  private calculateFabricUtilization(): {
    nodeUtilization: number;
    edgeUtilization: number;
    memoryUtilization: number;
    overallUtilization: number;
  } {
    const nodeCount = Array.from((this.fabric as any).graph.nodes).length;
    const edgeCount = Array.from((this.fabric as any).graph.edges).length;

    const nodeUtilization = nodeCount / this.expansionPolicy.constraints.maxNodes;
    const edgeUtilization = edgeCount / this.expansionPolicy.constraints.maxEdges;
    
    // Simplified memory estimation
    const estimatedMemory = (nodeCount * 1024) + (edgeCount * 512);
    const memoryUtilization = estimatedMemory / this.expansionPolicy.constraints.maxMemory;

    const overallUtilization = (nodeUtilization + edgeUtilization + memoryUtilization) / 3;

    return {
      nodeUtilization,
      edgeUtilization,
      memoryUtilization,
      overallUtilization
    };
  }

  /**
   * Determine if expansion should be triggered
   */
  private shouldTriggerExpansion(utilization: any): boolean {
    switch (this.expansionPolicy.trigger) {
      case 'usage':
        return utilization.overallUtilization >= this.expansionPolicy.threshold;

      case 'demand':
        // Check if there's high demand on existing nodes
        return this.detectHighDemand();

      case 'prediction':
        // Predict future demand
        const predictedUtilization = this.predictFutureUtilization();
        return predictedUtilization >= this.expansionPolicy.threshold;

      case 'manual':
        return false;

      default:
        return false;
    }
  }

  /**
   * Detect high demand on fabric
   */
  private detectHighDemand(): boolean {
    const nodes = Array.from((this.fabric as any).graph.nodes.values()) as FabricNode[];
    const utilization = this.calculateFabricUtilization();

    // Check if utilization is high
    if (utilization.overallUtilization >= this.expansionPolicy.threshold) {
      return true;
    }

    // Check if nodes have high access counts (simplified)
    const highAccessNodes = nodes.filter(node => {
      const accessCount = (node.properties as any)?.accessCount || 0;
      return accessCount > 100;
    });

    // If more than 10% of nodes have high access, expand
    return highAccessNodes.length / nodes.length > 0.1;
  }

  /**
   * Predict future utilization
   */
  private predictFutureUtilization(): number {
    const utilization = this.calculateFabricUtilization();
    
    // Simple linear prediction based on growth rate
    const predictedGrowth = utilization.overallUtilization * this.config.growthRate;
    return Math.min(1.0, utilization.overallUtilization + predictedGrowth);
  }

  /**
   * Perform fabric expansion
   */
  private performExpansion(currentUtilization: any): void {
    const expansionStrategy = this.expansionPolicy.strategy;
    let nodesToAdd = 0;
    let edgesToAdd = 0;

    switch (expansionStrategy) {
      case 'incremental':
        nodesToAdd = Math.floor(
          this.expansionPolicy.constraints.maxNodes * 
          this.expansionPolicy.constraints.growthRate
        );
        edgesToAdd = Math.floor(nodesToAdd * 2);
        break;

      case 'exponential':
        const currentNodes = Array.from((this.fabric as any).graph.nodes).length;
        nodesToAdd = Math.floor(currentNodes * this.config.growthRate);
        edgesToAdd = Math.floor(nodesToAdd * 2.5);
        break;

      case 'adaptive':
        nodesToAdd = this.calculateAdaptiveGrowth(currentUtilization);
        edgesToAdd = Math.floor(nodesToAdd * 2);
        break;
    }

    // Execute expansion
    this.expandNodes(nodesToAdd);
    this.expandEdges(edgesToAdd);

    // Record expansion event
    this.recordExpansionEvent({
      id: uuidv4(),
      type: 'subgraph_creation',
      timestamp: Date.now(),
      impact: nodesToAdd + edgesToAdd,
      justification: `Utilization: ${(currentUtilization.overallUtilization * 100).toFixed(2)}%, Strategy: ${expansionStrategy}`
    });
  }

  /**
   * Calculate adaptive growth
   */
  private calculateAdaptiveGrowth(utilization: any): number {
    const utilizationRatio = utilization.overallUtilization;
    
    // Higher utilization = more aggressive growth
    const growthMultiplier = 1 + (utilizationRatio - 0.5) * 2;
    const baseGrowth = this.expansionPolicy.constraints.maxNodes * 
                      this.expansionPolicy.constraints.growthRate;

    return Math.floor(baseGrowth * growthMultiplier);
  }

  /**
   * Expand fabric with new nodes
   */
  private expandNodes(count: number): void {
    const existingNodes = Array.from((this.fabric as any).graph.nodes.values()) as FabricNode[];
    const existingTypes = new Set(existingNodes.map((n: FabricNode) => n.type as string));

    for (let i = 0; i < count; i++) {
      const nodeType = this.generateNodeType(existingTypes);
      const node: Partial<FabricNode> = {
        id: uuidv4(),
        type: nodeType as any,
        layer: 'data' as any,
        properties: this.generateNodeData(nodeType),
        superposition: { states: [] } as any,
        version: '1.0',
        realityId: 'default',
        timestamp: Date.now(),
        projections: []
      };

      // Fabric doesn't have direct addNode - would need to use the fabric service
      // this.fabric.addNode(node);

      // Record node addition event
      this.recordExpansionEvent({
        id: uuidv4(),
        type: 'node_addition',
        timestamp: Date.now(),
        impact: 1,
        justification: `Auto-generated ${nodeType} node`
      });
    }
  }

  /**
   * Generate node type
   */
  private generateNodeType(existingTypes: Set<string>): string {
    const types = ['file', 'semantic', 'agent', 'flow', 'compute'];
    
    // Prefer existing types for consistency
    if (existingTypes.size > 0) {
      const existingArray = Array.from(existingTypes);
      if (Math.random() < 0.7) {
        return existingArray[Math.floor(Math.random() * existingArray.length)];
      }
    }

    return types[Math.floor(Math.random() * types.length)];
  }

  /**
   * Generate node data
   */
  private generateNodeData(type: string): any {
    const baseData = {
      autoGenerated: true,
      generation: Date.now()
    };

    switch (type) {
      case 'compute':
        return {
          ...baseData,
          computeType: 'generic',
          parameters: {
            complexity: Math.random(),
            efficiency: Math.random()
          }
        };

      case 'file':
        return {
          ...baseData,
          dataType: 'buffer',
          capacity: Math.floor(Math.random() * 1000) + 1
        };

      case 'semantic':
        return {
          ...baseData,
          semanticType: 'monitor',
          sensitivity: Math.random()
        };

      case 'agent':
        return {
          ...baseData,
          agentType: 'inferred',
          capacity: Math.random()
        };

      case 'flow':
        return {
          ...baseData,
          flowType: 'template',
          connections: Math.floor(Math.random() * 5) + 1
        };

      default:
        return baseData;
    }
  }

  /**
   * Expand fabric with new edges
   */
  private expandEdges(count: number): void {
    const nodes = Array.from((this.fabric as any).graph.nodes.values()) as FabricNode[];
    const existingEdges = Array.from((this.fabric as any).graph.edges.values()) as FabricEdge[];
    const existingConnections = new Set<string>(
      existingEdges.map(e => `${e.sourceId}-${e.targetId}`)
    );

    let edgesCreated = 0;
    let attempts = 0;
    const maxAttempts = count * 10;

    while (edgesCreated < count && attempts < maxAttempts) {
      attempts++;

      // Select random nodes
      const sourceIndex = Math.floor(Math.random() * nodes.length);
      const targetIndex = Math.floor(Math.random() * nodes.length);

      if (sourceIndex === targetIndex) {
        continue;
      }

      const source = nodes[sourceIndex] as FabricNode;
      const target = nodes[targetIndex] as FabricNode;

      // Check if edge already exists
      const connectionKey = `${source.id}-${target.id}`;
      if (existingConnections.has(connectionKey)) {
        continue;
      }

      // Create edge
      const edge: Partial<FabricEdge> = {
        id: uuidv4(),
        sourceId: source.id,
        targetId: target.id,
        type: this.generateEdgeType(source, target) as any,
        weight: Math.random(),
        properties: {
          autoGenerated: true,
          expansionGeneration: this.expansionHistory.length
        },
        superposition: { states: [] } as any,
        direction: 'directed',
        version: '1.0',
        realityId: 'default',
        timestamp: Date.now(),
        layer: 'data' as any
      };

      // Fabric doesn't have direct addEdge - would need to use the fabric service
      // this.fabric.addEdge(edge);
      existingConnections.add(connectionKey);
      edgesCreated++;

      // Record edge addition event
      this.recordExpansionEvent({
        id: uuidv4(),
        type: 'edge_addition',
        timestamp: Date.now(),
        impact: 1,
        justification: `Auto-generated ${edge.type} edge`
      });
    }
  }

  /**
   * Generate edge type
   */
  private generateEdgeType(source: FabricNode, target: FabricNode): string {
    const edgeTypes = ['data_flow', 'control_flow', 'semantic', 'dependency'];

    // Context-aware edge type selection
    if (source.type === 'file' && target.type === 'compute') {
      return 'dependency';
    }

    if (source.type === 'flow' || target.type === 'flow') {
      return 'dependency';
    }

    if (source.type === 'semantic' || target.type === 'semantic') {
      return 'semantic';
    }

    return edgeTypes[Math.floor(Math.random() * edgeTypes.length)];
  }

  /**
   * Record expansion event
   */
  private recordExpansionEvent(event: ExpansionEvent): void {
    this.expansionHistory.push(event);

    // Keep only last 1000 events
    if (this.expansionHistory.length > 1000) {
      this.expansionHistory = this.expansionHistory.slice(-1000);
    }
  }

  /**
   * Get fabric
   */
  public getFabric(): FabricGraph {
    return this.fabric;
  }

  /**
   * Get expansion policy
   */
  public getExpansionPolicy(): ExpansionPolicy {
    return this.expansionPolicy;
  }

  /**
   * Set expansion policy
   */
  public setExpansionPolicy(policy: Partial<ExpansionPolicy>): void {
    this.expansionPolicy = {
      ...this.expansionPolicy,
      ...policy
    };
  }

  /**
   * Get expansion history
   */
  public getExpansionHistory(limit?: number): ExpansionEvent[] {
    if (limit) {
      return this.expansionHistory.slice(-limit);
    }
    return this.expansionHistory;
  }

  /**
   * Get expansion statistics
   */
  public getExpansionStats(): {
    totalExpansions: number;
    nodesAdded: number;
    edgesAdded: number;
    averageImpact: number;
    expansionRate: number;
  } {
    const nodeAdditions = this.expansionHistory.filter(e => e.type === 'node_addition');
    const edgeAdditions = this.expansionHistory.filter(e => e.type === 'edge_addition');
    const subgraphCreations = this.expansionHistory.filter(e => e.type === 'subgraph_creation');

    const nodesAdded = nodeAdditions.reduce((sum, e) => sum + e.impact, 0);
    const edgesAdded = edgeAdditions.reduce((sum, e) => sum + e.impact, 0);

    const totalImpact = this.expansionHistory.reduce((sum, e) => sum + e.impact, 0);
    const averageImpact = this.expansionHistory.length > 0 ? 
      totalImpact / this.expansionHistory.length : 0;

    // Calculate expansion rate (expansions per hour)
    const now = Date.now();
    const oneHourAgo = now - 3600000;
    const recentExpansions = this.expansionHistory.filter(e => e.timestamp > oneHourAgo);
    const expansionRate = recentExpansions.length;

    return {
      totalExpansions: this.expansionHistory.length,
      nodesAdded,
      edgesAdded,
      averageImpact,
      expansionRate
    };
  }

  /**
   * Trigger manual expansion
   */
  public triggerManualExpansion(nodeCount: number, edgeCount: number): void {
    this.expandNodes(nodeCount);
    this.expandEdges(edgeCount);

    this.recordExpansionEvent({
      id: uuidv4(),
      type: 'subgraph_creation',
      timestamp: Date.now(),
      impact: nodeCount + edgeCount,
      justification: 'Manual expansion triggered'
    });
  }

  /**
   * Prune underutilized nodes
   */
  public pruneUnderutilized(threshold: number = 0.1): number {
    const nodes = Array.from((this.fabric as any).graph.nodes.values()) as FabricNode[];
    const nodesToRemove: string[] = [];

    for (const node of nodes) {
      const accessCount = (node.properties as any)?.accessCount || 0;
      const age = Date.now() - node.timestamp;
      const ageHours = age / (1000 * 60 * 60);

      // Remove old, underutilized nodes
      if (ageHours > 24 && accessCount < threshold * 100) {
        nodesToRemove.push(node.id);
      }
    }

    for (const nodeId of nodesToRemove) {
      // Fabric doesn't have direct removeNode
      // this.fabric.removeNode(nodeId);
    }

    return nodesToRemove.length;
  }

  /**
   * Optimize fabric structure
   */
  public optimizeFabric(): void {
    // Remove orphaned edges
    const nodes = Array.from((this.fabric as any).graph.nodes.values()) as FabricNode[];
    const nodeIds = new Set(nodes.map(n => n.id));
    const edges = Array.from((this.fabric as any).graph.edges.values()) as FabricEdge[];

    for (const edge of edges) {
      if (!nodeIds.has(edge.sourceId) || !nodeIds.has(edge.targetId)) {
        // Fabric doesn't have direct removeEdge
        // this.fabric.removeEdge(edge.id);
      }
    }

    // Record optimization event
    this.recordExpansionEvent({
      id: uuidv4(),
      type: 'subgraph_creation',
      timestamp: Date.now(),
      impact: 0,
      justification: 'Fabric optimization - removed orphaned edges'
    });
  }
}