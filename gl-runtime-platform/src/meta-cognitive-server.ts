# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: typescript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Meta-Cognitive Runtime API Server (Version 14.0.0)
 * 
 * REST API server for all meta-cognitive capabilities:
 * - Self-Awareness
 * - Meta-Reasoning
 * - Self-Monitoring
 * - Meta-Correction
 * - Reflective Memory
 * - Meta-Cognitive Feedback Loop
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import { MetaCognitiveRuntime } from '../meta-cognition';

const app = express();
const PORT = process.env.META_COGNITIVE_PORT || 3005;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Meta-Cognitive Runtime
const metaRuntime = new MetaCognitiveRuntime();

// ============================================================================
// HEALTH ENDPOINTS
// ============================================================================

app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    version: '14.0.0',
    metaCognitive: 'active',
    components: {
      selfAwareness: 'active',
      metaReasoning: 'active',
      selfMonitoring: 'active',
      metaCorrection: 'active',
      reflectiveMemory: 'active',
      feedbackLoop: 'active'
    }
  });
});

// ============================================================================
// META-COGNITIVE STATUS ENDPOINTS
// ============================================================================

app.get('/api/v14/meta-cognitive/status', async (req: Request, res: Response) => {
  try {
    const summary = await metaRuntime.getSummary();
    res.json(summary);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get meta-cognitive status' });
  }
});

app.get('/api/v14/meta-cognitive/state', async (req: Request, res: Response) => {
  try {
    const state = await metaRuntime.getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get meta-cognitive state' });
  }
});

// ============================================================================
// SELF-AWARENESS ENDPOINTS
// ============================================================================

app.get('/api/v14/awareness/state', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getSelfAwareness().getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get awareness state' });
  }
});

app.get('/api/v14/awareness/observations', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const observations = metaRuntime.getSelfAwareness().getObservations({
      type,
      limit
    });
    
    res.json(observations);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get observations' });
  }
});

app.get('/api/v14/awareness/self-model', (req: Request, res: Response) => {
  try {
    const selfModel = metaRuntime.getSelfAwareness().getSelfModel();
    res.json(selfModel);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get self-model' });
  }
});

app.get('/api/v14/awareness/behavior-patterns', (req: Request, res: Response) => {
  try {
    const patterns = metaRuntime.getSelfAwareness().getBehaviorPatterns();
    res.json(patterns);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get behavior patterns' });
  }
});

// ============================================================================
// META-REASONING ENDPOINTS
// ============================================================================

app.get('/api/v14/reasoning/state', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getMetaReasoning().getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get reasoning state' });
  }
});

app.get('/api/v14/reasoning/history', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const history = metaRuntime.getMetaReasoning().getReasoningHistory(limit);
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get reasoning history' });
  }
});

app.get('/api/v14/reasoning/strategies', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const strategies = metaRuntime.getMetaReasoning().getStrategyHistory(limit);
    res.json(strategies);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get strategy history' });
  }
});

app.get('/api/v14/reasoning/decisions', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const decisions = metaRuntime.getMetaReasoning().getDecisionHistory(limit);
    res.json(decisions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get decision history' });
  }
});

// ============================================================================
// SELF-MONITORING ENDPOINTS
// ============================================================================

app.get('/api/v14/monitoring/state', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getSelfMonitoring().getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get monitoring state' });
  }
});

app.get('/api/v14/monitoring/performance', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getSelfMonitoring().getState();
    res.json(state.performanceMetrics);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get performance metrics' });
  }
});

app.get('/api/v14/monitoring/errors', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : 50;
    const errors = metaRuntime.getSelfMonitoring().getRecentErrors(limit);
    res.json(errors);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get recent errors' });
  }
});

app.get('/api/v14/monitoring/alerts', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const severity = req.query.severity as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const alerts = metaRuntime.getSelfMonitoring().getAlerts({
      type,
      severity,
      limit
    });
    
    res.json(alerts);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get alerts' });
  }
});

app.get('/api/v14/monitoring/version-history', (req: Request, res: Response) => {
  try {
    const history = metaRuntime.getSelfMonitoring().getVersionHistory();
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get version history' });
  }
});

// ============================================================================
// META-CORRECTION ENDPOINTS
// ============================================================================

app.get('/api/v14/correction/state', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getMetaCorrection().getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get correction state' });
  }
});

app.get('/api/v14/correction/history', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const history = metaRuntime.getMetaCorrection().getCorrectionHistory({
      type,
      limit
    });
    
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get correction history' });
  }
});

app.get('/api/v14/correction/suggestions', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const applied = req.query.applied === 'true';
    const severity = req.query.severity as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const suggestions = metaRuntime.getMetaCorrection().getSuggestions({
      type,
      applied,
      severity,
      limit
    });
    
    res.json(suggestions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get correction suggestions' });
  }
});

// ============================================================================
// REFLECTIVE MEMORY ENDPOINTS
// ============================================================================

app.get('/api/v14/memory/state', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getReflectiveMemory().getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get memory state' });
  }
});

app.get('/api/v14/memories', async (req: Request, res: Response) => {
  try {
    const category = req.query.category as string;
    const memoryType = req.query.memoryType as string;
    const tags = req.query.tags as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const minConfidence = req.query.minConfidence ? parseFloat(req.query.minConfidence as string) : undefined;
    const minEffectiveness = req.query.minEffectiveness ? parseFloat(req.query.minEffectiveness as string) : undefined;
    
    const memories = await metaRuntime.getReflectiveMemory().retrieveMemories({
      category,
      memoryType,
      tags: tags ? tags.split(',') : undefined,
      limit,
      minConfidence,
      minEffectiveness
    });
    
    res.json(memories);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve memories' });
  }
});

app.get('/api/v14/memory/search', async (req: Request, res: Response) => {
  try {
    const keywords = req.query.keywords as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : 20;
    
    if (!keywords) {
      return res.status(400).json({ error: 'Keywords parameter is required' });
    }
    
    const memories = await metaRuntime.getReflectiveMemory().semanticSearch(
      keywords.split(','),
      limit
    );
    
    res.json(memories);
  } catch (error) {
    res.status(500).json({ error: 'Failed to search memories' });
  }
});

app.get('/api/v14/memory/wisdom', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const minMaturity = req.query.minMaturity ? parseFloat(req.query.minMaturity as string) : undefined;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const wisdom = metaRuntime.getReflectiveMemory().getWisdom({
      type,
      minMaturity,
      limit
    });
    
    res.json(wisdom);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get wisdom' });
  }
});

// ============================================================================
// FEEDBACK LOOP ENDPOINTS
// ============================================================================

app.get('/api/v14/feedback/state', (req: Request, res: Response) => {
  try {
    const state = metaRuntime.getFeedbackLoop().getState();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get feedback loop state' });
  }
});

app.get('/api/v14/feedback/cycles', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const cycles = metaRuntime.getFeedbackLoop().getCycles(limit);
    res.json(cycles);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get feedback cycles' });
  }
});

app.get('/api/v14/feedback/suggestions', (req: Request, res: Response) => {
  try {
    const target = req.query.target as string;
    const applied = req.query.applied === 'true';
    const priority = req.query.priority as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const suggestions = metaRuntime.getFeedbackLoop().getSuggestions({
      target,
      applied,
      priority,
      limit
    });
    
    res.json(suggestions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get optimization suggestions' });
  }
});

// ============================================================================
// CONTROL ENDPOINTS
// ============================================================================

app.post('/api/v14/meta-cognitive/start', async (req: Request, res: Response) => {
  try {
    const intervalMs = req.body.intervalMs || 60000;
    await metaRuntime.start(intervalMs);
    res.json({ status: 'started', intervalMs });
  } catch (error) {
    res.status(500).json({ error: 'Failed to start meta-cognitive runtime' });
  }
});

app.post('/api/v14/meta-cognitive/stop', async (req: Request, res: Response) => {
  try {
    await metaRuntime.stop();
    res.json({ status: 'stopped' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to stop meta-cognitive runtime' });
  }
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

app.use((err: Error, req: Request, res: Response, next: any) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error', message: err.message });
});

// ============================================================================
// START SERVER
// ============================================================================

if (require.main === module) {
  metaRuntime.initialize().then(() => {
    metaRuntime.start(60000).then(() => {
      app.listen(PORT, () => {
        console.log(`🌌 GL Meta-Cognitive Runtime v14.0.0`);
        console.log(`🚀 Server running on port ${PORT}`);
        console.log(`🧠 Meta-Cognitive capabilities active`);
        console.log(`📊 Status: http://localhost:${PORT}/health`);
        console.log(`📈 Summary: http://localhost:${PORT}/api/v14/meta-cognitive/status`);
      });
    });
  }).catch(error => {
    console.error('Failed to initialize Meta-Cognitive Runtime:', error);
    process.exit(1);
  });
}

export default app;