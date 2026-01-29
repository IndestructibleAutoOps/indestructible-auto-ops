// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-builder
// @GL-charter-version: 2.0.0

import { GlobalDAGGraph, DAGNode, DAGEdge } from '../dag-model';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Global DAG Builder
 * Constructs the global DAG from repositories, pipelines, agents, and resources
 */

export interface DAGBuilderConfig {
  repositories: Array<{
    id: string;
    organization: string;
    path: string;
    glLayer: string;
  }>;
  pipelines: Array<{
    id: string;
    repository: string;
    organization: string;
    dependencies?: string[];
  }>;
  agents: Array<{
    id: string;
    repository: string;
    organization: string;
    priority: number;
  }>;
  clusters: Array<{
    id: string;
    region: string;
  }>;
}

export class GlobalDAGBuilder {
  private graph: GlobalDAGGraph;
  private config: DAGBuilderConfig;
  
  constructor(config: DAGBuilderConfig) {
    this.graph = new GlobalDAGGraph();
    this.config = config;
  }
  
  /**
   * Build the complete global DAG
   */
  async build(): Promise<GlobalDAGGraph> {
    console.log('🏗️  Building Global DAG...');
    
    // Build repository nodes
    await this.buildRepositoryNodes();
    
    // Build pipeline nodes
    await this.buildPipelineNodes();
    
    // Build agent nodes
    await this.buildAgentNodes();
    
    // Build file nodes
    await this.buildFileNodes();
    
    // Build semantic nodes
    await this.buildSemanticNodes();
    
    // Build cluster nodes
    await this.buildClusterNodes();
    
    // Build deployment nodes
    await this.buildDeploymentNodes();
    
    // Build edges between nodes
    await this.buildEdges();
    
    // Validate graph
    this.validateGraph();
    
    console.log('✅ Global DAG built successfully');
    return this.graph;
  }
  
  /**
   * Build repository nodes
   */
  private async buildRepositoryNodes(): Promise<void> {
    for (const repo of this.config.repositories) {
      const node: DAGNode = {
        id: `repo-${repo.id}`,
        type: 'repo',
        repository: repo.id,
        organization: repo.organization,
        glLayer: repo.glLayer,
        semanticAnchor: `@GL-repo:${repo.id}`,
        dependencies: [],
        dependents: [],
        priority: 1,
        status: 'pending',
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          retryCount: 0
        },
        governance: {
          isCompliant: true,
          complianceScore: 100,
          violations: [],
          lastAuditAt: new Date().toISOString()
        }
      };
      
      this.graph.addNode(node);
    }
  }
  
  /**
   * Build pipeline nodes
   */
  private async buildPipelineNodes(): Promise<void> {
    for (const pipeline of this.config.pipelines) {
      const node: DAGNode = {
        id: `pipeline-${pipeline.id}`,
        type: 'pipeline',
        repository: pipeline.repository,
        organization: pipeline.organization,
        glLayer: 'GL70-89',
        semanticAnchor: `@GL-pipeline:${pipeline.id}`,
        dependencies: [
          `repo-${pipeline.repository}`,
          ...(pipeline.dependencies || []).map(dep => `pipeline-${dep}`)
        ],
        dependents: [],
        priority: 5,
        status: 'pending',
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          retryCount: 0
        },
        governance: {
          isCompliant: true,
          complianceScore: 100,
          violations: [],
          lastAuditAt: new Date().toISOString()
        }
      };
      
      this.graph.addNode(node);
    }
  }
  
  /**
   * Build agent nodes
   */
  private async buildAgentNodes(): Promise<void> {
    for (const agent of this.config.agents) {
      const node: DAGNode = {
        id: `agent-${agent.id}`,
        type: 'agent',
        repository: agent.repository,
        organization: agent.organization,
        glLayer: 'GL80-89',
        semanticAnchor: `@GL-agent:${agent.id}`,
        dependencies: [`repo-${agent.repository}`],
        dependents: [],
        priority: agent.priority,
        status: 'pending',
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          retryCount: 0
        },
        governance: {
          isCompliant: true,
          complianceScore: 100,
          violations: [],
          lastAuditAt: new Date().toISOString()
        }
      };
      
      this.graph.addNode(node);
    }
  }
  
  /**
   * Build file nodes by scanning repositories
   */
  private async buildFileNodes(): Promise<void> {
    for (const repo of this.config.repositories) {
      if (!fs.existsSync(repo.path)) continue;
      
      const scanDirectory = (dir: string, basePath: string = ''): void => {
        const files = fs.readdirSync(dir);
        
        for (const file of files) {
          const fullPath = path.join(dir, file);
          const relativePath = path.join(basePath, file);
          const stat = fs.statSync(fullPath);
          
          if (stat.isDirectory()) {
            // Skip certain directories
            if (['node_modules', '.git', 'dist', 'build', 'summarized_conversations'].includes(file)) {
              continue;
            }
            scanDirectory(fullPath, relativePath);
          } else {
            const fileExt = path.extname(file);
            const fileType = this.getFileType(fileExt);
            
            const node: DAGNode = {
              id: `file-${repo.id}-${relativePath.replace(/\//g, '-')}`,
              type: 'file',
              repository: repo.id,
              organization: repo.organization,
              glLayer: 'GL50-69',
              semanticAnchor: `@GL-file:${relativePath}`,
              path: relativePath,
              dependencies: [`repo-${repo.id}`],
              dependents: [],
              priority: 3,
              status: 'pending',
              metadata: {
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                retryCount: 0
              },
              governance: {
                isCompliant: true,
                complianceScore: 100,
                violations: [],
                lastAuditAt: new Date().toISOString()
              }
            };
            
            this.graph.addNode(node);
          }
        }
      };
      
      scanDirectory(repo.path);
    }
  }
  
  /**
   * Build semantic nodes from SRG
   */
  private async buildSemanticNodes(): Promise<void> {
    // Extract semantic nodes from SRG (if available)
    const semanticNodes = this.graph.getNodesByType('file');
    
    for (const node of semanticNodes) {
      const semanticNode: DAGNode = {
        id: `semantic-${node.id}`,
        type: 'semantic-unit',
        repository: node.repository,
        organization: node.organization,
        glLayer: node.glLayer,
        semanticAnchor: node.semanticAnchor,
        dependencies: [node.id],
        dependents: [],
        priority: 4,
        status: 'pending',
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          retryCount: 0
        },
        governance: {
          isCompliant: true,
          complianceScore: 100,
          violations: [],
          lastAuditAt: new Date().toISOString()
        }
      };
      
      this.graph.addNode(semanticNode);
    }
  }
  
  /**
   * Build cluster nodes
   */
  private async buildClusterNodes(): Promise<void> {
    for (const cluster of this.config.clusters) {
      const node: DAGNode = {
        id: `cluster-${cluster.id}`,
        type: 'cluster',
        repository: 'infrastructure',
        organization: 'MachineNativeOps',
        glLayer: 'GL90-99',
        semanticAnchor: `@GL-cluster:${cluster.id}`,
        dependencies: [],
        dependents: [],
        priority: 1,
        status: 'pending',
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          retryCount: 0
        },
        governance: {
          isCompliant: true,
          complianceScore: 100,
          violations: [],
          lastAuditAt: new Date().toISOString()
        }
      };
      
      this.graph.addNode(node);
    }
  }
  
  /**
   * Build deployment nodes
   */
  private async buildDeploymentNodes(): Promise<void> {
    const pipelines = this.graph.getNodesByType('pipeline');
    const clusters = this.graph.getNodesByType('cluster');
    
    for (const pipeline of pipelines) {
      for (const cluster of clusters) {
        const node: DAGNode = {
          id: `deployment-${pipeline.repository}-${cluster.id}`,
          type: 'deployment',
          repository: pipeline.repository,
          organization: pipeline.organization,
          glLayer: 'GL90-99',
          semanticAnchor: `@GL-deployment:${pipeline.repository}-${cluster.id}`,
          dependencies: [pipeline.id, cluster.id],
          dependents: [],
          priority: 8,
          status: 'pending',
          metadata: {
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            retryCount: 0
          },
          governance: {
            isCompliant: true,
            complianceScore: 100,
            violations: [],
            lastAuditAt: new Date().toISOString()
          }
        };
        
        this.graph.addNode(node);
      }
    }
  }
  
  /**
   * Build edges between nodes
   */
  private async buildEdges(): Promise<void> {
    const nodes = Array.from(this.graph.getNodesByType('file'));
    
    for (const node of nodes) {
      // Add dependency edges
      for (const depId of node.dependencies) {
        const edge: DAGEdge = {
          id: `edge-${depId}-${node.id}`,
          source: depId,
          target: node.id,
          type: 'dependency',
          strength: 1.0,
          critical: true
        };
        
        this.graph.addEdge(edge);
      }
    }
  }
  
  /**
   * Validate graph structure
   */
  private validateGraph(): void {
    const cycles = this.graph.detectCycles();
    
    if (cycles.length > 0) {
      console.warn('⚠️  Detected circular dependencies:', cycles);
      // Auto-fix cycles by breaking edges
      for (const cycle of cycles) {
        if (cycle.length > 0) {
          const edgeToRemove = this.graph.getNodesByType('file')
            .find(n => n.id === cycle[0]);
          if (edgeToRemove) {
            edgeToRemove.dependencies = edgeToRemove.dependencies.filter(
              d => d !== cycle[cycle.length - 1]
            );
          }
        }
      }
    }
    
    console.log('✅ Graph validation complete');
  }
  
  /**
   * Get file type from extension
   */
  private getFileType(ext: string): string {
    const typeMap: Record<string, string> = {
      '.ts': 'typescript',
      '.js': 'javascript',
      '.py': 'python',
      '.yaml': 'yaml',
      '.yml': 'yaml',
      '.json': 'json',
      '.md': 'markdown',
      '.txt': 'text'
    };
    
    return typeMap[ext] || 'unknown';
  }
}