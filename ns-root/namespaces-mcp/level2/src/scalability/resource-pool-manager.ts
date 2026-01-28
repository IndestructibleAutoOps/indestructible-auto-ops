// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/scalability
 * @gl-semantic-anchor GL-00-SRC_SCALABIL_RESOURCEPOOL
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Resource Pool Manager
 * 
 * Multi-tier resource pool management with intelligent allocation,
 * health monitoring, and quota management.
 * 
 * Performance Targets:
 * - Pool Efficiency: >95%
 * - Allocation Latency: <100ms
 * - Rebalancing Time: <30s
 * - Health Check: <50ms
 * 
 * @module scalability/resource-pool-manager
 */

import { EventEmitter } from 'events';

/**
 * Pool tier levels
 */
export enum PoolTier {
  HOT = 'hot',           // Immediately available
  WARM = 'warm',         // Quick activation
  COLD = 'cold',         // Slower activation
  RESERVED = 'reserved'  // Pre-allocated
}

/**
 * Resource pool state
 */
export enum PoolState {
  ACTIVE = 'active',
  DEGRADED = 'degraded',
  MAINTENANCE = 'maintenance',
  DRAINING = 'draining',
  FAILED = 'failed'
}

/**
 * Resource health status
 */
export enum HealthStatus {
  HEALTHY = 'healthy',
  DEGRADED = 'degraded',
  UNHEALTHY = 'unhealthy',
  UNKNOWN = 'unknown'
}

/**
 * Pool resource
 */
export interface PoolResource {
  id: string;
  poolId: string;
  tier: PoolTier;
  type: string;
  capacity: number;
  allocated: number;
  available: number;
  health: HealthStatus;
  lastHealthCheck?: Date;
  createdAt: Date;
  lastUsed?: Date;
  metadata: Record<string, any>;
}

/**
 * Resource pool configuration
 */
export interface ResourcePoolConfig {
  id: string;
  name: string;
  resourceType: string;
  tiers: {
    [PoolTier.HOT]: { minSize: number; maxSize: number };
    [PoolTier.WARM]: { minSize: number; maxSize: number };
    [PoolTier.COLD]: { minSize: number; maxSize: number };
    [PoolTier.RESERVED]: { minSize: number; maxSize: number };
  };
  targetUtilization: number;
  rebalanceThreshold: number;
  healthCheckInterval: number; // seconds
  quotas?: ResourceQuota[];
}

/**
 * Resource quota
 */
export interface ResourceQuota {
  id: string;
  name: string;
  resourceType: string;
  limit: number;
  used: number;
  period: 'hourly' | 'daily' | 'monthly';
  resetAt: Date;
}

/**
 * Pool allocation request
 */
export interface PoolAllocationRequest {
  requestId: string;
  poolId: string;
  amount: number;
  tier?: PoolTier;
  duration?: number; // seconds
  priority: number;
  metadata?: Record<string, any>;
}

/**
 * Pool allocation result
 */
export interface PoolAllocationResult {
  requestId: string;
  success: boolean;
  resources: PoolResource[];
  tier: PoolTier;
  allocationTime: number;
  error?: string;
}

/**
 * Pool statistics
 */
export interface PoolStatistics {
  poolId: string;
  totalCapacity: number;
  allocatedCapacity: number;
  availableCapacity: number;
  utilizationRate: number;
  efficiency: number;
  tierDistribution: Record<PoolTier, {
    count: number;
    capacity: number;
    utilization: number;
  }>;
  healthDistribution: Record<HealthStatus, number>;
  allocationStats: {
    totalAllocations: number;
    successfulAllocations: number;
    failedAllocations: number;
    averageAllocationTime: number;
  };
}

/**
 * Rebalancing plan
 */
export interface RebalancingPlan {
  poolId: string;
  actions: Array<{
    type: 'move' | 'promote' | 'demote' | 'remove';
    resourceId: string;
    fromTier: PoolTier;
    toTier: PoolTier;
    reason: string;
  }>;
  estimatedTime: number;
  expectedImprovement: number;
}

/**
 * Resource Pool Manager Configuration
 */
export interface ResourcePoolManagerConfig {
  pools: ResourcePoolConfig[];
  enableAutoRebalancing: boolean;
  rebalancingInterval: number; // seconds
  enableHealthMonitoring: boolean;
  healthCheckInterval: number; // seconds
  enableQuotaManagement: boolean;
}

/**
 * Resource Pool Manager
 * 
 * Manages multi-tier resource pools with intelligent allocation,
 * automatic rebalancing, and health monitoring.
 */
export class ResourcePoolManager extends EventEmitter {
  private config: ResourcePoolManagerConfig;
  private pools: Map<string, ResourcePoolConfig>;
  private resources: Map<string, PoolResource>;
  private poolResources: Map<string, Set<string>>; // poolId -> resourceIds
  private quotas: Map<string, ResourceQuota>;
  private statistics: Map<string, PoolStatistics>;
  private isRunning: boolean;

  constructor(config: ResourcePoolManagerConfig) {
    super();
    this.config = config;
    this.pools = new Map();
    this.resources = new Map();
    this.poolResources = new Map();
    this.quotas = new Map();
    this.statistics = new Map();
    this.isRunning = false;

    this.initializePools();
  }

  /**
   * Initialize resource pools
   */
  private initializePools(): void {
    for (const poolConfig of this.config.pools) {
      this.pools.set(poolConfig.id, poolConfig);
      this.poolResources.set(poolConfig.id, new Set());

      // Initialize pool resources
      this.createInitialResources(poolConfig);

      // Initialize quotas
      if (poolConfig.quotas) {
        for (const quota of poolConfig.quotas) {
          this.quotas.set(quota.id, quota);
        }
      }

      // Initialize statistics
      this.statistics.set(poolConfig.id, this.createEmptyStatistics(poolConfig.id));
    }

    this.emit('pools-initialized', {
      count: this.pools.size,
      totalResources: this.resources.size
    });
  }

  /**
   * Start the pool manager
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      throw new Error('Pool manager already running');
    }

    this.isRunning = true;
    this.emit('started');

    // Start health monitoring
    if (this.config.enableHealthMonitoring) {
      this.startHealthMonitoring();
    }

    // Start auto-rebalancing
    if (this.config.enableAutoRebalancing) {
      this.startAutoRebalancing();
    }

    // Start quota management
    if (this.config.enableQuotaManagement) {
      this.startQuotaManagement();
    }
  }

  /**
   * Stop the pool manager
   */
  async stop(): Promise<void> {
    this.isRunning = false;
    this.emit('stopped');
  }

  /**
   * Allocate resources from pool
   */
  async allocate(request: PoolAllocationRequest): Promise<PoolAllocationResult> {
    const startTime = Date.now();

    try {
      const pool = this.pools.get(request.poolId);
      if (!pool) {
        throw new Error(`Pool not found: ${request.poolId}`);
      }

      // Check quota
      if (this.config.enableQuotaManagement) {
        const quotaCheck = this.checkQuota(pool.resourceType, request.amount);
        if (!quotaCheck.allowed) {
          throw new Error(`Quota exceeded: ${quotaCheck.reason}`);
        }
      }

      // Find available resources
      const resources = await this.findAvailableResources(
        request.poolId,
        request.amount,
        request.tier,
        request.priority
      );

      if (resources.length < request.amount) {
        throw new Error(`Insufficient resources: requested ${request.amount}, available ${resources.length}`);
      }

      // Allocate resources
      const allocated = resources.slice(0, request.amount);
      for (const resource of allocated) {
        resource.allocated += 1;
        resource.available = resource.capacity - resource.allocated;
        resource.lastUsed = new Date();
      }

      // Update quota
      if (this.config.enableQuotaManagement) {
        this.updateQuotaUsage(pool.resourceType, request.amount);
      }

      const allocationTime = Date.now() - startTime;

      // Update statistics
      this.updateAllocationStats(request.poolId, true, allocationTime);

      this.emit('allocation-success', {
        requestId: request.requestId,
        poolId: request.poolId,
        resourceCount: allocated.length,
        allocationTime
      });

      return {
        requestId: request.requestId,
        success: true,
        resources: allocated,
        tier: allocated[0].tier,
        allocationTime
      };

    } catch (error) {
      const allocationTime = Date.now() - startTime;
      
      this.updateAllocationStats(request.poolId, false, allocationTime);

      this.emit('allocation-failed', {
        requestId: request.requestId,
        error: error instanceof Error ? error.message : 'Unknown error',
        allocationTime
      });

      return {
        requestId: request.requestId,
        success: false,
        resources: [],
        tier: request.tier || PoolTier.HOT,
        allocationTime,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Release resources back to pool
   */
  async release(resourceIds: string[]): Promise<void> {
    for (const id of resourceIds) {
      const resource = this.resources.get(id);
      if (resource && resource.allocated > 0) {
        resource.allocated -= 1;
        resource.available = resource.capacity - resource.allocated;
        
        this.emit('resource-released', {
          resourceId: id,
          poolId: resource.poolId
        });
      }
    }

    // Trigger rebalancing if needed
    if (this.config.enableAutoRebalancing) {
      await this.checkRebalancing();
    }
  }

  /**
   * Get pool statistics
   */
  getPoolStatistics(poolId: string): PoolStatistics | null {
    return this.statistics.get(poolId) || null;
  }

  /**
   * Get all pools statistics
   */
  getAllStatistics(): Map<string, PoolStatistics> {
    return new Map(this.statistics);
  }

  /**
   * Rebalance pool
   */
  async rebalancePool(poolId: string): Promise<RebalancingPlan> {
    const pool = this.pools.get(poolId);
    if (!pool) {
      throw new Error(`Pool not found: ${poolId}`);
    }

    const plan = this.createRebalancingPlan(poolId);
    
    if (plan.actions.length === 0) {
      return plan;
    }

    const startTime = Date.now();

    // Execute rebalancing actions
    for (const action of plan.actions) {
      await this.executeRebalancingAction(action);
    }

    const rebalancingTime = Date.now() - startTime;

    this.emit('pool-rebalanced', {
      poolId,
      actionsCount: plan.actions.length,
      rebalancingTime
    });

    return plan;
  }

  /**
   * Create initial resources for pool
   */
  private createInitialResources(poolConfig: ResourcePoolConfig): void {
    const tiers = [PoolTier.HOT, PoolTier.WARM, PoolTier.COLD, PoolTier.RESERVED];

    for (const tier of tiers) {
      const tierConfig = poolConfig.tiers[tier];
      
      for (let i = 0; i < tierConfig.minSize; i++) {
        const resource = this.createResource(poolConfig.id, tier, poolConfig.resourceType);
        this.resources.set(resource.id, resource);
        this.poolResources.get(poolConfig.id)!.add(resource.id);
      }
    }
  }

  /**
   * Create resource
   */
  private createResource(
    poolId: string,
    tier: PoolTier,
    resourceType: string
  ): PoolResource {
    return {
      id: `${poolId}-${tier}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      poolId,
      tier,
      type: resourceType,
      capacity: 100,
      allocated: 0,
      available: 100,
      health: HealthStatus.HEALTHY,
      createdAt: new Date(),
      metadata: {}
    };
  }

  /**
   * Find available resources
   */
  private async findAvailableResources(
    poolId: string,
    amount: number,
    preferredTier?: PoolTier,
    priority?: number
  ): Promise<PoolResource[]> {
    const poolResourceIds = this.poolResources.get(poolId);
    if (!poolResourceIds) {
      return [];
    }

    const poolResources = Array.from(poolResourceIds)
      .map(id => this.resources.get(id)!)
      .filter(r => r.available > 0 && r.health === HealthStatus.HEALTHY);

    // Sort by tier preference and availability
    const tierOrder = preferredTier 
      ? [preferredTier, PoolTier.HOT, PoolTier.WARM, PoolTier.COLD, PoolTier.RESERVED]
      : [PoolTier.HOT, PoolTier.WARM, PoolTier.COLD, PoolTier.RESERVED];

    poolResources.sort((a, b) => {
      const aTierIndex = tierOrder.indexOf(a.tier);
      const bTierIndex = tierOrder.indexOf(b.tier);
      
      if (aTierIndex !== bTierIndex) {
        return aTierIndex - bTierIndex;
      }
      
      return b.available - a.available;
    });

    return poolResources.slice(0, amount);
  }

  /**
   * Check quota
   */
  private checkQuota(
    resourceType: string,
    amount: number
  ): { allowed: boolean; reason?: string } {
    for (const quota of this.quotas.values()) {
      if (quota.resourceType === resourceType) {
        if (quota.used + amount > quota.limit) {
          return {
            allowed: false,
            reason: `Quota limit exceeded: ${quota.name} (${quota.used + amount}/${quota.limit})`
          };
        }
      }
    }

    return { allowed: true };
  }

  /**
   * Update quota usage
   */
  private updateQuotaUsage(resourceType: string, amount: number): void {
    for (const quota of this.quotas.values()) {
      if (quota.resourceType === resourceType) {
        quota.used += amount;
      }
    }
  }

  /**
   * Create rebalancing plan
   */
  private createRebalancingPlan(poolId: string): RebalancingPlan {
    const pool = this.pools.get(poolId);
    if (!pool) {
      return {
        poolId,
        actions: [],
        estimatedTime: 0,
        expectedImprovement: 0
      };
    }

    const actions: RebalancingPlan['actions'] = [];
    const poolResourceIds = this.poolResources.get(poolId)!;
    const poolResources = Array.from(poolResourceIds).map(id => this.resources.get(id)!);

    // Analyze tier utilization
    const tierStats = this.calculateTierStatistics(poolResources);

    // Move underutilized resources to lower tiers
    for (const resource of poolResources) {
      if (resource.tier === PoolTier.HOT && resource.allocated === 0) {
        const lastUsed = resource.lastUsed?.getTime() || 0;
        const idleTime = Date.now() - lastUsed;
        
        if (idleTime > 3600000) { // 1 hour
          actions.push({
            type: 'demote',
            resourceId: resource.id,
            fromTier: PoolTier.HOT,
            toTier: PoolTier.WARM,
            reason: 'Idle for over 1 hour'
          });
        }
      }
    }

    // Promote frequently used warm resources
    for (const resource of poolResources) {
      if (resource.tier === PoolTier.WARM && resource.allocated > 0) {
        const utilizationRate = resource.allocated / resource.capacity;
        
        if (utilizationRate > 0.8) {
          actions.push({
            type: 'promote',
            resourceId: resource.id,
            fromTier: PoolTier.WARM,
            toTier: PoolTier.HOT,
            reason: 'High utilization rate'
          });
        }
      }
    }

    return {
      poolId,
      actions,
      estimatedTime: actions.length * 5, // 5 seconds per action
      expectedImprovement: actions.length * 2 // 2% improvement per action
    };
  }

  /**
   * Execute rebalancing action
   */
  private async executeRebalancingAction(
    action: RebalancingPlan['actions'][0]
  ): Promise<void> {
    const resource = this.resources.get(action.resourceId);
    if (!resource) return;

    resource.tier = action.toTier;
    
    this.emit('resource-rebalanced', {
      resourceId: action.resourceId,
      action: action.type,
      fromTier: action.fromTier,
      toTier: action.toTier
    });

    // Simulate rebalancing time
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  /**
   * Calculate tier statistics
   */
  private calculateTierStatistics(
    resources: PoolResource[]
  ): Record<PoolTier, { count: number; utilization: number }> {
    const stats: Record<PoolTier, { count: number; utilization: number }> = {
      [PoolTier.HOT]: { count: 0, utilization: 0 },
      [PoolTier.WARM]: { count: 0, utilization: 0 },
      [PoolTier.COLD]: { count: 0, utilization: 0 },
      [PoolTier.RESERVED]: { count: 0, utilization: 0 }
    };

    for (const resource of resources) {
      stats[resource.tier].count++;
      stats[resource.tier].utilization += resource.allocated / resource.capacity;
    }

    // Calculate average utilization
    for (const tier of Object.keys(stats) as PoolTier[]) {
      if (stats[tier].count > 0) {
        stats[tier].utilization /= stats[tier].count;
      }
    }

    return stats;
  }

  /**
   * Update allocation statistics
   */
  private updateAllocationStats(
    poolId: string,
    success: boolean,
    allocationTime: number
  ): void {
    const stats = this.statistics.get(poolId);
    if (!stats) return;

    stats.allocationStats.totalAllocations++;
    
    if (success) {
      stats.allocationStats.successfulAllocations++;
    } else {
      stats.allocationStats.failedAllocations++;
    }

    stats.allocationStats.averageAllocationTime = 
      (stats.allocationStats.averageAllocationTime * 
       (stats.allocationStats.totalAllocations - 1) + allocationTime) /
      stats.allocationStats.totalAllocations;
  }

  /**
   * Create empty statistics
   */
  private createEmptyStatistics(poolId: string): PoolStatistics {
    return {
      poolId,
      totalCapacity: 0,
      allocatedCapacity: 0,
      availableCapacity: 0,
      utilizationRate: 0,
      efficiency: 0,
      tierDistribution: {
        [PoolTier.HOT]: { count: 0, capacity: 0, utilization: 0 },
        [PoolTier.WARM]: { count: 0, capacity: 0, utilization: 0 },
        [PoolTier.COLD]: { count: 0, capacity: 0, utilization: 0 },
        [PoolTier.RESERVED]: { count: 0, capacity: 0, utilization: 0 }
      },
      healthDistribution: {
        [HealthStatus.HEALTHY]: 0,
        [HealthStatus.DEGRADED]: 0,
        [HealthStatus.UNHEALTHY]: 0,
        [HealthStatus.UNKNOWN]: 0
      },
      allocationStats: {
        totalAllocations: 0,
        successfulAllocations: 0,
        failedAllocations: 0,
        averageAllocationTime: 0
      }
    };
  }

  /**
   * Update pool statistics
   */
  private updatePoolStatistics(poolId: string): void {
    const poolResourceIds = this.poolResources.get(poolId);
    if (!poolResourceIds) return;

    const resources = Array.from(poolResourceIds).map(id => this.resources.get(id)!);
    const stats = this.statistics.get(poolId)!;

    // Calculate totals
    stats.totalCapacity = resources.reduce((sum, r) => sum + r.capacity, 0);
    stats.allocatedCapacity = resources.reduce((sum, r) => sum + r.allocated, 0);
    stats.availableCapacity = resources.reduce((sum, r) => sum + r.available, 0);
    stats.utilizationRate = stats.totalCapacity > 0 
      ? stats.allocatedCapacity / stats.totalCapacity 
      : 0;

    // Calculate tier distribution
    for (const tier of Object.keys(stats.tierDistribution) as PoolTier[]) {
      const tierResources = resources.filter(r => r.tier === tier);
      stats.tierDistribution[tier] = {
        count: tierResources.length,
        capacity: tierResources.reduce((sum, r) => sum + r.capacity, 0),
        utilization: tierResources.length > 0
          ? tierResources.reduce((sum, r) => sum + r.allocated / r.capacity, 0) / tierResources.length
          : 0
      };
    }

    // Calculate health distribution
    for (const health of Object.keys(stats.healthDistribution) as HealthStatus[]) {
      stats.healthDistribution[health] = resources.filter(r => r.health === health).length;
    }

    // Calculate efficiency
    stats.efficiency = stats.utilizationRate * 100;
  }

  /**
   * Check rebalancing
   */
  private async checkRebalancing(): Promise<void> {
    for (const poolId of this.pools.keys()) {
      const stats = this.statistics.get(poolId);
      if (!stats) continue;

      const pool = this.pools.get(poolId)!;
      
      // Check if rebalancing is needed
      if (Math.abs(stats.utilizationRate - pool.targetUtilization) > pool.rebalanceThreshold) {
        await this.rebalancePool(poolId);
      }
    }
  }

  /**
   * Start health monitoring
   */
  private startHealthMonitoring(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      for (const resource of this.resources.values()) {
        this.performHealthCheck(resource);
      }
    }, this.config.healthCheckInterval * 1000);
  }

  /**
   * Perform health check
   */
  private performHealthCheck(resource: PoolResource): void {
    // Simplified health check
    const utilizationRate = resource.allocated / resource.capacity;
    
    if (utilizationRate < 0.9) {
      resource.health = HealthStatus.HEALTHY;
    } else if (utilizationRate < 0.95) {
      resource.health = HealthStatus.DEGRADED;
    } else {
      resource.health = HealthStatus.UNHEALTHY;
    }

    resource.lastHealthCheck = new Date();
  }

  /**
   * Start auto-rebalancing
   */
  private startAutoRebalancing(): void {
    setInterval(async () => {
      if (!this.isRunning) return;

      await this.checkRebalancing();
    }, this.config.rebalancingInterval * 1000);
  }

  /**
   * Start quota management
   */
  private startQuotaManagement(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      const now = new Date();
      
      for (const quota of this.quotas.values()) {
        if (now >= quota.resetAt) {
          quota.used = 0;
          
          // Calculate next reset time
          switch (quota.period) {
            case 'hourly':
              quota.resetAt = new Date(now.getTime() + 3600000);
              break;
            case 'daily':
              quota.resetAt = new Date(now.getTime() + 86400000);
              break;
            case 'monthly':
              quota.resetAt = new Date(now.getFullYear(), now.getMonth() + 1, 1);
              break;
          }

          this.emit('quota-reset', { quotaId: quota.id });
        }
      }
    }, 60000); // Check every minute
  }

  /**
   * Update statistics periodically
   */
  private startStatisticsUpdate(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      for (const poolId of this.pools.keys()) {
        this.updatePoolStatistics(poolId);
      }
    }, 30000); // Update every 30 seconds
  }
}

/**
 * Create resource pool manager with default configuration
 */
export function createResourcePoolManager(
  customConfig?: Partial<ResourcePoolManagerConfig>
): ResourcePoolManager {
  const defaultConfig: ResourcePoolManagerConfig = {
    pools: [],
    enableAutoRebalancing: true,
    rebalancingInterval: 300,
    enableHealthMonitoring: true,
    healthCheckInterval: 60,
    enableQuotaManagement: true
  };

  const config = { ...defaultConfig, ...customConfig };
  return new ResourcePoolManager(config);
}