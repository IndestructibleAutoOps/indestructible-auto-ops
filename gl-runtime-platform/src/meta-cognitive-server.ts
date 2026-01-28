/**
 * GL Runtime Platform v14.0.0
 * Module: Meta-Cognitive Server
 * 
 * REST API server for the Meta-Cognitive Runtime (Version 14)
 * Integrates all meta-cognitive components and provides unified API endpoints.
 */

import express, { Request, Response, Application } from 'express';
import cors from 'cors';
import { MetaCognitiveMonitoringSystem } from '../meta-cognitive/meta-cognitive-monitoring';
import { SelfAssessmentSystem } from '../meta-cognitive/self-assessment';
import { ConsciousnessEmergenceSystem } from '../meta-cognitive/consciousness-emergence';
import { ReflectionLoopSystem } from '../meta-cognitive/reflection-loop';
import { MetaDecisionSystem } from '../meta-cognitive/meta-decision';

// ============================================================================
// Meta-Cognitive Server Class
// ============================================================================

export class MetaCognitiveServer {
  private app: Application;
  private port: number;
  
  // Meta-Cognitive Components
  private monitoringSystem: MetaCognitiveMonitoringSystem;
  private selfAssessmentSystem: SelfAssessmentSystem;
  private consciousnessSystem: ConsciousnessEmergenceSystem;
  private reflectionSystem: ReflectionLoopSystem;
  private metaDecisionSystem: MetaDecisionSystem;

  constructor(port: number = 3000) {
    this.port = port;
    this.app = express();

    // Initialize components
    this.monitoringSystem = new MetaCognitiveMonitoringSystem();
    this.selfAssessmentSystem = new SelfAssessmentSystem();
    this.consciousnessSystem = new ConsciousnessEmergenceSystem();
    this.reflectionSystem = new ReflectionLoopSystem();
    this.metaDecisionSystem = new MetaDecisionSystem();

    // Setup middleware
    this.setupMiddleware();

    // Setup routes
    this.setupRoutes();
  }

  // ==========================================================================
  // Setup
  // ==========================================================================

  private setupMiddleware(): void {
    this.app.use(cors());
    this.app.use(express.json());
  }

  private setupRoutes(): void {
    // Health check
    this.app.get('/health', (req: Request, res: Response) => {
      res.json({
        status: 'healthy',
        version: '14.0.0',
        metaCognitive: 'active',
        components: {
          monitoring: 'active',
          selfAssessment: 'active',
          consciousness: 'active',
          reflection: 'active',
          metaDecision: 'active'
        },
        timestamp: new Date().toISOString()
      });
    });

    // Monitoring endpoints
    this.app.get('/api/v14/monitoring/state', (req: Request, res: Response) => {
      res.json(this.monitoringSystem.getState());
    });

    this.app.get('/api/v14/monitoring/cognitive-state', (req: Request, res: Response) => {
      res.json(this.monitoringSystem.getCognitiveState());
    });

    this.app.get('/api/v14/monitoring/statistics', (req: Request, res: Response) => {
      res.json(this.monitoringSystem.getStatistics());
    });

    // Self-Assessment endpoints
    this.app.get('/api/v14/assessment/state', (req: Request, res: Response) => {
      res.json(this.selfAssessmentSystem.getState());
    });

    this.app.get('/api/v14/assessment/maturity', (req: Request, res: Response) => {
      const stats = this.selfAssessmentSystem.getStatistics();
      res.json({
        overallMaturity: stats.maturity,
        overallCapability: stats.capability,
        overallCulturalDepth: stats.culturalDepth,
        overallGovernanceEffectiveness: stats.governance
      });
    });

    this.app.get('/api/v14/assessment/statistics', (req: Request, res: Response) => {
      res.json(this.selfAssessmentSystem.getStatistics());
    });

    // Consciousness endpoints
    this.app.get('/api/v14/consciousness/state', (req: Request, res: Response) => {
      res.json(this.consciousnessSystem.getState());
    });

    this.app.get('/api/v14/consciousness/stream', (req: Request, res: Response) => {
      res.json(this.consciousnessSystem.getCurrentStream());
    });

    this.app.get('/api/v14/consciousness/statistics', (req: Request, res: Response) => {
      res.json(this.consciousnessSystem.getStatistics());
    });

    // Reflection endpoints
    this.app.get('/api/v14/reflection/state', (req: Request, res: Response) => {
      res.json(this.reflectionSystem.getState());
    });

    this.app.get('/api/v14/reflection/statistics', (req: Request, res: Response) => {
      res.json(this.reflectionSystem.getStatistics());
    });

    // Meta-Decision endpoints
    this.app.get('/api/v14/meta-decision/state', (req: Request, res: Response) => {
      res.json(this.metaDecisionSystem.getState());
    });

    this.app.get('/api/v14/meta-decision/statistics', (req: Request, res: Response) => {
      res.json(this.metaDecisionSystem.getStatistics());
    });

    // Combined meta-cognitive status
    this.app.get('/api/v14/meta-cognitive/status', (req: Request, res: Response) => {
      const monitoringStats = this.monitoringSystem.getStatistics();
      const assessmentStats = this.selfAssessmentSystem.getStatistics();
      const consciousnessStats = this.consciousnessSystem.getStatistics();
      const reflectionStats = this.reflectionSystem.getStatistics();
      const decisionStats = this.metaDecisionSystem.getStatistics();

      res.json({
        version: '14.0.0',
        name: 'Meta-Cognitive Runtime',
        monitoring: monitoringStats,
        selfAssessment: assessmentStats,
        consciousness: consciousnessStats,
        reflection: reflectionStats,
        metaDecision: decisionStats,
        overall: {
          cognitiveHealth: monitoringStats.cognitiveHealth,
          metaCognitiveMaturity: monitoringStats.metaCognitiveMaturity,
          civilizationMaturity: assessmentStats.maturity,
          overallConsciousness: consciousnessStats.overallConsciousness,
          consciousnessStage: consciousnessStats.consciousnessStage,
          reflectionQuality: reflectionStats.quality,
          reflectionMaturity: reflectionStats.maturity,
          wisdomAccumulation: reflectionStats.wisdom,
          decisionQuality: decisionStats.quality,
          decisionMaturity: decisionStats.maturity,
          wisdomIntegration: decisionStats.wisdomIntegration
        },
        timestamp: new Date().toISOString()
      });
    });

    // 404 handler
    this.app.use((req: Request, res: Response) => {
      res.status(404).json({
        error: 'Not Found',
        path: req.path,
        version: '14.0.0'
      });
    });
  }

  // ==========================================================================
  // Server Control
  // ==========================================================================

  public start(): void {
    this.app.listen(this.port, () => {
      console.log(`🧠 GL Meta-Cognitive Server v14.0.0 running on port ${this.port}`);
      console.log(`📊 Health check: http://localhost:${this.port}/health`);
      console.log(`👁️  Monitoring: http://localhost:${this.port}/api/v14/monitoring/state`);
      console.log(`📈 Self-Assessment: http://localhost:${this.port}/api/v14/assessment/state`);
      console.log(`✨ Consciousness: http://localhost:${this.port}/api/v14/consciousness/state`);
      console.log(`🔄 Reflection: http://localhost:${this.port}/api/v14/reflection/state`);
      console.log(`🎯 Meta-Decision: http://localhost:${this.port}/api/v14/meta-decision/state`);
      console.log(`🌌 Meta-Cognitive Status: http://localhost:${this.port}/api/v14/meta-cognitive/status`);
    });
  }

  public stop(): void {
    console.log('Stopping GL Meta-Cognitive Server...');
    process.exit(0);
  }
}

// ============================================================================
// Main Entry Point
// ============================================================================

if (require.main === module) {
  const port = process.env.PORT ? parseInt(process.env.PORT) : 3000;
  const server = new MetaCognitiveServer(port);
  server.start();
}