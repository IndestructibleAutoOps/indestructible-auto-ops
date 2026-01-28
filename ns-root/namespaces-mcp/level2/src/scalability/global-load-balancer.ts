// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/scalability
 * @gl-semantic-anchor GL-00-SRC_SCALABIL_GLOBALLOADBA
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Global Load Balancer
 * 
 * Intelligent traffic distribution with geographic routing optimization,
 * health-based routing, and DDoS protection.
 * 
 * Performance Targets:
 * - Routing Decision: <10ms
 * - Availability: 99.99%
 * - Throughput: 100K+ req/s
 * - Latency: <5ms overhead
 * 
 * @module scalability/global-load-balancer
 */

import { EventEmitter } from 'events';

/**
 * Load balancing algorithms
 */
export enum LoadBalancingAlgorithm {
  ROUND_ROBIN = 'round-robin',
  LEAST_CONNECTIONS = 'least-connections',
  LEAST_RESPONSE_TIME = 'least-response-time',
  IP_HASH = 'ip-hash',
  WEIGHTED_ROUND_ROBIN = 'weighted-round-robin',
  GEOGRAPHIC = 'geographic',
  HEALTH_BASED = 'health-based',
  ADAPTIVE = 'adaptive'
}

/**
 * Backend server state
 */
export enum BackendState {
  HEALTHY = 'healthy',
  DEGRADED = 'degraded',
  UNHEALTHY = 'unhealthy',
  MAINTENANCE = 'maintenance',
  DRAINING = 'draining'
}

/**
 * Geographic region
 */
export interface GeographicRegion {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  continent: string;
  country: string;
}

/**
 * Backend server configuration
 */
export interface BackendServer {
  id: string;
  address: string;
  port: number;
  weight: number;
  region: GeographicRegion;
  state: BackendState;
  maxConnections: number;
  currentConnections: number;
  responseTime: number; // ms
  healthScore: number; // 0-100
  metadata: Record<string, any>;
}

/**
 * Health check configuration
 */
export interface HealthCheckConfig {
  enabled: boolean;
  interval: number; // seconds
  timeout: number; // seconds
  healthyThreshold: number;
  unhealthyThreshold: number;
  path?: string;
  expectedStatus?: number;
  expectedBody?: string;
}

/**
 * Session affinity configuration
 */
export interface SessionAffinityConfig {
  enabled: boolean;
  type: 'cookie' | 'ip' | 'header';
  cookieName?: string;
  headerName?: string;
  ttl: number; // seconds
}

/**
 * DDoS protection configuration
 */
export interface DDoSProtectionConfig {
  enabled: boolean;
  rateLimit: number; // requests per second per IP
  burstSize: number;
  blockDuration: number; // seconds
  whitelist: string[];
  blacklist: string[];
}

/**
 * Routing request
 */
export interface RoutingRequest {
  requestId: string;
  clientIp: string;
  clientRegion?: GeographicRegion;
  path: string;
  method: string;
  headers: Record<string, string>;
  sessionId?: string;
  timestamp: Date;
}

/**
 * Routing result
 */
export interface RoutingResult {
  requestId: string;
  backend: BackendServer;
  routingTime: number;
  algorithm: LoadBalancingAlgorithm;
  sessionAffinity: boolean;
  metadata?: Record<string, any>;
}

/**
 * Load balancer statistics
 */
export interface LoadBalancerStats {
  totalRequests: number;
  successfulRoutes: number;
  failedRoutes: number;
  averageRoutingTime: number;
  requestsPerSecond: number;
  backendStats: Map<string, {
    requests: number;
    connections: number;
    responseTime: number;
    errorRate: number;
  }>;
  regionStats: Map<string, {
    requests: number;
    averageLatency: number;
  }>;
}

/**
 * Global Load Balancer Configuration
 */
export interface GlobalLoadBalancerConfig {
  algorithm: LoadBalancingAlgorithm;
  backends: BackendServer[];
  healthCheck: HealthCheckConfig;
  sessionAffinity: SessionAffinityConfig;
  ddosProtection: DDoSProtectionConfig;
  enableMetrics: boolean;
  metricsInterval: number; // seconds
}

/**
 * Global Load Balancer
 * 
 * Distributes traffic across multiple backend servers with intelligent
 * routing based on health, geography, and performance metrics.
 */
export class GlobalLoadBalancer extends EventEmitter {
  private config: GlobalLoadBalancerConfig;
  private backends: Map<string, BackendServer>;
  private sessions: Map<string, string>; // sessionId -> backendId
  private rateLimits: Map<string, { count: number; resetTime: number }>;
  private stats: LoadBalancerStats;
  private roundRobinIndex: number;
  private isRunning: boolean;

  constructor(config: GlobalLoadBalancerConfig) {
    super();
    this.config = config;
    this.backends = new Map();
    this.sessions = new Map();
    this.rateLimits = new Map();
    this.roundRobinIndex = 0;
    this.isRunning = false;

    this.stats = {
      totalRequests: 0,
      successfulRoutes: 0,
      failedRoutes: 0,
      averageRoutingTime: 0,
      requestsPerSecond: 0,
      backendStats: new Map(),
      regionStats: new Map()
    };

    this.initializeBackends();
  }

  /**
   * Initialize backend servers
   */
  private initializeBackends(): void {
    for (const backend of this.config.backends) {
      this.backends.set(backend.id, backend);
      this.stats.backendStats.set(backend.id, {
        requests: 0,
        connections: 0,
        responseTime: 0,
        errorRate: 0
      });
    }

    this.emit('backends-initialized', {
      count: this.backends.size,
      backends: Array.from(this.backends.keys())
    });
  }

  /**
   * Start the load balancer
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      throw new Error('Load balancer already running');
    }

    this.isRunning = true;
    this.emit('started');

    // Start health checks
    if (this.config.healthCheck.enabled) {
      this.startHealthChecks();
    }

    // Start metrics collection
    if (this.config.enableMetrics) {
      this.startMetricsCollection();
    }

    // Start rate limit cleanup
    this.startRateLimitCleanup();
  }

  /**
   * Stop the load balancer
   */
  async stop(): Promise<void> {
    this.isRunning = false;
    this.emit('stopped');
  }

  /**
   * Route a request to a backend server
   */
  async route(request: RoutingRequest): Promise<RoutingResult> {
    const startTime = Date.now();

    try {
      // Check DDoS protection
      if (this.config.ddosProtection.enabled) {
        if (!this.checkRateLimit(request.clientIp)) {
          throw new Error('Rate limit exceeded');
        }
      }

      // Check session affinity
      let backend: BackendServer | null = null;
      let sessionAffinity = false;

      if (this.config.sessionAffinity.enabled && request.sessionId) {
        const backendId = this.sessions.get(request.sessionId);
        if (backendId) {
          const sessionBackend = this.backends.get(backendId);
          if (sessionBackend && sessionBackend.state === BackendState.HEALTHY) {
            backend = sessionBackend;
            sessionAffinity = true;
          }
        }
      }

      // Select backend using algorithm
      if (!backend) {
        backend = await this.selectBackend(request);
        
        // Store session affinity
        if (this.config.sessionAffinity.enabled && request.sessionId) {
          this.sessions.set(request.sessionId, backend.id);
          setTimeout(() => {
            this.sessions.delete(request.sessionId!);
          }, this.config.sessionAffinity.ttl * 1000);
        }
      }

      if (!backend) {
        throw new Error('No healthy backend available');
      }

      // Update backend connections
      backend.currentConnections++;

      const routingTime = Date.now() - startTime;

      // Update statistics
      this.updateStats(backend, routingTime, true);

      this.emit('route-success', {
        requestId: request.requestId,
        backendId: backend.id,
        routingTime
      });

      return {
        requestId: request.requestId,
        backend,
        routingTime,
        algorithm: this.config.algorithm,
        sessionAffinity
      };

    } catch (error) {
      const routingTime = Date.now() - startTime;
      
      this.stats.failedRoutes++;
      
      this.emit('route-failed', {
        requestId: request.requestId,
        error: error instanceof Error ? error.message : 'Unknown error',
        routingTime
      });

      throw error;
    }
  }

  /**
   * Release backend connection
   */
  releaseConnection(backendId: string): void {
    const backend = this.backends.get(backendId);
    if (backend && backend.currentConnections > 0) {
      backend.currentConnections--;
    }
  }

  /**
   * Add backend server
   */
  addBackend(backend: BackendServer): void {
    this.backends.set(backend.id, backend);
    this.stats.backendStats.set(backend.id, {
      requests: 0,
      connections: 0,
      responseTime: 0,
      errorRate: 0
    });

    this.emit('backend-added', { backendId: backend.id });
  }

  /**
   * Remove backend server
   */
  removeBackend(backendId: string): void {
    const backend = this.backends.get(backendId);
    if (backend) {
      // Set to draining state first
      backend.state = BackendState.DRAINING;
      
      // Wait for connections to drain
      setTimeout(() => {
        this.backends.delete(backendId);
        this.stats.backendStats.delete(backendId);
        this.emit('backend-removed', { backendId });
      }, 30000); // 30 second drain period
    }
  }

  /**
   * Update backend health
   */
  updateBackendHealth(backendId: string, healthScore: number): void {
    const backend = this.backends.get(backendId);
    if (backend) {
      backend.healthScore = healthScore;
      
      // Update state based on health score
      if (healthScore >= 80) {
        backend.state = BackendState.HEALTHY;
      } else if (healthScore >= 50) {
        backend.state = BackendState.DEGRADED;
      } else {
        backend.state = BackendState.UNHEALTHY;
      }

      this.emit('backend-health-updated', {
        backendId,
        healthScore,
        state: backend.state
      });
    }
  }

  /**
   * Get load balancer statistics
   */
  getStats(): LoadBalancerStats {
    return { ...this.stats };
  }

  /**
   * Get healthy backends
   */
  getHealthyBackends(): BackendServer[] {
    return Array.from(this.backends.values()).filter(
      b => b.state === BackendState.HEALTHY || b.state === BackendState.DEGRADED
    );
  }

  /**
   * Select backend using configured algorithm
   */
  private async selectBackend(request: RoutingRequest): Promise<BackendServer> {
    const healthyBackends = this.getHealthyBackends();
    
    if (healthyBackends.length === 0) {
      throw new Error('No healthy backends available');
    }

    switch (this.config.algorithm) {
      case LoadBalancingAlgorithm.ROUND_ROBIN:
        return this.selectRoundRobin(healthyBackends);
      
      case LoadBalancingAlgorithm.LEAST_CONNECTIONS:
        return this.selectLeastConnections(healthyBackends);
      
      case LoadBalancingAlgorithm.LEAST_RESPONSE_TIME:
        return this.selectLeastResponseTime(healthyBackends);
      
      case LoadBalancingAlgorithm.IP_HASH:
        return this.selectIpHash(healthyBackends, request.clientIp);
      
      case LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN:
        return this.selectWeightedRoundRobin(healthyBackends);
      
      case LoadBalancingAlgorithm.GEOGRAPHIC:
        return this.selectGeographic(healthyBackends, request.clientRegion);
      
      case LoadBalancingAlgorithm.HEALTH_BASED:
        return this.selectHealthBased(healthyBackends);
      
      case LoadBalancingAlgorithm.ADAPTIVE:
        return this.selectAdaptive(healthyBackends, request);
      
      default:
        return healthyBackends[0];
    }
  }

  /**
   * Round-robin selection
   */
  private selectRoundRobin(backends: BackendServer[]): BackendServer {
    const backend = backends[this.roundRobinIndex % backends.length];
    this.roundRobinIndex++;
    return backend;
  }

  /**
   * Least connections selection
   */
  private selectLeastConnections(backends: BackendServer[]): BackendServer {
    return backends.reduce((least, current) => 
      current.currentConnections < least.currentConnections ? current : least
    );
  }

  /**
   * Least response time selection
   */
  private selectLeastResponseTime(backends: BackendServer[]): BackendServer {
    return backends.reduce((fastest, current) =>
      current.responseTime < fastest.responseTime ? current : fastest
    );
  }

  /**
   * IP hash selection
   */
  private selectIpHash(backends: BackendServer[], clientIp: string): BackendServer {
    const hash = this.hashString(clientIp);
    const index = hash % backends.length;
    return backends[index];
  }

  /**
   * Weighted round-robin selection
   */
  private selectWeightedRoundRobin(backends: BackendServer[]): BackendServer {
    const totalWeight = backends.reduce((sum, b) => sum + b.weight, 0);
    let random = Math.random() * totalWeight;
    
    for (const backend of backends) {
      random -= backend.weight;
      if (random <= 0) {
        return backend;
      }
    }
    
    return backends[0];
  }

  /**
   * Geographic selection
   */
  private selectGeographic(
    backends: BackendServer[],
    clientRegion?: GeographicRegion
  ): BackendServer {
    if (!clientRegion) {
      return this.selectRoundRobin(backends);
    }

    // Find backends in same region
    const sameRegion = backends.filter(
      b => b.region.id === clientRegion.id
    );
    
    if (sameRegion.length > 0) {
      return this.selectLeastConnections(sameRegion);
    }

    // Find closest region by distance
    return backends.reduce((closest, current) => {
      const currentDistance = this.calculateDistance(
        clientRegion,
        current.region
      );
      const closestDistance = this.calculateDistance(
        clientRegion,
        closest.region
      );
      return currentDistance < closestDistance ? current : closest;
    });
  }

  /**
   * Health-based selection
   */
  private selectHealthBased(backends: BackendServer[]): BackendServer {
    return backends.reduce((healthiest, current) =>
      current.healthScore > healthiest.healthScore ? current : healthiest
    );
  }

  /**
   * Adaptive selection (combines multiple factors)
   */
  private selectAdaptive(
    backends: BackendServer[],
    request: RoutingRequest
  ): BackendServer {
    // Score each backend based on multiple factors
    const scores = backends.map(backend => {
      let score = 0;
      
      // Health score (40% weight)
      score += (backend.healthScore / 100) * 0.4;
      
      // Connection load (30% weight)
      const connectionRatio = backend.currentConnections / backend.maxConnections;
      score += (1 - connectionRatio) * 0.3;
      
      // Response time (20% weight)
      const maxResponseTime = Math.max(...backends.map(b => b.responseTime));
      score += (1 - (backend.responseTime / maxResponseTime)) * 0.2;
      
      // Geographic proximity (10% weight)
      if (request.clientRegion) {
        const distance = this.calculateDistance(request.clientRegion, backend.region);
        const maxDistance = Math.max(...backends.map(b => 
          this.calculateDistance(request.clientRegion!, b.region)
        ));
        score += (1 - (distance / maxDistance)) * 0.1;
      }
      
      return { backend, score };
    });

    // Select backend with highest score
    return scores.reduce((best, current) =>
      current.score > best.score ? current : best
    ).backend;
  }

  /**
   * Check rate limit
   */
  private checkRateLimit(clientIp: string): boolean {
    // Check whitelist
    if (this.config.ddosProtection.whitelist.includes(clientIp)) {
      return true;
    }

    // Check blacklist
    if (this.config.ddosProtection.blacklist.includes(clientIp)) {
      return false;
    }

    const now = Date.now();
    const limit = this.rateLimits.get(clientIp);

    if (!limit || now > limit.resetTime) {
      // Reset or create new limit
      this.rateLimits.set(clientIp, {
        count: 1,
        resetTime: now + 1000 // 1 second window
      });
      return true;
    }

    if (limit.count < this.config.ddosProtection.rateLimit) {
      limit.count++;
      return true;
    }

    // Rate limit exceeded
    if (limit.count === this.config.ddosProtection.rateLimit) {
      // Add to temporary blacklist
      setTimeout(() => {
        this.rateLimits.delete(clientIp);
      }, this.config.ddosProtection.blockDuration * 1000);
    }

    return false;
  }

  /**
   * Update statistics
   */
  private updateStats(
    backend: BackendServer,
    routingTime: number,
    success: boolean
  ): void {
    this.stats.totalRequests++;
    
    if (success) {
      this.stats.successfulRoutes++;
    }

    // Update average routing time
    this.stats.averageRoutingTime = 
      (this.stats.averageRoutingTime * (this.stats.totalRequests - 1) + routingTime) /
      this.stats.totalRequests;

    // Update backend stats
    const backendStats = this.stats.backendStats.get(backend.id);
    if (backendStats) {
      backendStats.requests++;
      backendStats.connections = backend.currentConnections;
      backendStats.responseTime = backend.responseTime;
    }

    // Update region stats
    const regionStats = this.stats.regionStats.get(backend.region.id);
    if (regionStats) {
      regionStats.requests++;
      regionStats.averageLatency = 
        (regionStats.averageLatency * (regionStats.requests - 1) + routingTime) /
        regionStats.requests;
    } else {
      this.stats.regionStats.set(backend.region.id, {
        requests: 1,
        averageLatency: routingTime
      });
    }
  }

  /**
   * Calculate geographic distance (Haversine formula)
   */
  private calculateDistance(
    region1: GeographicRegion,
    region2: GeographicRegion
  ): number {
    const R = 6371; // Earth's radius in km
    const dLat = this.toRadians(region2.latitude - region1.latitude);
    const dLon = this.toRadians(region2.longitude - region1.longitude);
    
    const a = 
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRadians(region1.latitude)) *
      Math.cos(this.toRadians(region2.latitude)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  /**
   * Convert degrees to radians
   */
  private toRadians(degrees: number): number {
    return degrees * (Math.PI / 180);
  }

  /**
   * Hash string to number
   */
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }

  /**
   * Start health checks
   */
  private startHealthChecks(): void {
    setInterval(async () => {
      if (!this.isRunning) return;

      for (const backend of this.backends.values()) {
        try {
          const healthScore = await this.performHealthCheck(backend);
          this.updateBackendHealth(backend.id, healthScore);
        } catch (error) {
          this.updateBackendHealth(backend.id, 0);
        }
      }
    }, this.config.healthCheck.interval * 1000);
  }

  /**
   * Perform health check on backend
   */
  private async performHealthCheck(backend: BackendServer): Promise<number> {
    // Simplified health check - in production, would make actual HTTP request
    const factors = {
      state: backend.state === BackendState.HEALTHY ? 100 : 
             backend.state === BackendState.DEGRADED ? 60 : 0,
      connections: (1 - backend.currentConnections / backend.maxConnections) * 100,
      responseTime: Math.max(0, 100 - backend.responseTime)
    };

    return (factors.state * 0.5 + factors.connections * 0.3 + factors.responseTime * 0.2);
  }

  /**
   * Start metrics collection
   */
  private startMetricsCollection(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      // Calculate requests per second
      const now = Date.now();
      this.stats.requestsPerSecond = this.stats.totalRequests; // Simplified

      this.emit('metrics-collected', this.getStats());
    }, this.config.metricsInterval * 1000);
  }

  /**
   * Start rate limit cleanup
   */
  private startRateLimitCleanup(): void {
    setInterval(() => {
      const now = Date.now();
      for (const [ip, limit] of this.rateLimits.entries()) {
        if (now > limit.resetTime) {
          this.rateLimits.delete(ip);
        }
      }
    }, 60000); // Cleanup every minute
  }
}

/**
 * Create global load balancer with default configuration
 */
export function createGlobalLoadBalancer(
  customConfig?: Partial<GlobalLoadBalancerConfig>
): GlobalLoadBalancer {
  const defaultConfig: GlobalLoadBalancerConfig = {
    algorithm: LoadBalancingAlgorithm.ADAPTIVE,
    backends: [],
    healthCheck: {
      enabled: true,
      interval: 30,
      timeout: 5,
      healthyThreshold: 2,
      unhealthyThreshold: 3
    },
    sessionAffinity: {
      enabled: true,
      type: 'cookie',
      cookieName: 'LBSESSION',
      ttl: 3600
    },
    ddosProtection: {
      enabled: true,
      rateLimit: 1000,
      burstSize: 100,
      blockDuration: 300,
      whitelist: [],
      blacklist: []
    },
    enableMetrics: true,
    metricsInterval: 60
  };

  const config = { ...defaultConfig, ...customConfig };
  return new GlobalLoadBalancer(config);
}