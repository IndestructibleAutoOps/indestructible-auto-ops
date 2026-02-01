// @GL-governed
// @GL-layer: governance
// @GL-semantic: semantic-graph-orchestrator
// @GL-charter-version: 2.0.0

import { ContentParser, ParsedContent } from './content-parsers';
import { SemanticClassifier, SemanticClassification } from './semantic-classifiers';
import { GLMapper, GLMapping } from './gl-mapping';
import { SchemaInferencer, SchemaInference } from './schema-infer';
import { IntentResolver, IntentResolution } from './intent-resolver';
import fs from 'fs/promises';
import path from 'path';

export interface SemanticAnalysis {
  filePath: string;
  parsedContent: ParsedContent;
  classification: SemanticClassification;
  mapping: GLMapping;
  schemaInference: SchemaInference;
  intentResolution: IntentResolution;
  analysisTimestamp: string;
  overallCompliance: boolean;
  issues: string[];
  recommendations: string[];
}

export class SemanticGraphOrchestrator {
  private contentParser: ContentParser;
  private semanticClassifier: SemanticClassifier;
  private glMapper: GLMapper;
  private schemaInferencer: SchemaInferencer;
  private intentResolver: IntentResolver;

  constructor() {
    this.contentParser = new ContentParser();
    this.semanticClassifier = new SemanticClassifier();
    this.glMapper = new GLMapper();
    this.schemaInferencer = new SchemaInferencer();
    this.intentResolver = new IntentResolver();
  }

  async analyzeFile(filePath: string): Promise<SemanticAnalysis> {
    const fileContent = await fs.readFile(filePath, 'utf-8');
    
    // Step 1: Parse content
    const parsedContent = await this.contentParser.parse(filePath);
    
    // Step 2: Classify semantics
    const classification = this.semanticClassifier.classify(filePath, parsedContent);
    
    // Step 3: Map to GL standards
    const mapping = this.glMapper.map(filePath, classification, fileContent);
    
    // Step 4: Infer schema
    const schemaInference = this.schemaInferencer.infer(filePath, parsedContent, classification);
    
    // Step 5: Resolve intent
    const intentResolution = this.intentResolver.resolve(filePath, parsedContent, classification, mapping);
    
    // Step 6: Compile overall analysis
    const overallCompliance = this.checkOverallCompliance(classification, mapping, schemaInference);
    const issues = this.compileIssues(classification, mapping, schemaInference);
    const recommendations = this.compileRecommendations(mapping, intentResolution);

    return {
      filePath,
      parsedContent,
      classification,
      mapping,
      schemaInference,
      intentResolution,
      analysisTimestamp: new Date().toISOString(),
      overallCompliance,
      issues,
      recommendations
    };
  }

  async analyzeDirectory(directoryPath: string, recursive: boolean = true): Promise<SemanticAnalysis[]> {
    const analyses: SemanticAnalysis[] = [];
    const files = await this.scanDirectory(directoryPath, recursive);
    
    for (const file of files) {
      try {
        const analysis = await this.analyzeFile(file);
        analyses.push(analysis);
      } catch (error) {
        console.error(`Error analyzing file ${file}:`, error);
      }
    }
    
    return analyses;
  }

  private async scanDirectory(directoryPath: string, recursive: boolean): Promise<string[]> {
    const files: string[] = [];
    const entries = await fs.readdir(directoryPath, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(directoryPath, entry.name);
      
      if (entry.isDirectory() && recursive) {
        // Skip node_modules and other common exclusions
        if (!entry.name.startsWith('.') && entry.name !== 'node_modules' && entry.name !== 'dist') {
          const subFiles = await this.scanDirectory(fullPath, recursive);
          files.push(...subFiles);
        }
      } else if (entry.isFile()) {
        // Include relevant file types
        const ext = path.extname(entry.name).toLowerCase();
        if (['.ts', '.js', '.py', '.yaml', '.yml', '.json', '.md'].includes(ext)) {
          files.push(fullPath);
        }
      }
    }
    
    return files;
  }

  private checkOverallCompliance(
    classification: SemanticClassification,
    mapping: GLMapping,
    schemaInference: SchemaInference
  ): boolean {
    return mapping.governanceCompliant &&
           classification.governanceCompliance.hasGovernedTag &&
           classification.governanceCompliance.hasSemanticAnchor &&
           classification.governanceCompliance.hasGLLayer &&
           classification.governanceCompliance.hasCharterVersion &&
           mapping.issues.length === 0;
  }

  private compileIssues(
    classification: SemanticClassification,
    mapping: GLMapping,
    schemaInference: SchemaInference
  ): string[] {
    const issues: string[] = [];
    
    issues.push(...mapping.issues);
    
    if (schemaInference.missingMetadata.length > 0) {
      issues.push(`Missing metadata: ${schemaInference.missingMetadata.join(', ')}`);
    }
    
    return issues;
  }

  private compileRecommendations(mapping: GLMapping, intentResolution: IntentResolution): string[] {
    const recommendations: string[] = [];
    
    recommendations.push(...intentResolution.recommendations);
    
    if (mapping.missingTags.length > 0) {
      recommendations.push(`Add missing tags: ${mapping.missingTags.join(', ')}`);
    }
    
    return recommendations;
  }

  async generateAutoRepairPatch(analysis: SemanticAnalysis): Promise<{ patch: string; filePath: string }> {
    const { filePath, mapping } = analysis;
    
    if (!mapping.governanceCompliant) {
      const fileContent = await fs.readFile(filePath, 'utf-8');
      const patchedContent = this.glMapper.applyGovernanceTags(fileContent, mapping);
      
      return {
        filePath,
        patch: patchedContent
      };
    }
    
    return {
      filePath,
      patch: ''
    };
  }

  async applyAutoRepairPatch(analysis: SemanticAnalysis): Promise<boolean> {
    const { patch, filePath } = await this.generateAutoRepairPatch(analysis);
    
    if (patch) {
      await fs.writeFile(filePath, patch, 'utf-8');
      return true;
    }
    
    return false;
  }
}