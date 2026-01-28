/**
 * GL Cognitive Mesh Core
 * @GL-layer: GL11
 * @GL-semantic: mesh-core-orchestrator
 * @GL-audit-trail: ../../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Core orchestrator for the Cognitive Mesh - manages all mesh components
 */

import { MeshMemory } from '../mesh-memory';
import { MeshRouting } from '../mesh-routing';
import { MeshNodes } from '../mesh-nodes';
import { MeshSynchronization } from '../mesh-synchronization';
import { MeshOptimizer } from '../mesh-optimizer';
import { MeshEmergence } from '../mesh-emergence';
import { EventEmitter } from 'events';

export interface MeshConfig {
  maxNodes: number;
  syncInterval: number;
  optimizationThreshold: number;
  emergenceThreshold: number;
}

export interface MeshState {
  active: boolean;
  nodesCount: number;
  sharedMemorySize: number;
  lastSync: Date;
  emergenceLevel: number;
}

export class MeshCore extends EventEmitter {
  private memory: MeshMemory;
  private routing: MeshRouting;
  private nodes: MeshNodes;
  private sync: MeshSynchronization;
  private optimizer: MeshOptimizer;
  private emergence: MeshEmergence;
  
  private config: MeshConfig;
  private initialized: boolean = false;

  constructor(config?: Partial<MeshConfig>) {
    super();
    
    this.config = {
      maxNodes: 100,
      syncInterval: 5000,
      optimizationThreshold: 0.8,
      emergenceThreshold: 0.7,
      ...config
    };

    this.memory = new MeshMemory();
    this.routing = new MeshRouting(this.memory);
    this.nodes = new MeshNodes(this.config.maxNodes);
    this.sync = new MeshSynchronization(this.memory, this.config.syncInterval);
    this.optimizer = new MeshOptimizer(this.memory, this.config.optimizationThreshold);
    this.emergence = new MeshEmergence(this.memory, this.config.emergenceThreshold);
  }

  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    await this.memory.initialize();
    await this.nodes.initialize();
    await this.sync.initialize();
    await this.optimizer.initialize();
    await this.emergence.initialize();

    // Set up event forwarding
    this.sync.on('sync', (data) => this.emit('sync', data));
    this.optimizer.on('optimized', (data) => this.emit('optimized', data));
    this.emergence.on('emergence', (data) => this.emit('emergence', data));
    this.nodes.on('node-activated', (data) => this.emit('node-activated', data));

    this.initialized = true;
    this.emit('initialized');
  }

  getState(): MeshState {
    return {
      active: this.initialized,
      nodesCount: this.nodes.getActiveNodesCount(),
      sharedMemorySize: this.memory.getSize(),
      lastSync: this.sync.getLastSyncTime(),
      emergenceLevel: this.emergence.getCurrentLevel()
    };
  }

  getMemory(): MeshMemory {
    return this.memory;
  }

  getRouting(): MeshRouting {
    return this.routing;
  }

  getNodes(): MeshNodes {
    return this.nodes;
  }

  getSync(): MeshSynchronization {
    return this.sync;
  }

  getOptimizer(): MeshOptimizer {
    return this.optimizer;
  }

  getEmergence(): MeshEmergence {
    return this.emergence;
  }

  async shutdown(): Promise<void> {
    await this.sync.shutdown();
    await this.optimizer.shutdown();
    await this.emergence.shutdown();
    this.initialized = false;
    this.emit('shutdown');
  }
}