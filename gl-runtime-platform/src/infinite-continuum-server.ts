// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - REST API Server
 * Version 20.0.0
 * Extended server for continuum management and monitoring
 */

import express, { Request, Response, Router } from 'express';
import { InfiniteLearningContinuum } from './infinite-continuum';
import { UnifiedIntelligenceFabric } from '../unified-intelligence-fabric';

export class InfiniteContinuumServer {
  private app: express.Application;
  private router: Router;
  private continuum: InfiniteLearningContinuum;
  private fabric: UnifiedIntelligenceFabric;
  private port: number;
  private server: any = null;

  constructor(
    fabric: UnifiedIntelligenceFabric,
    port: number = 8081
  ) {
    this.fabric = fabric;
    this.port = port;
    this.app = express();
    this.router = Router();
    
    // Initialize continuum
    this.continuum = new InfiniteLearningContinuum(fabric);

    // Middleware
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // Routes
    this.setupRoutes();
    this.app.use('/api/v20/continuum', this.router);
  }

  /**
   * Setup API routes
   */
  private setupRoutes(): void {
    // Lifecycle Management
    this.router.post('/initialize', this.initialize.bind(this));
    this.router.post('/start', this.start.bind(this));
    this.router.post('/stop', this.stop.bind(this));
    this.router.get('/status', this.getStatus.bind(this));
    this.router.get('/health', this.getHealth.bind(this));

    // Knowledge Accretion
    this.router.get('/knowledge/metrics', this.getKnowledgeMetrics.bind(this));
    this.router.post('/knowledge/nodes', this.addKnowledgeNode.bind(this));
    this.router.get('/knowledge/nodes', this.getKnowledgeNodes.bind(this));
    this.router.get('/knowledge/search', this.searchKnowledge.bind(this));

    // Semantic Reformation
    this.router.get('/semantic/clusters', this.getClusters.bind(this));
    this.router.get('/semantic/boundaries', this.getBoundaries.bind(this));
    this.router.get('/semantic/history', this.getReformationHistory.bind(this));

    // Algorithmic Evolution
    this.router.get('/algorithms/population', this.getPopulation.bind(this));
    this.router.get('/algorithms/best', this.getBestAlgorithm.bind(this));
    this.router.get('/algorithms/stats', this.getAlgorithmStats.bind(this));
    this.router.post('/algorithms/initial', this.addInitialAlgorithm.bind(this));

    // Infinite Composition
    this.router.post('/composition/generate', this.generateComposition.bind(this));
    this.router.get('/composition/:id', this.getComposition.bind(this));
    this.router.post('/composition/:id/execute', this.executeComposition.bind(this));
    this.router.get('/composition/stats', this.getCompositionStats.bind(this));

    // Fabric Expansion
    this.router.get('/expansion/stats', this.getExpansionStats.bind(this));
    this.router.get('/expansion/history', this.getExpansionHistory.bind(this));
    this.router.post('/expansion/trigger', this.triggerExpansion.bind(this));
    this.router.post('/expansion/prune', this.pruneFabric.bind(this));

    // Continuum Memory
    this.router.post('/memory/store', this.storeMemory.bind(this));
    this.router.get('/memory/:id', this.retrieveMemory.bind(this));
    this.router.get('/memory/search', this.searchMemory.bind(this));
    this.router.get('/memory/recent', this.getRecentMemories.bind(this));
    this.router.get('/memory/stats', this.getMemoryStats.bind(this));

    // Continuum Management
    this.router.get('/metrics', this.getMetrics.bind(this));
    this.router.get('/config', this.getConfig.bind(this));
    this.router.put('/config', this.updateConfig.bind(this));
    this.router.get('/state/export', this.exportState.bind(this));
    this.router.post('/state/import', this.importState.bind(this));
    this.router.post('/reset', this.resetContinuum.bind(this));
  }

  // ============================================================================
  // Lifecycle Management Routes
  // ============================================================================

  private async initialize(req: Request, res: Response): Promise<void> {
    try {
      await this.continuum.initialize();
      res.json({ success: true, message: 'Continuum initialized' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async start(req: Request, res: Response): Promise<void> {
    try {
      await this.continuum.start();
      res.json({ success: true, message: 'Continuum started' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async stop(req: Request, res: Response): Promise<void> {
    try {
      await this.continuum.stop();
      res.json({ success: true, message: 'Continuum stopped' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getStatus(req: Request, res: Response): Promise<void> {
    try {
      const status = {
        initialized: this.continuum.isInitialized(),
        started: this.continuum.isStarted(),
        version: InfiniteLearningContinuum.VERSION
      };
      res.json(status);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getHealth(req: Request, res: Response): Promise<void> {
    try {
      const health = this.continuum.getHealthStatus();
      const statusCode = health.status === 'healthy' ? 200 : 
                        health.status === 'degraded' ? 200 : 503;
      res.status(statusCode).json(health);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Knowledge Accretion Routes
  // ============================================================================

  private async getKnowledgeMetrics(req: Request, res: Response): Promise<void> {
    try {
      const metrics = this.continuum.getKnowledgeAccretion().getMetrics();
      res.json(metrics);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async addKnowledgeNode(req: Request, res: Response): Promise<void> {
    try {
      const { content, type, source, confidence } = req.body;
      const nodeId = this.continuum.getKnowledgeAccretion().addKnowledgeNode(
        content,
        type,
        source,
        confidence
      );
      res.json({ success: true, nodeId });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getKnowledgeNodes(req: Request, res: Response): Promise<void> {
    try {
      const { type, source } = req.query;
      let nodes: any[];

      if (type) {
        // @ts-expect-error - Type validated in queryByType method
        nodes = this.continuum.getKnowledgeAccretion().queryByType(type);
      } else if (source) {
        nodes = this.continuum.getKnowledgeAccretion().queryBySource(source as string);
      } else {
        nodes = Array.from(this.continuum.getKnowledgeAccretion().getKnowledgeGraph().nodes.values());
      }

      res.json({ nodes: nodes.slice(0, 100) }); // Limit to 100
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async searchKnowledge(req: Request, res: Response): Promise<void> {
    try {
      const { query } = req.query;
      if (!query) {
        res.status(400).json({ success: false, error: 'Query parameter required' });
        return;
      }

      const nodes = this.continuum.getKnowledgeAccretion().searchByContent(query as string);
      res.json({ nodes: nodes.slice(0, 50) });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Semantic Reformation Routes
  // ============================================================================

  private async getClusters(req: Request, res: Response): Promise<void> {
    try {
      const clusters = this.continuum.getSemanticReformation().getClusters();
      res.json({ clusters });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getBoundaries(req: Request, res: Response): Promise<void> {
    try {
      const boundaries = this.continuum.getSemanticReformation().getConceptBoundaries();
      res.json({ boundaries });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getReformationHistory(req: Request, res: Response): Promise<void> {
    try {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
      const history = this.continuum.getSemanticReformation().getReformationHistory(limit);
      res.json({ history });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Algorithmic Evolution Routes
  // ============================================================================

  private async getPopulation(req: Request, res: Response): Promise<void> {
    try {
      const population = this.continuum.getAlgorithmicEvolution().getPopulation();
      res.json({ population: population.slice(0, 100) });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getBestAlgorithm(req: Request, res: Response): Promise<void> {
    try {
      const algorithm = this.continuum.getAlgorithmicEvolution().getBestAlgorithm();
      res.json({ algorithm });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getAlgorithmStats(req: Request, res: Response): Promise<void> {
    try {
      const stats = this.continuum.getAlgorithmicEvolution().getPopulationStats();
      res.json(stats);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async addInitialAlgorithm(req: Request, res: Response): Promise<void> {
    try {
      const { algorithmType, parameters } = req.body;
      const genomeId = this.continuum.getAlgorithmicEvolution().addInitialGenome(
        algorithmType,
        parameters
      );
      res.json({ success: true, genomeId });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Infinite Composition Routes
  // ============================================================================

  private async generateComposition(req: Request, res: Response): Promise<void> {
    try {
      const { constraints, seed } = req.body;
      const composition = this.continuum.getInfiniteComposition().generateComposition(
        constraints,
        seed
      );
      res.json({ composition });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getComposition(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const composition = this.continuum.getInfiniteComposition().getComposition(id);
      
      if (!composition) {
        res.status(404).json({ success: false, error: 'Composition not found' });
        return;
      }

      res.json({ composition });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async executeComposition(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const { input } = req.body;
      const result = this.continuum.getInfiniteComposition().executeComposition(id, input);
      res.json({ success: true, result });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getCompositionStats(req: Request, res: Response): Promise<void> {
    try {
      const stats = this.continuum.getInfiniteComposition().getStatistics();
      res.json(stats);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Fabric Expansion Routes
  // ============================================================================

  private async getExpansionStats(req: Request, res: Response): Promise<void> {
    try {
      const stats = this.continuum.getFabricExpansion().getExpansionStats();
      res.json(stats);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getExpansionHistory(req: Request, res: Response): Promise<void> {
    try {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
      const history = this.continuum.getFabricExpansion().getExpansionHistory(limit);
      res.json({ history });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async triggerExpansion(req: Request, res: Response): Promise<void> {
    try {
      const { nodeCount, edgeCount } = req.body;
      this.continuum.getFabricExpansion().triggerManualExpansion(
        nodeCount || 10,
        edgeCount || 20
      );
      res.json({ success: true, message: 'Expansion triggered' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async pruneFabric(req: Request, res: Response): Promise<void> {
    try {
      const { threshold } = req.query;
      const pruned = this.continuum.getFabricExpansion().pruneUnderutilized(
        threshold ? parseFloat(threshold as string) : undefined
      );
      res.json({ success: true, prunedCount: pruned });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Continuum Memory Routes
  // ============================================================================

  private async storeMemory(req: Request, res: Response): Promise<void> {
    try {
      const { data, semanticTags, relatedEvents } = req.body;
      const memoryId = this.continuum.getContinuumMemory().storeMemory(
        data,
        semanticTags || [],
        relatedEvents || []
      );
      res.json({ success: true, memoryId });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async retrieveMemory(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const memory = this.continuum.getContinuumMemory().retrieveMemory(id);
      
      if (!memory) {
        res.status(404).json({ success: false, error: 'Memory not found' });
        return;
      }

      res.json({ memory });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async searchMemory(req: Request, res: Response): Promise<void> {
    try {
      const { query, limit } = req.query;
      if (!query) {
        res.status(400).json({ success: false, error: 'Query parameter required' });
        return;
      }

      const memories = this.continuum.getContinuumMemory().searchByContent(
        query as string,
        limit ? parseInt(limit as string) : 10
      );
      res.json({ memories });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getRecentMemories(req: Request, res: Response): Promise<void> {
    try {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : 10;
      const memories = this.continuum.getContinuumMemory().getRecentMemories(limit);
      res.json({ memories });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getMemoryStats(req: Request, res: Response): Promise<void> {
    try {
      const stats = this.continuum.getContinuumMemory().getStatistics();
      res.json(stats);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Continuum Management Routes
  // ============================================================================

  private async getMetrics(req: Request, res: Response): Promise<void> {
    try {
      const metrics = this.continuum.getMetrics();
      res.json(metrics);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async getConfig(req: Request, res: Response): Promise<void> {
    try {
      const config = this.continuum.getConfig();
      res.json(config);
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async updateConfig(req: Request, res: Response): Promise<void> {
    try {
      this.continuum.updateConfig(req.body);
      res.json({ success: true, message: 'Configuration updated' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async exportState(req: Request, res: Response): Promise<void> {
    try {
      const state = this.continuum.exportState();
      res.json({ state });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async importState(req: Request, res: Response): Promise<void> {
    try {
      const { state } = req.body;
      this.continuum.importState(state);
      res.json({ success: true, message: 'State imported' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  private async resetContinuum(req: Request, res: Response): Promise<void> {
    try {
      await this.continuum.reset();
      res.json({ success: true, message: 'Continuum reset' });
    } catch (error: any) {
      res.status(500).json({ success: false, error: error.message });
    }
  }

  // ============================================================================
  // Server Lifecycle
  // ============================================================================

  /**
   * Start the server
   */
  public async startServer(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.server = this.app.listen(this.port, () => {
        console.log(`Infinite Continuum Server listening on port ${this.port}`);
        resolve();
      });

      this.server.on('error', (error: any) => {
        reject(error);
      });
    });
  }

  /**
   * Stop the server
   */
  public async stopServer(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.server) {
        this.server.close((error: any) => {
          if (error) {
            reject(error);
          } else {
            console.log('Infinite Continuum Server stopped');
            resolve();
          }
        });
      } else {
        resolve();
      }
    });
  }

  /**
   * Get Express app instance
   */
  public getApp(): express.Application {
    return this.app;
  }

  /**
   * Get continuum instance
   */
  public getContinuum(): InfiniteLearningContinuum {
    return this.continuum;
  }
}