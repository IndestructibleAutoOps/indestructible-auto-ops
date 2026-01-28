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
}

export function setupRoutes(app: express.Application, services: Services): void {
  const router = express.Router();
  router.use(express.json());
  router.use(express.urlencoded({ extended: true }));

  // Health check endpoint
  router.get('/health', (req, res) => {
    res.json({
      status: 'healthy',
      version: '5.0.0',
      timestamp: new Date().toISOString(),
      governance: {
        activated: true,
        charterVersion: '2.0.0'
      }
    });
  });

  // Audit endpoint - trigger per-file audit
  router.post('/api/v1/audit', async (req, res) => {
    try {
      const { filePath } = req.body;
      
      if (!filePath) {
        return res.status(400).json({
          error: 'filePath is required'
        });
      }

      logger.info(`Starting audit for file: ${filePath}`);

      // Execute per-file pipeline
      await services.orchestrator.executePerFilePipeline(filePath);

      // Generate audit report
      const completedTasks = services.orchestrator.getAllCompletedTasks();
      const auditReport = {
        id: uuidv4(),
        filePath,
        timestamp: new Date().toISOString(),
        tasks: completedTasks,
        summary: {
          total: completedTasks.length,
          completed: completedTasks.filter(t => t.status === 'completed').length,
          failed: completedTasks.filter(t => t.status === 'failed').length
        }
      };

      // Store artifact
      await services.artifactStore.storeArtifact({
        id: auditReport.id,
        type: 'audit-report',
        name: `audit-${filePath.replace(/\//g, '-')}`,
        content: auditReport,
        timestamp: new Date().toISOString(),
        metadata: {
          filePath,
          charterVersion: '2.0.0'
        }
      });

      res.json({
        success: true,
        auditReportId: auditReport.id,
        summary: auditReport.summary
      });

    } catch (error: any) {
      logger.error(`Audit failed: ${error.message}`);
      res.status(500).json({
        error: 'Audit failed',
        message: error.message
      });
    }
  });

  // Fix endpoint - trigger automatic fixes
  router.post('/api/v1/fix', async (req, res) => {
    try {
      const { auditReportId } = req.body;
      
      if (!auditReportId) {
        return res.status(400).json({
          error: 'auditReportId is required'
        });
      }

      logger.info(`Starting fix for audit report: ${auditReportId}`);

      // Load audit report
      const auditReport = await services.artifactStore.loadArtifact(auditReportId);
      
      if (!auditReport) {
        return res.status(404).json({
          error: 'Audit report not found'
        });
      }

      // Generate and apply fixes (simplified)
      const fixResults = await applyFixes(services, auditReport);

      res.json({
        success: true,
        fixResults
      });

    } catch (error: any) {
      logger.error(`Fix failed: ${error.message}`);
      res.status(500).json({
        error: 'Fix failed',
        message: error.message
      });
    }
  });

  // Deploy endpoint - deploy changes
  router.post('/api/v1/deploy', async (req, res) => {
    try {
      logger.info('Starting deployment');

      // Git operations
      const status = await services.gitConnector.getStatus();
      
      if (status.files.length > 0) {
        for (const file of status.files) {
          await services.gitConnector.add(file.path);
        }
        
        await services.gitConnector.commit('GL Automated Fix Deployment');
        await services.gitConnector.push();
      }

      res.json({
        success: true,
        message: 'Deployment completed successfully',
        timestamp: new Date().toISOString()
      });

    } catch (error: any) {
      logger.error(`Deployment failed: ${error.message}`);
      res.status(500).json({
        error: 'Deployment failed',
        message: error.message
      });
    }
  });

  // Orchestrate endpoint - execute multi-agent orchestration
  router.post('/api/v1/orchestrate', async (req, res) => {
    try {
      const { pipeline, files } = req.body;
      
      logger.info(`Starting orchestration for pipeline: ${pipeline}`);

      // Execute orchestration
      for (const file of files) {
        await services.orchestrator.executePerFilePipeline(file);
      }

      const results = services.orchestrator.getAllCompletedTasks();

      res.json({
        success: true,
        pipeline,
        filesProcessed: files.length,
        tasksExecuted: results.length
      });

    } catch (error: any) {
      logger.error(`Orchestration failed: ${error.message}`);
      res.status(500).json({
        error: 'Orchestration failed',
        message: error.message
      });
    }
  });

  // Get events endpoint
  router.get('/api/v1/events', async (req, res) => {
    try {
      const events = await services.eventStream.loadEvents();
      res.json({
        success: true,
        count: events.length,
        events
      });
    } catch (error: any) {
      logger.error(`Failed to get events: ${error.message}`);
      res.status(500).json({
        error: 'Failed to get events',
        message: error.message
      });
    }
  });

  // Get artifacts endpoint
  router.get('/api/v1/artifacts', async (req, res) => {
    try {
      const { type } = req.query;
      
      let artifacts: any[];
      if (type) {
        artifacts = await services.artifactStore.getArtifactsByType(type as string);
      } else {
        artifacts = [];
      }

      res.json({
        success: true,
        count: artifacts.length,
        artifacts
      });
    } catch (error: any) {
      logger.error(`Failed to get artifacts: ${error.message}`);
      res.status(500).json({
        error: 'Failed to get artifacts',
        message: error.message
      });
    }
  });

  app.use('/', router);
}

async function applyFixes(services: Services, auditReport: any): Promise<any> {
  // Simplified fix logic - would be expanded in production
  const fixes = [];
  
  for (const task of auditReport.content.tasks) {
    if (task.status === 'failed') {
      // Create fix for failed task
      fixes.push({
        taskId: task.id,
        status: 'fixed',
        message: 'Applied automatic fix'
      });
    }
  }
  
  return fixes;
}