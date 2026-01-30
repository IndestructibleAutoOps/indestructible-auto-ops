// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: code-intelligence-pattern-library
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Code Intelligence & Security Layer - Pattern Library
 * Version 21.0.0
 * Attack/Defense Intelligence Abstraction Templates
 */

import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// Core Pattern Types
// ============================================================================

export interface Pattern {
  id: string;
  name: string;
  category: PatternCategory;
  description: string;
  
  // Pattern structure
  structure: PatternStructure;
  
  // Applicability
  applicability: PatternApplicability;
  
  // Transformation rules
  transformations: PatternTransformation[];
  
  // Validation
  validation: PatternValidation;
  
  // Metadata
  metadata: PatternMetadata;
}

export type PatternCategory = 
  | 'security-hardening'
  | 'performance-optimization'
  | 'architecture-refactoring'
  | 'test-generation'
  | 'documentation-synthesis';

export interface PatternStructure {
  // AST pattern matching
  astPattern?: string;
  
  // Semantic pattern description
  semanticDescription: string;
  
  // Code template
  template?: string;
  
  // Configuration
  configuration: Record<string, any>;
}

export interface PatternApplicability {
  languages: string[];
  frameworks: string[];
  codeTypes: string[];
  minComplexity?: number;
  maxComplexity?: number;
}

export interface PatternTransformation {
  id: string;
  type: 'insertion' | 'replacement' | 'deletion' | 'restructuring';
  description: string;
  rule: TransformationRule;
}

export interface TransformationRule {
  // Match condition
  matchCondition: MatchCondition;
  
  // Transformation action
  action: TransformationAction;
  
  // Safety checks
  safetyChecks: SafetyCheck[];
}

export interface MatchCondition {
  type: 'ast' | 'semantic' | 'control-flow' | 'data-flow';
  pattern: string | object;
  context?: Record<string, any>;
}

export interface TransformationAction {
  type: 'insert-code' | 'replace-code' | 'delete-code' | 'wrap-code' | 'extract-function';
  template?: string;
  parameters?: Record<string, any>;
}

export interface SafetyCheck {
  type: 'behavior-preservation' | 'type-safety' | 'resource-safety' | 'side-effect-check';
  rule: string;
  severity: 'error' | 'warning' | 'info';
}

export interface PatternValidation {
  preConditions: ValidationCondition[];
  postConditions: ValidationCondition[];
  invariants: ValidationCondition[];
}

export interface ValidationCondition {
  type: 'semantic' | 'syntactic' | 'behavioral' | 'performance';
  condition: string;
  checkMethod: 'static' | 'dynamic' | 'formal';
}

export interface PatternMetadata {
  createdAt: number;
  updatedAt: number;
  createdBy: string;
  approved: boolean;
  tags: string[];
  usageCount: number;
  successRate: number;
  evolution: PatternEvolution;
}

export interface PatternEvolution {
  generation: number;
  parentPatterns: string[];
  mutationHistory: PatternMutation[];
  performanceMetrics: PatternPerformanceMetrics;
}

export interface PatternMutation {
  timestamp: number;
  type: 'optimization' | 'generalization' | 'specialization' | 'bugfix';
  description: string;
  impact: number;
}

export interface PatternPerformanceMetrics {
  avgApplicationTime: number;
  successRate: number;
  behaviorPreservationRate: number;
  userSatisfaction: number;
}

// ============================================================================
// Security Hardening Patterns
// ============================================================================

export const INPUT_VALIDATION_PATTERN: Pattern = {
  id: 'input-validation-pattern-v1',
  name: 'Input Validation Pattern',
  category: 'security-hardening',
  description: 'Comprehensive input validation for user-supplied data to prevent injection attacks',
  structure: {
    semanticDescription: 'Validate all user inputs against expected type, format, length, and content before processing',
    configuration: {
      validationLevels: ['type', 'format', 'length', 'content', 'business-rule'],
      stripTags: true,
      escapeSpecialChars: true,
      maxStringLength: 10000
    }
  },
  applicability: {
    languages: ['TypeScript', 'JavaScript', 'Python', 'Java'],
    frameworks: ['Express', 'Spring', 'Django', 'FastAPI'],
    codeTypes: ['function', 'method', 'handler', 'controller']
  },
  transformations: [
    {
      id: 'insert-validation',
      type: 'insertion',
      description: 'Insert input validation at function entry',
      rule: {
        matchCondition: {
          type: 'semantic',
          pattern: 'function-with-user-input',
          context: { hasValidation: false }
        },
        action: {
          type: 'insert-code',
          template: `
// Input validation
if (!validateInput(input)) {
  throw new ValidationError('Invalid input');
}
          `,
          parameters: { input: 'function_parameter' }
        },
        safetyChecks: [
          {
            type: 'behavior-preservation',
            rule: 'Validation must not change valid inputs',
            severity: 'error'
          },
          {
            type: 'side-effect-check',
            rule: 'Validation must have no side effects',
            severity: 'error'
          }
        ]
      }
    }
  ],
  validation: {
    preConditions: [
      {
        type: 'syntactic',
        condition: 'Function has at least one parameter',
        checkMethod: 'static'
      }
    ],
    postConditions: [
      {
        type: 'semantic',
        condition: 'All inputs are validated before use',
        checkMethod: 'static'
      }
    ],
    invariants: [
      {
        type: 'behavioral',
        condition: 'Valid inputs pass through unchanged',
        checkMethod: 'dynamic'
      }
    ]
  },
  metadata: {
    createdAt: Date.now(),
    updatedAt: Date.now(),
    createdBy: 'GL-System',
    approved: true,
    tags: ['security', 'validation', 'injection-prevention', 'input-sanitization'],
    usageCount: 0,
    successRate: 1.0,
    evolution: {
      generation: 1,
      parentPatterns: [],
      mutationHistory: [],
      performanceMetrics: {
        avgApplicationTime: 100,
        successRate: 1.0,
        behaviorPreservationRate: 1.0,
        userSatisfaction: 0.95
      }
    }
  }
};

export const OUTPUT_ENCODING_PATTERN: Pattern = {
  id: 'output-encoding-pattern-v1',
  name: 'Output Encoding Pattern',
  category: 'security-hardening',
  description: 'Encode output to prevent XSS and other injection attacks',
  structure: {
    semanticDescription: 'Encode all dynamic output before rendering to prevent code injection',
    configuration: {
      encodingMethods: ['html', 'javascript', 'css', 'url'],
      contextAware: true,
      autoEscape: true
    }
  },
  applicability: {
    languages: ['TypeScript', 'JavaScript', 'Python', 'Java'],
    frameworks: ['React', 'Vue', 'Angular', 'Express'],
    codeTypes: ['function', 'method', 'template', 'component']
  },
  transformations: [
    {
      id: 'insert-encoding',
      type: 'insertion',
      description: 'Insert output encoding before rendering',
      rule: {
        matchCondition: {
          type: 'semantic',
          pattern: 'dynamic-output-rendering',
          context: { hasEncoding: false }
        },
        action: {
          type: 'wrap-code',
          template: 'escapeOutput(VALUE)',
          parameters: { VALUE: 'output_expression' }
        },
        safetyChecks: [
          {
            type: 'behavior-preservation',
            rule: 'Encoding must preserve content meaning',
            severity: 'error'
          }
        ]
      }
    }
  ],
  validation: {
    preConditions: [
      {
        type: 'syntactic',
        condition: 'Output expression exists',
        checkMethod: 'static'
      }
    ],
    postConditions: [
      {
        type: 'semantic',
        condition: 'All dynamic output is encoded',
        checkMethod: 'static'
      }
    ],
    invariants: [
      {
        type: 'behavioral',
        condition: 'Encoded output displays correctly in browser',
        checkMethod: 'dynamic'
      }
    ]
  },
  metadata: {
    createdAt: Date.now(),
    updatedAt: Date.now(),
    createdBy: 'GL-System',
    approved: true,
    tags: ['security', 'encoding', 'xss-prevention', 'output-sanitization'],
    usageCount: 0,
    successRate: 1.0,
    evolution: {
      generation: 1,
      parentPatterns: [],
      mutationHistory: [],
      performanceMetrics: {
        avgApplicationTime: 50,
        successRate: 1.0,
        behaviorPreservationRate: 1.0,
        userSatisfaction: 0.92
      }
    }
  }
};

// ============================================================================
// Performance Optimization Patterns
// ============================================================================

export const MEMOIZATION_PATTERN: Pattern = {
  id: 'memoization-pattern-v1',
  name: 'Memoization Pattern',
  category: 'performance-optimization',
  description: 'Cache expensive function calls to improve performance',
  structure: {
    semanticDescription: 'Store results of expensive function calls and return cached results for identical inputs',
    configuration: {
      cacheSize: 100,
      ttl: 60000,
      cacheStrategy: 'lru'
    }
  },
  applicability: {
    languages: ['TypeScript', 'JavaScript', 'Python'],
    frameworks: [],
    codeTypes: ['function', 'method'],
    minComplexity: 5
  },
  transformations: [
    {
      id: 'wrap-memoization',
      type: 'insertion',
      description: 'Wrap function with memoization decorator/wrapper',
      rule: {
        matchCondition: {
          type: 'semantic',
          pattern: 'pure-function-with-expensive-computation',
          context: { isMemoized: false }
        },
        action: {
          type: 'wrap-code',
          template: `
const memoizedFn = memoize(FUNCTION, {
  maxSize: ${cacheSize},
  ttl: ${ttl}
});
          `,
          parameters: { 
            FUNCTION: 'function_name',
            cacheSize: 100,
            ttl: 60000
          }
        },
        safetyChecks: [
          {
            type: 'behavior-preservation',
            rule: 'Memoized function must return same results as original',
            severity: 'error'
          },
          {
            type: 'side-effect-check',
            rule: 'Function must be pure (no side effects)',
            severity: 'warning'
          }
        ]
      }
    }
  ],
  validation: {
    preConditions: [
      {
        type: 'semantic',
        condition: 'Function is pure (no side effects)',
        checkMethod: 'static'
      },
      {
        type: 'syntactic',
        condition: 'Function has deterministic return value',
        checkMethod: 'static'
      }
    ],
    postConditions: [
      {
        type: 'performance',
        condition: 'Function execution time reduced by >50% for repeated calls',
        checkMethod: 'dynamic'
      }
    ],
    invariants: [
      {
        type: 'behavioral',
        condition: 'Memoized function produces identical results to original',
        checkMethod: 'dynamic'
      }
    ]
  },
  metadata: {
    createdAt: Date.now(),
    updatedAt: Date.now(),
    createdBy: 'GL-System',
    approved: true,
    tags: ['performance', 'caching', 'memoization', 'optimization'],
    usageCount: 0,
    successRate: 1.0,
    evolution: {
      generation: 1,
      parentPatterns: [],
      mutationHistory: [],
      performanceMetrics: {
        avgApplicationTime: 75,
        successRate: 0.98,
        behaviorPreservationRate: 1.0,
        userSatisfaction: 0.88
      }
    }
  }
};

// ============================================================================
// Architecture Refactoring Patterns
// ============================================================================

export const SINGLE_RESPONSIBILITY_PATTERN: Pattern = {
  id: 'single-responsibility-pattern-v1',
  name: 'Single Responsibility Pattern',
  category: 'architecture-refactoring',
  description: 'Split functions with multiple responsibilities into smaller, focused functions',
  structure: {
    semanticDescription: 'Each function should have one clear responsibility',
    configuration: {
      maxComplexity: 10,
      maxParameters: 5,
      maxLines: 50
    }
  },
  applicability: {
    languages: ['TypeScript', 'JavaScript', 'Python', 'Java'],
    frameworks: [],
    codeTypes: ['function', 'method', 'class']
  },
  transformations: [
    {
      id: 'extract-responsibility',
      type: 'restructuring',
      description: 'Extract separate responsibilities into new functions',
      rule: {
        matchCondition: {
          type: 'semantic',
          pattern: 'function-with-multiple-responsibilities',
          context: { 
            complexity: { gt: 10 },
            lines: { gt: 50 }
          }
        },
        action: {
          type: 'extract-function',
          template: `
function RESPONSIBILITY_NAME(parameters) {
  // Extracted responsibility logic
}
          `,
          parameters: { RESPONSIBILITY_NAME: 'extracted_function_name' }
        },
        safetyChecks: [
          {
            type: 'behavior-preservation',
            rule: 'Extracted functions must preserve original behavior',
            severity: 'error'
          },
          {
            type: 'type-safety',
            rule: 'Type signatures must be preserved',
            severity: 'error'
          }
        ]
      }
    }
  ],
  validation: {
    preConditions: [
      {
        type: 'syntactic',
        condition: 'Function has complexity > 10 or lines > 50',
        checkMethod: 'static'
      }
    ],
    postConditions: [
      {
        type: 'semantic',
        condition: 'Each extracted function has single responsibility',
        checkMethod: 'static'
      },
      {
        type: 'syntactic',
        condition: 'Complexity reduced to < 10',
        checkMethod: 'static'
      }
    ],
    invariants: [
      {
        type: 'behavioral',
        condition: 'Refactored code produces identical results',
        checkMethod: 'dynamic'
      }
    ]
  },
  metadata: {
    createdAt: Date.now(),
    updatedAt: Date.now(),
    createdBy: 'GL-System',
    approved: true,
    tags: ['architecture', 'refactoring', 'clean-code', 'single-responsibility'],
    usageCount: 0,
    successRate: 0.95,
    evolution: {
      generation: 1,
      parentPatterns: [],
      mutationHistory: [],
      performanceMetrics: {
        avgApplicationTime: 200,
        successRate: 0.95,
        behaviorPreservationRate: 0.98,
        userSatisfaction: 0.90
      }
    }
  }
};

// ============================================================================
// Pattern Library Registry
// ============================================================================

export class PatternLibrary {
  private patterns: Map<string, Pattern>;
  private categoryIndex: Map<PatternCategory, Set<string>>;
  private tagIndex: Map<string, Set<string>>;

  constructor() {
    this.patterns = new Map();
    this.categoryIndex = new Map();
    this.tagIndex = new Map();
    
    // Register default patterns
    this.register(INPUT_VALIDATION_PATTERN);
    this.register(OUTPUT_ENCODING_PATTERN);
    this.register(MEMOIZATION_PATTERN);
    this.register(SINGLE_RESPONSIBILITY_PATTERN);
  }

  /**
   * Register a pattern
   */
  public register(pattern: Pattern): void {
    this.patterns.set(pattern.id, pattern);
    
    // Update category index
    if (!this.categoryIndex.has(pattern.category)) {
      this.categoryIndex.set(pattern.category, new Set());
    }
    this.categoryIndex.get(pattern.category)!.add(pattern.id);
    
    // Update tag index
    for (const tag of pattern.metadata.tags) {
      if (!this.tagIndex.has(tag)) {
        this.tagIndex.set(tag, new Set());
      }
      this.tagIndex.get(tag)!.add(pattern.id);
    }
  }

  /**
   * Get pattern by ID
   */
  public get(id: string): Pattern | undefined {
    return this.patterns.get(id);
  }

  /**
   * Get patterns by category
   */
  public getByCategory(category: PatternCategory): Pattern[] {
    const ids = this.categoryIndex.get(category);
    if (!ids) return [];
    
    return Array.from(ids)
      .map(id => this.patterns.get(id)!)
      .filter(p => p !== undefined);
  }

  /**
   * Get patterns by tags
   */
  public getByTag(tag: string): Pattern[] {
    const ids = this.tagIndex.get(tag);
    if (!ids) return [];
    
    return Array.from(ids)
      .map(id => this.patterns.get(id)!)
      .filter(p => p !== undefined);
  }

  /**
   * Search patterns
   */
  public search(query: PatternSearchQuery): Pattern[] {
    let results: Pattern[] = Array.from(this.patterns.values());

    if (query.category) {
      results = results.filter(p => p.category === query.category);
    }

    if (query.languages && query.languages.length > 0) {
      results = results.filter(p => 
        query.languages!.some(lang => p.applicability.languages.includes(lang))
      );
    }

    if (query.frameworks && query.frameworks.length > 0) {
      results = results.filter(p => 
        query.frameworks!.some(fw => p.applicability.frameworks.includes(fw))
      );
    }

    if (query.tags && query.tags.length > 0) {
      results = results.filter(p =>
        query.tags!.some(tag => p.metadata.tags.includes(tag))
      );
    }

    if (query.approved !== undefined) {
      results = results.filter(p => p.metadata.approved === query.approved);
    }

    if (query.minSuccessRate !== undefined) {
      results = results.filter(p => 
        p.metadata.evolution.performanceMetrics.successRate >= query.minSuccessRate!
      );
    }

    return results;
  }

  /**
   * Find applicable patterns for given context
   */
  public findApplicablePatterns(context: PatternContext): Pattern[] {
    return this.patterns.filter(pattern => {
      // Check language applicability
      if (!pattern.applicability.languages.includes(context.language)) {
        return false;
      }

      // Check framework applicability
      if (context.framework && !pattern.applicability.frameworks.includes(context.framework)) {
        return false;
      }

      // Check code type applicability
      if (!pattern.applicability.codeTypes.includes(context.codeType)) {
        return false;
      }

      // Check complexity constraints
      if (pattern.applicability.minComplexity !== undefined) {
        if (context.complexity < pattern.applicability.minComplexity) {
          return false;
        }
      }

      if (pattern.applicability.maxComplexity !== undefined) {
        if (context.complexity > pattern.applicability.maxComplexity) {
          return false;
        }
      }

      return true;
    });
  }

  /**
   * Update pattern usage statistics
   */
  public recordUsage(patternId: string, success: boolean): void {
    const pattern = this.patterns.get(patternId);
    if (!pattern) return;

    pattern.metadata.usageCount++;
    
    // Update success rate
    const totalUsage = pattern.metadata.usageCount;
    const currentSuccessRate = pattern.metadata.evolution.performanceMetrics.successRate;
    const newSuccessRate = ((currentSuccessRate * (totalUsage - 1)) + (success ? 1 : 0)) / totalUsage;
    pattern.metadata.evolution.performanceMetrics.successRate = newSuccessRate;
  }

  /**
   * Get all patterns
   */
  public getAll(): Pattern[] {
    return Array.from(this.patterns.values());
  }

  /**
   * Export patterns as JSON
   */
  public export(): string {
    const data = {
      patterns: Array.from(this.patterns.values()),
      exportedAt: Date.now()
    };
    
    return JSON.stringify(data, null, 2);
  }

  /**
   * Import patterns from JSON
   */
  public import(json: string): void {
    try {
      const data = JSON.parse(json);
      
      if (data.patterns && Array.isArray(data.patterns)) {
        for (const pattern of data.patterns) {
          this.register(pattern);
        }
      }
    } catch (error) {
      throw new Error('Failed to import patterns: Invalid JSON');
    }
  }
}

export interface PatternSearchQuery {
  category?: PatternCategory;
  languages?: string[];
  frameworks?: string[];
  tags?: string[];
  approved?: boolean;
  minSuccessRate?: number;
}

export interface PatternContext {
  language: string;
  framework?: string;
  codeType: string;
  complexity: number;
  features?: string[];
}