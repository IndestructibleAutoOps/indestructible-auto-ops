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
 * GL Universal Intelligence Server (Version 15.0.0)
 * 通用智慧層 API 伺服器
 * 
 * 提供完整的通用智慧能力 API
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import { UniversalIntelligenceSystem } from '../universal-intelligence';

// ============================================================================
// Express Application
// ============================================================================

const app = express();
const PORT = process.env.UNIVERSAL_INTELLIGENCE_PORT || 3007;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Universal Intelligence System
const uiSystem = new UniversalIntelligenceSystem();

// ============================================================================
// Health Check
// ============================================================================

app.get('/health', (req: Request, res: Response) => {
  const status = uiSystem.getStatus();
  res.json({
    status: 'healthy',
    version: '15.0.0',
    universalIntelligence: 'active',
    uptime: status.uptime,
    initialized: status.initialized,
    engines: status.engineStatus
  });
});

// ============================================================================
// System Status
// ============================================================================

app.get('/api/v15/status', (req: Request, res: Response) => {
  const status = uiSystem.getStatus();
  const statistics = uiSystem.getStatistics();
  const intelligenceLevel = uiSystem.getIntelligenceLevel();

  res.json({
    version: '15.0.0',
    status,
    statistics,
    intelligenceLevel,
    timestamp: new Date()
  });
});

// ============================================================================
// Demonstration Endpoint
// ============================================================================

app.get('/api/v15/demonstrate', async (req: Request, res: Response) => {
  try {
    const result = await uiSystem.demonstrateIntelligence();
    res.json({ success: true, result });
  } catch (error: any) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// ============================================================================
// Start Server
// ============================================================================

async function startServer() {
  try {
    await uiSystem.initialize();
    console.log('✅ Universal Intelligence System initialized');

    app.listen(PORT, () => {
      console.log(`🌌 GL Universal Intelligence Server v15.0.0 running on port ${PORT}`);
      console.log(`📊 Health check: http://localhost:${PORT}/health`);
      console.log(`📈 Status: http://localhost:${PORT}/api/v15/status`);
      console.log(`🎯 Demonstration: http://localhost:${PORT}/api/v15/demonstrate`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  startServer();
}

export { app, uiSystem };
