// @GL-governed
// @GL-layer: governance
// @GL-semantic: semantic-classifier
// @GL-charter-version: 2.0.0

import { ParsedContent } from '../content-parsers';

export interface SemanticClassification {
  role: string;
  purpose: string;
  category: string;
  glLayer: string;
  semanticAnchor: string;
  criticality: 'low' | 'medium' | 'high' | 'critical';
  dependencies: string[];
  provides: string[];
  governanceCompliance: {
    hasSemanticAnchor: boolean;
    hasGLLayer: boolean;
    hasCharterVersion: boolean;
    hasGovernedTag: boolean;
    schemaCompliant: boolean;
  };
}

export class SemanticClassifier {
  classify(filePath: string, parsedContent: ParsedContent): SemanticClassification {
    const pathSegments = filePath.split('/');
    const fileName = pathSegments[pathSegments.length - 1];
    
    // Determine role based on path and content
    const role = this.determineRole(filePath, parsedContent);
    const purpose = this.determinePurpose(filePath, parsedContent);
    const category = this.determineCategory(filePath, parsedContent);
    const glLayer = this.determineGLLayer(filePath, parsedContent);
    const semanticAnchor = this.determineSemanticAnchor(filePath, parsedContent);
    const criticality = this.determineCriticality(filePath, parsedContent);
    const dependencies = this.extractDependencies(filePath, parsedContent);
    const provides = this.extractProvides(filePath, parsedContent);
    const governanceCompliance = this.checkGovernanceCompliance(filePath, parsedContent);

    return {
      role,
      purpose,
      category,
      glLayer,
      semanticAnchor,
      criticality,
      dependencies,
      provides,
      governanceCompliance
    };
  }

  private determineRole(filePath: string, content: ParsedContent): string {
    const pathLower = filePath.toLowerCase();
    
    if (pathLower.includes('orchestrat')) return 'orchestrator';
    if (pathLower.includes('pipeline')) return 'pipeline';
    if (pathLower.includes('agent')) return 'agent';
    if (pathLower.includes('connector')) return 'connector';
    if (pathLower.includes('scanner')) return 'scanner';
    if (pathLower.includes('validator')) return 'validator';
    if (pathLower.includes('policy')) return 'policy';
    if (pathLower.includes('engine')) return 'engine';
    if (pathLower.includes('runtime')) return 'runtime';
    if (pathLower.includes('api')) return 'api';
    if (pathLower.includes('route')) return 'route';
    if (pathLower.includes('model')) return 'data-model';
    if (pathLower.includes('schema')) return 'schema';
    if (pathLower.includes('config')) return 'configuration';
    if (pathLower.includes('hook')) return 'hook';
    if (pathLower.includes('docker') || pathLower.includes('k8s') || pathLower.includes('deployment')) return 'deployment';
    if (pathLower.includes('readme')) return 'documentation';
    if (content.type === 'code') {
      if (content.classes && content.classes.length > 0) return 'class';
      if (content.functions && content.functions.length > 0) return 'module';
    }
    
    return 'resource';
  }

  private determinePurpose(filePath: string, content: ParsedContent): string {
    const pathLower = filePath.toLowerCase();
    
    if (pathLower.includes('audit')) return 'governance-audit';
    if (pathLower.includes('repair') || pathLower.includes('fix')) return 'auto-repair';
    if (pathLower.includes('deploy')) return 'deployment';
    if (pathLower.includes('sync')) return 'synchronization';
    if (pathLower.includes('monitor')) return 'monitoring';
    if (pathLower.includes('security')) return 'security';
    if (pathLower.includes('quality')) return 'quality-assurance';
    if (pathLower.includes('scan')) return 'scanning';
    if (pathLower.includes('event')) return 'event-management';
    if (pathLower.includes('artifact')) return 'artifact-storage';
    if (pathLower.includes('index')) return 'indexing';
    if (pathLower.includes('graph')) return 'graph-management';
    if (pathLower.includes('semantic')) return 'semantic-analysis';
    if (pathLower.includes('federation')) return 'federation-governance';
    
    if (content.apiEndpoints && content.apiEndpoints.length > 0) return 'api-exposure';
    if (content.schemas && content.schemas.length > 0) return 'schema-definition';
    if (content.functions && content.functions.length > 0) return 'functionality';
    if (content.classes && content.classes.length > 0) return 'behavior-implementation';
    
    return 'general-purpose';
  }

  private determineCategory(filePath: string, content: ParsedContent): string {
    if (content.type === 'code') {
      if (filePath.includes('test') || filePath.includes('spec')) return 'testing';
      if (filePath.includes('src/')) return 'source';
      return 'code';
    }
    if (content.type === 'configuration') return 'configuration';
    if (content.type === 'data') return 'data';
    if (content.type === 'documentation') return 'documentation';
    return 'other';
  }

  private determineGLLayer(filePath: string, content: ParsedContent): string {
    const pathLower = filePath.toLowerCase();
    
    if (pathLower.includes('governance') || pathLower.includes('policy') || pathLower.includes('audit')) return 'GL90-99';
    if (pathLower.includes('engine') || pathLower.includes('runtime') || pathLower.includes('orchestrat')) return 'GL70-89';
    if (pathLower.includes('federation')) return 'GL50-69';
    if (pathLower.includes('agent')) return 'GL30-49';
    if (pathLower.includes('connector') || pathLower.includes('scanner')) return 'GL10-29';
    if (pathLower.includes('deployment') || pathLower.includes('ops')) return 'GL00-09';
    
    return 'GL00-99';
  }

  private determineSemanticAnchor(filePath: string, content: ParsedContent): string {
    const fileName = filePath.split('/').pop() || '';
    const baseName = fileName.replace(/\.(ts|js|py|yaml|yml|json|md)$/, '');
    
    const pathLower = filePath.toLowerCase();
    
    if (pathLower.includes('orchestrat')) return 'orchestrator-engine';
    if (pathLower.includes('policy')) return 'policy-engine';
    if (pathLower.includes('event')) return 'event-stream';
    if (pathLower.includes('artifact')) return 'artifact-store';
    if (pathLower.includes('scanner')) return 'resource-scanner';
    if (pathLower.includes('indexer')) return 'resource-indexer';
    if (pathLower.includes('graph')) return 'resource-graph';
    if (pathLower.includes('semantic')) return 'semantic-analysis';
    if (pathLower.includes('federation')) return 'federation-governance';
    
    if (content.type === 'code') {
      if (content.classes && content.classes.length > 0) {
        return content.classes[0].toLowerCase().replace(/[^a-z0-9]/g, '-');
      }
      if (content.functions && content.functions.length > 0) {
        return content.functions[0].toLowerCase().replace(/[^a-z0-9]/g, '-');
      }
    }
    
    return baseName.toLowerCase().replace(/[^a-z0-9]/g, '-');
  }

  private determineCriticality(filePath: string, content: ParsedContent): 'low' | 'medium' | 'high' | 'critical' {
    const pathLower = filePath.toLowerCase();
    
    if (pathLower.includes('engine') || pathLower.includes('orchestrat') || pathLower.includes('runtime')) {
      return 'critical';
    }
    if (pathLower.includes('governance') || pathLower.includes('policy') || pathLower.includes('security')) {
      return 'critical';
    }
    if (pathLower.includes('api') || pathLower.includes('route') || pathLower.includes('connector')) {
      return 'high';
    }
    if (pathLower.includes('federation') || pathLower.includes('federation')) {
      return 'high';
    }
    if (pathLower.includes('agent') || pathLower.includes('pipeline')) {
      return 'high';
    }
    if (pathLower.includes('scanner') || pathLower.includes('validator')) {
      return 'medium';
    }
    if (pathLower.includes('monitor') || pathLower.includes('event')) {
      return 'medium';
    }
    
    return 'low';
  }

  private extractDependencies(filePath: string, content: ParsedContent): string[] {
    const deps: string[] = [];
    
    if (content.imports) {
      content.imports.forEach(imp => {
        if (!imp.startsWith('.') && !imp.startsWith('/')) {
          deps.push(imp);
        }
      });
    }
    
    return [...new Set(deps)];
  }

  private extractProvides(filePath: string, content: ParsedContent): string[] {
    const provides: string[] = [];
    
    if (content.exports) {
      content.exports.forEach(exp => provides.push(exp));
    }
    if (content.apiEndpoints) {
      content.apiEndpoints.forEach(ep => {
        if (ep.path && ep.method) {
          provides.push(`${ep.method} ${ep.path}`);
        }
      });
    }
    
    return [...new Set(provides)];
  }

  private checkGovernanceCompliance(filePath: string, content: ParsedContent): SemanticClassification['governanceCompliance'] {
    const contentStr = content.content.toString();
    
    return {
      hasSemanticAnchor: /@GL-semantic:/.test(contentStr),
      hasGLLayer: /@GL-layer:/.test(contentStr),
      hasCharterVersion: /@GL-charter-version:/.test(contentStr),
      hasGovernedTag: /@GL-governed/.test(contentStr),
      schemaCompliant: this.checkSchemaCompliance(filePath, content)
    };
  }

  private checkSchemaCompliance(filePath: string, content: ParsedContent): boolean {
    // Basic schema compliance check
    if (content.type === 'configuration') {
      const contentStr = content.content.toString();
      return /apiVersion:|kind:|metadata:|spec:/.test(contentStr);
    }
    return true;
  }
}