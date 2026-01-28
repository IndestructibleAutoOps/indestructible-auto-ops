// @GL-governed
// @GL-layer: governance
// @GL-semantic: gl-mapping-engine
// @GL-charter-version: 2.0.0

import { SemanticClassification } from '../semantic-classifiers';

export interface GLMapping {
  filePath: string;
  glSemanticAnchor: string;
  glLayer: string;
  glCharterVersion: string;
  governanceCompliant: boolean;
  missingTags: string[];
  recommendedPath: string;
  mappingConfidence: number;
  issues: string[];
}

export class GLMapper {
  private readonly VALID_LAYERS = ['GL00-09', 'GL10-29', 'GL30-49', 'GL50-69', 'GL70-89', 'GL90-99'];
  private readonly CHARTER_VERSION = '2.0.0';

  map(filePath: string, classification: SemanticClassification, fileContent: string): GLMapping {
    const glSemanticAnchor = this.generateSemanticAnchor(filePath, classification);
    const glLayer = this.validateLayer(classification.glLayer);
    const glCharterVersion = this.CHARTER_VERSION;
    const governanceCompliant = this.checkGovernanceCompliance(fileContent);
    const missingTags = this.identifyMissingTags(fileContent);
    const recommendedPath = this.generateRecommendedPath(filePath, classification);
    const mappingConfidence = this.calculateConfidence(classification);
    const issues = this.identifyIssues(filePath, classification, fileContent);

    return {
      filePath,
      glSemanticAnchor,
      glLayer,
      glCharterVersion,
      governanceCompliant,
      missingTags,
      recommendedPath,
      mappingConfidence,
      issues
    };
  }

  private generateSemanticAnchor(filePath: string, classification: SemanticClassification): string {
    const parts = [];
    
    // Add category prefix
    if (classification.role) {
      parts.push(classification.role);
    }
    if (classification.purpose) {
      parts.push(classification.purpose);
    }
    
    const anchor = parts.join('-').toLowerCase().replace(/[^a-z0-9-]/g, '-');
    return anchor.replace(/-+/g, '-').replace(/^-|-$/g, '');
  }

  private validateLayer(layer: string): string {
    if (this.VALID_LAYERS.includes(layer)) {
      return layer;
    }
    // Default to broader range if invalid
    return 'GL00-99';
  }

  private checkGovernanceCompliance(content: string): boolean {
    const requiredTags = ['@GL-governed', '@GL-layer:', '@GL-semantic:', '@GL-charter-version:'];
    return requiredTags.every(tag => content.includes(tag));
  }

  private identifyMissingTags(content: string): string[] {
    const missing: string[] = [];
    
    if (!content.includes('@GL-governed')) missing.push('@GL-governed');
    if (!content.includes('@GL-layer:')) missing.push('@GL-layer:');
    if (!content.includes('@GL-semantic:')) missing.push('@GL-semantic:');
    if (!content.includes('@GL-charter-version:')) missing.push('@GL-charter-version:');
    if (!content.includes('@GL-audit-trail:')) missing.push('@GL-audit-trail:');
    
    return missing;
  }

  private generateRecommendedPath(filePath: string, classification: SemanticClassification): string {
    const parts = ['gl-runtime-platform'];
    
    // Map GL layer to directory structure
    switch (classification.glLayer) {
      case 'GL90-99':
        parts.push('governance');
        break;
      case 'GL70-89':
        parts.push('engine');
        break;
      case 'GL50-69':
        parts.push('federation');
        break;
      case 'GL30-49':
        parts.push('agents');
        break;
      case 'GL10-29':
        parts.push('connectors');
        break;
      case 'GL00-09':
        parts.push('ops');
        break;
      default:
        parts.push('src');
    }
    
    // Add role-specific subdirectory
    if (classification.role === 'orchestrator') parts.push('orchestrator-engine');
    else if (classification.role === 'policy') parts.push('policies');
    else if (classification.role === 'event') parts.push('event-stream');
    else if (classification.role === 'agent') parts.push('agents');
    else if (classification.role === 'connector') parts.push('connectors');
    else if (classification.role === 'scanner') parts.push('scanners');
    else if (classification.role === 'validator') parts.push('validators');
    else if (classification.role === 'api') parts.push('api');
    
    const fileName = filePath.split('/').pop() || '';
    parts.push(fileName);
    
    return parts.join('/');
  }

  private calculateConfidence(classification: SemanticClassification): number {
    let confidence = 0.5; // Base confidence
    
    // Increase confidence based on classification quality
    if (classification.role !== 'resource') confidence += 0.1;
    if (classification.purpose !== 'general-purpose') confidence += 0.1;
    if (classification.glLayer !== 'GL00-99') confidence += 0.1;
    if (classification.criticality === 'critical' || classification.criticality === 'high') confidence += 0.1;
    
    // Decrease confidence if governance compliance is missing
    if (!classification.governanceCompliance.hasSemanticAnchor) confidence -= 0.1;
    if (!classification.governanceCompliance.hasGLLayer) confidence -= 0.1;
    
    return Math.min(1.0, Math.max(0.0, confidence));
  }

  private identifyIssues(filePath: string, classification: SemanticClassification, content: string): string[] {
    const issues: string[] = [];
    
    // Check naming conventions
    const fileName = filePath.split('/').pop() || '';
    if (!/^[a-z0-9-]+(\.[a-z]+)?$/.test(fileName)) {
      issues.push('Filename does not follow kebab-case convention');
    }
    
    // Check path structure
    if (filePath.includes('\\')) {
      issues.push('Path contains Windows-style backslashes');
    }
    
    // Check governance tags
    if (!classification.governanceCompliance.hasGovernedTag) {
      issues.push('Missing @GL-governed tag');
    }
    if (!classification.governanceCompliance.hasSemanticAnchor) {
      issues.push('Missing @GL-semantic anchor');
    }
    if (!classification.governanceCompliance.hasGLLayer) {
      issues.push('Missing @GL-layer specification');
    }
    if (!classification.governanceCompliance.hasCharterVersion) {
      issues.push('Missing @GL-charter-version');
    }
    
    // Check for schema compliance
    if (!classification.governanceCompliance.schemaCompliant) {
      issues.push('Schema compliance issue detected');
    }
    
    return issues;
  }

  generateGovernanceTags(mapping: GLMapping): string[] {
    const tags: string[] = [];
    
    tags.push('// @GL-governed');
    tags.push(`// @GL-layer: ${mapping.glLayer}`);
    tags.push(`// @GL-semantic: ${mapping.glSemanticAnchor}`);
    tags.push(`// @GL-charter-version: ${mapping.glCharterVersion}`);
    tags.push('// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json');
    
    return tags;
  }

  applyGovernanceTags(content: string, mapping: GLMapping): string {
    const tags = this.generateGovernanceTags(mapping);
    const tagBlock = tags.join('\n') + '\n\n';
    
    // Check if content already has GL tags
    if (/\/\/\s*@GL-governed/.test(content)) {
      // Replace existing tags
      return content.replace(/\/\/\s*@GL-governed[^\n]*\n(\/\/\s*@GL-[^\n]*\n)*/, tagBlock);
    } else {
      // Add tags at the beginning
      return tagBlock + content;
    }
  }
}