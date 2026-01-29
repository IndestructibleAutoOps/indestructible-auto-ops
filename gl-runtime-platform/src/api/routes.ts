// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: api-routes
// @GL-charter-version: 2.0.0

import express from 'express';
import { OrchestratorEngine } from '../orchestration/orchestrator-engine';
import { PolicyEngine } from '../policies/policy-engine';
import { EventStreamManager } from '../events/event-stream-manager';
import { ArtifactStore } from '../storage/artifact-store';
import { GitConnector } from '../connectors/git-connector';
import { createLogger } from '../utils/logger';
import { v4 as uuidv4 } from 'uuid';

const logger = createLogger('API-Routes');

export interface Services {
  orchestrator: OrchestratorEngine;
  policyEngine: PolicyEngine;
  eventStream: EventStreamManager;
  artifactStore: ArtifactStore;
  gitConnector: GitConnector;
  srgRuntime?: any;
  globalDAGRuntime?: any;
}

export function setupRoutes(app: express.Application, services: Services): void {
  const router = express.Router();
  router.use(express.json());
  router.use(express.urlencoded({ extended: true }));

  router.get('/health', (req, res) => {
    const srgStatus = services.srgRuntime?.getStatus() || {
      ready: false,
      totalFilesAnalyzed: 0,
      compliantFiles: 0,
      nonCompliantFiles: 0
    };
    
    const dagStats = services.globalDAGRuntime?.getStats?.() || {
      totalNodes: 0,
      totalEdges: 0,
      organizations: 0,
      repositories: 0,
      clusters: 0,
      pipelines: 0,
      agents: 0
    };
    
    res.json({
      status: 'healthy',
      version: '9.0.0',
      timestamp: new Date().toISOString(),
      governance: {
        activated: true,
        charterVersion: '2.0.0'
      },
      semanticGraph: {
        enabled: true,
        ready: srgStatus.ready,
        totalFilesAnalyzed: srgStatus.totalFilesAnalyzed,
        compliantFiles: srgStatus.compliantFiles,
        nonCompliantFiles: srgStatus.nonCompliantFiles
      },
      selfHealingEngine: {
        enabled: true,
        operational: true
      },
      globalDAG: {
        enabled: true,
        operational: services.globalDAGRuntime !== undefined,
        totalNodes: dagStats.totalNodes,
        totalEdges: dagStats.totalEdges,
        organizations: dagStats.organizations,
        repositories: dagStats.repositories,
        clusters: dagStats.clusters
      }
    });
  });

  router.get('/api/v9/dag/status', async (req, res) => {
    try {
      if (!services.globalDAGRuntime) {
        return res.status(503).json({ error: 'Global DAG Runtime not available' });
      }
      const stats = services.globalDAGRuntime.getStats();
      res.json({ success: true, data: stats });
    } catch (error) {
      logger.error('Failed to get DAG status', error);
      res.status(500).json({ error: 'Failed to get DAG status' });
    }
  });

  router.get('/api/v1/events', async (req, res) => {
    try {
      const events = await services.eventStream.loadEvents();
      const limit = parseInt(req.query.limit as string) || 100;
      const filteredEvents = events.slice(0, limit);
      res.json({ success: true, count: filteredEvents.length, events: filteredEvents });
    } catch (error) {
      logger.error('Failed to query events', error);
      res.status(500).json({ error: 'Failed to query events' });
    }
  });

  router.get('/api/v1/artifacts', async (req, res) => {
    try {
      const limit = parseInt(req.query.limit as string) || 100;
      const artifacts = await services.artifactStore.listArtifacts(limit);
      res.json({ success: true, count: artifacts.length, artifacts });
    } catch (error) {
      logger.error('Failed to list artifacts', error);
      res.status(500).json({ error: 'Failed to list artifacts' });
    }
  });

  app.use('/api', router);
}
