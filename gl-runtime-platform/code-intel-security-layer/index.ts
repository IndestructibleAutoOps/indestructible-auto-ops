// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: code-intelligence-layer
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Code Intelligence & Security Layer（生成型）
 * Version 21.0.0
 * Main Integration - 主整合文件
 */

import { Capability, CapabilitySchemaRegistry } from './capability-schema';
import { Pattern, PatternLibrary } from './pattern-library';
import { GeneratedCapability, GeneratorEngine } from './generator-engine';
import { EvaluationResult, EvaluationEngine } from './evaluation-engine';
import { DeploymentResult, DeploymentWeaver } from './deployment-weaver';
import { EvolutionEngine, UsageData } from './evolution-engine';
import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// Main Layer Interface
// ============================================================================

export interface CodeIntelLayerConfig {
  generator?: any;
  evaluation?: any;
  deployment?: any;
  evolution?: any;
  autoStart?: boolean;
}

export interface CodeIntelRequest {
  capability: Capability;
  sourceCode?: string;
  language: string;
  framework?: string;
  options?: any;
}

export interface CodeIntelResult {
  success: boolean;
  generatedCapability?: GeneratedCapability;
  evaluationResult?: EvaluationResult;
  deploymentResult?: DeploymentResult;
  errors: string[];
  warnings: string[];
  metrics: {
    generationTime: number;
    evaluationTime: number;
    totalTime: number;
  };
}

// ============================================================================
// Code Intelligence Layer - Main Class
// ============================================================================

export class CodeIntelligenceLayer {
  public static readonly VERSION = '21.0.0';
  
  private capabilityRegistry: CapabilitySchemaRegistry;
  private patternLibrary: PatternLibrary;
  private generatorEngine: GeneratorEngine;
  private evaluationEngine: EvaluationEngine;
  private deploymentWeaver: DeploymentWeaver;
  private evolutionEngine: EvolutionEngine;
  private initialized: boolean = false;
  private started: boolean = false;

  constructor(config?: CodeIntelLayerConfig) {
    // Initialize components
    this.capabilityRegistry = new CapabilitySchemaRegistry();
    this.patternLibrary = new PatternLibrary();
    this.generatorEngine = new GeneratorEngine(
      this.capabilityRegistry,
      this.patternLibrary,
      config?.generator
    );
    this.evaluationEngine = new EvaluationEngine(config?.evaluation);
    this.deploymentWeaver = new DeploymentWeaver(config?.deployment);
    this.evolutionEngine = new EvolutionEngine(
      this.capabilityRegistry,
      this.patternLibrary,
      config?.evolution
    );

    // Register default capabilities
    this.registerDefaultCapabilities();

    // Auto-start if configured
    if (config?.autoStart) {
      this.start();
    }
  }

  /**
   * Initialize the layer
   */
  public async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    // Register default capabilities
    this.registerDefaultCapabilities();

    this.initialized = true;
  }

  /**
   * Start the layer
   */
  public async start(): Promise<void> {
    if (!this.initialized) {
      await this.initialize();
    }

    if (this.started) {
      return;
    }

    // Start evolution engine
    this.evolutionEngine.start();

    this.started = true;
  }

  /**
   * Stop the layer
   */
  public async stop(): Promise<void> {
    if (!this.started) {
      return;
    }

    // Stop evolution engine
    this.evolutionEngine.stop();

    this.started = false;
  }

  /**
   * Execute code intelligence workflow
   */
  public async execute(request: CodeIntelRequest): Promise<CodeIntelResult> {
    const startTime = Date.now();
    const errors: string[] = [];
    const warnings: string[] = [];

    try {
      // Phase 1: Generate capability
      const generationStart = Date.now();
      const generationResult = await this.generatorEngine.generateCapability(
        request.capability,
        {
          language: request.language,
          framework: request.framework,
          targetCode: request.sourceCode
        },
        request.options
      );
      const generationTime = Date.now() - generationStart;

      if (!generationResult.success) {
        return {
          success: false,
          errors: generationResult.errors,
          warnings: generationResult.warnings,
          metrics: {
            generationTime,
            evaluationTime: 0,
            totalTime: Date.now() - startTime
          }
        };
      }

      const generatedCapability = generationResult.generatedCapability!;

      // Phase 2: Evaluate generated capability
      const evaluationStart = Date.now();
      const evaluationRequest = {
        id: uuidv4(),
        originalCode: request.sourceCode,
        generatedCapability,
        evaluationType: ['behavior-equivalence', 'security-regression', 'semantic-consistency', 'explainability', 'audit-trail'],
        options: {
          testInputs: request.options?.testInputs,
          expectedOutputs: request.options?.expectedOutputs,
          explanationLevel: 'standard'
        },
        timestamp: Date.now()
      };

      const evaluationResult = await this.evaluationEngine.evaluate(evaluationRequest);
      const evaluationTime = Date.now() - evaluationStart;

      // Phase 3: Record usage data for evolution
      this.evolutionEngine.recordUsage({
        capabilityId: request.capability.id,
        timestamp: Date.now(),
        success: evaluationResult.success,
        executionTime: generationResult.metrics.generationTime,
        userFeedback: request.options?.userFeedback,
        issues: evaluationResult.success ? [] : evaluationResult.errors
      });

      // Phase 4: Deploy if requested
      let deploymentResult: DeploymentResult | undefined;
      if (request.options?.deploy) {
        const deploymentRequest = {
          id: uuidv4(),
          generatedCapabilities: [generatedCapability],
          evaluationResults: new Map([['main', evaluationResult]]),
          deploymentTargets: request.options.deploymentTargets || [],
          options: {
            includeTests: true,
            includeDocs: true,
            minConfidenceScore: 0.7,
            optimizeForProduction: false
          },
          timestamp: Date.now()
        };

        deploymentResult = await this.deploymentWeaver.deploy(deploymentRequest);
      }

      const totalTime = Date.now() - startTime;

      return {
        success: evaluationResult.success,
        generatedCapability,
        evaluationResult,
        deploymentResult,
        errors: [...generationResult.errors, ...evaluationResult.errors],
        warnings: [...generationResult.warnings, ...evaluationResult.warnings],
        metrics: {
          generationTime,
          evaluationTime,
          totalTime
        }
      };

    } catch (error: any) {
      errors.push(error.message);
      
      return {
        success: false,
        errors,
        warnings,
        metrics: {
          generationTime: 0,
          evaluationTime: 0,
          totalTime: Date.now() - startTime
        }
      };
    }
  }

  /**
   * Register default capabilities
   */
  private registerDefaultCapabilities(): void {
    // Import and register predefined capabilities
    const { DEEP_CODE_UNDERSTANDING_CAPABILITY } = require('./capability-schema/index');
    const { SECURITY_HARDENING_CAPABILITY } = require('./capability-schema/index');

    this.capabilityRegistry.register(DEEP_CODE_UNDERSTANDING_CAPABILITY);
    this.capabilityRegistry.register(SECURITY_HARDENING_CAPABILITY);
  }

  /**
   * Get capability by ID
   */
  public getCapability(id: string): Capability | undefined {
    return this.capabilityRegistry.get(id);
  }

  /**
   * Get pattern by ID
   */
  public getPattern(id: string): Pattern | undefined {
    return this.patternLibrary.get(id);
  }

  /**
   * Get capabilities by category
   */
  public getCapabilitiesByCategory(category: string): Capability[] {
    return this.capabilityRegistry.getByCategory(category as any);
  }

  /**
   * Get patterns by category
   */
  public getPatternsByCategory(category: string): Pattern[] {
    return this.patternLibrary.getByCategory(category as any);
  }

  /**
   * Get layer statistics
   */
  public getStatistics(): {
    capabilities: number;
    patterns: number;
    generationCacheSize: number;
    evolutionGeneration: number;
    totalEvolutions: number;
    isStarted: boolean;
  } {
    const generatorStats = this.generatorEngine.getStatistics();
    const evolutionStats = this.evolutionEngine.getStatistics();

    return {
      capabilities: this.capabilityRegistry.getAll().length,
      patterns: this.patternLibrary.getAll().length,
      generationCacheSize: generatorStats.cacheSize,
      evolutionGeneration: evolutionStats.generation,
      totalEvolutions: evolutionStats.totalEvolutions,
      isStarted: this.started
    };
  }

  /**
   * Get evolution metrics
   */
  public getEvolutionMetrics() {
    return this.evolutionEngine.getMetrics();
  }

  /**
   * Export layer state
   */
  public exportState(): string {
    const state = {
      version: CodeIntelligenceLayer.VERSION,
      initialized: this.initialized,
      started: this.started,
      capabilities: this.capabilityRegistry.export(),
      patterns: this.patternLibrary.export(),
      evolutionState: this.evolutionEngine.exportState(),
      statistics: this.getStatistics(),
      exportedAt: Date.now()
    };

    return JSON.stringify(state, null, 2);
  }

  /**
   * Import layer state
   */
  public importState(json: string): void {
    try {
      const state = JSON.parse(json);

      // Import evolution state
      if (state.evolutionState) {
        this.evolutionEngine.importState(state.evolutionState);
      }

      // Import capabilities and patterns
      if (state.capabilities) {
        this.capabilityRegistry.import(state.capabilities);
      }

      if (state.patterns) {
        this.patternLibrary.import(state.patterns);
      }

    } catch (error: any) {
      throw new Error(`Failed to import state: ${error.message}`);
    }
  }

  /**
   * Reset layer
   */
  public async reset(): Promise<void> {
    await this.stop();
    this.capabilityRegistry = new CapabilitySchemaRegistry();
    this.patternLibrary = new PatternLibrary();
    this.registerDefaultCapabilities();
    this.initialized = false;
  }
}

// Export all components
export * from './capability-schema';
export * from './pattern-library';
export * from './generator-engine';
export * from './evaluation-engine';
export * from './deployment-weaver';
export * from './evolution-engine';
export * from './fabric-continuum-integration';
/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */

/**
 * Code Intelligence & Security Layer - Main Integration Module
 * 
 * This module provides integration with V19 Unified Intelligence Fabric
 * for code analysis, security scanning, and governance enforcement.
 */

import { DeploymentWeaver } from './deployment-weaver';
import { PatternLibrary } from './pattern-library';

/**
 * Code Intelligence Layer configuration
 */
export interface CodeIntelConfig {
  enableFabricIntegration: boolean;
  securityLevel: 'low' | 'medium' | 'high';
  fabricEndpoint?: string;
}

/**
 * Main Code Intelligence Layer class
 */
export class CodeIntelligenceLayer {
  private config: CodeIntelConfig;
  private deploymentWeaver: DeploymentWeaver;
  private patternLibrary: PatternLibrary;

  constructor(config: CodeIntelConfig = { enableFabricIntegration: true, securityLevel: 'high' }) {
    this.config = config;
    this.deploymentWeaver = new DeploymentWeaver();
    this.patternLibrary = new PatternLibrary();
  }

  /**
   * Initialize the Code Intelligence Layer with V19 Fabric integration
   */
  async initialize(): Promise<void> {
    console.log('Initializing Code Intelligence Layer...');
    
    if (this.config.enableFabricIntegration) {
      console.log('🔗 Connecting to V19 Unified Intelligence Fabric...');
      await this.connectToFabric();
    }
    
    await this.deploymentWeaver.initialize();
    await this.patternLibrary.loadPatterns();
    
    console.log('✅ Code Intelligence Layer initialized');
  }

  /**
   * Connect to V19 Unified Intelligence Fabric
   */
  private async connectToFabric(): Promise<void> {
    // Simulate fabric connection
    const endpoint = this.config.fabricEndpoint || 'fabric://v19-unified';
    console.log(`Connected to fabric at: ${endpoint}`);
    
    // Integration point with V19 fabric
    return Promise.resolve();
  }

  /**
   * Analyze code for vulnerabilities and issues
   */
  async analyzeCode(code: string): Promise<{ vulnerabilities: number; issues: number }> {
    const vulnerabilities = await this.deploymentWeaver.scanVulnerabilities(code);
    const issues = await this.patternLibrary.detectIssues(code);
    
    return { vulnerabilities, issues };
  }

  /**
   * Enforce security policies
   */
  async enforceSecurityPolicies(code: string): Promise<boolean> {
    const analysis = await this.analyzeCode(code);
    return analysis.vulnerabilities === 0 && analysis.issues === 0;
  }

  /**
   * Get fabric integration status
   */
  getFabricIntegrationStatus(): { connected: boolean; endpoint?: string } {
    return {
      connected: this.config.enableFabricIntegration,
      endpoint: this.config.fabricEndpoint || 'fabric://v19-unified'
    };
  }
}

/**
 * Export singleton instance
 */
export const codeIntelLayer = new CodeIntelligenceLayer();
