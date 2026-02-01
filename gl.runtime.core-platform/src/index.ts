// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: platform-entry-point
// @GL-charter-version: 2.0.0

import express from 'express';
import { OrchestratorEngine } from './orchestration/orchestrator-engine';
import { PolicyEngine } from './policies/policy-engine';
import { EventStreamManager } from './events/event-stream-manager';
import { ArtifactStore } from './storage/artifact-store';
import { GitConnector } from './connectors/git-connector';
import { createLogger } from './utils/logger';
import { setupRoutes } from './api/routes';

const logger = createLogger('GL-Runtime-Platform');

export class GLRuntimePlatform {
  private app: express.Application;
  private orchestrator: OrchestratorEngine;
  private policyEngine: PolicyEngine;
  private eventStream: EventStreamManager;
  private artifactStore: ArtifactStore;
  private gitConnector: GitConnector;
  private srgRuntime: any;

  constructor() {
    this.app = express();
    this.orchestrator = new OrchestratorEngine();
    this.policyEngine = new PolicyEngine();
    this.eventStream = new EventStreamManager();
    this.artifactStore = new ArtifactStore();
    this.gitConnector = new GitConnector();
    
    // SRG will be initialized dynamically
    this.srgRuntime = null;
    
    this.initialize();
  }

  private async initialize(): Promise<void> {
    logger.info('Initializing GL Runtime Platform v7.0.0');
    
    // Log governance event
    await this.eventStream.logEvent({
      eventType: 'platform_init',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        version: '7.0.0',
        charterVersion: '2.0.0',
        semanticGraphEnabled: true
      }
    });

    // Initialize Semantic Graph Runtime dynamically
    try {
      const { SemanticGraphRuntime } = await import('./engine/semantic-graph-runtime');
      this.srgRuntime = new SemanticGraphRuntime({
        autoRefreshInterval: 300,
        storagePath: 'storage/gl-semantic-graph/',
        enabled: true
      });
      await this.srgRuntime.initialize(process.cwd());
      logger.info('Semantic Graph Runtime initialized');
    } catch (error) {
      logger.warn('Semantic Graph Runtime initialization failed:', error);
    }

    // Setup routes with SRG runtime
    setupRoutes(this.app, {
      orchestrator: this.orchestrator,
      policyEngine: this.policyEngine,
      eventStream: this.eventStream,
      artifactStore: this.artifactStore,
      gitConnector: this.gitConnector,
      srgRuntime: this.srgRuntime
    });

    logger.info('GL Runtime Platform initialized successfully');
  }

  public async start(port: number = 3000): Promise<void> {
    return new Promise((resolve) => {
      this.app.listen(port, () => {
        const srgStatus = this.srgRuntime?.getStatus() || {
          ready: false,
          totalFilesAnalyzed: 0,
          compliantFiles: 0
        };
        logger.info(`GL Runtime Platform listening on port ${port}`);
        logger.info(`Semantic Graph Runtime: ${srgStatus.ready ? 'Ready' : 'Not Ready'}`);
        logger.info(`Files analyzed: ${srgStatus.totalFilesAnalyzed}`);
        logger.info(`Compliant files: ${srgStatus.compliantFiles}`);
        resolve();
      });
    });
  }

  public getApp(): express.Application {
    return this.app;
  }

  public getSRGRuntime(): any {
    return this.srgRuntime;
  }
}

// Main entry point
async function main() {
  const platform = new GLRuntimePlatform();
  await platform.start(3000);
}

if (require.main === module) {
  main().catch((error) => {
    logger.error('Failed to start platform', error);
    process.exit(1);
  });
}

export default GLRuntimePlatform;