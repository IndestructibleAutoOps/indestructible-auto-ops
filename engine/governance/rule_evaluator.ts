/**
 * @module rule_evaluator
 * @description Governance rule evaluation engine
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-10-OPERATIONAL
 * @gl-module engine/governance
 * @gl-semantic-anchor GL-10-GOV-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import { GLEvent, EvidenceRecord } from '../interfaces.d';
import type { ConfigObject, MetadataObject, RuleDefinition, RuleViolation, CustomRuleEvaluator } from '../types';

/**
 * Rule Evaluator
 * 
 * GL00-99: Unified Governance Framework
 * 
 * Evaluates governance rules against configuration with
 * support for various rule types and custom evaluators.
 */
export class RuleEvaluator {
  private evidence: EvidenceRecord[] = [];
  private readonly ruleRegistry: Map<string, RuleDefinition> = new Map();
  private readonly customEvaluators: Map<string, CustomRuleEvaluator> = new Map();

  constructor() {
    // Register built-in rule types
    this.registerBuiltInRules();
  }

  /**
   * Evaluate rules against configuration
   */
  async evaluate(
    config: ConfigObject,
    env: string,
    context?: MetadataObject
  ): Promise<{
    events: GLEvent[];
    violations: RuleViolation[];
  }> {
    const startTime = Date.now();
    const events: GLEvent[] = [];
    const violations: RuleViolation[] = [];

    try {
      // Get applicable rules
      const rules = this.getApplicableRules(env);

      for (const rule of rules) {
        const result = await this.evaluateRule(config, rule, context);
        
        events.push(...result.events);
        
        if (!result.passed) {
          violations.push({
            rule: rule.name,
            path: rule.path || 'root',
            message: rule.message || `Rule ${rule.name} failed`,
            severity: rule.severity || 'error'
          });
        }
      }

      // Generate summary event
      const summaryEvent: GLEvent = {
        id: this.generateEventId(),
        timestamp: new Date().toISOString(),
        type: 'rule_evaluation',
        stage: 'governance',
        component: 'rule_evaluator',
        data: {
          ruleCount: rules.length,
          violationCount: violations.length,
          env
        },
        metadata: {
          duration: Date.now() - startTime
        }
      };

      events.push(summaryEvent);

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'rule_evaluator',
        action: 'evaluate',
        status: violations.length === 0 ? 'success' : 'warning',
        input: { env, ruleCount: rules.length },
        output: { violationCount: violations.length },
        metrics: { duration: Date.now() - startTime }
      });

      return { events, violations };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'rule_evaluator',
        action: 'evaluate',
        status: 'error',
        input: { env },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        events,
        violations: [{ rule: 'system', path: 'root', message: errorMsg, severity: 'error' }]
      };
    }
  }

  /**
   * Evaluate single rule
   */
  private async evaluateRule(
    config: ConfigObject,
    rule: RuleDefinition,
    context?: MetadataObject
  ): Promise<{ passed: boolean; events: GLEvent[] }> {
    const events: GLEvent[] = [];
    let passed = false;

    try {
      switch (rule.type) {
        case 'required':
          passed = this.evaluateRequiredRule(config, rule);
          break;
        case 'forbidden':
          passed = this.evaluateForbiddenRule(config, rule);
          break;
        case 'pattern':
          passed = this.evaluatePatternRule(config, rule);
          break;
        case 'range':
          passed = this.evaluateRangeRule(config, rule);
          break;
        case 'enum':
          passed = this.evaluateEnumRule(config, rule);
          break;
        case 'custom':
          passed = await this.evaluateCustomRule(config, rule, context);
          break;
        default:
          throw new Error(`Unknown rule type: ${rule.type}`);
      }

      // Generate rule evaluation event
      const event: GLEvent = {
        id: this.generateEventId(),
        timestamp: new Date().toISOString(),
        type: 'rule_evaluation',
        stage: 'governance',
        component: 'rule_evaluator',
        data: {
          ruleName: rule.name,
          ruleType: rule.type,
          path: rule.path,
          passed
        },
        metadata: {}
      };

      events.push(event);

      return { passed, events };
    } catch (error) {
      return { passed: false, events };
    }
  }

  /**
   * Evaluate required rule
   */
  private evaluateRequiredRule(config: ConfigObject, rule: RuleDefinition): boolean {
    const path = rule.path || '';
    const value = this.getValueAtPath(config, path);
    return value !== undefined && value !== null;
  }

  /**
   * Evaluate forbidden rule
   */
  private evaluateForbiddenRule(config: ConfigObject, rule: RuleDefinition): boolean {
    const path = rule.path || '';
    const value = this.getValueAtPath(config, path);
    return value === undefined || value === null;
  }

  /**
   * Validate regex pattern to prevent ReDoS attacks
   * @security Checks for potentially dangerous regex patterns
   */
  private isValidRegexPattern(pattern: string): boolean {
    // Reject empty patterns
    if (!pattern || pattern.length === 0) {
      return false;
    }
    // Reject patterns that are too long (potential ReDoS)
    if (pattern.length > 1000) {
      return false;
    }
    // Reject patterns with nested quantifiers (common ReDoS pattern)
    const dangerousPatterns = [
      /(\+|\*|\?)\s*\1/,  // Consecutive quantifiers
      /\([^)]*(\+|\*)[^)]*\)\s*(\+|\*)/,  // Nested quantifiers
    ];
    for (const dangerous of dangerousPatterns) {
      if (dangerous.test(pattern)) {
        return false;
      }
    }
    // Try to compile the regex to ensure it's valid
    try {
      // nosemgrep: javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp
      new RegExp(pattern);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Evaluate pattern rule
   * @security Pattern is validated before creating RegExp to prevent ReDoS
   */
  private evaluatePatternRule(config: ConfigObject, rule: RuleDefinition): boolean {
    const path = rule.path || '';
    const value = this.getValueAtPath(config, path);
    
    if (typeof value !== 'string') {
      return false;
    }

    const patternStr = rule.pattern || '';
    
    // Security: Validate pattern before creating RegExp
    if (!this.isValidRegexPattern(patternStr)) {
      // Log warning and return false for invalid patterns
      console.warn(`Invalid or potentially dangerous regex pattern rejected: ${patternStr.substring(0, 50)}...`);
      return false;
    }

    // nosemgrep: javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp
    const pattern = new RegExp(patternStr);
    return pattern.test(value);
  }

  /**
   * Evaluate range rule
   */
  private evaluateRangeRule(config: ConfigObject, rule: RuleDefinition): boolean {
    const path = rule.path || '';
    const value = this.getValueAtPath(config, path);

    if (typeof value !== 'number') {
      return false;
    }

    if (rule.min !== undefined && value < rule.min) {
      return false;
    }

    if (rule.max !== undefined && value > rule.max) {
      return false;
    }

    return true;
  }

  /**
   * Evaluate enum rule
   */
  private evaluateEnumRule(config: ConfigObject, rule: RuleDefinition): boolean {
    const path = rule.path || '';
    const value = this.getValueAtPath(config, path);
    return rule.values?.includes(value) ?? false;
  }

  /**
   * Evaluate custom rule
   */
  private async evaluateCustomRule(
    config: ConfigObject,
    rule: RuleDefinition,
    context?: MetadataObject
  ): Promise<boolean> {
    const evaluatorName = (rule as RuleDefinition & { evaluator?: string }).evaluator;
    const evaluator = evaluatorName ? this.customEvaluators.get(evaluatorName) : undefined;

    if (!evaluator) {
      throw new Error(`Custom evaluator not found: ${evaluatorName}`);
    }

    return evaluator(config, rule);
  }

  /**
   * Dangerous keys that could lead to prototype pollution
   */
  private static readonly DANGEROUS_KEYS = new Set([
    '__proto__',
    'constructor',
    'prototype'
  ]);

  /**
   * Get value at path
   * @security Validates keys to prevent prototype pollution attacks
   */
  private getValueAtPath(obj: ConfigObject, path: string): unknown {
    if (!path) return obj;
    
    const keys = path.split('.');
    let current: unknown = obj;

    for (const key of keys) {
      // Security: Prevent prototype pollution by rejecting dangerous keys
      if (RuleEvaluator.DANGEROUS_KEYS.has(key)) {
        console.warn(`Potentially dangerous key rejected: ${key}`);
        return undefined;
      }
      
      if (current === null || current === undefined) {
        return undefined;
      }
      
      // Security: Only access own properties, not inherited ones
      if (typeof current === 'object' && current !== null) {
        if (!Object.prototype.hasOwnProperty.call(current, key)) {
          return undefined;
        }
      }
      
      // Security: Key is validated above against DANGEROUS_KEYS blocklist
      // and hasOwnProperty check ensures only own properties are accessed
      current = (current as Record<string, unknown>)[key]; // nosemgrep
    }

    return current;
  }

  /**
   * Get applicable rules for environment
   */
  private getApplicableRules(env: string): RuleDefinition[] {
    const rules: RuleDefinition[] = [];

    for (const [name, rule] of this.ruleRegistry.entries()) {
      const ruleWithEnv = rule as RuleDefinition & { environments?: string[] };
      if (ruleWithEnv.environments?.includes(env) || ruleWithEnv.environments?.includes('*')) {
        rules.push({ ...rule, name });
      }
    }

    return rules;
  }

  /**
   * Register built-in rules
   */
  private registerBuiltInRules(): void {
    // Naming convention rules
    this.registerRule('kebab-case-names', {
      name: 'kebab-case-names',
      type: 'pattern',
      path: 'name',
      pattern: '^[a-z][a-z0-9-]*$',
      message: 'Name must be in kebab-case',
      severity: 'error'
    });

    // Required fields rule
    this.registerRule('required-metadata', {
      name: 'required-metadata',
      type: 'required',
      path: 'metadata',
      message: 'Metadata is required',
      severity: 'error'
    });
  }

  /**
   * Register rule
   */
  registerRule(name: string, rule: RuleDefinition): void {
    this.ruleRegistry.set(name, rule);
  }

  /**
   * Register custom evaluator
   */
  registerCustomEvaluator(name: string, evaluator: CustomRuleEvaluator): void {
    this.customEvaluators.set(name, evaluator);
  }

  /**
   * Generate unique event ID
   */
  private generateEventId(): string {
    return `rule_event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}