/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Cognitive Mesh API Server
 * @GL-layer: GL11
 * @GL-semantic: cognitive-mesh-api
 * @GL-audit-trail: ../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * REST API for Cognitive Mesh functionality
 */

import express, { Request, Response } from 'express';
import { MeshCore } from '../cognitive-mesh/mesh-core';
import { MeshMemory, MemoryEntry, MemoryQuery } from '../cognitive-mesh/mesh-memory';
import { CognitiveNode } from '../cognitive-mesh/mesh-nodes';
import { RoutingDecision, RoutingRequest } from '../cognitive-mesh/mesh-routing';

const app = express();
const PORT = process.env.PORT || 3001;
app.use(express.json());

// Global mesh instance
let meshCore: MeshCore | null = null;

// Initialize mesh
async function initializeMesh() {
  if (!meshCore) {
    meshCore = new MeshCore({
      maxNodes: 100,
      syncInterval: 5000,
      optimizationThreshold: 0.8,
      emergenceThreshold: 0.7
    });
    await meshCore.initialize();
    console.log('Cognitive Mesh initialized successfully');
  }
  return meshCore;
}

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'gl-cognitive-mesh',
    version: '11.0.0',
    mesh_active: meshCore !== null,
    timestamp: new Date().toISOString()
  });
});

// Get mesh status
app.get('/api/v11/mesh/status', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const state = meshCore!.getState();
    res.json({
      success: true,
      data: state
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Store memory entry
app.post('/api/v11/mesh/memory', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const entry: MemoryEntry = req.body;
    await meshCore!.getMemory().store(entry);
    
    res.json({
      success: true,
      data: { id: entry.id }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Query memory
app.post('/api/v11/mesh/memory/query', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const query: MemoryQuery = req.body;
    const results = await meshCore!.getMemory().query(query);
    
    res.json({
      success: true,
      data: results,
      count: results.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Semantic search
app.get('/api/v11/mesh/memory/search', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const { semanticKey, limit } = req.query;
    const results = await meshCore!.getMemory().semanticSearch(
      semanticKey as string,
      limit ? parseInt(limit as string) : 10
    );
    
    res.json({
      success: true,
      data: results,
      count: results.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Register node
app.post('/api/v11/mesh/nodes', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const nodeData = req.body;
    const nodeId = await meshCore!.getNodes().registerNode(nodeData);
    
    res.json({
      success: true,
      data: { nodeId }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Get all nodes
app.get('/api/v11/mesh/nodes', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const nodes = meshCore!.getNodes().getAllNodes();
    
    res.json({
      success: true,
      data: nodes,
      count: nodes.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Get node statistics
app.get('/api/v11/mesh/nodes/statistics', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const stats = meshCore!.getNodes().getStatistics();
    
    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Route task
app.post('/api/v11/mesh/route', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const request: RoutingRequest = req.body;
    const availableNodes = meshCore!.getNodes().getActiveNodes();
    
    const decision = await meshCore!.getRouting().route(request, availableNodes);
    
    res.json({
      success: true,
      data: decision
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Get sync status
app.get('/api/v11/mesh/sync/status', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const status = meshCore!.getSync().getStatus();
    
    res.json({
      success: true,
      data: status
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Force sync
app.post('/api/v11/mesh/sync/force', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    await meshCore!.getSync().forceSync();
    
    res.json({
      success: true,
      message: 'Sync triggered successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Get optimization metrics
app.get('/api/v11/mesh/optimizer/metrics', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const metrics = meshCore!.getOptimizer().getCurrentMetrics();
    
    res.json({
      success: true,
      data: metrics
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Get emergence metrics
app.get('/api/v11/mesh/emergence/metrics', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const metrics = meshCore!.getEmergence().getMetrics();
    
    res.json({
      success: true,
      data: metrics
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Get recent patterns
app.get('/api/v11/mesh/emergence/patterns', async (req: Request, res: Response) => {
  try {
    if (!meshCore) {
      await initializeMesh();
    }
    
    const limit = req.query.limit ? parseInt(req.query.limit as string) : 10;
    const patterns = meshCore!.getEmergence().getRecentPatterns(limit);
    
    res.json({
      success: true,
      data: patterns,
      count: patterns.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Start server
app.listen(PORT, async () => {
  console.log(`GL Cognitive Mesh API Server running on port ${PORT}`);
  await initializeMesh();
});

export { app, initializeMesh };