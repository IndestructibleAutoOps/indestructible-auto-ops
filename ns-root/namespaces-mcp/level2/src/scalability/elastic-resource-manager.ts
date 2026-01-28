// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/scalability
 * @gl-semantic-anchor GL-00-SRC_SCALABIL_ELASTICRESOU
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Elastic Resource Manager
 * 
 * Dynamic resource allocation engine with intelligent capacity planning
 * and cost optimization for infinite scalability.
 * 
 * Performance Targets:
 * - Scale-up Time: <30s
 * - Resource Utilization: >95%
 * - Allocation Latency: <100ms
 * - Cost Optimization: 30% reduction
 * 
 * @module scalability/elastic-resource-manager
 */

import { EventEmitter } from 'events';

/**
 * Resource types supported by the system
 */
export enum ResourceType {
  COMPUTE = 'compute',
  MEMORY = 'memory',
  STORAGE = 'storage',
  NETWORK = 'network',
  GPU = 'gpu',
  CUSTOM = 'custom'
}

/**
 * Resource allocation strategies
 */
export enum AllocationStrategy {
  BEST_FIT = 'best-fit',           // Minimize fragmentation
  FIRST_FIT = 'first-fit',         // Fast allocation
  WORST_FIT = 'worst-fit',         // Balance distribution
  NEXT_FIT = 'next-fit',           // Sequential allocation
  PREDICTIVE = 'predictive',       // ML-based prediction
  COST_OPTIMIZED = 'cost-optimized' // Minimize cost
}

/**
 * Resource state
 */
export enum ResourceState {
  AVAILABLE = 'available',
  ALLOCATED = 'allocated',
  RESERVED = 'reserved',
  SCALING = 'scaling',
  MAINTENANCE = 'maintenance',
  FAILED = 'failed'
}

/**
 * Resource specification
 */
export interface ResourceSpec {
  type: ResourceType;
  amount: number;
  unit: string;
  constraints?: Record<string, any>;
  tags?: Record<string, string>;
}

/**
 * Resource instance
 */
export interface ResourceInstance {
  id: string;
  type: ResourceType;
  spec: ResourceSpec;
  state: ResourceState;
  allocatedTo?: string;
  createdAt: Date;
  lastUsed?: Date;
  metadata: Record<string, any>;
}

/**
 * Resource pool configuration
 */
export interface ResourcePoolConfig {
  minSize: number;
  maxSize: number;
  targetUtilization: number;
  scaleUpThreshold: number;
  scaleDownThreshold: number;
  cooldownPeriod: number; // seconds
}

/**
 * Allocation request
 */
export interface AllocationRequest {
  requestId: string;
  resources: ResourceSpec[];
  strategy: AllocationStrategy;
  priority: number;
  timeout?: number;
  constraints?: Record<string, any>;
  metadata?: Record<string, any>;
}

/**
 * Allocation result
 */
export interface AllocationResult {
  requestId: string;
  success: boolean;
  allocatedResources: ResourceInstance[];
  allocationTime: number;
  error?: string;
  metadata?: Record<string, any>;
}

/**
 * Capacity planning metrics
 */
export interface CapacityMetrics {
  totalCapacity: Record<ResourceType, number>;
  allocatedCapacity: Record<ResourceType, number>;
  availableCapacity: Record<ResourceType, number>;
  utilizationRate: Record<ResourceType, number>;
  projectedDemand: Record<ResourceType, number>;
  recommendedScaling: Record<ResourceType, number>;
}

/**
 * Cost optimization recommendation
 */
export interface CostOptimization {
  currentCost: number;
  optimizedCost: number;
  savings: number;
  savingsPercentage: number;
  recommendations: Array<{
    action: string;
    impact: string;
    estimatedSavings: number;
  }>;
}

/**
 * Elastic Resource Manager Configuration
 */
export interface ElasticResourceManagerConfig {
  pools: Map<ResourceType, ResourcePoolConfig>;
  defaultStrategy: AllocationStrategy;
  enableAutoScaling: boolean;
  enableCostOptimization: boolean;
  metricsInterval: number; // seconds
  optimizationInterval: number; // seconds
}

/**
 * Elastic Resource Manager
 * 
 * Manages dynamic resource allocation with intelligent capacity planning
 * and cost optimization.
 */
export class ElasticResourceManager extends EventEmitter {
  private config: ElasticResourceManagerConfig;
  private resources: Map<string, ResourceInstance>;
  private pools: Map<ResourceType, ResourceInstance[]>;
  private allocationQueue: AllocationRequest[];
  private metricsHistory: CapacityMetrics[];
  private lastScaleTime: Map<ResourceType, Date>;
  private isRunning: boolean;

  constructor(config: ElasticResourceManagerConfig) {
    super();
    this.config = config;
    this.resources = new Map();
    this.pools = new Map();
    this.allocationQueue = [];
    this.metricsHistory = [];
    this.lastScaleTime = new Map();
    this.isRunning = false;

    this.initializePools();
  }

  /**
   * Initialize resource pools
   */
  private initializePools(): void {
    for (const [type, poolConfig] of this.config.pools.entries()) {
      const pool: ResourceInstance[] = [];
      
      // Create initial pool resources
      for (let i = 0; i < poolConfig.minSize; i++) {
        const resource = this.createResource(type, {
          type,
          amount: 1,
          unit: this.getDefaultUnit(type)
        });
        pool.push(resource);
        this.resources.set(resource.id, resource);
      }
      
      this.pools.set(type, pool);
      this.lastScaleTime.set(type, new Date());
    }

    this.emit('pools-initialized', {
      pools: Array.from(this.pools.keys()),
      totalResources: this.resources.size
    });
  }

  /**
   * Start the resource manager
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      throw new Error('Resource manager already running');
    }

    this.isRunning = true;
    this.emit('started');

    // Start metrics collection
    if (this.config.metricsInterval > 0) {
      this.startMetricsCollection();
    }

    // Start auto-scaling
    if (this.config.enableAutoScaling) {
      this.startAutoScaling();
    }

    // Start cost optimization
    if (this.config.enableCostOptimization) {
      this.startCostOptimization();
    }
  }

  /**
   * Stop the resource manager
   */
  async stop(): Promise<void> {
    this.isRunning = false;
    this.emit('stopped');
  }

  /**
   * Allocate resources
   */
  async allocate(request: AllocationRequest): Promise<AllocationResult> {
    const startTime = Date.now();

    try {
      // Validate request
      this.validateAllocationRequest(request);

      // Find available resources
      const allocatedResources: ResourceInstance[] = [];
      
      for (const spec of request.resources) {
        const resource = await this.findAvailableResource(
          spec,
          request.strategy,
          request.constraints
        );

        if (!resource) {
          // Trigger scaling if needed
          if (this.config.enableAutoScaling) {
            await this.scaleUp(spec.type, 1);
            // Retry allocation
            const retryResource = await this.findAvailableResource(
              spec,
              request.strategy,
              request.constraints
            );
            if (retryResource) {
              allocatedResources.push(retryResource);
            } else {
              throw new Error(`Unable to allocate resource: ${spec.type}`);
            }
          } else {
            throw new Error(`No available resources for type: ${spec.type}`);
          }
        } else {
          allocatedResources.push(resource);
        }
      }

      // Mark resources as allocated
      for (const resource of allocatedResources) {
        resource.state = ResourceState.ALLOCATED;
        resource.allocatedTo = request.requestId;
        resource.lastUsed = new Date();
      }

      const allocationTime = Date.now() - startTime;

      this.emit('allocation-success', {
        requestId: request.requestId,
        resourceCount: allocatedResources.length,
        allocationTime
      });

      return {
        requestId: request.requestId,
        success: true,
        allocatedResources,
        allocationTime
      };

    } catch (error) {
      const allocationTime = Date.now() - startTime;

      this.emit('allocation-failed', {
        requestId: request.requestId,
        error: error instanceof Error ? error.message : 'Unknown error',
        allocationTime
      });

      return {
        requestId: request.requestId,
        success: false,
        allocatedResources: [],
        allocationTime,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Release resources
   */
  async release(resourceIds: string[]): Promise<void> {
    for (const id of resourceIds) {
      const resource = this.resources.get(id);
      if (resource && resource.state === ResourceState.ALLOCATED) {
        resource.state = ResourceState.AVAILABLE;
        resource.allocatedTo = undefined;
        
        this.emit('resource-released', {
          resourceId: id,
          type: resource.type
        });
      }
    }

    // Trigger scale-down if needed
    if (this.config.enableAutoScaling) {
      await this.checkScaleDown();
    }
  }

  /**
   * Scale up resources
   */
  private async scaleUp(type: ResourceType, count: number): Promise<void> {
    const pool = this.pools.get(type);
    const poolConfig = this.config.pools.get(type);

    if (!pool || !poolConfig) {
      throw new Error(`No pool configuration for type: ${type}`);
    }

    // Check cooldown period
    const lastScale = this.lastScaleTime.get(type);
    if (lastScale) {
      const timeSinceLastScale = (Date.now() - lastScale.getTime()) / 1000;
      if (timeSinceLastScale < poolConfig.cooldownPeriod) {
        return; // Skip scaling during cooldown
      }
    }

    // Check max size
    if (pool.length + count > poolConfig.maxSize) {
      count = poolConfig.maxSize - pool.length;
    }

    if (count <= 0) {
      return;
    }

    const startTime = Date.now();

    // Create new resources
    for (let i = 0; i < count; i++) {
      const resource = this.createResource(type, {
        type,
        amount: 1,
        unit: this.getDefaultUnit(type)
      });
      pool.push(resource);
      this.resources.set(resource.id, resource);
    }

    const scaleTime = Date.now() - startTime;
    this.lastScaleTime.set(type, new Date());

    this.emit('scaled-up', {
      type,
      count,
      newSize: pool.length,
      scaleTime
    });
  }

  /**
   * Check and perform scale-down
   */
  private async checkScaleDown(): Promise<void> {
    for (const [type, pool] of this.pools.entries()) {
      const poolConfig = this.config.pools.get(type);
      if (!poolConfig) continue;

      const availableCount = pool.filter(
        r => r.state === ResourceState.AVAILABLE
      ).length;
      const utilizationRate = 1 - (availableCount / pool.length);

      if (utilizationRate < poolConfig.scaleDownThreshold &&
          pool.length > poolConfig.minSize) {
        
        // Check cooldown
        const lastScale = this.lastScaleTime.get(type);
        if (lastScale) {
          const timeSinceLastScale = (Date.now() - lastScale.getTime()) / 1000;
          if (timeSinceLastScale < poolConfig.cooldownPeriod) {
            continue;
          }
        }

        // Remove excess available resources
        const targetSize = Math.max(
          poolConfig.minSize,
          Math.ceil(pool.length * poolConfig.targetUtilization)
        );
        const removeCount = pool.length - targetSize;

        if (removeCount > 0) {
          await this.scaleDown(type, removeCount);
        }
      }
    }
  }

  /**
   * Scale down resources
   */
  private async scaleDown(type: ResourceType, count: number): Promise<void> {
    const pool = this.pools.get(type);
    if (!pool) return;

    const availableResources = pool.filter(
      r => r.state === ResourceState.AVAILABLE
    );

    const toRemove = availableResources.slice(0, Math.min(count, availableResources.length));

    for (const resource of toRemove) {
      this.resources.delete(resource.id);
      const index = pool.indexOf(resource);
      if (index > -1) {
        pool.splice(index, 1);
      }
    }

    this.lastScaleTime.set(type, new Date());

    this.emit('scaled-down', {
      type,
      count: toRemove.length,
      newSize: pool.length
    });
  }

  /**
   * Get capacity metrics
   */
  getCapacityMetrics(): CapacityMetrics {
    const metrics: CapacityMetrics = {
      totalCapacity: {} as Record<ResourceType, number>,
      allocatedCapacity: {} as Record<ResourceType, number>,
      availableCapacity: {} as Record<ResourceType, number>,
      utilizationRate: {} as Record<ResourceType, number>,
      projectedDemand: {} as Record<ResourceType, number>,
      recommendedScaling: {} as Record<ResourceType, number>
    };

    for (const [type, pool] of this.pools.entries()) {
      const total = pool.length;
      const allocated = pool.filter(r => r.state === ResourceState.ALLOCATED).length;
      const available = pool.filter(r => r.state === ResourceState.AVAILABLE).length;

      metrics.totalCapacity[type] = total;
      metrics.allocatedCapacity[type] = allocated;
      metrics.availableCapacity[type] = available;
      metrics.utilizationRate[type] = total > 0 ? allocated / total : 0;

      // Simple projection based on recent trend
      metrics.projectedDemand[type] = this.projectDemand(type);
      metrics.recommendedScaling[type] = this.calculateRecommendedScaling(type);
    }

    return metrics;
  }

  /**
   * Get cost optimization recommendations
   */
  getCostOptimization(): CostOptimization {
    const currentCost = this.calculateCurrentCost();
    const recommendations = this.generateCostRecommendations();
    const optimizedCost = currentCost - recommendations.reduce(
      (sum, rec) => sum + rec.estimatedSavings,
      0
    );

    return {
      currentCost,
      optimizedCost,
      savings: currentCost - optimizedCost,
      savingsPercentage: ((currentCost - optimizedCost) / currentCost) * 100,
      recommendations
    };
  }

  /**
   * Helper: Create resource instance
   */
  private createResource(type: ResourceType, spec: ResourceSpec): ResourceInstance {
    return {
      id: `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      spec,
      state: ResourceState.AVAILABLE,
      createdAt: new Date(),
      metadata: {}
    };
  }

  /**
   * Helper: Find available resource
   */
  private async findAvailableResource(
    spec: ResourceSpec,
    strategy: AllocationStrategy,
    constraints?: Record<string, any>
  ): Promise<ResourceInstance | null> {
    const pool = this.pools.get(spec.type);
    if (!pool) return null;

    const available = pool.filter(r => r.state === ResourceState.AVAILABLE);
    if (available.length === 0) return null;

    // Apply strategy
    switch (strategy) {
      case AllocationStrategy.FIRST_FIT:
        return available[0];
      
      case AllocationStrategy.BEST_FIT:
        // Find resource with closest match to requirements
        return available.reduce((best, current) => {
          return this.calculateFitScore(current, spec) > 
                 this.calculateFitScore(best, spec) ? current : best;
        });
      
      case AllocationStrategy.COST_OPTIMIZED:
        // Find cheapest available resource
        return available.reduce((cheapest, current) => {
          return this.calculateCost(current) < this.calculateCost(cheapest) 
            ? current : cheapest;
        });
      
      default:
        return available[0];
    }
  }

  /**
   * Helper: Validate allocation request
   */
  private validateAllocationRequest(request: AllocationRequest): void {
    if (!request.requestId) {
      throw new Error('Request ID is required');
    }
    if (!request.resources || request.resources.length === 0) {
      throw new Error('At least one resource specification is required');
    }
  }

  /**
   * Helper: Get default unit for resource type
   */
  private getDefaultUnit(type: ResourceType): string {
    const units: Record<ResourceType, string> = {
      [ResourceType.COMPUTE]: 'cores',
      [ResourceType.MEMORY]: 'GB',
      [ResourceType.STORAGE]: 'GB',
      [ResourceType.NETWORK]: 'Gbps',
      [ResourceType.GPU]: 'units',
      [ResourceType.CUSTOM]: 'units'
    };
    return units[type];
  }

  /**
   * Helper: Calculate fit score
   */
  private calculateFitScore(resource: ResourceInstance, spec: ResourceSpec): number {
    // Simple scoring based on resource match
    return resource.spec.amount >= spec.amount ? 1 : 0;
  }

  /**
   * Helper: Calculate resource cost
   */
  private calculateCost(resource: ResourceInstance): number {
    // Simplified cost calculation
    const baseCosts: Record<ResourceType, number> = {
      [ResourceType.COMPUTE]: 0.05,
      [ResourceType.MEMORY]: 0.01,
      [ResourceType.STORAGE]: 0.001,
      [ResourceType.NETWORK]: 0.02,
      [ResourceType.GPU]: 0.50,
      [ResourceType.CUSTOM]: 0.10
    };
    return (baseCosts[resource.type] || 0.10) * resource.spec.amount;
  }

  /**
   * Helper: Calculate current total cost
   */
  private calculateCurrentCost(): number {
    let total = 0;
    for (const resource of this.resources.values()) {
      total += this.calculateCost(resource);
    }
    return total;
  }

  /**
   * Helper: Project demand
   */
  private projectDemand(type: ResourceType): number {
    // Simple projection based on current utilization
    const pool = this.pools.get(type);
    if (!pool) return 0;

    const allocated = pool.filter(r => r.state === ResourceState.ALLOCATED).length;
    return allocated * 1.2; // 20% growth projection
  }

  /**
   * Helper: Calculate recommended scaling
   */
  private calculateRecommendedScaling(type: ResourceType): number {
    const pool = this.pools.get(type);
    const poolConfig = this.config.pools.get(type);
    if (!pool || !poolConfig) return 0;

    const projected = this.projectDemand(type);
    const current = pool.length;
    const target = Math.ceil(projected / poolConfig.targetUtilization);

    return Math.max(0, target - current);
  }

  /**
   * Helper: Generate cost recommendations
   */
  private generateCostRecommendations(): Array<{
    action: string;
    impact: string;
    estimatedSavings: number;
  }> {
    const recommendations = [];

    // Check for underutilized resources
    for (const [type, pool] of this.pools.entries()) {
      const available = pool.filter(r => r.state === ResourceState.AVAILABLE).length;
      const utilizationRate = 1 - (available / pool.length);

      if (utilizationRate < 0.5 && pool.length > 1) {
        const savingsPerResource = this.calculateCost(pool[0]);
        recommendations.push({
          action: `Scale down ${type} resources`,
          impact: `Reduce ${type} pool by ${Math.floor(available / 2)} resources`,
          estimatedSavings: savingsPerResource * Math.floor(available / 2)
        });
      }
    }

    return recommendations;
  }

  /**
   * Start metrics collection
   */
  private startMetricsCollection(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      const metrics = this.getCapacityMetrics();
      this.metricsHistory.push(metrics);

      // Keep only last 1000 metrics
      if (this.metricsHistory.length > 1000) {
        this.metricsHistory.shift();
      }

      this.emit('metrics-collected', metrics);
    }, this.config.metricsInterval * 1000);
  }

  /**
   * Start auto-scaling
   */
  private startAutoScaling(): void {
    setInterval(async () => {
      if (!this.isRunning) return;

      for (const [type, pool] of this.pools.entries()) {
        const poolConfig = this.config.pools.get(type);
        if (!poolConfig) continue;

        const available = pool.filter(r => r.state === ResourceState.AVAILABLE).length;
        const utilizationRate = 1 - (available / pool.length);

        // Scale up if utilization is high
        if (utilizationRate > poolConfig.scaleUpThreshold) {
          const scaleCount = Math.ceil(pool.length * 0.2); // Scale by 20%
          await this.scaleUp(type, scaleCount);
        }
      }

      // Check for scale-down
      await this.checkScaleDown();
    }, 30000); // Check every 30 seconds
  }

  /**
   * Start cost optimization
   */
  private startCostOptimization(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      const optimization = this.getCostOptimization();
      this.emit('cost-optimization', optimization);
    }, this.config.optimizationInterval * 1000);
  }
}

/**
 * Create elastic resource manager with default configuration
 */
export function createElasticResourceManager(
  customConfig?: Partial<ElasticResourceManagerConfig>
): ElasticResourceManager {
  const defaultConfig: ElasticResourceManagerConfig = {
    pools: new Map([
      [ResourceType.COMPUTE, {
        minSize: 10,
        maxSize: 1000,
        targetUtilization: 0.75,
        scaleUpThreshold: 0.85,
        scaleDownThreshold: 0.50,
        cooldownPeriod: 300
      }],
      [ResourceType.MEMORY, {
        minSize: 10,
        maxSize: 1000,
        targetUtilization: 0.75,
        scaleUpThreshold: 0.85,
        scaleDownThreshold: 0.50,
        cooldownPeriod: 300
      }],
      [ResourceType.STORAGE, {
        minSize: 5,
        maxSize: 500,
        targetUtilization: 0.70,
        scaleUpThreshold: 0.80,
        scaleDownThreshold: 0.40,
        cooldownPeriod: 600
      }]
    ]),
    defaultStrategy: AllocationStrategy.BEST_FIT,
    enableAutoScaling: true,
    enableCostOptimization: true,
    metricsInterval: 60,
    optimizationInterval: 300
  };

  const config = { ...defaultConfig, ...customConfig };
  return new ElasticResourceManager(config);
}