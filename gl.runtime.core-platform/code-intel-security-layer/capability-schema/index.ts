// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: code-intelligence-capability-schema
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Code Intelligence & Security Layer - Capability Schema
 * Version 21.0.0
 * Capability Description Language (CDL) - 能力描述語言
 */

import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// Core Capability Types
// ============================================================================

export interface Capability {
  id: string;
  name: string;
  version: string;
  category: CapabilityCategory;
  description: string;
  
  // Input/Output Specification
  inputs: CapabilityInput[];
  outputs: CapabilityOutput[];
  
  // Dimensions
  dimensions: CapabilityDimensions;
  
  // Guarantees
  guarantees: CapabilityGuarantee[];
  
  // Metadata
  metadata: CapabilityMetadata;
  
  // Evolution tracking
  evolution: CapabilityEvolution;
}

export type CapabilityCategory = 
  | 'deep-code-understanding'
  | 'security-hardening'
  | 'performance-optimization'
  | 'architecture-refactoring'
  | 'test-generation'
  | 'documentation-synthesis'
  | 'dependency-analysis'
  | 'vulnerability-detection';

export interface CapabilityInput {
  id: string;
  type: InputType;
  description: string;
  required: boolean;
  validation?: ValidationRule[];
}

export type InputType = 
  | 'sourcecode'
  | 'runtimetraces'
  | 'dependency-graph'
  | 'configuration'
  | 'metrics'
  | 'logs'
  | 'user-feedback'
  | 'pattern-hints';

export interface ValidationRule {
  type: 'regex' | 'schema' | 'custom' | 'type-check';
  rule: string | object;
  errorMessage: string;
}

export interface CapabilityOutput {
  id: string;
  type: OutputType;
  description: string;
  format: OutputFormat;
}

export type OutputType = 
  | 'semantic-model'
  | 'architecture-map'
  | 'risk-profile'
  | 'patch'
  | 'refactored-code'
  | 'test-cases'
  | 'documentation'
  | 'metrics'
  | 'report'
  | 'visualization';

export type OutputFormat = 'json' | 'yaml' | 'xml' | 'markdown' | 'sarif' | 'html' | 'binary';

// ============================================================================
// Capability Dimensions
// ============================================================================

export interface CapabilityDimensions {
  languages: string[];
  frameworks: string[];
  analysisDepth: AnalysisDepth[];
  scope: Scope[];
  complexity: ComplexityRange;
}

export type AnalysisDepth = 
  | 'ast'
  | 'cfg'
  | 'dfg'
  | 'semantic-intent'
  | 'runtime-behavior'
  | 'security-semantics';

export type Scope = 
  | 'file'
  | 'module'
  | 'package'
  | 'repository'
  | 'monorepo'
  | 'ecosystem';

export interface ComplexityRange {
  min: number;
  max: number;
  unit: 'lines' | 'functions' | 'classes' | 'modules' | 'packages';
}

// ============================================================================
// Capability Guarantees
// ============================================================================

export interface CapabilityGuarantee {
  type: GuaranteeType;
  description: string;
  verificationMethod: VerificationMethod;
  confidenceLevel: number; // 0-1
}

export type GuaranteeType = 
  | 'behavior-preserving'
  | 'security-non-regressive'
  | 'performance-non-regressive'
  | 'explainable'
  | 'reversible'
  | 'audit-trail'
  | 'minimal-change';

export type VerificationMethod = 
  | 'formal-verification'
  | 'differential-testing'
  | 'static-analysis'
  | 'runtime-validation'
  | 'human-review'
  | 'automated-testing';

// ============================================================================
// Capability Metadata
// ============================================================================

export interface CapabilityMetadata {
  createdAt: number;
  updatedAt: number;
  createdBy: string;
  approvedBy?: string;
  approvalStatus: 'pending' | 'approved' | 'rejected';
  tags: string[];
  dependencies: string[]; // IDs of other capabilities
  conflictingCapabilities?: string[];
  performanceMetrics?: PerformanceMetrics;
}

export interface PerformanceMetrics {
  avgExecutionTime: number; // ms
  maxMemoryUsage: number; // MB
  throughput: number; // operations per second
  accuracy: number; // 0-1
  falsePositiveRate: number; // 0-1
}

// ============================================================================
// Capability Evolution
// ============================================================================

export interface CapabilityEvolution {
  generation: number;
  parentIds: string[];
  mutationHistory: MutationEvent[];
  performanceHistory: PerformanceSnapshot[];
  adaptationRate: number;
}

export interface MutationEvent {
  id: string;
  timestamp: number;
  type: 'pattern-update' | 'schema-extension' | 'optimization' | 'bugfix';
  description: string;
  impact: number;
}

export interface PerformanceSnapshot {
  timestamp: number;
  metrics: PerformanceMetrics;
  context: string;
}

// ============================================================================
// Capability Schema Registry
// ============================================================================

export class CapabilitySchemaRegistry {
  private capabilities: Map<string, Capability>;
  private categoryIndex: Map<CapabilityCategory, Set<string>>;
  private tagIndex: Map<string, Set<string>>;

  constructor() {
    this.capabilities = new Map();
    this.categoryIndex = new Map();
    this.tagIndex = new Map();
  }

  /**
   * Register a capability schema
   */
  public register(capability: Capability): void {
    this.capabilities.set(capability.id, capability);
    
    // Update category index
    if (!this.categoryIndex.has(capability.category)) {
      this.categoryIndex.set(capability.category, new Set());
    }
    this.categoryIndex.get(capability.category)!.add(capability.id);
    
    // Update tag index
    for (const tag of capability.metadata.tags) {
      if (!this.tagIndex.has(tag)) {
        this.tagIndex.set(tag, new Set());
      }
      this.tagIndex.get(tag)!.add(capability.id);
    }
  }

  /**
   * Get capability by ID
   */
  public get(id: string): Capability | undefined {
    return this.capabilities.get(id);
  }

  /**
   * Get capabilities by category
   */
  public getByCategory(category: CapabilityCategory): Capability[] {
    const ids = this.categoryIndex.get(category);
    if (!ids) return [];
    
    return Array.from(ids)
      .map(id => this.capabilities.get(id)!)
      .filter(c => c !== undefined);
  }

  /**
   * Get capabilities by tags
   */
  public getByTag(tag: string): Capability[] {
    const ids = this.tagIndex.get(tag);
    if (!ids) return [];
    
    return Array.from(ids)
      .map(id => this.capabilities.get(id)!)
      .filter(c => c !== undefined);
  }

  /**
   * Search capabilities
   */
  public search(query: CapabilitySearchQuery): Capability[] {
    let results: Capability[] = Array.from(this.capabilities.values());

    if (query.category) {
      results = results.filter(c => c.category === query.category);
    }

    if (query.languages && query.languages.length > 0) {
      results = results.filter(c => 
        query.languages!.some(lang => c.dimensions.languages.includes(lang))
      );
    }

    if (query.frameworks && query.frameworks.length > 0) {
      results = results.filter(c => 
        query.frameworks!.some(fw => c.dimensions.frameworks.includes(fw))
      );
    }

    if (query.tags && query.tags.length > 0) {
      results = results.filter(c =>
        query.tags!.some(tag => c.metadata.tags.includes(tag))
      );
    }

    if (query.approvalStatus) {
      results = results.filter(c => 
        c.metadata.approvalStatus === query.approvalStatus
      );
    }

    return results;
  }

  /**
   * Validate capability schema
   */
  public validate(capability: Capability): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check required fields
    if (!capability.id) errors.push('Capability ID is required');
    if (!capability.name) errors.push('Capability name is required');
    if (!capability.category) errors.push('Capability category is required');
    
    // Validate inputs
    if (capability.inputs.length === 0) {
      warnings.push('Capability has no inputs');
    }
    
    // Validate outputs
    if (capability.outputs.length === 0) {
      warnings.push('Capability has no outputs');
    }
    
    // Validate guarantees
    if (capability.guarantees.length === 0) {
      warnings.push('Capability has no guarantees');
    }
    
    // Validate evolution
    if (capability.evolution.generation < 0) {
      errors.push('Evolution generation must be non-negative');
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings
    };
  }

  /**
   * Get all capabilities
   */
  public getAll(): Capability[] {
    return Array.from(this.capabilities.values());
  }

  /**
   * Export capabilities as JSON
   */
  public export(): string {
    const data = {
      capabilities: Array.from(this.capabilities.values()),
      exportedAt: Date.now()
    };
    
    return JSON.stringify(data, null, 2);
  }

  /**
   * Import capabilities from JSON
   */
  public import(json: string): void {
    try {
      const data = JSON.parse(json);
      
      if (data.capabilities && Array.isArray(data.capabilities)) {
        for (const cap of data.capabilities) {
          this.register(cap);
        }
      }
    } catch (error) {
      throw new Error('Failed to import capabilities: Invalid JSON');
    }
  }
}

export interface CapabilitySearchQuery {
  category?: CapabilityCategory;
  languages?: string[];
  frameworks?: string[];
  tags?: string[];
  approvalStatus?: 'pending' | 'approved' | 'rejected';
  minConfidence?: number;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

// ============================================================================
// Predefined Capability Templates
// ============================================================================

export const DEEP_CODE_UNDERSTANDING_CAPABILITY: Capability = {
  id: 'deep-code-understanding-v1',
  name: 'Deep Code Understanding',
  version: '1.0.0',
  category: 'deep-code-understanding',
  description: 'Multi-dimensional deep semantic analysis of source code including AST, control flow, data flow, and developer intent inference',
  inputs: [
    {
      id: 'source-code',
      type: 'sourcecode',
      description: 'Source code to analyze',
      required: true,
      validation: [
        { type: 'type-check', rule: 'string', errorMessage: 'Source code must be a string' }
      ]
    },
    {
      id: 'dependency-graph',
      type: 'dependency-graph',
      description: 'Optional dependency graph for cross-file analysis',
      required: false
    },
    {
      id: 'runtimetraces',
      type: 'runtimetraces',
      description: 'Optional runtime traces for behavior modeling',
      required: false
    }
  ],
  outputs: [
    {
      id: 'semantic-model',
      type: 'semantic-model',
      description: 'Comprehensive semantic representation of the code',
      format: 'json'
    },
    {
      id: 'architecture-map',
      type: 'architecture-map',
      description: 'Visualizable architecture mapping',
      format: 'json'
    },
    {
      id: 'risk-profile',
      type: 'risk-profile',
      description: 'Identified risks and vulnerabilities',
      format: 'sarif'
    }
  ],
  dimensions: {
    languages: ['TypeScript', 'JavaScript', 'Python', 'Java', 'Rust', 'C/C++'],
    frameworks: ['React', 'Vue', 'Angular', 'Spring', 'Django', 'Express'],
    analysisDepth: ['ast', 'cfg', 'dfg', 'semantic-intent'],
    scope: ['file', 'module', 'package', 'repository'],
    complexity: { min: 10, max: 1000000, unit: 'lines' }
  },
  guarantees: [
    {
      type: 'explainable',
      description: 'All analysis results are explainable and traceable to source',
      verificationMethod: 'human-review',
      confidenceLevel: 0.9
    },
    {
      type: 'audit-trail',
      description: 'Complete audit trail of all analysis steps',
      verificationMethod: 'automated-testing',
      confidenceLevel: 1.0
    }
  ],
  metadata: {
    createdAt: Date.now(),
    updatedAt: Date.now(),
    createdBy: 'GL-System',
    approvalStatus: 'approved',
    tags: ['semantic', 'analysis', 'multi-language', 'deep'],
    dependencies: [],
    performanceMetrics: {
      avgExecutionTime: 5000,
      maxMemoryUsage: 512,
      throughput: 0.2,
      accuracy: 0.95,
      falsePositiveRate: 0.05
    }
  },
  evolution: {
    generation: 1,
    parentIds: [],
    mutationHistory: [],
    performanceHistory: [],
    adaptationRate: 0.1
  }
};

export const SECURITY_HARDENING_CAPABILITY: Capability = {
  id: 'security-hardening-v1',
  name: 'Security Hardening',
  version: '1.0.0',
  category: 'security-hardening',
  description: 'Automatic security vulnerability detection and patch generation with behavior preservation guarantees',
  inputs: [
    {
      id: 'source-code',
      type: 'sourcecode',
      description: 'Source code to harden',
      required: true
    },
    {
      id: 'vulnerability-report',
      type: 'report',
      description: 'Optional vulnerability report to target',
      required: false
    }
  ],
  outputs: [
    {
      id: 'patched-code',
      type: 'patch',
      description: 'Security-patched source code',
      format: 'json'
    },
    {
      id: 'security-report',
      type: 'report',
      description: 'Detailed security analysis report',
      format: 'sarif'
    }
  ],
  dimensions: {
    languages: ['TypeScript', 'JavaScript', 'Python', 'Java', 'C/C++'],
    frameworks: ['Express', 'Spring', 'Django', 'React', 'Angular'],
    analysisDepth: ['ast', 'security-semantics'],
    scope: ['file', 'module', 'package'],
    complexity: { min: 1, max: 100000, unit: 'lines' }
  },
  guarantees: [
    {
      type: 'behavior-preserving',
      description: 'Security patches preserve original behavior',
      verificationMethod: 'differential-testing',
      confidenceLevel: 0.99
    },
    {
      type: 'security-non-regressive',
      description: 'No new security vulnerabilities introduced',
      verificationMethod: 'static-analysis',
      confidenceLevel: 0.95
    }
  ],
  metadata: {
    createdAt: Date.now(),
    updatedAt: Date.now(),
    createdBy: 'GL-System',
    approvalStatus: 'approved',
    tags: ['security', 'patching', 'automatic', 'behavior-preserving'],
    dependencies: ['deep-code-understanding-v1'],
    performanceMetrics: {
      avgExecutionTime: 10000,
      maxMemoryUsage: 1024,
      throughput: 0.1,
      accuracy: 0.98,
      falsePositiveRate: 0.02
    }
  },
  evolution: {
    generation: 1,
    parentIds: [],
    mutationHistory: [],
    performanceHistory: [],
    adaptationRate: 0.05
  }
};