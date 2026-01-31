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
 * GL Meta-Cognitive Runtime Deep API Server (Version 14.0.0 Deep)
 * 
 * REST API server for all deep meta-cognitive capabilities:
 * - Deep Consciousness Assessment
 * - Wisdom Extraction and Application
 * - Decision Optimization
 * - Deep Thinking
 * 
 * Integrated with original v14 capabilities
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import { DeepMetaCognitiveRuntime } from '../meta-cognition/deep-index';

const app = express();
const PORT = process.env.DEEP_META_COGNITIVE_PORT || 3006;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Deep Meta-Cognitive Runtime
const deepRuntime = new DeepMetaCognitiveRuntime();

// ============================================================================
// HEALTH ENDPOINTS
// ============================================================================

app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    version: '14.0.0-Deep',
    deepMetaCognitive: 'active',
    components: {
      deepConsciousness: 'active',
      wisdomEngine: 'active',
      decisionOptimizer: 'active',
      deepThinking: 'active'
    }
  });
});

// ============================================================================
// DEEP META-COGNITIVE STATUS ENDPOINTS
// ============================================================================

app.get('/api/v14/deep/status', async (req: Request, res: Response) => {
  try {
    const summary = await deepRuntime.getSummary();
    res.json(summary);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get deep meta-cognitive status' });
  }
});

app.get('/api/v14/deep/state', async (req: Request, res: Response) => {
  try {
    const state = await deepRuntime.performComprehensiveAssessment();
    res.json(state);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get deep meta-cognitive state' });
  }
});

// ============================================================================
// DEEP CONSCIOUSNESS ENDPOINTS
// ============================================================================

app.get('/api/v14/deep/consciousness/assessment', async (req: Request, res: Response) => {
  try {
    const assessment = deepRuntime.getDeepConsciousness().getCurrentAssessment();
    res.json(assessment);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get consciousness assessment' });
  }
});

app.get('/api/v14/deep/consciousness/history', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const history = deepRuntime.getDeepConsciousness().getAssessmentHistory(limit);
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get consciousness history' });
  }
});

app.get('/api/v14/deep/consciousness/transcendence-events', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const events = deepRuntime.getDeepConsciousness().getTranscendenceEvents(limit);
    res.json(events);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get transcendence events' });
  }
});

app.get('/api/v14/deep/consciousness/evolution-pathways', (req: Request, res: Response) => {
  try {
    const currentStage = req.query.stage as string || 'emerging';
    const pathways = deepRuntime.getDeepConsciousness().getEvolutionPathways(currentStage);
    res.json({ stage: currentStage, pathways });
  } catch (error) {
    res.status(500).json({ error: 'Failed to get evolution pathways' });
  }
});

// ============================================================================
// WISDOM ENGINE ENDPOINTS
// ============================================================================

app.get('/api/v14/deep/wisdom/state', (req: Request, res: Response) => {
  try {
    const stats = deepRuntime.getWisdomEngine().getStatistics();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get wisdom state' });
  }
});

app.get('/api/v14/deep/wisdom/query', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const category = req.query.category as string;
    const minMaturity = req.query.minMaturity ? parseFloat(req.query.minMaturity as string) : undefined;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const wisdom = deepRuntime.getWisdomEngine().queryWisdom({
      type: type as any,
      category: category as any,
      minMaturity,
      limit
    });
    
    res.json(wisdom);
  } catch (error) {
    res.status(500).json({ error: 'Failed to query wisdom' });
  }
});

app.get('/api/v14/deep/wisdom/taxonomy', (req: Request, res: Response) => {
  try {
    const taxonomy = deepRuntime.getWisdomEngine().getTaxonomy();
    res.json(taxonomy);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get wisdom taxonomy' });
  }
});

// ============================================================================
// DECISION OPTIMIZER ENDPOINTS
// ============================================================================

app.get('/api/v14/deep/decisions/state', (req: Request, res: Response) => {
  try {
    const stats = deepRuntime.getDecisionOptimizer().getStatistics();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get decision state' });
  }
});

app.get('/api/v14/deep/decisions/history', (req: Request, res: Response) => {
  try {
    const type = req.query.type as string;
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    
    const history = deepRuntime.getDecisionOptimizer().getDecisionHistory({
      type: type as any,
      limit
    });
    
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get decision history' });
  }
});

app.get('/api/v14/deep/decisions/patterns', (req: Request, res: Response) => {
  try {
    const patterns = deepRuntime.getDecisionOptimizer().getDecisionPatterns();
    res.json(Object.fromEntries(patterns));
  } catch (error) {
    res.status(500).json({ error: 'Failed to get decision patterns' });
  }
});

// ============================================================================
// DEEP THINKING ENDPOINTS
// ============================================================================

app.get('/api/v14/deep/thinking/state', (req: Request, res: Response) => {
  try {
    const stats = deepRuntime.getDeepThinking().getStatistics();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get thinking state' });
  }
});

app.get('/api/v14/deep/thinking/history', (req: Request, res: Response) => {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit as string) : undefined;
    const history = deepRuntime.getDeepThinking().getThinkingHistory(limit);
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get thinking history' });
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
  deepRuntime.initialize().then(() => {
    app.listen(PORT, () => {
      console.log(`🌌 GL Deep Meta-Cognitive Runtime v14.0.0-Deep`);
      console.log(`🚀 Server running on port ${PORT}`);
      console.log(`🧠 Deep Meta-Cognitive capabilities active`);
      console.log(`📊 Status: http://localhost:${PORT}/health`);
      console.log(`📈 Summary: http://localhost:${PORT}/api/v14/deep/status`);
    });
  }).catch(error => {
    console.error('Failed to initialize Deep Meta-Cognitive Runtime:', error);
    process.exit(1);
  });
}

export default app;