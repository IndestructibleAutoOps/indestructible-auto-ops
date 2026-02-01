/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Cognitive Mesh Routing - Cognitive Routing
 * @GL-layer: GL11
 * @GL-semantic: mesh-cognitive-routing
 * @GL-audit-trail: ../../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Automatically routes tasks to optimal agents and strategies
 */

import { MeshMemory, MemoryQuery } from '../mesh-memory';
import { CognitiveNode } from '../mesh-nodes';

export interface RoutingDecision {
  targetNodeId: string;
  targetAgentId: string;
  strategyId?: string;
  confidence: number;
  reasoning: string[];
  alternativePaths: RoutingDecision[];
}

export interface RoutingRequest {
  taskType: string;
  requiredCapabilities: string[];
  priority: number; // 1-10
  context: {
    semanticKey?: string;
    previousAttempts?: string[];
    metadata?: Record<string, any>;
  };
}

export interface RoutingConfig {
  enableSemanticRouting: boolean;
  enableLoadBalancing: boolean;
  enablePerformanceBasedRouting: boolean;
  fallbackThreshold: number;
}

export class MeshRouting {
  private memory: MeshMemory;
  private config: RoutingConfig;
  private routingHistory: Map<string, RoutingDecision[]> = new Map();

  constructor(memory: MeshMemory, config?: Partial<RoutingConfig>) {
    this.memory = memory;
    this.config = {
      enableSemanticRouting: true,
      enableLoadBalancing: true,
      enablePerformanceBasedRouting: true,
      fallbackThreshold: 0.6,
      ...config
    };
  }

  /**
   * Route a task to the optimal agent
   */
  async route(request: RoutingRequest, availableNodes: CognitiveNode[]): Promise<RoutingDecision> {
    // Filter nodes by required capabilities
    const capableNodes = availableNodes.filter(node =>
      request.requiredCapabilities.every(cap => node.capabilities.includes(cap))
    );

    if (capableNodes.length === 0) {
      throw new Error('No capable nodes available');
    }

    // Score nodes based on multiple factors
    const scoredNodes = await this.scoreNodes(capableNodes, request);

    // Sort by score
    scoredNodes.sort((a, b) => b.score - a.score);

    const bestChoice = scoredNodes[0];
    const alternatives = scoredNodes.slice(1, 5).map(s => ({
      targetNodeId: s.node.id,
      targetAgentId: s.node.agentId,
      confidence: s.score,
      reasoning: s.reasoning,
      alternativePaths: []
    }));

    const decision: RoutingDecision = {
      targetNodeId: bestChoice.node.id,
      targetAgentId: bestChoice.node.agentId,
      strategyId: await this.findBestStrategy(request),
      confidence: bestChoice.score,
      reasoning: bestChoice.reasoning,
      alternativePaths: alternatives
    };

    // Record routing decision
    this.recordDecision(request, decision);

    return decision;
  }

  /**
   * Score nodes based on routing strategy
   */
  private async scoreNodes(
    nodes: CognitiveNode[],
    request: RoutingRequest
  ): Promise<Array<{ node: CognitiveNode; score: number; reasoning: string[] }>> {
    const results = [];

    for (const node of nodes) {
      let score = 0;
      const reasoning: string[] = [];

      // Load-based scoring
      if (this.config.enableLoadBalancing) {
        const loadScore = (1 - node.load) * 0.3;
        score += loadScore;
        reasoning.push(`Load score: ${loadScore.toFixed(3)} (load: ${node.load.toFixed(2)})`);
      }

      // Performance-based scoring
      if (this.config.enablePerformanceBasedRouting) {
        const totalTasks = node.performance.tasksCompleted + node.performance.tasksFailed;
        const successRate = totalTasks > 0 ? node.performance.tasksCompleted / totalTasks : 1.0;
        const perfScore = successRate * 0.3;
        score += perfScore;
        reasoning.push(`Performance score: ${perfScore.toFixed(3)} (success rate: ${(successRate * 100).toFixed(1)}%)`);
      }

      // Semantic-based scoring
      if (this.config.enableSemanticRouting && request.context.semanticKey) {
        const semanticScore = await this.calculateSemanticScore(node, request.context.semanticKey);
        score += semanticScore * 0.4;
        reasoning.push(`Semantic score: ${semanticScore.toFixed(3)}`);
      }

      results.push({ node, score, reasoning });
    }

    return results;
  }

  /**
   * Calculate semantic compatibility score
   */
  private async calculateSemanticScore(node: CognitiveNode, semanticKey: string): Promise<number> {
    const query: MemoryQuery = {
      type: 'semantic',
      source: node.agentId,
      semanticKey
    };

    const memories = await this.memory.query(query);
    
    // Check if node has experience with similar semantics
    const semanticProfile = node.metadata.semanticProfile || [];
    const hasSimilarSemantic = semanticProfile.some(profile => 
      semanticKey.includes(profile) || profile.includes(semanticKey)
    );

    if (hasSimilarSemantic) {
      return 1.0;
    }

    // Base score on memory relevance
    if (memories.length > 0) {
      return 0.8;
    }

    return 0.5; // Default score for capable but inexperienced nodes
  }

  /**
   * Find best strategy for the request
   */
  private async findBestStrategy(request: RoutingRequest): Promise<string | undefined> {
    const query: MemoryQuery = {
      type: 'strategy',
      tags: request.requiredCapabilities,
      minConfidence: 0.7,
      limit: 1
    };

    const strategies = await this.memory.query(query);
    return strategies.length > 0 ? strategies[0].id : undefined;
  }

  /**
   * Record routing decision for learning
   */
  private recordDecision(request: RoutingRequest, decision: RoutingDecision): void {
    const key = this.getRequestKey(request);
    if (!this.routingHistory.has(key)) {
      this.routingHistory.set(key, []);
    }

    this.routingHistory.get(key)!.push(decision);

    // Store in mesh memory for learning
    this.memory.store({
      id: `routing_${Date.now()}_${decision.targetNodeId}`,
      type: 'semantic',
      data: {
        request,
        decision
      },
      metadata: {
        source: 'mesh-routing',
        timestamp: new Date(),
        confidence: decision.confidence,
        tags: ['routing', 'decision', request.taskType, ...request.requiredCapabilities]
      },
      semanticKey: request.context.semanticKey || request.taskType
    });
  }

  /**
   * Get routing history for learning
   */
  getRoutingHistory(taskType: string): RoutingDecision[] {
    const history: RoutingDecision[] = [];
    
    for (const decisions of this.routingHistory.values()) {
      history.push(...decisions.filter(d => 
        d.reasoning.some(r => r.includes(taskType))
      ));
    }

    return history;
  }

  private getRequestKey(request: RoutingRequest): string {
    return `${request.taskType}_${request.requiredCapabilities.join('_')}`;
  }
}