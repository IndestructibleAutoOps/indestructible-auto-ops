/**
 * GL Evolution API Server
 * @GL-layer: GL12
 * @GL-semantic: evolution-api
 * @GL-audit-trail: ../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * REST API for Self-Evolving Runtime functionality
 */

import express, { Request, Response } from 'express';
import { SelfRewritingEngine, RewriteOperation } from '../evolution/self-rewriting-engine';
import { EvolutionaryStrategyEngine } from '../evolution/evolutionary-strategy-engine';
import { StructuralMutationEngine, Mutation } from '../evolution/structural-mutation-engine';
import { SelfOptimizationLoop } from '../evolution/self-optimization-loop';
import { EvolutionaryMemory, MemoryEntry } from '../evolution/evolutionary-memory';
import { SelfVersioning, VersionChange } from '../evolution/self-versioning';

const app = express();
const PORT = process.env.PORT || 3002;
app.use(express.json());

// Global instances
let rewritingEngine: SelfRewritingEngine;
let strategyEngine: EvolutionaryStrategyEngine;
let mutationEngine: StructuralMutationEngine;
let optimizationLoop: SelfOptimizationLoop;
let evolutionaryMemory: EvolutionaryMemory;
let selfVersioning: SelfVersioning;

// Initialize all components
async function initializeEvolution() {
  rewritingEngine = new SelfRewritingEngine();
  strategyEngine = new EvolutionaryStrategyEngine();
  mutationEngine = new StructuralMutationEngine();
  optimizationLoop = new SelfOptimizationLoop();
  evolutionaryMemory = new EvolutionaryMemory();
  selfVersioning = new SelfVersioning();
  
  console.log('GL Self-Evolving Runtime initialized successfully');
}

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'gl-evolution',
    version: '12.0.0',
    timestamp: new Date().toISOString()
  });
});

// Self-Rewriting Engine endpoints
app.get('/api/v12/rewriting/history', (req: Request, res: Response) => {
  const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
  res.json({
    success: true,
    data: rewritingEngine.getRewriteHistory(limit)
  });
});

app.post('/api/v12/rewriting/propose', async (req: Request, res: Response) => {
  try {
    const operation: RewriteOperation = req.body;
    const success = await rewritingEngine.proposeRewrite(operation);
    res.json({ success, data: { operation } });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

app.post('/api/v12/rewriting/execute', async (req: Request, res: Response) => {
  try {
    const operation: RewriteOperation = req.body;
    const result = await rewritingEngine.executeRewrite(operation);
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Evolutionary Strategy Engine endpoints
app.get('/api/v12/strategy/population', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: strategyEngine.getPopulation()
  });
});

app.get('/api/v12/strategy/best', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: strategyEngine.getBestStrategy()
  });
});

app.post('/api/v12/strategy/evolve', async (req: Request, res: Response) => {
  try {
    const generations = req.query.generations ? parseInt(req.query.generations as string) : 10;
    const results = await strategyEngine.evolve(generations);
    res.json({ success: true, data: results });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

app.post('/api/v12/strategy/stop', (req: Request, res: Response) => {
  strategyEngine.stop();
  res.json({ success: true, message: 'Evolution stopped' });
});

// Structural Mutation Engine endpoints
app.get('/api/v12/mutation/history', (req: Request, res: Response) => {
  const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
  res.json({
    success: true,
    data: mutationEngine.getMutationHistory(limit)
  });
});

app.post('/api/v12/mutation/execute', async (req: Request, res: Response) => {
  try {
    const mutation: Mutation = req.body;
    const result = await mutationEngine.executeMutation(mutation);
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Self-Optimization Loop endpoints
app.get('/api/v12/optimization/current', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: optimizationLoop.getCurrentCycle()
  });
});

app.get('/api/v12/optimization/history', (req: Request, res: Response) => {
  const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
  res.json({
    success: true,
    data: optimizationLoop.getCycleHistory(limit)
  });
});

app.post('/api/v12/optimization/start', async (req: Request, res: Response) => {
  try {
    await optimizationLoop.start();
    res.json({ success: true, message: 'Optimization loop started' });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

app.post('/api/v12/optimization/stop', (req: Request, res: Response) => {
  optimizationLoop.stop();
  res.json({ success: true, message: 'Optimization loop stopped' });
});

// Evolutionary Memory endpoints
app.get('/api/v12/memory/statistics', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: evolutionaryMemory.getStatistics()
  });
});

app.post('/api/v12/memory/query', async (req: Request, res: Response) => {
  try {
    const query = req.body;
    const results = await evolutionaryMemory.query(query);
    res.json({ success: true, data: results, count: results.length });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

app.post('/api/v12/memory/store', async (req: Request, res: Response) => {
  try {
    const entry: MemoryEntry = req.body;
    await evolutionaryMemory.store(entry);
    res.json({ success: true, data: { id: entry.id } });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Self-Versioning endpoints
app.get('/api/v12/version/current', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: selfVersioning.getCurrentVersion()
  });
});

app.get('/api/v12/version/all', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: selfVersioning.getAllVersions()
  });
});

app.post('/api/v12/version/create', async (req: Request, res: Response) => {
  try {
    const { baseVersion, changes, type } = req.body;
    const version = await selfVersioning.createVersion(baseVersion, changes, type);
    res.json({ success: true, data: version });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

app.post('/api/v12/version/deploy', async (req: Request, res: Response) => {
  try {
    const { versionId } = req.body;
    const success = await selfVersioning.deployVersion(versionId);
    res.json({ success, data: { versionId, deployed: success } });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

// Start server
app.listen(PORT, async () => {
  console.log(`GL Evolution API Server running on port ${PORT}`);
  await initializeEvolution();
});

export { app, initializeEvolution };