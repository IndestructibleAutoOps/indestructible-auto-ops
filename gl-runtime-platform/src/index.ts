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

  constructor() {
    this.app = express();
    this.orchestrator = new OrchestratorEngine();
    this.policyEngine = new PolicyEngine();
    this.eventStream = new EventStreamManager();
    this.artifactStore = new ArtifactStore();
    this.gitConnector = new GitConnector();
    
    this.initialize();
  }

  private async initialize(): Promise<void> {
    logger.info('Initializing GL Runtime Platform v5.0.0');
    
    // Log governance event
    await this.eventStream.logEvent({
      eventType: 'platform_init',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        version: '5.0.0',
        charterVersion: '2.0.0'
      }
    });

    // Setup routes
    setupRoutes(this.app, {
      orchestrator: this.orchestrator,
      policyEngine: this.policyEngine,
      eventStream: this.eventStream,
      artifactStore: this.artifactStore,
      gitConnector: this.gitConnector
    });

    logger.info('GL Runtime Platform initialized successfully');
  }

  public async start(port: number = 3000): Promise<void> {
    return new Promise((resolve) => {
      this.app.listen(port, () => {
        logger.info(`GL Runtime Platform listening on port ${port}`);
        resolve();
      });
    });
  }

  public getApp(): express.Application {
    return this.app;
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