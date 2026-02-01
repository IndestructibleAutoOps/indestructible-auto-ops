// @GL-governed
// @GL-layer: governance
// @GL-semantic: schema-inferencer
// @GL-charter-version: 2.0.0

import { ParsedContent } from '../content-parsers';
import { SemanticClassification } from '../semantic-classifiers';

export interface SchemaInference {
  filePath: string;
  inferredSchema?: any;
  requiredFields: string[];
  optionalFields: string[];
  missingMetadata: string[];
  recommendedSchema?: string;
  schemaType: 'json-schema' | 'yaml-schema' | 'typescript-interface' | 'python-class' | 'unknown';
  confidence: number;
}

export class SchemaInferencer {
  infer(filePath: string, parsedContent: ParsedContent, classification: SemanticClassification): SchemaInference {
    const schemaType = this.determineSchemaType(parsedContent);
    const requiredFields = this.extractRequiredFields(parsedContent, classification);
    const optionalFields = this.extractOptionalFields(parsedContent, classification);
    const missingMetadata = this.identifyMissingMetadata(filePath, classification);
    const inferredSchema = this.generateInferredSchema(parsedContent, classification);
    const recommendedSchema = this.generateRecommendedSchema(filePath, classification);
    const confidence = this.calculateConfidence(parsedContent, classification);

    return {
      filePath,
      inferredSchema,
      requiredFields,
      optionalFields,
      missingMetadata,
      recommendedSchema,
      schemaType,
      confidence
    };
  }

  private determineSchemaType(content: ParsedContent): SchemaInference['schemaType'] {
    if (content.type === 'configuration' && content.format === 'yaml') return 'yaml-schema';
    if (content.type === 'data' && content.format === 'json') return 'json-schema';
    if (content.type === 'code') {
      if (content.language === 'typescript') return 'typescript-interface';
      if (content.language === 'python') return 'python-class';
    }
    return 'unknown';
  }

  private extractRequiredFields(content: ParsedContent, classification: SemanticClassification): string[] {
    const required: string[] = [];
    
    // Extract from code
    if (content.functions) {
      content.functions.forEach(fn => {
        // Look for required parameters
        if (fn.includes('required')) required.push(fn);
      });
    }
    
    // Extract from configuration
    if (content.type === 'configuration') {
      const contentStr = content.content.toString();
      const requiredMatch = contentStr.match(/required:\s*\[([^\]]+)\]/);
      if (requiredMatch) {
        const fields = requiredMatch[1].split(',').map((f: any) => f.trim().replace(/['"]/g, ''));
        required.push(...fields);
      }
    }
    
    // Add governance-specific required fields
    if (classification.role === 'agent' || classification.role === 'pipeline') {
      required.push('name', 'type', 'priority', 'enabled', 'config');
    }
    
    if (classification.role === 'configuration' || content.type === 'configuration') {
      required.push('apiVersion', 'kind', 'metadata', 'spec');
    }
    
    return [...new Set(required)];
  }

  private extractOptionalFields(content: ParsedContent, classification: SemanticClassification): string[] {
    const optional: string[] = [];
    
    // Extract from code
    if (content.functions) {
      content.functions.forEach(fn => {
        if (fn.includes('optional')) optional.push(fn);
      });
    }
    
    // Common optional fields for governance
    optional.push('annotations', 'labels', 'description', 'version', 'created_at');
    
    return [...new Set(optional)];
  }

  private identifyMissingMetadata(filePath: string, classification: SemanticClassification): string[] {
    const missing: string[] = [];
    
    // Check for required metadata fields
    if (classification.role === 'agent' || classification.role === 'pipeline') {
      missing.push('metadata.name');
      missing.push('metadata.version');
      missing.push('metadata.owner');
    }
    
    if (classification.purpose.includes('api')) {
      missing.push('spec.apiVersion');
      missing.push('spec.endpoints');
    }
    
    return [...new Set(missing)];
  }

  private generateInferredSchema(content: ParsedContent, classification: SemanticClassification): any {
    const schema: any = {
      type: 'object',
      properties: {},
      required: []
    };
    
    // Add fields based on classification
    if (classification.role === 'agent') {
      schema.properties = {
        id: { type: 'string' },
        name: { type: 'string' },
        type: { type: 'string' },
        priority: { type: 'number' },
        enabled: { type: 'boolean' },
        config: { type: 'object' },
        dependencies: { type: 'array', items: { type: 'string' } },
        outputs: { type: 'array', items: { type: 'string' } }
      };
      schema.required = ['id', 'name', 'type', 'priority', 'enabled', 'config'];
    }
    
    if (content.apiEndpoints && content.apiEndpoints.length > 0) {
      schema.properties.apiEndpoints = {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            path: { type: 'string' },
            method: { type: 'string', enum: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'] }
          }
        }
      };
    }
    
    if (content.functions && content.functions.length > 0) {
      schema.properties.functions = {
        type: 'array',
        items: { type: 'string' }
      };
      schema.properties.functions.items.enum = content.functions;
    }
    
    return schema;
  }

  private generateRecommendedSchema(filePath: string, classification: SemanticClassification): string {
    const fileName = filePath.split('/').pop() || '';
    const baseName = fileName.replace(/\.(ts|js|py|yaml|yml|json)$/, '');
    
    let schema = '';
    
    if (classification.role === 'agent' || classification.purpose === 'agent') {
      schema = `apiVersion: orchestration.machinenativeops.io/v1
kind: Agent
metadata:
  name: ${baseName}
  version: "1.0.0"
  created_at: "${new Date().toISOString()}"
  layer: "${classification.glLayer}"
  owner: "engineering-team"
  annotations:
    governance.machinenativeops.io/classification: "internal"
    governance.machinenativeops.io/approval: "approved"
    governance.machinenativeops.io/charter-version: "2.0.0"

spec:
  enabled: true
  config:
    validation_scope:
      - "engine"
      - "governance"
    strict_mode: true
    enforce_semantic_anchors: true
  dependencies: []
  outputs:
    - "${baseName}-report.json"
    - "${baseName}-summary.md"`;
    } else if (classification.role === 'pipeline' || classification.purpose.includes('pipeline')) {
      schema = `apiVersion: pipeline.machinenativeops.io/v1
kind: Pipeline
metadata:
  name: ${baseName}
  version: "1.0.0"
  created_at: "${new Date().toISOString()}"
  layer: "${classification.glLayer}"
  owner: "engineering-team"

spec:
  enabled: true
  stages:
    - name: validate
      enabled: true
    - name: fix
      enabled: true
    - name: deploy
      enabled: false
  triggers:
    - event: "gl-audit-complete"
    - event: "gl-violation-detected"`;
    }
    
    return schema;
  }

  private calculateConfidence(content: ParsedContent, classification: SemanticClassification): number {
    let confidence = 0.3; // Base confidence
    
    // Increase confidence based on content analysis
    if (content.type !== 'text') confidence += 0.1;
    if (classification.role !== 'resource') confidence += 0.1;
    if (classification.purpose !== 'general-purpose') confidence += 0.1;
    if (content.functions && content.functions.length > 0) confidence += 0.1;
    if (content.classes && content.classes.length > 0) confidence += 0.1;
    if (content.apiEndpoints && content.apiEndpoints.length > 0) confidence += 0.1;
    if (content.schemas && content.schemas.length > 0) confidence += 0.1;
    
    // Increase confidence if governance tags are present
    if (classification.governanceCompliance.hasSemanticAnchor) confidence += 0.1;
    if (classification.governanceCompliance.hasGLLayer) confidence += 0.1;
    
    return Math.min(1.0, Math.max(0.0, confidence));
  }

  validateSchema(filePath: string, schema: any): boolean {
    // Basic schema validation
    if (!schema || typeof schema !== 'object') return false;
    if (!schema.properties) return false;
    if (!Array.isArray(schema.required)) return false;
    
    return true;
  }
}