// @GL-governed
// @GL-layer: governance
// @GL-semantic: intent-resolver
// @GL-charter-version: 2.0.0

import { ParsedContent } from '../content-parsers';
import { SemanticClassification } from '../semantic-classifiers';
import { GLMapping } from '../gl-mapping';

export interface IntentResolution {
  filePath: string;
  primaryIntent: string;
  secondaryIntents: string[];
  actions: string[];
  requiredCapabilities: string[];
  dependencies: string[];
  recommendations: string[];
  autoRepairCandidate: boolean;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

export class IntentResolver {
  resolve(filePath: string, parsedContent: ParsedContent, classification: SemanticClassification, mapping: GLMapping): IntentResolution {
    const primaryIntent = this.determinePrimaryIntent(filePath, classification);
    const secondaryIntents = this.determineSecondaryIntents(filePath, classification);
    const actions = this.determineActions(filePath, classification, parsedContent);
    const requiredCapabilities = this.determineRequiredCapabilities(classification);
    const dependencies = this.determineDependencies(parsedContent, classification);
    const recommendations = this.generateRecommendations(filePath, classification, mapping);
    const autoRepairCandidate = this.isAutoRepairCandidate(classification, mapping);
    const priority = this.determinePriority(filePath, classification, mapping);

    return {
      filePath,
      primaryIntent,
      secondaryIntents,
      actions,
      requiredCapabilities,
      dependencies,
      recommendations,
      autoRepairCandidate,
      priority
    };
  }

  private determinePrimaryIntent(filePath: string, classification: SemanticClassification): string {
    const pathLower = filePath.toLowerCase();
    
    if (pathLower.includes('orchestrat')) return 'coordinate-multi-agent-execution';
    if (pathLower.includes('policy') || pathLower.includes('validator')) return 'enforce-governance-rules';
    if (pathLower.includes('repair') || pathLower.includes('fix')) return 'automatically-repair-violations';
    if (pathLower.includes('audit') || pathLower.includes('scan')) return 'audit-governance-compliance';
    if (pathLower.includes('deploy')) return 'deploy-changes-to-environment';
    if (pathLower.includes('api') || pathLower.includes('route')) return 'expose-api-endpoints';
    if (pathLower.includes('connector')) return 'integrate-with-external-systems';
    if (pathLower.includes('event')) return 'manage-governance-events';
    if (pathLower.includes('artifact')) return 'store-and-retrieve-artifacts';
    if (pathLower.includes('graph') || pathLower.includes('semantic')) return 'analyze-system-semantics';
    if (pathLower.includes('federation')) return 'coordinate-cross-repo-governance';
    
    // Determine from classification
    if (classification.role === 'agent') return 'execute-automated-tasks';
    if (classification.role === 'pipeline') return 'execute-orchestrated-workflow';
    if (classification.role === 'engine') return 'provide-core-runtime-capabilities';
    
    return 'provide-system-functionality';
  }

  private determineSecondaryIntents(filePath: string, classification: SemanticClassification): string[] {
    const intents: string[] = [];
    const pathLower = filePath.toLowerCase();
    
    // Common secondary intents
    intents.push('maintain-governance-compliance');
    intents.push('log-governance-events');
    
    // Path-specific secondary intents
    if (pathLower.includes('security')) intents.push('enforce-security-policies');
    if (pathLower.includes('quality')) intents.push('ensure-code-quality');
    if (pathLower.includes('monitor')) intents.push('monitor-system-health');
    if (pathLower.includes('sync')) intents.push('synchronize-data');
    if (pathLower.includes('federation')) intents.push('coordinate-across-organizations');
    
    // Classification-based secondary intents
    if (classification.criticality === 'critical' || classification.criticality === 'high') {
      intents.push('support-mission-critical-operations');
    }
    
    if (classification.governanceCompliance.hasGovernedTag) {
      intents.push('adhere-to-gl-governance-standards');
    }
    
    return [...new Set(intents)];
  }

  private determineActions(filePath: string, classification: SemanticClassification, parsedContent: ParsedContent): string[] {
    const actions: string[] = [];
    
    // Actions based on role
    if (classification.role === 'orchestrator') {
      actions.push('coordinate-agents');
      actions.push('manage-task-lifecycle');
      actions.push('handle-dependencies');
      actions.push('monitor-execution');
    }
    
    if (classification.role === 'agent') {
      actions.push('execute-tasks');
      actions.push('report-results');
      actions.push('handle-retries');
    }
    
    if (classification.role === 'validator') {
      actions.push('validate-schema');
      actions.push('check-compliance');
      actions.push('report-violations');
    }
    
    if (classification.role === 'connector') {
      actions.push('scan-repository');
      actions.push('generate-diffs');
      actions.push('create-patches');
      actions.push('apply-changes');
    }
    
    // Actions based on purpose
    if (classification.purpose.includes('audit')) {
      actions.push('scan-files');
      actions.push('validate-policies');
      actions.push('generate-reports');
    }
    
    if (classification.purpose.includes('repair')) {
      actions.push('identify-violations');
      actions.push('generate-fixes');
      actions.push('apply-patches');
    }
    
    if (classification.purpose.includes('api')) {
      actions.push('handle-requests');
      actions.push('validate-input');
      actions.push('execute-operations');
      actions.push('return-responses');
    }
    
    // Actions based on content
    if (parsedContent.functions) {
      actions.push(...parsedContent.functions.map(fn => `execute-${fn}`));
    }
    
    return [...new Set(actions)];
  }

  private determineRequiredCapabilities(classification: SemanticClassification): string[] {
    const capabilities: string[] = [];
    
    // Core capabilities
    capabilities.push('governance-awareness');
    capabilities.push('event-logging');
    capabilities.push('artifact-storage');
    
    // Role-specific capabilities
    if (classification.role === 'orchestrator') {
      capabilities.push('multi-agent-coordination');
      capabilities.push('task-scheduling');
      capabilities.push('dependency-resolution');
    }
    
    if (classification.role === 'validator') {
      capabilities.push('schema-validation');
      capabilities.push('policy-enforcement');
      capabilities.push('violation-detection');
    }
    
    if (classification.role === 'connector') {
      capabilities.push('git-operations');
      capabilities.push('file-system-access');
      capabilities.push('patch-generation');
    }
    
    // Purpose-specific capabilities
    if (classification.purpose.includes('semantic')) {
      capabilities.push('content-parsing');
      capabilities.push('semantic-analysis');
      capabilities.push('gl-mapping');
    }
    
    if (classification.purpose.includes('federation')) {
      capabilities.push('cross-repo-orchestration');
      capabilities.push('trust-validation');
      capabilities.push('event-aggregation');
    }
    
    return [...new Set(capabilities)];
  }

  private determineDependencies(parsedContent: ParsedContent, classification: SemanticClassification): string[] {
    const deps: string[] = [];
    
    // Extract from imports
    if (parsedContent.imports) {
      deps.push(...parsedContent.imports);
    }
    
    // Common governance dependencies
    deps.push('gl-policy-engine');
    deps.push('gl-event-stream');
    deps.push('gl-artifact-store');
    
    // Role-specific dependencies
    if (classification.role === 'orchestrator') {
      deps.push('gl-agent-registry');
      deps.push('task-queue');
    }
    
    if (classification.role === 'validator') {
      deps.push('schema-registry');
      deps.push('policy-store');
    }
    
    if (classification.role === 'connector') {
      deps.push('git-client');
      deps.push('file-scanner');
    }
    
    return [...new Set(deps)];
  }

  private generateRecommendations(filePath: string, classification: SemanticClassification, mapping: GLMapping): string[] {
    const recommendations: string[] = [];
    
    // Governance compliance recommendations
    if (!classification.governanceCompliance.hasGovernedTag) {
      recommendations.push('Add @GL-governed tag');
    }
    if (!classification.governanceCompliance.hasSemanticAnchor) {
      recommendations.push(`Add @GL-semantic: ${mapping.glSemanticAnchor}`);
    }
    if (!classification.governanceCompliance.hasGLLayer) {
      recommendations.push(`Add @GL-layer: ${mapping.glLayer}`);
    }
    if (!classification.governanceCompliance.hasCharterVersion) {
      recommendations.push('Add @GL-charter-version: 2.0.0');
    }
    
    // Path recommendations
    if (mapping.recommendedPath !== filePath) {
      recommendations.push(`Consider moving to recommended path: ${mapping.recommendedPath}`);
    }
    
    // Schema recommendations
    if (!classification.governanceCompliance.schemaCompliant) {
      recommendations.push('Ensure schema compliance with GL standards');
    }
    
    // Criticality-based recommendations
    if (classification.criticality === 'critical') {
      recommendations.push('Add comprehensive error handling');
      recommendations.push('Add health check endpoints');
      recommendations.push('Implement circuit breaker pattern');
    }
    
    return recommendations;
  }

  private isAutoRepairCandidate(classification: SemanticClassification, mapping: GLMapping): boolean {
    // Files are auto-repair candidates if:
    // 1. They have governance compliance issues
    // 2. They have missing tags
    // 3. They have mapping issues
    
    const hasComplianceIssues = !classification.governanceCompliance.hasGovernedTag ||
                                  !classification.governanceCompliance.hasSemanticAnchor ||
                                  !classification.governanceCompliance.hasGLLayer ||
                                  !classification.governanceCompliance.hasCharterVersion;
    
    const hasMissingTags = mapping.missingTags.length > 0;
    const hasIssues = mapping.issues.length > 0;
    
    return hasComplianceIssues || hasMissingTags || hasIssues;
  }

  private determinePriority(filePath: string, classification: SemanticClassification, mapping: GLMapping): IntentResolution['priority'] {
    // Critical: Governance core, orchestration engine, policy engine
    if (classification.criticality === 'critical') return 'critical';
    
    // High: Agents, APIs, connectors, federation components
    if (classification.criticality === 'high') return 'high';
    
    // Medium: Validators, scanners, monitors
    if (classification.criticality === 'medium') return 'medium';
    
    // High priority if it's an auto-repair candidate
    if (this.isAutoRepairCandidate(classification, mapping)) return 'high';
    
    // Low: Documentation, configuration
    return 'low';
  }
}