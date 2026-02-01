// @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: resource-graph-runtime
# @GL-charter-version: 2.0.0

import { ResourceGraphManager } from '../../governance/gl-resource-graph/resource-graph-manager';
import { GlobalResourceGraph } from '../../governance/gl-resource-graph/resource-graph-manager';
import { EventStreamManager } from '../src/events/event-stream-manager';
import { createLogger } from '../src/utils/logger';

const logger = createLogger('ResourceGraphRuntime');

export interface RuntimeConfig {
  autoRefresh: boolean;
  refreshIntervalMs: number;
  requireGraphForOperations: boolean;
}

export class ResourceGraphRuntime {
  private resourceGraphManager: ResourceGraphManager;
  private eventStream: EventStreamManager;
  private currentGraph: GlobalResourceGraph | null = null;
  private config: RuntimeConfig;

  constructor(config?: Partial<RuntimeConfig>) {
    this.resourceGraphManager = new ResourceGraphManager();
    this.eventStream = new EventStreamManager();
    this.config = {
      autoRefresh: config?.autoRefresh ?? true,
      refreshIntervalMs: config?.refreshIntervalMs ?? 300000, // 5 minutes
      requireGraphForOperations: config?.requireGraphForOperations ?? true
    };

    if (this.config.autoRefresh) {
      this.startAutoRefresh();
    }
  }

  public async initialize(rootPath: string): Promise<void> {
    logger.info(`Initializing Resource Graph Runtime for: ${rootPath}`);
    
    await this.eventStream.logEvent({
      eventType: 'runtime_init_started',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        rootPath,
        autoRefresh: this.config.autoRefresh
      }
    });

    // Build or load Global Resource Graph
    const isFresh = await this.resourceGraphManager.checkGraphFreshness(rootPath);
    
    if (isFresh) {
      // Load existing graph
      // In production, would load from artifact store
      logger.info('Loading existing Global Resource Graph');
    } else {
      // Build new graph
      logger.info('Building new Global Resource Graph');
      this.currentGraph = await this.resourceGraphManager.buildGlobalResourceGraph(rootPath);
    }

    await this.eventStream.logEvent({
      eventType: 'runtime_init_completed',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        nodeCount: this.currentGraph?.nodes.length || 0,
        edgeCount: this.currentGraph?.edges.length || 0
      }
    });

    logger.info('Resource Graph Runtime initialized successfully');
  }

  public async ensureGraphReady(rootPath: string): Promise<void> {
    if (!this.currentGraph) {
      await this.initialize(rootPath);
    } else {
      const isFresh = await this.resourceGraphManager.checkGraphFreshness(rootPath);
      if (!isFresh) {
        logger.info('Refreshing Global Resource Graph');
        this.currentGraph = await this.resourceGraphManager.buildGlobalResourceGraph(rootPath);
      }
    }
  }

  public getCurrentGraph(): GlobalResourceGraph | null {
    return this.currentGraph;
  }

  public async resolveFile(path: string): Promise<any> {
    if (this.config.requireGraphForOperations) {
      await this.ensureGraphReady('.');
    }

    const resolver = this.resourceGraphManager.getResolver();
    return resolver.resolveFile(path);
  }

  public async resolveDependencies(path: string): Promise<any[]> {
    if (this.config.requireGraphForOperations) {
      await this.ensureGraphReady('.');
    }

    const resolver = this.resourceGraphManager.getResolver();
    const node = resolver.resolveFile(path);
    
    if (node) {
      return resolver.getDependencies(node.id);
    }
    
    return [];
  }

  public async resolveMissingDependencies(): Promise<string[]> {
    if (this.config.requireGraphForOperations) {
      await this.ensureGraphReady('.');
    }

    const resolver = this.resourceGraphManager.getResolver();
    const result = resolver.resolveMissingDependencies();
    
    return result.missing || [];
  }

  public async resolveGovernanceCompliance(): Promise<string[]> {
    if (this.config.requireGraphForOperations) {
      await this.ensureGraphReady('.');
    }

    const resolver = this.resourceGraphManager.getResolver();
    const result = resolver.resolveGovernanceCompliance();
    
    return result.missing || [];
  }

  public async getCyclicDependencies(): Promise<string[][]> {
    if (this.config.requireGraphForOperations) {
      await this.ensureGraphReady('.');
    }

    const resolver = this.resourceGraphManager.getResolver();
    return resolver.resolveCyclicDependencies();
  }

  private startAutoRefresh(): void {
    setInterval(async () => {
      try {
        logger.info('Auto-refreshing Global Resource Graph');
        this.currentGraph = await this.resourceGraphManager.buildGlobalResourceGraph('.');
        
        await this.eventStream.logEvent({
          eventType: 'grg_auto_refreshed',
          layer: 'GL90-99',
          semanticAnchor: 'GL-ROOT-GOVERNANCE',
          timestamp: new Date().toISOString(),
          metadata: {
            nodeCount: this.currentGraph?.nodes.length || 0,
            edgeCount: this.currentGraph?.edges.length || 0
          }
        });
      } catch (error: any) {
        logger.error(`Auto-refresh failed: ${error.message}`);
      }
    }, this.config.refreshIntervalMs);
  }

  public async shutdown(): Promise<void> {
    logger.info('Shutting down Resource Graph Runtime');
    // In production, would clean up resources
  }
}