// @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: resource-graph-manager
# @GL-charter-version: 2.0.0

import { ResourceGraphScanner } from './scanners/scanner';
import { ResourceGraphIndexer } from './indexers/indexer';
import { ResourceGraphModel } from './graph-model/graph-model';
import { ResourceGraphResolver } from './resolvers/resolver';
import { GraphData } from './graph-model/graph-model';
import { EventStreamManager } from '../src/events/event-stream-manager';
import { ArtifactStore } from '../src/storage/artifact-store';
import { createLogger } from '../src/utils/logger';

const logger = createLogger('ResourceGraphManager');

export interface GlobalResourceGraph {
  version: string;
  timestamp: string;
  nodes: any[];
  edges: any[];
  statistics: any;
  resolutions: any;
}

export class ResourceGraphManager {
  private scanner: ResourceGraphScanner;
  private indexer: ResourceGraphIndexer;
  private graphModel: ResourceGraphModel;
  private resolver: ResourceGraphResolver;
  private eventStream: EventStreamManager;
  private artifactStore: ArtifactStore;

  constructor() {
    this.scanner = new ResourceGraphScanner();
    this.indexer = new ResourceGraphIndexer();
    this.graphModel = new ResourceGraphModel();
    this.eventStream = new EventStreamManager();
    this.artifactStore = new ArtifactStore();
    
    // Initialize resolver after graph is built
    this.resolver = new ResourceGraphResolver(
      { nodes: [], edges: [] },
      new Map()
    );
  }

  public async buildGlobalResourceGraph(rootPath: string): Promise<GlobalResourceGraph> {
    logger.info(`Building Global Resource Graph for: ${rootPath}`);
    
    // Log governance event
    await this.eventStream.logEvent({
      eventType: 'grg_build_started',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        rootPath,
        version: '6.0.0'
      }
    });

    // Step 1: Scan repository
    const scanResults = await this.scanner.scanRepository(rootPath);
    logger.info(`Scanned ${scanResults.length} files`);

    // Step 2: Build index
    this.indexer.buildIndex(scanResults);
    logger.info(`Index built: ${this.indexer.getIndexSize()} entries`);

    // Step 3: Build graph model
    this.graphModel.buildGraph(this.indexer['pathIndex']);
    logger.info(`Graph built: ${this.graphModel.getStatistics().nodeCount} nodes`);

    // Step 4: Initialize resolver
    this.resolver = new ResourceGraphResolver(
      this.graphModel.exportGraph(),
      this.indexer['pathIndex']
    );

    // Step 5: Run resolutions
    const resolutions = this.resolver.exportResolutions();
    logger.info(`Resolutions: ${JSON.stringify(resolutions)}`);

    // Step 6: Build Global Resource Graph artifact
    const grg: GlobalResourceGraph = {
      version: '6.0.0',
      timestamp: new Date().toISOString(),
      nodes: this.graphModel.getNodes(),
      edges: this.graphModel.getEdges(),
      statistics: this.graphModel.getStatistics(),
      resolutions: resolutions
    };

    // Step 7: Store artifact
    await this.artifactStore.storeArtifact({
      id: `global-resource-graph-${Date.now()}`,
      type: 'metadata',
      name: 'global-resource-graph',
      content: grg,
      timestamp: new Date().toISOString(),
      metadata: {
        version: '6.0.0',
        rootPath,
        charterVersion: '2.0.0'
      }
    });

    // Log governance event
    await this.eventStream.logEvent({
      eventType: 'grg_build_completed',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        version: '6.0.0',
        nodeCount: grg.nodes.length,
        edgeCount: grg.edges.length,
        missingDependencies: resolutions.missingDependencies.length,
        nonCompliantFiles: resolutions.nonCompliantFiles.length
      }
    });

    logger.info(`Global Resource Graph built successfully`);
    return grg;
  }

  public getScanner(): ResourceGraphScanner {
    return this.scanner;
  }

  public getIndexer(): ResourceGraphIndexer {
    return this.indexer;
  }

  public getGraphModel(): ResourceGraphModel {
    return this.graphModel;
  }

  public getResolver(): ResourceGraphResolver {
    return this.resolver;
  }

  public async loadGlobalResourceGraph(artifactId: string): Promise<GlobalResourceGraph | null> {
    const artifact = await this.artifactStore.loadArtifact(artifactId);
    
    if (artifact && artifact.type === 'metadata') {
      const grg = artifact.content as GlobalResourceGraph;
      
      // Rebuild graph model from loaded data
      this.graphModel.importGraph({
        nodes: grg.nodes,
        edges: grg.edges
      });
      
      // Update resolver
      this.resolver = new ResourceGraphResolver(
        this.graphModel.exportGraph(),
        new Map()
      );
      
      logger.info(`Global Resource Graph loaded: ${grg.nodes.length} nodes`);
      return grg;
    }
    
    return null;
  }

  public async checkGraphFreshness(rootPath: string): Promise<boolean> {
    // Check if the graph is up to date
    // In production, would compare file timestamps
    const lastModified = new Date();
    // Simplified check - always return false for now
    return false;
  }
}