/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/scalability
 * @gl-semantic-anchor GL-00-SRC_SCALABIL_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Scalability Module
 * 
 * Infinite scalability fabric providing elastic resource management,
 * global load balancing, auto-scaling, resource pooling, and
 * performance optimization.
 * 
 * @module scalability
 */

// Elastic Resource Manager
export {
  ElasticResourceManager,
  createElasticResourceManager,
  ResourceType,
  AllocationStrategy,
  ResourceState,
  ResourceSpec,
  ResourceInstance,
  ResourcePoolConfig,
  AllocationRequest,
  AllocationResult,
  CapacityMetrics,
  CostOptimization,
  ElasticResourceManagerConfig
} from './elastic-resource-manager';

// Global Load Balancer
export {
  GlobalLoadBalancer,
  createGlobalLoadBalancer,
  LoadBalancingAlgorithm,
  BackendState,
  GeographicRegion,
  BackendServer,
  HealthCheckConfig,
  SessionAffinityConfig,
  DDoSProtectionConfig,
  RoutingRequest,
  RoutingResult,
  LoadBalancerStats,
  GlobalLoadBalancerConfig
} from './global-load-balancer';

// Auto-Scaling Engine
export {
  AutoScalingEngine,
  createAutoScalingEngine,
  ScalingDirection,
  TriggerType,
  ComparisonOperator,
  ScalingMetric,
  MetricTrigger,
  ScheduleTrigger,
  EventTrigger,
  PredictiveTrigger,
  CustomTrigger,
  ScalingTrigger,
  ScalingPolicy,
  ScalingDecision,
  ScalingEvent,
  PredictionModel,
  TimeSeriesPoint,
  AutoScalingEngineConfig
} from './auto-scaling-engine';

// Resource Pool Manager
export {
  ResourcePoolManager,
  createResourcePoolManager,
  PoolTier,
  PoolState,
  HealthStatus,
  PoolResource,
  ResourcePoolConfig,
  ResourceQuota,
  PoolAllocationRequest,
  PoolAllocationResult,
  PoolStatistics,
  RebalancingPlan,
  ResourcePoolManagerConfig
} from './resource-pool-manager';

// Performance Optimizer
export {
  PerformanceOptimizer,
  createPerformanceOptimizer,
  MetricType,
  OptimizationAction,
  BottleneckSeverity,
  PerformanceMetric,
  PerformanceBaseline,
  Bottleneck,
  OptimizationRecommendation,
  OptimizationResult,
  PerformanceProfile,
  TuningParameter,
  PerformanceOptimizerConfig
} from './performance-optimizer';

// Infinite Scalability System
export {
  InfiniteScalabilitySystem,
  createInfiniteScalabilitySystem,
  SystemState,
  ScalingOperation,
  SystemMetrics,
  SystemHealth,
  InfiniteScalabilitySystemConfig
} from './infinite-scalability-system';

/**
 * Module version
 */
export const VERSION = '1.0.0';

/**
 * Module metadata
 */
export const METADATA = {
  name: 'Infinite Scalability Fabric',
  version: VERSION,
  description: 'Enterprise-grade infinite scalability with elastic resources, global load balancing, and intelligent optimization',
  components: [
    'Elastic Resource Manager',
    'Global Load Balancer',
    'Auto-Scaling Engine',
    'Resource Pool Manager',
    'Performance Optimizer'
  ],
  performanceTargets: {
    scaleUpTime: '<30s',
    routingDecision: '<10ms',
    predictionAccuracy: '>99%',
    poolEfficiency: '>95%',
    optimizationDecision: '<50ms'
  }
};