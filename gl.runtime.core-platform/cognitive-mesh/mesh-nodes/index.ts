/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Cognitive Mesh Nodes - Distributed Cognitive Nodes
 * @GL-layer: GL11
 * @GL-semantic: mesh-cognitive-nodes
 * @GL-audit-trail: ../../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Manages cognitive nodes (agents) that connect to the mesh
 */

import { EventEmitter } from 'events';
import { MeshMemory } from '../mesh-memory';

export interface CognitiveNode {
  id: string;
  agentId: string;
  capabilities: string[];
  status: 'active' | 'idle' | 'busy' | 'offline';
  load: number; // 0-1
  performance: {
    tasksCompleted: number;
    tasksFailed: number;
    averageTaskTime: number;
  };
  metadata: {
    joinedAt: Date;
    lastActivity: Date;
    semanticProfile: string[];
  };
}

export interface NodeCapability {
  name: string;
  level: number; // 0-10
  experience: number;
}

export class MeshNodes extends EventEmitter {
  private nodes: Map<string, CognitiveNode> = new Map();
  private maxNodes: number;
  private initialized: boolean = false;

  constructor(maxNodes: number = 100) {
    super();
    this.maxNodes = maxNodes;
  }

  async initialize(): Promise<void> {
    this.initialized = true;
    this.emit('initialized');
  }

  /**
   * Register a new cognitive node (agent)
   */
  async registerNode(node: Omit<CognitiveNode, 'id'>): Promise<string> {
    if (!this.initialized) {
      throw new Error('MeshNodes not initialized');
    }

    if (this.nodes.size >= this.maxNodes) {
      throw new Error('Max nodes reached');
    }

    const id = `node_${node.agentId}_${Date.now()}`;
    const newNode: CognitiveNode = {
      id,
      ...node,
      metadata: {
        ...node.metadata,
        joinedAt: new Date(),
        lastActivity: new Date()
      }
    };

    this.nodes.set(id, newNode);
    this.emit('node-registered', { nodeId: id, agentId: node.agentId });
    this.emit('node-activated', newNode);
    
    return id;
  }

  /**
   * Unregister a node
   */
  async unregisterNode(nodeId: string): Promise<boolean> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      return false;
    }

    this.nodes.delete(nodeId);
    this.emit('node-unregistered', { nodeId, agentId: node.agentId });
    return true;
  }

  /**
   * Update node status
   */
  async updateNodeStatus(nodeId: string, status: CognitiveNode['status']): Promise<boolean> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      return false;
    }

    node.status = status;
    node.metadata.lastActivity = new Date();
    this.emit('node-status-updated', { nodeId, status });
    return true;
  }

  /**
   * Update node load
   */
  async updateNodeLoad(nodeId: string, load: number): Promise<boolean> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      return false;
    }

    node.load = Math.max(0, Math.min(1, load));
    node.metadata.lastActivity = new Date();
    return true;
  }

  /**
   * Record task completion
   */
  async recordTaskCompletion(nodeId: string, success: boolean, duration: number): Promise<boolean> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      return false;
    }

    if (success) {
      node.performance.tasksCompleted++;
    } else {
      node.performance.tasksFailed++;
    }

    // Update average task time
    const totalTasks = node.performance.tasksCompleted + node.performance.tasksFailed;
    node.performance.averageTaskTime = 
      (node.performance.averageTaskTime * (totalTasks - 1) + duration) / totalTasks;

    node.metadata.lastActivity = new Date();
    return true;
  }

  /**
   * Get node by ID
   */
  getNode(nodeId: string): CognitiveNode | undefined {
    return this.nodes.get(nodeId);
  }

  /**
   * Get node by agent ID
   */
  getNodeByAgentId(agentId: string): CognitiveNode | undefined {
    for (const node of this.nodes.values()) {
      if (node.agentId === agentId) {
        return node;
      }
    }
    return undefined;
  }

  /**
   * Get all active nodes
   */
  getActiveNodes(): CognitiveNode[] {
    return Array.from(this.nodes.values()).filter(n => n.status === 'active' || n.status === 'idle');
  }

  /**
   * Get all nodes
   */
  getAllNodes(): CognitiveNode[] {
    return Array.from(this.nodes.values());
  }

  /**
   * Get active nodes count
   */
  getActiveNodesCount(): number {
    return this.getActiveNodes().length;
  }

  /**
   * Find nodes by capability
   */
  findNodesByCapability(capability: string): CognitiveNode[] {
    return this.getActiveNodes().filter(n => 
      n.capabilities.includes(capability)
    );
  }

  /**
   * Find best node for task based on load and performance
   */
  findBestNode(capabilities: string[]): CognitiveNode | undefined {
    const candidates = this.getActiveNodes().filter(n => 
      capabilities.every(cap => n.capabilities.includes(cap))
    );

    if (candidates.length === 0) {
      return undefined;
    }

    // Score nodes based on load (lower is better) and success rate (higher is better)
    const scored = candidates.map(node => {
      const totalTasks = node.performance.tasksCompleted + node.performance.tasksFailed;
      const successRate = totalTasks > 0 ? node.performance.tasksCompleted / totalTasks : 1.0;
      const score = (1 - node.load) * 0.6 + successRate * 0.4;
      return { node, score };
    });

    scored.sort((a, b) => b.score - a.score);
    return scored[0].node;
  }

  /**
   * Get node statistics
   */
  getStatistics() {
    const nodes = Array.from(this.nodes.values());
    const active = nodes.filter(n => n.status === 'active' || n.status === 'idle');
    
    return {
      total: nodes.length,
      active: active.length,
      idle: nodes.filter(n => n.status === 'idle').length,
      busy: nodes.filter(n => n.status === 'busy').length,
      offline: nodes.filter(n => n.status === 'offline').length,
      averageLoad: active.length > 0 
        ? active.reduce((sum, n) => sum + n.load, 0) / active.length 
        : 0,
      totalTasksCompleted: nodes.reduce((sum, n) => sum + n.performance.tasksCompleted, 0),
      totalTasksFailed: nodes.reduce((sum, n) => sum + n.performance.tasksFailed, 0)
    };
  }
}