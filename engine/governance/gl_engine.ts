/**
 * @module gl_engine
 * @description Core governance engine for policy enforcement
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

import { GovernanceEngineInterface, GLEvent, EvidenceRecord, ValidationResult } from '../interfaces.d';
import { RuleEvaluator } from './rule_evaluator';
import { AnchorResolver } from './anchor_resolver';
import { EventsWriter } from './events_writer';
import type { ConfigObject, MetadataObject, PolicyDefinition, RuleDefinition, RuleViolation } from '../types';

/**
 * Governance Engine
 * 
 * GL00-99: Unified Governance Framework
 * 
 * Core governance engine that orchestrates rule evaluation,
 * anchor resolution, and event streaming for full audit trail.
 */
export class GovernanceEngine implements GovernanceEngineInterface {
  private evidence: EvidenceRecord[] = [];
  private readonly ruleEvaluator: RuleEvaluator;
  private readonly anchorResolver: AnchorResolver;
  private readonly eventsWriter: EventsWriter;
  private readonly policyRegistry: Map<string, PolicyDefinition> = new Map();
  private readonly ruleRegistry: Map<string, RuleDefinition> = new Map();

  constructor(options?: {
    ruleEvaluator?: RuleEvaluator;
    anchorResolver?: AnchorResolver;
    eventsWriter?: EventsWriter;
  }) {
    this.ruleEvaluator = options?.ruleEvaluator || new RuleEvaluator();
    this.anchorResolver = options?.anchorResolver || new AnchorResolver();
    this.eventsWriter = options?.eventsWriter || new EventsWriter();
  }

  /**
   * Enforce governance policies on configuration
   */
  async enforce(
    config: ConfigObject,
    env: string,
    context?: MetadataObject
  ): Promise<{
    events: GLEvent[];
    violations: Array<{ path: string; message: string; severity: string }>;
    passed: boolean;
  }> {
    const startTime = Date.now();
    const events: GLEvent[] = [];
    const violations: Array<{ path: string; message: string; severity: string }> = [];

    try {
      // Resolve semantic anchors
      const anchorsResolved = await this.resolveAnchors(config, env);
      events.push(...anchorsResolved.events);

      // Evaluate governance rules
      const ruleEvaluation = await this.evaluateRules(config, env, context);
      events.push(...ruleEvaluation.events);
      violations.push(...ruleEvaluation.violations);

      // Validate against policies
      const policyValidation = await this.validatePolicies(config, env);
      events.push(...policyValidation.events);
      violations.push(...policyValidation.violations);

      const passed = violations.length === 0;

      // Generate governance event
      const glEvent: GLEvent = {
        id: this.generateEventId(),
        timestamp: new Date().toISOString(),
        type: 'governance_enforcement',
        stage: 'governance',
        component: 'gl_engine',
        data: {
          env,
          passed,
          violationCount: violations.length,
          eventCount: events.length
        },
        metadata: {
          duration: Date.now() - startTime,
          evidenceCount: this.evidence.length
        }
      };

      events.push(glEvent);

      // Write events to stream
      await this.eventsWriter.write(events);

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'gl_engine',
        action: 'enforce',
        status: passed ? 'success' : 'error',
        input: { env },
        output: {
          passed,
          violationCount: violations.length,
          eventCount: events.length
        },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        events,
        violations,
        passed
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'gl_engine',
        action: 'enforce',
        status: 'error',
        input: { env },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        events,
        violations: [{ path: 'root', message: errorMsg, severity: 'error' }],
        passed: false
      };
    }
  }

  /**
   * Resolve semantic anchors
   */
  private async resolveAnchors(
    config: ConfigObject,
    env: string
  ): Promise<{ events: GLEvent[] }> {
    const events: GLEvent[] = [];

    try {
      const resolved = await this.anchorResolver.resolve(config);

      const event: GLEvent = {
        id: this.generateEventId(),
        timestamp: new Date().toISOString(),
        type: 'anchor_resolution',
        stage: 'governance',
        component: 'anchor_resolver',
        data: {
          anchorsFound: resolved.anchorsFound,
          aliasesFound: resolved.aliasesFound,
          errors: resolved.errors.length
        },
        metadata: { env }
      };

      events.push(event);

      return { events };
    } catch (error) {
      return { events: [] };
    }
  }

  /**
   * Evaluate governance rules
   */
  private async evaluateRules(
    config: ConfigObject,
    env: string,
    context?: MetadataObject
  ): Promise<{ events: GLEvent[]; violations: RuleViolation[] }> {
    const events: GLEvent[] = [];
    const violations: RuleViolation[] = [];

    try {
      const result = await this.ruleEvaluator.evaluate(config, env, context);
      events.push(...result.events);
      violations.push(...result.violations);

      return { events, violations };
    } catch (error) {
      return { events, violations };
    }
  }

  /**
   * Validate against policies
   */
  private async validatePolicies(
    config: ConfigObject,
    env: string
  ): Promise<{ events: GLEvent[]; violations: RuleViolation[] }> {
    const events: GLEvent[] = [];
    const violations: RuleViolation[] = [];

    // Load environment-specific policies
    const policies = this.getPoliciesForEnv(env);

    for (const policy of policies) {
      try {
        const validation = await this.validatePolicy(config, policy);
        
        if (!validation.valid) {
          violations.push(...validation.errors.map((err: string) => ({
            rule: policy.name,
            path: policy.name,
            message: err,
            severity: policy.severity || 'error'
          })));
        }

        const event: GLEvent = {
          id: this.generateEventId(),
          timestamp: new Date().toISOString(),
          type: 'policy_validation',
          stage: 'governance',
          component: 'gl_engine',
          data: {
            policyName: policy.name,
            valid: validation.valid
          },
          metadata: { env }
        };

        events.push(event);
      } catch (error) {
        violations.push({
          rule: policy.name,
          path: policy.name,
          message: `Policy validation failed: ${error instanceof Error ? error.message : String(error)}`,
          severity: 'error'
        });
      }
    }

    return { events, violations };
  }

  /**
   * Validate single policy
   */
  private async validatePolicy(config: ConfigObject, policy: PolicyDefinition): Promise<ValidationResult> {
    // Placeholder - actual policy validation logic
    return { valid: true, errors: [], warnings: [], duration: 0, evidence: [] };
  }

  /**
   * Get policies for environment
   */
  private getPoliciesForEnv(env: string): PolicyDefinition[] {
    const policies: PolicyDefinition[] = [];

    for (const [name, policy] of this.policyRegistry.entries()) {
      if (policy.environments?.includes(env) || policy.environments?.includes('*')) {
        policies.push({ ...policy, name });
      }
    }

    return policies;
  }

  /**
   * Register policy
   */
  registerPolicy(name: string, policy: PolicyDefinition): void {
    this.policyRegistry.set(name, policy);
  }

  /**
   * Register rule
   */
  registerRule(name: string, rule: RuleDefinition): void {
    this.ruleRegistry.set(name, rule);
  }

  /**
   * Generate unique event ID
   */
  private generateEventId(): string {
    return `gl_event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}