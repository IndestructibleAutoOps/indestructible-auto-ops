/**
 * GL Runtime Platform v13.0.0
 * Module: Civilization Server
 * 
 * REST API server for the Autonomous Civilization Layer (Version 13)
 * Integrates all civilization components and provides unified API endpoints.
 */

import express, { Request, Response, Application } from 'express';
import cors from 'cors';
import { GovernanceSystem } from '../civilization/governance-system';
import { CulturalEngine } from '../civilization/cultural-engine';
import { RoleSpecializationSystem } from '../civilization/role-specialization';
import { EcosystemEngine } from '../civilization/ecosystem-engine';
import { SustainabilityEngine } from '../civilization/sustainability-engine';
import { CivilizationMemory } from '../civilization/civilization-memory';
import { ExpansionEngine } from '../civilization/expansion-engine';

// ============================================================================
// Civilization Server Class
// ============================================================================

export class CivilizationServer {
  private app: Application;
  private port: number;
  
  // Civilization Components
  private governanceSystem: GovernanceSystem;
  private culturalEngine: CulturalEngine;
  private roleSpecialization: RoleSpecializationSystem;
  private ecosystemEngine: EcosystemEngine;
  private sustainabilityEngine: SustainabilityEngine;
  private civilizationMemory: CivilizationMemory;
  private expansionEngine: ExpansionEngine;

  constructor(port: number = 3000) {
    this.port = port;
    this.app = express();

    // Initialize components
    this.governanceSystem = new GovernanceSystem();
    this.culturalEngine = new CulturalEngine();
    this.roleSpecialization = new RoleSpecializationSystem();
    this.ecosystemEngine = new EcosystemEngine();
    this.sustainabilityEngine = new SustainabilityEngine();
    this.civilizationMemory = new CivilizationMemory();
    this.expansionEngine = new ExpansionEngine();

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
        version: '13.0.0',
        civilization: 'active',
        components: {
          governance: 'active',
          cultural: 'active',
          specialization: 'active',
          ecosystem: 'active',
          sustainability: 'active',
          memory: 'active',
          expansion: 'active'
        },
        timestamp: new Date().toISOString()
      });
    });

    // Governance endpoints
    this.app.get('/api/v13/governance/state', (req: Request, res: Response) => {
      res.json(this.governanceSystem.getState());
    });

    this.app.get('/api/v13/governance/laws', (req: Request, res: Response) => {
      res.json({ laws: this.governanceSystem.getLaws() });
    });

    this.app.get('/api/v13/governance/norms', (req: Request, res: Response) => {
      res.json({ norms: this.governanceSystem.getNorms() });
    });

    this.app.get('/api/v13/governance/roles', (req: Request, res: Response) => {
      res.json({ roles: this.governanceSystem.getRoles() });
    });

    this.app.get('/api/v13/governance/institutions', (req: Request, res: Response) => {
      res.json({ institutions: this.governanceSystem.getInstitutions() });
    });

    this.app.get('/api/v13/governance/events', (req: Request, res: Response) => {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : 50;
      res.json({ events: this.governanceSystem.getEvents(limit) });
    });

    this.app.get('/api/v13/governance/statistics', (req: Request, res: Response) => {
      res.json(this.governanceSystem.getStatistics());
    });

    // Cultural endpoints
    this.app.get('/api/v13/cultural/state', (req: Request, res: Response) => {
      res.json(this.culturalEngine.getState());
    });

    this.app.get('/api/v13/cultural/values', (req: Request, res: Response) => {
      res.json({ values: this.culturalEngine.getValues() });
    });

    this.app.get('/api/v13/cultural/strategies', (req: Request, res: Response) => {
      res.json({ strategies: this.culturalEngine.getStrategies() });
    });

    this.app.get('/api/v13/cultural/semantics', (req: Request, res: Response) => {
      res.json({ semantics: this.culturalEngine.getSemantics() });
    });

    this.app.get('/api/v13/cultural/behaviors', (req: Request, res: Response) => {
      res.json({ behaviorPatterns: this.culturalEngine.getBehaviorPatterns() });
    });

    this.app.get('/api/v13/cultural/philosophies', (req: Request, res: Response) => {
      res.json({ repairPhilosophies: this.culturalEngine.getRepairPhilosophies() });
    });

    this.app.get('/api/v13/cultural/shifts', (req: Request, res: Response) => {
      res.json({ culturalShifts: this.culturalEngine.getCulturalShifts() });
    });

    this.app.get('/api/v13/cultural/statistics', (req: Request, res: Response) => {
      res.json(this.culturalEngine.getStatistics());
    });

    // Role specialization endpoints
    this.app.get('/api/v13/specialization/state', (req: Request, res: Response) => {
      res.json(this.roleSpecialization.getState());
    });

    this.app.get('/api/v13/specialization/roles', (req: Request, res: Response) => {
      res.json({ roles: this.roleSpecialization.getRoles() });
    });

    this.app.get('/api/v13/specialization/species', (req: Request, res: Response) => {
      res.json({ species: this.roleSpecialization.getSpecies() });
    });

    this.app.get('/api/v13/specialization/capabilities', (req: Request, res: Response) => {
      res.json({ capabilities: this.roleSpecialization.getCapabilities() });
    });

    this.app.get('/api/v13/specialization/statistics', (req: Request, res: Response) => {
      res.json(this.roleSpecialization.getStatistics());
    });

    // Ecosystem endpoints
    this.app.get('/api/v13/ecosystem/state', (req: Request, res: Response) => {
      res.json(this.ecosystemEngine.getState());
    });

    this.app.get('/api/v13/ecosystem/roles', (req: Request, res: Response) => {
      res.json({ roles: this.ecosystemEngine.getRoles() });
    });

    this.app.get('/api/v13/ecosystem/resources', (req: Request, res: Response) => {
      res.json({ resources: this.ecosystemEngine.getResources() });
    });

    this.app.get('/api/v13/ecosystem/relationships', (req: Request, res: Response) => {
      res.json({ relationships: this.ecosystemEngine.getRelationships() });
    });

    this.app.get('/api/v13/ecosystem/events', (req: Request, res: Response) => {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : 50;
      res.json({ events: this.ecosystemEngine.getEvents(limit) });
    });

    this.app.get('/api/v13/ecosystem/statistics', (req: Request, res: Response) => {
      res.json(this.ecosystemEngine.getStatistics());
    });

    // Sustainability endpoints
    this.app.get('/api/v13/sustainability/state', (req: Request, res: Response) => {
      res.json(this.sustainabilityEngine.getState());
    });

    this.app.get('/api/v13/sustainability/repairs', (req: Request, res: Response) => {
      res.json({ repairActions: this.sustainabilityEngine.getRepairActions() });
    });

    this.app.get('/api/v13/sustainability/optimizations', (req: Request, res: Response) => {
      res.json({ optimizationActions: this.sustainabilityEngine.getOptimizationActions() });
    });

    this.app.get('/api/v13/sustainability/evolutions', (req: Request, res: Response) => {
      res.json({ evolutionTriggers: this.sustainabilityEngine.getEvolutionTriggers() });
    });

    this.app.get('/api/v13/sustainability/governance', (req: Request, res: Response) => {
      res.json({ governanceActions: this.sustainabilityEngine.getGovernanceActions() });
    });

    this.app.get('/api/v13/sustainability/expansions', (req: Request, res: Response) => {
      res.json({ expansionActions: this.sustainabilityEngine.getExpansionActions() });
    });

    this.app.get('/api/v13/sustainability/events', (req: Request, res: Response) => {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : 50;
      res.json({ events: this.sustainabilityEngine.getEvents(limit) });
    });

    this.app.get('/api/v13/sustainability/statistics', (req: Request, res: Response) => {
      res.json(this.sustainabilityEngine.getStatistics());
    });

    // Memory endpoints
    this.app.get('/api/v13/memory/state', (req: Request, res: Response) => {
      res.json(this.civilizationMemory.getState());
    });

    this.app.get('/api/v13/memory/strategic', (req: Request, res: Response) => {
      res.json({ strategicMemories: this.civilizationMemory.getStrategicMemories() });
    });

    this.app.get('/api/v13/memory/normative', (req: Request, res: Response) => {
      res.json({ normativeMemories: this.civilizationMemory.getNormativeMemories() });
    });

    this.app.get('/api/v13/memory/cultural', (req: Request, res: Response) => {
      res.json({ culturalMemories: this.civilizationMemory.getCulturalMemories() });
    });

    this.app.get('/api/v13/memory/evolutionary', (req: Request, res: Response) => {
      res.json({ evolutionaryMemories: this.civilizationMemory.getEvolutionaryMemories() });
    });

    this.app.get('/api/v13/memory/historical', (req: Request, res: Response) => {
      res.json({ historicalEvents: this.civilizationMemory.getHistoricalEvents() });
    });

    this.app.get('/api/v13/memory/wisdom', (req: Request, res: Response) => {
      res.json({ wisdomSyntheses: this.civilizationMemory.getWisdomSyntheses() });
    });

    this.app.get('/api/v13/memory/statistics', (req: Request, res: Response) => {
      res.json(this.civilizationMemory.getStatistics());
    });

    // Expansion endpoints
    this.app.get('/api/v13/expansion/state', (req: Request, res: Response) => {
      res.json(this.expansionEngine.getState());
    });

    this.app.get('/api/v13/expansion/targets', (req: Request, res: Response) => {
      res.json({ targets: this.expansionEngine.getTargets() });
    });

    this.app.get('/api/v13/expansion/campaigns', (req: Request, res: Response) => {
      res.json({ campaigns: this.expansionEngine.getCampaigns() });
    });

    this.app.get('/api/v13/expansion/strategies', (req: Request, res: Response) => {
      res.json({ strategies: this.expansionEngine.getStrategies() });
    });

    this.app.get('/api/v13/expansion/metrics', (req: Request, res: Response) => {
      res.json({ metrics: this.expansionEngine.getMetrics() });
    });

    this.app.get('/api/v13/expansion/events', (req: Request, res: Response) => {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : 50;
      res.json({ events: this.expansionEngine.getEvents(limit) });
    });

    this.app.get('/api/v13/expansion/statistics', (req: Request, res: Response) => {
      res.json(this.expansionEngine.getStatistics());
    });

    // Combined civilization status
    this.app.get('/api/v13/civilization/status', (req: Request, res: Response) => {
      res.json({
        version: '13.0.0',
        name: 'Autonomous Civilization Layer',
        governance: this.governanceSystem.getStatistics(),
        cultural: this.culturalEngine.getStatistics(),
        specialization: this.roleSpecialization.getStatistics(),
        ecosystem: this.ecosystemEngine.getStatistics(),
        sustainability: this.sustainabilityEngine.getStatistics(),
        memory: this.civilizationMemory.getStatistics(),
        expansion: this.expansionEngine.getStatistics(),
        overall: {
          health: this.ecosystemEngine.getState().health.overall,
          cohesion: this.governanceSystem.getState().cultureScore,
          sustainability: this.sustainabilityEngine.getState().metrics.overallHealth,
          expansionSuccess: this.expansionEngine.getStatistics().overallSuccess
        },
        timestamp: new Date().toISOString()
      });
    });

    // 404 handler
    this.app.use((req: Request, res: Response) => {
      res.status(404).json({
        error: 'Not Found',
        path: req.path,
        version: '13.0.0'
      });
    });
  }

  // ==========================================================================
  // Server Control
  // ==========================================================================

  public start(): void {
    this.app.listen(this.port, () => {
      console.log(`🌌 GL Civilization Server v13.0.0 running on port ${this.port}`);
      console.log(`📊 Health check: http://localhost:${this.port}/health`);
      console.log(`🏛️  Governance: http://localhost:${this.port}/api/v13/governance/state`);
      console.log(`🎭 Cultural: http://localhost:${this.port}/api/v13/cultural/state`);
      console.log(`👥 Specialization: http://localhost:${this.port}/api/v13/specialization/state`);
      console.log(`🌿 Ecosystem: http://localhost:${this.port}/api/v13/ecosystem/state`);
      console.log(`🔄 Sustainability: http://localhost:${this.port}/api/v13/sustainability/state`);
      console.log(`📜 Memory: http://localhost:${this.port}/api/v13/memory/state`);
      console.log(`🌍 Expansion: http://localhost:${this.port}/api/v13/expansion/state`);
      console.log(`🌌 Civilization Status: http://localhost:${this.port}/api/v13/civilization/status`);
    });
  }

  public stop(): void {
    console.log('Stopping GL Civilization Server...');
    process.exit(0);
  }
}

// ============================================================================
// Main Entry Point
// ============================================================================

if (require.main === module) {
  const port = process.env.PORT ? parseInt(process.env.PORT) : 3000;
  const server = new CivilizationServer(port);
  server.start();
}