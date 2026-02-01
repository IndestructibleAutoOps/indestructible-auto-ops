// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-server
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - REST API Server
 * Version 19.0.0
 * 
 * 核心：統一智慧織網 API
 * - 提供 Fabric 的所有功能的 REST API 接口
 * - 支援所有 V1-18 能力的統一訪問
 * - 實時狀態監控與控制
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import { UnifiedIntelligenceFabric, FabricStatus } from '../unified-intelligence-fabric';

// ============================================================================
// Server Configuration
// ============================================================================

const PORT = 3011;
const app = express();
let fabric: UnifiedIntelligenceFabric;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ============================================================================
// Health Check
// ============================================================================

app.get('/health', async (req: Request, res: Response) => {
  try {
    if (!fabric || !fabric.isInitialized()) {
      return res.status(503).json({
        status: 'unhealthy',
        message: 'Unified Intelligence Fabric not initialized'
      });
    }
    
    const status = await fabric.getStatus();
    
    res.json({
      status: 'healthy',
      version: '19.0.0',
      timestamp: Date.now(),
      fabric: status
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: (error as Error).message
    });
  }
});

// ============================================================================
// Fabric Status
// ============================================================================

app.get('/api/v19/fabric/status', async (req: Request, res: Response) => {
  try {
    const status = await fabric.getStatus();
    res.json(status);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// High-Level Operations
// ============================================================================

/**
 * POST /api/v19/fabric/reason
 * 在織網上執行推理
 */
app.post('/api/v19/fabric/reason', async (req: Request, res: Response) => {
  try {
    const { query, reasoningStyle, maxDepth } = req.body;
    
    if (!query) {
      return res.status(400).json({
        error: 'Missing required field: query'
      });
    }
    
    const result = await fabric.reason(query, {
      reasoningStyle,
      maxDepth
    });
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/repair
 * 在織網上執行修復
 */
app.post('/api/v19/fabric/repair', async (req: Request, res: Response) => {
  try {
    const { nodeId, issue, strategy } = req.body;
    
    if (!nodeId || !issue) {
      return res.status(400).json({
        error: 'Missing required fields: nodeId, issue'
      });
    }
    
    const result = await fabric.repair(nodeId, issue, {
      strategy
    });
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/evolve
 * 在織網上執行演化
 */
app.post('/api/v19/fabric/evolve', async (req: Request, res: Response) => {
  try {
    const { scope, intensity } = req.body;
    
    await fabric.evolve({
      scope,
      intensity
    });
    
    res.json({
      status: 'evolution_triggered',
      scope,
      intensity,
      timestamp: Date.now()
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/deploy
 * 在織網上執行部署
 */
app.post('/api/v19/fabric/deploy', async (req: Request, res: Response) => {
  try {
    const { target, config } = req.body;
    
    if (!target || !config) {
      return res.status(400).json({
        error: 'Missing required fields: target, config'
      });
    }
    
    const result = await fabric.deploy(target, config);
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// Node and Edge Operations
// ============================================================================

/**
 * POST /api/v19/fabric/nodes
 * 添加節點到織網
 */
app.post('/api/v19/fabric/nodes', async (req: Request, res: Response) => {
  try {
    const node = req.body;
    
    if (!node.id || !node.type || !node.layer) {
      return res.status(400).json({
        error: 'Missing required fields: id, type, layer'
      });
    }
    
    const nodeId = await fabric.addNode(node);
    
    res.json({
      nodeId,
      message: 'Node added successfully'
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * GET /api/v19/fabric/nodes/:id
 * 獲取節點
 */
app.get('/api/v19/fabric/nodes/:id', async (req: Request, res: Response) => {
  try {
    const node = await fabric.getNode(req.params.id);
    
    if (!node) {
      return res.status(404).json({
        error: 'Node not found'
      });
    }
    
    res.json(node);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * PUT /api/v19/fabric/nodes/:id
 * 更新節點
 */
app.put('/api/v19/fabric/nodes/:id', async (req: Request, res: Response) => {
  try {
    await fabric.updateNode(req.params.id, req.body);
    
    res.json({
      message: 'Node updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * DELETE /api/v19/fabric/nodes/:id
 * 刪除節點
 */
app.delete('/api/v19/fabric/nodes/:id', async (req: Request, res: Response) => {
  try {
    await fabric.removeNode(req.params.id);
    
    res.json({
      message: 'Node removed successfully'
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/edges
 * 添加邊到織網
 */
app.post('/api/v19/fabric/edges', async (req: Request, res: Response) => {
  try {
    const edge = req.body;
    
    if (!edge.id || !edge.sourceId || !edge.targetId || !edge.type) {
      return res.status(400).json({
        error: 'Missing required fields: id, sourceId, targetId, type'
      });
    }
    
    const edgeId = await fabric.addEdge(edge);
    
    res.json({
      edgeId,
      message: 'Edge added successfully'
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * GET /api/v19/fabric/nodes
 * 查詢節點
 */
app.get('/api/v19/fabric/nodes', async (req: Request, res: Response) => {
  try {
    const filter = req.query;
    const nodes = await fabric.queryNodes(filter);
    
    res.json({
      count: nodes.length,
      nodes
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * GET /api/v19/fabric/edges
 * 查詢邊
 */
app.get('/api/v19/fabric/edges', async (req: Request, res: Response) => {
  try {
    const filter = req.query;
    const edges = await fabric.queryEdges(filter);
    
    res.json({
      count: edges.length,
      edges
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * GET /api/v19/fabric/path/:source/:target
 * 尋找路徑
 */
app.get('/api/v19/fabric/path/:source/:target', async (req: Request, res: Response) => {
  try {
    const { source, target } = req.params;
    const options = req.query;
    
    const path = await fabric.findPath(source, target, options);
    
    res.json({
      source,
      target,
      path,
      length: path.length
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// Superposition Operations
// ============================================================================

/**
 * GET /api/v19/fabric/superposition/:nodeId/expand
 * 展開疊加態
 */
app.get('/api/v19/fabric/superposition/:nodeId/expand', async (req: Request, res: Response) => {
  try {
    const { nodeId } = req.params;
    const options = req.query;
    
    const result = await fabric.expandSuperposition(nodeId, options);
    
    if (!result) {
      return res.status(404).json({
        error: 'Superposition not found'
      });
    }
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/superposition/:nodeId/collapse
 * 坍縮疊加態
 */
app.post('/api/v19/fabric/superposition/:nodeId/collapse', async (req: Request, res: Response) => {
  try {
    const { nodeId } = req.params;
    const options = req.body;
    
    const result = await fabric.collapseSuperposition(nodeId, options);
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/superposition/merge
 * 合併疊加態
 */
app.post('/api/v19/fabric/superposition/merge', async (req: Request, res: Response) => {
  try {
    const { nodeIds, options } = req.body;
    
    if (!nodeIds || !Array.isArray(nodeIds)) {
      return res.status(400).json({
        error: 'Missing required field: nodeIds (array)'
      });
    }
    
    const result = await fabric.mergeSuperpositions(nodeIds, options);
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// Algorithm Operations
// ============================================================================

/**
 * POST /api/v19/fabric/algorithms
 * 註冊演算法
 */
app.post('/api/v19/fabric/algorithms', async (req: Request, res: Response) => {
  try {
    await fabric.registerAlgorithm(req.body);
    
    res.json({
      message: 'Algorithm registered successfully'
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/algorithms/:id/execute
 * 執行演算法
 */
app.post('/api/v19/fabric/algorithms/:id/execute', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { input, parameters } = req.body;
    
    const result = await fabric.executeAlgorithm(id, input, parameters);
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// Composition Operations
// ============================================================================

/**
 * POST /api/v19/fabric/compositions
 * 註冊組合
 */
app.post('/api/v19/fabric/compositions', async (req: Request, res: Response) => {
  try {
    await fabric.registerComposition(req.body);
    
    res.json({
      message: 'Composition registered successfully'
    });
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

/**
 * POST /api/v19/fabric/compositions/:id/execute
 * 執行組合
 */
app.post('/api/v19/fabric/compositions/:id/execute', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { input, options } = req.body;
    
    const result = await fabric.executeComposition(id, input, options);
    
    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// Demonstration Endpoint
// ============================================================================

/**
 * GET /api/v19/fabric/demonstrate
 * 演示 Fabric 的核心能力
 */
app.get('/api/v19/fabric/demonstrate', async (req: Request, res: Response) => {
  try {
    const demonstrations: any = {
      timestamp: Date.now(),
      fabricVersion: '19.0.0',
      capabilities: {}
    };
    
    // 1. 統一圖演示
    demonstrations.capabilities.unifiedGraph = {
      description: 'All V1-18 capabilities converged into a single unified graph',
      totalNodes: (await fabric.getStatus()).statistics.core.metadata.totalNodes,
      totalEdges: (await fabric.getStatus()).statistics.core.metadata.totalEdges,
      layers: Object.keys((await fabric.getStatus()).statistics.core.layerStats).length
    };
    
    // 2. 疊加態儲存演示
    demonstrations.capabilities.superpositionStorage = {
      description: 'Native superposition storage for multi-version, multi-semantic, multi-reality nodes',
      totalSuperpositions: (await fabric.getStatus()).statistics.storage.totalSuperpositions,
      averageCompressionRatio: (await fabric.getStatus()).statistics.storage.averageCompressionRatio,
      compressionSavings: (await fabric.getStatus()).statistics.storage.compressionSavings.toFixed(2) + '%'
    };
    
    // 3. 智慧流演示
    demonstrations.capabilities.intelligenceFlows = {
      description: 'Reasoning, repair, evolution, deployment flows on the fabric',
      totalFlowsExecuted: (await fabric.getStatus()).statistics.flows.stepsExecuted,
      activeFlows: 0,
      flowTypes: ['reasoning', 'repair', 'evolution', 'deployment', 'execution', 'synchronization']
    };
    
    // 4. 算力流演示
    demonstrations.capabilities.computeFlows = {
      description: 'Compute resources flowing on the fabric',
      totalNodes: (await fabric.getStatus()).statistics.compute.totalNodes,
      activeNodes: (await fabric.getStatus()).statistics.compute.activeNodes,
      runningTasks: (await fabric.getStatus()).statistics.compute.runningTasks
    };
    
    // 5. 演算法演示
    demonstrations.capabilities.algorithmLayer = {
      description: 'Transformation rules flowing on the fabric',
      totalAlgorithms: (await fabric.getStatus()).statistics.algo.totalAlgorithms,
      totalExecutions: (await fabric.getStatus()).statistics.algo.totalExecutions,
      successRate: ((await fabric.getStatus()).statistics.algo.successfulExecutions / 
                    (await fabric.getStatus()).statistics.algo.totalExecutions * 100).toFixed(2) + '%'
    };
    
    // 6. 組合演示
    demonstrations.capabilities.compositionLayer = {
      description: 'Path search and composition on the fabric',
      totalCompositions: (await fabric.getStatus()).statistics.composition.totalCompositions,
      totalExecutions: (await fabric.getStatus()).statistics.composition.totalExecutions,
      compositionTypes: Object.keys((await fabric.getStatus()).statistics.composition.compositionTypes)
    };
    
    // 7. 永續演化演示
    demonstrations.capabilities.perpetualEvolution = {
      description: 'Fabric evolves itself as an intrinsic property',
      generation: (await fabric.getStatus()).statistics.evolution.generation,
      fitness: (await fabric.getStatus()).statistics.evolution.fitness.toFixed(3),
      adaptationRate: (await fabric.getStatus()).statistics.evolution.adaptationRate.toFixed(3),
      stability: (await fabric.getStatus()).statistics.evolution.stability.toFixed(3)
    };
    
    res.json(demonstrations);
  } catch (error) {
    res.status(500).json({
      error: (error as Error).message
    });
  }
});

// ============================================================================
// Server Startup
// ============================================================================

async function startServer() {
  console.log('='.repeat(80));
  console.log('GL Unified Intelligence Fabric v19.0.0 - REST API Server');
  console.log('='.repeat(80));
  
  // Initialize Fabric
  console.log('\nInitializing Unified Intelligence Fabric...');
  fabric = new UnifiedIntelligenceFabric();
  await fabric.initialize();
  
  // Start Server
  app.listen(PORT, () => {
    console.log('\n' + '='.repeat(80));
    console.log(`✓ Fabric Server running on http://localhost:${PORT}`);
    console.log('\nAvailable Endpoints:');
    console.log(`  Health Check:     GET  http://localhost:${PORT}/health`);
    console.log(`  Fabric Status:    GET  http://localhost:${PORT}/api/v19/fabric/status`);
    console.log(`  Reason:           POST http://localhost:${PORT}/api/v19/fabric/reason`);
    console.log(`  Repair:           POST http://localhost:${PORT}/api/v19/fabric/repair`);
    console.log(`  Evolve:           POST http://localhost:${PORT}/api/v19/fabric/evolve`);
    console.log(`  Deploy:           POST http://localhost:${PORT}/api/v19/fabric/deploy`);
    console.log(`  Nodes:            GET  http://localhost:${PORT}/api/v19/fabric/nodes`);
    console.log(`  Edges:            GET  http://localhost:${PORT}/api/v19/fabric/edges`);
    console.log(`  Demonstrate:      GET  http://localhost:${PORT}/api/v19/fabric/demonstrate`);
    console.log('='.repeat(80));
    console.log('\nFabric is ready to accept requests.');
    console.log('All V1-18 capabilities are now converged into the Unified Intelligence Fabric.\n');
  });
}

// Handle shutdown
process.on('SIGTERM', async () => {
  console.log('\nReceived SIGTERM, shutting down gracefully...');
  if (fabric) {
    await fabric.shutdown();
  }
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('\nReceived SIGINT, shutting down gracefully...');
  if (fabric) {
    await fabric.shutdown();
  }
  process.exit(0);
});

// Start server
startServer().catch(error => {
  console.error('Failed to start server:', error);
  process.exit(1);
});